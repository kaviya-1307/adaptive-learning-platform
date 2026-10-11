"""
Script to create batch9_solutions.py containing curated solutions for Batch 9 (Problems 461-510).
"""

content = '''"""
Curated and specialized solutions for MBPP problems (Batch 9: 461-510).
"""

BATCH9_SOLUTIONS = {
    461: {
        "starter_code_javascript": "function first_Factorial_Divisible_Number(x) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function first_Factorial_Divisible_Number(x) {
    let fact = 1;
    for (let i = 1; i < x; i++) {
        fact = (fact * i) % x;
        if (fact === 0) return i;
    }
    return x - 1;
}""",
        "starter_code_java": "class Solution {\\n    public int first_Factorial_Divisible_Number(int x) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int first_Factorial_Divisible_Number(int x) {
        long fact = 1;
        for (int i = 1; i < x; i++) {
            fact = (fact * i) % x;
            if (fact == 0) return i;
        }
        return x - 1;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int first_Factorial_Divisible_Number(int x);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    int first_Factorial_Divisible_Number(int x) {
        long long fact = 1;
        for (int i = 1; i < x; ++i) {
            fact = (fact * i) % x;
            if (fact == 0) return i;
        }
        return x - 1;
    }
};"""
    },

    462: {
        "starter_code_javascript": "function remove_matching_tuple(test_list1, test_list2) {\\n    return [];\\n}",
        "reference_solution_javascript": """function remove_matching_tuple(test_list1, test_list2) {
    let set2 = new Set(test_list2.map(sub => JSON.stringify(sub)));
    return test_list1.filter(sub => !set2.has(JSON.stringify(sub)));
}""",
        "starter_code_java": "class Solution {\\n    public String[][] remove_matching_tuple(String[][] test_list1, String[][] test_list2) {\\n        return new String[][]{};\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public String[][] remove_matching_tuple(String[][] test_list1, String[][] test_list2) {
        List<String[]> res = new ArrayList<>();
        for (String[] sub1 : test_list1) {
            boolean found = false;
            for (String[] sub2 : test_list2) {
                if (Arrays.equals(sub1, sub2)) {
                    found = true;
                    break;
                }
            }
            if (!found) res.add(sub1);
        }
        return res.toArray(new String[0][]);
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<vector<string>> remove_matching_tuple(const vector<vector<string>>& test_list1, const vector<vector<string>>& test_list2);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
using namespace std;
class Solution {
public:
    vector<vector<string>> remove_matching_tuple(const vector<vector<string>>& test_list1, const vector<vector<string>>& test_list2) {
        vector<vector<string>> res;
        for (const auto& sub1 : test_list1) {
            bool found = false;
            for (const auto& sub2 : test_list2) {
                if (sub1 == sub2) {
                    found = true;
                    break;
                }
            }
            if (!found) res.push_back(sub1);
        }
        return res;
    }
};"""
    },

    463: {
        "starter_code_javascript": "function largest_palindrome(A, n) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function largest_palindrome(A, n) {
    let sorted = [...A].sort((a, b) => a - b);
    for (let i = n - 1; i >= 0; i--) {
        let s = String(sorted[i]);
        if (s === s.split('').reverse().join('')) return sorted[i];
    }
    return -1;
}""",
        "starter_code_java": "class Solution {\\n    public int largest_palindrome(int[] A, int n) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    private boolean isPal(int x) {
        String s = String.valueOf(x);
        return s.equals(new StringBuilder(s).reverse().toString());
    }
    public int largest_palindrome(int[] A, int n) {
        int[] arr = A.clone();
        Arrays.sort(arr);
        for (int i = n - 1; i >= 0; i--) {
            if (isPal(arr[i])) return arr[i];
        }
        return -1;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int largest_palindrome(vector<int> A, int n);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <algorithm>
using namespace std;
class Solution {
public:
    int largest_palindrome(vector<int> A, int n) {
        sort(A.begin(), A.end());
        for (int i = n - 1; i >= 0; --i) {
            string s = to_string(A[i]);
            string rev = s;
            reverse(rev.begin(), rev.end());
            if (s == rev) return A[i];
        }
        return -1;
    }
};"""
    },

    464: {
        "starter_code_javascript": "function sort_tuple(tup) {\\n    return [];\\n}",
        "reference_solution_javascript": """function sort_tuple(tup) {
    return [...tup].sort((a, b) => a[a.length - 1] - b[b.length - 1]);
}""",
        "starter_code_java": "class Solution {\\n    public int[][] sort_tuple(int[][] tup) {\\n        return new int[][]{};\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[][] sort_tuple(int[][] tup) {
        int[][] res = tup.clone();
        Arrays.sort(res, (a, b) -> Integer.compare(a[a.length - 1], b[b.length - 1]));
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<vector<int>> sort_tuple(vector<vector<int>> tup);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    vector<vector<int>> sort_tuple(vector<vector<int>> tup) {
        sort(tup.begin(), tup.end(), [](const vector<int>& a, const vector<int>& b) {
            return a.back() < b.back();
        });
        return tup;
    }
};"""
    },

    467: {
        "starter_code_javascript": "function sum_gp(a, n, r) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function sum_gp(a, n, r) {
    let term = 1;
    let sum = 0;
    for (let i = 0; i < n; i++) {
        sum += a * term;
        term *= r;
    }
    return sum;
}""",
        "starter_code_java": "class Solution {\\n    public int sum_gp(int a, int n, int r) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int sum_gp(int a, int n, int r) {
        long term = 1;
        long sum = 0;
        for (int i = 0; i < n; i++) {
            sum += a * term;
            term *= r;
        }
        return (int) sum;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int sum_gp(int a, int n, int r);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    int sum_gp(int a, int n, int r) {
        long long term = 1;
        long long sum = 0;
        for (int i = 0; i < n; ++i) {
            sum += a * term;
            term *= r;
        }
        return (int) sum;
    }
};"""
    },

    469: {
        "starter_code_javascript": "function binary_to_integer(test_tup) {\\n    return '';\\n}",
        "reference_solution_javascript": """function binary_to_integer(test_tup) {
    let s = test_tup.join("");
    return String(parseInt(s, 2));
}""",
        "starter_code_java": "class Solution {\\n    public String binary_to_integer(int[] test_tup) {\\n        return \\"\\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String binary_to_integer(int[] test_tup) {
        int res = 0;
        for (int b : test_tup) res = (res << 1) | b;
        return String.valueOf(res);
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    string binary_to_integer(const vector<int>& test_tup);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
using namespace std;
class Solution {
public:
    string binary_to_integer(const vector<int>& test_tup) {
        int res = 0;
        for (int b : test_tup) res = (res << 1) | b;
        return to_string(res);
    }
};"""
    },

    470: {
        "starter_code_javascript": "function remove_lowercase(str1) {\\n    return '';\\n}",
        "reference_solution_javascript": """function remove_lowercase(str1) {
    return str1.replace(/[a-z]/g, "");
}""",
        "starter_code_java": "class Solution {\\n    public String remove_lowercase(String str1) {\\n        return \\"\\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String remove_lowercase(String str1) {
        return str1.replaceAll("[a-z]", "");
    }
}""",
        "starter_code_cpp": "#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    string remove_lowercase(const string& str1);\\n};",
        "reference_solution_cpp": """#include <string>
using namespace std;
class Solution {
public:
    string remove_lowercase(const string& str1) {
        string res = "";
        for (char c : str1) if (!(c >= 'a' && c <= 'z')) res += c;
        return res;
    }
};"""
    },

    472: {
        "starter_code_javascript": "function surfacearea_cone(r, h) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function surfacearea_cone(r, h) {
    let l = Math.sqrt(r * r + h * h);
    return Math.PI * r * (r + l);
}""",
        "starter_code_java": "class Solution {\\n    public double surfacearea_cone(int r, int h) {\\n        return 0.0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public double surfacearea_cone(int r, int h) {
        double l = Math.sqrt(r * r + h * h);
        return Math.PI * r * (r + l);
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    double surfacearea_cone(int r, int h);\\n};",
        "reference_solution_cpp": """#include <cmath>
const double PI = 3.14159265358979323846;
class Solution {
public:
    double surfacearea_cone(int r, int h) {
        double l = std::sqrt(r * r + h * h);
        return PI * r * (r + l);
    }
};"""
    },

    476: {
        "starter_code_javascript": "function num_comm_div(x, y) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function num_comm_div(x, y) {
    let g = 1;
    for (let i = 1; i <= Math.min(x, y); i++) {
        if (x % i === 0 && y % i === 0) g = i;
    }
    let count = 0;
    for (let i = 1; i * i <= g; i++) {
        if (g % i === 0) {
            count += (i * i === g) ? 1 : 2;
        }
    }
    return count;
}""",
        "starter_code_java": "class Solution {\\n    public int num_comm_div(int x, int y) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int num_comm_div(int x, int y) {
        int g = 1;
        int min = Math.min(x, y);
        for (int i = 1; i <= min; i++) {
            if (x % i == 0 && y % i == 0) g = i;
        }
        int count = 0;
        for (int i = 1; i * i <= g; i++) {
            if (g % i == 0) {
                count += (i * i == g) ? 1 : 2;
            }
        }
        return count;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int num_comm_div(int x, int y);\\n};",
        "reference_solution_cpp": """#include <algorithm>
using namespace std;
class Solution {
public:
    int num_comm_div(int x, int y) {
        int g = 1;
        int m = min(x, y);
        for (int i = 1; i <= m; ++i) if (x % i == 0 && y % i == 0) g = i;
        int count = 0;
        for (int i = 1; i * i <= g; ++i) {
            if (g % i == 0) count += (i * i == g) ? 1 : 2;
        }
        return count;
    }
};"""
    },

    478: {
        "starter_code_javascript": "function add_consecutive_nums(nums) {\\n    return [];\\n}",
        "reference_solution_javascript": """function add_consecutive_nums(nums) {
    let res = [];
    for (let i = 0; i < nums.length - 1; i++) res.push(nums[i] + nums[i + 1]);
    return res;
}""",
        "starter_code_java": "class Solution {\\n    public int[] add_consecutive_nums(int[] nums) {\\n        return new int[]{};\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int[] add_consecutive_nums(int[] nums) {
        int[] res = new int[nums.length - 1];
        for (int i = 0; i < nums.length - 1; i++) res[i] = nums[i] + nums[i + 1];
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<int> add_consecutive_nums(const vector<int>& nums);\\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    vector<int> add_consecutive_nums(const vector<int>& nums) {
        vector<int> res;
        for (size_t i = 0; i + 1 < nums.size(); ++i) res.push_back(nums[i] + nums[i + 1]);
        return res;
    }
};"""
    },

    480: {
        "starter_code_javascript": "function re_order(A) {\\n    return [];\\n}",
        "reference_solution_javascript": """function re_order(A) {
    let nonZero = A.filter(x => x !== 0);
    while (nonZero.length < A.length) nonZero.push(0);
    return nonZero;
}""",
        "starter_code_java": "class Solution {\\n    public int[] re_order(int[] A) {\\n        return new int[]{};\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int[] re_order(int[] A) {
        int[] res = new int[A.length];
        int k = 0;
        for (int x : A) if (x != 0) res[k++] = x;
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<int> re_order(vector<int> A);\\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    vector<int> re_order(vector<int> A) {
        vector<int> res(A.size(), 0);
        size_t k = 0;
        for (int x : A) if (x != 0) res[k++] = x;
        return res;
    }
};"""
    },

    481: {
        "starter_code_javascript": "function permutation_coefficient(n, k) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function permutation_coefficient(n, k) {
    let p = 1;
    for (let i = 0; i < k; i++) p *= (n - i);
    return p;
}""",
        "starter_code_java": "class Solution {\\n    public int permutation_coefficient(int n, int k) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int permutation_coefficient(int n, int k) {
        int p = 1;
        for (int i = 0; i < k; i++) p *= (n - i);
        return p;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int permutation_coefficient(int n, int k);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    int permutation_coefficient(int n, int k) {
        int p = 1;
        for (int i = 0; i < k; ++i) p *= (n - i);
        return p;
    }
};"""
    },

    482: {
        "starter_code_javascript": "function remove_words(list1, removewords) {\\n    return [];\\n}",
        "reference_solution_javascript": """function remove_words(list1, removewords) {
    let rem = new Set(removewords);
    return list1.filter(x => !rem.has(x));
}""",
        "starter_code_java": "class Solution {\\n    public String[] remove_words(String[] list1, String[] removewords) {\\n        return new String[]{};\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public String[] remove_words(String[] list1, String[] removewords) {
        Set<String> rem = new HashSet<>(Arrays.asList(removewords));
        List<String> res = new ArrayList<>();
        for (String w : list1) if (!rem.contains(w)) res.add(w);
        return res.toArray(new String[0]);
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<string> remove_words(const vector<string>& list1, const vector<string>& removewords);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <unordered_set>
using namespace std;
class Solution {
public:
    vector<string> remove_words(const vector<string>& list1, const vector<string>& removewords) {
        unordered_set<string> rem(removewords.begin(), removewords.end());
        vector<string> res;
        for (const auto& w : list1) if (!rem.count(w)) res.push_back(w);
        return res;
    }
};"""
    },

    483: {
        "starter_code_javascript": "function same_order(l1, l2) {\\n    return false;\\n}",
        "reference_solution_javascript": """function same_order(l1, l2) {
    let s1 = new Set(l1), s2 = new Set(l2);
    let common = new Set([...s1].filter(x => s2.has(x)));
    let f1 = l1.filter(x => common.has(x));
    let f2 = l2.filter(x => common.has(x));
    if (f1.length !== f2.length) return false;
    for (let i = 0; i < f1.length; i++) if (f1[i] !== f2[i]) return false;
    return true;
}""",
        "starter_code_java": "class Solution {\\n    public boolean same_order(String[] l1, String[] l2) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public boolean same_order(String[] l1, String[] l2) {
        Set<String> s1 = new HashSet<>(Arrays.asList(l1));
        Set<String> s2 = new HashSet<>(Arrays.asList(l2));
        Set<String> common = new HashSet<>(s1);
        common.retainAll(s2);
        List<String> f1 = new ArrayList<>();
        for (String s : l1) if (common.contains(s)) f1.add(s);
        List<String> f2 = new ArrayList<>();
        for (String s : l2) if (common.contains(s)) f2.add(s);
        return f1.equals(f2);
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    bool same_order(const vector<string>& l1, const vector<string>& l2);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <unordered_set>
using namespace std;
class Solution {
public:
    bool same_order(const vector<string>& l1, const vector<string>& l2) {
        unordered_set<string> s1(l1.begin(), l1.end());
        unordered_set<string> s2(l2.begin(), l2.end());
        unordered_set<string> common;
        for (const auto& s : s1) if (s2.count(s)) common.insert(s);
        vector<string> f1, f2;
        for (const auto& s : l1) if (common.count(s)) f1.push_back(s);
        for (const auto& s : l2) if (common.count(s)) f2.push_back(s);
        return f1 == f2;
    }
};"""
    },

    484: {
        "starter_code_javascript": "function average_Odd(n) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function average_Odd(n) {
    return Math.floor((1 + n) / 2);
}""",
        "starter_code_java": "class Solution {\\n    public int average_Odd(int n) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int average_Odd(int n) {
        return (1 + n) / 2;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int average_Odd(int n);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    int average_Odd(int n) {
        return (1 + n) / 2;
    }
};"""
    },

    485: {
        "starter_code_javascript": "function no_of_subsequences(arr, k) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function no_of_subsequences(arr, k) {
    let n = arr.length;
    let dp = Array.from({length: k + 1}, () => new Array(n + 1).fill(0));
    for (let i = 1; i <= k; i++) {
        for (let j = 1; j <= n; j++) {
            dp[i][j] = dp[i][j - 1];
            if (arr[j - 1] <= i && arr[j - 1] > 0) {
                dp[i][j] += dp[Math.floor(i / arr[j - 1])][j - 1] + 1;
            }
        }
    }
    return dp[k][n];
}""",
        "starter_code_java": "class Solution {\\n    public int no_of_subsequences(int[] arr, int k) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int no_of_subsequences(int[] arr, int k) {
        int n = arr.length;
        int[][] dp = new int[k + 1][n + 1];
        for (int i = 1; i <= k; i++) {
            for (int j = 1; j <= n; j++) {
                dp[i][j] = dp[i][j - 1];
                if (arr[j - 1] <= i && arr[j - 1] > 0) {
                    dp[i][j] += dp[i / arr[j - 1]][j - 1] + 1;
                }
            }
        }
        return dp[k][n];
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int no_of_subsequences(const vector<int>& arr, int k);\\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    int no_of_subsequences(const vector<int>& arr, int k) {
        int n = arr.size();
        vector<vector<int>> dp(k + 1, vector<int>(n + 1, 0));
        for (int i = 1; i <= k; ++i) {
            for (int j = 1; j <= n; ++j) {
                dp[i][j] = dp[i][j - 1];
                if (arr[j - 1] <= i && arr[j - 1] > 0) {
                    dp[i][j] += dp[i / arr[j - 1]][j - 1] + 1;
                }
            }
        }
        return dp[k][n];
    }
};"""
    },

    487: {
        "starter_code_javascript": "function add_str(test_tup, K) {\\n    return [];\\n}",
        "reference_solution_javascript": """function add_str(test_tup, K) {
    let res = [];
    for (let x of test_tup) {
        res.push(x);
        res.push(K);
    }
    return res;
}""",
        "starter_code_java": "class Solution {\\n    public Object[] add_str(int[] test_tup, String K) {\\n        return new Object[]{};\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public Object[] add_str(int[] test_tup, String K) {
        Object[] res = new Object[test_tup.length * 2];
        for (int i = 0; i < test_tup.length; i++) {
            res[i * 2] = test_tup[i];
            res[i * 2 + 1] = K;
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<string> add_str(const vector<int>& test_tup, const string& K);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
using namespace std;
class Solution {
public:
    vector<string> add_str(const vector<int>& test_tup, const string& K) {
        vector<string> res;
        for (int x : test_tup) {
            res.push_back(to_string(x));
            res.push_back(K);
        }
        return res;
    }
};"""
    },

    488: {
        "starter_code_javascript": "function sum_elements(test_tup) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function sum_elements(test_tup) {
    return test_tup.reduce((a, b) => a + b, 0);
}""",
        "starter_code_java": "class Solution {\\n    public int sum_elements(int[] test_tup) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int sum_elements(int[] test_tup) {
        int s = 0;
        for (int x : test_tup) s += x;
        return s;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int sum_elements(const vector<int>& test_tup);\\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    int sum_elements(const vector<int>& test_tup) {
        int s = 0;
        for (int x : test_tup) s += x;
        return s;
    }
};"""
    },

    489: {
        "starter_code_javascript": "function modular_sum(arr, n, m) {\\n    return false;\\n}",
        "reference_solution_javascript": """function modular_sum(arr, n, m) {
    if (n > m) return true;
    let DP = new Array(m).fill(false);
    for (let i = 0; i < n; i++) {
        if (DP[0]) return true;
        let temp = new Array(m).fill(false);
        for (let j = 0; j < m; j++) {
            if (DP[j]) {
                if (!DP[(j + arr[i]) % m]) temp[(j + arr[i]) % m] = true;
            }
        }
        for (let j = 0; j < m; j++) if (temp[j]) DP[j] = true;
        DP[arr[i] % m] = true;
    }
    return DP[0];
}""",
        "starter_code_java": "class Solution {\\n    public boolean modular_sum(int[] arr, int n, int m) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public boolean modular_sum(int[] arr, int n, int m) {
        if (n > m) return true;
        boolean[] DP = new boolean[m];
        for (int i = 0; i < n; i++) {
            if (DP[0]) return true;
            boolean[] temp = new boolean[m];
            for (int j = 0; j < m; j++) {
                if (DP[j]) {
                    if (!DP[(j + arr[i]) % m]) temp[(j + arr[i]) % m] = true;
                }
            }
            for (int j = 0; j < m; j++) if (temp[j]) DP[j] = true;
            DP[arr[i] % m] = true;
        }
        return DP[0];
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    bool modular_sum(const vector<int>& arr, int n, int m);\\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    bool modular_sum(const vector<int>& arr, int n, int m) {
        if (n > m) return true;
        vector<bool> DP(m, false);
        for (int i = 0; i < n; ++i) {
            if (DP[0]) return true;
            vector<bool> temp(m, false);
            for (int j = 0; j < m; ++j) {
                if (DP[j]) {
                    if (!DP[(j + arr[i]) % m]) temp[(j + arr[i]) % m] = true;
                }
            }
            for (int j = 0; j < m; ++j) if (temp[j]) DP[j] = true;
            DP[arr[i] % m] = true;
        }
        return DP[0];
    }
};"""
    },

    490: {
        "starter_code_javascript": "function radix_sort(nums) {\\n    return [];\\n}",
        "reference_solution_javascript": """function radix_sort(nums) {
    return [...nums].sort((a, b) => a - b);
}""",
        "starter_code_java": "class Solution {\\n    public int[] radix_sort(int[] nums) {\\n        return new int[]{};\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[] radix_sort(int[] nums) {
        int[] res = nums.clone();
        Arrays.sort(res);
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<int> radix_sort(vector<int> nums);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    vector<int> radix_sort(vector<int> nums) {
        sort(nums.begin(), nums.end());
        return nums;
    }
};"""
    },

    492: {
        "starter_code_javascript": "function sqrt_root(num) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function sqrt_root(num) {
    return Math.sqrt(num);
}""",
        "starter_code_java": "class Solution {\\n    public double sqrt_root(int num) {\\n        return 0.0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public double sqrt_root(int num) {
        return Math.sqrt(num);
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    double sqrt_root(int num);\\n};",
        "reference_solution_cpp": """#include <cmath>
class Solution {
public:
    double sqrt_root(int num) {
        return std::sqrt(num);
    }
};"""
    },

    493: {
        "starter_code_javascript": "function volume_tetrahedron(num) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function volume_tetrahedron(num) {
    let vol = (Math.pow(num, 3)) / (6 * Math.sqrt(2));
    return Math.round(vol * 100) / 100;
}""",
        "starter_code_java": "class Solution {\\n    public double volume_tetrahedron(int num) {\\n        return 0.0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public double volume_tetrahedron(int num) {
        double vol = Math.pow(num, 3) / (6.0 * Math.sqrt(2.0));
        return Math.round(vol * 100.0) / 100.0;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    double volume_tetrahedron(int num);\\n};",
        "reference_solution_cpp": """#include <cmath>
class Solution {
public:
    double volume_tetrahedron(int num) {
        double vol = std::pow(num, 3) / (6.0 * std::sqrt(2.0));
        return std::round(vol * 100.0) / 100.0;
    }
};"""
    },

    494: {
        "starter_code_javascript": "function get_lcm(l) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function get_lcm(l) {
    const gcd = (a, b) => b === 0 ? a : gcd(b, a % b);
    const lcm = (a, b) => Math.floor((a * b) / gcd(a, b));
    let res = l[0];
    for (let i = 1; i < l.length; i++) res = lcm(res, l[i]);
    return res;
}""",
        "starter_code_java": "class Solution {\\n    public int get_lcm(int[] l) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    private long gcd(long a, long b) { return b == 0 ? a : gcd(b, a % b); }
    private long lcm(long a, long b) { return (a * b) / gcd(a, b); }
    public int get_lcm(int[] l) {
        long res = l[0];
        for (int i = 1; i < l.length; i++) res = lcm(res, l[i]);
        return (int) res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int get_lcm(const vector<int>& l);\\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
    long long gcd(long long a, long long b) { return b == 0 ? a : gcd(b, a % b); }
    long long lcm(long long a, long long b) { return (a * b) / gcd(a, b); }
public:
    int get_lcm(const vector<int>& l) {
        long long res = l[0];
        for (size_t i = 1; i < l.size(); ++i) res = lcm(res, l[i]);
        return (int) res;
    }
};"""
    },

    496: {
        "starter_code_javascript": "function lbs(arr) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function lbs(arr) {
    let n = arr.length;
    let lis = new Array(n).fill(1);
    for (let i = 1; i < n; i++) {
        for (let j = 0; j < i; j++) {
            if (arr[i] > arr[j] && lis[i] < lis[j] + 1) lis[i] = lis[j] + 1;
        }
    }
    let lds = new Array(n).fill(1);
    for (let i = n - 2; i >= 0; i--) {
        for (let j = n - 1; j > i; j--) {
            if (arr[i] > arr[j] && lds[i] < lds[j] + 1) lds[i] = lds[j] + 1;
        }
    }
    let maxVal = 0;
    for (let i = 0; i < n; i++) {
        let cur = lis[i] + lds[i] - 1;
        if (cur > maxVal) maxVal = cur;
    }
    return maxVal;
}""",
        "starter_code_java": "class Solution {\\n    public int lbs(int[] arr) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int lbs(int[] arr) {
        int n = arr.length;
        int[] lis = new int[n];
        for (int i = 0; i < n; i++) lis[i] = 1;
        for (int i = 1; i < n; i++) {
            for (int j = 0; j < i; j++) {
                if (arr[i] > arr[j] && lis[i] < lis[j] + 1) lis[i] = lis[j] + 1;
            }
        }
        int[] lds = new int[n];
        for (int i = 0; i < n; i++) lds[i] = 1;
        for (int i = n - 2; i >= 0; i--) {
            for (int j = n - 1; j > i; j--) {
                if (arr[i] > arr[j] && lds[i] < lds[j] + 1) lds[i] = lds[j] + 1;
            }
        }
        int maxVal = 0;
        for (int i = 0; i < n; i++) {
            int cur = lis[i] + lds[i] - 1;
            if (cur > maxVal) maxVal = cur;
        }
        return maxVal;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int lbs(const vector<int>& arr);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    int lbs(const vector<int>& arr) {
        int n = arr.size();
        vector<int> lis(n, 1);
        for (int i = 1; i < n; ++i) {
            for (int j = 0; j < i; ++j) {
                if (arr[i] > arr[j] && lis[i] < lis[j] + 1) lis[i] = lis[j] + 1;
            }
        }
        vector<int> lds(n, 1);
        for (int i = n - 2; i >= 0; --i) {
            for (int j = n - 1; j > i; --j) {
                if (arr[i] > arr[j] && lds[i] < lds[j] + 1) lds[i] = lds[j] + 1;
            }
        }
        int maxVal = 0;
        for (int i = 0; i < n; ++i) {
            maxVal = max(maxVal, lis[i] + lds[i] - 1);
        }
        return maxVal;
    }
};"""
    },

    497: {
        "starter_code_javascript": "function check_string(str1) {\\n    return [];\\n}",
        "reference_solution_javascript": """function check_string(str1) {
    let res = [];
    if (!/[A-Z]/.test(str1)) res.push('String must have 1 upper case character.');
    if (!/[a-z]/.test(str1)) res.push('String must have 1 lower case character.');
    if (!/[0-9]/.test(str1)) res.push('String must have 1 number.');
    if (str1.length < 7) res.push('String length should be atleast 8.');
    if (res.length === 0) res.push('Valid string.');
    return res;
}""",
        "starter_code_java": "class Solution {\\n    public String[] check_string(String str1) {\\n        return new String[]{};\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public String[] check_string(String str1) {
        List<String> res = new ArrayList<>();
        boolean hasUpper = false, hasLower = false, hasDigit = false;
        for (char c : str1.toCharArray()) {
            if (Character.isUpperCase(c)) hasUpper = true;
            if (Character.isLowerCase(c)) hasLower = true;
            if (Character.isDigit(c)) hasDigit = true;
        }
        if (!hasUpper) res.add("String must have 1 upper case character.");
        if (!hasLower) res.add("String must have 1 lower case character.");
        if (!hasDigit) res.add("String must have 1 number.");
        if (str1.length() < 7) res.add("String length should be atleast 8.");
        if (res.isEmpty()) res.add("Valid string.");
        return res.toArray(new String[0]);
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<string> check_string(const string& str1);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <cctype>
using namespace std;
class Solution {
public:
    vector<string> check_string(const string& str1) {
        vector<string> res;
        bool hasUpper = false, hasLower = false, hasDigit = false;
        for (char c : str1) {
            if (isupper((unsigned char)c)) hasUpper = true;
            if (islower((unsigned char)c)) hasLower = true;
            if (isdigit((unsigned char)c)) hasDigit = true;
        }
        if (!hasUpper) res.push_back("String must have 1 upper case character.");
        if (!hasLower) res.push_back("String must have 1 lower case character.");
        if (!hasDigit) res.push_back("String must have 1 number.");
        if (str1.length() < 7) res.push_back("String length should be atleast 8.");
        if (res.empty()) res.push_back("Valid string.");
        return res;
    }
};"""
    },

    498: {
        "starter_code_javascript": "function max_sum_increasing_subsequence(arr, n) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function max_sum_increasing_subsequence(arr, n) {
    let msis = [...arr];
    for (let i = 1; i < n; i++) {
        for (let j = 0; j < i; j++) {
            if (arr[i] > arr[j] && msis[i] < msis[j] + arr[i]) {
                msis[i] = msis[j] + arr[i];
            }
        }
    }
    return Math.max(...msis);
}""",
        "starter_code_java": "class Solution {\\n    public int max_sum_increasing_subsequence(int[] arr, int n) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int max_sum_increasing_subsequence(int[] arr, int n) {
        int[] msis = arr.clone();
        for (int i = 1; i < n; i++) {
            for (int j = 0; j < i; j++) {
                if (arr[i] > arr[j] && msis[i] < msis[j] + arr[i]) {
                    msis[i] = msis[j] + arr[i];
                }
            }
        }
        int maxVal = msis[0];
        for (int i = 1; i < n; i++) if (msis[i] > maxVal) maxVal = msis[i];
        return maxVal;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int max_sum_increasing_subsequence(const vector<int>& arr, int n);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    int max_sum_increasing_subsequence(const vector<int>& arr, int n) {
        vector<int> msis = arr;
        for (int i = 1; i < n; ++i) {
            for (int j = 0; j < i; ++j) {
                if (arr[i] > arr[j] && msis[i] < msis[j] + arr[i]) {
                    msis[i] = msis[j] + arr[i];
                }
            }
        }
        return *max_element(msis.begin(), msis.end());
    }
};"""
    },

    500: {
        "starter_code_javascript": "function capitalize_first_last_letters(str1) {\\n    return '';\\n}",
        "reference_solution_javascript": """function capitalize_first_last_letters(str1) {
    return str1.split(" ").map(w => {
        if (w.length === 1) return w.toUpperCase();
        return w[0].toUpperCase() + w.slice(1, -1) + w[w.length - 1].toUpperCase();
    }).join(" ");
}""",
        "starter_code_java": "class Solution {\\n    public String capitalize_first_last_letters(String str1) {\\n        return \\"\\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String capitalize_first_last_letters(String str1) {
        String[] words = str1.split(" ");
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < words.length; i++) {
            if (i > 0) sb.append(" ");
            String w = words[i];
            if (w.length() == 1) {
                sb.append(Character.toUpperCase(w.charAt(0)));
            } else {
                sb.append(Character.toUpperCase(w.charAt(0)))
                  .append(w.substring(1, w.length() - 1))
                  .append(Character.toUpperCase(w.charAt(w.length() - 1)));
            }
        }
        return sb.toString();
    }
}""",
        "starter_code_cpp": "#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    string capitalize_first_last_letters(const string& str1);\\n};",
        "reference_solution_cpp": """#include <string>
#include <sstream>
#include <cctype>
using namespace std;
class Solution {
public:
    string capitalize_first_last_letters(const string& str1) {
        istringstream iss(str1);
        string word, res;
        bool first = true;
        while (iss >> word) {
            if (!first) res += " ";
            first = false;
            if (word.length() == 1) {
                word[0] = toupper((unsigned char)word[0]);
            } else {
                word[0] = toupper((unsigned char)word[0]);
                word.back() = toupper((unsigned char)word.back());
            }
            res += word;
        }
        return res;
    }
};"""
    },

    503: {
        "starter_code_javascript": "function negative_count(nums) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function negative_count(nums) {
    let count = nums.filter(x => x < 0).length;
    return Math.round((count / nums.length) * 100) / 100;
}""",
        "starter_code_java": "class Solution {\\n    public double negative_count(int[] nums) {\\n        return 0.0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public double negative_count(int[] nums) {
        int count = 0;
        for (int x : nums) if (x < 0) count++;
        return Math.round((count * 1.0 / nums.length) * 100.0) / 100.0;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    double negative_count(const vector<int>& nums);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <cmath>
using namespace std;
class Solution {
public:
    double negative_count(const vector<int>& nums) {
        int count = 0;
        for (int x : nums) if (x < 0) count++;
        return round((static_cast<double>(count) / nums.size()) * 100.0) / 100.0;
    }
};"""
    },

    504: {
        "starter_code_javascript": "function min_coins(coins, m, V) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function min_coins(coins, m, V) {
    let dp = new Array(V + 1).fill(Infinity);
    dp[0] = 0;
    for (let i = 1; i <= V; i++) {
        for (let j = 0; j < m; j++) {
            if (coins[j] <= i && dp[i - coins[j]] !== Infinity) {
                dp[i] = Math.min(dp[i], dp[i - coins[j]] + 1);
            }
        }
    }
    return dp[V] === Infinity ? -1 : dp[V];
}""",
        "starter_code_java": "class Solution {\\n    public int min_coins(int[] coins, int m, int V) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int min_coins(int[] coins, int m, int V) {
        int[] dp = new int[V + 1];
        Arrays.fill(dp, 1000000);
        dp[0] = 0;
        for (int i = 1; i <= V; i++) {
            for (int j = 0; j < m; j++) {
                if (coins[j] <= i) {
                    dp[i] = Math.min(dp[i], dp[i - coins[j]] + 1);
                }
            }
        }
        return dp[V] >= 1000000 ? -1 : dp[V];
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int min_coins(const vector<int>& coins, int m, int V);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    int min_coins(const vector<int>& coins, int m, int V) {
        vector<int> dp(V + 1, 1000000);
        dp[0] = 0;
        for (int i = 1; i <= V; ++i) {
            for (int j = 0; j < m; ++j) {
                if (coins[j] <= i) {
                    dp[i] = min(dp[i], dp[i - coins[j]] + 1);
                }
            }
        }
        return dp[V] >= 1000000 ? -1 : dp[V];
    }
};"""
    },

    505: {
        "starter_code_javascript": "function check_permutation(str1, str2) {\\n    return false;\\n}",
        "reference_solution_javascript": """function check_permutation(str1, str2) {
    if (str1.length !== str2.length) return false;
    return str1.split('').sort().join('') === str2.split('').sort().join('');
}""",
        "starter_code_java": "class Solution {\\n    public boolean check_permutation(String str1, String str2) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public boolean check_permutation(String str1, String str2) {
        if (str1.length() != str2.length()) return false;
        char[] c1 = str1.toCharArray();
        char[] c2 = str2.toCharArray();
        Arrays.sort(c1);
        Arrays.sort(c2);
        return Arrays.equals(c1, c2);
    }
}""",
        "starter_code_cpp": "#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    bool check_permutation(string str1, string str2);\\n};",
        "reference_solution_cpp": """#include <string>
#include <algorithm>
using namespace std;
class Solution {
public:
    bool check_permutation(string str1, string str2) {
        if (str1.length() != str2.length()) return false;
        sort(str1.begin(), str1.end());
        sort(str2.begin(), str2.end());
        return str1 == str2;
    }
};"""
    },

    507: {
        "starter_code_javascript": "function nth_items(list, n) {\\n    return [];\\n}",
        "reference_solution_javascript": """function nth_items(list, n) {
    let res = [];
    for (let i = 0; i < list.length; i += n) res.push(list[i]);
    return res;
}""",
        "starter_code_java": "class Solution {\\n    public int[] nth_items(int[] list, int n) {\\n        return new int[]{};\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int[] nth_items(int[] list, int n) {
        int len = (list.length + n - 1) / n;
        int[] res = new int[len];
        int idx = 0;
        for (int i = 0; i < list.length; i += n) res[idx++] = list[i];
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<int> nth_items(const vector<int>& list, int n);\\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    vector<int> nth_items(const vector<int>& list, int n) {
        vector<int> res;
        for (size_t i = 0; i < list.size(); i += n) res.push_back(list[i]);
        return res;
    }
};"""
    },

    508: {
        "starter_code_javascript": "function first_repeated_word(str1) {\\n    return '';\\n}",
        "reference_solution_javascript": """function first_repeated_word(str1) {
    let seen = new Set();
    for (let w of str1.split(" ")) {
        if (seen.has(w)) return w;
        seen.add(w);
    }
    return "None";
}""",
        "starter_code_java": "class Solution {\\n    public String first_repeated_word(String str1) {\\n        return \\"\\";\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public String first_repeated_word(String str1) {
        Set<String> seen = new HashSet<>();
        for (String w : str1.split(" ")) {
            if (seen.contains(w)) return w;
            seen.add(w);
        }
        return "None";
    }
}""",
        "starter_code_cpp": "#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    string first_repeated_word(const string& str1);\\n};",
        "reference_solution_cpp": """#include <string>
#include <sstream>
#include <unordered_set>
using namespace std;
class Solution {
public:
    string first_repeated_word(const string& str1) {
        unordered_set<string> seen;
        istringstream iss(str1);
        string w;
        while (iss >> w) {
            if (seen.count(w)) return w;
            seen.insert(w);
        }
        return "None";
    }
};"""
    },

    509: {
        "starter_code_javascript": "function basesnum_coresspondingnum(bases_num, index) {\\n    return [];\\n}",
        "reference_solution_javascript": """function basesnum_coresspondingnum(bases_num, index) {
    return bases_num.map((b, i) => Math.pow(b, index[i]));
}""",
        "starter_code_java": "import java.math.BigInteger;\\nclass Solution {\\n    public BigInteger[] basesnum_coresspondingnum(int[] bases_num, int[] index) {\\n        return new BigInteger[]{};\\n    }\\n}",
        "reference_solution_java": """import java.math.BigInteger;
class Solution {
    public BigInteger[] basesnum_coresspondingnum(int[] bases_num, int[] index) {
        BigInteger[] res = new BigInteger[bases_num.length];
        for (int i = 0; i < bases_num.length; i++) {
            res[i] = BigInteger.valueOf(bases_num[i]).pow(index[i]);
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<string> basesnum_coresspondingnum(const vector<int>& bases_num, const vector<int>& index);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <algorithm>
using namespace std;

static string big_mul(const string& num, int m) {
    if (m == 0 || num == "0") return "0";
    string res = "";
    int carry = 0;
    for (int i = (int)num.size() - 1; i >= 0; --i) {
        long long prod = (long long)(num[i] - '0') * m + carry;
        res.push_back((char)('0' + (prod % 10)));
        carry = prod / 10;
    }
    while (carry > 0) {
        res.push_back((char)('0' + (carry % 10)));
        carry /= 10;
    }
    reverse(res.begin(), res.end());
    return res;
}

static string big_pow(int base, int exp) {
    if (exp == 0) return "1";
    string res = "1";
    for (int i = 0; i < exp; ++i) {
        res = big_mul(res, base);
    }
    return res;
}

class Solution {
public:
    vector<string> basesnum_coresspondingnum(const vector<int>& bases_num, const vector<int>& index) {
        vector<string> res;
        for (size_t i = 0; i < bases_num.size(); ++i) {
            res.push_back(big_pow(bases_num[i], index[i]));
        }
        return res;
    }
};"""
    },

    510: {
        "starter_code_javascript": "function find_Diff(arr, n) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function find_Diff(arr, n) {
    let a = [...arr].sort((x, y) => x - y);
    let count = 0, max_count = 0, min_count = n;
    for (let i = 0; i < n - 1; i++) {
        if (a[i] === a[i + 1]) {
            count++;
            continue;
        } else {
            max_count = Math.max(max_count, count);
            min_count = Math.min(min_count, count);
            count = 0;
        }
    }
    return max_count - min_count;
}""",
        "starter_code_java": "class Solution {\\n    public int find_Diff(int[] arr, int n) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int find_Diff(int[] arr, int n) {
        int[] a = arr.clone();
        Arrays.sort(a);
        int count = 0, max_count = 0, min_count = n;
        for (int i = 0; i < n - 1; i++) {
            if (a[i] == a[i + 1]) {
                count++;
                continue;
            } else {
                max_count = Math.max(max_count, count);
                min_count = Math.min(min_count, count);
                count = 0;
            }
        }
        return max_count - min_count;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int find_Diff(vector<int> arr, int n);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    int find_Diff(vector<int> arr, int n) {
        sort(arr.begin(), arr.end());
        int count = 0, max_count = 0, min_count = n;
        for (int i = 0; i < n - 1; ++i) {
            if (arr[i] == arr[i + 1]) {
                count++;
                continue;
            } else {
                max_count = max(max_count, count);
                min_count = min(min_count, count);
                count = 0;
            }
        }
        return max_count - min_count;
    }
};"""
    }
}
'''

with open("scripts/batch9_solutions.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Created scripts/batch9_solutions.py successfully!")
