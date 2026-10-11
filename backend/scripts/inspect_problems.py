import json
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.core.database import SessionLocal
from app.models.problem import Problem
from app.engine.code_runner import extract_target_function_name

def dump_problems(start_id, end_id, out_file=None):
    db = SessionLocal()
    probs = db.query(Problem).filter(Problem.id.between(start_id, end_id)).order_by(Problem.id).all()
    out = []
    for p in probs:
        fn_name = extract_target_function_name(p.starter_code_python)
        tcs = [{'input': json.loads(tc.input_data), 'output': json.loads(tc.expected_output)} for tc in p.test_cases]
        out.append({
            'id': p.id,
            'slug': p.slug,
            'title': p.title,
            'fn_name': fn_name,
            'starter_py': p.starter_code_python,
            'ref_py': p.reference_solution_python,
            'test_cases': tcs
        })
    db.close()
    if out_file:
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(out, f, indent=2)
    return out

if __name__ == '__main__':
    s = int(sys.argv[1]) if len(sys.argv) > 1 else 311
    e = int(sys.argv[2]) if len(sys.argv) > 2 else 360
    f = sys.argv[3] if len(sys.argv) > 3 else None
    res = dump_problems(s, e, f)
    print(f"Dumped {len(res)} problems.")
