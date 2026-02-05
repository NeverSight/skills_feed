---
name: neon-js-react
description: Sets up the full Neon SDK with authentication AND database queries in React apps (Vite, CRA). Creates typed client, generates database types, and configures auth UI. Use for auth + database integration.
allowed-tools: ["Bash", "Write", "Read", "Edit", "Glob", "Grep"]
---

# Neon JS for React

Help developers set up @neondatabase/neon-js with authentication AND database queries in React applications (Vite, CRA, etc.).

## When to Use

Use this skill when:
- Setting up Neon Auth + Database in a React app (Vite, CRA, etc.)
- User needs both authentication AND database queries
- User mentions "neon-js", "neon auth + database", or "full neon SDK"
- User is NOT using Next.js (for Next.js, use `neon-auth-nextjs` as a starting point and add Data API configuration, or see `examples/nextjs-neon-auth/`)

## Critical Rules

1. **Adapter Factory Pattern**: Always call adapters with `()`
   ```typescript
   adapter: SupabaseAuthAdapter()  // Correct
   adapter: SupabaseAuthAdapter    // Wrong - missing ()
   ```

2. **React Adapter Import**: NOT exported from main - use subpath
   ```typescript
   import { BetterAuthReactAdapter } from '@neondatabase/neon-js/auth/react/adapters';
   ```

3. **Type Safety**: Always use Database generic for type-safe queries
   ```typescript
   const client = createClient<Database>({...});
   ```

4. **CSS Import**: Choose ONE - either `/ui/css` OR `/ui/tailwind`, never both

---

## Setup

### 1. Install
```bash
npm install @neondatabase/neon-js
```

### 2. Generate Database Types
```bash
npx neon-js gen-types --db-url "postgresql://user:pass@host:5432/db" --output src/database.types.ts
```

**CLI Options:**
```bash
npx neon-js gen-types --db-url <url> [options]

# Required
--db-url <url>              Database connection string

# Optional
--output, -o <path>         Output file (default: database.types.ts)
--schema, -s <name>         Schema to include (repeatable, default: public)
--postgrest-v9-compat       Disable one-to-one relationship detection
--query-timeout <duration>  Query timeout (e.g., 30s, 1m, default: 15s)
```

### 3. Create Client (`src/client.ts`)
```typescript
import { createClient } from '@neondatabase/neon-js';
import type { Database } from './database.types';

export const neonClient = createClient<Database>({
  auth: {
    url: import.meta.env.VITE_NEON_AUTH_URL,
    // allowAnonymous: true, // Enable for RLS access without login
  },
  dataApi: {
    url: import.meta.env.VITE_NEON_DATA_API_URL,
  },
});
```

### 4. Create Provider (`src/providers.tsx`)
```typescript
import { NeonAuthUIProvider } from '@neondatabase/neon-js/auth/react';
import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom';
import { neonClient } from './client';

// Import CSS (choose one)
import '@neondatabase/neon-js/ui/css';

export function Providers({ children }: { children: React.ReactNode }) {
  const navigate = useNavigate();

  return (
    <NeonAuthUIProvider
      authClient={neonClient.auth}
      navigate={navigate}
      redirectTo="/dashboard"
      Link={({href, children}) => <Link to={href}>{children}</Link>}
    >
      {children}
    </NeonAuthUIProvider>
  );
}
```

### 5. Wrap App (`src/main.tsx`)
```typescript
import { BrowserRouter } from 'react-router-dom';
import { Providers } from './providers';
import App from './App';

createRoot(document.getElementById('root')!).render(
  <BrowserRouter>
    <Providers>
      <App />
    </Providers>
  </BrowserRouter>
);
```

### 6. Environment Variables (`.env.local`)
```
VITE_NEON_AUTH_URL=https://your-auth.neon.tech
VITE_NEON_DATA_API_URL=https://your-data-api.neon.tech/rest/v1
```

---

## CSS & Styling

### Import Options

**Without Tailwind** (pre-built CSS bundle ~47KB):
```typescript
// In provider or main.tsx
import '@neondatabase/neon-js/ui/css';
```

**With Tailwind CSS v4**:
```css
@import 'tailwindcss';
@import '@neondatabase/neon-js/ui/tailwind';
```

**IMPORTANT**: Never import both - causes duplicate styles.

### Dark Mode

```typescript
<NeonAuthUIProvider
  defaultTheme="system" // 'light' | 'dark' | 'system'
  // ...
>
```

### Custom Theming

Override CSS variables in your stylesheet:
```css
:root {
  --primary: oklch(0.7 0.15 250);
  --primary-foreground: oklch(0.98 0 0);
  --background: oklch(1 0 0);
  --foreground: oklch(0.1 0 0);
  --card: oklch(1 0 0);
  --border: oklch(0.9 0 0);
  --radius: 0.5rem;
}

.dark {
  --background: oklch(0.15 0 0);
  --foreground: oklch(0.98 0 0);
}
```

---

## NeonAuthUIProvider Props

Full configuration:

```typescript
<NeonAuthUIProvider
  // Required
  authClient={neonClient.auth}  // Note: .auth property of neonClient

  // Navigation
  navigate={navigate}
  Link={({href, children}) => <Link to={href}>{children}</Link>}
  redirectTo="/dashboard"

  // Social/OAuth
  social={{
    providers: ['google'],
  }}

  // Feature Flags
  emailOTP={true}
  emailVerification={true}
  magicLink={false}
  multiSession={false}
  credentials={{ forgotPassword: true }}

  // Sign Up Fields
  signUp={{ fields: ['name'] }}

  // Account Fields
  account={{ fields: ['image', 'name', 'company'] }}

  // Organizations
  organization={{}}

  // Dark Mode
  defaultTheme="system"

  // Custom Labels
  localization={{
    SIGN_IN: 'Welcome Back',
    SIGN_UP: 'Create Account',
  }}
>
  {children}
</NeonAuthUIProvider>
```

---

## Database Queries

### Select

```typescript
// Basic select
const { data, error } = await neonClient
  .from('todos')
  .select('*');

// Select with filter
const { data, error } = await neonClient
  .from('todos')
  .select('*')
  .eq('user_id', userId)
  .order('created_at', { ascending: false });

// Select with relations
const { data, error } = await neonClient
  .from('posts')
  .select(`
    *,
    author:users(name, avatar),
    comments(id, content)
  `);

// Single row
const { data, error } = await neonClient
  .from('todos')
  .select('*')
  .eq('id', todoId)
  .single();
```

### Insert

```typescript
// Single insert
const { data, error } = await neonClient
  .from('todos')
  .insert({ title: 'New todo', user_id: userId })
  .select()
  .single();

// Bulk insert
const { data, error } = await neonClient
  .from('todos')
  .insert([
    { title: 'Todo 1', user_id: userId },
    { title: 'Todo 2', user_id: userId },
  ])
  .select();
```

### Update

```typescript
const { data, error } = await neonClient
  .from('todos')
  .update({ completed: true })
  .eq('id', todoId)
  .select()
  .single();
```

### Delete

```typescript
const { error } = await neonClient
  .from('todos')
  .delete()
  .eq('id', todoId);
```

### Upsert

```typescript
const { data, error } = await neonClient
  .from('profiles')
  .upsert({ user_id: userId, bio: 'Updated bio' })
  .select()
  .single();
```

### Filters

```typescript
// Equality
.eq('column', value)
.neq('column', value)

// Comparison
.gt('column', value)      // greater than
.gte('column', value)     // greater than or equal
.lt('column', value)      // less than
.lte('column', value)     // less than or equal

// Pattern matching
.like('column', '%pattern%')
.ilike('column', '%pattern%')  // case insensitive

// Arrays
.in('column', [1, 2, 3])
.contains('tags', ['javascript'])
.containedBy('tags', ['javascript', 'typescript'])

// Null
.is('column', null)
.not('column', 'is', null)

// Range
.range(0, 9)  // pagination
```

### Ordering & Pagination

```typescript
const { data, error } = await neonClient
  .from('posts')
  .select('*')
  .order('created_at', { ascending: false })
  .range(0, 9)  // First 10 items
  .limit(10);
```

---

## Auth Methods

### Default API (BetterAuth)

```typescript
// Sign up
await neonClient.auth.signUp.email({ email, password, name });

// Sign in
await neonClient.auth.signIn.email({ email, password });

// OAuth
await neonClient.auth.signIn.social({
  provider: 'google',
  callbackURL: '/dashboard',
});

// Get session
const session = await neonClient.auth.getSession();

// Sign out
await neonClient.auth.signOut();
```

### With SupabaseAuthAdapter

```typescript
import { createClient, SupabaseAuthAdapter } from '@neondatabase/neon-js';

const neonClient = createClient<Database>({
  auth: {
    url: import.meta.env.VITE_NEON_AUTH_URL,
    adapter: SupabaseAuthAdapter(),
  },
  dataApi: {
    url: import.meta.env.VITE_NEON_DATA_API_URL,
  },
});

// Supabase-style methods
await neonClient.auth.signUp({ email, password, options: { data: { name } } });
await neonClient.auth.signInWithPassword({ email, password });
await neonClient.auth.signInWithOAuth({ provider: 'google', options: { redirectTo } });
const { data: session } = await neonClient.auth.getSession();
await neonClient.auth.signOut();

// Event listener
neonClient.auth.onAuthStateChange((event, session) => {
  console.log(event); // 'SIGNED_IN', 'SIGNED_OUT', 'TOKEN_REFRESHED'
});
```

### With BetterAuthReactAdapter

```typescript
import { createClient } from '@neondatabase/neon-js';
import { BetterAuthReactAdapter } from '@neondatabase/neon-js/auth/react/adapters';

const neonClient = createClient<Database>({
  auth: {
    url: import.meta.env.VITE_NEON_AUTH_URL,
    adapter: BetterAuthReactAdapter(),
  },
  dataApi: {
    url: import.meta.env.VITE_NEON_DATA_API_URL,
  },
});

// Includes useSession() hook
const { data, isPending, error } = neonClient.auth.useSession();
```

---

## Session Hook

```typescript
function MyComponent() {
  const { data: session, isPending, error, refetch } = neonClient.auth.useSession();

  if (isPending) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  if (!session) return <div>Not signed in</div>;

  return (
    <div>
      <p>Hello, {session.user.name}</p>
      <p>Email: {session.user.email}</p>
    </div>
  );
}
```

**Session shape:**
```typescript
{
  user: {
    id: string;
    email: string;
    name: string;
    image?: string;
    emailVerified: boolean;
  };
  session: {
    id: string;
    token: string;
    expiresAt: Date;
  };
}
```

---

## UI Components

### AuthView - Main Auth Interface

```typescript
import { AuthView } from '@neondatabase/neon-js/auth/react';

// Route: /auth/:pathname
function AuthPage() {
  const { pathname } = useParams();
  return <AuthView pathname={pathname} />;
}
```

**Pathnames**: `sign-in`, `sign-up`, `forgot-password`, `reset-password`, `callback`, `sign-out`

### Conditional Rendering

```typescript
import {
  SignedIn,
  SignedOut,
  AuthLoading,
  RedirectToSignIn,
} from '@neondatabase/neon-js/auth/react';

function MyPage() {
  return (
    <>
      <AuthLoading>
        <LoadingSpinner />
      </AuthLoading>

      <SignedIn>
        <Dashboard />
      </SignedIn>

      <SignedOut>
        <LandingPage />
      </SignedOut>

      <RedirectToSignIn />
    </>
  );
}
```

### UserButton

```typescript
import { UserButton } from '@neondatabase/neon-js/auth/react';

function Header() {
  return (
    <header>
      <UserButton />
    </header>
  );
}
```

### Account Management

```typescript
import {
  AccountSettingsCards,
  SecuritySettingsCards,
  SessionsCard,
  ChangePasswordCard,
  ChangeEmailCard,
  DeleteAccountCard,
  ProvidersCard,
} from '@neondatabase/neon-js/auth/react';
```

### Organization Components

```typescript
import {
  OrganizationSwitcher,
  OrganizationSettingsCards,
  OrganizationMembersCard,
} from '@neondatabase/neon-js/auth/react';
```

---

## Social/OAuth Providers

### Configuration

```typescript
<NeonAuthUIProvider
  social={{
    providers: ['google'],
  }}
>
```

### Programmatic Sign-In

```typescript
await neonClient.auth.signIn.social({
  provider: 'google',
  callbackURL: '/dashboard',
});
```

### Supported Providers

`google`, `github`, `twitter`, `discord`, `apple`, `microsoft`, `facebook`, `linkedin`, `spotify`, `twitch`, `gitlab`, `bitbucket`

---

## Protected Routes

```typescript
// routes.tsx
import { Routes, Route } from 'react-router-dom';

export function AppRoutes() {
  return (
    <Routes>
      {/* Public */}
      <Route path="/" element={<HomePage />} />

      {/* Auth */}
      <Route path="/auth/:pathname" element={<AuthPage />} />

      {/* Protected */}
      <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
      <Route path="/account/:view?" element={<ProtectedRoute><AccountPage /></ProtectedRoute>} />
    </Routes>
  );
}

// ProtectedRoute.tsx
function ProtectedRoute({ children }: { children: React.ReactNode }) {
  return (
    <>
      <AuthLoading><LoadingSpinner /></AuthLoading>
      <RedirectToSignIn />
      <SignedIn>{children}</SignedIn>
    </>
  );
}
```

---

## Advanced Features

### Anonymous Access

Enable RLS-based data access for unauthenticated users:

```typescript
const neonClient = createClient<Database>({
  auth: {
    url: import.meta.env.VITE_NEON_AUTH_URL,
    allowAnonymous: true,
  },
  dataApi: {
    url: import.meta.env.VITE_NEON_DATA_API_URL,
  },
});

// Queries work without sign-in (using anonymous JWT)
const { data } = await neonClient.from('public_posts').select('*');
```

### Get JWT Token

```typescript
const token = await neonClient.auth.getJWTToken();

// Use for external API calls
const response = await fetch('/api/external', {
  headers: { Authorization: `Bearer ${token}` },
});
```

### Identity Linking

```typescript
// List linked accounts
const { data } = await neonClient.auth.getUserIdentities();

// Link new provider
await neonClient.auth.linkIdentity({
  provider: 'github',
  options: { redirectTo: '/account/security' },
});

// Unlink provider
await neonClient.auth.unlinkIdentity({ identity_id: 'id' });
```

### Auth State Events (Supabase Adapter)

```typescript
const { data: { subscription } } = neonClient.auth.onAuthStateChange((event, session) => {
  switch (event) {
    case 'SIGNED_IN': /* ... */ break;
    case 'SIGNED_OUT': /* ... */ break;
    case 'TOKEN_REFRESHED': /* ... */ break;
    case 'USER_UPDATED': /* ... */ break;
  }
});

// Cleanup
subscription.unsubscribe();
```

### Cross-Tab Sync

Automatic via BroadcastChannel. Sign out in one tab signs out all tabs.

---

## Error Handling

### Query Errors

```typescript
const { data, error } = await neonClient.from('todos').select('*');

if (error) {
  console.error('Query failed:', error.message);
  return;
}

// Use data safely
console.log(data);
```

### Auth Errors

```typescript
const { error } = await neonClient.auth.signIn.email({ email, password });

if (error) {
  toast.error(error.message);
  return;
}
```

### Common Errors

| Error | Cause |
|-------|-------|
| `Invalid credentials` | Wrong email/password |
| `User already exists` | Email registered |
| `permission denied for table` | Missing RLS policy or GRANT |
| `JWT expired` | Token needs refresh |

---

## FAQ / Troubleshooting

### Anonymous access not working?

Grant permissions to the `anonymous` role in your database:

```sql
-- Grant SELECT on specific tables
GRANT SELECT ON public.posts TO anonymous;
GRANT SELECT ON public.products TO anonymous;

-- RLS policy for anonymous access
CREATE POLICY "Anyone can read published posts"
  ON public.posts FOR SELECT
  USING (published = true);
```

### "permission denied for table" error?

1. Check RLS is enabled: `ALTER TABLE posts ENABLE ROW LEVEL SECURITY;`
2. Create appropriate policies for authenticated users
3. Grant permissions: `GRANT SELECT, INSERT ON public.posts TO authenticated;`

### Database types out of date?

Regenerate types after schema changes:

```bash
npx neon-js gen-types --db-url "postgresql://..." --output src/database.types.ts
```

### OAuth not working in iframe?

OAuth automatically uses popup flow in iframes. Ensure popups aren't blocked.

### Session not persisting?

1. Cookies enabled?
2. Auth URL correct in `.env.local`?
3. Not in incognito with cookies blocked?

---

## Performance Notes

- **Session caching**: 60-second TTL
- **Request deduplication**: Concurrent calls share single request
- **Auto token injection**: JWT automatically added to all queries
- **Cross-tab sync**: <50ms via BroadcastChannel
