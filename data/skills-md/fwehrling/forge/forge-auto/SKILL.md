---
name: forge-auto
description: >
  FORGE Autopilot — Intelligent autonomous mode. FORGE analyzes the project state,
  automatically decides the next action, and orchestrates all agents
  until completion. Configurable checkpoints for human review.
  Usage: /forge-auto or /forge-auto "specific objective"
---

# /forge-auto — FORGE Autopilot Mode

FORGE takes full control of the development pipeline. It analyzes, decides,
executes, verifies, and iterates automatically until the objective is complete.

## French Language Rule

All content generated in French MUST use proper accents (é, è, ê, à, ù, ç, ô, î, etc.), follow French grammar rules (agreements, conjugations), and use correct spelling.

## Principle

```
The user provides an objective → FORGE handles EVERYTHING else.
Planning → Architecture → Stories → Code → Tests → Verification → Deployment
```

## Workflow

1. **Load memory**:
   - Read `.forge/memory/MEMORY.md` for project context
   - Read the latest session from `.forge/memory/sessions/` for continuity
   - Read `.forge/sprint-status.yaml` for the current state
   - Read `.forge/config.yml` for configuration
   - `forge-memory search "<current objective>" --limit 3`
     → Load relevant past decisions and context

2. **Analyze state and determine the phase**:

   The decision system follows this logic:

   ```
   IF no artifacts exist:
     → Start with /forge-plan (generates the PRD)

   IF PRD exists BUT no architecture:
     → Launch /forge-architect

   IF architecture exists BUT no UX design:
     → Launch /forge-ux

   IF UX exists BUT no stories:
     → Launch /forge-stories

   IF stories exist with "pending" status:
     → Count unblocked pending stories
     → IF 2+ unblocked stories AND Agent Teams available (CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1):
       → Delegate to /forge-team build [STORY-IDs] (parallel execution)
       → Wait for team completion, then continue with QA verdicts
     → ELSE:
       → Pick the next unblocked story
       → Launch /forge-build STORY-XXX (sequential)

   IF an "in_progress" story exists:
     → Resume /forge-build STORY-XXX

   IF story is implemented (Dev tests pass):
     → Launch /forge-verify STORY-XXX

   IF QA verdict = FAIL:
     → Increment failure counter for this story
     → IF failure counter < 3:
       → Fix and relaunch /forge-verify
     → IF failure counter >= 3:
       → Escalate to /forge-loop "Fix STORY-XXX: [QA failure summary]" --mode hitl
       → forge-loop iterates autonomously with sandbox guardrails until tests pass
       → On success: reset failure counter, continue with /forge-verify

   IF QA verdict = PASS:
     → Move to the next story

   IF all stories are "completed":
     → Propose /forge-deploy or new stories
   ```

3. **Execute with the appropriate agents**:
   - Each phase invokes the corresponding agent (PM, Architect, UX, SM, Dev, QA)
   - The agent loads its persona from `references/agents/`
   - The agent produces its artifacts in `docs/` or `src/`
   - **Agent Teams acceleration**: when entering the build phase with 2+ unblocked stories,
     and `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` is set, autopilot delegates to
     `/forge-team build` for parallel story implementation (up to 4 Dev + 1 QA).
     If Agent Teams is not available, stories are built sequentially as before.

4. **Automatic quality gates**:
   - After each story: lint + typecheck + tests > 80% coverage
   - After each /forge-verify: mandatory QA verdict
   - **Loop escalation**: if 3 consecutive failures on the same story, autopilot
     delegates to `/forge-loop` in HITL mode with the QA failure summary as task.
     forge-loop iterates with sandbox guardrails (cost cap, circuit breaker, rollback)
     until tests pass, then returns control to autopilot for re-verification.
   - Ultimate circuit breaker: if forge-loop also fails (hits its own circuit breaker)
     → pause + report to user

5. **Save memory**:
   - `forge-memory log` for each story completed during this session:
     ```bash
     forge-memory log "{STORY_ID} terminée : {N} tests, couverture {X}%" --agent dev --story {STORY_ID}
     ```
   - `forge-memory log` for the session summary:
     ```bash
     forge-memory log "Session autopilot terminée : {completed}/{total} stories, phase {PHASE}"
     ```
   - Consolidate session logs into MEMORY.md:
     ```bash
     forge-memory consolidate --verbose
     ```
   - Sync the full memory index:
     ```bash
     forge-memory sync
     ```
   - Update `.forge/sprint-status.yaml`

6. **Human checkpoints** (configurable):
   - Default: checkpoint after each major phase (plan, architecture, stories)
   - `--no-pause` mode: no checkpoints (full autopilot)
   - `--pause-stories` mode: pause after story decomposition
   - `--pause-each` mode: pause after each story

## Options

```bash
# Full autopilot — FORGE decides everything
/forge-auto

# Autopilot with a specific objective
/forge-auto "Implement the authentication system"

# Autopilot without pauses (warning: fully autonomous)
/forge-auto --no-pause

# Autopilot with pause after stories
/forge-auto --pause-stories

# Autopilot with pause after each story
/forge-auto --pause-each

# Resume autopilot after a pause
/forge-auto --resume
```

## Progress Report

At each step, FORGE displays:

```
FORGE AUTOPILOT — Progress
──────────────────────────────
Phase     : Development (Story 3/8)
Last      : STORY-002 ✓ (QA: PASS)
Current   : STORY-003 — Implementation
Next      : STORY-004 (pending)

Metrics:
  Stories   : 2 completed / 1 in_progress / 5 pending
  Tests     : 47 pass / 0 fail
  Coverage  : 87%

Memory    : .forge/memory/MEMORY.md (up to date)
Session   : .forge/memory/sessions/2025-01-15.md
```

## How /forge-auto Uses Other FORGE Tools

| Situation | Autopilot delegates to | Condition |
| --- | --- | --- |
| 2+ unblocked stories ready | `/forge-team build` (parallel) | Agent Teams enabled |
| 1 story ready | `/forge-build STORY-XXX` (sequential) | Always |
| 3 consecutive failures on a story | `/forge-loop` (iterative fix) | Always |
| forge-loop also fails | Pause + report to user | Ultimate circuit breaker |

## Difference with /forge-loop

| Aspect         | /forge-loop                     | /forge-auto                             |
| -------------- | ------------------------------- | --------------------------------------- |
| **Scope**      | A specific task                 | The entire project                      |
| **Decision**   | The user chooses the task       | FORGE decides the next action           |
| **Agents**     | A single one (usually Dev)     | All agents depending on the phase       |
| **Memory**     | Local fix_plan.md              | Persistent project memory               |
| **Progression**| Linear (iterations)            | Full pipeline (plan → deploy)           |
| **Use case**   | "Implement this feature"       | "Build this project from A to Z"        |
| **Relation**   | Standalone or called by auto   | Calls /forge-loop on difficult stories  |

## Coexistence with Manual Mode

Autopilot and manual commands are 100% compatible:

- You can start with `/forge-auto`, pause, then continue manually
- You can work manually then launch `/forge-auto --resume` to continue
- Memory is shared: both modes read/write the same files
- `/forge-status` works in both modes

## Notes

- Autopilot ALWAYS respects quality gates (no shortcuts)
- The circuit breaker protects against infinite loops
- Persistent memory ensures continuity between sessions
- Compatible with projects initialized via `/forge-init`
- Also works for resuming existing projects (analyzes the state)
