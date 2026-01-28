---
name: gemini
description: Interact with Google's Gemini model via CLI. Use when needing a second opinion from another LLM, cross-validation, or leveraging Gemini's Google Search grounding. Supports multi-turn conversations with session management.
---

# Gemini CLI

## Commands

### New conversation (ask)

```bash
gemini --model auto "your prompt here" --output-format json 2>/dev/null
```

Response includes `session_id` for follow-up:
```json
{
  "session_id": "uuid-here",
  "response": "...",
  "stats": {...}
}
```

### Continue conversation (reply)

```bash
gemini --model auto --resume <session_id> -p "follow-up prompt" --output-format json 2>/dev/null
```

Context from previous turns is preserved.

## Examples

```bash
# Ask Gemini for code review
result=$(gemini --model auto "Review this function for potential bugs: $(cat src/utils.ts)" --output-format json 2>/dev/null)
session_id=$(echo "$result" | jq -r '.session_id')
echo "$result" | jq -r '.response'

# Follow up on the same session (using session_id from above)
result=$(gemini --model auto --resume "$session_id" -p "How would you refactor it?" --output-format json 2>/dev/null)
session_id=$(echo "$result" | jq -r '.session_id')
echo "$result" | jq -r '.response'

# Leverage Google Search grounding
result=$(gemini --model auto "What are the latest changes in TypeScript 5.8?" --output-format json 2>/dev/null)
echo "$result" | jq -r '.response'
```

## ⚠️ CRITICAL: Session ID Handling

**If you don't parse `session_id`, you CANNOT continue the conversation!**

For every response, you MUST:
1. Extract `session_id` from the JSON response
2. Use `--resume <session_id>` for follow-up questions

❌ WRONG:
```bash
gemini "prompt" --output-format json 2>/dev/null | jq -r '.response'
# session_id lost → cannot continue conversation
```

✅ CORRECT:
```bash
result=$(gemini --model auto "prompt" --output-format json 2>/dev/null)
session_id=$(echo "$result" | jq -r '.session_id')
response=$(echo "$result" | jq -r '.response')
# session_id preserved for follow-up
```

## Notes

- Gemini automatically uses `google_web_search` when needed
- Image analysis: include file path in prompt, Gemini reads via `read_file`
