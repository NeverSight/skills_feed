---
name: strategic-compact
description: Strategic compaction suggestion framework that monitors session complexity and suggests context compaction at optimal logical boundaries rather than arbitrary thresholds.
allowed-tools: Read, Bash
---

# Strategic Compact Skill

A framework for intelligently suggesting context compaction at optimal moments during long coding sessions, preserving work continuity while managing context window limitations.

## Design Philosophy

### Why Strategic Compaction > Auto-Compaction

Auto-compaction operates on simple thresholds (token count, time elapsed) without understanding the semantic state of your work. This leads to several problems:

1. **Mid-Task Disruption**: Auto-compact might trigger while you're debugging a complex issue, losing the mental model you've built up over many interactions.

2. **Context Fragmentation**: Arbitrary cutoffs create artificial boundaries in your work history, making it harder to understand the full picture when resuming.

3. **Lost Continuity**: Important context about "why" decisions were made gets compacted away at random points rather than preserved at meaningful boundaries.

4. **Incomplete State**: Compacting mid-implementation can lose track of partially completed work, leading to duplicated effort or missed steps.

**Strategic compaction** instead:

- Monitors for **logical boundaries** in your work (task completion, phase transitions)
- Considers the **semantic state** of the session (actively debugging vs. between tasks)
- Provides **suggestions** rather than forcing compaction
- Integrates with **context-saver** to preserve critical state before compaction
- Respects your **workflow rhythm** rather than imposing arbitrary limits

The goal is compaction that feels like a natural pause point, not an interruption.

---

## When to Use

This skill operates primarily through the **PreToolUse hook**, passively monitoring session state and providing suggestions at appropriate moments.

### Automatic Monitoring (PreToolUse Hook)

The skill attaches to every tool call, maintaining counters and evaluating whether the current moment represents a good compaction opportunity.

### Manual Invocation

You can also invoke the skill directly:
- `/strategic-compact` - Check current session state and get recommendation
- `/strategic-compact status` - View tool counts and threshold proximity
- `/strategic-compact now` - Force a compaction suggestion (with context-saver integration)

---

## Tool Call Tracking Mechanism

### How to Count Tool Calls

The skill maintains session state by tracking tool invocations. This is implemented through the PreToolUse hook which fires before each tool execution.

```yaml
# Session State Structure
session_state:
  tool_counts:
    total: 0              # All tool calls
    significant: 0        # Tools that modify state or are complex
    read_operations: 0    # Read, Glob, Grep operations
    write_operations: 0   # Write, Edit, Bash operations
    navigation: 0         # Directory changes, file searches

  boundaries:
    tasks_completed: 0    # TaskUpdate with status=completed
    phases_completed: 0   # Major implementation phases
    commits_made: 0       # Successful git commits

  flags:
    active_debugging: false    # Currently in debug cycle
    active_implementation: false  # Mid-feature implementation
    last_error_count: 0       # Errors in recent tool calls

  timestamps:
    session_start: null
    last_boundary: null       # Last logical boundary crossed
    last_suggestion: null     # Avoid repeated suggestions
```

### Which Tools to Count

**Significant Tools** (count toward threshold):
- `Edit` - File modifications
- `Write` - File creation/overwrite
- `Bash` - Command execution (especially git, npm, build commands)
- `NotebookEdit` - Jupyter modifications
- `TaskUpdate` - Task state changes

**Tracked but Weighted Lower**:
- `Read` - File reading (0.5 weight)
- `Glob` - File pattern matching (0.3 weight)
- `Grep` - Content searching (0.3 weight)
- `WebFetch` / `WebSearch` - External lookups (0.5 weight)

**Boundary Markers** (reset considerations):
- `TaskUpdate` with `status: completed` - Task boundary
- `Bash` with `git commit` - Commit boundary
- Skill invocations for phase completion

### Session State Tracking

State is maintained in-memory during the session. The PreToolUse hook updates counters before each tool execution:

```python
# Pseudocode for state tracking
def on_pre_tool_use(tool_name, parameters):
    state = get_session_state()

    # Update counters
    state.tool_counts.total += 1
    state.tool_counts[categorize(tool_name)] += get_weight(tool_name)

    # Check for boundary markers
    if is_boundary_marker(tool_name, parameters):
        state.boundaries[get_boundary_type(tool_name, parameters)] += 1
        state.timestamps.last_boundary = now()

    # Update activity flags
    update_activity_flags(state, tool_name, parameters)

    # Evaluate suggestion opportunity
    if should_suggest_compact(state):
        return generate_suggestion(state)

    return None  # Allow tool to proceed
```

---

## Threshold Configuration

### Default Threshold

The default threshold is **50 significant tool calls** between logical boundaries.

This number is based on:
- Typical context window capacity for detailed work
- Average session complexity before context becomes "stale"
- Balance between interruption frequency and context quality

### How to Configure Custom Thresholds

Thresholds can be configured in your project's `.claude/settings.json`:

```json
{
  "skills": {
    "strategic-compact": {
      "thresholds": {
        "default": 50,
        "aggressive": 30,
        "relaxed": 75,
        "never": -1
      },
      "active_threshold": "default",
      "boundary_weight": {
        "task_completion": 0.5,
        "commit": 0.3,
        "phase_completion": 0.7
      }
    }
  }
}
```

### Different Thresholds for Different Scenarios

| Scenario | Threshold | Rationale |
|----------|-----------|-----------|
| Standard Development | 50 | Balanced for typical feature work |
| Complex Debugging | 75 | Need more context for issue tracking |
| Quick Fixes | 30 | Less context needed, faster cycles |
| Large Refactoring | 40 | Many files, context can get stale |
| Documentation | 60 | Mostly reading, less state to track |
| Plan Execution | Per-phase | Align with plan phase boundaries |

**Dynamic Threshold Adjustment**:

The skill can adjust thresholds based on detected activity:

```yaml
dynamic_rules:
  - condition: "active_debugging == true"
    adjustment: "+25"
    reason: "Preserve debugging context"

  - condition: "error_rate > 0.3"
    adjustment: "+15"
    reason: "Troubleshooting in progress"

  - condition: "time_since_boundary > 30min"
    adjustment: "-10"
    reason: "Context likely getting stale"
```

---

## Logical Boundaries

The skill identifies optimal compaction moments by recognizing logical boundaries in your work.

### When to Suggest Compact

#### After Completing a Phase/Task

**Strong Signal** - Task completion is the clearest boundary.

```yaml
trigger:
  event: TaskUpdate
  parameters:
    status: completed
  conditions:
    - tool_count.significant >= threshold * 0.6
    - time_since_last_suggestion > 10min
```

Suggestion appears after the task is marked complete, offering a natural pause point.

#### After Major Implementation Milestone

**Strong Signal** - Commits and successful builds indicate stable points.

```yaml
trigger:
  event: Bash
  command_pattern: "git commit"
  result: success
  conditions:
    - tool_count.significant >= threshold * 0.7
    - not pending_tasks_in_current_feature
```

#### Before Starting New Feature

**Medium Signal** - Beginning new work is a good reset point.

```yaml
trigger:
  event: TaskUpdate
  parameters:
    status: in_progress
  conditions:
    - previous_task_completed
    - feature_boundary_detected
    - tool_count.significant >= threshold * 0.5
```

#### When Context is About to Overflow

**Warning Signal** - Proactive suggestion before forced compaction.

```yaml
trigger:
  event: any
  conditions:
    - estimated_context_usage > 0.8
    - tool_count.significant >= threshold * 0.9
  priority: high
```

### When NOT to Suggest Compact

#### During Active Debugging

```yaml
suppress_when:
  - recent_error_count > 0
  - last_tool_was: [Read, Grep, Glob]  # Investigating
  - pattern_detected: "debug_cycle"
  - task_subject_contains: ["debug", "fix", "investigate"]
```

**Rationale**: Debugging requires building up mental models and context. Compacting mid-debug loses the trail of investigation.

#### During Active Implementation

```yaml
suppress_when:
  - uncommitted_changes: true
  - last_tools_sequence: [Edit, Edit, Edit]  # Active coding
  - time_since_last_edit < 5min
  - test_failures_unresolved: true
```

**Rationale**: Mid-implementation compaction risks losing track of partial work and the reasoning behind changes.

#### Other Suppression Conditions

```yaml
suppress_when:
  - last_suggestion < 10min_ago  # Avoid nagging
  - user_deferred_recently: true  # Respect user choice
  - critical_operation_in_progress: true
  - rollback_or_revert_active: true
```

---

## Best Practices

### When to Accept Compact Suggestion

**Accept when**:
- You've just completed a logical unit of work
- The suggestion aligns with a natural pause in your workflow
- You're about to context-switch to a different feature/area
- You've made a commit and tests are passing
- You notice responses are getting slower or less accurate

### When to Defer

**Defer when**:
- You're in the middle of tracking down a bug
- You have uncommitted changes you're still working on
- You're about to run a critical command that needs context
- You're iterating on a specific piece of code
- The current task is almost complete (< 5 minutes remaining)

### How to Preserve Context Before Compact

Before accepting a compaction suggestion, ensure critical context is preserved:

1. **Check for uncommitted work**:
   ```bash
   git status
   git diff --stat
   ```

2. **Review active tasks**:
   ```
   TaskList to see pending work
   ```

3. **Document decision points**:
   - Any architectural decisions made
   - Reasoning behind non-obvious choices
   - Known issues or TODOs discovered

4. **Capture current position**:
   - What file/function you're working in
   - What the next step should be
   - Any blockers or dependencies

### Using context-saver Skill Before Compacting

The strategic-compact skill integrates with the `context-saver` skill to preserve session state:

```yaml
compact_workflow:
  1. Detect compaction opportunity
  2. Check if context-saver is available
  3. If available:
     - Invoke context-saver with current session state
     - Wait for context file creation
     - Include context file path in compact summary
  4. Present compaction suggestion with preserved context reference
  5. If accepted:
     - Perform compaction
     - New session starts with context file reference
```

**Integration Example**:

```
[Strategic Compact Suggestion]

Session Status:
- Tool calls: 67 (threshold: 50)
- Last boundary: Task "Implement auth flow" completed 5 min ago
- Current state: Between tasks, no active debugging

Recommendation: Good time to compact

Before compacting, I'll save your context:
> Invoking context-saver skill...
> Context saved to: .claude/contexts/session-2024-01-15-auth-impl.md

You can reference this context in your next session with:
> "Continue from .claude/contexts/session-2024-01-15-auth-impl.md"

Accept compaction? [Y/n]
```

---

## PreToolUse Hook Configuration

### Example hooks.json Configuration

Create or update `.claude/hooks.json` in your project:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "name": "strategic-compact-monitor",
        "skill": "strategic-compact",
        "enabled": true,
        "priority": 10,
        "config": {
          "threshold": 50,
          "mode": "suggest",
          "integrate_context_saver": true,
          "suppress_during": [
            "debugging",
            "active_implementation",
            "rollback"
          ],
          "boundary_events": [
            "task_completion",
            "git_commit",
            "phase_transition",
            "feature_boundary"
          ]
        }
      }
    ]
  }
}
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `threshold` | number | 50 | Tool calls before suggesting |
| `mode` | string | "suggest" | "suggest", "warn", or "silent" |
| `integrate_context_saver` | boolean | true | Auto-invoke context-saver |
| `suppress_during` | array | [...] | Activity types to suppress during |
| `boundary_events` | array | [...] | Events that count as boundaries |
| `min_interval` | number | 600 | Min seconds between suggestions |
| `dynamic_threshold` | boolean | true | Adjust threshold based on activity |

### How to Enable/Disable

**Enable for a project**:
```bash
# Add to project settings
echo '{"skills": {"strategic-compact": {"enabled": true}}}' > .claude/settings.json
```

**Disable temporarily**:
```
/strategic-compact disable
```

**Disable for session**:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "name": "strategic-compact-monitor",
        "enabled": false
      }
    ]
  }
}
```

### Integration with Claude Code

The skill integrates with Claude Code's hook system:

```
Claude Code Session
      │
      ▼
  PreToolUse Hook
      │
      ▼
  strategic-compact-monitor
      │
      ├── Update counters
      ├── Check boundaries
      ├── Evaluate conditions
      │
      ▼
  [Suggestion or Pass-through]
      │
      ▼
  Tool Execution
      │
      ▼
  PostToolUse (optional logging)
```

---

## Suggestion Message Format

### Clear, Non-Intrusive Suggestions

Suggestions should be informative but not disruptive:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Context Compaction Suggested
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 Session Metrics:
   Tool calls:     72 significant (threshold: 50)
   Session time:   45 minutes
   Last boundary:  Task completed 3 min ago

 Boundary Detected:
   Task "Add user authentication" marked complete
   Git commit: "feat: implement JWT auth flow"
   No pending changes or active debugging

 Recommendation: GOOD TIME TO COMPACT

 Options:
   [1] Compact now (will invoke context-saver first)
   [2] Defer for 15 minutes
   [3] Defer until next boundary
   [4] Dismiss (don't suggest again this session)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Include Current Tool Count

Always show the current state so users understand why the suggestion appeared:

```
Tool Activity Summary:
  - Edits:    23 files modified
  - Reads:    45 files examined
  - Commands: 18 bash operations
  - Searches: 12 grep/glob operations

  Weighted Total: 72 (threshold: 50)
```

### Include Reason for Suggestion

Be explicit about why this moment was chosen:

```
Why now?
  ✓ Task "Implement auth flow" completed
  ✓ Successful commit made
  ✓ All tests passing
  ✓ No uncommitted changes
  ✓ No active debugging session

This is a natural pause point in your workflow.
```

### Minimal Mode (for experienced users)

```
[Compact? 72/50 calls | Task done | Clean state] Y/n/defer
```

---

## Advanced Configuration

### Per-Project Thresholds

Different projects may need different thresholds:

```json
{
  "projects": {
    "large-monorepo": {
      "threshold": 40,
      "reason": "Many files, context gets stale quickly"
    },
    "focused-library": {
      "threshold": 75,
      "reason": "Smaller scope, more context helpful"
    },
    "debugging-session": {
      "threshold": 100,
      "reason": "Need extensive context for investigation"
    }
  }
}
```

### Custom Boundary Definitions

Define project-specific boundaries:

```json
{
  "custom_boundaries": {
    "migration_complete": {
      "trigger": "Bash",
      "pattern": "npm run migrate",
      "success_required": true,
      "weight": 0.8
    },
    "deploy_staging": {
      "trigger": "Bash",
      "pattern": "deploy.*staging",
      "weight": 1.0
    }
  }
}
```

### Integration with Other Skills

The strategic-compact skill can coordinate with:

- **context-saver**: Automatic context preservation before compact
- **implement-phase**: Phase completion as boundary markers
- **create-plan**: Plan phase transitions as boundaries
- **code-review**: Review completion as boundary markers

```yaml
skill_integration:
  context-saver:
    invoke_before_compact: true
    pass_session_state: true

  implement-phase:
    listen_for: phase_complete
    boundary_weight: 1.0

  create-plan:
    listen_for: plan_created
    suggest_compact_after: true
```

---

## Troubleshooting

### Suggestions Too Frequent

Increase threshold or add suppression conditions:
```json
{
  "threshold": 75,
  "min_interval": 900
}
```

### Suggestions Never Appear

Check that:
1. Hook is enabled in `.claude/hooks.json`
2. Threshold is set appropriately
3. Skill is not permanently suppressed

### Context Not Being Saved

Ensure context-saver skill is available:
```bash
ls -la skills/context-saver/SKILL.md
```

### Boundaries Not Detected

Add custom boundary patterns for your workflow:
```json
{
  "custom_boundaries": {
    "my_workflow_step": {
      "trigger": "Bash",
      "pattern": "your-command-pattern"
    }
  }
}
```

---

## Summary

The strategic-compact skill transforms context compaction from an arbitrary interruption into a thoughtful workflow optimization. By monitoring session state, recognizing logical boundaries, and integrating with context preservation tools, it ensures that compaction happens at optimal moments without disrupting active work.

Key principles:
1. **Suggest, don't force** - Respect user workflow
2. **Boundary-aware** - Align with natural pause points
3. **Context-preserving** - Integrate with context-saver
4. **Configurable** - Adapt to different projects and preferences
5. **Non-intrusive** - Clear but minimal suggestions

Use this skill to maintain high-quality context throughout long sessions while avoiding the disruption of poorly-timed compaction.
