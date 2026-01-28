---
name: dev-specs
description: Generate lean implementation specifications from BRD use cases
version: 2.0.1
---

# /dev-specs - Lean Implementation Specifications

> **Skill Awareness**: See `skills/_registry.md` for all available skills.
> - **Before**: Ensure `/debrief` completed (BRD exists)
> - **Auto**: Runs `/dev-scout` if `tech-context.md` missing
> - **During**: Calls `/dev-arch` for patterns
> - **Reads**: `_quality-attributes.md` (Specification Level)
> - **After**: Use `/dev-coding` for implementation

Generate **lean, requirements-focused** specs from BRD use cases. Focuses on WHAT to build, not HOW.

## When to Use

- After `/debrief` created BRD use cases
- Before starting implementation
- When onboarding engineers to a feature

## Usage

```
/dev-specs auth                              # Generate specs for auth feature
/dev-specs auth UC-AUTH-001                  # Single use case only
/dev-specs billing --api=swagger.json        # With API spec file
/dev-specs payments --schema=schema.prisma   # With DB schema
```

## Core Rule: WHAT, Not HOW

Specs define **requirements and constraints**, not implementation details.

**Include:**
- Requirements (testable, bulleted)
- Technical constraints (stack, location, patterns)
- Acceptance criteria (testable outcomes)
- File checklist (where to work)

**Exclude:**
- Pseudocode (gets stale)
- Detailed implementation (discovered during coding)
- Code examples (reference existing patterns instead)

## Prerequisites

1. `plans/brd/` exists with use cases
2. `plans/features/{feature}/` exists
3. `plans/brd/tech-context.md` exists (auto-runs scout if missing)

## Output Structure

```
plans/features/{feature}/
├── codebase-context.md          # From /dev-scout
└── specs/
    ├── README.md                # Index, implementation order
    ├── shared/                  # Shared across UCs
    │   ├── data-model.md
    │   ├── patterns.md
    │   └── security.md
    └── UC-XXX-001-slug.md       # Lean spec per UC (~150 lines)
```

## Expected Outcome

**Lean specs** (~150 lines per UC) that define **WHAT to build**, not HOW.

**Output structure:**
```
plans/features/{feature}/
├── codebase-context.md          # From /dev-scout
└── specs/
    ├── README.md                # Index, implementation order
    ├── shared/                  # Shared across UCs
    │   ├── data-model.md
    │   ├── patterns.md
    │   └── security.md
    └── UC-XXX-001-slug.md       # Lean spec per UC
```

**Each UC spec includes:**
- **Requirements** - WHAT to achieve (testable outcomes)
- **Acceptance Criteria** - HOW to verify it works
- **Technical Constraints** - Stack patterns to use (reference tech-context.md)
- **Work Area** - General location (e.g., "auth feature area", NOT specific files)
- **API Contract** - If external interface
- **Dependencies** - What must exist first

**Each UC spec does NOT include:**
- ❌ Specific file names to create/modify
- ❌ DO/DON'T implementation lists
- ❌ Pseudocode or step-by-step instructions
- ❌ "How to code" details

**Engineer figures out:** File names, implementation approach, code structure

## Success Criteria

- Engineer knows WHAT to build
- Engineer knows WHERE to build it (file checklist)
- Engineer can verify success (acceptance criteria)
- Specs reference existing patterns, don't rewrite them
- Stack-aware (uses tech-context.md patterns)
- ~150 lines per UC spec max

## Prerequisites

Auto-checked and resolved:
1. `plans/brd/` exists with use cases
2. `plans/features/{feature}/` exists
3. `plans/brd/tech-context.md` exists (auto-runs project scout if missing)
4. `plans/features/{feature}/codebase-context.md` exists (auto-runs feature scout if missing)

## Context Sources

**Read these to understand HOW:**
- `tech-context.md` - Project patterns (API, data, structure)
- `codebase-context.md` - Feature-specific implementation
- `architecture.md` - Architecture decisions (call `/dev-arch` if missing)
- `_quality-attributes.md` - Specification Level checklist

**Read these to understand WHAT:**
- `plans/brd/use-cases/{feature}/*.md` - Business requirements
- `plans/docs-graph.json` - Dependencies between UCs

## Scope Inference

**Analyze UC to determine what's needed** (don't ask user):

From UC content, infer:
- **UI needed?** → UC mentions forms, pages, views, user sees/clicks/enters
- **API needed?** → UC mentions data operations, persistence, validation
- **Both?** → Full-stack (most common)
- **Testing level** → From `_quality-attributes.md` or project standards

**Example:**
- UC: "User can login via email/password form" → Full-stack (form + API + validation)
- UC: "System sends daily report email" → Backend only (cron job + email service)
- UC: "User sees loading spinner during API calls" → Frontend only (UI state)

**Only ask user for additional context if helpful:**
- API specs (Swagger, OpenAPI) if integrating external API
- Design files (Figma) if complex UI
- DB schema if existing database

## Impact Analysis

For each UC, identify:
- What's new? (files to create)
- What changes? (files to modify)
- What's shared? (reusable across UCs → specs/shared/)
- Dependencies? (what must exist first)

## Shared Specs

Create `specs/shared/` for cross-UC concerns:
- `data-model.md` - Schema changes, entities, relationships
- `patterns.md` - Pattern references (not pseudocode)
- `security.md` - Auth, permissions, validation rules

## Index Generation

Create `specs/README.md` with:
- Implementation order
- Dependencies between specs
- Quick reference to all UCs

## Stack Awareness

Specs **must** read `tech-context.md` to know the right approach:

| Stack Aspect | Spec Impact |
|--------------|-------------|
| BaaS (Directus) | Use collections, not tables |
| Composables | New API calls in composables/ |
| Zod | Schemas in shared/schemas/ |
| Server Actions | Use 'use server', not API routes |

**Example:**
```markdown
## Technical Constraints
- Use existing `useUserProfile` composable
- Follow VeeValidate + Zod pattern from auth forms
- Profile fields exist in Directus users collection
```

## Spec Format

See `references/spec-template.md` for structure.

**Max:** ~150 lines per UC
**Focus:** Requirements + acceptance criteria
**No:** Pseudocode or detailed HOW

## Tools

| Tool | Purpose |
|------|---------|
| `Read` | BRD, tech-context, codebase-context, architecture |
| `Glob` | Find related files |
| `Write` | Create spec files |
| `AskUserQuestion` | Ask for additional context (API specs, design files) if needed |
| `Context7` | Look up API/library patterns |

## Philosophy

Specs are **contracts**, not **pseudocode**.
- Define WHAT (requirements)
- Reference HOW (existing patterns)
- Implementation discovers details fresh during `/dev-coding`

## Anti-Patterns

❌ Writing 500+ line implementation plans
❌ Including pseudocode that gets stale
❌ Rewriting existing patterns
❌ Over-specifying implementation details
❌ Ignoring tech-context.md (suggests wrong approach)

## Reference

See `references/spec-template.md` for output structure (principle + empty template).
