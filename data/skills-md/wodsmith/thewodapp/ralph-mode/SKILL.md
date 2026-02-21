---
name: ralph-mode
description: Autonomous AI coding loop that ships features while you sleep. Use when the user wants to run Ralph, start an autonomous coding session, work overnight, or let Claude implement multiple user stories autonomously. Triggers on "ralph", "autonomous mode", "overnight coding", "autonomous loop", or requests to implement multiple stories without supervision.
---

# Ralph Mode

Ralph is an autonomous AI coding loop that spawns fresh context windows repeatedly until all tasks are complete. Memory persists via git history and text files while each iteration starts fresh.

Named after Ralph Wiggum from The Simpsons - perpetually confused, always making mistakes, but never stopping. The philosophy: iteration beats perfection.

## Two Execution Modes

Ralph works in two environments:

| Mode | Environment | How It Works | Fresh Context Via |
|------|-------------|--------------|-------------------|
| **Local** | CLI terminal | Bash loop spawns `claude -p` | New CLI process |
| **Remote** | Web/API/Agent SDK | Controller spawns Task subagents | New Task call |

Both achieve the same goal: fresh context per iteration to avoid context rot.

## Quick Start

### Initialize Ralph

```bash
bun .claude/skills/ralph-mode/scripts/init-ralph.ts
```

This creates `scripts/ralph/` with all necessary files.

### Populate PRD

Edit `scripts/ralph/prd.json` with your user stories (see [prd-guide.md](references/prd-guide.md)).

### Run Ralph

**Local Mode (CLI):**
```bash
./scripts/ralph/ralph.sh 20      # AFK: 20 iterations max
./scripts/ralph/ralph-once.sh    # HITL: single iteration
```

**Remote Mode (Web/API):**
Load `scripts/ralph/ralph-controller.md` and follow its instructions. The controller will spawn Task subagents for each story.

## How It Works

### Local Mode (Bash Loop)

```
┌─────────────────────────────────────────┐
│  ralph.sh (bash loop)                   │
│  └─▶ claude -p < prompt.md              │
│       └─▶ Implements ONE story          │
│       └─▶ Commits if passing            │
│       └─▶ Updates state files           │
│  └─▶ Loop until done or max iterations  │
└─────────────────────────────────────────┘
```

### Remote Mode (Task-Based)

```
┌─────────────────────────────────────────┐
│  Ralph Controller (you or outer agent)  │
│  └─▶ Reads prd.json, progress.txt       │
│  └─▶ Selects next story                 │
│  └─▶ Task(general-purpose) ────────────────┐
│       │                                    │
│       ▼                                    │
│  ┌─────────────────────────────────────┐   │
│  │  Ralph Worker (subagent)            │   │
│  │  - Fresh context window             │   │
│  │  - Implements ONE story             │   │
│  │  - Runs feedback loops              │   │
│  │  - Commits if passing               │   │
│  │  - Updates state files              │   │
│  └─────────────────────────────────────┘   │
│       │                                    │
│       ◀────────────────────────────────────┘
│  └─▶ Verifies result                    │
│  └─▶ Loop until done or max iterations  │
└─────────────────────────────────────────┘
```

**Key insight**: Each `Task()` call creates a fresh context window - exactly what Ralph needs.

## File Structure

```
scripts/ralph/
├── ralph.sh            # Local: AFK mode loop
├── ralph-once.sh       # Local: HITL single iteration
├── ralph-controller.md # Remote: Controller instructions
├── ralph-worker.md     # Remote: Worker template
├── prompt.md           # Local: Iteration prompt
├── prd.json            # User stories with completion status
└── progress.txt        # Accumulated learnings
```

## Remote Mode: Enforced Subagent Use

In remote mode, the controller **MUST NOT** implement code directly:

```
❌ Controller writes code     → Context rot, defeats purpose
✅ Controller spawns workers  → Fresh context per story
```

The controller only:
1. Reads state files
2. Selects next story
3. Spawns Task subagents
4. Verifies results
5. Loops

All implementation happens in subagents with fresh context.

### Spawning a Worker

```javascript
Task({
  subagent_type: "general-purpose",
  description: "Implement US-003: Add email validation",
  prompt: `[contents of ralph-worker.md with story details filled in]`
})
```

### Worker Responsibilities

Each worker subagent:
1. Loads context (progress.txt, AGENTS.md)
2. Implements ONE story
3. Runs feedback loops (typecheck, lint, test)
4. Commits only if ALL pass
5. Updates prd.json and progress.txt
6. Reports results back to controller

## Memory Persistence

Ralph forgets everything between iterations. Memory persists ONLY through:

| File | Purpose |
|------|---------|
| `prd.json` | Task status (`passes` field) |
| `progress.txt` | Learnings, patterns, gotchas |
| Git commits | Implementation history |
| `AGENTS.md` | Permanent project patterns |

## The 11 Tips for Success

### 1. Ralph Is A Loop
The agent chooses tasks, not you. Define the end state. Ralph gets there.

### 2. Start With HITL, Then Go AFK
- **HITL**: Watch, intervene, refine prompts
- **AFK**: Bulk work once foundation is solid

### 3. Define The Scope
PRD items with explicit `passes` field and acceptance criteria.

### 4. Track Progress
`progress.txt` IS the memory. Codebase Patterns at the TOP.

### 5. Use Feedback Loops
Block commits unless typecheck/lint/test all pass.

### 6. Take Small Steps
One story per iteration. Context rot is real.

### 7. Prioritize Risky Tasks
Architecture → Integration → Features → Polish

### 8. Define Quality Expectations
Tell Ralph: prototype vs production vs library.

### 9. Use Sandboxes
Docker for local AFK. Isolated environments for remote.

### 10. Pay To Play
Even HITL Ralph beats manual multi-phase prompting.

### 11. Make It Your Own
Ralph is just a loop. Adapt for coverage, linting, refactoring, etc.

## Usage Examples

### Local HITL (Learning)
```bash
./scripts/ralph/ralph-once.sh
# Watch output, intervene if needed
# Run again when ready
```

### Local AFK (Overnight)
```bash
./scripts/ralph/ralph.sh 50  # Let it run
```

### Remote HITL (Web Session)
1. Read `ralph-controller.md`
2. Read `prd.json` and `progress.txt`
3. Select a story
4. Spawn ONE Task subagent with worker prompt
5. Verify result
6. Repeat manually

### Remote AFK (Agent-to-Agent)
An outer agent or Agent SDK program runs the controller loop, spawning subagents until all stories pass.

## Monitoring Progress

```bash
# Story status
cat scripts/ralph/prd.json | jq '.userStories[] | {id, title, passes}'

# Learnings
cat scripts/ralph/progress.txt

# Recent commits
git log --oneline -10
```

## Safety

- Local AFK uses `--dangerously-skip-permissions`
- Use Docker sandboxes when possible
- Always cap iterations
- Ctrl+C stops local loops immediately
- `git reset --hard` reverts uncommitted changes

## When NOT to Use

- Exploratory work without clear outcomes
- Major refactors without explicit criteria
- Security-critical code needing human review
- Early architectural decisions (use HITL)

## References

- [prd-guide.md](references/prd-guide.md) - Writing effective user stories
- [patterns.md](references/patterns.md) - Common patterns and gotchas
- [ralph-controller.md](scripts/ralph-controller.md) - Remote controller instructions
- [ralph-worker.md](scripts/ralph-worker.md) - Worker subagent template
