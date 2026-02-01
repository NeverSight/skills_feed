---
name: database-schema-manager
description:
  Manages LibSQL/Turso database schemas with Zod validation, creates migrations,
  and ensures type-safe database operations. Use when creating database tables,
  writing migrations, or implementing schema validation.
---

# Database Schema Manager

## Quick Start

This skill manages LibSQL/Turso database schemas:

1. **Schema design**: Create tables with proper types and indexes
2. **Zod validation**: Schema-first approach with type inference
3. **Migrations**: Version-controlled schema changes
4. **Type safety**: Ensure TypeScript types match database schema

### When to Use

- Creating new database tables
- Writing database migrations
- Implementing schema validation
- Need type-safe database operations

## Database Connection

```typescript
// src/lib/db.ts
import { createClient } from '@libsql/client';

export const db = createClient({
  url: import.meta.env.VITE_TURSO_DATABASE_URL,
  authToken: import.meta.env.VITE_TURSO_AUTH_TOKEN,
});

// Test connection
export async function testConnection(): Promise<boolean> {
  try {
    await db.execute('SELECT 1');
    return true;
  } catch (error) {
    console.error('Database connection failed:', error);
    return false;
  }
}
```

## Table Creation Pattern

```sql
-- migrations/001_create_projects_table.sql
CREATE TABLE IF NOT EXISTS projects (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT,
  genre TEXT NOT NULL,
  target_word_count INTEGER NOT NULL,
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL
) STRICT;

CREATE INDEX idx_projects_created_at ON projects(created_at DESC);
CREATE INDEX idx_projects_genre ON projects(genre);
```

**Key Guidelines**:

- `TEXT PRIMARY KEY` for UUID identifiers
- `INTEGER` for timestamps (Unix milliseconds)
- `TEXT` for enums (validated by Zod, not database constraints)
- `STRICT` mode for type safety
- Indexes for frequently queried columns

## Zod Validation (Schema-First)

```typescript
// src/features/projects/types/project.schema.ts
import { z } from 'zod';

// Zod schema (source of truth)
export const projectSchema = z.object({
  id: z.string().uuid(),
  title: z.string().min(1).max(200),
  description: z.string().max(1000).optional(),
  genre: z.enum(['fantasy', 'scifi', 'mystery', 'romance', 'thriller']),
  targetWordCount: z.number().int().positive().max(1000000),
  createdAt: z.number().int().positive(),
  updatedAt: z.number().int().positive(),
});

// Infer TypeScript type from Zod schema
export type Project = z.infer<typeof projectSchema>;

// Partial schema for updates (all fields optional except id)
export const projectUpdateSchema = projectSchema
  .partial()
  .required({ id: true });
export type ProjectUpdate = z.infer<typeof projectUpdateSchema>;

// Schema for creation (omit id, timestamps)
export const projectCreateSchema = projectSchema.omit({
  id: true,
  createdAt: true,
  updatedAt: true,
});
export type ProjectCreate = z.infer<typeof projectCreateSchema>;
```

## Type-Safe Database Operations

### Service Pattern with Validation

```typescript
// src/features/projects/services/projectService.ts
import { db } from '@/lib/db';
import {
  projectSchema,
  projectCreateSchema,
  type Project,
} from '../types/project.schema';

export const projectService = {
  async getAll(): Promise<Project[]> {
    const result = await db.execute(
      'SELECT * FROM projects ORDER BY created_at DESC',
    );
    return z.array(projectSchema).parse(result.rows);
  },

  async getById(id: string): Promise<Project | null> {
    const result = await db.execute({
      sql: 'SELECT * FROM projects WHERE id = ?',
      args: [id],
    });
    if (result.rows.length === 0) return null;
    return projectSchema.parse(result.rows[0]);
  },

  async create(data: unknown): Promise<Project> {
    // Validate input
    const validated = projectCreateSchema.parse(data);

    const project: Project = {
      id: crypto.randomUUID(),
      ...validated,
      createdAt: Date.now(),
      updatedAt: Date.now(),
    };

    await db.execute({
      sql: `INSERT INTO projects (id, title, description, genre, target_word_count, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)`,
      args: [
        project.id,
        project.title,
        project.description ?? null,
        project.genre,
        project.targetWordCount,
        project.createdAt,
        project.updatedAt,
      ],
    });

    return project;
  },

  async update(id: string, data: unknown): Promise<Project> {
    // Validate input
    const validated = projectCreateSchema.partial().parse(data);

    const updatedAt = Date.now();

    await db.execute({
      sql: `UPDATE projects
            SET title = COALESCE(?, title),
                description = COALESCE(?, description),
                genre = COALESCE(?, genre),
                target_word_count = COALESCE(?, target_word_count),
                updated_at = ?
            WHERE id = ?`,
      args: [
        validated.title,
        validated.description,
        validated.genre,
        validated.targetWordCount,
        updatedAt,
        id,
      ],
    });

    const updated = await projectService.getById(id);
    if (!updated) throw new Error('Project not found after update');
    return updated;
  },

  async delete(id: string): Promise<void> {
    await db.execute({
      sql: 'DELETE FROM projects WHERE id = ?',
      args: [id],
    });
  },
};
```

## Migration Pattern

### Migration File Structure

```
migrations/
├── 001_create_projects_table.sql
├── 002_create_chapters_table.sql
├── 003_add_version_column.sql
└── README.md
```

### Migration Template

```sql
-- migrations/003_add_version_column.sql
-- Description: Add version tracking column to projects table
-- Date: 2024-12-04

-- Add new column
ALTER TABLE projects ADD COLUMN version INTEGER NOT NULL DEFAULT 1;

-- Create index for version queries
CREATE INDEX idx_projects_version ON projects(version);

-- Update existing rows (if needed)
UPDATE projects SET version = 1 WHERE version IS NULL;
```

### Migration Runner

```typescript
// scripts/run-migration.ts
import { db } from '../src/lib/db';
import { readFileSync } from 'fs';

async function runMigration(filename: string): Promise<void> {
  const sql = readFileSync(`migrations/${filename}`, 'utf-8');

  // Split by semicolon and execute each statement
  const statements = sql
    .split(';')
    .map(s => s.trim())
    .filter(s => s.length > 0 && !s.startsWith('--'));

  for (const statement of statements) {
    await db.execute(statement);
  }

  console.log(`✅ Migration ${filename} completed`);
}

// Usage: pnpm tsx scripts/run-migration.ts 003_add_version_column.sql
runMigration(process.argv[2]).catch(console.error);
```

## Transaction Pattern

```typescript
// src/features/projects/services/projectService.ts
export async function createProjectWithChapters(
  projectData: ProjectCreate,
  chapterTitles: string[],
): Promise<Project> {
  // LibSQL supports transactions
  const transaction = await db.batch([
    {
      sql: `INSERT INTO projects (id, title, genre, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)`,
      args: [
        crypto.randomUUID(),
        projectData.title,
        projectData.genre,
        Date.now(),
        Date.now(),
      ],
    },
    ...chapterTitles.map((title, index) => ({
      sql: `INSERT INTO chapters (id, project_id, title, position, created_at)
            VALUES (?, ?, ?, ?, ?)`,
      args: [crypto.randomUUID(), projectId, title, index, Date.now()],
    })),
  ]);

  return await projectService.getById(projectId);
}
```

## Common Patterns

### Enum Validation

```typescript
// Zod enum matches database TEXT column
export const genreSchema = z.enum(['fantasy', 'scifi', 'mystery', 'romance']);

// Usage in table
genre: genreSchema.parse(row.genre);
```

### Timestamp Handling

```typescript
// Store as Unix milliseconds (INTEGER)
createdAt: Date.now();

// Convert to Date when needed
const createdDate = new Date(project.createdAt);
```

### Null vs Undefined

```typescript
// Database uses NULL
description TEXT  -- Can be NULL

// TypeScript uses optional (undefined)
description?: string

// Convert between them
description: row.description ?? undefined  // NULL → undefined
args: [project.description ?? null]         // undefined → NULL
```

### Camel Case Conversion

```typescript
// Database uses snake_case
target_word_count INTEGER

// TypeScript uses camelCase
targetWordCount: number

// Convert in queries
const row = { target_word_count: 50000 };
const project = {
  targetWordCount: row.target_word_count
};
```

## Schema Consistency Checklist

- [ ] Zod schema matches database columns
- [ ] TypeScript types inferred from Zod schema
- [ ] Enum values match across all layers
- [ ] Timestamps stored as Unix milliseconds (INTEGER)
- [ ] NULL/undefined handled correctly
- [ ] snake_case database ↔ camelCase TypeScript mapping
- [ ] Indexes created for frequently queried columns
- [ ] STRICT mode enabled on tables
- [ ] Validation errors handled gracefully

## Common Issues

**Validation fails on database read**

- Ensure Zod schema matches database column types exactly
- Check for NULL vs undefined handling

**Type mismatch between database and TypeScript**

- Use `z.infer<typeof schema>` to generate TypeScript types from Zod
- Don't manually create TypeScript interfaces

**Migration fails with syntax error**

- LibSQL may not support all SQLite features
- Test migrations locally before deploying

**Enum validation error**

- Verify enum values match between Zod schema and database inserts
- Remember: database stores TEXT, Zod validates values

## Success Criteria

- All database operations type-checked at compile time
- Zod schemas validate all inputs before database operations
- No runtime type errors from database reads
- Migrations version-controlled and reproducible
- Schema changes documented

## References

- LibSQL Documentation: https://docs.turso.tech/libsql
- Zod Documentation: https://zod.dev/
- SQLite Strict Tables: https://www.sqlite.org/stricttables.html
