"""
Verify all 30 curated solutions using CodeRunner for Java, C++, and JavaScript.
"""
import sys
import logging
from app.core.database import SessionLocal
from app.models.problem import Problem
from app.engine.code_runner import CodeRunner
from scripts.curated_solutions import CURATED_30

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_curated():
    db = SessionLocal()
    total = len(CURATED_30)
    print(f"Testing {total} curated problems across Java, C++, JavaScript...", flush=True)

    results = {"java": {"passed": 0, "failed": []}, "cpp": {"passed": 0, "failed": []}, "javascript": {"passed": 0, "failed": []}}

    for pid, sol_data in CURATED_30.items():
        prob = db.query(Problem).filter(Problem.id == pid).first()
        if not prob:
            print(f"Problem {pid} not found in DB!", flush=True)
            continue

        print(f"--> Testing Problem {pid} ({prob.slug})...", flush=True)
        tcs = [{"id": tc.id, "input_data": tc.input_data, "expected_output": tc.expected_output, "is_hidden": tc.is_hidden} for tc in prob.test_cases]

        # 1. Test JavaScript
        js_code = sol_data["reference_solution_javascript"]
        js_starter = sol_data["starter_code_javascript"]
        js_res = CodeRunner.execute(js_code, tcs, "javascript", js_starter, is_submission=True)
        if js_res.get("status") == "Accepted":
            results["javascript"]["passed"] += 1
            print(f"  [P{pid:2d}] JS:   PASSED ({js_res['passed_test_cases']}/{js_res['total_test_cases']})", flush=True)
        else:
            err = js_res.get("compile_error") or (js_res.get("results")[0].get("error_message") if js_res.get("results") else "WA")
            results["javascript"]["failed"].append((pid, js_res.get("status"), err))
            print(f"  [P{pid:2d}] JS:   FAILED {js_res.get('status')} - {err}", flush=True)

        # 2. Test Java
        java_code = sol_data["reference_solution_java"]
        java_starter = sol_data["starter_code_java"]
        java_res = CodeRunner.execute(java_code, tcs, "java", java_starter, is_submission=True)
        if java_res.get("status") == "Accepted":
            results["java"]["passed"] += 1
            print(f"  [P{pid:2d}] JAVA: PASSED ({java_res['passed_test_cases']}/{java_res['total_test_cases']})", flush=True)
        else:
            err = java_res.get("compile_error") or (java_res.get("results")[0].get("error_message") if java_res.get("results") else "WA")
            results["java"]["failed"].append((pid, java_res.get("status"), err))
            print(f"  [P{pid:2d}] JAVA: FAILED {java_res.get('status')} - {err}", flush=True)

        # 3. Test C++
        cpp_code = sol_data["reference_solution_cpp"]
        cpp_starter = sol_data["starter_code_cpp"]
        cpp_res = CodeRunner.execute(cpp_code, tcs, "cpp", cpp_starter, is_submission=True)
        if cpp_res.get("status") == "Accepted":
            results["cpp"]["passed"] += 1
            print(f"  [P{pid:2d}] CPP:  PASSED ({cpp_res['passed_test_cases']}/{cpp_res['total_test_cases']})", flush=True)
        else:
            err = cpp_res.get("compile_error") or (cpp_res.get("results")[0].get("error_message") if cpp_res.get("results") else "WA")
            results["cpp"]["failed"].append((pid, cpp_res.get("status"), err))
            print(f"  [P{pid:2d}] CPP:  FAILED {cpp_res.get('status')} - {err}", flush=True)

    db.close()

    print("\n" + "="*50, flush=True)
    print("CURATED 30 VERIFICATION SUMMARY:", flush=True)
    print(f"JavaScript: {results['javascript']['passed']}/{total}", flush=True)
    print(f"Java:       {results['java']['passed']}/{total}", flush=True)
    print(f"C++:        {results['cpp']['passed']}/{total}", flush=True)
    print("="*50, flush=True)

    return results

if __name__ == "__main__":
    verify_curated()
