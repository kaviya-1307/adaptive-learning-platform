"""
Admin-Only Performance Monitoring and Live Dataset Export Schemas (Phase 5).
Guarantees:
- Password, password_hash, tokens, and secrets are NEVER exposed.
- Raw student solution code is excluded from summary and monitoring endpoints.
- Strictly formatted for administrative and research evaluation.
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict, Field


class AdminOverviewStats(BaseModel):
    """Aggregated platform-level activity and participation metrics."""
    total_registered_students: int
    onboarding_completed_count: int
    diagnostic_completed_count: int
    total_submissions_count: int
    total_solved_submissions_count: int
    active_students_count: int
    total_recommendations_count: int
    submissions_by_language: Dict[str, int] = {}


class AdminStudentListItem(BaseModel):
    """Sanitized student profile item for the admin monitoring table."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    role: str
    created_at: datetime
    onboarding_completed: bool
    learning_goal: Optional[str] = None
    experience_level: Optional[str] = None
    diagnostic_completed: bool
    diagnostic_score: Optional[int] = None
    diagnostic_total: Optional[int] = None
    diagnostic_completed_at: Optional[datetime] = None
    total_submissions: int = 0
    solved_problems_count: int = 0
    last_activity_at: Optional[datetime] = None


class AdminStudentListResponse(BaseModel):
    """Paginated list response of monitored students."""
    total_count: int
    students: List[AdminStudentListItem]


class AdminDiagnosticSummaryItem(BaseModel):
    """Sanitized per-problem diagnostic test record."""
    problem_id: int
    problem_title: str
    is_solved: bool
    attempts_count: int
    time_spent_seconds: int
    created_at: datetime


class AdminSubmissionSummaryItem(BaseModel):
    """Sanitized submission log item."""
    submission_id: int
    problem_id: int
    problem_title: str
    language: str
    status: str
    passed_test_cases: int
    total_test_cases: int
    execution_time_ms: float
    created_at: datetime


class AdminTopicMasteryItem(BaseModel):
    """Topic mastery score for the learner."""
    topic_id: int
    topic_name: str
    mastery_score: float
    confidence_score: float
    total_interactions: int


class AdminConceptWeaknessItem(BaseModel):
    """Granular concept mastery metrics."""
    concept: str
    mastery_score: float
    weakness_score: float
    weakness_level: str
    interactions: int
    solved_count: int


class AdminRecommendationSummaryItem(BaseModel):
    """Personalized recommendation history record."""
    recommendation_id: int
    problem_id: int
    problem_title: str
    difficulty: str
    topic_name: str
    recommendation_reason: Optional[str] = None
    created_at: datetime


class AdminStudentDetailResponse(BaseModel):
    """Comprehensive single-student inspection record for admin evaluation."""
    id: int
    name: str
    email: str
    role: str
    created_at: datetime
    onboarding_completed: bool
    learning_goal: Optional[str] = None
    experience_level: Optional[str] = None
    diagnostic_completed: bool
    diagnostic_score: Optional[int] = None
    diagnostic_total: Optional[int] = None
    diagnostic_completed_at: Optional[datetime] = None
    diagnostic_attempts: List[AdminDiagnosticSummaryItem] = []
    total_submissions: int = 0
    solved_problems_count: int = 0
    submissions_by_status: Dict[str, int] = {}
    submissions_by_language: Dict[str, int] = {}
    recent_submissions: List[AdminSubmissionSummaryItem] = []
    topic_mastery: List[AdminTopicMasteryItem] = []
    top_weak_concepts: List[AdminConceptWeaknessItem] = []
    recent_recommendations: List[AdminRecommendationSummaryItem] = []
    last_activity_at: Optional[datetime] = None


class AdminExportStudentItem(BaseModel):
    """Sanitized evaluation item for research dataset export."""
    student_id: int
    name: str
    email: str
    role: str
    registration_date: str
    onboarding_completed: bool
    learning_goal: Optional[str] = None
    experience_level: Optional[str] = None
    diagnostic_completed: bool
    diagnostic_score: Optional[int] = None
    diagnostic_total: Optional[int] = None
    diagnostic_score_percent: Optional[float] = None
    total_submissions: int
    solved_submissions: int
    submission_pass_rate: float
    languages_used: List[str] = []
    average_mastery: float
    total_recommendations: int
    last_activity: Optional[str] = None


class AdminExportResponse(BaseModel):
    """Research export container for the live student dataset."""
    exported_at: datetime
    total_students: int
    dataset: List[AdminExportStudentItem]
