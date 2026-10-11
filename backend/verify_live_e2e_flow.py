"""
Live End-to-End Flow Verification Script
Tests against the live running server at http://127.0.0.1:8000
Validates all requirements of Phase 18:
1. Register new user
2. Login
3. Diagnostic gate enforcement
4. Diagnostic problem description and constraints
5. Problem number and ordering
6. Multi-language support and starter codes
7. Run code execution without creating diagnostic attempt
8. Server-authoritative submission evaluation (fake is_solved rejected)
9. Successful submission marked solved
10. Diagnostic completion and score persistence
11. Retake prevention
12. Recommendation unlocked and learner-specific
13. Problem catalog sequential 1..889 verification
14. Normal practice submission
"""
import uuid
import requests
import sys

BASE_URL = "http://127.0.0.1:8000/api"

def run_e2e():
    session = requests.Session()
    uid = uuid.uuid4().hex[:8]
    email = f"e2e_user_{uid}@test.com"
    password = "StudentPass123!"
    name = f"E2E Student {uid}"

    print(f"=== 1. Register new user: {email} ===")
    reg_res = session.post(f"{BASE_URL}/auth/register", json={
        "name": name,
        "email": email,
        "password": password
    })
    assert reg_res.status_code in (200, 201), f"Registration failed: {reg_res.text}"
    token = reg_res.json().get("access_token") or reg_res.json().get("token")
    headers = {"Authorization": f"Bearer {token}"}
    print("Registration successful, JWT token received.")

    print("\n=== 2. Verify Diagnostic Gate ===")
    rec_gate = session.get(f"{BASE_URL}/recommendations/next", headers=headers)
    assert rec_gate.status_code == 403, f"Expected 403 Forbidden on ungated recommendations, got {rec_gate.status_code}"
    print("Gate verified: Recommendations access is strictly blocked (403 Forbidden) prior to diagnostic completion.")

    print("\n=== 3. Inspect Diagnostic Problems ===")
    diag_res = session.get(f"{BASE_URL}/diagnostic/problems", headers=headers)
    assert diag_res.status_code == 200, f"Failed to fetch diagnostic problems: {diag_res.text}"
    diag_probs = diag_res.json()
    assert len(diag_probs) == 7, f"Expected 7 diagnostic problems, got {len(diag_probs)}"
    
    # Check problem ordering: 1, 6, 10, 18, 21, 26, 33
    diag_ids = [p["id"] for p in diag_probs]
    print(f"Diagnostic problem IDs in order: {diag_ids}")
    assert diag_ids == [1, 6, 10, 18, 21, 26, 33], f"Unexpected diagnostic IDs order: {diag_ids}"

    # Check descriptions
    for p in diag_probs:
        assert p.get("description_markdown") is not None, f"Problem {p['id']} missing description"
        assert len(p["description_markdown"]) > 20, f"Problem {p['id']} description too short"
        assert "Write an optimal solution in Python." not in p["description_markdown"]
        print(f"Problem {p['id']} ({p['title']}): description present ({len(p['description_markdown'])} chars), supported languages: {p['supported_languages']}")

    print("\n=== 4. Test Multi-Language Starter Codes on Problem 1 ===")
    p1 = diag_probs[0]
    assert "python" in p1["supported_languages"]
    assert "java" in p1["supported_languages"]
    assert "cpp" in p1["supported_languages"]
    assert "javascript" in p1["supported_languages"]
    assert "class Solution" in p1["starter_code_java"]
    assert "class Solution" in p1["starter_code_cpp"]
    assert "function twoSum" in p1["starter_code_javascript"]
    print("Starter codes for Python, Java, C++, and JavaScript verified.")

    print("\n=== 5. Test Run Code (Does NOT create diagnostic attempt) ===")
    run_res = session.post(f"{BASE_URL}/submissions/run", headers=headers, json={
        "problem_id": 1,
        "code": "def twoSum(nums, target): return []",
        "language": "python"
    })
    assert run_res.status_code == 200
    print(f"Run code returned status: {run_res.json().get('status')}")

    # Check history endpoint to confirm 0 attempts recorded
    hist_res = session.get(f"{BASE_URL}/diagnostic/history", headers=headers)
    assert hist_res.status_code == 200
    assert len(hist_res.json()) == 0, "Run Code erroneously created a diagnostic attempt record!"
    print("Confirmed: Run Code did NOT create any diagnostic attempt.")

    print("\n=== 6. Test Server-Authoritative Evaluation (Submit fake is_solved) ===")
    # Client sends is_solved=True with empty or wrong code
    fake_sub = session.post(f"{BASE_URL}/diagnostic/submit", headers=headers, json={
        "problem_id": 1,
        "is_solved": True,
        "code_submitted": "def twoSum(nums, target): return []",
        "language": "python",
        "time_spent_seconds": 15
    })
    assert fake_sub.status_code == 200
    fake_data = fake_sub.json()
    assert fake_data["is_solved"] is False, "Server trusted fake is_solved=True with failing code!"
    print("Confirmed: Server authoritative evaluation rejected fake is_solved=True and marked is_solved=False.")

    print("\n=== 7. Submit Genuine Solution for Problem 1 ===")
    correct_p1_py = """def twoSum(nums: list[int], target: int) -> list[int]:
    seen = {}
    for i, num in enumerate(nums):
        diff = target - num
        if diff in seen:
            return [seen[diff], i]
        seen[num] = i
    return []
"""
    good_sub = session.post(f"{BASE_URL}/diagnostic/submit", headers=headers, json={
        "problem_id": 1,
        "code_submitted": correct_p1_py,
        "language": "python",
        "time_spent_seconds": 30
    })
    assert good_sub.status_code == 200
    good_data = good_sub.json()
    assert good_data["is_solved"] is True, f"Correct solution was not marked solved: {good_data}"
    print("Confirmed: Server evaluated genuine code and marked is_solved=True.")

    print("\n=== 8. Submit Remaining Diagnostic Problems and Complete Assessment ===")
    # Submit for the remaining 6 problems
    for p in diag_probs[1:]:
        session.post(f"{BASE_URL}/diagnostic/submit", headers=headers, json={
            "problem_id": p["id"],
            "code_submitted": "def solve(): return None",
            "language": "python",
            "time_spent_seconds": 20
        })

    comp_res = session.post(f"{BASE_URL}/diagnostic/complete", headers=headers)
    assert comp_res.status_code == 200, f"Complete diagnostic failed: {comp_res.text}"
    comp_data = comp_res.json()
    print(f"Diagnostic completion result: {comp_data}")
    assert comp_data["total_problems"] == 7
    assert comp_data["solved_count"] == 1
    assert comp_data["score_percent"] == 14.3

    print("\n=== 9. Verify Retake Prevention ===")
    retake_sub = session.post(f"{BASE_URL}/diagnostic/submit", headers=headers, json={
        "problem_id": 1,
        "code_submitted": "def twoSum(): pass",
        "language": "python"
    })
    assert retake_sub.status_code == 400, "Completed student was able to submit diagnostic attempt!"
    print("Confirmed: Completed diagnostic cannot be retaken (HTTP 400).")

    print("\n=== 10. Verify Recommendations Unlocked & Reflect Learner State ===")
    next_rec = session.get(f"{BASE_URL}/recommendations/next", headers=headers)
    assert next_rec.status_code == 200, f"Recommendations still blocked after completion: {next_rec.text}"
    rec_data = next_rec.json()
    print(f"Recommended Problem: ID={rec_data['problem']['id']}, Title='{rec_data['problem']['title']}', Concept={rec_data['primary_weak_concept']}, Score={rec_data['recommendation_score']}")
    assert rec_data["problem"]["id"] != 1, "Recommended problem should not be already solved problem 1!"

    print("\n=== 11. Verify Problem Catalog (Exactly 889 Problems, Sequential 1..889) ===")
    cat_res = session.get(f"{BASE_URL}/problems?limit=1000", headers=headers)
    assert cat_res.status_code == 200
    problems = cat_res.json()
    print(f"Total problems returned by catalog: {len(problems)}")
    assert len(problems) == 889, f"Expected 889 problems in catalog, got {len(problems)}"

    order_indices = [p["order_index"] for p in problems]
    ids = [p["id"] for p in problems]
    assert order_indices == list(range(1, 890)), f"Catalog order_indices are not sequential 1..889!"
    assert ids == list(range(1, 890)), f"Catalog IDs are not sequential 1..889!"
    print("Catalog Integrity Verified: Exactly 889 problems, sequential 1 to 889 without gaps, duplicates, or misordering.")

    print("\n=== 12. Verify Practice Submission on Recommended Problem ===")
    rec_pid = rec_data["problem"]["id"]
    prac_sub = session.post(f"{BASE_URL}/submissions/submit", headers=headers, json={
        "problem_id": rec_pid,
        "code": "def solve(): return None",
        "language": "python"
    })
    assert prac_sub.status_code in (200, 201), f"Practice submission failed: {prac_sub.text}"
    print(f"Practice submission recorded successfully: status={prac_sub.json().get('status')}")

    print("\n=======================================================")
    print(">>> ALL LIVE END-TO-END FLOW CHECKS PASSED PERFECTLY <<<")
    print("=======================================================")

if __name__ == "__main__":
    run_e2e()
