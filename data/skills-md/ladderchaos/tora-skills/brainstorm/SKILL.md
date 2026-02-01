---
name: brainstorm
description: Structured ideation and exploration workflow. Use this skill when exploring ideas, evaluating options, or needing creative problem-solving before implementation.
---

# Brainstorm

Structured workflow for exploring ideas, evaluating trade-offs, and reaching decisions before committing to implementation.

## When This Skill Activates

- Exploring multiple approaches to a problem
- Evaluating architecture or design options
- Creative problem-solving sessions
- When "I'm not sure how to approach this"
- Before starting complex features

## Brainstorm Protocol

### Phase 1: Diverge (Generate Options)

Generate multiple approaches without judgment:

```markdown
## Options

### Option A: [Name]
- **Approach**: [Brief description]
- **Pros**: [Benefits]
- **Cons**: [Drawbacks]

### Option B: [Name]
- **Approach**: [Brief description]
- **Pros**: [Benefits]
- **Cons**: [Drawbacks]

### Option C: [Name]
- **Approach**: [Brief description]
- **Pros**: [Benefits]
- **Cons**: [Drawbacks]
```

**Rules for divergence:**
- Aim for 3-5 distinct options
- Include at least one unconventional approach
- No filtering yet - capture all ideas
- Brief descriptions only

### Phase 2: Analyze (Evaluate Trade-offs)

Compare options against criteria:

```markdown
## Analysis

| Criteria | Option A | Option B | Option C |
|----------|----------|----------|----------|
| Complexity | Low | Medium | High |
| Time to implement | Fast | Medium | Slow |
| Maintainability | Good | Good | Poor |
| Fits existing patterns | Yes | Partial | No |
| Risk | Low | Medium | High |
```

**Common criteria:**
- Implementation complexity
- Performance implications
- Maintainability
- Security considerations
- Alignment with existing patterns

### Phase 3: Converge (Decide)

Make a recommendation:

```markdown
## Recommendation

**Selected**: Option [X]

**Rationale**: [Why this option best balances the trade-offs]

**Risks to monitor**: [What could go wrong]

**Next steps**:
1. [First action]
2. [Second action]
```

## Quick Brainstorm (5-minute version)

For smaller decisions:

```markdown
## Quick Decision: [Topic]

**Options**: A) [option] | B) [option] | C) [option]

**Pick**: [Choice] because [one-line rationale]
```

## When to Skip Brainstorming

- Clear requirements with obvious solution
- Bug fixes with known cause
- Following established patterns
- User has already decided approach

## Output Formats

| Scenario | Format |
|----------|--------|
| Architecture decision | Full 3-phase + ADR |
| Feature approach | Full 3-phase |
| Implementation detail | Quick brainstorm |
| Naming/style choice | Quick brainstorm |

## Anti-Patterns

- Analysis paralysis - set time limit
- Premature convergence - explore before deciding
- Skipping trade-off analysis
- Not documenting the decision rationale
