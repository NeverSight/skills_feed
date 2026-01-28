---
name: commit-assistant
description: Provides conventional commits guidance and auto-generates commit messages from git changes. Integrates with /ccpm:commit for automated git commits linked to Linear issues. Auto-activates when users ask about committing, creating git commits, or discussing commit message formats.
allowed-tools: [Bash, Task]
---

# Commit Assistant

Comprehensive guidance on conventional commits with automatic message generation integrated with CCPM's Linear workflow. Ensures all commits are properly formatted, issue-linked, and semantically meaningful.

## When to Use

This skill auto-activates when:

- User asks **"commit my changes"**, **"create a git commit"**, **"how do I commit"**
- User asks about **"conventional commits"** or **"commit message format"**
- Running **`/ccpm:commit`** command
- Making changes that need to be committed to version control
- Need guidance on **commit type** or **commit message structure**
- Need help **generating commit messages** from code changes

## Core Principles

### 1. Conventional Commits Format

All commits in CCPM follow [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
type(scope): message

[optional body]

[optional footer]
```

**Format breakdown**:
- **type**: What kind of change (feat, fix, docs, refactor, test, chore, perf, style)
- **scope**: What component or module changed (optional but recommended)
- **message**: Clear, concise description in imperative mood
- **body**: Detailed explanation (only for complex changes)
- **footer**: Issue references, breaking changes (optional)

### 2. Why Conventional Commits Matter

**Conventional commits enable**:
- ✅ Automatic changelog generation
- ✅ Semantic versioning (SemVer) automation
- ✅ Better git history readability
- ✅ Linear issue linking
- ✅ Filtered log searches (`git log --grep="^feat"`)
- ✅ CI/CD pipeline triggers (e.g., deploy on "feat:" commits)

### 3. Imperative Mood

Always write commit messages in **imperative mood** (command form):

**✅ Correct**:
- "add user authentication"
- "fix database connection timeout"
- "refactor auth module for clarity"
- "update API documentation"

**❌ Incorrect**:
- "added user authentication"
- "fixed database connection timeout"
- "refactoring auth module"
- "updates API documentation"

**Why**: Imperative mood matches git's own commit messages and convention specifications.

## Commit Types Explained

### `feat:` - New Features

**Use when**: Adding new functionality to the codebase.

**Examples**:
- `feat(auth): add JWT token refresh endpoint`
- `feat(api): implement rate limiting middleware`
- `feat(ui): add dark mode toggle`

**When NOT to use**: Bug fixes should use `fix:`, not `feat:`

### `fix:` - Bug Fixes

**Use when**: Fixing a bug or defect in existing functionality.

**Examples**:
- `fix(auth): prevent expired tokens from accessing protected routes`
- `fix(api): handle null values in user query results`
- `fix(ui): correct button alignment on mobile devices`

**When NOT to use**: Adding new features should use `feat:`, not `fix:`

### `docs:` - Documentation Changes

**Use when**: Writing or updating documentation, comments, README, or API docs.

**Examples**:
- `docs(readme): add installation instructions`
- `docs(api): document rate limiting headers`
- `docs: add troubleshooting guide`

**Impact**: Does NOT trigger version bumps (not a "feature" or "fix")

### `refactor:` - Code Refactoring

**Use when**: Restructuring code without changing functionality (performance, readability, maintainability).

**Examples**:
- `refactor(auth): extract JWT validation to separate module`
- `refactor(api): simplify error handling logic`
- `refactor: rename misleading variable names`

**Impact**: Does NOT trigger version bumps (internal improvement only)

### `test:` - Test Additions/Changes

**Use when**: Adding, updating, or fixing tests (no production code changes).

**Examples**:
- `test(auth): add tests for JWT expiration`
- `test(api): improve test coverage for rate limiter`
- `test: fix flaky database integration test`

**Impact**: Does NOT trigger version bumps

### `chore:` - Build/Tooling Changes

**Use when**: Updating dependencies, build config, CI/CD, or development tools.

**Examples**:
- `chore(deps): upgrade Node.js to v20.11`
- `chore(build): update webpack configuration`
- `chore(ci): configure GitHub Actions for linting`

**Impact**: Does NOT trigger version bumps

### `perf:` - Performance Improvements

**Use when**: Code optimization that improves performance metrics.

**Examples**:
- `perf(api): cache database queries for 5 minutes`
- `perf(ui): optimize image rendering for 40% faster load time`
- `perf: reduce bundle size by 15%`

**Impact**: Triggers patch version bump (like `fix:`)

### `style:` - Code Style Changes

**Use when**: Formatting, whitespace, or code style changes (no logic changes).

**Examples**:
- `style: reformat code according to ESLint rules`
- `style(css): remove unused CSS classes`
- `style: add missing semicolons`

**Impact**: Does NOT trigger version bumps

## Auto-Generation with `/ccpm:commit`

The `/ccpm:commit` command provides intelligent commit message auto-generation.

### Usage

**Basic usage**:
```bash
/ccpm:commit                    # Auto-detect issue, generate message
/ccpm:commit AUTH-123           # Link specific issue
/ccpm:commit AUTH-123 "Fix login validation"  # Explicit message
```

### How Auto-Detection Works

1. **Detects current git branch** for Linear issue ID
   - Example: `feat/AUTH-123-jwt-auth` → extracts `AUTH-123`
   - Example: `fix/WORK-456-cache-bug` → extracts `WORK-456`

2. **Analyzes git changes** to determine commit type
   - Tests added/modified → `test:`
   - Documentation only → `docs:`
   - Bug fix + test → `fix:`
   - New feature + test → `feat:`

3. **Extracts scope** from changed files
   - Files: `src/auth/jwt.ts`, `src/auth/login.ts` → scope: `auth`
   - Files: `src/api/users.ts`, `src/api/posts.ts` → scope: `api`

4. **Generates message** from:
   - Linear issue title
   - Git diff summary
   - Changed function/class names
   - Test names if tests added

5. **Links to Linear** automatically
   - Adds issue ID to footer
   - Updates Linear with commit link
   - Creates audit trail

### Example Auto-Generation Flow

**Scenario**: Branch `fix/AUTH-123-jwt-expiration`, changed `src/auth/jwt.ts`

```bash
$ /ccpm:commit

Analyzing changes for commit...

Branch: fix/AUTH-123-jwt-expiration
Issue: AUTH-123
Linear Title: "Prevent expired tokens from accessing API"

Changes detected:
- src/auth/jwt.ts: Modified token validation logic
- test/auth/jwt.test.ts: Added 2 tests for expiration

Commit type: fix (bug fix with tests)
Scope: auth
Message: "prevent expired tokens from accessing API"

Generated commit:
```
fix(auth): prevent expired tokens from accessing API

- Added token expiration check in validateToken()
- Added tests for expired token rejection
- Updated middleware to handle token validation errors

Closes AUTH-123
```

Proceed with commit? (yes/no)
```

## Best Practices

### 1. Keep Messages Concise

**First line** should be:
- Under 72 characters
- Complete thought
- Clear, specific (not vague like "fix bug" or "update code")

**✅ Good**: `fix(auth): validate JWT expiration before token use`
**❌ Bad**: `fix: bug` or `fix: updates`

### 2. Use the Scope

Always include scope when possible (what changed):

**✅ Good**: `feat(api):`, `fix(ui):`, `docs(readme):`
**❌ Bad**: `feat: new stuff`, `fix: problem`

### 3. Reference Issues in Footer

Link to Linear issues in commit footer:

```
fix(auth): prevent expired tokens

[body explaining the fix]

Closes AUTH-123
Refs AUTH-120
```

**Common footers**:
- `Closes ISSUE-123` - Closes the issue
- `Fixes ISSUE-123` - Fixes the issue
- `Refs ISSUE-123` - Just references
- `BREAKING CHANGE: ...` - Documents breaking changes

### 4. Add Body for Complex Changes

For significant changes, add explanation:

```
feat(auth): implement OAuth2 authentication flow

- Added OAuth2 provider integration
- Implemented token refresh mechanism
- Added session persistence to Redis
- Updated user model with OAuth fields

This enables third-party sign-in for better UX.
Addresses AUTH-127 requirements.

Closes AUTH-127
```

### 5. Group Related Changes

If multiple related files change, use single commit:

```bash
git add src/auth/jwt.ts test/auth/jwt.test.ts
git commit -m "fix(auth): validate JWT expiration"
```

Not:

```bash
git add src/auth/jwt.ts
git commit -m "fix(auth): validate JWT expiration"
git add test/auth/jwt.test.ts
git commit -m "test(auth): add JWT expiration tests"
```

## Commit Message Examples

### Example 1: Simple Feature

**Scenario**: Added new user registration endpoint

```
feat(api): add user registration endpoint

- POST /auth/register creates new user accounts
- Validates email format and password strength
- Returns JWT token on successful registration

Closes AUTH-101
```

**Analysis**:
- ✅ Type: `feat:` (new feature)
- ✅ Scope: `api` (API endpoint changed)
- ✅ Message: Imperative mood, under 72 chars
- ✅ Body: Clear explanation
- ✅ Issue link: References LINEAR issue

### Example 2: Bug Fix

**Scenario**: Fixed database timeout issue

```
fix(db): handle connection timeouts gracefully

- Added 30-second connection timeout
- Retry logic with exponential backoff
- Return 503 Service Unavailable to clients
- Log timeout events for monitoring

Fixes DB-456
Refs AUTH-123
```

**Analysis**:
- ✅ Type: `fix:` (bug fix)
- ✅ Scope: `db` (database layer)
- ✅ Message: Clear problem & solution
- ✅ Body: Technical details
- ✅ Issue links: Primary issue + related

### Example 3: Refactoring

**Scenario**: Extracted authentication logic into module

```
refactor(auth): extract validation logic to utility module

- Move JWT validation to src/auth/validators.ts
- Extract middleware factory to src/auth/middleware.ts
- Improve code reusability and testability
- No functional changes
```

**Analysis**:
- ✅ Type: `refactor:` (internal improvement)
- ✅ Scope: `auth` (authentication module)
- ✅ Message: Clear intent (extract, not add)
- ✅ Body: What was extracted + benefit
- ✅ No issue link: Not user-facing change

### Example 4: Documentation Update

**Scenario**: Added API authentication guide

```
docs(api): add authentication implementation guide

- New section: JWT token flow diagrams
- New section: Token refresh strategy
- Code examples for common authentication patterns
- Links to security best practices
```

**Analysis**:
- ✅ Type: `docs:` (documentation)
- ✅ Scope: `api` (API documentation)
- ✅ Message: Clear what was added
- ✅ Body: Section breakdown
- ✅ No issue link: Documentation improvement

### Example 5: Performance Optimization

**Scenario**: Added caching to reduce database queries

```
perf(api): implement request caching for 40% query reduction

- Cache GET requests for 5 minutes (TTL)
- Invalidate cache on POST/PUT/DELETE
- Add Redis cache layer
- Reduces database load by 40% in benchmarks

Closes PERF-234
```

**Analysis**:
- ✅ Type: `perf:` (performance improvement)
- ✅ Scope: `api` (API layer)
- ✅ Message: Clear improvement + metric (40%)
- ✅ Body: Implementation details
- ✅ Metrics: Quantifiable improvement shown

### Example 6: Multi-File Feature

**Scenario**: Implemented complete authentication system

```
feat(auth): implement JWT authentication system

- Add JWT token generation and validation
- Add login endpoint with credential verification
- Add logout endpoint with token blacklisting
- Add protected route middleware
- Add 90 tests covering all scenarios

This enables secure user authentication and session management.
Replaces legacy session-based auth system.

Closes AUTH-105
Closes AUTH-106
Closes AUTH-107
```

**Analysis**:
- ✅ Type: `feat:` (new feature)
- ✅ Scope: `auth` (authentication)
- ✅ Message: High-level overview
- ✅ Body: All components included
- ✅ Multiple issues: References all related tasks
- ✅ Impact statement: Explains change scope

## Integration with `/ccpm:commit`

### Command Syntax

```bash
/ccpm:commit [issue-id] [message]
```

**Examples**:

```bash
# Auto-detect everything from current branch
/ccpm:commit

# Specify issue, auto-generate message
/ccpm:commit AUTH-123

# Specify issue and message
/ccpm:commit AUTH-123 "Fix login validation error"

# Just provide message (detects issue from branch)
/ccpm:commit "Refactor authentication module"
```

### What the Command Does

1. **Analyzes** current git changes
2. **Detects** commit type from changes
3. **Extracts** scope from modified files
4. **Generates** commit message (if not provided)
5. **Links** to Linear issue
6. **Creates** the commit
7. **Updates** Linear with commit link
8. **Suggests** next action (verification, sync, etc.)

### Workflow Example

```bash
# 1. Make changes
$ vim src/auth/jwt.ts

# 2. Stage changes
$ git add src/auth/jwt.ts test/auth/jwt.test.ts

# 3. Create conventional commit linked to Linear
$ /ccpm:commit

Analyzing changes...
Branch: fix/AUTH-123-jwt-expiration
Files: src/auth/jwt.ts, test/auth/jwt.test.ts
Type: fix
Scope: auth

Generated commit:
  fix(auth): prevent expired tokens from accessing API

Proceed? (yes/no)

# 4. Commit created automatically
$ git log -1 --oneline
a1b2c3d fix(auth): prevent expired tokens from accessing API

# 5. Linear updated
AUTH-123 comment added: "Commit: a1b2c3d"
```

## Common Mistakes to Avoid

### Mistake 1: Wrong Commit Type

**❌ Mistake**: Using `feat:` for a bug fix
```bash
feat(auth): fix JWT validation
```

**✅ Correct**: Use `fix:` for bug fixes
```bash
fix(auth): validate JWT expiration
```

**Why**: Different types trigger different version bumps. A bug fix should not bump minor version.

### Mistake 2: Vague Messages

**❌ Mistake**: Generic, unclear message
```bash
fix: update auth
chore: fixes
feat: improvements
```

**✅ Correct**: Specific, action-oriented messages
```bash
fix(auth): validate JWT expiration before token use
chore(deps): upgrade Node.js to v20.11
feat(api): add user registration endpoint
```

### Mistake 3: Avoiding Issue Links

**❌ Mistake**: No issue reference
```bash
fix(auth): prevent expired tokens
```

**✅ Correct**: Link to Linear issue
```bash
fix(auth): prevent expired tokens

Closes AUTH-123
```

**Why**: Creates audit trail and helps team understand why change was made.

### Mistake 4: Past Tense in Message

**❌ Mistake**: Past tense (non-imperative)
```bash
fixed JWT validation
added user registration
refactored auth module
```

**✅ Correct**: Imperative mood
```bash
fix JWT validation
add user registration
refactor auth module
```

### Mistake 5: Too Much Detail in Subject Line

**❌ Mistake**: Long, detailed first line
```bash
feat(auth): add comprehensive JWT authentication system with token refresh
 and improved security checks including rate limiting and IP whitelisting
```

**✅ Correct**: Concise subject (under 72 chars), details in body
```bash
feat(auth): add JWT authentication system

- Add token generation and validation
- Add logout with token blacklisting
- Add protected route middleware
- Add rate limiting and IP checks
```

## Integration with CCPM Workflow

### In Planning Phase

When planning a task with `/ccpm:plan`:

```markdown
Task: "Implement JWT authentication"

Implementation plan:
- [ ] Create auth module
- [ ] Add login endpoint
- [ ] Add protected route middleware
- [ ] Add comprehensive tests

Commits expected:
1. `feat(auth): create JWT authentication module`
2. `feat(api): add login endpoint`
3. `feat(api): add protected route middleware`
4. `test(auth): add JWT validation tests`
```

### During Implementation

When making changes during `/ccpm:work`:

```bash
# 1. Work on feature
$ vim src/auth/jwt.ts

# 2. Run tests
$ npm test

# 3. Create conventional commit
$ /ccpm:commit

# 4. Sync progress
$ /ccpm:sync "Implemented JWT validation"

# 5. Repeat for each logical change
```

### Before Verification

When verifying with `/ccpm:verify`:

**Commit history should show**:
```
a1b2c3d feat(auth): prevent expired tokens from accessing API
b2c3d4e feat(api): add login endpoint
c3d4e5f test(auth): add JWT validation tests
```

**Each commit** should:
- ✅ Be conventional format
- ✅ Be linked to Linear issue
- ✅ Have clear, specific message
- ✅ Include related tests

### Before Completion

When finalizing with `/ccpm:done`:

**Check commit history**:
```bash
git log --oneline --grep="ISSUE-123"
```

**Should show**:
- ✅ Multiple logical commits (not one giant commit)
- ✅ Clear progression from task start to completion
- ✅ All conventional commits format
- ✅ All linked to issue

## Activation Triggers

This skill activates when you:

- Ask **"How do I commit changes?"**
- Ask **"Create a git commit"** or **"commit my changes"**
- Ask **"What's a conventional commit?"**
- Ask **"What should my commit message be?"**
- Ask **"How do I write commit messages?"**
- Ask about **"commit message format"** or **"commit types"**
- Run **`/ccpm:commit`** command
- Run **`/ccpm:done`** (which includes commit step)
- Need help **generating** or **formatting** commit messages

## Integration with Other CCPM Skills

**Works alongside**:

- **pm-workflow-guide**: Suggests committing at right workflow stages
- **external-system-safety**: If commits trigger external updates (GitHub Actions, CD/CI)
- **ccpm-code-review**: Verifies commits follow quality standards
- **docs-seeker**: For commit message examples and best practices

**Example combined workflow**:

```
User: "I finished the JWT feature"
       ↓
/ccpm:sync → Update Linear with progress
       ↓
/ccpm:commit → Create conventional commit
       ↓
commit-assistant → Auto-generate message, link to issue
       ↓
/ccpm:verify → Run quality checks on changed code
       ↓
/ccpm:done → Create PR, sync external systems
```

## Summary

This skill ensures:

- ✅ All commits follow conventional commit format
- ✅ Commit messages are clear and specific
- ✅ Issues are properly linked in commits
- ✅ Commit history is searchable and meaningful
- ✅ Automatic changelog generation possible
- ✅ Semantic versioning automation enabled
- ✅ Git history is clean and maintainable

**Philosophy**: Clear commits enable clear history, which enables automation and team communication.

---

**Based on**: [Conventional Commits 1.0.0](https://www.conventionalcommits.org/)
**License**: MIT
**CCPM Integration**: `/ccpm:commit`, `/ccpm:sync`, `/ccpm:done`
