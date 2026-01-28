---
title: "context-analyzer: Project context analysis engine for documentation creation"
name: context-analyzer
description: Project context analysis engine that scans project structure and surfaces relevant information for documentation creation
tags:
  - sdd-workflow
  - ai-assistant
  - utility
  - shared-architecture
custom_fields:
  layer: null
  artifact_type: null
  architecture_approaches: [ai-agent-based]
  priority: primary
  development_status: active
  skill_category: utility
  upstream_artifacts: [PRD-00, ADR-000]
  downstream_artifacts: []
---

# context-analyzer

## Purpose

Scan project structure and build a context model for intelligent documentation creation.

**Problem Solved**: AI assistants lack awareness of project context, existing artifacts, and current workflow state when creating documentation, leading to missing references and duplicate content.

**Solution**: Analyze project directories, parse artifact metadata and traceability sections, and build a context model that surfaces relevant information for new document creation.

## When to Use This Skill

**Use context-analyzer when**:
- Starting documentation work in an existing project
- Creating a new artifact that needs upstream references
- Need to understand what documentation already exists
- Want to identify gaps in documentation coverage
- Preparing context for doc-* skill invocation

**Do NOT use when**:
- Project has no existing documentation
- Working on a single, isolated document
- Full project audit needed (use trace-check instead)

## Skill Inputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| project_root | string | Yes | Root path of the project to analyze |
| target_artifact_type | string | No | Artifact type being created (e.g., "PRD", "SPEC") |
| depth | string | No | Analysis depth: "quick" (structure only), "standard" (default), "deep" (full content) |

## Skill Workflow

### Step 1: Scan Project Structure

Enumerate all documentation artifacts by type and location:

**Directory Patterns**:
```
{project_root}/
├── docs/
│   ├── BRD/
│   ├── PRD/
│   ├── EARS/
│   ├── BDD/
│   ├── ADR/
│   ├── SYS/
│   ├── REQ/
│   ├── IMPL/
│   ├── CTR/
│   ├── SPEC/
│   └── TASKS/
└── ai_dev_flow/  (framework templates)
```

**Artifact Discovery**:
```bash
# Example discovery pattern
find {project_root}/docs -name "*.md" -o -name "*.yaml" -o -name "*.feature"
```

**Output Structure**:
```yaml
artifact_inventory:
  BRD:
    count: 3
    files:
      - id: BRD-01
        path: docs/BRD/BRD-01_platform_foundation.md
        title: Platform Foundation
        status: Approved
      - id: BRD-02
        path: docs/BRD/BRD-02_partner_integration.md
        title: Partner Integration
        status: Draft
  PRD:
    count: 2
    files:
      - id: PRD-01
        path: docs/PRD/PRD-01_core_features.md
        title: Core Features
        status: In Review
  SPEC:
    count: 0
    files: []
```

### Step 2: Parse Artifact Metadata

Extract metadata and key information from discovered artifacts:

**YAML Frontmatter Extraction**:
```yaml
# From document header
---
title: "BRD-01: Platform Foundation"
tags:
  - platform-brd
  - shared-architecture
custom_fields:
  layer: 1
  artifact_type: BRD
  status: Approved
---
```

**Document Control Extraction**:
```markdown
## Document Control

| Item | Details |
|------|---------|
| **Status** | Approved |
| **Version** | 2.1.0 |
| **Last Updated** | 2025-11-15 |
```

**Parsed Metadata Model**:
```yaml
artifact_metadata:
  BRD-01:
    title: Platform Foundation
    layer: 1
    status: Approved
    version: 2.1.0
    last_updated: 2025-11-15
    tags: [platform-brd, shared-architecture]
```

### Step 3: Extract Traceability Information

Parse Section 7 Traceability from each artifact:

**Upstream Sources Extraction**:
```markdown
### Upstream Sources
| Source | Type | Reference |
|--------|------|-----------|
| [BRD-01](../BRD/BRD-01_platform.md#BRD-01) | Business Requirements | Platform foundation |
```

**Downstream Artifacts Extraction**:
```markdown
### Downstream Artifacts
| Artifact | Type | Reference |
|----------|------|-----------|
| [SPEC-01](../SPEC/SPEC-01_api.yaml) | Technical Specification | API implementation |
```

**Traceability Graph**:
```yaml
traceability_graph:
  BRD-01:
    upstream: []
    downstream: [PRD-01, PRD-00]
  PRD-01:
    upstream: [BRD-01]
    downstream: [EARS-01, SPEC-01]
  SPEC-01:
    upstream: [PRD-01, REQ-01]
    downstream: [TASKS-01]
```

### Step 4: Determine Workflow Position

Calculate current position in SDD workflow:

**Layer Mapping**:
| Layer | Artifact Type | Required Upstream |
|-------|---------------|-------------------|
| 1 | BRD | None |
| 2 | PRD | BRD |
| 3 | EARS | PRD |
| 4 | BDD | EARS |
| 5 | ADR | BDD |
| 6 | SYS | ADR |
| 7 | REQ | SYS |
| 8 | IMPL | REQ (optional) |
| 9 | CTR | IMPL or REQ (optional) |
| 10 | SPEC | REQ, optional IMPL/CTR |
| 11 | TASKS | SPEC |

**Position Analysis**:
```yaml
workflow_position:
  completed_layers: [1, 2, 3]
  current_layer: 4
  next_required: [BDD, ADR]
  gaps:
    - layer: 3
      type: EARS
      status: incomplete
      reason: "Only 2 of 5 PRD features have EARS coverage"
```

### Step 5: Identify Upstream Candidates

For a target artifact type, identify relevant upstream documents:

**Relevance Scoring**:
| Factor | Weight | Description |
|--------|--------|-------------|
| Direct upstream | 50% | Immediate predecessor in workflow |
| Topic match | 30% | Key terms and domain alignment |
| Recency | 10% | Recently updated documents |
| Status | 10% | Approved documents preferred |

**Upstream Candidates Output**:
```yaml
upstream_candidates:
  target_type: SPEC
  candidates:
    - id: REQ-01
      relevance: 95%
      title: API Requirements
      reason: "Direct upstream, topic match: API, approved status"
    - id: REQ-02
      relevance: 80%
      title: Data Model Requirements
      reason: "Direct upstream, related topic: data"
    - id: ADR-005
      relevance: 70%
      title: API Architecture Decision
      reason: "Architecture context for API design"
```

### Step 6: Extract Key Terms

Build project vocabulary from existing documentation:

**Term Extraction Methods**:
- Document titles and headers
- Glossary sections
- Frequently used technical terms
- Domain-specific vocabulary

**Key Terms Output**:
```yaml
key_terms:
  domain_terms:
    - term: workflow
      frequency: 45
      documents: [BRD-01, PRD-01, REQ-01]
    - term: resource
      frequency: 32
      documents: [BRD-01, REQ-02, SPEC-01]
  technical_terms:
    - term: WebSocket
      frequency: 18
      documents: [ADR-003, SPEC-01]
    - term: PostgreSQL
      frequency: 12
      documents: [BRD-01, ADR-000]
```

### Step 7: Build Context Model

Assemble complete context model for session use:

**Complete Context Model**:
```yaml
context_model:
  project_root: /path/to/project
  scan_timestamp: 2025-11-29T14:30:00Z
  scan_depth: standard

  artifact_inventory:
    total_count: 25
    by_type:
      BRD: 3
      PRD: 5
      EARS: 4
      BDD: 6
      ADR: 3
      REQ: 4
      SPEC: 0
      TASKS: 0

  workflow_position:
    completed_layers: [1, 2, 3, 4, 5, 7]
    current_layer: 7
    ready_for: [SPEC, TASKS]
    gaps:
      - type: SYS
        status: missing
        impact: "SPEC creation may lack system context"

  upstream_candidates:
    target_type: SPEC
    primary:
      - id: REQ-01
        title: Core API Requirements
        relevance: 95%
    secondary:
      - id: ADR-003
        title: WebSocket Architecture
        relevance: 75%

  key_terms:
    domain: [workflow, resource, validation, processing]
    technical: [WebSocket, PostgreSQL, Redis, REST API]

  coverage_gaps:
    - area: Testing
      description: "BDD scenarios cover only 60% of EARS requirements"
    - area: Implementation
      description: "No SPEC or TASKS documents created yet"
```

## Example Usage

### Example 1: Pre-SPEC Context

**User Request**: "I'm about to create a SPEC document, what context do I have?"

**Context Analysis**:
```yaml
context_summary:
  target: SPEC creation
  readiness: ready
  upstream_available:
    - REQ-01: Core API Requirements (Approved)
    - REQ-02: Data Model Requirements (Approved)
    - ADR-003: WebSocket Architecture (Approved)
  recommended_references:
    - "Reference REQ-01 for API endpoint specifications"
    - "Include ADR-003 for WebSocket implementation decisions"
  warnings:
    - "No CTR (contract) documents exist - consider if API contracts needed"
```

### Example 2: Gap Analysis

**User Request**: "What documentation is missing in this project?"

**Gap Analysis Output**:
```yaml
documentation_gaps:
  critical:
    - type: SYS
      reason: "No system requirements linking ADR to REQ"
      impact: "REQ documents may lack architectural context"
    - type: SPEC
      reason: "No technical specifications for implementation"
      impact: "Cannot proceed to code generation"
  moderate:
    - type: BDD
      coverage: 60%
      reason: "4 of 10 EARS requirements have BDD scenarios"
  low:
    - type: IMPL
      reason: "Implementation plan optional but recommended for complex projects"
```

### Example 3: Quick Structure Check

**User Request**: "What docs exist in this project?"

**Quick Scan Output** (depth: quick):
```yaml
project_structure:
  docs_directory: /project/docs
  artifact_counts:
    BRD: 3
    PRD: 5
    EARS: 4
    BDD: 6
    ADR: 3
    SYS: 0
    REQ: 4
    IMPL: 0
    CTR: 0
    SPEC: 0
    TASKS: 0
  total_artifacts: 25
  workflow_coverage: 50% (6 of 12 layers)
```

## Integration with Other Skills

| Integration | Description |
|-------------|-------------|
| skill-recommender | Provides project context for better recommendations |
| doc-* skills | Supplies upstream candidates and key terms |
| quality-advisor | Shares artifact inventory for validation |
| workflow-optimizer | Provides workflow position data |
| trace-check | Overlaps with traceability extraction (uses trace-check for deep validation) |

## Quality Gates

### Definition of Done

- [ ] Project structure scanned successfully
- [ ] All artifact types discovered
- [ ] Metadata extracted from discovered artifacts
- [ ] Traceability graph built
- [ ] Workflow position calculated
- [ ] Upstream candidates identified for target type
- [ ] Context model assembled and returned

### Performance Targets

| Metric | Target |
|--------|--------|
| Quick scan latency | <500ms |
| Standard scan latency | <2s for 100 artifacts |
| Deep scan latency | <5s for 100 artifacts |
| Memory usage | <200MB for 100 artifacts |

## Traceability

**Required Tags**:
```
@prd: PRD.000.002
@adr: ADR-000
```

### Upstream Sources

| Source | Type | Reference |
|--------|------|-----------|
| PRD-00 | Product Requirements | [PRD-00]({project_root}/ai_dev_flow/PRD/PRD-00_ai_assisted_documentation_features.md#PRD-00) |
| ADR-000 | Architecture Decision | [ADR-000]({project_root}/ai_dev_flow/ADR/ADR-00_ai_powered_documentation_assistant_architecture.md#ADR-000) |

### Downstream Artifacts

| Artifact | Type | Reference |
|----------|------|-----------|
| skill-recommender | Skill Consumer | Uses context for better recommendations |
| doc-* skills | Skill Consumer | Uses context for artifact creation |

---

## Version Information

**Version**: 1.0.0
**Created**: 2025-11-29
**Status**: Active
**Author**: AI Dev Flow Framework Team
