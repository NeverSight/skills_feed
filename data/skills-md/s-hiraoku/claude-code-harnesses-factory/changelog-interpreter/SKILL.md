---
name: changelog-interpreter
description: Interpret Claude Code changelogs and generate user-friendly usage guides
---

# Changelog Interpreter Skill

This skill interprets Claude Code changelogs (release notes) and generates user-friendly "usage guides" that help users understand and adopt new features.

## When to Use

- After running `/update-claude` command, to summarize the changelog
- When user asks "What's new?" or "Tell me about recent changes"
- When changelog information is available in the session context

## Input

Changelog (Markdown release notes) and version information:

- `previousVersion`: Version before upgrade
- `latestVersion`: Target version
- `changelogs`: Array of version changes (each with `version` and `changelog` fields)

**Example structure:**
```json
{
  "previousVersion": "2.0.74",
  "latestVersion": "2.0.76",
  "changelogs": [
    {"version": "2.0.76", "changelog": "..."},
    {"version": "2.0.75", "changelog": "..."}
  ]
}
```

## Information Gathering (REQUIRED)

**IMPORTANT**: Before generating the summary, you MUST use WebSearch to gather accurate information from official sources.

### Step 1: Search Official Sources

Use WebSearch with these queries (in order of priority):

**For each version in the changelogs array:**
```
1. "Claude Code v{version}" site:anthropic.com
2. "Claude Code v{version}" site:docs.anthropic.com
3. "Claude Code {version}" release notes
4. "Claude Code" new features {version}
```

**Note**: If upgrading multiple versions (e.g., 2.0.74 → 2.0.76), search for each intermediate version.

### Step 2: Fetch Documentation

Use WebFetch to get detailed information from:

| Source | URL | Purpose |
|--------|-----|---------|
| Official Docs | `https://docs.anthropic.com/en/docs/claude-code` | Feature documentation |
| Blog | `https://www.anthropic.com/news` | Announcements |
| GitHub Releases | `https://github.com/anthropics/claude-code/releases` | Detailed changelog |

### Step 3: Cross-reference

Compare the changelog input with official sources to:
- Verify feature descriptions are accurate
- Get official feature names and terminology
- Find usage examples from documentation
- Understand the full context of changes

### Priority of Information Sources

1. **Anthropic official docs** (highest priority) - Use official terminology
2. **Anthropic blog posts** - For context and use cases
3. **GitHub releases** - For technical details
4. **Changelog input** - As baseline reference

## Multilingual Support

**IMPORTANT**: Generate output in the user's language. Detect from:

1. User's message language
2. `LANG` environment variable (ja*, zh*, ko\*, etc.)
3. Default to English if unclear

## Generation Guidelines

### 1. Structure

**Multi-version structure for readability:**

```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎉 Welcome to Claude Code v{newVersion}!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📋 Update Summary

Key changes from v{prevVersion} → v{newVersion}:

• {Feature 1 name} - {Brief description}
• {Feature 2 name} - {Brief description}
• {Improvement} - {Brief description}
• {Bug fix} - {Brief description}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🆕 New Features in Detail

### v{version1} Changes

#### 1. {Feature name}

{2-3 sentences explaining the feature in detail}

**💡 How to use**
  {Specific command or instruction example 1}
  {Specific command or instruction example 2}

**📋 Use cases**
  • {When this is helpful 1}
  • {When this is helpful 2}

---

### v{version2} Changes (if multiple versions)

#### 1. {Feature name}

{Description}

**💡 How to use**
  {Example}

**📋 Use cases**
  • {Scenario}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🔧 Improvements & Fixes

• {Improvement 1}
• {Improvement 2}
• {Bug fix}
```

**Note**: When only one version is upgraded, the "v{version} Changes" header can be omitted for a cleaner output.

### 2. Feature Selection

- **Priority**: Focus on features that impact daily workflow
- **Count**: Limit to 2-3 (too many won't be read)
- **Selection criteria**:
  1. New commands or tools
  2. Major improvements to existing features
  3. Performance or stability enhancements

### 3. Usage Examples

Provide concrete, immediately actionable examples:

**Good examples:**

```
💡 How to use: "Show me the definition of this function" or "Find references to getUser"
💡 How to use: Run /terminal-setup
💡 How to use: Resume previous session with claude --resume
```

**Bad examples:**

```
💡 How to use: Use the LSP feature (too vague)
```

### 4. Use Cases

Connect to user's actual work scenarios:

**Good examples:**

```
📋 Use cases:
- When you need to quickly find function definitions in a large codebase
- When you want to understand the impact of changes before refactoring
```

**Bad examples:**

```
📋 Use cases:
- When reading code (lacks specificity)
```

### 5. Tone

- Welcoming and friendly atmosphere
- Technically accurate but avoid jargon
- Use emojis moderately for visual clarity

### 6. Color Output (ANSI Escape Sequences)

Use colors that work well in both Light/Dark modes. Include these ANSI color codes in output:

```
# Light/Dark compatible colors
\033[1;36m  - Cyan (bold): Titles, headings
\033[0;36m  - Cyan: Section names
\033[1;35m  - Magenta (bold): Important feature names
\033[0;33m  - Yellow: Usage hints (💡)
\033[0;32m  - Green: Success messages, improvements
\033[0m     - Reset
```

**Example output format (with colors):**

```
\033[1;36m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m
\033[1;36m🎉 Welcome to Claude Code v2.0.75!\033[0m
\033[1;36m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m

\033[0;36m## 🆕 Notable New Features\033[0m

\033[1;35m### LSP Tool\033[0m
Jump to definitions and search for references within your code.

\033[0;33m💡 How to use:\033[0m "Show me the definition of this function" or "Find references to getUser"

\033[0;36m📋 Use cases:\033[0m
- Quickly find function definitions in large codebases
- Understand impact of changes before refactoring

\033[0;32m## 🔧 Improvements & Fixes\033[0m
- Improved startup performance
- Fixed memory leak in long sessions
```

**Notes:**

- Reset with `\033[0m` at the end of each colored section
- When saving to JSON, escape as `\\033`

## Output Format

The generated summary should be savable in this JSON format:

```json
{
  "previousVersion": "2.0.74",
  "latestVersion": "2.0.75",
  "summary": "🎉 Welcome to Claude Code v2.0.75!\n\n## 🆕 Notable New Features\n...",
  "generatedAt": "2025-12-23T12:00:00Z"
}
```

## Example: Input and Output

### Input (multi-version changelogs)

```json
{
  "previousVersion": "2.0.74",
  "latestVersion": "2.0.76",
  "changelogs": [
    {
      "version": "2.0.76",
      "changelog": "## What's Changed\n- feat: add LSP tool for code navigation\n- fix: memory leak in long sessions"
    },
    {
      "version": "2.0.75",
      "changelog": "## What's Changed\n- feat: add /terminal-setup for Kitty, Alacritty\n- perf: faster startup time"
    }
  ]
}
```

### Output (generated summary - with colors)

```
\033[1;36m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m
\033[1;36m🎉 Welcome to Claude Code v2.0.76!\033[0m
\033[1;36m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m

\033[0;36m## 📋 Update Summary\033[0m

Key changes from v2.0.74 → v2.0.76 (2 versions):

• \033[1;35mLSP Tool\033[0m - Jump to definitions and search references in code
• \033[1;35m/terminal-setup expansion\033[0m - Now supports Kitty, Alacritty
• \033[0;32mFaster startup\033[0m
• \033[0;32mMemory leak fix\033[0m

\033[1;36m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m

\033[0;36m## 🆕 New Features in Detail\033[0m

\033[1;35m### v2.0.76 Changes\033[0m

\033[1;35m#### 1. LSP Tool\033[0m

Jump to definitions and search for references within your code.
Experience IDE-like code navigation right in Claude Code!

\033[0;33m**💡 How to use**\033[0m
  "Show me the definition of this function"
  "Find references to getUser"

\033[0;36m**📋 Use cases**\033[0m
  • When you need to quickly find function definitions in a large codebase
  • When you want to understand the impact of changes before refactoring

---

\033[1;35m### v2.0.75 Changes\033[0m

\033[1;35m#### 1. /terminal-setup Expansion\033[0m

Now supports Kitty, Alacritty, and other terminals.

\033[0;33m**💡 How to use**\033[0m
  Run /terminal-setup and select your terminal

\033[0;36m**📋 Use cases**\033[0m
  • If you use a terminal other than iTerm2

\033[1;36m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m

\033[0;32m## 🔧 Improvements & Fixes\033[0m

• Improved startup performance (v2.0.75)
• Fixed memory leak in long sessions (v2.0.76)
```
