import ast
import json
from app.core.database import SessionLocal
from app.models.problem import Problem
from app.engine.code_runner import extract_target_function_name

def infer_type(val):
    if isinstance(val, bool): return "bool"
    if isinstance(val, int): return "int"
    if isinstance(val, float): return "double"
    if isinstance(val, str): return "str"
    if isinstance(val, list):
        if not val: return "list_int"
        inner = infer_type(val[0])
        return f"list_{inner}"
    return "any"

def java_type(t_name):
    mapping = {
        "bool": "boolean",
        "int": "int",
        "double": "double",
        "str": "String",
        "list_int": "int[]",
        "list_double": "double[]",
        "list_str": "String[]",
        "list_bool": "boolean[]",
        "list_list_int": "int[][]",
        "list_list_str": "String[][]",
    }
    return mapping.get(t_name, "Object")

def cpp_type(t_name):
    mapping = {
        "bool": "bool",
        "int": "int",
        "double": "double",
        "str": "string",
        "list_int": "vector<int>",
        "list_double": "vector<double>",
        "list_str": "vector<string>",
        "list_bool": "vector<bool>",
        "list_list_int": "vector<vector<int>>",
        "list_list_str": "vector<vector<string>>",
    }
    return mapping.get(t_name, "auto")

if __name__ == "__main__":
    db = SessionLocal()
    probs = db.query(Problem).filter(Problem.id.between(41, 50)).all()
    for p in probs:
        tc = p.test_cases[0]
        inp = json.loads(tc.input_data)
        out = json.loads(tc.expected_output)
        fn_name = extract_target_function_name(p.starter_code_python)
        
        arg_types = [infer_type(v) for v in inp.values()] if isinstance(inp, dict) else [infer_type(inp)]
        ret_type = infer_type(out)
        
        print(f"Problem {p.id} ({p.title[:30]}): fn={fn_name}")
        print(f"  Inputs: {list(inp.keys()) if isinstance(inp, dict) else 'arg'} -> {arg_types} (Java: {[java_type(t) for t in arg_types]})")
        print(f"  Return: {ret_type} (Java: {java_type(ret_type)}, C++: {cpp_type(ret_type)})")
        print("  Python Code:")
        for line in p.reference_solution_python.strip().split("\n")[:4]:
            print(f"    {line}")
        print()
    db.close()
