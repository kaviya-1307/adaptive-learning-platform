import ast
import json
import re
from typing import List, Dict, Any, Optional

def infer_java_type(val: Any) -> str:
    if isinstance(val, bool):
        return "boolean"
    if isinstance(val, int):
        return "int"
    if isinstance(val, float):
        return "double"
    if isinstance(val, str):
        return "String"
    if isinstance(val, list):
        if not val:
            return "int[]"
        inner = infer_java_type(val[0])
        return f"{inner}[]"
    if isinstance(val, dict):
        return "Map<String, Object>"
    return "Object"

JAVA_HELPERS = """
    private static long _gcd(long a, long b) {
        a = Math.abs(a); b = Math.abs(b);
        while (b != 0) { long t = b; b = a % b; a = t; }
        return a;
    }
    private static int _gcd(int a, int b) {
        return (int) _gcd((long) a, (long) b);
    }
    private static boolean _in(int val, int[] arr) {
        for (int x : arr) if (x == val) return true;
        return false;
    }
    private static boolean _in(String val, String[] arr) {
        for (String x : arr) if (Objects.equals(x, val)) return true;
        return false;
    }
    private static boolean _in(char ch, String s) {
        return s.indexOf(ch) != -1;
    }
    private static boolean _in(String sub, String s) {
        return s.contains(sub);
    }
    private static <T> boolean _in(T val, Collection<T> col) {
        return col.contains(val);
    }
    private static int len(int[] a) { return a.length; }
    private static int len(String[] a) { return a.length; }
    private static int len(double[] a) { return a.length; }
    private static int len(boolean[] a) { return a.length; }
    private static int len(int[][] a) { return a.length; }
    private static int len(String s) { return s.length(); }
    private static int len(Collection<?> c) { return c.size(); }
    private static int len(Map<?, ?> m) { return m.size(); }
    public static int[] _nlargest(int n, int[] nums) {
        int[] copy = nums.clone();
        Arrays.sort(copy);
        int[] res = new int[Math.min(n, copy.length)];
        for (int i = 0; i < res.length; i++) res[i] = copy[copy.length - 1 - i];
        return res;
    }
    public static int[] _nsmallest(int n, int[] nums) {
        int[] copy = nums.clone();
        Arrays.sort(copy);
        int[] res = new int[Math.min(n, copy.length)];
        System.arraycopy(copy, 0, res, 0, res.length);
        return res;
    }
    public static class _HeapQ {
        public int[] nlargest(int n, int[] nums) { return _nlargest(n, nums); }
        public int[] nsmallest(int n, int[] nums) { return _nsmallest(n, nums); }
    }
    public static _HeapQ heapq = new _HeapQ();
    public static _HeapQ hq = heapq;

    public static class _Re {
        public String[] findall(String pat, String text) {
            try {
                Pattern p = Pattern.compile(pat);
                Matcher m = p.matcher(text);
                List<String> list = new ArrayList<>();
                while (m.find()) {
                    if (m.groupCount() > 0) list.add(m.group(1));
                    else list.add(m.group());
                }
                return list.toArray(new String[0]);
            } catch (Exception e) {
                return new String[0];
            }
        }
        public boolean search(String pat, String text) {
            try {
                return Pattern.compile(pat).matcher(text).find();
            } catch (Exception e) {
                return false;
            }
        }
        public String sub(String pat, String repl, String text) {
            try {
                return text.replaceAll(pat, repl);
            } catch (Exception e) {
                return text;
            }
        }
    }
    public static _Re re = new _Re();
"""

class PyToJavaVisitor(ast.NodeVisitor):
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
            ptype = self.param_types.get(a.arg, "Object")
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
        return f"{self.indent()}public {self.ret_type} {fn_name}({', '.join(params)}) {{\n{body_str}\n{self.indent()}}}"

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
                    sub_assign = ast.Assign(targets=[t], value=v)
                    sub_lines.append(self.visit_Assign(sub_assign))
                return "\n".join(sub_lines)
            names = []
            for elt in node.targets[0].elts:
                if isinstance(elt, ast.Name):
                    if elt.id not in self.declared_vars:
                        self.declared_vars.add(elt.id)
                    names.append(elt.id)
            return f"{self.indent()}// tuple unpack {names}"
        val = self.visit(node.value)
        if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            var_name = node.targets[0].id
            if var_name not in self.declared_vars:
                self.declared_vars.add(var_name)
                return f"{self.indent()}var {var_name} = {val};"
            else:
                return f"{self.indent()}{var_name} = {val};"
        elif len(node.targets) == 1 and isinstance(node.targets[0], ast.Subscript):
            target = self.visit(node.targets[0])
            return f"{self.indent()}{target} = {val};"

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
            header = f"for (var {target_name} : {iter_expr})"

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
            return "null"
        if isinstance(val, bool):
            return "true" if val else "false"
        if isinstance(val, str):
            return json.dumps(val)
        return str(val)

    def visit_Name(self, node: ast.Name) -> str:
        mapping = {"True": "true", "False": "false", "None": "null"}
        return mapping.get(node.id, node.id)

    def visit_List(self, node: ast.List) -> str:
        elts = [self.visit(e) for e in node.elts]
        return f"new int[]{{{', '.join(elts)}}}"

    def visit_Tuple(self, node: ast.Tuple) -> str:
        elts = [self.visit(e) for e in node.elts]
        return f"new int[]{{{', '.join(elts)}}}"

    def visit_BinOp(self, node: ast.BinOp) -> str:
        left = self.visit(node.left)
        right = self.visit(node.right)
        if isinstance(node.op, ast.Pow):
            return f"(int) Math.pow({left}, {right})"
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
                return f"new int[{right}]"
            if isinstance(node.right, ast.List) and len(node.right.elts) == 1:
                elem = self.visit(node.right.elts[0])
                return f"new int[{left}]"
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
                parts.append(f"Objects.equals({curr}, {comp})")
            elif isinstance(op_node, ast.NotEq):
                parts.append(f"(!Objects.equals({curr}, {comp}))")
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
            upper = self.visit(node.slice.upper) if node.slice.upper else f"{val}.length()"
            return f"{val}.substring({lower}, {upper})"

        if isinstance(node.slice, ast.UnaryOp) and isinstance(node.slice.op, ast.USub) and isinstance(node.slice.operand, ast.Constant) and isinstance(node.slice.operand.value, int):
            idx = node.slice.operand.value
            return f"{val}[{val}.length - {idx}]"

        idx = self.visit(node.slice)
        return f"{val}[{idx}]"

    def visit_Attribute(self, node: ast.Attribute) -> str:
        val = self.visit(node.value)
        attr = node.attr
        if val in ("math", "np"):
            if attr in ("sqrt", "floor", "ceil", "abs", "sin", "cos", "tan", "log", "exp", "pow"):
                return f"Math.{attr}"
            if attr == "pi":
                return "Math.PI"
            if attr == "gcd":
                return "_gcd"
        return f"{val}.{attr}"

    def visit_Call(self, node: ast.Call) -> str:
        func = self.visit(node.func)
        args = [self.visit(a) for a in node.args]

        if func == "len":
            return f"len({args[0]})"
        if func == "min":
            return f"Math.min({', '.join(args)})"
        if func == "max":
            return f"Math.max({', '.join(args)})"
        if func == "abs":
            return f"Math.abs({args[0]})"
        if func == "sum":
            return f"sum({args[0]})"
        if func == "str":
            return f"String.valueOf({args[0]})"
        if func == "int":
            return f"(int) ({args[0]})"
        if func == "float":
            return f"(double) ({args[0]})"
        if func == "pow":
            return f"(int) Math.pow({args[0]}, {args[1]})"
        if func == "set":
            if not args:
                return "new HashSet<>()"
            return f"new HashSet<>()"
        if func == "list":
            if not args:
                return "new ArrayList<>()"
            return f"{args[0]}"
        if func.endswith(".sort"):
            base = func[:-5]
            return f"Arrays.sort({base})"
        if func.endswith(".append"):
            base = func[:-7]
            return f"{base}.add({args[0]})"

        return f"{func}({', '.join(args)})"

def transpile_py_to_java(py_code: str, ret_type: str, param_types: Dict[str, str]) -> str:
    tree = ast.parse(py_code)
    visitor = PyToJavaVisitor(ret_type, param_types)
    funcs = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
    if not funcs:
        raise ValueError("No FunctionDef found in Python code")

    helper_code = []
    for f in funcs[:-1]:
        h_vis = PyToJavaVisitor("int", {a.arg: "int" for a in f.args.args})
        h_c = h_vis.visit(f)
        h_c = h_c.replace("public int ", "private static int ")
        helper_code.append(h_c)

    main_fn = funcs[-1]
    main_code = visitor.visit(main_fn)

    helpers_str = "\n".join(helper_code)
    if helpers_str:
        helpers_str += "\n"

    return f"""import java.io.*;
import java.util.*;
import java.util.regex.*;
import java.util.stream.*;

public class Solution {{
{JAVA_HELPERS}
{helpers_str}{main_code}
}}
"""
