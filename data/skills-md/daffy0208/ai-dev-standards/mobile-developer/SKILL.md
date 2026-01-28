---
name: mobile-developer
description: Expert in React Native, Expo, and cross-platform mobile development
version: 1.0.0
tags: [mobile, react-native, expo, ios, android, cross-platform]
---

# Mobile Developer Skill

I help you build cross-platform mobile apps with React Native and Expo.

## What I Do

**App Development:**

- React Native / Expo apps (iOS + Android)
- Navigation and routing
- State management
- API integration

**Native Features:**

- Camera, location, notifications
- Biometric authentication
- File system access
- Device sensors

**Performance:**

- Optimize bundle size
- Lazy loading
- Image optimization
- Memory management

**Distribution:**

- App Store / Google Play submission
- Over-the-air (OTA) updates
- Beta testing (TestFlight, internal testing)

## Quick Start: Expo App

### Create New App

```bash
# Create Expo app
npx create-expo-app my-app --template blank-typescript

cd my-app

# Install dependencies
npx expo install react-native-screens react-native-safe-area-context
npx expo install expo-router

# Start development
npx expo start
```

### Project Structure

```
my-app/
├── app/
│   ├── (tabs)/
│   │   ├── index.tsx          # Home tab
│   │   ├── profile.tsx        # Profile tab
│   │   └── _layout.tsx        # Tab layout
│   ├── users/
│   │   └── [id].tsx          # Dynamic route
│   ├── _layout.tsx           # Root layout
│   └── +not-found.tsx        # 404 page
├── components/
│   ├── Button.tsx
│   ├── Card.tsx
│   └── Loading.tsx
├── hooks/
│   └── useAuth.ts
├── app.json
└── package.json
```

---

## Navigation with Expo Router

### Tab Navigation

```typescript
// app/(tabs)/_layout.tsx
import { Tabs } from 'expo-router'
import { Ionicons } from '@expo/vector-icons'

export default function TabLayout() {
  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: '#007AFF',
        headerShown: false
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: 'Home',
          tabBarIcon: ({ color, size }) => (
            <Ionicons name="home" size={size} color={color} />
          )
        }}
      />
      <Tabs.Screen
        name="profile"
        options={{
          title: 'Profile',
          tabBarIcon: ({ color, size }) => (
            <Ionicons name="person" size={size} color={color} />
          )
        }}
      />
    </Tabs>
  )
}
```

### Stack Navigation

```typescript
// app/users/[id].tsx
import { useLocalSearchParams } from 'expo-router'
import { View, Text } from 'react-native'

export default function UserDetail() {
  const { id } = useLocalSearchParams()

  return (
    <View>
      <Text>User ID: {id}</Text>
    </View>
  )
}
```

---

## UI Components

### Custom Button

```typescript
// components/Button.tsx
import { TouchableOpacity, Text, StyleSheet, ActivityIndicator } from 'react-native'

interface ButtonProps {
  title: string
  onPress: () => void
  variant?: 'primary' | 'secondary'
  loading?: boolean
  disabled?: boolean
}

export function Button({
  title,
  onPress,
  variant = 'primary',
  loading = false,
  disabled = false
}: ButtonProps) {
  return (
    <TouchableOpacity
      style={[
        styles.button,
        variant === 'primary' ? styles.primary : styles.secondary,
        disabled && styles.disabled
      ]}
      onPress={onPress}
      disabled={disabled || loading}
      activeOpacity={0.7}
    >
      {loading ? (
        <ActivityIndicator color="#fff" />
      ) : (
        <Text style={styles.text}>{title}</Text>
      )}
    </TouchableOpacity>
  )
}

const styles = StyleSheet.create({
  button: {
    padding: 16,
    borderRadius: 8,
    alignItems: 'center',
    justifyContent: 'center'
  },
  primary: {
    backgroundColor: '#007AFF'
  },
  secondary: {
    backgroundColor: '#8E8E93'
  },
  disabled: {
    opacity: 0.5
  },
  text: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600'
  }
})
```

### Card Component

```typescript
// components/Card.tsx
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native'
import { ReactNode } from 'react'

interface CardProps {
  title?: string
  children: ReactNode
  onPress?: () => void
}

export function Card({ title, children, onPress }: CardProps) {
  const Container = onPress ? TouchableOpacity : View

  return (
    <Container
      style={styles.card}
      onPress={onPress}
      activeOpacity={onPress ? 0.7 : 1}
    >
      {title && <Text style={styles.title}>{title}</Text>}
      {children}
    </Container>
  )
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3
  },
  title: {
    fontSize: 18,
    fontWeight: '600',
    marginBottom: 12
  }
})
```

---

## Data Fetching

### Custom Hook

```typescript
// hooks/useQuery.ts
import { useState, useEffect } from 'react'

interface UseQueryResult<T> {
  data: T | null
  loading: boolean
  error: Error | null
  refetch: () => void
}

export function useQuery<T>(url: string): UseQueryResult<T> {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)

  const fetchData = async () => {
    try {
      setLoading(true)
      const response = await fetch(url)

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const json = await response.json()
      setData(json)
      setError(null)
    } catch (e) {
      setError(e as Error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
  }, [url])

  return { data, loading, error, refetch: fetchData }
}
```

### Usage

```typescript
// app/(tabs)/index.tsx
import { View, Text, FlatList, RefreshControl } from 'react-native'
import { useQuery } from '@/hooks/useQuery'
import { Card } from '@/components/Card'

interface Post {
  id: string
  title: string
  content: string
}

export default function HomeScreen() {
  const { data, loading, error, refetch } = useQuery<Post[]>(
    'https://api.example.com/posts'
  )

  if (error) {
    return (
      <View>
        <Text>Error: {error.message}</Text>
      </View>
    )
  }

  return (
    <FlatList
      data={data || []}
      keyExtractor={(item) => item.id}
      renderItem={({ item }) => (
        <Card title={item.title}>
          <Text>{item.content}</Text>
        </Card>
      )}
      refreshControl={
        <RefreshControl refreshing={loading} onRefresh={refetch} />
      }
    />
  )
}
```

---

## Native Features

### Camera

```typescript
// app/camera.tsx
import { Camera, CameraType } from 'expo-camera'
import { useState } from 'react'
import { Button, View, StyleSheet } from 'react-native'

export default function CameraScreen() {
  const [type, setType] = useState(CameraType.back)
  const [permission, requestPermission] = Camera.useCameraPermissions()

  if (!permission) {
    return <View />
  }

  if (!permission.granted) {
    return (
      <View style={styles.container}>
        <Button onPress={requestPermission} title="Grant Camera Permission" />
      </View>
    )
  }

  return (
    <View style={styles.container}>
      <Camera style={styles.camera} type={type}>
        <View style={styles.buttonContainer}>
          <Button
            onPress={() => {
              setType(current =>
                current === CameraType.back
                  ? CameraType.front
                  : CameraType.back
              )
            }}
            title="Flip Camera"
          />
        </View>
      </Camera>
    </View>
  )
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  camera: { flex: 1 },
  buttonContainer: {
    flex: 1,
    backgroundColor: 'transparent',
    justifyContent: 'flex-end',
    padding: 20
  }
})
```

### Push Notifications

```typescript
// hooks/useNotifications.ts
import { useState, useEffect, useRef } from 'react'
import * as Notifications from 'expo-notifications'
import * as Device from 'expo-device'
import { Platform } from 'react-native'

Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: false,
    shouldSetBadge: false
  })
})

export function useNotifications() {
  const [expoPushToken, setExpoPushToken] = useState('')
  const notificationListener = useRef<Notifications.Subscription>()
  const responseListener = useRef<Notifications.Subscription>()

  useEffect(() => {
    registerForPushNotificationsAsync().then(token => setExpoPushToken(token || ''))

    notificationListener.current = Notifications.addNotificationReceivedListener(notification => {
      console.log('Notification received:', notification)
    })

    responseListener.current = Notifications.addNotificationResponseReceivedListener(response => {
      console.log('Notification clicked:', response)
    })

    return () => {
      Notifications.removeNotificationSubscription(notificationListener.current!)
      Notifications.removeNotificationSubscription(responseListener.current!)
    }
  }, [])

  return { expoPushToken }
}

async function registerForPushNotificationsAsync() {
  let token

  if (Platform.OS === 'android') {
    await Notifications.setNotificationChannelAsync('default', {
      name: 'default',
      importance: Notifications.AndroidImportance.MAX,
      vibrationPattern: [0, 250, 250, 250],
      lightColor: '#FF231F7C'
    })
  }

  if (Device.isDevice) {
    const { status: existingStatus } = await Notifications.getPermissionsAsync()
    let finalStatus = existingStatus

    if (existingStatus !== 'granted') {
      const { status } = await Notifications.requestPermissionsAsync()
      finalStatus = status
    }

    if (finalStatus !== 'granted') {
      alert('Failed to get push token for push notification!')
      return
    }

    token = (await Notifications.getExpoPushTokenAsync()).data
  } else {
    alert('Must use physical device for Push Notifications')
  }

  return token
}
```

### Location

```typescript
// hooks/useLocation.ts
import { useState, useEffect } from 'react'
import * as Location from 'expo-location'

export function useLocation() {
  const [location, setLocation] = useState<Location.LocationObject | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    ;(async () => {
      const { status } = await Location.requestForegroundPermissionsAsync()

      if (status !== 'granted') {
        setError('Permission to access location was denied')
        return
      }

      const location = await Location.getCurrentPositionAsync({})
      setLocation(location)
    })()
  }, [])

  return { location, error }
}
```

---

## State Management

### Zustand (Recommended)

```typescript
// store/auth.ts
import { create } from 'zustand'

interface User {
  id: string
  email: string
  name: string
}

interface AuthStore {
  user: User | null
  token: string | null
  login: (email: string, password: string) => Promise<void>
  logout: () => void
}

export const useAuthStore = create<AuthStore>(set => ({
  user: null,
  token: null,

  login: async (email, password) => {
    const response = await fetch('https://api.example.com/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    })

    const { user, token } = await response.json()

    set({ user, token })
  },

  logout: () => {
    set({ user: null, token: null })
  }
}))
```

**Usage:**

```typescript
// app/login.tsx
import { useState } from 'react'
import { View, TextInput } from 'react-native'
import { useAuthStore } from '@/store/auth'
import { Button } from '@/components/Button'

export default function LoginScreen() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const login = useAuthStore(state => state.login)

  return (
    <View>
      <TextInput
        placeholder="Email"
        value={email}
        onChangeText={setEmail}
        autoCapitalize="none"
      />
      <TextInput
        placeholder="Password"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />
      <Button
        title="Login"
        onPress={() => login(email, password)}
      />
    </View>
  )
}
```

---

## Performance Optimization

### Image Optimization

```typescript
// components/OptimizedImage.tsx
import { Image } from 'expo-image'
import { StyleSheet } from 'react-native'

interface OptimizedImageProps {
  uri: string
  width: number
  height: number
}

export function OptimizedImage({ uri, width, height }: OptimizedImageProps) {
  return (
    <Image
      source={{ uri }}
      style={{ width, height }}
      contentFit="cover"
      transition={200}
      cachePolicy="memory-disk"
      placeholder={require('@/assets/placeholder.png')}
    />
  )
}
```

### Lazy Loading

```typescript
// app/(tabs)/index.tsx
import { lazy, Suspense } from 'react'
import { View, ActivityIndicator } from 'react-native'

const HeavyComponent = lazy(() => import('@/components/HeavyComponent'))

export default function HomeScreen() {
  return (
    <View>
      <Suspense fallback={<ActivityIndicator />}>
        <HeavyComponent />
      </Suspense>
    </View>
  )
}
```

### List Optimization

```typescript
import { FlashList } from '@shopify/flash-list'

export default function OptimizedList({ data }) {
  return (
    <FlashList
      data={data}
      renderItem={({ item }) => <Card>{item.title}</Card>}
      estimatedItemSize={100}
      keyExtractor={(item) => item.id}
    />
  )
}
```

---

## App Configuration

### app.json

```json
{
  "expo": {
    "name": "My App",
    "slug": "my-app",
    "version": "1.0.0",
    "orientation": "portrait",
    "icon": "./assets/icon.png",
    "userInterfaceStyle": "automatic",
    "splash": {
      "image": "./assets/splash.png",
      "resizeMode": "contain",
      "backgroundColor": "#ffffff"
    },
    "ios": {
      "supportsTablet": true,
      "bundleIdentifier": "com.yourcompany.myapp",
      "buildNumber": "1"
    },
    "android": {
      "adaptiveIcon": {
        "foregroundImage": "./assets/adaptive-icon.png",
        "backgroundColor": "#ffffff"
      },
      "package": "com.yourcompany.myapp",
      "versionCode": 1,
      "permissions": ["CAMERA", "ACCESS_FINE_LOCATION", "NOTIFICATIONS"]
    },
    "plugins": [
      "expo-router",
      [
        "expo-camera",
        {
          "cameraPermission": "Allow $(PRODUCT_NAME) to access your camera"
        }
      ],
      [
        "expo-location",
        {
          "locationAlwaysAndWhenInUsePermission": "Allow $(PRODUCT_NAME) to use your location."
        }
      ]
    ]
  }
}
```

---

## Building and Deploying

### Build for iOS

```bash
# Install EAS CLI
npm install -g eas-cli

# Login
eas login

# Configure build
eas build:configure

# Build for iOS
eas build --platform ios

# Submit to App Store
eas submit --platform ios
```

### Build for Android

```bash
# Build for Android
eas build --platform android

# Submit to Google Play
eas submit --platform android
```

### Over-the-Air (OTA) Updates

```bash
# Create update
eas update --branch production --message "Bug fixes"

# Users get update automatically (no app store review)
```

---

## Testing

### Jest + React Native Testing Library

```typescript
// __tests__/Button.test.tsx
import { render, fireEvent } from '@testing-library/react-native'
import { Button } from '@/components/Button'

describe('Button', () => {
  it('calls onPress when pressed', () => {
    const onPress = jest.fn()
    const { getByText } = render(<Button title="Click me" onPress={onPress} />)

    fireEvent.press(getByText('Click me'))

    expect(onPress).toHaveBeenCalledTimes(1)
  })

  it('shows loading indicator when loading', () => {
    const { getByTestId } = render(
      <Button title="Click me" onPress={() => {}} loading />
    )

    expect(getByTestId('loading-indicator')).toBeTruthy()
  })
})
```

---

## Common Patterns

### Protected Routes

```typescript
// app/_layout.tsx
import { useEffect } from 'react'
import { useRouter, Slot } from 'expo-router'
import { useAuthStore } from '@/store/auth'

export default function RootLayout() {
  const router = useRouter()
  const user = useAuthStore(state => state.user)

  useEffect(() => {
    if (!user) {
      router.replace('/login')
    }
  }, [user])

  return <Slot />
}
```

### Form Handling

```typescript
// hooks/useForm.ts
import { useState } from 'react'

export function useForm<T>(initialValues: T) {
  const [values, setValues] = useState<T>(initialValues)
  const [errors, setErrors] = useState<Partial<Record<keyof T, string>>>({})

  const handleChange = (name: keyof T) => (value: any) => {
    setValues(prev => ({ ...prev, [name]: value }))
    setErrors(prev => ({ ...prev, [name]: undefined }))
  }

  const validate = (rules: Partial<Record<keyof T, (value: any) => string | undefined>>) => {
    const newErrors: Partial<Record<keyof T, string>> = {}

    Object.keys(rules).forEach(key => {
      const error = rules[key as keyof T]?.(values[key as keyof T])
      if (error) {
        newErrors[key as keyof T] = error
      }
    })

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  return { values, errors, handleChange, validate }
}
```

---

## When to Use Me

**Perfect for:**

- Building iOS + Android apps from one codebase
- Rapid mobile prototyping
- Apps with native features (camera, location, push)
- Cross-platform mobile development

**I'll help you:**

- Set up React Native / Expo projects
- Implement navigation
- Integrate native features
- Optimize performance
- Submit to app stores

## What I'll Create

```
📱 Cross-Platform Apps
🧭 Navigation Systems
📸 Camera Integration
📍 Location Services
🔔 Push Notifications
🚀 App Store Submissions
```

Let's build amazing mobile experiences!
