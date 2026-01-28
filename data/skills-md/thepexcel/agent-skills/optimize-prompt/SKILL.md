---
name: optimize-prompt
description: Prompt optimization consultant for AI system prompts and custom instructions. Supports Claude API, OpenAI API, Gemini API, CLAUDE.md, ChatGPT, and n8n. Use when user wants to improve, review, or create prompts, system instructions, or custom instructions for any AI platform.
---

# Prompt Optimization Consultant

Expert consultant for optimizing AI prompts across platforms. **Asks first, optimizes second.**

## Consultant Workflow

```
DISCOVER → DIAGNOSE → OPTIMIZE → VALIDATE
```

### Phase 1: DISCOVER (Always First)

**Before touching any prompt, ask these questions:**

| Question | Why It Matters |
|----------|----------------|
| **Platform?** | Claude API / OpenAI API / Gemini API / CLAUDE.md / ChatGPT / n8n | Format differs by platform |
| **Model?** | Opus / Sonnet / Haiku / GPT-4o / GPT-5 / Gemini | Model-specific clauses needed |
| **Prompt type?** | System prompt / User prompt / Both | Different optimization strategies |
| **Goal?** | What should the AI do? | Informs structure and examples |
| **Current issues?** | What's not working? | Prioritizes fixes |

**Skip discovery only if:** User provides all context upfront OR says "just optimize it."

### Phase 2: DIAGNOSE

Score against platform-appropriate criteria (see [checklist.md](references/checklist.md)).

### Phase 3: OPTIMIZE

Apply platform-specific techniques. Show before/after for each change.

### Phase 4: VALIDATE

Verify no conflicting instructions and structure is coherent.

---

## Quick Reference

### System Prompt vs User Prompt

| Put in System Prompt | Put in User Prompt |
|----------------------|-------------------|
| Role/persona | Specific task |
| Persistent behavior | Dynamic content |
| Output format | User's actual input |
| Boundaries & rules | Task-specific context |
| Tool usage guidelines | Current session info |

**Rule:** Consistency across sessions → System. Specific to this interaction → User.

### Platform Quick Guide

| Platform | Key Optimization |
|----------|------------------|
| **Claude API** | XML tags, anti-over-engineering clause, tools in API field |
| **OpenAI API** | Message roles, pin model version, tools in tools field |
| **Gemini API** | Critical instructions at END, temp=1.0, knowledge cutoff |
| **CLAUDE.md** | Inline content, 150-200 instructions, no progressive disclosure |
| **ChatGPT** | Markdown, Memory integration, 1500 char limit |
| **n8n** | Dynamic variables `{{ $now }}`, clear tool naming, memory node |

### Model-Specific Additions

| Model | Required Addition |
|-------|-------------------|
| **Claude Opus 4.5** | Anti-over-engineering clause (mandatory) |
| **Claude Haiku** | More examples (3-5), numbered steps |
| **OpenAI GPT** | Explicit verbosity control |
| **Gemini** | Grounding clause if using context |

---

## Core Techniques

### 1. Structure by Platform

**Claude (API & CLAUDE.md):** XML tags
```xml
<context>Role and project</context>
<instructions>What to do</instructions>
<examples>Concrete examples</examples>
```

**OpenAI/ChatGPT:** Markdown with clear sections
```markdown
## Role
You are a helpful assistant...

## Instructions
1. Always...
2. Never...
```

**Gemini:** XML or Markdown (pick one, don't mix)
- Place critical instructions at END for long context

### 2. Instruction Hierarchy

| Priority | Marker | Use For |
|----------|--------|---------|
| 1st | CRITICAL | Security, data loss prevention |
| 2nd | IMPORTANT | Quality-affecting rules |
| 3rd | Regular | Normal instructions |

**Max 2-3 CRITICAL items.** If everything is critical, nothing is.

### 3. Anti-Over-Engineering (Opus Required)

```markdown
Avoid over-engineering. Only make changes that are directly requested.
Keep solutions simple and focused. Don't add features beyond what was asked.
Don't create abstractions for one-time operations.
```

### 4. Examples (3-5 Diverse)

```markdown
<example>
User: "Add caching"
Bad: "Adding Redis..."
Good: "What's the bottleneck? Let me profile first."
</example>
```

### 5. Tables Over Paragraphs

```markdown
| Tool | Purpose | Flag |
|------|---------|------|
| sql_query.py | Query | --schema |
| sql_write.py | Update | --save |
```

---

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| Vague instructions | Replace with specific steps |
| Everything is CRITICAL | Max 2-3 truly critical items |
| No examples | Add 3-5 concrete examples |
| Explaining basics | Trust the model knows |
| Wrong format for platform | Match platform conventions |
| System/User confusion | Separate by persistence vs task-specific |

---

## Output Format

```markdown
## Discovery Summary
- Platform: [X]
- Model: [X]
- Type: [System/User/Both]
- Goal: [X]
- Issues: [X]

## Score: [X/100]

## Issues Found
1. **[Issue]** (Priority: High/Medium/Low)
   - Current: `[snippet]`
   - Problem: [why]
   - Fix: `[improved]`

## Optimized Prompt
[Full optimized version]

## Changes Made
- [bullet list]
```

---

## References

| Reference | Use For |
|-----------|---------|
| [platforms.md](references/platforms.md) | Platform-specific deep dive |
| [system-vs-user.md](references/system-vs-user.md) | System/User prompt guidance |
| [techniques.md](references/techniques.md) | Core optimization techniques |
| [checklist.md](references/checklist.md) | Scoring checklist by platform |
| [model-comparison.md](references/model-comparison.md) | Model-specific behaviors |
