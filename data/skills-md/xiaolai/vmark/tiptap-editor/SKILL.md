---
name: tiptap-editor
description: Tiptap editor API patterns for vmark WYSIWYG development. Use when working with editor commands, node traversal, selection handling, or format operations.
---

# Tiptap Editor API Patterns

## Overview

This skill documents proper Tiptap API usage patterns for vmark development. It helps distinguish when to use Tiptap's high-level API vs direct ProseMirror access.

## When to Use Tiptap API

**Always prefer Tiptap API for:**
- Format commands (bold, italic, underline, etc.)
- Block type changes (heading, paragraph, code block)
- List operations (bullet, ordered, toggle, indent/outdent)
- Table operations via Tiptap table extension
- Content insertion and replacement
- Editor state queries (`isActive`, `getAttributes`)

**Tiptap patterns to use:**
```typescript
// Direct commands
editor.commands.toggleBold()
editor.commands.setHeading({ level: 2 })
editor.commands.setContent(doc, { emitUpdate: false })

// Chained commands (for multiple operations)
editor.chain().focus().setHeading({ level: 2 }).run()
editor.chain().focus().toggleMark("underline").run()

// State queries
editor.isActive("blockquote")
editor.isActive("heading", { level: 2 })
editor.getAttributes("link")
```

## When Direct ProseMirror is Appropriate

**Use ProseMirror directly for:**
- Markdown conversion layer (`proseMirrorToMdast.ts`, `mdastToProseMirror.ts`)
- Multi-cursor/selection subclassing (`MultiSelection.ts`)
- Custom node views
- Low-level transaction manipulation
- Schema-level operations

## Known Issues in vmark

### 1. cursorHandlers.ts Block Boundary Issue
`src/hooks/mcpBridge/cursorHandlers.ts` uses `doc.textContent` which flattens the document and loses block boundaries. The correct approach is to use `$pos` helpers:

```typescript
// WRONG - loses block structure
const text = doc.textContent;

// RIGHT - respects block boundaries
const $pos = doc.resolve(from);
const currentNode = $pos.parent;
const blockStart = $pos.before($pos.depth);
const blockEnd = $pos.after($pos.depth);
```

### 2. Cursor Sync Drift After WYSIWYG Edits
`sourceLine` attributes are only set on initial parse. After WYSIWYG edits that add/remove blocks, line numbers no longer match the source. This is a known limitation.

### 3. HtmlNodeView.ts Store Issue
`src/plugins/markdownArtifacts/HtmlNodeView.ts` writes cursor info to wrong store.

## References

- `references/patterns.md` - Detailed API patterns and $pos usage
- `references/examples.md` - Real code examples from vmark codebase

## Workflow

1. Identify operation type (format, block, selection, traversal)
2. Check if Tiptap has a built-in command for it
3. Use `editor.commands.xxx()` for single operations
4. Use `editor.chain().focus().xxx().run()` when focus is needed or chaining
5. For node traversal, use `doc.resolve(pos)` to get `$pos` helpers
6. For state queries, use `editor.isActive()` or `editor.getAttributes()`
