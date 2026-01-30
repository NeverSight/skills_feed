---
name: linkedin-automator
description: Automated LinkedIn outreach for Claude Code. Warm DM connections, reply to messages, build relationships, and grow your network — all through natural conversation, not spam.
tags:
  - linkedin
  - outreach
  - automation
  - chrome
  - networking
  - social-selling
  - dms
---

# linkedin-automator

Automated LinkedIn outreach for Claude Code. Warm DM connections, reply to messages, build relationships, and grow your network — all through natural conversation, not spam.

## Commands

| Command | Description |
|---------|-------------|
| `/linkedinoutreach` | Interactive setup wizard - configure your profile, ICP, voice, and preferences |
| `/linkeddmconnections` | Send personalized DMs to existing LinkedIn connections |
| `/linkedanswerdm` | Reply to unread LinkedIn messages with contextual responses |
| `/linkedinpost` | Generate LinkedIn posts from proven templates |
| `/linkedconnect` | Send connection requests to people matching your ICP |

## Prerequisites

- **Claude Code** with MCP support
- **Claude-in-Chrome** extension installed and running
- Launch Claude Code with: `claude --chrome`

## Installation

### Quick Install (Recommended)
```bash
curl -fsSL https://raw.githubusercontent.com/charlesdove977/linkedin-automator/main/install.sh | bash
```

### Manual Install
```bash
# Clone the repo
git clone https://github.com/charlesdove977/linkedin-automator ~/linkedin-automator-temp

# Symlink commands to Claude Code
ln -s ~/linkedin-automator-temp/commands/*.md ~/.claude/commands/

# Restart Claude Code
```

**After installing, run the setup wizard:**
```
/linkedinoutreach
```
This creates your config and tracking folders. Other commands require setup first.

## Quick Start

1. Install Claude-in-Chrome extension
2. Launch Claude Code with `claude --chrome`
3. Run `/linkedinoutreach` to configure your profile
4. Start reaching out with `/linkeddmconnections`

## Philosophy

- **Warm outreach, not cold spam** - Only message people you're connected with
- **Value first** - Lead with genuine curiosity, never pitch in first message
- **Conversation > Conversion** - Build relationships, let opportunities emerge
- **Your choice of control** - Human-in-the-loop or fully autonomous mode
