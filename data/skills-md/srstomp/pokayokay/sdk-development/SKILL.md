---
name: sdk-development
description: Create, extract, and publish TypeScript SDKs. Covers analyzing existing applications to extract reusable logic, designing clean SDK APIs, implementing typed clients with proper error handling, bundling for multiple targets (ESM/CJS/browser), and publishing to npm (public or private registries). Use this skill when building SDKs, extracting shared code into packages, or creating developer tooling libraries.
---

# SDK Development

Create professional TypeScript SDKs from scratch or by extraction.

## Development Process

```
┌─────────────────────────────────────────────────────────────┐
│                   SDK DEVELOPMENT PROCESS                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. ANALYZE          2. DESIGN           3. IMPLEMENT       │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │ Find code   │ →  │ Define API  │ →  │ Build SDK   │     │
│  │ Map deps    │    │ Plan types  │    │ Add types   │     │
│  │ Set bounds  │    │ Error strat │    │ Handle errs │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│                                                             │
│  4. BUILD            5. TEST            6. PUBLISH          │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │ Bundle      │ →  │ Unit tests  │ →  │ npm publish │     │
│  │ ESM/CJS     │    │ Integration │    │ Docs        │     │
│  │ Types       │    │ Examples    │    │ Changelog   │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Extraction Workflow

When extracting SDK from existing application:

```
┌─────────────────────────────────────────────────────────────┐
│                    EXTRACTION WORKFLOW                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  EXISTING APP                        NEW SDK PACKAGE        │
│  ┌─────────────────────┐            ┌─────────────────────┐│
│  │ src/                │            │ @org/auth-sdk/      ││
│  │ ├── services/       │            │ ├── src/            ││
│  │ │   └── auth/       │ ────────►  │ │   ├── client.ts   ││
│  │ │       ├── client  │  Extract   │ │   ├── types.ts    ││
│  │ │       ├── types   │            │ │   └── errors.ts   ││
│  │ │       └── errors  │            │ ├── package.json    ││
│  │ └── utils/          │            │ └── tsconfig.json   ││
│  └─────────────────────┘            └─────────────────────┘│
│                                              │              │
│                                              ▼              │
│  UPDATED APP                         npm publish            │
│  ┌─────────────────────┐                     │              │
│  │ import { AuthClient }│ ◄──────────────────┘              │
│  │ from '@org/auth-sdk' │                                   │
│  └─────────────────────┘                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

### New SDK Structure

```
my-sdk/
├── src/
│   ├── index.ts           # Public exports
│   ├── client.ts          # Main client class
│   ├── types.ts           # Public types
│   ├── errors.ts          # Error classes
│   └── internal/          # Internal utilities
│       └── http.ts
├── tests/
│   ├── client.test.ts
│   └── integration/
├── examples/
│   └── basic-usage.ts
├── package.json
├── tsconfig.json
├── tsup.config.ts         # Build config
├── vitest.config.ts       # Test config
├── README.md
├── CHANGELOG.md
└── LICENSE
```

### Minimal package.json

```json
{
  "name": "@org/my-sdk",
  "version": "1.0.0",
  "description": "SDK for My Service",
  "type": "module",
  "exports": {
    ".": {
      "import": "./dist/index.js",
      "require": "./dist/index.cjs",
      "types": "./dist/index.d.ts"
    }
  },
  "main": "./dist/index.cjs",
  "module": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "files": ["dist"],
  "scripts": {
    "build": "tsup",
    "test": "vitest",
    "prepublishOnly": "npm run build && npm test"
  },
  "devDependencies": {
    "tsup": "^8.0.0",
    "typescript": "^5.0.0",
    "vitest": "^1.0.0"
  },
  "peerDependencies": {
    "typescript": ">=4.7"
  },
  "peerDependenciesMeta": {
    "typescript": { "optional": true }
  }
}
```

### Minimal tsup.config.ts

```typescript
import { defineConfig } from 'tsup';

export default defineConfig({
  entry: ['src/index.ts'],
  format: ['esm', 'cjs'],
  dts: true,
  clean: true,
  sourcemap: true,
});
```

## SDK Design Principles

### 1. Clean Public API

```typescript
// ✅ Good: Clear, minimal exports
export { AuthClient } from './client';
export { AuthError, TokenExpiredError } from './errors';
export type { AuthConfig, User, Session } from './types';

// ❌ Bad: Exposing internals
export * from './internal/http';
export { parseJwt } from './utils';
```

### 2. Typed Everything

```typescript
// ✅ Good: Full type coverage
interface AuthConfig {
  baseUrl: string;
  timeout?: number;
  onTokenRefresh?: (token: string) => void;
}

class AuthClient {
  constructor(config: AuthConfig) {}
  
  async login(email: string, password: string): Promise<Session> {}
  async logout(): Promise<void> {}
  getUser(): User | null {}
}
```

### 3. Meaningful Errors

```typescript
// ✅ Good: Typed, informative errors
class AuthError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode?: number,
  ) {
    super(message);
    this.name = 'AuthError';
  }
}

class TokenExpiredError extends AuthError {
  constructor() {
    super('Access token has expired', 'TOKEN_EXPIRED', 401);
    this.name = 'TokenExpiredError';
  }
}
```

### 4. Sensible Defaults

```typescript
// ✅ Good: Works out of the box
const client = new AuthClient({
  baseUrl: 'https://api.example.com',
  // timeout: 30000 (default)
  // retries: 3 (default)
  // storage: localStorage (default in browser)
});
```

### 5. Framework Agnostic

```typescript
// ✅ Good: Core SDK has no framework deps
// @org/auth-sdk        - Core SDK
// @org/auth-sdk-react  - React bindings (optional)
// @org/auth-sdk-vue    - Vue bindings (optional)
```

## Extraction Checklist

### Before Extraction
- [ ] Identify all code to extract
- [ ] Map internal dependencies
- [ ] Identify external dependencies
- [ ] Find all usages in app
- [ ] Document current behavior
- [ ] Write tests for existing behavior

### During Extraction
- [ ] Create new package structure
- [ ] Move code incrementally
- [ ] Update imports in original app
- [ ] Run tests after each move
- [ ] Keep original working until done

### After Extraction
- [ ] SDK has its own tests
- [ ] Original app uses SDK as dependency
- [ ] No duplicate code remains
- [ ] Documentation complete
- [ ] Examples provided

## Anti-Patterns

### ❌ Leaking Internals

```typescript
// Bad: Internal types exposed
export interface _InternalHttpConfig { ... }
export function _makeRequest() { ... }

// Good: Only public API exported
export { AuthClient } from './client';
export type { AuthConfig } from './types';
```

### ❌ Tight Coupling

```typescript
// Bad: SDK depends on app-specific code
import { appConfig } from '../../../config';
import { logger } from '../../../utils/logger';

// Good: SDK is self-contained, configurable
class AuthClient {
  constructor(config: AuthConfig) {
    this.baseUrl = config.baseUrl;
    this.logger = config.logger ?? console;
  }
}
```

### ❌ No Error Handling

```typescript
// Bad: Raw errors bubble up
async function login() {
  const res = await fetch('/auth/login');
  return res.json(); // What if it fails?
}

// Good: Wrapped, typed errors
async function login() {
  try {
    const res = await fetch('/auth/login');
    if (!res.ok) {
      throw AuthError.fromResponse(res);
    }
    return res.json();
  } catch (err) {
    throw AuthError.wrap(err);
  }
}
```

### ❌ Breaking Changes

```typescript
// Bad: Rename without deprecation
// v1: login(email, password)
// v2: signIn(credentials) // Breaks all users!

// Good: Deprecate, then remove
/** @deprecated Use signIn() instead */
login(email: string, password: string) {
  return this.signIn({ email, password });
}

signIn(credentials: Credentials) { ... }
```

---

**References:**
- [references/extraction-analysis.md](references/extraction-analysis.md) — Analyzing code, finding boundaries, planning extraction
- [references/sdk-architecture.md](references/sdk-architecture.md) — SDK structure, patterns, API design
- [references/implementation.md](references/implementation.md) — TypeScript patterns, types, error handling
- [references/building-bundling.md](references/building-bundling.md) — Build tools, formats, tree-shaking
- [references/publishing.md](references/publishing.md) — npm publishing, private registries, versioning, CI/CD
