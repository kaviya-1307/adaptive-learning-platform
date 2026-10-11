import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json

from app.core.database import SessionLocal
from app.models.problem import Problem
from scripts.batch10_solutions import BATCH10_SOLUTIONS
from app.engine.code_runner import JavaCodeRunner, CppCodeRunner

db = SessionLocal()
p = db.query(Problem).filter(Problem.id == 531).first()
tcs = [{'id': tc.id, 'input_data': tc.input_data, 'expected_output': tc.expected_output, 'is_hidden': tc.is_hidden} for tc in p.test_cases]
db.close()

spec = BATCH10_SOLUTIONS[531]
res_java = JavaCodeRunner.execute(spec['reference_solution_java'], tcs, starter_code=spec['starter_code_java'], is_submission=True)
res_cpp = CppCodeRunner.execute(spec['reference_solution_cpp'], tcs, starter_code=spec['starter_code_cpp'], is_submission=True)

print("Java status:", res_java.get("status"))
print("Java compile error:", res_java.get("compile_error"))
if res_java.get("results"):
    print("Java result 0:", res_java["results"][0])

print("\nC++ status:", res_cpp.get("status"))
print("C++ compile error:", res_cpp.get("compile_error"))
if res_cpp.get("results"):
    print("C++ result 0:", res_cpp["results"][0])
