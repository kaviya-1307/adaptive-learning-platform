import sys
import json
sys.path.insert(0, '.')

from app.engine.code_runner import (
    _generate_java_driver,
    _generate_cpp_driver
)

pid = 701
with open('scripts/batch13_dump.json') as f:
    probs = json.load(f)

p = [x for x in probs if x['id'] == pid][0]
tcs = [{'id': i+1, 'input_data': json.dumps(tc['input']), 'expected_output': json.dumps(tc['output']), 'is_hidden': False} for i, tc in enumerate(p['test_cases'])]

print("--- C++ DRIVER 701 ---")
drv = _generate_cpp_driver(p['fn_name'], tcs)
print("\n".join(drv.splitlines()[-40:]))

print("--- JAVA DRIVER 701 ---")
drv = _generate_java_driver(p['fn_name'], tcs)
print("\n".join(drv.splitlines()[-40:]))
