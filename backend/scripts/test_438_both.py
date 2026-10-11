import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.engine.code_runner import CppCodeRunner, JavaCodeRunner

java_code = """
import java.util.*;
class Solution {
    public int[] Find_Min(int[][] lst) {
        int[] min = lst[0];
        for (int i = 1; i < lst.length; i++) {
            int[] a = min, b = lst[i];
            int len = Math.min(a.length, b.length);
            int diff = 0;
            for (int j = 0; j < len; j++) {
                if (a[j] < b[j]) { diff = -1; break; }
                if (a[j] > b[j]) { diff = 1; break; }
            }
            if (diff == 0) {
                if (b.length < a.length) min = b;
            } else if (diff > 0) {
                min = b;
            }
        }
        return min;
    }
    public Object Find_Min(char[][] lst) {
        char[] min = lst[0];
        for (int i = 1; i < lst.length; i++) {
            char[] a = min, b = lst[i];
            int len = Math.min(a.length, b.length);
            int diff = 0;
            for (int j = 0; j < len; j++) {
                if (a[j] < b[j]) { diff = -1; break; }
                if (a[j] > b[j]) { diff = 1; break; }
            }
            if (diff == 0) {
                if (b.length < a.length) min = b;
            } else if (diff > 0) {
                min = b;
            }
        }
        String[] res = new String[min.length];
        for (int i = 0; i < min.length; i++) res[i] = String.valueOf(min[i]);
        return res;
    }
    public String[] Find_Min(String[][] lst) {
        String[] min = lst[0];
        for (int i = 1; i < lst.length; i++) {
            String[] a = min, b = lst[i];
            int len = Math.min(a.length, b.length);
            int diff = 0;
            for (int j = 0; j < len; j++) {
                int cmp = a[j].compareTo(b[j]);
                if (cmp < 0) { diff = -1; break; }
                if (cmp > 0) { diff = 1; break; }
            }
            if (diff == 0) {
                if (b.length < a.length) min = b;
            } else if (diff > 0) {
                min = b;
            }
        }
        return min;
    }
}
"""

cpp_code = """
#include <vector>
#include <string>
#include <iostream>
using namespace std;

struct MinListResult {
    vector<int> int_res;
    vector<string> str_res;
    bool is_str = false;

    bool operator==(const vector<int>& o) const { return int_res == o; }
    bool operator==(const vector<string>& o) const { return str_res == o; }
    friend ostream& operator<<(ostream& os, const MinListResult& r) {
        if (r.is_str) {
            os << "[";
            for (size_t i = 0; i < r.str_res.size(); ++i) {
                if (i > 0) os << ", ";
                os << "\\\"" << r.str_res[i] << "\\\"";
            }
            os << "]";
        } else {
            os << "[";
            for (size_t i = 0; i < r.int_res.size(); ++i) {
                if (i > 0) os << ", ";
                os << r.int_res[i];
            }
            os << "]";
        }
        return os;
    }
};

class Solution {
public:
    MinListResult Find_Min(const vector<vector<int>>& lst) {
        auto min = lst[0];
        for (size_t i = 1; i < lst.size(); ++i) if (lst[i] < min) min = lst[i];
        MinListResult r;
        r.int_res = min;
        return r;
    }
    template <typename T>
    MinListResult Find_Min(const vector<vector<T>>& lst) {
        auto min = lst[0];
        for (size_t i = 1; i < lst.size(); ++i) if (lst[i] < min) min = lst[i];
        MinListResult r;
        r.is_str = true;
        for (auto c : min) r.str_res.push_back(string(1, c));
        return r;
    }
};
"""

tcs = [
    {'id': 1, 'input_data': '{"lst": [[1], [1, 2], [1, 2, 3]]}', 'expected_output': '[1]', 'is_hidden': False},
    {'id': 2, 'input_data': '{"lst": [[1, 1], [1, 1, 1], [1, 2, 7, 8]]}', 'expected_output': '[1, 1]', 'is_hidden': False},
    {'id': 3, 'input_data': '{"lst": [["x"], ["x", "y"], ["x", "y", "z"]]}', 'expected_output': '["x"]', 'is_hidden': False}
]

res_java = JavaCodeRunner.execute(java_code, tcs, is_submission=True)
print("PID 438 Java Result:", res_java["status"], f"{res_java['passed_test_cases']}/{res_java['total_test_cases']}")
if res_java.get("compile_error"):
    print("Java Error:", res_java["compile_error"][:200])

res_cpp = CppCodeRunner.execute(cpp_code, tcs, is_submission=True)
print("PID 438 C++ Result:", res_cpp["status"], f"{res_cpp['passed_test_cases']}/{res_cpp['total_test_cases']}")
if res_cpp.get("compile_error"):
    print("C++ Error:", res_cpp["compile_error"][:200])
