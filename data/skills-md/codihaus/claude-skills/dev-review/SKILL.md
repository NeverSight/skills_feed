---
name: dev-review
description: Code review with focus on quality, security, and best practices
version: 1.4.1
---

# /dev-review - Code Review

> **Skill Awareness**: See `skills/_registry.md` for all available skills.
> - **Before**: After `/dev-coding` implementation and `/dev-test` passes
> - **Reads**: `_quality-attributes.md` (ALL Levels - verification)
> - **If issues**: Fix with `/dev-coding`, then review again
> - **If major changes**: Create CR via `/debrief`

Review code changes for quality, security, and adherence to standards.

## When to Use

- After implementing a feature
- Before merging a PR
- To get feedback on approach
- To catch issues before production

## Usage

```
/dev-review                      # Review uncommitted changes
/dev-review --staged             # Review staged changes only
/dev-review src/auth/            # Review specific directory
/dev-review UC-AUTH-001          # Review changes for specific UC
```

## Input

Reviews can be based on:
1. **Git diff** - Uncommitted or staged changes
2. **File list** - Specific files to review
3. **UC reference** - Files changed for a use case (from spec)

## Output

```markdown
## Review Summary

**Verdict**: ✅ Approve | ⚠️ Request Changes | ❓ Needs Discussion

**Stats**: X files, Y additions, Z deletions

### Issues Found

#### 🔴 Critical (must fix)
- [security] SQL injection risk in `src/api/users.ts:45`
- [bug] Null pointer in `src/utils/parse.ts:23`

#### 🟡 Important (should fix)
- [performance] N+1 query in `src/api/posts.ts:67`
- [error-handling] Unhandled promise rejection

#### 🔵 Suggestions (nice to have)
- [style] Consider extracting to helper function
- [naming] `data` is too generic, suggest `userProfile`

### By File
- `src/api/auth.ts` - 2 issues
- `src/components/Form.tsx` - 1 suggestion

### Positives
- Good error handling in login flow
- Clean separation of concerns
```

## Expected Outcome

Review report with verdict and categorized issues.

**Report includes:**
- Verdict (Approve/Request Changes/Needs Discussion)
- Issues found (by severity: critical/important/suggestion)
- Issues by file
- Positives (acknowledge good work)
- Spec compliance (if UC provided)

## Review Workflow

**1. Load Context (once):**
- Read `plans/brd/tech-context.md` → Identify stack(s)
- Load `knowledge/stacks/{stack}/_index.md` → Focus on "For /dev-review" section
- Read `_quality-attributes.md` → Get all level checklists
- Read spec (if UC provided) → Get requirements
- Get git diff or file list → Understand what changed

**2. Analyze Changes:**
- Review each changed file
- Apply: Security + Quality + Conventions + Stack-Specific checks
- Note issues by severity (critical/important/suggestion)
- Acknowledge good practices

**3. Verify Spec Compliance (if UC provided):**
- Check all requirements met
- Identify missing items
- Flag unauthorized additions

**4. Generate Report:**
- Verdict (Approve/Request Changes/Needs Discussion)
- Issues by severity
- Issues by file
- Spec compliance status
- Positives

**5. Offer Fix (if issues found):**
- Critical/Important → Suggest auto-fix via `/dev-coding`
- Suggestions → User decides

## Success Criteria

- Stack knowledge loaded and applied
- Security risks identified
- Quality issues found
- Spec compliance verified
- Conventions checked
- Framework patterns verified (from stack knowledge)
- Constructive feedback with suggested fixes
- Clear verdict given

## Review Focus Areas

### Security
- Input validation (sanitized, injection prevented, XSS prevented)
- Authentication (required where needed, tokens validated, sessions secure)
- Authorization (permissions checked, data access restricted, admin protected)
- Data protection (passwords hashed, sensitive data not logged, no secrets in code)
- API security (rate limiting, CORS, no sensitive data in URLs)

### Quality
- Error handling (caught, user-friendly messages, logged, not swallowed)
- Performance (no N+1 queries, pagination on lists, async heavy ops, no memory leaks)
- Maintainability (readable, functions not too long, no magic values, DRY)
- Testing (new code tested, edge cases covered, meaningful tests)

### Conventions
- Naming (variables, files, components per scout)
- Structure (correct location, follows patterns, organized imports)
- Style (matches configs, consistent, no linting errors)
- Git (proper commit format, no unrelated changes, no debug code)

### Spec Compliance
- Requirements met (all implemented)
- Requirements not met (missing items)
- Not in spec (unauthorized additions)

### Stack-Specific

**CRITICAL: Load framework-specific review checklists**

After loading stack knowledge (from Context Sources → Step 1), apply framework-specific checks from the "For /dev-review" section:

**React projects:**
- Hooks follow Rules of Hooks (no conditional calls, correct order)
- All dependencies included in useEffect/useCallback/useMemo
- No infinite loops, no stale closures
- State updates are immutable
- Performance optimizations appropriate (memo, lazy)
- Lists have stable keys

**Vue 3 projects:**
- Uses `<script setup>` (not Options API)
- Composables follow naming convention (use*)
- No destructuring reactive without toRefs
- ref() accessed with .value in script (not in template)
- v-for has unique :key
- No v-for + v-if on same element
- Props not mutated directly

**Next.js projects:**
- Server vs Client Components used correctly
- Server Actions have "use server" directive
- Data fetching uses proper Next.js patterns
- No client-side code in Server Components

**Nuxt projects:**
- Composables follow naming convention (useX)
- Server routes in correct location
- Auto-imports used correctly
- SSR-safe code (no window access in setup)

**Directus projects:**
- Collections accessed properly
- Permissions configured
- Field types match requirements
- Flows and hooks follow patterns

**If stack knowledge file doesn't exist**, apply general best practices only.

## Context Sources

**Read to understand what was changed:**
- git diff (uncommitted or staged)
- Specific files (if provided)

**Read to understand standards:**

**Step 1: Load stack knowledge (CRITICAL)**
- Read `plans/brd/tech-context.md` → Identify stack(s)
- Extract stack names (look for "Primary Stack" or "Tech Stack" section)
- Load corresponding knowledge files:
  - If "React" → Read `knowledge/stacks/react/_index.md` → Focus on "For /dev-review" section
  - If "Vue" → Read `knowledge/stacks/vue/_index.md` → Focus on "For /dev-review" section
  - If "Next.js" → Read `knowledge/stacks/nextjs/_index.md` → Focus on "For /dev-review" section
  - If "Nuxt" → Read `knowledge/stacks/nuxt/_index.md` → Focus on "For /dev-review" section
  - If "Directus" → Read `knowledge/stacks/directus/_index.md` → Focus on "For /dev-review" section

**Step 2: Load project and spec context**
- `tech-context.md` - Project conventions
- `architecture.md` - Architecture decisions (if exists)
- `spec` - Requirements (if UC provided)
- `_quality-attributes.md` - ALL levels (Architecture, Specification, Implementation, Review)
- Config files (`.eslintrc`, `tsconfig.json`, etc.)

## Severity Levels

| Level | Icon | Meaning | Action |
|-------|------|---------|--------|
| Critical | 🔴 | Security risk, bug, breaks functionality | Must fix before merge |
| Important | 🟡 | Performance, maintainability issues | Should fix |
| Suggestion | 🔵 | Style, improvements | Nice to have |
| Positive | ✅ | Good practice noted | Encouragement |

## Verdicts

| Verdict | When |
|---------|------|
| ✅ Approve | No critical/important issues |
| ⚠️ Request Changes | Has critical or multiple important issues |
| ❓ Needs Discussion | Unclear requirements, architectural concerns |

## Review Best Practices

### Be Constructive

```markdown
// BAD
"This code is bad"

// GOOD
"This could cause a SQL injection. Consider using parameterized queries:
```sql
SELECT * FROM users WHERE id = $1
```"
```

### Explain Why

```markdown
// BAD
"Don't use var"

// GOOD
"Use const/let instead of var - var has function scope which can lead to
unexpected behavior. const also signals intent that the value won't change."
```

### Suggest Alternatives

```markdown
// Issue + Solution
"The N+1 query here will cause performance issues with many posts.

Consider using an include/join:
```typescript
const posts = await db.posts.findMany({
  include: { author: true }
});
```"
```

### Acknowledge Good Work

```markdown
### Positives
- Clean separation of API and business logic
- Good error messages for users
- Comprehensive input validation
```

## Tools Used

| Tool | Purpose |
|------|---------|
| `Bash` | git diff, git log |
| `Read` | Read changed files |
| `Grep` | Search for patterns |
| `Glob` | Find related files |

## Integration

| Skill | Relationship |
|-------|--------------|
| `/dev-coding` | Review after implementation |
| `/dev-scout` | Get project conventions |
| `/dev-specs` | Check spec compliance |

## Example Review

```
User: /dev-review UC-AUTH-001

Step 1: Load Context
- Read tech-context.md → Stack: Next.js 14 + TypeScript
- Read knowledge/stacks/nextjs/_index.md → "For /dev-review" section
  → Check Server Actions, App Router, Server Components
- Read knowledge/stacks/react/_index.md → "For /dev-review" section
  → Check Hooks, state management, performance
- Read _quality-attributes.md → All level checklists
- Read UC-AUTH-001 spec → Requirements
- Get git diff → Changed files

Step 2: Analyze
- src/api/auth/login.ts: Clean ✓
- src/components/LoginForm.tsx: 1 issue (React hooks deps missing)
- src/lib/api.ts: 1 suggestion (naming)

Step 3: Generate Report

## Review Summary

**Verdict**: ⚠️ Request Changes

**Stats**: 3 files, +245 additions, -12 deletions

### Issues Found

#### 🔴 Critical
None

#### 🟡 Important
- [error-handling] `src/components/LoginForm.tsx:34`
  Promise rejection not handled. If API fails, user sees nothing.
  ```tsx
  // Add error state
  .catch(err => setError(err.message))
  ```

#### 🔵 Suggestions
- [naming] `src/lib/api.ts:12`
  `data` is generic. Consider `credentials` for clarity.

### Spec Compliance
- [x] POST /api/auth/login works
- [x] Returns token
- [x] Validates input
- [ ] Missing: Rate limiting (spec requirement)

### Positives
- Good validation on both client and server
- Clean component structure
- Proper TypeScript types
```

## Fix Loop

When issues are found, `/dev-review` can trigger `/dev-coding` to fix them:

```
/dev-review
    ↓
Issues found?
├── No → Pass ✅ → Suggest /dev-changelog
└── Yes → Offer to fix
        ↓
    "1 important issue found. Fix now?"
    ├── Yes → Load /dev-coding with fix context
    │         ↓
    │         Fix applied
    │         ↓
    │         Re-run /dev-review (auto)
    └── No → Output review, user fixes manually
```

### Fix Flow

```markdown
**Review found issues:**

| # | Severity | File | Issue |
|---|----------|------|-------|
| 1 | 🟡 Important | LoginForm.tsx:34 | Promise rejection not handled |
| 2 | 🔵 Suggestion | api.ts:12 | Generic variable name |

**Options:**
- A: Fix important issues automatically (1 issue)
- B: Fix all issues automatically (2 issues)
- C: I'll fix manually
```

**If user chooses A or B:**

```
1. Load /dev-coding skill
   → Pass: files to fix, issues to address

2. /dev-coding applies fixes
   → Uses existing patterns from scout
   → Follows spec requirements

3. Auto re-run /dev-review
   → Verify fixes applied correctly
   → Check for new issues introduced

4. If pass → Suggest /dev-changelog
```

## After Pass: Changelog

When review passes (no critical/important issues):

```markdown
## Review Complete ✅

**Verdict**: Approved

No critical or important issues found.

**Next Steps:**
1. Run `/dev-changelog` to document what was built
2. Commit and push changes
3. Create PR

💡 Run `/dev-changelog {feature}` to create implementation summary.
```

## Integration

| Skill | Relationship |
|-------|--------------|
| `/dev-coding` | Review after implementation |
| `/dev-coding` | Call to fix issues (fix loop) |
| `/dev-scout` | Get project conventions |
| `/dev-specs` | Check spec compliance |
| `/dev-changelog` | Document after pass |

## Complete Flow

```
/dev-coding → /dev-test → /dev-review
                              │
                    ┌─────────┴─────────┐
                    │   Issues found?   │
                    └─────────┬─────────┘
                              │
              ┌───────────────┼───────────────┐
              ↓               ↓               ↓
         Critical        Important        None
              │               │               │
              ↓               ↓               ↓
         Must fix        Offer fix       Pass ✅
              │               │               │
              └───────┬───────┘               │
                      ↓                       │
              /dev-coding (fix)               │
                      ↓                       │
              /dev-review (re-run)            │
                      ↓                       │
                    Pass ────────────────────→│
                                              ↓
                                    /dev-changelog
                                              ↓
                                    summary.md created
```
