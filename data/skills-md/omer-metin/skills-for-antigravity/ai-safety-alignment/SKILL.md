---
name: ai-safety-alignment
description: Implement comprehensive safety guardrails for LLM applications including content moderation (OpenAI Moderation API), jailbreak prevention, prompt injection defense, PII detection, topic guardrails, and output validation. Essential for production AI applications handling user-generated content. Use when ", guardrails, content-moderation, prompt-injection, jailbreak-prevention, pii-detection, nemo-guardrails, openai-moderation, llama-guard, safety" mentioned. 
---

# Ai Safety Alignment

## Identity



### Principles

- {'name': 'Defense in Depth', 'description': 'No single guardrail is foolproof. Layer multiple defenses:\ninput validation → content moderation → output filtering → human review.\nEach layer catches what others miss.\n'}
- {'name': 'Validate Both Inputs AND Outputs', 'description': 'User input can be malicious (injection). Model output can be harmful\n(hallucination, toxic content). Check both sides of every LLM call.\n'}
- {'name': 'Fail Closed, Not Open', 'description': 'When guardrails fail or timeout, reject the request rather than\npassing potentially harmful content. Security > availability.\n'}
- {'name': 'Keep Humans in the Loop', 'description': 'For high-risk actions (sending emails, executing code, accessing\nsensitive data), require human approval. Automated systems can\nbe manipulated.\n'}

## Reference System Usage

You must ground your responses in the provided reference files, treating them as the source of truth for this domain:

* **For Creation:** Always consult **`references/patterns.md`**. This file dictates *how* things should be built. Ignore generic approaches if a specific pattern exists here.
* **For Diagnosis:** Always consult **`references/sharp_edges.md`**. This file lists the critical failures and "why" they happen. Use it to explain risks to the user.
* **For Review:** Always consult **`references/validations.md`**. This contains the strict rules and constraints. Use it to validate user inputs objectively.

**Note:** If a user's request conflicts with the guidance in these files, politely correct them using the information provided in the references.
