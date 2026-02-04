---
name: hooks-development
description: Claude Code hooks development guide. TRIGGERS - create hook, PostToolUse, PreToolUse, Stop hook, hook lifecycle, decision block.
---

# Hooks Development

Guide for developing Claude Code hooks with proper output visibility patterns.

## When to Use This Skill

- Creating a new PostToolUse or PreToolUse hook
- Hook output is not visible to Claude (most common issue)
- User asks about `decision: block` pattern
- Debugging why hook messages don't appear
- User mentions "Claude Code hooks" or "hook visibility"

---

## Quick Reference: Visibility Patterns

**Critical insight**: PostToolUse hook stdout is only visible to Claude when JSON contains `"decision": "block"`.

| Output Format                  | Claude Visibility |
| ------------------------------ | ----------------- |
| Plain text                     | Not visible       |
| JSON without `decision: block` | Not visible       |
| JSON with `decision: block`    | Visible           |

**Exit code behavior**:

| Exit Code | stdout Behavior                         | Claude Visibility             |
| --------- | --------------------------------------- | ----------------------------- |
| **0**     | JSON parsed, shown in verbose mode only | Only if `"decision": "block"` |
| **2**     | Ignored, uses stderr instead            | stderr shown to Claude        |
| **Other** | stderr shown in verbose mode            | Not shown to Claude           |

---

## Minimal Working Pattern

```bash
/usr/bin/env bash << 'SKILL_SCRIPT_EOF'
#!/usr/bin/env bash
set -euo pipefail

# Read hook payload from stdin
PAYLOAD=$(cat)
FILE_PATH=$(echo "$PAYLOAD" | jq -r '.tool_input.file_path // empty')

[[ -z "$FILE_PATH" ]] && exit 0

# Your condition here
if [[ condition_met ]]; then
    jq -n \
        --arg reason "[HOOK] Your message to Claude" \
        '{decision: "block", reason: $reason}'
fi

exit 0
SKILL_SCRIPT_EOF
```

**Key points**:

1. Use `jq -n` to generate valid JSON
2. Include `"decision": "block"` for visibility
3. Exit with code 0
4. The "blocking error" label is cosmetic - operation continues

---

## TodoWrite Templates

### Creating a PostToolUse Hook

```markdown
1. [pending] Create hook script with shebang and set -euo pipefail
2. [pending] Parse PAYLOAD from stdin with jq
3. [pending] Add condition check for when to trigger
4. [pending] Output JSON with decision:block pattern
5. [pending] Register hook in hooks.json with matcher
6. [pending] Test by editing a matching file
7. [pending] Verify Claude sees the message in system-reminder
```

### Debugging Invisible Hook Output

```markdown
1. [pending] Verify hook executes (add debug log to /tmp)
2. [pending] Check JSON format is valid (pipe to jq .)
3. [pending] Confirm decision:block is present in output
4. [pending] Verify exit code is 0
5. [pending] Check hooks.json matcher pattern
6. [pending] Restart Claude Code session
```

---

## Reference Documentation

- [Lifecycle Reference](./references/lifecycle-reference.md) - All 10 hook events, diagrams, use cases, configuration pitfalls
- [Visibility Patterns](./references/visibility-patterns.md) - Full exit code and JSON schema details
- [Hook Templates](./references/hook-templates.md) - Copy-paste templates for common patterns
- [Debugging Guide](./references/debugging-guide.md) - Troubleshooting invisible output

---

## Post-Change Checklist (Self-Evolution)

When this skill is updated:

- [ ] Update [evolution-log.md](./references/evolution-log.md) with discovery
- [ ] Verify code examples still work
- [ ] Check if ADR needs updating: [PostToolUse Hook Visibility ADR](../../../../docs/adr/2025-12-17-posttooluse-hook-visibility.md)

---

## Related Resources

- [ADR: PostToolUse Hook Visibility](../../../../docs/adr/2025-12-17-posttooluse-hook-visibility.md)
- [GitHub Issue #3983](https://github.com/anthropics/claude-code/issues/3983) - Original bug report
- [Claude Code Hooks Reference](https://code.claude.com/docs/en/hooks) - Official documentation

---

## Troubleshooting

| Issue                      | Cause                          | Solution                                            |
| -------------------------- | ------------------------------ | --------------------------------------------------- |
| Hook output not visible    | Missing decision:block in JSON | Add `"decision": "block"` to JSON output            |
| JSON parse error in hook   | Invalid JSON syntax            | Use `jq -n` to generate valid JSON                  |
| Hook not executing         | Wrong matcher pattern          | Check hooks.json matcher regex matches tool name    |
| Plain text output ignored  | Only JSON parsed               | Wrap output in JSON with decision:block             |
| Exit code 2 behavior       | stderr used instead of stdout  | Use exit 0 with JSON, or exit 2 for stderr messages |
| Session not seeing changes | Hooks cached                   | Restart Claude Code session after hook changes      |
| Verbose mode not showing   | Disabled by default            | Enable verbose mode in Claude Code settings         |
| jq command not found       | jq not installed               | `brew install jq`                                   |
