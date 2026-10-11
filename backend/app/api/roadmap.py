"""
Adaptive Learning Roadmap API Router (Phase 2 Step 4).
Exposes endpoints for fetching personalized, adaptive roadmap progression.
"""
import logging
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.api.deps import get_current_user
from app.ml.roadmap_engine import AdaptiveRoadmapEngine
from app.schemas.roadmap import RoadmapResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get(
    "",
    response_model=RoadmapResponse,
    status_code=status.HTTP_200_OK,
    summary="Get personalized adaptive learning roadmap"
)
def get_roadmap(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns the authenticated learner's personalized adaptive roadmap.
    Stages and concepts are dynamically evaluated from the learner's current concept state,
    prerequisite progression, and weakness targeting.
    """
    return AdaptiveRoadmapEngine.generate_roadmap(db, current_user.id)
