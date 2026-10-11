import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json
import time

from app.core.database import SessionLocal
from app.models.problem import Problem
from app.engine.code_runner import JavaScriptCodeRunner, JavaCodeRunner, CppCodeRunner

def validate_batch1():
    db = SessionLocal()
    probs = db.query(Problem).filter(Problem.id.between(61, 110)).order_by(Problem.id).all()
    
    js_pass = 0
    java_pass = 0
    cpp_pass = 0
    total = len(probs)
    
    failures = []
    
    print(f"=== Validating Batch 1 (Problems 61..110, {total} problems) ===")
    start_time = time.time()
    
    for idx, p in enumerate(probs):
        pid = p.id
        tcs = [
            {
                "id": tc.id,
                "input_data": tc.input_data,
                "expected_output": tc.expected_output,
                "is_hidden": tc.is_hidden
            }
            for tc in p.test_cases
        ]
        
        # JS validation
        res_js = JavaScriptCodeRunner.execute(
            p.reference_solution_javascript,
            tcs,
            starter_code=p.starter_code_javascript,
            is_submission=True
        )
        js_ok = res_js.get("status") == "Accepted"
        if js_ok:
            js_pass += 1
        else:
            err = res_js.get("compile_error") or (res_js.get("results")[0].get("error_message") if res_js.get("results") else "Unknown")
            failures.append((pid, "JavaScript", res_js.get("status"), err))
            
        # Java validation
        res_java = JavaCodeRunner.execute(
            p.reference_solution_java,
            tcs,
            starter_code=p.starter_code_java,
            timeout_seconds=10.0,
            is_submission=True
        )
        java_ok = res_java.get("status") == "Accepted"
        if java_ok:
            java_pass += 1
        else:
            err = res_java.get("compile_error") or (res_java.get("results")[0].get("error_message") if res_java.get("results") else "Unknown")
            failures.append((pid, "Java", res_java.get("status"), err))
            
        # C++ validation
        res_cpp = CppCodeRunner.execute(
            p.reference_solution_cpp,
            tcs,
            starter_code=p.starter_code_cpp,
            is_submission=True
        )
        cpp_ok = res_cpp.get("status") == "Accepted"
        if cpp_ok:
            cpp_pass += 1
        else:
            err = res_cpp.get("compile_error") or (res_cpp.get("results")[0].get("error_message") if res_cpp.get("results") else "Unknown")
            failures.append((pid, "C++", res_cpp.get("status"), err))
            
        status_str = f"[{idx+1}/{total}] ID {pid} ({p.title[:30]}): JS={'OK' if js_ok else 'FAIL'} Java={'OK' if java_ok else 'FAIL'} C++={'OK' if cpp_ok else 'FAIL'}"
        print(status_str)
        
    db.close()
    elapsed = time.time() - start_time
    
    print("\n" + "="*50)
    print(f"BATCH 1 VALIDATION RESULTS (Elapsed: {elapsed:.1f}s):")
    print(f"JavaScript: {js_pass}/{total} ({'PASSED' if js_pass == total else 'FAILED'})")
    print(f"Java:       {java_pass}/{total} ({'PASSED' if java_pass == total else 'FAILED'})")
    print(f"C++:        {cpp_pass}/{total} ({'PASSED' if cpp_pass == total else 'FAILED'})")
    print("="*50)
    
    if failures:
        print(f"\nTotal Failures ({len(failures)}):")
        for pid, lang, status, err in failures:
            print(f"  Problem {pid} [{lang}]: {status} -> {str(err)[:120]}")
    else:
        print("\nAll 50 problems in Batch 1 (61..110) are 100% ACCEPTED across JavaScript, Java, and C++!")

if __name__ == "__main__":
    validate_batch1()
