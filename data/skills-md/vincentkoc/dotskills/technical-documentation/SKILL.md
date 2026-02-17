---
name: technical-documentation
description: Build and review high-quality technical docs for brownfield and evergreen documentation systems.
license: AGPL-3.0-only
metadata:
  source: "https://github.com/vincentkoc/dotskills"
---

# Technical Documentation

## Purpose

Produce and review technical documentation that is clear, actionable, and maintainable for both humans and agents.

## When to use

- Creating or overhauling docs in an existing product/codebase (brownfield).
- Building evergreen docs meant to stay accurate and reusable over time.
- Reviewing doc diffs for structure, clarity, and operational correctness.

## Workflow

1. Classify task: `build` or `review`; context: `brownfield` or `evergreen`.
2. Read `references/principles.md` for the governing ruleset (Matt Palmer + OpenAI).
3. For build tasks, follow `references/build.md`.
4. For review tasks, follow `references/review.md`.
5. Use `references/tooling.md` when platform/tooling choices affect recommendations.
6. In brownfield mode, prioritize compatibility with current docs IA, tooling, and release state.
7. In evergreen mode, prioritize timeless wording, update strategy, and durable structure.
8. Return deliverables plus validation notes and remaining gaps.

## Inputs

- Doc type (tutorial, how-to, reference, explanation) and audience.
- File scope or diff scope.
- Docs framework/tooling constraints (Fern, Mintlify, Sphinx, etc.).
- Build/review mode and brownfield/evergreen intent.

## Outputs

- Updated draft or review findings with clear next actions.
- Validation notes (what was checked, what remains).
- Navigation/maintenance recommendations for long-term quality.
