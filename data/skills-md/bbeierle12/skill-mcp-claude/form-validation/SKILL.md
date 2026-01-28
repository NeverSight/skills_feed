---
name: form-validation
description: Schema-first validation with Zod, timing patterns (reward early, punish late), async validation, and error message design. Use when implementing form validation for any framework. The foundation skill that all framework-specific skills depend on.
---

# Form Validation

Schema-first validation using Zod as the single source of truth for both runtime validation and TypeScript types.

## Quick Start

```typescript
import { z } from 'zod';

// 1. Define schema (validation + types in one place)
const schema = z.object({
  email: z.string().min(1, 'Required').email('Invalid email'),
  age: z.number().positive().optional()
});

// 2. Infer TypeScript types (never manually define)
type FormData = z.infer<typeof schema>;

// 3. Use with form library
import { zodResolver } from '@hookform/resolvers/zod';
const { register } = useForm<FormData>({
  resolver: zodResolver(schema)
});
```

## Core Principle: Reward Early, Punish Late

This is the optimal validation timing pattern backed by UX research:

| Event | Show Valid (✓) | Show Invalid (✗) | Why |
|-------|----------------|------------------|-----|
| On input | ✅ Immediately | ❌ Never | Don't yell while typing |
| On blur | ✅ Immediately | ✅ Yes | User finished, show errors |
| During correction | ✅ Immediately | ✅ Real-time | Let them fix quickly |

### Implementation

```typescript
// React Hook Form
useForm({
  mode: 'onBlur',           // First validation on blur (punish late)
  reValidateMode: 'onChange' // Re-validate on change (real-time correction)
});

// TanStack Form
useForm({
  validators: {
    onBlur: schema,          // Validate on blur
    onChange: schema         // Re-validate on change (after touched)
  }
});
```

## Zod Schema Patterns

### Basic Types

```typescript
import { z } from 'zod';

// Strings
z.string()                          // Any string
z.string().min(1, 'Required')       // Non-empty (better than .nonempty())
z.string().email('Invalid email')
z.string().url('Invalid URL')
z.string().uuid('Invalid ID')
z.string().regex(/^\d{5}$/, 'Invalid ZIP')

// Numbers
z.number()                          // Any number
z.number().positive('Must be positive')
z.number().int('Must be whole number')
z.number().min(0).max(100)

// Booleans
z.boolean()
z.literal(true)                     // Must be exactly true

// Enums
z.enum(['admin', 'user', 'guest'])

// Arrays
z.array(z.string())
z.array(z.string()).min(1, 'Select at least one')

// Objects
z.object({
  name: z.string(),
  email: z.string().email()
})
```

### Common Form Schemas

```typescript
// schemas/auth.ts
export const loginSchema = z.object({
  email: z
    .string()
    .min(1, 'Please enter your email')
    .email('Please enter a valid email'),
  password: z
    .string()
    .min(1, 'Please enter your password'),
  rememberMe: z.boolean().optional().default(false)
});

export const registrationSchema = z.object({
  email: z
    .string()
    .min(1, 'Email is required')
    .email('Please enter a valid email'),
  password: z
    .string()
    .min(1, 'Password is required')
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Include at least one uppercase letter')
    .regex(/[a-z]/, 'Include at least one lowercase letter')
    .regex(/[0-9]/, 'Include at least one number'),
  confirmPassword: z
    .string()
    .min(1, 'Please confirm your password')
}).refine(data => data.password === data.confirmPassword, {
  message: 'Passwords do not match',
  path: ['confirmPassword']
});

export const forgotPasswordSchema = z.object({
  email: z
    .string()
    .min(1, 'Email is required')
    .email('Please enter a valid email')
});

export const resetPasswordSchema = z.object({
  password: z
    .string()
    .min(8, 'Password must be at least 8 characters'),
  confirmPassword: z.string()
}).refine(data => data.password === data.confirmPassword, {
  message: 'Passwords do not match',
  path: ['confirmPassword']
});
```

```typescript
// schemas/profile.ts
export const profileSchema = z.object({
  firstName: z.string().min(1, 'First name is required'),
  lastName: z.string().min(1, 'Last name is required'),
  email: z.string().email('Invalid email'),
  phone: z
    .string()
    .regex(/^\+?[\d\s-()]+$/, 'Invalid phone number')
    .optional()
    .or(z.literal('')),
  bio: z
    .string()
    .max(500, 'Bio must be 500 characters or less')
    .optional()
});

export const addressSchema = z.object({
  street: z.string().min(1, 'Street address is required'),
  city: z.string().min(1, 'City is required'),
  state: z.string().min(1, 'State is required'),
  zip: z.string().regex(/^\d{5}(-\d{4})?$/, 'Invalid ZIP code'),
  country: z.string().min(1, 'Country is required').default('US')
});
```

```typescript
// schemas/payment.ts
export const paymentSchema = z.object({
  cardName: z.string().min(1, 'Name on card is required'),
  cardNumber: z
    .string()
    .regex(/^\d{13,19}$/, 'Invalid card number')
    .refine(val => luhnCheck(val), 'Invalid card number'),
  expMonth: z
    .string()
    .regex(/^(0[1-9]|1[0-2])$/, 'Invalid month'),
  expYear: z
    .string()
    .regex(/^\d{2}$/, 'Invalid year')
    .refine(val => {
      const year = parseInt(val, 10) + 2000;
      return year >= new Date().getFullYear();
    }, 'Card has expired'),
  cvc: z.string().regex(/^\d{3,4}$/, 'Invalid CVC')
});

// Luhn algorithm for card validation
function luhnCheck(cardNumber: string): boolean {
  let sum = 0;
  let isEven = false;
  
  for (let i = cardNumber.length - 1; i >= 0; i--) {
    let digit = parseInt(cardNumber[i], 10);
    
    if (isEven) {
      digit *= 2;
      if (digit > 9) digit -= 9;
    }
    
    sum += digit;
    isEven = !isEven;
  }
  
  return sum % 10 === 0;
}
```

### Advanced Patterns

#### Conditional Validation

```typescript
const orderSchema = z.object({
  deliveryMethod: z.enum(['shipping', 'pickup']),
  address: z.object({
    street: z.string(),
    city: z.string(),
    zip: z.string()
  }).optional()
}).refine(
  data => {
    if (data.deliveryMethod === 'shipping') {
      return data.address?.street && data.address?.city && data.address?.zip;
    }
    return true;
  },
  {
    message: 'Address is required for shipping',
    path: ['address']
  }
);
```

#### Cross-Field Validation

```typescript
const dateRangeSchema = z.object({
  startDate: z.date(),
  endDate: z.date()
}).refine(
  data => data.endDate >= data.startDate,
  {
    message: 'End date must be after start date',
    path: ['endDate']
  }
);
```

#### Schema Composition

```typescript
// Base schemas
const nameSchema = z.object({
  firstName: z.string().min(1),
  lastName: z.string().min(1)
});

const contactSchema = z.object({
  email: z.string().email(),
  phone: z.string().optional()
});

// Composed schema
const userSchema = nameSchema.merge(contactSchema).extend({
  role: z.enum(['admin', 'user'])
});
```

## Async Validation

For server-side checks (username availability, email uniqueness):

```typescript
// With Zod refine
const usernameSchema = z
  .string()
  .min(3, 'Username must be at least 3 characters')
  .refine(
    async (username) => {
      const response = await fetch(`/api/check-username?u=${encodeURIComponent(username)}`);
      const { available } = await response.json();
      return available;
    },
    { message: 'This username is already taken' }
  );

// With TanStack Form (built-in debouncing)
const form = useForm({
  defaultValues: { username: '' },
  validators: {
    onChangeAsyncDebounceMs: 500,
    onChangeAsync: async ({ value }) => {
      const response = await fetch(`/api/check-username?u=${value.username}`);
      const { available } = await response.json();
      if (!available) {
        return { fields: { username: 'Username is taken' } };
      }
      return undefined;
    }
  }
});
```

### Debounced Validation Helper

```typescript
// utils/debounced-validator.ts
export function createDebouncedValidator<T>(
  validator: (value: T) => Promise<string | undefined>,
  delay: number = 500
) {
  let timeoutId: ReturnType<typeof setTimeout>;
  let latestValue: T;
  
  return (value: T): Promise<string | undefined> => {
    latestValue = value;
    
    return new Promise((resolve) => {
      clearTimeout(timeoutId);
      
      timeoutId = setTimeout(async () => {
        // Only validate if this is still the latest value
        if (value === latestValue) {
          const error = await validator(value);
          resolve(error);
        } else {
          resolve(undefined);
        }
      }, delay);
    });
  };
}

// Usage
const checkUsername = createDebouncedValidator(async (username: string) => {
  const response = await fetch(`/api/check-username?u=${username}`);
  const { available } = await response.json();
  return available ? undefined : 'Username is taken';
}, 500);
```

## Error Messages

### Principles

1. **Specific**: Tell users exactly what's wrong
2. **Actionable**: Tell users how to fix it
3. **Contextual**: Reference the field name
4. **Friendly**: Don't blame the user

### Examples

```typescript
// ❌ BAD: Generic, unhelpful
const badSchema = z.object({
  email: z.string().email(),        // "Invalid"
  password: z.string().min(8),       // "Too short"
  phone: z.string().regex(/^\d+$/)   // "Invalid"
});

// ✅ GOOD: Specific, actionable
const goodSchema = z.object({
  email: z
    .string()
    .min(1, 'Please enter your email address')
    .email('Please enter a valid email (e.g., name@example.com)'),
  password: z
    .string()
    .min(1, 'Please create a password')
    .min(8, 'Password must be at least 8 characters'),
  phone: z
    .string()
    .regex(/^\d{10}$/, 'Please enter a 10-digit phone number')
});
```

### Message Templates

```typescript
// utils/validation-messages.ts
export const messages = {
  required: (field: string) => `Please enter your ${field}`,
  email: 'Please enter a valid email address',
  minLength: (field: string, min: number) => 
    `${field} must be at least ${min} characters`,
  maxLength: (field: string, max: number) => 
    `${field} must be ${max} characters or less`,
  pattern: (field: string, example: string) => 
    `Please enter a valid ${field} (e.g., ${example})`,
  match: (field: string) => `${field} fields must match`,
  unique: (field: string) => `This ${field} is already in use`,
  future: (field: string) => `${field} must be a future date`,
  past: (field: string) => `${field} must be a past date`
};

// Usage
const schema = z.object({
  email: z
    .string()
    .min(1, messages.required('email'))
    .email(messages.email),
  password: z
    .string()
    .min(1, messages.required('password'))
    .min(8, messages.minLength('Password', 8))
});
```

## Validation Timing Utility

```typescript
// utils/validation-timing.ts
export type ValidationMode = 'onBlur' | 'onChange' | 'onSubmit' | 'all';

export interface ValidationTimingConfig {
  /** When to first show errors */
  showErrorsOn: ValidationMode;
  /** When to re-validate after first error */
  revalidateOn: ValidationMode;
  /** Debounce delay for onChange (ms) */
  debounceMs?: number;
}

export const TIMING_PRESETS = {
  /** Default: Reward early, punish late */
  standard: {
    showErrorsOn: 'onBlur',
    revalidateOn: 'onChange'
  } as ValidationTimingConfig,
  
  /** For password strength, character counts */
  realtime: {
    showErrorsOn: 'onChange',
    revalidateOn: 'onChange'
  } as ValidationTimingConfig,
  
  /** For simple, short forms */
  submitOnly: {
    showErrorsOn: 'onSubmit',
    revalidateOn: 'onSubmit'
  } as ValidationTimingConfig,
  
  /** For expensive async validation */
  debounced: {
    showErrorsOn: 'onBlur',
    revalidateOn: 'onChange',
    debounceMs: 500
  } as ValidationTimingConfig
} as const;

// React Hook Form mapping
export function toRHFConfig(timing: ValidationTimingConfig) {
  return {
    mode: timing.showErrorsOn === 'all' ? 'all' : timing.showErrorsOn,
    reValidateMode: timing.revalidateOn === 'all' ? 'onChange' : timing.revalidateOn
  };
}
```

## File Structure

```
form-validation/
├── SKILL.md
├── references/
│   ├── zod-patterns.md         # Deep-dive Zod patterns
│   ├── timing-research.md      # UX research on validation timing
│   └── error-message-guide.md  # Writing good error messages
└── scripts/
    ├── schemas/
    │   ├── auth.ts             # Login, registration, password reset
    │   ├── profile.ts          # User profile, addresses
    │   ├── payment.ts          # Credit cards, billing
    │   └── common.ts           # Reusable field schemas
    ├── validation-timing.ts    # Timing utilities
    ├── async-validator.ts      # Debounced async validation
    └── messages.ts             # Error message templates
```

## Framework Integration

| Framework | Adapter | Import |
|-----------|---------|--------|
| React Hook Form | @hookform/resolvers/zod | `zodResolver(schema)` |
| TanStack Form | @tanstack/zod-form-adapter | `zodValidator()` |
| VeeValidate | @vee-validate/zod | `toTypedSchema(schema)` |
| Vanilla | Direct | `schema.safeParse(data)` |

## Reference

- `references/zod-patterns.md` — Complete Zod API patterns
- `references/timing-research.md` — UX research backing timing decisions
- `references/error-message-guide.md` — Writing effective error messages
