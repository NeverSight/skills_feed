---
name: react-native
description: >-
  Best practices for React Native and Expo applications. Covers list
  performance, animations with Reanimated, navigation, UI patterns, and
  monorepo configuration. Use when building, reviewing, or optimizing
  React Native / Expo apps.
---

# React Native

Performance-first patterns for React Native and Expo, organized by impact.

## Priority 1: List Performance (CRITICAL)

Lists are the #1 performance bottleneck in RN apps. Get these right first.

### Use FlashList

Replace `FlatList` with `@shopify/flash-list` for large lists.

```tsx
import { FlashList } from '@shopify/flash-list';

<FlashList
  data={items}
  renderItem={({ item }) => <ItemRow item={item} />}
  estimatedItemSize={80}
  keyExtractor={(item) => item.id}
/>
```

### Memoize List Items

Every list item must be memoized.

```tsx
const ItemRow = memo(function ItemRow({ item }: { item: Item }) {
  return (
    <View style={styles.row}>
      <Text>{item.title}</Text>
    </View>
  );
});
```

### Stabilize Callbacks

Extract callbacks and avoid inline objects in list items.

```tsx
// BAD: New function + new style object every render
<Pressable onPress={() => onSelect(item.id)} style={{ padding: 16 }}>

// GOOD: Stable references
const handlePress = useCallback(() => onSelect(item.id), [item.id, onSelect]);
<Pressable onPress={handlePress} style={styles.pressable}>
```

### Optimize Images in Lists

Use `expo-image` with proper sizing and caching.

```tsx
import { Image } from 'expo-image';

<Image
  source={{ uri: item.thumbnailUrl }}
  style={styles.thumbnail}
  contentFit="cover"
  placeholder={item.blurhash}
  transition={200}
  recyclingKey={item.id}
/>
```

### Item Types for Heterogeneous Lists

Use `getItemType` to help FlashList reuse cells efficiently.

```tsx
<FlashList
  data={mixedItems}
  renderItem={renderItem}
  getItemType={(item) => item.type} // 'header' | 'content' | 'ad'
  estimatedItemSize={100}
/>
```

## Priority 2: Animation (HIGH)

### GPU-Only Properties

Only animate `transform` and `opacity`. Everything else triggers layout.

```tsx
import Animated, { useAnimatedStyle, withSpring } from 'react-native-reanimated';

const animatedStyle = useAnimatedStyle(() => ({
  transform: [{ scale: withSpring(isPressed.value ? 0.95 : 1) }],
  opacity: withSpring(isVisible.value ? 1 : 0),
}));
```

### Derived Values

Use `useDerivedValue` for computed animations to avoid redundant calculations.

```tsx
const progress = useSharedValue(0);
const rotation = useDerivedValue(() => `${progress.value * 360}deg`);

const animatedStyle = useAnimatedStyle(() => ({
  transform: [{ rotate: rotation.value }],
}));
```

### Gesture Handling

Use `react-native-gesture-handler` for 60fps gesture tracking.

```tsx
import { Gesture, GestureDetector } from 'react-native-gesture-handler';

const pan = Gesture.Pan()
  .onUpdate((e) => {
    translateX.value = e.translationX;
    translateY.value = e.translationY;
  })
  .onEnd(() => {
    translateX.value = withSpring(0);
    translateY.value = withSpring(0);
  });

// Use Gesture.Tap() instead of Pressable for animated press feedback
const tap = Gesture.Tap()
  .onBegin(() => { scale.value = withSpring(0.95); })
  .onFinalize(() => { scale.value = withSpring(1); });
```

## Priority 3: Navigation (HIGH)

### Native Navigators

Always prefer native stack and tabs over JS-based alternatives.

```tsx
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';

// BAD: JS-based stack (slower transitions, no native gestures)
import { createStackNavigator } from '@react-navigation/stack';

// GOOD: Native stack (native transitions + gestures)
const Stack = createNativeStackNavigator();
```

### Screen Options

Configure headers and animations natively.

```tsx
<Stack.Screen
  name="Detail"
  component={DetailScreen}
  options={{
    headerLargeTitle: true,    // iOS large title
    animation: 'slide_from_right',
  }}
/>
```

## Priority 4: UI Patterns (HIGH)

### Safe Areas

Handle safe areas correctly for all device shapes.

```tsx
import { SafeAreaView } from 'react-native-safe-area-context';

// For scrollable content
<SafeAreaView edges={['top']} style={{ flex: 1 }}>
  <ScrollView contentInsetAdjustmentBehavior="automatic">
    {children}
  </ScrollView>
</SafeAreaView>
```

### Native Modals

Use native modal presentation instead of JS overlays.

```tsx
<Stack.Screen
  name="Settings"
  component={SettingsScreen}
  options={{ presentation: 'modal' }}
/>
```

### Native Menus

Use context menus instead of custom dropdown components.

```tsx
import * as ContextMenu from 'zeego/context-menu';

<ContextMenu.Root>
  <ContextMenu.Trigger>
    <Pressable><Text>Options</Text></Pressable>
  </ContextMenu.Trigger>
  <ContextMenu.Content>
    <ContextMenu.Item key="edit" onSelect={handleEdit}>
      <ContextMenu.ItemTitle>Edit</ContextMenu.ItemTitle>
    </ContextMenu.Item>
    <ContextMenu.Item key="delete" onSelect={handleDelete} destructive>
      <ContextMenu.ItemTitle>Delete</ContextMenu.ItemTitle>
    </ContextMenu.Item>
  </ContextMenu.Content>
</ContextMenu.Root>
```

### Pressable Over TouchableOpacity

```tsx
// BAD: Legacy touch component
<TouchableOpacity onPress={onPress}>{children}</TouchableOpacity>

// GOOD: Modern Pressable with feedback
<Pressable
  onPress={onPress}
  style={({ pressed }) => [styles.button, pressed && styles.pressed]}
  android_ripple={{ color: 'rgba(0,0,0,0.1)' }}
>
  {children}
</Pressable>
```

## Priority 5: State Management (MEDIUM)

### Minimize Re-renders

Subscribe only to the state you need.

```tsx
// BAD: Re-renders on any store change
const store = useStore();
return <Text>{store.user.name}</Text>;

// GOOD: Selector extracts only needed value
const name = useStore((s) => s.user.name);
return <Text>{name}</Text>;
```

### React Compiler Compatibility

When using React Compiler with Reanimated:

```tsx
// Destructure shared value functions for compiler compatibility
const { value } = useSharedValue(0);

// Use worklet directive for Reanimated callbacks
const animatedStyle = useAnimatedStyle(() => {
  'worklet';
  return { opacity: value };
});
```

## Priority 6: Monorepo (MEDIUM)

### Native Dependencies

Keep native dependencies in the app package, not shared packages.

```
packages/
  ui/              # Pure React components (no native deps)
  shared/          # Business logic, types
apps/
  mobile/          # Native deps (expo-image, reanimated) here
```

### Single Dependency Versions

Enforce one version per dependency across the monorepo.

```json
// Root package.json
{
  "resolutions": {
    "react-native": "0.76.x",
    "react-native-reanimated": "3.x"
  }
}
```

## Quick Reference

| Issue | Fix | Priority |
|-------|-----|----------|
| Slow scrolling lists | FlashList + memoized items | CRITICAL |
| Inline objects in lists | Extract to StyleSheet | CRITICAL |
| Janky animations | Only transform/opacity | HIGH |
| JS-based navigation | Native stack/tabs | HIGH |
| Custom dropdown menus | Native context menus | HIGH |
| Full store subscription | Selectors | MEDIUM |
| Native deps in shared pkg | Move to app package | MEDIUM |
