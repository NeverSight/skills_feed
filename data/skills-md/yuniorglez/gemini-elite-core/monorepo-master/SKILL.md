---
name: monorepo-master
description: Senior Monorepo Architect & Platform Engineer for 2026. Master of high-scale Turborepo orchestration, Bun-first workspace management, and Next.js 16/Tailwind 4 modular architectures. Expert in resolving complex dependency graphs, optimizing remote caching, and implementing Zero-Trust CI/CD pipelines for large-scale engineering teams.
---

# 🏗️ Skill: monorepo-master (v1.0.0)

## Executive Summary
Senior Monorepo Architect & Platform Engineer for 2026. Master of high-scale Turborepo orchestration, Bun-first workspace management, and Next.js 16/Tailwind 4 modular architectures. Expert in resolving complex dependency graphs, optimizing remote caching, and implementing Zero-Trust CI/CD pipelines for large-scale engineering teams.

---

## 📋 The Conductor's Protocol

1.  **Topology Assessment**: Analyze the monorepo structure (Nested vs. Flat) and determine the optimal workspace boundaries (apps, packages, tools).
2.  **Package Manager Selection**: Default to **Bun v1.2+** for 2026. If legacy requirements exist, use `pnpm` with strict hoisting.
3.  **Sequential Activation**:
    `activate_skill(name="monorepo-master")` → `activate_skill(name="next16-expert")` → `activate_skill(name="tailwind4-expert")` → `activate_skill(name="github-actions-pro")`.
4.  **Verification**: Execute `bun x turbo run build --dry-run` to verify the task graph and cache hits before committing.

---

## 🛠️ Mandatory Protocols (2026 Standards)

### 1. Bun-First Workspace Management
As of 2026, Bun is the production standard for monorepos due to its sub-millisecond module resolution and integrated test runner.
- **Rule**: Never use `npm install` or `yarn`. Use `bun install` with `bun.lockb` for deterministic builds.
- **Protocol**: Define workspaces in the root `package.json` using the `"workspaces": ["apps/*", "packages/*"]` pattern.

### 2. Turborepo 2.5+ Orchestration
- **Task Graph**: Define strict `dependsOn` relationships in `turbo.json`. Always ensure `^build` (upstream build) is required for app builds.
- **Remote Caching**: Always configure a Remote Cache (Vercel or custom S3-based) to ensure sub-5s CI times.
- **Persistent Tasks**: Use the `cache: false` and `persistent: true` flags for dev servers to prevent cache poisoning.

### 3. Tailwind CSS 4 (CSS-First) Architecture
In 2026 monorepos, Tailwind 4 configuration lives in CSS, not JS.
- **Shared Config**: Create a `packages/tailwind-config` containing a `base.css` with `@theme` blocks.
- **Import Pattern**: Apps should `@import "@repo/tailwind-config/base.css"` and extend as needed.
- **Direct Ref**: Ensure shared UI packages (e.g., `@repo/ui`) use React 19 direct `ref` props and Tailwind 4 container queries.

### 4. Next.js 16 & React 19 Integration
- **Internal Packages**: Use `transpilePackages` in `next.config.ts` for shared UI/logic packages.
- **Proxy Paradigms**: Leverage Next.js 16's internal proxying for cross-app communication in a monorepo.
- **Type Safety**: Use `workspace:*` for internal dependencies to ensure TypeScript always resolves to the latest source code, not stale builds.

---

## 🚀 Show, Don't Just Tell (Implementation Patterns)

### Modern `turbo.json` (2026 Optimized)
```json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": [".env", "tsconfig.json"],
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": [".next/**", "dist/**"]
    },
    "lint": {
      "dependsOn": ["^lint"]
    },
    "test": {
      "dependsOn": ["^build"],
      "outputs": ["coverage/**"],
      "inputs": ["src/**/*.ts", "src/**/*.tsx", "test/**/*.ts"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "type-check": {
      "cache": true
    }
  }
}
```

### Shared UI Package Structure (Tailwind 4 + React 19)
`packages/ui/src/button.tsx`:
```tsx
import * as React from "react";

// React 19: No more forwardRef!
export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary";
}

export function Button({ className, variant = "primary", ...props }: ButtonProps) {
  return (
    <button
      // Tailwind 4: Native container queries and CSS-first variables
      className={`rounded-lg px-4 py-2 transition-all @container ${
        variant === "primary" ? "bg-primary text-white" : "bg-secondary"
      } ${className}`}
      {...props}
    />
  );
}
```

`packages/ui/package.json`:
```json
{
  "name": "@repo/ui",
  "version": "0.0.0",
  "exports": {
    ".": "./src/index.ts",
    "./styles.css": "./src/styles.css"
  },
  "peerDependencies": {
    "react": "^19.0.0",
    "tailwindcss": "^4.0.0"
  }
}
```

---

## 🛡️ The Do Not List (Anti-Patterns)

1.  **DO NOT** use relative paths (e.g., `../../packages/ui`) for imports. Always use the workspace name (`@repo/ui`).
2.  **DO NOT** commit `node_modules`. Ensure your `.gitignore` is correctly configured at the root.
3.  **DO NOT** publish internal packages to npm. Use `private: true` and `workspace:*` versions.
4.  **DO NOT** mix package managers. If the repo uses Bun, every developer and CI job must use Bun.
5.  **DO NOT** ignore `turbo.json` inputs. Missing inputs cause false cache hits (stale builds).

---

## 📂 Progressive Disclosure (Deep Dives)

- **[Dependency Management & Hoisting](./references/dependencies.md)**: Solving "Ghost Dependencies" and Bun's resolution logic.
- **[Turborepo Task Orchestration](./references/turbo-deep-dive.md)**: Advanced pipeline configurations and global hashes.
- **[Tailwind 4 Monorepo Strategy](./references/tailwind-4-strategy.md)**: CSS-First themes and cross-package scanning.
- **[CI/CD with Hardened Runners](./references/cicd-automation.md)**: OIDC, Bun cache actions, and change-aware testing.

---

## 🛠️ Specialized Tools & Scripts

- `scripts/monorepo-doctor.sh`: Analyzes the monorepo for dependency mismatches and circular references.
- `scripts/scaffold-package.ts`: Scaffolds a new package with 2026 standards (Bun, Tailwind 4, TSConfig).

---

## 🎓 Learning Resources
- [Turborepo Documentation](https://turbo.build/repo/docs)
- [Bun Workspaces Guide](https://bun.sh/docs/install/workspaces)
- [Next.js Monorepo Best Practices](https://nextjs.org/docs/app/building-your-application/configuring/monorepos)

---
*Updated: January 23, 2026 - 18:15*
