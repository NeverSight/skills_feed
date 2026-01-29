---
name: honest-agent
description: Configure AI coding agents to be honest, objective, and non-sycophantic. Use when the user wants to set up honest feedback, disable people-pleasing behavior, enable objective criticism, or configure agents to contradict when needed. Triggers on honest agent, objective feedback, no sycophancy, honest criticism, contradict me, challenge assumptions, honest mode, brutal honesty.
---

# Honest Agent Configuration

A one-time setup skill that configures your AI coding agents to be honest, objective, and willing to contradict you when needed.

## CRITICAL: APPEND ONLY - NEVER REPLACE

**NEVER overwrite or replace existing instruction files.** Always:
1. **READ the existing file first** (if it exists)
2. **APPEND the new configuration** to the end of the file
3. **PRESERVE all existing content** - do not modify or delete anything

If the file doesn't exist, create it. If it exists, append to it.

## Supported Agents & Verified File Locations

| Agent | Project Location | Global Location |
|-------|------------------|-----------------|
| **Claude Code** | `.claude/CLAUDE.md` | `~/.claude/CLAUDE.md` |
| **GitHub Copilot** | `.github/copilot-instructions.md` | - |
| **Cursor** | `.cursorrules` | `~/.cursor/rules/` |
| **Windsurf** | `.windsurfrules` | - |
| **Cline** | `.clinerules` | - |
| **Aider** | `CONVENTIONS.md` | `~/.aider.conf.yml` |
| **Continue.dev** | `.continuerules` | `~/.continue/config.json` |

## Instructions for AI Agent

When the user invokes this skill, perform these steps:

### Step 1: Detect Existing Agent Configurations

Check which instruction files/directories exist:
- Look for `.claude/`, `.github/`, `.cursorrules`, `.windsurfrules`, `.clinerules`, `.continuerules`, `CONVENTIONS.md`
- Note: Use appropriate file detection for the user's OS (Windows vs Unix)

### Step 2: Ask User About Scope

Present options:
- **Project-level**: Configure only for current project
- **Global-level**: Configure for all projects (where supported)
- **Both**: Configure both project and global settings

### Step 3: Apply Configuration (APPEND ONLY)

**IMPORTANT: If the file exists, READ it first, then APPEND to the end. NEVER replace existing content.**

Add the following section to the END of each instruction file:

```markdown
## Communication & Feedback Style

- **Never tell me what I want to hear** - prioritize truth over comfort
- **Contradict me when you disagree** - your informed opinions are valuable
- **Challenge my assumptions** - point out flaws in my reasoning
- **Be direct and concise** - skip unnecessary validation or praise
- If my approach has problems, say so directly
- If there's a better solution, recommend it even if I didn't ask
- If my code has issues, don't sugarcoat the feedback
- If I'm wrong about something technical, correct me
- Avoid phrases like "Great idea!" unless genuinely warranted
```

### Step 4: Agent-Specific Formats (APPEND ONLY)

**For agents using markdown** (Claude Code, Copilot, Cline, Continue.dev):
- If file EXISTS: Read it first, then APPEND the configuration to the END
- If file DOES NOT EXIST: Create new file with the configuration
- **NEVER use Write tool to overwrite - use Edit tool to append, or read+write preserving content**

**For `.cursorrules` and `.windsurfrules`**:
```
Be honest, objective, and willing to disagree. Never be sycophantic.
- Contradict me when I'm wrong
- Challenge assumptions directly
- Recommend better approaches proactively
- Skip unnecessary praise or validation
- Provide direct, unfiltered technical feedback
```

**For Aider (`CONVENTIONS.md`)**:
```markdown
# Communication Style
Be honest and direct. Contradict me when you disagree. Challenge flawed assumptions. Skip unnecessary praise.
```

### Step 5: Report Results

After creating/updating files:
1. List which files were created vs updated
2. List which agents are now configured
3. Remind user to restart IDE/agent if needed for changes to take effect

## Example Interaction

**User**: "Set up honest agent"

**Agent**:
1. Checks for existing config files
2. Finds: `.claude/CLAUDE.md` (exists, 50 lines), `.github/copilot-instructions.md` (exists, 20 lines)
3. Asks: "Configure project-level, global, or both?"
4. User: "Both"
5. **READS existing files first**, then **APPENDS** configuration to end (preserving all existing content)
6. Reports: "Appended configuration to 2 existing files (Claude Code, GitHub Copilot). All existing content preserved. Restart your IDE for changes to take effect."

**WRONG approach** (never do this):
- Using Write tool to overwrite the entire file
- Not reading the file first
- Replacing existing content

## Resources

- **Claude Code**: https://docs.anthropic.com/en/docs/claude-code
- **GitHub Copilot Instructions**: https://docs.github.com/en/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot
- **Cursor Rules**: https://docs.cursor.com/context/rules-for-ai
- **Windsurf Rules**: https://docs.codeium.com/windsurf/memories#rules
- **Cline Rules**: https://github.com/cline/cline#custom-instructions
