---
name: docs-update
description: Documentation update workflow. Use when modifying files in docs/ directory or any markdown files (*.md).
---

# Documentation Update Workflow

Workflow for documentation changes with SSOT awareness.

## Prerequisites

- **Use `git-workflow` Skill** for branch, commit, and PR workflow.
- **Understand SSOT structure** before editing any documentation.

## SSOT Awareness

**Critical**: Before editing documentation, identify if the file is an SSOT or references one.

### SSOT Locations

| Category | SSOT Location | Description |
|----------|---------------|-------------|
| Agent behavior | `AGENTS.md` | Entry point for all agents |
| Agent instruction design | `docs/design/ai-agents-instruction.md` | Command/Skill/Rule architecture |
| Label definitions | `docs/standards/task-classification.md` | All label types and meanings |
| Label → Skill mapping | `.claude/skills/label-context-mapping/` | Operational routing |
| Coding conventions | `docs/standards/coding-conventions.md` | Code style rules |
| Security rules | `docs/standards/security.md` | Security requirements |
| Testing standards | `docs/standards/testing.md` | Test requirements |
| Workflow | `docs/standards/workflow.md` | Development workflow |

### SSOT Rules

1. **If editing an SSOT file**: Update carefully, as other files reference it
2. **If editing a non-SSOT file**: Ensure it references the SSOT, don't duplicate information
3. **If information conflicts**: The SSOT is authoritative; update the referencing file

## Applicable Files

| Path | Type | Description |
|------|------|-------------|
| `AGENTS.md` | SSOT | Agent behavior entry point |
| `ARCHITECTURE.md` | SSOT | System architecture |
| `docs/standards/` | SSOT | Project standards |
| `docs/design/` | Reference | Design documents |
| `docs/guidelines/` | Reference | Detailed guidelines |
| `docs/crypto/` | Reference | Chain-specific documentation |
| `docs/task-contexts/` | Context | Task-specific procedures |
| `internal/AGENTS.md` | Scoped SSOT | Internal package guidelines |
| `pkg/AGENTS.md` | Scoped SSOT | Public package guidelines |

## Documentation Hierarchy

```
AGENTS.md (entry point)
    │
    ├─ docs/design/ai-agents-instruction.md (instruction system design)
    │
    ├─ docs/standards/ (SSOT for standards)
    │   ├─ task-classification.md (label definitions)
    │   ├─ coding-conventions.md
    │   ├─ security.md
    │   ├─ testing.md
    │   └─ workflow.md
    │
    ├─ docs/guidelines/ (detailed how-to)
    │   ├─ database.md
    │   └─ code-generation.md
    │
    └─ docs/task-contexts/ (task-specific context)
        ├─ bug-fix.md, feature-add.md, etc.
        └─ chains/ (chain-specific)
```

## Workflow

### 1. Identify Document Type

Before editing, determine:

- Is this file an SSOT?
- Does this file reference an SSOT?
- What other files might be affected?

### 2. Check for Duplicated Information

If the information you're adding already exists elsewhere:

- Find the SSOT location
- Add a reference instead of duplicating

### 3. Make Changes

Follow markdown style guidelines:

- Use ATX-style headers (`#`, `##`, `###`)
- One blank line between sections
- Code blocks with language specifier
- Tables for structured data
- Relative links within docs

### 4. Verify Cross-References

After changes:

- [ ] Links work correctly
- [ ] SSOT references are accurate
- [ ] No information duplication
- [ ] Consistent formatting

## Markdown Style

### Headers

```markdown
# Top Level (document title)
## Section
### Subsection
```

### Code Blocks

Always specify language:

```markdown
```go
func example() {}
```

```bash
make go-lint
```

```

### Tables

Use tables for structured data:

```markdown
| Column 1 | Column 2 |
|----------|----------|
| Value 1  | Value 2  |
```

### Links

- Use relative links: `[link](../path/to/file.md)`
- Verify links work after moving files
- Update cross-references when renaming

## Self-Review Checklist

- [ ] SSOT location identified (if applicable)
- [ ] No duplicated information
- [ ] References point to correct SSOT
- [ ] Markdown renders correctly
- [ ] Links work
- [ ] Consistent formatting
- [ ] Tables align properly

## Commit & PR

Use `git-workflow` skill for commits:

- **Commit type**: `docs`
- **Scope**: Optional (or target area: `btc`, `eth`, `standards`, etc.)

Example: `docs(standards): update coding conventions for error handling`

## Related

- `git-workflow` - Branch, commit, PR workflow
- [AGENTS.md](../../../AGENTS.md) - Agent entry point
- [AI Agent Instruction Design](../../../docs/design/ai-agents-instruction.md) - System design
- [Task Classification](../../../docs/standards/task-classification.md) - Label SSOT
