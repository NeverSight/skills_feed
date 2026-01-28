---
name: refactoring
description: |
  Restructures existing code to improve readability, maintainability, and performance without changing external behavior.

  USE WHEN: Restructuring code without changing behavior, extracting methods/classes, removing duplication, applying design patterns, improving code organization, reducing technical debt.
  DO NOT USE: For bug fixes (use /debugging), for adding tests (use /testing), for new features (implement directly).

  TRIGGERS: refactor, restructure, rewrite, clean up, simplify, extract, inline, rename, move, split, merge, decompose, modularize, decouple, technical debt, code smell, DRY, SOLID, improve code, modernize, reorganize.
triggers:
  - refactor
  - restructure
  - rewrite
  - clean up
  - simplify
  - extract
  - inline
  - rename
  - move
  - split
  - merge
  - decompose
  - modularize
  - decouple
  - technical debt
  - code smell
  - DRY
  - SOLID
  - improve code
  - modernize
  - reorganize
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Refactoring

## Overview

This skill focuses on improving code quality through systematic refactoring techniques. It identifies code smells and applies proven refactoring patterns to enhance maintainability while preserving functionality.

Use this skill when the user requests:

- Code restructuring or cleanup
- Reducing technical debt
- Improving code organization
- Applying design patterns
- Breaking up large files or functions
- Removing duplication
- Modernizing legacy code
- Improving testability

## Scope Selection

**When to use this skill:**

- Local refactoring (single module/file)
- Pattern application (extract method, introduce interface)
- Test refactoring and test suite improvements
- Data pipeline restructuring
- Safe refactoring with test coverage

**When to escalate to senior-software-engineer:**

- Architectural changes affecting multiple modules
- API redesign requiring migration paths
- Cross-cutting refactoring with unclear scope
- Performance optimization requiring profiling
- Infrastructure refactoring (delegate to senior-infrastructure-engineer)
- Security-sensitive refactoring (delegate to security-engineer)

## Instructions

### 1. Identify Refactoring Opportunities

**Code Smells to Search For:**

- Long methods (>50 lines) or large classes (>300 lines)
- Duplicated code blocks
- High cyclomatic complexity
- Magic numbers and string literals
- Deep nesting (>3 levels)
- Feature envy (method using data from another class)
- Shotgun surgery (one change requires many edits)
- Data clumps (same group of parameters)
- Primitive obsession (using primitives instead of objects)

**Use Grep/Glob to find patterns:**

```bash
# Find long functions (rough heuristic)
rg "^(\s*)(def|function|fn|func)\s+\w+" --after-context=60

# Find duplicated code
rg --multiline "pattern.*\n.*pattern"

# Find magic numbers
rg "\b\d{2,}\b" --type=py --type=js --type=rs
```

### 2. Plan the Refactoring

**Before starting:**

1. **Verify test coverage** - Run tests to establish baseline
2. **List all changes** - Document sequence of refactorings
3. **Identify dependencies** - What code depends on what you're changing?
4. **Plan rollback points** - Where can you safely commit?
5. **Check for impact** - Grep for references to functions/classes being changed

**Red flags that require escalation:**

- No test coverage exists
- Changes affect public APIs with external consumers
- Unclear ownership or multiple teams involved
- Performance-critical hot paths

### 3. Apply Refactoring Patterns

#### Code Organization Patterns

**Extract Method/Function:**

- Break down long functions into smaller, focused ones
- Each function should do one thing
- Improves readability and testability

**Extract Class:**

- Split large classes with multiple responsibilities
- Follow Single Responsibility Principle
- Improves cohesion and reduces coupling

**Move Method/Field:**

- Relocate methods to classes that use their data
- Reduces feature envy
- Improves encapsulation

**Inline Method/Variable:**

- Remove unnecessary indirection
- Simplify overly abstracted code
- Use when abstraction doesn't add value

**Rename:**

- Improve naming clarity
- Use domain language
- Make intent explicit

#### Structural Patterns

**Replace Conditional with Polymorphism:**

- Replace type switches with subclass methods
- Enables Open/Closed Principle
- Improves extensibility

**Introduce Parameter Object:**

- Group related parameters into objects
- Reduces parameter lists
- Makes data relationships explicit

**Replace Magic Numbers with Constants:**

- Define named constants for literals
- Improves readability and maintainability
- Centralizes configuration

**Decompose Conditional:**

- Extract complex conditions into named functions
- Replace nested ifs with guard clauses
- Improves readability

#### Test Refactoring Patterns

**Extract Test Fixture:**

- Move common setup into fixture/factory
- Reduces duplication in test files
- Improves test maintainability

**Introduce Test Data Builder:**

- Replace complex object construction with builders
- Makes test intent clearer
- Simplifies test setup

**Replace Assertion Roulette:**

- Use descriptive assertion messages
- One logical assertion per test
- Clear failure messages

**Extract Test Helper:**

- Move repeated test logic into helpers
- Keep tests focused on behavior
- Improves test readability

#### Data Pipeline Patterns

**Extract Transformation:**

- Isolate data transformation logic
- Make transformations composable
- Improves testability

**Introduce Pipeline Interface:**

- Define standard input/output contracts
- Enable stage composition
- Simplifies testing and debugging

**Replace Inline Processing with Stages:**

- Break monolithic processing into stages
- Each stage has single responsibility
- Enables parallelization and monitoring

### 4. Safe Refactoring Workflow

**For each refactoring step:**

1. **Make the change** - One refactoring at a time
2. **Run tests** - Verify behavior preserved
3. **Commit** - Create checkpoint with clear message
4. **Repeat** - Move to next refactoring

**If tests fail:**

- Revert immediately (git checkout)
- Analyze failure - is it a test issue or behavior change?
- Fix or adjust approach

**Commit message format:**

```text
refactor: extract calculate_discount from process_order

Improves testability by isolating discount logic.
No behavior change.
```

### 5. Verify Changes

**Verification checklist:**

- All tests pass (existing + any new tests)
- No regressions in functionality
- Performance hasn't degraded (for hot paths)
- Code coverage maintained or improved
- Linting passes
- Build succeeds

**For large refactorings:**

- Run additional smoke tests
- Check memory usage (if applicable)
- Review error handling preservation

## Best Practices

1. **Small Steps**: Make incremental changes, not big bang rewrites
2. **Test First**: Ensure tests exist before refactoring - write them if missing
3. **One Thing at a Time**: Focus on single refactoring per commit
4. **Preserve Behavior**: External behavior must remain unchanged
5. **Keep It Working**: Code should pass tests after each step
6. **Document Intent**: Explain why refactoring was needed in commits
7. **Refactor Tests Too**: Keep tests clean and maintainable
8. **Use Type Safety**: Leverage type systems to catch errors early
9. **Measure Don't Guess**: Profile before optimizing performance
10. **Know When to Stop**: Don't over-engineer or add unnecessary abstraction

## Common Patterns with Examples

### Pattern 1: Extract Method

```python
# Before: Long method with multiple responsibilities
def process_order(order):
    # Validate order
    if not order.items:
        raise ValueError("Empty order")
    if order.total < 0:
        raise ValueError("Invalid total")

    # Calculate discount
    discount = 0
    if order.customer.is_premium:
        discount = order.total * 0.1
    if order.total > 1000:
        discount += order.total * 0.05

    # Apply discount and save
    order.final_total = order.total - discount
    order.save()

# After: Extracted methods with single responsibility
def process_order(order):
    validate_order(order)
    discount = calculate_discount(order)
    finalize_order(order, discount)

def validate_order(order):
    if not order.items:
        raise ValueError("Empty order")
    if order.total < 0:
        raise ValueError("Invalid total")

def calculate_discount(order) -> float:
    discount = 0
    if order.customer.is_premium:
        discount = order.total * 0.1
    if order.total > 1000:
        discount += order.total * 0.05
    return discount

def finalize_order(order, discount: float):
    order.final_total = order.total - discount
    order.save()
```

### Pattern 2: Replace Magic Numbers with Constants

```javascript
// Before
if (response.status === 200) {
  setTimeout(retry, 3000);
  if (attempts > 5) {
    throw new Error("Max retries exceeded");
  }
}

// After
const HTTP_OK = 200;
const RETRY_DELAY_MS = 3000;
const MAX_RETRY_ATTEMPTS = 5;

if (response.status === HTTP_OK) {
  setTimeout(retry, RETRY_DELAY_MS);
  if (attempts > MAX_RETRY_ATTEMPTS) {
    throw new Error("Max retries exceeded");
  }
}
```

### Pattern 3: Replace Nested Conditionals with Guard Clauses

```python
# Before
def get_payment_amount(employee):
    if employee.is_active:
        if employee.is_full_time:
            if employee.tenure > 5:
                return employee.salary * 1.1
            else:
                return employee.salary
        else:
            return employee.hourly_rate * employee.hours
    else:
        return 0

# After
def get_payment_amount(employee):
    if not employee.is_active:
        return 0

    if not employee.is_full_time:
        return employee.hourly_rate * employee.hours

    if employee.tenure > 5:
        return employee.salary * 1.1

    return employee.salary
```

### Pattern 4: Introduce Parameter Object

```typescript
// Before
function createUser(
  firstName: string,
  lastName: string,
  email: string,
  phone: string,
  street: string,
  city: string,
  state: string,
  zip: string
) {
  // ...
}

// After
interface UserDetails {
  name: PersonName;
  contact: ContactInfo;
  address: Address;
}

interface PersonName {
  first: string;
  last: string;
}

interface ContactInfo {
  email: string;
  phone: string;
}

interface Address {
  street: string;
  city: string;
  state: string;
  zip: string;
}

function createUser(details: UserDetails) {
  // ...
}
```

### Pattern 5: Replace Type Code with Polymorphism

```rust
// Before
enum ShapeType { Circle, Rectangle, Triangle }

struct Shape {
    shape_type: ShapeType,
    radius: f64,
    width: f64,
    height: f64,
    base: f64,
}

impl Shape {
    fn area(&self) -> f64 {
        match self.shape_type {
            ShapeType::Circle => 3.14159 * self.radius * self.radius,
            ShapeType::Rectangle => self.width * self.height,
            ShapeType::Triangle => 0.5 * self.base * self.height,
        }
    }
}

// After
trait Shape {
    fn area(&self) -> f64;
}

struct Circle { radius: f64 }
struct Rectangle { width: f64, height: f64 }
struct Triangle { base: f64, height: f64 }

impl Shape for Circle {
    fn area(&self) -> f64 {
        3.14159 * self.radius * self.radius
    }
}

impl Shape for Rectangle {
    fn area(&self) -> f64 {
        self.width * self.height
    }
}

impl Shape for Triangle {
    fn area(&self) -> f64 {
        0.5 * self.base * self.height
    }
}
```

### Pattern 6: Extract Data Pipeline Stage

```python
# Before: Monolithic processing
def process_data(raw_data):
    # Validate
    if not raw_data:
        raise ValueError("Empty data")

    # Clean
    cleaned = []
    for item in raw_data:
        if item.get('status') == 'valid':
            cleaned.append(item)

    # Transform
    transformed = []
    for item in cleaned:
        transformed.append({
            'id': item['id'],
            'value': item['raw_value'] * 100,
            'timestamp': item['ts']
        })

    # Aggregate
    total = sum(item['value'] for item in transformed)
    return {'items': transformed, 'total': total}

# After: Pipeline with composable stages
def validate_input(raw_data):
    if not raw_data:
        raise ValueError("Empty data")
    return raw_data

def filter_valid(data):
    return [item for item in data if item.get('status') == 'valid']

def transform_items(data):
    return [
        {
            'id': item['id'],
            'value': item['raw_value'] * 100,
            'timestamp': item['ts']
        }
        for item in data
    ]

def aggregate_results(transformed):
    total = sum(item['value'] for item in transformed)
    return {'items': transformed, 'total': total}

def process_data(raw_data):
    return (raw_data
            |> validate_input
            |> filter_valid
            |> transform_items
            |> aggregate_results)
```

### Pattern 7: Simplify Test with Builder

```go
// Before
func TestUserRegistration(t *testing.T) {
    user := &User{
        FirstName: "John",
        LastName: "Doe",
        Email: "john@example.com",
        Phone: "555-0100",
        Address: Address{
            Street: "123 Main St",
            City: "Springfield",
            State: "IL",
            Zip: "62701",
        },
        Preferences: Preferences{
            NewsletterEnabled: true,
            Theme: "dark",
        },
        CreatedAt: time.Now(),
    }

    err := RegisterUser(user)
    assert.NoError(t, err)
}

// After
func TestUserRegistration(t *testing.T) {
    user := NewUserBuilder().
        WithName("John", "Doe").
        WithEmail("john@example.com").
        Build()

    err := RegisterUser(user)
    assert.NoError(t, err)
}

// Test builder focuses on what matters for each test
func TestUserWithNewsletter(t *testing.T) {
    user := NewUserBuilder().WithNewsletter(true).Build()
    // ...
}
```

## When to Stop Refactoring

**Stop if:**

- Tests start failing unexpectedly
- Scope is expanding beyond initial plan
- Unsure about architectural implications
- Performance concerns arise
- Security implications unclear

**In these cases:**

- Commit current progress
- Document remaining work
- Escalate to senior-software-engineer or relevant specialist
