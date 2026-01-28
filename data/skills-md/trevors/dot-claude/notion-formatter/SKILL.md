---
name: notion-formatter
description: Format markdown content for Notion import with proper syntax for toggles, code blocks, and tables. Use when formatting responses for Notion, creating Notion-compatible documentation, or preparing markdown for Notion paste/import.
---

# Notion Formatter

## Quick Start

Notion is a **block-based editor**, not a pure markdown system. It supports standard markdown for basic formatting (headers, lists, bold, italic, inline code), but many features require Notion-specific syntax or manual creation. This skill helps you format markdown optimally for Notion import by applying the right syntax, annotating manual steps, and warning about limitations.

## Core Workflow

### 1. Identify Your Content Type

- **Claude response**: Formatting text I just generated for Notion
- **Documentation**: Converting existing `.md` files to Notion format
- **Mixed content**: Markdown with images, code, tables

### 2. Apply Standard Markdown (What Works Everywhere)

Use standard markdown for these features—they'll convert automatically when pasted into Notion:

```markdown
**bold** _italic_ `inline code` ~strikethrough~

# Heading 1

## Heading 2

### Heading 3

- Bullet point
- Another point
  - Nested bullet

1. Numbered item
2. Second item

[] Checkbox item
```

### 3. Use Notion-Specific Syntax

**Key distinction:** Use `>` for toggles (collapsible sections), `"` for blockquotes. See REFERENCE.md for detailed syntax and examples of all features.

**Quick syntax:**

```markdown
> Toggle heading
> Hidden content here

" Blockquote text
```

```javascript
code here
```

| Column 1 | Column 2 |
| -------- | -------- |
| Data 1   | Data 2   |

![alt](https://example.com/image.png)

### 4. Annotate Manual Steps

Mark features that need manual creation in Notion with annotations:

- **Equations:** Use `[NOTION: Recreate equation manually]`
- **Other unsupported features:** Use `[NOTION: Feature name here]`

### 5. Verify Output

Before sending to Notion, check:

- [ ] Standard markdown is correct (headers, lists, formatting)
- [ ] Toggle syntax uses `>` followed by space (greater-than space)
- [ ] Blockquotes use `"` followed by space (quote space)
- [ ] Code blocks have language labels
- [ ] Images use full URLs, not local paths
- [ ] Tables use pipe syntax
- [ ] Manual step annotations are clear

## Examples

### Example 1: Formatting a Response

If I generate a response with code and a table, format it with language-labeled code blocks and pipe-syntax tables.

**Code block example:**

```python
# Example code
def process_data(items):
    return [x * 2 for x in items]
```

**Table example:**

| Input | Output |
| ----- | ------ |
| 1     | 2      |
| 5     | 10     |

### Example 2: Converting Documentation

For multi-section documents, use toggles to create collapsible sections with `> Section Title` and content indented underneath.

## Best Practices

- **Keep it simple**: Avoid deeply nested structures
- **Test tables first**: If a table is complex, consider creating it manually in Notion
- **Image URLs**: Always verify images are accessible online
- **Break large docs**: Paste in chunks if a document fails to import entirely
- **Manual polish**: Always review in Notion after paste—fix extra line breaks and language detection

---

For detailed syntax, gotchas, and troubleshooting, see REFERENCE.md
