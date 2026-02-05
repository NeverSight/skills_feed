---
name: tsdoc-comments
description: Use when documenting public APIs. Use when writing library code. Use when using JSDoc-style comments. Use when generating documentation. Use when explaining complex types.
---

# Use TSDoc for API Comments

## Overview

TSDoc is the standard for documenting TypeScript code. It extends JSDoc with TypeScript-specific features like generic type parameters (`@template`). Good documentation explains not just what code does, but why, and helps users understand your API through IDE tooltips and generated docs.

Well-documented code reduces support burden and improves developer experience for your API consumers.

## When to Use This Skill

- Documenting public APIs
- Writing library code for others
- Explaining complex type parameters
- Generating documentation from code
- Providing IDE tooltips

## The Iron Rule

**Document public APIs with TSDoc. Explain what, why, and provide examples. Use @template for generic type parameters.**

## Detection

Watch for undocumented public APIs:

```typescript
// RED FLAGS - Missing documentation
export function process(data: unknown): Result;  // What does it do?
export type Transform<T> = /* complex type */;   // What's T for?
export class ApiClient {                         // How do I use this?
  constructor(config: Config) {}
}
```

## Basic TSDoc Structure

```typescript
/**
 * Short description of what this does.
 *
 * Longer explanation if needed. Explain why this exists,
 * when to use it, and any important caveats.
 *
 * @param paramName - Description of parameter
 * @returns Description of return value
 * @example
 * ```typescript
 * const result = myFunction('input');
 * console.log(result); // 'processed: input'
 * ```
 */
function myFunction(input: string): string {
  return `processed: ${input}`;
}
```

## Documenting Functions

```typescript
/**
 * Fetches user data from the API.
 *
 * Automatically handles authentication and retries failed requests
 * up to 3 times with exponential backoff.
 *
 * @param userId - The unique identifier for the user
 * @param options - Optional configuration for the request
 * @returns A promise that resolves to the user data
 * @throws {ApiError} When the user is not found or the request fails
 * @example
 * ```typescript
 * const user = await fetchUser('123');
 * console.log(user.name);
 * ```
 */
async function fetchUser(
  userId: string,
  options?: FetchOptions
): Promise<User> {
  // Implementation
}
```

## Documenting Generic Types

```typescript
/**
 * Creates a partial version of a type where all properties are optional.
 *
 * @template T - The type to make partial
 * @example
 * ```typescript
 * interface User {
 *   name: string;
 *   age: number;
 * }
 *
 * type PartialUser = Partial<User>;
 * // { name?: string; age?: number; }
 * ```
 */
type MyPartial<T> = {
  [K in keyof T]?: T[K];
};
```

## Documenting Classes

```typescript
/**
 * Client for interacting with the REST API.
 *
 * Handles authentication, request retries, and response parsing.
 * Create one instance per application and reuse it.
 *
 * @example
 * ```typescript
 * const client = new ApiClient({
 *   baseUrl: 'https://api.example.com',
 *   apiKey: process.env.API_KEY
 * });
 *
 * const users = await client.users.list();
 * ```
 */
export class ApiClient {
  /**
   * Creates a new API client instance.
   *
   * @param config - Configuration options for the client
   */
  constructor(config: ClientConfig) {}

  /**
   * Resources for managing users.
   */
  readonly users: UserResource;
}
```

## Common TSDoc Tags

```typescript
/**
 * Description of the function.
 *
 * @param name - Parameter description
 * @returns Return value description
 * @throws {ErrorType} When/why this error is thrown
 * @example Code example showing usage
 * @deprecated Use newFunction instead. Will be removed in v2.0.
 * @see Related function or documentation
 * @internal For internal use only, not part of public API
 */

// For generic types:
/**
 * @template T - Description of type parameter
 * @template K - Description of second parameter
 */

// For class members:
/**
 * @readonly This property is read-only
 * @protected This member is protected
 */
```

## Pressure Resistance Protocol

When documenting code:

1. **Document public APIs**: Everything exported should be documented
2. **Explain why, not just what**: Help users make good decisions
3. **Provide examples**: Show real usage patterns
4. **Document exceptions**: What can go wrong and why
5. **Keep it current**: Update docs when code changes

## Red Flags

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| No documentation | Users guess at usage | Add TSDoc comments |
| "Obvious" comments | `// Adds 1 to x` | Explain why, not what |
| Outdated docs | Misleading users | Update with code changes |
| Missing @template | Generics unexplained | Document type parameters |

## Common Rationalizations

### "The code is self-documenting"

**Reality**: Code shows what happens, not why. Documentation explains intent and context.

### "I'll document it later"

**Reality**: You won't. Document as you write when context is fresh.

### "It's just internal code"

**Reality**: Your future self and coworkers are also users. Document anything non-obvious.

## Quick Reference

| Tag | Use For |
|-----|---------|
| `@param` | Function parameters |
| `@returns` | Return value description |
| `@template` | Generic type parameters |
| `@example` | Usage examples |
| `@throws` | Exceptions thrown |
| `@deprecated` | Mark deprecated APIs |
| `@see` | Related documentation |

## The Bottom Line

Document public APIs with TSDoc. Explain what functions do, why they exist, and how to use them. Good documentation appears in IDE tooltips and reduces support burden.

## Reference

- Effective TypeScript, 2nd Edition by Dan Vanderkam
- Item 68: Use TSDoc for API Comments
