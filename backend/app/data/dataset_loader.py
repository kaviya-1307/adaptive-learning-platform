"""
Codeforces Dataset Loader Utility.
Provides read-only access to the offline Codeforces User-Problem Interaction Dataset:
- Problem metadata (problem IDs, ratings, tags)
- User concept weaknesses and mastery
- User rating-bucket weaknesses
- User-level features
- Interaction logs

Guarantees:
- Original dataset files are preserved read-only.
- The special metadata tag '*special' is excluded from learning concepts,
  while preserved in original problem tags metadata.
- No synthetic records or fabricated user data.
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
from functools import lru_cache
import pandas as pd
import logging

logger = logging.getLogger(__name__)

# Base path to the dataset directory
DATA_DIR = Path(__file__).resolve().parent

# File paths
PROBLEMS_CSV = DATA_DIR / "problems.csv"
USER_TAG_WEAKNESS_CSV = DATA_DIR / "user_tag_weakness.csv"
USER_RATING_WEAKNESS_CSV = DATA_DIR / "user_rating_weakness.csv"
USER_FEATURES_CSV = DATA_DIR / "user_features.csv"
PROCESSED_DATA_CSV = DATA_DIR / "processed_data.csv"

# Special metadata tags that are NOT algorithmic learning concepts
EXCLUDED_CONCEPT_TAGS: Set[str] = {"*special"}


def filter_learning_concepts(tags_input: Any) -> List[str]:
    """
    Parses a comma-separated tag string or list of tags and excludes
    metadata tags such as '*special' from algorithmic learning concepts.
    Preserves all real Codeforces learning concepts.
    """
    if tags_input is None:
        return []

    if isinstance(tags_input, (list, tuple, set)):
        tag_list = [str(t).strip().lower() for t in tags_input if str(t).strip()]
    elif isinstance(tags_input, str):
        tag_list = [t.strip().lower() for t in tags_input.split(",") if t.strip()]
    elif pd.isna(tags_input):
        return []
    else:
        return []

    # Exclude metadata tags (e.g. *special)
    return [t for t in tag_list if t not in EXCLUDED_CONCEPT_TAGS]


@lru_cache(maxsize=1)
def load_problems() -> pd.DataFrame:
    """
    Loads the Codeforces problems catalog (10,864 problems).
    Columns: problem_id, rating, tags, concepts (filtered).
    Original 'tags' column is untouched.
    """
    if not PROBLEMS_CSV.exists():
        raise FileNotFoundError(f"problems.csv not found at {PROBLEMS_CSV}")

    df = pd.read_csv(PROBLEMS_CSV)
    df["rating"] = df["rating"].fillna(0).astype(int)
    df["tags"] = df["tags"].fillna("")
    # Add parsed learning concepts column (excluding '*special')
    df["concepts"] = df["tags"].apply(filter_learning_concepts)
    return df


@lru_cache(maxsize=1)
def load_user_tag_weakness() -> pd.DataFrame:
    """
    Loads user × concept weakness dataset (34,138 rows).
    Columns: user, tag, attempts, solved, solve_rate, avg_rating, mastery, skill_score, weakness_score, is_weak
    """
    if not USER_TAG_WEAKNESS_CSV.exists():
        raise FileNotFoundError(f"user_tag_weakness.csv not found at {USER_TAG_WEAKNESS_CSV}")

    return pd.read_csv(USER_TAG_WEAKNESS_CSV)


@lru_cache(maxsize=1)
def load_user_rating_weakness() -> pd.DataFrame:
    """
    Loads user × rating-bucket weakness dataset (12,658 rows).
    Columns: user, rating_bucket, attempts, solved, solve_rate, expected_rate, performance_ratio,
             avg_rating, mastery, skill_score, weakness_score, is_weak
    """
    if not USER_RATING_WEAKNESS_CSV.exists():
        raise FileNotFoundError(f"user_rating_weakness.csv not found at {USER_RATING_WEAKNESS_CSV}")

    return pd.read_csv(USER_RATING_WEAKNESS_CSV)


@lru_cache(maxsize=1)
def load_user_features() -> pd.DataFrame:
    """
    Loads user-level aggregated features (995 users).
    Columns: user, solved, attempts, solve_rate, avg_attempts, avg_problem_rating, max_problem_rating, rating, max_rating
    """
    if not USER_FEATURES_CSV.exists():
        raise FileNotFoundError(f"user_features.csv not found at {USER_FEATURES_CSV}")

    return pd.read_csv(USER_FEATURES_CSV)


def load_processed_interactions(nrows: Optional[int] = None) -> pd.DataFrame:
    """
    Loads raw user-problem interactions (up to 921,797 rows).
    Columns: user, problem_id, solved, attempts, rating, tags
    """
    if not PROCESSED_DATA_CSV.exists():
        raise FileNotFoundError(f"processed_data.csv not found at {PROCESSED_DATA_CSV}")

    return pd.read_csv(PROCESSED_DATA_CSV, nrows=nrows)


@lru_cache(maxsize=1)
def get_distinct_learning_concepts() -> List[str]:
    """
    Extracts all unique learning concepts across the entire problem set,
    guaranteeing that metadata tags such as '*special' are excluded.
    """
    df_problems = load_problems()
    concept_set: Set[str] = set()
    for concepts_list in df_problems["concepts"]:
        concept_set.update(concepts_list)
    return sorted(list(concept_set))


@lru_cache(maxsize=1024)
def get_problem_by_id(problem_id: str) -> Optional[Dict[str, Any]]:
    """
    Looks up problem metadata by Codeforces problem_id (e.g. '2218-G').
    Returns dict with problem_id, rating, raw tags, and valid learning concepts.
    """
    df = load_problems()
    matches = df[df["problem_id"] == str(problem_id).strip()]
    if matches.empty:
        return None
    row = matches.iloc[0]
    return {
        "problem_id": row["problem_id"],
        "rating": int(row["rating"]),
        "tags": str(row["tags"]),
        "concepts": list(row["concepts"]),
    }


def get_dataset_summary() -> Dict[str, Any]:
    """
    Returns high-level statistics of the integrated real Codeforces dataset.
    """
    df_problems = load_problems()
    df_tags = load_user_tag_weakness()
    df_ratings = load_user_rating_weakness()
    df_users = load_user_features()

    concepts = get_distinct_learning_concepts()

    return {
        "problems_count": len(df_problems),
        "ratings_range": [int(df_problems["rating"].min()), int(df_problems["rating"].max())],
        "unique_learning_concepts_count": len(concepts),
        "sample_learning_concepts": concepts[:10],
        "has_special_in_learning_concepts": "*special" in concepts,
        "users_count": len(df_users),
        "user_tag_interactions_count": len(df_tags),
        "user_rating_bucket_interactions_count": len(df_ratings),
        "dataset_files": {
            "problems.csv": PROBLEMS_CSV.exists(),
            "user_tag_weakness.csv": USER_TAG_WEAKNESS_CSV.exists(),
            "user_rating_weakness.csv": USER_RATING_WEAKNESS_CSV.exists(),
            "user_features.csv": USER_FEATURES_CSV.exists(),
            "processed_data.csv": PROCESSED_DATA_CSV.exists(),
        }
    }
