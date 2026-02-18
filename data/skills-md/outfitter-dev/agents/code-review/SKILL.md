---
name: code-review
description: This skill should be used when reviewing code before commit, conducting quality gates, or when "review", "fresh eyes", "pre-commit review", or "quality gate" are mentioned.
metadata:
  version: "1.0.0"
---

# Fresh Eyes Review

Systematic pre-commit quality gate → checklist-based review → findings → summary.

<when_to_use>

- Pre-commit code review and quality gates
- Pre-merge pull request reviews
- Systematic code audits before deployment
- Quality verification for critical changes
- Second-opinion review requests

NOT for: quick sanity checks, trivial typo fixes, formatting-only changes

</when_to_use>

<announcement_protocol>

## Starting Review

**Review Scope:** { files/areas under review }
**Focus Areas:** { specific concerns or general quality gate }
**Checklist:** { full or targeted categories }

## During Review

Emit findings as discovered:
- **{SEVERITY}** `{FILE_PATH}:{LINE}` — { issue description }
- **Impact:** { consequences if shipped }
- **Fix:** { concrete remediation }

## Completing Review

**Review Complete**

**Findings Summary:**
- ◆◆ Severe: {COUNT} — blocking issues
- ◆ Moderate: {COUNT} — should fix before merge
- ◇ Minor: {COUNT} — consider addressing

**Recommendation:** { ship / fix blockers / needs rework }

{ detailed findings below if any found }

</announcement_protocol>

<checklist>

## Type Safety

- ✓ No `any` types without justification comment
- ✓ Null/undefined handled explicitly (optional chaining, nullish coalescing)
- ✓ Type guards used for union types
- ✓ Discriminated unions for state machines
- ✓ Generic constraints specified where needed
- ✓ Return types explicit on public functions
- ✓ No type assertions without safety comment

## Error Handling

- ✓ All error paths handled (no silent failures)
- ✓ Meaningful error messages with context
- ✓ Errors propagated or logged appropriately
- ✓ Result types used for expected failures
- ✓ Try/catch blocks have specific error handling
- ✓ Promise rejections handled
- ✓ Resource cleanup in finally blocks

## Security

- ✓ User input validated before use
- ✓ No hardcoded secrets or credentials
- ✓ Authentication/authorization checks present
- ✓ Parameterized queries (no SQL injection)
- ✓ XSS prevention (sanitized output)
- ✓ CSRF protection where applicable
- ✓ Sensitive data encrypted/hashed
- ✓ Rate limiting on public endpoints

## Testing

- ✓ Tests exist for new functionality
- ✓ Edge cases covered
- ✓ Error scenarios tested
- ✓ Actual assertions (not just execution)
- ✓ No test pollution (proper setup/teardown)
- ✓ Mocks used appropriately (not overused)
- ✓ Test names describe behavior
- ✓ Integration tests for critical paths

## Code Quality

- ✓ Names reveal intent (functions, variables, types)
- ✓ Functions <50 lines (single responsibility)
- ✓ Files <500 lines (consider splitting)
- ✓ No magic numbers (use named constants)
- ✓ DRY violations eliminated
- ✓ Nested conditionals <3 deep
- ✓ Cyclomatic complexity reasonable
- ✓ Dead code removed

## Documentation

- ✓ Public APIs have JSDoc/TSDoc
- ✓ Complex algorithms explained
- ✓ Non-obvious decisions documented
- ✓ Breaking changes noted
- ✓ TODOs have context and owner
- ✓ README updated if behavior changes
- ✓ Examples provided for complex usage

## Performance

- ✓ No obvious N+1 queries
- ✓ Appropriate data structures used
- ✓ Unnecessary allocations avoided
- ✓ Heavy operations async/batched
- ✓ Caching where beneficial
- ✓ Database indexes considered

## Rust-Specific (when applicable)

- ✓ `rustfmt` and `clippy` passing
- ✓ `Result` preferred over panic
- ✓ No `unwrap`/`expect` outside tests/startup
- ✓ Ownership/borrowing idiomatic
- ✓ `Send`/`Sync` bounds respected
- ✓ Unsafe code justified with comments
- ✓ Proper error types (`thiserror`/`anyhow`)

</checklist>

<stages>

## 1. Announce (activeForm: Announcing review)

Emit starting protocol:
- Scope of review
- Focus areas
- Checklist approach (full or targeted)

## 2. Checklist (activeForm: Running checklist review)

Systematically verify each category:
- Type Safety → Error Handling → Security → Testing → Quality → Docs → Performance
- Flag violations immediately with severity
- Note clean areas briefly

## 3. Deep Dive (activeForm: Investigating findings)

For each finding:
- Verify it's actually a problem (not false positive)
- Assess severity and impact
- Determine concrete fix
- Check for pattern across codebase

## 4. Summarize (activeForm: Compiling review summary)

Emit completion protocol:
- Findings count by severity
- Recommendation (ship / fix blockers / rework)
- Detailed findings list
- Optional: patterns noticed, suggestions for future

Load the **maintain-tasks** skill for tracking review stages.

</stages>

<finding_format>

**{SEVERITY}** `{FILE_PATH}:{LINE_RANGE}`

**Issue:** { clear description of problem }

**Impact:** { consequences if shipped — security risk, runtime error, maintenance burden, etc }

**Fix:** { concrete steps to remediate }

**Pattern:** { if issue appears multiple times, note scope }

---

Example:

**◆◆** `src/auth/login.ts:45-52`

**Issue:** Password compared using `==` instead of constant-time comparison

**Impact:** Timing attack vulnerability — attacker can infer password length and content through response timing

**Fix:** Use `crypto.timingSafeEqual()` or bcrypt's built-in comparison

**Pattern:** Single occurrence

---

</finding_format>

<severity_guidance>

**◆◆ Severe (blocking):**
- Security vulnerabilities
- Data loss risks
- Runtime crashes in common paths
- Breaking changes without migration
- Test failures or missing critical tests

**◆ Moderate (should fix):**
- Type safety violations
- Unhandled error cases
- Poor error messages
- Missing tests for edge cases
- Significant code quality issues
- Missing documentation for public APIs

**◇ Minor (consider addressing):**
- Code style inconsistencies
- Overly complex but functional code
- Minor performance optimizations
- Documentation improvements
- TODOs without context
- Naming improvements

</severity_guidance>

<workflow>

Loop: Scan → Verify → Document → Next category

1. **Announce review** — scope, focus, approach
2. **Run checklist** — systematically verify each category
3. **Document findings** — severity, location, issue, impact, fix
4. **Investigate patterns** — does finding repeat? Broader issue?
5. **Deep dive blockers** — verify severity assessment, ensure fix is clear
6. **Compile summary** — counts by severity, recommendation
7. **Deliver findings** — completion protocol with detailed list

At each finding:
- Verify it's actually a problem
- Assess impact if shipped
- Determine concrete fix
- Note if pattern across files

</workflow>

<validation>

Before completing review:

**Check coverage:**
- ✓ All checklist categories verified?
- ✓ Both happy path and error paths reviewed?
- ✓ Tests examined for actual assertions?
- ✓ Security-sensitive areas given extra scrutiny?

**Check findings quality:**
- ✓ Severity accurately assessed?
- ✓ Impact clearly explained?
- ✓ Fix actionable and concrete?
- ✓ False positives eliminated?

**Check recommendation:**
- ✓ Aligned with findings severity?
- ✓ Blockers clearly marked?
- ✓ Path forward unambiguous?

</validation>

<rules>

ALWAYS:
- Announce review start with scope and focus
- Run systematic checklist, don't skip categories
- Emit findings as discovered, don't batch at end
- Assess severity honestly (err toward caution)
- Provide concrete fixes, not just complaints
- Complete with summary and recommendation
- Mark false positives if checklist item doesn't apply
- Consider patterns (single issue or systemic?)

NEVER:
- Skip checklist review for "quick check"
- Assume code is safe without verification
- Flag style preferences as blockers
- Provide vague findings without fix guidance
- Approve severe findings "for later fix"
- Complete review without announcement protocol
- Miss security checks on user input paths
- Ignore test quality (execution != validation)

</rules>

<references>

Core methodology:
- [checklist.md](references/checklist.md) — extended checklist details, examples, severity guidance

Related skills:
- codebase-recon — evidence-based investigation (foundation for review)
- debugging — structured bug investigation

</references>
