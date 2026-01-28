---
name: doc-naming
description: Enforces unified ID naming standards and threshold naming rules for all SDD documentation artifacts
tags:
  - sdd-workflow
  - shared-architecture
  - quality-assurance
  - required-both-approaches
custom_fields:
  layer: null
  artifact_type: null
  architecture_approaches: [ai-agent-based, traditional-8layer]
  priority: shared
  development_status: active
  skill_category: quality-assurance
  upstream_artifacts: []
  downstream_artifacts: []
---

# doc-naming Skill

Enforces unified ID naming standards and threshold naming rules for all SDD documentation artifacts.

---

## 1. Purpose & Scope

### When to Invoke

Invoke this skill BEFORE creating or editing any SDD documentation artifact. Use it to:
- Verify element ID format compliance
- Check for removed/legacy patterns
- Validate threshold tag syntax
- Ensure document ID format correctness

### Coverage

This skill covers all 12 SDD document types:

| Layer | Document Type | Description |
|-------|---------------|-------------|
| 1 | BRD | Business Requirements Document |
| 2 | PRD | Product Requirements Document |
| 3 | EARS | Easy Approach to Requirements Syntax |
| 4 | BDD | Behavior-Driven Development |
| 5 | ADR | Architecture Decision Record |
| 6 | SYS | System Requirements |
| 7 | REQ | Atomic Requirements |
| 8 | IMPL | Implementation Approach |
| 9 | CTR | Data Contracts |
| 10 | SPEC | Technical Specifications |
| 11 | TASKS | AI Task Breakdown |

---

## 2. Reserved ID Exemption (TYPE-00_*)

### Scope

Documents with reserved ID `000` are FULLY EXEMPT from standard validation.

### Pattern

`{DOC_TYPE}-00_{slug}.{ext}`

### Document Types

- Index documents (e.g., `BRD-00_index.md`, `REQ-00_index.md`)
- Traceability matrix templates (e.g., `SPEC-00_TRACEABILITY_MATRIX-TEMPLATE.md`)
- Glossaries, registries, checklists

### Rationale

Reserved ID 000 documents are framework infrastructure (indexes, templates, reference materials), not project artifacts requiring traceability or quality gates.

### Validation Behavior

Skip all element ID and traceability checks when filename matches `{TYPE}-00_*` pattern.

---

## 3. Document ID Format (TYPE-NN)

### Pattern

```
TYPE-NN
```

- **TYPE**: Uppercase document type acronym (BRD, PRD, EARS, etc.)
- **Separator**: Single dash `-`
- **NN**: 2+ digit sequential number with leading zeros

### Validation Regex

```regex
^[A-Z]{2,5}-[0-9]{2,}$
```

### Examples

| Document ID | Valid | Reason |
|-------------|-------|--------|
| `BRD-01` | ✅ | Correct format |
| `PRD-02` | ✅ | Correct format |
| `ADR-001` | ✅ | 3-digit ID allowed |
| `TASKS-12` | ✅ | Correct format |
| `brd-01` | ❌ | Lowercase not allowed |
| `PRD_02` | ❌ | Underscore not allowed |
| `BRD-1` | ❌ | Single digit not allowed |
| `BRD01` | ❌ | Missing dash separator |

### Filename Convention

```
TYPE-NN_descriptive_slug.md
```

Example: `BRD-01_ib_stock_options_mcp_server.md`

### REF Document Pattern

Reference documents use a modified pattern within parent TYPE directories:

| Component | Pattern | Example |
|-----------|---------|---------|
| H1 ID | `{TYPE}-REF-NN` | `# BRD-REF-01: Project Overview` |
| Filename | `{TYPE}-REF-NN_{slug}.md` | `BRD-REF-01_project_overview.md` |
| Location | Within parent TYPE directory | `docs/BRD/BRD-REF-01_project_overview.md` |

**Notes**:
- REF documents are supplementary and do not participate in formal traceability chain
- Similar exemption treatment as `{TYPE}-000` index documents
- Numbering is independent per parent TYPE (BRD-REF-01, ADR-REF-01 are separate sequences)

---

## 4. Element ID Format (TYPE.NN.TT.SS)

### Pattern

```
{DOC_TYPE}.{DOC_NUM}.{ELEM_TYPE}.{SEQ}
```

| Segment | Description | Format |
|---------|-------------|--------|
| DOC_TYPE | Document type acronym | 2-5 uppercase letters |
| DOC_NUM | Document number | 2+ digits |
| ELEM_TYPE | Element type code | 2+ digits (01-31) |
| SEQ | Sequential number | 2+ digits |

### Validation Regex

```regex
^[A-Z]{2,5}\.[0-9]{2,}\.[0-9]{2,}\.[0-9]{2,}$
```

### Examples

| Element ID | Valid | Breakdown |
|------------|-------|-----------|
| `BRD.02.06.01` | ✅ | BRD doc 02, Acceptance Criteria (06), item 01 |
| `PRD.01.09.03` | ✅ | PRD doc 01, User Story (09), item 03 |
| `ADR.05.10.01` | ✅ | ADR doc 05, Decision (10), item 01 |
| `SPEC.03.16.02` | ✅ | SPEC doc 03, Interface (16), item 02 |
| `AC-001` | ❌ | Legacy pattern - use TYPE.NN.06.SS |
| `FR-01` | ❌ | Legacy pattern - use TYPE.NN.01.SS |
| `BRD-02-06-01` | ❌ | Wrong separator (use dots) |
| `brd.02.06.01` | ❌ | Lowercase not allowed |

### Heading Format

Element IDs appear as markdown headings:

```markdown
### BRD.02.06.01: User Authentication Acceptance Criteria
#### PRD.01.09.03: User Login Story
```

---

## 5. Element Type Codes Table

All 31 element type codes with document type applicability:

| Code | Element Type | Applicable Document Types |
|------|--------------|---------------------------|
| 01 | Functional Requirement | BRD, PRD, SYS, REQ |
| 02 | Quality Attribute | BRD, PRD, SYS |
| 03 | Constraint | BRD, PRD |
| 04 | Assumption | BRD, PRD |
| 05 | Dependency | BRD, PRD, REQ |
| 06 | Acceptance Criteria | BRD, PRD, REQ |
| 07 | Risk | BRD, PRD |
| 08 | Metric | BRD, PRD |
| 09 | User Story | PRD, BRD |
| 10 | Decision | ADR, BRD |
| 11 | Use Case | PRD, SYS |
| 12 | Alternative | ADR |
| 13 | Consequence | ADR |
| 14 | Test Scenario | BDD |
| 15 | Step | BDD, SPEC |
| 16 | Interface | SPEC, CTR |
| 17 | Data Model | SPEC, CTR |
| 18 | Task | TASKS |
| 20 | Contract Clause | CTR |
| 21 | Validation Rule | SPEC |
| 22 | Feature Item | BRD, PRD |
| 23 | Business Objective | BRD |
| 24 | Stakeholder Need | BRD, PRD |
| 25 | EARS Statement | EARS |
| 26 | System Requirement | SYS |
| 27 | Atomic Requirement | REQ |
| 28 | Specification Element | SPEC |
| 29 | Implementation Phase | IMPL |
| 30 | Task Item | TASKS |

### Quick Lookup by Document Type

| Document | Common Element Codes |
|----------|---------------------|
| BRD | 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 22, 23, 24 |
| PRD | 01, 02, 03, 04, 05, 06, 07, 08, 09, 11, 22, 24 |
| EARS | 25 |
| BDD | 14, 15 |
| ADR | 10, 12, 13 |
| SYS | 01, 02, 11, 26 |
| REQ | 01, 05, 06, 27 |
| IMPL | 29 |
| CTR | 16, 17, 20 |
| SPEC | 15, 16, 17, 21, 28 |
| TASKS | 18, 30 |

---

## 6. Removed/Legacy Patterns

These patterns are DEPRECATED. Do NOT use them in new documents.

| Removed Pattern | Migration Path | Applies To |
|-----------------|----------------|------------|
| `AC-XXX` | `TYPE.NN.06.SS` | BRD, PRD, REQ |
| `FR-XXX` | `TYPE.NN.01.SS` | BRD, PRD, SYS, REQ |
| `BC-XXX` | `TYPE.NN.03.SS` | BRD, PRD |
| `BA-XXX` | `TYPE.NN.04.SS` | BRD, PRD |
| `QA-XXX` | `TYPE.NN.02.SS` | BRD, PRD, SYS |
| `BO-XXX` | `TYPE.NN.23.SS` | BRD |
| `RISK-XXX` | `TYPE.NN.07.SS` | BRD, PRD |
| `METRIC-XXX` | `TYPE.NN.08.SS` | BRD, PRD |
| `Feature F-XXX` | `TYPE.NN.22.SS` | BRD, PRD |
| `Event-XXX` | `TYPE.NN.25.SS` | EARS |
| `State-XXX` | `TYPE.NN.25.SS` | EARS |
| `TASK-XXX` | `TYPE.NN.18.SS` | TASKS |
| `T-XXX` | `TYPE.NN.18.SS` | TASKS |
| `Phase-XXX` | `TYPE.NN.29.SS` | IMPL |
| `IP-XXX` | `TYPE.NN.29.SS` | IMPL |
| `IF-XXX` | `TYPE.NN.16.SS` | CTR |
| `DM-XXX` | `TYPE.NN.17.SS` | CTR |
| `CC-XXX` | `TYPE.NN.20.SS` | CTR |
| `DEC-XXX` | `TYPE.NN.10.SS` | ADR |
| `ALT-XXX` | `TYPE.NN.12.SS` | ADR |
| `CON-XXX` | `TYPE.NN.13.SS` | ADR |

### Migration Examples

| Legacy | Unified Format |
|--------|----------------|
| `### AC-001: Login Validation` | `### BRD.02.06.01: Login Validation` |
| `#### FR-01: User Auth` | `#### PRD.01.01.01: User Auth` |
| `### Event-001: KYC Submission` | `### EARS.06.25.01: KYC Submission` |
| `### TASK-01: Setup` | `### TASKS.02.18.01: Setup` |
| `### Phase-01: Init` | `### IMPL.02.29.01: Init` |
| `### DEC-01: Use PostgreSQL` | `### ADR.05.10.01: Use PostgreSQL` |
| `### ALT-01: MongoDB Option` | `### ADR.05.12.01: MongoDB Option` |

---

## 7. Threshold Tag Format

### Tag Pattern

```
@threshold: {DOC_TYPE}.{DOC_NUM}.{threshold_key}
```

### Key Format

```
{category}.{subcategory}.{attribute}[.{qualifier}]
```

### Valid Categories

| Category | Description | Example Keys |
|----------|-------------|--------------|
| perf | Performance metrics | `perf.latency.p99` |
| timeout | Timeout values | `timeout.api.request` |
| rate | Rate limits | `rate.api.requests_per_second` |
| retry | Retry policies | `retry.max_attempts` |
| circuit | Circuit breaker | `circuit.failure_threshold` |
| alert | Alerting thresholds | `alert.error_rate.critical` |
| cache | Cache settings | `cache.ttl.session` |
| pool | Connection pools | `pool.max_connections` |
| queue | Queue settings | `queue.max_size` |
| batch | Batch processing | `batch.size.max` |

### Examples

| Threshold Tag | Valid | Breakdown |
|---------------|-------|-----------|
| `@threshold: PRD.035.timeout.partner.bridge` | ✅ | PRD doc 035, timeout category |
| `@threshold: BRD.02.perf.latency.p99` | ✅ | BRD doc 02, performance category |
| `@threshold: ADR.05.circuit.failure_threshold` | ✅ | ADR doc 05, circuit breaker |
| `@threshold: timeout.partner.bridge` | ❌ | Missing doc reference |
| `@threshold: PRD-035.timeout` | ❌ | Wrong separator (dash vs dot) |

### Source Documents for Thresholds

| Doc Type | Threshold Scope |
|----------|-----------------|
| BRD | Business-level thresholds (SLAs, business rules) |
| PRD | Product-level thresholds (user experience, product metrics) |
| ADR | Technical thresholds (architecture decisions, system limits) |

---

## 8. Validation Examples by Document Type

### BRD Examples

```markdown
### BRD.02.01.01: User Authentication Requirement
### BRD.02.06.01: Login Acceptance Criteria
### BRD.02.23.01: Revenue Growth Objective
### BRD.02.09.01: User Onboarding Story
### BRD.02.10.01: Database Selection Decision
@threshold: BRD.02.perf.response_time.max
```

### PRD Examples

```markdown
### PRD.01.09.01: User Login Story
### PRD.01.22.01: Dashboard Feature
### PRD.01.06.01: Feature Acceptance Criteria
@threshold: PRD.01.timeout.session.idle
```

### EARS Examples

```markdown
#### EARS.06.25.01: KYC Submission Event
#### EARS.06.25.02: Pending Status State
```

### ADR Examples

```markdown
### ADR.05.10.01: Use PostgreSQL Decision
### ADR.05.12.01: MongoDB Alternative
### ADR.05.13.01: Migration Consequence
@threshold: ADR.05.circuit.failure_threshold
```

### SPEC Examples

```markdown
### SPEC.03.16.01: REST API Interface
### SPEC.03.17.01: User Data Model
### SPEC.03.21.01: Email Validation Rule
```

### CTR Examples

```markdown
### CTR.02.16.01: Partner API Interface
### CTR.02.17.01: Order Data Model
### CTR.02.20.01: Rate Limit Clause
```

### TASKS Examples

```markdown
### TASKS.02.18.01: Setup Development Environment
### TASKS.02.30.01: Configure CI Pipeline
```

### IMPL Examples

```markdown
### IMPL.02.29.01: Foundation Phase
### IMPL.02.29.02: Integration Phase
```

---

## 9. Pre-Flight Checklist

Run this checklist BEFORE creating any SDD document:

### Document Setup

- [ ] Document ID follows `TYPE-NN` format
- [ ] Filename follows `TYPE-NN_descriptive_slug.md` pattern
- [ ] YAML frontmatter includes correct `artifact_type` and `layer`
- [ ] Not a reserved ID document (TYPE-00_*) requiring exemption

### Element IDs

- [ ] All element IDs use 4-segment dot notation: `TYPE.NN.TT.SS`
- [ ] Element type code (TT) is valid for this document type (see Section 5)
- [ ] Sequential numbers (SS) are unique within the document
- [ ] No legacy patterns (AC-XXX, FR-XXX, DEC-XXX, etc.) are used

### Threshold Tags

- [ ] All `@threshold:` tags include document reference: `TYPE.NN.key`
- [ ] Threshold keys follow category.subcategory.attribute format
- [ ] Categories are from the approved list (perf, timeout, rate, etc.)

### Cross-References

- [ ] Traceability tags use correct prefixes (@brd:, @prd:, @adr:, etc.)
- [ ] Referenced document IDs exist
- [ ] Element ID references are complete (all 4 segments)

---

## 10. Error Recovery

### Detecting Legacy Patterns

Use grep to find legacy patterns:

```bash
# Find all legacy patterns in a file
grep -E "(AC|FR|BC|BA|QA|BO|RISK|METRIC)-[0-9]+" file.md
grep -E "(Event|State|TASK|Phase|IP|IF|DM|CC)-[0-9]+" file.md
grep -E "(DEC|ALT|CON)-[0-9]+" file.md
grep -E "Feature F-[0-9]+" file.md
grep -E "T-[0-9]+" file.md
```

### Migration Procedure

1. **Identify the document type and number** from the filename
   - Example: `BRD-02_requirements.md` → DOC_TYPE=BRD, DOC_NUM=02

2. **Look up the element type code** from Section 5
   - Example: `AC-XXX` → Acceptance Criteria → Code 06
   - Example: `DEC-XXX` → Decision → Code 10

3. **Construct the unified ID**
   - Pattern: `{DOC_TYPE}.{DOC_NUM}.{ELEM_TYPE}.{SEQ}`
   - Example: `AC-001` in BRD-02 → `BRD.02.06.01`
   - Example: `DEC-01` in ADR-05 → `ADR.05.10.01`

4. **Replace all occurrences**
   ```bash
   # Example sed replacement
   sed -i 's/### AC-001:/### BRD.02.06.01:/g' file.md
   sed -i 's/### DEC-01:/### ADR.05.10.01:/g' file.md
   ```

5. **Validate the result**
   ```bash
   # Verify no legacy patterns remain
   grep -E "(AC|FR|BC|BA|DEC|ALT|CON)-[0-9]+" file.md
   ```

### Common Migration Errors

| Error | Cause | Fix |
|-------|-------|-----|
| Wrong element code | Using FR code (01) for Acceptance Criteria | Use code 06 for AC |
| Missing document number | `BRD..06.01` | Include document number: `BRD.02.06.01` |
| Dash instead of dot | `BRD-02-06-01` | Use dots: `BRD.02.06.01` |
| Lowercase type | `brd.02.06.01` | Uppercase: `BRD.02.06.01` |

---

## 11. Source References

### Primary Sources

| Document | Location | Content |
|----------|----------|---------|
| ID Naming Standards | `ai_dev_flow/ID_NAMING_STANDARDS.md` | Document IDs, Element IDs, 31 type codes |
| Threshold Naming Rules | `ai_dev_flow/THRESHOLD_NAMING_RULES.md` | Threshold tags, key formats, categories |

### Validation Rules Files

Each document type has validation rules with Element ID compliance checks:

| Document Type | Validation Rules File |
|---------------|----------------------|
| BRD | `ai_dev_flow/BRD/BRD_VALIDATION_RULES.md` |
| PRD | `ai_dev_flow/PRD/PRD_VALIDATION_RULES.md` |
| EARS | `ai_dev_flow/EARS/EARS_VALIDATION_RULES.md` |
| BDD | `ai_dev_flow/BDD/BDD_VALIDATION_RULES.md` |
| ADR | `ai_dev_flow/ADR/ADR_VALIDATION_RULES.md` |
| SYS | `ai_dev_flow/SYS/SYS_VALIDATION_RULES.md` |
| REQ | `ai_dev_flow/REQ/REQ_VALIDATION_RULES.md` |
| IMPL | `ai_dev_flow/IMPL/IMPL_VALIDATION_RULES.md` |
| CTR | `ai_dev_flow/CTR/CTR_VALIDATION_RULES.md` |
| SPEC | `ai_dev_flow/SPEC/SPEC_VALIDATION_RULES.md` |
| TASKS | `ai_dev_flow/TASKS/TASKS_VALIDATION_RULES.md` |

### Related Skills

| Skill | Purpose |
|-------|---------|
| doc-validator | Automated validation of SDD documents |
| doc-flow | SDD workflow orchestration |
| trace-check | Traceability validation |

---

### Diagram Standards

All diagrams MUST use Mermaid syntax. Text-based diagrams (ASCII art, box drawings) are prohibited.
See: `ai_dev_flow/DIAGRAM_STANDARDS.md` and `mermaid-gen` skill.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.2.0 | 2026-01-17 | Updated to 11 active artifact types; Removed legacy element codes 19, 31 |
| 1.1.0 | 2025-12-29 | Added Reserved ID Exemption, REF document pattern, ADR removed patterns, fixed element type codes for BRD |
| 1.0.0 | 2025-12-19 | Initial release with all 31 element codes and 18 removed patterns |
