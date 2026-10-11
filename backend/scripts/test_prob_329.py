import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json
from app.core.database import SessionLocal
from app.models.problem import Problem
from app.engine.code_runner import JavaScriptCodeRunner, JavaCodeRunner, CppCodeRunner

db = SessionLocal()
p = db.query(Problem).filter(Problem.id == 329).first()
tcs = [{'id': tc.id, 'input_data': tc.input_data, 'expected_output': tc.expected_output, 'is_hidden': tc.is_hidden} for tc in p.test_cases]
db.close()

# 1. JS
js_code = """function Sort(sub_li) {
    return [...sub_li].sort((a, b) => {
        let va = Number(a[1]);
        let vb = Number(b[1]);
        return va - vb;
    });
}"""
js_res = JavaScriptCodeRunner.execute(js_code, tcs, starter_code="function Sort(sub_li) {}", is_submission=True)
print("JS:", js_res.get("status"), js_res.get("compile_error"))

# 2. Java
java_code = """import java.util.*;
class Solution {
    public Object[][] Sort(Object[][] sub_li) {
        Object[][] res = sub_li.clone();
        Arrays.sort(res, (a, b) -> {
            int va = Integer.parseInt(String.valueOf(a[1]));
            int vb = Integer.parseInt(String.valueOf(b[1]));
            return Integer.compare(va, vb);
        });
        return res;
    }
}"""
java_starter = """class Solution {
    public Object[][] Sort(Object[][] sub_li) {
        return new Object[][]{};
    }
}"""
java_res = JavaCodeRunner.execute(java_code, tcs, starter_code=java_starter, is_submission=True)
print("Java:", java_res.get("status"), java_res.get("compile_error"), (java_res.get("results") or [{}])[0].get("error_message"))

# 3. C++
cpp_code = """#include <vector>
#include <string>
#include <algorithm>
#include <iostream>
using namespace std;
class Solution {
public:
    vector<vector<string>> Sort(vector<vector<string>> sub_li) {
        sort(sub_li.begin(), sub_li.end(), [](const vector<string>& a, const vector<string>& b) {
            return stoi(a[1]) < stoi(b[1]);
        });
        return sub_li;
    }
};"""
cpp_starter = """#include <vector>
#include <string>
using namespace std;
class Solution {
public:
    vector<vector<string>> Sort(vector<vector<string>> sub_li);
};"""
cpp_res = CppCodeRunner.execute(cpp_code, tcs, starter_code=cpp_starter, is_submission=True)
print("Cpp:", cpp_res.get("status"), cpp_res.get("compile_error"), (cpp_res.get("results") or [{}])[0].get("error_message"))
