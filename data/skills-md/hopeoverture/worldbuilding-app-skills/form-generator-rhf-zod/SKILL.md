---
name: form-generator-rhf-zod
description: This skill should be used when generating React forms with React Hook Form, Zod validation, and shadcn/ui components. Applies when creating entity forms, character editors, location forms, data entry forms, or any form requiring client and server validation. Trigger terms include create form, generate form, build form, React Hook Form, RHF, Zod validation, form component, entity form, character form, data entry, form schema.
---

# Form Generator with React Hook Form & Zod

Generate production-ready React forms using React Hook Form, Zod validation schemas, and accessible shadcn/ui form controls. This skill creates forms with client-side and server-side validation, proper TypeScript types, and consistent error handling.

## When to Use This Skill

Apply this skill when:
- Creating forms for entities (characters, locations, items, factions)
- Building data entry interfaces with validation requirements
- Generating forms with complex field types and conditional logic
- Setting up forms that need both client and server validation
- Creating accessible forms with proper ARIA attributes
- Building forms with multi-step or wizard patterns

## Resources Available

### Scripts

**scripts/generate_form.py** - Generates form component, Zod schema, and server action from field specifications.

Usage:
```bash
python scripts/generate_form.py --name CharacterForm --fields fields.json --output components/forms
```

**scripts/generate_zod_schema.py** - Converts field specifications to Zod schema with validation rules.

Usage:
```bash
python scripts/generate_zod_schema.py --fields fields.json --output lib/schemas
```

### References

**references/rhf-patterns.md** - React Hook Form patterns, hooks, and best practices
**references/zod-validation.md** - Zod schema patterns, refinements, and custom validators
**references/shadcn-form-controls.md** - shadcn/ui form component usage and examples
**references/server-actions.md** - Server action patterns for form submission

### Assets

**assets/form-template.tsx** - Base form component template with RHF setup
**assets/field-templates/** - Individual field component templates (Input, Textarea, Select, Checkbox, etc.)
**assets/validation-schemas.ts** - Common Zod validation patterns
**assets/form-utils.ts** - Form utility functions (formatters, transformers, validators)

## Form Generation Process

### Step 1: Define Field Specifications

Create a field specification file describing form fields, types, validation rules, and UI properties.

Field specification format:
```json
{
  "fields": [
    {
      "name": "characterName",
      "label": "Character Name",
      "type": "text",
      "required": true,
      "validation": {
        "minLength": 2,
        "maxLength": 100,
        "pattern": "^[a-zA-Z\\s'-]+$"
      },
      "placeholder": "Enter character name",
      "helpText": "The character's full name as it appears in your world"
    },
    {
      "name": "age",
      "label": "Age",
      "type": "number",
      "required": false,
      "validation": {
        "min": 0,
        "max": 10000
      }
    },
    {
      "name": "faction",
      "label": "Faction",
      "type": "select",
      "required": true,
      "options": "dynamic",
      "optionsSource": "api.getFactions()"
    },
    {
      "name": "biography",
      "label": "Biography",
      "type": "textarea",
      "required": false,
      "validation": {
        "maxLength": 5000
      },
      "rows": 8
    }
  ],
  "formOptions": {
    "submitLabel": "Create Character",
    "resetLabel": "Clear Form",
    "showReset": true,
    "successMessage": "Character created successfully",
    "errorMessage": "Failed to create character"
  }
}
```

### Step 2: Generate Zod Schema

Use scripts/generate_zod_schema.py to create type-safe validation schema:

```bash
python scripts/generate_zod_schema.py --fields character-fields.json --output lib/schemas/character.ts
```

Generated schema includes:
- Field-level validation rules
- Custom refinements and transformations
- Type inference for TypeScript
- Error message customization
- Server-side validation support

### Step 3: Generate Form Component

Use scripts/generate_form.py to create React Hook Form component:

```bash
python scripts/generate_form.py --name CharacterForm --fields character-fields.json --output components/forms
```

Generated component includes:
- React Hook Form setup with useForm hook
- Zod schema resolver integration
- shadcn/ui FormField components
- Proper TypeScript types inferred from schema
- Accessible form controls with ARIA labels
- Error display with FormMessage components
- Form submission handler with loading states
- Success/error toast notifications

### Step 4: Create Server Action

Generate server action for form submission with server-side validation:

```typescript
'use server'

import { z } from 'zod'
import { characterSchema } from '@/lib/schemas/character'
import { createCharacter } from '@/lib/db/characters'

export async function createCharacterAction(data: z.infer<typeof characterSchema>) {
  // Server-side validation
  const validated = characterSchema.safeParse(data)

  if (!validated.success) {
    return {
      success: false,
      errors: validated.error.flatten().fieldErrors
    }
  }

  // Database operation
  const character = await createCharacter(validated.data)

  return {
    success: true,
    data: character
  }
}
```

### Step 5: Integrate Form into Page

Import and use generated form component in page or parent component:

```tsx
import { CharacterForm } from '@/components/forms/CharacterForm'

export default function CreateCharacterPage() {
  return (
    <div className="container max-w-2xl py-8">
      <h1 className="text-3xl font-bold mb-6">Create New Character</h1>
      <CharacterForm />
    </div>
  )
}
```

## Field Type Support

Supported field types and their shadcn/ui mappings:

- **text** → Input (type="text")
- **email** → Input (type="email")
- **password** → Input (type="password")
- **number** → Input (type="number")
- **tel** → Input (type="tel")
- **url** → Input (type="url")
- **textarea** → Textarea
- **select** → Select with SelectTrigger/SelectContent
- **multiselect** → MultiSelect custom component
- **checkbox** → Checkbox
- **radio** → RadioGroup with RadioGroupItem
- **switch** → Switch
- **date** → DatePicker (Popover + Calendar)
- **datetime** → DateTimePicker custom component
- **file** → Input (type="file")
- **combobox** → Combobox (Command + Popover)
- **tags** → TagInput custom component
- **slider** → Slider
- **color** → ColorPicker custom component

## Validation Patterns

Common validation patterns using Zod:

### String Validation
```typescript
// Required with length constraints
z.string().min(2, "Too short").max(100, "Too long")

// Email
z.string().email("Invalid email")

// URL
z.string().url("Invalid URL")

// Pattern matching
z.string().regex(/^[a-zA-Z]+$/, "Letters only")

// Trimmed strings
z.string().trim().min(1)

// Custom transformation
z.string().transform(val => val.toLowerCase())
```

### Number Validation
```typescript
// Range validation
z.number().min(0).max(100)

// Integer only
z.number().int("Must be whole number")

// Positive numbers
z.number().positive("Must be positive")

// Custom refinement
z.number().refine(val => val % 5 === 0, "Must be multiple of 5")
```

### Array Validation
```typescript
// Array with min/max items
z.array(z.string()).min(1, "Select at least one").max(5, "Too many")

// Non-empty array
z.array(z.string()).nonempty("Required")
```

### Object Validation
```typescript
// Nested objects
z.object({
  address: z.object({
    street: z.string(),
    city: z.string(),
    zipCode: z.string().regex(/^\d{5}$/)
  })
})
```

### Conditional Validation
```typescript
// Refine with cross-field validation
z.object({
  password: z.string().min(8),
  confirmPassword: z.string()
}).refine(data => data.password === data.confirmPassword, {
  message: "Passwords must match",
  path: ["confirmPassword"]
})
```

### Optional and Nullable Fields
```typescript
// Optional (can be undefined)
z.string().optional()

// Nullable (can be null)
z.string().nullable()

// Optional with default
z.string().default("default value")
```

## Form Patterns

### Basic Form Structure

```tsx
'use client'

import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Button } from '@/components/ui/button'
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { toast } from 'sonner'

const formSchema = z.object({
  name: z.string().min(2).max(100),
  email: z.string().email()
})

type FormValues = z.infer<typeof formSchema>

export function ExampleForm() {
  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: '',
      email: ''
    }
  })

  async function onSubmit(values: FormValues) {
    try {
      const result = await submitAction(values)
      if (result.success) {
        toast.success('Submitted successfully')
        form.reset()
      } else {
        toast.error(result.message)
      }
    } catch (error) {
      toast.error('An error occurred')
    }
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Name</FormLabel>
              <FormControl>
                <Input placeholder="Enter name" {...field} />
              </FormControl>
              <FormDescription>Your display name</FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input type="email" placeholder="you@example.com" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <Button type="submit" disabled={form.formState.isSubmitting}>
          {form.formState.isSubmitting ? 'Submitting...' : 'Submit'}
        </Button>
      </form>
    </Form>
  )
}
```

### Array Fields with useFieldArray

```tsx
import { useFieldArray } from 'react-hook-form'
import { Button } from '@/components/ui/button'

// In schema
const formSchema = z.object({
  tags: z.array(z.object({
    value: z.string().min(1)
  })).min(1)
})

// In component
const { fields, append, remove } = useFieldArray({
  control: form.control,
  name: 'tags'
})

// In JSX
{fields.map((field, index) => (
  <div key={field.id} className="flex gap-2">
    <FormField
      control={form.control}
      name={`tags.${index}.value`}
      render={({ field }) => (
        <FormItem className="flex-1">
          <FormControl>
            <Input {...field} />
          </FormControl>
          <FormMessage />
        </FormItem>
      )}
    />
    <Button type="button" variant="destructive" size="icon" onClick={() => remove(index)}>
      X
    </Button>
  </div>
))}
<Button type="button" onClick={() => append({ value: '' })}>
  Add Tag
</Button>
```

### File Upload with Preview

```tsx
const [preview, setPreview] = useState<string | null>(null)

<FormField
  control={form.control}
  name="avatar"
  render={({ field: { value, onChange, ...field } }) => (
    <FormItem>
      <FormLabel>Avatar</FormLabel>
      <FormControl>
        <Input
          type="file"
          accept="image/*"
          {...field}
          onChange={(e) => {
            const file = e.target.files?.[0]
            if (file) {
              onChange(file)
              const reader = new FileReader()
              reader.onloadend = () => setPreview(reader.result as string)
              reader.readAsDataURL(file)
            }
          }}
        />
      </FormControl>
      {preview && (
        <img src={preview} alt="Preview" className="mt-2 h-32 w-32 object-cover rounded" />
      )}
      <FormMessage />
    </FormItem>
  )}
/>
```

### Conditional Fields

```tsx
const showAdvanced = form.watch('showAdvanced')

<FormField
  control={form.control}
  name="showAdvanced"
  render={({ field }) => (
    <FormItem className="flex items-center gap-2">
      <FormControl>
        <Switch checked={field.value} onCheckedChange={field.onChange} />
      </FormControl>
      <FormLabel>Show Advanced Options</FormLabel>
    </FormItem>
  )}
/>

{showAdvanced && (
  <FormField
    control={form.control}
    name="advancedOption"
    render={({ field }) => (
      <FormItem>
        <FormLabel>Advanced Option</FormLabel>
        <FormControl>
          <Input {...field} />
        </FormControl>
        <FormMessage />
      </FormItem>
    )}
  />
)}
```

## Accessibility Considerations

Ensure forms are accessible by:

1. **Proper Labels**: Every form control must have an associated FormLabel
2. **Error Messages**: Use FormMessage to announce validation errors
3. **Descriptions**: Use FormDescription for helpful context
4. **Required Fields**: Mark required fields visually and in ARIA attributes
5. **Focus Management**: Ensure logical tab order and focus indicators
6. **Keyboard Navigation**: All controls operable via keyboard
7. **ARIA Attributes**: FormField automatically sets aria-describedby and aria-invalid
8. **Error Summary**: Consider adding error summary at top of form for screen readers

## Testing Generated Forms

Test forms using React Testing Library and Vitest:

```tsx
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { CharacterForm } from './CharacterForm'

describe('CharacterForm', () => {
  it('validates required fields', async () => {
    render(<CharacterForm />)

    const submitButton = screen.getByRole('button', { name: /submit/i })
    await userEvent.click(submitButton)

    expect(await screen.findByText(/name is required/i)).toBeInTheDocument()
  })

  it('submits valid data', async () => {
    const mockSubmit = vi.fn()
    render(<CharacterForm onSubmit={mockSubmit} />)

    await userEvent.type(screen.getByLabelText(/name/i), 'Aragorn')
    await userEvent.click(screen.getByRole('button', { name: /submit/i }))

    await waitFor(() => {
      expect(mockSubmit).toHaveBeenCalledWith({
        name: 'Aragorn'
      })
    })
  })
})
```

## Common Use Cases for Worldbuilding

### Character Creation Form
Fields: name, race, faction, class, age, appearance, biography, relationships, attributes, inventory

### Location Form
Fields: name, type, region, coordinates, climate, population, government, description, points of interest

### Item/Artifact Form
Fields: name, type, rarity, owner, location, properties, history, magical effects, value

### Event/Timeline Form
Fields: title, date, location, participants, description, consequences, related events

### Faction/Organization Form
Fields: name, type, leader, headquarters, goals, allies, enemies, members, history

## Implementation Checklist

When generating forms, ensure:

- [ ] Zod schema created with all validation rules
- [ ] Form component uses zodResolver
- [ ] All field types mapped to appropriate shadcn/ui components
- [ ] FormField used for each field with proper render prop
- [ ] FormLabel, FormControl, FormMessage included for each field
- [ ] Form submission handler with error handling
- [ ] Loading states during submission
- [ ] Success/error feedback (toasts or messages)
- [ ] Server action created with server-side validation
- [ ] TypeScript types inferred from Zod schema
- [ ] Accessibility attributes present
- [ ] Form reset after successful submission
- [ ] Proper default values set

## Dependencies Required

Ensure these packages are installed:

```bash
npm install react-hook-form @hookform/resolvers zod
npm install sonner  # for toast notifications
```

shadcn/ui components needed:
```bash
npx shadcn-ui@latest add form button input textarea select checkbox radio-group switch slider
```

## Best Practices

1. **Co-locate validation**: Keep Zod schemas close to form components
2. **Reuse schemas**: Share schemas between client and server validation
3. **Type inference**: Use `z.infer<typeof schema>` for TypeScript types
4. **Granular validation**: Validate on blur for better UX
5. **Optimistic updates**: Show success state before server confirmation when appropriate
6. **Error recovery**: Allow users to easily fix validation errors
7. **Progress indication**: Show loading states during async operations
8. **Data persistence**: Consider auto-saving drafts for long forms
9. **Field dependencies**: Use form.watch() for conditional fields
10. **Performance**: Use mode: 'onBlur' or 'onChange' based on form complexity

## Troubleshooting

**Issue**: Form not submitting
- Check handleSubmit is wrapping onSubmit
- Verify zodResolver is configured
- Check for validation errors in form state

**Issue**: Validation not working
- Ensure schema matches field names exactly
- Check resolver is zodResolver(schema)
- Verify field is registered with FormField

**Issue**: TypeScript errors
- Use z.infer<typeof schema> for type inference
- Ensure form values type matches schema type
- Check FormField generic type matches field value type

**Issue**: Field not updating
- Verify field spread {...field} is applied
- Check value/onChange are not overridden incorrectly
- Use field.value and field.onChange for controlled components

## Additional Resources

Consult references/ directory for detailed patterns:
- references/rhf-patterns.md - Advanced React Hook Form patterns
- references/zod-validation.md - Complex validation scenarios
- references/shadcn-form-controls.md - All form component variants
- references/server-actions.md - Server-side form handling

Use assets/ directory for starting templates:
- assets/form-template.tsx - Copy and customize
- assets/field-templates/ - Individual field implementations
- assets/validation-schemas.ts - Common validation patterns
