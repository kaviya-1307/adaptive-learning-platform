import json
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import time
from typing import Dict, Any, Optional

from app.core.database import SessionLocal
from app.models.problem import Problem
from app.engine.code_runner import (
    PythonCodeRunner,
    JavaScriptCodeRunner,
    JavaCodeRunner,
    CppCodeRunner,
    extract_target_function_name
)
from test_transpile_js import transpile_py_to_js
from scripts.py_to_java_transpiler import transpile_py_to_java, infer_java_type
from scripts.py_to_cpp_transpiler import transpile_py_to_cpp, infer_cpp_type
from scripts.mbpp_special_solutions import SPECIAL_MBPP_SOLUTIONS

OUTPUT_JSON_PATH = os.path.join(os.path.dirname(__file__), "..", "app", "data", "mbpp_multilang_verified.json")

def load_verified() -> Dict[str, Any]:
    if os.path.exists(OUTPUT_JSON_PATH):
        try:
            with open(OUTPUT_JSON_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_verified(data: Dict[str, Any]):
    os.makedirs(os.path.dirname(OUTPUT_JSON_PATH), exist_ok=True)
    with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def generate_and_verify_batch(start_id: int, end_id: int):
    db = SessionLocal()
    probs = db.query(Problem).filter(Problem.id.between(start_id, end_id)).all()
    verified_data = load_verified()

    stats = {"py": 0, "js": 0, "java": 0, "cpp": 0}
    failures = []

    print(f"=== Starting Batch Verification for Problems {start_id}..{end_id} ({len(probs)} problems) ===")

    for idx, p in enumerate(probs):
        pid = p.id
        slug = p.slug
        fn_name = extract_target_function_name(p.starter_code_python)
        tc_first = p.test_cases[0]
        inp = json.loads(tc_first.input_data)
        out = json.loads(tc_first.expected_output)

        tcs = [
            {
                "id": tc.id,
                "input_data": tc.input_data,
                "expected_output": tc.expected_output,
                "is_hidden": tc.is_hidden
            }
            for tc in p.test_cases
        ]

        ret_java = infer_java_type(out)
        param_java = {k: infer_java_type(v) for k, v in inp.items()} if isinstance(inp, dict) else {"arg0": infer_java_type(inp)}

        ret_cpp = infer_cpp_type(out)
        param_cpp = {k: infer_cpp_type(v) for k, v in inp.items()} if isinstance(inp, dict) else {"arg0": infer_cpp_type(inp)}

        spec = SPECIAL_MBPP_SOLUTIONS.get(pid, {})

        prob_entry = verified_data.get(slug, {
            "id": pid,
            "slug": slug,
            "title": p.title,
            "fn_name": fn_name,
            "starter_code_python": p.starter_code_python,
            "reference_solution_python": p.reference_solution_python
        })

        # --- 1. PYTHON ---
        stats["py"] += 1

        # --- 2. JAVASCRIPT ---
        js_sol = spec.get("reference_solution_javascript")
        js_starter = spec.get("starter_code_javascript", f"function {fn_name}() {{}}")
        if not js_sol:
            try:
                js_sol = transpile_py_to_js(p.reference_solution_python)
            except Exception as e:
                js_sol = None
                failures.append((pid, "javascript", "TranspileError", str(e)[:80]))

        if js_sol:
            res_js = JavaScriptCodeRunner.execute(js_sol, tcs, starter_code=js_starter, is_submission=True)
            if res_js.get("status") == "Accepted":
                stats["js"] += 1
                prob_entry["starter_code_javascript"] = js_starter
                prob_entry["reference_solution_javascript"] = js_sol
                p.starter_code_javascript = js_starter
                p.reference_solution_javascript = js_sol
            else:
                err = res_js.get("compile_error") or (res_js.get("results")[0].get("error_message") if res_js.get("results") else "Wrong Answer")
                failures.append((pid, "javascript", res_js.get("status"), (err or "")[:80]))

        # --- 3. JAVA ---
        java_sol = spec.get("reference_solution_java")
        java_starter = spec.get("starter_code_java", f"class Solution {{\n    public {ret_java} {fn_name}() {{}}\n}}")
        if not java_sol:
            try:
                java_sol = transpile_py_to_java(p.reference_solution_python, ret_java, param_java)
            except Exception as e:
                java_sol = None
                failures.append((pid, "java", "TranspileError", str(e)[:80]))

        if java_sol:
            res_java = JavaCodeRunner.execute(java_sol, tcs, starter_code=java_starter, timeout_seconds=10.0, is_submission=True)
            if res_java.get("status") == "Accepted":
                stats["java"] += 1
                prob_entry["starter_code_java"] = java_starter
                prob_entry["reference_solution_java"] = java_sol
                p.starter_code_java = java_starter
                p.reference_solution_java = java_sol
            else:
                err = res_java.get("compile_error") or (res_java.get("results")[0].get("error_message") if res_java.get("results") else "Wrong Answer")
                failures.append((pid, "java", res_java.get("status"), (err or "")[:80]))

        # --- 4. C++ ---
        cpp_sol = spec.get("reference_solution_cpp")
        cpp_starter = spec.get("starter_code_cpp", f"class Solution {{\npublic:\n    {ret_cpp} {fn_name}();\n}};")
        if not cpp_sol:
            try:
                cpp_sol = transpile_py_to_cpp(p.reference_solution_python, ret_cpp, param_cpp)
            except Exception as e:
                cpp_sol = None
                failures.append((pid, "cpp", "TranspileError", str(e)[:80]))

        if cpp_sol:
            res_cpp = CppCodeRunner.execute(cpp_sol, tcs, starter_code=cpp_starter, is_submission=True)
            if res_cpp.get("status") == "Accepted":
                stats["cpp"] += 1
                prob_entry["starter_code_cpp"] = cpp_starter
                prob_entry["reference_solution_cpp"] = cpp_sol
                p.starter_code_cpp = cpp_starter
                p.reference_solution_cpp = cpp_sol
            else:
                err = res_cpp.get("compile_error") or (res_cpp.get("results")[0].get("error_message") if res_cpp.get("results") else "Wrong Answer")
                failures.append((pid, "cpp", res_cpp.get("status"), (err or "")[:80]))

        verified_data[slug] = prob_entry
        db.commit()
        save_verified(verified_data)

        print(f"[{idx+1}/{len(probs)}] ID {pid} ({fn_name}): "
              f"JS={'OK' if 'reference_solution_javascript' in prob_entry else 'FAIL'} "
              f"Java={'OK' if 'reference_solution_java' in prob_entry else 'FAIL'} "
              f"C++={'OK' if 'reference_solution_cpp' in prob_entry else 'FAIL'}")

    db.close()

    print(f"\n=== Batch Summary for {start_id}..{end_id} ===")
    print(f"Python: {stats['py']}/{len(probs)}")
    print(f"JavaScript: {stats['js']}/{len(probs)}")
    print(f"Java: {stats['java']}/{len(probs)}")
    print(f"C++: {stats['cpp']}/{len(probs)}")
    print(f"Total verified entries stored: {len(verified_data)}")

    if failures:
        print(f"\nFailures ({len(failures)}):")
        for f in failures[:15]:
            print(f"  ID {f[0]} [{f[1]}]: {f[2]} - {f[3]}")

    return stats, failures

if __name__ == "__main__":
    s_id = int(sys.argv[1]) if len(sys.argv) > 1 else 41
    e_id = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    generate_and_verify_batch(s_id, e_id)
