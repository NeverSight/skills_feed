---
name: todo-task-run
description: Execute tasks from TODO file - Generic task runner [/todo-task-run xxx]
argument-hint: <file_path>
arguments:
  - name: file_path
    description: Path to the TODO file to execute
    required: true
user-invocable: true
---

**Target TODO file**: $ARGUMENTS

## Usage

```
/todo-task-run <file_path>
```

### Arguments
- `file_path` (required): Path to the TODO file to execute

## 📋 Development Rules

### 🚨 Guardrails (Prohibited Actions)

**CRITICAL - Forward-Only Policy:**
- ❌ **NEVER use `git reset`, `git restore`, `git revert`, or any rollback commands**
- ✅ **Always move forward**: Fix errors with new changes, not by undoing previous ones

### Task Completion Procedure

**IMPORTANT**: When completing a task, be sure to follow these steps:

1. **Update checkbox immediately after task execution** - Change `- [ ]` to `- [x]` to mark completion
2. **Document related files** - List names of created/modified files

## 📚 Reference Documentation

- [todo-task-planning skill](../todo-task-planning/SKILL.md)
- [key-guidelines skill](../key-guidelines/SKILL.md)

## Core Guidelines

Before starting any task, read and follow `/key-guidelines`

## Command Overview

The `/todo-task-run` command is designed as a **generic task runner** - it takes a pre-existing TODO.md file and systematically executes ALL tasks defined within it until completion.

### Role and Responsibility
- **Complete Execution**: Execute ALL tasks in TODO.md sequentially until every task is marked `- [x]`
- **Progress Management**: Orchestrate task execution, manage progress, and coordinate the overall workflow
- **Continuous Operation**: Continue executing tasks until completion or blocker - NEVER stop prematurely
- **Not for planning**: This command does NOT create tasks or convert requirements into actionable items
- **Task planning**: Use `/todo-task-planning` to convert requirements into a structured TODO.md before using this command
- **Task Runner Focus**: Act as a task runner, delegating individual work to subagents as much as possible

### Execution Guarantee
This command guarantees:
1. ✅ **Every task will be executed** in sequential order
2. ✅ **No tasks will be skipped** unless explicitly blocked
3. ✅ **Session continues until all tasks are complete** or a blocker is encountered
4. ✅ **Incomplete tasks will NOT be left unfinished** without user awareness

### Relationship with todo-task-planning
1. **Planning phase** (`/todo-task-planning`): Analyze requirements → Create TODO.md with actionable tasks
2. **Execution phase** (this command): Orchestrate task execution → Manage progress → Integrate completion status → Coordinate overall workflow

### Command Invocation
```
/todo-task-run TODO.md
```

## Processing Flow

**⚠️ CRITICAL EXECUTION POLICY**:

This command MUST execute ALL tasks in TODO.md sequentially, completing every task:
- ✅ **Execute tasks one by one** in the order they appear
- ✅ **After each task completion, check for remaining incomplete tasks**
- ✅ **Continue executing until ALL tasks are marked `- [x]`**
- ❌ **NEVER end the session while incomplete tasks remain**
- ❌ **NEVER skip tasks unless explicitly blocked**

**Session Continuation Rule**:
The session ONLY ends when ONE of these conditions is met:
1. ✅ All tasks in TODO.md are marked `- [x]` (complete)
2. 🚧 A task is blocked and requires user intervention
3. ❌ An unrecoverable error occurs

### Prerequisites

#### Input Contract
This command expects a TODO.md file with the following format:
- Tasks must be written as markdown checkboxes (`- [ ]` for incomplete, `- [x]` for complete)
- The file should contain actionable task items
- No strict schema validation is required - the command adapts to your task structure

### Initial Setup (Using Task Tool)
- Read TODO.md file specified in $ARGUMENTS
- **Classify each task by subagent type**:
  - Scan task descriptions for keywords (explore, investigate, implement, etc.)
  - Pre-determine subagent type for each task based on Subagent Classification Rules
  - Identify task dependencies (which tasks need results from previous tasks)
  - Log classification results for transparency

### Subagent Classification Rules

When executing tasks, select the appropriate subagent based on task characteristics:

- **Implementation Tasks** (implement, add, create, update features) → Use general-purpose subagent
  - Examples: Adding new features, modifying existing code, creating files
  - Standard implementation work without specific subagent requirements

- **Investigation Tasks** (explore, investigate, research) → Use `Explore` subagent
  - Examples: Codebase exploration, finding files, analyzing patterns
  - Specialized in comprehensive codebase analysis and discovery

### Memory File Initialization

**CRITICAL**: Before starting task execution, initialize memory system:

#### 1. Variable Initialization
At the start of task execution, declare context accumulation variables:
```
TASK_CONTEXT = {}  # Store context across tasks
MEMORY_FILES = {}  # Track active memory file paths
INVESTIGATION_FINDINGS = []  # Accumulate investigation results
```

#### 2. Load Existing Memory Files
Before executing any task, check and load relevant existing memory files:
- **Planning files**: `/docs/memory/planning/*.md` - Contains task breakdown and strategy
- **Exploration files**: `/docs/memory/explorations/*.md` - Contains codebase analysis results
- **Pattern files**: `/docs/memory/patterns/*.md` - Contains reusable technical patterns
- **Investigation files**: `/docs/memory/investigation-*.md` - Contains previous problem-solving insights

#### 3. Context Accumulation Strategy
As tasks progress:
- Store task execution results in `TASK_CONTEXT` for use in subsequent tasks
- Reference previous task outputs to inform current task decisions
- Document learnings and context in TODO.md task notes
- Link related memory files to build comprehensive understanding

### Task Execution: Sequential Task Tool Orchestration

**⚠️ CRITICAL: Sequential Execution Pattern Required**

All tasks MUST be executed sequentially using the Task tool. Each task's results inform the next task's context.

#### Execution Pattern Overview

```typescript
// Sequential execution pattern
const task_1_result = await Task({ subagent_type: "[subagent_type]", ... });
// ⚠️ WAIT for task_1 to complete, THEN proceed
const task_2_result = await Task({ subagent_type: "[subagent_type]", ... });
// ⚠️ WAIT for task_2 to complete, THEN proceed
const task_3_result = await Task({ subagent_type: "[subagent_type]", ... });

// ❌ WRONG: Parallel execution (DO NOT DO THIS)
Promise.all([
  Task({ subagent_type: "...", ... }),
  Task({ subagent_type: "...", ... })  // Tasks must be sequential!
]);
```

#### Task Classification and Subagent Selection

Before executing each task, determine the appropriate subagent based on task characteristics (see "Subagent Classification Rules" section):

- **Implementation Tasks** → `subagent_type: "general-purpose"` (or omit parameter)
- **Investigation Tasks** → `subagent_type: "Explore"`

#### Task Tool Execution Template

For each incomplete task (`- [ ]`) in TODO.md, execute using this pattern:

```typescript
const task_N_result = await Task({
  subagent_type: "[determined_subagent_type]",  // From classification rules
  description: "Execute task N: [task title from TODO.md]",
  prompt: `
    ## 📋 Development Rules (MUST Follow)

    ### 🚨 Guardrails (Prohibited Actions)
    **CRITICAL - Forward-Only Policy:**
    - ❌ NEVER use \`git reset\`, \`git restore\`, \`git revert\`, or any rollback commands
    - ✅ Always move forward: Fix errors with new changes, not by undoing previous ones

    ### Task Completion Procedure
    1. Update checkbox immediately after task execution (\`- [ ]\` → \`- [x]\`)
    2. Document related files (list names of created/modified files)

    ## Task Context
    **Current Task:** [Full task description from TODO.md]
    **Task Number:** N of [total_tasks]
    **Target File:** ${$ARGUMENTS}

    ## Previous Task Results
    ${task_N-1_result?.summary || "This is the first task"}
    ${task_N-1_result?.files_modified || ""}
    ${task_N-1_result?.key_findings || ""}

    ## Memory Files
    ${MEMORY_FILES.planning || ""}
    ${MEMORY_FILES.exploration || ""}
    ${MEMORY_FILES.patterns || ""}

    ## Task-Specific Instructions

    ### For Investigation Tasks (Explore subagent):
    1. Create investigation memory file at start:
       - Path: \`/docs/memory/investigation-YYYY-MM-DD-{topic}.md\`
       - Record findings immediately during investigation
       - Save technical patterns in \`/docs/memory/patterns/\`
    2. Document discoveries and insights for future reference
    3. Include links to related documentation

    ### For Implementation Tasks (General-purpose subagent):
    1. Follow existing code patterns discovered in exploration
    2. Adhere to YAGNI principle (implement only what's necessary)
    3. Reference memory files for context and technical patterns
    4. Record implementation context in TODO.md task notes

    ## Required Steps After Task Completion

    1. **Update TODO.md file** (${$ARGUMENTS})
       - Change completed task: \`- [ ]\` → \`- [x]\`
       - Add related file information below task
       - Record implementation details and notes
       - Format example:
         \`\`\`markdown
         - [x] Task title
           - Files: \`path/to/file1.rb\`, \`path/to/file2.rb\`
           - Notes: Brief description of implementation
         \`\`\`

    2. **Save investigation results** (for investigation tasks)
       - Consolidate insights in investigation memory file
       - Record technical discoveries for future reference
       - Link to related documentation and patterns

    3. **Update TODO.md with execution context**
       - Add task notes: implementation details, decisions, learnings
       - Record blockers with 🚧 marker if encountered
       - Document context for next task in task description

    4. **Report results**
       - Summarize changes made
       - List modified/created files with absolute paths
       - Note any issues or blockers encountered
       - Provide context for next task

    5. **⚠️ MANDATORY: Check for remaining tasks**
       - See "Execution Checkpoints" section (Lines 482-612) for detailed 3-step procedure
       - Must re-read TODO.md, detect `- [ ]` pattern, and branch appropriately

    ## Expected Output Format

    Return structured results for context accumulation:

    \`\`\`typescript
    {
      summary: "Brief description of what was accomplished",
      files_modified: ["absolute/path/to/file1", "absolute/path/to/file2"],
      key_findings: "Important discoveries or decisions (for investigation tasks)",
      blockers: "Any issues encountered (if applicable)",
      context_for_next_task: "Information needed by subsequent tasks"
    }
    \`\`\`
  `
});
```

#### Context Accumulation Between Tasks

**Critical Pattern**: Each task's results must be passed to the next task through the `prompt` parameter.

```typescript
// Task 1
const task_1_result = await Task({
  subagent_type: "Explore",
  description: "Investigate codebase for feature X",
  prompt: `[instructions]`
});

// Task 2 receives task_1_result in context
const task_2_result = await Task({
  subagent_type: "general-purpose",
  description: "Implement feature X based on investigation",
  prompt: `
    ## Previous Task Results
    ${task_1_result.summary}

    Files discovered: ${task_1_result.files_modified.join(', ')}
    Key findings: ${task_1_result.key_findings}

    [rest of task 2 instructions]
  `
});
```

#### Verification Gates After Each Task

**⚠️ MANDATORY**: After each Task tool execution, verify success before proceeding:

```typescript
const task_N_result = await Task({ ... });

// Verification gate
if (!task_N_result || task_N_result.blockers) {
  // Handle error:
  // 1. Mark task with 🚧 in TODO.md
  // 2. Record blocker in TODO.md with context
  // 3. Report to user with details
  // 4. STOP execution until blocker is resolved

  throw new Error(`Task N blocked: ${task_N_result.blockers}`);
}

// Verify expected outputs exist
if (!task_N_result.summary || !task_N_result.files_modified) {
  // Task completed but didn't return expected format
  // Log warning but continue if non-critical
}

// ✅ Verification passed, proceed to next task
const task_N+1_result = await Task({ ... });
```

#### Error Handling Protocol

When a task encounters an error or blocker:

**CRITICAL - Forward-Only Error Recovery:**
- ❌ **NEVER use `git reset`, `git restore`, `git revert`** to undo errors
- ✅ **Create new changes to fix errors** - Keep the history transparent
- ✅ **If code is broken, fix it forward** - Add corrections, don't erase mistakes

**Error Recovery Steps:**

1. **Mark task status in TODO.md**:
   ```markdown
   - [ ] 🚧 Task title (BLOCKED: reason for blockage)
   ```

2. **Record blocker details in TODO.md**:
   ```markdown
   - [ ] 🚧 Task title (BLOCKED: reason)
     - 🚧 Blocker: [Detailed description]
     - 🔧 Attempted: [What was tried]
     - 📋 Next steps: [How to resolve]
     - ⚠️ Recovery: Fix forward, not rollback
   ```

3. **Report to user**:
   - Clear description of the blocker
   - Impact on subsequent tasks
   - Recommended resolution steps
   - Plan for forward-only fix

4. **STOP execution**:
   - DO NOT proceed to next task
   - DO NOT rollback changes
   - Wait for user intervention or blocker resolution

5. **After blocker resolution**:
   - Once the user resolves the blocker or provides guidance
   - Re-read TODO.md to check current task status
   - If task is now unblocked, resume execution from that task
   - Continue with normal Task Execution Loop
   - **IMPORTANT**: DO NOT skip remaining tasks - continue until ALL tasks are complete

#### Task Execution Loop

**High-Level Flow Diagram**:

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                     TASK EXECUTION LOOP FLOW                              ║
╚═══════════════════════════════════════════════════════════════════════════╝

    START: Read TODO.md and identify first incomplete task
      │
      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 1: TASK EXECUTION                                                │
│  ─────────────────────────                                              │
│                                                                          │
│  1. Read TODO.md → identify next incomplete task (`- [ ]`)              │
│  2. Classify task → determine subagent_type                             │
│  3. Execute Task tool with accumulated context                          │
│  4. Verify completion (verification gate)                               │
│  5. Update TODO.md status (`- [ ]` → `- [x]`)                           │
│  6. Store task result for next task's context                           │
│                                                                          │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  🚨 PHASE 2: CONTINUATION CHECK PROCEDURE (MANDATORY GATE)              │
│  ────────────────────────────────────────────────────────              │
│                                                                          │
│  Step 1: Re-read TODO.md from disk                                      │
│           const todo_content = await Read({ file_path: $ARGUMENTS })    │
│                                                                          │
│  Step 2: Detect incomplete tasks                                        │
│           const has_incomplete_tasks = todo_content.includes('- [ ]')   │
│                                                                          │
│  Step 3: Branch Decision ──────────────┐                                │
│                                         │                                │
└─────────────────────────────────────────┼────────────────────────────────┘
                                          │
                    ┌─────────────────────┴────────────────────┐
                    │                                           │
                    ▼                                           ▼
        ┌───────────────────────┐                 ┌────────────────────────┐
        │  has_incomplete_tasks │                 │  has_incomplete_tasks  │
        │  === true             │                 │  === false             │
        └───────────────────────┘                 └────────────────────────┘
                    │                                           │
                    │                                           │
                    ▼                                           ▼
        ┌───────────────────────┐                 ┌────────────────────────┐
        │  PATH A:              │                 │  PATH B:               │
        │  CONTINUE LOOP        │                 │  FINAL COMPLETION      │
        │                       │                 │                        │
        │  ✅ Execute next task │                 │  ✅ Verify ALL [x]     │
        │     via Task tool     │                 │  ✅ Add timestamp      │
        │                       │                 │  ✅ Generate report    │
        │  ❌ DO NOT proceed to │                 │  ✅ End session        │
        │     Final Completion  │                 │                        │
        │                       │                 │                        │
        │  ❌ DO NOT end session│                 │  🎯 COMPLETE           │
        └───────────────────────┘                 └────────────────────────┘
                    │                                           │
                    │                                           │
                    │ (loop back to PHASE 1)                   END
                    │
                    └──────────────┐
                                   │
                                   ▼
                    Return to PHASE 1: Execute next task
```

**Critical Decision Points**:

1. **Verification Gate** (After each task): Did the task complete successfully?
   - ✅ YES → Continue to Continuation Check
   - ❌ NO → Mark blocker (`🚧`), report to user, STOP

2. **Continuation Check Gate** (Mandatory after EACH task): Are there incomplete tasks?
   - ✅ YES (`- [ ]` found) → PATH A: Continue to next task (loop back to PHASE 1)
   - ✅ NO (all `- [x]`) → PATH B: Proceed to Final Completion Process

**Loop Termination Conditions**:
- ✅ **Normal completion**: All tasks marked `- [x]` → Final Completion Process
- 🚧 **Blocked**: Task encounters blocker → STOP, report to user
- ❌ **Error**: Unrecoverable error → STOP, report to user

Repeat the Task tool pattern for each incomplete task until:
- All tasks are marked `- [x]` (completed), OR
- A task is blocked with `🚧` marker (stop and report)

**Execution Flow**:
1. Read TODO.md and identify next incomplete task (`- [ ]`)
2. Classify task and determine `subagent_type`
3. Execute Task tool with accumulated context
4. Verify task completion (verification gate)
5. Update TODO.md status (`- [ ]` → `- [x]`)
6. Store task result for next task's context
7. **CRITICAL: After each task completion, IMMEDIATELY re-read TODO.md and check for remaining incomplete tasks**
8. **If ANY incomplete tasks remain (`- [ ]`), IMMEDIATELY continue to next task (return to step 1)**
9. **ONLY proceed to "Final Completion Process" when ALL tasks are marked `- [x]`**

**⚠️ MANDATORY CONTINUATION CHECK**:

See "Execution Checkpoints" section (Lines 482-612) for the required 3-step procedure that MUST be executed after EACH task completion.

#### Execution Checkpoints: 3-Step Post-Task Procedure

**⚠️ CRITICAL: Execute After EVERY Task Completion**

After each Task tool execution completes, you MUST execute this 3-step checkpoint procedure:

```
╔════════════════════════════════════════════════════════════════╗
║  🎯 EXECUTION CHECKPOINT - POST-TASK VERIFICATION             ║
║  ─────────────────────────────────────────────────────────     ║
║                                                                ║
║  Execute this 3-step procedure after EVERY task completion:   ║
║                                                                ║
║  ┌──────────────────────────────────────────────────────┐    ║
║  │ STEP 1: Re-read TODO.md from disk                    │    ║
║  │         ↓                                             │    ║
║  │         const todo = await Read({ file_path: ... })   │    ║
║  │                                                        │    ║
║  │ Purpose: Get fresh state, not stale in-memory data    │    ║
║  └──────────────────────────────────────────────────────┘    ║
║                          │                                     ║
║                          ▼                                     ║
║  ┌──────────────────────────────────────────────────────┐    ║
║  │ STEP 2: Check for '- [ ]' pattern existence          │    ║
║  │         ↓                                             │    ║
║  │         const has_incomplete = todo.includes('- [ ]') │    ║
║  │                                                        │    ║
║  │ Purpose: Detect if ANY incomplete tasks remain        │    ║
║  └──────────────────────────────────────────────────────┘    ║
║                          │                                     ║
║                          ▼                                     ║
║  ┌──────────────────────────────────────────────────────┐    ║
║  │ STEP 3: Branch decision based on detection result    │    ║
║  │                                                        │    ║
║  │  if (has_incomplete === true) {                       │    ║
║  │    → Continue to next task (loop back to PHASE 1)    │    ║
║  │    → DO NOT end session                               │    ║
║  │  } else {                                             │    ║
║  │    → Proceed to Final Completion Process             │    ║
║  │    → Safe to end session after final steps           │    ║
║  │  }                                                     │    ║
║  │                                                        │    ║
║  │ Purpose: Prevent premature session termination        │    ║
║  └──────────────────────────────────────────────────────┘    ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

**Checkpoint Implementation Code**:

```typescript
// ════════════════════════════════════════════════════════════════
// EXECUTION CHECKPOINT - Execute after EVERY task completion
// ════════════════════════════════════════════════════════════════

// STEP 1: Re-read TODO.md from disk
const todo_content = await Read({ file_path: $ARGUMENTS });

// STEP 2: Check for '- [ ]' pattern existence
const has_incomplete_tasks = todo_content.includes('- [ ]');

// STEP 3: Branch decision
if (has_incomplete_tasks) {
  // ✅ PATH A: At least one incomplete task exists
  // → MUST continue to next task
  // → CANNOT proceed to Final Completion Process
  // → CANNOT end session

  console.log('✅ Checkpoint: Incomplete tasks detected, continuing loop...');

  // Return to PHASE 1: Execute next task
  const next_task_result = await Task({
    subagent_type: "[determined_type]",
    description: "Execute next incomplete task",
    prompt: `[task instructions with accumulated context]`
  });

  // After next task completes, return to this checkpoint (recursive loop)

} else {
  // ✅ PATH B: NO incomplete tasks remain
  // → All tasks are marked '- [x]'
  // → Safe to proceed to Final Completion Process
  // → Session can end after final steps

  console.log('✅ Checkpoint: All tasks complete, proceeding to final steps...');

  // Proceed to "Final Completion Process" section
}
```

**Checkpoint Failure Indicators**:

If you find yourself in any of these situations, the checkpoint was not executed correctly:

| ❌ Failure Indicator | ✅ Correct Action |
|----------------------|-------------------|
| Ending session while `- [ ]` exists in TODO.md | Execute checkpoint → Detect incomplete tasks → Continue loop |
| Proceeding to Final Completion without reading TODO.md | Execute STEP 1: Re-read file from disk |
| Assuming all tasks done based on in-memory state | Execute STEP 2: Explicit pattern detection |
| Skipping checkpoint "because task seemed final" | ALWAYS execute checkpoint after EVERY task |

**Visual Reminder - When to Execute**:

```
Task Execution Timeline:
════════════════════════════════════════════════════════════════

Task N-1        Task N          🎯 CHECKPOINT      Task N+1
   │               │                  │               │
   │               │                  │               │
   ▼               ▼                  ▼               ▼
[Execute]  →  [Complete]  →  [3-Step Check]  →  [Continue/End]
               [Update TODO]   │
                               ├─ Step 1: Read
                               ├─ Step 2: Detect
                               └─ Step 3: Branch
                                       │
                                       ├─ Found [ ] → Next Task
                                       └─ All [x]  → Final Steps

🚨 CRITICAL: Checkpoint executes AFTER TODO.md update, BEFORE next decision
```

**Connection to Continuation Check Procedure**:

This checkpoint procedure is the **in-loop implementation** of the "Continuation Check Procedure" section (Lines 614-701):
- **Checkpoint** = Execution code after each task (what you DO)
- **Continuation Check Procedure** = Detailed specification (what it MEANS)

Both sections describe the same mandatory 3-step process from different perspectives. The checkpoint ensures continuous execution until completion.

### Continuation Check Procedure

**⚠️ MANDATORY GATE: This procedure is the critical decision point between task execution and final completion.**

After completing each task, you MUST execute this 3-step continuation check procedure:

#### Step 1: Re-read TODO.md

**Why this is mandatory**:
- TODO.md is the single source of truth for task completion status
- The file may have been updated by the previous Task execution
- In-memory state may be stale - always read from disk

#### Step 2: Detect Incomplete Tasks

**Detection logic**:
- Pattern found → At least one task remains incomplete
- Pattern not found → All tasks are complete (`- [x]`)

(See Lines 532-571 in "Execution Checkpoints" for implementation code)

#### Step 3: Branch Decision

```
┌─────────────────────────────────────────────────────┐
│         Continuation Check Decision Tree            │
└─────────────────────────────────────────────────────┘
                          │
                          ▼
         ┌────────────────────────────────┐
         │ has_incomplete_tasks?          │
         └────────────────────────────────┘
                 /                \
                /                  \
              YES                  NO
               │                    │
               ▼                    ▼
    ┌──────────────────┐   ┌─────────────────────┐
    │ ✅ Continue Loop │   │ ✅ Final Completion │
    │                  │   │                     │
    │ - Execute next   │   │ - Verify ALL tasks  │
    │   task via Task  │   │   are [x]           │
    │   tool           │   │ - Add completion    │
    │                  │   │   timestamp         │
    │ - DO NOT proceed │   │ - Generate final    │
    │   to Final       │   │   report            │
    │   Completion     │   │                     │
    │                  │   │ - End session       │
    │ - DO NOT end     │   │                     │
    │   session        │   │                     │
    └──────────────────┘   └─────────────────────┘
           │
           │ (loop continues)
           ▼
    Return to Step 1 after
    next task completion
```

#### Implementation Template

See Lines 532-571 in "Execution Checkpoints" section for complete implementation code with detailed comments.

**⚠️ WARNING: Common Mistakes to Avoid**:

| ❌ WRONG | ✅ CORRECT |
|----------|------------|
| Proceeding to Final Completion while `- [ ]` exists | Always check TODO.md before final steps |
| Ending session with incomplete tasks | Continue loop until all `- [x]` |
| Assuming all tasks are done without checking | Explicit file read + pattern detection |
| Using stale in-memory state | Fresh `Read()` call every time |

**Visual Reminder**:

```
╔═══════════════════════════════════════════════════════════╗
║  🚨 CRITICAL CHECKPOINT                                   ║
║                                                           ║
║  Before proceeding to Final Completion Process:          ║
║                                                           ║
║  ✅ Read TODO.md from disk                               ║
║  ✅ Check for '- [ ]' pattern                            ║
║  ✅ If found → Continue to next task                     ║
║  ✅ If NOT found → Proceed to Final Completion           ║
║                                                           ║
║  This gate prevents premature session termination        ║
╚═══════════════════════════════════════════════════════════╝
```

### Error Handling and Investigation

When encountering errors or unexpected issues during task execution:

**CRITICAL - Forward-Only Error Recovery:**
- ❌ **NEVER use `git reset`, `git restore`, `git revert`** to undo errors
- ✅ **Always fix forward with new changes** - Preserve complete history
- ✅ **Document the fix** - Record why the error occurred and how it was resolved

#### Hybrid Investigation Approach
1. **Reference existing memory files**: Check `/docs/memory/` for previous investigations on similar issues
2. **Investigate as needed**: If no relevant documentation exists or the issue is novel, conduct investigation
3. **Document findings**: Record new insights in appropriate memory files for future reference

#### Error Recovery Workflow
1. **Identify the error**: Understand the root cause through debugging or investigation
2. **Consult documentation**: Review existing memory files and reference documentation
3. **Resolve the issue**: Apply fixes based on documented patterns or new solutions
   - **IMPORTANT**: Create new changes for fixes, do not rollback
4. **Update memory**: If new patterns or solutions emerge, document them in `/docs/memory/patterns/`
   - Record what went wrong and how it was fixed
   - Document lessons learned for future tasks
5. **Continue execution**: Resume task execution after resolving the error

#### When to Create Memory Files
- **New technical patterns**: Document reusable solutions in `/docs/memory/patterns/`
- **Complex investigations**: Create investigation files when debugging takes significant effort
- **System insights**: Record important technical discoveries about the codebase or infrastructure

### Final Completion Process (Using Task Tool)

```
╔═══════════════════════════════════════════════════════════════════════════╗
║  🚨 CRITICAL PREREQUISITE CHECK                                          ║
║                                                                           ║
║  This section is ONLY accessible after:                                  ║
║  1. Executing "Execution Checkpoints" 3-step procedure (Lines 482-612)  ║
║  2. Passing "Continuation Check Procedure" gate (Lines 614-701)         ║
║  3. Confirming PATH B (Final Completion) - NO '- [ ]' in TODO.md        ║
║                                                                           ║
║  If '- [ ]' exists → Return to Task Execution Loop (PATH A)             ║
║  Only proceed if ALL tasks are '- [x]' (PATH B confirmed)               ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

**⚠️ MANDATORY VERIFICATION**:

This section is ONLY accessible if the Continuation Check Procedure (Lines 614-701) returned PATH B (all tasks complete).

Before proceeding, verify:
1. ✅ Continuation Check completed (3-step procedure executed)
2. ✅ ALL tasks marked `- [x]` (no `- [ ]` pattern exists)
3. ✅ No blocked tasks (no `🚧` markers)

(See Lines 532-571 in "Execution Checkpoints" for verification code template)

**Required steps upon all tasks completion**:
1. **Final update of file specified in $ARGUMENTS**:
   - Confirm all tasks are in completed state (`- [x]`)
   - Add completion date/time and overall implementation summary
   - Record reference information for future maintenance
2. **Final consolidation of investigation results**:
   - Final organization of all investigation results in memory file
   - Record project-wide impact and future prospects
   - Prepare in a form that can be utilized as reference information for similar tasks

**Final Report to User**:

After completing all final steps, provide a comprehensive summary:
- ✅ Total tasks completed: [N] out of [N]
- ✅ All tasks status: Complete
- ✅ Files modified: [List of all files]
- ✅ Next steps: [If applicable]
