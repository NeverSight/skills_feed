---
name: form-react
description: Production-ready React form patterns using React Hook Form (default) and TanStack Form with Zod integration. Use when building forms in React applications. Implements reward-early-punish-late validation timing.
---

# Form React

Production React form patterns. Default stack: **React Hook Form + Zod**.

## Quick Start

```bash
npm install react-hook-form @hookform/resolvers zod
```

```tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

// 1. Define schema
const schema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Min 8 characters')
});

type FormData = z.infer<typeof schema>;

// 2. Use form
function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
    mode: 'onBlur' // Reward early, punish late
  });

  return (
    <form onSubmit={handleSubmit(data => console.log(data))}>
      <input {...register('email')} type="email" autoComplete="email" />
      {errors.email && <span>{errors.email.message}</span>}
      
      <input {...register('password')} type="password" autoComplete="current-password" />
      {errors.password && <span>{errors.password.message}</span>}
      
      <button type="submit">Sign in</button>
    </form>
  );
}
```

## When to Use Which

| Criteria | React Hook Form | TanStack Form |
|----------|-----------------|---------------|
| Performance | ✅ Best (uncontrolled) | Good (controlled) |
| Bundle size | 12KB | ~15KB |
| TypeScript | Good | ✅ Excellent |
| Cross-framework | ❌ React only | ✅ Multi-framework |
| React Native | Requires workarounds | ✅ Native support |
| Built-in async validation | Manual | ✅ Built-in debouncing |
| Ecosystem | ✅ Mature (4+ years) | Growing |

**Default: React Hook Form** — Better performance for most React web apps.

**Use TanStack Form when:**
- Building cross-framework component libraries
- Need strict controlled component behavior
- Heavy async validation (username checks)
- React Native applications

## React Hook Form Patterns

### Basic Form

```tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { loginSchema, type LoginFormData } from './schemas';

export function LoginForm({ onSubmit }: { onSubmit: (data: LoginFormData) => void }) {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting, touchedFields }
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
    mode: 'onBlur',           // First validation on blur (punish late)
    reValidateMode: 'onChange' // Re-validate on change (real-time correction)
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)} noValidate>
      <div className="form-field">
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          autoComplete="email"
          aria-invalid={!!errors.email}
          {...register('email')}
        />
        {touchedFields.email && errors.email && (
          <span role="alert">{errors.email.message}</span>
        )}
      </div>

      <div className="form-field">
        <label htmlFor="password">Password</label>
        <input
          id="password"
          type="password"
          autoComplete="current-password"
          aria-invalid={!!errors.password}
          {...register('password')}
        />
        {touchedFields.password && errors.password && (
          <span role="alert">{errors.password.message}</span>
        )}
      </div>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Signing in...' : 'Sign in'}
      </button>
    </form>
  );
}
```

### Reusable Form Field Component

```tsx
// FormField.tsx
import { useFormContext } from 'react-hook-form';
import { ReactNode } from 'react';

interface FormFieldProps {
  name: string;
  label: string;
  type?: string;
  autoComplete?: string;
  hint?: string;
  required?: boolean;
  children?: ReactNode;
}

export function FormField({
  name,
  label,
  type = 'text',
  autoComplete,
  hint,
  required,
  children
}: FormFieldProps) {
  const {
    register,
    formState: { errors, touchedFields }
  } = useFormContext();

  const error = errors[name];
  const touched = touchedFields[name];
  const showError = touched && error;
  const showValid = touched && !error;

  return (
    <div className={`form-field ${showError ? 'error' : ''} ${showValid ? 'valid' : ''}`}>
      <label htmlFor={name}>
        {label}
        {required && <span aria-hidden="true">*</span>}
      </label>
      
      {hint && <span className="hint">{hint}</span>}
      
      {children || (
        <input
          id={name}
          type={type}
          autoComplete={autoComplete}
          aria-invalid={!!error}
          aria-describedby={error ? `${name}-error` : undefined}
          {...register(name)}
        />
      )}
      
      {showError && (
        <span id={`${name}-error`} role="alert" className="error-message">
          {error.message as string}
        </span>
      )}
    </div>
  );
}
```

### Using FormProvider for Nested Components

```tsx
// Form wrapper
import { FormProvider, useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

export function CheckoutForm() {
  const methods = useForm({
    resolver: zodResolver(checkoutSchema),
    mode: 'onBlur'
  });

  return (
    <FormProvider {...methods}>
      <form onSubmit={methods.handleSubmit(onSubmit)}>
        <ContactSection />
        <ShippingSection />
        <PaymentSection />
        <button type="submit">Place Order</button>
      </form>
    </FormProvider>
  );
}

// Nested section component
function ContactSection() {
  return (
    <fieldset>
      <legend>Contact Information</legend>
      <FormField name="email" label="Email" type="email" autoComplete="email" required />
      <FormField name="phone" label="Phone" type="tel" autoComplete="tel" />
    </fieldset>
  );
}
```

### Watching Values (Real-time)

```tsx
import { useForm, useWatch } from 'react-hook-form';

function RegistrationForm() {
  const { register, control } = useForm();
  
  // Watch password for strength meter
  const password = useWatch({ control, name: 'password', defaultValue: '' });
  
  return (
    <form>
      <input type="password" {...register('password')} />
      <PasswordStrength password={password} />
    </form>
  );
}
```

### Conditional Fields

```tsx
import { useFormContext, useWatch } from 'react-hook-form';

function ConditionalField({ watchField, condition, children }) {
  const { control } = useFormContext();
  const value = useWatch({ control, name: watchField });
  
  if (!condition(value)) return null;
  return <>{children}</>;
}

// Usage
<ConditionalField watchField="hasCompany" condition={(val) => val === true}>
  <FormField name="companyName" label="Company Name" />
</ConditionalField>
```

### Async Validation (Username Check)

```tsx
import { useForm } from 'react-hook-form';

function RegistrationForm() {
  const { register, setError, clearErrors } = useForm();
  
  const checkUsername = async (username: string) => {
    if (username.length < 3) return;
    
    const response = await fetch(`/api/check-username?u=${username}`);
    const { available } = await response.json();
    
    if (!available) {
      setError('username', { type: 'manual', message: 'Username is taken' });
    } else {
      clearErrors('username');
    }
  };

  return (
    <input
      {...register('username')}
      onBlur={(e) => checkUsername(e.target.value)}
    />
  );
}
```

### Form Reset

```tsx
function EditProfileForm({ defaultValues }) {
  const { reset, handleSubmit } = useForm({ defaultValues });
  
  // Reset to new values
  useEffect(() => {
    reset(defaultValues);
  }, [defaultValues, reset]);
  
  // Reset to initial values
  const handleCancel = () => reset();
  
  return (
    <form>
      {/* fields */}
      <button type="button" onClick={handleCancel}>Cancel</button>
      <button type="submit">Save</button>
    </form>
  );
}
```

### Array Fields (Dynamic)

```tsx
import { useFieldArray, useForm } from 'react-hook-form';

function TeamMembersForm() {
  const { control, register } = useForm({
    defaultValues: {
      members: [{ name: '', email: '' }]
    }
  });
  
  const { fields, append, remove } = useFieldArray({
    control,
    name: 'members'
  });

  return (
    <form>
      {fields.map((field, index) => (
        <div key={field.id}>
          <input {...register(`members.${index}.name`)} placeholder="Name" />
          <input {...register(`members.${index}.email`)} placeholder="Email" />
          <button type="button" onClick={() => remove(index)}>Remove</button>
        </div>
      ))}
      
      <button type="button" onClick={() => append({ name: '', email: '' })}>
        Add Member
      </button>
    </form>
  );
}
```

## TanStack Form Patterns

### Basic Form

```tsx
import { useForm } from '@tanstack/react-form';
import { zodValidator } from '@tanstack/zod-form-adapter';
import { loginSchema } from './schemas';

function LoginForm() {
  const form = useForm({
    defaultValues: {
      email: '',
      password: ''
    },
    onSubmit: async ({ value }) => {
      await login(value);
    },
    validatorAdapter: zodValidator()
  });

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        e.stopPropagation();
        form.handleSubmit();
      }}
    >
      <form.Field
        name="email"
        validators={{ onBlur: loginSchema.shape.email }}
      >
        {(field) => (
          <div className="form-field">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              autoComplete="email"
              value={field.state.value}
              onChange={(e) => field.handleChange(e.target.value)}
              onBlur={field.handleBlur}
            />
            {field.state.meta.isTouched && field.state.meta.errors.length > 0 && (
              <span role="alert">{field.state.meta.errors[0]}</span>
            )}
          </div>
        )}
      </form.Field>

      <form.Field
        name="password"
        validators={{ onBlur: loginSchema.shape.password }}
      >
        {(field) => (
          <div className="form-field">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              autoComplete="current-password"
              value={field.state.value}
              onChange={(e) => field.handleChange(e.target.value)}
              onBlur={field.handleBlur}
            />
            {field.state.meta.isTouched && field.state.meta.errors.length > 0 && (
              <span role="alert">{field.state.meta.errors[0]}</span>
            )}
          </div>
        )}
      </form.Field>

      <form.Subscribe selector={(state) => [state.canSubmit, state.isSubmitting]}>
        {([canSubmit, isSubmitting]) => (
          <button type="submit" disabled={!canSubmit}>
            {isSubmitting ? 'Signing in...' : 'Sign in'}
          </button>
        )}
      </form.Subscribe>
    </form>
  );
}
```

### Async Validation with Debouncing

```tsx
<form.Field
  name="username"
  validators={{
    onBlur: loginSchema.shape.username,
    onChangeAsyncDebounceMs: 500,
    onChangeAsync: async ({ value }) => {
      const response = await fetch(`/api/check-username?u=${value}`);
      const { available } = await response.json();
      return available ? undefined : 'Username is taken';
    }
  }}
>
  {(field) => (
    <div>
      <input
        value={field.state.value}
        onChange={(e) => field.handleChange(e.target.value)}
        onBlur={field.handleBlur}
      />
      {field.state.meta.isValidating && <span>Checking...</span>}
      {field.state.meta.errors[0] && <span>{field.state.meta.errors[0]}</span>}
    </div>
  )}
</form.Field>
```

### Linked Fields (Password Confirmation)

```tsx
<form.Field
  name="confirmPassword"
  validators={{
    onChangeListenTo: ['password'],
    onChange: ({ value, fieldApi }) => {
      const password = fieldApi.form.getFieldValue('password');
      return value !== password ? 'Passwords do not match' : undefined;
    }
  }}
>
  {(field) => (
    <input
      type="password"
      value={field.state.value}
      onChange={(e) => field.handleChange(e.target.value)}
    />
  )}
</form.Field>
```

## Common Patterns

### Form with Server Errors

```tsx
function LoginForm() {
  const [serverError, setServerError] = useState<string | null>(null);
  
  const { handleSubmit, setError } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema)
  });

  const onSubmit = async (data: LoginFormData) => {
    try {
      setServerError(null);
      await login(data);
    } catch (error) {
      if (error.field) {
        // Field-specific error
        setError(error.field, { message: error.message });
      } else {
        // General error
        setServerError(error.message);
      }
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {serverError && (
        <div role="alert" className="form-error">
          {serverError}
        </div>
      )}
      {/* fields */}
    </form>
  );
}
```

### Loading State

```tsx
function ContactForm() {
  const { handleSubmit, formState: { isSubmitting } } = useForm();

  return (
    <form onSubmit={handleSubmit(onSubmit)} aria-busy={isSubmitting}>
      {/* fields */}
      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? (
          <>
            <Spinner aria-hidden="true" />
            <span className="sr-only">Sending message...</span>
            Sending...
          </>
        ) : (
          'Send Message'
        )}
      </button>
    </form>
  );
}
```

### Focus First Error

```tsx
import { useForm } from 'react-hook-form';
import { useRef, useEffect } from 'react';

function MyForm() {
  const formRef = useRef<HTMLFormElement>(null);
  const { handleSubmit, formState: { errors, isSubmitSuccessful } } = useForm();
  
  // Focus first error after failed submit
  useEffect(() => {
    if (Object.keys(errors).length > 0) {
      const firstError = formRef.current?.querySelector('[aria-invalid="true"]');
      (firstError as HTMLElement)?.focus();
    }
  }, [errors]);

  return <form ref={formRef}>{/* fields */}</form>;
}
```

## File Structure

```
form-react/
├── SKILL.md
├── references/
│   ├── rhf-patterns.md         # React Hook Form deep-dive
│   ├── tanstack-patterns.md    # TanStack Form deep-dive
│   └── migration-guide.md      # Formik → RHF migration
└── scripts/
    ├── rhf-form-builder.tsx    # RHF form patterns
    ├── tanstack-form-builder.tsx # TanStack patterns
    ├── form-field.tsx          # Reusable field component
    ├── use-form-field.ts       # Custom hook
    └── schemas/                # Shared with form-validation
        ├── auth.ts
        ├── profile.ts
        └── payment.ts
```

## Integration with Other Skills

```tsx
// Combine: form-react + form-validation + form-accessibility + form-security
import { useForm, FormProvider } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { loginSchema } from 'form-validation/schemas/auth';
import { FormField } from 'form-accessibility/aria-form-wrapper';
import { AUTOCOMPLETE } from 'form-security/autocomplete-config';

function LoginForm({ onSubmit }) {
  const methods = useForm({
    resolver: zodResolver(loginSchema),
    mode: 'onBlur'
  });

  return (
    <FormProvider {...methods}>
      <form onSubmit={methods.handleSubmit(onSubmit)}>
        <FormField
          label="Email"
          name="email"
          error={methods.formState.errors.email?.message}
          touched={methods.formState.touchedFields.email}
          required
        >
          <input
            type="email"
            autoComplete={AUTOCOMPLETE.email}
            {...methods.register('email')}
          />
        </FormField>
        {/* ... */}
      </form>
    </FormProvider>
  );
}
```

## Reference

- `references/rhf-patterns.md` — Complete React Hook Form patterns
- `references/tanstack-patterns.md` — TanStack Form patterns
- `references/migration-guide.md` — Migrating from Formik
