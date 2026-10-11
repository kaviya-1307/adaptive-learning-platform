"""
Admin API Router Foundation & Performance Monitoring (Phase 5).
Provides protected endpoints for authorized administrators to:
1. Probe admin service status (GET /status)
2. View platform-wide learning activity metrics (GET /overview)
3. Monitor registered students and their learning progress (GET /users)
4. Inspect individual student learning history and concept mastery (GET /users/{user_id})
5. Extract sanitized live student dataset for faculty/research evaluation (GET /export)

Security Guarantees:
- Every endpoint requires ADMIN role via require_admin dependency.
- Passwords, password hashes, and JWT tokens are NEVER exposed.
- Raw source code and diagnostic answers are excluded from summary/monitoring responses.
"""
import csv
import io
import logging
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, or_

from app.core.database import get_db
from app.api.deps import require_admin
from app.models.user import User, UserRole
from app.models.problem import Problem
from app.models.onboarding import OnboardingProfile
from app.models.submission import Submission
from app.models.diagnostic_attempt import DiagnosticAttempt
from app.models.recommendation import Recommendation
from app.models.learner_knowledge_state import LearnerKnowledgeState
from app.models.learner_concept_state import LearnerConceptState
from app.models.topic import Topic
from app.schemas.admin import (
    AdminOverviewStats,
    AdminStudentListItem,
    AdminStudentListResponse,
    AdminDiagnosticSummaryItem,
    AdminSubmissionSummaryItem,
    AdminTopicMasteryItem,
    AdminConceptWeaknessItem,
    AdminRecommendationSummaryItem,
    AdminStudentDetailResponse,
    AdminExportStudentItem,
    AdminExportResponse,
)

logger = logging.getLogger(__name__)
router = APIRouter()


class AdminStatusResponse(BaseModel):
    status: str
    message: str
    admin_email: str
    role: str


@router.get(
    "/status",
    response_model=AdminStatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Admin service authorization probe"
)
def get_admin_status(
    admin_user: User = Depends(require_admin)
):
    """
    Protected verification endpoint requiring ADMIN role.
    """
    return AdminStatusResponse(
        status="ok",
        message="Admin authorization verified successfully.",
        admin_email=admin_user.email,
        role=admin_user.role,
    )


@router.get(
    "/overview",
    response_model=AdminOverviewStats,
    status_code=status.HTTP_200_OK,
    summary="Get platform-wide student participation and learning analytics"
)
def get_admin_overview(
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Returns aggregated platform metrics for all registered students:
    - Total students
    - Onboarding completed count
    - Diagnostic completed count
    - Total submissions and accepted submissions count
    - Active students count
    - Total recommendations generated
    - Submission breakdown by programming language
    """
    # 1. Total registered students
    total_students = db.query(User).filter(User.role == UserRole.STUDENT).count()

    # 2. Onboarding completed count
    onboarding_completed = (
        db.query(OnboardingProfile)
        .join(User, OnboardingProfile.user_id == User.id)
        .filter(User.role == UserRole.STUDENT)
        .count()
    )

    # 3. Diagnostic completed count
    diagnostic_completed = (
        db.query(User)
        .filter(User.role == UserRole.STUDENT, User.diagnostic_completed == True)
        .count()
    )

    # 4. Submission metrics
    total_subs = db.query(Submission).count()
    solved_subs = db.query(Submission).filter(Submission.status == "Accepted").count()

    # Submissions by language
    lang_rows = (
        db.query(Submission.language, func.count(Submission.id))
        .group_by(Submission.language)
        .all()
    )
    lang_breakdown = {lang or "python": count for lang, count in lang_rows}

    # 5. Active students: distinct students with at least 1 submission or diagnostic attempt
    sub_user_ids = {r[0] for r in db.query(Submission.user_id).distinct().all()}
    diag_user_ids = {r[0] for r in db.query(DiagnosticAttempt.user_id).distinct().all()}
    active_user_ids = sub_user_ids.union(diag_user_ids)
    active_students_count = len(active_user_ids)

    # 6. Total recommendations
    total_recs = db.query(Recommendation).count()

    return AdminOverviewStats(
        total_registered_students=total_students,
        onboarding_completed_count=onboarding_completed,
        diagnostic_completed_count=diagnostic_completed,
        total_submissions_count=total_subs,
        total_solved_submissions_count=solved_subs,
        active_students_count=active_students_count,
        total_recommendations_count=total_recs,
        submissions_by_language=lang_breakdown
    )


@router.get(
    "/users",
    response_model=AdminStudentListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get sanitized list of monitored students with performance metrics"
)
def get_admin_students(
    search: Optional[str] = Query(None, description="Search by student name or email"),
    diagnostic_filter: Optional[str] = Query("all", description="Filter by diagnostic: 'all', 'completed', 'pending'"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Returns a sanitized, paginated list of registered students for administrator monitoring.
    Never exposes passwords, hashes, JWT tokens, or raw code.
    """
    query = db.query(User).filter(User.role == UserRole.STUDENT)

    if search:
        search_term = f"%{search.strip().lower()}%"
        query = query.filter(or_(
            func.lower(User.name).like(search_term),
            func.lower(User.email).like(search_term)
        ))

    if diagnostic_filter == "completed":
        query = query.filter(User.diagnostic_completed == True)
    elif diagnostic_filter == "pending":
        query = query.filter(User.diagnostic_completed == False)

    total_count = query.count()
    users = query.order_by(User.id.desc()).offset(skip).limit(limit).all()

    if not users:
        return AdminStudentListResponse(total_count=total_count, students=[])

    user_ids = [u.id for u in users]

    # Pre-fetch onboarding profiles
    onboarding_map = {
        p.user_id: p for p in db.query(OnboardingProfile).filter(OnboardingProfile.user_id.in_(user_ids)).all()
    }

    # Aggregate submission counts per user
    sub_counts = dict(
        db.query(Submission.user_id, func.count(Submission.id))
        .filter(Submission.user_id.in_(user_ids))
        .group_by(Submission.user_id)
        .all()
    )

    # Aggregate distinct solved problems per user
    solved_counts = dict(
        db.query(Submission.user_id, func.count(func.distinct(Submission.problem_id)))
        .filter(Submission.user_id.in_(user_ids), Submission.status == "Accepted")
        .group_by(Submission.user_id)
        .all()
    )

    # Compute latest activity timestamp per user across submissions, diagnostic attempts, and onboarding
    latest_subs = dict(
        db.query(Submission.user_id, func.max(Submission.created_at))
        .filter(Submission.user_id.in_(user_ids))
        .group_by(Submission.user_id)
        .all()
    )
    latest_diags = dict(
        db.query(DiagnosticAttempt.user_id, func.max(DiagnosticAttempt.created_at))
        .filter(DiagnosticAttempt.user_id.in_(user_ids))
        .group_by(DiagnosticAttempt.user_id)
        .all()
    )

    student_items: List[AdminStudentListItem] = []
    for u in users:
        ob = onboarding_map.get(u.id)
        t_sub = sub_counts.get(u.id, 0)
        s_count = solved_counts.get(u.id, 0)

        # Derive latest activity
        activity_candidates = [u.created_at]
        if ob and ob.completed_at:
            activity_candidates.append(ob.completed_at)
        if u.id in latest_subs and latest_subs[u.id]:
            activity_candidates.append(latest_subs[u.id])
        if u.id in latest_diags and latest_diags[u.id]:
            activity_candidates.append(latest_diags[u.id])

        last_active = max(activity_candidates) if activity_candidates else u.created_at

        student_items.append(AdminStudentListItem(
            id=u.id,
            name=u.name,
            email=u.email,
            role=u.role,
            created_at=u.created_at,
            onboarding_completed=ob is not None,
            learning_goal=ob.learning_goal if ob else None,
            experience_level=ob.experience_level if ob else None,
            diagnostic_completed=bool(u.diagnostic_completed),
            diagnostic_score=u.diagnostic_score,
            diagnostic_total=u.diagnostic_total,
            diagnostic_completed_at=u.diagnostic_completed_at,
            total_submissions=t_sub,
            solved_problems_count=s_count,
            last_activity_at=last_active
        ))

    return AdminStudentListResponse(total_count=total_count, students=student_items)


@router.get(
    "/users/{user_id}",
    response_model=AdminStudentDetailResponse,
    status_code=status.HTTP_200_OK,
    summary="Inspect individual student learning record and performance history"
)
def get_admin_student_detail(
    user_id: int,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Inspects a single student's complete learning journey for faculty/administrative evaluation:
    - Profile & onboarding
    - Diagnostic attempts log (without exposing solution code)
    - Submissions statistics and recent submission history
    - 10-topic knowledge states
    - Granular concept mastery & weakness ratings
    - Recommendation history
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student #{user_id} not found."
        )

    # 1. Onboarding
    ob = user.onboarding_profile

    # 2. Diagnostic attempts summary
    diag_attempts = (
        db.query(DiagnosticAttempt)
        .filter(DiagnosticAttempt.user_id == user.id)
        .order_by(DiagnosticAttempt.created_at.asc())
        .all()
    )
    prob_ids = [d.problem_id for d in diag_attempts]
    prob_map = {p.id: p for p in db.query(Problem).filter(Problem.id.in_(prob_ids)).all()} if prob_ids else {}

    diag_summary: List[AdminDiagnosticSummaryItem] = [
        AdminDiagnosticSummaryItem(
            problem_id=da.problem_id,
            problem_title=prob_map.get(da.problem_id).title if prob_map.get(da.problem_id) else f"Problem #{da.problem_id}",
            is_solved=da.is_solved,
            attempts_count=da.attempts_count,
            time_spent_seconds=da.time_spent_seconds,
            created_at=da.created_at
        )
        for da in diag_attempts
    ]

    # 3. Submissions summary & breakdown
    submissions = (
        db.query(Submission)
        .filter(Submission.user_id == user.id)
        .order_by(Submission.created_at.desc())
        .all()
    )
    sub_prob_ids = [s.problem_id for s in submissions]
    sub_prob_map = {p.id: p for p in db.query(Problem).filter(Problem.id.in_(sub_prob_ids)).all()} if sub_prob_ids else {}

    sub_status_breakdown: Dict[str, int] = {}
    sub_lang_breakdown: Dict[str, int] = {}
    for s in submissions:
        sub_status_breakdown[s.status] = sub_status_breakdown.get(s.status, 0) + 1
        lang = s.language or "python"
        sub_lang_breakdown[lang] = sub_lang_breakdown.get(lang, 0) + 1

    solved_count = len({s.problem_id for s in submissions if s.status == "Accepted"})

    recent_subs: List[AdminSubmissionSummaryItem] = [
        AdminSubmissionSummaryItem(
            submission_id=s.id,
            problem_id=s.problem_id,
            problem_title=sub_prob_map.get(s.problem_id).title if sub_prob_map.get(s.problem_id) else f"Problem #{s.problem_id}",
            language=s.language or "python",
            status=s.status,
            passed_test_cases=s.passed_test_cases,
            total_test_cases=s.total_test_cases,
            execution_time_ms=s.execution_time_ms,
            created_at=s.created_at
        )
        for s in submissions[:20]
    ]

    # 4. Topic mastery breakdown
    topic_rows = db.query(Topic).order_by(Topic.order_index.asc()).all()
    t_name_map = {t.id: t.name for t in topic_rows}
    k_states = (
        db.query(LearnerKnowledgeState)
        .filter(LearnerKnowledgeState.user_id == user.id)
        .all()
    )
    topic_masteries: List[AdminTopicMasteryItem] = [
        AdminTopicMasteryItem(
            topic_id=ks.topic_id,
            topic_name=t_name_map.get(ks.topic_id, f"Topic #{ks.topic_id}"),
            mastery_score=round(ks.mastery_score, 3),
            confidence_score=round(ks.confidence_score, 3),
            total_interactions=ks.total_interactions
        )
        for ks in k_states
    ]

    # 5. Top weak concepts
    c_states = (
        db.query(LearnerConceptState)
        .filter(LearnerConceptState.user_id == user.id)
        .order_by(LearnerConceptState.weakness_score.desc())
        .limit(10)
        .all()
    )
    top_weak: List[AdminConceptWeaknessItem] = [
        AdminConceptWeaknessItem(
            concept=cs.concept,
            mastery_score=round(cs.mastery_score, 3),
            weakness_score=round(cs.weakness_score, 3),
            weakness_level=cs.weakness_level,
            interactions=cs.interactions,
            solved_count=cs.solved_count
        )
        for cs in c_states
    ]

    # 6. Recommendation history
    recs = (
        db.query(Recommendation)
        .filter(Recommendation.user_id == user.id)
        .order_by(Recommendation.created_at.desc())
        .limit(10)
        .all()
    )
    rec_prob_ids = [r.problem_id for r in recs]
    rec_prob_map = {p.id: p for p in db.query(Problem).filter(Problem.id.in_(rec_prob_ids)).all()} if rec_prob_ids else {}

    rec_history: List[AdminRecommendationSummaryItem] = [
        AdminRecommendationSummaryItem(
            recommendation_id=r.id,
            problem_id=r.problem_id,
            problem_title=rec_prob_map.get(r.problem_id).title if rec_prob_map.get(r.problem_id) else f"Problem #{r.problem_id}",
            difficulty=rec_prob_map.get(r.problem_id).difficulty if rec_prob_map.get(r.problem_id) else "Medium",
            topic_name=rec_prob_map.get(r.problem_id).topic_name if rec_prob_map.get(r.problem_id) else "General",
            recommendation_reason=getattr(r, "recommendation_reason", None) or getattr(r, "primary_weak_concept", None),
            created_at=r.created_at
        )
        for r in recs
    ]

    # 7. Last activity
    activity_dates = [user.created_at]
    if ob and ob.completed_at:
        activity_dates.append(ob.completed_at)
    if diag_attempts:
        activity_dates.append(diag_attempts[-1].created_at)
    if submissions:
        activity_dates.append(submissions[0].created_at)
    last_active = max(activity_dates)

    return AdminStudentDetailResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role,
        created_at=user.created_at,
        onboarding_completed=ob is not None,
        learning_goal=ob.learning_goal if ob else None,
        experience_level=ob.experience_level if ob else None,
        diagnostic_completed=bool(user.diagnostic_completed),
        diagnostic_score=user.diagnostic_score,
        diagnostic_total=user.diagnostic_total,
        diagnostic_completed_at=user.diagnostic_completed_at,
        diagnostic_attempts=diag_summary,
        total_submissions=len(submissions),
        solved_problems_count=solved_count,
        submissions_by_status=sub_status_breakdown,
        submissions_by_language=sub_lang_breakdown,
        recent_submissions=recent_subs,
        topic_mastery=topic_masteries,
        top_weak_concepts=top_weak,
        recent_recommendations=rec_history,
        last_activity_at=last_active
    )


@router.get(
    "/export",
    summary="Extract sanitized live student dataset for faculty evaluation & research",
    response_description="Returns JSON dataset or downloadable CSV file of student activity"
)
def export_admin_live_dataset(
    format: str = Query("json", description="Export format: 'json' or 'csv'"),
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    ADMIN-only research export extracting accumulated live student learning data.
    Sanitized to completely omit passwords, hashes, tokens, and raw solution code.
    Supports JSON and CSV formats.
    """
    students = (
        db.query(User)
        .filter(User.role == UserRole.STUDENT)
        .order_by(User.id.asc())
        .all()
    )

    if not students:
        if format.lower() == "csv":
            return Response(
                content="student_id,name,email,role,registration_date\n",
                media_type="text/csv",
                headers={"Content-Disposition": "attachment; filename=adaptive_learning_live_dataset.csv"}
            )
        return AdminExportResponse(exported_at=datetime.now(timezone.utc), total_students=0, dataset=[])

    user_ids = [s.id for s in students]

    # Pre-fetch onboarding
    onboarding_map = {
        p.user_id: p for p in db.query(OnboardingProfile).filter(OnboardingProfile.user_id.in_(user_ids)).all()
    }

    # Pre-fetch submission stats
    all_subs = db.query(Submission).filter(Submission.user_id.in_(user_ids)).all()
    user_subs_map: Dict[int, List[Submission]] = {}
    for sub in all_subs:
        user_subs_map.setdefault(sub.user_id, []).append(sub)

    # Pre-fetch average mastery
    avg_masteries = dict(
        db.query(LearnerKnowledgeState.user_id, func.avg(LearnerKnowledgeState.mastery_score))
        .filter(LearnerKnowledgeState.user_id.in_(user_ids))
        .group_by(LearnerKnowledgeState.user_id)
        .all()
    )

    # Pre-fetch recommendation counts
    rec_counts = dict(
        db.query(Recommendation.user_id, func.count(Recommendation.id))
        .filter(Recommendation.user_id.in_(user_ids))
        .group_by(Recommendation.user_id)
        .all()
    )

    # Pre-fetch latest diagnostic attempts
    latest_diags = dict(
        db.query(DiagnosticAttempt.user_id, func.max(DiagnosticAttempt.created_at))
        .filter(DiagnosticAttempt.user_id.in_(user_ids))
        .group_by(DiagnosticAttempt.user_id)
        .all()
    )

    export_items: List[AdminExportStudentItem] = []
    for s in students:
        ob = onboarding_map.get(s.id)
        subs = user_subs_map.get(s.id, [])
        total_sub_count = len(subs)
        solved_sub_count = len([x for x in subs if x.status == "Accepted"])
        pass_rate = round((solved_sub_count / total_sub_count) * 100.0, 1) if total_sub_count > 0 else 0.0
        langs = sorted(list({x.language for x in subs if x.language}))
        avg_m = round(float(avg_masteries.get(s.id, 0.0)), 3)
        total_r = rec_counts.get(s.id, 0)

        # Last activity
        candidates = [s.created_at]
        if ob and ob.completed_at:
            candidates.append(ob.completed_at)
        if s.id in latest_diags and latest_diags[s.id]:
            candidates.append(latest_diags[s.id])
        if subs:
            candidates.append(max(x.created_at for x in subs))
        last_act = max(candidates).strftime("%Y-%m-%d %H:%M:%S") if candidates else None

        score_pct = (
            round((s.diagnostic_score / s.diagnostic_total) * 100.0, 1)
            if s.diagnostic_score is not None and s.diagnostic_total
            else None
        )

        export_items.append(AdminExportStudentItem(
            student_id=s.id,
            name=s.name,
            email=s.email,
            role=s.role,
            registration_date=s.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            onboarding_completed=ob is not None,
            learning_goal=ob.learning_goal if ob else None,
            experience_level=ob.experience_level if ob else None,
            diagnostic_completed=bool(s.diagnostic_completed),
            diagnostic_score=s.diagnostic_score,
            diagnostic_total=s.diagnostic_total,
            diagnostic_score_percent=score_pct,
            total_submissions=total_sub_count,
            solved_submissions=solved_sub_count,
            submission_pass_rate=pass_rate,
            languages_used=langs,
            average_mastery=avg_m,
            total_recommendations=total_r,
            last_activity=last_act
        ))

    if format.lower() == "csv":
        output = io.StringIO()
        fieldnames = [
            "student_id",
            "name",
            "email",
            "role",
            "registration_date",
            "onboarding_completed",
            "learning_goal",
            "experience_level",
            "diagnostic_completed",
            "diagnostic_score",
            "diagnostic_total",
            "diagnostic_score_percent",
            "total_submissions",
            "solved_submissions",
            "submission_pass_rate",
            "languages_used",
            "average_mastery",
            "total_recommendations",
            "last_activity"
        ]
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        for item in export_items:
            row_dict = item.model_dump()
            row_dict["languages_used"] = "; ".join(row_dict.get("languages_used", []))
            writer.writerow(row_dict)

        filename = f"adaptive_learning_live_dataset_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.csv"
        return Response(
            content=output.getvalue(),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    return AdminExportResponse(
        exported_at=datetime.now(timezone.utc),
        total_students=len(export_items),
        dataset=export_items
    )
