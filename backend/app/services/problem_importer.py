"""
Problem Importer & Dataset Audit Service for LeetCode Adaptive Learning Platform.
Phase 3 Step 2: Quality > Quantity Validation and Idempotent Import Pipeline.

Handles:
  1. Auditing external problem datasets (e.g. Codeforces problems.csv) against strict
     executable problem criteria.
  2. Recording explicit, auditable rejection reasons for incomplete/metadata-only candidates.
  3. Providing idempotent, safe problem import with transaction rollback protection.
  4. Reporting full platform problem catalog health metrics.
"""
import csv
import logging
import os
from collections import Counter
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy.orm import Session

from app.models.problem import Problem
from app.models.test_case import TestCase
from app.models.topic import Topic
from app.services.problem_validator import ProblemValidator, ValidationResult

logger = logging.getLogger(__name__)


# MBPP task IDs that are incompatible with deterministic sandbox judging
# (e.g., non-deterministic set comparisons, float precision variations, or recursion limits)
INCOMPATIBLE_MBPP_TASK_IDS = {
    2, 13, 40, 50, 75, 81, 88, 97, 106, 110, 114, 123, 124, 130, 143, 153, 156, 160,
    177, 182, 185, 193, 197, 205, 206, 213, 219, 223, 237, 243, 252, 255, 257, 259,
    261, 262, 273, 278, 280, 290, 299, 305, 310, 324, 341, 342, 343, 363, 367, 368,
    376, 393, 399, 401, 415, 417, 429, 440, 445, 470, 473, 475, 486, 490, 493, 512,
    528, 533, 534, 538, 560, 561, 579, 580, 582, 587, 590, 596, 599, 601, 607, 613,
    616, 642, 660, 691, 698, 703, 710, 715, 717, 720, 726, 740, 758, 766, 773, 779,
    780, 783, 785, 788, 791, 816, 819, 828, 862, 888, 894, 906, 912, 916, 920, 922,
    927, 936, 938, 940, 941, 945, 946, 949, 951, 963, 969
}


class ProblemImporter:
    """
    Manages safe, idempotent problem bank validation and ingestion.
    """

    @classmethod
    def audit_external_dataset(
        cls,
        csv_path: str,
        max_rows: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Audits an external dataset file (e.g. Codeforces problems.csv) against
        platform standards without writing to the database.

        Returns comprehensive statistics, rejection reasons, and schema compliance.
        """
        if not os.path.isabs(csv_path):
            csv_path = os.path.abspath(csv_path)

        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Dataset file not found at: {csv_path}")

        total_rows = 0
        valid_candidates: List[Dict[str, Any]] = []
        rejections: List[Dict[str, Any]] = []
        rejection_reason_counts: Counter = Counter()
        rating_values: List[float] = []
        unique_tags: Counter = Counter()

        with open(csv_path, mode="r", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            for row in reader:
                total_rows += 1
                if max_rows and total_rows > max_rows:
                    break

                # Track ratings and tags
                raw_rating = row.get("rating")
                if raw_rating:
                    try:
                        rating_values.append(float(raw_rating))
                    except (ValueError, TypeError):
                        pass

                raw_tags = row.get("tags")
                if raw_tags and raw_tags.lower() != "nan":
                    for t in raw_tags.split(","):
                        t_clean = t.strip().lower()
                        if t_clean:
                            unique_tags[t_clean] += 1

                # Validate against full candidate criteria
                result: ValidationResult = ProblemValidator.validate_dataset_candidate(row)

                if result.is_valid:
                    valid_candidates.append(row)
                else:
                    rejections.append({
                        "problem_id": row.get("problem_id"),
                        "errors": result.errors,
                        "warnings": result.warnings
                    })
                    for err in result.errors:
                        # Extract error code prefix before colon
                        err_code = err.split(":")[0].strip() if ":" in err else err
                        rejection_reason_counts[err_code] += 1

        rating_stats: Dict[str, Any] = {}
        if rating_values:
            sorted_ratings = sorted(rating_values)
            rating_stats = {
                "min": sorted_ratings[0],
                "max": sorted_ratings[-1],
                "median": sorted_ratings[len(sorted_ratings) // 2],
                "count": len(sorted_ratings)
            }

        return {
            "dataset_path": csv_path,
            "total_rows_inspected": total_rows,
            "valid_candidates_count": len(valid_candidates),
            "rejected_candidates_count": len(rejections),
            "valid_percentage": round(len(valid_candidates) / total_rows * 100.0, 4) if total_rows else 0.0,
            "rejection_reasons_summary": dict(rejection_reason_counts.most_common()),
            "rating_statistics": rating_stats,
            "top_tags": dict(unique_tags.most_common(15)),
            "sample_rejection": rejections[0] if rejections else None
        }

    @classmethod
    def import_problem(
        cls,
        db: Session,
        problem_data: Dict[str, Any],
        dry_run: bool = False,
        run_judge: bool = True
    ) -> Tuple[bool, str, Optional[Problem]]:
        """
        Idempotently validates and inserts a problem into the database.
        Rolls back on failure.
        """
        # 1. Check existing slug collision
        slug = problem_data.get("slug")
        if not slug:
            return False, "Missing required slug field", None

        existing = db.query(Problem).filter(Problem.slug == slug).first()
        if existing:
            return False, f"Problem with slug '{slug}' already exists (ID: {existing.id})", existing

        # 2. Topic validation
        topic_id = problem_data.get("topic_id")
        topic = db.query(Topic).filter(Topic.id == topic_id).first()
        if not topic:
            return False, f"Topic ID {topic_id} does not exist", None

        # 3. Create transient Problem and TestCase models
        problem = Problem(
            title=problem_data.get("title"),
            slug=slug,
            topic_id=topic_id,
            difficulty=problem_data.get("difficulty"),
            description_markdown=problem_data.get("description_markdown"),
            constraints_markdown=problem_data.get("constraints_markdown"),
            starter_code_python=problem_data.get("starter_code_python"),
            reference_solution_python=problem_data.get("reference_solution_python"),
            order_index=problem_data.get("order_index", 0),
            is_diagnostic=problem_data.get("is_diagnostic", False),
        )

        test_cases_data = problem_data.get("test_cases", [])
        for idx, tc_data in enumerate(test_cases_data):
            tc = TestCase(
                input_data=tc_data.get("input_data"),
                expected_output=str(tc_data.get("expected_output")),
                is_hidden=tc_data.get("is_hidden", False),
                order_index=tc_data.get("order_index", idx)
            )
            problem.test_cases.append(tc)

        # 4. Strict Validation
        val_result = ProblemValidator.validate_problem_model(problem, db=db, run_judge=run_judge)
        if not val_result.is_valid:
            err_msg = "; ".join(val_result.errors)
            return False, f"Validation failed: {err_msg}", None

        if dry_run:
            return True, "Dry-run validation successful", None

        # 5. Atomic persistence
        try:
            db.add(problem)
            db.commit()
            db.refresh(problem)
            return True, f"Problem successfully imported with ID {problem.id}", problem
        except Exception as e:
            db.rollback()
            logger.exception("Failed to persist problem to database")
            return False, f"Database error during import: {str(e)}", None

    @classmethod
    def get_catalog_health(cls, db: Session, curated_only: bool = False) -> Dict[str, Any]:
        """
        Returns full platform catalog metrics and health diagnostics.
        """
        return ProblemValidator.validate_catalog(db, run_judge=False, curated_only=curated_only)

    @classmethod
    def import_mbpp_dataset(
        cls,
        db: Session,
        jsonl_path: Optional[str] = None,
        dry_run: bool = False,
        max_import: Optional[int] = None,
        run_judge: bool = True
    ) -> Dict[str, Any]:
        """
        Imports and validates coding problems from the Google Research MBPP dataset.
        Idempotent, safe to rerun, atomic, and quality-controlled.
        """
        import ast
        import json
        import os
        import re

        if not jsonl_path:
            # Default to backend/app/data/mbpp.jsonl
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            jsonl_path = os.path.join(base_dir, "data", "mbpp.jsonl")

        if not os.path.exists(jsonl_path):
            raise FileNotFoundError(f"MBPP dataset not found at: {jsonl_path}")

        # Fetch topics lookup
        topics = {t.name.lower(): t.id for t in db.query(Topic).all()}
        if not topics:
            raise RuntimeError("No topics found in database. Seed topics first.")

        # Helper for deterministic topic mapping
        def determine_topic_id(prompt: str, code: str, fn_name: str) -> int:
            p = prompt.lower()
            c = code.lower()
            f = fn_name.lower()

            if any(k in p or k in c for k in ["min_cost", "matrix", "grid", "cost path", "subsequence", "longest increasing", "edit distance", "knapsack", "coin change", "ways to", "fibonacci", "catalan", "bell number", "memo", "lcs", "dynamic programming"]):
                return topics.get("dynamic programming", 9)
            if any(k in p or k in c for k in ["tree", "binary tree", "bst", "inorder", "preorder", "postorder", "leaf", "ancestor"]):
                return topics.get("trees", 6)
            if any(k in p or k in c for k in ["graph", "bfs", "dfs", "cycle", "shortest path", "dijkstra", "adjacent", "node", "edge", "connected component"]):
                return topics.get("graphs", 7)
            if any(k in p or k in c for k in ["permutation", "combination", "backtrack", "partition", "n-queen", "subsets", "powerset", "sudoku"]):
                return topics.get("backtracking", 10)
            if any(k in p or k in c for k in ["greedy", "schedule", "interval", "meeting", "activity", "maximize profit", "gas station"]):
                return topics.get("greedy algorithms", 8)
            if any(k in p or k in c for k in ["stack", "queue", "parenthes", "rpn", "postfix", "prefix notation", "balanced"]):
                return topics.get("stack & queue", 5)
            if any(k in p or k in c for k in ["linked list", "singly linked", "doubly linked", "linkedlist"]):
                return topics.get("linked lists", 4)
            if any(k in p or k in c for k in ["hash", "frequency", "count occurrences", "anagram", "unique elements", "distinct elements", "duplicate", "dictionary", "dict", "char count"]):
                return topics.get("hashing", 3)
            if any(k in p or k in c for k in ["string", "substring", "character", "palindrome", "vowel", "consonant", "word", "regex", "sentence", "uppercase", "lowercase"]):
                return topics.get("strings", 2)
            return topics.get("arrays", 1)

        # Helper for deterministic difficulty mapping
        def determine_difficulty(code: str, topic_id: int) -> Tuple[str, int]:
            lines = [line.strip() for line in code.split("\n") if line.strip() and not line.strip().startswith("#")]
            num_lines = len(lines)
            has_recursion = "return" in code and any(line.count("(") > 1 for line in lines)
            has_nested = "for " in code and (code.count("for ") >= 2 or code.count("while ") >= 2)

            if topic_id in (9, 10, 7) or has_nested or (num_lines > 15 and has_recursion):
                if num_lines > 20:
                    return "Hard", 1900
                return "Medium", 1400
            elif num_lines > 10:
                return "Medium", 1300
            else:
                return "Easy", 1000

        with open(jsonl_path, "r", encoding="utf-8") as f:
            raw_lines = f.readlines()

        total_discovered = len(raw_lines)
        existing_slugs = {p.slug for p in db.query(Problem.slug).all()}
        already_existing_count = 0
        imported_count = 0
        rejection_reasons = Counter()
        topic_counts = Counter()
        diff_counts = Counter()

        batch_to_add: List[Problem] = []

        for line_idx, line in enumerate(raw_lines):
            if max_import and imported_count >= max_import:
                break

            try:
                item = json.loads(line)
            except Exception:
                rejection_reasons["MALFORMED_JSON"] += 1
                continue

            task_id = item.get("task_id", line_idx + 1)
            raw_prompt = item.get("text", "").strip()
            raw_code = item.get("code", "").strip()
            test_list = item.get("test_list", [])

            # Generate clean title and slug
            cleaned_title = raw_prompt.rstrip(".").replace("Write a python function to ", "").replace("Write a function to ", "").strip()
            cleaned_title = cleaned_title[:80].strip()
            cleaned_title = cleaned_title[0].upper() + cleaned_title[1:] if cleaned_title else f"Problem {task_id}"

            slug_name = re.sub(r"[^a-z0-9]+", "-", cleaned_title.lower()).strip("-")
            slug = f"mbpp-{task_id}-{slug_name}" if slug_name else f"mbpp-{task_id}"

            # Idempotency check: Skip if already exists
            if slug in existing_slugs:
                already_existing_count += 1
                continue

            # Skip known incompatible dataset records (un-executable / non-deterministic assert expressions)
            if task_id in INCOMPATIBLE_MBPP_TASK_IDS:
                rejection_reasons["INCOMPATIBLE_DATASET_RECORD"] += 1
                continue

            # 1. AST compilation of reference solution
            try:
                tree = ast.parse(raw_code)
            except SyntaxError as e:
                rejection_reasons["SYNTAX_ERROR"] += 1
                continue

            funcs = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
            if not funcs:
                rejection_reasons["NO_FUNCTION_DEF"] += 1
                continue

            fn = funcs[-1]
            fn_name = fn.name
            arg_names = [a.arg for a in fn.args.args]

            # 2. Parse test cases
            parsed_tcs = []
            for t_idx, test_str in enumerate(test_list):
                try:
                    t_tree = ast.parse(test_str.strip())
                    assert_node = t_tree.body[0]
                    if not isinstance(assert_node, ast.Assert):
                        continue
                    comp = assert_node.test
                    if not isinstance(comp, ast.Compare) or len(comp.ops) != 1 or not isinstance(comp.ops[0], ast.Eq):
                        continue
                    call_node = comp.left

                    if isinstance(call_node, ast.Call) and isinstance(call_node.func, ast.Name) and call_node.func.id == "set":
                        call_node = call_node.args[0]

                    if not isinstance(call_node, ast.Call):
                        continue

                    args_vals = [ast.literal_eval(a) for a in call_node.args]
                    exp_val = ast.literal_eval(comp.comparators[0])

                    if len(args_vals) == len(arg_names):
                        kwargs = dict(zip(arg_names, args_vals))
                    else:
                        continue

                    parsed_tcs.append({
                        "id": t_idx + 1,
                        "input_data": json.dumps(kwargs),
                        "expected_output": json.dumps(exp_val),
                        "is_hidden": (t_idx > 0)
                    })
                except Exception:
                    continue

            if len(parsed_tcs) < 2:
                rejection_reasons["INSUFFICIENT_TEST_CASES"] += 1
                continue

            # Topic & Difficulty
            topic_id = determine_topic_id(raw_prompt, raw_code, fn_name)
            difficulty, rating = determine_difficulty(raw_code, topic_id)

            # Markdown Statement
            first_tc = parsed_tcs[0]
            desc_md = f"### Problem Statement\n\n{raw_prompt}\n\n"
            desc_md += f"#### Example:\n- **Input**: `{first_tc['input_data']}`\n- **Output**: `{first_tc['expected_output']}`\n"

            constraints_md = "- $1 \\le \\text{input size} \\le 10^5$\n- Execution Time Limit: 3.0 seconds\n- Memory Limit: 256 MB"

            starter_code = f"def {fn_name}({', '.join(arg_names)}):\n    # Write your solution here\n    pass\n"

            # Create transient problem
            problem = Problem(
                title=cleaned_title,
                slug=slug,
                topic_id=topic_id,
                difficulty=difficulty,
                description_markdown=desc_md,
                constraints_markdown=constraints_md,
                starter_code_python=starter_code,
                reference_solution_python=raw_code,
                order_index=40 + imported_count + 1,
                is_diagnostic=False,
            )

            for tc_dict in parsed_tcs:
                problem.test_cases.append(TestCase(
                    input_data=tc_dict["input_data"],
                    expected_output=tc_dict["expected_output"],
                    is_hidden=tc_dict["is_hidden"],
                    order_index=tc_dict["id"]
                ))

            # Validate against full sandbox judge
            val_res = ProblemValidator.validate_problem_model(problem, db=db, run_judge=run_judge, judge_timeout=4.0)
            if not val_res.is_valid:
                err_code = val_res.errors[0].split(":")[0].strip() if val_res.errors else "VALIDATION_FAILED"
                rejection_reasons[err_code] += 1
                continue

            # Candidate passed all gates!
            if not dry_run:
                batch_to_add.append(problem)
                existing_slugs.add(slug)

            imported_count += 1
            topic_counts[topic_id] += 1
            diff_counts[difficulty] += 1

            # Commit periodically in batches
            if not dry_run and len(batch_to_add) >= 50:
                try:
                    db.add_all(batch_to_add)
                    db.commit()
                    batch_to_add = []
                except Exception as ex:
                    db.rollback()
                    logger.exception(f"Batch commit failed: {ex}")
                    batch_to_add = []

        # Commit any remaining problems in the batch
        if not dry_run and batch_to_add:
            try:
                db.add_all(batch_to_add)
                db.commit()
            except Exception as ex:
                db.rollback()
                logger.exception(f"Final batch commit failed: {ex}")

        total_after = db.query(Problem).count()

        return {
            "total_discovered": total_discovered,
            "already_existing_count": already_existing_count,
            "newly_imported_count": imported_count,
            "rejected_count": sum(rejection_reasons.values()),
            "rejection_reasons_summary": dict(rejection_reasons.most_common()),
            "topic_distribution": dict(topic_counts),
            "difficulty_distribution": dict(diff_counts),
            "total_database_problems_after": total_after,
            "dry_run": dry_run
        }

