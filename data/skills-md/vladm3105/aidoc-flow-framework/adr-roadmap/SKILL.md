---
title: "adr-roadmap: Generate phased implementation roadmaps from Architecture Decision Records"
name: adr-roadmap
description: Generate phased implementation roadmaps from Architecture Decision Records
tags:
  - sdd-workflow
  - shared-architecture
custom_fields:
  layer: null
  artifact_type: null
  architecture_approaches: [ai-agent-based, traditional-8layer]
  priority: shared
  development_status: active
  skill_category: utility
  upstream_artifacts: [ADR]
  downstream_artifacts: [TASKS, Code]
---

# adr-roadmap

## Purpose

Analyze Architecture Decision Records (ADRs) and generate phased implementation roadmaps with timelines, dependencies, resource allocation, and risk assessment for any project type.

**Key Capabilities**:
- Universal ADR analysis across any domain (web, mobile, data, ML, infrastructure, embedded)
- Automatic dependency mapping and critical path identification
- Phase decomposition based on complexity, dependencies, and milestones
- Timeline estimation with effort calculation and risk buffers
- Mermaid diagram generation (dependency graphs, Gantt charts)
- Risk assessment per phase
- Testing strategy definition
- Technical debt tracking

---

## When to Use This Skill

### Use adr-roadmap when:
- Project has ≥5 ADRs requiring coordinated implementation
- Need visibility into architectural dependencies and critical path
- Planning multi-phase rollout of architectural decisions
- Require timeline estimation from ADR complexity assessments
- Stakeholders need executive summary of implementation plan
- Managing technical debt and need phased remediation plan
- Team needs clear milestone definitions and acceptance criteria

### Do NOT use adr-roadmap when:
- Single ADR with straightforward implementation (direct implementation)
- ADRs are informational only with no implementation needed
- Planning from requirements (BRD/PRD) not ADRs → use `project-mngt` skill instead
- Need to generate documentation artifacts (SYS/REQ/SPEC) → use `doc-flow` skill instead
- Only need architecture diagrams → use `charts-flow` skill instead

---

## Skill Inputs

### Required Inputs

| Input | Description | Example |
|-------|-------------|---------|
| **adr_directory** | Absolute path to ADR markdown files | `{project_root}/docs/ADR/` |
| **project_context** | Project type, team size, timeline constraints | "Trading platform, 5 FTE, 6-month timeline" |

### Optional Inputs

| Input | Description | Default |
|-------|-------------|---------|
| **output_file** | Roadmap destination path | `{adr_directory}/ADR-00_IMPLEMENTATION-ROADMAP.md` |
| **max_phase_duration** | Maximum weeks per phase | 8 weeks |
| **prioritize_adr** | Force specific ADR ID first (e.g., "ADR-02") | None |
| **phase_model** | Phasing approach: `poc-mvp-prod`, `iterative`, `waterfall` | `poc-mvp-prod` |
| **team_size** | Number of FTE engineers | 3 |
| **target_phases** | Desired number of phases | Auto-calculate |

---

## Skill Workflow

### Step 1: Analyze ADR Directory

**Actions**:
1. Read all `ADR-*.md` files from specified directory
2. Extract metadata from each ADR:
   - ADR ID and title
   - Status (Proposed, Accepted, Deprecated)
   - Complexity rating (1-5 scale from Implementation Assessment section)
   - Effort estimate (from Implementation Assessment section)
   - Dependencies (from Related Decisions section)
3. Count total ADRs and validate structure
4. Identify ADR index file (`ADR-00_index.md`) if present
5. Identify traceability matrix if present

**Validation**:
- Warn if any ADR missing complexity rating
- Warn if dependency references broken (ADR ID doesn't exist)
- Error if no ADRs found in directory

**Output**: ADR inventory with metadata

---

### Step 2: Build Dependency Graph

**Actions**:
1. Parse "Related Decisions" section from each ADR:
   - Upstream dependencies (must implement first)
   - Downstream impacts (will be affected)
   - Parallel decisions (can implement concurrently)
2. Create adjacency matrix of ADR dependencies
3. Detect circular dependencies (error condition)
4. Calculate critical path (longest dependency chain)
5. Identify independent ADR clusters (can parallelize)

**Dependency Classification**:
- **Hard dependency**: ADR-B requires ADR-A implementation complete
- **Soft dependency**: ADR-B references ADR-A decision but can proceed in parallel
- **No dependency**: ADRs completely independent

**Output**:
- Dependency matrix (table format)
- Mermaid flowchart showing ADR relationships
- Critical path highlighted

---

### Step 3: Calculate Complexity Scores

**Actions**:
1. Aggregate complexity ratings per ADR:
   - Complexity 1-2: Simple (1-2 days effort)
   - Complexity 3: Moderate (3-5 days effort)
   - Complexity 4: Complex (1-2 weeks effort)
   - Complexity 5: Architectural change (3-4 weeks effort)
2. Sum total effort across all ADRs
3. Identify high-risk ADRs (complexity 4-5 with many dependencies)
4. Calculate risk buffer (add 20-30% contingency)

**Effort Estimation Formula**:
```
Total Effort = Σ(ADR Complexity × Base Effort) × Risk Buffer
Base Effort (1=1d, 2=2d, 3=4d, 4=10d, 5=20d)
Risk Buffer = 1.2 (20% contingency)
```

**Output**:
- Total effort estimate in person-days
- High-risk ADR list
- Effort distribution per complexity level

---

### Step 4: Create Phase Structure

**Phasing Algorithm**:

Apply selected phase model:

#### A. POC-MVP-Prod Model (Default)
```
Phase 1: POC (Proof of Concept)
  - Minimal ADRs to validate technical feasibility
  - Target: 2-3 weeks
  - Criteria: Core integration working end-to-end

Phase 2: MVP (Minimum Viable Product)
  - Add multi-user, persistence, basic security
  - Target: 4-6 weeks
  - Criteria: Production-ready for limited users

Phase 3: Production
  - Cloud deployment, full security, monitoring
  - Target: 6-8 weeks
  - Criteria: Enterprise-grade reliability

Phase 4: Scale & Optimize
  - Performance tuning, advanced patterns
  - Target: 4-6 weeks
  - Criteria: Performance targets met

Phase 5: Advanced Features
  - Extended capabilities, continuous improvement
  - Target: Ongoing
  - Criteria: Feature backlog prioritized
```

#### B. Iterative Model
```
Each iteration (2-4 weeks):
  - Select ADR cluster (low dependency)
  - Implement and validate
  - Integrate with existing system
  - Deploy incrementally
```

#### C. Waterfall Model
```
Phase by ADR category:
  - Infrastructure ADRs
  - Core business logic ADRs
  - Integration ADRs
  - Optimization ADRs
```

**Phase Assignment Rules**:
1. **Respect dependencies**: Upstream ADRs in earlier phases
2. **Balance phase size**: Target max_phase_duration (default 8 weeks)
3. **Isolate risk**: High-risk ADRs in separate phase or early POC
4. **Enable parallelization**: Independent ADRs can be in same phase
5. **Milestone alignment**: Phases end at natural milestones (POC, MVP, Beta, GA)

**Output**:
- Phase definitions (1-N phases)
- ADR assignments per phase
- Phase duration estimates
- Parallel implementation opportunities identified

---

### Step 5: Generate Timeline

**Actions**:
1. Calculate phase durations from ADR effort estimates:
   ```
   Phase Duration = (Σ ADR Effort in Phase) / (Team Size × Efficiency Factor)
   Efficiency Factor = 0.7 (account for meetings, context switching)
   ```
2. Add inter-phase buffers:
   - Integration testing: 1 week between major phases
   - Security review: 1-2 weeks before production
   - Stakeholder review: Gates between phases
3. Create Gantt chart (Mermaid format):
   ```mermaid
   gantt
       title ADR Implementation Timeline
       dateFormat YYYY-MM-DD
       section Phase 1
       POC: p1, 2025-01-15, 3w
       section Phase 2
       MVP: p2, after p1, 6w
   ```
4. Identify critical milestones:
   - Go/no-go decision points
   - External dependency dates
   - Release windows

**Output**:
- Timeline table (phase, start, end, duration)
- Mermaid Gantt chart
- Milestone list with dates

---

### Step 6: Create Roadmap Document

**Generate comprehensive roadmap** at `{output_file}`:

**Document Structure**:

```markdown
# ADR Implementation Roadmap

## Document Control

| Item | Details |
|------|---------|
| **Project Name** | [Enter project name] |
| **Document Version** | [e.g., 1.0] |
| **Date** | [Current date] |
| **Document Owner** | [Name and title] |
| **Prepared By** | [Technical Lead/Architect name] |
| **Status** | [Draft / In Review / Approved] |

### Document Revision History

| Version | Date | Author | Changes Made | Approver |
|---------|------|--------|--------------|----------|
| 1.0 | [Date] | [Name] | Initial roadmap | |
| | | | | |

## Executive Summary
- Project overview
- Total ADRs: N
- Total phases: M
- Timeline: X weeks
- Team size: Y FTE
- Key milestones

## Phase 1: [Phase Name]
### Objectives
### Duration
### ADRs to Implement
  #### ADR-XXX: Title
  - Complexity: N/5
  - Effort: X hours
  - Scope: What to implement
  - Deferred: What to skip
  - Acceptance Criteria
### System Architecture
  - Mermaid diagram
### Implementation Order
  - Week-by-week breakdown
### Deliverables
### Success Criteria
### Risk Assessment
### Exit Criteria

## Phase 2: [Phase Name]
[Same structure]

...

## ADR Dependency Matrix
- Mermaid flowchart
- Critical path highlighted
- Parallel opportunities

## Technical Debt Management
- POC shortcuts (acceptable)
- MVP shortcuts (acceptable)
- Production standards (zero tolerance)
- Debt remediation timeline

## Risk Assessment
- Phase 1 risks
- Phase 2 risks
- Go/no-go thresholds

## Testing Strategy
- Phase 1: Manual testing only
- Phase 2: Automated unit/integration
- Phase 3: Security, performance, compliance
- Phase 4: Load testing, chaos engineering

## Acceptance Criteria
- Phase 1 acceptance
- Phase 2 acceptance
- [Per phase]

## Traceability
- ADR to Phase mapping table
- Phase to Timeline mapping
- Upstream sources (BRD, PRD)
- Downstream artifacts (SYS, REQ, SPEC)
```

**Document Formatting**:
- Use objective, factual language (per CLAUDE.md guidelines)
- Include Mermaid diagrams for visualizations
- Provide measurable acceptance criteria
- Specify complexity ratings (1-5 scale)
- Document failure modes and risks
- No subjective qualifiers (amazing, easy, powerful)
- Token limit: <100,000 tokens per file

**Output**: Complete roadmap markdown file

---

## Adaptation Guidelines

### For Greenfield Projects

**Characteristics**:
- No existing codebase
- Clean slate architecture
- Can choose optimal tech stack

**Phasing Strategy**:
1. **Front-load infrastructure**: Cloud, database, auth decisions first
2. **Establish baseline**: Technology stack (ADR-000) in Phase 1
3. **Enable parallelization**: Independent modules early
4. **Defer optimization**: Performance tuning to later phases

**Example Phase Structure**:
```
Phase 1: Foundation (Tech stack, cloud, database)
Phase 2: Core Features (Business logic ADRs)
Phase 3: Integration (External services, APIs)
Phase 4: Polish (Performance, UX, advanced features)
```

---

### For Brownfield/Legacy Migration Projects

**Characteristics**:
- Existing production system
- Must maintain backward compatibility
- Gradual migration required

**Phasing Strategy**:
1. **Phase by risk level**: Low-risk changes first for confidence
2. **Maintain compatibility**: Each phase independently deployable
3. **Include rollback plans**: Every phase has back-out procedure
4. **Dual-run periods**: Run old and new systems in parallel

**Example Phase Structure**:
```
Phase 1: Infrastructure Prep (Observability, feature flags)
Phase 2: Low-Risk Migration (Read-only endpoints)
Phase 3: Medium-Risk Migration (Write endpoints with rollback)
Phase 4: High-Risk Migration (Core business logic)
Phase 5: Decommission Legacy (Remove old system)
```

**Migration-Specific Sections to Add**:
- Rollback procedures per phase
- Data migration strategy
- Dual-run validation criteria
- Backward compatibility requirements

---

### For Refactoring Projects

**Characteristics**:
- Improving existing system
- No new features
- Minimize customer-facing changes

**Phasing Strategy**:
1. **Phase by module boundaries**: Refactor one component at a time
2. **Continuous deployment**: Each phase independently deployable
3. **Minimize disruption**: Changes invisible to users
4. **Test extensively**: Heavy emphasis on regression testing

**Example Phase Structure**:
```
Phase 1: Test Infrastructure (Add missing tests)
Phase 2: Module A Refactor (Database layer)
Phase 3: Module B Refactor (API layer)
Phase 4: Module C Refactor (Business logic)
Phase 5: Cleanup (Remove deprecated code)
```

---

## Decision Frameworks

### Framework 1: Phase Scope Decisions

**When to create a new phase?**

Decision tree:
```
1. Check dependencies:
   - New ADRs have no dependencies on current phase? → New phase
   - All dependencies in current/prior phases? → Same phase

2. Check complexity threshold:
   - Current phase exceeds max_phase_duration (8 weeks)? → New phase
   - Under threshold? → Same phase

3. Check risk isolation:
   - ADR is high-risk (complexity 4-5)? → Consider separate phase for POC
   - Low-medium risk? → Group with similar ADRs

4. Check milestone boundary:
   - Natural project milestone (POC, MVP, Beta, GA)? → Phase boundary
   - Mid-milestone? → Same phase
```

**Output**: Phase boundary decision

---

### Framework 2: ADR Sequencing Within Phase

**Order ADRs by**:

Priority ranking (highest to lowest):
1. **Dependency** (hard constraint): Upstream ADRs before downstream
2. **Risk** (strategic):
   - POC phase: High-risk ADRs first (de-risk early)
   - Production phase: Low-risk ADRs first (build confidence)
3. **Complexity** (team morale): Mix high and low complexity
4. **Business value** (stakeholder visibility): High-value features earlier

**Algorithm**:
```python
def sequence_adrs(adrs_in_phase):
    # Step 1: Topological sort by dependencies (must respect)
    sorted_by_deps = topological_sort(adrs_in_phase)

    # Step 2: Within each dependency level, sort by risk/value
    for level in sorted_by_deps:
        if phase == "POC":
            level.sort(key=lambda adr: adr.risk, reverse=True)  # High-risk first
        else:
            level.sort(key=lambda adr: adr.value, reverse=True)  # High-value first

    return flatten(sorted_by_deps)
```

**Output**: Ordered ADR sequence per phase

---

### Framework 3: Complexity Scoring

**Aggregate ADR complexity** when explicit ratings not available:

Estimation heuristics:
```
Complexity 1 (Trivial):
- Simple configuration change
- Library upgrade (no breaking changes)
- Documentation update
- Effort: 1 day

Complexity 2 (Simple):
- Add logging/monitoring
- Simple API endpoint
- Basic CRUD operation
- Effort: 2 days

Complexity 3 (Moderate):
- New authentication provider
- Database schema change
- Third-party integration
- Effort: 3-5 days

Complexity 4 (Complex):
- New deployment architecture
- Real-time data processing
- Multi-service integration
- Effort: 1-2 weeks

Complexity 5 (Architectural):
- Cloud provider migration
- Event-driven architecture
- Major technology swap
- Effort: 3-4 weeks
```

**Output**: Complexity rating per ADR

---

### Framework 4: Technical Debt Classification

**Acceptable shortcuts per phase**:

| Phase | Acceptable Shortcuts | Must Have | Remediation Phase |
|-------|---------------------|-----------|-------------------|
| **POC** | Hardcoded credentials, in-memory data, print logging, no tests, local deployment | Working integration | MVP |
| **MVP** | Basic error handling, simple caching, minimal monitoring | Multi-user auth, persistence, unit tests | Production |
| **Production** | Partial optimization | Full security, monitoring, HA, compliance | Scale |
| **Scale** | Some manual processes | Performance targets, auto-scaling | Advanced |
| **Advanced** | None (continuous improvement) | All features production-grade | N/A |

**Output**: Technical debt tracking table

---

## Example Usage Scenarios

### Example 1: MCP Server Project (27 ADRs)

**User Invocation**:
```
Use the adr-roadmap skill to create implementation roadmap.

Inputs:
- ADR directory: {project_root}/docs/ADR/
- Project context: Interactive Brokers MCP server, 3 developers, POC in 3 weeks
- Phase model: poc-mvp-prod
- Team size: 3

Generate roadmap in {project_root}/docs/ADR/ADR-00_IMPLEMENTATION-ROADMAP.md
```

**Skill Actions**:
1. Read 27 ADRs from `{project_root}/docs/ADR/`
2. Extract complexity: ADR-02 (4/5), ADR-003 (2/5), etc.
3. Parse dependencies: ADR-006 depends on ADR-003
4. Create 5 phases:
   - Phase 1: POC (ADR-000, 001, 002, 003 partial)
   - Phase 2: MVP (ADR-006, 010, 012, 004, 013, 020, 007, 023)
   - Phase 3: Production (ADR-014, 011, 016, 017, 018, 019, 026)
   - Phase 4: Scale (ADR-009, 008, 005, 021, 025)
   - Phase 5: Advanced (ADR-015, 022, 024)
5. Calculate timelines:
   - POC: 2-3 weeks (80 hours / 3 FTE = 2.7 weeks)
   - MVP: 4-6 weeks
   - etc.
6. Generate Mermaid dependency graph
7. Create comprehensive roadmap document

**Generated Output**: `ADR-00_IMPLEMENTATION-ROADMAP.md` (~1,400 lines)

---

### Example 2: Web App Migration (12 ADRs)

**User Invocation**:
```
Use adr-roadmap skill for microservices migration roadmap.

Inputs:
- ADR directory: {example_project_a}/architecture/decisions/
- Project context: Monolith to microservices migration, 8 developers, 9-month timeline
- Phase model: iterative
- Team size: 8

Generate roadmap in {example_project_a}/architecture/decisions/ADR-00_IMPLEMENTATION-ROADMAP.md
```

**Skill Actions**:
1. Read 12 migration ADRs
2. Identify migration ADRs:
   - ADR-01: Service decomposition strategy
   - ADR-02: API gateway selection
   - ADR-003: Service mesh (Istio)
   - ADR-004: Database-per-service pattern
   - etc.
3. Phase by service boundaries (iterative):
   - Iteration 1: User service (ADR-01, 002, 004)
   - Iteration 2: Product service (ADR-005, 006)
   - Iteration 3: Order service (ADR-007, 008)
   - Iteration 4: Payment service (ADR-009, 010)
4. Add migration-specific sections:
   - Dual-run strategy per iteration
   - Rollback procedures
   - Data migration plans
5. Generate roadmap with 4 iterations (2 months each)

**Generated Output**: Migration roadmap with rollback plans

---

### Example 3: Data Platform (35 ADRs, Large Project)

**User Invocation**:
```
Create 6-month data platform roadmap.

Inputs:
- ADR directory: {example_project_b}/docs/ADR/
- Project context: Real-time analytics platform, 10 engineers, 6-month timeline
- Phase model: waterfall
- Team size: 10
- Target phases: 6

Generate roadmap in {example_project_b}/docs/ADR/ADR-00_IMPLEMENTATION-ROADMAP.md
```

**Skill Actions**:
1. Read 35 ADRs across data engineering stack
2. Group ADRs by category:
   - Ingestion: 8 ADRs (Kafka, Kinesis, CDC)
   - Storage: 6 ADRs (Data lake, warehouse, lakehouse)
   - Processing: 10 ADRs (Spark, Flink, DBT)
   - Serving: 6 ADRs (APIs, caching, query engines)
   - Orchestration: 5 ADRs (Airflow, monitoring, alerting)
3. Create 6 monthly phases:
   - Month 1: Ingestion infrastructure
   - Month 2: Storage layer
   - Month 3: Processing pipelines
   - Month 4: Serving layer
   - Month 5: Orchestration
   - Month 6: Optimization & launch
4. Calculate resource allocation (10 engineers across tracks)
5. Generate roadmap with parallel work streams

**Generated Output**: Resource-aware roadmap with 6 phases

---

### Example 4: Embedded Systems (15 ADRs, Hardware Constraints)

**User Invocation**:
```
Create roadmap for IoT device firmware.

Inputs:
- ADR directory: /firmware/docs/adr/
- Project context: IoT sensor firmware, 2 embedded engineers, hardware prototype ready
- Phase model: poc-mvp-prod
- Team size: 2
- Constraints: Hardware prototype available Week 4

Generate roadmap in /firmware/docs/adr/ADR-00_IMPLEMENTATION-ROADMAP.md
```

**Skill Actions**:
1. Read 15 embedded firmware ADRs
2. Identify hardware-dependent vs. software-only ADRs
3. Create phases aligned with hardware milestones:
   - Phase 1: Software simulation (Weeks 1-3)
   - Phase 2: Hardware integration (Weeks 4-6, after prototype)
   - Phase 3: Field testing (Weeks 7-10)
   - Phase 4: Production firmware (Weeks 11-12)
4. Add hardware constraint notes
5. Generate roadmap with hardware dependencies

**Generated Output**: Hardware-aware roadmap with gated phases

---

## Quality Gates (Definition of Done)

Roadmap document must satisfy:

### Completeness
- [ ] All ADRs from directory included
- [ ] Every ADR assigned to exactly one phase
- [ ] All dependencies documented in matrix
- [ ] Timeline calculated for all phases
- [ ] Risk assessment completed per phase
- [ ] Testing strategy defined per phase
- [ ] Acceptance criteria clear per phase
- [ ] Traceability section complete

### Accuracy
- [ ] Dependency graph validated (no circular dependencies)
- [ ] Critical path identified correctly
- [ ] Effort estimates justified from ADR complexity
- [ ] Phase durations realistic for team size
- [ ] Risk ratings aligned with ADR assessments

### Quality
- [ ] Mermaid diagrams render correctly
- [ ] Language objective and factual (CLAUDE.md compliant)
- [ ] No subjective claims (amazing, easy, powerful)
- [ ] Measurable acceptance criteria
- [ ] Token limit <100,000 per document
- [ ] Markdown formatting valid
- [ ] Tables formatted correctly

### Usability
- [ ] Executive summary provides overview
- [ ] Stakeholders can understand timeline
- [ ] Engineers can start implementation from roadmap
- [ ] Clear next actions defined
- [ ] Go/no-go decision criteria explicit

---

## Skill Constraints

### What NOT to Do

- **Do NOT make technology recommendations**: Use ADR decisions as-is
- **Do NOT skip ADRs**: All must be mapped to phases
- **Do NOT create phases >8 weeks**: Break down into smaller phases
- **Do NOT ignore dependencies**: Validate critical path
- **Do NOT use subjective language**: Follow CLAUDE.md guidelines
- **Do NOT guess complexity**: Use ADR ratings or ask for clarification
- **Do NOT create unrealistic timelines**: Account for team size and efficiency
- **Do NOT skip risk assessment**: Every phase requires risk analysis
- **Do NOT omit rollback plans**: Production phases require rollback procedures

### Edge Cases to Handle

**Missing ADR metadata**:
- If complexity rating missing → Estimate from ADR content or default to 3/5
- If dependencies missing → Assume independent (warn user)
- If effort estimate missing → Calculate from complexity

**Circular dependencies**:
- Error condition: Roadmap cannot proceed
- Action: Report circular dependency chain to user
- Resolution: User must update ADRs to break cycle

**Zero ADRs found**:
- Error condition: No ADRs in directory
- Action: Validate directory path, check for different naming convention
- Resolution: User provides correct path

**Conflicting constraints**:
- Example: User wants 3-week POC but ADRs require 6 weeks minimum
- Action: Report constraint conflict with calculations
- Resolution: User adjusts constraints or reduces POC scope

---

## Output Format Specification

### Generated Roadmap Document

**File**: `{project}/docs/ADR/ADR-00_IMPLEMENTATION-ROADMAP.md`

**Size**: 1,000-2,000 lines (varies by ADR count)

**Token Limit**: <100,000 tokens

**Sections** (in order):

1. **Document Header**:
   ```markdown
   # ADR Implementation Roadmap
   ```

2. **Document Control**:
   - Project metadata table (name, version, date, owner, preparer, status)
   - Document Revision History table (version, date, author, changes, approver)

3. **Table of Contents**: Links to all sections

4. **Executive Summary**:
   - Project overview
   - Total ADRs, phases, timeline
   - Key milestones table
   - Critical success factors

5. **Phase Definitions** (1 section per phase):
   - Objectives
   - Duration estimate
   - ADRs to implement (with complexity, effort, scope)
   - System architecture diagram (Mermaid)
   - Implementation order (week-by-week)
   - Deliverables
   - Success criteria
   - Risk assessment
   - Exit criteria

6. **ADR Dependency Matrix**:
   - Mermaid flowchart
   - Critical path highlighted
   - Parallel implementation opportunities

7. **Technical Debt Management**:
   - Acceptable shortcuts per phase
   - Remediation timeline
   - Debt cost estimation

8. **Risk Assessment**:
   - Risks per phase (table format)
   - Go/no-go thresholds

9. **Testing Strategy**:
   - Test approach per phase
   - Coverage goals
   - Test environments

10. **Acceptance Criteria**:
    - Functional requirements per phase
    - Quality attributes per phase
    - Technical validation

11. **Traceability**:
    - ADR to Phase mapping table
    - Phase to Timeline mapping
    - Upstream sources
    - Downstream artifacts

---

## Related Documentation

### AI Dev Flow Framework
- [SPEC_DRIVEN_DEVELOPMENT_GUIDE.md]({project_root}/ai_dev_flow/SPEC_DRIVEN_DEVELOPMENT_GUIDE.md) - Specification-driven development methodology
- [ID_NAMING_STANDARDS.md]({project_root}/ai_dev_flow/ID_NAMING_STANDARDS.md) - Document ID conventions
- [TOOL_OPTIMIZATION_GUIDE.md]({project_root}/ai_dev_flow/TOOL_OPTIMIZATION_GUIDE.md) - Token limits and optimization

### Related Skills
- [project-mngt](../project-mngt/) - Use for requirement-based planning (BRD/PRD → MVP)
- [doc-flow](../doc-flow/) - Use for generating SYS/REQ/SPEC documents from ADRs
- [charts-flow](../charts-flow/) - Use for enhanced Mermaid diagram generation

### ADR Documentation
- [ADR-TEMPLATE.md]({project_root}/ai_dev_flow/ADR/ADR-TEMPLATE.md) - ADR template structure
- [README.md]({project_root}/ai_dev_flow/ADR/README.md) - ADR documentation guide

---

## Related Skills

### Use `project-mngt` Skill Instead When:
- Planning from business/product requirements (BRD/PRD), not architectural decisions
- Defining MVP/MMP/MMR scope before technical design
- No ADRs exist yet (requirements → ADRs workflow)
- Need product roadmap vs. implementation roadmap

### Use `doc-flow` Skill Instead When:
- Generating SYS/REQ/SPEC documents from ADRs
- Creating detailed specification artifacts
- Not focused on implementation phasing or timeline
- Need traceability matrix generation

### Combine `adr-roadmap` + `charts-flow` When:
- Need enhanced visualizations beyond standard Mermaid
- Want architecture diagrams alongside roadmap
- Require multiple diagram types (sequence, C4, state machines)

### Combine `adr-roadmap` + `project-mngt` When:
- Have both requirements (BRD/PRD) and architectural decisions (ADR)
- Need to align product roadmap with implementation roadmap
- Want to map features to ADR phases

---

## Version

- **Version:** 1.0.0
- **Last Updated:** 2025-01-08
- **Created:** 2025-01-08
- **Author:** AI Dev Flow Framework
- **Status:** Active

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-01-08 | Initial skill creation with comprehensive methodology |

---

**End of Skill Definition**
