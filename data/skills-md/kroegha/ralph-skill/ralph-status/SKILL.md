---
name: ralph-status
description: Display project status dashboard and optionally continue the Ralph Loop. Use when checking progress, viewing status, or when user says "ralph status", "show progress", or "how is it going".
disable-model-invocation: true
allowed-tools: Read, Bash, Glob, Grep, AskUserQuestion
---

# Ralph Status Dashboard Skill

Display project status and offer to continue autonomous development if tasks remain.

## WORKFLOW

### Step 1: Detect Platform

```bash
# Detect operating system
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]] || [[ -n "$WINDIR" ]]; then
    PLATFORM="windows"
else
    PLATFORM="unix"
fi
```

### Step 2: Check Prerequisites

**Unix:**
```bash
sqlite3 --version 2>/dev/null || echo "SQLite not found"
```

**Windows:**
```powershell
sqlite3 --version 2>$null
if (-not $?) { Write-Host "SQLite not found" }
```

If SQLite not available:
```
SQLite is required. Install it:
- Windows: winget install SQLite.SQLite
- macOS: brew install sqlite3
- Linux: sudo apt install sqlite3
```

### Step 3: Locate Database

```bash
# Check for ralph.db
if [[ -f "ralph.db" ]]; then
    echo "Database found"
else
    echo "Database not found"
fi
```

If not found:
```
Ralph database not found.
Run /ralph-new to create a new project, or
Run /ralph-enhance to add features to an existing project.
```

### Step 4: Query Database Status

**Get task counts:**
```bash
PLANNED=$(sqlite3 ralph.db "SELECT COUNT(*) FROM tasks WHERE status='planned';")
IN_PROGRESS=$(sqlite3 ralph.db "SELECT COUNT(*) FROM tasks WHERE status='in-progress';")
COMPLETED=$(sqlite3 ralph.db "SELECT COUNT(*) FROM tasks WHERE status='completed';")
FAILED=$(sqlite3 ralph.db "SELECT COUNT(*) FROM tasks WHERE status='failed';")
TOTAL=$((PLANNED + IN_PROGRESS + COMPLETED + FAILED))
```

**Get current work:**
```bash
sqlite3 ralph.db "SELECT task_id, name, started_at FROM tasks WHERE status='in-progress';"
```

**Get next up:**
```bash
sqlite3 ralph.db "SELECT task_id, name, priority FROM tasks WHERE status='planned' ORDER BY priority, created_at LIMIT 5;"
```

**Get recent activity:**
```bash
sqlite3 ralph.db "SELECT datetime(created_at, 'localtime'), task_id, outcome FROM iterations ORDER BY created_at DESC LIMIT 10;"
```

**Get blockers (3+ failures):**
```bash
sqlite3 ralph.db "SELECT t.task_id, t.name, t.iteration_count FROM tasks t WHERE t.status='failed' OR t.iteration_count >= 3;"
```

### Step 5: Display Dashboard

```
╔══════════════════════════════════════════════════════════════════╗
║                     RALPH PROJECT STATUS                          ║
║                     [Project Name]                                 ║
╠══════════════════════════════════════════════════════════════════╣

TASK SUMMARY
────────────────────────────────────────────────────────────────────
  ● In Progress:  [N]
  ○ Planned:      [N]
  ✓ Completed:    [N]
  ✗ Failed:       [N]
  ─────────────────
    Total:        [N]

PROGRESS
────────────────────────────────────────────────────────────────────
  [████████████████████░░░░░░░░░░] [XX]% Complete

  Iterations: [N] total | [N] success | [N] failed
  Success Rate: [XX]%

CURRENTLY WORKING ON
────────────────────────────────────────────────────────────────────
  🔄 [US-XXX]: [Task name]
     Started: [timestamp] | Iterations: [N]

NEXT UP
────────────────────────────────────────────────────────────────────
  1. [US-XXX]: [Task name]    Priority: [N]
  2. [US-XXX]: [Task name]    Priority: [N]

BLOCKERS (if any)
────────────────────────────────────────────────────────────────────
  ⚠️  [US-XXX]: [Task name] - Failed [N] times

╚══════════════════════════════════════════════════════════════════╝
```

### Step 6: Offer Options

If there are pending or in-progress tasks, ask:

```
Tasks remaining: [N] planned, [N] in-progress

Would you like to:
A) Continue development (run Ralph Loop automatically)
B) View web dashboard (Kanban board)
C) Exit (status only)
```

Use AskUserQuestion tool for this.

### Step 7: Handle User Choice

**If A) Continue development:**

Automatically start the Ralph Loop inline:

```
WHILE there are pending tasks:
    1. Get next task from database
    2. Mark as in-progress
    3. Implement the task
    4. Run Playwright tests
    5. If pass: mark complete, commit
    6. If fail: log learnings, increment failure count
    7. Continue to next task
END WHILE
```

When complete, output:
```
<promise>COMPLETE</promise>
```

**If B) View web dashboard:**

Generate dashboard data and start HTTP server:

**Unix:**
```bash
# Generate dashboard JSON
./scripts/ralph-db.sh dashboard

# Start HTTP server (runs in background)
echo "Starting HTTP server on port 8080..."
python3 -m http.server 8080 &
SERVER_PID=$!

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  Dashboard running at: http://localhost:8080/dashboard.html"
echo "  Press Ctrl+C to stop the server"
echo "═══════════════════════════════════════════════════════"
```

**Windows:**
```powershell
# Generate dashboard JSON
.\scripts\ralph-db.ps1 dashboard

# Start HTTP server
Write-Host ""
Write-Host "Starting HTTP server on port 8080..."
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════"
Write-Host "  Dashboard running at: http://localhost:8080/dashboard.html"
Write-Host "  Press Ctrl+C to stop the server"
Write-Host "═══════════════════════════════════════════════════════"
python -m http.server 8080
```

After starting the server, open `http://localhost:8080/dashboard.html` in the browser.

**If C) Exit:**
Just show status, no further action.

### Step 8: If All Complete

If all tasks are completed:

```
🎉 ALL TASKS COMPLETE!

Summary:
- Total tasks: [N]
- Completed: [N]
- Failed: [N]
- Success rate: [XX]%

Final verification recommended:
- Run full test suite
- Review git log
- Check for any cleanup needed
```

Output:
```
<promise>COMPLETE</promise>
```

## CROSS-PLATFORM COMMANDS

| Action | Windows (PowerShell) | Unix (Bash) |
|--------|---------------------|-------------|
| Check file exists | `Test-Path "file"` | `[[ -f file ]]` |
| Run SQLite | `sqlite3 ralph.db "query"` | `sqlite3 ralph.db "query"` |
| Run dashboard script | `.\scripts\ralph-db.ps1 dashboard` | `./scripts/ralph-db.sh dashboard` |
| Count in variable | `$count = sqlite3 ...` | `COUNT=$(sqlite3 ...)` |

## QUICK COMMANDS REFERENCE

```bash
# View CLI status
./scripts/ralph-db.sh status      # Unix
.\scripts\ralph-db.ps1 status     # Windows

# List all tasks
./scripts/ralph-db.sh list

# List by status
./scripts/ralph-db.sh list planned
./scripts/ralph-db.sh list failed

# View recent activity
./scripts/ralph-db.sh log

# Generate web dashboard
./scripts/ralph-db.sh dashboard
```

## WEB DASHBOARD FEATURES

The dashboard.html provides:
- 4-column Kanban board: Planned → In Progress → Done → Failed
- Auto-refresh every 5 seconds
- Manual refresh button
- Light/Dark mode toggle
- Progress bar and statistics
- Task cards with details
