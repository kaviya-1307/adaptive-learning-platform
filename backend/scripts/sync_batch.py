import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json

from app.core.database import SessionLocal
from app.models.problem import Problem
from app.engine.code_runner import extract_target_function_name
from test_transpile_js import transpile_py_to_js
from scripts.py_to_java_transpiler import transpile_py_to_java, infer_java_type
from scripts.py_to_cpp_transpiler import transpile_py_to_cpp, infer_cpp_type
from scripts.mbpp_special_solutions import SPECIAL_MBPP_SOLUTIONS

JSON_PATH = os.path.join(os.path.dirname(__file__), "..", "app", "data", "mbpp_multilang_verified.json")

def sync_batch(start_id: int, end_id: int):
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    db = SessionLocal()
    probs = db.query(Problem).filter(Problem.id.between(start_id, end_id)).order_by(Problem.id).all()
    
    synced_count = 0
    for p in probs:
        pid = p.id
        slug = p.slug
        fn_name = extract_target_function_name(p.starter_code_python)
        tc_first = p.test_cases[0]
        inp = json.loads(tc_first.input_data)
        out = json.loads(tc_first.expected_output)

        ret_java = infer_java_type(out)
        param_java = {k: infer_java_type(v) for k, v in inp.items()} if isinstance(inp, dict) else {"arg0": infer_java_type(inp)}

        ret_cpp = infer_cpp_type(out)
        param_cpp = {k: infer_cpp_type(v) for k, v in inp.items()} if isinstance(inp, dict) else {"arg0": infer_cpp_type(inp)}

        spec = SPECIAL_MBPP_SOLUTIONS.get(pid, {})

        # JS
        js_sol = spec.get("reference_solution_javascript")
        js_starter = spec.get("starter_code_javascript", f"function {fn_name}() {{\n    // Write your solution here\n}}")
        if not js_sol:
            js_sol = transpile_py_to_js(p.reference_solution_python)

        # Java
        java_sol = spec.get("reference_solution_java")
        java_starter = spec.get("starter_code_java", f"class Solution {{\n    public {ret_java} {fn_name}() {{\n        // Write your solution here\n    }}\n}}")
        if not java_sol:
            java_sol = transpile_py_to_java(p.reference_solution_python, ret_java, param_java)

        # C++
        cpp_sol = spec.get("reference_solution_cpp")
        cpp_starter = spec.get("starter_code_cpp", f"class Solution {{\npublic:\n    {ret_cpp} {fn_name}();\n}};")
        if not cpp_sol:
            cpp_sol = transpile_py_to_cpp(p.reference_solution_python, ret_cpp, param_cpp)

        # Update DB
        p.starter_code_javascript = js_starter
        p.reference_solution_javascript = js_sol
        p.starter_code_java = java_starter
        p.reference_solution_java = java_sol
        p.starter_code_cpp = cpp_starter
        p.reference_solution_cpp = cpp_sol

        # Update JSON
        data[slug] = {
            "id": pid,
            "slug": slug,
            "title": p.title,
            "fn_name": fn_name,
            "starter_code_python": p.starter_code_python,
            "reference_solution_python": p.reference_solution_python,
            "starter_code_javascript": js_starter,
            "reference_solution_javascript": js_sol,
            "starter_code_java": java_starter,
            "reference_solution_java": java_sol,
            "starter_code_cpp": cpp_starter,
            "reference_solution_cpp": cpp_sol
        }
        synced_count += 1

    db.commit()
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    # Check overall database counts
    total = db.query(Problem).count()
    js_cnt = db.query(Problem).filter(Problem.reference_solution_javascript.isnot(None), Problem.reference_solution_javascript != '').count()
    java_cnt = db.query(Problem).filter(Problem.reference_solution_java.isnot(None), Problem.reference_solution_java != '').count()
    cpp_cnt = db.query(Problem).filter(Problem.reference_solution_cpp.isnot(None), Problem.reference_solution_cpp != '').count()
    db.close()

    print(f"Synced {synced_count} problems ({start_id}..{end_id}) to DB and JSON.")
    print(f"CURRENT DB STATE: Total={total}, JS={js_cnt}, Java={java_cnt}, C++={cpp_cnt}")

if __name__ == "__main__":
    s_id = int(sys.argv[1]) if len(sys.argv) > 1 else 111
    e_id = int(sys.argv[2]) if len(sys.argv) > 2 else 160
    sync_batch(s_id, e_id)
