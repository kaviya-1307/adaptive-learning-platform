"""
Adaptive Recommendation API Router (Phase 2 Step 3 & Milestone 6).
Exposes endpoints for fetching active recommendations, triggering fresh recommendations,
diversity-aware Top-K recommendations, and viewing recommendation history.
"""
import logging
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.models.recommendation import Recommendation
from app.api.deps import get_current_user, require_diagnostic_completed
from app.services.recommendation_engine import RecommendationEngine
from app.ml.state_engine import get_problem_learning_concepts
from app.schemas.recommendation import (
    RecommendationResponse,
    RecommendationProblemSummary,
    RecommendationHistoryItem,
)

logger = logging.getLogger(__name__)
router = APIRouter()


def _format_recommendation_response(rec: Recommendation) -> RecommendationResponse:
    """Helper to convert Recommendation ORM model to RecommendationResponse schema."""
    prob = rec.problem
    topic_name = prob.topic.name if (prob and prob.topic) else "General DSA"
    topic_slug = prob.topic.slug if (prob and prob.topic) else "general"

    # Resolve learning concepts and problem rating
    concepts = get_problem_learning_concepts(prob) if prob else []
    rating = RecommendationEngine.get_problem_rating(prob) if prob else 1000

    prob_summary = RecommendationProblemSummary(
        id=prob.id if prob else rec.problem_id,
        title=prob.title if prob else f"Problem #{rec.problem_id}",
        slug=prob.slug if prob else f"problem-{rec.problem_id}",
        difficulty=prob.difficulty if prob else "Medium",
        topic_name=topic_name,
        topic_slug=topic_slug,
        order_index=prob.order_index if prob else 0,
        description_markdown=prob.description_markdown if prob else None,
        concepts=concepts,
        rating=rating,
    )

    rec_score = getattr(rec, "recommendation_score", None)
    gap = getattr(rec, "concept_gap", None)
    fit = getattr(rec, "difficulty_fit", None)
    primary_concept = getattr(rec, "primary_weak_concept", None)

    return RecommendationResponse(
        id=rec.id,
        user_id=rec.user_id,
        problem_id=rec.problem_id,
        predicted_success_prob=round(float(rec.predicted_success_prob), 4),
        explanation_text=rec.explanation_text,
        is_active=rec.is_active,
        created_at=rec.created_at,
        problem=prob_summary,
        recommendation_score=round(float(rec_score), 4) if rec_score is not None else None,
        concept_gap=round(float(gap), 4) if gap is not None else None,
        difficulty_fit=round(float(fit), 4) if fit is not None else None,
        primary_weak_concept=primary_concept,
        weak_concepts=[primary_concept] if primary_concept else concepts,
        difficulty_reason=f"Problem difficulty ({rating}) targeted for optimal challenge learning",
        recommendation_reason=f"Selected to target knowledge gap in {primary_concept or 'targeted DSA concepts'}",
    )


def _format_candidate_response(cand: dict, user_id: int, rec_id: int = 0) -> RecommendationResponse:
    """Formats a candidate dictionary from recommend_top_k into RecommendationResponse."""
    prob = cand["problem"]
    topic_name = cand.get("topic_name", "General DSA")
    topic_slug = cand.get("topic_slug", "general")
    concepts = cand.get("concepts", [])
    rating = cand.get("problem_rating", 1000)

    prob_summary = RecommendationProblemSummary(
        id=prob.id,
        title=prob.title,
        slug=prob.slug,
        difficulty=prob.difficulty,
        topic_name=topic_name,
        topic_slug=topic_slug,
        order_index=prob.order_index,
        description_markdown=prob.description_markdown,
        concepts=concepts,
        rating=rating,
    )

    primary_concept = cand.get("primary_concept")

    return RecommendationResponse(
        id=rec_id,
        user_id=user_id,
        problem_id=prob.id,
        predicted_success_prob=round(float(cand.get("predicted_success_prob", 0.70)), 4),
        explanation_text=cand.get("explanation_text", ""),
        is_active=False,
        created_at=datetime.now(timezone.utc),
        problem=prob_summary,
        recommendation_score=round(float(cand.get("recommendation_score", 0.0)), 4),
        concept_gap=round(float(cand.get("concept_gap", 0.0)), 4),
        difficulty_fit=round(float(cand.get("difficulty_fit", 0.0)), 4),
        primary_weak_concept=primary_concept,
        weak_concepts=[primary_concept] if primary_concept else concepts,
        difficulty_reason=f"Problem difficulty ({rating}) targeted for optimal challenge learning",
        recommendation_reason=f"Selected to target knowledge gap in {primary_concept or 'targeted DSA concepts'}",
    )


@router.get(
    "/next",
    response_model=RecommendationResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current active problem recommendation for learner"
)
def get_next_recommendation(
    current_user: User = Depends(require_diagnostic_completed),
    db: Session = Depends(get_db)
):
    """
    Returns the learner's current active recommendation.
    If no active recommendation exists, automatically generates one based on latest concept states.
    """
    rec = RecommendationEngine.get_active_recommendation(db, current_user.id)
    return _format_recommendation_response(rec)


@router.post(
    "/generate",
    response_model=RecommendationResponse,
    status_code=status.HTTP_200_OK,
    summary="Force generate a fresh recommendation based on latest knowledge state"
)
def generate_recommendation(
    current_user: User = Depends(require_diagnostic_completed),
    db: Session = Depends(get_db)
):
    """
    Calculates and persists a fresh next-problem recommendation.
    Deactivates the previous active recommendation and saves the new one with is_active=True.
    """
    rec = RecommendationEngine.generate_recommendation(db, current_user.id, force_new=True)
    return _format_recommendation_response(rec)


@router.get(
    "/top",
    response_model=List[RecommendationResponse],
    status_code=status.HTTP_200_OK,
    summary="Get diversity-aware Top-K problem recommendations"
)
def get_top_recommendations(
    limit: int = Query(10, ge=1, le=40, description="Number of recommendations to return (Top-K)"),
    current_user: User = Depends(require_diagnostic_completed),
    db: Session = Depends(get_db)
):
    """
    Returns personalized, diversity-aware Top-K problem recommendations
    ranked by (0.60 * concept_gap + 0.40 * difficulty_fit) with MAX_SAME_PRIMARY_CONCEPT = 2.
    """
    top_candidates = RecommendationEngine.recommend_top_k(
        db,
        current_user.id,
        top_k=limit,
        exclude_all_attempted=True
    )
    return [
        _format_candidate_response(cand, current_user.id, rec_id=idx + 1)
        for idx, cand in enumerate(top_candidates)
    ]


@router.get(
    "/history",
    response_model=List[RecommendationHistoryItem],
    status_code=status.HTTP_200_OK,
    summary="Get learner's recommendation dispatch history"
)
def get_recommendation_history(
    current_user: User = Depends(require_diagnostic_completed),
    db: Session = Depends(get_db)
):
    """
    Returns historical recommendations specifically for the authenticated user.
    """
    history_recs = RecommendationEngine.get_recommendation_history(db, current_user.id)

    results = []
    for r in history_recs:
        prob = r.problem
        concepts = get_problem_learning_concepts(prob) if prob else []
        rating = RecommendationEngine.get_problem_rating(prob) if prob else 1000
        rec_score = getattr(r, "recommendation_score", None)
        gap = getattr(r, "concept_gap", None)
        fit = getattr(r, "difficulty_fit", None)
        primary_concept = getattr(r, "primary_weak_concept", None)

        results.append(
            RecommendationHistoryItem(
                id=r.id,
                user_id=r.user_id,
                problem_id=r.problem_id,
                problem_title=prob.title if prob else f"Problem #{r.problem_id}",
                problem_slug=prob.slug if prob else f"problem-{r.problem_id}",
                topic_name=prob.topic.name if (prob and prob.topic) else "General DSA",
                difficulty=prob.difficulty if prob else "Medium",
                predicted_success_prob=round(float(r.predicted_success_prob), 4),
                explanation_text=r.explanation_text,
                is_active=r.is_active,
                created_at=r.created_at,
                recommendation_score=round(float(rec_score), 4) if rec_score is not None else None,
                concept_gap=round(float(gap), 4) if gap is not None else None,
                difficulty_fit=round(float(fit), 4) if fit is not None else None,
                primary_weak_concept=primary_concept,
                concepts=concepts,
                rating=rating,
            )
        )
    return results
