---
name: react-native-basics
description: Master React Native fundamentals - components, styling, layout, and Expo
sasmp_version: "1.3.0"
bonded_agent: 01-react-native-fundamentals
bond_type: PRIMARY_BOND
version: "2.0.0"
updated: "2025-01"
---

# React Native Basics Skill

> Learn production-ready React Native fundamentals including core components, StyleSheet, Flexbox, and Expo SDK.

## Prerequisites

- JavaScript/TypeScript fundamentals
- React basics (components, props, state, hooks)
- Node.js and npm/yarn installed
- Xcode (iOS) or Android Studio (Android)

## Learning Objectives

After completing this skill, you will be able to:
- [ ] Create and compose React Native components
- [ ] Apply styles using StyleSheet API
- [ ] Build responsive layouts with Flexbox
- [ ] Use platform-specific code (iOS/Android)
- [ ] Set up and use Expo for development

---

## Topics Covered

### 1. Core Components
```
View          - Container component (like div)
Text          - Text display (required for strings)
Image         - Image rendering
ScrollView    - Scrollable container
FlatList      - Optimized list rendering
TextInput     - User input
Pressable     - Touch handling
```

### 2. Styling System
```typescript
// StyleSheet.create for performance
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    padding: 16,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#1a1a1a',
  },
});
```

### 3. Flexbox Layout
```typescript
// Common patterns
flexDirection: 'row' | 'column'     // Main axis
justifyContent: 'center' | 'space-between'  // Main axis alignment
alignItems: 'center' | 'stretch'    // Cross axis alignment
flex: 1                              // Grow to fill
```

### 4. Platform-Specific Code
```typescript
import { Platform } from 'react-native';

// Method 1: Platform.select
const styles = StyleSheet.create({
  shadow: Platform.select({
    ios: { shadowColor: '#000', shadowOpacity: 0.1 },
    android: { elevation: 4 },
  }),
});

// Method 2: Platform.OS
if (Platform.OS === 'ios') {
  // iOS specific code
}
```

### 5. Expo Setup
```bash
# Create new project
npx create-expo-app MyApp
cd MyApp

# Start development
npx expo start

# Build for production
eas build --platform all
```

---

## Quick Start Example

```tsx
import React from 'react';
import { View, Text, StyleSheet, FlatList, Pressable } from 'react-native';

interface Item {
  id: string;
  title: string;
}

export default function App() {
  const [items, setItems] = React.useState<Item[]>([
    { id: '1', title: 'Learn React Native' },
    { id: '2', title: 'Build first app' },
  ]);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>My Tasks</Text>
      <FlatList
        data={items}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <Pressable style={styles.item}>
            <Text>{item.title}</Text>
          </Pressable>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16, backgroundColor: '#f5f5f5' },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 16 },
  item: { backgroundColor: '#fff', padding: 16, marginBottom: 8, borderRadius: 8 },
});
```

---

## Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| "Text strings must be wrapped" | Raw text outside `<Text>` | Wrap all text in `<Text>` |
| Styles not applying | Plain object vs StyleSheet | Use `StyleSheet.create()` |
| FlatList not scrolling | No height/flex | Add `flex: 1` to parent |
| Image not showing | Invalid source | Check URI or require path |

---

## Validation Checklist

- [ ] Components render without errors
- [ ] Styles apply correctly on both platforms
- [ ] FlatList handles large lists efficiently
- [ ] Platform-specific code works correctly
- [ ] Expo build succeeds

---

## Related Resources

- [React Native Docs](https://reactnative.dev/docs/getting-started)
- [Expo Docs](https://docs.expo.dev/)

---

## Usage

```
Skill("react-native-basics")
```

**Bonded Agent**: `01-react-native-fundamentals`
