---
name: type-fest
description: TypeScript utility types library with 180+ compile-time transformations for strict type operations, deep object manipulation, case conversions, and JSON-safe typing. Use when building type-safe APIs, config systems, state management, transforming external data schemas or when you are creating a new type.
---

# type-fest: Advanced TypeScript Utility Types

type-fest provides 180+ compile-time utility types with zero runtime overhead for production TypeScript applications. Use it when built-in TypeScript utilities are insufficient for strict type operations, deep transformations, or complex type-level programming.

## When to Use This Skill

**Activate for:**
- API response/request type transformations (snake_case ↔ camelCase)
- Deep configuration merging and partial updates
- Immutable state management with readonly guarantees
- JSON serialization type safety (Date → string, etc.)
- Removing/selecting object properties with strict checking
- Type-safe path access and property selection
- Async function return type extraction
- Conditional type operations

**Skip for:**
- Runtime validation (use zod/yup/io-ts - type-fest is compile-time only)
- Simple cases covered by built-in `Partial`, `Pick`, `Omit`
- Runtime type guards (complement type-fest with runtime checks)

## Installation

```bash
npm install type-fest
```

Import granularly for optimal tree-shaking:
```typescript
import type {Except, Merge, PartialDeep, Jsonify} from 'type-fest';
```

## Essential Utilities

### `Except<T, K>` - Strict Property Removal

**Use when:** Removing keys from objects with compile-time verification.

**Advantage over `Omit`:** Catches typos - requires removed keys to actually exist.

```typescript
import type {Except} from 'type-fest';

interface User {
  id: number;
  email: string;
  password: string;
  role: string;
}

// Remove sensitive fields for public API
type PublicUser = Except<User, 'password'>;
// Result: { id: number; email: string; role: string }

// Catches typos
type Bad = Except<User, 'pasword'>; // ✗ Error: 'pasword' doesn't exist

// Strict mode prevents re-adding omitted props
type StrictPublic = Except<User, 'password', {requireExactProps: true}>;
```

### `Merge<T, U>` - Type-Safe Object Merging

**Use when:** Combining types where second type's properties override the first.

```typescript
import type {Merge} from 'type-fest';

interface BaseConfig {
  host: string;
  port: number;
  timeout: number;
}

interface ProdOverrides {
  port: 3306;  // Literal type
  ssl: boolean;
  poolSize: number;
}

type ProdConfig = Merge<BaseConfig, ProdOverrides>;
// Result: { host: string; port: 3306; timeout: number; ssl: boolean; poolSize: number }
```

### `PartialDeep<T>` - Recursive Optional Properties

**Use when:** Deep configuration objects or nested partial updates.

```typescript
import type {PartialDeep} from 'type-fest';

interface AppSettings {
  theme: {
    colors: {
      primary: string;
      secondary: string;
    };
    fontSize: number;
  };
  features: {
    autoSave: boolean;
  };
}

// User can override any nested property
function updateSettings(updates: PartialDeep<AppSettings>) {
  // updates.theme?.colors?.primary is allowed
}

// Valid calls
updateSettings({theme: {colors: {primary: '#ff0000'}}});
updateSettings({features: {autoSave: false}});
updateSettings({theme: {fontSize: 16}});
```

### `Jsonify<T>` - JSON Serialization Types

**Use when:** Typing API responses/requests that undergo JSON serialization.

**What it does:** 
- `Date` → `string`
- `Map`, `Set` → `{}`
- Functions, `undefined` → removed
- Recursively transforms nested types

```typescript
import type {Jsonify} from 'type-fest';

interface Activity {
  userId: number;
  timestamp: Date;
  metadata: Map<string, string>;
  handler: () => void;
}

type ApiActivity = Jsonify<Activity>;
// Result: { userId: number; timestamp: string; metadata: {} }
// (handler and Map removed, Date → string)

async function fetchActivity(id: string): Promise<Activity> {
  const response = await fetch(`/api/activity/${id}`);
  const json: ApiActivity = await response.json();
  
  // Reconstruct proper types
  return {
    userId: json.userId,
    timestamp: new Date(json.timestamp), // string → Date
    metadata: new Map(),
    handler: () => console.log('loaded')
  };
}
```

### `ReadonlyDeep<T>` - Deep Immutability

**Use when:** Enforcing immutability in state management, config objects.

```typescript
import type {ReadonlyDeep} from 'type-fest';

interface State {
  users: Array<{
    id: number;
    profile: {name: string};
  }>;
}

type ImmutableState = ReadonlyDeep<State>;

const state: ImmutableState = {users: [{id: 1, profile: {name: 'John'}}]};

// All modification attempts cause errors
state.users.push(...); // ✗ Error
state.users[0].profile.name = 'Jane'; // ✗ Error
```

### `CamelCase<T>` - Case Transformation

**Use when:** Converting API/database naming to JavaScript conventions.

```typescript
import type {CamelCase} from 'type-fest';

interface DbUser {
  'user-id': number;
  'email_address': string;
  'created_at': string;
}

type AppUser = {
  [K in keyof DbUser as CamelCase<K>]: DbUser[K]
};
// Result: { userId: number; emailAddress: string; createdAt: string }

// Also available: SnakeCase, KebabCase, PascalCase
```

### `LiteralUnion<T, U>` - Autocomplete-Preserving Unions

**Use when:** Creating extensible string enums that preserve IDE autocomplete.

**Problem solved:** `'red' | 'blue' | string` loses autocomplete for `'red'` and `'blue'`.

```typescript
import type {LiteralUnion} from 'type-fest';

// Without LiteralUnion - no autocomplete
type BadColor = 'red' | 'blue' | 'green' | string;

// With LiteralUnion - IDE autocompletes known values
type Color = LiteralUnion<'red' | 'blue' | 'green', string>;

function setTheme(color: Color) {
  // IDE suggests 'red', 'blue', 'green'
  // But also accepts '#FF5733', 'custom-color', etc.
}
```

### `AsyncReturnType<T>` - Unwrap Promise Types

**Use when:** Typing async function results without manually unwrapping Promise.

```typescript
import type {AsyncReturnType} from 'type-fest';

async function fetchUser(id: number) {
  const res = await fetch(`/api/users/${id}`);
  const data = await res.json();
  return {
    id,
    name: data.name,
    email: data.email,
    roles: data.roles as string[]
  };
}

type User = AsyncReturnType<typeof fetchUser>;
// Result: { id: number; name: any; email: any; roles: string[] }

// Use in callbacks
function processUsers(users: User[]) {
  users.forEach(u => console.log(u.name));
}
```

### `RequireAtLeastOne<T, K>` - Conditional Required Props

**Use when:** Enforcing "at least one of these fields must be present".

```typescript
import type {RequireAtLeastOne} from 'type-fest';

interface SearchParams {
  query?: string;
  userId?: number;
  email?: string;
  tags?: string[];
}

type ValidSearch = RequireAtLeastOne<SearchParams, 'query' | 'userId' | 'email'>;

function search(params: ValidSearch) {
  // At least one of: query, userId, or email is guaranteed
}

search({query: 'test'}); // ✓
search({userId: 123, tags: ['tag']}); // ✓
search({tags: ['tag']}); // ✗ Error: need query, userId, or email
```

### `ConditionalPick<T, Condition>` - Select by Type

**Use when:** Extracting properties that match a specific type.

```typescript
import type {ConditionalPick} from 'type-fest';

interface Endpoint {
  path: string;
  method: 'GET' | 'POST';
  timeout: number;
  retries: number;
  handler: (req: any) => Promise<any>;
  validate: (data: any) => boolean;
}

// Extract only functions
type EndpointFns = ConditionalPick<Endpoint, Function>;
// Result: { handler: ...; validate: ... }

// Extract only numbers
type EndpointNums = ConditionalPick<Endpoint, number>;
// Result: { timeout: number; retries: number }
```

### `Paths<T>` - Type-Safe Property Paths

**Use when:** Building type-safe get/set utilities like lodash.

```typescript
import type {Paths} from 'type-fest';

interface Config {
  database: {
    host: string;
    credentials: {
      user: string;
      password: string;
    };
  };
  api: {endpoint: string};
}

type ConfigPath = Paths<Config>;
// Union: 'database' | 'database.host' | 'database.credentials' | 
//        'database.credentials.user' | 'database.credentials.password' | 
//        'api' | 'api.endpoint'

function get<P extends ConfigPath>(config: Config, path: P): any {
  return path.split('.').reduce((obj: any, key) => obj?.[key], config);
}

get(config, 'database.credentials.user'); // ✓ Autocompletes
get(config, 'invalid.path'); // ✗ Type error
```

### `Simplify<T>` - Flatten Intersection Types

**Use when:** Improving IDE hints and type assignability for composed types.

```typescript
import type {Simplify} from 'type-fest';

type Position = {x: number; y: number};
type Size = {width: number; height: number};
type Styles = {color: string; opacity: number};

// Without Simplify - IDE shows: Position & Size & Styles
type Complex = Position & Size & Styles;

// With Simplify - IDE shows flat object
type Simple = Simplify<Position & Size & Styles>;
// Result: { x: number; y: number; width: number; height: number; color: string; opacity: number }
```

## Common Patterns

### API Client with Type Transformations

```typescript
import type {Except, Jsonify, CamelCase, AsyncReturnType, ReadonlyDeep} from 'type-fest';

// External API (snake_case)
interface ApiUser {
  user_id: number;
  email_address: string;
  created_at: string;
}

// Internal app (camelCase)
type AppUser = {
  [K in keyof ApiUser as CamelCase<K>]: ApiUser[K]
};

// Public user (no sensitive data)
type PublicUser = Except<AppUser, 'emailAddress'>;

// Immutable state
type UserState = ReadonlyDeep<AppUser>;

class UserService {
  async getUser(id: number): Promise<AppUser> {
    const res = await fetch(`/api/users/${id}`);
    const data: Jsonify<ApiUser> = await res.json();
    
    return {
      userId: data.user_id,
      emailAddress: data.email_address,
      createdAt: data.created_at
    };
  }
}

type User = AsyncReturnType<UserService['getUser']>;
```

### Configuration Management

```typescript
import type {PartialDeep, Merge, Simplify} from 'type-fest';

interface BaseConfig {
  database: {host: string; port: number};
  api: {timeout: number};
}

interface EnvOverrides {
  database: {port: 3306};
  api: {retries: number};
}

// Merge and flatten
type FinalConfig = Simplify<Merge<BaseConfig, EnvOverrides>>;

function loadConfig(
  defaults: BaseConfig,
  overrides: PartialDeep<EnvOverrides>
): FinalConfig {
  // Deep merge logic
  return {...defaults, ...overrides} as FinalConfig;
}
```

### Type-Safe Builders

```typescript
import type {RequireAtLeastOne, Merge} from 'type-fest';

interface BaseRequest {
  timeout?: number;
  headers?: Record<string, string>;
}

interface RequiredFields {
  url: string;
}

type HttpRequest = RequireAtLeastOne<
  Merge<RequiredFields, BaseRequest>,
  'url'
>;

class HttpClient {
  request(config: HttpRequest) {
    // config.url guaranteed to exist
    fetch(config.url, {
      method: 'GET',
      headers: config.headers
    });
  }
}
```

## Composition Strategy

Combine utilities for powerful type transformations:

```typescript
import type {Merge, Simplify, PartialDeep, Except} from 'type-fest';

// Base + overrides + flatten
type CleanMerge<T, U> = Simplify<Merge<T, U>>;

// Remove sensitive + deep partial
type SafePartial<T> = PartialDeep<Except<T, 'password' | 'secret'>>;

// Chain multiple operations
type ComplexType = Simplify<
  Merge<
    Merge<BaseType, OverrideType>,
    FinalType
  >
>;
```

## Important Gotchas

### 1. Runtime vs Compile-Time

**CRITICAL:** type-fest types don't validate at runtime.

```typescript
// DON'T assume runtime safety
function process(data: Jsonify<MyType>) {
  const date = new Date(data.timestamp); // Could fail if data is malformed
}

// DO add runtime validation
function process(data: Jsonify<MyType>) {
  if (typeof data.timestamp !== 'string') {
    throw new Error('Invalid timestamp');
  }
  const date = new Date(data.timestamp);
}
```

### 2. Deep Type Nesting Limits

Avoid excessive `PartialDeep`/`ReadonlyDeep` nesting (3-4 levels max):

```typescript
// DON'T
type Bad = PartialDeep<PartialDeep<DeepType>>;

// DO
type Good = PartialDeep<DeepType>;
```

### 3. Import Only What You Need

Tree-shaking works best with granular imports:

```typescript
// DO
import type {Except, Merge} from 'type-fest';

// DON'T
import type * as TypeFest from 'type-fest';
```

### 4. `LiteralUnion` Scope

Don't use with already-narrow types:

```typescript
// DON'T
type Bad = LiteralUnion<'active', 'active' | 'inactive'>;

// DO
type Good = LiteralUnion<'active' | 'inactive', string>;
```

## Quick Reference

| Need | type-fest Utility | Alternative |
|------|------------------|-------------|
| Remove keys (strict) | `Except<T, K>` | `Omit<T, K>` (lenient) |
| Merge objects | `Merge<T, U>` | `T & U` (intersection) |
| Deep partial | `PartialDeep<T>` | `Partial<T>` (shallow) |
| Deep readonly | `ReadonlyDeep<T>` | `Readonly<T>` (shallow) |
| JSON-safe types | `Jsonify<T>` | Manual transformation |
| Case conversion | `CamelCase<T>` | Manual mapping |
| Extensible enums | `LiteralUnion<T, U>` | `T \| U` (no autocomplete) |
| Unwrap Promise | `AsyncReturnType<T>` | Manual extraction |
| Require some keys | `RequireAtLeastOne<T, K>` | Custom conditional types |
| Pick by type | `ConditionalPick<T, C>` | Custom mapped types |
| Type paths | `Paths<T>` | String literals |
| Flatten types | `Simplify<T>` | Intersection types |

## Additional Utilities

**Also available (180+ total):**
- `RequireExactlyOne` - Exactly one key required
- `SetRequired`, `SetOptional` - Modify individual properties
- `SnakeCase`, `KebabCase`, `PascalCase` - Other case conversions
- `IsEqual<T, U>` - Type equality checking
- `Get<T, Path>` - Type-safe property access
- `Opaque<T>` - Branded types
- `PromiseValue<T>` - Extract Promise value
- Plus 170+ more specialized utilities

Browse the full list: [https://github.com/sindresorhus/type-fest](https://github.com/sindresorhus/type-fest)

## Resources

- **GitHub:** https://github.com/sindresorhus/type-fest
- **Docs:** https://sindresorhus.com/type-fest
- **Full type list:** Browse `/source` directory
- **Examples:** Check test files for usage patterns
- **LLM Guide:** https://context7.com/sindresorhus/type-fest/llms.txt
