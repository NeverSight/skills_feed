---
name: planning-validate
description: >
  Validates planning artifacts (spec.md, plan.md, data-model.md, contracts/) for quality,
  completeness, and consistency. Checks for mandatory sections, cross-artifact consistency,
  and constitution compliance. Always run after /speckit.plan completes.
version: 0.0.1
license: MIT
compatibility: Requires spec kit with check-prerequisites.sh
metadata:
  author: drillan
  category: quality-gate
  repository: https://github.com/drillan/speckit-gates
---

# planning-validate

Validates planning artifacts for quality and consistency after `/speckit.plan` completes.

## Purpose

This skill automatically validates your planning artifacts to catch specification gaps before task generation. It checks:

- **spec.md completeness**: All mandatory sections present with content
- **plan.md executability**: Technical context, project structure, and constitution check completed
- **data-model.md consistency**: Entities align with spec requirements (if exists)
- **Contract coverage**: API contracts defined for required endpoints (if contracts/ exists)
- **Constitution compliance**: Plan follows project constitution rules (if constitution.md exists)

## Output

The skill outputs a **Quality Assessment** with:

- **GREEN**: All checks pass - proceed to `/speckit.tasks`
- **YELLOW**: Minor warnings - review but can proceed
- **RED**: Blockers found - must resolve before proceeding

## Usage

This skill runs automatically after `/speckit.plan`. You can also run it manually:

```bash
npx skills run planning-validate
```

## Exit Codes

| Code | Status | Meaning |
|------|--------|---------|
| 0 | GREEN | All checks pass |
| 1 | YELLOW | Warnings present |
| 2 | RED | Blockers present |
| 3 | Error | Required files missing |

## Checks Performed

### spec.md Checks

1. File exists and is readable
2. Summary section present with content
3. User Stories section present with at least one story
4. Functional Requirements section present with FR-XXX items
5. Success Criteria section present

### plan.md Checks

1. File exists and is readable
2. Technical Context section present
3. Project Structure section present
4. Constitution Check section present (unless skipped)
5. Gate Result shows PASS status

### data-model.md Checks (if exists)

1. Entities section present
2. At least one entity defined
3. Entity names are consistent with spec.md terminology

### contracts/ Checks (if exists)

1. At least one contract file present
2. Contract files are valid markdown
3. Contract endpoints match spec.md requirements

### constitution.md Checks (if exists)

1. Plan.md references constitution principles
2. No constitution violations in Gate Result

## Blocker Examples

- "spec.md: Missing User Stories section"
- "plan.md: Constitution Check section shows FAIL status"
- "data-model.md: Entity 'UserAccount' not referenced in spec.md"

## Recommendations

After receiving a RED or YELLOW status:

1. Review the specific blockers or warnings listed
2. Update the affected artifacts to address issues
3. Re-run `/speckit.plan` to regenerate plan.md
4. Run `planning-validate` again to verify fixes
