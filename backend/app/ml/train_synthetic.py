"""
Synthetic Dataset Generator and Training Script for LSTM Knowledge Tracing Model.
Generates reproducible prototype weights saved to backend/app/ml/lstm_kt_weights.pt.
"""
import os
import random
import logging
import torch
import torch.nn as nn
import torch.optim as optim
from typing import List, Tuple

from app.ml.lstm_kt_model import (
    LSTMKnowledgeTracingModel,
    NUM_TOPICS,
    FEATURE_DIM,
    DEFAULT_WEIGHTS_PATH,
    TOPIC_ID_MAP,
    DIFFICULTY_MAP,
)

logger = logging.getLogger(__name__)


def generate_synthetic_data(
    num_learners: int = 250,
    min_seq_len: int = 10,
    max_seq_len: int = 25,
    seed: int = 42
) -> List[Tuple[torch.Tensor, torch.Tensor]]:
    """
    Generates synthetic sequences of student problem attempts and corresponding topic mastery vectors.
    :return: List of (interaction_tensor [seq_len, 13], target_mastery_tensor [seq_len, 10])
    """
    random.seed(seed)
    torch.manual_seed(seed)

    dataset = []

    for _ in range(num_learners):
        seq_len = random.randint(min_seq_len, max_seq_len)
        # Initial latent knowledge state for 10 topics [0.15, 0.45]
        latent_mastery = [random.uniform(0.15, 0.40) for _ in range(NUM_TOPICS)]

        interactions = []
        mastery_targets = []

        for step in range(seq_len):
            # Select a topic (1 to 10)
            topic_id = random.randint(1, NUM_TOPICS)
            topic_idx = TOPIC_ID_MAP[topic_id]

            # Select difficulty
            difficulty = random.choice(["easy", "medium", "hard"])
            diff_scalar = DIFFICULTY_MAP[difficulty]

            # Probability of success depends on current mastery and difficulty
            current_skill = latent_mastery[topic_idx]
            prob_success = max(0.1, min(0.95, current_skill - (diff_scalar - 0.5) * 0.4))
            is_correct = random.random() < prob_success

            # Execution time: faster when correct/easy, slower when struggling
            base_time = 300.0 + diff_scalar * 800.0
            time_ms = base_time + (0 if is_correct else random.uniform(200, 1000))
            norm_time = min(time_ms / 3000.0, 1.0)

            # Construct 13-dim feature vector
            feature = [0.0] * FEATURE_DIM
            feature[topic_idx] = 1.0
            feature[10] = diff_scalar
            feature[11] = 1.0 if is_correct else 0.0
            feature[12] = norm_time
            interactions.append(feature)

            # Update latent mastery for the target topic
            if is_correct:
                delta = 0.04 + diff_scalar * 0.06  # Easy: +0.06, Hard: +0.10
                latent_mastery[topic_idx] = min(0.98, latent_mastery[topic_idx] + delta)
            else:
                delta = 0.03 + (1.0 - diff_scalar) * 0.03  # Easy fail: -0.05, Hard fail: -0.03
                latent_mastery[topic_idx] = max(0.05, latent_mastery[topic_idx] - delta)

            # Record target snapshot for all 10 topics
            mastery_targets.append(list(latent_mastery))

        x_tensor = torch.tensor(interactions, dtype=torch.float32)  # [seq_len, 13]
        y_tensor = torch.tensor(mastery_targets, dtype=torch.float32)  # [seq_len, 10]
        dataset.append((x_tensor, y_tensor))

    return dataset


def train_synthetic_model(
    output_weights_path: str = DEFAULT_WEIGHTS_PATH,
    epochs: int = 70,
    learning_rate: float = 0.005,
    seed: int = 42
) -> LSTMKnowledgeTracingModel:
    """
    Trains the LSTM KT model on synthetic data and persists the weights.
    """
    torch.manual_seed(seed)
    model = LSTMKnowledgeTracingModel()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    criterion = nn.MSELoss()

    dataset = generate_synthetic_data(num_learners=200, seed=seed)

    model.train()
    print(f"Starting training on {len(dataset)} synthetic learner trajectories for {epochs} epochs...")

    for epoch in range(1, epochs + 1):
        total_loss = 0.0
        random.shuffle(dataset)

        for x_seq, y_seq in dataset:
            # Batch size = 1
            x_batch = x_seq.unsqueeze(0)  # [1, seq_len, 13]
            y_batch = y_seq.unsqueeze(0)  # [1, seq_len, 10]

            optimizer.zero_grad()
            predictions, _ = model(x_batch)
            loss = criterion(predictions, y_batch)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        avg_loss = total_loss / len(dataset)
        if epoch % 10 == 0 or epoch == 1:
            print(f"Epoch {epoch:02d}/{epochs:02d} - Loss (MSE): {avg_loss:.5f}")

    # Save weights
    os.makedirs(os.path.dirname(output_weights_path), exist_ok=True)
    torch.save(model.state_dict(), output_weights_path)
    print(f"Successfully saved trained prototype weights to: {output_weights_path}")

    model.eval()
    return model


if __name__ == "__main__":
    train_synthetic_model()
