---
name: delegation
description: This skill configures automatic task delegation between agents in Synapse A2A. Configure delegation rules via settings files (.synapse/settings.json and .synapse/delegate.md) or the interactive config TUI (synapse config). Supports orchestrator mode (Claude coordinates) and passthrough mode (direct forwarding). Includes agent status verification, priority levels, error handling, and File Safety integration.
---

# Delegation Skill

Configure automatic task delegation to other agents based on natural language rules.

## Configuration

Delegation is configured via settings files, managed using:
- `synapse init` - Create .synapse/ with template files
- `synapse config` - Interactive TUI for editing settings
- Direct file editing

### Configuration Files

| File | Purpose |
|------|---------|
| `.synapse/settings.json` | Enable/disable delegation and set A2A flow mode |
| `.synapse/delegate.md` | Define delegation rules and agent responsibilities |

### Settings Structure

In `.synapse/settings.json`:

```json
{
  "a2a": {
    "flow": "auto"  // "roundtrip" | "oneway" | "auto"
  },
  "delegation": {
    "enabled": true  // Enable automatic task delegation
  }
}
```

### Delegate Rules Structure

The `.synapse/delegate.md` file defines delegation rules in YAML frontmatter followed by optional markdown documentation.

#### Schema

```yaml
---
# Delegate rules configuration
version: 1  # Schema version (required)

# Agent definitions with their responsibilities
agents:
  codex:
    responsibilities:
      - "Code implementation and refactoring"
      - "File editing and creation"
      - "Bug fixes"
    default_priority: 3

  gemini:
    responsibilities:
      - "Research and web search"
      - "Documentation review"
      - "API exploration"
    default_priority: 3

  claude:
    responsibilities:
      - "Code review and analysis"
      - "Architecture planning"
      - "Complex problem solving"
    default_priority: 3

# Delegation rules (evaluated in order, first match wins)
rules:
  - name: "coding-tasks"
    description: "Route coding tasks to Codex"
    match:
      keywords: ["implement", "refactor", "fix", "edit", "create file"]
      file_patterns: ["*.py", "*.ts", "*.js"]
    target: codex
    priority: 3
    flow: roundtrip  # Wait for response

  - name: "research-tasks"
    description: "Route research to Gemini"
    match:
      keywords: ["research", "search", "find", "look up", "documentation"]
    target: gemini
    priority: 2
    flow: oneway  # Fire and forget

  - name: "review-tasks"
    description: "Route reviews to Claude"
    match:
      keywords: ["review", "analyze", "evaluate", "assess"]
    target: claude
    priority: 3
    flow: roundtrip

# Fallback behavior when no rules match
fallback:
  action: manual  # "manual" | "ask" | "default_agent"
  default_agent: claude  # Used when action is "default_agent"
---

# Delegation Rules Documentation

Additional markdown content here for human-readable documentation...
```

#### Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `version` | integer | Yes | Schema version (currently `1`) |
| `agents` | object | Yes | Agent definitions keyed by agent name |
| `agents.<name>.responsibilities` | string[] | No | List of task types this agent handles |
| `agents.<name>.default_priority` | integer | No | Default priority (1-5) for this agent |
| `rules` | array | No | Ordered list of delegation rules |
| `rules[].name` | string | Yes | Unique rule identifier |
| `rules[].description` | string | No | Human-readable description |
| `rules[].match` | object | Yes | Conditions for rule matching |
| `rules[].match.keywords` | string[] | No | Keywords to match in task text |
| `rules[].match.file_patterns` | string[] | No | Glob patterns for file-related tasks |
| `rules[].target` | string | Yes | Target agent name |
| `rules[].priority` | integer | No | Task priority (1-5, default: 3) |
| `rules[].flow` | string | No | `"roundtrip"` \| `"oneway"` \| `"auto"` |
| `fallback` | object | No | Behavior when no rules match |
| `fallback.action` | string | No | `"manual"` \| `"ask"` \| `"default_agent"` |
| `fallback.default_agent` | string | No | Agent to use for `"default_agent"` action |

#### Rule Evaluation

Rules are evaluated in order from top to bottom. The first matching rule is applied:

1. **Keyword matching**: Case-insensitive substring match against task text
2. **File pattern matching**: Glob patterns matched against mentioned file paths
3. **Combined conditions**: All specified conditions must match (AND logic)

If no rules match, the `fallback` behavior is applied.

## Delegating Tasks

Use the `@agent` pattern to send tasks to other agents:

```text
@codex Please refactor this function
@gemini Research the latest API changes
@claude Review this design document
```

For programmatic delegation (from AI agents):

```bash
# Fire and forget (default)
synapse send codex "Refactor this function" --from claude

# Wait for response (roundtrip)
synapse send gemini "Analyze this code" --response --from claude

# Urgent follow-up
synapse send gemini "Status update?" --priority 4 --from claude

# Reply to a --response request
synapse reply "Here is the analysis..." --from gemini
```

**Important:** When responding to a `--response` request, the receiver MUST use `synapse reply` to send the response.

## Modes

### Orchestrator Mode (Recommended)

Claude analyzes tasks, delegates to appropriate agent, waits for response, integrates results.

```text
User → Claude (analyze) → @codex/@gemini → Claude (integrate) → User
```

### Passthrough Mode

Direct forwarding without processing.

```text
User → Claude (route) → @codex/@gemini → User
```

### Manual Mode (Default)

No automatic delegation. User explicitly uses @agent patterns.

## Pre-Delegation Checklist

Before delegating any task:

1. **Verify agent is READY**: `synapse list` (Rich TUI with auto-refresh on changes)
2. **Check file locks**: `synapse file-safety locks` (for file edits)
3. **Verify branch**: `git branch --show-current` (for coding tasks)

**Agent Status:**

| Status | Meaning | Action |
|--------|---------|--------|
| READY | Idle, waiting for input | Safe to delegate |
| WAITING | Awaiting user input | Use terminal jump to respond |
| PROCESSING | Busy handling a task | Wait or use --priority 5 |
| DONE | Task completed | Will return to READY shortly |

**Note:** `synapse list` provides real-time agent monitoring with auto-refresh. Press 1-9/↑↓ to select agent, `Enter`/`j` to jump, `k` to kill, `/` to filter, ESC to clear, q to quit.

## Priority Levels

| Priority | Use Case |
|----------|----------|
| 1-2 | Low priority, background tasks |
| 3 | Normal tasks (default) |
| 4 | Urgent follow-ups |
| 5 | Critical/emergency tasks |

## Available Agents

| Agent | Strengths | Port Range |
|-------|-----------|------------|
| claude | Code review, analysis, planning | 8100-8109 |
| gemini | Research, web search, documentation | 8110-8119 |
| codex | Coding, file editing, refactoring | 8120-8129 |
| opencode | AI coding, file operations | 8130-8139 |
| copilot | Code suggestions, completions | 8140-8149 |

## References

For detailed documentation, read:

- `references/modes.md` - Delegation modes and workflows
- `references/file-safety.md` - File Safety integration
- `references/examples.md` - Example sessions and configurations
