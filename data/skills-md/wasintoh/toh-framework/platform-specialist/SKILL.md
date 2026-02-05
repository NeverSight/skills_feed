---
name: platform-specialist
description: >
  Platform-specific integration expert for LINE Mini App (LIFF), Expo (React Native),
  and Tauri (Desktop). Handles platform APIs, native features, and deployment.
  Called when app needs platform-specific features beyond standard web.
  Triggers: "LINE Mini App", "LIFF", "LINE OA", "mobile app", "Expo", "React Native",
  "desktop app", "Tauri", platform integration, native features.
---

# Platform Specialist

Make web apps native. LINE, Mobile, Desktop - same quality, platform-optimized.

<core_principle>
## The Platform Promise

Same beautiful UI → Platform-specific magic → Native-feeling experience

We adapt, not rebuild. Core logic stays the same.
</core_principle>

<line_mini_app>
## LINE Mini App (LIFF)

### What is LIFF?
LINE Front-end Framework - run web apps inside LINE app with access to LINE APIs.

### Setup
```bash
npm install @line/liff
```

```typescript
// src/lib/liff.ts
import liff from '@line/liff'

const LIFF_ID = process.env.NEXT_PUBLIC_LIFF_ID!

export async function initializeLiff() {
  try {
    await liff.init({ liffId: LIFF_ID })
    return true
  } catch (error) {
    console.error('LIFF init failed:', error)
    return false
  }
}

export function isInLiff(): boolean {
  return liff.isInClient()
}

export function isLoggedIn(): boolean {
  return liff.isLoggedIn()
}

export async function login() {
  if (!liff.isLoggedIn()) {
    liff.login()
  }
}

export async function logout() {
  if (liff.isLoggedIn()) {
    liff.logout()
  }
}

export async function getProfile() {
  if (!liff.isLoggedIn()) return null
  return await liff.getProfile()
}

export async function getAccessToken() {
  return liff.getAccessToken()
}

// Send message to LINE chat
export async function sendMessage(text: string) {
  if (!liff.isInClient()) return
  
  await liff.sendMessages([
    { type: 'text', text }
  ])
}

// Share to LINE
export async function shareMessage(text: string) {
  if (!liff.isApiAvailable('shareTargetPicker')) return
  
  await liff.shareTargetPicker([
    { type: 'text', text }
  ])
}

// Close LIFF window
export function closeLiff() {
  if (liff.isInClient()) {
    liff.closeWindow()
  }
}
```

### LIFF Provider
```tsx
// src/providers/liff-provider.tsx
'use client'

import { createContext, useContext, useEffect, useState } from 'react'
import { initializeLiff, getProfile, isLoggedIn, isInLiff } from '@/lib/liff'

interface LiffProfile {
  userId: string
  displayName: string
  pictureUrl?: string
  statusMessage?: string
}

interface LiffContextType {
  isReady: boolean
  isInLiff: boolean
  isLoggedIn: boolean
  profile: LiffProfile | null
  error: string | null
}

const LiffContext = createContext<LiffContextType>({
  isReady: false,
  isInLiff: false,
  isLoggedIn: false,
  profile: null,
  error: null,
})

export function LiffProvider({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState<LiffContextType>({
    isReady: false,
    isInLiff: false,
    isLoggedIn: false,
    profile: null,
    error: null,
  })

  useEffect(() => {
    async function init() {
      const success = await initializeLiff()
      
      if (!success) {
        setState(prev => ({ ...prev, isReady: true, error: 'LIFF init failed' }))
        return
      }

      const inLiff = isInLiff()
      const loggedIn = isLoggedIn()
      let profile = null

      if (loggedIn) {
        profile = await getProfile()
      }

      setState({
        isReady: true,
        isInLiff: inLiff,
        isLoggedIn: loggedIn,
        profile,
        error: null,
      })
    }

    init()
  }, [])

  return (
    <LiffContext.Provider value={state}>
      {children}
    </LiffContext.Provider>
  )
}

export const useLiff = () => useContext(LiffContext)
```

### Connect LIFF to Supabase Auth
```typescript
// src/lib/liff-auth.ts
import { supabase } from './supabase'
import { getAccessToken, getProfile } from './liff'

export async function signInWithLiff() {
  const accessToken = getAccessToken()
  const profile = await getProfile()
  
  if (!accessToken || !profile) {
    throw new Error('LIFF not logged in')
  }

  // Create or sign in user via Supabase Edge Function
  const { data, error } = await supabase.functions.invoke('liff-auth', {
    body: {
      accessToken,
      userId: profile.userId,
      displayName: profile.displayName,
      pictureUrl: profile.pictureUrl,
    }
  })

  if (error) throw error
  
  // Set Supabase session
  await supabase.auth.setSession({
    access_token: data.access_token,
    refresh_token: data.refresh_token,
  })

  return data.user
}
```

### LINE-Specific UI Components
```tsx
// LINE-style button
export function LineButton({ onClick, children }: { 
  onClick: () => void
  children: React.ReactNode 
}) {
  return (
    <button
      onClick={onClick}
      className="w-full bg-[#06C755] hover:bg-[#05B34D] text-white 
                 font-medium py-3 px-4 rounded-lg transition-colors"
    >
      {children}
    </button>
  )
}

// LINE profile card
export function LineProfileCard({ profile }: { profile: LiffProfile }) {
  return (
    <div className="flex items-center gap-3 p-4 bg-white rounded-lg shadow-sm">
      <img 
        src={profile.pictureUrl || '/default-avatar.png'} 
        alt={profile.displayName}
        className="w-12 h-12 rounded-full"
      />
      <div>
        <p className="font-medium">{profile.displayName}</p>
        {profile.statusMessage && (
          <p className="text-sm text-slate-500">{profile.statusMessage}</p>
        )}
      </div>
    </div>
  )
}
```

### LIFF Deployment Checklist
- [ ] Create LIFF app in LINE Developers Console
- [ ] Set LIFF endpoint URL (your deployed URL)
- [ ] Configure LIFF scope (profile, openid, etc.)
- [ ] Set NEXT_PUBLIC_LIFF_ID in environment
- [ ] Test in LINE app (not browser)
</line_mini_app>

<expo_react_native>
## Expo (React Native)

### Project Setup
```bash
# Create new Expo project
npx create-expo-app my-app --template tabs

# Or with our stack
npx create-expo-app my-app
cd my-app
npx expo install nativewind
npx expo install react-native-reanimated
npm install zustand @supabase/supabase-js
```

### NativeWind Setup (Tailwind for RN)
```javascript
// tailwind.config.js
module.exports = {
  content: [
    "./app/**/*.{js,jsx,ts,tsx}",
    "./components/**/*.{js,jsx,ts,tsx}"
  ],
  presets: [require("nativewind/preset")],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

```javascript
// babel.config.js
module.exports = function (api) {
  api.cache(true);
  return {
    presets: [
      ["babel-preset-expo", { jsxImportSource: "nativewind" }],
      "nativewind/babel",
    ],
  };
};
```

### File Structure
```
my-app/
├── app/                    # Expo Router (file-based routing)
│   ├── (tabs)/            # Tab navigation group
│   │   ├── index.tsx      # Home tab
│   │   ├── explore.tsx    # Explore tab
│   │   └── _layout.tsx    # Tab layout
│   ├── _layout.tsx        # Root layout
│   └── +not-found.tsx     # 404 page
├── components/
│   ├── ui/                # Reusable UI components
│   └── features/          # Feature-specific components
├── lib/
│   ├── supabase.ts       # Supabase client
│   └── utils.ts          # Utilities
├── stores/               # Zustand stores
└── types/                # TypeScript types
```

### Common Components Translation

**Web (shadcn) → React Native**
```tsx
// Web: Button
<Button variant="default">Click me</Button>

// React Native equivalent
import { Pressable, Text } from 'react-native'

export function Button({ children, onPress, variant = 'default' }) {
  return (
    <Pressable 
      onPress={onPress}
      className={`px-4 py-3 rounded-lg ${
        variant === 'default' 
          ? 'bg-blue-600 active:bg-blue-700' 
          : 'bg-slate-100 active:bg-slate-200'
      }`}
    >
      <Text className={`text-center font-medium ${
        variant === 'default' ? 'text-white' : 'text-slate-900'
      }`}>
        {children}
      </Text>
    </Pressable>
  )
}
```

```tsx
// Web: Card
<Card><CardContent>...</CardContent></Card>

// React Native equivalent
import { View } from 'react-native'

export function Card({ children, className = '' }) {
  return (
    <View className={`bg-white rounded-xl shadow-sm p-4 ${className}`}>
      {children}
    </View>
  )
}
```

```tsx
// Web: Input
<Input placeholder="Enter text" />

// React Native equivalent
import { TextInput } from 'react-native'

export function Input({ placeholder, value, onChangeText, ...props }) {
  return (
    <TextInput
      placeholder={placeholder}
      value={value}
      onChangeText={onChangeText}
      className="border border-slate-200 rounded-lg px-4 py-3 text-base"
      placeholderTextColor="#94a3b8"
      {...props}
    />
  )
}
```

### Navigation (Expo Router)
```tsx
// app/(tabs)/_layout.tsx
import { Tabs } from 'expo-router'
import { Home, Search, User } from 'lucide-react-native'

export default function TabLayout() {
  return (
    <Tabs screenOptions={{
      tabBarActiveTintColor: '#2563eb',
      headerShown: false,
    }}>
      <Tabs.Screen
        name="index"
        options={{
          title: 'Home',
          tabBarIcon: ({ color, size }) => (
            <Home size={size} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="explore"
        options={{
          title: 'Search',
          tabBarIcon: ({ color, size }) => (
            <Search size={size} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="profile"
        options={{
          title: 'Profile',
          tabBarIcon: ({ color, size }) => (
            <User size={size} color={color} />
          ),
        }}
      />
    </Tabs>
  )
}
```

### Supabase in Expo
```typescript
// lib/supabase.ts
import 'react-native-url-polyfill/auto'
import AsyncStorage from '@react-native-async-storage/async-storage'
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.EXPO_PUBLIC_SUPABASE_URL!
const supabaseKey = process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient(supabaseUrl, supabaseKey, {
  auth: {
    storage: AsyncStorage,
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: false,
  },
})
```

### Expo Deployment
```bash
# Development build
npx expo start

# Build for testing
eas build --profile development --platform ios
eas build --profile development --platform android

# Production build
eas build --profile production --platform all

# Submit to stores
eas submit --platform ios
eas submit --platform android
```
</expo_react_native>

<tauri_desktop>
## Tauri (Desktop App)

### Why Tauri?
- Reuse Next.js/React web code
- Native performance (Rust backend)
- Small bundle size (~10MB vs Electron's 100MB+)
- Cross-platform (macOS, Windows, Linux)

### Setup (Add to existing Next.js)
```bash
# Install Tauri CLI
npm install -D @tauri-apps/cli

# Initialize Tauri in existing project
npx tauri init
```

### Configuration
```json
// src-tauri/tauri.conf.json
{
  "build": {
    "beforeBuildCommand": "npm run build",
    "beforeDevCommand": "npm run dev",
    "devPath": "http://localhost:3000",
    "distDir": "../out"
  },
  "package": {
    "productName": "My App",
    "version": "1.0.0"
  },
  "tauri": {
    "bundle": {
      "active": true,
      "icon": [
        "icons/32x32.png",
        "icons/128x128.png",
        "icons/128x128@2x.png",
        "icons/icon.icns",
        "icons/icon.ico"
      ],
      "identifier": "com.myapp.app",
      "targets": "all"
    },
    "windows": [
      {
        "title": "My App",
        "width": 1200,
        "height": 800,
        "resizable": true,
        "fullscreen": false
      }
    ]
  }
}
```

### Next.js Config for Tauri
```javascript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',  // Static export for Tauri
  images: {
    unoptimized: true  // Required for static export
  }
}

module.exports = nextConfig
```

### Tauri Commands (Rust ↔ JavaScript)
```rust
// src-tauri/src/main.rs
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}!", name)
}

#[tauri::command]
async fn read_file(path: String) -> Result<String, String> {
    std::fs::read_to_string(path)
        .map_err(|e| e.to_string())
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![greet, read_file])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

```typescript
// Call from React
import { invoke } from '@tauri-apps/api/tauri'

async function greetUser() {
  const message = await invoke('greet', { name: 'Wasin' })
  console.log(message) // "Hello, Wasin!"
}

async function readLocalFile() {
  const content = await invoke('read_file', { 
    path: '/path/to/file.txt' 
  })
  console.log(content)
}
```

### Desktop-Specific Features
```typescript
// Window controls
import { appWindow } from '@tauri-apps/api/window'

await appWindow.minimize()
await appWindow.maximize()
await appWindow.close()

// System tray
import { TrayIcon } from '@tauri-apps/api/tray'

// File dialogs
import { open, save } from '@tauri-apps/api/dialog'

const selected = await open({
  multiple: false,
  filters: [{ name: 'Images', extensions: ['png', 'jpg'] }]
})

// Notifications
import { sendNotification } from '@tauri-apps/api/notification'

await sendNotification({
  title: 'My App',
  body: 'Operation completed!'
})
```

### Build & Distribute
```bash
# Development
npm run tauri dev

# Build for current platform
npm run tauri build

# Build for all platforms (requires cross-compilation setup)
npm run tauri build -- --target universal-apple-darwin  # macOS
npm run tauri build -- --target x86_64-pc-windows-msvc  # Windows
npm run tauri build -- --target x86_64-unknown-linux-gnu  # Linux
```
</tauri_desktop>

<platform_decision_tree>
## When to Use Which Platform

```
User Request
    │
    ▼
┌─────────────────────────────────────┐
│ Has "LINE" or "LIFF" keywords?      │
│ Or targets LINE users specifically? │
└─────────────────────────────────────┘
    │ YES → LINE Mini App
    │ NO ↓
┌─────────────────────────────────────┐
│ Has "mobile", "iOS", "Android",     │
│ "app store", or "native" keywords?  │
└─────────────────────────────────────┘
    │ YES → Expo (React Native)
    │ NO ↓
┌─────────────────────────────────────┐
│ Has "desktop", "mac", "windows",    │
│ "offline", or "native" keywords?    │
└─────────────────────────────────────┘
    │ YES → Tauri
    │ NO ↓
┌─────────────────────────────────────┐
│ Default: Next.js Web App            │
│ (Works everywhere via browser)      │
└─────────────────────────────────────┘
```
</platform_decision_tree>
