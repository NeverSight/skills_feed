---
name: code-review
description: Perform automated code reviews checking for security vulnerabilities, performance issues, and code quality. Use before creating PRs or when reviewing complex changes.
allowed-tools: Read, Grep, Glob, Bash
---

# Code Review Skill

This skill helps you perform thorough code reviews for quality, security, and performance.

## When to Use This Skill

- Before creating pull requests
- Reviewing complex changes
- Checking for security vulnerabilities
- Identifying performance issues
- Ensuring code quality standards
- Mentoring junior developers

## Code Review Checklist

### 1. Functionality

- [ ] Code does what it's supposed to do
- [ ] Edge cases are handled
- [ ] Error handling is appropriate
- [ ] No obvious bugs
- [ ] Logic is correct and efficient

### 2. Code Quality

- [ ] Code is readable and maintainable
- [ ] Functions are small and focused
- [ ] Variable names are descriptive
- [ ] No code duplication
- [ ] Follows DRY principle
- [ ] Comments explain "why", not "what"

### 3. Type Safety

- [ ] No use of `any` (or justified with comment)
- [ ] Proper TypeScript types
- [ ] No type assertions without reason
- [ ] Interfaces/types are well-defined
- [ ] Generics used appropriately

### 4. Testing

- [ ] New code has tests
- [ ] Tests cover edge cases
- [ ] Tests are meaningful
- [ ] No flaky tests
- [ ] Test names are descriptive

### 5. Performance

- [ ] No unnecessary re-renders (React)
- [ ] Database queries are optimized
- [ ] No N+1 query problems
- [ ] Caching used appropriately
- [ ] Bundle size impact considered

### 6. Security

- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] Input validation present
- [ ] Authentication/authorization checked
- [ ] Secrets not committed
- [ ] CORS configured properly

## Common Issues to Look For

### Anti-Patterns

**❌ Magic Numbers**
```typescript
// Bad
if (user.age > 18) {
  allowAccess();
}

// Good
const LEGAL_AGE = 18;
if (user.age >= LEGAL_AGE) {
  allowAccess();
}
```

**❌ Deep Nesting**
```typescript
// Bad
if (user) {
  if (user.isActive) {
    if (user.hasPermission) {
      if (resource.isAvailable) {
        // do something
      }
    }
  }
}

// Good
if (!user || !user.isActive || !user.hasPermission || !resource.isAvailable) {
  return;
}
// do something
```

**❌ Large Functions**
```typescript
// Bad
function processUser() {
  // 200 lines of code
}

// Good
function processUser() {
  validateUser();
  enrichUserData();
  saveUser();
  notifyUser();
}
```

**❌ Using `any`**
```typescript
// Bad
function processData(data: any) {
  return data.value;
}

// Good
interface Data {
  value: string;
}

function processData(data: Data) {
  return data.value;
}
```

### Security Issues

**❌ SQL Injection**
```typescript
// Bad
const query = `SELECT * FROM users WHERE id = ${userId}`;

// Good
const query = db.query.users.findFirst({
  where: eq(users.id, userId),
});
```

**❌ XSS Vulnerability**
```typescript
// Bad
element.innerHTML = userInput;

// Good
element.textContent = userInput;
// Or use framework's safe rendering
<div>{userInput}</div>
```

**❌ Exposed Secrets**
```typescript
// Bad
const apiKey = "sk_live_12345...";

// Good
const apiKey = process.env.API_KEY;
```

**❌ Missing Input Validation**
```typescript
// Bad
export async function updateUser(data: any) {
  await db.update(users).set(data);
}

// Good
const updateUserSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
});

export async function updateUser(data: unknown) {
  const validated = updateUserSchema.parse(data);
  await db.update(users).set(validated);
}
```

### Performance Issues

**❌ N+1 Queries**
```typescript
// Bad
const posts = await db.query.posts.findMany();
for (const post of posts) {
  const author = await db.query.users.findFirst({
    where: eq(users.id, post.authorId),
  });
  post.author = author;
}

// Good
const posts = await db.query.posts.findMany({
  with: {
    author: true,
  },
});
```

**❌ Missing Memoization**
```typescript
// Bad
function Component({ data }) {
  const processedData = expensiveOperation(data);
  return <div>{processedData}</div>;
}

// Good
function Component({ data }) {
  const processedData = useMemo(() => expensiveOperation(data), [data]);
  return <div>{processedData}</div>;
}
```

**❌ Unnecessary Re-renders**
```typescript
// Bad
function Parent() {
  return <Child onClick={() => handleClick()} />;
}

// Good
function Parent() {
  const handleClick = useCallback(() => {
    // handle click
  }, []);

  return <Child onClick={handleClick} />;
}
```

## Review Process

### 1. Understand the Change

```bash
# View the diff
git diff main...feature-branch

# See changed files
git diff --name-only main...feature-branch

# See commit history
git log main..feature-branch --oneline
```

### 2. Check Code Quality

```bash
# Run linter
pnpm biome check .

# Run type checker
pnpm tsc --noEmit

# Run tests
pnpm test
```

### 3. Check for Common Issues

```bash
# Search for 'any' usage
grep -r "any" apps/ packages/ --include="*.ts" --include="*.tsx"

# Search for console.log
grep -r "console.log" apps/ packages/ --include="*.ts" --include="*.tsx"

# Search for TODO comments
grep -r "TODO" apps/ packages/ --include="*.ts" --include="*.tsx"

# Search for hardcoded credentials
grep -r "password\|secret\|key" apps/ packages/ --include="*.ts"
```

### 4. Review Database Changes

```bash
# Check migration files
ls -la packages/database/migrations/

# Review migration SQL
cat packages/database/migrations/latest.sql
```

### 5. Check Dependencies

```bash
# Check for new dependencies
git diff package.json

# Check for security vulnerabilities
pnpm audit

# Check for outdated packages
pnpm outdated
```

## Automated Review Tools

### TypeScript Compiler

```bash
# Check types across workspace
pnpm tsc --noEmit

# Check specific package
pnpm -F @sgcarstrends/web tsc --noEmit
```

### Biome Linter

```bash
# Lint all files
pnpm biome check .

# Lint with details
pnpm biome check . --verbose

# Check specific files
pnpm biome check apps/web/src/**/*.ts
```

### Tests

```bash
# Run all tests
pnpm test

# Run with coverage
pnpm test:coverage

# Check coverage threshold
pnpm test -- --coverage --coverageThreshold='{"global":{"branches":80,"functions":80,"lines":80}}'
```

## Review Comments

### Constructive Feedback

**❌ Poor Comment**
```
This is wrong.
```

**✅ Good Comment**
```
Consider using `useMemo` here to avoid recalculating on every render.
This could impact performance with large datasets.
```

**❌ Poor Comment**
```
Don't use any.
```

**✅ Good Comment**
```
The `any` type bypasses type safety. Consider defining a proper interface:

interface UserData {
  id: string;
  name: string;
  email: string;
}
```

### Comment Categories

**🔴 Must Fix** - Critical issues that block merge
```
🔴 This creates an SQL injection vulnerability. Use parameterized queries.
```

**🟡 Should Fix** - Important but not blocking
```
🟡 This function is doing too much. Consider breaking it into smaller functions.
```

**🟢 Suggestion** - Nice to have improvements
```
🟢 You could simplify this with optional chaining: `user?.profile?.name`
```

**💡 Learning** - Educational comments
```
💡 FYI: Next.js automatically optimizes images when using the Image component.
```

**❓ Question** - Asking for clarification
```
❓ Is there a reason we're not using the existing `formatDate` utility?
```

## Review Patterns by Language/Framework

### TypeScript/JavaScript

Check for:
- Proper typing (no `any`)
- Async/await usage
- Error handling
- Modern syntax (optional chaining, nullish coalescing)

```typescript
// Look for improvements
const value = data && data.user && data.user.name;  // ❌
const value = data?.user?.name;  // ✅

const value = data || 'default';  // ❌ (0, '', false are falsy)
const value = data ?? 'default';  // ✅ (only null/undefined)
```

### React

Check for:
- Proper hooks usage
- Memoization where needed
- Key props in lists
- useEffect dependencies

```typescript
// Check useEffect dependencies
useEffect(() => {
  fetchData(userId);  // ❌ Missing dependency
}, []);

useEffect(() => {
  fetchData(userId);  // ✅ Correct dependencies
}, [userId]);
```

### Next.js

Check for:
- Server vs client components
- Proper use of async components
- Metadata exports
- Image optimization

```typescript
// ❌ Missing 'use client'
import { useState } from 'react';

export default function Component() {
  const [state, setState] = useState();
  // ...
}

// ✅ Correct
'use client';
import { useState } from 'react';

export default function Component() {
  const [state, setState] = useState();
  // ...
}
```

### Database (Drizzle)

Check for:
- Proper indexing
- N+1 queries
- Transaction usage
- Migration safety

```typescript
// ❌ N+1 query
const users = await db.query.users.findMany();
for (const user of users) {
  user.posts = await db.query.posts.findMany({
    where: eq(posts.userId, user.id),
  });
}

// ✅ Single query with join
const users = await db.query.users.findMany({
  with: {
    posts: true,
  },
});
```

## Pull Request Review

### Before Approving

- [ ] All tests pass
- [ ] No linting errors
- [ ] Type checks pass
- [ ] No security vulnerabilities
- [ ] Performance is acceptable
- [ ] Documentation updated if needed
- [ ] Breaking changes documented
- [ ] Commit messages follow convention

### Review Tiers

**Level 1: Quick Review** (< 100 lines)
- Run automated checks
- Scan for obvious issues
- Check tests exist

**Level 2: Standard Review** (100-500 lines)
- Detailed code review
- Test coverage check
- Performance consideration
- Security check

**Level 3: Thorough Review** (> 500 lines)
- Architecture review
- Multiple reviewers
- Performance testing
- Security audit
- Documentation review

## Self-Review Checklist

Before requesting review:

```bash
# 1. Check your changes
git diff main...HEAD

# 2. Run quality checks
pnpm biome check --write .
pnpm tsc --noEmit
pnpm test

# 3. Check for common issues
grep -r "console.log" . --include="*.ts" --include="*.tsx"
grep -r "TODO" . --include="*.ts" --include="*.tsx"

# 4. Review your commits
git log main..HEAD --oneline

# 5. Check PR size
git diff --stat main...HEAD
```

## Code Review Metrics

Track these metrics:

- **Review time**: Time from PR creation to approval
- **Iterations**: Number of review rounds
- **Comments**: Number of review comments
- **Defects found**: Bugs caught in review
- **Coverage delta**: Test coverage change

## References

- TypeScript Best Practices: https://typescript-eslint.io/rules/
- React Best Practices: https://react.dev/learn
- Security: OWASP Top 10
- Related files:
  - Root CLAUDE.md - Code style guidelines
  - `biome.json` - Linting rules

## Best Practices

1. **Be Constructive**: Focus on improvement, not criticism
2. **Explain Why**: Don't just say "wrong", explain the issue
3. **Suggest Solutions**: Provide alternatives when possible
4. **Prioritize**: Mark critical issues vs suggestions
5. **Be Timely**: Review PRs promptly
6. **Ask Questions**: Seek to understand before judging
7. **Praise Good Code**: Acknowledge well-written code
8. **Stay Professional**: Keep feedback objective and respectful
