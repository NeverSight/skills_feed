---
name: doc-req
description: Create Atomic Requirements (REQ) - Layer 7 artifact using REQ v3.0 format with 12 sections, SPEC-readiness scoring, and IMPL-readiness scoring
tags:
  - sdd-workflow
  - layer-7-artifact
  - shared-architecture
custom_fields:
  layer: 7
  artifact_type: REQ
  architecture_approaches: [ai-agent-based, traditional-8layer]
  priority: shared
  development_status: active
  skill_category: core-workflow
  upstream_artifacts: [BRD,PRD,EARS,BDD,ADR,SYS]
  downstream_artifacts: [IMPL,CTR,SPEC]
---

# doc-req

## Purpose

Create **Atomic Requirements (REQ)** documents - Layer 7 artifact in the SDD workflow that decomposes system requirements into atomic, implementation-ready requirements using REQ v3.0 format.

**Layer**: 7

**Upstream**: BRD (Layer 1), PRD (Layer 2), EARS (Layer 3), BDD (Layer 4), ADR (Layer 5), SYS (Layer 6)

**Downstream Artifacts**: IMPL (Layer 8), CTR (Layer 9), SPEC (Layer 10), Code (Layer 13)

## Prerequisites

### Upstream Artifact Verification (CRITICAL)

**Before creating this document, you MUST:**

1. **List existing upstream artifacts**:
   ```bash
   ls docs/BRD/ docs/PRD/ docs/EARS/ docs/BDD/ docs/ADR/ docs/SYS/ docs/REQ/ 2>/dev/null
   ```

2. **Reference only existing documents** in traceability tags
3. **Use `null`** only when upstream artifact type genuinely doesn't exist
4. **NEVER use placeholders** like `BRD-XXX` or `TBD`
5. **Do NOT create missing upstream artifacts** - skip functionality instead


Before creating REQ, read:

1. **Shared Standards**: `.claude/skills/doc-flow/SHARED_CONTENT.md`
2. **Upstream SYS**: Read system requirements driving this REQ
3. **Template**: `ai_dev_flow/REQ/REQ-TEMPLATE.md`
4. **Creation Rules**: `ai_dev_flow/REQ/REQ_CREATION_RULES.md`
5. **Validation Rules**: `ai_dev_flow/REQ/REQ_VALIDATION_RULES.md`
6. **Validation Script**: `./ai_dev_flow/scripts/validate_req_template.sh`

## When to Use This Skill

Use `doc-req` when:
- Have completed BRD through SYS (Layers 1-6)
- Need to decompose system requirements into atomic units
- Preparing for implementation (Layer 8+)
- Achieving >=90% SPEC-readiness score
- You are at Layer 7 of the SDD workflow

## Reserved ID Exemption (REQ-00_*)

**Scope**: Documents with reserved ID `000` are FULLY EXEMPT from validation.

**Pattern**: `REQ-00_*.md`

**Document Types**:
- Index documents (`REQ-00_index.md`)
- Traceability matrix templates (`REQ-00_TRACEABILITY_MATRIX-TEMPLATE.md`)
- Glossaries, registries, checklists

**Rationale**: Reserved ID 000 documents are framework infrastructure, not project artifacts requiring traceability or quality gates.

**Validation Behavior**: Skip all checks when filename matches `REQ-00_*` pattern.

## REQ-Specific Guidance

### 1. REQ v3.0 Format (12 Required Sections)

**CRITICAL**: REQ v3.0 expanded from 7 to 12 sections

**Document Control** (MANDATORY - First section before all numbered sections)

**Core Sections**:
1. **Description**: Atomic requirement + SHALL/SHOULD/MAY language + context + scenario
2. **Functional Requirements**: Core capabilities + business rules
3. **Interface Specifications**: Protocol/ABC definitions + DTOs + REST endpoints
4. **Data Schemas**: JSON Schema + Pydantic models + Database schema
5. **Error Handling Specifications**: Exception catalog + error response schema + circuit breaker config
6. **Configuration Specifications**: YAML schema + environment variables + validation
7. **Quality Attributes**: Performance targets (p50/p95/p99) + reliability/security/scalability
8. **Implementation Guidance**: Algorithms/patterns + concurrency/async + dependency injection
9. **Acceptance Criteria**: >=15 measurable criteria covering functional/error/quality/data/integration
10. **Verification Methods**: BDD scenarios + unit/integration/contract/performance tests
11. **Traceability**: Section 7 format with cumulative tags (6 required)
12. **Change History**: Version control table

### 2. Document Control Requirements (11 Mandatory Fields)

| Field | Format | Example |
|-------|--------|---------|
| Status | Approved/In Review/Draft | Approved |
| Version | Semantic X.Y.Z | 2.0.1 |
| Date Created | ISO 8601 | 2025-11-18 |
| Last Updated | ISO 8601 | 2025-11-19 |
| Author | Name/Role | System Architect |
| Priority | Level (P-level) | High (P2) |
| Category | Type | Functional |
| Source Document | DOC-ID section X.Y.Z | SYS-02 section 3.1.1 |
| Verification Method | Method type | BDD + Integration Test |
| Assigned Team | Team name | IB Integration Team |
| SPEC-Ready Score | Format with emoji | >=90% (Target: >=90%) |
| IMPL-Ready Score | Format with emoji | >=90% (Target: >=90%) |
| Template Version | Must be 3.0 | 3.0 |

### 3. Dual Readiness Scoring (SPEC-Ready + IMPL-Ready)

**MANDATORY**: Each REQ must calculate BOTH scores

**SPEC-Ready Score Formula**:
```
SPEC-Ready Score = (Completed Sections / 12) * 100%
```

**IMPL-Ready Score**: Measures readiness for implementation approach documentation

**Quality Gate**: Both scores >=90% required for layer transition

**Status and Ready Score Mapping**:

| Ready Score | Required Status |
|-------------|-----------------|
| >= 90% | Approved |
| 70-89% | In Review |
| < 70% | Draft |

**Note**: For REQ documents with dual scores, use the LOWER score to determine status.

**Example**:
```markdown
## Readiness Scores

**SPEC-Ready Score**: >=95% (Target: >=90%)
**IMPL-Ready Score**: >=92% (Target: >=90%)

**Section Status**:
- [x] 1. Description
- [x] 2. Functional Requirements
- [x] 3. Interface Specifications
- [x] 4. Data Schemas
- [x] 5. Error Handling Specifications
- [x] 6. Configuration Specifications
- [x] 7. Quality Attributes
- [x] 8. Implementation Guidance
- [x] 9. Acceptance Criteria
- [x] 10. Verification Methods
- [x] 11. Traceability
- [ ] 12. Change History (In Progress)

**Readiness**: READY for SPEC/IMPL creation
```

### 4. Element ID Format (MANDATORY)

**Pattern**: `REQ.{DOC_NUM}.{ELEM_TYPE}.{SEQ}` (4 segments, dot-separated)

| Element Type | Code | Example |
|--------------|------|---------|
| Functional Requirement | 01 | REQ.02.01.01 |
| Dependency | 05 | REQ.02.05.01 |
| Acceptance Criteria | 06 | REQ.02.06.01 |
| Atomic Requirement | 27 | REQ.02.27.01 |

**REMOVED PATTERNS** - Do NOT use:
- `AC-XXX` - Use `REQ.NN.06.SS`
- `FR-XXX` - Use `REQ.NN.01.SS`
- `R-XXX` - Use `REQ.NN.27.SS`
- `REQ-XXX` - Use `REQ.NN.27.SS`

**Reference**: `ID_NAMING_STANDARDS.md` - Cross-Reference Link Format

### 5. Atomic Requirement Principles

- **Single Responsibility**: Each REQ defines exactly one requirement
- **Measurable**: Acceptance criteria provide true/false outcomes
- **Self-Contained**: Understandable without external context
- **SPEC-Ready**: Contains ALL information for automated SPEC generation (>=90% completeness)
- **Modal Language**: SHALL (absolute), SHOULD (preferred), MAY (optional)

### 6. Domain/Subdomain Organization

**Location**: `REQ/{domain}/{subdomain}/` within project docs directory

**Domains**: `api/` (external integrations), `risk/` (risk management), `data/` (data requirements), `ml/` (ML requirements), `auth/` (security), etc.

**Format**: `REQ-NN_descriptive_slug.md`

**Example**: `REQ-risk-limits-01_position_validation.md`

## Tag Format Convention (By Design)

The SDD framework uses two distinct notation systems for cross-references:

| Notation | Format        | Artifacts                               | Purpose                                                             |
|----------|---------------|----------------------------------------|---------------------------------------------------------------------|
| Dash     | TYPE-NN      | ADR, SPEC, CTR            | Technical artifacts - references to files/documents                 |
| Dot      | TYPE.NN.TT.SS | BRD, PRD, EARS, BDD, SYS, REQ, IMPL, TASKS | Hierarchical artifacts - references to elements inside documents |

**Key Distinction**:
- `@adr: ADR-033` -> Points to the document `ADR-033_risk_limit_enforcement.md`
- `@brd: BRD.17.01.03` -> Points to element 01.03 inside document `BRD-017.md`

## Cumulative Tagging Requirements

**Layer 7 (REQ)**: Must include tags from Layers 1-6 (BRD, PRD, EARS, BDD, ADR, SYS)

**Tag Count**: 6 tags (@brd, @prd, @ears, @bdd, @adr, @sys)

**Format**:
```markdown
## Traceability

**Required Tags** (Cumulative Tagging Hierarchy - Layer 7):
```markdown
@brd: BRD.01.01.03
@prd: PRD.01.07.02
@ears: EARS.01.25.01
@bdd: BDD.01.14.01
@adr: ADR-033, ADR-045
@sys: SYS.01.01.01, SYS.01.02.07
```

**Upstream Sources**:
- [BRD-01](../BRD/BRD-01_platform.md#BRD-01)
- [PRD-01](../PRD/PRD-01_integration.md#PRD-01)
- [EARS-01](../EARS/EARS-01_risk.md#EARS-01)
- [BDD-01](../BDD/BDD-01_limits.feature)
- [ADR-033](../ADR/ADR-033_database.md#ADR-033)
- [SYS-01](../SYS/SYS-01_order.md#SYS-01)

**Downstream Artifacts**:
- IMPL-NN (to be created) - Implementation approach
- CTR-NN (to be created) - Data contracts
- SPEC-NN (to be created) - Technical specifications
```

**Element Type Codes for Tags**:
- EARS: Type 25 (formal requirement)
- BDD: Type 14 (scenario)
- SYS: Type 01 (functional), 02 (quality attribute), 26 (system req)

## Threshold Registry Integration

**Purpose**: Prevent magic numbers by referencing centralized threshold registry.

### When @threshold Tag is Required

Use `@threshold` for ALL quantitative values that are:
- Business-critical (compliance limits, SLAs)
- Configurable (timeout values, rate limits, retry policies)
- Shared across documents (performance targets)
- Quality attribute-related (p50/p95/p99 latencies, throughput limits)
- Error handling configurations (circuit breaker, retry counts)

### @threshold Tag Format

```markdown
@threshold: PRD.NN.category.subcategory.key
```

**Examples**:
- `@threshold: PRD.035.perf.api.p95_latency`
- `@threshold: PRD.035.timeout.circuit_breaker.threshold`
- `@threshold: PRD.035.retry.max_attempts`
- `@threshold: PRD.035.limit.api.requests_per_second`

### REQ-Specific Threshold Categories

| Category | REQ Usage | Example Key |
|----------|-----------|-------------|
| `perf.*` | Performance acceptance criteria | `perf.api.p95_latency` |
| `timeout.*` | Circuit breaker, connection configs | `timeout.circuit_breaker.reset` |
| `retry.*` | Retry policy configurations | `retry.max_attempts` |
| `limit.*` | Rate limits, resource limits | `limit.api.requests_per_second` |
| `resource.*` | Memory, CPU constraints | `resource.memory.max_heap` |

### Magic Number Detection

**Invalid (hardcoded values)**:
- `p95 response time: 200ms`
- `max_retries: 3`
- `rate_limit: 100 req/s`

**Valid (registry references)**:
- `p95 response time: @threshold: PRD.NN.perf.api.p95_latency`
- `max_retries: @threshold: PRD.NN.retry.max_attempts`
- `rate_limit: @threshold: PRD.NN.limit.api.requests_per_second`

## Upstream/Downstream Artifacts

**Upstream Sources**:
- **BRD** (Layer 1) - Business requirements
- **PRD** (Layer 2) - Product features
- **EARS** (Layer 3) - Formal requirements
- **BDD** (Layer 4) - Test scenarios
- **ADR** (Layer 5) - Architecture decisions
- **SYS** (Layer 6) - System requirements (PRIMARY SOURCE)

**Downstream Artifacts**:
- **IMPL** (Layer 8) - Implementation approach (optional)
- **CTR** (Layer 9) - Data contracts (optional)
- **SPEC** (Layer 10) - Technical specifications
- **Code** (Layer 13) - Implementation

**Same-Type Document Relationships** (conditional):
- `@related-req: REQ-NN` - REQs sharing domain context
- `@depends-req: REQ-NN` - REQ that must be implemented first

## Creation Process

### Step 1: Read Upstream Artifacts

Especially focus on SYS (Layer 6) - system requirements to decompose.

### Step 2: Reserve ID Number

Check `ai_dev_flow/REQ/` for next available ID number.

**ID Numbering Convention**: Start with 2 digits and expand only as needed.
- ✅ Correct: REQ-01, REQ-99, REQ-102
- ❌ Incorrect: REQ-001, REQ-009 (extra leading zero not required)

**Domain-based naming**: `REQ-domain-subdomain-NN`

### Step 3: Create REQ File

**Location Options**:
- Flat: `docs/REQ/REQ-{NN}_{slug}.md`
- Domain-based: `docs/REQ/{domain}/REQ-NN_{slug}.md`
- Subdomain: `docs/REQ/{domain}/{subdomain}/REQ-NN_{slug}.md`

**On-Demand Folder Creation**: Before saving the document, create the target directory:
```bash
# Create target directory if it doesn't exist
mkdir -p docs/REQ/{domain}/         # For domain-based structure
# OR
mkdir -p docs/REQ/{domain}/{subdomain}/  # For subdomain structure
```

**Domain Selection**: Use domain from project configuration or upstream SYS context:
- Financial: `risk/`, `trading/`, `collection/`, `compliance/`, `ml/`
- SaaS: `tenant/`, `subscription/`, `billing/`, `workspace/`
- Generic: `api/`, `auth/`, `data/`, `core/`, `integration/`

**Section Files**: For large requirements (>50KB), use Section Files format: `REQ-NN.S_section_title.md` (S = section number).

### Step 4: Fill Document Control Section

Complete metadata with all 11 required fields plus Document Revision History table.

### Step 5: Complete All 12 Required Sections

**Critical**: REQ v3.0 requires all 12 sections for >=90% SPEC-readiness

1. **Description**: Atomic requirement + SHALL/SHOULD/MAY language
2. **Functional Requirements**: Core capabilities + business rules
3. **Interface Specifications**: APIs, endpoints, contracts, Protocol/ABC class
4. **Data Schemas**: Models, validation, constraints, Pydantic/dataclass
5. **Error Handling Specifications**: Error codes, recovery, exception definitions
6. **Configuration Specifications**: Settings, feature flags, YAML config
7. **Quality Attributes**: Performance, security, scalability with thresholds
8. **Implementation Guidance**: Technical approach, patterns
9. **Acceptance Criteria**: >=15 measurable criteria
10. **Verification Methods**: BDD scenarios, tests
11. **Traceability**: Cumulative tags (6 tags)
12. **Change History**: Version control table

### Step 6: Calculate Readiness Scores

Count completed sections and calculate both SPEC-Ready and IMPL-Ready percentages.

**Quality Gate**: Both scores must achieve >=90%

### Step 7: Add Cumulative Tags

Include all 6 upstream tags (@brd through @sys).

### Step 8: Create/Update Traceability Matrix

**MANDATORY**: Update `ai_dev_flow/REQ/REQ-00_TRACEABILITY_MATRIX-TEMPLATE.md`

### Step 9: Validate REQ

```bash
./ai_dev_flow/scripts/validate_req_template.sh ai_dev_flow/REQ/REQ-NN_*.md

python ai_dev_flow/scripts/validate_tags_against_docs.py --artifact REQ-NN --expected-layers brd,prd,ears,bdd,adr,sys --strict
```

### Step 10: Commit Changes

Commit REQ file and traceability matrix.

## Validation

### Validation Checks (20 Total)

| Check | Description | Type |
|-------|-------------|------|
| CHECK 1 | Required 12 sections | Error |
| CHECK 2 | Document Control (11 fields) | Error |
| CHECK 3 | Traceability structure | Error/Warning |
| CHECK 4 | Legacy (deprecated) | Info |
| CHECK 5 | Version format (X.Y.Z) | Error |
| CHECK 6 | Date format (ISO 8601) | Error |
| CHECK 7 | Priority format (P1-P4) | Warning |
| CHECK 8 | Source document format | Warning |
| CHECK 9 | SPEC-Ready Score | Error/Warning |
| CHECK 10 | Template Version (3.0) | Error |
| CHECK 11 | Change History | Error/Warning |
| CHECK 12 | Filename/ID format | Error |
| CHECK 13 | Resource tag (Template 2.0) | Error |
| CHECK 14 | Cumulative tagging (6 tags) | Error |
| CHECK 15 | Complete upstream chain | Error |
| CHECK 16 | Link resolution | Error/Warning |
| CHECK 17 | Traceability matrix | Warning |
| CHECK 18 | SPEC-Ready content | Warning |
| CHECK 19 | IMPL-Ready Score | Error |
| CHECK 20 | Element ID format compliance | Error |

### Validation Tiers

| Tier | Type | Exit Code | Description |
|------|------|-----------|-------------|
| Tier 1 | Errors | 1 | Blocking - must fix before commit |
| Tier 2 | Warnings | 0 | Quality issues - recommended to fix |
| Tier 3 | Info | 0 | Informational - no action required |

### Automated Validation

```bash
# Validate single file
./scripts/validate_req_template.sh docs/REQ/REQ-NN_slug.md

# Validate all REQ files
find docs/REQ -name "REQ-*.md" -exec ./scripts/validate_req_template.sh {} \;

# Cumulative tagging validation
python ai_dev_flow/scripts/validate_tags_against_docs.py \
  --artifact REQ-NN \
  --expected-layers brd,prd,ears,bdd,adr,sys \
  --strict
```

### Manual Checklist

- [ ] Document Control section at top with 11 required fields
- [ ] All 12 required sections completed
- [ ] SPEC-Ready Score >=90%
- [ ] IMPL-Ready Score >=90%
- [ ] Template Version = 3.0
- [ ] Section 3: Interface Specifications with Protocol/ABC class
- [ ] Section 4: Data Schemas with Pydantic/dataclass models
- [ ] Section 5: Error Handling with exception definitions
- [ ] Section 6: Configuration with YAML schema
- [ ] Section 7: Quality Attributes with @threshold references
- [ ] Section 9: >=15 acceptance criteria
- [ ] Cumulative tags: @brd through @sys (6 tags) included
- [ ] Each requirement atomic (single responsibility)
- [ ] Acceptance criteria testable and measurable
- [ ] Traceability matrix updated

### Diagram Standards
All diagrams MUST use Mermaid syntax. Text-based diagrams (ASCII art, box drawings) are prohibited.
See: `ai_dev_flow/DIAGRAM_STANDARDS.md` and `mermaid-gen` skill.

## Common Pitfalls

1. **Incomplete sections**: All 12 sections mandatory for SPEC-readiness
2. **Missing new sections**: Sections 3-7 are new in v3.0 - don't skip them
3. **Low readiness scores**: Both SPEC-Ready and IMPL-Ready must achieve >=90%
4. **Non-atomic requirements**: Each REQ must be single, testable unit
5. **Missing cumulative tags**: Layer 7 must include all 6 upstream tags
6. **Vague acceptance criteria**: Must be measurable and testable
7. **Hardcoded values**: Use @threshold references, not magic numbers
8. **Legacy element IDs**: Use `REQ.NN.TT.SS` format, not AC-XXX or FR-XXX
9. **Status/score mismatch**: Status must match the LOWER of the two scores

## Post-Creation Validation (MANDATORY - NO CONFIRMATION)

**CRITICAL**: Execute this validation loop IMMEDIATELY after document creation.

### Automatic Validation Loop

```
LOOP:
  1. Run: python scripts/validate_cross_document.py --document {doc_path} --auto-fix
  2. IF errors fixed: GOTO LOOP (re-validate)
  3. IF warnings fixed: GOTO LOOP (re-validate)
  4. IF unfixable issues: Log for manual review, continue
  5. IF clean: Mark VALIDATED, proceed
```

### Validation Command

```bash
# Per-document validation (Phase 1)
python ai_dev_flow/scripts/validate_cross_document.py --document docs/REQ/REQ-NN_slug.md --auto-fix

# Layer validation (Phase 2) - run when all REQ documents complete
python ai_dev_flow/scripts/validate_cross_document.py --layer REQ --auto-fix
```

### Layer-Specific Upstream Requirements

| This Layer | Required Upstream Tags | Count |
|------------|------------------------|-------|
| REQ (Layer 7) | @brd, @prd, @ears, @bdd, @adr, @sys | 6 tags |

### Auto-Fix Actions (No Confirmation Required)

| Issue | Fix Action |
|-------|------------|
| Missing @brd/@prd/@ears/@bdd/@adr/@sys tag | Add with upstream document reference |
| Invalid tag format | Correct to TYPE.NN.TT.SS (4-segment) or TYPE-NN format |
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

**Blocking**: YES - Cannot proceed to IMPL/SPEC creation until Phase 1 validation passes with 0 errors.

---

## Next Skill

After creating REQ, use:

**`doc-spec`** (or optionally `doc-impl`/`doc-ctr` first) - Create Technical Specifications (Layer 10)

The SPEC will:
- Reference this REQ as upstream source
- Include all 7 upstream tags (@brd through @req)
- Use YAML format
- Define implementation contracts
- Achieve 100% implementation-readiness

## Reference Documents

REQ artifacts do not support REF documents. Reference documents are limited to **BRD and ADR types only** per the SDD framework.

For supplementary documentation needs, create:
- **BRD-REF**: Business context and domain glossaries
- **ADR-REF**: Technical reference guides and architecture summaries

## Related Resources

- **Template**: `ai_dev_flow/REQ/REQ-TEMPLATE.md` (primary authority)
- **REQ Creation Rules**: `ai_dev_flow/REQ/REQ_CREATION_RULES.md`
- **REQ Validation Rules**: `ai_dev_flow/REQ/REQ_VALIDATION_RULES.md`
- **REQ README**: `ai_dev_flow/REQ/README.md`
- **Shared Standards**: `.claude/skills/doc-flow/SHARED_CONTENT.md`

**Section Templates** (for documents >50KB):
- Index template: `ai_dev_flow/REQ/REQ-SECTION-0-TEMPLATE.md`
- Content template: `ai_dev_flow/REQ/REQ-SECTION-TEMPLATE.md`
- Reference: `ai_dev_flow/ID_NAMING_STANDARDS.md` (Section-Based File Splitting)

## Quick Reference

**REQ Purpose**: Atomic, implementation-ready requirements

**Layer**: 7

**Tags Required**: @brd, @prd, @ears, @bdd, @adr, @sys (6 tags)

**Format**: REQ v3.0 (12 sections)

**Quality Gate**: SPEC-Ready Score >=90% AND IMPL-Ready Score >=90%

**Element ID Format**: `REQ.NN.TT.SS`
- Functional Requirement = 01
- Dependency = 05
- Acceptance Criteria = 06
- Atomic Requirement = 27

**Removed Patterns**: AC-XXX, FR-XXX, R-XXX, REQ-XXX

**Document Control Fields**: 11 required (+ Template Version = 3.0)

**Status/Score Mapping**: >=90% Approved, 70-89% In Review, <70% Draft

**File Size Limits**: >50KB use section files

**Next**: doc-spec (or optionally doc-impl/doc-ctr first)
