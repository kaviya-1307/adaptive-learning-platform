import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.engine.code_runner import CppCodeRunner, JavaCodeRunner

cpp_code = """
#ifndef null
#define null ""
#endif
#include <unordered_map>
#include <string>
using namespace std;
class Solution {
public:
    unordered_map<string, string> drop_empty(const unordered_map<string, string>& dict1) {
        unordered_map<string, string> res;
        for (const auto& p : dict1) {
            if (!p.second.empty() && p.second != "null" && p.second != "None") {
                res[p.first] = p.second;
            }
        }
        return res;
    }
};
"""
tcs = [
    {'id': 1, 'input_data': '{"dict1": {"c1": "Red", "c2": "Green", "c3": null}}', 'expected_output': '{"c1": "Red", "c2": "Green"}', 'is_hidden': False},
    {'id': 2, 'input_data': '{"dict1": {"c1": "Red", "c2": null, "c3": null}}', 'expected_output': '{"c1": "Red"}', 'is_hidden': False},
    {'id': 3, 'input_data': '{"dict1": {"c1": null, "c2": "Green", "c3": null}}', 'expected_output': '{"c2": "Green"}', 'is_hidden': False}
]
res = CppCodeRunner.execute(cpp_code, tcs, is_submission=True)
print("PID 446 C++ Result:", res["status"], f"{res['passed_test_cases']}/{res['total_test_cases']}")
if res.get("compile_error"):
    print("Compile error:", res["compile_error"][:200])
