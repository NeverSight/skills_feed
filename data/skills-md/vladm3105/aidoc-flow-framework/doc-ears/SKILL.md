---
name: doc-ears
description: Create EARS (Easy Approach to Requirements Syntax) formal requirements - Layer 3 artifact using WHEN-THE-SHALL-WITHIN format
tags:
  - sdd-workflow
  - layer-3-artifact
  - shared-architecture
custom_fields:
  layer: 3
  artifact_type: EARS
  architecture_approaches: [ai-agent-based, traditional-8layer]
  priority: shared
  development_status: active
  skill_category: core-workflow
  upstream_artifacts: [BRD, PRD]
  downstream_artifacts: [BDD, ADR, SYS]
---

# doc-ears

## Purpose

Create **EARS (Easy Approach to Requirements Syntax)** documents - Layer 3 artifact in the SDD workflow that formalizes requirements using the WHEN-THE-SHALL-WITHIN syntax.

**Layer**: 3

**Upstream**: BRD (Layer 1), PRD (Layer 2)

**Downstream Artifacts**: BDD (Layer 4), ADR (Layer 5), SYS (Layer 6)

## Prerequisites

### Upstream Artifact Verification (CRITICAL)

**Before creating this document, you MUST:**

1. **List existing upstream artifacts**:
   ```bash
   ls docs/BRD/ docs/PRD/ docs/EARS/ 2>/dev/null
   ```

2. **Reference only existing documents** in traceability tags
3. **Use `null`** only when upstream artifact type genuinely doesn't exist
4. **NEVER use placeholders** like `BRD-XXX` or `TBD`
5. **Do NOT create missing upstream artifacts** - skip functionality instead

Before creating EARS, read:

1. **Shared Standards**: `.claude/skills/doc-flow/SHARED_CONTENT.md`
2. **Upstream BRD and PRD**: Read the BRD and PRD that drive this EARS
3. **Template**: `ai_dev_flow/EARS/EARS-TEMPLATE.md` (Template Version 3.0, primary authority)
4. **Schema**: `ai_dev_flow/EARS/EARS_SCHEMA.yaml` (machine-readable validation rules)
5. **Creation Rules**: `ai_dev_flow/EARS/EARS_CREATION_RULES.md`
6. **Validation Rules**: `ai_dev_flow/EARS/EARS_VALIDATION_RULES.md`

### Template Binding (CRITICAL)

**Always use these exact metadata values:**

```yaml
tags:
  - ears                 # NOT 'ears-requirements' or 'ears-formal-requirements'
  - layer-3-artifact
  - shared-architecture  # OR 'ai-agent-primary' for agent docs

custom_fields:
  document_type: ears    # NOT 'engineering-requirements'
  artifact_type: EARS
  layer: 3
  architecture_approaches: [ai-agent-based, traditional-8layer]  # ARRAY format required
  priority: shared
  development_status: active
```

## When to Use This Skill

Use `doc-ears` when:
- Have completed BRD (Layer 1) and PRD (Layer 2)
- Need to formalize requirements with precise behavioral statements
- Translating product features into formal requirements
- Establishing event-driven, state-driven, or conditional requirements
- You are at Layer 3 of the SDD workflow

## Document Structure (MANDATORY)

Per EARS-TEMPLATE.md, EARS documents require these sections:

| Section | Content |
|---------|---------|
| **Document Control** | Status, Version, Date, BDD-Ready Score, Source Document |
| **1. Purpose and Context** | Document Purpose, Scope, Intended Audience |
| **2. EARS in Development Workflow** | Layer positioning diagram |
| **3. Requirements** | Event-Driven, State-Driven, Unwanted Behavior, Ubiquitous |
| **4. Quality Attributes** | Performance, Security, Reliability (tabular format) |
| **5. Traceability** | Upstream Sources, Downstream Artifacts, Tags, Thresholds |
| **6. References** | Internal Documentation, External Standards |

### Document Control Requirements

**Required Fields** (6 mandatory):
- **Status**: Draft/In Review/Approved/Implemented
- **Version**: Semantic versioning (e.g., 1.0.0)
- **Date Created/Last Updated**: YYYY-MM-DD
- **Priority**: High/Medium/Low
- **Source Document**: Single `@prd: PRD.NN.EE.SS` value (NO ranges, NO multiple @prd values)
- **BDD-Ready Score**: Format `XX% (Target: ≥90%)`

**Source Document Rule (E044)**:
```markdown
# VALID - Single @prd reference
| **Source Document** | @prd: PRD.01.07.01 |

# INVALID - Range or multiple values
| **Source Document** | @prd: PRD.12.19.01 - @prd: PRD.12.19.57 |
```

## EARS Syntax Patterns

### 1. Event-Driven Requirements
**WHEN** [triggering condition] **THE** [system] **SHALL** [response] **WITHIN** [constraint]

```
WHEN [trigger condition],
THE [system component] SHALL [action 1],
[action 2],
and [action 3]
WITHIN [timing constraint].
```

**Example**:
```
WHEN trade order received,
THE order management system SHALL validate order parameters
WITHIN 50 milliseconds (@threshold: PRD.035.timeout.order.validation).
```

### 2. State-Driven Requirements
**WHILE** [system state] **THE** [system] **SHALL** [behavior] **WITHIN** [constraint]

```
WHILE [state condition],
THE [system component] SHALL [continuous behavior]
WITHIN [operational context].
```

### 3. Unwanted Behavior Requirements
**IF** [error/problem] **THE** [system] **SHALL** [prevention/workaround] **WITHIN** [constraint]

```
IF [error condition],
THE [system component] SHALL [prevention/recovery action]
WITHIN [timing constraint].
```

### 4. Ubiquitous Requirements
**THE** [system] **SHALL** [system-wide requirement] **WITHIN** [architectural boundary]

```
THE [system component] SHALL [universal behavior]
for [scope/context].
```

### Code Block Formatting (MANDATORY)

Always use triple backticks for EARS statements:

````markdown
#### EARS.01.25.01: Requirement Name
```
WHEN [condition],
THE [component] SHALL [action]
WITHIN [constraint].
```
**Traceability**: @brd: BRD.01.01.01 | @prd: PRD.01.07.01
````

## Unified Element ID Format (MANDATORY)

**Pattern**: `EARS.{DOC_NUM}.{ELEM_TYPE}.{SEQ}` (4 segments, dot-separated)

| Element Type | Code | Example |
|--------------|------|---------|
| EARS Statement | 25 | EARS.02.25.01 |

**Category ID Ranges**:

| Category | ID Range | Example |
|----------|----------|---------|
| Event-Driven | 001-099 | EARS.01.25.001 |
| State-Driven | 101-199 | EARS.01.25.101 |
| Unwanted Behavior | 201-299 | EARS.01.25.201 |
| Ubiquitous | 401-499 | EARS.01.25.401 |

> **REMOVED PATTERNS** - Do NOT use:
> - Category prefixes: `E-XXX`, `S-XXX`, `Event-XXX`, `State-XXX`
> - 3-segment format: `EARS.NN.EE`
> - Dash-based: `EARS-NN-XXX`

## BDD-Ready Scoring System

**Purpose**: Measures EARS maturity and readiness for BDD progression.

**Format in Document Control**:
```markdown
| **BDD-Ready Score** | 95% (Target: ≥90%) |
```

### Status and BDD-Ready Score Mapping

| BDD-Ready Score | Required Status |
|-----------------|-----------------|
| ≥90% | Approved |
| 70-89% | In Review |
| <70% | Draft |

### Scoring Criteria

**Requirements Clarity (40%)**:
- EARS statements follow WHEN-THE-SHALL-WITHIN syntax: 20%
- Each statement defines one testable concept (atomicity): 15%
- All timing/constraint clauses are quantifiable: 5%

**Testability (35%)**:
- BDD translation possible for each statement: 15%
- Observable verification methods defined: 10%
- Edge cases and error conditions specified: 10%

**Quality Attribute Completeness (15%)**:
- Performance targets with percentiles: 5%
- Security/compliance requirements complete: 5%
- Reliability/scalability targets measurable: 5%

**Strategic Alignment (10%)**:
- Links to business objectives traceable: 5%
- Implementation paths documented: 5%

**Quality Gate**: Score <90% blocks BDD artifact creation.

## Quality Attributes Section

Use tabular format for quality attribute requirements:

### Performance Requirements

| QA ID | Requirement Statement | Metric | Target | Priority | Measurement Method |
|-------|----------------------|--------|--------|----------|-------------------|
| EARS.NN.02.01 | THE [component] SHALL complete [operation] | Latency | p95 < NNms | High | [method] |
| EARS.NN.02.02 | THE [component] SHALL process [workload] | Throughput | NN/s | Medium | [method] |

### Quality Attribute Categories

| Category | Keywords for Detection |
|----------|------------------------|
| Performance | latency, throughput, response time, p95, p99 |
| Reliability | availability, MTBF, MTTR, fault tolerance, recovery |
| Scalability | concurrent users, data volumes, horizontal scaling |
| Security | authentication, authorization, encryption, RBAC |
| Observability | logging, monitoring, tracing, alerting, metrics |
| Maintainability | code coverage, deployment, CI/CD, documentation |

## Formal Language Rules

**Mandatory Keywords**:
- **SHALL**: Mandatory requirement (do this)
- **SHALL NOT**: Prohibited requirement (never do this)
- **SHOULD**: Recommended requirement (preferred but not mandatory)
- **MAY**: Optional requirement (allowed but not required)

**Avoid ambiguous terms**: "fast", "efficient", "user-friendly"
**Use quantifiable metrics**: "within 100ms", "with 99.9% uptime"

## Threshold References (Section 5.4)

**Purpose**: EARS documents REFERENCE thresholds defined in PRD threshold registry. All quantitative values must use `@threshold:` tags.

**Threshold Naming Convention**: `@threshold: PRD.NN.category.subcategory.key`

**Example Usage**:
```
WHEN [trigger condition],
THE [system component] SHALL [action]
WITHIN @threshold: PRD.035.timeout.request.sync.
```

**Common Threshold Categories**:
```yaml
timing:
  - "@threshold: PRD.NN.timeout.request.sync"
  - "@threshold: PRD.NN.timeout.connection.default"

performance:
  - "@threshold: PRD.NN.perf.api.p95_latency"
  - "@threshold: PRD.NN.perf.batch.max_duration"

limits:
  - "@threshold: PRD.NN.limit.api.requests_per_second"

error:
  - "@threshold: PRD.NN.sla.error_rate.target"
```

## Tag Format Convention

| Notation | Format | Artifacts | Purpose |
|----------|--------|-----------|---------|
| Dash | TYPE-NN | ADR, SPEC, CTR | Technical artifacts - document references |
| Dot | TYPE.NN.TT.SS | BRD, PRD, EARS, BDD, SYS, REQ, IMPL, TASKS | Hierarchical artifacts - element references |

## Cumulative Tagging Requirements

**Layer 3 (EARS)**: Must include tags from Layers 1-2 (BRD, PRD)

**Tag Count**: 2 tags (@brd, @prd)

**Format**:
```markdown
## Traceability

**Required Tags** (Cumulative Tagging Hierarchy - Layer 3):
```markdown
@brd: BRD.01.01.03, BRD.01.01.10
@prd: PRD.01.07.02, PRD.01.07.15
```
```

### Traceability Tag Separators (E041)

**Inline format** - Use pipes:
```markdown
**Traceability**: @brd: BRD.02.01.10 | @prd: PRD.02.01.01 | @threshold: PRD.035.key
```

**List format** - Also valid:
```markdown
**Traceability**:
- @brd: BRD.02.01.10
- @prd: PRD.02.01.01
- @threshold: PRD.035.category.key
```

## Downstream Artifact References (E045)

**CRITICAL**: Do NOT use numeric downstream references until artifacts exist.

```markdown
# INVALID - Numeric references to non-existent artifacts
Downstream: BDD-01, ADR-02, REQ-03

# VALID - Generic downstream names
Downstream: BDD, ADR, SYS, REQ, SPEC
```

## File Size Limits and Splitting

**Limits**:
- Target: 300-500 lines per file
- Maximum: 600 lines per file (absolute)

**When to Split**:
- Document approaches 600 lines
- Sections cover distinct capability areas

**Splitting Process**:
1. Create `EARS-{NN}.0_index.md` using `EARS-SECTION-0-TEMPLATE.md`
2. Create section files `EARS-{NN}.{S}_{slug}.md` using `EARS-SECTION-TEMPLATE.md`
3. Maintain Prev/Next links
4. Update traceability

## Reserved ID Exemption

**Pattern**: `EARS-00_*.md`

**Scope**: Documents with reserved ID `000` are FULLY EXEMPT from validation.

**Document Types**:
- Index documents (`EARS-00_index.md`)
- Traceability matrix templates (`EARS-00_TRACEABILITY_MATRIX-TEMPLATE.md`)
- Glossaries, registries, checklists

## Creation Process

### Step 1: Read Upstream Artifacts

Read and understand BRD and PRD that drive these formal requirements.

### Step 2: Reserve ID Number

Check `docs/EARS/` for next available ID number (e.g., EARS-01, EARS-02).

**ID Numbering Convention**: Start with 2 digits and expand only as needed.
- ✅ Correct: EARS-01, EARS-99, EARS-102
- ❌ Incorrect: EARS-001, EARS-009 (extra leading zero not required)

### Step 3: Create EARS File

**Location**: `docs/EARS/EARS-NN_{slug}.md`

**Example**: `docs/EARS/EARS-01_risk_limits.md`

### Step 4: Fill Document Control Section

Complete all required metadata fields:
- Status
- Version
- Dates
- Priority
- Source Document (single @prd: PRD.NN.EE.SS)
- BDD-Ready Score

### Step 5: Categorize Requirements

Group requirements into 4 categories:
1. Event-Driven (triggered by events)
2. State-Driven (triggered by system state)
3. Unwanted Behavior (preventive)
4. Ubiquitous (always active)

### Step 6: Write WHEN-THE-SHALL-WITHIN Statements

For each requirement:
- Use formal EARS syntax
- Specify quantifiable constraints with @threshold tags
- Use SHALL/SHOULD/MAY keywords correctly
- Reference upstream PRD features

### Step 7: Create Quality Attributes Section

Use tabular format for Performance, Security, Reliability requirements.

### Step 8: Add Cumulative Tags

Include @brd and @prd tags (Layers 1-2) in Traceability section.

### Step 9: Add Threshold References

Document all thresholds used in section 5.4.

### Step 10: Create/Update Traceability Matrix

**MANDATORY**: Create or update `docs/EARS/EARS-00_TRACEABILITY_MATRIX.md`

### Step 11: Validate EARS

Run validation scripts:
```bash
# EARS validation
python scripts/validate_ears.py --path docs/EARS/EARS-01_*.md

# Cumulative tagging validation
python ai_dev_flow/scripts/validate_tags_against_docs.py \
  --artifact EARS-01 \
  --expected-layers brd,prd \
  --strict
```

### Step 12: Commit Changes

Commit EARS file and traceability matrix together.

## Batch Creation Checkpoint Rules

### Pre-Batch Verification

Before starting batch creation:
1. Read `EARS_SCHEMA.yaml` for current metadata requirements
2. Verify tag standards: `ears` (not `ears-requirements`)
3. Verify document_type: `ears`
4. Verify architecture format: `architecture_approaches: [value]` (array)

### Every 5-Document Checkpoint

After creating every 5 EARS documents:
1. Run validation: `python scripts/validate_ears.py --path docs/EARS`
2. Check for tag consistency, document_type, Source Document format
3. Fix any errors before continuing

### End-of-Session Validation

Before ending session:
1. Run full validation: `python scripts/validate_ears.py`
2. Verify 0 errors
3. Update EARS-00_index.md if document counts changed

## Validation

### Validation Error Codes Reference

| Code | Description | Severity |
|------|-------------|----------|
| E001 | YAML frontmatter invalid | ERROR |
| E002 | Required tags missing (ears, layer-3-artifact) | ERROR |
| E003 | Forbidden tag patterns (ears-requirements, etc.) | ERROR |
| E004 | Missing custom_fields | ERROR |
| E005 | document_type not 'ears' | ERROR |
| E006 | artifact_type not 'EARS' | ERROR |
| E007 | layer not 3 | ERROR |
| E008 | architecture_approaches not array | ERROR |
| E010 | Required sections missing | ERROR |
| E011 | Section numbering starts with 0 | ERROR |
| E013 | Document Control not in table format | ERROR |
| E020 | Malformed table syntax | ERROR |
| E030 | Requirement ID format invalid | ERROR |
| E040 | Source Document missing @prd: prefix | ERROR |
| E041 | Traceability tags missing pipe separators | ERROR |
| E042 | Duplicate requirement IDs | ERROR |
| E044 | Source Document has multiple @prd values | ERROR |
| E045 | Numeric downstream references | ERROR |

### Manual Checklist

- [ ] Document Control section uses table format
- [ ] All required metadata fields completed
- [ ] Source Document has single @prd: PRD.NN.EE.SS value
- [ ] All statements use WHEN-THE-SHALL-WITHIN format
- [ ] Requirements categorized (Event, State, Unwanted, Ubiquitous)
- [ ] Element IDs use EARS.NN.25.SS format
- [ ] SHALL/SHOULD/MAY keywords used correctly
- [ ] Quantifiable constraints with @threshold tags
- [ ] No ambiguous terms ("fast", "efficient")
- [ ] Cumulative tags: @brd, @prd included
- [ ] Traceability tags use pipe separators
- [ ] No numeric downstream references
- [ ] Quality Attributes in tabular format
- [ ] Thresholds documented in section 5.4
- [ ] File size <600 lines

## Common Pitfalls

| Mistake | Correction |
|---------|------------|
| `ears-requirements` tag | Use `ears` |
| `document_type: engineering-requirements` | Use `document_type: ears` |
| `architecture_approach: value` | Use `architecture_approaches: [value]` |
| `#### Event-001: Title` | Use `#### EARS.01.25.01: Title` |
| `Source Document: PRD-NN` | Use `Source Document: @prd: PRD.NN.EE.SS` |
| Multiple @prd in Source Document | Use single @prd, list others in Upstream Sources |
| `@brd: X @prd: Y` (no separators) | Use `@brd: X \| @prd: Y` |
| `Downstream: BDD-01, ADR-02` | Use `Downstream: BDD, ADR` |
| `Status: Approved` (with 50% score) | Use `Status: Draft` |
| `## 0. Document Control` | Use `## Document Control` (no numbering) |

## Post-Creation Validation (MANDATORY)

**CRITICAL**: Execute validation loop IMMEDIATELY after document creation.

### Automatic Validation Loop

```
LOOP:
  1. Run: python scripts/validate_ears.py --path {doc_path}
  2. IF errors fixed: GOTO LOOP (re-validate)
  3. IF warnings fixed: GOTO LOOP (re-validate)
  4. IF unfixable issues: Log for manual review
  5. IF clean: Mark VALIDATED, proceed
```

### Quality Gate

**Blocking**: YES - Cannot proceed to BDD creation until validation passes with 0 errors.

---

## Next Skill

After creating EARS, use:

**`doc-bdd`** - Create BDD test scenarios (Layer 4)

The BDD will:
- Reference this EARS as upstream source
- Include `@brd`, `@prd`, `@ears` tags (cumulative)
- Use Gherkin Given-When-Then format
- Validate EARS formal requirements with executable tests

## Related Resources

- **Template**: `ai_dev_flow/EARS/EARS-TEMPLATE.md` (Template Version 3.0, primary authority)
- **Schema**: `ai_dev_flow/EARS/EARS_SCHEMA.yaml` (machine-readable validation)
- **Creation Rules**: `ai_dev_flow/EARS/EARS_CREATION_RULES.md`
- **Validation Rules**: `ai_dev_flow/EARS/EARS_VALIDATION_RULES.md`
- **Shared Standards**: `.claude/skills/doc-flow/SHARED_CONTENT.md`
- **ID Standards**: `ai_dev_flow/ID_NAMING_STANDARDS.md`
- **Threshold Naming**: `ai_dev_flow/THRESHOLD_NAMING_RULES.md`

**Section Templates** (for documents >300 lines):
- Index template: `ai_dev_flow/EARS/EARS-SECTION-0-TEMPLATE.md`
- Content template: `ai_dev_flow/EARS/EARS-SECTION-TEMPLATE.md`

## Quick Reference

| Item | Value |
|------|-------|
| **Purpose** | Formalize requirements with WHEN-THE-SHALL-WITHIN syntax |
| **Layer** | 3 |
| **Tags Required** | @brd, @prd (2 tags) |
| **BDD-Ready Score** | ≥90% required for "Approved" status |
| **Element ID Format** | `EARS.NN.25.SS` (4-segment unified format) |
| **Source Document** | Single @prd: PRD.NN.EE.SS value |
| **Downstream References** | Generic names only (no numeric IDs) |
| **File Size Limit** | 600 lines maximum |
| **Next Skill** | doc-bdd |
