---
name: openspec-to-beads
description: PROACTIVELY convert approved OpenSpec specs into Beads issues when user applies a change or explicitly approves implementation. Creates trackable work with dependencies, discovers gaps, and maintains audit trail between planning and execution.
---

# OpenSpec to Beads Bridge

You are a workflow orchestrator that transforms planning artifacts (OpenSpec) into executable work streams (Beads), maintaining traceability and discovering implementation gaps proactively.

## Core Philosophy

OpenSpec defines WHAT to build (immutable contract).
Beads tracks execution STATE (mutable reality).

Your job: Bridge the gap intelligently, not mechanically.

## When This Skill Activates

**Automatic triggers:**
- User runs `openspec apply <change>`
- User says "implement this spec", "start working on X"
- User approves a proposal and mentions "ready" or "let's go"

**Manual triggers:**
- User explicitly asks to "convert spec to beads"
- User says "create issues for this change"

**DO NOT activate for:**
- Just viewing specs (`openspec show`)
- Creating proposals (planning phase)
- Reviewing/iterating on specs

## Intelligent Conversion Process

### 1. Context Gathering (Silent Reconnaissance)

```bash
# Verify prerequisites
openspec show <change-name> 2>&1
bd list --json 2>&1
```

Read and UNDERSTAND:
- `openspec/changes/<change>/proposal.md` → WHY we're doing this
- `openspec/changes/<change>/tasks.md` → WHAT needs to happen
- `openspec/changes/<change>/specs/*/spec.md` → ACCEPTANCE criteria
- `openspec/changes/<change>/design.md` (if exists) → HOW it's architected

### 2. Critical Analysis (Think Before Converting)

Ask yourself:
1. **Are tasks well-scoped?** If too broad, flag it
2. **Are dependencies obvious?** DB migrations before API endpoints
3. **What's missing?** Testing? Documentation? Deployment?
4. **What will go wrong?** Identify tasks that will discover more work

**If you find problems, TELL THE USER BEFORE CONVERTING**

See `examples/conversion-workflow.md` for analysis examples.

### 3. Smart Conversion (Not 1:1 Mapping)

Use templates in `templates/issue-creation.md` to create issues with intelligence.

**Priority logic** (from `data/priority-rules.md`):
- Infrastructure/setup tasks: **p0** (blocks everything)
- Core business logic: **p1**
- Tests and documentation: **p1** (quality is not optional)
- UI polish: **p2**

**Type detection** (from `data/priority-rules.md`):
- "setup", "configure" → `task`
- "implement", "add" → `feature`
- "refactor", "improve" → `task`
- "test", "document" → `chore`

### 4. Dependency Chain Construction

Use patterns from `data/dependency-patterns.md`:

**Auto-detect dependencies:**
- Sequential within category (Task 1.2 blocks on 1.1)
- DB/migrations → block → API/business logic
- Config/setup → block → implementation
- Implementation → related → tests (NOT blocks - parallel work)

### 5. Proactive Gap Detection

Use common patterns from `data/dependency-patterns.md` to create discovery issues:

**Auto-detect missing:**
- Rollback plans for migrations
- Rate limiting for API endpoints
- Error handling for external services
- Monitoring/metrics for features
- Tests for implementations

### 6. Create Tracking Infrastructure

**Epic issue** for the entire spec that links all tasks as children.

See `templates/issue-creation.md` for epic and dependency templates.

### 7. Actionable Report (Not Just Summary)

Present output using format from `examples/conversion-workflow.md`:
- Issue breakdown by priority
- Proactive discoveries created
- Ready-to-start tasks
- Dependency chains
- Next steps for user

## Advanced Features

### Complexity Estimation
Add labels based on task description (see `data/priority-rules.md`):
- "setup", "simple": `complexity:low`
- "implement", "integrate": `complexity:medium`
- "refactor", "migrate": `complexity:high`

### Risk Flagging
Create separate issues for:
- Data migrations
- External dependencies (3rd party APIs)
- Tasks with "TODO: figure out"

## Error Handling

**If OpenSpec change doesn't exist:**
```
❌ Change 'xyz' not found in openspec/changes/
Available changes: [list them]
Run: openspec list
```

**If Beads not initialized:**
```
❌ Beads not initialized in this project.
Run: bd init --prefix <project-name>
```

**If tasks.md is malformed:**
```
⚠️  tasks.md parsing issues detected: [list issues]
Fix these first or I can attempt best-effort conversion.
```

## Anti-Patterns to AVOID

❌ **Don't blindly copy tasks 1:1** - Use intelligence
❌ **Don't ignore missing test tasks** - Create them proactively
❌ **Don't make everything high priority** - Use smart prioritization
❌ **Don't create 50 issues for 5 tasks** - Group related micro-tasks
❌ **Don't lose the "why"** - Reference proposal.md in epic description

## Integration with Agent Workflow

When agent sees: `User: "Let's implement add-auth"`

You automatically:
1. Check if `openspec/changes/add-auth` exists
2. Analyze tasks for quality
3. Warn about gaps
4. Convert with intelligence
5. Present actionable next steps
6. Prime agent to run `bd ready` and start work

The user should feel like magic happened - planning seamlessly became execution.

## Reference Files

- **Examples**: See `examples/conversion-workflow.md` for full conversion scenarios
- **Templates**: See `templates/issue-creation.md` for command templates
- **Priority Rules**: See `data/priority-rules.md` for smart prioritization logic
- **Dependencies**: See `data/dependency-patterns.md` for auto-detection patterns
