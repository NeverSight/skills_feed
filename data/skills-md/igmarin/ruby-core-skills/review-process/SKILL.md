---
name: review-process
license: MIT
description: >
  Reviews PRs using structured findings with severity levels (Critical/Major/Minor/Nitpick),
  verifies changeset includes tests for new/modified logic, reviews for correctness + safety +
  security + domain language adherence, checks for scope creep and authorization gaps (missing
  checks are Critical), presents structured table of findings by severity, generates
  self-review checklists for authors, produces findings reports, determines re-review criteria
  — and performs re-review verification by reviewing the diff against each finding.
  Use when the user requests a code review, asks to review a pull request, or needs a structured
  code audit with severity-classified findings. Trigger words: code review, review PR, PR review,
  code audit, structured review, severity levels.
metadata:
  version: 1.0.0
  user-invocable: "true"
  type: "process-discipline"
---
# Review Process

Standardized code review process for Ruby code changesets.

## Quick Reference

| Severity | Definition | Target Action |
|----------|--------------|---------------|
| **Critical** | Security issue, data corruption risk, crash/unhandled exception | Must resolve; blocks merge |
| **Major** | Logical flaw, structural issue, design smell, missing tests | High priority to fix before merge |
| **Minor** | Inefficient query, duplicate code, suboptimal naming, missing YARD | Optional/nice-to-have in this changeset |
| **Nitpick** | Formatting, style guides, purely cosmetic | Acknowledge; do not block merge |

## HARD-GATE

```text
REVIEW GATES:
1. Every review must classify findings using the standard severity levels (Critical, Major, Minor, Nitpick).
2. Any Critical finding automatically blocks the review; a re-review is MANDATORY once addressed. DO NOT merge changesets with unresolved Critical issues.
3. The reviewer must verify that the changeset includes tests for any new or modified logic.
```

## Process Steps

### Step 1: Context Gathering
- Confirm the stated business intent matches what the code actually does — flag divergence as a Major finding.
- Check scope creep: flag files changed that are unrelated to the PR's stated purpose.
- Identify entry points (controllers, jobs, rake tasks) to trace the full call path through the changeset.

### Step 2: Self-Review Checklists (For Authors)
- [ ] Tests cover happy paths, boundaries, and error states
- [ ] YARD docs on new/modified public interfaces
- [ ] No hardcoded secrets or environment config
- [ ] Syntax checks and linters pass

### Step 3: Analysis (For Reviewers)
Apply these domain-specific checks beyond generic correctness:
- **Authorisation:** Verify every action checks policy/permission — missing checks are Critical.
- **N+1 queries:** Flag `.each` loops that call associations without eager-loading as Major.
- **Error handling:** Confirm service objects rescue and return structured error responses rather than raising through to the controller.
- **Domain language:** Confirm new method/class names align with the established ubiquitous language (e.g., `Order`, `Invoice`, `Subscription` — not generic terms like `Record` or `Item`).
- **Test coverage gate:** Any new public method or branch without a corresponding spec is at minimum a Major finding.

### Step 4: Write Findings
For each issue identified, format it as a structured finding:
- **Location:** File path and line numbers
- **Severity:** Critical / Major / Minor / Nitpick
- **Description:** What is the technical issue and why is it risky?
- **Suggestion:** Concrete code block or action to fix it.

---

## Checkpoint Pattern

Align with the author or reviewer:
1. **Review Findings Report:** Present the structured table of findings categorized by severity.
2. **Re-Review Verification:** Once fixes are made, review the diff specifically addressing the findings and state the new status.

---

## Structured Finding Examples

### Critical

**Location:** `lib/orders/creator.rb:L15-L25`
**Severity:** Critical
**Description:** Unhandled `ProductNotFoundError` when ordering a product that doesn't exist. This will cause a 500 error in the application controller layer.
**Suggestion:**
```ruby
def call
  # ...
rescue ProductNotFoundError => e
  logger.error("Failed to create order: #{e.message}")
  { success: false, response: { error: { message: "Product not found" } } }
end
```

### Minor

**Location:** `app/models/subscription.rb:L10-L12`
**Severity:** Minor
**Description:** Public method `#days_remaining` lacks a YARD doc comment, making it invisible to documentation generators and harder for new contributors to understand intent.
**Suggestion:**
```ruby
# @return [Integer] number of days until the subscription expires
def days_remaining
  (expires_at.to_date - Date.today).to_i
end
```

---

## Integration

| Context | Next Skill |
|---------|----------|
| Addressing review findings | **respond-to-review** |
| Adding missing tests | **tdd-process** |
| Cleaning up identified smells | **refactor-process** |
