"""
Pydantic Schemas for Learner Knowledge State API (Milestone 5).
"""
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class TopicMasteryItem(BaseModel):
    """Schema representing learner mastery for an individual DSA topic."""
    model_config = ConfigDict(from_attributes=True)

    topic_id: int
    topic_name: str
    topic_slug: str
    order_index: int = 0
    mastery_score: float = Field(..., ge=0.0, le=1.0, description="Mastery probability in range [0.0, 1.0]")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence estimation in range [0.0, 1.0]")
    total_interactions: int = Field(0, ge=0, description="Total problem attempts on this topic")
    mastery_level: str = Field("Novice", description="Human-readable mastery label: Novice, Developing, Proficient, Master")
    updated_at: Optional[datetime] = None


class ConceptMasteryItem(BaseModel):
    """Schema representing learner mastery for an individual Codeforces learning concept."""
    model_config = ConfigDict(from_attributes=True)

    concept: str
    mastery_score: float = Field(..., ge=0.0, le=1.0, description="Bayesian smoothed concept mastery [0.0, 1.0]")
    weakness_score: float = Field(..., ge=0.0, le=1.0, description="Concept weakness score [0.0, 1.0]")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Concept confidence estimation [0.0, 1.0]")
    weakness_level: str = Field("Moderate", description="Weakness tier: Very Low, Low, Moderate, High, Very High")
    interactions: int = Field(0, ge=0, description="Total problem interactions on this concept")
    solved_count: int = Field(0, ge=0, description="Total solved interactions on this concept")
    updated_at: Optional[datetime] = None


class KnowledgeStateResponse(BaseModel):
    """Schema representing complete 10-topic knowledge profile for a user."""
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    overall_mastery: float = Field(..., ge=0.0, le=1.0, description="Mean mastery across all 10 topics")
    overall_confidence: float = Field(..., ge=0.0, le=1.0, description="Mean confidence across all 10 topics")
    total_interactions: int = Field(0, ge=0, description="Aggregate problem interactions across all topics")
    topics: List[TopicMasteryItem]
    concepts: Optional[List[ConceptMasteryItem]] = None
    last_updated: Optional[datetime] = None


class RecalculateStateResponse(BaseModel):
    """Schema returned after triggering a knowledge state recalculation."""
    model_config = ConfigDict(from_attributes=True)

    message: str
    user_id: int
    topics_updated: int
    knowledge_state: KnowledgeStateResponse
