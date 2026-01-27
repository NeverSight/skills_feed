---
name: mobile-app-developer
description: Expert in cross-platform mobile development (React Native/Flutter), bridging native performance with shared business logic.
---

# Mobile App Developer

## Purpose

Provides cross-platform mobile development expertise specializing in React Native and Flutter. Builds high-performance mobile applications with offline-first architectures, native module integration, and optimized delivery pipelines for iOS and Android.

## When to Use

- Building new mobile apps targeting both iOS and Android
- Migrating web applications to mobile (React Native)
- Implementing complex native features (Bluetooth, Biometrics, AR) in cross-platform apps
- Optimizing app performance (startup time, frame drops, bundle size)
- Designing offline-first data synchronization layers
- Setting up mobile CI/CD pipelines (Fastlane, EAS, Codemagic)

---
---

## 2. Decision Framework

### Framework Selection (2026 Standards)

```
Which framework fits the project?
│
├─ **React Native (0.76+)**
│  ├─ Team knows React? → **Yes** (Fastest ramp-up)
│  ├─ Need OTA Updates? → **Yes** (Expo Updates / CodePush)
│  ├─ Heavy Native UI? → **Maybe** (New Architecture makes this easier, but complex)
│  └─ Ecosystem? → **Massive** (npm, vast library support)
│
├─ **Flutter (3.24+)**
│  ├─ Pixel Perfection needed? → **Yes** (Skia/Impeller rendering guarantees consistency)
│  ├─ Heavy Animation? → **Yes** (60/120fps default)
│  ├─ Desktop support needed? → **Yes** (First-class Windows/macOS/Linux)
│  └─ Dart knowledge? → **Required** (Learning curve for JS devs)
│
└─ **Expo (Managed RN)**
   ├─ Rapid MVP? → **Yes** (Zero config, EAS Build)
   ├─ Custom Native Code? → **Yes** (Config Plugins handle 99% of cases)
   └─ Ejecting? → **No** (Prebuild allows native code without ejecting)
```

### State Management & Architecture

| Architecture | React Native | Flutter | Best For |
|--------------|--------------|---------|----------|
| **MVVM** | MobX / Legend-State | Provider / Riverpod | Reactive UI, clean separation |
| **Redux-style** | Redux Toolkit / Zustand | BLoC / Cubit | Complex enterprise apps, strict flow |
| **Atomic** | Recoil / Jotai | Riverpod | Fine-grained updates, high performance |
| **Offline-First** | WatermelonDB / Realm | Hive / Isar / Drift | Apps needing robust sync |

### Performance Constraints

| Metric | Target | Optimization Strategy |
|--------|--------|-----------------------|
| **Cold Start** | < 1.5s | Hermes (RN), Lazy Loading, Deferred initialization |
| **Frame Rate** | 60fps (min) / 120fps (target) | Memoization, release thread (JS) vs UI thread, Impeller (Flutter) |
| **Bundle Size** | < 30MB (Universal) | ProGuard/R8, Split APKs, Asset Optimization |
| **Memory** | < 200MB (Avg) | Image caching, List recycling (FlashList) |

**Red Flags → Escalate to `mobile-developer` (Native):**
- Requirements for kernel-level driver interaction
- App is a "wrapper" around a single heavy 3D view (Unity integration might be better)
- Strict requirement for < 10MB app size
- Dependency on private/undocumented iOS APIs

---
---

## 3. Core Workflows

### Workflow 1: React Native New Architecture Setup

**Goal:** Initialize a high-performance React Native app with Fabric & TurboModules.

**Steps:**

1.  **Initialization (Expo)**
    ```bash
    npx create-expo-app@latest my-app -t default
    cd my-app
    npx expo install expo-router react-native-reanimated
    ```

2.  **Configuration (app.json)**
    ```json
    {
      "expo": {
        "newArchEnabled": true,
        "plugins": [
          "expo-router",
          "expo-font",
          ["expo-build-properties", {
            "ios": { "newArchEnabled": true },
            "android": { "newArchEnabled": true }
          }]
        ]
      }
    }
    ```

3.  **Directory Structure (File-based Routing)**
    ```
    /app
      /_layout.tsx      # Root layout (Provider setup)
      /index.tsx        # Home screen
      /(tabs)/          # Tab navigation group
        /_layout.tsx    # Tab configuration
        /home.tsx
        /settings.tsx
      /product/[id].tsx # Dynamic route
    /components         # UI Components
    /services           # API & Logic
    /store              # State Management
    ```

4.  **Navigation Implementation**
    ```tsx
    // app/_layout.tsx
    import { Stack } from 'expo-router';
    import { QueryClientProvider } from '@tanstack/react-query';

    export default function RootLayout() {
      return (
        <QueryClientProvider client={queryClient}>
          <Stack screenOptions={{ headerShown: false }}>
            <Stack.Screen name="(tabs)" />
            <Stack.Screen name="modal" options={{ presentation: 'modal' }} />
          </Stack>
        </QueryClientProvider>
      );
    }
    ```

---
---

### Workflow 3: Performance Optimization (FlashList)

**Goal:** Render 10,000+ list items at 60fps.

**Steps:**

1.  **Replace FlatList**
    ```tsx
    import { FlashList } from "@shopify/flash-list";

    const MyList = ({ data }) => {
      return (
        <FlashList
          data={data}
          renderItem={({ item }) => <ListItem item={item} />}
          estimatedItemSize={100} // Critical for performance
          keyExtractor={item => item.id}
          onEndReached={loadMore}
          onEndReachedThreshold={0.5}
        />
      );
    };
    ```

2.  **Memoize List Items**
    ```tsx
    const ListItem = React.memo(({ item }) => {
      return (
        <View style={styles.item}>
          <Text>{item.title}</Text>
        </View>
      );
    }, (prev, next) => prev.item.id === next.item.id);
    ```

3.  **Image Optimization**
    -   Use `expo-image` (uses SDWebImage/Glide native caching).
    -   Enable `cachePolicy="memory-disk"`.
    -   Use `transition={200}` for smooth loading.

---
---

## 4. Patterns & Templates

### Pattern 1: Native Module (Expo Config Plugin)

**Use case:** Adding native code without ejecting.

```javascript
// plugins/withCustomNative.js
const { withAndroidManifest } = require('@expo/config-plugins');

const withCustomNative = (config) => {
  return withAndroidManifest(config, async (config) => {
    const androidManifest = config.modResults;
    
    // Add permission
    androidManifest.manifest['uses-permission'].push({
      $: { 'android:name': 'android.permission.BLUETOOTH' }
    });

    return config;
  });
};

module.exports = withCustomNative;
```

### Pattern 2: Biometric Authentication Hook

**Use case:** Secure login with FaceID/TouchID.

```tsx
import * as LocalAuthentication from 'expo-local-authentication';

export function useBiometrics() {
  const authenticate = async () => {
    const hasHardware = await LocalAuthentication.hasHardwareAsync();
    if (!hasHardware) return false;

    const isEnrolled = await LocalAuthentication.isEnrolledAsync();
    if (!isEnrolled) return false;

    const result = await LocalAuthentication.authenticateAsync({
      promptMessage: 'Login with FaceID',
      fallbackLabel: 'Use Passcode',
    });

    return result.success;
  };

  return { authenticate };
}
```

### Pattern 3: The "Smart" API Layer

**Use case:** Handling auth tokens, retries, and network errors gracefully.

```typescript
import axios from 'axios';
import * as SecureStore from 'expo-secure-store';

const api = axios.create({ baseURL: 'https://api.example.com' });

api.interceptors.request.use(async (config) => {
  const token = await SecureStore.getItemAsync('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Trigger token refresh logic
      // If refresh fails, redirect to login
    }
    return Promise.reject(error);
  }
);
```

---
---

## 6. Integration Patterns

### **backend-developer:**
-   **Handoff**: Backend provides OpenAPI (Swagger) spec → Mobile dev generates TypeScript clients (`openapi-generator`).
-   **Collaboration**: Designing "Mobile-First" APIs (pagination, partial responses, minimal payload).
-   **Tools**: Postman, GraphQL.

### **ui-designer:**
-   **Handoff**: Designer provides Figma with Auto-Layout → Dev maps to Flexbox (`flexDirection`, `justifyContent`).
-   **Collaboration**: Exporting SVGs vs PNGs (use SVGs/VectorDrawable).
-   **Tools**: Zeplin, Figma Dev Mode.

### **qa-expert:**
-   **Handoff**: Dev provides test builds (TestFlight/Firebase) → QA runs regression.
-   **Collaboration**: Providing test IDs for E2E automation (`testID="login_btn"`).
-   **Tools**: Appium, Detox, Maestro.

---
