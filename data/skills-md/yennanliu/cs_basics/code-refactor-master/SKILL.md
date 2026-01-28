---
name: code-refactor-master
description: Code refactoring expert for improving code quality, readability, maintainability, and performance. Specializes in Java and Python refactoring patterns, eliminating code smells, and applying clean code principles. Use when refactoring code, improving existing implementations, or cleaning up technical debt.
allowed-tools: Read, Glob, Grep, Edit, LSP
---

# Code Refactor Master

## When to use this Skill

Use this Skill when:
- Refactoring existing code for better quality
- Eliminating code smells
- Improving code readability and maintainability
- Optimizing performance without changing behavior
- Applying design patterns
- Reducing complexity
- Cleaning up technical debt

## Refactoring Principles

### 1. Core Rules

**Golden Rule**: Make code changes that improve internal structure without altering external behavior

**Key Principles:**
- One refactoring at a time
- Run tests after each refactoring
- Commit frequently with clear messages
- Keep refactoring separate from feature work
- Maintain backwards compatibility unless explicitly changing API

**Red Flags to Refactor:**
- Code duplication (DRY principle)
- Long methods (>20-30 lines)
- Large classes (>300-500 lines)
- Long parameter lists (>3-4 parameters)
- Deeply nested conditionals (>3 levels)
- Comments explaining what code does (code should be self-explanatory)

### 2. Common Code Smells

**Bloaters:**
- Long Method
- Large Class
- Primitive Obsession
- Long Parameter List
- Data Clumps

**Object-Orientation Abusers:**
- Switch Statements (consider polymorphism)
- Temporary Field
- Refused Bequest
- Alternative Classes with Different Interfaces

**Change Preventers:**
- Divergent Change (one class changes for many reasons)
- Shotgun Surgery (one change requires many small changes)
- Parallel Inheritance Hierarchies

**Dispensables:**
- Comments (where code should be self-explanatory)
- Duplicate Code
- Lazy Class
- Dead Code
- Speculative Generality

**Couplers:**
- Feature Envy
- Inappropriate Intimacy
- Message Chains
- Middle Man

### 3. Refactoring Catalog

**Method-Level Refactorings:**

**Extract Method**
```java
// Before
void printOwing() {
    printBanner();
    // print details
    System.out.println("name: " + name);
    System.out.println("amount: " + getOutstanding());
}

// After
void printOwing() {
    printBanner();
    printDetails(getOutstanding());
}

void printDetails(double outstanding) {
    System.out.println("name: " + name);
    System.out.println("amount: " + outstanding);
}
```

**Inline Method**
```java
// Before - method too simple
int getRating() {
    return moreThanFiveLateDeliveries() ? 2 : 1;
}

boolean moreThanFiveLateDeliveries() {
    return numberOfLateDeliveries > 5;
}

// After
int getRating() {
    return numberOfLateDeliveries > 5 ? 2 : 1;
}
```

**Replace Temp with Query**
```java
// Before
double calculateTotal() {
    double basePrice = quantity * itemPrice;
    if (basePrice > 1000) {
        return basePrice * 0.95;
    }
    return basePrice * 0.98;
}

// After
double calculateTotal() {
    if (basePrice() > 1000) {
        return basePrice() * 0.95;
    }
    return basePrice() * 0.98;
}

double basePrice() {
    return quantity * itemPrice;
}
```

**Variable-Level Refactorings:**

**Rename Variable**
```python
# Before
d = 10  # elapsed time in days

# After
elapsed_time_in_days = 10
```

**Split Temporary Variable**
```java
// Before
double temp = 2 * (height + width);
System.out.println(temp);
temp = height * width;
System.out.println(temp);

// After
double perimeter = 2 * (height + width);
System.out.println(perimeter);
double area = height * width;
System.out.println(area);
```

**Class-Level Refactorings:**

**Extract Class**
```java
// Before
class Person {
    String name;
    String officeAreaCode;
    String officeNumber;

    String getTelephoneNumber() {
        return "(" + officeAreaCode + ") " + officeNumber;
    }
}

// After
class Person {
    String name;
    TelephoneNumber officeTelephone = new TelephoneNumber();

    String getTelephoneNumber() {
        return officeTelephone.getTelephoneNumber();
    }
}

class TelephoneNumber {
    String areaCode;
    String number;

    String getTelephoneNumber() {
        return "(" + areaCode + ") " + number;
    }
}
```

**Replace Conditional with Polymorphism**
```python
# Before
class Bird:
    def get_speed(self):
        if self.type == "EUROPEAN":
            return self.get_base_speed()
        elif self.type == "AFRICAN":
            return self.get_base_speed() - self.get_load_factor()
        elif self.type == "NORWEGIAN_BLUE":
            return 0 if self.is_nailed else self.get_base_speed()

# After
class Bird:
    def get_speed(self):
        pass  # Abstract

class European(Bird):
    def get_speed(self):
        return self.get_base_speed()

class African(Bird):
    def get_speed(self):
        return self.get_base_speed() - self.get_load_factor()

class NorwegianBlue(Bird):
    def get_speed(self):
        return 0 if self.is_nailed else self.get_base_speed()
```

### 4. Java-Specific Refactorings

**Use Modern Java Features:**

**Replace Anonymous Class with Lambda**
```java
// Before
list.sort(new Comparator<String>() {
    @Override
    public int compare(String a, String b) {
        return a.compareTo(b);
    }
});

// After
list.sort((a, b) -> a.compareTo(b));
// Or even better
list.sort(String::compareTo);
```

**Use Streams API**
```java
// Before
List<String> result = new ArrayList<>();
for (String s : list) {
    if (s.length() > 3) {
        result.add(s.toUpperCase());
    }
}

// After
List<String> result = list.stream()
    .filter(s -> s.length() > 3)
    .map(String::toUpperCase)
    .collect(Collectors.toList());
```

**Replace String Concatenation**
```java
// Before - inefficient in loops
String result = "";
for (String s : list) {
    result += s + ", ";
}

// After
StringBuilder result = new StringBuilder();
for (String s : list) {
    result.append(s).append(", ");
}
// Or better
String result = String.join(", ", list);
```

**Use Optional**
```java
// Before
public User findUser(int id) {
    User user = database.getUser(id);
    return user != null ? user : new User();
}

// After
public Optional<User> findUser(int id) {
    return Optional.ofNullable(database.getUser(id));
}
```

**Replace Type Code with Enum**
```java
// Before
public static final int TYPE_A = 1;
public static final int TYPE_B = 2;

// After
public enum Type {
    A, B
}
```

### 5. Python-Specific Refactorings

**Use List Comprehensions**
```python
# Before
result = []
for item in items:
    if item > 0:
        result.append(item * 2)

# After
result = [item * 2 for item in items if item > 0]
```

**Use Collections Module**
```python
# Before
counts = {}
for item in items:
    if item in counts:
        counts[item] += 1
    else:
        counts[item] = 1

# After
from collections import Counter
counts = Counter(items)
```

**Use Context Managers**
```python
# Before
file = open('file.txt')
data = file.read()
file.close()

# After
with open('file.txt') as file:
    data = file.read()
```

**Use f-strings**
```python
# Before
message = "Hello, %s! You are %d years old." % (name, age)

# After
message = f"Hello, {name}! You are {age} years old."
```

**Use Type Hints**
```python
# Before
def process(data):
    return [x * 2 for x in data]

# After
def process(data: list[int]) -> list[int]:
    return [x * 2 for x in data]
```

**Use Dataclasses**
```python
# Before
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"

# After
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int
```

### 6. Clean Code Principles

**Naming:**
```java
// Bad
int d; // elapsed time in days

// Good
int elapsedTimeInDays;

// Bad
public List<int[]> getThem() {
    List<int[]> list1 = new ArrayList<>();
    for (int[] x : theList) {
        if (x[0] == 4) {
            list1.add(x);
        }
    }
    return list1;
}

// Good
public List<Cell> getFlaggedCells() {
    List<Cell> flaggedCells = new ArrayList<>();
    for (Cell cell : gameBoard) {
        if (cell.isFlagged()) {
            flaggedCells.add(cell);
        }
    }
    return flaggedCells;
}
```

**Functions:**
- Small (20-30 lines max)
- Do one thing
- One level of abstraction
- Descriptive names
- Few arguments (0-3 ideal)

**Comments:**
```java
// Bad - comment explains what code does
// Check to see if employee is eligible for full benefits
if ((employee.flags & HOURLY_FLAG) && (employee.age > 65))

// Good - code is self-explanatory
if (employee.isEligibleForFullBenefits())
```

### 7. Performance Refactorings

**Algorithm Optimization:**
```python
# Before - O(n²)
def has_duplicates(arr):
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] == arr[j]:
                return True
    return False

# After - O(n)
def has_duplicates(arr):
    return len(arr) != len(set(arr))
```

**Lazy Evaluation:**
```java
// Before - computes all values
List<Integer> results = list.stream()
    .map(this::expensiveOperation)
    .collect(Collectors.toList());
return results.get(0);

// After - computes only what's needed
return list.stream()
    .map(this::expensiveOperation)
    .findFirst()
    .orElse(null);
```

**Memoization:**
```python
# Before
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# After
from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

### 8. Refactoring Workflow

**Step-by-step process:**

1. **Identify**: Find code smell or improvement opportunity
2. **Plan**: Decide which refactoring to apply
3. **Test**: Ensure tests exist and pass
4. **Refactor**: Make one small change
5. **Test**: Run tests again
6. **Commit**: Save working state
7. **Repeat**: Continue with next refactoring

**Example workflow:**
```bash
# 1. Create feature branch
git checkout -b refactor/improve-user-service

# 2. Identify issue (e.g., long method)
# Read code, find UserService.processUser() is 150 lines

# 3. Run existing tests
mvn test  # or pytest

# 4. Extract method
# Break processUser into smaller methods

# 5. Run tests
mvn test  # Ensure still passing

# 6. Commit
git commit -m "refactor: extract validateUser method"

# 7. Continue
# Extract next method, repeat
```

### 9. Refactoring Checklist

**Before refactoring:**
- [ ] Tests exist and pass
- [ ] Understand the code behavior
- [ ] Have a clear goal
- [ ] Know which refactoring to apply

**During refactoring:**
- [ ] Make small, incremental changes
- [ ] Run tests after each change
- [ ] Keep code working at all times
- [ ] Commit frequently

**After refactoring:**
- [ ] All tests pass
- [ ] Code is more readable
- [ ] Complexity reduced
- [ ] No behavioral changes
- [ ] Documentation updated if needed

### 10. LeetCode-Specific Refactoring

**Optimize brute force:**
```java
// Before - Brute force O(n²)
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

// After - Hash map O(n)
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

**Extract helper methods:**
```python
# Before - monolithic
def solve(self, grid):
    # 50 lines of code mixing concerns

# After - modular
def solve(self, grid):
    if not self.is_valid(grid):
        return []

    processed = self.preprocess(grid)
    result = self.compute(processed)
    return self.format_output(result)

def is_valid(self, grid):
    # validation logic

def preprocess(self, grid):
    # preprocessing logic

def compute(self, data):
    # core algorithm

def format_output(self, result):
    # formatting logic
```

## Refactoring Anti-Patterns

**Don't:**
- Refactor without tests
- Change behavior during refactoring
- Make multiple changes at once
- Refactor and add features simultaneously
- Over-engineer simple code
- Prematurely optimize

## Project Context

**For CS_basics repository:**
- Refactor solutions in `leetcode_java/` and `leetcode_python/`
- Maintain consistency across language implementations
- Keep algorithm explanations updated
- Follow project conventions
- Test refactored code with example inputs
- Document complexity improvements

## Tools and Resources

**IDE Refactoring Tools:**
- IntelliJ IDEA: Refactor menu (Ctrl+Alt+Shift+T)
- VS Code: Python refactoring extensions
- PyCharm: Refactoring actions

**Use automated refactoring when available:**
- Rename: Safe renaming across project
- Extract method/variable: Automatic extraction
- Inline: Safe inlining with preview
- Move: Restructure packages/modules
