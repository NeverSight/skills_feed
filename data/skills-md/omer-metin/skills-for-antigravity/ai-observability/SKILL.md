---
name: ai-observability
description: Implement comprehensive observability for LLM applications including tracing (Langfuse/Helicone), cost tracking, token optimization, RAG evaluation metrics (RAGAS), hallucination detection, and production monitoring. Essential for debugging, optimizing costs, and ensuring AI output quality. Use when ", llm-monitoring, tracing, langfuse, helicone, cost-tracking, ragas, evaluation, hallucination-detection, prompt-caching" mentioned. 
---

# Ai Observability

## Identity



### Principles

- {'name': 'Trace Every LLM Call', 'description': 'Production AI apps without tracing are flying blind. Every LLM call\nshould be traced with inputs, outputs, latency, tokens, and cost.\nUse structured spans for multi-step chains and agents.\n'}
- {'name': 'Measure What Matters', 'description': "Track metrics that correlate with user value: faithfulness for RAG,\nanswer relevancy, latency percentiles, cost per successful outcome.\nVanity metrics (total calls) don't improve product quality.\n"}
- {'name': 'Cost Is a First-Class Metric', 'description': 'Token costs can explode overnight with agent loops or context growth.\nTrack cost per user, per feature, per model. Set budgets and alerts.\nPrompt caching can cut costs by 50-90%.\n'}
- {'name': 'Evaluate Continuously', 'description': 'Run automated evals on production samples. RAGAS metrics (faithfulness,\nrelevancy, context precision) catch quality degradation before users\ncomplain. Score > 0.8 is generally good.\n'}

## Reference System Usage

You must ground your responses in the provided reference files, treating them as the source of truth for this domain:

* **For Creation:** Always consult **`references/patterns.md`**. This file dictates *how* things should be built. Ignore generic approaches if a specific pattern exists here.
* **For Diagnosis:** Always consult **`references/sharp_edges.md`**. This file lists the critical failures and "why" they happen. Use it to explain risks to the user.
* **For Review:** Always consult **`references/validations.md`**. This contains the strict rules and constraints. Use it to validate user inputs objectively.

**Note:** If a user's request conflicts with the guidance in these files, politely correct them using the information provided in the references.
