---
name: spec-constitution
description: Create or update the project constitution with core principles and governance rules. Use when user says "/spec-constitution", "create constitution", "update principles", or needs project-wide development standards. Constitution is referenced by all other spec commands.
---

# Spec-Constitution

Create or update project constitution at `.specify/memory/constitution.md`.

**Prerequisites**: `.specify/` directory structure must exist.

## Workflow

1. **Load template** - Read `.specify/memory/constitution.md`
2. **Find placeholders** - Identify `[ALL_CAPS_IDENTIFIER]` tokens
3. **Collect values** - From user input or repo context
4. **Draft constitution** - Replace placeholders
5. **Propagate changes** - Update dependent templates
6. **Validate** - No unexplained placeholders
7. **Write file** - Save constitution
8. **Report** - Summary with commit suggestion

## Placeholders

| Token | Description |
|-------|-------------|
| `[PROJECT_NAME]` | Project identifier |
| `[PRINCIPLE_N_NAME]` | Principle titles |
| `[PRINCIPLE_N_DESCRIPTION]` | Principle details |
| `[CONSTITUTION_VERSION]` | MAJOR.MINOR.PATCH |
| `[RATIFICATION_DATE]` | YYYY-MM-DD |
| `[LAST_AMENDED_DATE]` | YYYY-MM-DD |

## Version Bumping

- **MAJOR**: Breaking governance changes
- **MINOR**: New principles/sections
- **PATCH**: Clarifications, typos

## Propagation Checklist

After updating constitution, check:
- `.specify/templates/plan-template.md`
- `.specify/templates/spec-template.md`
- `.specify/templates/tasks-template.md`
- README.md, quickstart.md

## Sync Report Format

```markdown
<!--
Version: 1.0.0 → 1.1.0
Modified: Old Title → New Title
Added: New Section
Templates: ✅ plan-template.md, ⚠ tasks-template.md
TODOs: TODO(RATIFICATION_DATE): Ask team
-->
```

## Next Steps

After `/spec-constitution`:
- `/spec-specify` - Create spec using new principles
