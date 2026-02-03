---
name: zod-validation
description: Guide for Zod schema validation patterns in TypeScript. Use when creating validation schemas, defining types, validating forms, API inputs, or handling validation errors.
---

# Zod Validation Patterns

## Schema Location

```
features/<feature>/model/
├── <feature>-schemas.ts      # Zod schemas + inferred types
└── <feature>-constants.ts    # Constants used in schemas
```

## Basic Schema

```typescript
// account-schemas.ts
import { z } from 'zod'

export const AccountSchema = z.object({
  id: z.string().ulid(),
  userId: z.string().ulid(),
  name: z.string().min(1).max(100),
  balance: z.number().default(0),
  deleted: z.boolean().default(false),
  createdAt: z.date(),
  updatedAt: z.date(),
})

export type Account = z.infer<typeof AccountSchema>
```

## Input Schemas (Pick/Omit)

```typescript
// Create - only user-provided fields
export const CreateAccountSchema = AccountSchema.pick({
  name: true,
})
export type CreateAccountInput = z.infer<typeof CreateAccountSchema>

// Update - partial user fields
export const UpdateAccountSchema = AccountSchema.pick({
  name: true,
  balance: true,
}).partial()
export type UpdateAccountInput = z.infer<typeof UpdateAccountSchema>
```

## Common Patterns

```typescript
// Optional with default
z.string().default('')
z.number().default(0)
z.boolean().default(false)

// Nullable vs Optional
z.string().nullable()      // string | null
z.string().optional()      // string | undefined
z.string().nullish()       // string | null | undefined

// Enums
export const StatusSchema = z.enum(['active', 'suspended', 'deleted'])
export type Status = z.infer<typeof StatusSchema>

// Literals
z.literal('draft')

// Union
z.union([z.string(), z.number()])

// Arrays
z.array(z.string())
z.string().array()         // Same as above

// Records/Maps
z.record(z.string())       // { [key: string]: string }
```

## Shared Schemas (@saas4dev/core)

```typescript
import {
  UlidSchema,           // z.string().ulid()
  EmailSchema,          // z.string().email()
  RequiredStringSchema, // z.string().min(1)
  UrlSchema,            // z.string().url()
  PhoneSchema,          // Phone validation
} from '@saas4dev/core'
```

## Refinements

```typescript
// Custom validation
const PasswordSchema = z.string()
  .min(8)
  .refine(
    (val) => /[A-Z]/.test(val),
    { message: 'Must contain uppercase' }
  )
  .refine(
    (val) => /[0-9]/.test(val),
    { message: 'Must contain number' }
  )

// Cross-field validation
const DateRangeSchema = z.object({
  startDate: z.date(),
  endDate: z.date(),
}).refine(
  (data) => data.endDate > data.startDate,
  { message: 'End date must be after start', path: ['endDate'] }
)
```

## Transform

```typescript
// Transform input
const TrimmedString = z.string().trim()
const LowerEmail = z.string().email().toLowerCase()

// Coerce types
z.coerce.number()    // "123" -> 123
z.coerce.date()      // "2024-01-01" -> Date
z.coerce.boolean()   // "true" -> true
```

## Error Handling

```typescript
import { convertZodErrorsToKeyValue } from '@saas4dev/core'

try {
  const data = Schema.parse(input)
} catch (error) {
  if (error instanceof z.ZodError) {
    const fieldErrors = convertZodErrorsToKeyValue(error)
    // { name: 'Required', email: 'Invalid email' }
    return { success: false, errors: fieldErrors }
  }
}

// Safe parse (no throw)
const result = Schema.safeParse(input)
if (!result.success) {
  const errors = convertZodErrorsToKeyValue(result.error)
}
```

## Form Integration

```typescript
// React Hook Form
import { zodResolver } from '@hookform/resolvers/zod'

const form = useForm<CreateAccountInput>({
  resolver: zodResolver(CreateAccountSchema),
  defaultValues: { name: '' },
})
```

## Server Action Input

```typescript
// ZSA validates automatically
export const createAction = authedProcedure
  .createServerAction()
  .input(CreateAccountSchema, { type: 'formData' })
  .handler(async ({ input }) => {
    // input is typed and validated
  })
```

## Constants Pattern

```typescript
// account-constants.ts
export const ACCOUNT_MAX_NAME_LENGTH = 100
export const ACCOUNT_TYPES = ['checking', 'savings', 'credit'] as const

// Use in schema
const AccountSchema = z.object({
  name: z.string().max(ACCOUNT_MAX_NAME_LENGTH),
  type: z.enum(ACCOUNT_TYPES),
})
```
