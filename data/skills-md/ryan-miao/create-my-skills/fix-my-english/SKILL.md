---
name: fix-my-english
description: Fix English grammar and translate to Chinese. Always invoke when user's message starts with "fme" or "fix my en".
---

# Fix My English

Trigger: Message starts with `fme` or `fix my en`

## Workflow

1. Remove the prefix (`fme ` or `fix my en `)
2. Correct grammar/vocabulary errors
3. Output in this format:

```markdown
---
你想说: [Chinese translation]

错误: "[original]" → "[corrected]"
---
```

## Examples

| Input | Output |
|-------|--------|
| `fme i want add button` | `你想说: 我想添加一个按钮\n\n错误: "i want add button" → "I want to add a button"` |
| `fix my en thanks for help` | `你想说: 谢谢你的帮助\n\n错误: "thanks for help" → "thanks for helping"` |
