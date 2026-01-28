---
name: agent-speak
description: Speak messages aloud using ElevenLabs TTS. Use when completing tasks, reporting progress, or notifying the user of important events. Invoke via the agent-speak CLI command.
---

# Agent Speak

Speak messages aloud to notify the user when completing tasks.

## Usage

```bash
agent-speak "Your message here"
agent-speak --worktree <path> "Your message here"
agent-speak --voice <name> "Your message here"
agent-speak --model <model-id> "Your message here"
```

## Voice Selection

Use `--worktree` with the current working directory to get a deterministic voice unique to your worktree. This ensures agents in different worktrees have different voices.

```bash
agent-speak --worktree "$(pwd)" "Task complete"
```

Always use the worktree flag so your voice is consistent and distinct from other agents.

### Available voice presets

If you need to specify manually:
- `rachel`, `bella`, `elli`, `freya`, `nicole`, `domi` (female)
- `josh`, `adam`, `sam`, `arnold`, `dave`, `fin`, `clyde` (male)

```bash
agent-speak --voice josh "Build complete"
```

## When to Use

Speak notifications after:
- Completing a significant task
- Finishing a multi-step workflow
- Encountering an error that needs user attention
- Completing a build or deployment

## Examples

```bash
# After completing a feature
agent-speak --worktree "$(pwd)" "Finished implementing the authentication flow"

# After a build
agent-speak --worktree "$(pwd)" "Build complete with no errors"

# After an error
agent-speak --worktree "$(pwd)" "Build failed. Check the terminal for details"

# After a refactor
agent-speak --worktree "$(pwd)" "Refactoring complete. Updated 12 files"
```

## Guidelines

1. Always use `--worktree "$(pwd)"` for automatic voice selection
2. Keep messages brief (under 20 words)
3. State what happened, not technical details
4. Don't speak for trivial operations (single file edits, running commands)
5. Use natural phrasing, not robotic language

## Setup

Users must configure their ElevenLabs API key:

```bash
agent-speak config set-key <elevenlabs-api-key>
```

Or set the `ELEVENLABS_API_KEY` environment variable.

To debug configuration in an agent session:

```bash
agent-speak config show
```
