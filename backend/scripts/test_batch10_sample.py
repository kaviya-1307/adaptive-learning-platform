import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json

from app.core.database import SessionLocal
from app.models.problem import Problem
from app.engine.code_runner import JavaScriptCodeRunner, JavaCodeRunner, CppCodeRunner

db = SessionLocal()

def run_test(pid, js_code, js_starter, java_code, java_starter, cpp_code, cpp_starter):
    p = db.query(Problem).filter(Problem.id == pid).first()
    tcs = [{'id': tc.id, 'input_data': tc.input_data, 'expected_output': tc.expected_output, 'is_hidden': tc.is_hidden} for tc in p.test_cases]
    res_js = JavaScriptCodeRunner.execute(js_code, tcs, starter_code=js_starter, is_submission=True)
    res_java = JavaCodeRunner.execute(java_code, tcs, starter_code=java_starter, is_submission=True)
    res_cpp = CppCodeRunner.execute(cpp_code, tcs, starter_code=cpp_starter, is_submission=True)
    print(f"Problem {pid}:")
    print("  JS:  ", res_js.get("status"))
    print("  Java:", res_java.get("status"), res_java.get("compile_error") or "")
    print("  C++: ", res_cpp.get("status"), res_cpp.get("compile_error") or "")

# 531
run_test(
    531,
    "function extract_values(text) { let matches = text.match(/\"([^\"]*)\"/g); return matches ? matches.map(m => m.slice(1, -1)) : []; }",
    "function extract_values(text) { return []; }",
    """import java.util.*;
class Solution {
    public String[] extract_values(String text) {
        List<String> list = new ArrayList<>();
        int i = 0;
        while (i < text.length()) {
            int start = text.indexOf('"', i);
            if (start == -1) break;
            int end = text.indexOf('"', start + 1);
            if (end == -1) break;
            list.add(text.substring(start + 1, end));
            i = end + 1;
        }
        return list.toArray(new String[0]);
    }
}""",
    "class Solution { public String[] extract_values(String text) { return new String[]{}; } }",
    """#include <vector>
#include <string>
using namespace std;
class Solution {
public:
    vector<string> extract_values(const string& text) {
        vector<string> res;
        size_t i = 0;
        while (i < text.length()) {
            size_t start = text.find('"', i);
            if (start == string::npos) break;
            size_t end = text.find('"', start + 1);
            if (end == string::npos) break;
            res.push_back(text.substr(start + 1, end - start - 1));
            i = end + 1;
        }
        return res;
    }
};""",
    "#include <vector>\n#include <string>\nusing namespace std;\nclass Solution { public: vector<string> extract_values(const string& text); };"
)

# 536
run_test(
    536,
    "function empty_list(length) { return Array.from({length}, () => ({})); }",
    "function empty_list(length) { return []; }",
    """import java.util.*;
class Solution {
    public Object[] empty_list(int length) {
        Object[] res = new Object[length];
        for (int i = 0; i < length; i++) res[i] = new HashMap<String, Object>();
        return res;
    }
}""",
    "class Solution { public Object[] empty_list(int length) { return new Object[]{}; } }",
    """#include <vector>
#include <unordered_map>
#include <string>
using namespace std;
class Solution {
public:
    vector<unordered_map<string, string>> empty_list(int length) {
        return vector<unordered_map<string, string>>(length);
    }
};""",
    "#include <vector>\n#include <unordered_map>\n#include <string>\nusing namespace std;\nclass Solution { public: vector<unordered_map<string, string>> empty_list(int length); };"
)

# 537
run_test(
    537,
    "function sort_sublists(list1) { return list1.map(sub => [...sub].sort()); }",
    "function sort_sublists(list1) { return []; }",
    """import java.util.*;
class Solution {
    public String[][] sort_sublists(String[][] list1) {
        String[][] res = new String[list1.length][];
        for (int i = 0; i < list1.length; i++) {
            res[i] = list1[i].clone();
            Arrays.sort(res[i]);
        }
        return res;
    }
}""",
    "class Solution { public String[][] sort_sublists(String[][] list1) { return new String[][]{}; } }",
    """#include <vector>
#include <string>
#include <algorithm>
using namespace std;
class Solution {
public:
    vector<vector<string>> sort_sublists(vector<vector<string>> list1) {
        for (auto& sub : list1) sort(sub.begin(), sub.end());
        return list1;
    }
};""",
    "#include <vector>\n#include <string>\nusing namespace std;\nclass Solution { public: vector<vector<string>> sort_sublists(vector<vector<string>> list1); };"
)

# 549
run_test(
    549,
    "function find_adverbs(text) { let m = text.match(/\\w+ly/); return m ? `${m.index}-${m.index + m[0].length}: ${m[0]}` : ''; }",
    "function find_adverbs(text) { return ''; }",
    """class Solution {
    public String find_adverbs(String text) {
        int n = text.length();
        int i = 0;
        while (i < n) {
            while (i < n && !Character.isLetter(text.charAt(i))) i++;
            int start = i;
            while (i < n && Character.isLetter(text.charAt(i))) i++;
            int end = i;
            if (end > start) {
                String word = text.substring(start, end);
                if (word.endsWith("ly")) {
                    return start + "-" + end + ": " + word;
                }
            }
        }
        return "";
    }
}""",
    "class Solution { public String find_adverbs(String text) { return \"\"; } }",
    """#include <string>
#include <cctype>
using namespace std;
class Solution {
public:
    string find_adverbs(const string& text) {
        int n = text.length();
        int i = 0;
        while (i < n) {
            while (i < n && !isalpha((unsigned char)text[i])) i++;
            int start = i;
            while (i < n && isalpha((unsigned char)text[i])) i++;
            int end = i;
            if (end > start) {
                string word = text.substr(start, end - start);
                if (word.length() >= 2 && word.substr(word.length() - 2) == "ly") {
                    return to_string(start) + "-" + to_string(end) + ": " + word;
                }
            }
        }
        return "";
    }
};""",
    "#include <string>\nusing namespace std;\nclass Solution { public: string find_adverbs(const string& text); };"
)

# 556
run_test(
    556,
    "function removezero_ip(ip) { return ip.replace(/\\.[0]*/g, '.'); }",
    "function removezero_ip(ip) { return ''; }",
    """class Solution {
    public String removezero_ip(String ip) {
        String[] parts = ip.split("\\\\.");
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < parts.length; i++) {
            if (i > 0) sb.append(".");
            int j = 0;
            while (j < parts[i].length() - 1 && parts[i].charAt(j) == '0') j++;
            sb.append(parts[i].substring(j));
        }
        return sb.toString();
    }
}""",
    "class Solution { public String removezero_ip(String ip) { return \"\"; } }",
    """#include <string>
#include <sstream>
#include <vector>
using namespace std;
class Solution {
public:
    string removezero_ip(const string& ip) {
        stringstream ss(ip);
        string part;
        string res = "";
        bool first = true;
        while (getline(ss, part, '.')) {
            if (!first) res += ".";
            first = false;
            size_t j = 0;
            while (j + 1 < part.length() && part[j] == '0') j++;
            res += part.substr(j);
        }
        return res;
    }
};""",
    "#include <string>\nusing namespace std;\nclass Solution { public: string removezero_ip(const string& ip); };"
)

db.close()
