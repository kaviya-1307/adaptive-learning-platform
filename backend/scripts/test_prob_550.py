import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json

from app.core.database import SessionLocal
from app.models.problem import Problem
from app.engine.code_runner import CppCodeRunner

# Let's inspect problem 550
db = SessionLocal()
p = db.query(Problem).filter(Problem.id == 550).first()
tcs = [{'id': tc.id, 'input_data': tc.input_data, 'expected_output': tc.expected_output, 'is_hidden': tc.is_hidden} for tc in p.test_cases]
db.close()

for tc in tcs:
    print(tc['input_data'], "->", tc['expected_output'])
