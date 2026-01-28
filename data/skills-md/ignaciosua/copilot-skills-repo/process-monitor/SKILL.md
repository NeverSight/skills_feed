---
name: process-monitor
description: Shows system processes sorted by CPU or memory, load average, RAM usage and uptime. Use for performance monitoring.
---

# Process Monitor

Monitors system processes and displays performance statistics.

## Usage

```bash
python ~/.copilot/skills/process-monitor/process_monitor.py [options]
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--top N` | Show top N processes | 10 |
| `--sort` | Sort by: cpu, mem | cpu |
| `--stats-only` | Show only system stats, no processes | false |

## Output

JSON with:
- `processes`: List of top processes (pid, name, cpu%, mem%)
- `load_average`: System load (1, 5, 15 min)
- `memory`: RAM usage (total, used, available, percent)
- `uptime`: System uptime

## Examples

### Default (Top 10 by CPU)
```bash
python ~/.copilot/skills/process-monitor/process_monitor.py
```

### Top 5 by Memory
```bash
python ~/.copilot/skills/process-monitor/process_monitor.py --top 5 --sort mem
```

### System Stats Only
```bash
python ~/.copilot/skills/process-monitor/process_monitor.py --stats-only
```
