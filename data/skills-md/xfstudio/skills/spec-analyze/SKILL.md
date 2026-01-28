---
name: spec-analyze
description: Perform non-destructive cross-artifact consistency and quality analysis across spec.md, plan.md, and tasks.md. Use when user says "/spec-analyze", "analyze the spec", "check consistency" after /spec-tasks to identify issues before implementation.
---

# Spec-Analyze

Cross-artifact consistency analysis - READ-ONLY, no file modifications.

**Prerequisites**: tasks.md must exist (run `/spec-tasks` first).

## Workflow

1. **Initialize** - Run `.specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks`
2. **Load artifacts** - spec.md, plan.md, tasks.md, constitution.md
3. **Build semantic models** - Requirements inventory, task mapping
4. **Detection passes** - 6 analysis categories
5. **Assign severity** - CRITICAL/HIGH/MEDIUM/LOW
6. **Produce report** - Markdown table with findings
7. **Offer remediation** - Ask before any edits

## Detection Categories

### A. Duplication Detection
- Near-duplicate requirements
- Mark lower-quality for consolidation

### B. Ambiguity Detection
- Vague adjectives (fast, scalable, intuitive)
- Unresolved placeholders (TODO, ???)

### C. Underspecification
- Verbs without measurable outcomes
- Missing acceptance criteria
- Tasks referencing undefined components

### D. Constitution Alignment
- MUST principle violations → CRITICAL
- Missing mandated sections

### E. Coverage Gaps
- Requirements with zero tasks
- Tasks with no mapped requirement
- Non-functional requirements not in tasks

### F. Inconsistency
- Terminology drift
- Missing data entities
- Task ordering contradictions
- Conflicting requirements

## Severity Levels

| Level | Criteria |
|-------|----------|
| CRITICAL | Constitution violation, missing core artifact, baseline blocker |
| HIGH | Duplicate/conflicting requirement, untestable criterion |
| MEDIUM | Terminology drift, missing NFR coverage |
| LOW | Style/wording, minor redundancy |

## Report Format

```markdown
## Specification Analysis Report

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| A1 | Duplication | HIGH | spec.md:L120 | Similar requirements | Merge phrasing |

**Coverage Summary:**
| Requirement | Has Task? | Task IDs |
|-------------|-----------|----------|

**Metrics:**
- Total Requirements: X
- Coverage %: Y%
- Critical Issues: Z
```

## Operating Constraints

- **STRICTLY READ-ONLY** - No file modifications
- **Constitution is non-negotiable** - Violations are CRITICAL
- Max 50 findings (aggregate overflow)
- Deterministic results on rerun

## Next Actions

- CRITICAL issues → Resolve before `/spec-implement`
- LOW/MEDIUM only → May proceed with suggestions

## Next Steps

After `/spec-analyze`:
- Fix identified issues
- `/spec-implement` - Execute implementation
