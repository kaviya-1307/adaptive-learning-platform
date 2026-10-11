import os
import sys
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import SessionLocal
from app.models.problem import Problem
from app.engine.code_runner import extract_target_function_name

db = SessionLocal()
probs = db.query(Problem).filter(Problem.id.between(661, 710)).order_by(Problem.id).all()
js_count = sum(1 for p in probs if p.reference_solution_javascript)
java_count = sum(1 for p in probs if p.reference_solution_java)
cpp_count = sum(1 for p in probs if p.reference_solution_cpp)

print(f"Problems 661-710 in DB: Total={len(probs)}, JS={js_count}, Java={java_count}, C++={cpp_count}")
print("batch13_solutions.py exists:", os.path.exists("scripts/batch13_solutions.py"))

dump = []
for p in probs:
    fn_name = extract_target_function_name(p.starter_code_python)
    tcs = []
    for tc in p.test_cases:
        tcs.append({
            "id": tc.id,
            "input": json.loads(tc.input_data),
            "output": json.loads(tc.expected_output),
            "is_hidden": tc.is_hidden
        })
    dump.append({
        "id": p.id,
        "slug": p.slug,
        "title": p.title,
        "fn_name": fn_name,
        "ref_py": p.reference_solution_python,
        "starter_py": p.starter_code_python,
        "test_cases": tcs
    })

with open("scripts/batch13_dump.json", "w", encoding="utf-8") as f:
    json.dump(dump, f, indent=2)

print(f"Dumped {len(dump)} problems to scripts/batch13_dump.json")
db.close()
