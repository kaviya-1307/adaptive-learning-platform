"""
Pydantic schemas for code execution, submission evaluation, and submission history.
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class CodeRunRequest(BaseModel):
    problem_id: int
    code: str
    language: str = "python"


class CodeSubmitRequest(BaseModel):
    problem_id: int
    code: str
    language: str = "python"


class TestCaseExecutionResult(BaseModel):
    test_case_id: int
    status: str  # 'Passed', 'Wrong Answer', 'Runtime Error', 'Time Limit Exceeded'
    input_data: Optional[str] = None
    expected_output: Optional[str] = None
    actual_output: Optional[str] = None
    stdout: Optional[str] = None
    execution_time_ms: float = 0.0
    is_hidden: bool = False
    error_message: Optional[str] = None


class CodeRunResponse(BaseModel):
    status: str  # 'Accepted', 'Wrong Answer', 'Runtime Error', 'Time Limit Exceeded', 'Compilation Error'
    passed_test_cases: int
    total_test_cases: int
    execution_time_ms: float
    results: List[TestCaseExecutionResult] = []
    compile_error: Optional[str] = None


class SubmissionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    problem_id: int
    language: str = "python"
    status: str  # 'Accepted', 'Wrong Answer', 'Runtime Error', 'Time Limit Exceeded', 'Compilation Error'
    passed_test_cases: int
    total_test_cases: int
    execution_time_ms: float
    created_at: datetime
    results: List[TestCaseExecutionResult] = []
    compile_error: Optional[str] = None


class SubmissionHistoryItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    problem_id: int
    language: str = "python"
    status: str
    passed_test_cases: int
    total_test_cases: int
    execution_time_ms: float
    created_at: datetime
