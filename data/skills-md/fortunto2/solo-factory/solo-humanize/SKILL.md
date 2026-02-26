---
name: solo-humanize
description: Strip AI writing patterns from text — em dashes, stock phrases, promotional inflation, performed authenticity, rule-of-three lists. Use when user says "humanize this", "make it sound human", "strip AI patterns", "clean up the copy", or after /content-gen or /landing-gen produces output.
license: MIT
metadata:
  author: fortunto2
  version: "1.0.1"
  openclaw:
    emoji: "✍️"
allowed-tools: Read, Write, Edit, Glob, Grep
argument-hint: "[file-path or paste text]"
---

# /humanize

Strip AI writing patterns from user-facing text. Takes a file or pasted text and rewrites it to read like a human wrote it, without losing meaning or structure.

## Why this exists

LLM output has recognizable tells — em dashes, stock phrases, promotional inflation, performed authenticity. Readers (and Google) notice. This skill catches those patterns and rewrites them.

## When to use

- After `/content-gen`, `/landing-gen`, `/video-promo` — polish the output
- Before publishing any user-facing prose (blog posts, landing pages, emails)
- When editing CLAUDE.md or docs that will be read by humans
- Standalone: `/humanize path/to/file.md`

## Input

- **File path** from `$ARGUMENTS` — reads and rewrites in place
- **No argument** — asks to paste text, outputs cleaned version
- Works on `.md`, `.txt`, and text content in `.tsx`/`.html` (string literals only)

## Pattern Catalog

### 1. Em Dash Overuse (—)

The most obvious AI tell. Replace with commas, periods, colons, or restructure the sentence.

| Before | After |
|--------|-------|
| "The tool — which is free — works great" | "The tool (which is free) works great" |
| "Three features — speed, security, simplicity" | "Three features: speed, security, simplicity" |
| "We built this — and it changed everything" | "We built this. It changed everything." |

**Rule:** Max 1 em dash per 500 words. Zero is better.

### 2. Stock Phrases

Phrases that signal "AI wrote this." Remove or replace with specific language.

**Filler phrases (delete entirely):**
- "it's worth noting that" → (just state the thing)
- "at the end of the day" → (cut)
- "in today's world" / "in the modern landscape" → (cut)
- "without further ado" → (cut)
- "let's dive in" / "let's explore" → (cut)

**Promotional inflation (replace with specifics):**
- "game-changer" → what specifically changed?
- "revolutionary" → what's actually new?
- "cutting-edge" → describe the technology
- "seamless" → "works without configuration" (or whatever it actually does)
- "leverage" → "use"
- "robust" → "handles X edge cases" (specific)
- "streamline" → "cut steps from N to M"
- "empower" → what can the user now do?
- "unlock" → what's the actual capability?

**Performed authenticity (rewrite):**
- "to be honest" → (if you need to say this, the rest wasn't honest?)
- "let me be frank" → (just be frank)
- "I have to say" → (just say it)
- "honestly" → (cut)
- "the truth is" → (cut, state the truth directly)

### 3. Rule of Three

AI loves triplets: "fast, secure, and scalable." Real writing varies list length.

| Before | After |
|--------|-------|
| "Fast, secure, and scalable" | "Fast and secure" (if scalable isn't proven) |
| "Build, deploy, and iterate" | "Build and ship" (if that's what you mean) |
| Three bullet points that all say the same thing | One clear bullet |

**Rule:** If you find 3+ triplet lists in one document, break at least half of them.

### 4. Structural Patterns

**Every section has the same shape:**
AI tends to write: heading → one-sentence intro → 3 bullets → transition sentence. Real writing varies section length and structure.

**Hedging sandwich:**
"While X has limitations, it offers Y, making it Z." → Pick a side. State it.

**False balance:**
"On one hand X, on the other hand Y." → If one side is clearly better, say so.

### 5. Sycophantic Openers

- "Great question!" → (cut)
- "That's a fantastic idea!" → (cut, or say what's specifically good about it)
- "Absolutely!" → (cut if not genuine agreement)
- "I'd be happy to help!" → (just help)

### 6. Passive Voice / Weak Verbs

- "It should be noted that" → (cut, just note it)
- "There are several factors that" → name the factors
- "It is important to" → say why
- "This can be achieved by" → "Do X"

## Process

1. **Read the input** — file path or pasted text.

2. **Scan for patterns** — check each category above. Count violations per category.

3. **Rewrite** — fix each violation while preserving:
   - Technical accuracy (don't change code, commands, or technical terms)
   - Structure (headings, lists, code blocks stay)
   - Tone intent (if the original was casual, keep it casual)
   - Length (aim for same or shorter, never longer)

4. **Report what changed:**
   ```
   Humanized: {file or "pasted text"}

   Changes:
     Em dashes:  {N} removed
     Stock phrases: {N} replaced
     Inflation: {N} deflated
     Triplets: {N} broken
     Sycophancy: {N} cut
     Total: {N} patterns fixed

   Before: {word count}
   After:  {word count}
   ```

5. **If file path:** write the cleaned version back. Show a diff summary.
   **If pasted text:** output the cleaned version directly.

## What NOT to change

- Code blocks and inline code
- Technical terms, library names, CLI commands
- Quotes from other people (attributed quotes stay verbatim)
- Numbers, dates, URLs
- Headings structure (don't merge or split sections)
- Content meaning — only rephrase, never add or remove ideas

## Edge Cases

- **Short text (<50 words):** just apply stock phrase filter, skip structural analysis
- **Already clean:** report "No AI patterns found. Text looks human."
- **Code-heavy docs:** skip code blocks entirely, only process prose sections
- **Non-English text:** apply em dash and structural rules (they're universal), skip English stock phrases
