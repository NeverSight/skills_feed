---
name: debrief
description: Customer requirements → questionnaire (default) or BRD (with --answers flag)
version: 5.3.2
---

# /debrief - Business Requirements Document

**Role**: Business analyst creating market-validated BRDs.

**Focus**: WHAT features + WHY (business), not HOW (technical).

---

## When to Use

- New project → Create BRD
- Add features → Extend BRD
- Process customer answers → Update BRD
- Questionnaire only → Generate questions

---

## Usage

```bash
/debrief "Customer wants..."                # New project → questionnaire output
/debrief "Add {feature}"                    # Add feature → questionnaire output
/debrief --answers questionnaire.xlsx       # Process answers → CREATE BRD
/debrief --generate-brd questionnaire.xlsx  # Generate BRD from research
```

**Key principle**:
- **Without flags**: ONLY outputs questionnaire (no BRD)
- **With --answers or --generate-brd**: Creates BRD files

---

## Output

**Default (no flags)**: `questionnaire-{date}.xlsx` only (3 sheets: Summary, Questions, References)

**With --answers or --generate-brd**:
- `plans/brd/` - Project-wide BRD files
- `plans/brd/use-cases/` - Use cases by feature
- `plans/features/{feature}/` - Feature-specific files

---

## Key Principles

### 1. Questionnaire First (Default)

**Default behavior (no flags)**:
- ALWAYS output: Summary + Questionnaire (3 sheets Excel)
- NEVER auto-create: BRD files, use cases, feature folders

**BRD creation (explicit flags)**:
- `--answers questionnaire.xlsx` → Creates BRD after customer fills it
- `--generate-brd questionnaire.xlsx` → Creates BRD from existing research

**Why**: User reviews research first, validates with customer, THEN creates BRD.

### 2. Business Focus ONLY

**Do**:
- WHAT features users need (login, checkout, reports)
- WHY they need it (business value, user goal)
- WHEN it's needed (MVP, Standard, Advanced)

**Never do**:
- HOW to code it (files, functions, APIs)
- WHICH technology (React, Vue, database)
- WHERE to put code (components, services)

**This is NOT dev-specs**. Stay business level. No technical suggestions.

**If you mention files, code, APIs, or tech → YOU ARE DOING IT WRONG.**

### 3. Deep Research + Revalidation (ALWAYS)

**Always thorough** (regardless of scope tier):
1. Comparison pages (feature matrix)
2. **Multi-source revalidation** (MANDATORY):
   - Ecosystems (Chrome, WordPress, GitHub, NPM)
   - User signals (Reddit, reviews, forums)
   - Competitor direct (pricing, features)
3. Full evidence per feature (3+ source types)

**No shortcuts**: MVP/Standard/Full all get same deep research + revalidation.

### 4. Questionnaire = Decision Tool

**How to generate**:
1. Write JSON to temp file: `/tmp/debrief-questions-{timestamp}.json`
2. Call Python script with file path:
```bash
python .claude/skills/debrief/scripts/generate_questionnaire.py \
  plans/brd/use-cases/{feature-name}/questionnaire-{YYYY-MM-DD}.xlsx \
  /tmp/debrief-questions-{timestamp}.json
```
(See `references/workflow.md` for full JSON format)

**CRITICAL: Populate with real data**:
- **questions array**: 2-5 questions per feature (validation + open questions)
- **references object**: URLs by feature (comparison, reviews, ecosystems)
- **research object**: Feature counts, tier breakdown, source counts

**3 sheets generated**:
- Summary (features count, tier breakdown, research stats)
- Questions (validation + open questions with context)
- References (URLs by feature, organized by source type)

**Purpose**: User reviews evidence, makes decisions, validates with customer.

Then create BRD via `--answers` or `--generate-brd`.

---

## Workflow

**See** `references/workflow.md` for detailed steps.

**CRITICAL**: ALWAYS ask context questions FIRST using AskUserQuestion tool before doing any research.

**Modes**:
- **New Project**:
  1. Ask 4 questions (Industry, Users, Constraints, Scope mode: MVP/Market Standard/Full)
  2. Research + questionnaire → `plans/brd/use-cases/{project}/questionnaire-{date}.xlsx`
  3. NO BRD created
- **Add Feature**:
  1. Ask 2 questions (Feature name, Scope mode: MVP/Market Standard/Full)
  2. Research + questionnaire → `plans/brd/use-cases/{feature}/questionnaire-{date}.xlsx`
  3. NO BRD created
- **Process Answers** (`--answers`):
  1. Read filled questionnaire
  2. **ASK what to do**: Continue research / Ask follow-ups / Create BRD
  3. Execute based on choice
- **Generate BRD** (`--generate-brd`): Create BRD from research

**Default**: Questionnaire only. BRD requires explicit flag AND user confirmation.

---

## Market Research (Always Deep)

**See** `references/research.md`.

**Always deep**: Comparison + ecosystems + user signals + full evidence.

**Tiers**:
- **MVP**: 80%+ competitors, free tier, high demand
- **Standard**: 60-80% competitors, pro tier, expected
- **Advanced**: <60% competitors, enterprise, differentiator

---

## Tools

AskUserQuestion, WebSearch, Glob, Read, Write, Bash

---

## References

- `references/workflow.md` - Principles and methodology
- `references/research.md` - Market research guide
- `references/codes.md` - Group codes and file patterns
- `references/templates/` - Output formats

---

## Scripts

**Generate questionnaire from JSON file**:
```bash
python .claude/skills/debrief/scripts/generate_questionnaire.py \
  plans/brd/use-cases/{feature}/questionnaire-{date}.xlsx \
  /tmp/debrief-questions.json
```

**JSON file should be written to `/tmp/` first**, then passed to script.
