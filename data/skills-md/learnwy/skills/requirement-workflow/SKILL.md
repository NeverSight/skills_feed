---
name: "requirement-workflow"
description: "State-machine driven orchestrator for structured software development. Supports skill/agent injection at each stage. Triggers: 'build a feature', 'fix this bug', 'implement', 'develop', 'refactor'."
---

# Requirement Workflow Orchestrator

State-machine driven development workflow with **agent/skill injection** support.

## When to Use

**Invoke when:**
- Feature development: "build a user authentication system"
- Bug fixes: "fix the login issue"
- Refactoring: "refactor this module"
- Keywords: `feature`, `bugfix`, `refactor`, `implement`, `develop`

**Do NOT invoke when:**
- Simple Q&A or code explanations
- Single-line changes
- User declines: "just fix it, no workflow"

## ⚠️ CRITICAL: Execution Rules

**AI MUST follow these steps IN ORDER. Skipping steps is NOT allowed.**

```
┌──────────────────────────────────────────────────────────────────┐
│ 1. MUST run init-workflow.sh to create workflow                  │
│ 2. MUST run advance-stage.sh to transition each stage            │
│ 3. MUST create stage document BEFORE advancing to next stage     │
│ 4. MUST launch injected agents at indicated timing               │
└──────────────────────────────────────────────────────────────────┘
```

## Execution Steps

### Step 1: Analyze & Select Level

**Output to user:**
```
📊 Requirement Analysis:
- Type: feature | bugfix | refactor | hotfix
- Level: L1 | L2 | L3
- Scope: {affected files/modules}
- Reason: {why this level}
```

| Level | Condition | Doc Depth |
|-------|-----------|-----------|
| **L1** | Clear scope, ≤3 files, quick fix | Brief PRD + simple design |
| **L2** | Standard feature, 4-15 files | Full PRD + detailed design |
| **L3** | Security/cross-module/breaking | Comprehensive + compliance |

### Step 2: Initialize Workflow (REQUIRED)

**MUST run this command:**
```bash
./scripts/init-workflow.sh -r <project_root> -n <name> -t <type> -l <level>
```

**Example:**
```bash
./scripts/init-workflow.sh -r /project -n "user-auth" -t feature -l L2
```

### Step 3: Execute Stage Loop (REQUIRED)

**For EACH stage, follow this pattern:**

```
┌─────────────────────────────────────────────────────────────────┐
│ A. Run: ./scripts/advance-stage.sh -r <project_root>            │
│                                                                 │
│ B. Check output for injected agents/skills                      │
│                                                                 │
│ C. Launch pre_stage agents (if any)                             │
│                                                                 │
│ D. Complete stage work and CREATE DOCUMENT:                     │
│    - ANALYZING → Create spec.md                                 │
│    - PLANNING  → Create tasks.md                                │
│    - DESIGNING → Create design.md                               │
│    - TESTING   → Create checklist.md                            │
│    - DELIVERING → Create report.md                              │
│                                                                 │
│ E. Launch post_stage agents (if any)                            │
│                                                                 │
│ F. Repeat until status = DONE                                   │
└─────────────────────────────────────────────────────────────────┘
```

### Stage Document Requirements

| Stage | Document | L1 Depth | L2 Depth | L3 Depth |
|-------|----------|----------|----------|----------|
| ANALYZING | `spec.md` | 1-2 paragraphs | Standard PRD | Comprehensive |
| PLANNING | `tasks.md` | 3-5 tasks | 5-15 tasks | Full breakdown |
| DESIGNING | `design.md` | Key decisions | Full design | + security |
| IMPLEMENTING | Code | Quality code | Quality code | + security |
| TESTING | `checklist.md` | Basic tests | Full coverage | + security tests |
| DELIVERING | `report.md` | Brief summary | Full report | Compliance report |

### Example Execution

```
User: "Add user authentication feature"

AI: 
📊 Requirement Analysis:
- Type: feature
- Level: L2
- Scope: ~8 files (auth module, API, frontend)
- Reason: Standard feature, multiple modules

Initializing workflow...

$ ./scripts/init-workflow.sh -r /project -n "user-auth" -t feature -l L2
✅ Created: .trae/workflow/20240115_001_feature_user-auth/

$ ./scripts/advance-stage.sh -r /project
✅ Successfully transitioned to ANALYZING
🤖 Injected Agents:
  � Before stage: risk-auditor

[Launching risk-auditor agent...]

Now creating spec.md...

� spec.md created with:
- Background
- Objectives
- Scope
- Acceptance Criteria

$ ./scripts/advance-stage.sh -r /project
✅ Successfully transitioned to PLANNING

Now creating tasks.md...
...
```

## Scripts

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `init-workflow.sh` | Initialize workflow | Step 2 (once) |
| `advance-stage.sh` | Advance stage | Step 3 (each stage) |
| `get-status.sh` | Check status | Anytime |
| `inject-agent.sh` | Manage agents | Setup |
| `inject-skill.sh` | Manage skills | Setup |
| `generate-report.sh` | Generate report | DELIVERING stage |

## References

- [Agents](agents/AGENTS.md) - Available agents
- [L1 Workflow](references/WORKFLOW_L1.md) - Quick workflow details
- [L2 Workflow](references/WORKFLOW_L2.md) - Standard workflow details
- [L3 Workflow](references/WORKFLOW_L3.md) - Complex workflow details
- [Injection Guide](references/INJECTION_GUIDE.md) - Agent/Skill injection
- [Usage Examples](examples/USAGE.md) - More examples
