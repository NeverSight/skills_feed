---
name: technical-articles
description: Writing technical articles and blog posts. Use when creating articles in docs/articles/ or blog content explaining patterns, techniques, or lessons learned.
---

# Technical Articles

Two modes: **punchy** for single patterns, **narrative** for explorations.

## Punchy Mode (Default)

For articles explaining one pattern or technique. 30-80 lines.

### Structure

1. **TL;DR**: One sentence, bold the key insight
2. **The Problem**: Show broken code, explain why in 1-2 sentences
3. **The Solution**: Show fixed code, explain in 1-2 sentences
4. **When to Apply**: Bullet list of triggers
5. **Summary**: Table or one-liner

### Example

```markdown
# Parse at the Edges

**TL;DR**: Keep data serialized throughout the system. Parse to rich objects only at the moment you need them.

## The Problem

[code showing parse → serialize → parse → serialize churn]

The rich object was only needed briefly. Every other step was pure churn.

## The Solution

If data enters serialized and leaves serialized, keep it serialized in the middle.

## When to Apply

- Dates: Keep as ISO strings, parse for date pickers
- Markdown: Keep as strings, parse for rendering
- JSON columns: Pass through, parse when accessing fields

## Summary

| Data Type | Keep As    | Parse For          |
| --------- | ---------- | ------------------ |
| Dates     | ISO string | Date math, pickers |
| Markdown  | String     | Rendering          |
```

### Rules

- No preamble ("In this article...")
- Code speaks. Prose explains WHY.
- Short sentences. Fragments fine.
- End with table or one-liner, not conclusion paragraph

### Style Preferences

- **Lead with solution**: Show the pattern first, then explain the problem as context (not the other way around)
- **Blockquotes for key insights**: Put the core insight in a blockquote near the top. Repeat it later if it reinforces understanding.
- **Inline links**: Link to related patterns within the prose, not just in a "References" section at the end
- **Tight prose**: Cut sections that don't add value. If the code is self-explanatory, don't over-explain.

---

## Narrative Mode

For lessons learned, explorations, or when the journey matters. 150-250 lines.

### Structure

1. **Hook**: Drop into a scenario ("I was refactoring X when...")
2. **The Problem**: Show the pain with specific examples
3. **The Realization**: What clicked ("Here's what I realized...")
4. **The Refactor**: Show the change with code
5. **What Changed**: Concrete improvements
6. **The Lesson**: Distill to a principle

### Example Opening

```markdown
# The Case Against catch-all `types.ts`

I was refactoring a database schema system when I opened `types.ts` and stared at 750 lines of type definitions. DateTime types at the top. Validator types in the middle. Everything that vaguely related to "data" lived in this one file.

But here's the weird part: the DateTime functions lived in `datetime.ts`. Why were the types separated from their implementations?
```

### Rules

- Specific details ("750 lines", not "a large file")
- First person is optional—direct statements ("Agent skills aren't complicated") can be stronger than manufactured drama ("I spent way too long thinking...")
- Build to an insight, don't start with it
- Show before/after code
- End with a transferable principle
- Mix short and long sentences
- Use blockquotes to highlight realizations or key insights

---

## Choosing a Mode

| Use Punchy             | Use Narrative         |
| ---------------------- | --------------------- |
| Single pattern or rule | Journey to an insight |
| Reference material     | Lesson learned        |
| Quick lookup           | Story worth telling   |
| 30-80 lines            | 150-250 lines         |

Default to punchy. Use narrative when the story adds value.
