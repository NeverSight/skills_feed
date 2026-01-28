---
name: documentation
description: Use when the user asks to enhance documentation, add code comments, create API docs, improve README files, or document code. Triggers on keywords like "document", "documentation", "API docs", "comments", "JSDoc", "XML comments", "README", "getting started", "setup instructions".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task, TodoWrite
---

# Documentation Enhancement

Expert technical writer for code documentation, API docs, and README files.

> **Autonomous mode**: Set `autonomous: true` in task context to skip approval gate and execute directly.

**⚠️ MUST READ** `.claude/skills/shared/anti-hallucination-protocol.md` — validation checkpoints, evidence chains, confidence levels

---

## Phase 1: Investigation

1. **Discovery** - Search for files needing documentation
2. **Analysis** - Identify documentation gaps, missing comments, undocumented APIs
3. **Knowledge Graph** - Build structured analysis in `.ai/workspace/analysis/[task-name].md`

Track per file: `documentationGaps`, `complexityLevel`, `apiDocumentationNeeds`, `exampleRequirements`

## Phase 2: Documentation Plan

Generate plan covering:
- Scope (which files/APIs/components)
- Documentation type (code comments, API docs, README, architecture)
- Priority order (public APIs first, then complex logic, then internal)

## Phase 3: Approval Gate

**CRITICAL**: Present plan for approval. Skip if `autonomous: true`.

## Phase 4: Execution

Apply documentation following patterns from references.

### Code Documentation Mode
**⚠️ MUST READ** `.claude/skills/documentation/references/code-documentation-patterns.md`

5 patterns available: C# XML docs, TypeScript JSDoc, API endpoint docs, README feature docs, inline comments.

### README Mode
**⚠️ MUST READ** `.claude/skills/documentation/references/readme-template.md`

Workflow:
1. **Discovery** - Project structure, features, setup requirements
2. **Template** - Apply README structure (Features, Prerequisites, Installation, Configuration, Usage, Development, Testing, Troubleshooting)
3. **Validate** - Verify all instructions are accurate and testable

## Phase 5: Validation

- Accurate (matches actual code)
- Complete (covers all public APIs)
- Helpful (includes practical examples)
- Consistent (follows established patterns)

## Guidelines

- **Accuracy-first**: Verify every documented feature with actual code
- **Explain "why" not "what"**: Don't state the obvious
- **Example-driven**: Include practical, copy-pasteable examples
- **Keep docs close to code**: Prefer inline over separate files
- **User-first for READMEs**: Organize for new users getting started


## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
