---
name: en-to-zh-translator
description: "Translate English text files (.txt, .md) to Chinese for language learning and translation practice. Use when the user asks to translate a text file to Chinese, create a Chinese version of an English document, or generate bilingual materials for translation training. The translation preserves sentence structure and combines broken sentences into complete lines."
---

# English to Chinese Translator

## Overview

Translates English text files to natural Chinese while preserving sentence structure for effective bidirectional translation practice. Combines broken sentences into complete lines. Output files use the `_zh` suffix (e.g., `document.txt` → `document_zh.txt`).

## Translation Workflow

1. **Read the source file** - Read the full English text file to understand context and tone
2. **Translate to Chinese** - Apply translation guidelines (see below)
3. **Write translated file** - Create `{original_name}_zh.{ext}` in the same directory

## Translation Guidelines

### Core Principles

1. **Natural but not ornate** - Translate into flowing, natural Chinese, but avoid overly literary or poetic language. The goal is clarity and reversibility.

2. **Preserve sentence structure** - Maintain the original English sentence structure where possible. This makes it easier to translate back to English for practice.

   ✓ Good: "I love learning foreign languages." → "我喜欢学习外语。"
   ✗ Avoid: Complex restructuring that loses alignment with source

3. **Combine broken sentences** - When an English sentence is broken across multiple lines, combine it into one complete line in Chinese. Preserve paragraph breaks and meaningful structural line breaks.

4. **Handle special elements**:
   - Stage directions: `(Laughter)` → `（笑声）`, `(Applause)` → `（掌声）`
   - Quotes: Preserve quoted speech structure
   - Numbers: Keep numerals as-is (don't convert to Chinese characters)

### Quality Checklist

Before writing the output, verify:
- [ ] Chinese flows naturally but isn't overly abstract
- [ ] Broken sentences are combined into complete lines
- [ ] Paragraph breaks are preserved
- [ ] Special elements (stage directions, quotes) are properly handled
- [ ] Meaning is preserved accurately without over-interpretation

### Examples

**Input (file.txt):**
```
I love learning foreign languages.

In fact, I love it so much that I like
to learn a new language every two years,
```

**Output (file_zh.txt):**
```
我喜欢学习外语。

事实上，我太喜欢了，以至于我想每两年学习一门新语言，
```

## Usage

The skill is triggered when users request:
- "Translate this file to Chinese"
- "Create a Chinese version of {filename}"
- "Help me practice translation with this text"

The skill handles `.txt` and `.md` files.
