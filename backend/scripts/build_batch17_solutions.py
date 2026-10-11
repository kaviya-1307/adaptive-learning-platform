import os

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "batch17_solutions.py")

solutions_code = '''"""
Curated and specialized solutions for MBPP problems (Batch 17: 861-889).
Final Batch of the 889-problem platform.
"""

BATCH17_SOLUTIONS = {
    861: {
        "starter_code_javascript": "function max_char(str1) {\\n    return '';\\n}",
        "reference_solution_javascript": """function max_char(str1) {
    const counts = {};
    for (let c of str1) counts[c] = (counts[c] || 0) + 1;
    let best = '', maxC = 0;
    for (let c of str1) {
        if (counts[c] > maxC) {
            maxC = counts[c];
            best = c;
        }
    }
    return best;
}""",
        "starter_code_java": "class Solution {\\n    public String max_char(String str1) {\\n        return \"\";\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public String max_char(String str1) {
        Map<Character, Integer> counts = new HashMap<>();
        for (char c : str1.toCharArray()) counts.put(c, counts.getOrDefault(c, 0) + 1);
        char best = str1.charAt(0);
        int maxC = 0;
        for (char c : str1.toCharArray()) {
            if (counts.get(c) > maxC) {
                maxC = counts.get(c);
                best = c;
            }
        }
        return String.valueOf(best);
    }
}""",
        "starter_code_cpp": "#include <string>\\nclass Solution {\\npublic:\\n    std::string max_char(std::string str1);\\n};",
        "reference_solution_cpp": """#include <string>
#include <unordered_map>
class Solution {
public:
    std::string max_char(const std::string& str1) {
        std::unordered_map<char, int> counts;
        for (char c : str1) counts[c]++;
        char best = str1[0];
        int maxC = 0;
        for (char c : str1) {
            if (counts[c] > maxC) {
                maxC = counts[c];
                best = c;
            }
        }
        return std::string(1, best);
    }
};"""
    },

    862: {
        "starter_code_javascript": "function sorted_models(models) {\\n    return [];\\n}",
        "reference_solution_javascript": """function sorted_models(models) {
    return [...models].sort((a, b) => (a.color || '').localeCompare(b.color || ''));
}""",
        "starter_code_java": "class Solution {\\n    public Object[] sorted_models(Object[] models) {\\n        return new Object[0];\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public Object[] sorted_models(Object[] models) {
        Object[] res = models.clone();
        Arrays.sort(res, (a, b) -> {
            Map ma = (Map) a;
            Map mb = (Map) b;
            String ca = String.valueOf(ma.get("color"));
            String cb = String.valueOf(mb.get("color"));
            return ca.compareTo(cb);
        });
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <unordered_map>\\n#include <string>\\nclass Solution {\\npublic:\\n    std::vector<std::unordered_map<std::string, std::string>> sorted_models(std::vector<std::unordered_map<std::string, std::string>> models);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <unordered_map>
#include <string>
#include <algorithm>
class Solution {
public:
    std::vector<std::unordered_map<std::string, std::string>> sorted_models(std::vector<std::unordered_map<std::string, std::string>> models) {
        std::stable_sort(models.begin(), models.end(), [](const auto& a, const auto& b) {
            auto itA = a.find("color");
            auto itB = b.find("color");
            std::string colA = (itA != a.end()) ? itA->second : "";
            std::string colB = (itB != b.end()) ? itB->second : "";
            return colA < colB;
        });
        return models;
    }
};"""
    },

    863: {
        "starter_code_javascript": "function check_element(test_tup, check_list) {\\n    return false;\\n}",
        "reference_solution_javascript": """function check_element(test_tup, check_list) {
    const s = new Set(test_tup);
    return check_list.some(x => s.has(x));
}""",
        "starter_code_java": "class Solution {\\n    public boolean check_element(int[] test_tup, int[] check_list) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public boolean check_element(int[] test_tup, int[] check_list) {
        Set<Integer> s = new HashSet<>();
        for (int x : test_tup) s.add(x);
        for (int x : check_list) if (s.contains(x)) return true;
        return false;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    bool check_element(std::vector<int> test_tup, std::vector<int> check_list);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <unordered_set>
class Solution {
public:
    bool check_element(const std::vector<int>& test_tup, const std::vector<int>& check_list) {
        std::unordered_set<int> s(test_tup.begin(), test_tup.end());
        for (int x : check_list) if (s.count(x)) return true;
        return false;
    }
};"""
    },

    864: {
        "starter_code_javascript": "function combine_lists(num1, num2) {\\n    return [];\\n}",
        "reference_solution_javascript": """function combine_lists(num1, num2) {
    const res = [];
    let i = 0, j = 0;
    while (i < num1.length && j < num2.length) {
        if (num1[i] <= num2[j]) res.push(num1[i++]);
        else res.push(num2[j++]);
    }
    while (i < num1.length) res.push(num1[i++]);
    while (j < num2.length) res.push(num2[j++]);
    return res;
}""",
        "starter_code_java": "class Solution {\\n    public int[] combine_lists(int[] num1, int[] num2) {\\n        return new int[0];\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int[] combine_lists(int[] num1, int[] num2) {
        int[] res = new int[num1.length + num2.length];
        int i = 0, j = 0, k = 0;
        while (i < num1.length && j < num2.length) {
            if (num1[i] <= num2[j]) res[k++] = num1[i++];
            else res[k++] = num2[j++];
        }
        while (i < num1.length) res[k++] = num1[i++];
        while (j < num2.length) res[k++] = num2[j++];
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    std::vector<int> combine_lists(std::vector<int> num1, std::vector<int> num2);\\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    std::vector<int> combine_lists(const std::vector<int>& num1, const std::vector<int>& num2) {
        std::vector<int> res;
        size_t i = 0, j = 0;
        while (i < num1.size() && j < num2.size()) {
            if (num1[i] <= num2[j]) res.push_back(num1[i++]);
            else res.push_back(num2[j++]);
        }
        while (i < num1.size()) res.push_back(num1[i++]);
        while (j < num2.size()) res.push_back(num2[j++]);
        return res;
    }
};"""
    },

    865: {
        "starter_code_javascript": "function num_position(text) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function num_position(text) {
    for (let i = 0; i < text.length; i++) {
        if (text[i] >= '0' && text[i] <= '9') return i;
    }
    return -1;
}""",
        "starter_code_java": "class Solution {\\n    public int num_position(String text) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int num_position(String text) {
        for (int i = 0; i < text.length(); i++) {
            if (Character.isDigit(text.charAt(i))) return i;
        }
        return -1;
    }
}""",
        "starter_code_cpp": "#include <string>\\nclass Solution {\\npublic:\\n    int num_position(std::string text);\\n};",
        "reference_solution_cpp": """#include <string>
#include <cctype>
class Solution {
public:
    int num_position(const std::string& text) {
        for (size_t i = 0; i < text.size(); i++) {
            if (std::isdigit(static_cast<unsigned char>(text[i]))) return (int) i;
        }
        return -1;
    }
};"""
    },

    866: {
        "starter_code_javascript": "function len_log(list1) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function len_log(list1) {
    let minL = list1[0].length;
    for (let s of list1) if (s.length < minL) minL = s.length;
    return minL;
}""",
        "starter_code_java": "class Solution {\\n    public int len_log(String[] list1) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int len_log(String[] list1) {
        int minL = list1[0].length();
        for (String s : list1) if (s.length() < minL) minL = s.length();
        return minL;
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nclass Solution {\\npublic:\\n    int len_log(std::vector<std::string> list1);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <algorithm>
class Solution {
public:
    int len_log(const std::vector<std::string>& list1) {
        size_t minL = list1[0].size();
        for (const auto& s : list1) minL = std::min(minL, s.size());
        return (int) minL;
    }
};"""
    },

    867: {
        "starter_code_javascript": "function get_item(tup1, index) {\\n    return '';\\n}",
        "reference_solution_javascript": """function get_item(tup1, index) {
    if (index < 0) index += tup1.length;
    return String(tup1[index]);
}""",
        "starter_code_java": "class Solution {\\n    public String get_item(Object[] tup1, int index) {\\n        return \"\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String get_item(Object[] tup1, int index) {
        if (index < 0) index += tup1.length;
        return String.valueOf(tup1[index]);
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nclass Solution {\\npublic:\\n    std::string get_item(std::vector<std::string> tup1, int index);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
class Solution {
public:
    std::string get_item(const std::vector<std::string>& tup1, int index) {
        if (index < 0) index += tup1.size();
        return tup1[index];
    }
};"""
    },

    868: {
        "starter_code_javascript": "function chinese_zodiac(year) {\\n    return '';\\n}",
        "reference_solution_javascript": """function chinese_zodiac(year) {
    const signs = ['Dragon', 'Snake', 'Horse', 'sheep', 'Monkey', 'Rooster', 'Dog', 'Pig', 'Rat', 'Ox', 'Tiger', 'Hare'];
    let idx = ((year - 2000) % 12 + 12) % 12;
    return signs[idx];
}""",
        "starter_code_java": "class Solution {\\n    public String chinese_zodiac(int year) {\\n        return \"\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String chinese_zodiac(int year) {
        String[] signs = {"Dragon", "Snake", "Horse", "sheep", "Monkey", "Rooster", "Dog", "Pig", "Rat", "Ox", "Tiger", "Hare"};
        int idx = ((year - 2000) % 12 + 12) % 12;
        return signs[idx];
    }
}""",
        "starter_code_cpp": "#include <string>\\nclass Solution {\\npublic:\\n    std::string chinese_zodiac(int year);\\n};",
        "reference_solution_cpp": """#include <string>
#include <vector>
class Solution {
public:
    std::string chinese_zodiac(int year) {
        std::vector<std::string> signs = {"Dragon", "Snake", "Horse", "sheep", "Monkey", "Rooster", "Dog", "Pig", "Rat", "Ox", "Tiger", "Hare"};
        int idx = ((year - 2000) % 12 + 12) % 12;
        return signs[idx];
    }
};"""
    },

    869: {
        "starter_code_javascript": "function nCr_mod_p(n, r, p) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function nCr_mod_p(n, r, p) {
    if (r > n - r) r = n - r;
    const C = new Array(r + 1).fill(0);
    C[0] = 1;
    for (let i = 1; i <= n; i++) {
        for (let j = Math.min(i, r); j > 0; j--) {
            C[j] = (C[j] + C[j - 1]) % p;
        }
    }
    return C[r];
}""",
        "starter_code_java": "class Solution {\\n    public int nCr_mod_p(int n, int r, int p) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int nCr_mod_p(int n, int r, int p) {
        if (r > n - r) r = n - r;
        int[] C = new int[r + 1];
        C[0] = 1;
        for (int i = 1; i <= n; i++) {
            for (int j = Math.min(i, r); j > 0; j--) {
                C[j] = (C[j] + C[j - 1]) % p;
            }
        }
        return C[r];
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int nCr_mod_p(int n, int r, int p);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
class Solution {
public:
    int nCr_mod_p(int n, int r, int p) {
        if (r > n - r) r = n - r;
        std::vector<int> C(r + 1, 0);
        C[0] = 1;
        for (int i = 1; i <= n; i++) {
            for (int j = std::min(i, r); j > 0; j--) {
                C[j] = (C[j] + C[j - 1]) % p;
            }
        }
        return C[r];
    }
};"""
    },

    870: {
        "starter_code_javascript": "function subset(ar, n) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function subset(ar, n) {
    const sorted = [...ar].sort((a, b) => a - b);
    let count = 1;
    for (let i = 0; i < n - 1; i++) {
        if (sorted[i] === sorted[i + 1]) count++;
        else break;
    }
    return count;
}""",
        "starter_code_java": "class Solution {\\n    public int subset(int[] ar, int n) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int subset(int[] ar, int n) {
        int[] sorted = ar.clone();
        Arrays.sort(sorted);
        int count = 1;
        for (int i = 0; i < n - 1; i++) {
            if (sorted[i] == sorted[i + 1]) count++;
            else break;
        }
        return count;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    int subset(std::vector<int> ar, int n);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
class Solution {
public:
    int subset(std::vector<int> ar, int n) {
        std::sort(ar.begin(), ar.end());
        int count = 1;
        for (int i = 0; i < n - 1; i++) {
            if (ar[i] == ar[i + 1]) count++;
            else break;
        }
        return count;
    }
};"""
    },

    871: {
        "starter_code_javascript": "function profit_amount(actual_cost, sale_amount) {\\n    return null;\\n}",
        "reference_solution_javascript": """function profit_amount(actual_cost, sale_amount) {
    if (actual_cost > sale_amount) return actual_cost - sale_amount;
    return null;
}""",
        "starter_code_java": "class Solution {\\n    public Integer profit_amount(int actual_cost, int sale_amount) {\\n        return null;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public Integer profit_amount(int actual_cost, int sale_amount) {
        if (actual_cost > sale_amount) return actual_cost - sale_amount;
        return null;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int profit_amount(int actual_cost, int sale_amount);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    int profit_amount(int actual_cost, int sale_amount) {
        if (actual_cost > sale_amount) return actual_cost - sale_amount;
        return 0;
    }
};"""
    },

    872: {
        "starter_code_javascript": "function is_abundant(n) {\\n    return false;\\n}",
        "reference_solution_javascript": """function is_abundant(n) {
    let sum = 0;
    for (let i = 1; i < n; i++) {
        if (n % i === 0) sum += i;
    }
    return sum > n;
}""",
        "starter_code_java": "class Solution {\\n    public boolean is_abundant(int n) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public boolean is_abundant(int n) {
        int sum = 0;
        for (int i = 1; i < n; i++) {
            if (n % i == 0) sum += i;
        }
        return sum > n;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    bool is_abundant(int n);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    bool is_abundant(int n) {
        int sum = 0;
        for (int i = 1; i < n; i++) {
            if (n % i == 0) sum += i;
        }
        return sum > n;
    }
};"""
    },

    873: {
        "starter_code_javascript": "function split_list(text) {\\n    return [];\\n}",
        "reference_solution_javascript": """function split_list(text) {
    return text.match(/[A-Z][^A-Z]*/g) || [];
}""",
        "starter_code_java": "class Solution {\\n    public String[] split_list(String text) {\\n        return new String[0];\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
import java.util.regex.*;
class Solution {
    public String[] split_list(String text) {
        List<String> list = new ArrayList<>();
        Matcher m = Pattern.compile("[A-Z][^A-Z]*").matcher(text);
        while (m.find()) list.add(m.group());
        return list.toArray(new String[0]);
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nclass Solution {\\npublic:\\n    std::vector<std::string> split_list(std::string text);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <cctype>
class Solution {
public:
    std::vector<std::string> split_list(const std::string& text) {
        std::vector<std::string> res;
        std::string cur = "";
        for (char c : text) {
            if (std::isupper(static_cast<unsigned char>(c))) {
                if (!cur.empty()) res.push_back(cur);
                cur = std::string(1, c);
            } else {
                cur += c;
            }
        }
        if (!cur.empty()) res.push_back(cur);
        return res;
    }
};"""
    },

    874: {
        "starter_code_javascript": "function get_First_Set_Bit_Pos(n) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function get_First_Set_Bit_Pos(n) {
    if (n === 0) return 0;
    return Math.log2(n & -n) + 1;
}""",
        "starter_code_java": "class Solution {\\n    public int get_First_Set_Bit_Pos(int n) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int get_First_Set_Bit_Pos(int n) {
        if (n == 0) return 0;
        return Integer.numberOfTrailingZeros(n) + 1;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int get_First_Set_Bit_Pos(int n);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    int get_First_Set_Bit_Pos(int n) {
        if (n == 0) return 0;
        return __builtin_ctz(n) + 1;
    }
};"""
    },

    875: {
        "starter_code_javascript": "function int_to_roman(num) {\\n    return '';\\n}",
        "reference_solution_javascript": """function int_to_roman(num) {
    const val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1];
    const syb = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"];
    let res = "";
    for (let i = 0; i < val.length; i++) {
        while (num >= val[i]) {
            res += syb[i];
            num -= val[i];
        }
    }
    return res;
}""",
        "starter_code_java": "class Solution {\\n    public String int_to_roman(int num) {\\n        return \"\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String int_to_roman(int num) {
        int[] val = {1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1};
        String[] syb = {"M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"};
        StringBuilder res = new StringBuilder();
        for (int i = 0; i < val.length; i++) {
            while (num >= val[i]) {
                res.append(syb[i]);
                num -= val[i];
            }
        }
        return res.toString();
    }
}""",
        "starter_code_cpp": "#include <string>\\nclass Solution {\\npublic:\\n    std::string int_to_roman(int num);\\n};",
        "reference_solution_cpp": """#include <string>
#include <vector>
class Solution {
public:
    std::string int_to_roman(int num) {
        int val[] = {1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1};
        std::string syb[] = {"M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"};
        std::string res = "";
        for (int i = 0; i < 13; i++) {
            while (num >= val[i]) {
                res += syb[i];
                num -= val[i];
            }
        }
        return res;
    }
};"""
    },

    876: {
        "starter_code_javascript": "function Average(lst) {\\n    return 0.0;\\n}",
        "reference_solution_javascript": """function Average(lst) {
    let s = 0;
    for (let x of lst) s += x;
    return s / lst.length;
}""",
        "starter_code_java": "class Solution {\\n    public double Average(int[] lst) {\\n        return 0.0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public double Average(int[] lst) {
        double s = 0;
        for (int x : lst) s += x;
        return s / lst.length;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    double Average(std::vector<int> lst);\\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    double Average(const std::vector<int>& lst) {
        double s = 0;
        for (int x : lst) s += x;
        return s / lst.size();
    }
};"""
    },

    877: {
        "starter_code_javascript": "function get_noOfways(n) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function get_noOfways(n) {
    if (n === 0) return 0;
    if (n === 1) return 1;
    let a = 0, b = 1;
    for (let i = 2; i <= n; i++) {
        let c = a + b;
        a = b;
        b = c;
    }
    return b;
}""",
        "starter_code_java": "class Solution {\\n    public int get_noOfways(int n) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int get_noOfways(int n) {
        if (n == 0) return 0;
        if (n == 1) return 1;
        int a = 0, b = 1;
        for (int i = 2; i <= n; i++) {
            int c = a + b;
            a = b;
            b = c;
        }
        return b;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int get_noOfways(int n);\\n};",
        "reference_solution_cpp": """class Solution {
public:
    int get_noOfways(int n) {
        if (n == 0) return 0;
        if (n == 1) return 1;
        int a = 0, b = 1;
        for (int i = 2; i <= n; i++) {
            int c = a + b;
            a = b;
            b = c;
        }
        return b;
    }
};"""
    },

    878: {
        "starter_code_javascript": "function roman_to_int(s) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function roman_to_int(s) {
    const val = { 'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000 };
    let total = 0;
    for (let i = 0; i < s.length; i++) {
        if (i > 0 && val[s[i]] > val[s[i - 1]]) {
            total += val[s[i]] - 2 * val[s[i - 1]];
        } else {
            total += val[s[i]];
        }
    }
    return total;
}""",
        "starter_code_java": "class Solution {\\n    public int roman_to_int(String s) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int roman_to_int(String s) {
        Map<Character, Integer> val = new HashMap<>();
        val.put('I', 1); val.put('V', 5); val.put('X', 10);
        val.put('L', 50); val.put('C', 100); val.put('D', 500); val.put('M', 1000);
        int total = 0;
        for (int i = 0; i < s.length(); i++) {
            int cur = val.get(s.charAt(i));
            if (i > 0 && cur > val.get(s.charAt(i - 1))) {
                total += cur - 2 * val.get(s.charAt(i - 1));
            } else {
                total += cur;
            }
        }
        return total;
    }
}""",
        "starter_code_cpp": "#include <string>\\nclass Solution {\\npublic:\\n    int roman_to_int(std::string s);\\n};",
        "reference_solution_cpp": """#include <string>
#include <unordered_map>
class Solution {
public:
    int roman_to_int(const std::string& s) {
        std::unordered_map<char, int> val = {
            {'I', 1}, {'V', 5}, {'X', 10}, {'L', 50}, {'C', 100}, {'D', 500}, {'M', 1000}
        };
        int total = 0;
        for (size_t i = 0; i < s.size(); i++) {
            int cur = val[s[i]];
            if (i > 0 && cur > val[s[i - 1]]) {
                total += cur - 2 * val[s[i - 1]];
            } else {
                total += cur;
            }
        }
        return total;
    }
};"""
    },

    879: {
        "starter_code_javascript": "function sum_Even(l, r) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function sum_Even(l, r) {
    function sumNat(n) { return n * (n + 1); }
    return sumNat(Math.floor(r / 2)) - sumNat(Math.floor((l - 1) / 2));
}""",
        "starter_code_java": "class Solution {\\n    public int sum_Even(int l, int r) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    private int sumNat(int n) { return n * (n + 1); }
    public int sum_Even(int l, int r) {
        return sumNat(r / 2) - sumNat((l - 1) / 2);
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int sum_Even(int l, int r);\\n};",
        "reference_solution_cpp": """class Solution {
    int sumNat(int n) { return n * (n + 1); }
public:
    int sum_Even(int l, int r) {
        return sumNat(r / 2) - sumNat((l - 1) / 2);
    }
};"""
    },

    880: {
        "starter_code_javascript": "function word_len(s) {\\n    return false;\\n}",
        "reference_solution_javascript": """function word_len(s) {
    const word = s.split(' ')[0];
    return word.length % 2 === 0;
}""",
        "starter_code_java": "class Solution {\\n    public boolean word_len(String s) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public boolean word_len(String s) {
        String word = s.split(" ")[0];
        return word.length() % 2 == 0;
    }
}""",
        "starter_code_cpp": "#include <string>\\nclass Solution {\\npublic:\\n    bool word_len(std::string s);\\n};",
        "reference_solution_cpp": """#include <string>
class Solution {
public:
    bool word_len(const std::string& s) {
        size_t sp = s.find(' ');
        size_t len = (sp == std::string::npos) ? s.size() : sp;
        return len % 2 == 0;
    }
};"""
    },

    881: {
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
    std::string camel_to_snake(const std::string& text) {
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

    882: {
        "starter_code_javascript": "function remove_empty(tuple1) {\\n    return [];\\n}",
        "reference_solution_javascript": """function remove_empty(tuple1) {
    return tuple1.filter(t => {
        if (Array.isArray(t)) return t.length > 0;
        return Boolean(t);
    });
}""",
        "starter_code_java": "class Solution {\\n    public Object[] remove_empty(Object[] tuple1) {\\n        return new Object[0];\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public Object[] remove_empty(Object[] tuple1) {
        List<Object> res = new ArrayList<>();
        for (Object t : tuple1) {
            if (t instanceof Object[]) {
                if (((Object[]) t).length > 0) res.add(t);
            } else if (t instanceof int[]) {
                if (((int[]) t).length > 0) res.add(t);
            } else if (t instanceof String[]) {
                if (((String[]) t).length > 0) res.add(t);
            } else if (t != null) {
                res.add(t);
            }
        }
        return res.toArray();
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nclass Solution {\\npublic:\\n    std::vector<std::string> remove_empty(std::vector<std::string> tuple1);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
class Solution {
public:
    std::vector<std::string> remove_empty(const std::vector<std::string>& tuple1) {
        std::vector<std::string> res;
        for (const auto& s : tuple1) {
            if (!s.empty()) res.push_back(s);
        }
        return res;
    }
};"""
    },

    883: {
        "starter_code_javascript": "function check(string) {\\n    return '';\\n}",
        "reference_solution_javascript": """function check(string) {
    const vowels = new Set("AEIOUaeiou");
    const found = new Set();
    for (let c of string) if (vowels.has(c)) found.add(c);
    return found.size >= 5 ? "accepted" : "not accepted";
}""",
        "starter_code_java": "class Solution {\\n    public String check(String string) {\\n        return \"\";\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public String check(String string) {
        Set<Character> found = new HashSet<>();
        String vowels = "AEIOUaeiou";
        for (char c : string.toCharArray()) {
            if (vowels.indexOf(c) != -1) found.add(c);
        }
        return found.size() >= 5 ? "accepted" : "not accepted";
    }
}""",
        "starter_code_cpp": "#include <string>\\nclass Solution {\\npublic:\\n    std::string check(std::string string);\\n};",
        "reference_solution_cpp": """#include <string>
#include <unordered_set>
class Solution {
public:
    std::string check(const std::string& str) {
        std::unordered_set<char> found;
        std::string vowels = "AEIOUaeiou";
        for (char c : str) {
            if (vowels.find(c) != std::string::npos) found.insert(c);
        }
        return found.size() >= 5 ? "accepted" : "not accepted";
    }
};"""
    },

    884: {
        "starter_code_javascript": "function floor_Max(A, B, N) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function floor_Max(A, B, N) {
    let x = Math.min(B - 1, N);
    return Math.floor((A * x) / B);
}""",
        "starter_code_java": "class Solution {\\n    public int floor_Max(int A, int B, int N) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int floor_Max(int A, int B, int N) {
        int x = Math.min(B - 1, N);
        return (A * x) / B;
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int floor_Max(int A, int B, int N);\\n};",
        "reference_solution_cpp": """#include <algorithm>
class Solution {
public:
    int floor_Max(int A, int B, int N) {
        int x = std::min(B - 1, N);
        return (A * x) / B;
    }
};"""
    },

    885: {
        "starter_code_javascript": "function min_of_two(x, y) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function min_of_two(x, y) {
    return x < y ? x : y;
}""",
        "starter_code_java": "class Solution {\\n    public int min_of_two(int x, int y) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int min_of_two(int x, int y) {
        return Math.min(x, y);
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int min_of_two(int x, int y);\\n};",
        "reference_solution_cpp": """#include <algorithm>
class Solution {
public:
    int min_of_two(int x, int y) {
        return std::min(x, y);
    }
};"""
    },

    886: {
        "starter_code_javascript": "function maximum_segments(n, a, b, c) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function maximum_segments(n, a, b, c) {
    const dp = new Array(n + 10).fill(-1);
    dp[0] = 0;
    for (let i = 0; i < n; i++) {
        if (dp[i] !== -1) {
            if (i + a <= n) dp[i + a] = Math.max(dp[i] + 1, dp[i + a]);
            if (i + b <= n) dp[i + b] = Math.max(dp[i] + 1, dp[i + b]);
            if (i + c <= n) dp[i + c] = Math.max(dp[i] + 1, dp[i + c]);
        }
    }
    return dp[n];
}""",
        "starter_code_java": "class Solution {\\n    public int maximum_segments(int n, int a, int b, int c) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int maximum_segments(int n, int a, int b, int c) {
        int[] dp = new int[n + 10];
        Arrays.fill(dp, -1);
        dp[0] = 0;
        for (int i = 0; i < n; i++) {
            if (dp[i] != -1) {
                if (i + a <= n) dp[i + a] = Math.max(dp[i] + 1, dp[i + a]);
                if (i + b <= n) dp[i + b] = Math.max(dp[i] + 1, dp[i + b]);
                if (i + c <= n) dp[i + c] = Math.max(dp[i] + 1, dp[i + c]);
            }
        }
        return dp[n];
    }
}""",
        "starter_code_cpp": "class Solution {\\npublic:\\n    int maximum_segments(int n, int a, int b, int c);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
class Solution {
public:
    int maximum_segments(int n, int a, int b, int c) {
        std::vector<int> dp(n + 10, -1);
        dp[0] = 0;
        for (int i = 0; i < n; i++) {
            if (dp[i] != -1) {
                if (i + a <= n) dp[i + a] = std::max(dp[i] + 1, dp[i + a]);
                if (i + b <= n) dp[i + b] = std::max(dp[i] + 1, dp[i + b]);
                if (i + c <= n) dp[i + c] = std::max(dp[i] + 1, dp[i + c]);
            }
        }
        return dp[n];
    }
};"""
    },

    887: {
        "starter_code_javascript": "function concatenate_nested(test_tup1, test_tup2) {\\n    return [];\\n}",
        "reference_solution_javascript": """function concatenate_nested(test_tup1, test_tup2) {
    return test_tup1.concat(test_tup2);
}""",
        "starter_code_java": "class Solution {\\n    public int[] concatenate_nested(int[] test_tup1, int[] test_tup2) {\\n        return new int[0];\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int[] concatenate_nested(int[] test_tup1, int[] test_tup2) {
        int[] res = new int[test_tup1.length + test_tup2.length];
        System.arraycopy(test_tup1, 0, res, 0, test_tup1.length);
        System.arraycopy(test_tup2, 0, res, test_tup1.length, test_tup2.length);
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    std::vector<int> concatenate_nested(std::vector<int> test_tup1, std::vector<int> test_tup2);\\n};",
        "reference_solution_cpp": """#include <vector>
class Solution {
public:
    std::vector<int> concatenate_nested(const std::vector<int>& test_tup1, const std::vector<int>& test_tup2) {
        std::vector<int> res = test_tup1;
        res.insert(res.end(), test_tup2.begin(), test_tup2.end());
        return res;
    }
};"""
    },

    888: {
        "starter_code_javascript": "function left_rotate(s, d) {\\n    return '';\\n}",
        "reference_solution_javascript": """function left_rotate(s, d) {
    return s.slice(d) + s.slice(0, d);
}""",
        "starter_code_java": "class Solution {\\n    public String left_rotate(String s, int d) {\\n        return \"\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String left_rotate(String s, int d) {
        return s.substring(d) + s.substring(0, d);
    }
}""",
        "starter_code_cpp": "#include <string>\\nclass Solution {\\npublic:\\n    std::string left_rotate(std::string s, int d);\\n};",
        "reference_solution_cpp": """#include <string>
class Solution {
public:
    std::string left_rotate(const std::string& s, int d) {
        return s.substr(d) + s.substr(0, d);
    }
};"""
    },

    889: {
        "starter_code_javascript": "function min_sum_path(A) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function min_sum_path(A) {
    const memo = [...A[A.length - 1]];
    for (let i = A.length - 2; i >= 0; i--) {
        for (let j = 0; j < A[i].length; j++) {
            memo[j] = A[i][j] + Math.min(memo[j], memo[j + 1]);
        }
    }
    return memo[0];
}""",
        "starter_code_java": "class Solution {\\n    public int min_sum_path(int[][] A) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int min_sum_path(int[][] A) {
        int n = A.length;
        int[] memo = A[n - 1].clone();
        for (int i = n - 2; i >= 0; i--) {
            for (int j = 0; j < A[i].length; j++) {
                memo[j] = A[i][j] + Math.min(memo[j], memo[j + 1]);
            }
        }
        return memo[0];
    }
}""",
        "starter_code_cpp": "#include <vector>\\nclass Solution {\\npublic:\\n    int min_sum_path(std::vector<std::vector<int>> A);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
class Solution {
public:
    int min_sum_path(const std::vector<std::vector<int>>& A) {
        int n = A.size();
        std::vector<int> memo = A.back();
        for (int i = n - 2; i >= 0; i--) {
            for (size_t j = 0; j < A[i].size(); j++) {
                memo[j] = A[i][j] + std::min(memo[j], memo[j + 1]);
            }
        }
        return memo[0];
    }
};"""
    }
}
'''

def main():
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(solutions_code)
    print(f"Batch 17 solutions written to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
