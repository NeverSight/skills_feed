---
name: workflow-orchestrator
description: Automatically coordinates multi-skill workflows and triggers follow-up actions. Use when completing PRD creation, implementation, or any milestone that should trigger additional skills. This skill reads the auto-trigger configuration and executes the workflow chain.
allowed-tools: Read, Write, Edit, Bash, Grep, AskUserQuestion
metadata:
  hooks:
    after_complete:
      - trigger: session-logger
        mode: auto
        reason: "Save workflow execution context"
---

# Workflow Orchestrator

A skill that automatically coordinates workflows across multiple skills, triggering follow-up actions at appropriate milestones.

## When This Skill Activates

This skill should be triggered automatically when:
- A skill completes its main workflow
- A milestone is reached (PRD complete, implementation done, etc.)
- User says "complete workflow" or "finish the process"

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                    Workflow Orchestration                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Detect Milestone → 2. Read Hooks → 3. Execute Chain    │
│                                                             │
│  prd-planner complete                                       │
│       ↓                                                     │
│  workflow-orchestrator                                      │
│       ↓                                                     │
│  ┌─────────────────────────────────────┐                   │
│  │ auto-trigger self-improving-agent   │ (background)       │
│  │ auto-trigger session-logger         │ (auto)            │
│  └─────────────────────────────────────┘                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Trigger Configuration

Read trigger definitions from `skills/auto-trigger/SKILL.md`:

```yaml
hooks:
  after_complete:
    - trigger: self-improving-agent
      mode: background
    - trigger: session-logger
      mode: auto
  on_error:
    - trigger: self-improving-agent
      mode: background
```

## Execution Modes

| Mode | Behavior | Use When |
|------|----------|----------|
| `auto` | Execute immediately, no confirmation | Logging, status updates |
| `background` | Execute without blocking | Reflection, analysis |
| `ask_first` | Ask user before executing | PRs, deployments, major changes |

## Milestone Detection

### PRD Complete

```markdown
Detected when:
- docs/{scope}-prd.md exists
- All phases in {scope}-prd-task-plan.md are checked
- Status shows "COMPLETE"

Actions:
1. Trigger self-improving-agent (background)
2. Trigger session-logger (auto)
```

### Implementation Complete

```markdown
Detected when:
- All PRD requirements implemented
- Tests pass
- Code committed

Actions:
1. Trigger code-reviewer (ask_first)
2. Trigger create-pr if changes staged
3. Trigger session-logger (auto)
```

### Self-Improvement Complete

```markdown
Detected when:
- Reflection complete
- Patterns abstracted
- Skill files modified

Actions:
1. Trigger create-pr (ask_first)
2. Trigger session-logger (auto)
```

### Universal Learning (Any Skill Complete)

```markdown
Detected when:
- ANY skill completes its workflow
- User provides feedback
- Error or issue encountered

Actions:
1. Trigger self-improving-agent (background)
2. Trigger session-logger (auto)

The self-improving-agent:
- Extracts experience from completed skill
- Identifies patterns and insights
- Updates related skills with learned patterns
- Consolidates memory for future reference
```

## Error Handling (on_error)

Detected when:
- A command returns non-zero exit code
- Tests fail after following skill guidance
- User reports the guidance produced incorrect results

Actions:
1. Trigger self-improving-agent (background) for self-correction
2. Trigger session-logger (auto) to capture error context

## Hook Implementation in Skills

To enable auto-trigger, add this section to any skill's SKILL.md:

```markdown
## Auto-Trigger (After Completion)

When this skill completes, automatically trigger:

```yaml
hooks:
  after_complete:
    - trigger: skill-name
      mode: auto|background|ask_first
      context: "relevant context"
  on_error:
    - trigger: self-improving-agent
      mode: background
```

### Current Skill Hooks

- **prd-planner**: After PRD complete → self-improving-agent + session-logger
- **self-improving-agent**: After improvement → create-pr + session-logger
- **prd-implementation-precheck**: After implementation → self-improving-agent + session-logger
- **code-reviewer**: After review → self-improving-agent + session-logger
- **debugger**: After debugging → self-improving-agent + session-logger
- **create-pr**: After PR created → session-logger
- **session-logger**: No trigger (terminates chain)

### Universal Learning Pattern

```
┌─────────────────────────────────────────────────────────────┐
│                  ANY Skill Completes                        │
└──────────────┬──────────────────────────────────────────────┘
               │
               ↓
    ┌──────────────────────┐
    │ workflow-orchestrator │
    └──────────┬───────────┘
               │
    ┌──────────┴─────────┐
    ↓                   ↓
self-improving-agent  session-logger
    ↓                   ↓
Learn from experience  Save context
    ↓                   ↓
Update skills         Log session
    ↓
create-pr (if modified)
```
```

## Workflow Examples

### Example 1: PRD Creation Workflow

```
User: "Create a PRD for user authentication"
        ↓
prd-planner executes
        ↓
Phase 6 complete: PRD delivered
        ↓
workflow-orchestrator detects milestone
        ↓
┌─────────────────────────────────┐
│ Background: self-improving-agent │ → Learns from PRD patterns
│ Auto: session-logger             │ → Saves session
└─────────────────────────────────┘
```

### Example 2: Full Feature Workflow

```
User: "Create a PRD and implement it"
        ↓
prd-planner → workflow-orchestrator
        ↓
self-improving-agent → workflow-orchestrator
        ↓
prd-implementation-precheck
        ↓
implementation complete → workflow-orchestrator
        ↓
code-reviewer → self-improving-agent → workflow-orchestrator
        ↓
create-pr → workflow-orchestrator
        ↓
session-logger
```

Each step triggers `self-improving-agent` to learn from the experience.

## Implementation Steps

### Step 1: Detect Milestone

Check for completion indicators:

```bash
# PRD complete?
grep -q "COMPLETE" docs/{scope}-prd-task-plan.md

# All phases checked?
grep -q "^\- \[x\].*Phase 6" docs/{scope}-prd-task-plan.md

# PRD file exists?
ls docs/{scope}-prd.md
```

### Step 2: Read Trigger Config

```bash
# Read hooks from auto-trigger skill
cat skills/auto-trigger/SKILL.md
```

### Step 3: Execute Hooks

For each hook in order (before_start, after_complete, on_error):
1. Check if condition is met
2. Execute based on mode
3. Pass context to triggered skill
4. Wait/continue based on mode

### Step 4: Update Status

Log what was triggered and the result:

```markdown
## Workflow Execution

- [x] self-improving-agent (background) - Started
- [x] session-logger (auto) - Session saved
- [ ] create-pr (ask_first) - Pending user approval
```

## Skills with Auto-Trigger

| Skill | Triggers After |
|-------|----------------|
| `prd-planner` | self-improving-agent, session-logger |
| `self-improving-agent` | create-pr, session-logger |
| `prd-implementation-precheck` | code-reviewer, session-logger |
| `code-reviewer` | self-improving-agent, session-logger |
| `create-pr` | session-logger |
| `refactoring-specialist` | self-improving-agent, session-logger |
| `debugger` | self-improving-agent, session-logger |

## Adding Auto-Trigger to Existing Skills

To add auto-trigger capability to an existing skill, add to the end of its SKILL.md:

```markdown
---

## Auto-Trigger

When this skill completes, automatically trigger:

```yaml
hooks:
  after_complete:
    - trigger: session-logger
      mode: auto
      context: "Save session context"
```
```

For more complex triggers, specify mode and context:

```markdown
## Auto-Trigger

When this skill completes:

```yaml
hooks:
  after_complete:
    - trigger: next-skill
      mode: background
      context: "Description"
    - trigger: session-logger
      mode: auto
      context: "Save session"
    - trigger: create-pr
      mode: ask_first
      context: "Create PR if files modified"
  on_error:
    - trigger: self-improving-agent
      mode: background
```
```

## Best Practices

1. **Always log to session** - Every workflow should end with session-logger
2. **Ask before major actions** - PRs, deployments, destructive changes
3. **Background for analysis** - Reflection, evaluation, optimization
4. **Auto for status** - Logging, status updates, bookmarks
5. **Don't create loops** - Ensure chains terminate
