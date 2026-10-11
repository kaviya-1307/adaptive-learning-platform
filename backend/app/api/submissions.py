"""
Submissions & Code Evaluation API Routes.
Provides endpoints to run solutions against visible test cases, submit solutions
against the full test suite, persist submission records, and fetch history.
"""
import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.core.database import get_db
from app.models.problem import Problem
from app.models.submission import Submission
from app.models.user import User
from app.schemas.submission import (
    CodeRunRequest,
    CodeSubmitRequest,
    CodeRunResponse,
    SubmissionResponse,
    SubmissionHistoryItem,
    TestCaseExecutionResult,
)
from app.api.deps import get_current_user, get_current_user_optional, require_diagnostic_completed
from app.engine.code_runner import CodeRunner, PythonCodeRunner, SUPPORTED_LANGUAGES
from app.ml.state_engine import KnowledgeStateEngine
from app.services.recommendation_engine import RecommendationEngine

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/run",
    response_model=CodeRunResponse,
    status_code=status.HTTP_200_OK,
    summary="Run code against visible test cases"
)
def run_code(
    payload: CodeRunRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Executes user solution code against visible test cases for rapid debugging.
    Does NOT save a submission record to the database.
    Diagnostic problems can be run during assessment. General practice problems require diagnostic completion.
    """
    problem = (
        db.query(Problem)
        .options(joinedload(Problem.test_cases))
        .filter(Problem.id == payload.problem_id)
        .first()
    )

    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Problem with id {payload.problem_id} not found."
        )

    # Protect non-diagnostic practice problems with diagnostic gating
    if not problem.is_diagnostic:
        require_diagnostic_completed(current_user)

    # Validate requested language
    req_lang = (payload.language or "python").lower().strip()
    if req_lang not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported language '{payload.language}'. Supported languages: {', '.join(sorted(SUPPORTED_LANGUAGES))}"
        )

    if req_lang not in problem.supported_languages:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Language '{req_lang}' is not supported for problem '{problem.title}'. Supported: {', '.join(problem.supported_languages)}"
        )

    # Filter visible test cases
    visible_tcs = [
        {
            "id": tc.id,
            "input_data": tc.input_data,
            "expected_output": tc.expected_output,
            "is_hidden": tc.is_hidden,
        }
        for tc in sorted(problem.test_cases, key=lambda t: t.order_index)
        if not tc.is_hidden
    ]

    if not visible_tcs:
        # Fallback to all test cases if none marked visible
        visible_tcs = [
            {
                "id": tc.id,
                "input_data": tc.input_data,
                "expected_output": tc.expected_output,
                "is_hidden": False,
            }
            for tc in problem.test_cases
        ]

    starter_code = {
        "python": problem.starter_code_python,
        "java": problem.starter_code_java,
        "cpp": problem.starter_code_cpp,
        "javascript": problem.starter_code_javascript,
    }.get(req_lang, problem.starter_code_python)

    exec_result = CodeRunner.execute(
        code=payload.code,
        test_cases=visible_tcs,
        language=req_lang,
        starter_code=starter_code,
        is_submission=False
    )

    return CodeRunResponse(
        status=exec_result.get("status", "Runtime Error"),
        passed_test_cases=exec_result.get("passed_test_cases", 0),
        total_test_cases=exec_result.get("total_test_cases", len(visible_tcs)),
        execution_time_ms=exec_result.get("execution_time_ms", 0.0),
        compile_error=exec_result.get("compile_error"),
        results=[
            TestCaseExecutionResult(
                test_case_id=r.get("test_case_id", 0),
                status=r.get("status", "Runtime Error"),
                input_data=r.get("input_data"),
                expected_output=r.get("expected_output"),
                actual_output=r.get("actual_output"),
                stdout=r.get("stdout"),
                execution_time_ms=r.get("execution_time_ms", 0.0),
                is_hidden=r.get("is_hidden", False),
                error_message=r.get("error_message")
            )
            for r in exec_result.get("results", [])
        ]
    )


@router.post(
    "/submit",
    response_model=SubmissionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit solution, evaluate against all test cases, and record submission"
)
def submit_code(
    payload: CodeSubmitRequest,
    current_user: User = Depends(require_diagnostic_completed),
    db: Session = Depends(get_db)
):
    """
    Evaluates user code against all visible and hidden test cases.
    Records the final submission result in the MySQL database.
    """
    problem = (
        db.query(Problem)
        .options(joinedload(Problem.test_cases))
        .filter(Problem.id == payload.problem_id)
        .first()
    )

    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Problem with id {payload.problem_id} not found."
        )

    # Validate requested language
    req_lang = (payload.language or "python").lower().strip()
    if req_lang not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported language '{payload.language}'. Supported languages: {', '.join(sorted(SUPPORTED_LANGUAGES))}"
        )

    if req_lang not in problem.supported_languages:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Language '{req_lang}' is not supported for problem '{problem.title}'. Supported: {', '.join(problem.supported_languages)}"
        )

    all_tcs = [
        {
            "id": tc.id,
            "input_data": tc.input_data,
            "expected_output": tc.expected_output,
            "is_hidden": tc.is_hidden,
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
        code=payload.code,
        test_cases=all_tcs,
        language=req_lang,
        starter_code=starter_code,
        is_submission=True
    )

    # Persist submission in database with recorded language
    submission = Submission(
        user_id=current_user.id,
        problem_id=problem.id,
        language=req_lang,
        code=payload.code,
        status=exec_result.get("status", "Runtime Error"),
        passed_test_cases=exec_result.get("passed_test_cases", 0),
        total_test_cases=exec_result.get("total_test_cases", len(all_tcs)),
        execution_time_ms=exec_result.get("execution_time_ms", 0.0)
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)

    logger.info(
        f"Submission #{submission.id} created: user={current_user.id}, problem={problem.slug}, "
        f"language={submission.language}, status={submission.status}, score={submission.passed_test_cases}/{submission.total_test_cases}"
    )

    # Milestone 5 & Phase 2: Update Learner Knowledge State & Concept States
    try:
        KnowledgeStateEngine.update_state_from_submission(
            db=db,
            user_id=current_user.id,
            problem=problem,
            submission=submission
        )
    except Exception as kt_err:
        logger.warning(f"Knowledge state update failed gracefully: {kt_err}")

    # Phase 3 Step 1: Update adaptive recommendation for learner immediately after submission
    try:
        RecommendationEngine.generate_recommendation(
            db=db,
            user_id=current_user.id,
            force_new=True
        )
    except Exception as rec_err:
        logger.warning(f"Next recommendation generation failed gracefully: {rec_err}")

    return SubmissionResponse(
        id=submission.id,
        user_id=submission.user_id,
        problem_id=submission.problem_id,
        language=submission.language,
        status=submission.status,
        passed_test_cases=submission.passed_test_cases,
        total_test_cases=submission.total_test_cases,
        execution_time_ms=submission.execution_time_ms,
        created_at=submission.created_at,
        compile_error=exec_result.get("compile_error"),
        results=[
            TestCaseExecutionResult(
                test_case_id=r.get("test_case_id", 0),
                status=r.get("status", "Runtime Error"),
                input_data=r.get("input_data"),
                expected_output=r.get("expected_output"),
                actual_output=r.get("actual_output"),
                stdout=r.get("stdout"),
                execution_time_ms=r.get("execution_time_ms", 0.0),
                is_hidden=r.get("is_hidden", False),
                error_message=r.get("error_message")
            )
            for r in exec_result.get("results", [])
        ]
    )


@router.get(
    "/history/{problem_id}",
    response_model=List[SubmissionHistoryItem],
    status_code=status.HTTP_200_OK,
    summary="Get user's past submission history for a problem"
)
def get_submission_history(
    problem_id: int,
    current_user: User = Depends(require_diagnostic_completed),
    db: Session = Depends(get_db)
):
    """
    Returns list of past submissions by the current user for the given problem.
    """
    submissions = (
        db.query(Submission)
        .filter(
            Submission.user_id == current_user.id,
            Submission.problem_id == problem_id
        )
        .order_by(Submission.created_at.desc())
        .all()
    )
    return submissions


@router.get(
    "/{submission_id}",
    response_model=SubmissionHistoryItem,
    status_code=status.HTTP_200_OK,
    summary="Get details of a single past submission"
)
def get_submission_detail(
    submission_id: int,
    current_user: User = Depends(require_diagnostic_completed),
    db: Session = Depends(get_db)
):
    """
    Returns submission metadata for the given submission ID.
    """
    submission = (
        db.query(Submission)
        .filter(
            Submission.id == submission_id,
            Submission.user_id == current_user.id
        )
        .first()
    )

    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Submission #{submission_id} not found."
        )

    return submission
