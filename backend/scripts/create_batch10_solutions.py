"""
Script to create batch10_solutions.py containing curated solutions for Batch 10 (Problems 511-560).
"""

content = '''"""
Curated and specialized solutions for MBPP problems (Batch 10: 511-560).
"""

BATCH10_SOLUTIONS = {
    511: {
        "starter_code_javascript": "function check_abundant(n) {\\n    return false;\\n}",
        "reference_solution_javascript": """function check_abundant(n) {
    let sum = 0;
    for (let i = 1; i <= Math.floor(Math.sqrt(n)); i++) {
        if (n % i === 0) {
            if (Math.floor(n / i) === i) sum += i;
            else sum += i + Math.floor(n / i);
        }
    }
    sum -= n;
    return sum > n;
}""",
        "starter_code_java": "class Solution {\\n    public boolean check_abundant(int n) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public boolean check_abundant(int n) {
        int sum = 0;
        for (int i = 1; i <= (int) Math.sqrt(n); i++) {
            if (n % i == 0) {
                if (n / i == i) sum += i;
                else sum += i + (n / i);
            }
        }
        sum -= n;
        return sum > n;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    bool check_abundant(int n);\\n};",
        "reference_solution_cpp": """#include <cmath>
class Solution {
public:
    bool check_abundant(int n) {
        int sum = 0;
        for (int i = 1; i <= (int) std::sqrt(n); ++i) {
            if (n % i == 0) {
                if (n / i == i) sum += i;
                else sum += i + (n / i);
            }
        }
        sum -= n;
        return sum > n;
    }
};"""
    },

    512: {
        "starter_code_javascript": "function fill_spaces(text) {\\n    return '';\\n}",
        "reference_solution_javascript": """function fill_spaces(text) {
    return text.replace(/[ ,.]/g, ':');
}""",
        "starter_code_java": "class Solution {\\n    public String fill_spaces(String text) {\\n        return \\"\\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String fill_spaces(String text) {
        return text.replaceAll("[ ,.]", ":");
    }
}""",
        "starter_code_cpp": "#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    string fill_spaces(string text);\\n};",
        "reference_solution_cpp": """#include <string>
using namespace std;
class Solution {
public:
    string fill_spaces(string text) {
        for (char& c : text) {
            if (c == ' ' || c == ',' || c == '.') c = ':';
        }
        return text;
    }
};"""
    },

    513: {
        "starter_code_javascript": "function count_digits(num1, num2) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function count_digits(num1, num2) {
    let n = BigInt(num1) + BigInt(num2);
    let c = 0;
    while (n > 0n) {
        n = n / 10n;
        c++;
    }
    return c;
}""",
        "starter_code_java": "class Solution {\\n    public int count_digits(long num1, long num2) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int count_digits(long num1, long num2) {
        long n = num1 + num2;
        int c = 0;
        while (n > 0) {
            n /= 10;
            c++;
        }
        return c;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int count_digits(long long num1, long long num2);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    int count_digits(long long num1, long long num2) {
        long long n = num1 + num2;
        int c = 0;
        while (n > 0) {
            n /= 10;
            c++;
        }
        return c;
    }
};"""
    },

    514: {
        "starter_code_javascript": "function flatten_tuple(test_list) {\\n    return '';\\n}",
        "reference_solution_javascript": """function flatten_tuple(test_list) {
    return test_list.flat().join(' ');
}""",
        "starter_code_java": "class Solution {\\n    public String flatten_tuple(String[][] test_list) {\\n        return \\"\\";\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public String flatten_tuple(String[][] test_list) {
        List<String> res = new ArrayList<>();
        for (String[] sub : test_list) {
            for (String s : sub) res.add(s);
        }
        return String.join(" ", res);
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    string flatten_tuple(const vector<vector<string>>& test_list);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
using namespace std;
class Solution {
public:
    string flatten_tuple(const vector<vector<string>>& test_list) {
        string res = "";
        for (const auto& sub : test_list) {
            for (const auto& s : sub) {
                if (!res.empty()) res += " ";
                res += s;
            }
        }
        return res;
    }
};"""
    },

    515: {
        "starter_code_javascript": "function toggle_F_and_L_bits(n) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function toggle_F_and_L_bits(n) {
    if (n === 1) return 0;
    let temp = n;
    temp |= temp >> 1;
    temp |= temp >> 2;
    temp |= temp >> 4;
    temp |= temp >> 8;
    temp |= temp >> 16;
    let mask = ((temp + 1) >> 1) + 1;
    return n ^ mask;
}""",
        "starter_code_java": "class Solution {\\n    public int toggle_F_and_L_bits(int n) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int toggle_F_and_L_bits(int n) {
        if (n == 1) return 0;
        int temp = n;
        temp |= temp >> 1;
        temp |= temp >> 2;
        temp |= temp >> 4;
        temp |= temp >> 8;
        temp |= temp >> 16;
        int mask = ((temp + 1) >> 1) + 1;
        return n ^ mask;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int toggle_F_and_L_bits(int n);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    int toggle_F_and_L_bits(int n) {
        if (n == 1) return 0;
        int temp = n;
        temp |= temp >> 1;
        temp |= temp >> 2;
        temp |= temp >> 4;
        temp |= temp >> 8;
        temp |= temp >> 16;
        int mask = ((temp + 1) >> 1) + 1;
        return n ^ mask;
    }
};"""
    },

    516: {
        "starter_code_javascript": "function last_occurence_char(string, char) {\\n    return null;\\n}",
        "reference_solution_javascript": """function last_occurence_char(string, char) {
    let idx = string.lastIndexOf(char);
    return idx === -1 ? null : idx + 1;
}""",
        "starter_code_java": "class Solution {\\n    public Integer last_occurence_char(String string, String ch) {\\n        return null;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public Integer last_occurence_char(String string, String ch) {
        int idx = string.lastIndexOf(ch);
        return idx == -1 ? null : idx + 1;
    }
}""",
        "starter_code_cpp": "#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int last_occurence_char(const string& s, const string& ch);\\n};",
        "reference_solution_cpp": """#include <string>
using namespace std;
class Solution {
public:
    int last_occurence_char(const string& s, const string& ch) {
        if (ch.empty()) return 0;
        size_t idx = s.rfind(ch[0]);
        if (idx == string::npos) return 0;
        return (int) idx + 1;
    }
};"""
    },

    517: {
        "starter_code_javascript": "function Total_Hamming_Distance(n) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function Total_Hamming_Distance(n) {
    let i = 1, sum = 0;
    while (Math.floor(n / i) > 0) {
        sum += Math.floor(n / i);
        i *= 2;
    }
    return sum;
}""",
        "starter_code_java": "class Solution {\\n    public int Total_Hamming_Distance(int n) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int Total_Hamming_Distance(int n) {
        int i = 1, sum = 0;
        while (n / i > 0) {
            sum += n / i;
            i *= 2;
        }
        return sum;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int Total_Hamming_Distance(int n);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    int Total_Hamming_Distance(int n) {
        int i = 1, sum = 0;
        while (n / i > 0) {
            sum += n / i;
            i *= 2;
        }
        return sum;
    }
};"""
    },

    518: {
        "starter_code_javascript": "function longest_increasing_subsequence(arr) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function longest_increasing_subsequence(arr) {
    let n = arr.length;
    if (n === 0) return 0;
    let dp = new Array(n).fill(1);
    for (let i = 1; i < n; i++) {
        for (let j = 0; j < i; j++) {
            if (arr[i] > arr[j] && dp[i] < dp[j] + 1) dp[i] = dp[j] + 1;
        }
    }
    return Math.max(...dp);
}""",
        "starter_code_java": "class Solution {\\n    public int longest_increasing_subsequence(int[] arr) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int longest_increasing_subsequence(int[] arr) {
        int n = arr.length;
        if (n == 0) return 0;
        int[] dp = new int[n];
        Arrays.fill(dp, 1);
        int max = 1;
        for (int i = 1; i < n; i++) {
            for (int j = 0; j < i; j++) {
                if (arr[i] > arr[j] && dp[i] < dp[j] + 1) dp[i] = dp[j] + 1;
            }
            max = Math.max(max, dp[i]);
        }
        return max;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int longest_increasing_subsequence(const vector<int>& arr);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    int longest_increasing_subsequence(const vector<int>& arr) {
        int n = arr.size();
        if (n == 0) return 0;
        vector<int> dp(n, 1);
        int max_len = 1;
        for (int i = 1; i < n; ++i) {
            for (int j = 0; j < i; ++j) {
                if (arr[i] > arr[j] && dp[i] < dp[j] + 1) dp[i] = dp[j] + 1;
            }
            max_len = max(max_len, dp[i]);
        }
        return max_len;
    }
};"""
    },

    519: {
        "starter_code_javascript": "function odd_Num_Sum(n) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function odd_Num_Sum(n) {
    let sm = 0;
    for (let i = 1; i <= n; i++) {
        let j = 2 * i - 1;
        sm += Math.pow(j, 5);
    }
    return sm;
}""",
        "starter_code_java": "class Solution {\\n    public int odd_Num_Sum(int n) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int odd_Num_Sum(int n) {
        long sm = 0;
        for (int i = 1; i <= n; i++) {
            long j = 2 * i - 1;
            sm += j * j * j * j * j;
        }
        return (int) sm;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int odd_Num_Sum(int n);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    int odd_Num_Sum(int n) {
        long long sm = 0;
        for (int i = 1; i <= n; ++i) {
            long long j = 2 * i - 1;
            sm += j * j * j * j * j;
        }
        return (int) sm;
    }
};"""
    },

    520: {
        "starter_code_javascript": "function find_Max(arr, low, high) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function find_Max(arr, low, high) {
    if (high < low) return arr[0];
    if (high === low) return arr[low];
    let mid = low + Math.floor((high - low) / 2);
    if (mid < high && arr[mid + 1] < arr[mid]) return arr[mid];
    if (mid > low && arr[mid] < arr[mid - 1]) return arr[mid - 1];
    if (arr[low] > arr[mid]) return find_Max(arr, low, mid - 1);
    else return find_Max(arr, mid + 1, high);
}""",
        "starter_code_java": "class Solution {\\n    public int find_Max(int[] arr, int low, int high) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int find_Max(int[] arr, int low, int high) {
        if (high < low) return arr[0];
        if (high == low) return arr[low];
        int mid = low + (high - low) / 2;
        if (mid < high && arr[mid + 1] < arr[mid]) return arr[mid];
        if (mid > low && arr[mid] < arr[mid - 1]) return arr[mid - 1];
        if (arr[low] > arr[mid]) return find_Max(arr, low, mid - 1);
        else return find_Max(arr, mid + 1, high);
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int find_Max(const vector<int>& arr, int low, int high);\\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    int find_Max(const vector<int>& arr, int low, int high) {
        if (high < low) return arr[0];
        if (high == low) return arr[low];
        int mid = low + (high - low) / 2;
        if (mid < high && arr[mid + 1] < arr[mid]) return arr[mid];
        if (mid > low && arr[mid] < arr[mid - 1]) return arr[mid - 1];
        if (arr[low] > arr[mid]) return find_Max(arr, low, mid - 1);
        else return find_Max(arr, mid + 1, high);
    }
};"""
    },

    521: {
        "starter_code_javascript": "function extract_column(list1, n) {\\n    return [];\\n}",
        "reference_solution_javascript": """function extract_column(list1, n) {
    return list1.map(row => row[n]);
}""",
        "starter_code_java": "class Solution {\\n    public int[] extract_column(int[][] list1, int n) {\\n        return new int[]{};\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int[] extract_column(int[][] list1, int n) {
        int[] res = new int[list1.length];
        for (int i = 0; i < list1.length; i++) res[i] = list1[i][n];
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<int> extract_column(const vector<vector<int>>& list1, int n);\\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    vector<int> extract_column(const vector<vector<int>>& list1, int n) {
        vector<int> res;
        for (const auto& row : list1) res.push_back(row[n]);
        return res;
    }
};"""
    },

    522: {
        "starter_code_javascript": "function Seq_Linear(seq_nums) {\\n    return '';\\n}",
        "reference_solution_javascript": """function Seq_Linear(seq_nums) {
    if (seq_nums.length <= 2) return "Linear Sequence";
    let diff = seq_nums[1] - seq_nums[0];
    for (let i = 2; i < seq_nums.length; i++) {
        if (seq_nums[i] - seq_nums[i - 1] !== diff) return "Non Linear Sequence";
    }
    return "Linear Sequence";
}""",
        "starter_code_java": "class Solution {\\n    public String Seq_Linear(int[] seq_nums) {\\n        return \\"\\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String Seq_Linear(int[] seq_nums) {
        if (seq_nums.length <= 2) return "Linear Sequence";
        int diff = seq_nums[1] - seq_nums[0];
        for (int i = 2; i < seq_nums.length; i++) {
            if (seq_nums[i] - seq_nums[i - 1] != diff) return "Non Linear Sequence";
        }
        return "Linear Sequence";
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    string Seq_Linear(const vector<int>& seq_nums);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
using namespace std;
class Solution {
public:
    string Seq_Linear(const vector<int>& seq_nums) {
        if (seq_nums.size() <= 2) return "Linear Sequence";
        int diff = seq_nums[1] - seq_nums[0];
        for (size_t i = 2; i < seq_nums.size(); ++i) {
            if (seq_nums[i] - seq_nums[i - 1] != diff) return "Non Linear Sequence";
        }
        return "Linear Sequence";
    }
};"""
    },

    523: {
        "starter_code_javascript": "function tuple_to_float(test_tup) {\\n    return 0.0;\\n}",
        "reference_solution_javascript": """function tuple_to_float(test_tup) {
    return parseFloat(test_tup.join('.'));
}""",
        "starter_code_java": "class Solution {\\n    public double tuple_to_float(int[] test_tup) {\\n        return 0.0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public double tuple_to_float(int[] test_tup) {
        String s = test_tup[0] + "." + test_tup[1];
        return Double.parseDouble(s);
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    double tuple_to_float(const vector<int>& test_tup);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
using namespace std;
class Solution {
public:
    double tuple_to_float(const vector<int>& test_tup) {
        string s = to_string(test_tup[0]) + "." + to_string(test_tup[1]);
        return stod(s);
    }
};"""
    },

    524: {
        "starter_code_javascript": "function Split(list) {\\n    return [];\\n}",
        "reference_solution_javascript": """function Split(list) {
    return list.filter(x => x % 2 !== 0);
}""",
        "starter_code_java": "class Solution {\\n    public int[] Split(int[] list) {\\n        return new int[]{};\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[] Split(int[] list) {
        List<Integer> res = new ArrayList<>();
        for (int x : list) if (x % 2 != 0) res.add(x);
        int[] out = new int[res.size()];
        for (int i = 0; i < res.size(); i++) out[i] = res.get(i);
        return out;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<int> Split(const vector<int>& list);\\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    vector<int> Split(const vector<int>& list) {
        vector<int> res;
        for (int x : list) if (x % 2 != 0) res.push_back(x);
        return res;
    }
};"""
    },

    525: {
        "starter_code_javascript": "function difference(n) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function difference(n) {
    let S = Math.floor((n * (n + 1)) / 2);
    return S * (S - 1);
}""",
        "starter_code_java": "class Solution {\\n    public int difference(int n) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int difference(int n) {
        int S = (n * (n + 1)) / 2;
        return S * (S - 1);
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int difference(int n);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    int difference(int n) {
        int S = (n * (n + 1)) / 2;
        return S * (S - 1);
    }
};"""
    },

    526: {
        "starter_code_javascript": "function find_Odd_Pair(A, N) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function find_Odd_Pair(A, N) {
    let odd = 0, even = 0;
    for (let i = 0; i < N; i++) {
        if (A[i] % 2 !== 0) odd++;
        else even++;
    }
    return odd * even;
}""",
        "starter_code_java": "class Solution {\\n    public int find_Odd_Pair(int[] A, int N) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int find_Odd_Pair(int[] A, int N) {
        int odd = 0, even = 0;
        for (int i = 0; i < N; i++) {
            if (A[i] % 2 != 0) odd++;
            else even++;
        }
        return odd * even;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int find_Odd_Pair(const vector<int>& A, int N);\\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    int find_Odd_Pair(const vector<int>& A, int N) {
        int odd = 0, even = 0;
        for (int i = 0; i < N; ++i) {
            if (A[i] % 2 != 0) odd++;
            else even++;
        }
        return odd * even;
    }
};"""
    },

    527: {
        "starter_code_javascript": "function toggle_string(string) {\\n    return '';\\n}",
        "reference_solution_javascript": """function toggle_string(string) {
    return string.split('').map(c => c === c.toUpperCase() ? c.toLowerCase() : c.toUpperCase()).join('');
}""",
        "starter_code_java": "class Solution {\\n    public String toggle_string(String string) {\\n        return \\"\\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String toggle_string(String string) {
        StringBuilder sb = new StringBuilder();
        for (char c : string.toCharArray()) {
            if (Character.isUpperCase(c)) sb.append(Character.toLowerCase(c));
            else sb.append(Character.toUpperCase(c));
        }
        return sb.toString();
    }
}""",
        "starter_code_cpp": "#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    string toggle_string(string string);\\n};",
        "reference_solution_cpp": """#include <string>
#include <cctype>
using namespace std;
class Solution {
public:
    string toggle_string(string s) {
        for (char& c : s) {
            if (isupper((unsigned char)c)) c = tolower((unsigned char)c);
            else if (islower((unsigned char)c)) c = toupper((unsigned char)c);
        }
        return s;
    }
};"""
    },

    528: {
        "starter_code_javascript": "function digit_distance_nums(n1, n2) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function digit_distance_nums(n1, n2) {
    let diff = Math.abs(n1 - n2);
    return String(diff).split('').reduce((sum, d) => sum + parseInt(d), 0);
}""",
        "starter_code_java": "class Solution {\\n    public int digit_distance_nums(int n1, int n2) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int digit_distance_nums(int n1, int n2) {
        int diff = Math.abs(n1 - n2);
        int sum = 0;
        while (diff > 0) {
            sum += diff % 10;
            diff /= 10;
        }
        return sum;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int digit_distance_nums(int n1, int n2);\\n};",
        "reference_solution_cpp": """#include <cmath>
class Solution {
public:
    int digit_distance_nums(int n1, int n2) {
        int diff = std::abs(n1 - n2);
        int sum = 0;
        while (diff > 0) {
            sum += diff % 10;
            diff /= 10;
        }
        return sum;
    }
};"""
    },

    529: {
        "starter_code_javascript": "function max_sub_array_sum(a, size) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function max_sub_array_sum(a, size) {
    let max_so_far = 0, max_ending_here = 0;
    for (let i = 0; i < size; i++) {
        max_ending_here += a[i];
        if (max_ending_here < 0) max_ending_here = 0;
        else if (max_so_far < max_ending_here) max_so_far = max_ending_here;
    }
    return max_so_far;
}""",
        "starter_code_java": "class Solution {\\n    public int max_sub_array_sum(int[] a, int size) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int max_sub_array_sum(int[] a, int size) {
        int max_so_far = 0, max_ending_here = 0;
        for (int i = 0; i < size; i++) {
            max_ending_here += a[i];
            if (max_ending_here < 0) max_ending_here = 0;
            else if (max_so_far < max_ending_here) max_so_far = max_ending_here;
        }
        return max_so_far;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int max_sub_array_sum(const vector<int>& a, int size);\\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    int max_sub_array_sum(const vector<int>& a, int size) {
        int max_so_far = 0, max_ending_here = 0;
        for (int i = 0; i < size; ++i) {
            max_ending_here += a[i];
            if (max_ending_here < 0) max_ending_here = 0;
            else if (max_so_far < max_ending_here) max_so_far = max_ending_here;
        }
        return max_so_far;
    }
};"""
    },

    530: {
        "starter_code_javascript": "function Find_Max_Length(lst) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function Find_Max_Length(lst) {
    return Math.max(...lst.map(x => x.length));
}""",
        "starter_code_java": "class Solution {\\n    public int Find_Max_Length(int[][] lst) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int Find_Max_Length(int[][] lst) {
        int max = 0;
        for (int[] x : lst) if (x.length > max) max = x.length;
        return max;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int Find_Max_Length(const vector<vector<int>>& lst);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    int Find_Max_Length(const vector<vector<int>>& lst) {
        int max_len = 0;
        for (const auto& x : lst) max_len = max(max_len, (int)x.size());
        return max_len;
    }
};"""
    },

    531: {
        "starter_code_javascript": "function extract_values(text) {\\n    return [];\\n}",
        "reference_solution_javascript": """function extract_values(text) {
    let matches = text.match(/"([^"]*)"/g);
    if (!matches) return [];
    return matches.map(m => m.slice(1, -1));
}""",
        "starter_code_java": "class Solution {\\n    public String[] extract_values(String text) {\\n        return new String[]{};\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public String[] extract_values(String text) {
        List<String> list = new ArrayList<>();
        int i = 0;
        while (i < text.length()) {
            int start = text.indexOf('"', i);
            if (start == -1) break;
            int end = text.indexOf('"', start + 1);
            if (end == -1) break;
            list.add(text.substring(start + 1, end));
            i = end + 1;
        }
        return list.toArray(new String[0]);
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<string> extract_values(const string& text);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
using namespace std;
class Solution {
public:
    vector<string> extract_values(const string& text) {
        vector<string> res;
        size_t i = 0;
        while (i < text.length()) {
            size_t start = text.find('"', i);
            if (start == string::npos) break;
            size_t end = text.find('"', start + 1);
            if (end == string::npos) break;
            res.push_back(text.substr(start + 1, end - start - 1));
            i = end + 1;
        }
        return res;
    }
};"""
    },

    532: {
        "starter_code_javascript": "function count_Pairs(arr, n) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function count_Pairs(arr, n) {
    let cnt = 0;
    for (let i = 0; i < n; i++) {
        for (let j = i + 1; j < n; j++) {
            if (arr[i] !== arr[j]) cnt++;
        }
    }
    return cnt;
}""",
        "starter_code_java": "class Solution {\\n    public int count_Pairs(int[] arr, int n) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int count_Pairs(int[] arr, int n) {
        int cnt = 0;
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                if (arr[i] != arr[j]) cnt++;
            }
        }
        return cnt;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int count_Pairs(const vector<int>& arr, int n);\\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    int count_Pairs(const vector<int>& arr, int n) {
        int cnt = 0;
        for (int i = 0; i < n; ++i) {
            for (int j = i + 1; j < n; ++j) {
                if (arr[i] != arr[j]) cnt++;
            }
        }
        return cnt;
    }
};"""
    },

    533: {
        "starter_code_javascript": "function split(word) {\\n    return [];\\n}",
        "reference_solution_javascript": """function split(word) {
    return word.split('');
}""",
        "starter_code_java": "class Solution {\\n    public String[] split(String word) {\\n        return new String[]{};\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String[] split(String word) {
        String[] res = new String[word.length()];
        for (int i = 0; i < word.length(); i++) {
            res[i] = String.valueOf(word.charAt(i));
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<string> split(const string& word);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
using namespace std;
class Solution {
public:
    vector<string> split(const string& word) {
        vector<string> res;
        for (char c : word) res.push_back(string(1, c));
        return res;
    }
};"""
    },

    534: {
        "starter_code_javascript": "function sum_digits(n) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function sum_digits(n) {
    let sum = 0;
    while (n > 0) {
        sum += n % 10;
        n = Math.floor(n / 10);
    }
    return sum;
}""",
        "starter_code_java": "class Solution {\\n    public int sum_digits(int n) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int sum_digits(int n) {
        int sum = 0;
        while (n > 0) {
            sum += n % 10;
            n /= 10;
        }
        return sum;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int sum_digits(int n);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    int sum_digits(int n) {
        int sum = 0;
        while (n > 0) {
            sum += n % 10;
            n /= 10;
        }
        return sum;
    }
};"""
    },

    535: {
        "starter_code_javascript": "function issort_list(list1) {\\n    return false;\\n}",
        "reference_solution_javascript": """function issort_list(list1) {
    for (let i = 0; i < list1.length - 1; i++) {
        if (list1[i] > list1[i + 1]) return false;
    }
    return true;
}""",
        "starter_code_java": "class Solution {\\n    public boolean issort_list(int[] list1) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public boolean issort_list(int[] list1) {
        for (int i = 0; i < list1.length - 1; i++) {
            if (list1[i] > list1[i + 1]) return false;
        }
        return true;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    bool issort_list(const vector<int>& list1);\\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    bool issort_list(const vector<int>& list1) {
        for (size_t i = 0; i + 1 < list1.size(); ++i) {
            if (list1[i] > list1[i + 1]) return false;
        }
        return true;
    }
};"""
    },

    536: {
        "starter_code_javascript": "function empty_list(length) {\\n    return [];\\n}",
        "reference_solution_javascript": """function empty_list(length) {
    return Array.from({length}, () => ({}));
}""",
        "starter_code_java": "class Solution {\\n    public Object[] empty_list(int length) {\\n        return new Object[]{};\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public Object[] empty_list(int length) {
        Object[] res = new Object[length];
        for (int i = 0; i < length; i++) res[i] = new HashMap<String, Object>();
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <unordered_map>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<unordered_map<string, string>> empty_list(int length);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <unordered_map>
#include <string>
using namespace std;
class Solution {
public:
    vector<unordered_map<string, string>> empty_list(int length) {
        return vector<unordered_map<string, string>>(length);
    }
};"""
    },

    537: {
        "starter_code_javascript": "function sort_sublists(list1) {\\n    return [];\\n}",
        "reference_solution_javascript": """function sort_sublists(list1) {
    return list1.map(sub => [...sub].sort());
}""",
        "starter_code_java": "class Solution {\\n    public String[][] sort_sublists(String[][] list1) {\\n        return new String[][]{};\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public String[][] sort_sublists(String[][] list1) {
        String[][] res = new String[list1.length][];
        for (int i = 0; i < list1.length; i++) {
            res[i] = list1[i].clone();
            Arrays.sort(res[i]);
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<vector<string>> sort_sublists(vector<vector<string>> list1);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <algorithm>
using namespace std;
class Solution {
public:
    vector<vector<string>> sort_sublists(vector<vector<string>> list1) {
        for (auto& sub : list1) sort(sub.begin(), sub.end());
        return list1;
    }
};"""
    },

    538: {
        "starter_code_javascript": "function remove_words(list1, charlist) {\\n    return [];\\n}",
        "reference_solution_javascript": """function remove_words(list1, charlist) {
    return list1.map(line => {
        let words = line.split(/\\\\s+/).filter(w => w.length > 0);
        let kept = words.filter(word => !charlist.some(phrase => word.includes(phrase)));
        return kept.join(' ');
    });
}""",
        "starter_code_java": "class Solution {\\n    public String[] remove_words(String[] list1, String[] charlist) {\\n        return new String[]{};\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public String[] remove_words(String[] list1, String[] charlist) {
        String[] res = new String[list1.length];
        for (int i = 0; i < list1.length; i++) {
            String line = list1[i].trim();
            if (line.isEmpty()) { res[i] = ""; continue; }
            String[] words = line.split("\\\\\\\\s+");
            List<String> kept = new ArrayList<>();
            for (String w : words) {
                boolean contains = false;
                for (String ph : charlist) {
                    if (w.contains(ph)) { contains = true; break; }
                }
                if (!contains) kept.add(w);
            }
            res[i] = String.join(" ", kept);
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<string> remove_words(const vector<string>& list1, const vector<string>& charlist);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <sstream>
using namespace std;
class Solution {
public:
    vector<string> remove_words(const vector<string>& list1, const vector<string>& charlist) {
        vector<string> res;
        for (const auto& line : list1) {
            stringstream ss(line);
            string w;
            vector<string> kept;
            while (ss >> w) {
                bool contains = false;
                for (const auto& ph : charlist) {
                    if (w.find(ph) != string::npos) { contains = true; break; }
                }
                if (!contains) kept.push_back(w);
            }
            string out = "";
            for (size_t i = 0; i < kept.size(); ++i) {
                if (i > 0) out += " ";
                out += kept[i];
            }
            res.push_back(out);
        }
        return res;
    }
};"""
    },

    539: {
        "starter_code_javascript": "function max_sum_pair_diff_lessthan_K(arr, N, K) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function max_sum_pair_diff_lessthan_K(arr, N, K) {
    let sorted = [...arr].sort((a, b) => a - b);
    let dp = new Array(N).fill(0);
    for (let i = 1; i < N; i++) {
        dp[i] = dp[i - 1];
        if (sorted[i] - sorted[i - 1] < K) {
            if (i >= 2) dp[i] = Math.max(dp[i], dp[i - 2] + sorted[i] + sorted[i - 1]);
            else dp[i] = Math.max(dp[i], sorted[i] + sorted[i - 1]);
        }
    }
    return dp[N - 1];
}""",
        "starter_code_java": "class Solution {\\n    public int max_sum_pair_diff_lessthan_K(int[] arr, int N, int K) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int max_sum_pair_diff_lessthan_K(int[] arr, int N, int K) {
        int[] sorted = arr.clone();
        Arrays.sort(sorted);
        int[] dp = new int[N];
        for (int i = 1; i < N; i++) {
            dp[i] = dp[i - 1];
            if (sorted[i] - sorted[i - 1] < K) {
                if (i >= 2) dp[i] = Math.max(dp[i], dp[i - 2] + sorted[i] + sorted[i - 1]);
                else dp[i] = Math.max(dp[i], sorted[i] + sorted[i - 1]);
            }
        }
        return dp[N - 1];
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int max_sum_pair_diff_lessthan_K(vector<int> arr, int N, int K);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    int max_sum_pair_diff_lessthan_K(vector<int> arr, int N, int K) {
        sort(arr.begin(), arr.end());
        vector<int> dp(N, 0);
        for (int i = 1; i < N; ++i) {
            dp[i] = dp[i - 1];
            if (arr[i] - arr[i - 1] < K) {
                if (i >= 2) dp[i] = max(dp[i], dp[i - 2] + arr[i] + arr[i - 1]);
                else dp[i] = max(dp[i], arr[i] + arr[i - 1]);
            }
        }
        return dp[N - 1];
    }
};"""
    },

    540: {
        "starter_code_javascript": "function two_unique_nums(nums) {\\n    return [];\\n}",
        "reference_solution_javascript": """function two_unique_nums(nums) {
    let counts = {};
    for (let x of nums) counts[x] = (counts[x] || 0) + 1;
    return nums.filter(x => counts[x] === 1);
}""",
        "starter_code_java": "class Solution {\\n    public int[] two_unique_nums(int[] nums) {\\n        return new int[]{};\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[] two_unique_nums(int[] nums) {
        Map<Integer, Integer> map = new LinkedHashMap<>();
        for (int x : nums) map.put(x, map.getOrDefault(x, 0) + 1);
        List<Integer> list = new ArrayList<>();
        for (int x : nums) if (map.get(x) == 1) list.add(x);
        int[] res = new int[list.size()];
        for (int i = 0; i < list.size(); i++) res[i] = list.get(i);
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<int> two_unique_nums(const vector<int>& nums);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <unordered_map>
using namespace std;
class Solution {
public:
    vector<int> two_unique_nums(const vector<int>& nums) {
        unordered_map<int, int> counts;
        for (int x : nums) counts[x]++;
        vector<int> res;
        for (int x : nums) if (counts[x] == 1) res.push_back(x);
        return res;
    }
};"""
    },

    541: {
        "starter_code_javascript": "function unique_product(list_data) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function unique_product(list_data) {
    let uniq = [...new Set(list_data)];
    return uniq.reduce((p, x) => p * x, 1);
}""",
        "starter_code_java": "class Solution {\\n    public int unique_product(int[] list_data) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int unique_product(int[] list_data) {
        Set<Integer> set = new HashSet<>();
        for (int x : list_data) set.add(x);
        long prod = 1;
        for (int x : set) prod *= x;
        return (int) prod;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int unique_product(const vector<int>& list_data);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <unordered_set>
using namespace std;
class Solution {
public:
    int unique_product(const vector<int>& list_data) {
        unordered_set<int> s(list_data.begin(), list_data.end());
        long long prod = 1;
        for (int x : s) prod *= x;
        return (int) prod;
    }
};"""
    },

    542: {
        "starter_code_javascript": "function surfacearea_cylinder(r, h) {\\n    return 0.0;\\n}",
        "reference_solution_javascript": """function surfacearea_cylinder(r, h) {
    return (2 * 3.1415 * r * r) + (2 * 3.1415 * r * h);
}""",
        "starter_code_java": "class Solution {\\n    public double surfacearea_cylinder(int r, int h) {\\n        return 0.0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public double surfacearea_cylinder(int r, int h) {
        return (2.0 * 3.1415 * r * r) + (2.0 * 3.1415 * r * h);
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    double surfacearea_cylinder(int r, int h);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    double surfacearea_cylinder(int r, int h) {
        return (2.0 * 3.1415 * r * r) + (2.0 * 3.1415 * r * h);
    }
};"""
    },

    543: {
        "starter_code_javascript": "function count_no(A, N, L, R) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function count_no(A, N, L, R) {
    let count = 0, ans = L;
    for (let i = L; i <= R; i++) {
        if (i % A !== 0) count++;
        if (count === N) { ans = i; break; }
    }
    return ans;
}""",
        "starter_code_java": "class Solution {\\n    public int count_no(int A, int N, int L, int R) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int count_no(int A, int N, int L, int R) {
        int count = 0, ans = L;
        for (int i = L; i <= R; i++) {
            if (i % A != 0) count++;
            if (count == N) { ans = i; break; }
        }
        return ans;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int count_no(int A, int N, int L, int R);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    int count_no(int A, int N, int L, int R) {
        int count = 0, ans = L;
        for (int i = L; i <= R; ++i) {
            if (i % A != 0) count++;
            if (count == N) { ans = i; break; }
        }
        return ans;
    }
};"""
    },

    544: {
        "starter_code_javascript": "function is_Sub_Array(A, B, n, m) {\\n    return false;\\n}",
        "reference_solution_javascript": """function is_Sub_Array(A, B, n, m) {
    let i = 0, j = 0;
    while (i < n && j < m) {
        if (A[i] === B[j]) {
            i++; j++;
            if (j === m) return true;
        } else {
            i = i - j + 1;
            j = 0;
        }
    }
    return false;
}""",
        "starter_code_java": "class Solution {\\n    public boolean is_Sub_Array(int[] A, int[] B, int n, int m) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public boolean is_Sub_Array(int[] A, int[] B, int n, int m) {
        int i = 0, j = 0;
        while (i < n && j < m) {
            if (A[i] == B[j]) {
                i++; j++;
                if (j == m) return true;
            } else {
                i = i - j + 1;
                j = 0;
            }
        }
        return false;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    bool is_Sub_Array(const vector<int>& A, const vector<int>& B, int n, int m);\\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    bool is_Sub_Array(const vector<int>& A, const vector<int>& B, int n, int m) {
        int i = 0, j = 0;
        while (i < n && j < m) {
            if (A[i] == B[j]) {
                i++; j++;
                if (j == m) return true;
            } else {
                i = i - j + 1;
                j = 0;
            }
        }
        return false;
    }
};"""
    },

    545: {
        "starter_code_javascript": "function last_Digit_Factorial(n) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function last_Digit_Factorial(n) {
    if (n === 0) return 1;
    if (n <= 2) return n;
    if (n === 3) return 6;
    if (n === 4) return 4;
    return 0;
}""",
        "starter_code_java": "class Solution {\\n    public int last_Digit_Factorial(int n) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int last_Digit_Factorial(int n) {
        if (n == 0) return 1;
        if (n <= 2) return n;
        if (n == 3) return 6;
        if (n == 4) return 4;
        return 0;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int last_Digit_Factorial(int n);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    int last_Digit_Factorial(int n) {
        if (n == 0) return 1;
        if (n <= 2) return n;
        if (n == 3) return 6;
        if (n == 4) return 4;
        return 0;
    }
};"""
    },

    546: {
        "starter_code_javascript": "function interleave_lists(list1, list2, list3) {\\n    return [];\\n}",
        "reference_solution_javascript": """function interleave_lists(list1, list2, list3) {
    let res = [];
    let len = Math.min(list1.length, list2.length, list3.length);
    for (let i = 0; i < len; i++) {
        res.push(list1[i], list2[i], list3[i]);
    }
    return res;
}""",
        "starter_code_java": "class Solution {\\n    public int[] interleave_lists(int[] list1, int[] list2, int[] list3) {\\n        return new int[]{};\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int[] interleave_lists(int[] list1, int[] list2, int[] list3) {
        int len = Math.min(list1.length, Math.min(list2.length, list3.length));
        int[] res = new int[len * 3];
        int idx = 0;
        for (int i = 0; i < len; i++) {
            res[idx++] = list1[i];
            res[idx++] = list2[i];
            res[idx++] = list3[i];
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<int> interleave_lists(const vector<int>& list1, const vector<int>& list2, const vector<int>& list3);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    vector<int> interleave_lists(const vector<int>& list1, const vector<int>& list2, const vector<int>& list3) {
        int len = min({(int)list1.size(), (int)list2.size(), (int)list3.size()});
        vector<int> res;
        res.reserve(len * 3);
        for (int i = 0; i < len; ++i) {
            res.push_back(list1[i]);
            res.push_back(list2[i]);
            res.push_back(list3[i]);
        }
        return res;
    }
};"""
    },

    547: {
        "starter_code_javascript": "function surface_Area(b, s) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function surface_Area(b, s) {
    return 2 * b * s + b * b;
}""",
        "starter_code_java": "class Solution {\\n    public int surface_Area(int b, int s) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int surface_Area(int b, int s) {
        return 2 * b * s + b * b;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int surface_Area(int b, int s);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    int surface_Area(int b, int s) {
        return 2 * b * s + b * b;
    }
};"""
    },

    548: {
        "starter_code_javascript": "function catalan_number(num) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function catalan_number(num) {
    if (num <= 1) return 1;
    let c = new Array(num + 1).fill(0);
    c[0] = 1; c[1] = 1;
    for (let i = 2; i <= num; i++) {
        for (let j = 0; j < i; j++) {
            c[i] += c[j] * c[i - j - 1];
        }
    }
    return c[num];
}""",
        "starter_code_java": "class Solution {\\n    public int catalan_number(int num) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int catalan_number(int num) {
        if (num <= 1) return 1;
        int[] c = new int[num + 1];
        c[0] = 1; c[1] = 1;
        for (int i = 2; i <= num; i++) {
            for (int j = 0; j < i; j++) {
                c[i] += c[j] * c[i - j - 1];
            }
        }
        return c[num];
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int catalan_number(int num);\\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    int catalan_number(int num) {
        if (num <= 1) return 1;
        vector<int> c(num + 1, 0);
        c[0] = 1; c[1] = 1;
        for (int i = 2; i <= num; ++i) {
            for (int j = 0; j < i; ++j) {
                c[i] += c[j] * c[i - j - 1];
            }
        }
        return c[num];
    }
};"""
    },

    549: {
        "starter_code_javascript": "function find_adverbs(text) {\\n    return '';\\n}",
        "reference_solution_javascript": """function find_adverbs(text) {
    let m = text.match(/\\\\w+ly/);
    if (m) {
        let start = m.index;
        let end = start + m[0].length;
        return `${start}-${end}: ${m[0]}`;
    }
    return "";
}""",
        "starter_code_java": "class Solution {\\n    public String find_adverbs(String text) {\\n        return \\"\\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String find_adverbs(String text) {
        int n = text.length();
        int i = 0;
        while (i < n) {
            while (i < n && !Character.isLetter(text.charAt(i))) i++;
            int start = i;
            while (i < n && Character.isLetter(text.charAt(i))) i++;
            int end = i;
            if (end > start) {
                String word = text.substring(start, end);
                if (word.endsWith("ly")) {
                    return start + "-" + end + ": " + word;
                }
            }
        }
        return "";
    }
}""",
        "starter_code_cpp": "#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    string find_adverbs(const string& text);\\n};",
        "reference_solution_cpp": """#include <string>
#include <cctype>
using namespace std;
class Solution {
public:
    string find_adverbs(const string& text) {
        int n = text.length();
        int i = 0;
        while (i < n) {
            while (i < n && !isalpha((unsigned char)text[i])) i++;
            int start = i;
            while (i < n && isalpha((unsigned char)text[i])) i++;
            int end = i;
            if (end > start) {
                string word = text.substr(start, end - start);
                if (word.length() >= 2 && word.substr(word.length() - 2) == "ly") {
                    return to_string(start) + "-" + to_string(end) + ": " + word;
                }
            }
        }
        return "";
    }
};"""
    },

    550: {
        "starter_code_javascript": "function expensive_items(items, n) {\\n    return [];\\n}",
        "reference_solution_javascript": """function expensive_items(items, n) {
    return [...items].sort((a, b) => b.price - a.price).slice(0, n);
}""",
        "starter_code_java": "class Solution {\\n    public Object[] expensive_items(Object[] items, int n) {\\n        return new Object[]{};\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public Object[] expensive_items(Object[] items, int n) {
        List<Map<String, Object>> list = new ArrayList<>();
        for (Object obj : items) list.add((Map<String, Object>) obj);
        list.sort((a, b) -> Double.compare(((Number) b.get("price")).doubleValue(), ((Number) a.get("price")).doubleValue()));
        return list.subList(0, Math.min(n, list.size())).toArray(new Object[0]);
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <unordered_map>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<unordered_map<string, string>> expensive_items(vector<unordered_map<string, string>> items, int n);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <unordered_map>
#include <string>
#include <algorithm>
using namespace std;
class Solution {
public:
    vector<unordered_map<string, string>> expensive_items(vector<unordered_map<string, string>> items, int n) {
        sort(items.begin(), items.end(), [](const unordered_map<string, string>& a, const unordered_map<string, string>& b) {
            double pa = stod(a.at("price"));
            double pb = stod(b.at("price"));
            return pa > pb;
        });
        if ((int)items.size() > n) items.resize(n);
        return items;
    }
};"""
    },

    551: {
        "starter_code_javascript": "function split_Arr(a, n, k) {\\n    return [];\\n}",
        "reference_solution_javascript": """function split_Arr(a, n, k) {
    return a.slice(k).concat(a.slice(0, k));
}""",
        "starter_code_java": "class Solution {\\n    public int[] split_Arr(int[] a, int n, int k) {\\n        return new int[]{};\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int[] split_Arr(int[] a, int n, int k) {
        int[] res = new int[n];
        int idx = 0;
        for (int i = k; i < n; i++) res[idx++] = a[i];
        for (int i = 0; i < k; i++) res[idx++] = a[i];
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<int> split_Arr(const vector<int>& a, int n, int k);\\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    vector<int> split_Arr(const vector<int>& a, int n, int k) {
        vector<int> res;
        res.reserve(n);
        for (int i = k; i < n; ++i) res.push_back(a[i]);
        for (int i = 0; i < k; ++i) res.push_back(a[i]);
        return res;
    }
};"""
    },

    552: {
        "starter_code_javascript": "function big_diff(nums) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function big_diff(nums) {
    return Math.max(...nums) - Math.min(...nums);
}""",
        "starter_code_java": "class Solution {\\n    public int big_diff(int[] nums) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int big_diff(int[] nums) {
        int min = nums[0], max = nums[0];
        for (int x : nums) {
            if (x < min) min = x;
            if (x > max) max = x;
        }
        return max - min;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int big_diff(const vector<int>& nums);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    int big_diff(const vector<int>& nums) {
        int mn = nums[0], mx = nums[0];
        for (int x : nums) {
            if (x < mn) mn = x;
            if (x > mx) mx = x;
        }
        return mx - mn;
    }
};"""
    },

    553: {
        "starter_code_javascript": "function perfect_squares(a, b) {\\n    return [];\\n}",
        "reference_solution_javascript": """function perfect_squares(a, b) {
    let res = [];
    let start = Math.ceil(Math.sqrt(a));
    while (start * start <= b) {
        res.push(start * start);
        start++;
    }
    return res;
}""",
        "starter_code_java": "class Solution {\\n    public int[] perfect_squares(int a, int b) {\\n        return new int[]{};\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[] perfect_squares(int a, int b) {
        List<Integer> list = new ArrayList<>();
        int start = (int) Math.ceil(Math.sqrt(a));
        while (start * start <= b) {
            list.add(start * start);
            start++;
        }
        int[] res = new int[list.size()];
        for (int i = 0; i < list.size(); i++) res[i] = list.get(i);
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<int> perfect_squares(int a, int b);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <cmath>
using namespace std;
class Solution {
public:
    vector<int> perfect_squares(int a, int b) {
        vector<int> res;
        int start = (int)ceil(sqrt(a));
        while (start * start <= b) {
            res.push_back(start * start);
            start++;
        }
        return res;
    }
};"""
    },

    554: {
        "starter_code_javascript": "function swap_List(newList) {\\n    return [];\\n}",
        "reference_solution_javascript": """function swap_List(newList) {
    let res = [...newList];
    let temp = res[0];
    res[0] = res[res.length - 1];
    res[res.length - 1] = temp;
    return res;
}""",
        "starter_code_java": "class Solution {\\n    public int[] swap_List(int[] newList) {\\n        return new int[]{};\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int[] swap_List(int[] newList) {
        int[] res = newList.clone();
        int temp = res[0];
        res[0] = res[res.length - 1];
        res[res.length - 1] = temp;
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<int> swap_List(vector<int> newList);\\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    vector<int> swap_List(vector<int> newList) {
        if (!newList.empty()) {
            int temp = newList.front();
            newList.front() = newList.back();
            newList.back() = temp;
        }
        return newList;
    }
};"""
    },

    555: {
        "starter_code_javascript": "function sum_Of_product(n) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function sum_Of_product(n) {
    const C = (n, k) => {
        let res = 1;
        if (k > n - k) k = n - k;
        for (let i = 0; i < k; i++) {
            res = (res * (n - i)) / (i + 1);
        }
        return Math.round(res);
    };
    return C(2 * n, n - 1);
}""",
        "starter_code_java": "class Solution {\\n    public int sum_Of_product(int n) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    private long C(int n, int k) {
        long res = 1;
        if (k > n - k) k = n - k;
        for (int i = 0; i < k; i++) {
            res = (res * (n - i)) / (i + 1);
        }
        return res;
    }
    public int sum_Of_product(int n) {
        return (int) C(2 * n, n - 1);
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int sum_Of_product(int n);\\n};",
        "reference_solution_cpp": """class Solution {
    long long C(int n, int k) {
        long long res = 1;
        if (k > n - k) k = n - k;
        for (int i = 0; i < k; ++i) {
            res = (res * (n - i)) / (i + 1);
        }
        return res;
    }
public:
    int sum_Of_product(int n) {
        return (int) C(2 * n, n - 1);
    }
};"""
    },

    556: {
        "starter_code_javascript": "function removezero_ip(ip) {\\n    return '';\\n}",
        "reference_solution_javascript": """function removezero_ip(ip) {
    return ip.replace(/\\\\.[0]*/g, '.');
}""",
        "starter_code_java": "class Solution {\\n    public String removezero_ip(String ip) {\\n        return \\"\\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String removezero_ip(String ip) {
        String[] parts = ip.split("\\\\\\\\.");
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < parts.length; i++) {
            if (i > 0) sb.append(".");
            int j = 0;
            while (j < parts[i].length() - 1 && parts[i].charAt(j) == '0') j++;
            sb.append(parts[i].substring(j));
        }
        return sb.toString();
    }
}""",
        "starter_code_cpp": "#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    string removezero_ip(const string& ip);\\n};",
        "reference_solution_cpp": """#include <string>
#include <sstream>
#include <vector>
using namespace std;
class Solution {
public:
    string removezero_ip(const string& ip) {
        stringstream ss(ip);
        string part;
        string res = "";
        bool first = true;
        while (getline(ss, part, '.')) {
            if (!first) res += ".";
            first = false;
            size_t j = 0;
            while (j + 1 < part.length() && part[j] == '0') j++;
            res += part.substr(j);
        }
        return res;
    }
};"""
    },

    557: {
        "starter_code_javascript": "function diff_even_odd(list1) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function diff_even_odd(list1) {
    let first_even = list1.find(x => x % 2 === 0);
    let first_odd = list1.find(x => x % 2 !== 0);
    if (first_even === undefined) first_even = -1;
    if (first_odd === undefined) first_odd = -1;
    return first_even - first_odd;
}""",
        "starter_code_java": "class Solution {\\n    public int diff_even_odd(int[] list1) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int diff_even_odd(int[] list1) {
        int first_even = -1, first_odd = -1;
        for (int x : list1) {
            if (first_even == -1 && x % 2 == 0) first_even = x;
            if (first_odd == -1 && x % 2 != 0) first_odd = x;
        }
        return first_even - first_odd;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int diff_even_odd(const vector<int>& list1);\\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    int diff_even_odd(const vector<int>& list1) {
        int first_even = -1, first_odd = -1;
        for (int x : list1) {
            if (first_even == -1 && x % 2 == 0) first_even = x;
            if (first_odd == -1 && x % 2 != 0) first_odd = x;
        }
        return first_even - first_odd;
    }
};"""
    },

    558: {
        "starter_code_javascript": "function min_Swaps(str1, str2) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function min_Swaps(str1, str2) {
    let count = 0;
    for (let i = 0; i < str1.length; i++) if (str1[i] !== str2[i]) count++;
    if (count % 2 === 0) return Math.floor(count / 2);
    return "Not Possible";
}""",
        "starter_code_java": "class Solution {\\n    public Object min_Swaps(String str1, String str2) {\\n        return null;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public Object min_Swaps(String str1, String str2) {
        int count = 0;
        for (int i = 0; i < str1.length(); i++) if (str1.charAt(i) != str2.charAt(i)) count++;
        if (count % 2 == 0) return count / 2;
        return "Not Possible";
    }
}""",
        "starter_code_cpp": "#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    string min_Swaps(const string& str1, const string& str2);\\n};",
        "reference_solution_cpp": """#include <string>
using namespace std;
class Solution {
public:
    string min_Swaps(const string& str1, const string& str2) {
        int count = 0;
        for (size_t i = 0; i < str1.length(); ++i) if (str1[i] != str2[i]) count++;
        if (count % 2 == 0) return to_string(count / 2);
        return "Not Possible";
    }
};"""
    },

    559: {
        "starter_code_javascript": "function find_kth(arr1, arr2, m, n, k) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function find_kth(arr1, arr2, m, n, k) {
    let merged = [];
    let i = 0, j = 0;
    while (i < m && j < n) {
        if (arr1[i] < arr2[j]) merged.push(arr1[i++]);
        else merged.push(arr2[j++]);
    }
    while (i < m) merged.push(arr1[i++]);
    while (j < n) merged.push(arr2[j++]);
    return merged[k - 1];
}""",
        "starter_code_java": "class Solution {\\n    public int find_kth(int[] arr1, int[] arr2, int m, int n, int k) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int find_kth(int[] arr1, int[] arr2, int m, int n, int k) {
        int[] merged = new int[m + n];
        int i = 0, j = 0, d = 0;
        while (i < m && j < n) {
            if (arr1[i] < arr2[j]) merged[d++] = arr1[i++];
            else merged[d++] = arr2[j++];
        }
        while (i < m) merged[d++] = arr1[i++];
        while (j < n) merged[d++] = arr2[j++];
        return merged[k - 1];
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int find_kth(const vector<int>& arr1, const vector<int>& arr2, int m, int n, int k);\\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    int find_kth(const vector<int>& arr1, const vector<int>& arr2, int m, int n, int k) {
        vector<int> merged(m + n);
        int i = 0, j = 0, d = 0;
        while (i < m && j < n) {
            if (arr1[i] < arr2[j]) merged[d++] = arr1[i++];
            else merged[d++] = arr2[j++];
        }
        while (i < m) merged[d++] = arr1[i++];
        while (j < n) merged[d++] = arr2[j++];
        return merged[k - 1];
    }
};"""
    },

    560: {
        "starter_code_javascript": "function armstrong_number(number) {\\n    return false;\\n}",
        "reference_solution_javascript": """function armstrong_number(number) {
    let s = String(number);
    let times = s.length;
    let sum = 0;
    for (let c of s) sum += Math.pow(parseInt(c), times);
    return number === sum;
}""",
        "starter_code_java": "class Solution {\\n    public boolean armstrong_number(int number) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public boolean armstrong_number(int number) {
        String s = String.valueOf(number);
        int times = s.length();
        int sum = 0;
        for (char c : s.toCharArray()) sum += Math.pow(c - '0', times);
        return number == sum;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    bool armstrong_number(int number);\\n};",
        "reference_solution_cpp": """#include <string>
#include <cmath>
using namespace std;
class Solution {
public:
    bool armstrong_number(int number) {
        string s = to_string(number);
        int times = s.length();
        int sum = 0;
        for (char c : s) sum += pow(c - '0', times);
        return number == sum;
    }
};"""
    }
}
'''

with open("scripts/batch10_solutions.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Created scripts/batch10_solutions.py successfully!")
