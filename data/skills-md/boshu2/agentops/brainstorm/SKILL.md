---
name: brainstorm
description: 'Separate WHAT from HOW before planning. Clarify goals, explore approaches, capture structured design decisions. Triggers: brainstorm, explore idea, clarify goal, idea phase.'
metadata:
  tier: solo
  dependencies: []
---

# /brainstorm — Clarify Goals Before Planning

> **Purpose:** Separate WHAT from HOW. Explore the problem space before committing to a solution.

Four phases:
1. **Assess clarity** — Is the goal specific enough?
2. **Understand idea** — What problem, who benefits, what exists?
3. **Explore approaches** — Generate options, compare tradeoffs
4. **Capture design** — Write structured output for `/plan`

---

## Quick Start

```bash
/brainstorm "add user authentication"     # full 4-phase process
/brainstorm                                # prompts for goal
```

---

## Execution Steps

### Phase 1: Assess Clarity

If the user provided a goal string, evaluate it. Otherwise prompt for one.

Use `AskUserQuestion` with options to gauge clarity:

- **clear** — Goal is specific and actionable (e.g., "add JWT auth to the API")
- **vague** — Goal exists but needs narrowing (e.g., "improve security")
- **exploring** — No firm goal yet, just a direction (e.g., "something with auth")

If **vague** or **exploring**, ask follow-up questions to sharpen the goal before proceeding. Do NOT move to Phase 2 until you have a concrete problem statement (one sentence, testable).

### Phase 2: Understand the Idea

Answer these questions (use codebase exploration as needed):

1. **What problem does this solve?** — State the pain point in concrete terms.
2. **Who benefits?** — End users, developers, operators, CI pipeline?
3. **What exists today?** — Current state, prior art in the codebase, adjacent systems.
4. **What constraints matter?** — Performance, compatibility, security, timeline.

Summarize findings before moving on. If anything is unclear, ask the user.

### Phase 3: Explore Approaches

Generate **2-3 distinct approaches**. For each:

- **Name** — Short label (e.g., "JWT middleware", "OAuth proxy", "Session cookies")
- **How it works** — 2-3 sentences
- **Pros** — What it gets right
- **Cons** — What it gets wrong or defers
- **Effort** — Rough scope (small / medium / large)

Present the comparison and use `AskUserQuestion` to let the user pick an approach or request a hybrid.

### Phase 4: Capture Design

Generate a date slug: `YYYY-MM-DD-<goal-slug>` (lowercase, hyphens, no spaces).

Write the output file to `.agents/brainstorm/YYYY-MM-DD-<slug>.md`:

```markdown
---
name: <goal-slug>
date: YYYY-MM-DD
status: captured
---
# Brainstorm: <Goal>
## Problem Statement
## Approaches Considered
## Selected Approach
## Open Questions
## Next Step: /plan
```

All five sections must be populated. The "Next Step" section should contain a concrete `/plan` invocation suggestion with the selected approach as context.

Create the `.agents/brainstorm/` directory if it does not exist.

---

## Termination

Phase 4 output written = done. No further phases, no loops.

## Validation

After writing the output file, verify:
1. File exists at the expected path
2. All 5 sections (`Problem Statement`, `Approaches Considered`, `Selected Approach`, `Open Questions`, `Next Step: /plan`) are present and non-empty

Report the file path to the user.

---

## Examples

**Example 1: Specific goal**
```
User: /brainstorm "add rate limiting to the API"

Phase 1: Goal is clear — add rate limiting to the API.
Phase 2: Problem is uncontrolled request volume causing timeouts.
         Benefits operators and end users. No rate limiting exists today.
Phase 3: Three approaches — token bucket middleware, API gateway,
         per-route decorators. User picks token bucket.
Phase 4: Writes .agents/brainstorm/2026-02-17-rate-limiting.md
```

**Example 2: Vague goal**
```
User: /brainstorm "improve performance"

Phase 1: Goal is vague. Asks: "Which part? API response times,
         build speed, database queries, or something else?"
         User says: "API response times on the search endpoint."
Phase 2: Investigates search endpoint, finds N+1 queries.
Phase 3: Approaches — query optimization, caching layer, pagination.
Phase 4: Writes .agents/brainstorm/2026-02-17-search-performance.md
```

---

## See Also

- [skills/plan/SKILL.md](../plan/SKILL.md) — Decompose the selected approach into actionable issues
