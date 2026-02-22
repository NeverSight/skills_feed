---
name: prompt-engineering
description: "Creates system prompts, writes tool descriptions, and structures agent instructions for agentic systems. Use when the user asks to create, generate, or design prompts for AI agents, especially for tool-using agents, planning agents, or autonomous systems. **PROACTIVE ACTIVATION**: Auto-invoke when designing prompts for agents, tools, or agentic workflows in AI projects. **DETECTION**: Check for agent/tool-related code, prompt files, or user mentions of \"prompt\", \"agent\", \"LLM\". **USE CASES**: Designing system prompts, tool descriptions, agent instructions, prompt optimization, reducing hallucinations."
author: mguinada
version: 1.0.0
tags: [prompts, agents, ai, prompt-engineering, techniques]
---

# Prompt Engineering for Agentic Systems

## Overview

Generate optimized prompts for agentic systems with clear rationale for technique selection.

**Core Principles:**
- **Match technique to task** - Different agent types require different prompting approaches
- **Trade-offs matter** - Always consider cost, latency, and accuracy when selecting techniques
- **Structure over verbosity** - Well-organized prompts outperform long unstructured ones
- **Test and iterate** - Verify prompts work before deploying to production

> **For broader agentic system design** (choosing workflows vs agents, ACI/tool specifications, guardrails, multi-agent patterns), see the **ai-engineering skill**.

## When to Use

Invoke this skill when:
- Creating prompts for tool-using agents (ReAct pattern)
- Designing prompts for planning or strategy agents
- Building prompts for data processing or validation agents
- Reducing hallucinations in fact-based tasks
- Optimizing prompt performance or cost

## Common Scenarios

### Scenario 1: Tool-Using Agent (ReAct)

**Use when**: Agent needs to reason and use tools autonomously

```markdown
## SYSTEM
You are a research agent. Your goal is to gather information and synthesize findings.

## INSTRUCTIONS
Follow this pattern for each action:
Thought: [what you want to do]
Action: [tool name and parameters]
Observation: [result from tool]

When you have enough information, provide a final summary.

## AVAILABLE TOOLS
- search(query): Search for information
- read(url): Read a webpage
- finish(summary): Complete the task

## STOP CONDITION
Stop when you have answered the user's question or gathered sufficient information.
```

---

### Scenario 2: Planning Agent (Tree of Thoughts)

**Use when**: Agent needs to explore multiple approaches before committing

```markdown
## TASK
Design a migration strategy from monolith to microservices.

## INSTRUCTIONS
Generate 3 different approaches:

Approach 1: [description]
- Pros: [list]
- Cons: [list]
- Effort: [estimate]

Approach 2: [description]
- Pros: [list]
- Cons: [list]
- Effort: [estimate]

Approach 3: [description]
- Pros: [list]
- Cons: [list]
- Effort: [estimate]

Then select the best approach and explain your reasoning.
```

---

### Scenario 3: Data Validation (Few-Shot with Negative Examples)

**Use when**: Agent needs consistent output format and should avoid common errors

```markdown
## TASK
Validate email addresses and return structured JSON.

## VALID EXAMPLES
Input: user@example.com
Output: {"valid": true, "reason": "proper email format"}

Input: user.name@company.co.uk
Output: {"valid": true, "reason": "proper email format"}

## INVALID EXAMPLES (what NOT to accept)
Input: user@.com
Output: {"valid": false, "reason": "invalid domain format"}

Input: @example.com
Output: {"valid": false, "reason": "missing local part"}

Input: user example.com
Output: {"valid": false, "reason": "missing @ symbol"}

## NOW VALIDATE
Input: {user_input}
```

---

### Scenario 4: Factual Accuracy (Chain-of-Verification)

**Use when**: Reducing hallucinations is critical

```markdown
## TASK
Explain how transformers handle long-context windows

## STEP 1: Initial Answer
Provide your explanation...

## STEP 2: Verification Questions
Generate 5 questions that would expose errors in your answer:
1. [question]
2. [question]
3. [question]
4. [question]
5. [question]

## STEP 3: Answer Verification
Answer each verification question factually...

## STEP 4: Final Answer
Refine your original answer based on verification results...
```

---

### Scenario 5: Complex Decision (Structured Thinking)

**Use when**: Agent needs to analyze trade-offs before deciding

```markdown
## TASK
Recommend: microservices or monolith for our startup?

## THINKING PROTOCOL

[UNDERSTAND]
- Restate the problem in your own words
- Identify what's actually being asked

[ANALYZE]
- Break down into sub-components
- Note assumptions and constraints

[STRATEGIZE]
- Outline 2-3 approaches
- Evaluate trade-offs

[EXECUTE]
- Provide final recommendation
- Explain reasoning
```

---

### Scenario 6: Self-Improving Output (Self-Refine)

**Use when**: You want the agent to review and improve its own work

```markdown
## TASK
Write a README for the checkout API

## STEP 1: Initial Draft
[Generate initial README]

## STEP 2: Critique
Identify 3-5 improvements needed:
- [weakness 1]
- [weakness 2]
- [weakness 3]

## STEP 3: Refinement
Rewrite addressing all identified improvements...
```

---

## Quick Decision Tree

Use this table to select techniques quickly:

| Agent Characteristic | Recommended Technique |
|---------------------|----------------------|
| Uses tools autonomously | ReAct |
| Planning/strategy with alternatives | Tree of Thoughts |
| High-stakes correctness | Self-Consistency |
| Factual accuracy, hallucination reduction | Chain-of-Verification (CoVe) |
| Single-path complex reasoning | Chain of Thought |
| Complex decisions with trade-offs | Structured Thinking Protocol |
| Reducing bias, multiple viewpoints | Multi-Perspective Prompting |
| Uncertainty quantification | Confidence-Weighted Prompting |
| Proprietary documentation, prevent hallucinations | Context Injection with Boundaries |
| Self-review and improvement | Self-Refine |
| Breaking complex problems into subproblems | Least-to-Most Prompting |
| High-quality content through multiple passes | Iterative Refinement Loop |
| Multi-stage workflows with specialized prompts | Prompt Chaining |
| Improving recall for factual questions | Generated Knowledge Prompting |
| Unclear how to structure the prompt | Meta-Prompting (nuclear option) |
| Strict technical requirements | Constraint-First Prompting |
| Requires consistent format/tone | Few-Shot (supports negative examples) |
| Simple, well-defined task | Zero-Shot |
| Domain-specific expertise | Role Prompting |
| Procedural workflow | Instruction Tuning |

For detailed decision logic with branching, see [decision-tree.md](references/decision-tree.md)

## Technique Reference

All available techniques with examples, use cases, and risks: [techniques.md](references/techniques.md)

## Critical Anti-Patterns

Common mistakes to avoid: [anti-patterns.md](references/anti-patterns.md)

**Critical warnings**:
- **Do NOT use ReAct without tools** - Adds unnecessary complexity
- **Do NOT use Tree of Thoughts for deterministic problems** - Single correct answer doesn't need alternatives
- **Do NOT use vague roles** - "Expert" without scope provides little benefit
- **Do NOT omit stop conditions** - Agents may continue indefinitely
- **Do NOT use Self-Refine for objective tasks** - Calculations don't need self-critique

## Canonical Template

Use this template as the foundation for generated prompts: [template.md](references/template.md)

**Basic structure**:
```markdown
## SYSTEM / ROLE
You are a [specific role] with authority over [explicit scope]
Boundaries: [what you must NOT do]

## TASK
[Single clear goal in one sentence]

## INSTRUCTIONS
Follow these steps:
1. [First step]
2. [Second step]

Constraints:
- [Specific limits]
- [Format requirements]

## STOP CONDITION
Stop when: [success criteria]
```

## Output Rationale Template

When delivering a generated prompt, use this structure:

```markdown
## Generated Prompt for [Agent Name/Type]

[prompt in code block]

## Rationale

**Agent Type**: [Tool-using / Planner / Conversational / Data-processor]

**Task Complexity**: [Simple / Multi-step / Planning-heavy]

**Techniques Used**:
- [Technique]: [Why it works for this use case]

**Expected Behavior**: [What the agent will do]

**Trade-offs**: [Cost, latency, flexibility - ALWAYS include if technique increases tokens or latency]

**Considerations**: [Edge cases, limitations, or risks]
```

## Guardrail Rule

If a prompt increases latency, token usage, or operational cost, this **MUST** be stated explicitly in the rationale under "Trade-offs."

Techniques that increase cost/latency:
- Self-Consistency (multiple generations)
- Chain-of-Verification (multiple passes)
- Iterative Refinement Loop (multiple passes)
- Self-Refine (multiple passes)
- Tree of Thoughts (exploring alternatives)
- Least-to-Most Prompting (sequential subproblems)
