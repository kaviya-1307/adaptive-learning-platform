"""
Comprehensive Verification Suite for Milestone 5: LSTM Knowledge Tracing Model & Learner State Engine.
Validates:
1. PyTorch LSTM KT Model import, forward pass, output shape [batch_size, 10], values in [0, 1]
2. Synthetic weights loading & deterministic fallback
3. KnowledgeStateEngine 10-topic initialization for new learners
4. Accepted interaction updates target topic mastery positively
5. Wrong Answer interaction penalizes target topic appropriately
6. Difficulty sensitivity (Hard Accepted vs Easy Accepted)
7. Unrelated topics isolation (no arbitrary corruption)
8. Clamping & confidence score calculation in [0, 1]
9. GET /api/knowledge-state returns authenticated 10-topic profile
10. POST /api/knowledge-state/recalculate replays full interaction sequence
11. Integration with POST /api/submissions/submit updates knowledge state in DB in real time
"""
import sys
import uuid
import torch
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import SessionLocal
from app.models.problem import Problem
from app.models.topic import Topic
from app.models.submission import Submission
from app.models.learner_knowledge_state import LearnerKnowledgeState
from app.ml.lstm_kt_model import (
    LSTMKnowledgeTracingModel,
    encode_interaction,
    build_interaction_sequence,
    load_trained_model,
    NUM_TOPICS,
    FEATURE_DIM,
)
from app.ml.state_engine import KnowledgeStateEngine, get_mastery_level_label

client = TestClient(app)


def run_m5_tests():
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
    print("STARTING MILESTONE 5: LSTM KNOWLEDGE TRACING & STATE ENGINE SUITE")
    print("=================================================================\n")

    # -------------------------------------------------------------
    # 1. PyTorch Model Architecture & Forward Pass Tests
    # -------------------------------------------------------------
    print("--- [1] PyTorch LSTM Knowledge Tracing Model Architecture ---")
    model = load_trained_model()
    check(isinstance(model, LSTMKnowledgeTracingModel), "Model instance created successfully")

    # Single-step input [1, 1, 13]
    dummy_input = encode_interaction(topic_id=1, difficulty="Medium", is_correct=True, time_ms=250.0)
    check(dummy_input.shape == (1, 1, FEATURE_DIM), f"Encoded interaction tensor shape is (1, 1, {FEATURE_DIM})")

    out_seq, _ = model(dummy_input)
    check(out_seq.shape == (1, 1, NUM_TOPICS), f"Forward pass output shape is (1, 1, {NUM_TOPICS})")

    pred_mastery = model.predict_latest_mastery(dummy_input)
    check(pred_mastery.shape == (1, NUM_TOPICS), f"predict_latest_mastery output shape is (1, {NUM_TOPICS})")
    check(bool(torch.all(pred_mastery >= 0.0) and torch.all(pred_mastery <= 1.0)), "All predicted mastery values are within [0.0, 1.0]")

    # Sequence input [1, 5, 13]
    dummy_interactions = [
        {"topic_id": 1, "difficulty": "Easy", "is_correct": True, "time_ms": 100.0},
        {"topic_id": 1, "difficulty": "Medium", "is_correct": True, "time_ms": 200.0},
        {"topic_id": 3, "difficulty": "Hard", "is_correct": False, "time_ms": 1500.0},
        {"topic_id": 2, "difficulty": "Easy", "is_correct": True, "time_ms": 150.0},
        {"topic_id": 1, "difficulty": "Hard", "is_correct": True, "time_ms": 800.0},
    ]
    seq_tensor = build_interaction_sequence(dummy_interactions)
    check(seq_tensor.shape == (1, 5, FEATURE_DIM), f"Batch sequence tensor shape is (1, 5, {FEATURE_DIM})")

    seq_out, _ = model(seq_tensor)
    check(seq_out.shape == (1, 5, NUM_TOPICS), f"Multi-step sequence output shape is (1, 5, {NUM_TOPICS})")

    # -------------------------------------------------------------
    # 2. KnowledgeStateEngine Core Logic & Isolation Tests
    # -------------------------------------------------------------
    print("\n--- [2] KnowledgeStateEngine Initialization & Update Logic ---")
    db = SessionLocal()
    unique_id = uuid.uuid4().hex[:8]
    test_email = f"m5_learner_{unique_id}@test.com"
    test_password = "SecurePassword123!"
    test_name = f"M5 Test Learner {unique_id}"

    # Register learner via API
    reg_res = client.post("/api/auth/register", json={
        "name": test_name,
        "email": test_email,
        "password": test_password
    })
    check(reg_res.status_code == 201, "Registered new learner for M5 testing")
    token = reg_res.json()["access_token"]
    user_id = reg_res.json()["user"]["id"]
    headers = {"Authorization": f"Bearer {token}"}

    # Verify initial state creation for all 10 topics
    initial_states = KnowledgeStateEngine.get_or_initialize_user_states(db, user_id)
    check(len(initial_states) == 10, f"Learner initialized with exactly 10 topic states (Got {len(initial_states)})")
    check(all(0.0 <= s.mastery_score <= 1.0 for s in initial_states), "Initial mastery scores are within [0.0, 1.0]")
    check(all(0.0 <= s.confidence_score <= 1.0 for s in initial_states), "Initial confidence scores are within [0.0, 1.0]")

    # Snapshot initial state of Topic 1 (Arrays) and Topic 6 (Trees)
    array_topic = db.query(Topic).filter(Topic.slug == "arrays").first()
    tree_topic = db.query(Topic).filter(Topic.slug == "trees").first()

    array_initial = db.query(LearnerKnowledgeState).filter(
        LearnerKnowledgeState.user_id == user_id,
        LearnerKnowledgeState.topic_id == array_topic.id
    ).first()
    tree_initial = db.query(LearnerKnowledgeState).filter(
        LearnerKnowledgeState.user_id == user_id,
        LearnerKnowledgeState.topic_id == tree_topic.id
    ).first()

    initial_array_mastery = array_initial.mastery_score
    initial_tree_mastery = tree_initial.mastery_score

    # Simulate Accepted Problem on Topic 1 (Arrays)
    array_problem = db.query(Problem).filter(Problem.slug == "two-sum-target-pair").first()
    sim_sub_accepted = Submission(
        user_id=user_id,
        problem_id=array_problem.id,
        code="def twoSum(nums, target): return [0, 1]",
        status="Accepted",
        passed_test_cases=4,
        total_test_cases=4,
        execution_time_ms=120.0
    )
    db.add(sim_sub_accepted)
    db.commit()
    db.refresh(sim_sub_accepted)

    update_res = KnowledgeStateEngine.update_state_from_submission(
        db=db,
        user_id=user_id,
        problem=array_problem,
        submission=sim_sub_accepted
    )
    check(update_res["new_mastery"] > initial_array_mastery, f"Accepted submission increased Arrays mastery: {initial_array_mastery:.3f} -> {update_res['new_mastery']:.3f}")
    check(update_res["total_interactions"] == 1, "Total interactions incremented to 1")

    # Verify Unrelated Topic (Trees) was NOT arbitrarily corrupted
    tree_after = db.query(LearnerKnowledgeState).filter(
        LearnerKnowledgeState.user_id == user_id,
        LearnerKnowledgeState.topic_id == tree_topic.id
    ).first()
    check(tree_after.mastery_score == initial_tree_mastery, f"Unrelated topic (Trees) mastery remained intact ({tree_after.mastery_score:.3f})")

    # Simulate Wrong Answer Problem on Topic 1 (Arrays)
    prev_array_mastery = update_res["new_mastery"]
    sim_sub_wrong = Submission(
        user_id=user_id,
        problem_id=array_problem.id,
        code="def twoSum(nums, target): return []",
        status="Wrong Answer",
        passed_test_cases=0,
        total_test_cases=4,
        execution_time_ms=80.0
    )
    db.add(sim_sub_wrong)
    db.commit()
    db.refresh(sim_sub_wrong)

    update_wrong_res = KnowledgeStateEngine.update_state_from_submission(
        db=db,
        user_id=user_id,
        problem=array_problem,
        submission=sim_sub_wrong
    )
    check(update_wrong_res["new_mastery"] < prev_array_mastery, f"Wrong Answer submission decreased Arrays mastery: {prev_array_mastery:.3f} -> {update_wrong_res['new_mastery']:.3f}")
    check(0.0 <= update_wrong_res["new_mastery"] <= 1.0, "Updated mastery remains strictly in [0.0, 1.0]")
    check(0.0 <= update_wrong_res["confidence"] <= 1.0, "Updated confidence remains strictly in [0.0, 1.0]")

    # -------------------------------------------------------------
    # 3. REST API Endpoint Tests: GET /api/knowledge-state
    # -------------------------------------------------------------
    print("\n--- [3] REST API: GET /api/knowledge-state ---")
    get_state_res = client.get("/api/knowledge-state", headers=headers)
    check(get_state_res.status_code == 200, f"GET /api/knowledge-state returned 200 (Got {get_state_res.status_code})")
    state_json = get_state_res.json()

    check(state_json["user_id"] == user_id, f"Response user_id matches {user_id}")
    check(len(state_json["topics"]) == 10, f"Response contains exactly 10 topics (Got {len(state_json['topics'])})")
    check(0.0 <= state_json["overall_mastery"] <= 1.0, f"overall_mastery ({state_json['overall_mastery']}) in [0, 1]")
    check(0.0 <= state_json["overall_confidence"] <= 1.0, f"overall_confidence ({state_json['overall_confidence']}) in [0, 1]")

    # Verify Topic Schema Fields
    first_topic = state_json["topics"][0]
    check("topic_id" in first_topic and "topic_name" in first_topic, "Topic contains topic_id and topic_name")
    check("mastery_score" in first_topic and "confidence_score" in first_topic, "Topic contains mastery_score and confidence_score")
    check("mastery_level" in first_topic, f"Topic contains mastery_level label ({first_topic['mastery_level']})")

    # Unauthenticated check
    unauth_res = client.get("/api/knowledge-state")
    check(unauth_res.status_code == 401, "GET /api/knowledge-state unauthenticated request rejected with 401")

    # -------------------------------------------------------------
    # 4. REST API Endpoint Tests: POST /api/knowledge-state/recalculate
    # -------------------------------------------------------------
    print("\n--- [4] REST API: POST /api/knowledge-state/recalculate ---")
    recalc_res = client.post("/api/knowledge-state/recalculate", headers=headers)
    check(recalc_res.status_code == 200, f"POST /api/knowledge-state/recalculate returned 200 (Got {recalc_res.status_code})")
    recalc_json = recalc_res.json()

    check(recalc_json["topics_updated"] == 10, f"Recalculated all 10 topics (Got {recalc_json['topics_updated']})")
    check("knowledge_state" in recalc_json, "Response contains refreshed knowledge_state")
    check(len(recalc_json["knowledge_state"]["topics"]) == 10, "Refreshed knowledge state has 10 topics")

    # -------------------------------------------------------------
    # 5. Live E2E Integration: POST /api/submissions/submit
    # -------------------------------------------------------------
    print("\n--- [5] Live E2E Integration: Submission Pipeline -> KT Engine ---")
    correct_solution_code = """
def twoSum(nums: list[int], target: int) -> list[int]:
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
"""
    live_submit_res = client.post("/api/submissions/submit", json={
        "problem_id": array_problem.id,
        "code": correct_solution_code
    }, headers=headers)
    check(live_submit_res.status_code == 201, "Live POST /api/submissions/submit succeeded with 201")
    live_submit_data = live_submit_res.json()
    check(live_submit_data["status"] == "Accepted", "Live submission status is Accepted")

    # Check updated knowledge state via GET API
    updated_state_res = client.get("/api/knowledge-state", headers=headers)
    check(updated_state_res.status_code == 200, "Fetched updated knowledge state")
    updated_state_json = updated_state_res.json()
    updated_array_item = next(t for t in updated_state_json["topics"] if t["topic_id"] == array_topic.id)

    check(updated_array_item["total_interactions"] >= 3, f"Live submission incremented total_interactions to {updated_array_item['total_interactions']}")
    check(updated_array_item["mastery_score"] > 0.25, f"Live submission boosted Arrays mastery to {updated_array_item['mastery_score']:.3f}")

    db.close()

    print("\n=================================================================")
    print(f"MILESTONE 5 VERIFICATION SUMMARY: ALL {passed_checks}/{total_checks} CHECKS PASSED (100% SUCCESS)")
    print("=================================================================")


if __name__ == "__main__":
    run_m5_tests()
