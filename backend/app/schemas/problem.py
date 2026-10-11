from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class TopicResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    slug: str
    order_index: int


class TestCaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    input_data: str
    expected_output: str
    is_hidden: bool
    order_index: int


class ProblemSummary(BaseModel):
    """Problem listing and diagnostic summary schema."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    slug: str
    difficulty: str
    is_diagnostic: bool
    order_index: int
    supported_languages: List[str] = ["python"]
    starter_code_python: Optional[str] = None
    starter_code_java: Optional[str] = None
    starter_code_cpp: Optional[str] = None
    starter_code_javascript: Optional[str] = None
    description_markdown: Optional[str] = None
    constraints_markdown: Optional[str] = None
    topic: TopicResponse


class ProblemDetail(BaseModel):
    """Full problem schema including description, starter code, and visible test cases."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    slug: str
    difficulty: str
    is_diagnostic: bool
    order_index: int
    description_markdown: str
    constraints_markdown: Optional[str] = None
    starter_code_python: str
    starter_code_java: Optional[str] = None
    starter_code_cpp: Optional[str] = None
    starter_code_javascript: Optional[str] = None
    supported_languages: List[str] = ["python"]
    topic: TopicResponse
    visible_test_cases: List[TestCaseResponse] = []


class DiagnosticAttemptCreate(BaseModel):
    problem_id: int
    is_solved: Optional[bool] = False
    time_spent_seconds: int = 0
    code_submitted: Optional[str] = None
    language: Optional[str] = "python"


class DiagnosticAttemptResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    problem_id: int
    is_solved: bool
    attempts_count: int
    time_spent_seconds: int
    code_submitted: Optional[str] = None
    language: Optional[str] = "python"
    created_at: datetime
    passed_test_cases: Optional[int] = None
    total_test_cases: Optional[int] = None
    status: Optional[str] = None
    compile_error: Optional[str] = None
    runtime_error: Optional[str] = None


class DiagnosticCompleteResponse(BaseModel):
    message: str
    total_problems: int
    solved_count: int
    score_percent: float
    knowledge_states_initialized: int


class DiagnosticScoreResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    diagnostic_completed: bool
    diagnostic_score: int
    diagnostic_total: int
    score: Optional[int] = None
    total: Optional[int] = None
    score_percent: float
    status: Optional[str] = "completed"
    completed_at: Optional[datetime] = None
    diagnostic_completed_at: Optional[datetime] = None
    knowledge_states_initialized: int = 10
    attempts: List[DiagnosticAttemptResponse] = []
