---
name: spec-writing
description: Use when the user wants to create project specs, design systems, or feature plans. Triggers on "create spec", "plan project", "design system", "plan feature", or "write specification".
version: 3.0.0
---

# Spec Writing v3.0

Generate comprehensive project specifications with SPEC.md as the core file and optional supplements for reference material.

## Core Principle

**SPEC.md is always the complete spec. SPEC/ files are optional lookup supplements.**

```
SPEC.md               # Always created, always self-sufficient
CLAUDE.md             # Generated with spec references

SPEC/                 # Optional, created when user agrees
├── api-reference.md  # Lookup: endpoint schemas, request/response
├── sdk-patterns.md   # Lookup: external SDK usage patterns
└── data-models.md    # Lookup: complex entity schemas
```

Key distinction:
- **SPEC.md** = Things you READ (narrative, decisions, requirements)
- **SPEC/*.md** = Things you LOOK UP (schemas, SDK patterns, external API details)

## Single Adaptive Flow

One interview flow replaces previous Quick/SPEC/DEEP modes:

```
Interview starts
    ↓
Build SPEC.md progressively
    ↓
Hit reference-heavy topic? ──→ Ask: "Create SPEC/[topic].md for lookup?"
    ↓                                    ↓
Continue interview                  User decides (yes/no)
    ↓
Generate SPEC.md + CLAUDE.md
    ↓
If user said yes → Generate SPEC/[topic].md files
```

## Interview Workflow

### Phase 1: Vision & Problem
- Problem statement
- Target users
- Success criteria

### Phase 2: Requirements
- MVP features (must-have)
- Out of scope (explicit)
- User flows

### Phase 3: Architecture
- System type detection
- Architecture pattern (present 2-3 alternatives with tradeoffs)
- Tech stack with recommendations

### Phase 4: Tech Stack Details
- Frontend (if applicable)
- Backend (if applicable)
- Database (if applicable)
- Use multiple choice with recommendations

### Phase 5: Design & Security
- Visual design (if frontend)
- Authentication approach
- Constraints & compliance

### Supplement Prompts (Mid-Interview)

When hitting reference-heavy topics, ask:

> "Your API has 15 endpoints with detailed schemas. Should I:
> - A) Keep it inline in SPEC.md (shorter reference section)
> - B) Create SPEC/api-reference.md as a separate lookup file"

Create supplements only for:
- **Reference material** - Stuff you look up, not read through
- **External dependencies** - SDK docs, library patterns, third-party APIs

## Opinionated Recommendations

Lead with recommended options, allow override:

```
Which package manager?

- A) bun (Recommended) - Fastest, built-in test runner, drop-in npm replacement
- B) pnpm - Fast, strict dependency resolution, good for monorepos
- C) npm - Universal compatibility, no setup needed
- D) yarn - If team already uses it
```

Principles:
1. Lead with recommended option + brief rationale
2. Context-aware (desktop app? acknowledge Tauri vs Electron tradeoffs)
3. Acknowledge "it depends" cases (team familiarity, existing codebase)
4. Stay current with ecosystem changes

## SPEC.md Structure

```markdown
# [Project Name]

## Overview
Problem, solution, target users, success criteria.

## Product Requirements
Core features (MVP), future scope, out of scope, user flows.

## Technical Architecture
Tech stack (with rationale), system design diagram, data models, API endpoints.

## System Maps
- Architecture diagram (ASCII)
- Data model relations
- User flow diagrams
- Wireframes (key screens)

## Design System
(If frontend) Colors, typography, components, accessibility.

## File Structure
Project directory layout.

## Development Phases
Phased implementation plan with checkboxes.

## Open Questions
Decisions to make during development.

---

## References
(If supplements exist) Trigger-based links to SPEC/ files.
```

## Connecting SPEC.md to Supplements

When supplements exist, reference them with triggers:

**Inline (in relevant sections):**
```markdown
## API Design

**Endpoints overview:**
- `POST /auth/login` - User authentication
- `GET /projects` - List user projects

→ When implementing endpoints, reference `SPEC/api-reference.md` for full request/response schemas.
```

**References section (bottom):**
```markdown
---

## References

→ When implementing API endpoints: `SPEC/api-reference.md`
→ When using Anthropic SDK: `SPEC/sdk-patterns.md`
```

## CLAUDE.md Generation

Agent-optimized pointer file:

```markdown
# [Project Name]

[One-line description]

## Spec Reference

Primary spec: `SPEC.md`

→ When implementing API endpoints: `SPEC/api-reference.md`
→ When using [SDK/Library]: `SPEC/sdk-patterns.md`

## Key Constraints

- [Critical constraint 1 - surfaced from spec]
- [Critical constraint 2]
- [Out of scope reminder]

## Commands

- `[package-manager] run dev` - Start development
- `[package-manager] run test` - Run tests
- `[package-manager] run build` - Production build

## Current Status

→ Check `SPEC.md` → Development Phases section
```

Principles:
- Surface critical constraints directly (prevent missed context)
- Trigger-based supplement references
- Short - pointer, not duplication
- Status points to SPEC.md (single source)

## Context7 Integration

After tech choices, fetch relevant documentation:

```
1. resolve-library-id for each technology
2. query-docs for setup guides and patterns
3. Include insights in relevant spec files
```

## Best Practices

### Interview Conduct

- **Multiple choice**: Use AskUserQuestion options, not open-ended text
- **2-3 alternatives**: For key decisions, show options with tradeoffs
- **YAGNI**: Ruthlessly simplify - "Do we really need this for MVP?"
- **Supplements on demand**: Only offer when content is truly reference-heavy

### Output Quality

- Be specific and actionable
- Include code examples for data models
- Reference Context7 documentation
- Keep scope realistic for MVP
- Include system maps (architecture, data relations, user flows)

## Reference Files

### Templates
- `references/output-template.md` - SPEC.md structure
- `templates/index.template.md`
- `templates/overview.template.md`
- `templates/architecture.template.md`
- `templates/frontend.template.md`
- `templates/backend.template.md`
- `templates/design-system.template.md`
- `templates/api-reference.template.md`
- `templates/cli-reference.template.md`
- `templates/data-models.template.md`
- `templates/security.template.md`

### References
- `references/interview-questions.md` - Question bank with recommendations
- `references/spec-folder-template.md` - Supplement structure guide

### Examples
- `examples/web-app-spec.md`
- `examples/cli-spec.md`
- `examples/api-spec.md`
- `examples/library-spec.md`

## Related Commands

- `/spec` - Generate project specification
- `/feature` - Generate feature specification
- `/design` - Generate design system specification
- `/sync` - Sync spec with codebase changes (git-aware)

## Integration with Other Skills

### feature-dev

After creating specs, use feature-dev agents:
1. `code-explorer` - Analyze existing patterns
2. `code-architect` - Design implementation
3. `code-reviewer` - Review implementation

### frontend-design

Use design specs to implement components following the specification.
