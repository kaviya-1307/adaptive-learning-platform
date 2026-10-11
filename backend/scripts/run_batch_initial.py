import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json
import time

from app.core.database import SessionLocal
from app.models.problem import Problem
from app.engine.code_runner import (
    JavaScriptCodeRunner,
    JavaCodeRunner,
    CppCodeRunner,
    extract_target_function_name
)
from test_transpile_js import transpile_py_to_js
from scripts.py_to_java_transpiler import transpile_py_to_java, infer_java_type
from scripts.py_to_cpp_transpiler import transpile_py_to_cpp, infer_cpp_type
from scripts.mbpp_special_solutions import SPECIAL_MBPP_SOLUTIONS

def run_initial_batch(start_id, end_id):
    db = SessionLocal()
    probs = db.query(Problem).filter(Problem.id.between(start_id, end_id)).order_by(Problem.id).all()
    
    stats = {"js": 0, "java": 0, "cpp": 0}
    total = len(probs)
    failures = []
    
    print(f"=== Initial Transpiler & Runner Pass for Problems {start_id}..{end_id} ({total} problems) ===")
    
    for idx, p in enumerate(probs):
        pid = p.id
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

        # JS
        js_sol = spec.get("reference_solution_javascript")
        js_starter = spec.get("starter_code_javascript", f"function {fn_name}() {{}}")
        if not js_sol:
            try:
                js_sol = transpile_py_to_js(p.reference_solution_python)
            except Exception as e:
                js_sol = None
                failures.append((pid, "JavaScript", "TranspileError", str(e)))

        js_ok = False
        if js_sol:
            res_js = JavaScriptCodeRunner.execute(js_sol, tcs, starter_code=js_starter, is_submission=True)
            js_ok = res_js.get("status") == "Accepted"
            if js_ok:
                stats["js"] += 1
            else:
                err = res_js.get("compile_error") or (res_js.get("results")[0].get("error_message") if res_js.get("results") else "WA")
                failures.append((pid, "JavaScript", res_js.get("status"), err))

        # Java
        java_sol = spec.get("reference_solution_java")
        java_starter = spec.get("starter_code_java", f"class Solution {{\n    public {ret_java} {fn_name}() {{}}\n}}")
        if not java_sol:
            try:
                java_sol = transpile_py_to_java(p.reference_solution_python, ret_java, param_java)
            except Exception as e:
                java_sol = None
                failures.append((pid, "Java", "TranspileError", str(e)))

        java_ok = False
        if java_sol:
            res_java = JavaCodeRunner.execute(java_sol, tcs, starter_code=java_starter, timeout_seconds=10.0, is_submission=True)
            java_ok = res_java.get("status") == "Accepted"
            if java_ok:
                stats["java"] += 1
            else:
                err = res_java.get("compile_error") or (res_java.get("results")[0].get("error_message") if res_java.get("results") else "WA")
                failures.append((pid, "Java", res_java.get("status"), err))

        # C++
        cpp_sol = spec.get("reference_solution_cpp")
        cpp_starter = spec.get("starter_code_cpp", f"class Solution {{\npublic:\n    {ret_cpp} {fn_name}();\n}};")
        if not cpp_sol:
            try:
                cpp_sol = transpile_py_to_cpp(p.reference_solution_python, ret_cpp, param_cpp)
            except Exception as e:
                cpp_sol = None
                failures.append((pid, "C++", "TranspileError", str(e)))

        cpp_ok = False
        if cpp_sol:
            res_cpp = CppCodeRunner.execute(cpp_sol, tcs, starter_code=cpp_starter, is_submission=True)
            cpp_ok = res_cpp.get("status") == "Accepted"
            if cpp_ok:
                stats["cpp"] += 1
            else:
                err = res_cpp.get("compile_error") or (res_cpp.get("results")[0].get("error_message") if res_cpp.get("results") else "WA")
                failures.append((pid, "C++", res_cpp.get("status"), err))

        print(f"[{idx+1}/{total}] ID {pid} ({fn_name}): JS={'OK' if js_ok else 'FAIL'} Java={'OK' if java_ok else 'FAIL'} C++={'OK' if cpp_ok else 'FAIL'}", flush=True)

    db.close()

    print("\n" + "="*50)
    print(f"PASS STATS for {start_id}..{end_id}:")
    print(f"JavaScript: {stats['js']}/{total}")
    print(f"Java:       {stats['java']}/{total}")
    print(f"C++:        {stats['cpp']}/{total}")
    print("="*50)

    if failures:
        print(f"\nFailures ({len(failures)}):")
        for pid, lang, status, err in failures:
            print(f"  PID {pid} [{lang}]: {status} -> {str(err)[:120]}")
            
    return stats, failures

if __name__ == "__main__":
    s_id = int(sys.argv[1]) if len(sys.argv) > 1 else 161
    e_id = int(sys.argv[2]) if len(sys.argv) > 2 else 210
    run_initial_batch(s_id, e_id)
