---
name: agent-install-guide
description: "Use when creating INSTALL.md, setup guides, or configuration instructions intended to be executed by AI agents."
license: MIT
metadata:
  author: shihyuho
  version: "1.0.0"
---

# Agent Install Guide

## Overview

AI agents need **deterministic**, **verifiable** instructions. Unlike humans who can infer "download to a safe place", AI agents need exact paths and explicit success criteria.

This skill provides principles for writing "Agent-Ready" installation guides.

## When to Use

- Creating installation or setup documentation
- Writing guides that AI agents will execute
- Documenting installation for automation

## Workflow

1. **Ask for filename**: User may have a preferred location (e.g., `docs/setup.md`, `INSTALL.md`). If no preference, suggest `INSTALL.md`.
2. **Apply principles**: Follow the core principles below when writing.
3. **Offer README integration**: After creating the guide, ask if user wants to add a reference to their project README.

## Core Principles

These are the concepts to internalize, not rules to follow blindly:

### 1. Determinism

Every instruction should have exactly one interpretation.

| ❌ Ambiguous | ✅ Deterministic |
|--------------|------------------|
| "Download to a safe location" | "Download to `~/.local/share/toolname`" |
| "Add to your PATH" | `echo 'export PATH=...' >> ~/.zshrc` |
| "Edit the config file" | Provide full content via heredoc |

### 2. Idempotency

Commands should be safe to run multiple times.

| ❌ Fragile | ✅ Idempotent |
|------------|---------------|
| `mkdir config` | `mkdir -p ~/.config/app` |
| `ln -s src dest` | `ln -sf src dest` |
| `rm file` | `rm -f file` |

### 3. Verifiability

Every significant step should have a way to confirm success.

**Examples of verification:**
- `which toolname` - binary is in PATH
- `toolname --version` - correct version installed
- `ls -l ~/.config/app/` - config file exists
- `curl localhost:8080/health` - service is running

### 4. Interactivity

When choices exist, ask the user rather than assuming.

**Trigger situations:**
- Multiple installation options (plugins, themes)
- Platform-specific paths
- Optional features
- Subscription tiers

## Patterns & Techniques

Use these when applicable to your specific installation:

### Meta-Instructions Block

A block at the top telling executing agents what to do. Adapt to your needs:

```markdown
> **🤖 AI AGENTS:** [What to do before/during installation]
> - [Action 1]
> - [Action 2]
> - [Verification instruction]
```

### Heredoc for Config Files

Instead of "edit the file", provide complete content:

```bash
cat <<EOF > ~/.config/myapp/config.json
{
  "key": "value"
}
EOF
```

### Decision Trees

When installation branches based on user choice:

```markdown
**If user has Pro subscription:**
`npm install myapp-pro`

**If user has Free tier:**
`npm install myapp-free`
```

### Shell Detection (when needed)

Only when modifying shell config. Not every installation needs this.

```bash
# Detect shell config file
case "$SHELL" in
  */zsh)  SHELL_RC="${ZDOTDIR:-$HOME}/.zshrc" ;;
  */bash) SHELL_RC="$HOME/.bashrc" ;;
  */fish) SHELL_RC="$HOME/.config/fish/config.fish" ;;
  *)      SHELL_RC="$HOME/.profile" ;;
esac
```

## Common Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| Relative paths | `ln -s ./file` breaks in wrong directory | Use `$(pwd)/file` or absolute paths |
| Vague "add to PATH" | Agent doesn't know which shell | Provide exact command or detect shell |
| Missing `sudo` warning | Agent fails on permission denied | Warn upfront or use user-space dirs |
| Interactive prompts | `apt install` hangs waiting for input | Use `-y` flag or equivalent |

## Limitations

- **Unix-focused**: macOS/Linux assumed. Windows needs different handling.
- **User-space preferred**: Avoid system directories when possible.

## Reference

See `references/INSTALL_TEMPLATE.md` for structural concepts.
See `references/README_INTEGRATION_TEMPLATE.md` for adding install links to README.
