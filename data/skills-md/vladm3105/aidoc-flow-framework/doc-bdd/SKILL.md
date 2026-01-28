---
name: doc-bdd
description: Layer 4 artifact for Behavior-Driven Development test scenarios using Gherkin Given-When-Then format
tags:
  - sdd-workflow
  - layer-4-artifact
  - shared-architecture
custom_fields:
  layer: 4
  artifact_type: BDD
  architecture_approaches: [ai-agent-based, traditional-8layer]
  priority: shared
  development_status: active
  skill_category: core-workflow
  upstream_artifacts: [BRD, PRD, EARS]
  downstream_artifacts: [ADR, SYS, REQ]
---

# doc-bdd

## Purpose

Create **BDD (Behavior-Driven Development)** test scenarios - Layer 4 artifact in the SDD workflow that defines executable test scenarios using Gherkin syntax.

**Layer**: 4

**Upstream**: BRD (Layer 1), PRD (Layer 2), EARS (Layer 3)

**Downstream**: ADR (Layer 5), SYS (Layer 6), REQ (Layer 7)

## Prerequisites

### Upstream Artifact Verification (CRITICAL)

**Before creating this document, you MUST:**

1. **List existing upstream artifacts**:
   ```bash
   ls docs/BRD/ docs/PRD/ docs/EARS/ docs/BDD/ 2>/dev/null
   ```

2. **Reference only existing documents** in traceability tags
3. **Use `null`** only when upstream artifact type genuinely doesn't exist
4. **NEVER use placeholders** like `BRD-XXX` or `TBD`
5. **Do NOT create missing upstream artifacts** - skip functionality instead

Before creating BDD, read:

1. **Shared Standards**: `.claude/skills/doc-flow/SHARED_CONTENT.md`
2. **Upstream BRD, PRD, EARS**: Read artifacts that drive these test scenarios
3. **Template**: `ai_dev_flow/BDD/BDD-SECTION-TEMPLATE.feature`
4. **Creation Rules**: `ai_dev_flow/BDD/BDD_CREATION_RULES.md`
5. **Validation Rules**: `ai_dev_flow/BDD/BDD_VALIDATION_RULES.md`
6. **Splitting Rules**: `ai_dev_flow/BDD/BDD_SPLITTING_RULES.md`

## When to Use This Skill

Use `doc-bdd` when:
- Have completed BRD (Layer 1), PRD (Layer 2), EARS (Layer 3)
- Need to define executable test scenarios
- Validating EARS formal requirements with Given-When-Then format
- Creating acceptance criteria for features
- You are at Layer 4 of the SDD workflow

## Section-Based Structure (MANDATORY)

**All BDD suites MUST use section-based structure.** No backward compatibility with legacy formats.

### Directory Structure

```
docs/BDD/
├── BDD-02_knowledge_engine/           # Suite folder
│   ├── BDD-02.0_index.md              # Index file (MANDATORY)
│   ├── BDD-02.1_ingest.feature        # Section 1
│   ├── BDD-02.2_query.feature         # Section 2
│   ├── BDD-02.3.00_learning.feature   # Aggregator (if 5+ subsections)
│   ├── BDD-02.3.01_learning_path.feature    # Subsection 1
│   ├── BDD-02.3.02_bias_detection.feature   # Subsection 2
│   ├── BDD-02_README.md               # Optional companion
│   └── BDD-02_TRACEABILITY.md         # Optional companion
└── BDD-02_knowledge_engine.feature    # Redirect stub (0 scenarios)
```

### Three Valid File Patterns (ONLY)

| Pattern | Example | Use When |
|---------|---------|----------|
| Section-Only | `BDD-02.14_query_result_filtering.feature` | Standard section (≤500 lines, ≤12 scenarios) |
| Subsection | `BDD-02.24.01_quality_performance.feature` | Section requires splitting |
| Aggregator | `BDD-02.12.00_query_graph_traversal.feature` | Organizing multiple subsections (@redirect, 0 scenarios) |

### Prohibited Patterns (ERROR)

| Pattern | Example | Fix |
|---------|---------|-----|
| _partN suffix | `BDD-02_query_part1.feature` | Use `BDD-02.2.01_query.feature` |
| Single-file | `BDD-02_knowledge_engine.feature` (with scenarios) | Use section-based format |
| features/ subdirectory | `BDD-02_slug/features/` | Put `.feature` files at suite folder root |

### Critical Rules

1. **All `.feature` files in suite folder** - No `features/` subdirectory
2. **Index file mandatory**: `BDD-NN.0_index.md` for all suites
3. **Max 500 lines** per `.feature` file (soft limit: 400)
4. **Max 12 scenarios** per Feature block
5. **Section metadata tags required**: `@section`, `@parent_doc`, `@index`

## Gherkin Syntax

### Feature File Structure

```gherkin
# Traceability Tags (Gherkin-native, NOT in comments)
@section: 2.14
@parent_doc: BDD-02
@index: BDD-02.0_index.md
@brd:BRD.02.01.03
@prd:PRD.02.07.02
@ears:EARS.02.14.01

Feature: BDD-02.14: Query Result Filtering
  As a data analyst
  I want filtered query results
  So that I can focus on relevant data

  Background:
    Given the system timezone is "America/New_York"
    And the current time is "09:30:00" in "America/New_York"

  @primary @functional
  Scenario: Successful filter application
    Given valid filter criteria
    When user applies filter
    Then filtered results are returned
    And response time is less than @threshold:PRD.02.perf.api.p95_latency
```

### Tags Placement (CRITICAL - E041)

**Tags MUST be Gherkin-native, NOT in comments.**

```gherkin
# INVALID (frameworks cannot parse comment-based tags):
# @brd: BRD.01.01.01
# @prd: PRD.01.01.01
Feature: My Feature

# VALID (Gherkin-native tags before Feature):
@brd:BRD.01.01.01
@prd:PRD.01.01.01
@ears:EARS.01.24.01
Feature: My Feature
```

### Times and Timezones (MANDATORY)

- All times include seconds: `HH:MM:SS`
- Use IANA timezone format: `America/New_York`, `America/Los_Angeles`
- Avoid ambiguous abbreviations (EST/EDT/PST/PDT)

```gherkin
Given the current time is "14:30:00" in "America/New_York"
And the system timezone is "America/New_York"
```

## Unified Element ID Format (MANDATORY)

**Pattern**: `BDD.{DOC_NUM}.{ELEM_TYPE}.{SEQ}` (4 segments, dot-separated)

| Element Type | Code | Example |
|--------------|------|---------|
| Test Scenario | 14 | BDD.02.14.01 |
| Step | 15 | BDD.02.15.01 |

> **REMOVED PATTERNS** - Do NOT use:
> - `SCENARIO-XXX`, `TS-XXX` → Use `BDD.NN.14.SS`
> - `STEP-XXX` → Use `BDD.NN.15.SS`
> - `TC-XXX` → Use `BDD.NN.14.SS`

## ADR-Ready Scoring System

**Purpose**: Measures BDD maturity and readiness for ADR progression.

**Format in Document Control**:
```markdown
| **ADR-Ready Score** | ✅ 95% (Target: ≥90%) |
```

### Status and ADR-Ready Score Mapping

| ADR-Ready Score | Required Status |
|-----------------|-----------------|
| ≥90% | Approved |
| 70-89% | In Review |
| <70% | Draft |

### Scoring Criteria

**Scenario Completeness (35%)**:
- All EARS statements translated to BDD scenarios: 15%
- Comprehensive coverage (success/error/edge): 15%
- Observable verification methods specified: 5%

**Testability (30%)**:
- Scenarios are automatable: 15%
- Data-driven Examples tables used: 10%
- Performance benchmarks quantifiable: 5%

**Architecture Requirements Clarity (25%)**:
- Performance, security, scalability quality attributes specified: 15%
- Integration points and external dependencies defined: 10%

**Business Validation (10%)**:
- Business acceptance criteria traceable: 5%
- Measurable success outcomes defined: 5%

**Quality Gate**: Score <90% blocks ADR artifact creation.

## Threshold Registry Integration (MANDATORY)

**All quantitative values MUST use `@threshold:` keys.** No hardcoded magic numbers.

### Inline Step Format

```gherkin
# INVALID (hardcoded):
Then response time is less than 200ms

# VALID (threshold reference):
Then response time is less than @threshold:PRD.035.perf.api.p95_latency
```

### Scenario Tag Format

```gherkin
@threshold:PRD.NN.perf.api.p95_latency
Scenario: API responds within performance threshold
```

### Common Threshold Categories

| Category | BDD Usage | Example Key |
|----------|-----------|-------------|
| `perf.*` | Performance validation | `perf.api.p95_latency` |
| `sla.*` | SLA validation | `sla.uptime.target` |
| `limit.*` | Rate limit testing | `limit.api.requests_per_second` |
| `timeout.*` | Timeout validation | `timeout.request.sync` |

## Cumulative Tagging Requirements

**Layer 4 (BDD)**: Must include tags from Layers 1-3 (BRD, PRD, EARS)

**Tag Count**: 3+ tags (@brd, @prd, @ears)

**Format** (Gherkin-native tags before Feature):
```gherkin
@brd:BRD.01.01.03
@prd:PRD.01.07.02
@ears:EARS.01.24.01
Feature: Feature Name
```

## Tag Format Convention

| Notation | Format | Artifacts | Purpose |
|----------|--------|-----------|---------|
| Dash | TYPE-NN | ADR, SPEC, CTR | Technical artifacts - document references |
| Dot | TYPE.NN.TT.SS | BRD, PRD, EARS, BDD, SYS, REQ | Hierarchical artifacts - element references |

## Scenario Types

**All 8 categories should be represented:**

| Category | Tag | Description |
|----------|-----|-------------|
| Success Path | `@primary` | Happy path scenarios |
| Alternative Path | `@alternative` | Optional parameters, different workflows |
| Error Conditions | `@negative` | Invalid inputs, error handling |
| Edge Cases | `@edge_case`, `@boundary` | Boundary conditions, limits |
| Data-Driven | `@data_driven` | Parameterized with Examples tables |
| Integration | `@integration` | External system interactions |
| Quality Attributes | `@quality_attribute` | Performance, security, reliability |
| Failure Recovery | `@failure_recovery` | Error recovery, circuit breakers |

### Success Path Example

```gherkin
@primary @functional
Scenario: User logs in successfully
  Given valid credentials
  When user submits login
  Then user is authenticated
```

### Error Conditions Example

```gherkin
@negative @error_handling
Scenario: Trade rejected due to insufficient funds
  Given account balance is $1000
  When trade requires $5000
  Then trade is rejected
  And error code "INSUFFICIENT_FUNDS" is returned
```

### Edge Cases Example

```gherkin
@edge_case @boundary
Scenario: Trade at exact position limit
  Given current delta is 0.499
  And position limit is 0.50
  When trade increases delta to 0.50
  Then trade is accepted
```

### Data-Driven Example

```gherkin
@data_driven
Scenario Outline: Validate price precision
  Given instrument <symbol>
  When price is <price>
  Then precision should be <decimals> decimal places
  Examples:
    | symbol | price  | decimals |
    | SPY    | 450.25 | 2        |
    | AMZN   | 3250.5 | 1        |
```

## Section Metadata Requirements

All `.feature` files MUST include section metadata tags:

```gherkin
@section: NN.SS              # Section number (e.g., 2.1, 2.14)
@parent_doc: BDD-NN          # Parent BDD suite (e.g., BDD-02)
@index: BDD-NN.0_index.md    # Index file reference
@brd:BRD.NN.EE.SS            # Upstream BRD element
@prd:PRD.NN.EE.SS            # Upstream PRD element
@ears:EARS.NN.SS.RR          # Upstream EARS requirement
```

**For subsections, add**:
```gherkin
@parent_section: NN.SS       # Parent section number
```

**Feature Title Format**:
```gherkin
Feature: BDD-NN.SS: Domain Description
```

## Aggregator Files

**Use when**: Section has 5+ subsections

**Requirements**:
- `@redirect` tag MUST be present
- 0 scenarios (redirect stub only)
- List subsections in Feature description

```gherkin
@redirect
@section: 2.12.00
@parent_doc: BDD-02
@index: BDD-02.0_index.md

Feature: BDD-02.12: Query Graph Traversal (Aggregator)

  This is a redirect stub. Test scenarios are in subsections:
  - BDD-02.12.01_depth_first.feature - Depth-first traversal tests
  - BDD-02.12.02_breadth_first.feature - Breadth-first traversal tests

Background:
  Given the system timezone is "America/New_York"
  # No scenarios in aggregator - redirect only
```

## Index File Template

**Mandatory**: `BDD-NN.0_index.md` for each suite

```markdown
# BDD-02.0: Knowledge Engine Test Suite Index

## Suite Overview
**Purpose**: Test scenarios for Knowledge Engine functionality
**Scope**: Ingest, Query, Learning, Performance Monitoring

## Section File Map
| Section | File | Scenarios | Lines | Status | Description |
|---------|------|-----------|-------|--------|-------------|
| 02.1 | BDD-02.1_ingest.feature | 8 | 350 | Active | Ingest tests |
| 02.2 | BDD-02.2_query.feature | 10 | 420 | Active | Query tests |

## Traceability Matrix
| BDD Section | Upstream Source | Description |
|-------------|----------------|-------------|
| BDD-02.1 | EARS.02.01-05 | Ingest requirements |
| BDD-02.2 | EARS.02.06-12 | Query requirements |
```

## Creation Process

### Step 1: Read Upstream Artifacts

Read BRD, PRD, and EARS to understand requirements to test.

### Step 2: Reserve Suite ID

Check `docs/BDD/` for next available ID (e.g., BDD-01, BDD-02).

**ID Numbering Convention**: Start with 2 digits and expand only as needed.
- ✅ Correct: BDD-01, BDD-99, BDD-102
- ❌ Incorrect: BDD-001, BDD-009 (extra leading zero not required)

### Step 3: Create Suite Folder

```bash
mkdir -p docs/BDD/BDD-02_knowledge_engine/
```

### Step 4: Create Index File

```bash
cp ai_dev_flow/BDD/BDD-SECTION-0-TEMPLATE.md docs/BDD/BDD-02_knowledge_engine/BDD-02.0_index.md
```

### Step 5: Design Section Split

- Identify logical domains or EARS groupings
- Estimate scenarios per section (target: 6-10)
- Plan for subsections if needed (>500 lines)

### Step 6: Create Section Files

```bash
cp ai_dev_flow/BDD/BDD-SECTION-TEMPLATE.feature docs/BDD/BDD-02_knowledge_engine/BDD-02.1_ingest.feature
```

### Step 7: Add Section Metadata Tags

- `@section`, `@parent_doc`, `@index`
- Upstream traceability: `@brd`, `@prd`, `@ears`

### Step 8: Write Scenarios

For each requirement from EARS/PRD:
1. Success path scenario
2. Error condition scenarios (2-3)
3. Edge case scenarios (1-2)
4. Scenario outlines for parameterized tests

### Step 9: Replace Magic Numbers with Thresholds

- Add to PRD threshold registry first if key missing
- Use `@threshold:PRD.NN.category.key` format

### Step 10: Create Redirect Stub

```bash
# Create redirect stub at docs/BDD/ root
touch docs/BDD/BDD-02_knowledge_engine.feature
```

Add minimal content with `@redirect` tag and 0 scenarios.

### Step 11: Update Index File

- List all section files with scenario counts
- Add traceability matrix

### Step 12: Validate BDD Suite

```bash
python3 scripts/validate_bdd_suite.py --root BDD
```

### Step 13: Commit Changes

Commit suite folder and redirect stub together.

## Validation

### Validation Error Codes Reference

| Code | Description | Severity |
|------|-------------|----------|
| E001 | Document Control fields missing | ERROR |
| E002 | Gherkin syntax invalid | ERROR |
| E003 | ADR-Ready Score format invalid | ERROR |
| E004 | Upstream traceability tags missing | ERROR |
| E041 | Tags in comments (not Gherkin-native) | ERROR |
| E008 | Element ID format invalid | ERROR |
| CHECK 9.1 | File naming pattern invalid | ERROR |
| CHECK 9.2 | Prohibited pattern detected | ERROR |
| CHECK 9.3 | Aggregator requirements not met | ERROR |
| CHECK 9.4 | File size exceeds limits | ERROR |
| CHECK 9.5 | Section metadata tags missing | ERROR |
| CHECK 9.6 | Index file missing | ERROR |
| CHECK 9.7 | Non-Gherkin content in .feature file | ERROR |

### Manual Checklist

**File Structure**:
- [ ] All `.feature` files in suite folder (no `features/` subdirectory)
- [ ] Index file exists: `BDD-NN.0_index.md`
- [ ] Redirect stub at `docs/BDD/BDD-NN_slug.feature` (0 scenarios)
- [ ] No file exceeds 500 lines
- [ ] No Feature block exceeds 12 scenarios

**File Naming**:
- [ ] All files match one of 3 valid patterns
- [ ] No prohibited patterns (_partN, single-file)

**Tags and Metadata**:
- [ ] Tags are Gherkin-native (NOT in comments)
- [ ] Section metadata: `@section`, `@parent_doc`, `@index`
- [ ] Cumulative tags: `@brd`, `@prd`, `@ears`
- [ ] All quantitative values use `@threshold:` keys
- [ ] Times include seconds (HH:MM:SS) with IANA timezone

**Scenarios**:
- [ ] All 8 scenario categories represented
- [ ] Given-When-Then structure
- [ ] No subjective language ("fast", "reliable")
- [ ] Observable outcomes in Then steps

**Aggregators** (if applicable):
- [ ] Has `@redirect` tag
- [ ] Has 0 scenarios
- [ ] Lists subsections in Feature description

## Common Pitfalls

| Mistake | Correction |
|---------|------------|
| Tags in comments `# @brd:` | Use Gherkin-native `@brd:` before Feature |
| `ADR-Ready Score: 95%` | Use `✅ 95% (Target: ≥90%)` |
| `response time < 200ms` (hardcoded) | Use `@threshold:PRD.NN.perf.api.p95_latency` |
| `.feature` in `features/` subdir | Put at suite folder root |
| `BDD-02_query_part1.feature` | Use `BDD-02.2.01_query.feature` |
| Missing @ears tag | All 3 upstream tags are MANDATORY |
| Only success scenarios | Include all 8 scenario categories |
| `Status: Approved` (with <90% score) | Use `Status: In Review` or `Draft` |
| File >500 lines | Split into subsections |
| `09:30` (no seconds) | Use `09:30:00` |
| `EST` timezone | Use `America/New_York` |

## Post-Creation Validation (MANDATORY)

**CRITICAL**: Execute validation loop IMMEDIATELY after document creation.

### Automatic Validation Loop

```
LOOP:
  1. Run: python scripts/validate_bdd_suite.py --root BDD
  2. IF errors fixed: GOTO LOOP (re-validate)
  3. IF warnings fixed: GOTO LOOP (re-validate)
  4. IF unfixable issues: Log for manual review
  5. IF clean: Mark VALIDATED, proceed
```

### Quality Gate

**Blocking**: YES - Cannot proceed to ADR creation until validation passes with 0 errors.

---

## Reserved ID Exemption

**Pattern**: `BDD-00_*.md` or `BDD-00_*.feature`

**Scope**: Documents with reserved ID `000` are FULLY EXEMPT from validation.

**Document Types**:
- Index documents (`BDD-00_index.md`)
- Traceability matrix templates
- Glossaries, registries, checklists

---

## Next Skill

After creating BDD, use:

**`doc-adr`** - Create Architecture Decision Records (Layer 5)

The ADR will:
- Document architectural decisions for topics identified in BRD/PRD
- Include `@brd`, `@prd`, `@ears`, `@bdd` tags (cumulative)
- Use Context-Decision-Consequences format
- Reference BDD scenarios that validate the architecture

## Related Resources

- **Template**: `ai_dev_flow/BDD/BDD-SECTION-TEMPLATE.feature`
- **Index Template**: `ai_dev_flow/BDD/BDD-SECTION-0-TEMPLATE.md`
- **Subsection Template**: `ai_dev_flow/BDD/BDD-SUBSECTION-TEMPLATE.feature`
- **Aggregator Template**: `ai_dev_flow/BDD/BDD-AGGREGATOR-TEMPLATE.feature`
- **Creation Rules**: `ai_dev_flow/BDD/BDD_CREATION_RULES.md`
- **Validation Rules**: `ai_dev_flow/BDD/BDD_VALIDATION_RULES.md`
- **Splitting Rules**: `ai_dev_flow/BDD/BDD_SPLITTING_RULES.md`
- **Shared Standards**: `.claude/skills/doc-flow/SHARED_CONTENT.md`
- **ID Standards**: `ai_dev_flow/ID_NAMING_STANDARDS.md`

## Quick Reference

| Item | Value |
|------|-------|
| **Purpose** | Define executable test scenarios |
| **Layer** | 4 |
| **Tags Required** | @brd, @prd, @ears (3 tags) |
| **ADR-Ready Score** | ≥90% required for "Approved" status |
| **Element ID Format** | `BDD.NN.14.SS` (scenarios), `BDD.NN.15.SS` (steps) |
| **File Structure** | Nested suite folder: `docs/BDD/BDD-NN_{slug}/` |
| **Max File Size** | 500 lines (soft: 400) |
| **Max Scenarios** | 12 per Feature block |
| **Time Format** | HH:MM:SS with IANA timezone |
| **Quantitative Values** | Use `@threshold:PRD.NN.category.key` |
| **Next Skill** | doc-adr |
