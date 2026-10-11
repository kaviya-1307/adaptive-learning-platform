import json
import sys

def inspect_problems(start_id, end_id):
    with open("scripts/batch7_dump.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    for p in data:
        if start_id <= p["id"] <= end_id:
            print("="*60)
            print(f"ID {p['id']} ({p['fn_name']}): {p['title']}")
            print("Python Solution:")
            print(p["ref_py"].strip())
            print("Test Cases:")
            for idx, tc in enumerate(p["test_cases"]):
                print(f"  TC {idx+1}: {tc['input']} -> {tc['output']}")

if __name__ == "__main__":
    s = int(sys.argv[1]) if len(sys.argv) > 1 else 361
    e = int(sys.argv[2]) if len(sys.argv) > 2 else 380
    inspect_problems(s, e)
