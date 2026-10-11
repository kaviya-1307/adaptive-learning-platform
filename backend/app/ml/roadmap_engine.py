"""
Adaptive Learning Roadmap Engine (Phase 2 Step 4).
Generates dynamic, personalized learning roadmaps based on the learner's current concept-level
knowledge state, prerequisite relationships, and empirical weakness targeting.
"""
import logging
from typing import List, Dict, Any, Optional, Set
from collections import defaultdict
from sqlalchemy.orm import Session

from app.models.problem import Problem
from app.models.learner_concept_state import LearnerConceptState
from app.ml.state_engine import (
    KnowledgeStateEngine,
    get_problem_learning_concepts,
)
from app.ml.concept_profile_engine import (
    get_distinct_learning_concepts,
    filter_learning_concepts,
)
from app.services.recommendation_engine import (
    RecommendationEngine,
    calculate_difficulty_fit,
    compute_recommendation_score,
)
from app.schemas.roadmap import (
    RoadmapConceptItem,
    RoadmapStage,
    RoadmapResponse,
)

logger = logging.getLogger(__name__)

# Documented Completion Thresholds
CONCEPT_COMPLETION_MASTERY_THRESHOLD: float = 0.70
CONCEPT_COMPLETION_CONFIDENCE_THRESHOLD: float = 0.20
STAGE_COMPLETION_MASTERY_THRESHOLD: float = 0.70
STAGE_COMPLETION_CONFIDENCE_THRESHOLD: float = 0.20

# 4 Broad Progression Stages mapping all 37 distinct Codeforces learning concepts (*special excluded)
ROADMAP_STAGES_CONFIG = [
    {
        "stage_id": "stage_foundations",
        "stage_name": "Foundations",
        "description": "Core implementation primitives, strings, basic mathematics, sorting, and hash tables.",
        "order": 1,
        "prerequisites": [],
        "concepts": [
            "implementation",
            "math",
            "brute force",
            "strings",
            "sortings",
            "hashing",
        ]
    },
    {
        "stage_id": "stage_data_structures",
        "stage_name": "Data Structures",
        "description": "Essential memory layouts, linear and hierarchical structures, trees, and disjoint-set unions.",
        "order": 2,
        "prerequisites": ["stage_foundations"],
        "concepts": [
            "data structures",
            "trees",
            "dsu",
        ]
    },
    {
        "stage_id": "stage_core_algorithms",
        "stage_name": "Core Algorithms",
        "description": "Binary search, two pointers, greedy choices, graph traversals, and divide-and-conquer strategies.",
        "order": 3,
        "prerequisites": ["stage_data_structures"],
        "concepts": [
            "binary search",
            "two pointers",
            "greedy",
            "dfs and similar",
            "graphs",
            "shortest paths",
            "divide and conquer",
            "ternary search",
            "constructive algorithms",
            "interactive",
            "communication",
            "schedules",
        ]
    },
    {
        "stage_id": "stage_advanced",
        "stage_name": "Advanced Algorithms",
        "description": "Dynamic programming, bit manipulation, network flows, and specialized algorithmic techniques.",
        "order": 4,
        "prerequisites": ["stage_core_algorithms"],
        "concepts": [
            "dp",
            "bitmasks",
            "combinatorics",
            "flows",
            "graph matchings",
            "meet-in-the-middle",
            "expression parsing",
            "matrices",
            "probabilities",
            "games",
            "geometry",
            "number theory",
            "string suffix structures",
            "2-sat",
            "fft",
            "chinese remainder theorem",
        ]
    },
]


class AdaptiveRoadmapEngine:
    """
    Engine for generating and progressing personalized, adaptive learning roadmaps.
    """

    @classmethod
    def is_concept_completed(cls, cs: LearnerConceptState) -> bool:
        """
        Documented rule: Concept is mastered/completed when mastery >= 0.70
        and confidence >= 0.20 (or solved_count >= 1 with mastery >= 0.65).
        """
        if cs.mastery_score >= CONCEPT_COMPLETION_MASTERY_THRESHOLD and cs.confidence_score >= CONCEPT_COMPLETION_CONFIDENCE_THRESHOLD:
            return True
        if cs.solved_count >= 1 and cs.mastery_score >= 0.65:
            return True
        return False

    @classmethod
    def determine_concept_status(
        cls,
        cs: LearnerConceptState,
        stage_unlocked: bool
    ) -> str:
        """
        Evaluates concept progression status: 'completed', 'in_progress', 'available', or 'locked'.
        """
        if cls.is_concept_completed(cs):
            return "completed"
        if cs.interactions > 0:
            return "in_progress"
        if stage_unlocked:
            return "available"
        return "locked"

    @classmethod
    def calculate_concept_priority(cls, cs: LearnerConceptState) -> int:
        """
        Calculates learning priority rank within a stage (1 = highest urgency):
        - Confirmed weakness (weakness >= 0.50 and confidence > 0.0) -> Priority 1
        - In-progress developing skill (interactions > 0 and mastery < 0.70) -> Priority 2
        - Unseen concept (interactions == 0) -> Priority 3
        - Completed concept -> Priority 4
        """
        if cls.is_concept_completed(cs):
            return 4
        if cs.weakness_score >= 0.50 and cs.confidence_score > 0.0:
            return 1
        if cs.interactions > 0:
            return 2
        return 3

    @classmethod
    def get_stage_recommended_problems(
        cls,
        db: Session,
        user_id: int,
        stage_concepts: List[str],
        concept_map: Dict[str, LearnerConceptState],
        learning_target: int,
        limit: int = 3
    ) -> List[int]:
        """
        Finds application problems covering this stage's concepts, excludes attempted problems,
        ranks them by recommendation score (0.60 * gap + 0.40 * fit), and returns top problem IDs.
        """
        attempted_ids = RecommendationEngine.get_attempted_problem_ids(db, user_id)
        all_problems = db.query(Problem).all()

        stage_concept_set = set(stage_concepts)
        eligible_candidates = []

        for p in all_problems:
            if p.id in attempted_ids:
                continue
            p_concepts = get_problem_learning_concepts(p)
            # Check overlap with stage concepts
            if any(c in stage_concept_set for c in p_concepts):
                gap = RecommendationEngine.calculate_candidate_concept_gap(p_concepts, concept_map)
                p_rating = RecommendationEngine.get_problem_rating(p)
                fit = calculate_difficulty_fit(p_rating, learning_target)
                score = compute_recommendation_score(gap, fit)
                eligible_candidates.append((score, p.id))

        # Sort descending by score, tie-break on problem ID
        eligible_candidates.sort(key=lambda item: (-item[0], item[1]))
        return [item[1] for item in eligible_candidates[:limit]]

    @classmethod
    def generate_roadmap(
        cls,
        db: Session,
        user_id: int
    ) -> RoadmapResponse:
        """
        Dynamically generates the complete adaptive roadmap for the learner:
        1. Reads persisted LearnerConceptState rows (does not reset learner state).
        2. Evaluates each of the 4 progression stages.
        3. Determines unlocking, status, priority, and completion per stage.
        4. Attaches personalized recommended problems from catalog.
        5. Computes overall roadmap completion percentage.
        """
        # 1. Fetch current persisted concept states
        concept_states = KnowledgeStateEngine.get_or_initialize_user_concept_states(db, user_id)
        concept_map: Dict[str, LearnerConceptState] = {cs.concept: cs for cs in concept_states}

        # 2. Learner learning target for problem ranking
        learning_target = RecommendationEngine.get_user_learning_target(db, user_id)

        # 3. Evaluate stages sequentially to handle prerequisites
        processed_stages: List[RoadmapStage] = []
        previous_stage_has_progress = True  # Foundations is always unlocked
        completed_stage_count = 0

        for stage_cfg in ROADMAP_STAGES_CONFIG:
            stage_id = stage_cfg["stage_id"]
            stage_name = stage_cfg["stage_name"]
            description = stage_cfg["description"]
            order = stage_cfg["order"]
            stage_concepts = stage_cfg["concepts"]

            # Filter to valid concepts in this stage (*special excluded)
            valid_stage_concepts = filter_learning_concepts(stage_concepts)

            # Check unlocking prerequisite
            is_unlocked = previous_stage_has_progress

            # Concept items evaluation
            concept_items: List[RoadmapConceptItem] = []
            stage_masteries = []
            stage_weaknesses = []
            stage_confidences = []
            stage_has_any_progress = False
            completed_concepts_in_stage = 0

            for c_name in valid_stage_concepts:
                cs = concept_map.get(c_name)
                if not cs:
                    continue

                c_status = cls.determine_concept_status(cs, stage_unlocked=is_unlocked)
                c_priority = cls.calculate_concept_priority(cs)

                if c_status == "completed":
                    completed_concepts_in_stage += 1
                if cs.interactions > 0 or c_status == "completed":
                    stage_has_any_progress = True

                stage_masteries.append(float(cs.mastery_score))
                stage_weaknesses.append(float(cs.weakness_score))
                stage_confidences.append(float(cs.confidence_score))

                # Recommended problems for this specific concept if weak
                concept_recs = []
                if c_status in ["available", "in_progress"]:
                    concept_recs = cls.get_stage_recommended_problems(
                        db, user_id, [c_name], concept_map, learning_target, limit=2
                    )

                is_confirmed = (float(cs.weakness_score) >= 0.50 and float(cs.confidence_score) > 0.0)
                concept_items.append(
                    RoadmapConceptItem(
                        concept=c_name,
                        mastery_score=round(float(cs.mastery_score), 4),
                        weakness_score=round(float(cs.weakness_score), 4),
                        confidence_score=round(float(cs.confidence_score), 4),
                        weakness_level=cs.weakness_level,
                        status=c_status,
                        priority=c_priority,
                        interactions=cs.interactions,
                        solved_count=cs.solved_count,
                        is_confirmed_weakness=is_confirmed,
                        recommended_problem_ids=concept_recs,
                    )
                )

            # Sort concepts within stage: highest priority first, then highest weakness
            concept_items.sort(key=lambda ci: (ci.priority, -ci.weakness_score, ci.concept))

            # Aggregate stage metrics
            avg_mastery = sum(stage_masteries) / max(1, len(stage_masteries))
            avg_weakness = sum(stage_weaknesses) / max(1, len(stage_weaknesses))
            avg_confidence = sum(stage_confidences) / max(1, len(stage_confidences))

            # Stage status evaluation
            is_stage_completed = (
                completed_concepts_in_stage == len(valid_stage_concepts) or
                (avg_mastery >= STAGE_COMPLETION_MASTERY_THRESHOLD and avg_confidence >= STAGE_COMPLETION_CONFIDENCE_THRESHOLD)
            )

            if is_stage_completed:
                stage_status = "completed"
                completed_stage_count += 1
            elif stage_has_any_progress:
                stage_status = "in_progress"
            elif is_unlocked:
                stage_status = "available"
            else:
                stage_status = "locked"

            # Recommended problems for the stage overall
            stage_recs = cls.get_stage_recommended_problems(
                db, user_id, valid_stage_concepts, concept_map, learning_target, limit=3
            )

            # Prerequisite condition for next stage: unlocked if this stage has progress or completed
            previous_stage_has_progress = (stage_has_any_progress or is_stage_completed)

            stage_prereqs = stage_cfg.get("prerequisites", [])
            total_concepts_cnt = len(valid_stage_concepts)
            stage_prog_pct = round((completed_concepts_in_stage / max(1, total_concepts_cnt)) * 100.0, 1)

            processed_stages.append(
                RoadmapStage(
                    stage_id=stage_id,
                    stage_name=stage_name,
                    description=description,
                    order_index=order,
                    prerequisites=stage_prereqs,
                    total_concepts=total_concepts_cnt,
                    completed_concepts=completed_concepts_in_stage,
                    progress_percent=stage_prog_pct,
                    status=stage_status,
                    priority=order,  # Will be adjusted below
                    mastery=round(avg_mastery, 4),
                    weakness=round(avg_weakness, 4),
                    confidence=round(avg_confidence, 4),
                    concepts=concept_items,
                    recommended_problem_ids=stage_recs,
                )
            )

        # 4. Resolve current focus stage and adjust stage priorities
        # Priority 1 is assigned to the active focus stage:
        # Check if any stage has a confirmed high weakness (weakness >= 0.55 and confidence > 0.0)
        confirmed_weak_stages = [
            s for s in processed_stages
            if s.status != "completed" and any(c.priority == 1 for c in s.concepts)
        ]

        if confirmed_weak_stages:
            focus_stage = confirmed_weak_stages[0]
        else:
            # Fall back to earliest non-completed stage
            non_completed = [s for s in processed_stages if s.status != "completed"]
            focus_stage = non_completed[0] if non_completed else processed_stages[-1]

        # Re-index priorities so current focus stage is Priority 1
        p_rank = 2
        for s in processed_stages:
            if s.stage_id == focus_stage.stage_id:
                s.priority = 1
            else:
                s.priority = p_rank
                p_rank += 1

        total_stages = len(processed_stages)
        overall_progress = round((completed_stage_count / total_stages) * 100.0, 1)

        return RoadmapResponse(
            user_id=user_id,
            current_stage=focus_stage.stage_name,
            current_stage_id=focus_stage.stage_id,
            total_stages=total_stages,
            completed_stages=completed_stage_count,
            overall_progress_percent=overall_progress,
            stages=processed_stages,
        )
