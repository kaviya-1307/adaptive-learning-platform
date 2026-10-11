"""
Phase 5 Verification Suite: Live Student Dataset & Admin-Only Performance Monitoring.
Covers all 15 core verification scenarios:
1. test_01_student_blocked_from_admin_overview (403 Forbidden)
2. test_02_student_blocked_from_admin_users_list (403 Forbidden)
3. test_03_student_blocked_from_admin_user_detail (403 Forbidden)
4. test_04_student_blocked_from_admin_export (403 Forbidden)
5. test_05_unauthenticated_request_rejected_on_admin_endpoints (401 Unauthorized)
6. test_06_admin_can_access_admin_overview (200 OK with valid metrics)
7. test_07_admin_can_access_admin_users_list (200 OK with sanitized student list)
8. test_08_admin_users_list_never_exposes_password_hash
9. test_09_admin_users_list_never_exposes_raw_source_code
10. test_10_admin_can_inspect_single_student_detail (200 OK with mastery, diagnostic, and submissions)
11. test_11_admin_export_produces_sanitized_live_dataset_json_and_csv
12. test_12_live_student_lifecycle_and_activity_persistence (Complete 13-step lifecycle test)
13. test_13_student_isolation_strictly_preserved (Student A cannot access Student B's records)
14. test_14_public_registration_cannot_create_admin (Role injection prevented)
15. test_15_phases_1_to_4_regressions_zero (Regression check)
"""
import unittest
import uuid
from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.main import app
from app.core.database import SessionLocal
from app.core.security import get_password_hash, create_access_token
from app.models.user import User, UserRole
from app.models.problem import Problem
from app.models.diagnostic_attempt import DiagnosticAttempt
from app.models.submission import Submission
from app.models.recommendation import Recommendation
from app.models.learner_concept_state import LearnerConceptState
from app.models.learner_knowledge_state import LearnerKnowledgeState
from app.models.onboarding import OnboardingProfile

client = TestClient(app)


class TestPhase5AdminMonitoring(unittest.TestCase):
    def setUp(self):
        self.db = SessionLocal()
        self.created_users = []

    def tearDown(self):
        self.db.rollback()
        if self.created_users:
            user_ids = [u.id for u in self.created_users if u is not None and getattr(u, 'id', None) is not None]
            if user_ids:
                id_list = ",".join(str(i) for i in user_ids)
                self.db.execute(text(f"DELETE FROM recommendations WHERE user_id IN ({id_list})"))
                self.db.execute(text(f"DELETE FROM submissions WHERE user_id IN ({id_list})"))
                self.db.execute(text(f"DELETE FROM diagnostic_attempts WHERE user_id IN ({id_list})"))
                self.db.execute(text(f"DELETE FROM learner_concept_states WHERE user_id IN ({id_list})"))
                self.db.execute(text(f"DELETE FROM learner_knowledge_state WHERE user_id IN ({id_list})"))
                self.db.execute(text(f"DELETE FROM onboarding_profiles WHERE user_id IN ({id_list})"))
                self.db.execute(text(f"DELETE FROM users WHERE id IN ({id_list})"))
                self.db.commit()
        self.db.close()

    def _register_student(self, name_prefix="p5_student"):
        uid = uuid.uuid4().hex[:8]
        raw_password = "Password123!"
        res = client.post("/api/auth/register", json={
            "name": f"{name_prefix}_{uid}",
            "email": f"{name_prefix}_{uid}@test.com",
            "password": raw_password
        })
        self.assertEqual(res.status_code, 201)
        data = res.json()
        user_id = data["user"]["id"]
        token = data["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        db_user = self.db.query(User).filter(User.id == user_id).first()
        if db_user:
            self.created_users.append(db_user)
        return db_user, raw_password, token, headers

    def _create_admin(self):
        uid = uuid.uuid4().hex[:8]
        raw_pwd = "AdminSecurePass123!"
        admin = User(
            name=f"Admin_{uid}",
            email=f"admin_{uid}@test.com",
            password_hash=get_password_hash(raw_pwd),
            role=UserRole.ADMIN,
            diagnostic_completed=True,
            diagnostic_exempt=True
        )
        self.db.add(admin)
        self.db.commit()
        self.db.refresh(admin)
        self.created_users.append(admin)
        token = create_access_token(subject=str(admin.id), role=admin.role)
        headers = {"Authorization": f"Bearer {token}"}
        return admin, raw_pwd, token, headers

    # -------------------------------------------------------------------------
    # 1. Student blocked from admin overview (403)
    # -------------------------------------------------------------------------
    def test_01_student_blocked_from_admin_overview(self):
        """1. Authenticated STUDENT receives 403 Forbidden on GET /api/admin/overview."""
        student, pwd, token, headers = self._register_student("p5_t1")
        res = client.get("/api/admin/overview", headers=headers)
        self.assertEqual(res.status_code, 403)
        self.assertIn("Admin privileges required", res.json().get("detail", ""))

    # -------------------------------------------------------------------------
    # 2. Student blocked from admin users list (403)
    # -------------------------------------------------------------------------
    def test_02_student_blocked_from_admin_users_list(self):
        """2. Authenticated STUDENT receives 403 Forbidden on GET /api/admin/users."""
        student, pwd, token, headers = self._register_student("p5_t2")
        res = client.get("/api/admin/users", headers=headers)
        self.assertEqual(res.status_code, 403)
        self.assertIn("Admin privileges required", res.json().get("detail", ""))

    # -------------------------------------------------------------------------
    # 3. Student blocked from admin user detail (403)
    # -------------------------------------------------------------------------
    def test_03_student_blocked_from_admin_user_detail(self):
        """3. Authenticated STUDENT receives 403 Forbidden on GET /api/admin/users/{user_id}."""
        student, pwd, token, headers = self._register_student("p5_t3")
        res = client.get(f"/api/admin/users/{student.id}", headers=headers)
        self.assertEqual(res.status_code, 403)
        self.assertIn("Admin privileges required", res.json().get("detail", ""))

    # -------------------------------------------------------------------------
    # 4. Student blocked from admin export (403)
    # -------------------------------------------------------------------------
    def test_04_student_blocked_from_admin_export(self):
        """4. Authenticated STUDENT receives 403 Forbidden on GET /api/admin/export."""
        student, pwd, token, headers = self._register_student("p5_t4")
        res = client.get("/api/admin/export", headers=headers)
        self.assertEqual(res.status_code, 403)
        self.assertIn("Admin privileges required", res.json().get("detail", ""))

    # -------------------------------------------------------------------------
    # 5. Unauthenticated request rejected on admin endpoints (401)
    # -------------------------------------------------------------------------
    def test_05_unauthenticated_request_rejected_on_admin_endpoints(self):
        """5. Unauthenticated request without token receives 401 Unauthorized on admin endpoints."""
        for path in ["/api/admin/status", "/api/admin/overview", "/api/admin/users", "/api/admin/export"]:
            res = client.get(path)
            self.assertEqual(res.status_code, 401, f"Path {path} should reject unauthenticated with 401")

    # -------------------------------------------------------------------------
    # 6. Admin can access admin overview (200)
    # -------------------------------------------------------------------------
    def test_06_admin_can_access_admin_overview(self):
        """6. Authenticated ADMIN accesses /api/admin/overview and receives platform metrics."""
        admin, pwd, token, headers = self._create_admin()
        res = client.get("/api/admin/overview", headers=headers)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("total_registered_students", data)
        self.assertIn("onboarding_completed_count", data)
        self.assertIn("diagnostic_completed_count", data)
        self.assertIn("total_submissions_count", data)
        self.assertIn("total_solved_submissions_count", data)
        self.assertIn("active_students_count", data)
        self.assertIn("total_recommendations_count", data)
        self.assertIn("submissions_by_language", data)
        self.assertGreater(data["total_registered_students"], 0)

    # -------------------------------------------------------------------------
    # 7. Admin can access admin users list (200)
    # -------------------------------------------------------------------------
    def test_07_admin_can_access_admin_users_list(self):
        """7. Authenticated ADMIN accesses /api/admin/users and receives student list."""
        admin, pwd, token, headers = self._create_admin()
        res = client.get("/api/admin/users", headers=headers)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("total_count", data)
        self.assertIn("students", data)
        self.assertIsInstance(data["students"], list)
        self.assertGreater(len(data["students"]), 0)

        # Verify each item has student fields
        first_st = data["students"][0]
        self.assertIn("id", first_st)
        self.assertIn("name", first_st)
        self.assertIn("email", first_st)
        self.assertIn("role", first_st)
        self.assertEqual(first_st["role"], "STUDENT")

    # -------------------------------------------------------------------------
    # 8. Admin users list never exposes password hash
    # -------------------------------------------------------------------------
    def test_08_admin_users_list_never_exposes_password_hash(self):
        """8. Admin student list strictly NEVER exposes password, password_hash, or tokens."""
        admin, pwd, token, headers = self._create_admin()
        res = client.get("/api/admin/users", headers=headers)
        self.assertEqual(res.status_code, 200)
        text_resp = res.text
        self.assertNotIn("password_hash", text_resp)
        self.assertNotIn("$2b$", text_resp)
        self.assertNotIn("access_token", text_resp)

        for st in res.json()["students"]:
            self.assertNotIn("password", st)
            self.assertNotIn("password_hash", st)

    # -------------------------------------------------------------------------
    # 9. Admin users list never exposes raw source code
    # -------------------------------------------------------------------------
    def test_09_admin_users_list_never_exposes_raw_source_code(self):
        """9. Admin student list and overview never leak raw submission source code."""
        admin, pwd, token, headers = self._create_admin()
        res = client.get("/api/admin/users", headers=headers)
        self.assertEqual(res.status_code, 200)
        text_resp = res.text
        self.assertNotIn("def solution", text_resp)
        self.assertNotIn("code_submitted", text_resp)

    # -------------------------------------------------------------------------
    # 10. Admin can inspect single student detail (200)
    # -------------------------------------------------------------------------
    def test_10_admin_can_inspect_single_student_detail(self):
        """10. Admin inspects individual student learning record and receives detailed breakdown."""
        student, pwd, s_token, s_headers = self._register_student("p5_t10_inspect")
        admin, a_pwd, a_token, a_headers = self._create_admin()

        res = client.get(f"/api/admin/users/{student.id}", headers=a_headers)
        self.assertEqual(res.status_code, 200)
        detail = res.json()
        self.assertEqual(detail["id"], student.id)
        self.assertEqual(detail["email"], student.email)
        self.assertIn("diagnostic_attempts", detail)
        self.assertIn("recent_submissions", detail)
        self.assertIn("topic_mastery", detail)
        self.assertIn("top_weak_concepts", detail)
        self.assertIn("recent_recommendations", detail)
        self.assertNotIn("password_hash", detail)

    # -------------------------------------------------------------------------
    # 11. Admin export produces sanitized live dataset (JSON & CSV)
    # -------------------------------------------------------------------------
    def test_11_admin_export_produces_sanitized_live_dataset_json_and_csv(self):
        """11. Admin export endpoint produces valid research-grade JSON and CSV datasets."""
        admin, pwd, token, headers = self._create_admin()

        # A) JSON Export
        res_json = client.get("/api/admin/export?format=json", headers=headers)
        self.assertEqual(res_json.status_code, 200)
        exp_data = res_json.json()
        self.assertIn("exported_at", exp_data)
        self.assertIn("total_students", exp_data)
        self.assertIn("dataset", exp_data)
        self.assertGreater(exp_data["total_students"], 0)

        first_rec = exp_data["dataset"][0]
        self.assertIn("student_id", first_rec)
        self.assertIn("name", first_rec)
        self.assertIn("email", first_rec)
        self.assertIn("diagnostic_score", first_rec)
        self.assertIn("total_submissions", first_rec)
        self.assertNotIn("password_hash", first_rec)

        # B) CSV Export
        res_csv = client.get("/api/admin/export?format=csv", headers=headers)
        self.assertEqual(res_csv.status_code, 200)
        self.assertIn("text/csv", res_csv.headers.get("content-type", ""))
        self.assertIn("attachment; filename=", res_csv.headers.get("content-disposition", ""))
        csv_text = res_csv.text
        self.assertTrue(csv_text.startswith("student_id,name,email,role"))
        self.assertNotIn("password_hash", csv_text)

    # -------------------------------------------------------------------------
    # 12. Complete Real-User Lifecycle Test (Live-Data Persistence)
    # -------------------------------------------------------------------------
    def test_12_live_student_lifecycle_and_activity_persistence(self):
        """
        12. Explicit real-user lifecycle test:
        1. Register new STUDENT
        2. Login
        3. Complete onboarding
        4. Complete diagnostic
        5. Submit coding problem
        6. Receive recommendation
        7. Verify knowledge state updated
        8. Verify concept state updated
        9. Logout
        10. Login again
        11. Verify all previous progress remains
        12. Login as ADMIN
        13. Verify new student's activity appears in admin monitoring data
        """
        # Step 1: Register new student
        uid = uuid.uuid4().hex[:8]
        raw_password = "SecureStudentPass123!"
        reg_res = client.post("/api/auth/register", json={
            "name": f"LiveLearner_{uid}",
            "email": f"live_learner_{uid}@test.com",
            "password": raw_password
        })
        self.assertEqual(reg_res.status_code, 201)
        reg_data = reg_res.json()
        student_id = reg_data["user"]["id"]
        db_student = self.db.query(User).filter(User.id == student_id).first()
        self.created_users.append(db_student)

        # Step 2: Login
        login_res = client.post("/api/auth/login", json={
            "email": f"live_learner_{uid}@test.com",
            "password": raw_password
        })
        self.assertEqual(login_res.status_code, 200)
        s_token = login_res.json()["access_token"]
        s_headers = {"Authorization": f"Bearer {s_token}"}

        # Step 3: Complete onboarding
        ob_res = client.post("/api/onboarding", headers=s_headers, json={
            "learning_goal": "placement_prep",
            "experience_level": "intermediate"
        })
        self.assertEqual(ob_res.status_code, 200)

        # Step 4: Complete diagnostic (solve 3 problems)
        diag_probs = client.get("/api/diagnostic/problems", headers=s_headers).json()
        self.assertEqual(len(diag_probs), 7)
        for i in range(3):
            sub_res = client.post("/api/diagnostic/submit", headers=s_headers, json={
                "problem_id": diag_probs[i]["id"],
                "is_solved": True,
                "time_spent_seconds": 30
            })
            self.assertEqual(sub_res.status_code, 200)

        comp_diag_res = client.post("/api/diagnostic/complete", headers=s_headers)
        self.assertEqual(comp_diag_res.status_code, 200)
        self.assertEqual(comp_diag_res.json()["solved_count"], 3)

        # Step 5: Submit coding problems (solve Problem 1 Two Sum in Python)
        py_solution = """def twoSum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return [seen[target - n], i]
        seen[n] = i
    return []
"""
        code_sub = client.post("/api/submissions/submit", headers=s_headers, json={
            "problem_id": 1,
            "code": py_solution,
            "language": "python"
        })
        self.assertIn(code_sub.status_code, [200, 201])
        self.assertEqual(code_sub.json()["status"], "Accepted")

        # Step 6: Receive recommendation
        rec_res = client.get("/api/recommendations/next", headers=s_headers)
        self.assertEqual(rec_res.status_code, 200)
        self.assertIn("problem_id", rec_res.json())

        # Step 7 & 8: Verify learner knowledge state & concept state updated in DB
        self.db.rollback()
        k_states = self.db.query(LearnerKnowledgeState).filter(LearnerKnowledgeState.user_id == student_id).all()
        self.assertEqual(len(k_states), 10, "Must have 10 initialized topic knowledge states.")
        c_states = self.db.query(LearnerConceptState).filter(LearnerConceptState.user_id == student_id).all()
        self.assertGreater(len(c_states), 0, "Must have updated concept states.")

        # Step 9: Logout (represented by dropping token client-side)
        del s_headers

        # Step 10: Login again
        login2_res = client.post("/api/auth/login", json={
            "email": f"live_learner_{uid}@test.com",
            "password": raw_password
        })
        self.assertEqual(login2_res.status_code, 200)
        token2 = login2_res.json()["access_token"]
        headers2 = {"Authorization": f"Bearer {token2}"}

        # Step 11: Verify all previous progress remains intact
        me_res = client.get("/api/auth/me", headers=headers2)
        self.assertEqual(me_res.status_code, 200)
        me_data = me_res.json()
        self.assertTrue(me_data["onboarding_completed"])
        self.assertTrue(me_data["diagnostic_completed"])
        self.assertEqual(me_data["diagnostic_score"], 3)
        self.assertEqual(me_data["diagnostic_total"], 7)

        # Step 12: Login as ADMIN
        admin, a_pwd, a_token, a_headers = self._create_admin()

        # Step 13: Verify newly created student's activity appears in admin monitoring data
        admin_users_res = client.get(f"/api/admin/users?search=live_learner_{uid}", headers=a_headers)
        self.assertEqual(admin_users_res.status_code, 200)
        st_list = admin_users_res.json()["students"]
        self.assertEqual(len(st_list), 1)
        monitored_student = st_list[0]
        self.assertEqual(monitored_student["id"], student_id)
        self.assertTrue(monitored_student["diagnostic_completed"])
        self.assertEqual(monitored_student["diagnostic_score"], 3)
        self.assertEqual(monitored_student["solved_problems_count"], 1)
        self.assertEqual(monitored_student["total_submissions"], 1)
        self.assertIsNotNone(monitored_student["last_activity_at"])

    # -------------------------------------------------------------------------
    # 13. Student isolation strictly preserved
    # -------------------------------------------------------------------------
    def test_13_student_isolation_strictly_preserved(self):
        """13. Student A cannot access Student B's submissions or diagnostic attempts."""
        student_a, pwd_a, tok_a, headers_a = self._register_student("p5_t13_a")
        student_b, pwd_b, tok_b, headers_b = self._register_student("p5_t13_b")

        # Student A completes diagnostic
        probs = client.get("/api/diagnostic/problems", headers=headers_a).json()
        client.post("/api/diagnostic/submit", headers=headers_a, json={
            "problem_id": probs[0]["id"], "is_solved": True, "time_spent_seconds": 25
        })
        client.post("/api/diagnostic/complete", headers=headers_a)

        # Student B cannot access Student A's score endpoint
        score_b = client.get("/api/diagnostic/score", headers=headers_b)
        self.assertEqual(score_b.status_code, 400, "Student B cannot see any completed score")

        # Student B cannot access Student A's diagnostic history
        hist_b = client.get("/api/diagnostic/history", headers=headers_b).json()
        self.assertEqual(len(hist_b), 0, "Student B's history must remain strictly empty")

    # -------------------------------------------------------------------------
    # 14. Public registration cannot create admin
    # -------------------------------------------------------------------------
    def test_14_public_registration_cannot_create_admin(self):
        """14. Attempts to inject role: 'ADMIN' during public registration are forced to 'STUDENT'."""
        uid = uuid.uuid4().hex[:8]
        res = client.post("/api/auth/register", json={
            "name": f"Hacker_{uid}",
            "email": f"hacker_{uid}@test.com",
            "password": "Password123!",
            "role": "ADMIN"
        })
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertEqual(data["user"]["role"], "STUDENT", "Public registration must strictly enforce STUDENT role")
        db_user = self.db.query(User).filter(User.id == data["user"]["id"]).first()
        self.created_users.append(db_user)
        self.assertEqual(db_user.role, "STUDENT")

    # -------------------------------------------------------------------------
    # 15. Regression check across previous phases
    # -------------------------------------------------------------------------
    def test_15_phases_1_to_4_regressions_zero(self):
        """15. Confirm that baseline diagnostic exemptions, gate, and existing users remain unregressed."""
        # Baseline legacy user accesses platform normally
        legacy = self.db.query(User).filter(User.id <= 297, User.diagnostic_exempt == True).first()
        self.assertIsNotNone(legacy)
        token = create_access_token(subject=str(legacy.id), role=legacy.role)
        headers = {"Authorization": f"Bearer {token}"}

        d_res = client.get("/api/dashboard/summary", headers=headers)
        self.assertEqual(d_res.status_code, 200, "Legacy exempt students must access dashboard without error")


if __name__ == "__main__":
    unittest.main(verbosity=2)
