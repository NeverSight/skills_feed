---
name: alexa-cli
description: Control Amazon Echo/Alexa devices via the `alexacli` CLI. Use when the user asks to speak/announce on Echo devices, send voice commands to Alexa, control smart home devices, list Alexa devices, or trigger routines.
---

# Alexa CLI

Control Echo devices via the `alexacli` command.

## Requirements

Install from: https://github.com/buddyh/alexa-cli

```bash
brew install buddyh/tap/alexacli
# or
go install github.com/buddyh/alexa-cli/cmd/alexa@latest
```

## Commands

```bash
# List devices
alexacli devices

# Text-to-speech
alexacli speak "Hello" -d Kitchen             # Specific device
alexacli speak "Dinner is ready!" --announce  # ALL devices

# Voice commands (smart home, music, etc.)
alexacli command "turn off the lights" -d Kitchen
alexacli command "set thermostat to 72" -d Kitchen
alexacli command "play jazz" -d "Living Room"
alexacli command "set timer 10 minutes" -d Office

# Ask and get response back
alexacli ask "what's the temperature" -d Kitchen
alexacli ask "what's on my calendar" -d Kitchen

# History
alexacli history
alexacli history --limit 5

# Routines (WIP)
alexacli routine list
alexacli routine run "Good Night"

# Smart home direct control (WIP)
alexacli sh list
alexacli sh on "Kitchen Light"
alexacli sh off "All Lights"
```

## JSON Output

All commands support `--json`:

```bash
alexacli devices --json
alexacli ask "what time is it" -d Kitchen --json
```

## Notes

- Device names support partial, case-insensitive matching
- `command` is preferred for smart home - natural language is more flexible
- `ask` retrieves Alexa's actual response (useful for queries)
- Uses unofficial Amazon API (same as Alexa app)
