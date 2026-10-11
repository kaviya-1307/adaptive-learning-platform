import json

with open('scripts/batch10_dump.json', 'r', encoding='utf-8') as f:
    problems = json.load(f)

print(f"Total problems in Batch 10: {len(problems)}")
for p in problems:
    pid = p['id']
    fn = p['fn_name']
    tc = p['test_cases'][0]
    in_args = list(tc['input'].keys())
    out_val = tc['output']
    out_t = type(out_val).__name__
    print(f"ID {pid:3d}: {fn:30s} | In: {str(in_args):25s} | Out ({out_t}): {str(out_val)[:30]}")
