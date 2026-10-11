import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json
from app.core.database import SessionLocal
from app.models.problem import Problem
from app.engine.code_runner import JavaScriptCodeRunner, JavaCodeRunner, CppCodeRunner

db = SessionLocal()
p = db.query(Problem).filter(Problem.id == 354).first()
tcs = [{'id': tc.id, 'input_data': tc.input_data, 'expected_output': tc.expected_output, 'is_hidden': tc.is_hidden} for tc in p.test_cases]
db.close()

# JS
js_code = """function remove_empty(list1) {
    return list1.filter(x => {
        if (Array.isArray(x)) return x.length > 0;
        return Boolean(x);
    });
}"""
js_res = JavaScriptCodeRunner.execute(js_code, tcs, starter_code="function remove_empty(list1) {}", is_submission=True)
print("JS:", js_res.get("status"), js_res.get("compile_error"), (js_res.get("results") or [{}])[0].get("actual_output"))

# Java
java_code = """import java.util.*;
class Solution {
    public Object[] remove_empty(Object[] list1) {
        List<Object> res = new ArrayList<>();
        for (Object x : list1) {
            if (x instanceof Object[]) {
                if (((Object[]) x).length > 0) res.add(x);
            } else if (x instanceof int[]) {
                if (((int[]) x).length > 0) res.add(x);
            } else if (x instanceof String) {
                if (!((String) x).isEmpty()) res.add(x);
            } else if (x != null) {
                res.add(x);
            }
        }
        return res.toArray();
    }
}"""
java_starter = """class Solution {
    public Object[] remove_empty(Object[] list1) {
        return new Object[]{};
    }
}"""
java_res = JavaCodeRunner.execute(java_code, tcs, starter_code=java_starter, is_submission=True)
print("Java:", java_res.get("status"), java_res.get("compile_error"), (java_res.get("results") or [{}])[0].get("error_message"))

# C++
cpp_code = """#include <vector>
#include <string>
#include <iostream>
using namespace std;

class Solution {
public:
    vector<string> remove_empty(const vector<string>& list1) {
        vector<string> res;
        for (const auto& s : list1) {
            if (!s.empty() && s != "[]") res.push_back(s);
        }
        return res;
    }
};"""
cpp_starter = """#include <vector>
#include <string>
using namespace std;
class Solution {
public:
    vector<string> remove_empty(const vector<string>& list1);
};"""
cpp_res = CppCodeRunner.execute(cpp_code, tcs, starter_code=cpp_starter, is_submission=True)
print("Cpp:", cpp_res.get("status"), cpp_res.get("compile_error"), (cpp_res.get("results") or [{}])[0].get("error_message"))
