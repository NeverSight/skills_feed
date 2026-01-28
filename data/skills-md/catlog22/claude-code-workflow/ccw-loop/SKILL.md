---
name: CCW Loop
description: Stateless iterative development loop workflow with documented progress. Supports develop, debug, and validate phases with file-based state tracking. Triggers on "ccw-loop", "dev loop", "development loop", "开发循环", "迭代开发".
argument-hint: TASK="<task description>" [--loop-id=<id>] [--auto]
---

# CCW Loop - Codex Stateless Iterative Development Workflow

Stateless iterative development loop using Codex subagent pattern. Supports develop, debug, and validate phases with file-based state tracking.

## Arguments

| Arg | Required | Description |
|-----|----------|-------------|
| TASK | No | Task description (for new loop, mutually exclusive with --loop-id) |
| --loop-id | No | Existing loop ID to continue (from API or previous session) |
| --auto | No | Auto-cycle mode (develop -> debug -> validate -> complete) |

## Unified Architecture (Codex Subagent Pattern)

```
+-------------------------------------------------------------+
|                     Dashboard (UI)                           |
|  [Create] [Start] [Pause] [Resume] [Stop] [View Progress]    |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|              loop-v2-routes.ts (Control Plane)               |
|                                                              |
|  State: .workflow/.loop/{loopId}.json (MASTER)                         |
|  Tasks: .workflow/.loop/{loopId}.tasks.jsonl                           |
|                                                              |
|  /start -> Trigger ccw-loop skill with --loop-id             |
|  /pause -> Set status='paused' (skill checks before action)  |
|  /stop  -> Set status='failed' (skill terminates)            |
|  /resume -> Set status='running' (skill continues)           |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|               ccw-loop Skill (Execution Plane)               |
|                                                              |
|  Codex Pattern: spawn_agent -> wait -> send_input -> close   |
|                                                              |
|  Reads/Writes: .workflow/.loop/{loopId}.json (unified state)           |
|  Writes: .workflow/.loop/{loopId}.progress/* (progress files)          |
|                                                              |
|  BEFORE each action:                                         |
|    -> Check status: paused/stopped -> exit gracefully        |
|    -> running -> continue with action                        |
|                                                              |
|  Actions: init -> develop -> debug -> validate -> complete   |
+-------------------------------------------------------------+
```

## Key Design Principles (Codex Adaptation)

1. **Unified State**: API and Skill share `.workflow/.loop/{loopId}.json` state file
2. **Control Signals**: Skill checks status field before each action (paused/stopped)
3. **File-Driven**: All progress documented in `.workflow/.loop/{loopId}.progress/`
4. **Resumable**: Continue any loop with `--loop-id`
5. **Dual Trigger**: Supports API trigger (`--loop-id`) and direct call (task description)
6. **Single Agent Deep Interaction**: Use send_input for multi-phase execution instead of multiple agents

## Subagent 机制

### 核心 API

| API | 作用 |
|-----|------|
| `spawn_agent({ message })` | 创建 subagent，返回 `agent_id` |
| `wait({ ids, timeout_ms })` | 等待结果（唯一取结果入口） |
| `send_input({ id, message })` | 继续交互/追问 |
| `close_agent({ id })` | 关闭回收（不可逆） |

### 可用模式

- **单 Agent 深度交互**: 一个 agent 多阶段，`send_input` 继续
- **多 Agent 并行**: 主协调器 + 多 worker，`wait({ ids: [...] })` 批量等待
- **混合模式**: 按需组合

## Execution Modes

### Mode 1: Interactive

User manually selects each action, suitable for complex tasks.

```
User -> Select action -> Execute -> View results -> Select next action
```

### Mode 2: Auto-Loop

Automatic execution in preset order, suitable for standard development flow.

```
Develop -> Debug -> Validate -> (if issues) -> Develop -> ...
```

## Session Structure (Unified Location)

```
.workflow/.loop/
+-- {loopId}.json              # Master state file (API + Skill shared)
+-- {loopId}.tasks.jsonl       # Task list (API managed)
+-- {loopId}.progress/         # Skill progress files
    +-- develop.md             # Development progress timeline
    +-- debug.md               # Understanding evolution document
    +-- validate.md            # Validation report
    +-- changes.log            # Code changes log (NDJSON)
    +-- debug.log              # Debug log (NDJSON)
```

## Implementation (Codex Subagent Pattern)

### Session Setup

```javascript
// Helper: Get UTC+8 (China Standard Time) ISO string
const getUtc8ISOString = () => new Date(Date.now() + 8 * 60 * 60 * 1000).toISOString()

// loopId source:
// 1. API trigger: from --loop-id parameter
// 2. Direct call: generate new loop-v2-{timestamp}-{random}

const loopId = args['--loop-id'] || (() => {
  const timestamp = getUtc8ISOString().replace(/[-:]/g, '').split('.')[0]
  const random = Math.random().toString(36).substring(2, 10)
  return `loop-v2-${timestamp}-${random}`
})()

const loopFile = `.workflow/.loop/${loopId}.json`
const progressDir = `.workflow/.loop/${loopId}.progress`

// Create progress directory
mkdir -p "${progressDir}"
```

### Main Execution Flow (Single Agent Deep Interaction)

```javascript
// ==================== CODEX CCW-LOOP: SINGLE AGENT ORCHESTRATOR ====================

// Step 1: Read or create initial state
let state = null
if (existingLoopId) {
  state = JSON.parse(Read(`.workflow/.loop/${loopId}.json`))
  if (!state) {
    console.error(`Loop not found: ${loopId}`)
    return
  }
} else {
  state = createInitialState(loopId, taskDescription)
  Write(`.workflow/.loop/${loopId}.json`, JSON.stringify(state, null, 2))
}

// Step 2: Create orchestrator agent (single agent handles all phases)
const agent = spawn_agent({
  message: `
## TASK ASSIGNMENT

### MANDATORY FIRST STEPS (Agent Execute)
1. **Read role definition**: ~/.codex/agents/ccw-loop-executor.md (MUST read first)
2. Read: .workflow/project-tech.json
3. Read: .workflow/project-guidelines.json

---

## LOOP CONTEXT

- **Loop ID**: ${loopId}
- **State File**: .workflow/.loop/${loopId}.json
- **Progress Dir**: ${progressDir}
- **Mode**: ${mode}  // 'interactive' or 'auto'

## CURRENT STATE

${JSON.stringify(state, null, 2)}

## TASK DESCRIPTION

${taskDescription}

## EXECUTION INSTRUCTIONS

You are executing CCW Loop orchestrator. Your job:

1. **Check Control Signals**
   - Read .workflow/.loop/${loopId}.json
   - If status === 'paused' -> Output "PAUSED" and stop
   - If status === 'failed' -> Output "STOPPED" and stop
   - If status === 'running' -> Continue

2. **Select Next Action**
   Based on skill_state:
   - If not initialized -> Execute INIT
   - If mode === 'interactive' -> Output MENU and wait for input
   - If mode === 'auto' -> Auto-select based on state

3. **Execute Action**
   - Follow action instructions from ~/.codex/skills/ccw-loop/phases/actions/
   - Update progress files in ${progressDir}/
   - Update state in .workflow/.loop/${loopId}.json

4. **Output Format**
   \`\`\`
   ACTION_RESULT:
   - action: {action_name}
   - status: success | failed | needs_input
   - message: {user message}
   - state_updates: {JSON of skill_state updates}

   NEXT_ACTION_NEEDED: {action_name} | WAITING_INPUT | COMPLETED | PAUSED
   \`\`\`

## FIRST ACTION

${!state.skill_state ? 'Execute: INIT' : mode === 'auto' ? 'Auto-select next action' : 'Show MENU'}
`
})

// Step 3: Main orchestration loop
let iteration = 0
const maxIterations = state.max_iterations || 10

while (iteration < maxIterations) {
  iteration++

  // Wait for agent output
  const result = wait({ ids: [agent], timeout_ms: 600000 })
  const output = result.status[agent].completed

  // Parse action result
  const actionResult = parseActionResult(output)

  // Handle different outcomes
  switch (actionResult.next_action) {
    case 'COMPLETED':
    case 'PAUSED':
    case 'STOPPED':
      close_agent({ id: agent })
      return actionResult

    case 'WAITING_INPUT':
      // Interactive mode: display menu, get user choice
      const userChoice = await displayMenuAndGetChoice(actionResult)

      // Send user choice back to agent
      send_input({
        id: agent,
        message: `
## USER INPUT RECEIVED

Action selected: ${userChoice.action}
${userChoice.data ? `Additional data: ${JSON.stringify(userChoice.data)}` : ''}

## EXECUTE SELECTED ACTION

Follow instructions for: ${userChoice.action}
Update state and progress files accordingly.
`
      })
      break

    default:
      // Auto mode: agent continues to next action
      // Check if we need to prompt for continuation
      if (actionResult.next_action && actionResult.next_action !== 'NONE') {
        send_input({
          id: agent,
          message: `
## CONTINUE EXECUTION

Previous action completed: ${actionResult.action}
Result: ${actionResult.status}

## EXECUTE NEXT ACTION

Continue with: ${actionResult.next_action}
`
        })
      }
  }

  // Update iteration count in state
  const currentState = JSON.parse(Read(`.workflow/.loop/${loopId}.json`))
  currentState.current_iteration = iteration
  currentState.updated_at = getUtc8ISOString()
  Write(`.workflow/.loop/${loopId}.json`, JSON.stringify(currentState, null, 2))
}

// Step 4: Cleanup
close_agent({ id: agent })
```

## Action Catalog

| Action | Purpose | Output Files | Trigger |
|--------|---------|--------------|---------|
| [action-init](phases/actions/action-init.md) | Initialize loop session | meta.json, state.json | First run |
| [action-develop](phases/actions/action-develop.md) | Execute development task | progress.md, tasks.json | Has pending tasks |
| [action-debug](phases/actions/action-debug.md) | Hypothesis-driven debug | understanding.md, hypotheses.json | Needs debugging |
| [action-validate](phases/actions/action-validate.md) | Test and validate | validation.md, test-results.json | Needs validation |
| [action-complete](phases/actions/action-complete.md) | Complete loop | summary.md | All done |
| [action-menu](phases/actions/action-menu.md) | Display action menu | - | Interactive mode |

## Usage

```bash
# Start new loop (direct call)
/ccw-loop TASK="Implement user authentication"

# Continue existing loop (API trigger or manual resume)
/ccw-loop --loop-id=loop-v2-20260122-abc123

# Auto-cycle mode
/ccw-loop --auto TASK="Fix login bug and add tests"

# API triggered auto-cycle
/ccw-loop --loop-id=loop-v2-20260122-abc123 --auto
```

## Reference Documents

| Document | Purpose |
|----------|---------|
| [phases/orchestrator.md](phases/orchestrator.md) | Orchestrator: state reading + action selection |
| [phases/state-schema.md](phases/state-schema.md) | State structure definition |
| [specs/loop-requirements.md](specs/loop-requirements.md) | Loop requirements specification |
| [specs/action-catalog.md](specs/action-catalog.md) | Action catalog |

## Error Handling

| Situation | Action |
|-----------|--------|
| Session not found | Create new session |
| State file corrupted | Rebuild from file contents |
| Agent timeout | send_input to request convergence |
| Agent unexpectedly closed | Re-spawn, paste previous output |
| Tests fail | Loop back to develop/debug |
| >10 iterations | Warn user, suggest break |

## Codex Best Practices Applied

1. **Role Path Passing**: Agent reads role file itself (no content embedding)
2. **Single Agent Deep Interaction**: Use send_input for multi-phase instead of multiple agents
3. **Delayed close_agent**: Only close after confirming no more interaction needed
4. **Context Reuse**: Same agent maintains all exploration context automatically
5. **Explicit wait()**: Always use wait({ ids }) to get results, not close_agent
