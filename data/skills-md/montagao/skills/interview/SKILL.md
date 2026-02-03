---
name: interview
description: Conduct an in-depth interview with the user to create a detailed specification document. Invoke as "/interview [topic]" where topic describes what to interview about. Use when asked to "interview me", "create a spec", "help me spec out", "gather requirements", or when needing to deeply understand a project before implementation.
allowed-tools: AskUserQuestion, Write
---

# Interview

Conduct a thorough, in-depth interview to produce a comprehensive specification document.

## Process

1. **Understand the scope** from the provided arguments/instructions
2. **Interview iteratively** using AskUserQuestion - continue until all aspects are covered
3. **Write the spec** to a file when complete

## Interview Guidelines

### Question Depth

Ask non-obvious questions. Skip surface-level questions the user has likely already considered. Dig into:

- Edge cases and failure modes
- Constraints and non-functional requirements
- User personas and their specific needs
- Integration points and dependencies
- Security, privacy, and compliance implications
- Scalability and performance expectations
- Migration and backwards compatibility
- Rollback and recovery strategies
- Observability and debugging needs
- Trade-offs the user is willing to make

### Question Style

- Ask 1-2 focused questions at a time (use AskUserQuestion with options when choices are clear)
- Follow up on vague answers - push for specifics
- Challenge assumptions politely
- Surface implicit requirements the user hasn't stated
- Explore "what if" scenarios

### Areas to Cover

Adapt based on context, but consider:

**Technical**: Architecture, data models, APIs, storage, caching, auth, error handling
**UX**: User flows, states, feedback, accessibility, edge case UI
**Operational**: Deployment, monitoring, alerts, on-call, maintenance
**Business**: Success metrics, timelines, dependencies, stakeholders, budget constraints
**Risk**: What could go wrong? What's the blast radius? What's the mitigation?

## Output

When the interview is complete, write a structured spec to a file (e.g., `spec.md` or `docs/<topic>-spec.md`).

The spec should include:
- Overview and goals
- Requirements (functional and non-functional)
- Technical approach
- Open questions (if any remain)
- Out of scope items

## Instructions

<instructions>$ARGUMENTS</instructions>
