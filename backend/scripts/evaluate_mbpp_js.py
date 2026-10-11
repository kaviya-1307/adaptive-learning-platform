import json
import time
from app.core.database import SessionLocal
from app.models.problem import Problem
from app.engine.code_runner import JavaScriptCodeRunner, extract_target_function_name
from test_transpile_js import transpile_py_to_js

def evaluate_js(start_id=41, end_id=889):
    db = SessionLocal()
    probs = db.query(Problem).filter(Problem.id.between(start_id, end_id)).all()
    passed = []
    failed = []
    
    t0 = time.time()
    for idx, p in enumerate(probs):
        fn_name = extract_target_function_name(p.starter_code_python)
        try:
            js = transpile_py_to_js(p.reference_solution_python)
            starter = f"function {fn_name}() {{}}"
            tcs = [{'id': tc.id, 'input_data': tc.input_data, 'expected_output': tc.expected_output, 'is_hidden': tc.is_hidden} for tc in p.test_cases]
            res = JavaScriptCodeRunner.execute(js, tcs, starter_code=starter, is_submission=True)
            if res.get('status') == 'Accepted':
                passed.append((p.id, fn_name))
            else:
                err = res.get('compile_error') or (res.get('results')[0].get('error_message') if res.get('results') else 'Unknown')
                failed.append((p.id, fn_name, res.get('status'), (err or '')[:120]))
        except Exception as e:
            failed.append((p.id, fn_name, 'Exception', str(e)[:120]))
        
        if (idx + 1) % 100 == 0 or (idx + 1) == len(probs):
            print(f"[{idx+1}/{len(probs)}] Passed: {len(passed)}, Failed: {len(failed)} ({len(passed)/(idx+1)*100:.1f}%)")

    elapsed = round(time.time() - t0, 1)
    print(f"\nCompleted in {elapsed}s: Total {len(probs)} | Passed {len(passed)} | Failed {len(failed)} ({len(passed)/len(probs)*100:.1f}%)")
    
    print("\nSample failures:")
    for f in failed[:15]:
        print(f"  ID {f[0]} ({f[1]}): {f[2]} - {f[3]}")

    db.close()
    return passed, failed

if __name__ == "__main__":
    evaluate_js()
