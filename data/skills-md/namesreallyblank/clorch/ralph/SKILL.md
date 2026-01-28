---
name: ralph
description: Setup Ralph autonomous coding loop (external fresh-context pattern)
impact: HIGH
triggers:
  - "ralph"
  - "autonomous"
  - "afk mode"
  - "fresh context"
  - "loop coding"
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - AskUserQuestion
  - TaskCreate
  - TaskUpdate
  - TaskList
  - TaskGet
metadata:
  tags: ralph, autonomous, loop, fresh-context, afk, tasks
  author: Geoffrey Huntley (pattern), Clorch (integration)
  references:
    - https://ghuntley.com/ralph/
    - https://ghuntley.com/loop/
    - https://x.com/trq212/status/2014480496013803643
---

# Ralph - Autonomous Loop Setup

Ralph is an external bash loop that runs Claude with fresh context for each task.
Named after Ralph Wiggum from The Simpsons.

## Core Principle

> "One bash loop. Static prompt. Clean task list. Fresh start every iteration."

The loop MUST be **external** to Claude. Each iteration MUST be a **fresh Claude process**.

## Claude Code Tasks Integration (NEW)

Ralph now integrates with Claude Code's native Tasks feature:
- **`CLAUDE_CODE_TASK_LIST_ID`** - Shared across iterations for coordination
- **Task tools enabled** - TaskCreate, TaskUpdate, TaskList, TaskGet
- **Hybrid approach** - Uses both `.ralph/task.md` (validation) and native Tasks (coordination)

See `TASKS.md` for full documentation.

## Workspace Isolation

Ralph is **project-specific**. Each project has its own `.ralph/` directory:

```
my-project/
└── .ralph/                    ← Project-specific Ralph workspace
    ├── analysis-meta.json     ← Cache metadata
    ├── project-context.md     ← Cached analysis
    ├── guardrails.md          ← Accumulated (persists across runs)
    ├── history/               ← Past runs archived
    └── task.md                ← Current tasks
```

- Guardrails accumulate per-project
- Analysis cached per-project
- Memory learnings tagged with project ID
- No cross-project contamination

See `WORKSPACE.md` for full isolation protocol.

## Commands

| Command | Description |
|---------|-------------|
| `/ralph "goal"` | Setup Ralph session (auto-detects brownfield) |
| `/ralph "goal" --docker` | Setup with Docker execution (API key required) |
| `/ralph "goal" --parallel N` | Setup with N parallel workers (requires Docker) |
| `/ralph status` | Check current progress (tasks complete/pending) |
| `/ralph summary` | Process completed run, store learnings |
| `/ralph start` | Auto-start Ralph loop in new terminal |
| `/ralph validate` | Validate Ralph's work (visual + tests) |

---

## Brownfield Mode (Existing Codebases)

Ralph automatically detects existing projects and adapts:

### Auto-Detection

If any of these exist, brownfield mode activates:
- `package.json`, `go.mod`, `pyproject.toml`, `Cargo.toml`
- `src/`, `lib/`, `app/` directories

### Brownfield Workflow

1. **Analyze codebase** - Detect stack, test framework, patterns
2. **Generate context-aware prompt.md** - Include project specifics
3. **Create smart validations** - Use actual test commands
4. **Seed guardrails** - From project patterns + memory

### Brownfield prompt.md Template

The prompt.md includes project context:
```markdown
## Project Context

**Stack:** {detected framework} + {database}
**Package Manager:** {npm|pnpm|yarn|bun}

**Commands:**
- Test: `{actual test command}`
- Lint: `{actual lint command}`
- Build: `{actual build command}`

**Key Directories:**
- `src/` - Source code
- `tests/` - Test files
- `prisma/` - Database schema
```

### Brownfield Task Patterns

**Bug Fix:**
```markdown
### Investigate {issue}
- description: Find root cause in {suspected_area}
- validation: `test -f .ralph/investigation.md`
- passes: false

### Fix {issue}
- description: Implement fix based on investigation
- validation: `{test_cmd} -- --grep "{related}"`
- passes: false
```

**Feature Addition:**
```markdown
### Explore Related Code
- description: Understand existing patterns
- validation: `test -f .ralph/exploration.md`
- passes: false

### Implement {feature}
- description: Add feature following project patterns
- validation: `{test_cmd} && {build_cmd}`
- passes: false
```

See BROWNFIELD.md for full documentation.

---

## Clorch → Ralph Handoff

**Key Insight:** Clorch does deep analysis, Ralph executes with fresh context.

```
┌─────────────────────────────────────────────────────────────┐
│  CLORCH (This Session)                                      │
│                                                             │
│  1. Analyze codebase (tldr, scout, grep)                   │
│  2. Recall memory (past learnings)                          │
│  3. Generate project-context.md                             │
│  4. Create smart tasks with file paths                      │
│  5. Seed guardrails from patterns                           │
│                                                             │
│  OUTPUT: .ralph/ directory ready                            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  RALPH LOOP (External, fresh per iteration)                 │
│                                                             │
│  - Reads pre-analyzed context                               │
│  - Executes one task                                        │
│  - Has full project understanding without analysis cost     │
└─────────────────────────────────────────────────────────────┘
```

**Why this works:**
- Clorch has agents, memory, AST tools → deep analysis
- Ralph has fresh context → no pollution
- Analysis done once → all iterations benefit

See `HANDOFF.md` for full protocol.

---

## Setup Workflow (`/ralph "goal"`)

### 0. Detect & Analyze (Brownfield - Incremental)

If existing project detected, Clorch analyzes with caching:

**Check for existing analysis:**
```bash
if [ -f ".ralph/analysis-meta.json" ]; then
  # Incremental: reuse base, update changed files
  LAST_SCAN=$(jq -r '.fileIndex.lastScan' .ralph/analysis-meta.json)
  CHANGED=$(git diff --name-only --since="$LAST_SCAN" HEAD)
else
  # Full analysis needed
fi
```

**Full Analysis (first time or stale):**
```bash
tldr tree . --ext .ts,.tsx,.js,.py,.go
tldr structure src/ --lang typescript
```

**Incremental Update (subsequent runs):**
```bash
# Only re-analyze changed files
git diff --name-only --since="$LAST_SCAN" HEAD | while read file; do
  tldr extract "$file"
done
```

**Goal-Specific Exploration (always fresh):**
```
Task(subagent_type="scout", prompt="
  Find code related to: {goal}
  Return: file paths, key functions, patterns
")
```

**Memory Recall:**
```bash
cd $CLAUDE_PROJECT_DIR/opc && PYTHONPATH=. uv run python scripts/core/recall_learnings.py \
  --query "{project} {goal}" --k 5
```

**Output:**
- `.ralph/project-context.md` - Base analysis (cached/updated)
- `.ralph/goal-context.md` - Goal-specific (fresh)
- `.ralph/analysis-meta.json` - Timestamps and hashes

See `INCREMENTAL.md` for full caching protocol.

### 1. Decompose the Goal

Break the goal into atomic, validatable tasks:

```markdown
### Task Name
- description: What to implement
- validation: `command that returns 0 on success`
- passes: false
```

**Requirements:**
- Each task must be independently completable
- Each task needs a validation command
- Order by dependency (foundation first)
- 15-25 tasks is typical for a feature

### 2. Create .ralph/ Directory

```bash
mkdir -p .ralph
```

### 3. Write prompt.md (Static - NEVER Changes)

```markdown
# Ralph Agent

You are a fresh Ralph agent. Your context is clean.

## Instructions

1. Read `.ralph/guardrails.md` FIRST - these are learned constraints
2. Read `.ralph/task.md` to find your current task
3. Find the FIRST task where `passes: false`
4. Implement ONLY that task
5. Run the validation command for that task
6. If validation passes: change `passes: false` to `passes: true`
7. If validation fails: append a guardrail to `.ralph/guardrails.md`
8. Commit your work with a clear message
9. Exit

## Code Quality

Write **modular, maintainable code**:

### File Size
- Keep files 150-500 lines (optimal for review and AI tools)
- Split files over 500 lines into focused modules
- Extract shared utilities to dedicated files

### Organization
- One module = one responsibility
- Group related functions together
- Separate pure logic from I/O operations
- Use meaningful names (`data_storage.py` not `utils2.py`)

### Structure
```
feature/
├── core.py       # Main logic
├── models.py     # Data structures
├── handlers.py   # I/O and side effects
└── utils.py      # Pure helper functions
```

### Don't
- Create god files (1000+ lines)
- Duplicate code across files
- Mix concerns in one function
- Over-engineer for hypothetical futures

### Match Project Style
- Follow existing patterns in the codebase
- Use the same naming conventions
- Match the existing directory structure
- Respect established abstractions

## Rules

- Do ONE task only
- Do NOT modify this prompt file
- Do NOT modify task descriptions, only the passes flag
- Commit your work with a clear message
- Trust the files, not your memory (you have none)
- Write modular code that future iterations can build on
```

### 4. Write task.md

```markdown
# Task: {Goal Description}

Created: {date}
Max Iterations: 50

## Tasks

{decomposed tasks with passes: false}
```

### Task Format with Benchmarks

Tasks can optionally include benchmark criteria:

```markdown
### API Authentication
- description: Implement JWT auth for /api routes
- validation: `npm test -- --grep "auth"`
- benchmark:
    - latency: < 100ms
    - memory: < 50MB
    - command: `npm run benchmark:auth`
- passes: false
```

**Benchmark fields:**
| Field | Description | Example |
|-------|-------------|---------|
| latency | Max acceptable response time | `< 100ms` |
| memory | Max memory usage | `< 50MB` |
| command | Benchmark script to run | `npm run benchmark` |

Benchmarks run automatically after each task passes validation. Results logged to `.ralph/benchmark.log`.

### 5. Check Memory for Relevant Learnings

```bash
cd $CLAUDE_PROJECT_DIR/opc && PYTHONPATH=. uv run python scripts/core/recall_learnings.py \
  --query "{goal keywords}" --k 3 --text-only
```

### 6. Write guardrails.md (Seed + Accumulate)

**First run:** Seed from memory, project patterns, AND code quality guidelines
**Subsequent runs:** Preserve previous guardrails + add new

```markdown
# Guardrails

## Code Quality (Always Include)
- Keep files 150-500 lines (split if larger)
- One module = one responsibility
- Match existing project patterns and conventions
- Extract shared utilities to dedicated files
- Write tests alongside new code

## Project Patterns (from analysis)
{detected patterns that should be followed}

## From Memory
{recalled learnings about this project}

## Learned from Previous Runs
{guardrails from past Ralph sessions - PRESERVED}
- [2026-01-20 goal:"fix auth"] Always invalidate tokens on password change
- [2026-01-21 goal:"add API"] Use transaction for multi-table ops

---

## Learned This Run
{new guardrails added during current execution}
```

**Key:** Guardrails accumulate across Ralph runs. Don't wipe them.

See `CODE_QUALITY.md` for detailed guidelines and validation commands.

### 7. Write activity.log (Empty)

```bash
touch .ralph/activity.log
```

### 8. Update .gitignore

Add Ralph-generated files to .gitignore (if not already present):

```bash
# Check if .gitignore exists and add Ralph patterns
if [ -f .gitignore ]; then
  if ! grep -q ".ralph/activity.log" .gitignore; then
    cat >> .gitignore << 'EOF'

# Ralph generated files (logs, cache)
.ralph/activity.log
.ralph/cost.log
.ralph/analysis-meta.json
.ralph/project-context.md
.ralph/history/
EOF
    echo "Updated .gitignore with Ralph patterns"
  fi
else
  # Create .gitignore with Ralph patterns
  cat > .gitignore << 'EOF'
# Ralph generated files (logs, cache)
.ralph/activity.log
.ralph/cost.log
.ralph/analysis-meta.json
.ralph/project-context.md
.ralph/history/
EOF
  echo "Created .gitignore with Ralph patterns"
fi
```

See `GITIGNORE.md` for full details on what to track vs ignore.

### 9. Inform User (Host Mode - Default)

The loop script is centralized at `~/.claude/ralph-docker/ralph-loop-host.sh`.
No need to generate per-project.

**Output to user:**

```
Ralph setup complete!

Files created in .ralph/
- task.md: X tasks to complete
- prompt.md: Static agent instructions
- guardrails.md: N initial guardrails from memory

To start: ~/.claude/ralph-docker/ralph-loop-host.sh [max_iterations]
Or use: /ralph start (auto-opens terminal)

Monitor: tail -f .ralph/activity.log
Check progress: grep "passes:" .ralph/task.md
```

### Central Loop Script

The host-based loop at `~/.claude/ralph-docker/ralph-loop-host.sh`:
- Auto-detects project root (git, package.json, etc.)
- Uses project-specific `.ralph/` directory
- Runs `claude -p` with fresh context per iteration
- Works with Claude Code subscription (no API key needed)

---

## Docker Mode (`/ralph "goal" --docker`)

When `--docker` flag is used, inform user about Docker execution:

### Prerequisites Check

```bash
# Check Docker is available
docker info > /dev/null 2>&1 || echo "Warning: Docker not running"

# Check API key is set (OAuth doesn't work in containers)
[ -n "$ANTHROPIC_API_KEY" ] || echo "Warning: ANTHROPIC_API_KEY not set"
```

### Output to user (Docker mode)

```
Ralph Docker setup complete!

Files created in .ralph/
- task.md: X tasks to complete
- prompt.md: Static agent instructions
- guardrails.md: N initial guardrails from memory

Prerequisites:
- Docker Desktop running
- ANTHROPIC_API_KEY environment variable set
  (OAuth tokens don't work in containers)

To start: ANTHROPIC_API_KEY=your-key ~/.claude/ralph-docker/ralph-docker.sh [max_iterations]

Monitor: tail -f .ralph/activity.log
Check progress: grep "passes:" .ralph/task.md

Benefits of Docker mode:
- Security isolation (Claude can only access /workspace)
- Can run on remote servers
- Resource limits (4GB RAM, 2 CPUs)

Note: Subscription users without API key should use host mode instead.
```

The Docker script at `~/.claude/ralph-docker/ralph-docker.sh`:
- Auto-detects project root and .ralph/ directory
- Builds Docker image if needed
- Runs in isolated container with restricted network
- Tracks costs and enforces budget limits

---

## Parallel Mode (`/ralph "goal" --parallel N`)

When `--parallel N` flag is used:

### 1. Setup base Ralph files as normal

### 2. Inform user about parallel script

The parallel script at `~/.claude/ralph-docker/ralph-parallel.sh`:
- Runs N concurrent Docker containers
- Each worker has dedicated task lanes
- Requires API key (no OAuth support)

### 3. Output to user (Parallel mode)

```
Ralph Parallel setup complete!

Files created in .ralph/
- task.md: X tasks to complete (will be distributed across workers)
- prompt.md: Static agent instructions
- guardrails.md: N initial guardrails
- ralph-parallel.sh: Parallel execution script

This will create:
- N git worktrees (isolated working directories)
- N Docker containers (one per worktree)
- Tasks distributed round-robin across workers

Prerequisites:
- Docker Desktop running
- Git repository (for worktrees)
- ANTHROPIC_API_KEY environment variable set

To start: ANTHROPIC_API_KEY=your-key ~/.claude/ralph-docker/ralph-parallel.sh N [max_iterations_per_worker]

Monitor all workers: tail -f ../ralph-worktree-*/.ralph/activity.log

Note: Parallel mode increases API costs linearly with worker count.
```

---

## Status Workflow (`/ralph status`)

### Check Current Progress

```bash
# Count completed vs pending
echo "=== Ralph Status ==="
echo "Completed: $(grep -c 'passes: true' .ralph/task.md 2>/dev/null || echo 0)"
echo "Pending: $(grep -c 'passes: false' .ralph/task.md 2>/dev/null || echo 0)"
echo ""
echo "=== Recent Activity ==="
tail -20 .ralph/activity.log
echo ""
echo "=== Guardrails Learned ==="
grep -c "^## Sign:" .ralph/guardrails.md 2>/dev/null || echo "0"
```

---

## Summary Workflow (`/ralph summary`)

### 1. Parse Results

```bash
COMPLETED=$(grep -c 'passes: true' .ralph/task.md 2>/dev/null || echo 0)
PENDING=$(grep -c 'passes: false' .ralph/task.md 2>/dev/null || echo 0)
GUARDRAILS=$(grep -c "^## Sign:" .ralph/guardrails.md 2>/dev/null || echo 0)
```

### 2. Extract New Guardrails

Read `.ralph/guardrails.md` and identify guardrails added during the run (those with "Added: Iteration" in them).

### 3. Store Significant Learnings

For each guardrail added during the run, store as a learning:

```bash
cd $CLAUDE_PROJECT_DIR/opc && PYTHONPATH=. uv run python scripts/core/store_learning.py \
  --session-id "ralph-$(date +%s)" \
  --type WORKING_SOLUTION \
  --content "{guardrail content}" \
  --context "Ralph run for {goal}" \
  --tags "ralph,guardrail,auto-generated" \
  --confidence medium
```

### 4. Archive Run to History

```bash
# Archive completed run for future reference
GOAL_SLUG=$(echo "{goal}" | tr ' ' '-' | tr '[:upper:]' '[:lower:]' | cut -c1-30)
DATE=$(date +%Y-%m-%d)

mkdir -p .ralph/history
cp .ralph/task.md ".ralph/history/${DATE}-${GOAL_SLUG}.md"

# Update analysis-meta.json with run info
```

### 5. Generate Summary

```markdown
# Ralph Run Summary

## Workspace
- Project: {project_name}
- Root: {project_root}

## Results
- Tasks completed: X/Y
- Iterations used: N
- Guardrails learned: Z

## Completed Tasks
{list of tasks with passes: true}

## Remaining Tasks (if any)
{list of tasks with passes: false}

## New Guardrails
{guardrails added during run}

## Next Steps
- [ ] Review the generated code
- [ ] Run full test suite
- [ ] Create commit for the work

Run archived to: .ralph/history/{date}-{goal}.md
```

---

## Why External Loop Is Required

Using hooks or agent spawning within Claude Code means the **main session still accumulates context**:

```
Main Session Context:
  Turn 1: "Starting ralph loop..."
  Turn 2: Agent 1 completed task 1
  Turn 3: Agent 2 completed task 2
  ...
  Turn 20: [Context polluted with 20 turns of orchestration noise]
```

External loop means:
- Each `claude -p` spawns a **fresh process**
- Process reads files, does work, exits
- **Zero context accumulation**
- Loop control is external (bash decides when to stop, not Claude)

---

## Common Mistakes (Don't Do These)

| Mistake | Why It Fails |
|---------|--------------|
| Compaction instead of wipe | AI guesses what's important, guesses wrong |
| Growing instruction files | Fills context before work starts |
| AI controls the loop | AI can't decide when to stop |
| Vague task definitions | Need specific, validatable tasks |
| Modifying prompt.md | Must be static for clean context |

---

## Cost Expectations

| Setup | Typical Cost | Result |
|-------|--------------|--------|
| Correct (fresh context) | $30-50 | Working proof of concept |
| Wrong (accumulated context) | $300+ | Broken mess |

Budget ~$2-3 per iteration. Most projects: 15-25 iterations.

---

## IdeaRalph Integration

For ideation phase before Ralph implementation:

1. Use IdeaRalph MCP tools (brainstorm, validate, refine, prd, architecture)
2. Convert architecture output to task.md format
3. Run `/ralph setup` with converted tasks

See `/idea-to-ralph` skill for full pipeline.
