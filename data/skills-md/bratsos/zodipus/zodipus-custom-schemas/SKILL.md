---
name: zodipus-custom-schemas
description: Define custom Zod schemas for Prisma JSON fields using @zodSchema annotations. Use when working with typed JSON, metadata fields, settings objects, complex JSON structures in Prisma, or custom-schemas.ts.
license: MIT
metadata:
  author: zodipus
  version: "1.0.0"
---

# Custom JSON Schemas

Type your Prisma JSON fields with custom Zod schemas using `@zodSchema` annotations.

## When to Apply

- User has JSON fields in Prisma schema
- User mentions `@zodSchema` annotation
- User wants typed metadata, settings, or config fields
- User asks about `custom-schemas.ts`
- User needs validation for JSON data
- User mentions "typed JSON" or "JSON validation"

## The Problem

Prisma's `Json` type has no runtime type safety:

```prisma
model Post {
  id       String @id
  metadata Json?  // Type: JsonValue (any)
}
```

```typescript
// No type safety - anything goes
post.metadata = { random: 'stuff', 123: true };
post.metadata = 'just a string';
post.metadata = [1, 2, 3];
```

## The Solution

Use `@zodSchema` to define exactly what your JSON should contain.

### Step 1: Annotate in Prisma Schema

Add a triple-slash comment with `@zodSchema SchemaName` above your JSON field:

```prisma
model Post {
  id        String  @id @default(cuid())
  title     String
  content   String?

  /// @zodSchema PostMetadataSchema
  metadata  Json?
}

model User {
  id       String @id @default(cuid())
  email    String @unique

  /// @zodSchema UserSettingsSchema
  settings Json   @default("{}")

  /// @zodSchema UserPreferencesSchema
  preferences Json?
}
```

### Step 2: Run Generation

```bash
npx prisma generate
```

This creates a `custom-schemas.ts` file with placeholder schemas:

```typescript
// generated/custom-schemas.ts
import { z } from 'zod';

// Placeholder - replace with your schema
export const PostMetadataSchema = z.unknown();
export const UserSettingsSchema = z.unknown();
export const UserPreferencesSchema = z.unknown();
```

### Step 3: Define Your Schemas

Replace the placeholders with real schemas:

```typescript
// generated/custom-schemas.ts
import { z } from 'zod';

export const PostMetadataSchema = z.object({
  tags: z.array(z.string()).default([]),
  views: z.number().int().nonnegative().default(0),
  featured: z.boolean().default(false),
  seo: z.object({
    title: z.string().max(60).optional(),
    description: z.string().max(160).optional(),
    keywords: z.array(z.string()).optional(),
  }).optional(),
});

export const UserSettingsSchema = z.object({
  theme: z.enum(['light', 'dark', 'system']).default('system'),
  notifications: z.object({
    email: z.boolean().default(true),
    push: z.boolean().default(false),
    sms: z.boolean().default(false),
  }).default({}),
  language: z.string().default('en'),
  timezone: z.string().default('UTC'),
});

export const UserPreferencesSchema = z.object({
  dashboard: z.object({
    layout: z.enum(['grid', 'list']).default('grid'),
    itemsPerPage: z.number().int().min(10).max(100).default(20),
  }).optional(),
  privacy: z.object({
    showEmail: z.boolean().default(false),
    showActivity: z.boolean().default(true),
  }).optional(),
});
```

### Step 4: Use It

Now your schemas have full type safety:

```typescript
import { PostSchema, UserSchema } from './generated';

// Validated with your custom schema
const post = PostSchema.parse({
  id: '123',
  title: 'My Post',
  content: 'Hello world',
  metadata: {
    tags: ['tutorial', 'prisma'],
    views: 100,
    featured: true,
    seo: {
      title: 'My Post - Tutorial',
      description: 'Learn about Prisma',
    },
  },
});

// TypeScript knows the shape
post.metadata.tags;        // string[]
post.metadata.views;       // number
post.metadata.seo?.title;  // string | undefined
```

## Common Patterns

### Settings Object

```typescript
export const AppSettingsSchema = z.object({
  theme: z.enum(['light', 'dark', 'system']).default('system'),
  fontSize: z.enum(['small', 'medium', 'large']).default('medium'),
  compactMode: z.boolean().default(false),
  sidebar: z.object({
    collapsed: z.boolean().default(false),
    width: z.number().int().min(200).max(400).default(280),
  }).default({}),
});
```

### Metadata with Timestamps

```typescript
export const AuditMetadataSchema = z.object({
  createdBy: z.string().optional(),
  updatedBy: z.string().optional(),
  version: z.number().int().default(1),
  changelog: z.array(z.object({
    date: z.coerce.date(),
    user: z.string(),
    action: z.string(),
  })).default([]),
});
```

### Configuration with Defaults

```typescript
export const NotificationConfigSchema = z.object({
  enabled: z.boolean().default(true),
  channels: z.object({
    email: z.boolean().default(true),
    slack: z.boolean().default(false),
    webhook: z.string().url().optional(),
  }).default({}),
  frequency: z.enum(['instant', 'hourly', 'daily']).default('instant'),
  quietHours: z.object({
    enabled: z.boolean().default(false),
    start: z.string().regex(/^\d{2}:\d{2}$/).optional(),
    end: z.string().regex(/^\d{2}:\d{2}$/).optional(),
  }).optional(),
});
```

### Array of Objects

```typescript
export const ProductVariantsSchema = z.array(z.object({
  sku: z.string(),
  name: z.string(),
  price: z.number().positive(),
  stock: z.number().int().nonnegative(),
  attributes: z.record(z.string()).optional(),
}));
```

### Union/Discriminated Union Types

```typescript
// Simple union
export const PaymentMethodSchema = z.union([
  z.object({
    type: z.literal('card'),
    last4: z.string().length(4),
    brand: z.enum(['visa', 'mastercard', 'amex']),
    expiryMonth: z.number().int().min(1).max(12),
    expiryYear: z.number().int(),
  }),
  z.object({
    type: z.literal('bank'),
    bankName: z.string(),
    accountLast4: z.string().length(4),
  }),
  z.object({
    type: z.literal('paypal'),
    email: z.string().email(),
  }),
]);

// Discriminated union (recommended for type inference)
export const PaymentMethodSchema = z.discriminatedUnion('type', [
  z.object({
    type: z.literal('card'),
    last4: z.string().length(4),
    brand: z.enum(['visa', 'mastercard', 'amex']),
  }),
  z.object({
    type: z.literal('bank'),
    bankName: z.string(),
    accountLast4: z.string().length(4),
  }),
]);
```

### Recursive/Nested Structures

```typescript
// Tree structure (menu, categories, etc.)
interface TreeNode {
  id: string;
  name: string;
  children?: TreeNode[];
}

export const TreeNodeSchema: z.ZodType<TreeNode> = z.lazy(() =>
  z.object({
    id: z.string(),
    name: z.string(),
    children: z.array(TreeNodeSchema).optional(),
  })
);

export const MenuSchema = z.array(TreeNodeSchema);
```

### Flexible Key-Value Store

```typescript
// For arbitrary key-value pairs
export const CustomFieldsSchema = z.record(
  z.string(),
  z.union([z.string(), z.number(), z.boolean(), z.null()])
);

// With constraints
export const LabeledFieldsSchema = z.record(
  z.string().regex(/^[a-z_][a-z0-9_]*$/), // lowercase snake_case keys
  z.string().max(500)
);
```

## Best Practices

### 1. Always Use Defaults

Prevents null/undefined issues when creating new records:

```typescript
export const SettingsSchema = z.object({
  theme: z.enum(['light', 'dark']).default('light'),
  notifications: z.boolean().default(true),
}).default({}); // Default for the entire object
```

### 2. Make Optional Fields Explicit

Be clear about what's required vs optional:

```typescript
export const ProfileSchema = z.object({
  // Required
  displayName: z.string().min(1).max(50),

  // Optional (can be undefined)
  bio: z.string().max(500).optional(),

  // Nullable (can be null)
  avatarUrl: z.string().url().nullable(),

  // Optional with default
  isPublic: z.boolean().default(true),
});
```

### 3. Validate Constraints

Add business rule validations:

```typescript
export const PriceSchema = z.object({
  amount: z.number().positive(),
  currency: z.enum(['USD', 'EUR', 'GBP']),
  discount: z.number().min(0).max(100).optional(),
}).refine(
  (data) => !data.discount || data.amount > 0,
  { message: 'Discount requires positive amount' }
);
```

### 4. Document with `.describe()`

Add descriptions for documentation:

```typescript
export const ApiConfigSchema = z.object({
  endpoint: z.string().url().describe('API base URL'),
  timeout: z.number().int().positive().default(30000).describe('Request timeout in ms'),
  retries: z.number().int().min(0).max(5).default(3).describe('Number of retry attempts'),
});
```

## Regeneration Behavior

When you run `npx prisma generate`:

1. **New `@zodSchema` annotations**: Adds placeholder to `custom-schemas.ts`
2. **Existing schemas**: Preserved - your definitions are NOT overwritten
3. **Removed annotations**: Schema export remains (manual cleanup needed)

## Troubleshooting

### Schema Not Being Used

Ensure the annotation is a **triple-slash comment**:

```prisma
// Wrong - single slash
// @zodSchema MySchema
metadata Json?

// Wrong - double slash doc comment
/** @zodSchema MySchema */
metadata Json?

// Correct - triple slash
/// @zodSchema MySchema
metadata Json?
```

### Type Errors After Editing custom-schemas.ts

Run generation again to update model schemas:

```bash
npx prisma generate
```

### Schema Name Must Match Export

The annotation name must exactly match the export:

```prisma
/// @zodSchema PostMetadataSchema
metadata Json?
```

```typescript
// Must match exactly
export const PostMetadataSchema = z.object({...});
```
