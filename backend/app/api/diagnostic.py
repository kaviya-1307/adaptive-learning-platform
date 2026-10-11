import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql import func

from app.core.database import get_db
from app.models.problem import Problem
from app.models.topic import Topic
from app.models.diagnostic_attempt import DiagnosticAttempt
from app.models.learner_knowledge_state import LearnerKnowledgeState
from app.models.user import User
from app.schemas.problem import (
    ProblemSummary,
    TopicResponse,
    DiagnosticAttemptCreate,
    DiagnosticAttemptResponse,
    DiagnosticCompleteResponse,
    DiagnosticScoreResponse,
)
from app.api.deps import get_current_user, get_current_user_optional
from app.ml.state_engine import KnowledgeStateEngine
from app.services.recommendation_engine import RecommendationEngine
from app.engine.code_runner import CodeRunner

logger = logging.getLogger(__name__)
router = APIRouter()

# Experience-based initial mastery mapping (shared with onboarding)
EXPERIENCE_PRIOR_MAP = {
    "beginner": {"mastery": 0.25, "confidence": 0.30},
    "intermediate": {"mastery": 0.50, "confidence": 0.40},
    "advanced": {"mastery": 0.75, "confidence": 0.50},
}


@router.get(
    "/status",
    status_code=status.HTTP_200_OK,
    summary="Get the current user's diagnostic assessment status"
)
def get_diagnostic_status(
    current_user: User = Depends(get_current_user)
):
    """
    Returns the authoritative diagnostic completion status and metadata for the current user.
    """
    total = current_user.diagnostic_total
    score = current_user.diagnostic_score
    score_percent = round((score / total) * 100, 1) if (total and score is not None and total > 0) else None
    return {
        "diagnostic_completed": bool(current_user.diagnostic_completed),
        "diagnostic_exempt": bool(current_user.diagnostic_exempt),
        "diagnostic_score": score,
        "diagnostic_total": total,
        "score_percent": score_percent,
        "diagnostic_completed_at": current_user.diagnostic_completed_at,
        "can_take_diagnostic": not current_user.diagnostic_completed and not current_user.diagnostic_exempt
    }


@router.get(
    "/problems",
    response_model=List[ProblemSummary],
    status_code=status.HTTP_200_OK,
    summary="Get the diagnostic problem suite (6-8 flagged problems)"
)
def get_diagnostic_problems(
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """
    Returns all problems flagged as diagnostic (is_diagnostic=True).
    These form the initial 6-8 problem assessment used to calibrate
    the learner's prior knowledge state.
    Rejects completed students from restarting the diagnostic.
    """
    if current_user and getattr(current_user, "diagnostic_completed", False):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Diagnostic assessment has already been completed."
        )

    problems = (
        db.query(Problem)
        .options(joinedload(Problem.topic))
        .join(Topic, Problem.topic_id == Topic.id)
        .filter(Problem.is_diagnostic == True)
        .order_by(Problem.order_index.asc())
        .all()
    )

    if not problems:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No diagnostic problems found. Please ensure the database has been seeded."
        )

    return problems


@router.post(
    "/submit",
    response_model=DiagnosticAttemptResponse,
    status_code=status.HTTP_200_OK,
    summary="Submit a single diagnostic problem attempt"
)
def submit_diagnostic_attempt(
    payload: DiagnosticAttemptCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Records a single diagnostic problem attempt with server-authoritative evaluation.
    If code is submitted, evaluates it using CodeRunner against test cases.
    Rejects attempts if the diagnostic has already been completed.
    """
    if getattr(current_user, "diagnostic_completed", False):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Diagnostic assessment has already been completed."
        )

    # Verify problem exists and is diagnostic
    problem = (
        db.query(Problem)
        .options(joinedload(Problem.test_cases))
        .filter(Problem.id == payload.problem_id, Problem.is_diagnostic == True)
        .first()
    )

    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Diagnostic problem with id {payload.problem_id} not found."
        )

    req_lang = (payload.language or "python").lower()
    supported = problem.supported_languages or ["python"]
    if req_lang not in supported:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Language '{req_lang}' is not supported for diagnostic problem '{problem.title}'. Supported: {supported}"
        )

    exec_result = None
    code_raw = payload.code_submitted
    code_str = (code_raw or "").strip()
    if not code_str:
        is_solved = False
        exec_result = {
            "status": "Compilation Error",
            "passed_test_cases": 0,
            "total_test_cases": len(problem.test_cases) if problem.test_cases else 1,
            "compile_error": "Code submission is required and cannot be empty.",
            "runtime_error": None,
            "results": []
        }
    else:
        all_tcs = [
            {
                "id": tc.id,
                "input_data": tc.input_data,
                "expected_output": tc.expected_output,
                "is_hidden": tc.is_hidden
            }
            for tc in sorted(problem.test_cases, key=lambda t: t.order_index)
        ]
        starter_code = {
            "python": problem.starter_code_python,
            "java": problem.starter_code_java,
            "cpp": problem.starter_code_cpp,
            "javascript": problem.starter_code_javascript,
        }.get(req_lang, problem.starter_code_python)

        exec_result = CodeRunner.execute(
            code=payload.code_submitted,
            test_cases=all_tcs,
            language=req_lang,
            starter_code=starter_code,
            is_submission=True
        )
        is_solved = (exec_result.get("status") == "Accepted")

    # Upsert attempt
    attempt = db.query(DiagnosticAttempt).filter(
        DiagnosticAttempt.user_id == current_user.id,
        DiagnosticAttempt.problem_id == payload.problem_id
    ).first()

    if attempt:
        attempt.is_solved = is_solved
        attempt.attempts_count += 1
        attempt.time_spent_seconds = payload.time_spent_seconds
        attempt.code_submitted = payload.code_submitted
        attempt.language = req_lang
    else:
        attempt = DiagnosticAttempt(
            user_id=current_user.id,
            problem_id=payload.problem_id,
            is_solved=is_solved,
            attempts_count=1,
            time_spent_seconds=payload.time_spent_seconds,
            code_submitted=payload.code_submitted,
            language=req_lang
        )
        db.add(attempt)

    db.commit()
    db.refresh(attempt)

    resp = DiagnosticAttemptResponse.model_validate(attempt)
    if exec_result:
        resp.passed_test_cases = exec_result.get("passed_test_cases")
        resp.total_test_cases = exec_result.get("total_test_cases")
        resp.status = exec_result.get("status")
        resp.compile_error = exec_result.get("compile_error")
        resp.runtime_error = exec_result.get("runtime_error")
    return resp


@router.post(
    "/complete",
    response_model=DiagnosticCompleteResponse,
    status_code=status.HTTP_200_OK,
    summary="Finalize the diagnostic and initialize learner knowledge states"
)
def complete_diagnostic(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Finalizes the diagnostic session.
    Computes per-topic mastery from diagnostic results, then initializes or
    updates LearnerKnowledgeState for each topic. Topics covered in the
    diagnostic receive data-driven mastery. Topics without diagnostic data
    use the user's onboarding prior (or default 0.25).
    Permanently marks diagnostic_completed=True on the user.
    """
    if getattr(current_user, "diagnostic_completed", False):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Diagnostic assessment has already been completed."
        )
    # Fetch all diagnostic problem ids
    diagnostic_problems = db.query(Problem).filter(Problem.is_diagnostic == True).all()
    total_problems = len(diagnostic_problems)

    if total_problems == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No diagnostic problems found in the database. Seed the database first."
        )

    # Fetch user's diagnostic attempts
    attempts = db.query(DiagnosticAttempt).filter(
        DiagnosticAttempt.user_id == current_user.id
    ).all()

    attempt_map = {a.problem_id: a for a in attempts}
    solved_count = sum(1 for a in attempts if a.is_solved)

    # Build per-topic mastery from diagnostic results
    topic_results: dict = {}  # topic_id -> {solved: int, total: int}
    for problem in diagnostic_problems:
        tid = problem.topic_id
        if tid not in topic_results:
            topic_results[tid] = {"solved": 0, "total": 0}
        topic_results[tid]["total"] += 1
        attempt = attempt_map.get(problem.id)
        if attempt and attempt.is_solved:
            topic_results[tid]["solved"] += 1

    # Determine the onboarding prior (fallback)
    profile = current_user.onboarding_profile
    experience_level = profile.experience_level if profile else "beginner"
    prior = EXPERIENCE_PRIOR_MAP.get(experience_level, {"mastery": 0.25, "confidence": 0.30})

    # Update or create LearnerKnowledgeState for ALL topics
    all_topics = db.query(Topic).all()
    k_states_initialized = 0

    for topic in all_topics:
        # Data-driven mastery for topics covered in diagnostic
        if topic.id in topic_results and topic_results[topic.id]["total"] > 0:
            t_res = topic_results[topic.id]
            mastery = t_res["solved"] / t_res["total"]
            confidence = 0.60 if t_res["total"] >= 2 else 0.45
        else:
            # Fall back to onboarding prior
            mastery = prior["mastery"]
            confidence = prior["confidence"]

        existing = db.query(LearnerKnowledgeState).filter(
            LearnerKnowledgeState.user_id == current_user.id,
            LearnerKnowledgeState.topic_id == topic.id
        ).first()

        if existing:
            existing.mastery_score = mastery
            existing.confidence_score = confidence
            existing.total_interactions = existing.total_interactions + (
                topic_results.get(topic.id, {}).get("total", 0)
            )
        else:
            new_state = LearnerKnowledgeState(
                user_id=current_user.id,
                topic_id=topic.id,
                mastery_score=mastery,
                confidence_score=confidence,
                total_interactions=topic_results.get(topic.id, {}).get("total", 0)
            )
            db.add(new_state)

        k_states_initialized += 1

    db.commit()

    # Initialize / update granular concept states from diagnostic evidence (Phase 2 Step 4)
    KnowledgeStateEngine.update_concept_states_from_diagnostic(db, current_user.id)

    # Phase 3 Step 1: Initialize personalized problem recommendation from calibrated concept states
    try:
        RecommendationEngine.generate_recommendation(
            db=db,
            user_id=current_user.id,
            force_new=True
        )
    except Exception as rec_err:
        logger.warning(f"Initial recommendation generation after diagnostic failed gracefully: {rec_err}")

    score_percent = round((solved_count / total_problems) * 100, 1) if total_problems > 0 else 0.0

    # Phase 2: Authoritative diagnostic completion persistence
    current_user.diagnostic_completed = True
    current_user.diagnostic_score = solved_count
    current_user.diagnostic_total = total_problems
    current_user.diagnostic_completed_at = func.now()
    db.commit()
    db.refresh(current_user)

    return DiagnosticCompleteResponse(
        message="Diagnostic completed. Learner knowledge states have been initialized.",
        total_problems=total_problems,
        solved_count=solved_count,
        score_percent=score_percent,
        knowledge_states_initialized=k_states_initialized
    )


@router.get(
    "/history",
    response_model=List[DiagnosticAttemptResponse],
    status_code=status.HTTP_200_OK,
    summary="Get the current user's diagnostic history"
)
def get_diagnostic_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns all diagnostic attempts for the authenticated user.
    """
    attempts = (
        db.query(DiagnosticAttempt)
        .filter(DiagnosticAttempt.user_id == current_user.id)
        .order_by(DiagnosticAttempt.created_at)
        .all()
    )
    return attempts


@router.get(
    "/score",
    response_model=DiagnosticScoreResponse,
    status_code=status.HTTP_200_OK,
    summary="Get the completed diagnostic score and summary for the current user"
)
def get_diagnostic_score(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns the authoritative diagnostic score, completion timestamp,
    summary metrics, and per-problem breakdown for a student who has completed the diagnostic.
    Rejects with 400 Bad Request if diagnostic is not completed.
    """
    if not getattr(current_user, "diagnostic_completed", False):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Diagnostic assessment has not been completed yet."
        )

    # Fetch attempts
    attempts = (
        db.query(DiagnosticAttempt)
        .filter(DiagnosticAttempt.user_id == current_user.id)
        .order_by(DiagnosticAttempt.created_at)
        .all()
    )

    total = current_user.diagnostic_total or len(attempts) or 7
    solved = current_user.diagnostic_score if current_user.diagnostic_score is not None else sum(1 for a in attempts if a.is_solved)
    score_percent = round((solved / total) * 100, 1) if total > 0 else 0.0

    k_states_count = (
        db.query(LearnerKnowledgeState)
        .filter(LearnerKnowledgeState.user_id == current_user.id)
        .count()
    ) or 10

    return DiagnosticScoreResponse(
        diagnostic_completed=True,
        diagnostic_score=solved,
        diagnostic_total=total,
        score=solved,
        total=total,
        score_percent=score_percent,
        status="completed",
        completed_at=current_user.diagnostic_completed_at,
        diagnostic_completed_at=current_user.diagnostic_completed_at,
        knowledge_states_initialized=k_states_count,
        attempts=attempts
    )
