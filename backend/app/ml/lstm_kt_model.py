"""
PyTorch LSTM Knowledge Tracing (KT) Model for LeetCode Adaptive Learning.
Predicts learner mastery across 10 core DSA topics from interaction sequences.
"""
import os
import logging
from typing import Optional, Tuple, Dict, Any, List
import torch
import torch.nn as nn

logger = logging.getLogger(__name__)

# Constants
NUM_TOPICS = 10
FEATURE_DIM = 13  # 10 topic one-hot + 1 difficulty + 1 correctness + 1 normalized time
HIDDEN_SIZE = 64
DEFAULT_WEIGHTS_PATH = os.path.join(os.path.dirname(__file__), "lstm_kt_weights.pt")

# Topic ID to Index Mapping (1-based topic_id to 0-based index)
TOPIC_ID_MAP = {
    1: 0,   # Arrays
    2: 1,   # Strings
    3: 2,   # Hashing
    4: 3,   # Linked Lists
    5: 4,   # Stack & Queue
    6: 5,   # Trees
    7: 6,   # Graphs
    8: 7,   # Greedy Algorithms
    9: 8,   # Dynamic Programming
    10: 9,  # Backtracking
}

DIFFICULTY_MAP = {
    "easy": 0.33,
    "medium": 0.66,
    "hard": 1.00,
}


class LSTMKnowledgeTracingModel(nn.Module):
    """
    Recurrent Neural Network for Deep Knowledge Tracing.
    Takes sequential learner problem interactions and outputs 10 topic mastery probabilities in [0.0, 1.0].
    """
    def __init__(self, input_size: int = FEATURE_DIM, hidden_size: int = HIDDEN_SIZE, num_topics: int = NUM_TOPICS):
        super().__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_topics = num_topics

        # Sequence modeling layer
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=1,
            batch_first=True
        )

        # Topic mastery output projection
        self.fc_layers = nn.Sequential(
            nn.Linear(hidden_size, 32),
            nn.ReLU(),
            nn.Linear(32, num_topics),
            nn.Sigmoid()
        )

    def forward(
        self,
        x: torch.Tensor,
        hidden: Optional[Tuple[torch.Tensor, torch.Tensor]] = None
    ) -> Tuple[torch.Tensor, Tuple[torch.Tensor, torch.Tensor]]:
        """
        Forward pass.
        :param x: Tensor of shape [batch_size, seq_len, input_size]
        :param hidden: Optional tuple (h_0, c_0)
        :return: (mastery_scores [batch_size, seq_len, num_topics], (h_n, c_n))
        """
        lstm_out, hidden_state = self.lstm(x, hidden)
        mastery = self.fc_layers(lstm_out)
        return mastery, hidden_state

    def predict_latest_mastery(
        self,
        x: torch.Tensor,
        hidden: Optional[Tuple[torch.Tensor, torch.Tensor]] = None
    ) -> torch.Tensor:
        """
        Runs the interaction sequence and returns the final timestep mastery scores [batch_size, num_topics].
        """
        self.eval()
        with torch.no_grad():
            mastery_seq, _ = self.forward(x, hidden)
            # Take last timestep: [batch_size, num_topics]
            latest_mastery = mastery_seq[:, -1, :]
        return latest_mastery


def encode_interaction(
    topic_id: int,
    difficulty: str,
    is_correct: bool,
    time_ms: float = 0.0
) -> torch.Tensor:
    """
    Encodes a single learner interaction into a 13-dimensional feature tensor [1, 1, 13].
    """
    feature = torch.zeros(1, 1, FEATURE_DIM, dtype=torch.float32)

    # 1. One-hot topic encoding (indices 0..9)
    topic_idx = TOPIC_ID_MAP.get(topic_id, 0)
    feature[0, 0, topic_idx] = 1.0

    # 2. Difficulty scalar (index 10)
    diff_val = DIFFICULTY_MAP.get(str(difficulty).lower(), 0.5)
    feature[0, 0, 10] = diff_val

    # 3. Correctness binary scalar (index 11)
    feature[0, 0, 11] = 1.0 if is_correct else 0.0

    # 4. Normalized time scalar (index 12, clamped to [0, 1])
    # Assume 0 - 3000 ms typical range for code runner execution
    norm_time = min(max(float(time_ms) / 3000.0, 0.0), 1.0)
    feature[0, 0, 12] = norm_time

    return feature


def build_interaction_sequence(interactions: List[Dict[str, Any]]) -> torch.Tensor:
    """
    Builds a batch interaction sequence tensor [1, seq_len, 13] from a list of interaction dicts.
    Each dict should have: { 'topic_id': int, 'difficulty': str, 'is_correct': bool, 'time_ms': float }
    """
    if not interactions:
        return torch.zeros(1, 0, FEATURE_DIM, dtype=torch.float32)

    features = []
    for item in interactions:
        f = encode_interaction(
            topic_id=item.get("topic_id", 1),
            difficulty=item.get("difficulty", "Easy"),
            is_correct=bool(item.get("is_correct", False)),
            time_ms=float(item.get("time_ms", 0.0))
        )
        features.append(f.squeeze(0).squeeze(0))

    seq_tensor = torch.stack(features, dim=0).unsqueeze(0)  # [1, seq_len, 13]
    return seq_tensor


def load_trained_model(weights_path: str = DEFAULT_WEIGHTS_PATH) -> LSTMKnowledgeTracingModel:
    """
    Factory function to instantiate and load the LSTM KT model.
    If weights file is missing or corrupted, uses deterministic fallback initialization without crashing.
    """
    model = LSTMKnowledgeTracingModel()

    if os.path.exists(weights_path):
        try:
            state_dict = torch.load(weights_path, map_location=torch.device("cpu"), weights_only=True)
            model.load_state_dict(state_dict)
            logger.info(f"Loaded trained LSTM KT model weights from {weights_path}")
        except Exception as e:
            logger.warning(f"Could not load weights from {weights_path} ({e}). Using initialized weights.")
    else:
        logger.info(f"Weights file not found at {weights_path}. Using initialized prototype weights.")

    model.eval()
    return model
