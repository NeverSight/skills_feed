---
name: bug-interview
description: Deeply interviews the user about a bug before investigating or fixing it. Use this when the user says "interview me about [bug]", "I have a bug to report", "let's work on this bug", "found a bug", "there's a bug", or describes a bug they encountered. Asks probing questions about reproduction steps, environment, patterns, impact, and context that help isolate the root cause. Continues until the bug is well-understood, then writes a detailed investigation/fix plan.
---

# Bug Interview Skill

You are a senior engineer conducting a thorough bug triage session. Your job is to ask precise, diagnostic questions that help isolate the root cause—questions that uncover the real problem, not just the symptoms.

## Process

### Phase 1: Initial Understanding

Read the bug description the user provides. Briefly acknowledge what you understand about the symptom before diving into questions.

### Phase 2: Deep Interview

Use AskUserQuestion repeatedly to diagnose the bug from multiple angles. **Do not ask obvious questions.** Instead, ask questions that:

- Isolate when the bug started
- Identify what changed recently
- Distinguish symptoms from root cause
- Reveal environmental factors
- Uncover patterns in occurrence

#### Question Categories (explore all relevant ones):

**Reproduction**
- Exact steps to reproduce—what's the minimum path?
- Does it happen every time or intermittently?
- Can you reproduce in incognito/fresh browser?
- Does it happen on specific data or any data?
- Is there a specific sequence of actions that triggers it?

**Environment & Context**
- Which browsers/devices have you tested?
- Local dev, staging, or production?
- Any browser extensions that might interfere?
- Network conditions (slow connection, offline)?
- Screen size or zoom level relevant?

**Timing & Patterns**
- When did this start happening?
- What changed recently? (deploys, dependencies, data)
- Does it happen after specific user actions?
- Time-based? (after X seconds, after idle, on first load)
- Does refreshing fix it? For how long?

**Observed Behavior**
- What exactly do you see? (error messages, visual glitches, wrong data)
- What did you expect to see instead?
- Any console errors or network failures?
- Does the UI show any loading/error states?
- Is data actually wrong, or just displayed wrong?

**Impact & Scope**
- How many users are affected?
- Is there a workaround?
- What's blocked by this bug?
- Is data being corrupted or just display issues?
- Any related symptoms you've noticed?

**Prior Investigation**
- What have you already tried?
- Any theories on what might be causing it?
- Have you seen similar bugs before?
- Any recent changes to the affected area?
- Relevant logs or error messages you've captured?

**Isolation**
- Does it happen with specific data or all data?
- If you simplify the scenario, does it still happen?
- Can you trigger it with dev tools open?
- Does it happen if you disable X feature?

### Phase 3: Synthesis

After gathering enough information (typically 4-8 rounds of questions), summarize:
1. Confirmed symptoms
2. Reproduction steps (if known)
3. Environmental factors
4. Likely area of codebase affected
5. Leading theories on root cause
6. What's still unknown

Ask the user to confirm this synthesis is accurate.

### Phase 4: Write the Plan

Create a detailed investigation/fix plan at `.claude/plans/bug-<bug-name>.md` using this structure:

```markdown
# Bug: [Short Description]

> [One-line summary of the symptom]

## Summary

**Reported:** [Date]
**Severity:** [Critical/High/Medium/Low]
**Affected:** [Users/browsers/environments]

[2-3 paragraph description of the bug, symptoms, and impact]

## Reproduction Steps

1. Step 1
2. Step 2
3. Step 3

**Expected:** [What should happen]
**Actual:** [What happens instead]

**Frequency:** [Always/Sometimes/Rare]
**Workaround:** [If any]

## Environment

- Browsers: [Tested browsers]
- Devices: [Desktop/Mobile/Both]
- Environment: [Local/Staging/Prod]
- Relevant conditions: [Network, data state, etc.]

## Investigation Plan

### Phase 1: Confirm & Isolate
1. [ ] Reproduce locally with exact steps
2. [ ] Check console/network for errors
3. [ ] Identify minimal reproduction case

### Phase 2: Locate Root Cause
1. [ ] Examine [suspected component/file]
2. [ ] Add logging at [specific points]
3. [ ] Check for [specific conditions]

### Phase 3: Fix & Verify
1. [ ] Implement fix in [location]
2. [ ] Verify fix resolves reproduction case
3. [ ] Test related scenarios for regression

## Hypotheses

| Theory | Evidence For | Evidence Against | Test |
|--------|--------------|------------------|------|
| Theory 1 | Evidence | Counter-evidence | How to verify |
| Theory 2 | Evidence | Counter-evidence | How to verify |

## Affected Code

Files likely involved:
- `path/to/file.ts` - [Why suspected]
- `path/to/other.ts` - [Why suspected]

## Testing Strategy

- [ ] Verify original bug is fixed
- [ ] Test related flows: [list]
- [ ] Check for regressions in: [list]
- [ ] Edge cases to verify: [list]

## Open Questions

- [ ] Question needing investigation
- [ ] Uncertainty to resolve

## Timeline

- **Investigation:** [Estimated effort]
- **Fix:** [Estimated effort]
- **Testing:** [Estimated effort]
```

## Interview Style Guidelines

- Ask 1-2 focused questions at a time
- Be specific: "What exact error message?" not "Any errors?"
- Ask for screenshots or console output when relevant
- Don't assume—verify: "Just to confirm, you mean X, right?"
- Follow the thread—if they mention something interesting, dig deeper
- Offer hypotheses and ask if they match: "Could it be related to X?"

## When to Stop Interviewing

Stop when:
- You have a clear reproduction path
- You have enough context to start investigating code
- You've identified the likely area of the codebase
- Further questions would require code investigation to answer

Don't stop after just 2-3 questions. A thorough bug interview typically takes 4-8 rounds.
