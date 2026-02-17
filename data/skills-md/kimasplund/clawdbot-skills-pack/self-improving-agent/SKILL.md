---
name: self-improving-agent
description: Enables continuous self-improvement through learning from failures, user corrections, and capability gaps. Integrates with QAVR for learned memory ranking.
user-invocable: true
---

# Self-Improving Agent

Captures learnings, errors, and corrections to enable continuous improvement across sessions.

## Activation Triggers

This skill automatically activates when:

| Trigger | What Gets Logged | Location |
|---------|------------------|----------|
| **Command fails** | Error type, context, recovery suggestion | `logs/failures_detailed.jsonl` |
| **User corrects** | "No, that's wrong...", "Actually..." | `logs/corrections.jsonl` |
| **Missing capability** | "Can you X?" where X isn't available | `logs/missing_capabilities.jsonl` |
| **API/tool fails** | Failure pattern, suggested fix | `logs/failures_detailed.jsonl` |
| **Better approach found** | Optimization learned | `logs/learnings.jsonl` |

## How It Works

### 1. Automatic Logging (via hooks)
```
PostToolUse → enhanced-failure-logger.js → logs failures with context
UserMessage → correction-detector.js → detects "wrong/actually/try again"
Response → capability-tracker.js → detects unfulfilled requests
```

### 2. Learning Aggregation
All learnings flow to `logs/learnings.jsonl`:
```json
{
  "timestamp": "2026-01-26T12:00:00Z",
  "type": "user_correction|tool_failure|missing_capability",
  "category": "factual_error|command_failed|web_browsing",
  "description": "what was learned",
  "source": "which detector"
}
```

### 3. Session Start Review
On each session start, recent learnings are shown:
```
=== Learning Review ===
[Learnings] 47 total entries
[Recent]
  • [tool_failure] Bash failed: timeout - WebFetch to external API...
  • [user_correction] User corrected: "No, use the other file..."
[Corrections] 12 user corrections logged
[Capability Gaps] Top requested:
  • send emails (5x)
  • browse web (3x)
```

### 4. QAVR Integration
Successful learnings boost Q-values for related memories, improving future retrieval.

## Manual Commands

### Review Learnings
```bash
# Show all learnings
cat ~/.claude/logs/learnings.jsonl | tail -20

# Show corrections only
cat ~/.claude/logs/corrections.jsonl | jq -s 'group_by(.correction_type) | map({type: .[0].correction_type, count: length})'

# Show capability gaps report
node ~/.claude/scripts/hooks/capability-tracker.js --report
```

### Test Detection
```bash
# Test correction detector
node ~/.claude/scripts/hooks/correction-detector.js

# Test failure logger
node ~/.claude/scripts/hooks/enhanced-failure-logger.js

# Test capability tracker
node ~/.claude/scripts/hooks/capability-tracker.js
```

## Learning Categories

### Correction Types
- `factual_error` - Wrong information provided
- `retry_request` - User asked to try again
- `misunderstanding` - Misinterpreted the request
- `failed_solution` - Solution didn't work

### Failure Types
- `permission_error` - Access denied
- `not_found` - File/resource missing
- `timeout` - Operation timed out
- `network_error` - Connection issues
- `syntax_error` - Invalid syntax
- `api_error` - External API failed
- `command_failed` - Shell command failed
- `agent_failed` - Subagent failed

### Capability Categories
- `web_browsing` - Internet access requests
- `image_processing` - Image/photo handling
- `communication` - Email/messaging
- `database_access` - SQL/database queries
- `external_api` - Third-party services
- `memory_persistence` - Long-term memory

## Configuration

In `settings.json`, these hooks enable self-improvement:

```json
{
  "hooks": {
    "SessionStart": [...],  // Reviews learnings
    "PostToolUse": [
      {"matcher": "Bash", "hooks": [{"command": "enhanced-failure-logger.js"}]},
      {"matcher": "Task", "hooks": [{"command": "enhanced-failure-logger.js"}]}
    ]
  }
}
```

## Benefits

1. **Learn from mistakes** - Don't repeat the same errors
2. **Understand user preferences** - Track what corrections mean
3. **Identify skill gaps** - Know what features to build
4. **Improve over time** - QAVR ranking gets better with feedback
5. **Context persistence** - Learnings survive session restarts

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| **QAVR** | Successful learnings boost memory Q-values |
| **Memory Consolidation** | Periodic cleanup of old learnings |
| **Confidence Check** | Review learnings before major tasks |
| **IR-v2** | Use learnings to inform pattern selection |

## Files

```
~/.claude/
├── logs/
│   ├── learnings.jsonl           # All learnings
│   ├── corrections.jsonl         # User corrections
│   ├── failures_detailed.jsonl   # Enhanced failure logs
│   ├── missing_capabilities.jsonl # Capability requests
│   └── capability_gaps.json      # Aggregated gaps
└── scripts/hooks/
    ├── correction-detector.js
    ├── enhanced-failure-logger.js
    ├── capability-tracker.js
    └── session-start.js (reviews learnings)
```
