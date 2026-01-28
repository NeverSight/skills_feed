---
name: java-developer
description: Expert Java developer for implementing LeetCode problems, data structures, and algorithms. Helps write clean, efficient Java code following best practices for competitive programming and interview preparation. Use when writing or implementing Java solutions.
allowed-tools: Read, Glob, Grep, Edit, Write, Bash
---

# Java Developer

## When to use this Skill

Use this Skill when:
- Writing new Java solutions for LeetCode problems
- Implementing data structures or algorithms in Java
- Converting solutions from other languages to Java
- Setting up Java test cases with JUnit

## Instructions

### 1. Code Structure

**Follow the project's Java conventions:**
- Package structure: `AlgorithmJava`, `DataStructure`, `LeetCodeJava`
- Use Java 8 compatibility features
- Include proper imports and class declarations
- Follow camelCase naming conventions

**For LeetCode problems:**
```java
package LeetCodeJava;

/**
 * Problem {number}: {title}
 * Difficulty: {Easy/Medium/Hard}
 *
 * {Brief problem description}
 *
 * Time Complexity: O(?)
 * Space Complexity: O(?)
 */
public class Problem{Number}{Title} {
    public ReturnType methodName(InputType param) {
        // Implementation
    }
}
```

### 2. Best Practices

**Optimize for interviews:**
- Write clean, readable code first
- Add comments only for complex logic
- Use meaningful variable names
- Handle edge cases explicitly

**Common patterns:**
- Two pointers: `left`, `right` or `i`, `j`
- Sliding window: `start`, `end`
- Binary search: `lo`, `hi`, `mid`
- DFS/BFS: Use Stack/Queue with explicit types

**Data structures to prefer:**
- `List<>` instead of arrays when size varies
- `HashMap<>` for O(1) lookups
- `HashSet<>` for uniqueness checks
- `PriorityQueue<>` for heap operations
- `Deque<>` for stack/queue flexibility

### 3. Performance Guidelines

**Time Complexity Goals:**
- Array problems: Aim for O(n) or O(n log n)
- String problems: Aim for O(n) with HashMap/array counting
- Tree problems: O(n) traversal is usually optimal
- Graph problems: O(V + E) for BFS/DFS

**Space Optimization:**
- Modify input in-place when possible
- Use bit manipulation for boolean arrays
- Consider iterative over recursive for O(1) space

### 4. Testing Approach

**Include test cases:**
```java
// In test class
@Test
public void testBasicCase() {
    Problem{Number}{Title} solution = new Problem{Number}{Title}();
    assertEquals(expected, solution.methodName(input));
}

@Test
public void testEdgeCase() {
    // Test empty input, null, single element, etc.
}
```

### 5. Common Mistakes to Avoid

- Integer overflow: Use `long` for large sums
- Array index out of bounds: Check `i < arr.length`
- Null pointer: Validate inputs
- Off-by-one errors: Double-check loop boundaries
- Mutable vs immutable: Be careful with references

### 6. Java-Specific Tips

**Useful methods:**
```java
// String
s.charAt(i), s.substring(i, j), s.toCharArray()

// Collections
Collections.sort(list), Collections.reverse(list)
Arrays.sort(arr), Arrays.fill(arr, val)

// Math
Math.max(a, b), Math.min(a, b), Math.abs(x)

// Queue/Stack
queue.offer(), queue.poll(), queue.peek()
stack.push(), stack.pop(), stack.peek()
```

**Lambda expressions for sorting:**
```java
Arrays.sort(intervals, (a, b) -> a[0] - b[0]);
PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[0] - b[0]);
```

## Example Workflow

1. **Read the problem** from leetcode_java/ or create new file
2. **Identify the pattern** (two pointers, sliding window, DP, etc.)
3. **Write the solution** with clear variable names
4. **Add complexity analysis** in comments
5. **Test with examples** including edge cases
6. **Optimize if needed** after correct solution works

## Project-Specific Notes

- Maven project: Build with `mvn compile`, test with `mvn test`
- JUnit 5 is configured for testing
- Problems are organized by algorithm type
- Follow existing code style in the package
