---
name: using-generic-agents
description: Use to decide what kind of generic agent you should use
user-invocable: false
---

**CRITICAL:** Your operator's direction supercedes these directions. If the operator specifies a type of agent, execute their task with that agent.

## Model Characteristics

**Haiku:** Excellent at following specific, detailed instructions. Poor at making its own decisions. Give it a clear prompt and it executes well; ask it to figure things out and it struggles. Be detailed.

**Sonnet:** Capable of making decisions but gets off-track easily. Will explain concepts, describe structures, and gather extraneous information when you just want it to do the thing, so guard against this when prompting the agent.

**Opus:** Stays on-track through complex tasks. Better judgment, fewer loops. Expensive—don't use for clearly-definable workflows where Sonnet/Haiku would suffice.

## When to Use Each

Use `haiku-general-purpose` for:
- Well-defined tasks with detailed prompts
- High-volume parallel workflows (cost matters)
- Simple execution where speed > quality

Use `sonnet-general-purpose` for:
- Multi-file reasoning and debugging
- Tasks requiring some judgment
- Daily coding work (80-90% of tasks)

Use `opus-general-purpose` for:
- Tasks requiring sustained focus and judgment
- When Sonnet keeps wandering or looping
- Complex analysis where staying on-track matters
- High-stakes decisions needing nuance
