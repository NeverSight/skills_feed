---
name: doc-ref
description: Create Reference Documents (REF) - supplementary documentation that doesn't participate in formal traceability chain
tags:
  - sdd-workflow
  - supplementary-documentation
  - shared-architecture
  - required-both-approaches
custom_fields:
  layer: "N/A"
  artifact_type: REF
  architecture_approaches: [ai-agent-based, traditional-8layer]
  priority: shared
  development_status: active
  skill_category: utility
  upstream_artifacts: [BRD, ADR]
  downstream_artifacts: []
  valid_parent_types: [BRD, ADR]
---

# doc-ref

## Purpose

Create **Reference Documents (REF)** - supplementary documentation for BRD and ADR artifact types in the SDD framework. REF documents provide supporting information without participating in the formal traceability chain.

**Layer**: Not applicable (supplementary to any layer)

**Traceability**: Optional (encouraged but not required)

**Validation**: Minimal (non-blocking)

## Naming Convention

**Format**: `{TYPE}-REF-DOC_NUM_{slug}.md`

| Component | Description | Example |
|-----------|-------------|---------|
| `{TYPE}` | Parent artifact type | **BRD or ADR only** |
| `REF` | Reference document indicator | REF |
| `DOC_NUM` | Variable-length sequence (2+ digits) | 01, 02, 100, 1000 |
| `{slug}` | Descriptive slug (snake_case) | project_overview |

**Scope**: REF documents are LIMITED to **BRD and ADR artifact types ONLY**.

**Examples**:
- `BRD-REF-01_project_overview.md` - Business context
- `BRD-REF-02_strategic_vision.md` - Strategic vision
- `ADR-REF-01_technology_stack_summary.md` - Tech overview
- `ADR-REF-02_infrastructure_guide.md` - Infrastructure reference

**Numbering**: Independent sequence per parent TYPE (variable-length: 01-99, 100-999, 1000+)
- BRD-REF-01, BRD-REF-02 (BRD sequence)
- ADR-REF-01, ADR-REF-02 (ADR sequence - separate from BRD)

**Location**: Within parent TYPE directory
- `docs/BRD/BRD-REF-01_project_overview.md`
- `docs/ADR/ADR-REF-01_technology_stack_summary.md`

## When to Use This Skill

Use `doc-ref` when creating supplementary documentation that:

- **BRD-REF**: Project overviews, executive summaries, strategic vision, stakeholder guides
- **ADR-REF**: Technology stack summaries, architecture overviews, infrastructure guides

**Do NOT use `doc-ref` for**:
- Documents that should participate in traceability chain
- Core artifacts (BRD, PRD, REQ, ADR, SPEC, etc.)
- Documents requiring validation gates
- **Any parent type other than BRD or ADR** (REF is limited to these two types)

## Template Reference

**Template**: `ai_dev_flow/REF-TEMPLATE.md`

### Required Sections (4 Mandatory)

1. **YAML Frontmatter** - Metadata with `artifact_type: REF`
2. **Document Control** - Version, date, author, status
3. **Document Revision History** - Change tracking
4. **Introduction** - Purpose and scope

### Optional Sections

- **Related Documents** - Cross-references (traceability encouraged)
- **Content sections** - As needed for the specific reference material

## Creation Process

### Step 1: Determine Parent Type

Identify which artifact type this reference document supports (**BRD or ADR only**):
- Business context → BRD-REF-NN
- Architecture context → ADR-REF-NN

### Step 2: Check Existing REF Documents

```bash
# List existing REF documents for the parent type
ls docs/BRD/*-REF-*.md 2>/dev/null    # For BRD references
ls docs/ADR/*-REF-*.md 2>/dev/null    # For ADR references
```

### Step 3: Allocate Next Number

```bash
# Find highest REF number for parent type
ls docs/BRD/*-REF-*.md 2>/dev/null | sort -V | tail -1
```

**ID Numbering Convention**: Start with 2 digits and expand only as needed.
- ✅ Correct: BRD-REF-01, ADR-REF-99, BRD-REF-102
- ❌ Incorrect: BRD-REF-001, ADR-REF-009 (extra leading zero not required)

### Step 4: Create Document

1. Copy template: `ai_dev_flow/REF-TEMPLATE.md`
2. Rename to: `{TYPE}-REF-NN_{slug}.md` (NN = next sequence number, 2+ digits)
3. Update H1 heading: `# {TYPE}-REF-NN: [Document Title]`
4. Fill Document Control section
5. Write Introduction
6. Add content sections as needed
7. [Optional] Add Related Documents section

### Step 5: Place Document

Save in parent TYPE directory:
```
docs/{TYPE}/{TYPE}-REF-NN_{slug}.md
```

## Element IDs (Not Applicable)

REF documents are **free-format supplementary documents** and do NOT use element IDs:

- **No element type codes** (01-31 codes from ID_NAMING_STANDARDS.md do not apply)
- **No sub-element IDs** (no `TYPE.NN.TT.SS` pattern)
- Content sections can be organized freely without formal ID structure

**Rationale**: REF documents serve as reference targets that other documents link to. They provide supporting information but do not define formal requirements or architecture decisions requiring element-level traceability.

## Validation Rules

### Required (Blocking)

| Check | Description |
|-------|-------------|
| H1 ID Match | H1 must match pattern `{TYPE}-REF-NN: Title` |
| Document Control | Must have Document Control section |
| Revision History | Must have Document Revision History |
| Introduction | Must have Introduction section |

### Exempted (Not Checked)

| Check | Reason |
|-------|--------|
| Cumulative Tags | REF docs don't participate in traceability chain |
| Full Traceability | Traceability is optional |
| Quality Gates | Non-blocking validation |
| SPEC-Ready Score | Not applicable |

## Common Use Cases

### 1. Project Overview (BRD-REF)

General project description for stakeholders:
```markdown
# BRD-REF-01: Project Overview

## Document Control
...

## 1. Introduction

This document provides a high-level overview of the project for stakeholder reference...
```

### 2. Strategic Vision (BRD-REF)

Strategic roadmap and vision:
```markdown
# BRD-REF-02: Strategic Vision

## Document Control
...

## 1. Introduction

This document outlines the strategic vision and roadmap for the project...
```

### 3. Technology Summary (ADR-REF)

Consolidated architecture reference:
```markdown
# ADR-REF-01: Technology Stack Summary

## Document Control
...

## 1. Introduction

This document summarizes the technology decisions documented across ADRs...
```

### 4. Infrastructure Guide (ADR-REF)

Infrastructure reference documentation:
```markdown
# ADR-REF-02: Infrastructure Guide

## Document Control
...

## 1. Introduction

Reference guide for infrastructure components and deployment architecture...
```

## Ready-Score Exemptions

**REF documents are EXEMPT from ALL ready-scores and quality gates:**

| Aspect | Standard Document | REF Document |
|--------|-------------------|--------------|
| **PRD-Ready Score** (BRD-REF) | Required ≥90% | **NOT APPLICABLE** |
| **SYS-Ready Score** (ADR-REF) | Required ≥90% | **NOT APPLICABLE** |
| **Cumulative Tags** | Required per layer | **NOT REQUIRED** |
| **Quality Gates** | Full validation | **EXEMPT** |
| **Format** | Structured sections | **Free format** |

## Comparison: REF vs Regular Artifacts

| Aspect | Regular Artifacts | REF Documents |
|--------|-------------------|---------------|
| Traceability | Required (cumulative tags) | Optional |
| Validation | Full (blocking) | Minimal (4 checks only) |
| Quality Gates | Must pass | Exempt |
| Workflow Position | Defined layer | No layer |
| Numbering | TYPE-NN | {TYPE}-REF-NN |
| Valid Parent Types | All artifact types | **BRD and ADR only** |

### Diagram Standards
All diagrams MUST use Mermaid syntax. Text-based diagrams (ASCII art, box drawings) are prohibited.
See: `ai_dev_flow/DIAGRAM_STANDARDS.md` and `mermaid-gen` skill.

## Related Resources

- **Template**: `ai_dev_flow/REF-TEMPLATE.md`
- **Naming Standards**: `ai_dev_flow/ID_NAMING_STANDARDS.md`
- **Validation**: `ai_dev_flow/scripts/validate_artifact.py`

## Regex Validation Patterns

### Filename Pattern
```regex
^(BRD|ADR)-REF-[0-9]{2,}_[a-z0-9_]+\.md$
```

**Valid**: `BRD-REF-01_project_overview.md`, `ADR-REF-100_technology_stack.md`
**Invalid**: `PRD-REF-01_features.md` (PRD not allowed), `BRD-REF-1_overview.md` (single digit)

### H1 ID Pattern
```regex
^#\s(BRD|ADR)-REF-[0-9]{2,}:.+$
```

**Valid**: `# BRD-REF-01: Project Overview`, `# ADR-REF-100: Technology Stack Summary`
**Invalid**: `# REQ-REF-01: Requirements Reference` (REQ not allowed)

## Quick Reference

- **Format**: `{TYPE}-REF-NN_{slug}.md`
- **DOC_NUM**: Variable-length (2+ digits: 01-99, 100-999, 1000+)
- **Valid Parent Types**: **BRD and ADR only**
- **Required Sections**: Document Control, Revision History, Introduction
- **Traceability**: Optional (encouraged but not required)
- **Validation**: Minimal (non-blocking, 4 checks only)
- **Element IDs**: NOT APPLICABLE - REF documents use free format
- **Ready-Scores**: NOT APPLICABLE - no quality gate enforcement

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1 | 2025-12-29 | Fixed DOC_NUM to variable-length (was NNN 3-digit); Added Element IDs section; Added Regex Validation; Updated examples |
| 1.0 | 2025-11-30 | Initial skill creation |
