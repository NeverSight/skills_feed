---
name: sec-shenanigans-memo-writer
description: Convert SEC evidence, taxonomy classifications, and ratio diagnostics into an investor-grade Shenanigans risk memo. Use when users ask for a final report, diligence brief, investment-risk summary, or management-question list.
---
# SEC Shenanigans Memo Writer

Generate final decision-ready outputs from bundle artifacts.

## Inputs

- Required: `evidence-table.md`, `risk-register.md`, `ratio-diagnostics.md`

## Workflow

1. Validate input schemas and link integrity (`evidence_id`, `risk_id`).
1. Rank risks by impact and confidence.
1. Draft memo using required sections.
1. Draft diligence tracker as open questions.
1. Write artifacts `shenanigans-memo.md` and `open-questions.md`.

## Required Output Artifacts

Write both files using required sections/columns in `../sec-shenanigans-orchestrator/references/bundle-contract.md`.

## Rules

- Clean Output Handling: If the inputted `risk-register.md` is empty, write a memo explicitly stating that no material forensic red flags were identified based on the provided evidence. Do not invent artificial concerns to fill space.
- Separate evidence, interpretation, and uncertainty.
- Use neutral forensic language.
- Include watchlist items when confidence is low.

Use `references/memo-template.md` for narrative structure.
