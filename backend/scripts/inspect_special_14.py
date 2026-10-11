import json

with open('scripts/batch14_dump.json') as f:
    probs = json.load(f)

for pid in [721, 732, 738, 747, 756]:
    p = [x for x in probs if x['id'] == pid][0]
    print(f"=== ID {pid}: {p['fn_name']} ===")
    print("Ref py:\n", p['ref_py'])
    for tc in p['test_cases']:
        print("  IN:", tc['input'], "--> OUT:", tc['output'])
