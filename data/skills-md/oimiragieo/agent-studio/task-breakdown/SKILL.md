---
name: task-breakdown
description: Break down implementation plans into organized task lists using Epic → Story → Task hierarchy with Enabler support, P1/P2/P3 prioritization, and TaskCreate integration
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Skill, TaskCreate, TaskUpdate, TaskList, Grep, Glob]
args: '<plan-file> [--create-tasks] [--output <path>]'
best_practices:
  - Always identify Enablers first (shared infrastructure that blocks all stories)
  - Use P1/P2/P3 prioritization (P1 = MVP must-haves)
  - Invoke template-renderer for consistent task document generation
  - Create TaskCreate calls for all atomic tasks with proper dependencies
  - Validate acceptance criteria are testable and measurable
  - Ensure task IDs follow convention (ENABLER-X.Y, P1-X.Y.Z, P2-X.Y.Z, P3-X.Y.Z)
error_handling: strict
streaming: not_supported
---

# Task Breakdown Skill

<identity>
Task Breakdown Skill - Transforms implementation plans into structured task lists using Epic → Story → Task hierarchy (ADR-045). Supports Enabler tasks for shared infrastructure, P1/P2/P3 prioritization (MoSCoW method), and automatic TaskCreate integration for tracking.
</identity>

<capabilities>
- Parse implementation plans and extract phases/milestones
- Identify Enabler tasks (shared infrastructure that blocks all user stories)
- Organize tasks by Epic → User Story → Task hierarchy
- Apply P1/P2/P3 prioritization (Must/Should/Could have)
- Generate acceptance criteria for user stories
- Calculate dependencies and blockers (Enablers → P1 → P2 → P3)
- Invoke template-renderer to create structured task documents
- Create TaskCreate calls for all atomic tasks with proper metadata
- Validate task completeness and dependency integrity
- Support SAFe/Azure DevOps/Jira task organization patterns
</capabilities>

## Purpose

Break down high-level implementation plans into actionable task lists with proper user story organization, enabling:

1. **Structured Planning**: Epic → Story → Task hierarchy with clear dependencies
2. **Infrastructure First**: Enabler tasks completed before user-facing work
3. **Priority-Driven**: P1 (MVP) → P2 (Nice-to-Have) → P3 (Polish) execution order
4. **Acceptance Driven**: Each story has testable acceptance criteria
5. **Tracking Integration**: Automatic TaskCreate for all tasks with proper metadata

## When to Use

Invoke this skill after plan-generator creates an implementation plan and before development starts:

```javascript
// After plan-generator completes
Skill({
  skill: 'task-breakdown',
  args: '.claude/context/plans/my-feature-plan.md --create-tasks --output .claude/context/artifacts/tasks/my-feature-tasks.md',
});
```

**Use when:**

- Plan-generator has created a multi-phase implementation plan
- You need to convert plan phases into trackable tasks
- User stories need to be prioritized (P1/P2/P3)
- Shared infrastructure (Enablers) needs to be identified
- TaskCreate calls are needed for task tracking system

**Skip when:**

- Plan is already in task format (no conversion needed)
- Single-phase simple task (directly use TaskCreate)
- Exploratory research (use research-synthesis instead)

## Iron Law: Enablers Before Stories

**CRITICAL**: Enabler tasks (shared infrastructure) MUST complete before any user story begins.

```
WRONG (concurrent):
ENABLER-1.1 ─┐
             ├──→ [ALL START TOGETHER - RACE CONDITIONS]
P1-1.1.1 ────┘

CORRECT (sequential):
ENABLER-1.1 → ENABLER-1.2 → [ALL ENABLERS DONE] → P1-1.1.1 → P1-1.1.2 → ...
```

**Why**: Enablers provide shared infrastructure (database schema, authentication middleware, shared utilities). Starting user stories before enablers complete causes:

- Duplicate infrastructure work across stories
- Breaking changes when enabler completes late
- Integration bugs from inconsistent infrastructure

**Task Dependencies**: All P1 story tasks MUST have `addBlockedBy: ['ENABLER-1.1', 'ENABLER-1.2', ...]`

## Workflow

### Step 1: Read Plan and Extract Structure

Read the implementation plan created by plan-generator:

```javascript
const plan = Read('.claude/context/plans/my-feature-plan.md');

// Extract key information:
// - Plan title and overview
// - Executive summary
// - Total phases and milestones
// - Dependencies between phases
// - Key deliverables per phase
// - Estimated effort per phase
```

Parse the plan structure:

- Identify all phases (Phase 0: Research, Phase 1: Foundation, Phase 2: Core Features, etc.)
- Extract tasks from each phase
- Identify parallelizable work (PARALLEL_OK flags)
- Note dependencies between phases

### Step 2: Identify Enablers (Shared Infrastructure)

**CRITICAL**: Scan phases for infrastructure work that blocks all user stories.

Enabler Indicators:

- Database schema/migrations
- Authentication/authorization middleware
- Shared utility libraries
- API scaffolding/routing setup
- Configuration/environment setup
- Deployment infrastructure (Docker, CI/CD)

**Example Enablers**:

```
Phase 1: Foundation
├── Task 1.1: Create user database schema → ENABLER-1.1
├── Task 1.2: Implement JWT token service → ENABLER-1.2
└── Task 1.3: Set up authentication middleware → ENABLER-1.3

Reason: All user stories need these for authentication
```

**Enabler Extraction Algorithm**:

1. Find tasks in "Foundation" or "Infrastructure" phases
2. Check if task description includes: schema, middleware, shared, infrastructure, setup, config
3. Verify task is referenced by multiple user stories
4. Mark as `[ENABLER]` and assign ID: `ENABLER-X.Y`

### Step 3: Extract User Stories from Plan Phases

Convert plan phases into user stories using the "As a... I want... So that..." format.

**Phase → Story Mapping**:

```
Plan Phase 2: Core Features
├── Milestone 2.1: User login functionality
│   ├── Task: Create login API endpoint
│   └── Task: Build login form UI
└── Milestone 2.2: User registration

↓ CONVERT TO ↓

User Story 1.1: User Login with Email/Password [P1]
As a registered user,
I want to log in with my email and password,
So that I can access my account securely.

Tasks:
- [P1-1.1.1] Create login API endpoint
- [P1-1.1.2] Build login form UI
```

**Story Extraction Rules**:

1. Each milestone becomes a user story (if user-facing)
2. Combine related tasks under the same story
3. Generate user role, capability, business value
4. Extract acceptance criteria from plan verification steps
5. Calculate estimated effort (sum of task efforts)

### Step 4: Apply P1/P2/P3 Prioritization (MoSCoW Method)

Classify each user story by priority:

| Priority              | MoSCoW      | Meaning                             | Criteria                                                              |
| --------------------- | ----------- | ----------------------------------- | --------------------------------------------------------------------- |
| **P1 (MVP)**          | Must Have   | Critical for minimum viable product | Core functionality, user login, data CRUD, essential workflows        |
| **P2 (Nice-to-Have)** | Should Have | Important but not blocking          | Password reset, profile editing, advanced search, email notifications |
| **P3 (Polish)**       | Could Have  | Refinement and optimization         | Remember me checkbox, avatars, dark mode, performance tweaks          |

**Prioritization Algorithm**:

```javascript
function prioritizeStory(story, plan) {
  // P1 indicators (MVP)
  if (
    story.includes('authentication') ||
    story.includes('core data') ||
    story.includes('essential workflow')
  ) {
    return 'P1';
  }

  // P3 indicators (polish)
  if (
    story.includes('optimization') ||
    story.includes('polish') ||
    story.includes('nice-to-have')
  ) {
    return 'P3';
  }

  // Default to P2
  return 'P2';
}
```

**Priority Assignment Rules**:

- Foundation/infrastructure → Enabler (not P1/P2/P3)
- Core user flows → P1
- User account management (beyond login) → P2
- UI polish, performance optimizations → P3
- Check plan's "Critical Path" section for P1 hints

### Step 5: Generate Acceptance Criteria

For each user story, create testable acceptance criteria:

**Acceptance Criteria Formula**:

```
- [ ] {User action} results in {expected outcome}
- [ ] {Edge case} handled with {specific behavior}
- [ ] {Performance metric} meets {threshold}
- [ ] {Security requirement} enforced
```

**Examples**:

```markdown
User Story: User Login with Email/Password [P1]

Acceptance Criteria:

- [ ] User can submit email and password via login form
- [ ] Valid credentials return JWT token and redirect to dashboard
- [ ] Invalid credentials show error message "Invalid email or password"
- [ ] Failed login attempts are logged for security audit
- [ ] Login response time < 200ms (p95)
```

**Extraction from Plan**:

1. Look for plan's "Verification Commands" per task → convert to acceptance criteria
2. Extract performance requirements from plan overview
3. Add security criteria for auth/data handling stories
4. Include error handling criteria for all user actions

### Step 6: Assign Task IDs and Dependencies

Use standardized task ID convention:

**Task ID Format**:

- **Enablers**: `ENABLER-X.Y` (e.g., `ENABLER-1.1`, `ENABLER-1.2`)
  - X = Enabler group number
  - Y = Task number within group
- **P1 Tasks**: `P1-X.Y.Z` (e.g., `P1-1.1.1`, `P1-1.1.2`)
  - X = Story number within P1
  - Y = Substory (usually 1 unless nested)
  - Z = Task number within story
- **P2 Tasks**: `P2-X.Y.Z` (same structure as P1)
- **P3 Tasks**: `P3-X.Y.Z` (same structure as P1)

**Dependency Rules**:

1. **All P1 stories** depend on **all Enablers**
2. **P2 stories** depend on **P1 stories** they extend
3. **P3 stories** depend on **P1 or P2** they enhance
4. **Tasks within a story** are sequential by default (each depends on previous)

**Example Dependencies**:

```javascript
// Enabler tasks (no dependencies)
TaskCreate({ subject: 'ENABLER-1.1: Create user database schema', ... });
TaskCreate({ subject: 'ENABLER-1.2: Implement JWT token service', ... });

// P1 story tasks (blocked by enablers)
TaskCreate({
  subject: 'P1-1.1.1: Create login API endpoint',
  metadata: { priority: 'p1', story: '1.1' }
});
TaskUpdate({ taskId: 'P1-1.1.1', addBlockedBy: ['ENABLER-1.1', 'ENABLER-1.2'] });

// P1 story task (blocked by previous task in same story)
TaskCreate({
  subject: 'P1-1.1.2: Build login form UI',
  metadata: { priority: 'p1', story: '1.1' }
});
TaskUpdate({ taskId: 'P1-1.1.2', addBlockedBy: ['P1-1.1.1'] });

// P2 story task (blocked by P1 story it extends)
TaskCreate({
  subject: 'P2-2.1.1: Implement password reset token generation',
  metadata: { priority: 'p2', story: '2.1' }
});
TaskUpdate({ taskId: 'P2-2.1.1', addBlockedBy: ['P1-1.1.1'] }); // Needs auth infrastructure
```

### Step 7: Invoke Template Renderer

Use template-renderer to generate the structured task document:

```javascript
// Build token map from extracted data
const tokens = {
  // Header metadata
  FEATURE_NAME: extractFeatureName(plan),
  VERSION: '1.0.0',
  AUTHOR: 'Claude',
  DATE: new Date().toISOString().split('T')[0],
  STATUS: 'draft',
  PRIORITY: determinePriority(plan),
  ESTIMATED_EFFORT: calculateTotalEffort(plan),

  // Overview
  FEATURE_DISPLAY_NAME: extractDisplayName(plan),
  FEATURE_DESCRIPTION: plan.executiveSummary,
  BUSINESS_VALUE: extractBusinessValue(plan),
  USER_IMPACT: extractUserImpact(plan),

  // Epic level
  EPIC_NAME: extractEpicName(plan),
  EPIC_GOAL: plan.overview.goal,
  SUCCESS_CRITERIA: extractSuccessCriteria(plan),

  // Enablers (repeat for each enabler)
  ENABLER_1_NAME: 'Authentication Infrastructure',
  ENABLER_1_PURPOSE: 'Set up shared authentication middleware and database schema',
  ENABLER_1_EFFORT: '2 days',

  // User stories (repeat for each story)
  // P1 stories, P2 stories, P3 stories

  // Summary counts
  ENABLER_COUNT: enablers.length,
  P1_STORY_COUNT: p1Stories.length,
  P2_STORY_COUNT: p2Stories.length,
  P3_STORY_COUNT: p3Stories.length,
  TOTAL_STORIES: allStories.length,
  TOTAL_TASKS: allTasks.length,
  TOTAL_EFFORT: totalEffort,
};

// Invoke template-renderer
Skill({
  skill: 'template-renderer',
  args: {
    templateName: 'tasks-template',
    outputPath: outputPath,
    tokens: tokens,
  },
});
```

### Step 8: Create TaskCreate Calls (Optional --create-tasks)

If `--create-tasks` flag is provided, generate TaskCreate calls for all tasks:

```javascript
// Phase 1: Create all Enabler tasks
enablers.forEach(enabler => {
  TaskCreate({
    subject: `${enabler.id}: ${enabler.title}`,
    description: enabler.description,
    activeForm: enabler.activeForm,
    metadata: {
      type: 'enabler',
      blocksAll: true,
      estimatedEffort: enabler.effort,
      outputArtifacts: enabler.outputs,
    },
  });
});

// Phase 2: Create P1 tasks with Enabler dependencies
p1Tasks.forEach(task => {
  TaskCreate({
    subject: `${task.id}: ${task.title}`,
    description: task.description,
    activeForm: task.activeForm,
    metadata: {
      priority: 'p1',
      story: task.storyId,
      estimatedEffort: task.effort,
      outputArtifacts: task.outputs,
    },
  });

  // Block P1 tasks on all enablers
  TaskUpdate({
    taskId: task.id,
    addBlockedBy: enablers.map(e => e.id),
  });

  // Block on previous task in same story
  if (task.previousTaskInStory) {
    TaskUpdate({
      taskId: task.id,
      addBlockedBy: [task.previousTaskInStory],
    });
  }
});

// Phase 3: Create P2 tasks
p2Tasks.forEach(task => {
  TaskCreate({
    subject: `${task.id}: ${task.title}`,
    description: task.description,
    activeForm: task.activeForm,
    metadata: {
      priority: 'p2',
      story: task.storyId,
      estimatedEffort: task.effort,
    },
  });

  // Block P2 on dependencies (usually P1 stories)
  TaskUpdate({
    taskId: task.id,
    addBlockedBy: task.dependencies,
  });
});

// Phase 4: Create P3 tasks (similar to P2)
```

**TaskCreate Best Practices**:

1. Always include `activeForm` (present continuous for spinner display)
2. Use metadata for priority, story ID, effort, outputs
3. Create tasks in dependency order (Enablers → P1 → P2 → P3)
4. Use TaskUpdate immediately after TaskCreate to set dependencies
5. Record task IDs in memory for verification

### Step 9: Validation and Verification

Run post-breakdown validation:

```bash
# Check no unresolved placeholders in task document
grep "{{" <output-file> && echo "ERROR: Unresolved tokens!" || echo "✓ All tokens resolved"

# Verify all P1 stories have acceptance criteria
grep -A 5 "## User Story.*\[P1\]" <output-file> | grep "Acceptance Criteria" || echo "WARNING: P1 missing acceptance criteria"

# Check task ID format
grep -E "(ENABLER-[0-9]+\.[0-9]+|P[123]-[0-9]+\.[0-9]+\.[0-9]+)" <output-file> || echo "WARNING: Invalid task IDs"

# Verify dependency integrity (if --create-tasks used)
TaskList() # Check all tasks created successfully
```

**Validation Checklist**:

- [ ] All `{{PLACEHOLDER}}` values replaced
- [ ] All enabler tasks identified and marked `[ENABLER]`
- [ ] User stories prioritized (P1 = MVP, P2 = Nice-to-Have, P3 = Polish)
- [ ] Task dependencies documented (blockedBy references)
- [ ] Acceptance criteria defined for each user story
- [ ] Task IDs follow convention (ENABLER-X.Y, P1-X.Y.Z)
- [ ] If `--create-tasks`: All TaskCreate calls successful
- [ ] Task summary table has correct counts

## Examples

### Example 1: Basic Task Breakdown (No TaskCreate)

```javascript
// After plan-generator creates a plan
Skill({
  skill: 'task-breakdown',
  args: '.claude/context/plans/auth-feature-plan.md --output .claude/context/artifacts/tasks/auth-tasks.md',
});

// Result: .claude/context/artifacts/tasks/auth-tasks.md created with:
// - 2 Enabler groups (database, authentication middleware)
// - 3 P1 user stories (login, logout, session management)
// - 2 P2 user stories (password reset, profile editing)
// - 1 P3 user story (remember me checkbox)
// - All tasks have IDs, descriptions, acceptance criteria
```

### Example 2: Task Breakdown with TaskCreate Integration

```javascript
// Generate task document AND create tasks in tracking system
Skill({
  skill: 'task-breakdown',
  args: '.claude/context/plans/api-feature-plan.md --create-tasks --output .claude/context/artifacts/tasks/api-tasks.md',
});

// Result:
// 1. Task document created at .claude/context/artifacts/tasks/api-tasks.md
// 2. TaskCreate calls executed for all tasks:
//    - ENABLER-1.1: Create API schema
//    - ENABLER-1.2: Set up API versioning
//    - P1-1.1.1: Create GET /users endpoint
//    - P1-1.1.2: Add authentication to GET /users
//    - ... (all tasks created)
// 3. Dependencies set via TaskUpdate
// 4. TaskList() shows all tasks ready for assignment
```

### Example 3: From Planner Agent

```javascript
// In planner agent workflow
// Step 1: Create implementation plan
Skill({
  skill: 'plan-generator',
  args: '--feature "User Authentication" --output .claude/context/plans/auth-plan.md',
});

// Step 2: Break down plan into tasks
Skill({
  skill: 'task-breakdown',
  args: '.claude/context/plans/auth-plan.md --create-tasks --output .claude/context/artifacts/tasks/auth-tasks.md',
});

// Step 3: Verify tasks created
TaskList(); // Shows all tasks with proper priorities and dependencies

// Step 4: Developer can now claim tasks in order:
// 1. Claim ENABLER-1.1 (no blockers)
// 2. After ENABLER-1.1 done, claim P1-1.1.1 (now unblocked)
// 3. Continue sequential execution
```

### Example 4: Manual Task Breakdown (CLI)

```bash
# Using skill via CLI
node .claude/skills/task-breakdown/scripts/main.cjs \
  --plan .claude/context/plans/feature-plan.md \
  --output ./tasks.md \
  --create-tasks

# Output:
# ✓ Plan parsed: 5 phases, 14 tasks extracted
# ✓ Identified 2 Enabler groups (4 tasks)
# ✓ Extracted 8 user stories (4 P1, 3 P2, 1 P3)
# ✓ Generated acceptance criteria for all stories
# ✓ Task document created: ./tasks.md
# ✓ Created 14 tasks in tracking system
# ✓ All dependencies configured
# → Next: TaskList() to view tasks
```

## Integration with Planner Agent

The task-breakdown skill is designed to be invoked by the planner agent after plan-generator:

**Planner Agent Workflow**:

```
1. [PLANNER] Invoke plan-generator → creates .claude/context/plans/feature-plan.md
2. [PLANNER] Invoke task-breakdown → creates .claude/context/artifacts/tasks/feature-tasks.md
3. [PLANNER] Review task breakdown for completeness
4. [PLANNER] If --create-tasks used: TaskList() to verify all tasks created
5. [PLANNER] Hand off to developer agent to claim first unblocked task
```

**Expected Output**:

```
[PLANNER] ✓ Plan created: auth-feature-plan.md (5 phases, 14 tasks)
[PLANNER] → Invoking task-breakdown...
[TASK-BREAKDOWN] ✓ Identified 2 Enabler groups (4 tasks)
[TASK-BREAKDOWN] ✓ Extracted 8 user stories (4 P1, 3 P2, 1 P3)
[TASK-BREAKDOWN] ✓ Task document created: auth-tasks.md
[TASK-BREAKDOWN] ✓ Created 14 tasks in tracking system
[PLANNER] → Verification: TaskList()
[PLANNER] ✓ All tasks visible, ready for development
[PLANNER] → Next: Developer claims ENABLER-1.1
```

## Task ID to TaskCreate Mapping

**How to convert task IDs to TaskCreate subject strings**:

```javascript
// Task ID in document: ENABLER-1.1
// TaskCreate subject: "ENABLER-1.1: Create user database schema"

// Task ID in document: P1-1.1.1
// TaskCreate subject: "P1-1.1.1: Create login API endpoint"

// Format: "{TASK_ID}: {TASK_TITLE}"
```

**Metadata to include**:

```javascript
TaskCreate({
  subject: 'ENABLER-1.1: Create user database schema',
  description:
    'Design and implement users table with email, password_hash, created_at, last_login columns. Create migration file.',
  activeForm: 'Creating user database schema',
  metadata: {
    type: 'enabler', // 'enabler' | 'p1' | 'p2' | 'p3'
    blocksAll: true, // Only for enablers
    priority: 'enabler', // 'enabler' | 'p1' | 'p2' | 'p3'
    story: null, // Story ID (e.g., '1.1') or null for enablers
    estimatedEffort: '4 hours', // From plan
    outputArtifacts: ['migration file', 'schema documentation'],
    verificationCommand: 'psql -c "\\d users"',
  },
});
```

## Best Practices

1. **Always identify Enablers first** - Shared infrastructure must complete before user stories
2. **Use P1 for MVP only** - P1 should be releasable minimum viable product
3. **Testable acceptance criteria** - Every criterion should be verifiable (e.g., "response time < 200ms")
4. **Follow task ID convention** - ENABLER-X.Y, P1-X.Y.Z, P2-X.Y.Z, P3-X.Y.Z
5. **Sequential task creation** - Create tasks in dependency order to avoid circular dependencies
6. **Invoke template-renderer** - Don't manually write task documents (use token replacement)
7. **Validate before TaskCreate** - Check task document completeness before creating tasks
8. **Use metadata extensively** - Include priority, story, effort, outputs in TaskCreate metadata
9. **Record task IDs** - Keep list of created task IDs in memory for verification

## Error Handling

**Missing Plan File**:

```
ERROR: Plan file not found: .claude/context/plans/missing-plan.md
Ensure plan-generator has run successfully before invoking task-breakdown.
```

**No User Stories Extracted**:

```
ERROR: No user stories extracted from plan
Plan may be too abstract. Ensure plan has concrete phases with tasks.
Check plan sections: Executive Summary, Implementation Phases, Key Deliverables.
```

**Invalid Task ID Format**:

```
ERROR: Invalid task ID format: "TASK-1.1"
Must use: ENABLER-X.Y for enablers, P1-X.Y.Z for P1 tasks
Example: ENABLER-1.1, P1-1.1.1, P2-2.1.3
```

**Circular Dependency Detected**:

```
ERROR: Circular dependency detected: P1-1.1.2 → P1-1.1.3 → P1-1.1.2
Fix: Ensure tasks within a story are sequential, not circular.
```

**TaskCreate Failed**:

```
ERROR: TaskCreate failed for P1-1.1.1
Reason: Task with same subject already exists
Solution: Check TaskList() for existing tasks before creating
```

## Memory Protocol (MANDATORY)

**Before starting:**

```bash
cat .claude/context/memory/learnings.md
```

Check for:

- Previously created task breakdowns
- Common task ID patterns for this project
- User preferences for prioritization
- Known issues with plan-generator output

**After completing:**

- New task breakdown created → Append to `.claude/context/memory/learnings.md`
  ```
  ## Task Breakdown: {feature-name} ({date})
  - Plan: {plan-file}
  - Output: {task-file}
  - Enablers: {count}
  - User Stories: P1={count}, P2={count}, P3={count}
  - Tasks Created: {yes/no}, Count={count}
  ```
- Issue found → Append to `.claude/context/memory/issues.md`
  ```
  ## Issue: {description} ({date})
  - Context: task-breakdown skill processing {plan-file}
  - Problem: {what went wrong}
  - Workaround: {how it was resolved}
  ```
- Decision made → Append to `.claude/context/memory/decisions.md`
  ```
  ## [ADR-XXX] {title}
  - Date: {date}
  - Context: {why decision was needed}
  - Decision: {what was decided}
  - Consequences: {impact}
  ```

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.
