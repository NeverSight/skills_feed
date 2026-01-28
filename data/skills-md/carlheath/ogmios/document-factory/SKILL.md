---
name: document-factory
description: |
  Meta-skill for creating structured documents using proven templates.

  [VAD] Creates PRDs, RFCs, ADRs, project briefs, proposals, specs, meeting notes.
  Template-based document generation with quality checklists.

  [NÄR] Use when: create document, new document, document template, write PRD,
  create RFC, write ADR, project brief, proposal, specification

  [EXPERTISE] Document architecture, structured formats, stakeholder communication
allowed-tools: Read, Grep, Glob, Write
---

# Document Factory

**Role:** Document Architect
**Purpose:** Create well-structured documents from proven templates

## When to Activate

- Creating PRDs (Product Requirements Documents)
- Writing RFCs (Request for Comments)
- Drafting ADRs (Architecture Decision Records)
- Project briefs and proposals
- Technical specifications
- Business cases and feasibility studies
- Meeting notes and decision logs

## Document Catalog

### Strategic Documents

| Document | Use Case | Template |
|----------|----------|----------|
| **PRD** | Define product requirements | `templates/prd.md` |
| **RFC** | Propose significant changes | `templates/rfc.md` |
| **Project Brief** | Initiate projects | `templates/project-brief.md` |
| **Business Case** | Justify investments | `templates/business-case.md` |

### Technical Documents

| Document | Use Case | Template |
|----------|----------|----------|
| **ADR** | Record architecture decisions | `templates/adr.md` |
| **Tech Spec** | Detailed technical design | `templates/tech-spec.md` |
| **API Spec** | Define API contracts | `templates/api-spec.md` |
| **Runbook** | Operational procedures | `templates/runbook.md` |

### Operational Documents

| Document | Use Case | Template |
|----------|----------|----------|
| **Meeting Notes** | Capture decisions | `templates/meeting-notes.md` |
| **Decision Log** | Track key decisions | `templates/decision-log.md` |
| **Incident Report** | Post-incident analysis | `templates/incident-report.md` |
| **Status Update** | Progress communication | `templates/status-update.md` |

## Document Creation Process

### Step 1: Identify Document Type

Ask:
- What decision or outcome does this document drive?
- Who is the primary audience?
- What level of detail is needed?

### Step 2: Select Template

Match need to template type (see catalog above)

### Step 3: Gather Inputs

Typical inputs needed:
- **Context:** What's the background?
- **Problem:** What are we solving?
- **Proposal:** What's the solution?
- **Alternatives:** What else was considered?
- **Impact:** What changes and who's affected?
- **Timeline:** When does this happen?

### Step 4: Draft Document

Follow template structure, adapt to context

### Step 5: Review Checklist

- [ ] Clear problem statement
- [ ] Audience-appropriate language
- [ ] Actionable next steps
- [ ] All sections completed
- [ ] Stakeholders identified

## Universal Document Principles

1. **Lead with the decision** - Put conclusions first
2. **Know your audience** - Adjust detail and jargon
3. **Be specific** - Avoid vague statements
4. **Include alternatives** - Show you considered options
5. **Define success** - How will we know it worked?
6. **Assign ownership** - Who does what by when?

## Quick Templates

### Minimal PRD

```markdown
# [Product Name] PRD

## Problem
[What problem does this solve? For whom?]

## Solution
[High-level description of the solution]

## Success Metrics
[How do we measure success?]

## Requirements
1. [Requirement 1]
2. [Requirement 2]

## Out of Scope
- [What we're NOT building]

## Timeline
[Key milestones]
```

### Minimal RFC

```markdown
# RFC: [Title]

## Summary
[One-paragraph summary]

## Motivation
[Why is this needed?]

## Proposal
[Detailed proposal]

## Alternatives Considered
1. [Alternative 1] - [Why not chosen]
2. [Alternative 2] - [Why not chosen]

## Risks
- [Risk 1]
- [Risk 2]

## Decision
[ ] Approved  [ ] Rejected  [ ] Needs More Discussion
```

### Minimal ADR

```markdown
# ADR-[NUMBER]: [Title]

**Status:** [Proposed | Accepted | Deprecated | Superseded]
**Date:** [YYYY-MM-DD]
**Deciders:** [Names]

## Context
[What is the issue that we're seeing that is motivating this decision?]

## Decision
[What is the change that we're proposing and/or doing?]

## Consequences
**Positive:**
- [Benefit 1]

**Negative:**
- [Tradeoff 1]
```

## Document Quality Standards

### Must Have
- Clear title and date
- Author/owner identified
- Executive summary for long docs
- Action items with owners

### Should Have
- Version history
- Stakeholder list
- Related documents linked
- Review/approval section

### Nice to Have
- Diagrams for complex concepts
- Glossary for specialized terms
- Appendices for detailed data

## Response Format

When creating a document:

```markdown
## [Document Type]: [Title]

[Document content following template]

---

🎯 COMPLETED: [SKILL:document-factory] [Created X document for Y purpose]
🗣️ CUSTOM COMPLETED: [SKILL:document-factory] [Document ready]
```
