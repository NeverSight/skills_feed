---
name: react-native-expert
description: Expert guidance for building mobile applications with React Native and Expo. Use when the user asks to create, modify, debug, or architect mobile apps, implement native features (camera, notifications, storage, navigation), set up React Native projects, work with Expo or bare React Native workflows, integrate with device APIs, handle app state management, or optimize mobile performance. Triggers on mobile app development, React Native, Expo, iOS/Android cross-platform development.
---

# React Native Mobile Development Expert

Expert guidance for building production-quality mobile applications with React Native.

## Project Initialization

### Expo (Recommended for most projects)

```bash
npx create-expo-app@latest my-app --template blank-typescript
cd my-app
npx expo start
```

### Bare React Native (When native code access required)

```bash
npx @react-native-community/cli init MyApp --template react-native-template-typescript
cd MyApp
npx react-native run-ios  # or run-android
```

**Choose Expo when:** rapid prototyping, standard features, OTA updates needed, limited native customization.

**Choose Bare when:** custom native modules required, existing native codebase integration, specific native library needs.

## Project Structure

```
src/
├── app/                    # Expo Router screens (if using Expo Router)
├── components/
│   ├── ui/                 # Reusable UI primitives
│   └── features/           # Feature-specific components
├── hooks/                  # Custom hooks
├── services/               # API clients, external services
├── stores/                 # State management (Zustand/Redux)
├── utils/                  # Helper functions
├── types/                  # TypeScript definitions
└── constants/              # App-wide constants, theme
```

## Navigation

### Expo Router (File-based, recommended for Expo)

```typescript
// app/_layout.tsx
import { Stack } from 'expo-router';

export default function RootLayout() {
  return (
    <Stack>
      <Stack.Screen name="index" options={{ title: 'Home' }} />
      <Stack.Screen name="details/[id]" options={{ title: 'Details' }} />
    </Stack>
  );
}

// app/details/[id].tsx
import { useLocalSearchParams } from 'expo-router';

export default function Details() {
  const { id } = useLocalSearchParams<{ id: string }>();
  return <Text>Item {id}</Text>;
}
```

### React Navigation (Traditional approach)

```typescript
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

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

## State Management

### Zustand (Recommended for simplicity)

```typescript
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface AuthStore {
  user: User | null;
  token: string | null;
  setAuth: (user: User, token: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      setAuth: (user, token) => set({ user, token }),
      logout: () => set({ user: null, token: null }),
    }),
    {
      name: 'auth-storage',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);
```

### TanStack Query (Server state)

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

export function useTodos() {
  return useQuery({
    queryKey: ['todos'],
    queryFn: () => api.getTodos(),
  });
}

export function useCreateTodo() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.createTodo,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['todos'] }),
  });
}
```

## Styling

### NativeWind (Tailwind for React Native)

```bash
npx expo install nativewind tailwindcss
```

```typescript
// tailwind.config.js
module.exports = {
  content: ['./app/**/*.{js,tsx}', './src/**/*.{js,tsx}'],
  presets: [require('nativewind/preset')],
  theme: { extend: {} },
};

// Component usage
import { View, Text } from 'react-native';

export function Card({ title }: { title: string }) {
  return (
    <View className="bg-white rounded-xl p-4 shadow-md">
      <Text className="text-lg font-bold text-gray-900">{title}</Text>
    </View>
  );
}
```

### StyleSheet (Built-in)

```typescript
import { StyleSheet, View, Text } from 'react-native';

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3, // Android shadow
  },
});
```

## Common Native Features

### Camera

```typescript
import { CameraView, useCameraPermissions } from 'expo-camera';

export function CameraScreen() {
  const [permission, requestPermission] = useCameraPermissions();
  const cameraRef = useRef<CameraView>(null);

  const takePicture = async () => {
    const photo = await cameraRef.current?.takePictureAsync();
    console.log(photo?.uri);
  };

  if (!permission?.granted) {
    return <Button title="Grant Permission" onPress={requestPermission} />;
  }

  return <CameraView ref={cameraRef} style={{ flex: 1 }} facing="back" />;
}
```

### Push Notifications (Expo)

```typescript
import * as Notifications from 'expo-notifications';
import * as Device from 'expo-device';

Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: true,
  }),
});

export async function registerForPushNotifications() {
  if (!Device.isDevice) return null;
  
  const { status } = await Notifications.requestPermissionsAsync();
  if (status !== 'granted') return null;
  
  const token = await Notifications.getExpoPushTokenAsync({
    projectId: 'your-project-id',
  });
  return token.data;
}
```

### Secure Storage

```typescript
import * as SecureStore from 'expo-secure-store';

export const secureStorage = {
  async setItem(key: string, value: string) {
    await SecureStore.setItemAsync(key, value);
  },
  async getItem(key: string) {
    return SecureStore.getItemAsync(key);
  },
  async removeItem(key: string) {
    await SecureStore.deleteItemAsync(key);
  },
};
```

### Biometric Authentication

```typescript
import * as LocalAuthentication from 'expo-local-authentication';

export async function authenticateWithBiometrics() {
  const hasHardware = await LocalAuthentication.hasHardwareAsync();
  const isEnrolled = await LocalAuthentication.isEnrolledAsync();
  
  if (!hasHardware || !isEnrolled) return false;
  
  const result = await LocalAuthentication.authenticateAsync({
    promptMessage: 'Authenticate to continue',
    fallbackLabel: 'Use passcode',
  });
  
  return result.success;
}
```

## Performance Optimization

### List Rendering

```typescript
import { FlashList } from '@shopify/flash-list';

// Prefer FlashList over FlatList for large lists
<FlashList
  data={items}
  renderItem={({ item }) => <ItemCard item={item} />}
  estimatedItemSize={80}
  keyExtractor={(item) => item.id}
/>
```

### Memoization

```typescript
// Memoize expensive components
const MemoizedItem = memo(function Item({ data }: Props) {
  return <View>...</View>;
});

// Memoize callbacks passed to children
const handlePress = useCallback(() => {
  doSomething(id);
}, [id]);
```

### Image Optimization

```typescript
import { Image } from 'expo-image';

// Use expo-image for caching and performance
<Image
  source={{ uri: imageUrl }}
  style={{ width: 200, height: 200 }}
  contentFit="cover"
  placeholder={blurhash}
  transition={200}
/>
```

## Forms

### React Hook Form + Zod

```typescript
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const schema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Min 8 characters'),
});

type FormData = z.infer<typeof schema>;

export function LoginForm() {
  const { control, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  const onSubmit = (data: FormData) => {
    console.log(data);
  };

  return (
    <View>
      <Controller
        control={control}
        name="email"
        render={({ field: { onChange, onBlur, value } }) => (
          <TextInput
            placeholder="Email"
            onBlur={onBlur}
            onChangeText={onChange}
            value={value}
            keyboardType="email-address"
            autoCapitalize="none"
          />
        )}
      />
      {errors.email && <Text className="text-red-500">{errors.email.message}</Text>}
      
      <Controller
        control={control}
        name="password"
        render={({ field: { onChange, onBlur, value } }) => (
          <TextInput
            placeholder="Password"
            onBlur={onBlur}
            onChangeText={onChange}
            value={value}
            secureTextEntry
          />
        )}
      />
      {errors.password && <Text className="text-red-500">{errors.password.message}</Text>}
      
      <Button title="Login" onPress={handleSubmit(onSubmit)} />
    </View>
  );
}
```

## API Integration

### Axios with Interceptors

```typescript
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';

export const api = axios.create({
  baseURL: 'https://api.example.com',
  timeout: 10000,
});

api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout();
    }
    return Promise.reject(error);
  }
);
```

## Testing

### Jest + React Native Testing Library

```typescript
import { render, screen, fireEvent } from '@testing-library/react-native';
import { LoginForm } from './LoginForm';

describe('LoginForm', () => {
  it('shows validation errors for invalid input', async () => {
    render(<LoginForm />);
    
    fireEvent.press(screen.getByText('Login'));
    
    expect(await screen.findByText('Invalid email')).toBeTruthy();
  });

  it('submits with valid data', async () => {
    const onSubmit = jest.fn();
    render(<LoginForm onSubmit={onSubmit} />);
    
    fireEvent.changeText(screen.getByPlaceholderText('Email'), 'test@example.com');
    fireEvent.changeText(screen.getByPlaceholderText('Password'), 'password123');
    fireEvent.press(screen.getByText('Login'));
    
    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password123',
      });
    });
  });
});
```

### Detox (E2E Testing)

```typescript
// e2e/login.test.ts
describe('Login Flow', () => {
  beforeAll(async () => {
    await device.launchApp();
  });

  it('should login successfully', async () => {
    await element(by.id('email-input')).typeText('user@example.com');
    await element(by.id('password-input')).typeText('password123');
    await element(by.id('login-button')).tap();
    await expect(element(by.id('home-screen'))).toBeVisible();
  });
});
```

## Building & Deployment

### Expo EAS Build

```bash
# Install EAS CLI
npm install -g eas-cli

# Configure project
eas build:configure

# Build for stores
eas build --platform ios --profile production
eas build --platform android --profile production

# Submit to stores
eas submit --platform ios
eas submit --platform android
```

### eas.json Configuration

```json
{
  "cli": { "version": ">= 5.0.0" },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal"
    },
    "preview": {
      "distribution": "internal",
      "ios": { "simulator": true }
    },
    "production": {
      "ios": { "resourceClass": "m1-medium" },
      "android": { "buildType": "apk" }
    }
  },
  "submit": {
    "production": {
      "ios": { "appleId": "your@email.com", "ascAppId": "123456789" },
      "android": { "serviceAccountKeyPath": "./google-services.json" }
    }
  }
}
```

### OTA Updates (Expo)

```typescript
import * as Updates from 'expo-updates';

export async function checkForUpdates() {
  if (__DEV__) return;
  
  const update = await Updates.checkForUpdateAsync();
  if (update.isAvailable) {
    await Updates.fetchUpdateAsync();
    await Updates.reloadAsync();
  }
}
```

## Environment Configuration

### app.config.ts (Expo)

```typescript
export default ({ config }: ConfigContext): ExpoConfig => ({
  ...config,
  name: process.env.APP_ENV === 'production' ? 'MyApp' : 'MyApp (Dev)',
  slug: 'my-app',
  extra: {
    apiUrl: process.env.API_URL,
    eas: { projectId: 'your-project-id' },
  },
});
```

### Accessing Environment Variables

```typescript
import Constants from 'expo-constants';

const API_URL = Constants.expoConfig?.extra?.apiUrl;
```

## Error Handling & Monitoring

### Error Boundaries

```typescript
import { ErrorBoundary } from 'react-error-boundary';

function ErrorFallback({ error, resetErrorBoundary }) {
  return (
    <View className="flex-1 justify-center items-center p-4">
      <Text className="text-lg font-bold">Something went wrong</Text>
      <Text className="text-gray-600 mb-4">{error.message}</Text>
      <Button title="Try Again" onPress={resetErrorBoundary} />
    </View>
  );
}

export function App() {
  return (
    <ErrorBoundary FallbackComponent={ErrorFallback}>
      <MainApp />
    </ErrorBoundary>
  );
}
```

### Sentry Integration

```typescript
import * as Sentry from '@sentry/react-native';

Sentry.init({
  dsn: 'your-dsn',
  tracesSampleRate: 1.0,
  environment: __DEV__ ? 'development' : 'production',
});

// Wrap root component
export default Sentry.wrap(App);
```

## Essential Libraries

| Category | Library | Purpose |
|----------|---------|---------|
| Navigation | `expo-router` or `@react-navigation/native` | Screen navigation |
| State | `zustand`, `@tanstack/react-query` | Client & server state |
| Styling | `nativewind` | Tailwind CSS for RN |
| Forms | `react-hook-form` + `zod` | Form handling & validation |
| Lists | `@shopify/flash-list` | High-performance lists |
| Images | `expo-image` | Cached, optimized images |
| Icons | `@expo/vector-icons` | Icon sets |
| Storage | `@react-native-async-storage/async-storage` | Persistent storage |
| Secure Storage | `expo-secure-store` | Encrypted storage |
| HTTP | `axios` | API requests |
| Animations | `react-native-reanimated` | Smooth animations |
| Gestures | `react-native-gesture-handler` | Touch handling |

## Common Patterns

### Safe Area Handling

```typescript
import { SafeAreaProvider, SafeAreaView } from 'react-native-safe-area-context';

export function App() {
  return (
    <SafeAreaProvider>
      <SafeAreaView style={{ flex: 1 }} edges={['top', 'bottom']}>
        <Content />
      </SafeAreaView>
    </SafeAreaProvider>
  );
}
```

### Keyboard Avoiding

```typescript
import { KeyboardAvoidingView, Platform } from 'react-native';

<KeyboardAvoidingView
  behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
  style={{ flex: 1 }}
>
  <FormContent />
</KeyboardAvoidingView>
```

### Pull to Refresh

```typescript
const [refreshing, setRefreshing] = useState(false);

const onRefresh = useCallback(async () => {
  setRefreshing(true);
  await fetchData();
  setRefreshing(false);
}, []);

<FlatList
  refreshControl={
    <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
  }
  ...
/>
```

## Debugging

- **Expo DevTools**: Press `j` in terminal for debugger
- **React DevTools**: `npx react-devtools`
- **Flipper**: Native debugging (bare RN)
- **Reactotron**: State inspection, API monitoring

```bash
# Shake device or Cmd+D (iOS) / Cmd+M (Android) for dev menu
# Enable "Debug JS Remotely" for breakpoints
```

## Best Practices

1. **TypeScript everywhere** - Define types for navigation, API responses, store state
2. **Absolute imports** - Configure `tsconfig.json` paths with `@/` prefix
3. **Component composition** - Small, focused components over large monoliths
4. **Platform-specific code** - Use `.ios.tsx` / `.android.tsx` when needed
5. **Accessibility** - Add `accessibilityLabel`, `accessibilityRole` props
6. **Offline support** - Cache API responses, handle network errors gracefully
7. **Deep linking** - Configure URL schemes for app links
8. **App icons & splash** - Use `expo-splash-screen` for smooth loading
