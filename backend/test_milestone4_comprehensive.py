"""
Comprehensive Verification Suite for Adaptive Learning Platform - Milestones 1 to 4.
Validates:
- M1: Health & Database connection
- M2: Auth, JWT, User Profile, Onboarding Flow
- M3: Topics, Problem Catalog, Filters, Diagnostic Assessment
- M4: Code Runner, Submissions API, DB Persistence, Error Handling, Submissions History
"""
import sys
import uuid
import json
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal, check_database_connection
from app.models.problem import Problem
from app.models.submission import Submission

client = TestClient(app)

def run_tests():
    total_checks = 0
    passed_checks = 0

    def check(condition, message):
        nonlocal total_checks, passed_checks
        total_checks += 1
        if condition:
            passed_checks += 1
            print(f"  [PASS] Check #{total_checks}: {message}")
        else:
            print(f"  [FAIL] Check #{total_checks}: {message}")
            raise AssertionError(f"Check failed: {message}")

    print("=================================================================")
    print("STARTING MILESTONES 1-4 FULL VERIFICATION SUITE")
    print("=================================================================\n")

    # -------------------------------------------------------------
    # 1. MILESTONE 1: Health & Database Connectivity
    # -------------------------------------------------------------
    print("--- [M1] Health & Database Connectivity Checks ---")
    db_check = check_database_connection()
    check(db_check["connected"] is True, f"Direct MySQL connection alive: {db_check['message']}")

    res = client.get("/api/health")
    check(res.status_code == 200, f"GET /api/health returned 200 (Got {res.status_code})")
    health_data = res.json()
    check(health_data["status"] in ("ok", "healthy"), f"Health status is ok/healthy (Got {health_data.get('status')})")
    check("healthy" in health_data["database"].lower() or "connected" in health_data["database"].lower(), "Database report in health API is healthy")

    # Root endpoint check
    root_res = client.get("/")
    check(root_res.status_code == 200, "GET / root returns metadata")

    # -------------------------------------------------------------
    # 2. MILESTONE 2: Authentication & Onboarding
    # -------------------------------------------------------------
    print("\n--- [M2] Authentication & Onboarding Checks ---")
    unique_id = uuid.uuid4().hex[:8]
    test_email = f"learner_{unique_id}@test.com"
    test_password = "SecurePassword123!"
    test_name = f"Test Learner {unique_id}"

    # Register
    reg_res = client.post("/api/auth/register", json={
        "name": test_name,
        "email": test_email,
        "password": test_password
    })
    check(reg_res.status_code == 201, f"POST /api/auth/register created user (status: {reg_res.status_code})")
    token_data = reg_res.json()
    check("access_token" in token_data, "Registration returns access_token")
    auth_token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}

    # Duplicate registration rejection
    dup_res = client.post("/api/auth/register", json={
        "name": test_name,
        "email": test_email,
        "password": test_password
    })
    check(dup_res.status_code == 400, f"Duplicate registration rejected with 400 (Got {dup_res.status_code})")

    # Login
    login_res = client.post("/api/auth/login", json={
        "email": test_email,
        "password": test_password
    })
    check(login_res.status_code == 200, f"POST /api/auth/login returned 200 (status: {login_res.status_code})")
    login_token = login_res.json()["access_token"]
    check(bool(login_token), "Login token is valid")

    # GET /auth/me
    me_res = client.get("/api/auth/me", headers=headers)
    check(me_res.status_code == 200, f"GET /api/auth/me returned 200 (Got {me_res.status_code})")
    me_data = me_res.json()
    check(me_data["email"] == test_email, f"User email matches {test_email}")
    check(me_data["onboarding_completed"] is False, "New user onboarding_completed is False")

    # Submit Onboarding
    onboard_res = client.post("/api/onboarding", json={
        "learning_goal": "interview_prep",
        "experience_level": "intermediate"
    }, headers=headers)
    check(onboard_res.status_code == 200, f"POST /api/onboarding completed (status: {onboard_res.status_code})")
    onboard_data = onboard_res.json()
    check(onboard_data["learning_goal"] == "interview_prep", "Onboarding goal matches")
    check(onboard_data["experience_level"] == "intermediate", "Onboarding experience matches")

    # GET /onboarding/me
    onboard_me = client.get("/api/onboarding/me", headers=headers)
    check(onboard_me.status_code == 200, "GET /api/onboarding/me returned 200")

    # -------------------------------------------------------------
    # 3. MILESTONE 3: Problems & Diagnostic Assessment
    # -------------------------------------------------------------
    print("\n--- [M3] DSA Problem Bank & Diagnostic APIs ---")
    topics_res = client.get("/api/problems/topics")
    check(topics_res.status_code == 200, "GET /api/problems/topics returned 200")
    topics = topics_res.json()
    check(len(topics) == 10, f"Retrieved all 10 core DSA topics (Got {len(topics)})")

    problems_res = client.get("/api/problems")
    check(problems_res.status_code == 200, "GET /api/problems returned 200")
    problems = problems_res.json()
    check(len(problems) >= 35, f"Retrieved curated problem bank (Count: {len(problems)})")

    # Filter by Topic
    array_probs_res = client.get("/api/problems?topic=arrays")
    check(array_probs_res.status_code == 200, "GET /api/problems?topic=arrays returned 200")
    array_probs = array_probs_res.json()
    check(len(array_probs) >= 5, f"Arrays topic contains 5 problems (Got {len(array_probs)})")

    # Filter by Difficulty
    easy_probs_res = client.get("/api/problems?difficulty=easy")
    check(easy_probs_res.status_code == 200, "GET /api/problems?difficulty=easy returned 200")
    easy_probs = easy_probs_res.json()
    check(all(p["difficulty"] == "Easy" for p in easy_probs), "All filtered problems have Easy difficulty")

    # Problem Detail by Slug
    prob_detail_res = client.get("/api/problems/two-sum-target-pair")
    check(prob_detail_res.status_code == 200, "GET /api/problems/two-sum-target-pair returned 200")
    p1 = prob_detail_res.json()
    check("starter_code_python" in p1, "Problem detail contains starter_code_python")
    check(len(p1["visible_test_cases"]) > 0, "Problem detail contains visible test cases")

    # Diagnostic suite
    diag_res = client.get("/api/diagnostic/problems")
    check(diag_res.status_code == 200, "GET /api/diagnostic/problems returned 200")
    diag_probs = diag_res.json()
    check(len(diag_probs) >= 6, f"Diagnostic suite contains 6+ problems (Got {len(diag_probs)})")

    # Submit Diagnostic attempt
    diag_submit = client.post("/api/diagnostic/submit", json={
        "problem_id": diag_probs[0]["id"],
        "is_solved": True,
        "time_spent_seconds": 120,
        "code_submitted": "def twoSum(nums, target): return [0, 1]"
    }, headers=headers)
    check(diag_submit.status_code == 200, "POST /api/diagnostic/submit recorded attempt")

    # Complete Diagnostic
    diag_complete = client.post("/api/diagnostic/complete", headers=headers)
    check(diag_complete.status_code == 200, "POST /api/diagnostic/complete initialized prior knowledge")

    # -------------------------------------------------------------
    # 4. MILESTONE 4: Code Runner, Submissions & Execution
    # -------------------------------------------------------------
    print("\n--- [M4] Python Coding Interface & Test Case Evaluation ---")

    # 4.1 Run Code (Correct Solution)
    two_sum_correct_code = """
def twoSum(nums: list[int], target: int) -> list[int]:
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
"""
    run_res = client.post("/api/submissions/run", json={
        "problem_id": p1["id"],
        "code": two_sum_correct_code
    }, headers=headers)
    check(run_res.status_code == 200, f"POST /api/submissions/run returned 200 (status: {run_res.status_code})")
    run_data = run_res.json()
    check(run_data["status"] == "Accepted", f"Run status is Accepted (Got {run_data['status']})")
    check(run_data["passed_test_cases"] == run_data["total_test_cases"], f"All visible test cases passed ({run_data['passed_test_cases']}/{run_data['total_test_cases']})")
    check(run_data["execution_time_ms"] >= 0.0, f"Reported execution time: {run_data['execution_time_ms']} ms")

    # 4.2 Run Code (Wrong Answer)
    two_sum_wrong_code = "def twoSum(nums: list[int], target: int) -> list[int]: return [99, 99]"
    run_wrong_res = client.post("/api/submissions/run", json={
        "problem_id": p1["id"],
        "code": two_sum_wrong_code
    }, headers=headers)
    check(run_wrong_res.status_code == 200, "POST /api/submissions/run (Wrong Answer) returned 200")
    run_wrong_data = run_wrong_res.json()
    check(run_wrong_data["status"] == "Wrong Answer", f"Wrong answer detected correctly (Got {run_wrong_data['status']})")
    check(run_wrong_data["passed_test_cases"] == 0, "0 test cases passed on wrong answer")

    # 4.3 Run Code (Syntax / Compilation Error)
    syntax_error_code = "def twoSum(nums, target): return ["
    run_syntax_res = client.post("/api/submissions/run", json={
        "problem_id": p1["id"],
        "code": syntax_error_code
    }, headers=headers)
    check(run_syntax_res.status_code == 200, "POST /api/submissions/run (Syntax Error) returned 200")
    run_syntax_data = run_syntax_res.json()
    check(run_syntax_data["status"] == "Compilation Error", f"Compilation Error detected (Got {run_syntax_data['status']})")
    check(run_syntax_data["compile_error"] is not None, f"Compile error message present: {run_syntax_data['compile_error']}")

    # 4.4 Run Code (Runtime Error)
    runtime_error_code = "def twoSum(nums, target): return 1 / 0"
    run_rt_res = client.post("/api/submissions/run", json={
        "problem_id": p1["id"],
        "code": runtime_error_code
    }, headers=headers)
    check(run_rt_res.status_code == 200, "POST /api/submissions/run (Runtime Error) returned 200")
    run_rt_data = run_rt_res.json()
    check(run_rt_data["status"] == "Runtime Error", f"Runtime error detected (Got {run_rt_data['status']})")

    # 4.5 Run Code (Time Limit Exceeded - Infinite Loop)
    timeout_code = "def twoSum(nums, target):\n    while True: pass"
    run_tle_res = client.post("/api/submissions/run", json={
        "problem_id": p1["id"],
        "code": timeout_code
    }, headers=headers)
    check(run_tle_res.status_code == 200, "POST /api/submissions/run (TLE) returned 200")
    run_tle_data = run_tle_res.json()
    check(run_tle_data["status"] == "Time Limit Exceeded", f"TLE detected (Got {run_tle_data['status']})")

    # 4.6 Submit Solution (Full Test Suite Evaluation + DB Persistence)
    submit_res = client.post("/api/submissions/submit", json={
        "problem_id": p1["id"],
        "code": two_sum_correct_code
    }, headers=headers)
    check(submit_res.status_code == 201, f"POST /api/submissions/submit created submission (status: {submit_res.status_code})")
    submit_data = submit_res.json()
    check(submit_data["status"] == "Accepted", f"Submission status is Accepted (Got {submit_data['status']})")
    check(submit_data["passed_test_cases"] == submit_data["total_test_cases"], f"All test cases passed ({submit_data['passed_test_cases']}/{submit_data['total_test_cases']})")
    submission_id = submit_data["id"]

    # Verify DB persistence directly
    db = SessionLocal()
    sub_row = db.query(Submission).filter(Submission.id == submission_id).first()
    check(sub_row is not None, f"Submission #{submission_id} found in MySQL database")
    check(sub_row.status == "Accepted", "MySQL submission row status is 'Accepted'")
    check(sub_row.user_id == me_data["id"], f"MySQL submission user_id matches {me_data['id']}")
    db.close()

    # 4.7 Submission History
    history_res = client.get(f"/api/submissions/history/{p1['id']}", headers=headers)
    check(history_res.status_code == 200, f"GET /api/submissions/history/{p1['id']} returned 200")
    history_data = history_res.json()
    check(len(history_data) >= 1, f"Submission history retrieved ({len(history_data)} entries)")
    check(history_data[0]["id"] == submission_id, "Latest submission ID matches")

    # 4.8 Single Submission Detail
    detail_res = client.get(f"/api/submissions/{submission_id}", headers=headers)
    check(detail_res.status_code == 200, f"GET /api/submissions/{submission_id} returned 200")
    detail_data = detail_res.json()
    check(detail_data["id"] == submission_id, "Detail submission ID matches")

    # 4.9 Multi-Topic Evaluation Suite (Testing 5 distinct DSA topics)
    print("\n--- [M4] Multi-Topic Reference Submission Verification ---")
    multi_topic_cases = [
        ("best-time-to-buy-and-sell-stock", "def maxProfit(prices: list[int]) -> int:\n    min_p, max_p = float('inf'), 0\n    for p in prices:\n        if p < min_p: min_p = p\n        elif p - min_p > max_p: max_p = p - min_p\n    return max_p\n"),
        ("valid-anagram-check", "def isAnagram(s: str, t: str) -> bool:\n    return sorted(s) == sorted(t)\n"),
        ("reverse-linked-list", "def reverseList(head: list[int]) -> list[int]:\n    return head[::-1]\n"),
        ("maximum-depth-of-binary-tree", "def maxDepth(root: list) -> int:\n    if not root or root[0] is None: return 0\n    depth = 0\n    level = [0]\n    n = len(root)\n    while level:\n        next_level = []\n        depth += 1\n        for idx in level:\n            left, right = 2 * idx + 1, 2 * idx + 2\n            if left < n and root[left] is not None: next_level.append(left)\n            if right < n and root[right] is not None: next_level.append(right)\n        level = next_level\n    return depth\n"),
        ("climbing-stairs-min-cost", "def minCostClimbingStairs(cost: list[int]) -> int:\n    first, second = cost[0], cost[1]\n    for i in range(2, len(cost)):\n        curr = cost[i] + min(first, second)\n        first, second = second, curr\n    return min(first, second)\n"),
    ]

    for slug, code in multi_topic_cases:
        p_res = client.get(f"/api/problems/{slug}")
        check(p_res.status_code == 200, f"Loaded problem {slug}")
        prob = p_res.json()
        sub_test = client.post("/api/submissions/submit", json={
            "problem_id": prob["id"],
            "code": code
        }, headers=headers)
        check(sub_test.status_code == 201, f"Submitted solution for {slug} (status: 201)")
        sub_json = sub_test.json()
        check(sub_json["status"] == "Accepted", f"Problem {slug} passed all test cases: status = Accepted ({sub_json['passed_test_cases']}/{sub_json['total_test_cases']})")

    print("\n=================================================================")
    print(f"VERIFICATION SUMMARY: ALL {passed_checks}/{total_checks} CHECKS PASSED (100% SUCCESS)")
    print("=================================================================")

if __name__ == "__main__":
    run_tests()
