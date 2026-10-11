"""
Personalized Learner Dashboard & Progress Analytics Router (Milestone 7).
Provides an aggregated summary endpoint combining Knowledge State, Submissions,
Recommendations, and Difficulty Metrics.
"""
import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.core.database import get_db
from app.models.user import User
from app.models.topic import Topic
from app.models.problem import Problem
from app.models.submission import Submission
from app.models.recommendation import Recommendation
from app.models.learner_knowledge_state import LearnerKnowledgeState
from app.api.deps import get_current_user, require_diagnostic_completed
from app.ml.state_engine import KnowledgeStateEngine, get_mastery_level_label
from app.schemas.dashboard import (
    DashboardSummaryResponse,
    UserSummary,
    OverallLearningState,
    DashboardTopicMastery,
    DifficultyStatItem,
    ProblemSolvingStats,
    ActiveRecommendationSummary,
    RecommendationHistorySummaryItem,
    RecentSubmissionSummaryItem,
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get(
    "/summary",
    response_model=DashboardSummaryResponse,
    status_code=status.HTTP_200_OK,
    summary="Get aggregated learner dashboard summary and progress metrics"
)
def get_dashboard_summary(
    current_user: User = Depends(require_diagnostic_completed),
    db: Session = Depends(get_db)
):
    """
    Returns an aggregated analytics summary for the authenticated learner:
    1. User Profile & Onboarding Goals
    2. Overall Knowledge State & 10-Topic Mastery Breakdown
    3. Problem Solving Statistics & Difficulty Distribution
    4. Active Next Problem Recommendation & History (M6)
    5. Recent Submission History (M4)
    """
    user_id = current_user.id

    # 1. User Summary
    onboarding = current_user.onboarding_profile
    user_info = UserSummary(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        learning_goal=onboarding.learning_goal if onboarding else None,
        experience_level=onboarding.experience_level if onboarding else None,
        diagnostic_completed=bool(current_user.diagnostic_completed),
        diagnostic_score=current_user.diagnostic_score,
        diagnostic_total=current_user.diagnostic_total,
    )

    # 2. Knowledge State Metrics (M5)
    states = KnowledgeStateEngine.get_or_initialize_user_states(db, user_id)
    topic_rows = db.query(Topic).order_by(Topic.order_index.asc()).all()
    topic_map = {t.id: t for t in topic_rows}

    topic_masteries: List[DashboardTopicMastery] = []
    total_mastery = 0.0
    total_confidence = 0.0
    total_interactions = 0
    latest_update = None

    for s in states:
        t = topic_map.get(s.topic_id)
        t_name = t.name if t else f"Topic {s.topic_id}"
        t_slug = t.slug if t else f"topic-{s.topic_id}"
        t_order = t.order_index if t else s.topic_id

        mastery_pct = round(s.mastery_score * 100.0, 1)
        level_label = get_mastery_level_label(s.mastery_score)

        topic_masteries.append(
            DashboardTopicMastery(
                topic_id=s.topic_id,
                topic_name=t_name,
                topic_slug=t_slug,
                mastery_score=round(s.mastery_score, 4),
                mastery_percentage=mastery_pct,
                confidence_score=round(s.confidence_score, 4),
                total_interactions=s.total_interactions,
                mastery_level=level_label,
                order_index=t_order,
            )
        )
        total_mastery += s.mastery_score
        total_confidence += s.confidence_score
        total_interactions += s.total_interactions

        if s.updated_at:
            if latest_update is None or s.updated_at > latest_update:
                latest_update = s.updated_at

    # Sort topics by order_index
    topic_masteries.sort(key=lambda x: x.order_index)

    num_topics = len(states) if states else 1
    overall_mastery = round(total_mastery / num_topics, 4)
    overall_confidence = round(total_confidence / num_topics, 4)

    learning_state = OverallLearningState(
        overall_mastery=overall_mastery,
        overall_confidence=overall_confidence,
        total_interactions=total_interactions,
        last_updated=latest_update,
    )

    # 3. Problem Solving Performance & Difficulty Breakdown (M4)
    user_submissions = (
        db.query(Submission)
        .filter(Submission.user_id == user_id)
        .all()
    )

    total_submissions = len(user_submissions)
    accepted_submissions = sum(1 for sub in user_submissions if sub.status == "Accepted")
    wrong_submissions = total_submissions - accepted_submissions
    acceptance_rate = round((accepted_submissions / total_submissions * 100.0), 1) if total_submissions > 0 else 0.0

    # Count distinct solved problem IDs
    solved_problem_ids = {sub.problem_id for sub in user_submissions if sub.status == "Accepted"}
    total_solved = len(solved_problem_ids)

    # Count solved by difficulty
    solved_problems = (
        db.query(Problem)
        .filter(Problem.id.in_(solved_problem_ids))
        .all()
        if solved_problem_ids else []
    )

    easy_solved = sum(1 for p in solved_problems if p.difficulty.lower() == "easy")
    medium_solved = sum(1 for p in solved_problems if p.difficulty.lower() == "medium")
    hard_solved = sum(1 for p in solved_problems if p.difficulty.lower() == "hard")

    # Total catalog problem counts for accurate progress percentages
    all_catalog_problems = db.query(Problem).all()
    easy_total = sum(1 for p in all_catalog_problems if p.difficulty.lower() == "easy") or 1
    medium_total = sum(1 for p in all_catalog_problems if p.difficulty.lower() == "medium") or 1
    hard_total = sum(1 for p in all_catalog_problems if p.difficulty.lower() == "hard") or 1

    difficulty_breakdown = [
        DifficultyStatItem(
            difficulty="Easy",
            solved_count=easy_solved,
            total_count=easy_total,
            percentage=round(easy_solved / easy_total * 100.0, 1),
        ),
        DifficultyStatItem(
            difficulty="Medium",
            solved_count=medium_solved,
            total_count=medium_total,
            percentage=round(medium_solved / medium_total * 100.0, 1),
        ),
        DifficultyStatItem(
            difficulty="Hard",
            solved_count=hard_solved,
            total_count=hard_total,
            percentage=round(hard_solved / hard_total * 100.0, 1),
        ),
    ]

    problem_stats = ProblemSolvingStats(
        total_submissions=total_submissions,
        total_solved=total_solved,
        accepted_submissions=accepted_submissions,
        wrong_submissions=wrong_submissions,
        acceptance_rate=acceptance_rate,
        easy_solved=easy_solved,
        medium_solved=medium_solved,
        hard_solved=hard_solved,
        difficulty_breakdown=difficulty_breakdown,
    )

    # 4. Active Recommendation (M6)
    active_rec_row = (
        db.query(Recommendation)
        .options(joinedload(Recommendation.problem).joinedload(Problem.topic))
        .filter(
            Recommendation.user_id == user_id,
            Recommendation.is_active == True
        )
        .first()
    )

    active_recommendation: Optional[ActiveRecommendationSummary] = None
    if active_rec_row and active_rec_row.problem:
        prob = active_rec_row.problem
        active_recommendation = ActiveRecommendationSummary(
            recommendation_id=active_rec_row.id,
            problem_id=prob.id,
            problem_title=prob.title,
            problem_slug=prob.slug,
            topic_name=prob.topic.name if prob.topic else "General DSA",
            difficulty=prob.difficulty,
            predicted_success_prob=round(float(active_rec_row.predicted_success_prob), 4),
            explanation_text=active_rec_row.explanation_text,
        )

    # 5. Recommendation History (Latest 5)
    rec_history_rows = (
        db.query(Recommendation)
        .options(joinedload(Recommendation.problem).joinedload(Problem.topic))
        .filter(Recommendation.user_id == user_id)
        .order_by(Recommendation.created_at.desc(), Recommendation.id.desc())
        .limit(5)
        .all()
    )

    recommendation_history: List[RecommendationHistorySummaryItem] = []
    for r in rec_history_rows:
        prob = r.problem
        recommendation_history.append(
            RecommendationHistorySummaryItem(
                id=r.id,
                problem_id=r.problem_id,
                problem_title=prob.title if prob else f"Problem #{r.problem_id}",
                problem_slug=prob.slug if prob else f"problem-{r.problem_id}",
                topic_name=prob.topic.name if (prob and prob.topic) else "General DSA",
                difficulty=prob.difficulty if prob else "Medium",
                predicted_success_prob=round(float(r.predicted_success_prob), 4),
                explanation_text=r.explanation_text,
                is_active=r.is_active,
                created_at=r.created_at,
            )
        )

    # 6. Recent Submissions (Latest 5)
    recent_sub_rows = (
        db.query(Submission)
        .options(joinedload(Submission.problem).joinedload(Problem.topic))
        .filter(Submission.user_id == user_id)
        .order_by(Submission.created_at.desc(), Submission.id.desc())
        .limit(5)
        .all()
    )

    recent_submissions: List[RecentSubmissionSummaryItem] = []
    for s in recent_sub_rows:
        prob = s.problem
        recent_submissions.append(
            RecentSubmissionSummaryItem(
                submission_id=s.id,
                problem_id=s.problem_id,
                problem_title=prob.title if prob else f"Problem #{s.problem_id}",
                problem_slug=prob.slug if prob else f"problem-{s.problem_id}",
                topic_name=prob.topic.name if (prob and prob.topic) else "General DSA",
                difficulty=prob.difficulty if prob else "Medium",
                status=s.status,
                passed_test_cases=s.passed_test_cases,
                total_test_cases=s.total_test_cases,
                execution_time_ms=round(float(s.execution_time_ms or 0.0), 2),
                created_at=s.created_at,
            )
        )

    return DashboardSummaryResponse(
        user=user_info,
        learning_state=learning_state,
        topic_mastery=topic_masteries,
        problem_stats=problem_stats,
        active_recommendation=active_recommendation,
        recommendation_history=recommendation_history,
        recent_submissions=recent_submissions,
    )
