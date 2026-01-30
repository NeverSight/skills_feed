---
name: composable-svelte-forms
description: Form patterns and validation for Composable Svelte. Use when building forms, validating user input, or integrating Zod schemas. Covers FormConfig, createFormReducer, field-level validation, async validation, form state management, and reactive wrapper patterns.
---

# Composable Svelte Forms

This skill covers form patterns, Zod validation integration, and state management for forms in Composable Svelte applications.

---

## FORMS SYSTEM

### Integrated Mode (Recommended)

**When**: Complex apps where parent needs to observe form submission, validation, and integrate with other state.

---

## COMPLETE EXAMPLE

### 1. Define Zod Schema

```typescript
import { z } from 'zod';

const contactSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  email: z.string().email('Invalid email address'),
  message: z.string().min(10, 'Message must be at least 10 characters')
});

type ContactData = z.infer<typeof contactSchema>;
```

### 2. Create Form Config

```typescript
import type { FormConfig } from '@composable-svelte/core/components/form';

export const contactFormConfig: FormConfig<ContactData> = {
  schema: contactSchema,
  initialData: { name: '', email: '', message: '' },
  mode: 'all', // Validate on blur, change, and submit
  debounceMs: 500,
  onSubmit: async (data) => {
    const result = await api.submitContact(data);
    return result;
  }
};
```

### 3. Parent State

```typescript
interface AppState {
  contactForm: FormState<ContactData>;
  submissions: Submission[];
  successMessage: string | null;
}
```

### 4. Parent Actions

```typescript
type AppAction =
  | { type: 'contactForm'; action: FormAction<ContactData> }
  | { type: 'clearSuccessMessage' };
```

### 5. Parent Reducer

```typescript
import { createFormReducer, scope } from '@composable-svelte/core';

const formReducer = createFormReducer(contactFormConfig);

const appReducer: Reducer<AppState, AppAction> = (state, action, deps) => {
  switch (action.type) {
    case 'contactForm': {
      const [formState, formEffect] = formReducer(
        state.contactForm,
        action.action,
        deps
      );

      const newState = { ...state, contactForm: formState };
      const effect = Effect.map(formEffect, (fa): AppAction => ({
        type: 'contactForm',
        action: fa
      }));

      // Observe submission success
      if (action.action.type === 'submissionSucceeded') {
        return [
          {
            ...newState,
            submissions: [...state.submissions, {
              id: crypto.randomUUID(),
              data: formState.data,
              timestamp: Date.now()
            }],
            successMessage: 'Thanks for contacting us!'
          },
          Effect.batch(
            effect,
            Effect.afterDelay(3000, (d) => d({ type: 'clearSuccessMessage' }))
          )
        ];
      }

      return [newState, effect];
    }

    case 'clearSuccessMessage':
      return [{ ...state, successMessage: null }, Effect.none()];

    default:
      return [state, Effect.none()];
  }
};
```

### 6. Component - Reactive Wrapper

**CRITICAL**: Use reactive wrapper pattern for forms to integrate form state with parent state.

```svelte
<script lang="ts">
  import { FormField, Button } from '@composable-svelte/core/components';

  export let store: Store<AppState, AppAction>;

  // Reactive wrapper for form store
  let formStoreState = $state(store.state.contactForm);

  $effect(() => {
    formStoreState = store.state.contactForm;
  });

  const formStore = {
    get state() { return formStoreState; },
    dispatch(action: FormAction<ContactData>) {
      store.dispatch({ type: 'contactForm', action });
    }
  };
</script>

{#if $store.successMessage}
  <div class="success">{$store.successMessage}</div>
{/if}

<form onsubmit={(e) => { e.preventDefault(); formStore.dispatch({ type: 'submit' }); }}>
  <FormField
    field="name"
    send={(action) => formStore.dispatch(action)}
    state={formStore.state}
  >
    <label>Name</label>
    <input type="text" />
  </FormField>

  <FormField
    field="email"
    send={(action) => formStore.dispatch(action)}
    state={formStore.state}
  >
    <label>Email</label>
    <input type="email" />
  </FormField>

  <FormField
    field="message"
    send={(action) => formStore.dispatch(action)}
    state={formStore.state}
  >
    <label>Message</label>
    <textarea rows={4} />
  </FormField>

  <Button
    type="submit"
    disabled={formStore.state.isSubmitting || Object.keys(formStore.state.errors).length > 0}
  >
    {formStore.state.isSubmitting ? 'Submitting...' : 'Submit'}
  </Button>
</form>
```

---

## KEY CONCEPTS

### Reactive Wrapper Pattern

**Why needed**: Forms need to integrate with parent state while maintaining reactive updates.

```typescript
// Reactive wrapper for form store
let formStoreState = $state(store.state.contactForm);

$effect(() => {
  formStoreState = store.state.contactForm;
});

const formStore = {
  get state() { return formStoreState; },
  dispatch(action: FormAction<ContactData>) {
    store.dispatch({ type: 'contactForm', action });
  }
};
```

**What it does**:
- Creates reactive local state that tracks form state from parent
- Provides dispatch method that wraps actions for parent
- Enables FormField components to work with scoped state

---

### Parent Observation

**Critical Pattern**: Parent can observe form events to react to submission, validation failures, etc.

```typescript
// Observe submission success
if (action.action.type === 'submissionSucceeded') {
  return [
    {
      ...newState,
      submissions: [...state.submissions, {
        id: crypto.randomUUID(),
        data: formState.data,
        timestamp: Date.now()
      }],
      successMessage: 'Thanks for contacting us!'
    },
    Effect.batch(
      effect,
      Effect.afterDelay(3000, (d) => d({ type: 'clearSuccessMessage' }))
    )
  ];
}

// Observe submission failure
if (action.action.type === 'submissionFailed') {
  return [
    newState,
    Effect.batch(
      effect,
      Effect.fireAndForget(async () => {
        toast.error('Submission failed. Please try again.');
      })
    )
  ];
}

// Observe validation failure
if (action.action.type === 'validationFailed') {
  return [
    newState,
    Effect.batch(
      effect,
      Effect.fireAndForget(async () => {
        toast.error('Please fix validation errors.');
      })
    )
  ];
}
```

---

## FORM STATE REFERENCE

### FormState Type

```typescript
interface FormState<T> {
  data: T;                          // Current form data
  errors: Record<string, string>;   // Field-level errors
  isSubmitting: boolean;            // ✅ USE THIS for loading state
  touched: Record<string, boolean>; // Which fields have been touched
  isDirty: boolean;                 // Has form been modified?
  isValid: boolean;                 // Are all fields valid?
}
```

### CRITICAL: Use isSubmitting

**❌ WRONG**:
```typescript
{#if formStore.state.submission.status === 'submitting'}
  Loading...
{/if}
```

**✅ CORRECT**:
```typescript
{#if formStore.state.isSubmitting}
  Loading...
{/if}
```

**WHY**: Use `isSubmitting` boolean, not `submission.status`. Simpler API, less nesting.

---

## FORM ACTIONS

### FormAction Types

```typescript
type FormAction<T> =
  | { type: 'fieldChanged'; field: keyof T; value: any }
  | { type: 'fieldBlurred'; field: keyof T }
  | { type: 'submit' }
  | { type: 'reset' }
  | { type: 'submissionSucceeded' }
  | { type: 'submissionFailed'; error: string }
  | { type: 'validationFailed'; errors: Record<string, string> };
```

### Field-Level Errors

```typescript
// Errors are automatically populated from Zod validation
{#if formStore.state.errors.email}
  <span class="error">{formStore.state.errors.email}</span>
{/if}
```

---

## ASYNC VALIDATION

### Define Async Validators in Schema

```typescript
const schema = z.object({
  username: z.string().refine(
    async (username) => {
      const available = await api.checkUsername(username);
      return available;
    },
    { message: 'Username is already taken' }
  ),
  email: z.string().email().refine(
    async (email) => {
      const exists = await api.checkEmail(email);
      return !exists;
    },
    { message: 'Email already registered' }
  )
});
```

### Async Validation Flow

1. User types in field
2. On blur or after debounce, async validator runs
3. Loading state shown during validation
4. Error displayed if validation fails

---

## FORM CONFIGURATION OPTIONS

### FormConfig Reference

```typescript
interface FormConfig<T> {
  schema: z.ZodSchema<T>;           // Zod schema for validation
  initialData: T;                   // Initial form values
  mode: 'all' | 'blur' | 'submit';  // When to validate
  debounceMs?: number;              // Debounce validation (default: 300ms)
  onSubmit: (data: T) => Promise<Result>; // Submit handler
}
```

### Validation Modes

- `'all'` - Validate on blur, change, and submit (recommended for most forms)
- `'blur'` - Validate only on blur and submit (better UX for long forms)
- `'submit'` - Validate only on submit (fastest, but less feedback)

---

## COMPLETE FORM EXAMPLES

### Example 1: Registration Form

```typescript
// Schema
const registrationSchema = z.object({
  username: z.string().min(3, 'Username must be at least 3 characters'),
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  confirmPassword: z.string()
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ['confirmPassword']
});

// Config
const registrationFormConfig: FormConfig<RegistrationData> = {
  schema: registrationSchema,
  initialData: { username: '', email: '', password: '', confirmPassword: '' },
  mode: 'blur',
  debounceMs: 500,
  onSubmit: async (data) => {
    const result = await api.register(data);
    return result;
  }
};

// Component
<script lang="ts">
  import { FormField, Button } from '@composable-svelte/core/components';

  let formStoreState = $state(store.state.registrationForm);

  $effect(() => {
    formStoreState = store.state.registrationForm;
  });

  const formStore = {
    get state() { return formStoreState; },
    dispatch(action) {
      store.dispatch({ type: 'registrationForm', action });
    }
  };
</script>

<form onsubmit={(e) => { e.preventDefault(); formStore.dispatch({ type: 'submit' }); }}>
  <FormField field="username" send={(a) => formStore.dispatch(a)} state={formStore.state}>
    <label>Username</label>
    <input type="text" />
  </FormField>

  <FormField field="email" send={(a) => formStore.dispatch(a)} state={formStore.state}>
    <label>Email</label>
    <input type="email" />
  </FormField>

  <FormField field="password" send={(a) => formStore.dispatch(a)} state={formStore.state}>
    <label>Password</label>
    <input type="password" />
  </FormField>

  <FormField field="confirmPassword" send={(a) => formStore.dispatch(a)} state={formStore.state}>
    <label>Confirm Password</label>
    <input type="password" />
  </FormField>

  <Button type="submit" disabled={formStore.state.isSubmitting || !formStore.state.isValid}>
    {formStore.state.isSubmitting ? 'Creating Account...' : 'Create Account'}
  </Button>
</form>
```

### Example 2: Multi-Step Form

```typescript
// State
interface MultiStepFormState {
  step: 1 | 2 | 3;
  step1: FormState<Step1Data>;
  step2: FormState<Step2Data>;
  step3: FormState<Step3Data>;
}

// Actions
type MultiStepFormAction =
  | { type: 'step1'; action: FormAction<Step1Data> }
  | { type: 'step2'; action: FormAction<Step2Data> }
  | { type: 'step3'; action: FormAction<Step3Data> }
  | { type: 'nextStep' }
  | { type: 'prevStep' };

// Reducer
case 'nextStep': {
  // Validate current step before proceeding
  const currentStep = state.step;
  if (currentStep === 1 && !state.step1.isValid) {
    return [state, Effect.none()];
  }
  if (currentStep === 2 && !state.step2.isValid) {
    return [state, Effect.none()];
  }

  return [
    { ...state, step: (state.step + 1) as 1 | 2 | 3 },
    Effect.none()
  ];
}

case 'step3': {
  const [formState, formEffect] = step3Reducer(state.step3, action.action, deps);

  // Observe final submission
  if (action.action.type === 'submissionSucceeded') {
    const allData = {
      ...state.step1.data,
      ...state.step2.data,
      ...formState.data
    };

    return [
      { ...state, step3: formState },
      Effect.batch(
        Effect.map(formEffect, (fa): MultiStepFormAction => ({ type: 'step3', action: fa })),
        Effect.run(async (d) => {
          await api.submitCompleteForm(allData);
          d({ type: 'formCompleted' });
        })
      )
    ];
  }

  return [
    { ...state, step3: formState },
    Effect.map(formEffect, (fa): MultiStepFormAction => ({ type: 'step3', action: fa }))
  ];
}

// Component
{#if state.step === 1}
  <Step1Form store={step1Store} />
  <Button onclick={() => store.dispatch({ type: 'nextStep' })}>Next</Button>
{:else if state.step === 2}
  <Step2Form store={step2Store} />
  <Button onclick={() => store.dispatch({ type: 'prevStep' })}>Back</Button>
  <Button onclick={() => store.dispatch({ type: 'nextStep' })}>Next</Button>
{:else}
  <Step3Form store={step3Store} />
  <Button onclick={() => store.dispatch({ type: 'prevStep' })}>Back</Button>
  <Button onclick={() => formStore.dispatch({ type: 'submit' })}>Submit</Button>
{/if}
```

---

## COMMON ANTI-PATTERNS

### 1. Wrong Form State Access

#### ❌ WRONG
```typescript
{#if formStore.state.submission.status === 'submitting'}
  Loading...
{/if}
```

#### ✅ CORRECT
```typescript
{#if formStore.state.isSubmitting}
  Loading...
{/if}
```

**WHY**: Use `isSubmitting` boolean, not `submission.status`. Simpler API, less nesting.

---

### 2. Not Using Reactive Wrapper

#### ❌ WRONG
```svelte
<script lang="ts">
  // Directly using parent store in form fields
</script>

<FormField
  field="name"
  send={(action) => store.dispatch({ type: 'contactForm', action })}
  state={store.state.contactForm}
>
  <input type="text" />
</FormField>
```

#### ✅ CORRECT
```svelte
<script lang="ts">
  // Create reactive wrapper
  let formStoreState = $state(store.state.contactForm);

  $effect(() => {
    formStoreState = store.state.contactForm;
  });

  const formStore = {
    get state() { return formStoreState; },
    dispatch(action) {
      store.dispatch({ type: 'contactForm', action });
    }
  };
</script>

<FormField
  field="name"
  send={(action) => formStore.dispatch(action)}
  state={formStore.state}
>
  <input type="text" />
</FormField>
```

**WHY**: Reactive wrapper ensures proper reactivity and cleaner component code.

---

### 3. Not Observing Submission Events

#### ❌ WRONG
```typescript
case 'contactForm': {
  const [formState, formEffect] = formReducer(state.contactForm, action.action, deps);

  // Just return new state, don't observe events
  return [
    { ...state, contactForm: formState },
    Effect.map(formEffect, (fa): AppAction => ({ type: 'contactForm', action: fa }))
  ];
}
```

#### ✅ CORRECT
```typescript
case 'contactForm': {
  const [formState, formEffect] = formReducer(state.contactForm, action.action, deps);

  const newState = { ...state, contactForm: formState };
  const effect = Effect.map(formEffect, (fa): AppAction => ({ type: 'contactForm', action: fa }));

  // Observe submission success
  if (action.action.type === 'submissionSucceeded') {
    return [
      {
        ...newState,
        submissions: [...state.submissions, { data: formState.data, timestamp: Date.now() }],
        successMessage: 'Form submitted successfully!'
      },
      Effect.batch(
        effect,
        Effect.afterDelay(3000, (d) => d({ type: 'clearSuccessMessage' }))
      )
    ];
  }

  return [newState, effect];
}
```

**WHY**: Parent needs to react to form submission to show success messages, navigate, etc.

---

## DECISION TOOLS

### Form Integration Decision

```
Do you need parent to observe form events?
│
├─ YES (most cases)
│  └─ Integrated Mode
│     - Parent state includes FormState<T>
│     - Parent observes submissionSucceeded/submissionFailed
│     - Use reactive wrapper in component
│
└─ NO (standalone forms, prototypes)
   └─ Standalone Mode
      - Create store directly in component
      - Handle submission locally
      - Simpler but less composable
```

### Validation Mode Selection

```
What's the form complexity?
│
├─ Short form (1-3 fields)
│  └─ mode: 'all' (instant feedback)
│
├─ Medium form (4-8 fields)
│  └─ mode: 'blur' (validate on blur + submit)
│
└─ Long form (8+ fields)
   └─ mode: 'submit' (validate only on submit)
```

---

## CHECKLISTS

### Form Feature Checklist

- [ ] 1. Define Zod schema
- [ ] 2. Create FormConfig with schema and onSubmit
- [ ] 3. Add FormState to parent state
- [ ] 4. Use createFormReducer + scope in parent reducer
- [ ] 5. Parent observes submissionSucceeded/submissionFailed
- [ ] 6. Create reactive wrapper in component ($state + $effect)
- [ ] 7. Use formStore.state.isSubmitting (NOT submission.status)
- [ ] 8. Test with TestStore (see composable-svelte-testing skill)

---

## TEMPLATES

### Form Integration Template

```typescript
// config.ts
import { z } from 'zod';
import type { FormConfig } from '@composable-svelte/core/components/form';

const schema = z.object({
  name: z.string().min(1, 'Required'),
  email: z.string().email('Invalid email')
});

type FormData = z.infer<typeof schema>;

export const formConfig: FormConfig<FormData> = {
  schema,
  initialData: { name: '', email: '' },
  mode: 'all',
  debounceMs: 500,
  onSubmit: async (data) => {
    const result = await api.submit(data);
    return result;
  }
};

// Parent state and reducer
interface AppState {
  contactForm: FormState<ContactData>;
  submissions: Submission[];
}

const formReducer = createFormReducer(formConfig);

case 'contactForm': {
  const [formState, formEffect] = formReducer(state.contactForm, action.action, deps);
  const newState = { ...state, contactForm: formState };

  if (action.action.type === 'submissionSucceeded') {
    return [
      {
        ...newState,
        submissions: [...state.submissions, { data: formState.data, timestamp: Date.now() }]
      },
      Effect.map(formEffect, (fa): AppAction => ({ type: 'contactForm', action: fa }))
    ];
  }

  return [newState, Effect.map(formEffect, (fa): AppAction => ({ type: 'contactForm', action: fa }))];
}

// Component.svelte
<script lang="ts">
  import { FormField, Button } from '@composable-svelte/core/components';

  let formStoreState = $state(store.state.contactForm);

  $effect(() => {
    formStoreState = store.state.contactForm;
  });

  const formStore = {
    get state() { return formStoreState; },
    dispatch(action) {
      store.dispatch({ type: 'contactForm', action });
    }
  };
</script>

<form onsubmit={(e) => { e.preventDefault(); formStore.dispatch({ type: 'submit' }); }}>
  <FormField field="name" send={(a) => formStore.dispatch(a)} state={formStore.state}>
    <label>Name</label>
    <input type="text" />
  </FormField>

  <FormField field="email" send={(a) => formStore.dispatch(a)} state={formStore.state}>
    <label>Email</label>
    <input type="email" />
  </FormField>

  <Button type="submit" disabled={formStore.state.isSubmitting}>
    Submit
  </Button>
</form>
```

---

## SUMMARY

This skill covers form patterns for Composable Svelte:

1. **Integrated Mode**: Forms integrated with parent state
2. **Reactive Wrapper Pattern**: $state + $effect for form integration
3. **Parent Observation**: React to submission success/failure
4. **Zod Integration**: Schema-based validation
5. **Field-Level Errors**: Automatic error handling
6. **Async Validation**: Server-side validation support
7. **CRITICAL**: Use `isSubmitting`, not `submission.status`

**Remember**: Use reactive wrapper pattern for forms, observe submission events in parent, test with TestStore (see **composable-svelte-testing** skill).

For core architecture, see **composable-svelte-core** skill.
For navigation with forms, see **composable-svelte-navigation** skill.
For testing forms, see **composable-svelte-testing** skill.
For component library, see **composable-svelte-components** skill.
