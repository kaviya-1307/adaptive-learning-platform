import sys
import json
sys.path.insert(0, '.')

from app.engine.code_runner import JavaCodeRunner

with open('scripts/batch13_dump.json') as f:
    probs = json.load(f)

p701 = [p for p in probs if p['id'] == 701][0]
tcs701 = [{'id': i+1, 'input_data': json.dumps(tc['input']), 'expected_output': json.dumps(tc['output']), 'is_hidden': False} for i, tc in enumerate(p701['test_cases'])]

java_code = """import java.util.*;

class Solution {
    public Object second_smallest(int[] numbers) {
        if (numbers.length < 2) return null;
        Set<Integer> uniq = new TreeSet<>();
        for (int x : numbers) uniq.add(x);
        if (uniq.size() < 2) return null;
        Iterator<Integer> it = uniq.iterator();
        it.next();
        return it.next();
    }
    public Object second_smallest(Object[] numbers) {
        if (numbers.length < 2) return null;
        Set<Double> uniq = new TreeSet<>();
        for (Object x : numbers) {
            if (x instanceof Number) uniq.add(((Number) x).doubleValue());
        }
        if (uniq.size() < 2) return null;
        Iterator<Double> it = uniq.iterator();
        it.next();
        return it.next();
    }
}"""

res = JavaCodeRunner.execute(java_code, tcs701, starter_code="class Solution {};", is_submission=True)
print("701 Java Status:", res.get('status'))
print("701 Compile error:", res.get('compile_error'))
for i, r in enumerate(res.get('results', [])):
    print(f"  TC {i+1}: status={r.get('status')}, actual={r.get('actual_output')}")
