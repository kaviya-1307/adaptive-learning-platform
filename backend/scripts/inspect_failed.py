import json

with open('scripts/batch8_dump.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

failed_ids = [411, 412, 414, 415, 416, 419, 420, 422, 424, 426, 427, 428, 431, 433, 437, 438, 440]

for p in data:
    pid = p['id']
    if pid in failed_ids:
        print(f"=== PID {pid}: {p['fn_name']} ===")
        print(p['ref_py'].strip())
        print('Tests:')
        for tc in p['test_cases']:
            print(f"  {tc['input']} -> {tc['output']}")
        print('-' * 40)
