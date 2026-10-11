"""
Special multi-language implementations for Batch 1 (Problems 61..110)
"""

BATCH1_SOLUTIONS = {
    63: {
        "starter_code_javascript": "function find_Product(arr, n) {\n    return 0;\n}",
        "reference_solution_javascript": """function find_Product(arr, n) {
    arr.sort((a, b) => a - b);
    let prod = 1;
    for (let i = 0; i < n; i++) {
        const prev = (i === 0) ? arr[n - 1] : arr[i - 1];
        if (prev !== arr[i]) prod *= arr[i];
    }
    return prod;
}""",
        "starter_code_java": "class Solution {\n    public int find_Product(int[] arr, int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int find_Product(int[] arr, int n) {
        int[] copy = arr.clone();
        Arrays.sort(copy);
        int prod = 1;
        for (int i = 0; i < n; i++) {
            int prev = (i == 0) ? copy[n - 1] : copy[i - 1];
            if (prev != copy[i]) prod *= copy[i];
        }
        return prod;
    }
}""",
        "starter_code_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    int find_Product(vector<int> arr, int n) {\n        return 0;\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    int find_Product(vector<int> arr, int n) {
        sort(arr.begin(), arr.end());
        int prod = 1;
        for (int i = 0; i < n; ++i) {
            int prev = (i == 0) ? arr[n - 1] : arr[i - 1];
            if (prev != arr[i]) prod *= arr[i];
        }
        return prod;
    }
};"""
    },

    65: {
        "starter_code_javascript": "function remove(list) {\n    return [];\n}",
        "reference_solution_javascript": """function remove(list) {
    return list.map(s => s.replace(/[0-9]/g, ''));
}""",
        "starter_code_java": "class Solution {\n    public String[] remove(String[] list) {\n        return new String[]{};\n    }\n}",
        "reference_solution_java": """class Solution {
    public String[] remove(String[] list) {
        String[] res = new String[list.length];
        for (int i = 0; i < list.length; i++) {
            res[i] = list[i].replaceAll("[0-9]", "");
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\n#include <string>\nusing namespace std;\nclass Solution {\npublic:\n    vector<string> remove(const vector<string>& list) {\n        return {};\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <cctype>
using namespace std;
class Solution {
public:
    vector<string> remove(const vector<string>& list) {
        vector<string> res;
        for (const auto& s : list) {
            string cur = "";
            for (char c : s) if (!isdigit(static_cast<unsigned char>(c))) cur += c;
            res.push_back(cur);
        }
        return res;
    }
};"""
    },

    68: {
        "starter_code_javascript": "function count_Substring_With_Equal_Ends(s) {\n    return 0;\n}",
        "reference_solution_javascript": """function count_Substring_With_Equal_Ends(s) {
    let result = 0, n = s.length;
    for (let i = 0; i < n; i++) {
        for (let j = 1; i + j <= n; j++) {
            if (s[i] === s[i + j - 1]) result++;
        }
    }
    return result;
}""",
        "starter_code_java": "class Solution {\n    public int count_Substring_With_Equal_Ends(String s) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int count_Substring_With_Equal_Ends(String s) {
        int result = 0, n = s.length();
        for (int i = 0; i < n; i++) {
            for (int j = 1; i + j <= n; j++) {
                if (s.charAt(i) == s.charAt(i + j - 1)) result++;
            }
        }
        return result;
    }
}""",
        "starter_code_cpp": "#include <string>\nusing namespace std;\nclass Solution {\npublic:\n    int count_Substring_With_Equal_Ends(const string& s) {\n        return 0;\n    }\n};",
        "reference_solution_cpp": """#include <string>
using namespace std;
class Solution {
public:
    int count_Substring_With_Equal_Ends(const string& s) {
        int result = 0, n = s.length();
        for (int i = 0; i < n; ++i) {
            for (int j = 1; i + j <= n; ++j) {
                if (s[i] == s[i + j - 1]) ++result;
            }
        }
        return result;
    }
};"""
    },

    69: {
        "starter_code_javascript": "function func(nums, k) {\n    return [];\n}",
        "reference_solution_javascript": """function func(nums, k) {
    const counts = new Map();
    for (const row of nums) {
        for (const x of row) {
            counts.set(x, (counts.get(x) || 0) + 1);
        }
    }
    const heap = [];
    for (const [key, v] of counts.entries()) {
        if (heap.length < k) {
            heap.push([v, key]);
            heap.sort((a, b) => a[0] - b[0] || a[1] - b[1]);
        } else if (v > heap[0][0]) {
            heap.shift();
            heap.push([v, key]);
            heap.sort((a, b) => a[0] - b[0] || a[1] - b[1]);
        }
    }
    return heap.map(item => item[1]);
}""",
        "starter_code_java": "class Solution {\n    public int[] func(int[][] nums, int k) {\n        return new int[]{};\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[] func(int[][] nums, int k) {
        Map<Integer, Integer> counts = new LinkedHashMap<>();
        for (int[] row : nums) {
            for (int x : row) {
                counts.put(x, counts.getOrDefault(x, 0) + 1);
            }
        }
        PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[0] != b[0] ? Integer.compare(a[0], b[0]) : Integer.compare(a[1], b[1]));
        for (Map.Entry<Integer, Integer> e : counts.entrySet()) {
            int key = e.getKey(), v = e.getValue();
            if (pq.size() < k) {
                pq.offer(new int[]{v, key});
            } else if (v > pq.peek()[0]) {
                pq.poll();
                pq.offer(new int[]{v, key});
            }
        }
        int[] res = new int[pq.size()];
        int idx = 0;
        while (!pq.isEmpty()) {
            res[idx++] = pq.poll()[1];
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    vector<int> func(const vector<vector<int>>& nums, int k) {\n        return {};\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <unordered_map>
#include <queue>
using namespace std;
class Solution {
public:
    vector<int> func(const vector<vector<int>>& nums, int k) {
        vector<int> order;
        unordered_map<int, int> counts;
        for (const auto& row : nums) {
            for (int x : row) {
                if (!counts.count(x)) order.push_back(x);
                counts[x]++;
            }
        }
        auto cmp = [](const pair<int, int>& a, const pair<int, int>& b) {
            if (a.first != b.first) return a.first > b.first;
            return a.second > b.second;
        };
        priority_queue<pair<int, int>, vector<pair<int, int>>, decltype(cmp)> pq(cmp);
        for (int key : order) {
            int v = counts[key];
            if ((int)pq.size() < k) {
                pq.push({v, key});
            } else if (v > pq.top().first) {
                pq.pop();
                pq.push({v, key});
            }
        }
        vector<int> res;
        while (!pq.empty()) {
            res.push_back(pq.top().second);
            pq.pop();
        }
        return res;
    }
};"""
    },

    74: {
        "starter_code_javascript": "function find_Nth_Digit(p, q, N) {\n    return 0;\n}",
        "reference_solution_javascript": """function find_Nth_Digit(p, q, N) {
    let res = 0;
    while (N > 0) {
        N--;
        p *= 10;
        res = Math.floor(p / q);
        p %= q;
    }
    return res;
}""",
        "starter_code_java": "class Solution {\n    public int find_Nth_Digit(int p, int q, int N) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int find_Nth_Digit(int p, int q, int N) {
        int res = 0;
        while (N > 0) {
            N--;
            p *= 10;
            res = p / q;
            p %= q;
        }
        return res;
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    int find_Nth_Digit(int p, int q, int N) {\n        return 0;\n    }\n};",
        "reference_solution_cpp": """class Solution {
public:
    int find_Nth_Digit(int p, int q, int N) {
        int res = 0;
        while (N > 0) {
            --N;
            p *= 10;
            res = p / q;
            p %= q;
        }
        return res;
    }
};"""
    },

    75: {
        "starter_code_javascript": "function sort_mixed_list(mixed_list) {\n    return [];\n}",
        "reference_solution_javascript": """function sort_mixed_list(mixed_list) {
    const intPart = mixed_list.filter(x => typeof x === 'number').sort((a, b) => a - b);
    const strPart = mixed_list.filter(x => typeof x === 'string').sort();
    return intPart.concat(strPart);
}""",
        "starter_code_java": "class Solution {\n    public Object[] sort_mixed_list(Object[] mixed_list) {\n        return new Object[]{};\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public Object[] sort_mixed_list(Object[] mixed_list) {
        List<Integer> ints = new ArrayList<>();
        List<String> strs = new ArrayList<>();
        for (Object o : mixed_list) {
            if (o instanceof Number) ints.add(((Number) o).intValue());
            else if (o instanceof String) strs.add((String) o);
        }
        Collections.sort(ints);
        Collections.sort(strs);
        Object[] res = new Object[ints.size() + strs.size()];
        int idx = 0;
        for (int x : ints) res[idx++] = x;
        for (String s : strs) res[idx++] = s;
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\n#include <string>\nusing namespace std;\nclass Solution {\npublic:\n    vector<string> sort_mixed_list(const vector<string>& mixed_list) {\n        return {};\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <algorithm>
#include <cctype>
using namespace std;
class Solution {
public:
    vector<string> sort_mixed_list(const vector<string>& mixed_list) {
        vector<int> ints;
        vector<string> strs;
        for (const auto& s : mixed_list) {
            bool isNum = !s.empty();
            for (char c : s) if (!isdigit(c)) isNum = false;
            if (isNum) ints.push_back(stoi(s));
            else strs.push_back(s);
        }
        sort(ints.begin(), ints.end());
        sort(strs.begin(), strs.end());
        vector<string> res;
        for (int x : ints) res.push_back(to_string(x));
        for (const auto& s : strs) res.push_back(s);
        return res;
    }
};"""
    },

    76: {
        "starter_code_javascript": "function div_even_odd(list1) {\n    return 0;\n}",
        "reference_solution_javascript": """function div_even_odd(list1) {
    let first_even = -1, first_odd = -1;
    for (const x of list1) {
        if (x % 2 === 0 && first_even === -1) first_even = x;
        if (x % 2 !== 0 && first_odd === -1) first_odd = x;
        if (first_even !== -1 && first_odd !== -1) break;
    }
    return Math.floor(first_even / first_odd);
}""",
        "starter_code_java": "class Solution {\n    public int div_even_odd(int[] list1) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int div_even_odd(int[] list1) {
        int first_even = -1, first_odd = -1;
        for (int x : list1) {
            if (x % 2 == 0 && first_even == -1) first_even = x;
            if (x % 2 != 0 && first_odd == -1) first_odd = x;
            if (first_even != -1 && first_odd != -1) break;
        }
        return first_even / first_odd;
    }
}""",
        "starter_code_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    int div_even_odd(const vector<int>& list1) {\n        return 0;\n    }\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    int div_even_odd(const vector<int>& list1) {
        int first_even = -1, first_odd = -1;
        for (int x : list1) {
            if (x % 2 == 0 && first_even == -1) first_even = x;
            if (x % 2 != 0 && first_odd == -1) first_odd = x;
            if (first_even != -1 && first_odd != -1) break;
        }
        return first_even / first_odd;
    }
};"""
    },

    77: {
        "starter_code_javascript": "function rearange_string(S) {\n    return \"\";\n}",
        "reference_solution_javascript": """function rearange_string(S) {
    const counts = {};
    for (const c of S) counts[c] = (counts[c] || 0) + 1;
    const heap = Object.keys(counts).map(c => [counts[c], c]);
    heap.sort((a, b) => b[0] - a[0] || a[1].localeCompare(b[1]));
    if (heap[0][0] * 2 > S.length + 1) return "";
    const ans = [];
    while (heap.length >= 2) {
        const first = heap.shift();
        const second = heap.shift();
        ans.push(first[1], second[1]);
        if (first[0] - 1 > 0) heap.push([first[0] - 1, first[1]]);
        if (second[0] - 1 > 0) heap.push([second[0] - 1, second[1]]);
        heap.sort((a, b) => b[0] - a[0] || a[1].localeCompare(b[1]));
    }
    if (heap.length > 0) ans.push(heap[0][1]);
    return ans.join("");
}""",
        "starter_code_java": "class Solution {\n    public String rearange_string(String S) {\n        return \"\";\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public String rearange_string(String S) {
        Map<Character, Integer> counts = new HashMap<>();
        for (char c : S.toCharArray()) counts.put(c, counts.getOrDefault(c, 0) + 1);
        PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> b[1] != a[1] ? Integer.compare(b[1], a[1]) : Integer.compare(a[0], b[0]));
        for (Map.Entry<Character, Integer> e : counts.entrySet()) {
            pq.offer(new int[]{(int) e.getKey(), e.getValue()});
        }
        if (pq.peek()[1] * 2 > S.length() + 1) return "";
        StringBuilder sb = new StringBuilder();
        while (pq.size() >= 2) {
            int[] first = pq.poll();
            int[] second = pq.poll();
            sb.append((char) first[0]);
            sb.append((char) second[0]);
            if (first[1] - 1 > 0) pq.offer(new int[]{first[0], first[1] - 1});
            if (second[1] - 1 > 0) pq.offer(new int[]{second[0], second[1] - 1});
        }
        if (!pq.isEmpty()) sb.append((char) pq.poll()[0]);
        return sb.toString();
    }
}""",
        "starter_code_cpp": "#include <string>\nusing namespace std;\nclass Solution {\npublic:\n    string rearange_string(const string& S) {\n        return \"\";\n    }\n};",
        "reference_solution_cpp": """#include <string>
#include <unordered_map>
#include <queue>
using namespace std;
class Solution {
public:
    string rearange_string(const string& S) {
        unordered_map<char, int> counts;
        for (char c : S) counts[c]++;
        auto cmp = [](const pair<char, int>& a, const pair<char, int>& b) {
            if (a.second != b.second) return a.second < b.second;
            return a.first > b.first;
        };
        priority_queue<pair<char, int>, vector<pair<char, int>>, decltype(cmp)> pq(cmp);
        for (auto& p : counts) pq.push(p);
        if (pq.top().second * 2 > (int)S.length() + 1) return "";
        string ans = "";
        while (pq.size() >= 2) {
            auto first = pq.top(); pq.pop();
            auto second = pq.top(); pq.pop();
            ans += first.first;
            ans += second.first;
            if (first.second - 1 > 0) pq.push({first.first, first.second - 1});
            if (second.second - 1 > 0) pq.push({second.first, second.second - 1});
        }
        if (!pq.empty()) ans += pq.top().first;
        return ans;
    }
};"""
    },

    78: {
        "starter_code_java": "class Solution {\n    public int[] filter_evennumbers(int[] nums) {\n        return new int[]{};\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[] filter_evennumbers(int[] nums) {
        List<Integer> list = new ArrayList<>();
        for (int x : nums) if (x % 2 == 0) list.add(x);
        int[] res = new int[list.size()];
        for (int i = 0; i < list.size(); i++) res[i] = list.get(i);
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    vector<int> filter_evennumbers(const vector<int>& nums) {\n        return {};\n    }\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    vector<int> filter_evennumbers(const vector<int>& nums) {
        vector<int> res;
        for (int x : nums) if (x % 2 == 0) res.push_back(x);
        return res;
    }
};"""
    },

    79: {
        "starter_code_javascript": "function find_Sum(arr, n) {\n    return 0;\n}",
        "reference_solution_javascript": """function find_Sum(arr, n) {
    const counts = {};
    for (const x of arr) counts[x] = (counts[x] || 0) + 1;
    let s = 0;
    for (const x of arr) {
        if (counts[x] > 1) s += x;
    }
    return s;
}""",
        "starter_code_java": "class Solution {\n    public int find_Sum(int[] arr, int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int find_Sum(int[] arr, int n) {
        Map<Integer, Integer> counts = new HashMap<>();
        for (int x : arr) counts.put(x, counts.getOrDefault(x, 0) + 1);
        int s = 0;
        for (int x : arr) {
            if (counts.get(x) > 1) s += x;
        }
        return s;
    }
}""",
        "starter_code_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    int find_Sum(const vector<int>& arr, int n) {\n        return 0;\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <unordered_map>
using namespace std;
class Solution {
public:
    int find_Sum(const vector<int>& arr, int n) {
        unordered_map<int, int> counts;
        for (int x : arr) counts[x]++;
        int s = 0;
        for (int x : arr) {
            if (counts[x] > 1) s += x;
        }
        return s;
    }
};"""
    },

    82: {
        "starter_code_javascript": "function get_gcd(l) {\n    return 0;\n}",
        "reference_solution_javascript": """function get_gcd(l) {
    function gcd(a, b) {
        while (b) { let t = b; b = a % b; a = t; }
        return a;
    }
    let res = l[0];
    for (let i = 1; i < l.length; i++) res = gcd(res, l[i]);
    return res;
}""",
        "starter_code_java": "class Solution {\n    public int get_gcd(int[] l) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    private int gcd(int a, int b) {
        while (b != 0) { int t = b; b = a % b; a = t; }
        return a;
    }
    public int get_gcd(int[] l) {
        int res = l[0];
        for (int i = 1; i < l.length; i++) res = gcd(res, l[i]);
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    int get_gcd(const vector<int>& l) {\n        return 0;\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <numeric>
using namespace std;
class Solution {
public:
    int get_gcd(const vector<int>& l) {
        int res = l[0];
        for (size_t i = 1; i < l.size(); ++i) res = std::gcd(res, l[i]);
        return res;
    }
};"""
    },

    83: {
        "starter_code_java": "class Solution {\n    public boolean test_distinct(int[] data) {\n        return false;\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public boolean test_distinct(int[] data) {
        Set<Integer> set = new HashSet<>();
        for (int x : data) {
            if (!set.add(x)) return false;
        }
        return true;
    }
}""",
        "starter_code_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    bool test_distinct(const vector<int>& data) {\n        return false;\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <unordered_set>
using namespace std;
class Solution {
public:
    bool test_distinct(const vector<int>& data) {
        unordered_set<int> set;
        for (int x : data) {
            if (set.count(x)) return false;
            set.insert(x);
        }
        return true;
    }
};"""
    },

    86: {
        "starter_code_java": "class Solution {\n    public int[] specified_element(int[][] nums, int N) {\n        return new int[]{};\n    }\n}",
        "reference_solution_java": """class Solution {
    public int[] specified_element(int[][] nums, int N) {
        int[] res = new int[nums.length];
        for (int i = 0; i < nums.length; i++) res[i] = nums[i][N];
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
        for (const auto& row : nums) res.push_back(row[N]);
        return res;
    }
};"""
    },

    89: {
        "starter_code_java": "class Solution {\n    public String check_Equality(String str) {\n        return \"\";\n    }\n}",
        "reference_solution_java": """class Solution {
    public String check_Equality(String str) {
        if (str.length() > 0 && str.charAt(0) == str.charAt(str.length() - 1)) {
            return "Equal";
        }
        return "Not Equal";
    }
}"""
    },

    90: {
        "starter_code_java": "class Solution {\n    public int[] counting_sort(int[] my_list) {\n        return new int[]{};\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[] counting_sort(int[] my_list) {
        int[] copy = my_list.clone();
        Arrays.sort(copy);
        return copy;
    }
}""",
        "starter_code_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    vector<int> counting_sort(vector<int> my_list) {\n        return {};\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    vector<int> counting_sort(vector<int> my_list) {
        sort(my_list.begin(), my_list.end());
        return my_list;
    }
};"""
    },

    91: {
        "starter_code_java": "class Solution {\n    public int tn_gp(int a, int n, int r) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int tn_gp(int a, int n, int r) {
        return (int) (a * Math.pow(r, n - 1));
    }
}"""
    },

    93: {
        "starter_code_javascript": "function find_Max_Num(arr, n) {\n    return 0;\n}",
        "reference_solution_javascript": """function find_Max_Num(arr, n) {
    arr.sort((a, b) => b - a);
    let num = arr[0];
    for (let i = 1; i < n; i++) num = num * 10 + arr[i];
    return num;
}""",
        "starter_code_java": "class Solution {\n    public int find_Max_Num(int[] arr, int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int find_Max_Num(int[] arr, int n) {
        int[] copy = arr.clone();
        Arrays.sort(copy);
        int num = copy[n - 1];
        for (int i = n - 2; i >= 0; i--) num = num * 10 + copy[i];
        return num;
    }
}""",
        "starter_code_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    int find_Max_Num(vector<int> arr, int n) {\n        return 0;\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    int find_Max_Num(vector<int> arr, int n) {
        sort(arr.rbegin(), arr.rend());
        int num = arr[0];
        for (int i = 1; i < n; ++i) num = num * 10 + arr[i];
        return num;
    }
};"""
    },

    96: {
        "starter_code_java": "class Solution {\n    public int max_len_sub(int[] arr, int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int max_len_sub(int[] arr, int n) {
        int[] mls = new int[n];
        Arrays.fill(mls, 1);
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < i; j++) {
                if (Math.abs(arr[i] - arr[j]) <= 1 && mls[i] < mls[j] + 1) {
                    mls[i] = mls[j] + 1;
                }
            }
        }
        int max = 0;
        for (int i = 0; i < n; i++) if (max < mls[i]) max = mls[i];
        return max;
    }
}""",
        "starter_code_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    int max_len_sub(const vector<int>& arr, int n) {\n        return 0;\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <cmath>
#include <algorithm>
using namespace std;
class Solution {
public:
    int max_len_sub(const vector<int>& arr, int n) {
        vector<int> mls(n, 1);
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < i; ++j) {
                if (abs(arr[i] - arr[j]) <= 1 && mls[i] < mls[j] + 1) {
                    mls[i] = mls[j] + 1;
                }
            }
        }
        int max_val = 0;
        for (int i = 0; i < n; ++i) max_val = max(max_val, mls[i]);
        return max_val;
    }
};"""
    },

    97: {
        "starter_code_java": "class Solution {\n    public int count_Substrings(String s, int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int count_Substrings(String s, int n) {
        int count = 0, sum = 0;
        Map<Integer, Integer> mp = new HashMap<>();
        mp.put(0, 1);
        for (int i = 0; i < n; i++) {
            sum += s.charAt(i) - '0';
            int key = sum - (i + 1);
            count += mp.getOrDefault(key, 0);
            mp.put(key, mp.getOrDefault(key, 0) + 1);
        }
        return count;
    }
}""",
        "starter_code_cpp": "#include <string>\nusing namespace std;\nclass Solution {\npublic:\n    int count_Substrings(const string& s, int n) {\n        return 0;\n    }\n};",
        "reference_solution_cpp": """#include <string>
#include <unordered_map>
using namespace std;
class Solution {
public:
    int count_Substrings(const string& s, int n) {
        int count = 0, sum = 0;
        unordered_map<int, int> mp;
        mp[0] = 1;
        for (int i = 0; i < n; ++i) {
            sum += s[i] - '0';
            int key = sum - (i + 1);
            count += mp[key];
            mp[key]++;
        }
        return count;
    }
};"""
    },

    98: {
        "starter_code_java": "class Solution {\n    public int smallest_num(int[] xs) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int smallest_num(int[] xs) {
        int m = xs[0];
        for (int x : xs) if (x < m) m = x;
        return m;
    }
}"""
    },

    99: {
        "starter_code_javascript": "function max_difference(test_list) {\n    return 0;\n}",
        "reference_solution_javascript": """function max_difference(test_list) {
    let mx = 0;
    for (const [a, b] of test_list) {
        const d = Math.abs(b - a);
        if (d > mx) mx = d;
    }
    return mx;
}""",
        "starter_code_java": "class Solution {\n    public int max_difference(int[][] test_list) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int max_difference(int[][] test_list) {
        int mx = 0;
        for (int[] p : test_list) {
            int d = Math.abs(p[1] - p[0]);
            if (d > mx) mx = d;
        }
        return mx;
    }
}""",
        "starter_code_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    int max_difference(const vector<vector<int>>& test_list) {\n        return 0;\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <cmath>
#include <algorithm>
using namespace std;
class Solution {
public:
    int max_difference(const vector<vector<int>>& test_list) {
        int mx = 0;
        for (const auto& p : test_list) {
            mx = max(mx, abs(p[1] - p[0]));
        }
        return mx;
    }
};"""
    },

    100: {
        "starter_code_javascript": "function subject_marks(subjectmarks) {\n    return [];\n}",
        "reference_solution_javascript": """function subject_marks(subjectmarks) {
    const copy = subjectmarks.slice();
    copy.sort((a, b) => a[1] - b[1]);
    return copy;
}""",
        "starter_code_java": "class Solution {\n    public Object[][] subject_marks(Object[][] subjectmarks) {\n        return new Object[][]{};\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public Object[][] subject_marks(Object[][] subjectmarks) {
        Object[][] copy = subjectmarks.clone();
        Arrays.sort(copy, (a, b) -> Integer.compare(((Number) a[1]).intValue(), ((Number) b[1]).intValue()));
        return copy;
    }
}""",
        "starter_code_cpp": "#include <vector>\n#include <string>\nusing namespace std;\nclass Solution {\npublic:\n    vector<vector<string>> subject_marks(vector<vector<string>> subjectmarks) {\n        return {};\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <algorithm>
using namespace std;
class Solution {
public:
    vector<vector<string>> subject_marks(vector<vector<string>> subjectmarks) {
        stable_sort(subjectmarks.begin(), subjectmarks.end(), [](const vector<string>& a, const vector<string>& b) {
            return stoi(a[1]) < stoi(b[1]);
        });
        return subjectmarks;
    }
};"""
    },

    101: {
        "starter_code_java": "class Solution {\n    public int recursive_list_sum(Object[] data_list) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int recursive_list_sum(Object[] data_list) {
        int total = 0;
        for (Object el : data_list) {
            if (el instanceof Object[]) {
                total += recursive_list_sum((Object[]) el);
            } else if (el instanceof int[]) {
                for (int x : (int[]) el) total += x;
            } else if (el instanceof Number) {
                total += ((Number) el).intValue();
            }
        }
        return total;
    }
}""",
        "starter_code_cpp": "#include <vector>\n#include <string>\nusing namespace std;\nclass Solution {\npublic:\n    int recursive_list_sum(const vector<string>& data_list) {\n        return 0;\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <cctype>
using namespace std;
class Solution {
public:
    int recursive_list_sum(const vector<string>& data_list) {
        int total = 0;
        for (const auto& s : data_list) {
            string num = "";
            for (char c : s) {
                if (isdigit(c)) num += c;
                else if (!num.empty()) {
                    total += stoi(num);
                    num = "";
                }
            }
            if (!num.empty()) total += stoi(num);
        }
        return total;
    }
};"""
    },

    103: {
        "starter_code_javascript": "function bell_number(n) {\n    return 0;\n}",
        "reference_solution_javascript": """function bell_number(n) {
    const bell = Array.from({length: n + 1}, () => new Array(n + 1).fill(0n));
    bell[0][0] = 1n;
    for (let i = 1; i <= n; i++) {
        bell[i][0] = bell[i - 1][i - 1];
        for (let j = 1; j <= i; j++) {
            bell[i][j] = bell[i - 1][j - 1] + bell[i][j - 1];
        }
    }
    return bell[n][0];
}""",
        "starter_code_java": "import java.math.BigInteger;\nclass Solution {\n    public BigInteger bell_number(int n) {\n        return BigInteger.ZERO;\n    }\n}",
        "reference_solution_java": """import java.math.BigInteger;
class Solution {
    public BigInteger bell_number(int n) {
        BigInteger[][] bell = new BigInteger[n + 1][n + 1];
        bell[0][0] = BigInteger.ONE;
        for (int i = 1; i <= n; i++) {
            bell[i][0] = bell[i - 1][i - 1];
            for (int j = 1; j <= i; j++) {
                bell[i][j] = bell[i - 1][j - 1].add(bell[i][j - 1]);
            }
        }
        return bell[n][0];
    }
}""",
        "starter_code_cpp": "#include <string>\nusing namespace std;\nclass Solution {\npublic:\n    string bell_number(int n) {\n        return \"\";\n    }\n};",
        "reference_solution_cpp": """#include <string>
#include <vector>
#include <algorithm>
using namespace std;
class Solution {
    string addStr(const string& a, const string& b) {
        string res = "";
        int i = (int)a.length() - 1, j = (int)b.length() - 1, carry = 0;
        while (i >= 0 || j >= 0 || carry) {
            int s = carry;
            if (i >= 0) s += a[i--] - '0';
            if (j >= 0) s += b[j--] - '0';
            res += (s % 10) + '0';
            carry = s / 10;
        }
        reverse(res.begin(), res.end());
        return res.empty() ? "0" : res;
    }
public:
    string bell_number(int n) {
        vector<vector<string>> bell(n + 1, vector<string>(n + 1, "0"));
        bell[0][0] = "1";
        for (int i = 1; i <= n; ++i) {
            bell[i][0] = bell[i - 1][i - 1];
            for (int j = 1; j <= i; ++j) {
                bell[i][j] = addStr(bell[i - 1][j - 1], bell[i][j - 1]);
            }
        }
        return bell[n][0];
    }
};"""
    },

    104: {
        "starter_code_java": "class Solution {\n    public boolean is_Monotonic(int[] A) {\n        return false;\n    }\n}",
        "reference_solution_java": """class Solution {
    public boolean is_Monotonic(int[] A) {
        boolean inc = true, dec = true;
        for (int i = 0; i < A.length - 1; i++) {
            if (A[i] > A[i + 1]) inc = false;
            if (A[i] < A[i + 1]) dec = false;
        }
        return inc || dec;
    }
}""",
        "starter_code_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    bool is_Monotonic(const vector<int>& A) {\n        return false;\n    }\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    bool is_Monotonic(const vector<int>& A) {
        bool inc = true, dec = true;
        for (size_t i = 0; i + 1 < A.size(); ++i) {
            if (A[i] > A[i + 1]) inc = false;
            if (A[i] < A[i + 1]) dec = false;
        }
        return inc || dec;
    }
};"""
    },

    105: {
        "starter_code_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    bool is_sublist(const vector<int>& l, const vector<int>& s) {\n        return false;\n    }\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    bool is_sublist(const vector<int>& l, const vector<int>& s) {
        if (s.empty()) return true;
        if (s.size() > l.size()) return false;
        for (size_t i = 0; i + s.size() <= l.size(); ++i) {
            bool ok = true;
            for (size_t j = 0; j < s.size(); ++j) {
                if (l[i + j] != s[j]) { ok = false; break; }
            }
            if (ok) return true;
        }
        return false;
    }
};"""
    },

    106: {
        "starter_code_java": "class Solution {\n    public String get_equal(int[][] Input, int k) {\n        return \"\";\n    }\n}",
        "reference_solution_java": """class Solution {
    public String get_equal(int[][] Input, int k) {
        for (int[] t : Input) {
            if (t.length != k) return "All tuples do not have same length";
        }
        return "All tuples have same length";
    }
}"""
    },

    107: {
        "starter_code_javascript": "function comb_sort(nums) {\n    return [];\n}",
        "reference_solution_javascript": """function comb_sort(nums) {
    const copy = nums.slice();
    copy.sort((a, b) => a - b);
    return copy;
}""",
        "starter_code_java": "class Solution {\n    public int[] comb_sort(int[] nums) {\n        return new int[]{};\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[] comb_sort(int[] nums) {
        int[] copy = nums.clone();
        Arrays.sort(copy);
        return copy;
    }
}""",
        "starter_code_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    vector<int> comb_sort(vector<int> nums) {\n        return {};\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    vector<int> comb_sort(vector<int> nums) {
        sort(nums.begin(), nums.end());
        return nums;
    }
};"""
    },

    109: {
        "starter_code_javascript": "function multiple_split(text) {\n    return [];\n}",
        "reference_solution_javascript": """function multiple_split(text) {
    return text.split(/; |, |\\*|\\n/);
}""",
        "starter_code_java": "class Solution {\n    public String[] multiple_split(String text) {\n        return new String[]{};\n    }\n}",
        "reference_solution_java": """class Solution {
    public String[] multiple_split(String text) {
        return text.split("; |, |\\\\*|\\n");
    }
}""",
        "starter_code_cpp": "#include <vector>\n#include <string>\n#include <regex>\nusing namespace std;\nclass Solution {\npublic:\n    vector<string> multiple_split(const string& text) {\n        regex re(\"; |, |\\\\*|\\n\");\n        sregex_token_iterator it(text.begin(), text.end(), re, -1);\n        sregex_token_iterator reg_end;\n        vector<string> res;\n        for (; it != reg_end; ++it) res.push_back(*it);\n        return res;\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <regex>
using namespace std;
class Solution {
public:
    vector<string> multiple_split(const string& text) {
        regex re(\"; |, |\\\\*|\\n\");\n        sregex_token_iterator it(text.begin(), text.end(), re, -1);\n        sregex_token_iterator reg_end;\n        vector<string> res;\n        for (; it != reg_end; ++it) res.push_back(*it);\n        return res;\n    }\n};"""
    },

    110: {
        "starter_code_java": "class Solution {\n    public boolean is_samepatterns(String[] colors, String[] patterns) {\n        return false;\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public boolean is_samepatterns(String[] colors, String[] patterns) {
        if (colors.length != patterns.length) return false;
        Map<String, String> pToC = new HashMap<>();
        Map<String, String> cToP = new HashMap<>();
        for (int i = 0; i < patterns.length; i++) {
            String p = patterns[i], c = colors[i];
            if (pToC.containsKey(p) && !pToC.get(p).equals(c)) return false;
            if (cToP.containsKey(c) && !cToP.get(c).equals(p)) return false;
            pToC.put(p, c);
            cToP.put(c, p);
        }
        return true;
    }
}""",
        "starter_code_cpp": "#include <vector>\n#include <string>\nusing namespace std;\nclass Solution {\npublic:\n    bool is_samepatterns(const vector<string>& colors, const vector<string>& patterns) {\n        return false;\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <unordered_map>
using namespace std;
class Solution {
public:
    bool is_samepatterns(const vector<string>& colors, const vector<string>& patterns) {
        if (colors.size() != patterns.size()) return false;
        unordered_map<string, string> pToC, cToP;
        for (size_t i = 0; i < patterns.size(); ++i) {
            const string& p = patterns[i];
            const string& c = colors[i];
            if (pToC.count(p) && pToC[p] != c) return false;
            if (cToP.count(c) && cToP[c] != p) return false;
            pToC[p] = c;
            cToP[c] = p;
        }
        return true;
    }
};"""
    }
}
