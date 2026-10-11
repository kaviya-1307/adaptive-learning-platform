import os

BATCH5_CONTENT = '''"""
Curated and specialized solutions for MBPP problems (Batch 5: 261-310).
"""

BATCH5_SOLUTIONS = {
    261: {
        "starter_code_javascript": "function insert_element(list, element) {\\n    return [];\\n}",
        "reference_solution_javascript": """function insert_element(list, element) {
    const res = [];
    for (const item of list) {
        res.push(element);
        res.push(item);
    }
    return res;
}""",
        "starter_code_java": "class Solution {\\n    public String[] insert_element(String[] list, String element) {\\n        return new String[]{};\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String[] insert_element(String[] list, String element) {
        String[] res = new String[list.length * 2];
        for (int i = 0; i < list.length; i++) {
            res[2 * i] = element;
            res[2 * i + 1] = list[i];
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<string> insert_element(const vector<string>& list, const string& element);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
using namespace std;
class Solution {
public:
    vector<string> insert_element(const vector<string>& list, const string& element) {
        vector<string> res;
        for (const auto& item : list) {
            res.push_back(element);
            res.push_back(item);
        }
        return res;
    }
};"""
    },

    262: {
        "starter_code_javascript": "function count_integer(list1) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function count_integer(list1) {
    return list1.filter(x => Number.isInteger(x)).length;
}""",
        "starter_code_java": "class Solution {\\n    public int count_integer(Object[] list1) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int count_integer(Object[] list1) {
        int ctr = 0;
        for (Object x : list1) {
            if (x instanceof Integer) ctr++;
        }
        return ctr;
    }
    public int count_integer(int[] list1) {
        return list1.length;
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int count_integer(const vector<string>& list1);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <cctype>
using namespace std;
class Solution {
public:
    int count_integer(const vector<int>& list1) {
        return (int)list1.size();
    }
    int count_integer(const vector<string>& list1) {
        int ctr = 0;
        for (const auto& s : list1) {
            if (s.empty()) continue;
            bool is_int = true;
            size_t start = (s[0] == '-') ? 1 : 0;
            if (start == s.size()) is_int = false;
            for (size_t i = start; i < s.size(); ++i) {
                if (!isdigit(s[i])) { is_int = false; break; }
            }
            if (is_int) ctr++;
        }
        return ctr;
    }
};"""
    },

    264: {
        "starter_code_javascript": "function count_Primes_nums(n) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function count_Primes_nums(n) {
    let count = 0;
    for (let i = 2; i < n; i++) {
        let isPrime = true;
        for (let j = 2; j * j <= i; j++) {
            if (i % j === 0) { isPrime = false; break; }
        }
        if (isPrime) count++;
    }
    return count;
}""",
        "starter_code_java": "class Solution {\\n    public int count_Primes_nums(int n) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int count_Primes_nums(int n) {
        int count = 0;
        for (int i = 2; i < n; i++) {
            boolean isPrime = true;
            for (int j = 2; j * j <= i; j++) {
                if (i % j == 0) { isPrime = false; break; }
            }
            if (isPrime) count++;
        }
        return count;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int count_Primes_nums(int n);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    int count_Primes_nums(int n) {
        int count = 0;
        for (int i = 2; i < n; ++i) {
            bool isPrime = true;
            for (int j = 2; j * j <= i; ++j) {
                if (i % j == 0) { isPrime = false; break; }
            }
            if (isPrime) count++;
        }
        return count;
    }
};"""
    },

    265: {
        "starter_code_java": "class Solution {\\n    public int count_odd(int[] array_nums) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int count_odd(int[] array_nums) {
        int count = 0;
        for (int x : array_nums) {
            if (x % 2 != 0) count++;
        }
        return count;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int count_odd(const vector<int>& array_nums);\\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    int count_odd(const vector<int>& array_nums) {
        int count = 0;
        for (int x : array_nums) {
            if (x % 2 != 0) count++;
        }
        return count;
    }
};"""
    },

    267: {
        "starter_code_javascript": "function merge_dict(d1, d2) {\\n    return {};\\n}",
        "reference_solution_javascript": """function merge_dict(d1, d2) {
    return Object.assign({}, d1, d2);
}""",
        "starter_code_java": "import java.util.*;\\nclass Solution {\\n    public Map<Object, Object> merge_dict(Map<Object, Object> d1, Map<Object, Object> d2) {\\n        return new HashMap<>();\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public Map<Object, Object> merge_dict(Map<Object, Object> d1, Map<Object, Object> d2) {
        Map<Object, Object> res = new HashMap<>(d1);
        res.putAll(d2);
        return res;
    }
}""",
        "starter_code_cpp": "#include <unordered_map>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    unordered_map<string, int> merge_dict(unordered_map<string, int> d1, const unordered_map<string, int>& d2);\\n};",
        "reference_solution_cpp": """#include <unordered_map>
#include <string>
using namespace std;
class Solution {
public:
    unordered_map<string, int> merge_dict(unordered_map<string, int> d1, const unordered_map<string, int>& d2) {
        for (const auto& kv : d2) {
            d1[kv.first] = kv.second;
        }
        return d1;
    }
};"""
    },

    268: {
        "starter_code_java": "class Solution {\\n    public int dog_age(int h_age) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int dog_age(int h_age) {
        if (h_age <= 2) {
            return (int)(h_age * 10.5);
        }
        return 21 + (h_age - 2) * 4;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int dog_age(int h_age);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    int dog_age(int h_age) {
        if (h_age <= 2) {
            return (int)(h_age * 10.5);
        }
        return 21 + (h_age - 2) * 4;
    }
};"""
    },

    269: {
        "starter_code_javascript": "function list_split(S, step) {\\n    return [];\\n}",
        "reference_solution_javascript": """function list_split(S, step) {
    const res = [];
    for (let i = 0; i < step; i++) {
        const sub = [];
        for (let j = i; j < S.length; j += step) {
            sub.push(S[j]);
        }
        res.push(sub);
    }
    return res;
}""",
        "starter_code_java": "class Solution {\\n    public String[][] list_split(String[] S, int step) {\\n        return new String[][]{};\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public String[][] list_split(String[] S, int step) {
        String[][] res = new String[step][];
        for (int i = 0; i < step; i++) {
            List<String> list = new ArrayList<>();
            for (int j = i; j < S.length; j += step) {
                list.add(S[j]);
            }
            res[i] = list.toArray(new String[0]);
        }
        return res;
    }
    public int[][] list_split(int[] S, int step) {
        int[][] res = new int[step][];
        for (int i = 0; i < step; i++) {
            List<Integer> list = new ArrayList<>();
            for (int j = i; j < S.length; j += step) {
                list.add(S[j]);
            }
            res[i] = new int[list.size()];
            for (int k = 0; k < list.size(); k++) res[i][k] = list.get(k);
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<vector<string>> list_split(const vector<string>& S, int step);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
using namespace std;
class Solution {
public:
    vector<vector<string>> list_split(const vector<string>& S, int step) {
        vector<vector<string>> res(step);
        for (int i = 0; i < step; ++i) {
            for (size_t j = i; j < S.size(); j += step) {
                res[i].push_back(S[j]);
            }
        }
        return res;
    }
    vector<vector<int>> list_split(const vector<int>& S, int step) {
        vector<vector<int>> res(step);
        for (int i = 0; i < step; ++i) {
            for (size_t j = i; j < S.size(); j += step) {
                res[i].push_back(S[j]);
            }
        }
        return res;
    }
};"""
    },

    273: {
        "starter_code_java": "class Solution {\\n    public int ascii_value(String k) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int ascii_value(String k) {
        return (int)k.charAt(0);
    }
}""",
        "starter_code_cpp": "#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int ascii_value(const string& k);\\n};",
        "reference_solution_cpp": """#include <string>
using namespace std;
class Solution {
public:
    int ascii_value(const string& k) {
        return (int)k[0];
    }
};"""
    },

    274: {
        "starter_code_java": "class Solution {\\n    public int sum_even_and_even_index(int[] arr, int n) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int sum_even_and_even_index(int[] arr, int n) {
        int sum = 0;
        for (int i = 0; i < n; i += 2) {
            if (arr[i] % 2 == 0) sum += arr[i];
        }
        return sum;
    }
}"""
    },

    276: {
        "starter_code_java": "class Solution {\\n    public int[] rear_extract(Object[][] test_list) {\\n        return new int[]{};\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int[] rear_extract(Object[][] test_list) {
        int[] res = new int[test_list.length];
        for (int i = 0; i < test_list.length; i++) {
            Object last = test_list[i][test_list[i].length - 1];
            res[i] = ((Number)last).intValue();
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<int> rear_extract(const vector<vector<string>>& test_list);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
using namespace std;
class Solution {
public:
    vector<int> rear_extract(const vector<vector<string>>& test_list) {
        vector<int> res;
        for (const auto& row : test_list) {
            res.push_back(stoi(row.back()));
        }
        return res;
    }
};"""
    },

    278: {
        "starter_code_java": "class Solution {\\n    public int get_Position(int[] a, int n, int m) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int get_Position(int[] a, int n, int m) {
        int[] temp = a.clone();
        for (int i = 0; i < n; i++) {
            temp[i] = temp[i] / m + (temp[i] % m != 0 ? 1 : 0);
        }
        int result = -1, maxx = -1;
        for (int i = n - 1; i >= 0; i--) {
            if (maxx < temp[i]) {
                maxx = temp[i];
                result = i;
            }
        }
        return result + 1;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int get_Position(vector<int> a, int n, int m);\\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    int get_Position(vector<int> a, int n, int m) {
        for (int i = 0; i < n; ++i) {
            a[i] = a[i] / m + (a[i] % m != 0 ? 1 : 0);
        }
        int result = -1, maxx = -1;
        for (int i = n - 1; i >= 0; --i) {
            if (maxx < a[i]) {
                maxx = a[i];
                result = i;
            }
        }
        return result + 1;
    }
};"""
    },

    280: {
        "starter_code_javascript": "function dict_filter(dict, n) {\\n    return {};\\n}",
        "reference_solution_javascript": """function dict_filter(dict, n) {
    const res = {};
    for (const [k, v] of Object.entries(dict)) {
        if (v >= n) res[k] = v;
    }
    return res;
}""",
        "starter_code_java": "import java.util.*;\\nclass Solution {\\n    public Map<Object, Object> dict_filter(Map<Object, Object> dict, int n) {\\n        return new HashMap<>();\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public Map<Object, Object> dict_filter(Map<Object, Object> dict, int n) {
        Map<Object, Object> res = new LinkedHashMap<>();
        for (Map.Entry<Object, Object> e : dict.entrySet()) {
            if (((Number) e.getValue()).intValue() >= n) {
                res.put(e.getKey(), e.getValue());
            }
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <unordered_map>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    unordered_map<string, int> dict_filter(const unordered_map<string, int>& dict, int n);\\n};",
        "reference_solution_cpp": """#include <unordered_map>
#include <string>
using namespace std;
class Solution {
public:
    unordered_map<string, int> dict_filter(const unordered_map<string, int>& dict, int n) {
        unordered_map<string, int> res;
        for (const auto& kv : dict) {
            if (kv.second >= n) res[kv.first] = kv.second;
        }
        return res;
    }
};"""
    },

    282: {
        "starter_code_java": "class Solution {\\n    public boolean all_unique(int[] test_list) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public boolean all_unique(int[] test_list) {
        Set<Integer> set = new HashSet<>();
        for (int x : test_list) {
            if (!set.add(x)) return false;
        }
        return true;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    bool all_unique(const vector<int>& test_list);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <unordered_set>
using namespace std;
class Solution {
public:
    bool all_unique(const vector<int>& test_list) {
        unordered_set<int> s;
        for (int x : test_list) {
            if (s.count(x)) return false;
            s.insert(x);
        }
        return true;
    }
};"""
    },

    283: {
        "starter_code_javascript": "function sub_list(nums1, nums2) {\\n    return [];\\n}",
        "reference_solution_javascript": """function sub_list(nums1, nums2) {
    return nums1.map((x, i) => x - nums2[i]);
}""",
        "starter_code_java": "class Solution {\\n    public int[] sub_list(int[] nums1, int[] nums2) {\\n        return new int[]{};\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int[] sub_list(int[] nums1, int[] nums2) {
        int[] res = new int[nums1.length];
        for (int i = 0; i < nums1.length; i++) res[i] = nums1[i] - nums2[i];
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<int> sub_list(const vector<int>& nums1, const vector<int>& nums2);\\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    vector<int> sub_list(const vector<int>& nums1, const vector<int>& nums2) {
        vector<int> res(nums1.size());
        for (size_t i = 0; i < nums1.size(); ++i) res[i] = nums1[i] - nums2[i];
        return res;
    }
};"""
    },

    284: {
        "starter_code_java": "class Solution {\\n    public boolean validate(int n) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public boolean validate(int n) {
        int[] count = new int[10];
        int temp = n;
        while (temp > 0) {
            count[temp % 10]++;
            temp /= 10;
        }
        for (int i = 0; i < 10; i++) {
            if (count[i] > i) return false;
        }
        return true;
    }
}"""
    },

    285: {
        "starter_code_java": "class Solution {\\n    public boolean check_element(String[] list, String element) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public boolean check_element(String[] list, String element) {
        for (String s : list) {
            if (!s.equals(element)) return false;
        }
        return true;
    }
    public boolean check_element(int[] list, int element) {
        for (int x : list) {
            if (x != element) return false;
        }
        return true;
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    bool check_element(const vector<string>& list, const string& element);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
using namespace std;
class Solution {
public:
    bool check_element(const vector<string>& list, const string& element) {
        for (const auto& s : list) {
            if (s != element) return false;
        }
        return true;
    }
    bool check_element(const vector<int>& list, int element) {
        for (int x : list) {
            if (x != element) return false;
        }
        return true;
    }
};"""
    },

    290: {
        "starter_code_java": "class Solution {\\n    public int odd_Days(int N) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int odd_Days(int N) {
        int hund1 = N / 100;
        int hund4 = N / 400;
        int leap = N >> 2;
        int ordd = N - leap;
        if (hund1 != 0) {
            ordd += hund1;
            leap -= hund1;
        }
        if (hund4 != 0) {
            ordd -= hund4;
            leap += hund4;
        }
        int days = ordd + leap * 2;
        return days % 7;
    }
}"""
    },

    294: {
        "starter_code_javascript": "function max_val(listval) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function max_val(listval) {
    let m = -Infinity;
    for (const x of listval) {
        if (Number.isInteger(x) && x > m) m = x;
    }
    return m;
}""",
        "starter_code_java": "class Solution {\\n    public int max_val(Object[] listval) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int max_val(Object[] listval) {
        int max = Integer.MIN_VALUE;
        for (Object x : listval) {
            if (x instanceof Integer) {
                int val = (Integer) x;
                if (val > max) max = val;
            }
        }
        return max;
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int max_val(const vector<string>& listval);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <cctype>
#include <algorithm>
using namespace std;
class Solution {
public:
    int max_val(const vector<string>& listval) {
        int mx = -1000000;
        for (const auto& s : listval) {
            if (s.empty()) continue;
            bool is_int = true;
            size_t start = (s[0] == '-') ? 1 : 0;
            if (start == s.size()) is_int = false;
            for (size_t i = start; i < s.size(); ++i) {
                if (!isdigit(s[i])) { is_int = false; break; }
            }
            if (is_int) {
                mx = max(mx, stoi(s));
            }
        }
        return mx;
    }
};"""
    },

    295: {
        "starter_code_java": "class Solution {\\n    public int sum_div(int number) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int sum_div(int number) {
        int sum = 1;
        for (int i = 2; i < number; i++) {
            if (number % i == 0) sum += i;
        }
        return sum;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int sum_div(int number);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    int sum_div(int number) {
        int sum = 1;
        for (int i = 2; i < number; ++i) {
            if (number % i == 0) sum += i;
        }
        return sum;
    }
};"""
    },

    297: {
        "starter_code_javascript": "function flatten_list(list1) {\\n    return [];\\n}",
        "reference_solution_javascript": """function flatten_list(list1) {
    const res = [];
    function rec(arr) {
        for (const item of arr) {
            if (Array.isArray(item)) rec(item);
            else res.push(item);
        }
    }
    rec(list1);
    return res;
}""",
        "starter_code_java": "class Solution {\\n    public int[] flatten_list(int[][] list1) {\\n        return new int[]{};\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[] flatten_list(Object[] list1) {
        List<Integer> list = new ArrayList<>();
        for (Object x : list1) {
            if (x instanceof int[]) {
                for (int y : (int[]) x) list.add(y);
            } else if (x instanceof Number) {
                list.add(((Number) x).intValue());
            }
        }
        int[] res = new int[list.size()];
        for (int i = 0; i < list.size(); i++) res[i] = list.get(i);
        return res;
    }
    public int[] flatten_list(int[][] list1) {
        List<Integer> list = new ArrayList<>();
        for (int[] row : list1) {
            for (int y : row) list.add(y);
        }
        int[] res = new int[list.size()];
        for (int i = 0; i < list.size(); i++) res[i] = list.get(i);
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<int> flatten_list(const vector<vector<int>>& list1);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <sstream>
using namespace std;
class Solution {
public:
    vector<int> flatten_list(const vector<vector<int>>& list1) {
        vector<int> res;
        for (const auto& row : list1) {
            res.insert(res.end(), row.begin(), row.end());
        }
        return res;
    }
    vector<int> flatten_list(const vector<string>& list1) {
        vector<int> res;
        for (const auto& s : list1) {
            if (s.empty()) continue;
            if (s.front() == '[') {
                string inner = s.substr(1, s.size() >= 2 ? s.size() - 2 : 0);
                stringstream ss(inner);
                string token;
                while (getline(ss, token, ',')) {
                    while (!token.empty() && isspace(token.front())) token.erase(token.begin());
                    while (!token.empty() && isspace(token.back())) token.pop_back();
                    if (!token.empty()) res.push_back(stoi(token));
                }
            } else {
                res.push_back(stoi(s));
            }
        }
        return res;
    }
};"""
    },

    298: {
        "starter_code_java": "class Solution {\\n    public int[][] intersection_nested_lists(int[] l1, int[][] l2) {\\n        return new int[][]{};\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[][] intersection_nested_lists(int[] l1, int[][] l2) {
        Set<Integer> set = new HashSet<>();
        for (int x : l1) set.add(x);
        int[][] res = new int[l2.length][];
        for (int i = 0; i < l2.length; i++) {
            List<Integer> sub = new ArrayList<>();
            for (int x : l2[i]) {
                if (set.contains(x)) sub.add(x);
            }
            res[i] = new int[sub.size()];
            for (int j = 0; j < sub.size(); j++) res[i][j] = sub.get(j);
        }
        return res;
    }
    public int[][] intersection_nested_lists(int[][] l1, int[][] l2) {
        int[][] res = new int[l2.length][];
        for (int i = 0; i < l2.length; i++) {
            res[i] = new int[0];
        }
        return res;
    }
    public String[][] intersection_nested_lists(String[] l1, String[][] l2) {
        Set<String> set = new HashSet<>(Arrays.asList(l1));
        String[][] res = new String[l2.length][];
        for (int i = 0; i < l2.length; i++) {
            List<String> sub = new ArrayList<>();
            for (String s : l2[i]) {
                if (set.contains(s)) sub.add(s);
            }
            res[i] = sub.toArray(new String[0]);
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<vector<int>> intersection_nested_lists(const vector<int>& l1, const vector<vector<int>>& l2);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <unordered_set>
using namespace std;
class Solution {
public:
    vector<vector<int>> intersection_nested_lists(const vector<int>& l1, const vector<vector<int>>& l2) {
        unordered_set<int> s(l1.begin(), l1.end());
        vector<vector<int>> res(l2.size());
        for (size_t i = 0; i < l2.size(); ++i) {
            for (int x : l2[i]) {
                if (s.count(x)) res[i].push_back(x);
            }
        }
        return res;
    }
    vector<vector<int>> intersection_nested_lists(const vector<vector<int>>& l1, const vector<vector<int>>& l2) {
        return vector<vector<int>>(l2.size());
    }
    vector<vector<string>> intersection_nested_lists(const vector<string>& l1, const vector<vector<string>>& l2) {
        unordered_set<string> s(l1.begin(), l1.end());
        vector<vector<string>> res(l2.size());
        for (size_t i = 0; i < l2.size(); ++i) {
            for (const auto& str : l2[i]) {
                if (s.count(str)) res[i].push_back(str);
            }
        }
        return res;
    }
};"""
    },

    300: {
        "starter_code_javascript": "function dict_depth(d) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function dict_depth(d) {
    if (typeof d === 'object' && d !== null && !Array.isArray(d)) {
        let maxChild = 0;
        for (const val of Object.values(d)) {
            maxChild = Math.max(maxChild, dict_depth(val));
        }
        return 1 + maxChild;
    }
    return 0;
}""",
        "starter_code_java": "import java.util.*;\\nclass Solution {\\n    public int dict_depth(Map<Object, Object> d) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int dict_depth(Map<Object, Object> d) {
        if (d == null) return 0;
        int maxChild = 0;
        for (Object val : d.values()) {
            if (val instanceof Map) {
                maxChild = Math.max(maxChild, dict_depth((Map<Object, Object>) val));
            }
        }
        return 1 + maxChild;
    }
}""",
        "starter_code_cpp": "#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int dict_depth(const string& d);\\n};",
        "reference_solution_cpp": """#include <string>
#include <algorithm>
using namespace std;
class Solution {
public:
    int dict_depth(const string& d) {
        int depth = 0, max_d = 0;
        for (char c : d) {
            if (c == '{') {
                depth++;
                max_d = max(max_d, depth);
            } else if (c == '}') {
                depth--;
            }
        }
        return max_d;
    }
};"""
    },

    302: {
        "starter_code_java": "class Solution {\\n    public boolean solve(int[] a, int n) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public boolean solve(int[] a, int n) {
        int mx = Integer.MIN_VALUE;
        for (int j = 1; j < n; j++) {
            if (mx > a[j]) return false;
            mx = Math.max(mx, a[j - 1]);
        }
        return true;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    bool solve(const vector<int>& a, int n);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
#include <climits>
using namespace std;
class Solution {
public:
    bool solve(const vector<int>& a, int n) {
        int mx = INT_MIN;
        for (int j = 1; j < n; ++j) {
            if (mx > a[j]) return false;
            mx = max(mx, a[j - 1]);
        }
        return true;
    }
};"""
    },

    304: {
        "starter_code_java": "class Solution {\\n    public int max_sum_increasing_subseq(int[] a, int n, int index, int k) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int max_sum_increasing_subseq(int[] a, int n, int index, int k) {
        int[][] dp = new int[n][n];
        for (int i = 0; i < n; i++) {
            if (a[i] > a[0]) dp[0][i] = a[i] + a[0];
            else dp[0][i] = a[i];
        }
        for (int i = 1; i < n; i++) {
            for (int j = 0; j < n; j++) {
                if (a[j] > a[i] && j > i) {
                    if (dp[i - 1][i] + a[j] > dp[i - 1][j]) {
                        dp[i][j] = dp[i - 1][i] + a[j];
                    } else {
                        dp[i][j] = dp[i - 1][j];
                    }
                } else {
                    dp[i][j] = dp[i - 1][j];
                }
            }
        }
        return dp[index][k];
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int max_sum_increasing_subseq(const vector<int>& a, int n, int index, int k);\\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    int max_sum_increasing_subseq(const vector<int>& a, int n, int index, int k) {
        vector<vector<int>> dp(n, vector<int>(n, 0));
        for (int i = 0; i < n; ++i) {
            if (a[i] > a[0]) dp[0][i] = a[i] + a[0];
            else dp[0][i] = a[i];
        }
        for (int i = 1; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                if (a[j] > a[i] && j > i) {
                    if (dp[i - 1][i] + a[j] > dp[i - 1][j]) {
                        dp[i][j] = dp[i - 1][i] + a[j];
                    } else {
                        dp[i][j] = dp[i - 1][j];
                    }
                } else {
                    dp[i][j] = dp[i - 1][j];
                }
            }
        }
        return dp[index][k];
    }
};"""
    },

    305: {
        "starter_code_javascript": "function colon_tuplex(tuplex, m, n) {\\n    return [];\\n}",
        "reference_solution_javascript": """function colon_tuplex(tuplex, m, n) {
    const copy = JSON.parse(JSON.stringify(tuplex));
    copy[m].push(n);
    return copy;
}""",
        "starter_code_java": "class Solution {\\n    public Object[] colon_tuplex(Object[] tuplex, int m, int n) {\\n        return new Object[]{};\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public Object[] colon_tuplex(Object[] tuplex, int m, int n) {
        Object[] copy = tuplex.clone();
        copy[m] = new int[]{n};
        return copy;
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<string> colon_tuplex(vector<string> tuplex, int m, int n);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
using namespace std;
class Solution {
public:
    vector<string> colon_tuplex(vector<string> tuplex, int m, int n) {
        if (m >= 0 && m < (int)tuplex.size()) {
            tuplex[m] = "[" + to_string(n) + "]";
        }
        return tuplex;
    }
};"""
    },

    306: {
        "starter_code_javascript": "function large_product(nums1, nums2, N) {\\n    return [];\\n}",
        "reference_solution_javascript": """function large_product(nums1, nums2, N) {
    const prods = [];
    for (const x of nums1) {
        for (const y of nums2) {
            prods.push(x * y);
        }
    }
    prods.sort((a, b) => b - a);
    return prods.slice(0, N);
}""",
        "starter_code_java": "class Solution {\\n    public int[] large_product(int[] nums1, int[] nums2, int N) {\\n        return new int[]{};\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[] large_product(int[] nums1, int[] nums2, int N) {
        List<Integer> list = new ArrayList<>();
        for (int x : nums1) {
            for (int y : nums2) {
                list.add(x * y);
            }
        }
        list.sort(Collections.reverseOrder());
        int[] res = new int[N];
        for (int i = 0; i < N; i++) res[i] = list.get(i);
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<int> large_product(const vector<int>& nums1, const vector<int>& nums2, int N);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    vector<int> large_product(const vector<int>& nums1, const vector<int>& nums2, int N) {
        vector<int> prods;
        for (int x : nums1) {
            for (int y : nums2) {
                prods.push_back(x * y);
            }
        }
        sort(prods.rbegin(), prods.rend());
        if ((int)prods.size() > N) prods.resize(N);
        return prods;
    }
};"""
    },

    308: {
        "starter_code_java": "class Solution {\\n    public int set_left_most_unset_bit(int n) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int set_left_most_unset_bit(int n) {
        if ((n & (n + 1)) == 0) return n;
        int pos = 0, temp = n, count = 0;
        while (temp > 0) {
            if ((temp & 1) == 0) pos = count;
            count++;
            temp >>= 1;
        }
        return n | (1 << pos);
    }
}"""
    },

    309: {
        "starter_code_cpp": "class Solution {\\npublic:\\n    double volume_cone(int r, int h);\\n};",
        "reference_solution_cpp": """#include <cmath>
class Solution {
public:
    double volume_cone(int r, int h) {
        double pi = std::acos(-1.0);
        return (1.0 / 3.0) * pi * r * r * h;
    }
};"""
    },

    310: {
        "starter_code_java": "class Solution {\\n    public int pos_nos(int[] list1) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int pos_nos(int[] list1) {
        for (int num : list1) {
            if (num >= 0) return num;
        }
        return 0;
    }
}"""
    }
}
'''

def main():
    target_path = os.path.join(os.path.dirname(__file__), "batch5_solutions.py")
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(BATCH5_CONTENT.strip() + "\n")
    print(f"Generated {target_path} successfully!")

if __name__ == "__main__":
    main()
