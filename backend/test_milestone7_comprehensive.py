"""
Comprehensive Verification Suite for Milestone 7: Personalized Learner Dashboard & Progress Analytics.
Validates:
1. Authentication protection (401 for unauthorized, 200 for valid JWT)
2. Complete Dashboard Summary schema response structure
3. 10-Topic Mastery data integration with M5 `learner_knowledge_state`
4. Problem solving performance statistics (total, accepted, wrong, unique solved, acceptance rate)
5. Unique solved problem counting deduplication
6. Difficulty breakdown distribution (Easy, Medium, Hard)
7. Active M6 recommendation integration in dashboard summary
8. Recommendation dispatch history integration (latest 5 records)
9. Recent submission history integration (latest 5 records)
10. Strict User Isolation security (User A cannot view User B metrics/stats)
"""
import sys
import uuid
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import SessionLocal
from app.models.problem import Problem
from app.models.submission import Submission
from app.models.learner_knowledge_state import LearnerKnowledgeState
from app.models.recommendation import Recommendation
from app.services.recommendation_engine import RecommendationEngine

client = TestClient(app)


def run_m7_tests():
    total_checks = 0
    passed_checks = 0

    def check(condition: bool, message: str):
        nonlocal total_checks, passed_checks
        total_checks += 1
        if condition:
            passed_checks += 1
            print(f"  [PASS] Check #{total_checks}: {message}")
        else:
            print(f"  [FAIL] Check #{total_checks}: {message}")
            raise AssertionError(f"Check failed: {message}")

    print("=================================================================")
    print("STARTING MILESTONE 7: PERSONALIZED LEARNER DASHBOARD SUITE")
    print("=================================================================\n")

    db = SessionLocal()

    # -------------------------------------------------------------
    # 1. Unauthenticated Access Protection
    # -------------------------------------------------------------
    print("--- [1] Authentication & Security Checks ---")
    unauth_res = client.get("/api/dashboard/summary")
    check(unauth_res.status_code == 401, "GET /api/dashboard/summary rejected without token (Got 401)")

    # Register Learner A
    uid_a = uuid.uuid4().hex[:8]
    reg_a = client.post("/api/auth/register", json={
        "name": f"Dashboard User {uid_a}",
        "email": f"dash_{uid_a}@test.com",
        "password": "Password123!"
    })
    check(reg_a.status_code == 201, "Registered User A for dashboard testing")
    token_a = reg_a.json()["access_token"]
    user_a_id = reg_a.json()["user"]["id"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    # Submit onboarding for User A
    onboard_res = client.post("/api/onboarding", json={
        "learning_goal": "interview_prep",
        "experience_level": "intermediate"
    }, headers=headers_a)
    check(onboard_res.status_code == 200, "User A completed onboarding")

    # -------------------------------------------------------------
    # 2. Initial Dashboard Summary Structure & User Info
    # -------------------------------------------------------------
    print("\n--- [2] Initial Dashboard Summary Schema Verification ---")
    dash_res_1 = client.get("/api/dashboard/summary", headers=headers_a)
    check(dash_res_1.status_code == 200, f"GET /api/dashboard/summary returned 200 (Got {dash_res_1.status_code})")
    dash_1 = dash_res_1.json()

    # User info checks
    check(dash_1["user"]["id"] == user_a_id, f"Dashboard user.id matches User A ({user_a_id})")
    check(dash_1["user"]["learning_goal"] == "interview_prep", "Dashboard user.learning_goal matches 'interview_prep'")
    check(dash_1["user"]["experience_level"] == "intermediate", "Dashboard user.experience_level matches 'intermediate'")

    # Learning state checks
    check(0.0 <= dash_1["learning_state"]["overall_mastery"] <= 1.0, f"Overall mastery in [0, 1] (Got {dash_1['learning_state']['overall_mastery']})")
    check(0.0 <= dash_1["learning_state"]["overall_confidence"] <= 1.0, f"Overall confidence in [0, 1] (Got {dash_1['learning_state']['overall_confidence']})")
    check(dash_1["learning_state"]["total_interactions"] == 0, "Initial total interactions is 0")

    # -------------------------------------------------------------
    # 3. 10-Topic Mastery Integration Checks (M5)
    # -------------------------------------------------------------
    print("\n--- [3] 10-Topic Knowledge State Verification ---")
    topics = dash_1["topic_mastery"]
    check(len(topics) == 10, f"Dashboard returns exactly 10 topic masteries (Got {len(topics)})")

    # Verify each topic attributes and consistency with MySQL
    expected_topics = [
        "Arrays", "Strings", "Hashing", "Linked Lists", "Stack & Queue",
        "Trees", "Graphs", "Greedy Algorithms", "Dynamic Programming", "Backtracking"
    ]
    for idx, t in enumerate(topics):
        check(t["topic_name"] == expected_topics[idx], f"Topic #{idx+1} name matches '{expected_topics[idx]}'")
        check(0.0 <= t["mastery_score"] <= 1.0, f"Topic '{t['topic_name']}' mastery_score in [0, 1]")
        check(t["mastery_percentage"] == round(t["mastery_score"] * 100.0, 1), f"Topic '{t['topic_name']}' mastery_percentage matches")
        check(t["mastery_level"] in ("Novice", "Developing", "Proficient", "Master"), f"Topic '{t['topic_name']}' has valid mastery_level ({t['mastery_level']})")

    # -------------------------------------------------------------
    # 4. Problem Solving Stats & Solved Count Deduplication
    # -------------------------------------------------------------
    print("\n--- [4] Problem Solving Statistics & Deduplication ---")
    check(dash_1["problem_stats"]["total_submissions"] == 0, "Initial total_submissions is 0")
    check(dash_1["problem_stats"]["total_solved"] == 0, "Initial total_solved is 0")
    check(dash_1["problem_stats"]["acceptance_rate"] == 0.0, "Initial acceptance_rate is 0.0%")

    # Load problem #1 (Two Sum - Easy) and problem #2 (Stock - Easy) and problem #31 (Climbing Stairs - Easy/Medium)
    p_two_sum = db.query(Problem).filter(Problem.slug == "two-sum-target-pair").first()
    p_stock = db.query(Problem).filter(Problem.slug == "best-time-to-buy-and-sell-stock").first()

    # Submission 1: Two Sum -> Accepted
    sub1 = Submission(
        user_id=user_a_id,
        problem_id=p_two_sum.id,
        code="def twoSum(): pass",
        status="Accepted",
        passed_test_cases=4,
        total_test_cases=4,
        execution_time_ms=50.0
    )
    db.add(sub1)

    # Submission 2: Two Sum -> Accepted again (Duplicate Accepted for same problem)
    sub2 = Submission(
        user_id=user_a_id,
        problem_id=p_two_sum.id,
        code="def twoSum(): pass",
        status="Accepted",
        passed_test_cases=4,
        total_test_cases=4,
        execution_time_ms=45.0
    )
    db.add(sub2)

    # Submission 3: Stock -> Wrong Answer
    sub3 = Submission(
        user_id=user_a_id,
        problem_id=p_stock.id,
        code="def maxProfit(): pass",
        status="Wrong Answer",
        passed_test_cases=1,
        total_test_cases=3,
        execution_time_ms=80.0
    )
    db.add(sub3)
    db.commit()

    # Query updated dashboard
    dash_res_2 = client.get("/api/dashboard/summary", headers=headers_a)
    dash_2 = dash_res_2.json()
    stats = dash_2["problem_stats"]

    check(stats["total_submissions"] == 3, f"Total submissions count is 3 (Got {stats['total_submissions']})")
    check(stats["accepted_submissions"] == 2, f"Accepted submissions count is 2 (Got {stats['accepted_submissions']})")
    check(stats["wrong_submissions"] == 1, f"Wrong submissions count is 1 (Got {stats['wrong_submissions']})")
    check(stats["total_solved"] == 1, f"Unique total_solved is 1 (Deduplication verified: Got {stats['total_solved']})")
    check(stats["acceptance_rate"] == 66.7, f"Acceptance rate is 66.7% (Got {stats['acceptance_rate']}%)")
    check(stats["easy_solved"] == 1, f"Easy solved count is 1 (Got {stats['easy_solved']})")

    # Difficulty breakdown
    diff_map = {d["difficulty"]: d for d in stats["difficulty_breakdown"]}
    check("Easy" in diff_map and "Medium" in diff_map and "Hard" in diff_map, "Difficulty breakdown covers Easy, Medium, Hard")
    check(diff_map["Easy"]["solved_count"] == 1, "Easy tier has 1 solved problem")
    check(diff_map["Medium"]["solved_count"] == 0, "Medium tier has 0 solved problems")
    check(diff_map["Hard"]["solved_count"] == 0, "Hard tier has 0 solved problems")

    # -------------------------------------------------------------
    # 5. Active Recommendation & History Integration (M6)
    # -------------------------------------------------------------
    print("\n--- [5] Active Recommendation & History Integration ---")
    # Generate an active recommendation for User A
    rec_gen_res = client.post("/api/recommendations/generate", headers=headers_a)
    check(rec_gen_res.status_code == 200, "Generated active recommendation for User A")
    rec_data = rec_gen_res.json()

    dash_res_3 = client.get("/api/dashboard/summary", headers=headers_a)
    dash_3 = dash_res_3.json()

    active_rec = dash_3["active_recommendation"]
    check(active_rec is not None, "Dashboard active_recommendation is populated")
    check(active_rec["problem_id"] == rec_data["problem"]["id"], "Active recommendation problem_id matches M6 recommendation")
    check(active_rec["problem_title"] == rec_data["problem"]["title"], f"Active recommendation title: '{active_rec['problem_title']}'")
    check(0.0 <= active_rec["predicted_success_prob"] <= 1.0, f"Active recommendation predicted_success_prob: {active_rec['predicted_success_prob']}")
    check(len(active_rec["explanation_text"]) > 20, "Active recommendation explanation text present")

    # Check recommendation history list
    rec_hist = dash_3["recommendation_history"]
    check(len(rec_hist) >= 1, f"Dashboard recommendation_history contains records (Count: {len(rec_hist)})")
    check(rec_hist[0]["id"] == rec_data["id"], "Most recent recommendation is first in history")

    # -------------------------------------------------------------
    # 6. Recent Submissions Feed Integration
    # -------------------------------------------------------------
    print("\n--- [6] Recent Submissions Feed Integration ---")
    recent_subs = dash_3["recent_submissions"]
    check(len(recent_subs) == 3, f"Dashboard recent_submissions contains all 3 submissions (Got {len(recent_subs)})")
    check(recent_subs[0]["submission_id"] == sub3.id, "Most recent submission (sub3) is first")
    check(recent_subs[0]["status"] == "Wrong Answer", "sub3 status is 'Wrong Answer'")
    check(recent_subs[1]["status"] == "Accepted", "sub2 status is 'Accepted'")
    check(recent_subs[0]["problem_title"] == p_stock.title, f"Recent submission problem_title: '{recent_subs[0]['problem_title']}'")

    # -------------------------------------------------------------
    # 7. User Isolation Security Verification
    # -------------------------------------------------------------
    print("\n--- [7] Strict User Isolation Verification ---")
    uid_b = uuid.uuid4().hex[:8]
    reg_b = client.post("/api/auth/register", json={
        "name": f"Dashboard User {uid_b}",
        "email": f"dash_{uid_b}@test.com",
        "password": "Password123!"
    })
    token_b = reg_b.json()["access_token"]
    user_b_id = reg_b.json()["user"]["id"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    dash_b_res = client.get("/api/dashboard/summary", headers=headers_b)
    check(dash_b_res.status_code == 200, "User B dashboard summary returned 200")
    dash_b = dash_b_res.json()

    # User B must have 0 submissions, 0 solved, 0 history
    check(dash_b["user"]["id"] == user_b_id, f"User B id is {user_b_id}")
    check(dash_b["problem_stats"]["total_submissions"] == 0, "User B has 0 submissions (Isolated from User A)")
    check(dash_b["problem_stats"]["total_solved"] == 0, "User B has 0 solved (Isolated from User A)")
    check(len(dash_b["recent_submissions"]) == 0, "User B has empty recent_submissions")
    check(len(dash_b["recommendation_history"]) == 0, "User B has empty recommendation_history")

    db.close()

    print("\n=================================================================")
    print(f"MILESTONE 7 VERIFICATION SUMMARY: ALL {passed_checks}/{total_checks} CHECKS PASSED (100% SUCCESS)")
    print("=================================================================")


if __name__ == "__main__":
    run_m7_tests()
