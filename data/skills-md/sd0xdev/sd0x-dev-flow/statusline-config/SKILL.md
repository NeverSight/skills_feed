---
name: statusline-config
description: "Customize Claude Code statusline. Use when: user says 'statusline', 'status line', 'customize statusline', 'modify statusline', 'statusline settings', 'statusline theme', 'change theme', 'color scheme', wants to add/remove/change segments (cost, git, model, context), switch color themes (catppuccin, dracula, nord), or asks what can be shown in the statusline."
---

# StatusLine Config

Customize `~/.claude/statusline-command.sh` — segments, themes, and colors.

## When NOT to Use

| Scenario | Use Instead |
|----------|-------------|
| Setting statusline for the first time (no customization needed) | Built-in `statusline-setup` agent (Claude Code agent type) — applies defaults automatically |
| Editing `settings.json` directly | Manual edit — this skill manages `statusline-command.sh`, not `settings.json` |
| Debugging Claude Code startup issues | `/claude-health` — config health check |

## Segments

| Segment     | JSON Field                            | Default | Notes                                 |
| ----------- | ------------------------------------- | ------- | ------------------------------------- |
| Directory   | `workspace.current_dir`               | ON      | Truncate deep paths: `~/.../last-dir` |
| Git branch  | shell `git`                           | ON      | `--no-optional-locks`, cache 5s       |
| Model       | `model.display_name`                  | ON      | -                                     |
| Context %   | `context_window.remaining_percentage` | ON      | Green >40%, Yellow 20-40%, Red <=20%  |
| Cost        | `cost.total_cost_usd`                 | ON      | Show when >= $0.005, `est $X.XX`      |
| >200k alert | `exceeds_200k_tokens`                 | ON      | Show only when `true`                 |

For full JSON schema, see [json-schema.md](references/json-schema.md).

## Themes

| Theme              | Type      | Default | Notes                                 |
| ------------------ | --------- | ------- | ------------------------------------- |
| `ansi-default`     | ANSI 16   | ✅      | Safe fallback, works everywhere       |
| `catppuccin-mocha` | TrueColor | —       | Recommended — pastel, WCAG AA >=4.5:1 |
| `dracula`          | TrueColor | —       | Vibrant purple/pink accents           |
| `nord`             | TrueColor | —       | Arctic blue, muted tones              |
| `none`             | —         | —       | No colors (`NO_COLOR` auto-triggers)  |

Switch via: `export CLAUDE_STATUSLINE_THEME=catppuccin-mocha`

For complete token→hex mappings, see [themes.md](references/themes.md).

## Semantic Tokens

Scripts use semantic tokens instead of hardcoded colors:

| Token        | Role                 | Example             |
| ------------ | -------------------- | ------------------- |
| `C_CWD`      | Directory path       | blue / sapphire     |
| `C_BRANCH`   | Git branch name      | magenta / mauve     |
| `C_MODEL`    | Model display name   | cyan / teal         |
| `C_CTX_OK`   | Context >= 41%       | green               |
| `C_CTX_WARN` | Context 21-40%       | yellow              |
| `C_CTX_BAD`  | Context <= 20%       | red                 |
| `C_COST`     | Cost display         | muted text          |
| `C_ALERT`    | >200k token warning  | orange/peach + bold |
| `C_SEP`      | Pipe separator `\|`  | dim/overlay         |
| `C_MUTED`    | Secondary info       | subtext             |
| `C_TEXT`     | General text         | foreground          |
| `C_RESET`    | Reset all formatting | `\033[0m`           |

## Workflow

**No args** → Apply best-practice defaults (all ON segments + `ansi-default` theme). Go to step 4.

**Theme change** (e.g. "use catppuccin-mocha", "switch to dracula") → Read [themes.md](references/themes.md), apply requested theme. Go to step 4. Aliases: `catppuccin` → `catppuccin-mocha`.

**Custom requests** (e.g. "add cost", "remove git", "no colors") → Interactive flow:

1. Read current script: `cat ~/.claude/statusline-command.sh`
2. Ask segments to enable/disable (AskUserQuestion multiSelect)
3. Ask theme preference (AskUserQuestion with theme options)
4. Generate script following Script Rules + selected theme from [themes.md](references/themes.md)
5. Write to `~/.claude/statusline-command.sh`
6. Verify: `echo '{"model":{"display_name":"Opus 4.6"},"workspace":{"current_dir":"/tmp/test"},"context_window":{"remaining_percentage":55},"cost":{"total_cost_usd":0.42},"exceeds_200k_tokens":false}' | ~/.claude/statusline-command.sh`

## Script Rules

- Shebang: `#!/bin/sh` (POSIX)
- Read stdin: `input=$(cat)`
- Parse JSON: `jq -r '.field // fallback'`
- Theme from env: `theme="${CLAUDE_STATUSLINE_THEME:-ansi-default}"`
- NO_COLOR: `[ -n "${NO_COLOR:-}" ] && theme="none"`
- Theme aliases: `catppuccin` → `catppuccin-mocha`
- Invalid theme: fallback to `ansi-default`
- Color output: `printf "%b"` for ANSI/TrueColor, `printf "%s"` for none
- TrueColor format: `\033[38;2;R;G;Bm` (24-bit foreground)
- Git: `git --no-optional-locks -C "$dir"`
- Git cache: `/tmp/claude-statusline-git-cache-$(id -u)`, 5s TTL, `stat -f %m` (macOS) / `stat -c %Y` (Linux)
- CWD truncation: depth >2 → `~/.../basename`
- Cost: only when `>= 0.005`, format `est $X.XX`
- Alert style: `C_ALERT` + bold (`\033[1m`) to distinguish from `C_CTX_BAD`

## Script Structure

```sh
#!/bin/sh
input=$(cat)
# ... extract JSON fields ...

theme="${CLAUDE_STATUSLINE_THEME:-ansi-default}"
[ -n "${NO_COLOR:-}" ] && theme="none"

case "$theme" in
  catppuccin|catppuccin-mocha) # set C_* tokens with TrueColor values ;;
  dracula)          # ... ;;
  nord)             # ... ;;
  none)             # all C_* = "" ;;
  *)                # ansi-default: ANSI 16 colors ;;
esac

# ... build output using C_* tokens ...
if [ "$theme" = "none" ]; then
  printf "%s" "$out"
else
  printf "%b" "$out"
fi
```

## Example Output

```
~/.../my-project | feat/auth | Opus 4.6 | ctx 48% left · est $0.12
~/.../my-project | main | Opus 4.6 | ctx 18% left · est $1.23 · >200k
```

## Output

| Artifact | Path | Description |
|----------|------|-------------|
| StatusLine script | `~/.claude/statusline-command.sh` | POSIX shell script consuming JSON stdin |

## Verification

After generating the script, verify:

- [ ] `~/.claude/statusline-command.sh` exists and is executable (`chmod +x`)
- [ ] Test echo passes: `echo '{"model":{"display_name":"Opus 4.6"},"workspace":{"current_dir":"/tmp/test"},"context_window":{"remaining_percentage":55},"cost":{"total_cost_usd":0.42},"exceeds_200k_tokens":false}' | ~/.claude/statusline-command.sh`
- [ ] Output contains expected segments (directory, model, context %)
- [ ] Theme matches user selection (check color codes in script)
- [ ] `NO_COLOR=1` produces uncolored output
