"""
Curated and specialized solutions for MBPP problems (Batch 15: 761-810).
"""

BATCH15_SOLUTIONS = {
    761: {
        "starter_code_javascript": "function check_Type_Of_Triangle(a, b, c) {\n    return '';\n}",
        "reference_solution_javascript": """function check_Type_Of_Triangle(a, b, c) {
    let sqa = a * a, sqb = b * b, sqc = c * c;
    if (sqa === sqa + sqb || sqb === sqa + sqc || sqc === sqa + sqb) return "Right-angled Triangle";
    else if (sqa > sqc + sqb || sqb > sqa + sqc || sqc > sqa + sqb) return "Obtuse-angled Triangle";
    else return "Acute-angled Triangle";
}""",
        "starter_code_java": "class Solution {\n    public String check_Type_Of_Triangle(int a, int b, int c) {\n        return "";\n    }\n}",
        "reference_solution_java": """class Solution {
    public String check_Type_Of_Triangle(int a, int b, int c) {
        long sqa = (long) a * a, sqb = (long) b * b, sqc = (long) c * c;
        if (sqa == sqa + sqb || sqb == sqa + sqc || sqc == sqa + sqb) return "Right-angled Triangle";
        else if (sqa > sqc + sqb || sqb > sqa + sqc || sqc > sqa + sqb) return "Obtuse-angled Triangle";
        else return "Acute-angled Triangle";
    }
}""",
        "starter_code_cpp": "#include <string>\nclass Solution {\npublic:\n    std::string check_Type_Of_Triangle(int a, int b, int c);\n};",
        "reference_solution_cpp": """#include <string>
class Solution {
public:
    std::string check_Type_Of_Triangle(int a, int b, int c) {
        long long sqa = 1LL * a * a, sqb = 1LL * b * b, sqc = 1LL * c * c;
        if (sqa == sqa + sqb || sqb == sqa + sqc || sqc == sqa + sqb) return "Right-angled Triangle";
        else if (sqa > sqc + sqb || sqb > sqa + sqc || sqc > sqa + sqb) return "Obtuse-angled Triangle";
        else return "Acute-angled Triangle";
    }
};"""
    },

    762: {
        "starter_code_javascript": "function sum_column(list1, C) {\n    return 0;\n}",
        "reference_solution_javascript": """function sum_column(list1, C) {
    let sum = 0;
    for (let row of list1) sum += row[C];
    return sum;
}""",
        "starter_code_java": "class Solution {\n    public int sum_column(int[][] list1, int C) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int sum_column(int[][] list1, int C) {
        int sum = 0;
        for (int[] row : list1) sum += row[C];
        return sum;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    int sum_column(std::vector<std::vector<int>> list1, int C);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    int sum_column(std::vector<std::vector<int>> list1, int C) {
        int sum = 0;
        for (const auto& row : list1) sum += row[C];
        return sum;
    }
};"""
    },

    763: {
        "starter_code_javascript": "function second_frequent(input) {\n    return '';\n}",
        "reference_solution_javascript": """function second_frequent(input) {
    const counts = new Map();
    for (let s of input) counts.set(s, (counts.get(s) || 0) + 1);
    const vals = [...counts.values()].sort((a, b) => b - a);
    const target = vals[1];
    for (let [k, v] of counts.entries()) {
        if (v === target) return k;
    }
    return "";
}""",
        "starter_code_java": "import java.util.*;\nclass Solution {\n    public String second_frequent(String[] input) {\n        return "";\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public String second_frequent(String[] input) {
        Map<String, Integer> counts = new LinkedHashMap<>();
        for (String s : input) counts.put(s, counts.getOrDefault(s, 0) + 1);
        List<Integer> vals = new ArrayList<>(counts.values());
        vals.sort(Collections.reverseOrder());
        int target = vals.get(1);
        for (Map.Entry<String, Integer> e : counts.entrySet()) {
            if (e.getValue() == target) return e.getKey();
        }
        return "";
    }
}""",
        "starter_code_cpp": "#include <vector>\n#include <string>\nclass Solution {\npublic:\n    std::string second_frequent(std::vector<std::string> input);\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <unordered_map>
#include <algorithm>
class Solution {
public:
    std::string second_frequent(std::vector<std::string> input) {
        std::unordered_map<std::string, int> counts;
        std::vector<std::string> order;
        for (const auto& s : input) {
            if (counts.find(s) == counts.end()) order.push_back(s);
            counts[s]++;
        }
        std::vector<int> vals;
        for (const auto& p : counts) vals.push_back(p.second);
        std::sort(vals.rbegin(), vals.rend());
        int target = vals[1];
        for (const auto& s : order) {
            if (counts[s] == target) return s;
        }
        return "";
    }
};"""
    },

    764: {
        "starter_code_javascript": "function round_up(a, digits) {\n    return 0;\n}",
        "reference_solution_javascript": """function round_up(a, digits) {
    let factor = Math.pow(10, digits);
    return Math.ceil(a * factor) / factor;
}""",
        "starter_code_java": "class Solution {\n    public double round_up(double a, int digits) {\n        return 0.0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public double round_up(double a, int digits) {
        double factor = Math.pow(10, digits);
        return Math.ceil(a * factor) / factor;
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    double round_up(double a, int digits);\n};",
        "reference_solution_cpp": """#include <cmath>
class Solution {
public:
    double round_up(double a, int digits) {
        double factor = std::pow(10.0, digits);
        return std::ceil(a * factor) / factor;
    }
};"""
    },

    765: {
        "starter_code_javascript": "function count_Pairs(arr, n) {\n    return 0;\n}",
        "reference_solution_javascript": """function count_Pairs(arr, n) {
    let cnt = 0;
    for (let i = 0; i < n; i++) {
        for (let j = i + 1; j < n; j++) {
            if (arr[i] === arr[j]) cnt++;
        }
    }
    return cnt;
}""",
        "starter_code_java": "class Solution {\n    public int count_Pairs(int[] arr, int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int count_Pairs(int[] arr, int n) {
        int cnt = 0;
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                if (arr[i] == arr[j]) cnt++;
            }
        }
        return cnt;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    int count_Pairs(std::vector<int> arr, int n);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    int count_Pairs(std::vector<int> arr, int n) {
        int cnt = 0;
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                if (arr[i] == arr[j]) cnt++;
            }
        }
        return cnt;
    }
};"""
    },

    766: {
        "starter_code_javascript": "function extract_max(input) {\n    return 0;\n}",
        "reference_solution_javascript": """function extract_max(input) {
    const nums = input.match(/\\d+/g).map(Number);
    return Math.max(...nums);
}""",
        "starter_code_java": "class Solution {\n    public int extract_max(String input) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int extract_max(String input) {
        int max = -1;
        int cur = 0;
        boolean inNum = false;
        for (char c : input.toCharArray()) {
            if (Character.isDigit(c)) {
                cur = cur * 10 + (c - '0');
                inNum = true;
            } else {
                if (inNum) {
                    if (cur > max) max = cur;
                    cur = 0;
                    inNum = false;
                }
            }
        }
        if (inNum && cur > max) max = cur;
        return max;
    }
}""",
        "starter_code_cpp": "#include <string>\nclass Solution {\npublic:\n    int extract_max(std::string input);\n};",
        "reference_solution_cpp": """#include <string>
#include <cctype>
#include <algorithm>
class Solution {
public:
    int extract_max(std::string input) {
        int maxVal = -1;
        int cur = 0;
        bool inNum = false;
        for (char c : input) {
            if (isdigit((unsigned char)c)) {
                cur = cur * 10 + (c - '0');
                inNum = true;
            } else {
                if (inNum) {
                    maxVal = std::max(maxVal, cur);
                    cur = 0;
                    inNum = false;
                }
            }
        }
        if (inNum) maxVal = std::max(maxVal, cur);
        return maxVal;
    }
};"""
    },

    767: {
        "starter_code_javascript": "function get_key(dict) {\n    return [];\n}",
        "reference_solution_javascript": """function get_key(dict) {
    return Object.keys(dict).map(Number).sort((a, b) => a - b);
}""",
        "starter_code_java": "import java.util.*;\nclass Solution {\n    public int[] get_key(Map<Object, Object> dict) {\n        return new int[]{};\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[] get_key(Map<Object, Object> dict) {
        List<Integer> list = new ArrayList<>();
        for (Object k : dict.keySet()) {
            list.add(Integer.parseInt(k.toString()));
        }
        Collections.sort(list);
        int[] res = new int[list.size()];
        for (int i = 0; i < list.size(); i++) res[i] = list.get(i);
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\n#include <string>\n#include <unordered_map>\nclass Solution {\npublic:\n    std::vector<int> get_key(std::unordered_map<std::string, std::string> dict);\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <unordered_map>
#include <algorithm>
class Solution {
public:
    std::vector<int> get_key(std::unordered_map<std::string, std::string> dict) {
        std::vector<int> res;
        for (const auto& p : dict) res.push_back(std::stoi(p.first));
        std::sort(res.begin(), res.end());
        return res;
    }
};"""
    },

    768: {
        "starter_code_javascript": "function generate_matrix(n) {\n    return [];\n}",
        "reference_solution_javascript": """function generate_matrix(n) {
    if (n <= 0) return [];
    let matrix = Array.from({ length: n }, () => new Array(n).fill(0));
    let top = 0, bottom = n - 1, left = 0, right = n - 1;
    let cur = 1;
    while (cur <= n * n) {
        for (let c = left; c <= right; c++) matrix[top][c] = cur++;
        top++;
        for (let r = top; r <= bottom; r++) matrix[r][right] = cur++;
        right--;
        for (let c = right; c >= left; c--) matrix[bottom][c] = cur++;
        bottom--;
        for (let r = bottom; r >= top; r--) matrix[r][left] = cur++;
        left++;
    }
    return matrix;
}""",
        "starter_code_java": "class Solution {\n    public int[][] generate_matrix(int n) {\n        return new int[][]{};\n    }\n}",
        "reference_solution_java": """class Solution {
    public int[][] generate_matrix(int n) {
        if (n <= 0) return new int[0][0];
        int[][] matrix = new int[n][n];
        int top = 0, bottom = n - 1, left = 0, right = n - 1;
        int cur = 1;
        while (cur <= n * n) {
            for (int c = left; c <= right; c++) matrix[top][c] = cur++;
            top++;
            for (int r = top; r <= bottom; r++) matrix[r][right] = cur++;
            right--;
            for (int c = right; c >= left; c--) matrix[bottom][c] = cur++;
            bottom--;
            for (int r = bottom; r >= top; r--) matrix[r][left] = cur++;
            left++;
        }
        return matrix;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    std::vector<std::vector<int>> generate_matrix(int n);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    std::vector<std::vector<int>> generate_matrix(int n) {
        if (n <= 0) return {};
        std::vector<std::vector<int>> matrix(n, std::vector<int>(n, 0));
        int top = 0, bottom = n - 1, left = 0, right = n - 1;
        int cur = 1;
        while (cur <= n * n) {
            for (int c = left; c <= right; c++) matrix[top][c] = cur++;
            top++;
            for (int r = top; r <= bottom; r++) matrix[r][right] = cur++;
            right--;
            for (int c = right; c >= left; c--) matrix[bottom][c] = cur++;
            bottom--;
            for (int r = bottom; r >= top; r--) matrix[r][left] = cur++;
            left++;
        }
        return matrix;
    }
};"""
    },

    769: {
        "starter_code_javascript": "function slope(x1, y1, x2, y2) {\n    return 0;\n}",
        "reference_solution_javascript": """function slope(x1, y1, x2, y2) {
    return (y2 - y1) / (x2 - x1);
}""",
        "starter_code_java": "class Solution {\n    public double slope(int x1, int y1, int x2, int y2) {\n        return 0.0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public double slope(int x1, int y1, int x2, int y2) {
        return (double)(y2 - y1) / (x2 - x1);
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    double slope(int x1, int y1, int x2, int y2);\n};",
        "reference_solution_cpp": """class Solution {
public:
    double slope(int x1, int y1, int x2, int y2) {
        return (double)(y2 - y1) / (x2 - x1);
    }
};"""
    },

    770: {
        "starter_code_javascript": "function max_sub_array_sum(a, size) {\n    return 0;\n}",
        "reference_solution_javascript": """function max_sub_array_sum(a, size) {
    let max_so_far = -Infinity, max_ending_here = 0;
    let start = 0, end = 0, s = 0;
    for (let i = 0; i < size; i++) {
        max_ending_here += a[i];
        if (max_so_far < max_ending_here) {
            max_so_far = max_ending_here;
            start = s;
            end = i;
        }
        if (max_ending_here < 0) {
            max_ending_here = 0;
            s = i + 1;
        }
    }
    return end - start + 1;
}""",
        "starter_code_java": "class Solution {\n    public int max_sub_array_sum(int[] a, int size) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int max_sub_array_sum(int[] a, int size) {
        long max_so_far = Long.MIN_VALUE, max_ending_here = 0;
        int start = 0, end = 0, s = 0;
        for (int i = 0; i < size; i++) {
            max_ending_here += a[i];
            if (max_so_far < max_ending_here) {
                max_so_far = max_ending_here;
                start = s;
                end = i;
            }
            if (max_ending_here < 0) {
                max_ending_here = 0;
                s = i + 1;
            }
        }
        return end - start + 1;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    int max_sub_array_sum(std::vector<int> a, int size);\n};",
        "reference_solution_cpp": """#include <vector>
#include <climits>
class Solution {
public:
    int max_sub_array_sum(std::vector<int> a, int size) {
        long long max_so_far = LLONG_MIN, max_ending_here = 0;
        int start = 0, end = 0, s = 0;
        for (int i = 0; i < size; i++) {
            max_ending_here += a[i];
            if (max_so_far < max_ending_here) {
                max_so_far = max_ending_here;
                start = s;
                end = i;
            }
            if (max_ending_here < 0) {
                max_ending_here = 0;
                s = i + 1;
            }
        }
        return end - start + 1;
    }
};"""
    },

    771: {
        "starter_code_javascript": "function cube_Sum(n) {\n    return 0;\n}",
        "reference_solution_javascript": """function cube_Sum(n) {
    let sum = 0;
    for (let i = 0; i < n; i++) {
        let x = 2 * i + 1;
        sum += x * x * x;
    }
    return sum;
}""",
        "starter_code_java": "class Solution {\n    public int cube_Sum(int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int cube_Sum(int n) {
        int sum = 0;
        for (int i = 0; i < n; i++) {
            int x = 2 * i + 1;
            sum += x * x * x;
        }
        return sum;
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    int cube_Sum(int n);\n};",
        "reference_solution_cpp": """class Solution {
public:
    int cube_Sum(int n) {
        int sum = 0;
        for (int i = 0; i < n; i++) {
            int x = 2 * i + 1;
            sum += x * x * x;
        }
        return sum;
    }
};"""
    },

    772: {
        "starter_code_javascript": "function min_Swaps(s1, s2) {\n    return 0;\n}",
        "reference_solution_javascript": """function min_Swaps(s1, s2) {
    let c0 = 0, c1 = 0;
    for (let i = 0; i < s1.length; i++) {
        if (s1[i] === '0' && s2[i] === '1') c0++;
        else if (s1[i] === '1' && s2[i] === '0') c1++;
    }
    let res = Math.floor(c0 / 2) + Math.floor(c1 / 2);
    if (c0 % 2 === 0 && c1 % 2 === 0) return res;
    else if ((c0 + c1) % 2 === 0) return res + 2;
    else return -1;
}""",
        "starter_code_java": "class Solution {\n    public int min_Swaps(String s1, String s2) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int min_Swaps(String s1, String s2) {
        int c0 = 0, c1 = 0;
        for (int i = 0; i < s1.length(); i++) {
            if (s1.charAt(i) == '0' && s2.charAt(i) == '1') c0++;
            else if (s1.charAt(i) == '1' && s2.charAt(i) == '0') c1++;
        }
        int res = c0 / 2 + c1 / 2;
        if (c0 % 2 == 0 && c1 % 2 == 0) return res;
        else if ((c0 + c1) % 2 == 0) return res + 2;
        else return -1;
    }
}""",
        "starter_code_cpp": "#include <string>\nclass Solution {\npublic:\n    int min_Swaps(std::string s1, std::string s2);\n};",
        "reference_solution_cpp": """#include <string>
class Solution {
public:
    int min_Swaps(std::string s1, std::string s2) {
        int c0 = 0, c1 = 0;
        for (size_t i = 0; i < s1.length(); i++) {
            if (s1[i] == '0' && s2[i] == '1') c0++;
            else if (s1[i] == '1' && s2[i] == '0') c1++;
        }
        int res = c0 / 2 + c1 / 2;
        if (c0 % 2 == 0 && c1 % 2 == 0) return res;
        else if ((c0 + c1) % 2 == 0) return res + 2;
        else return -1;
    }
};"""
    },

    773: {
        "starter_code_javascript": "function sort_tuple(tup) {\n    return [];\n}",
        "reference_solution_javascript": """function sort_tuple(tup) {
    return [...tup].sort((a, b) => String(a[0]).localeCompare(String(b[0])));
}""",
        "starter_code_java": "import java.util.*;\nclass Solution {\n    public Object[][] sort_tuple(Object[][] tup) {\n        return new Object[][]{};\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public Object[][] sort_tuple(Object[][] tup) {
        Object[][] res = tup.clone();
        Arrays.sort(res, (a, b) -> a[0].toString().compareTo(b[0].toString()));
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\n#include <string>\nclass Solution {\npublic:\n    std::vector<std::vector<std::string>> sort_tuple(std::vector<std::vector<std::string>> tup);\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <algorithm>
class Solution {
public:
    std::vector<std::vector<std::string>> sort_tuple(std::vector<std::vector<std::string>> tup) {
        std::sort(tup.begin(), tup.end(), [](const auto& a, const auto& b) {
            return a[0] < b[0];
        });
        return tup;
    }
};"""
    },

    774: {
        "starter_code_javascript": "function Check_Solution(a, b, c) {\n    return '';\n}",
        "reference_solution_javascript": """function Check_Solution(a, b, c) {
    return b === 0 ? "Yes" : "No";
}""",
        "starter_code_java": "class Solution {\n    public String Check_Solution(int a, int b, int c) {\n        return "";\n    }\n}",
        "reference_solution_java": """class Solution {
    public String Check_Solution(int a, int b, int c) {
        return b == 0 ? "Yes" : "No";
    }
}""",
        "starter_code_cpp": "#include <string>\nclass Solution {\npublic:\n    std::string Check_Solution(int a, int b, int c);\n};",
        "reference_solution_cpp": """#include <string>
class Solution {
public:
    std::string Check_Solution(int a, int b, int c) {
        return b == 0 ? "Yes" : "No";
    }
};"""
    },

    775: {
        "starter_code_javascript": "function get_inv_count(arr, n) {\n    return 0;\n}",
        "reference_solution_javascript": """function get_inv_count(arr, n) {
    let inv_count = 0;
    for (let i = 0; i < n; i++) {
        for (let j = i + 1; j < n; j++) {
            if (arr[i] > arr[j]) inv_count++;
        }
    }
    return inv_count;
}""",
        "starter_code_java": "class Solution {\n    public int get_inv_count(int[] arr, int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int get_inv_count(int[] arr, int n) {
        int inv_count = 0;
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                if (arr[i] > arr[j]) inv_count++;
            }
        }
        return inv_count;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    int get_inv_count(std::vector<int> arr, int n);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    int get_inv_count(std::vector<int> arr, int n) {
        int inv_count = 0;
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                if (arr[i] > arr[j]) inv_count++;
            }
        }
        return inv_count;
    }
};"""
    },

    776: {
        "starter_code_javascript": "function get_odd_occurence(arr, arr_size) {\n    return 0;\n}",
        "reference_solution_javascript": """function get_odd_occurence(arr, arr_size) {
    let res = 0;
    for (let i = 0; i < arr_size; i++) res ^= arr[i];
    return res;
}""",
        "starter_code_java": "class Solution {\n    public int get_odd_occurence(int[] arr, int arr_size) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int get_odd_occurence(int[] arr, int arr_size) {
        int res = 0;
        for (int i = 0; i < arr_size; i++) res ^= arr[i];
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    int get_odd_occurence(std::vector<int> arr, int arr_size);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    int get_odd_occurence(std::vector<int> arr, int arr_size) {
        int res = 0;
        for (int i = 0; i < arr_size; i++) res ^= arr[i];
        return res;
    }
};"""
    },

    777: {
        "starter_code_javascript": "function nth_super_ugly_number(n, primes) {\n    return 0;\n}",
        "reference_solution_javascript": """function nth_super_ugly_number(n, primes) {
    const uglies = [1];
    const idx = new Array(primes.length).fill(0);
    while (uglies.length < n) {
        let nextUgly = Infinity;
        for (let i = 0; i < primes.length; i++) {
            nextUgly = Math.min(nextUgly, uglies[idx[i]] * primes[i]);
        }
        uglies.push(nextUgly);
        for (let i = 0; i < primes.length; i++) {
            if (uglies[idx[i]] * primes[i] === nextUgly) idx[i]++;
        }
    }
    return uglies[n - 1];
}""",
        "starter_code_java": "class Solution {\n    public int nth_super_ugly_number(int n, int[] primes) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int nth_super_ugly_number(int n, int[] primes) {
        int[] uglies = new int[n];
        uglies[0] = 1;
        int k = primes.length;
        int[] idx = new int[k];
        for (int i = 1; i < n; i++) {
            long nextUgly = Long.MAX_VALUE;
            for (int j = 0; j < k; j++) {
                nextUgly = Math.min(nextUgly, (long) uglies[idx[j]] * primes[j]);
            }
            uglies[i] = (int) nextUgly;
            for (int j = 0; j < k; j++) {
                if ((long) uglies[idx[j]] * primes[j] == nextUgly) idx[j]++;
            }
        }
        return uglies[n - 1];
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    int nth_super_ugly_number(int n, std::vector<int> primes);\n};",
        "reference_solution_cpp": """#include <vector>
#include <climits>
#include <algorithm>
class Solution {
public:
    int nth_super_ugly_number(int n, std::vector<int> primes) {
        std::vector<long long> uglies = {1};
        std::vector<int> idx(primes.size(), 0);
        while ((int)uglies.size() < n) {
            long long nextUgly = LLONG_MAX;
            for (size_t i = 0; i < primes.size(); i++) {
                nextUgly = std::min(nextUgly, uglies[idx[i]] * primes[i]);
            }
            uglies.push_back(nextUgly);
            for (size_t i = 0; i < primes.size(); i++) {
                if (uglies[idx[i]] * primes[i] == nextUgly) idx[i]++;
            }
        }
        return (int)uglies[n - 1];
    }
};"""
    },

    778: {
        "starter_code_javascript": "function get_Number(n, k) {\n    return 0;\n}",
        "reference_solution_javascript": """function get_Number(n, k) {
    let arr = [];
    for (let odd = 1; odd <= n; odd += 2) arr.push(odd);
    for (let even = 2; even <= n; even += 2) arr.push(even);
    return arr[k - 1];
}""",
        "starter_code_java": "class Solution {\n    public int get_Number(int n, int k) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int get_Number(int n, int k) {
        int[] arr = new int[n];
        int idx = 0;
        for (int odd = 1; odd <= n; odd += 2) arr[idx++] = odd;
        for (int even = 2; even <= n; even += 2) arr[idx++] = even;
        return arr[k - 1];
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    int get_Number(int n, int k);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    int get_Number(int n, int k) {
        std::vector<int> arr;
        for (int odd = 1; odd <= n; odd += 2) arr.push_back(odd);
        for (int even = 2; even <= n; even += 2) arr.push_back(even);
        return arr[k - 1];
    }
};"""
    },

    779: {
        "starter_code_javascript": "function find_Digits(n) {\n    return 0;\n}",
        "reference_solution_javascript": """function find_Digits(n) {
    if (n < 0) return 0;
    if (n <= 1) return 1;
    let x = n * Math.log10(n / Math.E) + Math.log10(2 * Math.PI * n) / 2.0;
    return Math.floor(x) + 1;
}""",
        "starter_code_java": "class Solution {\n    public int find_Digits(int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int find_Digits(int n) {
        if (n < 0) return 0;
        if (n <= 1) return 1;
        double x = n * Math.log10(n / Math.E) + Math.log10(2 * Math.PI * n) / 2.0;
        return (int) Math.floor(x) + 1;
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    int find_Digits(int n);\n};",
        "reference_solution_cpp": """#include <cmath>
class Solution {
public:
    int find_Digits(int n) {
        if (n < 0) return 0;
        if (n <= 1) return 1;
        double pi = std::acos(-1.0);
        double e = std::exp(1.0);
        double x = n * std::log10(n / e) + std::log10(2 * pi * n) / 2.0;
        return (int) std::floor(x) + 1;
    }
};"""
    },

    780: {
        "starter_code_javascript": "function find_platform(arr, dep, n) {\n    return 0;\n}",
        "reference_solution_javascript": """function find_platform(arr, dep, n) {
    arr.sort((a, b) => a - b);
    dep.sort((a, b) => a - b);
    let plat = 1, res = 1;
    let i = 1, j = 0;
    while (i < n && j < n) {
        if (arr[i] <= dep[j]) { plat++; i++; }
        else { plat--; j++; }
        if (plat > res) res = plat;
    }
    return res;
}""",
        "starter_code_java": "import java.util.Arrays;\nclass Solution {\n    public int find_platform(int[] arr, int[] dep, int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """import java.util.Arrays;
class Solution {
    public int find_platform(int[] arr, int[] dep, int n) {
        Arrays.sort(arr);
        Arrays.sort(dep);
        int plat = 1, res = 1;
        int i = 1, j = 0;
        while (i < n && j < n) {
            if (arr[i] <= dep[j]) { plat++; i++; }
            else { plat--; j++; }
            if (plat > res) res = plat;
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    int find_platform(std::vector<int> arr, std::vector<int> dep, int n);\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
class Solution {
public:
    int find_platform(std::vector<int> arr, std::vector<int> dep, int n) {
        std::sort(arr.begin(), arr.end());
        std::sort(dep.begin(), dep.end());
        int plat = 1, res = 1;
        int i = 1, j = 0;
        while (i < n && j < n) {
            if (arr[i] <= dep[j]) { plat++; i++; }
            else { plat--; j++; }
            if (plat > res) res = plat;
        }
        return res;
    }
};"""
    },

    781: {
        "starter_code_javascript": "function lcopy(xs) {\n    return [];\n}",
        "reference_solution_javascript": """function lcopy(xs) {
    return xs.slice();
}""",
        "starter_code_java": "class Solution {\n    public int[] lcopy(int[] xs) {\n        return new int[]{};\n    }\n}",
        "reference_solution_java": """class Solution {
    public int[] lcopy(int[] xs) {
        return xs.clone();
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    std::vector<int> lcopy(std::vector<int> xs);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    std::vector<int> lcopy(std::vector<int> xs) {
        return xs;
    }
};"""
    },

    782: {
        "starter_code_javascript": "function area_trapezium(base1, base2, height) {\n    return 0;\n}",
        "reference_solution_javascript": """function area_trapezium(base1, base2, height) {
    return 0.5 * (base1 + base2) * height;
}""",
        "starter_code_java": "class Solution {\n    public int area_trapezium(int base1, int base2, int height) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int area_trapezium(int base1, int base2, int height) {
        return (int)(0.5 * (base1 + base2) * height);
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    int area_trapezium(int base1, int base2, int height);\n};",
        "reference_solution_cpp": """class Solution {
public:
    int area_trapezium(int base1, int base2, int height) {
        return (int)(0.5 * (base1 + base2) * height);
    }
};"""
    },

    783: {
        "starter_code_javascript": "function Sum(N) {\n    return 0;\n}",
        "reference_solution_javascript": """function Sum(N) {
    const sum = new Array(N + 1).fill(0);
    for (let i = 2; i <= N; i++) {
        if (sum[i] === 0) {
            for (let j = i; j <= N; j += i) sum[j] += i;
        }
    }
    return sum[N];
}""",
        "starter_code_java": "class Solution {\n    public int Sum(int N) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int Sum(int N) {
        int[] sum = new int[N + 1];
        for (int i = 2; i <= N; i++) {
            if (sum[i] == 0) {
                for (int j = i; j <= N; j += i) sum[j] += i;
            }
        }
        return sum[N];
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    int Sum(int N);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    int Sum(int N) {
        std::vector<int> sum(N + 1, 0);
        for (int i = 2; i <= N; i++) {
            if (sum[i] == 0) {
                for (int j = i; j <= N; j += i) sum[j] += i;
            }
        }
        return sum[N];
    }
};"""
    },

    784: {
        "starter_code_javascript": "function is_triangleexists(a, b, c) {\n    return false;\n}",
        "reference_solution_javascript": """function is_triangleexists(a, b, c) {
    if (a !== 0 && b !== 0 && c !== 0 && a + b + c === 180) {
        return (a + b >= c || b + c >= a || a + c >= b);
    }
    return false;
}""",
        "starter_code_java": "class Solution {\n    public boolean is_triangleexists(int a, int b, int c) {\n        return false;\n    }\n}",
        "reference_solution_java": """class Solution {
    public boolean is_triangleexists(int a, int b, int c) {
        if (a != 0 && b != 0 && c != 0 && a + b + c == 180) {
            return (a + b >= c || b + c >= a || a + c >= b);
        }
        return false;
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    bool is_triangleexists(int a, int b, int c);\n};",
        "reference_solution_cpp": """class Solution {
public:
    bool is_triangleexists(int a, int b, int c) {
        if (a != 0 && b != 0 && c != 0 && a + b + c == 180) {
            return (a + b >= c || b + c >= a || a + c >= b);
        }
        return false;
    }
};"""
    },

    785: {
        "starter_code_javascript": "function Sum_of_Inverse_Divisors(N, Sum) {\n    return 0;\n}",
        "reference_solution_javascript": """function Sum_of_Inverse_Divisors(N, Sum) {
    return Math.round((Sum / N) * 100) / 100;
}""",
        "starter_code_java": "class Solution {\n    public double Sum_of_Inverse_Divisors(int N, int Sum) {\n        return 0.0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public double Sum_of_Inverse_Divisors(int N, int Sum) {
        double ans = (double) Sum / N;
        return Math.round(ans * 100.0) / 100.0;
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    double Sum_of_Inverse_Divisors(int N, int Sum);\n};",
        "reference_solution_cpp": """#include <cmath>
class Solution {
public:
    double Sum_of_Inverse_Divisors(int N, int Sum) {
        double ans = (double) Sum / N;
        return std::round(ans * 100.0) / 100.0;
    }
};"""
    },

    786: {
        "starter_code_javascript": "function remove_negs(num_list) {\n    return [];\n}",
        "reference_solution_javascript": """function remove_negs(num_list) {
    return num_list.filter(x => x >= 0);
}""",
        "starter_code_java": "import java.util.*;\nclass Solution {\n    public int[] remove_negs(int[] num_list) {\n        return new int[]{};\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[] remove_negs(int[] num_list) {
        List<Integer> list = new ArrayList<>();
        for (int x : num_list) if (x >= 0) list.add(x);
        int[] res = new int[list.size()];
        for (int i = 0; i < list.size(); i++) res[i] = list.get(i);
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    std::vector<int> remove_negs(std::vector<int> num_list);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    std::vector<int> remove_negs(std::vector<int> num_list) {
        std::vector<int> res;
        for (int x : num_list) if (x >= 0) res.push_back(x);
        return res;
    }
};"""
    },

    787: {
        "starter_code_javascript": "function sum_of_odd_Factors(n) {\n    return 0;\n}",
        "reference_solution_javascript": """function sum_of_odd_Factors(n) {
    let res = 1;
    while (n % 2 === 0) n = Math.floor(n / 2);
    for (let i = 3; i * i <= n; i++) {
        let curr_sum = 1, curr_term = 1;
        while (n % i === 0) {
            n = Math.floor(n / i);
            curr_term *= i;
            curr_sum += curr_term;
        }
        res *= curr_sum;
    }
    if (n >= 2) res *= (1 + n);
    return res;
}""",
        "starter_code_java": "class Solution {\n    public int sum_of_odd_Factors(int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int sum_of_odd_Factors(int n) {
        int res = 1;
        while (n % 2 == 0) n /= 2;
        for (int i = 3; i * i <= n; i++) {
            int curr_sum = 1, curr_term = 1;
            while (n % i == 0) {
                n /= i;
                curr_term *= i;
                curr_sum += curr_term;
            }
            res *= curr_sum;
        }
        if (n >= 2) res *= (1 + n);
        return res;
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    int sum_of_odd_Factors(int n);\n};",
        "reference_solution_cpp": """class Solution {
public:
    int sum_of_odd_Factors(int n) {
        int res = 1;
        while (n % 2 == 0) n /= 2;
        for (int i = 3; i * i <= n; i++) {
            int curr_sum = 1, curr_term = 1;
            while (n % i == 0) {
                n /= i;
                curr_term *= i;
                curr_sum += curr_term;
            }
            res *= curr_sum;
        }
        if (n >= 2) res *= (1 + n);
        return res;
    }
};"""
    },

    788: {
        "starter_code_javascript": "function raw_heap(rawheap) {\n    return [];\n}",
        "reference_solution_javascript": """function raw_heap(rawheap) {
    function siftDown(i, n) {
        while (2 * i + 1 < n) {
            let left = 2 * i + 1, right = 2 * i + 2, smallest = i;
            if (rawheap[left] < rawheap[smallest]) smallest = left;
            if (right < n && rawheap[right] < rawheap[smallest]) smallest = right;
            if (smallest !== i) {
                [rawheap[i], rawheap[smallest]] = [rawheap[smallest], rawheap[i]];
                i = smallest;
            } else break;
        }
    }
    const n = rawheap.length;
    for (let i = Math.floor((n - 2) / 2); i >= 0; i--) siftDown(i, n);
    return rawheap;
}""",
        "starter_code_java": "class Solution {\n    public int[] raw_heap(int[] rawheap) {\n        return new int[]{};\n    }\n}",
        "reference_solution_java": """class Solution {
    private void siftDown(int[] arr, int i, int n) {
        while (2 * i + 1 < n) {
            int left = 2 * i + 1, right = 2 * i + 2, smallest = i;
            if (arr[left] < arr[smallest]) smallest = left;
            if (right < n && arr[right] < arr[smallest]) smallest = right;
            if (smallest != i) {
                int tmp = arr[i]; arr[i] = arr[smallest]; arr[smallest] = tmp;
                i = smallest;
            } else break;
        }
    }
    public int[] raw_heap(int[] rawheap) {
        int n = rawheap.length;
        for (int i = (n - 2) / 2; i >= 0; i--) {
            siftDown(rawheap, i, n);
        }
        return rawheap;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    std::vector<int> raw_heap(std::vector<int> rawheap);\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
class Solution {
    void siftDown(std::vector<int>& arr, int i, int n) {
        while (2 * i + 1 < n) {
            int left = 2 * i + 1, right = 2 * i + 2, smallest = i;
            if (arr[left] < arr[smallest]) smallest = left;
            if (right < n && arr[right] < arr[smallest]) smallest = right;
            if (smallest != i) {
                std::swap(arr[i], arr[smallest]);
                i = smallest;
            } else break;
        }
    }
public:
    std::vector<int> raw_heap(std::vector<int> rawheap) {
        int n = rawheap.size();
        for (int i = (n - 2) / 2; i >= 0; i--) {
            siftDown(rawheap, i, n);
        }
        return rawheap;
    }
};"""
    },

    789: {
        "starter_code_javascript": "function check_Even_Parity(x) {\n    return false;\n}",
        "reference_solution_javascript": """function check_Even_Parity(x) {
    let parity = 0;
    while (x !== 0) {
        x = x & (x - 1);
        parity++;
    }
    return parity % 2 === 0;
}""",
        "starter_code_java": "class Solution {\n    public boolean check_Even_Parity(int x) {\n        return false;\n    }\n}",
        "reference_solution_java": """class Solution {
    public boolean check_Even_Parity(int x) {
        int parity = 0;
        while (x != 0) {
            x = x & (x - 1);
            parity++;
        }
        return parity % 2 == 0;
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    bool check_Even_Parity(int x);\n};",
        "reference_solution_cpp": """class Solution {
public:
    bool check_Even_Parity(int x) {
        int parity = 0;
        while (x != 0) {
            x = x & (x - 1);
            parity++;
        }
        return parity % 2 == 0;
    }
};"""
    },

    790: {
        "starter_code_javascript": "function find_Min_Swaps(arr, n) {\n    return 0;\n}",
        "reference_solution_javascript": """function find_Min_Swaps(arr, n) {
    let noOfZeroes = new Array(n).fill(0);
    let count = 0;
    noOfZeroes[n - 1] = 1 - arr[n - 1];
    for (let i = n - 2; i >= 0; i--) {
        noOfZeroes[i] = noOfZeroes[i + 1] + (arr[i] === 0 ? 1 : 0);
    }
    for (let i = 0; i < n; i++) {
        if (arr[i] === 1) count += noOfZeroes[i];
    }
    return count;
}""",
        "starter_code_java": "class Solution {\n    public int find_Min_Swaps(int[] arr, int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int find_Min_Swaps(int[] arr, int n) {
        int[] noOfZeroes = new int[n];
        int count = 0;
        noOfZeroes[n - 1] = 1 - arr[n - 1];
        for (int i = n - 2; i >= 0; i--) {
            noOfZeroes[i] = noOfZeroes[i + 1] + (arr[i] == 0 ? 1 : 0);
        }
        for (int i = 0; i < n; i++) {
            if (arr[i] == 1) count += noOfZeroes[i];
        }
        return count;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    int find_Min_Swaps(std::vector<int> arr, int n);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    int find_Min_Swaps(std::vector<int> arr, int n) {
        std::vector<int> noOfZeroes(n, 0);
        int count = 0;
        noOfZeroes[n - 1] = 1 - arr[n - 1];
        for (int i = n - 2; i >= 0; i--) {
            noOfZeroes[i] = noOfZeroes[i + 1] + (arr[i] == 0 ? 1 : 0);
        }
        for (int i = 0; i < n; i++) {
            if (arr[i] == 1) count += noOfZeroes[i];
        }
        return count;
    }
};"""
    },

    791: {
        "starter_code_javascript": "function listify_list(list1) {\n    return [];\n}",
        "reference_solution_javascript": """function listify_list(list1) {
    return list1.map(s => s.split(''));
}""",
        "starter_code_java": "class Solution {\n    public String[][] listify_list(String[] list1) {\n        return new String[][]{};\n    }\n}",
        "reference_solution_java": """class Solution {
    public String[][] listify_list(String[] list1) {
        String[][] res = new String[list1.length][];
        for (int i = 0; i < list1.length; i++) {
            String s = list1[i];
            res[i] = new String[s.length()];
            for (int j = 0; j < s.length(); j++) {
                res[i][j] = String.valueOf(s.charAt(j));
            }
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\n#include <string>\nclass Solution {\npublic:\n    std::vector<std::vector<std::string>> listify_list(std::vector<std::string> list1);\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
class Solution {
public:
    std::vector<std::vector<std::string>> listify_list(std::vector<std::string> list1) {
        std::vector<std::vector<std::string>> res(list1.size());
        for (size_t i = 0; i < list1.size(); i++) {
            for (char c : list1[i]) {
                res[i].push_back(std::string(1, c));
            }
        }
        return res;
    }
};"""
    },

    792: {
        "starter_code_javascript": "function count_list(input_list) {\n    return 0;\n}",
        "reference_solution_javascript": """function count_list(input_list) {
    return input_list.length * input_list.length;
}""",
        "starter_code_java": "class Solution {\n    public int count_list(int[][] input_list) {\n        return 0;\n    }\n    public int count_list(Object[][] input_list) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int count_list(int[][] input_list) {
        return input_list.length * input_list.length;
    }
    public int count_list(Object[][] input_list) {
        return input_list.length * input_list.length;
    }
}""",
        "starter_code_cpp": "#include <vector>\n#include <string>\nclass Solution {\npublic:\n    int count_list(const std::vector<std::vector<int>>& input_list);\n    int count_list(const std::vector<std::vector<std::string>>& input_list);\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
class Solution {
public:
    int count_list(const std::vector<std::vector<int>>& input_list) {
        return (int)(input_list.size() * input_list.size());
    }
    int count_list(const std::vector<std::vector<std::string>>& input_list) {
        return (int)(input_list.size() * input_list.size());
    }
};"""
    },

    793: {
        "starter_code_javascript": "function sub_lists(my_list) {\n    return [];\n}",
        "reference_solution_javascript": """function sub_lists(my_list) {
    let res = [[]];
    for (let k = 1; k <= my_list.length; k++) {
        function backtrack(start, cur) {
            if (cur.length === k) { res.push([...cur]); return; }
            for (let i = start; i < my_list.length; i++) {
                cur.push(my_list[i]);
                backtrack(i + 1, cur);
                cur.pop();
            }
        }
        backtrack(0, []);
    }
    return res;
}""",
        "starter_code_java": "import java.util.*;\nclass Solution {\n    public int[][] sub_lists(int[] my_list) {\n        return new int[][]{};\n    }\n    public String[][] sub_lists(String[] my_list) {\n        return new String[][]{};\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[][] sub_lists(int[] my_list) {
        List<int[]> res = new ArrayList<>();
        res.add(new int[0]);
        for (int k = 1; k <= my_list.length; k++) {
            combineInt(my_list, 0, k, new ArrayList<>(), res);
        }
        return res.toArray(new int[res.size()][]);
    }
    private void combineInt(int[] arr, int start, int k, List<Integer> cur, List<int[]> res) {
        if (cur.size() == k) {
            int[] item = new int[k];
            for (int i = 0; i < k; i++) item[i] = cur.get(i);
            res.add(item);
            return;
        }
        for (int i = start; i < arr.length; i++) {
            cur.add(arr[i]);
            combineInt(arr, i + 1, k, cur, res);
            cur.remove(cur.size() - 1);
        }
    }
    public String[][] sub_lists(String[] my_list) {
        List<String[]> res = new ArrayList<>();
        res.add(new String[0]);
        for (int k = 1; k <= my_list.length; k++) {
            combineStr(my_list, 0, k, new ArrayList<>(), res);
        }
        return res.toArray(new String[res.size()][]);
    }
    private void combineStr(String[] arr, int start, int k, List<String> cur, List<String[]> res) {
        if (cur.size() == k) {
            res.add(cur.toArray(new String[0]));
            return;
        }
        for (int i = start; i < arr.length; i++) {
            cur.add(arr[i]);
            combineStr(arr, i + 1, k, cur, res);
            cur.remove(cur.size() - 1);
        }
    }
}""",
        "starter_code_cpp": "#include <vector>\n#include <string>\nclass Solution {\npublic:\n    std::vector<std::vector<int>> sub_lists(std::vector<int> my_list);\n    std::vector<std::vector<std::string>> sub_lists(std::vector<std::string> my_list);\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
class Solution {
    void combineInt(const std::vector<int>& arr, size_t start, size_t k, std::vector<int>& cur, std::vector<std::vector<int>>& res) {
        if (cur.size() == k) { res.push_back(cur); return; }
        for (size_t i = start; i < arr.size(); i++) {
            cur.push_back(arr[i]);
            combineInt(arr, i + 1, k, cur, res);
            cur.pop_back();
        }
    }
    void combineStr(const std::vector<std::string>& arr, size_t start, size_t k, std::vector<std::string>& cur, std::vector<std::vector<std::string>>& res) {
        if (cur.size() == k) { res.push_back(cur); return; }
        for (size_t i = start; i < arr.size(); i++) {
            cur.push_back(arr[i]);
            combineStr(arr, i + 1, k, cur, res);
            cur.pop_back();
        }
    }
public:
    std::vector<std::vector<int>> sub_lists(std::vector<int> my_list) {
        std::vector<std::vector<int>> res;
        res.push_back({});
        for (size_t k = 1; k <= my_list.size(); k++) {
            std::vector<int> cur;
            combineInt(my_list, 0, k, cur, res);
        }
        return res;
    }
    std::vector<std::vector<std::string>> sub_lists(std::vector<std::string> my_list) {
        std::vector<std::vector<std::string>> res;
        res.push_back({});
        for (size_t k = 1; k <= my_list.size(); k++) {
            std::vector<std::string> cur;
            combineStr(my_list, 0, k, cur, res);
        }
        return res;
    }
};"""
    },

    794: {
        "starter_code_javascript": "function check_alphanumeric(string) {\n    return '';\n}",
        "reference_solution_javascript": """function check_alphanumeric(string) {
    return /[a-zA-Z0-9]$/.test(string) ? "Accept" : "Discard";
}""",
        "starter_code_java": "class Solution {\n    public String check_alphanumeric(String string) {\n        return "";\n    }\n}",
        "reference_solution_java": """class Solution {
    public String check_alphanumeric(String string) {
        if (string.isEmpty()) return "Discard";
        char c = string.charAt(string.length() - 1);
        return Character.isLetterOrDigit(c) ? "Accept" : "Discard";
    }
}""",
        "starter_code_cpp": "#include <string>\nclass Solution {\npublic:\n    std::string check_alphanumeric(std::string string);\n};",
        "reference_solution_cpp": """#include <string>
#include <cctype>
class Solution {
public:
    std::string check_alphanumeric(std::string string) {
        if (string.empty()) return "Discard";
        char c = string.back();
        return isalnum((unsigned char)c) ? "Accept" : "Discard";
    }
};"""
    },

    795: {
        "starter_code_javascript": "function anagram_lambda(texts, str) {\n    return [];\n}",
        "reference_solution_javascript": """function anagram_lambda(texts, str) {
    const sortChars = (s) => s.split('').sort().join('');
    const target = sortChars(str);
    return texts.filter(t => sortChars(t) === target);
}""",
        "starter_code_java": "import java.util.*;\nclass Solution {\n    public String[] anagram_lambda(String[] texts, String str) {\n        return new String[]{};\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    private String sortChars(String s) {
        char[] chars = s.toCharArray();
        Arrays.sort(chars);
        return new String(chars);
    }
    public String[] anagram_lambda(String[] texts, String str) {
        String target = sortChars(str);
        List<String> list = new ArrayList<>();
        for (String t : texts) {
            if (sortChars(t).equals(target)) list.add(t);
        }
        return list.toArray(new String[0]);
    }
}""",
        "starter_code_cpp": "#include <vector>\n#include <string>\nclass Solution {\npublic:\n    std::vector<std::string> anagram_lambda(std::vector<std::string> texts, std::string str);\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <algorithm>
class Solution {
    std::string sortChars(std::string s) {
        std::sort(s.begin(), s.end());
        return s;
    }
public:
    std::vector<std::string> anagram_lambda(std::vector<std::string> texts, std::string str) {
        std::string target = sortChars(str);
        std::vector<std::string> res;
        for (const auto& t : texts) {
            if (sortChars(t) == target) res.push_back(t);
        }
        return res;
    }
};"""
    },

    796: {
        "starter_code_javascript": "function find_longest_conseq_subseq(arr, n) {\n    return 0;\n}",
        "reference_solution_javascript": """function find_longest_conseq_subseq(arr, n) {
    if (n === 0) return 0;
    arr.sort((a, b) => a - b);
    let v = [arr[0]];
    for (let i = 1; i < n; i++) {
        if (arr[i] !== arr[i - 1]) v.push(arr[i]);
    }
    let ans = 0, count = 0;
    for (let i = 0; i < v.length; i++) {
        if (i > 0 && v[i] === v[i - 1] + 1) count++;
        else count = 1;
        ans = Math.max(ans, count);
    }
    return ans;
}""",
        "starter_code_java": "import java.util.*;\nclass Solution {\n    public int find_longest_conseq_subseq(int[] arr, int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int find_longest_conseq_subseq(int[] arr, int n) {
        if (n == 0) return 0;
        Arrays.sort(arr);
        List<Integer> v = new ArrayList<>();
        v.add(arr[0]);
        for (int i = 1; i < n; i++) {
            if (arr[i] != arr[i - 1]) v.add(arr[i]);
        }
        int ans = 0, count = 0;
        for (int i = 0; i < v.size(); i++) {
            if (i > 0 && v.get(i) == v.get(i - 1) + 1) count++;
            else count = 1;
            ans = Math.max(ans, count);
        }
        return ans;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    int find_longest_conseq_subseq(std::vector<int> arr, int n);\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
class Solution {
public:
    int find_longest_conseq_subseq(std::vector<int> arr, int n) {
        if (n == 0) return 0;
        std::sort(arr.begin(), arr.end());
        std::vector<int> v;
        v.push_back(arr[0]);
        for (int i = 1; i < n; i++) {
            if (arr[i] != arr[i - 1]) v.push_back(arr[i]);
        }
        int ans = 0, count = 0;
        for (size_t i = 0; i < v.size(); i++) {
            if (i > 0 && v[i] == v[i - 1] + 1) count++;
            else count = 1;
            ans = std::max(ans, count);
        }
        return ans;
    }
};"""
    },

    797: {
        "starter_code_javascript": "function palindrome_lambda(texts) {\n    return [];\n}",
        "reference_solution_javascript": """function palindrome_lambda(texts) {
    return texts.filter(s => s === s.split('').reverse().join(''));
}""",
        "starter_code_java": "import java.util.*;\nclass Solution {\n    public String[] palindrome_lambda(String[] texts) {\n        return new String[]{};\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    private boolean isPal(String s) {
        int i = 0, j = s.length() - 1;
        while (i < j) {
            if (s.charAt(i++) != s.charAt(j--)) return false;
        }
        return true;
    }
    public String[] palindrome_lambda(String[] texts) {
        List<String> list = new ArrayList<>();
        for (String s : texts) if (isPal(s)) list.add(s);
        return list.toArray(new String[0]);
    }
}""",
        "starter_code_cpp": "#include <vector>\n#include <string>\nclass Solution {\npublic:\n    std::vector<std::string> palindrome_lambda(std::vector<std::string> texts);\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <algorithm>
class Solution {
public:
    std::vector<std::string> palindrome_lambda(std::vector<std::string> texts) {
        std::vector<std::string> res;
        for (const auto& s : texts) {
            std::string rev = s;
            std::reverse(rev.begin(), rev.end());
            if (s == rev) res.push_back(s);
        }
        return res;
    }
};"""
    },

    798: {
        "starter_code_javascript": "function ntimes_list(nums, n) {\n    return [];\n}",
        "reference_solution_javascript": """function ntimes_list(nums, n) {
    return nums.map(x => n * x);
}""",
        "starter_code_java": "class Solution {\n    public int[] ntimes_list(int[] nums, int n) {\n        return new int[]{};\n    }\n}",
        "reference_solution_java": """class Solution {
    public int[] ntimes_list(int[] nums, int n) {
        int[] res = new int[nums.length];
        for (int i = 0; i < nums.length; i++) res[i] = n * nums[i];
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    std::vector<int> ntimes_list(std::vector<int> nums, int n);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    std::vector<int> ntimes_list(std::vector<int> nums, int n) {
        std::vector<int> res(nums.size());
        for (size_t i = 0; i < nums.size(); i++) res[i] = n * nums[i];
        return res;
    }
};"""
    },

    799: {
        "starter_code_javascript": "function check_monthnumb(monthname2) {\n    return false;\n}",
        "reference_solution_javascript": """function check_monthnumb(monthname2) {
    const months = new Set(["January", "March", "May", "July", "August", "Augest", "October", "December"]);
    return months.has(monthname2);
}""",
        "starter_code_java": "import java.util.*;\nclass Solution {\n    public boolean check_monthnumb(String monthname2) {\n        return false;\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public boolean check_monthnumb(String monthname2) {
        Set<String> set = new HashSet<>(Arrays.asList("January", "March", "May", "July", "August", "Augest", "October", "December"));
        return set.contains(monthname2);
    }
}""",
        "starter_code_cpp": "#include <string>\n#include <unordered_set>\nclass Solution {\npublic:\n    bool check_monthnumb(std::string monthname2);\n};",
        "reference_solution_cpp": """#include <string>
#include <unordered_set>
class Solution {
public:
    bool check_monthnumb(std::string monthname2) {
        std::unordered_set<std::string> set = {"January", "March", "May", "July", "August", "Augest", "October", "December"};
        return set.find(monthname2) != set.end();
    }
};"""
    },

    800: {
        "starter_code_javascript": "function min_Num(arr, n) {\n    return 0;\n}",
        "reference_solution_javascript": """function min_Num(arr, n) {
    let odd = 0;
    for (let i = 0; i < n; i++) if (arr[i] % 2 !== 0) odd++;
    return odd % 2 !== 0 ? 1 : 2;
}""",
        "starter_code_java": "class Solution {\n    public int min_Num(int[] arr, int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int min_Num(int[] arr, int n) {
        int odd = 0;
        for (int i = 0; i < n; i++) if (arr[i] % 2 != 0) odd++;
        return odd % 2 != 0 ? 1 : 2;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    int min_Num(std::vector<int> arr, int n);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    int min_Num(std::vector<int> arr, int n) {
        int odd = 0;
        for (int i = 0; i < n; i++) if (arr[i] % 2 != 0) odd++;
        return odd % 2 != 0 ? 1 : 2;
    }
};"""
    },

    801: {
        "starter_code_javascript": "function length_Of_Last_Word(a) {\n    return 0;\n}",
        "reference_solution_javascript": """function length_Of_Last_Word(a) {
    const trimmed = a.trim();
    if (!trimmed) return 0;
    const parts = trimmed.split(/\\s+/);
    return parts[parts.length - 1].length;
}""",
        "starter_code_java": "class Solution {\n    public int length_Of_Last_Word(String a) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int length_Of_Last_Word(String a) {
        String trimmed = a.trim();
        if (trimmed.isEmpty()) return 0;
        String[] parts = trimmed.split("\\s+");
        return parts[parts.length - 1].length();
    }
}""",
        "starter_code_cpp": "#include <string>\nclass Solution {\npublic:\n    int length_Of_Last_Word(std::string a);\n};",
        "reference_solution_cpp": """#include <string>
#include <sstream>
class Solution {
public:
    int length_Of_Last_Word(std::string a) {
        std::istringstream iss(a);
        std::string word, last;
        while (iss >> word) last = word;
        return (int)last.length();
    }
};"""
    },

    802: {
        "starter_code_javascript": "function remove_list_range(list1, leftrange, rigthrange) {\n    return [];\n}",
        "reference_solution_javascript": """function remove_list_range(list1, leftrange, rigthrange) {
    return list1.filter(sub => Math.min(...sub) >= leftrange && Math.max(...sub) <= rigthrange);
}""",
        "starter_code_java": "import java.util.*;\nclass Solution {\n    public int[][] remove_list_range(int[][] list1, int leftrange, int rigthrange) {\n        return new int[][]{};\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[][] remove_list_range(int[][] list1, int leftrange, int rigthrange) {
        List<int[]> res = new ArrayList<>();
        for (int[] sub : list1) {
            int min = Integer.MAX_VALUE, max = Integer.MIN_VALUE;
            for (int x : sub) {
                if (x < min) min = x;
                if (x > max) max = x;
            }
            if (min >= leftrange && max <= rigthrange) res.add(sub);
        }
        return res.toArray(new int[res.size()][]);
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    std::vector<std::vector<int>> remove_list_range(std::vector<std::vector<int>> list1, int leftrange, int rigthrange);\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
class Solution {
public:
    std::vector<std::vector<int>> remove_list_range(std::vector<std::vector<int>> list1, int leftrange, int rigthrange) {
        std::vector<std::vector<int>> res;
        for (const auto& sub : list1) {
            int minVal = *std::min_element(sub.begin(), sub.end());
            int maxVal = *std::max_element(sub.begin(), sub.end());
            if (minVal >= leftrange && maxVal <= rigthrange) res.push_back(sub);
        }
        return res;
    }
};"""
    },

    803: {
        "starter_code_javascript": "function sum_positivenum(nums) {\n    return 0;\n}",
        "reference_solution_javascript": """function sum_positivenum(nums) {
    return nums.filter(x => x > 0).reduce((a, b) => a + b, 0);
}""",
        "starter_code_java": "class Solution {\n    public int sum_positivenum(int[] nums) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int sum_positivenum(int[] nums) {
        int sum = 0;
        for (int x : nums) if (x > 0) sum += x;
        return sum;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    int sum_positivenum(std::vector<int> nums);\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    int sum_positivenum(std::vector<int> nums) {
        int sum = 0;
        for (int x : nums) if (x > 0) sum += x;
        return sum;
    }
};"""
    },

    804: {
        "starter_code_javascript": "function are_Rotations(string1, string2) {\n    return false;\n}",
        "reference_solution_javascript": """function are_Rotations(string1, string2) {
    if (string1.length !== string2.length) return false;
    return (string1 + string1).includes(string2);
}""",
        "starter_code_java": "class Solution {\n    public boolean are_Rotations(String string1, String string2) {\n        return false;\n    }\n}",
        "reference_solution_java": """class Solution {
    public boolean are_Rotations(String string1, String string2) {
        if (string1.length() != string2.length()) return false;
        return (string1 + string1).contains(string2);
    }
}""",
        "starter_code_cpp": "#include <string>\nclass Solution {\npublic:\n    bool are_Rotations(std::string string1, std::string string2);\n};",
        "reference_solution_cpp": """#include <string>
class Solution {
public:
    bool are_Rotations(std::string string1, std::string string2) {
        if (string1.length() != string2.length()) return false;
        return (string1 + string1).find(string2) != std::string::npos;
    }
};"""
    },

    805: {
        "starter_code_javascript": "function check_subset(list1, list2) {\n    return false;\n}",
        "reference_solution_javascript": """function check_subset(list1, list2) {
    const s = new Set(list1.map(x => JSON.stringify(x)));
    return list2.every(x => s.has(JSON.stringify(x)));
}""",
        "starter_code_java": "import java.util.*;\nclass Solution {\n    public boolean check_subset(int[][] list1, int[][] list2) {\n        return false;\n    }\n    public boolean check_subset(Object[][] list1, Object[][] list2) {\n        return false;\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public boolean check_subset(int[][] list1, int[][] list2) {
        for (int[] b : list2) {
            boolean found = false;
            for (int[] a : list1) {
                if (Arrays.equals(a, b)) { found = true; break; }
            }
            if (!found) return false;
        }
        return true;
    }
    public boolean check_subset(Object[][] list1, Object[][] list2) {
        for (Object[] b : list2) {
            boolean found = false;
            for (Object[] a : list1) {
                if (Arrays.deepEquals(a, b)) { found = true; break; }
            }
            if (!found) return false;
        }
        return true;
    }
}""",
        "starter_code_cpp": "#include <vector>\n#include <string>\nclass Solution {\npublic:\n    bool check_subset(std::vector<std::vector<int>> list1, std::vector<std::vector<int>> list2);\n    bool check_subset(std::vector<std::vector<std::string>> list1, std::vector<std::vector<std::string>> list2);\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <algorithm>
class Solution {
public:
    bool check_subset(std::vector<std::vector<int>> list1, std::vector<std::vector<int>> list2) {
        for (const auto& b : list2) {
            if (std::find(list1.begin(), list1.end(), b) == list1.end()) return false;
        }
        return true;
    }
    bool check_subset(std::vector<std::vector<std::string>> list1, std::vector<std::vector<std::string>> list2) {
        for (const auto& b : list2) {
            if (std::find(list1.begin(), list1.end(), b) == list1.end()) return false;
        }
        return true;
    }
};"""
    },

    806: {
        "starter_code_javascript": "function fibonacci(n) {\n    return 0;\n}",
        "reference_solution_javascript": """function fibonacci(n) {
    if (n === 1 || n === 2) return 1;
    let a = 1, b = 1;
    for (let i = 3; i <= n; i++) {
        let c = a + b;
        a = b;
        b = c;
    }
    return b;
}""",
        "starter_code_java": "class Solution {\n    public int fibonacci(int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int fibonacci(int n) {
        if (n == 1 || n == 2) return 1;
        int a = 1, b = 1;
        for (int i = 3; i <= n; i++) {
            int c = a + b;
            a = b;
            b = c;
        }
        return b;
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    int fibonacci(int n);\n};",
        "reference_solution_cpp": """class Solution {
public:
    int fibonacci(int n) {
        if (n == 1 || n == 2) return 1;
        int a = 1, b = 1;
        for (int i = 3; i <= n; i++) {
            int c = a + b;
            a = b;
            b = c;
        }
        return b;
    }
};"""
    },

    807: {
        "starter_code_javascript": "function check_Concat(str1, str2) {\n    return false;\n}",
        "reference_solution_javascript": """function check_Concat(str1, str2) {
    const N = str1.length, M = str2.length;
    if (N % M !== 0) return false;
    for (let i = 0; i < N; i++) {
        if (str1[i] !== str2[i % M]) return false;
    }
    return true;
}""",
        "starter_code_java": "class Solution {\n    public boolean check_Concat(String str1, String str2) {\n        return false;\n    }\n}",
        "reference_solution_java": """class Solution {
    public boolean check_Concat(String str1, String str2) {
        int N = str1.length(), M = str2.length();
        if (N % M != 0) return false;
        for (int i = 0; i < N; i++) {
            if (str1.charAt(i) != str2.charAt(i % M)) return false;
        }
        return true;
    }
}""",
        "starter_code_cpp": "#include <string>\nclass Solution {\npublic:\n    bool check_Concat(std::string str1, std::string str2);\n};",
        "reference_solution_cpp": """#include <string>
class Solution {
public:
    bool check_Concat(std::string str1, std::string str2) {
        int N = str1.length(), M = str2.length();
        if (N % M != 0) return false;
        for (int i = 0; i < N; i++) {
            if (str1[i] != str2[i % M]) return false;
        }
        return true;
    }
};"""
    },

    808: {
        "starter_code_javascript": "function min_difference(test_list) {\n    return 0;\n}",
        "reference_solution_javascript": """function min_difference(test_list) {
    let minDiff = Infinity;
    for (let pair of test_list) {
        minDiff = Math.min(minDiff, Math.abs(pair[1] - pair[0]));
    }
    return minDiff;
}""",
        "starter_code_java": "class Solution {\n    public int min_difference(int[][] test_list) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int min_difference(int[][] test_list) {
        int minDiff = Integer.MAX_VALUE;
        for (int[] pair : test_list) {
            minDiff = Math.min(minDiff, Math.abs(pair[1] - pair[0]));
        }
        return minDiff;
    }
}""",
        "starter_code_cpp": "#include <vector>\nclass Solution {\npublic:\n    int min_difference(std::vector<std::vector<int>> test_list);\n};",
        "reference_solution_cpp": """#include <vector>
#include <climits>
#include <cmath>
#include <algorithm>
class Solution {
public:
    int min_difference(std::vector<std::vector<int>> test_list) {
        int minDiff = INT_MAX;
        for (const auto& pair : test_list) {
            minDiff = std::min(minDiff, std::abs(pair[1] - pair[0]));
        }
        return minDiff;
    }
};"""
    },

    809: {
        "starter_code_javascript": "function lcm(x, y) {\n    return 0;\n}",
        "reference_solution_javascript": """function lcm(x, y) {
    function gcd(a, b) {
        while (b !== 0) {
            let t = b;
            b = a % b;
            a = t;
        }
        return a;
    }
    return Math.floor((x * y) / gcd(x, y));
}""",
        "starter_code_java": "class Solution {\n    public int lcm(int x, int y) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    private int gcd(int a, int b) {
        while (b != 0) {
            int t = b;
            b = a % b;
            a = t;
        }
        return a;
    }
    public int lcm(int x, int y) {
        return (x * y) / gcd(x, y);
    }
}""",
        "starter_code_cpp": "class Solution {\npublic:\n    int lcm(int x, int y);\n};",
        "reference_solution_cpp": """#include <numeric>
class Solution {
    int gcd(int a, int b) {
        while (b != 0) {
            int t = b;
            b = a % b;
            a = t;
        }
        return a;
    }
public:
    int lcm(int x, int y) {
        return (x * y) / gcd(x, y);
    }
};"""
    },

    810: {
        "starter_code_javascript": "function sort_String(str) {\n    return '';\n}",
        "reference_solution_javascript": """function sort_String(str) {
    return str.split('').sort().join('');
}""",
        "starter_code_java": "import java.util.Arrays;\nclass Solution {\n    public String sort_String(String str) {\n        return "";\n    }\n}",
        "reference_solution_java": """import java.util.Arrays;
class Solution {
    public String sort_String(String str) {
        char[] chars = str.toCharArray();
        Arrays.sort(chars);
        return new String(chars);
    }
}""",
        "starter_code_cpp": "#include <string>\nclass Solution {\npublic:\n    std::string sort_String(std::string str);\n};",
        "reference_solution_cpp": """#include <string>
#include <algorithm>
class Solution {
public:
    std::string sort_String(std::string str) {
        std::sort(str.begin(), str.end());
        return str;
    }
};"""
    }
}
