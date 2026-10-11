import re
import json

log_path = "C:/Users/Welcome/.gemini/antigravity-ide/brain/9721effd-bff9-4657-8a48-395520ba5c7e/.system_generated/tasks/task-578.log"
with open(log_path, "r", encoding="utf-8") as f:
    text = f.read()

# Find all failed problem IDs
failed_ids = set()
for m in re.finditer(r"PID\s+(\d+)", text):
    failed_ids.add(int(m.group(1)))

failed_ids = sorted(list(failed_ids))
print(f"Total failed problem IDs in Batch 9: {len(failed_ids)}")
print("Failed IDs:", failed_ids)

with open("scripts/batch9_dump.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for p in data:
    if p["id"] in failed_ids:
        print("=" * 60)
        print(f"PID {p['id']}: {p['fn_name']}")
        print(p["ref_py"].strip())
        print("Tests:")
        for tc in p["test_cases"]:
            print(f"  {tc['input']} -> {tc['output']}")
