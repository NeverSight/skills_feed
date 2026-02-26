---
name: implement
description: Implement tasks from docs/task/*.md. Reads the task document, follows implementation steps, and updates status in TASKS.md. Use "/implement auto {task}" to auto-chain through test → document → ship. Use "/implement -m 1 2 3" for multi-task parallel execution.
model: opus
---

# /implement - Implementation Agent

> **Model:** opus (complex coding requires advanced reasoning)

## Command Flags

| Flag | Short | Description |
|------|-------|-------------|
| `--help` | `-h` | Show available commands and options |
| `--version` | `-v` | Show workflow skills version |
| `--multi` | `-m` | Multi-task mode: spawn parallel agents |
| `auto` | | Enable auto-chain (test → document → ship) |

### Flag Handling

**On `-h` or `--help`:**
```
/implement - Implementation Agent

Usage:
  /implement {ID}                    Implement a single task
  /implement auto {ID}               Implement with auto-chain enabled
  /implement -m {ID1} {ID2} ...      Implement multiple tasks in parallel
  /implement auto -m {ID1} {ID2}     Multi-task with auto-chain
  /implement -h, --help              Show this help message
  /implement -v, --version           Show version

Arguments:
  {ID}    Task ID (number) or task filename (e.g., 001-auth-jwt)

Options:
  auto    After implementation, automatically chain through:
          test → document → ship
  -m      Spawn parallel agents for each task

Examples:
  /implement 1                       # Implement task #1
  /implement 001-auth-jwt            # Using task filename
  /implement auto 1                  # With auto-chain
  /implement -m 1 2 3                # Three tasks in parallel

Next: /test {ID}
```

**On `-v` or `--version`:**
Display:
```
Workflow Skills v1.4.1
https://github.com/eljun/claude-skills
```

---

## When to Use

Invoke `/implement {ID}` when:
- A task document exists in `docs/task/`
- Task is in "Planned" status in TASKS.md
- Ready to start coding

**Example:** `/implement 1` or `/implement 001-dashboard-redesign`

## Invocation Options

| Command | Mode | Behavior |
|---------|------|----------|
| `/implement {ID}` | Manual | Implement single task, then notify user to run `/test` |
| `/implement auto {ID}` | Automated | Implement, then auto-chain through test → document → ship |
| `/implement -m {ID1} {ID2} ...` | Multi-task | Spawn parallel agents for each task |
| `/implement --multi {ID1} {ID2}` | Multi-task | Same as `-m` |
| `/implement auto -m {ID1} {ID2}` | Multi + Auto | Parallel tasks with auto-chain |

### Task ID Resolution

The `{ID}` can be:
- **Numeric ID:** `1`, `2`, `3` → Looks up in TASKS.md, finds matching task document
- **Padded ID:** `001`, `002` → Same as numeric
- **Full filename:** `001-dashboard-redesign` → Direct file reference

**Resolution process:**
1. If numeric → Read TASKS.md, find row with matching ID, get task doc path
2. If filename → Look for `docs/task/{filename}.md` directly

### Auto Mode

When invoked with `auto`, the implement skill:
1. Sets `Automation: auto` in the task document (overrides any existing value)
2. Implements the task as normal
3. After completion, automatically spawns `/test {ID}` (haiku)
4. The pipeline continues: test → document → ship

This lets you skip `/task auto` and trigger the full pipeline from implement:
```
/implement auto {ID} → implement code
    ↓
/test (haiku)
    │
PASS → /document → /ship → PR + notify
FAIL → /implement (with test report) → retry
```

### Multi-Task Mode

When invoked with `-m` or `--multi`, the implement skill spawns parallel agents:

```
/implement -m 1 2 3
       │
       ├── Validate all tasks exist in TASKS.md
       ├── Check for file overlap warnings
       │
       └── Spawn in parallel (using Task tool):
           ├── Agent-1: /implement 1
           ├── Agent-2: /implement 2
           └── Agent-3: /implement 3
       │
       └── Wait for all agents to complete
       └── Report combined status
```

**Multi-task with auto mode:**
```
/implement auto -m 1 2 3
```
Each spawned agent runs with auto mode, chaining to test → document → ship.

#### Pre-Flight Checks for Multi-Task

**CRITICAL:** Background agents cannot prompt for permissions interactively. You MUST complete all checks and get user approval BEFORE spawning agents.

##### Step 1: Validate Tasks Exist
```
✓ Task 1: 001-auth-jwt.md (found)
✓ Task 2: 002-fix-portal.md (found)
✗ Task 3: Not found in TASKS.md → STOP if any missing
```

##### Step 2: Check for File Overlap
Read each task's "File Changes" section:
```
⚠️ Warning: Tasks 1 and 2 both modify src/auth/middleware.ts

Options:
1. Continue anyway (may need manual conflict resolution)
2. Run sequentially instead
3. Cancel
```

##### Step 3: Check Dependencies
```
⚠️ Task 2 is blocked by Task 1
Recommendation: Run sequentially or resolve dependency first
```

##### Step 4: Scan for Dangerous Operations

Read each task document and scan for these keywords:

| Keywords Found | Risk Level | Action |
|----------------|------------|--------|
| `migration`, `schema`, `ALTER TABLE`, `prisma migrate` | ⚠️ Database | Require explicit approval |
| `rm `, `delete file`, `remove`, `unlink` | 🚫 Deletion | Block - user must do manually |
| `DROP`, `TRUNCATE`, `DELETE FROM` (without WHERE) | 🚫 Data loss | Block - user must do manually |
| `--force`, `reset --hard`, `-rf` | 🚫 Destructive | Block |
| `API_KEY`, `SECRET`, `password`, `credential` | ⚠️ Sensitive | Warn user |
| `sudo`, `chmod 777`, `chown` | 🚫 System | Block |

##### Step 5: Permission Approval (REQUIRED)

**Display this prompt and WAIT for user confirmation:**

```
═══════════════════════════════════════════════════════════════
MULTI-TASK PERMISSION CHECK
═══════════════════════════════════════════════════════════════

Tasks to implement in parallel:
  #1 {Task 1 name}
  #2 {Task 2 name}
  #3 {Task 3 name}

PERMISSIONS FOR BACKGROUND AGENTS
───────────────────────────────────────────────────────────────
✅ GRANTED (safe operations):
   • Read, Edit, Write files
   • Glob, Grep (search)
   • Git: add, commit, status, diff, checkout -b, log
   • npm/npx: install, run, build, test, lint

⚠️ REQUIRES APPROVAL (detected in tasks):
   • {e.g., "Database migration in Task #2"}
   • {e.g., "Schema changes in Task #1"}
   • (None detected)

🚫 BLOCKED (agents will stop if needed):
   • File deletion (rm, unlink, rimraf)
   • Destructive git (push --force, reset --hard, clean -f)
   • Database destruction (DROP, TRUNCATE)
   • System commands (sudo, chmod)

───────────────────────────────────────────────────────────────
If agents encounter blocked operations, they will STOP and
report back. You can then perform those manually.
═══════════════════════════════════════════════════════════════

Approve and start parallel implementation? (yes/no)
```

**DO NOT spawn agents until user types "yes" or confirms.**

##### Step 6: Spawn Agents with Pre-Authorized Tools

Only after user approval, spawn agents with these allowed tools:

```
Task({
  subagent_type: "general-purpose",
  model: "opus",
  prompt: "/implement {ID}",
  run_in_background: true,
  allowed_tools: [
    "Read",
    "Edit",
    "Write",
    "Glob",
    "Grep",
    "Bash(git add *)",
    "Bash(git commit *)",
    "Bash(git status)",
    "Bash(git diff *)",
    "Bash(git checkout -b *)",
    "Bash(git log *)",
    "Bash(npm install *)",
    "Bash(npm run *)",
    "Bash(npx *)"
  ]
})
```

**Note:** Dangerous operations are NOT in allowed_tools, so agents physically cannot perform them.

## Workflow

```
/implement [auto] [-m] {ID} [{ID2} ...]
       ↓
1. Parse arguments: detect "auto" flag, "-m/--multi" flag, task ID(s)
2. If multi-task → Run pre-flight checks, spawn parallel agents, exit
3. Resolve task ID → find docs/task/{ID}-{name}.md
4. Read task document
5. If "auto" flag → set Automation: auto in task doc
6. Check Automation field (manual | auto)
7. Move task to "## In Progress" in TASKS.md
8. ⚠️ MANDATORY: Invoke specialized skills (see Step 2 below)
   └── /vercel-react-best-practices (if installed + React code)
   └── /supabase-postgres-best-practices (if installed + DB code)
9. Implement following task document steps
10. Commit with [task-{ID}] prefix for traceability
11. Update status to "TESTING" when complete
       ↓
┌─── Automation Mode? ───┐
│                        │
▼ Manual                 ▼ Auto
Notify user              Invoke /test {ID}
Ready for /test
```

**⚠️ GUARDRAIL:** Step 8 is NOT optional. If specialized skills are installed and relevant to the task, they MUST be invoked BEFORE writing any code. See "Step 2: Invoke Specialized Skills" below for details.

## Auto Mode Behavior

When invoked with `/implement auto {ID}` OR task document has `Automation: auto`:

1. If invoked with `auto` argument, update the task document to set `Automation: auto`
2. After implementation completes, automatically invoke `/test {ID}`

## Pre-Implementation Checklist

Before writing ANY code:

### 0. Parse Arguments

Check for flags and task ID(s):
- `-m` or `--multi` → Multi-task mode (spawn parallel agents)
- `auto` → Set automation mode
- Remaining args → Task ID(s)

**Examples:**
- `/implement 1` → Single task, manual mode
- `/implement auto 1` → Single task, auto mode
- `/implement -m 1 2 3` → Multi-task, manual mode
- `/implement auto -m 1 2` → Multi-task, auto mode

If `auto` is detected, update the task document header:
```markdown
> **Automation:** auto
```

### 1. Resolve Task ID

Convert the task ID to the task document path:

1. Read TASKS.md
2. Find the row with matching ID in the first column
3. Get the task doc path from that row
4. Verify the file exists in `docs/task/`

**Example:**
```
Input: /implement 1
TASKS.md row: | 1 | Dashboard Redesign | HIGH | [001-dashboard-redesign.md](...) |
Resolved: docs/task/001-dashboard-redesign.md
```

### 2. Read the Task Document (Primary Context Source)
```
docs/task/{ID}-{task-name}.md
```

**IMPORTANT — Context Efficiency:**
The task document was created by the `/task` agent, which already performed a thorough codebase analysis. The task document contains all the context you need: requirements, file paths, implementation steps, and architectural decisions.

- **DO** trust the task document as your primary source of truth
- **DO** read the specific files listed in the task document's "Files to Modify" or implementation steps
- **DO NOT** perform broad codebase exploration (scanning directories, reading unrelated files, trying to "understand the entire codebase")
- **DO NOT** re-analyze architecture that the plan agent already documented

If the task document references specific files, read only those files. This keeps your context window efficient and avoids redundant exploration.

Understand:
- Task ID (for commit messages)
- Requirements (must have vs nice to have)
- Proposed solution
- File changes needed
- Implementation steps

### 3. Invoke Specialized Skills (MANDATORY - DO NOT SKIP)

**CRITICAL GUARDRAIL:** Before writing ANY code, you MUST check for and invoke specialized skills. This is NOT optional.

#### Step 3a: Detect Installed Skills

Check if these skills are available by looking for them in the available skills/tools:

| Skill | Detection | Invoke When |
|-------|-----------|-------------|
| `/vercel-react-best-practices` | Skill is listed in available tools | ANY React/Next.js/TypeScript code |
| `/supabase-postgres-best-practices` | Skill is listed in available tools | ANY database queries, RLS, schema, Supabase code |

#### Step 3b: Invoke BEFORE Writing Code

**If skill is detected → MUST invoke it FIRST, before writing any code.**

```
# For React/Next.js projects:
/vercel-react-best-practices

# For Supabase/PostgreSQL projects:
/supabase-postgres-best-practices
```

#### Step 3c: Verification Checklist

Before proceeding to Step 4, confirm:

- [ ] Checked if `/vercel-react-best-practices` is available
- [ ] If available AND task involves React/Next.js → Invoked it
- [ ] Checked if `/supabase-postgres-best-practices` is available
- [ ] If available AND task involves database → Invoked it

#### HARD STOP - Do NOT Proceed If:

```
⛔ STOP: You detected a specialized skill is installed but did not invoke it.

This is a guardrail violation. You MUST:
1. Invoke the skill NOW before writing any code
2. Apply the best practices from the skill to your implementation
3. Only then proceed to Step 3

Skipping specialized skills leads to:
- Suboptimal code patterns
- Performance issues
- Security vulnerabilities
- Technical debt
```

> **Why this matters:** These skills contain critical best practices from Vercel and Supabase engineers. Skipping them means writing code that may have performance issues, security vulnerabilities, or anti-patterns that will need to be fixed later.

### 4. Update TASKS.md

Move task from "Planned" to "In Progress":

```markdown
## In Progress

| ID | Task | Started | Task Doc | Status |
|----|------|---------|----------|--------|
| 1 | Quick Actions Redesign | Jan 25 | [001-quick-actions.md](docs/task/001-quick-actions.md) | Implementing |
```

### 5. Verify Dependencies

Check that all prerequisites exist:
- Required API endpoints
- Required types/interfaces
- Required packages installed
- No blocking tasks

---

## Commit Convention

**IMPORTANT:** All commits must include the task ID prefix for traceability.

### Format
```
[task-{ID}] {type}: {description}

{optional body}

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

### Examples
```bash
# Feature commit
git commit -m "[task-1] feat: Add JWT authentication middleware

Implements token validation and refresh logic.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"

# Fix commit
git commit -m "[task-2] fix: Resolve portal login redirect issue

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

### Why This Matters

The `[task-{ID}]` prefix enables:
1. **Traceability:** Easy to see which commits belong to which task
2. **Multi-task support:** When multiple agents work in parallel, `/ship` can identify task-specific changes
3. **Filtering:** `git log --grep="\[task-1\]"` shows all commits for task 1
4. **PR generation:** `/ship` can create accurate PR descriptions

---

## Implementation Guidelines

### Follow the Task Document

The task document is your spec. Follow it step by step:

1. **Step 1** → Complete → Verify
2. **Step 2** → Complete → Verify
3. Continue until all steps done

### Invoke Skills When Applicable (MUST Use If Installed)

| Situation | Skill (Required If Installed) |
|-----------|-------------------------------|
| React/Next.js code | `/vercel-react-best-practices` |
| Database work | `/supabase-postgres-best-practices` |
| Need clarification | Ask user |

### Quality Standards

- No `any` types - use proper TypeScript types
- All hooks before early returns
- AbortController in useEffect with fetches
- Clean, readable code
- Handle loading/error/empty states

### Track Progress

Update the task document as you go:
- Check off completed requirements
- Note any deviations from plan
- Document blockers encountered

---

## Common Implementation Patterns

### Creating New Files

```typescript
// 1. Create the file
// 2. Add to index exports if needed
// 3. Import where used
```

### Modifying Existing Files

```typescript
// 1. Read the file first (always!)
// 2. Understand existing patterns
// 3. Make minimal, focused changes
// 4. Don't refactor unrelated code
```

### Web Development

- Check project's CLAUDE.md for patterns
- Follow existing code patterns
- Use proper authentication
- Use ORM for database queries, not raw SQL

---

## Completion Checklist

Before marking as ready for testing:

### Code Quality
- [ ] Code compiles without errors
- [ ] No TypeScript errors
- [ ] Follows existing patterns
- [ ] No unnecessary complexity

### Functionality
- [ ] All "Must Have" requirements implemented
- [ ] Happy path works
- [ ] Loading states handled
- [ ] Error states handled
- [ ] Empty states handled

### Task Document
- [ ] Requirements checked off
- [ ] Any deviations documented
- [ ] Notes added for tester

---

## Update Status to TESTING

When implementation is complete:

### 1. Update TASKS.md

Move to "Testing" section:

```markdown
## Testing

| ID | Task | Task Doc | Test Report | Status |
|----|------|----------|-------------|--------|
| 1 | Quick Actions Redesign | [001-quick-actions.md](docs/task/001-quick-actions.md) | Pending | Ready for test |
```

### 2. Update Task Document

Add completion notes:

```markdown
> **Status:** TESTING
> **Completed:** {Date}
> **Implementation Notes:** {Any important notes for tester}
```

### 3. Pre-Completion Verification (REQUIRED)

**Before marking implementation complete, verify:**

```
┌─────────────────────────────────────────────────────────────┐
│ ⚠️ SPECIALIZED SKILLS VERIFICATION                          │
├─────────────────────────────────────────────────────────────┤
│ □ Did task involve React/Next.js code?                      │
│   → If YES: Did you invoke /vercel-react-best-practices?    │
│                                                             │
│ □ Did task involve database/Supabase code?                  │
│   → If YES: Did you invoke /supabase-postgres-best-practices│
│                                                             │
│ □ If skill was available but NOT invoked:                   │
│   → STOP. Go back and invoke it. Apply best practices.      │
│   → Then return here to complete.                           │
└─────────────────────────────────────────────────────────────┘
```

**If you skipped a specialized skill:** You must go back, invoke it, review your code against the best practices, and make any necessary corrections before proceeding.

### 4. Inform User / Chain to Next Skill

**Check the task document for `Automation: auto` field.**

#### Manual Mode (or if Automation field is missing)
```
Implementation complete for: #{ID} - {Task Title}

Files changed:
- path/to/file1.tsx (created)
- path/to/file2.tsx (modified)

Commits made:
- [task-{ID}] feat: Add authentication middleware
- [task-{ID}] feat: Add token refresh logic

Next Steps:
  /test {ID}              # e.g., /test 1
  /test {ID}-{task-name}  # e.g., /test 001-auth-jwt
```

#### Auto Mode
```
Implementation complete for: #{ID} - {Task Title}

Files changed:
- path/to/file1.tsx (created)
- path/to/file2.tsx (modified)

[AUTO] Spawning /test with haiku model...
```
Use Task tool to spawn test agent with **model: haiku**:
`Task({ subagent_type: "general-purpose", model: "haiku", prompt: "/test {ID}" })`

#### Multi-Task Completion

When all parallel agents complete:
```
Multi-task implementation complete!

Results:
├── Task #1: ✓ Complete (3 commits)
├── Task #2: ✓ Complete (2 commits)
└── Task #3: ✗ Failed (blocked by missing API)

Next Steps (for successful tasks):
  /test 1                  # Test task #1
  /test 2                  # Test task #2
  /test 001-auth-jwt       # Using task name

Failed task requires attention:
  Task #3: See docs/task/003-feature-name.md for blocker details
```

---

## Handling Issues

### Blocked by Missing Dependency

1. Document the blocker in task document
2. Update TASKS.md status to "Blocked"
3. Inform user with specific blocker details
4. Create sub-task if needed via `/task`

### Requirement Unclear

1. Ask user for clarification
2. Update task document with clarified requirements
3. Continue implementation

### Scope Creep

1. Stick to task document scope
2. Note additional ideas in "Nice to Have" or separate task
3. Don't expand scope without user approval

---

## Specialized Skills (MANDATORY When Installed)

These plugins must be installed separately. **Once installed, invocation is MANDATORY — not optional.**

| Plugin | Install From | When to Invoke |
|--------|--------------|----------------|
| `vercel-react-best-practices` | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | ANY React/Next.js/TypeScript code |
| `supabase-postgres-best-practices` | [supabase/agent-skills](https://github.com/supabase/agent-skills) | ANY database queries, RLS, schema, Supabase code |

### Enforcement Summary

```
┌────────────────────────────────────────────────────────────────┐
│ SPECIALIZED SKILLS ARE NOT OPTIONAL ONCE INSTALLED             │
├────────────────────────────────────────────────────────────────┤
│ 1. BEFORE writing code → Check if skills are available         │
│ 2. IF available AND relevant → INVOKE immediately              │
│ 3. APPLY best practices to your implementation                 │
│ 4. BEFORE completing → Verify you invoked required skills      │
│ 5. IF skipped → Go back, invoke, review code, fix issues       │
└────────────────────────────────────────────────────────────────┘
```

Failure to invoke specialized skills when available leads to:
- Code that violates best practices
- Performance issues that need fixing later
- Security vulnerabilities
- Technical debt and rework
