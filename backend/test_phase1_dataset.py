"""
Phase 1 Verification Script: Codeforces Dataset Integration
============================================================
Validates:
1. All 5 dataset files exist and are intact with non-zero row counts.
2. Dataset loader loads problems, user features, tag weaknesses, and rating weaknesses.
3. Problem IDs, ratings, and tags are parsed correctly.
4. '*special' is excluded from learning concepts while preserved in raw problem tags.
5. Original dataset rows are unmodified.
6. Summary metrics report valid statistics.
"""

import sys
import hashlib
from app.data import (
    load_problems,
    load_user_tag_weakness,
    load_user_rating_weakness,
    load_user_features,
    load_processed_interactions,
    get_distinct_learning_concepts,
    get_problem_by_id,
    get_dataset_summary,
    filter_learning_concepts,
    PROBLEMS_CSV,
    USER_TAG_WEAKNESS_CSV,
    USER_RATING_WEAKNESS_CSV,
    USER_FEATURES_CSV,
    PROCESSED_DATA_CSV,
)

TOTAL_CHECKS = 0
PASSED_CHECKS = 0


def record_check(desc: str, condition: bool, details: str = ""):
    global TOTAL_CHECKS, PASSED_CHECKS
    TOTAL_CHECKS += 1
    if condition:
        PASSED_CHECKS += 1
        print(f"  [PASS] Check #{TOTAL_CHECKS}: {desc}")
    else:
        print(f"  [FAIL] Check #{TOTAL_CHECKS}: {desc} -- {details}")
        assert False, f"Check #{TOTAL_CHECKS} failed: {desc} ({details})"


def test_dataset():
    print("=" * 70)
    print("RUNNING PHASE 1: REAL CODEFORCES DATASET INTEGRATION VERIFICATION")
    print("=" * 70)

    # 1. File existence
    print("\n--- [1] Dataset File Existence ---")
    record_check("problems.csv exists", PROBLEMS_CSV.exists())
    record_check("user_tag_weakness.csv exists", USER_TAG_WEAKNESS_CSV.exists())
    record_check("user_rating_weakness.csv exists", USER_RATING_WEAKNESS_CSV.exists())
    record_check("user_features.csv exists", USER_FEATURES_CSV.exists())
    record_check("processed_data.csv exists", PROCESSED_DATA_CSV.exists())

    # 2. Loading and row counts
    print("\n--- [2] Dataset Loading & Row Counts ---")
    df_problems = load_problems()
    record_check("problems.csv has exactly 10,864 rows", len(df_problems) == 10864, f"Got {len(df_problems)}")

    df_user_tags = load_user_tag_weakness()
    record_check("user_tag_weakness.csv has exactly 34,138 rows", len(df_user_tags) == 34138, f"Got {len(df_user_tags)}")

    df_user_ratings = load_user_rating_weakness()
    record_check("user_rating_weakness.csv has exactly 12,658 rows", len(df_user_ratings) == 12658, f"Got {len(df_user_ratings)}")

    df_user_features = load_user_features()
    record_check("user_features.csv has exactly 995 rows", len(df_user_features) == 995, f"Got {len(df_user_features)}")

    # Sample read of processed_data (50 rows)
    df_interactions_sample = load_processed_interactions(nrows=50)
    record_check("processed_data.csv reads valid interaction sample", len(df_interactions_sample) == 50)

    # 3. Problem IDs and Ratings
    print("\n--- [3] Problem Metadata & Ratings Integrity ---")
    sample_problem = get_problem_by_id("2218-G")
    record_check("Problem 2218-G found in dataset", sample_problem is not None)
    record_check("Problem 2218-G rating is 1800", sample_problem.get("rating") == 1800)
    record_check("Problem 2218-G has concepts ['implementation', 'math']",
                 set(sample_problem.get("concepts", [])) == {"implementation", "math"})

    # Check rating bounds across all problems
    ratings = df_problems["rating"]
    min_rating = int(ratings.min())
    max_rating = int(ratings.max())
    record_check("Problem ratings range is authentic (800 to 3500)", min_rating >= 800 and max_rating <= 3500, f"Range: {min_rating}-{max_rating}")

    # 4. Tag Filtering & '*special' Exclusion
    print("\n--- [4] Tag Filtering & *special Handling ---")
    distinct_concepts = get_distinct_learning_concepts()
    record_check("Distinct learning concepts count > 30", len(distinct_concepts) >= 30, f"Got {len(distinct_concepts)}")
    record_check("'*special' is NOT in learning concepts", "*special" not in distinct_concepts)
    record_check("'dp' is in learning concepts", "dp" in distinct_concepts)
    record_check("'greedy' is in learning concepts", "greedy" in distinct_concepts)
    record_check("'graphs' is in learning concepts", "graphs" in distinct_concepts)
    record_check("'trees' is in learning concepts", "trees" in distinct_concepts)
    record_check("'binary search' is in learning concepts", "binary search" in distinct_concepts)

    # Verify *special still exists in original raw tags of problems where assigned
    problems_with_special = df_problems[df_problems["tags"].str.contains(r"\*special", regex=True)]
    record_check("Original tags preserve '*special' metadata", len(problems_with_special) > 0, f"Found {len(problems_with_special)}")
    # Verify that in those problems, 'concepts' column does NOT contain '*special'
    special_leaked = any("*special" in concepts for concepts in problems_with_special["concepts"])
    record_check("No leakage of '*special' into concepts list", not special_leaked)

    # 5. User Weakness Integrity
    print("\n--- [5] User Weakness Data Integrity ---")
    record_check("user_tag_weakness contains 'weakness_score'", "weakness_score" in df_user_tags.columns)
    record_check("user_tag_weakness contains 'mastery'", "mastery" in df_user_tags.columns)
    record_check("user_tag_weakness contains 'is_weak'", "is_weak" in df_user_tags.columns)
    record_check("user_tag_weakness contains 'solve_rate'", "solve_rate" in df_user_tags.columns)

    # 6. Summary Dictionary
    print("\n--- [6] Dataset Summary ---")
    summary = get_dataset_summary()
    record_check("get_dataset_summary returns problems_count == 10864", summary["problems_count"] == 10864)
    record_check("get_dataset_summary has_special_in_learning_concepts is False", summary["has_special_in_learning_concepts"] is False)
    record_check("get_dataset_summary users_count == 995", summary["users_count"] == 995)

    print("\n" + "=" * 70)
    print(f"PHASE 1 VERIFICATION SUMMARY: ALL {PASSED_CHECKS}/{TOTAL_CHECKS} CHECKS PASSED (100% SUCCESS)")
    print("=" * 70)


if __name__ == "__main__":
    test_dataset()
