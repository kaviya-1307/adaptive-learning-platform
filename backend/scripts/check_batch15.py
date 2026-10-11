import sys
sys.path.insert(0, '.')
import json
import re
from app.engine.code_runner import _generate_java_driver, _generate_cpp_driver

with open('scripts/batch15_dump.json', 'r', encoding='utf-8') as f:
    probs = json.load(f)

for p in probs:
    pid = p['id']
    fn = p['fn_name']
    tcs = [{'id': i+1, 'input_data': json.dumps(tc['input']), 'expected_output': json.dumps(tc['output']), 'is_hidden': False} for i, tc in enumerate(p['test_cases'])]
    
    try:
        j_drv = _generate_java_driver(fn, tcs)
        j_calls = [l.strip() for l in j_drv.split('\n') if 'sol.' in l]
        patterns = set()
        for jc in j_calls:
            sig = re.sub(r'"[^"]*"', '"str"', jc)
            sig = re.sub(r'\b\d+\b', 'NUM', sig)
            patterns.add(sig)
        if len(patterns) > 1:
            print(f"ID {pid} ({fn}) has multiple Java signatures:")
            for pat in patterns:
                print("   ", pat)
    except Exception as e:
        print(f"ID {pid} Java driver error: {e}")
        
    try:
        c_drv = _generate_cpp_driver(fn, tcs)
    except Exception as e:
        print(f"ID {pid} C++ driver error: {e}")

print("Driver check completed.")
