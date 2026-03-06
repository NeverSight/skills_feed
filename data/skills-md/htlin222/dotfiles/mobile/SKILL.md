---
name: mobile
description: Develop React Native or Flutter apps with native integrations. Use for mobile development, cross-platform code, or app optimization.
---

# Mobile Development

Build cross-platform mobile applications.

## When to Use

- React Native development
- Flutter development
- Mobile performance issues
- Native module integration
- App store deployment

## React Native

### Component Structure

```tsx
import React, { useState, useCallback } from "react";
import { View, Text, TouchableOpacity, StyleSheet } from "react-native";

interface Props {
  title: string;
  onPress: () => void;
}

export function Button({ title, onPress }: Props) {
  const [pressed, setPressed] = useState(false);

  const handlePress = useCallback(() => {
    setPressed(true);
    onPress();
  }, [onPress]);

  return (
    <TouchableOpacity
      style={[styles.button, pressed && styles.pressed]}
      onPress={handlePress}
      activeOpacity={0.7}
    >
      <Text style={styles.text}>{title}</Text>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  button: {
    backgroundColor: "#007AFF",
    padding: 16,
    borderRadius: 8,
  },
  pressed: {
    opacity: 0.8,
  },
  text: {
    color: "white",
    fontWeight: "600",
    textAlign: "center",
  },
});
```

### Navigation

```tsx
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

type RootStackParamList = {
  Home: undefined;
  Details: { id: string };
};

const Stack = createNativeStackNavigator<RootStackParamList>();

function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Details" component={DetailsScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

## Flutter

### Widget Structure

```dart
class MyButton extends StatelessWidget {
  final String title;
  final VoidCallback onPressed;

  const MyButton({
    Key? key,
    required this.title,
    required this.onPressed,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: onPressed,
      style: ElevatedButton.styleFrom(
        padding: const EdgeInsets.all(16),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8),
        ),
      ),
      child: Text(title),
    );
  }
}
```

## Performance Tips

- Use FlatList/ListView for long lists
- Memoize callbacks with useCallback
- Avoid inline styles (use StyleSheet)
- Lazy load screens and images
- Profile with Flipper/DevTools

## Common Patterns

| Pattern    | React Native        | Flutter             |
| ---------- | ------------------- | ------------------- |
| State      | useState/Redux      | setState/Riverpod   |
| Navigation | React Navigation    | Navigator 2.0       |
| HTTP       | fetch/axios         | http/dio            |
| Storage    | AsyncStorage        | shared_preferences  |
| Animations | Animated/Reanimated | AnimationController |

## Examples

**Input:** "Build a list screen"
**Action:** Create FlatList with virtualization, pull-to-refresh, pagination

**Input:** "Add offline support"
**Action:** Implement AsyncStorage caching, sync queue, network detection
