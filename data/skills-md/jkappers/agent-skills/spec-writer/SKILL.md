---
name: spec-writer
description: Write feature specifications that capture requirements and acceptance criteria. Use when (1) writing a new feature spec, (2) documenting functional requirements, (3) defining acceptance criteria for a feature, (4) capturing design goals and constraints for planned work, or (5) structuring a product idea into a formal specification.
argument-hint: "[feature name or description]"
---

# Spec Writing

Capture WHAT and WHY. Never prescribe HOW.

When invoked with arguments, write a spec for: $ARGUMENTS

## Workflow

1. Gather context: Collect feature description, target users, problem statement, and constraints from user input or $ARGUMENTS. Ask clarifying questions for missing information.
2. Create directory: `specs/feature-name/`
3. Copy `assets/spec.md` to `specs/feature-name/README.md`
4. Complete every section from the Required Sections table below
5. Validate against the checklist before completing

## Required Sections

| Section | Content |
|---------|---------|
| Feature Overview | 2-3 paragraphs: what, who, problem solved |
| Success Criteria | Measurable outcomes defining "done" |
| Design Goals | Primary (must) and secondary (nice to have) |
| User Experience | 1-2 paragraphs: interaction, journey |
| Design Rationale | 1-2 paragraphs: why this approach, trade-offs |
| Constraints/Assumptions | Technical constraints, business assumptions |
| Functional Requirements | FR-N format, max 6-8, with acceptance criteria |
| Edge Cases | Unusual inputs, failure scenarios |

## Acceptance Criteria

```markdown
- [ ] Given [context], when [action], then [expected result]
```

Include 2-4 criteria per requirement: happy path + key failure cases.

## Scope Check

More than 6-8 requirements = feature too large. Split: identify 3-4 core requirements, flag rest for separate spec in "Scope Notes" section.

## Validation Checklist

- [ ] Single MVP focus (one deliverable)
- [ ] All requirements have testable criteria
- [ ] No TODO/TBD placeholders
- [ ] Edge cases documented

## Exclusions

A spec defines WHAT to build, not HOW to build it. Exclude:

- Implementation approach or technical strategy
- Architecture diagrams
- Code examples
- Database schemas
- API signatures
- Technology or framework choices
- Development estimates, timelines, or phase sections

## Supporting Files

- `assets/spec.md` - Spec template
- `references/spec-guide.md` - Extended guidance on ADRs and archival
