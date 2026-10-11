import sys
import json
sys.path.insert(0, '.')

from app.engine.code_runner import CppCodeRunner

with open('scripts/batch13_dump.json') as f:
    probs = json.load(f)

p701 = [p for p in probs if p['id'] == 701][0]
tcs701 = [{'id': i+1, 'input_data': json.dumps(tc['input']), 'expected_output': json.dumps(tc['output']), 'is_hidden': False} for i, tc in enumerate(p701['test_cases'])]

cpp_code = """#include <vector>
#include <string>
#include <set>

class Solution {
public:
    double second_smallest(const std::vector<int>& numbers) {
        if (numbers.size() < 2) return 0;
        std::set<int> uniq(numbers.begin(), numbers.end());
        if (uniq.size() < 2) return 0;
        auto it = uniq.begin();
        ++it;
        return *it;
    }
    double second_smallest(const std::vector<std::string>& numbers) {
        if (numbers.size() < 2) return 0;
        std::set<double> uniq;
        for (const auto& s : numbers) uniq.insert(std::stod(s));
        if (uniq.size() < 2) return 0;
        auto it = uniq.begin();
        ++it;
        return *it;
    }
};"""

res = CppCodeRunner.execute(cpp_code, tcs701, starter_code="class Solution {};", is_submission=True)
print("701 C++ Status:", res.get('status'))
print("701 Compile error:", res.get('compile_error'))
for i, r in enumerate(res.get('results', [])):
    print(f"  TC {i+1}: status={r.get('status')}, actual={r.get('actual_output')}")
