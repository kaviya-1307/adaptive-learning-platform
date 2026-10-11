import sys
sys.path.insert(0, '.')
import json
import re
from app.engine.code_runner import _generate_java_driver, _generate_cpp_driver

with open('scripts/batch14_dump.json', 'r', encoding='utf-8') as f:
    probs = json.load(f)

for p in probs:
    pid = p['id']
    fn = p['fn_name']
    tcs = [{'id': i+1, 'input_data': json.dumps(tc['input']), 'expected_output': json.dumps(tc['output']), 'is_hidden': False} for i, tc in enumerate(p['test_cases'])]
    
    j_drv = _generate_java_driver(fn, tcs)
    c_drv = _generate_cpp_driver(fn, tcs)
    
    j_calls = [l.strip() for l in j_drv.split('\n') if 'sol.' in l]
    patterns = set()
    for jc in j_calls:
        sig = re.sub(r'"[^"]*"', '"str"', jc)
        sig = re.sub(r'\b\d+\b', 'NUM', sig)
        sig = re.sub(r'NUM(, NUM)+', 'NUMS', sig)
        patterns.add(sig)
    if len(patterns) > 1:
        print(f"ID {pid} ({fn}) has multiple Java signatures:")
        for pat in patterns:
            print("   ", pat)
