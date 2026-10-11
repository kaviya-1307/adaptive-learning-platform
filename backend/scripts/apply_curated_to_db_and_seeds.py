"""
Applies CURATED_30 multi-language solutions to the database and multi_lang_dump.json.
"""
import json
from app.core.database import SessionLocal
from app.models.problem import Problem
from scripts.curated_solutions import CURATED_30

def apply_curated():
    db = SessionLocal()
    updated = 0

    # 1. Update Database
    for pid, sol in CURATED_30.items():
        prob = db.query(Problem).filter(Problem.id == pid).first()
        if prob:
            prob.starter_code_java = sol["starter_code_java"]
            prob.reference_solution_java = sol["reference_solution_java"]
            prob.starter_code_cpp = sol["starter_code_cpp"]
            prob.reference_solution_cpp = sol["reference_solution_cpp"]
            prob.starter_code_javascript = sol["starter_code_javascript"]
            prob.reference_solution_javascript = sol["reference_solution_javascript"]
            updated += 1

    db.commit()
    print(f"Updated {updated} curated problems in database.")

    # 2. Update multi_lang_dump.json
    try:
        with open("multi_lang_dump.json", "r", encoding="utf-8") as f:
            dump = json.load(f)
    except Exception:
        dump = {}

    for pid, sol in CURATED_30.items():
        prob = db.query(Problem).filter(Problem.id == pid).first()
        dump[str(pid)] = {
            "slug": prob.slug if prob else f"problem-{pid}",
            "title": prob.title if prob else f"Problem {pid}",
            "starter_code_java": sol["starter_code_java"],
            "reference_solution_java": sol["reference_solution_java"],
            "starter_code_cpp": sol["starter_code_cpp"],
            "reference_solution_cpp": sol["reference_solution_cpp"],
            "starter_code_javascript": sol["starter_code_javascript"],
            "reference_solution_javascript": sol["reference_solution_javascript"]
        }

    with open("multi_lang_dump.json", "w", encoding="utf-8") as f:
        json.dump(dump, f, indent=2)

    print(f"multi_lang_dump.json now has {len(dump)} problems.")
    db.close()

if __name__ == "__main__":
    apply_curated()
