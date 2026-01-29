---
name: collaborating-with-gemini
description: Delegates coding tasks to Gemini CLI for prototyping, debugging, and code review. Use when needing algorithm implementation, bug analysis, or code quality feedback. Supports multi-turn sessions via SESSION_ID.
---

## Quick Start

```bash
python scripts/gemini_bridge.py --cd "/path/to/project" --PROMPT "Your task"
```

**Output:** JSON with `success`, `SESSION_ID`, `agent_messages`, and optional `error`.

## Parameters

```
usage: gemini_bridge.py [-h] --PROMPT PROMPT --cd CD [--sandbox] [--SESSION_ID SESSION_ID] [--return-all-messages] [--model MODEL]

Gemini Bridge

options:
  -h, --help            show this help message and exit
  --PROMPT PROMPT       Instruction for the task to send to gemini.
  --cd CD               Set the workspace root for gemini before executing the task.
  --sandbox             Run in sandbox mode. Defaults to `False`.
  --SESSION_ID SESSION_ID
                        Resume the specified session of the gemini. Defaults to empty string, start a new session.
  --return-all-messages
                        Return all messages (e.g. reasoning, tool calls, etc.) from the gemini session. Set to `False` by default, only the agent's final reply message is
                        returned.
  --model MODEL         The model to use for the gemini session. This parameter is strictly prohibited unless explicitly specified by the user.
```

## Multi-turn Sessions

**Always capture `SESSION_ID`** from the first response for follow-up:

```bash
# Initial task
python scripts/gemini_bridge.py --cd "/project" --PROMPT "Analyze auth in login.py"

# Continue with SESSION_ID
python scripts/gemini_bridge.py --cd "/project" --SESSION_ID "uuid-from-response" --PROMPT "Write unit tests for that"
```

## Common Patterns

**Prototyping (request diffs):**
```bash
python scripts/gemini_bridge.py --cd "/project" --PROMPT "Generate unified diff to add logging"
```

**Debug with full trace:**
```bash
python scripts/gemini_bridge.py --cd "/project" --PROMPT "Debug this error" --return-all-messages
```
