---
name: last30days
description: "Research any topic from the last 30 days across Reddit, X, and web. Uses paid APIs (~$0.03) for real engagement metrics. Use when user asks to research trends, find recommendations, get prompting techniques, or understand what people are discussing. Triggers on: /last30days [topic], research [topic], what's trending, best [X] recommendations."
---

# last30days

Research ANY topic across Reddit, X, and web with real engagement metrics.

## Workflow

### 1. Parse Intent

Extract from user input:
- **TOPIC**: What to research
- **TARGET_TOOL**: Where prompts will be used (if specified)
- **QUERY_TYPE**: RECOMMENDATIONS | NEWS | PROMPTING | GENERAL

### 2. Ask Payment Consent (REQUIRED FIRST ACTION)

**Before any search, use AskUserQuestion:**

```
question: "To search Reddit and X with real engagement metrics, I need to make a small payment (~$0.03). Continue?"
options: ["Yes, make payment", "No, use free web search only"]
```

- User says Yes -> Follow x402 workflow in `references/x402-workflow.md`
- User says No -> Skip to WebSearch only

### 3. Execute Research

**If paid:** Follow `references/x402-workflow.md` then supplement with WebSearch.

**If web-only:** Do WebSearch directly:
- RECOMMENDATIONS: `best {TOPIC} recommendations`, `most popular {TOPIC}`
- NEWS: `{TOPIC} news 2026`, `{TOPIC} announcement`
- PROMPTING: `{TOPIC} prompts examples 2026`
- GENERAL: `{TOPIC} 2026`, `{TOPIC} discussion`

Use user's exact terminology. Exclude reddit.com, x.com (covered by paid APIs).

### 4. Synthesize & Present

See `references/output-patterns.md` for format by query type.

Ask user: "Would you like me to save this research to a markdown file?"
- If yes: Write report to `{TOPIC}-research.md` in current directory

End with invitation: "Share your vision for what you want to create and I'll write a prompt for {TARGET_TOOL}."

### 5. Write Prompts

When user shares vision, write ONE tailored prompt using research insights.
Match the format research recommends (JSON, structured, prose, etc).

---

## Tools

| Tool | Endpoint | Cost |
|------|----------|------|
| Reddit Search | `https://proxy-monetize.fluxapay.xyz/api/openai-api-endpoints/web_search` | ~$0.02 |
| X Search | `https://proxy-monetize.fluxapay.xyz/api/grok-api-call/v1/responses` | ~$0.01 |

Payment workflow: `references/x402-workflow.md`
Error handling: `fluxa-wallet/error-handle.md`
Agent ID setup: `fluxa-wallet/initialize-agent-id.md`
