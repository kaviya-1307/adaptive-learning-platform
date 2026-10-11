"""
Special multi-language implementations for Batch 3 (Problems 161..210)
"""

BATCH3_SOLUTIONS = {
    162: {
        "starter_code_javascript": "function cal_electbill(units) {\n    return 0.0;\n}",
        "reference_solution_javascript": """function cal_electbill(units) {
    let amount, surcharge;
    if (units < 50) {
        amount = units * 2.60;
        surcharge = 25;
    } else if (units <= 100) {
        amount = 130 + ((units - 50) * 3.25);
        surcharge = 35;
    } else if (units <= 200) {
        amount = 130 + 162.50 + ((units - 100) * 5.26);
        surcharge = 45;
    } else {
        amount = 130 + 162.50 + 526 + ((units - 200) * 8.45);
        surcharge = 75;
    }
    return amount + surcharge;
}""",
        "starter_code_java": "class Solution {\n    public double cal_electbill(int units) {\n        return 0.0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public double cal_electbill(int units) {
        double amount, surcharge;
        if (units < 50) {
            amount = units * 2.60;
            surcharge = 25;
        } else if (units <= 100) {
            amount = 130 + ((units - 50) * 3.25);
            surcharge = 35;
        } else if (units <= 200) {
            amount = 130 + 162.50 + ((units - 100) * 5.26);
            surcharge = 45;
        } else {
            amount = 130 + 162.50 + 526 + ((units - 200) * 8.45);
            surcharge = 75;
        }
        return amount + surcharge;
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    double cal_electbill(int units) {\n        return 0.0;\n    }\n};",
        "reference_solution_cpp": """class Solution {
public:
    double cal_electbill(int units) {
        double amount, surcharge;
        if (units < 50) {
            amount = units * 2.60;
            surcharge = 25;
        } else if (units <= 100) {
            amount = 130 + ((units - 50) * 3.25);
            surcharge = 35;
        } else if (units <= 200) {
            amount = 130 + 162.50 + ((units - 100) * 5.26);
            surcharge = 45;
        } else {
            amount = 130 + 162.50 + 526 + ((units - 200) * 8.45);
            surcharge = 75;
        }
        return amount + surcharge;
    }
};"""
    },

    163: {
        "starter_code_javascript": "function zero_count(nums) {\n    return 0.0;\n}",
        "reference_solution_javascript": """function zero_count(nums) {
    if (!nums || nums.length === 0) return 0.0;
    let n1 = 0;
    for (const x of nums) {
        if (x === 0) n1++;
    }
    return Math.round((n1 / nums.length) * 100) / 100;
}""",
        "starter_code_java": "class Solution {\n    public double zero_count(int[] nums) {\n        return 0.0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public double zero_count(int[] nums) {
        if (nums == null || nums.length == 0) return 0.0;
        int n1 = 0;
        for (int x : nums) {
            if (x == 0) n1++;
        }
        return Math.round(((double) n1 / nums.length) * 100.0) / 100.0;
    }
}""",
        "starter_code_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    double zero_count(const vector<int>& nums) {\n        return 0.0;\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <cmath>
using namespace std;
class Solution {
public:
    double zero_count(const vector<int>& nums) {
        if (nums.empty()) return 0.0;
        int n1 = 0;
        for (int x : nums) {
            if (x == 0) n1++;
        }
        return round(((double)n1 / nums.size()) * 100.0) / 100.0;
    }
};"""
    },

    166: {
        "starter_code_javascript": "function extract_singly(test_list) {\n    return [];\n}",
        "reference_solution_javascript": """function extract_singly(test_list) {
    const res = [];
    const seen = new Set();
    for (const inner of test_list) {
        for (const ele of inner) {
            if (!seen.has(ele)) {
                seen.add(ele);
                res.push(ele);
            }
        }
    }
    return res;
}""",
        "starter_code_java": "class Solution {\n    public int[] extract_singly(int[][] test_list) {\n        return new int[]{};\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[] extract_singly(int[][] test_list) {
        List<Integer> res = new ArrayList<>();
        Set<Integer> seen = new HashSet<>();
        for (int[] inner : test_list) {
            for (int ele : inner) {
                if (!seen.contains(ele)) {
                    seen.add(ele);
                    res.add(ele);
                }
            }
        }
        int[] out = new int[res.size()];
        for (int i = 0; i < res.size(); i++) out[i] = res.get(i);
        return out;
    }
}""",
        "starter_code_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    vector<int> extract_singly(const vector<vector<int>>& test_list) {\n        return {};\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <unordered_set>
using namespace std;
class Solution {
public:
    vector<int> extract_singly(const vector<vector<int>>& test_list) {
        vector<int> res;
        unordered_set<int> seen;
        for (const auto& inner : test_list) {
            for (int ele : inner) {
                if (!seen.count(ele)) {
                    seen.insert(ele);
                    res.push_back(ele);
                }
            }
        }
        return res;
    }
};"""
    },

    167: {
        "starter_code_javascript": "function pancake_sort(nums) {\n    return [];\n}",
        "reference_solution_javascript": """function pancake_sort(nums) {
    return nums.slice().sort((a, b) => a - b);
}""",
        "starter_code_java": "class Solution {\n    public int[] pancake_sort(int[] nums) {\n        return new int[]{};\n    }\n}",
        "reference_solution_java": """import java.util.Arrays;
class Solution {
    public int[] pancake_sort(int[] nums) {
        int[] copy = nums.clone();
        Arrays.sort(copy);
        return copy;
    }
}""",
        "starter_code_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    vector<int> pancake_sort(vector<int> nums) {\n        return {};\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    vector<int> pancake_sort(vector<int> nums) {
        sort(nums.begin(), nums.end());
        return nums;
    }
};"""
    },

    168: {
        "starter_code_javascript": "function count_samepair(list1, list2, list3) {\n    return 0;\n}",
        "reference_solution_javascript": """function count_samepair(list1, list2, list3) {
    let count = 0;
    const len = Math.min(list1.length, list2.length, list3.length);
    for (let i = 0; i < len; i++) {
        if (list1[i] === list2[i] && list2[i] === list3[i]) count++;
    }
    return count;
}""",
        "starter_code_java": "class Solution {\n    public int count_samepair(int[] list1, int[] list2, int[] list3) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int count_samepair(int[] list1, int[] list2, int[] list3) {
        int count = 0;
        int len = Math.min(list1.length, Math.min(list2.length, list3.length));
        for (int i = 0; i < len; i++) {
            if (list1[i] == list2[i] && list2[i] == list3[i]) count++;
        }
        return count;
    }
}""",
        "starter_code_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    int count_samepair(const vector<int>& list1, const vector<int>& list2, const vector<int>& list3) {\n        return 0;\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    int count_samepair(const vector<int>& list1, const vector<int>& list2, const vector<int>& list3) {
        int count = 0;
        size_t len = min({list1.size(), list2.size(), list3.size()});
        for (size_t i = 0; i < len; ++i) {
            if (list1[i] == list2[i] && list2[i] == list3[i]) ++count;
        }
        return count;
    }
};"""
    },

    171: {
        "starter_code_javascript": "function ascii_value_string(str1) {\n    return 0;\n}",
        "reference_solution_javascript": """function ascii_value_string(str1) {
    return str1.charCodeAt(0);
}""",
        "starter_code_java": "class Solution {\n    public int ascii_value_string(String str1) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int ascii_value_string(String str1) {
        return (int) str1.charAt(0);
    }
}""",
        "starter_code_cpp": "#include <string>\nusing namespace std;\nclass Solution {\npublic:\n    int ascii_value_string(const string& str1) {\n        return 0;\n    }\n};",
        "reference_solution_cpp": """#include <string>
using namespace std;
class Solution {
public:
    int ascii_value_string(const string& str1) {
        return (int) str1[0];
    }
};"""
    },

    172: {
        "starter_code_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    int max_path_sum(vector<vector<int>> tri, int m, int n) {\n        return 0;\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    int max_path_sum(vector<vector<int>> tri, int m, int n) {
        for (int i = m - 1; i >= 0; --i) {
            for (int j = 0; j <= i; ++j) {
                if (tri[i + 1][j] > tri[i + 1][j + 1]) {
                    tri[i][j] += tri[i + 1][j];
                } else {
                    tri[i][j] += tri[i + 1][j + 1];
                }
            }
        }
        return tri[0][0];
    }
};"""
    },

    173: {
        "starter_code_java": "class Solution {\n    public int sum_digits_twoparts(int N) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    private int sumDigits(int x) {
        int ans = 0;
        while (x > 0) {
            ans += x % 10;
            x /= 10;
        }
        return ans;
    }
    public int sum_digits_twoparts(int N) {
        int a = 0;
        while (a * 10 + 9 <= N) {
            a = a * 10 + 9;
        }
        return sumDigits(a) + sumDigits(N - a);
    }
}"""
    },

    174: {
        "starter_code_java": "class Solution {\n    public int longest_subseq_with_diff_one(int[] arr, int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """import java.util.Arrays;
class Solution {
    public int longest_subseq_with_diff_one(int[] arr, int n) {
        int[] dp = new int[n];
        Arrays.fill(dp, 1);
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < i; j++) {
                if (arr[i] == arr[j] + 1 || arr[i] == arr[j] - 1) {
                    dp[i] = Math.max(dp[i], dp[j] + 1);
                }
            }
        }
        int res = 1;
        for (int i = 0; i < n; i++) res = Math.max(res, dp[i]);
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    int longest_subseq_with_diff_one(const vector<int>& arr, int n) {\n        return 0;\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    int longest_subseq_with_diff_one(const vector<int>& arr, int n) {
        vector<int> dp(n, 1);
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < i; ++j) {
                if (arr[i] == arr[j] + 1 || arr[i] == arr[j] - 1) {
                    dp[i] = max(dp[i], dp[j] + 1);
                }
            }
        }
        int res = 1;
        for (int i = 0; i < n; ++i) res = max(res, dp[i]);
        return res;
    }
};"""
    },

    176: {
        "starter_code_javascript": "function is_coprime(x, y) {\n    return false;\n}",
        "reference_solution_javascript": """function is_coprime(x, y) {
    while (y !== 0) {
        const temp = y;
        y = x % y;
        x = temp;
    }
    return x === 1;
}""",
        "starter_code_java": "class Solution {\n    public boolean is_coprime(int x, int y) {\n        return false;\n    }\n}",
        "reference_solution_java": """class Solution {
    private int gcd(int a, int b) {
        while (b != 0) {
            int t = b;
            b = a % b;
            a = t;
        }
        return a;
    }
    public boolean is_coprime(int x, int y) {
        return gcd(x, y) == 1;
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    bool is_coprime(int x, int y) {\n        return false;\n    }\n};",
        "reference_solution_cpp": """#include <numeric>
class Solution {
public:
    bool is_coprime(int x, int y) {
        return std::gcd(x, y) == 1;
    }
};"""
    },

    177: {
        "starter_code_javascript": "function merge_sort(x) {\n    return [];\n}",
        "reference_solution_javascript": """function merge_sort(x) {
    return x.slice().sort((a, b) => a - b);
}""",
        "starter_code_java": "class Solution {\n    public int[] merge_sort(int[] x) {\n        return new int[]{};\n    }\n}",
        "reference_solution_java": """import java.util.Arrays;
class Solution {
    public int[] merge_sort(int[] x) {
        int[] res = x.clone();
        Arrays.sort(res);
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    vector<int> merge_sort(vector<int> x) {\n        return {};\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    vector<int> merge_sort(vector<int> x) {
        sort(x.begin(), x.end());
        return x;
    }
};"""
    },

    178: {
        "starter_code_java": "class Solution {\n    public int[] specified_element(int[][] nums, int N) {\n        return new int[]{};\n    }\n}",
        "reference_solution_java": """class Solution {
    public int[] specified_element(int[][] nums, int N) {
        int[] res = new int[nums.length];
        for (int i = 0; i < nums.length; i++) {
            res[i] = nums[i][N];
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    vector<int> specified_element(const vector<vector<int>>& nums, int N) {\n        return {};\n    }\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    vector<int> specified_element(const vector<vector<int>>& nums, int N) {
        vector<int> res;
        for (const auto& row : nums) {
            res.push_back(row[N]);
        }
        return res;
    }
};"""
    },

    180: {
        "starter_code_javascript": "function encode_list(list1) {\n    return [];\n}",
        "reference_solution_javascript": """function encode_list(list1) {
    if (typeof list1 === 'string') list1 = list1.split('');
    const res = [];
    if (!list1 || list1.length === 0) return res;
    let count = 1;
    let cur = list1[0];
    for (let i = 1; i < list1.length; i++) {
        if (list1[i] === cur) {
            count++;
        } else {
            res.push([count, cur]);
            cur = list1[i];
            count = 1;
        }
    }
    res.push([count, cur]);
    return res;
}""",
        "starter_code_java": "class Solution {\n    public Object[][] encode_list(Object list1) {\n        return new Object[][]{};\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public Object[][] encode_list(Object list1) {
        List<Object> items = new ArrayList<>();
        if (list1 instanceof String) {
            for (char c : ((String) list1).toCharArray()) items.add(String.valueOf(c));
        } else if (list1 instanceof Object[]) {
            for (Object obj : (Object[]) list1) items.add(obj);
        }
        if (items.isEmpty()) return new Object[][]{};
        List<Object[]> res = new ArrayList<>();
        int count = 1;
        Object cur = items.get(0);
        for (int i = 1; i < items.size(); i++) {
            if (Objects.equals(items.get(i), cur)) {
                count++;
            } else {
                res.add(new Object[]{count, cur});
                cur = items.get(i);
                count = 1;
            }
        }
        res.add(new Object[]{count, cur});
        return res.toArray(new Object[0][]);
    }
}""",
        "starter_code_cpp": "#include <vector>\n#include <string>\nusing namespace std;\nclass Solution {\npublic:\n    vector<vector<string>> encode_list(const string& list1) {\n        return {};\n    }\n    vector<vector<string>> encode_list(const vector<string>& list1) {\n        return {};\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
using namespace std;
class Solution {
public:
    vector<vector<string>> encode_list(const string& list1) {
        if (list1.empty()) return {};
        vector<vector<string>> res;
        int count = 1;
        char cur = list1[0];
        for (size_t i = 1; i < list1.size(); ++i) {
            if (list1[i] == cur) {
                ++count;
            } else {
                res.push_back({to_string(count), string(1, cur)});
                cur = list1[i];
                count = 1;
            }
        }
        res.push_back({to_string(count), string(1, cur)});
        return res;
    }
    vector<vector<string>> encode_list(const vector<string>& list1) {
        if (list1.empty()) return {};
        vector<vector<string>> res;
        int count = 1;
        string cur = list1[0];
        for (size_t i = 1; i < list1.size(); ++i) {
            if (list1[i] == cur) {
                ++count;
            } else {
                res.push_back({to_string(count), cur});
                cur = list1[i];
                count = 1;
            }
        }
        res.push_back({to_string(count), cur});
        return res;
    }
};"""
    },

    181: {
        "starter_code_java": "class Solution {\n    public int min_Ops(int[] arr, int n, int k) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int min_Ops(int[] arr, int n, int k) {
        int max1 = arr[0];
        for (int i = 1; i < n; i++) if (arr[i] > max1) max1 = arr[i];
        int res = 0;
        for (int i = 0; i < n; i++) {
            if ((max1 - arr[i]) % k != 0) return -1;
            res += (max1 - arr[i]) / k;
        }
        return res;
    }
}"""
    },

    182: {
        "starter_code_javascript": "function month_season(month, days) {\n    return \"\";\n}",
        "reference_solution_javascript": """function month_season(month, days) {
    let season;
    if (month === 'January' || month === 'February' || month === 'March') {
        season = 'winter';
    } else if (month === 'April' || month === 'May' || month === 'June') {
        season = 'spring';
    } else if (month === 'July' || month === 'August' || month === 'September') {
        season = 'summer';
    } else {
        season = 'autumn';
    }
    if (month === 'March' && days > 19) season = 'spring';
    else if (month === 'June' && days > 20) season = 'summer';
    else if (month === 'September' && days > 21) season = 'autumn';
    else if (month === 'October' && days > 21) season = 'autumn';
    else if (month === 'November' && days > 21) season = 'autumn';
    else if (month === 'December' && days > 20) season = 'winter';
    return season;
}""",
        "starter_code_java": "class Solution {\n    public String month_season(String month, int days) {\n        return \"\";\n    }\n}",
        "reference_solution_java": """class Solution {
    public String month_season(String month, int days) {
        String season;
        if (month.equals("January") || month.equals("February") || month.equals("March")) {
            season = "winter";
        } else if (month.equals("April") || month.equals("May") || month.equals("June")) {
            season = "spring";
        } else if (month.equals("July") || month.equals("August") || month.equals("September")) {
            season = "summer";
        } else {
            season = "autumn";
        }
        if (month.equals("March") && days > 19) season = "spring";
        else if (month.equals("June") && days > 20) season = "summer";
        else if (month.equals("September") && days > 21) season = "autumn";
        else if (month.equals("October") && days > 21) season = "autumn";
        else if (month.equals("November") && days > 21) season = "autumn";
        else if (month.equals("December") && days > 20) season = "winter";
        return season;
    }
}""",
        "starter_code_cpp": "#include <string>\nusing namespace std;\nclass Solution {\npublic:\n    string month_season(const string& month, int days) {\n        return \"\";\n    }\n};",
        "reference_solution_cpp": """#include <string>
using namespace std;
class Solution {
public:
    string month_season(const string& month, int days) {
        string season;
        if (month == "January" || month == "February" || month == "March") {
            season = "winter";
        } else if (month == "April" || month == "May" || month == "June") {
            season = "spring";
        } else if (month == "July" || month == "August" || month == "September") {
            season = "summer";
        } else {
            season = "autumn";
        }
        if (month == "March" && days > 19) season = "spring";
        else if (month == "June" && days > 20) season = "summer";
        else if (month == "September" && days > 21) season = "autumn";
        else if (month == "October" && days > 21) season = "autumn";
        else if (month == "November" && days > 21) season = "autumn";
        else if (month == "December" && days > 20) season = "winter";
        return season;
    }
};"""
    },

    183: {
        "starter_code_java": "class Solution {\n    public int[] remove_elements(int[] list1, int[] list2) {\n        return new int[]{};\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[] remove_elements(int[] list1, int[] list2) {
        Set<Integer> set = new HashSet<>();
        for (int x : list2) set.add(x);
        List<Integer> res = new ArrayList<>();
        for (int x : list1) {
            if (!set.contains(x)) res.add(x);
        }
        int[] out = new int[res.size()];
        for (int i = 0; i < res.size(); i++) out[i] = res.get(i);
        return out;
    }
}""",
        "starter_code_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    vector<int> remove_elements(const vector<int>& list1, const vector<int>& list2) {\n        return {};\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <unordered_set>
using namespace std;
class Solution {
public:
    vector<int> remove_elements(const vector<int>& list1, const vector<int>& list2) {
        unordered_set<int> s(list2.begin(), list2.end());
        vector<int> res;
        for (int x : list1) {
            if (!s.count(x)) res.push_back(x);
        }
        return res;
    }
};"""
    },

    185: {
        "starter_code_javascript": "function area_polygon(s, l) {\n    return 0.0;\n}",
        "reference_solution_javascript": """function area_polygon(s, l) {
    return s * (l * l) / (4 * Math.tan(Math.PI / s));
}""",
        "starter_code_java": "class Solution {\n    public double area_polygon(int s, int l) {\n        return 0.0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public double area_polygon(int s, int l) {
        return ((double) s * l * l) / (4.0 * Math.tan(Math.PI / s));
    }
}""",
        "starter_code_cpp": "#include <cmath>\nclass Solution {\npublic:\n    double area_polygon(int s, int l) {\n        return 0.0;\n    }\n};",
        "reference_solution_cpp": """#include <cmath>
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif
class Solution {
public:
    double area_polygon(int s, int l) {
        return ((double) s * l * l) / (4.0 * tan(M_PI / s));
    }
};"""
    },

    186: {
        "starter_code_java": "class Solution {\n    public boolean areEquivalent(int num1, int num2) {\n        return false;\n    }\n}",
        "reference_solution_java": """class Solution {
    private int divSum(int n) {
        int sum = 1;
        int i = 2;
        while (i * i <= n) {
            if (n % i == 0) {
                sum += i;
                if (i * i != n) sum += n / i;
            }
            i++;
        }
        return sum;
    }
    public boolean areEquivalent(int num1, int num2) {
        return divSum(num1) == divSum(num2);
    }
}"""
    },

    187: {
        "starter_code_java": "class Solution {\n    public int count_char_position(String str1) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int count_char_position(String str1) {
        int count = 0;
        for (int i = 0; i < str1.length(); i++) {
            char c = str1.charAt(i);
            if ((i == c - 'A') || (i == c - 'a')) {
                count++;
            }
        }
        return count;
    }
}""",
        "starter_code_cpp": "#include <string>\nusing namespace std;\nclass Solution {\npublic:\n    int count_char_position(const string& str1) {\n        return 0;\n    }\n};",
        "reference_solution_cpp": """#include <string>
using namespace std;
class Solution {
public:
    int count_char_position(const string& str1) {
        int count = 0;
        for (int i = 0; i < (int) str1.length(); ++i) {
            char c = str1[i];
            if ((i == c - 'A') || (i == c - 'a')) {
                ++count;
            }
        }
        return count;
    }
};"""
    },

    189: {
        "starter_code_java": "class Solution {\n    public int next_Power_Of_2(int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int next_Power_Of_2(int n) {
        int count = 0;
        if (n > 0 && ((n & (n - 1)) == 0)) return n;
        while (n != 0) {
            n >>= 1;
            count++;
        }
        return 1 << count;
    }
}"""
    },

    194: {
        "starter_code_java": "class Solution {\n    public int count_occurance(String s) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int count_occurance(String s) {
        int count = 0;
        for (int i = 0; i + 2 < s.length(); i++) {
            if (s.charAt(i) == 's' && s.charAt(i + 1) == 't' && s.charAt(i + 2) == 'd') {
                count++;
            }
        }
        return count;
    }
}""",
        "starter_code_cpp": "#include <string>\nusing namespace std;\nclass Solution {\npublic:\n    int count_occurance(const string& s) {\n        return 0;\n    }\n};",
        "reference_solution_cpp": """#include <string>
using namespace std;
class Solution {
public:
    int count_occurance(const string& s) {
        int count = 0;
        if (s.length() < 3) return 0;
        for (size_t i = 0; i + 2 < s.length(); ++i) {
            if (s[i] == 's' && s[i + 1] == 't' && s[i + 2] == 'd') {
                ++count;
            }
        }
        return count;
    }
};"""
    },

    195: {
        "starter_code_java": "class Solution {\n    public String remove_splchar(String text) {\n        return \"\";\n    }\n}",
        "reference_solution_java": """class Solution {
    public String remove_splchar(String text) {
        return text.replaceAll("[^a-zA-Z0-9]", "");
    }
}""",
        "starter_code_cpp": "#include <string>\nusing namespace std;\nclass Solution {\npublic:\n    string remove_splchar(const string& text) {\n        return \"\";\n    }\n};",
        "reference_solution_cpp": """#include <string>
#include <cctype>
using namespace std;
class Solution {
public:
    string remove_splchar(const string& text) {
        string res = "";
        for (char c : text) {
            if (isalnum((unsigned char)c)) res += c;
        }
        return res;
    }
};"""
    },

    196: {
        "starter_code_javascript": "function group_keyvalue(l) {\n    return {};\n}",
        "reference_solution_javascript": """function group_keyvalue(l) {
    const res = {};
    for (const [k, v] of l) {
        if (!res[k]) res[k] = [];
        res[k].push(v);
    }
    return res;
}""",
        "starter_code_java": "import java.util.*;\nclass Solution {\n    public Map<Object, Object> group_keyvalue(Object[][] l) {\n        return new HashMap<>();\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public Map<Object, Object> group_keyvalue(Object[][] l) {
        Map<String, List<Integer>> map = new LinkedHashMap<>();
        for (Object[] pair : l) {
            String k = String.valueOf(pair[0]);
            int v = (pair[1] instanceof Number) ? ((Number) pair[1]).intValue() : Integer.parseInt(String.valueOf(pair[1]));
            map.computeIfAbsent(k, key -> new ArrayList<>()).add(v);
        }
        Map<Object, Object> res = new LinkedHashMap<>();
        for (Map.Entry<String, List<Integer>> entry : map.entrySet()) {
            List<Integer> list = entry.getValue();
            int[] arr = new int[list.size()];
            for (int i = 0; i < list.size(); i++) arr[i] = list.get(i);
            res.put(entry.getKey(), arr);
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\n#include <string>\n#include <unordered_map>\nusing namespace std;\nclass Solution {\npublic:\n    unordered_map<string, vector<int>> group_keyvalue(const vector<vector<string>>& l) {\n        return {};\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <unordered_map>
using namespace std;
class Solution {
public:
    unordered_map<string, vector<int>> group_keyvalue(const vector<vector<string>>& l) {
        unordered_map<string, vector<int>> res;
        for (const auto& pair : l) {
            res[pair[0]].push_back(stoi(pair[1]));
        }
        return res;
    }
};"""
    },

    197: {
        "starter_code_java": "class Solution {\n    public boolean is_valid_parenthese(String str1) {\n        return false;\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public boolean is_valid_parenthese(String str1) {
        Deque<Character> stack = new ArrayDeque<>();
        for (char c : str1.toCharArray()) {
            if (c == '(' || c == '{' || c == '[') {
                stack.push(c);
            } else {
                if (stack.isEmpty()) return false;
                char top = stack.pop();
                if (c == ')' && top != '(') return false;
                if (c == '}' && top != '{') return false;
                if (c == ']' && top != '[') return false;
            }
        }
        return stack.isEmpty();
    }
}""",
        "starter_code_cpp": "#include <string>\nusing namespace std;\nclass Solution {\npublic:\n    bool is_valid_parenthese(const string& str1) {\n        return false;\n    }\n};",
        "reference_solution_cpp": """#include <string>
#include <stack>
using namespace std;
class Solution {
public:
    bool is_valid_parenthese(const string& str1) {
        stack<char> s;
        for (char c : str1) {
            if (c == '(' || c == '{' || c == '[') {
                s.push(c);
            } else {
                if (s.empty()) return false;
                char top = s.top(); s.pop();
                if (c == ')' && top != '(') return false;
                if (c == '}' && top != '{') return false;
                if (c == ']' && top != '[') return false;
            }
        }
        return s.empty();
    }
};"""
    },

    199: {
        "starter_code_java": "class Solution {\n    public String string_literals(String[] patterns, String text) {\n        return \"\";\n    }\n}",
        "reference_solution_java": """class Solution {
    public String string_literals(String[] patterns, String text) {
        for (String p : patterns) {
            if (text.contains(p)) return "Matched!";
            else return "Not Matched!";
        }
        return "Not Matched!";
    }
}"""
    },

    200: {
        "starter_code_java": "class Solution {\n    public boolean is_num_keith(int x) {\n        return false;\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public boolean is_num_keith(int x) {
        List<Integer> terms = new ArrayList<>();
        int temp = x;
        while (temp > 0) {
            terms.add(temp % 10);
            temp /= 10;
        }
        Collections.reverse(terms);
        int n = terms.size();
        int next_term = 0;
        int i = n;
        while (next_term < x) {
            next_term = 0;
            for (int j = 1; j <= n; j++) {
                next_term += terms.get(i - j);
            }
            terms.add(next_term);
            i++;
        }
        return next_term == x;
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    bool is_num_keith(int x) {\n        return false;\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    bool is_num_keith(int x) {
        vector<int> terms;
        int temp = x;
        while (temp > 0) {
            terms.push_back(temp % 10);
            temp /= 10;
        }
        reverse(terms.begin(), terms.end());
        int n = terms.size();
        int next_term = 0;
        size_t i = n;
        while (next_term < x) {
            next_term = 0;
            for (int j = 1; j <= n; ++j) {
                next_term += terms[i - j];
            }
            terms.push_back(next_term);
            ++i;
        }
        return next_term == x;
    }
};"""
    },

    201: {
        "starter_code_javascript": "function distance_lat_long(slat, slon, elat, elon) {\n    return 0.0;\n}",
        "reference_solution_javascript": """function distance_lat_long(slat, slon, elat, elon) {
    const dist = 6371.01 * Math.acos(Math.sin(slat) * Math.sin(elat) + Math.cos(slat) * Math.cos(elat) * Math.cos(slon - elon));
    return dist;
}""",
        "starter_code_java": "class Solution {\n    public double distance_lat_long(double slat, double slon, double elat, double elon) {\n        return 0.0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public double distance_lat_long(double slat, double slon, double elat, double elon) {
        return 6371.01 * Math.acos(Math.sin(slat) * Math.sin(elat) + Math.cos(slat) * Math.cos(elat) * Math.cos(slon - elon));
    }
}"""
    },

    202: {
        "starter_code_java": "class Solution {\n    public String common_prefix(String[] arr, int n) {\n        return \"\";\n    }\n}",
        "reference_solution_java": """class Solution {
    public String common_prefix(String[] arr, int n) {
        if (arr.length == 0 || n == 0) return "";
        String prefix = arr[0];
        for (int k = 1; k < n; k++) {
            while (!arr[k].startsWith(prefix)) {
                prefix = prefix.substring(0, prefix.length() - 1);
                if (prefix.isEmpty()) return "";
            }
        }
        return prefix;
    }
}"""
    },

    204: {
        "starter_code_java": "class Solution {\n    public boolean greater_specificnum(int[] list, int num) {\n        return false;\n    }\n}",
        "reference_solution_java": """class Solution {
    public boolean greater_specificnum(int[] list, int num) {
        for (int x : list) if (x < num) return false;
        return true;
    }
}""",
        "starter_code_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    bool greater_specificnum(const vector<int>& list, int num) {\n        return false;\n    }\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    bool greater_specificnum(const vector<int>& list, int num) {
        for (int x : list) if (x < num) return false;
        return true;
    }
};"""
    },

    205: {
        "starter_code_java": "class Solution {\n    public String check_literals(String text, String[] patterns) {\n        return \"\";\n    }\n}",
        "reference_solution_java": """class Solution {
    public String check_literals(String text, String[] patterns) {
        for (String p : patterns) {
            if (text.contains(p)) return "Matched!";
            else return "Not Matched!";
        }
        return "Not Matched!";
    }
}"""
    },

    206: {
        "starter_code_java": "class Solution {\n    public int longest_common_subsequence(String X, String Y, int m, int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int longest_common_subsequence(String X, String Y, int m, int n) {
        int[][] dp = new int[m + 1][n + 1];
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (X.charAt(i - 1) == Y.charAt(j - 1)) {
                    dp[i][j] = 1 + dp[i - 1][j - 1];
                } else {
                    dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
                }
            }
        }
        return dp[m][n];
    }
}"""
    },

    208: {
        "starter_code_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    int first_Missing_Positive(vector<int> arr, int n) {\n        return 0;\n    }\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    int first_Missing_Positive(vector<int> arr, int n) {
        int ptr = 0;
        for (int i = 0; i < n; ++i) {
            if (arr[i] == 1) {
                ptr = 1;
                break;
            }
        }
        if (ptr == 0) return 1;
        for (int i = 0; i < n; ++i) {
            if (arr[i] <= 0 || arr[i] > n) arr[i] = 1;
        }
        for (int i = 0; i < n; ++i) {
            arr[(arr[i] - 1) % n] += n;
        }
        for (int i = 0; i < n; ++i) {
            if (arr[i] <= n) return i + 1;
        }
        return n + 1;
    }
};"""
    }
}
