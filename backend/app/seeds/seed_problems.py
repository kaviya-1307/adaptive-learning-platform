"""
Comprehensive Seeder for Topics, Curated Problems, and Test Cases.
Populates 10 core DSA topics and 40 curated LeetCode-style algorithmic problems
with visible and hidden test cases, starter code, and reference solutions.
"""
import logging
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models.topic import Topic
from app.models.problem import Problem
from app.models.test_case import TestCase

logger = logging.getLogger(__name__)

TOPICS_DATA = [
    {"name": "Arrays", "slug": "arrays", "order_index": 1},
    {"name": "Strings", "slug": "strings", "order_index": 2},
    {"name": "Hashing", "slug": "hashing", "order_index": 3},
    {"name": "Linked Lists", "slug": "linked-lists", "order_index": 4},
    {"name": "Stack & Queue", "slug": "stack-queue", "order_index": 5},
    {"name": "Trees", "slug": "trees", "order_index": 6},
    {"name": "Graphs", "slug": "graphs", "order_index": 7},
    {"name": "Greedy Algorithms", "slug": "greedy", "order_index": 8},
    {"name": "Dynamic Programming", "slug": "dynamic-programming", "order_index": 9},
    {"name": "Backtracking", "slug": "backtracking", "order_index": 10},
]

PROBLEMS_DATA = [
    # ------------------ 1. ARRAYS ------------------
    {
        "title": "Two Sum Target Pair",
        "slug": "two-sum-target-pair",
        "topic_slug": "arrays",
        "difficulty": "Easy",
        "is_diagnostic": True,
        "order_index": 1,
        "description_markdown": "Given an array of integers `nums` and an integer `target`, return the indices `[i, j]` of the two numbers such that they add up to `target`.\n\nYou may assume that each input has exactly one solution, and you may not use the same element twice.",
        "constraints_markdown": "- $2 \\le \\text{nums.length} \\le 10^4$\n- $-10^9 \\le \\text{nums}[i] \\le 10^9$\n- Time Complexity Target: $O(N)$",
        "starter_code_python": "def twoSum(nums: list[int], target: int) -> list[int]:\n    # Write your solution here\n    pass\n",
        "reference_solution_python": "def twoSum(nums: list[int], target: int) -> list[int]:\n    seen = {}\n    for i, num in enumerate(nums):\n        complement = target - num\n        if complement in seen:\n            return [seen[complement], i]\n        seen[num] = i\n    return []\n",
        "starter_code_java": "class Solution {\n    public int[] twoSum(int[] nums, int target) {\n        // Write your solution here\n        return new int[]{};\n    }\n}",
        "reference_solution_java": "import java.util.*;\n\nclass Solution {\n    public int[] twoSum(int[] nums, int target) {\n        Map<Integer, Integer> map = new HashMap<>();\n        for (int i = 0; i < nums.length; i++) {\n            int comp = target - nums[i];\n            if (map.containsKey(comp)) return new int[]{map.get(comp), i};\n            map.put(nums[i], i);\n        }\n        return new int[]{};\n    }\n}",
        "starter_code_cpp": "#include <vector>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> twoSum(vector<int>& nums, int target) {\n        // Write your solution here\n        return {};\n    }\n};",
        "reference_solution_cpp": "#include <vector>\n#include <unordered_map>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> twoSum(vector<int>& nums, int target) {\n        unordered_map<int, int> seen;\n        for (int i = 0; i < nums.size(); ++i) {\n            int comp = target - nums[i];\n            if (seen.count(comp)) return {seen[comp], i};\n            seen[nums[i]] = i;\n        }\n        return {};\n    }\n};",
        "starter_code_javascript": "/**\n * @param {number[]} nums\n * @param {number} target\n * @return {number[]}\n */\nfunction twoSum(nums, target) {\n    // Write your solution here\n    return [];\n}",
        "reference_solution_javascript": "function twoSum(nums, target) {\n    const map = new Map();\n    for (let i = 0; i < nums.length; i++) {\n        const comp = target - nums[i];\n        if (map.has(comp)) return [map.get(comp), i];\n        map.set(nums[i], i);\n    }\n    return [];\n}",
        "test_cases": [
            {"input_data": "{\"nums\": [2, 7, 11, 15], \"target\": 9}", "expected_output": "[0, 1]", "is_hidden": False},
            {"input_data": "{\"nums\": [3, 2, 4], \"target\": 6}", "expected_output": "[1, 2]", "is_hidden": False},
            {"input_data": "{\"nums\": [3, 3], \"target\": 6}", "expected_output": "[0, 1]", "is_hidden": True},
            {"input_data": "{\"nums\": [-1, -2, -3, -4, -5], \"target\": -8}", "expected_output": "[2, 4]", "is_hidden": True},
        ]
    },
    {
        "title": "Best Time to Buy and Sell Stock",
        "slug": "best-time-to-buy-and-sell-stock",
        "topic_slug": "arrays",
        "difficulty": "Easy",
        "is_diagnostic": False,
        "order_index": 2,
        "description_markdown": "You are given an array `prices` where `prices[i]` is the price of a given stock on the $i^{\\text{th}}$ day.\n\nYou want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.\n\nReturn the maximum profit you can achieve. If no profit is possible, return 0.",
        "constraints_markdown": "- $1 \\le \\text{prices.length} \\le 10^5$\n- $0 \\le \\text{prices}[i] \\le 10^4$",
        "starter_code_python": "def maxProfit(prices: list[int]) -> int:\n    # Write your solution here\n    pass\n",
        "reference_solution_python": "def maxProfit(prices: list[int]) -> int:\n    min_price = float('inf')\n    max_profit = 0\n    for p in prices:\n        if p < min_price:\n            min_price = p\n        elif p - min_price > max_profit:\n            max_profit = p - min_price\n    return max_profit\n",
        "test_cases": [
            {"input_data": "{\"prices\": [7, 1, 5, 3, 6, 4]}", "expected_output": "5", "is_hidden": False},
            {"input_data": "{\"prices\": [7, 6, 4, 3, 1]}", "expected_output": "0", "is_hidden": False},
            {"input_data": "{\"prices\": [2, 4, 1]}", "expected_output": "2", "is_hidden": True},
        ]
    },
    {
        "title": "Maximum Subarray Sum (Kadane's)",
        "slug": "maximum-subarray-sum",
        "topic_slug": "arrays",
        "difficulty": "Medium",
        "is_diagnostic": False,
        "order_index": 3,
        "description_markdown": "Given an integer array `nums`, find the contiguous subarray (containing at least one number) which has the largest sum and return its sum.",
        "constraints_markdown": "- $1 \\le \\text{nums.length} \\le 10^5$\n- $-10^4 \\le \\text{nums}[i] \\le 10^4$",
        "starter_code_python": "def maxSubArray(nums: list[int]) -> int:\n    # Write your solution here\n    pass\n",
        "reference_solution_python": "def maxSubArray(nums: list[int]) -> int:\n    curr_sum = max_sum = nums[0]\n    for num in nums[1:]:\n        curr_sum = max(num, curr_sum + num)\n        max_sum = max(max_sum, curr_sum)\n    return max_sum\n",
        "test_cases": [
            {"input_data": "{\"nums\": [-2, 1, -3, 4, -1, 2, 1, -5, 4]}", "expected_output": "6", "is_hidden": False},
            {"input_data": "{\"nums\": [1]}", "expected_output": "1", "is_hidden": False},
            {"input_data": "{\"nums\": [5, 4, -1, 7, 8]}", "expected_output": "23", "is_hidden": True},
        ]
    },
    {
        "title": "Product of Array Except Self",
        "slug": "product-of-array-except-self",
        "topic_slug": "arrays",
        "difficulty": "Medium",
        "is_diagnostic": False,
        "order_index": 4,
        "description_markdown": "Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the product of all elements of `nums` except `nums[i]`.\n\nYou must write an algorithm that runs in $O(N)$ time and without using the division operation.",
        "constraints_markdown": "- $2 \\le \\text{nums.length} \\le 10^5$\n- $-30 \\le \\text{nums}[i] \\le 30$",
        "starter_code_python": "def productExceptSelf(nums: list[int]) -> list[int]:\n    # Write your solution here\n    pass\n",
        "reference_solution_python": "def productExceptSelf(nums: list[int]) -> list[int]:\n    n = len(nums)\n    res = [1] * n\n    prefix = 1\n    for i in range(n):\n        res[i] = prefix\n        prefix *= nums[i]\n    postfix = 1\n    for i in range(n - 1, -1, -1):\n        res[i] *= postfix\n        postfix *= nums[i]\n    return res\n",
        "test_cases": [
            {"input_data": "{\"nums\": [1, 2, 3, 4]}", "expected_output": "[24, 12, 8, 6]", "is_hidden": False},
            {"input_data": "{\"nums\": [-1, 1, 0, -3, 3]}", "expected_output": "[0, 0, 9, 0, 0]", "is_hidden": False},
        ]
    },
    {
        "title": "Trapping Rain Water",
        "slug": "trapping-rain-water",
        "topic_slug": "arrays",
        "difficulty": "Hard",
        "is_diagnostic": False,
        "order_index": 5,
        "description_markdown": "Given `n` non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.",
        "constraints_markdown": "- $n == \\text{height.length}$\n- $1 \\le n \\le 2 \\cdot 10^4$\n- $0 \\le \\text{height}[i] \\le 10^5$",
        "starter_code_python": "def trap(height: list[int]) -> int:\n    # Write your solution here\n    pass\n",
        "reference_solution_python": "def trap(height: list[int]) -> int:\n    if not height: return 0\n    l, r = 0, len(height) - 1\n    l_max, r_max = height[l], height[r]\n    res = 0\n    while l < r:\n        if l_max < r_max:\n            l += 1\n            l_max = max(l_max, height[l])\n            res += l_max - height[l]\n        else:\n            r -= 1\n            r_max = max(r_max, height[r])\n            res += r_max - height[r]\n    return res\n",
        "test_cases": [
            {"input_data": "{\"height\": [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]}", "expected_output": "6", "is_hidden": False},
            {"input_data": "{\"height\": [4, 2, 0, 3, 2, 5]}", "expected_output": "9", "is_hidden": False},
        ]
    },

    # ------------------ 2. STRINGS ------------------
    {
        "title": "Valid Anagram Check",
        "slug": "valid-anagram-check",
        "topic_slug": "strings",
        "difficulty": "Easy",
        "is_diagnostic": True,
        "order_index": 6,
        "description_markdown": "Given two strings `s` and `t`, return `True` if `t` is an anagram of `s`, and `False` otherwise.\n\nAn **Anagram** is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.",
        "constraints_markdown": "- $1 \\le s.length, t.length \\le 5 \\cdot 10^4$\n- `s` and `t` consist of lowercase English letters.",
        "starter_code_python": "def isAnagram(s: str, t: str) -> bool:\n    # Write your solution here\n    pass\n",
        "reference_solution_python": "def isAnagram(s: str, t: str) -> bool:\n    if len(s) != len(t): return False\n    count = {}\n    for c in s:\n        count[c] = count.get(c, 0) + 1\n    for c in t:\n        if c not in count or count[c] == 0:\n            return False\n        count[c] -= 1\n    return True\n",
        "test_cases": [
            {"input_data": "{\"s\": \"anagram\", \"t\": \"nagaram\"}", "expected_output": "true", "is_hidden": False},
            {"input_data": "{\"s\": \"rat\", \"t\": \"car\"}", "expected_output": "false", "is_hidden": False},
            {"input_data": "{\"s\": \"a\", \"t\": \"ab\"}", "expected_output": "false", "is_hidden": True},
        ]
    },
    {
        "title": "Valid Palindrome",
        "slug": "valid-palindrome",
        "topic_slug": "strings",
        "difficulty": "Easy",
        "is_diagnostic": False,
        "order_index": 7,
        "description_markdown": "A phrase is a **palindrome** if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward.\n\nGiven a string `s`, return `True` if it is a palindrome, or `False` otherwise.",
        "constraints_markdown": "- $1 \\le s.length \\le 2 \\cdot 10^5$\n- `s` consists only of printable ASCII characters.",
        "starter_code_python": "def isPalindrome(s: str) -> bool:\n    # Write your solution here\n    pass\n",
        "reference_solution_python": "def isPalindrome(s: str) -> bool:\n    filtered = [c.lower() for c in s if c.isalnum()]\n    return filtered == filtered[::-1]\n",
        "test_cases": [
            {"input_data": "{\"s\": \"A man, a plan, a canal: Panama\"}", "expected_output": "true", "is_hidden": False},
            {"input_data": "{\"s\": \"race a car\"}", "expected_output": "false", "is_hidden": False},
            {"input_data": "{\"s\": \" \"}", "expected_output": "true", "is_hidden": True},
        ]
    },
    {
        "title": "Longest Substring Without Repeating Characters",
        "slug": "longest-substring-without-repeating-characters",
        "topic_slug": "strings",
        "difficulty": "Medium",
        "is_diagnostic": False,
        "order_index": 8,
        "description_markdown": "Given a string `s`, find the length of the **longest substring** without repeating characters.",
        "constraints_markdown": "- $0 \\le s.length \\le 5 \\cdot 10^4$\n- `s` consists of English letters, digits, symbols and spaces.",
        "starter_code_python": "def lengthOfLongestSubstring(s: str) -> int:\n    # Write your solution here\n    pass\n",
        "reference_solution_python": "def lengthOfLongestSubstring(s: str) -> int:\n    char_set = set()\n    l = 0\n    res = 0\n    for r in range(len(s)):\n        while s[r] in char_set:\n            char_set.remove(s[l])\n            l += 1\n        char_set.add(s[r])\n        res = max(res, r - l + 1)\n    return res\n",
        "test_cases": [
            {"input_data": "{\"s\": \"abcabcbb\"}", "expected_output": "3", "is_hidden": False},
            {"input_data": "{\"s\": \"bbbbb\"}", "expected_output": "1", "is_hidden": False},
            {"input_data": "{\"s\": \"pwwkew\"}", "expected_output": "3", "is_hidden": True},
        ]
    },
    {
        "title": "Group Anagrams",
        "slug": "group-anagrams",
        "topic_slug": "strings",
        "difficulty": "Medium",
        "is_diagnostic": False,
        "order_index": 9,
        "description_markdown": "Given an array of strings `strs`, group the anagrams together. You can return the answer in any order.",
        "constraints_markdown": "- $1 \\le \\text{strs.length} \\le 10^4$\n- $0 \\le \\text{strs}[i].length \\le 100$",
        "starter_code_python": "def groupAnagrams(strs: list[str]) -> list[list[str]]:\n    # Write your solution here\n    pass\n",
        "reference_solution_python": "from collections import defaultdict\ndef groupAnagrams(strs: list[str]) -> list[list[str]]:\n    ans = defaultdict(list)\n    for s in strs:\n        ans[\"\".join(sorted(s))].append(s)\n    return [sorted(group) for group in sorted(ans.values())]\n",
        "test_cases": [
            {"input_data": "{\"strs\": [\"eat\", \"tea\", \"tan\", \"ate\", \"nat\", \"bat\"]}", "expected_output": "[[\"ate\", \"eat\", \"tea\"], [\"bat\"], [\"nat\", \"tan\"]]", "is_hidden": False},
            {"input_data": "{\"strs\": [\"\"]}", "expected_output": "[[\"\"]]", "is_hidden": False},
        ]
    },

    # ------------------ 3. HASHING ------------------
    {
        "title": "Subarray Sum Equals K",
        "slug": "subarray-sum-equals-k",
        "topic_slug": "hashing",
        "difficulty": "Medium",
        "is_diagnostic": True,
        "order_index": 10,
        "description_markdown": "Given an array of integers `nums` and an integer `k`, return the total number of subarrays whose sum equals to `k`.\n\nA subarray is a contiguous non-empty sequence of elements within an array.",
        "constraints_markdown": "- $1 \\le \\text{nums.length} \\le 2 \\cdot 10^4$\n- $-1000 \\le \\text{nums}[i] \\le 1000$\n- $-10^7 \\le k \\le 10^7$",
        "starter_code_python": "def subarraySum(nums: list[int], k: int) -> int:\n    # Write your solution here\n    pass\n",
        "reference_solution_python": "def subarraySum(nums: list[int], k: int) -> int:\n    count = 0\n    curr_sum = 0\n    prefix_counts = {0: 1}\n    for n in nums:\n        curr_sum += n\n        if curr_sum - k in prefix_counts:\n            count += prefix_counts[curr_sum - k]\n        prefix_counts[curr_sum] = prefix_counts.get(curr_sum, 0) + 1\n    return count\n",
        "test_cases": [
            {"input_data": "{\"nums\": [1, 1, 1], \"k\": 2}", "expected_output": "2", "is_hidden": False},
            {"input_data": "{\"nums\": [1, 2, 3], \"k\": 3}", "expected_output": "2", "is_hidden": False},
            {"input_data": "{\"nums\": [1, -1, 0], \"k\": 0}", "expected_output": "3", "is_hidden": True},
        ]
    },
    {
        "title": "Contains Duplicate",
        "slug": "contains-duplicate",
        "topic_slug": "hashing",
        "difficulty": "Easy",
        "is_diagnostic": False,
        "order_index": 11,
        "description_markdown": "Given an integer array `nums`, return `True` if any value appears **at least twice** in the array, and return `False` if every element is distinct.",
        "constraints_markdown": "- $1 \\le \\text{nums.length} \\le 10^5$\n- $-10^9 \\le \\text{nums}[i] \\le 10^9$",
        "starter_code_python": "def containsDuplicate(nums: list[int]) -> bool:\n    # Write your solution here\n    pass\n",
        "reference_solution_python": "def containsDuplicate(nums: list[int]) -> bool:\n    return len(nums) != len(set(nums))\n",
        "test_cases": [
            {"input_data": "{\"nums\": [1, 2, 3, 1]}", "expected_output": "true", "is_hidden": False},
            {"input_data": "{\"nums\": [1, 2, 3, 4]}", "expected_output": "false", "is_hidden": False},
        ]
    },
    {
        "title": "Top K Frequent Elements",
        "slug": "top-k-frequent-elements",
        "topic_slug": "hashing",
        "difficulty": "Medium",
        "is_diagnostic": False,
        "order_index": 12,
        "description_markdown": "Given an integer array `nums` and an integer `k`, return the `k` most frequent elements. You may return the answer in any sorted order.",
        "constraints_markdown": "- $1 \\le \\text{nums.length} \\le 10^5$\n- $k$ is in the range $[1, \\text{number of unique elements}]$",
        "starter_code_python": "def topKFrequent(nums: list[int], k: int) -> list[int]:\n    # Write your solution here\n    pass\n",
        "reference_solution_python": "from collections import Counter\ndef topKFrequent(nums: list[int], k: int) -> list[int]:\n    count = Counter(nums)\n    return sorted([item[0] for item in count.most_common(k)])\n",
        "test_cases": [
            {"input_data": "{\"nums\": [1, 1, 1, 2, 2, 3], \"k\": 2}", "expected_output": "[1, 2]", "is_hidden": False},
            {"input_data": "{\"nums\": [1], \"k\": 1}", "expected_output": "[1]", "is_hidden": False},
        ]
    },
    {
        "title": "Longest Consecutive Sequence",
        "slug": "longest-consecutive-sequence",
        "topic_slug": "hashing",
        "difficulty": "Medium",
        "is_diagnostic": False,
        "order_index": 13,
        "description_markdown": "Given an unsorted array of integers `nums`, return the length of the longest consecutive elements sequence.\n\nYou must write an algorithm that runs in $O(N)$ time.",
        "constraints_markdown": "- $0 \\le \\text{nums.length} \\le 10^5$\n- $-10^9 \\le \\text{nums}[i] \\le 10^9$",
        "starter_code_python": "def longestConsecutive(nums: list[int]) -> int:\n    # Write your solution here\n    pass\n",
        "reference_solution_python": "def longestConsecutive(nums: list[int]) -> int:\n    num_set = set(nums)\n    longest = 0\n    for n in num_set:\n        if (n - 1) not in num_set:\n            length = 1\n            while (n + length) in num_set:\n                length += 1\n            longest = max(longest, length)\n    return longest\n",
        "test_cases": [
            {"input_data": "{\"nums\": [100, 4, 200, 1, 3, 2]}", "expected_output": "4", "is_hidden": False},
            {"input_data": "{\"nums\": [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]}", "expected_output": "9", "is_hidden": False},
        ]
    },

    # ------------------ 4. LINKED LISTS ------------------
    {
        "title": "Reverse Linked List",
        "slug": "reverse-linked-list",
        "topic_slug": "linked-lists",
        "difficulty": "Easy",
        "is_diagnostic": False,
        "order_index": 14,
        "description_markdown": "Given the `head` of a singly linked list represented as a list of integers, reverse the list, and return the reversed list values.",
        "constraints_markdown": "- The number of nodes in the list is in the range $[0, 5000]$.\n- $-5000 \\le \\text{Node.val} \\le 5000$",
        "starter_code_python": "def reverseList(head: list[int]) -> list[int]:\n    # Write your solution here\n    pass\n",
        "reference_solution_python": "def reverseList(head: list[int]) -> list[int]:\n    return head[::-1]\n",
        "test_cases": [
            {"input_data": "{\"head\": [1, 2, 3, 4, 5]}", "expected_output": "[5, 4, 3, 2, 1]", "is_hidden": False},
            {"input_data": "{\"head\": [1, 2]}", "expected_output": "[2, 1]", "is_hidden": False},
            {"input_data": "{\"head\": []}", "expected_output": "[]", "is_hidden": True},
        ]
    },
    {
        "title": "Merge Two Sorted Lists",
        "slug": "merge-two-sorted-lists",
        "topic_slug": "linked-lists",
        "difficulty": "Easy",
        "is_diagnostic": False,
        "order_index": 15,
        "description_markdown": "You are given two sorted integer arrays `list1` and `list2`. Merge the two lists into one sorted list and return it.",
        "constraints_markdown": "- The number of nodes in both lists is in the range $[0, 50]$.\n- $-100 \\le \\text{val} \\le 100$",
        "starter_code_python": "def mergeTwoLists(list1: list[int], list2: list[int]) -> list[int]:\n    # Write your solution here\n    pass\n",
        "reference_solution_python": "def mergeTwoLists(list1: list[int], list2: list[int]) -> list[int]:\n    return sorted(list1 + list2)\n",
        "test_cases": [
            {"input_data": "{\"list1\": [1, 2, 4], \"list2\": [1, 3, 4]}", "expected_output": "[1, 1, 2, 3, 4, 4]", "is_hidden": False},
            {"input_data": "{\"list1\": [], \"list2\": []}", "expected_output": "[]", "is_hidden": False},
        ]
    },
    {
        "title": "Remove Nth Node From End of List",
        "slug": "remove-nth-node-from-end-of-list",
        "topic_slug": "linked-lists",
        "difficulty": "Medium",
        "is_diagnostic": False,
        "order_index": 16,
        "description_markdown": "Given the `head` array of a linked list, remove the $n^{\\text{th}}$ node from the end of the list and return its head array.",
        "constraints_markdown": "- The number of nodes in the list is `sz` ($1 \\le sz \\le 30$).\n- $1 \\le n \\le sz$",
        "starter_code_python": "def removeNthFromEnd(head: list[int], n: int) -> list[int]:\n    # Write your solution here\n    pass\n",
        "reference_solution_python": "def removeNthFromEnd(head: list[int], n: int) -> list[int]:\n    idx = len(head) - n\n    return head[:idx] + head[idx+1:]\n",
        "test_cases": [
            {"input_data": "{\"head\": [1, 2, 3, 4, 5], \"n\": 2}", "expected_output": "[1, 2, 3, 5]", "is_hidden": False},
            {"input_data": "{\"head\": [1], \"n\": 1}", "expected_output": "[]", "is_hidden": False},
        ]
    },

    # ------------------ 5. STACK & QUEUE ------------------
    {
        "title": "Valid Parentheses String",
        "slug": "valid-parentheses",
        "topic_slug": "stack-queue",
        "difficulty": "Easy",
        "is_diagnostic": False,
        "order_index": 17,
        "description_markdown": "Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.",
        "constraints_markdown": "- $1 \\le s.length \\le 10^4$",
        "starter_code_python": "def isValid(s: str) -> bool:\n    # Write your solution here\n    pass\n",
        "reference_solution_python": "def isValid(s: str) -> bool:\n    stack = []\n    mapping = {')': '(', '}': '{', ']': '['}\n    for char in s:\n        if char in mapping:\n            top = stack.pop() if stack else '#'\n            if mapping[char] != top:\n                return False\n        else:\n            stack.append(char)\n    return not stack\n",
        "test_cases": [
            {"input_data": "{\"s\": \"()[]{}\"}", "expected_output": "true", "is_hidden": False},
            {"input_data": "{\"s\": \"(]\"}", "expected_output": "false", "is_hidden": False},
            {"input_data": "{\"s\": \"([{}])\"}", "expected_output": "true", "is_hidden": True},
        ]
    },
    {
        "title": "Evaluate Reverse Polish Notation",
        "slug": "evaluate-reverse-polish-notation",
        "topic_slug": "stack-queue",
        "difficulty": "Medium",
        "is_diagnostic": True,
        "order_index": 18,
        "description_markdown": "You are given an array of strings `tokens` that represents an arithmetic expression in a **Reverse Polish Notation**.\n\nEvaluate the expression and return an integer that represents the value of the expression.",
        "constraints_markdown": "- $1 \\le \\text{tokens.length} \\le 10^4$\n- `tokens[i]` is either an operator: `\"+\"`, `\"-\"`, `\"*\"`, or `\"/\"`, or an integer.",
        "starter_code_python": "def evalRPN(tokens: list[str]) -> int:\n    # Write your solution here\n    pass\n",
        "reference_solution_python": "def evalRPN(tokens: list[str]) -> int:\n    stack = []\n    for t in tokens:\n        if t in '+-*/':\n            b, a = stack.pop(), stack.pop()\n            if t == '+': stack.append(a + b)\n            elif t == '-': stack.append(a - b)\n            elif t == '*': stack.append(a * b)\n            elif t == '/': stack.append(int(a / b))\n        else:\n            stack.append(int(t))\n    return stack[0]\n",
        "test_cases": [
            {"input_data": "{\"tokens\": [\"2\", \"1\", \"+\", \"3\", \"*\"]}", "expected_output": "9", "is_hidden": False},
            {"input_data": "{\"tokens\": [\"4\", \"13\", \"5\", \"/\", \"+\"]}", "expected_output": "6", "is_hidden": False},
            {"input_data": "{\"tokens\": [\"10\", \"6\", \"9\", \"3\", \"+\", \"-11\", \"*\", \"/\", \"*\", \"17\", \"+\", \"5\", \"+\"]}", "expected_output": "22", "is_hidden": True},
        ]
    },
    {
        "title": "Daily Temperatures Next Warmer Day",
        "slug": "daily-temperatures",
        "topic_slug": "stack-queue",
        "difficulty": "Medium",
        "is_diagnostic": False,
        "order_index": 19,
        "description_markdown": "Given an array of integers `temperatures` represents the daily temperatures, return an array `answer` such that `answer[i]` is the number of days you have to wait after the $i^{\\text{th}}$ day to get a warmer temperature. If there is no future day, keep `answer[i] == 0`.",
        "constraints_markdown": "- $1 \\le \\text{temperatures.length} \\le 10^5$\n- $30 \\le \\text{temperatures}[i] \\le 100$",
        "starter_code_python": "def dailyTemperatures(temperatures: list[int]) -> list[int]:\n    # Write your solution here\n    pass\n",
        "reference_solution_python": "def dailyTemperatures(temperatures: list[int]) -> list[int]:\n    res = [0] * len(temperatures)\n    stack = [] # (temp, idx)\n    for i, t in enumerate(temperatures):\n        while stack and t > stack[-1][0]:\n            _, prev_i = stack.pop()\n            res[prev_i] = i - prev_i\n        stack.append((t, i))\n    return res\n",
        "test_cases": [
            {"input_data": "{\"temperatures\": [73, 74, 75, 71, 69, 72, 76, 73]}", "expected_output": "[1, 1, 4, 2, 1, 1, 0, 0]", "is_hidden": False},
            {"input_data": "{\"temperatures\": [30, 40, 50, 60]}", "expected_output": "[1, 1, 1, 0]", "is_hidden": False},
        ]
    },
    {
        "title": "Largest Rectangle in Histogram",
        "slug": "largest-rectangle-in-histogram",
        "topic_slug": "stack-queue",
        "difficulty": "Hard",
        "is_diagnostic": False,
        "order_index": 20,
        "description_markdown": "Given an array of integers `heights` representing the histogram's bar height where the width of each bar is 1, return the area of the largest rectangle in the histogram.",
        "constraints_markdown": "- $1 \\le \\text{heights.length} \\le 10^5$\n- $0 \\le \\text{heights}[i] \\le 10^4$",
        "starter_code_python": "def largestRectangleArea(heights: list[int]) -> int:\n    # Write your solution here\n    pass\n",
        "reference_solution_python": "def largestRectangleArea(heights: list[int]) -> int:\n    max_area = 0\n    stack = [] # (index, height)\n    for i, h in enumerate(heights):\n        start = i\n        while stack and stack[-1][1] > h:\n            idx, height = stack.pop()\n            max_area = max(max_area, height * (i - idx))\n            start = idx\n        stack.append((start, h))\n    for i, h in stack:\n        max_area = max(max_area, h * (len(heights) - i))\n    return max_area\n",
        "test_cases": [
            {"input_data": "{\"heights\": [2, 1, 5, 6, 2, 3]}", "expected_output": "10", "is_hidden": False},
            {"input_data": "{\"heights\": [2, 4]}", "expected_output": "4", "is_hidden": False},
        ]
    },

    # ------------------ 6. TREES ------------------
    {
        "title": "Maximum Depth of Binary Tree",
        "slug": "maximum-depth-of-binary-tree",
        "topic_slug": "trees",
        "difficulty": "Easy",
        "is_diagnostic": True,
        "order_index": 21,
        "description_markdown": "Given the root of a binary tree encoded as a level-order list (with `None` for missing nodes), return its maximum depth.\n\nA binary tree's **maximum depth** is the number of nodes along the longest path from the root node down to the farthest leaf node.",
        "constraints_markdown": "- The number of nodes in the tree is in the range $[0, 10^4]$.\n- $-100 \\le \\text{Node.val} \\le 100$",
        "starter_code_python": "def maxDepth(root: list) -> int:\n    # Write your solution here\n    pass\n",
        "reference_solution_python": "def maxDepth(root: list) -> int:\n    if not root or root[0] is None: return 0\n    depth = 0\n    level = [0]\n    n = len(root)\n    while level:\n        next_level = []\n        depth += 1\n        for idx in level:\n            left, right = 2 * idx + 1, 2 * idx + 2\n            if left < n and root[left] is not None: next_level.append(left)\n            if right < n and root[right] is not None: next_level.append(right)\n        level = next_level\n    return depth\n",
        "test_cases": [
            {"input_data": "{\"root\": [3, 9, 20, null, null, 15, 7]}", "expected_output": "3", "is_hidden": False},
            {"input_data": "{\"root\": [1, null, 2]}", "expected_output": "2", "is_hidden": False},
            {"input_data": "{\"root\": []}", "expected_output": "0", "is_hidden": True},
        ]
    },
    {
        "title": "Invert Binary Tree",
        "slug": "invert-binary-tree",
        "topic_slug": "trees",
        "difficulty": "Easy",
        "is_diagnostic": False,
        "order_index": 22,
        "description_markdown": "Given the root of a binary tree as an array, invert the tree (swap left and right child at every level), and return its array representation.",
        "constraints_markdown": "- The number of nodes in the tree is in the range $[0, 100]$.",
        "starter_code_python": "def invertTree(root: list) -> list:\n    # Write your solution here\n    pass\n",
        "reference_solution_python": "def invertTree(root: list) -> list:\n    if not root: return []\n    res = list(root)\n    n = len(res)\n    level = 1\n    idx = 0\n    while idx < n:\n        end = min(idx + (1 << (level - 1)), n)\n        sub = res[idx:end]\n        res[idx:end] = sub[::-1]\n        idx = end\n        level += 1\n    return res\n",
        "test_cases": [
            {"input_data": "{\"root\": [4, 2, 7, 1, 3, 6, 9]}", "expected_output": "[4, 7, 2, 9, 6, 3, 1]", "is_hidden": False},
            {"input_data": "{\"root\": [2, 1, 3]}", "expected_output": "[2, 3, 1]", "is_hidden": False},
        ]
    },
    {
        "title": "Lowest Common Ancestor of a BST",
        "slug": "lowest-common-ancestor-of-bst",
        "topic_slug": "trees",
        "difficulty": "Medium",
        "is_diagnostic": False,
        "order_index": 23,
        "description_markdown": "Given a Binary Search Tree represented as an array and two values `p` and `q`, return the value of the Lowest Common Ancestor (LCA) node.",
        "constraints_markdown": "- All node values are unique.\n- `p` and `q` will exist in the BST.",
        "starter_code_python": "def lowestCommonAncestor(root: list, p: int, q: int) -> int:\n    # Write your solution here\n    pass\n",
        "reference_solution_python": "def lowestCommonAncestor(root: list, p: int, q: int) -> int:\n    curr = 0\n    while curr < len(root) and root[curr] is not None:\n        val = root[curr]\n        if p > val and q > val:\n            curr = 2 * curr + 2\n        elif p < val and q < val:\n            curr = 2 * curr + 1\n        else:\n            return val\n    return root[0]\n",
        "test_cases": [
            {"input_data": "{\"root\": [6, 2, 8, 0, 4, 7, 9], \"p\": 2, \"q\": 8}", "expected_output": "6", "is_hidden": False},
            {"input_data": "{\"root\": [6, 2, 8, 0, 4, 7, 9], \"p\": 2, \"q\": 4}", "expected_output": "2", "is_hidden": False},
        ]
    },
    {
        "title": "Validate Binary Search Tree",
        "slug": "validate-binary-search-tree",
        "topic_slug": "trees",
        "difficulty": "Medium",
        "is_diagnostic": False,
        "order_index": 24,
        "description_markdown": "Given the root of a binary tree represented as an array, determine if it is a valid binary search tree (BST).",
        "constraints_markdown": "- The number of nodes in the tree is in the range $[1, 10^4]$.",
        "starter_code_python": "def isValidBST(root: list) -> bool:\n    # Write your solution here\n    pass\n",
        "reference_solution_python": "def isValidBST(root: list) -> bool:\n    def helper(idx, low, high):\n        if idx >= len(root) or root[idx] is None: return True\n        val = root[idx]\n        if val <= low or val >= high: return False\n        return helper(2 * idx + 1, low, val) and helper(2 * idx + 2, val, high)\n    return helper(0, float('-inf'), float('inf'))\n",
        "test_cases": [
            {"input_data": "{\"root\": [2, 1, 3]}", "expected_output": "true", "is_hidden": False},
            {"input_data": "{\"root\": [5, 1, 4, null, null, 3, 6]}", "expected_output": "false", "is_hidden": False},
        ]
    },
    {
        "title": "Binary Tree Maximum Path Sum",
        "slug": "binary-tree-maximum-path-sum",
        "topic_slug": "trees",
        "difficulty": "Hard",
        "is_diagnostic": False,
        "order_index": 25,
        "description_markdown": "A path in a binary tree is a sequence of nodes where each pair of adjacent nodes has an edge. Find the maximum path sum of any non-empty path.",
        "constraints_markdown": "- The number of nodes in the tree is in the range $[1, 3 \\cdot 10^4]$.\n- $-1000 \\le \\text{Node.val} \\le 1000$",
        "starter_code_python": "def maxPathSum(root: list) -> int:\n    # Write your solution here\n    pass\n",
        "reference_solution_python": "def maxPathSum(root: list) -> int:\n    max_sum = [float('-inf')]\n    def helper(idx):\n        if idx >= len(root) or root[idx] is None: return 0\n        left = max(0, helper(2 * idx + 1))\n        right = max(0, helper(2 * idx + 2))\n        max_sum[0] = max(max_sum[0], root[idx] + left + right)\n        return root[idx] + max(left, right)\n    helper(0)\n    return max_sum[0]\n",
        "test_cases": [
            {"input_data": "{\"root\": [1, 2, 3]}", "expected_output": "6", "is_hidden": False},
            {"input_data": "{\"root\": [-10, 9, 20, null, null, 15, 7]}", "expected_output": "42", "is_hidden": False},
        ]
    },

    # ------------------ 7. GRAPHS ------------------
    {
        "title": "Number of Connected Islands",
        "slug": "number-of-connected-islands",
        "topic_slug": "graphs",
        "difficulty": "Medium",
        "is_diagnostic": True,
        "order_index": 26,
        "description_markdown": "Given an `m x n` 2D binary grid `grid` which represents a map of `'1'`s (land) and `'0'`s (water), return the number of islands.\n\nAn **island** is surrounded by water and is formed by connecting adjacent lands horizontally or vertically.",
        "constraints_markdown": "- $m == \\text{grid.length}$\n- $n == \\text{grid}[i].length$\n- $1 \\le m, n \\le 300$",
        "starter_code_python": "def numIslands(grid: list[list[str]]) -> int:\n    # Write your solution here\n    pass\n",
        "reference_solution_python": "def numIslands(grid: list[list[str]]) -> int:\n    if not grid: return 0\n    rows, cols = len(grid), len(grid[0])\n    count = 0\n    def dfs(r, c):\n        if r < 0 or c < 0 or r >= rows or c >= cols or grid[r][c] != '1': return\n        grid[r][c] = '#' # visited\n        for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:\n            dfs(r + dr, c + dc)\n    for r in range(rows):\n        for c in range(cols):\n            if grid[r][c] == '1':\n                dfs(r, c)\n                count += 1\n    return count\n",
        "test_cases": [
            {"input_data": "{\"grid\": [[\"1\",\"1\",\"1\",\"1\",\"0\"],[\"1\",\"1\",\"0\",\"1\",\"0\"],[\"1\",\"1\",\"0\",\"0\",\"0\"],[\"0\",\"0\",\"0\",\"0\",\"0\"]]}", "expected_output": "1", "is_hidden": False},
            {"input_data": "{\"grid\": [[\"1\",\"1\",\"0\",\"0\",\"0\"],[\"1\",\"1\",\"0\",\"0\",\"0\"],[\"0\",\"0\",\"1\",\"0\",\"0\"],[\"0\",\"0\",\"0\",\"1\",\"1\"]]}", "expected_output": "3", "is_hidden": False},
        ]
    },
    {
        "title": "Clone Graph",
        "slug": "clone-graph",
        "topic_slug": "graphs",
        "difficulty": "Medium",
        "is_diagnostic": False,
        "order_index": 27,
        "description_markdown": "Given an adjacency list representing an undirected connected graph `adjList`, return a deep copy (clone) adjacency list of the graph.",
        "constraints_markdown": "- The number of nodes in the graph is in the range $[0, 100]$.",
        "starter_code_python": "def cloneGraph(adjList: list[list[int]]) -> list[list[int]]:\n    # Write your solution here\n    pass\n",
        "reference_solution_python": "def cloneGraph(adjList: list[list[int]]) -> list[list[int]]:\n    return [list(neighbors) for neighbors in adjList]\n",
        "test_cases": [
            {"input_data": "{\"adjList\": [[2,4],[1,3],[2,4],[1,3]]}", "expected_output": "[[2, 4], [1, 3], [2, 4], [1, 3]]", "is_hidden": False},
            {"input_data": "{\"adjList\": [[]]}", "expected_output": "[[]]", "is_hidden": False},
        ]
    },
    {
        "title": "Course Schedule Cycle Detection",
        "slug": "course-schedule",
        "topic_slug": "graphs",
        "difficulty": "Medium",
        "is_diagnostic": False,
        "order_index": 28,
        "description_markdown": "There are a total of `numCourses` courses you have to take, labeled from `0` to `numCourses - 1`. You are given an array `prerequisites` where `prerequisites[i] = [a, b]` indicates you must take course `b` before course `a`.\n\nReturn `True` if you can finish all courses, or `False` if there is a cycle.",
        "constraints_markdown": "- $1 \\le \\text{numCourses} \\le 2000$\n- $0 \\le \\text{prerequisites.length} \\le 5000$",
        "starter_code_python": "def canFinish(numCourses: int, prerequisites: list[list[int]]) -> bool:\n    # Write your solution here\n    pass\n",
        "reference_solution_python": "def canFinish(numCourses: int, prerequisites: list[list[int]]) -> bool:\n    preMap = {i: [] for i in range(numCourses)}\n    for crs, pre in prerequisites:\n        preMap[crs].append(pre)\n    visiting = set()\n    visited = set()\n    def dfs(crs):\n        if crs in visiting: return False\n        if crs in visited: return True\n        visiting.add(crs)\n        for pre in preMap[crs]:\n            if not dfs(pre): return False\n        visiting.remove(crs)\n        visited.add(crs)\n        return True\n    for c in range(numCourses):\n        if not dfs(c): return False\n    return True\n",
        "test_cases": [
            {"input_data": "{\"numCourses\": 2, \"prerequisites\": [[1, 0]]}", "expected_output": "true", "is_hidden": False},
            {"input_data": "{\"numCourses\": 2, \"prerequisites\": [[1, 0], [0, 1]]}", "expected_output": "false", "is_hidden": False},
        ]
    },
    {
        "title": "Word Ladder Shortest Transformation",
        "slug": "word-ladder",
        "topic_slug": "graphs",
        "difficulty": "Hard",
        "is_diagnostic": False,
        "order_index": 29,
        "description_markdown": "A transformation sequence from word `beginWord` to word `endWord` using a dictionary `wordList` is a sequence where each adjacent pair differs by a single letter. Return the number of words in the shortest transformation sequence.",
        "constraints_markdown": "- $1 \\le \\text{beginWord.length} \\le 10$\n- $1 \\le \\text{wordList.length} \\le 5000$",
        "starter_code_python": "def ladderLength(beginWord: str, endWord: str, wordList: list[str]) -> int:\n    # Write your solution here\n    pass\n",
        "reference_solution_python": "from collections import deque\ndef ladderLength(beginWord: str, endWord: str, wordList: list[str]) -> int:\n    words = set(wordList)\n    if endWord not in words: return 0\n    queue = deque([(beginWord, 1)])\n    visited = {beginWord}\n    while queue:\n        word, dist = queue.popleft()\n        if word == endWord: return dist\n        for i in range(len(word)):\n            for c in 'abcdefghijklmnopqrstuvwxyz':\n                next_word = word[:i] + c + word[i+1:]\n                if next_word in words and next_word not in visited:\n                    visited.add(next_word)\n                    queue.append((next_word, dist + 1))\n    return 0\n",
        "test_cases": [
            {"input_data": "{\"beginWord\": \"hit\", \"endWord\": \"cog\", \"wordList\": [\"hot\",\"dot\",\"dog\",\"lot\",\"log\",\"cog\"]}", "expected_output": "5", "is_hidden": False},
            {"input_data": "{\"beginWord\": \"hit\", \"endWord\": \"cog\", \"wordList\": [\"hot\",\"dot\",\"dog\",\"lot\",\"log\"]}", "expected_output": "0", "is_hidden": False},
        ]
    },

    # ------------------ 8. GREEDY ------------------
    {
        "title": "Jump Game Can Reach End",
        "slug": "jump-game",
        "topic_slug": "greedy",
        "difficulty": "Medium",
        "is_diagnostic": False,
        "order_index": 30,
        "description_markdown": "You are given an integer array `nums`. You are initially positioned at the array's first index, and each element in the array represents your maximum jump length at that position. Return `True` if you can reach the last index.",
        "constraints_markdown": "- $1 \\le \\text{nums.length} \\le 10^4$\n- $0 \\le \\text{nums}[i] \\le 10^5$",
        "starter_code_python": "def canJump(nums: list[int]) -> bool:\n    # Write your solution here\n    pass\n",
        "reference_solution_python": "def canJump(nums: list[int]) -> bool:\n    goal = len(nums) - 1\n    for i in range(len(nums) - 1, -1, -1):\n        if i + nums[i] >= goal:\n            goal = i\n    return goal == 0\n",
        "test_cases": [
            {"input_data": "{\"nums\": [2, 3, 1, 1, 4]}", "expected_output": "true", "is_hidden": False},
            {"input_data": "{\"nums\": [3, 2, 1, 0, 4]}", "expected_output": "false", "is_hidden": False},
        ]
    },
    {
        "title": "Gas Station Circuit",
        "slug": "gas-station",
        "topic_slug": "greedy",
        "difficulty": "Medium",
        "is_diagnostic": False,
        "order_index": 31,
        "description_markdown": "There are `n` gas stations along a circular route, where the amount of gas at the $i^{\\text{th}}$ station is `gas[i]`. Traveling from station `i` to `i + 1` costs `cost[i]`. Return the starting gas station index if you can travel around the circuit once clockwise.",
        "constraints_markdown": "- $n == \\text{gas.length} == \\text{cost.length}$\n- $1 \\le n \\le 10^5$",
        "starter_code_python": "def canCompleteCircuit(gas: list[int], cost: list[int]) -> int:\n    # Write your solution here\n    pass\n",
        "reference_solution_python": "def canCompleteCircuit(gas: list[int], cost: list[int]) -> int:\n    if sum(gas) < sum(cost): return -1\n    total = 0\n    start = 0\n    for i in range(len(gas)):\n        total += gas[i] - cost[i]\n        if total < 0:\n            total = 0\n            start = i + 1\n    return start\n",
        "test_cases": [
            {"input_data": "{\"gas\": [1, 2, 3, 4, 5], \"cost\": [3, 4, 5, 1, 2]}", "expected_output": "3", "is_hidden": False},
            {"input_data": "{\"gas\": [2, 3, 4], \"cost\": [3, 4, 3]}", "expected_output": "-1", "is_hidden": False},
        ]
    },
    {
        "title": "Task Scheduler Minimum Intervals",
        "slug": "task-scheduler",
        "topic_slug": "greedy",
        "difficulty": "Medium",
        "is_diagnostic": False,
        "order_index": 32,
        "description_markdown": "Given a characters array `tasks`, representing the tasks a CPU needs to do, and a cooldown integer `n`, return the least number of units of times that the CPU will take to finish all the given tasks.",
        "constraints_markdown": "- $1 \\le \\text{tasks.length} \\le 10^4$\n- $0 \\le n \\le 100$",
        "starter_code_python": "def leastInterval(tasks: list[str], n: int) -> int:\n    # Write your solution here\n    pass\n",
        "reference_solution_python": "from collections import Counter\ndef leastInterval(tasks: list[str], n: int) -> int:\n    counts = Counter(tasks)\n    max_count = max(counts.values())\n    num_max = sum(1 for v in counts.values() if v == max_count)\n    return max(len(tasks), (max_count - 1) * (n + 1) + num_max)\n",
        "test_cases": [
            {"input_data": "{\"tasks\": [\"A\",\"A\",\"A\",\"B\",\"B\",\"B\"], \"n\": 2}", "expected_output": "8", "is_hidden": False},
            {"input_data": "{\"tasks\": [\"A\",\"C\",\"A\",\"B\",\"D\",\"B\"], \"n\": 1}", "expected_output": "6", "is_hidden": False},
        ]
    },

    # ------------------ 9. DYNAMIC PROGRAMMING ------------------
    {
        "title": "Climbing Stairs with Minimum Cost",
        "slug": "climbing-stairs-min-cost",
        "topic_slug": "dynamic-programming",
        "difficulty": "Easy",
        "is_diagnostic": True,
        "order_index": 33,
        "description_markdown": "You are given an integer array `cost` where `cost[i]` is the cost of $i^{\\text{th}}$ step on a staircase. Once you pay the cost, you can climb either one or two steps.\n\nYou can either start from index 0 or index 1. Return the minimum cost to reach the top of the floor.",
        "constraints_markdown": "- $2 \\le \\text{cost.length} \\le 1000$\n- $0 \\le \\text{cost}[i] \\le 999$",
        "starter_code_python": "def minCostClimbingStairs(cost: list[int]) -> int:\n    # Write your solution here\n    pass\n",
        "reference_solution_python": "def minCostClimbingStairs(cost: list[int]) -> int:\n    first, second = cost[0], cost[1]\n    for i in range(2, len(cost)):\n        curr = cost[i] + min(first, second)\n        first, second = second, curr\n    return min(first, second)\n",
        "test_cases": [
            {"input_data": "{\"cost\": [10, 15, 20]}", "expected_output": "15", "is_hidden": False},
            {"input_data": "{\"cost\": [1, 100, 1, 1, 1, 100, 1, 1, 100, 1]}", "expected_output": "6", "is_hidden": False},
            {"input_data": "{\"cost\": [0, 0, 0, 1]}", "expected_output": "0", "is_hidden": True},
        ]
    },
    {
        "title": "Coin Change Minimum Count",
        "slug": "coin-change",
        "topic_slug": "dynamic-programming",
        "difficulty": "Medium",
        "is_diagnostic": False,
        "order_index": 34,
        "description_markdown": "You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money.\n\nReturn the fewest number of coins that you need to make up that amount. If that amount cannot be made up, return -1.",
        "constraints_markdown": "- $1 \\le \\text{coins.length} \\le 12$\n- $0 \\le \\text{amount} \\le 10^4$",
        "starter_code_python": "def coinChange(coins: list[int], amount: int) -> int:\n    # Write your solution here\n    pass\n",
        "reference_solution_python": "def coinChange(coins: list[int], amount: int) -> int:\n    dp = [float('inf')] * (amount + 1)\n    dp[0] = 0\n    for a in range(1, amount + 1):\n        for c in coins:\n            if a - c >= 0:\n                dp[a] = min(dp[a], 1 + dp[a - c])\n    return dp[amount] if dp[amount] != float('inf') else -1\n",
        "test_cases": [
            {"input_data": "{\"coins\": [1, 2, 5], \"amount\": 11}", "expected_output": "3", "is_hidden": False},
            {"input_data": "{\"coins\": [2], \"amount\": 3}", "expected_output": "-1", "is_hidden": False},
            {"input_data": "{\"coins\": [1], \"amount\": 0}", "expected_output": "0", "is_hidden": True},
        ]
    },
    {
        "title": "Longest Increasing Subsequence",
        "slug": "longest-increasing-subsequence",
        "topic_slug": "dynamic-programming",
        "difficulty": "Medium",
        "is_diagnostic": False,
        "order_index": 35,
        "description_markdown": "Given an integer array `nums`, return the length of the longest strictly increasing subsequence.",
        "constraints_markdown": "- $1 \\le \\text{nums.length} \\le 2500$\n- $-10^4 \\le \\text{nums}[i] \\le 10^4$",
        "starter_code_python": "def lengthOfLIS(nums: list[int]) -> int:\n    # Write your solution here\n    pass\n",
        "reference_solution_python": "import bisect\ndef lengthOfLIS(nums: list[int]) -> int:\n    tails = []\n    for x in nums:\n        idx = bisect.bisect_left(tails, x)\n        if idx == len(tails):\n            tails.append(x)\n        else:\n            tails[idx] = x\n    return len(tails)\n",
        "test_cases": [
            {"input_data": "{\"nums\": [10, 9, 2, 5, 3, 7, 101, 18]}", "expected_output": "4", "is_hidden": False},
            {"input_data": "{\"nums\": [0, 1, 0, 3, 2, 3]}", "expected_output": "4", "is_hidden": False},
            {"input_data": "{\"nums\": [7, 7, 7, 7, 7]}", "expected_output": "1", "is_hidden": True},
        ]
    },
    {
        "title": "Unique Paths Grid Combinations",
        "slug": "unique-paths",
        "topic_slug": "dynamic-programming",
        "difficulty": "Medium",
        "is_diagnostic": False,
        "order_index": 36,
        "description_markdown": "There is a robot on an `m x n` grid. The robot is initially located at the top-left corner `(0, 0)`. The robot tries to move to the bottom-right corner `(m - 1, n - 1)`. The robot can only move down or right. Return the number of possible unique paths.",
        "constraints_markdown": "- $1 \\le m, n \\le 100$",
        "starter_code_python": "def uniquePaths(m: int, n: int) -> int:\n    # Write your solution here\n    pass\n",
        "reference_solution_python": "import math\ndef uniquePaths(m: int, n: int) -> int:\n    return math.comb(m + n - 2, m - 1)\n",
        "test_cases": [
            {"input_data": "{\"m\": 3, \"n\": 7}", "expected_output": "28", "is_hidden": False},
            {"input_data": "{\"m\": 3, \"n\": 2}", "expected_output": "3", "is_hidden": False},
        ]
    },
    {
        "title": "Edit Distance Levenshtein Transformation",
        "slug": "edit-distance",
        "topic_slug": "dynamic-programming",
        "difficulty": "Hard",
        "is_diagnostic": False,
        "order_index": 37,
        "description_markdown": "Given two strings `word1` and `word2`, return the minimum number of operations required to convert `word1` to `word2` (insert, delete, or replace character).",
        "constraints_markdown": "- $0 \\le \\text{word1.length}, \\text{word2.length} \\le 500$",
        "starter_code_python": "def minDistance(word1: str, word2: str) -> int:\n    # Write your solution here\n    pass\n",
        "reference_solution_python": "def minDistance(word1: str, word2: str) -> int:\n    m, n = len(word1), len(word2)\n    dp = [[0] * (n + 1) for _ in range(m + 1)]\n    for i in range(m + 1): dp[i][0] = i\n    for j in range(n + 1): dp[0][j] = j\n    for i in range(1, m + 1):\n        for j in range(1, n + 1):\n            if word1[i-1] == word2[j-1]:\n                dp[i][j] = dp[i-1][j-1]\n            else:\n                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])\n    return dp[m][n]\n",
        "test_cases": [
            {"input_data": "{\"word1\": \"horse\", \"word2\": \"ros\"}", "expected_output": "3", "is_hidden": False},
            {"input_data": "{\"word1\": \"intention\", \"word2\": \"execution\"}", "expected_output": "5", "is_hidden": False},
        ]
    },

    # ------------------ 10. BACKTRACKING ------------------
    {
        "title": "Subsets Power Set Generation",
        "slug": "subsets",
        "topic_slug": "backtracking",
        "difficulty": "Medium",
        "is_diagnostic": False,
        "order_index": 38,
        "description_markdown": "Given an integer array `nums` of unique elements, return all possible subsets (the power set). The solution set must not contain duplicate subsets. Return the subsets sorted.",
        "constraints_markdown": "- $1 \\le \\text{nums.length} \\le 10$\n- $-10 \\le \\text{nums}[i] \\le 10$",
        "starter_code_python": "def subsets(nums: list[int]) -> list[list[int]]:\n    # Write your solution here\n    pass\n",
        "reference_solution_python": "def subsets(nums: list[int]) -> list[list[int]]:\n    res = []\n    nums.sort()\n    def backtrack(start, path):\n        res.append(list(path))\n        for i in range(start, len(nums)):\n            path.append(nums[i])\n            backtrack(i + 1, path)\n            path.pop()\n    backtrack(0, [])\n    return sorted(res)\n",
        "test_cases": [
            {"input_data": "{\"nums\": [1, 2, 3]}", "expected_output": "[[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]", "is_hidden": False},
            {"input_data": "{\"nums\": [0]}", "expected_output": "[[], [0]]", "is_hidden": False},
        ]
    },
    {
        "title": "Combination Sum Target",
        "slug": "combination-sum",
        "topic_slug": "backtracking",
        "difficulty": "Medium",
        "is_diagnostic": False,
        "order_index": 39,
        "description_markdown": "Given an array of distinct integers `candidates` and a target integer `target`, return a list of all unique combinations of candidates where the chosen numbers sum to `target`. You may use the same number an unlimited number of times.",
        "constraints_markdown": "- $1 \\le \\text{candidates.length} \\le 30$\n- $2 \\le \\text{candidates}[i] \\le 40$\n- $1 \\le \\text{target} \\le 40$",
        "starter_code_python": "def combinationSum(candidates: list[int], target: int) -> list[list[int]]:\n    # Write your solution here\n    pass\n",
        "reference_solution_python": "def combinationSum(candidates: list[int], target: int) -> list[list[int]]:\n    res = []\n    def backtrack(remain, combo, start):\n        if remain == 0:\n            res.append(list(combo))\n            return\n        if remain < 0: return\n        for i in range(start, len(candidates)):\n            combo.append(candidates[i])\n            backtrack(remain - candidates[i], combo, i)\n            combo.pop()\n    backtrack(target, [], 0)\n    return sorted([sorted(x) for x in res])\n",
        "test_cases": [
            {"input_data": "{\"candidates\": [2, 3, 6, 7], \"target\": 7}", "expected_output": "[[2, 2, 3], [7]]", "is_hidden": False},
            {"input_data": "{\"candidates\": [2, 3, 5], \"target\": 8}", "expected_output": "[[2, 2, 2, 2], [2, 3, 3], [3, 5]]", "is_hidden": False},
        ]
    },
    {
        "title": "N-Queens Puzzle Solver",
        "slug": "n-queens",
        "topic_slug": "backtracking",
        "difficulty": "Hard",
        "is_diagnostic": False,
        "order_index": 40,
        "description_markdown": "The **n-queens** puzzle is the problem of placing `n` queens on an `n x n` chessboard such that no two queens attack each other. Return the number of distinct solutions to the n-queens puzzle.",
        "constraints_markdown": "- $1 \\le n \\le 9$",
        "starter_code_python": "def totalNQueens(n: int) -> int:\n    # Write your solution here\n    pass\n",
        "reference_solution_python": "def totalNQueens(n: int) -> int:\n    cols, pos_diag, neg_diag = set(), set(), set()\n    res = [0]\n    def backtrack(r):\n        if r == n:\n            res[0] += 1\n            return\n        for c in range(n):\n            if c in cols or (r + c) in pos_diag or (r - c) in neg_diag: continue\n            cols.add(c)\n            pos_diag.add(r + c)\n            neg_diag.add(r - c)\n            backtrack(r + 1)\n            cols.remove(c)\n            pos_diag.remove(r + c)\n            neg_diag.remove(r - c)\n    backtrack(0)\n    return res[0]\n",
        "test_cases": [
            {"input_data": "{\"n\": 4}", "expected_output": "2", "is_hidden": False},
            {"input_data": "{\"n\": 1}", "expected_output": "1", "is_hidden": False},
            {"input_data": "{\"n\": 8}", "expected_output": "92", "is_hidden": True},
        ]
    },
]

# Synchronize verified multi-language implementations into PROBLEMS_DATA
import json
import os

_MULTI_LANG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "multi_lang_dump.json")
if os.path.exists(_MULTI_LANG_PATH):
    try:
        with open(_MULTI_LANG_PATH, "r", encoding="utf-8") as _f:
            _multi_data = json.load(_f)
            for _p in PROBLEMS_DATA:
                _order = str(_p.get("order_index"))
                if _order in _multi_data:
                    for _k in [
                        "starter_code_java", "reference_solution_java",
                        "starter_code_cpp", "reference_solution_cpp",
                        "starter_code_javascript", "reference_solution_javascript"
                    ]:
                        if _k in _multi_data[_order]:
                            _p[_k] = _multi_data[_order][_k]
    except Exception as _e:
        logger.warning(f"Could not load multi_lang_dump.json: {_e}")


def seed_database(db: Session = None) -> dict:
    """
    Seeds Topics, Problems, and Test Cases into MySQL database.
    Idempotent: updates existing records or inserts new records.
    """
    should_close = False
    if db is None:
        db = SessionLocal()
        should_close = True

    try:
        # 1. Seed Topics
        topic_map = {}
        for t_data in TOPICS_DATA:
            topic = db.query(Topic).filter(Topic.slug == t_data["slug"]).first()
            if not topic:
                topic = Topic(
                    name=t_data["name"],
                    slug=t_data["slug"],
                    order_index=t_data["order_index"]
                )
                db.add(topic)
                db.flush()
            else:
                topic.name = t_data["name"]
                topic.order_index = t_data["order_index"]
                db.flush()
            topic_map[t_data["slug"]] = topic

        # 2. Seed Problems & Test Cases
        problems_seeded = 0
        test_cases_seeded = 0
        diagnostic_count = 0

        for p_data in PROBLEMS_DATA:
            topic = topic_map.get(p_data["topic_slug"])
            if not topic:
                logger.warning(f"Topic {p_data['topic_slug']} not found for problem {p_data['title']}")
                continue

            problem = db.query(Problem).filter(Problem.slug == p_data["slug"]).first()
            if not problem:
                problem = Problem(
                    title=p_data["title"],
                    slug=p_data["slug"],
                    topic_id=topic.id,
                    difficulty=p_data["difficulty"],
                    description_markdown=p_data["description_markdown"],
                    constraints_markdown=p_data.get("constraints_markdown"),
                    starter_code_python=p_data["starter_code_python"],
                    reference_solution_python=p_data.get("reference_solution_python"),
                    starter_code_java=p_data.get("starter_code_java"),
                    reference_solution_java=p_data.get("reference_solution_java"),
                    starter_code_cpp=p_data.get("starter_code_cpp"),
                    reference_solution_cpp=p_data.get("reference_solution_cpp"),
                    starter_code_javascript=p_data.get("starter_code_javascript"),
                    reference_solution_javascript=p_data.get("reference_solution_javascript"),
                    order_index=p_data.get("order_index", 0),
                    is_diagnostic=p_data.get("is_diagnostic", False)
                )
                db.add(problem)
                db.flush()
            else:
                problem.title = p_data["title"]
                problem.topic_id = topic.id
                problem.difficulty = p_data["difficulty"]
                problem.description_markdown = p_data["description_markdown"]
                problem.constraints_markdown = p_data.get("constraints_markdown")
                problem.starter_code_python = p_data["starter_code_python"]
                problem.reference_solution_python = p_data.get("reference_solution_python")
                if "starter_code_java" in p_data:
                    problem.starter_code_java = p_data["starter_code_java"]
                if "reference_solution_java" in p_data:
                    problem.reference_solution_java = p_data["reference_solution_java"]
                if "starter_code_cpp" in p_data:
                    problem.starter_code_cpp = p_data["starter_code_cpp"]
                if "reference_solution_cpp" in p_data:
                    problem.reference_solution_cpp = p_data["reference_solution_cpp"]
                if "starter_code_javascript" in p_data:
                    problem.starter_code_javascript = p_data["starter_code_javascript"]
                if "reference_solution_javascript" in p_data:
                    problem.reference_solution_javascript = p_data["reference_solution_javascript"]
                problem.order_index = p_data.get("order_index", 0)
                problem.is_diagnostic = p_data.get("is_diagnostic", False)
                db.flush()

            problems_seeded += 1
            if problem.is_diagnostic:
                diagnostic_count += 1

            # Seed Test Cases
            existing_tcs = {tc.order_index: tc for tc in problem.test_cases}
            for idx, tc_data in enumerate(p_data.get("test_cases", [])):
                if idx in existing_tcs:
                    tc = existing_tcs[idx]
                    tc.input_data = tc_data["input_data"]
                    tc.expected_output = tc_data["expected_output"]
                    tc.is_hidden = tc_data.get("is_hidden", False)
                else:
                    tc = TestCase(
                        problem_id=problem.id,
                        input_data=tc_data["input_data"],
                        expected_output=tc_data["expected_output"],
                        is_hidden=tc_data.get("is_hidden", False),
                        order_index=idx
                    )
                    db.add(tc)
                test_cases_seeded += 1

        db.commit()

        result = {
            "success": True,
            "topics_count": len(TOPICS_DATA),
            "problems_count": problems_seeded,
            "diagnostic_count": diagnostic_count,
            "test_cases_count": test_cases_seeded,
        }
        logger.info(f"Database seeded successfully: {result}")
        return result

    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding database: {e}")
        raise e
    finally:
        if should_close:
            db.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    res = seed_database()
    print("Seed Output:", res)
