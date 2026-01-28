---
name: clipboard
description: Auto-copy code, commands, and shareable content to system clipboard. Proactively copies paste-worthy output; manually invoke with /copy.
---

# Clipboard

Auto-copy to system clipboard, either proactively or via `/copy`.

## Auto-copy (no prompt needed)

Copy automatically when output is clearly paste-worthy:
- Commit messages, PR descriptions
- Code snippets user asked to "write" or "generate"
- Shell commands, curl, SQL queries (not executed)
- Config files, templates, dotfiles
- Critique/feedback meant for sharing

Append `(Copied to clipboard)` when auto-copying.

## Don't auto-copy

- Explanations, tutorials, answers
- Code already written to files
- Conversation, options, suggestions

## Manual: /copy

- `/copy` - copy last response
- `/copy <text>` - copy specific text

## Platform commands

- macOS: `pbcopy`
- Linux: `xclip -selection clipboard`
- WSL: `clip.exe`

## Example

```
User: Give me a curl to test the webhook
Assistant: curl -X POST https://api.example.com/hook -d '{"test":1}'

(Copied to clipboard)
```
