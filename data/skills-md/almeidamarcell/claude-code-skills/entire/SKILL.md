---
name: entire
description: Capture AI agent sessions in your git workflow. Use for setup, rewinding to checkpoints, exploring session history, and troubleshooting.
---

# Entire - AI Session Tracking for Git

## Overview

Entire hooks into your git workflow to capture AI agent sessions on every push. Sessions are indexed alongside commits, creating a searchable record of how code was written in your repo.

**Core capabilities:**
- 📸 **Checkpoint sessions** - Save points you can rewind to
- ⏪ **Rewind to any checkpoint** - Restore code to earlier states
- 📖 **Explain sessions** - Understand how code was created
- 🔄 **Resume previous work** - Pick up where you left off
- 🩺 **Diagnose issues** - Fix stuck sessions

## When to Use This Skill

**Use this skill when:**
- User wants to install/enable Entire
- User mentions rewinding, undoing, or reverting AI changes
- User wants to understand how code was generated
- User asks about session history or checkpoints
- User encounters Entire errors or stuck sessions
- User wants to resume previous AI work

**Don't use for:**
- Standard git operations (use git directly)
- Code review (use standard review tools)
- General debugging (unless related to Entire sessions)

## Prerequisites Check

Before helping with Entire, verify:

```bash
# Check if Entire is installed
which entire

# Check if repository has Entire enabled
entire status
```

If not installed, guide user through installation first.

## Installation & Setup

### Installing Entire

**Recommended: Homebrew (macOS/Linux)**
```bash
brew tap entireio/tap
brew install entireio/tap/entire
```

**Alternative: Go**
```bash
go install github.com/entireio/cli/cmd/entire@latest
```

### Enabling in Repository

**Default setup (manual-commit strategy):**
```bash
cd /path/to/your/repo
entire enable
```

**With options:**
```bash
# Use auto-commit strategy (creates git commits automatically)
entire enable --strategy auto-commit

# Setup for Gemini CLI instead of Claude Code
entire enable --agent gemini

# Disable automatic session push
entire enable --skip-push-sessions

# Force reinstall hooks
entire enable --force

# Save settings locally (not committed to git)
entire enable --local
```

**What `entire enable` does:**
1. Installs git hooks to track AI sessions
2. Creates `.entire/` directory for configuration
3. Sets up session tracking (default: manual-commit strategy)
4. Your code commits stay clean - session metadata stored separately on `entire/checkpoints/v1` branch

**After enabling:**
```bash
entire status  # Verify Entire is active
```

## Key Concepts

### Sessions
A **session** represents a complete interaction with your AI agent from start to finish.

**Session ID format:** `YYYY-MM-DD-<UUID>`
Example: `2026-02-11-abc123de-f456-7890-abcd-ef1234567890`

Sessions capture:
- All prompts and responses
- Files modified
- Timestamps
- Agent metadata

**Storage:** Sessions are stored on the `entire/checkpoints/v1` branch, separate from your code.

### Checkpoints
A **checkpoint** is a snapshot within a session - a save point you can rewind to.

**Checkpoint ID format:** 12-character hex string
Example: `a3b2c4d5e6f7`

**When checkpoints are created:**
- **manual-commit strategy** (default): When you or agent make a git commit
- **auto-commit strategy**: After each agent response

### Strategies

| Strategy | Code Commits | Safe on main? | Best For |
|----------|--------------|---------------|----------|
| **manual-commit** (default) | None on your branch | ✅ Yes | Most workflows - keeps git history clean |
| **auto-commit** | Automatic after each response | ⚠️ Use caution | Teams wanting automatic code commits |

**Switching strategies:**
```bash
entire disable
entire enable --strategy auto-commit
```

## Core Workflows

### 1. Check Current Session Status

Always start by checking status:

```bash
entire status
```

**Output includes:**
- Current session ID
- Active strategy
- Number of checkpoints
- Whether session is in progress

**Interpreting status:**
- **"No active session"** - Start working with Claude Code/Gemini
- **"Session in progress"** - Currently tracking
- **"Entire is disabled"** - Run `entire enable`

### 2. Rewind to Previous Checkpoint

When agent makes unwanted changes:

```bash
entire rewind
```

**Interactive flow:**
1. Shows list of available checkpoints with:
   - Checkpoint ID
   - Timestamp
   - Associated commit message (if any)
2. User selects checkpoint
3. Code restored to that exact state

**What rewind does:**
- Restores all files to checkpoint state
- Preserves session history
- Non-destructive (can rewind forward again)

**Manual-commit strategy:**
- Always allows full rewind
- Restores files from shadow branch

**Auto-commit strategy:**
- Full rewind on feature branches
- Logs-only on main (preserves shared history)

**Example scenario:**
```
User: "The Claude just broke my authentication, I want to go back"
Assistant: Let me help you rewind to before those changes.

$ entire rewind

# Then guide user through checkpoint selection
```

### 3. Resume Previous Session

To pick up where you left off on a different branch:

```bash
entire resume <branch-name>
```

**What it does:**
1. Checks out the specified branch
2. Restores latest checkpointed session metadata
3. Prints command(s) to continue work

**Example:**
```bash
entire resume feature/auth
# Output:
# Checked out branch 'feature/auth'
# Restored session: 2026-02-11-abc123de...
# To continue: claude code continue
```

### 4. Explain Sessions and Commits

Understand how code was created:

```bash
# Explain current session
entire explain

# Explain specific session
entire explain <session-id>

# Explain specific commit
entire explain <commit-hash>
```

**Use cases:**
- "How was this feature implemented?"
- "What prompts led to these changes?"
- "Why did the agent make this decision?"

**Output includes:**
- Session transcript
- Prompts and responses
- Files touched
- Reasoning and context

### 5. Troubleshooting with Doctor

When sessions are stuck or behaving strangely:

```bash
entire doctor
```

**What doctor does:**
- Detects orphaned sessions
- Identifies conflicting state
- Suggests fixes
- Can clean up automatically

**Common issues doctor fixes:**
- Stuck sessions that won't checkpoint
- Shadow branch conflicts
- Metadata inconsistencies

**Example:**
```
User: "Entire says I have a session but I don't see any checkpoints"
Assistant: Let's run the doctor to diagnose this.

$ entire doctor
```

### 6. Clean Up Orphaned Data

Remove unused Entire data:

```bash
entire clean
```

**What it cleans:**
- Orphaned shadow branches
- Old session metadata
- Unreferenced checkpoints

**When to use:**
- After heavy rebasing
- When switching strategies
- Periodic maintenance

### 7. Reset Shadow Branch

Nuclear option when shadow branch is corrupted:

```bash
entire reset
```

**⚠️ WARNING:** This deletes the shadow branch and session state for current HEAD commit.

**When to use:**
- Shadow branch conflicts that doctor can't fix
- After complex git operations (rebase, merge conflicts)
- Starting fresh on current commit

**What it does:**
- Deletes `entire/<HEAD-hash>-<worktree-hash>` branch
- Clears session state for current commit
- Does NOT affect committed checkpoints on `entire/checkpoints/v1`

**Use with force flag:**
```bash
entire reset --force
```

### 8. Disable Entire

Temporarily or permanently disable:

```bash
entire disable
```

**What it does:**
- Removes git hooks
- Stops session tracking
- Preserves all existing session data
- Your code and commit history remain untouched

**Re-enable:**
```bash
entire enable --force
```

## Configuration

Entire uses two config files in `.entire/`:

### settings.json (Project Settings)
Shared across team, typically committed:

```json
{
  "strategy": "manual-commit",
  "agent": "claude-code",
  "enabled": true
}
```

### settings.local.json (Local Overrides)
Personal settings, gitignored:

```json
{
  "enabled": false,
  "log_level": "debug"
}
```

### Key Configuration Options

| Option | Values | Description |
|--------|--------|-------------|
| `enabled` | `true`, `false` | Enable/disable Entire |
| `log_level` | `debug`, `info`, `warn`, `error` | Logging verbosity |
| `strategy` | `manual-commit`, `auto-commit` | Session capture strategy |
| `strategy_options.push_sessions` | `true`, `false` | Auto-push checkpoints branch |
| `strategy_options.summarize.enabled` | `true`, `false` | AI-generated summaries |
| `telemetry` | `true`, `false` | Anonymous usage stats |

**Editing config:**
```bash
# Edit project settings
vim .entire/settings.json

# Edit local settings
vim .entire/settings.local.json

# Check effective settings
entire status
```

## Advanced Features

### Auto-Summarization

Generate AI summaries at commit time:

**Enable:**
```json
{
  "strategy_options": {
    "summarize": {
      "enabled": true
    }
  }
}
```

**Requirements:**
- Claude CLI installed and authenticated
- `claude` command in PATH

**What it captures:**
- Intent and outcome
- Key learnings
- Friction points
- Open items

### Git Worktrees Support

Entire works with git worktrees - each worktree has independent session tracking.

**Example:**
```bash
# Create worktree
git worktree add ../feature-branch feature/new-auth

# Enable Entire in worktree
cd ../feature-branch
entire enable

# Sessions tracked independently
```

### Concurrent Sessions

Multiple sessions can run on same commit:
- Each tracked separately
- Independent rewind
- Entire warns about concurrent work

## Troubleshooting Guide

### Common Issues

| Issue | Diagnosis | Solution |
|-------|-----------|----------|
| "Not a git repository" | Not in git repo | Navigate to git repository |
| "Entire is disabled" | Hooks not installed | `entire enable` |
| "No rewind points found" | No checkpoints created | Make a commit (manual) or wait for response (auto) |
| "shadow branch conflict" | Corrupted shadow branch | `entire reset --force` |

### SSH Authentication Errors

**Error:**
```
ssh: handshake failed: ssh: unable to authenticate
```

**Fix:**
```bash
ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts
ssh-keyscan -t ecdsa github.com >> ~/.ssh/known_hosts
```

This is a known issue with go-git's SSH handling.

### Debug Mode

**Via environment variable:**
```bash
ENTIRE_LOG_LEVEL=debug entire status
```

**Via settings:**
```json
{
  "log_level": "debug"
}
```

**Debug logs location:** `.entire/logs/`

### Stuck Sessions

**Symptoms:**
- Checkpoints not saving
- Status shows old session
- Rewind points not appearing

**Fix:**
```bash
# Try doctor first
entire doctor

# If that fails, reset
entire reset --force

# Re-enable
entire enable --force
```

### Accessibility

For screen readers:
```bash
export ACCESSIBLE=1
entire enable
```

Uses simpler text prompts instead of interactive TUI.

## Integration with Claude Code

Entire is designed to work seamlessly with Claude Code:

### During Development

**Claude Code workflow:**
1. User works with Claude Code
2. Entire automatically tracks session in background
3. Checkpoints created based on strategy
4. User can check status anytime: `entire status`

**Typical commands Claude might suggest:**

```bash
# Before starting work
entire status

# After significant changes
entire status  # Check checkpoint count

# If something goes wrong
entire rewind

# When switching tasks
entire resume <branch>
```

### When to Suggest Rewind

**Proactively suggest rewind when:**
- Agent made changes that broke tests
- User expresses regret about changes
- User says "undo", "go back", "revert"
- Implementation went in wrong direction

**Example:**
```
User: "These changes broke the login flow"
Assistant: Let's rewind to before these changes.

$ entire rewind

[Shows checkpoint list - guide user to select pre-breaking checkpoint]
```

### When to Suggest Explain

**Suggest explain when:**
- User asks "how was this created?"
- User questions agent's reasoning
- User debugging mysterious changes
- User onboarding to codebase

**Example:**
```
User: "I don't understand why the auth was implemented this way"
Assistant: Let me show you the session that created this.

$ entire explain src/auth/login.ts

[Shows session transcript and reasoning]
```

## Common Scenarios

### Scenario 1: Initial Setup

```
User: "Set up Entire for me"
Assistant: I'll help you install and enable Entire in this repository.

# First, check if Entire is installed
$ which entire

# If not installed
$ brew tap entireio/tap
$ brew install entireio/tap/entire

# Navigate to your repository
$ cd /path/to/your/repo

# Enable Entire (default: manual-commit strategy)
$ entire enable

# Verify it's working
$ entire status

Entire is now tracking your AI sessions! Work normally with Claude Code,
and checkpoints will be created when you commit.
```

### Scenario 2: Undo Unwanted Changes

```
User: "Claude just broke my authentication system, I need to undo this"
Assistant: Let's rewind to before those changes.

$ entire rewind

[Interactive checkpoint list appears]
Available checkpoints:
1. a3b2c4d5e6f7 - 2026-02-11 14:23 - "Add login validation"
2. f9e8d7c6b5a4 - 2026-02-11 14:15 - "Initial auth setup"
3. 1a2b3c4d5e6f - 2026-02-11 14:00 - "Create user model"

Select checkpoint to rewind to: 2

[Code restored to checkpoint 2]

Your code has been restored to the state before the breaking changes.
You can now continue working from this checkpoint.
```

### Scenario 3: Understanding Generated Code

```
User: "How was this payment processing code created?"
Assistant: Let me show you the session that generated this code.

$ entire explain src/payment/processor.ts

Session: 2026-02-11-abc123de-f456-7890-abcd-ef1234567890
Date: 2026-02-11 13:45 - 14:30

Prompts & Responses:
1. User: "Add Stripe payment processing"
   Claude: [Implemented payment processor with retry logic...]

2. User: "Add error handling for failed payments"
   Claude: [Added try-catch blocks and error logging...]

3. User: "Add webhook handling"
   Claude: [Created webhook endpoint and validation...]

Files Modified:
- src/payment/processor.ts (created)
- src/payment/webhooks.ts (created)
- src/api/routes.ts (modified)

This shows you the full context of how the payment system was built.
```

### Scenario 4: Resume Previous Work

```
User: "I want to continue working on the feature/auth branch"
Assistant: Let me help you resume that work.

$ entire resume feature/auth

Checked out branch 'feature/auth'
Restored session: 2026-02-10-def456gh-i789-0123-jklm-no4567890123
Last checkpoint: b1a2c3d4e5f6 - "Add password reset flow"

To continue:
$ claude code continue

You can now pick up where you left off on the auth feature.
```

### Scenario 5: Debugging Stuck Session

```
User: "Entire says I have a session but checkpoints aren't saving"
Assistant: Let's diagnose this with the doctor command.

$ entire doctor

Diagnosing Entire state...

Issues found:
✗ Orphaned session state detected
✗ Shadow branch missing for current HEAD
✓ Configuration valid
✓ Git hooks installed

Suggested fixes:
1. Clean orphaned session: entire clean
2. Reset shadow branch: entire reset --force

Run these fixes? [y/n]: y

Cleaning orphaned data...
Resetting shadow branch...

✓ Fixed! Run 'entire enable --force' to restart session tracking.

$ entire enable --force

Your Entire installation is now healthy and ready to track sessions.
```

### Scenario 6: Switching Strategies

```
User: "I want Entire to automatically commit after each response"
Assistant: I'll switch you to the auto-commit strategy.

# First, disable current setup
$ entire disable

# Re-enable with auto-commit strategy
$ entire enable --strategy auto-commit

# Verify new strategy
$ entire status

Strategy: auto-commit
Checkpoints will now be created automatically after each agent response,
with code committed to your active branch.

Note: Be cautious using auto-commit on main/master branches.
```

### Scenario 7: Exploring Session History

```
User: "Show me all the sessions where we worked on authentication"
Assistant: Let me search through your Entire session history.

$ entire explain --help  # Check available options

# List recent sessions
$ git log entire/checkpoints/v1 --oneline | grep -i auth

# Explain specific session
$ entire explain 2026-02-09-auth-session-id

This will show all sessions related to authentication work.
You can then use 'entire explain' on specific sessions to see details.
```

## Best Practices

### When to Proactively Suggest Entire

**As Claude, suggest Entire when:**

1. **Before risky changes:**
   ```
   "I'm about to refactor the database layer. Let's checkpoint first."
   $ entire status  # Verify session tracking
   ```

2. **After breaking changes:**
   ```
   "The tests are failing after my changes. Let's rewind."
   $ entire rewind
   ```

3. **When user is confused:**
   ```
   "You seem unsure about these changes. We can always rewind if needed."
   $ entire status  # Show current checkpoint count
   ```

4. **During complex iterations:**
   ```
   "We're on iteration 3 of this feature. Previous checkpoints are available if we need to backtrack."
   ```

### Communication Patterns

**Clear checkpoint messaging:**
```
✓ "Checkpoint saved. You can rewind to this point anytime."
✓ "This is checkpoint 3 in this session. Previous states are preserved."
✓ "I've committed the changes. Entire created a checkpoint automatically."

✗ Don't say: "Changes saved" (ambiguous)
✗ Don't say: "Committed" (unclear if checkpoint was created)
```

**Rewind guidance:**
```
✓ "Let's rewind to before these changes using 'entire rewind'"
✓ "We have 5 checkpoints - which point would you like to restore?"
✓ "Rewind is non-destructive - we can always move forward again"

✗ Don't say: "Let's undo this" (unclear if using git or Entire)
✗ Don't say: "Revert to previous version" (ambiguous)
```

### Integration with Development Workflow

**Start of session:**
```bash
entire status  # Check what's being tracked
```

**During development:**
- Work naturally with Claude Code
- Checkpoints happen automatically (based on strategy)
- Check status occasionally: `entire status`

**When things go wrong:**
```bash
entire rewind  # Interactive restore
```

**Switching branches:**
```bash
entire resume <branch>  # Restore session context
```

**End of day:**
```bash
entire status  # See final checkpoint count
git push  # Pushes code + checkpoints (if configured)
```

### Privacy & Security

**What Entire captures:**
- Session transcripts (prompts & responses)
- File paths and modifications
- Timestamps and metadata
- Agent configuration

**What Entire doesn't capture:**
- Credentials or secrets
- Files outside repository
- User's system information

**Logs location:** `.entire/logs/` (gitignored by default)

**Session metadata:** Stored on `entire/checkpoints/v1` branch

### Team Usage

**Sharing checkpoints:**
- Configure `strategy_options.push_sessions: true`
- Team members can see session history
- Useful for:
  - Understanding how code was built
  - Onboarding new developers
  - Code archaeology
  - Learning from AI sessions

**Personal usage:**
- Keep `push_sessions: false` for private sessions
- Use `.entire/settings.local.json` for personal preferences

## Command Reference Quick Guide

| Command | Use When | Output |
|---------|----------|--------|
| `entire status` | Check current session | Session info, strategy, checkpoint count |
| `entire enable` | First time setup | Installs hooks, creates config |
| `entire rewind` | Undo changes | Interactive checkpoint selection |
| `entire resume <branch>` | Switch branches with context | Restores session, prints continue command |
| `entire explain` | Understand code creation | Session transcript and metadata |
| `entire doctor` | Fix issues | Diagnoses and suggests fixes |
| `entire clean` | Remove orphaned data | Cleans up unused branches/metadata |
| `entire reset` | Nuclear option | Deletes shadow branch for current HEAD |
| `entire disable` | Stop tracking | Removes hooks, preserves data |
| `entire version` | Check CLI version | Version number |

## Error Messages & Solutions

### "Not a git repository"
**Cause:** Running Entire outside a git repository
**Solution:** `cd` into your git repository first

### "Entire is disabled"
**Cause:** Hooks not installed
**Solution:** `entire enable`

### "No rewind points found"
**Cause:** No checkpoints created yet
**Solution:**
- **manual-commit:** Make a git commit
- **auto-commit:** Wait for next agent response
- Check strategy: `entire status`

### "shadow branch conflict"
**Cause:** Corrupted shadow branch state
**Solution:** `entire reset --force`

### "Failed to fetch metadata: ssh: handshake failed"
**Cause:** go-git SSH bug
**Solution:**
```bash
ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts
ssh-keyscan -t ecdsa github.com >> ~/.ssh/known_hosts
```

### "Session in unexpected state"
**Cause:** Interrupted operations or git conflicts
**Solution:**
```bash
entire doctor  # Try automatic fix first
entire reset --force  # If doctor can't fix
entire enable --force  # Restart tracking
```

## Advanced Usage

### Custom Configuration

**Project-wide settings** (`.entire/settings.json`):
```json
{
  "strategy": "manual-commit",
  "agent": "claude-code",
  "enabled": true,
  "strategy_options": {
    "push_sessions": true,
    "summarize": {
      "enabled": true
    }
  },
  "telemetry": false
}
```

**Personal overrides** (`.entire/settings.local.json`):
```json
{
  "log_level": "debug",
  "strategy_options": {
    "push_sessions": false
  }
}
```

### Multiple Agents

Enable both Claude Code and Gemini CLI:

```bash
# Enable Claude Code (default)
entire enable --agent claude-code

# Also enable Gemini
entire enable --agent gemini

# Both agents can be tracked simultaneously
```

### Session Metadata Structure

**Session ID:** `YYYY-MM-DD-<UUID>`
**Checkpoint ID:** 12-char hex string

**Metadata location:**
- Active sessions: `.git/entire-sessions/`
- Committed checkpoints: `entire/checkpoints/v1` branch

**Session files include:**
- `transcript.jsonl` - Full conversation
- `metadata.json` - Session info
- `files.json` - Modified files list

### Git Worktree Isolation

Each worktree gets independent session tracking:

```bash
# Main worktree
cd /repo
entire enable
# Sessions: .git/entire-sessions/main/

# Feature worktree
git worktree add ../feature feature/new-ui
cd ../feature
entire enable
# Sessions: .git/entire-sessions/feature-worktree-hash/
```

## Limitations & Known Issues

### Known Limitations

1. **SSH Authentication** - go-git v5 SSH bug requires manual known_hosts setup
2. **Large Repositories** - Very large sessions may be slow to explain
3. **Concurrent Sessions** - Warning shown, but both tracked independently
4. **Windows Support** - Requires WSL (Windows Subsystem for Linux)

### Gemini CLI Support

Currently in **preview**:
- Basic tracking works
- All commands supported
- Report issues: https://github.com/entireio/cli/issues

### Auto-Summarization

Requirements:
- Claude CLI must be installed
- `claude` command in PATH
- Authenticated with Claude

If summarization fails:
- Non-blocking - commit still succeeds
- Check `.entire/logs/` for errors

## Getting Help

### Resources

- **GitHub Repository:** https://github.com/entireio/cli
- **Issues:** https://github.com/entireio/cli/issues
- **Documentation:** README.md in the repo

### Command Help

```bash
entire --help              # General help
entire <command> --help    # Command-specific help
entire status --help       # Example: status help
```

### When Helping Users

**Before suggesting Entire commands:**
1. Check if Entire is installed: `which entire`
2. Check if enabled: `entire status`
3. Verify git repository: Inside git repo?

**Guide users step by step:**
1. Install (if needed)
2. Enable (if not enabled)
3. Explain what will happen
4. Run the command
5. Interpret the output

**Be specific about outcomes:**
- What checkpoint will be restored
- What files will change
- Whether operation is reversible

## Summary

Entire is a git workflow enhancement for AI-assisted development that:

✅ **Captures** AI sessions as checkpoints
✅ **Preserves** full session history and reasoning
✅ **Enables** rewinding to any checkpoint
✅ **Explains** how code was created
✅ **Resumes** previous work contexts
✅ **Diagnoses** and fixes session issues

**Key principles:**
- Non-invasive (separate metadata storage)
- Reversible (rewind is non-destructive)
- Team-friendly (shareable session history)
- Privacy-conscious (configurable data sharing)

**When in doubt:**
- Run `entire status` to see current state
- Use `entire doctor` to diagnose issues
- Rewind is always safe - you can rewind forward again

---

## Skill Activation Note

This skill is activated when:
- User mentions Entire, checkpoints, or rewinding
- User wants to undo AI changes
- User asks about session history
- User encounters Entire errors
- Setup/installation is needed

Always verify Entire is installed and enabled before suggesting commands.