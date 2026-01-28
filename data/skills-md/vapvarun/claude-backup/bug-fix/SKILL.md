---
name: bug-fix
description: Systematically diagnose and fix bugs by reproducing issues, identifying root causes, implementing fixes, and preventing regressions. Use when debugging errors, fixing issues, or troubleshooting problems.
---

# Systematic Bug Fixing

A methodical approach to debugging that prioritizes understanding over guessing.

## The Iron Law

**NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST**

## Rule Zero: Verify Bug Reports Before Fixing

**Bug reports, QA comments, and card descriptions can be WRONG. Verify first.**

Before fixing any reported issue:

| Step | Action |
|------|--------|
| 1 | **Read the actual code** - Understand current implementation |
| 2 | **Verify the claim** - Is it actually a bug or misunderstanding? |
| 3 | **Check official docs** - Framework docs, API references, etc. |
| 4 | **Trace execution flow** - Hook order, data flow, lifecycle |
| 5 | **Only fix if confirmed** - Push back with evidence if not a real bug |

**Common false positives:**
- Hook timing claims without understanding framework execution order
- "Missing" features that exist but need to be enabled
- "Bugs" that are actually intended behavior
- Performance issues based on code reading, not profiling

**If the bug report is wrong:** Don't fix it. Comment back explaining why it's not actually a bug.

Attempting solutions without understanding the underlying problem leads to:
- Wasted time (2-3 hours vs 15-30 minutes)
- New bugs introduced
- Original issue not actually fixed
- Technical debt accumulation

## When to Apply This Methodology

Use for any technical issue:
- Test failures
- Production bugs
- Unexpected behavior
- Performance problems
- Build failures
- Integration issues

Apply **especially** when:
- Under time pressure
- Quick fixes seem obvious
- After multiple failed attempts
- Understanding is incomplete

## Four Sequential Phases

### Phase 1: Root Cause Investigation

Complete these steps BEFORE proposing any fix:

#### 1. Read Error Messages Thoroughly

```bash
# Don't skip past errors - they often contain solutions
# Note: line numbers, file paths, error codes

# BAD: Glancing at error
"Something about undefined..."

# GOOD: Full analysis
Error: Cannot read property 'name' of undefined
    at getUserData (src/services/user.js:45:23)
    at async handleRequest (src/api/handler.js:12:15)
# -> Issue is in getUserData at line 45, 'name' accessed on undefined value
```

#### 2. Reproduce Consistently

```javascript
// Document exact reproduction steps
/*
REPRODUCTION STEPS:
1. Login as test user (test@example.com)
2. Navigate to /dashboard
3. Click "Export" button
4. Select date range > 30 days
5. Click "Generate"
ERROR: "Cannot read property 'map' of undefined"

ENVIRONMENT:
- Browser: Chrome 120
- Node: 18.17.0
- OS: macOS 14.1
*/
```

#### 3. Check Recent Changes

```bash
# What changed recently?
git log --oneline -20
git diff HEAD~5..HEAD -- src/

# Who touched the failing file?
git blame src/services/user.js

# When did it last work?
git bisect start
git bisect bad HEAD
git bisect good v1.2.3
```

#### 4. Trace Data Flow Backward

```javascript
// Work backward through call stack to find WHERE bad values originate

// Error occurs here:
function displayUser(user) {
  return user.name.toUpperCase(); // user is undefined!
}

// Trace back: Who calls displayUser?
function renderProfile() {
  const user = getCurrentUser(); // Returns undefined!
  return displayUser(user);
}

// Trace back: Why does getCurrentUser return undefined?
function getCurrentUser() {
  return userCache.get(userId); // userId is null!
}

// ROOT CAUSE FOUND: userId is null before cache lookup
```

#### 5. Gather Evidence in Multi-Component Systems

```javascript
// For systems with multiple layers, add diagnostic logging

// API -> Service -> Database
async function debugDataFlow() {
  console.log('[API] Request received:', req.body);

  const serviceResult = await service.process(data);
  console.log('[SERVICE] Result:', serviceResult);

  const dbResult = await db.save(serviceResult);
  console.log('[DB] Saved:', dbResult);

  // Identify which layer fails
}
```

### Phase 2: Pattern Analysis

Before forming solutions:

#### 1. Find Working Examples

```javascript
// Look for similar code that WORKS in the codebase

// Broken:
const users = await fetchUsers();
users.map(u => u.name); // Fails when users is undefined

// Working (in another file):
const posts = await fetchPosts();
if (!posts || posts.length === 0) {
  return [];
}
posts.map(p => p.title); // Works because of guard clause
```

#### 2. Compare Against References

```javascript
// Read documentation/examples COMPLETELY

// API Documentation says:
// fetchUsers() returns Promise<User[] | null>
// Returns null when: user not authenticated, rate limited

// Your assumption was:
// fetchUsers() always returns User[]

// FIX: Handle null case
const users = await fetchUsers();
if (!users) {
  throw new AuthenticationError('Not authenticated');
}
```

#### 3. List All Differences

```markdown
| Aspect | Working Code | Broken Code |
|--------|--------------|-------------|
| Null check | Yes | No |
| Error handling | try/catch | None |
| Async handling | await | Missing await |
| Input validation | Validates | Trusts input |
```

### Phase 3: Hypothesis and Testing

Apply scientific methodology:

#### 1. Form Single Hypothesis

```javascript
// State clearly: "I think X is the root cause because Y"

// HYPOTHESIS:
// The error occurs because fetchUsers() returns null when the
// session token expires, but we don't handle the null case.
// Evidence: Error only happens after ~30 minutes of inactivity
// (matching our 30-minute session timeout).
```

#### 2. Test Minimally

```javascript
// Make the SMALLEST possible change to test your theory
// One variable at a time

// TEST:
const users = await fetchUsers();
console.log('fetchUsers returned:', users, typeof users);
// If null: hypothesis confirmed
// If array: hypothesis wrong, form new hypothesis
```

#### 3. Verify or Reject

```javascript
// If test confirms hypothesis -> Phase 4
// If test rejects hypothesis -> Form new hypothesis

// DON'T: Add multiple fixes hoping one works
// DO: Test one thing, understand result, proceed logically
```

### Phase 4: Implementation

Fix the ROOT CAUSE, not symptoms:

#### 1. Create Failing Test Case

```javascript
// Write test BEFORE fix
describe('fetchUsers', () => {
  it('handles null response from expired session', async () => {
    // Arrange
    mockSession.expire();

    // Act & Assert
    await expect(getUserList()).rejects.toThrow('Session expired');
  });
});
```

#### 2. Implement Single Fix

```javascript
// BAD: Multiple changes at once
async function getUserList() {
  try {
    const users = await fetchUsers();
    if (!users) throw new Error('No users');
    if (!Array.isArray(users)) users = [users];
    return users.filter(u => u.active).map(u => u.name);
  } catch (e) {
    console.error(e);
    return [];
  }
}

// GOOD: Address only the identified root cause
async function getUserList() {
  const users = await fetchUsers();
  if (!users) {
    throw new SessionExpiredError('Session expired, please login again');
  }
  return users.map(u => u.name);
}
```

#### 3. Verify Fix

```bash
# Run specific test
npm test -- --grep "handles null response"

# Run related tests
npm test -- src/services/user.test.js

# Run full suite to check for regressions
npm test
```

#### 4. Handle Failed Fixes

```markdown
After 2 unsuccessful attempts:
  -> Return to Phase 1, gather more evidence

After 3+ failures:
  -> Question whether the architecture is fundamentally sound
  -> Discuss with team before continuing
  -> Consider if refactoring is needed
```

## Red Flags - Return to Phase 1

Stop immediately if you think:

| Thought | Why It's Wrong |
|---------|----------------|
| "Quick fix for now, investigate later" | You'll never investigate later |
| "Just try changing X and see if it works" | Random changes introduce new bugs |
| "It's probably X, let me fix that" | "Probably" means you don't know |
| "I don't fully understand but this might work" | Guaranteed to fail or cause new issues |

## Common Bug Categories

### Null/Undefined Errors

```javascript
// Problem: Accessing property on null/undefined
user.profile.avatar.url

// Solutions:
// 1. Optional chaining
user?.profile?.avatar?.url

// 2. Guard clauses
if (!user?.profile?.avatar) return defaultAvatar;

// 3. Nullish coalescing
const url = user?.profile?.avatar?.url ?? defaultAvatar;
```

### Async/Await Issues

```javascript
// Problem: Missing await
async function loadData() {
  const data = fetchData(); // Missing await!
  console.log(data); // Promise, not data
}

// Problem: Parallel vs Sequential
// BAD: Sequential (slow)
const user = await fetchUser();
const posts = await fetchPosts();
const comments = await fetchComments();

// GOOD: Parallel (fast)
const [user, posts, comments] = await Promise.all([
  fetchUser(),
  fetchPosts(),
  fetchComments(),
]);
```

### Race Conditions

```javascript
// Problem: State changes during async operation
async function updateUser() {
  const user = this.state.user; // Captured at start
  const updated = await api.updateUser(user);
  this.setState({ user: updated }); // Overwrites changes made during await!
}

// Solution: Use functional update
this.setState(prevState => ({
  user: { ...prevState.user, ...updated }
}));
```

### Off-by-One Errors

```javascript
// Problem: Array bounds
for (let i = 0; i <= array.length; i++) { // <= should be <
  array[i]; // Undefined on last iteration
}

// Problem: Pagination
const page = 1;
const offset = page * pageSize; // Should be (page - 1) * pageSize
```

### State Mutation

```javascript
// Problem: Mutating state directly
const newArray = oldArray;
newArray.push(item); // Mutates oldArray too!

// Solution: Create new references
const newArray = [...oldArray, item];
const newObject = { ...oldObject, newProperty: value };
```

## Debugging Tools

### Browser DevTools

```javascript
// Breakpoints
debugger; // Pauses execution

// Console methods
console.log(obj);
console.table(arrayOfObjects);
console.trace(); // Shows call stack
console.time('operation');
// ... operation
console.timeEnd('operation');
```

### Node.js Debugging

```bash
# Inspect mode
node --inspect src/index.js

# Break on first line
node --inspect-brk src/index.js

# Debug tests
node --inspect-brk node_modules/.bin/jest --runInBand
```

### Git Bisect

```bash
# Find the commit that introduced the bug
git bisect start
git bisect bad                 # Current commit is bad
git bisect good v1.2.0         # This version was good
# Git checks out middle commit
# Test it, then:
git bisect good  # or
git bisect bad
# Repeat until git finds the bad commit
git bisect reset  # Return to original state
```

## Debugging Checklist

- [ ] Can reproduce the issue consistently
- [ ] Read complete error message and stack trace
- [ ] Checked recent changes (git log/blame)
- [ ] Identified root cause (not just symptoms)
- [ ] Found working example for comparison
- [ ] Formed testable hypothesis
- [ ] Fix addresses root cause only
- [ ] Created regression test
- [ ] Tested edge cases
- [ ] No new issues introduced
- [ ] Documented the fix

## Post-Fix Actions

1. **Add regression test** - Prevent issue from returning
2. **Update documentation** - If behavior was unclear
3. **Consider related code** - Same bug elsewhere?
4. **Add monitoring** - Detect if it happens again
5. **Share learnings** - Help team avoid similar issues
