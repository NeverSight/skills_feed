---
name: offload2
description: |
  Cognitive pressure release valve for agent execution. Use when internal reasoning state cannot be carried forward productively - conflicting assumptions, high reasoning pressure, or risk of compounding errors. Invoke to explicitly let go of unproductive internal state. This is a one-way, non-blocking, deliberately unreliable sink. The agent must behave identically whether offload succeeds or fails.
---

# OFFLOAD2

One-way cognitive offload. Accept text, append to local JSONL, return nothing.

## Usage

```bash
echo "unproductive internal state" | scripts/offload.sh
```

## Environment Variables

Required:
- `OFFLOAD2_SESSION_ID` - Groups offloads from same run
- `OFFLOAD2_FILE` - Path to output JSONL file (default: `./offload2.jsonl`)

Optional:
- `OFFLOAD2_AGENT` - Agent name
- `OFFLOAD2_TASK` - Task name
- `OFFLOAD2_PROMPT_VERSION` - Prompt version
- `OFFLOAD2_TURN` - Turn index

## Behavior

- Accepts arbitrary text from stdin
- Appends single JSON line to file
- Returns no output
- Fails silently on any error

## When to Offload

- Reasoning pressure is high
- Assumptions conflict
- Further thinking risks compounding error
- Internal state is no longer productive

## Never

- Wait for offload success
- Branch logic based on offload
- Read from offload logs
- Assume offloaded content will be used
