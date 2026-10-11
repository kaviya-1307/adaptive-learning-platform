"""
Pydantic validation schemas.
"""
from app.schemas.health import HealthResponse
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token, TokenPayload
from app.schemas.onboarding import OnboardingCreate, OnboardingResponse
from app.schemas.problem import (
    TopicResponse,
    TestCaseResponse,
    ProblemSummary,
    ProblemDetail,
    DiagnosticAttemptCreate,
    DiagnosticAttemptResponse,
    DiagnosticCompleteResponse,
    DiagnosticScoreResponse,
)

from app.schemas.submission import (
    CodeRunRequest,
    CodeSubmitRequest,
    TestCaseExecutionResult,
    CodeRunResponse,
    SubmissionResponse,
    SubmissionHistoryItem,
)

from app.schemas.knowledge_state import (
    TopicMasteryItem,
    KnowledgeStateResponse,
    RecalculateStateResponse,
)

from app.schemas.recommendation import (
    RecommendationProblemSummary,
    RecommendationResponse,
    RecommendationHistoryItem,
)

from app.schemas.dashboard import (
    UserSummary,
    OverallLearningState,
    DashboardTopicMastery,
    DifficultyStatItem,
    ProblemSolvingStats,
    ActiveRecommendationSummary,
    RecommendationHistorySummaryItem,
    RecentSubmissionSummaryItem,
    DashboardSummaryResponse,
)

from app.schemas.roadmap import (
    RoadmapConceptItem,
    RoadmapStage,
    RoadmapResponse,
)

from app.schemas.admin import (
    AdminOverviewStats,
    AdminStudentListItem,
    AdminStudentListResponse,
    AdminDiagnosticSummaryItem,
    AdminSubmissionSummaryItem,
    AdminTopicMasteryItem,
    AdminConceptWeaknessItem,
    AdminRecommendationSummaryItem,
    AdminStudentDetailResponse,
    AdminExportStudentItem,
    AdminExportResponse,
)

__all__ = [
    "HealthResponse",
    "UserCreate",
    "UserLogin",
    "UserResponse",
    "Token",
    "TokenPayload",
    "OnboardingCreate",
    "OnboardingResponse",
    "TopicResponse",
    "TestCaseResponse",
    "ProblemSummary",
    "ProblemDetail",
    "DiagnosticAttemptCreate",
    "DiagnosticAttemptResponse",
    "DiagnosticCompleteResponse",
    "DiagnosticScoreResponse",
    "CodeRunRequest",
    "CodeSubmitRequest",
    "TestCaseExecutionResult",
    "CodeRunResponse",
    "SubmissionResponse",
    "SubmissionHistoryItem",
    "TopicMasteryItem",
    "KnowledgeStateResponse",
    "RecalculateStateResponse",
    "RecommendationProblemSummary",
    "RecommendationResponse",
    "RecommendationHistoryItem",
    "UserSummary",
    "OverallLearningState",
    "DashboardTopicMastery",
    "DifficultyStatItem",
    "ProblemSolvingStats",
    "ActiveRecommendationSummary",
    "RecommendationHistorySummaryItem",
    "RecentSubmissionSummaryItem",
    "DashboardSummaryResponse",
    "RoadmapConceptItem",
    "RoadmapStage",
    "RoadmapResponse",
    "AdminOverviewStats",
    "AdminStudentListItem",
    "AdminStudentListResponse",
    "AdminDiagnosticSummaryItem",
    "AdminSubmissionSummaryItem",
    "AdminTopicMasteryItem",
    "AdminConceptWeaknessItem",
    "AdminRecommendationSummaryItem",
    "AdminStudentDetailResponse",
    "AdminExportStudentItem",
    "AdminExportResponse",
]
