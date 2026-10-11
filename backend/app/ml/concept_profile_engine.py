"""
Real Codeforces Concept Profile Engine (Phase 2 Step 1).
Provides offline-dataset-driven learning profile calculations:
- Bayesian smoothed concept mastery (Beta-Binomial conjugate prior, alpha=1, beta=1)
- Concept-level confidence calculation (interaction threshold K)
- Weakness score (1 - mastery) and 5-tier weakness level classification
- Real Codeforces concept gap matching (*special excluded)
- User difficulty target calculation (average solved rating + configurable challenge margin)
- Weak concepts discovery (weakness >= threshold, sorted descending)
- Graceful cold-start handling for unknown learners and unseen concepts

Guarantees:
- Codeforces dataset files are accessed strictly read-only via app.data.dataset_loader.
- No synthetic or fabricated learner data.
- The special metadata tag '*special' is excluded from all learning concepts and gaps.
- Does not modify or replace the existing 10-topic synthetic LSTM state engine yet.
"""

from typing import List, Dict, Any, Optional, Set
from functools import lru_cache
import logging

from app.data.dataset_loader import (
    load_problems,
    load_user_tag_weakness,
    load_user_rating_weakness,
    load_user_features,
    filter_learning_concepts,
    get_distinct_learning_concepts,
    get_problem_by_id,
)

logger = logging.getLogger(__name__)

# Configurable Mathematical Constants
DEFAULT_ALPHA: float = 1.0
DEFAULT_BETA: float = 1.0
DEFAULT_CONFIDENCE_K: float = 10.0
DEFAULT_CHALLENGE_MARGIN: int = 150
MIN_CODEFORCES_RATING: int = 800
MAX_CODEFORCES_RATING: int = 3500
WEAKNESS_THRESHOLD: float = 0.35

# Weakness Level Boundaries (from Colab ML pipeline)
WEAKNESS_LEVEL_VERY_LOW: str = "Very Low"       # <= 0.20
WEAKNESS_LEVEL_LOW: str = "Low"                 # (0.20, 0.35]
WEAKNESS_LEVEL_MODERATE: str = "Moderate"       # (0.35, 0.50]
WEAKNESS_LEVEL_HIGH: str = "High"               # (0.50, 0.65]
WEAKNESS_LEVEL_VERY_HIGH: str = "Very High"     # > 0.65


def calculate_bayesian_mastery(
    solved: int,
    interactions: int,
    alpha: float = DEFAULT_ALPHA,
    beta: float = DEFAULT_BETA
) -> float:
    """
    Computes Bayesian-smoothed concept mastery score using Laplace / Beta-Binomial prior:
        M_c = (S_c + alpha) / (N_c + alpha + beta)

    Where:
        S_c = solved count for concept
        N_c = total interactions/attempts for concept
        alpha = prior success (default: 1.0)
        beta = prior failure (default: 1.0)

    For 0 interactions (cold start): M_c = (0 + 1) / (0 + 2) = 0.5 (neutral prior).
    Guarantees value is bounded in [0.0, 1.0].
    """
    s = max(0, int(solved))
    n = max(s, int(interactions))
    a = max(0.0001, float(alpha))
    b = max(0.0001, float(beta))

    score = (s + a) / (n + a + b)
    return round(max(0.0, min(1.0, score)), 4)


def calculate_concept_confidence(
    interactions: int,
    k: float = DEFAULT_CONFIDENCE_K
) -> float:
    """
    Computes concept evaluation confidence score separately from mastery:
        C_c = min(1.0, N_c / K)

    Where:
        N_c = total interactions for concept
        K = interaction saturation threshold (default: 10.0)

    Guarantees:
        - Value is strictly bounded in [0.0, 1.0].
        - Confidence is NEVER multiplied into mastery.
    """
    n = max(0, int(interactions))
    threshold = max(0.0001, float(k))
    conf = min(1.0, n / threshold)
    return round(max(0.0, min(1.0, conf)), 4)


def calculate_weakness_score(mastery_score: float) -> float:
    """
    Computes concept weakness score independently from confidence:
        W_c = 1.0 - M_c

    Guarantees value is bounded in [0.0, 1.0].
    Does NOT use effective_weakness = weakness * confidence.
    """
    m = max(0.0, min(1.0, float(mastery_score)))
    return round(max(0.0, min(1.0, 1.0 - m)), 4)


def get_weakness_level(weakness_score: float) -> str:
    """
    Categorizes concept weakness into 5 standardized tiers:
    - Very Low:  weakness <= 0.20
    - Low:       0.20 < weakness <= 0.35
    - Moderate:  0.35 < weakness <= 0.50
    - High:      0.50 < weakness <= 0.65
    - Very High: weakness > 0.65
    """
    w = max(0.0, min(1.0, float(weakness_score)))
    if w <= 0.20:
        return WEAKNESS_LEVEL_VERY_LOW
    elif w <= 0.35:
        return WEAKNESS_LEVEL_LOW
    elif w <= 0.50:
        return WEAKNESS_LEVEL_MODERATE
    elif w <= 0.65:
        return WEAKNESS_LEVEL_HIGH
    else:
        return WEAKNESS_LEVEL_VERY_HIGH


def calculate_learning_target(
    avg_solved_rating: float,
    challenge_margin: int = DEFAULT_CHALLENGE_MARGIN,
    min_rating: int = MIN_CODEFORCES_RATING,
    max_rating: int = MAX_CODEFORCES_RATING
) -> int:
    """
    Computes optimal challenge rating target:
        learning_target = round(avg_solved_rating + challenge_margin)
    Clipped to valid Codeforces rating range [min_rating, max_rating].
    """
    target = round(float(avg_solved_rating) + float(challenge_margin))
    return int(max(min_rating, min(max_rating, target)))


@lru_cache(maxsize=1)
def _get_indexed_user_tag_weakness() -> Dict[str, Dict[str, Dict[str, Any]]]:
    """
    Internal cached index of user × concept interaction statistics.
    Keyed by: user -> concept_tag -> stats_dict.
    Filters out metadata tags like '*special'.
    """
    df = load_user_tag_weakness()
    user_map: Dict[str, Dict[str, Dict[str, Any]]] = {}

    for _, row in df.iterrows():
        raw_tag = str(row["tag"]).strip().lower()
        # Exclude *special and metadata tags
        if raw_tag in {"*special"} or not raw_tag:
            continue

        u = str(row["user"]).strip()
        if u not in user_map:
            user_map[u] = {}

        attempts = int(row.get("attempts", 0))
        solved = int(row.get("solved", 0))
        avg_rating = float(row.get("avg_rating", 0.0))

        user_map[u][raw_tag] = {
            "attempts": attempts,
            "solved": solved,
            "solve_rate": float(row.get("solve_rate", 0.0)),
            "avg_rating": avg_rating,
        }

    return user_map


@lru_cache(maxsize=1)
def _get_indexed_user_features() -> Dict[str, Dict[str, Any]]:
    """
    Internal cached index of user-level feature aggregations.
    Keyed by user handle string.
    """
    df = load_user_features()
    feature_map: Dict[str, Dict[str, Any]] = {}

    for _, row in df.iterrows():
        u = str(row["user"]).strip()
        feature_map[u] = {
            "user": u,
            "solved": int(row.get("solved", 0)),
            "attempts": int(row.get("attempts", 0)),
            "solve_rate": float(row.get("solve_rate", 0.0)),
            "avg_attempts": float(row.get("avg_attempts", 0.0)),
            "avg_problem_rating": float(row.get("avg_problem_rating", 0.0)),
            "max_problem_rating": float(row.get("max_problem_rating", 0.0)),
            "rating": float(row.get("rating", 0.0)),
            "max_rating": float(row.get("max_rating", 0.0)),
        }

    return feature_map


def get_user_concept_profile(
    user_id: Any,
    alpha: float = DEFAULT_ALPHA,
    beta: float = DEFAULT_BETA,
    k: float = DEFAULT_CONFIDENCE_K
) -> Dict[str, Dict[str, Any]]:
    """
    Constructs comprehensive concept-level learning profile across all real Codeforces concepts.
    Guarantees:
    - *special is strictly excluded from concepts.
    - All distinct learning concepts (~37 concepts) are returned.
    - Cold-start / unseen concepts receive deterministic neutral prior (mastery=0.5, weakness=0.5, confidence=0.0).
    - Returns dictionary mapping concept_name -> profile_dict.
    """
    user_key = str(user_id).strip()
    tag_map = _get_indexed_user_tag_weakness()
    user_tags = tag_map.get(user_key, {})

    all_concepts = get_distinct_learning_concepts()
    profile: Dict[str, Dict[str, Any]] = {}

    for concept in all_concepts:
        if concept in user_tags:
            c_data = user_tags[concept]
            interactions = c_data["attempts"]
            solved_count = c_data["solved"]
            total_attempts = interactions
            avg_attempts = round(interactions / max(1, solved_count), 2)
            avg_rating = c_data["avg_rating"]
            max_rating = avg_rating  # Representative rating for tag bucket
        else:
            # Unseen concept or cold-start unknown learner
            interactions = 0
            solved_count = 0
            total_attempts = 0
            avg_attempts = 0.0
            avg_rating = 0.0
            max_rating = 0.0

        mastery_score = calculate_bayesian_mastery(solved_count, interactions, alpha=alpha, beta=beta)
        confidence = calculate_concept_confidence(interactions, k=k)
        weakness_score = calculate_weakness_score(mastery_score)
        weakness_level = get_weakness_level(weakness_score)

        profile[concept] = {
            "user": user_key,
            "concept": concept,
            "interactions": interactions,
            "solved_count": solved_count,
            "total_attempts": total_attempts,
            "avg_attempts": avg_attempts,
            "avg_problem_rating": avg_rating,
            "max_problem_rating": max_rating,
            "smoothed_solve_rate": mastery_score,
            "mastery_score": mastery_score,
            "weakness_score": weakness_score,
            "confidence": confidence,
            "weakness_confidence": confidence,
            "weakness_level": weakness_level,
        }

    return profile


def get_user_concept_profile_list(
    user_id: Any,
    alpha: float = DEFAULT_ALPHA,
    beta: float = DEFAULT_BETA,
    k: float = DEFAULT_CONFIDENCE_K
) -> List[Dict[str, Any]]:
    """
    Convenience wrapper returning user concept profile as an ordered list of concept dictionaries.
    """
    profile_dict = get_user_concept_profile(user_id, alpha=alpha, beta=beta, k=k)
    return [profile_dict[c] for c in sorted(profile_dict.keys())]


def get_user_difficulty_profile(
    user_id: Any,
    challenge_margin: int = DEFAULT_CHALLENGE_MARGIN,
    min_rating: int = MIN_CODEFORCES_RATING,
    max_rating: int = MAX_CODEFORCES_RATING
) -> Dict[str, Any]:
    """
    Computes difficulty profile and learning target based on authentic interaction history:
        learning_target = round(avg_solved_rating + challenge_margin)
    Clipped to [min_rating, max_rating].

    For unknown users or learners with 0 solved interactions:
        Defaults gracefully to base rating (min_rating = 800) + challenge_margin (target = 950).
    """
    user_key = str(user_id).strip()
    feat_map = _get_indexed_user_features()
    user_feats = feat_map.get(user_key)

    if user_feats and user_feats.get("solved", 0) > 0 and user_feats.get("avg_problem_rating", 0) > 0:
        avg_solved = float(user_feats["avg_problem_rating"])
        max_solved = float(user_feats["max_problem_rating"])
        user_rating = float(user_feats["rating"])
        is_known = True
    else:
        # Unknown user or learner without solved problems
        avg_solved = float(min_rating)
        max_solved = float(min_rating)
        user_rating = float(min_rating)
        is_known = False

    target = calculate_learning_target(
        avg_solved,
        challenge_margin=challenge_margin,
        min_rating=min_rating,
        max_rating=max_rating
    )

    return {
        "user": user_key,
        "is_known_user": is_known,
        "avg_solved_rating": avg_solved,
        "max_problem_rating": max_solved,
        "user_rating": user_rating,
        "challenge_margin": challenge_margin,
        "learning_target": target,
        "min_rating": min_rating,
        "max_rating": max_rating,
    }


def calculate_concepts_gap_for_user(
    user_id: Any,
    concepts: Any
) -> float:
    """
    Calculates problem-level concept gap for a given list or string of concepts:
    1. Removes '*special' and non-learning tags using filter_learning_concepts.
    2. Retrieves learner weakness score for each valid concept.
    3. Handles unseen/unknown concepts safely using neutral prior (0.50).
    4. Computes mean concept gap score in [0.0, 1.0].
    """
    if isinstance(concepts, (list, tuple, set)):
        valid_concepts = filter_learning_concepts(",".join(str(c) for c in concepts if str(c).strip()))
    else:
        valid_concepts = filter_learning_concepts(concepts)

    if not valid_concepts:
        # No applicable learning concepts
        return 0.0

    profile = get_user_concept_profile(user_id)
    weaknesses = []

    for c in valid_concepts:
        if c in profile:
            weaknesses.append(profile[c]["weakness_score"])
        else:
            # Neutral fallback for unrecognized concept
            weaknesses.append(0.50)

    gap = sum(weaknesses) / len(weaknesses)
    return round(max(0.0, min(1.0, gap)), 4)


def calculate_concept_gap(
    user_id: Any,
    problem_id: str
) -> float:
    """
    Calculates concept gap between a learner and a Codeforces problem catalog entry.
    Loads problem metadata, cleans learning concepts (excluding '*special'),
    and computes the composite concept gap score in [0.0, 1.0].
    """
    problem = get_problem_by_id(str(problem_id).strip())
    if not problem:
        raise ValueError(f"Problem '{problem_id}' not found in Codeforces catalog.")

    concepts = problem.get("concepts", [])
    return calculate_concepts_gap_for_user(user_id, concepts)


def get_weak_concepts(
    user_id: Any,
    threshold: float = WEAKNESS_THRESHOLD,
    min_confidence: float = 0.0
) -> List[Dict[str, Any]]:
    """
    Identifies and returns all concepts where learner weakness meets or exceeds threshold:
        weakness_score >= threshold (default: 0.35)
    Optionally filters by minimum confidence (default: 0.0).
    Sorted descending by weakness_score (highest priority first), with alphabetical tie-breaking.
    """
    profile = get_user_concept_profile(user_id)
    weak_list = []

    for item in profile.values():
        w = item["weakness_score"]
        conf = item["confidence"]
        if w >= threshold and conf >= min_confidence:
            weak_list.append(item)

    # Sort descending by weakness score, tie-break by concept name ascending
    weak_list.sort(key=lambda x: (-x["weakness_score"], x["concept"]))
    return weak_list
