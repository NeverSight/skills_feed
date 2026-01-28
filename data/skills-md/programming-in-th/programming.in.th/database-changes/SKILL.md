---
name: database-changes
description: Use when modifying Prisma schema or database queries. Ensures proper migrations, type safety, and query performance.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

See [Database patterns](../../docs/database-patterns.md) for full reference.

**Schema changes**:
```bash
pnpm prisma migrate dev --name descriptive_name
pnpm check-types
```

**Query rules**:
- Always `import { prisma } from '@/lib/prisma'`
- Always use `select` for specific fields
- Always paginate with `take`/`skip`
- Avoid N+1: use `include` or batch with `where: { id: { in: ids } }`

**Models**: User, Task, Submission, Assessment, Category, Tag, Bookmark
