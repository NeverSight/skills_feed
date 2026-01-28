---
name: monta-lights
description: Control Meross smart plugs (lights). Use when the user says "turn on the lights", "turn off the lights", "lights on", "lights off", or asks about light/plug status.
---

# Monta Lights

Control Meross smart plugs via CLI.

## Prerequisites

- Environment variables: `MEROSS_EMAIL`, `MEROSS_PASSWORD`
- Python package: `pip install meross_iot`

## Commands

### Turn all lights ON

```bash
python3 scripts/meross_cli.py on
```

### Turn all lights OFF

```bash
python3 scripts/meross_cli.py off
```

### Check status

```bash
python3 scripts/meross_cli.py list
```

Run scripts from the skill directory: `~/.claude/skills/monta-lights/`

## Response

Confirm briefly: "Lights are now on" or "Lights are now off".
