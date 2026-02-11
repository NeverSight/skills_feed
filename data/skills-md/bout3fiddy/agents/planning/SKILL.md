---
name: planning
description: "Planning workflows for clarifying underspecified work, spec-driven delivery, and Linear-backed tracking."
---

# Planning (Clarify + Spec + Track)

Use this skill when work is underspecified, needs a spec-first plan, or should be captured/tracked in Linear.

## Scope & routing
- Use for planning/spec/clarification requests or when the user explicitly asks for a plan.
- If the primary task is creating/updating a skill, prefer skill-creator; use planning only for a plan-only response.
- If the request shifts to implementation/build work, hand off to `coding` after clarifying scope.
- When opening references, use full repo paths like `skills/planning/references/...` (not `references/...`). If a reference read fails, retry once with the full path.
- If a trigger clearly matches, open the referenced file before drafting the plan/spec. If you need 1-2 clarifying questions first, ask them before opening the ref.
- If a word/length limit is given, keep it short and minimize extra reads.

## Reference triggers (open when clearly relevant)
If the request clearly matches one of the categories below, open the reference before drafting the plan. If the tracker/tooling is unclear, ask a brief clarifying question first.
- Underspecified implementation request -> `skills/planning/references/ask-questions-if-underspecified.md`
- Spec-first/iterative plan -> `skills/planning/references/spec-driven-iterative-builder.md`
- Ticketing or Linear ops/brainstorm capture -> `skills/planning/references/linear-mcp-ops.md`

## References
- `skills/planning/references/ask-questions-if-underspecified.md` - minimal clarifying questions workflow
- `skills/planning/references/spec-driven-iterative-builder.md` - spec-first iterative delivery
- `skills/planning/references/linear-mcp-ops.md` - Linear MCP operations and brainstorming capture
