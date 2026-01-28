---
name: macos-say
description: Use macOS text-to-speech via the `say` command for voice feedback, audio narration, and spoken output.
---

# macOS Say Command

Provide voice feedback using macOS's built-in `say` command.

## Basic Usage
say "Hello, world"

## Key Options
- `-v <voice>` - Select voice (e.g., Samantha, Alex, Daniel)
- `-r <rate>` - Words per minute (default ~175)
- `-o <file>` - Output to audio file
- `-f <file>` - Read text from file

## Common Patterns
say "Task complete" &          # Non-blocking notification
say -v Daniel "Build finished" # Specific voice
say -o out.m4a --data-format=aac "Save as audio"

List voices: say -v ?
