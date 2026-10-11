"""
Phase 3 Step 1 Verification Suite: Final Adaptive Recommendation Integration.
Tests the complete end-to-end adaptive recommendation pipeline:

Pipeline 1: New User Journey
  Registration
  -> Diagnostic Test
  -> Concept-wise learner state initialization (37 Codeforces learning concepts)
  -> Personalized Roadmap (Stage unlocking, concept priorities)
  -> Personalized Problem Recommendation (0.60*gap + 0.40*fit, diversity-aware)

Pipeline 2: Existing User Journey
  Login
  -> Current Concept-wise Learner State
  -> Personalized Roadmap
  -> Personalized Problem Recommendation (fresh state, no stale cache)

Pipeline 3: Post-Problem Submission Loop
  Submission (Accepted & Failed)
  -> Evaluate submission
  -> Update learner concept state (Bayesian mastery, weakness, confidence)
  -> Recalculate weakness/mastery
  -> Automatically generate the next personalized recommendation
  -> Exclude all attempted problems

Pipeline 4: Cold-Start & Multi-User Isolation
  -> Cold-start user receives valid recommendations without fake history
  -> Multiple users remain strictly isolated across states, roadmaps, recommendations
"""
import uuid
import math
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import SessionLocal
from app.models.user import User
from app.models.problem import Problem
from app.models.submission import Submission
from app.models.diagnostic_attempt import DiagnosticAttempt
from app.models.learner_concept_state import LearnerConceptState
from app.models.recommendation import Recommendation
from app.services.recommendation_engine import (
    RecommendationEngine,
    calculate_difficulty_fit,
    compute_recommendation_score,
    TOP_K,
    MAX_SAME_PRIMARY_CONCEPT,
)
from app.ml.state_engine import (
    KnowledgeStateEngine,
    get_problem_learning_concepts,
)
from app.ml.roadmap_engine import AdaptiveRoadmapEngine

client = TestClient(app)

TOTAL_CHECKS = 0
PASSED_CHECKS = 0


def check(condition: bool, message: str):
    global TOTAL_CHECKS, PASSED_CHECKS
    TOTAL_CHECKS += 1
    if condition:
        PASSED_CHECKS += 1
        print(f"  [PASS] Check #{TOTAL_CHECKS}: {message}")
    else:
        print(f"  [FAIL] Check #{TOTAL_CHECKS}: {message}")
        raise AssertionError(f"Check #{TOTAL_CHECKS} failed: {message}")


def test_phase3_step1_pipeline():
    print("=======================================================================")
    print("RUNNING PHASE 3 — STEP 1: FINAL ADAPTIVE RECOMMENDATION INTEGRATION")
    print("=======================================================================\n")

    db = SessionLocal()

    # -------------------------------------------------------------
    # 1. New User Journey: Registration -> Diagnostic -> Concepts -> Roadmap -> Rec
    # -------------------------------------------------------------
    print("--- [1] New User Pipeline: Registration to Initial Recommendation ---")
    uid_1 = uuid.uuid4().hex[:8]
    reg_res = client.post("/api/auth/register", json={
        "name": f"New Learner {uid_1}",
        "email": f"new_learner_{uid_1}@test.com",
        "password": "Password123!"
    })
    check(reg_res.status_code == 201, "New user registration succeeded (201)")
    token_1 = reg_res.json()["access_token"]
    user_id_1 = reg_res.json()["user"]["id"]
    headers_1 = {"Authorization": f"Bearer {token_1}"}

    # Onboarding
    onboard_res = client.post("/api/onboarding", json={
        "learning_goal": "placement_prep",
        "experience_level": "intermediate"
    }, headers=headers_1)
    check(onboard_res.status_code == 200, "Completed onboarding")

    # Diagnostic problems
    diag_probs_res = client.get("/api/diagnostic/problems")
    check(diag_probs_res.status_code == 200, "Fetched diagnostic problems suite")
    diag_problems = diag_probs_res.json()
    check(len(diag_problems) >= 6, f"Diagnostic suite contains {len(diag_problems)} problems")

    # Submit diagnostic attempts:
    # #1 (Two Sum - hashing, data structures) -> Solved
    # #6 (Valid Anagram - strings, hashing) -> Solved
    # #33 (Climbing Stairs - dp) -> Failed
    client.post("/api/diagnostic/submit", json={
        "problem_id": 1,
        "is_solved": True,
        "time_spent_seconds": 90,
        "code_submitted": "def twoSum(): pass"
    }, headers=headers_1)

    client.post("/api/diagnostic/submit", json={
        "problem_id": 6,
        "is_solved": True,
        "time_spent_seconds": 60,
        "code_submitted": "def isAnagram(): pass"
    }, headers=headers_1)

    client.post("/api/diagnostic/submit", json={
        "problem_id": 33,
        "is_solved": False,
        "time_spent_seconds": 120,
        "code_submitted": "def minCostClimbingStairs(): pass"
    }, headers=headers_1)

    # Complete diagnostic -> Calibrates concept states and generates initial recommendation
    comp_res = client.post("/api/diagnostic/complete", headers=headers_1)
    check(comp_res.status_code == 200, "Diagnostic completion succeeded (200)")

    # Verify concept calibration:
    db.expire_all()
    concept_states = KnowledgeStateEngine.get_user_concept_states(db, user_id_1)
    c_map = {cs.concept: cs for cs in concept_states}
    check(len(concept_states) == 37, "37 Codeforces learning concepts initialized")
    check("*special" not in c_map, "*special strictly excluded from concept states")

    # Hashing: 2 solved -> mastery = (2+1)/(2+2) = 0.75, weakness = 0.25
    check(c_map["hashing"].mastery_score == 0.75, f"Hashing mastery calibrated to 0.75 (Got {c_map['hashing'].mastery_score})")
    check(c_map["hashing"].weakness_score == 0.25, f"Hashing weakness dropped to 0.25 (Got {c_map['hashing'].weakness_score})")

    # DP: 1 failed -> mastery = (0+1)/(1+2) = 0.3333, weakness = 0.6667
    check(abs(c_map["dp"].mastery_score - 0.3333) < 1e-3, f"DP mastery dropped to 0.3333 on failure (Got {c_map['dp'].mastery_score})")
    check(abs(c_map["dp"].weakness_score - 0.6667) < 1e-3, f"DP weakness elevated to 0.6667 (Got {c_map['dp'].weakness_score})")
    check(c_map["dp"].weakness_level == "Very High", f"DP weakness level is 'Very High' (Got {c_map['dp'].weakness_level})")

    # Verify Personalized Roadmap post-diagnostic
    roadmap_res = client.get("/api/roadmap", headers=headers_1)
    check(roadmap_res.status_code == 200, "GET /api/roadmap returned 200")
    rm_data = roadmap_res.json()
    check(rm_data["total_stages"] == 4, "Roadmap contains 4 progression stages")
    check(rm_data["current_stage_id"] == "stage_advanced", f"Focus stage points to Advanced Algorithms stage where DP weakness resides (Got {rm_data['current_stage_id']})")

    # Verify initial active recommendation
    rec_res = client.get("/api/recommendations/next", headers=headers_1)
    check(rec_res.status_code == 200, "GET /api/recommendations/next returned 200")
    rec_data = rec_res.json()
    check(rec_data["is_active"] is True, "Active recommendation is marked active")
    check(rec_data["problem"]["id"] not in {1, 6, 33}, f"Diagnostic attempted problems are excluded from recommendation (Got #{rec_data['problem']['id']})")
    check(rec_data["recommendation_score"] is not None, f"Recommendation score populated: {rec_data['recommendation_score']}")
    check(rec_data["concept_gap"] is not None, f"Concept gap populated: {rec_data['concept_gap']}")
    check(rec_data["difficulty_fit"] is not None, f"Difficulty fit populated: {rec_data['difficulty_fit']}")

    # -------------------------------------------------------------
    # 2. Existing User Journey: Login -> Current Concept State -> Roadmap -> Rec
    # -------------------------------------------------------------
    print("\n--- [2] Existing User Pipeline: Login & Current State Persistence ---")
    login_res = client.post("/api/auth/login", json={
        "email": f"new_learner_{uid_1}@test.com",
        "password": "Password123!"
    })
    check(login_res.status_code == 200, "Existing user login succeeded (200)")
    existing_token = login_res.json()["access_token"]
    existing_headers = {"Authorization": f"Bearer {existing_token}"}

    # Fetch concept states
    concepts_res = client.get("/api/knowledge-state/concepts", headers=existing_headers)
    check(concepts_res.status_code == 200, "GET /api/knowledge-state/concepts returned 200")
    existing_c_map = {c["concept"]: c for c in concepts_res.json()}
    check(existing_c_map["dp"]["weakness_score"] > 0.60, "Persisted DP weakness score retained on login")
    check(existing_c_map["hashing"]["mastery_score"] == 0.75, "Persisted Hashing mastery score retained on login")

    # Fetch roadmap
    existing_rm = client.get("/api/roadmap", headers=existing_headers).json()
    check(existing_rm["user_id"] == user_id_1, "Roadmap reflects authenticated existing user")

    # Fetch active recommendation: matches active rec created earlier
    existing_rec = client.get("/api/recommendations/next", headers=existing_headers).json()
    check(existing_rec["id"] == rec_data["id"], f"Active recommendation retrieved consistently ({existing_rec['id']} == {rec_data['id']})")

    # -------------------------------------------------------------
    # 3. Post-Problem Submission Pipeline:
    #    Submission -> Evaluate -> Update Concept State -> Recalculate -> Generate Next Rec
    # -------------------------------------------------------------
    print("\n--- [3] Problem Submission Pipeline: Evaluation -> KT Update -> Immediate Next Recommendation ---")
    prev_rec_id = rec_data["id"]
    rec_prob_slug = rec_data["problem"]["slug"]
    rec_prob_id = rec_data["problem"]["id"]

    # Problem 2: Best Time to Buy and Sell Stock (greedy, data structures)
    # Let's submit an Accepted solution for problem #2
    solution_code = """
def maxProfit(prices):
    min_p = float('inf')
    max_p = 0
    for p in prices:
        if p < min_p:
            min_p = p
        elif p - min_p > max_p:
            max_p = p - min_p
    return max_p
"""
    p_stock = db.query(Problem).filter(Problem.id == 2).first()
    check(p_stock is not None, "Loaded Problem #2 for submission")

    sub_res = client.post("/api/submissions/submit", json={
        "problem_id": 2,
        "code": solution_code
    }, headers=headers_1)
    check(sub_res.status_code == 201, "POST /api/submissions/submit returned 201")
    sub_info = sub_res.json()
    check(sub_info["status"] == "Accepted", "Submission status evaluated as Accepted")
    check(sub_info["passed_test_cases"] == sub_info["total_test_cases"], "All test cases passed")

    # Verify concept state updated from submission: greedy updated
    db.rollback()
    db.expire_all()
    c_after_sub = KnowledgeStateEngine.get_user_concept_states(db, user_id_1)
    after_map = {cs.concept: cs for cs in c_after_sub}
    check(after_map["greedy"].interactions == 1, f"Greedy interactions incremented to 1 (Got {after_map['greedy'].interactions})")
    check(after_map["greedy"].solved_count == 1, f"Greedy solved_count incremented to 1 (Got {after_map['greedy'].solved_count})")
    # S=1, N=1 -> (1+1)/(1+2) = 2/3 = 0.6667
    check(abs(after_map["greedy"].mastery_score - 0.6667) < 1e-3, f"Greedy mastery boosted to 0.6667 (Got {after_map['greedy'].mastery_score})")
    check(abs(after_map["greedy"].weakness_score - 0.3333) < 1e-3, f"Greedy weakness dropped to 0.3333 (Got {after_map['greedy'].weakness_score})")

    # Verify that the NEXT recommendation was immediately generated upon submission
    fresh_rec_res = client.get("/api/recommendations/next", headers=headers_1)
    check(fresh_rec_res.status_code == 200, "GET /api/recommendations/next returned 200 after submission")
    fresh_rec = fresh_rec_res.json()
    check(fresh_rec["id"] != prev_rec_id, f"Next recommendation was regenerated with new ID ({fresh_rec['id']} != {prev_rec_id})")
    check(fresh_rec["problem"]["id"] != 2, f"Submitted problem #2 is strictly excluded from next recommendation (#{fresh_rec['problem']['id']})")
    check(fresh_rec["is_active"] is True, "Next recommendation is active")

    # Verify previous recommendation was deactivated
    db.rollback()
    db.expire_all()
    old_rec_row = db.query(Recommendation).filter(Recommendation.id == prev_rec_id).first()
    check(old_rec_row.is_active is False, f"Previous recommendation #{prev_rec_id} deactivated")

    # Verify failed submission update loop:
    # Let's submit a Wrong Answer for Coin Change (#34 - dp)
    sub_fail = client.post("/api/submissions/submit", json={
        "problem_id": 34,
        "code": "def coinChange(coins, amount): return -999"
    }, headers=headers_1)
    check(sub_fail.status_code == 201, "POST /api/submissions/submit (Wrong Answer) returned 201")
    check(sub_fail.json()["status"] == "Wrong Answer", "Submission evaluated as Wrong Answer")

    # Verify DP concept state updated: interactions incremented, solved_count unchanged
    db.rollback()
    db.expire_all()
    c_after_fail = KnowledgeStateEngine.get_user_concept_states(db, user_id_1)
    fail_map = {cs.concept: cs for cs in c_after_fail}
    # DP diagnostic had interactions=1, solved=0. Now with this failed submission: interactions=2, solved=0
    # mastery = (0+1)/(2+2) = 1/4 = 0.25, weakness = 0.75
    check(fail_map["dp"].interactions == 2, f"DP interactions incremented to 2 on failure (Got {fail_map['dp'].interactions})")
    check(fail_map["dp"].solved_count == 0, f"DP solved_count remained 0 on failure (Got {fail_map['dp'].solved_count})")
    check(fail_map["dp"].mastery_score == 0.25, f"DP mastery dropped to 0.25 (Got {fail_map['dp'].mastery_score})")
    check(fail_map["dp"].weakness_score == 0.75, f"DP weakness elevated to 0.75 (Got {fail_map['dp'].weakness_score})")

    # Verify next recommendation generated after failure
    rec_after_fail = client.get("/api/recommendations/next", headers=headers_1).json()
    check(rec_after_fail["id"] != fresh_rec["id"], "Fresh recommendation generated after failed submission")
    check(rec_after_fail["problem"]["id"] not in {1, 6, 33, 2, 34}, f"Attempted problem #34 is excluded (#{rec_after_fail['problem']['id']})")

    # -------------------------------------------------------------
    # 4. Diversity-Aware Top-K Recommendations
    # -------------------------------------------------------------
    print("\n--- [4] Diversity-Aware Top-K Recommendation Verification ---")
    top_res = client.get("/api/recommendations/top?limit=10", headers=headers_1)
    check(top_res.status_code == 200, "GET /api/recommendations/top returned 200")
    top_items = top_res.json()
    check(len(top_items) == 10, f"Top-K returned exactly 10 candidates (Got {len(top_items)})")

    # Verify MAX_SAME_PRIMARY_CONCEPT = 2 cap
    primary_counts = {}
    for item in top_items:
        p_c = item["primary_weak_concept"]
        primary_counts[p_c] = primary_counts.get(p_c, 0) + 1
    max_observed = max(primary_counts.values()) if primary_counts else 0
    check(max_observed <= 2, f"Primary concept occurrences capped at <= 2 (Max observed: {max_observed})")
    check(len(primary_counts) >= 5, f"Top-10 recommendations cover diverse concepts (Count: {len(primary_counts)})")

    # Verify all attempted problems excluded from top items
    all_attempted = {1, 6, 33, 2, 34}
    for item in top_items:
        check(item["problem"]["id"] not in all_attempted, f"Top candidate #{item['problem']['id']} not in attempted set")

    # -------------------------------------------------------------
    # 5. Cold-Start Learner Safety & Non-Contamination
    # -------------------------------------------------------------
    print("\n--- [5] Cold-Start Learner Safety & Non-Contamination ---")
    uid_cold = uuid.uuid4().hex[:8]
    cold_reg = client.post("/api/auth/register", json={
        "name": f"Cold Learner {uid_cold}",
        "email": f"cold_{uid_cold}@test.com",
        "password": "Password123!"
    })
    token_cold = cold_reg.json()["access_token"]
    user_id_cold = cold_reg.json()["user"]["id"]
    headers_cold = {"Authorization": f"Bearer {token_cold}"}

    # Cold learner difficulty target
    cold_target = RecommendationEngine.get_user_learning_target(db, user_id_cold)
    check(cold_target == 950, f"Cold learner difficulty target is baseline 950 (Got {cold_target})")

    # Cold learner next recommendation
    cold_rec_res = client.get("/api/recommendations/next", headers=headers_cold)
    check(cold_rec_res.status_code == 200, "GET /api/recommendations/next succeeded for cold-start learner")
    cold_rec = cold_rec_res.json()
    check(cold_rec["is_active"] is True, "Cold-start recommendation is active")
    check(cold_rec["predicted_success_prob"] == 0.50, f"Cold-start success prob is neutral 0.50 (Got {cold_rec['predicted_success_prob']})")
    check(cold_rec["concept_gap"] == 0.50, f"Cold-start concept gap is neutral 0.50 (Got {cold_rec['concept_gap']})")

    # Verify zero fake Codeforces submissions created
    db.rollback()
    db.expire_all()
    cold_subs = db.query(Submission).filter(Submission.user_id == user_id_cold).count()
    check(cold_subs == 0, "Cold-start learner has 0 submissions in database (No fake history)")

    # -------------------------------------------------------------
    # 6. Multi-User Strict Isolation
    # -------------------------------------------------------------
    print("\n--- [6] Multi-User Strict Isolation Verification ---")
    # User 1 has attempted problems, DP weakness, history
    # Cold User has neutral state, 0 submissions, 0 history
    cold_hist = client.get("/api/recommendations/history", headers=headers_cold).json()
    check(len(cold_hist) == 1, f"Cold learner has only their own recommendation (Count: {len(cold_hist)})")

    user_1_hist = client.get("/api/recommendations/history", headers=headers_1).json()
    check(len(user_1_hist) >= 3, f"User 1 has multiple recommendations (Count: {len(user_1_hist)})")

    # User 1 cannot see Cold User recs and vice-versa
    for h in user_1_hist:
        check(h["user_id"] == user_id_1, f"User 1 history item belongs to User 1 ({h['user_id']} == {user_id_1})")

    # -------------------------------------------------------------
    # 7. Dashboard API Synchronization
    # -------------------------------------------------------------
    print("\n--- [7] Dashboard API Synchronization ---")
    dash_res = client.get("/api/dashboard/summary", headers=headers_1)
    check(dash_res.status_code == 200, "GET /api/dashboard/summary returned 200")
    dash = dash_res.json()
    check(dash["user"]["id"] == user_id_1, f"Dashboard user matches User 1 ({dash['user']['id']} == {user_id_1})")
    check(dash["problem_stats"]["total_submissions"] == 2, f"Dashboard recorded 2 submissions (Got {dash['problem_stats']['total_submissions']})")
    check(dash["problem_stats"]["total_solved"] == 1, f"Dashboard recorded 1 solved (Got {dash['problem_stats']['total_solved']})")
    check(dash["active_recommendation"] is not None, "Dashboard includes active recommendation")
    check(dash["active_recommendation"]["problem_id"] not in all_attempted, "Dashboard active recommendation excludes all attempted problems")

    print("\n" + "=" * 70)
    print(f"PHASE 3 STEP 1 PIPELINE VERIFICATION: ALL {PASSED_CHECKS}/{TOTAL_CHECKS} CHECKS PASSED (100% SUCCESS)")
    print("=" * 70)


if __name__ == "__main__":
    test_phase3_step1_pipeline()
