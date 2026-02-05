---
name: llm-caching
description: Optimize LLM costs and latency through KV caching and prompt caching. Use when (1) structuring prompts for cache hits, (2) configuring API cache_control for Anthropic/Cohere/OpenAI/Gemini, (3) setting up self-hosted inference with vLLM/SGLang/Ollama, (4) building agentic workflows with prefix reuse, (5) designing batch processing pipelines, or (6) understanding cache pricing and tradeoffs.
---

# LLM Caching

Maximize KV cache reuse to reduce costs and latency.

## Core Concept

LLMs compute Key (K) and Value (V) vectors for each token during inference. These encode the model's "understanding" of context. Caching avoids recomputation.

```
Level 1: KV Cache (inference)     - Within one generation, reuse previous tokens' K,V
Level 2: Prompt Cache (API)       - Across requests, persist KV state server-side
Level 3: Prefix Sharing (batch)   - Across users/requests, share common prefixes
```

## The Golden Rule

**Static content first, variable content last.**

```
[System prompt]         <- cacheable, same every request
[Tool definitions]      <- cacheable
[Few-shot examples]     <- cacheable (same order!)
[Reference documents]   <- cacheable if stable
[User message]          <- variable, at the end
```

Cache hits require the **prefix** (beginning) to match exactly. Any difference breaks caching for everything after.

## Prompt Structure Template

```
┌─────────────────────────────────────┐
│  1. System instructions (static)    │  <- cache_control
├─────────────────────────────────────┤
│  2. Tool definitions (static)       │  <- cache_control
├─────────────────────────────────────┤
│  3. Few-shot examples (static)      │  <- cache_control
├─────────────────────────────────────┤
│  4. Documents/context (semi-static) │  <- cache_control if reused
├─────────────────────────────────────┤
│  5. Conversation history (growing)  │  <- cache after N turns
├─────────────────────────────────────┤
│  6. Current user message (variable) │  <- no caching
└─────────────────────────────────────┘
```

## Anti-Patterns

| Anti-Pattern | Why It Breaks Caching |
|--------------|----------------------|
| Variable content early | Prefix changes every request |
| Randomizing few-shot order | Different order = different prefix |
| Timestamps in system prompt | Changes every request |
| User ID in prefix | Per-user cache = no sharing |
| Prompts < minimum threshold | Too small to cache (1024 tokens for Claude) |
| Shuffling tool definitions | Tool order is part of prefix |

## Cost Impact

| Operation | Typical Pricing | Notes |
|-----------|-----------------|-------|
| Cache write | ~1.25x input | One-time, stores KV state |
| Cache read | ~0.1x input | 90% savings on cache hit |
| No caching | 1x input | Full recomputation every time |

**Example:** 50k token system prompt, 100 requests
- Without cache: 50k × 100 × $3/1M = $15.00
- With cache: 50k × $3.75/1M + 50k × 99 × $0.30/1M = $1.67 (**89% savings**)

## Provider References

- **Anthropic Claude** (recommended): [references/claude.md](references/claude.md)
- **Cohere**: [references/cohere.md](references/cohere.md)
- **Self-hosted (vLLM, SGLang, Ollama, HuggingFace)**: [references/self-hosted.md](references/self-hosted.md)
- **OpenAI**: [references/openai.md](references/openai.md)
- **Google Gemini**: [references/gemini.md](references/gemini.md)

## Cookbooks

Practical examples: [references/cookbooks.md](references/cookbooks.md)

| Pattern | Key Insight |
|---------|-------------|
| Web scraping agent | Same tools + system prompt, different URLs |
| RAG pipeline | Cache document chunks, vary queries |
| Multi-turn chat | Growing prefix, cache conversation history |
| Batch processing | Same prompt template, different inputs |
| Agentic tool use | Cache tool definitions + examples |
| Multi-tenant SaaS | Shared base prompt, tenant-specific suffix |
