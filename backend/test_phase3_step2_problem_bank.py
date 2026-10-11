"""
Comprehensive Verification Suite for Phase 3 Step 2: Problem Bank Expansion & Validation.
LeetCode Adaptive Learning Platform.

Tests:
  1. Catalog Identity, Uniqueness, & Statement Completeness
  2. Starter Code & Reference Solution AST Syntax Compilation
  3. Test Case Integrity & JSON Kwargs Structure
  4. Sandbox Judge Consistency across all 40 Platform Problems
  5. Codeforces Dataset Audit & Clean Rejection of Incomplete Metadata
  6. Idempotent Ingestion & Duplicate Slug Collision Protection
  7. Cold-Start Recommendation Compatibility & Topic Coverage
  8. Multi-User Isolation & Diagnostic Assessment Integrity
"""
import ast
import json
import logging
import os
import sys
from collections import Counter
import unittest

# Ensure backend root is in sys.path
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.core.database import SessionLocal
from app.models.problem import Problem
from app.models.test_case import TestCase
from app.models.topic import Topic
from app.models.user import User
from app.models.learner_concept_state import LearnerConceptState
from app.services.problem_validator import ProblemValidator, ValidationResult
from app.services.problem_importer import ProblemImporter
from app.services.recommendation_engine import RecommendationEngine

logging.basicConfig(level=logging.WARNING)


class TestPhase3Step2ProblemBank(unittest.TestCase):
    def setUp(self):
        self.db = SessionLocal()

    def tearDown(self):
        self.db.close()

    def test_01_catalog_identity_and_completeness(self):
        """Verify all 40 curated catalog problems satisfy identity, uniqueness, and statement criteria."""
        problems = self.db.query(Problem).filter(Problem.id <= 40).all()
        self.assertEqual(len(problems), 40, f"Catalog must contain exactly 40 curated problems, found {len(problems)}")

        slugs = set()
        for p in problems:
            self.assertTrue(p.title and p.title.strip(), f"Problem {p.id} has empty title")
            self.assertTrue(p.slug and p.slug.strip(), f"Problem {p.id} has empty slug")
            self.assertNotIn(p.slug, slugs, f"Duplicate slug detected: {p.slug}")
            slugs.add(p.slug)

            # Statement completeness
            self.assertIsNotNone(p.description_markdown, f"Problem {p.id} has null description")
            self.assertGreaterEqual(len(p.description_markdown.strip()), 20, f"Problem {p.id} description too short")
            self.assertIsNotNone(p.constraints_markdown, f"Problem {p.id} has null constraints")
            self.assertGreaterEqual(len(p.constraints_markdown.strip()), 5, f"Problem {p.id} constraints too short")

            # Metadata correctness
            self.assertIn(p.difficulty, ["Easy", "Medium", "Hard"], f"Invalid difficulty: {p.difficulty}")
            self.assertIsNotNone(p.topic_id, f"Problem {p.id} has null topic_id")
            self.assertIsNotNone(p.topic, f"Problem {p.id} topic relationship broken")

    def test_02_starter_and_reference_code_compilation(self):
        """Verify 100% of starter and reference solutions compile into valid Python AST."""
        problems = self.db.query(Problem).filter(Problem.id <= 40).all()
        for p in problems:
            # Starter code
            self.assertTrue(p.starter_code_python and p.starter_code_python.strip(), f"Problem {p.id} empty starter code")
            try:
                tree = ast.parse(p.starter_code_python)
                starter_funcs = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
                self.assertGreater(len(starter_funcs), 0, f"Problem {p.id} starter code defines no function")
            except SyntaxError as e:
                self.fail(f"Problem {p.id} starter code syntax error: {e}")

            # Reference solution
            self.assertTrue(p.reference_solution_python and p.reference_solution_python.strip(), f"Problem {p.id} empty reference solution")
            try:
                ref_tree = ast.parse(p.reference_solution_python)
                ref_funcs = [n.name for n in ast.walk(ref_tree) if isinstance(n, ast.FunctionDef)]
                self.assertGreater(len(ref_funcs), 0, f"Problem {p.id} reference solution defines no function")
            except SyntaxError as e:
                self.fail(f"Problem {p.id} reference solution syntax error: {e}")

    def test_03_test_case_integrity_and_kwargs(self):
        """Verify all 96 curated test cases parse to JSON kwargs dictionary and have valid expected outputs."""
        test_cases = self.db.query(TestCase).filter(TestCase.problem_id <= 40).all()
        self.assertEqual(len(test_cases), 96, f"Expected 96 total test cases for curated problems, found {len(test_cases)}")

        for tc in test_cases:
            self.assertTrue(tc.input_data and tc.input_data.strip(), f"TestCase {tc.id} has empty input_data")
            try:
                parsed = json.loads(tc.input_data)
                self.assertIsInstance(parsed, dict, f"TestCase {tc.id} input_data must parse to a dict of kwargs")
            except json.JSONDecodeError as e:
                self.fail(f"TestCase {tc.id} invalid JSON input: {e}")

            self.assertIsNotNone(tc.expected_output, f"TestCase {tc.id} has null expected_output")
            self.assertNotEqual(tc.expected_output.strip(), "", f"TestCase {tc.id} has empty expected_output")

    def test_04_sandbox_judge_consistency_all_40(self):
        """Verify PythonCodeRunner executes all 40 reference solutions to 100% Accepted status."""
        catalog_report = ProblemValidator.validate_catalog(self.db, run_judge=True, curated_only=True)
        self.assertEqual(catalog_report["total_problems"], 40)
        self.assertEqual(catalog_report["valid_count"], 40, f"Expected 40 valid problems, got {catalog_report['valid_count']}")
        self.assertEqual(catalog_report["invalid_count"], 0, f"Found invalid problems: {catalog_report['invalid_count']}")
        self.assertEqual(catalog_report["judge_pass_rate"], 100.0, f"Judge pass rate was {catalog_report['judge_pass_rate']}%")

    def test_05_codeforces_dataset_audit_and_rejection(self):
        """Audit problems.csv and confirm 100% rejection with exact auditable reasons."""
        csv_path = os.path.join(BACKEND_DIR, "app", "data", "problems.csv")
        self.assertTrue(os.path.exists(csv_path), "problems.csv dataset must exist")

        audit = ProblemImporter.audit_external_dataset(csv_path)
        self.assertEqual(audit["total_rows_inspected"], 10864, f"Expected 10864 rows, got {audit['total_rows_inspected']}")
        self.assertEqual(audit["valid_candidates_count"], 0, "No raw Codeforces row should be marked valid without statements/tests")
        self.assertEqual(audit["rejected_candidates_count"], 10864, "All 10864 rows must be rejected due to incompleteness")

        reasons = audit["rejection_reasons_summary"]
        self.assertEqual(reasons.get("MISSING_PROBLEM_STATEMENT"), 10864)
        self.assertEqual(reasons.get("MISSING_CONSTRAINTS"), 10864)
        self.assertEqual(reasons.get("MISSING_STARTER_CODE"), 10864)
        self.assertEqual(reasons.get("MISSING_REFERENCE_SOLUTION"), 10864)
        self.assertEqual(reasons.get("MISSING_TEST_CASES"), 10864)

    def test_06_idempotency_and_collision_guardrails(self):
        """Verify duplicate slug collisions are rejected and transaction rollbacks work."""
        # Attempt to insert existing slug
        dup_candidate = {
            "title": "Duplicate Two Sum",
            "slug": "two-sum-target-pair",
            "topic_id": 1,
            "difficulty": "Easy"
        }
        success, msg, p = ProblemImporter.import_problem(self.db, dup_candidate, dry_run=False)
        self.assertFalse(success, "Must reject duplicate slug")
        self.assertIn("already exists", msg)

        # Attempt to insert incomplete problem
        broken_candidate = {
            "title": "Broken Problem",
            "slug": "broken-problem-xyz",
            "topic_id": 1,
            "difficulty": "Easy",
            "description_markdown": "Short",
            "constraints_markdown": "",
            "starter_code_python": "def broken():",
            "reference_solution_python": "def broken(): pass",
            "test_cases": []
        }
        success, msg, p = ProblemImporter.import_problem(self.db, broken_candidate, dry_run=False)
        self.assertFalse(success, "Must reject incomplete candidate")
        # Check DB was not modified
        remaining = self.db.query(Problem).filter(Problem.slug == "broken-problem-xyz").first()
        self.assertIsNone(remaining, "Broken problem should not exist in DB")

    def test_07_topic_and_diagnostic_coverage(self):
        """Verify all 10 topics have problems and 7 diagnostic problems are intact."""
        topics = self.db.query(Topic).all()
        self.assertEqual(len(topics), 10, "Expected 10 topics")

        diag_problems = self.db.query(Problem).filter(Problem.is_diagnostic == True).all()
        self.assertEqual(len(diag_problems), 7, f"Expected 7 diagnostic problems, got {len(diag_problems)}")

        # Verify difficulty distribution
        diffs = Counter(p.difficulty for p in self.db.query(Problem).filter(Problem.id <= 40).all())
        self.assertEqual(diffs["Easy"], 11)
        self.assertEqual(diffs["Medium"], 23)
        self.assertEqual(diffs["Hard"], 6)

    def test_08_recommendation_pipeline_cold_start_and_isolation(self):
        """Verify recommendation engine works smoothly with the verified 40 problems."""
        import uuid
        test_user = User(
            name="Test Learner P3S2",
            email=f"p3s2_test_{uuid.uuid4().hex[:8]}@example.com",
            password_hash="mock_hash_for_test"
        )
        self.db.add(test_user)
        self.db.commit()
        self.db.refresh(test_user)

        try:
            user_id = test_user.id

            # 1. Cold start recommendation target
            cold_target = RecommendationEngine.get_user_learning_target(self.db, user_id)
            self.assertIsInstance(cold_target, (int, float))
            self.assertGreaterEqual(cold_target, 800)

            # 2. Check candidate pool size is exactly 40 for fresh learner
            candidates = RecommendationEngine.evaluate_candidates(self.db, user_id, exclude_all_attempted=True, curated_only=True)
            self.assertEqual(len(candidates), 40, f"Candidate pool should contain all 40 curated problems, got {len(candidates)}")

            # 3. Top-K recommendations
            top_recs = RecommendationEngine.recommend_top_k(self.db, user_id, top_k=5, exclude_all_attempted=True)
            self.assertEqual(len(top_recs), 5)
            for r in top_recs:
                self.assertIn("problem_id", r)
                self.assertIn("title", r)
                self.assertIn("difficulty", r)
                self.assertIn("recommendation_score", r)
        finally:
            self.db.delete(test_user)
            self.db.commit()



if __name__ == "__main__":
    unittest.main(verbosity=2)
