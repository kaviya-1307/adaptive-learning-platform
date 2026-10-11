import sys
import json

with open('scripts/batch13_dump.json', 'r', encoding='utf-8') as f:
    problems = json.load(f)

start_id = int(sys.argv[1]) if len(sys.argv) > 1 else 661
end_id = int(sys.argv[2]) if len(sys.argv) > 2 else 710

for p in problems:
    pid = p['id']
    if pid < start_id or pid > end_id:
        continue
    print(f"==================== ID {pid}: {p['fn_name']} ====================")
    print("PYTHON REF:")
    print(p['ref_py'])
    print("TEST CASES:")
    for tc in p['test_cases']:
        print(f"  IN: {tc['input']}  -->  OUT: {tc['output']}")
    print()
