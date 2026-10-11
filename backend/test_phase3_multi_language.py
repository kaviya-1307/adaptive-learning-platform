"""
Phase 3 Multi-Language Coding Platform Verification Suite.
Validates:
1. Python execution working for run and submit.
2. Java execution working for run and submit (via installed javac & java 21).
3. JavaScript execution working for run and submit (via installed node).
4. C++ execution cleanly detects compiler not installed.
5. Unsupported language string rejected with HTTP 400 Bad Request.
6. Problem without language support rejects execution with HTTP 400 Bad Request.
7. Submissions persist the selected language in database.
8. Historical submissions remain readable with language field.
9. Problem detail endpoint returns supported_languages and starter codes.
10. Compilation/Syntax errors formatted correctly.
11. Runtime errors formatted correctly.
12. Timeouts handled with Time Limit Exceeded.
13. Student isolation preserved across multi-language submissions.
14. Diagnostic gating preserved for uncompleted students.
15. Recommendation generation operates seamlessly after multi-language submissions.
"""
import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.main import app
from app.core.database import SessionLocal
from app.models.user import User
from app.models.submission import Submission
from app.models.problem import Problem
from app.core.security import get_password_hash, create_access_token
from app.engine.code_runner import CodeRunner

client = TestClient(app)


class TestPhase3MultiLanguage:
    def setup_method(self):
        self.db = SessionLocal()
        self.test_user_ids = []

    def teardown_method(self):
        try:
            if self.test_user_ids:
                # Clean up dependent records
                for t in [
                    "submissions",
                    "diagnostic_attempts",
                    "recommendations",
                    "learner_knowledge_state",
                    "learner_concept_states",
                    "onboarding_profiles"
                ]:
                    self.db.execute(text(f"DELETE FROM {t} WHERE user_id IN ({','.join(str(i) for i in self.test_user_ids)})"))
                self.db.execute(text(f"DELETE FROM users WHERE id IN ({','.join(str(i) for i in self.test_user_ids)})"))
                self.db.commit()
        finally:
            self.db.close()

    def _create_exempt_student(self):
        uid = uuid.uuid4().hex[:8]
        user = User(
            email=f"ml_student_{uid}@test.com",
            password_hash=get_password_hash("StudentPass123!"),
            name=f"ML Student {uid}",
            role="STUDENT",
            diagnostic_exempt=True,
            diagnostic_completed=False
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        self.test_user_ids.append(user.id)
        token = create_access_token(subject=str(user.id), role="STUDENT")
        return user, token

    def _create_uncompleted_student(self):
        uid = uuid.uuid4().hex[:8]
        user = User(
            email=f"ml_new_{uid}@test.com",
            password_hash=get_password_hash("StudentPass123!"),
            name=f"ML New {uid}",
            role="STUDENT",
            diagnostic_exempt=False,
            diagnostic_completed=False
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        self.test_user_ids.append(user.id)
        token = create_access_token(subject=str(user.id), role="STUDENT")
        return user, token

    # -------------------------------------------------------------
    # 1. Existing Python Execution
    # -------------------------------------------------------------
    def test_01_python_execution_working(self):
        user, token = self._create_exempt_student()
        headers = {"Authorization": f"Bearer {token}"}

        code = """def twoSum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return [seen[target - n], i]
        seen[n] = i
    return []
"""
        res = client.post("/api/submissions/run", json={"problem_id": 1, "code": code, "language": "python"}, headers=headers)
        assert res.status_code == 200, res.text
        data = res.json()
        assert data["status"] == "Accepted"
        assert data["passed_test_cases"] == data["total_test_cases"]

    # -------------------------------------------------------------
    # 2. Java Execution (via javac & java 21)
    # -------------------------------------------------------------
    def test_02_java_execution_working(self):
        user, token = self._create_exempt_student()
        headers = {"Authorization": f"Bearer {token}"}

        code = """import java.util.HashMap;
import java.util.Map;

class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> map = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            if (map.containsKey(complement)) {
                return new int[]{map.get(complement), i};
            }
            map.put(nums[i], i);
        }
        return new int[]{};
    }
}"""
        res = client.post("/api/submissions/run", json={"problem_id": 1, "code": code, "language": "java"}, headers=headers)
        assert res.status_code == 200, res.text
        data = res.json()
        assert data["status"] == "Accepted"
        assert data["passed_test_cases"] == data["total_test_cases"]

    # -------------------------------------------------------------
    # 3. JavaScript Execution (via Node.js)
    # -------------------------------------------------------------
    def test_03_javascript_execution_working(self):
        user, token = self._create_exempt_student()
        headers = {"Authorization": f"Bearer {token}"}

        code = """function twoSum(nums, target) {
    const map = new Map();
    for (let i = 0; i < nums.length; i++) {
        const comp = target - nums[i];
        if (map.has(comp)) {
            return [map.get(comp), i];
        }
        map.set(nums[i], i);
    }
    return [];
}"""
        res = client.post("/api/submissions/run", json={"problem_id": 1, "code": code, "language": "javascript"}, headers=headers)
        assert res.status_code == 200, res.text
        data = res.json()
        assert data["status"] == "Accepted"
        assert data["passed_test_cases"] == data["total_test_cases"]

    # -------------------------------------------------------------
    # 4. C++ Execution & Compiler Verification
    # -------------------------------------------------------------
    def test_04_cpp_execution_cleanly_detects_compiler(self):
        user, token = self._create_exempt_student()
        headers = {"Authorization": f"Bearer {token}"}

        code = """#include <vector>
using namespace std;
class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) { return {}; }
};"""
        res = client.post("/api/submissions/run", json={"problem_id": 1, "code": code, "language": "cpp"}, headers=headers)
        assert res.status_code == 200, res.text
        data = res.json()
        import shutil
        if shutil.which("g++") or shutil.which("clang++"):
            # Compiler is installed and executed the code (returning Wrong Answer for empty vector return)
            assert data["status"] in ["Wrong Answer", "Accepted"]
            assert data["total_test_cases"] > 0
        else:
            assert data["status"] == "Compilation Error"
            assert "not installed" in data["compile_error"].lower() or "not configured" in data["compile_error"].lower()

    # -------------------------------------------------------------
    # 5. Unsupported Language Rejected
    # -------------------------------------------------------------
    def test_05_unsupported_language_rejected(self):
        user, token = self._create_exempt_student()
        headers = {"Authorization": f"Bearer {token}"}

        res = client.post("/api/submissions/run", json={"problem_id": 1, "code": "puts 1", "language": "ruby"}, headers=headers)
        assert res.status_code == 400
        assert "unsupported language" in res.json()["detail"].lower()

    # -------------------------------------------------------------
    # 6. Problem Not Supporting Language Rejected
    # -------------------------------------------------------------
    def test_06_problem_without_language_support_rejected(self):
        user, token = self._create_exempt_student()
        headers = {"Authorization": f"Bearer {token}"}

        # Problem 45 is an MBPP problem (Python only)
        res = client.post("/api/submissions/run", json={"problem_id": 45, "code": "function f() {}", "language": "javascript"}, headers=headers)
        assert res.status_code == 400
        assert "not supported for problem" in res.json()["detail"].lower()

    # -------------------------------------------------------------
    # 7. Submission Stores Selected Language
    # -------------------------------------------------------------
    def test_07_submission_stores_selected_language(self):
        user, token = self._create_exempt_student()
        headers = {"Authorization": f"Bearer {token}"}

        # Submit JavaScript solution
        js_code = """function twoSum(nums, target) {
    const map = new Map();
    for (let i = 0; i < nums.length; i++) {
        const comp = target - nums[i];
        if (map.has(comp)) return [map.get(comp), i];
        map.set(nums[i], i);
    }
    return [];
}"""
        res = client.post("/api/submissions/submit", json={"problem_id": 1, "code": js_code, "language": "javascript"}, headers=headers)
        assert res.status_code == 201, res.text
        data = res.json()
        sub_id = data["id"]
        assert data["language"] == "javascript"
        assert data["status"] == "Accepted"

        # Verify DB row
        self.db.rollback()
        sub = self.db.query(Submission).filter(Submission.id == sub_id).first()
        assert sub is not None
        assert sub.language == "javascript"

    # -------------------------------------------------------------
    # 8. Existing Submissions Remain Readable
    # -------------------------------------------------------------
    def test_08_existing_submissions_remain_readable(self):
        # 1. Verify historical submission #1 has language column and reads as 'python'
        sub1 = self.db.query(Submission).filter(Submission.id == 1).first()
        assert sub1 is not None
        assert sub1.language == "python"

        # 2. Test user reading their own submission via API returns language
        user, token = self._create_exempt_student()
        headers = {"Authorization": f"Bearer {token}"}
        sub_create = client.post("/api/submissions/submit", json={"problem_id": 1, "code": "def twoSum(nums, target): return []", "language": "python"}, headers=headers)
        assert sub_create.status_code == 201
        new_sub_id = sub_create.json()["id"]

        res = client.get(f"/api/submissions/{new_sub_id}", headers=headers)
        assert res.status_code == 200
        assert res.json()["language"] == "python"

    # -------------------------------------------------------------
    # 9. Problem Detail Returns Supported Languages & Starter Codes
    # -------------------------------------------------------------
    def test_09_problem_detail_returns_supported_languages(self):
        res = client.get("/api/problems/two-sum-target-pair")
        assert res.status_code == 200
        data = res.json()
        assert "supported_languages" in data
        assert "python" in data["supported_languages"]
        assert "java" in data["supported_languages"]
        assert "cpp" in data["supported_languages"]
        assert "javascript" in data["supported_languages"]
        assert data["starter_code_java"] is not None
        assert data["starter_code_javascript"] is not None

    # -------------------------------------------------------------
    # 10. Compilation / Syntax Error Handling
    # -------------------------------------------------------------
    def test_10_compilation_errors_handled_gracefully(self):
        user, token = self._create_exempt_student()
        headers = {"Authorization": f"Bearer {token}"}

        # Java compilation error
        bad_java = "class Solution { public int[] twoSum( {}}"
        res = client.post("/api/submissions/run", json={"problem_id": 1, "code": bad_java, "language": "java"}, headers=headers)
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "Compilation Error"
        assert data["compile_error"] is not None

        # JS syntax error
        bad_js = "function twoSum( {"
        res = client.post("/api/submissions/run", json={"problem_id": 1, "code": bad_js, "language": "javascript"}, headers=headers)
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "Compilation Error"
        assert data["compile_error"] is not None

    # -------------------------------------------------------------
    # 11. Runtime Error Handling
    # -------------------------------------------------------------
    def test_11_runtime_errors_handled_gracefully(self):
        user, token = self._create_exempt_student()
        headers = {"Authorization": f"Bearer {token}"}

        # JS runtime error
        throw_js = "function twoSum(nums, target) { throw new Error('Boom'); }"
        res = client.post("/api/submissions/run", json={"problem_id": 1, "code": throw_js, "language": "javascript"}, headers=headers)
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "Runtime Error"

    # -------------------------------------------------------------
    # 12. Timeout Handling
    # -------------------------------------------------------------
    def test_12_timeout_handling(self):
        user, token = self._create_exempt_student()
        headers = {"Authorization": f"Bearer {token}"}

        # Infinite loop in JS
        inf_js = "function twoSum(nums, target) { while(true){} }"
        res = client.post("/api/submissions/run", json={"problem_id": 1, "code": inf_js, "language": "javascript"}, headers=headers)
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "Time Limit Exceeded"

    # -------------------------------------------------------------
    # 13. Student Isolation Remains Intact
    # -------------------------------------------------------------
    def test_13_student_isolation_intact(self):
        user1, token1 = self._create_exempt_student()
        user2, token2 = self._create_exempt_student()

        # user1 submits
        client.post("/api/submissions/submit", json={"problem_id": 1, "code": "def twoSum(nums, target): return []", "language": "python"}, headers={"Authorization": f"Bearer {token1}"})

        # user2 checks history
        res = client.get("/api/submissions/history/1", headers={"Authorization": f"Bearer {token2}"})
        assert res.status_code == 200
        assert len(res.json()) == 0

    # -------------------------------------------------------------
    # 14. Diagnostic Gating Intact
    # -------------------------------------------------------------
    def test_14_diagnostic_gating_intact(self):
        uncompleted_user, token = self._create_uncompleted_student()
        headers = {"Authorization": f"Bearer {token}"}

        # Practice problem submission blocked with 403
        res = client.post("/api/submissions/submit", json={"problem_id": 2, "code": "def maxProfit(prices): return 0", "language": "python"}, headers=headers)
        assert res.status_code == 403
        assert "diagnostic" in res.json()["detail"].lower()

    # -------------------------------------------------------------
    # 15. Recommendation Engine Functions After Multi-Language Submission
    # -------------------------------------------------------------
    def test_15_recommendation_after_multilang_submission(self):
        user, token = self._create_exempt_student()
        headers = {"Authorization": f"Bearer {token}"}

        # Submit accepted Java solution
        java_code = """import java.util.HashMap;
import java.util.Map;

class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> map = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            if (map.containsKey(complement)) return new int[]{map.get(complement), i};
            map.put(nums[i], i);
        }
        return new int[]{};
    }
}"""
        sub_res = client.post("/api/submissions/submit", json={"problem_id": 1, "code": java_code, "language": "java"}, headers=headers)
        assert sub_res.status_code == 201

        # Check next recommendation
        rec_res = client.get("/api/recommendations/next", headers=headers)
        assert rec_res.status_code == 200
        rec_data = rec_res.json()
        assert rec_data["problem_id"] != 1  # Solved problem #1 is excluded
