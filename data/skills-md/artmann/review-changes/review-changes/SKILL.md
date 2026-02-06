---
name: review-changes
description: Review code changes in a feature branch before merging. Use when asked to review a branch, review changes, check a PR, or audit code before merge. Compares the current branch against the default branch (main/master) and categorizes issues by severity (Critical, Major, Minor) with actionable solutions.
license: MIT
metadata:
  author: Christoffer Artmann
  version: "1.0.0"
---

# Review Changes

Review code changes in a feature branch and identify issues before merging.

## Workflow

### 1. Determine Review Target

- **Remote PR**: If user provides PR number or URL (e.g., "review PR #123", "review https://github.com/org/repo/pull/123"):
  1. Checkout the PR: `gh pr checkout <PR_NUMBER>`
  2. Read PR context: `gh pr view <PR_NUMBER> --json title,body,comments`
  3. Use the PR description and comments as additional context for the review

- **Local Changes**: If no PR specified, review current branch against default branch (continue to step 2)

### 2. Detect Branches

```bash
# Get current branch
git branch --show-current

# Detect default branch (try remote HEAD, fall back to main)
git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo "main"
```

### 3. Get Changed Files

```bash
# List files changed between default branch and current branch
git diff --name-only <default-branch>...HEAD

# Get full diff for analysis
git diff <default-branch>...HEAD
```

### 4. Analyze Changes

Read each changed file and review for issues. Adapt review criteria to the detected language.

#### Review Process

For each changed file, systematically apply the guidelines from the "Things to look for" section:

1. **Identify applicable guidelines**: Based on the file type and content, determine which guidelines apply:
   - All **General Guidelines** apply to every file (API changes, auth, database, concurrency, async, external APIs, edge cases, defensive coding, memory/performance, file system, logging, testing, accessibility, code style)
   - Add **Language-Specific Guidelines** based on file extension (`.ts`/`.js` → TypeScript/JavaScript, `.tsx`/`.jsx` → React, `.py` → Python, `.go` → Go, `.rs` → Rust, `.java`/`.kt` → Java/Kotlin)

2. **Review each guideline explicitly**: Go through each applicable guideline and check if the code violates it:
   - Read the guideline's checklist items
   - Scan the changed code for violations
   - If a violation is found, note the file, line number, and specific issue
   - Assign severity based on the guideline's indicated level (Critical, Major, or Minor)

3. **Skip inapplicable guidelines**: If a guideline doesn't apply to the code (e.g., no database operations → skip Database & Persistence), move to the next one.

4. **Document findings as you go**: For each issue found, immediately record:
   - Which guideline was violated
   - The specific file and line number
   - What the problem is
   - How to fix it

Example review flow for a TypeScript API endpoint file:
```
□ API & Breaking Changes - Check for signature changes, removed fields
□ Authentication & Authorization - Check for auth middleware on routes
□ Database & Persistence - Check for N+1 queries, missing transactions
□ Concurrency - Check for race conditions in shared state
□ Async Code - Check for post-await validation
□ External API Handling - Check for timeouts, retries, error handling
□ Edge Cases & Boundaries - Check for null checks, empty arrays
□ Defensive Coding - Check for input validation
□ Memory & Performance - Check for unbounded collections, leaks
□ File System Operations - Check for existence checks, error handling
□ Logging & Observability - Check for meaningful error context
□ Testing Quality - N/A (not a test file)
□ Accessibility - N/A (not a UI file)
□ Code Style - Check for early returns, flat code
□ TypeScript/JavaScript - Check for dispose(), path.join(), URLSearchParams
□ React - N/A (not a React component)
```

#### Critical Issues (Must Fix)

Block the merge. These will break production or cause security incidents.

- **Broken code**: Syntax errors, undefined variables, missing imports, type errors
- **Security vulnerabilities**: SQL injection, XSS, exposed secrets/credentials, insecure auth
- **Data leaks**: Logging sensitive data, exposing PII, missing access controls
- **Runtime failures**: Code paths that will definitely crash in production

#### Major Issues (Should Fix)

Will likely cause problems for users or developers.

- **Unhandled async**: Promises without `.catch()` or `try/catch`, missing `await`
- **Missing error handling**: Bare try blocks, swallowed exceptions, no fallback for failures
- **No timeouts/retries**: Network calls without timeout, no retry logic for flaky operations
- **Resource leaks**: Unclosed connections, file handles, event listeners not cleaned up
- **Race conditions**: Shared state mutations, missing locks, concurrent access issues
- **Missing validation**: User input not validated, missing null checks on external data

#### Minor Issues (Nice to Fix)

Won't break anything but would improve the code.

- **Code clarity**: Confusing variable names, overly complex logic, missing comments on non-obvious code
- **Consistency**: Mixed patterns, inconsistent naming, style drift from codebase norms
- **Performance**: Obvious inefficiencies, N+1 patterns, unnecessary re-computation, O(n²) lookups where a `Set` or `Map` would provide O(1)
- **Dead code**: Unused variables, unreachable branches, commented-out code, redundant checks that can never be true due to earlier conditions
- **Code duplication**: Near-identical code blocks that should be extracted to a helper function
- **TODO/FIXME**: Unresolved todos that should be addressed

### 5. Check Test Coverage

For each new or modified file containing business logic:

- Check if corresponding test file exists
- If tests exist, verify new code paths have coverage
- Flag missing tests for critical paths

### 6. Format Output

Present findings grouped by severity, ordered Critical → Major → Minor.

```
## Branch Review: `feature/xyz` → `main`

### 🔴 Critical (X issues)

**1. [Brief title]**
- **File**: `path/to/file.ts:42`
- **Problem**: Clear description of what's wrong
- **Fix**: Specific solution

### 🟠 Major (X issues)

**1. [Brief title]**
- **File**: `path/to/file.ts:87`
- **Problem**: Description
- **Fix**: Solution

### 🟡 Minor (X issues)

**1. [Brief title]**
- **File**: `path/to/file.ts:123`
- **Problem**: Description
- **Fix**: Solution

---
**Summary**: X critical, Y major, Z minor issues found.
[Ready to merge / Needs fixes before merge]
```

If no issues found in a category, omit that section. End with clear merge recommendation.

#### Feedback Tone

- Be constructive and professional—explain *why* a change is needed, not just what to change
- Provide actionable suggestions: instead of "this is wrong", say "consider X because Y"
- For approvals, acknowledge the specific value of the contribution (e.g., "Good use of early returns for readability")
- When flagging issues, assume positive intent—the author may not have been aware of the concern

## Things to look for

Adapt review focus based on detected language and framework.

---

### General Guidelines

#### API & Breaking Changes

Flag changes that could break existing consumers:

- **Removed or renamed public functions/methods** without deprecation period
- **Changed function signatures** (new required parameters, changed return types)
- **Modified response shapes** in API endpoints (removed fields, changed types)
- **Changed default values** that alter existing behavior
- **Database schema changes** without migration scripts

```ts
// ❌ Bad - breaking change without migration path
function getUser(id: string): User  // was: function getUser(id: number): User

// ✅ Good - backwards compatible with deprecation
/** @deprecated Use getUserById(id: string) instead. Will be removed in v3.0 */
function getUser(id: number): User
function getUserById(id: string): User
```

#### Authentication & Authorization

Flag as **Critical** when security boundaries are weakened:

- **Missing auth checks** on new endpoints or routes
- **Downgraded permissions** (e.g., changing from admin-only to public)
- **Hardcoded credentials** or API keys in source code
- **JWT/session issues**: Missing expiry, weak secrets, improper validation
- **CORS misconfigurations**: Overly permissive origins (`*` in production)

```ts
// ❌ Bad - endpoint without auth check
app.get('/api/users/:id/private-data', (req, res) => {
  return db.getPrivateData(req.params.id);
});

// ✅ Good - proper auth middleware
app.get('/api/users/:id/private-data', requireAuth, checkOwnership, (req, res) => {
  return db.getPrivateData(req.params.id);
});
```

#### Database & Persistence

- **Missing transactions** for multi-step operations that should be atomic
- **N+1 query patterns**: Fetching related data in loops instead of joins/eager loading
- **Missing indexes** on frequently queried columns (especially foreign keys)
- **Unbounded queries**: `SELECT *` without `LIMIT` on potentially large tables
- **SQL injection**: String concatenation in queries instead of parameterized queries

```ts
// ❌ Bad - N+1 queries
const users = await db.getUsers();
for (const user of users) {
  user.posts = await db.getPostsByUserId(user.id); // Query per user!
}

// ✅ Good - single query with join
const users = await db.getUsersWithPosts();
```

#### Concurrency

Flag as **Critical** for data corruption risks:

- **Shared mutable state** accessed from multiple threads without synchronization
- **Missing locks/mutexes** when modifying shared resources
- **Check-then-act patterns** without atomicity (TOCTOU vulnerabilities)
- **Deadlock potential**: Acquiring multiple locks in inconsistent order

```ts
// ❌ Bad - race condition (check-then-act)
if (!cache.has(key)) {
  const value = await expensiveComputation();
  cache.set(key, value); // Another thread may have set it already
}

// ✅ Good - atomic operation
const value = cache.getOrSet(key, () => expensiveComputation());
```

#### Async Code

After any `await`, verify that assumptions made before the await are still valid. The world may have changed: files may have been deleted, state may have been modified, or resources may no longer be available.

##### Post-Await State Validation

Flag when code returns success without verifying the expected outcome:

```ts
// ❌ Bad - assumes setup succeeded
await this.setupController(notebook);
return true;

// ✅ Good - validates result before returning success
await this.setupController(notebook);
if (!this.controllers.has(notebookKey)) {
  logger.warn('Setup did not create controller');
  return false;
}
return true;
```

#### External API Handling

- **Missing timeouts** on HTTP requests (can hang indefinitely)
- **No retry logic** for transient failures (network blips, 503s)
- **Missing circuit breakers** for repeatedly failing services
- **Insufficient error handling**: Not distinguishing between 4xx and 5xx errors
- **Missing rate limiting** awareness (no backoff on 429 responses)

```ts
// ❌ Bad - no timeout, no retry, swallows errors
const data = await fetch(url).then(r => r.json()).catch(() => null);

// ✅ Good - timeout, retry logic, proper error handling
const data = await fetchWithRetry(url, {
  timeout: 5000,
  retries: 3,
  backoff: 'exponential',
  onError: (err, attempt) => logger.warn(`Attempt ${attempt} failed`, err)
});
```

#### Edge Cases & Boundaries

- **Empty collections**: Code assumes arrays/lists are non-empty
- **Null/undefined handling**: Missing checks on optional values
- **Boundary values**: Off-by-one errors in loops, incorrect range checks
- **Type coercion issues**: Implicit conversions leading to unexpected behavior
- **Unicode/encoding issues**: Assuming ASCII, incorrect string length calculations

```ts
// ❌ Bad - assumes non-empty array
const first = items[0].name;

// ✅ Good - handles empty case
const first = items[0]?.name ?? 'default';
```

#### Defensive Coding

- **Trusting external input**: Using data from APIs/users without validation
- **Assuming success**: Not handling failure cases for operations that can fail
- **Missing bounds checks**: Array access without verifying index is valid
- **Implicit assumptions**: Code relies on undocumented behavior or ordering

```ts
// ❌ Bad - trusts external data shape
const userName = apiResponse.user.profile.name;

// ✅ Good - validates structure
const userName = apiResponse?.user?.profile?.name;
if (!userName) {
  throw new ValidationError('Invalid API response: missing user name');
}
```

#### Input Sanitization

External data is untrusted. Any input from users, files, APIs, or environment must be sanitized before use in sensitive contexts.

##### Command Injection

Flag as **Critical**. Never pass unsanitized input to shell commands. Use argument arrays instead of string interpolation.

```ts
// ❌ Bad - command injection vulnerability
const output = execSync(`git log --author="${userInput}"`);

// ✅ Good - use argument array (no shell interpolation)
const output = execFileSync('git', ['log', `--author=${userInput}`]);

// ❌ Bad - file content used in command
const config = fs.readFileSync('config.txt', 'utf8');
execSync(`process ${config}`); // config.txt could contain: "; rm -rf /"

// ✅ Good - validate/sanitize file content first
const config = fs.readFileSync('config.txt', 'utf8');
if (!/^[a-zA-Z0-9_-]+$/.test(config)) {
  throw new Error('Invalid config format');
}
execFileSync('process', [config]);
```

##### Path Traversal

Flag as **Critical**. User input in file paths can escape intended directories. Always validate and resolve paths.

```ts
// ❌ Bad - path traversal vulnerability
const filePath = `./uploads/${userFilename}`;
// userFilename could be: "../../../etc/passwd"

// ✅ Good - resolve and validate path stays within allowed directory
const uploadsDir = path.resolve('./uploads');
const filePath = path.resolve(uploadsDir, userFilename);
if (!filePath.startsWith(uploadsDir + path.sep)) {
  throw new Error('Invalid file path');
}
```

##### XSS Prevention

Flag as **Critical**. User input rendered as HTML can execute malicious scripts. Always escape or use safe APIs.

```ts
// ❌ Bad - XSS vulnerability
element.innerHTML = `<p>Hello, ${userName}</p>`;

// ✅ Good - use textContent for plain text
element.textContent = `Hello, ${userName}`;

// ✅ Good - escape if HTML structure needed
import { escape } from 'lodash';
element.innerHTML = `<p>Hello, ${escape(userName)}</p>`;

// ❌ Bad - user input in URL without validation
link.href = userProvidedUrl; // Could be: "javascript:alert('xss')"

// ✅ Good - validate URL protocol
const url = new URL(userProvidedUrl);
if (!['http:', 'https:'].includes(url.protocol)) {
  throw new Error('Invalid URL protocol');
}
link.href = url.href;
```

##### Log Injection

Unsanitized input in logs can forge entries or inject control characters.

```ts
// ❌ Bad - log injection
logger.info(`User logged in: ${username}`);
// username could be: "admin\n[ERROR] System compromised"

// ✅ Good - sanitize or use structured logging
logger.info('User logged in', { username: username.replace(/[\n\r]/g, '') });

// ✅ Better - structured logging with proper escaping
logger.info({ event: 'login', username }); // Let logger handle encoding
```

##### SQL Injection

Flag as **Critical**. Never concatenate user input into queries. Use parameterized queries or prepared statements.

```ts
// ❌ Bad - SQL injection
const query = `SELECT * FROM users WHERE name = '${userName}'`;

// ✅ Good - parameterized query
const query = 'SELECT * FROM users WHERE name = ?';
db.query(query, [userName]);

// ✅ Good - ORM with built-in escaping
const user = await User.findOne({ where: { name: userName } });
```

#### Memory & Performance

- **Unbounded collections**: Arrays/maps that grow without limits
- **Memory leaks**: Event listeners not removed, closures holding references
- **Large allocations in loops**: Creating objects that could be reused
- **Blocking operations**: Synchronous I/O or CPU-heavy work on main thread
- **Missing pagination**: Loading entire datasets when only a subset is needed

```ts
// ❌ Bad - unbounded cache, memory leak
const cache = new Map();
function getCached(key: string) {
  if (!cache.has(key)) {
    cache.set(key, computeExpensiveValue(key));
  }
  return cache.get(key);
}

// ✅ Good - LRU cache with max size
const cache = new LRUCache({ maxSize: 1000 });
```

#### File System Operations

Flag these issues:

- **Missing file existence checks**: Reading files without verifying they exist first
- **Missing directory checks**: Writing files without ensuring parent directory exists
- **No error handling on fs operations**: File operations that assume success without try/catch or error callbacks

Look for patterns like:

- `fs.readFile(path)` without prior `fs.existsSync(path)` or `fs.access()` check
- `fs.writeFile(path)` without ensuring `path.dirname(path)` exists
- `open()`, `fopen()`, `File.read()` etc. without existence validation

#### Logging & Observability

Flag issues that hamper debugging production issues:

- **Insufficient logging**: No logs for important operations, errors without context
- **Excessive logging**: Verbose logs that create noise or performance issues
- **Missing correlation IDs**: Unable to trace requests across services
- **Logging sensitive data**: PII, passwords, tokens in log output (this is **Critical**)
- **No metrics/monitoring**: New features without observability hooks

```ts
// ❌ Bad - no context for debugging
logger.error('Failed');

// ✅ Good - actionable log with context
logger.error('Payment processing failed', {
  orderId,
  userId,
  errorCode: err.code,
  attempt: retryCount
});
```

#### Testing Quality

- **Tests that don't assert anything meaningful**: Empty tests, assertions that always pass
- **Missing edge case coverage**: Only happy path tested
- **Flaky tests**: Tests with race conditions, time dependencies, or external dependencies
- **Test pollution**: Tests that affect each other (shared state, missing cleanup)
- **Mocking too much**: Tests that don't exercise real code paths

```ts
// ❌ Bad - test doesn't verify behavior
it('should process data', async () => {
  await processData(input);
  expect(true).toBe(true);
});

// ✅ Good - verifies actual behavior
it('should transform input data correctly', async () => {
  const result = await processData(input);
  expect(result.status).toBe('processed');
  expect(result.items).toHaveLength(3);
});
```

#### Accessibility

Flag accessibility issues:

- **Missing alt text** on images
- **Non-semantic HTML**: Using divs for buttons, missing form labels
- **Keyboard inaccessible**: Interactive elements not reachable via keyboard
- **Missing ARIA labels** on icon-only buttons
- **Color-only indicators**: Information conveyed only through color

```tsx
// ❌ Bad - inaccessible button
<div onClick={handleClick} className="button">
  <Icon name="delete" />
</div>

// ✅ Good - accessible button
<button onClick={handleClick} aria-label="Delete item">
  <Icon name="delete" aria-hidden="true" />
</button>
```

#### Code Style

Prefer early returns over nested if statements. Flat code is easier to read and reason about.

```ts
// ❌ Bad - deeply nested
function process(data) {
  if (data) {
    if (data.valid) {
      if (data.items.length > 0) {
        return doWork(data);
      }
    }
  }
  return null;
}

// ✅ Good - early returns
function process(data) {
  if (!data) {
    return null;
  }
  if (!data.valid) {
    return null;
  }
  if (data.items.length === 0) {
    return null;
  }
  return doWork(data);
}
```

#### Error Messages

Flag error messages that fail to help users understand and resolve problems.

**Requirements for good error messages:**
- **Actionable** - Tell users what to do, not just what went wrong
- **Contextual** - Include what operation was attempted and relevant values
- **Specific** - "An error occurred" is never helpful
- **User-appropriate** - Don't expose stack traces or internal details to end users
- **Include identifiers** - Order IDs, user IDs, etc. for debugging
- **Error codes** - For programmatic handling and support tickets

```ts
// ❌ Bad - generic, not actionable
throw new Error('An error occurred');
throw new Error('Invalid input');
throw new Error('Operation failed');

// ✅ Good - specific, actionable, includes context
throw new Error('Failed to save user profile: email "user@example.com" is already registered. Please use a different email address.');
throw new Error(`Payment failed for order ${orderId}: card declined. Please check your card details or try a different payment method.`);
throw new Error(`File upload failed: ${filename} exceeds the 10MB size limit. Please compress the file or upload a smaller one.`);
```

For API/system errors, wrap internal details appropriately:

```ts
// ❌ Bad - exposes internals, not helpful to users
throw new Error('ECONNREFUSED 127.0.0.1:5432');
throw new Error('NullPointerException at line 42');
throw new Error(err.stack);

// ✅ Good - user-friendly with error code for support
throw new UserFacingError(
  'Unable to save your changes. Please try again in a few moments.',
  { code: 'DB_UNAVAILABLE', internal: err.message }
);
```

---

### Language/Framework-Specific Guidelines

#### TypeScript/JavaScript

- Unhandled promise rejections, missing `await`
- `any` types hiding bugs, incorrect type assertions
- Missing null checks (`?.` and `??` usage)
- Event listener cleanup in components

##### Disposable Resources

Flag when objects with `dispose()` methods are created but never disposed:

- `CancellationTokenSource` - must call `dispose()` in finally block
- `Disposable` subscriptions from event listeners
- Timer handles (`setTimeout`/`setInterval`) without cleanup

```ts
// ❌ Bad - CancellationTokenSource never disposed (causes listener leaks)
const cts = new CancellationTokenSource();
await doWork(cts.token);

// ✅ Good - disposed in finally block
const cts = new CancellationTokenSource();
try {
  await doWork(cts.token);
} finally {
  cts.dispose();
}
```

##### Filesystem

Always use `path.resolve()` or `path.join()` to build paths. Hardcoded path strings with `/` or `\` separators break cross-platform compatibility.

```ts
// ❌ Bad - hardcoded path separators
const modelPath = "data/models";
const filePath = dir + "/" + filename;

// ✅ Good - path module handles separators
import path from "path";

const modelPath = path.join("data", "models");
const filePath = path.join(dir, filename);
```

##### URLs

Always use `URLSearchParams` to construct query strings. Manual string concatenation is error-prone and fails to properly encode special characters.

```ts
// ❌ Bad - manual concatenation
const url = `/api/search?q=${query}&page=${page}`;

// ✅ Good - URLSearchParams handles encoding
const params = new URLSearchParams({ q: query, page: String(page) });
const url = `/api/search?${params}`;
```

##### Timers and Intervals

Always store timer IDs and clear them on cleanup. Uncleaned timers cause memory leaks and unexpected behavior.

```ts
// ❌ Bad - timer never cleared
function startPolling() {
  setInterval(() => fetchData(), 5000);
}

// ✅ Good - return cleanup function
function startPolling() {
  const id = setInterval(() => fetchData(), 5000);
  return () => clearInterval(id);
}

// ❌ Bad - setTimeout in loop without tracking
for (let i = 0; i < 5; i++) {
  setTimeout(() => process(i), i * 1000);
}

// ✅ Good - track all timer IDs for cleanup
const timers = [];
for (let i = 0; i < 5; i++) {
  timers.push(setTimeout(() => process(i), i * 1000));
}
// Later: timers.forEach(clearTimeout);
```

For precise timing, prefer recursive `setTimeout` over `setInterval`. Intervals can drift and stack if callbacks take longer than the interval:

```ts
// ⚠️ setInterval can drift and stack callbacks
setInterval(async () => {
  await slowOperation(); // If this takes >1000ms, callbacks stack
}, 1000);

// ✅ Recursive setTimeout waits for completion
function poll() {
  setTimeout(async () => {
    await slowOperation();
    poll(); // Schedule next only after completion
  }, 1000);
}
```

In Node.js, use `unref()` for background timers that shouldn't keep the process alive:

```ts
// Node.js: timer keeps process alive
const id = setInterval(checkHealth, 30000);

// Node.js: timer won't prevent process exit
const id = setInterval(checkHealth, 30000);
id.unref();
```

#### React

- Only use `useEffect` for side effects (data fetching, subscriptions, DOM mutations). Do not use it to derive or build state—use `useMemo` or compute during render instead.
- Ensure dependency arrays contain diffable values (primitives, stable references). Objects and arrays created inline will cause infinite re-renders.
- Missing `key` props in lists, or using array index as key when items can reorder
- State updates on unmounted components (missing cleanup in useEffect)

```tsx
// ❌ Bad - deriving state in useEffect
const [fullName, setFullName] = useState('');
useEffect(() => {
  setFullName(`${firstName} ${lastName}`);
}, [firstName, lastName]);

// ✅ Good - derive during render
const fullName = `${firstName} ${lastName}`;

// ✅ Also good - memoize if expensive
const fullName = useMemo(() => `${firstName} ${lastName}`, [firstName, lastName]);
```

##### Conditional Hook Calls

Flag as **Critical**. Hooks must be called in the same order on every render. Placing hooks inside conditionals, loops, or after early returns breaks React's internal tracking.

```tsx
// ❌ Bad - hook inside conditional
function Profile({ userId }) {
  if (!userId) {
    return <div>Please log in</div>;
  }
  const [user, setUser] = useState(null); // Hook after early return!
  useEffect(() => fetchUser(userId), [userId]);
  return <div>{user?.name}</div>;
}

// ✅ Good - hooks before any conditionals
function Profile({ userId }) {
  const [user, setUser] = useState(null);
  useEffect(() => {
    if (userId) {
      fetchUser(userId).then(setUser);
    }
  }, [userId]);

  if (!userId) {
    return <div>Please log in</div>;
  }
  return <div>{user?.name}</div>;
}
```

##### Mutating State Directly

Flag as **Critical**. React state must be treated as immutable. Direct mutations (`.push()`, `.splice()`, `obj.prop = x`) won't trigger re-renders and cause stale UI.

```tsx
// ❌ Bad - mutating state directly
const [items, setItems] = useState([]);
const addItem = (item) => {
  items.push(item); // Mutation!
  setItems(items);  // Same reference, no re-render
};

const [user, setUser] = useState({ name: 'Alice', age: 30 });
const updateAge = () => {
  user.age = 31; // Mutation!
  setUser(user);
};

// ✅ Good - create new references
const addItem = (item) => {
  setItems([...items, item]);
};

const updateAge = () => {
  setUser({ ...user, age: 31 });
};
```

##### Missing Hook Dependencies

Variables used inside `useEffect`, `useCallback`, or `useMemo` must be listed in the dependency array to avoid stale closures.

```tsx
// ❌ Bad - missing dependency
const [count, setCount] = useState(0);
const [multiplier, setMultiplier] = useState(2);

useEffect(() => {
  console.log(count * multiplier); // multiplier used but not in deps
}, [count]); // Missing: multiplier

// ✅ Good - all dependencies listed
useEffect(() => {
  console.log(count * multiplier);
}, [count, multiplier]);
```

##### Stale Closures in Callbacks

Event handlers and callbacks passed to child components may capture outdated state values if not properly managed.

```tsx
// ❌ Bad - stale closure in interval
function Counter() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const id = setInterval(() => {
      console.log(count); // Always logs initial value (0)
      setCount(count + 1); // Always sets to 1
    }, 1000);
    return () => clearInterval(id);
  }, []); // count captured at mount time
}

// ✅ Good - use functional update
useEffect(() => {
  const id = setInterval(() => {
    setCount(c => c + 1); // Always has current value
  }, 1000);
  return () => clearInterval(id);
}, []);

// ✅ Also good - include in deps and re-create interval
useEffect(() => {
  const id = setInterval(() => {
    setCount(count + 1);
  }, 1000);
  return () => clearInterval(id);
}, [count]);
```

##### Functional setState for Derived Updates

When the next state depends on the previous state, always use the functional form to avoid race conditions with batched updates.

```tsx
// ❌ Bad - may lose updates when batched
const increment = () => setCount(count + 1);
const incrementTwice = () => {
  setCount(count + 1);
  setCount(count + 1); // Both read same `count`, only increments by 1
};

// ✅ Good - functional updates always use latest state
const increment = () => setCount(c => c + 1);
const incrementTwice = () => {
  setCount(c => c + 1);
  setCount(c => c + 1); // Correctly increments by 2
};
```

##### Async Updates After Unmount

Async operations (fetch, timers) that update state after unmount cause memory leaks and "Can't perform state update on unmounted component" warnings. Use AbortController or cleanup flags.

```tsx
// ❌ Bad - no cleanup for async operation
useEffect(() => {
  fetch(`/api/user/${id}`)
    .then(res => res.json())
    .then(data => setUser(data)); // May run after unmount
}, [id]);

// ✅ Good - AbortController for fetch
useEffect(() => {
  const controller = new AbortController();
  fetch(`/api/user/${id}`, { signal: controller.signal })
    .then(res => res.json())
    .then(data => setUser(data))
    .catch(err => {
      if (err.name !== 'AbortError') {
        throw err;
      }
    });
  return () => controller.abort();
}, [id]);

// ✅ Good - cleanup flag for other async
useEffect(() => {
  let cancelled = false;
  fetchUser(id).then(data => {
    if (!cancelled) {
      setUser(data);
    }
  });
  return () => { cancelled = true; };
}, [id]);
```

##### Inline Objects Breaking Memoization

Inline object/array literals and arrow functions in JSX create new references on every render, breaking `React.memo` and causing unnecessary child re-renders.

```tsx
// ❌ Bad - new object/function on every render
function Parent() {
  return (
    <Child
      style={{ color: 'red' }}  // New object each render
      onClick={() => doSomething()}  // New function each render
      config={{ timeout: 5000 }}  // New object each render
    />
  );
}

// ✅ Good - stable references
const childStyle = { color: 'red' };
const childConfig = { timeout: 5000 };

function Parent() {
  const handleClick = useCallback(() => doSomething(), []);
  return (
    <Child
      style={childStyle}
      onClick={handleClick}
      config={childConfig}
    />
  );
}
```

##### Missing Form preventDefault

Form submissions without `e.preventDefault()` cause full page reloads in SPAs, losing application state.

```tsx
// ❌ Bad - page reloads on submit
function LoginForm() {
  const handleSubmit = (e) => {
    // Missing e.preventDefault()
    login(email, password);
  };
  return <form onSubmit={handleSubmit}>...</form>;
}

// ✅ Good - prevent default form behavior
function LoginForm() {
  const handleSubmit = (e) => {
    e.preventDefault();
    login(email, password);
  };
  return <form onSubmit={handleSubmit}>...</form>;
}
```

##### Timer Cleanup in useEffect

Timers created in `useEffect` must be cleared in the cleanup function. Failing to do so causes memory leaks and state updates on unmounted components.

```tsx
// ❌ Bad - timer not cleared
useEffect(() => {
  setTimeout(() => setStatus('ready'), 1000);
  setInterval(() => setCount(c => c + 1), 1000);
}, []);

// ✅ Good - cleanup both timers
useEffect(() => {
  const timeout = setTimeout(() => setStatus('ready'), 1000);
  const interval = setInterval(() => setCount(c => c + 1), 1000);
  return () => {
    clearTimeout(timeout);
    clearInterval(interval);
  };
}, []);
```

For timers that need to be cleared from event handlers, store the ID in a ref:

```tsx
// ❌ Bad - can't clear timer from handler
function Debounced() {
  useEffect(() => {
    // How do we clear this from onClick?
  }, []);

  const handleClick = () => {
    setTimeout(() => save(), 500); // Creates new timer each click
  };
}

// ✅ Good - ref holds timer ID
function Debounced() {
  const timerRef = useRef<NodeJS.Timeout>();

  const handleClick = () => {
    clearTimeout(timerRef.current); // Clear previous
    timerRef.current = setTimeout(() => save(), 500);
  };

  useEffect(() => {
    return () => clearTimeout(timerRef.current);
  }, []);
}
```

##### XSS and Unsafe HTML

Flag as **Critical**. React escapes content by default, but `dangerouslySetInnerHTML` bypasses this protection. Only use it with sanitized content.

```tsx
// ❌ Bad - XSS vulnerability
function Comment({ text }) {
  return <div dangerouslySetInnerHTML={{ __html: text }} />;
}

// ✅ Good - use a sanitizer library
import DOMPurify from 'dompurify';

function Comment({ text }) {
  return <div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(text) }} />;
}

// ✅ Better - render as plain text when possible
function Comment({ text }) {
  return <div>{text}</div>; // React escapes automatically
}
```

User-controlled URLs in `href` or `src` attributes can execute JavaScript:

```tsx
// ❌ Bad - javascript: URLs execute code
<a href={userUrl}>Click here</a>

// ✅ Good - validate protocol
function SafeLink({ url, children }) {
  const safeUrl = useMemo(() => {
    try {
      const parsed = new URL(url);
      return ['http:', 'https:'].includes(parsed.protocol) ? url : '#';
    } catch {
      return '#';
    }
  }, [url]);
  return <a href={safeUrl}>{children}</a>;
}
```

#### Python

- Bare `except:` clauses swallowing errors
- Missing context managers for resources (`with` statements)
- Mutable default arguments
- Missing type hints on public APIs

```python
# ❌ Bad - mutable default argument
def append_to(item, target=[]):
    target.append(item)
    return target

# ✅ Good - use None as default
def append_to(item, target=None):
    if target is None:
        target = []
    target.append(item)
    return target
```

#### Go

- Ignored error returns (`_ = err`)
- Unclosed resources (defer patterns)
- Data races in goroutines
- Nil pointer dereferences

```go
// ❌ Bad - ignored error
result, _ := doSomething()

// ✅ Good - handle or propagate error
result, err := doSomething()
if err != nil {
    return fmt.Errorf("doSomething failed: %w", err)
}
```

#### Rust

- `unwrap()` on Result/Option in non-test code
- Missing error propagation (`?` operator)
- Unsafe blocks without justification

```rust
// ❌ Bad - unwrap in production code
let value = some_option.unwrap();

// ✅ Good - handle the None case
let value = some_option.ok_or_else(|| Error::MissingValue)?;
```

#### Java/Kotlin

- Unchecked exceptions, missing null handling
- Resource leaks (try-with-resources)
- Mutable shared state

```java
// ❌ Bad - resource leak
FileInputStream fis = new FileInputStream("file.txt");
// ... use fis
fis.close(); // May not be called if exception thrown

// ✅ Good - try-with-resources
try (FileInputStream fis = new FileInputStream("file.txt")) {
    // ... use fis
} // Automatically closed
```
