"""
Pydantic Schemas for Personalized Learner Dashboard & Progress Analytics (Milestone 7).
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class UserSummary(BaseModel):
    """Authenticated user summary information for dashboard."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    learning_goal: Optional[str] = None
    experience_level: Optional[str] = None
    diagnostic_completed: bool = False
    diagnostic_score: Optional[int] = None
    diagnostic_total: Optional[int] = None


class OverallLearningState(BaseModel):
    """Aggregated mastery and confidence overview."""
    model_config = ConfigDict(from_attributes=True)

    overall_mastery: float = Field(..., ge=0.0, le=1.0, description="Average mastery score across 10 DSA topics")
    overall_confidence: float = Field(..., ge=0.0, le=1.0, description="Average confidence score across 10 DSA topics")
    total_interactions: int = Field(..., ge=0, description="Total problem submissions and diagnostic interactions")
    last_updated: Optional[datetime] = None


class DashboardTopicMastery(BaseModel):
    """Detailed topic mastery metrics for dashboard visualization."""
    model_config = ConfigDict(from_attributes=True)

    topic_id: int
    topic_name: str
    topic_slug: str
    mastery_score: float = Field(..., ge=0.0, le=1.0)
    mastery_percentage: float = Field(..., ge=0.0, le=100.0)
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    total_interactions: int
    mastery_level: str  # 'Novice', 'Developing', 'Proficient', 'Master'
    order_index: int = 0


class DifficultyStatItem(BaseModel):
    """Solved metrics for a single difficulty tier."""
    model_config = ConfigDict(from_attributes=True)

    difficulty: str
    solved_count: int
    total_count: int
    percentage: float


class ProblemSolvingStats(BaseModel):
    """Aggregated submission performance and difficulty distribution."""
    model_config = ConfigDict(from_attributes=True)

    total_submissions: int
    total_solved: int
    accepted_submissions: int
    wrong_submissions: int
    acceptance_rate: float = Field(..., ge=0.0, le=100.0)
    easy_solved: int
    medium_solved: int
    hard_solved: int
    difficulty_breakdown: List[DifficultyStatItem]


class ActiveRecommendationSummary(BaseModel):
    """Active personalized next-problem recommendation."""
    model_config = ConfigDict(from_attributes=True)

    recommendation_id: int
    problem_id: int
    problem_title: str
    problem_slug: str
    topic_name: str
    difficulty: str
    predicted_success_prob: float = Field(..., ge=0.0, le=1.0)
    explanation_text: str


class RecommendationHistorySummaryItem(BaseModel):
    """Summary item in recommendation dispatch history."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    problem_id: int
    problem_title: str
    problem_slug: str
    topic_name: str
    difficulty: str
    predicted_success_prob: float
    explanation_text: str
    is_active: bool
    created_at: datetime


class RecentSubmissionSummaryItem(BaseModel):
    """Recent code submission item for learner dashboard."""
    model_config = ConfigDict(from_attributes=True)

    submission_id: int
    problem_id: int
    problem_title: str
    problem_slug: str
    topic_name: str
    difficulty: str
    status: str
    passed_test_cases: int
    total_test_cases: int
    execution_time_ms: float
    created_at: datetime


class DashboardSummaryResponse(BaseModel):
    """Root response model for GET /api/dashboard/summary."""
    model_config = ConfigDict(from_attributes=True)

    user: UserSummary
    learning_state: OverallLearningState
    topic_mastery: List[DashboardTopicMastery]
    problem_stats: ProblemSolvingStats
    active_recommendation: Optional[ActiveRecommendationSummary] = None
    recommendation_history: List[RecommendationHistorySummaryItem]
    recent_submissions: List[RecentSubmissionSummaryItem]
