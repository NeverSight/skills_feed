---
name: heroui-native-skill
description: Build beautiful, accessible mobile UIs with HeroUI Native components for React Native and Expo. Use when building mobile apps with React Native, Expo, or when the user mentions HeroUI Native, heroui-native, mobile UI components, or needs professional mobile interfaces with smooth animations and accessibility built-in.
---

# HeroUI Native

A component library built on Tailwind v4 via Uniwind for React Native/Expo. Components come with smooth animations, polished details, and built-in accessibility.

## Quick Start

### 1. Install

```bash
npm install heroui-native
```

### 2. Install Peer Dependencies

```bash
npm install react-native-screens@~4.16.0 react-native-reanimated@~4.1.1 react-native-gesture-handler@^2.28.0 react-native-worklets@0.5.1 react-native-safe-area-context@~5.6.0 react-native-svg@15.12.1 tailwind-variants@^3.2.2 tailwind-merge@^3.4.0 @gorhom/bottom-sheet@^5
```

### 3. Setup Uniwind

Follow [Uniwind installation guide](https://docs.uniwind.dev/quickstart) for Tailwind CSS in React Native.

### 4. Configure global.css

```css
@import "tailwindcss";
@import "uniwind";
@import "heroui-native/styles";
@source './node_modules/heroui-native/lib';
```

### 5. Wrap App with Provider

```tsx
import { HeroUINativeProvider } from "heroui-native";
import { GestureHandlerRootView } from "react-native-gesture-handler";

export default function App() {
  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <HeroUINativeProvider>{/* Your app content */}</HeroUINativeProvider>
    </GestureHandlerRootView>
  );
}
```

For Expo Router, wrap in `app/_layout.tsx`:

```tsx
import { HeroUINativeProvider } from "heroui-native";
import { Stack } from "expo-router";

export default function RootLayout() {
  return (
    <HeroUINativeProvider>
      <Stack />
    </HeroUINativeProvider>
  );
}
```

## CRITICAL: Native Only - Do Not Use Web Patterns

**This guide is for HeroUI Native ONLY.** Do NOT use any prior knowledge of HeroUI React (web) patterns.

### What Changed in Native

| Feature      | React (Web)          | Native (Mobile)                     |
| ------------ | -------------------- | ----------------------------------- |
| **Styling**  | Tailwind CSS v4      | Uniwind (Tailwind for React Native) |
| **Colors**   | oklch format         | HSL format                          |
| **Package**  | `@heroui/react@beta` | `heroui-native`                     |
| **Platform** | Web browsers         | iOS & Android                       |

### WRONG (React web patterns)

```tsx
// DO NOT DO THIS - React web pattern
import { Button } from "@heroui/react";
import "./styles.css"; // CSS files don't work in React Native

<Button className="bg-blue-500">Click me</Button>;
```

### CORRECT (Native patterns)

```tsx
// DO THIS - Native pattern (Uniwind, React Native components)
import { Button } from "heroui-native";

<Button variant="primary" onPress={() => console.log("Pressed!")}>
  Click me
</Button>;
```

**Always fetch Native docs before implementing.** Do not assume React web patterns work.

### Critical Setup Requirements

1. **Uniwind is Required** - HeroUI Native uses Uniwind (Tailwind CSS for React Native)
2. **HeroUINativeProvider Required** - Wrap your app with `HeroUINativeProvider`
3. **GestureHandlerRootView Required** - Wrap with `GestureHandlerRootView` from react-native-gesture-handler
4. **Use Compound Components** - Components use compound structure (e.g., `Card.Header`, `Card.Body`)
5. **Use onPress, not onClick** - React Native uses `onPress` event handlers
6. **Platform-Specific Code** - Use `Platform.OS` for iOS/Android differences

## Core Patterns

### Compound Components

Components use dot notation for sub-components that work together:

```tsx
import { Button, Dialog, Card } from 'heroui-native';

// Button with explicit label
<Button>
  <Button.Label>Click me</Button.Label>
</Button>

// Dialog with compound parts
<Dialog>
  <Dialog.Trigger>Open</Dialog.Trigger>
  <Dialog.Portal>
    <Dialog.Overlay />
    <Dialog.Content>
      <Dialog.Close />
      <Dialog.Title>Title</Dialog.Title>
      <Dialog.Description>Description</Dialog.Description>
    </Dialog.Content>
  </Dialog.Portal>
</Dialog>

// Card with sections
<Card>
  <Card.Header>...</Card.Header>
  <Card.Body>
    <Card.Title>Title</Card.Title>
    <Card.Description>Description</Card.Description>
  </Card.Body>
  <Card.Footer>...</Card.Footer>
</Card>
```

### The `asChild` Prop

Merge component functionality into a custom child element:

```tsx
<Dialog.Trigger asChild>
  <Button variant="primary">Open Dialog</Button>
</Dialog.Trigger>
```

### Styling

Use `className` with Tailwind classes (via Uniwind):

```tsx
<Button className="bg-accent px-6 py-3 rounded-lg">
  <Button.Label>Custom Button</Button.Label>
</Button>
```

Use render props for state-based styling:

```tsx
<RadioGroup.Item value="opt1">
  {({ isSelected }) => (
    <RadioGroup.Label
      className={cn(
        "text-foreground",
        isSelected && "text-accent font-semibold",
      )}
    >
      Option 1
    </RadioGroup.Label>
  )}
</RadioGroup.Item>
```

### Colors

Semantic color variables with automatic dark mode:

- `bg-background`, `bg-surface`, `bg-overlay` - backgrounds
- `bg-accent`, `text-accent-foreground` - brand colors
- `bg-success`, `bg-warning`, `bg-danger` - status colors
- `text-foreground`, `text-muted` - text colors

## Available Components

For detailed component documentation, patterns, and props, see [references/components.md](../Welcome!/components.md).

### Buttons

- **Button** - Interactive button with variants: primary, secondary, tertiary, ghost, danger, danger-soft

### Forms

- **TextField** - Text input with label, description, error handling
- **Checkbox** - Toggle between checked/unchecked states
- **RadioGroup** - Single selection from options
- **Switch** - Toggle on/off states
- **Select** - Dropdown selection
- **InputOTP** - One-time password input
- **FormField** - Wrapper for consistent form layout
- **Label**, **Description**, **ErrorView** - Form helpers

### Navigation

- **Tabs** - Tabbed views with animated transitions
- **Accordion** - Collapsible content panels

### Overlays

- **Dialog** - Modal overlay with gestures
- **Bottom Sheet** - Slides up from bottom
- **Popover** - Floating content anchored to trigger
- **Toast** - Temporary notifications via `useToast()`

### Feedback

- **Spinner** - Loading indicator
- **Skeleton** / **SkeletonGroup** - Loading placeholders

### Layout

- **Card** - Container with Header, Body, Footer
- **Surface** - Elevation and background styling
- **Divider** - Visual separator

### Media

- **Avatar** - User avatar with image, initials, or fallback

### Data Display

- **Chip** - Compact capsule element

### Utilities

- **PressableFeedback** - Visual press feedback
- **ScrollShadow** - Gradient shadows on scroll
- **cn** - Class name utility (from heroui-native)
- **useThemeColor** - Access theme colors programmatically
