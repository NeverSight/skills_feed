---
name: code-standards
description: "Setup universal code quality standards in your project. Use when the user wants to generate coding standards files (CLAUDE.md, AGENTS.md, GEMINI.md, etc.) or mentions 'code standards', 'code review setup', or similar intent in any language."
version: "1.0.0"
metadata:
  author: qiaoshouqing
---

# Code Standards — Universal AI Tool Configuration Generator

Generate code standards files based on Linus Torvalds' "Good Taste" philosophy. Auto-detects AI tools in your project and creates the appropriate configuration files in the user's language.

## When to Use

- User wants to set up coding standards for a project
- User wants to sync code quality rules across AI coding tools
- User mentions "code standards", "init claude md", "code review", or equivalent in any language

## Instructions for Agent

### Step 1: Detect Language & Read Template

Detect the user's language. Read the matching template from this skill's `references/` directory:

- Simplified Chinese → `references/code-standards-zh-CN.md`
- Traditional Chinese → `references/code-standards-zh-TW.md`
- Japanese → `references/code-standards-ja.md`
- All other languages → `references/code-standards-en.md`

### Step 2: Detect AI Tools

```bash
PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)

[ -d "$PROJECT_ROOT/.cursor" ] && echo "CURSOR"
[ -f "$PROJECT_ROOT/AGENTS.md" ] || [ -d "$PROJECT_ROOT/.codex" ] && echo "CODEX"
[ -f "$PROJECT_ROOT/GEMINI.md" ] || [ -d "$PROJECT_ROOT/.gemini" ] && echo "GEMINI"
[ -d "$PROJECT_ROOT/.github" ] && echo "COPILOT"
[ -d "$PROJECT_ROOT/.windsurf" ] || [ -f "$PROJECT_ROOT/.windsurfrules" ] && echo "WINDSURF"
[ -f "$PROJECT_ROOT/.aider.conf.yml" ] && echo "AIDER"
[ -d "$PROJECT_ROOT/.clinerules" ] || [ -d "$PROJECT_ROOT/.roo" ] && echo "CLINE"
```

### Step 3: Generate Files

Write the template content directly. No confirmation needed — the user invoked this skill, that IS the intent.

**Always generate:** `CLAUDE.md`

**For each detected tool, also generate:**

| Tool | File | Notes |
|------|------|-------|
| Cursor | `.cursor/rules/code-standards.mdc` | Prepend `---\ndescription: "Linus Torvalds code standards"\nalwaysApply: true\n---\n` |
| Codex | `AGENTS.md` | Same content |
| Gemini | `GEMINI.md` | Same content |
| Copilot | `.github/copilot-instructions.md` | `mkdir -p .github` first |
| Windsurf | `.windsurfrules` | Same content |
| Aider | `CONVENTIONS.md` | Same content |
| Cline/Roo | `.clinerules/code-standards.md` | `mkdir -p .clinerules` first |

### Step 4: Report

Report created files in the user's language. Keep it brief.

## Response Guidelines

1. **Execute immediately** — No confirmation, no "shall I proceed?". Just write.
2. **Unconditionally overwrite existing files** — Always overwrite CLAUDE.md and other config files without asking. The invocation is explicit intent to replace.
3. **Respond in user's language** — Match the language they used to invoke.
4. **No extra commentary** — Detect, write, report. Done.

## Error Handling

| Situation | Action |
|-----------|--------|
| Not in a git repo | Use current directory as root |
| No tools detected | Only generate `CLAUDE.md` |
| Permission denied | Report error with path |
| Template not found | Fall back to English |
