import sys
import json
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
    
    # Test Java driver generation
    try:
        j_drv = _generate_java_driver(fn, tcs)
    except Exception as e:
        print(f"ID {pid} Java Driver Generation Exception: {e}")
        
    # Test C++ driver generation
    try:
        c_drv = _generate_cpp_driver(fn, tcs)
        # Check if C++ driver has obvious syntax errors like vector<int> initialized with vector<string>
        if "std::vector<int>>{{" in c_drv and "std::vector<std::string>" in c_drv:
            print(f"ID {pid} C++ Driver Type Mismatch: vector<int> with vector<string>")
    except Exception as e:
        print(f"ID {pid} C++ Driver Generation Exception: {e}")

print("Driver check completed.")
