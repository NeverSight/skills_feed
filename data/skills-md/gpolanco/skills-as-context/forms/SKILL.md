---
name: forms
description: >
  React Hook Form + Zod patterns for type-safe, accessible forms with server validation.
  Trigger: Use when creating forms with React Hook Form, Zod schemas, or Next.js Server Actions.
license: Apache-2.0
metadata:
  author: gpolanco
  version: "1.0.0"
  scope: [root]
  auto_invoke: "Creating forms"
allowed-tools: Read
---

# Forms (React Hook Form + Zod)

## 🚨 CRITICAL: Reference Files are MANDATORY

**This SKILL.md provides OVERVIEW only. For EXACT patterns:**

| Task | MANDATORY Reading |
|------|-------------------|
| **Form Components & Patterns** | ⚠️ [reference/validation.md](reference/validation.md) |

**⚠️ DO NOT implement custom form wrappers without reading the reference files FIRST.**

---

## When to Use

- Creating forms with React Hook Form
- Validating user input with Zod
- Submitting to Next.js Server Actions
- Building reusable form components

**Cross-references:**

- For Zod patterns → See `zod-4` skill
- For React patterns → See `react-19` skill
- For Server Actions → See `nextjs` skill (reference/architecture.md)

---

## Core Principle

> **Zod is the single source of truth.**
> If a rule isn't in Zod, it doesn't exist.

---

## ALWAYS

- **Define validation in Zod schemas** (never in JSX)
- **Revalidate on server** with `safeParse()` before persisting
- **Use `mode: "onTouched"`** for better UX
- **Provide `defaultValues`** for all fields
- **Use `FormWrapper`** (never inline `FormProvider + form`)
- **Use `FormField`** (never inline `Label + Input + Error`)
- **Apply `aria-invalid` and `aria-describedby`** for accessibility
- **Use `applyActionErrors` util** for server field errors
- **Return typed ApiResponse** from Server Actions

## NEVER

- Never validate in JSX (`required`, `validate` props)
- Never persist without server validation
- Never use `action={}` if you need rich UX feedback
- Never use `Controller` by default (only for non-native inputs)
- Never duplicate `Label + Input + Error` markup
- Never throw business logic errors from Server Actions
- Never show field errors only in toasts

## DEFAULTS

- Validation mode: `onTouched`
- Submit: React Hook Form → Server Action
- Feedback: Loading state + field errors + global error/success
- Components: `FormWrapper` + `FormField`

---

## 🚫 Critical Anti-Patterns

- **DO NOT** validate in JSX (`required`, `validate` props) → Zod is the single source of truth.
- **DO NOT** use native `action={}` if you need field errors or rich UX feedback → use `onSubmit` handler.
- **DO NOT** duplicate `FormWrapper` or `FormField` logic → use the provided shared components.
- **DO NOT** show field errors ONLY in toasts → they MUST be shown inline with the input.

---

## Schema Definition

```typescript
// features/users/schemas.ts
import { z } from "zod";

export const createUserSchema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters"),
  email: z.string().email("Invalid email address"),
  age: z.coerce.number().int().min(18, "Must be 18 or older"),
  role: z.enum(["user", "admin"]),
});

export type CreateUserInput = z.infer<typeof createUserSchema>;
```

---

## Server Action Contract

```typescript
// features/shared/types/api.ts
export type ApiResponse<T, TField extends string = string> =
  | { ok: true; data: T; message?: string }
  | { ok: false; error: string; fieldErrors?: Partial<Record<TField, string>> };
```

```typescript
// features/users/actions.ts
"use server";

import { createUserSchema } from "./schemas";
import type { ApiResponse } from "@/features/shared/types/api";

export async function createUser(
  data: unknown,
): Promise<ApiResponse<User, keyof CreateUserInput>> {
  // 1. Validate
  const result = createUserSchema.safeParse(data);
  if (!result.success) {
    return {
      ok: false,
      error: "Validation failed",
      fieldErrors: result.error.flatten().fieldErrors as any,
    };
  }

  // 2. Business logic
  try {
    const user = await db.users.create(result.data);
    return { ok: true, data: user, message: "User created successfully" };
  } catch (error) {
    return { ok: false, error: "Failed to create user" };
  }
}
```

---

## Form Setup

```typescript
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { createUserSchema, type CreateUserInput } from "./schemas";

const methods = useForm<CreateUserInput>({
  resolver: zodResolver(createUserSchema),
  mode: "onTouched",
  defaultValues: {
    name: "",
    email: "",
    age: 18,
    role: "user",
  },
});
```

---

## Form Component

```typescript
import { FormWrapper } from "@/features/shared/components/form/form-wrapper";
import { FormField } from "@/features/shared/components/form/form-field";
import { applyActionErrors } from "@/features/shared/components/form/utils";

export const CreateUserForm: React.FC = () => {
  const methods = useForm<CreateUserInput>({ /* ... */ });

  const onSubmit = async (data: CreateUserInput) => {
    const result = await createUser(data);

    if (!result.ok) {
      if (result.fieldErrors) {
        applyActionErrors({
          setError: methods.setError,
          fieldErrors: result.fieldErrors,
        });
      }
      methods.setError("root", { message: result.error });
      return;
    }

    // Success
    router.push("/users");
  };

  return (
    <FormWrapper methods={methods} onSubmit={onSubmit}>
      <FormField name="name" label="Full Name" type="text" />
      <FormField name="email" label="Email" type="email" />
      <FormField name="age" label="Age" type="number" />
      <FormField name="role" label="Role" type="select" options={roleOptions} />
    </FormWrapper>
  );
};
```

---

## FormWrapper (Required Component)

```typescript
// features/shared/components/form/form-wrapper/FormWrapper.tsx
import { FormProvider, type UseFormReturn } from "react-hook-form";

interface FormWrapperProps<T extends Record<string, any>> {
  methods: UseFormReturn<T>;
  onSubmit: (data: T) => void | Promise<void>;
  children: React.ReactNode;
  className?: string;
}

export const FormWrapper = <T extends Record<string, any>>({
  methods,
  onSubmit,
  children,
  className,
}: FormWrapperProps<T>) => {
  const globalError = methods.formState.errors.root?.message;

  return (
    <FormProvider {...methods}>
      <form onSubmit={methods.handleSubmit(onSubmit)} className={className}>
        {globalError && (
          <div className="rounded-md bg-destructive/10 p-3 text-destructive">
            {globalError}
          </div>
        )}
        {children}
      </form>
    </FormProvider>
  );
};
```

---

## FormField (Required Component)

```typescript
// features/shared/components/form/form-field/FormField.tsx
import { useFormContext } from "react-hook-form";
import { TextField } from "./fields/TextField";
import { SelectField } from "./fields/SelectField";

interface FormFieldProps {
  name: string;
  label: string;
  type?: "text" | "email" | "number" | "password" | "select" | "textarea";
  description?: string;
  [key: string]: any;
}

export const FormField: React.FC<FormFieldProps> = ({ name, type = "text", ...props }) => {
  if (type === "select") return <SelectField name={name} {...props} />;
  if (type === "textarea") return <TextareaField name={name} {...props} />;

  return <TextField name={name} type={type} {...props} />;
};
```

---

## FieldWrapper (Required Component)

```typescript
// features/shared/components/form/form-field/FieldWrapper.tsx
import { useFormContext } from "react-hook-form";
import { Label } from "@/features/shared/ui/label";

interface FieldWrapperProps {
  name: string;
  label: string;
  description?: string;
  required?: boolean;
  children: React.ReactNode;
}

export const FieldWrapper: React.FC<FieldWrapperProps> = ({
  name,
  label,
  description,
  required,
  children,
}) => {
  const { formState } = useFormContext();
  const error = formState.errors[name]?.message as string | undefined;

  const fieldId = `field-${name}`;
  const errorId = `error-${name}`;
  const descId = description ? `desc-${name}` : undefined;

  return (
    <div>
      <Label htmlFor={fieldId} required={required}>
        {label}
      </Label>
      {description && <p id={descId} className="text-sm text-muted-foreground">{description}</p>}
      {children}
      {error && (
        <p id={errorId} className="text-sm text-destructive" role="alert">
          {error}
        </p>
      )}
    </div>
  );
};
```

---

## TextField Example

```typescript
// features/shared/components/form/form-field/fields/TextField.tsx
import { useFormContext } from "react-hook-form";
import { Input } from "@/features/shared/ui/input";
import { FieldWrapper } from "../FieldWrapper";
import type { ComponentPropsWithoutRef } from "react";

interface TextFieldProps extends Omit<ComponentPropsWithoutRef<"input">, "name"> {
  name: string;
  label: string;
  description?: string;
}

export const TextField: React.FC<TextFieldProps> = ({
  name,
  label,
  description,
  type = "text",
  ...rest
}) => {
  const { register, formState } = useFormContext();
  const error = formState.errors[name];
  const fieldId = `field-${name}`;
  const errorId = error ? `error-${name}` : undefined;
  const descId = description ? `desc-${name}` : undefined;

  return (
    <FieldWrapper name={name} label={label} description={description}>
      <Input
        id={fieldId}
        type={type}
        aria-invalid={!!error}
        aria-describedby={[descId, errorId].filter(Boolean).join(" ") || undefined}
        disabled={formState.isSubmitting}
        {...register(name)}
        {...rest}
      />
    </FieldWrapper>
  );
};
```

---

## Utility: applyActionErrors

```typescript
// features/shared/components/form/utils/applyActionErrors.ts
import type { Path, UseFormSetError } from "react-hook-form";

interface ApplyActionErrorsParams<T extends Record<string, any>> {
  setError: UseFormSetError<T>;
  fieldErrors: Partial<Record<keyof T, string>>;
}

export function applyActionErrors<T extends Record<string, any>>({
  setError,
  fieldErrors,
}: ApplyActionErrorsParams<T>) {
  Object.entries(fieldErrors).forEach(([field, message]) => {
    setError(field as Path<T>, {
      type: "manual",
      message: message as string,
    });
  });
}
```

---

## Async Data with Reset

```typescript
// Load existing data
useEffect(() => {
  if (user) {
    methods.reset({
      name: user.name,
      email: user.email,
      age: user.age,
      role: user.role,
    });
  }
}, [user, methods]);
```

---

## Performance

```typescript
// ✅ Watch specific fields
const age = useWatch({ control: methods.control, name: "age" });

// ❌ Don't watch everything
const values = methods.watch(); // Triggers re-render on every field change
```

---

## Conditional Fields

```typescript
const methods = useForm({
  shouldUnregister: true, // Unregister fields when hidden
});

{showAdvanced && <FormField name="advancedOption" label="Advanced" />}
```

---

## Resources

- **React Hook Form**: [Official Docs](https://react-hook-form.com)
- **Zod Integration**: [zodResolver](https://react-hook-form.com/get-started#SchemaValidation)
- **Accessibility**: [WAI-ARIA Form Patterns](https://www.w3.org/WAI/ARIA/apg/patterns/form/)
