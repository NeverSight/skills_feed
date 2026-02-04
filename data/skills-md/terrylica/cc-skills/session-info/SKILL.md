---
name: session-info
description: Get current Claude Code session UUID and registry info. TRIGGERS - current session, session uuid, session id, what session, which session.
---

# Session Info Skill

Returns the current Claude Code session UUID and registry information.

## When to Use This Skill

Use this skill when:

- Need to know the current session UUID for debugging
- Want to check the session chain history
- Verify the session registry is working
- Find correlation between sessions and transcripts

## Implementation

Run the session info script:

```bash
bun $HOME/.claude/plugins/marketplaces/cc-skills/plugins/statusline-tools/scripts/get-session-info.ts
```

## Output Format

The script outputs structured session information:

```
Current Session: c1c1c149-1abe-45f3-8572-fd77aa046232
Short ID: c1c1c149
Project: ~/.claude
Registry: ~/.claude/projects/-Users-terryli--claude/.session-chain-cache.json
Chain Length: 3 session(s)
Last Updated: 2026-01-15T21:30:00.000Z
Managed By: session-registry-plugin@1.0.0

Metadata:
  Repo: cc-skills
  Hash: a1b2c3d4e5f6
  Branch: main
  Model: opus-4
  Cost: $0.42

Recent Sessions (last 5):
  1. 8e017a43 (2026-01-15T10:00:00.000Z)
  2. a2b3c4d5 (2026-01-15T14:00:00.000Z)
  3. c1c1c149 (2026-01-15T21:30:00.000Z)
```

## Registry Location

The session registry follows Claude Code's native path encoding:

```
~/.claude/projects/{encoded-path}/.session-chain-cache.json
```

Where `encoded-path` replaces `/` with `-`:

- `/Users/terryli/eon/cc-skills` → `-Users-terryli-eon-cc-skills`

## References

- [Registry Format](./references/registry-format.md) - Schema documentation

---

## Troubleshooting

| Issue                     | Cause                      | Solution                                         |
| ------------------------- | -------------------------- | ------------------------------------------------ |
| Script not found          | Plugin not installed       | Run `claude plugin list` to verify installation  |
| Session UUID undefined    | No active session          | Start Claude Code session first                  |
| Registry file not found   | First session in project   | Registry created automatically on first session  |
| Chain length is 0         | Fresh project              | Normal for new projects, chain grows over time   |
| Metadata missing          | Older session format       | Recent sessions include metadata automatically   |
| Path encoding looks wrong | Special characters in path | Claude Code uses `-` to replace `/` in paths     |
| Bun not found             | Bun not installed          | Install with `brew install oven-sh/bun/bun`      |
| Permission denied         | Registry file permissions  | Check ~/.claude permissions (should be readable) |
