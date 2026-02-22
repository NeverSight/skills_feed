---
name: prompt-generator
description: Meta-prompting skill that creates well-structured, verifiable, low-hallucination prompts for any use case. Use when the user wants to create, refine, or improve a prompt — including system prompts, role prompts, task prompts, or any AI instruction set. Triggers on requests like "create a prompt for...", "help me write a prompt", "refine this prompt", "make a better prompt for...", or "generate a prompt that...".
---

# Prompt Generator

Create high-quality, structured prompts using meta-prompting best practices: task decomposition, expert personas, iterative verification, and hallucination minimization.

## Workflow

### Phase 1: Gather Requirements

Ask the user (one at a time, maximum 3 questions):

1. **Goal**: "What is the primary goal or role of the system you want to create?"
2. **Output**: "What specific outputs do you expect? (format, length, style)"
3. **Accuracy**: "How should it handle uncertainty? (disclaim, ask for sources, or best-effort)"

Skip questions when answers are obvious from context. Minimize friction.

### Phase 2: Decompose (if complex)

For complex requests, break into subtasks and assign expert personas:

- **Expert Writer** — for copywriting, narrative, tone
- **Expert Analyst** — for data, logic, verification
- **Expert Python** — for code generation, computation
- **Expert [Domain]** — for specialized knowledge

Each expert gets complete, self-contained instructions (no shared memory between experts).

Use "fresh eyes" — never assign the same expert to both create AND validate.

### Phase 3: Generate the Prompt

Consolidate into a single, cohesive prompt. Include all applicable sections, omit sections not relevant to the use case:

```
## Role
[Short, direct role definition. Emphasize verification and disclaimers for uncertainty.]

## Context
[User's task, goals, background. Summarize clarifications from user input.]

## Instructions
1. [Stepwise approach, including how to verify data]
2. [Expert assignments if needed]
3. [How to handle uncertain or missing information]

## Constraints
[Limitations: style, length, references, disclaimers]

## Output Format
[Exact structure of the final output — bullets, paragraphs, code blocks, etc.]

## Reasoning
[OPTIONAL — include only if the user wants chain-of-thought or rationale.
Otherwise, omit to keep the prompt concise.]

## Examples
[OPTIONAL — include when user provides input/output pairs or when examples
significantly improve output quality. Omit for straightforward tasks.]
```

**Section inclusion guide:**
- Role, Context, Instructions, Constraints, Output Format — **always include**
- Reasoning — include only for complex analytical or multi-step tasks
- Examples — include when output quality depends on seeing concrete patterns

### Phase 4: Verify and Deliver

- Self-review: check for ambiguous instructions, missing constraints, or sections that could cause hallucination
- If experts were used, note their review
- Present the final prompt, organized and easy to follow
- Offer to iterate if the user wants adjustments

## Principles

- **Decompose** complex tasks into smaller subtasks
- **Fresh eyes** — separate creation from validation
- **Never guess** — disclaim uncertainty, ask for data
- **Concise** — only ask clarifying questions when critical
- **Iterative** — verify before delivering, offer refinement
- **Section-aware** — include only relevant sections, omit what doesn't apply
