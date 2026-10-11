import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json
from app.core.database import SessionLocal
from app.models.problem import Problem
from app.engine.code_runner import extract_target_function_name

db = SessionLocal()
probs = db.query(Problem).filter(Problem.id.between(461, 510)).order_by(Problem.id).all()
data = []
for p in probs:
    fn_name = extract_target_function_name(p.starter_code_python)
    tcs = []
    for tc in p.test_cases:
        tcs.append({
            'input': json.loads(tc.input_data),
            'output': json.loads(tc.expected_output)
        })
    data.append({
        'id': p.id,
        'title': p.title,
        'fn_name': fn_name,
        'ref_py': p.reference_solution_python,
        'test_cases': tcs
    })

with open('scripts/batch9_dump.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)
print(f'Dumped {len(data)} problems to scripts/batch9_dump.json')
