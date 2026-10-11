import ast
import json
import re
from typing import List, Dict, Any, Optional

def infer_cpp_type(val: Any) -> str:
    if isinstance(val, bool):
        return "bool"
    if isinstance(val, int):
        return "int"
    if isinstance(val, float):
        return "double"
    if isinstance(val, str):
        return "string"
    if isinstance(val, list):
        if not val:
            return "vector<int>"
        inner = infer_cpp_type(val[0])
        return f"vector<{inner}>"
    if isinstance(val, dict):
        return "unordered_map<string, int>"
    return "auto"

CPP_HEADER = """#include <iostream>
#include <vector>
#include <string>
#include <cmath>
#include <algorithm>
#include <numeric>
#include <unordered_map>
#include <unordered_set>
#include <queue>
#include <stack>
#include <sstream>
#include <regex>

using namespace std;

inline long long _gcd(long long a, long long b) {
    a = std::abs(a); b = std::abs(b);
    while (b) { long long t = b; b = a % b; a = t; }
    return a;
}

template <typename T>
inline int len(const T& c) {
    return static_cast<int>(c.size());
}

template <typename T>
inline auto sum(const vector<T>& v) {
    T s = 0;
    for (const auto& x : v) s += x;
    return s;
}

template <typename T>
inline bool _in(const T& val, const vector<T>& vec) {
    return std::find(vec.begin(), vec.end(), val) != vec.end();
}

inline bool _in(char ch, const string& s) {
    return s.find(ch) != string::npos;
}

inline bool _in(const string& sub, const string& s) {
    return s.find(sub) != string::npos;
}

template <typename K, typename V>
inline bool _in(const K& key, const unordered_map<K, V>& m) {
    return m.find(key) != m.end();
}

template <typename K>
inline bool _in(const K& key, const unordered_set<K>& s) {
    return s.find(key) != s.end();
}

template <typename T>
inline vector<T> _sorted(vector<T> v) {
    std::sort(v.begin(), v.end());
    return v;
}

inline string _sorted(string s) {
    std::sort(s.begin(), s.end());
    return s;
}

inline string _reverse(string s) {
    std::reverse(s.begin(), s.end());
    return s;
}

template <typename T>
inline vector<T> _reverse(vector<T> v) {
    std::reverse(v.begin(), v.end());
    return v;
}

template <typename T>
inline vector<T> _nlargest(int n, vector<T> v) {
    std::sort(v.begin(), v.end(), std::greater<T>());
    if (n < (int)v.size()) v.resize(n);
    return v;
}

template <typename T>
inline vector<T> _nsmallest(int n, vector<T> v) {
    std::sort(v.begin(), v.end());
    if (n < (int)v.size()) v.resize(n);
    return v;
}

struct _HeapQ {
    template <typename T>
    vector<T> nlargest(int n, vector<T> v) { return _nlargest(n, v); }
    template <typename T>
    vector<T> nsmallest(int n, vector<T> v) { return _nsmallest(n, v); }
    template <typename T>
    void heappush(vector<T>& v, T val) { v.push_back(val); std::push_heap(v.begin(), v.end(), std::greater<T>()); }
    template <typename T>
    T heappop(vector<T>& v) { std::pop_heap(v.begin(), v.end(), std::greater<T>()); T ret = v.back(); v.pop_back(); return ret; }
};
static _HeapQ heapq;
static _HeapQ hq;

struct _Re {
    vector<string> findall(const string& pat, const string& text) {
        try {
            regex r(pat);
            sregex_iterator next(text.begin(), text.end(), r);
            sregex_iterator end;
            vector<string> res;
            while (next != end) {
                smatch match = *next;
                if (match.size() > 1) res.push_back(match[1].str());
                else res.push_back(match.str());
                next++;
            }
            return res;
        } catch (...) {
            return {};
        }
    }
    bool search(const string& pat, const string& text) {
        try {
            return regex_search(text, regex(pat));
        } catch (...) {
            return false;
        }
    }
    string sub(const string& pat, const string& repl, const string& text) {
        try {
            return regex_replace(text, regex(pat), repl);
        } catch (...) {
            return text;
        }
    }
};
static _Re re;
"""

class PyToCppVisitor(ast.NodeVisitor):
    def __init__(self, ret_type: str, param_types: Dict[str, str]):
        self.ret_type = ret_type
        self.param_types = param_types
        self.declared_vars = set(param_types.keys())
        self.indent_level = 1

    def indent(self) -> str:
        return "    " * self.indent_level

    def visit_Module(self, node: ast.Module) -> str:
        body = []
        for stmt in node.body:
            c = self.visit(stmt)
            if c:
                body.append(c)
        return "\n".join(body)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> str:
        fn_name = node.name
        params = []
        for a in node.args.args:
            ptype = self.param_types.get(a.arg, "auto")
            if "vector" in ptype or ptype == "string":
                params.append(f"const {ptype}& {a.arg}")
            else:
                params.append(f"{ptype} {a.arg}")
            self.declared_vars.add(a.arg)

        self.indent_level += 1
        body_lines = []
        for stmt in node.body:
            c = self.visit(stmt)
            if c:
                body_lines.append(c)
        self.indent_level -= 1

        body_str = "\n".join(body_lines)
        return f"{self.indent()}{self.ret_type} {fn_name}({', '.join(params)}) {{\n{body_str}\n{self.indent()}}}"

    def visit_Return(self, node: ast.Return) -> str:
        if node.value is None:
            return f"{self.indent()}return;"
        val = self.visit(node.value)
        return f"{self.indent()}return {val};"

    def visit_Assign(self, node: ast.Assign) -> str:
        if len(node.targets) == 1 and isinstance(node.targets[0], (ast.Tuple, ast.List)):
            if isinstance(node.value, (ast.Tuple, ast.List)) and len(node.targets[0].elts) == len(node.value.elts):
                sub_lines = []
                for t, v in zip(node.targets[0].elts, node.value.elts):
                    sub_lines.append(self.visit_Assign(ast.Assign(targets=[t], value=v)))
                return "\n".join(sub_lines)
        val = self.visit(node.value)
        if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            var_name = node.targets[0].id
            if var_name not in self.declared_vars:
                self.declared_vars.add(var_name)
                return f"{self.indent()}auto {var_name} = {val};"
            else:
                return f"{self.indent()}{var_name} = {val};"
        elif len(node.targets) == 1 and isinstance(node.targets[0], ast.Subscript):
            target = self.visit(node.targets[0])
            return f"{self.indent()}{target} = {val};"
        elif len(node.targets) == 1 and isinstance(node.targets[0], (ast.Tuple, ast.List)):
            names = []
            for elt in node.targets[0].elts:
                if isinstance(elt, ast.Name):
                    if elt.id not in self.declared_vars:
                        self.declared_vars.add(elt.id)
                    names.append(elt.id)
            return f"{self.indent()}auto [{', '.join(names)}] = {val};"

        targets = [self.visit(t) for t in node.targets]
        return f"{self.indent()}{' = '.join(targets)} = {val};"

    def visit_AugAssign(self, node: ast.AugAssign) -> str:
        target = self.visit(node.target)
        val = self.visit(node.value)
        op_map = {
            ast.Add: "+=", ast.Sub: "-=", ast.Mult: "*=", ast.Div: "/=",
            ast.FloorDiv: "/=", ast.Mod: "%=",
            ast.BitAnd: "&=", ast.BitOr: "|=", ast.BitXor: "^=",
            ast.LShift: "<<=", ast.RShift: ">>="
        }
        op = op_map.get(type(node.op), "+=")
        return f"{self.indent()}{target} {op} {val};"

    def visit_If(self, node: ast.If) -> str:
        test = self.visit(node.test)
        self.indent_level += 1
        body_lines = [self.visit(s) for s in node.body]
        body = "\n".join(s for s in body_lines if s)
        self.indent_level -= 1

        res = f"{self.indent()}if ({test}) {{\n{body}\n{self.indent()}}}"
        if node.orelse:
            if len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If):
                elif_part = self.visit(node.orelse[0]).lstrip()
                res += f" else {elif_part}"
            else:
                self.indent_level += 1
                else_lines = [self.visit(s) for s in node.orelse]
                else_body = "\n".join(s for s in else_lines if s)
                self.indent_level -= 1
                res += f" else {{\n{else_body}\n{self.indent()}}}"
        return res

    def visit_IfExp(self, node: ast.IfExp) -> str:
        return f"({self.visit(node.test)} ? {self.visit(node.body)} : {self.visit(node.orelse)})"

    def visit_For(self, node: ast.For) -> str:
        iter_node = node.iter
        target_name = node.target.id if isinstance(node.target, ast.Name) else self.visit(node.target)
        if isinstance(node.target, ast.Name):
            self.declared_vars.add(target_name)

        if isinstance(iter_node, ast.Call) and isinstance(iter_node.func, ast.Name) and iter_node.func.id == "range":
            args = iter_node.args
            if len(args) == 1:
                start = "0"
                end = self.visit(args[0])
                cond = f"{target_name} < {end}"
                incr = f"++{target_name}"
            elif len(args) == 2:
                start = self.visit(args[0])
                end = self.visit(args[1])
                cond = f"{target_name} < {end}"
                incr = f"++{target_name}"
            else:
                start = self.visit(args[0])
                end = self.visit(args[1])
                step = self.visit(args[2])
                try:
                    step_val = ast.literal_eval(args[2])
                    if step_val > 0:
                        cond = f"{target_name} < {end}"
                        incr = f"{target_name} += {step}" if step != "1" else f"++{target_name}"
                    else:
                        cond = f"{target_name} > {end}"
                        incr = f"{target_name} += {step}" if step != "-1" else f"--{target_name}"
                except Exception:
                    cond = f"({step} > 0 ? {target_name} < {end} : {target_name} > {end})"
                    incr = f"{target_name} += {step}"

            header = f"for (int {target_name} = {start}; {cond}; {incr})"
        else:
            iter_expr = self.visit(iter_node)
            header = f"for (auto& {target_name} : {iter_expr})"

        self.indent_level += 1
        body_lines = [self.visit(s) for s in node.body]
        body = "\n".join(s for s in body_lines if s)
        self.indent_level -= 1
        return f"{self.indent()}{header} {{\n{body}\n{self.indent()}}}"

    def visit_While(self, node: ast.While) -> str:
        test = self.visit(node.test)
        self.indent_level += 1
        body_lines = [self.visit(s) for s in node.body]
        body = "\n".join(s for s in body_lines if s)
        self.indent_level -= 1
        return f"{self.indent()}while ({test}) {{\n{body}\n{self.indent()}}}"

    def visit_Expr(self, node: ast.Expr) -> str:
        val = self.visit(node.value)
        return f"{self.indent()}{val};"

    def visit_Break(self, node: ast.Break) -> str:
        return f"{self.indent()}break;"

    def visit_Continue(self, node: ast.Continue) -> str:
        return f"{self.indent()}continue;"

    def visit_Pass(self, node: ast.Pass) -> str:
        return f"{self.indent()}/* pass */;"

    def visit_Import(self, node: ast.Import) -> str:
        return ""

    def visit_ImportFrom(self, node: ast.ImportFrom) -> str:
        return ""

    def visit_Constant(self, node: ast.Constant) -> str:
        val = node.value
        if val is None:
            return "nullptr"
        if isinstance(val, bool):
            return "true" if val else "false"
        if isinstance(val, str):
            return f"string({json.dumps(val)})"
        return str(val)

    def visit_Name(self, node: ast.Name) -> str:
        mapping = {"True": "true", "False": "false", "None": "nullptr"}
        return mapping.get(node.id, node.id)

    def visit_List(self, node: ast.List) -> str:
        elts = [self.visit(e) for e in node.elts]
        return f"{{{', '.join(elts)}}}"

    def visit_Tuple(self, node: ast.Tuple) -> str:
        elts = [self.visit(e) for e in node.elts]
        return f"{{{', '.join(elts)}}}"

    def visit_BinOp(self, node: ast.BinOp) -> str:
        left = self.visit(node.left)
        right = self.visit(node.right)
        if isinstance(node.op, ast.Pow):
            return f"pow({left}, {right})"
        if isinstance(node.op, ast.FloorDiv):
            return f"({left} / {right})"
        op_map = {
            ast.Add: "+", ast.Sub: "-", ast.Mult: "*", ast.Div: "/",
            ast.Mod: "%", ast.BitAnd: "&", ast.BitOr: "|", ast.BitXor: "^",
            ast.LShift: "<<", ast.RShift: ">>"
        }
        op = op_map.get(type(node.op), "+")
        if isinstance(node.op, ast.Mult):
            if isinstance(node.left, ast.List) and len(node.left.elts) == 1:
                elem = self.visit(node.left.elts[0])
                return f"vector<int>({right}, {elem})"
            if isinstance(node.right, ast.List) and len(node.right.elts) == 1:
                elem = self.visit(node.right.elts[0])
                return f"vector<int>({left}, {elem})"
        return f"({left} {op} {right})"

    def visit_UnaryOp(self, node: ast.UnaryOp) -> str:
        operand = self.visit(node.operand)
        if isinstance(node.op, ast.Not):
            return f"(!{operand})"
        if isinstance(node.op, ast.USub):
            return f"(-{operand})"
        if isinstance(node.op, ast.UAdd):
            return f"(+{operand})"
        if isinstance(node.op, ast.Invert):
            return f"(~{operand})"
        return operand

    def visit_BoolOp(self, node: ast.BoolOp) -> str:
        op = " && " if isinstance(node.op, ast.And) else " || "
        values = [f"({self.visit(v)})" for v in node.values]
        return f"({op.join(values)})"

    def visit_Compare(self, node: ast.Compare) -> str:
        left = self.visit(node.left)
        parts = []
        curr = left
        for op_node, comp_node in zip(node.ops, node.comparators):
            comp = self.visit(comp_node)
            if isinstance(op_node, ast.Eq):
                parts.append(f"{curr} == {comp}")
            elif isinstance(op_node, ast.NotEq):
                parts.append(f"{curr} != {comp}")
            elif isinstance(op_node, ast.Lt):
                parts.append(f"{curr} < {comp}")
            elif isinstance(op_node, ast.LtE):
                parts.append(f"{curr} <= {comp}")
            elif isinstance(op_node, ast.Gt):
                parts.append(f"{curr} > {comp}")
            elif isinstance(op_node, ast.GtE):
                parts.append(f"{curr} >= {comp}")
            elif isinstance(op_node, ast.In):
                parts.append(f"(_in({curr}, {comp}))")
            elif isinstance(op_node, ast.NotIn):
                parts.append(f"(!_in({curr}, {comp}))")
            curr = comp
        return " && ".join(parts) if len(parts) > 1 else parts[0]

    def visit_Subscript(self, node: ast.Subscript) -> str:
        val = self.visit(node.value)
        if isinstance(node.slice, ast.Slice):
            lower = self.visit(node.slice.lower) if node.slice.lower else "0"
            upper = self.visit(node.slice.upper) if node.slice.upper else f"{val}.size()"
            step = self.visit(node.slice.step) if node.slice.step else None
            if step == "-1":
                return f"_reverse({val})"
            return f"{val}.substr({lower}, {upper} - ({lower}))"

        if isinstance(node.slice, ast.UnaryOp) and isinstance(node.slice.op, ast.USub) and isinstance(node.slice.operand, ast.Constant) and isinstance(node.slice.operand.value, int):
            idx = node.slice.operand.value
            return f"{val}[{val}.size() - {idx}]"

        idx = self.visit(node.slice)
        return f"{val}[{idx}]"

    def visit_Attribute(self, node: ast.Attribute) -> str:
        val = self.visit(node.value)
        attr = node.attr
        if val in ("math", "np"):
            if attr in ("sqrt", "floor", "ceil", "abs", "sin", "cos", "tan", "log", "exp", "pow"):
                return f"std::{attr}"
            if attr == "pi":
                return "M_PI"
            if attr == "gcd":
                return "_gcd"
        return f"{val}.{attr}"

    def visit_Call(self, node: ast.Call) -> str:
        func = self.visit(node.func)
        args = [self.visit(a) for a in node.args]

        if func == "len":
            return f"len({args[0]})"
        if func == "min":
            if len(args) == 1:
                return f"(*min_element({args[0]}.begin(), {args[0]}.end()))"
            if len(args) == 2:
                return f"min({args[0]}, {args[1]})"
            return f"min({{{', '.join(args)}}})"
        if func == "max":
            if len(args) == 1:
                return f"(*max_element({args[0]}.begin(), {args[0]}.end()))"
            if len(args) == 2:
                return f"max({args[0]}, {args[1]})"
            return f"max({{{', '.join(args)}}})"
        if func == "abs":
            return f"abs({args[0]})"
        if func == "sum":
            return f"sum({args[0]})"
        if func == "sorted":
            return f"_sorted({args[0]})"
        if func == "str":
            return f"to_string({args[0]})"
        if func == "int":
            return f"static_cast<int>({args[0]})"
        if func == "float":
            return f"static_cast<double>({args[0]})"
        if func == "pow":
            return f"pow({args[0]}, {args[1]})"
        if func == "round":
            return f"round({args[0]})"
        if func.endswith(".append"):
            base = func[:-7]
            return f"{base}.push_back({args[0]})"
        if func.endswith(".pop"):
            base = func[:-4]
            return f"{base}.pop_back()"
        if func.endswith(".sort"):
            base = func[:-5]
            return f"sort({base}.begin(), {base}.end())"

        return f"{func}({', '.join(args)})"

    def visit_ListComp(self, node: ast.ListComp) -> str:
        elt = self.visit(node.elt)
        gen = node.generators[0]
        iter_expr = self.visit(gen.iter)
        target = gen.target.id if isinstance(gen.target, ast.Name) else "x"
        return f"/* comp */"

def transpile_py_to_cpp(py_code: str, ret_type: str, param_types: Dict[str, str]) -> str:
    tree = ast.parse(py_code)
    visitor = PyToCppVisitor(ret_type, param_types)
    funcs = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
    if not funcs:
        raise ValueError("No FunctionDef found in Python code")

    helper_code = []
    for f in funcs[:-1]:
        h_vis = PyToCppVisitor("auto", {a.arg: "auto" for a in f.args.args})
        helper_code.append(h_vis.visit(f))

    main_fn = funcs[-1]
    main_code = visitor.visit(main_fn)

    helpers_str = "\n".join(helper_code)
    if helpers_str:
        helpers_str += "\n"

    return f"""{CPP_HEADER}

class Solution {{
public:
{helpers_str}{main_code}
}};
"""
