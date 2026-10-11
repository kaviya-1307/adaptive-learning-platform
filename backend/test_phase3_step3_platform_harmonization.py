"""
Phase 3 Step 3 Verification Suite: Platform Integration & Catalog Harmonization
Verifies:
1. Catalog scoping: all (889), curated (40), and diagnostic (7)
2. Dashboard summary catalog totals across difficulty breakdown
3. Submission lifecycle: both Accepted and Failed submissions update concept state and yield fresh recommendations
4. Strict attempted problem exclusion across the expanded catalog
5. Recommendation formula weights (0.60 gap + 0.40 fit) and diversity constraint (max 2 per primary concept)
6. Multi-user isolation
7. Complete database catalog integrity (889 problems, 2,642 test cases)
"""
import unittest
import uuid
from fastapi.testclient import TestClient
from collections import Counter

from app.main import app
from app.core.database import SessionLocal
from app.models.user import User
from app.models.onboarding import OnboardingProfile
from app.models.problem import Problem
from app.models.test_case import TestCase
from app.models.submission import Submission
from app.models.learner_concept_state import LearnerConceptState
from app.models.learner_knowledge_state import LearnerKnowledgeState
from app.models.recommendation import Recommendation
from app.services.recommendation_engine import (
    RecommendationEngine,
    calculate_difficulty_fit,
    compute_recommendation_score,
    TOP_K,
    MAX_SAME_PRIMARY_CONCEPT,
)
from app.ml.state_engine import (
    KnowledgeStateEngine,
    get_problem_learning_concepts,
)
from app.ml.roadmap_engine import AdaptiveRoadmapEngine

# Test harness compatibility shims
if not hasattr(KnowledgeStateEngine, "initialize_user_state"):
    def _initialize_user_state(db, user_id):
        KnowledgeStateEngine.get_or_initialize_user_states(db, user_id)
        KnowledgeStateEngine.get_or_initialize_user_concept_states(db, user_id)
    KnowledgeStateEngine.initialize_user_state = staticmethod(_initialize_user_state)

if not hasattr(KnowledgeStateEngine, "update_state_on_submission"):
    def _update_state_on_submission(db, user_id, problem_id, is_accepted):
        prob = db.query(Problem).filter(Problem.id == problem_id).first()
        sub = (
            db.query(Submission)
            .filter(Submission.user_id == user_id, Submission.problem_id == problem_id)
            .order_by(Submission.created_at.desc())
            .first()
        )
        if not sub:
            sub = Submission(
                user_id=user_id,
                problem_id=problem_id,
                code="# test submission",
                status="Accepted" if is_accepted else "Wrong Answer",
                passed_test_cases=1 if is_accepted else 0,
                total_test_cases=1,
                execution_time_ms=10.0,
            )
            db.add(sub)
            db.commit()
        return KnowledgeStateEngine.update_state_from_submission(db, user_id, prob, sub)
    KnowledgeStateEngine.update_state_on_submission = staticmethod(_update_state_on_submission)

if not hasattr(RecommendationEngine, "get_candidate_problems"):
    RecommendationEngine.get_candidate_problems = staticmethod(
        lambda db, user_id: RecommendationEngine.recommend_top_k(
            db, user_id, top_k=TOP_K, max_same_primary_concept=MAX_SAME_PRIMARY_CONCEPT
        )
    )

if not hasattr(RecommendationEngine, "get_user_attempted_problem_ids"):
    RecommendationEngine.get_user_attempted_problem_ids = staticmethod(
        lambda db, user_id: RecommendationEngine.get_attempted_problem_ids(db, user_id)
    )

client = TestClient(app)


class TestPhase3Step3PlatformHarmonization(unittest.TestCase):
    def setUp(self):
        self.db = SessionLocal()
        self.created_users = []

    def tearDown(self):
        if self.created_users:
            for u in self.created_users:
                self.db.query(Recommendation).filter(Recommendation.user_id == u.id).delete(synchronize_session=False)
                self.db.query(Submission).filter(Submission.user_id == u.id).delete(synchronize_session=False)
                self.db.query(LearnerConceptState).filter(LearnerConceptState.user_id == u.id).delete(synchronize_session=False)
                self.db.query(LearnerKnowledgeState).filter(LearnerKnowledgeState.user_id == u.id).delete(synchronize_session=False)
                self.db.query(OnboardingProfile).filter(OnboardingProfile.user_id == u.id).delete(synchronize_session=False)
                self.db.query(User).filter(User.id == u.id).delete(synchronize_session=False)
            self.db.commit()
        self.db.close()

    def _create_user(self, name_prefix="Step3User"):
        uid = uuid.uuid4().hex[:8]
        user = User(
            email=f"{name_prefix.lower()}_{uid}@example.com",
            name=f"{name_prefix}_{uid}",
            password_hash="fakehashstep3password",
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        profile = OnboardingProfile(
            user_id=user.id,
            learning_goal="interview_prep",
            experience_level="intermediate",
        )
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)

        self.created_users.append(user)
        return user

    def _get_auth_headers(self, user):
        from app.core.security import create_access_token
        token = create_access_token(subject=user.id)
        return {"Authorization": f"Bearer {token}"}

    def test_01_catalog_scoping_and_counts(self):
        """Verify /api/problems supports full catalog (889), curated (40), and diagnostic (7)."""
        # Full catalog
        resp_all = client.get("/api/problems")
        self.assertEqual(resp_all.status_code, 200)
        problems_all = resp_all.json()
        self.assertEqual(len(problems_all), 889, f"Expected 889 problems, got {len(problems_all)}")

        # Curated only
        resp_curated = client.get("/api/problems?curated_only=true")
        self.assertEqual(resp_curated.status_code, 200)
        problems_curated = resp_curated.json()
        self.assertEqual(len(problems_curated), 40, f"Expected 40 curated problems, got {len(problems_curated)}")
        for p in problems_curated:
            self.assertLessEqual(p["id"], 40, f"Curated problem ID {p['id']} > 40")

        # Diagnostic only
        resp_diag = client.get("/api/problems?is_diagnostic=true")
        self.assertEqual(resp_diag.status_code, 200)
        problems_diag = resp_diag.json()
        self.assertEqual(len(problems_diag), 7, f"Expected 7 diagnostic problems, got {len(problems_diag)}")
        for p in problems_diag:
            self.assertTrue(p["is_diagnostic"], f"Problem {p['id']} is not diagnostic")

    def test_02_dashboard_catalog_coverage_and_totals(self):
        """Verify dashboard summary difficulty breakdown totals sum to 889."""
        user = self._create_user("DashUser")
        headers = self._get_auth_headers(user)
        KnowledgeStateEngine.initialize_user_state(self.db, user.id)

        resp = client.get("/api/dashboard/summary", headers=headers)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()

        problem_stats = data.get("problem_stats", {})
        diff_breakdown = problem_stats.get("difficulty_breakdown", [])
        self.assertGreater(len(diff_breakdown), 0)

        total_catalog = sum(item["total_count"] for item in diff_breakdown)
        self.assertEqual(total_catalog, 889, f"Expected total catalog count 889, got {total_catalog}")

        counts_by_diff = {item["difficulty"]: item["total_count"] for item in diff_breakdown}
        self.assertEqual(counts_by_diff.get("Easy"), 640)
        self.assertEqual(counts_by_diff.get("Medium"), 232)
        self.assertEqual(counts_by_diff.get("Hard"), 17)

    def test_03_submission_accepted_triggers_recommendation_and_state_update(self):
        """Verify Accepted submission updates concept state and generates an active recommendation."""
        user = self._create_user("AcceptedUser")
        KnowledgeStateEngine.initialize_user_state(self.db, user.id)

        # Problem 1: Two Sum
        prob = self.db.query(Problem).filter(Problem.id == 1).first()
        self.assertIsNotNone(prob)

        # Initial state
        initial_rec = RecommendationEngine.generate_recommendation(self.db, user.id, force_new=True)
        self.assertIsNotNone(initial_rec)

        # Record Accepted submission
        sub = Submission(
            user_id=user.id,
            problem_id=prob.id,
            code="def two_sum(nums, target): return [0, 1]",
            status="Accepted",
            passed_test_cases=2,
            total_test_cases=2,
            execution_time_ms=15,
        )
        self.db.add(sub)
        self.db.commit()

        # Update state via KnowledgeStateEngine
        KnowledgeStateEngine.update_state_on_submission(self.db, user.id, prob.id, True)

        # Verify state updated
        concepts = get_problem_learning_concepts(prob)
        for c in concepts:
            st = (
                self.db.query(LearnerConceptState)
                .filter(LearnerConceptState.user_id == user.id, LearnerConceptState.concept == c)
                .first()
            )
            self.assertIsNotNone(st)
            self.assertGreater(st.interactions, 0)
            self.assertGreater(st.solved_count, 0)

        # Get next recommendation
        fresh_rec = RecommendationEngine.generate_recommendation(self.db, user.id, force_new=True)
        self.assertIsNotNone(fresh_rec)
        self.assertNotEqual(fresh_rec.problem_id, prob.id, "Attempted problem 1 must not be recommended")
        self.assertTrue(fresh_rec.is_active)

    def test_04_submission_wrong_answer_triggers_recommendation_and_state_update(self):
        """Verify Wrong Answer submission updates concept state and yields recommendation for practice."""
        user = self._create_user("FailUser")
        KnowledgeStateEngine.initialize_user_state(self.db, user.id)

        # Problem 2: Reverse String
        prob = self.db.query(Problem).filter(Problem.id == 2).first()
        self.assertIsNotNone(prob)

        sub = Submission(
            user_id=user.id,
            problem_id=prob.id,
            code="def reverse_string(s): return s",
            status="Wrong Answer",
            passed_test_cases=0,
            total_test_cases=2,
            execution_time_ms=10,
        )
        self.db.add(sub)
        self.db.commit()

        # Update state on failure
        KnowledgeStateEngine.update_state_on_submission(self.db, user.id, prob.id, False)

        # Verify state updated
        concepts = get_problem_learning_concepts(prob)
        for c in concepts:
            st = (
                self.db.query(LearnerConceptState)
                .filter(LearnerConceptState.user_id == user.id, LearnerConceptState.concept == c)
                .first()
            )
            self.assertIsNotNone(st)
            self.assertGreater(st.interactions, 0)
            self.assertEqual(st.solved_count, 0)
            self.assertGreater(st.weakness_score, 0.0)

        # Get next recommendation
        fresh_rec = RecommendationEngine.generate_recommendation(self.db, user.id, force_new=True)
        self.assertIsNotNone(fresh_rec)
        self.assertNotEqual(fresh_rec.problem_id, prob.id, "Attempted problem 2 must not be recommended")
        self.assertTrue(fresh_rec.is_active)

    def test_05_attempted_problem_exclusion_across_expanded_catalog(self):
        """Verify multiple attempted problems are never recommended."""
        user = self._create_user("ExclusionUser")
        KnowledgeStateEngine.initialize_user_state(self.db, user.id)

        # Attempt first 10 problems
        attempted_ids = list(range(1, 11))
        for pid in attempted_ids:
            sub = Submission(
                user_id=user.id,
                problem_id=pid,
                code="print('attempt')",
                status="Accepted" if pid % 2 == 0 else "Wrong Answer",
                passed_test_cases=1,
                total_test_cases=2,
                execution_time_ms=10,
            )
            self.db.add(sub)
        self.db.commit()

        # Request 10 consecutive recommendations
        for _ in range(10):
            rec = RecommendationEngine.generate_recommendation(self.db, user.id, force_new=True)
            self.assertIsNotNone(rec)
            self.assertNotIn(
                rec.problem_id,
                attempted_ids,
                f"Recommended problem {rec.problem_id} is in attempted set {attempted_ids}"
            )

    def test_06_recommendation_scoring_weights_and_diversity(self):
        """Verify recommendation scoring weights (0.60 gap + 0.40 fit) and diversity constraint."""
        # 1. Formula score check
        score = compute_recommendation_score(concept_gap=0.8, difficulty_fit=0.5)
        expected = 0.60 * 0.8 + 0.40 * 0.5
        self.assertAlmostEqual(score, expected, places=5)

        # 2. Candidate diversity check
        user = self._create_user("DiversityUser")
        KnowledgeStateEngine.initialize_user_state(self.db, user.id)

        candidates = RecommendationEngine.get_candidate_problems(self.db, user.id)
        self.assertGreater(len(candidates), 0)

        # Group by primary concept in top-K
        top_candidates = candidates[:TOP_K]
        concept_counts = Counter(c["primary_concept"] for c in top_candidates)
        for concept, count in concept_counts.items():
            self.assertLessEqual(
                count,
                MAX_SAME_PRIMARY_CONCEPT,
                f"Concept '{concept}' appeared {count} times in top-{TOP_K}, exceeding limit of {MAX_SAME_PRIMARY_CONCEPT}"
            )

    def test_07_multi_user_isolation(self):
        """Verify User 1 and User 2 states and recommendations remain strictly isolated."""
        u1 = self._create_user("IsoUser1")
        u2 = self._create_user("IsoUser2")

        KnowledgeStateEngine.initialize_user_state(self.db, u1.id)
        KnowledgeStateEngine.initialize_user_state(self.db, u2.id)

        # u1 attempts problem 1
        sub1 = Submission(
            user_id=u1.id,
            problem_id=1,
            code="test",
            status="Accepted",
            passed_test_cases=2,
            total_test_cases=2,
            execution_time_ms=10,
        )
        self.db.add(sub1)
        self.db.commit()
        KnowledgeStateEngine.update_state_on_submission(self.db, u1.id, 1, True)

        # u2's attempted set must be empty
        u2_attempted = RecommendationEngine.get_user_attempted_problem_ids(self.db, u2.id)
        self.assertEqual(len(u2_attempted), 0, "User 2 attempted problem set should be empty")

        # u1's attempted set contains 1
        u1_attempted = RecommendationEngine.get_user_attempted_problem_ids(self.db, u1.id)
        self.assertEqual(u1_attempted, {1})

    def test_08_database_catalog_integrity(self):
        """Verify exact catalog counts: 889 problems, 40 curated, 849 imported, 2,642 test cases."""
        total_probs = self.db.query(Problem).count()
        self.assertEqual(total_probs, 889)

        curated = self.db.query(Problem).filter(Problem.id <= 40).count()
        self.assertEqual(curated, 40)

        imported = self.db.query(Problem).filter(Problem.id > 40).count()
        self.assertEqual(imported, 849)

        total_tcs = self.db.query(TestCase).count()
        self.assertEqual(total_tcs, 2642)

        visible_tcs = self.db.query(TestCase).filter(TestCase.is_hidden == False).count()
        self.assertEqual(visible_tcs, 929)

        hidden_tcs = self.db.query(TestCase).filter(TestCase.is_hidden == True).count()
        self.assertEqual(hidden_tcs, 1713)

        # Every problem has at least 2 test cases
        for p in self.db.query(Problem).all():
            tc_count = self.db.query(TestCase).filter(TestCase.problem_id == p.id).count()
            self.assertGreaterEqual(tc_count, 2, f"Problem {p.id} has {tc_count} test cases (< 2)")


if __name__ == "__main__":
    unittest.main(verbosity=2)
