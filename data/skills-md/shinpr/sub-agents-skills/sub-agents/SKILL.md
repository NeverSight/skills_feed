---
name: sub-agents
description: Execute external CLI AIs as isolated sub-agents for task delegation, parallel processing, and context separation. Use when delegating complex multi-step tasks, running parallel investigations, needing fresh context without current conversation history, or leveraging specialized agent definitions. Returns structured JSON with agent output, exit code, and execution status.
allowed-tools: Bash Read
---

# Sub-Agents - External CLI AI Task Delegation

Spawns external CLI AIs (claude, cursor-agent, codex, gemini) as isolated sub-agents with dedicated context.

## Resources

- **[run_subagent.py](scripts/run_subagent.py)** - Main execution script
- **[codex.md](references/codex.md)** - Codex-specific setup (permissions, timeout)

**Script Path**: Use absolute path `{SKILL_DIR}/scripts/run_subagent.py` where `{SKILL_DIR}` is the directory containing this SKILL.md file.

## CLI-Specific Notes

Check the corresponding reference for your environment:
- **Codex**: Read [references/codex.md](references/codex.md) BEFORE first execution

## Interpreting User Requests

Extract parameters from user's natural language request:

| Parameter | Source |
|-----------|--------|
| --agent | Agent name from user request (see selection rules below) |
| --prompt | Task instruction part (excluding agent specification) |
| --cwd | Current working directory (absolute path) |

**Agent Selection Rules** (when user doesn't specify agent name):
1. Run `--list` to get available agents
2. **0 agents**: Inform user no agents available, show setup instructions (see [Agent Definition Format](#agent-definition-format))
3. **1 agent**: Auto-select without asking
4. **2+ agents**: Show list with descriptions, ask user to choose

**Example**:
"Run code-reviewer on src/"
→ `--agent code-reviewer --prompt "Review src/" --cwd $(pwd)`

## When to Use This Skill

**Use sub-agent when ANY of these apply:**
- Complex multi-step task (isolated context prevents interference)
- Parallel investigation (multiple agents can run simultaneously)
- Task needs fresh context (sub-agent starts without conversation history)
- Specialized agent definition exists (leverage pre-defined expert prompts)

## Important: Permission and Timeout

This script executes external CLIs that require elevated permissions.

**Before first execution:**
1. Request elevated permissions via your CLI's tool parameters
2. Set tool timeout to match `--timeout` argument (default: 600000ms)

**For Codex CLI** (most common permission issues): See [references/codex.md](references/codex.md) for exact JSON parameter format.

## Workflow

### Step 0: Read CLI-Specific Setup (if applicable)

If you are running on Codex, read [references/codex.md](references/codex.md) first.

### Step 1: List Available Agents

**Always list agents first** to discover available definitions:

```bash
scripts/run_subagent.py --list
```

Output:
```json
{"agents": [{"name": "code-reviewer", "description": "Reviews code..."}], "agents_dir": "/path/.agents"}
```

**If agents list is empty**:
1. Create `{cwd}/.agents/` directory
2. Add agent definition file (see [Agent Definition Format](#agent-definition-format))
3. Re-run `--list` to verify

### Step 2: Execute Agent

```bash
scripts/run_subagent.py \
  --agent <name> \
  --prompt "<task>" \
  --cwd <absolute-path>
```

### Step 3: Handle Response

Parse JSON output and check `status` field:

```json
{"result": "...", "exit_code": 0, "status": "success", "cli": "claude"}
```

**By status:**

| status | Meaning | Action |
|--------|---------|--------|
| `success` | Task completed | Use `result` directly |
| `partial` | Timeout but has output | Review partial `result`, may need retry |
| `error` | Execution failed | Check `error` field and `exit_code`, fix and retry |

**By exit_code** (when status is `error`):

| exit_code | Meaning | Resolution |
|-----------|---------|------------|
| 0 | Success | - |
| 124 | Timeout | Increase `--timeout` or simplify task |
| 127 | CLI not found | Install required CLI (claude, codex, etc.) |
| 1 | General error | Check `error` field in response |

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--list` | - | List available agents (no other params needed) |
| `--agent` | Yes* | Agent definition name from --list |
| `--prompt` | Yes* | Task description to delegate |
| `--cwd` | Yes* | Working directory (absolute path) |
| `--timeout` | No | Timeout ms (default: 600000) |
| `--cli` | No | Force CLI: `claude`, `cursor-agent`, `codex`, `gemini` |

*Required when not using --list

## Agent Definition Location

| Priority | Source | Path |
|----------|--------|------|
| 1 | Environment variable | `$SUB_AGENTS_DIR` |
| 2 | Default | `{cwd}/.agents/` |

To customize: `export SUB_AGENTS_DIR=/custom/path`

## Agent Definition Format

Place `.md` files in `.agents/` directory:

```markdown
---
run-agent: claude
---

# Agent Name

Brief description of agent's purpose.

## Task
What this agent does.

## Output Format
How results should be structured.
```

**Critical**: The `run-agent` frontmatter determines which CLI executes the agent. See [cli-formats.md](references/cli-formats.md) for CLI-specific behaviors.

## CLI Selection Priority

1. `--cli` argument (explicit override)
2. Agent definition `run-agent` frontmatter
3. Auto-detect caller environment
4. Default: `codex`

## Common Mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| Skip `--list` before execution | Agent not found error | Always run `--list` first |
| Use relative path for `--cwd` | Validation fails | Use absolute path |
| Ignore `status` field in response | Undetected errors | Always check `status` before using `result` |
| Very long prompts | May exceed CLI limits | Break into smaller tasks |
