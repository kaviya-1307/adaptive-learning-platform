import re
import json

with open("scripts/batch9_dump.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Auto-passed problems in all 3 languages
import sys
min_id = int(sys.argv[1]) if len(sys.argv) > 1 else 461
max_id = int(sys.argv[2]) if len(sys.argv) > 2 else 510

passed_all = {465, 466, 468, 471, 473, 474, 475, 477, 479, 486, 491, 495, 499, 501, 502, 506}
failed_probs = [p for p in data if p["id"] not in passed_all and min_id <= p["id"] <= max_id]

print(f"Total failed problems to implement: {len(failed_probs)}")

for p in failed_probs:
    print(f"=== PID {p['id']}: {p['fn_name']} ===")
    print(p["ref_py"].strip())
    print("Tests:")
    for tc in p["test_cases"]:
        print(f"  {tc['input']} -> {tc['output']}")
    print("-" * 50)
