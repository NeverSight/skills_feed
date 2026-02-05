---
name: text-statistics
description: Analyze text for word count, reading time, complexity metrics, and readability scores. Use when user asks to analyze document length, calculate reading time, or assess text complexity.
---

# Text Statistics

Quick analysis of text metrics including word count, reading time, complexity, and readability.

## When to Use

Invoke when user:
- Asks "how long is this text?"
- Wants reading time estimates
- Needs complexity or readability scores
- Says "analyze this document" or "how many words?"

## Core Capabilities

### 1. Basic Metrics

**Word Count**
- Total words
- Unique words
- Average word length

**Character Count**
- With and without spaces
- Alphanumeric vs punctuation

**Reading Time**
- Assuming 200-250 words/minute
- Adjusted for complexity

### 2. Complexity Analysis

**Sentence Structure**
- Average sentence length
- Sentence length variance
- Simple vs complex sentences

**Vocabulary**
- Unique word ratio
- Long word percentage (7+ chars)
- Syllable count estimates

### 3. Readability Scores

**Flesch Reading Ease**
- 0-100 scale
- Higher = easier to read

**Grade Level Estimate**
- US grade level equivalent
- Based on sentence/word complexity

## Output Format

```
TEXT STATISTICS REPORT
=====================

Basic Metrics:
- Word Count: X (Y unique)
- Character Count: X (Y without spaces)
- Reading Time: X-Y minutes

Complexity:
- Avg Sentence Length: X words
- Long Words (7+ chars): X%
- Vocabulary Richness: X%

Readability:
- Flesch Score: X/100 (Level)
- Grade Level: X

Interpretation:
[Brief assessment of text complexity and audience appropriateness]
```

## Examples

See `references/examples.md` for analyzed samples.

## Integration

Standalone skill. Useful before:
- Prose Polish (get baseline metrics)
- Content generation (target metrics)
