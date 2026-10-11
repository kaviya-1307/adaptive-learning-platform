"""
Curated and specialized solutions for MBPP problems (Batch 13: 661-710).
"""

BATCH13_SOLUTIONS = {
    661: {
        "starter_code_javascript": "function get_unique(test_list) {\n    return '';\n}",
        "reference_solution_javascript": """function get_unique(test_list) {
    const map = new Map();
    for (const sub of test_list) {
        if (!map.has(sub[1])) map.set(sub[1], new Set());
        map.get(sub[1]).add(sub[0]);
    }
    const pairs = [];
    for (const [k, s] of map.entries()) {
        pairs.push(`${k}: ${s.size}`);
    }
    return `{${pairs.join(', ')}}`;
}""",
        "starter_code_java": "class Solution {\n    public String get_unique(int[][] test_list) {\n        return "";\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public String get_unique(int[][] test_list) {
        Map<Integer, Set<Integer>> map = new LinkedHashMap<>();
        for (int[] sub : test_list) {
            map.computeIfAbsent(sub[1], k -> new HashSet<>()).add(sub[0]);
        }
        StringBuilder sb = new StringBuilder("{");
        boolean first = true;
        for (Map.Entry<Integer, Set<Integer>> e : map.entrySet()) {
            if (!first) sb.append(", ");
            first = false;
            sb.append(e.getKey()).append(": ").append(e.getValue().size());
        }
        sb.append("}");
        return sb.toString();
    }
}""",
        "starter_code_cpp": "#include <vector>\n#include <string>\nclass Solution {\npublic:\n    std::string get_unique(const std::vector<std::vector<int>>& test_list);\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <sstream>
class Solution {
public:
    std::string get_unique(const std::vector<std::vector<int>>& test_list) {
        std::unordered_map<int, std::unordered_set<int>> map;
        std::vector<int> order;
        for (const auto& sub : test_list) {
            int key = sub[1];
            int val = sub[0];
            if (map.find(key) == map.end()) order.push_back(key);
            map[key].insert(val);
        }
        std::ostringstream oss;
        oss << "{";
        for (size_t i = 0; i < order.size(); i++) {
            if (i > 0) oss << ", ";
            oss << order[i] << ": " << map[order[i]].size();
        }
        oss << "}";
        return oss.str();
    }
};"""
    },

    662: {
        "starter_code_javascript": "function product_Equal(n) {\n    return false;\n}",
        "reference_solution_javascript": """function product_Equal(n) {
    if (n < 10) return false;
    let prodOdd = 1, prodEven = 1;
    while (n > 0) {
        let digit = n % 10;
        prodOdd *= digit;
        n = Math.floor(n / 10);
        if (n === 0) break;
        digit = n % 10;
        prodEven *= digit;
        n = Math.floor(n / 10);
    }
    return prodOdd === prodEven;
}""",
        "starter_code_java": "class Solution {\n    public boolean product_Equal(int n) {\n        return false;\n    }\n}",
        "reference_solution_java": """class Solution {
    public boolean product_Equal(int n) {
        if (n < 10) return false;
        long prodOdd = 1, prodEven = 1;
        while (n > 0) {
            int digit = n % 10;
            prodOdd *= digit;
            n /= 10;
            if (n == 0) break;
            digit = n % 10;
            prodEven *= digit;
            n /= 10;
        }
        return prodOdd == prodEven;
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    bool product_Equal(int n);\n};",
        "reference_solution_cpp": """class Solution {
public:
    bool product_Equal(int n) {
        if (n < 10) return false;
        long long prodOdd = 1, prodEven = 1;
        while (n > 0) {
            int digit = n % 10;
            prodOdd *= digit;
            n /= 10;
            if (n == 0) break;
            digit = n % 10;
            prodEven *= digit;
            n /= 10;
        }
        return prodOdd == prodEven;
    }
};"""
    },

    663: {
        "starter_code_javascript": "function remove_duplicate(list1) {\n    return [];\n}",
        "reference_solution_javascript": """function remove_duplicate(list1) {
    if (list1.length === 0) return [];
    if (Array.isArray(list1[0])) {
        list1.sort((a, b) => {
            for (let i = 0; i < Math.min(a.length, b.length); i++) {
                if (a[i] !== b[i]) return a[i] - b[i];
            }
            return a.length - b.length;
        });
        const res = [list1[0]];
        for (let i = 1; i < list1.length; i++) {
            const prev = res[res.length - 1];
            const curr = list1[i];
            if (prev.length !== curr.length || !prev.every((v, idx) => v === curr[idx])) {
                res.push(curr);
            }
        }
        return res;
    }
    list1.sort((a, b) => (a < b ? -1 : a > b ? 1 : 0));
    return list1.filter((x, i) => i === 0 || x !== list1[i - 1]);
}""",
        "starter_code_java": "class Solution {\n    public int[] remove_duplicate(int[] list1) {\n        return new int[0];\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[][] remove_duplicate(int[][] list1) {
        Arrays.sort(list1, (a, b) -> {
            for (int i = 0; i < Math.min(a.length, b.length); i++) {
                if (a[i] != b[i]) return Integer.compare(a[i], b[i]);
            }
            return Integer.compare(a.length, b.length);
        });
        List<int[]> res = new ArrayList<>();
        if (list1.length > 0) res.add(list1[0]);
        for (int i = 1; i < list1.length; i++) {
            if (!Arrays.equals(list1[i], res.get(res.size() - 1))) {
                res.add(list1[i]);
            }
        }
        return res.toArray(new int[0][]);
    }
    public String[] remove_duplicate(String[] list1) {
        Arrays.sort(list1);
        List<String> res = new ArrayList<>();
        if (list1.length > 0) res.add(list1[0]);
        for (int i = 1; i < list1.length; i++) {
            if (!list1[i].equals(res.get(res.size() - 1))) {
                res.add(list1[i]);
            }
        }
        return res.toArray(new String[0]);
    }
    public int[] remove_duplicate(int[] list1) {
        Arrays.sort(list1);
        List<Integer> res = new ArrayList<>();
        if (list1.length > 0) res.add(list1[0]);
        for (int i = 1; i < list1.length; i++) {
            if (list1[i] != res.get(res.size() - 1)) {
                res.add(list1[i]);
            }
        }
        int[] out = new int[res.size()];
        for (int i = 0; i < out.length; i++) out[i] = res.get(i);
        return out;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    std::vector<int> remove_duplicate(std::vector<int> list1);\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <algorithm>
class Solution {
public:
    std::vector<std::vector<int>> remove_duplicate(std::vector<std::vector<int>> a) {
        std::sort(a.begin(), a.end());
        a.erase(std::unique(a.begin(), a.end()), a.end());
        return a;
    }
    std::vector<std::string> remove_duplicate(std::vector<std::string> a) {
        std::sort(a.begin(), a.end());
        a.erase(std::unique(a.begin(), a.end()), a.end());
        return a;
    }
    std::vector<int> remove_duplicate(std::vector<int> a) {
        std::sort(a.begin(), a.end());
        a.erase(std::unique(a.begin(), a.end()), a.end());
        return a;
    }
};"""
    },

    664: {
        "starter_code_javascript": "function check_valid(test_tup) {\n    return false;\n}",
        "reference_solution_javascript": """function check_valid(test_tup) {
    return test_tup.every(x => Boolean(x));
}""",
        "starter_code_java": "class Solution {\n    public boolean check_valid(boolean[] test_tup) {\n        return false;\n    }\n}",
        "reference_solution_java": """class Solution {
    public boolean check_valid(boolean[] test_tup) {
        for (boolean b : test_tup) if (!b) return false;
        return true;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    bool check_valid(const std::vector<bool>& test_tup);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    bool check_valid(const std::vector<bool>& test_tup) {
        for (bool b : test_tup) if (!b) return false;
        return true;
    }
};"""
    },

    665: {
        "starter_code_javascript": "function count_Fac(n) {\n    return 0;\n}",
        "reference_solution_javascript": """function count_Fac(n) {
    let m = n;
    let count = 0;
    let i = 2;
    while (i * i <= m) {
        let total = 0;
        while (n % i === 0) {
            n = Math.floor(n / i);
            total++;
        }
        let temp = 0;
        let j = 1;
        while (temp + j <= total) {
            temp += j;
            count++;
            j++;
        }
        i++;
    }
    if (n !== 1) count++;
    return count;
}""",
        "starter_code_java": "class Solution {\n    public int count_Fac(int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int count_Fac(int n) {
        int m = n;
        int count = 0;
        int i = 2;
        while (i * i <= m) {
            int total = 0;
            while (n % i == 0) {
                n /= i;
                total++;
            }
            int temp = 0;
            int j = 1;
            while (temp + j <= total) {
                temp += j;
                count++;
                j++;
            }
            i++;
        }
        if (n != 1) count++;
        return count;
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    int count_Fac(int n);\n};",
        "reference_solution_cpp": """class Solution {
public:
    int count_Fac(int n) {
        int m = n;
        int count = 0;
        int i = 2;
        while (i * i <= m) {
            int total = 0;
            while (n % i == 0) {
                n /= i;
                total++;
            }
            int temp = 0;
            int j = 1;
            while (temp + j <= total) {
                temp += j;
                count++;
                j++;
            }
            i++;
        }
        if (n != 1) count++;
        return count;
    }
};"""
    },

    666: {
        "starter_code_javascript": "function rombus_perimeter(a) {\n    return 0;\n}",
        "reference_solution_javascript": """function rombus_perimeter(a) {
    return 4 * a;
}""",
        "starter_code_java": "class Solution {\n    public int rombus_perimeter(int a) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int rombus_perimeter(int a) {
        return 4 * a;
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    int rombus_perimeter(int a);\n};",
        "reference_solution_cpp": """class Solution {
public:
    int rombus_perimeter(int a) {
        return 4 * a;
    }
};"""
    },

    667: {
        "starter_code_javascript": "function alternate_elements(list1) {\n    return [];\n}",
        "reference_solution_javascript": """function alternate_elements(list1) {
    return list1.filter((_, i) => i % 2 === 0);
}""",
        "starter_code_java": "class Solution {\n    public int[] alternate_elements(int[] list1) {\n        return new int[0];\n    }\n}",
        "reference_solution_java": """class Solution {
    public String[] alternate_elements(String[] list1) {
        int n = (list1.length + 1) / 2;
        String[] res = new String[n];
        for (int i = 0; i < n; i++) res[i] = list1[i * 2];
        return res;
    }
    public int[] alternate_elements(int[] list1) {
        int n = (list1.length + 1) / 2;
        int[] res = new int[n];
        for (int i = 0; i < n; i++) res[i] = list1[i * 2];
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    std::vector<int> alternate_elements(const std::vector<int>& list1);\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
class Solution {
public:
    std::vector<std::string> alternate_elements(const std::vector<std::string>& list1) {
        std::vector<std::string> res;
        for (size_t i = 0; i < list1.size(); i += 2) res.push_back(list1[i]);
        return res;
    }
    std::vector<int> alternate_elements(const std::vector<int>& list1) {
        std::vector<int> res;
        for (size_t i = 0; i < list1.size(); i += 2) res.push_back(list1[i]);
        return res;
    }
};"""
    },

    668: {
        "starter_code_javascript": "function text_match(text) {\n    return '';\n}",
        "reference_solution_javascript": """function text_match(text) {
    return text.includes('a') ? 'Found a match!' : 'Not matched!';
}""",
        "starter_code_java": "class Solution {\n    public String text_match(String text) {\n        return "";\n    }\n}",
        "reference_solution_java": """class Solution {
    public String text_match(String text) {
        return text.contains("a") ? "Found a match!" : "Not matched!";
    }
}""",
        "starter_code_cpp": "#include <string>\nclass Solution {\npublic:\n    std::string text_match(const std::string& text);\n};",
        "reference_solution_cpp": """#include <string>
class Solution {
public:
    std::string text_match(const std::string& text) {
        return text.find('a') != std::string::npos ? "Found a match!" : "Not matched!";
    }
};"""
    },

    669: {
        "starter_code_javascript": "function maxAverageOfPath(cost, N) {\n    return 0.0;\n}",
        "reference_solution_javascript": """function maxAverageOfPath(cost, N) {
    const dp = Array.from({length: N}, () => new Array(N).fill(0));
    dp[0][0] = cost[0][0];
    for (let i = 1; i < N; i++) dp[i][0] = dp[i - 1][0] + cost[i][0];
    for (let j = 1; j < N; j++) dp[0][j] = dp[0][j - 1] + cost[0][j];
    for (let i = 1; i < N; i++) {
        for (let j = 1; j < N; j++) {
            dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]) + cost[i][j];
        }
    }
    return dp[N - 1][N - 1] / (2 * N - 1);
}""",
        "starter_code_java": "class Solution {\n    public double maxAverageOfPath(int[][] cost, int N) {\n        return 0.0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public double maxAverageOfPath(int[][] cost, int N) {
        int[][] dp = new int[N][N];
        dp[0][0] = cost[0][0];
        for (int i = 1; i < N; i++) dp[i][0] = dp[i - 1][0] + cost[i][0];
        for (int j = 1; j < N; j++) dp[0][j] = dp[0][j - 1] + cost[0][j];
        for (int i = 1; i < N; i++) {
            for (int j = 1; j < N; j++) {
                dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]) + cost[i][j];
            }
        }
        return (double) dp[N - 1][N - 1] / (2.0 * N - 1.0);
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    double maxAverageOfPath(const std::vector<std::vector<int>>& cost, int N);\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
class Solution {
public:
    double maxAverageOfPath(const std::vector<std::vector<int>>& cost, int N) {
        std::vector<std::vector<int>> dp(N, std::vector<int>(N, 0));
        dp[0][0] = cost[0][0];
        for (int i = 1; i < N; i++) dp[i][0] = dp[i - 1][0] + cost[i][0];
        for (int j = 1; j < N; j++) dp[0][j] = dp[0][j - 1] + cost[0][j];
        for (int i = 1; i < N; i++) {
            for (int j = 1; j < N; j++) {
                dp[i][j] = std::max(dp[i - 1][j], dp[i][j - 1]) + cost[i][j];
            }
        }
        return (double)dp[N - 1][N - 1] / (2.0 * N - 1.0);
    }
};"""
    },

    670: {
        "starter_code_javascript": "function filter_data(students, h, w) {\n    return {};\n}",
        "reference_solution_javascript": """function filter_data(students, h, w) {
    const res = {};
    for (const [k, s] of Object.entries(students)) {
        if (s[0] >= h && s[1] >= w) {
            res[k] = s;
        }
    }
    return res;
}""",
        "starter_code_java": "import java.util.Map;\nclass Solution {\n    public Map<Object, Object> filter_data(Map<Object, Object> students, double h, int w) {\n        return null;\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public Map<Object, Object> filter_data(Map<Object, Object> students, double h, int w) {
        Map<Object, Object> res = new LinkedHashMap<>();
        for (Map.Entry<Object, Object> e : students.entrySet()) {
            if (e.getValue() instanceof Object[]) {
                Object[] arr = (Object[]) e.getValue();
                double height = ((Number) arr[0]).doubleValue();
                int weight = ((Number) arr[1]).intValue();
                if (height >= h && weight >= w) {
                    res.put(e.getKey(), arr);
                }
            }
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <unordered_map>\n#include <vector>\n#include <string>\nclass Solution {\npublic:\n    std::unordered_map<std::string, std::vector<std::string>> filter_data(const std::unordered_map<std::string, std::vector<std::string>>& students, double h, int w);\n};",
        "reference_solution_cpp": """#include <unordered_map>
#include <vector>
#include <string>
class Solution {
public:
    std::unordered_map<std::string, std::vector<std::string>> filter_data(
        const std::unordered_map<std::string, std::vector<std::string>>& students,
        double h,
        int w
    ) {
        std::unordered_map<std::string, std::vector<std::string>> res;
        for (const auto& p : students) {
            double height = std::stod(p.second[0]);
            int weight = std::stoi(p.second[1]);
            if (height >= h && weight >= w) {
                res[p.first] = p.second;
            }
        }
        return res;
    }
};"""
    },

    671: {
        "starter_code_javascript": "function count_same_pair(nums1, nums2) {\n    return 0;\n}",
        "reference_solution_javascript": """function count_same_pair(nums1, nums2) {
    let count = 0;
    const n = Math.min(nums1.length, nums2.length);
    for (let i = 0; i < n; i++) {
        if (nums1[i] === nums2[i]) count++;
    }
    return count;
}""",
        "starter_code_java": "class Solution {\n    public int count_same_pair(int[] nums1, int[] nums2) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int count_same_pair(int[] nums1, int[] nums2) {
        int count = 0;
        int n = Math.min(nums1.length, nums2.length);
        for (int i = 0; i < n; i++) {
            if (nums1[i] == nums2[i]) count++;
        }
        return count;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    int count_same_pair(const std::vector<int>& nums1, const std::vector<int>& nums2);\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
class Solution {
public:
    int count_same_pair(const std::vector<int>& nums1, const std::vector<int>& nums2) {
        int count = 0;
        size_t n = std::min(nums1.size(), nums2.size());
        for (size_t i = 0; i < n; i++) {
            if (nums1[i] == nums2[i]) count++;
        }
        return count;
    }
};"""
    },

    672: {
        "starter_code_javascript": "function power_base_sum(base, power) {\n    return 0;\n}",
        "reference_solution_javascript": """function power_base_sum(base, power) {
    const p = BigInt(base) ** BigInt(power);
    const s = p.toString();
    let sum = 0;
    for (const c of s) sum += Number(c);
    return sum;
}""",
        "starter_code_java": "class Solution {\n    public int power_base_sum(int base, int power) {\n        return 0;\n    }\n}",
        "reference_solution_java": """import java.math.BigInteger;
class Solution {
    public int power_base_sum(int base, int power) {
        BigInteger bi = BigInteger.valueOf(base).pow(power);
        String s = bi.toString();
        int sum = 0;
        for (int i = 0; i < s.length(); i++) {
            sum += s.charAt(i) - '0';
        }
        return sum;
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    int power_base_sum(int base, int power);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    int power_base_sum(int base, int power) {
        std::vector<int> digits = {1};
        for (int p = 0; p < power; p++) {
            int carry = 0;
            for (size_t i = 0; i < digits.size(); i++) {
                int prod = digits[i] * base + carry;
                digits[i] = prod % 10;
                carry = prod / 10;
            }
            while (carry > 0) {
                digits.push_back(carry % 10);
                carry /= 10;
            }
        }
        int sum = 0;
        for (int d : digits) sum += d;
        return sum;
    }
};"""
    },

    673: {
        "starter_code_javascript": "function extract_quotation(text1) {\n    return [];\n}",
        "reference_solution_javascript": """function extract_quotation(text1) {
    const res = [];
    const regex = /"([^"]*)"/g;
    let m;
    while ((m = regex.exec(text1)) !== null) {
        res.push(m[1]);
    }
    return res;
}""",
        "starter_code_java": "class Solution {\n    public String[] extract_quotation(String text1) {\n        return new String[0];\n    }\n}",
        "reference_solution_java": """import java.util.*;
import java.util.regex.*;
class Solution {
    public String[] extract_quotation(String text1) {
        List<String> res = new ArrayList<>();
        Pattern p = Pattern.compile("\\\"([^\\\"]*)\\\"");
        Matcher m = p.matcher(text1);
        while (m.find()) {
            res.add(m.group(1));
        }
        return res.toArray(new String[0]);
    }
}""",
        "starter_code_cpp": "#include <vector>\n#include <string>\nclass Solution {\npublic:\n    std::vector<std::string> extract_quotation(const std::string& text1);\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
class Solution {
public:
    std::vector<std::string> extract_quotation(const std::string& text1) {
        std::vector<std::string> res;
        size_t i = 0;
        while (i < text1.size()) {
            size_t start = text1.find('"', i);
            if (start == std::string::npos) break;
            size_t end = text1.find('"', start + 1);
            if (end == std::string::npos) break;
            res.push_back(text1.substr(start + 1, end - start - 1));
            i = end + 1;
        }
        return res;
    }
};"""
    },

    674: {
        "starter_code_javascript": "function remove_char(S) {\n    return '';\n}",
        "reference_solution_javascript": """function remove_char(S) {
    return S.replace(/[^a-zA-Z0-9]/g, '');
}""",
        "starter_code_java": "class Solution {\n    public String remove_char(String S) {\n        return "";\n    }\n}",
        "reference_solution_java": """class Solution {
    public String remove_char(String S) {
        return S.replaceAll("[^a-zA-Z0-9]", "");
    }
}""",
        "starter_code_cpp": "#include <string>\nclass Solution {\npublic:\n    std::string remove_char(const std::string& S);\n};",
        "reference_solution_cpp": """#include <string>
#include <cctype>
class Solution {
public:
    std::string remove_char(const std::string& S) {
        std::string res;
        for (char c : S) {
            if (isalnum((unsigned char)c)) res += c;
        }
        return res;
    }
};"""
    },

    675: {
        "starter_code_javascript": "function sum_list(lst1, lst2) {\n    return [];\n}",
        "reference_solution_javascript": """function sum_list(lst1, lst2) {
    return lst1.map((x, i) => x + lst2[i]);
}""",
        "starter_code_java": "class Solution {\n    public int[] sum_list(int[] lst1, int[] lst2) {\n        return new int[0];\n    }\n}",
        "reference_solution_java": """class Solution {
    public int[] sum_list(int[] lst1, int[] lst2) {
        int[] res = new int[lst1.length];
        for (int i = 0; i < lst1.length; i++) res[i] = lst1[i] + lst2[i];
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    std::vector<int> sum_list(const std::vector<int>& lst1, const std::vector<int>& lst2);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    std::vector<int> sum_list(const std::vector<int>& lst1, const std::vector<int>& lst2) {
        std::vector<int> res(lst1.size());
        for (size_t i = 0; i < lst1.size(); i++) res[i] = lst1[i] + lst2[i];
        return res;
    }
};"""
    },

    676: {
        "starter_code_javascript": "function add_list(nums1, nums2) {\n    return [];\n}",
        "reference_solution_javascript": """function add_list(nums1, nums2) {
    return nums1.map((x, i) => x + nums2[i]);
}""",
        "starter_code_java": "class Solution {\n    public int[] add_list(int[] nums1, int[] nums2) {\n        return new int[0];\n    }\n}",
        "reference_solution_java": """class Solution {
    public int[] add_list(int[] nums1, int[] nums2) {
        int[] res = new int[nums1.length];
        for (int i = 0; i < nums1.length; i++) res[i] = nums1[i] + nums2[i];
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    std::vector<int> add_list(const std::vector<int>& nums1, const std::vector<int>& nums2);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    std::vector<int> add_list(const std::vector<int>& nums1, const std::vector<int>& nums2) {
        std::vector<int> res(nums1.size());
        for (size_t i = 0; i < nums1.size(); i++) res[i] = nums1[i] + nums2[i];
        return res;
    }
};"""
    },

    677: {
        "starter_code_javascript": "function consecutive_duplicates(nums) {\n    return [];\n}",
        "reference_solution_javascript": """function consecutive_duplicates(nums) {
    return nums.filter((x, i) => i === 0 || x !== nums[i - 1]);
}""",
        "starter_code_java": "class Solution {\n    public int[] consecutive_duplicates(int[] nums) {\n        return new int[0];\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[] consecutive_duplicates(int[] nums) {
        if (nums.length == 0) return new int[0];
        List<Integer> list = new ArrayList<>();
        list.add(nums[0]);
        for (int i = 1; i < nums.length; i++) {
            if (nums[i] != nums[i - 1]) list.add(nums[i]);
        }
        int[] res = new int[list.size()];
        for (int i = 0; i < res.length; i++) res[i] = list.get(i);
        return res;
    }
    public String[] consecutive_duplicates(String[] nums) {
        if (nums.length == 0) return new String[0];
        List<String> list = new ArrayList<>();
        list.add(nums[0]);
        for (int i = 1; i < nums.length; i++) {
            if (!nums[i].equals(nums[i - 1])) list.add(nums[i]);
        }
        return list.toArray(new String[0]);
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    std::vector<int> consecutive_duplicates(const std::vector<int>& nums);\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
class Solution {
public:
    std::vector<int> consecutive_duplicates(const std::vector<int>& nums) {
        std::vector<int> res;
        for (size_t i = 0; i < nums.size(); i++) {
            if (i == 0 || nums[i] != nums[i - 1]) res.push_back(nums[i]);
        }
        return res;
    }
    std::vector<std::string> consecutive_duplicates(const std::vector<std::string>& nums) {
        std::vector<std::string> res;
        for (size_t i = 0; i < nums.size(); i++) {
            if (i == 0 || nums[i] != nums[i - 1]) res.push_back(nums[i]);
        }
        return res;
    }
};"""
    },

    678: {
        "starter_code_javascript": "function lateralsurface_cone(r, h) {\n    return 0.0;\n}",
        "reference_solution_javascript": """function lateralsurface_cone(r, h) {
    const l = Math.sqrt(r * r + h * h);
    return Math.PI * r * l;
}""",
        "starter_code_java": "class Solution {\n    public double lateralsurface_cone(int r, int h) {\n        return 0.0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public double lateralsurface_cone(int r, int h) {
        double l = Math.sqrt((double) r * r + (double) h * h);
        return Math.PI * r * l;
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    double lateralsurface_cone(double r, double h);\n};",
        "reference_solution_cpp": """#include <cmath>
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif
class Solution {
public:
    double lateralsurface_cone(double r, double h) {
        double l = std::sqrt(r * r + h * h);
        return M_PI * r * l;
    }
};"""
    },

    679: {
        "starter_code_javascript": "function replace_specialchar(text) {\n    return '';\n}",
        "reference_solution_javascript": """function replace_specialchar(text) {
    return text.replace(/[ ,.]/g, ':');
}""",
        "starter_code_java": "class Solution {\n    public String replace_specialchar(String text) {\n        return "";\n    }\n}",
        "reference_solution_java": """class Solution {
    public String replace_specialchar(String text) {
        return text.replaceAll("[ ,.]", ":");
    }
}""",
        "starter_code_cpp": "#include <string>\nclass Solution {\npublic:\n    std::string replace_specialchar(std::string text);\n};",
        "reference_solution_cpp": """#include <string>
class Solution {
public:
    std::string replace_specialchar(std::string text) {
        for (char& c : text) {
            if (c == ' ' || c == ',' || c == '.') c = ':';
        }
        return text;
    }
};"""
    },

    680: {
        "starter_code_javascript": "function find_first_occurrence(A, x) {\n    return 0;\n}",
        "reference_solution_javascript": """function find_first_occurrence(A, x) {
    let left = 0, right = A.length - 1;
    let result = -1;
    while (left <= right) {
        const mid = Math.floor((left + right) / 2);
        if (x === A[mid]) {
            result = mid;
            right = mid - 1;
        } else if (x < A[mid]) {
            right = mid - 1;
        } else {
            left = mid + 1;
        }
    }
    return result;
}""",
        "starter_code_java": "class Solution {\n    public int find_first_occurrence(int[] A, int x) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int find_first_occurrence(int[] A, int x) {
        int left = 0, right = A.length - 1;
        int result = -1;
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (x == A[mid]) {
                result = mid;
                right = mid - 1;
            } else if (x < A[mid]) {
                right = mid - 1;
            } else {
                left = mid + 1;
            }
        }
        return result;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    int find_first_occurrence(const std::vector<int>& A, int x);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    int find_first_occurrence(const std::vector<int>& A, int x) {
        int left = 0, right = (int)A.size() - 1;
        int result = -1;
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (x == A[mid]) {
                result = mid;
                right = mid - 1;
            } else if (x < A[mid]) {
                right = mid - 1;
            } else {
                left = mid + 1;
            }
        }
        return result;
    }
};"""
    },

    681: {
        "starter_code_javascript": "function sum_Of_Subarray_Prod(arr, n) {\n    return 0;\n}",
        "reference_solution_javascript": """function sum_Of_Subarray_Prod(arr, n) {
    let ans = 0;
    let res = 0;
    let i = n - 1;
    while (i >= 0) {
        const incr = arr[i] * (1 + res);
        ans += incr;
        res = incr;
        i--;
    }
    return ans;
}""",
        "starter_code_java": "class Solution {\n    public int sum_Of_Subarray_Prod(int[] arr, int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int sum_Of_Subarray_Prod(int[] arr, int n) {
        int ans = 0;
        int res = 0;
        int i = n - 1;
        while (i >= 0) {
            int incr = arr[i] * (1 + res);
            ans += incr;
            res = incr;
            i--;
        }
        return ans;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    int sum_Of_Subarray_Prod(const std::vector<int>& arr, int n);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    int sum_Of_Subarray_Prod(const std::vector<int>& arr, int n) {
        int ans = 0;
        int res = 0;
        int i = n - 1;
        while (i >= 0) {
            int incr = arr[i] * (1 + res);
            ans += incr;
            res = incr;
            i--;
        }
        return ans;
    }
};"""
    },

    682: {
        "starter_code_javascript": "function toggle_middle_bits(n) {\n    return 0;\n}",
        "reference_solution_javascript": """function toggle_middle_bits(n) {
    if (n === 1) return 1;
    let temp = n;
    temp |= temp >> 1;
    temp |= temp >> 2;
    temp |= temp >> 4;
    temp |= temp >> 8;
    temp |= temp >> 16;
    const middle = (temp >> 1) ^ 1;
    return n ^ middle;
}""",
        "starter_code_java": "class Solution {\n    public int toggle_middle_bits(int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int toggle_middle_bits(int n) {
        if (n == 1) return 1;
        int temp = n;
        temp |= temp >> 1;
        temp |= temp >> 2;
        temp |= temp >> 4;
        temp |= temp >> 8;
        temp |= temp >> 16;
        int middle = (temp >> 1) ^ 1;
        return n ^ middle;
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    int toggle_middle_bits(int n);\n};",
        "reference_solution_cpp": """class Solution {
public:
    int toggle_middle_bits(int n) {
        if (n == 1) return 1;
        int temp = n;
        temp |= temp >> 1;
        temp |= temp >> 2;
        temp |= temp >> 4;
        temp |= temp >> 8;
        temp |= temp >> 16;
        int middle = (temp >> 1) ^ 1;
        return n ^ middle;
    }
};"""
    },

    683: {
        "starter_code_javascript": "function left_insertion(a, x) {\n    return 0;\n}",
        "reference_solution_javascript": """function left_insertion(a, x) {
    let low = 0, high = a.length;
    while (low < high) {
        const mid = Math.floor((low + high) / 2);
        if (a[mid] < x) low = mid + 1;
        else high = mid;
    }
    return low;
}""",
        "starter_code_java": "class Solution {\n    public int left_insertion(int[] a, int x) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int left_insertion(int[] a, int x) {
        int low = 0, high = a.length;
        while (low < high) {
            int mid = low + (high - low) / 2;
            if (a[mid] < x) low = mid + 1;
            else high = mid;
        }
        return low;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    int left_insertion(const std::vector<int>& a, int x);\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
class Solution {
public:
    int left_insertion(const std::vector<int>& a, int x) {
        auto it = std::lower_bound(a.begin(), a.end(), x);
        return (int)(it - a.begin());
    }
};"""
    },

    684: {
        "starter_code_javascript": "function check_str(string) {\n    return '';\n}",
        "reference_solution_javascript": """function check_str(string) {
    return /^[aeiouAEIOU]/.test(string) ? 'Valid' : 'Invalid';
}""",
        "starter_code_java": "class Solution {\n    public String check_str(String string) {\n        return "";\n    }\n}",
        "reference_solution_java": """class Solution {
    public String check_str(String string) {
        if (string == null || string.isEmpty()) return "Invalid";
        char c = Character.toLowerCase(string.charAt(0));
        if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u') return "Valid";
        return "Invalid";
    }
}""",
        "starter_code_cpp": "#include <string>\nclass Solution {\npublic:\n    std::string check_str(const std::string& string);\n};",
        "reference_solution_cpp": """#include <string>
#include <cctype>
class Solution {
public:
    std::string check_str(const std::string& string) {
        if (string.empty()) return "Invalid";
        char c = tolower((unsigned char)string[0]);
        if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u') return "Valid";
        return "Invalid";
    }
};"""
    },

    685: {
        "starter_code_javascript": "function geometric_sum(n) {\n    return 0.0;\n}",
        "reference_solution_javascript": """function geometric_sum(n) {
    let sum = 0;
    for (let i = 0; i <= n; i++) sum += 1 / (2 ** i);
    return sum;
}""",
        "starter_code_java": "class Solution {\n    public double geometric_sum(int n) {\n        return 0.0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public double geometric_sum(int n) {
        double sum = 0.0;
        for (int i = 0; i <= n; i++) sum += 1.0 / Math.pow(2.0, i);
        return sum;
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    double geometric_sum(int n);\n};",
        "reference_solution_cpp": """#include <cmath>
class Solution {
public:
    double geometric_sum(int n) {
        double sum = 0.0;
        for (int i = 0; i <= n; i++) sum += 1.0 / std::pow(2.0, i);
        return sum;
    }
};"""
    },

    686: {
        "starter_code_javascript": "function find_Index(n) {\n    return 0;\n}",
        "reference_solution_javascript": """function find_Index(n) {
    return Math.round(Math.sqrt(2 * Math.pow(10, n - 1)));
}""",
        "starter_code_java": "class Solution {\n    public int find_Index(int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int find_Index(int n) {
        return (int) Math.round(Math.sqrt(2.0 * Math.pow(10.0, n - 1)));
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    int find_Index(int n);\n};",
        "reference_solution_cpp": """#include <cmath>
class Solution {
public:
    int find_Index(int n) {
        return (int)std::round(std::sqrt(2.0 * std::pow(10.0, n - 1)));
    }
};"""
    },

    687: {
        "starter_code_javascript": "function all_Characters_Same(s) {\n    return false;\n}",
        "reference_solution_javascript": """function all_Characters_Same(s) {
    for (let i = 1; i < s.length; i++) {
        if (s[i] !== s[0]) return false;
    }
    return true;
}""",
        "starter_code_java": "class Solution {\n    public boolean all_Characters_Same(String s) {\n        return false;\n    }\n}",
        "reference_solution_java": """class Solution {
    public boolean all_Characters_Same(String s) {
        for (int i = 1; i < s.length(); i++) {
            if (s.charAt(i) != s.charAt(0)) return false;
        }
        return true;
    }
}""",
        "starter_code_cpp": "#include <string>\nclass Solution {\npublic:\n    bool all_Characters_Same(const std::string& s);\n};",
        "reference_solution_cpp": """#include <string>
class Solution {
public:
    bool all_Characters_Same(const std::string& s) {
        for (size_t i = 1; i < s.size(); i++) {
            if (s[i] != s[0]) return false;
        }
        return true;
    }
};"""
    },

    688: {
        "starter_code_javascript": "function area_tetrahedron(side) {\n    return 0.0;\n}",
        "reference_solution_javascript": """function area_tetrahedron(side) {
    return Math.sqrt(3) * side * side;
}""",
        "starter_code_java": "class Solution {\n    public double area_tetrahedron(int side) {\n        return 0.0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public double area_tetrahedron(int side) {
        return Math.sqrt(3.0) * (double) side * side;
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    double area_tetrahedron(double side);\n};",
        "reference_solution_cpp": """#include <cmath>
class Solution {
public:
    double area_tetrahedron(double side) {
        return std::sqrt(3.0) * side * side;
    }
};"""
    },

    689: {
        "starter_code_javascript": "function rotate_right(list1, m, n) {\n    return [];\n}",
        "reference_solution_javascript": """function rotate_right(list1, m, n) {
    const part1 = list1.slice(-m);
    const part2 = list1.slice(0, list1.length - n);
    return part1.concat(part2);
}""",
        "starter_code_java": "class Solution {\n    public int[] rotate_right(int[] list1, int m, int n) {\n        return new int[0];\n    }\n}",
        "reference_solution_java": """class Solution {
    public int[] rotate_right(int[] list1, int m, int n) {
        int len1 = m;
        int len2 = list1.length - n;
        int[] res = new int[len1 + len2];
        System.arraycopy(list1, list1.length - m, res, 0, len1);
        System.arraycopy(list1, 0, res, len1, len2);
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    std::vector<int> rotate_right(const std::vector<int>& list1, int m, int n);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    std::vector<int> rotate_right(const std::vector<int>& list1, int m, int n) {
        std::vector<int> res;
        res.insert(res.end(), list1.end() - m, list1.end());
        res.insert(res.end(), list1.begin(), list1.end() - n);
        return res;
    }
};"""
    },

    690: {
        "starter_code_javascript": "function check_none(test_tup) {\n    return false;\n}",
        "reference_solution_javascript": """function check_none(test_tup) {
    return test_tup.some(x => x === null || x === undefined);
}""",
        "starter_code_java": "class Solution {\n    public boolean check_none(int[] test_tup) {\n        return false;\n    }\n}",
        "reference_solution_java": """class Solution {
    public boolean check_none(Integer[] test_tup) {
        for (Integer x : test_tup) if (x == null) return true;
        return false;
    }
    public boolean check_none(int[] test_tup) {
        return false;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    bool check_none(const std::vector<int>& test_tup);\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
class Solution {
public:
    bool check_none(const std::vector<std::string>& test_tup) {
        for (const auto& s : test_tup) if (s == "null") return true;
        return false;
    }
    bool check_none(const std::vector<int>& test_tup) {
        return false;
    }
};"""
    },

    691: {
        "starter_code_javascript": "function divisible_by_digits(startnum, endnum) {\n    return [];\n}",
        "reference_solution_javascript": """function divisible_by_digits(startnum, endnum) {
    const res = [];
    for (let n = startnum; n <= endnum; n++) {
        const s = String(n);
        let ok = true;
        for (const c of s) {
            const d = Number(c);
            if (d === 0 || n % d !== 0) {
                ok = false;
                break;
            }
        }
        if (ok) res.push(n);
    }
    return res;
}""",
        "starter_code_java": "class Solution {\n    public int[] divisible_by_digits(int startnum, int endnum) {\n        return new int[0];\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[] divisible_by_digits(int startnum, int endnum) {
        List<Integer> list = new ArrayList<>();
        for (int n = startnum; n <= endnum; n++) {
            int temp = n;
            boolean ok = true;
            while (temp > 0) {
                int d = temp % 10;
                if (d == 0 || n % d != 0) {
                    ok = false;
                    break;
                }
                temp /= 10;
            }
            if (ok) list.add(n);
        }
        int[] res = new int[list.size()];
        for (int i = 0; i < res.length; i++) res[i] = list.get(i);
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    std::vector<int> divisible_by_digits(int startnum, int endnum);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    std::vector<int> divisible_by_digits(int startnum, int endnum) {
        std::vector<int> res;
        for (int n = startnum; n <= endnum; n++) {
            int temp = n;
            bool ok = true;
            while (temp > 0) {
                int d = temp % 10;
                if (d == 0 || n % d != 0) {
                    ok = false;
                    break;
                }
                temp /= 10;
            }
            if (ok) res.push_back(n);
        }
        return res;
    }
};"""
    },

    692: {
        "starter_code_javascript": "function sector_area(r, a) {\n    return 0.0;\n}",
        "reference_solution_javascript": """function sector_area(r, a) {
    if (a >= 360) return null;
    const pi = 22 / 7;
    return (pi * r * r) * (a / 360);
}""",
        "starter_code_java": "class Solution {\n    public Object sector_area(int r, int a) {\n        return null;\n    }\n}",
        "reference_solution_java": """class Solution {
    public Object sector_area(int r, int a) {
        if (a >= 360) return null;
        double pi = 22.0 / 7.0;
        return (pi * r * r) * ((double) a / 360.0);
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    double sector_area(double r, double a);\n};",
        "reference_solution_cpp": """class Solution {
public:
    double sector_area(double r, double a) {
        if (a >= 360) return 0.0;
        double pi = 22.0 / 7.0;
        return (pi * r * r) * (a / 360.0);
    }
};"""
    },

    693: {
        "starter_code_javascript": "function lcs_of_three(X, Y, Z, m, n, o) {\n    return 0;\n}",
        "reference_solution_javascript": """function lcs_of_three(X, Y, Z, m, n, o) {
    const L = Array.from({length: m + 1}, () =>
        Array.from({length: n + 1}, () => new Array(o + 1).fill(0))
    );
    for (let i = 0; i <= m; i++) {
        for (let j = 0; j <= n; j++) {
            for (let k = 0; k <= o; k++) {
                if (i === 0 || j === 0 || k === 0) {
                    L[i][j][k] = 0;
                } else if (X[i - 1] === Y[j - 1] && X[i - 1] === Z[k - 1]) {
                    L[i][j][k] = L[i - 1][j - 1][k - 1] + 1;
                } else {
                    L[i][j][k] = Math.max(L[i - 1][j][k], L[i][j - 1][k], L[i][j][k - 1]);
                }
            }
        }
    }
    return L[m][n][o];
}""",
        "starter_code_java": "class Solution {\n    public int lcs_of_three(String X, String Y, String Z, int m, int n, int o) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int lcs_of_three(String X, String Y, String Z, int m, int n, int o) {
        int[][][] L = new int[m + 1][n + 1][o + 1];
        for (int i = 0; i <= m; i++) {
            for (int j = 0; j <= n; j++) {
                for (int k = 0; k <= o; k++) {
                    if (i == 0 || j == 0 || k == 0) {
                        L[i][j][k] = 0;
                    } else if (X.charAt(i - 1) == Y.charAt(j - 1) && X.charAt(i - 1) == Z.charAt(k - 1)) {
                        L[i][j][k] = L[i - 1][j - 1][k - 1] + 1;
                    } else {
                        L[i][j][k] = Math.max(L[i - 1][j][k], Math.max(L[i][j - 1][k], L[i][j][k - 1]));
                    }
                }
            }
        }
        return L[m][n][o];
    }
}""",
        "starter_code_cpp": "#include <string>\nclass Solution {\npublic:\n    int lcs_of_three(const std::string& X, const std::string& Y, const std::string& Z, int m, int n, int o);\n};",
        "reference_solution_cpp": """#include <string>
#include <vector>
#include <algorithm>
class Solution {
public:
    int lcs_of_three(const std::string& X, const std::string& Y, const std::string& Z, int m, int n, int o) {
        std::vector<std::vector<std::vector<int>>> L(m + 1, std::vector<std::vector<int>>(n + 1, std::vector<int>(o + 1, 0)));
        for (int i = 0; i <= m; i++) {
            for (int j = 0; j <= n; j++) {
                for (int k = 0; k <= o; k++) {
                    if (i == 0 || j == 0 || k == 0) {
                        L[i][j][k] = 0;
                    } else if (X[i - 1] == Y[j - 1] && X[i - 1] == Z[k - 1]) {
                        L[i][j][k] = L[i - 1][j - 1][k - 1] + 1;
                    } else {
                        L[i][j][k] = std::max({L[i - 1][j][k], L[i][j - 1][k], L[i][j][k - 1]});
                    }
                }
            }
        }
        return L[m][n][o];
    }
};"""
    },

    694: {
        "starter_code_javascript": "function capital_words_spaces(str1) {\n    return '';\n}",
        "reference_solution_javascript": """function capital_words_spaces(str1) {
    return str1.replace(/(\\w)([A-Z])/g, '$1 $2');
}""",
        "starter_code_java": "class Solution {\n    public String capital_words_spaces(String str1) {\n        return \"\";\n    }\n}",
        "reference_solution_java": """class Solution {
    public String capital_words_spaces(String str1) {
        return str1.replaceAll("(\\\\w)([A-Z])", "$1 $2");
    }
}""",
        "starter_code_cpp": "#include <string>\nclass Solution {\npublic:\n    std::string capital_words_spaces(const std::string& str1);\n};",
        "reference_solution_cpp": """#include <string>
#include <cctype>
class Solution {
public:
    std::string capital_words_spaces(const std::string& str1) {
        std::string res;
        for (size_t i = 0; i < str1.size(); i++) {
            if (i > 0 && isupper((unsigned char)str1[i]) && (isalnum((unsigned char)str1[i - 1]) || str1[i - 1] == '_')) {
                res += ' ';
            }
            res += str1[i];
        }
        return res;
    }
};"""
    },

    695: {
        "starter_code_javascript": "function sort_numeric_strings(nums_str) {\n    return [];\n}",
        "reference_solution_javascript": """function sort_numeric_strings(nums_str) {
    const res = nums_str.map(x => parseInt(x.trim(), 10));
    res.sort((a, b) => a - b);
    return res;
}""",
        "starter_code_java": "class Solution {\n    public int[] sort_numeric_strings(String[] nums_str) {\n        return new int[0];\n    }\n}",
        "reference_solution_java": """import java.util.Arrays;
class Solution {
    public int[] sort_numeric_strings(String[] nums_str) {
        int[] res = new int[nums_str.length];
        for (int i = 0; i < nums_str.length; i++) {
            res[i] = Integer.parseInt(nums_str[i].trim());
        }
        Arrays.sort(res);
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\n#include <string>\nclass Solution {\npublic:\n    std::vector<int> sort_numeric_strings(const std::vector<std::string>& nums_str);\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <algorithm>
class Solution {
public:
    std::vector<int> sort_numeric_strings(const std::vector<std::string>& nums_str) {
        std::vector<int> res;
        for (const auto& s : nums_str) {
            res.push_back(std::stoi(s));
        }
        std::sort(res.begin(), res.end());
        return res;
    }
};"""
    },

    696: {
        "starter_code_javascript": "function add_tuple(test_list, test_tup) {\n    return [];\n}",
        "reference_solution_javascript": """function add_tuple(test_list, test_tup) {
    return test_list.concat(test_tup);
}""",
        "starter_code_java": "class Solution {\n    public int[] add_tuple(int[] test_list, int[] test_tup) {\n        return new int[0];\n    }\n}",
        "reference_solution_java": """class Solution {
    public int[] add_tuple(int[] test_list, int[] test_tup) {
        int[] res = new int[test_list.length + test_tup.length];
        System.arraycopy(test_list, 0, res, 0, test_list.length);
        System.arraycopy(test_tup, 0, res, test_list.length, test_tup.length);
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    std::vector<int> add_tuple(std::vector<int> test_list, const std::vector<int>& test_tup);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    std::vector<int> add_tuple(std::vector<int> test_list, const std::vector<int>& test_tup) {
        test_list.insert(test_list.end(), test_tup.begin(), test_tup.end());
        return test_list;
    }
};"""
    },

    697: {
        "starter_code_javascript": "function check_min_heap(arr, i) {\n    return false;\n}",
        "reference_solution_javascript": """function check_min_heap(arr, i) {
    if (2 * i + 2 > arr.length) return true;
    const left_child = (arr[i] <= arr[2 * i + 1]) && check_min_heap(arr, 2 * i + 1);
    const right_child = (2 * i + 2 === arr.length) || ((arr[i] <= arr[2 * i + 2]) && check_min_heap(arr, 2 * i + 2));
    return left_child && right_child;
}""",
        "starter_code_java": "class Solution {\n    public boolean check_min_heap(int[] arr, int i) {\n        return false;\n    }\n}",
        "reference_solution_java": """class Solution {
    public boolean check_min_heap(int[] arr, int i) {
        if (2 * i + 2 > arr.length) return true;
        boolean left_child = (arr[i] <= arr[2 * i + 1]) && check_min_heap(arr, 2 * i + 1);
        boolean right_child = (2 * i + 2 == arr.length) || ((arr[i] <= arr[2 * i + 2]) && check_min_heap(arr, 2 * i + 2));
        return left_child && right_child;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    bool check_min_heap(const std::vector<int>& arr, int i);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    bool check_min_heap(const std::vector<int>& arr, int i) {
        if (2 * i + 2 > (int)arr.size()) return true;
        bool left_child = (arr[i] <= arr[2 * i + 1]) && check_min_heap(arr, 2 * i + 1);
        bool right_child = (2 * i + 2 == (int)arr.size()) || ((arr[i] <= arr[2 * i + 2]) && check_min_heap(arr, 2 * i + 2));
        return left_child && right_child;
    }
};"""
    },

    698: {
        "starter_code_javascript": "function jacobsthal_num(n) {\n    return 0;\n}",
        "reference_solution_javascript": """function jacobsthal_num(n) {
    const dp = new Array(n + 1).fill(0);
    dp[0] = 0;
    dp[1] = 1;
    for (let i = 2; i <= n; i++) dp[i] = dp[i - 1] + 2 * dp[i - 2];
    return dp[n];
}""",
        "starter_code_java": "class Solution {\n    public int jacobsthal_num(int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int jacobsthal_num(int n) {
        int[] dp = new int[n + 1];
        dp[0] = 0;
        dp[1] = 1;
        for (int i = 2; i <= n; i++) dp[i] = dp[i - 1] + 2 * dp[i - 2];
        return dp[n];
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    int jacobsthal_num(int n);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    int jacobsthal_num(int n) {
        std::vector<int> dp(n + 1, 0);
        dp[0] = 0;
        dp[1] = 1;
        for (int i = 2; i <= n; i++) dp[i] = dp[i - 1] + 2 * dp[i - 2];
        return dp[n];
    }
};"""
    },

    699: {
        "starter_code_javascript": "function min_k(test_list, K) {\n    return [];\n}",
        "reference_solution_javascript": """function min_k(test_list, K) {
    const sorted = [...test_list].sort((a, b) => a[1] - b[1]);
    return sorted.slice(0, K);
}""",
        "starter_code_java": "class Solution {\n    public Object[][] min_k(Object[][] test_list, int K) {\n        return new Object[0][0];\n    }\n}",
        "reference_solution_java": """import java.util.Arrays;
class Solution {
    public Object[][] min_k(Object[][] test_list, int K) {
        Object[][] copy = Arrays.copyOf(test_list, test_list.length);
        Arrays.sort(copy, (a, b) -> Integer.compare(((Number) a[1]).intValue(), ((Number) b[1]).intValue()));
        return Arrays.copyOfRange(copy, 0, K);
    }
}""",
        "starter_code_cpp": "#include <vector>\n#include <string>\nclass Solution {\npublic:\n    std::vector<std::vector<std::string>> min_k(std::vector<std::vector<std::string>> test_list, int K);\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <algorithm>
class Solution {
public:
    std::vector<std::vector<std::string>> min_k(std::vector<std::vector<std::string>> test_list, int K) {
        std::sort(test_list.begin(), test_list.end(), [](const std::vector<std::string>& a, const std::vector<std::string>& b) {
            return std::stoi(a[1]) < std::stoi(b[1]);
        });
        if ((size_t)K < test_list.size()) test_list.resize(K);
        return test_list;
    }
};"""
    },

    700: {
        "starter_code_javascript": "function extract_index_list(l1, l2, l3) {\n    return [];\n}",
        "reference_solution_javascript": """function extract_index_list(l1, l2, l3) {
    const res = [];
    const n = Math.min(l1.length, l2.length, l3.length);
    for (let i = 0; i < n; i++) {
        if (l1[i] === l2[i] && l2[i] === l3[i]) res.push(l1[i]);
    }
    return res;
}""",
        "starter_code_java": "class Solution {\n    public int[] extract_index_list(int[] l1, int[] l2, int[] l3) {\n        return new int[0];\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[] extract_index_list(int[] l1, int[] l2, int[] l3) {
        List<Integer> list = new ArrayList<>();
        int n = Math.min(l1.length, Math.min(l2.length, l3.length));
        for (int i = 0; i < n; i++) {
            if (l1[i] == l2[i] && l2[i] == l3[i]) list.add(l1[i]);
        }
        int[] res = new int[list.size()];
        for (int i = 0; i < res.length; i++) res[i] = list.get(i);
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    std::vector<int> extract_index_list(const std::vector<int>& l1, const std::vector<int>& l2, const std::vector<int>& l3);\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
class Solution {
public:
    std::vector<int> extract_index_list(const std::vector<int>& l1, const std::vector<int>& l2, const std::vector<int>& l3) {
        std::vector<int> res;
        size_t n = std::min({l1.size(), l2.size(), l3.size()});
        for (size_t i = 0; i < n; i++) {
            if (l1[i] == l2[i] && l2[i] == l3[i]) res.push_back(l1[i]);
        }
        return res;
    }
};"""
    },

    701: {
        "starter_code_javascript": "function second_smallest(numbers) {\n    return null;\n}",
        "reference_solution_javascript": """function second_smallest(numbers) {
    if (numbers.length < 2) return null;
    if (numbers.length === 2 && numbers[0] === numbers[1]) return null;
    const uniq = Array.from(new Set(numbers)).sort((a, b) => a - b);
    if (uniq.length < 2) return null;
    return uniq[1];
}""",
        "starter_code_java": "class Solution {\n    public Object second_smallest(int[] numbers) {\n        return null;\n    }\n}",
        "reference_solution_java": """import java.util.*;
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
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    double second_smallest(const std::vector<int>& numbers);\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <set>
class Solution {
public:
    double second_smallest(const std::vector<int>& numbers) {
        if (numbers.size() < 2) return 0;
        std::set<int> uniq(numbers.begin(), numbers.end());
        if (uniq.size() < 2) return 0;
        auto it = uniq.begin();
        ++it;
        return *it;
    }
    double second_smallest(const std::vector<std::string>& numbers) {
        if (numbers.size() < 2) return 0;
        std::set<double> uniq;
        for (const auto& s : numbers) uniq.insert(std::stod(s));
        if (uniq.size() < 2) return 0;
        auto it = uniq.begin();
        ++it;
        return *it;
    }
};"""
    },

    702: {
        "starter_code_javascript": "function text_match_zero_one(text) {\n    return '';\n}",
        "reference_solution_javascript": """function text_match_zero_one(text) {
    return text.includes('a') ? 'Found a match!' : 'Not matched!';
}""",
        "starter_code_java": "class Solution {\n    public String text_match_zero_one(String text) {\n        return "";\n    }\n}",
        "reference_solution_java": """class Solution {
    public String text_match_zero_one(String text) {
        return text.contains("a") ? "Found a match!" : "Not matched!";
    }
}""",
        "starter_code_cpp": "#include <string>\nclass Solution {\npublic:\n    std::string text_match_zero_one(const std::string& text);\n};",
        "reference_solution_cpp": """#include <string>
class Solution {
public:
    std::string text_match_zero_one(const std::string& text) {
        return text.find('a') != std::string::npos ? "Found a match!" : "Not matched!";
    }
};"""
    },

    703: {
        "starter_code_javascript": "function count_reverse_pairs(test_list) {\n    return '';\n}",
        "reference_solution_javascript": """function count_reverse_pairs(test_list) {
    let count = 0;
    for (let i = 0; i < test_list.length; i++) {
        const rev = test_list[i].split('').reverse().join('');
        for (let j = i; j < test_list.length; j++) {
            if (test_list[j] === rev) count++;
        }
    }
    return String(count);
}""",
        "starter_code_java": "class Solution {\n    public String count_reverse_pairs(String[] test_list) {\n        return "";\n    }\n}",
        "reference_solution_java": """class Solution {
    public String count_reverse_pairs(String[] test_list) {
        int count = 0;
        for (int i = 0; i < test_list.length; i++) {
            String rev = new StringBuilder(test_list[i]).reverse().toString();
            for (int j = i; j < test_list.length; j++) {
                if (test_list[j].equals(rev)) count++;
            }
        }
        return String.valueOf(count);
    }
}""",
        "starter_code_cpp": "#include <vector>\n#include <string>\nclass Solution {\npublic:\n    std::string count_reverse_pairs(const std::vector<std::string>& test_list);\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <algorithm>
class Solution {
public:
    std::string count_reverse_pairs(const std::vector<std::string>& test_list) {
        int count = 0;
        for (size_t i = 0; i < test_list.size(); i++) {
            std::string rev = test_list[i];
            std::reverse(rev.begin(), rev.end());
            for (size_t j = i; j < test_list.size(); j++) {
                if (test_list[j] == rev) count++;
            }
        }
        return std::to_string(count);
    }
};"""
    },

    704: {
        "starter_code_javascript": "function is_decimal(num) {\n    return false;\n}",
        "reference_solution_javascript": """function is_decimal(num) {
    return /^[0-9]+(\\.[0-9]{1,2})?$/.test(num);
}""",
        "starter_code_java": "class Solution {\n    public boolean is_decimal(String num) {\n        return false;\n    }\n}",
        "reference_solution_java": """class Solution {
    public boolean is_decimal(String num) {
        return num.matches("^[0-9]+(\\\\.[0-9]{1,2})?$");
    }
}""",
        "starter_code_cpp": "#include <string>\nclass Solution {\npublic:\n    bool is_decimal(const std::string& num);\n};",
        "reference_solution_cpp": """#include <string>
#include <regex>
class Solution {
public:
    bool is_decimal(const std::string& num) {
        std::regex re("^[0-9]+(\\.[0-9]{1,2})?$");
        return std::regex_match(num, re);
    }
};"""
    },

    705: {
        "starter_code_javascript": "function unique_Element(arr, n) {\n    return '';\n}",
        "reference_solution_javascript": """function unique_Element(arr, n) {
    const s = new Set(arr);
    return s.size === 1 ? 'YES' : 'NO';
}""",
        "starter_code_java": "class Solution {\n    public String unique_Element(int[] arr, int n) {\n        return "";\n    }\n}",
        "reference_solution_java": """class Solution {
    public String unique_Element(int[] arr, int n) {
        for (int i = 1; i < n; i++) {
            if (arr[i] != arr[0]) return "NO";
        }
        return "YES";
    }
}""",
        "starter_code_cpp": "#include <vector>\n#include <string>\nclass Solution {\npublic:\n    std::string unique_Element(const std::vector<int>& arr, int n);\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
class Solution {
public:
    std::string unique_Element(const std::vector<int>& arr, int n) {
        for (int i = 1; i < n; i++) {
            if (arr[i] != arr[0]) return "NO";
        }
        return "YES";
    }
};"""
    },

    706: {
        "starter_code_javascript": "function arc_length(d, a) {\n    return 0.0;\n}",
        "reference_solution_javascript": """function arc_length(d, a) {
    if (a >= 360) return null;
    const pi = 22 / 7;
    return (pi * d) * (a / 360);
}""",
        "starter_code_java": "class Solution {\n    public Object arc_length(int d, int a) {\n        return null;\n    }\n}",
        "reference_solution_java": """class Solution {
    public Object arc_length(int d, int a) {
        if (a >= 360) return null;
        double pi = 22.0 / 7.0;
        return (pi * d) * ((double) a / 360.0);
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    double arc_length(double d, double a);\n};",
        "reference_solution_cpp": """class Solution {
public:
    double arc_length(double d, double a) {
        if (a >= 360) return 0.0;
        double pi = 22.0 / 7.0;
        return (pi * d) * (a / 360.0);
    }
};"""
    },

    707: {
        "starter_code_javascript": "function check_monthnumber_number(monthnum3) {\n    return false;\n}",
        "reference_solution_javascript": """function check_monthnumber_number(monthnum3) {
    return monthnum3 === 4 || monthnum3 === 6 || monthnum3 === 9 || monthnum3 === 11;
}""",
        "starter_code_java": "class Solution {\n    public boolean check_monthnumber_number(int monthnum3) {\n        return false;\n    }\n}",
        "reference_solution_java": """class Solution {
    public boolean check_monthnumber_number(int monthnum3) {
        return monthnum3 == 4 || monthnum3 == 6 || monthnum3 == 9 || monthnum3 == 11;
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    bool check_monthnumber_number(int monthnum3);\n};",
        "reference_solution_cpp": """class Solution {
public:
    bool check_monthnumber_number(int monthnum3) {
        return monthnum3 == 4 || monthnum3 == 6 || monthnum3 == 9 || monthnum3 == 11;
    }
};"""
    },

    708: {
        "starter_code_javascript": "function find_Min_Diff(arr, n) {\n    return 0;\n}",
        "reference_solution_javascript": """function find_Min_Diff(arr, n) {
    const sorted = [...arr].sort((a, b) => a - b);
    let diff = Infinity;
    for (let i = 0; i < n - 1; i++) {
        if (sorted[i + 1] - sorted[i] < diff) {
            diff = sorted[i + 1] - sorted[i];
        }
    }
    return diff;
}""",
        "starter_code_java": "class Solution {\n    public int find_Min_Diff(int[] arr, int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """import java.util.Arrays;
class Solution {
    public int find_Min_Diff(int[] arr, int n) {
        int[] copy = Arrays.copyOf(arr, arr.length);
        Arrays.sort(copy);
        int diff = Integer.MAX_VALUE;
        for (int i = 0; i < n - 1; i++) {
            if (copy[i + 1] - copy[i] < diff) {
                diff = copy[i + 1] - copy[i];
            }
        }
        return diff;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    int find_Min_Diff(std::vector<int> arr, int n);\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
class Solution {
public:
    int find_Min_Diff(std::vector<int> arr, int n) {
        std::sort(arr.begin(), arr.end());
        int diff = 2e9;
        for (int i = 0; i < n - 1; i++) {
            if (arr[i + 1] - arr[i] < diff) {
                diff = arr[i + 1] - arr[i];
            }
        }
        return diff;
    }
};"""
    },

    709: {
        "starter_code_javascript": "function number_ctr(str) {\n    return 0;\n}",
        "reference_solution_javascript": """function number_ctr(str) {
    let count = 0;
    for (let i = 0; i < str.length; i++) {
        if (str[i] >= '0' && str[i] <= '9') count++;
    }
    return count;
}""",
        "starter_code_java": "class Solution {\n    public int number_ctr(String str) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int number_ctr(String str) {
        int count = 0;
        for (int i = 0; i < str.length(); i++) {
            char c = str.charAt(i);
            if (c >= '0' && c <= '9') count++;
        }
        return count;
    }
}""",
        "starter_code_cpp": "#include <string>\nclass Solution {\npublic:\n    int number_ctr(const std::string& str);\n};",
        "reference_solution_cpp": """#include <string>
#include <cctype>
class Solution {
public:
    int number_ctr(const std::string& str) {
        int count = 0;
        for (char c : str) {
            if (isdigit((unsigned char)c)) count++;
        }
        return count;
    }
};"""
    },

    710: {
        "starter_code_javascript": "function is_polite(n) {\n    return 0;\n}",
        "reference_solution_javascript": """function is_polite(n) {
    n = n + 1;
    const log2_n = Math.log2(n);
    return Math.floor(n + Math.log2(n + log2_n));
}""",
        "starter_code_java": "class Solution {\n    public int is_polite(int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int is_polite(int n) {
        n = n + 1;
        double log2_n = Math.log(n) / Math.log(2.0);
        return (int) (n + (Math.log(n + log2_n) / Math.log(2.0)));
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    int is_polite(int n);\n};",
        "reference_solution_cpp": """#include <cmath>
class Solution {
public:
    int is_polite(int n) {
        n = n + 1;
        double log2_n = std::log2(n);
        return (int)(n + std::log2(n + log2_n));
    }
};"""
    }
}
