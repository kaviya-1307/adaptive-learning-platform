import os

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "batch16_solutions.py")

solutions_code = '''"""
Curated and specialized solutions for MBPP problems (Batch 16: 811-860).
"""

BATCH16_SOLUTIONS = {
    811: {
        "starter_code_javascript": "function check_tuples(test_tuple, K) {\\n    return false;\\n}",
        "reference_solution_javascript": """function check_tuples(test_tuple, K) {
    const set = new Set(K);
    return test_tuple.every(x => set.has(x));
}""",
        "starter_code_java": "class Solution {\\n    public boolean check_tuples(int[] test_tuple, int[] K) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public boolean check_tuples(int[] test_tuple, int[] K) {
        Set<Integer> set = new HashSet<>();
        for (int x : K) set.add(x);
        for (int x : test_tuple) if (!set.contains(x)) return false;
        return true;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    bool check_tuples(std::vector<int> test_tuple, std::vector<int> K);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <unordered_set>
class Solution {
public:
    bool check_tuples(std::vector<int> test_tuple, std::vector<int> K) {
        std::unordered_set<int> s(K.begin(), K.end());
        for (int x : test_tuple) if (s.find(x) == s.end()) return false;
        return true;
    }
};"""
    },

    812: {
        "starter_code_javascript": "function text_match(text) {\\n    return '';\\n}",
        "reference_solution_javascript": """function text_match(text) {
    return /a.*b$/.test(text) ? "Found a match!" : "Not matched!";
}""",
        "starter_code_java": "class Solution {\\n    public String text_match(String text) {\\n        return \"\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String text_match(String text) {
        return text.matches(".*a.*b") ? "Found a match!" : "Not matched!";
    }
}""",
        "starter_code_cpp": "#include <string>\\nclass Solution {\\npublic:\\n    std::string text_match(std::string text);\\n};",
        "reference_solution_cpp": """#include <string>
class Solution {
public:
    std::string text_match(std::string text) {
        size_t pos = text.find('a');
        if (pos != std::string::npos && !text.empty() && text.back() == 'b') {
            return "Found a match!";
        }
        return "Not matched!";
    }
};"""
    },

    813: {
        "starter_code_javascript": "function Check_Solution(a, b, c) {\\n    return '';\\n}",
        "reference_solution_javascript": """function Check_Solution(a, b, c) {
    let d = b * b - 4 * a * c;
    if (d > 0) return "2 solutions";
    else if (d === 0) return "1 solution";
    else return "No solutions";
}""",
        "starter_code_java": "class Solution {\\n    public String Check_Solution(int a, int b, int c) {\\n        return \"\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String Check_Solution(int a, int b, int c) {
        long d = (long) b * b - 4L * a * c;
        if (d > 0) return "2 solutions";
        else if (d == 0) return "1 solution";
        else return "No solutions";
    }
}""",
        "starter_code_cpp": "#include <string>\\nclass Solution {\\npublic:\\n    std::string Check_Solution(int a, int b, int c);\\n};",
        "reference_solution_cpp": """#include <string>
class Solution {
public:
    std::string Check_Solution(int a, int b, int c) {
        long long d = 1LL * b * b - 4LL * a * c;
        if (d > 0) return "2 solutions";
        else if (d == 0) return "1 solution";
        else return "No solutions";
    }
};"""
    },

    814: {
        "starter_code_javascript": "function sum_even_odd(list1) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function sum_even_odd(list1) {
    let fe = -1, fo = -1;
    for (let x of list1) {
        if (x % 2 === 0 && fe === -1) fe = x;
        if (x % 2 !== 0 && fo === -1) fo = x;
    }
    return fe + fo;
}""",
        "starter_code_java": "class Solution {\\n    public int sum_even_odd(int[] list1) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int sum_even_odd(int[] list1) {
        int fe = -1, fo = -1;
        for (int x : list1) {
            if (x % 2 == 0 && fe == -1) fe = x;
            if (x % 2 != 0 && fo == -1) fo = x;
        }
        return fe + fo;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    int sum_even_odd(std::vector<int> list1);\\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    int sum_even_odd(std::vector<int> list1) {
        int fe = -1, fo = -1;
        for (int x : list1) {
            if (x % 2 == 0 && fe == -1) fe = x;
            if (x % 2 != 0 && fo == -1) fo = x;
        }
        return fe + fo;
    }
};"""
    },

    815: {
        "starter_code_javascript": "function parallelogram_perimeter(b, h) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function parallelogram_perimeter(b, h) {
    return 2 * (b * h);
}""",
        "starter_code_java": "class Solution {\\n    public int parallelogram_perimeter(int b, int h) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int parallelogram_perimeter(int b, int h) {
        return 2 * (b * h);
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int parallelogram_perimeter(int b, int h);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    int parallelogram_perimeter(int b, int h) {
        return 2 * (b * h);
    }
};"""
    },

    816: {
        "starter_code_javascript": "function div_of_nums(nums, m, n) {\\n    return [];\\n}",
        "reference_solution_javascript": """function div_of_nums(nums, m, n) {
    return nums.filter(x => (x % m === 0 && x % n === 0));
}""",
        "starter_code_java": "class Solution {\\n    public int[] div_of_nums(int[] nums, int m, int n) {\\n        return new int[0];\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[] div_of_nums(int[] nums, int m, int n) {
        List<Integer> list = new ArrayList<>();
        for (int x : nums) {
            if (x % m == 0 && x % n == 0) list.add(x);
        }
        int[] res = new int[list.size()];
        for (int i = 0; i < list.size(); i++) res[i] = list.get(i);
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    std::vector<int> div_of_nums(std::vector<int> nums, int m, int n);\\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    std::vector<int> div_of_nums(std::vector<int> nums, int m, int n) {
        std::vector<int> res;
        for (int x : nums) {
            if (x % m == 0 && x % n == 0) res.push_back(x);
        }
        return res;
    }
};"""
    },

    817: {
        "starter_code_javascript": "function all_Bits_Set_In_The_Given_Range(n, l, r) {\\n    return false;\\n}",
        "reference_solution_javascript": """function all_Bits_Set_In_The_Given_Range(n, l, r) {
    let num = ((1 << r) - 1) ^ ((1 << (l - 1)) - 1);
    let new_num = n & num;
    return num === new_num;
}""",
        "starter_code_java": "class Solution {\\n    public boolean all_Bits_Set_In_The_Given_Range(int n, int l, int r) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public boolean all_Bits_Set_In_The_Given_Range(int n, int l, int r) {
        int num = ((1 << r) - 1) ^ ((1 << (l - 1)) - 1);
        int new_num = n & num;
        return num == new_num;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    bool all_Bits_Set_In_The_Given_Range(int n, int l, int r);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    bool all_Bits_Set_In_The_Given_Range(int n, int l, int r) {
        int num = ((1 << r) - 1) ^ ((1 << (l - 1)) - 1);
        int new_num = n & num;
        return num == new_num;
    }
};"""
    },

    818: {
        "starter_code_javascript": "function is_Isomorphic(str1, str2) {\\n    return false;\\n}",
        "reference_solution_javascript": """function is_Isomorphic(str1, str2) {
    if (str1.length !== str2.length) return false;
    const m1 = {}, m2 = {};
    for (let i = 0; i < str1.length; i++) {
        let c1 = str1[i], c2 = str2[i];
        if (m1[c1] !== undefined && m1[c1] !== c2) return false;
        if (m2[c2] !== undefined && m2[c2] !== c1) return false;
        m1[c1] = c2;
        m2[c2] = c1;
    }
    return true;
}""",
        "starter_code_java": "class Solution {\\n    public boolean is_Isomorphic(String str1, String str2) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public boolean is_Isomorphic(String str1, String str2) {
        if (str1.length() != str2.length()) return false;
        Map<Character, Character> m1 = new HashMap<>();
        Map<Character, Character> m2 = new HashMap<>();
        for (int i = 0; i < str1.length(); i++) {
            char c1 = str1.charAt(i), c2 = str2.charAt(i);
            if (m1.containsKey(c1) && m1.get(c1) != c2) return false;
            if (m2.containsKey(c2) && m2.get(c2) != c1) return false;
            m1.put(c1, c2);
            m2.put(c2, c1);
        }
        return true;
    }
}""",
        "starter_code_cpp": "#include <string>\\nclass Solution {\\npublic:\\n    bool is_Isomorphic(std::string str1, std::string str2);\\n};",
        "reference_solution_cpp": """#include <string>
#include <unordered_map>
class Solution {
public:
    bool is_Isomorphic(std::string str1, std::string str2) {
        if (str1.size() != str2.size()) return false;
        std::unordered_map<char, char> m1, m2;
        for (size_t i = 0; i < str1.size(); i++) {
            char c1 = str1[i], c2 = str2[i];
            if (m1.count(c1) && m1[c1] != c2) return false;
            if (m2.count(c2) && m2[c2] != c1) return false;
            m1[c1] = c2;
            m2[c2] = c1;
        }
        return true;
    }
};"""
    },

    819: {
        "starter_code_javascript": "function sum_num(numbers) {\\n    return 0.0;\\n}",
        "reference_solution_javascript": """function sum_num(numbers) {
    let total = 0;
    for (let x of numbers) total += x;
    return total / numbers.length;
}""",
        "starter_code_java": "class Solution {\\n    public double sum_num(int[] numbers) {\\n        return 0.0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public double sum_num(int[] numbers) {
        double total = 0;
        for (int x : numbers) total += x;
        return total / numbers.length;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    double sum_num(std::vector<int> numbers);\\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    double sum_num(std::vector<int> numbers) {
        double total = 0;
        for (int x : numbers) total += x;
        return total / numbers.size();
    }
};"""
    },

    820: {
        "starter_code_javascript": "function is_odd(n) {\\n    return false;\\n}",
        "reference_solution_javascript": """function is_odd(n) {
    return (n ^ 1) === (n - 1);
}""",
        "starter_code_java": "class Solution {\\n    public boolean is_odd(int n) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public boolean is_odd(int n) {
        return (n ^ 1) == (n - 1);
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    bool is_odd(int n);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    bool is_odd(int n) {
        return (n ^ 1) == (n - 1);
    }
};"""
    },

    821: {
        "starter_code_javascript": "function reverse_list_lists(lists) {\\n    return [];\\n}",
        "reference_solution_javascript": """function reverse_list_lists(lists) {
    return lists.map(row => [...row].sort((a, b) => b - a));
}""",
        "starter_code_java": "class Solution {\\n    public int[][] reverse_list_lists(int[][] lists) {\\n        return new int[0][0];\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[][] reverse_list_lists(int[][] lists) {
        int[][] res = new int[lists.length][];
        for (int i = 0; i < lists.length; i++) {
            res[i] = new int[lists[i].length];
            Integer[] temp = new Integer[lists[i].length];
            for (int j = 0; j < lists[i].length; j++) temp[j] = lists[i][j];
            Arrays.sort(temp, Collections.reverseOrder());
            for (int j = 0; j < lists[i].length; j++) res[i][j] = temp[j];
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    std::vector<std::vector<int>> reverse_list_lists(std::vector<std::vector<int>> lists);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
class Solution {
public:
    std::vector<std::vector<int>> reverse_list_lists(std::vector<std::vector<int>> lists) {
        for (auto& row : lists) {
            std::sort(row.rbegin(), row.rend());
        }
        return lists;
    }
};"""
    },

    822: {
        "starter_code_javascript": "function find_Extra(arr1, arr2, n) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function find_Extra(arr1, arr2, n) {
    for (let i = 0; i < n; i++) {
        if (arr1[i] !== arr2[i]) return i;
    }
    return n;
}""",
        "starter_code_java": "class Solution {\\n    public int find_Extra(int[] arr1, int[] arr2, int n) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int find_Extra(int[] arr1, int[] arr2, int n) {
        for (int i = 0; i < n; i++) {
            if (arr1[i] != arr2[i]) return i;
        }
        return n;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    int find_Extra(std::vector<int> arr1, std::vector<int> arr2, int n);\\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    int find_Extra(std::vector<int> arr1, std::vector<int> arr2, int n) {
        for (int i = 0; i < n; i++) {
            if (arr1[i] != arr2[i]) return i;
        }
        return n;
    }
};"""
    },

    823: {
        "starter_code_javascript": "function same_Length(A, B) {\\n    return false;\\n}",
        "reference_solution_javascript": """function same_Length(A, B) {
    return String(Math.abs(A)).length === String(Math.abs(B)).length;
}""",
        "starter_code_java": "class Solution {\\n    public boolean same_Length(int A, int B) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public boolean same_Length(int A, int B) {
        while (A > 0 && B > 0) {
            A /= 10;
            B /= 10;
        }
        return (A == 0 && B == 0);
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    bool same_Length(int A, int B);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    bool same_Length(int A, int B) {
        while (A > 0 && B > 0) {
            A /= 10;
            B /= 10;
        }
        return (A == 0 && B == 0);
    }
};"""
    },

    824: {
        "starter_code_javascript": "function remove_spaces(text) {\\n    return '';\\n}",
        "reference_solution_javascript": """function remove_spaces(text) {
    return text.replace(/ +/g, ' ');
}""",
        "starter_code_java": "class Solution {\\n    public String remove_spaces(String text) {\\n        return \"\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String remove_spaces(String text) {
        return text.replaceAll(" +", " ");
    }
}""",
        "starter_code_cpp": "#include <string>\\nclass Solution {\\npublic:\\n    std::string remove_spaces(std::string text);\\n};",
        "reference_solution_cpp": """#include <string>
class Solution {
public:
    std::string remove_spaces(std::string text) {
        std::string res = "";
        bool prev_space = false;
        for (char c : text) {
            if (c == ' ') {
                if (!prev_space) res += c;
                prev_space = true;
            } else {
                res += c;
                prev_space = false;
            }
        }
        return res;
    }
};"""
    },

    825: {
        "starter_code_javascript": "function Extract(lst) {\\n    return [];\\n}",
        "reference_solution_javascript": """function Extract(lst) {
    return lst.map(item => item[item.length - 1]);
}""",
        "starter_code_java": "class Solution {\\n    public int[] Extract(int[][] lst) {\\n        return new int[0];\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int[] Extract(int[][] lst) {
        int[] res = new int[lst.length];
        for (int i = 0; i < lst.length; i++) res[i] = lst[i][lst[i].length - 1];
        return res;
    }
    public String[] Extract(char[][] lst) {
        String[] res = new String[lst.length];
        for (int i = 0; i < lst.length; i++) res[i] = String.valueOf(lst[i][lst[i].length - 1]);
        return res;
    }
    public String[] Extract(String[][] lst) {
        String[] res = new String[lst.length];
        for (int i = 0; i < lst.length; i++) res[i] = lst[i][lst[i].length - 1];
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    std::vector<int> Extract(std::vector<std::vector<int>> lst);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
class Solution {
public:
    std::vector<int> Extract(const std::vector<std::vector<int>>& lst) {
        std::vector<int> res;
        for (const auto& row : lst) res.push_back(row.back());
        return res;
    }
    std::vector<std::string> Extract(const std::vector<std::vector<char>>& lst) {
        std::vector<std::string> res;
        for (const auto& row : lst) res.push_back(std::string(1, row.back()));
        return res;
    }
    std::vector<std::string> Extract(const std::vector<std::vector<std::string>>& lst) {
        std::vector<std::string> res;
        for (const auto& row : lst) res.push_back(row.back());
        return res;
    }
};"""
    },

    826: {
        "starter_code_javascript": "function max_sum_subseq(A) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function max_sum_subseq(A) {
    let n = A.length;
    if (n === 1) return A[0];
    let dp = new Array(n);
    dp[0] = A[0];
    dp[1] = Math.max(A[0], A[1]);
    for (let i = 2; i < n; i++) {
        dp[i] = Math.max(dp[i - 1], dp[i - 2] + A[i], A[i]);
    }
    return dp[n - 1];
}""",
        "starter_code_java": "class Solution {\\n    public int max_sum_subseq(int[] A) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int max_sum_subseq(int[] A) {
        int n = A.length;
        if (n == 1) return A[0];
        int[] dp = new int[n];
        dp[0] = A[0];
        dp[1] = Math.max(A[0], A[1]);
        for (int i = 2; i < n; i++) {
            dp[i] = Math.max(dp[i - 1], Math.max(dp[i - 2] + A[i], A[i]));
        }
        return dp[n - 1];
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    int max_sum_subseq(std::vector<int> A);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
class Solution {
public:
    int max_sum_subseq(std::vector<int> A) {
        int n = A.size();
        if (n == 1) return A[0];
        std::vector<int> dp(n);
        dp[0] = A[0];
        dp[1] = std::max(A[0], A[1]);
        for (int i = 2; i < n; i++) {
            dp[i] = std::max({dp[i - 1], dp[i - 2] + A[i], A[i]});
        }
        return dp[n - 1];
    }
};"""
    },

    827: {
        "starter_code_javascript": "function sort_list_last(tuples) {\\n    return [];\\n}",
        "reference_solution_javascript": """function sort_list_last(tuples) {
    return [...tuples].sort((a, b) => a[a.length - 1] - b[b.length - 1]);
}""",
        "starter_code_java": "class Solution {\\n    public int[][] sort_list_last(int[][] tuples) {\\n        return new int[0][0];\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[][] sort_list_last(int[][] tuples) {
        int[][] res = tuples.clone();
        Arrays.sort(res, (a, b) -> Integer.compare(a[a.length - 1], b[b.length - 1]));
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    std::vector<std::vector<int>> sort_list_last(std::vector<std::vector<int>> tuples);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
class Solution {
public:
    std::vector<std::vector<int>> sort_list_last(std::vector<std::vector<int>> tuples) {
        std::stable_sort(tuples.begin(), tuples.end(), [](const std::vector<int>& a, const std::vector<int>& b) {
            return a.back() < b.back();
        });
        return tuples;
    }
};"""
    },

    828: {
        "starter_code_javascript": "function is_Word_Present(sentence, word) {\\n    return false;\\n}",
        "reference_solution_javascript": """function is_Word_Present(sentence, word) {
    return sentence.split(" ").includes(word);
}""",
        "starter_code_java": "class Solution {\\n    public boolean is_Word_Present(String sentence, String word) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public boolean is_Word_Present(String sentence, String word) {
        for (String w : sentence.split(" ")) {
            if (w.equals(word)) return true;
        }
        return false;
    }
}""",
        "starter_code_cpp": "#include <string>\\nclass Solution {\\npublic:\\n    bool is_Word_Present(std::string sentence, std::string word);\\n};",
        "reference_solution_cpp": """#include <string>
#include <sstream>
class Solution {
public:
    bool is_Word_Present(std::string sentence, std::string word) {
        std::stringstream ss(sentence);
        std::string w;
        while (ss >> w) {
            if (w == word) return true;
        }
        return false;
    }
};"""
    },

    829: {
        "starter_code_javascript": "function extract_elements(numbers, n) {\\n    return [];\\n}",
        "reference_solution_javascript": """function extract_elements(numbers, n) {
    let res = [];
    let i = 0;
    while (i < numbers.length) {
        let j = i;
        while (j < numbers.length && numbers[j] === numbers[i]) j++;
        if (j - i === n) res.push(numbers[i]);
        i = j;
    }
    return res;
}""",
        "starter_code_java": "class Solution {\\n    public int[] extract_elements(int[] numbers, int n) {\\n        return new int[0];\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[] extract_elements(int[] numbers, int n) {
        List<Integer> list = new ArrayList<>();
        int i = 0;
        while (i < numbers.length) {
            int j = i;
            while (j < numbers.length && numbers[j] == numbers[i]) j++;
            if (j - i == n) list.add(numbers[i]);
            i = j;
        }
        int[] res = new int[list.size()];
        for (int k = 0; k < list.size(); k++) res[k] = list.get(k);
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    std::vector<int> extract_elements(std::vector<int> numbers, int n);\\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    std::vector<int> extract_elements(std::vector<int> numbers, int n) {
        std::vector<int> res;
        size_t i = 0;
        while (i < numbers.size()) {
            size_t j = i;
            while (j < numbers.size() && numbers[j] == numbers[i]) j++;
            if (j - i == static_cast<size_t>(n)) res.push_back(numbers[i]);
            i = j;
        }
        return res;
    }
};"""
    },

    830: {
        "starter_code_javascript": "function check(arr, n) {\\n    return false;\\n}",
        "reference_solution_javascript": """function check(arr, n) {
    let g = 0;
    for (let i = 1; i < n; i++) {
        if (arr[i] - arr[i - 1] > 0 && g === 1) return false;
        if (arr[i] - arr[i] < 0) g = 1;
    }
    return true;
}""",
        "starter_code_java": "class Solution {\\n    public boolean check(int[] arr, int n) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public boolean check(int[] arr, int n) {
        int g = 0;
        for (int i = 1; i < n; i++) {
            if (arr[i] - arr[i - 1] > 0 && g == 1) return false;
            if (arr[i] - arr[i] < 0) g = 1;
        }
        return true;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    bool check(std::vector<int> arr, int n);\\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    bool check(std::vector<int> arr, int n) {
        int g = 0;
        for (int i = 1; i < n; i++) {
            if (arr[i] - arr[i - 1] > 0 && g == 1) return false;
            if (arr[i] - arr[i] < 0) g = 1;
        }
        return true;
    }
};"""
    },

    831: {
        "starter_code_javascript": "function match_num(string) {\\n    return false;\\n}",
        "reference_solution_javascript": """function match_num(string) {
    return string.startsWith('5');
}""",
        "starter_code_java": "class Solution {\\n    public boolean match_num(String string) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public boolean match_num(String string) {
        return string.startsWith("5");
    }
}""",
        "starter_code_cpp": "#include <string>\\nclass Solution {\\npublic:\\n    bool match_num(std::string string);\\n};",
        "reference_solution_cpp": """#include <string>
class Solution {
public:
    bool match_num(std::string str) {
        return !str.empty() && str[0] == '5';
    }
};"""
    },

    832: {
        "starter_code_javascript": "function smallest_multiple(n) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function smallest_multiple(n) {
    function gcd(a, b) { while (b) { let t = b; b = a % b; a = t; } return a; }
    function lcm(a, b) { return (a * b) / gcd(a, b); }
    let ans = 1;
    for (let i = 1; i <= n; i++) ans = lcm(ans, i);
    return ans;
}""",
        "starter_code_java": "class Solution {\\n    public int smallest_multiple(int n) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    private long gcd(long a, long b) {
        while (b != 0) { long t = b; b = a % b; a = t; }
        return a;
    }
    public int smallest_multiple(int n) {
        long ans = 1;
        for (int i = 1; i <= n; i++) {
            ans = (ans * i) / gcd(ans, i);
        }
        return (int) ans;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int smallest_multiple(int n);\\n};",
        "reference_solution_cpp": """#include <numeric>
class Solution {
    long long gcd(long long a, long long b) {
        while (b) { long long t = b; b = a % b; a = t; }
        return a;
    }
public:
    int smallest_multiple(int n) {
        long long ans = 1;
        for (int i = 1; i <= n; i++) {
            ans = (ans * i) / gcd(ans, i);
        }
        return (int) ans;
    }
};"""
    },

    833: {
        "starter_code_javascript": "function add_dict(d1, d2) {\\n    return {};\\n}",
        "reference_solution_javascript": """function add_dict(d1, d2) {
    const res = Object.assign({}, d1);
    for (let k in d2) {
        res[k] = (res[k] || 0) + d2[k];
    }
    return res;
}""",
        "starter_code_java": "import java.util.Map;\\nclass Solution {\\n    public Map<Object, Object> add_dict(Map<Object, Object> d1, Map<Object, Object> d2) {\\n        return null;\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public Map<Object, Object> add_dict(Map<Object, Object> d1, Map<Object, Object> d2) {
        Map<Object, Object> res = new HashMap<>(d1);
        for (Map.Entry<Object, Object> e : d2.entrySet()) {
            Number val2 = (Number) e.getValue();
            if (res.containsKey(e.getKey())) {
                Number val1 = (Number) res.get(e.getKey());
                res.put(e.getKey(), val1.intValue() + val2.intValue());
            } else {
                res.put(e.getKey(), val2.intValue());
            }
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <unordered_map>\\n#include <string>\\nclass Solution {\\npublic:\\n    std::unordered_map<std::string, int> add_dict(std::unordered_map<std::string, int> d1, std::unordered_map<std::string, int> d2);\\n};",
        "reference_solution_cpp": """#include <unordered_map>
#include <string>
class Solution {
public:
    std::unordered_map<std::string, int> add_dict(std::unordered_map<std::string, int> d1, std::unordered_map<std::string, int> d2) {
        std::unordered_map<std::string, int> res = d1;
        for (auto& p : d2) {
            res[p.first] += p.second;
        }
        return res;
    }
};"""
    },

    834: {
        "starter_code_javascript": "function count_Unset_Bits(n) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function count_Unset_Bits(n) {
    let cnt = 0;
    for (let i = 1; i <= n; i++) {
        let temp = i;
        while (temp > 0) {
            if (temp % 2 === 0) cnt++;
            temp = Math.floor(temp / 2);
        }
    }
    return cnt;
}""",
        "starter_code_java": "class Solution {\\n    public int count_Unset_Bits(int n) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int count_Unset_Bits(int n) {
        int cnt = 0;
        for (int i = 1; i <= n; i++) {
            int temp = i;
            while (temp > 0) {
                if (temp % 2 == 0) cnt++;
                temp /= 2;
            }
        }
        return cnt;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int count_Unset_Bits(int n);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    int count_Unset_Bits(int n) {
        int cnt = 0;
        for (int i = 1; i <= n; i++) {
            int temp = i;
            while (temp > 0) {
                if (temp % 2 == 0) cnt++;
                temp /= 2;
            }
        }
        return cnt;
    }
};"""
    },

    835: {
        "starter_code_javascript": "function even_num(x) {\\n    return false;\\n}",
        "reference_solution_javascript": """function even_num(x) {
    return x % 2 === 0;
}""",
        "starter_code_java": "class Solution {\\n    public boolean even_num(double x) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public boolean even_num(double x) {
        return x % 2 == 0;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    bool even_num(double x);\\n};",
        "reference_solution_cpp": """#include <cmath>
class Solution {
public:
    bool even_num(double x) {
        return std::fmod(x, 2.0) == 0.0;
    }
};"""
    },

    836: {
        "starter_code_javascript": "function sum_of_square(n) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function sum_of_square(n) {
    let res = 1;
    for (let i = 1; i <= n; i++) {
        res = Math.round(res * (n + i) / i);
    }
    return res;
}""",
        "starter_code_java": "class Solution {\\n    public int sum_of_square(int n) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int sum_of_square(int n) {
        long res = 1;
        for (int i = 1; i <= n; i++) {
            res = res * (n + i) / i;
        }
        return (int) res;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int sum_of_square(int n);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    int sum_of_square(int n) {
        long long res = 1;
        for (int i = 1; i <= n; i++) {
            res = res * (n + i) / i;
        }
        return (int) res;
    }
};"""
    },

    837: {
        "starter_code_javascript": "function lucky_num(n) {\\n    return [];\\n}",
        "reference_solution_javascript": """function lucky_num(n) {
    let list = [];
    for (let i = 1; i < n * n + 9; i += 2) list.push(i);
    let idx = 1;
    while (idx < list.length) {
        let step = list[idx];
        if (step > list.length) break;
        let nextList = [];
        for (let i = 0; i < list.length; i++) {
            if ((i + 1) % step !== 0) nextList.push(list[i]);
        }
        list = nextList;
        idx++;
    }
    return list.slice(0, n);
}""",
        "starter_code_java": "class Solution {\\n    public int[] lucky_num(int n) {\\n        return new int[0];\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[] lucky_num(int n) {
        List<Integer> list = new ArrayList<>();
        for (int i = 1; i < n * n + 9; i += 2) list.add(i);
        int idx = 1;
        while (idx < list.size()) {
            int step = list.get(idx);
            if (step > list.size()) break;
            List<Integer> nextList = new ArrayList<>();
            for (int i = 0; i < list.size(); i++) {
                if ((i + 1) % step != 0) nextList.add(list.get(i));
            }
            list = nextList;
            idx++;
        }
        int[] res = new int[n];
        for (int i = 0; i < n; i++) res[i] = list.get(i);
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    std::vector<int> lucky_num(int n);\\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    std::vector<int> lucky_num(int n) {
        std::vector<int> list;
        for (int i = 1; i < n * n + 9; i += 2) list.push_back(i);
        size_t idx = 1;
        while (idx < list.size()) {
            int step = list[idx];
            if (step > (int)list.size()) break;
            std::vector<int> nextList;
            for (size_t i = 0; i < list.size(); i++) {
                if ((i + 1) % step != 0) nextList.push_back(list[i]);
            }
            list = nextList;
            idx++;
        }
        list.resize(n);
        return list;
    }
};"""
    },

    838: {
        "starter_code_javascript": "function find_fixed_point(arr, n) {\\n    return -1;\\n}",
        "reference_solution_javascript": """function find_fixed_point(arr, n) {
    for (let i = 0; i < n; i++) {
        if (arr[i] === i) return i;
    }
    return -1;
}""",
        "starter_code_java": "class Solution {\\n    public int find_fixed_point(int[] arr, int n) {\\n        return -1;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int find_fixed_point(int[] arr, int n) {
        for (int i = 0; i < n; i++) {
            if (arr[i] == i) return i;
        }
        return -1;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    int find_fixed_point(std::vector<int> arr, int n);\\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    int find_fixed_point(std::vector<int> arr, int n) {
        for (int i = 0; i < n; i++) {
            if (arr[i] == i) return i;
        }
        return -1;
    }
};"""
    },

    839: {
        "starter_code_javascript": "function previous_palindrome(num) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function previous_palindrome(num) {
    for (let x = num - 1; x > 0; x--) {
        let s = String(x);
        if (s === s.split('').reverse().join('')) return x;
    }
    return 0;
}""",
        "starter_code_java": "class Solution {\\n    public int previous_palindrome(int num) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int previous_palindrome(int num) {
        for (int x = num - 1; x > 0; x--) {
            String s = String.valueOf(x);
            if (s.equals(new StringBuilder(s).reverse().toString())) return x;
        }
        return 0;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int previous_palindrome(int num);\\n};",
        "reference_solution_cpp": """#include <string>
#include <algorithm>
class Solution {
public:
    int previous_palindrome(int num) {
        for (int x = num - 1; x > 0; x--) {
            std::string s = std::to_string(x);
            std::string rev = s;
            std::reverse(rev.begin(), rev.end());
            if (s == rev) return x;
        }
        return 0;
    }
};"""
    },

    840: {
        "starter_code_javascript": "function check_date(m, d, y) {\\n    return false;\\n}",
        "reference_solution_javascript": """function check_date(m, d, y) {
    m = Number(m); d = Number(d); y = Number(y);
    if (m < 1 || m > 12 || d < 1 || d > 31) return false;
    const daysInMonth = [31, (y % 4 === 0 && (y % 100 !== 0 || y % 400 === 0)) ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
    return d <= daysInMonth[m - 1];
}""",
        "starter_code_java": "class Solution {\\n    public boolean check_date(int m, int d, int y) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    private boolean validate(int m, int d, int y) {
        if (m < 1 || m > 12 || d < 1 || d > 31) return false;
        int[] days = {31, (y % 4 == 0 && (y % 100 != 0 || y % 400 == 0)) ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
        return d <= days[m - 1];
    }
    public boolean check_date(int m, int d, int y) {
        return validate(m, d, y);
    }
    public boolean check_date(String m, String d, String y) {
        try {
            return validate(Integer.parseInt(m), Integer.parseInt(d), Integer.parseInt(y));
        } catch (Exception e) {
            return false;
        }
    }
}""",
        "starter_code_cpp": "#include <string>\\nclass Solution {\\npublic:\\n    bool check_date(int m, int d, int y);\\n};",
        "reference_solution_cpp": """#include <string>
class Solution {
    bool validate(int m, int d, int y) {
        if (m < 1 || m > 12 || d < 1 || d > 31) return false;
        int days[] = {31, (y % 4 == 0 && (y % 100 != 0 || y % 400 == 0)) ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
        return d <= days[m - 1];
    }
public:
    bool check_date(int m, int d, int y) {
        return validate(m, d, y);
    }
    bool check_date(std::string m, std::string d, std::string y) {
        try {
            return validate(std::stoi(m), std::stoi(d), std::stoi(y));
        } catch (...) {
            return false;
        }
    }
};"""
    },

    841: {
        "starter_code_javascript": "function maximum_product(nums) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function maximum_product(nums) {
    const s = [...nums].sort((a, b) => a - b);
    const n = s.length;
    return Math.max(s[n - 1] * s[n - 2] * s[n - 3], s[n - 1] * s[0] * s[1]);
}""",
        "starter_code_java": "class Solution {\\n    public int maximum_product(int[] nums) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int maximum_product(int[] nums) {
        int[] s = nums.clone();
        Arrays.sort(s);
        int n = s.length;
        return Math.max(s[n - 1] * s[n - 2] * s[n - 3], s[n - 1] * s[0] * s[1]);
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    int maximum_product(std::vector<int> nums);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
class Solution {
public:
    int maximum_product(std::vector<int> nums) {
        std::sort(nums.begin(), nums.end());
        int n = nums.size();
        return std::max(nums[n - 1] * nums[n - 2] * nums[n - 3], nums[n - 1] * nums[0] * nums[1]);
    }
};"""
    },

    842: {
        "starter_code_javascript": "function end_num(string) {\\n    return false;\\n}",
        "reference_solution_javascript": """function end_num(string) {
    return /[0-9]$/.test(string);
}""",
        "starter_code_java": "class Solution {\\n    public boolean end_num(String string) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public boolean end_num(String string) {
        if (string == null || string.isEmpty()) return false;
        return Character.isDigit(string.charAt(string.length() - 1));
    }
}""",
        "starter_code_cpp": "#include <string>\\nclass Solution {\\npublic:\\n    bool end_num(std::string string);\\n};",
        "reference_solution_cpp": """#include <string>
#include <cctype>
class Solution {
public:
    bool end_num(std::string str) {
        if (str.empty()) return false;
        return std::isdigit(static_cast<unsigned char>(str.back()));
    }
};"""
    },

    843: {
        "starter_code_javascript": "function is_Two_Alter(s) {\\n    return false;\\n}",
        "reference_solution_javascript": """function is_Two_Alter(s) {
    if (s.length < 2) return false;
    for (let i = 0; i < s.length - 2; i++) {
        if (s[i] !== s[i + 2]) return false;
    }
    if (s[0] === s[1]) return false;
    return true;
}""",
        "starter_code_java": "class Solution {\\n    public boolean is_Two_Alter(String s) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public boolean is_Two_Alter(String s) {
        if (s.length() < 2) return false;
        for (int i = 0; i < s.length() - 2; i++) {
            if (s.charAt(i) != s.charAt(i + 2)) return false;
        }
        if (s.charAt(0) == s.charAt(1)) return false;
        return true;
    }
}""",
        "starter_code_cpp": "#include <string>\\nclass Solution {\\npublic:\\n    bool is_Two_Alter(std::string s);\\n};",
        "reference_solution_cpp": """#include <string>
class Solution {
public:
    bool is_Two_Alter(std::string s) {
        if (s.size() < 2) return false;
        for (size_t i = 0; i + 2 < s.size(); i++) {
            if (s[i] != s[i + 2]) return false;
        }
        if (s[0] == s[1]) return false;
        return true;
    }
};"""
    },

    844: {
        "starter_code_javascript": "function rearrange_numbs(array_nums) {\\n    return [];\\n}",
        "reference_solution_javascript": """function rearrange_numbs(array_nums) {
    const key = x => (x === 0 ? 0 : -1 / x);
    return [...array_nums].sort((a, b) => key(a) - key(b));
}""",
        "starter_code_java": "class Solution {\\n    public int[] rearrange_numbs(int[] array_nums) {\\n        return new int[0];\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[] rearrange_numbs(int[] array_nums) {
        Integer[] arr = new Integer[array_nums.length];
        for (int i = 0; i < array_nums.length; i++) arr[i] = array_nums[i];
        Arrays.sort(arr, (a, b) -> {
            double ka = (a == 0) ? 0.0 : -1.0 / a;
            double kb = (b == 0) ? 0.0 : -1.0 / b;
            return Double.compare(ka, kb);
        });
        int[] res = new int[array_nums.length];
        for (int i = 0; i < array_nums.length; i++) res[i] = arr[i];
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    std::vector<int> rearrange_numbs(std::vector<int> array_nums);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
class Solution {
public:
    std::vector<int> rearrange_numbs(std::vector<int> array_nums) {
        std::stable_sort(array_nums.begin(), array_nums.end(), [](int a, int b) {
            double ka = (a == 0) ? 0.0 : -1.0 / a;
            double kb = (b == 0) ? 0.0 : -1.0 / b;
            return ka < kb;
        });
        return array_nums;
    }
};"""
    },

    845: {
        "starter_code_javascript": "function text_uppercase_lowercase(text) {\\n    return '';\\n}",
        "reference_solution_javascript": """function text_uppercase_lowercase(text) {
    return /[A-Z]+[a-z]+$/.test(text) ? "Found a match!" : "Not matched!";
}""",
        "starter_code_java": "class Solution {\\n    public String text_uppercase_lowercase(String text) {\\n        return \"\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String text_uppercase_lowercase(String text) {
        return text.matches(".*[A-Z]+[a-z]+") ? "Found a match!" : "Not matched!";
    }
}""",
        "starter_code_cpp": "#include <string>\\nclass Solution {\\npublic:\\n    std::string text_uppercase_lowercase(std::string text);\\n};",
        "reference_solution_cpp": """#include <string>
#include <cctype>
class Solution {
public:
    std::string text_uppercase_lowercase(std::string text) {
        int i = (int)text.size() - 1;
        int lower_count = 0;
        while (i >= 0 && std::islower(static_cast<unsigned char>(text[i]))) { lower_count++; i--; }
        int upper_count = 0;
        while (i >= 0 && std::isupper(static_cast<unsigned char>(text[i]))) { upper_count++; i--; }
        if (lower_count > 0 && upper_count > 0) return "Found a match!";
        return "Not matched!";
    }
};"""
    },

    846: {
        "starter_code_javascript": "function coin_change(S, m, n) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function coin_change(S, m, n) {
    const dp = new Array(n + 1).fill(0);
    dp[0] = 1;
    for (let i = 0; i < m; i++) {
        for (let j = S[i]; j <= n; j++) {
            dp[j] += dp[j - S[i]];
        }
    }
    return dp[n];
}""",
        "starter_code_java": "class Solution {\\n    public int coin_change(int[] S, int m, int n) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int coin_change(int[] S, int m, int n) {
        int[] dp = new int[n + 1];
        dp[0] = 1;
        for (int i = 0; i < m; i++) {
            for (int j = S[i]; j <= n; j++) {
                dp[j] += dp[j - S[i]];
            }
        }
        return dp[n];
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    int coin_change(std::vector<int> S, int m, int n);\\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    int coin_change(std::vector<int> S, int m, int n) {
        std::vector<int> dp(n + 1, 0);
        dp[0] = 1;
        for (int i = 0; i < m; i++) {
            for (int j = S[i]; j <= n; j++) {
                dp[j] += dp[j - S[i]];
            }
        }
        return dp[n];
    }
};"""
    },

    847: {
        "starter_code_javascript": "function multiply_list(items) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function multiply_list(items) {
    let tot = 1;
    for (let x of items) tot *= x;
    return tot;
}""",
        "starter_code_java": "class Solution {\\n    public int multiply_list(int[] items) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int multiply_list(int[] items) {
        int tot = 1;
        for (int x : items) tot *= x;
        return tot;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    int multiply_list(std::vector<int> items);\\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    int multiply_list(std::vector<int> items) {
        int tot = 1;
        for (int x : items) tot *= x;
        return tot;
    }
};"""
    },

    848: {
        "starter_code_javascript": "function chunk_tuples(test_tup, N) {\\n    return [];\\n}",
        "reference_solution_javascript": """function chunk_tuples(test_tup, N) {
    const res = [];
    for (let i = 0; i < test_tup.length; i += N) {
        res.push(test_tup.slice(i, i + N));
    }
    return res;
}""",
        "starter_code_java": "class Solution {\\n    public int[][] chunk_tuples(int[] test_tup, int N) {\\n        return new int[0][0];\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int[][] chunk_tuples(int[] test_tup, int N) {
        int num_chunks = (test_tup.length + N - 1) / N;
        int[][] res = new int[num_chunks][];
        for (int i = 0; i < num_chunks; i++) {
            int start = i * N;
            int end = Math.min(start + N, test_tup.length);
            res[i] = new int[end - start];
            for (int j = start; j < end; j++) res[i][j - start] = test_tup[j];
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    std::vector<std::vector<int>> chunk_tuples(std::vector<int> test_tup, int N);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
class Solution {
public:
    std::vector<std::vector<int>> chunk_tuples(const std::vector<int>& test_tup, int N) {
        std::vector<std::vector<int>> res;
        for (size_t i = 0; i < test_tup.size(); i += N) {
            size_t end = std::min(test_tup.size(), i + N);
            res.emplace_back(test_tup.begin() + i, test_tup.begin() + end);
        }
        return res;
    }
};"""
    },

    849: {
        "starter_code_javascript": "function super_seq(X, Y, m, n) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function super_seq(X, Y, m, n) {
    const dp = Array.from({ length: m + 1 }, () => new Array(n + 1).fill(0));
    for (let i = 0; i <= m; i++) {
        for (let j = 0; j <= n; j++) {
            if (i === 0) dp[i][j] = j;
            else if (j === 0) dp[i][j] = i;
            else if (X[i - 1] === Y[j - 1]) dp[i][j] = 1 + dp[i - 1][j - 1];
            else dp[i][j] = 1 + Math.min(dp[i - 1][j], dp[i][j - 1]);
        }
    }
    return dp[m][n];
}""",
        "starter_code_java": "class Solution {\\n    public int super_seq(String X, String Y, int m, int n) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int super_seq(String X, String Y, int m, int n) {
        int[][] dp = new int[m + 1][n + 1];
        for (int i = 0; i <= m; i++) {
            for (int j = 0; j <= n; j++) {
                if (i == 0) dp[i][j] = j;
                else if (j == 0) dp[i][j] = i;
                else if (X.charAt(i - 1) == Y.charAt(j - 1)) dp[i][j] = 1 + dp[i - 1][j - 1];
                else dp[i][j] = 1 + Math.min(dp[i - 1][j], dp[i][j - 1]);
            }
        }
        return dp[m][n];
    }
}""",
        "starter_code_cpp": "#include <string>\\nclass Solution {\\npublic:\\n    int super_seq(std::string X, std::string Y, int m, int n);\\n};",
        "reference_solution_cpp": """#include <string>
#include <vector>
#include <algorithm>
class Solution {
public:
    int super_seq(std::string X, std::string Y, int m, int n) {
        std::vector<std::vector<int>> dp(m + 1, std::vector<int>(n + 1, 0));
        for (int i = 0; i <= m; i++) {
            for (int j = 0; j <= n; j++) {
                if (i == 0) dp[i][j] = j;
                else if (j == 0) dp[i][j] = i;
                else if (X[i - 1] == Y[j - 1]) dp[i][j] = 1 + dp[i - 1][j - 1];
                else dp[i][j] = 1 + std::min(dp[i - 1][j], dp[i][j - 1]);
            }
        }
        return dp[m][n];
    }
};"""
    },

    850: {
        "starter_code_javascript": "function max_of_two(x, y) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function max_of_two(x, y) {
    return x > y ? x : y;
}""",
        "starter_code_java": "class Solution {\\n    public int max_of_two(int x, int y) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int max_of_two(int x, int y) {
        return Math.max(x, y);
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int max_of_two(int x, int y);\\n};",
        "reference_solution_cpp": """#include <algorithm>
class Solution {
public:
    int max_of_two(int x, int y) {
        return std::max(x, y);
    }
};"""
    },

    851: {
        "starter_code_javascript": "function mutiple_tuple(nums) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function mutiple_tuple(nums) {
    let product = 1;
    for (let x of nums) product *= x;
    return product;
}""",
        "starter_code_java": "class Solution {\\n    public int mutiple_tuple(int[] nums) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int mutiple_tuple(int[] nums) {
        int product = 1;
        for (int x : nums) product *= x;
        return product;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    int mutiple_tuple(std::vector<int> nums);\\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    int mutiple_tuple(std::vector<int> nums) {
        int product = 1;
        for (int x : nums) product *= x;
        return product;
    }
};"""
    },

    852: {
        "starter_code_javascript": "function rencontres_number(n, m) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function rencontres_number(n, m) {
    if (n === 0 && m === 0) return 1;
    if (n === 1 && m === 0) return 0;
    const D = [1, 0];
    for (let i = 2; i <= n - m; i++) {
        D[i] = (i - 1) * (D[i - 1] + D[i - 2]);
    }
    let C = 1;
    for (let i = 1; i <= m; i++) {
        C = Math.round(C * (n - i + 1) / i);
    }
    return C * D[n - m];
}""",
        "starter_code_java": "class Solution {\\n    public int rencontres_number(int n, int m) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int rencontres_number(int n, int m) {
        if (n == 0 && m == 0) return 1;
        if (n == 1 && m == 0) return 0;
        long[] D = new long[n - m + 1];
        D[0] = 1;
        if (n - m >= 1) D[1] = 0;
        for (int i = 2; i <= n - m; i++) {
            D[i] = (long)(i - 1) * (D[i - 1] + D[i - 2]);
        }
        long C = 1;
        for (int i = 1; i <= m; i++) {
            C = C * (n - i + 1) / i;
        }
        return (int)(C * D[n - m]);
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int rencontres_number(int n, int m);\\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    int rencontres_number(int n, int m) {
        if (n == 0 && m == 0) return 1;
        if (n == 1 && m == 0) return 0;
        std::vector<long long> D(n - m + 1, 0);
        D[0] = 1;
        if (n - m >= 1) D[1] = 0;
        for (int i = 2; i <= n - m; i++) {
            D[i] = 1LL * (i - 1) * (D[i - 1] + D[i - 2]);
        }
        long long C = 1;
        for (int i = 1; i <= m; i++) {
            C = C * (n - i + 1) / i;
        }
        return (int)(C * D[n - m]);
    }
};"""
    },

    853: {
        "starter_code_javascript": "function change_date_format(dt) {\\n    return '';\\n}",
        "reference_solution_javascript": """function change_date_format(dt) {
    const parts = dt.split("-");
    return `${parts[2]}-${parts[1]}-${parts[0]}`;
}""",
        "starter_code_java": "class Solution {\\n    public String change_date_format(String dt) {\\n        return \"\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String change_date_format(String dt) {
        String[] parts = dt.split("-");
        return parts[2] + "-" + parts[1] + "-" + parts[0];
    }
}""",
        "starter_code_cpp": "#include <string>\\nclass Solution {\\npublic:\\n    std::string change_date_format(std::string dt);\\n};",
        "reference_solution_cpp": """#include <string>
class Solution {
public:
    std::string change_date_format(std::string dt) {
        size_t first = dt.find('-');
        size_t second = dt.find('-', first + 1);
        std::string y = dt.substr(0, first);
        std::string m = dt.substr(first + 1, second - first - 1);
        std::string d = dt.substr(second + 1);
        return d + "-" + m + "-" + y;
    }
};"""
    },

    854: {
        "starter_code_javascript": "function count_tuplex(tuplex, value) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function count_tuplex(tuplex, value) {
    let count = 0;
    for (let x of tuplex) if (x === value) count++;
    return count;
}""",
        "starter_code_java": "class Solution {\\n    public int count_tuplex(int[] tuplex, int value) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int count_tuplex(int[] tuplex, int value) {
        int count = 0;
        for (int x : tuplex) if (x == value) count++;
        return count;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    int count_tuplex(std::vector<int> tuplex, int value);\\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    int count_tuplex(std::vector<int> tuplex, int value) {
        int count = 0;
        for (int x : tuplex) if (x == value) count++;
        return count;
    }
};"""
    },

    855: {
        "starter_code_javascript": "function text_match(text) {\\n    return '';\\n}",
        "reference_solution_javascript": """function text_match(text) {
    return text.includes('a') ? "Found a match!" : "Not matched!";
}""",
        "starter_code_java": "class Solution {\\n    public String text_match(String text) {\\n        return \"\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String text_match(String text) {
        return text.contains("a") ? "Found a match!" : "Not matched!";
    }
}""",
        "starter_code_cpp": "#include <string>\\nclass Solution {\\npublic:\\n    std::string text_match(std::string text);\\n};",
        "reference_solution_cpp": """#include <string>
class Solution {
public:
    std::string text_match(std::string text) {
        return text.find('a') != std::string::npos ? "Found a match!" : "Not matched!";
    }
};"""
    },

    856: {
        "starter_code_javascript": "function sum_series(number) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function sum_series(number) {
    let s = (number * (number + 1)) / 2;
    return s * s;
}""",
        "starter_code_java": "class Solution {\\n    public int sum_series(int number) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int sum_series(int number) {
        long s = (long) number * (number + 1) / 2;
        return (int) (s * s);
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int sum_series(int number);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    int sum_series(int number) {
        long long s = 1LL * number * (number + 1) / 2;
        return (int) (s * s);
    }
};"""
    },

    857: {
        "starter_code_javascript": "function remove_duplic_list(l) {\\n    return [];\\n}",
        "reference_solution_javascript": """function remove_duplic_list(l) {
    const seen = new Set();
    const res = [];
    for (let x of l) {
        if (!seen.has(x)) {
            seen.add(x);
            res.push(x);
        }
    }
    return res;
}""",
        "starter_code_java": "class Solution {\\n    public String[] remove_duplic_list(String[] l) {\\n        return new String[0];\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public String[] remove_duplic_list(String[] l) {
        Set<String> seen = new LinkedHashSet<>();
        for (String s : l) seen.add(s);
        return seen.toArray(new String[0]);
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nclass Solution {\\npublic:\\n    std::vector<std::string> remove_duplic_list(std::vector<std::string> l);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <unordered_set>
class Solution {
public:
    std::vector<std::string> remove_duplic_list(std::vector<std::string> l) {
        std::unordered_set<std::string> seen;
        std::vector<std::string> res;
        for (const auto& s : l) {
            if (seen.insert(s).second) res.push_back(s);
        }
        return res;
    }
};"""
    },

    858: {
        "starter_code_javascript": "function camel_to_snake(text) {\\n    return '';\\n}",
        "reference_solution_javascript": """function camel_to_snake(text) {
    let res = "";
    for (let i = 0; i < text.length; i++) {
        let ch = text[i];
        if (ch >= 'A' && ch <= 'Z') {
            if (i > 0) res += "_";
            res += ch.toLowerCase();
        } else {
            res += ch;
        }
    }
    return res;
}""",
        "starter_code_java": "class Solution {\\n    public String camel_to_snake(String text) {\\n        return \"\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String camel_to_snake(String text) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < text.length(); i++) {
            char c = text.charAt(i);
            if (Character.isUpperCase(c)) {
                if (i > 0) sb.append('_');
                sb.append(Character.toLowerCase(c));
            } else {
                sb.append(c);
            }
        }
        return sb.toString();
    }
}""",
        "starter_code_cpp": "#include <string>\\nclass Solution {\\npublic:\\n    std::string camel_to_snake(std::string text);\\n};",
        "reference_solution_cpp": """#include <string>
#include <cctype>
class Solution {
public:
    std::string camel_to_snake(std::string text) {
        std::string res;
        for (size_t i = 0; i < text.size(); i++) {
            char c = text[i];
            if (std::isupper(static_cast<unsigned char>(c))) {
                if (i > 0) res += '_';
                res += std::tolower(static_cast<unsigned char>(c));
            } else {
                res += c;
            }
        }
        return res;
    }
};"""
    },

    859: {
        "starter_code_javascript": "function dealnnoy_num(n, m) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function dealnnoy_num(n, m) {
    const dp = Array.from({ length: n + 1 }, () => new Array(m + 1).fill(0));
    for (let i = 0; i <= n; i++) dp[i][0] = 1;
    for (let j = 0; j <= m; j++) dp[0][j] = 1;
    for (let i = 1; i <= n; i++) {
        for (let j = 1; j <= m; j++) {
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1] + dp[i - 1][j - 1];
        }
    }
    return dp[n][m];
}""",
        "starter_code_java": "class Solution {\\n    public int dealnnoy_num(int n, int m) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int dealnnoy_num(int n, int m) {
        int[][] dp = new int[n + 1][m + 1];
        for (int i = 0; i <= n; i++) dp[i][0] = 1;
        for (int j = 0; j <= m; j++) dp[0][j] = 1;
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= m; j++) {
                dp[i][j] = dp[i - 1][j] + dp[i][j - 1] + dp[i - 1][j - 1];
            }
        }
        return dp[n][m];
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int dealnnoy_num(int n, int m);\\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    int dealnnoy_num(int n, int m) {
        std::vector<std::vector<int>> dp(n + 1, std::vector<int>(m + 1, 0));
        for (int i = 0; i <= n; i++) dp[i][0] = 1;
        for (int j = 0; j <= m; j++) dp[0][j] = 1;
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= m; j++) {
                dp[i][j] = dp[i - 1][j] + dp[i][j - 1] + dp[i - 1][j - 1];
            }
        }
        return dp[n][m];
    }
};"""
    },

    860: {
        "starter_code_javascript": "function series_sum(number) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function series_sum(number) {
    return Math.floor((number * (number + 1) * (2 * number + 1)) / 6);
}""",
        "starter_code_java": "class Solution {\\n    public int series_sum(int number) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int series_sum(int number) {
        return (int) (((long) number * (number + 1) * (2 * number + 1)) / 6);
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int series_sum(int number);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    int series_sum(int number) {
        return (int) ((1LL * number * (number + 1) * (2 * number + 1)) / 6);
    }
};"""
    }
}
'''

def main():
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(solutions_code)
    print(f"Batch 16 solutions written to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
