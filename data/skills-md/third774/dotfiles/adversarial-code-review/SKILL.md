---
name: adversarial-code-review
description: Review code through hostile perspectives to find bugs, security issues, and unintended consequences the author missed. Use when reviewing PRs, auditing codebases, or before critical deployments.
---

# Adversarial Code Review

**Core Principle:** Review as if you're trying to break the code. Deliberately adopt hostile perspectives—each reveals issues the others miss.

This is not about finding fault. It's about finding problems before users do.

## Review Mode

| Mode                       | Trigger                                | Focus                              |
| -------------------------- | -------------------------------------- | ---------------------------------- |
| **Diff-Focused** (default) | No explicit instruction, PR review     | What changed? What could break?    |
| **Audit**                  | "audit", "holistic", "codebase review" | Broader scope, systematic coverage |

When in doubt, use diff-focused mode. Audit mode requires explicit request.

## The Six Adversarial Lenses

Review through each lens deliberately. Don't blend them—switching perspectives forces deeper analysis.

| Lens                    | Core Question                         | Reveals                                                        |
| ----------------------- | ------------------------------------- | -------------------------------------------------------------- |
| **Malicious User**      | "How would I exploit this?"           | Input validation gaps, injection vectors, privilege escalation |
| **Careless Colleague**  | "How would this break if used wrong?" | API misuse, unclear contracts, error handling gaps             |
| **Future Maintainer**   | "What will confuse me in 6 months?"   | Implicit assumptions, missing context, temporal coupling       |
| **Ops/On-Call**         | "How will this fail at 3am?"          | Observability gaps, recovery paths, failure modes              |
| **Data Integrity**      | "What happens to state?"              | Race conditions, partial failures, consistency violations      |
| **Interaction Effects** | "What does this change elsewhere?"    | Unintended side effects, behavioral changes, contract breaks   |

### Lens Details

#### Malicious User

Assume the user is actively trying to break or exploit the system.

- What inputs are trusted that shouldn't be?
- Can I escalate privileges or access unauthorized data?
- What happens if I send malformed/oversized/unexpected input?
- Are there injection points (SQL, XSS, command, path traversal)?

For deep security reviews, see `references/security-lens-detail.md`.

#### Careless Colleague

Assume another developer will use this code without reading documentation.

- Is the API intuitive or are there "gotchas"?
- What happens if methods are called in wrong order?
- Are error messages helpful or cryptic?
- Could someone misuse this and get silent wrong results?

#### Future Maintainer

Assume you'll revisit this code in 6 months with no memory of writing it.

- Why does this code exist? Is that documented?
- What assumptions are implicit that should be explicit?
- Are there magic numbers/strings without explanation?
- Would I understand the control flow on first read?

#### Ops/On-Call

Assume this will fail in production at the worst possible time.

- How will I know when this fails? (Logging, metrics, alerts)
- Can I diagnose the problem from logs alone?
- Is there a recovery path? Can it be retried safely?
- What's the blast radius if this fails?

#### Data Integrity

Assume multiple things will try to modify state simultaneously.

- What happens if this runs twice concurrently?
- Are there partial failure states that leave data inconsistent?
- Is there a transaction boundary? What if it fails mid-way?
- Are reads and writes properly synchronized?

#### Interaction Effects

Assume this change has consequences beyond its immediate scope.

- What calls this? Will their expectations still hold?
- What does this call? What assumptions are we making?
- Does this subtly change behavior callers depend on?
- Are there caches, indexes, or derived data that need updating?

## Review Workflow

Copy this checklist when starting a review:

```
Adversarial Review Progress:
- [ ] Step 1: Determine mode (diff-focused or audit)
- [ ] Step 2: Understand the change/code purpose
- [ ] Step 3: Apply lenses (prioritize by risk, ~5 min each):
  - [ ] Malicious User
  - [ ] Careless Colleague
  - [ ] Future Maintainer
  - [ ] Ops/On-Call Engineer
  - [ ] Data Integrity
  - [ ] Interaction Effects
- [ ] Step 4: Filter findings through Impact Filter
- [ ] Step 5: Classify severity (Must Fix / Should Fix / Consider)
- [ ] Step 6: Limit "Consider" items to max 2
- [ ] Step 7: Identify at least one positive
- [ ] Step 8: Format report
```

### Lens Prioritization

Not all lenses are equally important for all code. Prioritize:

| Code Type            | Priority Lenses                         |
| -------------------- | --------------------------------------- |
| User input handling  | Malicious User, Data Integrity          |
| API/public interface | Careless Colleague, Interaction Effects |
| Background jobs      | Ops/On-Call, Data Integrity             |
| Business logic       | Future Maintainer, Interaction Effects  |
| Database operations  | Data Integrity, Ops/On-Call             |

## The Five Iron Laws

<IMPORTANT>
1. **No findings without specific location AND impact**
   - Bad: "This could have race conditions"
   - Good: "Line 45: concurrent access to `cache` without lock could cause data corruption when requests overlap"

2. **Severity matches actual risk, not theoretical worst-case**
   - Bad: "CRITICAL: This string could theoretically be used for XSS" (in internal CLI)
   - Good: "LOW: Unescaped string—not currently risky but add escaping if this reaches browser"

3. **Every "Must Fix" requires demonstration or clear reasoning**
   - Don't just assert the bug exists—show WHY it's a bug

4. **Alternative suggestions are optional, not mandated**
   - Present options. Don't dictate implementation details.

5. **Acknowledge at least one thing done well**
   - Adversarial doesn't mean hostile. Recognition builds trust.
     </IMPORTANT>

## Impact Filter

Every potential finding must pass this filter. Score 2+ to report:

```
□ Likely to occur (probability)
□ Impactful if it occurs (severity)
□ Non-obvious to the author (added value)
```

If a finding scores 0-1, don't report it. You're adding noise, not value.

## Severity Tiers

| Tier           | Definition                                      | Action                         | Examples                                                       |
| -------------- | ----------------------------------------------- | ------------------------------ | -------------------------------------------------------------- |
| **Must Fix**   | Breaks correctness, security, or data integrity | Block merge                    | SQL injection, race condition causing data loss, auth bypass   |
| **Should Fix** | Likely problems but not immediately broken      | Fix before or soon after merge | Missing error handling, unclear naming, no tests for edge case |
| **Consider**   | Style, optimization, theoretical concerns       | **Max 2 per review**           | Could be more idiomatic, minor perf optimization               |

### The "Consider" Trap

Limit "Consider" comments to 2 maximum. More than that:

- Dilutes important feedback
- Feels like nitpicking
- Reduces trust in your reviews

If you have many "Consider" items, pick the 2 most valuable and drop the rest.

## What NOT to Flag

- **Style preferences covered by linter/formatter** — Automation handles this
- **Alternative implementations of equal merit** — "I would have done X" isn't a bug
- **Hypothetical futures** — "What if we need to support Y someday..." isn't actionable
- **Things you'd do differently but aren't wrong** — Preferences aren't defects

**The Test:** "Would a reasonable senior engineer disagree with me here?"

If yes → Probably not worth commenting.

## Reporting Format

Structure findings clearly:

```markdown
## Summary

[1-2 sentence overview of the review]

### What's Done Well

- [Specific positive observation]

### Must Fix

#### [Issue Title]

**Location:** `file.ts:45-52`
**Lens:** [Which lens found this]
**Issue:** [Clear description of the problem]
**Impact:** [What happens if not fixed]
**Suggestion:** [Optional - how to fix]

### Should Fix

[Same format as Must Fix]

### Consider

[Brief bullet points only - max 2 items]
```

## When to Escalate

Stop the review and escalate when:

| Trigger                                         | Action                                                             |
| ----------------------------------------------- | ------------------------------------------------------------------ |
| Security-critical code (auth, crypto, payments) | See `references/security-lens-detail.md`, consider external review |
| 3+ "Must Fix" issues found                      | Stop reviewing. Escalate for fundamental redesign discussion.      |
| You don't understand the code                   | Don't guess. Request walkthrough before reviewing.                 |
| Architectural concerns                          | Flag for design discussion, don't try to "fix" in review           |

## Audit Mode

When explicitly requested to audit (not just review changes):

### Scope Definition

Before starting, clarify:

- What areas/modules to focus on?
- What's the primary concern? (Security? Performance? Maintainability?)
- What's the time budget?

### Sampling Strategy

For large codebases, don't review everything. Sample strategically:

1. **High-risk areas first** — Auth, payments, user input handling
2. **Recently changed code** — `git log --since="3 months ago" --name-only`
3. **Complex code** — High cyclomatic complexity, many dependencies
4. **Code with no tests** — Higher likelihood of hidden bugs

### Audit Checklist Addition

```
Audit-Specific Steps:
- [ ] Define scope and primary concerns with requester
- [ ] Identify high-risk areas for focused review
- [ ] Sample strategically (don't boil the ocean)
- [ ] Track coverage (what was reviewed vs skipped)
- [ ] Note systemic patterns across multiple files
```

## Edge Cases

For systematic edge case generation by input domain, see `references/edge-case-domains.md`.

## Common Mistakes

### Reviewing Without Understanding

Don't start reviewing until you understand:

- What is this code supposed to do?
- Why does this change exist?
- What's the broader context?

Reviewing without understanding produces shallow, unhelpful feedback.

### Lens Blending

Don't try to apply all lenses simultaneously. You'll miss things.

**Do this:**

1. Apply Malicious User lens → Note findings
2. Apply Careless Colleague lens → Note findings
3. Continue through remaining lenses

**Not this:**

- "Let me look at this code and find all the issues"

### Severity Inflation

Not everything is critical. Reserve "Must Fix" for actual blockers.

If everything is urgent, nothing is urgent.

### Missing the Forest for Trees

After applying all lenses, step back:

- Are there systemic patterns in the findings?
- Is there a deeper design issue causing multiple symptoms?
- Should this be a redesign conversation instead of a review?

## Key Principle

The goal isn't to find as many issues as possible. It's to find the issues that matter before they reach users.

Quality over quantity. Impact over volume. Trust over thoroughness.
