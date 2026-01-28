---
name: word-count-checker
description: Automatically checks word counts of documents when the user mentions word count in relation to a file. Triggers on phrases like "Check the word count of X", "Stop when the word count is N", or similar references to document word counts. Use this skill proactively whenever word count is mentioned with a document reference.
---

# Word Count Checker

## Overview

This skill enables automatic word count checking when word count is mentioned in relation to a document. Instead of requiring explicit requests, trigger this skill whenever the user references word count alongside a document.

## When to Use This Skill

Trigger this skill whenever the user mentions word count in relation to a document, including phrases like:
- "Check the word count of [filename]"
- "What's the word count of [filename]"
- "Stop when the word count is [number]"
- "Keep the word count under [number]"
- "How many words are in [filename]"
- Any similar reference to word count with a document

## How to Use

When word count is mentioned with a document reference:

1. **Identify the target file** from the user's message (e.g., `article.md`, `chapter1.md`)

2. **Run the word count command** using Bash:
   ```bash
   wc -w <filename>
   ```

3. **Interpret the context**:
   - **Checking**: If the user asks to check word count, report the current count
   - **Monitoring**: If the user mentions a target word count (e.g., "stop when word count is 4500"), compare the current count to the target and inform the user whether the goal has been met
   - **Writing**: If generating or editing content with a word count constraint, check periodically and adjust as needed

4. **Report clearly**: Present the word count information in a natural, contextual way based on the user's request

## Examples

**User**: "Check the word count of article.md"
**Action**: Run `wc -w article.md` and report: "article.md has 3,245 words."

**User**: "Keep writing chapter1.md until it reaches 5000 words"
**Action**: Periodically run `wc -w chapter1.md` while writing, and stop when the count reaches or exceeds 5000 words.

**User**: "What's the word count of my draft.md?"
**Action**: Run `wc -w draft.md` and report the count naturally in response.
