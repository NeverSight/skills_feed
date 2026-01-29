---
name: prompting
description: Prompt engineering guidance for writing and improving LLM prompts. Use when asked to (1) write a prompt for a specific task, (2) review or improve an existing prompt, (3) design system prompts for AI assistants, (4) structure prompts for specific output formats (JSON, XML, markdown), or (5) apply prompt engineering techniques like few-shot, chain-of-thought, or role prompting.
---

# Prompt Engineering

Guide for crafting effective prompts for large language models (Claude, GPT, Gemini, Llama, etc.).

## Workflow

1. **Clarify the goal**: What task should the prompt accomplish?
2. **Choose techniques**: Select from references/techniques.md
3. **Structure the prompt**: Apply appropriate format
4. **Add constraints**: Specify requirements and boundaries
5. **Test and refine**: Iterate based on outputs

## Writing a New Prompt

Start with this template:

```
[Context/Role - optional]
[Task - required]
[Constraints/Requirements - as needed]
[Output format - as needed]
[Examples - for complex tasks]
```

**Minimal prompt** (simple tasks):
```
Summarize this article in 3 bullet points.
```

**Structured prompt** (complex tasks):
```
You are a senior code reviewer.

Review this code for:
- Security vulnerabilities
- Performance issues
- Maintainability concerns

Format your response as:
## Summary
[1-2 sentences]

## Issues
- [severity]: [description]

## Recommendations
[prioritized list]
```

## Improving an Existing Prompt

Diagnose issues:

| Problem | Solution |
|---------|----------|
| Output too vague | Add specific constraints or examples |
| Wrong format | Specify output structure explicitly |
| Missing details | Use chain-of-thought or decomposition |
| Inconsistent results | Add few-shot examples |
| Off-topic responses | Strengthen role/context framing |

**Improvement checklist**:
- Is the task clear and unambiguous?
- Are constraints specific (not "be concise" but "under 100 words")?
- Does output format match intended use?
- Would examples clarify expectations?

## Quick Reference: Techniques

| Technique | When to Use |
|-----------|-------------|
| Few-shot | Specific format/style needed |
| Chain-of-thought | Complex reasoning, math, analysis |
| Role prompting | Domain expertise, specific tone |
| Task decomposition | Multi-step workflows |
| Constraints | Precise requirements |

See [references/techniques.md](references/techniques.md) for detailed patterns and examples.

## Quick Reference: Output Formats

| Format | When to Use |
|--------|-------------|
| XML tags | Complex prompts, clear section boundaries |
| JSON | Programmatic parsing, structured data |
| Markdown | Human-readable reports, documentation |

See [references/structured.md](references/structured.md) for format patterns.

## System Prompts

For designing AI assistant behavior, see [references/system-prompts.md](references/system-prompts.md).

Key sections:
- Identity and role definition
- Behavioral guidelines
- Constraints and boundaries
- Output format defaults
