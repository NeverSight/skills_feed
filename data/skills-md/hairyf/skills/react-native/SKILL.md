---
name: react-native
description: React Native framework for building native mobile apps with React. Use when building iOS/Android apps, working with native components, handling touch interactions, animations, or platform APIs.
metadata:
  author: Hairyf
  version: "2026.1.31"
  source: Generated from https://github.com/facebook/react-native-website, scripts located at https://github.com/antfu/skills
---

# React Native

> The skill is based on React Native, generated at 2026-01-31.

React Native lets you build mobile apps using only JavaScript. It uses the same design as React, letting you compose a rich mobile UI from declarative components. With React Native, you don't build a "mobile web app", an "HTML5 app", or a "hybrid app". You build a real mobile app that's indistinguishable from an app built using Objective-C or Java.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Core Components | View, Text, Image, TextInput, ScrollView - fundamental UI building blocks | [core-components](references/core-components.md) |
| Layout with Flexbox | Flexbox layout system for positioning and aligning components | [core-layout](references/core-layout.md) |
| Styling | StyleSheet API for creating and organizing component styles | [core-styling](references/core-styling.md) |

## Features

### Animations

| Topic | Description | Reference |
|-------|-------------|-----------|
| Animated API | Create fluid animations with Animated.Value, timing, spring, and gesture integration | [features-animations](references/features-animations.md) |
| Easing Functions | Easing functions for custom animation curves and natural motion | [features-easing](references/features-easing.md) |

### User Interactions

| Topic | Description | Reference |
|-------|-------------|-----------|
| Touch Handling | Pressable, Touchable components, and gesture responders for handling user input | [features-touch-handling](references/features-touch-handling.md) |
| Keyboard | Keyboard API for handling keyboard events, dismissing keyboard, and KeyboardAvoidingView | [features-keyboard](references/features-keyboard.md) |

### UI Components

| Topic | Description | Reference |
|-------|-------------|-----------|
| Additional Components | Modal, Switch, ActivityIndicator, RefreshControl for dialogs, toggles, loading states | [components-ui](references/components-ui.md) |

### Data Display

| Topic | Description | Reference |
|-------|-------------|-----------|
| Lists | FlatList and SectionList for efficiently rendering large, scrollable lists | [features-lists](references/features-lists.md) |

### Styling and Theming

| Topic | Description | Reference |
|-------|-------------|-----------|
| Colors and Theming | Colors, PlatformColor, Appearance API for theming and dark mode support | [features-colors-theming](references/features-colors-theming.md) |

### Platform Integration

| Topic | Description | Reference |
|-------|-------------|-----------|
| Platform APIs | Linking, Dimensions, Platform detection, AppState, and native integrations | [features-platform-apis](references/features-platform-apis.md) |
| Network | Fetch API for making HTTP requests and handling network responses | [features-network](references/features-network.md) |
| StatusBar | Control status bar appearance, style, and visibility | [features-statusbar](references/features-statusbar.md) |
| Share & Vibration | Native share dialog and device vibration for haptic feedback | [features-share-vibration](references/features-share-vibration.md) |
| Timers | setTimeout, setInterval, requestAnimationFrame for scheduling and delays | [features-timers](references/features-timers.md) |
| Platform-Specific APIs | Android (PermissionsAndroid, ToastAndroid, DrawerLayoutAndroid) and iOS (ActionSheetIOS) | [features-platform-specific](references/features-platform-specific.md) |

### Accessibility

| Topic | Description | Reference |
|-------|-------------|-----------|
| Accessibility | Screen reader support, accessibility labels, roles, and states | [features-accessibility](references/features-accessibility.md) |

### Advanced Styling

| Topic | Description | Reference |
|-------|-------------|-----------|
| Transforms | 2D and 3D transforms for rotation, scale, translation, and skew | [features-transforms](references/features-transforms.md) |

### Best Practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| Performance | Performance optimization techniques, profiling, and common bottlenecks | [best-practices-performance](references/best-practices-performance.md) |
| Debugging | Debugging tools, Dev Menu, LogBox, React Native DevTools, and debugging techniques | [best-practices-debugging](references/best-practices-debugging.md) |

## Key Recommendations

- **Use StyleSheet.create()** for all styles instead of inline objects
- **Use FlatList** instead of ScrollView for long lists
- **Enable useNativeDriver** for animations when possible (transform, opacity)
- **Use Pressable** for new touch interactions (preferred over Touchable components)
- **Handle platform differences** with Platform.select() and Platform.OS
- **Test on real devices** - simulator behavior may differ from actual devices
- **Optimize list performance** with getItemLayout for fixed-height items
- **Use TypeScript** for better type safety and developer experience
