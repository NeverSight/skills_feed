---
name: ralph
description: Set up and run Ralph Wiggum loop - autonomous AI coding with clean slate iterations, PRD-driven features, and CI quality gates. Use for long-running autonomous coding tasks.
---

# Ralph Wiggum Loop Skill

Autonomous AI coding pattern that runs agents in iterations with clean context, working on PRD-driven features while maintaining CI green.

## Commands

| Command | Action |
|---------|--------|
| `/ralph` | Show help menu |
| `/ralph setup` | Create Ralph infrastructure |
| `/ralph init` | Build custom PRD interactively |
| `/ralph run` | Execute the autonomous loop |

---

## `/ralph setup`

Create all Ralph files in the current directory.

**Steps:**
1. Read and copy templates from this skill's `templates/` folder:
   - [templates/ralph-loop.sh](templates/ralph-loop.sh) → `./ralph-loop.sh`
   - [templates/prd.json](templates/prd.json) → `./prd.json`
   - [templates/progress.txt](templates/progress.txt) → `./progress.txt`
   - [templates/README-RALPH.md](templates/README-RALPH.md) → `./README-RALPH.md`

2. Make script executable: `chmod +x ralph-loop.sh`

3. Detect project context and customize:
   - Check for `package.json` → determine package manager (pnpm/npm/yarn)
   - Check for `tsconfig.json` → TypeScript project
   - Update test commands in ralph-loop.sh accordingly

4. Show completion message with next steps

---

## `/ralph init`

Guide user through creating a custom PRD interactively.

**Questions to ask:**
1. Project name?
2. What features do you want to build? (collect 3-5 user stories)
3. For each story:
   - Title?
   - Description?
   - Acceptance criteria? (3-5 specific, testable criteria)

**Output:** Generate `prd.json` with user's input. Offer to create other Ralph files if not present.

---

## `/ralph run`

Execute the Ralph loop.

**Pre-flight checks:**
1. Verify `ralph-loop.sh` exists
2. Verify `prd.json` exists
3. Show summary:
   - Total user stories
   - Incomplete stories (where `passes: false`)
   - Max iterations configured
4. Ask for confirmation
5. Execute: `./ralph-loop.sh`

---

## `/ralph` (no args)

Show help menu:

```
Ralph Wiggum Loop - Autonomous AI Coding

Commands:
  /ralph setup  - Create Ralph infrastructure in this directory
  /ralph init   - Create a new PRD from scratch
  /ralph run    - Run the Ralph loop

What would you like to do?
```

---

## Key Principles

1. **Clean slate each iteration** - Fresh context, no baggage
2. **One feature at a time** - Prevents scope creep
3. **CI must stay green** - Tests and types pass every commit
4. **Progress tracking** - Append to progress.txt each iteration
5. **Clear stop condition** - `<promise>COMPLETE</promise>` when all stories pass
6. **Safety limit** - Max iterations prevents infinite loops

## PRD Quality Checklist

Good user stories are:
- ✅ Specific and scoped (completable in one iteration)
- ✅ Clear acceptance criteria (testable, unambiguous)
- ✅ Properly prioritized (1 = highest)
- ✅ Has `"passes": false` initially

Bad user stories are:
- ❌ Too vague ("build the UI")
- ❌ Too large (touches many systems)
- ❌ Unclear criteria ("make it nice")
