import json
import sys

def inspect(s_id=411, e_id=460):
    with open("scripts/batch8_dump.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    for p in data:
        if s_id <= p["id"] <= e_id:
            print("="*60)
            print(f"ID {p['id']} ({p['fn_name']}): {p['title']}")
            print("Python:")
            print(p["ref_py"].strip())
            print("Test Cases:")
            for idx, tc in enumerate(p["test_cases"]):
                print(f"  TC {idx+1}: {tc['input']} -> {tc['output']}")

if __name__ == "__main__":
    s = int(sys.argv[1]) if len(sys.argv) > 1 else 411
    e = int(sys.argv[2]) if len(sys.argv) > 2 else 460
    inspect(s, e)
