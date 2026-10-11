import os

BATCH6_CONTENT = '''"""
Curated and specialized solutions for MBPP problems (Batch 6: 311-360).
"""

BATCH6_SOLUTIONS = {
    312: {
        "starter_code_javascript": "function find_Max_Len_Even(str) {\\n    return \\"-1\\";\\n}",
        "reference_solution_javascript": """function find_Max_Len_Even(str) {
    const words = str.split(' ');
    let maxWord = "-1";
    for (const w of words) {
        if (w.length % 2 === 0 && (maxWord === "-1" || w.length > maxWord.length)) {
            maxWord = w;
        }
    }
    return maxWord;
}""",
        "starter_code_java": "class Solution {\\n    public String find_Max_Len_Even(String str) {\\n        return \\"-1\\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String find_Max_Len_Even(String str) {
        String[] words = str.split(" ");
        String maxWord = "-1";
        for (String w : words) {
            if (w.length() % 2 == 0) {
                if (maxWord.equals("-1") || w.length() > maxWord.length()) {
                    maxWord = w;
                }
            }
        }
        return maxWord;
    }
}""",
        "starter_code_cpp": "#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    string find_Max_Len_Even(const string& str);\\n};",
        "reference_solution_cpp": """#include <string>
#include <sstream>
using namespace std;
class Solution {
public:
    string find_Max_Len_Even(const string& str) {
        stringstream ss(str);
        string w;
        string maxWord = "-1";
        while (ss >> w) {
            if (w.length() % 2 == 0) {
                if (maxWord == "-1" || w.length() > maxWord.length()) {
                    maxWord = w;
                }
            }
        }
        return maxWord;
    }
};"""
    },

    314: {
        "starter_code_javascript": "function modified_encode(alist) {\\n    return [];\\n}",
        "reference_solution_javascript": """function modified_encode(alist) {
    const res = [];
    if (!alist || alist.length === 0) return res;
    let count = 1;
    let prev = alist[0];
    for (let i = 1; i < alist.length; i++) {
        if (alist[i] === prev) {
            count++;
        } else {
            res.push(count > 1 ? [count, prev] : prev);
            prev = alist[i];
            count = 1;
        }
    }
    res.push(count > 1 ? [count, prev] : prev);
    return res;
}""",
        "starter_code_java": "class Solution {\\n    public Object modified_encode(int[] alist) {\\n        return new Object[]{};\\n    }\\n    public Object modified_encode(String alist) {\\n        return new Object[]{};\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public Object modified_encode(int[] alist) {
        List<Object> res = new ArrayList<>();
        if (alist == null || alist.length == 0) return res.toArray();
        int count = 1;
        int prev = alist[0];
        for (int i = 1; i < alist.length; i++) {
            if (alist[i] == prev) {
                count++;
            } else {
                if (count > 1) res.add(new int[]{count, prev});
                else res.add(prev);
                prev = alist[i];
                count = 1;
            }
        }
        if (count > 1) res.add(new int[]{count, prev});
        else res.add(prev);
        return res.toArray();
    }
    public Object modified_encode(String alist) {
        List<Object> res = new ArrayList<>();
        if (alist == null || alist.length() == 0) return res.toArray(new String[0]);
        int count = 1;
        char prev = alist.charAt(0);
        for (int i = 1; i < alist.length(); i++) {
            if (alist.charAt(i) == prev) {
                count++;
            } else {
                if (count > 1) res.add(new Object[]{count, String.valueOf(prev)});
                else res.add(String.valueOf(prev));
                prev = alist.charAt(i);
                count = 1;
            }
        }
        if (count > 1) res.add(new Object[]{count, String.valueOf(prev)});
        else res.add(String.valueOf(prev));
        return res.toArray();
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    EncodeResult modified_encode(const vector<int>& alist);\\n    EncodeResult modified_encode(const string& alist);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <iostream>
using namespace std;

struct EncodeResult {
    string str_repr;
    vector<string> str_list;
    bool operator==(const vector<string>& v) const { return str_list == v; }
    friend ostream& operator<<(ostream& os, const EncodeResult& r) {
        os << r.str_repr;
        return os;
    }
};

class Solution {
public:
    EncodeResult modified_encode(const vector<int>& alist) {
        EncodeResult res;
        res.str_repr = "[";
        int count = 1;
        for (size_t i = 1; i <= alist.size(); ++i) {
            if (i < alist.size() && alist[i] == alist[i - 1]) {
                count++;
            } else {
                if (res.str_repr.size() > 1) res.str_repr += ", ";
                if (count > 1) res.str_repr += "[" + to_string(count) + ", " + to_string(alist[i - 1]) + "]";
                else res.str_repr += to_string(alist[i - 1]);
                count = 1;
            }
        }
        res.str_repr += "]";
        return res;
    }
    EncodeResult modified_encode(const string& alist) {
        EncodeResult res;
        res.str_repr = "[";
        int count = 1;
        for (size_t i = 1; i <= alist.size(); ++i) {
            if (i < alist.size() && alist[i] == alist[i - 1]) {
                count++;
            } else {
                if (res.str_repr.size() > 1) res.str_repr += ", ";
                if (count > 1) {
                    res.str_repr += "[" + to_string(count) + ", \\\"" + string(1, alist[i - 1]) + "\\\"]";
                    res.str_list.push_back("[" + to_string(count) + ", \\\"" + string(1, alist[i - 1]) + "\\\"]");
                } else {
                    res.str_repr += "\\\"" + string(1, alist[i - 1]) + "\\\"";
                    res.str_list.push_back(string(1, alist[i - 1]));
                }
                count = 1;
            }
        }
        res.str_repr += "]";
        return res;
    }
};"""
    },

    315: {
        "starter_code_java": "class Solution {\\n    public int max_volume(int s) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int max_volume(int s) {
        int maxvalue = 0;
        for (int i = 1; i < s - 1; i++) {
            for (int j = 1; j < s; j++) {
                int k = s - i - j;
                if (k > 0) {
                    maxvalue = Math.max(maxvalue, i * j * k);
                }
            }
        }
        return maxvalue;
    }
}"""
    },

    319: {
        "starter_code_javascript": "function position_min(list1) {\\n    return [];\\n}",
        "reference_solution_javascript": """function position_min(list1) {
    const minVal = Math.min(...list1);
    const res = [];
    for (let i = 0; i < list1.length; i++) {
        if (list1[i] === minVal) res.push(i);
    }
    return res;
}""",
        "starter_code_java": "class Solution {\\n    public int[] position_min(int[] list1) {\\n        return new int[]{};\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int[] position_min(int[] list1) {
        int minVal = Integer.MAX_VALUE;
        for (int x : list1) if (x < minVal) minVal = x;
        List<Integer> res = new ArrayList<>();
        for (int i = 0; i < list1.length; i++) {
            if (list1[i] == minVal) res.add(i);
        }
        int[] out = new int[res.size()];
        for (int i = 0; i < res.size(); i++) out[i] = res.get(i);
        return out;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<int> position_min(const vector<int>& list1);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    vector<int> position_min(const vector<int>& list1) {
        int minVal = *min_element(list1.begin(), list1.end());
        vector<int> res;
        for (size_t i = 0; i < list1.size(); ++i) {
            if (list1[i] == minVal) res.push_back(i);
        }
        return res;
    }
};"""
    },

    320: {
        "starter_code_java": "class Solution {\\n    public int[] re_arrange(int[] arr, int n) {\\n        return new int[]{};\\n    }\\n}",
        "reference_solution_java": """class Solution {
    private void right_rotate(int[] arr, int out_of_place, int cur) {
        int temp = arr[cur];
        for (int i = cur; i > out_of_place; i--) {
            arr[i] = arr[i - 1];
        }
        arr[out_of_place] = temp;
    }
    public int[] re_arrange(int[] arr, int n) {
        int[] res = arr.clone();
        int out_of_place = -1;
        for (int index = 0; index < n; index++) {
            if (out_of_place >= 0) {
                if ((res[index] >= 0 && res[out_of_place] < 0) ||
                    (res[index] < 0 && res[out_of_place] >= 0)) {
                    right_rotate(res, out_of_place, index);
                    if (index - out_of_place > 2) {
                        out_of_place += 2;
                    } else {
                        out_of_place = -1;
                    }
                }
            }
            if (out_of_place == -1) {
                if ((res[index] >= 0 && index % 2 == 0) ||
                    (res[index] < 0 && index % 2 == 1)) {
                    out_of_place = index;
                }
            }
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<int> re_arrange(vector<int> arr, int n);\\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
    void right_rotate(vector<int>& arr, int out_of_place, int cur) {
        int temp = arr[cur];
        for (int i = cur; i > out_of_place; i--) {
            arr[i] = arr[i - 1];
        }
        arr[out_of_place] = temp;
    }
public:
    vector<int> re_arrange(vector<int> arr, int n) {
        int out_of_place = -1;
        for (int index = 0; index < n; index++) {
            if (out_of_place >= 0) {
                if ((arr[index] >= 0 && arr[out_of_place] < 0) ||
                    (arr[index] < 0 && arr[out_of_place] >= 0)) {
                    right_rotate(arr, out_of_place, index);
                    if (index - out_of_place > 2) {
                        out_of_place += 2;
                    } else {
                        out_of_place = -1;
                    }
                }
            }
            if (out_of_place == -1) {
                if ((arr[index] >= 0 && index % 2 == 0) ||
                    (arr[index] < 0 && index % 2 == 1)) {
                    out_of_place = index;
                }
            }
        }
        return arr;
    }
};"""
    },

    322: {
        "starter_code_javascript": "function most_occurrences(test_list) {\\n    return \\"\\";\\n}",
        "reference_solution_javascript": """function most_occurrences(test_list) {
    const counts = {};
    for (const sub of test_list) {
        for (const wrd of sub.split(' ')) {
            counts[wrd] = (counts[wrd] || 0) + 1;
        }
    }
    let maxWord = "";
    let maxCount = -1;
    for (const [wrd, cnt] of Object.entries(counts)) {
        if (cnt > maxCount) {
            maxCount = cnt;
            maxWord = wrd;
        }
    }
    return maxWord;
}""",
        "starter_code_java": "class Solution {\\n    public String most_occurrences(String[] test_list) {\\n        return \\"\\";\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public String most_occurrences(String[] test_list) {
        Map<String, Integer> counts = new LinkedHashMap<>();
        for (String sub : test_list) {
            for (String wrd : sub.split("\\\\s+")) {
                counts.put(wrd, counts.getOrDefault(wrd, 0) + 1);
            }
        }
        String maxWord = "";
        int maxCount = -1;
        for (Map.Entry<String, Integer> e : counts.entrySet()) {
            if (e.getValue() > maxCount) {
                maxCount = e.getValue();
                maxWord = e.getKey();
            }
        }
        return maxWord;
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    string most_occurrences(const vector<string>& test_list);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <sstream>
#include <unordered_map>
using namespace std;
class Solution {
public:
    string most_occurrences(const vector<string>& test_list) {
        unordered_map<string, int> counts;
        vector<string> order;
        for (const auto& sub : test_list) {
            stringstream ss(sub);
            string wrd;
            while (ss >> wrd) {
                if (counts.find(wrd) == counts.end()) order.push_back(wrd);
                counts[wrd]++;
            }
        }
        string maxWord = "";
        int maxCount = -1;
        for (const auto& w : order) {
            if (counts[w] > maxCount) {
                maxCount = counts[w];
                maxWord = w;
            }
        }
        return maxWord;
    }
};"""
    },

    324: {
        "starter_code_javascript": "function rotate_left(list1, m, n) {\\n    return [];\\n}",
        "reference_solution_javascript": """function rotate_left(list1, m, n) {
    return list1.slice(m).concat(list1.slice(0, n));
}""",
        "starter_code_java": "class Solution {\\n    public int[] rotate_left(int[] list1, int m, int n) {\\n        return new int[]{};\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int[] rotate_left(int[] list1, int m, int n) {
        int len1 = list1.length - m;
        int len2 = n;
        int[] res = new int[len1 + len2];
        System.arraycopy(list1, m, res, 0, len1);
        System.arraycopy(list1, 0, res, len1, len2);
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<int> rotate_left(const vector<int>& list1, int m, int n);\\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    vector<int> rotate_left(const vector<int>& list1, int m, int n) {
        vector<int> res(list1.begin() + m, list1.end());
        res.insert(res.end(), list1.begin(), list1.begin() + n);
        return res;
    }
};"""
    },

    328: {
        "starter_code_java": "import java.util.*;\\nclass Solution {\\n    public Map<String, Integer> char_frequency(String str1) {\\n        return new HashMap<>();\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public Map<String, Integer> char_frequency(String str1) {
        Map<String, Integer> res = new LinkedHashMap<>();
        for (char c : str1.toCharArray()) {
            String s = String.valueOf(c);
            res.put(s, res.getOrDefault(s, 0) + 1);
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <string>\\n#include <unordered_map>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    unordered_map<string, int> char_frequency(const string& str1);\\n};",
        "reference_solution_cpp": """#include <string>
#include <unordered_map>
using namespace std;
class Solution {
public:
    unordered_map<string, int> char_frequency(const string& str1) {
        unordered_map<string, int> res;
        for (char c : str1) {
            res[string(1, c)]++;
        }
        return res;
    }
};"""
    },

    329: {
        "starter_code_javascript": "function Sort(sub_li) {\\n    return [];\\n}",
        "reference_solution_javascript": """function Sort(sub_li) {
    return [...sub_li].sort((a, b) => {
        let va = Number(a[1]);
        let vb = Number(b[1]);
        return va - vb;
    });
}""",
        "starter_code_java": "class Solution {\\n    public Object[][] Sort(Object[][] sub_li) {\\n        return new Object[][]{};\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public Object[][] Sort(Object[][] sub_li) {
        Object[][] res = sub_li.clone();
        Arrays.sort(res, (a, b) -> {
            int va = Integer.parseInt(String.valueOf(a[1]));
            int vb = Integer.parseInt(String.valueOf(b[1]));
            return Integer.compare(va, vb);
        });
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<vector<string>> Sort(vector<vector<string>> sub_li);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <algorithm>
using namespace std;
class Solution {
public:
    vector<vector<string>> Sort(vector<vector<string>> sub_li) {
        sort(sub_li.begin(), sub_li.end(), [](const vector<string>& a, const vector<string>& b) {
            return stoi(a[1]) < stoi(b[1]);
        });
        return sub_li;
    }
};"""
    },

    334: {
        "starter_code_java": "class Solution {\\n    public int count_Substring_With_Equal_Ends(String s) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int count_Substring_With_Equal_Ends(String s) {
        int result = 0;
        int n = s.length();
        for (int i = 0; i < n; i++) {
            for (int j = 1; j <= n - i; j++) {
                if (s.charAt(i) == s.charAt(i + j - 1)) {
                    result++;
                }
            }
        }
        return result;
    }
}""",
        "starter_code_cpp": "#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int count_Substring_With_Equal_Ends(const string& s);\\n};",
        "reference_solution_cpp": """#include <string>
using namespace std;
class Solution {
public:
    int count_Substring_With_Equal_Ends(const string& s) {
        int result = 0;
        int n = s.length();
        for (int i = 0; i < n; i++) {
            for (int j = 1; j <= n - i; j++) {
                if (s[i] == s[i + j - 1]) {
                    result++;
                }
            }
        }
        return result;
    }
};"""
    },

    336: {
        "starter_code_java": "class Solution {\\n    public int sum_three_smallest_nums(int[] lst) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int sum_three_smallest_nums(int[] lst) {
        List<Integer> pos = new ArrayList<>();
        for (int x : lst) if (x > 0) pos.add(x);
        Collections.sort(pos);
        int sum = 0;
        for (int i = 0; i < Math.min(3, pos.size()); i++) sum += pos.get(i);
        return sum;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int sum_three_smallest_nums(const vector<int>& lst);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    int sum_three_smallest_nums(const vector<int>& lst) {
        vector<int> pos;
        for (int x : lst) if (x > 0) pos.push_back(x);
        sort(pos.begin(), pos.end());
        int sum = 0;
        int limit = min((int)pos.size(), 3);
        for (int i = 0; i < limit; i++) sum += pos[i];
        return sum;
    }
};"""
    },

    338: {
        "starter_code_javascript": "function diff_consecutivenums(nums) {\\n    return [];\\n}",
        "reference_solution_javascript": """function diff_consecutivenums(nums) {
    const res = [];
    for (let i = 1; i < nums.length; i++) {
        res.push(nums[i] - nums[i - 1]);
    }
    return res;
}""",
        "starter_code_java": "class Solution {\\n    public int[] diff_consecutivenums(int[] nums) {\\n        return new int[]{};\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int[] diff_consecutivenums(int[] nums) {
        if (nums.length <= 1) return new int[]{};
        int[] res = new int[nums.length - 1];
        for (int i = 1; i < nums.length; i++) {
            res[i - 1] = nums[i] - nums[i - 1];
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<int> diff_consecutivenums(const vector<int>& nums);\\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    vector<int> diff_consecutivenums(const vector<int>& nums) {
        if (nums.size() <= 1) return {};
        vector<int> res;
        for (size_t i = 1; i < nums.size(); ++i) {
            res.push_back(nums[i] - nums[i - 1]);
        }
        return res;
    }
};"""
    },

    342: {
        "starter_code_javascript": "function check(string) {\\n    return \\"No\\";\\n}",
        "reference_solution_javascript": """function check(string) {
    if (!string || string.length === 0) return "No";
    for (let i = 0; i < string.length; i++) {
        if (string[i] !== '0' && string[i] !== '1') return "No";
    }
    return "Yes";
}""",
        "starter_code_java": "class Solution {\\n    public String check(String string) {\\n        return \\"No\\";\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public String check(String string) {
        if (string == null || string.isEmpty()) return "No";
        for (int i = 0; i < string.length(); i++) {
            char c = string.charAt(i);
            if (c != '0' && c != '1') return "No";
        }
        return "Yes";
    }
}""",
        "starter_code_cpp": "#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    string check(const string& string_val);\\n};",
        "reference_solution_cpp": """#include <string>
using namespace std;
class Solution {
public:
    string check(const string& string_val) {
        if (string_val.empty()) return "No";
        for (char c : string_val) {
            if (c != '0' && c != '1') return "No";
        }
        return "Yes";
    }
};"""
    },

    343: {
        "starter_code_java": "class Solution {\\n    public int minimum_Length(String s) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int minimum_Length(String s) {
        int[] arr = new int[26];
        int maxOcc = 0;
        int n = s.length();
        for (int i = 0; i < n; i++) {
            arr[s.charAt(i) - 'a']++;
        }
        for (int i = 0; i < 26; i++) {
            if (arr[i] > maxOcc) maxOcc = arr[i];
        }
        return n - maxOcc;
    }
}""",
        "starter_code_cpp": "#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int minimum_Length(const string& s);\\n};",
        "reference_solution_cpp": """#include <string>
#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    int minimum_Length(const string& s) {
        vector<int> arr(26, 0);
        int maxOcc = 0;
        int n = s.length();
        for (char c : s) {
            arr[c - 'a']++;
        }
        for (int count : arr) {
            maxOcc = max(maxOcc, count);
        }
        return n - maxOcc;
    }
};"""
    },

    344: {
        "starter_code_javascript": "function first_Element(arr, n, k) {\\n    return -1;\\n}",
        "reference_solution_javascript": """function first_Element(arr, n, k) {
    const count_map = {};
    for (let i = 0; i < n; i++) {
        count_map[arr[i]] = (count_map[arr[i]] || 0) + 1;
    }
    for (let i = 0; i < n; i++) {
        if (count_map[arr[i]] === k) return arr[i];
    }
    return -1;
}""",
        "starter_code_java": "class Solution {\\n    public int first_Element(int[] arr, int n, int k) {\\n        return -1;\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int first_Element(int[] arr, int n, int k) {
        Map<Integer, Integer> map = new HashMap<>();
        for (int i = 0; i < n; i++) {
            map.put(arr[i], map.getOrDefault(arr[i], 0) + 1);
        }
        for (int i = 0; i < n; i++) {
            if (map.get(arr[i]) == k) return arr[i];
        }
        return -1;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int first_Element(const vector<int>& arr, int n, int k);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <unordered_map>
using namespace std;
class Solution {
public:
    int first_Element(const vector<int>& arr, int n, int k) {
        unordered_map<int, int> count_map;
        for (int i = 0; i < n; ++i) {
            count_map[arr[i]]++;
        }
        for (int i = 0; i < n; ++i) {
            if (count_map[arr[i]] == k) return arr[i];
        }
        return -1;
    }
};"""
    },

    345: {
        "starter_code_java": "class Solution {\\n    public boolean unique_Characters(String str) {\\n        return false;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public boolean unique_Characters(String str) {
        for (int i = 0; i < str.length(); i++) {
            for (int j = i + 1; j < str.length(); j++) {
                if (str.charAt(i) == str.charAt(j)) return false;
            }
        }
        return true;
    }
}"""
    },

    346: {
        "starter_code_javascript": "function remove_column(list1, n) {\\n    return [];\\n}",
        "reference_solution_javascript": """function remove_column(list1, n) {
    return list1.map(row => row.filter((_, idx) => idx !== n));
}""",
        "starter_code_java": "class Solution {\\n    public int[][] remove_column(int[][] list1, int n) {\\n        return new int[][]{};\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int[][] remove_column(int[][] list1, int n) {
        int rows = list1.length;
        int[][] res = new int[rows][];
        for (int i = 0; i < rows; i++) {
            int cols = list1[i].length;
            res[i] = new int[cols - 1];
            int c = 0;
            for (int j = 0; j < cols; j++) {
                if (j != n) {
                    res[i][c++] = list1[i][j];
                }
            }
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<vector<int>> remove_column(vector<vector<int>> list1, int n);\\n};",
        "reference_solution_cpp": """#include <vector>
using namespace std;
class Solution {
public:
    vector<vector<int>> remove_column(vector<vector<int>> list1, int n) {
        for (auto& row : list1) {
            if (n < (int)row.size()) {
                row.erase(row.begin() + n);
            }
        }
        return list1;
    }
};"""
    },

    350: {
        "starter_code_javascript": "function find_max(test_list) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function find_max(test_list) {
    let maxVal = -Infinity;
    for (const row of test_list) {
        for (const item of row) {
            maxVal = Math.max(maxVal, Number(item));
        }
    }
    return maxVal;
}""",
        "starter_code_java": "class Solution {\\n    public int find_max(int[][] test_list) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int find_max(int[][] test_list) {
        int maxVal = Integer.MIN_VALUE;
        for (int[] row : test_list) {
            for (int x : row) {
                if (x > maxVal) maxVal = x;
            }
        }
        return maxVal;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int find_max(const vector<vector<int>>& test_list);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    int find_max(const vector<vector<int>>& test_list) {
        int maxVal = -2147483648;
        for (const auto& row : test_list) {
            for (int x : row) {
                maxVal = max(maxVal, x);
            }
        }
        return maxVal;
    }
};"""
    },

    351: {
        "starter_code_javascript": "function moddiv_list(nums1, nums2) {\\n    return [];\\n}",
        "reference_solution_javascript": """function moddiv_list(nums1, nums2) {
    const res = [];
    const len = Math.min(nums1.length, nums2.length);
    for (let i = 0; i < len; i++) {
        res.push(nums1[i] % nums2[i]);
    }
    return res;
}""",
        "starter_code_java": "class Solution {\\n    public int[] moddiv_list(int[] nums1, int[] nums2) {\\n        return new int[]{};\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int[] moddiv_list(int[] nums1, int[] nums2) {
        int len = Math.min(nums1.length, nums2.length);
        int[] res = new int[len];
        for (int i = 0; i < len; i++) {
            res[i] = nums1[i] % nums2[i];
        }
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<int> moddiv_list(const vector<int>& nums1, const vector<int>& nums2);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    vector<int> moddiv_list(const vector<int>& nums1, const vector<int>& nums2) {
        size_t len = min(nums1.size(), nums2.size());
        vector<int> res(len);
        for (size_t i = 0; i < len; ++i) {
            res[i] = nums1[i] % nums2[i];
        }
        return res;
    }
};"""
    },

    354: {
        "starter_code_javascript": "function remove_empty(list1) {\\n    return [];\\n}",
        "reference_solution_javascript": """function remove_empty(list1) {
    return list1.filter(x => {
        if (Array.isArray(x)) return x.length > 0;
        return Boolean(x);
    });
}""",
        "starter_code_java": "class Solution {\\n    public Object[] remove_empty(Object[] list1) {\\n        return new Object[]{};\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public Object[] remove_empty(Object[] list1) {
        List<Object> res = new ArrayList<>();
        for (Object x : list1) {
            if (x instanceof Object[]) {
                if (((Object[]) x).length > 0) res.add(x);
            } else if (x instanceof int[]) {
                if (((int[]) x).length > 0) res.add(x);
            } else if (x instanceof String) {
                if (!((String) x).isEmpty()) res.add(x);
            } else if (x != null) {
                res.add(x);
            }
        }
        return res.toArray();
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<string> remove_empty(const vector<string>& list1);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
using namespace std;
class Solution {
public:
    vector<string> remove_empty(const vector<string>& list1) {
        vector<string> res;
        for (const auto& s : list1) {
            if (!s.empty() && s != "[]") res.push_back(s);
        }
        return res;
    }
};"""
    },

    355: {
        "starter_code_java": "class Solution {\\n    public int max_occurrences(int[] nums) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public int max_occurrences(int[] nums) {
        Map<Integer, Integer> map = new LinkedHashMap<>();
        int maxVal = 0;
        int result = nums[0];
        for (int i : nums) {
            int occu = map.getOrDefault(i, 0) + 1;
            map.put(i, occu);
            if (occu > maxVal) {
                maxVal = occu;
                result = i;
            }
        }
        return result;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int max_occurrences(const vector<int>& nums);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <unordered_map>
using namespace std;
class Solution {
public:
    int max_occurrences(const vector<int>& nums) {
        unordered_map<int, int> counts;
        int maxVal = 0;
        int result = nums[0];
        for (int x : nums) {
            counts[x]++;
            if (counts[x] > maxVal) {
                maxVal = counts[x];
                result = x;
            }
        }
        return result;
    }
};"""
    },

    356: {
        "starter_code_java": "class Solution {\\n    public int min_flip_to_make_string_alternate(String str) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    private int get_flip(String str, char expected) {
        int flip_count = 0;
        for (int i = 0; i < str.length(); i++) {
            if (str.charAt(i) != expected) flip_count++;
            expected = (expected == '0') ? '1' : '0';
        }
        return flip_count;
    }
    public int min_flip_to_make_string_alternate(String str) {
        return Math.min(get_flip(str, '0'), get_flip(str, '1'));
    }
}""",
        "starter_code_cpp": "#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int min_flip_to_make_string_alternate(const string& str);\\n};",
        "reference_solution_cpp": """#include <string>
#include <algorithm>
using namespace std;
class Solution {
    int get_flip(const string& str, char expected) {
        int flip_count = 0;
        for (char c : str) {
            if (c != expected) flip_count++;
            expected = (expected == '0') ? '1' : '0';
        }
        return flip_count;
    }
public:
    int min_flip_to_make_string_alternate(const string& str) {
        return min(get_flip(str, '0'), get_flip(str, '1'));
    }
};"""
    },

    358: {
        "starter_code_javascript": "function adjacent_num_product(list_nums) {\\n    return 0;\\n}",
        "reference_solution_javascript": """function adjacent_num_product(list_nums) {
    let maxProd = -Infinity;
    for (let i = 1; i < list_nums.length; i++) {
        maxProd = Math.max(maxProd, list_nums[i] * list_nums[i - 1]);
    }
    return maxProd;
}""",
        "starter_code_java": "class Solution {\\n    public int adjacent_num_product(int[] list_nums) {\\n        return 0;\\n    }\\n}",
        "reference_solution_java": """class Solution {
    public int adjacent_num_product(int[] list_nums) {
        int maxProd = Integer.MIN_VALUE;
        for (int i = 1; i < list_nums.length; i++) {
            maxProd = Math.max(maxProd, list_nums[i] * list_nums[i - 1]);
        }
        return maxProd;
    }
}""",
        "starter_code_cpp": "#include <vector>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    int adjacent_num_product(const vector<int>& list_nums);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    int adjacent_num_product(const vector<int>& list_nums) {
        int maxProd = -2147483648;
        for (size_t i = 1; i < list_nums.size(); ++i) {
            maxProd = max(maxProd, list_nums[i] * list_nums[i - 1]);
        }
        return maxProd;
    }
};"""
    },

    360: {
        "starter_code_java": "class Solution {\\n    public String[][] float_sort(String[][] price) {\\n        return new String[][]{};\\n    }\\n}",
        "reference_solution_java": """import java.util.*;
class Solution {
    public String[][] float_sort(String[][] price) {
        String[][] res = price.clone();
        Arrays.sort(res, (a, b) -> Double.compare(Double.parseDouble(b[1]), Double.parseDouble(a[1])));
        return res;
    }
}""",
        "starter_code_cpp": "#include <vector>\\n#include <string>\\nusing namespace std;\\nclass Solution {\\npublic:\\n    vector<vector<string>> float_sort(vector<vector<string>> price);\\n};",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <algorithm>
using namespace std;
class Solution {
public:
    vector<vector<string>> float_sort(vector<vector<string>> price) {
        sort(price.begin(), price.end(), [](const vector<string>& a, const vector<string>& b) {
            return stod(a[1]) > stod(b[1]);
        });
        return price;
    }
};"""
    }
}
'''

with open(os.path.join(os.path.dirname(__file__), "batch6_solutions.py"), "w", encoding="utf-8") as f:
    f.write(BATCH6_CONTENT)
print("batch6_solutions.py generated successfully.")
