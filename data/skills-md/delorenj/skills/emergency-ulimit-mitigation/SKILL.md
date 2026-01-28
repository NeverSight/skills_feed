---
name: emergency-ulimit-mitigation
description: Emergency steps to mitigate ulimit-related crashes by increasing file descriptor limits and restarting services.
---

qqu='qq "`cat ~/d/AI/Prompts/Commands/fix-ulimit-exceeded.md`"'# Emergency `ulimit` Mitigation

**Tags:** AI/Prompt, ulimit, filedescriptors, crashing, toomanyfilesopen, Stability, Maintenance  
**Modified:** 2025-10-27T08:55:02-04:00

## Immediate Emergency Fix

```bash
# Instant relief - run immediately when services are crashing
ulimit -n 65536
echo 2097152 | sudo tee /proc/sys/fs/file-max
```

## Emergency Service Recovery

```bash
# Restart crashed services
sudo systemctl restart docker traefik
sudo docker system prune -f
```

## Check Current Status

```bash
# See what's using FDs
lsof | wc -l
cat /proc/sys/fs/file-nr | awk '{printf "FDs: %d/%d (%.1f%%)\n", $1, $3, ($1/$3)*100}'
```

## Deploy Full Solution

```bash
sudo ./scripts/set-ulimits.sh
sudo systemctl enable --now fd-monitor.timer
```

## Emergency Cleanup

```bash
./scripts/fd-cleanup.sh
```
