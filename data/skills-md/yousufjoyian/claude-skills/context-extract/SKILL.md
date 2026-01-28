---
name: context-extract
description: Append conversation context to cumulative project history - never overwrites
---

# Context Extract Skill

**CUMULATIVE** context extraction - always appends, never overwrites.

## Triggers

- "extract context"
- "save conversation"
- "export context"
- "dump context"

## Core Principle: APPEND ONLY

Each extraction ADDS to existing context files. This builds a complete project history over time.

## Output Structure

```
<project>/.claude/context/
├── HISTORY.md          # Cumulative session log (append-only)
├── DECISIONS.md        # All decisions ever made (append-only)
├── DIRECTIONS.md       # Direction changes and pivots (append-only)
└── archive/            # Old files if manual cleanup needed
    └── HISTORY_pre_YYYY-MM-DD.md
```

## Workflow

### Step 1: Read Existing Context Files

```bash
PROJECT=$(basename $(pwd))
CONTEXT_DIR=~/local_workspaces/$PROJECT/.claude/context
TIMESTAMP=$(date +%Y-%m-%d_%H%M)

mkdir -p $CONTEXT_DIR/archive

# Read existing files to understand current state
cat $CONTEXT_DIR/HISTORY.md 2>/dev/null || echo "[No history yet]"
cat $CONTEXT_DIR/DECISIONS.md 2>/dev/null || echo "[No decisions yet]"
cat $CONTEXT_DIR/DIRECTIONS.md 2>/dev/null || echo "[No direction changes yet]"
```

### Step 2: Detect Direction Changes

**CRITICAL:** Compare what was PLANNED vs what actually HAPPENED.

Check these sources for planned direction:
- Previous `HISTORY.md` "Next Actions" section
- `CONTEXT.md` "Resume" section
- User's initial request this session

If work diverged from plan, document it in DIRECTIONS.md:

```markdown
## Direction Change: YYYY-MM-DD HH:MM

**Original Plan:**
[What was supposed to happen]

**What Actually Happened:**
[What we did instead]

**Why the Pivot:**
[Reason - user request, blocker discovered, better approach found, etc.]

**Impact:**
[What this means for the project going forward]
```

### Step 3: Append to HISTORY.md

**APPEND** a new session block (never replace):

```markdown
---

## Session: YYYY-MM-DD HH:MM

### Goal
[What this session aimed to accomplish]

### Accomplished
- [x] Task 1
- [x] Task 2
- [→] Task 3 (in progress)
- [ ] Task 4 (not started)

### Files Changed
- `path/file.ts` - [what changed]
- `path/new.ts` - NEW: [purpose]

### Commands Run
```bash
[key commands only]
```

### Errors & Solutions
- **Error:** [description]
  **Fix:** [how resolved]

### Next Actions
1. [Priority 1]
2. [Priority 2]

### Notes
[Any context for future sessions]
```

### Step 4: Append to DECISIONS.md

**APPEND** any new decisions (check for duplicates first):

```markdown
---

## YYYY-MM-DD: [Decision Title]

**Context:** [Why this decision was needed]

**Options Considered:**
1. [Option A] - [pros/cons]
2. [Option B] - [pros/cons]

**Decision:** [What was chosen]

**Rationale:** [Why]

**Affected Files:** [list]

**Reversible:** [Yes/No - and how if yes]
```

### Step 5: Append to DIRECTIONS.md (if applicable)

Only add if direction changed from what was planned:

```markdown
---

## YYYY-MM-DD HH:MM: [Pivot Description]

**Was Planning To:** [original plan]

**Instead Did:** [what happened]

**Trigger:** [user request / blocker / discovery / better idea]

**Old Direction:**
[brief description of abandoned path]

**New Direction:**
[brief description of new path]

**Carryover:** [what from old direction still applies]

**Abandoned:** [what's being dropped]
```

### Step 6: Git Commit

```bash
cd ~/local_workspaces/$PROJECT

git add .claude/context/

git commit -m "$(cat <<'EOF'
docs(context): Append session context YYYY-MM-DD HH:MM

- Added session to HISTORY.md
- [N] new decisions recorded
- [Direction change noted / No direction change]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"

git push origin $(git branch --show-current) 2>/dev/null || echo "Push skipped"
```

### Step 7: Confirm

```
Context appended successfully!

HISTORY.md:
  + Session YYYY-MM-DD HH:MM added
  Total sessions: [N]

DECISIONS.md:
  + [N] new decisions added
  Total decisions: [M]

DIRECTIONS.md:
  + Direction change recorded: [title]
  OR
  (no direction change this session)

Git: [commit hash] pushed to origin/main
```

## Direction Change Detection

**Ask yourself before extracting:**

1. What did CONTEXT.md say to do next?
2. What did the user actually ask for?
3. Did we do what was planned, or something different?

**Common direction changes:**
- User requested different feature mid-session
- Discovered blocker that required pivot
- Found better approach than originally planned
- Scope change (bigger or smaller)
- Priority shift (different feature first)

**Always document WHY** - future agents need to know the reasoning.

## File Size Management

If HISTORY.md exceeds ~500 lines:
```bash
# Archive old content
mv $CONTEXT_DIR/HISTORY.md $CONTEXT_DIR/archive/HISTORY_pre_$(date +%Y-%m-%d).md

# Start fresh with reference
echo "# Project History (continued)

Previous history archived: archive/HISTORY_pre_$(date +%Y-%m-%d).md

---
" > $CONTEXT_DIR/HISTORY.md
```

## Example: Direction Change Entry

```markdown
---

## 2026-01-19 22:00: Gemini Migration Instead of Voice Improvements

**Was Planning To:** Improve voice input detection and add wake word support

**Instead Did:** Migrated Council backend from Claude CLI to Gemini API

**Trigger:** User request - provided detailed migration plan

**Old Direction:**
Voice UX improvements - better mic handling, wake word "Hey Claude"

**New Direction:**
Backend modernization - direct Gemini API, streaming, no subprocess

**Carryover:** Voice improvements still on roadmap, now lower priority

**Abandoned:** Nothing permanently - voice work deferred
```

## Integration with Other Skills

| Skill | Relationship |
|-------|--------------|
| `session-save` | Quick ~250 token summary; context-extract is comprehensive history |
| `onboard` | Reads HISTORY.md and DECISIONS.md for full project context |
| `synopsis` | Visual snapshot; context-extract is text archive |

## Key Differences from session-save

| Aspect | session-save | context-extract |
|--------|--------------|-----------------|
| Size | ~250 tokens | Unlimited (cumulative) |
| Overwrites | Yes (CONTEXT.md) | Never (append only) |
| Purpose | Quick handoff | Full project memory |
| Direction tracking | No | Yes |
| Decision log | No | Yes |
