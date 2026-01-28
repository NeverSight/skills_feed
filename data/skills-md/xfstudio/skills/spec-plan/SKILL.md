---
name: spec-plan
description: Execute implementation planning workflow to generate design artifacts (research.md, data-model.md, contracts/, quickstart.md). Use when user says "/spec-plan", "create a plan", "plan the implementation" after /spec-specify or /spec-clarify.
---

# Spec-Plan

Generate implementation plan and design artifacts.

**Prerequisites**: Feature spec must exist.

## Workflow

1. **Setup** - Run `.specify/scripts/bash/setup-plan.sh --json`
2. **Load context** - Read spec.md and constitution.md
3. **Fill plan template** - Technical context, constitution check
4. **Phase 0: Research** - Generate research.md (resolve NEEDS CLARIFICATION)
5. **Phase 1: Design** - Generate data-model.md, contracts/, quickstart.md
6. **Update agent context** - Run `.specify/scripts/bash/update-agent-context.sh`
7. **Report** - Output plan path and artifacts

## Script Usage

```bash
.specify/scripts/bash/setup-plan.sh --json
```

Output: `{"FEATURE_SPEC":"...","IMPL_PLAN":"...","SPECS_DIR":"...","BRANCH":"..."}`

## Plan Template Sections

### Technical Context
```markdown
**Language/Version**: Python 3.11
**Primary Dependencies**: FastAPI, SQLAlchemy
**Storage**: PostgreSQL
**Testing**: pytest
**Target Platform**: Linux server
**Project Type**: web
```

### Constitution Check
- Validate against `.specify/memory/constitution.md`
- ERROR if violations unjustified

## Generated Artifacts

| File | Purpose |
|------|---------|
| `plan.md` | Technical context and structure |
| `research.md` | Decisions and alternatives |
| `data-model.md` | Entities and relationships |
| `contracts/` | API specifications |
| `quickstart.md` | Integration scenarios |

## Phase 0: Research

For each NEEDS CLARIFICATION:
1. Research the unknown
2. Document decision and rationale
3. List alternatives considered

## Phase 1: Design

1. Extract entities → `data-model.md`
2. Generate API contracts → `contracts/`
3. Create test scenarios → `quickstart.md`
4. Update agent context

## Next Steps

After `/spec-plan`:
- `/spec-tasks` - Generate task list
- `/spec-checklist` - Create validation checklist
