---
name: debugger
description:
  Diagnose and fix runtime issues, errors, and bugs through systematic
  reproduction, root cause analysis, and targeted fixes. Use for debugging
  production issues, test failures, performance problems, and any type of
  software defect.
---

# Debugger Skill

Systematically diagnose and fix software bugs through structured investigation,
reproduction, root cause analysis, and targeted fixes.

## When to Use

Use this skill for:

- **Runtime Errors**: Exception handling, crashes, unhandled rejections
- **Test Failures**: Unit tests, integration tests, E2E tests not passing
- **Type Errors**: TypeScript compilation errors, type mismatches
- **Logic Bugs**: Incorrect behavior, wrong output, edge cases
- **Performance Issues**: Slow execution, memory leaks, bottlenecks
- **Integration Issues**: API failures, database errors, third-party service
  issues
- **Race Conditions**: Timing issues, async/await problems
- **State Management**: Redux, Context, or hook state bugs

Don't use for:

- New feature implementation (use feature-implementer)
- Code refactoring without bugs (use refactorer)
- Initial research (use Explore agent)

## Quick Start

### Step 1: Issue Understanding

```
What: [Brief description of the bug]
Where: [File(s) and line number(s)]
When: [Conditions when it occurs]
Impact: [Severity: Critical/High/Medium/Low]
Evidence: [Error message, stack trace, or behavior]
```

### Step 2: Reproduce

Create minimal reproduction:

- Identify exact steps to trigger
- Document environment conditions
- Capture before/after state
- Note any workarounds

### Step 3: Investigate

Use systematic approach:

- Read relevant code
- Trace execution flow
- Check data values at key points
- Verify assumptions

### Step 4: Root Cause

Identify the fundamental issue:

- Why did it happen?
- What was the incorrect assumption?
- What edge case was missed?

### Step 5: Fix

Implement targeted solution:

- Minimal change to fix root cause
- Add safeguards against regression
- Update tests if needed

### Step 6: Validate

Verify the fix:

- Original reproduction no longer fails
- Tests pass
- No new issues introduced
- Edge cases covered

## Debugging Methodology

### Phase 1: Gather Evidence

**What to collect:**

- Error messages (complete text)
- Stack traces (full trace, not truncated)
- Log output (with timestamps)
- State snapshots (variables, props, store)
- Environment details (OS, browser, Node version)

**Tools:**

- Logger service output
- Browser DevTools console
- Test runner output (Vitest, Playwright)
- TypeScript compiler errors
- Build output

**Commands:**

```bash
# Run with verbose output
npm run test -- --reporter=verbose

# TypeScript with detailed errors
npx tsc --noEmit --pretty

# Build with stack traces
npm run build 2>&1 | tee build.log
```

### Phase 2: Reproduce Reliably

**Create minimal reproduction:**

1. **Isolate the issue**
   - Remove unrelated code
   - Use minimal data
   - Simplify conditions

2. **Document steps**

   ```
   Reproduction Steps:
   1. [Action 1]
   2. [Action 2]
   3. [Action 3]
   Expected: [What should happen]
   Actual: [What actually happens]
   ```

3. **Verify consistency**
   - Try 3-5 times
   - Note any variations
   - Check different environments

### Phase 3: Form Hypotheses

**Ask systematic questions:**

- Is this a logic error, type error, or runtime error?
- Is it a timing issue (race condition)?
- Is it data-dependent?
- Is it environment-specific?
- Is it a regression (was it working before)?

**Common root causes:**

- Incorrect assumptions about data shape
- Missing null/undefined checks
- Async/await misuse
- Type coercion issues
- Off-by-one errors
- State mutation issues
- Incorrect error handling
- Missing dependencies in useEffect

### Phase 4: Investigate

**Read relevant code:**

```
1. Start at error location
2. Trace backward to find data source
3. Trace forward to find impact
4. Check related components/functions
```

**Add logging (temporarily):**

```typescript
// Use Logger service, not console.log
import { logger } from '@/lib/logging/logger';

logger.debug('Variable state', {
  component: 'ComponentName',
  value: myVar,
  type: typeof myVar,
});
```

**Use debugger statements (for browser):**

```typescript
// Temporary debugging
if (condition) {
  debugger; // Browser will pause here
}
```

### Phase 5: Root Cause Analysis

**Identify the true cause:**

Not just: "Variable is undefined" But: "Function assumes input always has
`.data` property, but API can return `null` on empty results"

Not just: "Test times out" But: "Async function doesn't resolve because mock
doesn't implement `.then()` method"

Not just: "Type error on line 42" But: "Function returns `Promise<T>` but caller
expects `T` because it's not awaiting"

**Causal chain:**

```
Root cause: [Fundamental issue]
    ↓
Proximate cause: [Immediate trigger]
    ↓
Symptom: [Observed error]
```

### Phase 6: Implement Fix

**Fix principles:**

1. **Targeted**: Address root cause, not symptoms

   ```typescript
   // ❌ Bad: Suppress symptom
   try {
     doThing();
   } catch {
     /* ignore */
   }

   // ✅ Good: Fix root cause
   if (data?.hasProperty) {
     doThing();
   }
   ```

2. **Minimal**: Smallest change that fixes issue
   - Don't refactor unrelated code
   - Don't add unnecessary features
   - Keep scope focused

3. **Defensive**: Add safeguards

   ```typescript
   // Add validation
   if (!data || !data.items) {
     logger.warn('Invalid data structure', { data });
     return [];
   }
   ```

4. **Tested**: Ensure it works
   - Original reproduction passes
   - Add test for regression prevention
   - Verify edge cases

**Common fix patterns:**

**Null/undefined handling:**

```typescript
// ❌ Before
const result = data.items[0].value;

// ✅ After
const result = data?.items?.[0]?.value ?? defaultValue;
```

**Async/await:**

```typescript
// ❌ Before
useEffect(() => {
  const data = await fetchData();
  setData(data);
}, []);

// ✅ After
useEffect(() => {
  const loadData = async () => {
    const data = await fetchData();
    setData(data);
  };
  void loadData();
}, []);
```

**Type errors:**

```typescript
// ❌ Before
function process(value: string | null): string {
  return value.toUpperCase(); // Error: Object is possibly null
}

// ✅ After
function process(value: string | null): string {
  return value?.toUpperCase() ?? '';
}
```

### Phase 7: Validate Fix

**Validation checklist:**

- [ ] Original error no longer occurs
- [ ] Tests pass (all, not just related ones)
- [ ] Build succeeds
- [ ] Lint passes
- [ ] No new errors introduced
- [ ] Edge cases work
- [ ] Performance not degraded

**Run validation:**

```bash
# Full validation
npm run lint && npm run test && npm run build
```

## Debugging Patterns by Issue Type

### TypeScript Errors

**Common issues:**

1. Type mismatch
2. Property doesn't exist
3. Object is possibly undefined
4. Await outside async function
5. Argument count mismatch

**Debugging approach:**

1. Read error message carefully (TypeScript errors are descriptive)
2. Check type definitions with `Cmd+Click` (VS Code)
3. Verify actual type vs expected type
4. Look for missing null checks
5. Check async/await usage

**Example fix:**

```typescript
// Error: Property 'name' does not exist on type 'User | null'
const userName = user.name;

// Fix: Add null check
const userName = user?.name ?? 'Anonymous';
```

### Test Failures

**Common issues:**

1. Mock not configured correctly
2. Async operation not awaited
3. Test isolation issues (shared state)
4. Timeout (async not resolving)
5. Assertion mismatch

**Debugging approach:**

1. Read test output carefully
2. Run single test in isolation
3. Check mock setup
4. Verify async operations resolve
5. Add console logging (temporarily)

**Example fix:**

```typescript
// ❌ Test failing: Mock not properly awaitable
vi.mock('@/lib/service', () => ({
  fetchData: vi.fn(() => ({ data: 'test' })),
}));

// ✅ Fix: Return promise
vi.mock('@/lib/service', () => ({
  fetchData: vi.fn(() => Promise.resolve({ data: 'test' })),
}));
```

### Runtime Errors

**Common issues:**

1. Uncaught exception
2. Unhandled promise rejection
3. Cannot read property of undefined
4. Function not defined
5. Network request failure

**Debugging approach:**

1. Check stack trace for error origin
2. Verify data shape at error point
3. Add defensive checks
4. Check for race conditions
5. Verify dependencies loaded

**Example fix:**

```typescript
// ❌ Error: Cannot read property 'length' of undefined
const count = items.length;

// ✅ Fix: Add defensive check
const count = items?.length ?? 0;
```

### Performance Issues

**Common issues:**

1. Infinite loop
2. Unnecessary re-renders
3. Memory leak
4. Large data processing
5. Blocking operations

**Debugging approach:**

1. Use React DevTools Profiler
2. Check useEffect dependencies
3. Look for missing memoization
4. Profile with browser DevTools
5. Check for cleanup functions

**Example fix:**

```typescript
// ❌ Performance issue: Infinite re-render
useEffect(() => {
  setData(processData(data));
}, [data]); // Triggers on own update!

// ✅ Fix: Remove circular dependency
useEffect(() => {
  setData(processData(initialData));
}, [initialData]);
```

### Race Conditions

**Common issues:**

1. State update after unmount
2. Multiple async operations
3. Callback with stale closure
4. Event handler timing

**Debugging approach:**

1. Check async operation lifecycle
2. Add cleanup functions
3. Use refs for latest values
4. Add abort controllers

**Example fix:**

```typescript
// ❌ Race condition: Update after unmount
useEffect(() => {
  fetchData().then(data => setData(data));
}, []);

// ✅ Fix: Add cleanup
useEffect(() => {
  let mounted = true;
  fetchData().then(data => {
    if (mounted) setData(data);
  });
  return () => {
    mounted = false;
  };
}, []);
```

## Project-Specific Debugging

### Novelist.ai Specifics

**Logger Service (REQUIRED):**

```typescript
import { logger } from '@/lib/logging/logger';

// ❌ Never use console.log
console.log('Debug:', value);

// ✅ Always use logger
logger.debug('Debug message', {
  component: 'ComponentName',
  value,
});
```

**Database Debugging:**

```typescript
// Check Turso connection
logger.debug('Database query', {
  component: 'ServiceName',
  table: 'table_name',
  params,
});
```

**Test Debugging:**

- Vitest for unit tests
- Playwright for E2E tests
- Use `data-testid` attributes for selectors

**Common Novelist.ai Issues:**

- LocalStorage vs Turso sync issues
- Device ID generation in tests
- Plot Engine state management
- World Building data relationships

## Advanced Debugging

### Binary Search Debugging

For complex bugs, use binary search:

1. Find known good state (e.g., working commit)
2. Find known bad state (e.g., current broken state)
3. Check midpoint
4. Narrow down until isolated

```bash
# Git bisect for regressions
git bisect start
git bisect bad HEAD
git bisect good <known-good-commit>
# Git will checkout midpoint
# Test and mark good/bad until found
```

### Heisenbug (Disappears when debugging)

Strategies:

1. Add non-invasive logging
2. Record state snapshots
3. Check for timing dependencies
4. Look for race conditions
5. Test in production mode

### Rubber Duck Debugging

When stuck:

1. Explain the problem out loud (or in writing)
2. Describe what the code does line-by-line
3. State your assumptions explicitly
4. Often reveals the issue

## Best Practices

### DO:

✓ Read error messages completely ✓ Create minimal reproductions ✓ Form
hypotheses before changing code ✓ Fix root cause, not symptoms ✓ Add tests for
regressions ✓ Use Logger service (not console.log) ✓ Validate fixes thoroughly ✓
Document complex bugs

### DON'T:

✗ Guess randomly ("try-and-see" debugging) ✗ Make multiple changes at once ✗
Skip reproduction step ✗ Fix symptoms without understanding cause ✗ Leave debug
code in production ✗ Ignore test failures ✗ Over-complicate fixes

## Output Format

When completing debugging, provide:

```markdown
## Debug Report: [Issue Title]

### Issue Summary

- **What**: [Brief description]
- **Where**: [File:line]
- **Severity**: [Critical/High/Medium/Low]

### Symptoms

- [Observed error or behavior]
- [Stack trace or error message]

### Reproduction Steps

1. [Step 1]
2. [Step 2]
3. [Result]

### Root Cause

[Explanation of fundamental issue]

### Solution

[Description of fix applied]

**Files Modified:**

- [File path 1] - [What was changed]
- [File path 2] - [What was changed]

### Validation

- [✓] Original issue resolved
- [✓] Tests passing
- [✓] Build succeeds
- [✓] No regressions

### Prevention

[How to avoid this in the future]
```

## Examples

### Example 1: Async/Await Error

**Issue**: Build fails with "await outside async function"

**Investigation**:

1. Read error: Line 140 in useWritingAssistant.ts
2. Found: `await` in useEffect callback
3. Root cause: useEffect callbacks can't be async

**Fix**:

```typescript
// Before
useEffect(() => {
  const data = await loadData();
  setData(data);
}, []);

// After
useEffect(() => {
  const load = async () => {
    const data = await loadData();
    setData(data);
  };
  void load();
}, []);
```

**Validation**: Build passes, tests pass ✓

### Example 2: Test Timeout

**Issue**: Test times out after 10 seconds

**Investigation**:

1. Test calls async function
2. Mock returns object, not promise
3. Test awaits forever

**Root cause**: Mock missing `.then()` method

**Fix**:

```typescript
// Before
mock.fn(() => ({ data: 'test' }));

// After
mock.fn(() => Promise.resolve({ data: 'test' }));
```

**Validation**: Test passes in <100ms ✓

### Example 3: Type Error

**Issue**: Property 'items' doesn't exist on type 'Response | null'

**Investigation**:

1. API can return null
2. Code assumes always returns object
3. No null check

**Root cause**: Missing null handling

**Fix**:

```typescript
// Before
const items = response.items;

// After
const items = response?.items ?? [];
```

**Validation**: TypeScript compiles, runtime safe ✓

## Integration with Other Skills

- **iterative-refinement**: For fixing multiple bugs in cycles
- **goap-agent**: For coordinating complex debugging across multiple files
- **test-runner**: For validating fixes
- **code-reviewer**: For reviewing fix quality

## Tools Available

This skill has access to:

- **Read**: Read source files
- **Grep**: Search for patterns
- **Glob**: Find files
- **Edit**: Fix bugs
- **Bash**: Run tests, build, validate

Use these tools systematically to diagnose and fix issues.
