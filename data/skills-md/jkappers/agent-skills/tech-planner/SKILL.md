---
name: tech-planner
description: >
  Use when (1) evaluating technical feasibility of a feature spec,
  (2) making technology or framework choices,
  (3) defining system architecture for a new feature,
  (4) documenting architectural decisions as ADRs,
  (5) analyzing integration points and data flow for a proposed change.
argument-hint: "[path/to/spec]"
---

# Technical Planning

Create technical overviews and Architecture Decision Records (ADRs) that document HOW a feature is built — architecture, integration, and decisions.

## Workflow

1. **Read the spec** — Load the spec from the argument path. If no path is provided, ask the user for the spec location.
2. **Analyze architecture** — Evaluate the analysis questions below against the spec.
3. **Create technical overview** — Write `specs/feature-name/tech.md` using [`assets/tech.md`](assets/tech-template.md).
4. **Determine if ADR(s) are needed** — Apply the decision criteria below. Skip if no ADR is warranted.
5. **Create ADR(s)** — Write `docs/adr/NNN-title.md` using [`assets/adr-template.md`](assets/adr-template.md). Scan existing ADRs for the highest number, increment by one, and pad to 3 digits.

## Architectural Analysis

Evaluate these questions for every technical plan:

1. What existing systems does this touch?
2. Where does this feature start and end?
3. How does it connect to existing components?
4. How does data flow through the system?
5. What are we gaining and giving up?

## When to Create an ADR

Create an ADR when the decision:

- Chooses between competing technologies or frameworks
- Sets a project-wide pattern or convention
- Selects an authentication or authorization approach
- Introduces a trade-off with long-term implications
- Is difficult or expensive to reverse

## When NOT to Create an ADR

Skip the ADR when the decision:

- Affects only a single feature (document in the feature spec instead)
- Covers implementation details within one component
- Describes a temporary workaround or experiment

See [`references/adr-guide.md`](references/adr-guide.md) for extended ADR guidance, status lifecycle, and content guidelines.

## Constraints

- Never include specific file paths, implementation order, code snippets, line-by-line details, time estimates, or timeline references in technical overviews or ADRs.
- Keep technical overviews focused on architecture boundaries, data flow, and integration — not implementation steps.

## Assets

- [`assets/tech-template.md`](assets/tech-template.md) — Technical overview template
- [`assets/adr-template.md`](assets/adr-template.md) — ADR template
- [`references/adr-guide.md`](references/adr-guide.md) — Extended ADR guidance
