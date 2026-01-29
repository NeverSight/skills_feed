---
name: ai-model-selector
description: "Use when selecting AI models, configuring API parameters, or implementing LLM calls. Covers OpenAI (GPT-5.2, GPT-5.1, GPT-4.1, o3), Anthropic (Claude 4.5), Google (Gemini 2.5/3), DeepSeek (V3.2, R1), and embedding models with specs, gotchas, and code templates."
user-invocable: true
version: 2.0.0
last_updated: 2026-01-28
license: MIT
author: Jason
compatibility:
  - claude-code
  - cursor
  - codex
  - opencode
tags:
  - llm
  - api
  - openai
  - anthropic
  - gemini
  - deepseek
  - embeddings
  - rag
---

# AI Model Selector Skill

Comprehensive guide to selecting and implementing AI models. Updated January 2026.

## Quick Decision Tree

```
What's your primary need?
│
├─► CODING/AGENTIC TASKS
│   ├─► Best quality → Claude Sonnet 4.5 or GPT-5.2-Codex
│   ├─► Complex reasoning → Claude Opus 4.5 (with effort param)
│   └─► Budget → DeepSeek-chat ($0.28/1M input)
│
├─► REASONING/MATH/SCIENCE
│   ├─► Maximum intelligence → GPT-5.2 Pro or Claude Opus 4.5
│   ├─► Good balance → GPT-5.2 (xhigh effort) or Gemini 2.5 Pro
│   └─► Budget → DeepSeek-reasoner (visible CoT)
│
├─► LONG DOCUMENTS (>200K tokens)
│   ├─► Up to 1M tokens → Claude Sonnet 4.5 (beta) or Gemini 2.5 Pro
│   ├─► Up to 400K → GPT-5.2
│   └─► Budget → DeepSeek-chat (128K)
│
├─► HIGH-VOLUME/LOW-LATENCY
│   ├─► Best speed → Claude Haiku 4.5
│   ├─► Cheapest → Gemini 2.5 Flash-Lite ($0.10/$0.40)
│   └─► Free tier → Gemini via AI Studio
│
├─► EMBEDDINGS/RAG
│   ├─► Best quality → Voyage 3.5 or voyage-3-large
│   ├─► Code-specific → voyage-code-3
│   ├─► Budget → text-embedding-3-small ($0.02/1M)
│   └─► Free → gemini-embedding-001
│
└─► MULTIMODAL (images/audio/video)
    ├─► Images → GPT-4o, Gemini 2.5 Pro/Flash, Claude 4.5
    ├─► Image generation → GPT Image 1, Imagen 4.0
    └─► Video generation → Veo 3.1
```

## Model Quick Reference (January 2026)

### Flagship Models

| Model | Context | Max Output | Input/Output $/1M | Best For |
|-------|---------|------------|-------------------|----------|
| GPT-5.2 | 400K | 128K | $1.75/$14 | Complex reasoning, coding |
| GPT-5.2 Pro | 400K | 128K | $21/$168 | Hardest problems |
| Claude Opus 4.5 | 200K | 64K | $5/$25 | Deep reasoning, agents |
| Claude Sonnet 4.5 | 200K (1M beta) | 64K | $3/$15 | Coding, balanced |
| Gemini 2.5 Pro | 1M | 64K | $1.25/$10 | Long context |
| Gemini 3 Pro | 1M | 64K | $2/$12 | Latest Google (preview) |

### Budget Models

| Model | Context | Input/Output $/1M | Best For |
|-------|---------|-------------------|----------|
| Claude Haiku 4.5 | 200K | $1/$5 | Fast, high-volume |
| Gemini 2.5 Flash | 1M | $0.30/$2.50 | Large-scale processing |
| Gemini 2.5 Flash-Lite | 1M | $0.10/$0.40 | Cheapest cloud option |
| DeepSeek-chat | 128K | $0.28/$0.42 | 10x cheaper than GPT |
| GPT-4o-mini | 128K | $0.15/$0.60 | Simple tasks |

## Critical Gotchas

### ⚠️ GPT-5.x / O-series Don't Support These Parameters:
```javascript
// WRONG - will error on GPT-5.2, o3, o4-mini
{
  temperature: 0.7,      // ❌ Not supported
  top_p: 0.9,            // ❌ Not supported
  max_tokens: 4096,      // ❌ Use max_completion_tokens
}

// CORRECT
{
  reasoning: { effort: "high" },  // none, low, medium, high, xhigh
  text: { verbosity: "medium" },  // low, medium, high
  max_completion_tokens: 4096
}
```

### ⚠️ Claude Opus 4.1 vs 4.5 Pricing
- Opus 4.1: $15/$75 per 1M tokens (legacy pricing)
- Opus 4.5: $5/$25 per 1M tokens (66% cheaper, better quality!)
- **Always use Opus 4.5 for new projects**

### ⚠️ Long Context Premium Pricing (Claude Sonnet)
- ≤200K tokens: $3/$15 per 1M
- >200K tokens: $6/$22.50 per 1M (automatic)

## Detailed Documentation

- [OpenAI Models](./models/openai.md) - GPT-5.2, GPT-5.1, GPT-4.1, o-series
- [Anthropic Models](./models/anthropic.md) - Claude Opus/Sonnet/Haiku 4.5
- [Google Models](./models/google.md) - Gemini 2.5/3 Pro/Flash
- [DeepSeek Models](./models/deepseek.md) - V3.2, R1 (cheapest option)
- [Embedding Models](./models/embeddings.md) - Voyage, OpenAI, Gemini

## Use Case Guides

- [Coding Tasks](./use-cases/coding.md) - Agentic coding, code review
- [Reasoning Tasks](./use-cases/reasoning.md) - Math, science, planning
- [RAG Pipelines](./use-cases/rag.md) - Embeddings, retrieval, generation

## Cost Optimization

### Batch API (50% off)
All major providers offer batch processing for non-urgent tasks:
- OpenAI: 50% off all models
- Anthropic: 50% off all models
- DeepSeek: 33% off

### Prompt Caching
- Claude: 90% savings on cache reads
- OpenAI: 90% savings on cached inputs
- DeepSeek: Automatic caching, 90% off hits

### Model Cascading
Route simple queries to cheap models, complex to expensive:
```
Simple question → Haiku 4.5 ($1/$5)
Complex task → Sonnet 4.5 ($3/$15)
Hardest problems → Opus 4.5 ($5/$25)
```

## API Code Templates

### OpenAI (GPT-5.2)
```javascript
const response = await fetch("https://api.openai.com/v1/responses", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${OPENAI_API_KEY}`,
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    model: "gpt-5.2",
    input: [{ role: "user", content: "Hello" }],
    reasoning: { effort: "medium" }
  })
});
```

### Anthropic (Claude)
```javascript
import Anthropic from '@anthropic-ai/sdk';
const anthropic = new Anthropic();

const response = await anthropic.messages.create({
  model: "claude-sonnet-4-5-20250929",
  max_tokens: 4096,
  messages: [{ role: "user", content: "Hello" }]
});
```

### Google (Gemini)
```javascript
import { GoogleGenerativeAI } from "@google/generative-ai";
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
const model = genAI.getGenerativeModel({ model: "gemini-2.5-flash" });

const result = await model.generateContent("Hello");
```

### DeepSeek (OpenAI-compatible)
```javascript
import OpenAI from 'openai';
const client = new OpenAI({
  baseURL: 'https://api.deepseek.com',
  apiKey: process.env.DEEPSEEK_API_KEY
});

const response = await client.chat.completions.create({
  model: 'deepseek-chat',
  messages: [{ role: 'user', content: 'Hello' }]
});
```

## Benchmark Reference (January 2026)

### SWE-bench Verified (Coding)
1. Claude Opus 4.5: 80.9%
2. GPT-5.1-Codex-Max: 77.9%
3. Claude Sonnet 4.5: 77.2%
4. GPT-5.2-Codex: ~78% (est.)

### AIME 2025 (Math)
1. GPT-5.2 (xhigh): 100%
2. o3: 90%+
3. Claude Opus 4.5: High 80s%
4. DeepSeek R1: 79.8%

### GPQA Diamond (Science)
1. GPT-5.2: ~92-93%
2. Claude Opus 4.5: ~85%+

---

*Last updated: January 28, 2026*
*Sources: Official documentation from OpenAI, Anthropic, Google, DeepSeek*
