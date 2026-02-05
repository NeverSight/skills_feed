---
name: polizy-patterns
description: Implementation patterns for polizy authorization. Use when implementing team access, folder inheritance, field-level permissions, temporary access, revocation, or any specific authorization scenario.
license: MIT
metadata:
  author: polizy
  version: "1.0.0"
---

# Polizy Implementation Patterns

Copy-paste patterns for common authorization scenarios.

## When to Apply

- User says "how do I implement X"
- User says "give team access to project"
- User says "make files inherit folder permissions"
- User says "grant temporary access"
- User says "revoke all permissions"
- User wants to implement a specific authorization scenario

## Pattern Selection Guide

| Scenario | Pattern | Reference |
|----------|---------|-----------|
| Specific user → specific resource | Direct Permissions | [DIRECT-PERMISSIONS.md](references/DIRECT-PERMISSIONS.md) |
| Team/group access | Group Access | [GROUP-ACCESS.md](references/GROUP-ACCESS.md) |
| Folder/file inheritance | Hierarchy | [HIERARCHY.md](references/HIERARCHY.md) |
| Sensitive fields (salary, PII) | Field-Level | [FIELD-LEVEL.md](references/FIELD-LEVEL.md) |
| Contractor/expiring access | Time-Limited | [TIME-LIMITED.md](references/TIME-LIMITED.md) |
| Removing access | Revocation | [REVOCATION.md](references/REVOCATION.md) |
| Tenant isolation | Multi-Tenant | [MULTI-TENANT.md](references/MULTI-TENANT.md) |

---

## Pattern 1: Direct Permissions

Grant specific user access to specific resource.

```typescript
// Grant permission
await authz.allow({
  who: { type: "user", id: "alice" },
  toBe: "owner",
  onWhat: { type: "document", id: "doc1" }
});

// Check permission
const canEdit = await authz.check({
  who: { type: "user", id: "alice" },
  canThey: "edit",
  onWhat: { type: "document", id: "doc1" }
});
```

---

## Pattern 2: Team-Based Access

Grant access through group membership.

```typescript
// 1. Add users to team
await authz.addMember({
  member: { type: "user", id: "alice" },
  group: { type: "team", id: "engineering" }
});

await authz.addMember({
  member: { type: "user", id: "bob" },
  group: { type: "team", id: "engineering" }
});

// 2. Grant team access to resource
await authz.allow({
  who: { type: "team", id: "engineering" },
  toBe: "editor",
  onWhat: { type: "project", id: "project1" }
});

// 3. Team members can now access
const canAliceEdit = await authz.check({
  who: { type: "user", id: "alice" },
  canThey: "edit",
  onWhat: { type: "project", id: "project1" }
}); // true
```

**Schema requirement:**
```typescript
relations: {
  member: { type: "group" },  // Required!
  editor: { type: "direct" },
}
```

---

## Pattern 3: Folder/File Hierarchy

Inherit permissions from parent resources.

```typescript
// 1. Set up hierarchy
await authz.setParent({
  child: { type: "document", id: "doc1" },
  parent: { type: "folder", id: "folder1" }
});

// 2. Grant access at folder level
await authz.allow({
  who: { type: "user", id: "alice" },
  toBe: "viewer",
  onWhat: { type: "folder", id: "folder1" }
});

// 3. Document inherits folder permission
const canView = await authz.check({
  who: { type: "user", id: "alice" },
  canThey: "view",
  onWhat: { type: "document", id: "doc1" }
}); // true
```

**Schema requirement:**
```typescript
relations: {
  parent: { type: "hierarchy" },  // Required!
  viewer: { type: "direct" },
},
hierarchyPropagation: {
  view: ["view"],  // CRITICAL: Without this, no inheritance!
}
```

---

## Pattern 4: Field-Level Permissions

Protect sensitive fields within records.

```typescript
// Grant general record access
await authz.allow({
  who: { type: "user", id: "employee" },
  toBe: "viewer",
  onWhat: { type: "profile", id: "emp123" }
});

// Grant specific field access
await authz.allow({
  who: { type: "user", id: "hr_manager" },
  toBe: "viewer",
  onWhat: { type: "profile", id: "emp123#salary" }
});

// Employee can view profile, but not salary
await authz.check({
  who: { type: "user", id: "employee" },
  canThey: "view",
  onWhat: { type: "profile", id: "emp123" }
}); // true

await authz.check({
  who: { type: "user", id: "employee" },
  canThey: "view",
  onWhat: { type: "profile", id: "emp123#salary" }
}); // false

// HR can view salary
await authz.check({
  who: { type: "user", id: "hr_manager" },
  canThey: "view",
  onWhat: { type: "profile", id: "emp123#salary" }
}); // true
```

---

## Pattern 5: Temporary Access

Grant time-limited permissions.

```typescript
// Access valid for 30 days
await authz.allow({
  who: { type: "user", id: "contractor" },
  toBe: "editor",
  onWhat: { type: "project", id: "project1" },
  when: {
    validSince: new Date(),
    validUntil: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000)
  }
});

// Scheduled future access
await authz.allow({
  who: { type: "user", id: "new_hire" },
  toBe: "viewer",
  onWhat: { type: "onboarding", id: "docs" },
  when: {
    validSince: new Date("2024-02-01")  // Starts Feb 1
  }
});
```

---

## Pattern 6: Revocation

Remove permissions.

```typescript
// Remove specific permission
await authz.disallowAllMatching({
  who: { type: "user", id: "bob" },
  was: "editor",
  onWhat: { type: "document", id: "doc1" }
});

// Remove all user permissions on a resource
await authz.disallowAllMatching({
  who: { type: "user", id: "bob" },
  onWhat: { type: "document", id: "doc1" }
});

// Remove all permissions on a resource (when deleting it)
await authz.disallowAllMatching({
  onWhat: { type: "document", id: "doc1" }
});

// Remove user from group
await authz.removeMember({
  member: { type: "user", id: "alice" },
  group: { type: "team", id: "engineering" }
});
```

---

## Pattern 7: Listing Accessible Objects

Find what a user can access.

```typescript
// List all documents alice can access
const result = await authz.listAccessibleObjects({
  who: { type: "user", id: "alice" },
  ofType: "document"
});

// Result:
// {
//   accessible: [
//     { object: { type: "document", id: "doc1" }, actions: ["edit", "view", "delete"] },
//     { object: { type: "document", id: "doc2" }, actions: ["view"] },
//   ]
// }

// Filter by action
const editableOnly = await authz.listAccessibleObjects({
  who: { type: "user", id: "alice" },
  ofType: "document",
  canThey: "edit"  // Only return editable documents
});
```

---

## Pattern 8: Combining Patterns

Real apps often combine multiple patterns:

```typescript
// Organizational structure (groups)
await authz.addMember({ member: alice, group: frontend });
await authz.addMember({ member: frontend, group: engineering });

// Resource hierarchy
await authz.setParent({ child: codeFile, parent: srcFolder });
await authz.setParent({ child: srcFolder, parent: projectRoot });

// Team access at project level
await authz.allow({ who: engineering, toBe: "editor", onWhat: projectRoot });

// Alice can now edit codeFile through:
// alice → member → frontend → member → engineering → editor → projectRoot ← parent ← srcFolder ← parent ← codeFile

await authz.check({ who: alice, canThey: "edit", onWhat: codeFile }); // true
```

---

## Common Mistakes

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Missing `member: { type: "group" }` | `addMember()` throws | Add group relation to schema |
| Missing `parent: { type: "hierarchy" }` | `setParent()` throws | Add hierarchy relation to schema |
| Missing `hierarchyPropagation` | Parent permissions don't flow | Add propagation config |
| Relation not in `actionToRelations` | `check()` returns false | Add relation to action's array |
| Checking wrong action | `check()` returns false | Verify action name matches schema |

---

## References

Each pattern has detailed documentation:

- [DIRECT-PERMISSIONS.md](references/DIRECT-PERMISSIONS.md) - Simple user-resource access
- [GROUP-ACCESS.md](references/GROUP-ACCESS.md) - Teams, departments, nested groups
- [HIERARCHY.md](references/HIERARCHY.md) - Folders, projects, inheritance
- [FIELD-LEVEL.md](references/FIELD-LEVEL.md) - PII, sensitive data protection
- [TIME-LIMITED.md](references/TIME-LIMITED.md) - Contractors, expiring access
- [REVOCATION.md](references/REVOCATION.md) - Removing access patterns
- [MULTI-TENANT.md](references/MULTI-TENANT.md) - Tenant isolation strategies

## Related Skills

- [polizy-schema](../polizy-schema/SKILL.md) - Schema design
- [polizy-troubleshooting](../polizy-troubleshooting/SKILL.md) - When things go wrong
