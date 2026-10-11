import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.core.database import get_db
from app.models.user import User
from app.models.onboarding import OnboardingProfile
from app.models.topic import Topic
from app.models.learner_knowledge_state import LearnerKnowledgeState
from app.schemas.onboarding import OnboardingCreate, OnboardingResponse
from app.api.deps import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter()

# Prior knowledge calibration map based on self-reported experience level
EXPERIENCE_PRIOR_MAP = {
    "beginner": {"mastery": 0.25, "confidence": 0.30},
    "intermediate": {"mastery": 0.50, "confidence": 0.40},
    "advanced": {"mastery": 0.75, "confidence": 0.50},
}


@router.post(
    "",
    response_model=OnboardingResponse,
    status_code=status.HTTP_200_OK,
    summary="Submit user onboarding preferences"
)
def submit_onboarding(
    payload: OnboardingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Save user learning goals and experience level.
    Calibrates baseline prior knowledge state across all curriculum topics.
    """
    level_key = payload.experience_level.strip().lower()
    goal_key = payload.learning_goal.strip().lower()

    if level_key not in EXPERIENCE_PRIOR_MAP:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid experience_level '{payload.experience_level}'. Must be one of: {list(EXPERIENCE_PRIOR_MAP.keys())}"
        )

    prior = EXPERIENCE_PRIOR_MAP[level_key]

    # Check if onboarding profile already exists (update or create)
    profile = db.query(OnboardingProfile).filter(
        OnboardingProfile.user_id == current_user.id
    ).first()

    if profile:
        profile.learning_goal = goal_key
        profile.experience_level = level_key
        profile.completed_at = func.now()
    else:
        profile = OnboardingProfile(
            user_id=current_user.id,
            learning_goal=goal_key,
            experience_level=level_key
        )
        db.add(profile)

    db.flush()

    # Initialize/update prior knowledge state across all topics if topics exist in DB
    topics = db.query(Topic).all()
    for topic in topics:
        k_state = db.query(LearnerKnowledgeState).filter(
            LearnerKnowledgeState.user_id == current_user.id,
            LearnerKnowledgeState.topic_id == topic.id
        ).first()

        if k_state:
            # If user has zero interactions, update prior mastery
            if k_state.total_interactions == 0:
                k_state.mastery_score = prior["mastery"]
                k_state.confidence_score = prior["confidence"]
        else:
            k_state = LearnerKnowledgeState(
                user_id=current_user.id,
                topic_id=topic.id,
                mastery_score=prior["mastery"],
                confidence_score=prior["confidence"],
                total_interactions=0
            )
            db.add(k_state)

    db.commit()
    db.refresh(profile)

    return OnboardingResponse(
        id=profile.id,
        user_id=profile.user_id,
        learning_goal=profile.learning_goal,
        experience_level=profile.experience_level,
        completed_at=profile.completed_at,
        initial_mastery_applied=prior["mastery"]
    )


@router.get(
    "/me",
    response_model=OnboardingResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current user onboarding profile"
)
def get_user_onboarding(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve the current user's onboarding preferences.
    """
    profile = db.query(OnboardingProfile).filter(
        OnboardingProfile.user_id == current_user.id
    ).first()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Onboarding has not been completed yet."
        )

    prior = EXPERIENCE_PRIOR_MAP.get(profile.experience_level, {"mastery": 0.5})

    return OnboardingResponse(
        id=profile.id,
        user_id=profile.user_id,
        learning_goal=profile.learning_goal,
        experience_level=profile.experience_level,
        completed_at=profile.completed_at,
        initial_mastery_applied=prior["mastery"]
    )
