import json
from collections import Counter
from app.core.database import SessionLocal
from app.models.problem import Problem
from app.engine.code_runner import JavaScriptCodeRunner, extract_target_function_name
from test_transpile_js import transpile_py_to_js

def diagnose():
    db = SessionLocal()
    probs = db.query(Problem).filter(Problem.id.between(41, 889)).all()
    categories = Counter()
    sample_per_cat = {}

    for p in probs:
        fn_name = extract_target_function_name(p.starter_code_python)
        try:
            js = transpile_py_to_js(p.reference_solution_python)
            starter = f"function {fn_name}() {{}}"
            tcs = [{'id': tc.id, 'input_data': tc.input_data, 'expected_output': tc.expected_output, 'is_hidden': tc.is_hidden} for tc in p.test_cases]
            res = JavaScriptCodeRunner.execute(js, tcs, starter_code=starter, is_submission=True)
            if res.get('status') != 'Accepted':
                status = res.get('status')
                err = res.get('compile_error') or (res.get('results')[0].get('error_message') if res.get('results') else 'Wrong Answer')
                
                # Categorize
                cat = "Other"
                if "is not defined" in err:
                    missing = err.split("is not defined")[0].split()[-1]
                    cat = f"NotDefined: {missing}"
                elif "is not a function" in err:
                    fn = err.split("is not a function")[0].split()[-1]
                    cat = f"NotAFunction: {fn}"
                elif "Cannot access" in err or "before initialization" in err:
                    cat = "TemporalDeadZone / Shadowing"
                elif "SyntaxError" in err:
                    cat = f"SyntaxError: {err.splitlines()[0][:40]}"
                elif status == "Wrong Answer":
                    cat = "Wrong Answer"
                elif status == "Time Limit Exceeded":
                    cat = "TLE"
                elif "TypeError" in err:
                    cat = f"TypeError: {err.splitlines()[0][:40]}"
                
                categories[cat] += 1
                if cat not in sample_per_cat:
                    sample_per_cat[cat] = (p.id, fn_name, err[:100])
        except Exception as e:
            cat = f"ASTException: {type(e).__name__}"
            categories[cat] += 1
            if cat not in sample_per_cat:
                sample_per_cat[cat] = (p.id, fn_name, str(e)[:100])

    print("Failure categories across 849 MBPP problems:")
    for cat, count in categories.most_common(25):
        sample = sample_per_cat[cat]
        print(f"  [{count:3d}] {cat}")
        print(f"        Sample ID {sample[0]} ({sample[1]}): {sample[2]}")

    db.close()

if __name__ == "__main__":
    diagnose()
