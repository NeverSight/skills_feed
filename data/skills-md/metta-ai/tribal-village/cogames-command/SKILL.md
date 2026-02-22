---
name: cogames-command
description: "Craft or adjust `cogames` commands for train/play/eval with missions, variants, and policies. Use when asked for a CoGames command."
---

# CoGames Command

## Workflow
- Gather goal (train/play/eval) and required inputs (mission, variants, policy/run id, cogs, repeats).
- Produce the full `uv run cogames <mode>` command.
- If asked to execute, run the command and summarize outcomes.
- Explain key flags briefly.
