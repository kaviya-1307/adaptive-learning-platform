import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json
from app.core.database import SessionLocal
from app.models.problem import Problem
from app.engine.code_runner import JavaScriptCodeRunner, JavaCodeRunner, CppCodeRunner

db = SessionLocal()
p = db.query(Problem).filter(Problem.id == 393).first()
tcs = [{'id': tc.id, 'input_data': tc.input_data, 'expected_output': tc.expected_output, 'is_hidden': tc.is_hidden} for tc in p.test_cases]
db.close()

# JS
js_code = """function rearrange_bigger(n) {
    const digits = String(n).split('');
    let i = digits.length - 2;
    while (i >= 0 && digits[i] >= digits[i + 1]) i--;
    if (i < 0) return false;
    let j = digits.length - 1;
    while (digits[j] <= digits[i]) j--;
    let t = digits[i]; digits[i] = digits[j]; digits[j] = t;
    const right = digits.slice(i + 1).sort();
    const res = digits.slice(0, i + 1).concat(right).join('');
    return parseInt(res, 10);
}"""
js_res = JavaScriptCodeRunner.execute(js_code, tcs, starter_code="function rearrange_bigger(n) {}", is_submission=True)
print("JS:", js_res.get("status"), js_res.get("compile_error"))

# Java
java_code = """import java.util.*;
class Solution {
    public Object rearrange_bigger(int n) {
        char[] digits = String.valueOf(n).toCharArray();
        int i = digits.length - 2;
        while (i >= 0 && digits[i] >= digits[i + 1]) i--;
        if (i < 0) return false;
        int j = digits.length - 1;
        while (digits[j] <= digits[i]) j--;
        char temp = digits[i];
        digits[i] = digits[j];
        digits[j] = temp;
        Arrays.sort(digits, i + 1, digits.length);
        return Integer.parseInt(new String(digits));
    }
}"""
java_starter = """class Solution {
    public Object rearrange_bigger(int n) {
        return false;
    }
}"""
java_res = JavaCodeRunner.execute(java_code, tcs, starter_code=java_starter, is_submission=True)
print("Java:", java_res.get("status"), java_res.get("compile_error"), (java_res.get("results") or [{}])[0].get("error_message"))

# C++
cpp_code = """#include <string>
#include <algorithm>
#include <iostream>
using namespace std;

struct RearrangeResult {
    bool is_false = false;
    int val = 0;
    bool operator==(bool b) const { return (!b) ? is_false : !is_false; }
    bool operator==(int v) const { return !is_false && val == v; }
    friend ostream& operator<<(ostream& os, const RearrangeResult& r) {
        if (r.is_false) os << "false";
        else os << r.val;
        return os;
    }
};

class Solution {
public:
    RearrangeResult rearrange_bigger(int n) {
        RearrangeResult res;
        string s = to_string(n);
        int i = (int)s.size() - 2;
        while (i >= 0 && s[i] >= s[i + 1]) i--;
        if (i < 0) {
            res.is_false = true;
            return res;
        }
        int j = (int)s.size() - 1;
        while (s[j] <= s[i]) j--;
        swap(s[i], s[j]);
        sort(s.begin() + i + 1, s.end());
        res.is_false = false;
        res.val = stoi(s);
        return res;
    }
};"""
cpp_starter = """class Solution {
public:
    RearrangeResult rearrange_bigger(int n);
};"""
cpp_res = CppCodeRunner.execute(cpp_code, tcs, starter_code=cpp_starter, is_submission=True)
print("Cpp:", cpp_res.get("status"), cpp_res.get("compile_error"), (cpp_res.get("results") or [{}])[0].get("error_message"))
