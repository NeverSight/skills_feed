---
name: mobile
description: Use this skill when building mobile applications, React Native apps, Expo projects, iOS/Android development, or cross-platform mobile features. Activates on mentions of React Native, Expo, mobile app, iOS, Android, Swift, Kotlin, Flutter, app store, push notifications, deep linking, mobile navigation, or native modules.
---

# Mobile Development

Build native-quality mobile apps with React Native and Expo.

## Quick Reference

### Expo SDK 53+ (2026 Standard)

**New Architecture is DEFAULT** - No opt-in required.

```bash
# Create new project
npx create-expo-app@latest my-app
cd my-app
npx expo start
```

**Key Changes:**

- Hermes engine default (JSC deprecated)
- Fabric renderer + Bridgeless mode
- All `expo-*` packages support New Architecture
- `expo-video` replaces `expo-av` for video
- `expo-audio` replaces `expo-av` for audio

### Project Structure

```
app/
├── (tabs)/           # Tab navigation group
│   ├── index.tsx     # Home tab
│   ├── profile.tsx   # Profile tab
│   └── _layout.tsx   # Tab layout
├── [id].tsx          # Dynamic route
├── _layout.tsx       # Root layout
└── +not-found.tsx    # 404 page
```

### Navigation (Expo Router)

```tsx
// app/_layout.tsx
import { Stack } from "expo-router";

export default function Layout() {
  return (
    <Stack>
      <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
      <Stack.Screen name="modal" options={{ presentation: "modal" }} />
    </Stack>
  );
}
```

**Deep Linking**

```tsx
// Navigate programmatically
import { router } from "expo-router";
router.push("/profile/123");
router.replace("/home");
router.back();
```

### Native Modules (New Architecture)

**Turbo Modules** - Synchronous, type-safe native access:

```tsx
// specs/NativeCalculator.ts
import type { TurboModule } from "react-native";
import { TurboModuleRegistry } from "react-native";

export interface Spec extends TurboModule {
  multiply(a: number, b: number): number;
}

export default TurboModuleRegistry.getEnforcing<Spec>("Calculator");
```

### Styling

**NativeWind (Tailwind for RN)**

```tsx
import { View, Text } from "react-native";

export function Card() {
  return (
    <View className="bg-white rounded-xl p-4 shadow-lg">
      <Text className="text-lg font-bold text-gray-900">Title</Text>
    </View>
  );
}
```

### State Management

Same as web - TanStack Query for server state, Zustand for client:

```tsx
import { useQuery } from "@tanstack/react-query";

function ProfileScreen() {
  const { data: user } = useQuery({
    queryKey: ["user"],
    queryFn: fetchUser,
  });
  return <UserProfile user={user} />;
}
```

### OTA Updates

```tsx
// app.config.js
export default {
  expo: {
    updates: {
      url: "https://u.expo.dev/your-project-id",
      fallbackToCacheTimeout: 0,
    },
    runtimeVersion: {
      policy: "appVersion",
    },
  },
};
```

### Push Notifications

```tsx
import * as Notifications from "expo-notifications";

// Request permissions
const { status } = await Notifications.requestPermissionsAsync();

// Get push token
const token = await Notifications.getExpoPushTokenAsync({
  projectId: "your-project-id",
});

// Schedule local notification
await Notifications.scheduleNotificationAsync({
  content: { title: "Reminder", body: "Check the app!" },
  trigger: { seconds: 60 },
});
```

### Performance Tips

1. **Use FlashList** over FlatList for long lists
2. **Avoid inline styles** - Use StyleSheet.create or NativeWind
3. **Optimize images** - Use expo-image with caching
4. **Profile with Flipper** or React DevTools

### Build & Deploy

```bash
# Development build
npx expo run:ios
npx expo run:android

# Production build (EAS)
eas build --platform all --profile production

# Submit to stores
eas submit --platform ios
eas submit --platform android
```

## Agents

- **mobile-app-builder** - Full mobile development expertise

## Deep Dives

- [references/expo-sdk-53.md](references/expo-sdk-53.md)
- [references/new-architecture.md](references/new-architecture.md)
- [references/native-modules.md](references/native-modules.md)
- [references/app-store-submission.md](references/app-store-submission.md)

## Examples

- [examples/expo-starter/](examples/expo-starter/)
- [examples/push-notifications/](examples/push-notifications/)
- [examples/native-module/](examples/native-module/)
