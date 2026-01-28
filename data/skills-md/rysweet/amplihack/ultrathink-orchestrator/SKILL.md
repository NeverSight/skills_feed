---
name: ultrathink-orchestrator
version: 1.0.0
description: Auto-invokes ultrathink workflow for any work request (default orchestrator)
auto_activate: true
priority: 5
triggers:
  - "implement"
  - "create"
  - "build"
  - "add"
  - "fix"
  - "update"
  - "refactor"
  - "design"
---

# Ultrathink Orchestrator Skill

## Purpose

This skill provides automatic orchestration for development and investigation tasks. It detects the task type from keywords and delegates to the appropriate workflow skill (investigation-workflow or default-workflow).

Auto-activation priority is LOW (5) to allow more specific skills to match first. When activated, this orchestrator selects between investigation-workflow and default-workflow based on the user's request keywords.

This skill acts as a thin wrapper around the canonical ultrathink command, following the amplihack pattern of single-source-of-truth for command logic.

## Canonical Sources

**This skill is a thin wrapper that references canonical sources:**

- **Primary Command**: `~/.amplihack/.claude/commands/amplihack/ultrathink.md` (278 lines)
- **Workflow Sources**:
  - Development: `~/.amplihack/.claude/workflow/DEFAULT_WORKFLOW.md`
  - Investigation: `~/.amplihack/.claude/workflow/INVESTIGATION_WORKFLOW.md`

The canonical command contains complete task detection logic, complexity estimation, and orchestration patterns for both investigation and development workflows.

## ⛔ MANDATORY EXECUTION PROCESS (5 Steps)

When this skill is activated, you MUST follow this exact 5-step process:

### Step 1: Read Canonical Command (MANDATORY)

```
Read(file_path="~/.amplihack/.claude/commands/amplihack/ultrathink.md")
```

**Validation Checkpoint**: Confirm ultrathink.md content is loaded before proceeding.

### Step 2: Detect Task Type (MANDATORY)

Analyze user request using keywords from canonical command:

- **Q&A keywords**: what is, explain briefly, quick question, how do I run, simple question
- **Investigation keywords**: investigate, explain, understand, analyze, research, explore
- **Development keywords**: implement, build, create, add feature, fix, refactor, deploy
- **Hybrid tasks**: Both investigation and development keywords present

**Validation Checkpoint**: Task type must be determined (Q&A, Investigation, Development, or Hybrid).

### Step 3: Invoke Workflow Skill (MANDATORY - BLOCKING)

⛔ **THIS IS A BLOCKING REQUIREMENT** - Session will be terminated if skipped.

**For Q&A tasks:**

```
Read(file_path="~/.amplihack/.claude/workflow/Q&A_WORKFLOW.md")
```

**For Investigation tasks:**

```
Skill(skill="investigation-workflow")
```

**For Development tasks:**

```
Skill(skill="default-workflow")
```

**For Hybrid tasks:**

```
Skill(skill="investigation-workflow")
# After investigation completes:
Skill(skill="default-workflow")
```

**Validation Checkpoint**: Confirm Skill tool was invoked OR proceed to Step 4.

### Step 4: Fallback to Read Tool (IF Step 3 Fails)

Only if skill invocation fails, use Read tool as fallback:

**Investigation fallback:**

```
Read(file_path="~/.amplihack/.claude/workflow/INVESTIGATION_WORKFLOW.md")
```

**Development fallback:**

```
Read(file_path="~/.amplihack/.claude/workflow/DEFAULT_WORKFLOW.md")
```

**Validation Checkpoint**: Confirm workflow content is loaded in context.

### Step 5: Execute Workflow Steps (MANDATORY)

Follow all steps from loaded workflow without skipping.

**Validation Checkpoint**: All workflow steps must be completed.

---

## Enforcement

**Power-Steering Detection:**

- Validates Skill tool invocation occurred
- Validates Read tool fallback if Skill failed
- Blocks session termination if workflow not loaded

**Self-Check Protocol:**
Before proceeding past Step 3, verify:

- [ ] Skill tool invoked with workflow skill name, OR
- [ ] Read tool used to load workflow markdown
- [ ] Workflow content confirmed in context

**No Shortcuts:**

- You cannot skip workflow invocation
- You cannot assume workflow content
- You must use Skill or Read tool explicitly

## Why This Pattern

**Benefits:**

- Single source of truth for orchestration logic in canonical command
- No content duplication between command and skill
- Task detection rules defined once, maintained once
- Changes to ultrathink command automatically inherited by skill

**Trade-offs:**

- Requires Read tool call to fetch canonical logic
- Slight indirection vs. inline implementation

This pattern aligns with amplihack philosophy: ruthless simplicity through elimination of duplication.

## Related Files

- **Canonical Command**: `~/.amplihack/.claude/commands/amplihack/ultrathink.md`
- **Development Workflow Skill**: `~/.amplihack/.claude/skills/default-workflow/`
- **Investigation Workflow Skill**: `~/.amplihack/.claude/skills/investigation-workflow/`
- **Canonical Workflows**:
  - `~/.amplihack/.claude/workflow/DEFAULT_WORKFLOW.md`
  - `~/.amplihack/.claude/workflow/INVESTIGATION_WORKFLOW.md`
