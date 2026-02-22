---
name: doc-sys
description: Create System Requirements (SYS) - Layer 6 artifact defining functional requirements and quality attributes
tags:
  - sdd-workflow
  - layer-6-artifact
  - shared-architecture
custom_fields:
  layer: 6
  artifact_type: SYS
  architecture_approaches: [ai-agent-based, traditional-8layer]
  priority: shared
  development_status: active
  skill_category: core-workflow
  upstream_artifacts: [BRD, PRD, EARS, BDD, ADR]
  downstream_artifacts: [REQ]
  version: "1.0"
  last_updated: "2026-02-10T15:00:00"
---

# doc-sys

## Purpose

Create **System Requirements (SYS)** documents - Layer 6 artifact in the SDD workflow that defines technical system requirements including functional capabilities and quality attributes.

**Layer**: 6

**Upstream**: BRD (Layer 1), PRD (Layer 2), EARS (Layer 3), BDD (Layer 4), ADR (Layer 5)

**Downstream Artifacts**: REQ (Layer 7), Code (Layer 13)

## Prerequisites

### Upstream Artifact Verification (CRITICAL)

**Before creating this document, you MUST:**

1. **List existing upstream artifacts**:
   ```bash
   ls docs/01_BRD/ docs/02_PRD/ docs/03_EARS/ docs/04_BDD/ docs/05_ADR/ docs/06_SYS/ docs/07_REQ/ 2>/dev/null
   ```

2. **Reference only existing documents** in traceability tags
3. **Use `null`** only when upstream artifact type genuinely doesn't exist
4. **NEVER use placeholders** like `BRD-XXX` or `TBD`
5. **Do NOT create missing upstream artifacts** - skip functionality instead


Before creating SYS, read:

1. **Shared Standards**: `.claude/skills/doc-flow/SHARED_CONTENT.md`
2. **Upstream ADR**: Read architecture decisions constraining system
3. **Template**: `ai_dev_flow/06_SYS/SYS-MVP-TEMPLATE.md`
4. **Creation Rules**: `ai_dev_flow/06_SYS/SYS_CREATION_RULES.md`
5. **Validation Rules**: `ai_dev_flow/06_SYS/SYS_VALIDATION_RULES.md`

## When to Use This Skill

Use `doc-sys` when:
- Have completed BRD through ADR (Layers 1-5)
- Need to define system-level technical requirements
- Translating architecture decisions into requirements
- Specifying functional system behavior and quality attributes
- You are at Layer 6 of the SDD workflow

## Reserved ID Exemption (SYS-00_*)

**Scope**: Documents with reserved ID `000` are FULLY EXEMPT from validation.

**Pattern**: `SYS-00_*.md`

**Document Types**: Index, Traceability matrix, Glossaries, Registries, Checklists

**Validation Behavior**: Skip all checks when filename matches `SYS-00_*` pattern.

## SYS-Specific Guidance

### 1. Five-Part SYS Document Structure

**Full Template**: See `ai_dev_flow/SYS/SYS-TEMPLATE.md` for complete structure.

**Part 1 - System Definition**:
- Document Control, Executive Summary, Scope

**Part 2 - System Requirements**:
- Functional Requirements, Quality Attributes

**Part 3 - System Specification**:
- Interface Specifications, Data Management Requirements, Testing and Validation Requirements

**Part 4 - System Operations**:
- Deployment and Operations Requirements, Compliance and Regulatory Requirements

**Part 5 - Validation and Control**:
- Acceptance Criteria, Risk Assessment, Traceability, Implementation Notes

### 2. Document Control Requirements

**Required Fields** (9 mandatory):
- Status, Version, Date Created/Last Updated, Author, Reviewers, Owner, Priority
- EARS-Ready Score
- REQ-Ready Score

**Format**:
```markdown
| Item | Details |
|------|---------|
| **EARS-Ready Score** | ✅ 95% (Target: ≥90%) |
| **REQ-Ready Score** | ✅ 95% (Target: ≥90%) |
```

### 3. REQ-Ready Scoring System

**Purpose**: Measures SYS maturity and readiness for progression to Requirements (REQ) decomposition.

**Format**: `✅ NN% (Target: ≥90%)`

**Status and REQ-Ready Score Mapping**:

| REQ-Ready Score | Required Status |
|-----------------|-----------------|
| ≥90% | Approved |
| 70-89% | In Review |
| <70% | Draft |

**Scoring Criteria**:
- **Requirements Decomposition Clarity (35%)**: System boundaries, functional decomposition, dependencies, ADR alignment
- **Quality Attributes Quantification (30%)**: Performance percentiles, reliability SLAs, security compliance, scalability metrics
- **Interface Specifications (20%)**: External APIs (CTR-ready), internal interfaces, data exchange protocols
- **Implementation Readiness (15%)**: Testing requirements, deployment/ops, monitoring/observability

**Quality Gate**: Score <90% blocks REQ artifact creation.

### 4. Element ID Format (MANDATORY)

**Pattern**: `SYS.{DOC_NUM}.{ELEM_TYPE}.{SEQ}` (4 segments, dot-separated)

| Element Type | Code | Example |
|--------------|------|---------|
| Functional Requirement | 01 | SYS.02.01.01 |
| Quality Attribute | 02 | SYS.02.02.01 |
| Use Case | 11 | SYS.02.11.01 |
| System Requirement | 26 | SYS.02.26.01 |

**REMOVED PATTERNS** - Do NOT use legacy formats:
- ❌ `FR-XXX` → Use `SYS.NN.01.SS`
- ❌ `QA-XXX` → Use `SYS.NN.02.SS`
- ❌ `UC-XXX` → Use `SYS.NN.11.SS`
- ❌ `SR-XXX` → Use `SYS.NN.26.SS`

**Reference**: [ID_NAMING_STANDARDS.md](../../ai_dev_flow/ID_NAMING_STANDARDS.md)

### 5. System Component Categorization

**System Types**:
- **API Services**: REST, GraphQL, or other API interfaces
- **Data Processing**: ETL, stream processing, batch processing systems
- **Integration Services**: Adapters, connectors, proxy services
- **Supporting Services**: Caching, messaging, configuration services
- **Infrastructure Components**: Load balancers, gateways, monitoring systems

**Criticality Levels**:
- **Mission-Critical**: Revenue-generating systems with <1 hour downtime SLA
- **Business-Critical**: Core operational systems with <4 hour downtime SLA
- **Operational Support**: Back-office systems with <24 hour downtime SLA

### 6. Threshold Registry Integration

**Purpose**: Prevent magic numbers by referencing centralized threshold registry.

**@threshold Tag Format**:
```markdown
@threshold: PRD.NN.category.subcategory.key
```

**SYS-Specific Threshold Categories**:

| Category | SYS Usage | Example Key |
|----------|-----------|-------------|
| `perf.*` | Performance requirements | `perf.api.p95_latency` |
| `sla.*` | Uptime and availability targets | `sla.uptime.target` |
| `timeout.*` | Circuit breaker, connection timeouts | `timeout.circuit_breaker.threshold` |
| `resource.*` | Memory, CPU, storage limits | `resource.memory.max_heap` |
| `limit.*` | Rate limits, connection limits | `limit.connection.max_total` |

**Invalid (hardcoded values)**:
- ❌ `p95 latency: 200ms`
- ❌ `uptime: 99.9%`

**Valid (registry references)**:
- ✅ `p95 latency: @threshold: PRD.NN.perf.api.p95_latency`
- ✅ `uptime: @threshold: PRD.NN.sla.uptime.target`

## Tag Format Convention (By Design)

| Notation | Format        | Artifacts                               | Purpose                                                             |
|----------|---------------|----------------------------------------|---------------------------------------------------------------------|
| Dash     | TYPE-NN      | ADR, SPEC, CTR            | Technical artifacts - references to files/documents                 |
| Dot      | TYPE.NN.TT.SS | BRD, PRD, EARS, BDD, SYS, REQ, IMPL, TASKS | Hierarchical artifacts - references to elements inside documents |

**Key Distinction**:
- `@adr: ADR-033` → Points to the document `ADR-033_risk_limit_enforcement.md`
- `@brd: BRD.17.01.01` → Points to element 01.01 inside document `BRD-017.md`

## Cumulative Tagging Requirements

**Layer 6 (SYS)**: Must include tags from Layers 1-5 (BRD, PRD, EARS, BDD, ADR)

**Tag Count**: 5 tags (@brd, @prd, @ears, @bdd, @adr)

**Format**:
```markdown
## Traceability

**Required Tags** (Cumulative Tagging Hierarchy - Layer 6):

@brd: BRD.01.01.03
@prd: PRD.01.07.02, PRD.01.07.15
@ears: EARS.01.25.01, EARS.01.25.02
@bdd: BDD.01.14.01
@adr: ADR-033, ADR-045
```

**Upstream Sources**:
- [BRD-01](../../01_BRD/BRD-01_platform/BRD-01_platform.md#BRD-01)
- [PRD-01](../../02_PRD/PRD-01_integration/PRD-01_integration.md#PRD-01)
- [EARS-01](../../03_EARS/EARS-01_risk/EARS-01_risk.md#EARS-01) - EARS type code: 25
- [BDD-01](../../04_BDD/BDD-01_limits/) - BDD scenario type code: 14
- [ADR-033](../../05_ADR/ADR-033_database/ADR-033_database.md#ADR-033)

## Upstream/Downstream Artifacts

**Upstream Sources**:
- **BRD** (Layer 1) - Business requirements
- **PRD** (Layer 2) - Product features
- **EARS** (Layer 3) - Formal requirements
- **BDD** (Layer 4) - Test scenarios
- **ADR** (Layer 5) - Architecture decisions (CRITICAL - defines constraints)

**Downstream Artifacts**:
- **REQ** (Layer 7) - Atomic requirements decomposed from SYS
- **Code** (Layer 13) - Implementation of system requirements

**Same-Type Document Relationships** (conditional):
- `@related-sys: SYS-NN` - SYS documents sharing system context
- `@depends-sys: SYS-NN` - SYS that must be implemented first

## Creation Process

### Step 1: Read Upstream Artifacts

Especially focus on ADR (Layer 5) - architecture decisions constrain system requirements.

### Step 2: Reserve ID Number

Check `ai_dev_flow/SYS/` for next available ID number.

**ID Numbering Convention**: Start with 2 digits and expand only as needed.
- ✅ Correct: SYS-01, SYS-99, SYS-102
- ❌ Incorrect: SYS-001, SYS-009 (extra leading zero not required)

### Step 3: Create SYS File

**Nested Folder Rule (MANDATORY)**: ALL SYS documents MUST use nested folders regardless of document size.

**Location**: `docs/06_SYS/SYS-NN_{slug}/SYS-NN_{slug}.md`

**Example**: `docs/06_SYS/SYS-01_order_management/SYS-01_order_management.md`

**CRITICAL**: Never create SYS files directly in `docs/06_SYS/` without a nested folder structure.

### Step 4: Fill Document Control Section

Complete metadata including EARS-Ready Score and REQ-Ready Score.

### Step 5: Define System Requirements

For each requirement:
- Use unified element ID format (`SYS.NN.TT.SS`)
- Specify inputs, processing, outputs (for functional)
- Specify measurable criteria (for quality attributes)
- Use `@threshold` tags for all quantitative values
- Reference upstream EARS/PRD
- Link to BDD verification

### Step 6: Create System Flows

Use Mermaid diagrams (not text-based):
- Sequence diagrams for interactions
- Flowcharts for logic
- State diagrams for workflows

### Step 7: Document Technical Constraints

From ADR decisions:
- List each constraint
- Explain impact
- Define verification

### Step 8: Add Cumulative Tags

Include all 5 upstream tags (@brd, @prd, @ears, @bdd, @adr).

### Step 9: Create/Update Traceability Matrix

**MANDATORY**: Update traceability matrix (`ai_dev_flow/SYS/SYS-00_TRACEABILITY_MATRIX-TEMPLATE.md`)

### Step 10: Validate SYS

Run validation commands (see Validation section).

### Step 11: Commit Changes

Commit SYS file and traceability matrix.

## Validation

### Validation Checks (8 Total)

| Check | Type | Description |
|-------|------|-------------|
| CHECK 1 | Error | Required Document Control Fields (9 fields) |
| CHECK 2 | Error | ADR Compliance Validation |
| CHECK 3 | Error | REQ-Ready Score Validation (format, threshold) |
| CHECK 4 | Error | Quality Attribute Quantification |
| CHECK 5 | Warning | System Boundaries |
| CHECK 6 | Warning | Interface Specifications (CTR-ready) |
| CHECK 7 | Warning | Upstream Traceability |
| CHECK 8 | Error | Element ID Format Compliance (unified 4-segment) |

### Validation Tiers

| Tier | Type | Exit Code | Action |
|------|------|-----------|--------|
| Tier 1 | Error | 1 | Must fix before commit |
| Tier 2 | Warning | 0 | Recommended to fix |
| Tier 3 | Info | 0 | No action required |

### Automated Validation

```bash
# Per-document validation (Phase 1)
python ai_dev_flow/scripts/validate_cross_document.py --document docs/SYS/SYS-NN_slug.md --auto-fix

# Layer validation (Phase 2) - run when all SYS documents complete
python ai_dev_flow/scripts/validate_cross_document.py --layer SYS --auto-fix

# Cumulative tagging validation
python ai_dev_flow/scripts/validate_tags_against_docs.py --artifact SYS-01 --expected-layers brd,prd,ears,bdd,adr --strict
```

### Manual Checklist

- [ ] Document Control section with 9 required fields
- [ ] REQ-Ready Score with ✅ emoji and percentage
- [ ] Requirements use unified element ID format (SYS.NN.TT.SS)
- [ ] No legacy patterns (FR-XXX, QA-XXX, UC-XXX, SR-XXX)
- [ ] Each requirement has measurable criteria
- [ ] All quantitative values use @threshold tags
- [ ] System flows use Mermaid diagrams
- [ ] Technical constraints from ADR documented
- [ ] Cumulative tags: @brd, @prd, @ears, @bdd, @adr included
- [ ] Each requirement references upstream source
- [ ] Verification method specified for each requirement
- [ ] Traceability matrix updated

## Post-Creation Validation (MANDATORY - NO CONFIRMATION)

**CRITICAL**: Execute this validation loop IMMEDIATELY after document creation. Do NOT proceed to next document until validation passes.

### Automatic Validation Loop

```
LOOP:
  1. Run: python ai_dev_flow/scripts/validate_cross_document.py --document {doc_path} --auto-fix
  2. IF errors fixed: GOTO LOOP (re-validate)
  3. IF warnings fixed: GOTO LOOP (re-validate)
  4. IF unfixable issues: Log for manual review, continue
  5. IF clean: Mark VALIDATED, proceed
```

### Layer-Specific Upstream Requirements

| This Layer | Required Upstream Tags | Count |
|------------|------------------------|-------|
| SYS (Layer 6) | @brd, @prd, @ears, @bdd, @adr | 5 tags |

### Auto-Fix Actions (No Confirmation Required)

| Issue | Fix Action |
|-------|------------|
| Missing @brd/@prd/@ears/@bdd/@adr tag | Add with upstream document reference |
| Invalid tag format | Correct to TYPE.NN.TT.SS (4-segment) or TYPE-NN format |
| Legacy element ID (FR-XXX, QA-XXX, etc.) | Convert to SYS.NN.TT.SS format |
| Broken link | Recalculate path from current location |
| Missing traceability section | Insert from template |

### Validation Codes Reference

| Code | Description | Severity |
|------|-------------|----------|
| XDOC-001 | Referenced requirement ID not found | ERROR |
| XDOC-002 | Missing cumulative tag | ERROR |
| XDOC-003 | Upstream document not found | ERROR |
| XDOC-006 | Tag format invalid | ERROR |
| XDOC-007 | Gap in cumulative tag chain | ERROR |
| XDOC-009 | Missing traceability section | ERROR |

### Quality Gate

**Blocking**: YES - Cannot proceed to REQ creation until Phase 1 validation passes with 0 errors.

## Common Pitfalls

1. **Vague requirements**: Must be measurable (not "fast" but "P95 <50ms")
2. **Missing ADR constraints**: System requirements must respect ADR decisions
3. **Text-based diagrams**: Use Mermaid ONLY, not ASCII art or code blocks
4. **Missing cumulative tags**: Layer 6 must include all 5 upstream tags
5. **No verification method**: Each requirement needs test approach
6. **Legacy element IDs**: Use SYS.NN.TT.SS not FR-XXX/QA-XXX/SR-XXX
7. **Hardcoded values**: Use @threshold tags, not magic numbers
8. **Wrong REQ-Ready Score format**: Must include ✅ emoji and percentage

---

## Downstream Creation Guidelines

### Creating REQ from SYS

**REQ Decomposition Rules**:
1. Each SYS functional requirement → 3-7 atomic REQ files
2. Each SYS quality attribute category → 2-4 atomic REQ files per category
3. Each SYS interface → 1-3 atomic REQ files per interface

**REQ Validation Against SYS**:
- All REQ capabilities must fit within SYS system boundaries
- All REQ acceptance criteria must satisfy SYS exit criteria
- All REQ quality attribute targets must meet or exceed SYS thresholds

**Interface CTR Creation**:
- When SYS specifies external API contracts, create CTR documents
- CTR requirements must exactly match SYS interface specifications

---

## Next Skill

After creating SYS, use:

**`doc-req`** - Create Atomic Requirements (Layer 7)

The REQ will:
- Decompose SYS into atomic requirements
- Include all 6 upstream tags (@brd through @sys)
- Use REQ v3.0 format (12 sections)
- Achieve ≥90% SPEC-readiness

## Reference Documents

SYS artifacts do not support REF documents. Reference documents are limited to **BRD and ADR types only** per the SDD framework.

For supplementary documentation needs, create:
- **BRD-REF**: Business context documentation
- **ADR-REF**: System architecture guides, QA attribute catalogs

## Related Resources

- **Template**: `ai_dev_flow/06_SYS/SYS-MVP-TEMPLATE.md` (primary authority)
- **SYS Creation Rules**: `ai_dev_flow/06_SYS/SYS_CREATION_RULES.md`
- **SYS Validation Rules**: `ai_dev_flow/06_SYS/SYS_VALIDATION_RULES.md`
- **SYS README**: `ai_dev_flow/06_SYS/README.md`
- **Shared Standards**: `.claude/skills/doc-flow/SHARED_CONTENT.md`

**Section Templates** (for documents >25K tokens):
- Index template: `ai_dev_flow/06_SYS/SYS-SECTION-0-TEMPLATE.md`
- Content template: `ai_dev_flow/06_SYS/SYS-SECTION-TEMPLATE.md`
- Reference: `ai_dev_flow/ID_NAMING_STANDARDS.md` (Section-Based File Splitting)

## Quick Reference

**SYS Purpose**: Define system-level technical requirements

**Layer**: 6

**Tags Required**: @brd, @prd, @ears, @bdd, @adr (5 tags)

**REQ-Ready Score**: ≥90% required for "Approved" status

**Element ID Format**: SYS.NN.TT.SS (FR=01, QA=02, UC=11, SR=26)

**Key Sections**:
- System Requirements (unified element IDs)
- System Flows (Mermaid diagrams)
- Technical Constraints (from ADR)

**Critical**: Use @threshold tags for all quantitative values

**Next**: doc-req

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-02-08 | Initial skill definition with YAML frontmatter standardization | System |
