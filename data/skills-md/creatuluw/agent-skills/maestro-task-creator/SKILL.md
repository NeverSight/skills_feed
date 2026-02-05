---
name: maestro-task-creator
description: Create Auto Run task documents for Maestro with markdown checklists. Use when user wants to create tasks/playbooks for automated execution, needs help structuring work into task documents, or asks to "create maestro tasks", "make a playbook", "break down into tasks", "plan auto run workflow".
---

# Maestro Task Creator

## Goals

Create well-structured Auto Run task documents for Maestro that enable:
- **Spec-driven execution**: Clear, actionable task checklists that AI agents can execute independently
- **Session isolation**: Tasks designed for clean context in fresh AI sessions
- **Iterative refinement**: Documents that can be reviewed, updated, and re-run
- **Progress tracking**: Checkboxes that mark completion state for each task

## Permissions

**Required:**
- File system read/write access to Auto Run document folder
- Write access to `images/` subfolder for task attachments

**Scope:**
- Can create markdown task documents (.md files)
- Can create images/ subfolder for attachments
- Cannot modify files outside Auto Run folder
- Cannot access sensitive configuration or system files

## Tool Usage

**Required Tools:**
- `read_file` - Examine existing task documents for patterns
- `edit_file` - Create or modify task documents
- `create_directory` - Create images/ subfolder when needed
- `terminal` - For file system operations if needed

**Command Patterns:**
```bash
# Read existing patterns
read_file <path-to-existing-tasks.md>

# Create new task document
edit_file -path <new-task.md> -mode create

# Create images directory
create_directory images/
```

**Tool Call Sequence:**
1. Read existing task documents (if available) to understand patterns
2. Discuss requirements with user (brainstorm questions one at a time)
3. Break down work into tasks
4. Create markdown document with checklist format
5. Review with user before finalizing

## Triggers

Use this skill when the user:
- Requests to "create maestro tasks", "make a playbook", or "set up auto run"
- Mentions "task breakdown", "work decomposition", or "planning tasks"
- Asks to structure work for "automated execution" or "batch processing"
- Wants to "plan", "specify", or "design" work before implementation
- References "Maestro Auto Run", "playbooks", or "checklists"
- Needs help organizing work into "executable tasks" or "actionable steps"

## Acceptance Criteria

1. **Task Executability**: Each task in the checklist is independently executable by an AI agent in a fresh session with sufficient context to complete without ambiguity

2. **Logical Organization**: Tasks follow a logical sequence (e.g., setup → implementation → verification → cleanup) with clear dependencies and no circular references

3. **Context Completeness**: Document provides enough context (project background, file locations, assumptions, success criteria) for an agent to understand what to do without additional clarification

4. **Verification Validated**: Document includes verification tasks that allow the agent to confirm success (e.g., "Run tests", "Verify feature works", "Check for errors")

## Core Instructions

### Step 1: Understand the Work

Discuss the work requirements with the user:
- **Ask one question at a time** to refine understanding
- **Focus on**: scope, constraints, success criteria, dependencies
- **Check existing context**: Read project files, docs, or recent work
- **Clarify**: What needs to be done, what's out of scope, what defines success

**Questions to explore:**
- "What's the overall goal or objective of this work?"
- "Are there any constraints or limitations I should know about?"
- "What files or systems will be involved?"
- "What does success look like? How will we know it's done?"

### Step 2: Plan Task Structure

Break down the work into tasks:
- **Granularity**: Each task should take 5-30 minutes for an AI agent
- **Independence**: Each task should be executable without context from other tasks
- **Dependencies**: Order tasks to satisfy dependencies (setup before implementation)
- **Verification**: Include tasks that verify or test the work

**Common task categories:**
```
- [ ] Setup/Preparation (install, configure, initialize)
- [ ] Implementation (code changes, file modifications)
- [ ] Testing/Verification (run tests, verify behavior)
- [ ] Documentation (update docs, add comments)
- [ ] Cleanup (remove temp files, reset state)
```

### Step 3: Create Task Document

Create markdown document with checklist format:

```markdown
# <Descriptive Title>

## Context
[Brief background: what we're doing and why]

## Tasks
- [ ] Task 1: Description of first task
- [ ] Task 2: Description of second task
- [ ] Task 3: Verify [specific outcome]

## Notes
[Assumptions, constraints, or additional context]
```

**Task writing guidelines:**
- **Action-oriented**: Start with verbs (Implement, Update, Create, Test)
- **Specific**: Include file names, paths, or locations
- **Complete**: Each task is self-contained with enough context
- **Verifiable**: Include how to confirm the task is done

**Examples:**
```markdown
- [ ] Install dependencies: Run `npm install` to install required packages
- [ ] Create auth component: Implement `src/components/Auth.tsx` with login/logout buttons
- [ ] Add unit tests: Write tests for `Auth.tsx` in `src/components/__tests__/Auth.test.tsx`
- [ ] Run tests: Execute `npm test` to verify all tests pass
```

### Step 4: Review and Validate

Review with user before finalizing:
- **Present in sections** (200-300 words) if document is large
- **Ask after each section**: "Does this look right so far?"
- **Check**: Are tasks clear? Dependencies correct? Context sufficient?

**Validation checklist:**
```
[ ] Tasks are independent and executable in isolation
[ ] Task order respects dependencies
[ ] Each task has enough context to be understood
[ ] Verification tasks are included
[ ] No tasks are too large (>30 min) or too small (<2 min)
[ ] Success criteria are clear
```

### Step 5: Save to Auto Run Folder

Save the document to the Maestro Auto Run folder:
- **Location**: Save to `.\.maestro\tasks\` relative to repository root
- **Filename**: Use descriptive name (e.g., `feature-auth.md`, `bugfix-login.md`)
- **Images**: Create `images/` subfolder if attaching screenshots or diagrams
- **Notify user**: After saving, explicitly inform the user of the full file path where the task document was saved

**Example notification:**
```
Task saved to: ./.maestro/tasks/feature-auth.md
You can find this task in your Maestro Auto Run folder.
```

**Example:**
```
.maestro/
└── tasks/
    ├── feature-auth.md
    └── images/
        └── auth-flow.png
```

## Decision Management

### Task Granularity

**When to split a task:**
- Task requires multiple different actions (e.g., "Implement auth and write tests" → split into two)
- Task would take >30 minutes for an AI agent
- Task touches multiple unrelated files or systems

**When to combine tasks:**
- Tasks are trivial (<2 minutes each)
- Tasks are tightly coupled (must be done together)
- Combining improves clarity or reduces redundancy

### Context vs. Minimalism

**Include context when:**
- Task references project-specific files, paths, or conventions
- Task depends on recent changes or decisions
- Success criteria are non-obvious
- Task requires understanding of project architecture

**Keep minimal when:**
- Task is self-contained and obvious (e.g., "Run npm test")
- Context would duplicate information from project README or docs
- Task is part of standard workflow (e.g., "Commit changes")

### Verification Strategy

**When to include verification tasks:**
- After any destructive action (delete files, modify production data)
- After implementation tasks (code changes, feature additions)
- At the end of document (overall verification)

**Types of verification:**
- Automated: Run tests, lint, build, scripts
- Manual: Check UI, verify logs, review files
- Output: Confirm file exists, check file content, verify data

### When to Use Playbooks

**Use a single document when:**
- Work is one-time or rarely repeated
- Tasks are linear and don't need configuration
- Simpler to manage as a single file

**Use a playbook (multiple documents) when:**
- Work has distinct phases that benefit from separation
- Need to reuse document configurations (Reset on Completion)
- Want to loop through documents indefinitely
- Different agents will work on different documents

**Playbook patterns:**
```
# Separate by phase
01-setup.md       (One-time initialization)
02-implement.md   (Main work - can loop)
03-verify.md      (Final verification)

# Separate by agent
frontend-tasks.md (Agent 1)
backend-tasks.md  (Agent 2)

# Separate by concern
code-changes.md   (Implementation)
tests.md          (Testing)
docs.md           (Documentation)
```

## Human Interaction

### When to Request Human Approval

**Required before:**
- Creating documents in unfamiliar or sensitive locations
- Writing tasks that modify production systems or data
- Structuring work with unclear requirements or scope
- Making architectural decisions that affect project structure

**Request format:**
```
I'm ready to create a task document for [work description].
Location: [Auto Run folder path]
Tasks: [number] tasks covering [overview]
Should I proceed? [yes/no/adjust]
```

### When to Request Human Advice

**Recommended for:**
- Unclear task dependencies or ordering
- Ambiguous success criteria or verification methods
- Multiple valid approaches to task breakdown
- Choosing between single document vs. playbook

**Request format:**
```
I have two options for structuring this work:

Option A: Single document with 15 tasks
- Simpler to manage
- All tasks in one place
- Easier to track progress

Option B: Playbook with 3 documents (setup, implement, verify)
- Can loop on implementation document
- Cleaner separation of concerns
- Better for parallel execution

Which approach would you prefer?
```

### When to Request Human Feedback

**Required after:**
- Creating initial task structure (before writing full document)
- Completing document draft (before finalizing)
- Making significant changes based on user feedback

**Request format:**
```
I've drafted a task document with [number] tasks:

[Show high-level summary or first section]

Does this structure look right? [yes/no/adjust]
```

## Limits

### What This Skill Does Not Cover

- **Task execution**: This skill creates tasks, not executes them (use Auto Run for execution)
- **Agent configuration**: Does not configure Maestro agents or providers
- **Scripting**: Does not write automation scripts (use other skills for that)
- **Complex workflows**: For multi-team, multi-system, or highly complex workflows, consider breaking into multiple playbooks

### Anti-Use Cases

Do NOT use this skill for:
- Simple to-do lists without AI execution context
- One-off commands (run directly in terminal instead)
- Human-only workflows (no need for Auto Run structure)
- Tasks requiring shared context across all steps (use a single AI conversation instead)

### Resource Requirements

- **Auto Run folder**: Must be configured in Maestro and accessible
- **Maestro installation**: User must have Maestro installed and configured
- **AI agent access**: At least one AI provider (Claude, Codex, etc.) must be configured

## References

*For detailed examples and patterns, see resources/examples.md*
*For troubleshooting task structure issues, see resources/troubleshooting.md*
*For Maestro documentation, visit https://docs.runmaestro.ai/autorun-playbooks*