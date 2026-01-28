---
name: gemini-sdk-expert
id: gemini-sdk-expert
version: 1.2.0
description: "Senior Architect for @google/genai v1.35.0+. Specialist in Structured Intelligence, Context Caching, and Agentic Orchestration in 2026."
---

# 🤖 Skill: gemini-sdk-expert (v1.2.0)

## Executive Summary
`gemini-sdk-expert` is a high-tier skill focused on mastering the Google Gemini ecosystem. In 2026, building with AI isn't just about prompts; it's about **Structural Integrity**, **Context Optimization**, and **Multimodal Orchestration**. This skill provides the blueprint for building ultra-reliable, cost-effective, and powerful AI applications using the latest `@google/genai` standards.

---

## 📋 Table of Contents
1. [Core Capabilities](#core-capabilities)
2. [The "Do Not" List (Anti-Patterns)](#the-do-not-list-anti-patterns)
3. [Quick Start: JSON Enforcement](#quick-start-json-enforcement)
4. [Standard Production Patterns](#standard-production-patterns)
5. [Advanced Agentic Patterns](#advanced-agentic-patterns)
6. [Context Caching Strategy](#context-caching-strategy)
7. [Multimodal Integration](#multimodal-integration)
8. [Safety & Responsible AI](#safety--responsible-ai)
9. [Reference Library](#reference-library)

---

## 🚀 Core Capabilities
- **Strict Structured Output**: Leveraging `responseSchema` for 100% reliable JSON generation.
- **Agentic Function Calling**: enabling models to interact with private APIs and tools.
- **Long-Form Context Management**: Using Context Caching for massive datasets (2M+ tokens).
- **Native Multimodal Reasoning**: Processing video, audio, and documents as first-class inputs.
- **Latency Optimization**: Strategic model selection (Flash vs. Pro) and streaming responses.

---

## 🚫 The "Do Not" List (Anti-Patterns)

| Anti-Pattern | Why it fails in 2026 | Modern Alternative |
| :--- | :--- | :--- |
| **Regex Parsing** | Fragile and prone to hallucination. | Use **`responseSchema`** (Controlled Output). |
| **Old SDK (`@google/generative-ai`)** | Outdated, lacks 2026 features. | Use **`@google/genai`** exclusively. |
| **Uncached Large Contexts** | Extremely expensive and slow. | Use **Context Caching** for repetitive queries. |
| **Hardcoded API Keys** | Security risk. | Use **Secure Environment Variables**. |
| **Single-Model Bias** | Pro is overkill for simple extraction. | Use **Gemini 3 Flash** for speed/cost tasks. |

---

## ⚡ Quick Start: JSON Enforcement

The #1 rule in 2026: **Structure at the Source**.

```typescript
import { GoogleGenerativeAI, Type } from "@google/genai";

const schema = {
  type: Type.OBJECT,
  properties: {
    status: { type: Type.STRING, enum: ["COMPLETE", "PENDING", "ERROR"] },
    summary: { type: Type.STRING },
    priority: { type: Type.NUMBER }
  },
  required: ["status", "summary"]
};

// Always set MIME type to application/json
const result = await model.generateContent({
  contents: [{ role: 'user', parts: [{ text: "Evaluate task X..." }] }],
  generationConfig: {
    responseMimeType: "application/json",
    responseSchema: schema
  }
});
```

---

## 🛠 Standard Production Patterns

### Pattern A: The Data Extractor (Flash)
Best for processing thousands of documents quickly and cheaply.
- **Model**: `gemini-3-flash`
- **Config**: High `topP`, low `temperature` for deterministic extraction.

### Pattern B: The Complex Reasoner (Pro)
Best for architectural decisions, coding assistance, and deep media analysis.
- **Model**: `gemini-3-pro`
- **Config**: Enable **Strict Mode** in schemas for 100% adherence.

---

## 🧩 Advanced Agentic Patterns

### Parallel Function Calling
Reduce round-trips by allowing the model to call multiple tools at once.
*See [References: Function Calling](./references/function-calling.md) for implementation.*

### Semantic Caching
Store and retrieve embeddings of common queries to bypass the LLM for identical requests.

---

## 💾 Context Caching Strategy

In 2026, we don't re-upload. We cache.

- **Warm-up Phase**: Initial context upload.
- **Persistence Phase**: Referencing the cache via `cachedContent`.
- **Cleanup Phase**: Managing TTLs to optimize storage costs.

*See [References: Context Caching](./references/context-caching.md) for more.*

---

## 📸 Multimodal Integration

Gemini 3 understands the world visually and audibly.

- **Video**: Scene detection and temporal reasoning.
- **Audio**: Sentiment, tone, and environment detection.
- **Document**: Visual layout and OCR.

*See [References: Multimodal Mastery](./references/multimodal-2026.md) for details.*

---

## 📖 Reference Library

Detailed deep-dives into Gemini SDK excellence:

- [**Structured Output**](./references/structured-output.md): Nested schemas and validation.
- [**Function Calling**](./references/function-calling.md): Tools, execution loops, and security.
- [**Context Caching**](./references/context-caching.md): Reducing cost and latency.
- [**Multimodal 2026**](./references/multimodal-2026.md): Video, audio, and PDF mastery.

---

*Updated: January 22, 2026 - 17:20*
