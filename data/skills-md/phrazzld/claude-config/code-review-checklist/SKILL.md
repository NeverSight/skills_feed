---
name: code-review-checklist
description: "Apply comprehensive code review checklist covering purpose, design, quality, correctness, security, performance, testing, and documentation. Use when reviewing pull requests, conducting code reviews, or self-reviewing changes before committing."
allowed-tools:
  - Read
  - Grep
  - Glob
---

# Code Review Checklist

Fast, focused checklist for reviewing code changes. Designed to complete in <5 minutes for typical PRs.

## Review Mindset

Before reviewing, adopt the right lens:

**The Ousterhout Question**: Does this change fight complexity or add to it?
- Hunt for shallow modules (interface ≈ implementation)
- Hunt for information leakage
- Hunt for generic names (Manager, Helper, Util, Handler)
- Hunt for pass-through methods

**The Torvalds Standard**: "The most important thing is to not make the code worse."
- Good code handles all cases uniformly
- Eliminate edge cases through better abstractions
- If nesting is deep, the structure is wrong

**CRITICAL**: You are capable of detecting subtle design flaws that automated tools miss. Don't just check syntax—evaluate whether this change makes the codebase easier or harder to understand and modify. That's the real job.

## How to Use This Checklist

- **For PR reviews:** Work through categories, flag issues, suggest improvements
- **For self-review:** Before requesting review, check your own changes
- **For pairing:** Use as discussion guide during pair programming

**Not every item applies to every PR.** Use judgment. Small fixes may skip entire categories.

---

## 1. Purpose & Design

**Does this change solve the right problem in the right way?**

- [ ] Does this change solve the stated problem?
- [ ] Is the approach appropriate for the problem scope?
- [ ] Are there simpler alternatives that were considered?
- [ ] Does this fit with existing architecture patterns?

**Red flags:**
- Over-engineered solution for simple problem
- Doesn't address root cause (treats symptom)
- Introduces new pattern when existing one would work

---

## 2. Code Quality

**Is the code readable, maintainable, and simple?**

- [ ] Are names clear and intention-revealing?
- [ ] Is the code self-documenting (minimal comments needed)?
- [ ] Are functions/modules focused on single responsibility?
- [ ] Is complexity managed (no deep nesting, long functions)?
- [ ] Are magic numbers/strings extracted to constants?

**Examples:**

❌ **Poor naming:**
```typescript
function proc(d: any) { ... }
const x = getUserData()
```

✅ **Clear naming:**
```typescript
function processPayment(data: PaymentData) { ... }
const activeUsers = getUserData()
```

❌ **Deep nesting:**
```typescript
if (user) {
  if (user.isActive) {
    if (user.hasPermission) {
      // deeply nested logic
    }
  }
}
```

✅ **Guard clauses:**
```typescript
if (!user) return
if (!user.isActive) return
if (!user.hasPermission) return
// flat logic
```

**Red flags:**
- Generic names (Manager, Helper, Util, Handler)
- Functions over 50 lines
- Nesting deeper than 3 levels
- Unclear variable purposes

---

## 3. Correctness

**Does the code work correctly under all conditions?**

- [ ] Are edge cases handled (null, empty, boundary values)?
- [ ] Is error handling appropriate and informative?
- [ ] Are async operations handled correctly (race conditions, timeouts)?
- [ ] Are types used correctly (no unsafe casts, `any` abuse)?
- [ ] Does the logic match the requirements?

**Edge cases to check:**
- Empty arrays/strings
- Null/undefined values
- Boundary values (0, -1, MAX_INT)
- Concurrent operations
- Network failures

**Examples:**

❌ **Missing edge case:**
```typescript
function getFirstUser(users: User[]) {
  return users[0].name  // Crashes on empty array
}
```

✅ **Edge case handled:**
```typescript
function getFirstUser(users: User[]) {
  return users[0]?.name ?? 'No users'
}
```

❌ **Type abuse:**
```typescript
const data: any = await fetchData()
const userId = (data as User).id  // Unsafe
```

✅ **Type safety:**
```typescript
const data = await fetchData()
if (!isUser(data)) throw new Error('Invalid user data')
const userId = data.id
```

**Red flags:**
- No null checks
- Ignored promise rejections
- Type assertions without validation
- Assumes happy path only

---

## 4. Security

**Are there security vulnerabilities?**

- [ ] Is user input validated and sanitized?
- [ ] Are secrets/credentials handled securely (no hardcoding)?
- [ ] Is authentication/authorization checked where needed?
- [ ] Are SQL/command injection risks mitigated?

**Common vulnerabilities:**

❌ **SQL injection:**
```typescript
db.query(`SELECT * FROM users WHERE id = ${userId}`)
```

✅ **Parameterized query:**
```typescript
db.query('SELECT * FROM users WHERE id = $1', [userId])
```

❌ **Hardcoded secret:**
```typescript
const API_KEY = 'sk_live_abc123...'
```

✅ **Environment variable:**
```typescript
const API_KEY = process.env.API_KEY
if (!API_KEY) throw new Error('API_KEY not configured')
```

❌ **Missing auth check:**
```typescript
async function deleteUser(userId: string) {
  await db.users.delete(userId)
}
```

✅ **Auth check:**
```typescript
async function deleteUser(userId: string, requestingUserId: string) {
  if (!canDeleteUser(requestingUserId, userId)) {
    throw new UnauthorizedError()
  }
  await db.users.delete(userId)
}
```

**Red flags:**
- Direct SQL string concatenation
- Secrets in code
- Missing auth checks on sensitive operations
- Unvalidated redirects or file paths

---

## 5. Performance

**Are there obvious performance issues?**

- [ ] Are there obvious performance issues (N+1 queries, unnecessary loops)?
- [ ] Is data fetching efficient (pagination, caching considered)?
- [ ] Are re-renders/re-computations minimized (React: memo, useMemo)?

**Common issues:**

❌ **N+1 query:**
```typescript
for (const user of users) {
  user.posts = await db.posts.find({ userId: user.id })
}
```

✅ **Batch query:**
```typescript
const userIds = users.map(u => u.id)
const posts = await db.posts.find({ userId: { $in: userIds } })
const postsByUser = groupBy(posts, 'userId')
users.forEach(u => u.posts = postsByUser[u.id] || [])
```

❌ **Unnecessary re-renders:**
```typescript
function UserList({ users }: Props) {
  const sorted = users.sort((a, b) => a.name.localeCompare(b.name))
  // Re-sorts on every render
}
```

✅ **Memoized computation:**
```typescript
function UserList({ users }: Props) {
  const sorted = useMemo(
    () => users.sort((a, b) => a.name.localeCompare(b.name)),
    [users]
  )
}
```

**Red flags:**
- Queries in loops
- Missing indexes on filtered/sorted columns
- Large payloads without pagination
- Expensive computations without memoization

---

## 6. Testing

**Are changes adequately tested?**

- [ ] Are critical paths tested (happy path + key errors)?
- [ ] Do tests verify behavior, not implementation details?
- [ ] Are test names clear about what they verify?

**Good test characteristics:**

✅ **Clear test name:**
```typescript
it('should return 404 when user not found', async () => {
  const response = await request(app).get('/users/999')
  expect(response.status).toBe(404)
})
```

✅ **Tests behavior:**
```typescript
it('should disable submit button while submitting', async () => {
  render(<Form />)
  const button = screen.getByRole('button', { name: 'Submit' })
  await userEvent.click(button)
  expect(button).toBeDisabled()
})
```

❌ **Tests implementation:**
```typescript
it('should call setState when button clicked', () => {
  const mockSetState = jest.fn()
  // Testing implementation detail, not behavior
})
```

**Red flags:**
- No tests for new feature
- Tests only test happy path
- Tests coupled to implementation
- Unclear what test verifies

---

## 7. Documentation

**Is the change adequately documented?**

- [ ] Are non-obvious decisions explained in comments?
- [ ] Is user-facing documentation updated (README, API docs)?
- [ ] Are breaking changes clearly documented?

**When to comment:**

✅ **Explain "why":**
```typescript
// Use exponential backoff to avoid overwhelming API during outages
const retryDelay = Math.pow(2, attempt) * 1000
```

✅ **Document non-obvious behavior:**
```typescript
// Returns null instead of throwing to allow graceful degradation
// when feature flag service is unavailable
function getFeatureFlag(name: string): boolean | null { ... }
```

❌ **Don't explain "what":**
```typescript
// Increment counter by 1
counter += 1
```

**Documentation updates needed:**
- New public API → Update API docs
- Changed behavior → Update README
- Breaking change → Update CHANGELOG, migration guide
- New environment variable → Update deployment docs

**Red flags:**
- Breaking change without migration guide
- New feature without usage examples
- Complex algorithm without explanation
- Changed behavior without updating docs

---

## Quick Decision Guide

### Stop and Fix Now (Block PR)
- Security vulnerabilities
- Data loss scenarios
- Breaking changes without migration path
- Incorrect logic on critical path

### Request Changes (Strong Suggestion)
- Poor naming (hard to understand)
- Missing error handling
- No tests for new behavior
- Performance issues (N+1, obvious bottlenecks)

### Suggest Improvements (Nice to Have)
- Could be simpler
- Could have better names
- Could use helper function
- Could add more tests

### Approve (Minor or Nitpick)
- Style preferences
- Alternative approaches (both work)
- Optional refactoring opportunities

---

## Philosophy

**Good code review is:**
- **Fast:** <5 minutes for typical PR
- **Focused:** Critical issues first, nitpicks last
- **Constructive:** Suggest improvements, don't just criticize
- **Collaborative:** Discussion, not dictation

**Good code review is NOT:**
- Gatekeeping or showing off knowledge
- Rewriting in your preferred style
- Blocking on personal preferences
- Testing (that's CI's job)

**Remember:** You're reviewing to help ship better code, not perfect code.
