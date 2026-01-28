---
name: spec-checklist
description: Generate custom quality checklists that validate REQUIREMENTS quality (not implementation). Use when user says "/spec-checklist", "create checklist for [domain]" to validate specification completeness before implementation.
---

# Spec-Checklist

Generate checklists that validate requirements quality - "unit tests for specifications".

**Prerequisites**: Feature directory must exist.

## Core Concept

Checklists are **UNIT TESTS FOR REQUIREMENTS** - they validate the SPECIFICATION, not the implementation.

### Wrong (Testing Implementation)
- ❌ "Verify the button clicks correctly"
- ❌ "Test error handling works"

### Correct (Testing Requirements Quality)
- ✅ "Are hover state requirements defined for all interactive elements?"
- ✅ "Is 'prominent display' quantified with specific sizing?"
- ✅ "Are accessibility requirements specified for keyboard navigation?"

## Workflow

1. **Setup** - Run `.specify/scripts/bash/check-prerequisites.sh --json`
2. **Clarify intent** - Generate up to 3 contextual questions
3. **Load context** - spec.md, plan.md, tasks.md
4. **Generate checklist** - Create `FEATURE_DIR/checklists/[domain].md`
5. **Number items** - CHK001, CHK002...

## Checklist Categories

| Category | Question Pattern |
|----------|------------------|
| Completeness | "Are [requirements] defined for [scenario]?" |
| Clarity | "Is [vague term] quantified with specific criteria?" |
| Consistency | "Do [requirements] align across [contexts]?" |
| Measurability | "Can [criterion] be objectively verified?" |
| Coverage | "Are [scenario type] requirements addressed?" |

## Item Structure

```markdown
- [ ] CHK001 Are visual hierarchy requirements defined for all card types? [Completeness]
- [ ] CHK002 Is 'prominent display' quantified with sizing/positioning? [Clarity, Spec §FR-4]
- [ ] CHK003 Are hover states consistent across interactive elements? [Consistency]
```

### Traceability Markers
- `[Spec §X.Y]` - Reference to spec section
- `[Gap]` - Missing requirement
- `[Ambiguity]` - Unclear requirement
- `[Conflict]` - Contradicting requirements

## Prohibited Patterns

❌ Never use:
- "Verify", "Test", "Confirm" + implementation behavior
- "Displays correctly", "works properly"
- "Click", "navigate", "render", "load"

✅ Always use:
- "Are [requirements] defined/specified/documented?"
- "Is [term] quantified/clarified?"
- "Do [requirements] align/cover?"

## Content Rules

- Soft cap: 40 items max
- Merge near-duplicates
- ≥80% must have traceability reference

## Next Steps

After `/spec-checklist`:
- Review and complete checklist items
- `/spec-implement` - Execute with checklist validation
