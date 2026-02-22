---
name: tiptap-dev
description: Expert guidance for building rich text editors with Tiptap - a headless, framework-agnostic editor built on ProseMirror. Use when creating custom nodes, marks, or extensions for Tiptap, implementing input rules or paste rules, working with the Tiptap commands API, building React integrations with useEditor, extending existing extensions, or creating custom node views.
---

# Tiptap Development Expert

Expert guidance for building rich text editors with Tiptap - a headless, framework-agnostic editor built on ProseMirror.

**See also:** `tiptap-editor` skill — VMark-specific Tiptap API patterns (commands, node traversal, selection handling). Use `tiptap-dev` for general Tiptap/ProseMirror development, and `tiptap-editor` for VMark-specific editor integration.

## When to Use This Skill

- Creating custom nodes, marks, or extensions for Tiptap
- Implementing input rules or paste rules
- Working with the Tiptap commands API
- Building React integrations with useEditor
- Extending existing extensions
- Creating custom node views
- Understanding the schema and content model

## Reference Files

| File | Description |
|------|-------------|
| `references/extensions.md` | Extension types (Node, Mark, Extension), creation patterns |
| `references/commands-and-api.md` | Commands API, editor API, chaining |
| `references/input-paste-rules.md` | Input rules and paste rules |
| `references/react-integration.md` | React-specific hooks and components |
| `references/schema.md` | Schema properties, content patterns |
| `references/examples.md` | Complete working examples |

## Quick Reference

### Extension Types

```typescript
// Functionality extension (no schema)
Extension.create({ name: 'myExtension', addKeyboardShortcuts() { ... } })

// Node extension (block content)
Node.create({ name: 'myNode', group: 'block', content: 'inline*' })

// Mark extension (inline formatting)
Mark.create({ name: 'myMark', parseHTML() { ... }, renderHTML() { ... } })
```

### Command Chaining

```typescript
editor.chain().focus().toggleBold().run()
editor.can().chain().focus().toggleBold().run() // dry run
```

### React Integration

```typescript
const editor = useEditor({
  extensions: [StarterKit],
  content: '<p>Hello</p>',
  immediatelyRender: false, // for SSR
})
```

## Core Concepts

1. **Headless Architecture**: Tiptap provides logic, you control rendering
2. **Extension-Based**: Everything is an extension (nodes, marks, functionality)
3. **ProseMirror Foundation**: Built on ProseMirror, full access to its APIs
4. **Schema-Driven**: Content model defined by node/mark schemas
5. **Command Pattern**: All operations via chainable commands
