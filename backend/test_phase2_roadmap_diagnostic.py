"""
Phase 2 Step 4 Verification Suite: Adaptive Roadmap + Diagnostic Integration.
Tests:
1. Diagnostic integration: completion updates concept-level states with empirical evidence.
2. Positive vs negative diagnostic evidence: correct answers increase mastery/confidence; incorrect answers reveal confirmed weakness.
3. No fake Codeforces history: zero fabricated submissions/interactions.
4. No double counting of diagnostic attempts.
5. Cold-start safety: new learner without diagnostic gets safe neutral roadmap without fake profile.
6. Roadmap generation: dynamic evaluation of 4 stages across all 37 learning concepts, excluding '*special'.
7. Prerequisite-aware progression & status: completed, in_progress, available, locked.
8. Dynamic roadmap updates: submitting practice solutions updates concept state and recalculates roadmap priority.
9. Recommendation engine integration: scoring weights (0.60/0.40) unchanged, attempted problem filtering respected.
10. API security & user isolation: 401 on unauthenticated access, strict isolation between learners.
"""
import uuid
from collections import Counter
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import SessionLocal
from app.models.user import User
from app.models.problem import Problem
from app.models.submission import Submission
from app.models.diagnostic_attempt import DiagnosticAttempt
from app.models.learner_concept_state import LearnerConceptState
from app.ml.state_engine import KnowledgeStateEngine, get_problem_learning_concepts
from app.ml.roadmap_engine import (
    AdaptiveRoadmapEngine,
    ROADMAP_STAGES_CONFIG,
    CONCEPT_COMPLETION_MASTERY_THRESHOLD,
    CONCEPT_COMPLETION_CONFIDENCE_THRESHOLD,
)
from app.services.recommendation_engine import (
    RecommendationEngine,
    compute_recommendation_score,
    CONCEPT_GAP_WEIGHT,
    DIFFICULTY_FIT_WEIGHT,
)

client = TestClient(app)


def run_phase2_step4_tests():
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
            raise AssertionError(f"Check #{total_checks} failed: {message}")

    print("=======================================================================")
    print("RUNNING PHASE 2 — STEP 4: ADAPTIVE ROADMAP & DIAGNOSTIC INTEGRATION")
    print("=======================================================================\n")

    db = SessionLocal()
    uid = uuid.uuid4().hex[:8]

    # -------------------------------------------------------------
    # 1. Cold-Start Learner Safety (Before Diagnostic)
    # -------------------------------------------------------------
    print("--- [1] Cold-Start Learner Safety (Pre-Diagnostic) ---")
    reg_res = client.post("/api/auth/register", json={
        "name": f"Roadmap Learner {uid}",
        "email": f"roadmap_{uid}@test.com",
        "password": "Password123!"
    })
    check(reg_res.status_code == 201, "Registered new learner")
    token = reg_res.json()["access_token"]
    user_id = reg_res.json()["user"]["id"]
    headers = {"Authorization": f"Bearer {token}"}

    # Pre-diagnostic concept states should be neutral
    pre_states = KnowledgeStateEngine.get_or_initialize_user_concept_states(db, user_id)
    check(len(pre_states) == 37, f"Initialized exactly 37 learning concepts (Got {len(pre_states)})")
    check(all(s.concept != "*special" for s in pre_states), "*special is strictly excluded from pre-diagnostic concept states")
    check(all(s.interactions == 0 for s in pre_states), "All concept interactions are initially 0 (No fake interactions)")
    check(all(s.solved_count == 0 for s in pre_states), "All concept solved counts are initially 0 (No fake solved counts)")
    check(all(s.mastery_score == 0.50 for s in pre_states), "All pre-diagnostic concepts hold neutral Bayesian prior (mastery=0.50)")
    check(all(s.confidence_score == 0.0 for s in pre_states), "All pre-diagnostic concepts hold zero confidence (confidence=0.0)")

    # Pre-diagnostic roadmap generation
    pre_roadmap_res = client.get("/api/roadmap", headers=headers)
    check(pre_roadmap_res.status_code == 200, "GET /api/roadmap returns 200 for pre-diagnostic learner")
    pre_roadmap = pre_roadmap_res.json()
    check(pre_roadmap["current_stage"] == "Foundations", "Pre-diagnostic roadmap starts at Foundations stage")
    check(pre_roadmap["total_stages"] == 4, "Total stages count is 4")
    check(pre_roadmap["completed_stages"] == 0, "Completed stages count is initially 0")
    check(pre_roadmap["overall_progress_percent"] == 0.0, "Overall progress percent is initially 0.0%")

    # -------------------------------------------------------------
    # 2. Diagnostic Assessment Integration & Concept Calibration
    # -------------------------------------------------------------
    print("\n--- [2] Diagnostic Assessment Integration & Concept Calibration ---")
    # Fetch diagnostic problems
    diag_probs_res = client.get("/api/diagnostic/problems")
    check(diag_probs_res.status_code == 200, "Fetched diagnostic problems suite")
    diag_probs = diag_probs_res.json()
    check(len(diag_probs) >= 6, f"Diagnostic suite contains 6+ problems (Count: {len(diag_probs)})")

    # Diagnostic Attempt 1: Problem #1 (Two Sum, concepts: 'hashing', 'data structures') -> Solved (True)
    p1 = diag_probs[0]
    att1_res = client.post("/api/diagnostic/submit", json={
        "problem_id": p1["id"],
        "is_solved": True,
        "time_spent_seconds": 60,
        "code_submitted": "def solution(): return True"
    }, headers=headers)
    check(att1_res.status_code == 200, f"Submitted diagnostic attempt for #{p1['id']} (Solved)")

    # Diagnostic Attempt 2: Problem #2 (Valid Anagram Check, concepts: 'strings', 'hashing') -> Solved (True)
    p2 = diag_probs[1]
    att2_res = client.post("/api/diagnostic/submit", json={
        "problem_id": p2["id"],
        "is_solved": True,
        "time_spent_seconds": 80,
        "code_submitted": "def solution(): return True"
    }, headers=headers)
    check(att2_res.status_code == 200, f"Submitted diagnostic attempt for #{p2['id']} (Solved)")

    # Diagnostic Attempt 3: Climbing Stairs (topic: DP, concepts: 'dp') -> Failed (False)
    # Find climbing stairs problem in diag suite
    p_dp = next((p for p in diag_probs if p["slug"] == "climbing-stairs-min-cost"), diag_probs[-1])
    att3_res = client.post("/api/diagnostic/submit", json={
        "problem_id": p_dp["id"],
        "is_solved": False,
        "time_spent_seconds": 120,
        "code_submitted": "def solution(): pass"
    }, headers=headers)
    check(att3_res.status_code == 200, f"Submitted diagnostic attempt for #{p_dp['id']} (Failed)")

    # Complete diagnostic
    complete_res = client.post("/api/diagnostic/complete", headers=headers)
    check(complete_res.status_code == 200, "POST /api/diagnostic/complete succeeded (200)")
    comp_json = complete_res.json()
    check(comp_json["knowledge_states_initialized"] == 10, "Diagnostic completion initialized 10 topic states (backward compatible)")

    # -------------------------------------------------------------
    # 3. Verify Calibrated Concept States (Positive vs Negative Evidence)
    # -------------------------------------------------------------
    print("\n--- [3] Empirical Concept Calibration Verification ---")
    db.rollback()
    db.expire_all()
    post_states = KnowledgeStateEngine.get_user_concept_states(db, user_id)
    post_map = {s.concept: s for s in post_states}

    # Hashing concept received 2 solved attempts (#1 and #2):
    # interactions = 2, solved = 2 -> Bayesian mastery = (2+1)/(2+2) = 3/4 = 0.75
    hashing_cs = post_map["hashing"]
    check(hashing_cs.interactions == 2, f"Hashing interactions calibrated to 2 (Got {hashing_cs.interactions})")
    check(hashing_cs.solved_count == 2, f"Hashing solved count calibrated to 2 (Got {hashing_cs.solved_count})")
    check(hashing_cs.mastery_score == 0.75, f"Hashing mastery boosted to 0.75 (Got {hashing_cs.mastery_score})")
    check(hashing_cs.weakness_score == 0.25, f"Hashing weakness dropped to 0.25 (Got {hashing_cs.weakness_score})")
    check(hashing_cs.confidence_score == 0.20, f"Hashing confidence increased to 0.20 (Got {hashing_cs.confidence_score})")

    # DP concept received 1 failed attempt:
    # interactions = 1, solved = 0 -> Bayesian mastery = (0+1)/(1+2) = 1/3 = 0.3333
    dp_cs = post_map["dp"]
    check(dp_cs.interactions == 1, f"DP interactions calibrated to 1 (Got {dp_cs.interactions})")
    check(dp_cs.solved_count == 0, f"DP solved count calibrated to 0 (Got {dp_cs.solved_count})")
    check(abs(dp_cs.mastery_score - 0.3333) < 1e-3, f"DP mastery dropped to 0.3333 on failure (Got {dp_cs.mastery_score})")
    check(abs(dp_cs.weakness_score - 0.6667) < 1e-3, f"DP weakness elevated to 0.6667 (Got {dp_cs.weakness_score})")
    check(dp_cs.weakness_level == "Very High", f"DP weakness level classified as Very High (Got {dp_cs.weakness_level})")
    check(dp_cs.confidence_score == 0.10, f"DP confidence is positive (0.10) confirming genuine weakness (Got {dp_cs.confidence_score})")

    # Unseen concept (e.g., bitmasks, greedy) maintained neutral prior
    greedy_cs = post_map["greedy"]
    check(greedy_cs.interactions == 0, "Untested concept (greedy) interactions remained 0")
    check(greedy_cs.mastery_score == 0.50, "Untested concept (greedy) mastery remained neutral 0.50")
    check(greedy_cs.confidence_score == 0.0, "Untested concept (greedy) confidence remained 0.0 (distinguished from confirmed weakness)")

    # Zero fake Codeforces history verification
    db.expire_all()
    sub_count = db.query(Submission).filter(Submission.user_id == user_id).count()
    check(sub_count == 0, "Diagnostic calibration created zero fake submission records in database")

    # No double counting on repeat recalculation
    KnowledgeStateEngine.update_concept_states_from_diagnostic(db, user_id)
    db.expire_all()
    recalc_hashing = db.query(LearnerConceptState).filter(
        LearnerConceptState.user_id == user_id,
        LearnerConceptState.concept == "hashing"
    ).first()
    check(recalc_hashing.interactions == 2, f"Repeat calibration preserves exact interaction count without double-counting (Got {recalc_hashing.interactions})")

    # -------------------------------------------------------------
    # 4. Adaptive Roadmap Generation & Stages
    # -------------------------------------------------------------
    print("\n--- [4] Adaptive Roadmap Generation & Stage Taxonomy ---")
    roadmap_res = client.get("/api/roadmap", headers=headers)
    check(roadmap_res.status_code == 200, "GET /api/roadmap returns 200 for calibrated learner")
    roadmap = roadmap_res.json()

    check(roadmap["total_stages"] == 4, "Roadmap contains 4 progression stages")
    stage_ids = [s["stage_id"] for s in roadmap["stages"]]
    check(stage_ids == ["stage_foundations", "stage_data_structures", "stage_core_algorithms", "stage_advanced"],
          "Stages follow the 4 progression tiers (Foundations -> Data Structures -> Core Algorithms -> Advanced)")

    # Verify all 37 distinct concepts are included across stages
    all_roadmap_concepts = []
    for s in roadmap["stages"]:
        for c in s["concepts"]:
            all_roadmap_concepts.append(c["concept"])

    check(len(all_roadmap_concepts) == 37, f"All 37 learning concepts are mapped across stages (Got {len(all_roadmap_concepts)})")
    check("*special" not in all_roadmap_concepts, "*special is strictly excluded from all roadmap concepts")

    # Stage statuses & concept statuses
    foundations_stage = roadmap["stages"][0]
    check(foundations_stage["status"] in ["available", "in_progress", "completed"], "Foundations stage is unlocked")

    # In Foundations, hashing was mastered (mastery=0.75, conf=0.20)
    hashing_item = next(c for c in foundations_stage["concepts"] if c["concept"] == "hashing")
    check(hashing_item["status"] == "completed", f"Hashing status is 'completed' (mastery={hashing_item['mastery_score']}, conf={hashing_item['confidence_score']})")

    # In Advanced stage, DP is confirmed weakness (weakness >= 0.50, conf > 0.0) -> priority 1
    advanced_stage = roadmap["stages"][3]
    dp_item = next(c for c in advanced_stage["concepts"] if c["concept"] == "dp")
    check(dp_item["status"] == "in_progress", f"DP concept status is 'in_progress' (Got {dp_item['status']})")
    check(dp_item["priority"] == 1, f"DP concept prioritized as #1 learning urgency within stage (Got {dp_item['priority']})")

    # -------------------------------------------------------------
    # 5. Dynamic Roadmap Progression (Practice Submission Loop)
    # -------------------------------------------------------------
    print("\n--- [5] Dynamic Roadmap Progression (Adaptive Mastery Update) ---")
    # Learner now practices and solves DP problems to improve DP mastery
    p_dp_prob = db.query(Problem).filter(Problem.slug == "climbing-stairs-min-cost").first()
    sub_dp1 = Submission(
        user_id=user_id,
        problem_id=p_dp_prob.id,
        code="def minCostClimbingStairs(): pass",
        status="Accepted",
        passed_test_cases=3,
        total_test_cases=3,
        execution_time_ms=45.0
    )
    db.add(sub_dp1)
    db.commit()

    # Trigger KT update for submission
    KnowledgeStateEngine.update_state_from_submission(db, user_id, p_dp_prob, sub_dp1)

    # Re-fetch concept state for DP
    db.expire_all()
    dp_after_sub = db.query(LearnerConceptState).filter(
        LearnerConceptState.user_id == user_id,
        LearnerConceptState.concept == "dp"
    ).first()
    check(dp_after_sub.interactions == 2, f"DP interactions incremented to 2 (Got {dp_after_sub.interactions})")
    check(dp_after_sub.solved_count == 1, f"DP solved count incremented to 1 (Got {dp_after_sub.solved_count})")
    check(dp_after_sub.mastery_score == 0.50, f"DP mastery improved: (1+1)/(2+2) = 0.50 (Got {dp_after_sub.mastery_score})")
    check(dp_after_sub.weakness_score == 0.50, f"DP weakness decreased from 0.6667 to 0.50 (Got {dp_after_sub.weakness_score})")

    # Simulate second successful DP submission to master the concept
    p_coin = db.query(Problem).filter(Problem.slug == "coin-change").first()
    if p_coin:
        sub_dp2 = Submission(
            user_id=user_id,
            problem_id=p_coin.id,
            code="def coinChange(): pass",
            status="Accepted",
            passed_test_cases=3,
            total_test_cases=3,
            execution_time_ms=50.0
        )
        db.add(sub_dp2)
        db.commit()
        KnowledgeStateEngine.update_state_from_submission(db, user_id, p_coin, sub_dp2)

    db.expire_all()
    dp_mastered = db.query(LearnerConceptState).filter(
        LearnerConceptState.user_id == user_id,
        LearnerConceptState.concept == "dp"
    ).first()
    check(dp_mastered.interactions == 3, f"DP interactions reached 3 (Got {dp_mastered.interactions})")
    check(dp_mastered.solved_count == 2, f"DP solved count reached 2 (Got {dp_mastered.solved_count})")
    check(dp_mastered.mastery_score == 0.60, f"DP mastery reached 0.60 (Got {dp_mastered.mastery_score})")

    # Re-fetch roadmap to verify dynamic adaptation
    updated_roadmap = client.get("/api/roadmap", headers=headers).json()
    adv_updated = updated_roadmap["stages"][3]
    dp_updated_item = next(c for c in adv_updated["concepts"] if c["concept"] == "dp")
    check(dp_updated_item["mastery_score"] == 0.60, f"Roadmap dynamically reflects new DP mastery (Got {dp_updated_item['mastery_score']})")
    check(dp_updated_item["weakness_score"] == 0.40, f"Roadmap dynamically reflects lowered DP weakness (Got {dp_updated_item['weakness_score']})")

    # -------------------------------------------------------------
    # 6. Recommendation Engine Integration & Weights Integrity
    # -------------------------------------------------------------
    print("\n--- [6] Recommendation Engine Integration & Weights Integrity ---")
    # Verify weights are strictly preserved: 0.60 * gap + 0.40 * fit
    check(CONCEPT_GAP_WEIGHT == 0.60, "Recommendation CONCEPT_GAP_WEIGHT is strictly 0.60")
    check(DIFFICULTY_FIT_WEIGHT == 0.40, "Recommendation DIFFICULTY_FIT_WEIGHT is strictly 0.40")
    formula_score = compute_recommendation_score(0.70, 0.80)
    expected_formula_score = round(0.60 * 0.70 + 0.40 * 0.80, 4)
    check(formula_score == expected_formula_score, f"Composite score matches 0.60/0.40 formula ({formula_score} == {expected_formula_score})")

    # Recommended problem IDs attached to roadmap stages
    for stage in updated_roadmap["stages"]:
        check(isinstance(stage["recommended_problem_ids"], list), f"Stage {stage['stage_name']} has recommended_problem_ids list")
        # Ensure attempted problems are excluded
        attempted_ids = RecommendationEngine.get_attempted_problem_ids(db, user_id)
        check(all(pid not in attempted_ids for pid in stage["recommended_problem_ids"]),
              f"Stage {stage['stage_name']} recommended problems exclude all attempted problems")

    # Verify /api/recommendations/top operates harmoniously with roadmap
    top_recs_res = client.get("/api/recommendations/top?limit=5", headers=headers)
    check(top_recs_res.status_code == 200, "GET /api/recommendations/top returns 200")
    top_recs = top_recs_res.json()
    check(len(top_recs) == 5, f"Returned 5 top recommendations (Got {len(top_recs)})")

    # -------------------------------------------------------------
    # 7. Security, Authentication & User Isolation
    # -------------------------------------------------------------
    print("\n--- [7] Security & User Isolation ---")
    # Unauthenticated access rejected with 401
    unauth_res = client.get("/api/roadmap")
    check(unauth_res.status_code == 401, "GET /api/roadmap unauthenticated rejected with 401")

    # Register user B
    uid_b = uuid.uuid4().hex[:8]
    reg_b = client.post("/api/auth/register", json={
        "name": f"User B {uid_b}",
        "email": f"b_{uid_b}@test.com",
        "password": "Password123!"
    })
    token_b = reg_b.json()["access_token"]
    user_b_id = reg_b.json()["user"]["id"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # User B roadmap
    roadmap_b = client.get("/api/roadmap", headers=headers_b).json()
    check(roadmap_b["user_id"] == user_b_id, f"User B roadmap belongs strictly to User B ({roadmap_b['user_id']} == {user_b_id})")
    # User B has not completed Hashing
    b_foundations = roadmap_b["stages"][0]
    b_hashing = next(c for c in b_foundations["concepts"] if c["concept"] == "hashing")
    check(b_hashing["status"] == "available", f"User B hashing status is 'available' (Isolated from User A completed state)")
    check(b_hashing["interactions"] == 0, "User B hashing interactions is 0 (Strict user isolation verified)")

    db.close()

    print("\n=======================================================================")
    print(f"PHASE 2 STEP 4 VERIFICATION SUMMARY: ALL {passed_checks}/{total_checks} CHECKS PASSED (100% SUCCESS)")
    print("=======================================================================")


if __name__ == "__main__":
    run_phase2_step4_tests()
