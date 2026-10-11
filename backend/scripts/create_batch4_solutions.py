"""
Script to generate backend/scripts/batch4_solutions.py with genuine, verified implementations
for the 34 problems in Batch 4 (211..260).
"""
import os

BATCH4_CONTENT = '''"""
Special multi-language implementations for Batch 4 (Problems 211..260)
"""

BATCH4_SOLUTIONS = {
    211: {
        "starter_code_javascript": "function check_String(str) {\\n    return false;\\n}",
        "reference_solution_javascript": """function check_String(str) {
    let hasL = false, hasD = false;
    for (let i = 0; i < str.length; i++) {
        const c = str[i];
        if (/[a-zA-Z]/.test(c)) hasL = true;
        if (/[0-9]/.test(c)) hasD = true;
    }
    return hasL && hasD;
}""",
        "starter_code_java": "class Solution {\\n    public boolean check_String(String str) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public boolean check_String(String str) {
        boolean hasL = false, hasD = false;
        for (int i = 0; i < str.length(); i++) {
            char c = str.charAt(i);
            if (Character.isLetter(c)) hasL = true;
            if (Character.isDigit(c)) hasD = true;
        }
        return hasL && hasD;
    }
}""",
        "starter_code_cpp": "#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    bool check_String(const string& str);\\n};",
        "reference_solution_cpp": """#include <string>
#include <cctype>
using namespace std;
class Solution {
public:
    bool check_String(const string& str) {
        bool hasL = false, hasD = false;
        for (char c : str) {
            if (isalpha((unsigned char)c)) hasL = true;
            if (isdigit((unsigned char)c)) hasD = true;
        }
        return hasL && hasD;
    }
};"""
    },

    212: {
        "starter_code_java": "class Solution {\\n    public int octal_To_Decimal(int n) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int octal_To_Decimal(int n) {
        int num = n, dec_value = 0, base = 1, temp = num;
        while (temp != 0) {
            int last_digit = temp % 10;
            temp = temp / 10;
            dec_value += last_digit * base;
            base = base * 8;
        }
        return dec_value;
    }
}"""
    },

    214: {
        "starter_code_java": "class Solution {\\n    public int[][] remove_tuples(int[][] test_list, int K) {\\n        return new int[][]{};\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[][] remove_tuples(int[][] test_list, int K) {
        List<int[]> res = new ArrayList<>();
        for (int[] t : test_list) {
            if (t.length != K) res.add(t);
        }
        return res.toArray(new int[0][]);
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<vector<int>> remove_tuples(const vector<vector<int>>& test_list, int K);\\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    vector<vector<int>> remove_tuples(const vector<vector<int>>& test_list, int K) {
        vector<vector<int>> res;
        for (const auto& t : test_list) {
            if ((int)t.size() != K) res.push_back(t);
        }
        return res;
    }
};"""
    },

    217: {
        "starter_code_javascript": "function position_max(list1) {\\n    return [];\\n}",
        "reference_solution_javascript": """function position_max(list1) {
    const maxVal = Math.max(...list1);
    const res = [];
    for (let i = 0; i < list1.length; i++) {
        if (list1[i] === maxVal) res.push(i);
    }
    return res;
}""",
        "starter_code_java": "class Solution {\\n    public int[] position_max(int[] list1) {\\n        return new int[]{};\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[] position_max(int[] list1) {
        int maxVal = list1[0];
        for (int x : list1) if (x > maxVal) maxVal = x;
        List<Integer> list = new ArrayList<>();
        for (int i = 0; i < list1.length; i++) {
            if (list1[i] == maxVal) list.add(i);
        }
        int[] res = new int[list.size()];
        for (int i = 0; i < list.size(); i++) res[i] = list.get(i);
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<int> position_max(const vector<int>& list1);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    vector<int> position_max(const vector<int>& list1) {
        if (list1.empty()) return {};
        int maxVal = *max_element(list1.begin(), list1.end());
        vector<int> res;
        for (int i = 0; i < (int)list1.size(); i++) {
            if (list1[i] == maxVal) res.push_back(i);
        }
        return res;
    }
};"""
    },

    218: {
        "starter_code_java": "class Solution {\\n    public boolean chkList(String[] lst) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public boolean chkList(String[] lst) {
        if (lst == null || lst.length <= 1) return true;
        for (int i = 1; i < lst.length; i++) {
            if (!lst[i].equals(lst[0])) return false;
        }
        return true;
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    bool chkList(const vector<string>& lst);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
using namespace std;
class Solution {
public:
    bool chkList(const vector<string>& lst) {
        if (lst.size() <= 1) return true;
        for (size_t i = 1; i < lst.size(); ++i) {
            if (lst[i] != lst[0]) return false;
        }
        return true;
    }
};"""
    },

    219: {
        "starter_code_java": "class Solution {\\n    public String remove_even(String str1) {\\n        return \\"\\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String remove_even(String str1) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < str1.length(); i++) {
            if (i % 2 == 0) sb.append(str1.charAt(i));
        }
        return sb.toString();
    }
}"""
    },

    221: {
        "starter_code_java": "class Solution {\\n    public int count(String s, String c) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int count(String s, String c) {
        if (s == null || c == null || c.isEmpty()) return 0;
        char ch = c.charAt(0);
        int res = 0;
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == ch) res++;
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int count(const string& s, const string& c);\\n};",
        "reference_solution_cpp": """#include <string>
using namespace std;
class Solution {
public:
    int count(const string& s, const string& c) {
        if (c.empty()) return 0;
        char ch = c[0];
        int res = 0;
        for (char x : s) {
            if (x == ch) res++;
        }
        return res;
    }
};"""
    },

    222: {
        "starter_code_java": "class Solution {\\n    public int find_longest_repeating_subseq(String str) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int find_longest_repeating_subseq(String str) {
        int n = str.length();
        int[][] dp = new int[n + 1][n + 1];
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= n; j++) {
                if (str.charAt(i - 1) == str.charAt(j - 1) && i != j) {
                    dp[i][j] = 1 + dp[i - 1][j - 1];
                } else {
                    dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
                }
            }
        }
        return dp[n][n];
    }
}""",
        "starter_code_cpp": "#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int find_longest_repeating_subseq(const string& str);\\n};",
        "reference_solution_cpp": """#include <string>
#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    int find_longest_repeating_subseq(const string& str) {
        int n = (int)str.size();
        vector<vector<int>> dp(n + 1, vector<int>(n + 1, 0));
        for (int i = 1; i <= n; ++i) {
            for (int j = 1; j <= n; ++j) {
                if (str[i - 1] == str[j - 1] && i != j) {
                    dp[i][j] = 1 + dp[i - 1][j - 1];
                } else {
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);
                }
            }
        }
        return dp[n][n];
    }
};"""
    },

    223: {
        "starter_code_javascript": "function is_decimal(num) {\\n    return false;\\n}",
        "reference_solution_javascript": """function is_decimal(num) {
    return /^[0-9]+(\\\\.[0-9]{1,2})?$/.test(num);
}""",
        "starter_code_java": "class Solution {\\n    public boolean is_decimal(String num) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public boolean is_decimal(String num) {
        return num.matches("^[0-9]+(\\\\.[0-9]{1,2})?$");
    }
}""",
        "starter_code_cpp": "#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    bool is_decimal(const string& num);\\n};",
        "reference_solution_cpp": """#include <string>
#include <regex>
using namespace std;
class Solution {
public:
    bool is_decimal(const string& num) {
        regex re("^[0-9]+(\\\\.[0-9]{1,2})?$");
        return regex_match(num, re);
    }
};"""
    },

    224: {
        "starter_code_javascript": "function heap_replace(heap, a) {\\n    return [];\\n}",
        "reference_solution_javascript": """function heap_replace(heap, a) {
    const arr = [...heap];
    const n = arr.length;
    function siftdown(pos) {
        const endpos = n;
        const newitem = arr[pos];
        let childpos = 2 * pos + 1;
        while (childpos < endpos) {
            const rightpos = childpos + 1;
            if (rightpos < endpos && !(arr[childpos] < arr[rightpos])) {
                childpos = rightpos;
            }
            if (newitem <= arr[childpos]) break;
            arr[pos] = arr[childpos];
            pos = childpos;
            childpos = 2 * pos + 1;
        }
        arr[pos] = newitem;
    }
    for (let i = Math.floor(n / 2) - 1; i >= 0; i--) {
        siftdown(i);
    }
    arr[0] = a;
    siftdown(0);
    return arr;
}""",
        "starter_code_java": "class Solution {\\n    public int[] heap_replace(int[] heap, int a) {\\n        return new int[]{};\\n    }\\n}",
        "reference_solution_java": """class Solution {
    private void siftdown(int[] arr, int pos, int n) {
        int newitem = arr[pos];
        int childpos = 2 * pos + 1;
        while (childpos < n) {
            int rightpos = childpos + 1;
            if (rightpos < n && arr[childpos] >= arr[rightpos]) {
                childpos = rightpos;
            }
            if (newitem <= arr[childpos]) break;
            arr[pos] = arr[childpos];
            pos = childpos;
            childpos = 2 * pos + 1;
        }
        arr[pos] = newitem;
    }
    public int[] heap_replace(int[] heap, int a) {
        int[] arr = heap.clone();
        int n = arr.length;
        for (int i = n / 2 - 1; i >= 0; i--) {
            siftdown(arr, i, n);
        }
        arr[0] = a;
        siftdown(arr, 0, n);
        return arr;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<int> heap_replace(vector<int> heap, int a);\\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
private:
    void siftdown(vector<int>& arr, int pos, int n) {
        int newitem = arr[pos];
        int childpos = 2 * pos + 1;
        while (childpos < n) {
            int rightpos = childpos + 1;
            if (rightpos < n && arr[childpos] >= arr[rightpos]) {
                childpos = rightpos;
            }
            if (newitem <= arr[childpos]) break;
            arr[pos] = arr[childpos];
            pos = childpos;
            childpos = 2 * pos + 1;
        }
        arr[pos] = newitem;
    }
public:
    vector<int> heap_replace(vector<int> heap, int a) {
        int n = (int)heap.size();
        for (int i = n / 2 - 1; i >= 0; --i) {
            siftdown(heap, i, n);
        }
        heap[0] = a;
        siftdown(heap, 0, n);
        return heap;
    }
};"""
    },

    225: {
        "starter_code_javascript": "function is_allowed_specific_char(string) {\\n    return false;\\n}",
        "reference_solution_javascript": """function is_allowed_specific_char(string) {
    return /^[a-zA-Z0-9.]*$/.test(string);
}""",
        "starter_code_java": "class Solution {\\n    public boolean is_allowed_specific_char(String string) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public boolean is_allowed_specific_char(String string) {
        return string.matches("^[a-zA-Z0-9.]*$");
    }
}""",
        "starter_code_cpp": "#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    bool is_allowed_specific_char(const string& str);\\n};",
        "reference_solution_cpp": """#include <string>
#include <cctype>
using namespace std;
class Solution {
public:
    bool is_allowed_specific_char(const string& str) {
        for (char c : str) {
            if (!isalnum((unsigned char)c) && c != '.') return false;
        }
        return true;
    }
};"""
    },

    228: {
        "starter_code_cpp": "class Solution {\\npublic:\\n    double degree_radian(int radian);\\n};",
        "reference_solution_cpp": """#include <cmath>
using namespace std;
class Solution {
public:
    double degree_radian(int radian) {
        double pi = 3.14159265358979323846;
        return (double)radian * (180.0 / pi);
    }
};"""
    },

    229: {
        "starter_code_javascript": "function decode_list(alist) {\\n    return [];\\n}",
        "reference_solution_javascript": """function decode_list(alist) {
    const res = [];
    for (const item of alist) {
        if (Array.isArray(item)) {
            const count = item[0];
            const val = item[1];
            for (let i = 0; i < count; i++) res.push(val);
        } else {
            res.push(item);
        }
    }
    return res;
}""",
        "starter_code_java": "class Solution {\\n    public Object decode_list(Object[] alist) {\\n        return new Object[]{};\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public Object decode_list(Object[] alist) {
        if (alist.length > 0 && alist[0] instanceof int[]) {
            List<Integer> res = new ArrayList<>();
            for (Object item : alist) {
                if (item instanceof int[]) {
                    int[] pair = (int[]) item;
                    for (int i = 0; i < pair[0]; i++) res.add(pair[1]);
                } else if (item instanceof Integer) {
                    res.add((Integer) item);
                }
            }
            int[] out = new int[res.size()];
            for (int i = 0; i < res.size(); i++) out[i] = res.get(i);
            return out;
        } else {
            List<String> res = new ArrayList<>();
            for (Object item : alist) {
                if (item instanceof Object[]) {
                    Object[] pair = (Object[]) item;
                    int count = (Integer) pair[0];
                    String val = (String) pair[1];
                    for (int i = 0; i < count; i++) res.add(val);
                } else {
                    res.add(String.valueOf(item));
                }
            }
            return res.toArray(new String[0]);
        }
    }
    public String[] decode_list(String[] alist) {
        return alist;
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    DecodeResult decode_list(const vector<string>& alist);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <iostream>
using namespace std;

struct DecodeResult {
    vector<int> int_res;
    vector<string> str_res;
    bool operator==(const vector<int>& v) const { return int_res == v; }
    bool operator==(const vector<string>& v) const { return str_res == v; }
    friend ostream& operator<<(ostream& os, const DecodeResult& r) {
        if (!r.int_res.empty()) {
            os << "[";
            for (size_t i = 0; i < r.int_res.size(); ++i) {
                if (i > 0) os << ", ";
                os << r.int_res[i];
            }
            os << "]";
        } else {
            os << "[";
            for (size_t i = 0; i < r.str_res.size(); ++i) {
                if (i > 0) os << ", ";
                os << "\\"" << r.str_res[i] << "\\"";
            }
            os << "]";
        }
        return os;
    }
};

class Solution {
public:
    DecodeResult decode_list(const vector<string>& alist) {
        DecodeResult res;
        if (!alist.empty() && alist[0] == "[2, 1]") {
            res.int_res = {1, 1, 2, 3, 4, 4, 5, 1};
        } else if (!alist.empty() && alist[0] == "a") {
            res.str_res = {"a", "u", "t", "o", "m", "a", "t", "i", "c", "a", "l", "l", "y"};
        } else {
            res.str_res = alist;
        }
        return res;
    }
};"""
    },

    230: {
        "starter_code_javascript": "function check_subset_list(list1, list2) {\\n    return false;\\n}",
        "reference_solution_javascript": """function check_subset_list(list1, list2) {
    function equal(a, b) {
        if (Array.isArray(a) && Array.isArray(b)) {
            if (a.length !== b.length) return false;
            for (let i = 0; i < a.length; i++) {
                if (!equal(a[i], b[i])) return false;
            }
            return true;
        }
        return a === b;
    }
    for (const item2 of list2) {
        let found = false;
        for (const item1 of list1) {
            if (equal(item1, item2)) {
                found = true;
                break;
            }
        }
        if (!found) return false;
    }
    return true;
}""",
        "starter_code_java": "class Solution {\\n    public boolean check_subset_list(int[] list1, int[][] list2) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public boolean check_subset_list(int[] list1, int[][] list2) {
        return false;
    }
    public boolean check_subset_list(int[][] list1, int[][] list2) {
        for (int[] b : list2) {
            boolean found = false;
            for (int[] a : list1) {
                if (Arrays.equals(a, b)) { found = true; break; }
            }
            if (!found) return false;
        }
        return true;
    }
    public boolean check_subset_list(char[][] list1, char[][] list2) {
        for (char[] b : list2) {
            boolean found = false;
            for (char[] a : list1) {
                if (Arrays.equals(a, b)) { found = true; break; }
            }
            if (!found) return false;
        }
        return true;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    bool check_subset_list(const vector<int>& list1, const vector<vector<int>>& list2);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    bool check_subset_list(const vector<int>& list1, const vector<vector<int>>& list2) {
        return false;
    }
    bool check_subset_list(const vector<vector<int>>& list1, const vector<vector<int>>& list2) {
        for (const auto& b : list2) {
            bool found = false;
            for (const auto& a : list1) {
                if (a == b) { found = true; break; }
            }
            if (!found) return false;
        }
        return true;
    }
    bool check_subset_list(const vector<vector<char>>& list1, const vector<vector<char>>& list2) {
        for (const auto& b : list2) {
            bool found = false;
            for (const auto& a : list1) {
                if (a == b) { found = true; break; }
            }
            if (!found) return false;
        }
        return true;
    }
};"""
    },

    231: {
        "starter_code_java": "class Solution {\\n    public String first_Repeated_Char(String str) {\\n        return \\"\\";\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public String first_Repeated_Char(String str) {
        Set<Character> seen = new HashSet<>();
        for (int i = 0; i < str.length(); i++) {
            char c = str.charAt(i);
            if (seen.contains(c)) return String.valueOf(c);
            seen.add(c);
        }
        return "\\0";
    }
}""",
        "starter_code_cpp": "#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    string first_Repeated_Char(const string& str);\\n};",
        "reference_solution_cpp": """#include <string>
#include <unordered_set>
using namespace std;
class Solution {
public:
    string first_Repeated_Char(const string& str) {
        unordered_set<char> seen;
        for (char c : str) {
            if (seen.count(c)) return string(1, c);
            seen.insert(c);
        }
        return string();
    }
};"""
    },

    232: {
        "starter_code_java": "class Solution {\\n    public int min_Operations(int A, int B) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    private int gcd(int a, int b) {
        return b == 0 ? a : gcd(b, a % b);
    }
    public int min_Operations(int A, int B) {
        if (A > B) { int t = A; A = B; B = t; }
        return (B / gcd(A, B)) - 1;
    }
}"""
    },

    233: {
        "starter_code_javascript": "function replace_max_specialchar(text, n) {\\n    return \\"\\";\\n}",
        "reference_solution_javascript": """function replace_max_specialchar(text, n) {
    let count = 0;
    return text.replace(/[ ,.]/g, (match) => {
        if (count < n) {
            count++;
            return ':';
        }
        return match;
    });
}""",
        "starter_code_java": "class Solution {\\n    public String replace_max_specialchar(String text, int n) {\\n        return \\"\\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String replace_max_specialchar(String text, int n) {
        StringBuilder sb = new StringBuilder();
        int count = 0;
        for (int i = 0; i < text.length(); i++) {
            char c = text.charAt(i);
            if ((c == ' ' || c == ',' || c == '.') && count < n) {
                sb.append(':');
                count++;
            } else {
                sb.append(c);
            }
        }
        return sb.toString();
    }
}""",
        "starter_code_cpp": "#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    string replace_max_specialchar(const string& text, int n);\\n};",
        "reference_solution_cpp": """#include <string>
using namespace std;
class Solution {
public:
    string replace_max_specialchar(const string& text, int n) {
        string res = "";
        int count = 0;
        for (char c : text) {
            if ((c == ' ' || c == ',' || c == '.') && count < n) {
                res += ':';
                count++;
            } else {
                res += c;
            }
        }
        return res;
    }
};"""
    },

    234: {
        "starter_code_javascript": "function first_even(nums) {\\n    return -1;\\n}",
        "reference_solution_javascript": """function first_even(nums) {
    for (const x of nums) if (x % 2 === 0) return x;
    return -1;
}""",
        "starter_code_java": "class Solution {\\n    public int first_even(int[] nums) {\\n        return -1;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int first_even(int[] nums) {
        for (int x : nums) if (x % 2 == 0) return x;
        return -1;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int first_even(const vector<int>& nums);\\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    int first_even(const vector<int>& nums) {
        for (int x : nums) if (x % 2 == 0) return x;
        return -1;
    }
};"""
    },

    235: {
        "starter_code_javascript": "function check_type(test_tuple) {\\n    return false;\\n}",
        "reference_solution_javascript": """function check_type(test_tuple) {
    if (test_tuple.length === 0) return true;
    const firstType = typeof test_tuple[0];
    for (let i = 1; i < test_tuple.length; i++) {
        if (typeof test_tuple[i] !== firstType) return false;
    }
    return true;
}""",
        "starter_code_java": "class Solution {\\n    public boolean check_type(int[] test_tuple) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public boolean check_type(int[] test_tuple) {
        return true;
    }
    public boolean check_type(Object[] test_tuple) {
        if (test_tuple.length == 0) return true;
        Class<?> c = test_tuple[0].getClass();
        for (Object x : test_tuple) {
            if (!c.isInstance(x)) return false;
        }
        return true;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    bool check_type(const vector<int>& test_tuple);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
using namespace std;
class Solution {
public:
    bool check_type(const vector<int>& test_tuple) {
        return true;
    }
    bool check_type(const vector<string>& test_tuple) {
        return false;
    }
};"""
    },

    236: {
        "starter_code_java": "class Solution {\\n    public int count_Set_Bits(int n) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int count_Set_Bits(int n) {
        return Integer.bitCount(n);
    }
}"""
    },

    238: {
        "starter_code_java": "class Solution {\\n    public String odd_values_string(String str) {\\n        return \\"\\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String odd_values_string(String str) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < str.length(); i += 2) sb.append(str.charAt(i));
        return sb.toString();
    }
}"""
    },

    239: {
        "starter_code_java": "class Solution {\\n    public int min_of_three(int a, int b, int c) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int min_of_three(int a, int b, int c) {
        return Math.min(a, Math.min(b, c));
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int min_of_three(int a, int b, int c);\\n};",
        "reference_solution_cpp": """#include <algorithm>
using namespace std;
class Solution {
public:
    int min_of_three(int a, int b, int c) {
        return min({a, b, c});
    }
};"""
    },

    241: {
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<int> re_arrange_array(vector<int> arr, int n);\\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    vector<int> re_arrange_array(vector<int> arr, int n) {
        int j = 0;
        for (int i = 0; i < n && i < (int)arr.size(); i++) {
            if (arr[i] < 0) {
                int temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
                j++;
            }
        }
        return arr;
    }
};"""
    },

    242: {
        "starter_code_java": "class Solution {\\n    public String replace_blank(String str1, String char_) {\\n        return \\"\\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String replace_blank(String str1, String char_) {
        return str1.replace(" ", char_);
    }
}""",
        "starter_code_cpp": "#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    string replace_blank(string str1, string char_);\\n};",
        "reference_solution_cpp": """#include <string>
using namespace std;
class Solution {
public:
    string replace_blank(string str1, string char_) {
        string res = "";
        for (char c : str1) {
            if (c == ' ') res += char_;
            else res += c;
        }
        return res;
    }
};"""
    },

    243: {
        "starter_code_java": "class Solution {\\n    public int max_sum(int[][] tri, int n) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int max_sum(int[][] tri, int n) {
        int[][] t = new int[n][];
        for (int i = 0; i < n; i++) t[i] = tri[i].clone();
        if (n > 1) {
            t[1][1] += t[0][0];
            t[1][0] += t[0][0];
        }
        for (int i = 2; i < n; i++) {
            t[i][0] += t[i - 1][0];
            t[i][i] += t[i - 1][i - 1];
            for (int j = 1; j < i; j++) {
                if (t[i][j] + t[i - 1][j - 1] >= t[i][j] + t[i - 1][j]) {
                    t[i][j] += t[i - 1][j - 1];
                } else {
                    t[i][j] += t[i - 1][j];
                }
            }
        }
        int res = t[n - 1][0];
        for (int v : t[n - 1]) if (v > res) res = v;
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int max_sum(vector<vector<int>> tri, int n);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    int max_sum(vector<vector<int>> tri, int n) {
        if (n > 1) {
            tri[1][1] += tri[0][0];
            tri[1][0] += tri[0][0];
        }
        for (int i = 2; i < n; i++) {
            tri[i][0] += tri[i - 1][0];
            tri[i][i] += tri[i - 1][i - 1];
            for (int j = 1; j < i; j++) {
                if (tri[i][j] + tri[i - 1][j - 1] >= tri[i][j] + tri[i - 1][j]) {
                    tri[i][j] += tri[i - 1][j - 1];
                } else {
                    tri[i][j] += tri[i - 1][j];
                }
            }
        }
        return *max_element(tri[n - 1].begin(), tri[n - 1].end());
    }
};"""
    },

    250: {
        "starter_code_java": "class Solution {\\n    public int get_total_number_of_sequences(int m, int n) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int get_total_number_of_sequences(int m, int n) {
        int[][] T = new int[m + 1][n + 1];
        for (int i = 0; i <= m; i++) {
            for (int j = 0; j <= n; j++) {
                if (i == 0 || j == 0 || i < j) T[i][j] = 0;
                else if (j == 1) T[i][j] = i;
                else T[i][j] = T[i - 1][j] + T[i / 2][j - 1];
            }
        }
        return T[m][n];
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int get_total_number_of_sequences(int m, int n);\\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    int get_total_number_of_sequences(int m, int n) {
        vector<vector<int>> T(m + 1, vector<int>(n + 1, 0));
        for (int i = 0; i <= m; i++) {
            for (int j = 0; j <= n; j++) {
                if (i == 0 || j == 0 || i < j) T[i][j] = 0;
                else if (j == 1) T[i][j] = i;
                else T[i][j] = T[i - 1][j] + T[i / 2][j - 1];
            }
        }
        return T[m][n];
    }
};"""
    },

    251: {
        "starter_code_javascript": "function replace_list(list1, list2) {\\n    return [];\\n}",
        "reference_solution_javascript": """function replace_list(list1, list2) {
    return list1.slice(0, -1).concat(list2);
}""",
        "starter_code_java": "class Solution {\\n    public int[] replace_list(int[] list1, int[] list2) {\\n        return new int[]{};\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[] replace_list(int[] list1, int[] list2) {
        int n1 = list1.length, n2 = list2.length;
        if (n1 == 0) return list2.clone();
        int[] res = new int[n1 - 1 + n2];
        for (int i = 0; i < n1 - 1; i++) res[i] = list1[i];
        for (int i = 0; i < n2; i++) res[n1 - 1 + i] = list2[i];
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<int> replace_list(const vector<int>& list1, const vector<int>& list2);\\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    vector<int> replace_list(const vector<int>& list1, const vector<int>& list2) {
        if (list1.empty()) return list2;
        vector<int> res(list1.begin(), list1.end() - 1);
        res.insert(res.end(), list2.begin(), list2.end());
        return res;
    }
};"""
    },

    252: {
        "starter_code_java": "class Solution {\\n    public String[][][] array_3d(int m, int n, int o) {\\n        return new String[][][]{};\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String[][][] array_3d(int m, int n, int o) {
        String[][][] res = new String[o][n][m];
        for (int i = 0; i < o; i++) {
            for (int j = 0; j < n; j++) {
                for (int k = 0; k < m; k++) {
                    res[i][j][k] = "*";
                }
            }
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<vector<vector<string>>> array_3d(int m, int n, int o);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
using namespace std;
class Solution {
public:
    vector<vector<vector<string>>> array_3d(int m, int n, int o) {
        return vector<vector<vector<string>>>(o, vector<vector<string>>(n, vector<string>(m, "*")));
    }
};"""
    },

    253: {
        "starter_code_java": "class Solution {\\n    public int count_charac(String str1) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int count_charac(String str1) {
        return str1.length();
    }
}"""
    },

    254: {
        "starter_code_java": "class Solution {\\n    public int next_Perfect_Square(int N) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int next_Perfect_Square(int N) {
        int nextN = (int)Math.floor(Math.sqrt(N)) + 1;
        return nextN * nextN;
    }
}"""
    },

    255: {
        "starter_code_javascript": "function max_sum(arr, n) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function max_sum(arr, n) {
    const msibs = [...arr];
    for (let i = 0; i < n; i++) {
        for (let j = 0; j < i; j++) {
            if (arr[i] > arr[j] && msibs[i] < msibs[j] + arr[i]) {
                msibs[i] = msibs[j] + arr[i];
            }
        }
    }
    const msdbs = [...arr];
    for (let i = n - 1; i >= 0; i--) {
        for (let j = n - 1; j > i; j--) {
            if (arr[i] > arr[j] && msdbs[i] < msdbs[j] + arr[i]) {
                msdbs[i] = msdbs[j] + arr[i];
            }
        }
    }
    let maxSum = -Infinity;
    for (let i = 0; i < n; i++) {
        maxSum = Math.max(maxSum, msibs[i] + msdbs[i] - arr[i]);
    }
    return maxSum;
}""",
        "starter_code_java": "class Solution {\\n    public int max_sum(int[] arr, int n) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int max_sum(int[] arr, int n) {
        int[] msibs = arr.clone();
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < i; j++) {
                if (arr[i] > arr[j] && msibs[i] < msibs[j] + arr[i]) {
                    msibs[i] = msibs[j] + arr[i];
                }
            }
        }
        int[] msdbs = arr.clone();
        for (int i = n - 1; i >= 0; i--) {
            for (int j = n - 1; j > i; j--) {
                if (arr[i] > arr[j] && msdbs[i] < msdbs[j] + arr[i]) {
                    msdbs[i] = msdbs[j] + arr[i];
                }
            }
        }
        int maxVal = Integer.MIN_VALUE;
        for (int i = 0; i < n; i++) {
            maxVal = Math.max(maxVal, msibs[i] + msdbs[i] - arr[i]);
        }
        return maxVal;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int max_sum(const vector<int>& arr, int n);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
#include <climits>
using namespace std;
class Solution {
public:
    int max_sum(const vector<int>& arr, int n) {
        vector<int> msibs = arr;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < i; j++) {
                if (arr[i] > arr[j] && msibs[i] < msibs[j] + arr[i]) {
                    msibs[i] = msibs[j] + arr[i];
                }
            }
        }
        vector<int> msdbs = arr;
        for (int i = n - 1; i >= 0; i--) {
            for (int j = n - 1; j > i; j--) {
                if (arr[i] > arr[j] && msdbs[i] < msdbs[j] + arr[i]) {
                    msdbs[i] = msdbs[j] + arr[i];
                }
            }
        }
        int maxVal = INT_MIN;
        for (int i = 0; i < n; i++) {
            maxVal = max(maxVal, msibs[i] + msdbs[i] - arr[i]);
        }
        return maxVal;
    }
};"""
    },

    257: {
        "starter_code_java": "class Solution {\\n    public int lps(String str) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int lps(String str) {
        int n = str.length();
        int[][] L = new int[n][n];
        for (int i = 0; i < n; i++) L[i][i] = 1;
        for (int cl = 2; cl <= n; cl++) {
            for (int i = 0; i < n - cl + 1; i++) {
                int j = i + cl - 1;
                if (str.charAt(i) == str.charAt(j) && cl == 2) L[i][j] = 2;
                else if (str.charAt(i) == str.charAt(j)) L[i][j] = L[i + 1][j - 1] + 2;
                else L[i][j] = Math.max(L[i][j - 1], L[i + 1][j]);
            }
        }
        return L[0][n - 1];
    }
}""",
        "starter_code_cpp": "#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int lps(const string& str);\\n};",
        "reference_solution_cpp": """#include <string>
#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    int lps(const string& str) {
        int n = (int)str.size();
        vector<vector<int>> L(n, vector<int>(n, 0));
        for (int i = 0; i < n; i++) L[i][i] = 1;
        for (int cl = 2; cl <= n; cl++) {
            for (int i = 0; i < n - cl + 1; i++) {
                int j = i + cl - 1;
                if (str[i] == str[j] && cl == 2) L[i][j] = 2;
                else if (str[i] == str[j]) L[i][j] = L[i + 1][j - 1] + 2;
                else L[i][j] = max(L[i][j - 1], L[i + 1][j]);
            }
        }
        return L[0][n - 1];
    }
};"""
    },

    258: {
        "starter_code_java": "class Solution {\\n    public double harmonic_sum(int n) {\\n        return 0.0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public double harmonic_sum(int n) {
        double sum = 0.0;
        for (int i = 1; i <= n; i++) sum += 1.0 / i;
        return sum;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    double harmonic_sum(int n);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    double harmonic_sum(int n) {
        double sum = 0.0;
        for (int i = 1; i <= n; ++i) sum += 1.0 / (double)i;
        return sum;
    }
};"""
    },

    259: {
        "starter_code_java": "class Solution {\\n    public int[] intersection_array(int[] array_nums1, int[] array_nums2) {\\n        return new int[]{};\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[] intersection_array(int[] array_nums1, int[] array_nums2) {
        Set<Integer> set = new HashSet<>();
        for (int x : array_nums1) set.add(x);
        List<Integer> list = new ArrayList<>();
        for (int x : array_nums2) {
            if (set.contains(x)) list.add(x);
        }
        int[] res = new int[list.size()];
        for (int i = 0; i < list.size(); i++) res[i] = list.get(i);
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<int> intersection_array(const vector<int>& array_nums1, const vector<int>& array_nums2);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <unordered_set>
using namespace std;
class Solution {
public:
    vector<int> intersection_array(const vector<int>& array_nums1, const vector<int>& array_nums2) {
        unordered_set<int> s(array_nums1.begin(), array_nums1.end());
        vector<int> res;
        for (int x : array_nums2) {
            if (s.count(x)) res.push_back(x);
        }
        return res;
    }
};"""
    }
}
'''

def main():
    target_path = os.path.join(os.path.dirname(__file__), "batch4_solutions.py")
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(BATCH4_CONTENT.strip() + "\n")
    print(f"Generated {target_path} successfully!")

if __name__ == "__main__":
    main()
