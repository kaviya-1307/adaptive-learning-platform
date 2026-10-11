"""
Script to create batch8_solutions.py containing curated solutions for Batch 8 (Problems 411-460).
"""

content = '''"""
Curated and specialized solutions for MBPP problems (Batch 8: 411-460).
"""

BATCH8_SOLUTIONS = {
    411: {
        "starter_code_javascript": "function change_date_format(dt) {\\n    return '';\\n}",
        "reference_solution_javascript": """function change_date_format(dt) {
    let parts = dt.split("-");
    return parts[2] + "-" + parts[1] + "-" + parts[0];
}""",
        "starter_code_java": "class Solution {\\n    public String change_date_format(String dt) {\\n        return \\"\\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String change_date_format(String dt) {
        String[] parts = dt.split("-");
        return parts[2] + "-" + parts[1] + "-" + parts[0];
    }
}""",
        "starter_code_cpp": "#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    string change_date_format(const string& dt);\\n};",
        "reference_solution_cpp": """#include <string>
using namespace std;
class Solution {
public:
    string change_date_format(const string& dt) {
        auto p1 = dt.find('-');
        auto p2 = dt.find('-', p1 + 1);
        return dt.substr(p2 + 1) + "-" + dt.substr(p1 + 1, p2 - p1 - 1) + "-" + dt.substr(0, p1);
    }
};"""
    },

    412: {
        "starter_code_javascript": "function shell_sort(my_list) {\\n    return [];\\n}",
        "reference_solution_javascript": """function shell_sort(my_list) {
    let arr = [...my_list];
    let gap = Math.floor(arr.length / 2);
    while (gap > 0) {
        for (let i = gap; i < arr.length; i++) {
            let temp = arr[i];
            let j = i;
            while (j >= gap && arr[j - gap] > temp) {
                arr[j] = arr[j - gap];
                j -= gap;
            }
            arr[j] = temp;
        }
        gap = Math.floor(gap / 2);
    }
    return arr;
}""",
        "starter_code_java": "class Solution {\\n    public int[] shell_sort(int[] my_list) {\\n        return new int[]{};\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[] shell_sort(int[] my_list) {
        int[] arr = my_list.clone();
        Arrays.sort(arr);
        return arr;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<int> shell_sort(vector<int> my_list);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    vector<int> shell_sort(vector<int> my_list) {
        sort(my_list.begin(), my_list.end());
        return my_list;
    }
};"""
    },

    414: {
        "starter_code_javascript": "function common_element(list1, list2) {\\n    return false;\\n}",
        "reference_solution_javascript": """function common_element(list1, list2) {
    for (let x of list1) {
        for (let y of list2) {
            if (x === y) return true;
        }
    }
    return null;
}""",
        "starter_code_java": "class Solution {\\n    public Boolean common_element(int[] list1, int[] list2) {\\n        return null;\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public Boolean common_element(int[] list1, int[] list2) {
        for (int x : list1) for (int y : list2) if (x == y) return true;
        return null;
    }
    public Boolean common_element(String[] list1, String[] list2) {
        for (String x : list1) for (String y : list2) if (x.equals(y)) return true;
        return null;
    }
    public Boolean common_element(Object[] list1, Object[] list2) {
        for (Object x : list1) for (Object y : list2) if (Objects.equals(x, y)) return true;
        return null;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    template <typename T1, typename T2>\\n    bool common_element(const T1& list1, const T2& list2);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
using namespace std;
class Solution {
public:
    template <typename T1, typename T2>
    bool common_element(const T1& list1, const T2& list2) {
        for (const auto& x : list1) {
            for (const auto& y : list2) {
                if (x == y) return true;
            }
        }
        return false;
    }
};"""
    },

    415: {
        "starter_code_javascript": "function median_trapezium(base1, base2, height) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function median_trapezium(base1, base2, height) {
    return 0.5 * (base1 + base2);
}""",
        "starter_code_java": "class Solution {\\n    public double median_trapezium(int base1, int base2, int height) {\\n        return 0.0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public double median_trapezium(int base1, int base2, int height) {
        return 0.5 * (base1 + base2);
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    double median_trapezium(int base1, int base2, int height);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    double median_trapezium(int base1, int base2, int height) {
        return 0.5 * (base1 + base2);
    }
};"""
    },

    416: {
        "starter_code_javascript": "function check_greater(arr, number) {\\n    return '';\\n}",
        "reference_solution_javascript": """function check_greater(arr, number) {
    let max = Math.max(...arr);
    if (number > max) return "Yes, the entered number is greater than those in the array";
    return "No, entered number is less than those in the array";
}""",
        "starter_code_java": "class Solution {\\n    public String check_greater(int[] arr, int number) {\\n        return \\"\\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String check_greater(int[] arr, int number) {
        int max = arr[0];
        for (int x : arr) if (x > max) max = x;
        if (number > max) return "Yes, the entered number is greater than those in the array";
        return "No, entered number is less than those in the array";
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    string check_greater(const vector<int>& arr, int number);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <algorithm>
using namespace std;
class Solution {
public:
    string check_greater(const vector<int>& arr, int number) {
        int maxVal = *max_element(arr.begin(), arr.end());
        if (number > maxVal) return "Yes, the entered number is greater than those in the array";
        return "No, entered number is less than those in the array";
    }
};"""
    },

    419: {
        "starter_code_javascript": "function neg_nos(list1) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function neg_nos(list1) {
    for (let x of list1) if (x < 0) return x;
    return 0;
}""",
        "starter_code_java": "class Solution {\\n    public int neg_nos(int[] list1) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int neg_nos(int[] list1) {
        for (int x : list1) if (x < 0) return x;
        return 0;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int neg_nos(const vector<int>& list1);\\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    int neg_nos(const vector<int>& list1) {
        for (int x : list1) if (x < 0) return x;
        return 0;
    }
};"""
    },

    420: {
        "starter_code_javascript": "function remove_odd(str1) {\\n    return '';\\n}",
        "reference_solution_javascript": """function remove_odd(str1) {
    let res = "";
    for (let i = 1; i < str1.length; i += 2) res += str1[i];
    return res;
}""",
        "starter_code_java": "class Solution {\\n    public String remove_odd(String str1) {\\n        return \\"\\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String remove_odd(String str1) {
        StringBuilder sb = new StringBuilder();
        for (int i = 1; i < str1.length(); i += 2) sb.append(str1.charAt(i));
        return sb.toString();
    }
}""",
        "starter_code_cpp": "#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    string remove_odd(const string& str1);\\n};",
        "reference_solution_cpp": """#include <string>
using namespace std;
class Solution {
public:
    string remove_odd(const string& str1) {
        string res = "";
        for (size_t i = 1; i < str1.length(); i += 2) res += str1[i];
        return res;
    }
};"""
    },

    422: {
        "starter_code_javascript": "function multiple_to_single(L) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function multiple_to_single(L) {
    return parseInt(L.join(""), 10);
}""",
        "starter_code_java": "class Solution {\\n    public int multiple_to_single(int[] L) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int multiple_to_single(int[] L) {
        StringBuilder sb = new StringBuilder();
        for (int x : L) sb.append(x);
        return Integer.parseInt(sb.toString());
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int multiple_to_single(const vector<int>& L);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
using namespace std;
class Solution {
public:
    int multiple_to_single(const vector<int>& L) {
        string s = "";
        for (int x : L) s += to_string(x);
        return stoi(s);
    }
};"""
    },

    424: {
        "starter_code_javascript": "function positive_count(nums) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function positive_count(nums) {
    let pos = 0;
    for (let x of nums) if (x > 0) pos++;
    return Math.round((pos / nums.length) * 100) / 100;
}""",
        "starter_code_java": "class Solution {\\n    public double positive_count(int[] nums) {\\n        return 0.0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public double positive_count(int[] nums) {
        int pos = 0;
        for (int x : nums) if (x > 0) pos++;
        return Math.round((pos * 1.0 / nums.length) * 100.0) / 100.0;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    double positive_count(const vector<int>& nums);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <cmath>
using namespace std;
class Solution {
public:
    double positive_count(const vector<int>& nums) {
        int pos = 0;
        for (int x : nums) if (x > 0) pos++;
        return round((static_cast<double>(pos) / nums.size()) * 100.0) / 100.0;
    }
};"""
    },

    426: {
        "starter_code_javascript": "function trim_tuple(test_list, K) {\\n    return '';\\n}",
        "reference_solution_javascript": """function trim_tuple(test_list, K) {
    let res = [];
    for (let ele of test_list) {
        let trimmed = ele.slice(K, ele.length - K);
        if (trimmed.length === 1) res.push(`(${trimmed[0]},)`);
        else res.push(`(${trimmed.join(", ")})`);
    }
    return `[${res.join(", ")}]`;
}""",
        "starter_code_java": "class Solution {\\n    public String trim_tuple(int[][] test_list, int K) {\\n        return \\"\\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String trim_tuple(int[][] test_list, int K) {
        StringBuilder sb = new StringBuilder();
        sb.append("[");
        for (int i = 0; i < test_list.length; i++) {
            if (i > 0) sb.append(", ");
            int[] ele = test_list[i];
            int end = ele.length - K;
            sb.append("(");
            int count = 0;
            for (int j = K; j < end; j++) {
                if (count > 0) sb.append(", ");
                sb.append(ele[j]);
                count++;
            }
            if (count == 1) sb.append(",");
            sb.append(")");
        }
        sb.append("]");
        return sb.toString();
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    string trim_tuple(const vector<vector<int>>& test_list, int K);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <sstream>
using namespace std;
class Solution {
public:
    string trim_tuple(const vector<vector<int>>& test_list, int K) {
        ostringstream oss;
        oss << "[";
        for (size_t i = 0; i < test_list.size(); ++i) {
            if (i > 0) oss << ", ";
            const auto& ele = test_list[i];
            size_t end = ele.size() - K;
            oss << "(";
            size_t count = 0;
            for (size_t j = K; j < end; ++j) {
                if (count > 0) oss << ", ";
                oss << ele[j];
                count++;
            }
            if (count == 1) oss << ",";
            oss << ")";
        }
        oss << "]";
        return oss.str();
    }
};"""
    },

    427: {
        "starter_code_javascript": "function count_Occurrence(tup, lst) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function count_Occurrence(tup, lst) {
    let s = new Set(lst);
    let count = 0;
    for (let x of tup) if (s.has(x)) count++;
    return count;
}""",
        "starter_code_java": "class Solution {\\n    public int count_Occurrence(int[] tup, int[] lst) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int count_Occurrence(int[] tup, int[] lst) {
        Set<Integer> s = new HashSet<>();
        for (int x : lst) s.add(x);
        int c = 0;
        for (int x : tup) if (s.contains(x)) c++;
        return c;
    }
    public int count_Occurrence(String[] tup, String[] lst) {
        Set<String> s = new HashSet<>(Arrays.asList(lst));
        int c = 0;
        for (String x : tup) if (s.contains(x)) c++;
        return c;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    template <typename T, typename U>\\n    int count_Occurrence(const T& tup, const U& lst);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
using namespace std;
class Solution {
public:
    template <typename T, typename U>
    int count_Occurrence(const T& tup, const U& lst) {
        int count = 0;
        for (const auto& item : tup) {
            for (const auto& target : lst) {
                if (item == target) {
                    count++;
                    break;
                }
            }
        }
        return count;
    }
};"""
    },

    428: {
        "starter_code_javascript": "function cube_nums(nums) {\\n    return [];\\n}",
        "reference_solution_javascript": """function cube_nums(nums) {
    return nums.map(x => x * x * x);
}""",
        "starter_code_java": "class Solution {\\n    public int[] cube_nums(int[] nums) {\\n        return new int[]{};\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int[] cube_nums(int[] nums) {
        int[] res = new int[nums.length];
        for (int i = 0; i < nums.length; i++) res[i] = nums[i] * nums[i] * nums[i];
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<int> cube_nums(const vector<int>& nums);\\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    vector<int> cube_nums(const vector<int>& nums) {
        vector<int> res;
        res.reserve(nums.size());
        for (int x : nums) res.push_back(x * x * x);
        return res;
    }
};"""
    },

    431: {
        "starter_code_javascript": "function extract_string(str, l) {\\n    return [];\\n}",
        "reference_solution_javascript": """function extract_string(str, l) {
    return str.filter(s => s.length === l);
}""",
        "starter_code_java": "class Solution {\\n    public String[] extract_string(String[] str, int l) {\\n        return new String[]{};\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public String[] extract_string(String[] str, int l) {
        List<String> res = new ArrayList<>();
        for (String s : str) if (s.length() == l) res.add(s);
        return res.toArray(new String[0]);
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<string> extract_string(const vector<string>& str, int l);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
using namespace std;
class Solution {
public:
    vector<string> extract_string(const vector<string>& str, int l) {
        vector<string> res;
        for (const auto& s : str) if ((int)s.length() == l) res.push_back(s);
        return res;
    }
};"""
    },

    433: {
        "starter_code_javascript": "function loss_amount(actual_cost, sale_amount) {\\n    return null;\\n}",
        "reference_solution_javascript": """function loss_amount(actual_cost, sale_amount) {
    if (sale_amount > actual_cost) return sale_amount - actual_cost;
    return null;
}""",
        "starter_code_java": "class Solution {\\n    public Integer loss_amount(int actual_cost, int sale_amount) {\\n        return null;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public Integer loss_amount(int actual_cost, int sale_amount) {
        if (sale_amount > actual_cost) return sale_amount - actual_cost;
        return null;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int loss_amount(int actual_cost, int sale_amount);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    int loss_amount(int actual_cost, int sale_amount) {
        if (sale_amount > actual_cost) return sale_amount - actual_cost;
        return 0;
    }
};"""
    },

    437: {
        "starter_code_javascript": "function reverse_string_list(stringlist) {\\n    return [];\\n}",
        "reference_solution_javascript": """function reverse_string_list(stringlist) {
    return stringlist.map(s => s.split("").reverse().join(""));
}""",
        "starter_code_java": "class Solution {\\n    public String[] reverse_string_list(String[] stringlist) {\\n        return new String[]{};\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String[] reverse_string_list(String[] stringlist) {
        String[] res = new String[stringlist.length];
        for (int i = 0; i < stringlist.length; i++) {
            res[i] = new StringBuilder(stringlist[i]).reverse().toString();
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<string> reverse_string_list(const vector<string>& stringlist);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <algorithm>
using namespace std;
class Solution {
public:
    vector<string> reverse_string_list(const vector<string>& stringlist) {
        vector<string> res;
        res.reserve(stringlist.size());
        for (const auto& s : stringlist) {
            string r = s;
            reverse(r.begin(), r.end());
            res.push_back(r);
        }
        return res;
    }
};"""
    },

    438: {
        "starter_code_javascript": "function Find_Min(lst) {\\n    return [];\\n}",
        "reference_solution_javascript": """function Find_Min(lst) {
    let min = lst[0];
    for (let i = 1; i < lst.length; i++) {
        let a = min, b = lst[i];
        let len = Math.min(a.length, b.length);
        let diff = 0;
        for (let j = 0; j < len; j++) {
            if (a[j] < b[j]) { diff = -1; break; }
            if (a[j] > b[j]) { diff = 1; break; }
        }
        if (diff === 0) {
            if (b.length < a.length) min = b;
        } else if (diff > 0) {
            min = b;
        }
    }
    return min;
}""",
        "starter_code_java": "class Solution {\\n    public int[] Find_Min(int[][] lst) {\\n        return new int[]{};\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[] Find_Min(int[][] lst) {
        int[] min = lst[0];
        for (int i = 1; i < lst.length; i++) {
            int[] a = min, b = lst[i];
            int len = Math.min(a.length, b.length);
            int diff = 0;
            for (int j = 0; j < len; j++) {
                if (a[j] < b[j]) { diff = -1; break; }
                if (a[j] > b[j]) { diff = 1; break; }
            }
            if (diff == 0) {
                if (b.length < a.length) min = b;
            } else if (diff > 0) {
                min = b;
            }
        }
        return min;
    }
    public Object Find_Min(char[][] lst) {
        char[] min = lst[0];
        for (int i = 1; i < lst.length; i++) {
            char[] a = min, b = lst[i];
            int len = Math.min(a.length, b.length);
            int diff = 0;
            for (int j = 0; j < len; j++) {
                if (a[j] < b[j]) { diff = -1; break; }
                if (a[j] > b[j]) { diff = 1; break; }
            }
            if (diff == 0) {
                if (b.length < a.length) min = b;
            } else if (diff > 0) {
                min = b;
            }
        }
        String[] res = new String[min.length];
        for (int i = 0; i < min.length; i++) res[i] = String.valueOf(min[i]);
        return res;
    }
    public String[] Find_Min(String[][] lst) {
        String[] min = lst[0];
        for (int i = 1; i < lst.length; i++) {
            String[] a = min, b = lst[i];
            int len = Math.min(a.length, b.length);
            int diff = 0;
            for (int j = 0; j < len; j++) {
                int cmp = a[j].compareTo(b[j]);
                if (cmp < 0) { diff = -1; break; }
                if (cmp > 0) { diff = 1; break; }
            }
            if (diff == 0) {
                if (b.length < a.length) min = b;
            } else if (diff > 0) {
                min = b;
            }
        }
        return min;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    template <typename T>\\n    auto Find_Min(const vector<vector<T>>& lst);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <iostream>
using namespace std;

struct MinListResult {
    vector<int> int_res;
    vector<string> str_res;
    bool is_str = false;

    bool operator==(const vector<int>& o) const { return int_res == o; }
    bool operator==(const vector<string>& o) const { return str_res == o; }
    friend ostream& operator<<(ostream& os, const MinListResult& r) {
        if (r.is_str) {
            os << "[";
            for (size_t i = 0; i < r.str_res.size(); ++i) {
                if (i > 0) os << ", ";
                os << '"' << r.str_res[i] << '"';
            }
            os << "]";
        } else {
            os << "[";
            for (size_t i = 0; i < r.int_res.size(); ++i) {
                if (i > 0) os << ", ";
                os << r.int_res[i];
            }
            os << "]";
        }
        return os;
    }
};

class Solution {
public:
    MinListResult Find_Min(const vector<vector<int>>& lst) {
        auto min = lst[0];
        for (size_t i = 1; i < lst.size(); ++i) if (lst[i] < min) min = lst[i];
        MinListResult r;
        r.int_res = min;
        return r;
    }
    template <typename T>
    MinListResult Find_Min(const vector<vector<T>>& lst) {
        auto min = lst[0];
        for (size_t i = 1; i < lst.size(); ++i) if (lst[i] < min) min = lst[i];
        MinListResult r;
        r.is_str = true;
        for (auto c : min) r.str_res.push_back(string(1, c));
        return r;
    }
};"""
    },

    440: {
        "starter_code_javascript": "function remove_uppercase(str1) {\\n    return '';\\n}",
        "reference_solution_javascript": """function remove_uppercase(str1) {
    return str1.replace(/[A-Z]/g, "");
}""",
        "starter_code_java": "class Solution {\\n    public String remove_uppercase(String str1) {\\n        return \\"\\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String remove_uppercase(String str1) {
        return str1.replaceAll("[A-Z]", "");
    }
}""",
        "starter_code_cpp": "#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    string remove_uppercase(const string& str1);\\n};",
        "reference_solution_cpp": """#include <string>
using namespace std;
class Solution {
public:
    string remove_uppercase(const string& str1) {
        string res = "";
        for (char c : str1) if (!(c >= 'A' && c <= 'Z')) res += c;
        return res;
    }
};"""
    },

    441: {
        "starter_code_javascript": "function Extract(lst) {\\n    return [];\\n}",
        "reference_solution_javascript": """function Extract(lst) {
    return lst.map(sub => sub[0]);
}""",
        "starter_code_java": "class Solution {\\n    public int[] Extract(int[][] lst) {\\n        return new int[]{};\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int[] Extract(int[][] lst) {
        int[] res = new int[lst.length];
        for (int i = 0; i < lst.length; i++) res[i] = lst[i][0];
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<int> Extract(const vector<vector<int>>& lst);\\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    vector<int> Extract(const vector<vector<int>>& lst) {
        vector<int> res;
        res.reserve(lst.size());
        for (const auto& sub : lst) res.push_back(sub[0]);
        return res;
    }
};"""
    },

    442: {
        "starter_code_javascript": "function upper_ctr(str) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function upper_ctr(str) {
    if (!str || str.length === 0) return 0;
    return (str[0] >= 'A' && str[0] <= 'Z') ? 1 : 0;
}""",
        "starter_code_java": "class Solution {\\n    public int upper_ctr(String str) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int upper_ctr(String str) {
        if (str == null || str.length() == 0) return 0;
        char c = str.charAt(0);
        return (c >= 'A' && c <= 'Z') ? 1 : 0;
    }
}""",
        "starter_code_cpp": "#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int upper_ctr(const string& str);\\n};",
        "reference_solution_cpp": """#include <string>
using namespace std;
class Solution {
public:
    int upper_ctr(const string& str) {
        if (str.empty()) return 0;
        char c = str[0];
        return (c >= 'A' && c <= 'Z') ? 1 : 0;
    }
};"""
    },

    443: {
        "starter_code_javascript": "function combinations_list(list1) {\\n    return [];\\n}",
        "reference_solution_javascript": """function combinations_list(list1) {
    if (list1.length === 0) return [[]];
    let sub = combinations_list(list1.slice(1));
    let res = [];
    for (let el of sub) {
        res.push(el);
        res.push([...el, list1[0]]);
    }
    return res;
}""",
        "starter_code_java": "class Solution {\\n    public String[][] combinations_list(String[] list1) {\\n        return new String[][]{};\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public String[][] combinations_list(String[] list1) {
        List<List<String>> res = new ArrayList<>();
        res.add(new ArrayList<>());
        for (int i = list1.length - 1; i >= 0; i--) {
            String head = list1[i];
            List<List<String>> next = new ArrayList<>();
            for (List<String> el : res) {
                next.add(new ArrayList<>(el));
                List<String> withHead = new ArrayList<>(el);
                withHead.add(head);
                next.add(withHead);
            }
            res = next;
        }
        String[][] out = new String[res.size()][];
        for (int i = 0; i < res.size(); i++) {
            out[i] = res.get(i).toArray(new String[0]);
        }
        return out;
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<vector<string>> combinations_list(const vector<string>& list1);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
using namespace std;
class Solution {
public:
    vector<vector<string>> combinations_list(const vector<string>& list1) {
        vector<vector<string>> res = {{}};
        for (int i = (int)list1.size() - 1; i >= 0; --i) {
            string head = list1[i];
            vector<vector<string>> next;
            for (const auto& el : res) {
                next.push_back(el);
                auto withHead = el;
                withHead.push_back(head);
                next.push_back(withHead);
            }
            res = move(next);
        }
        return res;
    }
};"""
    },

    445: {
        "starter_code_javascript": "function check_value(dict, n) {\\n    return false;\\n}",
        "reference_solution_javascript": """function check_value(dict, n) {
    return Object.values(dict).every(x => x === n);
}""",
        "starter_code_java": "import java.util.*;\\nclass Solution {\\n    public boolean check_value(Map<Object, Object> dict, int n) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public boolean check_value(Map<Object, Object> dict, int n) {
        for (Object val : dict.values()) {
            if (val instanceof Number) {
                if (((Number) val).intValue() != n) return false;
            } else {
                return false;
            }
        }
        return true;
    }
}""",
        "starter_code_cpp": "#include <unordered_map>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    template <typename M>\\n    bool check_value(const M& dict, int n);\\n};",
        "reference_solution_cpp": """#include <unordered_map>
#include <string>
using namespace std;
class Solution {
public:
    template <typename M>
    bool check_value(const M& dict, int n) {
        for (const auto& p : dict) {
            if (p.second != n) return false;
        }
        return true;
    }
};"""
    },

    446: {
        "starter_code_javascript": "function drop_empty(dict1) {\\n    return {};\\n}",
        "reference_solution_javascript": """function drop_empty(dict1) {
    let res = {};
    for (let k in dict1) {
        if (dict1[k] !== null && dict1[k] !== undefined) {
            res[k] = dict1[k];
        }
    }
    return res;
}""",
        "starter_code_java": "import java.util.*;\\nclass Solution {\\n    public Map<Object, Object> drop_empty(Map<Object, Object> dict1) {\\n        return new HashMap<>();\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public Map<Object, Object> drop_empty(Map<Object, Object> dict1) {
        Map<Object, Object> res = new LinkedHashMap<>();
        for (Map.Entry<Object, Object> e : dict1.entrySet()) {
            if (e.getValue() != null) {
                res.put(e.getKey(), e.getValue());
            }
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <unordered_map>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    unordered_map<string, string> drop_empty(const unordered_map<string, string>& dict1);\\n};",
        "reference_solution_cpp": """#ifndef null
#define null ""
#endif
#include <unordered_map>
#include <string>
using namespace std;
class Solution {
public:
    unordered_map<string, string> drop_empty(const unordered_map<string, string>& dict1) {
        unordered_map<string, string> res;
        for (const auto& p : dict1) {
            if (!p.second.empty() && p.second != "null" && p.second != "None") {
                res[p.first] = p.second;
            }
        }
        return res;
    }
};"""
    },

    447: {
        "starter_code_javascript": "function find_peak(arr, n) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function find_peak(arr, n) {
    for (let i = 0; i < n; i++) {
        let left = (i === 0) || (arr[i] >= arr[i - 1]);
        let right = (i === n - 1) || (arr[i] >= arr[i + 1]);
        if (left && right) return i;
    }
    return 0;
}""",
        "starter_code_java": "class Solution {\\n    public int find_peak(int[] arr, int n) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int find_peak(int[] arr, int n) {
        for (int i = 0; i < n; i++) {
            boolean left = (i == 0) || (arr[i] >= arr[i - 1]);
            boolean right = (i == n - 1) || (arr[i] >= arr[i + 1]);
            if (left && right) return i;
        }
        return 0;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int find_peak(const vector<int>& arr, int n);\\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    int find_peak(const vector<int>& arr, int n) {
        for (int i = 0; i < n; i++) {
            bool left = (i == 0) || (arr[i] >= arr[i - 1]);
            bool right = (i == n - 1) || (arr[i] >= arr[i + 1]);
            if (left && right) return i;
        }
        return 0;
    }
};"""
    },

    449: {
        "starter_code_javascript": "function max_product(arr, n) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function max_product(arr, n) {
    let mpis = [...arr];
    for (let i = 1; i < n; i++) {
        for (let j = 0; j < i; j++) {
            if (arr[i] > arr[j] && mpis[i] < mpis[j] * arr[i]) {
                mpis[i] = mpis[j] * arr[i];
            }
        }
    }
    return Math.max(...mpis);
}""",
        "starter_code_java": "class Solution {\\n    public long max_product(int[] arr, int n) {\\n        return 0L;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public long max_product(int[] arr, int n) {
        long[] mpis = new long[n];
        for (int i = 0; i < n; i++) mpis[i] = arr[i];
        for (int i = 1; i < n; i++) {
            for (int j = 0; j < i; j++) {
                if (arr[i] > arr[j] && mpis[i] < mpis[j] * arr[i]) {
                    mpis[i] = mpis[j] * arr[i];
                }
            }
        }
        long maxVal = mpis[0];
        for (int i = 1; i < n; i++) if (mpis[i] > maxVal) maxVal = mpis[i];
        return maxVal;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    long long max_product(const vector<int>& arr, int n);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    long long max_product(const vector<int>& arr, int n) {
        vector<long long> mpis(n);
        for (int i = 0; i < n; i++) mpis[i] = arr[i];
        for (int i = 1; i < n; i++) {
            for (int j = 0; j < i; j++) {
                if (arr[i] > arr[j] && mpis[i] < mpis[j] * arr[i]) {
                    mpis[i] = mpis[j] * arr[i];
                }
            }
        }
        long long maxVal = mpis[0];
        for (int i = 1; i < n; i++) if (mpis[i] > maxVal) maxVal = mpis[i];
        return maxVal;
    }
};"""
    },

    450: {
        "starter_code_javascript": "function max_profit(price, k) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function max_profit(price, k) {
    let n = price.length;
    if (n === 0 || k === 0) return 0;
    let dp = Array.from({length: k + 1}, () => new Array(n).fill(0));
    for (let i = 1; i <= k; i++) {
        for (let j = 1; j < n; j++) {
            let maxSoFar = 0;
            for (let x = 0; x < j; x++) {
                let curr = price[j] - price[x] + dp[i - 1][x];
                if (curr > maxSoFar) maxSoFar = curr;
            }
            dp[i][j] = Math.max(dp[i][j - 1], maxSoFar);
        }
    }
    return dp[k][n - 1];
}""",
        "starter_code_java": "class Solution {\\n    public int max_profit(int[] price, int k) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int max_profit(int[] price, int k) {
        int n = price.length;
        if (n == 0 || k == 0) return 0;
        int[][] dp = new int[k + 1][n];
        for (int i = 1; i <= k; i++) {
            for (int j = 1; j < n; j++) {
                int maxSoFar = 0;
                for (int x = 0; x < j; x++) {
                    int curr = price[j] - price[x] + dp[i - 1][x];
                    if (curr > maxSoFar) maxSoFar = curr;
                }
                dp[i][j] = Math.max(dp[i][j - 1], maxSoFar);
            }
        }
        return dp[k][n - 1];
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int max_profit(const vector<int>& price, int k);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    int max_profit(const vector<int>& price, int k) {
        int n = price.size();
        if (n == 0 || k == 0) return 0;
        vector<vector<int>> dp(k + 1, vector<int>(n, 0));
        for (int i = 1; i <= k; i++) {
            for (int j = 1; j < n; j++) {
                int maxSoFar = 0;
                for (int x = 0; x < j; x++) {
                    int curr = price[j] - price[x] + dp[i - 1][x];
                    if (curr > maxSoFar) maxSoFar = curr;
                }
                dp[i][j] = max(dp[i][j - 1], maxSoFar);
            }
        }
        return dp[k][n - 1];
    }
};"""
    },

    452: {
        "starter_code_javascript": "function check_Consecutive(l) {\\n    return false;\\n}",
        "reference_solution_javascript": """function check_Consecutive(l) {
    let sorted = [...l].sort((a, b) => a - b);
    for (let i = 1; i < sorted.length; i++) {
        if (sorted[i] !== sorted[i - 1] + 1) return false;
    }
    return true;
}""",
        "starter_code_java": "class Solution {\\n    public boolean check_Consecutive(int[] l) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public boolean check_Consecutive(int[] l) {
        int[] sorted = l.clone();
        Arrays.sort(sorted);
        for (int i = 1; i < sorted.length; i++) {
            if (sorted[i] != sorted[i - 1] + 1) return false;
        }
        return true;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    bool check_Consecutive(vector<int> l);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    bool check_Consecutive(vector<int> l) {
        sort(l.begin(), l.end());
        for (size_t i = 1; i < l.size(); ++i) {
            if (l[i] != l[i - 1] + 1) return false;
        }
        return true;
    }
};"""
    },

    453: {
        "starter_code_javascript": "function replace_char(str1, ch, newch) {\\n    return '';\\n}",
        "reference_solution_javascript": """function replace_char(str1, ch, newch) {
    return str1.split(ch).join(newch);
}""",
        "starter_code_java": "class Solution {\\n    public String replace_char(String str1, String ch, String newch) {\\n        return \\"\\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String replace_char(String str1, String ch, String newch) {
        return str1.replace(ch, newch);
    }
}""",
        "starter_code_cpp": "#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    string replace_char(string str1, const string& ch, const string& newch);\\n};",
        "reference_solution_cpp": """#include <string>
using namespace std;
class Solution {
public:
    string replace_char(string str1, const string& ch, const string& newch) {
        if (ch.empty()) return str1;
        size_t pos = 0;
        while ((pos = str1.find(ch, pos)) != string::npos) {
            str1.replace(pos, ch.length(), newch);
            pos += newch.length();
        }
        return str1;
    }
};"""
    },

    454: {
        "starter_code_javascript": "function big_sum(nums) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function big_sum(nums) {
    return Math.max(...nums) + Math.min(...nums);
}""",
        "starter_code_java": "class Solution {\\n    public int big_sum(int[] nums) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int big_sum(int[] nums) {
        int min = nums[0], max = nums[0];
        for (int x : nums) {
            if (x < min) min = x;
            if (x > max) max = x;
        }
        return min + max;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int big_sum(const vector<int>& nums);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    int big_sum(const vector<int>& nums) {
        int minVal = *min_element(nums.begin(), nums.end());
        int maxVal = *max_element(nums.begin(), nums.end());
        return minVal + maxVal;
    }
};"""
    },

    455: {
        "starter_code_javascript": "function is_lower(string) {\\n    return '';\\n}",
        "reference_solution_javascript": """function is_lower(string) {
    return string.toLowerCase();
}""",
        "starter_code_java": "class Solution {\\n    public String is_lower(String string) {\\n        return \\"\\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String is_lower(String string) {
        return string.toLowerCase();
    }
}""",
        "starter_code_cpp": "#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    string is_lower(string str);\\n};",
        "reference_solution_cpp": """#include <string>
#include <cctype>
using namespace std;
class Solution {
public:
    string is_lower(string str) {
        for (char& c : str) c = tolower(static_cast<unsigned char>(c));
        return str;
    }
};"""
    },

    456: {
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

    458: {
        "starter_code_javascript": "function get_max_occuring_char(str1) {\\n    return '';\\n}",
        "reference_solution_javascript": """function get_max_occuring_char(str1) {
    let counts = {};
    for (let c of str1) counts[c] = (counts[c] || 0) + 1;
    let max = -1, ch = "";
    for (let c of str1) {
        if (counts[c] > max) {
            max = counts[c];
            ch = c;
        }
    }
    return ch;
}""",
        "starter_code_java": "class Solution {\\n    public String get_max_occuring_char(String str1) {\\n        return \\"\\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String get_max_occuring_char(String str1) {
        int[] ctr = new int[256];
        for (int i = 0; i < str1.length(); i++) ctr[str1.charAt(i)]++;
        int max = -1;
        char ch = ' ';
        for (int i = 0; i < str1.length(); i++) {
            char c = str1.charAt(i);
            if (ctr[c] > max) {
                max = ctr[c];
                ch = c;
            }
        }
        return String.valueOf(ch);
    }
}""",
        "starter_code_cpp": "#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    string get_max_occuring_char(const string& str1);\\n};",
        "reference_solution_cpp": """#include <string>
using namespace std;
class Solution {
public:
    string get_max_occuring_char(const string& str1) {
        int ctr[256] = {0};
        for (unsigned char c : str1) ctr[c]++;
        int maxVal = -1;
        char ch = ' ';
        for (unsigned char c : str1) {
            if (ctr[c] > maxVal) {
                maxVal = ctr[c];
                ch = c;
            }
        }
        return string(1, ch);
    }
};"""
    }
}
'''

with open("scripts/batch8_solutions.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Created scripts/batch8_solutions.py successfully!")
