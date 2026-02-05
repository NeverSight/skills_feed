---
name: nextjs-firebase
description: Comprehensive guide for building Next.js 15.5+ applications with Firebase, including App Router, TypeScript, MUI v7, Turbopack production builds (beta), and Firebase services. Use when configuring Next.js projects, troubleshooting errors, setting up Firebase integration, working with App Router patterns, or implementing best practices for Next.js + Firebase development.
---

# Next.js 15.5+ + Firebase Development Guide

This skill provides comprehensive guidance for building modern Next.js 15.5+ applications with Firebase, TypeScript, Material-UI v7, and Node.js.

## When to Use This Skill

Use this skill when:
- Setting up a new Next.js 15.5+ project with Firebase
- Configuring Next.js with TypeScript, MUI v7, or Turbopack
- Working with Next.js App Router patterns (Server Components, Client Components, routing)
- Integrating Firebase services (Auth, Firestore, Storage, Firebase SDK v12.x)
- Troubleshooting build errors, runtime errors, or deployment issues
- Implementing best practices for Next.js + Firebase projects
- Optimizing performance and build times with Turbopack (beta for production builds)
- Using Node.js Middleware (stable in 15.5)
- Working with typed routes and route props helpers
- Understanding CLI commands and configuration options

## Quick Reference

### Essential Commands

```bash
# Create new project (Next.js 15.5+)
npx create-next-app@latest my-app --typescript --eslint --src-dir --app

# Development
npm run dev              # Start dev server (webpack by default)
npm run dev --turbopack  # Start with Turbopack (faster, optional)
npm run dev -- -p 4000   # Start on custom port

# Type checking & linting
tsc --noEmit            # Check types
npx eslint .            # Run ESLint CLI directly (next lint deprecated in 15.5)

# Generate types for routes (NEW in 15.5)
npx next typegen        # Generate route types without full build

# Build & production
npm run build           # Create production build (webpack - RECOMMENDED)
npm run start           # Start production server
```

**⚠️ Important:** Turbopack production builds (`--turbopack` flag) are in beta and **NOT RECOMMENDED** for production use yet. Use webpack (default) for builds.

### Project Stack

- **Framework:** Next.js 15.5+ with App Router
- **Language:** TypeScript 5.9.3+
- **UI Library:** Material-UI (MUI) v7.3.4+
- **Backend:** Firebase SDK v12.x (Firestore, Auth, Storage, App Hosting)
- **Bundler:** webpack (default, recommended) / Turbopack (optional for dev with --turbopack flag)
- **Runtime:** Node.js ≥22.x (recommended)

## Reference Documentation

The skill includes comprehensive reference documentation. Read these files as needed:

### Core References

- **[cli-commands.md](references/cli-commands.md)** - Complete Next.js CLI reference
  - Read when: Running CLI commands, debugging dev server, configuring ports
  
- **[create-next-app.md](references/create-next-app.md)** - Project initialization guide
  - Read when: Creating new Next.js projects, understanding setup options
  
- **[next-config.md](references/next-config.md)** - Configuration reference
  - Read when: Configuring Next.js, setting up Firebase-specific options, troubleshooting build config
  
- **[typescript.md](references/typescript.md)** - TypeScript integration guide
  - Read when: Setting up TypeScript, using typed routes, configuring type checking
  
- **[turbopack.md](references/turbopack.md)** - Turbopack bundler reference
  - Read when: Enabling Turbopack for dev (optional), understanding Turbopack limitations, troubleshooting bundler issues

### Practice Guides

- **[best-practices.md](references/best-practices.md)** - Comprehensive development guide
  - Read when: Starting a new project, implementing Firebase, working with App Router, setting up MUI
  - Contains: Project structure, Firebase setup, authentication patterns, Firestore patterns, routing patterns
  
- **[troubleshooting.md](references/troubleshooting.md)** - Common errors and solutions
  - Read when: Encountering build errors, runtime errors, TypeScript errors, Firebase errors, deployment issues
  - Contains: Solutions for hydration errors, module not found, Firebase auth errors, MUI setup issues

## Key Workflows

### 1. Starting a New Next.js + Firebase Project

1. **Create project:**
   ```bash
   npx create-next-app@latest my-app \
     --typescript \
     --eslint \
     --src-dir \
     --app \
     --turbopack
   ```

2. **Install Firebase and MUI:**
   ```bash
   npm install firebase  # Firebase SDK v12.x
   npm install @mui/material @mui/icons-material @emotion/react @emotion/styled
   ```

3. **Configure next.config.ts:**
   - Enable React Strict Mode
   - Add MUI packages to transpilePackages
   - Configure images for Firebase Storage
   - See [next-config.md](references/next-config.md) for full configuration

4. **Set up Firebase:**
   - Create Firebase project in console
   - Add web app and get config
   - Create `.env.local` with Firebase credentials
   - Initialize Firebase in `src/lib/firebase/config.ts`
   - See [best-practices.md](references/best-practices.md) for detailed setup

5. **Configure MUI:**
   - Set up ThemeProvider in root layout
   - Add AppRouterCacheProvider
   - Create custom theme
   - See [best-practices.md](references/best-practices.md) for MUI integration

### 2. Working with App Router

**Server Components (default):**
- Fetch data directly in components
- No 'use client' needed
- Can use async/await
- Example: [best-practices.md](references/best-practices.md) - "App Router Patterns"

**Client Components:**
- Add 'use client' directive at top
- Use React hooks (useState, useEffect, etc.)
- Firebase Auth listeners
- Interactive UI elements
- Example: [best-practices.md](references/best-practices.md) - "Client Components"

**Key principle:** Use Server Components by default, only add 'use client' when needed (interactivity, hooks, Firebase Auth).

### 3. Firebase Integration

**Authentication:**
- Use custom `useAuth` hook for auth state
- Implement protected routes with loading states
- Handle auth errors properly
- See [best-practices.md](references/best-practices.md) - "Firebase Authentication Patterns"

**Firestore:**
- Read data in Server Components when possible
- Write data in Client Components
- Use real-time listeners in Client Components
- Implement proper security rules
- See [best-practices.md](references/best-practices.md) - "Firestore Patterns"

### 4. Troubleshooting Common Issues

When encountering errors, follow this process:

1. **Identify error category:**
   - Build error → Check [troubleshooting.md](references/troubleshooting.md) - "Build Errors"
   - Runtime error → Check [troubleshooting.md](references/troubleshooting.md) - "Runtime Errors"
   - TypeScript error → Check [troubleshooting.md](references/troubleshooting.md) - "TypeScript Errors"
   - Firebase error → Check [troubleshooting.md](references/troubleshooting.md) - "Firebase Errors"

2. **Apply common solutions:**
   - Clear cache: `rm -rf .next node_modules && npm install`
   - Check environment variables
   - Verify 'use client' directive placement
   - Ensure proper loading state handling

3. **Enable debug mode if needed:**
   ```bash
   NEXT_DEBUG=1 npm run dev
   ```

### 5. Deployment to Firebase

1. Install Firebase CLI: `npm install -g firebase-tools`
2. Login: `firebase login`
3. Initialize: `firebase init hosting`
4. Configure firebase.json for Next.js
5. Build: `npm run build`
6. Deploy: `firebase deploy --only hosting`

See [best-practices.md](references/best-practices.md) - "Deployment to Firebase" for detailed steps.

## Important Configuration Files

### next.config.ts
Essential for Firebase + MUI setup:
```typescript
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  reactStrictMode: true,
  transpilePackages: [
    '@mui/material',
    '@mui/system',
    '@mui/icons-material',
  ],
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'firebasestorage.googleapis.com',
      },
    ],
  },
}

export default nextConfig
```

### tsconfig.json
Configure path aliases and includes:
```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": [
    "next-env.d.ts",
    ".next/types/**/*.ts",
    "**/*.ts",
    "**/*.tsx"
  ]
}
```

## Best Practices Summary

**Do:**
- ✅ Use TypeScript for type safety
- ✅ Use Server Components by default
- ✅ Handle loading and error states
- ✅ Use environment variables for Firebase config
- ✅ Enable React Strict Mode
- ✅ Use Turbopack for faster development
- ✅ Implement Firebase Security Rules
- ✅ Optimize images with next/image
- ✅ Check if Firebase already initialized

**Don't:**
- ❌ Don't use Firebase Auth in Server Components
- ❌ Don't ignore TypeScript errors in production
- ❌ Don't forget loading states
- ❌ Don't initialize Firebase multiple times
- ❌ Don't create Client Components unnecessarily
- ❌ Don't expose sensitive data in client code

## Progressive Reference Loading

Read reference files progressively based on task needs:

**For setup tasks:**
1. Start with [best-practices.md](references/best-practices.md)
2. Refer to [create-next-app.md](references/create-next-app.md) for initialization
3. Check [next-config.md](references/next-config.md) for configuration

**For development tasks:**
1. Check [best-practices.md](references/best-practices.md) for patterns
2. Refer to [typescript.md](references/typescript.md) for type issues
3. Check [turbopack.md](references/turbopack.md) for bundler features

**For troubleshooting:**
1. Start with [troubleshooting.md](references/troubleshooting.md)
2. Check specific error category
3. Refer to relevant practice guide for correct implementation

**For CLI operations:**
1. Check [cli-commands.md](references/cli-commands.md) for command syntax
2. Refer to examples in [best-practices.md](references/best-practices.md)

## Common Task Quick Guide

| Task | Reference | Section |
|------|-----------|---------|
| Create new project | [create-next-app.md](references/create-next-app.md) | Usage Examples |
| Set up Firebase | [best-practices.md](references/best-practices.md) | Firebase Configuration |
| Configure MUI v7 | [best-practices.md](references/best-practices.md) | Material-UI Integration |
| Fix hydration error | [troubleshooting.md](references/troubleshooting.md) | Runtime Errors |
| Set up auth | [best-practices.md](references/best-practices.md) | Firebase Authentication |
| Configure next.config | [next-config.md](references/next-config.md) | Firebase-Specific Config |
| Enable Turbopack | [turbopack.md](references/turbopack.md) | Getting Started |
| Fix build error | [troubleshooting.md](references/troubleshooting.md) | Build Errors |
| Deploy to Firebase | [best-practices.md](references/best-practices.md) | Deployment to Firebase |

## Notes

- This skill is optimized for Next.js 15.5+ with App Router (not Pages Router)
- All examples use TypeScript (not JavaScript)
- Firebase App Hosting is the deployment target (not Vercel)
- MUI v7.3.4+ is used for UI components
- **webpack is the default and recommended bundler for builds**
- Turbopack can be used for dev with `--turbopack` flag (optional, faster HMR)
- **Turbopack production builds are NOT RECOMMENDED** (beta, unstable)
- Node.js Middleware is now stable (supports full Node.js APIs)
- `next lint` command is deprecated (use ESLint CLI directly)
- `next typegen` command is new in 15.5 (generates types without full build)
- Typed routes are now stable (enables compile-time link validation)
- Firebase SDK v12.x is the current version

## Getting Help

If you encounter issues not covered in the troubleshooting guide:
1. Check Next.js documentation: https://nextjs.org/docs
2. Check Firebase documentation: https://firebase.google.com/docs
3. Search GitHub issues for Next.js and Firebase
4. Enable debug mode: `NEXT_DEBUG=1 npm run dev`
