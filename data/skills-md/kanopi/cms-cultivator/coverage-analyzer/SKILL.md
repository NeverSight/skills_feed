---
name: coverage-analyzer
description: Automatically analyze test coverage when user asks which code is tested, mentions coverage gaps, or shows code asking about testing. Identifies untested code paths and suggests test additions. Invoke when user asks "what's not tested?", "coverage", "untested code", or "which tests are missing?".
---

# Coverage Analyzer

Automatically analyze test coverage and identify untested code.

## Philosophy

Knowing what's tested gives confidence to refactor and prevents regressions.

### Core Beliefs

1. **Visibility Drives Action**: Can't improve what you can't measure
2. **Not All Code Needs 100% Coverage**: Prioritize critical paths over getters/setters
3. **Coverage ≠ Quality**: 100% coverage doesn't guarantee bug-free code
4. **Gap Analysis Guides Testing**: Knowing what's untested helps prioritize test writing

### Why Coverage Analysis Matters

- **Identify Risks**: Find critical code without test protection
- **Prioritize Effort**: Focus testing where it matters most
- **Prevent Regressions**: Tests catch bugs before they reach users
- **Enable Refactoring**: Good coverage allows confident code changes

## When to Use This Skill

Activate this skill when the user:
- Asks "what code isn't tested?"
- Mentions "test coverage" or "coverage report"
- Says "which tests are missing?"
- Shows code and asks "is this tested?"
- References "untested code paths"
- Asks "what's my coverage percentage?"

## Decision Framework

Before analyzing coverage, consider:

### What's the Goal?

1. **Find coverage gaps** → Identify untested code
2. **Measure current coverage** → Run coverage tools and report percentages
3. **Prioritize testing** → Focus on critical paths first
4. **Improve coverage** → Recommend specific tests to write

### What's the Scope?

- **Specific file** - User shows code → Analyze that file's coverage
- **Component/module** - User mentions feature → Check component tests
- **Recent changes** - User says "my code" → Check coverage of git diff
- **Entire project** - User says "overall coverage" → Run project-wide analysis

### What Test Types Exist?

**Check for**:
- PHPUnit tests (PHP) → Run `phpunit --coverage-text`
- Jest tests (JavaScript) → Run `jest --coverage`
- Cypress tests (E2E) → Integration coverage only
- Manual test documentation → Note gaps

### What Coverage Metrics Matter?

**Primary metrics**:
- **Line coverage** - Percentage of lines executed
- **Branch coverage** - Percentage of decision branches taken
- **Function coverage** - Percentage of functions called

**Priority order**:
1. Critical paths (auth, payments, data writes)
2. Public APIs
3. Security-sensitive code
4. Business logic
5. Getters/setters (lowest priority)

### What's a Good Target?

- **Critical code** - Aim for 90%+ coverage
- **Business logic** - Aim for 80%+ coverage
- **Overall project** - Aim for 70%+ coverage
- **Getters/setters** - Can skip, focus on behavior

### Decision Tree

```
User asks about coverage
    ↓
Determine scope (file/component/project)
    ↓
Check for existing test files
    ↓
Run coverage tool (PHPUnit/Jest/Cypress)
    ↓
Analyze gaps (prioritize critical paths)
    ↓
Report coverage with recommendations
    ↓
Suggest specific tests for gaps
```

## Quick Coverage Analysis

### 1. Check if Tests Exist

**PHP (PHPUnit):**
```bash
# Check for test files
find tests/ -name "*Test.php"

# Check specific class
test -f "tests/src/Unit/DataProcessorTest.php" && echo "Tests exist"
```

**JavaScript (Jest):**
```bash
# Check for test files
find . -name "*.test.js" -o -name "*.spec.js"
```

### 2. Run Coverage Analysis

**PHP:**
```bash
# Generate coverage report
vendor/bin/phpunit --coverage-text

# For Kanopi projects
ddev exec vendor/bin/phpunit --coverage-text
```

**JavaScript:**
```bash
# Jest coverage
npm run test -- --coverage

# Or directly
npx jest --coverage
```

### 3. Identify Gaps

**Common untested areas:**
- Error handling (catch blocks)
- Edge cases (empty input, null values)
- Private methods (test via public interface)
- Complex conditionals
- New features without tests

## Response Format

```markdown
## Test Coverage Analysis

### Summary
- **Overall Coverage**: 72%
- **Files Analyzed**: 45
- **Tested**: 32 files
- **Untested**: 13 files

### Coverage by Type
- Classes: 85% (34/40)
- Methods: 68% (156/230)
- Lines: 72% (2,340/3,250)
- Branches: 58% (89/153)

### 🔴 Critical Gaps (No Tests)

**1. PaymentProcessor.php** - 0% coverage
- **Risk**: High - handles money
- **Methods untested**: processPayment(), refund(), validate()
- **Recommendation**: Add unit tests immediately

**2. AuthenticationService.php** - 0% coverage
- **Risk**: Critical - security component
- **Methods untested**: authenticate(), validateToken()
- **Recommendation**: Add security tests ASAP

### 🟡 Partial Coverage

**3. UserManager.php** - 45% coverage
- ✅ Tested: getUser(), createUser()
- ❌ Untested: deleteUser(), updatePermissions()
- **Recommendation**: Add tests for delete and permission methods

### ✅ Well Tested

- DataProcessor.php - 95%
- EmailService.php - 88%
- ValidationHelper.php - 100%

### Suggested Actions

1. **Immediate** (Critical):
   - Add tests for PaymentProcessor
   - Add tests for AuthenticationService

2. **This Sprint**:
   - Complete UserManager tests
   - Add integration tests for checkout flow

3. **Next Sprint**:
   - Increase overall coverage to 80%
   - Add E2E tests for critical paths
```

## Detailed Analysis

### Method-Level Coverage

```markdown
## DataProcessor.php Coverage

| Method | Tested? | Coverage | Priority |
|--------|---------|----------|----------|
| processData() | ✅ Yes | 100% | - |
| validateInput() | ✅ Yes | 90% | Low |
| handleError() | ❌ No | 0% | High |
| formatOutput() | ⚠️ Partial | 60% | Medium |

### Untested Code Paths

**handleError() method:**
```php
public function handleError($error) {
  // Line 45: No test coverage
  if ($error instanceof ValidationException) {
    return $this->formatValidationError($error);
  }
  // Line 49: No test coverage
  if ($error instanceof DatabaseException) {
    return $this->formatDatabaseError($error);
  }
  // Line 53: Tested
  return $this->formatGenericError($error);
}
```

**Missing test cases:**
- ValidationException handling
- DatabaseException handling
- Edge case: null error

**Suggested test:**
```php
public function testHandleValidationException(): void {
  $exception = new ValidationException('Invalid input');
  $result = $this->processor->handleError($exception);
  $this->assertStringContains('validation error', $result);
}
```
```

## Integration with /test-coverage Command

- **This Skill**: Quick coverage checks
  - "Is this function tested?"
  - "What's missing tests?"
  - Single file/class analysis

- **`/test-coverage` Command**: Comprehensive coverage analysis
  - Full project coverage report
  - Trend analysis over time
  - CI/CD integration
  - Detailed HTML reports

## Coverage Goals

### Industry Standards

- **Minimum**: 70% coverage
- **Good**: 80% coverage
- **Excellent**: 90%+ coverage

**But remember**: 100% coverage ≠ bug-free code

### What to Focus On

**High Priority:**
- Authentication/authorization
- Payment processing
- Data validation
- Security-sensitive code
- Critical business logic

**Medium Priority:**
- API endpoints
- Form handlers
- Data transformations
- Email notifications

**Low Priority:**
- Simple getters/setters
- Configuration classes
- View rendering
- Logging statements

## Quick Commands

### PHP (PHPUnit)

```bash
# Text coverage report
vendor/bin/phpunit --coverage-text

# HTML coverage report
vendor/bin/phpunit --coverage-html coverage/

# Coverage for specific test
vendor/bin/phpunit --coverage-text tests/Unit/DataProcessorTest.php

# Kanopi projects
ddev exec vendor/bin/phpunit --coverage-html coverage/
```

### JavaScript (Jest)

```bash
# Terminal coverage
npm test -- --coverage

# HTML report
npm test -- --coverage --coverageReporters=html

# Watch mode with coverage
npm test -- --coverage --watch

# Coverage for specific file
npm test -- --coverage DataProcessor.test.js
```

## Common Gaps & Solutions

### Gap 1: Error Handling

**Untested:**
```php
try {
  $this->processData($data);
} catch (Exception $e) {
  // Untested catch block
  $this->logger->error($e->getMessage());
}
```

**Solution:**
```php
public function testProcessDataWithException(): void {
  $this->expectException(ProcessingException::class);
  $this->processor->processData([]);
}
```

### Gap 2: Edge Cases

**Untested:**
- Empty arrays
- Null values
- Maximum values
- Boundary conditions

**Solution**: Add tests for each edge case

### Gap 3: Integration Points

**Untested:**
- Database interactions
- API calls
- File system operations

**Solution**: Add integration tests or use mocks

## Coverage Best Practices

1. **Test behavior, not coverage** - Don't chase 100% blindly
2. **Focus on critical paths** - Test important code thoroughly
3. **Test edge cases** - Empty, null, min, max values
4. **Test error paths** - Exceptions and error handling
5. **Keep tests fast** - Slow tests won't run
6. **Update tests with code** - Keep tests current

## Resources

- [PHPUnit Code Coverage](https://phpunit.de/manual/current/en/code-coverage-analysis.html)
- [Jest Coverage](https://jestjs.io/docs/cli#--coverageboolean)
- [Code Coverage Best Practices](https://martinfowler.com/bliki/TestCoverage.html)
