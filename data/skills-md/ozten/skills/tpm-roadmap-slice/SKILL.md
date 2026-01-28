---
name: tpm-roadmap-slice
description: Generate a Phase Spec/PRD by extracting features from an annotated Vision PRD. Use when user wants to create quarterly phase documentation, extract requirements from vision, plan a development phase, or decompose features into R-nnnn requirements. Requires annotated Vision PRD with F-nnn tags and Coverage Index.
---

# PRD Phase Generator

Extract features from a Vision PRD into a detailed Phase PRD with requirements, priorities, and traceability.

## Inputs Required

1. **Vision PRD** — Annotated with `[F-nnn]` tags (use `prd-vision-annotator` first if missing)
2. **Coverage Index** — To identify which features are `Planned` vs already assigned

## Capacity Defaults

Per phase, target approximately:
- **10 features** (F-nnn)
- **50 functional requirements** (R-nnnn)  
- **100 acceptance criteria** (AC-nnnn)

Adjust based on user input about team size or timeline.

## Workflow

1. **Select features** — Choose ~10 `Planned` features from Coverage Index
2. **Decompose requirements** — Extract R-nnnn from each feature's vision prose
3. **Assign priorities** — Must / Should / Could for each requirement
4. **Generate Phase PRD** — Using template in `assets/phase-prd-template.md`
5. **Update Coverage Index** — Mark selected features as `In Progress`

## Step 1: Feature Selection

Review `Planned` features in Coverage Index. Select based on:

- **Dependencies** — Foundation features before dependent ones
- **Cohesion** — Group related features (e.g., all calendar views together)
- **Business priority** — Per user input or stakeholder notes
- **Complexity** — Balance large and small features

Present selection to user for approval before proceeding.

## Step 2: Requirement Decomposition

For each selected feature, read the Vision PRD section and extract atomic requirements.

**Vision prose:**
> User selects quantity, enters name/email, receives confirmation email immediately.

**Becomes:**
```markdown
### R-0141: RSVP Quantity Selection
**Parent:** F-014
**Priority:** Must

Users shall select the number of seats when submitting an RSVP.

### R-0142: RSVP Data Collection  
**Parent:** F-014
**Priority:** Must

The RSVP form shall collect attendee name and email address.

### R-0143: RSVP Confirmation Email
**Parent:** F-014
**Priority:** Must

The system shall send a confirmation email upon RSVP submission.
```

**Decomposition guidelines:**
- One behavior per requirement
- Use "shall" for required behaviors
- Keep requirements testable and atomic
- ~5 requirements per feature is typical

## Step 3: Priority Assignment

| Priority | Meaning | Guidance |
|----------|---------|----------|
| **Must** | Required for phase to ship | Core functionality, blockers |
| **Should** | Expected but negotiable | Important but not critical |
| **Could** | Nice to have | Enhancements, polish |

Aim for roughly 60% Must, 30% Should, 10% Could.

## Step 4: Generate Phase PRD

Use template at `assets/phase-prd-template.md`. Structure:

1. Phase Overview (goals, scope, timeline)
2. Features in Scope (list with F-nnn)
3. Functional Requirements (R-nnnn grouped by feature)
4. Quality Requirements section (placeholder — populated by `prd-qa-enricher`)
5. Acceptance Criteria section (placeholder — populated by `prd-qa-enricher`)

## Requirement Numbering

Continue R-nnnn sequence across phases:
- Phase I: R-0001 → R-0089
- Phase II: R-0090 → R-0179
- Phase III: R-0180 → R-0269

Check previous Phase PRDs to find the last used R-nnnn.

## References

- `references/naming-conventions.md` — ID formats and rules
- `references/phasing-process.md` — Detailed extraction workflow
