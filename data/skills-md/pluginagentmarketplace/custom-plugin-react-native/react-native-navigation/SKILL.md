---
name: react-native-navigation
description: Master React Navigation - stacks, tabs, drawers, deep linking, and TypeScript integration
sasmp_version: "1.3.0"
bonded_agent: 02-react-native-navigation
bond_type: PRIMARY_BOND
version: "2.0.0"
updated: "2025-01"
---

# React Native Navigation Skill

> Learn production-ready navigation patterns using React Navigation v6+ and Expo Router.

## Prerequisites

- React Native basics (components, styling)
- TypeScript fundamentals
- Understanding of React context

## Learning Objectives

After completing this skill, you will be able to:
- [ ] Set up React Navigation with TypeScript
- [ ] Implement Stack, Tab, and Drawer navigators
- [ ] Configure deep linking and universal links
- [ ] Handle authentication flows
- [ ] Pass params between screens type-safely

---

## Topics Covered

### 1. Installation
```bash
npm install @react-navigation/native @react-navigation/native-stack
npm install react-native-screens react-native-safe-area-context

# For tabs
npm install @react-navigation/bottom-tabs

# For drawers
npm install @react-navigation/drawer react-native-gesture-handler react-native-reanimated
```

### 2. Stack Navigator
```tsx
import { createNativeStackNavigator } from '@react-navigation/native-stack';

type RootStackParamList = {
  Home: undefined;
  Details: { id: string };
};

const Stack = createNativeStackNavigator<RootStackParamList>();

function RootNavigator() {
  return (
    <Stack.Navigator>
      <Stack.Screen name="Home" component={HomeScreen} />
      <Stack.Screen name="Details" component={DetailsScreen} />
    </Stack.Navigator>
  );
}
```

### 3. Tab Navigator
```tsx
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';

const Tab = createBottomTabNavigator();

function MainTabs() {
  return (
    <Tab.Navigator>
      <Tab.Screen name="Home" component={HomeScreen} />
      <Tab.Screen name="Profile" component={ProfileScreen} />
    </Tab.Navigator>
  );
}
```

### 4. Deep Linking
```tsx
const linking = {
  prefixes: ['myapp://', 'https://myapp.com'],
  config: {
    screens: {
      Home: 'home',
      Details: 'details/:id',
    },
  },
};

<NavigationContainer linking={linking}>
  {/* navigators */}
</NavigationContainer>
```

### 5. Type-Safe Navigation
```tsx
import { useNavigation } from '@react-navigation/native';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';

type NavigationProp = NativeStackNavigationProp<RootStackParamList>;

function HomeScreen() {
  const navigation = useNavigation<NavigationProp>();

  return (
    <Button
      title="Go to Details"
      onPress={() => navigation.navigate('Details', { id: '123' })}
    />
  );
}
```

---

## Quick Start Example

```tsx
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

type RootStackParamList = {
  Home: undefined;
  Details: { id: string; title: string };
};

const Stack = createNativeStackNavigator<RootStackParamList>();

export default function App() {
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

---

## Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| "Navigator not found" | Missing NavigationContainer | Wrap app in NavigationContainer |
| Params undefined | Type mismatch | Check ParamList types |
| Deep link not working | Config mismatch | Verify linking paths |

---

## Validation Checklist

- [ ] Navigation works on both platforms
- [ ] Deep links open correct screens
- [ ] TypeScript catches param errors
- [ ] Auth flow protects routes

---

## Usage

```
Skill("react-native-navigation")
```

**Bonded Agent**: `02-react-native-navigation`
