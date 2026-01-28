---
name: java-python-code-reviewer
description: Comprehensive code reviewer for Java and Python implementations focusing on correctness, efficiency, code quality, and algorithmic optimization. Reviews LeetCode solutions, data structures, and algorithm implementations. Use when reviewing code, checking solutions, or providing feedback on implementations.
allowed-tools: Read, Glob, Grep, LSP
---

# Java & Python Code Reviewer

## When to use this Skill

Use this Skill when:
- Reviewing LeetCode problem solutions
- Checking code correctness and efficiency
- Comparing Java and Python implementations
- Providing feedback on algorithm implementations
- Optimizing existing solutions

## Review Framework

### 1. Correctness Analysis

**Check for:**
- Edge cases handling (empty input, null, single element)
- Boundary conditions (array indices, loop termination)
- Logic errors in algorithm implementation
- Test case coverage (basic, edge, corner cases)

**Common edge cases:**
- Empty arrays/strings: `[]`, `""`
- Null inputs: `null`, `None`
- Single element: `[1]`, `"a"`
- Duplicates: `[1,1,1]`
- Negative numbers: `[-1, -5]`
- Large inputs: Test time/space limits

### 2. Time & Space Complexity

**Analyze and verify:**
- Time complexity: Count operations relative to input size
- Space complexity: Count auxiliary space used
- Compare against optimal solution

**Provide:**
```
Current: O(n²) time, O(1) space
Optimal: O(n) time, O(n) space using HashMap
Trade-off: Use extra space for better time complexity
```

**Complexity Reference:**
- O(1): Direct access
- O(log n): Binary search, balanced tree
- O(n): Single pass, linear scan
- O(n log n): Efficient sorting, divide-and-conquer
- O(n²): Nested loops
- O(2ⁿ): Exponential (backtracking, brute force)

### 3. Code Quality - Java

**Java Best Practices:**
- Use appropriate data structures (`ArrayList`, `HashMap`, `HashSet`)
- Follow naming conventions (camelCase for methods/variables)
- Handle null checks and validation
- Use generics properly (`List<Integer>` not raw types)
- Prefer interfaces over implementations (`List<>` not `ArrayList<>`)

**Java Anti-patterns to flag:**
```java
// Bad: Raw types
ArrayList list = new ArrayList();

// Good: Generics
List<Integer> list = new ArrayList<>();

// Bad: Manual array copying
for (int i = 0; i < arr.length; i++) { ... }

// Good: Built-in methods
Arrays.copyOf(arr, arr.length);

// Bad: String concatenation in loop
String s = "";
for (String str : list) { s += str; }

// Good: StringBuilder
StringBuilder sb = new StringBuilder();
for (String str : list) { sb.append(str); }
```

**Check for:**
- Integer overflow: Suggest `long` when needed
- Proper exception handling
- Memory leaks (unclosed resources)
- Thread safety if applicable

### 4. Code Quality - Python

**Python Best Practices:**
- Use Pythonic idioms (list comprehensions, enumerate, zip)
- Follow PEP 8 style guidelines
- Use appropriate data structures (`set`, `dict`, `deque`)
- Leverage built-in functions

**Python Anti-patterns to flag:**
```python
# Bad: Manual index tracking
for i in range(len(arr)):
    print(i, arr[i])

# Good: enumerate
for i, val in enumerate(arr):
    print(i, val)

# Bad: Building list with append in loop
result = []
for x in arr:
    result.append(x * 2)

# Good: List comprehension
result = [x * 2 for x in arr]

# Bad: Multiple membership checks
if x == 'a' or x == 'b' or x == 'c':

# Good: Use set or tuple
if x in {'a', 'b', 'c'}:
```

**Check for:**
- Use of appropriate collections (`collections.defaultdict`, `Counter`)
- Generator expressions for memory efficiency
- Proper use of `None` checks
- Type hints for clarity (optional but helpful)

### 5. Algorithm Optimization

**Suggest improvements for:**
- Unnecessary nested loops → Use HashMap for O(n)
- Repeated calculations → Use memoization/DP
- Redundant sorting → Use heap or quick select
- Multiple passes → Combine into single pass
- Extra space usage → In-place modifications

**Pattern Recognition:**
- Two Sum pattern → Use HashMap
- Sliding Window → Two pointers
- Subarray sum → Prefix sum
- Longest substring → Sliding window + HashMap
- Tree traversal → DFS/BFS with proper data structure

### 6. Comparison: Java vs Python

**When comparing implementations:**

**Java strengths:**
- Explicit types catch errors early
- Better for performance-critical code
- Clear data structure usage

**Python strengths:**
- More concise and readable
- Rich standard library (collections, itertools)
- Better for rapid prototyping

**Flag inconsistencies:**
- Different algorithms used (should be same approach)
- Different time/space complexity
- Missing edge case handling in one version

### 7. Review Output Format

**Structure your review as:**

```markdown
## Correctness: ✓ Pass / ⚠ Issues Found

[List any correctness issues]

## Complexity Analysis

- Time: O(?) - [Explain]
- Space: O(?) - [Explain]
- Optimal: [If current solution is not optimal]

## Code Quality

**Strengths:**
- [List positive aspects]

**Issues:**
- [Issue 1] at line X: [Explanation]
- [Issue 2] at line Y: [Explanation]

**Suggestions:**
- [Suggestion 1]: [Why it's better]
- [Suggestion 2]: [Why it's better]

## Overall Assessment

[Summary and recommendation]
```

## Review Checklist

**Before completing review:**
- [ ] Tested with edge cases
- [ ] Verified time complexity
- [ ] Verified space complexity
- [ ] Checked for common bugs
- [ ] Compared to optimal solution
- [ ] Suggested concrete improvements
- [ ] Provided code examples for suggestions

## Example Reviews

### Example 1: Two Sum

```java
// Code under review
public int[] twoSum(int[] nums, int target) {
    for (int i = 0; i < nums.length; i++) {
        for (int j = i + 1; j < nums.length; j++) {
            if (nums[i] + nums[j] == target) {
                return new int[]{i, j};
            }
        }
    }
    return new int[]{};
}
```

**Review:**
- Correctness: ✓ Works correctly
- Time: O(n²) - Can be optimized to O(n)
- Suggestion: Use HashMap to store seen numbers and their indices

**Optimized:**
```java
public int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> map = new HashMap<>();
    for (int i = 0; i < nums.length; i++) {
        int complement = target - nums[i];
        if (map.containsKey(complement)) {
            return new int[]{map.get(complement), i};
        }
        map.put(nums[i], i);
    }
    return new int[]{};
}
```

## Project Context

- Review solutions in `leetcode_java/` and `leetcode_python/`
- Compare implementations across languages
- Check against patterns in `algorithm/` and `data_structure/`
- Reference complexity charts in `doc/` for analysis
