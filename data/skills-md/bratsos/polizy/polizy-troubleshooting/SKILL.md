---
name: polizy-troubleshooting
description: Debug and fix polizy authorization issues. Use when permission checks fail unexpectedly, errors occur, or authorization behavior is confusing. Covers check algorithm, common issues, and anti-patterns.
license: MIT
metadata:
  author: polizy
  version: "1.0.0"
---

# Polizy Troubleshooting

Debug authorization issues when things don't work as expected.

## When to Apply

- User says "permission check not working"
- User says "user can't access X but should"
- Error messages from polizy
- User confused about why authorization behaves a certain way
- `check()` returns `false` unexpectedly

## Quick Diagnosis Flowchart

```
check() returns false unexpectedly
         │
         ▼
Is the relation in actionToRelations?
    │           │
   NO           YES
    │            │
    ▼            ▼
ADD IT      Is there a group relation?
             │           │
            NO           YES
             │            │
             ▼            ▼
    (Direct check)    Is user in group?
             │            │
             ▼           NO → Check addMember()
    Is tuple           YES
    present?            │
       │                ▼
      NO              Does group have permission?
       │                │
       ▼               NO → Check group's allow()
    Add with          YES
    allow()            │
                       ▼
                  Check depth limit
```

## Common Issues

### 1. Relation Not Mapped to Action

**Symptom:** `check()` returns `false` even with permission granted.

```typescript
// Schema
actionToRelations: {
  view: ["viewer"],  // "editor" missing!
  edit: ["editor"],
}

// Grant
await authz.allow({ who: alice, toBe: "editor", onWhat: doc });

// Check
await authz.check({ who: alice, canThey: "view", onWhat: doc }); // false!
```

**Fix:** Add relation to action's array:

```typescript
actionToRelations: {
  view: ["viewer", "editor"],  // Now editors can view
  edit: ["editor"],
}
```

### 2. Missing Group Relation

**Symptom:** `addMember()` throws error.

```typescript
// Schema missing group type
relations: {
  viewer: { type: "direct" },
}

await authz.addMember({ member: alice, group: team });
// Error: No group relation defined in schema
```

**Fix:** Add group relation:

```typescript
relations: {
  viewer: { type: "direct" },
  member: { type: "group" },  // Add this
}
```

### 3. Missing Hierarchy Propagation

**Symptom:** Parent permission doesn't flow to children.

```typescript
// Schema
relations: {
  parent: { type: "hierarchy" },
  viewer: { type: "direct" },
},
// Missing hierarchyPropagation!

await authz.setParent({ child: doc, parent: folder });
await authz.allow({ who: alice, toBe: "viewer", onWhat: folder });
await authz.check({ who: alice, canThey: "view", onWhat: doc }); // false!
```

**Fix:** Add `hierarchyPropagation`:

```typescript
hierarchyPropagation: {
  view: ["view"],  // Now view propagates
}
```

### 4. User Not in Group

**Symptom:** Group has permission but user can't access.

**Debug:**

```typescript
// Check group membership
const memberships = await authz.listTuples({
  subject: { type: "user", id: "alice" },
  relation: "member",
});
console.log("Alice's groups:", memberships);
```

**Fix:** Add user to group:

```typescript
await authz.addMember({ member: alice, group: team });
```

### 5. Max Depth Exceeded

**Symptom:** Deep group chain returns `false` silently.

**Detect:**

```typescript
const authz = new AuthSystem({
  storage,
  schema,
  throwOnMaxDepth: true,  // Throws instead of silent false
});

try {
  await authz.check({ who: alice, canThey: "view", onWhat: doc });
} catch (error) {
  if (error instanceof MaxDepthExceededError) {
    console.log("Depth exceeded at:", error.depth);
  }
}
```

**Fix:** Increase depth or reduce nesting:

```typescript
const authz = new AuthSystem({
  storage,
  schema,
  defaultCheckDepth: 20,  // Increase from default 10
});
```

### 6. Time-Based Condition Not Valid

**Symptom:** Permission granted with `when` but check fails.

**Debug:**

```typescript
const tuples = await authz.listTuples({
  subject: alice,
  object: doc,
});

for (const tuple of tuples) {
  console.log("Condition:", tuple.condition);
  if (tuple.condition?.validSince) {
    console.log("Starts:", tuple.condition.validSince);
  }
  if (tuple.condition?.validUntil) {
    console.log("Expires:", tuple.condition.validUntil);
  }
}
```

**Common causes:**
- `validSince` is in the future
- `validUntil` is in the past

## Debugging Techniques

### 1. List All Tuples for Subject

```typescript
const tuples = await authz.listTuples({
  subject: { type: "user", id: "alice" },
});

console.log("Alice's permissions:");
for (const tuple of tuples) {
  console.log(`  ${tuple.relation} on ${tuple.object.type}:${tuple.object.id}`);
}
```

### 2. List All Tuples for Object

```typescript
const tuples = await authz.listTuples({
  object: { type: "document", id: "doc1" },
});

console.log("Permissions on doc1:");
for (const tuple of tuples) {
  console.log(`  ${tuple.subject.type}:${tuple.subject.id} is ${tuple.relation}`);
}
```

### 3. Trace Group Membership

```typescript
async function traceGroupPath(userId: string) {
  const user = { type: "user", id: userId };
  const groups: string[] = [];

  const directMemberships = await authz.listTuples({
    subject: user,
    relation: "member",
  });

  for (const tuple of directMemberships) {
    groups.push(`${tuple.object.type}:${tuple.object.id}`);

    // Check nested groups
    const nestedMemberships = await authz.listTuples({
      subject: tuple.object,
      relation: "member",
    });

    for (const nested of nestedMemberships) {
      groups.push(`  → ${nested.object.type}:${nested.object.id}`);
    }
  }

  return groups;
}

console.log("Group path:", await traceGroupPath("alice"));
```

### 4. Trace Hierarchy Path

```typescript
async function traceHierarchyPath(objectType: string, objectId: string) {
  const path: string[] = [`${objectType}:${objectId}`];
  let current = { type: objectType, id: objectId };

  while (true) {
    const parentTuples = await authz.listTuples({
      subject: current,
      relation: "parent",
    });

    if (parentTuples.length === 0) break;

    const parent = parentTuples[0].object;
    path.push(`${parent.type}:${parent.id}`);
    current = parent;
  }

  return path;
}

console.log("Hierarchy:", await traceHierarchyPath("document", "doc1"));
// ["document:doc1", "folder:subfolder", "folder:root"]
```

### 5. Enable Logging

```typescript
const debugLog: string[] = [];

const authz = new AuthSystem({
  storage,
  schema,
  logger: {
    warn: (msg) => {
      debugLog.push(msg);
      console.warn("[Polizy]", msg);
    },
  },
});

// After operations, check debugLog for warnings
```

## Error Reference

| Error | Cause | Fix |
|-------|-------|-----|
| `SchemaError: Relation "X" is not defined` | Using undefined relation | Add relation to schema |
| `SchemaError: No group relation defined` | Missing group type | Add `member: { type: "group" }` |
| `SchemaError: No hierarchy relation defined` | Missing hierarchy type | Add `parent: { type: "hierarchy" }` |
| `MaxDepthExceededError` | Group/hierarchy too deep | Increase depth or flatten |
| `ConfigurationError: storage is required` | Missing storage adapter | Provide storage in constructor |
| `ConfigurationError: schema is required` | Missing schema | Provide schema in constructor |

## Anti-Patterns to Avoid

See [ANTI-PATTERNS.md](references/ANTI-PATTERNS.md) for detailed explanations:

1. **Duplicating permissions across users** - Use groups
2. **Deep group nesting** - Keep 2-3 levels
3. **Generic relation names** - Use semantic names
4. **Checking after action** - Check before
5. **Not handling authorization errors** - Show feedback

## References

- [CHECK-ALGORITHM.md](references/CHECK-ALGORITHM.md) - How check() works internally
- [COMMON-ISSUES.md](references/COMMON-ISSUES.md) - Detailed issue solutions
- [ANTI-PATTERNS.md](references/ANTI-PATTERNS.md) - What NOT to do

## Related Skills

- [polizy-schema](../polizy-schema/SKILL.md) - Schema design
- [polizy-patterns](../polizy-patterns/SKILL.md) - Implementation patterns
