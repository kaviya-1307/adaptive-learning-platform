"""
Pydantic Schemas for Adaptive Recommendation Engine (Milestone 6).
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class RecommendationProblemSummary(BaseModel):
    """Brief problem summary embedded inside recommendation response."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    slug: str
    difficulty: str
    topic_name: str
    topic_slug: str
    order_index: int = 0
    description_markdown: Optional[str] = None
    concepts: Optional[List[str]] = None
    rating: Optional[int] = None


class RecommendationResponse(BaseModel):
    """Schema returned for active and freshly generated problem recommendations."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    problem_id: int
    predicted_success_prob: float = Field(..., ge=0.0, le=1.0, description="Estimated success probability in [0.0, 1.0]")
    explanation_text: str = Field(..., description="Explainable AI rationale detailing concept weakness, difficulty, and recommendation reason")
    is_active: bool
    created_at: datetime
    problem: RecommendationProblemSummary

    # Phase 2 Step 3 Concept-Level Recommendation Metadata
    recommendation_score: Optional[float] = Field(None, description="Composite score: 0.60 * concept_gap + 0.40 * difficulty_fit")
    concept_gap: Optional[float] = Field(None, description="Mean learner weakness across problem concepts")
    difficulty_fit: Optional[float] = Field(None, description="Exponential difficulty fit: exp(-|rating - target| / 300)")
    primary_weak_concept: Optional[str] = Field(None, description="Primary targeted weak learning concept")
    weak_concepts: Optional[List[str]] = Field(None, description="All relevant weak learning concepts for this problem")
    difficulty_reason: Optional[str] = Field(None, description="Pedagogical rationale for difficulty match")
    recommendation_reason: Optional[str] = Field(None, description="Concise pedagogical reason for this recommendation")


class RecommendationHistoryItem(BaseModel):
    """Schema representing an individual past recommendation in user history."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    problem_id: int
    problem_title: str
    problem_slug: str
    topic_name: str
    difficulty: str
    predicted_success_prob: float
    explanation_text: str
    is_active: bool
    created_at: datetime

    # Phase 2 Step 3 Concept-Level Recommendation Metadata
    recommendation_score: Optional[float] = None
    concept_gap: Optional[float] = None
    difficulty_fit: Optional[float] = None
    primary_weak_concept: Optional[str] = None
    concepts: Optional[List[str]] = None
    rating: Optional[int] = None
