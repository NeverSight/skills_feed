---
name: heuristic-evaluation
description: Systematic usability evaluation using established heuristics (Nielsen's 10, Shneiderman's 8, or custom rubrics). Use when reviewing UI designs, screenshots, prototypes, or live products for usability issues. Triggers on "review this design", "what's wrong with this UI", "usability check", "evaluate this interface", or when user shares screenshots/mockups asking for feedback.
---

# Heuristic Evaluation

Systematic usability review using established principles.

## When to Trigger

- User shares a screenshot, mockup, or prototype
- User asks for design feedback or review
- User asks "what's wrong with this"
- User wants to improve an interface
- Before shipping user-facing changes

## Quick Start

1. Ask user to share the interface (screenshot, URL, or description)
2. Ask: "Any specific flows or areas of concern?"
3. Run evaluation using Nielsen's 10 (default) or requested framework

## Core Workflow

```
Heuristic Evaluation Progress:
- [ ] Step 1: Capture interface context
- [ ] Step 2: Select evaluation framework
- [ ] Step 3: Evaluate against each heuristic
- [ ] Step 4: Score severity of issues
- [ ] Step 5: Prioritize recommendations
```

### Step 1: Capture Context

Before evaluating, understand:
- **What is this?** (App type, purpose)
- **Who uses it?** (Target users, expertise level)
- **What task?** (Primary user flow being evaluated)

If not provided, ask: "What are users trying to accomplish here?"

### Step 2: Select Framework

**Default**: Nielsen's 10 Usability Heuristics

**Alternatives** (if user requests or context suggests):
- Shneiderman's 8 Golden Rules — for interaction-heavy interfaces
- Cognitive Walkthrough — for first-time user experience
- Custom rubric — if user provides one

See [references/frameworks.md](references/frameworks.md) for full framework details.

### Step 3: Nielsen's 10 Evaluation

For each heuristic, identify violations:

| # | Heuristic | What to look for |
|---|-----------|------------------|
| 1 | **Visibility of system status** | Loading indicators, progress, confirmation, current state |
| 2 | **Match real world** | Familiar language, logical order, conventions from domain |
| 3 | **User control & freedom** | Undo, cancel, exit, back navigation, escape hatches |
| 4 | **Consistency & standards** | Same words/actions mean same things, platform conventions |
| 5 | **Error prevention** | Confirmations for destructive actions, constraints, defaults |
| 6 | **Recognition over recall** | Visible options, contextual help, no memorization required |
| 7 | **Flexibility & efficiency** | Shortcuts, customization, accelerators for experts |
| 8 | **Aesthetic & minimalist** | No irrelevant info, clear hierarchy, signal vs noise |
| 9 | **Help users with errors** | Plain language errors, specific problem, constructive solution |
| 10 | **Help & documentation** | Searchable, task-focused, concise, accessible when needed |

### Step 4: Score Severity

Rate each issue found:

| Score | Severity | Description |
|-------|----------|-------------|
| 0 | Not a problem | Disagreement with heuristic but not usability issue |
| 1 | Cosmetic | Fix only if time permits |
| 2 | Minor | Low priority, causes minor friction |
| 3 | Major | High priority, significant impact on task completion |
| 4 | Catastrophic | Must fix before release, prevents task completion |

**Scoring factors**:
- Frequency: How often does user encounter this?
- Impact: How much does it block the task?
- Persistence: Can users work around it?

### Step 5: Prioritize Output

Rank issues by: Severity × Frequency

Group into:
1. **Fix immediately** (Severity 4, or Severity 3 + high frequency)
2. **Fix soon** (Severity 3, or Severity 2 + high frequency)
3. **Fix later** (Severity 1-2, low frequency)

## Output Template

**Automatically save the output to `design/08-heuristic-evaluation.md` using the Write tool** while presenting it to the user.

```markdown
## Heuristic Evaluation: [Interface Name]

**Evaluated**: [Date]
**Framework**: Nielsen's 10 Usability Heuristics
**Scope**: [Specific flow or screens evaluated]

### Summary
- Critical issues: [count]
- Major issues: [count]  
- Minor issues: [count]

### Critical Issues (Fix Immediately)

#### Issue 1: [Brief description]
- **Heuristic violated**: #[number] — [name]
- **Location**: [Where in the interface]
- **Problem**: [What's wrong]
- **Impact**: [How it affects users]
- **Recommendation**: [How to fix]
- **Severity**: [0-4]

[Repeat for each critical issue]

### Major Issues (Fix Soon)
[Same format]

### Minor Issues (Fix Later)
[Same format, can be condensed to a table]

### Strengths Observed
- [What the interface does well]

### Next Steps
1. [Prioritized action]
2. [Prioritized action]
```

## Adaptive Behavior

**If user provides a screenshot:**
- Analyze visually
- Call out specific elements by location
- Be concrete: "The save button in the top right..." not "buttons should..."

**If user describes interface:**
- Ask clarifying questions before evaluating
- Focus on described pain points first

**If user is designer:**
- Skip heuristic definitions
- Use shorthand: "H4 violation" instead of explaining consistency

**If user is developer:**
- Include implementation-aware suggestions
- Note which fixes are quick wins vs architectural changes

## Handoff

After presenting the evaluation, suggest:
> "Use this report to prioritize fixes. Want me to help refine any screens based on these findings?"

**Note:** File is automatically saved to `design/08-heuristic-evaluation.md` for reference.

## Integration Points

Works well with:
- `assumption-mapping` — before building, question if the design addresses real needs
- `critique` — for broader feedback beyond usability
- `accessibility-audit` — for WCAG-specific evaluation

## References

- [references/frameworks.md](references/frameworks.md) — Full heuristic definitions and alternatives
- [references/examples.md](references/examples.md) — Sample evaluations
