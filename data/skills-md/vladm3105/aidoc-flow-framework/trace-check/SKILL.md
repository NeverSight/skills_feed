---
title: "trace-check: Validate bidirectional traceability across SDD artifacts"
name: trace-check
description: Validate and update bidirectional traceability across SDD artifacts
tags:
  - sdd-workflow
  - shared-architecture
  - quality-assurance
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

# trace-check

## Purpose

Automated traceability validation across all SDD artifacts.

**Core Functions**:
- Validates bidirectional link consistency (upstream/downstream symmetry)
- Verifies ID format compliance (TYPE-XXX or TYPE-XXX-YY)
- Tests markdown link resolution (file paths and anchors)
- **NEW**: Validates cumulative tagging hierarchy (each layer includes ALL upstream tags)
- **NEW**: Layer-specific tag count validation (artifacts at layer N must have tags from layers 1 through N-1)
- Calculates coverage metrics (% artifacts with complete traceability)
- Detects orphaned artifacts (no upstream or downstream links)
- Auto-fixes broken links with backup creation

**SDD Workflow** (v2.0 - Functional Layer Groupings):
```
Business Layer: BRD → PRD → EARS →
Testing Layer: BDD →
Architecture Layer: ADR → SYS →
Requirements Layer: REQ →
Implementation Strategy Layer: IMPL (optional) →
Interface Layer: CTR (optional) →
Technical Specs Layer: SPEC →
Execution Planning Layer: TASKS →
Code & Validation Layer: Code → Tests → Validation → Review → Production
```

**Reference**: [TRACEABILITY.md v2.0]({project_root}/ai_dev_flow/TRACEABILITY.md) (updated 2025-10-31)

**Complexity**: Medium (requires parsing multiple file formats)

**Resource Requirements**:
- CPU: Moderate (file parsing, regex matching)
- Memory: 100-500MB for 100-200 artifacts
- Disk: 1-10MB for backup archives
- Network: None (local file operations only)

**Failure Modes**:
- Invalid ID format: Reports non-compliant document IDs
- Broken links: Reports file paths that do not resolve
- Missing anchors: Reports markdown anchors not found in target files
- Bidirectional gaps: Reports asymmetric traceability links
- Orphaned artifacts: Reports documents with no upstream or downstream references

## When to Use This Skill

**Use trace-check when**:
- Before committing changes to documentation
- After creating new artifacts (BRD, PRD, SPEC, etc.)
- After updating existing artifacts
- During periodic audits (weekly/sprint/release)
- Validating traceability matrix completeness
- Detecting orphaned artifacts
- Verifying ID format compliance
- Establishing baseline quality metrics

**Do NOT use trace-check when**:
- Working on code implementation (use code review tools)
- Validating code traceability (use docstring validators)
- For non-SDD documentation projects
- During active editing sessions (wait until stable state)

## Skill Inputs

| Input | Type | Description | Example/Default |
|-------|------|-------------|-----------------|
| project_root_path | Required | Path to project documentation root | `{project_root}/docs/` |
| artifact_types | Optional | Specific artifact types to validate | `["BRD", "SPEC"]` or `["all"]` (default) |
| strictness_level | Optional | Validation strictness | `"strict"` (default), `"permissive"`, `"pedantic"` |
| validate_cumulative | Optional | **NEW**: Validate cumulative tagging hierarchy | `true` or `false` (default) |
| auto_fix | Optional | Auto-fix broken links | `true` or `false` (default) |
| report_format | Optional | Output report format | `"markdown"` (default), `"json"`, `"text"` |

**Strictness Levels**:
- `permissive`: Warnings only, no failures for missing reverse links
- `strict`: Fails on broken links and missing bidirectional consistency
- `pedantic`: Fails on any traceability gaps including "To Be Created" sections

## Skill Workflow

### Step 1: Discover All Artifacts

**Actions**:
- Scan `docs/` directory for all artifact types
- Parse filenames to extract document IDs (BRD-01, SPEC-01, etc.)
- Build artifact inventory with file paths
- Filter by artifact_types parameter if specified

**Expected Results**:
- 50-200 artifacts per project
- Inventory mapping: ID → file path
- Coverage: All .md, .yaml, .feature files

**Validation**:
- Verify directory structure: `docs/{TYPE}/` exists
- Confirm file naming: `{TYPE}-{XXX}_{description}.{ext}`
- Check for duplicate IDs within same type

### Step 2: Parse Traceability Sections

**Actions**:
- Read each artifact's Section 7 "Traceability"
- Extract upstream sources (documents this derives from)
- Extract downstream artifacts (documents derived from this)
- Parse markdown links: `[ID](path#anchor)` format
- Store bidirectional relationship map

**Markdown Pattern Recognition**:
```
**Upstream Sources:**
- [BRD-01](../BRD/BRD-01_file.md#BRD-01) - Title (Status, Date)

**Downstream Artifacts:**
**In Progress:**
- [SPEC-01](../SPEC/SPEC-01_file.yaml#anchor) - Title (Status, Date)

**To Be Created:**
- SPEC-02+: Description (TBD)
```

**Data Structure**:
- Upstream map: {artifact_id: [upstream_ids]}
- Downstream map: {artifact_id: [downstream_ids]}
- Link details: {source_id, target_id, file_path, line_number, anchor}

### Step 2.5: Extract Traceability Tags from Code

**Actions**:
1. Scan all source files (.py, .md, .yaml, .feature) for tag patterns
2. Parse @brd:, @sys:, @spec:, @test:, @impl-status: tags
3. Validate format: TYPE.NN.TT.SS (4-segment unified format)
4. Build tag-to-document mapping
5. Cross-reference with actual document existence

**Tag Extraction Regex**:
```python
import re

TAG_PATTERN = r'@(\w+(?:-\w+)?):\s*([\w\.\-]+(?:[\.:]\w[\w\.\-]*)?(?:\s*,\s*[\w\.\-]+(?:[\.:]\w[\w\.\-]*)?)*)'

# Example matches (unified TYPE.NN.TT.SS format):
# @brd: BRD.01.01.30, BRD.01.01.03
# @sys: SYS.01.25.08
# @spec: SPEC-003
# @test: BDD.01.13.01
```

**Validation Rules**:
1. **Format Check:** All @brd/@prd tags must use unified TYPE.NN.TT.SS format (4-segment)
2. **Document Exists:** DOCUMENT-ID must reference existing file in docs/{TYPE}/
3. **Requirement Exists:** REQUIREMENT-ID must exist within the document
4. **No Orphans:** All tags must resolve to actual requirements
5. **Implementation Status:** @impl-status must be one of: pending|in-progress|complete|deprecated

**Output**:
```json
{
  "src/[project_module]/gateway/connection_service.py": {
    "tags": {
      "brd": ["BRD.01.01.01", "BRD.01.01.02", "BRD.01.01.03"],
      "sys": ["SYS.01.25.01", "SYS.01.25.02"],
      "spec": ["SPEC-01"],
      "test": ["BDD.01.13.01", "BDD.07.13.01"],
      "impl-status": ["complete"]
    },
    "line_numbers": {
      "BRD.01.01.01": 15,
      "BRD.01.01.02": 15
    }
  }
}
```

**Error Detection**:
- ❌ `@brd: 030` - Missing document and element ID
- ❌ `@brd: BRD.99.01.01` - Document BRD-99 doesn't exist
- ❌ `@brd: BRD.01.01.99` - Element 99 not in BRD-01
- ✅ `@brd: BRD.01.01.30` - Valid format and exists

**Scripts**:
```bash
# Extract tags
python scripts/extract_tags.py --source src/ docs/ tests/ --output docs/generated/tags.json

# Validate tags against documents
python scripts/validate_tags_against_docs.py --tags docs/generated/tags.json --strict

# Generate matrices
python scripts/generate_traceability_matrices.py --tags docs/generated/tags.json --output docs/generated/matrices/
```

### Step 2.6: Validate Cumulative Tagging Hierarchy

**Actions**:
1. For each artifact, determine its position in the artifact sequence (0-15+)
2. Verify artifact includes ALL required upstream tags for its artifact type
3. Check tag count matches expected range for artifact type
4. Validate optional artifacts (IMPL, CTR) handled correctly
5. Ensure tag chain completeness (if @adr exists, @brd through @bdd must exist)

**Expected Cumulative Tag Counts by Artifact Type**:
```
Business Layer:
  Strategy: 0 tags (external business docs)
  BRD: 0 tags (top level)
  PRD: 1 tag (@brd)
  EARS: 2 tags (@brd, @prd)

Testing Layer:
  BDD: 3+ tags (@brd through @ears)

Architecture Layer:
  ADR: 4 tags (@brd through @bdd)
  SYS: 5 tags (@brd through @adr)

Requirements Layer:
  REQ: 6 tags (@brd through @sys)

Implementation Strategy Layer:
  IMPL: 7 tags (@brd through @req) [optional]

Interface Layer:
  CTR: 8 tags (@brd through @impl) [optional]

Technical Specs Layer:
  SPEC: 7-9 tags (@brd through @req + optional impl/ctr)

Execution Planning Layer:
  TASKS: 8-10 tags (@brd through @spec)

Code & Validation Layer:
  Code: 9-11 tags (@brd through @tasks)
  Tests: 10-12 tags (@brd through @code)
  Validation: ALL tags from all upstream artifacts
```

**Note**: Functional layers group artifacts by purpose in the workflow. Tag counts accumulate as artifacts progress through the layers. Numbers indicate artifact sequence position (0-14) in the 15-layer architecture.

**Validation Script**:
```bash
# Validate cumulative tagging hierarchy compliance
python scripts/validate_tags_against_docs.py \
  --source src/ docs/ tests/ \
  --docs docs/ \
  --validate-cumulative \
  --strict
```

**Validation Rules**:
1. **Complete Chain**: Each artifact must include ALL upstream tags
2. **Artifact Type Validation**: Artifacts must have all tags from previous functional layers
3. **Optional Layers**: IMPL and CTR are optional; downstream artifacts adjust tag count accordingly
4. **Tag Chain Completeness**: If higher layer tag exists (e.g., @adr), all lower layer tags must exist (@brd through @bdd)
5. **No Gaps**: No missing tags in the cumulative chain

**Error Detection**:
- ❌ `SPEC missing @brd tag` - Incomplete upstream chain
- ❌ `REQ has @adr but missing @bdd` - Gap in cumulative chain
- ❌ `Code has 8 tags but should have 9-11` - Incorrect tag count for artifact type
- ✅ `SPEC has all 9 required tags (@brd through @spec)` - Valid cumulative tagging

**Benefits**:
- Regulatory compliance (SEC, FINRA, FDA, ISO audit trails)
- Complete impact analysis (upstream → downstream traceability)
- Automated validation prevents gaps in traceability chain
- CI/CD enforcement ensures 100% compliance

### Step 3: Validate ID Format Compliance

**Checks**:
- ID format: `TYPE-XXX` or `TYPE-XXX-YY`
- H1 header contains full ID: `# BRD-01`
- Zero-padding: `001` not `1`
- No ID collisions (each XXX unique per type)
- Valid TYPE: BRD, PRD, EARS, BDD, ADR, SYS, REQ, IMPL, CTR, SPEC, TASKS
- **CTR dual-file validation**: For each CTR, both .md and .yaml must exist with matching slugs (see below)

**Reference**: `{project_root}/ai_dev_flow/ID_NAMING_STANDARDS.md`

**Failure Examples**:
- `BRD-9` → Should be `BRD-009`
- `SPEC-1` → Should be `SPEC-01`
- `REQ-42` → Should be `REQ-042`

### Step 3.5: Validate CTR Dual-File Format (MANDATORY)

**Purpose**: Ensure all CTR artifacts comply with dual-file format requirement (.md + .yaml)

**Actions**:
1. Scan `docs/CTR/` for all CTR files
2. Group by CTR-ID (extract from filename)
3. For each CTR-ID, verify:
   - Both `CTR-XXX_{slug}.md` and `CTR-XXX_{slug}.yaml` exist
   - Slug portion matches exactly in both filenames
   - YAML file contains valid schema (JSON Schema, OpenAPI, or AsyncAPI)
4. Report missing files, slug mismatches, or invalid schemas

**Validation Logic**:
```python
def validate_ctr_dual_files(contracts_dir):
    """Validate CTR dual-file format compliance."""
    errors = []
    ctr_files = glob(f"{contracts_dir}/CTR-*.{{md,yaml}}")

    # Group files by CTR-ID
    ctr_groups = {}
    for filepath in ctr_files:
        filename = os.path.basename(filepath)
        # Extract: CTR-XXX_{slug}.ext → (CTR-XXX, slug, ext)
        match = re.match(r'(CTR-\d{3}(?:-\d{2})?)_(.+)\.(md|yaml)$', filename)
        if match:
            ctr_id, slug, ext = match.groups()
            if ctr_id not in ctr_groups:
                ctr_groups[ctr_id] = {}
            ctr_groups[ctr_id][ext] = (filepath, slug)

    # Validate each CTR group
    for ctr_id, files in ctr_groups.items():
        # Check both files exist
        if 'md' not in files:
            errors.append(f"{ctr_id}: Missing .md file (MANDATORY)")
        if 'yaml' not in files:
            errors.append(f"{ctr_id}: Missing .yaml file (MANDATORY)")

        # Check slug matches
        if 'md' in files and 'yaml' in files:
            md_slug = files['md'][1]
            yaml_slug = files['yaml'][1]
            if md_slug != yaml_slug:
                errors.append(
                    f"{ctr_id}: Slug mismatch - "
                    f"MD: '{md_slug}' vs YAML: '{yaml_slug}'"
                )

        # Validate YAML schema (basic check)
        if 'yaml' in files:
            yaml_path = files['yaml'][0]
            try:
                with open(yaml_path) as f:
                    schema = yaml.safe_load(f)
                    # Check for required schema fields
                    if not isinstance(schema, dict):
                        errors.append(f"{ctr_id}: YAML must be a dictionary/object")
                    elif 'openapi' not in schema and 'asyncapi' not in schema:
                        # Warn if not OpenAPI/AsyncAPI (may be custom JSON Schema)
                        errors.append(
                            f"{ctr_id}: YAML missing 'openapi' or 'asyncapi' field "
                            "(expected standard schema format)"
                        )
            except Exception as e:
                errors.append(f"{ctr_id}: Invalid YAML - {str(e)}")

    return errors
```

**Error Examples**:
- `CTR-01: Missing .yaml file (MANDATORY)` → Only .md exists
- `CTR-002: Missing .md file (MANDATORY)` → Only .yaml exists
- `CTR-003: Slug mismatch - MD: 'api_contract' vs YAML: 'api_spec'` → Slugs don't match
- `CTR-004: YAML missing 'openapi' or 'asyncapi' field` → Schema format unclear
- `CTR-005: Invalid YAML - parsing error at line 42` → Malformed YAML

**Success Criteria**:
- ✅ All CTR artifacts have both .md and .yaml files
- ✅ All slug portions match exactly
- ✅ All YAML files parse successfully
- ✅ All YAML files contain valid schema structure (OpenAPI, AsyncAPI, or JSON Schema)

### Step 3.6: Validate Architecture Decision Topics (NEW)

**Purpose**: Validate architecture topic subsections across BRD Section 7.2, PRD Section 18, and ADR Section 4.1 for layer separation compliance.

**Layer Separation Principle**:
```
BRD Section 7.2          →    PRD Section 18         →    ADR Section 4.1
(WHAT & WHY)                  (HOW to evaluate)          (Final decision)
─────────────────────────────────────────────────────────────────────────
Business drivers              Technical options          Selected option
Business constraints          Evaluation criteria        Trade-off analysis
```

**Subsection ID Format**: `{DOC_TYPE}.NN.EE.SS` (3-digit topic number)

| Component | Description | Example |
|-----------|-------------|---------|
| `{DOC_TYPE}` | Document type | `BRD` |
| `.NNN` | Document number (3-4 digits) | `.001` = BRD-01 |
| `.NNN` | Sequential topic number (3 digits, 001-999) | `.003` = third topic |

**Validation Logic**:
```python
def validate_architecture_topics(docs_dir):
    """Validate architecture decision topic traceability."""
    errors = []

    # 1. Extract BRD Section 7.2 topics
    brd_topics = extract_brd_section_72_topics(docs_dir)

    # 2. Validate topic ID format
    for topic_id, content in brd_topics.items():
        if not re.match(r'^[A-Z]+\.\d{2,9}\.\d{2,9}\.\d{2,9}$', topic_id):
            errors.append(f"{topic_id}: Invalid format (expected {{DOC_TYPE}}.NN.EE.SS)")

        # 3. Check business-only content (no technical options)
        if has_technical_content(content):
            errors.append(f"{topic_id}: Contains technical content (should be business-only)")

    # 4. Validate PRD Section 18 elaborations
    prd_topics = extract_prd_section_18_topics(docs_dir)
    for topic_id, content in prd_topics.items():
        # Check upstream reference exists
        if content.get('upstream') not in brd_topics:
            errors.append(f"PRD {topic_id}: Upstream BRD topic not found")

        # Check has technical content
        if not has_technical_options(content):
            errors.append(f"PRD {topic_id}: Missing technical options")

    # 5. Validate ADR Section 4.1 originating topics
    adr_topics = extract_adr_originating_topics(docs_dir)
    for adr_id, content in adr_topics.items():
        topic_ref = content.get('originating_topic')
        if topic_ref and topic_ref not in brd_topics:
            errors.append(f"{adr_id}: Originating topic {topic_ref} not found in BRD")

    return errors
```

**Content Validation Rules**:

| Layer | Section | Required Content | Forbidden Content |
|-------|---------|------------------|-------------------|
| BRD (Layer 1) | 7.2 | Business Driver, Business Constraints | Technical options, Evaluation criteria |
| PRD (Layer 2) | 18 | Technical Options, Evaluation Criteria, Upstream reference | Business constraints (duplicated from BRD) |
| ADR (Layer 5) | 4.1 | Originating Topic, Decision, References | Missing upstream references |

**Validation Regex Patterns**:
```python
# BRD Section 7.2 subsection header (H3-H5 depending on document context)
ARCHITECTURE_TOPIC_PATTERN = r'^#{3,5}\s+([A-Z]+\.\d{2,}\.\d{3}):\s+.+'

# PRD Section 18 upstream reference (3-digit topic number)
PRD_UPSTREAM_PATTERN = r'\*\*Upstream\*\*:\s*BRD-\d{2,}\s+§7\.2\.\d{3}'

# ADR Section 4.1 originating topic
ADR_ORIGINATING_PATTERN = r'\*\*Originating Topic\*\*:\s*([A-Z]+\.\d{2,}\.\d{3})\s*-\s*.+'
```

**Cross-Reference Validation**:
1. Each BRD Section 7.2 topic should have corresponding PRD Section 18 elaboration
2. Each PRD Section 18 topic should reference ADR (pending or actual)
3. Each ADR Section 4.1 should reference originating BRD topic

**Error Examples**:
- `BRD.001.01: Invalid format` → Should be `BRD.001.001` (3-digit topic)
- `BRD.001.1: Invalid format` → Should be `BRD.001.001` (3-digit topic)
- `BRD.001.001: Contains technical content` → "WebSocket" in BRD (move to PRD)
- `PRD 18.1: Upstream BRD topic not found` → References non-existent BRD topic
- `ADR-01: Originating topic BRD.999.001 not found` → Invalid topic reference

**Success Criteria**:
- ✅ All BRD Section 7.2 topics use `{DOC_TYPE}.NN.EE.SS` format
- ✅ All BRD Section 7.2 topics contain business-only content
- ✅ All PRD Section 18 topics reference valid BRD topics
- ✅ All PRD Section 18 topics contain technical elaboration
- ✅ All ADR Section 4.1 topics reference valid originating topics

### Step 4: Check Link Resolution

**Tests**:
- File exists: All markdown link paths resolve
- Relative paths: Correct from source file location
- Anchors exist: All `#anchor` references valid
- YAML files: Check `id:` field matches anchor
- Feature files: Verify `Scenario:` lines create anchors

**Relative Path Calculation**:
- From: `/docs/SPEC/SPEC-01.yaml`
- To: `/docs/BRD/BRD-01.md`
- Link: `[BRD-01](../BRD/BRD-01.md#BRD-01)`

**Anchor Validation**:
- Markdown: `# BRD-01` → anchor `#BRD-01`
- YAML: `id: ib_gateway_connection_service` → anchor `#ib_gateway_connection_service`
- Feature: `Scenario: User connects to IB Gateway` → anchor varies

**Failure Examples**:
- Link: `[SPEC-01](../SPEC/SPEC-01.yaml)` → File not found
- Link: `[BRD-01](../BRD/BRD-01.md#BRD-02)` → Anchor mismatch

### Step 5: Generate Bidirectional Consistency from Tags

**Logic - Tag-Based Approach**:
- Extract tags from code and documentation
- Build forward matrix: Requirements → Implementing files
- Build reverse matrix: Files → Requirements
- Auto-generate bidirectional traceability matrices
- Validate tag references against actual documents

**Forward Matrix (BRD → Code)**:
```markdown
| Requirement | Implementing Files | Status |
|-------------|-------------------|--------|
| BRD.01.01.01 | src/[project_module]/gateway/connection_service.py:15 | ✓ Complete |
| BRD.01.01.02 | src/[project_module]/gateway/connection_service.py:15 | ✓ Complete |
| BRD.01.01.30 | src/[project_module]/services/account_service.py:12 | ⚠️ In Progress |
```

**Reverse Matrix (Code → BRD)**:
```markdown
| Source File | BRD Requirements | Implementation Status |
|-------------|------------------|---------------------|
| src/[project_module]/gateway/connection_service.py | BRD.01.01.01, BRD.01.01.02, BRD.01.01.03 | Complete |
| src/[project_module]/services/account_service.py | BRD.01.01.30, BRD.01.01.31, BRD.01.01.32 | In Progress |
```

**Traditional Section 7 Validation** (Optional):
- For each A→B link in document A, verify B→A exists in document B
- Check upstream/downstream symmetry
- Detect missing reverse references
- Calculate consistency score: (matched pairs / total links) × 100%

**Scoring**:
- Target: ≥95% consistency
- Warning: 90-94% consistency
- Failure: <90% consistency

**Note:** Matrices are auto-generated from tags. Manual Section 7 is optional when using tag-based approach.

### Step 6: Calculate Coverage Metrics

**Metrics**:
- Count artifacts with complete traceability sections
- Calculate: (artifacts with Section 7 / total artifacts) × 100%
- Identify orphaned artifacts (no upstream/downstream links)
- Report coverage by artifact type

**Coverage Requirements**:
- Section 7 exists
- At least one upstream source listed (except BRD)
- Downstream artifacts identified or "To Be Created" noted

**Orphan Detection**:
- Root artifacts: BRD can have no upstream (business-driven)
- Leaf artifacts: IMPL can have no downstream (code is endpoint)
- Warning: REQ with no upstream (should link to BRD/PRD/EARS)
- Warning: SPEC with no downstream (should generate IMPL)

### Step 7: Generate Validation Report

**Report Sections**:

1. **Summary**: Pass/fail, coverage %, consistency score
2. **Broken Links**: File:line references with error details
3. **Missing Traceability**: Artifacts without Section 7
4. **Bidirectional Gaps**: A→B exists but B→A missing
5. **Orphaned Artifacts**: No upstream or downstream links
6. **Suggested Fixes**: Auto-fix commands or manual steps
7. **Coverage by Type**: Table with metrics per artifact type

**Report Format**:
- Markdown: Human-readable with tables and emojis
- JSON: Machine-readable for CI/CD integration
- Text: Plain text for console output

### Step 8: Auto-Fix Broken Links (if auto_fix=true)

**Actions**:
1. Create backup before modifications: `docs_backup_YYYYMMDD_HHMMSS.tar.gz`
2. Update document revision history (version bump, changelog)
3. Add missing downstream references to upstream documents
4. Fix relative path errors (../../ corrections)
5. Suggest new traceability entries based on filename patterns

**Safety Measures**:
- Backup creation mandatory before any changes
- Dry-run mode available for preview
- Rollback command provided in report
- Modification log generated

**Backup Command**:
```bash
cd {project_root}/docs
tar -czf ../backups/docs_backup_$(date +%Y%m%d_%H%M%S).tar.gz .
```

## Validation Checks

### ID Format Check

**Compliance**:
- Format: `TYPE-XXX` or `TYPE-XXX-YY`
- H1 header: Contains full document ID
- Zero-padding: 3 digits minimum (001, not 1)
- No collisions: Each XXX unique per type

**Regex Pattern**: `^(BRD|PRD|EARS|BDD|ADR|SYS|REQ|IMPL|CTR|SPEC|TASKS)-\d{3}(-\d{2})?$`

**Failure Examples**:
- `BRD-9` → Should be `BRD-009`
- `SPEC-1` → Should be `SPEC-01`
- `REQ-042-1` → Should be `REQ-042-01`

### Link Resolution Check

**Tests**:
- File exists: Path resolves to valid file
- Extension correct: .md, .yaml, .feature as expected
- Relative path: Correct from source file location
- Anchor exists: `#anchor` found in target file

**Failure Examples**:
- `[SPEC-01](../SPEC/SPEC-01.yaml)` → File not found
- `[BRD-01](../../BRD/BRD-01.md#BRD-01)` → Wrong path depth
- `[REQ-015](../REQ/REQ-015.md#REQ-015)` → File exists but anchor missing

### Anchor Validation Check

**Anchor Creation Rules**:
- Markdown: `# {ID}` → anchor `#{ID}`
- YAML: `id: {snake_case_name}` → anchor `#{snake_case_name}`
- Feature: `Scenario: {title}` → anchor varies by parser

**Validation**:
- Extract anchor from link: `[ID](path#anchor)`
- Parse target file for anchor existence
- Verify anchor format matches file type

**Failure Examples**:
- Link: `[SPEC-01](../SPEC/SPEC-01.yaml#SPEC-01)` → YAML has `id:` field, not H1
- Link: `[BDD-01](../BDD/BDD-01.feature#ib-gateway-connection)` → Scenario title mismatch

### Bidirectional Consistency Check

**Logic**:
- Forward exists: A→B link in document A Section 7.2
- Reverse exists: B→A link in document B Section 7.1
- Symmetry: Both directions present

**Scoring**: (matched pairs / total links) × 100%

**Failure Examples**:
- SPEC-01→BRD-01 exists, but BRD-01→SPEC-01 missing (50% consistency for this pair)
- BRD-01→PRD-01 exists, PRD-01→BRD-01 exists (100% consistency)

### Coverage Check

**Requirements**:
- Section 7 "Traceability" present
- At least one upstream source listed (except BRD - BRD is the only artifact type with OPTIONAL upstream)
- Downstream artifacts: OPTIONAL - only link to documents that already exist (no placeholders)

**Calculation**: (complete / total) × 100%

**Failure Examples**:
- SPEC-01 created but no upstream BRD reference (incomplete)
- REQ-042 with no downstream SPEC reference and no "To Be Created" note (incomplete)

### Orphan Detection Check

**Definitions**:
- No upstream: Artifact has no source documents
- No downstream: Artifact generates no other artifacts

**Traceability Rules**:
| Document Type | Upstream Traceability | Downstream Traceability |
|---------------|----------------------|------------------------|
| **BRD** | OPTIONAL (to other BRDs) | OPTIONAL |
| **All Other Documents** | REQUIRED | OPTIONAL |

**Key Rules**:
- **Upstream REQUIRED** (except BRD): Document MUST reference its upstream sources
- **Downstream OPTIONAL**: Only link to documents that already exist
- **No-TBD Rule**: NEVER use placeholder IDs (TBD, XXX, NNN) - leave empty or omit section

**Expected Behavior**:
- Root artifact: BRD can have no upstream (top-level business document)
- All other artifacts: MUST have upstream references
- Leaf artifacts: IMPL/Code can have no downstream (endpoint of chain)
- Downstream: OPTIONAL for all artifacts - only add when downstream docs exist

**Failure Examples**:
- REQ-05 with no BRD/PRD/EARS upstream (ERROR - upstream REQUIRED)
- PRD-02 with no BRD upstream (ERROR - upstream REQUIRED)
- SPEC-003 with no downstream IMPL (OK - downstream is OPTIONAL)
- Any document using "TBD", "XXX", or "NNN" placeholders (ERROR - No-TBD rule)

## Example Usage Scenarios

### Scenario 1: Quick Validation Before Commit

**User Request**: "Validate traceability before I commit SPEC-01"

**Assistant Action**: Uses trace-check skill with:
- project_root_path: `{project_root}/docs/`
- artifact_types: `["SPEC"]`
- strictness_level: `"strict"`
- auto_fix: `false`

**Output**:
```
✅ SPEC-01: ID format valid
✅ SPEC-01: Links resolve (BRD-01, SYS-002, REQ-01, ADR-02)
❌ SPEC-01: Bidirectional gap - BRD-01 missing reverse link
Coverage: SPEC artifacts 100% (1/1)
Consistency: 75% (3/4 links bidirectional)

Recommendation: Update BRD-01 Section 7.2 to add SPEC-01 reference
```

### Scenario 2: Full Audit with Auto-Fix

**User Request**: "Run full traceability audit and fix issues"

**Assistant Action**: Uses trace-check skill with:
- project_root_path: `{project_root}/docs/`
- artifact_types: `["all"]`
- strictness_level: `"strict"`
- auto_fix: `true`

**Actions**:
1. Scanned 87 artifacts (13 BRD, 15 PRD, 8 SPEC, 51 REQ)
2. Found 12 broken links - fixed 10, flagged 2 for manual review
3. Added 5 missing downstream references
4. Updated 5 document revision histories
5. Generated backup: `docs_backup_20251111_174001.tar.gz`

**Output**:
```
✅ Coverage: 98% (85/87 artifacts)
✅ Consistency: 96% (245/255 links)
⚠️ 2 orphaned artifacts: REQ-042, REQ-055 (no upstream)
📋 Auto-fixed: 15 issues
📝 Manual review: 2 issues (see report)
```

### Scenario 3: Specific Artifact Type Validation

**User Request**: "Check all SPEC files for traceability issues"

**Assistant Action**: Uses trace-check skill with:
- project_root_path: `{project_root}/docs/`
- artifact_types: `["SPEC"]`
- strictness_level: `"pedantic"`

**Output**:
```
Validated: 8 SPEC files
✅ SPEC-01: Perfect (100% traceability)
✅ SPEC-02: Perfect (100% traceability)
⚠️ SPEC-003: Missing BDD reference
❌ SPEC-004: Broken link to REQ-015 (file not found)
Coverage: 88% (7/8 SPEC with complete traceability)
```

### Scenario 4: Coverage Report Generation

**User Request**: "Generate traceability coverage report"

**Assistant Action**: Uses trace-check skill with:
- project_root_path: `{project_root}/docs/`
- report_format: `"markdown"`

**Output**:
```markdown
| Artifact Type | Total | Complete | Coverage | Orphaned |
|---------------|-------|----------|----------|----------|
| BRD           | 13    | 13       | 100%     | 0        |
| PRD           | 15    | 15       | 100%     | 0        |
| EARS          | 8     | 8        | 100%     | 0        |
| BDD           | 51    | 51       | 100%     | 0        |
| SPEC          | 8     | 7        | 88%      | 0        |
| REQ           | 42    | 40       | 95%      | 2        |
| **Total**     | **137** | **134** | **98%** | **2**  |
```

### Scenario 5: Cumulative Tagging Validation (NEW)

**User Request**: "Validate cumulative tagging compliance across all artifacts"

**Assistant Action**: Uses trace-check skill with:
- project_root_path: `{project_root}/docs/`
- artifact_types: `["all"]`
- strictness_level: `"strict"`
- validate_cumulative: `true`

**Actions**:
1. Scanned 87 artifacts across 15 artifact types organized in 11 functional layers
2. Validated tag count for each artifact against expected range for its artifact type
3. Checked for gaps in cumulative tag chains
4. Verified optional artifacts (IMPL, CTR) handled correctly

**Output**:
```
✅ Artifact Type Validation: 85/87 artifacts compliant (98%)
✅ Tag Chain Completeness: 100% (no gaps detected)
⚠️ Tag Count Issues: 2 artifacts
  - SPEC-004: Has 6 tags but artifact type requires 7-9 (missing @impl or @ctr)
  - Code file position_service.py: Has 8 tags but artifact type requires 9-11 (missing upstream tags)
❌ Cumulative Chain Gaps: 0 artifacts

Recommendations:
1. SPEC-004: Add missing @impl or @ctr tag (depending on project structure)
2. position_service.py: Add missing @tasks or @task_plans tag to docstring
3. Run validation weekly to catch gaps early
```

**Benefits**:
- Ensures regulatory compliance (complete audit trails)
- Prevents gaps in upstream traceability
- Automated enforcement of cumulative tagging standard

## Output Report Format

### Summary Section

```markdown
## Traceability Validation Report

**Project**: IB API MCP Server
**Validation Date**: 2025-11-11 17:40:01 EST
**Scope**: All artifacts (137 documents)

### Summary
- ✅ Overall Status: PASS (with warnings)
- 📊 Coverage: 98% (134/137 complete)
- 🔗 Consistency: 96% (245/255 bidirectional)
- ⚠️ Warnings: 3 issues require attention
- ❌ Errors: 0 blocking issues
```

### Broken Links Section

```markdown
## Broken Links (2 found)

| Source | Line | Target | Error |
|--------|------|--------|-------|
| SPEC-004 | 56 | REQ-015 | File not found: ../REQ/REQ-015.md |
| BDD-012 | 134 | SPEC-003 | Anchor not found: #ib_service_spec |
```

### Missing Traceability Section

```markdown
## Missing Traceability (3 artifacts)

| Artifact | Issue | Severity | Recommendation |
|----------|-------|----------|----------------|
| REQ-042 | No upstream sources | Warning | Add BRD/PRD reference |
| REQ-055 | No upstream sources | Warning | Add EARS reference |
| SPEC-003 | No BDD reference | Info | Add BDD-XXX when tests created |
```

### Bidirectional Gaps Section

```markdown
## Bidirectional Inconsistencies (10 found)

| Forward Link | Reverse Link | Status | Fix Command |
|--------------|--------------|--------|-------------|
| SPEC-01 → BRD-01 | BRD-01 → SPEC-01 | ✅ Fixed | Added to BRD-01:463 |
| SPEC-02 → REQ-03 | REQ-03 → SPEC-02 | ❌ Missing | Add to REQ-03 Section 7 |
```

### Coverage by Type

```markdown
## Coverage Metrics

| Type | Total | Complete | Coverage | Target | Status |
|------|-------|----------|----------|--------|--------|
| BRD  | 13    | 13       | 100%     | 100%   | ✅     |
| PRD  | 15    | 15       | 100%     | 100%   | ✅     |
| SPEC | 8     | 7        | 88%      | 100%   | ⚠️     |
| REQ  | 42    | 40       | 95%      | 100%   | ⚠️     |
```

## Quality Gates

### Definition of Done

- [ ] 100% link resolution (all markdown links resolve)
- [ ] 100% ID format compliance (TYPE-XXX or TYPE-XXX-YY)
- [ ] 100% CTR dual-file compliance (both .md and .yaml exist with matching slugs)
- [ ] ≥95% bidirectional consistency (forward and reverse links)
- [ ] Zero orphaned root artifacts (BRD must have downstream)
- [ ] Zero orphaned leaf artifacts (REQ must have downstream SPEC)
- [ ] All artifacts have Section 7 "Traceability"
- [ ] All auto-fixes logged in document revision history

### Acceptance Criteria

**Performance**:
- Report generation: <30 seconds for 100 artifacts
- Memory usage: <500MB for 200 artifacts
- Backup creation: <5 seconds for 100MB documentation

**Accuracy**:
- Zero false positives for valid traceability patterns
- Zero false negatives for broken links
- 100% detection of bidirectional gaps

**Safety**:
- Backup created before any auto-fix modifications
- Rollback command provided in report
- Modification log includes file:line details

**Compatibility**:
- Handles all SDD artifact types (BRD through TASKS)
- Supports .md, .yaml, .feature file formats
- Works with relative paths from any project root

## Auto-Fix Capabilities

### 1. Update Document Revision History

**Action**: Increment version and add changelog entry

**Example**:
```markdown
## Revision History

| Version | Date       | Author | Changes |
|---------|------------|--------|---------|
| 2.1     | 2025-11-11 | trace-check skill | Updated traceability: Added SPEC-01 reference |
| 2.0     | 2025-11-10 | User | Initial complete draft |
```

### 2. Add Missing Downstream References

**Detection**: SPEC-01 references BRD-01, but BRD-01 does not reference SPEC-01

**Action**: Add to BRD-01 Section 7.2 "Downstream Artifacts"

**Before**:
```markdown
**To Be Created:**
- SPEC-XXX: Technical implementation specifications
```

**After**:
```markdown
**In Progress:**
- [SPEC-01](../SPEC/SPEC-01_ib_gateway_connection_service.yaml#ib_gateway_connection_service) - IB Gateway Connection Service (Status: Draft, Created: 2025-11-11)

**To Be Created:**
- SPEC-02+: Additional technical specifications (TBD)
```

### 3. Fix Relative Path Errors

**Detection**: Link `[BRD-01](../../BRD/BRD-01.md#BRD-01)` from `/docs/SPEC/SPEC-01.yaml`

**Calculation**:
- From: `/docs/SPEC/SPEC-01.yaml`
- To: `/docs/BRD/BRD-01.md`
- Correct: `../BRD/BRD-01.md`

**Action**: Update link to `[BRD-01](../BRD/BRD-01.md#BRD-01)`

### 4. Suggest New Traceability Entries

**Pattern Analysis**:
- SPEC-01 likely relates to REQ-01, BDD-01
- REQ-042 likely relates to SPEC-004
- BDD-003 likely relates to SPEC-003

**Suggestion Format**:
```markdown
## Suggested Traceability Entries

**SPEC-003** (Missing BDD reference):
- Add to Section 7.2: `[BDD-003](../BDD/BDD-003_file.feature#scenario-id) - Test scenarios (To Be Created)`

**REQ-042** (No upstream):
- Add to Section 7.1: `[BRD-004](../BRD/BRD-004_file.md#BRD-004) - Source requirement (Verify)`
```

### 5. Backup Before Modifications

**Command**:
```bash
cd {project_root}/docs
tar -czf ../backups/docs_backup_$(date +%Y%m%d_%H%M%S).tar.gz .
```

**Verification**:
```bash
ls -lh ../backups/docs_backup_20251111_174001.tar.gz
# Output: 15M Nov 11 17:40 docs_backup_20251111_174001.tar.gz
```

**Rollback Command** (provided in report):
```bash
cd {project_root}/docs
tar -xzf ../backups/docs_backup_20251111_174001.tar.gz
```

## Related Documentation

### SDD Workflow Standards

**Primary References**:
- [SPEC_DRIVEN_DEVELOPMENT_GUIDE.md]({project_root}/ai_dev_flow/SPEC_DRIVEN_DEVELOPMENT_GUIDE.md) - Authoritative workflow definition
- [ID_NAMING_STANDARDS.md]({project_root}/ai_dev_flow/ID_NAMING_STANDARDS.md) - ID format rules and conventions
- [TRACEABILITY.md v2.0]({project_root}/ai_dev_flow/TRACEABILITY.md) - Traceability requirements and cumulative tagging standards (updated 2025-10-31)
- [TRACEABILITY_SETUP.md]({project_root}/ai_dev_flow/TRACEABILITY_SETUP.md) - Setup guide for automated validation and CI/CD integration
- [COMPLETE_TAGGING_EXAMPLE.md]({project_root}/ai_dev_flow/COMPLETE_TAGGING_EXAMPLE.md) - End-to-end cumulative tagging example

**Workflow Sequence** (v2.0): BRD → PRD → EARS → BDD → ADR → SYS → REQ → IMPL → CTR (optional) → SPEC → TASKS → Code → Tests → Validation

### Related Skills

**Complementary Skills**:
- [doc-flow]({project_root}/.claude/skills/doc-flow/SKILL.md) - Create SDD artifacts from templates
- [project-mngt]({project_root}/.claude/skills/project-mngt/SKILL.md) - MVP/MMP/MMR project planning
- [adr-roadmap]({project_root}/.claude/skills/adr-roadmap/SKILL.md) - Generate implementation roadmaps from ADRs

**Workflow Integration**:
1. Use `doc-flow` to create new artifacts
2. Use `trace-check` to validate traceability
3. Use `adr-roadmap` to generate implementation plans
4. Use `project-mngt` for release planning

### Artifact Templates

**Template Locations**:
- BRD: `{project_root}/ai_dev_flow/BRD/`
- PRD: `{project_root}/ai_dev_flow/PRD/`
- EARS: `{project_root}/ai_dev_flow/EARS/`
- BDD: `{project_root}/ai_dev_flow/BDD/`
- ADR: `{project_root}/ai_dev_flow/ADR/`
- SYS: `{project_root}/ai_dev_flow/SYS/`
- REQ: `{project_root}/ai_dev_flow/REQ/`
- SPEC: `{project_root}/ai_dev_flow/SPEC/`

**All templates include**:
- Section 7: Traceability with upstream/downstream structure
- Revision history table
- Document metadata header

### Validation Scripts

**Available Validators**:
- [add_cumulative_tagging_to_matrices.py]({project_root}/ai_dev_flow/scripts/add_cumulative_tagging_to_matrices.py) - Adds cumulative tagging sections to traceability matrices
- [batch_update_matrix_templates.py]({project_root}/ai_dev_flow/scripts/batch_update_matrix_templates.py) - Batch updates matrix templates with new features
- [validate_traceability_matrix_enforcement.py]({project_root}/ai_dev_flow/scripts/validate_traceability_matrix_enforcement.py) - Enforces traceability matrix presence and completeness

**Framework Guides**:
- [MATRIX_TEMPLATE_COMPLETION_GUIDE.md]({project_root}/ai_dev_flow/MATRIX_TEMPLATE_COMPLETION_GUIDE.md) - Guide for completing matrix templates with cumulative tagging

## Version Information

**Version**: 2.1.0
**Last Updated**: 2025-12-13
**Created**: 2025-11-11
**Status**: Active
**Author**: SDD Framework Team

**Change Log**:
- 2.1.1 (2025-12-15): Architecture Decision Topic format update
  - **FORMAT CHANGE**: Updated ADT format from `BRD.NNN.NN` to `{DOC_TYPE}.NN.EE.SS`
    - 3-digit topic number (001-999) for consistency with other IDs
    - Generic doc type support (not BRD-specific)
- 2.1.0 (2025-12-13): Architecture decision layer separation validation
  - **NEW FEATURE**: Added Step 3.6 - Architecture Decision Topic validation
    - Validates `{DOC_TYPE}.NN.EE.SS` subsection ID format (3-digit topic number)
    - Cross-reference validation: BRD Section 7.2 → PRD Section 18 → ADR Section 4.1
    - Content validation: Business-only in BRD, technical in PRD
    - Layer separation principle enforcement
  - **VALIDATION RULES**: Added content validation rules table
  - **REGEX PATTERNS**: Added validation patterns for topic extraction
- 2.0.1 (2025-11-13): Clarity improvements and CTR validation enhancement
  - **NEW FEATURE**: Added Step 3.5 - CTR dual-file format validation (MANDATORY)
    - Validates both .md and .yaml files exist for each CTR
    - Verifies slug matching between filenames
    - Validates YAML schema structure (OpenAPI/AsyncAPI/JSON Schema)
    - Provides detailed error reporting for compliance issues
  - **QUALITY GATE**: Added CTR dual-file compliance to Definition of Done checklist
  - **CLARIFICATION**: Changed "12 layers" to "11 functional layers, 15+ artifact types" for accuracy
  - **CLARIFICATION**: Renamed tag count table from "Layer" to "Artifact Type" to avoid confusion
  - **CLARIFICATION**: Added note explaining that numbers indicate artifact sequence, not layer numbers
  - **CONSISTENCY**: Updated all references from "layer validation" to "artifact type validation"
- 2.0.0 (2025-11-13): Major update for SDD Framework v2.0
  - Added cumulative tagging hierarchy validation (Step 2.6)
  - Added artifact-type-specific tag count validation
  - Updated artifact types: Added IMPL; clarified CTR as optional
  - Updated workflow to 11-layer structure (aligned with TRACEABILITY.md v2.0)
  - Added new validation parameter: validate_cumulative
  - Added expected tag counts by artifact type (Artifact 0-15)
  - Added cumulative tagging validation scenario (Scenario 5)
  - Updated validation scripts with --validate-cumulative flag
  - Enhanced error detection for cumulative tag chains
  - Added regulatory compliance benefits documentation
- 1.0.0 (2025-11-11): Initial release with full validation and auto-fix capabilities
