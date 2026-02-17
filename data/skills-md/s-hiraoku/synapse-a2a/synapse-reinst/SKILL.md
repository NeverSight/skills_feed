---
name: synapse-reinst
description: >-
  Re-inject Synapse A2A initial instructions after context has been cleared.
  Use this skill when the agent has lost its identity, A2A communication
  protocol, or configuration after /clear or context reset. Triggered by
  /synapse-reinst command.
---

# Synapse Re-Instruction

Restore Synapse A2A agent identity and instructions after `/clear` or context reset.

## When to Use

- After running `/clear` (or equivalent context reset)
- When the agent no longer recognizes Synapse commands
- When A2A communication has stopped working
- After any event that clears the agent's initial instructions

## Usage

Run the reinst script to output your full Synapse instructions:

```bash
python plugins/synapse-a2a/skills/synapse-reinst/scripts/reinst.py
```

The script reads environment variables set by Synapse at startup (`SYNAPSE_AGENT_ID`, `SYNAPSE_AGENT_TYPE`, `SYNAPSE_PORT`) which persist even after `/clear`.

## Instructions

1. Run the script above
2. Read the output carefully — it contains your full Synapse A2A configuration
3. Follow the instructions as if they were just sent to you
4. Resume normal operation with A2A communication enabled

## How It Works

The script:
1. Reads Synapse environment variables (set at agent startup, survives `/clear`)
2. Looks up your name/role from the agent registry
3. Loads your instruction template from `.synapse/settings.json`
4. Outputs the complete instruction with all placeholders replaced
