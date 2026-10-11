"""
Curated and specialized solutions for MBPP problems where language idioms
or complex constructs benefit from targeted implementations.
"""

SPECIAL_MBPP_SOLUTIONS = {
    41: {
        "starter_code_java": "class Solution {\n    public int min_cost(int[][] cost, int m, int n) {\n        return 0;\n    }\n}",
        "reference_solution_java": """class Solution {
    public int min_cost(int[][] cost, int m, int n) {
        int[][] tc = new int[m + 1][n + 1];
        tc[0][0] = cost[0][0];
        for (int i = 1; i <= m; i++) tc[i][0] = tc[i - 1][0] + cost[i][0];
        for (int j = 1; j <= n; j++) tc[0][j] = tc[0][j - 1] + cost[0][j];
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                tc[i][j] = Math.min(tc[i - 1][j - 1], Math.min(tc[i - 1][j], tc[i][j - 1])) + cost[i][j];
            }
        }
        return tc[m][n];
    }
}""",
        "starter_code_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    int min_cost(const vector<vector<int>>& cost, int m, int n) {\n        return 0;\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    int min_cost(const vector<vector<int>>& cost, int m, int n) {
        vector<vector<int>> tc(m + 1, vector<int>(n + 1, 0));
        tc[0][0] = cost[0][0];
        for (int i = 1; i <= m; i++) tc[i][0] = tc[i - 1][0] + cost[i][0];
        for (int j = 1; j <= n; j++) tc[0][j] = tc[0][j - 1] + cost[0][j];
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                tc[i][j] = min({tc[i - 1][j - 1], tc[i - 1][j], tc[i][j - 1]}) + cost[i][j];
            }
        }
        return tc[m][n];
    }
};""",
        "starter_code_javascript": "function min_cost(cost, m, n) {\n    return 0;\n}",
        "reference_solution_javascript": """function min_cost(cost, m, n) {
    const tc = Array.from({length: m + 1}, () => new Array(n + 1).fill(0));
    tc[0][0] = cost[0][0];
    for (let i = 1; i <= m; i++) tc[i][0] = tc[i - 1][0] + cost[i][0];
    for (let j = 1; j <= n; j++) tc[0][j] = tc[0][j - 1] + cost[0][j];
    for (let i = 1; i <= m; i++) {
        for (let j = 1; j <= n; j++) {
            tc[i][j] = Math.min(tc[i - 1][j - 1], tc[i - 1][j], tc[i][j - 1]) + cost[i][j];
        }
    }
    return tc[m][n];
}"""
    },
    45: {
        "starter_code_java": "class Solution {\n    public boolean differ_At_One_Bit_Pos(int a, int b) {\n        return false;\n    }\n}",
        "reference_solution_java": """class Solution {
    public boolean differ_At_One_Bit_Pos(int a, int b) {
        int x = a ^ b;
        return x > 0 && ((x & (x - 1)) == 0);
    }
}"""
    },
    47: {
        "starter_code_java": "class Solution {\n    public int[] square_nums(int[] nums) {\n        return new int[]{};\n    }\n}",
        "reference_solution_java": """class Solution {
    public int[] square_nums(int[] nums) {
        int[] res = new int[nums.length];
        for (int i = 0; i < nums.length; i++) res[i] = nums[i] * nums[i];
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    vector<int> square_nums(const vector<int>& nums) {\n        return {};\n    }\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    vector<int> square_nums(const vector<int>& nums) {
        vector<int> res;
        for (int x : nums) res.push_back(x * x);
        return res;
    }
};""",
        "starter_code_javascript": "function square_nums(nums) {\n    return [];\n}",
        "reference_solution_javascript": """function square_nums(nums) {
    return nums.map(x => x * x);
}"""
    },
    50: {
        "starter_code_java": "class Solution {\n    public String remove_Occ(String s, String ch) {\n        return \"\";\n    }\n}",
        "reference_solution_java": """class Solution {
    public String remove_Occ(String s, String ch) {
        int first = s.indexOf(ch);
        if (first != -1) s = s.substring(0, first) + s.substring(first + ch.length());
        int last = s.lastIndexOf(ch);
        if (last != -1) s = s.substring(0, last) + s.substring(last + ch.length());
        return s;
    }
}""",
        "starter_code_cpp": "#include <string>\nusing namespace std;\nclass Solution {\npublic:\n    string remove_Occ(string s, const string& ch) {\n        return \"\";\n    }\n};",
        "reference_solution_cpp": """#include <string>
using namespace std;
class Solution {
public:
    string remove_Occ(string s, const string& ch) {
        auto first = s.find(ch);
        if (first != string::npos) s.erase(first, ch.length());
        auto last = s.rfind(ch);
        if (last != string::npos) s.erase(last, ch.length());
        return s;
    }
};""",
        "starter_code_javascript": "function remove_Occ(s, ch) {\n    return \"\";\n}",
        "reference_solution_javascript": """function remove_Occ(s, ch) {
    const first = s.indexOf(ch);
    if (first !== -1) s = s.slice(0, first) + s.slice(first + ch.length);
    const last = s.lastIndexOf(ch);
    if (last !== -1) s = s.slice(0, last) + s.slice(last + ch.length);
    return s;
}"""
    },
    51: {
        "starter_code_java": "class Solution {\n    public int[][] sort_matrix(int[][] M) {\n        return new int[][]{};\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[][] sort_matrix(int[][] M) {
        int[][] res = M.clone();
        Arrays.sort(res, (a, b) -> {
            int sa = 0, sb = 0;
            for (int x : a) sa += x;
            for (int x : b) sb += x;
            return Integer.compare(sa, sb);
        });
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    vector<vector<int>> sort_matrix(vector<vector<int>> M) {\n        return {};\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <numeric>
#include <algorithm>
using namespace std;
class Solution {
public:
    vector<vector<int>> sort_matrix(vector<vector<int>> M) {
        sort(M.begin(), M.end(), [](const vector<int>& a, const vector<int>& b) {
            int sa = 0, sb = 0;
            for (int x : a) sa += x;
            for (int x : b) sb += x;
            return sa < sb;
        });
        return M;
    }
};"""
    },
    56: {
        "starter_code_java": "class Solution {\n    public String remove_dirty_chars(String string, String second_string) {\n        return \"\";\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public String remove_dirty_chars(String string, String second_string) {
        StringBuilder sb = new StringBuilder();
        Set<Character> set = new HashSet<>();
        for (char c : second_string.toCharArray()) set.add(c);
        for (char c : string.toCharArray()) {
            if (!set.contains(c)) sb.append(c);
        }
        return sb.toString();
    }
}""",
        "starter_code_cpp": "#include <string>\nusing namespace std;\nclass Solution {\npublic:\n    string remove_dirty_chars(const string& str, const string& second_string) {\n        return \"\";\n    }\n};",
        "reference_solution_cpp": """#include <string>
#include <unordered_set>
using namespace std;
class Solution {
public:
    string remove_dirty_chars(const string& str, const string& second_string) {
        unordered_set<char> s(second_string.begin(), second_string.end());
        string res = "";
        for (char c : str) {
            if (!s.count(c)) res += c;
        }
        return res;
    }
};"""
    },
    57: {
        "starter_code_java": "class Solution {\n    public boolean test_duplicate(int[] arraynums) {\n        return false;\n    }\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public boolean test_duplicate(int[] arraynums) {
        Set<Integer> set = new HashSet<>();
        for (int x : arraynums) {
            if (set.contains(x)) return true;
            set.add(x);
        }
        return false;
    }
}""",
        "starter_code_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    bool test_duplicate(const vector<int>& arraynums) {\n        return false;\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <unordered_set>
using namespace std;
class Solution {
public:
    bool test_duplicate(const vector<int>& arraynums) {
        unordered_set<int> s;
        for (int x : arraynums) {
            if (s.count(x)) return true;
            s.insert(x);
        }
        return false;
    }
};"""
    },
    59: {
        "starter_code_java": "class Solution {\n    public int[] multiples_of_num(int m, int n) {\n        return new int[]{};\n    }\n}",
        "reference_solution_java": """class Solution {
    public int[] multiples_of_num(int m, int n) {
        int[] res = new int[m];
        for (int i = 0; i < m; i++) res[i] = (i + 1) * n;
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    vector<int> multiples_of_num(int m, int n) {\n        return {};\n    }\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    vector<int> multiples_of_num(int m, int n) {
        vector<int> res(m);
        for (int i = 0; i < m; i++) res[i] = (i + 1) * n;
        return res;
    }
};"""
    },
    60: {
        "starter_code_cpp": "#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    int find_first_duplicate(const vector<int>& nums) {\n        return -1;\n    }\n};",
        "reference_solution_cpp": """#include <vector>
#include <unordered_set>
using namespace std;
class Solution {
public:
    int find_first_duplicate(const vector<int>& nums) {
        unordered_set<int> s;
        for (int x : nums) {
            if (s.count(x)) return x;
            s.insert(x);
        }
        return -1;
    }
};"""
    }
}

try:
    from scripts.batch1_solutions import BATCH1_SOLUTIONS
    SPECIAL_MBPP_SOLUTIONS.update(BATCH1_SOLUTIONS)
except ImportError:
    pass

try:
    from scripts.batch2_solutions import BATCH2_SOLUTIONS
    SPECIAL_MBPP_SOLUTIONS.update(BATCH2_SOLUTIONS)
except ImportError:
    pass

try:
    from scripts.batch3_solutions import BATCH3_SOLUTIONS
    SPECIAL_MBPP_SOLUTIONS.update(BATCH3_SOLUTIONS)
except ImportError:
    pass

try:
    from scripts.batch4_solutions import BATCH4_SOLUTIONS
    SPECIAL_MBPP_SOLUTIONS.update(BATCH4_SOLUTIONS)
except ImportError:
    pass

try:
    from scripts.batch5_solutions import BATCH5_SOLUTIONS
    SPECIAL_MBPP_SOLUTIONS.update(BATCH5_SOLUTIONS)
except ImportError:
    pass

for b_idx in range(6, 18):
    try:
        mod = __import__(f"scripts.batch{b_idx}_solutions", fromlist=[f"BATCH{b_idx}_SOLUTIONS"])
        SPECIAL_MBPP_SOLUTIONS.update(getattr(mod, f"BATCH{b_idx}_SOLUTIONS"))
    except ImportError:
        pass



