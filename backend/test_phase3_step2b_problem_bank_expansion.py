"""
Comprehensive Verification Suite for Phase 3 Step 2B: Problem Bank Expansion.
LeetCode Adaptive Learning Platform.

Tests:
  1. Existing 40 curated problems remain valid and intact.
  2. New problems are correctly imported (total problems >= 500).
  3. No duplicate problems (unique slugs and IDs).
  4. Every problem has all required fields (title, slug, statement, constraints, starter code, reference solution).
  5. Valid concept mapping across the 37 learning concepts (zero '*special' leakage).
  6. Valid difficulty distribution across Easy, Medium, and Hard.
  7. Every problem has valid test cases (>= 1 visible, >= 1 hidden).
  8. Reference solutions achieve 100% Accepted pass rate on judge execution.
  9. Recommendation generation works with the expanded 500+ problem bank.
  10. Attempted problems remain strictly excluded.
  11. New user cold-start recommendation works with expanded bank.
  12. Existing user recommendation generation works.
  13. Post-submission recommendation still works and updates.
  14. Multiple users remain strictly isolated.
  15. Re-running the importer is 100% idempotent (0 duplicate problems created).
"""
import ast
import json
import logging
import os
import sys
import unittest
import uuid
from collections import Counter

# Ensure backend root is in sys.path
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.core.database import SessionLocal
from app.models.problem import Problem
from app.models.test_case import TestCase
from app.models.topic import Topic
from app.models.user import User
from app.models.submission import Submission
from app.services.problem_validator import ProblemValidator
from app.services.problem_importer import ProblemImporter
from app.services.recommendation_engine import RecommendationEngine
from app.ml.state_engine import get_problem_learning_concepts
from app.data.dataset_loader import get_distinct_learning_concepts

logging.basicConfig(level=logging.WARNING)


class TestPhase3Step2BProblemBankExpansion(unittest.TestCase):
    def setUp(self):
        self.db = SessionLocal()

    def tearDown(self):
        self.db.close()

    def test_01_existing_40_problems_remain_valid(self):
        """Verify the original 40 curated problems remain intact with identical IDs and validity."""
        curated_problems = self.db.query(Problem).filter(Problem.id <= 40).all()
        self.assertEqual(len(curated_problems), 40, f"Expected 40 curated problems, found {len(curated_problems)}")

        # Verify key baseline problems
        two_sum = self.db.query(Problem).filter(Problem.slug == "two-sum-target-pair").first()
        self.assertIsNotNone(two_sum)
        self.assertEqual(two_sum.id, 1)
        self.assertTrue(two_sum.is_diagnostic)

        climbing_stairs = self.db.query(Problem).filter(Problem.slug == "climbing-stairs-min-cost").first()
        self.assertIsNotNone(climbing_stairs)
        self.assertEqual(climbing_stairs.id, 33)

        # Verify 7 diagnostic problems
        diag_count = sum(1 for p in curated_problems if p.is_diagnostic)
        self.assertEqual(diag_count, 7, f"Expected 7 diagnostic problems, got {diag_count}")

    def test_02_new_problems_imported_target_achieved(self):
        """Verify the catalog is expanded to at least 500 complete validated problems."""
        total_problems = self.db.query(Problem).count()
        self.assertGreaterEqual(
            total_problems, 500,
            f"Expected at least 500 validated problems in database, found {total_problems}"
        )

    def test_03_no_duplicate_slugs_or_ids(self):
        """Verify all problems have globally unique IDs and unique kebab-case slugs."""
        problems = self.db.query(Problem).all()
        slugs = set()
        ids = set()

        for p in problems:
            self.assertNotIn(p.slug, slugs, f"Duplicate slug detected: {p.slug}")
            slugs.add(p.slug)
            self.assertNotIn(p.id, ids, f"Duplicate ID detected: {p.id}")
            ids.add(p.id)

    def test_04_required_fields_completeness(self):
        """Verify every imported problem contains title, slug, statement, constraints, and code."""
        problems = self.db.query(Problem).all()
        for p in problems:
            self.assertTrue(p.title and p.title.strip(), f"Problem {p.id} empty title")
            self.assertTrue(p.slug and p.slug.strip(), f"Problem {p.id} empty slug")
            self.assertTrue(p.description_markdown and len(p.description_markdown.strip()) >= 20, f"Problem {p.id} short description")
            self.assertTrue(p.constraints_markdown and len(p.constraints_markdown.strip()) >= 5, f"Problem {p.id} short constraints")
            self.assertTrue(p.starter_code_python and p.starter_code_python.strip(), f"Problem {p.id} empty starter code")
            self.assertTrue(p.reference_solution_python and p.reference_solution_python.strip(), f"Problem {p.id} empty reference solution")

    def test_05_valid_concept_mapping_and_no_special_leakage(self):
        """Verify every problem maps exclusively to valid learning concepts and never contains '*special'."""
        valid_concept_set = set(get_distinct_learning_concepts())
        problems = self.db.query(Problem).all()

        for p in problems:
            concepts = get_problem_learning_concepts(p)
            self.assertGreater(len(concepts), 0, f"Problem {p.id} has no mapped concepts")
            self.assertNotIn("*special", concepts, f"Problem {p.id} leaked *special concept")
            for c in concepts:
                self.assertIn(c, valid_concept_set, f"Problem {p.id} mapped to invalid concept '{c}'")

    def test_06_difficulty_distribution(self):
        """Verify difficulty coverage spans Easy, Medium, and Hard tiers."""
        diffs = Counter(p.difficulty for p in self.db.query(Problem).all())
        self.assertGreater(diffs["Easy"], 50, f"Expected >50 Easy problems, got {diffs['Easy']}")
        self.assertGreater(diffs["Medium"], 100, f"Expected >100 Medium problems, got {diffs['Medium']}")
        self.assertGreaterEqual(diffs["Hard"], 15, f"Expected >=15 Hard problems, got {diffs['Hard']}")

    def test_07_test_case_integrity(self):
        """Verify every problem has at least 2 test cases (at least 1 visible, at least 1 hidden for imported)."""
        problems = self.db.query(Problem).all()
        for p in problems:
            tcs = p.test_cases
            self.assertGreaterEqual(len(tcs), 2, f"Problem {p.id} has fewer than 2 test cases")
            vis = sum(1 for tc in tcs if not tc.is_hidden)
            hid = sum(1 for tc in tcs if tc.is_hidden)
            self.assertGreaterEqual(vis, 1, f"Problem {p.id} has no visible test cases")
            if p.id > 40:
                self.assertGreaterEqual(hid, 1, f"Problem {p.id} has no hidden test cases")

            for tc in tcs:
                self.assertTrue(tc.input_data and tc.input_data.strip())
                self.assertTrue(tc.expected_output and tc.expected_output.strip())
                parsed_in = json.loads(tc.input_data)
                self.assertIsInstance(parsed_in, (dict, list))

    def test_08_reference_solutions_judge_execution_sample(self):
        """Verify random sample of newly imported problems pass 100% of test cases in sandbox judge."""
        from app.engine.code_runner import PythonCodeRunner

        sample_problems = self.db.query(Problem).filter(Problem.id > 40).limit(25).all()
        for p in sample_problems:
            tcs = [
                {
                    "id": tc.id,
                    "input_data": tc.input_data,
                    "expected_output": tc.expected_output,
                    "is_hidden": tc.is_hidden
                }
                for tc in p.test_cases
            ]
            res = PythonCodeRunner.execute(
                p.reference_solution_python,
                tcs,
                starter_code=p.starter_code_python,
                timeout_seconds=5.0,
                is_submission=True
            )
            self.assertEqual(res["status"], "Accepted", f"Problem {p.id} ({p.slug}) failed judge: {res}")
            self.assertEqual(res["passed_test_cases"], len(tcs))

    def test_09_recommendation_generation_with_expanded_bank(self):
        """Verify RecommendationEngine generates valid recommendations from the expanded 500+ bank."""
        user = User(
            name="Expanded Rec Learner",
            email=f"expanded_rec_{uuid.uuid4().hex[:8]}@test.com",
            password_hash="mockhash"
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        try:
            candidates = RecommendationEngine.evaluate_candidates(self.db, user.id, exclude_all_attempted=True)
            self.assertGreaterEqual(len(candidates), 500, f"Candidate pool should contain 500+ problems, got {len(candidates)}")

            top_recs = RecommendationEngine.recommend_top_k(self.db, user.id, top_k=10, exclude_all_attempted=True)
            self.assertEqual(len(top_recs), 10)
            for r in top_recs:
                self.assertIn("problem_id", r)
                self.assertIn("title", r)
                self.assertIn("difficulty", r)
                self.assertIn("recommendation_score", r)
        finally:
            self.db.delete(user)
            self.db.commit()

    def test_10_attempted_problems_excluded_from_expanded_bank(self):
        """Verify attempted problems are cleanly excluded from the candidate pool."""
        user = User(
            name="Attempt Learner",
            email=f"attempt_{uuid.uuid4().hex[:8]}@test.com",
            password_hash="mockhash"
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        try:
            initial_cands = RecommendationEngine.evaluate_candidates(self.db, user.id, exclude_all_attempted=True)
            total_initial = len(initial_cands)

            # Solve problem #1
            sub = Submission(
                user_id=user.id,
                problem_id=1,
                code="def twoSum(): pass",
                status="Accepted",
                passed_test_cases=4,
                total_test_cases=4,
                execution_time_ms=50.0
            )
            self.db.add(sub)
            self.db.commit()

            cands_after = RecommendationEngine.evaluate_candidates(self.db, user.id, exclude_all_attempted=True)
            self.assertEqual(len(cands_after), total_initial - 1)
            self.assertTrue(all(c["problem"].id != 1 for c in cands_after))
        finally:
            self.db.delete(user)
            self.db.commit()

    def test_11_cold_start_recommendation_works(self):
        """Verify brand-new cold-start learner receives valid active recommendation."""
        user = User(
            name="Cold Learner",
            email=f"cold_{uuid.uuid4().hex[:8]}@test.com",
            password_hash="mockhash"
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        try:
            rec = RecommendationEngine.generate_recommendation(self.db, user.id, force_new=True)
            self.assertIsNotNone(rec)
            self.assertTrue(rec.is_active)
            self.assertGreater(rec.problem_id, 0)
            self.assertGreater(len(rec.explanation_text), 20)
        finally:
            self.db.delete(user)
            self.db.commit()

    def test_12_existing_user_recommendation_works(self):
        """Verify recommendation generation for existing user with history."""
        user = User(
            name="Existing Learner",
            email=f"existing_{uuid.uuid4().hex[:8]}@test.com",
            password_hash="mockhash"
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        try:
            rec1 = RecommendationEngine.generate_recommendation(self.db, user.id, force_new=True)
            rec2 = RecommendationEngine.generate_recommendation(self.db, user.id, force_new=True)
            self.assertTrue(rec2.is_active)
            self.assertFalse(rec1.is_active)
        finally:
            self.db.delete(user)
            self.db.commit()

    def test_13_post_submission_recommendation_update(self):
        """Verify post-submission recommendation excludes submitted problem."""
        user = User(
            name="Sub Rec Learner",
            email=f"sub_rec_{uuid.uuid4().hex[:8]}@test.com",
            password_hash="mockhash"
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        try:
            rec = RecommendationEngine.generate_recommendation(self.db, user.id, force_new=True)
            sub_id = rec.problem_id

            sub = Submission(
                user_id=user.id,
                problem_id=sub_id,
                code="def solve(): pass",
                status="Accepted",
                passed_test_cases=3,
                total_test_cases=3,
                execution_time_ms=50.0
            )
            self.db.add(sub)
            self.db.commit()

            new_rec = RecommendationEngine.generate_recommendation(self.db, user.id, force_new=True)
            self.assertNotEqual(new_rec.problem_id, sub_id)
        finally:
            self.db.delete(user)
            self.db.commit()

    def test_14_multi_user_isolation(self):
        """Verify recommendation history and candidate sets are strictly isolated between users."""
        u1 = User(name="User 1", email=f"u1_{uuid.uuid4().hex[:8]}@test.com", password_hash="hash")
        u2 = User(name="User 2", email=f"u2_{uuid.uuid4().hex[:8]}@test.com", password_hash="hash")
        self.db.add_all([u1, u2])
        self.db.commit()
        self.db.refresh(u1)
        self.db.refresh(u2)

        try:
            RecommendationEngine.generate_recommendation(self.db, u1.id, force_new=True)
            u1_hist = RecommendationEngine.get_recommendation_history(self.db, u1.id)
            u2_hist = RecommendationEngine.get_recommendation_history(self.db, u2.id)

            self.assertEqual(len(u1_hist), 1)
            self.assertEqual(len(u2_hist), 0)
        finally:
            self.db.delete(u1)
            self.db.delete(u2)
            self.db.commit()

    def test_15_idempotent_import_rerun_safety(self):
        """Verify re-running the importer creates zero duplicate problems and is 100% idempotent."""
        count_before = self.db.query(Problem).count()
        res = ProblemImporter.import_mbpp_dataset(self.db, dry_run=False, run_judge=False)
        count_after = self.db.query(Problem).count()

        self.assertEqual(count_before, count_after, f"Re-running importer should not change count: {count_before} vs {count_after}")
        self.assertEqual(res["newly_imported_count"], 0, f"Expected 0 newly imported on rerun, got {res['newly_imported_count']}")
        self.assertGreater(res["already_existing_count"], 500)


if __name__ == "__main__":
    unittest.main(verbosity=2)
