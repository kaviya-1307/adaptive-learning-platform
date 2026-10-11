import sys
import json
import re
sys.path.insert(0, '.')

from app.engine.code_runner import (
    _generate_java_driver,
    _generate_cpp_driver
)

with open('scripts/batch13_dump.json') as f:
    probs = json.load(f)

for p in probs:
    pid = p['id']
    fn = p['fn_name']
    tcs = [{'id': i+1, 'input_data': json.dumps(tc['input']), 'expected_output': json.dumps(tc['output']), 'is_hidden': False} for i, tc in enumerate(p['test_cases'])]
    
    j_drv = _generate_java_driver(fn, tcs)
    c_drv = _generate_cpp_driver(fn, tcs)
    
    # Check if there are different types across TCs in Java
    j_calls = [l.strip() for l in j_drv.split('\n') if 'sol.' in l]
    patterns = set()
    for jc in j_calls:
        sig = re.sub(r'\"[^\"]*\"', '"str"', jc)
        sig = re.sub(r'\b\d+\b', 'NUM', sig)
        # ignore array size differences e.g. new int[]{NUM, NUM} vs new int[]{NUM}
        sig = re.sub(r'NUM(, NUM)+', 'NUMS', sig)
        patterns.add(sig)
    if len(patterns) > 1:
        print(f"ID {pid} ({fn}) has multiple Java signatures:")
        for pat in patterns:
            print("  ", pat)
