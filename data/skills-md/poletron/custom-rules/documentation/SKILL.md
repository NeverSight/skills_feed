---
name: documentation
description: >
  Expert technical writing skill. Provides templates for PRD, BRD, SRS, and Engineering docs.
  Trigger: "Write a PRD", "Document this feature", "Create specs", "Generate readme".
license: Apache-2.0
metadata:
  author: poletron
  version: "1.0"
  scope: [root]
  auto_invoke: "Writing documentation, PRDs, specs, or requirements"
---

## When to Use

Use this skill when:
- Structuring requirements or specifications
- Documenting business goals or market analysis
- Creating product requirement documents
- Writing technical or architecture documentation

---

## Available Templates (in assets/)

| Category | Template | Purpose |
|----------|----------|---------|
| **Business** | `brd.md` | Business Requirements (Why) |
| **Business** | `mrd.md` | Market Requirements (Who) |
| **Product** | `prd.md` | Product Requirements (What/Vision) |
| **Specs** | `srs.md` | Software Requirements Specification |
| **Specs** | `frd.md` | Functional Requirements |
| **Specs** | `uird.md` | UI/UX Requirements |
| **Architecture** | `sad.md` | System Architecture Document |
| **Architecture** | `trd.md` | Technical Requirements |
| **Dev** | `api-ref.md` | API Reference Template |
| **Dev** | `changelog-entry.md` | Changelog Entry Format |
| **Dev** | `project-readme.md` | README Template |

---

## Decision Tree

```
Need business justification?   → Use brd.md
Need market analysis?          → Use mrd.md
Need product vision?           → Use prd.md
Need technical spec?           → Use srs.md
Need user flows?               → Use frd.md
Need UI guidelines?            → Use uird.md
Need system design?            → Use sad.md
Need infra/constraints?        → Use trd.md
Need API docs?                 → Use api-ref.md
Need version notes?            → Use changelog-entry.md
Need project intro?            → Use project-readme.md
```

---

## Workflow

1. **Identify** the document type needed from the table above
2. **Load** the corresponding template from `assets/`
3. **Interview** the user to fill in the `[Placeholders]`
4. **Generate** the filled document

---

## Resources

All templates are in [assets/](assets/).

---

## Detailed Guidelines & Templates

### 1. README Structure

#### Essential Sections (Priority Order)

| Section | Purpose |
|---------|---------|
| **Title + One-liner** | What is this? |
| **Quick Start** | Running in <5 min |
| **Features** | What can I do? |
| **Configuration** | How to customize |
| **API Reference** | Link to detailed docs |
| **Contributing** | How to help |
| **License** | Legal |

#### README Template

```markdown
# Project Name

Brief one-line description.

## Quick Start

[Minimum steps to run]

## Features

- Feature 1
- Feature 2

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| PORT | Server port | 3000 |

## Documentation

- [API Reference](./docs/api.md)
- [Architecture](./docs/architecture.md)

## License

MIT
```

### 2. API Documentation Structure

#### Per-Endpoint Template

```markdown
## GET /users/:id

Get a user by ID.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| id | string | Yes | User ID |

**Response:**
- 200: User object
- 404: User not found

**Example:**
[Request and response example]
```

### 3. Code Comment Guidelines

#### JSDoc/TSDoc Template

```typescript
/**
 * Brief description of what the function does.
 * 
 * @param paramName - Description of parameter
 * @returns Description of return value
 * @throws ErrorType - When this error occurs
 * 
 * @example
 * const result = functionName(input);
 */
```

#### When to Comment

| ✅ Comment | ❌ Don't Comment |
|-----------|-----------------|
| Why (business logic) | What (obvious) |
| Complex algorithms | Every line |
| Non-obvious behavior | Self-explanatory code |
| API contracts | Implementation details |

### 4. Changelog Template (Keep a Changelog)

```markdown
# Changelog

## [Unreleased]
### Added
- New feature

## [1.0.0] - 2025-01-01
### Added
- Initial release
### Changed
- Updated dependency
### Fixed
- Bug fix
```

### 5. Architecture Decision Record (ADR)

```markdown
# ADR-001: [Title]

## Status
Accepted / Deprecated / Superseded

## Context
Why are we making this decision?

## Decision
What did we decide?

## Consequences
What are the trade-offs?
```

### 6. AI-Friendly Documentation (2025)

#### llms.txt Template

For AI crawlers and agents:

```markdown
# Project Name
> One-line objective.

## Core Files
- [src/index.ts]: Main entry
- [src/api/]: API routes
- [docs/]: Documentation

## Key Concepts
- Concept 1: Brief explanation
- Concept 2: Brief explanation
```

#### MCP-Ready Documentation

For RAG indexing:
- Clear H1-H3 hierarchy
- JSON/YAML examples for data structures
- Mermaid diagrams for flows
- Self-contained sections
