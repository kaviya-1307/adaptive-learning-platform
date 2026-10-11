import sys
import json

start_idx = int(sys.argv[1]) if len(sys.argv) > 1 else 0
count = int(sys.argv[2]) if len(sys.argv) > 2 else 10

with open('scripts/batch15_dump.json', 'r', encoding='utf-8') as f:
    probs = json.load(f)

for p in probs[start_idx:start_idx + count]:
    print(f"=== ID {p['id']}: {p['fn_name']} ({p['title']}) ===")
    print("Ref py:\n" + p['ref_py'].strip())
    print("TCs:")
    for tc in p['test_cases']:
        print(" ", tc['input'], "->", tc['output'])
    print()
