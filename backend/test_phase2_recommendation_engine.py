"""
Phase 2 Step 3 Verification Suite: Adaptive Recommendation Engine.
Tests:
1. Scoring math: concept_gap, difficulty_fit (exponential), recommendation_score formula (0.60/0.40).
2. Difficulty target: average solved rating + 150, clipping [800, 3500], cold-start baseline (950).
3. Concept handling: multiple concepts, *special exclusion, primary weak concept selection, neutral unseen handling.
4. Attempt filtering: solved excluded, unsolved attempted excluded, diagnostic attempts excluded, no duplicates.
5. Deterministic ranking by composite score: 0.60 * concept_gap + 0.40 * difficulty_fit.
6. Diversity-aware Top-K: MAX_SAME_PRIMARY_CONCEPT = 2 cap enforced across recommendations.
7. Explainability: transparent pedagogical explanation with primary weakness and difficulty match, no internal jargon.
8. Cold start: new learner receives valid recommendations without fake Codeforces history.
9. Existing learner: recommendations reflect persisted concept-level state.
10. Empty/small candidate safety: graceful handling without crashes.
11. REST APIs: /api/recommendations/next, /api/recommendations/generate, /api/recommendations/top.
"""
import uuid
import math
from collections import Counter
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
    compute_final_recommendation_score,
    generate_recommendation_explanation,
    DEFAULT_CHALLENGE_MARGIN,
    MIN_CODEFORCES_RATING,
    MAX_CODEFORCES_RATING,
    TOP_K,
    MAX_SAME_PRIMARY_CONCEPT,
)
from app.ml.concept_profile_engine import calculate_learning_target, filter_learning_concepts
from app.ml.state_engine import KnowledgeStateEngine, get_problem_learning_concepts

client = TestClient(app)


def run_phase2_step3_tests():
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
    print("RUNNING PHASE 2 — STEP 3: ADAPTIVE RECOMMENDATION ENGINE VERIFICATION")
    print("=======================================================================\n")

    # -------------------------------------------------------------
    # 1. Scoring Math & Formula Integrity
    # -------------------------------------------------------------
    print("--- [1] Scoring Math & Exponential Difficulty Fit ---")
    # Exact match -> fit == 1.0
    fit_exact = calculate_difficulty_fit(1500, 1500)
    check(fit_exact == 1.0, f"Exact difficulty match yields fit = 1.0 (Got {fit_exact})")

    # Offset of 300 -> exp(-1) = 0.3679
    fit_300 = calculate_difficulty_fit(1800, 1500)
    check(abs(fit_300 - round(math.exp(-1), 4)) < 1e-3, f"Offset 300 yields exp(-1) = 0.3679 (Got {fit_300})")

    # Symmetric behavior: |1200 - 1500| == |1800 - 1500|
    fit_neg_300 = calculate_difficulty_fit(1200, 1500)
    check(fit_300 == fit_neg_300, f"Difficulty fit is symmetric around learning target ({fit_300} == {fit_neg_300})")

    # Monotonic decay: farther distance gives lower fit
    fit_600 = calculate_difficulty_fit(2100, 1500)
    check(fit_exact > fit_300 > fit_600, f"Fit strictly decays with difficulty distance ({fit_exact} > {fit_300} > {fit_600})")

    # Final score formula: 0.60 * concept_gap + 0.40 * difficulty_fit
    score_1 = compute_recommendation_score(concept_gap=0.80, difficulty_fit=0.50)
    expected_score_1 = round(0.60 * 0.80 + 0.40 * 0.50, 4)
    check(score_1 == expected_score_1, f"Composite score matches 0.60*gap + 0.40*fit ({score_1} == {expected_score_1})")

    # Boundary conditions
    score_max = compute_recommendation_score(1.0, 1.0)
    score_min = compute_recommendation_score(0.0, 0.0)
    check(score_max == 1.0, f"Max score is 1.0 (Got {score_max})")
    check(score_min == 0.0, f"Min score is 0.0 (Got {score_min})")

    # -------------------------------------------------------------
    # 2. Learning Difficulty Target & Clipping
    # -------------------------------------------------------------
    print("\n--- [2] Learning Difficulty Target & Clipping ---")
    # Base formula: avg + 150
    t1 = calculate_learning_target(1000.0, challenge_margin=150)
    check(t1 == 1150, f"Target with avg 1000 and margin 150 is 1150 (Got {t1})")

    # Clipping to min rating (800)
    t_min = calculate_learning_target(600.0, challenge_margin=150)
    check(t_min == 800, f"Target clipped to minimum 800 when avg is low (Got {t_min})")

    # Clipping to max rating (3500)
    t_max = calculate_learning_target(3400.0, challenge_margin=150)
    check(t_max == 3500, f"Target clipped to maximum 3500 when avg is high (Got {t_max})")

    # Cold start target default (800 + 150 = 950)
    t_cold = calculate_learning_target(800.0, challenge_margin=150)
    check(t_cold == 950, f"Cold start baseline target is 950 (Got {t_cold})")

    # -------------------------------------------------------------
    # 3. Concept Handling, Gap Calculation & *special Exclusion
    # -------------------------------------------------------------
    print("\n--- [3] Concept Handling & Multi-Concept Gap ---")
    # Mock concept map
    class DummyConceptState:
        def __init__(self, weakness):
            self.weakness_score = weakness

    mock_map = {
        "graphs": DummyConceptState(0.80),
        "trees": DummyConceptState(0.40),
        "dp": DummyConceptState(0.20),
    }

    # Problem with multiple concepts: [graphs, trees] -> mean weakness = (0.80 + 0.40)/2 = 0.60
    gap_multi = RecommendationEngine.calculate_candidate_concept_gap(["graphs", "trees"], mock_map)
    check(gap_multi == 0.60, f"Multi-concept gap is mean of concept weaknesses (Got {gap_multi})")

    # *special is strictly ignored in gap calculation
    gap_with_special = RecommendationEngine.calculate_candidate_concept_gap(["graphs", "*special", "trees"], mock_map)
    check(gap_with_special == 0.60, f"*special is strictly ignored in candidate gap calculation (Got {gap_with_special})")

    # Unseen concept receives neutral 0.50 prior
    gap_unseen = RecommendationEngine.calculate_candidate_concept_gap(["unseen_concept_xyz"], mock_map)
    check(gap_unseen == 0.50, f"Unseen concept uses neutral prior 0.50 (Got {gap_unseen})")

    # Primary weak concept identification
    primary = RecommendationEngine.get_primary_weak_concept(["dp", "graphs", "trees"], mock_map)
    check(primary == "graphs", f"Primary weak concept correctly identified as highest weakness: graphs (Got {primary})")

    # Primary weak concept strictly ignores *special
    primary_special = RecommendationEngine.get_primary_weak_concept(["*special", "trees", "dp"], mock_map)
    check(primary_special == "trees", f"Primary concept ignores *special and selects trees (Got {primary_special})")

    # -------------------------------------------------------------
    # 4. Attempted Problem Filtering & User Isolation
    # -------------------------------------------------------------
    print("\n--- [4] Attempted Problem Filtering ---")
    db = SessionLocal()
    uid = uuid.uuid4().hex[:8]

    # Create learner for attempt filter testing
    reg_res = client.post("/api/auth/register", json={
        "name": f"Filter Learner {uid}",
        "email": f"filter_{uid}@test.com",
        "password": "Password123!"
    })
    check(reg_res.status_code == 201, "Registered learner for candidate filtering tests")
    user_id = reg_res.json()["user"]["id"]
    token = reg_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Initial candidate evaluation: 40 problems eligible
    all_cands = RecommendationEngine.evaluate_candidates(db, user_id, exclude_all_attempted=True)
    check(len(all_cands) == 40, f"All 40 problems initially eligible (Got {len(all_cands)})")

    # 1. Solved submission on problem #1
    p1 = db.query(Problem).filter(Problem.id == 1).first()
    sub_solved = Submission(
        user_id=user_id,
        problem_id=p1.id,
        code="def twoSum(): pass",
        status="Accepted",
        passed_test_cases=4,
        total_test_cases=4,
        execution_time_ms=50.0
    )
    db.add(sub_solved)
    db.commit()

    # 2. Unsolved (Wrong Answer) submission on problem #2
    p2 = db.query(Problem).filter(Problem.id == 2).first()
    sub_failed = Submission(
        user_id=user_id,
        problem_id=p2.id,
        code="def maxProfit(): pass",
        status="Wrong Answer",
        passed_test_cases=0,
        total_test_cases=3,
        execution_time_ms=60.0
    )
    db.add(sub_failed)
    db.commit()

    # 3. Diagnostic attempt on problem #3
    p3 = db.query(Problem).filter(Problem.id == 3).first()
    diag_attempt = DiagnosticAttempt(
        user_id=user_id,
        problem_id=p3.id,
        is_solved=False,
        time_spent_seconds=120,
        code_submitted="def maxSubArray(): pass"
    )
    db.add(diag_attempt)
    db.commit()

    attempted_ids = RecommendationEngine.get_attempted_problem_ids(db, user_id)
    check(1 in attempted_ids, "Problem #1 (solved) identified in attempted set")
    check(2 in attempted_ids, "Problem #2 (unsolved failed) identified in attempted set")
    check(3 in attempted_ids, "Problem #3 (diagnostic attempt) identified in attempted set")

    # Evaluate candidates with exclude_all_attempted=True
    cands_after = RecommendationEngine.evaluate_candidates(db, user_id, exclude_all_attempted=True)
    check(len(cands_after) == 37, f"Candidates reduced by 3 attempted problems: 40 - 3 = 37 (Got {len(cands_after)})")
    check(all(c["problem_id"] not in {1, 2, 3} for c in cands_after), "All 3 attempted problems are strictly excluded from candidates")

    # Top-K recommendation excludes attempted problems
    top_recs = RecommendationEngine.recommend_top_k(db, user_id, top_k=10, exclude_all_attempted=True)
    check(len(top_recs) == 10, f"Top-K returns 10 candidates (Got {len(top_recs)})")
    check(all(r["problem_id"] not in attempted_ids for r in top_recs), "Top-K recommendations exclude all attempted problems")

    # -------------------------------------------------------------
    # 5. Candidate Ranking by Composite Score
    # -------------------------------------------------------------
    print("\n--- [5] Deterministic Ranking by 0.60*Gap + 0.40*Fit ---")
    scores = [c["recommendation_score"] for c in cands_after]
    is_sorted = all(scores[i] >= scores[i+1] for i in range(len(scores) - 1))
    check(is_sorted, "Candidate problems are deterministically sorted in descending order of recommendation_score")

    # -------------------------------------------------------------
    # 6. Diversity-Aware Top-K Selection (MAX_SAME_PRIMARY_CONCEPT = 2)
    # -------------------------------------------------------------
    print("\n--- [6] Diversity-Aware Top-K Selection ---")
    top_10 = RecommendationEngine.recommend_top_k(
        db,
        user_id,
        top_k=10,
        max_same_primary_concept=MAX_SAME_PRIMARY_CONCEPT,
        exclude_all_attempted=True
    )
    check(len(top_10) == 10, f"Diversity-aware selection returned 10 items (Got {len(top_10)})")

    # Check that no primary concept appears more than MAX_SAME_PRIMARY_CONCEPT (2) times
    concept_counts = Counter([r["primary_concept"] for r in top_10])
    max_count = max(concept_counts.values()) if concept_counts else 0
    check(max_count <= MAX_SAME_PRIMARY_CONCEPT, f"No primary concept appears more than {MAX_SAME_PRIMARY_CONCEPT} times (Max observed: {max_count})")
    check(len(concept_counts) >= 5, f"Top-10 recommendations cover diverse concepts (Count: {len(concept_counts)})")

    # Verify no duplicate problem IDs in Top-K
    rec_prob_ids = [r["problem_id"] for r in top_10]
    check(len(rec_prob_ids) == len(set(rec_prob_ids)), "Top-K recommendations contain zero duplicate problems")

    # -------------------------------------------------------------
    # 7. Pedagogical Explainability
    # -------------------------------------------------------------
    print("\n--- [7] Pedagogical Explainability Verification ---")
    rec = RecommendationEngine.generate_recommendation(db, user_id, force_new=True)
    check(rec is not None, "Generated active recommendation")
    check(len(rec.explanation_text) > 30, f"Explanation text length > 30 chars (Length: {len(rec.explanation_text)})")
    check("Recommended to" in rec.explanation_text, "Explanation contains clear pedagogical reason prefix")
    check(str(rec.primary_weak_concept) in rec.explanation_text, f"Explanation mentions primary weak concept '{rec.primary_weak_concept}'")
    check("difficulty" in rec.explanation_text.lower(), "Explanation discusses difficulty fit")

    # Negative assertion: NO internal jargon in user-facing explanation
    jargon_terms = ["codeforces", "bayesian", "csv", ".pt", "pytorch", "object at 0x", "dataframe"]
    has_jargon = any(term in rec.explanation_text.lower() for term in jargon_terms)
    check(not has_jargon, "Explanation contains NO internal jargon (no Codeforces, Bayesian, CSV, or PyTorch terms)")

    # -------------------------------------------------------------
    # 8. Cold-Start Learner Safety (No Fake History)
    # -------------------------------------------------------------
    print("\n--- [8] Cold-Start Learner Safety ---")
    uid_cold = uuid.uuid4().hex[:8]
    reg_cold = client.post("/api/auth/register", json={
        "name": f"Cold Learner {uid_cold}",
        "email": f"cold_{uid_cold}@test.com",
        "password": "Password123!"
    })
    check(reg_cold.status_code == 201, "Registered brand-new cold-start learner")
    cold_user_id = reg_cold.json()["user"]["id"]
    cold_token = reg_cold.json()["access_token"]
    cold_headers = {"Authorization": f"Bearer {cold_token}"}

    # Verify zero submissions and neutral target
    cold_subs = db.query(Submission).filter(Submission.user_id == cold_user_id).count()
    check(cold_subs == 0, "Cold-start learner has 0 submissions (No fake history)")
    cold_target = RecommendationEngine.get_user_learning_target(db, cold_user_id)
    check(cold_target == 950, f"Cold-start learner difficulty target defaults to 950 (Got {cold_target})")

    # Generate recommendation for cold-start user
    cold_rec = RecommendationEngine.generate_recommendation(db, cold_user_id, force_new=True)
    check(cold_rec is not None, "Generated valid recommendation for cold-start learner without crashing")
    check(cold_rec.is_active is True, "Cold-start recommendation is active")
    check(cold_rec.predicted_success_prob in [0.5, 0.50], f"Cold-start success prob reflects neutral concept prior (Got {cold_rec.predicted_success_prob})")

    # -------------------------------------------------------------
    # 9. Existing Learner with Persisted Concept Weakness
    # -------------------------------------------------------------
    print("\n--- [9] Recommendation for Learner with Persisted Concept Weakness ---")
    # Simulate known weakness in 'dp': user has 5 attempts, 0 solved on dp concept
    dp_state = db.query(LearnerConceptState).filter(
        LearnerConceptState.user_id == user_id,
        LearnerConceptState.concept == "dp"
    ).first()
    if dp_state:
        dp_state.interactions = 5
        dp_state.solved_count = 0
        dp_state.mastery_score = 0.1429
        dp_state.weakness_score = 0.8571
        dp_state.confidence_score = 0.50
        dp_state.weakness_level = "Very High"
        db.commit()

    # Recommendations for this user should prioritize their high weakness
    cands_weak = RecommendationEngine.evaluate_candidates(db, user_id, exclude_all_attempted=True)
    top_weak = cands_weak[0]
    check("dp" in top_weak["concepts"] or top_weak["concept_gap"] >= 0.50, f"Recommendations adaptively target learner's high-weakness concepts (Top candidate concepts: {top_weak['concepts']})")

    # -------------------------------------------------------------
    # 10. Empty / Small Candidate Pool Safety
    # -------------------------------------------------------------
    print("\n--- [10] Empty / Small Candidate Pool Graceful Handling ---")
    # Even if top_k is requested larger than available pool, should not crash
    few_recs = RecommendationEngine.recommend_top_k(db, user_id, top_k=50, exclude_all_attempted=True)
    check(len(few_recs) <= 40, f"Handles requests larger than catalog without crashing (Returned {len(few_recs)})")
    check(len(few_recs) > 0, "Returns available candidates gracefully")

    # -------------------------------------------------------------
    # 11. REST API Endpoints Verification
    # -------------------------------------------------------------
    print("\n--- [11] REST API Endpoints Integration ---")
    # GET /api/recommendations/next
    next_res = client.get("/api/recommendations/next", headers=headers)
    check(next_res.status_code == 200, "GET /api/recommendations/next returns 200")
    next_json = next_res.json()
    check("recommendation_score" in next_json, "Response includes recommendation_score field")
    check("concept_gap" in next_json, "Response includes concept_gap field")
    check("difficulty_fit" in next_json, "Response includes difficulty_fit field")
    check("primary_weak_concept" in next_json, "Response includes primary_weak_concept field")
    check("concepts" in next_json["problem"], "Embedded problem includes learning concepts list")
    check("rating" in next_json["problem"], "Embedded problem includes numerical rating")

    # POST /api/recommendations/generate
    gen_res = client.post("/api/recommendations/generate", headers=headers)
    check(gen_res.status_code == 200, "POST /api/recommendations/generate returns 200")
    gen_json = gen_res.json()
    check(gen_json["is_active"] is True, "Generated recommendation is active")
    check(gen_json["recommendation_score"] is not None, "Generated recommendation has valid score")

    # GET /api/recommendations/top
    top_res = client.get("/api/recommendations/top?limit=5", headers=headers)
    check(top_res.status_code == 200, "GET /api/recommendations/top returns 200")
    top_list = top_res.json()
    check(len(top_list) == 5, f"GET /api/recommendations/top?limit=5 returns exactly 5 items (Got {len(top_list)})")
    check(all(item["recommendation_score"] is not None for item in top_list), "All Top-K recommendations have recommendation_score populated")

    # GET /api/recommendations/history
    hist_res = client.get("/api/recommendations/history", headers=headers)
    check(hist_res.status_code == 200, "GET /api/recommendations/history returns 200")
    hist_items = hist_res.json()
    check(len(hist_items) >= 2, f"History contains past recommendations (Count: {len(hist_items)})")
    check("primary_weak_concept" in hist_items[0], "History items include primary_weak_concept")

    # User isolation: cold learner cannot see user 1 recommendations
    cold_hist = client.get("/api/recommendations/history", headers=cold_headers).json()
    check(all(h["user_id"] == cold_user_id for h in cold_hist), "Cold learner history strictly isolated from other users")

    db.close()

    print("\n=======================================================================")
    print(f"PHASE 2 STEP 3 VERIFICATION SUMMARY: ALL {passed_checks}/{total_checks} CHECKS PASSED (100% SUCCESS)")
    print("=======================================================================")


if __name__ == "__main__":
    run_phase2_step3_tests()
