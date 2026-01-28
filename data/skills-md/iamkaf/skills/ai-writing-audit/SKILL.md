---
name: ai-writing-audit
description: Use when the user asks to "audit AI writing", "remove AI patterns", "make this sound less AI", "un-AI this text", or similar requests to identify/remove AI-generated writing patterns.
version: 1.1.0
---

Audit content for AI-generated writing patterns and rewrite to sound authentic.

## Scan Targets

- If paths provided: scan those paths
- Otherwise: scan markdown and source files project-wide (README*, docs/, src/, etc.)

## Process

### Phase 1: Scan and Flag

**Vocabulary:**
- Hype verbs: unleash, elevate, empower, foster, spearhead, unlock, delve, leverage
- Corporate adjectives: robust, comprehensive, seamless, cutting-edge, meticulous, pivotal
- Filler phrases: "in the rapidly evolving landscape of...", "it is important to note that..."

**Structure:**
- Emoji bullet lists with identical format per item (emoji + bold + explanation)
- Perfectly symmetrical lists (same length/structure for each item)
- Marketing tone for simple tools

**Tone:**
- Overly polite ("please feel free to...")
- Unwarranted enthusiasm
- Generic foo/bar examples lacking domain context

### Phase 2: Report

Present findings: files scanned, flagged lines with pattern type, suggested rewrites.

**Wait for approval before rewriting.**

### Phase 3: Rewrite

After approval, rewrite flagged content:

- Write like a dev explaining to another dev
- Use casual shorthand (repo, config, PR)
- Be direct about limitations
- Allow personality; skip polish
- No hype verbs, no symmetrical lists, no corporate fluff