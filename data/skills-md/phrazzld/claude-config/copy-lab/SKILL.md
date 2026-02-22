---
name: copy-lab
description: Orchestrate copy exploration. Brief, generate 5 distinct approaches, adversarial review, iterate to 90+ composite, present catalog, user selects, execute.
effort: high
---

# Copy Lab Skill

Design-lab pattern, but for copy. No files, no routes. Output inline only.

## Phase 1: Brief

Reuse gathering questions from `~/.claude/skills/copywriting/SKILL.md`:
- Page purpose
- Audience
- Product/offer
- Context

Ask only missing info. Keep it tight.

## Phase 2: Generate 5 Distinct Approaches

Create five different angles/strategies, not word variants.
Each approach must differ on at least two axes:
- Target persona framing
- Core promise or mechanism
- Proof angle
- Objection strategy
- Tone/voice
- Structure/section order

Label A-E with short name.

## Phase 3: Review Each With copy-reviewer

Run `copy-reviewer` agent lenses on each approach.
Capture per-lens scores + composite.

## Phase 4: Iterate Until All 5 Hit 90+

Revise each approach using review findings.
Keep approaches distinct. No convergence.
Repeat review until composite >= 90 for all five.

## Phase 5: Present Catalog

Inline catalog format:
- Approach name + 1-line strategy
- Final copy
- Scores (6 lenses + composite)
- Rationale: why it works, what risk it avoids

No file writes. No routes.

## Phase 6: User Selects, Execute

Ask user to pick A-E or mix.
If mix, synthesize one final draft and re-run review.
Deliver final copy only after composite >= 90.
