"""
Pydantic Schemas for Adaptive Learning Roadmap (Phase 2 Step 4).
"""
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class RoadmapConceptItem(BaseModel):
    """Details for a single learning concept within a roadmap stage."""
    model_config = ConfigDict(from_attributes=True)

    concept: str
    mastery_score: float = Field(..., ge=0.0, le=1.0, description="Bayesian mastery score")
    weakness_score: float = Field(..., ge=0.0, le=1.0, description="Concept weakness: 1 - mastery")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Empirical confidence score")
    weakness_level: str
    status: str = Field(..., description="'completed', 'in_progress', 'available', or 'locked'")
    priority: int = Field(..., description="Learning priority rank (1 = highest)")
    interactions: int = 0
    solved_count: int = 0
    is_confirmed_weakness: bool = False
    recommended_problem_ids: List[int] = []


class RoadmapStage(BaseModel):
    """Roadmap progression stage grouping related algorithmic concepts."""
    model_config = ConfigDict(from_attributes=True)

    stage_id: str
    stage_name: str
    description: str
    order_index: int = 1
    status: str = Field(..., description="'completed', 'in_progress', 'available', or 'locked'")
    priority: int = Field(..., description="Stage priority rank (1 = highest current focus)")
    prerequisites: List[str] = []
    total_concepts: int = 0
    completed_concepts: int = 0
    progress_percent: float = 0.0
    mastery: float = Field(..., ge=0.0, le=1.0, description="Average concept mastery in stage")
    weakness: float = Field(..., ge=0.0, le=1.0, description="Average concept weakness in stage")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Average concept confidence in stage")
    concepts: List[RoadmapConceptItem]
    recommended_problem_ids: List[int] = []


class RoadmapResponse(BaseModel):
    """Top-level adaptive roadmap response for learner."""
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    current_stage: str = Field(..., description="Name of the current focus stage")
    current_stage_id: str = Field(..., description="Identifier of the current focus stage")
    total_stages: int
    completed_stages: int
    overall_progress_percent: float
    stages: List[RoadmapStage]
