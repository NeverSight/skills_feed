---
name: task-orchestration
description: "Load PROACTIVELY when decomposing a user request into parallel agent work. Use when user says \"build this\", \"implement this feature\", or any request requiring multiple agents working concurrently. Guides task decomposition into parallelizable units, agent assignment with skill matching, dependency graph construction, and result aggregation. The runtime engine handles WRFC chain coordination automatically via <gv> directives."
metadata:
  version: 2.0.0
  category: orchestration
  tags: [orchestration, decomposition, agents, parallel, wrfc, coordination]
---

## Resources
```
scripts/
  validate-orchestration.sh
references/
  agent-assignment-guide.md
```

# Task Orchestration Protocol

The task orchestration protocol defines how the GoodVibes orchestrator decomposes feature requests into agent tasks, assigns agents and skills, manages parallel execution, and interacts with the runtime engine's WRFC chain system. This is the orchestrator's primary workflow for multi-agent feature delivery.

## When to Use This Skill

Use this skill when:

- User provides a feature request requiring multiple work streams
- Request involves multiple domains (backend, frontend, database, etc.)
- Request can be parallelized into independent subtasks
- Request requires coordination across multiple agents

Do NOT use this skill for:

- Simple single-file edits (handle directly)
- Pure analysis tasks without code changes
- Tasks already decomposed by the user

## Runtime Engine and WRFC Chains

The runtime engine manages Work-Review-Fix-Complete (WRFC) chains automatically. The orchestrator's role is:

1. **Decompose** the task into work agents
2. **Spawn** the initial work agents
3. **Execute `<gv>` directives** issued by the runtime engine — mechanically, immediately, without judgment

The runtime engine handles all review, fix, and completion decisions. The orchestrator does NOT manually spawn reviewers or fix agents. These come exclusively from runtime directives after each work agent completes.

### Directive Types

The runtime engine issues directives to the orchestrator via system messages containing `<gv>` tags:

```json
{"action":"spawn","wid":"wrfc_xxx","type":"reviewer","task":"Review the code..."}
{"action":"spawn","wid":"wrfc_xxx","type":"engineer","task":"Fix the issues..."}
{"action":"complete","wid":"wrfc_xxx"}
{"action":"escalate","wid":"wrfc_xxx","reason":"Max fix attempts reached"}
```

### Directive Compliance Rules

**These 4 rules are absolute and non-negotiable:**

1. **Immediate**: Execute directives the moment they arrive. NEVER defer, queue, or delay.
2. **First**: Execute directives BEFORE any other action. No intervening tool calls, no additional agent spawns, no user messages first.
3. **Autonomy ends**: Once the first directive arrives for a WRFC chain, the orchestrator has no further judgment over that chain. Only directives drive it.
4. **Runtime supersedes**: Runtime workflow logic ALWAYS supersedes orchestrator judgment. If a directive says review, review. If it says complete, complete.

### Configurable Thresholds

The runtime reads `goodvibes.json` for:
- `min_review_score` (default: 9.5) — score threshold for PASS
- `max_fix_attempts` (default: 3) — max fix cycles before escalation

The orchestrator never hardcodes these values. The runtime engine enforces them.

## Decomposition Process

### Step 1: Classify the Request

Before decomposing, classify the request into one of these categories:

**Feature Implementation** - Add new functionality
- Identify: "Add X feature", "Implement Y", "Create Z capability"
- Decomposition strategy: Split by domain (API, UI, DB, types)
- Parallelism: High (most work streams independent)

**Bug Fix** - Resolve existing issue
- Identify: "Fix X not working", "Resolve Y error", "Correct Z behavior"
- Decomposition strategy: Root cause first, then fix propagation
- Parallelism: Low (diagnosis must precede fixes)

**Refactoring** - Improve code structure without changing behavior
- Identify: "Refactor X", "Restructure Y", "Extract Z"
- Decomposition strategy: Analysis first, then file-by-file changes
- Parallelism: Medium (analysis sequential, changes parallel)

**Integration** - Connect existing systems
- Identify: "Integrate X with Y", "Connect A to B"
- Decomposition strategy: Understand both sides, then adapter layer
- Parallelism: Medium (research parallel, integration sequential)

**Enhancement** - Improve existing feature
- Identify: "Improve X", "Add Y to existing Z"
- Decomposition strategy: Understand current state, plan incremental additions
- Parallelism: Medium (discovery sequential, additions parallel)

### Step 2: Identify Parallel Opportunities

After classifying, identify work that can run in parallel:

**Independent domains:**
- API route + React component (if contract is defined upfront)
- Type definitions + database schema
- Multiple UI components with shared types
- Multiple API endpoints with shared middleware

**Independent files:**
- Creating new files in different directories
- Editing files with no import relationships
- Writing tests for different modules

**Independent research:**
- Checking multiple documentation sources
- Analyzing multiple files for patterns
- Discovering patterns in different directories

**When NOT to parallelize:**
- Type definitions must exist before implementation uses them
- Database schema must exist before API queries it
- Parent component must exist before child imports it
- Discovery must complete before planning

### Step 3: Define Agent Tasks

For each parallelizable work stream, define a task with:

**Task structure:**
```yaml
task_id: unique-task-identifier
agent: engineer | reviewer | tester | architect | deployer | integrator-ai | integrator-services | integrator-state | planner
skills: [skill-1, skill-2]
description: Brief description of what this task accomplishes
scope:
  files: [list of files to create/modify]
  directories: [directories to work within]
constraints:
  - Must use TypeScript
  - Follow existing patterns in src/features/
blocking: [list of task_ids this task blocks]
blocked_by: [list of task_ids blocking this task]
expected_outcome: What success looks like
```

**Example:**
```yaml
task_id: create-user-types
agent: engineer
skills: [gather-plan-apply, precision-mastery, error-recovery, goodvibes-memory]
description: Create TypeScript type definitions for User domain
scope:
  files: [src/types/user.ts, src/types/auth.ts]
  directories: [src/types]
constraints:
  - Use Zod for runtime validation
  - Export all types from src/types/index.ts
blocking: [create-user-api, create-user-components]
blocked_by: []
expected_outcome: Type files exist, export User, AuthContext, and validation schemas
```

### Step 4: Assign Agent and Skills

For each task, assign the appropriate agent type and skills using this decision table:

**Agent Type Selection:**

| Work Type | Agent Type | Rationale |
|-----------|------------|-----------|
| Implement API, components, features | engineer | Code creation and implementation |
| Review code quality, standards | reviewer | Code quality and standards enforcement |
| Write tests, test coverage | tester | Testing and validation |
| Plan architecture, design decisions | architect | High-level design and planning |
| Deploy applications, infrastructure | deployer | Deployment and infrastructure |
| Integrate AI/ML services | integrator-ai | AI/ML integration |
| Integrate external services | integrator-services | External service integration |
| Manage state and data flow | integrator-state | State management |
| Coordinate complex workflows | planner | High-level orchestration |

**Skills Assignment:**

All agents receive protocol skills by default:
- gather-plan-apply (GPA loop)
- precision-mastery (tool usage)
- error-recovery (error handling)
- goodvibes-memory (memory integration)

Additional skills by work type:

| Work Type | Additional Skills |
|-----------|-------------------|
| API implementation | trpc, prisma, nextauth, rest-api-design |
| Frontend components | react, nextjs, tailwindcss, shadcn-ui |
| Database schema | prisma, postgresql, drizzle |
| Authentication | clerk, nextauth, lucia |
| Type definitions | (none - protocol skills sufficient) |
| Code review | review-scoring + domain-specific review skills |

See `references/agent-assignment-guide.md` for complete assignment table.

## Agent Prompt Template

When spawning agents, ALWAYS include these elements in the agent prompt:

```markdown
## Task
[Specific, actionable description of what to accomplish]

## Scope
**Files to create:**
- path/to/file.ts - Brief description

**Files to modify:**
- path/to/existing.ts - What changes to make

**Directories in scope:**
- src/features/auth/ - Work within this directory

## Constraints
- [Technical constraint 1]
- [Pattern to follow]
- [Dependency requirement]

## Skills Available
- skill-name - When to use it
- skill-name - When to use it

## Expected Outcome
[Concrete definition of success]

## Blocking/Blocked By
**This task blocks:** [list of downstream tasks waiting for this]
**This task is blocked by:** [list of upstream tasks this waits for]
```

**Critical elements:**
1. Scope is explicit (file paths, not vague descriptions)
2. Skills are listed with usage guidance
3. Expected outcome is concrete and verifiable
4. Output format includes the `<gv>` tag (emitted automatically by the runtime hook; the orchestrator does not need to instruct agents about this)

**Note:** Do NOT add WRFC participation instructions to agent prompts. Agents only need to complete their work and emit a `<gv>` tag. The runtime engine handles the WRFC chain automatically.

## Monitoring and Coordination

### Track Active Agents

Maintain a task tracking structure:

```yaml
active_tasks:
  task-1:
    agent_id: agent_abc123
    status: running | completed | blocked | failed
    started_at: ISO-8601 timestamp
    last_update: ISO-8601 timestamp
    blocking: [task-2, task-3]
    blocked_by: []
  task-2:
    agent_id: agent_def456
    status: waiting
    blocked_by: [task-1]
```

### Agent Concurrency Limits

**Hard limit: 6 concurrent agent chains (from `max_parallel_agent_chains` in output style config)**

A "chain" includes the work agent plus its entire WRFC chain (review, fix, re-review). Each initial work agent spawn creates one chain. Count chains, not individual agents.

When you have more than 6 tasks:
1. Prioritize by dependency order (unblock downstream tasks first)
2. Queue remaining tasks
3. Spawn new agents as chains complete (when runtime issues `complete` directive)

**Task priority formula:**
```
priority = (number of tasks it blocks) - (number of tasks blocking it)
```

Higher priority = spawn first

### Executing `<gv>` Directives

When the runtime engine issues a directive:

1. **Stop everything** — do not complete any in-progress reasoning about other tasks
2. **Read the directive** — identify the `action`, `wid`, `type`, and `task` fields
3. **Execute immediately**:
   - `spawn`: Spawn the specified agent type with the provided task prompt
   - `complete`: Mark the WRFC chain as done, unblock any dependent tasks, spawn next queued task if slot available
   - `escalate`: Report to user with the escalation reason, do not spawn further agents for this chain
4. **Then resume** other orchestration work

**No exceptions.** A directive is never skipped, reordered, or conditioned on another event.

### WRFC Spawn Rules

1. **Initial spawns only**: Orchestrator spawns ONLY the initial work agents from task decomposition. All reviewer and fix agent spawns come from runtime directives.
2. **Parallel when possible**: Spawn all tasks in the same dependency wave together
3. **Wait for blockers**: Do NOT spawn dependent tasks until blocking tasks have received `complete` directives
4. **Respect the limit**: Do NOT exceed 6 concurrent chains
5. **Escalation handling**: If runtime issues `escalate`, report to user — do not attempt to fix the chain yourself

### Agent Communication

Agents do NOT communicate directly. All coordination flows through the orchestrator:

**Inter-agent dependencies:**
- Task A produces types.ts
- Task B needs types.ts
- Orchestrator: waits for A to receive `complete` directive, then spawns B with reference to types.ts location

**Shared state:**
- All agents read/write .goodvibes/memory/
- Orchestrator checks memory for decisions, patterns, failures before spawning
- Orchestrator logs orchestration decisions to .goodvibes/memory/decisions.json

## Mode-Specific Behavior

### Vibecoding Mode (Default)

**Confirm before initial decomposition:**
- Show task breakdown to user before spawning any agents
- Allow user to modify the decomposition
- Only the initial decomposition requires user confirmation; once agents are running, the runtime drives the process

**Auto-spawn on ambiguity:**
- If task decomposition has multiple valid approaches, pick the most common pattern from memory
- If no pattern exists, make a decision and log it to decisions.json
- Only escalate to user for architectural decisions (auth provider, database choice, etc.)

**Error handling:**
- Agent retries are managed by the runtime engine (up to `max_fix_attempts`)
- Runtime will issue `escalate` directive if max attempts are reached
- On `escalate`, present to user with context from the directive's `reason` field

### Justvibes Mode (Strict)

**Auto-proceed:**
- Skip the pre-decomposition confirmation
- Spawn agents immediately after decomposition is complete
- Runtime engine handles all WRFC cycles automatically

**Error handling:**
- Same as vibecoding — runtime manages fix attempts and issues `escalate` when exhausted
- Present escalation to user when received

## Decomposition Examples

### Example 1: Feature Implementation

**User request:** "Add user profile page with edit capability"

**Classification:** Feature Implementation

**Decomposition:**

```yaml
tasks:
  - task_id: create-profile-types
    agent: engineer
    skills: [gather-plan-apply, precision-mastery, error-recovery, goodvibes-memory]
    description: Create Profile and ProfileUpdate types
    scope:
      files: [src/types/profile.ts]
    blocking: [create-profile-api, create-profile-ui]
    blocked_by: []
    
  - task_id: create-profile-api
    agent: engineer
    skills: [gather-plan-apply, precision-mastery, error-recovery, goodvibes-memory, trpc, prisma]
    description: Implement tRPC routes for profile CRUD
    scope:
      files: [src/server/routers/profile.ts]
    blocking: [create-profile-ui]
    blocked_by: [create-profile-types]
    
  - task_id: create-profile-ui
    agent: engineer
    skills: [gather-plan-apply, precision-mastery, error-recovery, goodvibes-memory, nextjs, react, tailwindcss, shadcn-ui]
    description: Build profile page with edit form
    scope:
      files: [src/app/profile/page.tsx, src/components/ProfileForm.tsx]
    blocking: []
    blocked_by: [create-profile-types]
    
  - task_id: test-profile-feature
    agent: tester
    skills: [gather-plan-apply, precision-mastery, error-recovery, goodvibes-memory]
    description: Create tests for profile feature
    scope:
      files: [src/server/routers/profile.test.ts, src/components/ProfileForm.test.tsx]
    blocking: []
    blocked_by: [create-profile-api, create-profile-ui]
```

**Execution plan:**
1. Spawn create-profile-types (no blockers)
2. Wait for `complete` directive for create-profile-types
3. Spawn create-profile-api and create-profile-ui in parallel (both unblocked)
4. Wait for `complete` directives for both
5. Spawn test-profile-feature (blocked by API + UI)
6. Wait for `complete` directive for test-profile-feature
7. Aggregate results and return to user

**Note:** Review and fix cycles for each agent are handled automatically by the runtime engine via directives. The orchestrator does not schedule them.

**Parallelism:** 3 waves (types solo -> API + UI parallel -> tests solo)

### Example 2: Bug Fix

**User request:** "Fix login redirect loop on /dashboard"

**Classification:** Bug Fix

**Decomposition:**

```yaml
tasks:
  - task_id: diagnose-redirect-loop
    agent: engineer
    skills: [gather-plan-apply, precision-mastery, error-recovery, goodvibes-memory, nextjs, nextauth]
    description: Identify root cause of redirect loop
    scope:
      files: [src/middleware.ts, src/app/dashboard/page.tsx, src/lib/auth.ts]
    blocking: [fix-redirect-loop]
    blocked_by: []
    
  - task_id: fix-redirect-loop
    agent: engineer
    skills: [gather-plan-apply, precision-mastery, error-recovery, goodvibes-memory, nextjs, nextauth]
    description: Apply fix based on diagnosis
    scope:
      files: [determined by diagnosis]
    blocking: []
    blocked_by: [diagnose-redirect-loop]
```

**Execution plan:**
1. Spawn diagnose-redirect-loop
2. Wait for `complete` directive for diagnosis
3. Spawn fix-redirect-loop with diagnosis context
4. Wait for `complete` directive for fix
5. Return to user

**Parallelism:** None (fully sequential: diagnose -> fix)

### Example 3: Refactoring

**User request:** "Extract shared auth logic into reusable hooks"

**Classification:** Refactoring

**Decomposition:**

```yaml
tasks:
  - task_id: plan-refactoring-approach
    agent: architect
    skills: [gather-plan-apply, precision-mastery, error-recovery, goodvibes-memory]
    description: Design the refactoring strategy and hook API
    scope:
      directories: [src/components, src/app]
    blocking: [analyze-auth-patterns]
    blocked_by: []
    
  - task_id: analyze-auth-patterns
    agent: engineer
    skills: [gather-plan-apply, precision-mastery, error-recovery, goodvibes-memory]
    description: Discover all auth usage patterns in components
    scope:
      directories: [src/components, src/app]
    blocking: [create-auth-hooks]
    blocked_by: [plan-refactoring-approach]
    
  - task_id: create-auth-hooks
    agent: engineer
    skills: [gather-plan-apply, precision-mastery, error-recovery, goodvibes-memory, react]
    description: Create hooks based on discovered patterns
    scope:
      files: [src/hooks/useAuth.ts, src/hooks/useRequireAuth.ts]
    blocking: [refactor-components-1, refactor-components-2]
    blocked_by: [analyze-auth-patterns]
    
  - task_id: refactor-components-1
    agent: engineer
    skills: [gather-plan-apply, precision-mastery, error-recovery, goodvibes-memory, react]
    description: Refactor components in src/app to use hooks
    scope:
      directories: [src/app]
    blocking: []
    blocked_by: [create-auth-hooks]
    
  - task_id: refactor-components-2
    agent: engineer
    skills: [gather-plan-apply, precision-mastery, error-recovery, goodvibes-memory, react]
    description: Refactor components in src/components to use hooks
    scope:
      directories: [src/components]
    blocking: []
    blocked_by: [create-auth-hooks]
```

**Execution plan:**
1. Spawn plan-refactoring-approach (architect)
2. Wait for `complete` directive for planning
3. Spawn analyze-auth-patterns
4. Wait for `complete` directive for analysis
5. Spawn create-auth-hooks
6. Wait for `complete` directive for hooks
7. Spawn refactor-components-1 and refactor-components-2 in parallel
8. Wait for `complete` directives for both
9. Return to user

**Parallelism:** 4 waves (planning -> analysis -> hooks -> 2 refactors parallel)

## Escalation Criteria

Escalate to user immediately when:

1. **Architectural ambiguity** - Multiple valid approaches with significant tradeoffs
   - Example: "Use REST vs GraphQL for new API"
   - Escalation: Present options with pros/cons, request decision

2. **Missing information** - Task cannot be completed without user input
   - Example: "Which auth provider should we use?"
   - Escalation: List options, explain what's needed

3. **Scope expansion** - Task is larger than initially described
   - Example: "Adding profile page requires new database schema and migration"
   - Escalation: Show expanded scope, request approval

4. **Runtime escalation** - Runtime engine issues `escalate` directive
   - Example: Max fix attempts reached on a work agent
   - Escalation: Present the `reason` from the directive, request guidance or manual intervention

5. **Conflicting requirements** - Discovered constraints contradict each other
   - Example: "User wants Prisma but codebase uses Drizzle"
   - Escalation: Explain conflict, request resolution

## Summary

**Task orchestration workflow:**
1. Classify request (feature, bug, refactoring, etc.)
2. Identify parallel opportunities (domains, files, research)
3. Define agent tasks (task structure with blocking/blocked_by)
4. Assign agents and skills (use decision table)
5. Spawn initial work agents with structured prompts
6. Monitor active chains (up to 6 concurrent)
7. Execute `<gv>` directives from runtime immediately and mechanically
8. Aggregate results when all chains receive `complete` directives

**Key principles:**
- Explicit > implicit (file paths, not vague descriptions)
- Parallel when possible, sequential when necessary
- Orchestrator handles initial decomposition; runtime engine handles all WRFC cycles
- Execute directives before any other action — no exceptions
- Escalate on ambiguity in vibecoding, auto-proceed in justvibes
- Use memory to inform decisions and avoid repeating failures
