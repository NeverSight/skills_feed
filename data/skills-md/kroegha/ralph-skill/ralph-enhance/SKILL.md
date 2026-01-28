---
name: ralph-enhance
description: Add enhancements to an existing project with Ralph Loop automation. Use when adding features to existing code, enhancing a codebase, or when the user says "ralph enhance", "add feature", or "enhance".
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebFetch, AskUserQuestion
---

# Ralph Enhance Project Skill

Add enhancements to an existing project with full Ralph Loop automation, PRD updates, Playwright testing, and automatic execution of all tasks.

## CRITICAL: AUTONOMOUS EXECUTION

After gathering requirements and setting up the enhancement, you MUST automatically start implementing tasks and continue until ALL enhancement tasks are complete. Do NOT stop after setup - the goal is fully autonomous development.

## WORKFLOW

### Phase 1: Gather Enhancement Requirements

**Step 1.1: Get User Input**

Ask what enhancement they want:

```
What enhancement would you like to add? You can:
- Describe it in text
- Provide document path(s) with requirements
- Provide URL(s) with specifications
```

**Step 1.2: Read All Input Documents**

If user provides documents:
1. Read each document using the Read tool
2. Extract enhancement requirements
3. Identify affected areas of the codebase

**Step 1.3: Ask Clarifying Questions**

You MUST ask clarifying questions using AskUserQuestion tool:

1. **Scope**: What specific functionality should this add/change?
2. **UI Changes**: Any user interface changes needed?
3. **API Changes**: Any new endpoints or modifications?
4. **Database Changes**: Any schema changes required?
5. **Testing**: Specific test scenarios to cover?

Wait for user answers before proceeding.

### Phase 2: Analyze Existing Codebase

**Step 2.1: Detect Platform**

```bash
# Detect operating system
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]] || [[ -n "$WINDIR" ]]; then
    PLATFORM="windows"
else
    PLATFORM="unix"
fi
```

**Step 2.2: Discover Project Structure**

```bash
# Find project files
find . -type f \( -name "*.py" -o -name "*.ts" -o -name "*.js" \) | head -50
ls -la
```

Read package.json, pyproject.toml, or other config files to understand the stack.

**Step 2.3: Identify Tech Stack**

Determine:
- Programming language
- Framework (Express, FastAPI, Next.js, etc.)
- Database (if any)
- Testing framework
- Project conventions

**Step 2.4: Check for Existing Ralph Setup**

```bash
# Check for existing Ralph files
ls PRD.md ralph.db scripts/ralph*.sh dashboard.html 2>/dev/null
```

If Ralph is NOT set up:
- Initialize ralph.db with schema
- Create PRD.md if missing
- Copy loop scripts from Ralph-Skill installation
- Copy dashboard.html for web visualization

**Copy required files if missing:**

**Unix:**
```bash
# Copy from personal skills location
RALPH_PATH=~/.claude/skills/ralph-new
cp $RALPH_PATH/../../../templates/schema.sql templates/ 2>/dev/null
cp $RALPH_PATH/../../../scripts/ralph*.sh scripts/ 2>/dev/null
cp $RALPH_PATH/../../../templates/dashboard.html . 2>/dev/null
chmod +x scripts/*.sh 2>/dev/null
```

**Windows:**
```powershell
$ralphPath = "$env:USERPROFILE\.claude\skills\ralph-new"
Copy-Item "$ralphPath\..\..\..\templates\schema.sql" templates\ -ErrorAction SilentlyContinue
Copy-Item "$ralphPath\..\..\..\scripts\ralph*.ps1" scripts\ -ErrorAction SilentlyContinue
Copy-Item "$ralphPath\..\..\..\templates\dashboard.html" . -ErrorAction SilentlyContinue
```

If files not found locally, download from GitHub:
```bash
curl -sO https://raw.githubusercontent.com/kroegha/Ralph-Skill/main/templates/dashboard.html
curl -sO https://raw.githubusercontent.com/kroegha/Ralph-Skill/main/templates/schema.sql
```

**Step 2.5: Read Existing PRD**

```bash
cat PRD.md 2>/dev/null
```

Note the highest US-XXX number for new stories.

### Phase 3: Fetch Relevant Documentation

Fetch Context7 documentation for technologies relevant to the enhancement.

### Phase 4: Create Enhancement Document

**Step 4.1: Create Enhancement Doc**

```bash
mkdir -p docs/enhancements
```

Create `docs/enhancements/ENH-XXX.md`:

```markdown
# Enhancement: [Title]

## Overview
[Brief description]

## Requirements
[From user input]

## Technical Approach
[How to implement]

## Affected Files
- [Files to modify]
- [New files to create]

## Testing Strategy
- Unit tests: [what]
- E2E tests: [Playwright scenarios]
```

### Phase 5: Generate User Stories

**Step 5.1: Create Task Breakdown**

Break enhancement into user stories. Each MUST:
- Be completable in ONE context window (~10 min)
- Have clear acceptance criteria
- Include Playwright test steps

**Step 5.2: Update PRD.md**

Append new user stories:

```markdown
---

## Enhancement: ENH-XXX - [Title]

### US-XXX: [Story Title]
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

### Phase 6: Update Database

**Step 6.1: Add Tasks to Database**

For each new user story:

```bash
sqlite3 ralph.db "INSERT INTO tasks (task_id, name, type, status) VALUES ('US-XXX', 'Story title', 'enhancement', 'planned');"
```

**Step 6.2: Verify Database**

```bash
sqlite3 ralph.db "SELECT task_id, name, status FROM tasks WHERE status='planned';"
```

### Phase 7: Setup Testing for Enhancement

Create Playwright test file:

**For Node.js:**
```typescript
// tests/e2e/enh-xxx.spec.ts
import { test, expect } from '@playwright/test';

test.describe('ENH-XXX: [Title]', () => {
  test('US-XXX: [Story]', async ({ page }) => {
    // Test implementation
  });
});
```

**For Python:**
```python
# tests/e2e/test_enh_xxx.py
from playwright.sync_api import Page, expect

def test_us_xxx_story(page: Page):
    # Test implementation
    pass
```

### Phase 8: START THE RALPH LOOP (AUTOMATIC)

**CRITICAL: You MUST start implementing tasks automatically. Do NOT ask the user to run the loop.**

**Step 8.1: Implement the Inline Loop**

Execute this loop until all enhancement tasks are complete:

```
WHILE there are pending enhancement tasks in ralph.db:
    1. Get next task:
       TASK_ID=$(sqlite3 ralph.db "SELECT task_id FROM tasks WHERE status='planned' AND type='enhancement' ORDER BY priority LIMIT 1;")

    2. If no task, check for in-progress:
       TASK_ID=$(sqlite3 ralph.db "SELECT task_id FROM tasks WHERE status='in-progress' ORDER BY started_at LIMIT 1;")

    3. If still no task, ALL DONE - exit loop

    4. Mark as in-progress:
       sqlite3 ralph.db "UPDATE tasks SET status='in-progress', started_at=CURRENT_TIMESTAMP WHERE task_id='$TASK_ID';"

    5. Read task details from PRD.md

    6. IMPLEMENT the task:
       - Write/modify code files
       - Follow existing project patterns
       - Create/update tests

    7. RUN tests:
       # Node.js
       npx playwright test tests/e2e/enh-xxx.spec.ts
       # OR Python
       pytest tests/e2e/test_enh_xxx.py

    8. IF tests pass:
       - sqlite3 ralph.db "UPDATE tasks SET status='completed', completed_at=CURRENT_TIMESTAMP WHERE task_id='$TASK_ID';"
       - Update PRD.md: change [ ] to [x] for this task
       - git add . && git commit -m "Complete $TASK_ID: [description]"

    9. IF tests fail:
       - Append error to progress.txt with learnings
       - sqlite3 ralph.db "UPDATE tasks SET iteration_count=iteration_count+1 WHERE task_id='$TASK_ID';"
       - Check failure count:
         FAILURES=$(sqlite3 ralph.db "SELECT iteration_count FROM tasks WHERE task_id='$TASK_ID';")
         if [ $FAILURES -ge 3 ]; then
           sqlite3 ralph.db "UPDATE tasks SET status='failed' WHERE task_id='$TASK_ID';"
         fi
       - Try different approach on next iteration

    10. CONTINUE to next task
END WHILE
```

**Step 8.2: Platform-Specific Commands**

**Windows (PowerShell):**
```powershell
$taskId = sqlite3 ralph.db "SELECT task_id FROM tasks WHERE status='planned' ORDER BY priority LIMIT 1;"
sqlite3 ralph.db "UPDATE tasks SET status='in-progress' WHERE task_id='$taskId';"
npx playwright test
git add . ; git commit -m "Complete ${taskId}"
```

**Unix (Bash):**
```bash
TASK_ID=$(sqlite3 ralph.db "SELECT task_id FROM tasks WHERE status='planned' ORDER BY priority LIMIT 1;")
sqlite3 ralph.db "UPDATE tasks SET status='in-progress' WHERE task_id='$TASK_ID';"
npx playwright test
git add . && git commit -m "Complete $TASK_ID"
```

**Step 8.3: Loop Until Complete**

Continue until:
- All enhancement tasks are `completed`
- OR remaining tasks are `failed` (blocked)

When complete, output:
```
<promise>COMPLETE</promise>
```

When blocked, output:
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
1. All enhancement user stories are implemented
2. All Playwright tests pass
3. All enhancement tasks are marked complete in ralph.db
4. Final commit is made
5. `<promise>COMPLETE</promise>` is output

DO NOT stop after setup. DO NOT ask user to run the loop. Implement everything automatically.
