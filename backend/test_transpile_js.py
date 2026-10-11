import ast
import json
import re
from typing import List, Dict, Any, Optional
from app.core.database import SessionLocal
from app.models.problem import Problem
from app.engine.code_runner import JavaScriptCodeRunner, extract_target_function_name

PREAMBLE_JS = """
function _in(elem, container) {
    if (container == null) return false;
    if (typeof container === 'string' || Array.isArray(container)) return container.indexOf(elem) !== -1;
    if (container instanceof Set || container instanceof Map) return container.has(elem);
    if (typeof container === 'object') return elem in container;
    return false;
}
function _reverse(val) {
    if (val == null) return val;
    if (typeof val === 'string') return val.split('').reverse().join('');
    return [...val].reverse();
}
function _sorted(arr, key=null, reverse=false) {
    if (arr == null) return [];
    const copy = Array.from(arr);
    copy.sort((a, b) => {
        let ka = key ? key(a) : a;
        let kb = key ? key(b) : b;
        let res = 0;
        if (typeof ka === 'number' && typeof kb === 'number') res = ka - kb;
        else res = String(ka).localeCompare(String(kb));
        return reverse ? -res : res;
    });
    return copy;
}
function _gcd(a, b) {
    a = Math.abs(a); b = Math.abs(b);
    while (b) { let t = b; b = a % b; a = t; }
    return a;
}
function _eq(a, b) {
    if (a === b) return true;
    if (a == null || b == null) return false;
    if (Array.isArray(a) && Array.isArray(b)) {
        if (a.length !== b.length) return false;
        for (let i = 0; i < a.length; i++) if (!_eq(a[i], b[i])) return false;
        return true;
    }
    if (typeof a === 'object' && typeof b === 'object') {
        const ka = Object.keys(a), kb = Object.keys(b);
        if (ka.length !== kb.length) return false;
        for (let k of ka) if (!_eq(a[k], b[k])) return false;
        return true;
    }
    return false;
}
function range(start, stop, step) {
    if (stop === undefined) { stop = start; start = 0; }
    if (step === undefined) step = 1;
    const res = [];
    if (step > 0) {
        for (let i = start; i < stop; i += step) res.push(i);
    } else if (step < 0) {
        for (let i = start; i > stop; i += step) res.push(i);
    }
    return res;
}
function ord(c) { return typeof c === 'string' ? c.charCodeAt(0) : c; }
function chr(c) { return String.fromCharCode(c); }
function len(c) {
    if (c == null) return 0;
    if (c.length !== undefined) return c.length;
    if (c.size !== undefined) return c.size;
    if (typeof c === 'object') return Object.keys(c).length;
    return 0;
}
function sum(arr, start=0) {
    if (!arr) return start;
    return Array.from(arr).reduce((a, b) => a + b, start);
}
function any(arr) {
    if (!arr) return false;
    return Array.from(arr).some(Boolean);
}
function all(arr) {
    if (!arr) return true;
    return Array.from(arr).every(Boolean);
}
function reversed(arr) {
    if (!arr) return [];
    if (typeof arr === 'string') return arr.split('').reverse().join('');
    return [...arr].reverse();
}
function zip(...arrays) {
    if (!arrays.length) return [];
    const minLen = Math.min(...arrays.map(a => (a ? a.length : 0)));
    return Array.from({length: minLen}, (_, i) => arrays.map(a => a[i]));
}
function enumerate(arr, start=0) {
    if (!arr) return [];
    return Array.from(arr).map((x, i) => [i + start, x]);
}
function dict(iterable) {
    if (!iterable) return {};
    if (Array.isArray(iterable)) {
        const obj = {};
        for (const item of iterable) {
            if (Array.isArray(item) && item.length >= 2) obj[item[0]] = item[1];
        }
        return obj;
    }
    return Object.assign({}, iterable);
}
function isinstance(obj, typeName) {
    if (typeName === 'int' || typeName === Number) return Number.isInteger(obj);
    if (typeName === 'float') return typeof obj === 'number';
    if (typeName === 'str' || typeName === String) return typeof obj === 'string';
    if (typeName === 'list' || typeName === Array) return Array.isArray(obj);
    if (typeName === 'dict' || typeName === Object) return typeof obj === 'object' && !Array.isArray(obj);
    return false;
}
function type(obj) {
    if (Array.isArray(obj)) return 'list';
    if (obj === null) return 'NoneType';
    if (typeof obj === 'number') return Number.isInteger(obj) ? 'int' : 'float';
    return typeof obj;
}

const sys = { maxsize: 2147483647 };

const heapq = {
    nlargest: (n, arr, key) => {
        const copy = [...arr];
        if (key) copy.sort((a, b) => key(b) - key(a));
        else copy.sort((a, b) => b - a);
        return copy.slice(0, n);
    },
    nsmallest: (n, arr, key) => {
        const copy = [...arr];
        if (key) copy.sort((a, b) => key(a) - key(b));
        else copy.sort((a, b) => a - b);
        return copy.slice(0, n);
    },
    heappush: (arr, x) => { arr.push(x); arr.sort((a, b) => a - b); },
    heappop: (arr) => arr.shift(),
    heapify: (arr) => { arr.sort((a, b) => a - b); },
    heapreplace: (arr, x) => { const ret = arr.shift(); arr.push(x); arr.sort((a, b) => a - b); return ret; }
};
const hq = heapq;

const re = {
    compile: (pat, flags='') => {
        const regex = new RegExp(pat, flags.includes('i') ? 'i' : '');
        return {
            search: (s) => re.search(pat, s),
            match: (s) => re.match(pat, s),
            findall: (s) => re.findall(pat, s),
            split: (s) => s.split(new RegExp(pat)),
            sub: (repl, s) => s.replace(new RegExp(pat, 'g'), repl)
        };
    },
    findall: (pat, str) => {
        const r = new RegExp(pat, 'g');
        const matches = [];
        let m;
        while ((m = r.exec(str)) !== null) {
            matches.push(m[1] !== undefined ? m[1] : m[0]);
        }
        return matches;
    },
    finditer: (pat, str) => {
        const r = new RegExp(pat, 'g');
        const matches = [];
        let m;
        while ((m = r.exec(str)) !== null) {
            matches.push({ group: (i=0) => (i===0 ? m[0] : m[i]), start: () => m.index, end: () => m.index + m[0].length });
        }
        return matches;
    },
    search: (pat, str) => {
        const m = str.match(new RegExp(pat));
        return m ? { group: (i=0) => (i===0 ? m[0] : m[i]), start: () => m.index, end: () => m.index + m[0].length } : null;
    },
    match: (pat, str) => {
        const m = str.match(new RegExp('^' + pat));
        return m ? { group: (i=0) => (i===0 ? m[0] : m[i]), start: () => m.index, end: () => m.index + m[0].length } : null;
    },
    split: (pat, str) => str.split(new RegExp(pat)),
    sub: (pat, repl, str) => str.replace(new RegExp(pat, 'g'), repl)
};

const math = {
    sqrt: Math.sqrt, floor: Math.floor, ceil: Math.ceil, abs: Math.abs,
    pow: Math.pow, sin: Math.sin, cos: Math.cos, tan: Math.tan,
    log: Math.log, log10: Math.log10, log2: Math.log2, exp: Math.exp,
    pi: Math.PI, e: Math.E, gcd: _gcd,
    factorial: (n) => { let r = 1; for (let i = 2; i <= n; i++) r *= i; return r; },
    comb: (n, k) => {
        if (k < 0 || k > n) return 0;
        if (k === 0 || k === n) return 1;
        let c = 1;
        for (let i = 1; i <= k; i++) c = c * (n - (k - i)) / i;
        return Math.round(c);
    }
};

class _Counter extends Object {
    constructor(iterable) {
        super();
        if (iterable) {
            for (const x of iterable) this[x] = (this[x] || 0) + 1;
        }
    }
    items() {
        return Object.entries(this).filter(([k]) => typeof this[k] !== 'function');
    }
    keys() {
        return Object.keys(this).filter(k => typeof this[k] !== 'function');
    }
    values() {
        return Object.values(this).filter(v => typeof v !== 'function');
    }
    most_common(n) {
        const ent = this.items();
        ent.sort((a, b) => b[1] - a[1]);
        return n !== undefined ? ent.slice(0, n) : ent;
    }
}

const collections = {
    Counter: function(iterable) { return new _Counter(iterable); },
    defaultdict: function(factory) {
        const map = new Map();
        return new Proxy({}, {
            get: (target, prop) => {
                if (prop === 'items') return () => Array.from(map.entries());
                if (prop === 'keys') return () => Array.from(map.keys());
                if (prop === 'values') return () => Array.from(map.values());
                if (!map.has(prop)) map.set(prop, typeof factory === 'function' ? factory() : 0);
                return map.get(prop);
            },
            set: (target, prop, val) => {
                map.set(prop, val);
                return true;
            }
        });
    }
};
const Counter = collections.Counter;
const defaultdict = collections.defaultdict;

const itertools = {
    permutations: function*(arr, r) {
        const a = Array.from(arr);
        r = r === undefined ? a.length : r;
        function* perm(n, current, used) {
            if (current.length === r) { yield current; return; }
            for (let i = 0; i < n; i++) {
                if (!used[i]) {
                    used[i] = true;
                    yield* perm(n, current.concat([a[i]]), used);
                    used[i] = false;
                }
            }
        }
        yield* perm(a.length, [], []);
    },
    combinations: function*(arr, r) {
        const a = Array.from(arr);
        function* comb(start, current) {
            if (current.length === r) { yield current; return; }
            for (let i = start; i < a.length; i++) {
                yield* comb(i + 1, current.concat([a[i]]));
            }
        }
        yield* comb(0, []);
    },
    groupby: function*(iterable, keyFn=(x=>x)) {
        let prevKey = undefined;
        let group = [];
        for (const item of iterable) {
            const k = keyFn(item);
            if (prevKey !== undefined && k !== prevKey) {
                yield [prevKey, group];
                group = [];
            }
            prevKey = k;
            group.push(item);
        }
        if (group.length) yield [prevKey, group];
    }
};
const groupby = itertools.groupby;
"""

class PyToJsVisitor(ast.NodeVisitor):
    def __init__(self):
        self.declared_vars = set()
        self.indent_level = 0
        self.is_inside_fn = False

    def indent(self):
        return "    " * self.indent_level

    def visit_Module(self, node):
        body = []
        for stmt in node.body:
            code = self.visit(stmt)
            if code is not None and code != "":
                body.append(code)
        return "\n".join(body)

    def visit_FunctionDef(self, node):
        fn_name = node.name
        params = [arg.arg for arg in node.args.args]
        old_declared = set(self.declared_vars)
        self.declared_vars = set(params)
        self.indent_level += 1
        self.is_inside_fn = True

        body_lines = []
        for stmt in node.body:
            c = self.visit(stmt)
            if c is not None and c != "":
                body_lines.append(c)

        self.indent_level -= 1
        self.is_inside_fn = False
        self.declared_vars = old_declared
        body_str = "\n".join(body_lines)
        return f"{self.indent()}function {fn_name}({', '.join(params)}) {{\n{body_str}\n{self.indent()}}}"

    def visit_Return(self, node):
        if node.value is None:
            return f"{self.indent()}return;"
        val = self.visit(node.value)
        return f"{self.indent()}return {val};"

    def visit_Assign(self, node):
        val = self.visit(node.value)
        if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            var_name = node.targets[0].id
            if var_name not in self.declared_vars:
                self.declared_vars.add(var_name)
                return f"{self.indent()}let {var_name} = {val};"
            else:
                return f"{self.indent()}{var_name} = {val};"
        elif len(node.targets) == 1 and isinstance(node.targets[0], (ast.Tuple, ast.List)):
            names = []
            for elt in node.targets[0].elts:
                if isinstance(elt, ast.Name):
                    if elt.id not in self.declared_vars:
                        self.declared_vars.add(elt.id)
                    names.append(elt.id)
                else:
                    names.append(self.visit(elt))
            return f"{self.indent()}let [{', '.join(names)}] = {val};"
        elif len(node.targets) == 1 and isinstance(node.targets[0], ast.Subscript):
            target = self.visit(node.targets[0])
            return f"{self.indent()}{target} = {val};"

        targets = [self.visit(t) for t in node.targets]
        return f"{self.indent()}{' = '.join(targets)} = {val};"

    def visit_AugAssign(self, node):
        target = self.visit(node.target)
        val = self.visit(node.value)
        op_map = {
            ast.Add: "+=", ast.Sub: "-=", ast.Mult: "*=", ast.Div: "/=",
            ast.FloorDiv: "/=", ast.Mod: "%=", ast.Pow: "**=",
            ast.BitAnd: "&=", ast.BitOr: "|=", ast.BitXor: "^=",
            ast.LShift: "<<=", ast.RShift: ">>="
        }
        op = op_map.get(type(node.op), "+=")
        if isinstance(node.op, ast.FloorDiv):
            return f"{self.indent()}{target} = Math.floor({target} / {val});"
        return f"{self.indent()}{target} {op} {val};"

    def visit_If(self, node):
        test = self.visit(node.test)
        self.indent_level += 1
        body_lines = [self.visit(s) for s in node.body]
        body = "\n".join(s for s in body_lines if s is not None and s != "")
        self.indent_level -= 1

        res = f"{self.indent()}if ({test}) {{\n{body}\n{self.indent()}}}"
        if node.orelse:
            if len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If):
                elif_part = self.visit(node.orelse[0]).lstrip()
                res += f" else {elif_part}"
            else:
                self.indent_level += 1
                else_lines = [self.visit(s) for s in node.orelse]
                else_body = "\n".join(s for s in else_lines if s is not None and s != "")
                self.indent_level -= 1
                res += f" else {{\n{else_body}\n{self.indent()}}}"
        return res

    def visit_IfExp(self, node):
        return f"({self.visit(node.test)} ? {self.visit(node.body)} : {self.visit(node.orelse)})"

    def visit_For(self, node):
        iter_node = node.iter
        if isinstance(node.target, ast.Name):
            target_name = node.target.id
            if target_name not in self.declared_vars:
                self.declared_vars.add(target_name)
                t_decl = f"let {target_name}"
            else:
                t_decl = target_name
        elif isinstance(node.target, (ast.Tuple, ast.List)):
            names = []
            for e in node.target.elts:
                n = e.id if isinstance(e, ast.Name) else self.visit(e)
                names.append(n)
                self.declared_vars.add(n)
            t_decl = f"let [{', '.join(names)}]"
        else:
            t_decl = self.visit(node.target)

        if isinstance(iter_node, ast.Call) and isinstance(iter_node.func, ast.Name) and iter_node.func.id == "range":
            args = iter_node.args
            raw_tname = node.target.id if isinstance(node.target, ast.Name) else "i"
            if len(args) == 1:
                start = "0"
                end = self.visit(args[0])
                cond = f"{raw_tname} < {end}"
                incr = f"{raw_tname}++"
            elif len(args) == 2:
                start = self.visit(args[0])
                end = self.visit(args[1])
                cond = f"{raw_tname} < {end}"
                incr = f"{raw_tname}++"
            else:
                start = self.visit(args[0])
                end = self.visit(args[1])
                step = self.visit(args[2])
                try:
                    step_val = ast.literal_eval(args[2])
                    if step_val > 0:
                        cond = f"{raw_tname} < {end}"
                        incr = f"{raw_tname} += {step}" if step != "1" else f"{raw_tname}++"
                    else:
                        cond = f"{raw_tname} > {end}"
                        incr = f"{raw_tname} += {step}" if step != "-1" else f"{raw_tname}--"
                except Exception:
                    cond = f"({step} > 0 ? {raw_tname} < {end} : {raw_tname} > {end})"
                    incr = f"{raw_tname} += {step}"

            header = f"for ({t_decl} = {start}; {cond}; {incr})"
        else:
            iter_expr = self.visit(iter_node)
            header = f"for ({t_decl} of {iter_expr})"

        self.indent_level += 1
        body_lines = [self.visit(s) for s in node.body]
        body = "\n".join(s for s in body_lines if s is not None and s != "")
        self.indent_level -= 1
        return f"{self.indent()}{header} {{\n{body}\n{self.indent()}}}"

    def visit_While(self, node):
        test = self.visit(node.test)
        self.indent_level += 1
        body_lines = [self.visit(s) for s in node.body]
        body = "\n".join(s for s in body_lines if s is not None and s != "")
        self.indent_level -= 1
        return f"{self.indent()}while ({test}) {{\n{body}\n{self.indent()}}}"

    def visit_Expr(self, node):
        val = self.visit(node.value)
        return f"{self.indent()}{val};"

    def visit_Pass(self, node):
        return f"{self.indent()}/* pass */;"

    def visit_Break(self, node):
        return f"{self.indent()}break;"

    def visit_Continue(self, node):
        return f"{self.indent()}continue;"

    def visit_Import(self, node):
        return ""

    def visit_ImportFrom(self, node):
        return ""

    def visit_Lambda(self, node):
        params = [a.arg for a in node.args.args]
        body = self.visit(node.body)
        return f"(({', '.join(params)}) => {body})"

    def visit_Constant(self, node):
        val = node.value
        if val is None:
            return "null"
        if isinstance(val, bool):
            return "true" if val else "false"
        if isinstance(val, str):
            return json.dumps(val)
        return str(val)

    def visit_Name(self, node):
        if node.id in self.declared_vars:
            return node.id
        mapping = {
            "True": "true", "False": "false", "None": "null",
            "float": "Number", "int": "parseInt", "str": "String"
        }
        return mapping.get(node.id, node.id)

    def visit_List(self, node):
        elts = [self.visit(e) for e in node.elts]
        return f"[{', '.join(elts)}]"

    def visit_Tuple(self, node):
        elts = [self.visit(e) for e in node.elts]
        return f"[{', '.join(elts)}]"

    def visit_Dict(self, node):
        pairs = []
        for k, v in zip(node.keys, node.values):
            k_str = self.visit(k)
            v_str = self.visit(v)
            pairs.append(f"[{k_str}]: {v_str}")
        return f"{{{', '.join(pairs)}}}"

    def visit_Set(self, node):
        elts = [self.visit(e) for e in node.elts]
        return f"new Set([{', '.join(elts)}])"

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if isinstance(node.op, ast.FloorDiv):
            return f"Math.floor({left} / {right})"
        if isinstance(node.op, ast.Pow):
            return f"Math.pow({left}, {right})"
        op_map = {
            ast.Add: "+", ast.Sub: "-", ast.Mult: "*", ast.Div: "/",
            ast.Mod: "%", ast.BitAnd: "&", ast.BitOr: "|", ast.BitXor: "^",
            ast.LShift: "<<", ast.RShift: ">>"
        }
        op = op_map.get(type(node.op), "+")
        if isinstance(node.op, ast.Mult):
            if isinstance(node.left, ast.List) and len(node.left.elts) == 1:
                elem = self.visit(node.left.elts[0])
                return f"new Array({right}).fill({elem})"
            if isinstance(node.right, ast.List) and len(node.right.elts) == 1:
                elem = self.visit(node.right.elts[0])
                return f"new Array({left}).fill({elem})"
            if isinstance(node.left, ast.Constant) and isinstance(node.left.value, str):
                return f"{left}.repeat({right})"
        return f"({left} {op} {right})"

    def visit_UnaryOp(self, node):
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

    def visit_BoolOp(self, node):
        op = " && " if isinstance(node.op, ast.And) else " || "
        values = [f"({self.visit(v)})" for v in node.values]
        return f"({op.join(values)})"

    def visit_Compare(self, node):
        left = self.visit(node.left)
        parts = []
        curr = left
        for op_node, comp_node in zip(node.ops, node.comparators):
            comp = self.visit(comp_node)
            if isinstance(op_node, (ast.Eq, ast.Is)):
                parts.append(f"_eq({curr}, {comp})")
            elif isinstance(op_node, (ast.NotEq, ast.IsNot)):
                parts.append(f"(!_eq({curr}, {comp}))")
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

    def visit_Subscript(self, node):
        val = self.visit(node.value)
        if isinstance(node.slice, ast.Slice):
            lower = self.visit(node.slice.lower) if node.slice.lower else "0"
            upper = self.visit(node.slice.upper) if node.slice.upper else f"{val}.length"
            step = self.visit(node.slice.step) if node.slice.step else None
            if step == "-1":
                return f"(_reverse({val}))"
            return f"{val}.slice({lower}, {upper})"

        if isinstance(node.slice, ast.UnaryOp) and isinstance(node.slice.op, ast.USub) and isinstance(node.slice.operand, ast.Constant) and isinstance(node.slice.operand.value, int):
            idx = node.slice.operand.value
            return f"{val}[{val}.length - {idx}]"

        idx = self.visit(node.slice)
        return f"{val}[{idx}]"

    def visit_Attribute(self, node):
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

    def visit_Call(self, node):
        func = self.visit(node.func)
        args = [self.visit(a) for a in node.args]

        if not func:
            return ""

        if func == "len":
            return f"len({args[0]})"
        if func == "min":
            if len(args) == 1:
                return f"Math.min(...{args[0]})"
            return f"Math.min({', '.join(args)})"
        if func == "max":
            if len(args) == 1:
                return f"Math.max(...{args[0]})"
            return f"Math.max({', '.join(args)})"
        if func == "abs":
            return f"Math.abs({args[0]})"
        if func == "sum":
            if len(args) == 1:
                return f"sum({args[0]})"
            return f"sum({args[0]}, {args[1]})"
        if func == "sorted":
            kw_key = "null"
            kw_rev = "false"
            for kw in node.keywords:
                if kw.arg == "key":
                    kw_key = self.visit(kw.value)
                elif kw.arg == "reverse":
                    kw_rev = self.visit(kw.value)
            return f"_sorted({args[0]}, {kw_key}, {kw_rev})"
        if func == "set":
            return f"new Set({args[0] if args else ''})"
        if func == "list":
            return f"Array.from({args[0] if args else ''})"
        if func == "str":
            return f"String({args[0]})"
        if func == "int":
            return f"Math.floor(Number({args[0]}))"
        if func == "float":
            return f"Number({args[0]})"
        if func == "pow":
            return f"Math.pow({args[0]}, {args[1]})"
        if func == "round":
            return f"Math.round({args[0]})"
        if func == "map":
            return f"Array.from({args[1]}).map({args[0]})"
        if func == "filter":
            return f"Array.from({args[1]}).filter({args[0]})"
        if func == "zip":
            return f"zip({', '.join(args)})"
        if func == "enumerate":
            return f"enumerate({', '.join(args)})"
        if func == "any":
            return f"any({args[0]})"
        if func == "all":
            return f"all({args[0]})"
        if func == "reversed":
            return f"reversed({args[0]})"
        if func == "isinstance":
            return f"isinstance({args[0]}, {args[1]})"
        if func == "type":
            return f"type({args[0]})"
        if func == "dict":
            return f"dict({args[0] if args else ''})"

        # Method calls
        if func.endswith(".append"):
            base = func[:-7]
            return f"{base}.push({args[0]})"
        if func.endswith(".pop"):
            base = func[:-4]
            return f"{base}.pop()"
        if func.endswith(".remove"):
            base = func[:-7]
            return f"(() => {{ const _i = {base}.indexOf({args[0]}); if (_i !== -1) {base}.splice(_i, 1); }})()"
        if func.endswith(".sort"):
            base = func[:-5]
            return f"{base}.sort((a, b) => (typeof a === 'number' && typeof b === 'number' ? a - b : String(a).localeCompare(String(b))))"
        if func.endswith(".lower"):
            base = func[:-6]
            return f"{base}.toLowerCase()"
        if func.endswith(".upper"):
            base = func[:-6]
            return f"{base}.toUpperCase()"
        if func.endswith(".count"):
            base = func[:-6]
            return f"{base}.filter(x => x === {args[0]}).length"
        if func.endswith(".split"):
            base = func[:-6]
            return f"{base}.split({args[0] if args else ''})"
        if func.endswith(".join"):
            base = func[:-5]
            return f"{args[0]}.join({base})"
        if func.endswith(".strip"):
            base = func[:-6]
            return f"{base}.trim()"
        if func.endswith(".startswith"):
            base = func[:-11]
            return f"{base}.startsWith({args[0]})"
        if func.endswith(".endswith"):
            base = func[:-9]
            return f"{base}.endsWith({args[0]})"
        if func.endswith(".replace"):
            base = func[:-8]
            return f"{base}.replaceAll({args[0]}, {args[1]})"
        if func.endswith(".items"):
            base = func[:-6]
            return f"Object.entries({base})"
        if func.endswith(".keys"):
            base = func[:-5]
            return f"Object.keys({base})"
        if func.endswith(".values"):
            base = func[:-7]
            return f"Object.values({base})"

        return f"{func}({', '.join(args)})"

    def visit_ListComp(self, node):
        elt = self.visit(node.elt)
        gen = node.generators[0]
        iter_expr = self.visit(gen.iter)
        if isinstance(gen.target, (ast.Tuple, ast.List)):
            names = [e.id if isinstance(e, ast.Name) else self.visit(e) for e in gen.target.elts]
            target = f"[{', '.join(names)}]"
        elif isinstance(gen.target, ast.Name):
            target = gen.target.id
        else:
            target = "x"

        if gen.ifs:
            conds = " && ".join(self.visit(c) for c in gen.ifs)
            return f"{iter_expr}.filter({target} => {conds}).map({target} => {elt})"
        return f"{iter_expr}.map({target} => {elt})"

    def visit_GeneratorExp(self, node):
        return self.visit_ListComp(node)

    def visit_Starred(self, node):
        return f"...{self.visit(node.value)}"

def transpile_py_to_js(py_code: str) -> str:
    tree = ast.parse(py_code)
    visitor = PyToJsVisitor()
    body = visitor.visit(tree)
    return PREAMBLE_JS + "\n" + body
