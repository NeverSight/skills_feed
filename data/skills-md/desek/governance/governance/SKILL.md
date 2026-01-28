---
name: governance
description: Creates Architecture Decision Records (ADRs) and Change Requests (CRs) for project governance. Activates on keywords like "ADR", "architecture decision", "CR", "change request", "governance", "technical decision", or "requirement change". Use for documenting technology choices, architectural patterns, or scope modifications.
metadata:
  author: desek
  version: "1.1"
---

# Governance Documentation

Creates and manages governance documents: ADRs for architectural decisions, CRs for requirement changes.

## Document Selection

| Need | Document | Guide |
|------|----------|-------|
| Technical/architectural decision | ADR | [reference/adr-guide.md](reference/adr-guide.md) |
| Requirement or scope change | CR | [reference/cr-guide.md](reference/cr-guide.md) |

## ADR Workflow

Use this checklist when creating an Architecture Decision Record:

```
- [ ] Read the template: templates/ADR.md
- [ ] Check docs/adr/ for the next available number
- [ ] Create file: docs/adr/ADR-NNNN-{short-title}.md
- [ ] Fill in all required sections
- [ ] Set status to "proposed"
```

**Strict requirements:**
- File naming: `ADR-NNNN-{title}.md` (four-digit number, lowercase, hyphens)
- Initial status: `proposed`
- Location: project's `docs/adr/` folder

**Flexible (adapt to context):**
- Level of detail in alternatives section
- Number of consequences listed
- Diagram inclusion (recommended for complex decisions)

## CR Workflow

Use this checklist when creating a Change Request:

```
- [ ] Read the template: templates/CR.md
- [ ] Check docs/cr/ for the next available number
- [ ] Create file: docs/cr/CR-NNNN-{short-title}.md
- [ ] Fill in all required sections
- [ ] Write acceptance criteria in Gherkin format
- [ ] Set status to "proposed"
```

**Strict requirements:**
- File naming: `CR-NNNN-{title}.md` (four-digit number, lowercase, hyphens)
- Initial status: `proposed`
- Location: project's `docs/cr/` folder
- Acceptance criteria: Gherkin format (Given-When-Then)
- Requirements keywords: RFC 2119 (MUST, SHOULD, MAY)

**Flexible (adapt to context):**
- Document length (minimum 250 lines for complex changes)
- Number of diagrams
- Depth of impact assessment

## Templates

- **ADR**: [templates/ADR.md](templates/ADR.md)
- **CR**: [templates/CR.md](templates/CR.md)

## Reference Guides

For detailed lifecycle information, best practices, and examples:

- **ADR Guide**: [reference/adr-guide.md](reference/adr-guide.md)
- **CR Guide**: [reference/cr-guide.md](reference/cr-guide.md)

## Commit Message Format

Committing governance documents is the human's responsibility. When ready to commit, use these formats:

- **ADR**: `docs(adr): add ADR-NNNN {title}`
- **CR**: `docs(cr): add CR-NNNN {title}`
