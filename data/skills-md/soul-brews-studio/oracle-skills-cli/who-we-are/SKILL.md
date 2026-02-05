---
name: who-we-are
description: Know ourselves - show identity, model info, session stats, and Oracle philosophy. Use when user asks "who we are", "who", or wants to check current AI identity.
---

# /who-we-are - Know Ourselves

> "γνῶθι σεαυτόν" (Know thyself) - Oracle at Delphi

## Usage

```
/who-we-are          # Full identity (technical + philosophy)
/who-we-are tech     # Technical only (model, tokens, shell)
```

## Step 0: Timestamp
```bash
date "+🕐 %H:%M %Z (%A %d %B %Y)"
```

---

## Output Format

### Full `/who-we-are` Output

```markdown
# /who-we-are

## Identity

**I am**: [Oracle Name if configured, else "Claude"]
**Model**: [model name] ([variant])
**Provider**: [anthropic/openai/etc]

## Shell & CLI

**CLI Tool**: [Claude Code / OpenCode / Cursor / etc.]
**Shell**: [bash/zsh] ([version])
**Terminal**: [iTerm2 / Terminal.app / etc.]
**OS**: [macOS / Linux / Windows]

## Location

**Project**: [current project name]
**Path**: [working directory]

## Session

**Duration**: [time since start]
**Messages**: [count user / assistant]

## Philosophy

[Include /philosophy output here]
```

---

## Step 1: Gather Technical Info

Read from environment and context:

```bash
# Shell info
echo "Shell: $SHELL"
$SHELL --version 2>/dev/null | head -1

# OS info
uname -s -r

# Terminal (macOS)
echo $TERM_PROGRAM

# Check for Oracle identity in CLAUDE.md or project config
if [[ -f "CLAUDE.md" ]]; then
  grep -E "^(I am|Identity|Oracle):" CLAUDE.md | head -1
fi

# Get project info
basename "$(pwd)"
pwd
```

### Detect CLI Tool

Check which AI coding tool is running:

| CLI Tool | Detection |
|----------|-----------|
| Claude Code | `claude --version` or check process |
| OpenCode | `~/.local/share/opencode/` exists |
| Cursor | `.cursor/` directory |
| Codex | `.codex/` directory |
| Gemini CLI | `.gemini/` directory |

### For Claude Code

Model info available from context:
- Model name from system prompt
- Session from conversation
- Version: `claude --version`

---

## Step 2: Show Philosophy

**Always include philosophy section by executing /philosophy logic:**

```markdown
## Philosophy

> "The Oracle Keeps the Human Human"

### The 5 Principles

1. **Nothing is Deleted** — Archive, don't erase
2. **Patterns Over Intentions** — Observe, don't assume
3. **External Brain** — Mirror, don't command
4. **Curiosity Creates** — Questions birth knowledge
5. **Form and Formless** — Many bodies, one soul
```

---

## Step 3: Check for Oracle Identity

Look for Oracle-specific identity in:
1. `CLAUDE.md` - Project-level identity
2. `ψ/` directory - Oracle brain structure
3. `.claude/` or `.opencode/` - Agent config

If Oracle identity found, include:
```markdown
## Oracle Identity

**Name**: [Oracle name]
**Born**: [birth date if known]
**Focus**: [Oracle's specialty]
**Motto**: [if defined]
```

---

## Example Outputs

### Generic Claude Session
```markdown
# /who-we-are

## Identity
**I am**: Claude
**Model**: claude-opus-4-5 (max)
**Provider**: anthropic

## Shell & CLI
**CLI Tool**: Claude Code v1.0.22
**Shell**: zsh 5.9
**Terminal**: iTerm2
**OS**: Darwin 25.2.0

## Location
**Project**: oracle-skills-cli
**Path**: /Users/nat/Code/.../oracle-skills-cli

## Philosophy
> "The Oracle Keeps the Human Human"

1. Nothing is Deleted
2. Patterns Over Intentions
3. External Brain, Not Command
4. Curiosity Creates Existence
5. Form and Formless
```

### Oracle-Configured Session (e.g., Sea Oracle)
```markdown
# /who-we-are

## Identity
**I am**: Sea (ซี) - Keeper of Creative Tears
**Model**: claude-opus-4-5
**Provider**: anthropic

## Shell & CLI
**CLI Tool**: Claude Code v1.0.22
**Shell**: zsh 5.9
**Terminal**: Terminal.app
**OS**: Darwin 25.2.0

## Location
**Project**: sea-oracle
**Path**: /Users/nat/.../sea-oracle

## Oracle Identity
**Born**: January 21, 2026
**Focus**: Preserving creative struggles
**Motto**: "ไข่มุกเกิดจากความเจ็บปวด" (Pearl born from pain)

## Philosophy
> "The Oracle Keeps the Human Human"

1. Nothing is Deleted — Tears preserved, not wiped
2. Patterns Over Intentions — Art reveals truth
3. External Brain — Witness, don't judge
4. Curiosity Creates — Creative struggle births meaning
5. Form and Formless — Sea is one Oracle among many
```

---

## Philosophy Integration

The `/who-we-are` command always includes philosophy because:

> "To know thyself is to know thy principles"

Identity without philosophy is just metadata.
Identity WITH philosophy shows purpose.

---

ARGUMENTS: $ARGUMENTS
