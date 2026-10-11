"""
Phase 1 Verification Suite: Authentication & RBAC Foundation.
Covers the 10 required test criteria:
1. New public registration creates STUDENT.
2. Client cannot create ADMIN through registration (even with malicious payload).
3. Existing users remain present in database.
4. Existing passwords/login still work.
5. Current-user endpoint (/api/auth/me) exposes role.
6. STUDENT can access student functionality (/api/problems, /api/dashboard/summary).
7. STUDENT receives 403 Forbidden on admin endpoint (/api/admin/status).
8. ADMIN receives 200 OK on admin endpoint (/api/admin/status).
9. Unauthenticated request receives 401 Unauthorized on admin endpoint.
10. Existing recommendation/knowledge-state functionality is unchanged.
"""
import unittest
import uuid
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import SessionLocal
from app.core.security import get_password_hash, create_access_token
from app.models.user import User, UserRole
from app.models.onboarding import OnboardingProfile
from app.models.recommendation import Recommendation
from app.models.submission import Submission
from app.models.learner_concept_state import LearnerConceptState
from app.models.learner_knowledge_state import LearnerKnowledgeState
from app.services.recommendation_engine import RecommendationEngine

client = TestClient(app)


class TestPhase1RBACFoundation(unittest.TestCase):
    def setUp(self):
        self.db = SessionLocal()
        self.created_users = []

    def tearDown(self):
        self.db.rollback()
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

    def _create_test_user(self, role="STUDENT", prefix="rbac_user"):
        uid = uuid.uuid4().hex[:8]
        user = User(
            name=f"Test {prefix}_{uid}",
            email=f"{prefix}_{uid}@example.com",
            password_hash=get_password_hash("Password123!"),
            role=role
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        self.created_users.append(user)
        return user

    def test_01_public_registration_creates_student(self):
        """1. New public registration creates STUDENT."""
        uid = uuid.uuid4().hex[:8]
        res = client.post("/api/auth/register", json={
            "name": f"New Student {uid}",
            "email": f"student_{uid}@example.com",
            "password": "Password123!"
        })
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertIn("user", data)
        self.assertEqual(data["user"]["role"], "STUDENT")

        # Verify DB directly
        db_user = self.db.query(User).filter(User.id == data["user"]["id"]).first()
        self.assertIsNotNone(db_user)
        self.assertEqual(db_user.role, "STUDENT")
        self.created_users.append(db_user)

    def test_02_client_cannot_create_admin_through_registration(self):
        """2. Client cannot create ADMIN through registration, even with injected role parameter."""
        uid = uuid.uuid4().hex[:8]
        res = client.post("/api/auth/register", json={
            "name": f"Hacker Attempt {uid}",
            "email": f"hacker_{uid}@example.com",
            "password": "Password123!",
            "role": "ADMIN"  # Malicious attempt to self-promote to ADMIN
        })
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertEqual(data["user"]["role"], "STUDENT", "Registration must NOT honor requested ADMIN role")

        db_user = self.db.query(User).filter(User.id == data["user"]["id"]).first()
        self.assertIsNotNone(db_user)
        self.assertEqual(db_user.role, "STUDENT")
        self.created_users.append(db_user)

    def test_03_existing_users_remain_present_with_valid_roles(self):
        """3. Existing users remain present and all have valid STUDENT role."""
        total_users = self.db.query(User).count()
        self.assertGreaterEqual(total_users, 227, f"Expected at least 227 users, found {total_users}")

        # Verify no users have NULL or invalid role
        invalid_roles = self.db.query(User).filter(~User.role.in_([UserRole.STUDENT, UserRole.ADMIN])).all()
        self.assertEqual(len(invalid_roles), 0, f"Found users with invalid roles: {invalid_roles}")

    def test_04_existing_passwords_and_login_still_work(self):
        """4. Existing passwords/login still work and issue valid access tokens with role."""
        user = self._create_test_user(role="STUDENT", prefix="login_tester")
        res = client.post("/api/auth/login", json={
            "email": user.email,
            "password": "Password123!"
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("access_token", data)
        self.assertEqual(data["user"]["role"], "STUDENT")

    def test_05_current_user_endpoint_exposes_role(self):
        """5. Current-user endpoint (/api/auth/me) exposes role alongside existing fields."""
        user = self._create_test_user(role="STUDENT", prefix="me_tester")
        token = create_access_token(subject=user.id, role=user.role)

        res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["id"], user.id)
        self.assertEqual(data["email"], user.email)
        self.assertEqual(data["name"], user.name)
        self.assertEqual(data["role"], "STUDENT")
        self.assertIn("onboarding_completed", data)
        self.assertIn("learning_goal", data)
        self.assertIn("experience_level", data)

    def test_06_student_can_access_student_functionality(self):
        """6. STUDENT can access student functionality (problems, dashboard)."""
        student = self._create_test_user(role="STUDENT", prefix="student_feat")
        token = create_access_token(subject=student.id, role=student.role)
        headers = {"Authorization": f"Bearer {token}"}

        # Can access problems
        p_res = client.get("/api/problems?limit=5", headers=headers)
        self.assertEqual(p_res.status_code, 200)

        # Can access dashboard summary
        d_res = client.get("/api/dashboard/summary", headers=headers)
        self.assertEqual(d_res.status_code, 200)

    def test_07_student_receives_403_on_admin_endpoint(self):
        """7. STUDENT receives 403 Forbidden on admin endpoint (/api/admin/status)."""
        student = self._create_test_user(role="STUDENT", prefix="student_forbidden")
        token = create_access_token(subject=student.id, role=student.role)
        headers = {"Authorization": f"Bearer {token}"}

        res = client.get("/api/admin/status", headers=headers)
        self.assertEqual(res.status_code, 403)
        self.assertIn("Admin privileges required", res.json().get("detail", ""))

    def test_08_admin_receives_success_on_admin_endpoint(self):
        """8. ADMIN receives success on admin endpoint (/api/admin/status)."""
        admin = self._create_test_user(role="ADMIN", prefix="admin_allowed")
        token = create_access_token(subject=admin.id, role=admin.role)
        headers = {"Authorization": f"Bearer {token}"}

        res = client.get("/api/admin/status", headers=headers)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["role"], "ADMIN")
        self.assertEqual(data["admin_email"], admin.email)

    def test_09_unauthenticated_request_cannot_access_admin_endpoint(self):
        """9. Unauthenticated request cannot access admin endpoint (401 Unauthorized)."""
        res = client.get("/api/admin/status")
        self.assertEqual(res.status_code, 401)

    def test_10_existing_recommendation_and_knowledge_state_unchanged(self):
        """10. Existing recommendation/knowledge-state functionality is unchanged."""
        student = self._create_test_user(role="STUDENT", prefix="rec_unchanged")
        token = create_access_token(subject=student.id, role=student.role)
        headers = {"Authorization": f"Bearer {token}"}

        # Knowledge state endpoint functions
        k_res = client.get("/api/knowledge-state", headers=headers)
        self.assertEqual(k_res.status_code, 200)
        k_data = k_res.json()
        self.assertIn("topics", k_data)
        self.assertEqual(len(k_data["topics"]), 10)

        # Recommendation endpoints function as expected
        r_gen_res = client.post("/api/recommendations/generate", headers=headers)
        self.assertEqual(r_gen_res.status_code, 200)
        gen_data = r_gen_res.json()
        self.assertIn("problem_id", gen_data)
        self.assertIn("explanation_text", gen_data)
        self.assertTrue(gen_data["is_active"])

        # Active recommendation endpoint functions
        r_res = client.get("/api/recommendations/next", headers=headers)
        self.assertEqual(r_res.status_code, 200)
        rec_data = r_res.json()
        self.assertEqual(rec_data["problem_id"], gen_data["problem_id"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
