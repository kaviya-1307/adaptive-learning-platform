"""
Multi-Language Code Execution Engine for LeetCode Adaptive Learning Platform.
Safely executes user-submitted Python, Java, C++, and JavaScript solutions against test cases,
enforces timeouts, intercepts stdout/stderr, and provides structured evaluation metrics.
"""
import ast
import json
import logging
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT_SECONDS = 5.0
DEFAULT_JAVA_COMPILE_TIMEOUT_SECONDS = 30.0
SUPPORTED_LANGUAGES = ["python", "java", "cpp", "javascript"]


def extract_target_function_name(code_str: str, starter_code: Optional[str] = None) -> Optional[str]:
    """Extract entrypoint function name from starter code or user code using AST."""
    if starter_code:
        try:
            tree = ast.parse(starter_code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    return node.name
        except Exception:
            pass

    try:
        tree = ast.parse(code_str)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                return node.name
    except Exception:
        pass

    return None


def extract_js_function_name(code_str: str, starter_code: Optional[str] = None) -> Optional[str]:
    """Extract JavaScript function name from starter or user code."""
    for text in (starter_code, code_str):
        if not text:
            continue
        m = re.search(r"function\s+([a-zA-Z0-9_$]+)\s*\(", text)
        if m:
            return m.group(1)
        m = re.search(r"(?:var|let|const)\s+([a-zA-Z0-9_$]+)\s*=\s*function", text)
        if m:
            return m.group(1)
    return None


def _split_param_list(params_str: str) -> List[str]:
    parts = []
    current = []
    depth = 0
    for char in params_str:
        if char in ('<', '('):
            depth += 1
        elif char in ('>', ')'):
            depth -= 1
        elif char == ',' and depth == 0:
            parts.append(''.join(current).strip())
            current = []
            continue
        current.append(char)
    if current:
        parts.append(''.join(current).strip())
    return parts


def extract_java_method_name(code_str: str, starter_code: Optional[str] = None) -> Optional[str]:
    """Extract Java public method name from Solution class."""
    for text in (starter_code, code_str):
        if not text:
            continue
        m = re.search(r"public\s+(?:[A-Za-z0-9_\[\]]+(?:<[^>]+>)?)\s+([a-zA-Z0-9_]+)\s*\(", text)
        if m:
            return m.group(1)
        m = re.search(r"public\s+[A-Za-z0-9_<>\[\]]+\s+([a-zA-Z0-9_]+)\s*\(", text)
        if m:
            return m.group(1)
    return None


def extract_java_param_types(code_str: str, starter_code: Optional[str] = None) -> List[str]:
    """Extract list of Java parameter types for the public method."""
    for text in (starter_code, code_str):
        if not text:
            continue
        m = re.search(r"public\s+(?:[A-Za-z0-9_\[\]]+(?:<[^>]+>)?)\s+[a-zA-Z0-9_]+\s*\(([^)]*)\)", text)
        if not m:
            m = re.search(r"public\s+[A-Za-z0-9_<>\[\]]+\s+[a-zA-Z0-9_]+\s*\(([^)]*)\)", text)
        if m:
            params_str = m.group(1).strip()
            if not params_str:
                return []
            types = []
            for part in _split_param_list(params_str):
                tokens = part.strip().rsplit(maxsplit=1)
                if len(tokens) >= 2:
                    types.append(tokens[0])
                elif tokens:
                    types.append(tokens[0])
            return types
    return []


def extract_cpp_method_name(code_str: str, starter_code: Optional[str] = None) -> Optional[str]:
    """Extract C++ public method name from Solution class."""
    for text in (starter_code, code_str):
        if not text:
            continue
        m = re.search(r"(?:[A-Za-z0-9_:&]+(?:<[^>]+>)?[\s*&]*)\s+([a-zA-Z0-9_]+)\s*\([^{;]*\)\s*\{?", text)
        if m and m.group(1) not in ("main", "if", "for", "while", "switch"):
            return m.group(1)
        m = re.search(r"[A-Za-z0-9_<>:&]+\s+([a-zA-Z0-9_]+)\s*\([^{;]*\)\s*\{?", text)
        if m and m.group(1) not in ("main", "if", "for", "while", "switch"):
            return m.group(1)
    return None


def extract_cpp_param_types(code_str: str, starter_code: Optional[str] = None) -> List[str]:
    """Extract list of C++ parameter types for the public method."""
    for text in (starter_code, code_str):
        if not text:
            continue
        m = re.search(r"(?:[A-Za-z0-9_:&]+(?:<[^>]+>)?[\s*&]*)\s+([a-zA-Z0-9_]+)\s*\(([^)]*)\)", text)
        if not m:
            m = re.search(r"[A-Za-z0-9_<>:&]+\s+([a-zA-Z0-9_]+)\s*\(([^)]*)\)", text)
        if m and m.group(1) not in ("main", "if", "for", "while", "switch"):
            params_str = m.group(2).strip()
            if not params_str:
                return []
            types = []
            for part in _split_param_list(params_str):
                tokens = part.strip().rsplit(maxsplit=1)
                if len(tokens) >= 2:
                    types.append(tokens[0])
                elif tokens:
                    types.append(tokens[0])
            return types
    return []


# =====================================================================
# 1. PYTHON RUNNER (Preserves existing implementation)
# =====================================================================
WORKER_RUNNER_TEMPLATE = r"""
import sys
import io
import json
import time
import ast
import traceback

def run_evaluation():
    input_payload = json.loads(sys.stdin.read())
    code = input_payload["code"]
    fn_name = input_payload["fn_name"]
    test_cases = input_payload["test_cases"]

    try:
        compiled = compile(code, "<solution>", "exec")
    except SyntaxError as e:
        print(json.dumps({
            "status": "Compilation Error",
            "passed_test_cases": 0,
            "total_test_cases": len(test_cases),
            "execution_time_ms": 0.0,
            "compile_error": f"SyntaxError: {e.msg} (line {e.lineno})",
            "results": []
        }))
        return
    except Exception as e:
        print(json.dumps({
            "status": "Compilation Error",
            "passed_test_cases": 0,
            "total_test_cases": len(test_cases),
            "execution_time_ms": 0.0,
            "compile_error": f"CompileError: {str(e)}",
            "results": []
        }))
        return

    scope = {"__name__": "__main__"}
    try:
        exec(compiled, scope)
    except Exception as e:
        print(json.dumps({
            "status": "Runtime Error",
            "passed_test_cases": 0,
            "total_test_cases": len(test_cases),
            "execution_time_ms": 0.0,
            "compile_error": f"Error on load: {traceback.format_exc()}",
            "results": []
        }))
        return

    target_fn = scope.get(fn_name)
    if not target_fn or not callable(target_fn):
        callables = [v for k, v in scope.items() if callable(v) and not k.startswith("_") and k not in ("run_evaluation",)]
        if callables:
            target_fn = callables[-1]
        else:
            print(json.dumps({
                "status": "Runtime Error",
                "passed_test_cases": 0,
                "total_test_cases": len(test_cases),
                "execution_time_ms": 0.0,
                "compile_error": f"Function '{fn_name}' not defined in solution.",
                "results": []
            }))
            return

    results = []
    overall_status = "Accepted"
    total_exec_time = 0.0

    for tc in test_cases:
        tc_id = tc["id"]
        input_data_str = tc["input_data"]
        expected_output_str = tc["expected_output"]
        is_hidden = tc["is_hidden"]

        try:
            kwargs = json.loads(input_data_str)
        except Exception:
            kwargs = {}

        old_stdout = sys.stdout
        redirected_output = io.StringIO()
        sys.stdout = redirected_output

        tc_start = time.perf_counter()
        tc_error = None
        actual_val = None
        tc_status = "Passed"

        try:
            if isinstance(kwargs, dict):
                actual_val = target_fn(**kwargs)
            elif isinstance(kwargs, list):
                actual_val = target_fn(*kwargs)
            else:
                actual_val = target_fn(kwargs)
        except Exception as ex:
            tc_status = "Runtime Error"
            tc_error = traceback.format_exc()
        finally:
            tc_duration_ms = (time.perf_counter() - tc_start) * 1000.0
            total_exec_time += tc_duration_ms
            sys.stdout = old_stdout
            user_stdout = redirected_output.getvalue()
            if len(user_stdout) > 2000:
                user_stdout = user_stdout[:2000] + "\n... [stdout truncated]"

        if tc_status == "Passed":
            try:
                try:
                    exp_parsed = json.loads(expected_output_str)
                except Exception:
                    exp_parsed = expected_output_str.strip()

                is_match = False
                if isinstance(actual_val, bool) and isinstance(exp_parsed, str):
                    is_match = (actual_val == (exp_parsed.lower() in ("true", "1", "yes")))
                elif isinstance(actual_val, (int, float)) and isinstance(exp_parsed, (int, float)):
                    is_match = (abs(actual_val - exp_parsed) < 1e-6)
                elif isinstance(actual_val, list) and isinstance(exp_parsed, list):
                    if actual_val == exp_parsed:
                        is_match = True
                    else:
                        try:
                            a_s = sorted([str(sorted(x)) if isinstance(x, list) else str(x) for x in actual_val])
                            e_s = sorted([str(sorted(x)) if isinstance(x, list) else str(x) for x in exp_parsed])
                            is_match = (a_s == e_s)
                        except Exception:
                            is_match = False
                else:
                    is_match = (actual_val == exp_parsed)

                if not is_match:
                    tc_status = "Wrong Answer"
            except Exception as comp_err:
                tc_status = "Runtime Error"
                tc_error = f"Comparison exception: {str(comp_err)}"

        if tc_status != "Passed" and overall_status == "Accepted":
            overall_status = tc_status

        try:
            actual_str = json.dumps(actual_val)
        except Exception:
            actual_str = str(actual_val)

        results.append({
            "test_case_id": tc_id,
            "status": tc_status,
            "input_data": input_data_str if not is_hidden else "[Hidden Test Case]",
            "expected_output": expected_output_str if not is_hidden else "[Hidden Test Case]",
            "actual_output": actual_str if not is_hidden else ("[Hidden]" if tc_status == "Passed" else actual_str),
            "stdout": user_stdout,
            "execution_time_ms": round(tc_duration_ms, 2),
            "is_hidden": is_hidden,
            "error_message": tc_error
        })

    passed_count = sum(1 for r in results if r["status"] == "Passed")
    if passed_count < len(results) and overall_status == "Accepted":
        overall_status = "Wrong Answer"

    print(json.dumps({
        "status": overall_status,
        "passed_test_cases": passed_count,
        "total_test_cases": len(results),
        "execution_time_ms": round(total_exec_time, 2),
        "compile_error": None,
        "results": results
    }))

if __name__ == "__main__":
    run_evaluation()
"""


class PythonCodeRunner:
    @classmethod
    def execute(
        cls,
        code: str,
        test_cases: List[Dict[str, Any]],
        starter_code: Optional[str] = None,
        timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
        is_submission: bool = False
    ) -> Dict[str, Any]:
        if not code or not code.strip():
            return {
                "status": "Compilation Error",
                "passed_test_cases": 0,
                "total_test_cases": len(test_cases),
                "execution_time_ms": 0.0,
                "compile_error": "Empty code submitted. Please write a solution.",
                "results": []
            }

        active_tcs = test_cases if is_submission else [tc for tc in test_cases if not tc.get("is_hidden", False)]
        if not active_tcs:
            active_tcs = test_cases

        fn_name = extract_target_function_name(code, starter_code) or "solution"

        payload = {
            "code": code,
            "fn_name": fn_name,
            "test_cases": [
                {
                    "id": tc.get("id", idx + 1),
                    "input_data": tc.get("input_data", "{}"),
                    "expected_output": str(tc.get("expected_output", "")),
                    "is_hidden": tc.get("is_hidden", False) and is_submission
                }
                for idx, tc in enumerate(active_tcs)
            ]
        }

        start_time = time.perf_counter()
        try:
            process = subprocess.run(
                [sys.executable, "-c", WORKER_RUNNER_TEMPLATE],
                input=json.dumps(payload),
                capture_output=True,
                text=True,
                timeout=timeout_seconds
            )
            total_elapsed_ms = round((time.perf_counter() - start_time) * 1000.0, 2)

            if process.returncode != 0:
                stderr_text = process.stderr.strip() or "Process terminated with error."
                return {
                    "status": "Runtime Error",
                    "passed_test_cases": 0,
                    "total_test_cases": len(active_tcs),
                    "execution_time_ms": total_elapsed_ms,
                    "compile_error": stderr_text,
                    "results": []
                }

            stdout_text = process.stdout.strip()
            if not stdout_text:
                return {
                    "status": "Runtime Error",
                    "passed_test_cases": 0,
                    "total_test_cases": len(active_tcs),
                    "execution_time_ms": total_elapsed_ms,
                    "compile_error": "No output returned from execution worker.",
                    "results": []
                }

            result_data = json.loads(stdout_text)
            if not result_data.get("execution_time_ms"):
                result_data["execution_time_ms"] = total_elapsed_ms
            return result_data

        except subprocess.TimeoutExpired:
            total_elapsed_ms = round((time.perf_counter() - start_time) * 1000.0, 2)
            logger.warning(f"Python execution timed out after {timeout_seconds}s")
            return {
                "status": "Time Limit Exceeded",
                "passed_test_cases": 0,
                "total_test_cases": len(active_tcs),
                "execution_time_ms": total_elapsed_ms,
                "compile_error": f"Time Limit Exceeded: Execution took longer than {timeout_seconds} seconds.",
                "results": [
                    {
                        "test_case_id": tc.get("id", idx + 1),
                        "status": "Time Limit Exceeded",
                        "input_data": tc.get("input_data", "") if not tc.get("is_hidden", False) else "[Hidden Test Case]",
                        "expected_output": str(tc.get("expected_output", "")) if not tc.get("is_hidden", False) else "[Hidden Test Case]",
                        "actual_output": "Time Limit Exceeded",
                        "stdout": "",
                        "execution_time_ms": round(timeout_seconds * 1000.0, 2),
                        "is_hidden": tc.get("is_hidden", False),
                        "error_message": "Execution timed out."
                    }
                    for idx, tc in enumerate(active_tcs)
                ]
            }
        except Exception as e:
            total_elapsed_ms = round((time.perf_counter() - start_time) * 1000.0, 2)
            return {
                "status": "Runtime Error",
                "passed_test_cases": 0,
                "total_test_cases": len(active_tcs),
                "execution_time_ms": total_elapsed_ms,
                "compile_error": f"Execution runner error: {str(e)}",
                "results": []
            }


# =====================================================================
# 2. JAVASCRIPT RUNNER (Node.js)
# =====================================================================
NODE_WORKER_SCRIPT = r"""
const fs = require('fs');
const vm = require('vm');

function run() {
    let inputPayload;
    try {
        inputPayload = JSON.parse(fs.readFileSync(0, 'utf-8'));
    } catch (e) {
        console.log(JSON.stringify({
            status: "Runtime Error",
            passed_test_cases: 0,
            total_test_cases: 0,
            execution_time_ms: 0.0,
            compile_error: "Invalid worker input payload: " + e.message,
            results: []
        }));
        return;
    }

    const code = inputPayload.code;
    const fnName = inputPayload.fn_name;
    const testCases = inputPayload.test_cases || [];

    let logs = [];
    const sandbox = {
        console: {
            log: (...args) => logs.push(args.map(a => typeof a === 'object' ? JSON.stringify(a) : String(a)).join(' ')),
            error: (...args) => logs.push(args.map(a => typeof a === 'object' ? JSON.stringify(a) : String(a)).join(' ')),
            warn: (...args) => logs.push(args.map(a => typeof a === 'object' ? JSON.stringify(a) : String(a)).join(' '))
        },
        Math, parseInt, parseFloat, Array, Object, String, Number, Boolean, Map, Set
    };

    const context = vm.createContext(sandbox);

    let script;
    try {
        script = new vm.Script(code);
    } catch (e) {
        console.log(JSON.stringify({
            status: "Compilation Error",
            passed_test_cases: 0,
            total_test_cases: testCases.length,
            execution_time_ms: 0.0,
            compile_error: "SyntaxError: " + e.message,
            results: []
        }));
        return;
    }

    try {
        script.runInContext(context);
    } catch (e) {
        console.log(JSON.stringify({
            status: "Runtime Error",
            passed_test_cases: 0,
            total_test_cases: testCases.length,
            execution_time_ms: 0.0,
            compile_error: "Execution Error: " + e.message,
            results: []
        }));
        return;
    }

    let targetFn = context[fnName];
    if (!targetFn || typeof targetFn !== 'function') {
        for (const key of Object.keys(context)) {
            if (typeof context[key] === 'function' && !sandbox[key]) {
                targetFn = context[key];
                break;
            }
        }
    }

    if (!targetFn || typeof targetFn !== 'function') {
        console.log(JSON.stringify({
            status: "Runtime Error",
            passed_test_cases: 0,
            total_test_cases: testCases.length,
            execution_time_ms: 0.0,
            compile_error: "Function '" + fnName + "' not found in solution.",
            results: []
        }));
        return;
    }

    const fnStr = targetFn.toString();
    const paramMatch = fnStr.match(/\(([^)]*)\)/);
    const paramNames = paramMatch ? paramMatch[1].split(',').map(s => s.trim()).filter(Boolean) : [];

    const results = [];
    let overallStatus = "Accepted";
    let totalExecTime = 0.0;

    for (const tc of testCases) {
        const tcId = tc.id;
        const inputDataStr = tc.input_data;
        const expectedOutputStr = tc.expected_output;
        const isHidden = tc.is_hidden;

        let parsedInput;
        try {
            parsedInput = JSON.parse(inputDataStr);
        } catch (e) {
            parsedInput = {};
        }

        let args = [];
        if (paramNames.length > 0 && typeof parsedInput === 'object' && !Array.isArray(parsedInput) && parsedInput !== null) {
            for (const pName of paramNames) {
                args.push(parsedInput[pName]);
            }
        } else if (Array.isArray(parsedInput)) {
            args = parsedInput;
        } else {
            args = [parsedInput];
        }

        logs = [];
        const start = process.hrtime.bigint();
        let tcStatus = "Passed";
        let actualVal = null;
        let tcError = null;

        try {
            actualVal = targetFn.apply(null, args);
        } catch (e) {
            tcStatus = "Runtime Error";
            tcError = e.stack || e.message;
        }
        const end = process.hrtime.bigint();
        const durationMs = Number(end - start) / 1e6;
        totalExecTime += durationMs;

        if (tcStatus === "Passed") {
            let expParsed;
            try {
                expParsed = JSON.parse(expectedOutputStr);
            } catch (e) {
                expParsed = expectedOutputStr;
            }

            const isEqual = (a, b) => {
                if (a === b) return true;
                if (typeof a === 'boolean' && typeof b === 'boolean') return a === b;
                if (typeof a === 'bigint' || typeof b === 'bigint') {
                    if (String(a) === expectedOutputStr.trim() || String(b) === expectedOutputStr.trim()) return true;
                    try { return BigInt(a) === BigInt(b); } catch (e) {}
                }
                if (typeof a === 'number' && typeof b === 'number') return Math.abs(a - b) < 1e-6;
                if (Array.isArray(a) && Array.isArray(b)) {
                    if (a.length !== b.length) return false;
                    for (let i = 0; i < a.length; i++) {
                        if (!isEqual(a[i], b[i])) return false;
                    }
                    return true;
                }
                if (typeof a === 'object' && a !== null && typeof b === 'object' && b !== null) {
                    const keysA = Object.keys(a);
                    const keysB = Object.keys(b);
                    if (keysA.length !== keysB.length) return false;
                    for (const k of keysA) {
                        if (!Object.prototype.hasOwnProperty.call(b, k) || !isEqual(a[k], b[k])) return false;
                    }
                    return true;
                }
                return false;
            };

            if (!isEqual(actualVal, expParsed)) {
                tcStatus = "Wrong Answer";
            }
        }

        if (tcStatus !== "Passed" && overallStatus === "Accepted") {
            overallStatus = tcStatus;
        }

        let actualStr;
        try {
            actualStr = JSON.stringify(actualVal);
        } catch (e) {
            actualStr = String(actualVal);
        }

        results.push({
            test_case_id: tcId,
            status: tcStatus,
            input_data: !isHidden ? inputDataStr : "[Hidden Test Case]",
            expected_output: !isHidden ? expectedOutputStr : "[Hidden Test Case]",
            actual_output: !isHidden ? actualStr : (tcStatus === "Passed" ? "[Hidden]" : actualStr),
            stdout: logs.join('\n'),
            execution_time_ms: Math.round(durationMs * 100) / 100,
            is_hidden: isHidden,
            error_message: tcError
        });
    }

    const passedCount = results.filter(r => r.status === "Passed").length;
    if (passedCount < results.length && overallStatus === "Accepted") {
        overallStatus = "Wrong Answer";
    }

    console.log(JSON.stringify({
        status: overallStatus,
        passed_test_cases: passedCount,
        total_test_cases: results.length,
        execution_time_ms: Math.round(totalExecTime * 100) / 100,
        compile_error: null,
        results: results
    }));
}

run();
"""


class JavaScriptCodeRunner:
    @classmethod
    def execute(
        cls,
        code: str,
        test_cases: List[Dict[str, Any]],
        starter_code: Optional[str] = None,
        timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
        is_submission: bool = False
    ) -> Dict[str, Any]:
        node_bin = shutil.which("node")
        if not node_bin:
            return {
                "status": "Compilation Error",
                "passed_test_cases": 0,
                "total_test_cases": len(test_cases),
                "execution_time_ms": 0.0,
                "compile_error": "Node.js runtime is not installed on this system.",
                "results": []
            }

        if not code or not code.strip():
            return {
                "status": "Compilation Error",
                "passed_test_cases": 0,
                "total_test_cases": len(test_cases),
                "execution_time_ms": 0.0,
                "compile_error": "Empty JavaScript code submitted. Please write a solution.",
                "results": []
            }

        active_tcs = test_cases if is_submission else [tc for tc in test_cases if not tc.get("is_hidden", False)]
        if not active_tcs:
            active_tcs = test_cases

        fn_name = extract_js_function_name(code, starter_code) or "solution"

        payload = {
            "code": code,
            "fn_name": fn_name,
            "test_cases": [
                {
                    "id": tc.get("id", idx + 1),
                    "input_data": tc.get("input_data", "{}"),
                    "expected_output": str(tc.get("expected_output", "")),
                    "is_hidden": tc.get("is_hidden", False) and is_submission
                }
                for idx, tc in enumerate(active_tcs)
            ]
        }

        start_time = time.perf_counter()
        try:
            process = subprocess.run(
                [node_bin, "-e", NODE_WORKER_SCRIPT],
                input=json.dumps(payload),
                capture_output=True,
                text=True,
                timeout=timeout_seconds
            )
            total_elapsed_ms = round((time.perf_counter() - start_time) * 1000.0, 2)

            if process.returncode != 0:
                stderr_text = process.stderr.strip() or "Node.js process exited with error."
                return {
                    "status": "Runtime Error",
                    "passed_test_cases": 0,
                    "total_test_cases": len(active_tcs),
                    "execution_time_ms": total_elapsed_ms,
                    "compile_error": stderr_text,
                    "results": []
                }

            stdout_text = process.stdout.strip()
            if not stdout_text:
                return {
                    "status": "Runtime Error",
                    "passed_test_cases": 0,
                    "total_test_cases": len(active_tcs),
                    "execution_time_ms": total_elapsed_ms,
                    "compile_error": "No output returned from JavaScript worker.",
                    "results": []
                }

            result_data = json.loads(stdout_text)
            if not result_data.get("execution_time_ms"):
                result_data["execution_time_ms"] = total_elapsed_ms
            return result_data

        except subprocess.TimeoutExpired:
            total_elapsed_ms = round((time.perf_counter() - start_time) * 1000.0, 2)
            logger.warning(f"JavaScript execution timed out after {timeout_seconds}s")
            return {
                "status": "Time Limit Exceeded",
                "passed_test_cases": 0,
                "total_test_cases": len(active_tcs),
                "execution_time_ms": total_elapsed_ms,
                "compile_error": f"Time Limit Exceeded: Execution took longer than {timeout_seconds} seconds.",
                "results": [
                    {
                        "test_case_id": tc.get("id", idx + 1),
                        "status": "Time Limit Exceeded",
                        "input_data": tc.get("input_data", "") if not tc.get("is_hidden", False) else "[Hidden Test Case]",
                        "expected_output": str(tc.get("expected_output", "")) if not tc.get("is_hidden", False) else "[Hidden Test Case]",
                        "actual_output": "Time Limit Exceeded",
                        "stdout": "",
                        "execution_time_ms": round(timeout_seconds * 1000.0, 2),
                        "is_hidden": tc.get("is_hidden", False),
                        "error_message": "Execution timed out."
                    }
                    for idx, tc in enumerate(active_tcs)
                ]
            }
        except Exception as e:
            total_elapsed_ms = round((time.perf_counter() - start_time) * 1000.0, 2)
            return {
                "status": "Runtime Error",
                "passed_test_cases": 0,
                "total_test_cases": len(active_tcs),
                "execution_time_ms": total_elapsed_ms,
                "compile_error": f"JavaScript execution runner error: {str(e)}",
                "results": []
            }


# =====================================================================
# 3. JAVA RUNNER (javac & java 21)
# =====================================================================
def _py_to_java_literal(val: Any, expected_type: Optional[str] = None) -> str:
    if isinstance(val, bool):
        return "true" if val else "false"
    if isinstance(val, int):
        if val > 9223372036854775807 or val < -9223372036854775808:
            return f'new java.math.BigInteger("{val}")'
        if val > 2147483647 or val < -2147483648:
            return f"{val}L"
        return str(val)
    if isinstance(val, float):
        return f"{val}d"
    if isinstance(val, str):
        return json.dumps(val)
    if isinstance(val, dict):
        if not val:
            return "makeMap()"
        entries = []
        for k, v in val.items():
            entries.append(f"{_py_to_java_literal(k)}, {_py_to_java_literal(v)}")
        return f"makeMap({', '.join(entries)})"
    if isinstance(val, list):
        if not val:
            if expected_type == "Integer[]":
                return "new Integer[]{}"
            if expected_type == "String[]":
                return "new String[]{}"
            if expected_type == "char[][]":
                return "new char[][]{}"
            return "new int[]{}"
        if all(isinstance(x, dict) for x in val):
            return f"new Object[]{{{', '.join(_py_to_java_literal(x) for x in val)}}}"
        if all(isinstance(x, bool) for x in val):
            return f"new boolean[]{{{', '.join('true' if x else 'false' for x in val)}}}"
        if all(isinstance(x, int) and not isinstance(x, bool) for x in val):
            if any(x > 9223372036854775807 or x < -9223372036854775808 for x in val):
                items = [f'new java.math.BigInteger("{x}")' for x in val]
                return f"new java.math.BigInteger[]{{{', '.join(items)}}}"
            if any(x > 2147483647 or x < -2147483648 for x in val):
                return f"new long[]{{{', '.join(str(x) + 'L' for x in val)}}}"
            if expected_type == "Integer[]":
                return f"new Integer[]{{{', '.join(str(x) for x in val)}}}"
            return f"new int[]{{{', '.join(str(x) for x in val)}}}"
        if all(isinstance(x, str) for x in val):
            return f"new String[]{{{', '.join(json.dumps(x) for x in val)}}}"
        if all(x is None or isinstance(x, int) for x in val):
            return f"new Integer[]{{{', '.join(str(x) if x is not None else 'null' for x in val)}}}"
        if all(isinstance(x, list) for x in val):
            if expected_type != "String[][]" and val and any(x for x in val) and all(all(isinstance(y, str) and len(y) == 1 for y in x) for x in val):
                inner = ", ".join(f"new char[]{{{', '.join(repr(y) for y in x)}}}" for x in val)
                return f"new char[][]{{{inner}}}"
            if val and any(x for x in val) and all(all(isinstance(y, str) for y in x) for x in val):
                inner = ", ".join(f"new String[]{{{', '.join(json.dumps(y) for y in x)}}}" for x in val)
                return f"new String[][]{{{inner}}}"
            if val and all(all(isinstance(y, int) for y in x) for x in val):
                inner = ", ".join(f"new int[]{{{', '.join(str(y) for y in x)}}}" for x in val)
                return f"new int[][]{{{inner}}}"
            inner = ", ".join(f"new Object[]{{{', '.join(_py_to_java_literal(y) for y in x)}}}" for x in val)
            return f"new Object[][]{{{inner}}}"
        return f"new Object[]{{{', '.join(_py_to_java_literal(x) for x in val)}}}"
    return json.dumps(val)


def _generate_java_driver(method_name: str, test_cases: List[Dict[str, Any]], param_types: Optional[List[str]] = None) -> str:
    lines = [
        "import java.io.*;",
        "import java.util.*;",
        "",
        "public class Driver {",
        "    private static String escape(String s) {",
        "        if (s == null) return \"null\";",
        "        return s.replace(\"\\\\\", \"\\\\\\\\\").replace(\"\\\"\", \"\\\\\\\"\").replace(\"\\n\", \"\\\\n\").replace(\"\\r\", \"\\\\r\");",
        "    }",
        "",
        "    private static java.util.Map<Object, Object> makeMap(Object... kvs) {",
        "        java.util.Map<Object, Object> m = new java.util.LinkedHashMap<>();",
        "        for (int i = 0; i < kvs.length; i += 2) {",
        "            m.put(kvs[i], kvs[i + 1]);",
        "        }",
        "        return m;",
        "    }",
        "",
        "    private static String formatVal(Object obj) {",
        "        if (obj == null) return \"null\";",
        "        if (obj instanceof int[]) return Arrays.toString((int[]) obj);",
        "        if (obj instanceof long[]) return Arrays.toString((long[]) obj);",
        "        if (obj instanceof double[]) return Arrays.toString((double[]) obj);",
        "        if (obj instanceof boolean[]) return Arrays.toString((boolean[]) obj);",
        "        if (obj instanceof char[]) return Arrays.toString((char[]) obj);",
        "        if (obj instanceof Object[]) return Arrays.deepToString((Object[]) obj);",
        "        if (obj instanceof Map) return obj.toString();",
        "        return String.valueOf(obj);",
        "    }",
        "",
        "    private static boolean checkEqual(Object actual, Object expected) {",
        "        if (actual == null && expected == null) return true;",
        "        if (actual == null || expected == null) return false;",
        "        if (actual instanceof int[] && expected instanceof int[]) {",
        "            return Arrays.equals((int[]) actual, (int[]) expected);",
        "        }",
        "        if (actual instanceof long[] && expected instanceof long[]) {",
        "            return Arrays.equals((long[]) actual, (long[]) expected);",
        "        }",
        "        if (actual instanceof Object[] && expected instanceof Object[]) {",
        "            return Arrays.deepEquals((Object[]) actual, (Object[]) expected);",
        "        }",
        "        if (actual instanceof double[] && expected instanceof double[]) {",
        "            double[] a = (double[]) actual, b = (double[]) expected;",
        "            if (a.length != b.length) return false;",
        "            for (int i = 0; i < a.length; i++) if (Math.abs(a[i] - b[i]) >= 1e-6) return false;",
        "            return true;",
        "        }",
        "        if (actual instanceof boolean[] && expected instanceof boolean[]) {",
        "            return Arrays.equals((boolean[]) actual, (boolean[]) expected);",
        "        }",
        "        if (actual instanceof Map && expected instanceof Map) {",
        "            Map<?, ?> m1 = (Map<?, ?>) actual, m2 = (Map<?, ?>) expected;",
        "            if (m1.size() != m2.size()) return false;",
        "            for (Map.Entry<?, ?> e : m1.entrySet()) {",
        "                if (!m2.containsKey(e.getKey())) return false;",
        "                if (!checkEqual(e.getValue(), m2.get(e.getKey()))) return false;",
        "            }",
        "            return true;",
        "        }",
        "        if (actual instanceof Number && expected instanceof Number) {",
        "            return Math.abs(((Number) actual).doubleValue() - ((Number) expected).doubleValue()) < 1e-6;",
        "        }",
        "        return actual.equals(expected);",
        "    }",
        "",
        "    public static void main(String[] args) {",
        "        Solution sol = new Solution();",
        "        int passed = 0;",
        "        int total = " + str(len(test_cases)) + ";",
        "        long startTotal = System.nanoTime();",
        "        StringBuilder resultsJson = new StringBuilder();",
        "        resultsJson.append(\"[\");",
        "        String overallStatus = \"Accepted\";",
        ""
    ]

    for idx, tc in enumerate(test_cases):
        tc_id = tc.get("id", idx + 1)
        raw_input = tc.get("input_data", "{}")
        raw_exp = str(tc.get("expected_output", ""))
        is_hidden = tc.get("is_hidden", False)

        try:
            inp = json.loads(raw_input)
        except Exception:
            inp = {}

        if isinstance(inp, dict):
            args_call = ", ".join(
                _py_to_java_literal(v, param_types[p_idx] if (param_types and p_idx < len(param_types)) else None)
                for p_idx, v in enumerate(inp.values())
            )
        elif isinstance(inp, list):
            args_call = ", ".join(
                _py_to_java_literal(v, param_types[p_idx] if (param_types and p_idx < len(param_types)) else None)
                for p_idx, v in enumerate(inp)
            )
        else:
            args_call = _py_to_java_literal(inp, param_types[0] if param_types else None)

        try:
            exp_parsed = json.loads(raw_exp)
        except Exception:
            exp_parsed = raw_exp

        lines.extend([
            f"        // Test Case {tc_id}",
            "        {",
            "            ByteArrayOutputStream baos = new ByteArrayOutputStream();",
            "            PrintStream oldOut = System.out;",
            "            System.setOut(new PrintStream(baos));",
            "            String tcStatus = \"Passed\";",
            "            String tcError = null;",
            "            String actualStr = \"\";",
            "            long t0 = System.nanoTime();",
            "            try {",
            f"                Object actual = sol.{method_name}({args_call});",
            "                actualStr = formatVal(actual);",
        ])

        if isinstance(exp_parsed, list):
            if all(isinstance(x, bool) for x in exp_parsed):
                exp_lit = f"new boolean[]{{{', '.join(str(x).lower() for x in exp_parsed)}}}"
                lines.append(f"                if (!checkEqual(actual, {exp_lit})) {{ tcStatus = \"Wrong Answer\"; }}")
            elif not exp_parsed or all(isinstance(x, int) and not isinstance(x, bool) for x in exp_parsed):
                if any(x > 9223372036854775807 or x < -9223372036854775808 for x in exp_parsed):
                    items = [f'new java.math.BigInteger("{x}")' for x in exp_parsed]
                    exp_lit = f"new java.math.BigInteger[]{{{', '.join(items)}}}"
                elif any(x > 2147483647 or x < -2147483648 for x in exp_parsed):
                    exp_lit = f"new long[]{{{', '.join(str(x) + 'L' for x in exp_parsed)}}}"
                else:
                    exp_lit = f"new int[]{{{', '.join(str(x) for x in exp_parsed)}}}"
                lines.append(f"                if (!checkEqual(actual, {exp_lit})) {{ tcStatus = \"Wrong Answer\"; }}")
            elif all(isinstance(x, str) for x in exp_parsed):
                exp_lit = f"new String[]{{{', '.join(json.dumps(x) for x in exp_parsed)}}}"
                lines.append(f"                if (!checkEqual(actual, {exp_lit})) {{ tcStatus = \"Wrong Answer\"; }}")
            elif all(isinstance(x, float) for x in exp_parsed):
                exp_lit = f"new double[]{{{', '.join(f'{x}d' for x in exp_parsed)}}}"
                lines.append(f"                if (!checkEqual(actual, {exp_lit})) {{ tcStatus = \"Wrong Answer\"; }}")
            elif all(isinstance(x, list) for x in exp_parsed):
                if all(all(isinstance(y, int) for y in sub) for sub in exp_parsed):
                    inners = ", ".join(f"new int[]{{{', '.join(str(y) for y in sub)}}}" for sub in exp_parsed)
                    exp_lit = f"new int[][]{{{inners}}}"
                    lines.append(f"                if (!checkEqual(actual, {exp_lit})) {{ tcStatus = \"Wrong Answer\"; }}")
                elif all(all(isinstance(y, str) for y in sub) for sub in exp_parsed):
                    inners = ", ".join(f"new String[]{{{', '.join(json.dumps(y) for y in sub)}}}" for sub in exp_parsed)
                    exp_lit = f"new String[][]{{{inners}}}"
                    lines.append(f"                if (!checkEqual(actual, {exp_lit})) {{ tcStatus = \"Wrong Answer\"; }}")
                else:
                    inners = ", ".join(f"new Object[]{{{', '.join(_py_to_java_literal(y) for y in sub)}}}" for sub in exp_parsed)
                    exp_lit = f"new Object[][]{{{inners}}}"
                    lines.append(f"                if (!checkEqual(actual, {exp_lit})) {{ tcStatus = \"Wrong Answer\"; }}")
        elif isinstance(exp_parsed, bool):
            lines.append(f"                if (!checkEqual(actual, {str(exp_parsed).lower()})) {{ tcStatus = \"Wrong Answer\"; }}")
        elif isinstance(exp_parsed, (int, float)):
            if isinstance(exp_parsed, int) and (exp_parsed > 9223372036854775807 or exp_parsed < -9223372036854775808):
                lines.append(f'                if (!checkEqual(actual, new java.math.BigInteger("{exp_parsed}"))) {{ tcStatus = "Wrong Answer"; }}')
            elif isinstance(exp_parsed, int) and (exp_parsed > 2147483647 or exp_parsed < -2147483648):
                lines.append(f'                if (!checkEqual(actual, {exp_parsed}L)) {{ tcStatus = "Wrong Answer"; }}')
            else:
                lines.append(f'                if (!checkEqual(actual, {exp_parsed})) {{ tcStatus = "Wrong Answer"; }}')
        elif isinstance(exp_parsed, str):
            lines.append(f"                if (!checkEqual(actual, {json.dumps(exp_parsed)})) {{ tcStatus = \"Wrong Answer\"; }}")
        elif isinstance(exp_parsed, dict):
            exp_lit = _py_to_java_literal(exp_parsed)
            lines.append(f"                if (!checkEqual(actual, {exp_lit})) {{ tcStatus = \"Wrong Answer\"; }}")

        lines.extend([
            "            } catch (Throwable ex) {",
            "                tcStatus = \"Runtime Error\";",
            "                StringWriter sw = new StringWriter();",
            "                ex.printStackTrace(new PrintWriter(sw));",
            "                tcError = sw.toString();",
            "            } finally {",
            "                System.setOut(oldOut);",
            "            }",
            "            long t1 = System.nanoTime();",
            "            double durationMs = (t1 - t0) / 1e6;",
            "            if (\"Passed\".equals(tcStatus)) passed++;",
            "            else if (\"Accepted\".equals(overallStatus)) overallStatus = tcStatus;",
            "",
            "            if (" + str(idx) + " > 0) resultsJson.append(\",\");",
            "            resultsJson.append(\"{\");",
            f"            resultsJson.append(\"\\\"test_case_id\\\":\").append({tc_id}).append(\",\");",
            "            resultsJson.append(\"\\\"status\\\":\\\"\").append(tcStatus).append(\"\\\",\");",
            f"            resultsJson.append(\"\\\"input_data\\\":\\\"\").append(escape({json.dumps(raw_input if not is_hidden else '[Hidden Test Case]')})).append(\"\\\",\");",
            f"            resultsJson.append(\"\\\"expected_output\\\":\\\"\").append(escape({json.dumps(raw_exp if not is_hidden else '[Hidden Test Case]')})).append(\"\\\",\");",
            f"            resultsJson.append(\"\\\"actual_output\\\":\\\"\").append({('\"[Hidden]\"' if is_hidden else 'escape(actualStr)')}).append(\"\\\",\");",
            "            resultsJson.append(\"\\\"stdout\\\":\\\"\").append(escape(baos.toString())).append(\"\\\",\");",
            "            resultsJson.append(\"\\\"execution_time_ms\\\":\").append(Math.round(durationMs * 100.0) / 100.0).append(\",\");",
            f"            resultsJson.append(\"\\\"is_hidden\\\":\").append({str(is_hidden).lower()}).append(\",\");",
            "            resultsJson.append(\"\\\"error_message\\\":\").append(tcError == null ? \"null\" : \"\\\"\" + escape(tcError) + \"\\\"\");",
            "            resultsJson.append(\"}\");",
            "        }",
            ""
        ])

    lines.extend([
        "        resultsJson.append(\"]\");",
        "        long endTotal = System.nanoTime();",
        "        double totalMs = (endTotal - startTotal) / 1e6;",
        "        if (passed < total && \"Accepted\".equals(overallStatus)) overallStatus = \"Wrong Answer\";",
        "",
        "        StringBuilder finalJson = new StringBuilder();",
        "        finalJson.append(\"{\");",
        "        finalJson.append(\"\\\"status\\\":\\\"\").append(overallStatus).append(\"\\\",\");",
        "        finalJson.append(\"\\\"passed_test_cases\\\":\").append(passed).append(\",\");",
        "        finalJson.append(\"\\\"total_test_cases\\\":\").append(total).append(\",\");",
        "        finalJson.append(\"\\\"execution_time_ms\\\":\").append(Math.round(totalMs * 100.0) / 100.0).append(\",\");",
        "        finalJson.append(\"\\\"compile_error\\\":null,\");",
        "        finalJson.append(\"\\\"results\\\":\").append(resultsJson.toString());",
        "        finalJson.append(\"}\");",
        "        System.out.println(finalJson.toString());",
        "    }",
        "}"
    ])
    return "\n".join(lines)


class JavaCodeRunner:
    DEFAULT_COMPILE_TIMEOUT_SECONDS = DEFAULT_JAVA_COMPILE_TIMEOUT_SECONDS

    @classmethod
    def execute(
        cls,
        code: str,
        test_cases: List[Dict[str, Any]],
        starter_code: Optional[str] = None,
        timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
        is_submission: bool = False,
        compile_timeout: Optional[float] = None
    ) -> Dict[str, Any]:
        javac_bin = shutil.which("javac")
        java_bin = shutil.which("java")
        if not javac_bin or not java_bin:
            return {
                "status": "Compilation Error",
                "passed_test_cases": 0,
                "total_test_cases": len(test_cases),
                "execution_time_ms": 0.0,
                "compile_error": "Java compiler (javac) or runtime (java) is not installed on this system.",
                "results": []
            }

        if not code or not code.strip():
            return {
                "status": "Compilation Error",
                "passed_test_cases": 0,
                "total_test_cases": len(test_cases),
                "execution_time_ms": 0.0,
                "compile_error": "Empty Java code submitted. Please write a solution.",
                "results": []
            }

        active_tcs = test_cases if is_submission else [tc for tc in test_cases if not tc.get("is_hidden", False)]
        if not active_tcs:
            active_tcs = test_cases

        method_name = extract_java_method_name(code, starter_code) or "solve"
        param_types = extract_java_param_types(code, starter_code)

        start_time = time.perf_counter()
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                sol_file = os.path.join(tmpdir, "Solution.java")
                with open(sol_file, "w", encoding="utf-8") as f:
                    f.write(code)

                driver_code = _generate_java_driver(method_name, active_tcs, param_types)
                driver_file = os.path.join(tmpdir, "Driver.java")
                with open(driver_file, "w", encoding="utf-8") as f:
                    f.write(driver_code)

                # 1. Compile with bounded compilation timeout
                c_timeout = compile_timeout or cls.DEFAULT_COMPILE_TIMEOUT_SECONDS
                try:
                    c_proc = subprocess.run(
                        [javac_bin, "-encoding", "utf-8", "-proc:none", "Solution.java", "Driver.java"],
                        cwd=tmpdir,
                        capture_output=True,
                        text=True,
                        timeout=c_timeout
                    )
                except subprocess.TimeoutExpired:
                    total_elapsed_ms = round((time.perf_counter() - start_time) * 1000.0, 2)
                    logger.warning(f"Java compilation timed out after {c_timeout}s")
                    return {
                        "status": "Compilation Error",
                        "passed_test_cases": 0,
                        "total_test_cases": len(active_tcs),
                        "execution_time_ms": total_elapsed_ms,
                        "compile_error": f"Compilation timed out after {c_timeout} seconds.",
                        "results": []
                    }

                total_elapsed_ms = round((time.perf_counter() - start_time) * 1000.0, 2)

                if c_proc.returncode != 0:
                    return {
                        "status": "Compilation Error",
                        "passed_test_cases": 0,
                        "total_test_cases": len(active_tcs),
                        "execution_time_ms": total_elapsed_ms,
                        "compile_error": c_proc.stderr.strip() or "Java compilation failed.",
                        "results": []
                    }

                # 2. Execute with bounded runtime execution timeout
                try:
                    r_proc = subprocess.run(
                        [java_bin, "Driver"],
                        cwd=tmpdir,
                        capture_output=True,
                        text=True,
                        timeout=timeout_seconds
                    )
                except subprocess.TimeoutExpired:
                    total_elapsed_ms = round((time.perf_counter() - start_time) * 1000.0, 2)
                    logger.warning(f"Java execution timed out after {timeout_seconds}s")
                    return {
                        "status": "Time Limit Exceeded",
                        "passed_test_cases": 0,
                        "total_test_cases": len(active_tcs),
                        "execution_time_ms": total_elapsed_ms,
                        "compile_error": f"Time Limit Exceeded: Execution took longer than {timeout_seconds} seconds.",
                        "results": [
                            {
                                "test_case_id": tc.get("id", idx + 1),
                                "status": "Time Limit Exceeded",
                                "input_data": tc.get("input_data", "") if not tc.get("is_hidden", False) else "[Hidden Test Case]",
                                "expected_output": str(tc.get("expected_output", "")) if not tc.get("is_hidden", False) else "[Hidden Test Case]",
                                "actual_output": "Time Limit Exceeded",
                                "stdout": "",
                                "execution_time_ms": round(timeout_seconds * 1000.0, 2),
                                "is_hidden": tc.get("is_hidden", False),
                                "error_message": "Execution timed out."
                            }
                            for idx, tc in enumerate(active_tcs)
                        ]
                    }

                total_elapsed_ms = round((time.perf_counter() - start_time) * 1000.0, 2)

                if r_proc.returncode != 0:
                    stderr_text = r_proc.stderr.strip() or "Java execution failed."
                    return {
                        "status": "Runtime Error",
                        "passed_test_cases": 0,
                        "total_test_cases": len(active_tcs),
                        "execution_time_ms": total_elapsed_ms,
                        "compile_error": stderr_text,
                        "results": []
                    }

                stdout_text = r_proc.stdout.strip()
                if not stdout_text:
                    return {
                        "status": "Runtime Error",
                        "passed_test_cases": 0,
                        "total_test_cases": len(active_tcs),
                        "execution_time_ms": total_elapsed_ms,
                        "compile_error": "No output returned from Java execution.",
                        "results": []
                    }

                result_data = json.loads(stdout_text)
                if not result_data.get("execution_time_ms"):
                    result_data["execution_time_ms"] = total_elapsed_ms
                return result_data

        except Exception as e:
            total_elapsed_ms = round((time.perf_counter() - start_time) * 1000.0, 2)
            return {
                "status": "Runtime Error",
                "passed_test_cases": 0,
                "total_test_cases": len(active_tcs),
                "execution_time_ms": total_elapsed_ms,
                "compile_error": f"Java runner error: {str(e)}",
                "results": []
            }


# =====================================================================
# 4. C++ RUNNER (g++ / clang++)
# =====================================================================
def _py_to_cpp_literal(val: Any, expected_type: Optional[str] = None) -> str:
    if isinstance(val, bool):
        return "true" if val else "false"
    if isinstance(val, int):
        if val > 2147483647 or val < -2147483648:
            return f"{val}LL"
        return str(val)
    if isinstance(val, float):
        return f"{val}"
    if isinstance(val, str):
        return json.dumps(val)
    if isinstance(val, dict):
        if any(isinstance(v, dict) for v in val.values()):
            return f"std::string({json.dumps(json.dumps(val))})"
        if not val:
            if expected_type:
                return f"std::{expected_type}{{}}"
            return "std::unordered_map<std::string, std::string>{}"
        if all(isinstance(v, list) for v in val.values()):
            if all(all(isinstance(x, int) and not isinstance(x, bool) for x in v) for v in val.values()):
                map_type = "std::unordered_map<std::string, std::vector<int>>"
            else:
                map_type = "std::unordered_map<std::string, std::vector<std::string>>"
        elif all(isinstance(v, int) for v in val.values()):
            map_type = "std::unordered_map<std::string, int>"
        else:
            map_type = "std::unordered_map<std::string, std::string>"
        pairs = []
        for k, v in val.items():
            if map_type == "std::unordered_map<std::string, std::string>" and not isinstance(v, str):
                pairs.append(f"{{{_py_to_cpp_literal(k)}, {_py_to_cpp_literal(str(v))}}}")
            else:
                pairs.append(f"{{{_py_to_cpp_literal(k)}, {_py_to_cpp_literal(v)}}}")
        return f"{map_type}{{{', '.join(pairs)}}}"
    if isinstance(val, list):
        if not val:
            if expected_type and "string" in expected_type:
                return "std::vector<std::string>{}"
            if expected_type and "char" in expected_type:
                return "std::vector<char>{}"
            return "std::vector<int>{}"
        if all(isinstance(x, dict) for x in val):
            return f"std::vector<std::unordered_map<std::string, std::string>>{{{', '.join(_py_to_cpp_literal(x) for x in val)}}}"
        if all(isinstance(x, bool) for x in val):
            return f"std::vector<bool>{{{', '.join('true' if x else 'false' for x in val)}}}"
        if all(isinstance(x, int) and not isinstance(x, bool) for x in val):
            if any(x > 9223372036854775807 or x < -9223372036854775808 for x in val):
                return f"std::vector<std::string>{{{', '.join(json.dumps(str(x)) for x in val)}}}"
            if any(x > 2147483647 or x < -2147483648 for x in val):
                return f"std::vector<long long>{{{', '.join(str(x) + 'LL' for x in val)}}}"
            return f"std::vector<int>{{{', '.join(str(x) for x in val)}}}"
        if all(isinstance(x, str) for x in val):
            return f"std::vector<std::string>{{{', '.join(json.dumps(x) for x in val)}}}"
        if all(x is None or isinstance(x, int) for x in val):
            return f"std::vector<std::string>{{{', '.join(json.dumps(str(x) if x is not None else 'null') for x in val)}}}"
        if all(isinstance(x, list) for x in val):
            if (not expected_type or "string" not in expected_type) and val and any(x for x in val) and all(all(isinstance(y, str) and len(y) == 1 for y in x) for x in val):
                inner = ", ".join(f"std::vector<char>{{{', '.join(repr(y) for y in x)}}}" for x in val)
                return f"std::vector<std::vector<char>>{{{inner}}}"
            if val and any(x for x in val) and all(all(isinstance(y, str) for y in x) for x in val):
                inner = ", ".join(f"std::vector<std::string>{{{', '.join(json.dumps(y) for y in x)}}}" for x in val)
                return f"std::vector<std::vector<std::string>>{{{inner}}}"
            if val and all(all(isinstance(y, int) for y in x) for x in val):
                inner = ", ".join(f"std::vector<int>{{{', '.join(str(y) for y in x)}}}" for x in val)
                return f"std::vector<std::vector<int>>{{{inner}}}"
            inner = ", ".join(f"std::vector<std::string>{{{', '.join(json.dumps(str(y)) for y in x)}}}" for x in val)
            return f"std::vector<std::vector<std::string>>{{{inner}}}"
        return f"std::vector<std::string>{{{', '.join(json.dumps(str(x)) for x in val)}}}"
    return json.dumps(val)


def _generate_cpp_driver(method_name: str, test_cases: List[Dict[str, Any]], param_types: Optional[List[str]] = None) -> str:
    lines = [
        "#include <iostream>",
        "#include <vector>",
        "#include <string>",
        "#include <chrono>",
        "#include <sstream>",
        "#include <cmath>",
        "#include <algorithm>",
        "#include <unordered_map>",
        "#include <unordered_set>",
        "#include <queue>",
        "#include <stack>",
        "",
        "#include \"Solution.cpp\"",
        "",
        "static std::string escape(const std::string& s) {",
        "    std::string res;",
        "    for (char c : s) {",
        "        if (c == '\\\\') res += \"\\\\\\\\\";",
        "        else if (c == '\"') res += \"\\\\\\\"\";",
        "        else if (c == '\\n') res += \"\\\\n\";",
        "        else if (c == '\\r') res += \"\\\\r\";",
        "        else if (c == '\\t') res += \"\\\\t\";",
        "        else res += c;",
        "    }",
        "    return res;",
        "}",
        "",
        "template <typename T>",
        "static std::string formatVal(const T& val) {",
        "    std::ostringstream oss;",
        "    oss << val;",
        "    return oss.str();",
        "}",
        "",
        "static std::string formatVal(bool val) {",
        "    return val ? \"true\" : \"false\";",
        "}",
        "",
        "template <typename K, typename V>",
        "static std::string formatVal(const std::unordered_map<K, V>& m);",
        "",
        "template <typename T>",
        "static std::string formatVal(const std::vector<T>& vec) {",
        "    std::ostringstream oss;",
        "    oss << \"[\";",
        "    for (size_t i = 0; i < vec.size(); ++i) {",
        "        if (i > 0) oss << \", \";",
        "        oss << formatVal(vec[i]);",
        "    }",
        "    oss << \"]\";",
        "    return oss.str();",
        "}",
        "",
        "template <typename K, typename V>",
        "static std::string formatVal(const std::unordered_map<K, V>& m) {",
        "    std::ostringstream oss;",
        "    oss << \"{\";",
        "    bool first = true;",
        "    for (const auto& p : m) {",
        "        if (!first) oss << \", \";",
        "        first = false;",
        "        oss << formatVal(p.first) << \": \" << formatVal(p.second);",
        "    }",
        "    oss << \"}\";",
        "    return oss.str();",
        "}",
        "",
        "template <typename T, typename U>",
        "static bool checkEqual(const T& a, const U& b) {",
        "    return a == b;",
        "}",
        "",
        "template <typename K, typename V>",
        "static bool checkEqual(const std::unordered_map<K, V>& a, const std::unordered_map<K, V>& b) {",
        "    return a == b;",
        "}",
        "",
        "static bool checkEqual(const std::string& a, long long b) {",
        "    return a == std::to_string(b);",
        "}",
        "static bool checkEqual(long long a, const std::string& b) {",
        "    return std::to_string(a) == b;",
        "}",
        "static bool checkEqual(const std::string& a, int b) {",
        "    return a == std::to_string(b);",
        "}",
        "static bool checkEqual(int a, const std::string& b) {",
        "    return std::to_string(a) == b;",
        "}",
        "static bool checkEqual(const std::string& a, const std::string& b) {",
        "    return a == b;",
        "}",
        "",
        "static bool checkEqual(double a, double b) {",
        "    return std::abs(a - b) < 1e-6;",
        "}",
        "",
        "int main() {",
        "    Solution sol;",
        "    int passed = 0;",
        "    int total = " + str(len(test_cases)) + ";",
        "    std::string overallStatus = \"Accepted\";",
        "    std::ostringstream resultsJson;",
        "    resultsJson << \"[\";",
        "    auto startTotal = std::chrono::high_resolution_clock::now();",
        ""
    ]

    for idx, tc in enumerate(test_cases):
        tc_id = tc.get("id", idx + 1)
        raw_input = tc.get("input_data", "{}")
        raw_exp = str(tc.get("expected_output", ""))
        is_hidden = tc.get("is_hidden", False)

        try:
            inp = json.loads(raw_input)
        except Exception:
            inp = {}

        # Generate named local argument variables so both value and non-const reference signatures bind cleanly
        arg_decls = []
        arg_names = []
        if isinstance(inp, dict):
            for a_idx, (k, v) in enumerate(inp.items()):
                p_type = param_types[a_idx] if (param_types and a_idx < len(param_types)) else None
                v_name = f"arg_{idx}_{a_idx}"
                arg_decls.append(f"            auto {v_name} = {_py_to_cpp_literal(v, p_type)};")
                arg_names.append(v_name)
        elif isinstance(inp, list):
            for a_idx, v in enumerate(inp):
                p_type = param_types[a_idx] if (param_types and a_idx < len(param_types)) else None
                v_name = f"arg_{idx}_{a_idx}"
                arg_decls.append(f"            auto {v_name} = {_py_to_cpp_literal(v, p_type)};")
                arg_names.append(v_name)
        else:
            p_type = param_types[0] if param_types else None
            v_name = f"arg_{idx}_0"
            arg_decls.append(f"            auto {v_name} = {_py_to_cpp_literal(inp, p_type)};")
            arg_names.append(v_name)

        args_call = ", ".join(arg_names)

        lines.extend([
            f"    // Test Case {tc_id}",
            "    {",
            "        std::string tcStatus = \"Passed\";",
            "        std::string tcError = \"\";",
            "        std::string actualStr = \"\";",
            "        auto t0 = std::chrono::high_resolution_clock::now();",
            "        try {",
            *arg_decls,
            f"            auto actual = sol.{method_name}({args_call});",
            "            actualStr = formatVal(actual);",
        ])

        try:
            exp_parsed = json.loads(raw_exp)
        except Exception:
            exp_parsed = raw_exp

        if isinstance(exp_parsed, list):
            if all(isinstance(x, bool) for x in exp_parsed):
                exp_lit = f"std::vector<bool>{{{', '.join(str(x).lower() for x in exp_parsed)}}}"
                lines.append(f"            if (!checkEqual(actual, {exp_lit})) {{ tcStatus = \"Wrong Answer\"; }}")
            elif not exp_parsed or all(isinstance(x, int) and not isinstance(x, bool) for x in exp_parsed):
                if any(x > 9223372036854775807 or x < -9223372036854775808 for x in exp_parsed):
                    exp_lit = f"std::vector<std::string>{{{', '.join(json.dumps(str(x)) for x in exp_parsed)}}}"
                elif any(x > 2147483647 or x < -2147483648 for x in exp_parsed):
                    exp_lit = f"std::vector<long long>{{{', '.join(str(x) + 'LL' for x in exp_parsed)}}}"
                else:
                    exp_lit = f"std::vector<int>{{{', '.join(str(x) for x in exp_parsed)}}}"
                lines.append(f"            if (!checkEqual(actual, {exp_lit})) {{ tcStatus = \"Wrong Answer\"; }}")
            elif all(isinstance(x, str) for x in exp_parsed):
                exp_lit = f"std::vector<std::string>{{{', '.join(json.dumps(x) for x in exp_parsed)}}}"
                lines.append(f"            if (!checkEqual(actual, {exp_lit})) {{ tcStatus = \"Wrong Answer\"; }}")
            elif all(isinstance(x, float) for x in exp_parsed):
                exp_lit = f"std::vector<double>{{{', '.join(str(x) for x in exp_parsed)}}}"
                lines.append(f"            if (!checkEqual(actual, {exp_lit})) {{ tcStatus = \"Wrong Answer\"; }}")
            elif all(isinstance(x, dict) for x in exp_parsed):
                exp_lit = _py_to_cpp_literal(exp_parsed)
                lines.append(f"            if (!checkEqual(actual, {exp_lit})) {{ tcStatus = \"Wrong Answer\"; }}")
            elif all(isinstance(x, list) for x in exp_parsed):
                if exp_parsed and any(x for x in exp_parsed) and all(isinstance(y, list) for sub in exp_parsed for y in sub):
                    if all(all(all(isinstance(z, str) for z in y) for y in sub) for sub in exp_parsed):
                        inners = ", ".join(f"{{{', '.join(f'{{{', '.join(json.dumps(z) for z in y)}}}' for y in sub)}}}" for sub in exp_parsed)
                        exp_lit = f"std::vector<std::vector<std::vector<std::string>>>{{{inners}}}"
                        lines.append(f"            if (!checkEqual(actual, {exp_lit})) {{ tcStatus = \"Wrong Answer\"; }}")
                    elif all(all(all(isinstance(z, int) and not isinstance(z, bool) for z in y) for y in sub) for sub in exp_parsed):
                        inners = ", ".join(f"{{{', '.join(f'{{{', '.join(str(z) for z in y)}}}' for y in sub)}}}" for sub in exp_parsed)
                        exp_lit = f"std::vector<std::vector<std::vector<int>>>{{{inners}}}"
                        lines.append(f"            if (!checkEqual(actual, {exp_lit})) {{ tcStatus = \"Wrong Answer\"; }}")
                    else:
                        inners = ", ".join(f"{{{', '.join(f'{{{', '.join(json.dumps(str(z)) for y in sub)}}}' for y in sub)}}}" for sub in exp_parsed)
                        exp_lit = f"std::vector<std::vector<std::vector<std::string>>>{{{inners}}}"
                        lines.append(f"            if (!checkEqual(actual, {exp_lit})) {{ tcStatus = \"Wrong Answer\"; }}")
                elif all(all(isinstance(y, int) for y in sub) for sub in exp_parsed):
                    inners = ", ".join(f"{{{', '.join(str(y) for y in sub)}}}" for sub in exp_parsed)
                    exp_lit = f"std::vector<std::vector<int>>{{{inners}}}"
                    lines.append(f"            if (!checkEqual(actual, {exp_lit})) {{ tcStatus = \"Wrong Answer\"; }}")
                elif all(all(isinstance(y, str) for y in sub) for sub in exp_parsed):
                    inners = ", ".join(f"{{{', '.join(json.dumps(y) for y in sub)}}}" for sub in exp_parsed)
                    exp_lit = f"std::vector<std::vector<std::string>>{{{inners}}}"
                    lines.append(f"            if (!checkEqual(actual, {exp_lit})) {{ tcStatus = \"Wrong Answer\"; }}")
                else:
                    inners = ", ".join(f"{{{', '.join(json.dumps(str(y)) for y in sub)}}}" for sub in exp_parsed)
                    exp_lit = f"std::vector<std::vector<std::string>>{{{inners}}}"
                    lines.append(f"            if (!checkEqual(actual, {exp_lit})) {{ tcStatus = \"Wrong Answer\"; }}")
        elif isinstance(exp_parsed, bool):
            lines.append(f"            if (!checkEqual(actual, {str(exp_parsed).lower()})) {{ tcStatus = \"Wrong Answer\"; }}")
        elif isinstance(exp_parsed, (int, float)):
            if isinstance(exp_parsed, int) and (exp_parsed > 9223372036854775807 or exp_parsed < -9223372036854775808):
                lines.append(f"            if (!checkEqual(formatVal(actual), std::string(\"{exp_parsed}\"))) {{ tcStatus = \"Wrong Answer\"; }}")
            elif isinstance(exp_parsed, int) and (exp_parsed > 2147483647 or exp_parsed < -2147483648):
                lines.append(f"            if (!checkEqual(actual, {exp_parsed}LL)) {{ tcStatus = \"Wrong Answer\"; }}")
            else:
                lines.append(f"            if (!checkEqual(actual, {exp_parsed})) {{ tcStatus = \"Wrong Answer\"; }}")
        elif isinstance(exp_parsed, str):
            lines.append(f"            if (!checkEqual(actual, std::string({json.dumps(exp_parsed)}))) {{ tcStatus = \"Wrong Answer\"; }}")
        elif isinstance(exp_parsed, dict):
            exp_lit = _py_to_cpp_literal(exp_parsed)
            lines.append(f"            if (!checkEqual(actual, {exp_lit})) {{ tcStatus = \"Wrong Answer\"; }}")

        lines.extend([
            "        } catch (const std::exception& ex) {",
            "            tcStatus = \"Runtime Error\";",
            "            tcError = ex.what();",
            "        } catch (...) {",
            "            tcStatus = \"Runtime Error\";",
            "            tcError = \"Unknown native exception\";",
            "        }",
            "        auto t1 = std::chrono::high_resolution_clock::now();",
            "        double durationMs = std::chrono::duration<double, std::milli>(t1 - t0).count();",
            "        if (tcStatus == \"Passed\") passed++;",
            "        else if (overallStatus == \"Accepted\") overallStatus = tcStatus;",
            "",
            "        if (" + str(idx) + " > 0) resultsJson << \",\";",
            "        resultsJson << \"{\";",
            f"        resultsJson << \"\\\"test_case_id\\\": \" << {tc_id} << \", \";",
            "        resultsJson << \"\\\"status\\\": \\\"\" << tcStatus << \"\\\", \";",
            f"        resultsJson << \"\\\"input_data\\\": \\\"\" << escape({json.dumps(raw_input if not is_hidden else '[Hidden Test Case]')}) << \"\\\", \";",
            f"        resultsJson << \"\\\"expected_output\\\": \\\"\" << escape({json.dumps(raw_exp if not is_hidden else '[Hidden Test Case]')}) << \"\\\", \";",
            f"        resultsJson << \"\\\"actual_output\\\": \\\"\" << ({('\"[Hidden]\"' if is_hidden else 'escape(actualStr)')}) << \"\\\", \";",
            "        resultsJson << \"\\\"stdout\\\": \\\"\\\", \";",
            "        resultsJson << \"\\\"execution_time_ms\\\": \" << durationMs << \", \";",
            f"        resultsJson << \"\\\"is_hidden\\\": \" << {str(is_hidden).lower()} << \", \";",
            "        resultsJson << \"\\\"error_message\\\": \" << (tcError.empty() ? \"null\" : \"\\\"\" + escape(tcError) + \"\\\"\");",
            "        resultsJson << \"}\";",
            "    }",
            ""
        ])

    lines.extend([
        "    resultsJson << \"]\";",
        "    auto endTotal = std::chrono::high_resolution_clock::now();",
        "    double totalMs = std::chrono::duration<double, std::milli>(endTotal - startTotal).count();",
        "    if (passed < total && overallStatus == \"Accepted\") overallStatus = \"Wrong Answer\";",
        "",
        "    std::cout << \"{\\\"status\\\": \\\"\" << overallStatus << \"\\\", \"",
        "              << \"\\\"passed_test_cases\\\": \" << passed << \", \"",
        "              << \"\\\"total_test_cases\\\": \" << total << \", \"",
        "              << \"\\\"execution_time_ms\\\": \" << totalMs << \", \"",
        "              << \"\\\"compile_error\\\": null, \"",
        "              << \"\\\"results\\\": \" << resultsJson.str() << \"}\" << std::endl;",
        "    return 0;",
        "}"
    ])
    return "\n".join(lines)


class CppCodeRunner:
    DEFAULT_COMPILE_TIMEOUT_SECONDS = 30.0

    @classmethod
    def execute(
        cls,
        code: str,
        test_cases: List[Dict[str, Any]],
        starter_code: Optional[str] = None,
        timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
        is_submission: bool = False,
        compile_timeout: Optional[float] = None
    ) -> Dict[str, Any]:
        cpp_compiler = shutil.which("g++") or shutil.which("clang++")
        active_tcs = test_cases if is_submission else [tc for tc in test_cases if not tc.get("is_hidden", False)]
        if not active_tcs:
            active_tcs = test_cases

        if not cpp_compiler:
            return {
                "status": "Compilation Error",
                "passed_test_cases": 0,
                "total_test_cases": len(active_tcs),
                "execution_time_ms": 0.0,
                "compile_error": "C++ compiler (g++/clang++) is not installed on this system.",
                "results": []
            }

        if not code or not code.strip():
            return {
                "status": "Compilation Error",
                "passed_test_cases": 0,
                "total_test_cases": len(active_tcs),
                "execution_time_ms": 0.0,
                "compile_error": "Empty C++ code submitted. Please write a solution.",
                "results": []
            }

        method_name = extract_cpp_method_name(code, starter_code) or "solve"
        param_types = extract_cpp_param_types(code, starter_code)
        start_time = time.perf_counter()

        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                sol_file = os.path.join(tmpdir, "Solution.cpp")
                with open(sol_file, "w", encoding="utf-8") as f:
                    f.write(code)

                driver_code = _generate_cpp_driver(method_name, active_tcs, param_types)
                driver_file = os.path.join(tmpdir, "Driver.cpp")
                with open(driver_file, "w", encoding="utf-8") as f:
                    f.write(driver_code)

                exe_name = "driver.exe" if sys.platform == "win32" else "driver"
                c_timeout = compile_timeout or cls.DEFAULT_COMPILE_TIMEOUT_SECONDS

                # 1. Compile C++ with g++ / clang++
                try:
                    c_proc = subprocess.run(
                        [cpp_compiler, "-std=c++17", "-O2", "Driver.cpp", "-o", exe_name],
                        cwd=tmpdir,
                        capture_output=True,
                        text=True,
                        timeout=c_timeout
                    )
                except subprocess.TimeoutExpired:
                    total_elapsed_ms = round((time.perf_counter() - start_time) * 1000.0, 2)
                    logger.warning(f"C++ compilation timed out after {c_timeout}s")
                    return {
                        "status": "Compilation Error",
                        "passed_test_cases": 0,
                        "total_test_cases": len(active_tcs),
                        "execution_time_ms": total_elapsed_ms,
                        "compile_error": f"Compilation timed out after {c_timeout} seconds.",
                        "results": []
                    }

                total_elapsed_ms = round((time.perf_counter() - start_time) * 1000.0, 2)

                if c_proc.returncode != 0:
                    return {
                        "status": "Compilation Error",
                        "passed_test_cases": 0,
                        "total_test_cases": len(active_tcs),
                        "execution_time_ms": total_elapsed_ms,
                        "compile_error": c_proc.stderr.strip() or "C++ compilation failed.",
                        "results": []
                    }

                # 2. Run the compiled executable
                exe_path = os.path.join(tmpdir, exe_name)
                try:
                    r_proc = subprocess.run(
                        [exe_path],
                        cwd=tmpdir,
                        capture_output=True,
                        text=True,
                        timeout=timeout_seconds
                    )
                except subprocess.TimeoutExpired:
                    total_elapsed_ms = round((time.perf_counter() - start_time) * 1000.0, 2)
                    logger.warning(f"C++ execution timed out after {timeout_seconds}s")
                    return {
                        "status": "Time Limit Exceeded",
                        "passed_test_cases": 0,
                        "total_test_cases": len(active_tcs),
                        "execution_time_ms": total_elapsed_ms,
                        "compile_error": f"Time Limit Exceeded: Execution took longer than {timeout_seconds} seconds.",
                        "results": [
                            {
                                "test_case_id": tc.get("id", idx + 1),
                                "status": "Time Limit Exceeded",
                                "input_data": tc.get("input_data", "") if not tc.get("is_hidden", False) else "[Hidden Test Case]",
                                "expected_output": str(tc.get("expected_output", "")) if not tc.get("is_hidden", False) else "[Hidden Test Case]",
                                "actual_output": "Time Limit Exceeded",
                                "stdout": "",
                                "execution_time_ms": round(timeout_seconds * 1000.0, 2),
                                "is_hidden": tc.get("is_hidden", False),
                                "error_message": "Execution timed out."
                            }
                            for idx, tc in enumerate(active_tcs)
                        ]
                    }

                total_elapsed_ms = round((time.perf_counter() - start_time) * 1000.0, 2)

                if r_proc.returncode != 0:
                    stderr_text = r_proc.stderr.strip() or "C++ execution failed with non-zero exit code."
                    return {
                        "status": "Runtime Error",
                        "passed_test_cases": 0,
                        "total_test_cases": len(active_tcs),
                        "execution_time_ms": total_elapsed_ms,
                        "compile_error": stderr_text,
                        "results": [
                            {
                                "test_case_id": tc.get("id", idx + 1),
                                "status": "Runtime Error",
                                "input_data": tc.get("input_data", "") if not tc.get("is_hidden", False) else "[Hidden Test Case]",
                                "expected_output": str(tc.get("expected_output", "")) if not tc.get("is_hidden", False) else "[Hidden Test Case]",
                                "actual_output": "Runtime Error",
                                "stdout": r_proc.stdout,
                                "execution_time_ms": total_elapsed_ms,
                                "is_hidden": tc.get("is_hidden", False),
                                "error_message": stderr_text
                            }
                            for idx, tc in enumerate(active_tcs)
                        ]
                    }

                stdout_text = r_proc.stdout.strip()
                try:
                    parsed = json.loads(stdout_text)
                    parsed["execution_time_ms"] = total_elapsed_ms
                    return parsed
                except Exception:
                    # Look for JSON payload in stdout lines
                    for out_line in reversed(stdout_text.splitlines()):
                        try:
                            candidate = json.loads(out_line.strip())
                            if "status" in candidate and "results" in candidate:
                                candidate["execution_time_ms"] = total_elapsed_ms
                                return candidate
                        except Exception:
                            continue

                    return {
                        "status": "Runtime Error",
                        "passed_test_cases": 0,
                        "total_test_cases": len(active_tcs),
                        "execution_time_ms": total_elapsed_ms,
                        "compile_error": f"Failed to parse C++ execution output: {stdout_text[:500]}",
                        "results": []
                    }
        except Exception as e:
            total_elapsed_ms = round((time.perf_counter() - start_time) * 1000.0, 2)
            return {
                "status": "Runtime Error",
                "passed_test_cases": 0,
                "total_test_cases": len(active_tcs),
                "execution_time_ms": total_elapsed_ms,
                "compile_error": f"C++ runner error: {str(e)}",
                "results": []
            }


# =====================================================================
# 5. UNIFIED DISPATCHER (CodeRunner)
# =====================================================================
class CodeRunner:
    SUPPORTED_LANGUAGES = ["python", "java", "cpp", "javascript"]

    @classmethod
    def execute(
        cls,
        code: str,
        test_cases: List[Dict[str, Any]],
        language: str = "python",
        starter_code: Optional[str] = None,
        timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
        is_submission: bool = False
    ) -> Dict[str, Any]:
        lang = (language or "python").lower().strip()
        if lang == "python":
            return PythonCodeRunner.execute(code, test_cases, starter_code, timeout_seconds, is_submission)
        elif lang == "javascript":
            return JavaScriptCodeRunner.execute(code, test_cases, starter_code, timeout_seconds, is_submission)
        elif lang == "java":
            return JavaCodeRunner.execute(code, test_cases, starter_code, timeout_seconds, is_submission)
        elif lang == "cpp":
            return CppCodeRunner.execute(code, test_cases, starter_code, timeout_seconds, is_submission)
        else:
            active_tcs = test_cases if is_submission else [tc for tc in test_cases if not tc.get("is_hidden", False)]
            return {
                "status": "Compilation Error",
                "passed_test_cases": 0,
                "total_test_cases": len(active_tcs),
                "execution_time_ms": 0.0,
                "compile_error": f"Unsupported language '{language}'. Supported languages: {', '.join(cls.SUPPORTED_LANGUAGES)}",
                "results": []
            }
