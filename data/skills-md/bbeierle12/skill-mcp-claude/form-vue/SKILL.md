---
name: form-vue
description: Production-ready Vue form patterns using VeeValidate (default) or Vuelidate with Zod integration. Use when building forms in Vue 3 applications with Composition API.
---

# Form Vue

Production Vue 3 form patterns. Default stack: **VeeValidate + Zod**.

## Quick Start

```bash
npm install vee-validate @vee-validate/zod zod
```

```vue
<script setup lang="ts">
import { useForm, useField } from 'vee-validate';
import { toTypedSchema } from '@vee-validate/zod';
import { z } from 'zod';

// 1. Define schema
const schema = toTypedSchema(z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Min 8 characters')
}));

// 2. Use form
const { handleSubmit, errors } = useForm({ validationSchema: schema });
const { value: email } = useField('email');
const { value: password } = useField('password');

// 3. Handle submit
const onSubmit = handleSubmit((values) => {
  console.log(values);
});
</script>

<template>
  <form @submit="onSubmit">
    <input v-model="email" type="email" autocomplete="email" />
    <span v-if="errors.email">{{ errors.email }}</span>
    
    <input v-model="password" type="password" autocomplete="current-password" />
    <span v-if="errors.password">{{ errors.password }}</span>
    
    <button type="submit">Sign in</button>
  </form>
</template>
```

## When to Use Which

| Criteria | VeeValidate | Vuelidate |
|----------|-------------|-----------|
| API Style | Declarative (schema) | Imperative (rules) |
| Zod Integration | ✅ Native adapter | Manual |
| Bundle Size | ~15KB | ~10KB |
| Component Support | ✅ Built-in Field/Form | Manual binding |
| Async Validation | ✅ Built-in | ✅ Built-in |
| Cross-field Validation | ✅ Easy | More manual |
| Learning Curve | Low | Medium |

**Default: VeeValidate** — Better DX, native Zod support.

**Use Vuelidate when:**
- Need extremely fine-grained control
- Existing Vuelidate codebase
- Prefer imperative validation style

## VeeValidate Patterns

### Basic Form with Composition API

```vue
<script setup lang="ts">
import { useForm, useField } from 'vee-validate';
import { toTypedSchema } from '@vee-validate/zod';
import { loginSchema, type LoginFormData } from './schemas';

const emit = defineEmits<{
  submit: [data: LoginFormData]
}>();

// Form setup
const { handleSubmit, errors, meta } = useForm<LoginFormData>({
  validationSchema: toTypedSchema(loginSchema),
  validateOnMount: false
});

// Field setup
const { value: email, errorMessage: emailError, meta: emailMeta } = useField('email');
const { value: password, errorMessage: passwordError, meta: passwordMeta } = useField('password');
const { value: rememberMe } = useField('rememberMe');

// Submit handler
const onSubmit = handleSubmit((values) => {
  emit('submit', values);
});
</script>

<template>
  <form @submit="onSubmit" novalidate>
    <div class="form-field" :class="{ 'has-error': emailMeta.touched && emailError }">
      <label for="email">Email</label>
      <input
        id="email"
        v-model="email"
        type="email"
        autocomplete="email"
        :aria-invalid="emailMeta.touched && !!emailError"
        :aria-describedby="emailError ? 'email-error' : undefined"
      />
      <span v-if="emailMeta.touched && emailError" id="email-error" role="alert">
        {{ emailError }}
      </span>
    </div>

    <div class="form-field" :class="{ 'has-error': passwordMeta.touched && passwordError }">
      <label for="password">Password</label>
      <input
        id="password"
        v-model="password"
        type="password"
        autocomplete="current-password"
        :aria-invalid="passwordMeta.touched && !!passwordError"
        :aria-describedby="passwordError ? 'password-error' : undefined"
      />
      <span v-if="passwordMeta.touched && passwordError" id="password-error" role="alert">
        {{ passwordError }}
      </span>
    </div>

    <label class="checkbox">
      <input v-model="rememberMe" type="checkbox" />
      Remember me
    </label>

    <button type="submit" :disabled="meta.pending">
      {{ meta.pending ? 'Signing in...' : 'Sign in' }}
    </button>
  </form>
</template>
```

### Reusable FormField Component

```vue
<!-- components/FormField.vue -->
<script setup lang="ts">
import { useField } from 'vee-validate';
import { computed, useId } from 'vue';

interface Props {
  name: string;
  label: string;
  type?: string;
  autocomplete?: string;
  hint?: string;
  required?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  type: 'text'
});

const fieldId = useId();
const errorId = `${fieldId}-error`;
const hintId = `${fieldId}-hint`;

const { value, errorMessage, meta } = useField(() => props.name);

const showError = computed(() => meta.touched && !!errorMessage.value);
const showValid = computed(() => meta.touched && !errorMessage.value && meta.valid);

const describedBy = computed(() => {
  const ids = [];
  if (props.hint) ids.push(hintId);
  if (showError.value) ids.push(errorId);
  return ids.length > 0 ? ids.join(' ') : undefined;
});
</script>

<template>
  <div 
    class="form-field" 
    :class="{ 
      'form-field--error': showError,
      'form-field--valid': showValid
    }"
  >
    <label :for="fieldId">
      {{ label }}
      <span v-if="required" class="required" aria-hidden="true">*</span>
    </label>
    
    <span v-if="hint" :id="hintId" class="hint">{{ hint }}</span>
    
    <div class="input-wrapper">
      <input
        :id="fieldId"
        v-model="value"
        :type="type"
        :autocomplete="autocomplete"
        :aria-invalid="showError"
        :aria-describedby="describedBy"
        :aria-required="required"
      />
      
      <span v-if="showValid" class="icon icon--valid" aria-hidden="true">✓</span>
      <span v-if="showError" class="icon icon--error" aria-hidden="true">✗</span>
    </div>
    
    <span v-if="showError" :id="errorId" class="error" role="alert">
      {{ errorMessage }}
    </span>
  </div>
</template>
```

### Using FormField Component

```vue
<script setup lang="ts">
import { useForm } from 'vee-validate';
import { toTypedSchema } from '@vee-validate/zod';
import { loginSchema } from './schemas';
import FormField from './FormField.vue';

const { handleSubmit, meta } = useForm({
  validationSchema: toTypedSchema(loginSchema)
});

const onSubmit = handleSubmit((values) => {
  console.log(values);
});
</script>

<template>
  <form @submit="onSubmit" novalidate>
    <FormField
      name="email"
      label="Email"
      type="email"
      autocomplete="email"
      required
    />
    
    <FormField
      name="password"
      label="Password"
      type="password"
      autocomplete="current-password"
      required
    />
    
    <button type="submit" :disabled="meta.pending">
      Sign in
    </button>
  </form>
</template>
```

### Form with Initial Values

```vue
<script setup lang="ts">
import { useForm } from 'vee-validate';
import { toTypedSchema } from '@vee-validate/zod';
import { profileSchema } from './schemas';

interface Props {
  initialData?: {
    firstName: string;
    lastName: string;
    email: string;
  }
}

const props = defineProps<Props>();

const { handleSubmit, resetForm } = useForm({
  validationSchema: toTypedSchema(profileSchema),
  initialValues: props.initialData
});

// Reset to initial values
const handleCancel = () => {
  resetForm();
};

// Reset to new values
const handleReset = (newValues: typeof props.initialData) => {
  resetForm({ values: newValues });
};
</script>
```

### Async Validation (Username Check)

```vue
<script setup lang="ts">
import { useField } from 'vee-validate';
import { z } from 'zod';
import { toTypedSchema } from '@vee-validate/zod';

// Schema with async validation
const usernameSchema = z.string()
  .min(3, 'Username must be at least 3 characters')
  .refine(async (username) => {
    const response = await fetch(`/api/check-username?u=${username}`);
    const { available } = await response.json();
    return available;
  }, 'Username is already taken');

const { value, errorMessage, meta } = useField('username', toTypedSchema(usernameSchema));
</script>

<template>
  <div class="form-field">
    <label for="username">Username</label>
    <input
      id="username"
      v-model="value"
      type="text"
      autocomplete="username"
    />
    <span v-if="meta.pending" class="loading">Checking...</span>
    <span v-else-if="errorMessage" class="error">{{ errorMessage }}</span>
  </div>
</template>
```

### Cross-Field Validation (Password Confirmation)

```vue
<script setup lang="ts">
import { useForm, useField } from 'vee-validate';
import { toTypedSchema } from '@vee-validate/zod';
import { z } from 'zod';

const schema = toTypedSchema(
  z.object({
    password: z.string().min(8, 'Min 8 characters'),
    confirmPassword: z.string()
  }).refine(data => data.password === data.confirmPassword, {
    message: 'Passwords do not match',
    path: ['confirmPassword']
  })
);

const { handleSubmit } = useForm({ validationSchema: schema });
const { value: password } = useField('password');
const { value: confirmPassword, errorMessage: confirmError } = useField('confirmPassword');
</script>

<template>
  <form @submit="handleSubmit(onSubmit)">
    <input v-model="password" type="password" placeholder="Password" />
    <input v-model="confirmPassword" type="password" placeholder="Confirm password" />
    <span v-if="confirmError">{{ confirmError }}</span>
  </form>
</template>
```

### Field Arrays (Dynamic Fields)

```vue
<script setup lang="ts">
import { useForm, useFieldArray } from 'vee-validate';
import { toTypedSchema } from '@vee-validate/zod';
import { z } from 'zod';

const schema = toTypedSchema(z.object({
  teammates: z.array(z.object({
    name: z.string().min(1, 'Name required'),
    email: z.string().email('Invalid email')
  })).min(1, 'Add at least one teammate')
}));

const { handleSubmit } = useForm({
  validationSchema: schema,
  initialValues: {
    teammates: [{ name: '', email: '' }]
  }
});

const { fields, push, remove } = useFieldArray('teammates');
</script>

<template>
  <form @submit="handleSubmit(onSubmit)">
    <div v-for="(field, index) in fields" :key="field.key">
      <FormField :name="`teammates[${index}].name`" label="Name" />
      <FormField :name="`teammates[${index}].email`" label="Email" type="email" />
      <button type="button" @click="remove(index)" v-if="fields.length > 1">
        Remove
      </button>
    </div>
    
    <button type="button" @click="push({ name: '', email: '' })">
      Add teammate
    </button>
    
    <button type="submit">Submit</button>
  </form>
</template>
```

## Vuelidate Patterns

### Basic Form

```vue
<script setup lang="ts">
import { reactive, computed } from 'vue';
import { useVuelidate } from '@vuelidate/core';
import { required, email, minLength } from '@vuelidate/validators';

const state = reactive({
  email: '',
  password: ''
});

const rules = computed(() => ({
  email: { required, email },
  password: { required, minLength: minLength(8) }
}));

const v$ = useVuelidate(rules, state);

const onSubmit = async () => {
  const isValid = await v$.value.$validate();
  if (!isValid) return;
  
  console.log('Submitting:', state);
};
</script>

<template>
  <form @submit.prevent="onSubmit">
    <div class="form-field" :class="{ 'has-error': v$.email.$error }">
      <label for="email">Email</label>
      <input
        id="email"
        v-model="state.email"
        type="email"
        autocomplete="email"
        @blur="v$.email.$touch()"
      />
      <span v-if="v$.email.$error" class="error">
        {{ v$.email.$errors[0]?.$message }}
      </span>
    </div>

    <div class="form-field" :class="{ 'has-error': v$.password.$error }">
      <label for="password">Password</label>
      <input
        id="password"
        v-model="state.password"
        type="password"
        autocomplete="current-password"
        @blur="v$.password.$touch()"
      />
      <span v-if="v$.password.$error" class="error">
        {{ v$.password.$errors[0]?.$message }}
      </span>
    </div>

    <button type="submit" :disabled="v$.$pending">
      Sign in
    </button>
  </form>
</template>
```

### Vuelidate with Zod

```vue
<script setup lang="ts">
import { reactive } from 'vue';
import { useVuelidate } from '@vuelidate/core';
import { helpers } from '@vuelidate/validators';
import { z } from 'zod';

// Create Vuelidate validator from Zod schema
function zodValidator<T extends z.ZodType>(schema: T) {
  return helpers.withMessage(
    (value: unknown) => {
      const result = schema.safeParse(value);
      if (!result.success) {
        return result.error.errors[0]?.message || 'Invalid';
      }
      return true;
    },
    (value: unknown) => {
      const result = schema.safeParse(value);
      return result.success;
    }
  );
}

const emailSchema = z.string().email('Please enter a valid email');
const passwordSchema = z.string().min(8, 'Password must be at least 8 characters');

const state = reactive({
  email: '',
  password: ''
});

const rules = {
  email: { zodValidator: zodValidator(emailSchema) },
  password: { zodValidator: zodValidator(passwordSchema) }
};

const v$ = useVuelidate(rules, state);
</script>
```

## Shared Zod Schemas

```typescript
// schemas/index.ts (shared between React and Vue)
import { z } from 'zod';

export const loginSchema = z.object({
  email: z.string().min(1, 'Email is required').email('Invalid email'),
  password: z.string().min(1, 'Password is required'),
  rememberMe: z.boolean().optional().default(false)
});

export type LoginFormData = z.infer<typeof loginSchema>;

// VeeValidate usage
import { toTypedSchema } from '@vee-validate/zod';
const veeSchema = toTypedSchema(loginSchema);

// React Hook Form usage
import { zodResolver } from '@hookform/resolvers/zod';
const rhfResolver = zodResolver(loginSchema);
```

## File Structure

```
form-vue/
├── SKILL.md
├── references/
│   ├── veevalidate-patterns.md   # VeeValidate deep-dive
│   └── vuelidate-patterns.md     # Vuelidate deep-dive
└── scripts/
    ├── veevalidate-form.vue      # VeeValidate patterns
    ├── vuelidate-form.vue        # Vuelidate patterns
    ├── form-field.vue            # Reusable field component
    └── schemas/                  # Shared with form-validation
        ├── auth.ts
        ├── profile.ts
        └── payment.ts
```

## Reference

- `references/veevalidate-patterns.md` — Complete VeeValidate patterns
- `references/vuelidate-patterns.md` — Vuelidate patterns
