---
name: form-ux-patterns
description: UX patterns for complex forms including multi-step wizards, cognitive chunking (5-7 fields max), progressive disclosure, and conditional fields. Use when building checkout flows, onboarding wizards, or forms with many fields.
---

# Form UX Patterns

Patterns for complex forms based on cognitive load research and aviation UX principles.

## Quick Start

```tsx
// Multi-step form with chunking
import { useMultiStepForm } from './multi-step-form';

function CheckoutWizard() {
  const { currentStep, steps, goNext, goBack, isLastStep } = useMultiStepForm({
    steps: [
      { id: 'contact', title: 'Contact', fields: ['email', 'phone'] },
      { id: 'shipping', title: 'Shipping', fields: ['name', 'street', 'city', 'state', 'zip'] },
      { id: 'payment', title: 'Payment', fields: ['cardName', 'cardNumber', 'expiry', 'cvv'] }
    ]
  });

  return (
    <form>
      <StepIndicator steps={steps} current={currentStep} />
      <StepContent step={steps[currentStep]} />
      <StepNavigation onBack={goBack} onNext={goNext} isLast={isLastStep} />
    </form>
  );
}
```

## Core Principles

### 1. Cognitive Chunking (Aviation Principle)

> "Humans can hold 5-7 items in working memory" — Miller's Law

```tsx
// ❌ BAD: All fields on one page
<form>
  <input name="email" />
  <input name="phone" />
  <input name="name" />
  <input name="street" />
  <input name="street2" />
  <input name="city" />
  <input name="state" />
  <input name="zip" />
  <input name="cardName" />
  <input name="cardNumber" />
  <input name="expiry" />
  <input name="cvv" />
  {/* 12 fields = cognitive overload */}
</form>

// ✅ GOOD: Chunked into logical groups (5-7 max per group)
<form>
  <fieldset>
    <legend>Contact (2 fields)</legend>
    <input name="email" />
    <input name="phone" />
  </fieldset>
  
  <fieldset>
    <legend>Shipping (5 fields)</legend>
    <input name="name" />
    <input name="street" />
    <input name="city" />
    <input name="state" />
    <input name="zip" />
  </fieldset>
  
  <fieldset>
    <legend>Payment (4 fields)</legend>
    <input name="cardName" />
    <input name="cardNumber" />
    <input name="expiry" />
    <input name="cvv" />
  </fieldset>
</form>
```

### 2. Briefing vs. Checklist (Aviation Principle)

> Instructions should be separate from labels, given before the task.

```tsx
// ❌ BAD: Instructions mixed with labels
<label>
  Password (must be 8+ characters with uppercase, lowercase, and number)
</label>
<input type="password" />

// ✅ GOOD: Briefing before, label during
<div className="field-briefing">
  <p>Create a strong password with:</p>
  <ul>
    <li>At least 8 characters</li>
    <li>Uppercase and lowercase letters</li>
    <li>At least one number</li>
  </ul>
</div>

<label>Password</label>
<input type="password" />
```

### 3. Progressive Disclosure

> Show only what's needed, when it's needed.

```tsx
// Reveal fields based on selection
function ShippingForm() {
  const [method, setMethod] = useState<'standard' | 'express' | 'pickup'>('standard');

  return (
    <form>
      <RadioGroup
        label="Delivery method"
        value={method}
        onChange={setMethod}
        options={[
          { value: 'standard', label: 'Standard (5-7 days)' },
          { value: 'express', label: 'Express (2-3 days)' },
          { value: 'pickup', label: 'Store pickup' }
        ]}
      />

      {/* Only show address for shipping methods */}
      {method !== 'pickup' && (
        <AddressFields />
      )}

      {/* Only show store selector for pickup */}
      {method === 'pickup' && (
        <StoreSelector />
      )}
    </form>
  );
}
```

## Multi-Step Forms

### Step Configuration

```typescript
// types/multi-step.ts
export interface FormStep {
  /** Unique step identifier */
  id: string;
  
  /** Display title */
  title: string;
  
  /** Optional description (briefing) */
  description?: string;
  
  /** Fields in this step (for validation) */
  fields: string[];
  
  /** Zod schema for this step */
  schema?: z.ZodType;
  
  /** Whether step can be skipped */
  optional?: boolean;
  
  /** Condition for showing this step */
  condition?: (formData: Record<string, any>) => boolean;
}

export interface FormChunk {
  /** Chunk identifier */
  id: string;
  
  /** Chunk title */
  title: string;
  
  /** Briefing text (shown before fields) */
  briefing?: string;
  
  /** Fields in this chunk (max 5-7) */
  fields: string[];
}
```

### Multi-Step Hook

```typescript
// hooks/use-multi-step-form.ts
import { useState, useCallback, useMemo } from 'react';
import { UseFormReturn } from 'react-hook-form';

export interface UseMultiStepFormOptions {
  steps: FormStep[];
  form: UseFormReturn<any>;
  onComplete?: (data: any) => void;
}

export interface UseMultiStepFormReturn {
  /** Current step index */
  currentStep: number;
  
  /** Current step config */
  step: FormStep;
  
  /** All steps (filtered by conditions) */
  steps: FormStep[];
  
  /** Total step count */
  totalSteps: number;
  
  /** Whether on first step */
  isFirstStep: boolean;
  
  /** Whether on last step */
  isLastStep: boolean;
  
  /** Progress percentage (0-100) */
  progress: number;
  
  /** Go to next step (validates current) */
  goNext: () => Promise<boolean>;
  
  /** Go to previous step */
  goBack: () => void;
  
  /** Go to specific step */
  goTo: (index: number) => void;
  
  /** Can navigate to step (all previous valid) */
  canGoTo: (index: number) => boolean;
}

export function useMultiStepForm({
  steps: allSteps,
  form,
  onComplete
}: UseMultiStepFormOptions): UseMultiStepFormReturn {
  const [currentStep, setCurrentStep] = useState(0);
  
  // Filter steps by conditions
  const steps = useMemo(() => {
    const data = form.getValues();
    return allSteps.filter(step => 
      !step.condition || step.condition(data)
    );
  }, [allSteps, form]);
  
  const step = steps[currentStep];
  const totalSteps = steps.length;
  const isFirstStep = currentStep === 0;
  const isLastStep = currentStep === totalSteps - 1;
  const progress = ((currentStep + 1) / totalSteps) * 100;
  
  const goNext = useCallback(async () => {
    // Validate current step fields
    const isValid = await form.trigger(step.fields as any);
    
    if (!isValid) {
      // Focus first error
      const firstError = document.querySelector('[aria-invalid="true"]');
      (firstError as HTMLElement)?.focus();
      return false;
    }
    
    if (isLastStep) {
      // Submit form
      const data = form.getValues();
      onComplete?.(data);
    } else {
      setCurrentStep(prev => prev + 1);
      // Focus step heading
      requestAnimationFrame(() => {
        document.getElementById('step-heading')?.focus();
      });
    }
    
    return true;
  }, [step, isLastStep, form, onComplete]);
  
  const goBack = useCallback(() => {
    if (!isFirstStep) {
      setCurrentStep(prev => prev - 1);
      requestAnimationFrame(() => {
        document.getElementById('step-heading')?.focus();
      });
    }
  }, [isFirstStep]);
  
  const goTo = useCallback((index: number) => {
    if (index >= 0 && index < totalSteps) {
      setCurrentStep(index);
    }
  }, [totalSteps]);
  
  const canGoTo = useCallback((index: number) => {
    // Can always go back
    if (index < currentStep) return true;
    
    // Can only go forward if all previous steps are valid
    // (would need form state tracking for this)
    return index <= currentStep;
  }, [currentStep]);
  
  return {
    currentStep,
    step,
    steps,
    totalSteps,
    isFirstStep,
    isLastStep,
    progress,
    goNext,
    goBack,
    goTo,
    canGoTo
  };
}
```

### Step Indicator Component

```tsx
// components/StepIndicator.tsx
interface StepIndicatorProps {
  steps: FormStep[];
  currentStep: number;
  onStepClick?: (index: number) => void;
  canNavigate?: (index: number) => boolean;
}

export function StepIndicator({
  steps,
  currentStep,
  onStepClick,
  canNavigate
}: StepIndicatorProps) {
  return (
    <nav aria-label="Form progress">
      <ol className="step-indicator">
        {steps.map((step, index) => {
          const status = index < currentStep 
            ? 'complete' 
            : index === currentStep 
              ? 'current' 
              : 'upcoming';
          
          const clickable = canNavigate?.(index) ?? false;
          
          return (
            <li 
              key={step.id}
              className={`step-indicator__item step-indicator__item--${status}`}
            >
              {clickable ? (
                <button
                  type="button"
                  onClick={() => onStepClick?.(index)}
                  aria-current={status === 'current' ? 'step' : undefined}
                >
                  <span className="step-indicator__number">{index + 1}</span>
                  <span className="step-indicator__title">{step.title}</span>
                </button>
              ) : (
                <span aria-current={status === 'current' ? 'step' : undefined}>
                  <span className="step-indicator__number">{index + 1}</span>
                  <span className="step-indicator__title">{step.title}</span>
                </span>
              )}
            </li>
          );
        })}
      </ol>
      
      {/* Progress bar */}
      <div 
        className="step-indicator__progress"
        role="progressbar"
        aria-valuenow={currentStep + 1}
        aria-valuemin={1}
        aria-valuemax={steps.length}
        aria-label={`Step ${currentStep + 1} of ${steps.length}`}
      >
        <div 
          className="step-indicator__progress-fill"
          style={{ width: `${((currentStep + 1) / steps.length) * 100}%` }}
        />
      </div>
    </nav>
  );
}
```

### Step Navigation Component

```tsx
// components/StepNavigation.tsx
interface StepNavigationProps {
  onBack: () => void;
  onNext: () => void;
  isFirstStep: boolean;
  isLastStep: boolean;
  isSubmitting?: boolean;
  backLabel?: string;
  nextLabel?: string;
  submitLabel?: string;
}

export function StepNavigation({
  onBack,
  onNext,
  isFirstStep,
  isLastStep,
  isSubmitting = false,
  backLabel = 'Back',
  nextLabel = 'Continue',
  submitLabel = 'Submit'
}: StepNavigationProps) {
  return (
    <div className="step-navigation">
      {!isFirstStep && (
        <button
          type="button"
          onClick={onBack}
          className="step-navigation__back"
          disabled={isSubmitting}
        >
          {backLabel}
        </button>
      )}
      
      <button
        type="button"
        onClick={onNext}
        className="step-navigation__next"
        disabled={isSubmitting}
      >
        {isSubmitting ? (
          <>
            <Spinner aria-hidden="true" />
            <span className="sr-only">Processing...</span>
            Processing...
          </>
        ) : (
          isLastStep ? submitLabel : nextLabel
        )}
      </button>
    </div>
  );
}
```

## Conditional Fields

### Pattern: Show/Hide Based on Selection

```tsx
// components/ConditionalField.tsx
import { useFormContext, useWatch } from 'react-hook-form';
import { ReactNode } from 'react';

interface ConditionalFieldProps {
  /** Field to watch */
  watch: string;
  
  /** Condition for showing children */
  when: (value: any) => boolean;
  
  /** Children to render when condition is true */
  children: ReactNode;
  
  /** Whether to keep values when hidden */
  keepValues?: boolean;
}

export function ConditionalField({
  watch: watchField,
  when,
  children,
  keepValues = false
}: ConditionalFieldProps) {
  const { control, unregister } = useFormContext();
  const value = useWatch({ control, name: watchField });
  
  const shouldShow = when(value);
  
  // Optionally unregister fields when hidden
  useEffect(() => {
    if (!shouldShow && !keepValues) {
      // Get field names from children and unregister
      // (implementation depends on your field structure)
    }
  }, [shouldShow, keepValues]);
  
  if (!shouldShow) return null;
  
  return <>{children}</>;
}

// Usage
<FormField name="hasCompany" label="Are you a business?" type="checkbox" />

<ConditionalField watch="hasCompany" when={(v) => v === true}>
  <FormField name="companyName" label="Company name" />
  <FormField name="taxId" label="Tax ID" />
</ConditionalField>
```

### Pattern: Dynamic Field Array

```tsx
// components/RepeatableField.tsx
import { useFieldArray, useFormContext } from 'react-hook-form';

interface RepeatableFieldProps {
  name: string;
  label: string;
  maxItems?: number;
  minItems?: number;
  renderItem: (index: number) => ReactNode;
}

export function RepeatableField({
  name,
  label,
  maxItems = 10,
  minItems = 1,
  renderItem
}: RepeatableFieldProps) {
  const { control } = useFormContext();
  const { fields, append, remove } = useFieldArray({ control, name });
  
  const canAdd = fields.length < maxItems;
  const canRemove = fields.length > minItems;
  
  return (
    <fieldset className="repeatable-field">
      <legend>{label}</legend>
      
      {fields.map((field, index) => (
        <div key={field.id} className="repeatable-field__item">
          {renderItem(index)}
          
          {canRemove && (
            <button
              type="button"
              onClick={() => remove(index)}
              aria-label={`Remove item ${index + 1}`}
            >
              Remove
            </button>
          )}
        </div>
      ))}
      
      {canAdd && (
        <button
          type="button"
          onClick={() => append({})}
          className="repeatable-field__add"
        >
          Add {label.toLowerCase()}
        </button>
      )}
    </fieldset>
  );
}

// Usage
<RepeatableField
  name="teammates"
  label="Team Members"
  maxItems={5}
  renderItem={(index) => (
    <>
      <FormField name={`teammates.${index}.name`} label="Name" />
      <FormField name={`teammates.${index}.email`} label="Email" />
    </>
  )}
/>
```

## Form Layout Patterns

### Single Column (Recommended Default)

```tsx
// Best for most forms - clear visual flow
<form className="form-layout--single">
  <FormField name="email" label="Email" />
  <FormField name="password" label="Password" />
  <button type="submit">Sign in</button>
</form>

// CSS
.form-layout--single {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-width: 400px;
}
```

### Two Column (Use Sparingly)

```tsx
// Only for related short fields
<form className="form-layout--two-col">
  <FormField name="firstName" label="First name" />
  <FormField name="lastName" label="Last name" />
  
  <FormField name="city" label="City" className="col-span-1" />
  <FormField name="state" label="State" className="col-span-1" />
</form>

// CSS
.form-layout--two-col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

@media (max-width: 640px) {
  .form-layout--two-col {
    grid-template-columns: 1fr;
  }
}
```

### Card Sections

```tsx
// For long forms with distinct sections
<form className="form-layout--cards">
  <section className="form-card">
    <h3>Contact Information</h3>
    <FormField name="email" label="Email" />
    <FormField name="phone" label="Phone" />
  </section>
  
  <section className="form-card">
    <h3>Shipping Address</h3>
    <AddressFields />
  </section>
  
  <section className="form-card">
    <h3>Payment</h3>
    <PaymentFields />
  </section>
</form>
```

## File Structure

```
form-ux-patterns/
├── SKILL.md
├── references/
│   ├── cognitive-load.md       # Research on chunking
│   └── wizard-patterns.md      # Multi-step best practices
└── scripts/
    ├── multi-step-form.tsx     # Multi-step hook + components
    ├── conditional-field.tsx   # Show/hide patterns
    ├── repeatable-field.tsx    # Dynamic arrays
    ├── step-indicator.tsx      # Progress indicator
    └── step-indicator.css      # Styles
```

## Reference

- `references/cognitive-load.md` — Research on Miller's Law and chunking
- `references/wizard-patterns.md` — Multi-step wizard best practices
