"""
Knowledge State API Router (Milestone 5).
Exposes endpoints for fetching and recalculating the authenticated learner's 10-topic mastery profile.
"""
import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.models.learner_knowledge_state import LearnerKnowledgeState
from app.api.deps import get_current_user, require_diagnostic_completed
from app.ml.state_engine import KnowledgeStateEngine, get_mastery_level_label
from app.schemas.knowledge_state import (
    TopicMasteryItem,
    ConceptMasteryItem,
    KnowledgeStateResponse,
    RecalculateStateResponse,
)

logger = logging.getLogger(__name__)
router = APIRouter()


def _format_knowledge_response(
    user_id: int,
    states: List[LearnerKnowledgeState],
    db: Optional[Session] = None
) -> KnowledgeStateResponse:
    """Helper to assemble a KnowledgeStateResponse from a list of LearnerKnowledgeState rows."""
    topic_items = []
    total_mastery = 0.0
    total_confidence = 0.0
    total_interactions = 0
    latest_update = None

    for s in states:
        m_score = round(float(s.mastery_score), 4)
        c_score = round(float(s.confidence_score), 4)
        total_mastery += m_score
        total_confidence += c_score
        total_interactions += s.total_interactions

        if s.updated_at:
            if latest_update is None or s.updated_at > latest_update:
                latest_update = s.updated_at

        topic_name = s.topic.name if s.topic else f"Topic {s.topic_id}"
        topic_slug = s.topic.slug if s.topic else f"topic-{s.topic_id}"
        order_idx = s.topic.order_index if s.topic else s.topic_id

        topic_items.append(
            TopicMasteryItem(
                topic_id=s.topic_id,
                topic_name=topic_name,
                topic_slug=topic_slug,
                order_index=order_idx,
                mastery_score=m_score,
                confidence_score=c_score,
                total_interactions=s.total_interactions,
                mastery_level=get_mastery_level_label(m_score),
                updated_at=s.updated_at,
            )
        )

    num_topics = max(1, len(states))
    overall_mastery = round(total_mastery / num_topics, 4)
    overall_confidence = round(total_confidence / num_topics, 4)

    concept_items = None
    if db is not None:
        try:
            c_states = KnowledgeStateEngine.get_or_initialize_user_concept_states(db, user_id)
            concept_items = [
                ConceptMasteryItem(
                    concept=cs.concept,
                    mastery_score=round(float(cs.mastery_score), 4),
                    weakness_score=round(float(cs.weakness_score), 4),
                    confidence_score=round(float(cs.confidence_score), 4),
                    weakness_level=cs.weakness_level,
                    interactions=cs.interactions,
                    solved_count=cs.solved_count,
                    updated_at=cs.updated_at,
                )
                for cs in c_states
            ]
        except Exception as e:
            logger.warning(f"Could not load concept states for response: {e}")

    return KnowledgeStateResponse(
        user_id=user_id,
        overall_mastery=overall_mastery,
        overall_confidence=overall_confidence,
        total_interactions=total_interactions,
        topics=topic_items,
        concepts=concept_items,
        last_updated=latest_update,
    )


@router.get(
    "",
    response_model=KnowledgeStateResponse,
    status_code=status.HTTP_200_OK,
    summary="Get authenticated learner's 10-topic knowledge state"
)
def get_knowledge_state(
    current_user: User = Depends(require_diagnostic_completed),
    db: Session = Depends(get_db)
):
    """
    Returns the authenticated user's current 10-topic knowledge tracing profile.
    Automatically initializes missing topic rows with baseline priors if first access.
    """
    states = KnowledgeStateEngine.get_or_initialize_user_states(db, current_user.id)
    return _format_knowledge_response(current_user.id, states, db=db)


@router.get(
    "/concepts",
    response_model=List[ConceptMasteryItem],
    status_code=status.HTTP_200_OK,
    summary="Get authenticated learner's granular concept-level mastery profile"
)
def get_concept_states(
    current_user: User = Depends(require_diagnostic_completed),
    db: Session = Depends(get_db)
):
    """
    Returns granular concept-level mastery, weakness, and confidence profile
    across all 37 Codeforces learning concepts for the authenticated learner.
    """
    c_states = KnowledgeStateEngine.get_or_initialize_user_concept_states(db, current_user.id)
    return [
        ConceptMasteryItem(
            concept=cs.concept,
            mastery_score=round(float(cs.mastery_score), 4),
            weakness_score=round(float(cs.weakness_score), 4),
            confidence_score=round(float(cs.confidence_score), 4),
            weakness_level=cs.weakness_level,
            interactions=cs.interactions,
            solved_count=cs.solved_count,
            updated_at=cs.updated_at,
        )
        for cs in c_states
    ]


@router.post(
    "/recalculate",
    response_model=RecalculateStateResponse,
    status_code=status.HTTP_200_OK,
    summary="Recalculate learner knowledge state from all historical interactions"
)
def recalculate_knowledge_state(
    current_user: User = Depends(require_diagnostic_completed),
    db: Session = Depends(get_db)
):
    """
    Replays the authenticated user's entire sequence of diagnostic attempts and problem
    submissions using Bayesian concept updates to regenerate calibrated knowledge states.
    """
    updated_states = KnowledgeStateEngine.recalculate_user_knowledge_state(db, current_user.id)
    formatted_state = _format_knowledge_response(current_user.id, updated_states, db=db)

    return RecalculateStateResponse(
        message="Knowledge state successfully recalculated across all historical interactions.",
        user_id=current_user.id,
        topics_updated=len(updated_states),
        knowledge_state=formatted_state,
    )
