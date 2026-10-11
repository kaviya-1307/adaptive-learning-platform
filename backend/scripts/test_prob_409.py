import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json
from app.core.database import SessionLocal
from app.models.problem import Problem
from app.engine.code_runner import JavaScriptCodeRunner, JavaCodeRunner, CppCodeRunner

db = SessionLocal()
p = db.query(Problem).filter(Problem.id == 409).first()
tcs = [{'id': tc.id, 'input_data': tc.input_data, 'expected_output': tc.expected_output, 'is_hidden': tc.is_hidden} for tc in p.test_cases]
db.close()

# JS
js_code = """function count_element_in_list(list1, x) {
    let ctr = 0;
    for (const row of list1) {
        if (row.includes(x)) ctr++;
    }
    return ctr;
}"""
js_res = JavaScriptCodeRunner.execute(js_code, tcs, starter_code="function count_element_in_list(list1, x) {}", is_submission=True)
print("JS:", js_res.get("status"), js_res.get("compile_error"))

# Java
java_code = """import java.util.*;
class Solution {
    public int count_element_in_list(Object list1, Object x) {
        int ctr = 0;
        if (list1 instanceof int[][]) {
            int target = Integer.parseInt(String.valueOf(x));
            for (int[] row : (int[][]) list1) {
                for (int v : row) if (v == target) { ctr++; break; }
            }
        } else if (list1 instanceof char[][]) {
            char target = String.valueOf(x).charAt(0);
            for (char[] row : (char[][]) list1) {
                for (char v : row) if (v == target) { ctr++; break; }
            }
        } else if (list1 instanceof Object[][]) {
            for (Object[] row : (Object[][]) list1) {
                for (Object v : row) if (Objects.equals(v, x) || Objects.equals(String.valueOf(v), String.valueOf(x))) { ctr++; break; }
            }
        }
        return ctr;
    }
}"""
java_starter = """class Solution {
    public int count_element_in_list(Object list1, Object x) {
        return 0;
    }
}"""
java_res = JavaCodeRunner.execute(java_code, tcs, starter_code=java_starter, is_submission=True)
print("Java:", java_res.get("status"), java_res.get("compile_error"), (java_res.get("results") or [{}])[0].get("error_message"))

# C++
cpp_code = """#include <vector>
#include <string>
#include <algorithm>
using namespace std;

class Solution {
public:
    int count_element_in_list(const vector<vector<int>>& list1, int x) {
        int ctr = 0;
        for (const auto& row : list1) {
            if (find(row.begin(), row.end(), x) != row.end()) ctr++;
        }
        return ctr;
    }
    int count_element_in_list(const vector<vector<char>>& list1, const string& x) {
        char target = x.empty() ? '\\0' : x[0];
        int ctr = 0;
        for (const auto& row : list1) {
            if (find(row.begin(), row.end(), target) != row.end()) ctr++;
        }
        return ctr;
    }
    int count_element_in_list(const vector<vector<char>>& list1, char x) {
        int ctr = 0;
        for (const auto& row : list1) {
            if (find(row.begin(), row.end(), x) != row.end()) ctr++;
        }
        return ctr;
    }
    int count_element_in_list(const vector<vector<string>>& list1, const string& x) {
        int ctr = 0;
        for (const auto& row : list1) {
            if (find(row.begin(), row.end(), x) != row.end()) ctr++;
        }
        return ctr;
    }
};"""
cpp_starter = """#include <vector>
using namespace std;
class Solution {
public:
    template <typename T, typename U>
    int count_element_in_list(const T& list1, const U& x);
};"""
cpp_res = CppCodeRunner.execute(cpp_code, tcs, starter_code=cpp_starter, is_submission=True)
print("Cpp:", cpp_res.get("status"), cpp_res.get("compile_error"), (cpp_res.get("results") or [{}])[0].get("error_message"))
