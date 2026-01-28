---
name: sdlc-repository-templates
description: Templates, standards, and structure requirements for generating SDLC approach learning repositories. Use when creating new methodology learning repositories, artifact documentation, or validating repository structure.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# SDLC Repository Templates and Standards

## Purpose

This skill provides the complete template library and structural standards for generating comprehensive learning repositories for any SDLC approach (Agile, DDD, Structured Analysis, MBSE, Event-Driven, etc.).

## Repository Structure Pattern

```
{{DIRECTORY_NAME}}/
├── 01-{Phase_1_Name}/
│   ├── 01-{Artifact_1_Name}/
│   │   ├── README.md
│   │   └── examples/
│   │       ├── {example-1}.md
│   │       └── {example-2}.md
│   ├── 02-{Artifact_2_Name}/
│   │   ├── README.md
│   │   └── examples/
│   │       └── {example}.md
│   └── ...
├── 02-{Phase_2_Name}/
│   └── ...
├── README.md
├── {{APPROACH_ABBREV}}_Documents.md
└── tools/
    └── link_check.py
```

## Naming Conventions

### Phase Folders
- Format: `{NN}-{Phase_Name}/`
- NN = 01 to 99 (zero-padded)
- Phase_Name = Descriptive name with underscores (e.g., `01-Requirements_Gathering`)

### Artifact Folders
- Format: `{AA}-{Artifact_Name}/`
- AA = 01 to 99 (zero-padded, sequential within each phase)
- Artifact_Name = Descriptive name with underscores (e.g., `01-User_Stories`)

### Example Files
- Format: Lowercase with hyphens
- Examples: `user-story-template.md`, `backlog-prioritization.md`

### Artifact IDs
- Format: `PP-AA`
- PP = Phase number (01-99)
- AA = Artifact number within phase
- Used for traceability in master tracker

## Template: Artifact README.md

```markdown
# [Artifact Name]

## What this artifact is
[1-3 sentence definition of the artifact in the context of {{APPROACH_NAME}}]

## Intended audience and consumers
[Who creates it, who uses it, who reviews it]
Examples: Product Owner, Scrum Master, Development Team, Stakeholders, Architects, etc.

## Purpose and what it communicates
[Why this artifact exists, what decisions it enables, what problems it solves]

## What it is NOT intended to do
[Clear scope boundaries and anti-patterns to avoid over-engineering]

## When it is mandatory vs. optional (and why)
- **Mandatory when**: [Conditions where this artifact is required]
- **Optional when**: [Conditions where it can be skipped]
- **Rationale**: [Why the governance differs based on context]

## Inputs and upstream dependencies
[What information, artifacts, or activities must happen before this artifact can be created]
Examples:
- Requires: [Artifact ID PP-AA] - [Artifact Name]
- Informed by: [Stakeholder input, market research, etc.]

## Outputs and downstream consumers
[What artifacts, decisions, or activities depend on this artifact]
Examples:
- Feeds into: [Artifact ID PP-AA] - [Artifact Name]
- Enables: [Decision, activity, or workflow]

## Dependencies
[Cross-reference table of related artifacts with IDs]
| Dependency Type | Artifact ID | Artifact Name |
|-----------------|-------------|---------------|
| Prerequisites   | PP-AA       | [Name]        |
| Informs         | PP-AA       | [Name]        |
| Related         | PP-AA       | [Name]        |

## Success criteria and quality checks
[Checklist for "Definition of Done" - when is this artifact complete and usable?]
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Peer review completed]
- [ ] [Stakeholder approval obtained (if required)]

## Examples
See the [examples/](./examples/) folder for:
- [example-1.md](./examples/example-1.md) - [Brief description]
- [example-2.md](./examples/example-2.md) - [Brief description]
```

## Template: Main README.md

```markdown
# Learn {{APPROACH_NAME}}

A comprehensive, example-driven learning repository for **{{APPROACH_NAME}}** - a {{RIGOR_LEVEL}} rigor, {{FLEXIBILITY_LEVEL}} flexibility approach best suited for **{{BEST_FOR}}**.

## What is {{APPROACH_NAME}}?

[2-4 paragraph introduction to {{APPROACH_NAME}}]
- Core philosophy and principles
- When to use this approach
- Key differentiators from other approaches
- Reference to {{MAIN_REFERENCE_URL}}

## Repository Structure

This repository contains **{{TOTAL_ARTIFACTS}} artifacts** organized across **{{NUM_PHASES}} lifecycle phases**:

1. **Phase 01: {Phase_1_Name}** - [Brief description]
2. **Phase 02: {Phase_2_Name}** - [Brief description]
...
{{NUM_PHASES}}. **Phase {{NUM_PHASES}}: {Phase_N_Name}** - [Brief description]

Each artifact includes:
- **README.md**: Specification, purpose, audience, dependencies, success criteria
- **examples/**: Realistic examples using the **{{DOMAIN_EXAMPLE}}** domain

## How to Use This Repository

### For Learners
1. Start with [{{APPROACH_ABBREV}}_Documents.md](./{{APPROACH_ABBREV}}_Documents.md) for a complete artifact index
2. Follow the phases sequentially or jump to specific artifacts
3. Read the README for context, then study the examples
4. Trace dependencies to understand artifact relationships

### For Practitioners
- Use as a reference for deliverable templates
- Adapt examples to your own domain
- Use success criteria as quality gates
- Leverage dependency matrix for project planning

### For Teams
- Establish which artifacts are mandatory vs. optional for your project
- Customize examples to your specific context
- Use as onboarding material for new team members

## Example Domain: {{DOMAIN_EXAMPLE}}

All examples use a consistent **{{DOMAIN_EXAMPLE}}** domain to demonstrate cross-artifact traceability. This allows you to see how a single requirement flows through multiple lifecycle phases.

## Quality Validation

Run `tools/link_check.py` to validate:
- All internal links in {{APPROACH_ABBREV}}_Documents.md resolve correctly
- All example files exist and are accessible
- Cross-references between artifacts are valid

```bash
python tools/link_check.py
```

## Contributing

To add new artifacts or improve examples:
1. Follow the naming conventions in this README
2. Use the artifact README template from `.claude/skills/sdlc-repository-templates`
3. Ensure examples use the {{DOMAIN_EXAMPLE}} domain for consistency
4. Update {{APPROACH_ABBREV}}_Documents.md with new entries
5. Run link validation before submitting

## References

- Official Source: [{{MAIN_REFERENCE_URL}}]({{MAIN_REFERENCE_URL}})
- Rigor Level: {{RIGOR_LEVEL}}
- Flexibility: {{FLEXIBILITY_LEVEL}}
- Best For: {{BEST_FOR}}

## License

[Specify license - e.g., MIT, CC BY 4.0, etc.]
```

## Template: Master Tracker (_Documents.md)

```markdown
# {{APPROACH_NAME}} - Master Artifact Tracker

This document provides a complete index of all {{APPROACH_NAME}} artifacts organized by lifecycle phase.

## Quick Navigation
- [Phase 01: {Phase_1_Name}](#phase-01-phase_1_name)
- [Phase 02: {Phase_2_Name}](#phase-02-phase_2_name)
...

## Artifact Overview Table

| ID | Phase | Artifact | Folder | README | Example | Dependencies/Inputs |
|----|-------|----------|--------|--------|---------|---------------------|
| 01-01 | {Phase_1_Name} | {Artifact_1} | [01-{Phase_1}/01-{Artifact_1}/](./01-{Phase_1}/01-{Artifact_1}/) | ✅ | ✅ | — |
| 01-02 | {Phase_1_Name} | {Artifact_2} | [01-{Phase_1}/01-{Artifact_2}/](./01-{Phase_1}/01-{Artifact_2}/) | ✅ | ✅ | 01-01 |

## Phase Details

### Phase 01: {Phase_1_Name}

**Purpose**: [What this phase achieves in {{APPROACH_NAME}}]

**Artifacts**:
1. **[01-01] {Artifact_1_Name}** - [One-line description]
   - Examples: {example-1.md}, {example-2.md}
   - Dependencies: None
2. **[01-02] {Artifact_2_Name}** - [One-line description]
   - Examples: {example.md}
   - Dependencies: 01-01

## Dependency Matrix

| Artifact ID | Depends On | Feeds Into |
|-------------|------------|------------|
| 01-01       | —          | 01-02, 02-01 |
| 01-02       | 01-01      | 02-03 |

## Completion Status

- **Total Artifacts**: {{TOTAL_ARTIFACTS}}
- **READMEs Complete**: {{README_COUNT}}/{{TOTAL_ARTIFACTS}}
- **Examples Complete**: {{EXAMPLE_COUNT}}/{{TOTAL_ARTIFACTS}}
```

## Phase Definition Guidelines by Approach Type

### For Agile/Iterative
Phases: Discovery, Sprint Planning, Development Iteration, Review & Retrospective, Release, etc.
Artifacts: User Stories, Product Backlog, Sprint Backlog, Definition of Done, Burndown Charts

### For DDD (Domain-Driven Design)
Phases: Strategic Design, Bounded Context Mapping, Tactical Design, Domain Events, Implementation
Artifacts: Context Map, Ubiquitous Language, Aggregate Design, Domain Events Catalog

### For Structured Analysis
Phases: Requirements, Analysis, Design, Implementation, Testing, Deployment, Operations
Artifacts: DFDs, Data Dictionary, Process Specs, ERDs, Structure Charts

### For MBSE (Model-Based Systems Engineering)
Phases: Stakeholder Needs, Requirements Analysis, Logical Design, Physical Design, Verification
Artifacts: SysML Diagrams, Requirements Models, Interface Definitions

### For Event-Driven
Phases: Event Storming, Event Catalog, Schema Design, Consumer Design, Implementation
Artifacts: Event Map, Event Schemas, Consumer Contracts, Event Flows

## Example File Requirements

### Domain Consistency
- Use **{{DOMAIN_EXAMPLE}}** as the primary domain across all artifacts
- Creates cross-cutting comprehension (e.g., same user stories feed into same sprint plans)

### Realistic Scale
- Examples should be pedagogical (20-80 lines), not production-scale
- Show enough detail to be instructive
- Avoid overwhelming learners with complexity

### Traceability
Examples should reference:
- Upstream artifact IDs (e.g., "Based on User Story US-042 from 02-01")
- Requirement IDs, feature IDs, or other tracking identifiers
- Downstream consumers (e.g., "Feeds into Sprint Backlog 03-02")

### File Formats
- Primarily Markdown (.md) for textual artifacts
- Mermaid diagrams (.mmd or inline in .md) for visual models
- JSON/YAML for configuration examples
- Code snippets (.py, .js, .sql) where appropriate
- Screenshots or mockups (PNG/SVG) for UI artifacts

## Quality Criteria Checklist

✅ **Structure Consistency**: All phases and artifacts follow naming conventions
✅ **Template Adherence**: All READMEs use the standardized template
✅ **Domain Consistency**: All examples use {{DOMAIN_EXAMPLE}} domain
✅ **Traceability**: Dependencies clearly documented in master tracker
✅ **Completeness**: Every artifact has README + at least 1 example
✅ **Validation**: Link checker passes without errors
✅ **Alignment**: Content reflects {{RIGOR_LEVEL}} rigor and {{FLEXIBILITY_LEVEL}} flexibility
✅ **Authority**: Artifacts reference best practices from {{MAIN_REFERENCE_URL}}

## Best Practices

### When Creating Phases
1. Align with approach philosophy and methodology
2. Consider rigor level (more formal = more phases)
3. Consider flexibility (adaptive approaches may combine phases)
4. Typically 8-14 phases for comprehensive coverage

### When Defining Artifacts
1. Core deliverables only (3-11 per phase)
2. Industry-standard artifacts from authoritative sources
3. Appropriate to rigor level (formal approaches have more documentation)
4. Aligned with flexibility (adaptive approaches have lighter artifacts)

### When Writing Examples
1. Use consistent domain throughout repository
2. Include traceability IDs
3. Show realistic but not overwhelming detail
4. Reference upstream and downstream artifacts
5. Use proper file formats (markdown, mermaid, code)

## Common Pitfalls to Avoid

❌ **Inconsistent Naming**: Mixing underscores/hyphens, wrong padding
❌ **Template Deviation**: Skipping sections or using custom formats
❌ **Domain Switching**: Using different example domains across artifacts
❌ **Missing Traceability**: Not linking artifacts with IDs
❌ **Over-Engineering**: Production-scale examples that overwhelm learners
❌ **Under-Specification**: Examples too trivial to be instructive

## Related Skills

- `testing-conventions`: For creating test-related artifacts
- `api-standards`: For API design artifacts
- `deployment-process`: For deployment and operations artifacts
