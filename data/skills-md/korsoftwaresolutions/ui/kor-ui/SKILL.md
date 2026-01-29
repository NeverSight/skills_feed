---
name: kor-ui
description: Complete guide for using the Kor UI library (@korsolutions/ui) in React Native and Expo applications. Use this skill when building user interfaces with Universal UI, customizing themes, setting up the library, working with any of the 24+ components (Button, Input, Select, Alert, Card, Tabs, Menu, Popover, Calendar, Toast, etc.), styling and theming, implementing compound components, debugging component issues, or when the user mentions "@korsolutions/ui", "Universal UI", "UIProvider", or asks about unstyled primitives, theme customization, or React Native UI components. This skill covers installation, provider setup, component usage patterns, theme customization, variant system, hooks, responsive design, and troubleshooting.
---

# Universal UI Library

Universal UI (@korsolutions/ui) is a library of unstyled UI primitives for React Native and Expo applications. It provides production-ready components with a focus on minimal dependencies, compound component patterns, and comprehensive theming support.

## Core Principles

- **Unstyled Primitives**: Components are unstyled by default with variant-based styling
- **Compound Components**: All components follow Root + sub-component pattern
- **Variant System**: Each component offers multiple style variants
- **Minimal Dependencies**: Only React Native and Expo core dependencies
- **Full TypeScript Support**: Complete type definitions for all components
- **Cross-Platform**: iOS, Android, and Web support

## Quick Start

### Installation

```bash
npm install @korsolutions/ui
# or
yarn add @korsolutions/ui
# or
bun add @korsolutions/ui
```

### Provider Setup

Wrap your application with `UIProvider` in your root layout:

```tsx
import { UIProvider } from "@korsolutions/ui";
import { useSafeAreaInsets } from "react-native-safe-area-context";

export default function RootLayout() {
  const safeAreaInsets = useSafeAreaInsets();

  return (
    <UIProvider safeAreaInsets={safeAreaInsets}>
      <YourApp />
    </UIProvider>
  );
}
```

### Basic Import Pattern

```tsx
import { Button, Input, Card } from "@korsolutions/ui";

function MyComponent() {
  return (
    <Card.Root>
      <Card.Body>
        <Button.Root onPress={() => console.log("Pressed")}>
          <Button.Label>Click Me</Button.Label>
        </Button.Root>
      </Card.Body>
    </Card.Root>
  );
}
```

### Your First Component

```tsx
import { useState } from "react";
import { Button } from "@korsolutions/ui";

function SubmitButton() {
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    await submitForm();
    setLoading(false);
  };

  return (
    <Button.Root variant="default" isLoading={loading} onPress={handleSubmit}>
      <Button.Label>Submit</Button.Label>
    </Button.Root>
  );
}
```

## Component Overview

### Layout & Structure

| Component     | Description                                     | Variants | Reference                                                        |
| ------------- | ----------------------------------------------- | -------- | ---------------------------------------------------------------- |
| **Card**      | Content container with header, body, and footer | default  | [Layout Components](./references/components-layout.md#card)      |
| **ScrollBar** | Custom scrollbar styling                        | default  | [Layout Components](./references/components-layout.md#scrollbar) |
| **Portal**    | Render components outside hierarchy             | -        | [Layout Components](./references/components-layout.md#portal)    |
| **List**      | Performance-optimized list rendering            | -        | [Layout Components](./references/components-layout.md#list)      |

### Form Inputs

| Component        | Description                                          | Variants | Reference                                                          |
| ---------------- | ---------------------------------------------------- | -------- | ------------------------------------------------------------------ |
| **Input**        | Text input field                                     | default  | [Input Components](./references/components-inputs.md#input)        |
| **NumericInput** | Formatted numeric input (currency, percentage, etc.) | default  | [Input Components](./references/components-inputs.md#numericinput) |
| **Textarea**     | Multi-line text input                                | default  | [Input Components](./references/components-inputs.md#textarea)     |
| **Checkbox**     | Toggle selection with label                          | default  | [Input Components](./references/components-inputs.md#checkbox)     |
| **Select**       | Dropdown selection with search                       | default  | [Input Components](./references/components-inputs.md#select)       |
| **Field**        | Form field wrapper with label and validation         | -        | [Input Components](./references/components-inputs.md#field)        |

### Display Components

| Component      | Description                             | Variants                                               | Reference                                                           |
| -------------- | --------------------------------------- | ------------------------------------------------------ | ------------------------------------------------------------------- |
| **Typography** | Text with semantic variants             | heading-xs to 3xl, body-xs to lg, label, code, caption | [Display Components](./references/components-display.md#typography) |
| **Avatar**     | User avatar with image and fallback     | default                                                | [Display Components](./references/components-display.md#avatar)     |
| **Badge**      | Status indicators and labels            | default, secondary, success, warning, danger, info     | [Display Components](./references/components-display.md#badge)      |
| **Icon**       | Icon rendering with render prop pattern | -                                                      | [Display Components](./references/components-display.md#icon)       |
| **Empty**      | Empty state placeholders                | default                                                | [Display Components](./references/components-display.md#empty)      |
| **Progress**   | Linear progress indicators              | default                                                | [Display Components](./references/components-display.md#progress)   |

### Interactive Components

| Component    | Description                        | Variants           | Reference                                                                 |
| ------------ | ---------------------------------- | ------------------ | ------------------------------------------------------------------------- |
| **Button**   | Action buttons with loading states | default, secondary | [Interactive Components](./references/components-interactive.md#button)   |
| **Tabs**     | Tabbed navigation                  | default, line      | [Interactive Components](./references/components-interactive.md#tabs)     |
| **Menu**     | Dropdown menus                     | default            | [Interactive Components](./references/components-interactive.md#menu)     |
| **Popover**  | Positioned overlay content         | default            | [Interactive Components](./references/components-interactive.md#popover)  |
| **Calendar** | Date picker with range selection   | default            | [Interactive Components](./references/components-interactive.md#calendar) |

### Feedback Components

| Component       | Description                     | Variants                 | Reference                                                              |
| --------------- | ------------------------------- | ------------------------ | ---------------------------------------------------------------------- |
| **Alert**       | Inline notifications with icons | default, destructive     | [Feedback Components](./references/components-feedback.md#alert)       |
| **AlertDialog** | Modal confirmation dialogs      | default                  | [Feedback Components](./references/components-feedback.md#alertdialog) |
| **Toast**       | Transient notifications         | default, success, danger | [Feedback Components](./references/components-feedback.md#toast)       |

## Compound Component Pattern

All Universal UI components follow a compound component pattern where a parent component (usually `Root`) provides context to child sub-components.

### Structure

```tsx
<Component.Root {...rootProps}>
  <Component.SubComponent1 {...props} />
  <Component.SubComponent2 {...props} />
</Component.Root>
```

### Common Sub-Components

Most components share similar sub-component naming:

- **Root** - Parent container that provides context
- **Label** - Text label for the component
- **Icon** - Icon display with render prop pattern
- **Description** - Secondary descriptive text
- **Title** - Primary heading text
- **Body** - Main content area
- **Header** - Top section
- **Footer** - Bottom section

### Example: Button

```tsx
<Button.Root variant="default" onPress={handlePress} isLoading={loading}>
  <Button.Label>Submit Form</Button.Label>
</Button.Root>
```

### Example: Alert with Icon

```tsx
import { AlertCircle } from "lucide-react-native";

<Alert.Root variant="destructive">
  <Alert.Icon render={AlertCircle} />
  <Alert.Body>
    <Alert.Title>Error</Alert.Title>
    <Alert.Description>Something went wrong</Alert.Description>
  </Alert.Body>
</Alert.Root>;
```

### Example: Field with Input

```tsx
<Field.Root>
  <Field.Label for="email">Email Address</Field.Label>
  <Input id="email" value={email} onChange={setEmail} placeholder="you@example.com" />
  <Field.Description>We'll never share your email.</Field.Description>
  {error && <Field.Error>{error}</Field.Error>}
</Field.Root>
```

### Style Composition

Component styles are always composed with variant styles first, allowing user styles to override:

```tsx
// Variant styles are applied first
<Button.Root style={{ marginTop: 16 }}>
  <Button.Label style={{ fontWeight: "bold" }}>Custom Button</Button.Label>
</Button.Root>
```

This ensures your custom styles always take precedence over variant defaults.

## Theme System Basics

Universal UI includes a comprehensive theming system with light/dark mode support.

### Theme Tokens

The theme provides these customizable tokens:

- **colors** - Color palette with light/dark schemes
- **radius** - Border radius (default: 10)
- **fontSize** - Base font size (default: 16)
- **fontFamily** - Font family (default: "System")
- **letterSpacing** - Letter spacing (default: 0)

### Color Tokens

Each color scheme (light/dark) includes:

- **background** - Main background color
- **foreground** - Main text color
- **primary** - Primary brand color
- **primaryForeground** - Text on primary color
- **secondary** - Secondary brand color
- **secondaryForeground** - Text on secondary color
- **muted** - Muted background color
- **mutedForeground** - Muted text color
- **border** - Border color
- **surface** - Surface/card background
- **success**, **warning**, **danger**, **info** - Semantic colors

### Using the Theme

Access the theme in your components:

```tsx
import { useTheme } from "@korsolutions/ui";

function MyComponent() {
  const theme = useTheme();

  return (
    <View
      style={{
        backgroundColor: theme.colors.background,
        borderRadius: theme.radius,
        padding: 16,
      }}
    >
      <Text
        style={{
          color: theme.colors.foreground,
          fontSize: theme.fontSize,
          fontFamily: theme.fontFamily,
        }}
      >
        Themed Content
      </Text>
    </View>
  );
}
```

### Color Scheme

Toggle between light and dark mode:

```tsx
const theme = useTheme();

// Get current scheme
console.log(theme.colorScheme); // "light" | "dark"

// Set color scheme
theme.setColorScheme("dark");
```

### Quick Customization

Customize the theme via UIProvider:

```tsx
<UIProvider
  theme={{
    radius: 12,
    fontSize: 18,
    colors: {
      light: {
        primary: "hsla(220, 90%, 56%, 1)",
        primaryForeground: "hsla(0, 0%, 100%, 1)",
      },
      dark: {
        primary: "hsla(220, 90%, 70%, 1)",
        primaryForeground: "hsla(0, 0%, 100%, 1)",
      },
    },
  }}
  safeAreaInsets={safeAreaInsets}
>
  <App />
</UIProvider>
```

For detailed theming documentation, see [Theme Customization](./references/theme-customization.md).

## Common Patterns

### Form Field with Validation

```tsx
import { Field, Input } from "@korsolutions/ui";

<Field.Root>
  <Field.Label for="email">Email</Field.Label>
  <Input id="email" value={email} onChange={setEmail} placeholder="you@example.com" />
  <Field.Description>Enter your email address</Field.Description>
  {error && <Field.Error>{error}</Field.Error>}
</Field.Root>;
```

### Icons with Render Prop

Universal UI uses a render prop pattern for icons, supporting any icon library:

```tsx
import { AlertCircle, CheckCircle } from "lucide-react-native";
import { Alert } from "@korsolutions/ui";

// With lucide-react-native
<Alert.Icon render={AlertCircle} />

// With custom function
<Alert.Icon render={(props) => <CheckCircle {...props} size={20} />} />

// With @expo/vector-icons
import { MaterialCommunityIcons } from "@expo/vector-icons";
<Alert.Icon render={(props) => (
  <MaterialCommunityIcons {...props} name="alert-circle" />
)} />
```

### Controlled State Management

Most input components use controlled state:

```tsx
import { useState } from "react";
import { Input, Checkbox } from "@korsolutions/ui";

function Form() {
  const [text, setText] = useState("");
  const [checked, setChecked] = useState(false);

  return (
    <>
      <Input value={text} onChange={setText} />
      <Checkbox.Root checked={checked} onChange={setChecked}>
        <Checkbox.Indicator />
        <Checkbox.Content>
          <Checkbox.Title>Accept terms</Checkbox.Title>
        </Checkbox.Content>
      </Checkbox.Root>
    </>
  );
}
```

### Loading States

Buttons support loading states with built-in spinner:

```tsx
<Button.Root isLoading={isSubmitting} onPress={handleSubmit}>
  <Button.Label>Submit</Button.Label>
</Button.Root>
```

When `isLoading` is true, the button displays `Button.Spinner` and disables interaction.

### Disabled States

Most components support disabled states:

```tsx
<Button.Root isDisabled={!formValid} onPress={handleSubmit}>
  <Button.Label>Submit</Button.Label>
</Button.Root>

<Input isDisabled value={email} onChange={setEmail} />

<Checkbox.Root disabled checked={value} onChange={setValue}>
  <Checkbox.Indicator />
  <Checkbox.Content>
    <Checkbox.Title>Disabled option</Checkbox.Title>
  </Checkbox.Content>
</Checkbox.Root>
```

### Selecting Variants

Most components offer multiple variants:

```tsx
// Button variants
<Button.Root variant="default">
  <Button.Label>Default Button</Button.Label>
</Button.Root>

<Button.Root variant="secondary">
  <Button.Label>Secondary Button</Button.Label>
</Button.Root>

// Alert variants
<Alert.Root variant="default">
  <Alert.Body>
    <Alert.Title>Info</Alert.Title>
  </Alert.Body>
</Alert.Root>

<Alert.Root variant="destructive">
  <Alert.Body>
    <Alert.Title>Error</Alert.Title>
  </Alert.Body>
</Alert.Root>

// Badge variants
<Badge variant="success">Active</Badge>
<Badge variant="danger">Inactive</Badge>
<Badge variant="warning">Pending</Badge>
```

### Style Overrides

Override component styles using the `style` prop:

```tsx
<Button.Root
  style={{
    marginTop: 20,
    backgroundColor: "blue",
  }}
>
  <Button.Label style={{ color: "white", fontSize: 18 }}>Custom Styled</Button.Label>
</Button.Root>
```

## Import Reference

### Component Imports

```tsx
// Import individual components
import { Button, Input, Card, Alert } from "@korsolutions/ui";

// Import all components
import * as UI from "@korsolutions/ui";
```

### Hook Imports

```tsx
// Theme hook
import { useTheme } from "@korsolutions/ui";

// Responsive design hook
import { useScreenSize } from "@korsolutions/ui";

// React Navigation theme integration
import { useReactNavigationTheme } from "@korsolutions/ui";
```

### Provider Import

```tsx
import { UIProvider } from "@korsolutions/ui";
```

### Type Imports

```tsx
// Component prop types
import type { ButtonRootProps } from "@korsolutions/ui";
import type { InputProps } from "@korsolutions/ui";

// Theme types
import type { ThemeAssets, Colors } from "@korsolutions/ui";
```

## Quick Troubleshooting

### Provider Not Wrapping App

**Issue**: Components don't render or theme doesn't apply

**Solution**: Ensure `UIProvider` wraps your app in the root layout:

```tsx
// app/_layout.tsx
import { UIProvider } from "@korsolutions/ui";

export default function RootLayout() {
  return (
    <UIProvider>
      <Stack />
    </UIProvider>
  );
}
```

### Import Errors

**Issue**: Cannot resolve `@korsolutions/ui`

**Solution**: Install the package and restart your bundler:

```bash
npm install @korsolutions/ui
# Restart Metro bundler
```

### Theme Not Updating

**Issue**: Theme changes don't reflect in components

**Solution**: Ensure theme customization is passed to UIProvider before app renders:

```tsx
const customTheme = {
  colors: { light: { primary: "hsla(220, 90%, 56%, 1)" } },
};

<UIProvider theme={customTheme}>
  <App />
</UIProvider>;
```

### Styles Not Applying

**Issue**: Custom styles don't override component styles

**Solution**: Remember style composition order - user styles always override variant styles:

```tsx
// This works - style prop overrides variant
<Button.Root style={{ backgroundColor: "red" }}>
  <Button.Label>Red Button</Button.Label>
</Button.Root>
```

For comprehensive troubleshooting, see [Troubleshooting Guide](./references/troubleshooting.md).

## Reference Documentation

Consult these detailed references as needed:

### Component References

- [Layout Components](./references/components-layout.md) - Card, ScrollBar, Portal, List
- [Input Components](./references/components-inputs.md) - Input, NumericInput, Textarea, Checkbox, Select, Field
- [Display Components](./references/components-display.md) - Typography, Avatar, Badge, Icon, Empty, Progress
- [Interactive Components](./references/components-interactive.md) - Button, Tabs, Menu, Popover, Calendar
- [Feedback Components](./references/components-feedback.md) - Alert, AlertDialog, Toast

### System References

- [Theme Customization](./references/theme-customization.md) - Complete theming guide with color schemes, typography, and responsive design
- [Patterns & Recipes](./references/patterns-recipes.md) - Common implementation patterns for forms, modals, navigation, and feedback
- [Troubleshooting](./references/troubleshooting.md) - Solutions for setup, component, type, and platform-specific issues
