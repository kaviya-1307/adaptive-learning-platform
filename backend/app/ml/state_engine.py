"""
Knowledge State Engine for Learner Mastery Tracing (Phase 2 Step 2).
Manages database knowledge states and concept-level learning profiles:
- Live submissions update real Codeforces concept states using Bayesian smoothing
- Eliminates synthetic LSTM dependency from the live state update path
- Maintains backward-compatible 10 DSA topic states for platform recommendations and dashboards
- Resolves application problem concepts to real Codeforces learning concepts (*special excluded)
- Distinguishes cold-start (unseen concept, confidence=0) from actual learner weakness
"""
import logging
import math
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session, joinedload

from app.models.learner_knowledge_state import LearnerKnowledgeState
from app.models.learner_concept_state import LearnerConceptState
from app.models.topic import Topic
from app.models.problem import Problem
from app.models.submission import Submission
from app.models.diagnostic_attempt import DiagnosticAttempt
from app.models.user import User

from app.ml.concept_profile_engine import (
    calculate_bayesian_mastery,
    calculate_concept_confidence,
    calculate_weakness_score,
    get_weakness_level,
    filter_learning_concepts,
    get_distinct_learning_concepts,
)
from app.ml.lstm_kt_model import (
    load_trained_model,
    encode_interaction,
    build_interaction_sequence,
    TOPIC_ID_MAP,
    DIFFICULTY_MAP,
    NUM_TOPICS,
)

logger = logging.getLogger(__name__)

# Experience level prior fallbacks
EXPERIENCE_PRIOR_MAP = {
    "beginner": {"mastery": 0.25, "confidence": 0.30},
    "intermediate": {"mastery": 0.50, "confidence": 0.40},
    "advanced": {"mastery": 0.75, "confidence": 0.50},
}

# Topic slug to standard Codeforces learning concepts mapping
TOPIC_SLUG_TO_CONCEPTS: Dict[str, List[str]] = {
    "arrays": ["data structures", "implementation"],
    "strings": ["strings"],
    "hashing": ["hashing", "data structures"],
    "linked-lists": ["data structures"],
    "stack-queue": ["data structures"],
    "trees": ["trees", "dfs and similar"],
    "graphs": ["graphs", "dfs and similar"],
    "greedy": ["greedy"],
    "dynamic-programming": ["dp"],
    "backtracking": ["dfs and similar", "brute force"],
}

# Granular overrides for curated application problem slugs
PROBLEM_SLUG_TO_CONCEPTS: Dict[str, List[str]] = {
    "two-sum-target-pair": ["hashing", "data structures"],
    "best-time-to-buy-and-sell-stock": ["greedy", "data structures"],
    "maximum-subarray-sum": ["dp", "greedy"],
    "product-of-array-except-self": ["math", "data structures"],
    "trapping-rain-water": ["two pointers", "data structures"],
    "valid-anagram-check": ["strings", "hashing"],
    "valid-palindrome": ["two pointers", "strings"],
    "longest-substring-without-repeating-characters": ["two pointers", "hashing", "strings"],
    "group-anagrams": ["hashing", "sortings", "strings"],
    "subarray-sum-equals-k": ["hashing", "data structures"],
    "contains-duplicate": ["hashing", "data structures"],
    "top-k-frequent-elements": ["hashing", "data structures"],
    "longest-consecutive-sequence": ["hashing", "data structures"],
    "reverse-linked-list": ["data structures"],
    "merge-two-sorted-lists": ["two pointers", "data structures"],
    "remove-nth-node-from-end-of-list": ["two pointers", "data structures"],
    "valid-parentheses": ["data structures"],
    "evaluate-reverse-polish-notation": ["data structures", "expression parsing"],
    "daily-temperatures": ["data structures"],
    "largest-rectangle-in-histogram": ["data structures"],
    "maximum-depth-of-binary-tree": ["trees", "dfs and similar"],
    "invert-binary-tree": ["trees", "dfs and similar"],
    "lowest-common-ancestor-of-bst": ["trees", "dfs and similar"],
    "validate-binary-search-tree": ["trees", "dfs and similar"],
    "binary-tree-maximum-path-sum": ["trees", "dp", "dfs and similar"],
    "number-of-connected-islands": ["graphs", "dfs and similar"],
    "clone-graph": ["graphs", "dfs and similar"],
    "course-schedule": ["graphs", "dfs and similar"],
    "word-ladder": ["graphs", "shortest paths"],
    "jump-game": ["greedy", "dp"],
    "gas-station": ["greedy"],
    "task-scheduler": ["greedy", "math"],
    "climbing-stairs-min-cost": ["dp"],
    "coin-change": ["dp"],
    "longest-increasing-subsequence": ["dp", "binary search"],
    "unique-paths": ["dp", "math"],
    "edit-distance": ["dp", "strings"],
    "subsets": ["bitmasks", "dfs and similar"],
    "combination-sum": ["dfs and similar", "brute force"],
    "n-queens": ["dfs and similar", "brute force"],
}


def get_problem_learning_concepts(problem: Problem) -> List[str]:
    """
    Resolves the real Codeforces learning concepts for an application problem.
    1. Checks granular problem slug mapping.
    2. Falls back to problem topic slug mapping.
    3. Falls back to documented default ['data structures', 'implementation'].
    4. Strictly removes '*special' and non-learning tags.
    """
    slug = str(getattr(problem, "slug", "") or "").strip().lower()
    if slug in PROBLEM_SLUG_TO_CONCEPTS:
        raw_concepts = PROBLEM_SLUG_TO_CONCEPTS[slug]
    else:
        topic_slug = ""
        if hasattr(problem, "topic") and problem.topic:
            topic_slug = str(problem.topic.slug or "").strip().lower()
        if topic_slug in TOPIC_SLUG_TO_CONCEPTS:
            raw_concepts = TOPIC_SLUG_TO_CONCEPTS[topic_slug]
        else:
            raw_concepts = ["data structures", "implementation"]

    return filter_learning_concepts(",".join(raw_concepts))


def get_mastery_level_label(score: float) -> str:
    """
    Categorizes numerical mastery score into pedagogical tier.
    """
    if score >= 0.85:
        return "Master"
    elif score >= 0.60:
        return "Proficient"
    elif score >= 0.35:
        return "Developing"
    else:
        return "Novice"


class KnowledgeStateEngine:
    """
    State tracking engine that interfaces between the application database
    and the real Codeforces concept profile engine.
    """
    _model_instance = None

    @classmethod
    def get_model(cls):
        """
        Legacy factory retained strictly for backward compatibility and rollback inspection.
        NOTE: Not used by update_state_from_submission() or recalculate_user_knowledge_state().
        """
        if cls._model_instance is None:
            cls._model_instance = load_trained_model()
        return cls._model_instance

    @classmethod
    def get_or_initialize_user_states(
        cls,
        db: Session,
        user_id: int
    ) -> List[LearnerKnowledgeState]:
        """
        Retrieves existing knowledge state for all 10 topics for a learner.
        If any topic rows are missing, initializes them using onboarding prior or defaults.
        """
        all_topics = db.query(Topic).order_by(Topic.order_index).all()
        existing_states = (
            db.query(LearnerKnowledgeState)
            .options(joinedload(LearnerKnowledgeState.topic))
            .filter(LearnerKnowledgeState.user_id == user_id)
            .all()
        )
        existing_map = {s.topic_id: s for s in existing_states}

        # Determine user experience prior
        user = db.query(User).filter(User.id == user_id).first()
        exp_level = "beginner"
        if user and user.onboarding_profile:
            exp_level = user.onboarding_profile.experience_level or "beginner"
        prior = EXPERIENCE_PRIOR_MAP.get(str(exp_level).lower(), {"mastery": 0.25, "confidence": 0.30})

        created_any = False
        final_states = []

        for topic in all_topics:
            if topic.id in existing_map:
                final_states.append(existing_map[topic.id])
            else:
                new_state = LearnerKnowledgeState(
                    user_id=user_id,
                    topic_id=topic.id,
                    mastery_score=prior["mastery"],
                    confidence_score=prior["confidence"],
                    total_interactions=0
                )
                db.add(new_state)
                final_states.append(new_state)
                created_any = True

        if created_any:
            db.commit()
            for s in final_states:
                db.refresh(s)

        final_states.sort(key=lambda s: s.topic.order_index if s.topic else s.topic_id)
        return final_states

    @classmethod
    def get_or_initialize_user_concept_states(
        cls,
        db: Session,
        user_id: int
    ) -> List[LearnerConceptState]:
        """
        Retrieves or initializes learner concept states across all 37 distinct Codeforces learning concepts.
        If user has diagnostic attempts, seeds initial evidence from diagnostic history.
        Otherwise, initializes with neutral Bayesian prior (mastery=0.5, weakness=0.5, confidence=0.0).
        """
        all_concepts = get_distinct_learning_concepts()
        existing = (
            db.query(LearnerConceptState)
            .filter(LearnerConceptState.user_id == user_id)
            .all()
        )
        existing_map = {cs.concept: cs for cs in existing}

        # Check for diagnostic attempts to seed initial application evidence
        diag_attempts = (
            db.query(DiagnosticAttempt)
            .options(joinedload(DiagnosticAttempt.problem).joinedload(Problem.topic))
            .filter(DiagnosticAttempt.user_id == user_id)
            .all()
        )
        concept_evidence: Dict[str, Dict[str, int]] = {}
        for da in diag_attempts:
            if da.problem:
                c_list = get_problem_learning_concepts(da.problem)
                for c in c_list:
                    if c not in concept_evidence:
                        concept_evidence[c] = {"interactions": 0, "solved": 0}
                    concept_evidence[c]["interactions"] += 1
                    if da.is_solved:
                        concept_evidence[c]["solved"] += 1

        created_any = False
        final_states = []

        for concept in all_concepts:
            if concept in existing_map:
                final_states.append(existing_map[concept])
            else:
                ev = concept_evidence.get(concept, {"interactions": 0, "solved": 0})
                n = ev["interactions"]
                s = ev["solved"]
                m = calculate_bayesian_mastery(s, n)
                w = calculate_weakness_score(m)
                c = calculate_concept_confidence(n)
                wl = get_weakness_level(w)

                new_state = LearnerConceptState(
                    user_id=user_id,
                    concept=concept,
                    mastery_score=m,
                    weakness_score=w,
                    confidence_score=c,
                    weakness_level=wl,
                    interactions=n,
                    solved_count=s
                )
                db.add(new_state)
                final_states.append(new_state)
                created_any = True

        if created_any:
            db.commit()
            for cs in final_states:
                db.refresh(cs)

        final_states.sort(key=lambda cs: cs.concept)
        return final_states

    @classmethod
    def get_user_concept_states(
        cls,
        db: Session,
        user_id: int
    ) -> List[LearnerConceptState]:
        """
        Returns all concept states for a learner.
        """
        return (
            db.query(LearnerConceptState)
            .filter(LearnerConceptState.user_id == user_id)
            .order_by(LearnerConceptState.concept.asc())
            .all()
        )

    @classmethod
    def update_concept_states_from_diagnostic(
        cls,
        db: Session,
        user_id: int
    ) -> List[LearnerConceptState]:
        """
        Calibrates and updates learner concept states based on diagnostic assessment attempts.
        Guarantees:
        - Mapped learning concepts receive empirical evidence from actual diagnostic problem attempts.
        - Correct answers increase Bayesian mastery and confidence while lowering weakness.
        - Failed answers decrease Bayesian mastery, raising weakness with positive confidence (confirmed weakness).
        - Concepts not evaluated in the diagnostic maintain neutral Bayesian prior (0.50) with 0.0 confidence.
        - No fake Codeforces history, fabricated interactions, or artificial submissions.
        - Combines safely with existing practice submissions without double-counting.
        """
        # Ensure all 37 concept states exist
        concept_states = cls.get_or_initialize_user_concept_states(db, user_id)
        concept_map = {cs.concept: cs for cs in concept_states}

        # Check for user's diagnostic attempts
        diag_attempts = (
            db.query(DiagnosticAttempt)
            .options(joinedload(DiagnosticAttempt.problem).joinedload(Problem.topic))
            .filter(DiagnosticAttempt.user_id == user_id)
            .all()
        )

        # Also check for user's existing regular practice submissions
        submissions = (
            db.query(Submission)
            .options(joinedload(Submission.problem).joinedload(Problem.topic))
            .filter(Submission.user_id == user_id)
            .all()
        )

        # Aggregate evidence per concept
        concept_evidence: Dict[str, Dict[str, int]] = {}
        for da in diag_attempts:
            if da.problem:
                c_list = get_problem_learning_concepts(da.problem)
                for c in c_list:
                    if c not in concept_evidence:
                        concept_evidence[c] = {"interactions": 0, "solved": 0}
                    concept_evidence[c]["interactions"] += 1
                    if da.is_solved:
                        concept_evidence[c]["solved"] += 1

        for sub in submissions:
            if sub.problem:
                c_list = get_problem_learning_concepts(sub.problem)
                for c in c_list:
                    if c not in concept_evidence:
                        concept_evidence[c] = {"interactions": 0, "solved": 0}
                    concept_evidence[c]["interactions"] += 1
                    if sub.status == "Accepted":
                        concept_evidence[c]["solved"] += 1

        for concept, cs in concept_map.items():
            if concept in concept_evidence:
                n = concept_evidence[concept]["interactions"]
                s = concept_evidence[concept]["solved"]
                m = calculate_bayesian_mastery(s, n)
                w = calculate_weakness_score(m)
                conf = calculate_concept_confidence(n)
                wl = get_weakness_level(w)

                cs.interactions = n
                cs.solved_count = s
                cs.mastery_score = m
                cs.weakness_score = w
                cs.confidence_score = conf
                cs.weakness_level = wl
            else:
                # If zero interactions, ensure neutral prior
                if cs.interactions == 0:
                    cs.mastery_score = 0.50
                    cs.weakness_score = 0.50
                    cs.confidence_score = 0.00
                    cs.weakness_level = "Moderate"
                    cs.solved_count = 0

        db.commit()
        for cs in concept_states:
            db.refresh(cs)

        logger.info(f"[Phase 2 Diagnostic Integration] Updated concept states for user {user_id} across {len(diag_attempts)} diagnostic attempts.")
        return concept_states

    @classmethod
    def update_state_from_submission(
        cls,
        db: Session,
        user_id: int,
        problem: Problem,
        submission: Submission
    ) -> Dict[str, Any]:
        """
        Processes a single submission through the real concept-profile engine.
        Updates granular concept-level states for all concepts mapped to the problem,
        and updates the topic-level knowledge state without calling the synthetic LSTM.
        Guarantees:
        - No calls to get_model(), predict_latest_mastery(), or lstm_kt_weights.pt.
        - Preserves existing topic-level contract for backward compatibility.
        """
        is_correct = (submission.status == "Accepted")
        difficulty_str = problem.difficulty or "Medium"
        diff_scalar = DIFFICULTY_MAP.get(difficulty_str.lower(), 0.5)

        # 1. Update concept-level knowledge states for all concepts in the problem
        concepts = get_problem_learning_concepts(problem)
        cls.get_or_initialize_user_concept_states(db, user_id)

        updated_concept_states = []
        for concept in concepts:
            c_state = (
                db.query(LearnerConceptState)
                .filter(
                    LearnerConceptState.user_id == user_id,
                    LearnerConceptState.concept == concept
                )
                .first()
            )
            if not c_state:
                c_state = LearnerConceptState(
                    user_id=user_id,
                    concept=concept,
                    interactions=0,
                    solved_count=0
                )
                db.add(c_state)

            c_state.interactions += 1
            if is_correct:
                c_state.solved_count += 1

            c_state.mastery_score = calculate_bayesian_mastery(
                c_state.solved_count,
                c_state.interactions
            )
            c_state.confidence_score = calculate_concept_confidence(
                c_state.interactions
            )
            c_state.weakness_score = calculate_weakness_score(c_state.mastery_score)
            c_state.weakness_level = get_weakness_level(c_state.weakness_score)
            updated_concept_states.append(c_state)

        # 2. Update topic-level state for problem.topic_id (deterministic update, NO LSTM!)
        cls.get_or_initialize_user_states(db, user_id)
        topic_id = problem.topic_id
        target_state = (
            db.query(LearnerKnowledgeState)
            .filter(
                LearnerKnowledgeState.user_id == user_id,
                LearnerKnowledgeState.topic_id == topic_id
            )
            .first()
        )

        old_mastery = target_state.mastery_score if target_state else 0.25
        if target_state:
            target_state.total_interactions += 1
            n = target_state.total_interactions

            if is_correct:
                gain_factor = 0.05 + diff_scalar * 0.07  # Easy: +0.073, Med: +0.096, Hard: +0.12
                new_mastery = min(0.99, old_mastery + gain_factor)
            else:
                penalty_factor = 0.04 + (1.0 - diff_scalar) * 0.05  # Easy fail: -0.073, Hard fail: -0.04
                new_mastery = max(0.05, old_mastery - penalty_factor)

            target_state.mastery_score = round(float(new_mastery), 4)
            interaction_conf = min(0.95, 0.30 + 0.15 * math.log(1 + n))
            target_state.confidence_score = round(max(0.20, min(0.95, interaction_conf)), 4)

        db.commit()
        if target_state:
            db.refresh(target_state)
        for cs in updated_concept_states:
            db.refresh(cs)

        logger.info(
            f"[Phase 2 KT Update] user={user_id}, topic='{problem.topic.name if problem.topic else topic_id}', "
            f"concepts={concepts}, status={submission.status}, "
            f"topic_mastery: {old_mastery:.3f} -> {target_state.mastery_score if target_state else 0.0:.3f}"
        )

        return {
            "topic_id": topic_id,
            "topic_name": problem.topic.name if problem.topic else str(topic_id),
            "old_mastery": old_mastery,
            "new_mastery": target_state.mastery_score if target_state else 0.0,
            "confidence": target_state.confidence_score if target_state else 0.0,
            "total_interactions": target_state.total_interactions if target_state else 0,
            "mastery_level": get_mastery_level_label(target_state.mastery_score) if target_state else "Novice",
            "concepts_updated": [cs.concept for cs in updated_concept_states],
            "concept_states": [
                {
                    "concept": cs.concept,
                    "mastery_score": cs.mastery_score,
                    "weakness_score": cs.weakness_score,
                    "confidence": cs.confidence_score,
                    "weakness_level": cs.weakness_level,
                    "interactions": cs.interactions,
                    "solved_count": cs.solved_count,
                }
                for cs in updated_concept_states
            ],
        }

    @classmethod
    def recalculate_user_knowledge_state(
        cls,
        db: Session,
        user_id: int
    ) -> List[LearnerKnowledgeState]:
        """
        Reconstructs the full chronological interaction history (diagnostic attempts + submissions)
        and recomputes both the 10-topic knowledge states and concept-level states
        using deterministic Bayesian updates without calling the synthetic LSTM.
        """
        # Ensure base states exist
        topic_states = cls.get_or_initialize_user_states(db, user_id)
        topic_state_map = {s.topic_id: s for s in topic_states}

        concept_states = cls.get_or_initialize_user_concept_states(db, user_id)
        concept_state_map = {cs.concept: cs for cs in concept_states}

        # Reset concept states to neutral priors
        for cs in concept_states:
            cs.interactions = 0
            cs.solved_count = 0
            cs.mastery_score = 0.50
            cs.weakness_score = 0.50
            cs.confidence_score = 0.0
            cs.weakness_level = "Moderate"

        # 1. Fetch user onboarding prior as baseline for topics
        user = db.query(User).filter(User.id == user_id).first()
        exp_level = "beginner"
        if user and user.onboarding_profile:
            exp_level = user.onboarding_profile.experience_level or "beginner"
        prior = EXPERIENCE_PRIOR_MAP.get(str(exp_level).lower(), {"mastery": 0.25, "confidence": 0.30})

        for s in topic_states:
            s.mastery_score = prior["mastery"]
            s.confidence_score = prior["confidence"]
            s.total_interactions = 0

        # 2. Gather diagnostic attempts
        diag_attempts = (
            db.query(DiagnosticAttempt)
            .options(joinedload(DiagnosticAttempt.problem).joinedload(Problem.topic))
            .filter(DiagnosticAttempt.user_id == user_id)
            .order_by(DiagnosticAttempt.created_at.asc())
            .all()
        )

        # 3. Gather code submissions
        submissions = (
            db.query(Submission)
            .options(joinedload(Submission.problem).joinedload(Problem.topic))
            .filter(Submission.user_id == user_id)
            .order_by(Submission.created_at.asc())
            .all()
        )

        # 4. Build unified chronological event list
        events = []
        for d in diag_attempts:
            if d.problem:
                events.append({
                    "timestamp": d.created_at,
                    "problem": d.problem,
                    "topic_id": d.problem.topic_id,
                    "difficulty": d.problem.difficulty or "Medium",
                    "is_correct": d.is_solved,
                })

        for s in submissions:
            if s.problem:
                events.append({
                    "timestamp": s.created_at,
                    "problem": s.problem,
                    "topic_id": s.problem.topic_id,
                    "difficulty": s.problem.difficulty or "Medium",
                    "is_correct": (s.status == "Accepted"),
                })

        events.sort(key=lambda e: e["timestamp"] if e["timestamp"] else 0)

        # 5. Sequential update (NO LSTM!)
        for ev in events:
            problem = ev["problem"]
            is_corr = ev["is_correct"]
            diff_str = ev["difficulty"]
            diff_scalar = DIFFICULTY_MAP.get(diff_str.lower(), 0.5)

            # Concept updates
            concepts = get_problem_learning_concepts(problem)
            for concept in concepts:
                cs = concept_state_map.get(concept)
                if cs:
                    cs.interactions += 1
                    if is_corr:
                        cs.solved_count += 1
                    cs.mastery_score = calculate_bayesian_mastery(cs.solved_count, cs.interactions)
                    cs.confidence_score = calculate_concept_confidence(cs.interactions)
                    cs.weakness_score = calculate_weakness_score(cs.mastery_score)
                    cs.weakness_level = get_weakness_level(cs.weakness_score)

            # Topic update
            tid = ev["topic_id"]
            t_state = topic_state_map.get(tid)
            if t_state:
                old_m = t_state.mastery_score
                t_state.total_interactions += 1
                n = t_state.total_interactions

                if is_corr:
                    gain = 0.05 + diff_scalar * 0.07
                    new_m = min(0.99, old_m + gain)
                else:
                    pen = 0.04 + (1.0 - diff_scalar) * 0.05
                    new_m = max(0.05, old_m - pen)

                t_state.mastery_score = round(float(new_m), 4)
                interaction_conf = min(0.95, 0.30 + 0.15 * math.log(1 + n))
                t_state.confidence_score = round(max(0.20, min(0.95, interaction_conf)), 4)

        db.commit()
        for s in topic_states:
            db.refresh(s)
        for cs in concept_states:
            db.refresh(cs)

        logger.info(f"Recalculated knowledge states for user {user_id} across {len(events)} interactions.")
        return topic_states
