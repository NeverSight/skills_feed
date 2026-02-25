---
name: debugging
description: "Load PROACTIVELY when task involves investigating errors, diagnosing failures, or tracing unexpected behavior. Use when user says \"debug this\", \"fix this error\", \"why is this failing\", \"trace this issue\", or \"it's not working\". Covers error message and stack trace analysis, runtime debugging, network request inspection, state debugging, performance profiling, type error diagnosis, build failure resolution, and root cause analysis with memory-informed pattern matching against past failures."
metadata:
  version: 1.0.0
  category: quality
  tags: [debugging, errors, runtime, network, state, performance, analysis]
---

## Resources
```
scripts/
  validate-debugging.sh
references/
  debugging-patterns.md
```

# Debugging Quality Skill

This skill teaches you how to debug systematically using GoodVibes precision tools. Effective debugging requires a methodical approach: reproduce the issue, isolate the cause, identify the root problem, apply a fix, and verify the solution.

## When to Use This Skill

Load this skill when:
- Investigating runtime errors or exceptions
- Tracing unexpected behavior or logic errors
- Analyzing network request/response issues
- Debugging state management problems
- Diagnosing performance bottlenecks
- Investigating build or compilation errors
- Understanding TypeScript type errors
- Performing root cause analysis

Trigger phrases: "debug this error", "why is this failing", "investigate the issue", "trace the problem", "analyze the error".

## Core Workflow

### Phase 1: Reproduce - Confirm the Issue

Before debugging, confirm you can reproduce the issue reliably.

#### Step 1.1: Gather Error Context

Collect all available error information.

```yaml
precision_exec:
  commands:
    - cmd: "npm run typecheck 2>&1"
    - cmd: "npm run lint 2>&1"
    - cmd: "npm run build 2>&1"
  verbosity: standard
```

**What to capture:**
- Complete error message and stack trace
- Error type and code (if applicable)
- File path and line number
- Timestamps and environment info
- User actions that triggered the error

#### Step 1.2: Find Error Occurrences

Search for similar errors in the codebase.

```yaml
discover:
  queries:
    - id: error_throw_sites
      type: grep
      pattern: "throw new (Error|TypeError|RangeError)"
      glob: "**/*.{ts,tsx,js,jsx}"
    - id: error_handlers
      type: grep
      pattern: "catch\\s*\\("
      glob: "**/*.{ts,tsx,js,jsx}"
    - id: console_errors
      type: grep
      pattern: "console\\.(error|warn)"
      glob: "**/*.{ts,tsx,js,jsx}"
  verbosity: locations
```

**Pattern categories:**

| Error Pattern | Meaning | Common Causes |
|---------------|---------|---------------|
| ReferenceError | Variable not defined | Typo, missing import, scope issue |
| TypeError | Wrong type used | null/undefined, wrong method, type mismatch |
| RangeError | Value out of range | Array index, numeric overflow |
| SyntaxError | Invalid syntax | Parsing error, malformed JSON |
| NetworkError | Request failed | CORS, timeout, 404, auth failure |

#### Step 1.3: Reproduce Locally

Run the failing operation to confirm reproduction.

```yaml
precision_exec:
  commands:
    - cmd: "npm run dev"
      timeout_ms: 5000
  verbosity: minimal
```

**Reproduction checklist:**
- [ ] Error reproduces consistently
- [ ] Minimal steps to reproduce identified
- [ ] Environment matches production (Node version, deps)
- [ ] Error message matches reported issue

### Phase 2: Isolate - Narrow Down the Cause

Reduce the problem space to find where the error originates.

#### Step 2.1: Read the Stack Trace

Analyze the call stack to understand execution flow.

**Stack trace example:**
```
TypeError: Cannot read property 'name' of undefined
    at getUserName (src/utils/user.ts:42:18)
    at UserProfile (src/components/UserProfile.tsx:15:22)
    at renderWithHooks (node_modules/react/cjs/react.development.js:1234)
```

**Reading strategy:**
1. **Start at the top** - The actual error location
2. **Trace backwards** - Follow the call chain
3. **Ignore node_modules** - Focus on your code
4. **Find the entry point** - Where did the bad data come from?

```yaml
precision_read:
  files:
    - path: "src/utils/user.ts"
      extract: content
      range: {start: 35, end: 50}
    - path: "src/components/UserProfile.tsx"
      extract: content
      range: {start: 10, end: 25}
  verbosity: standard
```

#### Step 2.2: Trace Data Flow

Follow the data from source to error point.

```yaml
discover:
  queries:
    - id: function_calls
      type: grep
      pattern: "getUserName\\("
      glob: "**/*.{ts,tsx}"
    - id: data_sources
      type: grep
      pattern: "(fetch|axios|prisma).*user"
      glob: "**/*.{ts,tsx}"
    - id: prop_passing
      type: grep
      pattern: "user=\\{"
      glob: "**/*.tsx"
  verbosity: locations
```

**Data flow analysis:**
- Where does the data originate? (API, database, props)
- What transformations occur? (map, filter, destructure)
- What assumptions are made? (not null, specific shape)
- Where could it become undefined?

#### Step 2.3: Check Boundary Conditions

Test edge cases where errors commonly occur.

```yaml
discover:
  queries:
    - id: array_access
      type: grep
      pattern: "\\[[0-9]+\\]|\\[.*\\]"
      glob: "**/*.{ts,tsx}"
    - id: null_checks
      type: grep
      pattern: "(if.*===.*null|if.*===.*undefined|\\?\\.|\\?\\?)"
      glob: "**/*.{ts,tsx}"
    - id: optional_chaining
      type: grep
      pattern: "\\?\\."
      glob: "**/*.{ts,tsx}"
  verbosity: locations
```

**Common boundary issues:**

| Issue | Example | Fix |
|-------|---------|-----|
| Array out of bounds | `arr[arr.length]` | Check `arr.length > 0` |
| Null/undefined access | `user.name` | Use `user?.name` |
| Division by zero | `total / count` | Check `count !== 0` |
| Empty string operations | `str[0]` | Check `str.length > 0` |
| Missing object keys | `obj.key` | Use `obj?.key ?? default` |

### Phase 3: Identify - Pinpoint the Root Cause

Determine the underlying problem, not just the symptom.

#### Step 3.1: Analyze Error Patterns

Classify the error to understand common causes.

**Type Errors**

```yaml
precision_exec:
  commands:
    - cmd: "npm run typecheck 2>&1 | head -50"
  verbosity: standard
```

**Common TypeScript errors:**

| Error Code | Meaning | Fix |
|------------|---------|-----|
| TS2339 | Property does not exist | Add property to type or use optional chaining |
| TS2345 | Argument type mismatch | Fix the type or add type assertion |
| TS2322 | Type not assignable | Change the type or fix the value |
| TS2571 | Object is of type unknown | Add type guard or assertion |
| TS7006 | Implicit any parameter | Add parameter type annotation |

**Runtime Errors**

```yaml
discover:
  queries:
    - id: unsafe_access
      type: grep
      pattern: "\\.[a-zA-Z]+(?!\\?)"
      glob: "**/*.{ts,tsx}"
    - id: async_errors
      type: grep
      pattern: "await.*(?!try)"
      glob: "**/*.{ts,tsx}"
  verbosity: files_only
```

**Common runtime errors:**
- Cannot read property X of undefined
- Cannot read property X of null
- X is not a function
- X is not iterable
- Maximum call stack size exceeded (infinite recursion)

#### Step 3.2: Check Dependencies and Imports

Module resolution errors are common.

```yaml
discover:
  queries:
    - id: imports
      type: grep
      pattern: "^import.*from"
      glob: "**/*.{ts,tsx}"
    - id: dynamic_imports
      type: grep
      pattern: "import\\("
      glob: "**/*.{ts,tsx}"
    - id: require_statements
      type: grep
      pattern: "require\\("
      glob: "**/*.{ts,js}"
  verbosity: locations
```

**Common import issues:**

| Issue | Symptom | Fix |
|-------|---------|-----|
| Missing export | Module has no exported member | Add export to source file |
| Circular dependency | Cannot access before initialization | Restructure imports |
| Wrong path | Module not found | Fix relative path or alias |
| Default vs named | X is not a function | Use `import X` or `import { X }` |
| Type-only import | Cannot use as value | Remove `type` keyword |

#### Step 3.3: Validate Assumptions

Question assumptions about data shape and state.

```yaml
precision_grep:
  queries:
    - id: type_assertions
      pattern: "as (unknown|any|[A-Z][a-zA-Z]+)"
      glob: "**/*.{ts,tsx}"
  output:
    format: context
    context_before: 2
    context_after: 2
  verbosity: standard
```

**Dangerous assumptions:**
- API always returns expected shape
- Array is never empty
- User is always authenticated
- Data is always valid
- Props are always provided

**Validate with:**
- Runtime type validation (Zod, Yup)
- Type guards (`if (typeof x === 'string')`)
- Null checks (`if (x != null)`)
- Default values (`x ?? defaultValue`)

### Phase 4: Fix - Apply the Solution

Implement the fix based on root cause analysis.

#### Step 4.1: Choose the Right Fix

Match the fix to the problem type.

**Type Safety Fixes**

```typescript
// Before: Implicit any
function getUser(id) {
  return users.find(u => u.id === id);
}

// After: Explicit types
function getUser(id: string): User | undefined {
  return users.find(u => u.id === id);
}
```

**Null Safety Fixes**

```typescript
// Before: Unsafe access
const name = user.profile.name;

// After: Optional chaining
const name = user?.profile?.name ?? 'Anonymous';
```

**Async Error Handling**

```typescript
// Before: Unhandled promise
await fetchData();

// After: Try/catch
try {
  await fetchData();
} catch (error: unknown) {
  logger.error('Failed to fetch data', { error });
  throw new AppError('Data fetch failed', { cause: error });
}
```

**Array Boundary Fixes**

```typescript
// Before: Unsafe access
const first = items[0];

// After: Safe access
const first = items.length > 0 ? items[0] : null;
// Or: const first = items.at(0) ?? null;
```

#### Step 4.2: Add Defensive Code

Prevent similar errors in the future.

**Input validation:**

```typescript
import { z } from 'zod';

const userSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  name: z.string().min(1).max(100),
});

function processUser(data: unknown) {
  const user = userSchema.parse(data); // Throws if invalid
  // Now user is type-safe
}
```

**Type guards:**

```typescript
function isUser(value: unknown): value is User {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'email' in value
  );
}

if (isUser(data)) {
  // TypeScript knows data is User
  logger.info('User email', { email: data.email });
}
```

**Error boundaries (React):**

```typescript
import { ErrorBoundary } from 'react-error-boundary';

function ErrorFallback({ error }: { error: Error }) {
  return (
    <div role="alert">
      <p>Something went wrong:</p>
      <pre>{error.message}</pre>
    </div>
  );
}

<ErrorBoundary FallbackComponent={ErrorFallback}>
  <MyComponent />
</ErrorBoundary>
```

#### Step 4.3: Apply the Fix

Use precision_edit to make the change.

```yaml
precision_edit:
  edits:
    - path: "src/utils/user.ts"
      find: |
        function getUserName(user) {
          return user.name;
        }
      replace: |
        function getUserName(user: User | undefined): string {
          return user?.name ?? 'Unknown';
        }
  verbosity: minimal
```

### Phase 5: Verify - Confirm the Fix Works

Validate that the fix resolves the issue without breaking anything.

#### Step 5.1: Type Check

Ensure TypeScript errors are resolved.

```yaml
precision_exec:
  commands:
    - cmd: "npm run typecheck"
  verbosity: standard
```

**All type errors must be resolved.**

#### Step 5.2: Run Tests

Confirm tests pass.

```yaml
precision_exec:
  commands:
    - cmd: "npm test"
  verbosity: standard
```

**If tests fail:**
- Fix introduced a regression
- Test expectations need updating
- Test revealed another issue

#### Step 5.3: Manual Verification

Reproduce the original error scenario.

```yaml
precision_exec:
  commands:
    - cmd: "npm run dev"
      timeout_ms: 5000
  verbosity: minimal
```

**Verification checklist:**
- [ ] Original error no longer occurs
- [ ] Edge cases handled (null, empty, large values)
- [ ] No new errors introduced
- [ ] Performance not degraded
- [ ] User experience improved

### Phase 6: Network Debugging

Debug API requests and responses.

#### Step 6.1: Find Network Calls

Locate all HTTP requests.

```yaml
discover:
  queries:
    - id: fetch_calls
      type: grep
      pattern: "fetch\\("
      glob: "**/*.{ts,tsx,js,jsx}"
    - id: axios_calls
      type: grep
      pattern: "axios\\.(get|post|put|delete|patch)"
      glob: "**/*.{ts,tsx,js,jsx}"
    - id: api_routes
      type: glob
      patterns: ["src/app/api/**/*.ts", "pages/api/**/*.ts"]
  verbosity: locations
```

#### Step 6.2: Check Request/Response Handling

Validate error handling for network calls.

```yaml
precision_grep:
  queries:
    - id: fetch_with_catch
      pattern: "fetch\\([^)]+\\).*catch"
      glob: "**/*.{ts,tsx,js,jsx}"
  output:
    format: context
    context_after: 5
  verbosity: standard
```

**Common network issues:**

| Issue | Symptom | Fix |
|-------|---------|-----|
| CORS error | Blocked by CORS policy | Add CORS headers to API |
| 401 Unauthorized | Missing or invalid token | Add auth header, refresh token |
| 404 Not Found | Wrong URL or route | Fix endpoint path |
| 500 Server Error | Backend exception | Check server logs, fix backend |
| Timeout | Request takes too long | Increase timeout, optimize backend |
| Network failure | Failed to fetch | Check connectivity, retry logic |

**Debugging CORS:**

```typescript
// Next.js API route
export async function GET(request: Request) {
  return Response.json(data, {
    headers: {
      'Access-Control-Allow-Origin': '*', // Development only - use specific origin in production
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
  });
}
```

**Debugging authentication:**

```typescript
// Check for auth header
const token = request.headers.get('Authorization')?.replace('Bearer ', '');
if (!token) {
  return Response.json({ error: 'Unauthorized' }, { status: 401 });
}

try {
  const session = await verifyToken(token);
} catch (error: unknown) {
  logger.error('Token verification failed', { error });
  return Response.json({ error: 'Invalid token' }, { status: 401 });
}
```

#### Step 6.3: Validate Request Payloads

Ensure request data is correct.

```yaml
discover:
  queries:
    - id: request_bodies
      type: grep
      pattern: "(body:|JSON.stringify)"
      glob: "**/*.{ts,tsx}"
    - id: validation_schemas
      type: grep
      pattern: "z\\.object\\("
      glob: "**/*.{ts,tsx}"
  verbosity: locations
```

**Request validation:**

```typescript
import { z } from 'zod';

const createUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
});

export async function POST(request: Request) {
  const body = await request.json();
  const result = createUserSchema.safeParse(body);
  
  if (!result.success) {
    return Response.json(
      { error: 'Validation failed', details: result.error.flatten() },
      { status: 400 }
    );
  }
  
  // Now result.data is type-safe
}
```

### Phase 7: State Debugging

Debug React state and state management.

#### Step 7.1: Find State Usage

Locate state declarations and updates.

```yaml
discover:
  queries:
    - id: useState_calls
      type: grep
      pattern: "useState<?"
      glob: "**/*.{tsx,jsx}"
    - id: state_updates
      type: grep
      pattern: "set[A-Z][a-zA-Z]*\\("
      glob: "**/*.{tsx,jsx}"
    - id: useEffect_hooks
      type: grep
      pattern: "useEffect\\("
      glob: "**/*.{tsx,jsx}"
  verbosity: locations
```

**Common state issues:**

| Issue | Symptom | Fix |
|-------|---------|-----|
| Stale closure | State value is outdated | Use functional update |
| Missing dependency | useEffect doesn't re-run | Add to dependency array |
| Infinite loop | Component re-renders forever | Fix dependencies or condition |
| State race condition | Updates override each other | Use reducer or queue |
| Lost state on unmount | Data disappears | Lift state up or use global state |

**Stale closure fix:**

```typescript
// Before: Stale closure
const [count, setCount] = useState(0);

function increment() {
  setTimeout(() => {
    setCount(count + 1); // count is stale
  }, 1000);
}

// After: Functional update
function increment() {
  setTimeout(() => {
    setCount(prev => prev + 1); // Always current
  }, 1000);
}
```

**useEffect dependency fix:**

```typescript
// Before: Missing dependency
useEffect(() => {
  fetchData(userId);
}, []); // userId changes ignored

// After: Complete dependencies
useEffect(() => {
  fetchData(userId);
}, [userId]); // Re-runs when userId changes
```

#### Step 7.2: Check for State Mutations

Find direct state mutations (anti-pattern).

```yaml
discover:
  queries:
    - id: array_mutations
      type: grep
      pattern: "\\.(push|pop|shift|unshift|splice)\\("
      glob: "**/*.{tsx,jsx}"
    - id: object_mutations
      type: grep
      pattern: "[a-zA-Z]+\\.[a-zA-Z]+\\s*=\\s*"
      glob: "**/*.{tsx,jsx}"
  verbosity: locations
```

**Immutable updates:**

```typescript
// Before: Mutation
const [items, setItems] = useState([1, 2, 3]);
items.push(4); // BAD: Mutates state
setItems(items);

// After: Immutable
setItems([...items, 4]); // GOOD: New array

// Object updates
const [user, setUser] = useState({ name: 'Alice', age: 30 });
setUser({ ...user, age: 31 }); // GOOD: New object
```

### Phase 8: Performance Debugging

Diagnose performance bottlenecks.

#### Step 8.1: Find Performance Anti-patterns

Search for common performance issues.

```yaml
discover:
  queries:
    - id: n_plus_one
      type: grep
      pattern: "(for|forEach|map).*await.*(prisma|db|query)"
      glob: "**/*.{ts,tsx}"
    - id: inline_objects
      type: grep
      pattern: "(onClick|onChange|style)=\\{\\{"
      glob: "**/*.{tsx,jsx}"
    - id: missing_memo
      type: grep
      pattern: "(map|filter|reduce|sort)\\("
      glob: "**/*.{tsx,jsx}"
  verbosity: locations
```

**Performance issues:**

| Anti-pattern | Impact | Fix |
|--------------|--------|-----|
| N+1 queries | Slow database queries | Use `include` or batch loading |
| Inline objects in JSX | Unnecessary re-renders | Extract to constant or useMemo |
| Large lists without virtualization | Slow rendering | Use react-window or similar |
| Missing indexes | Slow queries | Add database indexes |
| Unnecessary re-renders | Laggy UI | Use React.memo, useMemo, useCallback |

#### Step 8.2: Profile Build Performance

Check for slow builds.

```yaml
precision_exec:
  commands:
    - cmd: "npm run build"
  verbosity: standard
```

**Build performance issues:**
- Large bundle size (check with bundle analyzer)
- Slow TypeScript compilation (check tsconfig)
- Missing tree-shaking (check imports)
- Development dependencies in production (check package.json)

### Phase 9: Root Cause Analysis

Go beyond symptoms to find underlying issues.

#### Step 9.1: Ask Why Five Times

Drill down to the root cause.

**Example:**
1. **Why did the app crash?** - User data was undefined
2. **Why was user data undefined?** - API returned null
3. **Why did API return null?** - Database query returned no rows
4. **Why were there no rows?** - User ID was incorrect
5. **Why was user ID incorrect?** - Route parameter parsing failed

**Root cause:** Route parameter parsing doesn't handle edge cases.

#### Step 9.2: Check System Dependencies

Validate environment and dependencies.

```yaml
precision_exec:
  commands:
    - cmd: "node --version"
    - cmd: "npm --version"
    - cmd: "npm list --depth=0"
  verbosity: minimal
```

**Common dependency issues:**
- Version mismatch (package.json vs lockfile)
- Peer dependency conflicts
- Outdated packages with known bugs
- Missing native dependencies

#### Step 9.3: Review Recent Changes

Find what changed before the error appeared.

```yaml
precision_exec:
  commands:
    - cmd: "git log --oneline -10"
    - cmd: "git diff HEAD~5..HEAD"
  verbosity: standard
```

**Git bisect for complex issues:**

```bash
git bisect start
git bisect bad HEAD
git bisect good v1.0.0
# Test, then mark:
git bisect good  # or bad
# Repeat until culprit commit found
```

### Phase 10: Prevention - Avoid Future Issues

Add safeguards to prevent recurrence.

#### Step 10.1: Add Tests

Write tests that catch the error.

```typescript
import { describe, it, expect } from 'vitest';

describe('getUserName', () => {
  it('should handle undefined user', () => {
    expect(getUserName(undefined)).toBe('Unknown');
  });
  
  it('should handle user without name', () => {
    expect(getUserName({ id: '123' })).toBe('Unknown');
  });
  
  it('should return user name', () => {
    expect(getUserName({ id: '123', name: 'Alice' })).toBe('Alice');
  });
});
```

#### Step 10.2: Add Logging

Log key decision points for future debugging.

```typescript
import { logger } from '@/lib/logger';

function processUser(user: User | undefined) {
  if (!user) {
    logger.warn('User is undefined in processUser');
    return null;
  }
  
  logger.info('Processing user', { userId: user.id });
  
  try {
    // Process user
  } catch (error: unknown) {
    logger.error('Failed to process user', { userId: user.id, error });
    throw error;
  }
}
```

**Logging best practices:**
- Use structured logging (JSON)
- Include context (user ID, request ID)
- Use appropriate log levels (error, warn, info, debug)
- Never log sensitive data (passwords, tokens)
- Use correlation IDs to trace requests

#### Step 10.3: Add Monitoring

Track errors in production.

**Error tracking (Sentry, Rollbar):**

```typescript
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  tracesSampleRate: 0.1,
  beforeSend(event, hint) {
    // Filter sensitive data
    if (event.request) {
      delete event.request.cookies;
    }
    return event;
  },
});
```

**Custom error classes:**

```typescript
export class AppError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number = 500,
    public context?: Record<string, unknown>
  ) {
    super(message);
    this.name = 'AppError';
  }
}

throw new AppError('User not found', 'USER_NOT_FOUND', 404, { userId });
```

## Common Debugging Patterns

See `references/debugging-patterns.md` for detailed patterns organized by category.

### Error Pattern Detection

Use `discover` to find multiple error patterns at once.

```yaml
discover:
  queries:
    # Type safety issues
    - { id: any_usage, type: grep, pattern: ':\\s*any', glob: '**/*.{ts,tsx}' }
    - { id: type_assertions, type: grep, pattern: 'as (any|unknown)', glob: '**/*.{ts,tsx}' }
    # Runtime safety
    - { id: unsafe_access, type: grep, pattern: '\\.[a-zA-Z]+(?!\\?)', glob: '**/*.{ts,tsx}' }
    - { id: unhandled_promises, type: grep, pattern: 'await.*(?!try)', glob: '**/*.{ts,tsx}' }
    # Performance
    - { id: n_plus_one, type: grep, pattern: 'for.*await.*prisma', glob: '**/*.{ts,tsx}' }
    - { id: inline_objects, type: grep, pattern: 'onClick=\\{\\{', glob: '**/*.{tsx,jsx}' }
  verbosity: locations
```

### Systematic Error Analysis

**Step 1: Categorize the error**
- Type error (compile-time)
- Runtime error (null, undefined, type mismatch)
- Logic error (wrong behavior, no exception)
- Performance error (too slow)
- Network error (API failure)

**Step 2: Find similar patterns**
- Search for the error message
- Search for the error type
- Search for the failing function name

**Step 3: Trace the data**
- Where does the data come from?
- What transformations occur?
- Where does it fail?

**Step 4: Validate assumptions**
- Is the data shape correct?
- Are types accurate?
- Are edge cases handled?

**Step 5: Fix and verify**
- Apply the fix
- Run type check
- Run tests
- Verify manually

## Precision Tools for Debugging

### Discover Tool

Run parallel searches to find error patterns.

```yaml
discover:
  queries:
    - id: error_sites
      type: grep
      pattern: "throw new"
      glob: '**/*.{ts,tsx,js,jsx}'
    - id: catch_blocks
      type: grep
      pattern: "catch\\s*\\("
      glob: '**/*.{ts,tsx,js,jsx}'
    - id: console_logs
      type: grep
      pattern: "console\\.(log|error|warn)"
      glob: '**/*.{ts,tsx,js,jsx}'
  verbosity: locations
```

### Precision Grep

Search with context for understanding surrounding code.

```yaml
precision_grep:
  queries:
    - id: error_context
      pattern: "TypeError|ReferenceError|RangeError"
      glob: "**/*.{ts,tsx,js,jsx}"
  output:
    format: context
    context_before: 5
    context_after: 5
  verbosity: standard
```

### Precision Exec

Run diagnostic commands.

```yaml
precision_exec:
  commands:
    - cmd: "npm run typecheck 2>&1"
    - cmd: "npm run lint 2>&1"
    - cmd: "npm test 2>&1"
  verbosity: standard
```

### Precision Edit

Apply fixes atomically.

```yaml
precision_edit:
  edits:
    - path: "src/utils/user.ts"
      find: "user.name"
      replace: "user?.name ?? 'Unknown'"
  verbosity: minimal
```

## Validation Script

Use `scripts/validate-debugging.sh` to validate debugging practices.

```bash
./scripts/validate-debugging.sh /path/to/project
```

**The script checks:**
- console.log statements removed from production
- Error boundaries implemented
- Source maps configured
- Proper logging libraries used
- Try/catch blocks handling errors
- Debug dependencies excluded from production

## Quick Reference

### Debugging Checklist

**Reproduce:**
- [ ] Error reproduces consistently
- [ ] Minimal reproduction steps identified
- [ ] Environment matches
- [ ] Error message captured

**Isolate:**
- [ ] Stack trace analyzed
- [ ] Data flow traced
- [ ] Boundary conditions tested
- [ ] Similar patterns found

**Identify:**
- [ ] Error categorized
- [ ] Root cause identified (not symptom)
- [ ] Assumptions validated
- [ ] Dependencies checked

**Fix:**
- [ ] Appropriate fix chosen
- [ ] Defensive code added
- [ ] Fix applied
- [ ] No new issues introduced

**Verify:**
- [ ] Type check passes
- [ ] Tests pass
- [ ] Manual verification complete
- [ ] Edge cases tested

**Prevent:**
- [ ] Tests added for the issue
- [ ] Logging added
- [ ] Monitoring configured
- [ ] Documentation updated

### Error Severity Guide

**Critical (fix immediately):**
- Application crashes
- Data loss or corruption
- Security vulnerabilities
- Production outage

**High (fix soon):**
- Feature completely broken
- Poor user experience
- Performance degradation
- Type safety violations

**Medium (fix when able):**
- Edge case failures
- Minor UX issues
- Console warnings
- Missing error handling

**Low (fix eventually):**
- Code style issues
- Missing documentation
- Optimization opportunities
- Refactoring needs

### Common Mistakes to Avoid

**Fixing symptoms, not causes:**
- BAD: Add null check without understanding why it's null
- GOOD: Trace why the value is null and fix the source

**Skipping verification:**
- BAD: Apply fix and assume it works
- GOOD: Run tests, type check, and manual verification

**Ignoring edge cases:**
- BAD: Fix the common case only
- GOOD: Test null, undefined, empty, and large values

**No prevention:**
- BAD: Fix the bug and move on
- GOOD: Add tests and logging to prevent recurrence

## Advanced Techniques

### Binary Search Debugging

For complex issues, use binary search to narrow down.

**Comment out half the code:**
1. Comment out half the function
2. If error persists, problem is in remaining half
3. If error disappears, problem is in commented half
4. Repeat until isolated

### Rubber Duck Debugging

Explain the problem out loud:
1. Describe what the code should do
2. Describe what it actually does
3. Walk through line by line
4. Often reveals the issue during explanation

### Time-Travel Debugging

Use git to find when the bug was introduced:

```bash
git bisect start
git bisect bad HEAD
git bisect good v1.0.0
# Test each commit
git bisect good  # or bad
```

### Logging Strategy

**Trace important values:**

```typescript
function processData(data: unknown) {
  logger.debug('Input data', { data });
  
  const validated = schema.parse(data);
  logger.debug('Validated data', { validated });
  
  const transformed = transform(validated);
  logger.debug('Transformed data', { transformed });
  
  return transformed;
}
```

**Use correlation IDs:**

```typescript
import { v4 as uuid } from 'uuid';

export async function POST(request: Request) {
  const requestId = uuid();
  logger.info('Request started', { requestId });
  
  try {
    const result = await processRequest(request);
    logger.info('Request completed', { requestId });
    return Response.json(result);
  } catch (error: unknown) {
    logger.error('Request failed', { requestId, error });
    throw error;
  }
}
```

## Integration with Other Skills

- Use **error-recovery** for automated fix attempts
- Use **code-review** to catch errors during review
- Use **testing-strategy** to prevent regressions
- Use **performance-audit** for performance issues
- Use **security-audit** for security vulnerabilities

## Resources

- `references/debugging-patterns.md` - Common error patterns by category
- `scripts/validate-debugging.sh` - Automated debugging practice validation
- Chrome DevTools - https://developer.chrome.com/docs/devtools/
- React DevTools - https://react.dev/learn/react-developer-tools
- Node.js Debugging Guide - https://nodejs.org/en/docs/guides/debugging-getting-started/
