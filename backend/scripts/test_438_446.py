import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json
from app.core.database import SessionLocal
from app.models.problem import Problem
from app.engine.code_runner import JavaCodeRunner, CppCodeRunner

db = SessionLocal()

for pid in [438, 446]:
    p = db.query(Problem).filter(Problem.id == pid).first()
    tcs = [
        {"id": tc.id, "input_data": tc.input_data, "expected_output": tc.expected_output, "is_hidden": tc.is_hidden}
        for tc in p.test_cases
    ]
    print(f"=== PID {pid} ===")
    for idx, tc in enumerate(tcs):
        print(f" TC {idx+1}: {tc['input_data']} -> {tc['expected_output']}")
