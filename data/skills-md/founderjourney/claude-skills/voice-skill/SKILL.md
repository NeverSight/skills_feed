---
name: voice-skill
description: Voice conversations with Claude Opus 4.5 about your code projects. Receive calls from Claude or call Claude to discuss problems, brainstorm, and get code reviews.
original_source: https://github.com/abracadabra50/claude-code-voice-skill
author: abracadabra50
license: MIT
---

# Voice Skill - Talk to Claude About Your Code

Enable voice conversations with Claude Opus 4.5 about your projects. Have Claude call you or call Claude directly to discuss problems, brainstorm ideas, and get real-time code reviews.

## When to Use This Skill

- Discussing complex code problems hands-free
- Brainstorming architecture decisions
- Getting verbal code reviews
- Explaining code while walking/commuting
- Pair programming via voice
- Quick questions without typing

## How It Works

1. **Claude Calls You**: Initiate outbound calls from Claude
2. **You Call Claude**: Call your Vapi number to reach Claude
3. **Live Context**: Claude has access to your project during calls
4. **Transcripts**: All calls automatically saved as markdown

## Setup

### Prerequisites
- Vapi account with API key
- Phone number (~$2/month)
- Node.js (for localtunnel)
- Python 3.8+

### 1. Install
```bash
pip install claude-code-voice-skill
```

### 2. Setup Credentials
```bash
voice-skill setup
```
Prompts for:
- Vapi API key
- Your phone number
- Your name (for personalized greetings)

### 3. Register Project
```bash
cd /path/to/your/project
voice-skill register
```
Captures project snapshot for context.

### 4. Start Service
```bash
voice-skill start
```
Launches server and tunnel.

## Commands

### Have Claude Call You
```bash
voice-skill call
```
Claude calls your registered number and greets you by name.

### Check Status
```bash
voice-skill status
```
Shows service status and active sessions.

### Update Name
```bash
voice-skill config name "Your Name"
```

### View Transcripts
```bash
ls ~/.voice-skill/transcripts/
```

## What Claude Can Do During Calls

### Read Files
"Claude, what's in the main.py file?"
→ Claude reads and explains the file

### Search Code
"Can you find where we handle authentication?"
→ Claude searches and reports findings

### Check Git Status
"What files have I changed today?"
→ Claude reports git diff summary

### Review Code
"Review the changes I made to the API module"
→ Claude provides verbal code review

### Brainstorm
"I need to add caching - what approaches should I consider?"
→ Claude discusses options with pros/cons

## Example Conversation

```
[Phone rings]

Claude: "Hey Alex! I see you're working on the user-service
project. What would you like to discuss?"

You: "I'm having trouble with the authentication middleware.
Can you take a look at auth.py?"

Claude: "Sure, let me read that... I see you're using JWT
tokens. The issue might be on line 45 where you're checking
the expiry. You're comparing timestamps in different formats..."

You: "Oh, that makes sense. What's the fix?"

Claude: "You should convert both to Unix timestamps before
comparing. I'd suggest using datetime.timestamp() on line 45..."
```

## Transcripts

Calls are automatically transcribed and saved:

```markdown
# Call Transcript - 2025-01-12 10:30 AM

**Project:** user-service
**Duration:** 8 minutes

## Summary
Discussed JWT authentication bug in auth.py.
Identified timestamp comparison issue on line 45.

## Full Transcript

**Claude:** Hey Alex! I see you're working on...
**You:** I'm having trouble with...
...
```

## Configuration

### Config File Location
```
~/.voice-skill/config.yaml
```

### Options
```yaml
user:
  name: "Your Name"
  phone: "+1234567890"

vapi:
  api_key: "your-key"
  phone_number: "+1987654321"

preferences:
  greeting_style: casual  # casual, professional
  auto_transcript: true
  transcript_dir: ~/.voice-skill/transcripts
```

## Voice Provider Options

The skill supports different voice providers:
- Default Vapi voices
- ElevenLabs integration
- Custom voice configurations

## Security

- API keys stored locally
- Calls encrypted via Vapi
- Transcripts stored locally only
- No data sent to third parties (beyond Vapi)

## Troubleshooting

### "Connection failed"
- Check internet connection
- Verify Vapi API key
- Restart with `voice-skill start`

### "Project not found"
- Run `voice-skill register` in project directory

### "Call not connecting"
- Verify phone number format (+country code)
- Check Vapi account balance

## Use Cases

- **Code Reviews**: Verbal feedback while looking at code
- **Debugging**: Talk through problems out loud
- **Architecture**: Discuss design decisions
- **Learning**: Explain code concepts
- **Accessibility**: Hands-free coding assistance

## Credits

Created by [abracadabra50](https://github.com/abracadabra50/claude-code-voice-skill). Licensed under MIT.
