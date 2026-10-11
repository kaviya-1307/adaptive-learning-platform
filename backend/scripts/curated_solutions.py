"""
Curated Multi-Language Solutions for Problems 4..40 (Excluding existing 10).
Contains verified implementations in Java, C++, and JavaScript.
"""

CURATED_30 = {
    4: {
        "starter_code_java": """class Solution {
    public int[] productExceptSelf(int[] nums) {
        // Write your solution here
        return new int[]{};
    }
}""",
        "reference_solution_java": """class Solution {
    public int[] productExceptSelf(int[] nums) {
        int n = nums.length;
        int[] res = new int[n];
        res[0] = 1;
        for (int i = 1; i < n; i++) res[i] = res[i - 1] * nums[i - 1];
        int right = 1;
        for (int i = n - 1; i >= 0; i--) {
            res[i] *= right;
            right *= nums[i];
        }
        return res;
    }
}""",
        "starter_code_cpp": """#include <vector>
using namespace std;

class Solution {
public:
    vector<int> productExceptSelf(vector<int>& nums) {
        // Write your solution here
        return {};
    }
};""",
        "reference_solution_cpp": """#include <vector>
using namespace std;

class Solution {
public:
    vector<int> productExceptSelf(vector<int>& nums) {
        int n = nums.size();
        vector<int> res(n, 1);
        for (int i = 1; i < n; ++i) res[i] = res[i - 1] * nums[i - 1];
        int right = 1;
        for (int i = n - 1; i >= 0; --i) {
            res[i] *= right;
            right *= nums[i];
        }
        return res;
    }
};""",
        "starter_code_javascript": """/**
 * @param {number[]} nums
 * @return {number[]}
 */
function productExceptSelf(nums) {
    // Write your solution here
    return [];
}""",
        "reference_solution_javascript": """function productExceptSelf(nums) {
    const n = nums.length;
    const res = new Array(n).fill(1);
    for (let i = 1; i < n; i++) res[i] = res[i - 1] * nums[i - 1];
    let right = 1;
    for (let i = n - 1; i >= 0; i--) {
        res[i] *= right;
        right *= nums[i];
    }
    return res;
}"""
    },

    5: {
        "starter_code_java": """class Solution {
    public int trap(int[] height) {
        // Write your solution here
        return 0;
    }
}""",
        "reference_solution_java": """class Solution {
    public int trap(int[] height) {
        if (height == null || height.length == 0) return 0;
        int l = 0, r = height.length - 1;
        int lMax = height[l], rMax = height[r], res = 0;
        while (l < r) {
            if (lMax < rMax) {
                l++;
                lMax = Math.max(lMax, height[l]);
                res += lMax - height[l];
            } else {
                r--;
                rMax = Math.max(rMax, height[r]);
                res += rMax - height[r];
            }
        }
        return res;
    }
}""",
        "starter_code_cpp": """#include <vector>
using namespace std;

class Solution {
public:
    int trap(vector<int>& height) {
        // Write your solution here
        return 0;
    }
};""",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int trap(vector<int>& height) {
        if (height.empty()) return 0;
        int l = 0, r = (int)height.size() - 1;
        int lMax = height[l], rMax = height[r], res = 0;
        while (l < r) {
            if (lMax < rMax) {
                l++;
                lMax = max(lMax, height[l]);
                res += lMax - height[l];
            } else {
                r--;
                rMax = max(rMax, height[r]);
                res += rMax - height[r];
            }
        }
        return res;
    }
};""",
        "starter_code_javascript": """/**
 * @param {number[]} height
 * @return {number}
 */
function trap(height) {
    // Write your solution here
    return 0;
}""",
        "reference_solution_javascript": """function trap(height) {
    if (!height || height.length === 0) return 0;
    let l = 0, r = height.length - 1;
    let lMax = height[l], rMax = height[r], res = 0;
    while (l < r) {
        if (lMax < rMax) {
            l++;
            lMax = Math.max(lMax, height[l]);
            res += lMax - height[l];
        } else {
            r--;
            rMax = Math.max(rMax, height[r]);
            res += rMax - height[r];
        }
    }
    return res;
}"""
    },

    8: {
        "starter_code_java": """class Solution {
    public int lengthOfLongestSubstring(String s) {
        // Write your solution here
        return 0;
    }
}""",
        "reference_solution_java": """import java.util.*;

class Solution {
    public int lengthOfLongestSubstring(String s) {
        Set<Character> set = new HashSet<>();
        int l = 0, res = 0;
        for (int r = 0; r < s.length(); r++) {
            while (set.contains(s.charAt(r))) {
                set.remove(s.charAt(l++));
            }
            set.add(s.charAt(r));
            res = Math.max(res, r - l + 1);
        }
        return res;
    }
}""",
        "starter_code_cpp": """#include <string>
using namespace std;

class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        // Write your solution here
        return 0;
    }
};""",
        "reference_solution_cpp": """#include <string>
#include <unordered_set>
#include <algorithm>
using namespace std;

class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        unordered_set<char> set;
        int l = 0, res = 0;
        for (int r = 0; r < (int)s.size(); ++r) {
            while (set.count(s[r])) {
                set.erase(s[l++]);
            }
            set.insert(s[r]);
            res = max(res, r - l + 1);
        }
        return res;
    }
};""",
        "starter_code_javascript": """/**
 * @param {string} s
 * @return {number}
 */
function lengthOfLongestSubstring(s) {
    // Write your solution here
    return 0;
}""",
        "reference_solution_javascript": """function lengthOfLongestSubstring(s) {
    const charSet = new Set();
    let l = 0, res = 0;
    for (let r = 0; r < s.length; r++) {
        while (charSet.has(s[r])) {
            charSet.delete(s[l++]);
        }
        charSet.add(s[r]);
        res = Math.max(res, r - l + 1);
    }
    return res;
}"""
    },

    9: {
        "starter_code_java": """class Solution {
    public String[][] groupAnagrams(String[] strs) {
        // Write your solution here
        return new String[][]{};
    }
}""",
        "reference_solution_java": """import java.util.*;

class Solution {
    public String[][] groupAnagrams(String[] strs) {
        Map<String, List<String>> map = new HashMap<>();
        for (String s : strs) {
            char[] ca = s.toCharArray();
            Arrays.sort(ca);
            String key = new String(ca);
            map.computeIfAbsent(key, k -> new ArrayList<>()).add(s);
        }
        List<String[]> list = new ArrayList<>();
        for (List<String> group : map.values()) {
            Collections.sort(group);
            list.add(group.toArray(new String[0]));
        }
        list.sort((a, b) -> (a.length > 0 && b.length > 0 ? a[0].compareTo(b[0]) : 0));
        return list.toArray(new String[0][]);
    }
}""",
        "starter_code_cpp": """#include <vector>
#include <string>
using namespace std;

class Solution {
public:
    vector<vector<string>> groupAnagrams(vector<string>& strs) {
        // Write your solution here
        return {};
    }
};""",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <unordered_map>
#include <algorithm>
using namespace std;

class Solution {
public:
    vector<vector<string>> groupAnagrams(vector<string>& strs) {
        unordered_map<string, vector<string>> map;
        for (const string& s : strs) {
            string key = s;
            sort(key.begin(), key.end());
            map[key].push_back(s);
        }
        vector<vector<string>> res;
        for (auto& pair : map) {
            sort(pair.second.begin(), pair.second.end());
            res.push_back(pair.second);
        }
        sort(res.begin(), res.end(), [](const vector<string>& a, const vector<string>& b) {
            return !a.empty() && !b.empty() && a[0] < b[0];
        });
        return res;
    }
};""",
        "starter_code_javascript": """/**
 * @param {string[]} strs
 * @return {string[][]}
 */
function groupAnagrams(strs) {
    // Write your solution here
    return [];
}""",
        "reference_solution_javascript": """function groupAnagrams(strs) {
    const map = new Map();
    for (const s of strs) {
        const key = s.split('').sort().join('');
        if (!map.has(key)) map.set(key, []);
        map.get(key).push(s);
    }
    const res = Array.from(map.values()).map(g => g.sort());
    res.sort((a, b) => (a[0] || '').localeCompare(b[0] || ''));
    return res;
}"""
    },

    11: {
        "starter_code_java": """class Solution {
    public boolean containsDuplicate(int[] nums) {
        // Write your solution here
        return false;
    }
}""",
        "reference_solution_java": """import java.util.*;

class Solution {
    public boolean containsDuplicate(int[] nums) {
        Set<Integer> set = new HashSet<>();
        for (int n : nums) {
            if (!set.add(n)) return true;
        }
        return false;
    }
}""",
        "starter_code_cpp": """#include <vector>
using namespace std;

class Solution {
public:
    bool containsDuplicate(vector<int>& nums) {
        // Write your solution here
        return false;
    }
};""",
        "reference_solution_cpp": """#include <vector>
#include <unordered_set>
using namespace std;

class Solution {
public:
    bool containsDuplicate(vector<int>& nums) {
        unordered_set<int> set;
        for (int n : nums) {
            if (set.count(n)) return true;
            set.insert(n);
        }
        return false;
    }
};""",
        "starter_code_javascript": """/**
 * @param {number[]} nums
 * @return {boolean}
 */
function containsDuplicate(nums) {
    // Write your solution here
    return false;
}""",
        "reference_solution_javascript": """function containsDuplicate(nums) {
    return new Set(nums).size !== nums.length;
}"""
    },

    12: {
        "starter_code_java": """class Solution {
    public int[] topKFrequent(int[] nums, int k) {
        // Write your solution here
        return new int[]{};
    }
}""",
        "reference_solution_java": """import java.util.*;

class Solution {
    public int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> count = new HashMap<>();
        for (int n : nums) count.put(n, count.getOrDefault(n, 0) + 1);
        PriorityQueue<Integer> pq = new PriorityQueue<>((a, b) -> count.get(b) - count.get(a));
        pq.addAll(count.keySet());
        int[] res = new int[k];
        for (int i = 0; i < k; i++) res[i] = pq.poll();
        Arrays.sort(res);
        return res;
    }
}""",
        "starter_code_cpp": """#include <vector>
using namespace std;

class Solution {
public:
    vector<int> topKFrequent(vector<int>& nums, int k) {
        // Write your solution here
        return {};
    }
};""",
        "reference_solution_cpp": """#include <vector>
#include <unordered_map>
#include <queue>
#include <algorithm>
using namespace std;

class Solution {
public:
    vector<int> topKFrequent(vector<int>& nums, int k) {
        unordered_map<int, int> count;
        for (int n : nums) count[n]++;
        auto comp = [&](int a, int b) { return count[a] > count[b]; };
        priority_queue<int, vector<int>, decltype(comp)> pq(comp);
        for (auto& p : count) {
            pq.push(p.first);
            if ((int)pq.size() > k) pq.pop();
        }
        vector<int> res;
        while (!pq.empty()) { res.push_back(pq.top()); pq.pop(); }
        sort(res.begin(), res.end());
        return res;
    }
};""",
        "starter_code_javascript": """/**
 * @param {number[]} nums
 * @param {number} k
 * @return {number[]}
 */
function topKFrequent(nums, k) {
    // Write your solution here
    return [];
}""",
        "reference_solution_javascript": """function topKFrequent(nums, k) {
    const map = new Map();
    for (const n of nums) map.set(n, (map.get(n) || 0) + 1);
    const sorted = Array.from(map.entries()).sort((a, b) => b[1] - a[1]);
    return sorted.slice(0, k).map(e => e[0]).sort((a, b) => a - b);
}"""
    },

    13: {
        "starter_code_java": """class Solution {
    public int longestConsecutive(int[] nums) {
        // Write your solution here
        return 0;
    }
}""",
        "reference_solution_java": """import java.util.*;

class Solution {
    public int longestConsecutive(int[] nums) {
        Set<Integer> set = new HashSet<>();
        for (int n : nums) set.add(n);
        int longest = 0;
        for (int n : set) {
            if (!set.contains(n - 1)) {
                int curr = n, len = 1;
                while (set.contains(curr + 1)) {
                    curr++;
                    len++;
                }
                longest = Math.max(longest, len);
            }
        }
        return longest;
    }
}""",
        "starter_code_cpp": """#include <vector>
using namespace std;

class Solution {
public:
    int longestConsecutive(vector<int>& nums) {
        // Write your solution here
        return 0;
    }
};""",
        "reference_solution_cpp": """#include <vector>
#include <unordered_set>
#include <algorithm>
using namespace std;

class Solution {
public:
    int longestConsecutive(vector<int>& nums) {
        unordered_set<int> set(nums.begin(), nums.end());
        int longest = 0;
        for (int n : set) {
            if (!set.count(n - 1)) {
                int curr = n, len = 1;
                while (set.count(curr + 1)) {
                    curr++;
                    len++;
                }
                longest = max(longest, len);
            }
        }
        return longest;
    }
};""",
        "starter_code_javascript": """/**
 * @param {number[]} nums
 * @return {number}
 */
function longestConsecutive(nums) {
    // Write your solution here
    return 0;
}""",
        "reference_solution_javascript": """function longestConsecutive(nums) {
    const numSet = new Set(nums);
    let longest = 0;
    for (const n of numSet) {
        if (!numSet.has(n - 1)) {
            let curr = n, len = 1;
            while (numSet.has(curr + 1)) {
                curr++;
                len++;
            }
            longest = Math.max(longest, len);
        }
    }
    return longest;
}"""
    },

    14: {
        "starter_code_java": """class Solution {
    public int[] reverseList(int[] head) {
        // Write your solution here
        return new int[]{};
    }
}""",
        "reference_solution_java": """class Solution {
    public int[] reverseList(int[] head) {
        if (head == null) return new int[]{};
        int n = head.length;
        int[] res = new int[n];
        for (int i = 0; i < n; i++) res[i] = head[n - 1 - i];
        return res;
    }
}""",
        "starter_code_cpp": """#include <vector>
using namespace std;

class Solution {
public:
    vector<int> reverseList(vector<int>& head) {
        // Write your solution here
        return {};
    }
};""",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    vector<int> reverseList(vector<int>& head) {
        vector<int> res = head;
        reverse(res.begin(), res.end());
        return res;
    }
};""",
        "starter_code_javascript": """/**
 * @param {number[]} head
 * @return {number[]}
 */
function reverseList(head) {
    // Write your solution here
    return [];
}""",
        "reference_solution_javascript": """function reverseList(head) {
    return [...head].reverse();
}"""
    },

    15: {
        "starter_code_java": """class Solution {
    public int[] mergeTwoLists(int[] list1, int[] list2) {
        // Write your solution here
        return new int[]{};
    }
}""",
        "reference_solution_java": """class Solution {
    public int[] mergeTwoLists(int[] list1, int[] list2) {
        int n1 = list1.length, n2 = list2.length;
        int[] res = new int[n1 + n2];
        int i = 0, j = 0, k = 0;
        while (i < n1 && j < n2) {
            if (list1[i] <= list2[j]) res[k++] = list1[i++];
            else res[k++] = list2[j++];
        }
        while (i < n1) res[k++] = list1[i++];
        while (j < n2) res[k++] = list2[j++];
        return res;
    }
}""",
        "starter_code_cpp": """#include <vector>
using namespace std;

class Solution {
public:
    vector<int> mergeTwoLists(vector<int>& list1, vector<int>& list2) {
        // Write your solution here
        return {};
    }
};""",
        "reference_solution_cpp": """#include <vector>
using namespace std;

class Solution {
public:
    vector<int> mergeTwoLists(vector<int>& list1, vector<int>& list2) {
        vector<int> res;
        int i = 0, j = 0;
        while (i < (int)list1.size() && j < (int)list2.size()) {
            if (list1[i] <= list2[j]) res.push_back(list1[i++]);
            else res.push_back(list2[j++]);
        }
        while (i < (int)list1.size()) res.push_back(list1[i++]);
        while (j < (int)list2.size()) res.push_back(list2[j++]);
        return res;
    }
};""",
        "starter_code_javascript": """/**
 * @param {number[]} list1
 * @param {number[]} list2
 * @return {number[]}
 */
function mergeTwoLists(list1, list2) {
    // Write your solution here
    return [];
}""",
        "reference_solution_javascript": """function mergeTwoLists(list1, list2) {
    const res = [];
    let i = 0, j = 0;
    while (i < list1.length && j < list2.length) {
        if (list1[i] <= list2[j]) res.push(list1[i++]);
        else res.push(list2[j++]);
    }
    while (i < list1.length) res.push(list1[i++]);
    while (j < list2.length) res.push(list2[j++]);
    return res;
}"""
    },

    16: {
        "starter_code_java": """class Solution {
    public int[] removeNthFromEnd(int[] head, int n) {
        // Write your solution here
        return new int[]{};
    }
}""",
        "reference_solution_java": """class Solution {
    public int[] removeNthFromEnd(int[] head, int n) {
        int len = head.length;
        if (len <= 1) return new int[]{};
        int target = len - n;
        int[] res = new int[len - 1];
        int k = 0;
        for (int i = 0; i < len; i++) {
            if (i != target) res[k++] = head[i];
        }
        return res;
    }
}""",
        "starter_code_cpp": """#include <vector>
using namespace std;

class Solution {
public:
    vector<int> removeNthFromEnd(vector<int>& head, int n) {
        // Write your solution here
        return {};
    }
};""",
        "reference_solution_cpp": """#include <vector>
using namespace std;

class Solution {
public:
    vector<int> removeNthFromEnd(vector<int>& head, int n) {
        int len = head.size();
        if (len <= 1) return {};
        int target = len - n;
        vector<int> res;
        for (int i = 0; i < len; ++i) {
            if (i != target) res.push_back(head[i]);
        }
        return res;
    }
};""",
        "starter_code_javascript": """/**
 * @param {number[]} head
 * @param {number} n
 * @return {number[]}
 */
function removeNthFromEnd(head, n) {
    // Write your solution here
    return [];
}""",
        "reference_solution_javascript": """function removeNthFromEnd(head, n) {
    const target = head.length - n;
    return head.filter((_, idx) => idx !== target);
}"""
    },

    17: {
        "starter_code_java": """class Solution {
    public boolean isValid(String s) {
        // Write your solution here
        return false;
    }
}""",
        "reference_solution_java": """import java.util.Stack;

class Solution {
    public boolean isValid(String s) {
        Stack<Character> stack = new Stack<>();
        for (char c : s.toCharArray()) {
            if (c == '(') stack.push(')');
            else if (c == '{') stack.push('}');
            else if (c == '[') stack.push(']');
            else if (stack.isEmpty() || stack.pop() != c) return false;
        }
        return stack.isEmpty();
    }
}""",
        "starter_code_cpp": """#include <string>
using namespace std;

class Solution {
public:
    bool isValid(string s) {
        // Write your solution here
        return false;
    }
};""",
        "reference_solution_cpp": """#include <string>
#include <stack>
using namespace std;

class Solution {
public:
    bool isValid(string s) {
        stack<char> st;
        for (char c : s) {
            if (c == '(') st.push(')');
            else if (c == '{') st.push('}');
            else if (c == '[') st.push(']');
            else {
                if (st.empty() || st.top() != c) return false;
                st.pop();
            }
        }
        return st.empty();
    }
};""",
        "starter_code_javascript": """/**
 * @param {string} s
 * @return {boolean}
 */
function isValid(s) {
    // Write your solution here
    return false;
}""",
        "reference_solution_javascript": """function isValid(s) {
    const stack = [];
    const map = { '(': ')', '{': '}', '[': ']' };
    for (const c of s) {
        if (map[c]) stack.push(map[c]);
        else if (stack.pop() !== c) return false;
    }
    return stack.length === 0;
}"""
    },

    19: {
        "starter_code_java": """class Solution {
    public int[] dailyTemperatures(int[] temperatures) {
        // Write your solution here
        return new int[]{};
    }
}""",
        "reference_solution_java": """import java.util.Stack;

class Solution {
    public int[] dailyTemperatures(int[] temperatures) {
        int n = temperatures.length;
        int[] res = new int[n];
        Stack<Integer> stack = new Stack<>();
        for (int i = 0; i < n; i++) {
            while (!stack.isEmpty() && temperatures[i] > temperatures[stack.peek()]) {
                int prev = stack.pop();
                res[prev] = i - prev;
            }
            stack.push(i);
        }
        return res;
    }
}""",
        "starter_code_cpp": """#include <vector>
using namespace std;

class Solution {
public:
    vector<int> dailyTemperatures(vector<int>& temperatures) {
        // Write your solution here
        return {};
    }
};""",
        "reference_solution_cpp": """#include <vector>
#include <stack>
using namespace std;

class Solution {
public:
    vector<int> dailyTemperatures(vector<int>& temperatures) {
        int n = temperatures.size();
        vector<int> res(n, 0);
        stack<int> st;
        for (int i = 0; i < n; ++i) {
            while (!st.empty() && temperatures[i] > temperatures[st.top()]) {
                int prev = st.top(); st.pop();
                res[prev] = i - prev;
            }
            st.push(i);
        }
        return res;
    }
};""",
        "starter_code_javascript": """/**
 * @param {number[]} temperatures
 * @return {number[]}
 */
function dailyTemperatures(temperatures) {
    // Write your solution here
    return [];
}""",
        "reference_solution_javascript": """function dailyTemperatures(temperatures) {
    const n = temperatures.length;
    const res = new Array(n).fill(0);
    const stack = [];
    for (let i = 0; i < n; i++) {
        while (stack.length > 0 && temperatures[i] > temperatures[stack[stack.length - 1]]) {
            const prev = stack.pop();
            res[prev] = i - prev;
        }
        stack.push(i);
    }
    return res;
}"""
    },

    20: {
        "starter_code_java": """class Solution {
    public int largestRectangleArea(int[] heights) {
        // Write your solution here
        return 0;
    }
}""",
        "reference_solution_java": """import java.util.Stack;

class Solution {
    public int largestRectangleArea(int[] heights) {
        int n = heights.length, maxArea = 0;
        Stack<Integer> stack = new Stack<>();
        for (int i = 0; i <= n; i++) {
            int h = (i == n) ? 0 : heights[i];
            while (!stack.isEmpty() && h < heights[stack.peek()]) {
                int height = heights[stack.pop()];
                int width = stack.isEmpty() ? i : i - stack.peek() - 1;
                maxArea = Math.max(maxArea, height * width);
            }
            stack.push(i);
        }
        return maxArea;
    }
}""",
        "starter_code_cpp": """#include <vector>
using namespace std;

class Solution {
public:
    int largestRectangleArea(vector<int>& heights) {
        // Write your solution here
        return 0;
    }
};""",
        "reference_solution_cpp": """#include <vector>
#include <stack>
#include <algorithm>
using namespace std;

class Solution {
public:
    int largestRectangleArea(vector<int>& heights) {
        int n = heights.size(), maxArea = 0;
        stack<int> st;
        for (int i = 0; i <= n; ++i) {
            int h = (i == n) ? 0 : heights[i];
            while (!st.empty() && h < heights[st.top()]) {
                int height = heights[st.top()]; st.pop();
                int width = st.empty() ? i : i - st.top() - 1;
                maxArea = max(maxArea, height * width);
            }
            st.push(i);
        }
        return maxArea;
    }
};""",
        "starter_code_javascript": """/**
 * @param {number[]} heights
 * @return {number}
 */
function largestRectangleArea(heights) {
    // Write your solution here
    return 0;
}""",
        "reference_solution_javascript": """function largestRectangleArea(heights) {
    let maxArea = 0;
    const stack = [];
    const n = heights.length;
    for (let i = 0; i <= n; i++) {
        const h = i === n ? 0 : heights[i];
        while (stack.length > 0 && h < heights[stack[stack.length - 1]]) {
            const height = heights[stack.pop()];
            const width = stack.length === 0 ? i : i - stack[stack.length - 1] - 1;
            maxArea = Math.max(maxArea, height * width);
        }
        stack.push(i);
    }
    return maxArea;
}"""
    },

    22: {
        "starter_code_java": """class Solution {
    public int[] invertTree(int[] root) {
        // Write your solution here
        return new int[]{};
    }
}""",
        "reference_solution_java": """import java.util.*;

class Solution {
    public int[] invertTree(int[] root) {
        if (root == null || root.length == 0) return new int[]{};
        int n = root.length;
        int[] res = root.clone();
        int levelStart = 0, levelSize = 1;
        while (levelStart < n) {
            int levelEnd = Math.min(n, levelStart + levelSize);
            for (int i = 0; i < (levelEnd - levelStart) / 2; i++) {
                int t = res[levelStart + i];
                res[levelStart + i] = res[levelEnd - 1 - i];
                res[levelEnd - 1 - i] = t;
            }
            levelStart += levelSize;
            levelSize *= 2;
        }
        return res;
    }
}""",
        "starter_code_cpp": """#include <vector>
using namespace std;

class Solution {
public:
    vector<int> invertTree(vector<int>& root) {
        // Write your solution here
        return {};
    }
};""",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    vector<int> invertTree(vector<int>& root) {
        if (root.empty()) return {};
        vector<int> res = root;
        int n = res.size();
        int levelStart = 0, levelSize = 1;
        while (levelStart < n) {
            int levelEnd = min(n, levelStart + levelSize);
            reverse(res.begin() + levelStart, res.begin() + levelEnd);
            levelStart += levelSize;
            levelSize *= 2;
        }
        return res;
    }
};""",
        "starter_code_javascript": """/**
 * @param {number[]} root
 * @return {number[]}
 */
function invertTree(root) {
    // Write your solution here
    return [];
}""",
        "reference_solution_javascript": """function invertTree(root) {
    if (!root || root.length === 0) return [];
    const res = [...root];
    const n = res.length;
    let levelStart = 0, levelSize = 1;
    while (levelStart < n) {
        const levelEnd = Math.min(n, levelStart + levelSize);
        const sub = res.slice(levelStart, levelEnd).reverse();
        for (let i = 0; i < sub.length; i++) res[levelStart + i] = sub[i];
        levelStart += levelSize;
        levelSize *= 2;
    }
    return res;
}"""
    },

    23: {
        "starter_code_java": """class Solution {
    public int lowestCommonAncestor(int[] root, int p, int q) {
        // Write your solution here
        return 0;
    }
}""",
        "reference_solution_java": """class Solution {
    public int lowestCommonAncestor(int[] root, int p, int q) {
        int curr = 0;
        int minVal = Math.min(p, q), maxVal = Math.max(p, q);
        while (curr < root.length) {
            int val = root[curr];
            if (val > maxVal) curr = 2 * curr + 1;
            else if (val < minVal) curr = 2 * curr + 2;
            else return val;
        }
        return root[0];
    }
}""",
        "starter_code_cpp": """#include <vector>
using namespace std;

class Solution {
public:
    int lowestCommonAncestor(vector<int>& root, int p, int q) {
        // Write your solution here
        return 0;
    }
};""",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int lowestCommonAncestor(vector<int>& root, int p, int q) {
        int curr = 0;
        int minVal = min(p, q), maxVal = max(p, q);
        while (curr < (int)root.size()) {
            int val = root[curr];
            if (val > maxVal) curr = 2 * curr + 1;
            else if (val < minVal) curr = 2 * curr + 2;
            else return val;
        }
        return root.empty() ? 0 : root[0];
    }
};""",
        "starter_code_javascript": """/**
 * @param {number[]} root
 * @param {number} p
 * @param {number} q
 * @return {number}
 */
function lowestCommonAncestor(root, p, q) {
    // Write your solution here
    return 0;
}""",
        "reference_solution_javascript": """function lowestCommonAncestor(root, p, q) {
    let curr = 0;
    const minVal = Math.min(p, q), maxVal = Math.max(p, q);
    while (curr < root.length) {
        const val = root[curr];
        if (val > maxVal) curr = 2 * curr + 1;
        else if (val < minVal) curr = 2 * curr + 2;
        else return val;
    }
    return root[0];
}"""
    },

    24: {
        "starter_code_java": """class Solution {
    public boolean isValidBST(Integer[] root) {
        // Write your solution here
        return false;
    }
}""",
        "reference_solution_java": """class Solution {
    public boolean isValidBST(Integer[] root) {
        return validate(root, 0, null, null);
    }
    private boolean validate(Integer[] root, int idx, Integer low, Integer high) {
        if (idx >= root.length || root[idx] == null) return true;
        int val = root[idx];
        if ((low != null && val <= low) || (high != null && val >= high)) return false;
        return validate(root, 2 * idx + 1, low, val) && validate(root, 2 * idx + 2, val, high);
    }
}""",
        "starter_code_cpp": """#include <vector>
#include <string>
using namespace std;

class Solution {
public:
    bool isValidBST(vector<int>& root) {
        // Write your solution here
        return false;
    }
    bool isValidBST(vector<string>& root) {
        // Write your solution here
        return false;
    }
};""",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <climits>
using namespace std;

class Solution {
public:
    bool isValidBST(vector<int>& root) {
        vector<string> sroot;
        for (int x : root) sroot.push_back(to_string(x));
        return isValidBST(sroot);
    }
    bool isValidBST(vector<string>& root) {
        return validate(root, 0, (long long)INT_MIN - 1, (long long)INT_MAX + 1);
    }
private:
    bool validate(const vector<string>& root, int idx, long long low, long long high) {
        if (idx >= (int)root.size() || root[idx] == "null") return true;
        long long val = stoll(root[idx]);
        if (val <= low || val >= high) return false;
        return validate(root, 2 * idx + 1, low, val) && validate(root, 2 * idx + 2, val, high);
    }
};""",
        "starter_code_javascript": """/**
 * @param {Array} root
 * @return {boolean}
 */
function isValidBST(root) {
    // Write your solution here
    return false;
}""",
        "reference_solution_javascript": """function isValidBST(root) {
    function validate(idx, low, high) {
        if (idx >= root.length || root[idx] === null || root[idx] === undefined) return true;
        const val = root[idx];
        if ((low !== null && val <= low) || (high !== null && val >= high)) return false;
        return validate(2 * idx + 1, low, val) && validate(2 * idx + 2, val, high);
    }
    return validate(0, null, null);
}"""
    },

    25: {
        "starter_code_java": """class Solution {
    public int maxPathSum(Integer[] root) {
        // Write your solution here
        return 0;
    }
}""",
        "reference_solution_java": """class Solution {
    private int maxSum = Integer.MIN_VALUE;
    public int maxPathSum(Integer[] root) {
        maxSum = Integer.MIN_VALUE;
        maxGain(root, 0);
        return maxSum;
    }
    private int maxGain(Integer[] root, int idx) {
        if (idx >= root.length || root[idx] == null) return 0;
        int left = Math.max(0, maxGain(root, 2 * idx + 1));
        int right = Math.max(0, maxGain(root, 2 * idx + 2));
        maxSum = Math.max(maxSum, root[idx] + left + right);
        return root[idx] + Math.max(left, right);
    }
}""",
        "starter_code_cpp": """#include <vector>
#include <string>
using namespace std;

class Solution {
public:
    int maxPathSum(vector<int>& root) {
        // Write your solution here
        return 0;
    }
    int maxPathSum(vector<string>& root) {
        // Write your solution here
        return 0;
    }
};""",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <algorithm>
#include <climits>
using namespace std;

class Solution {
    int maxSum = INT_MIN;
public:
    int maxPathSum(vector<int>& root) {
        vector<string> sroot;
        for (int x : root) sroot.push_back(to_string(x));
        return maxPathSum(sroot);
    }
    int maxPathSum(vector<string>& root) {
        maxSum = INT_MIN;
        maxGain(root, 0);
        return maxSum;
    }
private:
    int maxGain(const vector<string>& root, int idx) {
        if (idx >= (int)root.size() || root[idx] == "null") return 0;
        int val = stoi(root[idx]);
        int left = max(0, maxGain(root, 2 * idx + 1));
        int right = max(0, maxGain(root, 2 * idx + 2));
        maxSum = max(maxSum, val + left + right);
        return val + max(left, right);
    }
};""",
        "starter_code_javascript": """/**
 * @param {Array} root
 * @return {number}
 */
function maxPathSum(root) {
    // Write your solution here
    return 0;
}""",
        "reference_solution_javascript": """function maxPathSum(root) {
    let maxSum = -Infinity;
    function maxGain(idx) {
        if (idx >= root.length || root[idx] === null || root[idx] === undefined) return 0;
        const val = root[idx];
        const left = Math.max(0, maxGain(2 * idx + 1));
        const right = Math.max(0, maxGain(2 * idx + 2));
        maxSum = Math.max(maxSum, val + left + right);
        return val + Math.max(left, right);
    }
    maxGain(0);
    return maxSum;
}"""
    },

    27: {
        "starter_code_java": """class Solution {
    public int[][] cloneGraph(int[][] adjList) {
        // Write your solution here
        return new int[][]{};
    }
}""",
        "reference_solution_java": """class Solution {
    public int[][] cloneGraph(int[][] adjList) {
        if (adjList == null) return new int[][]{};
        int[][] res = new int[adjList.length][];
        for (int i = 0; i < adjList.length; i++) {
            res[i] = adjList[i] != null ? adjList[i].clone() : new int[]{};
        }
        return res;
    }
}""",
        "starter_code_cpp": """#include <vector>
using namespace std;

class Solution {
public:
    vector<vector<int>> cloneGraph(vector<vector<int>>& adjList) {
        // Write your solution here
        return {};
    }
};""",
        "reference_solution_cpp": """#include <vector>
using namespace std;

class Solution {
public:
    vector<vector<int>> cloneGraph(vector<vector<int>>& adjList) {
        return adjList;
    }
};""",
        "starter_code_javascript": """/**
 * @param {number[][]} adjList
 * @return {number[][]}
 */
function cloneGraph(adjList) {
    // Write your solution here
    return [];
}""",
        "reference_solution_javascript": """function cloneGraph(adjList) {
    return adjList.map(inner => [...inner]);
}"""
    },

    28: {
        "starter_code_java": """class Solution {
    public boolean canFinish(int numCourses, int[][] prerequisites) {
        // Write your solution here
        return false;
    }
}""",
        "reference_solution_java": """import java.util.*;

class Solution {
    public boolean canFinish(int numCourses, int[][] prerequisites) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < numCourses; i++) adj.add(new ArrayList<>());
        int[] inDegree = new int[numCourses];
        for (int[] p : prerequisites) {
            adj.get(p[1]).add(p[0]);
            inDegree[p[0]]++;
        }
        Queue<Integer> q = new LinkedList<>();
        for (int i = 0; i < numCourses; i++) {
            if (inDegree[i] == 0) q.offer(i);
        }
        int count = 0;
        while (!q.isEmpty()) {
            int node = q.poll();
            count++;
            for (int neighbor : adj.get(node)) {
                if (--inDegree[neighbor] == 0) q.offer(neighbor);
            }
        }
        return count == numCourses;
    }
}""",
        "starter_code_cpp": """#include <vector>
using namespace std;

class Solution {
public:
    bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {
        // Write your solution here
        return false;
    }
};""",
        "reference_solution_cpp": """#include <vector>
#include <queue>
using namespace std;

class Solution {
public:
    bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {
        vector<vector<int>> adj(numCourses);
        vector<int> inDegree(numCourses, 0);
        for (const auto& p : prerequisites) {
            adj[p[1]].push_back(p[0]);
            inDegree[p[0]]++;
        }
        queue<int> q;
        for (int i = 0; i < numCourses; ++i) {
            if (inDegree[i] == 0) q.push(i);
        }
        int count = 0;
        while (!q.empty()) {
            int node = q.front(); q.pop();
            count++;
            for (int neighbor : adj[node]) {
                if (--inDegree[neighbor] == 0) q.push(neighbor);
            }
        }
        return count == numCourses;
    }
};""",
        "starter_code_javascript": """/**
 * @param {number} numCourses
 * @param {number[][]} prerequisites
 * @return {boolean}
 */
function canFinish(numCourses, prerequisites) {
    // Write your solution here
    return false;
}""",
        "reference_solution_javascript": """function canFinish(numCourses, prerequisites) {
    const inDegree = new Array(numCourses).fill(0);
    const adj = Array.from({ length: numCourses }, () => []);
    for (const [course, pre] of prerequisites) {
        adj[pre].push(course);
        inDegree[course]++;
    }
    const queue = [];
    for (let i = 0; i < numCourses; i++) {
        if (inDegree[i] === 0) queue.push(i);
    }
    let count = 0;
    while (queue.length > 0) {
        const node = queue.shift();
        count++;
        for (const next of adj[node]) {
            inDegree[next]--;
            if (inDegree[next] === 0) queue.push(next);
        }
    }
    return count === numCourses;
}"""
    },

    29: {
        "starter_code_java": """class Solution {
    public int ladderLength(String beginWord, String endWord, String[] wordList) {
        // Write your solution here
        return 0;
    }
}""",
        "reference_solution_java": """import java.util.*;

class Solution {
    public int ladderLength(String beginWord, String endWord, String[] wordList) {
        Set<String> wordSet = new HashSet<>(Arrays.asList(wordList));
        if (!wordSet.contains(endWord)) return 0;
        Queue<String> queue = new LinkedList<>();
        queue.offer(beginWord);
        int level = 1;
        while (!queue.isEmpty()) {
            int size = queue.size();
            for (int i = 0; i < size; i++) {
                String word = queue.poll();
                char[] chars = word.toCharArray();
                for (int j = 0; j < chars.length; j++) {
                    char orig = chars[j];
                    for (char c = 'a'; c <= 'z'; c++) {
                        chars[j] = c;
                        String next = new String(chars);
                        if (next.equals(endWord)) return level + 1;
                        if (wordSet.remove(next)) {
                            queue.offer(next);
                        }
                    }
                    chars[j] = orig;
                }
            }
            level++;
        }
        return 0;
    }
}""",
        "starter_code_cpp": """#include <string>
#include <vector>
using namespace std;

class Solution {
public:
    int ladderLength(string beginWord, string endWord, vector<string>& wordList) {
        // Write your solution here
        return 0;
    }
};""",
        "reference_solution_cpp": """#include <string>
#include <vector>
#include <unordered_set>
#include <queue>
using namespace std;

class Solution {
public:
    int ladderLength(string beginWord, string endWord, vector<string>& wordList) {
        unordered_set<string> wordSet(wordList.begin(), wordList.end());
        if (!wordSet.count(endWord)) return 0;
        queue<string> q;
        q.push(beginWord);
        int level = 1;
        while (!q.empty()) {
            int size = q.size();
            while (size--) {
                string word = q.front(); q.pop();
                for (int i = 0; i < (int)word.size(); ++i) {
                    char orig = word[i];
                    for (char c = 'a'; c <= 'z'; ++c) {
                        word[i] = c;
                        if (word == endWord) return level + 1;
                        if (wordSet.erase(word)) {
                            q.push(word);
                        }
                    }
                    word[i] = orig;
                }
            }
            level++;
        }
        return 0;
    }
};""",
        "starter_code_javascript": """/**
 * @param {string} beginWord
 * @param {string} endWord
 * @param {string[]} wordList
 * @return {number}
 */
function ladderLength(beginWord, endWord, wordList) {
    // Write your solution here
    return 0;
}""",
        "reference_solution_javascript": """function ladderLength(beginWord, endWord, wordList) {
    const wordSet = new Set(wordList);
    if (!wordSet.has(endWord)) return 0;
    const queue = [beginWord];
    let level = 1;
    while (queue.length > 0) {
        const size = queue.length;
        for (let i = 0; i < size; i++) {
            const word = queue.shift();
            for (let j = 0; j < word.length; j++) {
                for (let c = 97; c <= 122; c++) {
                    const next = word.slice(0, j) + String.fromCharCode(c) + word.slice(j + 1);
                    if (next === endWord) return level + 1;
                    if (wordSet.has(next)) {
                        wordSet.delete(next);
                        queue.push(next);
                    }
                }
            }
        }
        level++;
    }
    return 0;
}"""
    },

    30: {
        "starter_code_java": """class Solution {
    public boolean canJump(int[] nums) {
        // Write your solution here
        return false;
    }
}""",
        "reference_solution_java": """class Solution {
    public boolean canJump(int[] nums) {
        int maxReach = 0;
        for (int i = 0; i < nums.length; i++) {
            if (i > maxReach) return false;
            maxReach = Math.max(maxReach, i + nums[i]);
            if (maxReach >= nums.length - 1) return true;
        }
        return true;
    }
}""",
        "starter_code_cpp": """#include <vector>
using namespace std;

class Solution {
public:
    bool canJump(vector<int>& nums) {
        // Write your solution here
        return false;
    }
};""",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    bool canJump(vector<int>& nums) {
        int maxReach = 0;
        for (int i = 0; i < (int)nums.size(); ++i) {
            if (i > maxReach) return false;
            maxReach = max(maxReach, i + nums[i]);
            if (maxReach >= (int)nums.size() - 1) return true;
        }
        return true;
    }
};""",
        "starter_code_javascript": """/**
 * @param {number[]} nums
 * @return {boolean}
 */
function canJump(nums) {
    // Write your solution here
    return false;
}""",
        "reference_solution_javascript": """function canJump(nums) {
    let maxReach = 0;
    for (let i = 0; i < nums.length; i++) {
        if (i > maxReach) return false;
        maxReach = Math.max(maxReach, i + nums[i]);
        if (maxReach >= nums.length - 1) return true;
    }
    return true;
}"""
    },

    31: {
        "starter_code_java": """class Solution {
    public int canCompleteCircuit(int[] gas, int[] cost) {
        // Write your solution here
        return 0;
    }
}""",
        "reference_solution_java": """class Solution {
    public int canCompleteCircuit(int[] gas, int[] cost) {
        int total = 0, curr = 0, start = 0;
        for (int i = 0; i < gas.length; i++) {
            total += gas[i] - cost[i];
            curr += gas[i] - cost[i];
            if (curr < 0) {
                curr = 0;
                start = i + 1;
            }
        }
        return total >= 0 ? start : -1;
    }
}""",
        "starter_code_cpp": """#include <vector>
using namespace std;

class Solution {
public:
    int canCompleteCircuit(vector<int>& gas, vector<int>& cost) {
        // Write your solution here
        return 0;
    }
};""",
        "reference_solution_cpp": """#include <vector>
using namespace std;

class Solution {
public:
    int canCompleteCircuit(vector<int>& gas, vector<int>& cost) {
        int total = 0, curr = 0, start = 0;
        for (int i = 0; i < (int)gas.size(); ++i) {
            total += gas[i] - cost[i];
            curr += gas[i] - cost[i];
            if (curr < 0) {
                curr = 0;
                start = i + 1;
            }
        }
        return total >= 0 ? start : -1;
    }
};""",
        "starter_code_javascript": """/**
 * @param {number[]} gas
 * @param {number[]} cost
 * @return {number}
 */
function canCompleteCircuit(gas, cost) {
    // Write your solution here
    return 0;
}""",
        "reference_solution_javascript": """function canCompleteCircuit(gas, cost) {
    let total = 0, curr = 0, start = 0;
    for (let i = 0; i < gas.length; i++) {
        total += gas[i] - cost[i];
        curr += gas[i] - cost[i];
        if (curr < 0) {
            curr = 0;
            start = i + 1;
        }
    }
    return total >= 0 ? start : -1;
}"""
    },

    32: {
        "starter_code_java": """class Solution {
    public int leastInterval(String[] tasks, int n) {
        // Write your solution here
        return 0;
    }
}""",
        "reference_solution_java": """import java.util.*;

class Solution {
    public int leastInterval(String[] tasks, int n) {
        int[] count = new int[26];
        for (String t : tasks) count[t.charAt(0) - 'A']++;
        Arrays.sort(count);
        int maxVal = count[25];
        int maxCount = 1;
        for (int i = 24; i >= 0; i--) {
            if (count[i] == maxVal) maxCount++;
            else break;
        }
        int partCount = maxVal - 1;
        int emptySlots = partCount * (n - (maxCount - 1));
        int availableTasks = tasks.length - maxVal * maxCount;
        int idles = Math.max(0, emptySlots - availableTasks);
        return tasks.length + idles;
    }
}""",
        "starter_code_cpp": """#include <vector>
#include <string>
using namespace std;

class Solution {
public:
    int leastInterval(vector<string>& tasks, int n) {
        // Write your solution here
        return 0;
    }
};""",
        "reference_solution_cpp": """#include <vector>
#include <string>
#include <algorithm>
using namespace std;

class Solution {
public:
    int leastInterval(vector<string>& tasks, int n) {
        vector<int> count(26, 0);
        for (const string& t : tasks) count[t[0] - 'A']++;
        sort(count.begin(), count.end());
        int maxVal = count[25];
        int maxCount = 1;
        for (int i = 24; i >= 0; --i) {
            if (count[i] == maxVal) maxCount++;
            else break;
        }
        int partCount = maxVal - 1;
        int emptySlots = partCount * (n - (maxCount - 1));
        int availableTasks = (int)tasks.size() - maxVal * maxCount;
        int idles = max(0, emptySlots - availableTasks);
        return (int)tasks.size() + idles;
    }
};""",
        "starter_code_javascript": """/**
 * @param {string[]} tasks
 * @param {number} n
 * @return {number}
 */
function leastInterval(tasks, n) {
    // Write your solution here
    return 0;
}""",
        "reference_solution_javascript": """function leastInterval(tasks, n) {
    const counts = new Map();
    for (const t of tasks) counts.set(t, (counts.get(t) || 0) + 1);
    const sorted = Array.from(counts.values()).sort((a, b) => b - a);
    const maxVal = sorted[0];
    let maxCount = 0;
    for (const c of sorted) {
        if (c === maxVal) maxCount++;
        else break;
    }
    const partCount = maxVal - 1;
    const emptySlots = partCount * (n - (maxCount - 1));
    const availableTasks = tasks.length - maxVal * maxCount;
    const idles = Math.max(0, emptySlots - availableTasks);
    return tasks.length + idles;
}"""
    },

    34: {
        "starter_code_java": """class Solution {
    public int coinChange(int[] coins, int amount) {
        // Write your solution here
        return 0;
    }
}""",
        "reference_solution_java": """import java.util.Arrays;

class Solution {
    public int coinChange(int[] coins, int amount) {
        int[] dp = new int[amount + 1];
        Arrays.fill(dp, amount + 1);
        dp[0] = 0;
        for (int coin : coins) {
            for (int i = coin; i <= amount; i++) {
                dp[i] = Math.min(dp[i], dp[i - coin] + 1);
            }
        }
        return dp[amount] > amount ? -1 : dp[amount];
    }
}""",
        "starter_code_cpp": """#include <vector>
using namespace std;

class Solution {
public:
    int coinChange(vector<int>& coins, int amount) {
        // Write your solution here
        return 0;
    }
};""",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int coinChange(vector<int>& coins, int amount) {
        vector<int> dp(amount + 1, amount + 1);
        dp[0] = 0;
        for (int coin : coins) {
            for (int i = coin; i <= amount; ++i) {
                dp[i] = min(dp[i], dp[i - coin] + 1);
            }
        }
        return dp[amount] > amount ? -1 : dp[amount];
    }
};""",
        "starter_code_javascript": """/**
 * @param {number[]} coins
 * @param {number} amount
 * @return {number}
 */
function coinChange(coins, amount) {
    // Write your solution here
    return 0;
}""",
        "reference_solution_javascript": """function coinChange(coins, amount) {
    const dp = new Array(amount + 1).fill(amount + 1);
    dp[0] = 0;
    for (const coin of coins) {
        for (let i = coin; i <= amount; i++) {
            dp[i] = Math.min(dp[i], dp[i - coin] + 1);
        }
    }
    return dp[amount] > amount ? -1 : dp[amount];
}"""
    },

    35: {
        "starter_code_java": """class Solution {
    public int lengthOfLIS(int[] nums) {
        // Write your solution here
        return 0;
    }
}""",
        "reference_solution_java": """import java.util.*;

class Solution {
    public int lengthOfLIS(int[] nums) {
        List<Integer> tails = new ArrayList<>();
        for (int x : nums) {
            int idx = Collections.binarySearch(tails, x);
            if (idx < 0) idx = -(idx + 1);
            if (idx == tails.size()) tails.add(x);
            else tails.set(idx, x);
        }
        return tails.size();
    }
}""",
        "starter_code_cpp": """#include <vector>
using namespace std;

class Solution {
public:
    int lengthOfLIS(vector<int>& nums) {
        // Write your solution here
        return 0;
    }
};""",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int lengthOfLIS(vector<int>& nums) {
        vector<int> tails;
        for (int x : nums) {
            auto it = lower_bound(tails.begin(), tails.end(), x);
            if (it == tails.end()) tails.push_back(x);
            else *it = x;
        }
        return tails.size();
    }
};""",
        "starter_code_javascript": """/**
 * @param {number[]} nums
 * @return {number}
 */
function lengthOfLIS(nums) {
    // Write your solution here
    return 0;
}""",
        "reference_solution_javascript": """function lengthOfLIS(nums) {
    const tails = [];
    for (const x of nums) {
        let l = 0, r = tails.length;
        while (l < r) {
            const m = (l + r) >> 1;
            if (tails[m] < x) l = m + 1;
            else r = m;
        }
        if (l === tails.length) tails.push(x);
        else tails[l] = x;
    }
    return tails.length;
}"""
    },

    36: {
        "starter_code_java": """class Solution {
    public int uniquePaths(int m, int n) {
        // Write your solution here
        return 0;
    }
}""",
        "reference_solution_java": """import java.util.Arrays;

class Solution {
    public int uniquePaths(int m, int n) {
        int[] dp = new int[n];
        Arrays.fill(dp, 1);
        for (int i = 1; i < m; i++) {
            for (int j = 1; j < n; j++) {
                dp[j] += dp[j - 1];
            }
        }
        return dp[n - 1];
    }
}""",
        "starter_code_cpp": """class Solution {
public:
    int uniquePaths(int m, int n) {
        // Write your solution here
        return 0;
    }
};""",
        "reference_solution_cpp": """#include <vector>
using namespace std;

class Solution {
public:
    int uniquePaths(int m, int n) {
        vector<int> dp(n, 1);
        for (int i = 1; i < m; ++i) {
            for (int j = 1; j < n; ++j) {
                dp[j] += dp[j - 1];
            }
        }
        return dp[n - 1];
    }
};""",
        "starter_code_javascript": """/**
 * @param {number} m
 * @param {number} n
 * @return {number}
 */
function uniquePaths(m, n) {
    // Write your solution here
    return 0;
}""",
        "reference_solution_javascript": """function uniquePaths(m, n) {
    const dp = new Array(n).fill(1);
    for (let i = 1; i < m; i++) {
        for (let j = 1; j < n; j++) {
            dp[j] += dp[j - 1];
        }
    }
    return dp[n - 1];
}"""
    },

    37: {
        "starter_code_java": """class Solution {
    public int minDistance(String word1, String word2) {
        // Write your solution here
        return 0;
    }
}""",
        "reference_solution_java": """class Solution {
    public int minDistance(String word1, String word2) {
        int m = word1.length(), n = word2.length();
        int[][] dp = new int[m + 1][n + 1];
        for (int i = 0; i <= m; i++) dp[i][0] = i;
        for (int j = 0; j <= n; j++) dp[0][j] = j;
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (word1.charAt(i - 1) == word2.charAt(j - 1)) dp[i][j] = dp[i - 1][j - 1];
                else dp[i][j] = 1 + Math.min(dp[i - 1][j - 1], Math.min(dp[i - 1][j], dp[i][j - 1]));
            }
        }
        return dp[m][n];
    }
}""",
        "starter_code_cpp": """#include <string>
using namespace std;

class Solution {
public:
    int minDistance(string word1, string word2) {
        // Write your solution here
        return 0;
    }
};""",
        "reference_solution_cpp": """#include <string>
#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int minDistance(string word1, string word2) {
        int m = word1.size(), n = word2.size();
        vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));
        for (int i = 0; i <= m; ++i) dp[i][0] = i;
        for (int j = 0; j <= n; ++j) dp[0][j] = j;
        for (int i = 1; i <= m; ++i) {
            for (int j = 1; j <= n; ++j) {
                if (word1[i - 1] == word2[j - 1]) dp[i][j] = dp[i - 1][j - 1];
                else dp[i][j] = 1 + min({dp[i - 1][j - 1], dp[i - 1][j], dp[i][j - 1]});
            }
        }
        return dp[m][n];
    }
};""",
        "starter_code_javascript": """/**
 * @param {string} word1
 * @param {string} word2
 * @return {number}
 */
function minDistance(word1, word2) {
    // Write your solution here
    return 0;
}""",
        "reference_solution_javascript": """function minDistance(word1, word2) {
    const m = word1.length, n = word2.length;
    const dp = Array.from({ length: m + 1 }, () => new Array(n + 1).fill(0));
    for (let i = 0; i <= m; i++) dp[i][0] = i;
    for (let j = 0; j <= n; j++) dp[0][j] = j;
    for (let i = 1; i <= m; i++) {
        for (let j = 1; j <= n; j++) {
            if (word1[i - 1] === word2[j - 1]) dp[i][j] = dp[i - 1][j - 1];
            else dp[i][j] = 1 + Math.min(dp[i - 1][j - 1], dp[i - 1][j], dp[i][j - 1]);
        }
    }
    return dp[m][n];
}"""
    },

    38: {
        "starter_code_java": """class Solution {
    public int[][] subsets(int[] nums) {
        // Write your solution here
        return new int[][]{};
    }
}""",
        "reference_solution_java": """import java.util.*;

class Solution {
    public int[][] subsets(int[] nums) {
        List<List<Integer>> res = new ArrayList<>();
        backtrack(nums, 0, new ArrayList<>(), res);
        res.sort((a, b) -> {
            int minLen = Math.min(a.size(), b.size());
            for (int i = 0; i < minLen; i++) {
                int cmp = Integer.compare(a.get(i), b.get(i));
                if (cmp != 0) return cmp;
            }
            return Integer.compare(a.size(), b.size());
        });
        int[][] out = new int[res.size()][];
        for (int i = 0; i < res.size(); i++) {
            out[i] = res.get(i).stream().mapToInt(Integer::intValue).toArray();
        }
        return out;
    }
    private void backtrack(int[] nums, int start, List<Integer> curr, List<List<Integer>> res) {
        res.add(new ArrayList<>(curr));
        for (int i = start; i < nums.length; i++) {
            curr.add(nums[i]);
            backtrack(nums, i + 1, curr, res);
            curr.remove(curr.size() - 1);
        }
    }
}""",
        "starter_code_cpp": """#include <vector>
using namespace std;

class Solution {
public:
    vector<vector<int>> subsets(vector<int>& nums) {
        // Write your solution here
        return {};
    }
};""",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    vector<vector<int>> subsets(vector<int>& nums) {
        vector<vector<int>> res;
        vector<int> curr;
        backtrack(nums, 0, curr, res);
        sort(res.begin(), res.end());
        return res;
    }
private:
    void backtrack(const vector<int>& nums, int start, vector<int>& curr, vector<vector<int>>& res) {
        res.push_back(curr);
        for (int i = start; i < (int)nums.size(); ++i) {
            curr.push_back(nums[i]);
            backtrack(nums, i + 1, curr, res);
            curr.pop_back();
        }
    }
};""",
        "starter_code_javascript": """/**
 * @param {number[]} nums
 * @return {number[][]}
 */
function subsets(nums) {
    // Write your solution here
    return [];
}""",
        "reference_solution_javascript": """function subsets(nums) {
    const res = [];
    function backtrack(start, curr) {
        res.push([...curr]);
        for (let i = start; i < nums.length; i++) {
            curr.push(nums[i]);
            backtrack(i + 1, curr);
            curr.pop();
        }
    }
    backtrack(0, []);
    res.sort((a, b) => {
        const minLen = Math.min(a.length, b.length);
        for (let i = 0; i < minLen; i++) {
            if (a[i] !== b[i]) return a[i] - b[i];
        }
        return a.length - b.length;
    });
    return res;
}"""
    },

    39: {
        "starter_code_java": """class Solution {
    public int[][] combinationSum(int[] candidates, int target) {
        // Write your solution here
        return new int[][]{};
    }
}""",
        "reference_solution_java": """import java.util.*;

class Solution {
    public int[][] combinationSum(int[] candidates, int target) {
        List<List<Integer>> res = new ArrayList<>();
        Arrays.sort(candidates);
        backtrack(candidates, target, 0, new ArrayList<>(), res);
        int[][] out = new int[res.size()][];
        for (int i = 0; i < res.size(); i++) {
            out[i] = res.get(i).stream().mapToInt(Integer::intValue).toArray();
        }
        return out;
    }
    private void backtrack(int[] candidates, int remain, int start, List<Integer> curr, List<List<Integer>> res) {
        if (remain == 0) {
            res.add(new ArrayList<>(curr));
            return;
        }
        for (int i = start; i < candidates.length; i++) {
            if (candidates[i] > remain) break;
            curr.add(candidates[i]);
            backtrack(candidates, remain - candidates[i], i, curr, res);
            curr.remove(curr.size() - 1);
        }
    }
}""",
        "starter_code_cpp": """#include <vector>
using namespace std;

class Solution {
public:
    vector<vector<int>> combinationSum(vector<int>& candidates, int target) {
        // Write your solution here
        return {};
    }
};""",
        "reference_solution_cpp": """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    vector<vector<int>> combinationSum(vector<int>& candidates, int target) {
        vector<vector<int>> res;
        vector<int> curr;
        sort(candidates.begin(), candidates.end());
        backtrack(candidates, target, 0, curr, res);
        return res;
    }
private:
    void backtrack(const vector<int>& candidates, int remain, int start, vector<int>& curr, vector<vector<int>>& res) {
        if (remain == 0) {
            res.push_back(curr);
            return;
        }
        for (int i = start; i < (int)candidates.size(); ++i) {
            if (candidates[i] > remain) break;
            curr.push_back(candidates[i]);
            backtrack(candidates, remain - candidates[i], i, curr, res);
            curr.pop_back();
        }
    }
};""",
        "starter_code_javascript": """/**
 * @param {number[]} candidates
 * @param {number} target
 * @return {number[][]}
 */
function combinationSum(candidates, target) {
    // Write your solution here
    return [];
}""",
        "reference_solution_javascript": """function combinationSum(candidates, target) {
    const res = [];
    candidates.sort((a, b) => a - b);
    function backtrack(remain, start, curr) {
        if (remain === 0) {
            res.push([...curr]);
            return;
        }
        for (let i = start; i < candidates.length; i++) {
            if (candidates[i] > remain) break;
            curr.push(candidates[i]);
            backtrack(remain - candidates[i], i, curr);
            curr.pop();
        }
    }
    backtrack(target, 0, []);
    return res;
}"""
    },

    40: {
        "starter_code_java": """class Solution {
    public int totalNQueens(int n) {
        // Write your solution here
        return 0;
    }
}""",
        "reference_solution_java": """class Solution {
    private int count = 0;
    public int totalNQueens(int n) {
        count = 0;
        boolean[] cols = new boolean[n];
        boolean[] diag1 = new boolean[2 * n];
        boolean[] diag2 = new boolean[2 * n];
        backtrack(0, n, cols, diag1, diag2);
        return count;
    }
    private void backtrack(int r, int n, boolean[] cols, boolean[] diag1, boolean[] diag2) {
        if (r == n) {
            count++;
            return;
        }
        for (int c = 0; c < n; c++) {
            if (cols[c] || diag1[r + c] || diag2[r - c + n]) continue;
            cols[c] = diag1[r + c] = diag2[r - c + n] = true;
            backtrack(r + 1, n, cols, diag1, diag2);
            cols[c] = diag1[r + c] = diag2[r - c + n] = false;
        }
    }
}""",
        "starter_code_cpp": """class Solution {
public:
    int totalNQueens(int n) {
        // Write your solution here
        return 0;
    }
};""",
        "reference_solution_cpp": """#include <vector>
using namespace std;

class Solution {
    int count = 0;
public:
    int totalNQueens(int n) {
        count = 0;
        vector<bool> cols(n, false), diag1(2 * n, false), diag2(2 * n, false);
        backtrack(0, n, cols, diag1, diag2);
        return count;
    }
private:
    void backtrack(int r, int n, vector<bool>& cols, vector<bool>& diag1, vector<bool>& diag2) {
        if (r == n) {
            count++;
            return;
        }
        for (int c = 0; c < n; ++c) {
            if (cols[c] || diag1[r + c] || diag2[r - c + n]) continue;
            cols[c] = diag1[r + c] = diag2[r - c + n] = true;
            backtrack(r + 1, n, cols, diag1, diag2);
            cols[c] = diag1[r + c] = diag2[r - c + n] = false;
        }
    }
};""",
        "starter_code_javascript": """/**
 * @param {number} n
 * @return {number}
 */
function totalNQueens(n) {
    // Write your solution here
    return 0;
}""",
        "reference_solution_javascript": """function totalNQueens(n) {
    let count = 0;
    const cols = new Set(), diag1 = new Set(), diag2 = new Set();
    function backtrack(r) {
        if (r === n) {
            count++;
            return;
        }
        for (let c = 0; c < n; c++) {
            if (cols.has(c) || diag1.has(r + c) || diag2.has(r - c)) continue;
            cols.add(c); diag1.add(r + c); diag2.add(r - c);
            backtrack(r + 1);
            cols.delete(c); diag1.delete(r + c); diag2.delete(r - c);
        }
    }
    backtrack(0);
    return count;
}"""
    }
}
