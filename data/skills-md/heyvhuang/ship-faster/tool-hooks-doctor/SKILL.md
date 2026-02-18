---
name: tool-hooks-doctor
description: "Detect whether Claude Code evolution hooks are installed/enabled, and print a copy-paste fix. Use when you expect runs/evolution artifacts but nothing is being written. Triggers: hooks, evolution, runs/evolution, settings.json, PreToolUse, PostToolUse."
allowed-tools:
  - Read
  - Bash
  - Grep
---

# Hooks Doctor (Claude Code)

Goal: quickly verify whether **Claude Code hooks** for `skill-evolution` are installed and enabled.

This is an atomic diagnostic tool used by other workflows so they can warn early when the evolution loop is not active.

## Scope

- Applies to: Claude Code hook installation / configuration
- Does not apply to: Cursor/OpenCode/etc that do not support Claude-style hooks

## What "healthy" looks like

1) Hook scripts exist at:
- `~/.claude/skills/skill-evolution/hooks/`

2) Settings enable the hooks in either:
- Project settings: `<repo_root>/.claude/settings.json`
- Or global settings: `~/.claude/settings.json`

3) A session produces artifacts under:
- `<project_root>/runs/evolution/<run_id>/...`

## Check (read-only)

Run these checks and report status as: OK / PARTIAL / MISSING.

### 1) Are the hook scripts installed?

```bash
ls -la ~/.claude/skills/skill-evolution/hooks/ 2>/dev/null || true
```

Required files:
- `pre-tool.sh`
- `post-bash.sh`
- `post-tool.sh`
- `session-end.sh`

If missing: user must install/update the `skill-evolution` skill first.

### 2) Are hooks enabled in settings?

Check both locations:

```bash
test -f .claude/settings.json && echo "project settings: .claude/settings.json" || true
test -f ~/.claude/settings.json && echo "global settings: ~/.claude/settings.json" || true

grep -n "skill-evolution/hooks/pre-tool.sh" .claude/settings.json ~/.claude/settings.json 2>/dev/null || true
grep -n "skill-evolution/hooks/post-bash.sh" .claude/settings.json ~/.claude/settings.json 2>/dev/null || true
grep -n "skill-evolution/hooks/post-tool.sh" .claude/settings.json ~/.claude/settings.json 2>/dev/null || true
grep -n "skill-evolution/hooks/session-end.sh" .claude/settings.json ~/.claude/settings.json 2>/dev/null || true
```

Interpretation:
- If none of the grep checks match: hooks are not enabled.
- If only some match: configuration is PARTIAL and should be fixed.

### 3) Quick runtime smoke test (optional)

If user confirms, run a harmless bash command in the project and then check:

```bash
ls -la runs/evolution 2>/dev/null || true
```

## Fix (write; require confirmation)

If hooks are not enabled, recommend installing **project-level hooks** (safer than global).

Before applying, tell the user exactly which file will be written:
- Project-level: `<repo_root>/.claude/settings.json` (recommended)
- Global: `~/.claude/settings.json`

Then wait for explicit confirmation.

### Install project-level hooks (recommended)

```bash
python3 - <<'PY'
import json
from pathlib import Path

settings = Path('.claude') / 'settings.json'
settings.parent.mkdir(parents=True, exist_ok=True)

data = {}
if settings.exists():
    data = json.loads(settings.read_text() or '{}')
if not isinstance(data, dict):
    data = {}

hooks = data.get('hooks')
if not isinstance(hooks, dict):
    hooks = {}

desired = {
  'PreToolUse': [{
    'matcher': 'Bash|Write|Edit',
    'hooks': [{'type':'command','command':'bash ~/.claude/skills/skill-evolution/hooks/pre-tool.sh'}]
  }],
  'PostToolUse': [
    {
      'matcher': 'Bash',
      'hooks': [{'type':'command','command':'bash ~/.claude/skills/skill-evolution/hooks/post-bash.sh "$TOOL_OUTPUT" "$EXIT_CODE"'}]
    },
    {
      'matcher': 'Write|Edit',
      'hooks': [{'type':'command','command':'bash ~/.claude/skills/skill-evolution/hooks/post-tool.sh "$TOOL_OUTPUT" "$EXIT_CODE"'}]
    }
  ],
  'Stop': [{
    'matcher': '',
    'hooks': [{'type':'command','command':'bash ~/.claude/skills/skill-evolution/hooks/session-end.sh'}]
  }]
}

def has_command(arr, matcher, command):
    for item in arr:
        if not isinstance(item, dict):
            continue
        if item.get('matcher') != matcher:
            continue
        hs = item.get('hooks')
        if not isinstance(hs, list):
            continue
        for h in hs:
            if isinstance(h, dict) and h.get('command') == command:
                return True
    return False

for event, items in desired.items():
    arr = hooks.get(event)
    if not isinstance(arr, list):
        arr = []
    for it in items:
        cmd = it['hooks'][0]['command']
        if not has_command(arr, it['matcher'], cmd):
            arr.append(it)
    hooks[event] = arr

data['hooks'] = hooks

if settings.exists():
    backup = settings.with_suffix(settings.suffix + '.bak')
    backup.write_text(settings.read_text())

settings.write_text(json.dumps(data, indent=2, ensure_ascii=True) + '\n')
print('Installed hooks into:', settings)
PY
```

### Install global hooks (optional)

Same as above, but write to `~/.claude/settings.json`.
