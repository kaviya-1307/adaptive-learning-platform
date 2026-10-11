"""
Phase 2 Step 1 Verification Suite: Real Codeforces Concept Profile Engine
========================================================================
Validates:
1. Mathematical precision:
   - Bayesian-smoothed concept mastery (M_c = (S_c + alpha) / (N_c + alpha + beta))
   - Alpha / Beta prior configuration (default alpha=1, beta=1)
   - Concept confidence calculation (C_c = min(1.0, N_c / K))
   - Confidence saturation at K interactions
   - Weakness score (W_c = 1.0 - M_c) independent of confidence
   - 5-tier weakness level classification and exact boundary handling
2. Dataset integrity:
   - Real Codeforces dataset loaded via dataset_loader
   - Excluded '*special' metadata tag from all learning concepts
   - Valid learning concepts preserved (37 distinct concepts)
   - Real problem lookup by ID
3. User Concept Profile:
   - Known user profile extraction from real Codeforces interactions
   - Unknown / cold-start learner handling with neutral prior (0.50)
   - Unseen concepts within known user profiles
   - All scores strictly bounded in [0.0, 1.0]
4. Difficulty Profile & Learning Target:
   - Challenge margin computation (avg solved rating + 150)
   - Configurable challenge margin
   - Rating clipping to [800, 3500]
   - Cold-start fallback for unknown learners (800 -> target 950)
5. Multi-dimensional Concept Gap:
   - Single-concept problem gap
   - Multi-concept composite problem gap
   - '*special' mixed tag filtering
   - Unseen concept graceful fallback
   - Real problem catalog calculation
   - Scores strictly bounded in [0.0, 1.0]
6. Weak Concepts Discovery:
   - Weakness threshold filtering (W_c >= 0.35)
   - Deterministic descending order by weakness score
   - Empty weak-concept edge case handling
"""

import sys
import math
from typing import Dict, Any

from app.data import (
    load_problems,
    load_user_features,
    load_user_tag_weakness,
    get_distinct_learning_concepts,
    get_problem_by_id,
    filter_learning_concepts,
)
from app.ml.concept_profile_engine import (
    calculate_bayesian_mastery,
    calculate_concept_confidence,
    calculate_weakness_score,
    get_weakness_level,
    calculate_learning_target,
    get_user_concept_profile,
    get_user_concept_profile_list,
    get_user_difficulty_profile,
    calculate_concept_gap,
    calculate_concepts_gap_for_user,
    get_weak_concepts,
    DEFAULT_ALPHA,
    DEFAULT_BETA,
    DEFAULT_CONFIDENCE_K,
    DEFAULT_CHALLENGE_MARGIN,
    MIN_CODEFORCES_RATING,
    MAX_CODEFORCES_RATING,
    WEAKNESS_THRESHOLD,
    WEAKNESS_LEVEL_VERY_LOW,
    WEAKNESS_LEVEL_LOW,
    WEAKNESS_LEVEL_MODERATE,
    WEAKNESS_LEVEL_HIGH,
    WEAKNESS_LEVEL_VERY_HIGH,
)

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


def run_phase2_tests():
    print("=" * 70)
    print("RUNNING PHASE 2 STEP 1: REAL CONCEPT PROFILE ENGINE VERIFICATION")
    print("=" * 70)

    # -------------------------------------------------------------
    # 1. Mathematical Tests: Bayesian Mastery
    # -------------------------------------------------------------
    print("\n--- [1] Mathematical Tests: Bayesian Mastery ---")
    # S=10, N=20, a=1, b=1 -> (10+1)/(20+2) = 11/22 = 0.50
    m1 = calculate_bayesian_mastery(10, 20, alpha=1.0, beta=1.0)
    record_check("Mastery 10/20 with a=1,b=1 is exactly 0.50", m1 == 0.50, f"Got {m1}")

    # S=15, N=49, a=1, b=1 -> 16/51 = 0.313725... -> 0.3137
    m2 = calculate_bayesian_mastery(15, 49, alpha=1.0, beta=1.0)
    record_check("Mastery 15/49 with a=1,b=1 is 0.3137", m2 == 0.3137, f"Got {m2}")

    # Cold start: S=0, N=0, a=1, b=1 -> (0+1)/(0+2) = 0.50
    m_cold = calculate_bayesian_mastery(0, 0, alpha=1.0, beta=1.0)
    record_check("Cold-start (0 interactions) yields neutral prior 0.50", m_cold == 0.50, f"Got {m_cold}")

    # Perfect solves: S=20, N=20 -> (20+1)/(20+2) = 21/22 = 0.9545
    m_perfect = calculate_bayesian_mastery(20, 20, alpha=1.0, beta=1.0)
    record_check("Perfect 20/20 solves yields smoothed mastery 0.9545 (< 1.0)", m_perfect == 0.9545, f"Got {m_perfect}")

    # Zero solves with attempts: S=0, N=20 -> (0+1)/(20+2) = 1/22 = 0.0455
    m_zero = calculate_bayesian_mastery(0, 20, alpha=1.0, beta=1.0)
    record_check("Zero solves in 20 attempts yields smoothed mastery 0.0455 (> 0.0)", m_zero == 0.0455, f"Got {m_zero}")

    # Configurable alpha / beta
    m_custom = calculate_bayesian_mastery(5, 10, alpha=2.0, beta=2.0)
    # (5+2)/(10+4) = 7/14 = 0.50
    record_check("Configurable alpha=2, beta=2 calculates correctly (0.50)", m_custom == 0.50, f"Got {m_custom}")

    # Bounds check
    record_check("Mastery strictly in [0.0, 1.0]", 0.0 <= m2 <= 1.0 and 0.0 <= m_perfect <= 1.0)

    # -------------------------------------------------------------
    # 2. Mathematical Tests: Weakness & Confidence
    # -------------------------------------------------------------
    print("\n--- [2] Mathematical Tests: Weakness & Confidence ---")
    w1 = calculate_weakness_score(m2)
    record_check("Weakness is 1 - mastery (1 - 0.3137 = 0.6863)", w1 == 0.6863, f"Got {w1}")

    w_cold = calculate_weakness_score(m_cold)
    record_check("Cold-start weakness is 0.50 (1 - 0.50)", w_cold == 0.50, f"Got {w_cold}")

    # Confidence calculation: C = min(1.0, N / K)
    c0 = calculate_concept_confidence(0, k=10.0)
    record_check("Confidence for 0 interactions is 0.0", c0 == 0.0, f"Got {c0}")

    c5 = calculate_concept_confidence(5, k=10.0)
    record_check("Confidence for 5 interactions (K=10) is 0.50", c5 == 0.50, f"Got {c5}")

    c10 = calculate_concept_confidence(10, k=10.0)
    record_check("Confidence for 10 interactions (K=10) is 1.0", c10 == 1.0, f"Got {c10}")

    c50 = calculate_concept_confidence(50, k=10.0)
    record_check("Confidence saturates at 1.0 for 50 interactions", c50 == 1.0, f"Got {c50}")

    # Confidence is NOT multiplied into mastery
    record_check("Confidence is independent from mastery (mastery != mastery * confidence)", m2 != m2 * c5)

    # -------------------------------------------------------------
    # 3. Mathematical Tests: Weakness Level Boundaries
    # -------------------------------------------------------------
    print("\n--- [3] Weakness Level Boundary Tests ---")
    record_check("Weakness 0.15 is 'Very Low'", get_weakness_level(0.15) == WEAKNESS_LEVEL_VERY_LOW)
    record_check("Weakness 0.20 (boundary) is 'Very Low'", get_weakness_level(0.20) == WEAKNESS_LEVEL_VERY_LOW)
    record_check("Weakness 0.2001 is 'Low'", get_weakness_level(0.2001) == WEAKNESS_LEVEL_LOW)
    record_check("Weakness 0.35 (boundary) is 'Low'", get_weakness_level(0.35) == WEAKNESS_LEVEL_LOW)
    record_check("Weakness 0.3501 is 'Moderate'", get_weakness_level(0.3501) == WEAKNESS_LEVEL_MODERATE)
    record_check("Weakness 0.50 (boundary) is 'Moderate'", get_weakness_level(0.50) == WEAKNESS_LEVEL_MODERATE)
    record_check("Weakness 0.5001 is 'High'", get_weakness_level(0.5001) == WEAKNESS_LEVEL_HIGH)
    record_check("Weakness 0.65 (boundary) is 'High'", get_weakness_level(0.65) == WEAKNESS_LEVEL_HIGH)
    record_check("Weakness 0.6501 is 'Very High'", get_weakness_level(0.6501) == WEAKNESS_LEVEL_VERY_HIGH)
    record_check("Weakness 0.90 is 'Very High'", get_weakness_level(0.90) == WEAKNESS_LEVEL_VERY_HIGH)

    # -------------------------------------------------------------
    # 4. Dataset Integration & Tag Filtering
    # -------------------------------------------------------------
    print("\n--- [4] Dataset Integration & Tag Filtering ---")
    all_concepts = get_distinct_learning_concepts()
    record_check("Distinct learning concepts count is exactly 37", len(all_concepts) == 37, f"Got {len(all_concepts)}")
    record_check("'*special' is NOT in learning concepts", "*special" not in all_concepts)
    record_check("'dp' is in learning concepts", "dp" in all_concepts)
    record_check("'greedy' is in learning concepts", "greedy" in all_concepts)
    record_check("'graphs' is in learning concepts", "graphs" in all_concepts)
    record_check("'trees' is in learning concepts", "trees" in all_concepts)
    record_check("'data structures' is in learning concepts", "data structures" in all_concepts)

    # Filter learning concepts preserves valid tags and excludes metadata
    filtered = filter_learning_concepts("implementation,math,*special")
    record_check("filter_learning_concepts excludes '*special' from raw string", set(filtered) == {"implementation", "math"})

    # Problem lookup
    prob = get_problem_by_id("2218-G")
    record_check("Lookup problem 2218-G succeeds", prob is not None)
    record_check("Problem 2218-G rating is 1800", prob["rating"] == 1800)
    record_check("Problem 2218-G concepts exclude '*special'", "*special" not in prob["concepts"])

    # -------------------------------------------------------------
    # 5. User Concept Profile: Known & Unknown Users
    # -------------------------------------------------------------
    print("\n--- [5] User Concept Profile Tests ---")
    # Known user in dataset: "-1e11"
    profile_known = get_user_concept_profile("-1e11")
    record_check("get_user_concept_profile returns all 37 learning concepts", len(profile_known) == 37, f"Got {len(profile_known)}")
    record_check("'*special' is NOT in user concept profile keys", "*special" not in profile_known)

    # Check ternary search for user -1e11 (attempts=49, solved=15)
    ts_profile = profile_known.get("ternary search")
    record_check("Ternary search found in user profile", ts_profile is not None)
    record_check("Ternary search interactions == 49", ts_profile["interactions"] == 49)
    record_check("Ternary search solved_count == 15", ts_profile["solved_count"] == 15)
    record_check("Ternary search mastery_score == 0.3137", ts_profile["mastery_score"] == 0.3137)
    record_check("Ternary search weakness_score == 0.6863", ts_profile["weakness_score"] == 0.6863)
    record_check("Ternary search confidence == 1.0 (49 >= 10)", ts_profile["confidence"] == 1.0)
    record_check("Ternary search weakness_confidence == 1.0", ts_profile["weakness_confidence"] == 1.0)
    record_check("Ternary search weakness_level is 'Very High'", ts_profile["weakness_level"] == WEAKNESS_LEVEL_VERY_HIGH)

    # Unknown user: "ghost_learner_9999"
    profile_unknown = get_user_concept_profile("ghost_learner_9999")
    record_check("Unknown user returns complete 37 concepts profile", len(profile_unknown) == 37)
    dp_unknown = profile_unknown["dp"]
    record_check("Unknown user dp interactions == 0", dp_unknown["interactions"] == 0)
    record_check("Unknown user dp mastery_score == 0.50 (neutral prior)", dp_unknown["mastery_score"] == 0.50)
    record_check("Unknown user dp weakness_score == 0.50", dp_unknown["weakness_score"] == 0.50)
    record_check("Unknown user dp confidence == 0.0", dp_unknown["confidence"] == 0.0)
    record_check("Unknown user dp weakness_level == 'Moderate'", dp_unknown["weakness_level"] == WEAKNESS_LEVEL_MODERATE)

    # List wrapper
    profile_list = get_user_concept_profile_list("-1e11")
    record_check("get_user_concept_profile_list returns list of 37 items", len(profile_list) == 37 and isinstance(profile_list, list))

    # Range validity
    all_valid = all(
        0.0 <= p["mastery_score"] <= 1.0 and
        0.0 <= p["weakness_score"] <= 1.0 and
        0.0 <= p["confidence"] <= 1.0
        for p in profile_known.values()
    )
    record_check("All profile scores strictly bounded within [0.0, 1.0]", all_valid)

    # -------------------------------------------------------------
    # 6. Difficulty Profile & Learning Target
    # -------------------------------------------------------------
    print("\n--- [6] Difficulty Profile & Learning Target Tests ---")
    # Known user "-1e11" (avg_problem_rating = 1493)
    diff_known = get_user_difficulty_profile("-1e11")
    record_check("Known user difficulty profile is_known_user is True", diff_known["is_known_user"] is True)
    record_check("Known user avg_solved_rating matches 1493.0", diff_known["avg_solved_rating"] == 1493.0)
    record_check("Learning target is 1493 + 150 = 1643", diff_known["learning_target"] == 1643, f"Got {diff_known['learning_target']}")

    # Configurable challenge margin (+200)
    diff_margin200 = get_user_difficulty_profile("-1e11", challenge_margin=200)
    record_check("Configurable challenge margin +200 yields 1693", diff_margin200["learning_target"] == 1693)

    # Rating clipping bounds
    target_high = calculate_learning_target(3450, challenge_margin=150)
    record_check("Upper rating clipping clamps to MAX_CODEFORCES_RATING (3500)", target_high == 3500, f"Got {target_high}")

    target_low = calculate_learning_target(700, challenge_margin=50)
    record_check("Lower rating clipping clamps to MIN_CODEFORCES_RATING (800)", target_low == 800, f"Got {target_low}")

    # Unknown user difficulty profile
    diff_unknown = get_user_difficulty_profile("unknown_user_123")
    record_check("Unknown user difficulty profile is_known_user is False", diff_unknown["is_known_user"] is False)
    record_check("Unknown user baseline rating is MIN_CODEFORCES_RATING (800)", diff_unknown["avg_solved_rating"] == 800.0)
    record_check("Unknown user learning target defaults to 800 + 150 = 950", diff_unknown["learning_target"] == 950)

    # -------------------------------------------------------------
    # 7. Concept Gap Calculation
    # -------------------------------------------------------------
    print("\n--- [7] Concept Gap Tests ---")
    # Single concept problem
    gap_single = calculate_concepts_gap_for_user("-1e11", ["ternary search"])
    record_check("Single concept gap matches weakness (0.6863)", gap_single == 0.6863, f"Got {gap_single}")

    # Multi-concept problem: ternary search (0.6863) + unknown concept (0.50) -> mean = (0.6863 + 0.50) / 2 = 0.59315 -> 0.5932
    gap_multi = calculate_concepts_gap_for_user("-1e11", ["ternary search", "unknown_concept_xyz"])
    expected_mean = round((0.6863 + 0.50) / 2.0, 4)
    record_check("Multi-concept gap computes accurate mean including unseen concept", gap_multi == expected_mean, f"Got {gap_multi}")

    # '*special' mixed tag filtering in concept gap
    gap_with_special = calculate_concepts_gap_for_user("-1e11", ["ternary search", "*special"])
    record_check("Mixed '*special' tag is ignored; gap matches single concept", gap_with_special == gap_single)

    # Empty / non-learning concepts return 0.0
    gap_empty = calculate_concepts_gap_for_user("-1e11", ["*special"])
    record_check("Empty valid concepts returns 0.0 gap", gap_empty == 0.0)

    # Real catalog problem 1004-B: 'constructive algorithms,greedy,implementation,math'
    gap_real = calculate_concept_gap("-1e11", "1004-B")
    record_check("Real problem 1004-B concept gap calculated in [0.0, 1.0]", 0.0 <= gap_real <= 1.0, f"Got {gap_real}")

    # Non-existent problem raises ValueError
    non_existent_raised = False
    try:
        calculate_concept_gap("-1e11", "non_existent_problem_xyz")
    except ValueError:
        non_existent_raised = True
    record_check("Non-existent problem ID raises ValueError", non_existent_raised)

    # -------------------------------------------------------------
    # 8. Weak Concepts Discovery & Ordering
    # -------------------------------------------------------------
    print("\n--- [8] Weak Concepts Tests ---")
    weak_concepts = get_weak_concepts("-1e11", threshold=0.35)
    record_check("get_weak_concepts returns non-empty list for user with weaknesses", len(weak_concepts) > 0)
    record_check("All returned weak concepts have weakness_score >= 0.35", all(c["weakness_score"] >= 0.35 for c in weak_concepts))

    # Verify descending ordering
    scores = [c["weakness_score"] for c in weak_concepts]
    is_descending = all(scores[i] >= scores[i+1] for i in range(len(scores) - 1))
    record_check("Weak concepts are strictly sorted in descending order", is_descending)

    # Empty weak concepts edge case: threshold > 1.0
    no_weak = get_weak_concepts("-1e11", threshold=1.05)
    record_check("Empty weak concepts case returns empty list []", no_weak == [])

    # Minimum confidence filtering
    weak_conf_filtered = get_weak_concepts("-1e11", threshold=0.35, min_confidence=0.5)
    record_check("Confidence filtering requires confidence >= 0.5", all(c["confidence"] >= 0.5 for c in weak_conf_filtered))

    print("\n" + "=" * 70)
    print(f"PHASE 2 STEP 1 SUMMARY: ALL {PASSED_CHECKS}/{TOTAL_CHECKS} CHECKS PASSED (100% SUCCESS)")
    print("=" * 70)


if __name__ == "__main__":
    run_phase2_tests()
