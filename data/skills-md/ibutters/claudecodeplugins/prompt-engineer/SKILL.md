---
name: prompt-engineer
description: This skill should be used when the user asks to "create a prompt", "optimize a prompt", "improve this prompt", "engineer a prompt", "prompt engineering best practices", "make this prompt better", "recommend a model", "which model should I use", "best model for", "GPT vs Claude", "Opus vs Sonnet", "Haiku vs Sonnet", "analyze prompt quality", "fix my prompt", "prompt for Claude", "prompt for GPT", or needs help with prompt engineering techniques, model selection, or prompt optimization for any LLM (Claude Opus/Sonnet/Haiku 4.5, GPT 5.1/Codex, Gemini Pro 3.0).
version: 1.0.0
---

# Prompt Engineering Skill

## Purpose

This skill enables comprehensive prompt engineering across multiple LLM models. Engineer, optimize, and refine prompts using established best practices. Create new prompts from scratch or improve existing ones for maximum effectiveness. Recommend optimal models based on specific requirements through interactive analysis.

**Supported Models:**
- Claude Opus 4.5, Sonnet 4.5, Haiku 4.5
- GPT 5.1, GPT 5.1 Codex
- Gemini Pro 3.0

## When to Use This Skill

Invoke this skill when the user requests:
- Creating a new prompt for any supported LLM model
- Optimizing or improving an existing prompt
- Recommending which model to use for a specific task
- Comparing models for specific use cases
- Analyzing prompt weaknesses or issues
- Applying model-specific optimization techniques
- Migrating prompts between different models
- Troubleshooting poor model performance

## Core Prompt Engineering Techniques

Six universal techniques apply across all models:

| Technique | When to Use | Impact |
|-----------|-------------|--------|
| **XML Tags** | 3+ components, structured output | High - clear separation |
| **Role Prompting** | Domain expertise needed | Medium - contextual knowledge |
| **Clear & Direct** | Always (baseline) | Critical - foundation |
| **Multishot Prompting** | Format/style consistency | High - 40-60% improvement |
| **Chain of Thought** | Complex reasoning | High - accuracy boost |
| **Prompt Chaining** | Multi-stage workflows | High - manages complexity |

**Technique Selection Matrix:**

| Task Type | Recommended Techniques |
|-----------|----------------------|
| Simple question/task | Clear & Direct |
| Classification/extraction | Clear & Direct + Examples |
| Analysis/reasoning | Clear & Direct + Chain of Thought |
| Domain-specific task | Clear & Direct + Role Prompting |
| Complex structured output | Clear & Direct + XML Tags + Examples |
| Multi-step process | Clear & Direct + Prompt Chaining |

## Supported Models Overview

### Claude Family

| Model | Best For | Speed | Quality | Cost |
|-------|----------|-------|---------|------|
| **Opus 4.5** | Research, creative, complex analysis | Slow | Highest | $$$$$ |
| **Sonnet 4.5** | Agentic coding, balanced production | Fast | High | $$ |
| **Haiku 4.5** | Classification, high-volume, latency-critical | Very Fast | Good | $ |

### OpenAI Family

| Model | Best For | Speed | Quality | Cost |
|-------|----------|-------|---------|------|
| **GPT 5.1** | General-purpose, function calling | Fast | High | $$ |
| **GPT 5.1 Codex** | Code generation, review, debugging | Fast | High (code) | $$ |

### Google Family

| Model | Best For | Speed | Quality | Cost |
|-------|----------|-------|---------|------|
| **Gemini Pro 3.0** | Multimodal, context caching, Google integration | Fast | High | $$ |

## Prompt Engineering Workflow

### Step 1: Understand Requirements

Gather essential information:
- Task purpose and success criteria
- Target model (if specified) or requirements for recommendation
- Input and output format requirements
- Constraints (length, style, format)
- Current issues (for optimization requests)

### Step 2: Select or Recommend Model

**If model specified:** Load the corresponding model guide from `reference/models/`.

**If model not specified:** Gather requirements via interactive dialog:
1. Task type (code, analysis, creative, data, conversation)
2. Priority (speed, quality, cost, balance)
3. Context size requirements
4. Special features needed (vision, function calling, JSON mode)

Then consult `reference/comparisons/model-comparison-matrix.md` and `reference/comparisons/use-case-recommendations.md`.

### Step 3: Select Techniques

Always start with Clear & Direct (foundation technique).

Add based on needs:
- **XML Tags:** Complex structure, 3+ components
- **Role Prompting:** Domain expertise required
- **Examples:** Format consistency needed
- **Chain of Thought:** Reasoning tasks
- **Prompt Chaining:** Multi-stage workflows

### Step 4: Load References

Load technique documentation from `reference/techniques/`:
- Always load: `03-be-clear-and-direct.md`
- Add as needed: Relevant technique files

Load model guide from `reference/models/`:
- Target model optimization guide

### Step 5: Draft or Optimize Prompt

**For new prompts:**
1. Apply selected techniques systematically
2. Structure with XML tags if appropriate
3. Add examples if format matters
4. Include model-specific optimizations

**For optimization:**
1. Analyze current prompt against checklist
2. Identify missing or misapplied techniques
3. Apply fixes systematically
4. Add model-specific optimizations

### Step 6: Validate

Use `reference/optimization/optimization-checklist.md` to verify:
- Clarity and completeness
- Proper technique application
- Model-specific requirements met
- No common pitfalls

### Step 7: Deliver

Provide:
1. Complete prompt (ready to use)
2. Technique explanation (what was applied and why)
3. Usage instructions (how to use, variables to replace)
4. Testing recommendations (how to verify it works)

## Reference Documentation

### Technique References

Detailed documentation for each technique:
- `reference/techniques/01-xml-tags.md` - Structuring prompts
- `reference/techniques/02-role-prompting.md` - System prompts and roles
- `reference/techniques/03-be-clear-and-direct.md` - Foundation technique
- `reference/techniques/04-multishot-prompting.md` - Using examples
- `reference/techniques/05-chain-of-thought.md` - Step-by-step reasoning
- `reference/techniques/06-prompt-chaining.md` - Multi-stage workflows

### Model Guides

Model-specific optimization guides:
- `reference/models/claude-opus-4.5.md` - Opus capabilities and optimizations
- `reference/models/claude-sonnet-4.5.md` - Sonnet capabilities and optimizations
- `reference/models/claude-haiku-4.5.md` - Haiku capabilities and optimizations
- `reference/models/gpt-5.1.md` - GPT 5.1 capabilities and optimizations
- `reference/models/gpt-5.1-codex.md` - Codex capabilities and optimizations
- `reference/models/gemini-pro-3.0.md` - Gemini capabilities and optimizations

### Comparison Resources

Cross-model analysis:
- `reference/comparisons/model-comparison-matrix.md` - Capability comparison
- `reference/comparisons/use-case-recommendations.md` - Task-based recommendations

### Optimization Resources

Quality assurance and troubleshooting:
- `reference/optimization/optimization-checklist.md` - Validation checklist
- `reference/optimization/troubleshooting-guide.md` - Common issues and fixes
- `reference/optimization/model-migration.md` - Adapting prompts between models

### Example Library

Working examples by category:
- `examples/classification-prompts.md` - Classification tasks
- `examples/code-generation-prompts.md` - Code generation tasks
- `examples/analysis-prompts.md` - Analysis and research tasks
- `examples/creative-prompts.md` - Creative writing tasks
- `examples/complex-workflow-prompts.md` - Multi-step workflows

## Key Principles

### 1. Clarity is Foundational

Every prompt must have clear context, explicit instructions, defined success criteria, and specified output format. Without clarity, other techniques cannot compensate.

### 2. Match Technique to Task

Simple tasks need simple prompts. Complex tasks benefit from multiple techniques. Match complexity to actual need.

### 3. Model-Specific Optimization Matters

Each model has unique characteristics. Apply model-specific optimizations after general techniques for best results.

### 4. Test and Iterate

First drafts rarely perfect. Test with real inputs, identify failure modes, refine systematically.

### 5. Progressive Disclosure

Load detailed references only when needed. Start with core workflow, dive into specifics as required.

## Quick Decision Guide

**Which model for coding?**
- Agentic/complex: Claude Sonnet 4.5
- Code generation focused: GPT 5.1 Codex
- Simple transforms: Claude Haiku 4.5

**Which model for analysis?**
- Complex research: Claude Opus 4.5
- General analysis: Claude Sonnet 4.5 or GPT 5.1
- Quick classification: Claude Haiku 4.5

**Which model for creative work?**
- Highest quality: Claude Opus 4.5
- Good quality, faster: Claude Sonnet 4.5

**Which model for high volume?**
- Speed critical: Claude Haiku 4.5
- Cost critical: Claude Haiku 4.5 or Gemini Pro 3.0

**Which model for multimodal?**
- Image understanding: Claude Opus 4.5 or Gemini Pro 3.0
- Vision + reasoning: Claude Opus 4.5

## Output Formats

### For New Prompts

Provide complete prompt, techniques applied, usage instructions, and testing recommendations.

### For Optimization

Provide analysis of issues, improved prompt, changes made with explanations, and testing recommendations.

### For Model Recommendations

Provide top 3 recommendations with match scores, comparison table, trade-off analysis, and prompt creation offer.

### For Prompt Analysis

Provide strengths, weaknesses, techniques assessment, and prioritized improvement recommendations.
