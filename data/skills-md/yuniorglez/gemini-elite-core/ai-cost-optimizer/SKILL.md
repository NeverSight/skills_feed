---
name: ai-cost-optimizer
id: ai-cost-optimizer
version: 1.1.0
description: "Master of LLM Economic Orchestration, specialized in Google GenAI (Gemini 3), Context Caching, and High-Fidelity Token Engineering."
last_updated: "2026-01-22"
---

# Skill: AI Cost Optimizer (Standard 2026)

**Role:** The AI Cost Optimizer is a specialized "Token Economist" responsible for maximizing the reasoning output of AI agents while minimizing the operational expense. In 2026, this role masters the pricing tiers of Gemini 3 Flash and Lite models, implementing "Thinking-Level" routing and multi-layered caching to achieve up to 90% cost reduction on high-volume apps.

## 🎯 Primary Objectives
1.  **Economic Orchestration:** Dynamically routing prompts between Gemini 3 Pro, Flash, and Lite based on complexity.
2.  **Context Caching Mastery:** Implementing implicit and explicit caching for system instructions and long documents (v1.35.0+).
3.  **Token Engineering:** Reducing "Noise tokens" through XML-tagging and strict response schemas.
4.  **Usage Governance:** Implementing granular quotas and attribution to prevent runaway API billing.

---

## 🏗️ The 2026 Economic Stack

### 1. Target Models
- **Gemini 3 Pro:** Reserved for "Mission Critical" reasoning and deep architecture mapping.
- **Gemini 3 Flash-Preview:** The "Workhorse" for most coding and extraction tasks ($0.50/1M input).
- **Gemini Flash-Lite-Latest:** The "Utility" agent for real-time validation and short-burst responses.

### 2. Optimization Tools
- **Google GenAI Context Caching:** Reducing input fees for stable context blocks.
- **Thinking Level Param:** Controlling reasoning depth for cost/latency trade-offs.
- **Prompt Registry:** Deduplicating and optimizing recurring system instructions.

---

## 🛠️ Implementation Patterns

### 1. The "Thinking Level" Router
Adjusting the model's internal reasoning effort based on the task type.

```typescript
// 2026 Pattern: Cost-Aware Generation
const model = genAI.getGenerativeModel({
  model: "gemini-3-flash",
  generationConfig: {
    thinkingLevel: taskComplexity === 'high' ? 'standard' : 'low',
    responseMimeType: "application/json",
  }
});
```

### 2. Explicit Context Caching (v1.35.0+)
Crucial for large codebases or stable documentation.

```typescript
// Squaads Standard: 1M+ token repository caching
const codebaseCache = await cacheManager.create({
  model: "gemini-flash-lite-latest", 
  contents: [{ role: "user", parts: [{ text: fullRepoData }] }],
  ttlSeconds: 86400, // Cache for 24 hours
});

// Subsequent calls use cachedContent to avoid full re-billing
const result = await model.generateContent({
  cachedContent: codebaseCache.name,
  contents: [{ role: "user", parts: [{ text: "Explain the auth flow." }] }],
});
```

### 3. XML System Instruction Packing
Using XML tags to reduce instruction drift and token wastage in multi-turn chats.

```xml
<system_instruction>
  <role>Senior Architect</role>
  <constraints>No legacy PHP, use Property Hooks</constraints>
</system_instruction>
```

---

## 🚫 The "Do Not List" (Anti-Patterns)
1.  **NEVER** send a full codebase in every prompt. Use **Repomix** for pruning and **Context Caching** for reuse.
2.  **NEVER** use high-resolution video frames (280 tokens) for tasks that only need low-res (70 tokens).
3.  **NEVER** default to Gemini 3 Pro. Always start with Flash-Lite and escalate only if validation fails.
4.  **NEVER** allow agents to run in an infinite loop without a "Kill Switch" based on token accumulation.

---

## 🛠️ Troubleshooting & Usage Audit

| Issue | Likely Cause | 2026 Corrective Action |
| :--- | :--- | :--- |
| **Billing Spikes** | Unoptimized multimodal input | Downsample images/video before sending to the model. |
| **Low Quality (Lite)** | Insufficient reasoning depth | Switch `thinkingLevel` to standard or route to Flash-Preview. |
| **Cache Misses** | Context drift in dynamic files | Isolate stable imports/types from volatile business logic. |
| **Hallucination** | Instruction drift in long context | Use `<system>` tags and explicit "Do Not" lists. |

---

## 📚 Reference Library
- **[Model Selection Matrix](./references/1-model-selection-matrix.md):** Choosing the right model for the job.
- **[Advanced Caching](./references/2-advanced-caching.md):** Mastering TTL and cache warming.
- **[Monitoring & Governance](./references/3-monitoring-and-governance.md):** Tools for tracking ROI.

---

## 📊 Economic Metrics
- **Cost per Feature:** < $0.05 (Target for Squaads agents).
- **Token Efficiency:** > 80% (Knowledge vs Boilerplate).
- **Cache Hit Rate:** > 75% for codebase queries.

---

## 🔄 Evolution of AI Pricing
- **2023:** Fixed per-token pricing (Prohibitive for large context).
- **2024:** First-gen Context Caching (Pro-only).
- **2025-2026:** Ubiquitous Caching and "Reasoning-on-Demand" (Thinking Level parameters).

---

**End of AI Cost Optimizer Standard (v1.1.0)**

*Updated: January 22, 2026 - 23:45*
