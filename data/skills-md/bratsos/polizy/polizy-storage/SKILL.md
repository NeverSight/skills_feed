---
name: polizy-storage
description: Storage adapter setup for polizy authorization. Use when configuring InMemory, Prisma, or custom storage adapters, database setup, or performance optimization.
license: MIT
metadata:
  author: polizy
  version: "1.0.0"
---

# Polizy Storage

Storage adapters handle persistence of authorization tuples.

## When to Apply

- User asks "set up database storage"
- User asks "use Prisma with polizy"
- User asks "create custom storage adapter"
- User asks about "production storage"
- User has performance concerns with authorization

## Adapter Comparison

| Feature | InMemoryStorageAdapter | PrismaAdapter |
|---------|------------------------|---------------|
| Persistence | No (RAM only) | Yes (database) |
| Multi-instance | No | Yes |
| Setup | Zero config | Prisma model required |
| Performance | Fastest | Good with indexes |
| Use case | Testing, dev | Production |

## Quick Setup

### InMemory (Development/Testing)

```typescript
import { AuthSystem, InMemoryStorageAdapter } from "polizy";

const storage = new InMemoryStorageAdapter();
const authz = new AuthSystem({ storage, schema });
```

### Prisma (Production)

```typescript
import { AuthSystem } from "polizy";
import { PrismaAdapter } from "polizy/prisma-storage";
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();
const storage = PrismaAdapter(prisma);
const authz = new AuthSystem({ storage, schema });
```

**Requires Prisma model** - see [PRISMA-ADAPTER.md](references/PRISMA-ADAPTER.md)

## InMemoryStorageAdapter

### When to Use

- Unit tests
- Development environment
- Single-process applications
- Prototyping

### Behavior

- Data stored in JavaScript `Map`
- Lost on process restart
- No network latency
- Fastest possible reads

### Testing Example

```typescript
import { describe, it, beforeEach } from "node:test";
import { AuthSystem, InMemoryStorageAdapter, defineSchema } from "polizy";

describe("authorization", () => {
  let authz: AuthSystem<typeof schema>;

  beforeEach(() => {
    // Fresh storage for each test
    const storage = new InMemoryStorageAdapter();
    authz = new AuthSystem({ storage, schema });
  });

  it("grants access correctly", async () => {
    await authz.allow({
      who: { type: "user", id: "alice" },
      toBe: "owner",
      onWhat: { type: "doc", id: "doc1" }
    });

    const result = await authz.check({
      who: { type: "user", id: "alice" },
      canThey: "edit",
      onWhat: { type: "doc", id: "doc1" }
    });

    assert.strictEqual(result, true);
  });
});
```

## PrismaAdapter

### When to Use

- Production environments
- Multi-instance deployments
- Need audit trail
- Data must survive restarts

### Setup Steps

1. **Install dependencies**
   ```bash
   npm install @prisma/client
   npm install -D prisma
   ```

2. **Add Prisma model** (see [PRISMA-ADAPTER.md](references/PRISMA-ADAPTER.md))

3. **Run migrations**
   ```bash
   npx prisma migrate dev --name add_polizy
   ```

4. **Use adapter**
   ```typescript
   import { PrismaAdapter } from "polizy/prisma-storage";
   const storage = PrismaAdapter(prisma);
   ```

## Storage Interface

All adapters implement:

```typescript
interface StorageAdapter<S, O> {
  write(tuples: InputTuple[]): Promise<StoredTuple[]>;
  delete(filter: DeleteFilter): Promise<number>;
  findTuples(filter: TupleFilter): Promise<StoredTuple[]>;
  findSubjects(object, relation, options?): Promise<Subject[]>;
  findObjects(subject, relation, options?): Promise<AnyObject[]>;
}
```

## Common Patterns

### Shared Storage Instance

```typescript
// storage.ts
import { InMemoryStorageAdapter } from "polizy";
// or: import { PrismaAdapter } from "polizy/prisma-storage";

export const storage = new InMemoryStorageAdapter();
// or: export const storage = PrismaAdapter(prisma);

// auth.ts
import { AuthSystem } from "polizy";
import { storage } from "./storage";
import { schema } from "./schema";

export const authz = new AuthSystem({ storage, schema });
```

### Environment-Based Selection

```typescript
import { AuthSystem, InMemoryStorageAdapter } from "polizy";
import { PrismaAdapter } from "polizy/prisma-storage";
import { PrismaClient } from "@prisma/client";

function createStorage() {
  if (process.env.NODE_ENV === "test") {
    return new InMemoryStorageAdapter();
  }

  const prisma = new PrismaClient();
  return PrismaAdapter(prisma);
}

const storage = createStorage();
export const authz = new AuthSystem({ storage, schema });
```

## Performance Considerations

| Concern | Solution |
|---------|----------|
| Slow reads | Add database indexes |
| Too many queries | Reduce group nesting depth |
| Large tuple counts | Periodic cleanup of expired tuples |
| Batch operations | Use `writeTuple` with parallel Promise.all |

## Common Issues

| Issue | Solution |
|-------|----------|
| Data lost on restart | Switch from InMemory to Prisma |
| "Table doesn't exist" | Run `npx prisma migrate deploy` |
| Slow checks | Reduce group/hierarchy depth |
| Memory growing | Clean up expired conditional tuples |

## References

- [PRISMA-ADAPTER.md](references/PRISMA-ADAPTER.md) - Full Prisma setup
- [CUSTOM-ADAPTERS.md](references/CUSTOM-ADAPTERS.md) - Building custom adapters
- [PERFORMANCE.md](references/PERFORMANCE.md) - Optimization strategies

## Related Skills

- [polizy-setup](../polizy-setup/SKILL.md) - Initial setup
- [polizy-troubleshooting](../polizy-troubleshooting/SKILL.md) - Debugging
