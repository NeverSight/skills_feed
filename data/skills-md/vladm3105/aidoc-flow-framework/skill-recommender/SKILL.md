---
title: "skill-recommender: Intelligent skill suggestion engine for documentation tasks"
name: skill-recommender
description: Intelligent skill suggestion engine that analyzes user intent and project context to recommend appropriate documentation skills
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

# skill-recommender

## Purpose

Analyze user requests and recommend appropriate documentation skills from the AI Dev Flow framework catalog.

**Problem Solved**: Users must know which of 25+ skills to invoke for their documentation task, requiring deep framework knowledge.

**Solution**: Parse user intent, match against skill catalog, and provide ranked recommendations with confidence scores and rationale.

## When to Use This Skill

**Use skill-recommender when**:
- User is unsure which skill to use for a documentation task
- Starting a new documentation workflow and need guidance
- Want to discover available skills for a specific intent
- Need help navigating the skill catalog

**Do NOT use when**:
- User explicitly requests a specific skill (e.g., "/skill doc-prd")
- Performing non-documentation tasks
- User is experienced and knows the target skill

## Skill Inputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| user_request | string | Yes | Natural language description of what user wants to do |
| project_context | object | No | Project structure and existing artifacts (from context-analyzer) |
| max_recommendations | number | No | Maximum recommendations to return (default: 3) |

## Skill Workflow

### Step 1: Parse User Intent

Extract action verbs and targets from the user request:

**Intent Categories**:
| Category | Signal Keywords | Example Request |
|----------|-----------------|-----------------|
| `create` | create, write, draft, new, add | "Create a new PRD for user authentication" |
| `update` | update, modify, edit, change, revise | "Update the traceability section of SPEC-01" |
| `validate` | validate, check, verify, audit, review | "Check if my artifacts have proper traceability" |
| `analyze` | analyze, review, examine, inspect | "Analyze the project documentation structure" |
| `plan` | plan, roadmap, schedule, organize | "Create an implementation roadmap from ADRs" |

**Target Extraction**:
| Target | Signal Keywords | Maps To |
|--------|-----------------|---------|
| business requirements | business, brd, objectives | doc-brd |
| product requirements | product, prd, features, user stories | doc-prd |
| formal requirements | ears, formal, when-the-shall | doc-ears |
| test scenarios | bdd, tests, scenarios, gherkin | doc-bdd |
| architecture decisions | adr, architecture, decision | doc-adr |
| system requirements | sys, system, technical | doc-sys |
| requirements | req, requirement, atomic | doc-req |
| implementation plan | impl, implementation, plan | doc-impl |
| contracts | ctr, contract, api, interface | doc-ctr |
| specifications | spec, specification, yaml | doc-spec |
| tasks | tasks, todo, implementation tasks | doc-tasks |
| traceability | trace, traceability, links | trace-check |
| validation | validate, quality, compliance | doc-validator |
| diagrams | diagram, mermaid, chart, flow | charts-flow, mermaid-gen |
| roadmap | roadmap, adr implementation | adr-roadmap |
| project management | mvp, mmp, release, planning | project-mngt |

### Step 2: Match Skills

Match parsed intent against skill catalog:

**Skill Catalog** (Core Documentation Skills):

| Skill ID | Category | Layer | Description |
|----------|----------|-------|-------------|
| doc-brd | core-workflow | 1 | Business Requirements Documents |
| doc-prd | core-workflow | 2 | Product Requirements Documents |
| doc-ears | core-workflow | 3 | EARS Formal Requirements |
| doc-bdd | core-workflow | 4 | BDD Test Scenarios |
| doc-adr | core-workflow | 5 | Architecture Decision Records |
| doc-sys | core-workflow | 6 | System Requirements |
| doc-req | core-workflow | 7 | Atomic Requirements |
| doc-impl | core-workflow | 8 | Implementation Plans (optional) |
| doc-ctr | core-workflow | 9 | API Contracts (optional) |
| doc-spec | core-workflow | 10 | Technical Specifications |
| doc-tasks | core-workflow | 11 | Implementation Tasks |

**Quality Assurance Skills**:

| Skill ID | Category | Description |
|----------|----------|-------------|
| trace-check | quality-assurance | Validate bidirectional traceability |
| doc-validator | quality-assurance | Validate documentation standards |
| code-review | quality-assurance | Code quality review |
| contract-tester | quality-assurance | Test API contracts |

**Utility Skills**:

| Skill ID | Category | Description |
|----------|----------|-------------|
| charts-flow | utility | Mermaid architecture diagrams |
| mermaid-gen | utility | Generate Mermaid diagrams |
| analytics-flow | utility | Analytics and data analysis |
| project-init | utility | Initialize project structure |

**Planning Skills**:

| Skill ID | Category | Description |
|----------|----------|-------------|
| adr-roadmap | planning | ADR implementation roadmaps |
| project-mngt | planning | MVP/MMP/MMR release planning |
| doc-flow | planning | SDD workflow orchestration |

### Step 3: Score and Rank

Calculate confidence scores based on:

| Factor | Weight | Description |
|--------|--------|-------------|
| Intent match | 40% | How well request matches skill intent signals |
| Target match | 30% | Explicit skill/artifact type mentioned |
| Context fit | 20% | Project state and workflow position |
| Usage patterns | 10% | Common skill sequences |

**Confidence Levels**:
- **High** (≥80%): Strong match, recommend with confidence
- **Medium** (50-79%): Good match, include alternative options
- **Low** (<50%): Weak match, suggest clarification

### Step 4: Generate Recommendations

Format recommendations with rationale:

**Output Format**:
```yaml
recommendations:
  - skill: doc-prd
    confidence: 92%
    rationale: "Request mentions 'product requirements' and 'features' - direct match for PRD creation"
    next_steps: "Run /skill doc-prd to create Product Requirements Document"

  - skill: doc-brd
    confidence: 65%
    rationale: "May need BRD first if business requirements not yet documented"
    condition: "Use if no BRD exists for this feature"

  - skill: doc-ears
    confidence: 45%
    rationale: "EARS follows PRD in workflow - consider after PRD completion"
    condition: "Use after PRD is complete"

clarification_needed: false
clarification_question: null
```

## Example Usage

### Example 1: Clear Intent

**User Request**: "I need to create a product requirements document for a new authentication feature"

**Skill Analysis**:
```
Intent: create (keywords: create, need)
Target: product requirements (keywords: product requirements document)
Domain: authentication feature
```

**Recommendations**:
```yaml
recommendations:
  - skill: doc-prd
    confidence: 95%
    rationale: "Explicit request for Product Requirements Document"
    next_steps: "Run /skill doc-prd to create PRD for authentication feature"

  - skill: doc-brd
    confidence: 40%
    rationale: "BRD may be needed upstream if not already created"
    condition: "Check if BRD exists for authentication feature"
```

### Example 2: Ambiguous Intent

**User Request**: "Help me document the system architecture"

**Skill Analysis**:
```
Intent: create (keywords: document)
Target: ambiguous - could be ADR, SYS, or diagrams
```

**Recommendations**:
```yaml
recommendations:
  - skill: doc-adr
    confidence: 60%
    rationale: "Architecture decisions typically documented in ADRs"

  - skill: doc-sys
    confidence: 55%
    rationale: "System requirements capture technical architecture"

  - skill: charts-flow
    confidence: 50%
    rationale: "Architecture diagrams visualize system structure"

clarification_needed: true
clarification_question: "What aspect of architecture? (1) Decisions/rationale (ADR), (2) System specs (SYS), (3) Visual diagrams?"
```

### Example 3: Validation Request

**User Request**: "Check if my documentation has proper links between artifacts"

**Skill Analysis**:
```
Intent: validate (keywords: check)
Target: traceability (keywords: links between artifacts)
```

**Recommendations**:
```yaml
recommendations:
  - skill: trace-check
    confidence: 98%
    rationale: "Direct request for traceability validation"
    next_steps: "Run /skill trace-check to validate bidirectional links"
```

## Integration with Other Skills

| Integration | Description |
|-------------|-------------|
| context-analyzer | Receives project context for better recommendations |
| doc-flow | Can be invoked by doc-flow for skill discovery |
| workflow-optimizer | Shares workflow position awareness |

## Quality Gates

### Definition of Done

- [ ] User request parsed successfully
- [ ] At least one skill recommendation provided
- [ ] Confidence scores calculated for all recommendations
- [ ] Rationale included for each recommendation
- [ ] Clarification question generated when ambiguous

### Performance Targets

| Metric | Target |
|--------|--------|
| Response latency | <500ms |
| Recommendation accuracy | ≥85% |
| User acceptance rate | ≥70% |

## Traceability

**Required Tags**:
```
@prd: PRD.000.001
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
| Selected doc-* skill | Skill Execution | Invoked based on recommendation |

---

## Version Information

**Version**: 1.0.0
**Created**: 2025-11-29
**Status**: Active
**Author**: AI Dev Flow Framework Team
