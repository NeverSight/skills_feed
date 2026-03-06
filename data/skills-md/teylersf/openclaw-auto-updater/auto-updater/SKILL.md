---
name: auto-updater
description: |
  Automatically update OpenClaw every night. Use when the user wants their agent to stay up-to-date 
  with the latest OpenClaw version. Runs a cron job that stops the gateway, runs the update, and restarts.
  Triggered when user mentions: "update yourself", "auto update", "nightly update", "keep updated", 
  "self update", or any variation of updating the agent.
---

# Auto-Updater Skill

This skill keeps OpenClaw updated by running a nightly cron job that executes an external shell script — so the update works even when the gateway restarts.

## Quick Setup

To enable auto-updates, say "set up auto-updater" and I'll:
1. Copy the update script to your home folder
2. Create a cron job that runs the script at 4 AM daily

## Why a Script?

The agent can't run commands while the gateway is restarting. We use a standalone shell script that runs independently of the agent.

## The Update Script

```bash
#!/bin/bash
# OpenClaw Auto-Updater

openclaw gateway stop
openclaw update.run
openclaw gateway start
```

## Change Update Time

Tell me "change update time to [time]" and I'll update the cron schedule.

## Manual Update

Say "update yourself now" and I'll run the script immediately.

## Troubleshooting

Check the log file: `~/openclaw-update.log`
