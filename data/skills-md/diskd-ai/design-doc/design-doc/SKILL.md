---
name: design-doc
description: Create technical design documents for new features, systems, refactoring plans, API designs, and database schemas. Use when asked to write a design doc, TRD (technical requirements document), RFC, or system design document. Triggers on requests like "write a design doc for X", "design the Y feature", "create a technical spec", or "plan the architecture for Z".
---

# Technical Design Document Skill

Create structured technical design documents that communicate system behavior, implementation approach, and acceptance criteria.

## Workflow

1. **Gather context**: Understand the feature/system scope, constraints, and goals
2. **Draft structure**: Use template from `references/template.md`
3. **Fill sections**: Work through each section, asking clarifying questions as needed
4. **Review**: Ensure acceptance criteria are testable and implementation outline is actionable

## Template

See `references/template.md` for the full template structure and section guidelines.

Core sections:
- **Context and motivation**: Problem statement, goals, non-goals
- **Implementation considerations**: Constraints and design principles
- **High-level behavior**: End-to-end system behavior
- **Domain-specific sections**: Adapt to feature type (discovery, validation, API, state, rendering)
- **Error handling and UX**: Error surfacing and recovery
- **Future-proofing**: Design for extensibility
- **Implementation outline**: Step-by-step approach
- **Testing approach**: Unit, integration, manual tests
- **Acceptance criteria**: Testable conditions for "done"

## Writing Guidelines

- Use `---` underlines for section headers (Setext style)
- Write in present tense for behavior ("loads", "validates", "returns")
- Be specific: "max 100 chars" not "reasonable length"
- Include concrete examples where behavior varies
- Non-goals are as important as goals - prevent scope creep
- Acceptance criteria must be verifiable, not subjective
