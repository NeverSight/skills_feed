---
name: code-review
description: "Load PROACTIVELY when task involves reviewing code, auditing quality, or validating implementations. Use when user says \"review this code\", \"check this PR\", \"audit the codebase\", or \"score this implementation\". Covers the 10-dimension weighted scoring rubric (correctness, security, performance, architecture, testing, error handling, type safety, maintainability, accessibility, documentation), automated pattern detection for anti-patterns, and structured review output with actionable findings."
metadata:
  version: 1.0.0
  category: quality
  tags: [review, quality, security, performance, testing, architecture, accessibility, scoring]
---

## Resources
```
scripts/
  validate-code-review.sh
references/
  review-patterns.md
```

# Code Review Quality Skill

This skill teaches you how to perform thorough, enterprise-grade code reviews using GoodVibes precision tools. A systematic code review catches issues early, ensures consistency, validates security and performance, and maintains high quality standards across the codebase.

## When to Use This Skill

Load this skill when:
- Reviewing pull requests or merge requests
- Performing code quality audits
- Validating security and performance of implementations
- Checking adherence to architectural patterns
- Assessing test coverage and quality
- Evaluating accessibility compliance
- Providing structured feedback to developers

Trigger phrases: "review this code", "check the PR", "quality audit", "security review", "performance review", "validate implementation".

## Core Workflow

### Phase 1: Discovery - Understand the Change

Before reviewing, understand what changed, why, and the scope of impact.

#### Step 1.1: Gather Change Context

Use `discover` to map all changed files and identify the type of change.

```yaml
discover:
  queries:
    - id: changed_files
      type: glob
      patterns: ["src/**/*"]  # List changed files for review
    - id: new_files
      type: glob
      patterns: ["**/*"]
    - id: test_files
      type: glob
      patterns: ["**/*.test.ts", "**/*.test.tsx", "**/*.spec.ts", "**/*.spec.tsx"]
  verbosity: files_only
```

**Extract from git:**

```yaml
precision_exec:
  commands:
    - cmd: "git diff --name-only HEAD~1..HEAD"
  verbosity: minimal
```

**What this reveals:**
- All files modified in the changeset
- New vs modified vs deleted files
- Test files included (or missing)
- Scope of change (frontend, backend, full-stack)

#### Step 1.2: Analyze Changed Code

Use `precision_read` to examine the actual changes.

```yaml
precision_read:
  files:
    - path: "src/api/user-routes.ts"  # Example changed file
      extract: content
    - path: "src/components/UserProfile.tsx"
      extract: content
  output:
    max_per_item: 200
  verbosity: standard
```

**Get diff context:**

```yaml
precision_exec:
  commands:
    - cmd: "git diff HEAD~1..HEAD -- src/api/user-routes.ts"
  verbosity: standard
```

#### Step 1.3: Find Related Code

Use `discover` to find imports, exports, and usage of changed symbols.

```yaml
discover:
  queries:
    - id: function_exports
      type: grep
      pattern: "export (function|const|class) (createUser|updateUser|deleteUser)"
      glob: "**/*.{ts,tsx,js,jsx}"
    - id: usage_sites
      type: grep
      pattern: "(createUser|updateUser|deleteUser)\\("
      glob: "**/*.{ts,tsx,js,jsx}"
    - id: related_tests
      type: grep
      pattern: "(createUser|updateUser|deleteUser)"
      glob: "**/*.test.{ts,tsx}"
  verbosity: locations
```

**What this reveals:**
- Where changed functions are used
- Potential breaking changes
- Test coverage for changed code
- Ripple effects across the codebase

### Phase 2: Security Review

Security issues are **critical** and must be caught in review.

#### Step 2.1: Check for Common Vulnerabilities

Use `discover` to find security anti-patterns.

```yaml
discover:
  queries:
    # SQL Injection
    - id: sql_injection
      type: grep
      pattern: '(query|execute|sql).*[`$].*\$\{'
      glob: "**/*.{ts,tsx,js,jsx}"
    # XSS vulnerabilities
    - id: dangerous_html
      type: grep
      pattern: "(dangerouslySetInnerHTML|innerHTML|outerHTML)"
      glob: "**/*.{ts,tsx,jsx}"
    # Hardcoded secrets
    - id: hardcoded_secrets
      type: grep
      pattern: '(password|secret|api[_-]?key|token)\s*=\s*["''][^"'']+["'']'
      glob: "**/*.{ts,tsx,js,jsx,json}"
    # Missing authentication
    - id: unauthed_routes
      type: grep
      pattern: "export (async )?function (GET|POST|PUT|DELETE|PATCH)"
      glob: "src/app/api/**/*.ts"
  verbosity: locations
```

**Critical patterns to check:**

| Pattern | Severity | Why It Matters |
|---------|----------|----------------|
| SQL injection | Critical | Allows attackers to read/modify database |
| XSS vulnerabilities | Critical | Allows script injection, session hijacking |
| Hardcoded secrets | Critical | Exposes credentials in source code |
| Missing auth checks | Critical | Exposes protected resources |
| Unsafe deserialization | Critical | Remote code execution |
| CORS misconfiguration | Major | Allows unauthorized origins |
| Weak password rules | Major | Account compromise |
| Missing input validation | Major | Data corruption, injection |

#### Step 2.2: Validate Input Handling

All external input must be validated.

```yaml
discover:
  queries:
    # Check for validation schemas
    - id: zod_schemas
      type: grep
      pattern: "z\\.(object|string|number|array|enum)"
      glob: "**/*.{ts,tsx}"
    # Check for direct request.json() without validation
    - id: unvalidated_input
      type: grep
      pattern: "(await request\\.json\\(\\)|req\\.body)(?!.*safeParse)"
      glob: "src/app/api/**/*.ts"
    # Check for SQL parameterization
    - id: parameterized_queries
      type: grep
      pattern: "(db\\.(query|execute)|prisma\\.|sql`)"
      glob: "**/*.{ts,js}"
  verbosity: locations
```

**Best practices to validate:**
- All API routes validate input with Zod, Joi, or equivalent
- All database queries use parameterized queries (Prisma, prepared statements)
- File uploads validate content type and size
- URLs and redirects are validated against allowlists

#### Step 2.3: Check Authentication & Authorization

Verify that protected resources require authentication.

```yaml
discover:
  queries:
    # Find auth middleware usage
    - id: auth_middleware
      type: grep
      pattern: "(getServerSession|auth\\(\\)|requireAuth|withAuth)"
      glob: "src/app/api/**/*.ts"
    # Find resource ownership checks
    - id: ownership_checks
      type: grep
      pattern: "(userId|authorId|ownerId)\s*===\s*(session|user|currentUser)"
      glob: "**/*.{ts,tsx}"
    # Find RBAC checks
    - id: rbac_checks
      type: grep
      pattern: "(role|permission|can)\s*===\s*"
      glob: "**/*.{ts,tsx}"
  verbosity: locations
```

**Critical checks:**
- [ ] Protected API routes call auth middleware
- [ ] User can only modify their own resources (ownership checks)
- [ ] Admin-only actions check for admin role
- [ ] JWTs are validated with proper secret
- [ ] Session tokens are rotated and have expiration

### Phase 3: Performance Review

Performance issues cause poor UX and cost scalability.

#### Step 3.1: Check for N+1 Queries

N+1 queries are the #1 database performance killer.

```yaml
discover:
  queries:
    # Find loops with database calls
    - id: n_plus_one
      type: grep
      pattern: "(for|forEach|map).*await.*(prisma|db|query|find)"
      glob: "**/*.{ts,tsx,js,jsx}"
    # Find Prisma include usage
    - id: prisma_includes
      type: grep
      pattern: "(findMany|findUnique|findFirst).*include:"
      glob: "**/*.{ts,js}"
  verbosity: locations
```

**How to fix:**
- Use `include` to eager load related records (Prisma)
- Use joins or `SELECT IN` for batch loading
- Implement DataLoader for GraphQL
- Cache frequently accessed data

#### Step 3.2: Check for Unnecessary Re-renders

React re-render issues harm frontend performance.

```yaml
discover:
  queries:
    # Find inline object/array creation in JSX
    - id: inline_objects
      type: grep
      pattern: "(onClick|onChange|style)=\\{\\{|=\\{\\["
      glob: "**/*.{tsx,jsx}"
    # Find missing useMemo/useCallback
    - id: missing_memoization
      type: grep
      pattern: "(map|filter|reduce)\\("
      glob: "**/*.{tsx,jsx}"
    # Find useEffect without dependencies
    - id: missing_deps
      type: grep
      pattern: "useEffect\\([^)]+\\)\\s*$"
      glob: "**/*.{tsx,jsx}"
  verbosity: locations
```

**Common issues:**

| Anti-pattern | Fix |
|-------------|-----|
| Inline object in props | Extract to constant or useMemo |
| Inline function in props | Wrap in useCallback |
| Large list without key | Add stable key prop |
| useEffect missing deps | Add all used variables to deps array |
| Context re-renders everything | Split context or use state managers |

#### Step 3.3: Check Database Indexes

Missing indexes cause slow queries.

```yaml
precision_read:
  files:
    - path: "prisma/schema.prisma"
      extract: content
  output:
    max_per_item: 500
  verbosity: standard
```

**Validate indexes exist for:**
- Foreign keys (userId, postId, etc.)
- Frequently filtered fields (status, createdAt, published)
- Fields used in WHERE clauses
- Compound indexes for multi-column queries

### Phase 4: Code Quality Review

Code quality affects maintainability and reliability.

#### Step 4.1: Check Type Safety

TypeScript should catch errors at compile time, not runtime.

```yaml
discover:
  queries:
    # Find any types
    - id: any_usage
      type: grep
      pattern: ":\s*any(\\s|;|,|\\))"
      glob: "**/*.{ts,tsx}"
    # Find type assertions (as)
    - id: type_assertions
      type: grep
      pattern: "as (unknown|any|string|number)"
      glob: "**/*.{ts,tsx}"
    # Find non-null assertions (!)
    - id: non_null_assertions
      type: grep
      pattern: "![.;,)\\]]"
      glob: "**/*.{ts,tsx}"
    # Find unsafe member access
    - id: unsafe_access
      type: grep
      pattern: "\\?\\."
      glob: "**/*.{ts,tsx}"
  verbosity: locations
```

**Type safety issues:**

| Issue | Severity | Fix |
|-------|----------|-----|
| `any` type usage | Major | Use proper types or unknown |
| `as any` assertions | Major | Fix the underlying type issue |
| `!` non-null assertion | Minor | Add null checks |
| Missing return types | Minor | Explicitly type function returns |
| Implicit any params | Major | Add parameter types |

#### Step 4.2: Check Error Handling

All async operations and API calls must handle errors.

```yaml
discover:
  queries:
    # Find floating promises
    - id: floating_promises
      type: grep
      pattern: "^\\s+[a-z][a-zA-Z]*\\(.*\\);$"
      glob: "**/*.{ts,tsx,js,jsx}"
    # Find empty catch blocks
    - id: empty_catch
      type: grep
      pattern: "catch.*\\{\\s*\\}"
      glob: "**/*.{ts,tsx,js,jsx}"
    # Find console.error (should use logger)
    - id: console_error
      type: grep
      pattern: "console\\.(error|warn|log)"
      glob: "**/*.{ts,tsx,js,jsx}"
  verbosity: locations
```

**Error handling checklist:**
- [ ] All promises have `.catch()` or `try/catch`
- [ ] Errors are logged with context (user ID, request ID)
- [ ] User-facing errors are sanitized (no stack traces)
- [ ] API errors return proper HTTP status codes
- [ ] Retry logic for transient failures

#### Step 4.3: Check Code Organization

Large files and high complexity make code hard to maintain.

```yaml
precision_exec:
  commands:
    - cmd: "find src -not -path '*/node_modules/*' -not -path '*/dist/*' -name '*.ts' -o -name '*.tsx' -print0 | xargs -0 wc -l | sort -rn | head -20"
  verbosity: standard
```

**Code organization rules:**
- Files should be < 300 lines (exception: generated code)
- Functions should be < 50 lines
- Cyclomatic complexity < 10
- Max nesting depth: 3 levels
- Extract helpers to separate files

### Phase 5: Testing Review

Tests validate correctness and prevent regressions.

#### Step 5.1: Check Test Coverage

Every changed file should have tests.

```yaml
discover:
  queries:
    # Find test files
    - id: test_files
      type: glob
      patterns: ["**/*.test.{ts,tsx}", "**/*.spec.{ts,tsx}"]
    # Find files without tests
    - id: source_files
      type: glob
      patterns: ["src/**/*.{ts,tsx}"]
    # Check test imports
    - id: test_imports
      type: grep
      pattern: "from ['\"].*/(api|lib|components)/"
      glob: "**/*.test.{ts,tsx}"
  verbosity: files_only
```

**Compare source files to test files:**

```javascript
// Pseudo-logic (implement with precision tools)
const sourceFiles = results.source_files.files;
const testFiles = results.test_files.files;
const missingTests = sourceFiles.filter(f => !testFiles.some(t => t.includes(f.replace('.ts', ''))));
```

#### Step 5.2: Check Test Quality

Tests should test behavior, not implementation.

```yaml
discover:
  queries:
    # Find skipped tests
    - id: skipped_tests
      type: grep
      pattern: "(it\\.skip|test\\.skip|describe\\.skip)"
      glob: "**/*.test.{ts,tsx}"
    # Find focused tests (.only)
    - id: focused_tests
      type: grep
      pattern: "(it\\.only|test\\.only|describe\\.only)"
      glob: "**/*.test.{ts,tsx}"
    # Find expect assertions
    - id: assertions
      type: grep
      pattern: "expect\\("
      glob: "**/*.test.{ts,tsx}"
    # Find mock usage
    - id: mocks
      type: grep
      pattern: "(vi\\.mock|jest\\.mock|vi\\.fn)"
      glob: "**/*.test.{ts,tsx}"
  verbosity: locations
```

**Test quality checklist:**
- [ ] No `.skip` or `.only` (should be removed before merge)
- [ ] Each test has at least one assertion
- [ ] Tests have descriptive names ("it should...", "when...then...")
- [ ] Tests are isolated (no shared state)
- [ ] Mocks are used sparingly (prefer real implementations)
- [ ] Edge cases are tested (null, empty, large values)

### Phase 6: Architecture Review

Architecture violations create technical debt.

#### Step 6.1: Check Dependency Direction

Dependencies should flow from outer layers to inner layers.

```yaml
discover:
  queries:
    # Find domain imports in UI
    - id: ui_imports_domain
      type: grep
      pattern: "from ['\"].*/(domain|core|lib)/"
      glob: "src/components/**/*.{ts,tsx}"
    # Find UI imports in domain
    - id: domain_imports_ui
      type: grep
      pattern: "from ['\"].*/(components|pages|app)/"
      glob: "src/domain/**/*.{ts,tsx}"
    # Find circular dependencies
    - id: imports
      type: grep
      pattern: "^import.*from"
      glob: "src/**/*.{ts,tsx}"
  verbosity: locations
```

**Dependency rules:**
- UI components can import hooks, utils, domain logic
- Domain logic should NOT import UI components
- API routes can import domain logic, not UI
- Shared utils should have zero dependencies

#### Step 6.2: Check for Layering Violations

```yaml
discover:
  queries:
    # Database access in components
    - id: db_in_components
      type: grep
      pattern: "(prisma|db\\.(query|execute))"
      glob: "src/components/**/*.{ts,tsx}"
    # Business logic in API routes
    - id: logic_in_routes
      type: grep
      pattern: "export (async )?function (GET|POST)"
      glob: "src/app/api/**/*.ts"
  verbosity: files_only
```

**Read the route handlers to check:**
- Route handlers should be < 30 lines (delegate to services)
- No database queries in components (use server actions or API routes)
- No business logic in routes (extract to service layer)

### Phase 7: Accessibility Review

Accessibility ensures your app is usable by everyone.

#### Step 7.1: Check Semantic HTML

Use proper HTML elements for accessibility.

```yaml
discover:
  queries:
    # Find div buttons (should be <button>)
    - id: div_buttons
      type: grep
      pattern: "<div.*(onClick|onKeyDown)"
      glob: "**/*.{tsx,jsx}"
    # Find missing alt text
    - id: missing_alt
      type: grep
      pattern: "<img(?![^>]*alt=)"
      glob: "**/*.{tsx,jsx}"
    # Find missing labels
    - id: missing_labels
      type: grep
      pattern: "<input(?![^>]*aria-label)(?![^>]*id=)"
      glob: "**/*.{tsx,jsx}"
    # Find missing ARIA roles
    - id: missing_roles
      type: grep
      pattern: "<(nav|header|footer|main)(?![^>]*role=)"
      glob: "**/*.{tsx,jsx}"
  verbosity: locations
```

**Accessibility checklist:**
- [ ] Buttons use `<button>`, not `<div onClick>`
- [ ] Images have descriptive `alt` text
- [ ] Form inputs have labels or `aria-label`
- [ ] Focus states are visible (no `outline: none` without replacement)
- [ ] Color contrast meets WCAG AA (4.5:1 for text)
- [ ] Keyboard navigation works (tab order, Enter/Space)

#### Step 7.2: Check ARIA Patterns

```yaml
discover:
  queries:
    # Find custom components
    - id: custom_components
      type: grep
      pattern: "(Accordion|Dialog|Dropdown|Tabs|Tooltip)"
      glob: "src/components/**/*.{tsx,jsx}"
  verbosity: files_only
```

**Read components to validate:**
- Modals trap focus and close on Escape
- Dropdowns support arrow keys
- Tabs support arrow keys and Home/End
- Tooltips are accessible (not just on hover)

### Phase 8: Review Scoring

Use the **review-scoring** skill to provide structured feedback.

See `plugins/goodvibes/skills/protocol/review-scoring/SKILL.md` for the full rubric.

**The 10 Dimensions (weighted):**

1. **Correctness** (15%) - Does it work? Does it meet requirements?
2. **Type Safety** (10%) - Proper TypeScript usage, no `any`
3. **Security** (15%) - No vulnerabilities, input validation, auth checks
4. **Performance** (10%) - No N+1 queries, proper indexes, memoization
5. **Error Handling** (10%) - All errors caught, logged, and handled
6. **Testing** (10%) - Adequate test coverage, quality assertions
7. **Code Quality** (10%) - Readable, maintainable, follows patterns
8. **Architecture** (10%) - Proper layering, no violations
9. **Accessibility** (5%) - Semantic HTML, ARIA, keyboard nav
10. **Documentation** (5%) - JSDoc, README, inline comments where needed

**Score each dimension 1-10:**
- 1-3: Needs major work
- 4-6: Needs improvement
- 7-8: Good, minor issues
- 9-10: Excellent

**Overall score = weighted average**

Pass/fail thresholds:
- **9.5+**: Excellent (approve immediately)
- **8.0-9.4**: Good (approve with minor suggestions)
- **7.0-7.9**: Acceptable (request changes - minor issues)
- **5.0-6.9**: Needs work (request changes - major issues)
- **< 5.0**: Reject (needs significant rework)

### Phase 9: Automated Validation

Run automated checks to catch issues.

```yaml
precision_exec:
  commands:
    # Type check
    - cmd: "npm run typecheck"
    # Lint
    - cmd: "npm run lint"
    # Tests
    - cmd: "npm run test"
    # Security audit
    - cmd: "npm audit --audit-level=moderate"
  verbosity: standard
```

**All checks must pass before approval.**

### Phase 10: Provide Feedback

Structured feedback is actionable and specific.

**Review output format:**

```markdown
## Review Summary

**Overall Score**: 8.2/10
**Verdict**: APPROVE with suggestions

**What changed**: Added user profile API with authentication
**Files reviewed**: 8 files (5 source, 3 test)

## Dimension Scores

1. Correctness: 9/10
2. Type Safety: 7/10
3. Security: 9/10
4. Performance: 8/10
5. Error Handling: 7/10
6. Testing: 8/10
7. Code Quality: 9/10
8. Architecture: 8/10
9. Accessibility: 8/10
10. Documentation: 7/10

## Issues Found

### Major (should fix)

- **FILE:LINE** - Type safety: Function `updateProfile` has implicit `any` return type
  - Fix: Add explicit return type `Promise<User>`
  - Impact: TypeScript can't catch type errors in callers

### Minor (nice to fix)

- **src/api/profile.ts:42** - Error handling: Empty catch block swallows errors
  - Fix: Log error with context before re-throwing
  - Impact: Makes debugging harder

## What Was Done Well

- Excellent input validation with Zod schemas
- Comprehensive test coverage (95%)
- Proper authentication checks on all routes
- Clean separation of concerns (route -> service -> repository)
```

**Feedback guidelines:**

- Be specific: Include file path and line number
- Be actionable: Explain exactly how to fix
- Explain impact: Why does this matter?
- Acknowledge good work: Highlight what was done well
- Categorize by severity: Critical > Major > Minor

## Common Review Patterns

See `references/review-patterns.md` for detailed anti-patterns organized by category.

**Quick reference:**

### Security Patterns

- SQL injection: String concatenation in queries
- XSS: Unsafe HTML rendering
- Auth bypass: Missing auth checks
- Secrets exposure: Hardcoded API keys

### Performance Patterns

- N+1 queries: Loops with database calls
- Missing indexes: WHERE clauses without indexes
- Unnecessary re-renders: Inline objects in React
- Memory leaks: Event listeners not cleaned up

### Code Quality Patterns

- Type unsafety: `any` types, type assertions
- Error handling: Floating promises, empty catches
- Complexity: Functions > 50 lines, nesting > 3
- Duplication: Copy-paste code

### Testing Patterns

- Missing tests: Changed files without tests
- Poor assertions: `expect(result).toBeTruthy()`
- Test pollution: Shared state between tests
- Skipped tests: `.skip` or `.only` left in

## Precision Tools for Review

### Discover Tool

Run multiple grep/glob queries in parallel to find patterns.

**Example: Find security issues**

```yaml
discover:
  queries:
    - id: sql_injection
      type: grep
      pattern: 'query.*\$\{'
    - id: hardcoded_secrets
      type: grep
      pattern: 'api[_-]?key\s*=\s*["''][^"'']+'
    - id: xss
      type: grep
      pattern: 'dangerouslySetInnerHTML'
  verbosity: locations
```

### Precision Grep

Search with context, multiline support, and token limits.

**Example: Find error handling**

```yaml
precision_grep:
  queries:
    - id: catch_blocks
      pattern: "try\\s*\\{[\\s\\S]*?\\}\\s*catch"
  output:
    format: context
    context_after: 3
    context_before: 1
  verbosity: standard
```

### Precision Exec

Run validation commands.

```yaml
precision_exec:
  commands:
    - cmd: "npm run typecheck"
    - cmd: "npm run lint"
    - cmd: "npm test -- --coverage"
  verbosity: standard
```

## Validation Script

Use `scripts/validate-code-review.sh` to validate review completeness.

```bash
./scripts/validate-code-review.sh /path/to/review-output.md
```

**The script checks:**
- Security patterns were checked
- Performance patterns were checked
- Test coverage was reviewed
- All changed files were reviewed
- Review includes scoring with rubric
- Feedback is specific with file/line references

## Quick Reference

### Review Checklist

**Before reviewing:**
- [ ] Understand the change (read PR description, commits)
- [ ] Get the diff (`git diff` or GitHub PR)
- [ ] Identify changed files and their purpose

**During review:**
- [ ] Security: Check for vulnerabilities, auth, validation
- [ ] Performance: Check for N+1, indexes, re-renders
- [ ] Type safety: Check for `any`, assertions, return types
- [ ] Error handling: Check for floating promises, empty catches
- [ ] Testing: Check coverage, quality, skipped tests
- [ ] Architecture: Check layering, dependencies, organization
- [ ] Accessibility: Check semantic HTML, ARIA, keyboard nav

**After review:**
- [ ] Run automated validation (typecheck, lint, test)
- [ ] Score all 10 dimensions
- [ ] Calculate weighted score
- [ ] Provide verdict (approve/request changes/reject)
- [ ] Write actionable feedback with file/line references

### Severity Guidelines

**Critical (must fix before merge):**
- Security vulnerabilities (SQL injection, XSS, auth bypass)
- Data loss bugs
- Compilation/runtime errors
- Breaking changes to public API

**Major (should fix before merge):**
- Type safety issues (`any` usage, missing types)
- Performance issues (N+1 queries, missing indexes)
- Missing error handling
- Missing tests for critical paths
- Architecture violations

**Minor (nice to fix, or address in follow-up):**
- Code style inconsistencies
- Missing documentation
- Non-critical accessibility issues
- Refactoring opportunities
- Low test coverage on edge cases

### Common Mistakes to Avoid

**Score inflation:**
- Don't give 9-10 scores when issues exist
- Be honest about quality gaps
- Critical issues should fail review

**Vague feedback:**
- BAD: "Fix the types"
- GOOD: "src/api/user.ts:42 - Add return type `Promise<User>` to function `getUser`"

**Ignoring positives:**
- Always acknowledge what was done well
- Positive feedback motivates improvement

**Inconsistent severity:**
- Security issues are always Critical
- Missing tests are Major, not Minor
- Style issues are Minor, not Major

## Advanced Techniques

### Batch Review with Discover

Review multiple PRs or files in parallel.

```yaml
discover:
  queries:
    - id: all_changes
      type: grep
      pattern: ".*"
      path: "src/"
  verbosity: files_only
```

Then read files in batch:

```yaml
precision_read:
  files:
    - path: "src/changed-file-1.ts"
    - path: "src/changed-file-2.ts"
  extract: content
  output:
    max_per_item: 100
  verbosity: standard
```

### Contextual Review

Use `precision_grep` with context to understand surrounding code.

```yaml
precision_grep:
  queries:
    - id: auth_checks
      pattern: "getServerSession|auth\\(\\)"
  output:
    format: context
    context_before: 5
    context_after: 10
  verbosity: standard
```

### Differential Review

Focus on changed lines only.

```yaml
precision_exec:
  commands:
    - cmd: "git diff HEAD~1..HEAD --unified=5"
  verbosity: standard
```

Parse the diff and review only changed sections.

### Automated Pattern Detection

Create a batch of security/performance checks.

```yaml
discover:
  queries:
    # Security
    - { id: sql_injection, type: grep, pattern: 'query.*\$\{' }
    - { id: xss, type: grep, pattern: 'dangerouslySetInnerHTML' }
    - { id: secrets, type: grep, pattern: 'password\s*=\s*["''][^"'']+' }
    # Performance
    - { id: n_plus_one, type: grep, pattern: 'for.*await.*prisma' }
    - { id: inline_objects, type: grep, pattern: 'onClick=\{\{', glob: '**/*.tsx' }
    # Quality
    - { id: any_usage, type: grep, pattern: ':\s*any', glob: '**/*.ts' }
    - { id: empty_catch, type: grep, pattern: 'catch.*\{\s*\}' }
  verbosity: locations
```

**Aggregate results and score based on findings.**

## Integration with Other Skills

- Use **review-scoring** for structured feedback with the 10-dimension rubric
- Use **error-recovery** when fix attempts fail during review remediation
- Use **precision-mastery** for advanced precision tool usage
- Use **testing-strategy** to validate test quality
- Use **component-architecture** when reviewing UI components
- Use **api-design** when reviewing API routes
- Use **database-layer** when reviewing database queries and schemas

## Resources

- `references/review-patterns.md` - Common anti-patterns by category
- `scripts/validate-code-review.sh` - Automated review validation
- `plugins/goodvibes/skills/protocol/review-scoring/SKILL.md` - Scoring rubric details
- OWASP Top 10 - https://owasp.org/www-project-top-ten/
- WCAG Guidelines - https://www.w3.org/WAI/WCAG21/quickref/
