---
name: sequential-thinking
description: Dynamic problem-solving through structured sequential thoughts. Use when breaking down complex problems, planning multi-step solutions, analyzing ambiguous requirements, debugging intricate issues, exploring design alternatives, or tackling problems where the full scope is unclear. Enables thought revision, branching, and iterative refinement.
---

# Sequential Thinking

## Overview

This skill provides structured sequential thinking for complex problem-solving through a dynamic, reflective thought process. Each thought can build on, question, or revise previous insights as understanding deepens.

## When to Use

- Breaking down complex problems into manageable steps
- Planning and design with room for revision
- Analysis that might need course correction
- Problems where full scope is unclear initially
- Multi-step solutions requiring maintained context
- Filtering irrelevant information from complex scenarios
- Debugging intricate issues requiring systematic exploration

## Script Location

The script is located at: `~/.config/opencode/skills/sequential-thinking/scripts/sequential-thinking.ts`

Use `$SKILL_DIR` or the full path when invoking from any directory.

## Core Workflow

### 1. Initialize Thinking

Start a thinking sequence by estimating total thoughts needed:

```bash
bun ~/.config/opencode/skills/sequential-thinking/scripts/sequential-thinking.ts sequentialthinking \
  --thought "Initial analysis of the problem..." \
  --thought-number 1 \
  --total-thoughts 5 \
  --next-thought-needed true
```

### 2. Continue Sequence

Build on previous thoughts, adjusting estimates as needed:

```bash
bun ~/.config/opencode/skills/sequential-thinking/scripts/sequential-thinking.ts sequentialthinking \
  --thought "Building on insight from step 1..." \
  --thought-number 2 \
  --total-thoughts 5 \
  --next-thought-needed true
```

### 3. Revise Previous Thinking

When reconsidering earlier conclusions:

```bash
bun ~/.config/opencode/skills/sequential-thinking/scripts/sequential-thinking.ts sequentialthinking \
  --thought "Reconsidering step 2, I realize..." \
  --thought-number 4 \
  --total-thoughts 6 \
  --is-revision true \
  --revises-thought 2 \
  --next-thought-needed true
```

### 4. Branch Exploration

Explore alternative approaches:

```bash
bun ~/.config/opencode/skills/sequential-thinking/scripts/sequential-thinking.ts sequentialthinking \
  --thought "Alternative approach from step 3..." \
  --thought-number 5 \
  --total-thoughts 7 \
  --branch-from-thought 3 \
  --branch-id "alternative-approach" \
  --next-thought-needed true
```

### 5. Complete Thinking

Conclude when solution is verified:

```bash
bun ~/.config/opencode/skills/sequential-thinking/scripts/sequential-thinking.ts sequentialthinking \
  --thought "Final verified conclusion..." \
  --thought-number 6 \
  --total-thoughts 6 \
  --next-thought-needed false
```

## Key Features

- **Adjustable estimates**: Modify `totalThoughts` up/down as understanding evolves
- **Thought revision**: Mark thoughts as revisions with `--is-revision` and `--revises-thought`
- **Branching**: Explore alternatives with `--branch-from-thought` and `--branch-id`
- **Non-linear thinking**: Branch or backtrack as needed
- **Hypothesis verification**: Generate and verify solution hypotheses iteratively

## Parameters Reference

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--thought` | Yes | Current thinking step content |
| `--thought-number` | Yes | Current position in sequence (1-based) |
| `--total-thoughts` | Yes | Estimated total thoughts (adjustable) |
| `--next-thought-needed` | Yes | `true` to continue, `false` to conclude |
| `--is-revision` | No | `true` if revising previous thinking |
| `--revises-thought` | No | Which thought number being revised |
| `--branch-from-thought` | No | Branching point thought number |
| `--branch-id` | No | Identifier for the branch |
| `--needs-more-thoughts` | No | Signal more thoughts needed |

## Output Formats

Control output with `--output` flag:
- `text` (default): Human-readable text
- `json`: Structured JSON
- `markdown`: Markdown formatted
- `raw`: Raw response data

## Resources

### scripts/
- `sequential-thinking.ts` - MCP server wrapper for sequential thinking (requires Bun runtime)

### references/
- `thinking-patterns.md` - Common thinking patterns and examples for various problem types
