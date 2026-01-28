---
name: auth-expert
id: auth-expert
version: 2.0.0
description: "Senior expert in Auth.js v5 (NextAuth), Edge-First authentication and security. Optimized for Next.js 16.1.1 and React 19.2."
---

# 🔑 Skill: auth-expert (v2.0.0)

## 🌟 Overview & Vision 2026
This skill provides a deep-dive into **Auth.js v5**, the successor to NextAuth.js. It is specifically optimized for the **Next.js 16.1.1** App Router, **React 19.2** Server Actions, and **Edge Runtime** constraints. 

In 2026, authentication is no longer just about a login form; it's about a unified session architecture that works across Server Components, Client Components, Middleware, and Server Actions without performance trade-offs.

---

## 📚 Table of Contents
1. [Core Architecture: The Dual-Config Pattern](#core-architecture-the-dual-config-pattern)
2. [Quick Start: The 5-Minute Setup](#quick-start-the-5-minute-setup)
3. [Universal Auth: The `auth()` Protocol](#universal-auth-the-auth-protocol)
4. [Route Protection & Middleware](#route-protection--middleware)
5. [React 19 Server Actions & Authentication](#react-19-server-actions--authentication)
6. [The "Do Not" List (Common Pitfalls)](#the-do-not-list-common-pitfalls)
7. [Security Hardening Checklist](#security-hardening-checklist)
8. [Advanced Patterns: Types & Extensibility](#advanced-patterns-types--extensibility)
9. [Deep Dives (References)](#deep-dives-references)

---

## 🏗️ Core Architecture: The Dual-Config Pattern
To avoid "Module not found" errors in the Edge Runtime (Middleware), Auth.js v5 requires a split configuration.

### 1. Edge-Compatible Logic (`auth.config.ts`)
This file contains only logic that can run on the Edge. **Never import database adapters or heavy Node.js libraries here.**

```typescript
import type { NextAuthConfig } from "next-auth";
import GitHub from "next-auth/providers/github";

// This is the base config for Middleware and Edge functions
export const authConfig = {
  providers: [
    GitHub({
      clientId: process.env.AUTH_GITHUB_ID,
      clientSecret: process.env.AUTH_GITHUB_SECRET,
    }),
  ],
  callbacks: {
    authorized({ auth, request: { nextUrl } }) {
      const isLoggedIn = !!auth?.user;
      const isOnDashboard = nextUrl.pathname.startsWith("/dashboard");
      
      if (isOnDashboard) {
        if (isLoggedIn) return true;
        return false; // Redirect unauthenticated users to login
      }
      return true;
    },
  },
} satisfies NextAuthConfig;
```

### 2. Full Logic (`auth.ts`)
This file imports `authConfig` and adds the database adapter (Node.js runtime).

```typescript
import NextAuth from "next-auth";
import { PrismaAdapter } from "@auth/prisma-adapter";
import { prisma } from "@/lib/db"; // Your Prisma client
import { authConfig } from "./auth.config";

export const { 
  handlers, 
  auth, 
  signIn, 
  signOut,
  update // Used to update the session manually
} = NextAuth({
  adapter: PrismaAdapter(prisma),
  session: { strategy: "jwt" }, // JWT is mandatory for Edge compatibility
  ...authConfig,
});
```

---

## ⚡ Quick Start: The 5-Minute Setup

### Step 1: Install Dependencies
```bash
bun add next-auth@beta @auth/prisma-adapter
```

### Step 2: Configure Environment Variables
```env
# Generate with: npx auth secret
AUTH_SECRET=your_ultra_secure_secret_here

# Provider Credentials
AUTH_GITHUB_ID=...
AUTH_GITHUB_SECRET=...
```

### Step 3: Create the Route Handler
`app/api/auth/[...nextauth]/route.ts`
```typescript
import { handlers } from "@/auth";
export const { GET, POST } = handlers;
```

---

## 🌍 Universal Auth: The `auth()` Protocol
One of the most powerful features of v5 is the universal `auth()` function. It works everywhere.

### 1. In Server Components (RSC)
```tsx
import { auth } from "@/auth";

export default async function ProfilePage() {
  const session = await auth();
  
  if (!session) {
    return <div>Not logged in.</div>;
  }

  return (
    <div>
      <h1>Welcome, {session.user?.name}</h1>
      <p>Role: {session.user?.role}</p>
    </div>
  );
}
```

### 2. In Server Actions
```typescript
"use server"
import { auth } from "@/auth";

export async function createPost(content: string) {
  const session = await auth();
  if (!session) throw new Error("Unauthorized");

  // Securely access user data
  const authorId = session.user.id;
  // ... database logic
}
```

### 3. In Client Components
Use the `useSession` hook from `next-auth/react`. **Note**: You must wrap your app in `<SessionProvider>`.

```tsx
"use client"
import { useSession } from "next-auth/react";

export function UserButton() {
  const { data: session, status } = useSession();

  if (status === "loading") return <div>...</div>;
  if (!session) return <button>Login</button>;

  return <img src={session.user.image} alt="Avatar" />;
}
```

---

## 🛡️ Route Protection & Middleware
The `middleware.ts` file is the first line of defense.

```typescript
import NextAuth from "next-auth";
import { authConfig } from "./auth.config";

export default NextAuth(authConfig).auth;

export const config = {
  // Matcher allows excluding static files and api routes if needed
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};
```

---

## 🧪 React 19 Server Actions & Authentication
React 19 introduces improved handling for forms and transitions. Use them for your login flows.

### Login Action Example
```typescript
"use server"
import { signIn } from "@/auth";
import { AuthError } from "next-auth";

export async function authenticate(
  prevState: string | undefined,
  formData: FormData,
) {
  try {
    await signIn("credentials", formData);
  } catch (error) {
    if (error instanceof AuthError) {
      switch (error.type) {
        case "CredentialsSignin":
          return "Invalid credentials.";
        default:
          return "Something went wrong.";
      }
    }
    throw error;
  }
}
```

---

## 🚫 The "Do Not" List (Common Pitfalls)

| Pitfall | Why it's bad | Solution |
| :--- | :--- | :--- |
| **Using `getServerSession`** | v4 legacy, slower in v5. | Use `auth()`. |
| **`NEXTAUTH_URL`** | Deprecated in v5. | Use `AUTH_URL` or let it auto-detect. |
| **Prisma in Middleware** | Middleware runs on Edge; Prisma needs Node. | Use split config pattern. |
| **Client-side only checks** | Easily bypassed by disabling JS. | Always verify session on server. |
| **Storing Secrets in Client** | Security breach. | Keep all secrets in `.env.local`. |
| **Ignoring CSRF** | Vulnerable to cross-site attacks. | Use built-in handlers and Actions. |

---

## 🏁 Security Hardening Checklist
- [ ] **Rotate Secrets**: Ensure `AUTH_SECRET` is rotated periodically.
- [ ] **Secure Cookies**: In production, cookies are automatically secure, but verify `trustHost`.
- [ ] **Role Validation**: Don't just check `!!session`, check `session.user.role === 'admin'`.
- [ ] **Rate Limiting**: Apply rate limiting to `app/api/auth` endpoints.
- [ ] **HTTPS Only**: Ensure your site is served over HTTPS to protect session cookies.

---

## 🔧 Advanced Patterns: Types & Extensibility
Extending the session object is a common requirement.

### `next-auth.d.ts`
```typescript
import { type DefaultSession } from "next-auth";

export type ExtendedUser = DefaultSession["user"] & {
  role: "ADMIN" | "USER";
  id: string;
};

declare module "next-auth" {
  interface Session {
    user: ExtendedUser;
  }
}
```

### Callback Logic for Roles
```typescript
callbacks: {
  async session({ token, session }) {
    if (token.sub && session.user) {
      session.user.id = token.sub;
    }
    if (token.role && session.user) {
      session.user.role = token.role as "ADMIN" | "USER";
    }
    return session;
  },
  async jwt({ token }) {
    if (!token.sub) return token;
    
    const existingUser = await getUserById(token.sub);
    if (!existingUser) return token;

    token.role = existingUser.role;
    return token;
  }
}
```

---

## 📖 Deep Dives (References)
For more complex scenarios, consult the following specialized guides:
- [Edge Compatibility & Runtimes](./references/edge-compatibility.md)
- [Advanced Providers & Custom Logic](./references/advanced-providers.md)
- [Security Best Practices](./references/security-best-practices.md)

---

## 🛠️ Troubleshooting

### "JWT expired" or "Invalid Signature"
Check if your `AUTH_SECRET` matches across all environments. If you changed it, all current sessions will be invalidated.

### "Redirect recursion"
This usually happens when your `middleware.ts` logic redirects to `/login` but doesn't exclude `/login` from the middleware matcher or the `authorized` check.

---
## 🗄️ Advanced Database Integration: Custom Schemas
When using Prisma or Drizzle, you might need to customize the table names or add extra fields.

### Prisma Schema Example
```prisma
// schema.prisma
model User {
  id            String    @id @default(cuid())
  name          String?
  email         String?   @unique
  emailVerified DateTime?
  image         String?
  role          UserRole  @default(USER)
  accounts      Account[]
  sessions      Session[]
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt
}

enum UserRole {
  ADMIN
  USER
}

model Account {
  id                 String  @id @default(cuid())
  userId             String
  type               String
  provider           String
  providerAccountId  String
  refresh_token      String? @db.Text
  access_token       String? @db.Text
  expires_at         Int?
  token_type         String?
  scope              String?
  id_token           String? @db.Text
  session_state      String?

  user User @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@unique([provider, providerAccountId])
}
```

### Drizzle Schema Example
```typescript
import {
  timestamp,
  pgTable,
  text,
  primaryKey,
  integer,
} from "drizzle-orm/pg-core"
import type { AdapterAccount } from '@auth/core/adapters'

export const users = pgTable("user", {
  id: text("id").notNull().primaryKey(),
  name: text("name"),
  email: text("email").notNull(),
  emailVerified: timestamp("emailVerified", { mode: "date" }),
  image: text("image"),
})

export const accounts = pgTable(
  "account",
  {
    userId: text("userId")
      .notNull()
      .references(() => users.id, { onDelete: "cascade" }),
    type: text("type").$type<AdapterAccount["type"]>().notNull(),
    provider: text("provider").notNull(),
    providerAccountId: text("providerAccountId").notNull(),
    refresh_token: text("refresh_token"),
    access_token: text("access_token"),
    expires_at: integer("expires_at"),
    token_type: text("token_type"),
    scope: text("scope"),
    id_token: text("id_token"),
    session_state: text("session_state"),
  },
  (account) => ({
    compoundKey: primaryKey({ columns: [account.provider, account.providerAccountId] }),
  })
)
```

---

## 🌐 Internationalization (i18n) & Authentication
Handling redirects and error messages in multiple languages.

### i18n-Aware Redirects
If you are using `next-intl` or a similar library, your auth logic should respect the current locale.

```typescript
// auth.config.ts
callbacks: {
  authorized({ auth, request: { nextUrl } }) {
    const locale = nextUrl.pathname.split('/')[1] || 'en';
    const isLoggedIn = !!auth?.user;
    
    if (nextUrl.pathname.startsWith(`/${locale}/dashboard`) && !isLoggedIn) {
      return Response.redirect(new URL(`/${locale}/login`, nextUrl));
    }
    return true;
  }
}
```

---

## 🛡️ Multi-Factor Authentication (MFA) in 2026
While Auth.js doesn't have a "one-click" MFA, you can implement it using the `callbacks` and a custom session state.

### Implementation Strategy
1.  **First Factor**: Standard login (OAuth/Credentials).
2.  **MFA Check**: After login, check if MFA is enabled for the user.
3.  **Temporary Session**: If MFA is required, mark the JWT as `mfa_pending: true`.
4.  **Verification**: Redirect to a `/verify-mfa` page.
5.  **Finalize**: Once verified, update the JWT to `mfa_verified: true`.

```typescript
// Example JWT Callback for MFA
async jwt({ token, user }) {
  if (user) {
    token.mfa_required = user.hasMfa;
    token.mfa_verified = false;
  }
  return token;
}

// In Middleware
if (token?.mfa_required && !token?.mfa_verified && pathname !== "/verify-mfa") {
  return Response.redirect(new URL("/verify-mfa", nextUrl));
}
```

---

## 🧪 Testing Authentication
Testing auth flows is critical for preventing regressions.

### 1. Integration Testing with Vitest
Mock the `auth` function to test protected components.

```typescript
import { vi, test, expect } from 'vitest';
import { auth } from '@/auth';

vi.mock('@/auth', () => ({
  auth: vi.fn(),
}));

test('shows secret content to logged-in users', async () => {
  (auth as any).mockResolvedValue({ user: { name: 'Test User' } });
  // Render component and assert
});
```

### 2. E2E Testing with Playwright
Use a dedicated test user and the `storageState` feature to stay logged in across tests.

```typescript
import { test, expect } from '@playwright/test';

test('can access dashboard after login', async ({ page }) => {
  await page.goto('/login');
  await page.fill('input[name="email"]', 'test@example.com');
  await page.fill('input[name="password"]', 'password');
  await page.click('button[type="submit"]');
  
  await expect(page).toHaveURL('/dashboard');
});
```

---

## 🔗 External Resources
- [Official Auth.js v5 Documentation](https://authjs.dev)
- [Auth.js GitHub Repository](https://github.com/nextauthjs/next-auth)
- [Prisma Adapter Documentation](https://authjs.dev/reference/adapter/prisma)

---

## 📜 Complete Implementation Example (The "Gold Standard")

### `auth.config.ts`
```typescript
import type { NextAuthConfig } from "next-auth";
import GitHub from "next-auth/providers/github";
import Credentials from "next-auth/providers/credentials";

export const authConfig = {
  providers: [
    GitHub,
    Credentials({
      async authorize(credentials) {
        // Validation logic here
        return null; 
      }
    })
  ],
  callbacks: {
    authorized({ auth, request: { nextUrl } }) {
      // Logic here
      return true;
    }
  }
} satisfies NextAuthConfig;
```

### `auth.ts`
```typescript
import NextAuth from "next-auth";
import { DrizzleAdapter } from "@auth/drizzle-adapter";
import { db } from "@/db";
import { authConfig } from "./auth.config";

export const { auth, handlers, signIn, signOut } = NextAuth({
  adapter: DrizzleAdapter(db),
  session: { strategy: "jwt" },
  ...authConfig,
});
```

### `middleware.ts`
```typescript
import NextAuth from "next-auth";
import { authConfig } from "./auth.config";

export default NextAuth(authConfig).auth;

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};
```

---

*Updated: January 22, 2026 - 15:18*
