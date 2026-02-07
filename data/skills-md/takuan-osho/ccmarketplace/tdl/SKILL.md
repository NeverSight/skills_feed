---
name: tdl
description: This skill should be used when implementing or improving Traceable Development Lifecycle (TDL) practices in software projects. Use this skill to establish end-to-end traceability from requirements through design, implementation, testing, deployment, and operations. Provides tools, templates, and best practices for ADRs, commit messages, PR templates, structured logging, and traceability analysis.
---

# Traceable Development Lifecycle (TDL) Skill

## Overview

TDL is a template-based development process that ensures complete traceability from requirements to implementation. It supports parallel development by multiple developers or AI agents through random ID generation and distributed traceability.

## Key Features

- **Random Base36 IDs**: 5-character IDs (e.g., `a3bf2`) prevent conflicts in parallel development
- **Distributed Traceability**: Each document maintains its own Links section - no central tracking file
- **5-Phase Workflow**: Analysis → Requirements → ADR → Design → Plan & Execution
- **Document Templates**: Standardized templates for all document types

## When to Use This Skill

Use this skill when:

- **Starting a new project** and want to establish traceability from the beginning
- **Improving existing projects** to add or enhance traceability practices
- **Creating documentation** (Analysis, Requirements, ADRs, Design, Plans)
- **Working in parallel** with other developers or AI agents
- **Troubleshooting production issues** and need to trace back to requirements/design
- **Conducting requirement analysis** and tracking implementation coverage

## Interactive Mode (Claude Code only)

When running in Claude Code and the user's intent is unclear, use AskUserQuestion tool to clarify:

**Document Type** (if not specified in the user's request):
- Question: "What type of TDL document do you want to create?"
- Header: "Doc Type"
- Options:
  - "Analysis (AN-)" - Problem exploration and discovery
  - "Requirement (FR/NFR-)" - Formal specification with acceptance criteria
  - "ADR (ADR-)" - Architecture/design decision record
  - "Task (T-)" - Implementation plan with design.md and plan.md

**Requirement Type** (when creating a requirement):
- Question: "What type of requirement is this?"
- Header: "Req Type"
- Options:
  - "FR - Functional Requirement (Recommended)" - Feature or behavior specification
  - "NFR - Non-Functional Requirement" - Performance, security, scalability, etc.

**NFR Category** (when creating a non-functional requirement):
- Question: "What category does this NFR belong to?"
- Header: "Category"
- Options:
  - "Performance" - Response time, throughput
  - "Security" - Authentication, authorization, data protection
  - "Scalability" - Load handling, growth capacity
  - "Reliability" - Availability, fault tolerance
- If user needs a different category, they can specify via the "Other" option

**ADR Template** (when creating an ADR):
- Question: "Which ADR template should be used?"
- Header: "Template"
- Options:
  - "Full ADR (Recommended)" - Comprehensive template for significant decisions
  - "Lite ADR" - Simplified template for tactical decisions

## TDL Workflow Phases

```
┌─────────────┐    ┌──────────────┐    ┌─────────┐    ┌────────┐    ┌──────────────────┐
│  Analysis   │───▶│ Requirements │───▶│   ADR   │───▶│ Design │───▶│ Plan & Execution │
│   (AN-)     │    │   (FR/NFR)   │    │ (ADR-)  │    │        │    │                  │
└─────────────┘    └──────────────┘    └─────────┘    └────────┘    └──────────────────┘
     │                    │                 │              │                  │
     │                    │                 │              │                  │
     ▼                    ▼                 ▼              ▼                  ▼
  Explore             Formalize         Document       Technical       Implementation
  problem             what/why          decisions       design           phases
```

### Phase 1: Analysis (AN-xxxxx)

**Purpose**: Explore problem space and discover requirements

**Output**: `docs/analysis/AN-xxxxx-topic.md`

```bash
python scripts/create_analysis.py "User Authentication Flow"
```

**Lifecycle**: Draft → Active → Complete → Archived (after requirements formalized)

### Phase 2: Requirements (FR-xxxxx / NFR-xxxxx)

**Purpose**: Formalize what needs to be built with measurable acceptance criteria

**Output**:
- Functional: `docs/requirements/FR-xxxxx-topic.md`
- Non-Functional: `docs/requirements/NFR-xxxxx-topic.md`

```bash
python scripts/create_requirement.py "User Authentication" --type FR
python scripts/create_requirement.py "API Response Time" --type NFR --category Performance
```

**Lifecycle**: Proposed → Accepted → Implemented → Verified → (Deprecated)

### Phase 3: Architecture Decision Records (ADR-xxxxx)

**Purpose**: Document important design decisions and their rationale

**Output**: `docs/adr/ADR-xxxxx-topic.md`

```bash
python scripts/create_adr.py "Use PostgreSQL for data storage"
python scripts/create_adr.py "Minor API change" --lite  # For tactical decisions
```

**Lifecycle**: Proposed → Accepted | Rejected → (Deprecated | Superseded by ADR-xxxxx)

### Phase 4 & 5: Design and Plan (T-xxxxx)

**Purpose**: Technical design and phased implementation plan

**Output**: `docs/tasks/T-xxxxx-topic/`
- `design.md`: How to implement (technical design)
- `plan.md`: What to do (phased implementation)

```bash
python scripts/create_task.py "implement-user-auth" --requirements FR-a1b2c,FR-d3e4f
```

**Lifecycle**: Not Started → Phase X In Progress → Blocked → Under Review → Completed

## Random ID System

TDL uses 5-character Base36 random IDs instead of sequential numbers to prevent conflicts in parallel development.

### Why Random IDs?

| Sequential IDs | Random IDs |
|---------------|------------|
| `FR-001`, `FR-002` | `FR-a3bf2`, `FR-b4cd8` |
| Conflicts when parallel work | No conflicts |
| Requires coordination | Independent generation |
| Central tracking file | Distributed traceability |

### ID Format

- **Characters**: 0-9 and a-z (Base36)
- **Length**: 5 characters
- **Combinations**: ~60 million
- **Collision probability**: ~1% at 1,100 documents

### Generate IDs

```bash
# Generate a raw ID
python scripts/tdl_new_id.py

# Generate with prefix
python scripts/tdl_new_id.py --prefix FR
# Output: FR-a3bf2
```

## Directory Structure

```
docs/
├── analysis/           # Problem exploration (AN-xxxxx)
│   ├── archive/        # Completed analyses
│   └── AN-a3bf2-topic.md
├── requirements/       # Formal requirements (FR/NFR-xxxxx)
│   ├── FR-b4cd8-topic.md
│   └── NFR-c5de9-topic.md
├── adr/               # Architecture decisions (ADR-xxxxx)
│   ├── archive/       # Deprecated/superseded ADRs
│   └── ADR-d6ef0-topic.md
├── tasks/             # Implementation tasks (T-xxxxx)
│   └── T-e7fa1-topic/
│       ├── design.md
│       └── plan.md
└── templates/         # Document templates
```

## Distributed Traceability

Every TDL document has a **Links** section that maintains relationships to other documents:

```markdown
## Links

- **Analysis**: [AN-a3bf2](../analysis/AN-a3bf2-topic.md)
- **Requirements**: [FR-b4cd8](../requirements/FR-b4cd8-topic.md)
- **Related ADRs**: N/A – First implementation
- **Issue**: #123
- **PR**: N/A – Not yet submitted
```

### Rules for Links

1. **Always include all link categories** - use `N/A – <reason>` if not applicable
2. **Use relative paths** for internal links
3. **External references** go in a separate section
4. **Update links** when relationships change

## Available Scripts

### Initialize TDL Structure

```bash
python scripts/init_tdl_docs.py [path]
```

Creates the complete directory structure and README files.

### Generate Random ID

```bash
python scripts/tdl_new_id.py [--prefix PREFIX]
```

Generates a unique 5-character Base36 ID with optional prefix.

### Create Documents

```bash
# Analysis
python scripts/create_analysis.py "Topic Name"

# Requirements
python scripts/create_requirement.py "Title" --type FR|NFR [--category Category]

# ADR
python scripts/create_adr.py "Decision Title" [--lite]

# Task (with design.md and plan.md)
python scripts/create_task.py "task-name" [--requirements FR-xxxxx,NFR-xxxxx]
```

### Analyze Traceability

```bash
# Show status summary
python scripts/trace_status.py

# Detailed report
python scripts/trace_status.py --verbose

# CI mode (exit 1 if gaps found)
python scripts/trace_status.py --check

# Markdown output
python scripts/trace_status.py --format markdown
```

## Document Templates

### Common Structure

All documents follow this structure:

```markdown
# Title

## Metadata

- **ID**: [TYPE-xxxxx]
- **Type**: [Document Type]
- **Owner**: [Person or role]
- **Reviewers**: [List]
- **Status**: [Status]
- **Date**: YYYY-MM-DD

## Links

- **[Link Type]**: [ID or N/A – reason]
...

## [Content Sections]
...

## External References

- [External links]
```

### Template Rules

1. **Language**: All documents in English
2. **Date format**: YYYY-MM-DD
3. **ID placement**: In Metadata, not in title
4. **Links section**: Required in all documents

## Code Integration

### In Commits

```bash
git commit -m "feat(auth): Implement JWT authentication

Implements FR-b4cd8 User Authentication
Related ADR: ADR-d6ef0

Closes: #123"
```

### In Code Comments

```python
class AuthMiddleware:
    """JWT authentication middleware.

    Implements: FR-b4cd8
    Design: docs/tasks/T-e7fa1-implement-auth/design.md
    """
```

### In Logs

```python
logger.info(
    "User authenticated",
    extra={
        "requirement": "FR-b4cd8",
        "user_id": user_id,
        "action": "auth.login.success"
    }
)
```

## Best Practices

### Document Management

1. **Create documents using scripts** - ensures proper ID generation and structure
2. **Update Links immediately** - when relationships are established
3. **Archive completed analyses** - after requirements are formalized
4. **Update status regularly** - reflect current state

### Parallel Development

1. **Always use random IDs** - never manually assign sequential numbers
2. **Check traceability before merging** - `python scripts/trace_status.py --check`
3. **No central tracking file** - rely on Links sections in documents
4. **Resolve conflicts in content, not IDs** - IDs should never conflict

### Quality Assurance

1. **Run traceability analysis** - before releases and in CI
2. **Fill all gaps** - orphan requirements need tasks, orphan tasks need requirements
3. **Review Links section** - in code reviews

## Quick Start

### For New Projects

```bash
# 1. Initialize structure
python scripts/init_tdl_docs.py

# 2. Start with analysis
python scripts/create_analysis.py "Initial Project Analysis"

# 3. Create requirements from analysis
python scripts/create_requirement.py "Core Feature" --type FR

# 4. Document design decisions
python scripts/create_adr.py "Technology Stack Selection"

# 5. Create implementation task
python scripts/create_task.py "implement-core-feature" --requirements FR-xxxxx
```

### For Existing Projects

```bash
# 1. Initialize structure (won't overwrite existing)
python scripts/init_tdl_docs.py

# 2. Check current traceability
python scripts/trace_status.py

# 3. Document existing architecture
python scripts/create_adr.py "Current Architecture Overview"

# 4. Gradually add traceability to new work
```

## Reference Materials

The `references/` directory contains:

- **`adr-template.md`** - ADR writing guide with examples
- **`commit-message-guide.md`** - Commit message standards
- **`pr-template.md`** - Pull request templates
- **`logging-patterns.md`** - Structured logging patterns
- **`api_reference.md`** - Script API documentation

## Troubleshooting

### "ID collision detected"

The script automatically retries up to 10 times. If this persists:
- Check if docs/ directory has an unusually large number of documents
- Manually verify the generated ID doesn't exist

### "Traceability gaps identified"

Run `python scripts/trace_status.py --verbose` to see:
- Requirements without implementing tasks
- Tasks without linked requirements

### "Links section missing"

All documents must have a Links section. Use the creation scripts to ensure proper structure.

## Summary

TDL provides a systematic approach to software development traceability:

| Component | Purpose |
|-----------|---------|
| Random IDs | Prevent parallel development conflicts |
| 5 Phases | Structured workflow from analysis to execution |
| Links Section | Distributed traceability without central file |
| Scripts | Automate document creation and analysis |
| Templates | Ensure consistent documentation |

Start small, use the provided scripts, and gradually build a culture of traceability.
