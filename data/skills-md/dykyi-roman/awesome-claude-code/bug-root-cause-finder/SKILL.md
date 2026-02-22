---
name: bug-root-cause-finder
description: Root cause analysis methods for PHP bugs. Provides 5 Whys technique, fault tree analysis, git bisect guidance, and stack trace parsing.
---

# Bug Root Cause Finder

Systematic methods for finding the true source of bugs, not just symptoms.

## Core Principle: Symptom ≠ Cause

The location where an error manifests is rarely where the bug originates.

```
Error Location:     OrderController::show() - NullPointerException
Symptom Location:   OrderRepository::find() - returns null
Root Cause:         OrderCreatedHandler - failed to persist order
True Root Cause:    RabbitMQ message lost due to missing ACK
```

## Method 1: 5 Whys Technique

Ask "why" repeatedly until you reach the root cause.

### Example Analysis

**Bug:** "Customer sees wrong order total"

1. **Why?** → The total displayed is $0
2. **Why?** → `Order::getTotal()` returns 0
3. **Why?** → `OrderItem` collection is empty
4. **Why?** → Items weren't loaded from database
5. **Why?** → Lazy loading failed due to closed EntityManager

**Root Cause:** EntityManager closed before accessing lazy-loaded collection

**Fix:** Eager load items in repository query, not lazy load

### 5 Whys Template

```markdown
## 5 Whys Analysis

**Bug Description:** [What user sees]

1. Why does [symptom] occur?
   → [First-level cause]

2. Why does [first-level cause] happen?
   → [Second-level cause]

3. Why does [second-level cause] happen?
   → [Third-level cause]

4. Why does [third-level cause] happen?
   → [Fourth-level cause]

5. Why does [fourth-level cause] happen?
   → [ROOT CAUSE]

**Fix Location:** [File:line where fix should be applied]
**Fix Type:** [Category: logic/null/boundary/race/resource/exception/type/sql/infinite]
```

## Method 2: Fault Tree Analysis

Build a tree of all possible causes for a failure.

### Fault Tree Structure

```
[FAILURE: Order total is $0]
        │
        ├── [OR] Order has no items
        │       ├── [AND] Items not added during creation
        │       │       ├── Cart was empty
        │       │       └── Cart-to-Order mapping failed
        │       │
        │       └── [AND] Items were deleted
        │               ├── Cascade delete triggered
        │               └── Manual deletion bug
        │
        └── [OR] Items exist but total calculation wrong
                ├── Price is 0
                │       ├── Product price not set
                │       └── Currency conversion failed
                │
                └── Quantity is 0
                        ├── Validation missing
                        └── Type coercion (string "0")
```

### Fault Tree Investigation Order

1. Start with most likely branches (based on code review)
2. Add logging/debugging to verify each branch
3. Eliminate branches systematically
4. Focus on remaining possibilities

## Method 3: Git Bisect

Find the exact commit that introduced a bug.

### Git Bisect Steps

```bash
# 1. Start bisect
git bisect start

# 2. Mark current (broken) as bad
git bisect bad

# 3. Mark known good commit (e.g., last release)
git bisect good v2.3.0

# 4. Git checks out middle commit - test it
# Run your reproduction test
php artisan test --filter=OrderTotalTest

# 5. Mark result
git bisect good  # if test passes
git bisect bad   # if test fails

# 6. Repeat until Git finds the culprit commit
# Git will output: "abc123 is the first bad commit"

# 7. Examine the commit
git show abc123

# 8. End bisect
git bisect reset
```

### Automated Git Bisect

```bash
# Run automatically with test script
git bisect start HEAD v2.3.0
git bisect run php artisan test --filter=OrderTotalTest
```

### Git Bisect Tips

- **Choose good boundaries:** Bad = current, Good = last known working
- **Use automated testing:** Faster and more reliable
- **Check for flaky tests:** Bisect fails with inconsistent tests
- **Look at the diff:** Focus on changed lines in culprit commit

## Method 4: Stack Trace Parsing

Extract actionable information from error traces.

### PHP Stack Trace Structure

```
Fatal error: Uncaught TypeError: OrderService::calculateTotal():
Argument #1 ($items) must be of type array, null given,
called in /app/src/Application/UseCase/CreateOrderUseCase.php on line 45

Stack trace:
#0 /app/src/Application/UseCase/CreateOrderUseCase.php(45): OrderService->calculateTotal(NULL)
#1 /app/src/Presentation/Api/OrderController.php(32): CreateOrderUseCase->execute(Object(CreateOrderCommand))
#2 /app/vendor/symfony/http-kernel/HttpKernel.php(163): OrderController->create(Object(Request))
#3 /app/vendor/symfony/http-kernel/HttpKernel.php(75): HttpKernel->handleRaw(Object(Request))
#4 /app/public/index.php(25): HttpKernel->handle(Object(Request))
#5 {main}

thrown in /app/src/Domain/Service/OrderService.php on line 23
```

### Key Information to Extract

| Element | Value | Meaning |
|---------|-------|---------|
| Error Type | TypeError | Type mismatch bug |
| Message | Argument #1 must be array, null given | Null pointer issue |
| Thrown Location | OrderService.php:23 | Where error detected |
| Call Location | CreateOrderUseCase.php:45 | Where bad value passed |
| Root Investigation | CreateOrderUseCase.php:45 | Start here |

### Stack Trace Analysis Steps

1. **Read error message** - What type of error?
2. **Find thrown location** - Where was error detected?
3. **Find call location** - Where was bad value passed?
4. **Trace backward** - How did bad value get there?
5. **Find origin** - Where was value first set to bad state?

### Common Stack Trace Patterns

**Pattern: Null from Repository**
```
#0 Repository->find() returns null
#1 Service uses result without check
#2 Controller calls service
```
→ Fix in #1: Add null check

**Pattern: Type Coercion**
```
#0 Method expects int, gets string
#1 Request data not validated
#2 Controller passes raw input
```
→ Fix in #1 or #2: Add validation/casting

**Pattern: Missing Dependency**
```
#0 Service->method() called
#1 Container->get() fails
#2 Dependency not registered
```
→ Fix: Register dependency in container

## Method 5: Dependency Graph Analysis

Trace data flow through the application.

### Data Flow Tracing

```php
// Trace the flow of $orderId
1. Controller receives $orderId from Request
2. UseCase receives $orderId as Command property
3. Repository uses $orderId in SQL query
4. Database returns null (ID doesn't exist)
5. UseCase passes null to Service
6. Service throws NullPointerException
```

### Dependency Questions

- Where does the value originate?
- What transformations does it undergo?
- Where is it validated?
- Where could it become invalid?
- Who else uses this value?

### Call Graph Investigation

```bash
# Find all callers of a method
grep -r "->calculateTotal(" src/

# Find all places where variable is set
grep -r "\$items\s*=" src/

# Find all null assignments
grep -r "= null" src/Domain/
```

## Method 6: State Timeline Reconstruction

Rebuild the sequence of state changes.

### Timeline Template

```markdown
## State Timeline

T0: Initial state
    - Order::status = DRAFT
    - Order::items = []

T1: AddItemToOrder executed
    - Order::items = [Item(id=1)]
    - Expected: status stays DRAFT ✓

T2: SubmitOrder executed
    - Order::status = SUBMITTED
    - Expected: items preserved ✓

T3: PaymentReceived event
    - Order::status = PAID
    - BUG: items cleared unexpectedly ✗

T4: GetOrder query
    - Returns Order with empty items
    - User sees $0 total

Root Cause: PaymentReceived handler incorrectly reinitializes Order
```

## Investigation Checklist

### Before Starting
- [ ] Reproduce bug consistently
- [ ] Identify exact error message
- [ ] Note conditions when bug occurs
- [ ] Check if bug is environment-specific

### During Investigation
- [ ] Parse stack trace for key locations
- [ ] Apply 5 Whys technique
- [ ] Build fault tree if multiple possible causes
- [ ] Use git bisect if recent regression
- [ ] Trace data flow from origin to error

### After Finding Root Cause
- [ ] Verify fix addresses root cause, not symptom
- [ ] Check for similar bugs in related code
- [ ] Document root cause for team knowledge
- [ ] Consider if design change prevents recurrence

## Quick Reference: Where to Look First

| Bug Type | First Investigation Point |
|----------|--------------------------|
| Null pointer | Repository/Factory that creates the null |
| Wrong calculation | Input values, not calculation logic |
| Missing data | Event handler or background job |
| Intermittent failure | Shared state or race condition |
| After deployment | Git diff between versions |
| Only in production | Environment config or data |
| Only for some users | User-specific data or permissions |
