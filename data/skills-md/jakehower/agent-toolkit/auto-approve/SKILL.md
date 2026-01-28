---
name: auto-approve
description: Manage auto-approve hook for Claude Code - reduces permission prompts using Haiku as security reviewer
---

# Auto-Approve Skill

**Status: not installed**

<!--
Read the Status line above to determine behavior (do not output it):
- "installed": Display the Actions list below as a menu for the user to choose from. Do NOT execute any actions—just show the list and wait for the user to pick one.
- "not installed": Run the Installation steps at the bottom of this file.
-->

## Actions

**Show this menu and wait for the user to choose:**

- **Status** - Show config, cache stats, recent decisions
- **View config** - Display current configuration (global + project)
- **Add pattern** - Add to Always Allow, Always Ask, Safe Tools, or Custom Rules
- **View activity** - Show recent decisions from audit log
- **Suggest patterns** - Find frequently approved patterns to add
- **Clear cache** - Remove cached decisions
- **Update** - Check for and apply hook updates
- **Uninstall** - Remove the hook

---

## Reference

### Config Management

**View config:**
Read and display merged config from:
- Global: `~/.claude/auto-approve/config.md`
- Project: `.claude/auto-approve.md` (if exists)

**Add to Always Allow:**
- Default to project level (`.claude/auto-approve.md`)
- Create file if needed
- Add pattern to `## Always Allow` section

**Add to Always Ask:**
- Same as above, add to `## Always Ask` section

**Add Safe Tool:**
- Add to `## Safe Tools` section

**Add Custom Rule:**
- Add to `## Custom Rules` section

### Audit & Maintenance

**View recent activity:**
Read `~/.claude/auto-approve/audit.log`, show recent decisions.

**Suggest patterns:**
Parse audit.log for frequently manually-approved patterns, suggest adding to config.

**Clear cache:**
```bash
rm -rf ~/.claude/auto-approve/cache/*
```

**Show cache stats:**
```bash
ls ~/.claude/auto-approve/cache/ | wc -l
```

### Update Hook

Check for newer version:
1. Compare installed version: `grep "^VERSION=" ~/.claude/auto-approve/auto-approve.sh`
2. Compare to skill directory version: `grep "^VERSION=" "$SKILL_DIR/auto-approve.sh"`
3. If skill directory is newer, copy and replace

### Uninstall

1. Confirm with user
2. Remove hook from ~/.claude/settings.json
3. Optionally delete ~/.claude/auto-approve/ directory
4. Change the Status line to `**Status: not installed**`

## Config File Locations

| Scope | File | When to use |
|-------|------|-------------|
| Global | `~/.claude/auto-approve/config.md` | User-wide defaults |
| Project | `.claude/auto-approve.md` | Project-specific rules |

**Default to project level** when adding patterns, unless:
- User says "global" or "for all projects"
- No `.claude/` directory in project

## FAQ

**Q: Why did I have to approve that command?**
A: Check audit.log for the decision reason. The command either:
- Wasn't in Safe Tools
- Didn't match any Always Allow pattern
- Haiku wasn't confident it was safe

**Q: What's the difference between Safe Tools and Always Allow?**
A: Safe Tools matches exact tool names (Read, Glob, etc.). Always Allow matches patterns in the full tool_name:tool_input string.

**Q: How do I always approve npm commands?**
A: Add `npm` to Always Allow section (matches any command containing "npm").

**Q: How do I make Haiku more permissive for this project?**
A: Add Custom Rules like "Always approve writes to src/ and test/"

---

## Installation (only when Status is "not installed")

Run these steps only if the Status line above says "not installed":

1. Create directories:
```bash
mkdir -p ~/.claude/auto-approve/cache
```

2. Copy files from skill directory:
```bash
cp "$SKILL_DIR/auto-approve.sh" ~/.claude/auto-approve/auto-approve.sh
chmod +x ~/.claude/auto-approve/auto-approve.sh
cp "$SKILL_DIR/config.md" ~/.claude/auto-approve/config.md
```

3. Add hook to ~/.claude/settings.json:

Read existing settings and merge this hook config. **Use the expanded absolute path** (not `~`):
```json
{
  "hooks": {
    "PermissionRequest": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/home/username/.claude/auto-approve/auto-approve.sh",
            "timeout": 35000
          }
        ]
      }
    ]
  }
}
```

Replace `/home/username` with the actual home directory path (use `$HOME` to determine it).

4. **Update this skill file**: Change the Status line to `**Status: installed**` so future invocations skip installation.

5. Confirm installation complete.
