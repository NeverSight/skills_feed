---
name: critique
description: Get a full literary critique of your completed manuscript. NYT/New Yorker style.
argument-hint: "[book N]"
---

Request a full manuscript critique using the critique agent.

## What This Does

1. Asks what length critique you want (long, medium, or short)
2. Checks if manuscript is complete
3. If complete, reads entire manuscript
4. Produces a literary review at your chosen length
5. Includes craft observations (long/medium modes)

## Prerequisites

**The manuscript must be complete.** The critique will check for:
- All chapters marked as drafted
- Status markers indicating completion
- Reasonable chapter count

If incomplete, it will decline and explain what's missing.

## Usage

```
/critique                  # Critique the current project
/critique book 2           # Critique specific book in series
```

If arguments provided: $ARGUMENTS

## Length Options

- **Long** — Full 1000-1500 word NYT/New Yorker style review with 2-3 craft observations
- **Medium** — Substantive 400-600 word review with 1-2 craft observations
- **Short** — Quick 150-250 word summary of key strengths and concerns

## Output

Critiques are saved to `critiques/critique-YYYY-MM-DD-{length}.md` and tracked in `progress.md`.

A professional literary review covering:
- Prose style
- Structure and pacing
- Characterization
- Emotional resonance
- Thematic coherence
- Plus craft-level technical observations (long/medium modes)

## When to Use

- After completing a full draft
- Before major revision
- When you need distance and perspective
