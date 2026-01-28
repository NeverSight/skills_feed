---
name: clig-eval-prompt
description: Generate a concise Chinese evaluation prompt for DevOps CLI projects based on clig.onev.dev guidelines, with weights, thresholds, and hard gates. Use when a user asks to create or store a reusable CLI review prompt, a scoring rubric, or an evaluation checklist derived from CLI design guidelines.
---

# Clig Eval Prompt

## Overview

Use this skill to produce the standardized evaluation prompt for reviewing DevOps CLI tools against clig.onev.dev. Keep output short, Chinese, and ready to copy-paste.

## Workflow

1) Load the canonical prompt from references/prompt.md.
2) Output it verbatim unless the user requests modifications.
3) If user requests changes (weights/thresholds/language/format), update only those parts and keep the rest intact.
4) If the user asks for a shorter version, compress wording but preserve all hard gates, thresholds, and dimensions.

## Output Rules

- Prefer the exact prompt text from references/prompt.md.
- Keep it in a single fenced code block.
- Do not add extra commentary unless asked.
- If user needs customization, ask one clarification question at a time.

## Resources

- references/prompt.md: Canonical DevOps CLI evaluation prompt (Chinese, concise).
