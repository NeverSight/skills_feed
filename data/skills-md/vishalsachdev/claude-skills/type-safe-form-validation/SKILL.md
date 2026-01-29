---
name: type-safe-form-validation
description: A comprehensive pattern for building type-safe forms and API validation using Zod, with automatic error formatting, runtime type checking, and seamless TypeScript integration. Use when building forms with client-side and server-side validation, validating API request/response payloads, creating reusable validation schemas, or ensuring data integrity across client and server.
---

# Type-Safe Form Validation with Zod

A comprehensive pattern for building type-safe forms and API validation using Zod, with automatic error formatting, runtime type checking, and seamless TypeScript integration.

## When to use this skill

- Building forms with client-side and server-side validation
- Validating API request/response payloads
- Creating reusable validation schemas
- Need automatic TypeScript type inference from schemas
- Want formatted, user-friendly error messages
- Validating complex nested objects and arrays
- Ensuring data integrity across client and server

## Core Features

1. **Single Source of Truth** - Define validation schema once, use everywhere
2. **Type Inference** - Automatic TypeScript types from schemas
3. **Runtime Validation** - Catch invalid data at runtime
4. **User-Friendly Errors** - Format errors for display
5. **Composable Schemas** - Build complex validations from simple pieces
6. **API Integration** - Validate requests and responses

## Implementation

### Step 1: Install Zod

```bash
npm install zod
# or
pnpm add zod
```

### Step 2: Create Validation Schemas

Create `lib/validation.ts`:

```typescript
import { z } from 'zod';

// Helper to format Zod errors for user display
export function formatValidationError(error: z.ZodError): string {
  return error.errors
    .map(err => `${err.path.join('.')}: ${err.message}`)
    .join(', ');
}

// Reusable patterns
const timestampPattern = /^(?:\d{1,2}:)?\d{1,2}:\d{1,2}$/;
const youtubeIdPattern = /^[a-zA-Z0-9_-]{11}$/;

// Common field schemas
export const emailSchema = z.string().email('Invalid email address');
export const urlSchema = z.string().url('Invalid URL');
export const timestampSchema = z.string().regex(
  timestampPattern,
  'Timestamp must be in format HH:MM:SS or MM:SS'
);

// YouTube URL validation
export const youtubeUrlSchema = z.string().refine(
  (url) => {
    try {
      const parsed = new URL(url);
      return parsed.hostname.includes('youtube.com') || parsed.hostname.includes('youtu.be');
    } catch {
      return false;
    }
  },
  { message: 'Must be a valid YouTube URL' }
);

// Video ID extraction and validation
export const videoIdSchema = z.string()
  .regex(youtubeIdPattern, 'Invalid YouTube video ID')
  .length(11, 'YouTube video ID must be 11 characters');

// Transcript segment
export const transcriptSegmentSchema = z.object({
  text: z.string().min(1),
  start: z.number().nonnegative(),
  duration: z.number().positive()
});

// Topic generation request
export const generateTopicsRequestSchema = z.object({
  transcript: z.array(transcriptSegmentSchema).min(1, 'Transcript cannot be empty'),
  model: z.enum(['gemini-2.5-flash-lite', 'gemini-2.5-flash', 'gemini-2.5-pro']).optional(),
  includeCandidatePool: z.boolean().optional(),
  excludeTopicKeys: z.array(z.string()).optional(),
  videoInfo: z.object({
    title: z.string(),
    author: z.string(),
    duration: z.number().nullable()
  }).optional(),
  mode: z.enum(['smart', 'fast']).optional()
});

// Chat request
export const chatRequestSchema = z.object({
  message: z.string().min(1, 'Message cannot be empty').max(1000, 'Message too long'),
  transcript: z.array(transcriptSegmentSchema),
  conversationHistory: z.array(z.object({
    role: z.enum(['user', 'assistant']),
    content: z.string()
  })).optional()
});

// Note creation
export const createNoteSchema = z.object({
  videoId: z.string().uuid('Invalid video ID'),
  source: z.enum(['chat', 'takeaways', 'transcript', 'custom']),
  text: z.string().min(1, 'Note cannot be empty').max(5000, 'Note too long'),
  metadata: z.object({
    transcript: z.object({
      start: z.number(),
      end: z.number().optional(),
      segmentIndex: z.number().optional()
    }).optional(),
    selectedText: z.string().optional()
  }).optional()
});

// User registration
export const registerSchema = z.object({
  email: emailSchema,
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Password must contain uppercase letter')
    .regex(/[a-z]/, 'Password must contain lowercase letter')
    .regex(/[0-9]/, 'Password must contain a number'),
  confirmPassword: z.string()
}).refine(
  (data) => data.password === data.confirmPassword,
  {
    message: "Passwords don't match",
    path: ["confirmPassword"]
  }
);

// Infer TypeScript types from schemas
export type GenerateTopicsRequest = z.infer<typeof generateTopicsRequestSchema>;
export type ChatRequest = z.infer<typeof chatRequestSchema>;
export type CreateNote = z.infer<typeof createNoteSchema>;
export type RegisterForm = z.infer<typeof registerSchema>;
```

### Step 3: Create Error Formatter

```typescript
// lib/validation-errors.ts
import { z } from 'zod';

export interface ValidationError {
  field: string;
  message: string;
}

export function formatZodErrors(error: z.ZodError): ValidationError[] {
  return error.errors.map(err => ({
    field: err.path.join('.'),
    message: err.message
  }));
}

export function getFieldError(
  errors: ValidationError[],
  field: string
): string | undefined {
  return errors.find(e => e.field === field)?.message;
}
```

## Usage Examples

### Example 1: API Route Validation

```typescript
// app/api/generate-topics/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { generateTopicsRequestSchema, formatValidationError } from '@/lib/validation';
import { z } from 'zod';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    // Validate request
    let validatedData;
    try {
      validatedData = generateTopicsRequestSchema.parse(body);
    } catch (error) {
      if (error instanceof z.ZodError) {
        return NextResponse.json(
          {
            error: 'Validation failed',
            details: formatValidationError(error)
          },
          { status: 400 }
        );
      }
      throw error;
    }

    // validatedData is now type-safe!
    const { transcript, model, mode } = validatedData;

    // Process with confidence - data is validated
    const topics = await generateTopics(transcript, model);

    return NextResponse.json({ topics });
  } catch (error) {
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
```

**Benefits**:
- ✅ Type-safe request data
- ✅ User-friendly error messages
- ✅ 400 for validation errors, 500 for server errors
- ✅ No manual type checking

---

### Example 2: React Hook Form Integration

```typescript
'use client';

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { registerSchema, RegisterForm } from '@/lib/validation';

export function SignUpForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting }
  } = useForm<RegisterForm>({
    resolver: zodResolver(registerSchema)
  });

  const onSubmit = async (data: RegisterForm) => {
    // data is type-safe and validated
    const response = await fetch('/api/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      // Handle error
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <input {...register('email')} type="email" placeholder="Email" />
        {errors.email && <span className="error">{errors.email.message}</span>}
      </div>

      <div>
        <input {...register('password')} type="password" placeholder="Password" />
        {errors.password && <span className="error">{errors.password.message}</span>}
      </div>

      <div>
        <input {...register('confirmPassword')} type="password" placeholder="Confirm" />
        {errors.confirmPassword && (
          <span className="error">{errors.confirmPassword.message}</span>
        )}
      </div>

      <button type="submit" disabled={isSubmitting}>
        Sign Up
      </button>
    </form>
  );
}
```

**Benefits**:
- ✅ Automatic client-side validation
- ✅ Type-safe form data
- ✅ No manual error checking
- ✅ Disabled submit during processing

---

### Example 3: Nested Object Validation

```typescript
import { z } from 'zod';

// Complex nested structure
const projectSchema = z.object({
  name: z.string().min(1),
  description: z.string().optional(),
  settings: z.object({
    visibility: z.enum(['public', 'private', 'unlisted']),
    features: z.object({
      comments: z.boolean(),
      analytics: z.boolean(),
      aiGeneration: z.object({
        enabled: z.boolean(),
        model: z.enum(['fast', 'balanced', 'quality']),
        maxTokens: z.number().min(100).max(10000)
      })
    }),
    limits: z.object({
      maxVideos: z.number().positive(),
      maxNotes: z.number().positive()
    })
  }),
  tags: z.array(z.string()).min(1).max(10)
});

type Project = z.infer<typeof projectSchema>;

// Validate complex object
const project: unknown = await fetchProject();
const validated = projectSchema.parse(project);

// TypeScript knows exact structure
console.log(validated.settings.features.aiGeneration.model);
//                    ^-- fully typed!
```

---

### Example 4: Array Validation with Constraints

```typescript
import { z } from 'zod';

// Validate array of topics with constraints
const topicsSchema = z.array(
  z.object({
    id: z.string().uuid(),
    title: z.string().min(3).max(100),
    segments: z.array(
      z.object({
        start: z.number().nonnegative(),
        end: z.number().positive()
      })
    ).min(1, 'Each topic must have at least one segment')
  })
).min(3, 'Must have at least 3 topics')
  .max(10, 'Cannot have more than 10 topics');

// Validation with helpful errors
try {
  const topics = topicsSchema.parse(data);
} catch (error) {
  if (error instanceof z.ZodError) {
    console.error(formatValidationError(error));
    // Output: "0.title: String must contain at least 3 character(s)"
  }
}
```

---

### Example 5: Transform and Validate

```typescript
import { z } from 'zod';

// Schema that transforms data during validation
const urlInputSchema = z.object({
  url: z.string()
    .transform((url) => url.trim())
    .pipe(
      z.string().url('Invalid URL')
    )
    .transform((url) => {
      // Extract video ID from YouTube URL
      const match = url.match(/(?:v=|youtu\.be\/)([a-zA-Z0-9_-]{11})/);
      return match ? match[1] : null;
    })
    .pipe(
      z.string().nullable().refine(
        (id) => id !== null,
        { message: 'Could not extract video ID from URL' }
      )
    )
});

// Usage
const result = urlInputSchema.parse({
  url: '  https://youtube.com/watch?v=dQw4w9WgXcQ  '
});

console.log(result.url); // "dQw4w9WgXcQ" (trimmed and extracted)
```

---

### Example 6: Conditional Validation

```typescript
import { z } from 'zod';

// Validation rules change based on other fields
const paymentSchema = z.discriminatedUnion('method', [
  z.object({
    method: z.literal('credit_card'),
    cardNumber: z.string().length(16),
    cvv: z.string().length(3),
    expiry: z.string().regex(/^\d{2}\/\d{2}$/)
  }),
  z.object({
    method: z.literal('paypal'),
    email: z.string().email()
  }),
  z.object({
    method: z.literal('bank_transfer'),
    accountNumber: z.string().min(8),
    routingNumber: z.string().length(9)
  })
]);

type Payment = z.infer<typeof paymentSchema>;

// TypeScript narrows types based on discriminator
function processPayment(payment: Payment) {
  switch (payment.method) {
    case 'credit_card':
      // TypeScript knows: payment.cardNumber, payment.cvv, payment.expiry exist
      return chargeCreditCard(payment.cardNumber, payment.cvv);

    case 'paypal':
      // TypeScript knows: payment.email exists
      return chargePaypal(payment.email);

    case 'bank_transfer':
      // TypeScript knows: payment.accountNumber, payment.routingNumber exist
      return bankTransfer(payment.accountNumber);
  }
}
```

---

## Advanced Patterns

### Pattern 1: Custom Validators

```typescript
import { z } from 'zod';

// Custom validation logic
const strongPasswordSchema = z.string().superRefine((password, ctx) => {
  if (password.length < 8) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      message: 'Password must be at least 8 characters'
    });
  }

  if (!/[A-Z]/.test(password)) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      message: 'Password must contain uppercase letter'
    });
  }

  if (!/[a-z]/.test(password)) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      message: 'Password must contain lowercase letter'
    });
  }

  if (!/[0-9]/.test(password)) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      message: 'Password must contain a number'
    });
  }

  if (!/[!@#$%^&*]/.test(password)) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      message: 'Password must contain special character'
    });
  }
});
```

---

### Pattern 2: Schema Composition

```typescript
import { z } from 'zod';

// Base schemas
const baseEntitySchema = z.object({
  id: z.string().uuid(),
  createdAt: z.string().datetime(),
  updatedAt: z.string().datetime()
});

const userDataSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1)
});

// Compose schemas
const userSchema = baseEntitySchema.merge(userDataSchema);

type User = z.infer<typeof userSchema>;
// { id, createdAt, updatedAt, email, name }
```

---

### Pattern 3: Partial Updates

```typescript
import { z } from 'zod';

const userSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1),
  age: z.number().positive(),
  bio: z.string().optional()
});

// For PATCH requests - all fields optional
const updateUserSchema = userSchema.partial();

type UpdateUser = z.infer<typeof updateUserSchema>;
// { email?, name?, age?, bio? }

// Ensure at least one field is provided
const updateUserWithOneField = userSchema.partial().refine(
  (data) => Object.keys(data).length > 0,
  { message: 'At least one field must be provided' }
);
```

---

### Pattern 4: Default Values

```typescript
import { z } from 'zod';

const configSchema = z.object({
  theme: z.enum(['light', 'dark']).default('light'),
  language: z.string().default('en'),
  notifications: z.object({
    email: z.boolean().default(true),
    push: z.boolean().default(false),
    sms: z.boolean().default(false)
  }).default({})
});

// Parse with defaults
const config = configSchema.parse({});
// { theme: 'light', language: 'en', notifications: { email: true, push: false, sms: false } }
```

---

## Form Component Patterns

### Pattern 1: Reusable Form Field

```typescript
import { UseFormRegister, FieldError } from 'react-hook-form';

interface FormFieldProps {
  name: string;
  label: string;
  register: UseFormRegister<any>;
  error?: FieldError;
  type?: string;
  required?: boolean;
}

export function FormField({ name, label, register, error, type = 'text', required }: FormFieldProps) {
  return (
    <div className="form-field">
      <label htmlFor={name}>
        {label}
        {required && <span className="required">*</span>}
      </label>

      <input
        id={name}
        type={type}
        {...register(name)}
        aria-invalid={error ? 'true' : 'false'}
        className={error ? 'error' : ''}
      />

      {error && (
        <span className="error-message" role="alert">
          {error.message}
        </span>
      )}
    </div>
  );
}
```

---

### Pattern 2: Multi-Step Form Validation

```typescript
import { z } from 'zod';

const step1Schema = z.object({
  email: z.string().email(),
  password: z.string().min(8)
});

const step2Schema = z.object({
  firstName: z.string().min(1),
  lastName: z.string().min(1)
});

const step3Schema = z.object({
  acceptTerms: z.literal(true, {
    errorMap: () => ({ message: 'You must accept the terms' })
  })
});

// Validate current step
function MultiStepForm() {
  const [step, setStep] = useState(1);

  const currentSchema = {
    1: step1Schema,
    2: step2Schema,
    3: step3Schema
  }[step];

  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: zodResolver(currentSchema)
  });

  const onSubmit = (data) => {
    if (step < 3) {
      setStep(step + 1);
    } else {
      // Final submission - validate all steps
      const fullSchema = step1Schema.merge(step2Schema).merge(step3Schema);
      const validated = fullSchema.parse(allData);
      submitForm(validated);
    }
  };

  return <form onSubmit={handleSubmit(onSubmit)}>...</form>;
}
```

---

## Best Practices

1. **Define schemas in lib/validation.ts** - Central location
2. **Export inferred types** - `export type X = z.infer<typeof xSchema>`
3. **Validate at API boundaries** - Both client and server
4. **Use formatValidationError** - Consistent error formatting
5. **Compose schemas** - Build complex from simple
6. **Set meaningful error messages** - Help users fix issues
7. **Use discriminated unions** - For conditional validation
8. **Add defaults where appropriate** - Better UX

---

## Common Pitfalls

1. **Forgetting to call .parse()** - Schema alone doesn't validate
2. **Not handling ZodError** - Always catch and format
3. **Circular dependencies** - Use z.lazy() for recursive schemas
4. **Overly strict validation** - Balance security and UX
5. **Client-only validation** - Always validate on server too
6. **Not using type inference** - Manually typing defeats the purpose
7. **Complex regex without explanation** - Add comments

---

## Testing

```typescript
import { describe, test, expect } from 'vitest';
import { registerSchema } from '@/lib/validation';
import { z } from 'zod';

describe('registerSchema', () => {
  test('valid registration data passes', () => {
    const valid = {
      email: 'user@example.com',
      password: 'SecurePass1',
      confirmPassword: 'SecurePass1'
    };

    expect(() => registerSchema.parse(valid)).not.toThrow();
  });

  test('invalid email fails', () => {
    const invalid = {
      email: 'not-an-email',
      password: 'SecurePass1',
      confirmPassword: 'SecurePass1'
    };

    expect(() => registerSchema.parse(invalid)).toThrow(z.ZodError);
  });

  test('mismatched passwords fail', () => {
    const invalid = {
      email: 'user@example.com',
      password: 'SecurePass1',
      confirmPassword: 'DifferentPass1'
    };

    expect(() => registerSchema.parse(invalid)).toThrow(z.ZodError);
  });

  test('weak password fails', () => {
    const invalid = {
      email: 'user@example.com',
      password: 'weak',
      confirmPassword: 'weak'
    };

    expect(() => registerSchema.parse(invalid)).toThrow(z.ZodError);
  });
});
```

---

## Migration from Manual Validation

**Before:**

```typescript
function validateUser(data: any) {
  const errors: string[] = [];

  if (!data.email || !/\S+@\S+\.\S+/.test(data.email)) {
    errors.push('Invalid email');
  }

  if (!data.password || data.password.length < 8) {
    errors.push('Password too short');
  }

  if (data.password !== data.confirmPassword) {
    errors.push('Passwords do not match');
  }

  if (errors.length > 0) {
    throw new Error(errors.join(', '));
  }

  return data as User; // Unsafe cast!
}
```

**After:**

```typescript
import { registerSchema } from '@/lib/validation';

function validateUser(data: unknown) {
  return registerSchema.parse(data);
  // Returns type-safe User object or throws ZodError
}
```

---

## Next Steps

After implementing this skill:

1. Replace all manual validation with Zod schemas
2. Add schemas for all API routes
3. Integrate with React Hook Form for client forms
4. Create reusable validation patterns library
5. Add custom validators for business logic
6. Set up schema testing

## Related Skills

- **Secure Next.js API Routes** - Validate requests before processing
- **AI Model Cascade** - Validate AI responses with schemas
- **Resilient Async Operations** - Combine with safePromise for parsing

---

Built from production validation patterns in [TLDW](https://github.com/vishalsachdev/tldw)
