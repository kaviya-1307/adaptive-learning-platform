import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json
from app.core.database import SessionLocal
from app.models.problem import Problem
from app.engine.code_runner import PythonCodeRunner, JavaScriptCodeRunner, JavaCodeRunner, CppCodeRunner

def verify_saved():
    with open('app/data/mbpp_multilang_verified.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    db = SessionLocal()
    all_ok = True
    print("Verifying problems 41..60 against live CodeRunner...")
    for pid in range(41, 61):
        prob = db.query(Problem).filter(Problem.id == pid).first()
        entries = [x for x in data.values() if x.get('id') == pid]
        if not entries:
            print(f"Problem {pid} not found in json!")
            all_ok = False
            continue
        v = entries[0]
        tcs = [{'id': tc.id, 'input_data': tc.input_data, 'expected_output': tc.expected_output, 'is_hidden': tc.is_hidden} for tc in prob.test_cases]

        res_js = JavaScriptCodeRunner.execute(v['reference_solution_javascript'], tcs, starter_code=v['starter_code_javascript'], is_submission=True)
        res_java = JavaCodeRunner.execute(v['reference_solution_java'], tcs, starter_code=v['starter_code_java'], is_submission=True)
        res_cpp = CppCodeRunner.execute(v['reference_solution_cpp'], tcs, starter_code=v['starter_code_cpp'], is_submission=True)

        js_ok = res_js.get('status') == 'Accepted'
        ja_ok = res_java.get('status') == 'Accepted'
        cp_ok = res_cpp.get('status') == 'Accepted'

        if js_ok and ja_ok and cp_ok:
            print(f"Problem {pid}: All Accepted (JS, Java, C++)")
        else:
            print(f"Problem {pid}: FAIL -> JS={res_js.get('status')} Java={res_java.get('status')} Cpp={res_cpp.get('status')}")
            all_ok = False

    if all_ok:
        print("\nAll problems 41..60 are 100% ACCEPTED in JS, Java, and C++!")
    db.close()

if __name__ == '__main__':
    verify_saved()
