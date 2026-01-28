---
name: ralph-new
description: Create a new greenfield project with full Ralph Loop automation. Use when starting a new project from scratch, creating a new application, or when the user says "ralph new", "new project", or "build me".
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebFetch, AskUserQuestion
---

# Ralph New Project Skill

Create a new greenfield project with full Ralph Loop automation including PRD generation, task database, Playwright testing, and automatic execution of all tasks.

## CRITICAL: AUTONOMOUS EXECUTION

After gathering requirements and setting up the project, you MUST automatically start the Ralph Loop and continue working until ALL tasks are complete. Do NOT stop after setup - the goal is fully autonomous development.

## WORKFLOW

### Phase 1: Gather Requirements

**Step 1.1: Get User Input**

Ask the user what they want to build. Accept:
- Text description
- Document paths (read them with Read tool)
- URLs (fetch with WebFetch)

```
What would you like to build? You can:
- Describe it in text
- Provide document path(s) with requirements
- Provide URL(s) with specifications
```

**Step 1.2: Read All Input Documents**

If user provides documents:
1. Read each document using the Read tool
2. Summarize key requirements from each
3. Combine into unified requirements

**Step 1.3: Ask Clarifying Questions**

You MUST ask clarifying questions using AskUserQuestion tool:

1. **Tech Stack**: What programming language/framework?
2. **Database**: What database if needed?
3. **Testing**: Confirm Playwright for E2E testing
4. **Authentication**: Does it need auth? What type?
5. **Any constraints**: Performance, security requirements?

Wait for user answers before proceeding.

### Phase 2: Fetch Documentation

**Step 2.1: Identify Technologies**

Based on user answers, identify all technologies needed.

**Step 2.2: Fetch Context7 Documentation**

For each technology, fetch current documentation using Context7 MCP tools or WebFetch.

Technology mapping:
- Next.js → nextjs
- React → react
- FastAPI → fastapi
- Django → django
- Express → express
- Playwright → playwright

### Phase 3: Create PRD with Tasks

**Step 3.1: Detect Platform**

```bash
# Detect operating system
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]] || [[ -n "$WINDIR" ]]; then
    PLATFORM="windows"
else
    PLATFORM="unix"
fi
```

**Step 3.2: Create Project Structure**

```bash
mkdir -p docs scripts tests/e2e
```

**Step 3.3: Generate PRD.md**

Create PRD.md with this exact structure:

```markdown
# Project Requirements Document

## Project Overview
[Brief description]

## Tech Stack
- Language: [e.g., Python 3.12]
- Framework: [e.g., FastAPI]
- Database: [e.g., SQLite]
- Testing: Playwright for E2E, pytest/jest for unit

## User Stories

### US-001: [Title]
**Description:** As a [user], I want [feature] so that [benefit].

**Acceptance Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] All tests pass

**Test Steps (Playwright):**
```json
[
  {"step": 1, "action": "navigate", "target": "/path"},
  {"step": 2, "action": "click", "target": "selector"},
  {"step": 3, "action": "verify", "target": "text", "expected": "result"}
]
```
```

**TASK SIZING:** Each task MUST be completable in ONE context window (~10 min).

**STORY ORDERING:**
1. Schema/database changes
2. Backend logic / API endpoints
3. UI components
4. Integration tests

**Step 3.4: Create progress.txt**

```markdown
# Progress Log

## Project: [Name]
Started: [Date]

## Learnings
(Patterns discovered during development)
```

**Step 3.5: Create AGENTS.md**

```markdown
# Agent Patterns

## Reusable Patterns
(Document patterns that work)

## Known Issues
(Track issues and solutions)
```

### Phase 4: Initialize Database

**Step 4.1: Check Prerequisites**

```bash
# Check SQLite
sqlite3 --version 2>/dev/null || echo "SQLite not found"
```

If not available, install:
- **Windows:** `winget install SQLite.SQLite`
- **macOS:** `brew install sqlite3`
- **Linux:** `sudo apt install sqlite3`

**Step 4.2: Copy Schema and Initialize**

Copy the schema from Ralph Skill templates directory and initialize:

```bash
# Initialize database
sqlite3 ralph.db < templates/schema.sql
```

Or create schema inline if template not available.

**Step 4.3: Import Tasks**

For each user story in PRD.md:

```bash
sqlite3 ralph.db "INSERT INTO tasks (task_id, name, type, status) VALUES ('US-001', 'Story title', 'user_story', 'planned');"
```

### Phase 5: Copy Loop Scripts and Dashboard

Copy the Ralph loop scripts and dashboard to the project:

**For Unix (Linux/macOS):**
```bash
# Copy scripts
cp [ralph-skill-path]/scripts/ralph.sh scripts/
cp [ralph-skill-path]/scripts/ralph-db.sh scripts/
chmod +x scripts/*.sh

# Copy dashboard
cp [ralph-skill-path]/templates/dashboard.html .
cp [ralph-skill-path]/templates/schema.sql templates/
```

**For Windows:**
```powershell
Copy-Item [ralph-skill-path]\scripts\ralph.ps1 scripts\
Copy-Item [ralph-skill-path]\scripts\ralph-db.ps1 scripts\

# Copy dashboard
Copy-Item [ralph-skill-path]\templates\dashboard.html .
Copy-Item [ralph-skill-path]\templates\schema.sql templates\
```

**Note:** The `[ralph-skill-path]` is typically:
- **Personal skills:** `~/.claude/skills/ralph-new/` (Unix) or `$env:USERPROFILE\.claude\skills\ralph-new\` (Windows)
- **If cloned:** The path where you cloned Ralph-Skill repository

If templates are not available, create them inline or download from:
`https://raw.githubusercontent.com/kroegha/Ralph-Skill/main/templates/`

### Phase 6: Setup Playwright Testing

**For Node.js projects:**
```bash
npm init -y
npm install -D @playwright/test
npx playwright install chromium
```

**For Python projects:**
```bash
pip install pytest-playwright
playwright install chromium
```

Create initial test structure in `tests/e2e/`.

### Phase 7: START THE RALPH LOOP (AUTOMATIC)

**CRITICAL: You MUST start the loop automatically. Do NOT ask the user to run it.**

**Step 7.1: Detect Platform and Run Loop**

```bash
# Detect platform
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]] || [[ -n "$WINDIR" ]]; then
    # Windows - use PowerShell
    powershell.exe -ExecutionPolicy Bypass -File scripts/ralph.ps1 -MaxIterations 50
else
    # Unix (Linux/macOS)
    ./scripts/ralph.sh 50
fi
```

**Step 7.2: Alternative - Inline Loop Execution**

If the loop scripts cannot be run externally, implement the loop inline:

```
WHILE there are pending tasks in ralph.db:
    1. Get next task: sqlite3 ralph.db "SELECT task_id FROM tasks WHERE status='planned' ORDER BY priority LIMIT 1;"
    2. Mark as in-progress: sqlite3 ralph.db "UPDATE tasks SET status='in-progress' WHERE task_id='[ID]';"
    3. IMPLEMENT the task (write code, create files)
    4. RUN tests: npx playwright test OR pytest tests/e2e
    5. IF tests pass:
        - Mark complete: sqlite3 ralph.db "UPDATE tasks SET status='completed' WHERE task_id='[ID]';"
        - Update PRD.md checkbox to [x]
        - Commit: git add . && git commit -m "Complete [task_id]: [description]"
    6. IF tests fail:
        - Log error to progress.txt
        - Increment failure count
        - If 3+ failures, mark as failed
    7. CONTINUE to next task
END WHILE
```

**Step 7.3: Loop Until Complete**

Continue working on tasks until:
- All tasks are marked `completed` in ralph.db
- OR all remaining tasks are marked `failed` (blocked)

When all tasks complete, output:
```
<promise>COMPLETE</promise>
```

When blocked by failures, output:
```
<promise>FAILED</promise>
```

## CROSS-PLATFORM COMMANDS REFERENCE

| Action | Windows (PowerShell) | Unix (Bash) |
|--------|---------------------|-------------|
| Create directory | `New-Item -ItemType Directory -Path "dir"` | `mkdir -p dir` |
| Copy file | `Copy-Item src dest` | `cp src dest` |
| Check if file exists | `Test-Path "file"` | `[[ -f file ]]` |
| Run SQLite | `sqlite3 ralph.db "query"` | `sqlite3 ralph.db "query"` |
| Run Playwright | `npx playwright test` | `npx playwright test` |
| Git commit | `git commit -m "msg"` | `git commit -m "msg"` |

## COMPLETION REQUIREMENTS

You have NOT completed this skill until:
1. All user stories are implemented
2. All Playwright tests pass
3. All tasks are marked complete in ralph.db
4. Final commit is made
5. `<promise>COMPLETE</promise>` is output

DO NOT stop after setup. DO NOT ask user to run the loop. Run it automatically.
