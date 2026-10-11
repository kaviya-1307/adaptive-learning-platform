"""
Script to create batch11_solutions.py containing curated solutions for Batch 11 (Problems 561-610).
"""

import os
import sys

# We will construct BATCH11_SOLUTIONS dictionary and write it to batch11_solutions.py
BATCH11_CODE = '''"""
Curated and specialized solutions for MBPP problems (Batch 11: 561-610).
"""

BATCH11_SOLUTIONS = {
    561: {
        "starter_code_javascript": "function is_Even(n) {\\n    return false;\\n}",
        "reference_solution_javascript": """function is_Even(n) {
    return (n ^ 1) === (n + 1);
}""",
        "starter_code_java": "class Solution {\\n    public boolean is_Even(int n) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public boolean is_Even(int n) {
        return (n ^ 1) == (n + 1);
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    bool is_Even(int n);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    bool is_Even(int n) {
        return (n ^ 1) == (n + 1);
    }
};"""
    },

    562: {
        "starter_code_javascript": "function first_repeated_char(str1) {\\n    return '';\\n}",
        "reference_solution_javascript": """function first_repeated_char(str1) {
    let seen = new Set();
    for (let c of str1) {
        if (seen.has(c)) return c;
        seen.add(c);
    }
    return "None";
}""",
        "starter_code_java": "class Solution {\\n    public String first_repeated_char(String str1) {\\n        return \\"\\";\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public String first_repeated_char(String str1) {
        Set<Character> seen = new HashSet<>();
        for (char c : str1.toCharArray()) {
            if (seen.contains(c)) return String.valueOf(c);
            seen.add(c);
        }
        return "None";
    }
}""",
        "starter_code_cpp": "#include <string>\\nclass Solution {\\npublic:\\n    std::string first_repeated_char(std::string str1);\\n};",
        "reference_solution_cpp": """#include <string>
#include <unordered_set>
class Solution {
public:
    std::string first_repeated_char(std::string str1) {
        std::unordered_set<char> seen;
        for (char c : str1) {
            if (seen.count(c)) return std::string(1, c);
            seen.insert(c);
        }
        return "None";
    }
};"""
    },

    563: {
        "starter_code_javascript": "function get_ludic(n) {\\n    return [];\\n}",
        "reference_solution_javascript": """function get_ludic(n) {
    let ludics = [];
    for (let i = 1; i <= n; i++) ludics.push(i);
    let index = 1;
    while (index < ludics.length) {
        let first_ludic = ludics[index];
        let remove_index = index + first_ludic;
        while (remove_index < ludics.length) {
            ludics.splice(remove_index, 1);
            remove_index += first_ludic - 1;
        }
        index++;
    }
    return ludics;
}""",
        "starter_code_java": "import java.util.*;\\nclass Solution {\\n    public List<Integer> get_ludic(int n) {\\n        return new ArrayList<>();\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public List<Integer> get_ludic(int n) {
        List<Integer> ludics = new ArrayList<>();
        for (int i = 1; i <= n; i++) ludics.add(i);
        int index = 1;
        while (index < ludics.size()) {
            int first_ludic = ludics.get(index);
            int remove_index = index + first_ludic;
            while (remove_index < ludics.size()) {
                ludics.remove(remove_index);
                remove_index += first_ludic - 1;
            }
            index++;
        }
        return ludics;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    std::vector<int> get_ludic(int n);\\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    std::vector<int> get_ludic(int n) {
        std::vector<int> ludics;
        for (int i = 1; i <= n; ++i) ludics.push_back(i);
        int index = 1;
        while (index < (int)ludics.size()) {
            int first_ludic = ludics[index];
            int remove_index = index + first_ludic;
            while (remove_index < (int)ludics.size()) {
                ludics.erase(ludics.begin() + remove_index);
                remove_index += first_ludic - 1;
            }
            index++;
        }
        return ludics;
    }
};"""
    },

    564: {
        "starter_code_javascript": "function reverse_words(s) {\\n    return '';\\n}",
        "reference_solution_javascript": """function reverse_words(s) {
    return s.trim().split(/\\\\s+/).reverse().join(" ");
}""",
        "starter_code_java": "class Solution {\\n    public String reverse_words(String s) {\\n        return \\"\\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String reverse_words(String s) {
        String[] parts = s.trim().split("\\\\s+");
        StringBuilder sb = new StringBuilder();
        for (int i = parts.length - 1; i >= 0; i--) {
            if (sb.length() > 0) sb.append(" ");
            sb.append(parts[i]);
        }
        return sb.toString();
    }
}""",
        "starter_code_cpp": "#include <string>\\nclass Solution {\\npublic:\\n    std::string reverse_words(std::string s);\\n};",
        "reference_solution_cpp": """#include <string>
#include <vector>
#include <sstream>
class Solution {
public:
    std::string reverse_words(std::string s) {
        std::stringstream ss(s);
        std::string word;
        std::vector<std::string> words;
        while (ss >> word) words.push_back(word);
        std::string res = "";
        for (int i = (int)words.size() - 1; i >= 0; --i) {
            if (!res.empty()) res += " ";
            res += words[i];
        }
        return res;
    }
};"""
    },

    565: {
        "starter_code_javascript": "function prime_num(num) {\\n    return false;\\n}",
        "reference_solution_javascript": """function prime_num(num) {
    if (num >= 1) {
        for (let i = 2; i < Math.floor(num / 2); i++) {
            if (num % i === 0) return false;
            else return true;
        }
        return num > 1;
    }
    return false;
}""",
        "starter_code_java": "class Solution {\\n    public boolean prime_num(int num) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public boolean prime_num(int num) {
        if (num >= 1) {
            for (int i = 2; i < num / 2; i++) {
                if (num % i == 0) return false;
                else return true;
            }
            return num > 1;
        }
        return false;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    bool prime_num(int num);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    bool prime_num(int num) {
        if (num >= 1) {
            for (int i = 2; i < num / 2; ++i) {
                if (num % i == 0) return false;
                else return true;
            }
            return num > 1;
        }
        return false;
    }
};"""
    },

    566: {
        "starter_code_javascript": "function radian_degree(degree) {\\n    return 0.0;\\n}",
        "reference_solution_javascript": """function radian_degree(degree) {
    return degree * (Math.PI / 180.0);
}""",
        "starter_code_java": "class Solution {\\n    public double radian_degree(int degree) {\\n        return 0.0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public double radian_degree(int degree) {
        return degree * (Math.PI / 180.0);
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    double radian_degree(int degree);\\n};",
        "reference_solution_cpp": """#include <cmath>
class Solution {
public:
    double radian_degree(int degree) {
        double pi = 3.14159265358979323846;
        return degree * (pi / 180.0);
    }
};"""
    },

    567: {
        "starter_code_javascript": "function bell_Number(n) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function bell_Number(n) {
    let bell = Array.from({length: n + 1}, () => new Array(n + 1).fill(0));
    bell[0][0] = 1;
    for (let i = 1; i <= n; i++) {
        bell[i][0] = bell[i - 1][i - 1];
        for (let j = 1; j <= i; j++) {
            bell[i][j] = bell[i - 1][j - 1] + bell[i][j - 1];
        }
    }
    return bell[n][0];
}""",
        "starter_code_java": "class Solution {\\n    public int bell_Number(int n) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int bell_Number(int n) {
        int[][] bell = new int[n + 1][n + 1];
        bell[0][0] = 1;
        for (int i = 1; i <= n; i++) {
            bell[i][0] = bell[i - 1][i - 1];
            for (int j = 1; j <= i; j++) {
                bell[i][j] = bell[i - 1][j - 1] + bell[i][j - 1];
            }
        }
        return bell[n][0];
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int bell_Number(int n);\\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    int bell_Number(int n) {
        std::vector<std::vector<int>> bell(n + 1, std::vector<int>(n + 1, 0));
        bell[0][0] = 1;
        for (int i = 1; i <= n; ++i) {
            bell[i][0] = bell[i - 1][i - 1];
            for (int j = 1; j <= i; ++j) {
                bell[i][j] = bell[i - 1][j - 1] + bell[i][j - 1];
            }
        }
        return bell[n][0];
    }
};"""
    },

    568: {
        "starter_code_javascript": "function floor_Min(A, B, N) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function floor_Min(A, B, N) {
    let x = Math.max(B - 1, N);
    return Math.floor((A * x) / B);
}""",
        "starter_code_java": "class Solution {\\n    public int floor_Min(int A, int B, int N) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int floor_Min(int A, int B, int N) {
        int x = Math.max(B - 1, N);
        return (A * x) / B;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int floor_Min(int A, int B, int N);\\n};",
        "reference_solution_cpp": """#include <algorithm>
class Solution {
public:
    int floor_Min(int A, int B, int N) {
        int x = std::max(B - 1, N);
        return (A * x) / B;
    }
};"""
    },

    569: {
        "starter_code_javascript": "function remove_kth_element(list1, L) {\\n    return [];\\n}",
        "reference_solution_javascript": """function remove_kth_element(list1, L) {
    let res = list1.slice();
    res.splice(L - 1, 1);
    return res;
}""",
        "starter_code_java": "import java.util.*;\\nclass Solution {\\n    public List<Integer> remove_kth_element(List<Integer> list1, int L) {\\n        return new ArrayList<>();\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public List<Integer> remove_kth_element(List<Integer> list1, int L) {
        List<Integer> res = new ArrayList<>(list1);
        if (L - 1 >= 0 && L - 1 < res.size()) {
            res.remove(L - 1);
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    std::vector<int> remove_kth_element(std::vector<int> list1, int L);\\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    std::vector<int> remove_kth_element(std::vector<int> list1, int L) {
        if (L - 1 >= 0 && L - 1 < (int)list1.size()) {
            list1.erase(list1.begin() + (L - 1));
        }
        return list1;
    }
};"""
    },

    570: {
        "starter_code_javascript": "function max_of_nth(test_list, N) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function max_of_nth(test_list, N) {
    let mx = -Infinity;
    for (let sub of test_list) {
        if (sub[N] > mx) mx = sub[N];
    }
    return mx;
}""",
        "starter_code_java": "import java.util.*;\\nclass Solution {\\n    public int max_of_nth(List<List<Integer>> test_list, int N) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int max_of_nth(List<List<Integer>> test_list, int N) {
        int mx = Integer.MIN_VALUE;
        for (List<Integer> sub : test_list) {
            if (sub.get(N) > mx) mx = sub.get(N);
        }
        return mx;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    int max_of_nth(const std::vector<std::vector<int>>& test_list, int N);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
class Solution {
public:
    int max_of_nth(const std::vector<std::vector<int>>& test_list, int N) {
        int mx = -2147483648;
        for (const auto& sub : test_list) {
            if (sub[N] > mx) mx = sub[N];
        }
        return mx;
    }
};"""
    },

    571: {
        "starter_code_javascript": "function merge(lst) {\\n    return [];\\n}",
        "reference_solution_javascript": """function merge(lst) {
    if (lst.length === 0) return [];
    let res = [];
    for (let j = 0; j < lst[0].length; j++) {
        let row = [];
        for (let i = 0; i < lst.length; i++) {
            row.push(lst[i][j]);
        }
        res.push(row);
    }
    return res;
}""",
        "starter_code_java": "class Solution {\\n    public String[][] merge(char[][] lst) {\\n        return new String[0][0];\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String[][] merge(char[][] lst) {
        if (lst == null || lst.length == 0) return new String[0][0];
        int r = lst.length, c = lst[0].length;
        String[][] res = new String[c][r];
        for (int i = 0; i < r; i++) {
            for (int j = 0; j < c; j++) {
                res[j][i] = String.valueOf(lst[i][j]);
            }
        }
        return res;
    }
    public int[][] merge(int[][] lst) {
        if (lst == null || lst.length == 0) return new int[0][0];
        int r = lst.length, c = lst[0].length;
        int[][] res = new int[c][r];
        for (int i = 0; i < r; i++) {
            for (int j = 0; j < c; j++) {
                res[j][i] = lst[i][j];
            }
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nclass Solution {\\npublic:\\n    std::vector<std::vector<std::string>> merge(const std::vector<std::vector<std::string>>& lst);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
using namespace std;
class Solution {
public:
    vector<vector<string>> merge(const vector<vector<string>>& lst) {
        if (lst.empty()) return {};
        int r = lst.size(), c = lst[0].size();
        vector<vector<string>> res(c, vector<string>(r));
        for (int i = 0; i < r; ++i) {
            for (int j = 0; j < c; ++j) {
                res[j][i] = lst[i][j];
            }
        }
        return res;
    }
    vector<vector<int>> merge(const vector<vector<int>>& lst) {
        if (lst.empty()) return {};
        int r = lst.size(), c = lst[0].size();
        vector<vector<int>> res(c, vector<int>(r));
        for (int i = 0; i < r; ++i) {
            for (int j = 0; j < c; ++j) {
                res[j][i] = lst[i][j];
            }
        }
        return res;
    }
};"""
    },

    572: {
        "starter_code_javascript": "function cummulative_sum(test_list) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function cummulative_sum(test_list) {
    let s = 0;
    for (let sub of test_list) {
        for (let x of sub) s += x;
    }
    return s;
}""",
        "starter_code_java": "import java.util.*;\\nclass Solution {\\n    public int cummulative_sum(List<List<Integer>> test_list) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int cummulative_sum(List<List<Integer>> test_list) {
        int s = 0;
        for (List<Integer> sub : test_list) {
            for (int x : sub) s += x;
        }
        return s;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    int cummulative_sum(const std::vector<std::vector<int>>& test_list);\\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    int cummulative_sum(const std::vector<std::vector<int>>& test_list) {
        int s = 0;
        for (const auto& sub : test_list) {
            for (int x : sub) s += x;
        }
        return s;
    }
};"""
    },

    573: {
        "starter_code_javascript": "function average_tuple(nums) {\\n    return [];\\n}",
        "reference_solution_javascript": """function average_tuple(nums) {
    if (nums.length === 0) return [];
    let n = nums.length;
    let m = nums[0].length;
    let res = [];
    for (let j = 0; j < m; j++) {
        let sum = 0;
        for (let i = 0; i < n; i++) sum += nums[i][j];
        res.push(sum / n);
    }
    return res;
}""",
        "starter_code_java": "import java.util.*;\\nclass Solution {\\n    public List<Double> average_tuple(List<List<Integer>> nums) {\\n        return new ArrayList<>();\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public List<Double> average_tuple(List<List<Integer>> nums) {
        List<Double> res = new ArrayList<>();
        if (nums.isEmpty()) return res;
        int n = nums.size();
        int m = nums.get(0).size();
        for (int j = 0; j < m; j++) {
            double sum = 0;
            for (int i = 0; i < n; i++) sum += nums.get(i).get(j);
            res.add(sum / n);
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    std::vector<double> average_tuple(const std::vector<std::vector<int>>& nums);\\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    std::vector<double> average_tuple(const std::vector<std::vector<int>>& nums) {
        std::vector<double> res;
        if (nums.empty()) return res;
        int n = nums.size();
        int m = nums[0].size();
        for (int j = 0; j < m; ++j) {
            double sum = 0;
            for (int i = 0; i < n; ++i) sum += nums[i][j];
            res.push_back(sum / n);
        }
        return res;
    }
};"""
    },

    574: {
        "starter_code_javascript": "function min_Jumps(a, b, d) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function min_Jumps(a, b, d) {
    let mn = Math.min(a, b);
    let mx = Math.max(a, b);
    if (d >= mx) return (d + mx - 1) / mx;
    if (d === 0) return 0;
    if (d === mn) return 1;
    return 2;
}""",
        "starter_code_java": "class Solution {\\n    public double min_Jumps(int a, int b, int d) {\\n        return 0.0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public double min_Jumps(int a, int b, int d) {
        int mn = Math.min(a, b);
        int mx = Math.max(a, b);
        if (d >= mx) return ((double)d + mx - 1) / mx;
        if (d == 0) return 0;
        if (d == mn) return 1;
        return 2;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    double min_Jumps(int a, int b, int d);\\n};",
        "reference_solution_cpp": """#include <algorithm>
class Solution {
public:
    double min_Jumps(int a, int b, int d) {
        int mn = std::min(a, b);
        int mx = std::max(a, b);
        if (d >= mx) return ((double)d + mx - 1) / mx;
        if (d == 0) return 0;
        if (d == mn) return 1;
        return 2;
    }
};"""
    },

    575: {
        "starter_code_javascript": "function div_list(nums1, nums2) {\\n    return [];\\n}",
        "reference_solution_javascript": """function div_list(nums1, nums2) {
    return nums1.map((x, i) => x / nums2[i]);
}""",
        "starter_code_java": "import java.util.*;\\nclass Solution {\\n    public List<Double> div_list(List<Integer> nums1, List<Integer> nums2) {\\n        return new ArrayList<>();\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public List<Double> div_list(List<Integer> nums1, List<Integer> nums2) {
        List<Double> res = new ArrayList<>();
        for (int i = 0; i < nums1.size(); i++) {
            res.add((double) nums1.get(i) / nums2.get(i));
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    std::vector<double> div_list(const std::vector<int>& nums1, const std::vector<int>& nums2);\\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    std::vector<double> div_list(const std::vector<int>& nums1, const std::vector<int>& nums2) {
        std::vector<double> res;
        for (size_t i = 0; i < nums1.size(); ++i) {
            res.push_back((double)nums1[i] / nums2[i]);
        }
        return res;
    }
};"""
    },

    576: {
        "starter_code_javascript": "function move_num(test_str) {\\n    return '';\\n}",
        "reference_solution_javascript": """function move_num(test_str) {
    let chars = '', digits = '';
    for (let c of test_str) {
        if (c >= '0' && c <= '9') digits += c;
        else chars += c;
    }
    return chars + digits;
}""",
        "starter_code_java": "class Solution {\\n    public String move_num(String test_str) {\\n        return \\"\\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String move_num(String test_str) {
        StringBuilder chars = new StringBuilder();
        StringBuilder digits = new StringBuilder();
        for (char c : test_str.toCharArray()) {
            if (Character.isDigit(c)) digits.append(c);
            else chars.append(c);
        }
        return chars.toString() + digits.toString();
    }
}""",
        "starter_code_cpp": "#include <string>\\nclass Solution {\\npublic:\\n    std::string move_num(const std::string& test_str);\\n};",
        "reference_solution_cpp": """#include <string>
#include <cctype>
class Solution {
public:
    std::string move_num(const std::string& test_str) {
        std::string chars = "", digits = "";
        for (char c : test_str) {
            if (std::isdigit(c)) digits += c;
            else chars += c;
        }
        return chars + digits;
    }
};"""
    },

    577: {
        "starter_code_javascript": "function largest_subset(a, n) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function largest_subset(a, n) {
    let dp = new Array(n).fill(0);
    dp[n - 1] = 1;
    for (let i = n - 2; i >= 0; i--) {
        let mxm = 0;
        for (let j = i + 1; j < n; j++) {
            if (a[j] % a[i] === 0 || a[i] % a[j] === 0) {
                mxm = Math.max(mxm, dp[j]);
            }
        }
        dp[i] = 1 + mxm;
    }
    return Math.max(...dp);
}""",
        "starter_code_java": "class Solution {\\n    public int largest_subset(int[] a, int n) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int largest_subset(int[] a, int n) {
        int[] dp = new int[n];
        dp[n - 1] = 1;
        int max = 1;
        for (int i = n - 2; i >= 0; i--) {
            int mxm = 0;
            for (int j = i + 1; j < n; j++) {
                if (a[j] % a[i] == 0 || a[i] % a[j] == 0) {
                    mxm = Math.max(mxm, dp[j]);
                }
            }
            dp[i] = 1 + mxm;
            max = Math.max(max, dp[i]);
        }
        return max;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    int largest_subset(const std::vector<int>& a, int n);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
class Solution {
public:
    int largest_subset(const std::vector<int>& a, int n) {
        std::vector<int> dp(n, 0);
        dp[n - 1] = 1;
        int max_val = 1;
        for (int i = n - 2; i >= 0; --i) {
            int mxm = 0;
            for (int j = i + 1; j < n; ++j) {
                if (a[j] % a[i] == 0 || a[i] % a[j] == 0) {
                    mxm = std::max(mxm, dp[j]);
                }
            }
            dp[i] = 1 + mxm;
            max_val = std::max(max_val, dp[i]);
        }
        return max_val;
    }
};"""
    },

    578: {
        "starter_code_javascript": "function increment_numerics(test_list, K) {\\n    return [];\\n}",
        "reference_solution_javascript": """function increment_numerics(test_list, K) {
    return test_list.map(ele => /^\\\\d+$/.test(ele) ? String(parseInt(ele, 10) + K) : ele);
}""",
        "starter_code_java": "import java.util.*;\\nclass Solution {\\n    public List<String> increment_numerics(List<String> test_list, int K) {\\n        return new ArrayList<>();\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public List<String> increment_numerics(List<String> test_list, int K) {
        List<String> res = new ArrayList<>();
        for (String ele : test_list) {
            if (ele.matches("\\\\d+")) {
                res.add(String.valueOf(Integer.parseInt(ele) + K));
            } else {
                res.add(ele);
            }
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nclass Solution {\\npublic:\\n    std::vector<std::string> increment_numerics(const std::vector<std::string>& test_list, int K);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <cctype>
class Solution {
public:
    std::vector<std::string> increment_numerics(const std::vector<std::string>& test_list, int K) {
        std::vector<std::string> res;
        for (const auto& ele : test_list) {
            bool is_num = !ele.empty();
            for (char c : ele) {
                if (!std::isdigit(c)) { is_num = false; break; }
            }
            if (is_num) {
                res.push_back(std::to_string(std::stoi(ele) + K));
            } else {
                res.push_back(ele);
            }
        }
        return res;
    }
};"""
    },

    579: {
        "starter_code_javascript": "function get_median(arr1, arr2, n) {\\n    return 0.0;\\n}",
        "reference_solution_javascript": """function get_median(arr1, arr2, n) {
    let merged = arr1.concat(arr2).sort((a, b) => a - b);
    let mid = merged.length / 2;
    return (merged[mid - 1] + merged[mid]) / 2;
}""",
        "starter_code_java": "class Solution {\\n    public double get_median(int[] arr1, int[] arr2, int n) {\\n        return 0.0;\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public double get_median(int[] arr1, int[] arr2, int n) {
        int[] merged = new int[2 * n];
        System.arraycopy(arr1, 0, merged, 0, n);
        System.arraycopy(arr2, 0, merged, n, n);
        Arrays.sort(merged);
        return (merged[n - 1] + merged[n]) / 2.0;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    double get_median(const std::vector<int>& arr1, const std::vector<int>& arr2, int n);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
class Solution {
public:
    double get_median(const std::vector<int>& arr1, const std::vector<int>& arr2, int n) {
        std::vector<int> merged = arr1;
        merged.insert(merged.end(), arr2.begin(), arr2.end());
        std::sort(merged.begin(), merged.end());
        return (merged[n - 1] + merged[n]) / 2.0;
    }
};"""
    },

    580: {
        "starter_code_javascript": "function nth_nums(nums, n) {\\n    return [];\\n}",
        "reference_solution_javascript": """function nth_nums(nums, n) {
    return nums.map(x => Math.pow(x, n));
}""",
        "starter_code_java": "import java.util.*;\\nclass Solution {\\n    public List<Integer> nth_nums(List<Integer> nums, int n) {\\n        return new ArrayList<>();\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public List<Integer> nth_nums(List<Integer> nums, int n) {
        List<Integer> res = new ArrayList<>();
        for (int x : nums) {
            res.add((int) Math.round(Math.pow(x, n)));
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    std::vector<int> nth_nums(const std::vector<int>& nums, int n);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <cmath>
class Solution {
public:
    std::vector<int> nth_nums(const std::vector<int>& nums, int n) {
        std::vector<int> res;
        for (int x : nums) {
            res.push_back((int)std::round(std::pow(x, n)));
        }
        return res;
    }
};"""
    },

    581: {
        "starter_code_javascript": "function is_upper(string) {\\n    return '';\\n}",
        "reference_solution_javascript": """function is_upper(string) {
    return string.toUpperCase();
}""",
        "starter_code_java": "class Solution {\\n    public String is_upper(String string) {\\n        return \\"\\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String is_upper(String string) {
        return string.toUpperCase();
    }
}""",
        "starter_code_cpp": "#include <string>\\nclass Solution {\\npublic:\\n    std::string is_upper(std::string string);\\n};",
        "reference_solution_cpp": """#include <string>
#include <cctype>
class Solution {
public:
    std::string is_upper(std::string str) {
        for (char &c : str) c = std::toupper(c);
        return str;
    }
};"""
    },

    582: {
        "starter_code_javascript": "function swap_List(newList) {\\n    return [];\\n}",
        "reference_solution_javascript": """function swap_List(newList) {
    if (newList.length < 2) return newList;
    let res = newList.slice();
    let temp = res[0];
    res[0] = res[res.length - 1];
    res[res.length - 1] = temp;
    return res;
}""",
        "starter_code_java": "import java.util.*;\\nclass Solution {\\n    public List<Integer> swap_List(List<Integer> newList) {\\n        return new ArrayList<>();\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public List<Integer> swap_List(List<Integer> newList) {
        if (newList.size() < 2) return newList;
        List<Integer> res = new ArrayList<>(newList);
        int temp = res.get(0);
        res.set(0, res.get(res.size() - 1));
        res.set(res.size() - 1, temp);
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    std::vector<int> swap_List(std::vector<int> newList);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
class Solution {
public:
    std::vector<int> swap_List(std::vector<int> newList) {
        if (newList.size() < 2) return newList;
        int temp = newList[0];
        newList[0] = newList[newList.size() - 1];
        newList[newList.size() - 1] = temp;
        return newList;
    }
};"""
    },

    583: {
        "starter_code_javascript": "function triangle_area(r) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function triangle_area(r) {
    return r < 0 ? -1 : r * r;
}""",
        "starter_code_java": "class Solution {\\n    public int triangle_area(int r) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int triangle_area(int r) {
        return r < 0 ? -1 : r * r;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int triangle_area(int r);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    int triangle_area(int r) {
        return r < 0 ? -1 : r * r;
    }
};"""
    },

    584: {
        "starter_code_javascript": "function find_First_Missing(array, start, end) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function find_First_Missing(array, start, end) {
    if (start > end) return end + 1;
    if (start !== array[start]) return start;
    let mid = Math.floor((start + end) / 2);
    if (array[mid] === mid) return find_First_Missing(array, mid + 1, end);
    return find_First_Missing(array, start, mid);
}""",
        "starter_code_java": "class Solution {\\n    public int find_First_Missing(int[] array, int start, int end) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int find_First_Missing(int[] array, int start, int end) {
        if (start > end) return end + 1;
        if (start != array[start]) return start;
        int mid = (start + end) / 2;
        if (array[mid] == mid) return find_First_Missing(array, mid + 1, end);
        return find_First_Missing(array, start, mid);
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    int find_First_Missing(const std::vector<int>& array, int start, int end);\\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    int find_First_Missing(const std::vector<int>& array, int start, int end) {
        if (start > end) return end + 1;
        if (start != array[start]) return start;
        int mid = (start + end) / 2;
        if (array[mid] == mid) return find_First_Missing(array, mid + 1, end);
        return find_First_Missing(array, start, mid);
    }
};"""
    },

    585: {
        "starter_code_javascript": "function replace_spaces(string) {\\n    return '';\\n}",
        "reference_solution_javascript": """function replace_spaces(string) {
    return string.trim().replace(/ /g, '%20');
}""",
        "starter_code_java": "class Solution {\\n    public String replace_spaces(String string) {\\n        return \\"\\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String replace_spaces(String string) {
        return string.trim().replace(" ", "%20");
    }
}""",
        "starter_code_cpp": "#include <string>\\nclass Solution {\\npublic:\\n    std::string replace_spaces(std::string string);\\n};",
        "reference_solution_cpp": """#include <string>
class Solution {
public:
    std::string replace_spaces(std::string str) {
        while (!str.empty() && (str.front() == ' ' || str.front() == '\\t')) str.erase(str.begin());
        while (!str.empty() && (str.back() == ' ' || str.back() == '\\t')) str.pop_back();
        std::string res = "";
        for (char c : str) {
            if (c == ' ') res += "%20";
            else res += c;
        }
        return res;
    }
};"""
    },

    586: {
        "starter_code_javascript": "function Split(list) {\\n    return [];\\n}",
        "reference_solution_javascript": """function Split(list) {
    return list.filter(x => x % 2 === 0);
}""",
        "starter_code_java": "import java.util.*;\\nclass Solution {\\n    public List<Integer> Split(List<Integer> list) {\\n        return new ArrayList<>();\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public List<Integer> Split(List<Integer> list) {
        List<Integer> res = new ArrayList<>();
        for (int x : list) {
            if (x % 2 == 0) res.add(x);
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    std::vector<int> Split(const std::vector<int>& list);\\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    std::vector<int> Split(const std::vector<int>& list) {
        std::vector<int> res;
        for (int x : list) {
            if (x % 2 == 0) res.push_back(x);
        }
        return res;
    }
};"""
    },

    587: {
        "starter_code_javascript": "function get_coordinates(test_tup) {\\n    return [];\\n}",
        "reference_solution_javascript": """function get_coordinates(test_tup) {
    let res = [];
    for (let x = test_tup[0] - 1; x <= test_tup[0] + 1; x++) {
        for (let y = test_tup[1] - 1; y <= test_tup[1] + 1; y++) {
            res.push([x, y]);
        }
    }
    return res;
}""",
        "starter_code_java": "import java.util.*;\\nclass Solution {\\n    public List<List<Integer>> get_coordinates(List<Integer> test_tup) {\\n        return new ArrayList<>();\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public List<List<Integer>> get_coordinates(List<Integer> test_tup) {
        List<List<Integer>> res = new ArrayList<>();
        int r = test_tup.get(0);
        int c = test_tup.get(1);
        for (int x = r - 1; x <= r + 1; x++) {
            for (int y = c - 1; y <= c + 1; y++) {
                res.add(Arrays.asList(x, y));
            }
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    std::vector<std::vector<int>> get_coordinates(const std::vector<int>& test_tup);\\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    std::vector<std::vector<int>> get_coordinates(const std::vector<int>& test_tup) {
        std::vector<std::vector<int>> res;
        int r = test_tup[0], c = test_tup[1];
        for (int x = r - 1; x <= r + 1; ++x) {
            for (int y = c - 1; y <= c + 1; ++y) {
                res.push_back({x, y});
            }
        }
        return res;
    }
};"""
    },

    588: {
        "starter_code_javascript": "function replace_spaces(text) {\\n    return '';\\n}",
        "reference_solution_javascript": """function replace_spaces(text) {
    return text.replace(/ /g, '_');
}""",
        "starter_code_java": "class Solution {\\n    public String replace_spaces(String text) {\\n        return \\"\\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String replace_spaces(String text) {
        return text.replace(" ", "_");
    }
}""",
        "starter_code_cpp": "#include <string>\\nclass Solution {\\npublic:\\n    std::string replace_spaces(std::string text);\\n};",
        "reference_solution_cpp": """#include <string>
class Solution {
public:
    std::string replace_spaces(std::string text) {
        for (char &c : text) {
            if (c == ' ') c = '_';
        }
        return text;
    }
};"""
    },

    589: {
        "starter_code_javascript": "function move_zero(num_list) {\\n    return [];\\n}",
        "reference_solution_javascript": """function move_zero(num_list) {
    let nonZeros = num_list.filter(x => x !== 0);
    let zeros = num_list.filter(x => x === 0);
    return nonZeros.concat(zeros);
}""",
        "starter_code_java": "import java.util.*;\\nclass Solution {\\n    public List<Integer> move_zero(List<Integer> num_list) {\\n        return new ArrayList<>();\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public List<Integer> move_zero(List<Integer> num_list) {
        List<Integer> res = new ArrayList<>();
        int zeros = 0;
        for (int x : num_list) {
            if (x == 0) zeros++;
            else res.add(x);
        }
        for (int i = 0; i < zeros; i++) res.add(0);
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    std::vector<int> move_zero(const std::vector<int>& num_list);\\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    std::vector<int> move_zero(const std::vector<int>& num_list) {
        std::vector<int> res;
        int zeros = 0;
        for (int x : num_list) {
            if (x == 0) zeros++;
            else res.push_back(x);
        }
        for (int i = 0; i < zeros; ++i) res.push_back(0);
        return res;
    }
};"""
    },

    590: {
        "starter_code_javascript": "function pair_OR_Sum(arr, n) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function pair_OR_Sum(arr, n) {
    let ans = 0;
    for (let i = 0; i < n; i++) {
        for (let j = i + 1; j < n; j++) {
            ans += (arr[i] ^ arr[j]);
        }
    }
    return ans;
}""",
        "starter_code_java": "class Solution {\\n    public int pair_OR_Sum(int[] arr, int n) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int pair_OR_Sum(int[] arr, int n) {
        int ans = 0;
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                ans += (arr[i] ^ arr[j]);
            }
        }
        return ans;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    int pair_OR_Sum(const std::vector<int>& arr, int n);\\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    int pair_OR_Sum(const std::vector<int>& arr, int n) {
        int ans = 0;
        for (int i = 0; i < n; ++i) {
            for (int j = i + 1; j < n; ++j) {
                ans += (arr[i] ^ arr[j]);
            }
        }
        return ans;
    }
};"""
    },

    591: {
        "starter_code_javascript": "function even_Power_Sum(n) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function even_Power_Sum(n) {
    let sum = 0;
    for (let i = 1; i <= n; i++) {
        let j = 2 * i;
        sum += j * j * j * j;
    }
    return sum;
}""",
        "starter_code_java": "class Solution {\\n    public int even_Power_Sum(int n) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int even_Power_Sum(int n) {
        int sum = 0;
        for (int i = 1; i <= n; i++) {
            int j = 2 * i;
            sum += j * j * j * j;
        }
        return sum;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int even_Power_Sum(int n);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    int even_Power_Sum(int n) {
        int sum = 0;
        for (int i = 1; i <= n; ++i) {
            int j = 2 * i;
            sum += j * j * j * j;
        }
        return sum;
    }
};"""
    },

    592: {
        "starter_code_javascript": "function heap_sort(iterable) {\\n    return [];\\n}",
        "reference_solution_javascript": """function heap_sort(iterable) {
    return iterable.slice().sort((a, b) => a - b);
}""",
        "starter_code_java": "import java.util.*;\\nclass Solution {\\n    public List<Integer> heap_sort(List<Integer> iterable) {\\n        return new ArrayList<>();\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public List<Integer> heap_sort(List<Integer> iterable) {
        List<Integer> res = new ArrayList<>(iterable);
        Collections.sort(res);
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    std::vector<int> heap_sort(std::vector<int> iterable);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
class Solution {
public:
    std::vector<int> heap_sort(std::vector<int> iterable) {
        std::sort(iterable.begin(), iterable.end());
        return iterable;
    }
};"""
    },

    593: {
        "starter_code_javascript": "function Check_Solution(a, b, c) {\\n    return '';\\n}",
        "reference_solution_javascript": """function Check_Solution(a, b, c) {
    return a === c ? "Yes" : "No";
}""",
        "starter_code_java": "class Solution {\\n    public String Check_Solution(int a, int b, int c) {\\n        return \\"\\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String Check_Solution(int a, int b, int c) {
        return a == c ? "Yes" : "No";
    }
}""",
        "starter_code_cpp": "#include <string>\\nclass Solution {\\npublic:\\n    std::string Check_Solution(int a, int b, int c);\\n};",
        "reference_solution_cpp": """#include <string>
class Solution {
public:
    std::string Check_Solution(int a, int b, int c) {
        return a == c ? "Yes" : "No";
    }
};"""
    },

    594: {
        "starter_code_javascript": "function noprofit_noloss(actual_cost, sale_amount) {\\n    return false;\\n}",
        "reference_solution_javascript": """function noprofit_noloss(actual_cost, sale_amount) {
    return actual_cost === sale_amount;
}""",
        "starter_code_java": "class Solution {\\n    public boolean noprofit_noloss(int actual_cost, int sale_amount) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public boolean noprofit_noloss(int actual_cost, int sale_amount) {
        return actual_cost == sale_amount;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    bool noprofit_noloss(int actual_cost, int sale_amount);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    bool noprofit_noloss(int actual_cost, int sale_amount) {
        return actual_cost == sale_amount;
    }
};"""
    },

    595: {
        "starter_code_javascript": "function wind_chill(v, t) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function wind_chill(v, t) {
    let windchill = 13.12 + 0.6215 * t - 11.37 * Math.pow(v, 0.16) + 0.3965 * t * Math.pow(v, 0.16);
    return Math.round(windchill);
}""",
        "starter_code_java": "class Solution {\\n    public int wind_chill(int v, int t) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int wind_chill(int v, int t) {
        double windchill = 13.12 + 0.6215 * t - 11.37 * Math.pow(v, 0.16) + 0.3965 * t * Math.pow(v, 0.16);
        return (int) Math.round(windchill);
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int wind_chill(int v, int t);\\n};",
        "reference_solution_cpp": """#include <cmath>
class Solution {
public:
    int wind_chill(int v, int t) {
        double windchill = 13.12 + 0.6215 * t - 11.37 * std::pow(v, 0.16) + 0.3965 * t * std::pow(v, 0.16);
        return (int) std::round(windchill);
    }
};"""
    },

    596: {
        "starter_code_javascript": "function sample_nam(sample_names) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function sample_nam(sample_names) {
    let filtered = sample_names.filter(el => el.length > 0 && /^[A-Z][a-z]*$/.test(el));
    return filtered.reduce((acc, el) => acc + el.length, 0);
}""",
        "starter_code_java": "import java.util.*;\\nclass Solution {\\n    public int sample_nam(List<String> sample_names) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int sample_nam(List<String> sample_names) {
        int count = 0;
        for (String el : sample_names) {
            if (el.matches("^[A-Z][a-z]*$")) {
                count += el.length();
            }
        }
        return count;
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nclass Solution {\\npublic:\\n    int sample_nam(const std::vector<std::string>& sample_names);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <cctype>
class Solution {
public:
    int sample_nam(const std::vector<std::string>& sample_names) {
        int count = 0;
        for (const auto& el : sample_names) {
            if (el.empty()) continue;
            if (!std::isupper(el[0])) continue;
            bool ok = true;
            for (size_t i = 1; i < el.size(); ++i) {
                if (!std::islower(el[i])) { ok = false; break; }
            }
            if (ok) count += el.size();
        }
        return count;
    }
};"""
    },

    597: {
        "starter_code_javascript": "function remove_parenthesis(items) {\\n    return '';\\n}",
        "reference_solution_javascript": """function remove_parenthesis(items) {
    return items[0].replace(/ ?\\\\([^)]+\\\\)/g, '');
}""",
        "starter_code_java": "import java.util.*;\\nclass Solution {\\n    public String remove_parenthesis(List<String> items) {\\n        return \\"\\";\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public String remove_parenthesis(List<String> items) {
        return items.get(0).replaceAll(" ?\\\\([^)]+\\\\)", "");
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nclass Solution {\\npublic:\\n    std::string remove_parenthesis(const std::vector<std::string>& items);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <regex>
class Solution {
public:
    std::string remove_parenthesis(const std::vector<std::string>& items) {
        std::regex re(" ?\\\\([^)]+\\\\)");
        return std::regex_replace(items[0], re, "");
    }
};"""
    },

    598: {
        "starter_code_javascript": "function is_nonagonal(n) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function is_nonagonal(n) {
    return Math.floor(n * (7 * n - 5) / 2);
}""",
        "starter_code_java": "class Solution {\\n    public int is_nonagonal(int n) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int is_nonagonal(int n) {
        return n * (7 * n - 5) / 2;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int is_nonagonal(int n);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    int is_nonagonal(int n) {
        return n * (7 * n - 5) / 2;
    }
};"""
    },

    599: {
        "starter_code_javascript": "function text_match_wordz_middle(text) {\\n    return '';\\n}",
        "reference_solution_javascript": """function text_match_wordz_middle(text) {
    return /\\\\Bz\\\\B/.test(text) ? 'Found a match!' : 'Not matched!';
}""",
        "starter_code_java": "class Solution {\\n    public String text_match_wordz_middle(String text) {\\n        return \\"\\";\\n    }\\n}",
        "reference_solution_java": """import java.util.regex.*;
class Solution {
    public String text_match_wordz_middle(String text) {
        Pattern p = Pattern.compile("\\\\Bz\\\\B");
        return p.matcher(text).find() ? "Found a match!" : "Not matched!";
    }
}""",
        "starter_code_cpp": "#include <string>\\nclass Solution {\\npublic:\\n    std::string text_match_wordz_middle(const std::string& text);\\n};",
        "reference_solution_cpp": """#include <string>
#include <regex>
class Solution {
public:
    std::string text_match_wordz_middle(const std::string& text) {
        std::regex re("\\\\Bz\\\\B");
        return std::regex_search(text, re) ? "Found a match!" : "Not matched!";
    }
};"""
    },

    600: {
        "starter_code_javascript": "function reverse_Array_Upto_K(input, k) {\\n    return [];\\n}",
        "reference_solution_javascript": """function reverse_Array_Upto_K(input, k) {
    let first = input.slice(0, k).reverse();
    return first.concat(input.slice(k));
}""",
        "starter_code_java": "import java.util.*;\\nclass Solution {\\n    public List<Integer> reverse_Array_Upto_K(List<Integer> input, int k) {\\n        return new ArrayList<>();\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public List<Integer> reverse_Array_Upto_K(List<Integer> input, int k) {
        List<Integer> res = new ArrayList<>(input.subList(0, k));
        Collections.reverse(res);
        res.addAll(input.subList(k, input.size()));
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    std::vector<int> reverse_Array_Upto_K(std::vector<int> input, int k);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
class Solution {
public:
    std::vector<int> reverse_Array_Upto_K(std::vector<int> input, int k) {
        std::reverse(input.begin(), input.begin() + k);
        return input;
    }
};"""
    },

    601: {
        "starter_code_javascript": "function find_k_product(test_list, K) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function find_k_product(test_list, K) {
    let prod = 1;
    for (let sub of test_list) prod *= sub[K];
    return prod;
}""",
        "starter_code_java": "import java.util.*;\\nclass Solution {\\n    public int find_k_product(List<List<Integer>> test_list, int K) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int find_k_product(List<List<Integer>> test_list, int K) {
        int prod = 1;
        for (List<Integer> sub : test_list) prod *= sub.get(K);
        return prod;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    int find_k_product(const std::vector<std::vector<int>>& test_list, int K);\\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    int find_k_product(const std::vector<std::vector<int>>& test_list, int K) {
        int prod = 1;
        for (const auto& sub : test_list) prod *= sub[K];
        return prod;
    }
};"""
    },

    602: {
        "starter_code_javascript": "function No_of_cubes(N, K) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function No_of_cubes(N, K) {
    let side = N - K + 1;
    return side * side * side;
}""",
        "starter_code_java": "class Solution {\\n    public int No_of_cubes(int N, int K) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int No_of_cubes(int N, int K) {
        int side = N - K + 1;
        return side * side * side;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int No_of_cubes(int N, int K);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    int No_of_cubes(int N, int K) {
        int side = N - K + 1;
        return side * side * side;
    }
};"""
    },

    603: {
        "starter_code_javascript": "function split_upperstring(text) {\\n    return [];\\n}",
        "reference_solution_javascript": """function split_upperstring(text) {
    return text.match(/[A-Z][^A-Z]*/g) || [];
}""",
        "starter_code_java": "import java.util.*;\\nclass Solution {\\n    public List<String> split_upperstring(String text) {\\n        return new ArrayList<>();\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
import java.util.regex.*;
class Solution {
    public List<String> split_upperstring(String text) {
        List<String> res = new ArrayList<>();
        Matcher m = Pattern.compile("[A-Z][^A-Z]*").matcher(text);
        while (m.find()) res.add(m.group());
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nclass Solution {\\npublic:\\n    std::vector<std::string> split_upperstring(const std::string& text);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <regex>
class Solution {
public:
    std::vector<std::string> split_upperstring(const std::string& text) {
        std::vector<std::string> res;
        std::regex re("[A-Z][^A-Z]*");
        auto begin = std::sregex_iterator(text.begin(), text.end(), re);
        auto end = std::sregex_iterator();
        for (auto it = begin; it != end; ++it) res.push_back(it->str());
        return res;
    }
};"""
    },

    604: {
        "starter_code_javascript": "function exchange_elements(lst) {\\n    return [];\\n}",
        "reference_solution_javascript": """function exchange_elements(lst) {
    let res = lst.slice();
    for (let i = 0; i + 1 < res.length; i += 2) {
        let tmp = res[i];
        res[i] = res[i + 1];
        res[i + 1] = tmp;
    }
    return res;
}""",
        "starter_code_java": "import java.util.*;\\nclass Solution {\\n    public List<Integer> exchange_elements(List<Integer> lst) {\\n        return new ArrayList<>();\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public List<Integer> exchange_elements(List<Integer> lst) {
        List<Integer> res = new ArrayList<>(lst);
        for (int i = 0; i + 1 < res.size(); i += 2) {
            int tmp = res.get(i);
            res.set(i, res.get(i + 1));
            res.set(i + 1, tmp);
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    std::vector<int> exchange_elements(std::vector<int> lst);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
class Solution {
public:
    std::vector<int> exchange_elements(std::vector<int> lst) {
        for (size_t i = 0; i + 1 < lst.size(); i += 2) {
            std::swap(lst[i], lst[i + 1]);
        }
        return lst;
    }
};"""
    },

    605: {
        "starter_code_javascript": "function sum_Range_list(nums, m, n) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function sum_Range_list(nums, m, n) {
    let sum = 0;
    for (let i = m; i <= n; i++) sum += nums[i];
    return sum;
}""",
        "starter_code_java": "import java.util.*;\\nclass Solution {\\n    public int sum_Range_list(List<Integer> nums, int m, int n) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int sum_Range_list(List<Integer> nums, int m, int n) {
        int sum = 0;
        for (int i = m; i <= n; i++) sum += nums.get(i);
        return sum;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    int sum_Range_list(const std::vector<int>& nums, int m, int n);\\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    int sum_Range_list(const std::vector<int>& nums, int m, int n) {
        int sum = 0;
        for (int i = m; i <= n; ++i) sum += nums[i];
        return sum;
    }
};"""
    },

    606: {
        "starter_code_javascript": "function are_Equal(arr1, arr2, n, m) {\\n    return false;\\n}",
        "reference_solution_javascript": """function are_Equal(arr1, arr2, n, m) {
    if (n !== m) return false;
    let a1 = arr1.slice().sort((a, b) => a - b);
    let a2 = arr2.slice().sort((a, b) => a - b);
    for (let i = 0; i < n - 1; i++) {
        if (a1[i] !== a2[i]) return false;
    }
    return true;
}""",
        "starter_code_java": "class Solution {\\n    public boolean are_Equal(int[] arr1, int[] arr2, int n, int m) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public boolean are_Equal(int[] arr1, int[] arr2, int n, int m) {
        if (n != m) return false;
        int[] a1 = arr1.clone();
        int[] a2 = arr2.clone();
        Arrays.sort(a1);
        Arrays.sort(a2);
        for (int i = 0; i < n - 1; i++) {
            if (a1[i] != a2[i]) return false;
        }
        return true;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    bool are_Equal(std::vector<int> arr1, std::vector<int> arr2, int n, int m);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
class Solution {
public:
    bool are_Equal(std::vector<int> arr1, std::vector<int> arr2, int n, int m) {
        if (n != m) return false;
        std::sort(arr1.begin(), arr1.end());
        std::sort(arr2.begin(), arr2.end());
        for (int i = 0; i < n - 1; ++i) {
            if (arr1[i] != arr2[i]) return false;
        }
        return true;
    }
};"""
    },

    607: {
        "starter_code_javascript": "function check_subset(test_tup1, test_tup2) {\\n    return false;\\n}",
        "reference_solution_javascript": """function check_subset(test_tup1, test_tup2) {
    let s1 = new Set(test_tup1);
    return test_tup2.every(x => s1.has(x));
}""",
        "starter_code_java": "import java.util.*;\\nclass Solution {\\n    public boolean check_subset(List<Integer> test_tup1, List<Integer> test_tup2) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public boolean check_subset(List<Integer> test_tup1, List<Integer> test_tup2) {
        Set<Integer> s1 = new HashSet<>(test_tup1);
        for (int x : test_tup2) {
            if (!s1.contains(x)) return false;
        }
        return true;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    bool check_subset(const std::vector<int>& test_tup1, const std::vector<int>& test_tup2);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <unordered_set>
class Solution {
public:
    bool check_subset(const std::vector<int>& test_tup1, const std::vector<int>& test_tup2) {
        std::unordered_set<int> s1(test_tup1.begin(), test_tup1.end());
        for (int x : test_tup2) {
            if (!s1.count(x)) return false;
        }
        return true;
    }
};"""
    },

    608: {
        "starter_code_javascript": "function matrix_to_list(test_list) {\\n    return '';\\n}",
        "reference_solution_javascript": """function matrix_to_list(test_list) {
    let t0 = [], t1 = [];
    for (let sub of test_list) {
        for (let pair of sub) {
            t0.push(pair[0]);
            t1.push(pair[1]);
        }
    }
    return `[(${t0.join(', ')}), (${t1.join(', ')})]`;
}""",
        "starter_code_java": "class Solution {\\n    public String matrix_to_list(int[][][] test_list) {\\n        return \\"\\";\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public String matrix_to_list(int[][][] test_list) {
        List<Integer> t0 = new ArrayList<>();
        List<Integer> t1 = new ArrayList<>();
        for (int[][] sub : test_list) {
            for (int[] pair : sub) {
                t0.add(pair[0]);
                t1.add(pair[1]);
            }
        }
        StringBuilder sb0 = new StringBuilder("(");
        for (int i = 0; i < t0.size(); i++) {
            if (i > 0) sb0.append(", ");
            sb0.append(t0.get(i));
        }
        sb0.append(")");
        StringBuilder sb1 = new StringBuilder("(");
        for (int i = 0; i < t1.size(); i++) {
            if (i > 0) sb1.append(", ");
            sb1.append(t1.get(i));
        }
        sb1.append(")");
        return "[" + sb0.toString() + ", " + sb1.toString() + "]";
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nclass Solution {\\npublic:\\n    std::string matrix_to_list(const std::vector<std::vector<std::vector<int>>>& test_list);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
class Solution {
public:
    std::string matrix_to_list(const std::vector<std::vector<std::vector<int>>>& test_list) {
        std::vector<int> t0, t1;
        for (const auto& sub : test_list) {
            for (const auto& pair : sub) {
                t0.push_back(pair[0]);
                t1.push_back(pair[1]);
            }
        }
        std::string s0 = "(", s1 = "(";
        for (size_t i = 0; i < t0.size(); ++i) {
            if (i > 0) s0 += ", ";
            s0 += std::to_string(t0[i]);
        }
        s0 += ")";
        for (size_t i = 0; i < t1.size(); ++i) {
            if (i > 0) s1 += ", ";
            s1 += std::to_string(t1[i]);
        }
        s1 += ")";
        return "[" + s0 + ", " + s1 + "]";
    }
};"""
    },

    609: {
        "starter_code_javascript": "function grouping_dictionary(l) {\\n    return {};\\n}",
        "reference_solution_javascript": """function grouping_dictionary(l) {
    let d = {};
    for (let [k, v] of l) {
        if (!d[k]) d[k] = [];
        d[k].push(v);
    }
    return d;
}""",
        "starter_code_java": "import java.util.*;\\nclass Solution {\\n    public Map<String, Object> grouping_dictionary(Object[][] l) {\\n        return new LinkedHashMap<>();\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public Map<String, Object> grouping_dictionary(Object[][] l) {
        Map<String, List<Integer>> temp = new LinkedHashMap<>();
        for (Object[] item : l) {
            String k = (String) item[0];
            int v = ((Number) item[1]).intValue();
            temp.computeIfAbsent(k, key -> new ArrayList<>()).add(v);
        }
        Map<String, Object> d = new LinkedHashMap<>();
        for (Map.Entry<String, List<Integer>> entry : temp.entrySet()) {
            List<Integer> list = entry.getValue();
            int[] arr = new int[list.size()];
            for (int i = 0; i < list.size(); i++) arr[i] = list.get(i);
            d.put(entry.getKey(), arr);
        }
        return d;
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\n#include <unordered_map>\\nclass Solution {\\npublic:\\n    std::unordered_map<std::string, std::vector<int>> grouping_dictionary(const std::vector<std::vector<std::string>>& l);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <unordered_map>
class Solution {
public:
    std::unordered_map<std::string, std::vector<int>> grouping_dictionary(const std::vector<std::vector<std::string>>& l) {
        std::unordered_map<std::string, std::vector<int>> res;
        for (const auto& item : l) {
            res[item[0]].push_back(std::stoi(item[1]));
        }
        return res;
    }
};"""
    },

    610: {
        "starter_code_javascript": "function rectangle_perimeter(l, b) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function rectangle_perimeter(l, b) {
    return 2 * (l + b);
}""",
        "starter_code_java": "class Solution {\\n    public int rectangle_perimeter(int l, int b) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int rectangle_perimeter(int l, int b) {
        return 2 * (l + b);
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int rectangle_perimeter(int l, int b);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    int rectangle_perimeter(int l, int b) {
        return 2 * (l + b);
    }
};"""
    }
}
'''

with open("scripts/batch11_solutions.py", "w", encoding="utf-8") as f:
    f.write(BATCH11_CODE.strip() + "\\n")

print(f"Created scripts/batch11_solutions.py successfully!")
