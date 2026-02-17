---
name: update
description: 'Reinstall all AgentOps skills globally from the latest source. Triggers: "update skills", "reinstall skills", "sync skills".'
metadata:
  tier: solo
  dependencies: []
---

# /update — Reinstall AgentOps Skills

> **Purpose:** One command to pull the latest skills from the repo and install them globally across all agents.

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

---

## Execution

### Step 1: Install

```bash
npx skills@latest add boshu2/agentops --all -g
```

Run this command. Wait for it to complete.

### Step 2: Verify

Confirm the output shows all skills installed with no failures.

If any skills failed to install, report which ones failed and suggest re-running or manual sync:
```bash
# Manual sync for a failed skill (replace <skill-name>):
yes | cp -r skills/<skill-name>/ ~/.claude/skills/<skill-name>/
```

### Step 3: Report

Tell the user:
1. How many skills installed successfully
2. Any failures and how to fix them
