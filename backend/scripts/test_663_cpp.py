import sys
import json
sys.path.insert(0, '.')

from app.engine.code_runner import CppCodeRunner

with open('scripts/batch13_dump.json') as f:
    probs = json.load(f)

p663 = [p for p in probs if p['id'] == 663][0]
tcs663 = [{'id': i+1, 'input_data': json.dumps(tc['input']), 'expected_output': json.dumps(tc['output']), 'is_hidden': False} for i, tc in enumerate(p663['test_cases'])]

cpp_code = """#include <vector>
#include <string>
#include <algorithm>

class Solution {
public:
    std::vector<std::vector<int>> remove_duplicate(std::vector<std::vector<int>> a) {
        std::sort(a.begin(), a.end());
        a.erase(std::unique(a.begin(), a.end()), a.end());
        return a;
    }
    std::vector<std::string> remove_duplicate(std::vector<std::string> a) {
        std::sort(a.begin(), a.end());
        a.erase(std::unique(a.begin(), a.end()), a.end());
        return a;
    }
    std::vector<int> remove_duplicate(std::vector<int> a) {
        std::sort(a.begin(), a.end());
        a.erase(std::unique(a.begin(), a.end()), a.end());
        return a;
    }
};"""

res = CppCodeRunner.execute(cpp_code, tcs663, starter_code="class Solution {};", is_submission=True)
print("663 C++ Status:", res.get('status'))
print("663 Compile error:", res.get('compile_error'))
