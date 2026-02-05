---
name: nuxt-ui-tdd
description: Guide for building Vue 3 components with NuxtUI using strict Test-Driven Development (TDD) methodology enforced by a TDD guard hook. Use this skill when implementing new UI components (atoms, molecules, organisms) for the Poche project, creating Storybook stories with interaction tests, or working within the RED-GREEN-REFACTOR cycle. Particularly useful when the user mentions "TDD", "test-first", "create a component", "build a component", "implement [ComponentName]", or when adding UI functionality.
---

# NuxtUI TDD Component Development

## Overview

Build Vue 3 components with NuxtUI following strict Test-Driven Development (TDD) methodology. This skill provides workflows, templates, and guardrails for creating well-tested, reusable UI components using the Atomic Design pattern.

## When to Use This Skill

Use this skill when:
- Building new Vue components (atoms, molecules, organisms)
- Creating components that wrap NuxtUI base components (UButton, UInput, UFormField, etc.)
- Working with Storybook interaction tests
- Following TDD methodology with the TDD guard hook
- User requests involve "implement [ComponentName]", "create a component", "build with TDD"

## Core Workflow

### 1. Determine Component Level

Before starting, identify the atomic design level. Consult `references/naming-conventions.md` for detailed guidance.

**Quick Reference**:
- **Atoms**: Single UI elements (Button, Input, Label, Icon)
- **Molecules**: 2-3 atoms combined (FormField, SearchBar, ArticleCard)
- **Organisms**: Complex sections (ArticleList, Navigation, ReaderView)
- **Templates**: Page layouts (DefaultLayout, AuthLayout)

**Naming Patterns**:
- Atoms: `{Element}.vue` (e.g., Button.vue)
- Molecules: `{Concept}{Type}.vue` (e.g., FormField.vue, SearchBar.vue)
- Organisms: `{Feature}{Component}.vue` (e.g., ArticleList.vue)

### 2. Create the Test File First

**Location**: Same directory as component
**Naming**: `{ComponentName}.stories.ts`

Use the template from `assets/story-template.ts` as a starting point.

**Critical TDD Rules**:
- Create ONLY ONE test/story initially
- Use the "Default" story for basic rendering
- Include ONE focused assertion per story
- Run test to confirm it fails (RED phase)

**Example First Test**:
```typescript
import type { Meta, StoryObj } from '@storybook/vue3';
import { expect, within } from '@storybook/test';
import SearchBar from './SearchBar.vue';

const meta = {
  title: 'Molecules/SearchBar',
  component: SearchBar,
  tags: ['autodocs'],
  argTypes: {
    placeholder: {
      control: 'text',
      description: 'Placeholder text',
    },
  },
} satisfies Meta<typeof SearchBar>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    placeholder: 'Search articles...',
  },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    const input = await canvas.findByPlaceholderText(/search articles/i);
    await expect(input).toBeInTheDocument();
  },
};
```

### 3. Capture RED Phase Evidence

Run Storybook test-runner to verify the test fails:

```bash
pnpm test:storybook:run -- {ComponentName}
```

Save the failure output:
```bash
pnpm test:storybook:run -- SearchBar | tee /tmp/searchbar-red-phase.txt
```

**Expected**: Test fails because component doesn't exist.

### 4. Update test.json for TDD Guard

Manually update `.claude/tdd-guard/data/test.json` to record the RED phase:

```json
{
  "verificationMode": false,
  "batchMode": false,
  "testModules": [
    {
      "moduleId": "/Users/tk/Code/poche/apps/web/components/molecules/SearchBar.stories.ts",
      "tests": [
        {
          "name": "Default",
          "fullName": "Molecules/SearchBar › Default",
          "state": "failed",
          "note": "RED phase - component doesn't exist"
        }
      ]
    }
  ],
  "redPhaseEvidence": {
    "completed": true,
    "command": "pnpm test:storybook -- SearchBar",
    "exitCode": 1,
    "timestamp": "2025-11-02T13:52:00.000Z",
    "testSuitesFailed": 1,
    "failureCount": 1,
    "totalTests": 1,
    "sampleErrors": [
      "FAIL browser: chromium components/molecules/SearchBar.stories.ts",
      "Failed to fetch dynamically imported module"
    ]
  },
  "unhandledErrors": [],
  "reason": "failed"
}
```

This step is CRITICAL - the TDD guard will block implementation without RED phase evidence.

### 5. Implement Minimal Component

**Location**: `apps/web/components/{level}/{ComponentName}.vue`

Use `assets/component-template.vue` as a starting point.

**Critical Implementation Rules**:
- Write ONLY the code needed to pass the current test
- Do NOT add untested props or functionality
- Wrap appropriate NuxtUI base components
- Keep it simple and minimal

**Example Minimal Implementation**:
```vue
<script setup lang="ts">
defineProps<{
  placeholder?: string;
}>();
</script>

<template>
  <UInput
    type="search"
    :placeholder="placeholder"
    leading-icon="i-lucide-search"
  />
</template>
```

### 6. Verify GREEN Phase

Run tests again to confirm they pass:

```bash
pnpm test:storybook:run -- {ComponentName}
```

**Expected**: Tests pass (GREEN phase).

### 7. Update test.json for GREEN Phase

Update test state to "passed":

```json
{
  "tests": [
    {
      "name": "Default",
      "state": "passed",
      "note": "GREEN phase - basic SearchBar with search icon"
    }
  ]
}
```

### 8. Repeat for Next Test

Add the NEXT test ONE AT A TIME and repeat steps 3-7.

**Common Second Tests**:
- Loading state
- Error state
- Disabled state
- With icon/feature
- Required field

**Example Second Test**:
```typescript
export const Loading: Story = {
  args: {
    placeholder: 'Searching...',
    loading: true,
  },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    const input = await canvas.findByPlaceholderText(/searching/i);
    await expect(input).toBeInTheDocument();

    const container = input.parentElement;
    const spinner = container?.querySelector('[class*="i-lucide"][class*="loader-circle"]');
    await expect(spinner).toBeInTheDocument();
  },
};
```

## TDD Guard Enforcement

The TDD guard hook enforces strict discipline. Common violations:

### Multiple Test Addition
**Violation**: Adding multiple tests/stories at once
**Fix**: Add ONE test at a time

### Premature Implementation
**Violation**: Creating component without RED phase evidence
**Fix**: Update test.json with failure evidence before implementing

### Over-Implementation
**Violation**: Adding untested props or functionality
**Fix**: Only implement what's needed for the current failing test

### Missing RED Phase
**Violation**: Implementing without test failure captured
**Fix**: Run tests, save output, update test.json with exit code and errors

## NuxtUI Component Patterns

### Wrapping UInput (Atom Example)

```vue
<script setup lang="ts">
defineProps<{
  placeholder?: string;
  type?: 'text' | 'email' | 'password' | 'search';
  disabled?: boolean;
}>();
</script>

<template>
  <UInput
    :placeholder="placeholder"
    :type="type"
    :disabled="disabled"
  />
</template>
```

### Combining UFormField + UInput (Molecule Example)

```vue
<script setup lang="ts">
defineProps<{
  label?: string;
  name?: string;
  placeholder?: string;
  required?: boolean;
}>();
</script>

<template>
  <UFormField :label="label" :name="name" :required="required">
    <UInput :placeholder="placeholder" :name="name" :required="required" />
  </UFormField>
</template>
```

### Common NuxtUI Props

Support these props when tests require them:
- `size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl'`
- `color?: 'primary' | 'secondary' | 'success' | 'error'`
- `variant?: 'solid' | 'outline' | 'soft' | 'ghost'`
- `loading?: boolean`
- `disabled?: boolean`
- `required?: boolean`

## Storybook Testing Patterns

### Finding Elements

```typescript
// By placeholder
const input = await canvas.findByPlaceholderText(/search/i);

// By label
const label = await canvas.findByLabelText(/email/i);

// By text content
const error = await canvas.findByText(/error message/i);

// By role
const button = await canvas.findByRole('button', { name: /submit/i });
```

### Common Assertions

```typescript
// Element exists
await expect(input).toBeInTheDocument();

// Has attribute
await expect(input).toHaveAttribute('required');
await expect(input).toHaveAttribute('type', 'search');

// Icon/spinner presence (use attribute selectors)
const icon = container?.querySelector('[class*="i-lucide"][class*="search"]');
await expect(icon).toBeInTheDocument();
```

## Test Coverage Guidelines

**Minimum tests per component**:
- **Atoms**: 2-3 tests (Default, Disabled, Loading/Error)
- **Molecules**: 3-5 tests (Default, With[Feature], State variations)
- **Organisms**: 5-10 tests (Multiple features, interactions, edge cases)

**What to test**:
1. Basic rendering with default props
2. Props affecting appearance/behavior
3. State variations (loading, disabled, error, empty)
4. Interactions (if applicable)
5. Validation and error messages
6. Accessibility (ARIA attributes, keyboard navigation)

## Common Pitfalls

### Pitfall 1: Storybook Hot Reload Issues
**Problem**: Tests fail with "failed to fetch" after creating component
**Solution**: Kill and restart Storybook server, wait for full rebuild

### Pitfall 2: Invalid querySelector Syntax
**Problem**: `querySelector('.iconify.i-lucide\\:icon')` fails
**Solution**: Use attribute selectors: `[class*="i-lucide"][class*="icon"]`

### Pitfall 3: Vue Prop Forwarding
**Problem**: Props work without explicit declaration
**Solution**: Leverage Vue's forwarding when appropriate, add explicit props when tests require them

### Pitfall 4: TDD Guard Blocks Refactoring
**Problem**: Guard blocks even reasonable code improvements
**Solution**: Only refactor tested code; add new tests before new features

## Running Tests

```bash
# Run all Storybook tests
pnpm test:storybook:run

# Run specific component tests
pnpm test:storybook:run -- ComponentName

# Run in watch mode (development)
pnpm test:storybook

# Run with coverage
pnpm test:storybook:run --coverage
```

## Success Criteria

A component is complete when:
- [ ] All planned tests pass (100% GREEN)
- [ ] Component follows naming conventions
- [ ] Props are properly typed with JSDoc comments
- [ ] Storybook autodocs enabled
- [ ] Atomic design level is correct
- [ ] Minimum test coverage achieved

## Resources

### References
- **references/naming-conventions.md** - Complete component naming and organizational guide following Atomic Design principles
- **references/tdd-workflow.md** - Detailed TDD workflow documentation with troubleshooting, patterns, and test.json management

### Assets
- **assets/story-template.ts** - Storybook story file template with TDD comments and common patterns
- **assets/component-template.vue** - Vue component template with NuxtUI patterns and prop examples

## Quick Start Checklist

For each new component:

1. [ ] Determine atomic level (atom/molecule/organism)
2. [ ] Create story file with ONE Default test
3. [ ] Run test to confirm failure (RED)
4. [ ] Save failure output to /tmp
5. [ ] Update test.json with RED phase evidence
6. [ ] Implement minimal component code
7. [ ] Run test to confirm success (GREEN)
8. [ ] Update test.json with GREEN phase
9. [ ] Repeat for next test

## Integration with Other Skills

This skill works well with:
- **nuxt-ui** - For NuxtUI component documentation and patterns
- **tailwindcss** - For styling and utility classes
- **turborepo** - For monorepo build and test execution
