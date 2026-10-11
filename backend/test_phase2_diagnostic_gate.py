"""
Phase 2 Verification Suite: One-Time Diagnostic Enforcement.
Covers the core criteria:
1. New public registration initializes diagnostic_completed=False, diagnostic_exempt=False.
2. New user is blocked from learning endpoints (dashboard, recommendations, submission) with 403 Forbidden.
3. Diagnostic code execution is allowed for diagnostic problems during assessment.
4. Partial diagnostic attempts (1 or more) do NOT bypass the gate (Attempt != Completion).
5. POST /api/diagnostic/complete sets permanent diagnostic completion state in database.
6. Once completed, learning endpoints (dashboard, recommendations) return 200 OK.
7. Retake prevention on POST /api/diagnostic/submit (returns 400 Bad Request).
8. Retake prevention on POST /api/diagnostic/complete (returns 400 Bad Request).
9. Restart prevention on GET /api/diagnostic/problems (returns 400 Bad Request).
10. Existing baseline users (diagnostic_exempt=True) access the platform normally without retaking.
11. Admin users are exempt from the diagnostic gate.
"""
import unittest
import uuid
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import SessionLocal
from app.core.security import get_password_hash, create_access_token
from app.models.user import User, UserRole
from app.models.problem import Problem
from app.models.onboarding import OnboardingProfile
from app.models.diagnostic_attempt import DiagnosticAttempt
from app.models.recommendation import Recommendation
from app.models.submission import Submission
from app.models.learner_concept_state import LearnerConceptState
from app.models.learner_knowledge_state import LearnerKnowledgeState
from app.ml.state_engine import KnowledgeStateEngine

client = TestClient(app)


class TestPhase2DiagnosticGate(unittest.TestCase):
    def setUp(self):
        self.db = SessionLocal()
        self.created_users = []

    def tearDown(self):
        self.db.rollback()
        if self.created_users:
            for u in self.created_users:
                self.db.query(Recommendation).filter(Recommendation.user_id == u.id).delete(synchronize_session=False)
                self.db.query(Submission).filter(Submission.user_id == u.id).delete(synchronize_session=False)
                self.db.query(DiagnosticAttempt).filter(DiagnosticAttempt.user_id == u.id).delete(synchronize_session=False)
                self.db.query(LearnerConceptState).filter(LearnerConceptState.user_id == u.id).delete(synchronize_session=False)
                self.db.query(LearnerKnowledgeState).filter(LearnerKnowledgeState.user_id == u.id).delete(synchronize_session=False)
                self.db.query(OnboardingProfile).filter(OnboardingProfile.user_id == u.id).delete(synchronize_session=False)
                self.db.query(User).filter(User.id == u.id).delete(synchronize_session=False)
            self.db.commit()
        self.db.close()

    def _register_student(self, name_prefix="diag_gate"):
        uid = uuid.uuid4().hex[:8]
        res = client.post("/api/auth/register", json={
            "name": f"{name_prefix}_{uid}",
            "email": f"{name_prefix}_{uid}@test.com",
            "password": "Password123!"
        })
        self.assertEqual(res.status_code, 201)
        data = res.json()
        user_id = data["user"]["id"]
        token = data["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        db_user = self.db.query(User).filter(User.id == user_id).first()
        self.created_users.append(db_user)
        return db_user, token, headers

    def test_01_new_registration_diagnostic_state(self):
        """1. New public registration initializes diagnostic_completed=False, diagnostic_exempt=False."""
        user, token, headers = self._register_student("reg_state")
        self.assertFalse(user.diagnostic_completed)
        self.assertFalse(user.diagnostic_exempt)
        self.assertIsNone(user.diagnostic_score)
        self.assertIsNone(user.diagnostic_total)
        self.assertIsNone(user.diagnostic_completed_at)

        # GET /api/auth/me reflects status
        me_res = client.get("/api/auth/me", headers=headers)
        self.assertEqual(me_res.status_code, 200)
        me_data = me_res.json()
        self.assertFalse(me_data["diagnostic_completed"])
        self.assertFalse(me_data["diagnostic_exempt"])

        # GET /api/diagnostic/status reflects status
        status_res = client.get("/api/diagnostic/status", headers=headers)
        self.assertEqual(status_res.status_code, 200)
        s_data = status_res.json()
        self.assertFalse(s_data["diagnostic_completed"])
        self.assertTrue(s_data["can_take_diagnostic"])

    def test_02_new_user_blocked_from_learning_endpoints(self):
        """2. New user is blocked from learning endpoints (dashboard, recommendations, submit) with 403."""
        user, token, headers = self._register_student("blocked_user")

        # Dashboard summary blocked
        d_res = client.get("/api/dashboard/summary", headers=headers)
        self.assertEqual(d_res.status_code, 403)
        self.assertIn("Diagnostic assessment required", d_res.json().get("detail", ""))

        # Recommendations blocked
        r_res = client.get("/api/recommendations/next", headers=headers)
        self.assertEqual(r_res.status_code, 403)
        self.assertIn("Diagnostic assessment required", r_res.json().get("detail", ""))

        # Submissions submit blocked
        s_res = client.post("/api/submissions/submit", headers=headers, json={
            "problem_id": 1,
            "code": "def solution(): return 42"
        })
        self.assertEqual(s_res.status_code, 403)
        self.assertIn("Diagnostic assessment required", s_res.json().get("detail", ""))

        # Submissions run for NON-diagnostic problem blocked
        non_diag_prob = self.db.query(Problem).filter(Problem.is_diagnostic == False).first()
        self.assertIsNotNone(non_diag_prob)
        run_res = client.post("/api/submissions/run", headers=headers, json={
            "problem_id": non_diag_prob.id,
            "code": "def solution(): return 42"
        })
        self.assertEqual(run_res.status_code, 403)

    def test_03_diagnostic_execution_allowed_during_assessment(self):
        """3. Diagnostic problems list and running code for diagnostic problems is allowed."""
        user, token, headers = self._register_student("diag_flow")

        # Can fetch diagnostic problems
        p_res = client.get("/api/diagnostic/problems", headers=headers)
        self.assertEqual(p_res.status_code, 200)
        probs = p_res.json()
        self.assertGreaterEqual(len(probs), 6)

        # Can run code for a diagnostic problem
        diag_prob_id = probs[0]["id"]
        run_res = client.post("/api/submissions/run", headers=headers, json={
            "problem_id": diag_prob_id,
            "code": "# Python code\nprint('testing diagnostic')"
        })
        self.assertEqual(run_res.status_code, 200)

    def test_04_partial_attempts_do_not_bypass_gate(self):
        """4. Partial diagnostic attempts (1 or more) do NOT bypass the gate (Attempt != Completion)."""
        user, token, headers = self._register_student("partial_att")
        diag_probs = client.get("/api/diagnostic/problems", headers=headers).json()

        # Submit 1st attempt
        att1 = client.post("/api/diagnostic/submit", headers=headers, json={
            "problem_id": diag_probs[0]["id"],
            "is_solved": True,
            "time_spent_seconds": 45,
            "code_submitted": "print('solved 1')"
        })
        self.assertEqual(att1.status_code, 200)

        # Submit 2nd attempt
        att2 = client.post("/api/diagnostic/submit", headers=headers, json={
            "problem_id": diag_probs[1]["id"],
            "is_solved": True,
            "time_spent_seconds": 60,
            "code_submitted": "print('solved 2')"
        })
        self.assertEqual(att2.status_code, 200)

        # Confirm attempts exist in DB (commit/rollback current session to see committed rows from endpoint)
        self.db.rollback()
        attempts_count = self.db.query(DiagnosticAttempt).filter(DiagnosticAttempt.user_id == user.id).count()
        self.assertEqual(attempts_count, 2)

        # CRITICAL CHECK: User has NOT completed diagnostic -> Dashboard still returns 403 Forbidden!
        d_res = client.get("/api/dashboard/summary", headers=headers)
        self.assertEqual(d_res.status_code, 403, "Partial diagnostic attempts must NOT grant access to dashboard!")

        # Recommendations still returns 403 Forbidden!
        r_res = client.get("/api/recommendations/next", headers=headers)
        self.assertEqual(r_res.status_code, 403, "Partial diagnostic attempts must NOT grant access to recommendations!")

    def test_05_complete_diagnostic_sets_permanent_state(self):
        """5. POST /api/diagnostic/complete sets permanent diagnostic completion state in DB."""
        user, token, headers = self._register_student("complete_state")
        diag_probs = client.get("/api/diagnostic/problems", headers=headers).json()

        # Submit one solved attempt
        client.post("/api/diagnostic/submit", headers=headers, json={
            "problem_id": diag_probs[0]["id"],
            "is_solved": True,
            "time_spent_seconds": 30
        })

        # Complete diagnostic
        comp_res = client.post("/api/diagnostic/complete", headers=headers)
        self.assertEqual(comp_res.status_code, 200)
        comp_data = comp_res.json()
        self.assertEqual(comp_data["solved_count"], 1)
        self.assertEqual(comp_data["total_problems"], len(diag_probs))

        # Check DB directly (rollback session to see new committed transaction from endpoint)
        self.db.rollback()
        fresh_user = self.db.query(User).filter(User.id == user.id).first()
        self.assertTrue(fresh_user.diagnostic_completed)
        self.assertEqual(fresh_user.diagnostic_score, 1)
        self.assertEqual(fresh_user.diagnostic_total, len(diag_probs))
        self.assertIsNotNone(fresh_user.diagnostic_completed_at)

        # GET /api/auth/me shows diagnostic_completed=True
        me_res = client.get("/api/auth/me", headers=headers)
        self.assertEqual(me_res.status_code, 200)
        self.assertTrue(me_res.json()["diagnostic_completed"])
        self.assertEqual(me_res.json()["diagnostic_score"], 1)

    def test_06_completed_user_can_access_learning_endpoints(self):
        """6. Once completed, learning endpoints (dashboard, recommendations) return 200 OK."""
        user, token, headers = self._register_student("completed_learner")
        diag_probs = client.get("/api/diagnostic/problems", headers=headers).json()

        # Submit and complete
        client.post("/api/diagnostic/submit", headers=headers, json={
            "problem_id": diag_probs[0]["id"],
            "is_solved": True,
            "time_spent_seconds": 25
        })
        client.post("/api/diagnostic/complete", headers=headers)

        # Dashboard now returns 200 OK!
        d_res = client.get("/api/dashboard/summary", headers=headers)
        self.assertEqual(d_res.status_code, 200)
        self.assertIn("learning_state", d_res.json())

        # Recommendations now returns 200 OK!
        r_res = client.get("/api/recommendations/next", headers=headers)
        self.assertEqual(r_res.status_code, 200)
        self.assertIn("problem_id", r_res.json())

    def test_07_retake_prevention_submit(self):
        """7. Retake prevention on POST /api/diagnostic/submit (returns 400 Bad Request)."""
        user, token, headers = self._register_student("retake_submit")
        diag_probs = client.get("/api/diagnostic/problems", headers=headers).json()
        client.post("/api/diagnostic/complete", headers=headers)

        # Attempt to submit after completion
        sub_res = client.post("/api/diagnostic/submit", headers=headers, json={
            "problem_id": diag_probs[0]["id"],
            "is_solved": True,
            "time_spent_seconds": 10
        })
        self.assertEqual(sub_res.status_code, 400)
        self.assertIn("already been completed", sub_res.json().get("detail", ""))

    def test_08_retake_prevention_complete(self):
        """8. Retake prevention on POST /api/diagnostic/complete (returns 400 Bad Request)."""
        user, token, headers = self._register_student("retake_comp")
        client.post("/api/diagnostic/complete", headers=headers)

        # Attempt to complete again
        comp2_res = client.post("/api/diagnostic/complete", headers=headers)
        self.assertEqual(comp2_res.status_code, 400)
        self.assertIn("already been completed", comp2_res.json().get("detail", ""))

    def test_09_retake_prevention_restart_problems(self):
        """9. Restart prevention on GET /api/diagnostic/problems (returns 400 Bad Request)."""
        user, token, headers = self._register_student("restart_prob")
        client.post("/api/diagnostic/complete", headers=headers)

        # Attempt to fetch diagnostic problems again with completed user
        prob_res = client.get("/api/diagnostic/problems", headers=headers)
        self.assertEqual(prob_res.status_code, 400)
        self.assertIn("already been completed", prob_res.json().get("detail", ""))

    def test_10_existing_users_are_exempt_and_access_normally(self):
        """10. Existing baseline users (diagnostic_exempt=True) access the platform normally."""
        # Find an existing baseline user from ID <= 297 with an onboarding profile
        legacy_user = self.db.query(User).filter(User.id <= 297, User.diagnostic_exempt == True).first()
        self.assertIsNotNone(legacy_user)
        self.assertTrue(legacy_user.diagnostic_exempt)

        token = create_access_token(subject=legacy_user.id, role=legacy_user.role)
        headers = {"Authorization": f"Bearer {token}"}

        # Dashboard accessible without completing diagnostic
        d_res = client.get("/api/dashboard/summary", headers=headers)
        self.assertEqual(d_res.status_code, 200)

        # GET /api/auth/me shows diagnostic_exempt=True
        me_res = client.get("/api/auth/me", headers=headers)
        self.assertEqual(me_res.status_code, 200)
        self.assertTrue(me_res.json()["diagnostic_exempt"])

    def test_11_admin_user_is_exempt(self):
        """11. Admin user is exempt from the diagnostic gate."""
        uid = uuid.uuid4().hex[:8]
        admin = User(
            name=f"Admin {uid}",
            email=f"admin_{uid}@test.com",
            password_hash=get_password_hash("Password123!"),
            role=UserRole.ADMIN,
            diagnostic_completed=False,
            diagnostic_exempt=False
        )
        self.db.add(admin)
        self.db.commit()
        self.db.refresh(admin)
        self.created_users.append(admin)

        token = create_access_token(subject=admin.id, role=admin.role)
        headers = {"Authorization": f"Bearer {token}"}

        # Admin can access dashboard even with diagnostic_completed=False and diagnostic_exempt=False
        d_res = client.get("/api/dashboard/summary", headers=headers)
        self.assertEqual(d_res.status_code, 200)


if __name__ == "__main__":
    unittest.main(verbosity=2)
