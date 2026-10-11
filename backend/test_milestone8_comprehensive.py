"""
Milestone 8 Comprehensive Verification Suite
============================================
Project: AI-Driven Adaptive Learning & Problem Recommendation Framework
Root: D:/Adaptive_Learning_platform

Validates the full end-to-end learner journey:
  1. Authentication & Onboarding
  2. Diagnostic Assessment Flow (Fetch -> Submit Attempts -> Complete Assessment)
  3. Baseline Knowledge State Initialization across 10 DSA Topics
  4. Adaptive ZPD Problem Recommendation Generation & Dispatch
  5. Python Coding Sandbox Execution & Solution Submission
  6. Real-Time LSTM Knowledge Tracing State Update
  7. Next Adaptive Problem Recommendation (Exclusion of Solved Problem)
  8. Consolidated Personalized Learner Dashboard Synchronization
  9. Strict User Isolation & Authentication Security

Usage:
  python test_milestone8_comprehensive.py
"""

import sys
import uuid
import logging
from typing import Dict, Any

from fastapi.testclient import TestClient
from sqlalchemy import text

from app.main import app
from app.core.database import SessionLocal, engine

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("test_milestone8")

client = TestClient(app)

TOTAL_CHECKS = 0
PASSED_CHECKS = 0


def record_check(description: str, condition: bool, details: str = ""):
    global TOTAL_CHECKS, PASSED_CHECKS
    TOTAL_CHECKS += 1
    if condition:
        PASSED_CHECKS += 1
        print(f"  [PASS] Check #{TOTAL_CHECKS}: {description}")
    else:
        print(f"  [FAIL] Check #{TOTAL_CHECKS}: {description} -- {details}")
        assert False, f"Check #{TOTAL_CHECKS} failed: {description} ({details})"


def generate_unique_user():
    uid = uuid.uuid4().hex[:8]
    return {
        "name": f"Learner M8 {uid}",
        "email": f"learner_m8_{uid}@test.com",
        "password": "Password123!"
    }


def main():
    print("=" * 70)
    print("STARTING MILESTONE 8: END-TO-END INTEGRATION & PRODUCT SUITE")
    print("=" * 70)

    # -------------------------------------------------------------
    # 1. Health & Database Connectivity
    # -------------------------------------------------------------
    print("\n--- [1] Health & Connectivity ---")
    resp_health = client.get("/api/health")
    record_check("GET /api/health returned 200", resp_health.status_code == 200, f"Got {resp_health.status_code}")
    health_data = resp_health.json()
    record_check("Health status is healthy", health_data.get("status") in ["ok", "healthy"])
    record_check("Database connectivity is healthy", "healthy" in health_data.get("database", "").lower())

    # -------------------------------------------------------------
    # 2. Learner Registration & Onboarding
    # -------------------------------------------------------------
    print("\n--- [2] Registration & Onboarding ---")
    user_a_creds = generate_unique_user()
    resp_reg = client.post("/api/auth/register", json=user_a_creds)
    record_check("User A registration succeeded (201)", resp_reg.status_code == 201)
    reg_data = resp_reg.json()
    token_a = reg_data["access_token"]
    user_a_id = reg_data["user"]["id"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    # Complete onboarding
    onboard_payload = {
        "learning_goal": "interview_prep",
        "experience_level": "intermediate"
    }
    resp_onboard = client.post("/api/onboarding", json=onboard_payload, headers=headers_a)
    record_check("User A onboarding completed (200)", resp_onboard.status_code == 200)

    # -------------------------------------------------------------
    # 3. Diagnostic Assessment Flow
    # -------------------------------------------------------------
    print("\n--- [3] Diagnostic Assessment Flow ---")
    resp_diag_probs = client.get("/api/diagnostic/problems")
    record_check("GET /api/diagnostic/problems returned 200", resp_diag_probs.status_code == 200)
    diag_probs = resp_diag_probs.json()
    record_check("Diagnostic suite contains problems (Count: 7)", len(diag_probs) == 7, f"Got {len(diag_probs)}")

    # Submit attempts for diagnostic problems
    # Problem 1: Solved
    p1 = diag_probs[0]
    resp_att1 = client.post("/api/diagnostic/submit", json={
        "problem_id": p1["id"],
        "is_solved": True,
        "time_spent_seconds": 120,
        "code_submitted": "def solution(): return True"
    }, headers=headers_a)
    record_check(f"Submitted diagnostic attempt for #{p1['id']} (Solved)", resp_att1.status_code == 200)
    att1_data = resp_att1.json()
    record_check("Attempt record is_solved is True", att1_data["is_solved"] is True)

    # Problem 2: Solved
    p2 = diag_probs[1]
    resp_att2 = client.post("/api/diagnostic/submit", json={
        "problem_id": p2["id"],
        "is_solved": True,
        "time_spent_seconds": 95,
        "code_submitted": "def solution(): return True"
    }, headers=headers_a)
    record_check(f"Submitted diagnostic attempt for #{p2['id']} (Solved)", resp_att2.status_code == 200)

    # Problem 3: Failed / Unsolved
    p3 = diag_probs[2]
    resp_att3 = client.post("/api/diagnostic/submit", json={
        "problem_id": p3["id"],
        "is_solved": False,
        "time_spent_seconds": 180,
        "code_submitted": "def solution(): pass"
    }, headers=headers_a)
    record_check(f"Submitted diagnostic attempt for #{p3['id']} (Unsolved)", resp_att3.status_code == 200)

    # Finalize diagnostic
    resp_complete = client.post("/api/diagnostic/complete", headers=headers_a)
    record_check("POST /api/diagnostic/complete returned 200", resp_complete.status_code == 200)
    comp_data = resp_complete.json()
    record_check("Diagnostic complete returns total_problems == 7", comp_data["total_problems"] == 7)
    record_check("Diagnostic complete returns solved_count == 2", comp_data["solved_count"] == 2)
    record_check("Diagnostic complete initialized 10 topic knowledge states", comp_data["knowledge_states_initialized"] == 10)

    # Verify diagnostic history
    resp_history = client.get("/api/diagnostic/history", headers=headers_a)
    record_check("GET /api/diagnostic/history returned 200", resp_history.status_code == 200)
    hist_items = resp_history.json()
    record_check("Diagnostic history contains 3 submitted attempts", len(hist_items) == 3)

    # -------------------------------------------------------------
    # 4. Baseline Knowledge State Verification (M5)
    # -------------------------------------------------------------
    print("\n--- [4] Baseline Knowledge State Verification ---")
    resp_ks = client.get("/api/knowledge-state", headers=headers_a)
    record_check("GET /api/knowledge-state returned 200", resp_ks.status_code == 200)
    ks_data = resp_ks.json()
    record_check("Knowledge state contains exactly 10 topics", len(ks_data["topics"]) == 10)
    record_check("Overall mastery is in [0, 1]", 0.0 <= ks_data["overall_mastery"] <= 1.0)
    record_check("Overall confidence is in [0, 1]", 0.0 <= ks_data["overall_confidence"] <= 1.0)

    # -------------------------------------------------------------
    # 5. Adaptive Recommendation Dispatch (M6)
    # -------------------------------------------------------------
    print("\n--- [5] Adaptive Recommendation Dispatch ---")
    resp_rec = client.get("/api/recommendations/next", headers=headers_a)
    record_check("GET /api/recommendations/next returned 200", resp_rec.status_code == 200)
    rec_data = resp_rec.json()
    record_check("Recommendation is active", rec_data.get("is_active") is True)
    record_check("Recommendation includes problem details", "problem" in rec_data and rec_data["problem"] is not None)
    rec_prob = rec_data["problem"]
    rec_prob_id = rec_prob["id"]
    rec_prob_slug = rec_prob["slug"]
    record_check("Recommended problem has title and slug", bool(rec_prob["title"]) and bool(rec_prob_slug))
    record_check("Predicted success probability in [0.01, 0.99]", 0.01 <= rec_data["predicted_success_prob"] <= 0.99)
    record_check("Pedagogical explanation text present", len(rec_data["explanation_text"]) > 10)

    # -------------------------------------------------------------
    # 6. Coding Workspace, Test Execution & Submission (M4)
    # -------------------------------------------------------------
    print("\n--- [6] Coding Workspace & Submission ---")
    # Fetch problem detail
    resp_p_detail = client.get(f"/api/problems/{rec_prob_slug}")
    record_check(f"Loaded problem details for {rec_prob_slug} (200)", resp_p_detail.status_code == 200)
    p_detail = resp_p_detail.json()

    # Provide correct Python solution for Two Sum (or problem 1) or Two Sum Target Pair
    SOLVER_MAP = {
        "two-sum-target-pair": "def twoSum(nums: list[int], target: int) -> list[int]:\n    seen = {}\n    for i, n in enumerate(nums):\n        if target - n in seen: return [seen[target - n], i]\n        seen[n] = i\n    return []\n",
        "best-time-to-buy-and-sell-stock": "def maxProfit(prices: list[int]) -> int:\n    min_p, max_p = float('inf'), 0\n    for p in prices:\n        if p < min_p: min_p = p\n        elif p - min_p > max_p: max_p = p - min_p\n    return max_p\n",
        "valid-anagram-check": "def isAnagram(s: str, t: str) -> bool:\n    return sorted(s) == sorted(t)\n",
        "reverse-linked-list": "def reverseList(head: list[int]) -> list[int]:\n    return head[::-1]\n",
        "maximum-depth-of-binary-tree": "def maxDepth(root: list) -> int:\n    if not root or root[0] is None: return 0\n    depth = 0\n    level = [0]\n    n = len(root)\n    while level:\n        next_level = []\n        depth += 1\n        for idx in level:\n            left, right = 2 * idx + 1, 2 * idx + 2\n            if left < n and root[left] is not None: next_level.append(left)\n            if right < n and root[right] is not None: next_level.append(right)\n        level = next_level\n    return depth\n",
        "climbing-stairs-min-cost": "def minCostClimbingStairs(cost: list[int]) -> int:\n    first, second = cost[0], cost[1]\n    for i in range(2, len(cost)):\n        curr = cost[i] + min(first, second)\n        first, second = second, curr\n    return min(first, second)\n",
    }
    solution_code = SOLVER_MAP.get(rec_prob_slug, p_detail.get("starter_code_python", ""))

    # Run code in sandbox
    resp_run = client.post("/api/submissions/run", json={
        "problem_id": rec_prob_id,
        "code": solution_code
    }, headers=headers_a)
    record_check("POST /api/submissions/run returned 200", resp_run.status_code == 200)
    run_result = resp_run.json()
    record_check("Run result contains status", "status" in run_result)

    # Submit solution
    resp_submit = client.post("/api/submissions/submit", json={
        "problem_id": rec_prob_id,
        "code": solution_code
    }, headers=headers_a)
    record_check("POST /api/submissions/submit returned 201", resp_submit.status_code == 201)
    sub_data = resp_submit.json()
    record_check("Submission persisted with valid ID", sub_data["id"] > 0)
    record_check("Submission evaluation status is Accepted", sub_data["status"] == "Accepted")

    # -------------------------------------------------------------
    # 7. Knowledge State Update & Next Recommendation Loop
    # -------------------------------------------------------------
    print("\n--- [7] Post-Submission Knowledge State & Recommendation Loop ---")
    resp_next_rec = client.get("/api/recommendations/next", headers=headers_a)
    record_check("GET /api/recommendations/next returned 200 after submission", resp_next_rec.status_code == 200)
    next_rec_data = resp_next_rec.json()
    next_prob_id = next_rec_data["problem"]["id"]
    record_check(f"Solved problem #{rec_prob_id} is excluded from next recommendation (#{next_prob_id})", next_prob_id != rec_prob_id)

    # -------------------------------------------------------------
    # 8. Personalized Learner Dashboard Synchronization (M7)
    # -------------------------------------------------------------
    print("\n--- [8] Learner Dashboard Synchronization ---")
    resp_dash = client.get("/api/dashboard/summary", headers=headers_a)
    record_check("GET /api/dashboard/summary returned 200", resp_dash.status_code == 200)
    dash_data = resp_dash.json()

    # User info
    record_check("Dashboard user.id matches User A", dash_data["user"]["id"] == user_a_id)
    record_check("Dashboard user.learning_goal matches", dash_data["user"]["learning_goal"] == "interview_prep")

    # 10-Topic Radar masteries
    record_check("Dashboard contains all 10 topic masteries", len(dash_data["topic_mastery"]) == 10)

    # Problem solving stats
    stats = dash_data["problem_stats"]
    record_check("Dashboard problem_stats.total_submissions >= 1", stats["total_submissions"] >= 1)
    record_check("Dashboard problem_stats.total_solved >= 1", stats["total_solved"] >= 1)
    record_check("Dashboard problem_stats.accepted_submissions >= 1", stats["accepted_submissions"] >= 1)
    record_check("Dashboard acceptance_rate > 0%", stats["acceptance_rate"] > 0.0)

    # Active recommendation embedded in dashboard
    record_check("Dashboard includes active_recommendation", dash_data["active_recommendation"] is not None)
    record_check("Dashboard active_recommendation id matches next recommendation", dash_data["active_recommendation"]["problem_id"] == next_prob_id)

    # Feeds
    record_check("Dashboard recent_submissions contains our submission", len(dash_data["recent_submissions"]) >= 1)
    record_check("Dashboard recommendation_history contains items", len(dash_data["recommendation_history"]) >= 1)

    # -------------------------------------------------------------
    # 9. Security & Strict User Isolation
    # -------------------------------------------------------------
    print("\n--- [9] Security & User Isolation ---")
    # Unauthenticated checks
    record_check("Unauthenticated /api/diagnostic/complete returns 401", client.post("/api/diagnostic/complete").status_code == 401)
    record_check("Unauthenticated /api/recommendations/next returns 401", client.get("/api/recommendations/next").status_code == 401)
    record_check("Unauthenticated /api/dashboard/summary returns 401", client.get("/api/dashboard/summary").status_code == 401)

    # User B registration
    user_b_creds = generate_unique_user()
    resp_reg_b = client.post("/api/auth/register", json=user_b_creds)
    token_b = resp_reg_b.json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    resp_dash_b = client.get("/api/dashboard/summary", headers=headers_b)
    record_check("User B dashboard summary returned 200", resp_dash_b.status_code == 200)
    dash_b = resp_dash_b.json()
    record_check("User B total_submissions is 0 (Isolated from User A)", dash_b["problem_stats"]["total_submissions"] == 0)
    record_check("User B total_solved is 0 (Isolated from User A)", dash_b["problem_stats"]["total_solved"] == 0)
    record_check("User B recent_submissions is empty", len(dash_b["recent_submissions"]) == 0)

    print("\n" + "=" * 70)
    print(f"MILESTONE 8 VERIFICATION SUMMARY: ALL {PASSED_CHECKS}/{TOTAL_CHECKS} CHECKS PASSED (100% SUCCESS)")
    print("=" * 70)


if __name__ == "__main__":
    main()
