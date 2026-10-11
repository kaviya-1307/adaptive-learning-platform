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
    
    print(f"=== ID {pid:3d} | {fn:30s} ===")
    # Java
    try:
        j_driver = _generate_java_driver(fn, tcs)
        j_calls = [l.strip() for l in j_driver.split('\n') if 'sol.' in l or ('checkEqual' in l and 'static' not in l and 'm2.get' not in l)]
        for jc in j_calls:
            print('   Java:', jc[:110])
    except Exception as e:
        print('   Java error:', e)
    # C++
    try:
        c_driver = _generate_cpp_driver(fn, tcs)
        c_calls = [l.strip() for l in c_driver.split('\n') if 'sol.' in l or 'auto arg_' in l or ('checkEqual' in l and 'static' not in l)]
        for cc in c_calls:
            print('   C++: ', cc[:110])
    except Exception as e:
        print('   C++ error:', e)
    print()
