---
name: velt-crdt-best-practices
description: Velt CRDT (Yjs) collaborative editing best practices for real-time applications. This skill should be used when implementing collaborative features using Velt CRDT stores, integrating with editors like Tiptap, BlockNote, CodeMirror, or ReactFlow, or debugging sync issues. Triggers on tasks involving real-time collaboration, multiplayer editing, CRDT stores, or Velt SDK integration.
license: MIT
metadata:
  author: velt
  version: "2.0.0"
---

# Velt CRDT Best Practices

Comprehensive best practices guide for implementing real-time collaborative editing with Velt CRDT (Yjs), maintained by Velt. Contains 33 rules across 5 categories, prioritized by impact to guide automated code generation and debugging.

## When to Apply

Reference these guidelines when:
- Setting up Velt client and CRDT stores
- Integrating with Tiptap, BlockNote, CodeMirror, or ReactFlow
- Implementing real-time synchronization
- Managing version history and checkpoints
- Debugging collaboration or sync issues
- Testing multi-user collaboration

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Core CRDT | CRITICAL | `core-` |
| 2 | Tiptap Integration | CRITICAL | `tiptap-` |
| 3 | BlockNote Integration | HIGH | `blocknote-` |
| 4 | CodeMirror Integration | HIGH | `codemirror-` |
| 5 | ReactFlow Integration | HIGH | `reactflow-` |

## Quick Reference

### 1. Core CRDT (CRITICAL)

- `core-install` - Install correct CRDT packages for your framework
- `core-velt-init` - Initialize Velt client before creating stores
- `core-store-create-react` - Use useVeltCrdtStore hook for React
- `core-store-create-vanilla` - Use createVeltStore for non-React
- `core-store-types` - Choose correct store type (text/array/map/xml)
- `core-store-subscribe` - Subscribe to store changes for remote updates
- `core-store-update` - Use update() method to modify values
- `core-version-save` - Save named version checkpoints
- `core-encryption` - Use custom encryption provider for sensitive data
- `core-debug-storemap` - Use VeltCrdtStoreMap for runtime debugging
- `core-debug-testing` - Test with multiple browser profiles

### 2. Tiptap Integration (CRITICAL)

- `tiptap-install` - Install Tiptap CRDT packages
- `tiptap-setup-react` - Use useVeltTiptapCrdtExtension for React
- `tiptap-setup-vanilla` - Use createVeltTipTapStore for non-React
- `tiptap-disable-history` - Disable Tiptap history to prevent conflicts
- `tiptap-editor-id` - Use unique editorId per instance
- `tiptap-cursor-css` - Add CSS for collaboration cursors
- `tiptap-testing` - Test collaboration with multiple users

### 3. BlockNote Integration (HIGH)

- `blocknote-install` - Install BlockNote CRDT package
- `blocknote-setup-react` - Use useVeltBlockNoteCrdtExtension
- `blocknote-editor-id` - Use unique editorId per instance
- `blocknote-testing` - Test collaboration with multiple users

### 4. CodeMirror Integration (HIGH)

- `codemirror-install` - Install CodeMirror CRDT packages
- `codemirror-setup-react` - Use useVeltCodeMirrorCrdtExtension for React
- `codemirror-setup-vanilla` - Use createVeltCodeMirrorStore for non-React
- `codemirror-ycollab` - Wire yCollab extension with store's Yjs objects
- `codemirror-editor-id` - Use unique editorId per instance
- `codemirror-testing` - Test collaboration with multiple users

### 5. ReactFlow Integration (HIGH)

- `reactflow-install` - Install ReactFlow CRDT package
- `reactflow-setup-react` - Use useVeltReactFlowCrdtExtension
- `reactflow-handlers` - Use CRDT handlers for node/edge changes
- `reactflow-editor-id` - Use unique editorId per instance
- `reactflow-testing` - Test collaboration with multiple users

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/shared/core/core-install.md
rules/shared/tiptap/tiptap-disable-history.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Verification checklist
- Source pointer to Velt documentation

## Compiled Documents

- `AGENTS.md` — Compressed index of all rules with file paths (start here)
- `AGENTS.full.md` — Full verbose guide with all rules expanded inline
