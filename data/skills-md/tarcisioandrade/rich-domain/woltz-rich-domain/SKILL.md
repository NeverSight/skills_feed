---
name: woltz-rich-domain
description: Guide for @woltz/rich-domain DDD library and ecosystem. Use when building domain models, repositories, or working with Prisma/TypeORM adapters.
---

# @woltz/rich-domain

TypeScript library for Domain-Driven Design with automatic change tracking and Standard Schema validation.

## Requirements

- Node.js >= 22.12
- TypeScript >= 5.4

## Ecosystem

| Package                           | Purpose                      |
| --------------------------------- | ---------------------------- |
| `@woltz/rich-domain`              | Core DDD building blocks     |
| `@woltz/rich-domain-prisma`       | Prisma ORM adapter           |
| `@woltz/rich-domain-typeorm`      | TypeORM adapter              |
| `@woltz/rich-domain-criteria-zod` | Zod schemas for Criteria API |
| `@woltz/rich-domain-export`       | Multi-format data export     |

## Quick Start

### 1. Define a Value Object

```typescript
import { ValueObject } from "@woltz/rich-domain";
import { z } from "zod";

class Email extends ValueObject<string> {
  protected static validation = {
    schema: z.string().email(),
  };

  getDomain(): string {
    return this.value.split("@")[1];
  }
}
```

### 2. Define an Entity

```typescript
import { Entity, Id } from "@woltz/rich-domain";

const PostSchema = z.object({
  id: z.custom<Id>(),
  title: z.string().min(1),
  content: z.string(),
  published: z.boolean(),
});

class Post extends Entity<z.infer<typeof PostSchema>> {
  protected static validation = { schema: PostSchema };

  publish(): void {
    this.props.published = true;
  }

  get title() {
    return this.props.title;
  }
}
```

### 3. Define an Aggregate

```typescript
import { Aggregate, Id, EntityHooks } from "@woltz/rich-domain";
import { UserCreatedEvent } from "./events";
import { Email } from "./email";

const UserSchema = z.object({
  id: z.custom<Id>(),
  email: z.custom<Email>(),
  name: z.string().min(2),
  posts: z.array(z.instanceof(Post)),
  createdAt: z.date(),
});
export type UserProps = z.infer<typeof UserSchema>;

class User extends Aggregate<UserProps, "createdAt"> {
  protected static validation = { schema: UserSchema };
  protected static hooks: EntityHooks<UserProps, User> = {
    onBeforeCreate: (props) => {
      if (!props.createdAt) props.createdAt = new Date();
    },
    onCreate: (entity) => {
      if (entity.isNew()) {
        entity.addDomainEvent(new UserCreatedEvent({ id: entity.id.value }));
      }
    },
  };

  getTypedChanges() {
    interface Entities {
      Post: Post;
    }
    return this.getChanges<Entities>();
  }

  addPost(title: string, content: string): void {
    this.props.posts.push(new Post({ title, content, published: false }));
  }

  get email() {
    return this.props.email.value;
  }
  get posts() {
    return this.props.posts;
  }
}
```

### 4. Use Change Tracking

```typescript
const user = await userRepository.findById(userId);

// Make changes
user.addPost("New Post", "Content");
user.posts[0].publish();

// Get changes automatically
// We strongly recommend using this `getTypedChanges` helper pattern for better DX
const changes = user.getTypedChanges();
// { creates: [...], updates: [...], deletes: [...] }

// After saving
user.markAsClean();
```

### 5. Query with Criteria

```typescript
import { Criteria } from "@woltz/rich-domain";

// fully type-safe, fields inferred from schema
const criteria = Criteria.create<User>()
  .where("status", "equals", "active")
  .whereContains("email", "@company.com")
  .orderBy("createdAt", "desc")
  .paginate(1, 20);

const result = await userRepository.find(criteria);
```

## Core Principles

1. **Aggregates define consistency boundaries** - Modify entities through their aggregate root
2. **Value Objects are immutable** - Use `clone()` to create modified copies
3. **Id tracks new vs existing** - `new Id()` for INSERT, `Id.from(value)` for UPDATE
4. **Change tracking is automatic** - Use `getChanges()` and `markAsClean()`
5. **Repositories abstract persistence** - Domain layer doesn't know about database

## References

For detailed documentation on specific topics:

- [Core Concepts](./references/core-concepts.md) - Entities, Aggregates, Value Objects, Lifecycle Hooks
- [Domain Events](./references/domain-events.md) - Event-driven architecture with example using BullMQ
- [Criteria API](./references/criteria.md) - Type-safe query building with filters, ordering, pagination
- [Criteria Zod](./references/criteria-zod.md) - Zod schemas for API query validation
- [Schema Registry](./references/schema-registry.md) - EntitySchemaRegistry for field mapping and relationships
- [Prisma Adapter](./references/prisma-adapter.md) - PrismaRepository, UnitOfWork, Transactions
- [TypeORM Adapter](./references/typeorm-adapter.md) - TypeORMRepository, change tracking
- [Export](./references/export.md) - CSV, JSON export with streaming support

**DO NOT read all files at once**. Load based on context.

## Resources

- [Documentation](https://woltz.mintlify.app)
