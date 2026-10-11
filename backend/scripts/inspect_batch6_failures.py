import json

with open("scripts/batch6_dump.json", "r", encoding="utf-8") as f:
    probs = json.load(f)

failed_ids = [312, 314, 315, 319, 320, 322, 324, 328, 329, 334, 336, 338, 342, 343, 344, 345, 346, 350, 351, 354, 355, 356, 358, 360]

for p in probs:
    if p["id"] in failed_ids:
        print("="*60)
        print(f"ID {p['id']} ({p['fn_name']}): {p['title']}")
        print("Python Solution:")
        print(p["ref_py"].strip())
        print("Test Cases:")
        for idx, tc in enumerate(p["test_cases"]):
            print(f"  TC {idx+1}: inp={tc['input']} -> out={tc['output']}")
