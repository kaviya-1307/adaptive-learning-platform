import json
from app.core.database import SessionLocal
from app.models.problem import Problem
from app.engine.code_runner import JavaCodeRunner
from scripts.mbpp_special_solutions import SPECIAL_MBPP_SOLUTIONS

db = SessionLocal()
for pid in [673, 694, 704]:
    p = db.query(Problem).filter(Problem.id == pid).first()
    tcs = [{'id': tc.id, 'input_data': tc.input_data, 'expected_output': tc.expected_output, 'is_hidden': tc.is_hidden} for tc in p.test_cases]
    spec = SPECIAL_MBPP_SOLUTIONS[pid]
    java_sol = spec['reference_solution_java']
    java_starter = spec['starter_code_java']
    res = JavaCodeRunner.execute(java_sol, tcs, starter_code=java_starter, timeout_seconds=10.0, is_submission=True)
    status = res.get('status')
    err = res.get('compile_error') or (res.get('results')[0].get('error_message') if res.get('results') else None)
    print(f"Problem {pid}: status={status}, err={err}")
db.close()
