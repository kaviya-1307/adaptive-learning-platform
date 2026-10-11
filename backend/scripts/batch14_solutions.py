"""
Curated and specialized solutions for MBPP problems (Batch 14: 711-760).
"""

BATCH14_SOLUTIONS = {
    711: {
        "starter_code_javascript": "function get_Pairs_Count(arr, n, sum) {\n    return 0;\n}",
        "reference_solution_javascript": """function get_Pairs_Count(arr, n, sum) {
    let count = 0;
    for (let i = 0; i < n; i++) {
        for (let j = i + 1; j < n; j++) {
            if (arr[i] + arr[j] === sum) count++;
        }
    }
    return count;
}""",
        "starter_code_java": "class Solution {\n    public int get_Pairs_Count(int[] arr, int n, int sum) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int get_Pairs_Count(int[] arr, int n, int sum) {
        int count = 0;
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                if (arr[i] + arr[j] == sum) count++;
            }
        }
        return count;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    int get_Pairs_Count(const std::vector<int>& arr, int n, int sum);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    int get_Pairs_Count(const std::vector<int>& arr, int n, int sum) {
        int count = 0;
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                if (arr[i] + arr[j] == sum) count++;
            }
        }
        return count;
    }
};"""
    },

    712: {
        "starter_code_javascript": "function check_Odd_Parity(x) {\n    return false;\n}",
        "reference_solution_javascript": """function check_Odd_Parity(x) {
    let parity = 0;
    while (x !== 0) {
        x = x & (x - 1);
        parity++;
    }
    return parity % 2 === 1;
}""",
        "starter_code_java": "class Solution {\n    public boolean check_Odd_Parity(int x) {\n        return false;\n    }\n}",
        "reference_solution_java": """class Solution {
    public boolean check_Odd_Parity(int x) {
        int parity = 0;
        while (x != 0) {
            x = x & (x - 1);
            parity++;
        }
        return parity % 2 == 1;
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    bool check_Odd_Parity(int x);\n};",
        "reference_solution_cpp": """class Solution {
public:
    bool check_Odd_Parity(int x) {
        int parity = 0;
        while (x != 0) {
            x = x & (x - 1);
            parity++;
        }
        return parity % 2 == 1;
    }
};"""
    },

    713: {
        "starter_code_javascript": "function Diff(li1, li2) {\n    return [];\n}",
        "reference_solution_javascript": """function Diff(li1, li2) {
    const s1 = new Set(li1);
    const s2 = new Set(li2);
    const d1 = [...s1].filter(x => !s2.has(x)).sort((a, b) => (a & 7) - (b & 7));
    const d2 = [...s2].filter(x => !s1.has(x)).sort((a, b) => (a & 7) - (b & 7));
    return d1.concat(d2);
}""",
        "starter_code_java": "import java.util.*;\nclass Solution {\n    public int[] Diff(int[] li1, int[] li2) {\n        return new int[]{};\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[] Diff(int[] li1, int[] li2) {
        Set<Integer> s1 = new HashSet<>();
        for (int x : li1) s1.add(x);
        Set<Integer> s2 = new HashSet<>();
        for (int x : li2) s2.add(x);
        List<Integer> d1 = new ArrayList<>();
        for (int x : s1) if (!s2.contains(x)) d1.add(x);
        d1.sort(Comparator.comparingInt(a -> (a & 7)));
        List<Integer> d2 = new ArrayList<>();
        for (int x : s2) if (!s1.contains(x)) d2.add(x);
        d2.sort(Comparator.comparingInt(a -> (a & 7)));
        int[] res = new int[d1.size() + d2.size()];
        int idx = 0;
        for (int x : d1) res[idx++] = x;
        for (int x : d2) res[idx++] = x;
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    std::vector<int> Diff(std::vector<int> li1, std::vector<int> li2);\n};",
        "reference_solution_cpp": """#include <vector>
#include <unordered_set>
#include <algorithm>
class Solution {
public:
    std::vector<int> Diff(std::vector<int> li1, std::vector<int> li2) {
        std::unordered_set<int> s1(li1.begin(), li1.end());
        std::unordered_set<int> s2(li2.begin(), li2.end());
        std::vector<int> d1, d2;
        for (int x : s1) if (s2.find(x) == s2.end()) d1.push_back(x);
        std::sort(d1.begin(), d1.end(), [](int a, int b) { return (a & 7) < (b & 7); });
        for (int x : s2) if (s1.find(x) == s1.end()) d2.push_back(x);
        std::sort(d2.begin(), d2.end(), [](int a, int b) { return (a & 7) < (b & 7); });
        d1.insert(d1.end(), d2.begin(), d2.end());
        return d1;
    }
};"""
    },

    714: {
        "starter_code_javascript": "function odd_Num_Sum(n) {\n    return 0;\n}",
        "reference_solution_javascript": """function odd_Num_Sum(n) {
    let sm = 0;
    for (let i = 1; i <= n; i++) {
        let j = 2 * i - 1;
        sm += j * j * j * j;
    }
    return sm;
}""",
        "starter_code_java": "class Solution {\n    public int odd_Num_Sum(int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int odd_Num_Sum(int n) {
        int sm = 0;
        for (int i = 1; i <= n; i++) {
            int j = 2 * i - 1;
            sm += j * j * j * j;
        }
        return sm;
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    int odd_Num_Sum(int n);\n};",
        "reference_solution_cpp": """class Solution {
public:
    int odd_Num_Sum(int n) {
        int sm = 0;
        for (int i = 1; i <= n; i++) {
            int j = 2 * i - 1;
            sm += j * j * j * j;
        }
        return sm;
    }
};"""
    },

    715: {
        "starter_code_javascript": "function check_expression(exp) {\n    return false;\n}",
        "reference_solution_javascript": """function check_expression(exp) {
    if ((exp.length & 1) !== 0) return false;
    let stack = [];
    for (let ch of exp) {
        if (ch === '(' || ch === '{' || ch === '[') {
            stack.push(ch);
        } else if (ch === ')' || ch === '}' || ch === ']') {
            if (stack.length === 0) return false;
            let top = stack.pop();
            if ((top === '(' && ch !== ')') || (top === '{' && ch !== '}') || (top === '[' && ch !== ']')) {
                return false;
            }
        }
    }
    return stack.length === 0;
}""",
        "starter_code_java": "import java.util.*;\nclass Solution {\n    public boolean check_expression(String exp) {\n        return false;\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public boolean check_expression(String exp) {
        if ((exp.length() & 1) != 0) return false;
        Deque<Character> stack = new ArrayDeque<>();
        for (int i = 0; i < exp.length(); i++) {
            char ch = exp.charAt(i);
            if (ch == '(' || ch == '{' || ch == '[') {
                stack.push(ch);
            } else if (ch == ')' || ch == '}' || ch == ']') {
                if (stack.isEmpty()) return false;
                char top = stack.pop();
                if ((top == '(' && ch != ')') || (top == '{' && ch != '}') || (top == '[' && ch != ']')) {
                    return false;
                }
            }
        }
        return stack.isEmpty();
    }
}""",
        "starter_code_cpp": "#include <string>\nclass Solution {\npublic:\n    bool check_expression(std::string exp);\n};",
        "reference_solution_cpp": """#include <string>
#include <stack>
class Solution {
public:
    bool check_expression(std::string exp) {
        if ((exp.length() & 1) != 0) return false;
        std::stack<char> st;
        for (char ch : exp) {
            if (ch == '(' || ch == '{' || ch == '[') {
                st.push(ch);
            } else if (ch == ')' || ch == '}' || ch == ']') {
                if (st.empty()) return false;
                char top = st.top();
                st.pop();
                if ((top == '(' && ch != ')') || (top == '{' && ch != '}') || (top == '[' && ch != ']')) {
                    return false;
                }
            }
        }
        return st.empty();
    }
};"""
    },

    716: {
        "starter_code_javascript": "function remove_length(test_str, K) {\n    return '';\n}",
        "reference_solution_javascript": """function remove_length(test_str, K) {
    return test_str.split(/\\s+/).filter(w => w.length !== K).join(' ');
}""",
        "starter_code_java": "class Solution {\n    public String remove_length(String test_str, int K) {\n        return "";\n    }\n}",
        "reference_solution_java": """class Solution {
    public String remove_length(String test_str, int K) {
        String[] words = test_str.split("\\s+");
        StringBuilder sb = new StringBuilder();
        for (String w : words) {
            if (w.length() != K) {
                if (sb.length() > 0) sb.append(" ");
                sb.append(w);
            }
        }
        return sb.toString();
    }
}""",
        "starter_code_cpp": "#include <string>\nclass Solution {\npublic:\n    std::string remove_length(std::string test_str, int K);\n};",
        "reference_solution_cpp": """#include <string>
#include <sstream>
class Solution {
public:
    std::string remove_length(std::string test_str, int K) {
        std::istringstream iss(test_str);
        std::string word, res;
        while (iss >> word) {
            if ((int)word.length() != K) {
                if (!res.empty()) res += " ";
                res += word;
            }
        }
        return res;
    }
};"""
    },

    717: {
        "starter_code_javascript": "function check_email(email) {\n    return '';\n}",
        "reference_solution_javascript": """function check_email(email) {
    const re = /^[a-z0-9]+[._]?[a-z0-9]+@[a-zA-Z0-9_]+[.][a-zA-Z0-9_]{2,3}$/;
    return re.test(email) ? "Valid Email" : "Invalid Email";
}""",
        "starter_code_java": "class Solution {\n    public String check_email(String email) {\n        return "";\n    }\n}",
        "reference_solution_java": """import java.util.regex.*;
class Solution {
    public String check_email(String email) {
        String regex = "^[a-z0-9]+[._]?[a-z0-9]+@[a-zA-Z0-9_]+[.][a-zA-Z0-9_]{2,3}$";
        return Pattern.compile(regex).matcher(email).matches() ? "Valid Email" : "Invalid Email";
    }
}""",
        "starter_code_cpp": "#include <string>\nclass Solution {\npublic:\n    std::string check_email(std::string email);\n};",
        "reference_solution_cpp": """#include <string>
#include <regex>
class Solution {
public:
    std::string check_email(std::string email) {
        std::regex re("^[a-z0-9]+[._]?[a-z0-9]+@[a-zA-Z0-9_]+[.][a-zA-Z0-9_]{2,3}$");
        return std::regex_match(email, re) ? "Valid Email" : "Invalid Email";
    }
};"""
    },

    718: {
        "starter_code_javascript": "function odd_position(nums) {\n    return false;\n}",
        "reference_solution_javascript": """function odd_position(nums) {
    for (let i = 0; i < nums.length; i++) {
        if (nums[i] % 2 !== i % 2) return false;
    }
    return true;
}""",
        "starter_code_java": "class Solution {\n    public boolean odd_position(int[] nums) {\n        return false;\n    }\n}",
        "reference_solution_java": """class Solution {
    public boolean odd_position(int[] nums) {
        for (int i = 0; i < nums.length; i++) {
            if (nums[i] % 2 != i % 2) return false;
        }
        return true;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    bool odd_position(std::vector<int> nums);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    bool odd_position(std::vector<int> nums) {
        for (size_t i = 0; i < nums.size(); i++) {
            if (nums[i] % 2 != (int)(i % 2)) return false;
        }
        return true;
    }
};"""
    },

    719: {
        "starter_code_javascript": "function count_vowels(test_str) {\n    return 0;\n}",
        "reference_solution_javascript": """function count_vowels(test_str) {
    let res = 0;
    const isVow = (c) => 'aeiou'.includes(c);
    for (let idx = 1; idx < test_str.length - 1; idx++) {
        if (!isVow(test_str[idx]) && (isVow(test_str[idx - 1]) || isVow(test_str[idx + 1]))) {
            res++;
        }
    }
    if (!isVow(test_str[0]) && isVow(test_str[1])) res++;
    if (!isVow(test_str[test_str.length - 1]) && isVow(test_str[test_str.length - 2])) res++;
    return res;
}""",
        "starter_code_java": "class Solution {\n    public int count_vowels(String test_str) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    private boolean isVow(char c) {
        return "aeiou".indexOf(c) != -1;
    }
    public int count_vowels(String test_str) {
        int res = 0;
        int n = test_str.length();
        for (int idx = 1; idx < n - 1; idx++) {
            if (!isVow(test_str.charAt(idx)) && (isVow(test_str.charAt(idx - 1)) || isVow(test_str.charAt(idx + 1)))) {
                res++;
            }
        }
        if (!isVow(test_str.charAt(0)) && isVow(test_str.charAt(1))) res++;
        if (!isVow(test_str.charAt(n - 1)) && isVow(test_str.charAt(n - 2))) res++;
        return res;
    }
}""",
        "starter_code_cpp": "#include <string>\nclass Solution {\npublic:\n    int count_vowels(std::string test_str);\n};",
        "reference_solution_cpp": """#include <string>
class Solution {
    bool isVow(char c) {
        return c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u';
    }
public:
    int count_vowels(std::string test_str) {
        int res = 0;
        int n = test_str.length();
        for (int idx = 1; idx < n - 1; idx++) {
            if (!isVow(test_str[idx]) && (isVow(test_str[idx - 1]) || isVow(test_str[idx + 1]))) {
                res++;
            }
        }
        if (!isVow(test_str[0]) && isVow(test_str[1])) res++;
        if (!isVow(test_str[n - 1]) && isVow(test_str[n - 2])) res++;
        return res;
    }
};"""
    },

    720: {
        "starter_code_javascript": "function find_Sum(arr, n) {\n    return 0;\n}",
        "reference_solution_javascript": """function find_Sum(arr, n) {
    const s = new Set(arr);
    let sum = 0;
    for (let x of s) sum += x;
    return sum;
}""",
        "starter_code_java": "import java.util.*;\nclass Solution {\n    public int find_Sum(int[] arr, int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int find_Sum(int[] arr, int n) {
        Set<Integer> set = new HashSet<>();
        int sum = 0;
        for (int i = 0; i < n; i++) {
            if (set.add(arr[i])) sum += arr[i];
        }
        return sum;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    int find_Sum(std::vector<int> arr, int n);\n};",
        "reference_solution_cpp": """#include <vector>
#include <unordered_set>
class Solution {
public:
    int find_Sum(std::vector<int> arr, int n) {
        std::unordered_set<int> set;
        int sum = 0;
        for (int i = 0; i < n; i++) {
            if (set.insert(arr[i]).second) sum += arr[i];
        }
        return sum;
    }
};"""
    },

    721: {
        "starter_code_javascript": "function pack_consecutive_duplicates(list1) {\n    return [];\n}",
        "reference_solution_javascript": """function pack_consecutive_duplicates(list1) {
    if (!list1 || list1.length === 0) return [];
    let res = [];
    let cur = [list1[0]];
    for (let i = 1; i < list1.length; i++) {
        if (list1[i] === list1[i - 1]) cur.push(list1[i]);
        else { res.push(cur); cur = [list1[i]]; }
    }
    res.push(cur);
    return res;
}""",
        "starter_code_java": "import java.util.*;\nclass Solution {\n    public int[][] pack_consecutive_duplicates(int[] list1) {\n        return new int[][]{};\n    }\n    public String[][] pack_consecutive_duplicates(String[] list1) {\n        return new String[][]{};\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[][] pack_consecutive_duplicates(int[] list1) {
        if (list1 == null || list1.length == 0) return new int[0][0];
        List<int[]> res = new ArrayList<>();
        int i = 0;
        while (i < list1.length) {
            int j = i;
            while (j < list1.length && list1[j] == list1[i]) j++;
            int[] group = new int[j - i];
            Arrays.fill(group, list1[i]);
            res.add(group);
            i = j;
        }
        return res.toArray(new int[res.size()][]);
    }
    public String[][] pack_consecutive_duplicates(String[] list1) {
        if (list1 == null || list1.length == 0) return new String[0][0];
        List<String[]> res = new ArrayList<>();
        int i = 0;
        while (i < list1.length) {
            int j = i;
            while (j < list1.length && list1[j].equals(list1[i])) j++;
            String[] group = new String[j - i];
            Arrays.fill(group, list1[i]);
            res.add(group);
            i = j;
        }
        return res.toArray(new String[res.size()][]);
    }
}""",
        "starter_code_cpp": "#include <vector>\n#include <string>\nclass Solution {\npublic:\n    std::vector<std::vector<int>> pack_consecutive_duplicates(const std::vector<int>& list1);\n    std::vector<std::vector<std::string>> pack_consecutive_duplicates(const std::vector<std::string>& list1);\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
class Solution {
public:
    std::vector<std::vector<int>> pack_consecutive_duplicates(const std::vector<int>& list1) {
        std::vector<std::vector<int>> res;
        if (list1.empty()) return res;
        std::vector<int> cur = {list1[0]};
        for (size_t i = 1; i < list1.size(); ++i) {
            if (list1[i] == list1[i - 1]) cur.push_back(list1[i]);
            else { res.push_back(cur); cur = {list1[i]}; }
        }
        res.push_back(cur);
        return res;
    }
    std::vector<std::vector<std::string>> pack_consecutive_duplicates(const std::vector<std::string>& list1) {
        std::vector<std::vector<std::string>> res;
        if (list1.empty()) return res;
        std::vector<std::string> cur = {list1[0]};
        for (size_t i = 1; i < list1.size(); ++i) {
            if (list1[i] == list1[i - 1]) cur.push_back(list1[i]);
            else { res.push_back(cur); cur = {list1[i]}; }
        }
        res.push_back(cur);
        return res;
    }
};"""
    },

    722: {
        "starter_code_javascript": "function count_Divisors(n) {\n    return '';\n}",
        "reference_solution_javascript": """function count_Divisors(n) {
    let count = 0;
    for (let i = 1; i * i <= n; i++) {
        if (n % i === 0) {
            if (Math.floor(n / i) === i) count += 1;
            else count += 2;
        }
    }
    return count % 2 === 0 ? "Even" : "Odd";
}""",
        "starter_code_java": "class Solution {\n    public String count_Divisors(int n) {\n        return "";\n    }\n}",
        "reference_solution_java": """class Solution {
    public String count_Divisors(int n) {
        int count = 0;
        for (int i = 1; i * i <= n; i++) {
            if (n % i == 0) {
                if (n / i == i) count += 1;
                else count += 2;
            }
        }
        return count % 2 == 0 ? "Even" : "Odd";
    }
}""",
        "starter_code_cpp": "#include <string>\nclass Solution {\npublic:\n    std::string count_Divisors(int n);\n};",
        "reference_solution_cpp": """#include <string>
class Solution {
public:
    std::string count_Divisors(int n) {
        int count = 0;
        for (int i = 1; i * i <= n; i++) {
            if (n % i == 0) {
                if (n / i == i) count += 1;
                else count += 2;
            }
        }
        return count % 2 == 0 ? "Even" : "Odd";
    }
};"""
    },

    723: {
        "starter_code_javascript": "function Odd_Length_Sum(arr) {\n    return 0;\n}",
        "reference_solution_javascript": """function Odd_Length_Sum(arr) {
    let sum = 0;
    const l = arr.length;
    for (let i = 0; i < l; i++) {
        sum += Math.floor(((i + 1) * (l - i) + 1) / 2) * arr[i];
    }
    return sum;
}""",
        "starter_code_java": "class Solution {\n    public int Odd_Length_Sum(int[] arr) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int Odd_Length_Sum(int[] arr) {
        int sum = 0;
        int l = arr.length;
        for (int i = 0; i < l; i++) {
            sum += (((i + 1) * (l - i) + 1) / 2) * arr[i];
        }
        return sum;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    int Odd_Length_Sum(std::vector<int> arr);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    int Odd_Length_Sum(std::vector<int> arr) {
        int sum = 0;
        int l = arr.size();
        for (int i = 0; i < l; i++) {
            sum += (((i + 1) * (l - i) + 1) / 2) * arr[i];
        }
        return sum;
    }
};"""
    },

    724: {
        "starter_code_javascript": "function mul_even_odd(list1) {\n    return 0;\n}",
        "reference_solution_javascript": """function mul_even_odd(list1) {
    let first_even = -1, first_odd = -1;
    for (let el of list1) {
        if (first_even === -1 && el % 2 === 0) first_even = el;
        if (first_odd === -1 && el % 2 !== 0) first_odd = el;
        if (first_even !== -1 && first_odd !== -1) break;
    }
    return first_even * first_odd;
}""",
        "starter_code_java": "class Solution {\n    public int mul_even_odd(int[] list1) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int mul_even_odd(int[] list1) {
        int first_even = -1, first_odd = -1;
        for (int el : list1) {
            if (first_even == -1 && el % 2 == 0) first_even = el;
            if (first_odd == -1 && el % 2 != 0) first_odd = el;
            if (first_even != -1 && first_odd != -1) break;
        }
        return first_even * first_odd;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    int mul_even_odd(std::vector<int> list1);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    int mul_even_odd(std::vector<int> list1) {
        int first_even = -1, first_odd = -1;
        for (int el : list1) {
            if (first_even == -1 && el % 2 == 0) first_even = el;
            if (first_odd == -1 && el % 2 != 0) first_odd = el;
            if (first_even != -1 && first_odd != -1) break;
        }
        return first_even * first_odd;
    }
};"""
    },

    725: {
        "starter_code_javascript": "function right_insertion(a, x) {\n    return 0;\n}",
        "reference_solution_javascript": """function right_insertion(a, x) {
    let low = 0, high = a.length;
    while (low < high) {
        let mid = Math.floor((low + high) / 2);
        if (a[mid] <= x) low = mid + 1;
        else high = mid;
    }
    return low;
}""",
        "starter_code_java": "class Solution {\n    public int right_insertion(int[] a, int x) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int right_insertion(int[] a, int x) {
        int low = 0, high = a.length;
        while (low < high) {
            int mid = (low + high) / 2;
            if (a[mid] <= x) low = mid + 1;
            else high = mid;
        }
        return low;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    int right_insertion(std::vector<int> a, int x);\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
class Solution {
public:
    int right_insertion(std::vector<int> a, int x) {
        return std::upper_bound(a.begin(), a.end(), x) - a.begin();
    }
};"""
    },

    726: {
        "starter_code_javascript": "function text_match_three(text) {\n    return '';\n}",
        "reference_solution_javascript": """function text_match_three(text) {
    return /ab{3}/.test(text) ? "Found a match!" : "Not matched!";
}""",
        "starter_code_java": "class Solution {\n    public String text_match_three(String text) {\n        return "";\n    }\n}",
        "reference_solution_java": """import java.util.regex.*;
class Solution {
    public String text_match_three(String text) {
        return Pattern.compile("ab{3}").matcher(text).find() ? "Found a match!" : "Not matched!";
    }
}""",
        "starter_code_cpp": "#include <string>\nclass Solution {\npublic:\n    std::string text_match_three(std::string text);\n};",
        "reference_solution_cpp": """#include <string>
#include <regex>
class Solution {
public:
    std::string text_match_three(std::string text) {
        std::regex re("ab{3}");
        return std::regex_search(text, re) ? "Found a match!" : "Not matched!";
    }
};"""
    },

    727: {
        "starter_code_javascript": "function perimeter_polygon(s, l) {\n    return 0;\n}",
        "reference_solution_javascript": """function perimeter_polygon(s, l) {
    return s * l;
}""",
        "starter_code_java": "class Solution {\n    public int perimeter_polygon(int s, int l) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int perimeter_polygon(int s, int l) {
        return s * l;
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    int perimeter_polygon(int s, int l);\n};",
        "reference_solution_cpp": """class Solution {
public:
    int perimeter_polygon(int s, int l) {
        return s * l;
    }
};"""
    },

    728: {
        "starter_code_javascript": "function even_position(nums) {\n    return false;\n}",
        "reference_solution_javascript": """function even_position(nums) {
    for (let i = 0; i < nums.length; i++) {
        if (nums[i] % 2 !== i % 2) return false;
    }
    return true;
}""",
        "starter_code_java": "class Solution {\n    public boolean even_position(int[] nums) {\n        return false;\n    }\n}",
        "reference_solution_java": """class Solution {
    public boolean even_position(int[] nums) {
        for (int i = 0; i < nums.length; i++) {
            if (nums[i] % 2 != i % 2) return false;
        }
        return true;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    bool even_position(std::vector<int> nums);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    bool even_position(std::vector<int> nums) {
        for (size_t i = 0; i < nums.size(); i++) {
            if (nums[i] % 2 != (int)(i % 2)) return false;
        }
        return true;
    }
};"""
    },

    729: {
        "starter_code_javascript": "function count_list(input_list) {\n    return 0;\n}",
        "reference_solution_javascript": """function count_list(input_list) {
    return input_list.length;
}""",
        "starter_code_java": "class Solution {\n    public int count_list(int[][] input_list) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int count_list(int[][] input_list) {
        return input_list.length;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    int count_list(std::vector<std::vector<int>> input_list);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    int count_list(std::vector<std::vector<int>> input_list) {
        return input_list.size();
    }
};"""
    },

    730: {
        "starter_code_javascript": "function last(arr, x, n) {\n    return 0;\n}",
        "reference_solution_javascript": """function last(arr, x, n) {
    let low = 0, high = n - 1, res = -1;
    while (low <= high) {
        let mid = Math.floor((low + high) / 2);
        if (arr[mid] > x) high = mid - 1;
        else if (arr[mid] < x) low = mid + 1;
        else { res = mid; low = mid + 1; }
    }
    return res;
}""",
        "starter_code_java": "class Solution {\n    public int last(int[] arr, int x, int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int last(int[] arr, int x, int n) {
        int low = 0, high = n - 1, res = -1;
        while (low <= high) {
            int mid = (low + high) / 2;
            if (arr[mid] > x) high = mid - 1;
            else if (arr[mid] < x) low = mid + 1;
            else { res = mid; low = mid + 1; }
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    int last(std::vector<int> arr, int x, int n);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    int last(std::vector<int> arr, int x, int n) {
        int low = 0, high = n - 1, res = -1;
        while (low <= high) {
            int mid = (low + high) / 2;
            if (arr[mid] > x) high = mid - 1;
            else if (arr[mid] < x) low = mid + 1;
            else { res = mid; low = mid + 1; }
        }
        return res;
    }
};"""
    },

    731: {
        "starter_code_javascript": "function text_starta_endb(text) {\n    return '';\n}",
        "reference_solution_javascript": """function text_starta_endb(text) {
    return /^a.*b$/.test(text) ? "Found a match!" : "Not matched!";
}""",
        "starter_code_java": "class Solution {\n    public String text_starta_endb(String text) {\n        return "";\n    }\n}",
        "reference_solution_java": """import java.util.regex.*;
class Solution {
    public String text_starta_endb(String text) {
        return Pattern.compile("^a.*b$").matcher(text).matches() ? "Found a match!" : "Not matched!";
    }
}""",
        "starter_code_cpp": "#include <string>\nclass Solution {\npublic:\n    std::string text_starta_endb(std::string text);\n};",
        "reference_solution_cpp": """#include <string>
#include <regex>
class Solution {
public:
    std::string text_starta_endb(std::string text) {
        std::regex re("^a.*b$");
        return std::regex_match(text, re) ? "Found a match!" : "Not matched!";
    }
};"""
    },

    732: {
        "starter_code_javascript": "function cheap_items(items, n) {\n    return [];\n}",
        "reference_solution_javascript": """function cheap_items(items, n) {
    return [...items].sort((a, b) => a.price - b.price).slice(0, n);
}""",
        "starter_code_java": "import java.util.*;\nclass Solution {\n    public Object[] cheap_items(Object[] items, int n) {\n        return new Object[]{};\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public Object[] cheap_items(Object[] items, int n) {
        List<Map<String, Object>> list = new ArrayList<>();
        for (Object o : items) {
            list.add((Map<String, Object>) o);
        }
        list.sort(Comparator.comparingDouble(m -> ((Number) m.get("price")).doubleValue()));
        int count = Math.min(n, list.size());
        return list.subList(0, count).toArray(new Object[count]);
    }
}""",
        "starter_code_cpp": "#include <vector>\n#include <string>\n#include <unordered_map>\nclass Solution {\npublic:\n    std::vector<std::unordered_map<std::string, std::string>> cheap_items(std::vector<std::unordered_map<std::string, std::string>> items, int n);\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <unordered_map>
#include <algorithm>
class Solution {
public:
    std::vector<std::unordered_map<std::string, std::string>> cheap_items(std::vector<std::unordered_map<std::string, std::string>> items, int n) {
        std::stable_sort(items.begin(), items.end(), [](const auto& a, const auto& b) {
            return std::stod(a.at("price")) < std::stod(b.at("price"));
        });
        if (n < (int)items.size()) items.resize(n);
        return items;
    }
};"""
    },

    733: {
        "starter_code_javascript": "function return_sum(dict) {\n    return 0;\n}",
        "reference_solution_javascript": """function return_sum(dict) {
    let sum = 0;
    for (let k in dict) sum += dict[k];
    return sum;
}""",
        "starter_code_java": "import java.util.*;\nclass Solution {\n    public int return_sum(Map<Object, Object> dict) {\n        return 0;\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int return_sum(Map<Object, Object> dict) {
        int sum = 0;
        for (Object v : dict.values()) {
            if (v instanceof Number) sum += ((Number) v).intValue();
        }
        return sum;
    }
}""",
        "starter_code_cpp": "#include <unordered_map>\n#include <string>\nclass Solution {\npublic:\n    int return_sum(std::unordered_map<std::string, int> dict);\n};",
        "reference_solution_cpp": """#include <unordered_map>
#include <string>
class Solution {
public:
    int return_sum(std::unordered_map<std::string, int> dict) {
        int sum = 0;
        for (const auto& p : dict) sum += p.second;
        return sum;
    }
};"""
    },

    734: {
        "starter_code_javascript": "function sum_in_Range(l, r) {\n    return 0;\n}",
        "reference_solution_javascript": """function sum_in_Range(l, r) {
    const sumOdd = (n) => {
        let terms = Math.floor((n + 1) / 2);
        return terms * terms;
    };
    return sumOdd(r) - sumOdd(l - 1);
}""",
        "starter_code_java": "class Solution {\n    public int sum_in_Range(int l, int r) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    private int sumOdd(int n) {
        int terms = (n + 1) / 2;
        return terms * terms;
    }
    public int sum_in_Range(int l, int r) {
        return sumOdd(r) - sumOdd(l - 1);
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    int sum_in_Range(int l, int r);\n};",
        "reference_solution_cpp": """class Solution {
    int sumOdd(int n) {
        int terms = (n + 1) / 2;
        return terms * terms;
    }
public:
    int sum_in_Range(int l, int r) {
        return sumOdd(r) - sumOdd(l - 1);
    }
};"""
    },

    735: {
        "starter_code_javascript": "function _sum(arr) {\n    return 0;\n}",
        "reference_solution_javascript": """function _sum(arr) {
    return arr.reduce((a, b) => a + b, 0);
}""",
        "starter_code_java": "class Solution {\n    public int _sum(int[] arr) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int _sum(int[] arr) {
        int sum = 0;
        for (int x : arr) sum += x;
        return sum;
    }
}""",
        "starter_code_cpp": "#include <vector>\n#include <numeric>\nclass Solution {\npublic:\n    int _sum(std::vector<int> arr);\n};",
        "reference_solution_cpp": """#include <vector>
#include <numeric>
class Solution {
public:
    int _sum(std::vector<int> arr) {
        return std::accumulate(arr.begin(), arr.end(), 0);
    }
};"""
    },

    736: {
        "starter_code_javascript": "function left_Rotate(n, d) {\n    return 0;\n}",
        "reference_solution_javascript": """function left_Rotate(n, d) {
    return ((n << d) | (n >>> (32 - d))) >>> 0;
}""",
        "starter_code_java": "class Solution {\n    public int left_Rotate(int n, int d) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int left_Rotate(int n, int d) {
        return (n << d) | (n >>> (32 - d));
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    int left_Rotate(int n, int d);\n};",
        "reference_solution_cpp": """class Solution {
public:
    int left_Rotate(int n, int d) {
        return (n << d) | ((unsigned int)n >> (32 - d));
    }
};"""
    },

    737: {
        "starter_code_javascript": "function remove_all_spaces(text) {\n    return '';\n}",
        "reference_solution_javascript": """function remove_all_spaces(text) {
    return text.replace(/\\s+/g, '');
}""",
        "starter_code_java": "class Solution {\n    public String remove_all_spaces(String text) {\n        return "";\n    }\n}",
        "reference_solution_java": """class Solution {
    public String remove_all_spaces(String text) {
        return text.replaceAll("\\s+", "");
    }
}""",
        "starter_code_cpp": "#include <string>\nclass Solution {\npublic:\n    std::string remove_all_spaces(std::string text);\n};",
        "reference_solution_cpp": """#include <string>
#include <cctype>
class Solution {
public:
    std::string remove_all_spaces(std::string text) {
        std::string res;
        for (char c : text) {
            if (!isspace((unsigned char)c)) res += c;
        }
        return res;
    }
};"""
    },

    738: {
        "starter_code_javascript": "function test_three_equal(x, y, z) {\n    return 0;\n}",
        "reference_solution_javascript": """function test_three_equal(x, y, z) {
    const s = new Set([x, y, z]);
    if (s.size === 3) return 0;
    return 4 - s.size;
}""",
        "starter_code_java": "import java.util.*;\nclass Solution {\n    public int test_three_equal(int x, int y, int z) {\n        return 0;\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int test_three_equal(int x, int y, int z) {
        Set<Integer> set = new HashSet<>(Arrays.asList(x, y, z));
        if (set.size() == 3) return 0;
        return 4 - set.size();
    }
}""",
        "starter_code_cpp": "#include <unordered_set>\nclass Solution {\npublic:\n    int test_three_equal(int x, int y, int z);\n};",
        "reference_solution_cpp": """#include <unordered_set>
class Solution {
public:
    int test_three_equal(int x, int y, int z) {
        std::unordered_set<int> s = {x, y, z};
        if (s.size() == 3) return 0;
        return 4 - (int)s.size();
    }
};"""
    },

    739: {
        "starter_code_javascript": "function count_Rotation(arr, n) {\n    return 0;\n}",
        "reference_solution_javascript": """function count_Rotation(arr, n) {
    for (let i = 1; i < n; i++) {
        if (arr[i] < arr[i - 1]) return i;
    }
    return 0;
}""",
        "starter_code_java": "class Solution {\n    public int count_Rotation(int[] arr, int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int count_Rotation(int[] arr, int n) {
        for (int i = 1; i < n; i++) {
            if (arr[i] < arr[i - 1]) return i;
        }
        return 0;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    int count_Rotation(std::vector<int> arr, int n);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    int count_Rotation(std::vector<int> arr, int n) {
        for (int i = 1; i < n; i++) {
            if (arr[i] < arr[i - 1]) return i;
        }
        return 0;
    }
};"""
    },

    740: {
        "starter_code_javascript": "function is_Perfect_Square(n) {\n    return false;\n}",
        "reference_solution_javascript": """function is_Perfect_Square(n) {
    if (n < 0) return false;
    let s = Math.round(Math.sqrt(n));
    return s * s === n;
}""",
        "starter_code_java": "class Solution {\n    public boolean is_Perfect_Square(int n) {\n        return false;\n    }\n}",
        "reference_solution_java": """class Solution {
    public boolean is_Perfect_Square(int n) {
        if (n < 0) return false;
        long s = Math.round(Math.sqrt(n));
        return s * s == n;
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    bool is_Perfect_Square(int n);\n};",
        "reference_solution_cpp": """#include <cmath>
class Solution {
public:
    bool is_Perfect_Square(int n) {
        if (n < 0) return false;
        long long s = std::round(std::sqrt(n));
        return s * s == n;
    }
};"""
    },

    741: {
        "starter_code_javascript": "function is_Product_Even(arr, n) {\n    return false;\n}",
        "reference_solution_javascript": """function is_Product_Even(arr, n) {
    for (let i = 0; i < n; i++) {
        if ((arr[i] & 1) === 0) return true;
    }
    return false;
}""",
        "starter_code_java": "class Solution {\n    public boolean is_Product_Even(int[] arr, int n) {\n        return false;\n    }\n}",
        "reference_solution_java": """class Solution {
    public boolean is_Product_Even(int[] arr, int n) {
        for (int i = 0; i < n; i++) {
            if ((arr[i] & 1) == 0) return true;
        }
        return false;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    bool is_Product_Even(std::vector<int> arr, int n);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    bool is_Product_Even(std::vector<int> arr, int n) {
        for (int i = 0; i < n; i++) {
            if ((arr[i] & 1) == 0) return true;
        }
        return false;
    }
};"""
    },

    742: {
        "starter_code_javascript": "function max_sum_list(lists) {\n    return [];\n}",
        "reference_solution_javascript": """function max_sum_list(lists) {
    let best = lists[0];
    let bestSum = best.reduce((a, b) => a + b, 0);
    for (let i = 1; i < lists.length; i++) {
        let curSum = lists[i].reduce((a, b) => a + b, 0);
        if (curSum > bestSum) {
            bestSum = curSum;
            best = lists[i];
        }
    }
    return best;
}""",
        "starter_code_java": "class Solution {\n    public int[] max_sum_list(int[][] lists) {\n        return new int[]{};\n    }\n}",
        "reference_solution_java": """class Solution {
    public int[] max_sum_list(int[][] lists) {
        int[] best = lists[0];
        long bestSum = sum(best);
        for (int i = 1; i < lists.length; i++) {
            long curSum = sum(lists[i]);
            if (curSum > bestSum) {
                bestSum = curSum;
                best = lists[i];
            }
        }
        return best;
    }
    private long sum(int[] arr) {
        long s = 0;
        for (int x : arr) s += x;
        return s;
    }
}""",
        "starter_code_cpp": "#include <vector>\n#include <numeric>\nclass Solution {\npublic:\n    std::vector<int> max_sum_list(std::vector<std::vector<int>> lists);\n};",
        "reference_solution_cpp": """#include <vector>
#include <numeric>
class Solution {
public:
    std::vector<int> max_sum_list(std::vector<std::vector<int>> lists) {
        auto best = lists[0];
        long long bestSum = std::accumulate(best.begin(), best.end(), 0LL);
        for (size_t i = 1; i < lists.size(); i++) {
            long long curSum = std::accumulate(lists[i].begin(), lists[i].end(), 0LL);
            if (curSum > bestSum) {
                bestSum = curSum;
                best = lists[i];
            }
        }
        return best;
    }
};"""
    },

    743: {
        "starter_code_javascript": "function max_run_uppercase(test_str) {\n    return 0;\n}",
        "reference_solution_javascript": """function max_run_uppercase(test_str) {
    let cnt = 0, res = 0;
    for (let i = 0; i < test_str.length; i++) {
        if (test_str[i] >= 'A' && test_str[i] <= 'Z') cnt++;
        else { res = cnt; cnt = 0; }
    }
    if (test_str[test_str.length - 1] >= 'A' && test_str[test_str.length - 1] <= 'Z') res = cnt;
    return res;
}""",
        "starter_code_java": "class Solution {\n    public int max_run_uppercase(String test_str) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int max_run_uppercase(String test_str) {
        int cnt = 0, res = 0;
        int n = test_str.length();
        for (int i = 0; i < n; i++) {
            if (Character.isUpperCase(test_str.charAt(i))) cnt++;
            else { res = cnt; cnt = 0; }
        }
        if (Character.isUpperCase(test_str.charAt(n - 1))) res = cnt;
        return res;
    }
}""",
        "starter_code_cpp": "#include <string>\nclass Solution {\npublic:\n    int max_run_uppercase(std::string test_str);\n};",
        "reference_solution_cpp": """#include <string>
#include <cctype>
class Solution {
public:
    int max_run_uppercase(std::string test_str) {
        int cnt = 0, res = 0;
        int n = test_str.length();
        for (int i = 0; i < n; i++) {
            if (isupper((unsigned char)test_str[i])) cnt++;
            else { res = cnt; cnt = 0; }
        }
        if (isupper((unsigned char)test_str[n - 1])) res = cnt;
        return res;
    }
};"""
    },

    744: {
        "starter_code_javascript": "function first_odd(nums) {\n    return 0;\n}",
        "reference_solution_javascript": """function first_odd(nums) {
    for (let x of nums) {
        if (x % 2 !== 0) return x;
    }
    return -1;
}""",
        "starter_code_java": "class Solution {\n    public int first_odd(int[] nums) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int first_odd(int[] nums) {
        for (int x : nums) {
            if (x % 2 != 0) return x;
        }
        return -1;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    int first_odd(std::vector<int> nums);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    int first_odd(std::vector<int> nums) {
        for (int x : nums) {
            if (x % 2 != 0) return x;
        }
        return -1;
    }
};"""
    },

    745: {
        "starter_code_javascript": "function check_K(test_tup, K) {\n    return false;\n}",
        "reference_solution_javascript": """function check_K(test_tup, K) {
    for (let el of test_tup) {
        if (el === K) return true;
    }
    return false;
}""",
        "starter_code_java": "class Solution {\n    public boolean check_K(int[] test_tup, int K) {\n        return false;\n    }\n}",
        "reference_solution_java": """class Solution {
    public boolean check_K(int[] test_tup, int K) {
        for (int el : test_tup) {
            if (el == K) return true;
        }
        return false;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    bool check_K(std::vector<int> test_tup, int K);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    bool check_K(std::vector<int> test_tup, int K) {
        for (int el : test_tup) {
            if (el == K) return true;
        }
        return false;
    }
};"""
    },

    746: {
        "starter_code_javascript": "function check_smaller(test_tup1, test_tup2) {\n    return false;\n}",
        "reference_solution_javascript": """function check_smaller(test_tup1, test_tup2) {
    const len = Math.min(test_tup1.length, test_tup2.length);
    for (let i = 0; i < len; i++) {
        if (test_tup1[i] <= test_tup2[i]) return false;
    }
    return true;
}""",
        "starter_code_java": "class Solution {\n    public boolean check_smaller(int[] test_tup1, int[] test_tup2) {\n        return false;\n    }\n}",
        "reference_solution_java": """class Solution {
    public boolean check_smaller(int[] test_tup1, int[] test_tup2) {
        int len = Math.min(test_tup1.length, test_tup2.length);
        for (int i = 0; i < len; i++) {
            if (test_tup1[i] <= test_tup2[i]) return false;
        }
        return true;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    bool check_smaller(std::vector<int> test_tup1, std::vector<int> test_tup2);\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
class Solution {
public:
    bool check_smaller(std::vector<int> test_tup1, std::vector<int> test_tup2) {
        size_t len = std::min(test_tup1.size(), test_tup2.size());
        for (size_t i = 0; i < len; i++) {
            if (test_tup1[i] <= test_tup2[i]) return false;
        }
        return true;
    }
};"""
    },

    747: {
        "starter_code_javascript": "function count_variable(a, b, c, d) {\n    return [];\n}",
        "reference_solution_javascript": """function count_variable(a, b, c, d) {
    let res = [];
    for (let i = 0; i < a; i++) res.push('p');
    for (let i = 0; i < b; i++) res.push('q');
    for (let i = 0; i < c; i++) res.push('r');
    for (let i = 0; i < d; i++) res.push('s');
    return res;
}""",
        "starter_code_java": "import java.util.*;\nclass Solution {\n    public String[] count_variable(int a, int b, int c, int d) {\n        return new String[]{};\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public String[] count_variable(int a, int b, int c, int d) {
        List<String> list = new ArrayList<>();
        for (int i = 0; i < a; i++) list.add("p");
        for (int i = 0; i < b; i++) list.add("q");
        for (int i = 0; i < c; i++) list.add("r");
        for (int i = 0; i < d; i++) list.add("s");
        return list.toArray(new String[0]);
    }
}""",
        "starter_code_cpp": "#include <vector>\n#include <string>\nclass Solution {\npublic:\n    std::vector<std::string> count_variable(int a, int b, int c, int d);\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
class Solution {
public:
    std::vector<std::string> count_variable(int a, int b, int c, int d) {
        std::vector<std::string> res;
        for (int i = 0; i < a; i++) res.push_back("p");
        for (int i = 0; i < b; i++) res.push_back("q");
        for (int i = 0; i < c; i++) res.push_back("r");
        for (int i = 0; i < d; i++) res.push_back("s");
        return res;
    }
};"""
    },

    748: {
        "starter_code_javascript": "function check_identical(test_list1, test_list2) {\n    return false;\n}",
        "reference_solution_javascript": """function check_identical(test_list1, test_list2) {
    if (test_list1.length !== test_list2.length) return false;
    for (let i = 0; i < test_list1.length; i++) {
        if (test_list1[i].length !== test_list2[i].length) return false;
        for (let j = 0; j < test_list1[i].length; j++) {
            if (test_list1[i][j] !== test_list2[i][j]) return false;
        }
    }
    return true;
}""",
        "starter_code_java": "import java.util.Arrays;\nclass Solution {\n    public boolean check_identical(int[][] test_list1, int[][] test_list2) {\n        return false;\n    }\n}",
        "reference_solution_java": """import java.util.Arrays;
class Solution {
    public boolean check_identical(int[][] test_list1, int[][] test_list2) {
        return Arrays.deepEquals(test_list1, test_list2);
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    bool check_identical(std::vector<std::vector<int>> test_list1, std::vector<std::vector<int>> test_list2);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    bool check_identical(std::vector<std::vector<int>> test_list1, std::vector<std::vector<int>> test_list2) {
        return test_list1 == test_list2;
    }
};"""
    },

    749: {
        "starter_code_javascript": "function road_rd(street) {\n    return '';\n}",
        "reference_solution_javascript": """function road_rd(street) {
    return street.replace(/Road$/, 'Rd.');
}""",
        "starter_code_java": "class Solution {\n    public String road_rd(String street) {\n        return "";\n    }\n}",
        "reference_solution_java": """class Solution {
    public String road_rd(String street) {
        return street.replaceAll("Road$", "Rd.");
    }
}""",
        "starter_code_cpp": "#include <string>\n#include <regex>\nclass Solution {\npublic:\n    std::string road_rd(std::string street);\n};",
        "reference_solution_cpp": """#include <string>
#include <regex>
class Solution {
public:
    std::string road_rd(std::string street) {
        return std::regex_replace(street, std::regex("Road$"), "Rd.");
    }
};"""
    },

    750: {
        "starter_code_javascript": "function string_length(str1) {\n    return 0;\n}",
        "reference_solution_javascript": """function string_length(str1) {
    return str1.length;
}""",
        "starter_code_java": "class Solution {\n    public int string_length(String str1) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int string_length(String str1) {
        return str1.length();
    }
}""",
        "starter_code_cpp": "#include <string>\nclass Solution {\npublic:\n    int string_length(std::string str1);\n};",
        "reference_solution_cpp": """#include <string>
class Solution {
public:
    int string_length(std::string str1) {
        return str1.length();
    }
};"""
    },

    751: {
        "starter_code_javascript": "function rombus_area(p, q) {\n    return 0;\n}",
        "reference_solution_javascript": """function rombus_area(p, q) {
    return Math.floor((p * q) / 2);
}""",
        "starter_code_java": "class Solution {\n    public int rombus_area(int p, int q) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int rombus_area(int p, int q) {
        return (p * q) / 2;
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    int rombus_area(int p, int q);\n};",
        "reference_solution_cpp": """class Solution {
public:
    int rombus_area(int p, int q) {
        return (p * q) / 2;
    }
};"""
    },

    752: {
        "starter_code_javascript": "function sort_by_dnf(arr, n) {\n    return [];\n}",
        "reference_solution_javascript": """function sort_by_dnf(arr, n) {
    let low = 0, mid = 0, high = n - 1;
    while (mid <= high) {
        if (arr[mid] === 0) {
            [arr[low], arr[mid]] = [arr[mid], arr[low]];
            low++; mid++;
        } else if (arr[mid] === 1) {
            mid++;
        } else {
            [arr[mid], arr[high]] = [arr[high], arr[mid]];
            high--;
        }
    }
    return arr;
}""",
        "starter_code_java": "class Solution {\n    public int[] sort_by_dnf(int[] arr, int n) {\n        return new int[]{};\n    }\n}",
        "reference_solution_java": """class Solution {
    public int[] sort_by_dnf(int[] arr, int n) {
        int low = 0, mid = 0, high = n - 1;
        while (mid <= high) {
            if (arr[mid] == 0) {
                int tmp = arr[low]; arr[low] = arr[mid]; arr[mid] = tmp;
                low++; mid++;
            } else if (arr[mid] == 1) {
                mid++;
            } else {
                int tmp = arr[mid]; arr[mid] = arr[high]; arr[high] = tmp;
                high--;
            }
        }
        return arr;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    std::vector<int> sort_by_dnf(std::vector<int> arr, int n);\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
class Solution {
public:
    std::vector<int> sort_by_dnf(std::vector<int> arr, int n) {
        int low = 0, mid = 0, high = n - 1;
        while (mid <= high) {
            if (arr[mid] == 0) {
                std::swap(arr[low], arr[mid]);
                low++; mid++;
            } else if (arr[mid] == 1) {
                mid++;
            } else {
                std::swap(arr[mid], arr[high]);
                high--;
            }
        }
        return arr;
    }
};"""
    },

    753: {
        "starter_code_javascript": "function div_of_nums(nums, m, n) {\n    return [];\n}",
        "reference_solution_javascript": """function div_of_nums(nums, m, n) {
    return nums.filter(x => x % m === 0 || x % n === 0);
}""",
        "starter_code_java": "import java.util.*;\nclass Solution {\n    public int[] div_of_nums(int[] nums, int m, int n) {\n        return new int[]{};\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[] div_of_nums(int[] nums, int m, int n) {
        List<Integer> list = new ArrayList<>();
        for (int x : nums) {
            if (x % m == 0 || x % n == 0) list.add(x);
        }
        int[] res = new int[list.size()];
        for (int i = 0; i < list.size(); i++) res[i] = list.get(i);
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    std::vector<int> div_of_nums(std::vector<int> nums, int m, int n);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    std::vector<int> div_of_nums(std::vector<int> nums, int m, int n) {
        std::vector<int> res;
        for (int x : nums) {
            if (x % m == 0 || x % n == 0) res.push_back(x);
        }
        return res;
    }
};"""
    },

    754: {
        "starter_code_javascript": "function lower_ctr(str) {\n    return 0;\n}",
        "reference_solution_javascript": """function lower_ctr(str) {
    let lower_ctr = 0;
    for (let i = 0; i < str.length; i++) {
        if (str[i] >= 'a' && str[i] <= 'z') lower_ctr++;
    }
    return lower_ctr;
}""",
        "starter_code_java": "class Solution {\n    public int lower_ctr(String str) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int lower_ctr(String str) {
        int lower_ctr = 0;
        for (int i = 0; i < str.length(); i++) {
            char c = str.charAt(i);
            if (c >= 'a' && c <= 'z') lower_ctr++;
        }
        return lower_ctr;
    }
}""",
        "starter_code_cpp": "#include <string>\nclass Solution {\npublic:\n    int lower_ctr(std::string str);\n};",
        "reference_solution_cpp": """#include <string>
class Solution {
public:
    int lower_ctr(std::string str) {
        int lower_ctr = 0;
        for (char c : str) {
            if (c >= 'a' && c <= 'z') lower_ctr++;
        }
        return lower_ctr;
    }
};"""
    },

    755: {
        "starter_code_javascript": "function check_monthnum_number(monthnum1) {\n    return false;\n}",
        "reference_solution_javascript": """function check_monthnum_number(monthnum1) {
    return monthnum1 === 2;
}""",
        "starter_code_java": "class Solution {\n    public boolean check_monthnum_number(int monthnum1) {\n        return false;\n    }\n}",
        "reference_solution_java": """class Solution {
    public boolean check_monthnum_number(int monthnum1) {
        return monthnum1 == 2;
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    bool check_monthnum_number(int monthnum1);\n};",
        "reference_solution_cpp": """class Solution {
public:
    bool check_monthnum_number(int monthnum1) {
        return monthnum1 == 2;
    }
};"""
    },

    756: {
        "starter_code_javascript": "function merge_dictionaries(dict1, dict2) {\n    return {};\n}",
        "reference_solution_javascript": """function merge_dictionaries(dict1, dict2) {
    return { ...dict2, ...dict1 };
}""",
        "starter_code_java": "import java.util.*;\nclass Solution {\n    public Map<Object, Object> merge_dictionaries(Map<Object, Object> dict1, Map<Object, Object> dict2) {\n        return new HashMap<>();\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public Map<Object, Object> merge_dictionaries(Map<Object, Object> dict1, Map<Object, Object> dict2) {
        Map<Object, Object> res = new HashMap<>(dict2);
        res.putAll(dict1);
        return res;
    }
}""",
        "starter_code_cpp": "#include <unordered_map>\n#include <string>\nclass Solution {\npublic:\n    std::unordered_map<std::string, std::string> merge_dictionaries(std::unordered_map<std::string, std::string> dict1, std::unordered_map<std::string, std::string> dict2);\n};",
        "reference_solution_cpp": """#include <unordered_map>
#include <string>
class Solution {
public:
    std::unordered_map<std::string, std::string> merge_dictionaries(std::unordered_map<std::string, std::string> dict1, std::unordered_map<std::string, std::string> dict2) {
        auto res = dict2;
        for (const auto& p : dict1) res[p.first] = p.second;
        return res;
    }
};"""
    },

    757: {
        "starter_code_javascript": "function pass_validity(p) {\n    return false;\n}",
        "reference_solution_javascript": """function pass_validity(p) {
    if (p.length < 6 || p.length > 12) return false;
    if (!/[a-z]/.test(p)) return false;
    if (!/[0-9]/.test(p)) return false;
    if (!/[A-Z]/.test(p)) return false;
    if (!/[$#@]/.test(p)) return false;
    if (/\\s/.test(p)) return false;
    return true;
}""",
        "starter_code_java": "import java.util.regex.*;\nclass Solution {\n    public boolean pass_validity(String p) {\n        return false;\n    }\n}",
        "reference_solution_java": """import java.util.regex.*;
class Solution {
    public boolean pass_validity(String p) {
        if (p.length() < 6 || p.length() > 12) return false;
        if (!Pattern.compile("[a-z]").matcher(p).find()) return false;
        if (!Pattern.compile("[0-9]").matcher(p).find()) return false;
        if (!Pattern.compile("[A-Z]").matcher(p).find()) return false;
        if (!Pattern.compile("[$#@]").matcher(p).find()) return false;
        if (Pattern.compile("\\s").matcher(p).find()) return false;
        return true;
    }
}""",
        "starter_code_cpp": "#include <string>\nclass Solution {\npublic:\n    bool pass_validity(std::string p);\n};",
        "reference_solution_cpp": """#include <string>
#include <cctype>
class Solution {
public:
    bool pass_validity(std::string p) {
        if (p.length() < 6 || p.length() > 12) return false;
        bool hasLower = false, hasUpper = false, hasDigit = false, hasSpecial = false;
        for (char c : p) {
            if (isspace((unsigned char)c)) return false;
            if (c >= 'a' && c <= 'z') hasLower = true;
            else if (c >= 'A' && c <= 'Z') hasUpper = true;
            else if (c >= '0' && c <= '9') hasDigit = true;
            else if (c == '$' || c == '#' || c == '@') hasSpecial = true;
        }
        return hasLower && hasUpper && hasDigit && hasSpecial;
    }
};"""
    },

    758: {
        "starter_code_javascript": "function check_substring(string, sample) {\n    return '';\n}",
        "reference_solution_javascript": """function check_substring(string, sample) {
    if (string.includes(sample)) {
        if (string.startsWith(sample)) return "string starts with the given substring";
        else return "string doesnt start with the given substring";
    }
    return "entered string isnt a substring";
}""",
        "starter_code_java": "class Solution {\n    public String check_substring(String string, String sample) {\n        return "";\n    }\n}",
        "reference_solution_java": """class Solution {
    public String check_substring(String string, String sample) {
        if (string.contains(sample)) {
            if (string.startsWith(sample)) return "string starts with the given substring";
            else return "string doesnt start with the given substring";
        }
        return "entered string isnt a substring";
    }
}""",
        "starter_code_cpp": "#include <string>\nclass Solution {\npublic:\n    std::string check_substring(std::string string, std::string sample);\n};",
        "reference_solution_cpp": """#include <string>
class Solution {
public:
    std::string check_substring(std::string string, std::string sample) {
        if (string.find(sample) != std::string::npos) {
            if (string.rfind(sample, 0) == 0) return "string starts with the given substring";
            else return "string doesnt start with the given substring";
        }
        return "entered string isnt a substring";
    }
};"""
    },

    759: {
        "starter_code_javascript": "function remove_even(l) {\n    return [];\n}",
        "reference_solution_javascript": """function remove_even(l) {
    return l.filter(x => x % 2 !== 0);
}""",
        "starter_code_java": "import java.util.*;\nclass Solution {\n    public int[] remove_even(int[] l) {\n        return new int[]{};\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[] remove_even(int[] l) {
        List<Integer> list = new ArrayList<>();
        for (int x : l) {
            if (x % 2 != 0) list.add(x);
        }
        int[] res = new int[list.size()];
        for (int i = 0; i < list.size(); i++) res[i] = list.get(i);
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    std::vector<int> remove_even(std::vector<int> l);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    std::vector<int> remove_even(std::vector<int> l) {
        std::vector<int> res;
        for (int x : l) {
            if (x % 2 != 0) res.push_back(x);
        }
        return res;
    }
};"""
    },

    760: {
        "starter_code_javascript": "function access_elements(nums, list_index) {\n    return [];\n}",
        "reference_solution_javascript": """function access_elements(nums, list_index) {
    return list_index.map(i => nums[i]);
}""",
        "starter_code_java": "class Solution {\n    public int[] access_elements(int[] nums, int[] list_index) {\n        return new int[]{};\n    }\n}",
        "reference_solution_java": """class Solution {
    public int[] access_elements(int[] nums, int[] list_index) {
        int[] res = new int[list_index.length];
        for (int i = 0; i < list_index.length; i++) {
            res[i] = nums[list_index[i]];
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    std::vector<int> access_elements(std::vector<int> nums, std::vector<int> list_index);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    std::vector<int> access_elements(std::vector<int> nums, std::vector<int> list_index) {
        std::vector<int> res;
        for (int idx : list_index) {
            res.push_back(nums[idx]);
        }
        return res;
    }
};"""
    }
}
