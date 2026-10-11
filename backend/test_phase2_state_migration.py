"""
Phase 2 Step 2 Verification Suite: Knowledge State Migration
============================================================
Validates:
1. Complete removal of synthetic LSTM from live state update paths:
   - Neither get_model() nor predict_latest_mastery() is invoked during update_state_from_submission().
   - lstm_kt_weights.pt is not required for live concept state updates.
2. Concept-level knowledge state creation and persistence:
   - LearnerConceptState initialized across all 37 distinct Codeforces learning concepts.
   - Successful submission updates interactions, solved_count, Bayesian mastery, weakness, confidence, and weakness_level.
   - Unsuccessful submission updates interactions without incrementing solved_count, lowering mastery and raising weakness.
   - All scores strictly bounded within [0.0, 1.0].
3. Multiple concepts handling:
   - Application problems mapped to multiple concepts update all relevant concepts.
   - '*special' metadata tag is strictly ignored.
4. Cold start & learner isolation:
   - New learners start with neutral Bayesian prior (mastery=0.50, weakness=0.50, confidence=0.0).
   - No fabricated Codeforces historical interactions or ratings.
5. Persistence & API compatibility:
   - Concept states successfully stored and retrieved from MySQL learner_concept_states table.
   - GET /api/knowledge-state returns backward-compatible 10 topics AND populated concepts list.
   - GET /api/knowledge-state/concepts returns granular concept profile.
   - POST /api/knowledge-state/recalculate works without LSTM.
   - Live POST /api/submissions/submit updates both topic and concept states in real time.
"""

import sys
import uuid
from unittest.mock import patch
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import SessionLocal
from app.models.user import User
from app.models.topic import Topic
from app.models.problem import Problem
from app.models.submission import Submission
from app.models.learner_knowledge_state import LearnerKnowledgeState
from app.models.learner_concept_state import LearnerConceptState
from app.ml.state_engine import (
    KnowledgeStateEngine,
    get_problem_learning_concepts,
    get_mastery_level_label,
)
from app.ml.concept_profile_engine import (
    get_distinct_learning_concepts,
    WEAKNESS_LEVEL_LOW,
    WEAKNESS_LEVEL_MODERATE,
    WEAKNESS_LEVEL_HIGH,
    WEAKNESS_LEVEL_VERY_HIGH,
)

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


def run_state_migration_tests():
    print("=" * 70)
    print("RUNNING PHASE 2 STEP 2: KNOWLEDGE STATE MIGRATION VERIFICATION")
    print("=" * 70)

    db = SessionLocal()
    uid = uuid.uuid4().hex[:8]
    test_email = f"p2_learner_{uid}@test.com"
    test_password = "Password123!"
    test_name = f"Phase2 Learner {uid}"

    # -------------------------------------------------------------
    # 1. User Registration & Cold-Start Concept State
    # -------------------------------------------------------------
    print("\n--- [1] Learner Registration & Cold-Start Concept States ---")
    reg_res = client.post("/api/auth/register", json={
        "name": test_name,
        "email": test_email,
        "password": test_password
    })
    record_check("Learner registration succeeded (201)", reg_res.status_code == 201)
    auth_data = reg_res.json()
    token = auth_data["access_token"]
    user_id = auth_data["user"]["id"]
    headers = {"Authorization": f"Bearer {token}"}

    # Verify cold-start concept states
    concept_states = KnowledgeStateEngine.get_or_initialize_user_concept_states(db, user_id)
    all_37_concepts = get_distinct_learning_concepts()
    record_check("Initialized exactly 37 distinct Codeforces learning concepts", len(concept_states) == 37, f"Got {len(concept_states)}")
    record_check("'*special' is NOT among concept states", all(cs.concept != "*special" for cs in concept_states))

    # Check neutral prior values for cold-start concepts
    dp_state = next(cs for cs in concept_states if cs.concept == "dp")
    record_check("Cold-start dp interactions == 0", dp_state.interactions == 0)
    record_check("Cold-start dp solved_count == 0", dp_state.solved_count == 0)
    record_check("Cold-start dp mastery_score is neutral prior 0.50", dp_state.mastery_score == 0.50)
    record_check("Cold-start dp weakness_score is 0.50", dp_state.weakness_score == 0.50)
    record_check("Cold-start dp confidence_score is 0.0", dp_state.confidence_score == 0.0)
    record_check("Cold-start dp weakness_level is 'Moderate'", dp_state.weakness_level == WEAKNESS_LEVEL_MODERATE)

    # -------------------------------------------------------------
    # 2. Synthetic LSTM Removal Verification
    # -------------------------------------------------------------
    print("\n--- [2] Synthetic LSTM Removal Verification ---")
    two_sum_prob = db.query(Problem).filter(Problem.slug == "two-sum-target-pair").first()
    record_check("Problem 'two-sum-target-pair' found in DB", two_sum_prob is not None)

    sim_sub = Submission(
        user_id=user_id,
        problem_id=two_sum_prob.id,
        code="def twoSum(nums, target): return [0, 1]",
        status="Accepted",
        passed_test_cases=4,
        total_test_cases=4,
        execution_time_ms=100.0
    )
    db.add(sim_sub)
    db.commit()
    db.refresh(sim_sub)

    # Verify that update_state_from_submission NEVER calls get_model() or predict_latest_mastery()
    with patch.object(KnowledgeStateEngine, "get_model", side_effect=RuntimeError("FAIL: get_model() was called!")) as mock_get_model:
        with patch("app.ml.lstm_kt_model.LSTMKnowledgeTracingModel.predict_latest_mastery", side_effect=RuntimeError("FAIL: predict_latest_mastery was called!")) as mock_predict:
            update_res = KnowledgeStateEngine.update_state_from_submission(
                db=db,
                user_id=user_id,
                problem=two_sum_prob,
                submission=sim_sub
            )
            record_check("State update executed without calling get_model()", mock_get_model.call_count == 0)
            record_check("State update executed without calling predict_latest_mastery()", mock_predict.call_count == 0)

    # -------------------------------------------------------------
    # 3. Concept State Update from Accepted Submission
    # -------------------------------------------------------------
    print("\n--- [3] Concept State Update: Accepted Submission ---")
    record_check("update_state_from_submission returned 'concepts_updated'", "concepts_updated" in update_res)
    concepts_updated = update_res["concepts_updated"]
    record_check("Two Sum updated mapped concepts ('hashing', 'data structures')", set(concepts_updated) == {"hashing", "data structures"}, f"Got {concepts_updated}")

    # Inspect hashing concept state in DB
    hashing_cs = db.query(LearnerConceptState).filter(
        LearnerConceptState.user_id == user_id,
        LearnerConceptState.concept == "hashing"
    ).first()
    record_check("Hashing concept state found in DB", hashing_cs is not None)
    record_check("Hashing interactions incremented to 1", hashing_cs.interactions == 1)
    record_check("Hashing solved_count incremented to 1", hashing_cs.solved_count == 1)
    # S=1, N=1, a=1, b=1 -> (1+1)/(1+2) = 2/3 = 0.6667
    record_check("Hashing mastery_score is 0.6667 (Bayesian (1+1)/(1+2))", hashing_cs.mastery_score == 0.6667, f"Got {hashing_cs.mastery_score}")
    # W = 1 - 0.6667 = 0.3333
    record_check("Hashing weakness_score is 0.3333 (1 - 0.6667)", hashing_cs.weakness_score == 0.3333, f"Got {hashing_cs.weakness_score}")
    # C = min(1.0, 1 / 10) = 0.10
    record_check("Hashing confidence_score is 0.10 (1 / 10)", hashing_cs.confidence_score == 0.10, f"Got {hashing_cs.confidence_score}")
    # Weakness 0.3333 is in (0.20, 0.35] -> Low
    record_check("Hashing weakness_level is 'Low' (0.3333 <= 0.35)", hashing_cs.weakness_level == WEAKNESS_LEVEL_LOW)

    # -------------------------------------------------------------
    # 4. Concept State Update: Wrong Answer Submission
    # -------------------------------------------------------------
    print("\n--- [4] Concept State Update: Wrong Answer Submission ---")
    climbing_stairs = db.query(Problem).filter(Problem.slug == "climbing-stairs-min-cost").first()
    record_check("Problem 'climbing-stairs-min-cost' found in DB", climbing_stairs is not None)

    sim_sub_fail = Submission(
        user_id=user_id,
        problem_id=climbing_stairs.id,
        code="def minCostClimbingStairs(cost): return 0",
        status="Wrong Answer",
        passed_test_cases=0,
        total_test_cases=3,
        execution_time_ms=50.0
    )
    db.add(sim_sub_fail)
    db.commit()
    db.refresh(sim_sub_fail)

    update_res_fail = KnowledgeStateEngine.update_state_from_submission(
        db=db,
        user_id=user_id,
        problem=climbing_stairs,
        submission=sim_sub_fail
    )
    record_check("Climbing Stairs updated 'dp' concept", "dp" in update_res_fail["concepts_updated"])

    dp_cs = db.query(LearnerConceptState).filter(
        LearnerConceptState.user_id == user_id,
        LearnerConceptState.concept == "dp"
    ).first()
    record_check("DP interactions incremented to 1", dp_cs.interactions == 1)
    record_check("DP solved_count remained 0 on Wrong Answer", dp_cs.solved_count == 0)
    # S=0, N=1, a=1, b=1 -> (0+1)/(1+2) = 1/3 = 0.3333
    record_check("DP mastery_score decreased to 0.3333 ((0+1)/(1+2))", dp_cs.mastery_score == 0.3333, f"Got {dp_cs.mastery_score}")
    # W = 1 - 0.3333 = 0.6667
    record_check("DP weakness_score increased to 0.6667", dp_cs.weakness_score == 0.6667, f"Got {dp_cs.weakness_score}")
    # Weakness 0.6667 > 0.65 -> Very High
    record_check("DP weakness_level is 'Very High' (0.6667 > 0.65)", dp_cs.weakness_level == WEAKNESS_LEVEL_VERY_HIGH)

    # -------------------------------------------------------------
    # 5. Multiple Concepts & '*special' Exclusion
    # -------------------------------------------------------------
    print("\n--- [5] Multi-Concept Mapping & '*special' Exclusion ---")
    max_subarr = db.query(Problem).filter(Problem.slug == "maximum-subarray-sum").first()
    concepts_multi = get_problem_learning_concepts(max_subarr)
    record_check("Maximum Subarray Sum maps to multiple concepts ('dp', 'greedy')", set(concepts_multi) == {"dp", "greedy"})
    record_check("'*special' is not in mapped concepts", "*special" not in concepts_multi)

    # -------------------------------------------------------------
    # 6. REST API Endpoints: Concept Profile Exposure
    # -------------------------------------------------------------
    print("\n--- [6] REST API: /api/knowledge-state Endpoints ---")
    # GET /api/knowledge-state returns topics AND concepts
    res_ks = client.get("/api/knowledge-state", headers=headers)
    record_check("GET /api/knowledge-state returned 200", res_ks.status_code == 200)
    ks_data = res_ks.json()
    record_check("Response contains backward-compatible 'topics' list (Count: 10)", len(ks_data.get("topics", [])) == 10)
    record_check("Response contains new 'concepts' list (Count: 37)", len(ks_data.get("concepts", [])) == 37)

    # Verify concept schema fields
    first_concept = ks_data["concepts"][0]
    required_fields = {"concept", "mastery_score", "weakness_score", "confidence_score", "weakness_level", "interactions", "solved_count"}
    record_check("Concept item contains all required fields", required_fields.issubset(set(first_concept.keys())))

    # Dedicated endpoint: GET /api/knowledge-state/concepts
    res_concepts = client.get("/api/knowledge-state/concepts", headers=headers)
    record_check("GET /api/knowledge-state/concepts returned 200", res_concepts.status_code == 200)
    concepts_list = res_concepts.json()
    record_check("Dedicated endpoint returns all 37 learning concepts", len(concepts_list) == 37)

    # Recalculate endpoint: POST /api/knowledge-state/recalculate (No LSTM!)
    with patch.object(KnowledgeStateEngine, "get_model", side_effect=RuntimeError("FAIL: get_model called during recalculate!")):
        res_recalc = client.post("/api/knowledge-state/recalculate", headers=headers)
        record_check("POST /api/knowledge-state/recalculate succeeded without LSTM (200)", res_recalc.status_code == 200)

    # -------------------------------------------------------------
    # 7. Live E2E Submission Flow
    # -------------------------------------------------------------
    print("\n--- [7] Live E2E Submission Pipeline Integration ---")
    live_sub_res = client.post(
        "/api/submissions/submit",
        json={
            "problem_id": two_sum_prob.id,
            "code": "def twoSum(nums, target):\n    seen = {}\n    for i, n in enumerate(nums):\n        if target - n in seen:\n            return [seen[target - n], i]\n        seen[n] = i\n    return []"
        },
        headers=headers
    )
    record_check("POST /api/submissions/submit succeeded (201)", live_sub_res.status_code == 201)
    sub_data = live_sub_res.json()
    record_check("Live submission status is Accepted", sub_data["status"] == "Accepted")

    # Fetch updated concept states to verify real-time update in MySQL
    res_after = client.get("/api/knowledge-state/concepts", headers=headers)
    after_concepts = {c["concept"]: c for c in res_after.json()}
    hashing_after = after_concepts["hashing"]
    record_check("Live submission incremented hashing interactions to 2", hashing_after["interactions"] == 2)
    record_check("Live submission incremented hashing solved_count to 2", hashing_after["solved_count"] == 2)
    # S=2, N=2 -> (2+1)/(2+2) = 3/4 = 0.75
    record_check("Live submission boosted hashing mastery to 0.75", hashing_after["mastery_score"] == 0.75)

    print("\n" + "=" * 70)
    print(f"PHASE 2 STEP 2 SUMMARY: ALL {PASSED_CHECKS}/{TOTAL_CHECKS} CHECKS PASSED (100% SUCCESS)")
    print("=" * 70)


if __name__ == "__main__":
    run_state_migration_tests()
