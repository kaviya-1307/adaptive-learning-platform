import json
from app.core.database import SessionLocal
from app.models.problem import Problem
from app.engine.code_runner import JavaCodeRunner, extract_target_function_name
from scripts.py_to_java_transpiler import transpile_py_to_java, infer_java_type

def test_java(start_id=41, end_id=50):
    db = SessionLocal()
    probs = db.query(Problem).filter(Problem.id.between(start_id, end_id)).all()
    passed = []
    failed = []

    for idx, p in enumerate(probs):
        fn_name = extract_target_function_name(p.starter_code_python)
        tc = p.test_cases[0]
        inp = json.loads(tc.input_data)
        out = json.loads(tc.expected_output)

        ret_type = infer_java_type(out)
        if isinstance(inp, dict):
            param_types = {k: infer_java_type(v) for k, v in inp.items()}
        else:
            param_types = {"arg0": infer_java_type(inp)}

        try:
            java_code = transpile_py_to_java(p.reference_solution_python, ret_type, param_types)
            starter = f"class Solution {{\n    public {ret_type} {fn_name}() {{}}\n}}"
            tcs = [{'id': tc.id, 'input_data': tc.input_data, 'expected_output': tc.expected_output, 'is_hidden': tc.is_hidden} for tc in p.test_cases]
            res = JavaCodeRunner.execute(java_code, tcs, starter_code=starter, is_submission=True)
            if res.get('status') == 'Accepted':
                passed.append((p.id, fn_name))
            else:
                err = res.get('compile_error') or (res.get('results')[0].get('error_message') if res.get('results') else 'Unknown')
                failed.append((p.id, fn_name, res.get('status'), (err or '')[:100]))
        except Exception as e:
            failed.append((p.id, fn_name, 'Exception', str(e)[:100]))

        print(f"[{idx+1}/{len(probs)}] ID {p.id}: {passed[-1][1] if passed and passed[-1][0] == p.id else 'FAILED'}")

    print(f"\nJava Result: Total {len(probs)} | Passed {len(passed)} | Failed {len(failed)} ({len(passed)/len(probs)*100:.1f}%)")
    for f in failed:
        print(f"  Fail {f[0]} ({f[1]}): {f[2]} - {f[3]}")

    db.close()

if __name__ == "__main__":
    test_java()
