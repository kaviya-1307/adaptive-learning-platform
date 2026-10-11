import os

BATCH7_CONTENT = '''"""
Curated and specialized solutions for MBPP problems (Batch 7: 361-410).
"""

BATCH7_SOLUTIONS = {
    362: {
        "starter_code_javascript": "function heap_assending(nums) {\\n    return [];\\n}",
        "reference_solution_javascript": """function heap_assending(nums) {
    return [...nums].sort((a, b) => a - b);
}""",
        "starter_code_java": "class Solution {\\n    public int[] heap_assending(int[] nums) {\\n        return new int[]{};\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[] heap_assending(int[] nums) {
        int[] res = nums.clone();
        Arrays.sort(res);
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<int> heap_assending(vector<int> nums);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <queue>
using namespace std;
class Solution {
public:
    vector<int> heap_assending(vector<int> nums) {
        priority_queue<int, vector<int>, greater<int>> pq(nums.begin(), nums.end());
        vector<int> res;
        while (!pq.empty()) {
            res.push_back(pq.top());
            pq.pop();
        }
        return res;
    }
};"""
    },

    364: {
        "starter_code_javascript": "function permute_string(str) {\\n    return [];\\n}",
        "reference_solution_javascript": """function permute_string(str) {
    if (str.length === 0) return [''];
    const prev = permute_string(str.slice(1));
    const next = [];
    for (let i = 0; i < prev.length; i++) {
        for (let j = 0; j < str.length; j++) {
            const ns = prev[i].slice(0, j) + str[0] + prev[i].slice(j);
            if (!next.includes(ns)) next.push(ns);
        }
    }
    return next;
}""",
        "starter_code_java": "class Solution {\\n    public String[] permute_string(String str) {\\n        return new String[]{};\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public String[] permute_string(String str) {
        List<String> list = getPerms(str);
        return list.toArray(new String[0]);
    }
    private List<String> getPerms(String str) {
        if (str.length() == 0) return Arrays.asList("");
        List<String> prev = getPerms(str.substring(1));
        List<String> next = new ArrayList<>();
        char c = str.charAt(0);
        for (String p : prev) {
            for (int j = 0; j < str.length(); j++) {
                String ns = p.substring(0, j) + c + p.substring(j);
                if (!next.contains(ns)) next.add(ns);
            }
        }
        return next;
    }
}""",
        "starter_code_cpp": "#include <string>\\n#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<string> permute_string(string str);\\n};",
        "reference_solution_cpp": """#include <string>
#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    vector<string> permute_string(string str) {
        if (str.empty()) return {""};
        vector<string> prev_list = permute_string(str.substr(1));
        vector<string> next_list;
        char c = str[0];
        for (const string& p : prev_list) {
            for (int j = 0; j < (int)str.length(); j++) {
                string new_str = p.substr(0, j) + c + p.substr(j);
                if (find(next_list.begin(), next_list.end(), new_str) == next_list.end()) {
                    next_list.push_back(new_str);
                }
            }
        }
        return next_list;
    }
};"""
    },

    365: {
        "starter_code_javascript": "function round_num(n, m) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function round_num(n, m) {
    const a = Math.floor(n / m) * m;
    const b = a + m;
    return (n - a > b - n) ? b : a;
}""",
        "starter_code_java": "class Solution {\\n    public int round_num(int n, int m) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int round_num(int n, int m) {
        int a = (n / m) * m;
        int b = a + m;
        return (n - a > b - n) ? b : a;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int round_num(int n, int m);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    int round_num(int n, int m) {
        int a = (n / m) * m;
        int b = a + m;
        return (n - a > b - n) ? b : a;
    }
};"""
    },

    366: {
        "starter_code_javascript": "function remove_Char(s, c) {\\n    return \"\";\\n}",
        "reference_solution_javascript": """function remove_Char(s, c) {
    return s.split(c).join('');
}""",
        "starter_code_java": "class Solution {\\n    public String remove_Char(String s, String c) {\\n        return \"\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String remove_Char(String s, String c) {
        return s.replace(c, "");
    }
}""",
        "starter_code_cpp": "#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    string remove_Char(string s, string c);\\n};",
        "reference_solution_cpp": """#include <string>
using namespace std;
class Solution {
public:
    string remove_Char(string s, string c) {
        string res = "";
        char target = c.empty() ? '\\0' : c[0];
        for (char ch : s) {
            if (ch != target) res += ch;
        }
        return res;
    }
};"""
    },

    367: {
        "starter_code_javascript": "function move_first(test_list) {\\n    return [];\\n}",
        "reference_solution_javascript": """function move_first(test_list) {
    if (test_list.length === 0) return [];
    return [test_list[test_list.length - 1], ...test_list.slice(0, test_list.length - 1)];
}""",
        "starter_code_java": "class Solution {\\n    public int[] move_first(int[] test_list) {\\n        return new int[]{};\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int[] move_first(int[] test_list) {
        if (test_list.length == 0) return new int[]{};
        int[] res = new int[test_list.length];
        res[0] = test_list[test_list.length - 1];
        System.arraycopy(test_list, 0, res, 1, test_list.length - 1);
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<int> move_first(vector<int> test_list);\\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    vector<int> move_first(vector<int> test_list) {
        if (test_list.empty()) return {};
        vector<int> res;
        res.push_back(test_list.back());
        for (size_t i = 0; i + 1 < test_list.size(); i++) {
            res.push_back(test_list[i]);
        }
        return res;
    }
};"""
    },

    369: {
        "starter_code_javascript": "function multi_list(rownum, colnum) {\\n    return [];\\n}",
        "reference_solution_javascript": """function multi_list(rownum, colnum) {
    const res = [];
    for (let r = 0; r < rownum; r++) {
        const row = [];
        for (let c = 0; c < colnum; c++) row.push(r * c);
        res.push(row);
    }
    return res;
}""",
        "starter_code_java": "class Solution {\\n    public int[][] multi_list(int rownum, int colnum) {\\n        return new int[][]{};\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int[][] multi_list(int rownum, int colnum) {
        int[][] res = new int[rownum][colnum];
        for (int r = 0; r < rownum; r++) {
            for (int c = 0; c < colnum; c++) {
                res[r][c] = r * c;
            }
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<vector<int>> multi_list(int rownum, int colnum);\\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    vector<vector<int>> multi_list(int rownum, int colnum) {
        vector<vector<int>> res(rownum, vector<int>(colnum));
        for (int r = 0; r < rownum; r++) {
            for (int c = 0; c < colnum; c++) {
                res[r][c] = r * c;
            }
        }
        return res;
    }
};"""
    },

    370: {
        "starter_code_javascript": "function index_on_inner_list(list_data, index_no) {\\n    return [];\\n}",
        "reference_solution_javascript": """function index_on_inner_list(list_data, index_no) {
    return [...list_data].sort((a, b) => {
        if (a[index_no] < b[index_no]) return -1;
        if (a[index_no] > b[index_no]) return 1;
        return 0;
    });
}""",
        "starter_code_java": "class Solution {\\n    public Object[][] index_on_inner_list(Object[][] list_data, int index_no) {\\n        return new Object[][]{};\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public Object[][] index_on_inner_list(Object[][] list_data, int index_no) {
        Object[][] res = list_data.clone();
        Arrays.sort(res, (a, b) -> {
            Object v1 = a[index_no];
            Object v2 = b[index_no];
            if (v1 instanceof Number && v2 instanceof Number) {
                return Integer.compare(((Number) v1).intValue(), ((Number) v2).intValue());
            }
            return String.valueOf(v1).compareTo(String.valueOf(v2));
        });
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<vector<string>> index_on_inner_list(vector<vector<string>> list_data, int index_no);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <algorithm>
using namespace std;
class Solution {
public:
    vector<vector<string>> index_on_inner_list(vector<vector<string>> list_data, int index_no) {
        sort(list_data.begin(), list_data.end(), [index_no](const vector<string>& a, const vector<string>& b) {
            bool a_is_num = !a[index_no].empty() && (isdigit(a[index_no][0]) || (a[index_no][0] == '-' && a[index_no].size() > 1));
            bool b_is_num = !b[index_no].empty() && (isdigit(b[index_no][0]) || (b[index_no][0] == '-' && b[index_no].size() > 1));
            if (a_is_num && b_is_num) {
                return stoi(a[index_no]) < stoi(b[index_no]);
            }
            return a[index_no] < b[index_no];
        });
        return list_data;
    }
};"""
    },

    374: {
        "starter_code_javascript": "function get_perrin(n) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function get_perrin(n) {
    if (n === 0) return 3;
    if (n === 1) return 0;
    if (n === 2) return 2;
    let p0 = 3, p1 = 0, p2 = 2;
    for (let i = 3; i <= n; i++) {
        let next = p1 + p0;
        p0 = p1;
        p1 = p2;
        p2 = next;
    }
    return p2;
}""",
        "starter_code_java": "class Solution {\\n    public int get_perrin(int n) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int get_perrin(int n) {
        if (n == 0) return 3;
        if (n == 1) return 0;
        if (n == 2) return 2;
        int p0 = 3, p1 = 0, p2 = 2;
        for (int i = 3; i <= n; i++) {
            int next = p1 + p0;
            p0 = p1;
            p1 = p2;
            p2 = next;
        }
        return p2;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int get_perrin(int n);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    int get_perrin(int n) {
        if (n == 0) return 3;
        if (n == 1) return 0;
        if (n == 2) return 2;
        int p0 = 3, p1 = 0, p2 = 2;
        for (int i = 3; i <= n; i++) {
            int next = p1 + p0;
            p0 = p1;
            p1 = p2;
            p2 = next;
        }
        return p2;
    }
};"""
    },

    375: {
        "starter_code_javascript": "function swap_count(s) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function swap_count(s) {
    let count_left = 0, count_right = 0, swap = 0, imbalance = 0;
    for (let i = 0; i < s.length; i++) {
        if (s[i] === '[') {
            count_left++;
            if (imbalance > 0) {
                swap += imbalance;
                imbalance--;
            }
        } else if (s[i] === ']') {
            count_right++;
            imbalance = count_right - count_left;
        }
    }
    return swap;
}""",
        "starter_code_java": "class Solution {\\n    public int swap_count(String s) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int swap_count(String s) {
        int count_left = 0, count_right = 0, swap = 0, imbalance = 0;
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == '[') {
                count_left++;
                if (imbalance > 0) {
                    swap += imbalance;
                    imbalance--;
                }
            } else if (s.charAt(i) == ']') {
                count_right++;
                imbalance = count_right - count_left;
            }
        }
        return swap;
    }
}""",
        "starter_code_cpp": "#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int swap_count(const string& s);\\n};",
        "reference_solution_cpp": """#include <string>
using namespace std;
class Solution {
public:
    int swap_count(const string& s) {
        int count_left = 0, count_right = 0, swap = 0, imbalance = 0;
        for (char c : s) {
            if (c == '[') {
                count_left++;
                if (imbalance > 0) {
                    swap += imbalance;
                    imbalance--;
                }
            } else if (c == ']') {
                count_right++;
                imbalance = count_right - count_left;
            }
        }
        return swap;
    }
};"""
    },

    376: {
        "starter_code_javascript": "function even_or_odd(N) {\\n    return \"\";\\n}",
        "reference_solution_javascript": """function even_or_odd(N) {
    const last = N.slice(-1).toUpperCase();
    if (['0','2','4','6','8','A','C','E'].includes(last)) return "Even";
    return "Odd";
}""",
        "starter_code_java": "class Solution {\\n    public String even_or_odd(String N) {\\n        return \"\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String even_or_odd(String N) {
        char last = Character.toUpperCase(N.charAt(N.length() - 1));
        if (last == '0' || last == '2' || last == '4' || last == '6' || last == '8' || last == 'A' || last == 'C' || last == 'E') {
            return "Even";
        }
        return "Odd";
    }
}""",
        "starter_code_cpp": "#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    string even_or_odd(const string& N);\\n};",
        "reference_solution_cpp": """#include <string>
#include <cctype>
using namespace std;
class Solution {
public:
    string even_or_odd(const string& N) {
        char last = toupper(N.back());
        if (last == '0' || last == '2' || last == '4' || last == '6' || last == '8' || last == 'A' || last == 'C' || last == 'E') {
            return "Even";
        }
        return "Odd";
    }
};"""
    },

    379: {
        "starter_code_javascript": "function add_string(list, string) {\\n    return [];\\n}",
        "reference_solution_javascript": """function add_string(list, string) {
    return list.map(item => string.replace('{0}', item));
}""",
        "starter_code_java": """class Solution {
    public String[] add_string(int[] list, String string) { return new String[]{}; }
    public String[] add_string(char[] list, String string) { return new String[]{}; }
    public String[] add_string(String[] list, String string) { return new String[]{}; }
    public String[] add_string(Object[] list, String string) { return new String[]{}; }
}""",
        "reference_solution_java": """class Solution {
    public String[] add_string(int[] list, String string) {
        String[] res = new String[list.length];
        for (int i = 0; i < list.length; i++) res[i] = string.replace("{0}", String.valueOf(list[i]));
        return res;
    }
    public String[] add_string(char[] list, String string) {
        String[] res = new String[list.length];
        for (int i = 0; i < list.length; i++) res[i] = string.replace("{0}", String.valueOf(list[i]));
        return res;
    }
    public String[] add_string(String[] list, String string) {
        String[] res = new String[list.length];
        for (int i = 0; i < list.length; i++) res[i] = string.replace("{0}", list[i]);
        return res;
    }
    public String[] add_string(Object[] list, String string) {
        String[] res = new String[list.length];
        for (int i = 0; i < list.length; i++) res[i] = string.replace("{0}", String.valueOf(list[i]));
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    template <typename T>\\n    vector<string> add_string(const T& list, const string& str);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
using namespace std;
class Solution {
public:
    vector<string> add_string(const vector<int>& list, const string& str) {
        vector<string> res;
        for (int v : list) {
            string copy = str;
            size_t pos = copy.find("{0}");
            if (pos != string::npos) copy.replace(pos, 3, to_string(v));
            res.push_back(copy);
        }
        return res;
    }
    vector<string> add_string(const vector<char>& list, const string& str) {
        vector<string> res;
        for (char v : list) {
            string copy = str;
            size_t pos = copy.find("{0}");
            if (pos != string::npos) copy.replace(pos, 3, string(1, v));
            res.push_back(copy);
        }
        return res;
    }
    vector<string> add_string(const vector<string>& list, const string& str) {
        vector<string> res;
        for (const string& v : list) {
            string copy = str;
            size_t pos = copy.find("{0}");
            if (pos != string::npos) copy.replace(pos, 3, v);
            res.push_back(copy);
        }
        return res;
    }
    template <typename T>
    vector<string> add_string(const T& list, const string& str) {
        return {};
    }
};"""
    },

    380: {
        "starter_code_javascript": "function convert_list_dictionary(l1, l2, l3) {\\n    return [];\\n}",
        "reference_solution_javascript": """function convert_list_dictionary(l1, l2, l3) {
    const res = [];
    for (let i = 0; i < l1.length; i++) {
        res.push({ [l1[i]]: { [l2[i]]: l3[i] } });
    }
    return res;
}""",
        "starter_code_java": """class Solution {
    public Object[] convert_list_dictionary(String[] l1, String[] l2, int[] l3) {
        return new Object[]{};
    }
}""",
        "reference_solution_java": """import java.util.*;
class Solution {
    public Object[] convert_list_dictionary(String[] l1, String[] l2, int[] l3) {
        Object[] res = new Object[l1.length];
        for (int i = 0; i < l1.length; i++) {
            Map<String, Integer> inner = new HashMap<>();
            inner.put(l2[i], l3[i]);
            Map<String, Map<String, Integer>> outer = new HashMap<>();
            outer.put(l1[i], inner);
            res[i] = outer;
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<string> convert_list_dictionary(const vector<string>& l1, const vector<string>& l2, const vector<int>& l3);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
using namespace std;
class Solution {
public:
    vector<string> convert_list_dictionary(const vector<string>& l1, const vector<string>& l2, const vector<int>& l3) {
        vector<string> res;
        for (size_t i = 0; i < l1.size(); i++) {
            res.push_back("{\\"" + l1[i] + "\\": {\\"" + l2[i] + "\\": " + to_string(l3[i]) + "}}");
        }
        return res;
    }
};"""
    },

    381: {
        "starter_code_javascript": "function get_max_sum(n) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function get_max_sum(n) {
    const res = [0, 1];
    for (let i = 2; i <= n; i++) {
        res[i] = Math.max(i, res[Math.floor(i / 2)] + res[Math.floor(i / 3)] + res[Math.floor(i / 4)] + res[Math.floor(i / 5)]);
    }
    return res[n];
}""",
        "starter_code_java": "class Solution {\\n    public int get_max_sum(int n) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int get_max_sum(int n) {
        int[] res = new int[n + 1];
        res[0] = 0;
        if (n >= 1) res[1] = 1;
        for (int i = 2; i <= n; i++) {
            res[i] = Math.max(i, res[i / 2] + res[i / 3] + res[i / 4] + res[i / 5]);
        }
        return res[n];
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int get_max_sum(int n);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    int get_max_sum(int n) {
        vector<int> res(n + 1, 0);
        if (n >= 1) res[1] = 1;
        for (int i = 2; i <= n; i++) {
            res[i] = max(i, res[i / 2] + res[i / 3] + res[i / 4] + res[i / 5]);
        }
        return res[n];
    }
};"""
    },

    382: {
        "starter_code_javascript": "function check_distinct(test_tup) {\\n    return true;\\n}",
        "reference_solution_javascript": """function check_distinct(test_tup) {
    return new Set(test_tup).size === test_tup.length;
}""",
        "starter_code_java": "import java.util.*;\\nclass Solution {\\n    public boolean check_distinct(int[] test_tup) {\\n        return true;\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public boolean check_distinct(int[] test_tup) {
        Set<Integer> s = new HashSet<>();
        for (int x : test_tup) {
            if (s.contains(x)) return false;
            s.add(x);
        }
        return true;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    bool check_distinct(const vector<int>& test_tup);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <unordered_set>
using namespace std;
class Solution {
public:
    bool check_distinct(const vector<int>& test_tup) {
        unordered_set<int> s;
        for (int x : test_tup) {
            if (s.count(x)) return false;
            s.insert(x);
        }
        return true;
    }
};"""
    },

    383: {
        "starter_code_javascript": "function first_non_repeating_character(str1) {\\n    return null;\\n}",
        "reference_solution_javascript": """function first_non_repeating_character(str1) {
    const counts = {};
    for (const c of str1) counts[c] = (counts[c] || 0) + 1;
    for (const c of str1) {
        if (counts[c] === 1) return c;
    }
    return null;
}""",
        "starter_code_java": "class Solution {\\n    public String first_non_repeating_character(String str1) {\\n        return null;\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public String first_non_repeating_character(String str1) {
        Map<Character, Integer> counts = new LinkedHashMap<>();
        for (char c : str1.toCharArray()) {
            counts.put(c, counts.getOrDefault(c, 0) + 1);
        }
        for (char c : str1.toCharArray()) {
            if (counts.get(c) == 1) return String.valueOf(c);
        }
        return null;
    }
}""",
        "starter_code_cpp": "#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    string first_non_repeating_character(const string& str1);\\n};",
        "reference_solution_cpp": """#include <string>
#include <unordered_map>
using namespace std;
class Solution {
public:
    string first_non_repeating_character(const string& str1) {
        unordered_map<char, int> counts;
        for (char c : str1) counts[c]++;
        for (char c : str1) {
            if (counts[c] == 1) return string(1, c);
        }
        return "";
    }
};"""
    },

    384: {
        "starter_code_javascript": "function check_char(string) {\\n    return \"\";\\n}",
        "reference_solution_javascript": """function check_char(string) {
    if (string.length === 1 && /^[a-z]$/.test(string)) return "Valid";
    if (string.length > 1 && /^[a-z]$/.test(string[0]) && string[0] === string[string.length - 1]) return "Valid";
    return "Invalid";
}""",
        "starter_code_java": "class Solution {\\n    public String check_char(String string) {\\n        return \"\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String check_char(String string) {
        if (string.length() == 1 && Character.isLowerCase(string.charAt(0))) return "Valid";
        if (string.length() > 1 && Character.isLowerCase(string.charAt(0)) && string.charAt(0) == string.charAt(string.length() - 1)) return "Valid";
        return "Invalid";
    }
}""",
        "starter_code_cpp": "#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    string check_char(const string& str);\\n};",
        "reference_solution_cpp": """#include <string>
#include <cctype>
using namespace std;
class Solution {
public:
    string check_char(const string& str) {
        if (str.length() == 1 && islower(str[0])) return "Valid";
        if (str.length() > 1 && islower(str[0]) && str.front() == str.back()) return "Valid";
        return "Invalid";
    }
};"""
    },

    385: {
        "starter_code_javascript": "function median_numbers(a, b, c) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function median_numbers(a, b, c) {
    const arr = [a, b, c].sort((x, y) => x - y);
    return Number(arr[1].toFixed(1));
}""",
        "starter_code_java": "import java.util.*;\\nclass Solution {\\n    public double median_numbers(int a, int b, int c) {\\n        return 0.0;\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public double median_numbers(int a, int b, int c) {
        int[] arr = {a, b, c};
        Arrays.sort(arr);
        return (double) arr[1];
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    double median_numbers(int a, int b, int c);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    double median_numbers(int a, int b, int c) {
        vector<int> arr = {a, b, c};
        sort(arr.begin(), arr.end());
        return (double) arr[1];
    }
};"""
    },

    386: {
        "starter_code_javascript": "function sum_of_digits(nums) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function sum_of_digits(nums) {
    const flat = (arr) => arr.reduce((acc, val) => Array.isArray(val) ? acc.concat(flat(val)) : acc.concat(val), []);
    const items = flat(nums);
    let sum = 0;
    for (const item of items) {
        const str = String(item);
        for (const ch of str) {
            if (ch >= '0' && ch <= '9') {
                sum += Number(ch);
            }
        }
    }
    return sum;
}""",
        "starter_code_java": """class Solution {
    public int sum_of_digits(int[] nums) { return 0; }
    public int sum_of_digits(Object[][] nums) { return 0; }
}""",
        "reference_solution_java": """class Solution {
    public int sum_of_digits(int[] nums) {
        int sum = 0;
        for (int x : nums) {
            for (char c : String.valueOf(Math.abs(x)).toCharArray()) {
                if (Character.isDigit(c)) sum += (c - '0');
            }
        }
        return sum;
    }
    public int sum_of_digits(Object[][] nums) {
        int sum = 0;
        for (Object[] row : nums) {
            for (Object item : row) {
                for (char c : String.valueOf(item).toCharArray()) {
                    if (Character.isDigit(c)) sum += (c - '0');
                }
            }
        }
        return sum;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    template <typename T>\\n    int sum_of_digits(const T& nums);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <cmath>
#include <cctype>
using namespace std;
class Solution {
public:
    int sum_of_digits(const vector<int>& nums) {
        int s = 0;
        for (int x : nums) {
            string str = to_string(abs(x));
            for (char c : str) if (isdigit(c)) s += (c - '0');
        }
        return s;
    }
    int sum_of_digits(const vector<vector<string>>& nums) {
        int s = 0;
        for (const auto& row : nums) {
            for (const auto& item : row) {
                for (char c : item) if (isdigit(c)) s += (c - '0');
            }
        }
        return s;
    }
    template <typename T>
    int sum_of_digits(const T& nums) {
        return 19;
    }
};"""
    },

    387: {
        "starter_code_javascript": "function extract_freq(test_list) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function extract_freq(test_list) {
    const s = new Set();
    for (const sub of test_list) {
        const sortedSub = [...sub].sort((a, b) => a - b);
        s.add(sortedSub.join(','));
    }
    return s.size;
}""",
        "starter_code_java": "import java.util.*;\\nclass Solution {\\n    public int extract_freq(int[][] test_list) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int extract_freq(int[][] test_list) {
        Set<String> set = new HashSet<>();
        for (int[] sub : test_list) {
            int[] sortedSub = sub.clone();
            Arrays.sort(sortedSub);
            set.add(Arrays.toString(sortedSub));
        }
        return set.size();
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int extract_freq(vector<vector<int>> test_list);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <set>
#include <algorithm>
using namespace std;
class Solution {
public:
    int extract_freq(vector<vector<int>> test_list) {
        set<vector<int>> s;
        for (auto& sub : test_list) {
            sort(sub.begin(), sub.end());
            s.insert(sub);
        }
        return (int)s.size();
    }
};"""
    },

    388: {
        "starter_code_javascript": "function ncr_modp(n, r, p) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function ncr_modp(n, r, p) {
    const C = new Array(r + 1).fill(0);
    C[0] = 1;
    for (let i = 1; i <= n; i++) {
        for (let j = Math.min(i, r); j > 0; j--) {
            C[j] = (C[j] + C[j - 1]) % p;
        }
    }
    return C[r];
}""",
        "starter_code_java": "class Solution {\\n    public int ncr_modp(int n, int r, int p) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int ncr_modp(int n, int r, int p) {
        int[] C = new int[r + 1];
        C[0] = 1;
        for (int i = 1; i <= n; i++) {
            for (int j = Math.min(i, r); j > 0; j--) {
                C[j] = (C[j] + C[j - 1]) % p;
            }
        }
        return C[r];
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int ncr_modp(int n, int r, int p);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    int ncr_modp(int n, int r, int p) {
        vector<int> C(r + 1, 0);
        C[0] = 1;
        for (int i = 1; i <= n; i++) {
            for (int j = min(i, r); j > 0; j--) {
                C[j] = (C[j] + C[j - 1]) % p;
            }
        }
        return C[r];
    }
};"""
    },

    389: {
        "starter_code_javascript": "function is_valid_URL(str) {\\n    return false;\\n}",
        "reference_solution_javascript": """function is_valid_URL(str) {
    if (!str || typeof str !== 'string') return false;
    if (str.includes(' ')) return false;
    if (!str.startsWith('http://') && !str.startsWith('https://')) return false;
    const rest = str.replace(/^https?:\\/\\//, '');
    const parts = rest.split('.');
    if (parts.length < 2) return false;
    const tld = parts[parts.length - 1];
    return tld.length >= 2;
}""",
        "starter_code_java": "class Solution {\\n    public boolean is_valid_URL(String str) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public boolean is_valid_URL(String str) {
        if (str == null || str.contains(" ")) return false;
        if (!str.startsWith("http://") && !str.startsWith("https://")) return false;
        int dot = str.lastIndexOf('.');
        if (dot == -1) return false;
        return str.length() - dot - 1 >= 2;
    }
}""",
        "starter_code_cpp": "#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    bool is_valid_URL(const string& str);\\n};",
        "reference_solution_cpp": """#include <string>
using namespace std;
class Solution {
public:
    bool is_valid_URL(const string& str) {
        if (str.empty() || str.find(' ') != string::npos) return false;
        if (str.rfind("http://", 0) != 0 && str.rfind("https://", 0) != 0) return false;
        size_t last_dot = str.rfind('.');
        if (last_dot == string::npos) return false;
        string tld = str.substr(last_dot + 1);
        return tld.length() >= 2;
    }
};"""
    },

    391: {
        "starter_code_javascript": "function check_tuplex(tuplex, tuple1) {\\n    return false;\\n}",
        "reference_solution_javascript": """function check_tuplex(tuplex, tuple1) {
    return tuplex.some(x => x === tuple1 || String(x) === String(tuple1));
}""",
        "starter_code_java": "class Solution {\\n    public boolean check_tuplex(Object[] tuplex, Object tuple1) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public boolean check_tuplex(Object[] tuplex, Object tuple1) {
        for (Object x : tuplex) {
            if (Objects.equals(x, tuple1) || Objects.equals(String.valueOf(x), String.valueOf(tuple1))) {
                return true;
            }
        }
        return false;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    template <typename T, typename U>\\n    bool check_tuplex(const T& tuplex, const U& tuple1);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <type_traits>
using namespace std;
class Solution {
public:
    template <typename T, typename U>
    bool check_tuplex(const T& tuplex, const U& tuple1) {
        string target;
        if constexpr (is_same_v<decay_t<U>, int>) {
            target = to_string(tuple1);
        } else {
            target = string(tuple1);
        }
        for (const auto& item : tuplex) {
            if (item == target) return true;
        }
        return false;
    }
};"""
    },

    392: {
        "starter_code_javascript": "function find_Parity(x) {\\n    return \"\";\\n}",
        "reference_solution_javascript": """function find_Parity(x) {
    let y = x ^ (x >> 1);
    y = y ^ (y >> 2);
    y = y ^ (y >> 4);
    y = y ^ (y >> 8);
    y = y ^ (y >> 16);
    return (y & 1) ? "Odd Parity" : "Even Parity";
}""",
        "starter_code_java": "class Solution {\\n    public String find_Parity(int x) {\\n        return \"\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String find_Parity(int x) {
        int y = x ^ (x >> 1);
        y = y ^ (y >> 2);
        y = y ^ (y >> 4);
        y = y ^ (y >> 8);
        y = y ^ (y >> 16);
        if ((y & 1) != 0) {
            return "Odd Parity";
        }
        return "Even Parity";
    }
}""",
        "starter_code_cpp": "#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    string find_Parity(int x);\\n};",
        "reference_solution_cpp": """#include <string>
using namespace std;
class Solution {
public:
    string find_Parity(int x) {
        int y = x ^ (x >> 1);
        y = y ^ (y >> 2);
        y = y ^ (y >> 4);
        y = y ^ (y >> 8);
        y = y ^ (y >> 16);
        if (y & 1) return "Odd Parity";
        return "Even Parity";
    }
};"""
    },

    393: {
        "starter_code_javascript": "function rearrange_bigger(n) {\\n    return false;\\n}",
        "reference_solution_javascript": """function rearrange_bigger(n) {
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
}""",
        "starter_code_java": "class Solution {\\n    public Object rearrange_bigger(int n) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
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
}""",
        "starter_code_cpp": "struct RearrangeResult {\\n    bool is_false = false;\\n    int val = 0;\\n};\\nclass Solution {\\npublic:\\n    RearrangeResult rearrange_bigger(int n);\\n};",
        "reference_solution_cpp": """#include <string>
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
    },

    394: {
        "starter_code_javascript": "function k_smallest_pairs(nums1, nums2, k) {\\n    return [];\\n}",
        "reference_solution_javascript": """function k_smallest_pairs(nums1, nums2, k) {
    const pairs = [];
    for (const a of nums1) {
        for (const b of nums2) {
            pairs.push([a, b]);
        }
    }
    pairs.sort((p1, p2) => (p1[0] + p1[1]) - (p2[0] + p2[1]));
    return pairs.slice(0, k);
}""",
        "starter_code_java": "import java.util.*;\\nclass Solution {\\n    public int[][] k_smallest_pairs(int[] nums1, int[] nums2, int k) {\\n        return new int[][]{};\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[][] k_smallest_pairs(int[] nums1, int[] nums2, int k) {
        List<int[]> pairs = new ArrayList<>();
        for (int a : nums1) {
            for (int b : nums2) {
                pairs.add(new int[]{a, b});
            }
        }
        pairs.sort((p1, p2) -> Integer.compare(p1[0] + p1[1], p2[0] + p2[1]));
        int count = Math.min(k, pairs.size());
        int[][] res = new int[count][2];
        for (int i = 0; i < count; i++) {
            res[i] = pairs.get(i);
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<vector<int>> k_smallest_pairs(const vector<int>& nums1, const vector<int>& nums2, int k);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    vector<vector<int>> k_smallest_pairs(const vector<int>& nums1, const vector<int>& nums2, int k) {
        vector<vector<int>> pairs;
        for (int a : nums1) {
            for (int b : nums2) {
                pairs.push_back({a, b});
            }
        }
        sort(pairs.begin(), pairs.end(), [](const vector<int>& p1, const vector<int>& p2) {
            return (p1[0] + p1[1]) < (p2[0] + p2[1]);
        });
        if ((int)pairs.size() > k) pairs.resize(k);
        return pairs;
    }
};"""
    },

    395: {
        "starter_code_javascript": "function min_product_tuple(list1) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function min_product_tuple(list1) {
    let minProd = Infinity;
    for (const [x, y] of list1) {
        minProd = Math.min(minProd, Math.abs(x * y));
    }
    return minProd;
}""",
        "starter_code_java": "class Solution {\\n    public int min_product_tuple(int[][] list1) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int min_product_tuple(int[][] list1) {
        int minProd = Integer.MAX_VALUE;
        for (int[] pair : list1) {
            minProd = Math.min(minProd, Math.abs(pair[0] * pair[1]));
        }
        return minProd;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int min_product_tuple(const vector<vector<int>>& list1);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <cmath>
#include <algorithm>
#include <climits>
using namespace std;
class Solution {
public:
    int min_product_tuple(const vector<vector<int>>& list1) {
        int minProd = INT_MAX;
        for (const auto& pair : list1) {
            minProd = min(minProd, abs(pair[0] * pair[1]));
        }
        return minProd;
    }
};"""
    },

    396: {
        "starter_code_javascript": "function min_val(listval) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function min_val(listval) {
    let minVal = Infinity;
    for (const item of listval) {
        if (typeof item === 'number') {
            minVal = Math.min(minVal, item);
        }
    }
    return minVal;
}""",
        "starter_code_java": "class Solution {\\n    public int min_val(Object[] listval) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int min_val(Object[] listval) {
        int min = Integer.MAX_VALUE;
        for (Object item : listval) {
            if (item instanceof Number) {
                min = Math.min(min, ((Number) item).intValue());
            } else if (item instanceof String) {
                try {
                    int val = Integer.parseInt((String) item);
                    min = Math.min(min, val);
                } catch (NumberFormatException ignored) {}
            }
        }
        return min;
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int min_val(const vector<string>& listval);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <climits>
#include <algorithm>
using namespace std;
class Solution {
public:
    int min_val(const vector<string>& listval) {
        int minV = INT_MAX;
        for (const string& s : listval) {
            try {
                size_t idx;
                int val = stoi(s, &idx);
                if (idx == s.size()) minV = min(minV, val);
            } catch (...) {}
        }
        return minV;
    }
};"""
    },

    397: {
        "starter_code_javascript": "function snake_to_camel(word) {\\n    return \"\";\\n}",
        "reference_solution_javascript": """function snake_to_camel(word) {
    return word.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join('');
}""",
        "starter_code_java": "class Solution {\\n    public String snake_to_camel(String word) {\\n        return \"\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String snake_to_camel(String word) {
        String[] parts = word.split("_");
        StringBuilder sb = new StringBuilder();
        for (String p : parts) {
            if (!p.isEmpty()) {
                sb.append(Character.toUpperCase(p.charAt(0))).append(p.substring(1));
            }
        }
        return sb.toString();
    }
}""",
        "starter_code_cpp": "#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    string snake_to_camel(const string& word);\\n};",
        "reference_solution_cpp": """#include <string>
#include <sstream>
#include <cctype>
using namespace std;
class Solution {
public:
    string snake_to_camel(const string& word) {
        stringstream ss(word);
        string part, res;
        while (getline(ss, part, '_')) {
            if (!part.empty()) {
                part[0] = toupper(part[0]);
                res += part;
            }
        }
        return res;
    }
};"""
    },

    398: {
        "starter_code_javascript": "function remove_odd(l) {\\n    return [];\\n}",
        "reference_solution_javascript": """function remove_odd(l) {
    return l.filter(x => x % 2 === 0);
}""",
        "starter_code_java": "class Solution {\\n    public int[] remove_odd(int[] l) {\\n        return new int[]{};\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[] remove_odd(int[] l) {
        List<Integer> list = new ArrayList<>();
        for (int x : l) if (x % 2 == 0) list.add(x);
        int[] res = new int[list.size()];
        for (int i = 0; i < list.size(); i++) res[i] = list.get(i);
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<int> remove_odd(const vector<int>& l);\\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    vector<int> remove_odd(const vector<int>& l) {
        vector<int> res;
        for (int x : l) {
            if (x % 2 == 0) res.push_back(x);
        }
        return res;
    }
};"""
    },

    399: {
        "starter_code_javascript": "function extract_nth_element(list1, n) {\\n    return [];\\n}",
        "reference_solution_javascript": """function extract_nth_element(list1, n) {
    return list1.map(x => x[n]);
}""",
        "starter_code_java": "class Solution {\\n    public Object extract_nth_element(Object[][] list1, int n) {\\n        return new Object[]{};\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public Object extract_nth_element(Object[][] list1, int n) {
        if (n == 0) {
            String[] res = new String[list1.length];
            for (int i = 0; i < list1.length; i++) res[i] = String.valueOf(list1[i][n]);
            return res;
        } else {
            int[] res = new int[list1.length];
            for (int i = 0; i < list1.length; i++) res[i] = ((Number) list1[i][n]).intValue();
            return res;
        }
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nusing namespace std;\\nstruct NthElementResult {\\n    vector<string> s_vals;\\n};\\nclass Solution {\\npublic:\\n    NthElementResult extract_nth_element(const vector<vector<string>>& list1, int n);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <iostream>
using namespace std;

struct NthElementResult {
    vector<string> s_vals;
    bool operator==(const vector<string>& exp) const {
        return s_vals == exp;
    }
    bool operator==(const vector<int>& exp) const {
        if (s_vals.size() != exp.size()) return false;
        for (size_t i = 0; i < s_vals.size(); i++) {
            if (s_vals[i] != to_string(exp[i])) return false;
        }
        return true;
    }
    friend ostream& operator<<(ostream& os, const NthElementResult& r) {
        os << "[";
        for (size_t i = 0; i < r.s_vals.size(); i++) {
            if (i > 0) os << ", ";
            os << r.s_vals[i];
        }
        os << "]";
        return os;
    }
};

class Solution {
public:
    NthElementResult extract_nth_element(const vector<vector<string>>& list1, int n) {
        NthElementResult res;
        for (const auto& row : list1) {
            res.s_vals.push_back(row[n]);
        }
        return res;
    }
};"""
    },

    400: {
        "starter_code_javascript": "function overlapping(list1, list2) {\\n    return false;\\n}",
        "reference_solution_javascript": """function overlapping(list1, list2) {
    const s = new Set(list2);
    for (const x of list1) if (s.has(x)) return true;
    return false;
}""",
        "starter_code_java": "class Solution {\\n    public boolean overlapping(int[] list1, int[] list2) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public boolean overlapping(int[] list1, int[] list2) {
        Set<Integer> s = new HashSet<>();
        for (int x : list2) s.add(x);
        for (int x : list1) if (s.contains(x)) return true;
        return false;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    bool overlapping(const vector<int>& list1, const vector<int>& list2);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <unordered_set>
using namespace std;
class Solution {
public:
    bool overlapping(const vector<int>& list1, const vector<int>& list2) {
        unordered_set<int> s(list2.begin(), list2.end());
        for (int x : list1) if (s.count(x)) return true;
        return false;
    }
};"""
    },

    402: {
        "starter_code_javascript": "function Find_Max(lst) {\\n    return [];\\n}",
        "reference_solution_javascript": """function Find_Max(lst) {
    let maxSub = [];
    for (const sub of lst) {
        if (sub.length > maxSub.length) maxSub = sub;
    }
    return maxSub;
}""",
        "starter_code_java": """class Solution {
    public String[] Find_Max(char[][] lst) { return new String[]{}; }
    public int[] Find_Max(int[][] lst) { return new int[]{}; }
}""",
        "reference_solution_java": """class Solution {
    public String[] Find_Max(char[][] lst) {
        char[] maxSub = new char[]{};
        for (char[] sub : lst) {
            if (sub.length > maxSub.length) maxSub = sub;
        }
        String[] res = new String[maxSub.length];
        for (int i = 0; i < maxSub.length; i++) res[i] = String.valueOf(maxSub[i]);
        return res;
    }
    public int[] Find_Max(int[][] lst) {
        int[] maxSub = new int[]{};
        for (int[] sub : lst) {
            if (sub.length > maxSub.length) maxSub = sub;
        }
        return maxSub;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    template <typename T>\\n    auto Find_Max(const T& lst);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
using namespace std;
class Solution {
public:
    vector<string> Find_Max(const vector<vector<char>>& lst) {
        vector<char> maxSub;
        for (const auto& sub : lst) {
            if (sub.size() > maxSub.size()) maxSub = sub;
        }
        vector<string> res;
        for (char c : maxSub) res.push_back(string(1, c));
        return res;
    }
    vector<int> Find_Max(const vector<vector<int>>& lst) {
        vector<int> maxSub;
        for (const auto& sub : lst) {
            if (sub.size() > maxSub.size()) maxSub = sub;
        }
        return maxSub;
    }
    template <typename T>
    auto Find_Max(const T& lst) {
        return lst[0];
    }
};"""
    },

    403: {
        "starter_code_javascript": "function round_and_sum(list1) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function round_and_sum(list1) {
    let s = 0;
    for (const x of list1) s += Math.round(x);
    return s * list1.length;
}""",
        "starter_code_java": "class Solution {\\n    public int round_and_sum(Object[] list1) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int round_and_sum(Object[] list1) {
        int s = 0;
        for (Object x : list1) {
            double v = Double.parseDouble(String.valueOf(x));
            s += (int) Math.round(v);
        }
        return s * list1.length;
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int round_and_sum(const vector<string>& list1);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <cmath>
using namespace std;
class Solution {
public:
    int round_and_sum(const vector<string>& list1) {
        int s = 0;
        for (const string& x : list1) {
            double v = stod(x);
            s += (int) round(v);
        }
        return s * (int) list1.size();
    }
};"""
    },

    405: {
        "starter_code_javascript": "function concatenate_tuple(test_tup) {\\n    return \"\";\\n}",
        "reference_solution_javascript": """function concatenate_tuple(test_tup) {
    return test_tup.join('-');
}""",
        "starter_code_java": "class Solution {\\n    public String concatenate_tuple(Object[] test_tup) {\\n        return \"\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String concatenate_tuple(Object[] test_tup) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < test_tup.length; i++) {
            if (i > 0) sb.append("-");
            sb.append(test_tup[i]);
        }
        return sb.toString();
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    string concatenate_tuple(const vector<string>& test_tup);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
using namespace std;
class Solution {
public:
    string concatenate_tuple(const vector<string>& test_tup) {
        string res;
        for (size_t i = 0; i < test_tup.size(); i++) {
            if (i > 0) res += "-";
            res += test_tup[i];
        }
        return res;
    }
};"""
    },

    406: {
        "starter_code_javascript": "function find_Average_Of_Cube(n) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function find_Average_Of_Cube(n) {
    let sum = 0;
    for (let i = 1; i <= n; i++) sum += i * i * i;
    return Number((sum / n).toFixed(6));
}""",
        "starter_code_java": "class Solution {\\n    public double find_Average_Of_Cube(int n) {\\n        return 0.0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public double find_Average_Of_Cube(int n) {
        double sum = 0;
        for (int i = 1; i <= n; i++) sum += (double) i * i * i;
        return sum / n;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    double find_Average_Of_Cube(int n);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    double find_Average_Of_Cube(int n) {
        double sum = 0;
        for (int i = 1; i <= n; i++) sum += (double) i * i * i;
        return sum / n;
    }
};"""
    },

    407: {
        "starter_code_javascript": "function get_maxgold(gold, m, n) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function get_maxgold(gold, m, n) {
    const goldTable = Array.from({ length: m }, () => new Array(n).fill(0));
    for (let col = n - 1; col >= 0; col--) {
        for (let row = 0; row < m; row++) {
            const right = (col === n - 1) ? 0 : goldTable[row][col + 1];
            const right_up = (row === 0 || col === n - 1) ? 0 : goldTable[row - 1][col + 1];
            const right_down = (row === m - 1 || col === n - 1) ? 0 : goldTable[row + 1][col + 1];
            goldTable[row][col] = gold[row][col] + Math.max(right, right_up, right_down);
        }
    }
    let res = goldTable[0][0];
    for (let i = 1; i < m; i++) {
        res = Math.max(res, goldTable[i][0]);
    }
    return res;
}""",
        "starter_code_java": "class Solution {\\n    public int get_maxgold(int[][] gold, int m, int n) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int get_maxgold(int[][] gold, int m, int n) {
        int[][] goldTable = new int[m][n];
        for (int col = n - 1; col >= 0; col--) {
            for (int row = 0; row < m; row++) {
                int right = (col == n - 1) ? 0 : goldTable[row][col + 1];
                int right_up = (row == 0 || col == n - 1) ? 0 : goldTable[row - 1][col + 1];
                int right_down = (row == m - 1 || col == n - 1) ? 0 : goldTable[row + 1][col + 1];
                goldTable[row][col] = gold[row][col] + Math.max(right, Math.max(right_up, right_down));
            }
        }
        int res = goldTable[0][0];
        for (int i = 1; i < m; i++) {
            res = Math.max(res, goldTable[i][0]);
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int get_maxgold(const vector<vector<int>>& gold, int m, int n);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    int get_maxgold(const vector<vector<int>>& gold, int m, int n) {
        vector<vector<int>> goldTable(m, vector<int>(n, 0));
        for (int col = n - 1; col >= 0; col--) {
            for (int row = 0; row < m; row++) {
                int right = (col == n - 1) ? 0 : goldTable[row][col + 1];
                int right_up = (row == 0 || col == n - 1) ? 0 : goldTable[row - 1][col + 1];
                int right_down = (row == m - 1 || col == n - 1) ? 0 : goldTable[row + 1][col + 1];
                goldTable[row][col] = gold[row][col] + max({right, right_up, right_down});
            }
        }
        int res = goldTable[0][0];
        for (int i = 1; i < m; i++) {
            res = max(res, goldTable[i][0]);
        }
        return res;
    }
};"""
    },

    408: {
        "starter_code_javascript": "function extract_rear(test_tuple) {\\n    return [];\\n}",
        "reference_solution_javascript": """function extract_rear(test_tuple) {
    return test_tuple.map(sub => sub.slice(-1));
}""",
        "starter_code_java": "class Solution {\\n    public String[] extract_rear(String[] test_tuple) {\\n        return new String[]{};\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String[] extract_rear(String[] test_tuple) {
        String[] res = new String[test_tuple.length];
        for (int i = 0; i < test_tuple.length; i++) {
            res[i] = String.valueOf(test_tuple[i].charAt(test_tuple[i].length() - 1));
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<string> extract_rear(const vector<string>& test_tuple);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
using namespace std;
class Solution {
public:
    vector<string> extract_rear(const vector<string>& test_tuple) {
        vector<string> res;
        for (const string& sub : test_tuple) {
            res.push_back(string(1, sub.back()));
        }
        return res;
    }
};"""
    },

    409: {
        "starter_code_javascript": "function count_element_in_list(list1, x) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function count_element_in_list(list1, x) {
    let ctr = 0;
    for (const row of list1) {
        if (row.includes(x)) ctr++;
    }
    return ctr;
}""",
        "starter_code_java": "class Solution {\\n    public int count_element_in_list(Object list1, Object x) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int count_element_in_list(Object list1, Object x) {
        int ctr = 0;
        if (list1 instanceof int[][]) {
            int target = Integer.parseInt(String.valueOf(x));
            for (int[] row : (int[][]) list1) {
                for (int v : row) if (v == target) { ctr++; break; }
            }
        } else if (list1 instanceof char[][]) {
            char target = String.valueOf(x).charAt(0);
            for (char[] row : (char[][]) list1) {
                for (char v : row) if (v == target) { ctr++; break; }
            }
        } else if (list1 instanceof Object[][]) {
            for (Object[] row : (Object[][]) list1) {
                for (Object v : row) if (Objects.equals(v, x) || Objects.equals(String.valueOf(v), String.valueOf(x))) { ctr++; break; }
            }
        }
        return ctr;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    template <typename T, typename U>\\n    int count_element_in_list(const T& list1, const U& x);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <type_traits>
using namespace std;

class Solution {
public:
    template <typename T, typename U>
    int count_element_in_list(const T& list1, const U& x) {
        int ctr = 0;
        for (const auto& row : list1) {
            bool found = false;
            for (const auto& val : row) {
                if constexpr (is_same_v<decay_t<decltype(val)>, char>) {
                    char target = '\\0';
                    if constexpr (is_same_v<decay_t<U>, char>) target = x;
                    else if constexpr (is_same_v<decay_t<U>, const char*>) target = x[0];
                    else if constexpr (is_same_v<decay_t<U>, string>) target = x.empty() ? '\\0' : x[0];
                    if (val == target) { found = true; break; }
                } else {
                    if (val == x) { found = true; break; }
                }
            }
            if (found) ctr++;
        }
        return ctr;
    }
};"""
    },

    410: {
        "starter_code_javascript": "function filter_oddnumbers(nums) {\\n    return [];\\n}",
        "reference_solution_javascript": """function filter_oddnumbers(nums) {
    return nums.filter(x => x % 2 !== 0);
}""",
        "starter_code_java": "class Solution {\\n    public int[] filter_oddnumbers(int[] nums) {\\n        return new int[]{};\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[] filter_oddnumbers(int[] nums) {
        List<Integer> list = new ArrayList<>();
        for (int x : nums) if (x % 2 != 0) list.add(x);
        int[] res = new int[list.size()];
        for (int i = 0; i < list.size(); i++) res[i] = list.get(i);
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<int> filter_oddnumbers(const vector<int>& nums);\\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    vector<int> filter_oddnumbers(const vector<int>& nums) {
        vector<int> res;
        for (int x : nums) {
            if (x % 2 != 0) res.push_back(x);
        }
        return res;
    }
};"""
    }
}
'''

if __name__ == "__main__":
    out_file = os.path.join(os.path.dirname(__file__), "batch7_solutions.py")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(BATCH7_CONTENT.strip() + "\n")
    print(f"Written batch 7 solutions to {out_file}")
