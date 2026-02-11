---
name: polizy-schema
description: Schema design guide for polizy authorization. Use when defining relations, actions, action mappings, hierarchy propagation, or modifying authorization models. Covers direct, group, and hierarchy relation types.
license: MIT
metadata:
  author: polizy
  version: "1.0.0"
---

# Polizy Schema Design

The schema is the heart of polizy. It defines your authorization model: what relationships exist and what actions they enable.

## When to Apply

- User says "design permissions schema" or "define authorization model"
- User asks "what relations do I need for X"
- User says "add new relation" or "add new action"
- User is confused about relation types (direct vs group vs hierarchy)
- User wants to modify their existing schema
- User asks about `defineSchema` or `actionToRelations`

## Priority Table

| Priority | Decision | Impact |
|----------|----------|--------|
| Critical | Choose correct relation types | Wrong type = broken inheritance |
| Critical | Map all actions to relations | Unmapped = always denied |
| Important | Configure hierarchyPropagation | Without it, no parent→child inheritance |
| Important | Use semantic names | Clarity for future maintainers |
| Optional | Keep schema minimal | Start simple, expand as needed |

## Schema Structure

```typescript
import { defineSchema } from "polizy";

const schema = defineSchema({
  // 1. Define relationship types
  relations: {
    owner: { type: "direct" },     // Direct permission
    editor: { type: "direct" },
    viewer: { type: "direct" },
    member: { type: "group" },     // Group membership
    parent: { type: "hierarchy" }  // Parent-child resources
  },

  // 2. Map actions to relations that grant them
  actionToRelations: {
    delete: ["owner"],
    edit: ["owner", "editor"],
    view: ["owner", "editor", "viewer"]
  },

  // 3. Optional: Define hierarchy propagation
  hierarchyPropagation: {
    view: ["view"],   // view on parent → view on child
    edit: ["edit"]    // edit on parent → edit on child
  }
});
```

## Relation Types Quick Reference

| Type | Purpose | Example | Use When |
|------|---------|---------|----------|
| `direct` | User → Resource | alice is owner of doc1 | Specific user needs specific resource access |
| `group` | User → Group membership | alice is member of engineering | Team-based access, organizational structure |
| `hierarchy` | Resource → Parent resource | doc1's parent is folder1 | Folder/file, project/task, inherited permissions |

See [RELATION-TYPES.md](references/RELATION-TYPES.md) for detailed explanations.

## Common Schema Patterns

### Basic Document Access
```typescript
const schema = defineSchema({
  relations: {
    owner: { type: "direct" },
    editor: { type: "direct" },
    viewer: { type: "direct" },
  },
  actionToRelations: {
    delete: ["owner"],
    edit: ["owner", "editor"],
    view: ["owner", "editor", "viewer"],
  },
});
```

### Team-Based Access
```typescript
const schema = defineSchema({
  relations: {
    owner: { type: "direct" },
    editor: { type: "direct" },
    viewer: { type: "direct" },
    member: { type: "group" },  // Required for addMember()
  },
  actionToRelations: {
    manage: ["owner"],
    edit: ["owner", "editor"],
    view: ["owner", "editor", "viewer"],
  },
});
```

### Hierarchical Resources (Folders/Files)
```typescript
const schema = defineSchema({
  relations: {
    owner: { type: "direct" },
    editor: { type: "direct" },
    viewer: { type: "direct" },
    parent: { type: "hierarchy" },  // Required for setParent()
  },
  actionToRelations: {
    delete: ["owner"],
    edit: ["owner", "editor"],
    view: ["owner", "editor", "viewer"],
  },
  hierarchyPropagation: {
    view: ["view"],  // CRITICAL: Without this, no inheritance
    edit: ["edit"],
  },
});
```

### Full-Featured Schema
```typescript
const schema = defineSchema({
  relations: {
    // Direct permissions
    owner: { type: "direct" },
    editor: { type: "direct" },
    viewer: { type: "direct" },
    commenter: { type: "direct" },

    // Group membership
    member: { type: "group" },

    // Hierarchy
    parent: { type: "hierarchy" },
  },
  actionToRelations: {
    // Destructive
    delete: ["owner"],
    transfer: ["owner"],

    // Modification
    edit: ["owner", "editor"],
    comment: ["owner", "editor", "commenter"],

    // Read
    view: ["owner", "editor", "viewer", "commenter"],
  },
  hierarchyPropagation: {
    view: ["view"],
    edit: ["edit"],
    comment: ["comment"],
  },
});
```

## Decision Guide: Which Relation Type?

```
Need to grant access to a specific user on a specific resource?
  → Use "direct" relation (owner, editor, viewer)

Need users to inherit access from a team/department?
  → Use "group" relation (member)
  → Add users to groups with addMember()
  → Grant group access with allow()

Need child resources to inherit parent permissions?
  → Use "hierarchy" relation (parent)
  → Set parent with setParent()
  → Configure hierarchyPropagation
```

## Common Mistakes

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Missing relation in actionToRelations | `check()` returns false | Add relation to the action's array |
| No `member: { type: "group" }` | `addMember()` throws error | Add group relation to schema |
| No `parent: { type: "hierarchy" }` | `setParent()` throws error | Add hierarchy relation to schema |
| Missing hierarchyPropagation | Parent permissions don't flow to children | Add hierarchyPropagation config |
| Using generic names ("access") | Can't distinguish read/write | Use semantic names (viewer, editor) |

## Schema Evolution

When adding to an existing schema:

```typescript
// v1: Basic
const schemaV1 = defineSchema({
  relations: {
    owner: { type: "direct" },
    viewer: { type: "direct" },
  },
  actionToRelations: {
    edit: ["owner"],
    view: ["owner", "viewer"],
  },
});

// v2: Add editor role
const schemaV2 = defineSchema({
  relations: {
    owner: { type: "direct" },
    editor: { type: "direct" },  // NEW
    viewer: { type: "direct" },
  },
  actionToRelations: {
    edit: ["owner", "editor"],  // UPDATED
    view: ["owner", "editor", "viewer"],  // UPDATED
  },
});

// v3: Add groups
const schemaV3 = defineSchema({
  relations: {
    owner: { type: "direct" },
    editor: { type: "direct" },
    viewer: { type: "direct" },
    member: { type: "group" },  // NEW
  },
  actionToRelations: {
    edit: ["owner", "editor"],
    view: ["owner", "editor", "viewer"],
  },
});
```

**Important:** Existing tuples remain valid when you add new relations/actions. No migration needed.

## Related Skills

- [polizy-patterns](../polizy-patterns/SKILL.md) - Implementation patterns
- [polizy-troubleshooting](../polizy-troubleshooting/SKILL.md) - Schema debugging

## References

- [RELATION-TYPES.md](references/RELATION-TYPES.md) - Deep dive into each relation type
- [SCHEMA-EXAMPLES.md](references/SCHEMA-EXAMPLES.md) - 10+ domain-specific schema examples
- [TYPE-SAFETY.md](references/TYPE-SAFETY.md) - TypeScript generics and type inference
