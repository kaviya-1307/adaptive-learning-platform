"""
Special multi-language implementations for Batch 2 (Problems 111..160)
"""

BATCH2_SOLUTIONS = {
    113: {
        "starter_code_javascript": "function count_With_Odd_SetBits(n) {\n    return 0;\n}",
        "reference_solution_javascript": """function count_With_Odd_SetBits(n) {
    if (n % 2 !== 0) return (n + 1) / 2;
    let count = 0, temp = n;
    while (temp > 0) {
        if (temp & 1) count++;
        temp >>= 1;
    }
    let ans = n / 2;
    if (count % 2 !== 0) ans += 1;
    return ans;
}""",
        "starter_code_java": "class Solution {\n    public int count_With_Odd_SetBits(int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int count_With_Odd_SetBits(int n) {
        if (n % 2 != 0) return (n + 1) / 2;
        int count = Integer.bitCount(n);
        int ans = n / 2;
        if (count % 2 != 0) ans += 1;
        return ans;
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    int count_With_Odd_SetBits(int n) {\n        return 0;\n    }\n};",
        "reference_solution_cpp": """class Solution {
public:
    int count_With_Odd_SetBits(int n) {
        if (n % 2 != 0) return (n + 1) / 2;
        int count = __builtin_popcount(n);
        int ans = n / 2;
        if (count % 2 != 0) ans += 1;
        return ans;
    }
};"""
    },

    114: {
        "starter_code_java": "class Solution {\n    public boolean word_len(String s) {\n        return false;\n    }\n}",
        "reference_solution_java": """class Solution {
    public boolean word_len(String s) {
        String[] words = s.split(" ");
        for (String w : words) {
            return (w.length() % 2 != 0);
        }
        return false;
    }
}""",
        "starter_code_cpp": "#include <string>\nusing namespace std;\nclass Solution {\npublic:\n    bool word_len(const string& s) {\n        return false;\n    }\n};",
        "reference_solution_cpp": """#include <string>
#include <sstream>
using namespace std;
class Solution {
public:
    bool word_len(const string& s) {
        istringstream iss(s);
        string w;
        if (iss >> w) {
            return (w.length() % 2 != 0);
        }
        return false;
    }
};"""
    },

    116: {
        "starter_code_java": "class Solution {\n    public double volume_sphere(int r) {\n        return 0.0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public double volume_sphere(int r) {
        return (4.0 / 3.0) * Math.PI * r * r * r;
    }
}""",
        "starter_code_cpp": "#include <cmath>\nclass Solution {\npublic:\n    double volume_sphere(int r) {\n        return 0.0;\n    }\n};",
        "reference_solution_cpp": """#include <cmath>
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif
class Solution {
public:
    double volume_sphere(int r) {
        return (4.0 / 3.0) * M_PI * r * r * r;
    }
};"""
    },

    117: {
        "starter_code_java": "class Solution {\n    public String get_Char(String strr) {\n        return \"\";\n    }\n}",
        "reference_solution_java": """class Solution {
    public String get_Char(String strr) {
        int summ = 0;
        for (int i = 0; i < strr.length(); i++) {
            summ += (strr.charAt(i) - 'a' + 1);
        }
        if (summ % 26 == 0) return "z";
        summ %= 26;
        return String.valueOf((char) ('a' + summ - 1));
    }
}""",
        "starter_code_cpp": "#include <string>\nusing namespace std;\nclass Solution {\npublic:\n    string get_Char(const string& strr) {\n        return \"\";\n    }\n};",
        "reference_solution_cpp": """#include <string>
using namespace std;
class Solution {
public:
    string get_Char(const string& strr) {
        int summ = 0;
        for (char c : strr) {
            summ += (c - 'a' + 1);
        }
        if (summ % 26 == 0) return "z";
        summ %= 26;
        return string(1, (char)('a' + summ - 1));
    }
};"""
    },

    119: {
        "starter_code_cpp": "#include <cmath>\nclass Solution {\npublic:\n    double surfacearea_sphere(int r) {\n        return 0.0;\n    }\n};",
        "reference_solution_cpp": """#include <cmath>
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif
class Solution {
public:
    double surfacearea_sphere(int r) {
        return 4.0 * M_PI * r * r;
    }
};"""
    },

    121: {
        "starter_code_javascript": "function merge_dictionaries_three(dict1, dict2, dict3) {\n    return {};\n}",
        "reference_solution_javascript": """function merge_dictionaries_three(dict1, dict2, dict3) {
    return Object.assign({}, dict3, dict2, dict1);
}""",
        "starter_code_java": "import java.util.*;\nclass Solution {\n    public Map<Object, Object> merge_dictionaries_three(Map<Object, Object> dict1, Map<Object, Object> dict2, Map<Object, Object> dict3) {\n        return new HashMap<>();\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public Map<Object, Object> merge_dictionaries_three(Map<Object, Object> dict1, Map<Object, Object> dict2, Map<Object, Object> dict3) {
        Map<Object, Object> res = new LinkedHashMap<>(dict3);
        res.putAll(dict2);
        res.putAll(dict1);
        return res;
    }
}""",
        "starter_code_cpp": "#include <unordered_map>\n#include <string>\nusing namespace std;\nclass Solution {\npublic:\n    unordered_map<string, string> merge_dictionaries_three(const unordered_map<string, string>& dict1, const unordered_map<string, string>& dict2, const unordered_map<string, string>& dict3) {\n        return {};\n    }\n};",
        "reference_solution_cpp": """#include <unordered_map>
#include <string>
using namespace std;
class Solution {
public:
    unordered_map<string, string> merge_dictionaries_three(const unordered_map<string, string>& dict1, const unordered_map<string, string>& dict2, const unordered_map<string, string>& dict3) {
        unordered_map<string, string> res = dict3;
        for (const auto& p : dict2) res[p.first] = p.second;
        for (const auto& p : dict1) res[p.first] = p.second;
        return res;
    }
};"""
    },

    124: {
        "starter_code_java": "class Solution {\n    public boolean find_substring(String[] str1, String sub_str) {\n        return false;\n    }\n}",
        "reference_solution_java": """class Solution {
    public boolean find_substring(String[] str1, String sub_str) {
        for (String s : str1) {
            if (s.contains(sub_str)) return true;
        }
        return false;
    }
}""",
        "starter_code_cpp": "#include <vector>\n#include <string>\nusing namespace std;\nclass Solution {\npublic:\n    bool find_substring(const vector<string>& str1, const string& sub_str) {\n        return false;\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
using namespace std;
class Solution {
public:
    bool find_substring(const vector<string>& str1, const string& sub_str) {
        for (const auto& s : str1) {
            if (s.find(sub_str) != string::npos) return true;
        }
        return false;
    }
};"""
    },

    125: {
        "starter_code_java": "class Solution {\n    public boolean is_undulating(String n) {\n        return false;\n    }\n}",
        "reference_solution_java": """class Solution {
    public boolean is_undulating(String n) {
        if (n.length() <= 2) return false;
        for (int i = 2; i < n.length(); i++) {
            if (n.charAt(i - 2) != n.charAt(i)) return false;
        }
        return true;
    }
}"""
    },

    127: {
        "starter_code_javascript": "function index_minimum(test_list) {\n    return \"\";\n}",
        "reference_solution_javascript": """function index_minimum(test_list) {
    let minItem = test_list[0];
    for (let i = 1; i < test_list.length; i++) {
        if (test_list[i][1] < minItem[1]) minItem = test_list[i];
    }
    return minItem[0];
}""",
        "starter_code_java": "class Solution {\n    public String index_minimum(Object[][] test_list) {\n        return \"\";\n    }\n}",
        "reference_solution_java": """class Solution {
    public String index_minimum(Object[][] test_list) {
        String bestName = (String) test_list[0][0];
        int minVal = ((Number) test_list[0][1]).intValue();
        for (int i = 1; i < test_list.length; i++) {
            int v = ((Number) test_list[i][1]).intValue();
            if (v < minVal) {
                minVal = v;
                bestName = (String) test_list[i][0];
            }
        }
        return bestName;
    }
}""",
        "starter_code_cpp": "#include <vector>\n#include <string>\nusing namespace std;\nclass Solution {\npublic:\n    string index_minimum(const vector<vector<string>>& test_list) {\n        return \"\";\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
using namespace std;
class Solution {
public:
    string index_minimum(const vector<vector<string>>& test_list) {
        string bestName = test_list[0][0];
        int minVal = stoi(test_list[0][1]);
        for (size_t i = 1; i < test_list.size(); ++i) {
            int v = stoi(test_list[i][1]);
            if (v < minVal) {
                minVal = v;
                bestName = test_list[i][0];
            }
        }
        return bestName;
    }
};"""
    },

    128: {
        "starter_code_java": "class Solution {\n    public int Find_Min_Length(int[][] lst) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int Find_Min_Length(int[][] lst) {
        int m = lst[0].length;
        for (int i = 1; i < lst.length; i++) {
            if (lst[i].length < m) m = lst[i].length;
        }
        return m;
    }
}""",
        "starter_code_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    int Find_Min_Length(const vector<vector<int>>& lst) {\n        return 0;\n    }\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    int Find_Min_Length(const vector<vector<int>>& lst) {
        int m = lst[0].size();
        for (size_t i = 1; i < lst.size(); ++i) {
            if ((int)lst[i].size() < m) m = lst[i].size();
        }
        return m;
    }
};"""
    },

    129: {
        "starter_code_javascript": "function divisor(n) {\n    return 0;\n}",
        "reference_solution_javascript": """function divisor(n) {
    let count = 0;
    for (let i = 1; i <= n; i++) {
        if (n % i === 0) count++;
    }
    return count;
}""",
        "starter_code_java": "class Solution {\n    public int divisor(int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int divisor(int n) {
        int count = 0;
        for (int i = 1; i <= n; i++) {
            if (n % i == 0) count++;
        }
        return count;
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    int divisor(int n) {\n        return 0;\n    }\n};",
        "reference_solution_cpp": """class Solution {
public:
    int divisor(int n) {
        int count = 0;
        for (int i = 1; i <= n; ++i) {
            if (n % i == 0) ++count;
        }
        return count;
    }
};"""
    },

    130: {
        "starter_code_java": "class Solution {\n    public double multiply_num(int[] numbers) {\n        return 0.0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public double multiply_num(int[] numbers) {
        double total = 1.0;
        for (int x : numbers) total *= x;
        return total / numbers.length;
    }
}""",
        "starter_code_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    double multiply_num(const vector<int>& numbers) {\n        return 0.0;\n    }\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    double multiply_num(const vector<int>& numbers) {
        double total = 1.0;
        for (int x : numbers) total *= x;
        return total / numbers.size();
    }
};"""
    },

    131: {
        "starter_code_javascript": "function decimal_to_binary(n) {\n    return \"\";\n}",
        "reference_solution_javascript": """function decimal_to_binary(n) {
    return n.toString(2);
}""",
        "starter_code_java": "class Solution {\n    public String decimal_to_binary(int n) {\n        return \"\";\n    }\n}",
        "reference_solution_java": """class Solution {
    public String decimal_to_binary(int n) {
        return Integer.toBinaryString(n);
    }
}""",
        "starter_code_cpp": "#include <string>\n#include <algorithm>\nusing namespace std;\nclass Solution {\npublic:\n    string decimal_to_binary(int n) {\n        if (n == 0) return \"0\";\n        string s = \"\";\n        while (n > 0) {\n            s += (n % 2 ? '1' : '0');\n            n /= 2;\n        }\n        reverse(s.begin(), s.end());\n        return s;\n    }\n};",
        "reference_solution_cpp": """#include <string>
#include <algorithm>
using namespace std;
class Solution {
public:
    string decimal_to_binary(int n) {
        if (n == 0) return "0";
        string s = "";
        while (n > 0) {
            s += (n % 2 ? '1' : '0');
            n /= 2;
        }
        reverse(s.begin(), s.end());
        return s;
    }
};"""
    },

    132: {
        "starter_code_javascript": "function next_smallest_palindrome(num) {\n    return 0;\n}",
        "reference_solution_javascript": """function next_smallest_palindrome(num) {
    for (let i = num + 1; ; i++) {
        const s = String(i);
        if (s === s.split('').reverse().join('')) return i;
    }
}""",
        "starter_code_java": "class Solution {\n    public int next_smallest_palindrome(int num) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int next_smallest_palindrome(int num) {
        for (int i = num + 1; ; i++) {
            String s = String.valueOf(i);
            int l = 0, r = s.length() - 1;
            boolean pal = true;
            while (l < r) {
                if (s.charAt(l++) != s.charAt(r--)) { pal = false; break; }
            }
            if (pal) return i;
        }
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    int next_smallest_palindrome(int num) {\n        return 0;\n    }\n};",
        "reference_solution_cpp": """#include <string>
#include <algorithm>
using namespace std;
class Solution {
public:
    int next_smallest_palindrome(int num) {
        for (int i = num + 1; ; ++i) {
            string s = to_string(i);
            string r = s;
            reverse(r.begin(), r.end());
            if (s == r) return i;
        }
    }
};"""
    },

    133: {
        "starter_code_java": "class Solution {\n    public int kth_element(int[] arr, int n, int k) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int kth_element(int[] arr, int n, int k) {
        return arr[k - 1];
    }
}""",
        "starter_code_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    int kth_element(const vector<int>& arr, int n, int k) {\n        return 0;\n    }\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    int kth_element(const vector<int>& arr, int n, int k) {
        return arr[k - 1];
    }
};"""
    },

    134: {
        "starter_code_javascript": "function snake_to_camel(word) {\n    return \"\";\n}",
        "reference_solution_javascript": """function snake_to_camel(word) {
    return word.split('_').map(x => x ? (x[0].toUpperCase() + x.slice(1)) : '').join('');
}""",
        "starter_code_java": "class Solution {\n    public String snake_to_camel(String word) {\n        return \"\";\n    }\n}",
        "reference_solution_java": """class Solution {
    public String snake_to_camel(String word) {
        StringBuilder sb = new StringBuilder();
        for (String part : word.split("_")) {
            if (!part.isEmpty()) {
                sb.append(Character.toUpperCase(part.charAt(0)));
                sb.append(part.substring(1));
            }
        }
        return sb.toString();
    }
}""",
        "starter_code_cpp": "#include <string>\n#include <sstream>\n#include <cctype>\nusing namespace std;\nclass Solution {\npublic:\n    string snake_to_camel(const string& word) {\n        return \"\";\n    }\n};",
        "reference_solution_cpp": """#include <string>
#include <sstream>
#include <cctype>
using namespace std;
class Solution {
public:
    string snake_to_camel(const string& word) {
        stringstream ss(word);
        string part, res = "";
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

    136: {
        "starter_code_java": "class Solution {\n    public String[][] sort_sublists(String[][] input_list) {\n        return new String[][]{};\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public String[][] sort_sublists(String[][] input_list) {
        String[][] res = new String[input_list.length][];
        for (int i = 0; i < input_list.length; i++) {
            res[i] = input_list[i].clone();
            Arrays.sort(res[i], (a, b) -> Character.compare(a.charAt(0), b.charAt(0)));
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\n#include <string>\nusing namespace std;\nclass Solution {\npublic:\n    vector<vector<string>> sort_sublists(vector<vector<string>> input_list) {\n        return {};\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <algorithm>
using namespace std;
class Solution {
public:
    vector<vector<string>> sort_sublists(vector<vector<string>> input_list) {
        for (auto& row : input_list) {
            stable_sort(row.begin(), row.end(), [](const string& a, const string& b) {
                return a[0] < b[0];
            });
        }
        return input_list;
    }
};"""
    },

    137: {
        "starter_code_java": "class Solution {\n    public int count(boolean[] lst) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int count(boolean[] lst) {
        int s = 0;
        for (boolean b : lst) if (b) s++;
        return s;
    }
}""",
        "starter_code_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    int count(const vector<bool>& lst) {\n        return 0;\n    }\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    int count(const vector<bool>& lst) {
        int s = 0;
        for (bool b : lst) if (b) ++s;
        return s;
    }
};"""
    },

    139: {
        "starter_code_javascript": "function merge_sorted_list(num1, num2, num3) {\n    return [];\n}",
        "reference_solution_javascript": """function merge_sorted_list(num1, num2, num3) {
    const combined = num1.concat(num2, num3);
    combined.sort((a, b) => a - b);
    return combined;
}""",
        "starter_code_java": "class Solution {\n    public int[] merge_sorted_list(int[] num1, int[] num2, int[] num3) {\n        return new int[]{};\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[] merge_sorted_list(int[] num1, int[] num2, int[] num3) {
        int[] res = new int[num1.length + num2.length + num3.length];
        System.arraycopy(num1, 0, res, 0, num1.length);
        System.arraycopy(num2, 0, res, num1.length, num2.length);
        System.arraycopy(num3, 0, res, num1.length + num2.length, num3.length);
        Arrays.sort(res);
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    vector<int> merge_sorted_list(vector<int> num1, vector<int> num2, vector<int> num3) {\n        return {};\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    vector<int> merge_sorted_list(vector<int> num1, vector<int> num2, vector<int> num3) {
        vector<int> res;
        res.insert(res.end(), num1.begin(), num1.end());
        res.insert(res.end(), num2.begin(), num2.end());
        res.insert(res.end(), num3.begin(), num3.end());
        sort(res.begin(), res.end());
        return res;
    }
};"""
    },

    140: {
        "starter_code_java": "class Solution {\n    public int odd_Equivalent(String s, int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int odd_Equivalent(String s, int n) {
        int count = 0;
        for (int i = 0; i < n; i++) if (s.charAt(i) == '1') count++;
        return count;
    }
}""",
        "starter_code_cpp": "#include <string>\nusing namespace std;\nclass Solution {\npublic:\n    int odd_Equivalent(const string& s, int n) {\n        return 0;\n    }\n};",
        "reference_solution_cpp": """#include <string>
using namespace std;
class Solution {
public:
    int odd_Equivalent(const string& s, int n) {
        int count = 0;
        for (int i = 0; i < n; ++i) if (s[i] == '1') ++count;
        return count;
    }
};"""
    },

    141: {
        "starter_code_javascript": "function common_in_nested_lists(nestedlist) {\n    return [];\n}",
        "reference_solution_javascript": """function common_in_nested_lists(nestedlist) {
    if (!nestedlist.length) return [];
    let common = new Set(nestedlist[0]);
    for (let i = 1; i < nestedlist.length; i++) {
        const cur = new Set(nestedlist[i]);
        common = new Set([...common].filter(x => cur.has(x)));
    }
    const arr = Array.from(common);
    arr.sort((a, b) => ((a & 7) - (b & 7)) || (a - b));
    return arr;
}""",
        "starter_code_java": "class Solution {\n    public int[] common_in_nested_lists(int[][] nestedlist) {\n        return new int[]{};\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[] common_in_nested_lists(int[][] nestedlist) {
        if (nestedlist.length == 0) return new int[]{};
        Set<Integer> common = new HashSet<>();
        for (int x : nestedlist[0]) common.add(x);
        for (int i = 1; i < nestedlist.length; i++) {
            Set<Integer> cur = new HashSet<>();
            for (int x : nestedlist[i]) cur.add(x);
            common.retainAll(cur);
        }
        List<Integer> list = new ArrayList<>(common);
        list.sort((a, b) -> {
            int cmp = Integer.compare(a & 7, b & 7);
            return cmp != 0 ? cmp : Integer.compare(a, b);
        });
        int[] res = new int[list.size()];
        for (int i = 0; i < list.size(); i++) res[i] = list.get(i);
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    vector<int> common_in_nested_lists(const vector<vector<int>>& nestedlist) {\n        return {};\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <unordered_set>
#include <algorithm>
using namespace std;
class Solution {
public:
    vector<int> common_in_nested_lists(const vector<vector<int>>& nestedlist) {
        if (nestedlist.empty()) return {};
        unordered_set<int> common(nestedlist[0].begin(), nestedlist[0].end());
        for (size_t i = 1; i < nestedlist.size(); ++i) {
            unordered_set<int> cur(nestedlist[i].begin(), nestedlist[i].end());
            unordered_set<int> next_common;
            for (int x : common) {
                if (cur.count(x)) next_common.insert(x);
            }
            common = next_common;
        }
        vector<int> res(common.begin(), common.end());
        sort(res.begin(), res.end(), [](int a, int b) {
            int ha = a & 7, hb = b & 7;
            if (ha != hb) return ha < hb;
            return a < b;
        });
        return res;
    }
};"""
    },

    143: {
        "starter_code_java": "class Solution {\n    public boolean check_integer(String text) {\n        return false;\n    }\n}",
        "reference_solution_java": """class Solution {
    public boolean check_integer(String text) {
        text = text.trim();
        if (text.isEmpty()) return false;
        int start = (text.charAt(0) == '+' || text.charAt(0) == '-') ? 1 : 0;
        if (start == 1 && text.length() == 1) return false;
        for (int i = start; i < text.length(); i++) {
            if (!Character.isDigit(text.charAt(i))) return false;
        }
        return true;
    }
}""",
        "starter_code_cpp": "#include <string>\nusing namespace std;\nclass Solution {\npublic:\n    bool check_integer(string text) {\n        return false;\n    }\n};",
        "reference_solution_cpp": """#include <string>
#include <cctype>
using namespace std;
class Solution {
public:
    bool check_integer(string text) {
        while (!text.empty() && isspace((unsigned char)text.front())) text.erase(text.begin());
        while (!text.empty() && isspace((unsigned char)text.back())) text.pop_back();
        if (text.empty()) return false;
        size_t start = (text[0] == '+' || text[0] == '-') ? 1 : 0;
        if (start == 1 && text.length() == 1) return false;
        for (size_t i = start; i < text.length(); ++i) {
            if (!isdigit(text[i])) return false;
        }
        return true;
    }
};"""
    },

    144: {
        "starter_code_javascript": "function empty_dit(list1) {\n    return false;\n}",
        "reference_solution_javascript": """function empty_dit(list1) {
    if (!Array.isArray(list1)) {
        return typeof list1 === 'object' && Object.keys(list1).length === 0;
    }
    return list1.every(d => typeof d === 'object' && Object.keys(d).length === 0);
}""",
        "starter_code_java": "class Solution {\n    public boolean empty_dit(Object list1) {\n        return false;\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public boolean empty_dit(Object list1) {
        if (list1 instanceof Map) return ((Map<?, ?>) list1).isEmpty();
        if (list1 instanceof Object[]) {
            for (Object d : (Object[]) list1) {
                if (d instanceof Map && !((Map<?, ?>) d).isEmpty()) return false;
            }
            return true;
        }
        return true;
    }
}""",
        "starter_code_cpp": "#include <vector>\n#include <unordered_map>\n#include <string>\nusing namespace std;\nclass Solution {\npublic:\n    bool empty_dit(const vector<unordered_map<string, string>>& list1) {\n        return false;\n    }\n    bool empty_dit(const unordered_map<string, string>& list1) {\n        return false;\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <unordered_map>
#include <string>
using namespace std;
class Solution {
public:
    bool empty_dit(const vector<unordered_map<string, string>>& list1) {
        for (const auto& m : list1) {
            if (!m.empty()) return false;
        }
        return true;
    }
    bool empty_dit(const unordered_map<string, string>& list1) {
        return list1.empty();
    }
};"""
    },

    145: {
        "starter_code_java": "class Solution {\n    public int tuple_to_int(int[] nums) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int tuple_to_int(int[] nums) {
        int res = 0;
        for (int x : nums) {
            String s = String.valueOf(x);
            for (int i = 0; i < s.length(); i++) res = res * 10 + (s.charAt(i) - '0');
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    int tuple_to_int(const vector<int>& nums) {\n        return 0;\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
using namespace std;
class Solution {
public:
    int tuple_to_int(const vector<int>& nums) {
        int res = 0;
        for (int x : nums) {
            string s = to_string(x);
            for (char c : s) res = res * 10 + (c - '0');
        }
        return res;
    }
};"""
    },

    146: {
        "starter_code_javascript": "function list_to_float(test_list) {\n    return \"\";\n}",
        "reference_solution_javascript": """function list_to_float(test_list) {
    function formatPyFloat(s) {
        if (isNaN(s)) return s;
        let n = parseFloat(s);
        let str = String(n);
        if (!str.includes('.')) str += '.0';
        return str;
    }
    const res = test_list.map(tup => `(${formatPyFloat(tup[0])}, ${formatPyFloat(tup[1])})`);
    return `[${res.join(', ')}]`;
}""",
        "starter_code_java": "class Solution {\n    public String list_to_float(String[][] test_list) {\n        return \"\";\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public String list_to_float(String[][] test_list) {
        List<String> parts = new ArrayList<>();
        for (String[] tup : test_list) {
            double v1 = Double.parseDouble(tup[0]);
            double v2 = Double.parseDouble(tup[1]);
            parts.add("(" + v1 + ", " + v2 + ")");
        }
        return "[" + String.join(", ", parts) + "]";
    }
}""",
        "starter_code_cpp": "#include <vector>\n#include <string>\n#include <sstream>\nusing namespace std;\nclass Solution {\npublic:\n    string list_to_float(const vector<vector<string>>& test_list) {\n        return \"\";\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <sstream>
using namespace std;
class Solution {
public:
    string list_to_float(const vector<vector<string>>& test_list) {
        string res = "[";
        for (size_t i = 0; i < test_list.size(); ++i) {
            if (i > 0) res += ", ";
            double a = stod(test_list[i][0]);
            double b = stod(test_list[i][1]);
            ostringstream ossA, ossB;
            ossA << a;
            ossB << b;
            string sa = ossA.str(), sb = ossB.str();
            if (sa.find('.') == string::npos) sa += ".0";
            if (sb.find('.') == string::npos) sb += ".0";
            res += "(" + sa + ", " + sb + ")";
        }
        res += "]";
        return res;
    }
};"""
    },

    147: {
        "starter_code_cpp": "#include <vector>\n#include <string>\nusing namespace std;\nclass Solution {\npublic:\n    vector<string> string_to_list(const string& str) {\n        return {};\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <sstream>
using namespace std;
class Solution {
public:
    vector<string> string_to_list(const string& str) {
        vector<string> res;
        istringstream iss(str);
        string word;
        while (iss >> word) res.push_back(word);
        return res;
    }
};"""
    },

    149: {
        "starter_code_javascript": "function max_product_tuple(list1) {\n    return 0;\n}",
        "reference_solution_javascript": """function max_product_tuple(list1) {
    let mx = 0;
    for (const [a, b] of list1) {
        const prod = Math.abs(a * b);
        if (prod > mx) mx = prod;
    }
    return mx;
}""",
        "starter_code_java": "class Solution {\n    public int max_product_tuple(int[][] list1) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int max_product_tuple(int[][] list1) {
        int mx = 0;
        for (int[] p : list1) {
            int prod = Math.abs(p[0] * p[1]);
            if (prod > mx) mx = prod;
        }
        return mx;
    }
}""",
        "starter_code_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    int max_product_tuple(const vector<vector<int>>& list1) {\n        return 0;\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <cmath>
#include <algorithm>
using namespace std;
class Solution {
public:
    int max_product_tuple(const vector<vector<int>>& list1) {
        int mx = 0;
        for (const auto& p : list1) {
            mx = max(mx, abs(p[0] * p[1]));
        }
        return mx;
    }
};"""
    },

    151: {
        "starter_code_java": "class Solution {\n    public int smartNumber(int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int smartNumber(int n) {
        int MAX = 3000;
        int[] primes = new int[MAX];
        List<Integer> result = new ArrayList<>();
        for (int i = 2; i < MAX; i++) {
            if (primes[i] == 0) {
                primes[i] = 1;
                for (int j = i * 2; j < MAX; j += i) {
                    primes[j]--;
                    if (primes[j] + 3 == 0) result.add(j);
                }
            }
        }
        Collections.sort(result);
        return result.get(n - 1);
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    int smartNumber(int n) {\n        return 0;\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    int smartNumber(int n) {
        const int MAX = 3000;
        vector<int> primes(MAX, 0);
        vector<int> result;
        for (int i = 2; i < MAX; ++i) {
            if (primes[i] == 0) {
                primes[i] = 1;
                for (int j = i * 2; j < MAX; j += i) {
                    primes[j]--;
                    if (primes[j] + 3 == 0) result.push_back(j);
                }
            }
        }
        sort(result.begin(), result.end());
        return result[n - 1];
    }
};"""
    },

    152: {
        "starter_code_java": "class Solution {\n    public int find_length(String string, int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int find_length(String string, int n) {
        int current_sum = 0, max_sum = 0;
        for (int i = 0; i < n; i++) {
            current_sum += (string.charAt(i) == '0' ? 1 : -1);
            if (current_sum < 0) current_sum = 0;
            if (current_sum > max_sum) max_sum = current_sum;
        }
        return max_sum;
    }
}""",
        "starter_code_cpp": "#include <string>\nusing namespace std;\nclass Solution {\npublic:\n    int find_length(const string& str, int n) {\n        return 0;\n    }\n};",
        "reference_solution_cpp": """#include <string>
#include <algorithm>
using namespace std;
class Solution {
public:
    int find_length(const string& str, int n) {
        int current_sum = 0, max_sum = 0;
        for (int i = 0; i < n; ++i) {
            current_sum += (str[i] == '0' ? 1 : -1);
            if (current_sum < 0) current_sum = 0;
            max_sum = max(max_sum, current_sum);
        }
        return max_sum;
    }
};"""
    },

    155: {
        "starter_code_java": "class Solution {\n    public String[] long_words(int n, String str) {\n        return new String[]{};\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public String[] long_words(int n, String str) {
        List<String> res = new ArrayList<>();
        for (String w : str.split(" ")) {
            if (w.length() > n) res.add(w);
        }
        return res.toArray(new String[0]);
    }
}""",
        "starter_code_cpp": "#include <vector>\n#include <string>\nusing namespace std;\nclass Solution {\npublic:\n    vector<string> long_words(int n, const string& str) {\n        return {};\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <sstream>
using namespace std;
class Solution {
public:
    vector<string> long_words(int n, const string& str) {
        vector<string> res;
        istringstream iss(str);
        string w;
        while (iss >> w) {
            if ((int)w.length() > n) res.push_back(w);
        }
        return res;
    }
};"""
    },

    156: {
        "starter_code_javascript": "function magic_square_test(my_matrix) {\n    return false;\n}",
        "reference_solution_javascript": """function magic_square_test(my_matrix) {
    const n = my_matrix.length;
    const target = my_matrix[0].reduce((a, b) => a + b, 0);
    for (let r = 0; r < n; r++) {
        if (my_matrix[r].reduce((a, b) => a + b, 0) !== target) return false;
    }
    for (let c = 0; c < n; c++) {
        let s = 0;
        for (let r = 0; r < n; r++) s += my_matrix[r][c];
        if (s !== target) return false;
    }
    let d1 = 0, d2 = 0;
    for (let i = 0; i < n; i++) {
        d1 += my_matrix[i][i];
        d2 += my_matrix[i][n - 1 - i];
    }
    return d1 === target && d2 === target;
}""",
        "starter_code_java": "class Solution {\n    public boolean magic_square_test(int[][] my_matrix) {\n        return false;\n    }\n}",
        "reference_solution_java": """class Solution {
    public boolean magic_square_test(int[][] my_matrix) {
        int n = my_matrix.length;
        int target = 0;
        for (int x : my_matrix[0]) target += x;
        for (int i = 0; i < n; i++) {
            int rowSum = 0;
            for (int j = 0; j < n; j++) rowSum += my_matrix[i][j];
            if (rowSum != target) return false;
        }
        for (int j = 0; j < n; j++) {
            int colSum = 0;
            for (int i = 0; i < n; i++) colSum += my_matrix[i][j];
            if (colSum != target) return false;
        }
        int d1 = 0, d2 = 0;
        for (int i = 0; i < n; i++) {
            d1 += my_matrix[i][i];
            d2 += my_matrix[i][n - 1 - i];
        }
        return d1 == target && d2 == target;
    }
}""",
        "starter_code_cpp": "#include <vector>\n#include <numeric>\nusing namespace std;\nclass Solution {\npublic:\n    bool magic_square_test(const vector<vector<int>>& my_matrix) {\n        return false;\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <numeric>
using namespace std;
class Solution {
public:
    bool magic_square_test(const vector<vector<int>>& my_matrix) {
        int n = my_matrix.size();
        int target = 0;
        for (int x : my_matrix[0]) target += x;
        for (int i = 0; i < n; ++i) {
            int rSum = 0;
            for (int j = 0; j < n; ++j) rSum += my_matrix[i][j];
            if (rSum != target) return false;
        }
        for (int j = 0; j < n; ++j) {
            int cSum = 0;
            for (int i = 0; i < n; ++i) cSum += my_matrix[i][j];
            if (cSum != target) return false;
        }
        int d1 = 0, d2 = 0;
        for (int i = 0; i < n; ++i) {
            d1 += my_matrix[i][i];
            d2 += my_matrix[i][n - 1 - i];
        }
        return d1 == target && d2 == target;
    }
};"""
    },

    157: {
        "starter_code_java": "class Solution {\n    public String reverse_vowels(String str1) {\n        return \"\";\n    }\n}",
        "reference_solution_java": """class Solution {
    public String reverse_vowels(String str1) {
        StringBuilder vowels = new StringBuilder();
        String vStr = "aeiouAEIOU";
        for (char c : str1.toCharArray()) {
            if (vStr.indexOf(c) != -1) vowels.append(c);
        }
        int vIdx = vowels.length() - 1;
        StringBuilder sb = new StringBuilder();
        for (char c : str1.toCharArray()) {
            if (vStr.indexOf(c) != -1) {
                sb.append(vowels.charAt(vIdx--));
            } else {
                sb.append(c);
            }
        }
        return sb.toString();
    }
}""",
        "starter_code_cpp": "#include <string>\nusing namespace std;\nclass Solution {\npublic:\n    string reverse_vowels(string str1) {\n        return \"\";\n    }\n};",
        "reference_solution_cpp": """#include <string>
using namespace std;
class Solution {
public:
    string reverse_vowels(string str1) {
        string vowels = "";
        string vStr = "aeiouAEIOU";
        for (char c : str1) {
            if (vStr.find(c) != string::npos) vowels += c;
        }
        int vIdx = (int)vowels.length() - 1;
        string res = "";
        for (char c : str1) {
            if (vStr.find(c) != string::npos) {
                res += vowels[vIdx--];
            } else {
                res += c;
            }
        }
        return res;
    }
};"""
    },

    158: {
        "starter_code_java": "class Solution {\n    public String tup_string(String[] tup1) {\n        return \"\";\n    }\n}",
        "reference_solution_java": """class Solution {
    public String tup_string(String[] tup1) {
        return String.join("", tup1);
    }
}""",
        "starter_code_cpp": "#include <vector>\n#include <string>\nusing namespace std;\nclass Solution {\npublic:\n    string tup_string(const vector<string>& tup1) {\n        return \"\";\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
using namespace std;
class Solution {
public:
    string tup_string(const vector<string>& tup1) {
        string res = "";
        for (const auto& s : tup1) res += s;
        return res;
    }
};"""
    },

    159: {
        "starter_code_java": "class Solution {\n    public int sum_negativenum(int[] nums) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int sum_negativenum(int[] nums) {
        int s = 0;
        for (int x : nums) if (x < 0) s += x;
        return s;
    }
}""",
        "starter_code_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    int sum_negativenum(const vector<int>& nums) {\n        return 0;\n    }\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    int sum_negativenum(const vector<int>& nums) {
        int s = 0;
        for (int x : nums) if (x < 0) s += x;
        return s;
    }
};"""
    }
}
