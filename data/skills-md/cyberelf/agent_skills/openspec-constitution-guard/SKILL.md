---
name: openspec-constitution-guard
description: This skill composes project AGENTS.md constitution files into openspec/config.yaml to inject quality validation gates into OpenSpec workflows. Use this skill when initializing openspec for the first time in a project or when AGENTS.md files are updated. The skill ensures openspec artifacts are validated against project-specific quality criteria from constitutions.
metadata:
  author: cyberelf
  version: "1.0"
---

# OpenSpec Constitution Guard

This skill ensures OpenSpec workflows enforce project-specific quality assurance criteria derived from AGENTS.md constitution files by injecting them into `openspec/config.yaml`.

## Purpose

OpenSpec workflows (`/opsx:apply`, `/opsx:verify`, `/opsx:archive`, etc.) include generic validation. This skill enriches them with **project-specific quality gates** extracted from AGENTS.md files across the workspace, ensuring all artifacts pass the project's defined testing and QA criteria before handoff.

## When to Use

Trigger this skill when:
- Initializing openspec for the first time in a project (`openspec init`)
- An AGENTS.md file is created, modified, or deleted in the project
- User explicitly requests to sync constitution quality gates with openspec config
- Validating that openspec configuration is up-to-date with constitution requirements

## Detection: When to Run

To detect if guards need composition:
1. Check if `openspec/config.yaml` exists
2. Look for `<!-- CONSTITUTION-GUARD:START` marker in the config file
3. If marker is missing → first-time setup needed
4. If AGENTS.md files have changed since `Last Updated` date → refresh needed

## Workflow

### Step 1: Locate All Constitution Files

Find all AGENTS.md files in the workspace:
```bash
find . -name "AGENTS.md" -type f | grep -v node_modules | grep -v .venv | grep -v target | grep -v openspec/AGENTS.md
```

**Exclude** `openspec/AGENTS.md` as it contains OpenSpec usage instructions already referenced by the system, not project-specific quality criteria.

Read each remaining file to understand its scope (root project, backend, frontend, specific module, etc.).

### Step 2: Read and Understand Quality Criteria

For each AGENTS.md file, identify sections related to quality assurance. Look for:
- Headings containing: "Quality", "Testing", "Checks", "Validation", "Assurance", "Checklist"
- Command examples (typically in backticks or code blocks)
- Goals or acceptance criteria (e.g., "Zero errors", "All tests pass")
- Architecture patterns and coding standards that should be enforced

**Key information to extract:**
1. **Automated commands** - What tools/commands must be run (e.g., `pytest`, `npm run lint`)
2. **Success criteria** - What constitutes passing (e.g., "zero warnings")
3. **Architecture rules** - Patterns that must be followed (e.g., "service layer separation")
4. **Testing requirements** - Coverage expectations, test types needed
5. **Stack identification** - What technology stack does this constitution govern

### Step 3: Interpret Criteria for Artifacts

Map the extracted criteria to specific OpenSpec artifacts in the config.yaml rules:

#### For `proposal` Artifact
Extract rules that validate **design decisions**:
- Architecture patterns that must be followed
- Type safety requirements
- Naming conventions
- What requires a proposal vs direct fix
- Breaking change documentation requirements

#### For `specs` Artifact
Extract rules that validate **specification quality**:
- Required sections in specs
- Format requirements (e.g., "Given/When/Then")
- Edge cases that must be documented
- API contract requirements

#### For `design` Artifact
Extract rules that validate **technical design**:
- Design patterns to follow
- System architecture requirements
- Integration points to consider
- Technology choices and their justification

#### For `tasks` Artifact
Extract rules that validate **implementation planning**:
- Task breakdown requirements
- Testing tasks that must be included
- Documentation tasks
- Deployment considerations

#### For General Context
Extract information that should be available to **all artifacts**:
- Tech stack information
- Coding conventions
- Team practices
- Backwards compatibility requirements

### Step 4: Compose the config.yaml

Create or update `openspec/config.yaml` with the constitution guards. The file should include:

1. **Context section**: Project-wide information injected into ALL artifacts
2. **Rules section**: Per-artifact specific validation rules
3. **Constitution metadata**: Source files and update timestamp

Template structure:
```yaml
# openspec/config.yaml

# Schema selection (if you have a preferred one)
schema: spec-driven

# <!-- CONSTITUTION-GUARD:START - Auto-generated from AGENTS.md files -->
# Context injected into ALL artifacts
context: |
  [PROJECT-WIDE CONTEXT]

# Per-artifact validation rules
rules:
  proposal:
    - [PROPOSAL-SPECIFIC RULES]
  
  specs:
    - [SPECS-SPECIFIC RULES]
  
  design:
    - [DESIGN-SPECIFIC RULES]
  
  tasks:
    - [TASKS-SPECIFIC RULES]

# Constitution metadata
# Source Constitutions:
# - [List each AGENTS.md file path]
# Last Updated: [YYYY-MM-DD]
# <!-- CONSTITUTION-GUARD:END -->
```

### Step 5: Update Configuration File

1. Check if `openspec/config.yaml` exists
   - If not, create it with initial configuration
   - If yes, read current content
2. Locate the `<!-- CONSTITUTION-GUARD:START` marker
3. If existing guard block found, replace it entirely
4. If no existing block, append to the file
5. Preserve any existing `schema:` declaration at the top
6. Ensure proper YAML formatting is maintained

**Critical**: Always validate YAML syntax after generation to ensure the file is parseable.

## Example Outputs

### Example: Basic Configuration

After reading constitutions with Python backend and TypeScript frontend:

```yaml
# openspec/config.yaml

schema: spec-driven

# <!-- CONSTITUTION-GUARD:START - Auto-generated from AGENTS.md files -->
# Context injected into ALL artifacts
context: |
  Tech stack: Python (FastAPI, Pydantic), TypeScript (React, Node.js), PostgreSQL
  Architecture: Service layer pattern - business logic in services/, API routes are thin
  Type safety: Strict typing required (no Any/any types)
  API style: RESTful with OpenAPI docs
  Testing: pytest + React Testing Library
  We value backwards compatibility for all public APIs

# Per-artifact validation rules
rules:
  proposal:
    - Include rollback plan for breaking changes
    - Mark breaking changes with **BREAKING** prefix
    - Identify affected teams/systems
    - Verify alignment with service layer architecture
  
  specs:
    - Use Given/When/Then format for scenarios
    - Document all edge cases and error conditions
    - Reference existing patterns before proposing new ones
    - Include API contract changes if applicable
  
  design:
    - Maintain service layer separation (logic in services/, not api/)
    - Use Pydantic models for all new data structures
    - Ensure strict typing (no Any types in Python/TypeScript)
    - Document integration points with existing services
  
  tasks:
    - Include unit test tasks for all new service logic
    - Include integration test tasks for API changes
    - Add type checking verification tasks
    - Include documentation update tasks

# Source Constitutions:
# - AGENTS.md
# - backend/AGENTS.md
# - frontend/AGENTS.md
# Last Updated: 2026-02-09
# <!-- CONSTITUTION-GUARD:END -->
```

### Example: With Automated Check Commands

After reading constitutions with specific test commands:

```yaml
# openspec/config.yaml

schema: spec-driven

# <!-- CONSTITUTION-GUARD:START - Auto-generated from AGENTS.md files -->
context: |
  Tech stack: Python (uv, FastAPI), TypeScript (Vite, React), PostgreSQL
  Automated checks required before completion:
  - Python: uv run pytest, uv run ruff check ., uv run pyright .
  - TypeScript: npm run lint, npm run tsc, npx playwright test
  Architecture: Microservices with event-driven communication
  All services must be independently deployable

rules:
  proposal:
    - Identify service boundaries affected
    - Document event schema changes
    - Include deployment strategy
    - Consider backwards compatibility for events
  
  specs:
    - Document event payloads in Given/When/Then scenarios
    - Include failure/retry scenarios
    - Specify service dependencies
  
  design:
    - Show event flow diagrams for cross-service changes
    - Use async/await patterns for I/O operations
    - Maintain service independence
  
  tasks:
    - Before marking complete, run: uv run pytest (Python)
    - Before marking complete, run: npm run lint && npm run tsc (TypeScript)
    - Include E2E test tasks for cross-service scenarios
    - Add event contract validation tasks

# Source Constitutions:
# - AGENTS.md
# - services/user/AGENTS.md  
# - services/order/AGENTS.md
# Last Updated: 2026-02-09
# <!-- CONSTITUTION-GUARD:END -->
```

### Example: Complex Multi-Stack Project

After reading constitutions from root, backend (Python), frontend (React), and mobile (Swift):

```yaml
# openspec/config.yaml

schema: spec-driven

# <!-- CONSTITUTION-GUARD:START - Auto-generated from AGENTS.md files -->
context: |
  Multi-platform project with shared API
  
  Backend (Python):
  - FastAPI + SQLAlchemy + Alembic
  - Service layer required for all business logic
  - Commands: uv run pytest, uv run ruff check ., uv run mypy .
  
  Web Frontend (TypeScript/React):
  - Vite + React + TanStack Query
  - Commands: npm run lint, npm run type-check, npm test
  
  Mobile (Swift):
  - SwiftUI + Combine
  - Commands: swift test, swiftlint
  
  Shared API contracts documented in docs/api/
  Zero tolerance for breaking changes without migration plan

rules:
  proposal:
    - Mark platform scope (backend/web/mobile/api)
    - For API changes, document impact on all clients
    - Include migration strategy for breaking changes
    - Specify API versioning approach if needed
  
  specs:
    - Use platform-specific scenario tags: [Backend], [Web], [Mobile]
    - Document API contract changes in OpenAPI format
    - Include backwards compatibility scenarios
    - Reference existing patterns from project codebase
  
  design:
    - Show component/service interaction diagrams
    - Maintain service layer in backend (no logic in routes)
    - Use proper state management patterns per platform
    - Document data flow for cross-platform features
  
  tasks:
    - Group tasks by platform with clear labels
    - Backend: Include pytest, ruff, mypy verification
    - Web: Include lint, type-check, unit test tasks
    - Mobile: Include SwiftLint and unit test tasks
    - For API changes, include contract validation task
    - Include platform-specific E2E test tasks

# Source Constitutions:
# - AGENTS.md
# - backend/AGENTS.md
# - frontend/AGENTS.md
# - mobile/AGENTS.md
# Last Updated: 2026-02-09
# <!-- CONSTITUTION-GUARD:END -->
```

## Interpretation Guidelines

When reading AGENTS.md files with varying structures:

1. **Look for imperative language**: "MUST", "SHALL", "required", "always"
2. **Identify command patterns**: Anything in backticks that looks like a shell command
3. **Find success criteria**: Phrases like "zero errors", "all pass", "no warnings"
4. **Recognize stack indicators**: Framework names, file extensions, folder names
5. **Extract checklists**: Bullet points with checkboxes or numbered items

### Categorizing Extracted Information

**For Context (applies to all artifacts):**
- Technology stack descriptions
- Architectural principles
- Naming conventions
- Team practices
- Backwards compatibility requirements
- General coding standards

**For Rules (specific to artifacts):**
- Specific format requirements (e.g., "Use Given/When/Then")
- Required sections in artifacts
- Validation commands to run
- Architecture patterns to enforce
- Testing requirements
- Documentation standards

If a constitution section is ambiguous, interpret conservatively—include the check rather than omit it.

All constitution items should be derived from project AGENTS.md files only, **DO NOT** include OpenSpec's own AGENTS.md or any common sense or best practices from other materials.

## How OpenSpec Uses the Configuration

When an OpenSpec command generates or works with an artifact, your configuration is automatically injected:

### Context Injection (ALL artifacts)
```
<context>
Tech stack: Python (FastAPI, Pydantic), TypeScript (React, Node.js), PostgreSQL
Architecture: Service layer pattern - business logic in services/, API routes are thin
Type safety: Strict typing required (no Any/any types)
...
</context>

<template>
[Schema's built-in template for this artifact]
</template>
```

### Rules Injection (matching artifact only)
For `/opsx:continue proposal` or when generating a proposal:
```
<rules>
- Include rollback plan for breaking changes
- Mark breaking changes with **BREAKING** prefix
- Identify affected teams/systems
- Verify alignment with service layer architecture
</rules>
```

This ensures every artifact is generated with your project's specific requirements in mind.

## Related OpenSpec Commands

Understanding which commands work with which artifacts:

| Command | Purpose | Affected Artifacts |
|---------|---------|-------------------|
| `/opsx:new` | Start a change | Creates change directory |
| `/opsx:continue` | Create next artifact | proposal → specs → design → tasks |
| `/opsx:ff` | Fast-forward (create all planning) | proposal, specs, design, tasks |
| `/opsx:apply` | Implement tasks | Works from tasks.md |
| `/opsx:verify` | Validate implementation | Checks against all artifacts |
| `/opsx:sync` | Merge specs to main | Updates openspec/specs/ |
| `/opsx:archive` | Complete change | Finalizes and archives |

Your constitution rules in config.yaml affect the quality and validation of artifacts throughout this workflow.

## Maintenance

When updating guards:
1. Re-read all AGENTS.md files
2. Extract updated quality criteria
3. Locate the `<!-- CONSTITUTION-GUARD:START` block in config.yaml
4. Replace the entire block with newly generated content
5. Preserve any existing `schema:` declaration at the top
6. Validate YAML syntax
7. Update the `Last Updated` timestamp
8. Test with `openspec new test-change` to verify configuration loads correctly

### Validation After Update

After updating config.yaml, verify it works:
```bash
# Check YAML syntax
python -c "import yaml; yaml.safe_load(open('openspec/config.yaml'))"

# Test with a dummy change
openspec new test-validation
# Check if context and rules are properly injected in artifacts
```

If you see errors about context or rules not being injected, check YAML indentation and structure.
