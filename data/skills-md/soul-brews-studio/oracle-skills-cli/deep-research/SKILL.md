---
name: deep-research
description: Deep Research via Gemini. Use when user says "deep research", "research this topic", or needs comprehensive analysis with sources.
alias: /gemini research
---

# /deep-research

**Alias for `/gemini research`** - Deep Research automation via Gemini.

Opens new tab, selects Deep Research mode, sends prompt, and starts research.

## Usage

```bash
/deep-research <topic>
```

## Examples

```bash
/deep-research compare yeast S-33 vs T-58
/deep-research best practices for brewing Belgian ales
/deep-research React Server Components vs traditional SSR
```

## Workflow

1. Create new Gemini tab
2. Select Deep Research mode (Tools → Deep Research)
3. Send research prompt
4. Click "Start research" button
5. Wait for results

## Script

The automation script handles the full flow:

```bash
bun ~/.claude/skills/deep-research/scripts/deep-research.ts "<topic>"
```

## Requirements

- MQTT broker running (`mosquitto`)
- Claude Browser Proxy extension installed and connected (v2.9.39+)
- Gemini tab access

## MQTT Commands Used

| Step | Action | Command |
|------|--------|---------|
| 1 | New tab | `create_tab` with gemini.google.com |
| 2 | Select mode | `select_mode` → Deep Research |
| 3 | Send prompt | `chat` with research topic |
| 4 | Start | `clickText` → "Start research" |
