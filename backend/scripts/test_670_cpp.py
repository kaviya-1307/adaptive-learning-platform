import sys
import json
sys.path.insert(0, '.')

from app.engine.code_runner import CppCodeRunner

with open('scripts/batch13_dump.json') as f:
    probs = json.load(f)

p670 = [p for p in probs if p['id'] == 670][0]
tcs670 = [{'id': i+1, 'input_data': json.dumps(tc['input']), 'expected_output': json.dumps(tc['output']), 'is_hidden': False} for i, tc in enumerate(p670['test_cases'])]

cpp_code = """#include <unordered_map>
#include <vector>
#include <string>

class Solution {
public:
    std::unordered_map<std::string, std::vector<std::string>> filter_data(
        const std::unordered_map<std::string, std::vector<std::string>>& students,
        double h,
        int w
    ) {
        std::unordered_map<std::string, std::vector<std::string>> res;
        for (const auto& p : students) {
            double height = std::stod(p.second[0]);
            int weight = std::stoi(p.second[1]);
            if (height >= h && weight >= w) {
                res[p.first] = p.second;
            }
        }
        return res;
    }
};"""

res = CppCodeRunner.execute(cpp_code, tcs670, starter_code="class Solution {};", is_submission=True)
print("670 C++ Status:", res.get('status'))
print("670 Compile error:", res.get('compile_error'))
for i, r in enumerate(res.get('results', [])):
    print(f"  TC {i+1}: status={r.get('status')}, actual={r.get('actual_output')}")
