---
name: assumption-mapping
description: Surface, prioritize, and track risky assumptions before investing significant effort. Use when starting a new project, before major feature work, when feeling uncertain about direction, when the user says "I think users want...", "we assume...", "probably...", or before any build decision that hasn't been validated with real users.
---

# Assumption Mapping

Surface hidden assumptions and prioritize which ones to validate before building.

## When to Trigger

- User is starting something new
- User expresses uncertainty ("I think...", "probably...", "should work...")
- User is about to invest significant effort
- User mentions building without mentioning validation
- User asks "what should I test first?"

## Quick Start

Ask the user:

1. "What are you building and for whom?"
2. "What needs to be true for this to succeed?"

Then run the assumption extraction workflow below.

## Core Workflow

```
Assumption Mapping Progress:
- [ ] Step 1: Extract assumptions from conversation
- [ ] Step 2: Categorize by type
- [ ] Step 3: Score risk and uncertainty
- [ ] Step 4: Prioritize for validation
- [ ] Step 5: Suggest validation methods
```

### Step 1: Extract Assumptions

Listen for assumption signals in what the user says:

| Signal phrase | Hidden assumption |
|---------------|-------------------|
| "Users want..." | Desirability assumption |
| "We can build..." | Feasibility assumption |
| "People will pay..." | Viability assumption |
| "It's easy to..." | Complexity assumption |
| "Everyone knows..." | Knowledge assumption |
| "They'll figure out..." | Usability assumption |

Extract 5-10 assumptions. Frame each as a testable statement:

**Bad**: "Users like simple things"
**Good**: "Users will complete onboarding in under 2 minutes without help"

### Step 2: Categorize Assumptions

Assign each assumption to one category:

| Category | Question it answers |
|----------|---------------------|
| **Desirability** | Do people want this? |
| **Feasibility** | Can we build this? |
| **Viability** | Can this sustain itself? |
| **Usability** | Can people use this? |
| **Ethical** | Should we build this? |

### Step 3: Score Each Assumption

Rate each assumption on two dimensions (1-5 scale):

**Impact**: If wrong, how badly does it hurt the project?
- 1 = Minor inconvenience
- 5 = Project fails completely

**Uncertainty**: How confident are we this is true?
- 1 = We have strong evidence
- 5 = Pure guess

### Step 4: Prioritize

Create a 2x2 priority matrix:

```
                    HIGH IMPACT
                         │
     ┌───────────────────┼───────────────────┐
     │                   │                   │
     │   VALIDATE LATER  │  VALIDATE FIRST   │
     │   (Low risk)      │  (Critical)       │
     │                   │                   │
LOW  ├───────────────────┼───────────────────┤ HIGH
UNCERTAINTY              │              UNCERTAINTY
     │                   │                   │
     │   SKIP            │  MONITOR          │
     │   (Safe)          │  (Watch for       │
     │                   │   signals)        │
     │                   │                   │
     └───────────────────┼───────────────────┘
                         │
                    LOW IMPACT
```

**Top-right quadrant = validate before building**

### Step 5: Suggest Validation Methods

For each critical assumption, suggest a lightweight validation:

| Assumption type | Fast validation (hours) | Deeper validation (days) |
|-----------------|-------------------------|--------------------------|
| Desirability | 5 user interviews | Landing page test |
| Feasibility | Technical spike | Prototype |
| Viability | Competitor pricing research | Willingness-to-pay interviews |
| Usability | 3-person hallway test | Usability study |

See [references/validation-methods.md](references/validation-methods.md) for detailed methods.

## Output Template

**Automatically save the output to `design/03-assumption-mapping.md` using the Write tool** while presenting findings in this format:

```markdown
## Assumption Map for [Project Name]

### Critical Assumptions (Validate First)
| # | Assumption | Type | Impact | Uncertainty | Suggested Test |
|---|------------|------|--------|-------------|----------------|
| 1 | [statement] | [type] | [1-5] | [1-5] | [method] |

### Secondary Assumptions (Validate Later)
[Same table format]

### Safe Assumptions (Monitor)
[Bulleted list]

### Recommended Next Steps
1. [First validation to run]
2. [Second validation to run]
```

## Adaptive Behavior

**If user is new to assumption mapping:**
- Explain briefly why we do this (1 sentence)
- Guide them through extraction with examples
- Keep the output simple

**If user is familiar:**
- Skip explanations
- Jump to extraction
- Offer the full matrix output

**Gauge familiarity by asking:** "Have you mapped assumptions before, or should I walk you through it?"

## Handoff

Suggest next steps:
> "Use this map to prioritize validation tests before full development. Want to proceed with `/solution-scoping` or test critical assumptions first?"

**Note:** File is automatically saved to `design/03-assumption-mapping.md` for context preservation.

## Integration Points

This skill works well before:
- `problem-framing` — if problem isn't clear yet
- `validation` — to test the critical assumptions identified here
- `ideation` — to generate solutions once assumptions are validated

## References

- [references/validation-methods.md](references/validation-methods.md) — Detailed validation techniques
- [references/examples.md](references/examples.md) — Complete worked examples
