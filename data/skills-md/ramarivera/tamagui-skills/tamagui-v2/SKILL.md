---
name: tamagui-v2
description: |
  Universal React UI framework for web and native (v1.144.0+). Use when building cross-platform apps with React Native + Web,
  creating styled components with `styled()`, configuring design tokens/themes, using Tamagui UI components
  (Button, Dialog, Sheet, Input, Select, Tabs, etc.), working with animations, or needing Bento/Takeout premium components.
  Triggers: "tamagui", "universal UI", "react native web", "styled()", "design tokens", "$token",
  "XStack/YStack/ZStack", "useTheme", "useMedia", "@tamagui/*" imports, "bento", "takeout", "one.js router",
  "createStyledContext", "withStaticProperties", "@tanstack/react-table", "zero sync", "better auth".
---

# Tamagui v2 Skill

> Universal React UI framework for web and native (v1.144.0+)

This skill provides comprehensive guidance for building cross-platform React applications using Tamagui's styling system, component library, Bento premium components, and Takeout starter kit.

---

## Overview

**Tamagui** is a universal UI framework that lets you write once and deploy to both web and React Native with optimal performance. It features:

- **Unified styling API** - `styled()` function with design tokens, variants, and responsive patterns
- **Optimizing compiler** - Extracts styles to atomic CSS at build time for maximum performance
- **Theme system** - 12-step color scales with automatic light/dark mode support
- **Cross-platform components** - Button, Dialog, Sheet, Input, Select, Tabs, and more
- **Premium ecosystem** - Bento (production forms, tables, lists) + Takeout (full-stack starter with routing, auth, database, real-time sync)

**Version:** 1.144.0+  
**Platforms:** Web (React), iOS/Android (React Native), Expo  
**License:** Open source (MIT) + Bento/Takeout (commercial licenses)

---

## When to Use This Skill

Activate this skill when encountering these triggers:

### Core Framework
- "tamagui", "universal UI", "react native web", "cross-platform UI"
- "styled()", "design tokens", "$token", "theme tokens"
- "XStack", "YStack", "ZStack", "Stack components"
- "useTheme", "useMedia", "responsive design"
- "@tamagui/*" imports, "@tamagui/core"
- "createStyledContext", "withStaticProperties"
- "variant", "variants", "defaultVariants"

### Bento Components
- "bento", "@tamagui/bento", "bento components"
- "React Hook Form", "react-hook-form", "form validation"
- "Zod", "zod validation", "form schema"
- "TanStack Table", "@tanstack/react-table", "data table"
- "virtualized list", "FlatList", "masonry layout"

### Takeout Starter
- "takeout", "tamagui takeout", "one.js"
- "file-based routing", "one router", "SSG", "SSR"
- "Better Auth", "authentication", "OAuth"
- "Drizzle ORM", "database", "PostgreSQL"
- "Zero Sync", "real-time sync", "offline-first"

### Platform-Specific
- "animation driver", "CSS animations", "Reanimated"
- "compiler optimization", "static extraction", "bundle size"
- "web-only", "native-only", "platform-specific"

---

## Quick Start Patterns

### 1. Basic Styling with styled()

Create custom components by extending existing ones:

```tsx
import { View, Text, styled } from '@tamagui/core'

// Simple styled component
export const Card = styled(View, {
  padding: '$4',
  backgroundColor: '$background',
  borderRadius: '$4',
  borderWidth: 1,
  borderColor: '$borderColor',
})

// With variants
export const Button = styled(View, {
  padding: '$3',
  borderRadius: '$2',
  backgroundColor: '$blue10',
  cursor: 'pointer',
  
  variants: {
    variant: {
      primary: {
        backgroundColor: '$blue10',
      },
      secondary: {
        backgroundColor: '$gray5',
      },
      outlined: {
        backgroundColor: 'transparent',
        borderWidth: 1,
        borderColor: '$borderColor',
      },
    },
    size: {
      small: { padding: '$2' },
      medium: { padding: '$3' },
      large: { padding: '$4' },
    },
  } as const,
  
  defaultVariants: {
    variant: 'primary',
    size: 'medium',
  },
})

// Usage
<Button variant="outlined" size="large">Click Me</Button>
```

### 2. Core Layout Components

**Stacks** are the foundation of Tamagui layouts:

```tsx
import { XStack, YStack, ZStack, Text, Button } from 'tamagui'

export function LayoutExample() {
  return (
    <YStack gap="$4" padding="$4">
      {/* Horizontal stack */}
      <XStack gap="$2" justifyContent="space-between" alignItems="center">
        <Text>Label</Text>
        <Button>Action</Button>
      </XStack>
      
      {/* Vertical stack with responsive gap */}
      <YStack 
        gap="$4"
        $gtSm={{ gap: '$6' }}  // Larger gap on small+ screens
      >
        <Card>Item 1</Card>
        <Card>Item 2</Card>
      </YStack>
      
      {/* Overlay stack (position: relative) */}
      <ZStack width={300} height={200}>
        <View backgroundColor="$blue5" fullscreen />
        <Text position="absolute" top="$4" left="$4">
          Overlay Text
        </Text>
      </ZStack>
    </YStack>
  )
}
```

### 3. Using Design Tokens

Design tokens provide consistent values across your app:

```tsx
import { View, Text, createTamagui } from '@tamagui/core'

// Tokens are defined in createTamagui config
const config = createTamagui({
  tokens: {
    color: {
      white: '#fff',
      black: '#000',
      blue: '#0066cc',
    },
    space: {
      1: 4,
      2: 8,
      3: 12,
      4: 16,
    },
    size: {
      sm: 100,
      md: 200,
      lg: 300,
    },
    radius: {
      1: 4,
      2: 8,
      3: 12,
      4: 16,
    },
  },
})

// Use tokens with $ prefix
<View 
  padding="$4"           // Uses space.4 = 16px
  backgroundColor="$blue" // Uses color.blue
  borderRadius="$3"      // Uses radius.3 = 12px
  width="$md"            // Uses size.md = 200px
/>

// Tokens work in styled()
const StyledCard = styled(View, {
  padding: '$4',
  margin: '$2',
  backgroundColor: '$background',
  borderRadius: '$4',
})
```

### 4. Theming with 12-Step Color Scales

Tamagui uses a semantic color scale system (1-12) for consistent theming:

```tsx
import { YStack, Text, Theme } from 'tamagui'

export function ThemeExample() {
  return (
    <YStack 
      backgroundColor="$color1"  // Subtle background
      borderColor="$color6"      // Regular border
      padding="$4"
    >
      <Text color="$color12">Heading (highest contrast)</Text>
      <Text color="$color11">Body text (high contrast)</Text>
      <Text color="$color10">Muted text (low contrast)</Text>
      
      {/* Apply sub-theme */}
      <Theme name="blue">
        <YStack 
          backgroundColor="$color9"  // Blue solid background
          padding="$3"
          borderRadius="$2"
        >
          <Text color="$color1">White text on blue</Text>
        </Theme>
      </YStack>
    </YStack>
  )
}

// Dynamic theme switching
import { useTheme } from '@tamagui/core'

export function ThemedComponent() {
  const theme = useTheme()
  
  // Access theme values directly
  console.log(theme.background.val) // e.g., "#ffffff"
  console.log(theme.color11.val)    // e.g., "#333333"
  
  return <Text color={theme.color11}>Themed Text</Text>
}
```

### 5. Responsive Design with Media Queries

Use media query props for responsive layouts:

```tsx
import { YStack, Text, useMedia } from 'tamagui'

export function ResponsiveExample() {
  const media = useMedia()
  
  return (
    <YStack
      padding="$4"
      $gtSm={{ padding: '$6' }}     // > sm breakpoint
      $gtMd={{ padding: '$8' }}     // > md breakpoint
      flexDirection="column"
      $gtLg={{ flexDirection: 'row' }}  // Row layout on large screens
    >
      <Text
        fontSize="$4"
        $gtSm={{ fontSize: '$5' }}
        $gtMd={{ fontSize: '$6' }}
      >
        Responsive Text
      </Text>
      
      {/* Conditional rendering based on media query */}
      {media.gtMd && <Text>Only on medium+ screens</Text>}
    </YStack>
  )
}

// Configure media queries in createTamagui
const config = createTamagui({
  media: {
    xs: { maxWidth: 660 },
    sm: { maxWidth: 800 },
    md: { maxWidth: 1020 },
    lg: { maxWidth: 1280 },
    xl: { maxWidth: 1420 },
    xxl: { maxWidth: 1600 },
    gtXs: { minWidth: 660 + 1 },
    gtSm: { minWidth: 800 + 1 },
    gtMd: { minWidth: 1020 + 1 },
    gtLg: { minWidth: 1280 + 1 },
  },
})
```

### 6. Animations with enterStyle/exitStyle

Add smooth animations to any component:

```tsx
import { YStack, Button, AnimatePresence } from 'tamagui'
import { useState } from 'react'

export function AnimationExample() {
  const [show, setShow] = useState(false)
  
  return (
    <YStack gap="$4">
      <Button onPress={() => setShow(!show)}>
        Toggle
      </Button>
      
      <AnimatePresence>
        {show && (
          <YStack
            key="animated-box"
            animation="quick"
            enterStyle={{ 
              opacity: 0, 
              y: -20,
              scale: 0.9,
            }}
            exitStyle={{ 
              opacity: 0,
              y: 20,
              scale: 0.9,
            }}
            opacity={1}
            y={0}
            scale={1}
            backgroundColor="$blue5"
            padding="$4"
            borderRadius="$4"
          >
            <Text>Animated Content</Text>
          </YStack>
        )}
      </AnimatePresence>
    </YStack>
  )
}

// Define animations in createTamagui
import { createAnimations } from '@tamagui/animations-react-native'

const animations = createAnimations({
  quick: {
    type: 'spring',
    damping: 20,
    mass: 1.2,
    stiffness: 250,
  },
  bouncy: {
    type: 'spring',
    damping: 10,
    mass: 0.9,
    stiffness: 100,
  },
})
```

### 7. Compound Components with createStyledContext

Build cohesive component families:

```tsx
import { createStyledContext, styled, View, Text } from '@tamagui/core'
import { withStaticProperties } from '@tamagui/helpers'

// Define context
const CardContext = createStyledContext({
  size: '$4' as any,
})

// Create base component
const CardFrame = styled(View, {
  backgroundColor: '$background',
  borderRadius: '$4',
  borderWidth: 1,
  borderColor: '$borderColor',
  
  context: CardContext,
  
  variants: {
    size: {
      small: { padding: '$3' },
      medium: { padding: '$4' },
      large: { padding: '$6' },
    },
  } as const,
})

// Create child components that consume context
const CardTitle = styled(Text, {
  context: CardContext,
  fontWeight: 'bold',
  
  variants: {
    size: {
      small: { fontSize: '$4' },
      medium: { fontSize: '$5' },
      large: { fontSize: '$6' },
    },
  } as const,
})

const CardDescription = styled(Text, {
  context: CardContext,
  color: '$color11',
  
  variants: {
    size: {
      small: { fontSize: '$3' },
      medium: { fontSize: '$4' },
      large: { fontSize: '$5' },
    },
  } as const,
})

// Compose with static properties
export const Card = withStaticProperties(CardFrame, {
  Title: CardTitle,
  Description: CardDescription,
})

// Usage - size cascades to all children
<Card size="large">
  <Card.Title>Large Card</Card.Title>
  <Card.Description>
    All text automatically sized large
  </Card.Description>
</Card>
```

### 8. Form Component Example

```tsx
import { Button, Dialog, Input, Label, XStack, YStack } from 'tamagui'

export function LoginForm() {
  return (
    <YStack gap="$4" padding="$4">
      <YStack gap="$2">
        <Label htmlFor="email">Email</Label>
        <Input 
          id="email" 
          placeholder="email@example.com"
          autoCapitalize="none"
          keyboardType="email-address"
        />
      </YStack>
      
      <YStack gap="$2">
        <Label htmlFor="password">Password</Label>
        <Input 
          id="password" 
          secureTextEntry
          placeholder="••••••••"
        />
      </YStack>
      
      <XStack gap="$2" justifyContent="flex-end">
        <Button variant="outlined">Cancel</Button>
        <Button theme="blue">Sign In</Button>
      </XStack>
    </YStack>
  )
}
```

### 9. Dialog Pattern

```tsx
import { Button, Dialog, XStack, YStack, H2, Paragraph } from 'tamagui'

export function DialogExample() {
  return (
    <Dialog>
      <Dialog.Trigger asChild>
        <Button>Open Dialog</Button>
      </Dialog.Trigger>

      <Dialog.Portal>
        <Dialog.Overlay
          key="overlay"
          animation="quick"
          opacity={0.5}
          enterStyle={{ opacity: 0 }}
          exitStyle={{ opacity: 0 }}
        />

        <Dialog.Content
          bordered
          elevate
          key="content"
          animation={['quick', { opacity: { overshootClamping: true } }]}
          enterStyle={{ x: 0, y: -20, opacity: 0, scale: 0.9 }}
          exitStyle={{ x: 0, y: 10, opacity: 0, scale: 0.95 }}
          gap="$4"
        >
          <Dialog.Title>Confirm Action</Dialog.Title>
          <Dialog.Description>
            Are you sure you want to proceed?
          </Dialog.Description>

          <XStack alignSelf="flex-end" gap="$2">
            <Dialog.Close displayWhenAdapted asChild>
              <Button variant="outlined">Cancel</Button>
            </Dialog.Close>
            <Dialog.Close asChild>
              <Button theme="blue">Confirm</Button>
            </Dialog.Close>
          </XStack>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog>
  )
}
```

### 10. Adapt Pattern (Mobile Sheet on Small Screens)

```tsx
import { Button, Dialog, Sheet, Adapt } from 'tamagui'

export function AdaptiveDialog() {
  return (
    <Dialog>
      <Dialog.Trigger asChild>
        <Button>Open</Button>
      </Dialog.Trigger>

      <Adapt when="sm" platform="touch">
        <Sheet animation="medium" zIndex={200000} modal dismissOnSnapToBottom>
          <Sheet.Frame padding="$4" gap="$4">
            <Adapt.Contents />
          </Sheet.Frame>
          <Sheet.Overlay 
            animation="lazy"
            enterStyle={{ opacity: 0 }}
            exitStyle={{ opacity: 0 }}
          />
        </Sheet>
      </Adapt>

      <Dialog.Portal>
        <Dialog.Overlay />
        <Dialog.Content>
          {/* Content shows as Dialog on desktop, Sheet on mobile */}
          <Dialog.Title>Adaptive UI</Dialog.Title>
          <Dialog.Description>
            This is a dialog on desktop, sheet on mobile
          </Dialog.Description>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog>
  )
}
```

---

## Bento Components Overview

Premium components from `@tamagui/bento` (requires [Bento license](https://tamagui.dev/bento) for production use).

### Forms System

Composable input components with React Hook Form and Zod integration:

```tsx
import { Input } from '@tamagui/bento/components/inputsParts'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const schema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
})

export function BentoForm() {
  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: zodResolver(schema),
  })
  
  return (
    <YStack gap="$4">
      <Input size="$4">
        <Input.Label htmlFor="email">Email</Input.Label>
        <Input.Box>
          <Input.Section>
            <Mail size={16} />
          </Input.Section>
          <Input.Area 
            id="email" 
            placeholder="email@example.com"
            {...register('email')}
          />
        </Input.Box>
        {errors.email && (
          <Input.Info color="$red10">{errors.email.message}</Input.Info>
        )}
      </Input>
      
      <Input size="$4">
        <Input.Label htmlFor="password">Password</Input.Label>
        <Input.Box>
          <Input.Area 
            id="password" 
            secureTextEntry
            placeholder="••••••••"
            {...register('password')}
          />
          <Input.Section>
            <Input.Button>
              <Eye size={16} />
            </Input.Button>
          </Input.Section>
        </Input.Box>
        {errors.password && (
          <Input.Info color="$red10">{errors.password.message}</Input.Info>
        )}
      </Input>
    </YStack>
  )
}
```

**Key Features:**
- **Input.Label** - Accessible label with `htmlFor` binding
- **Input.Box** - Focus-aware container with `FocusContext`
- **Input.Section** - Layout sections for icons/buttons
- **Input.Area** - Actual text input
- **Input.Icon** - Themed icon container
- **Input.Button** - Action button within input
- **Input.Info** - Helper/error text

### Tables with TanStack Table

Production-ready data tables with sorting, filtering, and pagination:

```tsx
import { DataTable } from '@tamagui/bento/components/Table'
import { createColumnHelper } from '@tanstack/react-table'

type User = {
  id: number
  name: string
  email: string
  role: string
}

const columnHelper = createColumnHelper<User>()

const columns = [
  columnHelper.accessor('name', {
    header: 'Name',
    cell: info => info.getValue(),
  }),
  columnHelper.accessor('email', {
    header: 'Email',
    cell: info => info.getValue(),
  }),
  columnHelper.accessor('role', {
    header: 'Role',
    cell: info => <Text textTransform="capitalize">{info.getValue()}</Text>,
  }),
]

export function UsersTable({ users }: { users: User[] }) {
  return (
    <DataTable
      data={users}
      columns={columns}
      enableSorting
      enableFiltering
      enablePagination
      pageSize={10}
    />
  )
}
```

### Virtualized Lists

Efficient list rendering with FlatList patterns:

```tsx
import { FlatList } from '@tamagui/bento/components/List'
import { YStack, Text } from 'tamagui'

export function VirtualizedList({ items }: { items: string[] }) {
  return (
    <FlatList
      data={items}
      keyExtractor={(item, index) => `${item}-${index}`}
      renderItem={({ item }) => (
        <YStack padding="$4" borderBottomWidth={1} borderColor="$borderColor">
          <Text>{item}</Text>
        </YStack>
      )}
      estimatedItemSize={60}
    />
  )
}
```

**Additional Patterns:**
- **Masonry layouts** - Pinterest-style grids
- **Horizontal carousels** - Swipeable lists
- **Animated lists** - Enter/exit animations
- **Pull to refresh** - Mobile-friendly refresh

---

## Takeout Stack Overview

Full-stack starter kit from [Tamagui Takeout](https://tamagui.dev/takeout) (requires license).

### One.js Routing

File-based routing with SSG/SSR/SPA modes:

```
app/
  _layout.tsx              # Root layout
  index.tsx                # / (home page)
  blog/
    [slug].tsx             # /blog/my-post (dynamic route)
  (auth)/                  # Route group (no URL nesting)
    login.tsx              # /login
    signup.tsx             # /signup
  +not-found.tsx           # Custom 404 page
```

**Type-safe navigation:**

```tsx
import { Link, useRouter, useParams } from 'one'

export function Navigation() {
  const router = useRouter()
  
  return (
    <YStack gap="$2">
      {/* Declarative navigation */}
      <Link href="/">Home</Link>
      <Link href="/blog/hello-world">Blog Post</Link>
      
      {/* Programmatic navigation */}
      <Button onPress={() => router.push('/about')}>
        Go to About
      </Button>
    </YStack>
  )
}

// Dynamic routes
export function BlogPost() {
  const { slug } = useParams<{ slug: string }>()
  return <Text>Post: {slug}</Text>
}
```

**Server-side data loading:**

```tsx
import { createLoader } from 'one'

export const loader = createLoader(async (context) => {
  const post = await db.query.posts.findFirst({
    where: eq(posts.slug, context.params.slug),
  })
  
  return { post }
})

export default function BlogPost() {
  const { post } = useLoader(loader)
  return <Text>{post.title}</Text>
}
```

### Better Auth Integration

Complete authentication system with multiple strategies:

```tsx
import { signIn, signOut, useSession } from '~/lib/auth'

export function AuthExample() {
  const session = useSession()
  
  if (!session.user) {
    return (
      <YStack gap="$4">
        {/* Email/password */}
        <Button onPress={() => signIn.email({ email, password })}>
          Sign In
        </Button>
        
        {/* OAuth */}
        <Button onPress={() => signIn.social({ provider: 'github' })}>
          Sign in with GitHub
        </Button>
        
        {/* Magic link */}
        <Button onPress={() => signIn.magicLink({ email })}>
          Send Magic Link
        </Button>
      </YStack>
    )
  }
  
  return (
    <YStack gap="$2">
      <Text>Welcome, {session.user.name}</Text>
      <Button onPress={() => signOut()}>Sign Out</Button>
    </YStack>
  )
}
```

**Features:**
- Email/password authentication
- OAuth (GitHub, Google, etc.)
- Magic links (email)
- OTP (email/phone)
- Session management
- JWT tokens for native apps

### Drizzle ORM (Database)

Type-safe database queries with PostgreSQL:

```tsx
import { db } from '~/db'
import { posts, users } from '~/db/schema'
import { eq, desc } from 'drizzle-orm'

// Define schema
export const posts = pgTable('posts', {
  id: serial('id').primaryKey(),
  title: text('title').notNull(),
  slug: text('slug').notNull().unique(),
  content: text('content'),
  authorId: integer('author_id').references(() => users.id),
  createdAt: timestamp('created_at').defaultNow(),
})

// Query
const allPosts = await db.query.posts.findMany({
  orderBy: [desc(posts.createdAt)],
  with: {
    author: true,  // Join with users
  },
})

// Insert
await db.insert(posts).values({
  title: 'My Post',
  slug: 'my-post',
  content: 'Post content...',
  authorId: 1,
})

// Update
await db.update(posts)
  .set({ title: 'Updated Title' })
  .where(eq(posts.id, 1))

// Delete
await db.delete(posts).where(eq(posts.id, 1))
```

### Zero Sync (Real-time Data)

Offline-first real-time synchronization:

```tsx
import { useQuery, useMutation } from '@rocicorp/zero/react'
import { z } from '@rocicorp/zero'

// Define schema
const todoSchema = z.object({
  id: z.string(),
  text: z.string(),
  completed: z.boolean(),
  createdAt: z.number(),
})

export function TodoList() {
  // Real-time query (updates automatically)
  const [todos] = useQuery(q => q.todos.orderBy('createdAt', 'desc'))
  
  // Optimistic mutation
  const [addTodo] = useMutation(async (tx, text: string) => {
    await tx.todos.insert({
      id: crypto.randomUUID(),
      text,
      completed: false,
      createdAt: Date.now(),
    })
  })
  
  const [toggleTodo] = useMutation(async (tx, id: string) => {
    const todo = await tx.todos.get(id)
    if (todo) {
      await tx.todos.update({
        id,
        completed: !todo.completed,
      })
    }
  })
  
  return (
    <YStack gap="$2">
      {todos.map(todo => (
        <XStack key={todo.id} gap="$2">
          <Checkbox 
            checked={todo.completed}
            onCheckedChange={() => toggleTodo(todo.id)}
          />
          <Text>{todo.text}</Text>
        </XStack>
      ))}
    </YStack>
  )
}
```

**Features:**
- Real-time synchronization across devices
- Offline-first architecture
- Optimistic mutations (instant UI updates)
- Automatic conflict resolution
- Type-safe queries with Zod
- Client-side replica for 0-latency queries

---

## Reference Guide

For detailed documentation on specific topics, refer to these reference files:

| Topic | Reference File | Description |
|-------|---------------|-------------|
| **Core Styling** | [`core-styling.md`](./references/core-styling.md) | `styled()` API, variant systems, `createStyledContext`, composition patterns, TypeScript integration |
| **Components** | [`components.md`](./references/components.md) | Button, Dialog, Sheet, Input, Select, Tabs, Switch, Popover, Stacks, Adapt pattern |
| **Theming** | [`theming.md`](./references/theming.md) | 12-step color scale system, theme creation, dynamic theme switching, `useTheme` hook |
| **Animations** | [`animations.md`](./references/animations.md) | Animation drivers (CSS, React Native, Reanimated, Motion), `enterStyle`/`exitStyle`, `AnimatePresence` |
| **Configuration** | [`configuration.md`](./references/configuration.md) | `createTamagui` function, tokens, themes, fonts, media queries, shorthands |
| **Compiler** | [`compiler.md`](./references/compiler.md) | Static extraction, Babel optimization, atomic CSS generation, platform-specific setup |
| **Bento Forms** | [`bento-forms.md`](./references/bento-forms.md) | React Hook Form integration, Zod validation, composable input system, accessibility |
| **Bento Tables** | [`bento-tables.md`](./references/bento-tables.md) | TanStack Table v8 integration, sorting, pagination, filtering, responsive layouts |
| **Bento Lists** | [`bento-lists.md`](./references/bento-lists.md) | FlatList patterns, virtualized lists, masonry layouts, performance optimization |
| **Takeout Routing** | [`takeout-routing.md`](./references/takeout-routing.md) | One.js file-based routing, SSG/SSR/SPA modes, dynamic routes, server-side data loading |
| **Takeout Auth** | [`takeout-auth.md`](./references/takeout-auth.md) | Better Auth integration, session management, OAuth, magic links, OTP |
| **Takeout Database** | [`takeout-database.md`](./references/takeout-database.md) | Drizzle ORM setup, schema definitions, type-safe queries, migrations |
| **Takeout Zero** | [`takeout-zero.md`](./references/takeout-zero.md) | Zero Sync for real-time data, offline-first architecture, optimistic mutations |
| **Breaking Changes** | [`breaking-changes-and-new-features.md`](./references/breaking-changes-and-new-features.md) | Migration guide from older versions, config v4/v5 differences |

---

## Common Pitfalls

### 1. Token Usage

**❌ Wrong:**
```tsx
<View padding={16} />  // Hard-coded value
<View padding="16px" /> // String with unit
```

**✅ Correct:**
```tsx
<View padding="$4" />  // Token reference
<View padding={16} />  // Number is OK if intentional (not extracted by compiler)
```

### 2. Variant Definitions

**❌ Wrong:**
```tsx
// Missing `as const`
variants: {
  size: {
    small: { padding: '$2' },
    large: { padding: '$4' },
  },
}
```

**✅ Correct:**
```tsx
// Must use `as const` for proper TypeScript inference
variants: {
  size: {
    small: { padding: '$2' },
    large: { padding: '$4' },
  },
} as const
```

### 3. Platform-Specific Styles

**❌ Wrong:**
```tsx
// Using platform detection in styled()
const Component = styled(View, {
  padding: Platform.OS === 'web' ? 10 : 20,  // Won't extract
})
```

**✅ Correct:**
```tsx
// Use platform prop modifiers
const Component = styled(View, {
  padding: 20,
  $platform-web: {
    padding: 10,
  },
})
```

### 4. Media Query Prop Order

**❌ Wrong:**
```tsx
<View 
  $gtMd={{ padding: '$8' }}  // Applied first
  padding="$4"               // Overrides media query
/>
```

**✅ Correct:**
```tsx
<View 
  padding="$4"               // Base value
  $gtMd={{ padding: '$8' }}  // Overrides on medium+
/>
```

### 5. Animation Driver Mismatch

**❌ Wrong:**
```tsx
// Using spring physics with CSS driver
import { createAnimations } from '@tamagui/animations-css'

const animations = createAnimations({
  bouncy: {
    type: 'spring',  // CSS doesn't support springs!
    damping: 10,
  },
})
```

**✅ Correct:**
```tsx
// CSS driver uses easing strings
import { createAnimations } from '@tamagui/animations-css'

const animations = createAnimations({
  bouncy: 'cubic-bezier(0.68, -0.55, 0.265, 1.55) 500ms',
})

// Or use React Native driver for springs
import { createAnimations } from '@tamagui/animations-react-native'

const animations = createAnimations({
  bouncy: {
    type: 'spring',
    damping: 10,
    stiffness: 100,
  },
})
```

### 6. Context Without Static Properties

**❌ Wrong:**
```tsx
// Creating compound components without withStaticProperties
const Card = styled(View, { context: CardContext })
const CardTitle = styled(Text, { context: CardContext })

// Usage requires separate imports
import { Card } from './Card'
import { CardTitle } from './CardTitle'

<Card>
  <CardTitle>Title</CardTitle>
</Card>
```

**✅ Correct:**
```tsx
import { withStaticProperties } from '@tamagui/helpers'

const CardFrame = styled(View, { context: CardContext })
const CardTitle = styled(Text, { context: CardContext })

export const Card = withStaticProperties(CardFrame, {
  Title: CardTitle,
})

// Single import
<Card>
  <Card.Title>Title</Card.Title>
</Card>
```

### 7. Missing AnimatePresence

**❌ Wrong:**
```tsx
// Using exitStyle without AnimatePresence
{show && (
  <View 
    animation="quick"
    enterStyle={{ opacity: 0 }}
    exitStyle={{ opacity: 0 }}  // Won't animate on exit!
  />
)}
```

**✅ Correct:**
```tsx
import { AnimatePresence } from 'tamagui'

<AnimatePresence>
  {show && (
    <View 
      key="animated-view"  // Key is required!
      animation="quick"
      enterStyle={{ opacity: 0 }}
      exitStyle={{ opacity: 0 }}
    />
  )}
</AnimatePresence>
```

### 8. Inline Styles vs. styled()

**❌ Wrong (Performance):**
```tsx
// Inline styles aren't extracted by compiler
{items.map(item => (
  <View 
    key={item.id}
    style={{ 
      padding: 16, 
      backgroundColor: '#fff',
      borderRadius: 8,
    }}
  />
))}
```

**✅ Correct:**
```tsx
// Use styled() for extractable styles
const ItemView = styled(View, {
  padding: '$4',
  backgroundColor: '$background',
  borderRadius: '$2',
})

{items.map(item => (
  <ItemView key={item.id} />
))}
```

### 9. Web vs. Native Differences

Be aware of platform-specific behaviors:

- **CSS driver** - Web only, no spring physics
- **Sheet component** - Better UX on mobile with touch gestures
- **Adapt pattern** - Automatically switches components based on platform/screen size
- **Form attributes** (type, action, method) - Web only
- **Animation drivers** - Reanimated performs poorly on web, great on native

### 10. Compiler Optimization

Styles must be **statically analyzable** for the compiler to extract them:

**❌ Won't Extract:**
```tsx
const dynamicPadding = isPremium ? '$6' : '$4'
<View padding={dynamicPadding} />  // Runtime dynamic value
```

**✅ Will Extract:**
```tsx
<View padding={isPremium ? '$6' : '$4'} />  // Inline ternary is OK
// Or use variants
<View size={isPremium ? 'large' : 'small'} />
```

---

## Code Generation Tips

When generating Tamagui code, follow these best practices:

### 1. Start with Configuration

Always ensure `createTamagui` config exists with tokens, themes, and media queries before generating components.

### 2. Use Tokens Consistently

Prefer design tokens (`$4`, `$background`, `$color11`) over hard-coded values for extractable, themeable styles.

### 3. Leverage Variants for Flexibility

Create components with size, variant, and state variants rather than separate component definitions:

```tsx
// ✅ Good - One component with variants
const Button = styled(View, {
  variants: {
    variant: { primary: {...}, secondary: {...} },
    size: { small: {...}, large: {...} },
  } as const,
})

// ❌ Avoid - Multiple separate components
const PrimaryButton = styled(View, { ... })
const SecondaryButton = styled(View, { ... })
```

### 4. Compose with createStyledContext

For compound components (Card, Input, Select), use `createStyledContext` to share size and styling:

```tsx
const Context = createStyledContext({ size: '$4' })
const Parent = styled(View, { context: Context, variants: {...} })
const Child = styled(Text, { context: Context, variants: {...} })
export const Component = withStaticProperties(Parent, { Child })
```

### 5. Include Accessibility

Always add accessibility props:

```tsx
<Input 
  id="email"
  aria-label="Email address"
  aria-describedby="email-error"
  aria-invalid={!!error}
/>
<Label htmlFor="email">Email</Label>
{error && <Text id="email-error">{error}</Text>}
```

### 6. Responsive by Default

Include responsive props for better UX:

```tsx
<YStack
  padding="$4"
  $gtSm={{ padding: '$6' }}
  $gtMd={{ padding: '$8' }}
  flexDirection="column"
  $gtLg={{ flexDirection: 'row' }}
/>
```

### 7. Animation Patterns

Use `enterStyle`/`exitStyle` for enter/exit animations and wrap with `AnimatePresence`:

```tsx
<AnimatePresence>
  {show && (
    <View
      key="unique-key"
      animation="quick"
      enterStyle={{ opacity: 0, y: -10 }}
      exitStyle={{ opacity: 0, y: 10 }}
      opacity={1}
      y={0}
    />
  )}
</AnimatePresence>
```

### 8. Platform Adaptation

Use the Adapt pattern for mobile-friendly UIs:

```tsx
<Dialog>
  <Adapt when="sm" platform="touch">
    <Sheet>
      <Adapt.Contents />
    </Sheet>
  </Adapt>
  <Dialog.Portal>
    <Dialog.Content>...</Dialog.Content>
  </Dialog.Portal>
</Dialog>
```

### 9. TypeScript Types

Always export prop types for reusable components:

```tsx
import { GetProps } from '@tamagui/core'

export const MyComponent = styled(View, { ... })
export type MyComponentProps = GetProps<typeof MyComponent>
```

### 10. Testing Considerations

When generating test code:

- Use `testID` prop for component identification (cross-platform)
- Mock theme context with `TamaguiProvider`
- Test responsive behavior with media query mocks
- Verify animations with `AnimatePresence` exit callbacks

---

## Version and Ecosystem Notes

**Current Version:** 1.144.0+

**Dependencies:**
- React 19+ (or React 18.2+)
- React Native (for native targets)
- Expo SDK (optional, for managed workflow)

**Ecosystem Packages:**

| Package | Description |
|---------|-------------|
| `tamagui` | Meta-package with core + components |
| `@tamagui/core` | Core styling engine |
| `@tamagui/animations-css` | CSS animation driver |
| `@tamagui/animations-react-native` | React Native animation driver |
| `@tamagui/animations-reanimated` | Reanimated v3 driver |
| `@tamagui/animations-moti` | Moti/Motion driver |
| `@tamagui/themes` | Theme creation helpers |
| `@tamagui/colors` | Radix UI color scales |
| `@tamagui/bento` | Premium components (license required) |
| Tamagui Takeout | Full-stack starter (license required) |

**Migration from v1.x:**
- Read [`breaking-changes-and-new-features.md`](./references/breaking-changes-and-new-features.md)
- Update to v4 or v5 config format
- Realign media queries to v4 naming
- Replace deprecated patterns

---

## Quick Links

- **Official Docs:** https://tamagui.dev
- **GitHub:** https://github.com/tamagui/tamagui
- **Bento Components:** https://tamagui.dev/bento
- **Takeout Starter:** https://tamagui.dev/takeout
- **Community:** https://discord.gg/4qh6tdcVDa
- **Twitter:** https://twitter.com/tamagui_js

---

## Additional Resources

For comprehensive examples and patterns, explore:

- **Tamagui Kitchen Sink:** https://tamagui.dev/kitchen-sink
- **Bento Component Library:** https://tamagui.dev/bento/showcase
- **Takeout Demo:** https://tamagui.dev/takeout/demo
- **GitHub Discussions:** https://github.com/tamagui/tamagui/discussions

---

**Last Updated:** January 2026  
**Skill Version:** 2.0  
**Generated From:** Official Tamagui documentation (v1.144.0+)
