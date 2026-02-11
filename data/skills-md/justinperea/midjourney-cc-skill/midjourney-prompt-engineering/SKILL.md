---
name: midjourney-prompt-engineering
description: Use when generating images with Midjourney, constructing MJ prompts, iterating on MJ output quality, choosing between --sref/--oref/style codes, scoring image results, or building reusable prompt patterns. Also use when exploring MJ style codes, animating images, or debugging why a prompt isn't producing the intended result.
---

# Midjourney Prompt Learning System

A skill that knows Midjourney. The foundation is a structured understanding of Midjourney V7 built from the [official documentation](https://docs.midjourney.com) — every parameter, prompt syntax rule, reference system, and style code mechanic. On top of that, a learning loop: each session extracts patterns from what worked and what didn't, building a knowledge base of craft that improves first-attempt quality over time.

## Architecture

**You are a multimodal reasoning model.** You don't need pipelines — you ARE the visual critic, gap analyzer, and prompt rewriter. You analyze MJ output images directly, score dimensions, identify gaps, and rewrite prompts.

**The one thing you can't do natively is remember across sessions.** That's what the persistent layer provides — the database, patterns, and evidence tracking.

## Knowledge Foundation (ships with the skill)

| File | What It Contains | Source |
|------|-----------------|--------|
| `knowledge/v7-parameters.md` | Every V7 parameter, prompt structure rules, breaking changes from V6 | [Official docs](https://docs.midjourney.com) |
| `knowledge/translation-tables.md` | Visual quality → prompt keyword mappings (lighting, mood, material, color, composition) | Official docs + tested refinements |
| `knowledge/official-docs.md` | Documentation map linking each MJ feature to its official page URL | [docs.midjourney.com](https://docs.midjourney.com) |
| `knowledge/failure-modes.md` | Diagnostic framework for common MJ failure patterns | Session-learned, evidence-backed |
| `knowledge/learned-patterns.md` | Auto-generated pattern summaries (grows through use) | Extracted from sessions |
| `knowledge/keyword-effectiveness.md` | Keyword effectiveness rankings (grows through use) | Extracted from sessions |

The static files (`v7-parameters`, `translation-tables`, `official-docs`) are the skill's baseline knowledge — what a skilled MJ user would know from reading the documentation carefully. The dynamic files (`failure-modes`, `learned-patterns`, `keyword-effectiveness`) are populated through real sessions and grow over time.

## Module Dependencies

| Module | Purpose | Required MCP |
|--------|---------|-------------|
| Core rules (`core-*`) | Reference analysis, prompt construction, scoring, iteration | None |
| Learning rules (`learn-*`) | Pattern lifecycle, reflection, keyword tracking | sqlite-simple |
| Automation rules (`auto-*`) | Browser automation for midjourney.com | playwright |

**Core only** (manual): Load `core-*` rules. Copy prompts to MJ manually.
**Core + Learning**: Add `learn-*` rules + sqlite MCP. Patterns persist across sessions.
**Full system**: Add `auto-*` rules + playwright MCP. Hands-free iteration.

```bash
# SQLite (for learning rules)
claude mcp add sqlite-simple -- npx @anthropic-ai/sqlite-simple-mcp mydatabase.db

# Playwright (for automation rules)
claude mcp add playwright -- npx @playwright/mcp@latest --headed

# Initialize the database
sqlite3 mydatabase.db < schema.sql
```

## Rules Quick Reference

| Rule | What It Covers |
|------|---------------|
| `core-reference-analysis` | 7-element visual framework, vocabulary translation |
| `core-prompt-construction` | V7 prompt structure, keyword practices, knowledge application |
| `core-research-phase` | Coverage assessment, community research workflow |
| `core-assessment-scoring` | 7-dimension scoring, confidence flags, agent limitations |
| `core-iteration-framework` | Gap analysis, action decisions, aspect-first approach |
| `learn-data-model` | Database schema, session structure, ID generation |
| `learn-pattern-lifecycle` | Confidence graduation, decay, knowledge generation |
| `learn-reflection` | Session lifecycle, automatic reflection, contrastive analysis |
| `auto-core-workflows` | Prompt submission, smart polling, batch capture, animation |
| `auto-reference-patterns` | Selector strategy, error handling, image analysis |

## Scoring

All iterations scored on **7 dimensions**: subject, lighting, color, mood, composition, material, spatial. All 7 always scored (1.0 for "not applicable"). Scores are preliminary until user-validated. See `rules/core-assessment-scoring.md`.

## Commands

| Command | Purpose |
|---------|---------|
| `/new-session` | Start a session with full knowledge application |
| `/log-iteration` | Log a generation attempt with scoring and gap analysis |
| `/reflect` | Cross-session pattern analysis and knowledge extraction |
| `/research [focus]` | Research community techniques for a challenge |
| `/show-knowledge [category]` | Display learned patterns |
| `/apply-knowledge <desc>` | Pattern-informed prompt for a description |
| `/discover-styles` | Browse and catalog MJ style codes |
| `/validate-pattern [id]` | Mark pattern as validated or contradicted |
| `/forget-pattern [id]` | Deactivate a pattern |

## Key Principle

Every pattern must have logged evidence. The system learns from real iteration data, not assumptions. Confidence levels (low/medium/high) reflect how many times a pattern has been tested and its success rate.

## Full Reference

For the complete compiled reference combining all rules, see `AGENTS.md`.
