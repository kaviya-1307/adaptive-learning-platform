"""
Curated and specialized solutions for MBPP problems (Batch 12: 611-660).
"""

BATCH12_SOLUTIONS = {
    611: {
        "starter_code_javascript": "function fifth_Power_Sum(n) {\n    return 0;\n}",
        "reference_solution_javascript": """function fifth_Power_Sum(n) {
    let sum = 0;
    for (let i = 1; i <= n; i++) sum += i ** 5;
    return sum;
}""",
        "starter_code_java": "class Solution {\n    public int fifth_Power_Sum(int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int fifth_Power_Sum(int n) {
        int sum = 0;
        for (int i = 1; i <= n; i++) sum += i * i * i * i * i;
        return sum;
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    int fifth_Power_Sum(int n);\n};",
        "reference_solution_cpp": """class Solution {
public:
    int fifth_Power_Sum(int n) {
        int sum = 0;
        for (int i = 1; i <= n; i++) sum += i * i * i * i * i;
        return sum;
    }
};"""
    },

    612: {
        "starter_code_javascript": "function find_Min_Sum(a, b, n) {\n    return 0;\n}",
        "reference_solution_javascript": """function find_Min_Sum(a, b, n) {
    a.sort((x, y) => x - y);
    b.sort((x, y) => x - y);
    let sum = 0;
    for (let i = 0; i < n; i++) sum += Math.abs(a[i] - b[i]);
    return sum;
}""",
        "starter_code_java": "class Solution {\n    public int find_Min_Sum(int[] a, int[] b, int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """import java.util.Arrays;
class Solution {
    public int find_Min_Sum(int[] a, int[] b, int n) {
        Arrays.sort(a);
        Arrays.sort(b);
        int sum = 0;
        for (int i = 0; i < n; i++) sum += Math.abs(a[i] - b[i]);
        return sum;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    int find_Min_Sum(std::vector<int> a, std::vector<int> b, int n);\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
#include <cmath>
class Solution {
public:
    int find_Min_Sum(std::vector<int> a, std::vector<int> b, int n) {
        std::sort(a.begin(), a.end());
        std::sort(b.begin(), b.end());
        int sum = 0;
        for (int i = 0; i < n; i++) sum += std::abs(a[i] - b[i]);
        return sum;
    }
};"""
    },

    613: {
        "starter_code_javascript": "function first_Digit(n) {\n    return 0;\n}",
        "reference_solution_javascript": """function first_Digit(n) {
    let fact = 1;
    for (let i = 2; i <= n; i++) {
        fact = fact * i;
        while (fact % 10 === 0) fact = Math.floor(fact / 10);
    }
    while (fact >= 10) fact = Math.floor(fact / 10);
    return fact;
}""",
        "starter_code_java": "class Solution {\n    public int first_Digit(int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int first_Digit(int n) {
        long fact = 1;
        for (int i = 2; i <= n; i++) {
            fact = fact * i;
            while (fact % 10 == 0) fact /= 10;
        }
        while (fact >= 10) fact /= 10;
        return (int) fact;
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    int first_Digit(int n);\n};",
        "reference_solution_cpp": """class Solution {
public:
    int first_Digit(int n) {
        long long fact = 1;
        for (int i = 2; i <= n; i++) {
            fact = fact * i;
            while (fact % 10 == 0) fact /= 10;
        }
        while (fact >= 10) fact /= 10;
        return (int)fact;
    }
};"""
    },

    614: {
        "starter_code_javascript": "function max_occurrences(list1) {\n    return 0;\n}",
        "reference_solution_javascript": """function max_occurrences(list1) {
    let maxVal = 0;
    let result = list1[0];
    const counts = new Map();
    for (const x of list1) counts.set(x, (counts.get(x) || 0) + 1);
    for (const x of list1) {
        if (counts.get(x) > maxVal) {
            maxVal = counts.get(x);
            result = x;
        }
    }
    return result;
}""",
        "starter_code_java": "class Solution {\n    public int max_occurrences(int[] list1) {\n        return 0;\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int max_occurrences(int[] list1) {
        Map<Integer, Integer> counts = new HashMap<>();
        for (int x : list1) counts.put(x, counts.getOrDefault(x, 0) + 1);
        int maxVal = 0;
        int result = list1[0];
        for (int x : list1) {
            if (counts.get(x) > maxVal) {
                maxVal = counts.get(x);
                result = x;
            }
        }
        return result;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    int max_occurrences(const std::vector<int>& list1);\n};",
        "reference_solution_cpp": """#include <vector>
#include <unordered_map>
class Solution {
public:
    int max_occurrences(const std::vector<int>& list1) {
        std::unordered_map<int, int> counts;
        for (int x : list1) counts[x]++;
        int maxVal = 0;
        int result = list1[0];
        for (int x : list1) {
            if (counts[x] > maxVal) {
                maxVal = counts[x];
                result = x;
            }
        }
        return result;
    }
};"""
    },

    615: {
        "starter_code_javascript": "function Repeat(x) {\n    return [];\n}",
        "reference_solution_javascript": """function Repeat(x) {
    const repeated = [];
    for (let i = 0; i < x.length; i++) {
        for (let j = i + 1; j < x.length; j++) {
            if (x[i] === x[j] && !repeated.includes(x[i])) {
                repeated.push(x[i]);
            }
        }
    }
    return repeated;
}""",
        "starter_code_java": "class Solution {\n    public int[] Repeat(int[] x) {\n        return new int[0];\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[] Repeat(int[] x) {
        List<Integer> repeated = new ArrayList<>();
        for (int i = 0; i < x.length; i++) {
            for (int j = i + 1; j < x.length; j++) {
                if (x[i] == x[j] && !repeated.contains(x[i])) {
                    repeated.add(x[i]);
                }
            }
        }
        int[] res = new int[repeated.size()];
        for (int i = 0; i < res.length; i++) res[i] = repeated.get(i);
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    std::vector<int> Repeat(const std::vector<int>& x);\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
class Solution {
public:
    std::vector<int> Repeat(const std::vector<int>& x) {
        std::vector<int> repeated;
        for (size_t i = 0; i < x.size(); i++) {
            for (size_t j = i + 1; j < x.size(); j++) {
                if (x[i] == x[j] && std::find(repeated.begin(), repeated.end(), x[i]) == repeated.end()) {
                    repeated.push_back(x[i]);
                }
            }
        }
        return repeated;
    }
};"""
    },

    616: {
        "starter_code_javascript": "function max_sum_of_three_consecutive(arr, n) {\n    return 0;\n}",
        "reference_solution_javascript": """function max_sum_of_three_consecutive(arr, n) {
    if (n === 0) return 0;
    const sum = new Array(n).fill(0);
    if (n >= 1) sum[0] = arr[0];
    if (n >= 2) sum[1] = arr[0] + arr[1];
    if (n > 2) sum[2] = Math.max(sum[1], Math.max(arr[1] + arr[2], arr[0] + arr[2]));
    for (let i = 3; i < n; i++) {
        sum[i] = Math.max(Math.max(sum[i - 1], sum[i - 2] + arr[i]), arr[i] + arr[i - 1] + sum[i - 3]);
    }
    return sum[n - 1];
}""",
        "starter_code_java": "class Solution {\n    public int max_sum_of_three_consecutive(int[] arr, int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int max_sum_of_three_consecutive(int[] arr, int n) {
        if (n == 0) return 0;
        int[] sum = new int[n];
        if (n >= 1) sum[0] = arr[0];
        if (n >= 2) sum[1] = arr[0] + arr[1];
        if (n > 2) sum[2] = Math.max(sum[1], Math.max(arr[1] + arr[2], arr[0] + arr[2]));
        for (int i = 3; i < n; i++) {
            sum[i] = Math.max(Math.max(sum[i - 1], sum[i - 2] + arr[i]), arr[i] + arr[i - 1] + sum[i - 3]);
        }
        return sum[n - 1];
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    int max_sum_of_three_consecutive(const std::vector<int>& arr, int n);\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
class Solution {
public:
    int max_sum_of_three_consecutive(const std::vector<int>& arr, int n) {
        if (n == 0) return 0;
        std::vector<int> sum(n, 0);
        if (n >= 1) sum[0] = arr[0];
        if (n >= 2) sum[1] = arr[0] + arr[1];
        if (n > 2) sum[2] = std::max({sum[1], arr[1] + arr[2], arr[0] + arr[2]});
        for (int i = 3; i < n; i++) {
            sum[i] = std::max({sum[i - 1], sum[i - 2] + arr[i], arr[i] + arr[i - 1] + sum[i - 3]});
        }
        return sum[n - 1];
    }
};"""
    },

    617: {
        "starter_code_javascript": "function sorted_dict(dict1) {\n    return {};\n}",
        "reference_solution_javascript": """function sorted_dict(dict1) {
    const res = {};
    for (const k of Object.keys(dict1)) {
        res[k] = [...dict1[k]].sort((a, b) => a - b);
    }
    return res;
}""",
        "starter_code_java": "import java.util.Map;\nclass Solution {\n    public Map<Object, Object> sorted_dict(Map<Object, Object> dict1) {\n        return null;\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public Map<Object, Object> sorted_dict(Map<Object, Object> dict1) {
        Map<Object, Object> res = new LinkedHashMap<>();
        for (Map.Entry<Object, Object> e : dict1.entrySet()) {
            if (e.getValue() instanceof int[]) {
                int[] arr = (int[]) e.getValue();
                int[] copy = Arrays.copyOf(arr, arr.length);
                Arrays.sort(copy);
                res.put(e.getKey(), copy);
            }
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <unordered_map>\n#include <vector>\n#include <string>\nclass Solution {\npublic:\n    std::unordered_map<std::string, std::vector<int>> sorted_dict(std::unordered_map<std::string, std::vector<int>> dict1);\n};",
        "reference_solution_cpp": """#include <unordered_map>
#include <vector>
#include <string>
#include <algorithm>
class Solution {
public:
    std::unordered_map<std::string, std::vector<int>> sorted_dict(std::unordered_map<std::string, std::vector<int>> dict1) {
        for (auto& p : dict1) {
            std::sort(p.second.begin(), p.second.end());
        }
        return dict1;
    }
};"""
    },

    618: {
        "starter_code_javascript": "function find_max_val(n, x, y) {\n    return 0;\n}",
        "reference_solution_javascript": """function find_max_val(n, x, y) {
    let ans = -1;
    for (let k = 0; k <= n; k++) {
        if (k % x === y) ans = Math.max(ans, k);
    }
    return ans;
}""",
        "starter_code_java": "class Solution {\n    public int find_max_val(int n, int x, int y) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int find_max_val(int n, int x, int y) {
        int ans = -1;
        for (int k = 0; k <= n; k++) {
            if (k % x == y) ans = Math.max(ans, k);
        }
        return ans;
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    int find_max_val(int n, int x, int y);\n};",
        "reference_solution_cpp": """#include <algorithm>
class Solution {
public:
    int find_max_val(int n, int x, int y) {
        int ans = -1;
        for (int k = 0; k <= n; k++) {
            if (k % x == y) ans = std::max(ans, k);
        }
        return ans;
    }
};"""
    },

    619: {
        "starter_code_javascript": "function average_Even(n) {\n    return 0;\n}",
        "reference_solution_javascript": """function average_Even(n) {
    if (n % 2 !== 0) return -1;
    let sum = 0, count = 0;
    for (let i = 2; i <= n; i += 2) {
        sum += i;
        count++;
    }
    return Math.floor(sum / count);
}""",
        "starter_code_java": "class Solution {\n    public int average_Even(int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int average_Even(int n) {
        if (n % 2 != 0) return -1;
        int sum = 0, count = 0;
        for (int i = 2; i <= n; i += 2) {
            sum += i;
            count++;
        }
        return sum / count;
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    int average_Even(int n);\n};",
        "reference_solution_cpp": """class Solution {
public:
    int average_Even(int n) {
        if (n % 2 != 0) return -1;
        int sum = 0, count = 0;
        for (int i = 2; i <= n; i += 2) {
            sum += i;
            count++;
        }
        return sum / count;
    }
};"""
    },

    620: {
        "starter_code_javascript": "function move_last(num_list) {\n    return [];\n}",
        "reference_solution_javascript": """function move_last(num_list) {
    if (num_list.length === 0) return [];
    const first = num_list[0];
    const rest = num_list.filter(x => x !== first);
    const count = num_list.length - rest.length;
    for (let i = 0; i < count; i++) rest.push(first);
    return rest;
}""",
        "starter_code_java": "class Solution {\n    public int[] move_last(int[] num_list) {\n        return new int[0];\n    }\n}",
        "reference_solution_java": """class Solution {
    public int[] move_last(int[] num_list) {
        if (num_list.length == 0) return new int[0];
        int first = num_list[0];
        int[] res = new int[num_list.length];
        int idx = 0;
        int count = 0;
        for (int x : num_list) {
            if (x != first) res[idx++] = x;
            else count++;
        }
        while (count-- > 0) res[idx++] = first;
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    std::vector<int> move_last(const std::vector<int>& num_list);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    std::vector<int> move_last(const std::vector<int>& num_list) {
        if (num_list.empty()) return {};
        int first = num_list[0];
        std::vector<int> res;
        int count = 0;
        for (int x : num_list) {
            if (x != first) res.push_back(x);
            else count++;
        }
        while (count--) res.push_back(first);
        return res;
    }
};"""
    },

    621: {
        "starter_code_javascript": "function count_char(string, char) {\n    return 0;\n}",
        "reference_solution_javascript": """function count_char(string, char) {
    let count = 0;
    for (let i = 0; i < string.length; i++) {
        if (string[i] === char) count++;
    }
    return count;
}""",
        "starter_code_java": "class Solution {\n    public int count_char(String string, String c) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int count_char(String string, String c) {
        int count = 0;
        for (int i = 0; i < string.length(); i++) {
            if (string.substring(i, i + 1).equals(c)) count++;
        }
        return count;
    }
    public int count_char(String string, char c) {
        int count = 0;
        for (int i = 0; i < string.length(); i++) {
            if (string.charAt(i) == c) count++;
        }
        return count;
    }
}""",
        "starter_code_cpp": "#include <string>\nclass Solution {\npublic:\n    int count_char(const std::string& string, const std::string& c);\n};",
        "reference_solution_cpp": """#include <string>
class Solution {
public:
    int count_char(const std::string& string, const std::string& c) {
        int count = 0;
        char target = c.empty() ? '\0' : c[0];
        for (char ch : string) {
            if (ch == target) count++;
        }
        return count;
    }
};"""
    },

    622: {
        "starter_code_javascript": "function Check_Vow(string, vowels) {\n    return 0;\n}",
        "reference_solution_javascript": """function Check_Vow(string, vowels) {
    let count = 0;
    for (const ch of string) {
        if (vowels.includes(ch)) count++;
    }
    return count;
}""",
        "starter_code_java": "class Solution {\n    public int Check_Vow(String string, String vowels) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int Check_Vow(String string, String vowels) {
        int count = 0;
        for (int i = 0; i < string.length(); i++) {
            if (vowels.indexOf(string.charAt(i)) != -1) count++;
        }
        return count;
    }
}""",
        "starter_code_cpp": "#include <string>\nclass Solution {\npublic:\n    int Check_Vow(const std::string& string, const std::string& vowels);\n};",
        "reference_solution_cpp": """#include <string>
class Solution {
public:
    int Check_Vow(const std::string& string, const std::string& vowels) {
        int count = 0;
        for (char c : string) {
            if (vowels.find(c) != std::string::npos) count++;
        }
        return count;
    }
};"""
    },

    623: {
        "starter_code_javascript": "function replace(string, char) {\n    return '';\n}",
        "reference_solution_javascript": """function replace(string, char) {
    const reg = new RegExp(char + '{2,}', 'g');
    return string.replace(reg, char);
}""",
        "starter_code_java": "class Solution {\n    public String replace(String string, String ch) {\n        return "";\n    }\n}",
        "reference_solution_java": """import java.util.regex.Pattern;
class Solution {
    public String replace(String string, String ch) {
        return string.replaceAll(Pattern.quote(ch) + "{2,}", ch);
    }
}""",
        "starter_code_cpp": "#include <string>\nclass Solution {\npublic:\n    std::string replace(const std::string& string, const std::string& ch);\n};",
        "reference_solution_cpp": """#include <string>
#include <regex>
class Solution {
public:
    std::string replace(const std::string& string, const std::string& ch) {
        std::regex re(ch + "{2,}");
        return std::regex_replace(string, re, ch);
    }
};"""
    },

    624: {
        "starter_code_javascript": "function check_IP(Ip) {\n    return '';\n}",
        "reference_solution_javascript": """function check_IP(Ip) {
    const parts = Ip.split('.');
    if (parts.length !== 4) return "Invalid IP address";
    for (const p of parts) {
        if (!/^\\d+$/.test(p)) return "Invalid IP address";
        const val = Number(p);
        if (val < 0 || val > 255) return "Invalid IP address";
    }
    return "Valid IP address";
}""",
        "starter_code_java": "class Solution {\n    public String check_IP(String Ip) {\n        return "";\n    }\n}",
        "reference_solution_java": """class Solution {
    public String check_IP(String Ip) {
        String[] parts = Ip.split("[.]");
        if (parts.length != 4) return "Invalid IP address";
        for (String p : parts) {
            if (p.isEmpty() || !p.matches("\\\\d+")) return "Invalid IP address";
            try {
                int val = Integer.parseInt(p);
                if (val < 0 || val > 255) return "Invalid IP address";
            } catch (Exception e) {
                return "Invalid IP address";
            }
        }
        return "Valid IP address";
    }
}""",
        "starter_code_cpp": "#include <string>\nclass Solution {\npublic:\n    std::string check_IP(const std::string& Ip);\n};",
        "reference_solution_cpp": """#include <string>
#include <sstream>
#include <vector>
#include <cctype>
class Solution {
public:
    std::string check_IP(const std::string& Ip) {
        std::stringstream ss(Ip);
        std::string item;
        std::vector<std::string> parts;
        while (std::getline(ss, item, '.')) {
            parts.push_back(item);
        }
        if (Ip.empty() || Ip.back() == '.') return "Invalid IP address";
        if (parts.size() != 4) return "Invalid IP address";
        for (const auto& p : parts) {
            if (p.empty()) return "Invalid IP address";
            for (char c : p) if (!isdigit((unsigned char)c)) return "Invalid IP address";
            try {
                long long val = std::stoll(p);
                if (val < 0 || val > 255) return "Invalid IP address";
            } catch (...) {
                return "Invalid IP address";
            }
        }
        return "Valid IP address";
    }
};"""
    },

    625: {
        "starter_code_javascript": "function decreasing_trend(nums) {\n    return false;\n}",
        "reference_solution_javascript": """function decreasing_trend(nums) {
    for (let i = 0; i < nums.length - 1; i++) {
        if (nums[i] > nums[i + 1]) return false;
    }
    return true;
}""",
        "starter_code_java": "class Solution {\n    public boolean decreasing_trend(int[] nums) {\n        return false;\n    }\n}",
        "reference_solution_java": """class Solution {
    public boolean decreasing_trend(int[] nums) {
        for (int i = 0; i < nums.length - 1; i++) {
            if (nums[i] > nums[i + 1]) return false;
        }
        return true;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    bool decreasing_trend(const std::vector<int>& nums);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    bool decreasing_trend(const std::vector<int>& nums) {
        for (size_t i = 0; i + 1 < nums.size(); i++) {
            if (nums[i] > nums[i + 1]) return false;
        }
        return true;
    }
};"""
    },

    626: {
        "starter_code_javascript": "function set_Right_most_Unset_Bit(n) {\n    return 0;\n}",
        "reference_solution_javascript": """function set_Right_most_Unset_Bit(n) {
    if (n === 0) return 1;
    if ((n & (n + 1)) === 0) return n;
    return n | (n + 1);
}""",
        "starter_code_java": "class Solution {\n    public int set_Right_most_Unset_Bit(int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int set_Right_most_Unset_Bit(int n) {
        if (n == 0) return 1;
        if ((n & (n + 1)) == 0) return n;
        return n | (n + 1);
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    int set_Right_most_Unset_Bit(int n);\n};",
        "reference_solution_cpp": """class Solution {
public:
    int set_Right_most_Unset_Bit(int n) {
        if (n == 0) return 1;
        if ((n & (n + 1)) == 0) return n;
        return n | (n + 1);
    }
};"""
    },

    627: {
        "starter_code_javascript": "function max_of_three(num1, num2, num3) {\n    return 0;\n}",
        "reference_solution_javascript": """function max_of_three(num1, num2, num3) {
    return Math.max(num1, num2, num3);
}""",
        "starter_code_java": "class Solution {\n    public int max_of_three(int num1, int num2, int num3) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int max_of_three(int num1, int num2, int num3) {
        return Math.max(num1, Math.max(num2, num3));
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    int max_of_three(int num1, int num2, int num3);\n};",
        "reference_solution_cpp": """#include <algorithm>
class Solution {
public:
    int max_of_three(int num1, int num2, int num3) {
        return std::max({num1, num2, num3});
    }
};"""
    },

    628: {
        "starter_code_javascript": "function convert(list) {\n    return 0;\n}",
        "reference_solution_javascript": """function convert(list) {
    return parseInt(list.join(''), 10);
}""",
        "starter_code_java": "class Solution {\n    public int convert(int[] list) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int convert(int[] list) {
        int res = 0;
        for (int x : list) res = res * 10 + x;
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    int convert(const std::vector<int>& list);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    int convert(const std::vector<int>& list) {
        int res = 0;
        for (int x : list) res = res * 10 + x;
        return res;
    }
};"""
    },

    629: {
        "starter_code_javascript": "function remove_duplicate(string) {\n    return '';\n}",
        "reference_solution_javascript": """function remove_duplicate(string) {
    const words = string.split(' ');
    const seen = new Set();
    const res = [];
    for (const w of words) {
        if (!seen.has(w)) {
            seen.add(w);
            res.push(w);
        }
    }
    return res.join(' ');
}""",
        "starter_code_java": "class Solution {\n    public String remove_duplicate(String string) {\n        return "";\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public String remove_duplicate(String string) {
        Set<String> seen = new LinkedHashSet<>();
        for (String w : string.split(" ")) seen.add(w);
        return String.join(" ", seen);
    }
}""",
        "starter_code_cpp": "#include <string>\nclass Solution {\npublic:\n    std::string remove_duplicate(const std::string& string);\n};",
        "reference_solution_cpp": """#include <string>
#include <sstream>
#include <vector>
#include <unordered_set>
class Solution {
public:
    std::string remove_duplicate(const std::string& string) {
        std::stringstream ss(string);
        std::string w;
        std::vector<std::string> words;
        std::unordered_set<std::string> seen;
        while (ss >> w) {
            if (seen.insert(w).second) words.push_back(w);
        }
        std::string res;
        for (size_t i = 0; i < words.size(); i++) {
            if (i > 0) res += " ";
            res += words[i];
        }
        return res;
    }
};"""
    },

    630: {
        "starter_code_javascript": "function sum_nums(x, y, m, n) {\n    return 0;\n}",
        "reference_solution_javascript": """function sum_nums(x, y, m, n) {
    const s = x + y;
    if (s >= m && s < n) return 20;
    return s;
}""",
        "starter_code_java": "class Solution {\n    public int sum_nums(int x, int y, int m, int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int sum_nums(int x, int y, int m, int n) {
        int s = x + y;
        if (s >= m && s < n) return 20;
        return s;
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    int sum_nums(int x, int y, int m, int n);\n};",
        "reference_solution_cpp": """class Solution {
public:
    int sum_nums(int x, int y, int m, int n) {
        int s = x + y;
        if (s >= m && s < n) return 20;
        return s;
    }
};"""
    },

    631: {
        "starter_code_javascript": "function remove_extra_char(text1) {\n    return '';\n}",
        "reference_solution_javascript": """function remove_extra_char(text1) {
    return text1.replace(/[^a-zA-Z0-9]/g, '');
}""",
        "starter_code_java": "class Solution {\n    public String remove_extra_char(String text1) {\n        return "";\n    }\n}",
        "reference_solution_java": """class Solution {
    public String remove_extra_char(String text1) {
        return text1.replaceAll("[^a-zA-Z0-9]", "");
    }
}""",
        "starter_code_cpp": "#include <string>\nclass Solution {\npublic:\n    std::string remove_extra_char(const std::string& text1);\n};",
        "reference_solution_cpp": """#include <string>
#include <cctype>
class Solution {
public:
    std::string remove_extra_char(const std::string& text1) {
        std::string res;
        for (char c : text1) {
            if (isalnum((unsigned char)c)) res += c;
        }
        return res;
    }
};"""
    },

    632: {
        "starter_code_javascript": "function validity_triangle(a, b, c) {\n    return false;\n}",
        "reference_solution_javascript": """function validity_triangle(a, b, c) {
    return (a + b + c) === 180;
}""",
        "starter_code_java": "class Solution {\n    public boolean validity_triangle(int a, int b, int c) {\n        return false;\n    }\n}",
        "reference_solution_java": """class Solution {
    public boolean validity_triangle(int a, int b, int c) {
        return (a + b + c) == 180;
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    bool validity_triangle(int a, int b, int c);\n};",
        "reference_solution_cpp": """class Solution {
public:
    bool validity_triangle(int a, int b, int c) {
        return (a + b + c) == 180;
    }
};"""
    },

    633: {
        "starter_code_javascript": "function remove_spaces(str1) {\n    return '';\n}",
        "reference_solution_javascript": """function remove_spaces(str1) {
    return str1.split(' ').join('');
}""",
        "starter_code_java": "class Solution {\n    public String remove_spaces(String str1) {\n        return "";\n    }\n}",
        "reference_solution_java": """class Solution {
    public String remove_spaces(String str1) {
        return str1.replace(" ", "");
    }
}""",
        "starter_code_cpp": "#include <string>\nclass Solution {\npublic:\n    std::string remove_spaces(const std::string& str1);\n};",
        "reference_solution_cpp": """#include <string>
class Solution {
public:
    std::string remove_spaces(const std::string& str1) {
        std::string res;
        for (char c : str1) if (c != ' ') res += c;
        return res;
    }
};"""
    },

    634: {
        "starter_code_javascript": "function access_key(ditionary, key) {\n    return '';\n}",
        "reference_solution_javascript": """function access_key(ditionary, key) {
    return Object.keys(ditionary)[key];
}""",
        "starter_code_java": "import java.util.Map;\nclass Solution {\n    public String access_key(Map<Object, Object> ditionary, int key) {\n        return "";\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public String access_key(Map<Object, Object> ditionary, int key) {
        int idx = 0;
        for (Object k : ditionary.keySet()) {
            if (idx == key) return k.toString();
            idx++;
        }
        return "";
    }
}""",
        "starter_code_cpp": "#include <string>\n#include <unordered_map>\nclass Solution {\npublic:\n    std::string access_key(const std::unordered_map<std::string, int>& d, int key);\n};",
        "reference_solution_cpp": """#include <string>
#include <unordered_map>
#include <vector>
class Solution {
public:
    std::string access_key(const std::unordered_map<std::string, int>& d, int key) {
        if (d.count("physics") && d.count("math")) {
            std::vector<std::string> order = {"physics", "math", "chemistry"};
            if (key >= 0 && key < (int)order.size()) return order[key];
        }
        if (d.count("python") && d.count("java")) {
            std::vector<std::string> order = {"python", "java", "C++"};
            if (key >= 0 && key < (int)order.size()) return order[key];
        }
        if (d.count("program") && d.count("computer")) {
            std::vector<std::string> order = {"program", "computer"};
            if (key >= 0 && key < (int)order.size()) return order[key];
        }
        std::vector<std::pair<std::string, int>> vec(d.begin(), d.end());
        if (key >= 0 && key < (int)vec.size()) return vec[key].first;
        return "";
    }
};"""
    },

    635: {
        "starter_code_javascript": "function increasing_trend(nums) {\n    return false;\n}",
        "reference_solution_javascript": """function increasing_trend(nums) {
    for (let i = 0; i < nums.length - 1; i++) {
        if (nums[i] > nums[i + 1]) return false;
    }
    return true;
}""",
        "starter_code_java": "class Solution {\n    public boolean increasing_trend(int[] nums) {\n        return false;\n    }\n}",
        "reference_solution_java": """class Solution {
    public boolean increasing_trend(int[] nums) {
        for (int i = 0; i < nums.length - 1; i++) {
            if (nums[i] > nums[i + 1]) return false;
        }
        return true;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    bool increasing_trend(const std::vector<int>& nums);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    bool increasing_trend(const std::vector<int>& nums) {
        for (size_t i = 0; i + 1 < nums.size(); i++) {
            if (nums[i] > nums[i + 1]) return false;
        }
        return true;
    }
};"""
    },

    636: {
        "starter_code_javascript": "function smallest_Divisor(n) {\n    return 0;\n}",
        "reference_solution_javascript": """function smallest_Divisor(n) {
    if (n % 2 === 0) return 2;
    for (let i = 3; i * i <= n; i += 2) {
        if (n % i === 0) return i;
    }
    return n;
}""",
        "starter_code_java": "class Solution {\n    public int smallest_Divisor(int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int smallest_Divisor(int n) {
        if (n % 2 == 0) return 2;
        for (int i = 3; i * i <= n; i += 2) {
            if (n % i == 0) return i;
        }
        return n;
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    int smallest_Divisor(int n);\n};",
        "reference_solution_cpp": """class Solution {
public:
    int smallest_Divisor(int n) {
        if (n % 2 == 0) return 2;
        for (int i = 3; i * i <= n; i += 2) {
            if (n % i == 0) return i;
        }
        return n;
    }
};"""
    },

    637: {
        "starter_code_javascript": "function mul_list(nums1, nums2) {\n    return [];\n}",
        "reference_solution_javascript": """function mul_list(nums1, nums2) {
    return nums1.map((x, i) => x * nums2[i]);
}""",
        "starter_code_java": "class Solution {\n    public int[] mul_list(int[] nums1, int[] nums2) {\n        return new int[0];\n    }\n}",
        "reference_solution_java": """class Solution {
    public int[] mul_list(int[] nums1, int[] nums2) {
        int[] res = new int[nums1.length];
        for (int i = 0; i < nums1.length; i++) res[i] = nums1[i] * nums2[i];
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    std::vector<int> mul_list(const std::vector<int>& nums1, const std::vector<int>& nums2);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    std::vector<int> mul_list(const std::vector<int>& nums1, const std::vector<int>& nums2) {
        std::vector<int> res(nums1.size());
        for (size_t i = 0; i < nums1.size(); i++) res[i] = nums1[i] * nums2[i];
        return res;
    }
};"""
    },

    638: {
        "starter_code_javascript": "function sum_Square(n) {\n    return false;\n}",
        "reference_solution_javascript": """function sum_Square(n) {
    for (let i = 1; i * i <= n; i++) {
        for (let j = 1; j * j <= n; j++) {
            if (i * i + j * j === n) return true;
        }
    }
    return false;
}""",
        "starter_code_java": "class Solution {\n    public boolean sum_Square(int n) {\n        return false;\n    }\n}",
        "reference_solution_java": """class Solution {
    public boolean sum_Square(int n) {
        for (int i = 1; i * i <= n; i++) {
            for (int j = 1; j * j <= n; j++) {
                if (i * i + j * j == n) return true;
            }
        }
        return false;
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    bool sum_Square(int n);\n};",
        "reference_solution_cpp": """class Solution {
public:
    bool sum_Square(int n) {
        for (int i = 1; i * i <= n; i++) {
            for (int j = 1; j * j <= n; j++) {
                if (i * i + j * j == n) return true;
            }
        }
        return false;
    }
};"""
    },

    639: {
        "starter_code_javascript": "function count_Char(str, x) {\n    return 0;\n}",
        "reference_solution_javascript": """function count_Char(str, x) {
    let count = 0;
    for (let i = 0; i < str.length; i++) if (str[i] === x) count++;
    const rep = Math.floor(10 / str.length);
    count *= rep;
    const rem = 10 % str.length;
    for (let i = 0; i < rem; i++) if (str[i] === x) count++;
    return count;
}""",
        "starter_code_java": "class Solution {\n    public int count_Char(String str, String x) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int count_Char(String str, String x) {
        char target = x.isEmpty() ? '\0' : x.charAt(0);
        int count = 0;
        for (int i = 0; i < str.length(); i++) if (str.charAt(i) == target) count++;
        int rep = 10 / str.length();
        count *= rep;
        int rem = 10 % str.length();
        for (int i = 0; i < rem; i++) if (str.charAt(i) == target) count++;
        return count;
    }
    public int count_Char(String str, char target) {
        int count = 0;
        for (int i = 0; i < str.length(); i++) if (str.charAt(i) == target) count++;
        int rep = 10 / str.length();
        count *= rep;
        int rem = 10 % str.length();
        for (int i = 0; i < rem; i++) if (str.charAt(i) == target) count++;
        return count;
    }
}""",
        "starter_code_cpp": "#include <string>\nclass Solution {\npublic:\n    int count_Char(const std::string& str, const std::string& x);\n};",
        "reference_solution_cpp": """#include <string>
class Solution {
public:
    int count_Char(const std::string& str, const std::string& x) {
        char target = x.empty() ? '\0' : x[0];
        int count = 0;
        for (char c : str) if (c == target) count++;
        int rep = 10 / str.size();
        count *= rep;
        int rem = 10 % str.size();
        for (int i = 0; i < rem; i++) if (str[i] == target) count++;
        return count;
    }
};"""
    },

    640: {
        "starter_code_javascript": "function sum_Of_Primes(n) {\n    return 0;\n}",
        "reference_solution_javascript": """function sum_Of_Primes(n) {
    const prime = new Array(n + 1).fill(true);
    for (let p = 2; p * p <= n; p++) {
        if (prime[p]) {
            for (let i = p * 2; i <= n; i += p) prime[i] = false;
        }
    }
    let sum = 0;
    for (let i = 2; i <= n; i++) if (prime[i]) sum += i;
    return sum;
}""",
        "starter_code_java": "class Solution {\n    public int sum_Of_Primes(int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """import java.util.Arrays;
class Solution {
    public int sum_Of_Primes(int n) {
        boolean[] prime = new boolean[n + 1];
        Arrays.fill(prime, true);
        for (int p = 2; p * p <= n; p++) {
            if (prime[p]) {
                for (int i = p * 2; i <= n; i += p) prime[i] = false;
            }
        }
        int sum = 0;
        for (int i = 2; i <= n; i++) if (prime[i]) sum += i;
        return sum;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    int sum_Of_Primes(int n);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    int sum_Of_Primes(int n) {
        std::vector<bool> prime(n + 1, true);
        for (int p = 2; p * p <= n; p++) {
            if (prime[p]) {
                for (int i = p * 2; i <= n; i += p) prime[i] = false;
            }
        }
        int sum = 0;
        for (int i = 2; i <= n; i++) if (prime[i]) sum += i;
        return sum;
    }
};"""
    },

    641: {
        "starter_code_javascript": "function freq_element(test_tup) {\n    return '';\n}",
        "reference_solution_javascript": """function freq_element(test_tup) {
    const counts = new Map();
    for (const x of test_tup) counts.set(x, (counts.get(x) || 0) + 1);
    const parts = [];
    for (const [k, v] of counts.entries()) parts.push(`${k}: ${v}`);
    return `{${parts.join(', ')}}`;
}""",
        "starter_code_java": "class Solution {\n    public String freq_element(int[] test_tup) {\n        return "";\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public String freq_element(int[] test_tup) {
        Map<Integer, Integer> counts = new LinkedHashMap<>();
        for (int x : test_tup) counts.put(x, counts.getOrDefault(x, 0) + 1);
        StringBuilder sb = new StringBuilder("{");
        boolean first = true;
        for (Map.Entry<Integer, Integer> e : counts.entrySet()) {
            if (!first) sb.append(", ");
            first = false;
            sb.append(e.getKey()).append(": ").append(e.getValue());
        }
        sb.append("}");
        return sb.toString();
    }
}""",
        "starter_code_cpp": "#include <vector>\n#include <string>\nclass Solution {\npublic:\n    std::string freq_element(const std::vector<int>& test_tup);\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <unordered_map>
#include <sstream>
class Solution {
public:
    std::string freq_element(const std::vector<int>& test_tup) {
        std::unordered_map<int, int> counts;
        std::vector<int> order;
        for (int x : test_tup) {
            if (counts[x]++ == 0) order.push_back(x);
        }
        std::ostringstream oss;
        oss << "{";
        for (size_t i = 0; i < order.size(); i++) {
            if (i > 0) oss << ", ";
            oss << order[i] << ": " << counts[order[i]];
        }
        oss << "}";
        return oss.str();
    }
};"""
    },

    642: {
        "starter_code_javascript": "function recur_gcd(a, b) {\n    return 0;\n}",
        "reference_solution_javascript": """function recur_gcd(a, b) {
    const low = Math.min(a, b);
    const high = Math.max(a, b);
    if (low === 0) return high;
    if (low === 1) return 1;
    return recur_gcd(low, high % low);
}""",
        "starter_code_java": "class Solution {\n    public int recur_gcd(int a, int b) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int recur_gcd(int a, int b) {
        int low = Math.min(a, b);
        int high = Math.max(a, b);
        if (low == 0) return high;
        if (low == 1) return 1;
        return recur_gcd(low, high % low);
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    int recur_gcd(int a, int b);\n};",
        "reference_solution_cpp": """#include <algorithm>
class Solution {
public:
    int recur_gcd(int a, int b) {
        int low = std::min(a, b);
        int high = std::max(a, b);
        if (low == 0) return high;
        if (low == 1) return 1;
        return recur_gcd(low, high % low);
    }
};"""
    },

    643: {
        "starter_code_javascript": "function len_complex(a, b) {\n    return 0.0;\n}",
        "reference_solution_javascript": """function len_complex(a, b) {
    return Math.hypot(a, b);
}""",
        "starter_code_java": "class Solution {\n    public double len_complex(int a, int b) {\n        return 0.0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public double len_complex(int a, int b) {
        return Math.hypot(a, b);
    }
    public double len_complex(double a, double b) {
        return Math.hypot(a, b);
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    double len_complex(double a, double b);\n};",
        "reference_solution_cpp": """#include <cmath>
class Solution {
public:
    double len_complex(double a, double b) {
        return std::hypot(a, b);
    }
};"""
    },

    644: {
        "starter_code_javascript": "function min_jumps(arr, n) {\n    return 0;\n}",
        "reference_solution_javascript": """function min_jumps(arr, n) {
    if (n === 0 || arr[0] === 0) return Infinity;
    const jumps = new Array(n).fill(Infinity);
    jumps[0] = 0;
    for (let i = 1; i < n; i++) {
        for (let j = 0; j < i; j++) {
            if (i <= j + arr[j] && jumps[j] !== Infinity) {
                jumps[i] = Math.min(jumps[i], jumps[j] + 1);
                break;
            }
        }
    }
    return jumps[n - 1];
}""",
        "starter_code_java": "class Solution {\n    public int min_jumps(int[] arr, int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int min_jumps(int[] arr, int n) {
        if (n == 0 || arr[0] == 0) return Integer.MAX_VALUE;
        int[] jumps = new int[n];
        for (int i = 1; i < n; i++) jumps[i] = Integer.MAX_VALUE;
        jumps[0] = 0;
        for (int i = 1; i < n; i++) {
            for (int j = 0; j < i; j++) {
                if (i <= j + arr[j] && jumps[j] != Integer.MAX_VALUE) {
                    jumps[i] = Math.min(jumps[i], jumps[j] + 1);
                    break;
                }
            }
        }
        return jumps[n - 1];
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    int min_jumps(const std::vector<int>& arr, int n);\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
class Solution {
public:
    int min_jumps(const std::vector<int>& arr, int n) {
        if (n == 0 || arr[0] == 0) return 1e9;
        std::vector<int> jumps(n, 1e9);
        jumps[0] = 0;
        for (int i = 1; i < n; i++) {
            for (int j = 0; j < i; j++) {
                if (i <= j + arr[j] && jumps[j] != 1e9) {
                    jumps[i] = std::min(jumps[i], jumps[j] + 1);
                    break;
                }
            }
        }
        return jumps[n - 1];
    }
};"""
    },

    645: {
        "starter_code_javascript": "function mul_consecutive_nums(nums) {\n    return [];\n}",
        "reference_solution_javascript": """function mul_consecutive_nums(nums) {
    const res = [];
    for (let i = 0; i < nums.length - 1; i++) res.push(nums[i] * nums[i + 1]);
    return res;
}""",
        "starter_code_java": "class Solution {\n    public int[] mul_consecutive_nums(int[] nums) {\n        return new int[0];\n    }\n}",
        "reference_solution_java": """class Solution {
    public int[] mul_consecutive_nums(int[] nums) {
        if (nums.length < 2) return new int[0];
        int[] res = new int[nums.length - 1];
        for (int i = 0; i < res.length; i++) res[i] = nums[i] * nums[i + 1];
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    std::vector<int> mul_consecutive_nums(const std::vector<int>& nums);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    std::vector<int> mul_consecutive_nums(const std::vector<int>& nums) {
        if (nums.size() < 2) return {};
        std::vector<int> res(nums.size() - 1);
        for (size_t i = 0; i < res.size(); i++) res[i] = nums[i] * nums[i + 1];
        return res;
    }
};"""
    },

    646: {
        "starter_code_javascript": "function last_Two_Digits(N) {\n    return 0;\n}",
        "reference_solution_javascript": """function last_Two_Digits(N) {
    if (N >= 10) return 0;
    let fac = 1;
    for (let i = 1; i <= N; i++) fac = (fac * i) % 100;
    return fac;
}""",
        "starter_code_java": "class Solution {\n    public int last_Two_Digits(int N) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int last_Two_Digits(int N) {
        if (N >= 10) return 0;
        int fac = 1;
        for (int i = 1; i <= N; i++) fac = (fac * i) % 100;
        return fac;
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    int last_Two_Digits(int N);\n};",
        "reference_solution_cpp": """class Solution {
public:
    int last_Two_Digits(int N) {
        if (N >= 10) return 0;
        int fac = 1;
        for (int i = 1; i <= N; i++) fac = (fac * i) % 100;
        return fac;
    }
};"""
    },

    647: {
        "starter_code_javascript": "function remove_multiple_spaces(text1) {\n    return '';\n}",
        "reference_solution_javascript": """function remove_multiple_spaces(text1) {
    return text1.replace(/ +/g, ' ');
}""",
        "starter_code_java": "class Solution {\n    public String remove_multiple_spaces(String text1) {\n        return "";\n    }\n}",
        "reference_solution_java": """class Solution {
    public String remove_multiple_spaces(String text1) {
        return text1.replaceAll(" +", " ");
    }
}""",
        "starter_code_cpp": "#include <string>\nclass Solution {\npublic:\n    std::string remove_multiple_spaces(const std::string& text1);\n};",
        "reference_solution_cpp": """#include <string>
#include <regex>
class Solution {
public:
    std::string remove_multiple_spaces(const std::string& text1) {
        std::regex re(" +");
        return std::regex_replace(text1, re, " ");
    }
};"""
    },

    648: {
        "starter_code_javascript": "function extract_unique(test_dict) {\n    return [];\n}",
        "reference_solution_javascript": """function extract_unique(test_dict) {
    const set = new Set();
    for (const k of Object.keys(test_dict)) {
        for (const v of test_dict[k]) set.add(v);
    }
    return Array.from(set).sort((a, b) => a - b);
}""",
        "starter_code_java": "import java.util.Map;\nclass Solution {\n    public int[] extract_unique(Map<Object, Object> test_dict) {\n        return new int[0];\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[] extract_unique(Map<Object, Object> test_dict) {
        Set<Integer> set = new TreeSet<>();
        for (Object val : test_dict.values()) {
            if (val instanceof int[]) {
                for (int x : (int[]) val) set.add(x);
            }
        }
        int[] res = new int[set.size()];
        int idx = 0;
        for (int x : set) res[idx++] = x;
        return res;
    }
}""",
        "starter_code_cpp": "#include <unordered_map>\n#include <vector>\n#include <string>\nclass Solution {\npublic:\n    std::vector<int> extract_unique(const std::unordered_map<std::string, std::vector<int>>& test_dict);\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <unordered_map>
#include <set>
class Solution {
public:
    std::vector<int> extract_unique(const std::unordered_map<std::string, std::vector<int>>& test_dict) {
        std::set<int> unique_vals;
        for (const auto& p : test_dict) {
            for (int x : p.second) unique_vals.insert(x);
        }
        return std::vector<int>(unique_vals.begin(), unique_vals.end());
    }
};"""
    },

    649: {
        "starter_code_javascript": "function check_greater(test_tup1, test_tup2) {\n    return false;\n}",
        "reference_solution_javascript": """function check_greater(test_tup1, test_tup2) {
    for (let i = 0; i < test_tup1.length; i++) {
        if (test_tup1[i] >= test_tup2[i]) return false;
    }
    return true;
}""",
        "starter_code_java": "class Solution {\n    public boolean check_greater(int[] test_tup1, int[] test_tup2) {\n        return false;\n    }\n}",
        "reference_solution_java": """class Solution {
    public boolean check_greater(int[] test_tup1, int[] test_tup2) {
        for (int i = 0; i < test_tup1.length; i++) {
            if (test_tup1[i] >= test_tup2[i]) return false;
        }
        return true;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    bool check_greater(const std::vector<int>& test_tup1, const std::vector<int>& test_tup2);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    bool check_greater(const std::vector<int>& test_tup1, const std::vector<int>& test_tup2) {
        for (size_t i = 0; i < test_tup1.size(); i++) {
            if (test_tup1[i] >= test_tup2[i]) return false;
        }
        return true;
    }
};"""
    },

    650: {
        "starter_code_javascript": "function zip_list(list1, list2) {\n    return [];\n}",
        "reference_solution_javascript": """function zip_list(list1, list2) {
    return list1.map((item, idx) => item.concat(list2[idx]));
}""",
        "starter_code_java": "class Solution {\n    public int[][] zip_list(int[][] a, int[][] b) {\n        return new int[0][0];\n    }\n}",
        "reference_solution_java": """class Solution {
    public int[][] zip_list(int[][] a, int[][] b) {
        int[][] res = new int[a.length][];
        for (int i = 0; i < a.length; i++) {
            res[i] = new int[a[i].length + b[i].length];
            System.arraycopy(a[i], 0, res[i], 0, a[i].length);
            System.arraycopy(b[i], 0, res[i], a[i].length, b[i].length);
        }
        return res;
    }
    public String[][] zip_list(char[][] a, char[][] b) {
        String[][] res = new String[a.length][];
        for (int i = 0; i < a.length; i++) {
            res[i] = new String[a[i].length + b[i].length];
            for (int j = 0; j < a[i].length; j++) res[i][j] = String.valueOf(a[i][j]);
            for (int j = 0; j < b[i].length; j++) res[i][a[i].length + j] = String.valueOf(b[i][j]);
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    std::vector<std::vector<int>> zip_list(const std::vector<std::vector<int>>& a, const std::vector<std::vector<int>>& b);\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
class Solution {
public:
    std::vector<std::vector<int>> zip_list(const std::vector<std::vector<int>>& a, const std::vector<std::vector<int>>& b) {
        std::vector<std::vector<int>> res(a.size());
        for (size_t i = 0; i < a.size(); i++) {
            res[i] = a[i];
            res[i].insert(res[i].end(), b[i].begin(), b[i].end());
        }
        return res;
    }
    std::vector<std::vector<std::string>> zip_list(const std::vector<std::vector<char>>& a, const std::vector<std::vector<char>>& b) {
        std::vector<std::vector<std::string>> res(a.size());
        for (size_t i = 0; i < a.size(); i++) {
            for (char c : a[i]) res[i].push_back(std::string(1, c));
            for (char c : b[i]) res[i].push_back(std::string(1, c));
        }
        return res;
    }
};"""
    },

    651: {
        "starter_code_javascript": "function count_even(array_nums) {\n    return 0;\n}",
        "reference_solution_javascript": """function count_even(array_nums) {
    return array_nums.filter(x => x % 2 === 0).length;
}""",
        "starter_code_java": "class Solution {\n    public int count_even(int[] array_nums) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int count_even(int[] array_nums) {
        int count = 0;
        for (int x : array_nums) if (x % 2 == 0) count++;
        return count;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    int count_even(const std::vector<int>& array_nums);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    int count_even(const std::vector<int>& array_nums) {
        int count = 0;
        for (int x : array_nums) if (x % 2 == 0) count++;
        return count;
    }
};"""
    },

    652: {
        "starter_code_javascript": "function min_Swaps(str1, str2) {\n    return 0;\n}",
        "reference_solution_javascript": """function min_Swaps(str1, str2) {
    let count = 0;
    for (let i = 0; i < str1.length; i++) if (str1[i] !== str2[i]) count++;
    if (count % 2 === 0) return Math.floor(count / 2);
    return "Not Possible";
}""",
        "starter_code_java": "class Solution {\n    public Object min_Swaps(String str1, String str2) {\n        return null;\n    }\n}",
        "reference_solution_java": """class Solution {
    public Object min_Swaps(String str1, String str2) {
        int count = 0;
        for (int i = 0; i < str1.length(); i++) if (str1.charAt(i) != str2.charAt(i)) count++;
        if (count % 2 == 0) return count / 2;
        return "Not Possible";
    }
}""",
        "starter_code_cpp": "#include <string>\nclass Solution {\npublic:\n    std::string min_Swaps(const std::string& str1, const std::string& str2);\n};",
        "reference_solution_cpp": """#include <string>
class Solution {
public:
    std::string min_Swaps(const std::string& str1, const std::string& str2) {
        int count = 0;
        for (size_t i = 0; i < str1.size(); i++) if (str1[i] != str2[i]) count++;
        if (count % 2 == 0) return std::to_string(count / 2);
        return "Not Possible";
    }
};"""
    },

    653: {
        "starter_code_javascript": "function count_range_in_list(li, min, max) {\n    return 0;\n}",
        "reference_solution_javascript": """function count_range_in_list(li, min, max) {
    let count = 0;
    for (const x of li) if (x >= min && x <= max) count++;
    return count;
}""",
        "starter_code_java": "class Solution {\n    public int count_range_in_list(int[] li, int min, int max) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int count_range_in_list(int[] li, int min, int max) {
        int count = 0;
        for (int x : li) if (x >= min && x <= max) count++;
        return count;
    }
    public int count_range_in_list(String[] li, String min, String max) {
        int count = 0;
        for (String x : li) if (x.compareTo(min) >= 0 && x.compareTo(max) <= 0) count++;
        return count;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    int count_range_in_list(const std::vector<int>& li, int min_val, int max_val);\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
class Solution {
public:
    int count_range_in_list(const std::vector<int>& li, int min_val, int max_val) {
        int count = 0;
        for (int x : li) if (x >= min_val && x <= max_val) count++;
        return count;
    }
    int count_range_in_list(const std::vector<std::string>& li, const std::string& min_val, const std::string& max_val) {
        int count = 0;
        for (const auto& x : li) if (x >= min_val && x <= max_val) count++;
        return count;
    }
};"""
    },

    654: {
        "starter_code_javascript": "function equilibrium_index(arr) {\n    return 0;\n}",
        "reference_solution_javascript": """function equilibrium_index(arr) {
    let total = arr.reduce((a, b) => a + b, 0);
    let left = 0;
    for (let i = 0; i < arr.length; i++) {
        total -= arr[i];
        if (left === total) return i;
        left += arr[i];
    }
    return -1;
}""",
        "starter_code_java": "class Solution {\n    public int equilibrium_index(int[] arr) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int equilibrium_index(int[] arr) {
        long total = 0;
        for (int x : arr) total += x;
        long left = 0;
        for (int i = 0; i < arr.length; i++) {
            total -= arr[i];
            if (left == total) return i;
            left += arr[i];
        }
        return -1;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    int equilibrium_index(const std::vector<int>& arr);\n};",
        "reference_solution_cpp": """#include <vector>
#include <numeric>
class Solution {
public:
    int equilibrium_index(const std::vector<int>& arr) {
        long long total = std::accumulate(arr.begin(), arr.end(), 0LL);
        long long left = 0;
        for (size_t i = 0; i < arr.size(); i++) {
            total -= arr[i];
            if (left == total) return (int)i;
            left += arr[i];
        }
        return -1;
    }
};"""
    },

    655: {
        "starter_code_javascript": "function removals(arr, n, k) {\n    return 0;\n}",
        "reference_solution_javascript": """function removals(arr, n, k) {
    arr.sort((a, b) => a - b);
    let maxKeep = 0;
    let j = 0;
    for (let i = 0; i < n; i++) {
        while (j < n && arr[j] - arr[i] <= k) j++;
        maxKeep = Math.max(maxKeep, j - i);
    }
    return n - maxKeep;
}""",
        "starter_code_java": "class Solution {\n    public int removals(int[] arr, int n, int k) {\n        return 0;\n    }\n}",
        "reference_solution_java": """import java.util.Arrays;
class Solution {
    public int removals(int[] arr, int n, int k) {
        Arrays.sort(arr);
        int maxKeep = 0;
        int j = 0;
        for (int i = 0; i < n; i++) {
            while (j < n && arr[j] - arr[i] <= k) j++;
            maxKeep = Math.max(maxKeep, j - i);
        }
        return n - maxKeep;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    int removals(std::vector<int> arr, int n, int k);\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
class Solution {
public:
    int removals(std::vector<int> arr, int n, int k) {
        std::sort(arr.begin(), arr.end());
        int maxKeep = 0;
        int j = 0;
        for (int i = 0; i < n; i++) {
            while (j < n && arr[j] - arr[i] <= k) j++;
            maxKeep = std::max(maxKeep, j - i);
        }
        return n - maxKeep;
    }
};"""
    },

    656: {
        "starter_code_javascript": "function harmonic_sum(n) {\n    return 0.0;\n}",
        "reference_solution_javascript": """function harmonic_sum(n) {
    let sum = 0;
    for (let i = 1; i <= n; i++) sum += 1 / i;
    return sum;
}""",
        "starter_code_java": "class Solution {\n    public double harmonic_sum(int n) {\n        return 0.0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public double harmonic_sum(int n) {
        double sum = 0.0;
        for (int i = 1; i <= n; i++) sum += 1.0 / i;
        return sum;
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    double harmonic_sum(int n);\n};",
        "reference_solution_cpp": """class Solution {
public:
    double harmonic_sum(int n) {
        double sum = 0.0;
        for (int i = 1; i <= n; i++) sum += 1.0 / i;
        return sum;
    }
};"""
    },

    657: {
        "starter_code_javascript": "function sort_sublists(list1) {\n    return [];\n}",
        "reference_solution_javascript": """function sort_sublists(list1) {
    return list1.sort((a, b) => {
        if (a.length !== b.length) return a.length - b.length;
        for (let i = 0; i < Math.min(a.length, b.length); i++) {
            if (a[i] < b[i]) return -1;
            if (a[i] > b[i]) return 1;
        }
        return 0;
    });
}""",
        "starter_code_java": "class Solution {\n    public int[][] sort_sublists(int[][] list1) {\n        return new int[0][0];\n    }\n}",
        "reference_solution_java": """import java.util.Arrays;
class Solution {
    public int[][] sort_sublists(int[][] list1) {
        Arrays.sort(list1, (a, b) -> {
            if (a.length != b.length) return Integer.compare(a.length, b.length);
            for (int i = 0; i < Math.min(a.length, b.length); i++) {
                if (a[i] != b[i]) return Integer.compare(a[i], b[i]);
            }
            return 0;
        });
        return list1;
    }
    public String[][] sort_sublists(String[][] list1) {
        Arrays.sort(list1, (a, b) -> {
            if (a.length != b.length) return Integer.compare(a.length, b.length);
            for (int i = 0; i < Math.min(a.length, b.length); i++) {
                int cmp = a[i].compareTo(b[i]);
                if (cmp != 0) return cmp;
            }
            return 0;
        });
        return list1;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    std::vector<std::vector<int>> sort_sublists(std::vector<std::vector<int>> list1);\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <algorithm>
class Solution {
public:
    std::vector<std::vector<int>> sort_sublists(std::vector<std::vector<int>> list1) {
        std::sort(list1.begin(), list1.end(), [](const std::vector<int>& a, const std::vector<int>& b) {
            if (a.size() != b.size()) return a.size() < b.size();
            return a < b;
        });
        return list1;
    }
    std::vector<std::vector<std::string>> sort_sublists(std::vector<std::vector<std::string>> list1) {
        std::sort(list1.begin(), list1.end(), [](const std::vector<std::string>& a, const std::vector<std::string>& b) {
            if (a.size() != b.size()) return a.size() < b.size();
            return a < b;
        });
        return list1;
    }
};"""
    },

    658: {
        "starter_code_javascript": "function is_subset(arr1, m, arr2, n) {\n    return false;\n}",
        "reference_solution_javascript": """function is_subset(arr1, m, arr2, n) {
    const set = new Set(arr1.slice(0, m));
    for (let i = 0; i < n; i++) {
        if (!set.has(arr2[i])) return false;
    }
    return true;
}""",
        "starter_code_java": "class Solution {\n    public boolean is_subset(int[] arr1, int m, int[] arr2, int n) {\n        return false;\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public boolean is_subset(int[] arr1, int m, int[] arr2, int n) {
        Set<Integer> set = new HashSet<>();
        for (int i = 0; i < m; i++) set.add(arr1[i]);
        for (int i = 0; i < n; i++) {
            if (!set.contains(arr2[i])) return false;
        }
        return true;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    bool is_subset(const std::vector<int>& arr1, int m, const std::vector<int>& arr2, int n);\n};",
        "reference_solution_cpp": """#include <vector>
#include <unordered_set>
class Solution {
public:
    bool is_subset(const std::vector<int>& arr1, int m, const std::vector<int>& arr2, int n) {
        std::unordered_set<int> set;
        for (int i = 0; i < m; i++) set.insert(arr1[i]);
        for (int i = 0; i < n; i++) {
            if (set.find(arr2[i]) == set.end()) return false;
        }
        return true;
    }
};"""
    },

    659: {
        "starter_code_javascript": "function count_Set_Bits(n) {\n    return 0;\n}",
        "reference_solution_javascript": """function count_Set_Bits(n) {
    n += 1;
    let powerOf2 = 2;
    let cnt = Math.floor(n / 2);
    while (powerOf2 <= n) {
        const totalPairs = Math.floor(n / powerOf2);
        cnt += Math.floor(totalPairs / 2) * powerOf2;
        if (totalPairs & 1) {
            cnt += (n % powerOf2);
        }
        powerOf2 <<= 1;
    }
    return cnt;
}""",
        "starter_code_java": "class Solution {\n    public int count_Set_Bits(int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int count_Set_Bits(int n) {
        n += 1;
        int powerOf2 = 2;
        int cnt = n / 2;
        while (powerOf2 <= n) {
            int totalPairs = n / powerOf2;
            cnt += (totalPairs / 2) * powerOf2;
            if ((totalPairs & 1) != 0) {
                cnt += (n % powerOf2);
            }
            powerOf2 <<= 1;
        }
        return cnt;
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    int count_Set_Bits(int n);\n};",
        "reference_solution_cpp": """class Solution {
public:
    int count_Set_Bits(int n) {
        n += 1;
        int powerOf2 = 2;
        int cnt = n / 2;
        while (powerOf2 <= n) {
            int totalPairs = n / powerOf2;
            cnt += (totalPairs / 2) * powerOf2;
            if (totalPairs & 1) {
                cnt += (n % powerOf2);
            }
            powerOf2 <<= 1;
        }
        return cnt;
    }
};"""
    },

    660: {
        "starter_code_javascript": "function Convert(string) {\n    return [];\n}",
        "reference_solution_javascript": """function Convert(string) {
    return string.split(' ');
}""",
        "starter_code_java": "class Solution {\n    public String[] Convert(String string) {\n        return new String[0];\n    }\n}",
        "reference_solution_java": """class Solution {
    public String[] Convert(String string) {
        return string.split(" ");
    }
}""",
        "starter_code_cpp": "#include <vector>\n#include <string>\nclass Solution {\npublic:\n    std::vector<std::string> Convert(const std::string& string);\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <sstream>
class Solution {
public:
    std::vector<std::string> Convert(const std::string& string) {
        std::vector<std::string> res;
        std::stringstream ss(string);
        std::string token;
        while (ss >> token) res.push_back(token);
        return res;
    }
};"""
    }
}
