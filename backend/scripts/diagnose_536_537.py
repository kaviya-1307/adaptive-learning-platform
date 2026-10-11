import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json

from app.core.database import SessionLocal
from app.models.problem import Problem
from scripts.batch10_solutions import BATCH10_SOLUTIONS
from app.engine.code_runner import JavaCodeRunner, CppCodeRunner

db = SessionLocal()
for pid in [536, 537]:
    p = db.query(Problem).filter(Problem.id == pid).first()
    tcs = [{'id': tc.id, 'input_data': tc.input_data, 'expected_output': tc.expected_output, 'is_hidden': tc.is_hidden} for tc in p.test_cases]
    spec = BATCH10_SOLUTIONS[pid]

    res_java = JavaCodeRunner.execute(spec['reference_solution_java'], tcs, starter_code=spec['starter_code_java'], is_submission=True)
    res_cpp = CppCodeRunner.execute(spec['reference_solution_cpp'], tcs, starter_code=spec['starter_code_cpp'], is_submission=True)

    print(f"\nProblem {pid}:")
    print("Java status:", res_java.get("status"), res_java.get("compile_error") or (res_java.get("results")[0] if res_java.get("results") else ""))
    print("C++ status:", res_cpp.get("status"), res_cpp.get("compile_error") or (res_cpp.get("results")[0] if res_cpp.get("results") else ""))

db.close()
