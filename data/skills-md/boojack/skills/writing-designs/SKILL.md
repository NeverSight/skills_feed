---
name: writing-designs
description: Researches how the industry solves a defined issue, collects references from engineering blogs, open-source projects, and technical articles, then produces a design document with industry baseline, research summary, design goals, non-goals, and proposed design. Use when an issue definition exists in docs/issues/ and a concrete design is needed before implementation begins.
---

# Writing Designs

Takes `definition.md` from `docs/issues/YYYY-MM-DD-<slug>/` as input. Produces a design document grounded in research, not speculation.

Does NOT implement code, create PRs, or make architectural changes. Output is a design document only.

```
NO DESIGN DECISION WITHOUT A CITED REFERENCE
```

## Workflow

```
- [ ] Step 1: Load Issue Definition
- [ ] Step 2: Research
- [ ] Step 3: Industry Baseline
- [ ] Step 4: Research Summary
- [ ] Step 5: Design Goals & Non-Goals
- [ ] Step 6: Proposed Design
- [ ] Step 7: Validate
```

### Step 1: Load Issue Definition

Read `definition.md` from the issue folder.

- If no folder is specified, list available folders and ask
- Extract: background, issue statement, current state, non-goals, open questions
- Note open questions that affect design decisions

### Step 2: Research

1. **Web search**: Engineering blogs, technical articles, documentation
2. **GitHub**: Open-source implementations, issues, PRs showing patterns

Prioritize primary sources from companies that have solved this at scale. Use at least 3 distinct search queries.

Rules:
- At least 5 references, each with a URL you actually visited
- Verify each URL loads via `WebFetch` before including
- Do NOT fabricate URLs

### Step 3: Industry Baseline

- Common/default solution and widely adopted patterns
- Trade-offs and known limitations
- Cite references by title

### Step 4: Research Summary

- Key patterns across sources
- Which approaches fit the current issue and codebase
- What research suggests about the issue's open questions

### Step 5: Design Goals & Non-Goals

**Design Goals** — derive from issue statement, order by priority. Each must be **verifiable**: a measurable metric or testable assertion.

**Non-Goals** — inherit all from issue definition, add any discovered during research.

### Step 6: Proposed Design

- Reference specific files/modules from issue definition's current state
- Explain key decisions and why alternatives were rejected (cite research)
- Include interface definitions or data flows where helpful
- Every decision traces to a design goal
- Pseudocode acceptable; implementation code is not

### Step 7: Validate

| Check | Criteria |
|---|---|
| References | 5+ entries with verified URLs via `WebFetch` |
| Industry Baseline | Cites references by title, no speculation |
| Design Goals | Verifiable, trace to issue statement |
| Non-Goals | All inherited items from issue definition included |
| Proposed Design | Every decision traces to a goal, no implementation code |

If any check fails, return to the failing step and revise.

## Output

Save to `docs/issues/YYYY-MM-DD-<slug>/design.md` in the same folder as `definition.md`.

```markdown
## References

## Industry Baseline

## Research Summary

## Design Goals

## Non-Goals

## Proposed Design
```

Missing any section invalidates the output.

## Anti-patterns

- ❌ "Most apps probably use X" → ✓ "PDF.js uses X (PR #7793)"
- ❌ Atomic goal + best-effort design → ✓ reconcile goals and design
- ❌ `keys.filter(k => ...)` → ✓ "Collect keys ending with suffix"
- ❌ Unverified URLs → ✓ every URL visited via `WebFetch`
- ❌ Features not traced to goals → ✓ every decision references a goal
