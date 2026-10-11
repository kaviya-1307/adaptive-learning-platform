import sys
import json
sys.path.insert(0, '.')

from app.engine.code_runner import (
    _generate_java_driver,
    _generate_cpp_driver
)

pid = int(sys.argv[1])
with open('scripts/batch13_dump.json') as f:
    probs = json.load(f)

p = [x for x in probs if x['id'] == pid][0]
tcs = [{'id': i+1, 'input_data': json.dumps(tc['input']), 'expected_output': json.dumps(tc['output']), 'is_hidden': False} for i, tc in enumerate(p['test_cases'])]

print(f"=== Problem {pid} ({p['fn_name']}) ===")
print("--- JAVA DRIVER ---")
drv = _generate_java_driver(p['fn_name'], tcs)
for l in drv.splitlines():
    if 'sol.' in l or ('checkEqual' in l and 'static' not in l and 'm2.get' not in l):
        print("  ", l.strip())

print("--- C++ DRIVER ---")
drv = _generate_cpp_driver(p['fn_name'], tcs)
for l in drv.splitlines():
    if 'sol.' in l or 'auto arg_' in l or ('checkEqual' in l and 'static' not in l):
        print("  ", l.strip())

