"""
Final Implementation Verification Test Suite
Covers all 20 required acceptance criteria from Phase 1 to Phase 16:
1. Exactly 889 problems
2. Sequential numbering 1-889
3. No duplicate numbering
4. No missing numbering / no gaps
5. Deterministic ordering in API
6. Multi-language support for diagnostic problems
7. Language execution across supported languages
8. Diagnostic problem descriptions and constraints returned
9. Diagnostic fake is_solved attack rejected
10. Run code does not create diagnostic attempt
11. Submit creates correct diagnostic attempt
12. Failed submission is not marked solved
13. Successful submission is marked solved
14. Diagnostic completion and score persistence
15. Diagnostic retake prevention
16. Diagnostic gate bypass prevention
17. Learner-specific recommendation divergence
18. Recommendation final_score sorting
19. Attempted problem exclusion
20. Recommendation diversity preservation
"""
import uuid
import json
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.main import app
from app.core.database import SessionLocal
from app.models.user import User
from app.models.problem import Problem
from app.models.test_case import TestCase
from app.models.diagnostic_attempt import DiagnosticAttempt
from app.models.submission import Submission
from app.models.learner_knowledge_state import LearnerKnowledgeState
from app.models.learner_concept_state import LearnerConceptState
from app.core.security import get_password_hash, create_access_token
from app.engine.code_runner import CodeRunner
from app.services.recommendation_engine import RecommendationEngine

client = TestClient(app)


class TestFinalImplementationSuite:
    def setup_method(self):
        self.db = SessionLocal()
        self.test_user_ids = []

    def teardown_method(self):
        try:
            if self.test_user_ids:
                uids = ",".join(str(i) for i in self.test_user_ids)
                for t in [
                    "submissions",
                    "diagnostic_attempts",
                    "recommendations",
                    "learner_knowledge_state",
                    "learner_concept_states",
                    "onboarding_profiles"
                ]:
                    self.db.execute(text(f"DELETE FROM {t} WHERE user_id IN ({uids})"))
                self.db.execute(text(f"DELETE FROM users WHERE id IN ({uids})"))
                self.db.commit()
        finally:
            self.db.close()

    def _create_student(self, exempt=False, completed=False):
        uid = uuid.uuid4().hex[:8]
        user = User(
            email=f"final_impl_{uid}@test.com",
            password_hash=get_password_hash("StudentPass123!"),
            name=f"Final Test {uid}",
            role="STUDENT",
            diagnostic_exempt=exempt,
            diagnostic_completed=completed
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        self.test_user_ids.append(user.id)
        token = create_access_token(subject=str(user.id), role="STUDENT")
        headers = {"Authorization": f"Bearer {token}"}
        return user, token, headers

    # 1. Exactly 889 problems
    def test_01_catalog_has_exactly_889_problems(self):
        total = self.db.query(Problem).count()
        assert total == 889, f"Expected exactly 889 problems in database, got {total}"

    # 2. Sequential numbering 1..889
    def test_02_sequential_numbering_1_to_889(self):
        probs = self.db.query(Problem).order_by(Problem.order_index.asc()).all()
        order_indices = [p.order_index for p in probs]
        expected = list(range(1, 890))
        assert order_indices == expected, f"Order indices do not match 1..889 sequentially: min={min(order_indices)}, max={max(order_indices)}"

    # 3. No duplicate numbering
    def test_03_no_duplicate_numbering(self):
        probs = self.db.query(Problem).all()
        order_indices = [p.order_index for p in probs]
        assert len(order_indices) == len(set(order_indices)) == 889, "Found duplicate order_index values in catalog"

    # 4. No missing numbering / no gaps
    def test_04_no_missing_numbering_and_no_gaps(self):
        probs = self.db.query(Problem).all()
        existing_set = {p.order_index for p in probs}
        expected_set = set(range(1, 890))
        diff = expected_set - existing_set
        assert len(diff) == 0, f"Found missing order_indices: {diff}"

    # 5. Deterministic ordering in API
    def test_05_deterministic_ordering_in_api(self):
        res = client.get("/api/problems?limit=50")
        assert res.status_code == 200
        data = res.json()
        assert len(data) == 50
        api_order = [p["order_index"] for p in data]
        assert api_order == list(range(1, 51)), f"API ordering is not sequentially 1..50: {api_order[:10]}"

    # 6. All diagnostic problems have all 4 languages
    def test_06_all_diagnostic_problems_have_all_four_languages(self):
        diag_probs = self.db.query(Problem).filter(Problem.is_diagnostic == True).order_by(Problem.order_index.asc()).all()
        assert len(diag_probs) == 7
        expected_languages = ["python", "java", "cpp", "javascript"]
        for p in diag_probs:
            for lang in expected_languages:
                assert lang in p.supported_languages, f"Problem {p.id} ({p.title}) missing language {lang}"

    # 7. Language execution across supported languages
    def test_07_language_execution_for_problem_1(self):
        p1 = self.db.query(Problem).filter(Problem.id == 1).first()
        tcs = [{"id": tc.id, "input_data": tc.input_data, "expected_output": tc.expected_output, "is_hidden": tc.is_hidden} for tc in p1.test_cases]

        # Python
        py_res = CodeRunner.execute(p1.reference_solution_python, tcs, "python", p1.starter_code_python, is_submission=True)
        assert py_res["status"] == "Accepted", f"Python solution failed: {py_res}"

        # JavaScript
        js_res = CodeRunner.execute(p1.reference_solution_javascript, tcs, "javascript", p1.starter_code_javascript, is_submission=True)
        assert js_res["status"] == "Accepted", f"JavaScript solution failed: {js_res}"

        # Java
        java_res = CodeRunner.execute(p1.reference_solution_java, tcs, "java", p1.starter_code_java, is_submission=True)
        assert java_res["status"] == "Accepted", f"Java solution failed: {java_res}"

        # C++
        cpp_res = CodeRunner.execute(p1.reference_solution_cpp, tcs, "cpp", p1.starter_code_cpp, is_submission=True)
        assert cpp_res["status"] == "Accepted", f"C++ solution failed: {cpp_res}"

    # 8. Diagnostic problem descriptions and constraints returned
    def test_08_diagnostic_endpoint_returns_descriptions_and_constraints(self):
        res = client.get("/api/diagnostic/problems")
        assert res.status_code == 200
        data = res.json()
        assert len(data) == 7
        for p in data:
            assert p.get("description_markdown") is not None, f"Problem {p['id']} missing description_markdown"
            assert len(p["description_markdown"].strip()) > 10, f"Problem {p['id']} has empty description_markdown"
            assert "Write an optimal solution in Python." not in p["description_markdown"], f"Problem {p['id']} has placeholder fallback description"

    # 9. Diagnostic fake is_solved attack rejected
    def test_09_fake_is_solved_attack_with_failing_code_is_rejected(self):
        user, token, headers = self._create_student(exempt=False, completed=False)

        # Malicious payload: claims is_solved=True but code returns wrong answer
        failing_code = "def twoSum(nums, target):\n    return []\n"
        res = client.post("/api/diagnostic/submit", headers=headers, json={
            "problem_id": 1,
            "is_solved": True,
            "code_submitted": failing_code,
            "language": "python"
        })
        assert res.status_code == 200
        data = res.json()
        assert data["is_solved"] is False, "Server trusted fake is_solved=True with failing code!"

        # Empty code attack
        res_empty = client.post("/api/diagnostic/submit", headers=headers, json={
            "problem_id": 1,
            "is_solved": True,
            "code_submitted": "   ",
            "language": "python"
        })
        assert res_empty.status_code == 200
        assert res_empty.json()["is_solved"] is False, "Server trusted fake is_solved=True with empty code!"

        # Syntax error attack
        res_syntax = client.post("/api/diagnostic/submit", headers=headers, json={
            "problem_id": 1,
            "is_solved": True,
            "code_submitted": "def invalid syntax : (",
            "language": "python"
        })
        assert res_syntax.status_code == 200
        assert res_syntax.json()["is_solved"] is False, "Server trusted fake is_solved=True with syntax error code!"

    # 10. Run code does not create diagnostic attempt
    def test_10_run_code_does_not_create_diagnostic_attempt(self):
        user, token, headers = self._create_student(exempt=False, completed=False)
        p1 = self.db.query(Problem).filter(Problem.id == 1).first()

        res = client.post("/api/submissions/run", headers=headers, json={
            "problem_id": 1,
            "code": p1.reference_solution_python,
            "language": "python"
        })
        assert res.status_code == 200

        self.db.rollback()
        attempt_count = self.db.query(DiagnosticAttempt).filter(DiagnosticAttempt.user_id == user.id).count()
        assert attempt_count == 0, f"Run code created an attempt in diagnostic_attempts table! Found {attempt_count}"

    # 11. Submit creates correct diagnostic attempt
    def test_11_submit_creates_diagnostic_attempt(self):
        user, token, headers = self._create_student(exempt=False, completed=False)
        p1 = self.db.query(Problem).filter(Problem.id == 1).first()

        res = client.post("/api/diagnostic/submit", headers=headers, json={
            "problem_id": 1,
            "code_submitted": p1.reference_solution_python,
            "language": "python",
            "time_spent_seconds": 25
        })
        assert res.status_code == 200
        data = res.json()
        assert data["is_solved"] is True
        assert data["language"] == "python"

        self.db.rollback()
        db_att = self.db.query(DiagnosticAttempt).filter(
            DiagnosticAttempt.user_id == user.id,
            DiagnosticAttempt.problem_id == 1
        ).first()
        assert db_att is not None
        assert db_att.is_solved is True

    # 12. Failed submission is not marked solved
    def test_12_failed_submission_is_not_marked_solved(self):
        user, token, headers = self._create_student(exempt=False, completed=False)

        res = client.post("/api/diagnostic/submit", headers=headers, json={
            "problem_id": 1,
            "code_submitted": "def twoSum(nums, target):\n    return [0, 0]\n",
            "language": "python"
        })
        assert res.status_code == 200
        assert res.json()["is_solved"] is False

    # 13. Successful submission is marked solved
    def test_13_successful_submission_is_marked_solved(self):
        user, token, headers = self._create_student(exempt=False, completed=False)
        p6 = self.db.query(Problem).filter(Problem.id == 6).first()

        res = client.post("/api/diagnostic/submit", headers=headers, json={
            "problem_id": 6,
            "code_submitted": p6.reference_solution_python,
            "language": "python"
        })
        assert res.status_code == 200
        assert res.json()["is_solved"] is True

    # 14. Diagnostic completion and score persistence
    def test_14_diagnostic_completion_and_score(self):
        user, token, headers = self._create_student(exempt=False, completed=False)
        diag_probs = self.db.query(Problem).filter(Problem.is_diagnostic == True).order_by(Problem.order_index.asc()).all()

        # Solve 3 problems correctly, 4 with wrong code
        for i, p in enumerate(diag_probs):
            code = p.reference_solution_python if i < 3 else "def solve(): return None\n"
            client.post("/api/diagnostic/submit", headers=headers, json={
                "problem_id": p.id,
                "code_submitted": code,
                "language": "python"
            })

        comp_res = client.post("/api/diagnostic/complete", headers=headers)
        assert comp_res.status_code == 200
        data = comp_res.json()
        assert data["total_problems"] == 7
        assert data["solved_count"] == 3

        # Verify DB directly
        self.db.rollback()
        fresh_user = self.db.query(User).filter(User.id == user.id).first()
        assert fresh_user.diagnostic_completed is True
        assert fresh_user.diagnostic_score == 3
        assert fresh_user.diagnostic_total == 7

    # 15. Diagnostic retake prevention
    def test_15_diagnostic_retake_prevention(self):
        user, token, headers = self._create_student(exempt=False, completed=True)

        res = client.post("/api/diagnostic/submit", headers=headers, json={
            "problem_id": 1,
            "code_submitted": "def twoSum(nums, target): return []",
            "language": "python"
        })
        assert res.status_code == 400
        assert "already been completed" in res.json()["detail"].lower()

        res2 = client.get("/api/diagnostic/problems", headers=headers)
        assert res2.status_code == 400

    # 16. Diagnostic gate bypass prevention
    def test_16_diagnostic_gate_bypass_prevention(self):
        user, token, headers = self._create_student(exempt=False, completed=False)

        res = client.get("/api/recommendations/next", headers=headers)
        assert res.status_code == 403, f"Expected 403 gated, got {res.status_code}"

    # 17. Learner-specific recommendation divergence
    def test_17_learner_specific_recommendation_divergence(self):
        # Create Student A: completed diagnostic, high mastery in Trees, very low in DP
        user_a, token_a, headers_a = self._create_student(exempt=False, completed=True)
        # Create Student B: completed diagnostic, high mastery in DP, very low in Trees
        user_b, token_b, headers_b = self._create_student(exempt=False, completed=True)

        from app.ml.state_engine import KnowledgeStateEngine
        KnowledgeStateEngine.get_or_initialize_user_concept_states(self.db, user_a.id)
        KnowledgeStateEngine.get_or_initialize_user_concept_states(self.db, user_b.id)

        # Set user_a weak in "dp" (0 solved out of 5)
        dp_a = self.db.query(LearnerConceptState).filter(
            LearnerConceptState.user_id == user_a.id,
            LearnerConceptState.concept == "dp"
        ).first()
        if dp_a:
            dp_a.interactions = 5
            dp_a.solved_count = 0
            dp_a.mastery_score = 0.14
            dp_a.weakness_score = 0.86
            dp_a.confidence_score = 0.50
            dp_a.weakness_level = "Very High"

        # Set user_b weak in "trees" (0 solved out of 5)
        trees_b = self.db.query(LearnerConceptState).filter(
            LearnerConceptState.user_id == user_b.id,
            LearnerConceptState.concept == "trees"
        ).first()
        if trees_b:
            trees_b.interactions = 5
            trees_b.solved_count = 0
            trees_b.mastery_score = 0.14
            trees_b.weakness_score = 0.86
            trees_b.confidence_score = 0.50
            trees_b.weakness_level = "Very High"

        self.db.commit()

        cands_a = RecommendationEngine.evaluate_candidates(self.db, user_a.id, exclude_all_attempted=True)
        cands_b = RecommendationEngine.evaluate_candidates(self.db, user_b.id, exclude_all_attempted=True)

        assert len(cands_a) > 0
        assert len(cands_b) > 0
        # Student A's top candidate targets DP, while Student B's top candidate targets Trees
        top_prob_a = cands_a[0]["problem"].id
        top_prob_b = cands_b[0]["problem"].id
        assert top_prob_a != top_prob_b, f"Expected different recommendations for different learners, but got same: A={top_prob_a}, B={top_prob_b}"

    # 18. Recommendation final_score sorting
    def test_18_recommendation_final_score_sorting(self):
        user, token, headers = self._create_student(exempt=False, completed=True)
        scored = RecommendationEngine.evaluate_candidates(self.db, user.id)
        assert len(scored) > 0
        final_scores = [item["final_score"] for item in scored]
        # Check sorted descending
        for i in range(len(final_scores) - 1):
            assert final_scores[i] >= final_scores[i + 1], f"Candidates not sorted by final_score descending at index {i}: {final_scores[i]} < {final_scores[i+1]}"

    # 19. Attempted problem exclusion
    def test_19_attempted_problem_exclusion(self):
        user, token, headers = self._create_student(exempt=False, completed=True)
        # Record a submission on Problem 43
        sub = Submission(
            user_id=user.id,
            problem_id=43,
            language="python",
            code="def foo(): pass",
            status="Wrong Answer",
            passed_test_cases=0,
            total_test_cases=2,
            execution_time_ms=10.0
        )
        self.db.add(sub)
        self.db.commit()

        recs = RecommendationEngine.recommend_top_k(self.db, user.id, top_k=20, exclude_all_attempted=True)
        rec_ids = [r["problem"].id for r in recs]
        assert 43 not in rec_ids, "Attempted problem 43 was not excluded from recommendations!"

    # 20. Recommendation diversity preservation
    def test_20_recommendation_diversity_preserved(self):
        user, token, headers = self._create_student(exempt=False, completed=True)
        recs = RecommendationEngine.recommend_top_k(self.db, user.id, top_k=5, max_same_primary_concept=2)
        assert len(recs) <= 5
        concept_counts = {}
        for r in recs:
            p_c = r["primary_concept"]
            concept_counts[p_c] = concept_counts.get(p_c, 0) + 1
            assert concept_counts[p_c] <= 2, f"Primary concept '{p_c}' exceeded max diversity limit of 2: count={concept_counts[p_c]}"
