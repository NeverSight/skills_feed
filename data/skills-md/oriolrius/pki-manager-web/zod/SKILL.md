---
name: Zod
description: Expert guidance for Zod schema validation including type inference, schema composition, parsing, refinements, transformations, error handling, and TypeScript integration. Use this when building type-safe validation, form validation, or API input validation.
---

# Zod

Expert assistance with Zod - TypeScript-first schema validation.

## Overview

Zod is a TypeScript-first schema declaration and validation library:
- **Type Inference**: Automatic TypeScript type inference
- **Zero Dependencies**: No runtime dependencies
- **Composable**: Build complex schemas from simple ones
- **Developer Experience**: Excellent autocomplete and error messages

## Installation

```bash
npm install zod
```

## Basic Usage

```typescript
import { z } from 'zod';

// Define schema
const userSchema = z.object({
  name: z.string(),
  age: z.number(),
  email: z.string().email(),
});

// Infer TypeScript type
type User = z.infer<typeof userSchema>;
// type User = { name: string; age: number; email: string }

// Parse data (throws on validation error)
const user = userSchema.parse({
  name: 'John',
  age: 30,
  email: 'john@example.com',
});

// Safe parse (returns result object)
const result = userSchema.safeParse({ name: 'John', age: '30' });
if (result.success) {
  console.log(result.data);
} else {
  console.error(result.error);
}
```

## Primitive Types

```typescript
// String
z.string();
z.string().min(5);
z.string().max(100);
z.string().length(10);
z.string().email();
z.string().url();
z.string().uuid();
z.string().regex(/^[a-z]+$/);
z.string().startsWith('https://');
z.string().endsWith('.com');

// Number
z.number();
z.number().int();
z.number().positive();
z.number().negative();
z.number().min(0);
z.number().max(100);
z.number().multipleOf(5);

// Boolean
z.boolean();

// Date
z.date();
z.date().min(new Date('2024-01-01'));
z.date().max(new Date('2025-01-01'));

// Literal
z.literal('admin');
z.literal(42);
z.literal(true);
```

## Complex Types

```typescript
// Object
const userSchema = z.object({
  name: z.string(),
  age: z.number(),
});

// Array
z.array(z.string());
z.array(z.number()).min(1).max(10);

// Tuple
z.tuple([z.string(), z.number(), z.boolean()]);

// Union (OR)
z.union([z.string(), z.number()]);
z.string().or(z.number()); // Same as above

// Discriminated Union
const shapeSchema = z.discriminatedUnion('kind', [
  z.object({ kind: z.literal('circle'), radius: z.number() }),
  z.object({ kind: z.literal('rectangle'), width: z.number(), height: z.number() }),
]);

// Intersection (AND)
const baseUser = z.object({ id: z.string() });
const namedUser = z.object({ name: z.string() });
const user = z.intersection(baseUser, namedUser);
// Or use extend
const user = baseUser.extend({ name: z.string() });

// Enum
z.enum(['admin', 'user', 'guest']);
z.nativeEnum(MyEnum);

// Record
z.record(z.string()); // { [key: string]: string }
z.record(z.string(), z.number()); // { [key: string]: number }

// Map
z.map(z.string(), z.number());

// Set
z.set(z.string());
```

## Modifiers

```typescript
// Optional
z.string().optional(); // string | undefined
z.object({ name: z.string().optional() });

// Nullable
z.string().nullable(); // string | null

// Nullish (optional + nullable)
z.string().nullish(); // string | null | undefined

// Default
z.string().default('default value');
z.number().default(0);

// Catch (provide fallback on parse error)
z.string().catch('fallback');
```

## Refinements

```typescript
// Custom validation
const passwordSchema = z.string().refine(
  (val) => val.length >= 8,
  { message: 'Password must be at least 8 characters' }
);

// Multiple refinements
const schema = z.string()
  .min(8)
  .refine((val) => /[A-Z]/.test(val), {
    message: 'Must contain uppercase letter',
  })
  .refine((val) => /[0-9]/.test(val), {
    message: 'Must contain number',
  });

// Superrefine (access ctx for multiple errors)
const schema = z.string().superRefine((val, ctx) => {
  if (val.length < 8) {
    ctx.addIssue({
      code: z.ZodIssueCode.too_small,
      minimum: 8,
      type: 'string',
      inclusive: true,
      message: 'Too short',
    });
  }
  if (!/[A-Z]/.test(val)) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      message: 'Must contain uppercase',
    });
  }
});
```

## Transformations

```typescript
// Transform value
const schema = z.string().transform((val) => val.toLowerCase());

// Chain transforms
const schema = z.string()
  .transform((val) => val.trim())
  .transform((val) => val.toLowerCase());

// Transform to different type
const numberSchema = z.string().transform((val) => parseInt(val, 10));

// Preprocess before validation
const schema = z.preprocess(
  (val) => (typeof val === 'string' ? val.trim() : val),
  z.string().min(1)
);
```

## Object Methods

```typescript
const userSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string(),
  age: z.number(),
});

// Pick fields
const nameOnly = userSchema.pick({ name: true });

// Omit fields
const withoutId = userSchema.omit({ id: true });

// Partial (all fields optional)
const partialUser = userSchema.partial();

// Deep Partial
const deepPartial = userSchema.deepPartial();

// Required (make all fields required)
const required = partialUser.required();

// Extend
const extendedUser = userSchema.extend({
  role: z.enum(['admin', 'user']),
});

// Merge
const merged = userSchema.merge(z.object({ role: z.string() }));

// Passthrough (allow extra fields)
const schema = userSchema.passthrough();

// Strict (disallow extra fields)
const schema = userSchema.strict();

// Strip (remove extra fields, default)
const schema = userSchema.strip();
```

## Error Handling

```typescript
const schema = z.object({
  name: z.string().min(2),
  age: z.number().min(18),
});

const result = schema.safeParse({ name: 'J', age: 15 });

if (!result.success) {
  // Zod error object
  console.log(result.error);

  // Format errors
  console.log(result.error.format());
  /*
  {
    name: { _errors: ['String must contain at least 2 characters'] },
    age: { _errors: ['Number must be greater than or equal to 18'] }
  }
  */

  // Flatten errors
  console.log(result.error.flatten());
  /*
  {
    formErrors: [],
    fieldErrors: {
      name: ['String must contain at least 2 characters'],
      age: ['Number must be greater than or equal to 18']
    }
  }
  */

  // Get first error
  console.log(result.error.issues[0]);
}

// Custom error messages
const schema = z.string().min(5, { message: 'Too short!' });
const schema = z.string().email({ message: 'Invalid email address' });

// Custom error map
const schema = z.string().min(5, 'Custom error');
```

## Async Validation

```typescript
// Async refinement
const schema = z.string().refine(
  async (email) => {
    const exists = await checkEmailExists(email);
    return !exists;
  },
  { message: 'Email already exists' }
);

// Parse async
const result = await schema.parseAsync('test@example.com');
const result = await schema.safeParseAsync('test@example.com');
```

## React Hook Form Integration

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const formSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email address'),
  age: z.number().min(18, 'Must be 18 or older'),
});

type FormData = z.infer<typeof formSchema>;

function MyForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(formSchema),
  });

  const onSubmit = (data: FormData) => {
    console.log(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('name')} />
      {errors.name && <span>{errors.name.message}</span>}

      <input {...register('email')} />
      {errors.email && <span>{errors.email.message}</span>}

      <input {...register('age', { valueAsNumber: true })} type="number" />
      {errors.age && <span>{errors.age.message}</span>}

      <button type="submit">Submit</button>
    </form>
  );
}
```

## tRPC Integration

```typescript
import { z } from 'zod';
import { publicProcedure, router } from './trpc';

const createUserSchema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
});

export const userRouter = router({
  create: publicProcedure
    .input(createUserSchema)
    .mutation(({ input }) => {
      // input is fully typed!
      const { name, email } = input;
      return createUser({ name, email });
    }),
});
```

## Common Patterns

### PKI Certificate Validation

```typescript
const distinguishedNameSchema = z.object({
  commonName: z.string().min(1),
  organization: z.string().optional(),
  organizationalUnit: z.string().optional(),
  country: z.string().length(2).optional(),
  state: z.string().optional(),
  locality: z.string().optional(),
});

const certificateSchema = z.object({
  subject: distinguishedNameSchema,
  issuer: distinguishedNameSchema,
  serialNumber: z.string(),
  notBefore: z.date(),
  notAfter: z.date(),
  keyUsage: z.array(z.enum([
    'digitalSignature',
    'nonRepudiation',
    'keyEncipherment',
    'dataEncipherment',
    'keyAgreement',
    'keyCertSign',
    'cRLSign',
  ])),
  extendedKeyUsage: z.array(z.enum([
    'serverAuth',
    'clientAuth',
    'codeSigning',
    'emailProtection',
    'timeStamping',
    'OCSPSigning',
  ])).optional(),
  subjectAlternativeNames: z.array(z.string()).optional(),
}).refine(
  (data) => data.notAfter > data.notBefore,
  { message: 'notAfter must be after notBefore' }
);
```

### API Response Validation

```typescript
const apiResponseSchema = z.object({
  success: z.boolean(),
  data: z.unknown().optional(),
  error: z.object({
    code: z.string(),
    message: z.string(),
  }).optional(),
}).refine(
  (data) => data.success ? data.data !== undefined : data.error !== undefined,
  { message: 'Response must have data if success, or error if not' }
);
```

## Best Practices

1. **Type Inference**: Always use `z.infer<typeof schema>` for types
2. **Reusable Schemas**: Define common schemas once, reuse everywhere
3. **Composition**: Build complex schemas from simple ones
4. **Error Messages**: Provide clear custom error messages
5. **safeParse**: Use `safeParse` when you want to handle errors yourself
6. **Transformations**: Use transforms to normalize data
7. **Refinements**: Use refinements for complex business logic
8. **Optional vs Nullable**: Understand the difference
9. **Strict Mode**: Use `.strict()` on objects to catch extra fields
10. **Documentation**: Add JSDoc comments to schemas

## Resources

- Documentation: https://zod.dev
- GitHub: https://github.com/colinhacks/zod
