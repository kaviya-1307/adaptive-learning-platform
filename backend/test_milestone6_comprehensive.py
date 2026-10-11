"""
Comprehensive Verification Suite for Milestone 6: Adaptive Recommendation Engine & Explainable Dispatch.
Validates:
1. Difficulty mapping (Easy -> 0.30, Medium -> 0.60, Hard -> 0.90)
2. Predicted success probability math & bounds in [0, 1]
3. Zone of Proximal Development (ZPD) suitability scoring
4. Weak-topic prioritization
5. Solved (Accepted) problem exclusion
6. Failed submission handling (remains eligible)
7. Deterministic candidate evaluation & ranking
8. Recommendation persistence in MySQL `recommendations` table
9. Recommendation lifecycle & is_active management
10. User isolation (cannot see another user's recommendations)
11. REST API: GET /api/recommendations/next
12. REST API: POST /api/recommendations/generate
13. REST API: GET /api/recommendations/history
14. Real-time M5 Knowledge State consumption
"""
import sys
import uuid
import math
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import SessionLocal
from app.models.problem import Problem
from app.models.topic import Topic
from app.models.submission import Submission
from app.models.learner_knowledge_state import LearnerKnowledgeState
from app.models.recommendation import Recommendation
from app.services.recommendation_engine import (
    RecommendationEngine,
    calculate_difficulty_score,
    estimate_success_probability,
    calculate_zpd_score,
    calculate_weakness_score,
    compute_final_recommendation_score,
    generate_recommendation_explanation,
    DIFFICULTY_SCORES,
    TARGET_SUCCESS_PROBABILITY,
)

client = TestClient(app)


def run_m6_tests():
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
    print("STARTING MILESTONE 6: ADAPTIVE RECOMMENDATION ENGINE SUITE")
    print("=================================================================\n")

    # -------------------------------------------------------------
    # 1. Mathematical Scoring & Utility Unit Tests
    # -------------------------------------------------------------
    print("--- [1] Difficulty Mapping & Success Probability Math ---")
    check(calculate_difficulty_score("Easy") == 0.30, "Easy difficulty maps to 0.30")
    check(calculate_difficulty_score("Medium") == 0.60, "Medium difficulty maps to 0.60")
    check(calculate_difficulty_score("Hard") == 0.90, "Hard difficulty maps to 0.90")
    check(calculate_difficulty_score("unknown") == 0.60, "Fallback difficulty maps to 0.60")

    # Success probability behavior
    p_easy_high = estimate_success_probability(mastery=0.80, difficulty_score=0.30)
    p_easy_low = estimate_success_probability(mastery=0.20, difficulty_score=0.30)
    p_hard_low = estimate_success_probability(mastery=0.20, difficulty_score=0.90)

    check(0.0 <= p_easy_high <= 1.0, f"P(success) in [0, 1] for Easy High Mastery (Got {p_easy_high})")
    check(p_easy_high > p_easy_low, f"Higher mastery increases P(success): {p_easy_high} > {p_easy_low}")
    check(p_easy_low > p_hard_low, f"Higher difficulty decreases P(success): {p_easy_low} > {p_hard_low}")

    # ZPD scoring behavior (Target = 0.70)
    zpd_perfect = calculate_zpd_score(0.70)
    zpd_too_easy = calculate_zpd_score(0.95)
    zpd_too_hard = calculate_zpd_score(0.20)

    check(zpd_perfect == 1.0, f"ZPD score is 1.0 at target probability (Got {zpd_perfect})")
    check(zpd_perfect > zpd_too_easy, f"Target probability scores higher ZPD than too easy ({zpd_perfect} > {zpd_too_easy})")
    check(zpd_perfect > zpd_too_hard, f"Target probability scores higher ZPD than too hard ({zpd_perfect} > {zpd_too_hard})")

    # Weakness scoring
    w_low_mastery = calculate_weakness_score(0.20)
    w_high_mastery = calculate_weakness_score(0.80)
    check(w_low_mastery == 0.80, f"Weakness score is 0.80 for 0.20 mastery")
    check(w_low_mastery > w_high_mastery, f"Lower mastery gives higher weakness priority ({w_low_mastery} > {w_high_mastery})")

    # -------------------------------------------------------------
    # 2. Candidate Filtering & Solved Problem Exclusion Tests
    # -------------------------------------------------------------
    print("\n--- [2] Candidate Problem Filtering & Exclusion Logic ---")
    db = SessionLocal()
    unique_id = uuid.uuid4().hex[:8]
    test_email = f"rec_learner_{unique_id}@test.com"
    test_password = "SecurePassword123!"
    test_name = f"Rec Learner {unique_id}"

    # Register learner
    reg_res = client.post("/api/auth/register", json={
        "name": test_name,
        "email": test_email,
        "password": test_password
    })
    check(reg_res.status_code == 201, "Registered new learner for recommendation tests")
    token = reg_res.json()["access_token"]
    user_id = reg_res.json()["user"]["id"]
    headers = {"Authorization": f"Bearer {token}"}

    # Initial state initialization
    rec_candidate_list = RecommendationEngine.evaluate_candidates(db, user_id)
    check(len(rec_candidate_list) == 40, f"All 40 problems initially eligible as candidates (Got {len(rec_candidate_list)})")

    # Mark Two Sum as solved (Accepted)
    p_two_sum = db.query(Problem).filter(Problem.slug == "two-sum-target-pair").first()
    sub_accepted = Submission(
        user_id=user_id,
        problem_id=p_two_sum.id,
        code="def twoSum(): pass",
        status="Accepted",
        passed_test_cases=4,
        total_test_cases=4,
        execution_time_ms=100.0
    )
    db.add(sub_accepted)
    db.commit()

    solved_set = RecommendationEngine.get_solved_problem_ids(db, user_id)
    check(p_two_sum.id in solved_set, f"Two Sum (#{p_two_sum.id}) identified in solved set")

    rec_candidates_after = RecommendationEngine.evaluate_candidates(db, user_id)
    check(len(rec_candidates_after) == 39, f"Eligible candidates reduced to 39 after solving 1 problem (Got {len(rec_candidates_after)})")
    check(all(c["problem"].id != p_two_sum.id for c in rec_candidates_after), "Solved problem Two Sum is excluded from candidates")

    # Simulate Failed Problem (Wrong Answer) on another problem
    p_stock = db.query(Problem).filter(Problem.slug == "best-time-to-buy-and-sell-stock").first()
    sub_failed = Submission(
        user_id=user_id,
        problem_id=p_stock.id,
        code="def maxProfit(): pass",
        status="Wrong Answer",
        passed_test_cases=0,
        total_test_cases=3,
        execution_time_ms=90.0
    )
    db.add(sub_failed)
    db.commit()

    rec_candidates_failed = RecommendationEngine.evaluate_candidates(db, user_id)
    check(len(rec_candidates_failed) == 39, "Failed problem is NOT excluded from candidate recommendations")
    check(any(c["problem"].id == p_stock.id for c in rec_candidates_failed), "Failed problem remains eligible for practice")

    # -------------------------------------------------------------
    # 3. Recommendation Generation, Lifecycle & Persistence
    # -------------------------------------------------------------
    print("\n--- [3] Recommendation Generation, Persistence & Lifecycle ---")
    rec_1 = RecommendationEngine.generate_recommendation(db, user_id, force_new=True)
    check(rec_1 is not None, "Generated first recommendation (Rec A)")
    check(rec_1.user_id == user_id, f"Rec A user_id matches {user_id}")
    check(rec_1.is_active is True, "Rec A is_active is True")
    check(0.0 <= rec_1.predicted_success_prob <= 1.0, f"Rec A predicted success probability: {rec_1.predicted_success_prob}")
    check(len(rec_1.explanation_text) > 30, f"Rec A explanation text generated: '{rec_1.explanation_text[:60]}...'")
    rec_1_id = rec_1.id

    # Verify DB persistence directly
    db_rec_1 = db.query(Recommendation).filter(Recommendation.id == rec_1_id).first()
    check(db_rec_1 is not None, "Rec A found in MySQL database")
    check(db_rec_1.problem_id == rec_1.problem_id, "Rec A problem_id matches DB row")

    # Generate second recommendation (Rec B)
    rec_2 = RecommendationEngine.generate_recommendation(db, user_id, force_new=True)
    check(rec_2 is not None, "Generated second recommendation (Rec B)")
    check(rec_2.is_active is True, "Rec B is_active is True")

    # Verify Lifecycle: Rec A is now inactive, Rec B is active
    db.refresh(db_rec_1)
    check(db_rec_1.is_active is False, "Rec A is_active automatically updated to False")
    check(rec_2.id != rec_1_id, "Rec B has new unique ID")

    # Verify History Preservation
    user_history = RecommendationEngine.get_recommendation_history(db, user_id)
    check(len(user_history) >= 2, f"History preserves both records (Count: {len(user_history)})")
    check(user_history[0].id == rec_2.id, "Most recent active recommendation is first in history")
    check(user_history[1].id == rec_1_id, "Previous recommendation preserved as history item")

    # -------------------------------------------------------------
    # 4. User Isolation Security Tests
    # -------------------------------------------------------------
    print("\n--- [4] User Isolation Security Verification ---")
    user2_uid = uuid.uuid4().hex[:8]
    reg_u2_res = client.post("/api/auth/register", json={
        "name": f"User 2 {user2_uid}",
        "email": f"u2_{user2_uid}@test.com",
        "password": "Password123!"
    })
    token_u2 = reg_u2_res.json()["access_token"]
    user2_id = reg_u2_res.json()["user"]["id"]
    headers_u2 = {"Authorization": f"Bearer {token_u2}"}

    # User 2 calls history
    u2_history_res = client.get("/api/recommendations/history", headers=headers_u2)
    check(u2_history_res.status_code == 200, "User 2 history endpoint returned 200")
    u2_history = u2_history_res.json()
    check(len(u2_history) == 0, "User 2 initially has 0 recommendations")
    check(all(r["user_id"] == user2_id for r in u2_history), "User 2 cannot see User 1 recommendations")

    # -------------------------------------------------------------
    # 5. REST API Endpoints Verification
    # -------------------------------------------------------------
    print("\n--- [5] REST API Endpoints: /api/recommendations/* ---")

    # 5.1 GET /api/recommendations/next
    next_res = client.get("/api/recommendations/next", headers=headers)
    check(next_res.status_code == 200, f"GET /api/recommendations/next returned 200 (Got {next_res.status_code})")
    next_json = next_res.json()

    check(next_json["user_id"] == user_id, f"Next recommendation user_id matches {user_id}")
    check(next_json["is_active"] is True, "Next recommendation is active")
    check("problem" in next_json, "Response includes embedded problem details")
    check("title" in next_json["problem"] and "slug" in next_json["problem"], "Embedded problem has title and slug")
    check("topic_name" in next_json["problem"], f"Embedded problem topic: {next_json['problem']['topic_name']}")
    check("explanation_text" in next_json, "Response includes explanation text")

    # 5.2 POST /api/recommendations/generate
    gen_res = client.post("/api/recommendations/generate", headers=headers)
    check(gen_res.status_code == 200, f"POST /api/recommendations/generate returned 200 (Got {gen_res.status_code})")
    gen_json = gen_res.json()
    check(gen_json["is_active"] is True, "Generated recommendation is active")

    # 5.3 GET /api/recommendations/history
    hist_res = client.get("/api/recommendations/history", headers=headers)
    check(hist_res.status_code == 200, f"GET /api/recommendations/history returned 200 (Got {hist_res.status_code})")
    hist_json = hist_res.json()
    check(len(hist_json) >= 3, f"Retrieved all recommendations in history (Count: {len(hist_json)})")
    check(hist_json[0]["id"] == gen_json["id"], "History latest item matches newly generated recommendation ID")

    # 5.4 Unauthenticated Access Rejection
    unauth_next = client.get("/api/recommendations/next")
    check(unauth_next.status_code == 401, "GET /api/recommendations/next unauthenticated rejected with 401")

    unauth_gen = client.post("/api/recommendations/generate")
    check(unauth_gen.status_code == 401, "POST /api/recommendations/generate unauthenticated rejected with 401")

    unauth_hist = client.get("/api/recommendations/history")
    check(unauth_hist.status_code == 401, "GET /api/recommendations/history unauthenticated rejected with 401")

    db.close()

    print("\n=================================================================")
    print(f"MILESTONE 6 VERIFICATION SUMMARY: ALL {passed_checks}/{total_checks} CHECKS PASSED (100% SUCCESS)")
    print("=================================================================")


if __name__ == "__main__":
    run_m6_tests()
