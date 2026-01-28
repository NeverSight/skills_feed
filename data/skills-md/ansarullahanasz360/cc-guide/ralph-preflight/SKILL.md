---
name: ralph-preflight
description: Pre-flight check for Ralph TUI loops. Validates config, templates, prd.json, and environment before starting a loop. Run after /prd to verify everything is ready. Detects global CLAUDE.md conflicts, validates template variables, and provides launch commands.
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Edit
  - Write
  - AskUserQuestion
  - TodoWrite
---

# Ralph TUI Pre-Flight Check

Fast verification that everything is configured correctly before starting a Ralph loop. Run this after creating a PRD with `/prd` to validate and launch.

## When to Use

- After running `/prd` to create a prd.json
- Before starting any Ralph loop
- When troubleshooting Ralph loop issues
- To verify template and config are in sync

## Pre-Flight Phases

Execute these checks in order. Stop and report if critical issues are found.

---

## Phase 1: Environment Check

### 1.1 Global CLAUDE.md Conflict Detection (CRITICAL)

Ralph loops can have global `~/.claude/CLAUDE.md` override local project `CLAUDE.md`. Check and warn:

```bash
# Check if global CLAUDE.md exists
if [ -f ~/.claude/CLAUDE.md ]; then
  echo "WARNING: Global CLAUDE.md exists at ~/.claude/CLAUDE.md"
  echo "This may override your local CLAUDE.md during Ralph loops"
  wc -l ~/.claude/CLAUDE.md
else
  echo "OK: No global CLAUDE.md found"
fi
```

**If global CLAUDE.md exists:**
- Show its contents (first 20 lines)
- Ask user if they want to:
  - A. Remove it temporarily (rename to CLAUDE.md.bak)
  - B. Keep it (may cause issues)
  - C. View full contents first

### 1.2 Ralph TUI Installation

```bash
which ralph-tui && ralph-tui --version
```

### 1.3 Required Tools

```bash
# Check tmux (required for persistent sessions)
which tmux && tmux -V

# Check git (required for worktrees)
git --version
```

### 1.4 Existing Ralph State Detection (CRITICAL)

Check if `.ralph-tui/` has data from a previous run that could interfere:

```bash
# Check for existing state
if [ -d .ralph-tui ]; then
  echo "Found existing .ralph-tui/ directory"

  # Check for progress file with content
  if [ -f .ralph-tui/progress.md ] && [ -s .ralph-tui/progress.md ]; then
    echo "⚠ progress.md exists with content ($(wc -l < .ralph-tui/progress.md) lines)"
  fi

  # Check for iteration logs
  if [ -d .ralph-tui/iterations ] && [ "$(ls -A .ralph-tui/iterations 2>/dev/null)" ]; then
    echo "⚠ iterations/ has $(ls .ralph-tui/iterations | wc -l) log files"
  fi

  # Check for session state
  if [ -f .ralph-tui/state.json ]; then
    echo "⚠ state.json exists (previous session state)"
  fi

  # Check for lock file (Ralph might be running)
  if [ -f .ralph-tui.lock ]; then
    echo "⚠ .ralph-tui.lock exists - Ralph may be running!"
  fi
else
  echo "OK: No existing .ralph-tui/ state"
fi
```

**If existing state is found, determine the situation:**

```
AskUserQuestion: "Found existing Ralph state from a previous run. What's the situation?"
├── "Previous run is complete, clean up for new PRD"
│   → Clean .ralph-tui/iterations/, progress.md, state.json
│   → Keep config.toml and templates
├── "Previous run is still active (different PRD)"
│   → Create new worktree for this PRD
│   → Keep current directory untouched
├── "Save progress to branch first, then clean"
│   → Commit current progress
│   → Clean for new PRD
└── "Let me check the progress first"
│   → Show progress.md contents
│   → Show iteration count
│   → Re-ask after review
```

**Cleanup commands (if user chooses to clean):**

```bash
# Remove iteration logs
rm -rf .ralph-tui/iterations/*

# Clear progress file (keep file, clear content)
echo "" > .ralph-tui/progress.md

# Remove session state
rm -f .ralph-tui/state.json
rm -f .ralph-tui.lock
rm -f .ralph-tui-session.json

# Verify cleanup
ls -la .ralph-tui/
echo "Cleaned. Ready for new Ralph loop."
```

**If previous run is still active:**

```bash
# Check current branch
CURRENT_BRANCH=$(git branch --show-current)
echo "Current branch: $CURRENT_BRANCH"

# Suggest worktree for new PRD
REPO_NAME=$(basename $(git rev-parse --show-toplevel))
echo "Suggested worktree: ../${REPO_NAME}-[new-prd-name]"
```

Then proceed to Phase 7 for worktree setup.

---

## Phase 2: Configuration Validation

### 2.1 Locate .ralph-tui/config.toml

```bash
# Check project config exists
if [ -f .ralph-tui/config.toml ]; then
  echo "OK: Config found at .ralph-tui/config.toml"
else
  echo "ERROR: No .ralph-tui/config.toml found"
  echo "Run: ralph-tui setup"
fi
```

### 2.2 Validate Config Settings

Read config.toml and verify critical settings:

| Setting | Required Value | Check |
|---------|---------------|-------|
| `tracker` | `"json"` | Must be json for prd.json execution |
| `agent` | `"claude"` | Claude agent |
| `prompt_template` | Path exists | Template file must exist |
| `model` | `"opus"` or `"sonnet"` | Valid model |
| `maxIterations` | > 0 | Reasonable iteration limit |

### 2.3 Show Template Source

```bash
ralph-tui template show | head -5
```

Verify it's loading from expected location (not default).

---

## Phase 3: Template Validation

### 3.1 Locate prompt.hbs

Get template path from config.toml `prompt_template` setting and verify file exists:

```bash
# Extract template path from config
grep "prompt_template" .ralph-tui/config.toml
# Verify file exists
ls -la [extracted-path]
```

### 3.2 Template Variable Check

Read the prompt.hbs and verify it uses these required variables:

**PRD Variables:**
- `{{prdName}}` - Project name
- `{{prdDescription}}` - Project overview
- `{{prdCompletedCount}}` / `{{prdTotalCount}}` - Progress
- `{{currentIteration}}` - Current iteration number (REQUIRED in header)

**Task Variables:**
- `{{taskId}}` - Story ID (e.g., US-001)
- `{{taskTitle}}` - Story title
- `{{taskDescription}}` - What and why (includes embedded tasks)
- `{{acceptanceCriteria}}` - Auto-formatted checkbox list
- `{{notes}}` - Additional context
- `{{dependsOn}}` - Prerequisites

**Context Variables:**
- `{{codebasePatterns}}` - Discovered patterns (optional)

**DEPRECATED (should NOT be in template):**
- `{{recentProgress}}` - Agent reads `.ralph-tui/progress.md` directly as first action

### 3.3 Template Quality Check (Optimized v2)

Verify template includes all critical elements:

**Structure Checks:**
- [ ] Template does NOT include `{{recentProgress}}` (agent reads file directly - this is redundant)
- [ ] Template includes `{{currentIteration}}` in header for tracking
- [ ] Template has explicit "Context Files (Read These First)" section with:
  - [ ] Path to `.ralph-tui/progress.md`
  - [ ] Instruction to find `PRD.md` in same directory as `prd.json`

**Workflow Checks:**
- [ ] Template includes 3-phase workflow: Context Gathering → Implementation → Documentation
- [ ] Phase 3 includes gibberish cleanup instructions (remove JSON fragments, malformed entries)
- [ ] Template defines verbose progress entry format with sections:
  - [ ] "What was implemented" (detailed descriptions)
  - [ ] "Files changed" (paths with descriptions)
  - [ ] "Learnings" (patterns, gotchas, architecture insights)
  - [ ] "Quality gate" (command output, test results)

**Rules Checks:**
- [ ] Template says "Be verbose and thorough - future iterations start with no memory"
- [ ] Template instructs to delete malformed entries (JSON fragments, `"type":"message"`, gibberish)
- [ ] Completion signals (COMPLETE, BLOCKED, SKIP, EJECT)
- [ ] Loop awareness (starts fresh each iteration, must read progress.md)

**Context References:**
- [ ] Reference to CLAUDE.md for project commands/conventions
- [ ] Reference to progress.md for iteration context
- [ ] Reference to PRD.md for full project goals

### 3.4 Template Anti-Pattern Detection

Flag these issues if found:

| Issue | Problem | Fix |
|-------|---------|-----|
| `{{recentProgress}}` in template | Redundant - agent reads file directly | Remove the section |
| No `{{currentIteration}}` | Can't track which iteration in logs | Add to header |
| No gibberish cleanup instruction | JSON fragments accumulate in progress.md | Add Phase 3 step 7 |
| Simple progress format | Future iterations lack context | Use verbose 4-section format |
| No "start with no memory" warning | Agent may not document thoroughly | Add to rules section |

---

## Phase 4: PRD Validation

### 4.1 Discover prd.json

Search for prd.json files:

```bash
find . -name "prd.json" -not -path "*/node_modules/*" 2>/dev/null
```

If multiple found, ask user to select. If none found, report and exit.

### 4.2 Validate prd.json Structure

Read the prd.json and verify required fields:

```json
{
  "name": "required - kebab-case",
  "description": "required - project context",
  "branchName": "required - git branch name",
  "userStories": [
    {
      "id": "required - e.g., US-001",
      "title": "required - short title",
      "description": "required - what and why",
      "acceptanceCriteria": "required - array of strings",
      "dependsOn": "optional - array of story IDs",
      "notes": "optional - additional context",
      "passes": "required - boolean, should be false initially"
    }
  ]
}
```

### 4.3 Template Variable Mapping

Verify prd.json fields will map correctly to template:

| prd.json Field | Template Variable | Status |
|----------------|-------------------|--------|
| `name` | `{{prdName}}` | Check |
| `description` | `{{prdDescription}}` | Check |
| `userStories[].id` | `{{taskId}}` | Check |
| `userStories[].title` | `{{taskTitle}}` | Check |
| `userStories[].description` | `{{taskDescription}}` | Check |
| `userStories[].acceptanceCriteria` | `{{acceptanceCriteria}}` | Check |
| `userStories[].notes` | `{{notes}}` | Check |
| `userStories[].dependsOn` | `{{dependsOn}}` | Check |

### 4.4 Tasks in Description Check

Verify each story's description includes embedded tasks:

```
**Tasks:**
1. First task
2. Second task
```

**WARNING:** Tasks are NOT a separate field - they must be in the description.

### 4.5 Acceptance Criteria Format

Verify acceptanceCriteria is an array of strings (Ralph auto-converts to checkboxes).

---

## Phase 5: Project Context Validation

### 5.1 Local CLAUDE.md Check

```bash
if [ -f CLAUDE.md ]; then
  echo "OK: Local CLAUDE.md found"
  # Check it has key sections
  grep -l "Commands\|Development\|Project" CLAUDE.md
else
  echo "WARNING: No local CLAUDE.md - Ralph will rely on global context"
fi
```

### 5.2 PRD.md Discovery

Check for human-readable PRD document:

```bash
find . -name "PRD.md" -o -name "prd.md" | head -5
```

If found, note the path for the prompt template enhancement.

### 5.3 Progress.md Path

Verify progress file path from config:

```bash
grep "progressFile" .ralph-tui/config.toml
# Default: .ralph-tui/progress.md
```

---

## Phase 6: Pre-Launch Summary

### 6.1 Generate Report

Present a clear summary:

```
═══════════════════════════════════════════════════════════════════════════
Ralph TUI Pre-Flight Check Results
═══════════════════════════════════════════════════════════════════════════

Environment
├── Global CLAUDE.md: ✗ Not found (good) / ⚠ Found (may conflict)
├── Ralph TUI: ✓ v0.x.x installed
├── tmux: ✓ v3.x installed
├── git: ✓ v2.x installed
└── Existing State: ✓ Clean / ⚠ Previous run detected (action taken)

Existing State Details (if found)
├── progress.md: [X lines] / Empty
├── iterations/: [X files] / Empty
├── state.json: Found / Not found
└── Lock file: ⚠ Running / Not found

Configuration (.ralph-tui/config.toml)
├── Tracker: json ✓
├── Agent: claude ✓
├── Model: opus ✓
├── Max Iterations: 70 ✓
├── Template Path: .ralph-tui/templates/prompt.hbs ✓
└── PRD Path: [discovered path] ✓

Template (.ralph-tui/templates/prompt.hbs)
├── File exists: ✓
├── PRD variables: ✓
├── Task variables: ✓
├── Context variables: ✓
├── Workflow section: ✓
└── Completion signals: ✓

PRD (docs/prds/[name]/prd.json)
├── Name: [prd-name] ✓
├── Branch: [branch-name] ✓
├── Stories: [count] stories ✓
├── All have IDs: ✓
├── All have descriptions: ✓
├── All have acceptance criteria: ✓
└── Tasks embedded in descriptions: ✓

Project Context
├── Local CLAUDE.md: ✓ Found
├── PRD.md: ✓ Found at [path]
└── Progress tracking: .ralph-tui/progress.md (clean)

═══════════════════════════════════════════════════════════════════════════
```

### 6.2 Issues Found

If any issues were found, list them with severity:

```
Issues Found:
├── [CRITICAL] Global CLAUDE.md may override local context
├── [CRITICAL] Existing Ralph state - may confuse model with old progress
├── [CRITICAL] Lock file present - Ralph may already be running
├── [WARNING] Story US-003 missing tasks in description
└── [INFO] Model set to sonnet, opus recommended for complex work
```

---

## Phase 7: Launch Options

### 7.1 Worktree vs Branch Question

```
AskUserQuestion: "How do you want to run this Ralph loop?"
├── "Branch only" - Create/switch to feature branch in current directory
├── "Worktree" - Create isolated worktree for parallel development
└── "Already set up" - Skip branch/worktree setup
```

### 7.2 Branch Setup (if selected)

```bash
# Determine base branch
git branch --show-current

# Create and checkout feature branch
git checkout -b [branchName-from-prd]
```

### 7.3 Worktree Setup (if selected)

```bash
# Get repo name and PRD name
REPO_NAME=$(basename $(git rev-parse --show-toplevel))
PRD_NAME=[name-from-prd]

# Create worktree
git worktree add ../${REPO_NAME}-${PRD_NAME} -b [branchName-from-prd]

# Show next steps
echo "Worktree created at: ../${REPO_NAME}-${PRD_NAME}"
echo "cd ../${REPO_NAME}-${PRD_NAME}"
```

### 7.4 Generate Launch Commands

Provide ready-to-copy commands:

```
═══════════════════════════════════════════════════════════════════════════
Launch Commands
═══════════════════════════════════════════════════════════════════════════

Option 1: Run in new tmux session (recommended)
───────────────────────────────────────────────────────────────────────────
tmux new-session -d -s ralph-[prd-name] "ralph-tui run --prd [prd-path]"
tmux attach-session -t ralph-[prd-name]
# Press 's' to start, then Ctrl+B D to detach

Option 2: Run directly (stays in foreground)
───────────────────────────────────────────────────────────────────────────
ralph-tui run --prd [prd-path]

Option 3: Run with verification (recommended first time)
───────────────────────────────────────────────────────────────────────────
ralph-tui run --prd [prd-path] --verify

Monitoring:
───────────────────────────────────────────────────────────────────────────
# Check progress
cat .ralph-tui/progress.md

# View iteration logs
ralph-tui logs

# Check session status
ralph-tui status

# Reattach to tmux
tmux attach-session -t ralph-[prd-name]
═══════════════════════════════════════════════════════════════════════════
```

---

## Quick Reference

### Template Variables from Ralph TUI

| Variable | Source | Description |
|----------|--------|-------------|
| `{{prdName}}` | prd.json `name` | Project name |
| `{{prdDescription}}` | prd.json `description` | Project context |
| `{{prdCompletedCount}}` | Calculated | Completed stories |
| `{{prdTotalCount}}` | Calculated | Total stories |
| `{{currentIteration}}` | Calculated | Current iteration number |
| `{{taskId}}` | `userStories[].id` | Current story ID |
| `{{taskTitle}}` | `userStories[].title` | Current story title |
| `{{taskDescription}}` | `userStories[].description` | Story description (includes tasks) |
| `{{acceptanceCriteria}}` | `userStories[].acceptanceCriteria` | Auto-formatted checkboxes |
| `{{notes}}` | `userStories[].notes` | Additional context |
| `{{dependsOn}}` | `userStories[].dependsOn` | Prerequisites |
| `{{codebasePatterns}}` | `.ralph-tui/progress.md` | Discovered patterns |

**DEPRECATED - Do NOT use:**
| Variable | Reason |
|----------|--------|
| `{{recentProgress}}` | Redundant - agent reads `.ralph-tui/progress.md` directly as first action every iteration |

### Common Issues

| Issue | Solution |
|-------|----------|
| Global CLAUDE.md overrides local | Rename `~/.claude/CLAUDE.md` to `.bak` |
| Existing state from previous run | Clean iterations/, progress.md, state.json OR use worktree |
| Lock file present | Another Ralph may be running; check tmux sessions |
| Template not loading | Check `prompt_template` path in config.toml |
| Tasks not showing | Embed tasks in `description` field, not separate |
| acceptanceCriteria empty | Ensure it's an array of strings |
| Progress corrupted | Check `.ralph-tui.lock`, use `ralph-tui resume` |
| Model confused by old progress | Clean progress.md before starting new PRD |
| Gibberish/JSON in progress.md | Template should include cleanup instructions in Phase 3 |
| Duplicate progress entries | Ralph auto-appends + agent appends; use cleanup instructions |
| Template uses `{{recentProgress}}` | Remove it - agent reads file directly (redundant) |
| Missing `{{currentIteration}}` | Add to header for iteration tracking |
| Sparse progress notes | Use verbose 4-section format; add "no memory" warning |

### Ralph TUI Commands

```bash
ralph-tui template show     # Show current template
ralph-tui doctor            # Diagnose issues
ralph-tui config show       # Show merged config
ralph-tui status            # Check session status
ralph-tui resume            # Resume interrupted session
ralph-tui logs              # View iteration logs
```
