---
name: sec-shenanigans-classifier
description: Classify SEC filing evidence using Financial Shenanigans taxonomy (EM1-7, CF1-3, KM1-2, AA1-3) and produce confidence-scored risk calls. Use when users ask to detect accounting tricks, map red flags to categories, or assess manipulation risk.
---
# SEC Shenanigans Classifier

Convert evidence into falsifiable risk hypotheses.

## Inputs

- Required: `evidence-table.md`
- Schema: `references/bundle-contract.md` in orchestrator skill

## Workflow

1. Validate `evidence-table.md` required columns.
1. Map evidence rows to candidate categories (`EM`, `CF`, `KM`, `AA`).
1. Build claims with supporting and counter evidence ids.
1. Apply confidence gates (`high|medium|low`).
1. Write artifact `risk-register.md`.

## Required Output Artifact

Write `risk-register.md` with required columns defined in `../sec-shenanigans-orchestrator/references/bundle-contract.md`.

## Rules

- Zero-Hallucination Policy: If the extracted evidence does not genuinely match any Shenanigans risk patterns, it is perfectly acceptable to output an empty `risk-register.md`. Never stretch the truth, invent concerns, or force a risk classification just because this is a forensic task. "No Shenanigans Found" is a valid and expected outcome for clean companies.
- Do not produce `high` confidence without at least one numeric and one disclosure signal.
- Keep claims testable and linked to `evidence_id`.
- If evidence is weak, keep call in watchlist (`low`).

Read taxonomy details in `references/shenanigans-taxonomy.md`.
