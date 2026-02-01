---
name: create-plan
description: Create detailed implementation plans through interactive research and iteration. This skill should be used when creating new implementation plans, designing feature specifications, planning technical work, or when the user asks to plan an implementation. Triggers on requests like "create a plan", "plan the implementation", "design how to implement", or when given a feature/task that needs structured planning before implementation.
context: fork
agent: Plan
---

# Create Plan

Create detailed, well-researched implementation plans through interactive collaboration and thorough codebase investigation.

## When to Use This Skill

- Planning new features or functionality
- Designing technical implementations before coding
- Creating phased development roadmaps
- Structuring complex refactoring work
- Any task requiring upfront planning and design

## Initial Input Handling

Parse the user's request to identify:

1. **Task description** - What needs to be implemented
2. **Context files** - Relevant existing code or documentation
3. **Constraints** - Timeline, technology, or scope limitations

| Scenario | Action |
|----------|--------|
| Parameters provided | Read all referenced files completely, then proceed to Research |
| Missing task description | Ask: "What feature or functionality should I plan?" |
| No context provided | Ask: "Are there existing files or documentation I should review?" |

## Planning Workflow

### Phase 1: Research

**Critical**: Thoroughly investigate the codebase before planning.

Spawn parallel sub-tasks using specialized agents:

```
Research Tasks:
- codebase-locator: Find all files related to the feature area
- codebase-analyzer: Understand existing patterns and architecture
- Explore: Investigate integration points and dependencies
```

For each research task, provide:
- Specific directories to examine
- Exact patterns or code to find
- Required output: file:line references

**Read all identified files completely** - no partial reads or summaries.

### Phase 2: Present Understanding

Before any design work, present findings:

1. **Codebase Analysis**
   - Relevant existing code with file:line references
   - Current patterns and conventions discovered
   - Integration points and dependencies

2. **Clarifying Questions**
   - Ask only questions that code investigation couldn't answer
   - Focus on business logic, user requirements, edge cases
   - Avoid questions answerable by reading more code

Wait for user response before proceeding.

### Phase 3: Research User Corrections

**Critical**: Do not accept user corrections at face value.

When the user provides corrections or additional context:
1. Verify claims through code investigation
2. Cross-reference with discovered patterns
3. Resolve any conflicts between user input and codebase reality

If conflicts exist, present findings and discuss before proceeding.

### Phase 4: Design Options

Present design approaches with trade-offs:

```
Option A: [Approach Name]
- Description: [How it works]
- Pros: [Benefits]
- Cons: [Drawbacks]
- Fits pattern: [Reference to existing codebase patterns]

Option B: [Alternative Approach]
- Description: [How it works]
- Pros: [Benefits]
- Cons: [Drawbacks]
- Fits pattern: [Reference to existing codebase patterns]

Recommendation: [Preferred option with rationale]
```

Wait for user feedback on approach before detailing phases.

### Phase 4b: Document Decision (ADR)

**Before creating a new ADR**, check for existing related decisions:

```
# Tiered ADR reading (context conservation)
1. Read("docs/decisions/INDEX.md")           # Scan all ADRs
2. Read("docs/decisions/ADR-NNNN.md", limit=10)  # Quick Reference only
3. Read full ADR only if directly relevant
```

**After user approves a design option**, invoke the ADR skill to document the decision:

```
Skill(skill="adr"): Document the design decision just made.

Context: [Why this decision was needed - from research phase]
Options Considered: [List options from Phase 4]
Decision: [The chosen option]
Rationale: [Why this option was selected]
Consequences: [Expected impacts]
```

The ADR will be created at `docs/decisions/ADR-NNNN-title.md` and INDEX.md will be updated.

**Update the plan** to reference the ADR in the Design Decision section:

```markdown
## Design Decision

[Brief description of chosen approach]

See [ADR-NNNN](../decisions/ADR-NNNN-title.md) for full rationale and alternatives considered.
```

**When to create ADRs during planning:**
- Choosing between architectural approaches
- Selecting technologies or libraries
- Establishing new patterns or conventions
- Making trade-offs with significant implications
- Decisions that future developers will question "why?"

### Phase 5: Phase Structure Review

Before writing detailed plan, present proposed phases:

```
Proposed Implementation Phases:

Phase 1: [Name] - [Brief description]
Phase 2: [Name] - [Brief description]
Phase 3: [Name] - [Brief description]

Does this structure make sense? Any phases to add/remove/reorder?
```

Get explicit approval before writing the full plan.

### Phase 6: Write the Plan

Write the implementation plan to the designated location:

**Default path**: `docs/plans/YYYY-MM-DD-description.md`

Use this structure:

```markdown
# Implementation Plan: [Feature Name]

## Overview
[2-3 sentence summary of what will be implemented]

## Context
[Background, motivation, relevant existing code references]

## Design Decision
[Chosen approach and rationale]

**ADR Reference**: [ADR-NNNN](../decisions/ADR-NNNN-title.md)

## Related ADRs
- [ADR-NNNN](../decisions/ADR-NNNN-title.md): [Brief description of relevance]

## Implementation Phases

### Phase 1: [Name]

**Objective**: [What this phase accomplishes]

**Verification Approach**: [How will we verify this phase works? What tests, commands, or checks will confirm success?]

**Tasks** (tests first, then implementation):
- [ ] Write tests: [test file] covering [scenarios]
- [ ] Implement: [file] to make tests pass
- [ ] Verify: [specific check or command]

**Exit Conditions**:

> Phase cannot proceed until ALL conditions pass.

Build Verification:
- [ ] `[build command]` succeeds
- [ ] `[lint command]` passes
- [ ] `[typecheck command]` passes (if applicable)

Runtime Verification:
- [ ] Application starts: `[start command]`
- [ ] No runtime errors in console
- [ ] [Service/endpoint] is accessible at [URL]

Functional Verification:
- [ ] `[test command]` passes
- [ ] [Specific test]: `[targeted test command]`
- [ ] [Manual check]: [Observable behavior to verify]

### Phase 2: [Name]
[Continue pattern...]

## Dependencies
[External dependencies, prerequisites, blockers]

## Risks and Mitigations
[Potential issues and how to handle them]
```

### Phase 7: Bootstrap Tasks

After writing the plan file, create Tasks for progress tracking:

**Process:**
1. Generate a task list ID from plan filename: `plan-{filename-without-extension}`
   - Example: `2026-01-24-user-auth.md` → `plan-2026-01-24-user-auth`

2. Create a Task for each phase:
   ```
   TaskCreate:
     subject: "Phase N: [Phase Name]"
     description: "[Phase objective] - Plan: [plan file path]"
     activeForm: "Implementing Phase N: [Name]"
   ```

3. Set sequential dependencies:
   ```
   TaskUpdate:
     taskId: [phase-N]
     addBlockedBy: [phase-(N-1)]  # Each phase blocked by previous
   ```

4. Add task list ID to plan metadata (top of file):
   ```markdown
   ---
   task_list_id: plan-2026-01-24-user-auth
   ---
   ```

**Completion Message:**
```
Plan created: [path]
Tasks created: [count] phases with sequential dependencies
Task List ID: [task_list_id]

To work on this plan:
  Single session:  /implement-plan [path]
  Multi-session:   CLAUDE_CODE_TASK_LIST_ID=[task_list_id] claude

Use the same task_list_id across sessions to share progress.
```

## Multi-Session Support

Tasks persist on the filesystem and can be shared across Claude Code sessions.

**Starting a shared session:**
```bash
CLAUDE_CODE_TASK_LIST_ID=plan-2026-01-24-user-auth claude
```

**Benefits:**
- Multiple developers can work on the same plan
- Progress syncs automatically via shared task list
- Dependency tracking prevents conflicts (blocked tasks visible)
- Resume from any session with the same task_list_id

**Task States:**
```
◻ #1 Phase 1: Setup
◻ #2 Phase 2: Core Logic › blocked by #1
◻ #3 Phase 3: Integration › blocked by #2
◻ #4 Phase 4: Testing › blocked by #3
```

## Critical Guidelines

### Verification-First Planning

Every phase in the plan MUST include:

1. **Verification Approach** - A clear statement of how success will be measured
2. **Tests before implementation** - Task lists must show test creation BEFORE implementation
3. **Specific test scenarios** - Not just "write tests" but what scenarios to cover

Example:
```markdown
**Verification Approach**: Unit tests verify password hashing and comparison.
Integration test confirms login endpoint accepts valid credentials and rejects invalid ones.

**Tasks** (tests first, then implementation):
- [ ] Write tests: `auth.service.spec.ts` covering hash generation, hash comparison, invalid inputs
- [ ] Write tests: `auth.controller.spec.ts` covering login success, login failure, missing credentials
- [ ] Implement: `auth.service.ts` - password hashing utilities
- [ ] Implement: `auth.controller.ts` - login endpoint
- [ ] Verify: `npm test -- auth` passes
```

### Be Thorough
- Read entire files, not partial content
- Verify facts through code investigation
- Follow import chains to understand dependencies

### Be Interactive
- Get buy-in at each step
- Allow course corrections throughout
- Present options rather than dictating

### Be Skeptical
- Research user claims before accepting
- Cross-reference multiple sources
- Challenge assumptions with evidence

### Exit Conditions Are Blocking Gates

Exit conditions are **mandatory gates** that must pass before advancing to the next phase. They are not advisory - they are requirements.

**Three Verification Categories** (all must pass):

1. **Build Verification** - Code compiles and passes static analysis:
   - Build commands (`npm run build`, `cargo build`, `go build`)
   - Linting (`npm run lint`, `flake8`, `golangci-lint`)
   - Type checking (`npm run typecheck`, `mypy`, `tsc --noEmit`)

2. **Runtime Verification** - Application actually runs:
   - Start command executes without error
   - No runtime exceptions or crashes
   - Services/endpoints become accessible
   - Health checks pass

3. **Functional Verification** - Correct behavior:
   - Test suites pass (`npm test`, `pytest`, `go test`)
   - Specific feature tests pass
   - Manual verification steps (for human-observable behaviors)

**Never skip a category** - each phase must have at least one check in each category.

### No Unresolved Questions

**Do NOT write plans with open questions.**

If planning encounters ambiguity:
1. Stop and research further
2. Present options to the user
3. Get resolution before continuing

A plan with "TBD" or "to be determined" sections is incomplete.

## Quality Checklist

Before finalizing any plan:

- [ ] All relevant code has been read completely
- [ ] File:line references are accurate and specific
- [ ] Design fits existing codebase patterns
- [ ] Phases are incrementally implementable
- [ ] Each phase has a Verification Approach section
- [ ] Tasks list tests BEFORE implementation
- [ ] Exit conditions cover all three verification categories
- [ ] No unresolved questions or TBD sections
- [ ] User has approved structure and approach
- [ ] Tasks bootstrapped with dependencies set
- [ ] task_list_id added to plan metadata

## Progress Tracking

Progress is tracked via **Task tools** which persist across sessions. See [ADR-0001](../../docs/decisions/ADR-0001-separate-plan-spec-from-progress-tracking.md).

**Task Persistence:**
- Tasks persist on filesystem between sessions
- Dependencies ensure correct execution order
- Multiple sessions can share the same task list via `CLAUDE_CODE_TASK_LIST_ID`

**Workflow:**
```
create-plan → TaskCreate (all phases) → Outputs task_list_id
                    ↓
implement-plan → TaskUpdate(in_progress) → implement-phase → TaskUpdate(completed)
                    ↓
Resume (any session) → CLAUDE_CODE_TASK_LIST_ID=xxx claude → TaskList shows progress
```

## Project Type Detection

Before writing exit conditions, detect the project type and suggest appropriate commands.

### Detection Strategy

Look for these files to identify project type:

| File | Project Type | Build | Test | Start |
|------|-------------|-------|------|-------|
| `package.json` | Node.js/TypeScript | `npm run build` | `npm test` | `npm start` |
| `pyproject.toml` or `setup.py` | Python | `pip install -e .` | `pytest` | `python -m app` |
| `Cargo.toml` | Rust | `cargo build` | `cargo test` | `cargo run` |
| `go.mod` | Go | `go build ./...` | `go test ./...` | `go run .` |
| `pom.xml` | Java/Maven | `mvn compile` | `mvn test` | `mvn exec:java` |
| `build.gradle` | Java/Gradle | `./gradlew build` | `./gradlew test` | `./gradlew run` |
| `Makefile` | Generic | `make build` | `make test` | `make run` |

### Exit Condition Templates by Project Type

**Node.js/TypeScript:**
```markdown
Build Verification:
- [ ] `npm run build` succeeds
- [ ] `npm run lint` passes
- [ ] `npm run typecheck` passes

Runtime Verification:
- [ ] `npm run start` or `npm run dev` starts without errors
- [ ] Server responds on expected port

Functional Verification:
- [ ] `npm test` passes
- [ ] `npm run test:e2e` passes (if applicable)
```

**Python:**
```markdown
Build Verification:
- [ ] `pip install -e .` succeeds
- [ ] `flake8` or `ruff` passes
- [ ] `mypy .` passes (if using type hints)

Runtime Verification:
- [ ] `python -m [module]` starts without errors
- [ ] Service responds on expected port

Functional Verification:
- [ ] `pytest` passes
- [ ] `pytest tests/integration` passes (if applicable)
```

**Go:**
```markdown
Build Verification:
- [ ] `go build ./...` succeeds
- [ ] `golangci-lint run` passes

Runtime Verification:
- [ ] `go run .` or compiled binary starts
- [ ] Health endpoint responds

Functional Verification:
- [ ] `go test ./...` passes
- [ ] `go test -race ./...` passes (race detection)
```

**Rust:**
```markdown
Build Verification:
- [ ] `cargo build` succeeds
- [ ] `cargo clippy` passes

Runtime Verification:
- [ ] `cargo run` starts without panics
- [ ] Service binds to expected port

Functional Verification:
- [ ] `cargo test` passes
- [ ] Integration tests pass
```

### Custom Exit Conditions

For each phase, also add **custom functional checks** specific to what that phase implements:

```markdown
Functional Verification:
- [ ] `npm test` passes
- [ ] Auth endpoint returns 200 on valid credentials
- [ ] Auth endpoint returns 401 on invalid credentials
- [ ] JWT token contains expected claims
```

These custom checks ensure the specific functionality of the phase works correctly, beyond just "tests pass."
