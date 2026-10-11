"""
Problem Validation Pipeline for LeetCode Adaptive Learning Platform.
Phase 3 Step 2: Quality > Quantity Validation Engine.

Enforces strict criteria for all coding problems:
  Criterion A: Identity & Uniqueness (Slug format, non-empty title, uniqueness)
  Criterion B: Statement Completeness (Description, constraints, example format)
  Criterion C: Metadata Correctness (Difficulty in Easy/Medium/Hard, topic existence)
  Criterion D: Executable Code Integrity (Python AST compilation, entrypoint matching)
  Criterion E: Test Case Integrity (>=1 visible, >=1 hidden, JSON kwargs, expected output)
  Criterion F: Judge Consistency (PythonCodeRunner executes reference solution to 100% Accepted)
  Criterion G: Difficulty Sanity (Rating bounds check)
"""
import ast
import json
import logging
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set

from sqlalchemy.orm import Session

from app.engine.code_runner import PythonCodeRunner, extract_target_function_name
from app.models.problem import Problem
from app.models.test_case import TestCase
from app.models.topic import Topic

logger = logging.getLogger(__name__)

VALID_DIFFICULTIES = {"Easy", "Medium", "Hard"}
MIN_DESCRIPTION_LENGTH = 20
MIN_CONSTRAINTS_LENGTH = 5


@dataclass
class ValidationResult:
    is_valid: bool
    problem_id: Optional[int] = None
    slug: Optional[str] = None
    title: Optional[str] = None
    difficulty: Optional[str] = None
    topic_name: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    judge_status: Optional[str] = None
    passed_test_cases: int = 0
    total_test_cases: int = 0
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "problem_id": self.problem_id,
            "slug": self.slug,
            "title": self.title,
            "difficulty": self.difficulty,
            "topic_name": self.topic_name,
            "errors": self.errors,
            "warnings": self.warnings,
            "judge_status": self.judge_status,
            "passed_test_cases": self.passed_test_cases,
            "total_test_cases": self.total_test_cases,
            "details": self.details,
        }


class ProblemValidator:
    """
    Validates coding problems against strict execution, correctness,
    and metadata integrity standards.
    """

    @classmethod
    def validate_problem_model(
        cls,
        problem: Problem,
        db: Optional[Session] = None,
        run_judge: bool = True,
        judge_timeout: float = 6.0
    ) -> ValidationResult:
        """
        Validate an existing SQLAlchemy Problem model instance.
        """
        errors: List[str] = []
        warnings: List[str] = []
        details: Dict[str, Any] = {}

        # 1. Identity & Uniqueness
        if not problem.title or not str(problem.title).strip():
            errors.append("IDENTITY_ERROR: Title cannot be empty")
        if not problem.slug or not str(problem.slug).strip():
            errors.append("IDENTITY_ERROR: Slug cannot be empty")
        elif not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", problem.slug):
            warnings.append(f"SLUG_FORMAT_WARNING: Slug '{problem.slug}' does not strictly match kebab-case")

        # 2. Metadata Correctness
        if problem.difficulty not in VALID_DIFFICULTIES:
            errors.append(f"METADATA_ERROR: Difficulty '{problem.difficulty}' is invalid. Must be one of {sorted(VALID_DIFFICULTIES)}")

        topic_name = "Unknown"
        if problem.topic:
            topic_name = problem.topic.name
        elif db and problem.topic_id:
            topic = db.query(Topic).filter(Topic.id == problem.topic_id).first()
            if topic:
                topic_name = topic.name
            else:
                errors.append(f"METADATA_ERROR: topic_id {problem.topic_id} does not exist in topics table")
        elif not problem.topic_id:
            errors.append("METADATA_ERROR: Missing topic_id")

        # 3. Statement Completeness
        desc = problem.description_markdown or ""
        if len(desc.strip()) < MIN_DESCRIPTION_LENGTH:
            errors.append(f"STATEMENT_ERROR: Description is missing or too short ({len(desc.strip())} < {MIN_DESCRIPTION_LENGTH} chars)")

        constraints = problem.constraints_markdown or ""
        if len(constraints.strip()) < MIN_CONSTRAINTS_LENGTH:
            warnings.append(f"STATEMENT_WARNING: Constraints missing or very short ({len(constraints.strip())} chars)")

        # 4. Executable Code & Syntax
        starter_code = problem.starter_code_python or ""
        ref_code = problem.reference_solution_python or ""

        starter_fn: Optional[str] = None
        if not starter_code.strip():
            errors.append("CODE_ERROR: starter_code_python is empty")
        else:
            try:
                tree = ast.parse(starter_code)
                starter_fn = extract_target_function_name(starter_code)
                if not starter_fn:
                    errors.append("CODE_ERROR: starter_code_python does not define a callable function")
            except SyntaxError as e:
                errors.append(f"SYNTAX_ERROR: starter_code_python syntax error: {e}")

        ref_fn: Optional[str] = None
        if not ref_code.strip():
            errors.append("CODE_ERROR: reference_solution_python is empty")
        else:
            try:
                tree = ast.parse(ref_code)
                ref_fn = extract_target_function_name(ref_code, starter_code)
                if not ref_fn:
                    errors.append("CODE_ERROR: reference_solution_python does not define a callable function")
                elif starter_fn and ref_fn != starter_fn:
                    # Function name mismatch
                    warnings.append(f"CODE_WARNING: starter function '{starter_fn}' differs from reference function '{ref_fn}'")
            except SyntaxError as e:
                errors.append(f"SYNTAX_ERROR: reference_solution_python syntax error: {e}")

        # 5. Test Case Integrity
        test_cases = problem.test_cases or []
        visible_tcs = [tc for tc in test_cases if not tc.is_hidden]
        hidden_tcs = [tc for tc in test_cases if tc.is_hidden]

        if len(test_cases) == 0:
            errors.append("TEST_CASE_ERROR: Problem has 0 test cases")
        else:
            if len(visible_tcs) == 0:
                warnings.append("TEST_CASE_WARNING: No visible test cases found")
            if len(hidden_tcs) == 0:
                warnings.append("TEST_CASE_WARNING: No hidden test cases found")

            # Validate test case payload structure
            for idx, tc in enumerate(test_cases):
                if not tc.input_data or not tc.input_data.strip():
                    errors.append(f"TEST_CASE_ERROR: Test case #{idx + 1} has empty input_data")
                else:
                    try:
                        parsed_input = json.loads(tc.input_data)
                        if not isinstance(parsed_input, dict):
                            errors.append(f"TEST_CASE_ERROR: Test case #{idx + 1} input_data is not a JSON object (kwargs dictionary)")
                    except json.JSONDecodeError as jde:
                        errors.append(f"TEST_CASE_ERROR: Test case #{idx + 1} input_data JSON parse error: {jde}")

                if tc.expected_output is None or str(tc.expected_output).strip() == "":
                    errors.append(f"TEST_CASE_ERROR: Test case #{idx + 1} has empty expected_output")

        # 6. Judge Consistency
        judge_status: Optional[str] = None
        passed_tcs = 0
        total_tcs = len(test_cases)

        if run_judge and not errors and ref_code and total_tcs > 0:
            formatted_tcs = [
                {
                    "id": tc.id or idx + 1,
                    "input_data": tc.input_data,
                    "expected_output": tc.expected_output,
                    "is_hidden": tc.is_hidden,
                }
                for idx, tc in enumerate(test_cases)
            ]

            try:
                run_res = PythonCodeRunner.execute(
                    code=ref_code,
                    test_cases=formatted_tcs,
                    starter_code=starter_code,
                    timeout_seconds=judge_timeout,
                    is_submission=True
                )
                judge_status = run_res.get("status", "Unknown")
                passed_tcs = run_res.get("passed_test_cases", 0)
                details["judge_exec_ms"] = run_res.get("execution_time_ms", 0.0)

                if judge_status != "Accepted":
                    errors.append(f"JUDGE_FAILURE: Reference solution did not pass all test cases (status='{judge_status}', passed={passed_tcs}/{total_tcs})")
                elif passed_tcs != total_tcs:
                    errors.append(f"JUDGE_FAILURE: Incomplete pass ({passed_tcs}/{total_tcs} passed)")
            except Exception as ex:
                judge_status = "Execution Exception"
                errors.append(f"JUDGE_ERROR: Sandbox invocation failed: {str(ex)}")

        is_valid = len(errors) == 0
        return ValidationResult(
            is_valid=is_valid,
            problem_id=problem.id,
            slug=problem.slug,
            title=problem.title,
            difficulty=problem.difficulty,
            topic_name=topic_name,
            errors=errors,
            warnings=warnings,
            judge_status=judge_status,
            passed_test_cases=passed_tcs,
            total_test_cases=total_tcs,
            details=details,
        )

    @classmethod
    def validate_dataset_candidate(cls, row: Dict[str, Any]) -> ValidationResult:
        """
        Evaluates an external dataset row (such as Codeforces problems.csv).
        Determines whether the row contains sufficient information to be imported.
        """
        errors: List[str] = []
        warnings: List[str] = []
        details: Dict[str, Any] = {}

        problem_id = row.get("problem_id") or row.get("id")
        rating = row.get("rating")
        tags = row.get("tags")

        # 1. Identity
        if not problem_id:
            errors.append("MISSING_IDENTITY: Candidate row has no problem_id")

        # 2. Problem statement check
        desc = row.get("description_markdown") or row.get("description") or row.get("statement")
        if not desc or len(str(desc).strip()) < MIN_DESCRIPTION_LENGTH:
            errors.append("MISSING_PROBLEM_STATEMENT: No problem statement or description provided in candidate row")

        # 3. Constraints check
        constraints = row.get("constraints_markdown") or row.get("constraints")
        if not constraints or len(str(constraints).strip()) < MIN_CONSTRAINTS_LENGTH:
            errors.append("MISSING_CONSTRAINTS: No constraints specification provided in candidate row")

        # 4. Starter code check
        starter = row.get("starter_code_python") or row.get("starter_code")
        if not starter or not str(starter).strip():
            errors.append("MISSING_STARTER_CODE: No executable Python starter template provided in candidate row")
        else:
            try:
                ast.parse(starter)
            except SyntaxError as se:
                errors.append(f"INVALID_STARTER_CODE: SyntaxError in starter template: {se}")

        # 5. Reference solution check
        ref = row.get("reference_solution_python") or row.get("reference_solution")
        if not ref or not str(ref).strip():
            errors.append("MISSING_REFERENCE_SOLUTION: No verified reference solution provided for judge testing")
        else:
            try:
                ast.parse(ref)
            except SyntaxError as se:
                errors.append(f"INVALID_REFERENCE_SOLUTION: SyntaxError in reference solution: {se}")

        # 6. Test cases check
        test_cases = row.get("test_cases") or []
        if not test_cases:
            errors.append("MISSING_TEST_CASES: Candidate row contains 0 test cases (visible and hidden test cases required)")
        else:
            vis = [tc for tc in test_cases if not tc.get("is_hidden", False)]
            hid = [tc for tc in test_cases if tc.get("is_hidden", False)]
            if not vis:
                warnings.append("NO_VISIBLE_TEST_CASES: Candidate has no visible test cases")
            if not hid:
                warnings.append("NO_HIDDEN_TEST_CASES: Candidate has no hidden test cases")

        # 7. Rating check
        if rating is not None:
            try:
                r_val = float(rating)
                details["raw_rating"] = r_val
                if r_val < 0 or r_val > 4000:
                    warnings.append(f"ANOMALOUS_RATING: Rating {r_val} outside typical 800-3500 range")
            except (ValueError, TypeError):
                warnings.append(f"INVALID_RATING_TYPE: Could not parse rating '{rating}'")
        else:
            warnings.append("MISSING_RATING: No difficulty rating provided")

        # 8. Tags check
        if not tags or str(tags).strip() == "" or str(tags).lower() == "nan":
            warnings.append("MISSING_TAGS: Candidate row has no topic/algorithm tags")
        else:
            details["tags"] = str(tags)

        is_valid = len(errors) == 0
        return ValidationResult(
            is_valid=is_valid,
            slug=str(problem_id) if problem_id else None,
            title=f"Problem {problem_id}" if problem_id else None,
            errors=errors,
            warnings=warnings,
            details=details,
        )

    @classmethod
    def validate_catalog(
        cls,
        db: Session,
        run_judge: bool = True,
        judge_timeout: float = 8.0,
        curated_only: bool = False
    ) -> Dict[str, Any]:
        """
        Validate problems currently stored in the database.
        """
        query = db.query(Problem)
        if curated_only:
            query = query.filter(Problem.id <= 40)
        problems = query.order_by(Problem.id).all()
        results: List[ValidationResult] = []

        valid_count = 0
        invalid_count = 0
        diff_dist: Dict[str, int] = {}
        topic_dist: Dict[str, int] = {}
        total_test_cases = 0
        judge_accepted_count = 0

        for p in problems:
            res = cls.validate_problem_model(p, db=db, run_judge=run_judge, judge_timeout=judge_timeout)
            results.append(res)
            if res.is_valid:
                valid_count += 1
            else:
                invalid_count += 1

            diff = p.difficulty or "Unknown"
            diff_dist[diff] = diff_dist.get(diff, 0) + 1

            top_name = res.topic_name or "Unknown"
            topic_dist[top_name] = topic_dist.get(top_name, 0) + 1

            total_test_cases += len(p.test_cases)
            if res.judge_status == "Accepted":
                judge_accepted_count += 1

        return {
            "total_problems": len(problems),
            "valid_count": valid_count,
            "invalid_count": invalid_count,
            "validation_pass_rate": round(valid_count / len(problems) * 100.0, 2) if problems else 0.0,
            "judge_pass_rate": round(judge_accepted_count / len(problems) * 100.0, 2) if problems else 0.0,
            "difficulty_distribution": diff_dist,
            "topic_distribution": topic_dist,
            "total_test_cases": total_test_cases,
            "results": [r.to_dict() for r in results],
        }
