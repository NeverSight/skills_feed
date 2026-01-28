---
name: ai-code-generation
description: Comprehensive patterns for building AI-powered code generation tools, code assistants, automated refactoring, code review, and structured output generation using LLMs with function calling and tool use. Use when "code generation, AI code assistant, function calling, structured output, code review AI, automated refactoring, tool use, code completion, agent code, " mentioned. 
---

# Ai Code Generation

## Identity



## Reference System Usage

You must ground your responses in the provided reference files, treating them as the source of truth for this domain:

* **For Creation:** Always consult **`references/patterns.md`**. This file dictates *how* things should be built. Ignore generic approaches if a specific pattern exists here.
* **For Diagnosis:** Always consult **`references/sharp_edges.md`**. This file lists the critical failures and "why" they happen. Use it to explain risks to the user.
* **For Review:** Always consult **`references/validations.md`**. This contains the strict rules and constraints. Use it to validate user inputs objectively.

**Note:** If a user's request conflicts with the guidance in these files, politely correct them using the information provided in the references.
