import json

with open("scripts/batch7_dump.json", "r", encoding="utf-8") as f:
    probs = json.load(f)

failed_ids = [362, 364, 365, 366, 367, 369, 370, 375, 376, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 402, 403, 405, 406, 407, 408, 409, 410]

for p in probs:
    if p["id"] in failed_ids:
        print("="*60)
        print(f"ID {p['id']} ({p['fn_name']}): {p['title']}")
        print("Python Solution:")
        print(p["ref_py"].strip())
        print("Test Cases:")
        for idx, tc in enumerate(p["test_cases"]):
            print(f"  TC {idx+1}: inp={tc['input']} -> out={tc['output']}")
