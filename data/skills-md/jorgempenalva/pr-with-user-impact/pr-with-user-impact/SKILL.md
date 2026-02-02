---
name: pr-with-user-impact
description: Generate PRs with concrete User Workflow Impact sections. Use when creating pull requests, commits, or describing code changes. Transforms technical changes into user-focused before/after documentation with emotional resonance.
---

# PR with User Workflow Impact

Generate pull requests that clearly communicate how code changes affect real users. Transforms technical diffs into concrete before/after examples with emotional resonance.

## When to Use

- Creating a pull request
- Writing commit messages for significant changes
- Describing the impact of a feature, fix, or refactor
- Reviewing changes before merge

## Core Principle

**Every change affects a user doing something.** Document the "who does what" and "how it changes for them" with concrete examples, not abstract descriptions.

---

## PR Template

Every PR includes this section:

```markdown
## User Workflow Impact

### [Workflow Name]
**User action:** [What the user is trying to accomplish]

| Before | After |
|--------|-------|
| [Concrete example of the problem with realistic details] | [Concrete example of the fix with realistic details] |

**Impact:** [Emotional language + business outcome]
```

---

## Writing Effective Before/After Tables

### WRONG - Abstract descriptions

| Before | After |
|--------|-------|
| Page was slow | Page is faster |
| Categories were imprecise | Categories are more precise |
| Error handling was bad | Error handling is better |

### RIGHT - Concrete and specific

| Before | After |
|--------|-------|
| Dashboard takes 4.2s to load—users see a blank screen, often refreshing thinking it's frozen | Dashboard loads in 0.8s with a skeleton UI appearing immediately |
| A category "Cancel and Refund Requests" with 47 docs—but 38 only mention cancellation, hiding that pricing is the real issue | Two categories: "Cancellation Due to Pricing" (38 docs) and "Refund Delays" (6 docs). The primary driver is obvious. |
| `{"error": "Something went wrong"}` | `{"error": "INVALID_DATE_FORMAT", "field": "start_date", "expected": "ISO 8601", "received": "12/25/2024"}` |

---

## Writing Effective Impact Statements

### WRONG - Clinical/factual only

> Page loads faster now.

> Users can now see more precise categories.

> Error handling is improved.

### RIGHT - Emotional + business outcome

> Eliminates the "is it broken?" moment. Users no longer abandon the dashboard before it loads.

> Patterns that were buried in misleading labels now surface on their own. Users act on real insights, not aggregation artifacts.

> Developers stop guessing what went wrong. The error tells them exactly what to fix.

---

## Emotional Language Bank

Use these phrases to make pain/relief tangible:

**Pain words:**
- "frustrating"
- "buried"
- "hidden"
- "misleading"
- "forced to manually"
- "wasted time"
- "mysterious"
- "silently fails"
- "guessing"

**Relief words:**
- "eliminates"
- "surfaces automatically"
- "immediately visible"
- "no longer need to"
- "obvious"
- "tells them exactly"
- "one click"

**Discovery framing:**
- "X was hidden in Y → X now surfaces as its own insight"
- "What was buried in [broad category] now appears as [specific item]"

---

## Examples by Change Type

### Performance improvement

```markdown
### Dashboard Loading
**User action:** Opening the analytics dashboard to check daily metrics

| Before | After |
|--------|-------|
| 4.2 second blank screen—users often refresh thinking the page is frozen | 0.8 second load with skeleton UI appearing immediately |

**Impact:** Eliminates the "is it broken?" moment. Users start their day with data instead of frustration.
```

### Bug fix

```markdown
### Form Submission
**User action:** Submitting the contact form

| Before | After |
|--------|-------|
| Entering "José García" causes silent failure—users retry multiple times before giving up or removing accents | "José García" submits successfully. All UTF-8 characters work. |

**Impact:** Users with accented names no longer have to "anglicize" their input to get through.
```

### Feature addition

```markdown
### Data Export
**User action:** Exporting results for a stakeholder presentation

| Before | After |
|--------|-------|
| Only CSV available—users manually convert to Excel, recreating charts and formatting | Direct Excel export with formatted tables and charts. One click to presentation-ready. |

**Impact:** Eliminates the CSV-to-Excel conversion ritual. "Analysis complete" to "ready to present" in seconds.
```

### Refactor/API change

```markdown
### API Error Handling
**User action:** Debugging a failed API integration

| Before | After |
|--------|-------|
| `{"error": "Something went wrong"}` | `{"error": "INVALID_DATE_FORMAT", "field": "start_date", "expected": "ISO 8601", "received": "12/25/2024"}` |

**Impact:** Developers stop guessing what went wrong. The error tells them exactly what to fix.
```

### Algorithm/data change

```markdown
### Category Review
**User action:** Reviewing AI-generated categories to find actionable patterns

| Before | After |
|--------|-------|
| A category "Cancel and Refund Requests" with 47 docs—but 38 only mention cancellation, hiding that pricing is the real issue | Two categories: "Cancellation Due to Pricing" (38 docs) and "Refund Delays" (6 docs). The primary driver is obvious. |

**Impact:** Patterns that were buried in misleading labels now surface on their own. Users act on real insights, not aggregation artifacts.
```

### Security/infrastructure change

```markdown
### Session Management
**User action:** Working on a long document without saving

| Before | After |
|--------|-------|
| Session expires silently after 30 minutes—users lose unsaved work with no warning | 5-minute warning before expiration with one-click extend. Auto-save every 60 seconds. |

**Impact:** No more lost work from surprise logouts. Users can focus on their task without watching the clock.
```

---

## Key Rules

1. **Never use abstract comparisons** - "better," "improved," "faster" need concrete proof
2. **Include realistic details** - times, counts, error messages, names, category names
3. **Testable claims** - someone could verify the before/after by using the product
4. **No technical jargon** - never mention parameters, thresholds, implementation details, or internal code concepts
5. **One scenario per section** - if multiple impacts, use multiple workflow sections
6. **Business outcomes** - connect to why stakeholders should care, not just what changed

---

## How to Identify User Workflows

When analyzing a diff, ask:

1. **Who uses this?** (End users, developers, admins, mobile users, etc.)
2. **What are they trying to accomplish?** (Login, search, export, debug, etc.)
3. **What was painful before?** (Slow, confusing, broken, manual, hidden)
4. **What's better now?** (Fast, clear, working, automatic, visible)
5. **Why should someone care?** (Time saved, errors prevented, decisions enabled)

---

## Anti-Patterns to Avoid

### Too technical
- "Refactored useEffect dependencies"
- "Updated webpack config"
- "Changed clustering scale from 0.7 to 0.5"
- "Fixed race condition in state management"

### Too vague
- "Improved performance"
- "Fixed bugs"
- "Better UX"
- "More accurate results"

### No user context
- "Added caching layer"
- "Migrated to new API"
- "Updated dependencies"

---

## Multiple User Types

When changes affect different user groups, include separate sections or a summary:

```markdown
## User Workflow Impact

### For End Users: Dashboard Loading
**User action:** Opening the app to check their data
| Before | After |
|--------|-------|
| 4s blank screen | 0.8s with skeleton UI |
**Impact:** Eliminates the "is it broken?" moment.

### For Developers: Error Debugging
**User action:** Investigating failed API calls
| Before | After |
|--------|-------|
| Generic error message | Structured error with field and expected format |
**Impact:** Debugging time drops from minutes to seconds.
```

---

## Quick Checklist

Before finalizing a PR, verify:

- [ ] Identified which users are affected
- [ ] Described what they're trying to do (the workflow)
- [ ] Showed concrete before/after with realistic details
- [ ] Used emotional language in impact statement
- [ ] Connected to business outcome (why it matters)
- [ ] Avoided technical jargon and implementation details
- [ ] Claims are testable by using the product
