"""
Phase 4 Verification Suite: Permanent Diagnostic Completion Enforcement,
Retake Prevention, and Diagnostic Score Display.

Covers all 15 required verification criteria:
1. test_01_incomplete_student_blocked_from_personalized_learning
2. test_02_incomplete_student_can_start_diagnostic
3. test_03_diagnostic_completion_stores_persistent_state
4. test_04_diagnostic_score_stored_correctly
5. test_05_completed_student_cannot_restart_diagnostic
6. test_06_completed_student_cannot_submit_another_attempt
7. test_07_completion_survives_fresh_login_session
8. test_08_completion_survives_refresh_and_status_check
9. test_09_completed_student_score_endpoint_works
10. test_10_existing_diagnostic_history_intact
11. test_11_legitimate_diagnostic_exemptions_work
12. test_12_recommendation_flow_works_after_diagnostic_completion
13. test_13_student_isolation_preserved
14. test_14_phase1_rbac_preserved
15. test_15_phase3_multilang_preserved
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


class TestPhase4DiagnosticCompletion(unittest.TestCase):
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

    def _register_student(self, name_prefix="p4_student"):
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
        admin = User(
            name=f"Admin_{uid}",
            email=f"admin_{uid}@test.com",
            password_hash=get_password_hash("AdminPass123!"),
            role=UserRole.ADMIN,
            diagnostic_completed=False,
            diagnostic_exempt=False
        )
        self.db.add(admin)
        self.db.commit()
        self.db.refresh(admin)
        self.created_users.append(admin)
        token = create_access_token(subject=str(admin.id), role=admin.role)
        headers = {"Authorization": f"Bearer {token}"}
        return admin, token, headers

    # -------------------------------------------------------------------------
    # 1. Incomplete student blocked from personalized learning
    # -------------------------------------------------------------------------
    def test_01_incomplete_student_blocked_from_personalized_learning(self):
        """1. Incomplete student is blocked from personalized learning with 403 Forbidden."""
        user, pwd, token, headers = self._register_student("p4_t1_block")

        # Dashboard summary blocked
        d_res = client.get("/api/dashboard/summary", headers=headers)
        self.assertEqual(d_res.status_code, 403)
        self.assertIn("Diagnostic assessment required", d_res.json().get("detail", ""))

        # Recommendations next blocked
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

        # Submissions run for non-diagnostic problem blocked
        non_diag = self.db.query(Problem).filter(Problem.is_diagnostic == False).first()
        self.assertIsNotNone(non_diag)
        run_res = client.post("/api/submissions/run", headers=headers, json={
            "problem_id": non_diag.id,
            "code": "def solution(): return 42"
        })
        self.assertEqual(run_res.status_code, 403)
        self.assertIn("Diagnostic assessment required", run_res.json().get("detail", ""))

    # -------------------------------------------------------------------------
    # 2. Incomplete student can start diagnostic
    # -------------------------------------------------------------------------
    def test_02_incomplete_student_can_start_diagnostic(self):
        """2. Incomplete student can fetch diagnostic problems and execute code on them."""
        user, pwd, token, headers = self._register_student("p4_t2_start")

        # Can fetch diagnostic problems
        p_res = client.get("/api/diagnostic/problems", headers=headers)
        self.assertEqual(p_res.status_code, 200)
        probs = p_res.json()
        self.assertEqual(len(probs), 7)
        for prob in probs:
            self.assertTrue(prob["is_diagnostic"])

        # Can run code for a diagnostic problem
        diag_prob_id = probs[0]["id"]
        run_res = client.post("/api/submissions/run", headers=headers, json={
            "problem_id": diag_prob_id,
            "code": "# Python test\ndef solution(): return 1"
        })
        self.assertEqual(run_res.status_code, 200)

    # -------------------------------------------------------------------------
    # 3. Diagnostic completion stores persistent state
    # -------------------------------------------------------------------------
    def test_03_diagnostic_completion_stores_persistent_state(self):
        """3. Diagnostic completion marks diagnostic_completed=True and sets timestamp in DB."""
        user, pwd, token, headers = self._register_student("p4_t3_persist")
        probs = client.get("/api/diagnostic/problems", headers=headers).json()

        # Submit an attempt
        client.post("/api/diagnostic/submit", headers=headers, json={
            "problem_id": probs[0]["id"],
            "is_solved": True,
            "time_spent_seconds": 35
        })

        # Complete diagnostic
        comp_res = client.post("/api/diagnostic/complete", headers=headers)
        self.assertEqual(comp_res.status_code, 200)

        # Check DB directly
        self.db.rollback()
        fresh_user = self.db.query(User).filter(User.id == user.id).first()
        self.assertTrue(fresh_user.diagnostic_completed)
        self.assertIsNotNone(fresh_user.diagnostic_completed_at)
        self.assertIsInstance(fresh_user.diagnostic_completed_at, datetime)

    # -------------------------------------------------------------------------
    # 4. Diagnostic score stored correctly
    # -------------------------------------------------------------------------
    def test_04_diagnostic_score_stored_correctly(self):
        """4. Diagnostic score and total are stored accurately matching solved attempts."""
        user, pwd, token, headers = self._register_student("p4_t4_score")
        probs = client.get("/api/diagnostic/problems", headers=headers).json()
        total_diag = len(probs)
        self.assertEqual(total_diag, 7)

        # Solve 3 problems, fail 1
        client.post("/api/diagnostic/submit", headers=headers, json={
            "problem_id": probs[0]["id"], "is_solved": True, "time_spent_seconds": 30
        })
        client.post("/api/diagnostic/submit", headers=headers, json={
            "problem_id": probs[1]["id"], "is_solved": True, "time_spent_seconds": 45
        })
        client.post("/api/diagnostic/submit", headers=headers, json={
            "problem_id": probs[2]["id"], "is_solved": True, "time_spent_seconds": 50
        })
        client.post("/api/diagnostic/submit", headers=headers, json={
            "problem_id": probs[3]["id"], "is_solved": False, "time_spent_seconds": 60
        })

        # Complete
        comp_res = client.post("/api/diagnostic/complete", headers=headers)
        self.assertEqual(comp_res.status_code, 200)
        data = comp_res.json()
        self.assertEqual(data["solved_count"], 3)
        self.assertEqual(data["total_problems"], 7)

        # Verify DB directly
        self.db.rollback()
        fresh_user = self.db.query(User).filter(User.id == user.id).first()
        self.assertEqual(fresh_user.diagnostic_score, 3)
        self.assertEqual(fresh_user.diagnostic_total, 7)

    # -------------------------------------------------------------------------
    # 5. Completed student cannot restart diagnostic
    # -------------------------------------------------------------------------
    def test_05_completed_student_cannot_restart_diagnostic(self):
        """5. Completed student cannot restart diagnostic (GET /problems returns 400 Bad Request)."""
        user, pwd, token, headers = self._register_student("p4_t5_norestart")
        client.post("/api/diagnostic/complete", headers=headers)

        # Attempt to get problems again
        prob_res = client.get("/api/diagnostic/problems", headers=headers)
        self.assertEqual(prob_res.status_code, 400)
        self.assertIn("already been completed", prob_res.json().get("detail", ""))

    # -------------------------------------------------------------------------
    # 6. Completed student cannot submit another attempt
    # -------------------------------------------------------------------------
    def test_06_completed_student_cannot_submit_another_attempt(self):
        """6. Completed student cannot submit attempts or complete again (400 Bad Request)."""
        user, pwd, token, headers = self._register_student("p4_t6_nosubmit")
        probs = self.db.query(Problem).filter(Problem.is_diagnostic == True).all()
        client.post("/api/diagnostic/complete", headers=headers)

        # Attempt to submit attempt after completion
        sub_res = client.post("/api/diagnostic/submit", headers=headers, json={
            "problem_id": probs[0].id,
            "is_solved": True,
            "time_spent_seconds": 20
        })
        self.assertEqual(sub_res.status_code, 400)
        self.assertIn("already been completed", sub_res.json().get("detail", ""))

        # Attempt to complete again
        comp2_res = client.post("/api/diagnostic/complete", headers=headers)
        self.assertEqual(comp2_res.status_code, 400)
        self.assertIn("already been completed", comp2_res.json().get("detail", ""))

    # -------------------------------------------------------------------------
    # 7. Completion survives fresh login session
    # -------------------------------------------------------------------------
    def test_07_completion_survives_fresh_login_session(self):
        """7. Diagnostic completion and score persist across a brand-new login session."""
        user, raw_pwd, token, headers = self._register_student("p4_t7_login")
        probs = client.get("/api/diagnostic/problems", headers=headers).json()

        # Solve 2 problems
        client.post("/api/diagnostic/submit", headers=headers, json={
            "problem_id": probs[0]["id"], "is_solved": True, "time_spent_seconds": 25
        })
        client.post("/api/diagnostic/submit", headers=headers, json={
            "problem_id": probs[1]["id"], "is_solved": True, "time_spent_seconds": 35
        })
        client.post("/api/diagnostic/complete", headers=headers)

        # Fresh Login
        login_res = client.post("/api/auth/login", json={
            "email": user.email,
            "password": raw_pwd
        })
        self.assertEqual(login_res.status_code, 200)
        login_data = login_res.json()
        user_info = login_data["user"]
        self.assertTrue(user_info["diagnostic_completed"])
        self.assertEqual(user_info["diagnostic_score"], 2)
        self.assertEqual(user_info["diagnostic_total"], 7)
        self.assertIsNotNone(user_info["diagnostic_completed_at"])

        # Call /api/auth/me with the new session token
        new_token = login_data["access_token"]
        new_headers = {"Authorization": f"Bearer {new_token}"}
        me_res = client.get("/api/auth/me", headers=new_headers)
        self.assertEqual(me_res.status_code, 200)
        me_data = me_res.json()
        self.assertTrue(me_data["diagnostic_completed"])
        self.assertEqual(me_data["diagnostic_score"], 2)
        self.assertEqual(me_data["diagnostic_total"], 7)

    # -------------------------------------------------------------------------
    # 8. Completion survives refresh and status check
    # -------------------------------------------------------------------------
    def test_08_completion_survives_refresh_and_status_check(self):
        """8. Diagnostic status endpoint returns completed state and learning endpoints remain unblocked."""
        user, raw_pwd, token, headers = self._register_student("p4_t8_status")
        probs = client.get("/api/diagnostic/problems", headers=headers).json()

        # Solve 4 problems
        for i in range(4):
            client.post("/api/diagnostic/submit", headers=headers, json={
                "problem_id": probs[i]["id"], "is_solved": True, "time_spent_seconds": 20
            })
        client.post("/api/diagnostic/complete", headers=headers)

        # Status check
        status_res = client.get("/api/diagnostic/status", headers=headers)
        self.assertEqual(status_res.status_code, 200)
        s_data = status_res.json()
        self.assertTrue(s_data["diagnostic_completed"])
        self.assertFalse(s_data["can_take_diagnostic"])
        self.assertEqual(s_data["diagnostic_score"], 4)
        self.assertEqual(s_data["diagnostic_total"], 7)
        self.assertEqual(s_data["score_percent"], round(4 / 7 * 100, 1))

        # Dashboard remains unblocked
        d_res = client.get("/api/dashboard/summary", headers=headers)
        self.assertEqual(d_res.status_code, 200)

        # Recommendations remain unblocked
        r_res = client.get("/api/recommendations/next", headers=headers)
        self.assertEqual(r_res.status_code, 200)

    # -------------------------------------------------------------------------
    # 9. Completed student score endpoint works
    # -------------------------------------------------------------------------
    def test_09_completed_student_score_endpoint_works(self):
        """9. Dedicated GET /api/diagnostic/score endpoint returns 200 for completed, 400 for uncompleted."""
        # A) Incomplete student
        inc_user, inc_pwd, inc_tok, inc_headers = self._register_student("p4_t9_inc")
        score_err_res = client.get("/api/diagnostic/score", headers=inc_headers)
        self.assertEqual(score_err_res.status_code, 400)
        self.assertIn("not been completed", score_err_res.json().get("detail", ""))

        # B) Completed student
        comp_user, comp_pwd, comp_tok, comp_headers = self._register_student("p4_t9_comp")
        probs = client.get("/api/diagnostic/problems", headers=comp_headers).json()
        for i in range(5):
            client.post("/api/diagnostic/submit", headers=comp_headers, json={
                "problem_id": probs[i]["id"], "is_solved": True, "time_spent_seconds": 15
            })
        client.post("/api/diagnostic/complete", headers=comp_headers)

        score_res = client.get("/api/diagnostic/score", headers=comp_headers)
        self.assertEqual(score_res.status_code, 200)
        sc = score_res.json()
        self.assertTrue(sc["diagnostic_completed"])
        self.assertEqual(sc["diagnostic_score"], 5)
        self.assertEqual(sc["diagnostic_total"], 7)
        self.assertEqual(sc["score"], 5)
        self.assertEqual(sc["total"], 7)
        self.assertEqual(sc["score_percent"], round(5 / 7 * 100, 1))
        self.assertEqual(sc["status"], "completed")
        self.assertIsNotNone(sc["completed_at"])

    # -------------------------------------------------------------------------
    # 10. Existing diagnostic history intact
    # -------------------------------------------------------------------------
    def test_10_existing_diagnostic_history_intact(self):
        """10. Existing diagnostic history returns attempts and baseline DB counts are preserved."""
        user, pwd, token, headers = self._register_student("p4_t10_hist")
        probs = client.get("/api/diagnostic/problems", headers=headers).json()

        # Submit 2 attempts
        p0 = self.db.query(Problem).filter(Problem.id == probs[0]["id"]).first()
        client.post("/api/diagnostic/submit", headers=headers, json={
            "problem_id": probs[0]["id"],
            "is_solved": True,
            "time_spent_seconds": 45,
            "code_submitted": p0.reference_solution_python
        })
        client.post("/api/diagnostic/submit", headers=headers, json={
            "problem_id": probs[1]["id"],
            "is_solved": False,
            "time_spent_seconds": 65,
            "code_submitted": "print('hist2')"
        })

        # History endpoint
        h_res = client.get("/api/diagnostic/history", headers=headers)
        self.assertEqual(h_res.status_code, 200)
        h_data = h_res.json()
        self.assertEqual(len(h_data), 2)
        self.assertTrue(h_data[0]["is_solved"])
        self.assertFalse(h_data[1]["is_solved"])

        # Baseline DB check: Ensure historical baseline diagnostic attempts >= 223
        baseline_attempts = self.db.query(DiagnosticAttempt).filter(DiagnosticAttempt.user_id <= 297).count()
        self.assertEqual(baseline_attempts, 223, "Baseline diagnostic attempts count must be exactly 223!")

    # -------------------------------------------------------------------------
    # 11. Legitimate diagnostic exemptions work
    # -------------------------------------------------------------------------
    def test_11_legitimate_diagnostic_exemptions_work(self):
        """11. Baseline exempt users and Admin users bypass the diagnostic gate legitimately."""
        # Baseline legacy user
        legacy = self.db.query(User).filter(User.id <= 297, User.diagnostic_exempt == True).first()
        self.assertIsNotNone(legacy)
        leg_token = create_access_token(subject=str(legacy.id), role=legacy.role)
        leg_headers = {"Authorization": f"Bearer {leg_token}"}

        d_res = client.get("/api/dashboard/summary", headers=leg_headers)
        self.assertEqual(d_res.status_code, 200)

        # Admin user
        admin, admin_token, admin_headers = self._create_admin()
        adm_d_res = client.get("/api/dashboard/summary", headers=admin_headers)
        self.assertEqual(adm_d_res.status_code, 200)

    # -------------------------------------------------------------------------
    # 12. Recommendation flow works after diagnostic completion
    # -------------------------------------------------------------------------
    def test_12_recommendation_flow_works_after_diagnostic_completion(self):
        """12. Recommendation engine functions seamlessly after diagnostic completion."""
        user, pwd, token, headers = self._register_student("p4_t12_rec")
        probs = client.get("/api/diagnostic/problems", headers=headers).json()

        # Submit an attempt and complete
        client.post("/api/diagnostic/submit", headers=headers, json={
            "problem_id": probs[0]["id"], "is_solved": True, "time_spent_seconds": 20
        })
        client.post("/api/diagnostic/complete", headers=headers)

        # Request next recommendation
        rec_res = client.get("/api/recommendations/next", headers=headers)
        self.assertEqual(rec_res.status_code, 200)
        rec_data = rec_res.json()
        self.assertIn("problem_id", rec_data)
        self.assertIn("problem", rec_data)
        self.assertTrue(len(rec_data["problem"]["title"]) > 0)
        self.assertTrue(len(rec_data["problem"]["topic_name"]) > 0)

        # Knowledge state is initialized
        self.db.rollback()
        states = self.db.query(LearnerKnowledgeState).filter(LearnerKnowledgeState.user_id == user.id).all()
        self.assertEqual(len(states), 10, "User must have 10 initialized topic knowledge states.")

    # -------------------------------------------------------------------------
    # 13. Student isolation preserved
    # -------------------------------------------------------------------------
    def test_13_student_isolation_preserved(self):
        """13. Student A's diagnostic results and history cannot leak to Student B."""
        user_a, pwd_a, tok_a, headers_a = self._register_student("p4_t13_user_a")
        user_b, pwd_b, tok_b, headers_b = self._register_student("p4_t13_user_b")

        probs = client.get("/api/diagnostic/problems", headers=headers_a).json()

        # User A solves 3 problems and completes
        for i in range(3):
            client.post("/api/diagnostic/submit", headers=headers_a, json={
                "problem_id": probs[i]["id"], "is_solved": True, "time_spent_seconds": 20
            })
        client.post("/api/diagnostic/complete", headers=headers_a)

        # User A gets score
        score_a = client.get("/api/diagnostic/score", headers=headers_a)
        self.assertEqual(score_a.status_code, 200)
        self.assertEqual(score_a.json()["diagnostic_score"], 3)

        # User B has NOT completed diagnostic -> cannot access score
        score_b = client.get("/api/diagnostic/score", headers=headers_b)
        self.assertEqual(score_b.status_code, 400)

        # User B's history is empty
        hist_b = client.get("/api/diagnostic/history", headers=headers_b).json()
        self.assertEqual(len(hist_b), 0)

        # User B is still blocked from dashboard
        dash_b = client.get("/api/dashboard/summary", headers=headers_b)
        self.assertEqual(dash_b.status_code, 403)

    # -------------------------------------------------------------------------
    # 14. Phase 1 RBAC preserved
    # -------------------------------------------------------------------------
    def test_14_phase1_rbac_preserved(self):
        """14. Student cannot access Admin routes (403); Admin receives 200."""
        user, pwd, token, headers = self._register_student("p4_t14_rbac")
        admin, admin_token, admin_headers = self._create_admin()

        # Student denied from admin status
        res_student = client.get("/api/admin/status", headers=headers)
        self.assertEqual(res_student.status_code, 403)

        # Admin allowed to access admin status
        res_admin = client.get("/api/admin/status", headers=admin_headers)
        self.assertEqual(res_admin.status_code, 200)
        self.assertEqual(res_admin.json()["role"], "ADMIN")

    # -------------------------------------------------------------------------
    # 15. Phase 3 multi-language preserved
    # -------------------------------------------------------------------------
    def test_15_phase3_multilang_preserved(self):
        """15. Python, Java, and JavaScript execution work reliably in code runner."""
        # Baseline exempt student to run submissions
        user = self.db.query(User).filter(User.id <= 297, User.diagnostic_exempt == True).first()
        self.assertIsNotNone(user)
        token = create_access_token(subject=str(user.id), role=user.role)
        headers = {"Authorization": f"Bearer {token}"}

        # 1. Python Execution
        py_code = """def twoSum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return [seen[target - n], i]
        seen[n] = i
    return []
"""
        res_py = client.post("/api/submissions/run", json={"problem_id": 1, "code": py_code, "language": "python"}, headers=headers)
        self.assertEqual(res_py.status_code, 200)
        self.assertEqual(res_py.json()["status"], "Accepted")

        # 2. JavaScript Execution
        js_code = """function twoSum(nums, target) {
    const map = new Map();
    for (let i = 0; i < nums.length; i++) {
        const comp = target - nums[i];
        if (map.has(comp)) return [map.get(comp), i];
        map.set(nums[i], i);
    }
    return [];
}
"""
        res_js = client.post("/api/submissions/run", json={"problem_id": 1, "code": js_code, "language": "javascript"}, headers=headers)
        self.assertEqual(res_js.status_code, 200)
        self.assertEqual(res_js.json()["status"], "Accepted")

        # 3. Java Execution
        java_code = """import java.util.*;

public class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> map = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int comp = target - nums[i];
            if (map.containsKey(comp)) {
                return new int[] { map.get(comp), i };
            }
            map.put(nums[i], i);
        }
        return new int[0];
    }
}
"""
        res_java = client.post("/api/submissions/run", json={"problem_id": 1, "code": java_code, "language": "java"}, headers=headers)
        self.assertEqual(res_java.status_code, 200)
        self.assertEqual(res_java.json()["status"], "Accepted")


if __name__ == "__main__":
    unittest.main(verbosity=2)
