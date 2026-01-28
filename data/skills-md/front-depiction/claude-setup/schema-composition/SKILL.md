---
name: schema-composition
description: Master Effect Schema composition patterns including Schema.compose vs Schema.pipe, transformations, filters, and validation. Use this skill when working with complex schema compositions, multi-step transformations, or when you need to validate and transform data through multiple stages.
---

# Schema Composition Skill

Expert guidance for composing, transforming, and validating data with Effect Schema.

## Core Concepts

### The Schema Type

Every schema in Effect has the type signature `Schema<Type, Encoded, Context>` where:

- **Type**: The validated, decoded output type (what you get after successful decoding)
- **Encoded**: The raw input type (what you provide for decoding)
- **Context**: External dependencies required for encoding/decoding (often `never`)

**Example:**
```typescript
import { Schema } from "effect"

// Schema<number, string, never>
//        ^Type  ^Encoded ^Context
const NumberFromString = Schema.NumberFromString
```

### Decoding vs Encoding

- **Decoding**: Transform `Encoded` → `Type` (e.g., string "123" → number 123)
- **Encoding**: Transform `Type` → `Encoded` (e.g., number 123 → string "123")

Effect Schema follows "parse, don't validate" - schemas transform data into the desired format, not just check validity.

## Schema.compose vs Schema.pipe

Understanding when to use `compose` vs `pipe` is fundamental to schema composition.

### Schema.compose - Chaining Transformations

Use `Schema.compose` to chain schemas with **different types** at each stage. It connects the output type of one schema to the input type of another.

**Type Signature:**
```text
Schema.compose: <A, B, R1>(from: Schema<B, A, R1>) =>
  <C, R2>(to: Schema<C, B, R2>) => Schema<C, A, R1 | R2>
```

**When to Use:**
- Multi-step transformations where each stage changes the type
- Connecting parsing and validation steps
- Building pipelines from `Encoded → Intermediate → Type`

**Example - Parse and Validate:**
```typescript
import { Schema } from "effect"

// Split string → array, then transform array → numbers
const schema = Schema.compose(
  Schema.split(","),              // string → readonly string[]
  Schema.Array(Schema.NumberFromString) // readonly string[] → readonly number[]
)

// Result: Schema<readonly number[], string, never>
console.log(Schema.decodeUnknownSync(schema)("1,2,3")) // [1, 2, 3]
```

**Example - Boolean from String via Literal:**
```typescript
import { Schema } from "effect"

const BooleanFromString = Schema.compose(
  Schema.Literal("on", "off"),  // string → "on" | "off"
  Schema.transform(
    Schema.Literal("on", "off"),
    Schema.Boolean,
    {
      strict: true,
      decode: (s) => s === "on",
      encode: (b) => b ? "on" : "off"
    }
  )
)
```

**Non-strict Composition:**

When type boundaries don't align perfectly, use `{ strict: false }`:

```typescript
import { Schema } from "effect"

// Without strict: false, TypeScript error
Schema.compose(
  Schema.Union(Schema.Null, Schema.Literal("0")),
  Schema.NumberFromString,
  { strict: false }
)
```

### Schema.pipe - Sequential Refinements

Use `Schema.pipe` to apply **filters and refinements** to the same type. It doesn't change the type, just adds validation constraints.

**When to Use:**
- Adding validation rules to an existing schema
- Chaining multiple filters on the same type
- Refining without transformation

**Example - Number Validation:**
```typescript
import { Schema } from "effect"

const PositiveInt = Schema.Number.pipe(
  Schema.int(),      // Ensure it's an integer
  Schema.positive()  // Ensure it's positive
)

// Type: Schema<number, number, never>
// Both Type and Encoded are `number`
```

**Example - String Validation:**
```typescript
import { Schema } from "effect"

const ValidEmail = Schema.String.pipe(
  Schema.trimmed(),
  Schema.lowercased(),
  Schema.minLength(5),
  Schema.pattern(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)
)
```

### Key Differences

| Aspect | Schema.compose | Schema.pipe |
|--------|---------------|-------------|
| **Purpose** | Chain transformations | Apply refinements |
| **Type Change** | Changes type at each stage | Type stays the same |
| **Example** | `string → array → numbers` | `number → positive number` |
| **Use Case** | Multi-step parsing | Validation constraints |

## Built-in Filters

Filters add validation constraints without changing the schema's type. They use `Schema.filter()` under the hood.

### String Filters

```typescript
import { Schema } from "effect"

// Length constraints
Schema.String.pipe(Schema.maxLength(5))
Schema.String.pipe(Schema.minLength(5))
Schema.String.pipe(Schema.nonEmptyString()) // alias: Schema.NonEmptyString
Schema.String.pipe(Schema.length(5))
Schema.String.pipe(Schema.length({ min: 2, max: 4 }))

// Pattern matching
Schema.String.pipe(Schema.pattern(/^[a-z]+$/))
Schema.String.pipe(Schema.startsWith("prefix"))
Schema.String.pipe(Schema.endsWith("suffix"))
Schema.String.pipe(Schema.includes("substring"))

// Case and whitespace validation
Schema.String.pipe(Schema.trimmed())        // No leading/trailing whitespace
Schema.String.pipe(Schema.lowercased())     // All lowercase
Schema.String.pipe(Schema.uppercased())     // All uppercase
Schema.String.pipe(Schema.capitalized())    // First letter capitalized
Schema.String.pipe(Schema.uncapitalized())  // First letter lowercase
```

### Number Filters

```typescript
import { Schema } from "effect"

// Range constraints
Schema.Number.pipe(Schema.greaterThan(5))
Schema.Number.pipe(Schema.greaterThanOrEqualTo(5))
Schema.Number.pipe(Schema.lessThan(5))
Schema.Number.pipe(Schema.lessThanOrEqualTo(5))
Schema.Number.pipe(Schema.between(-2, 2)) // Inclusive

// Type constraints
Schema.Number.pipe(Schema.int())         // alias: Schema.Int
Schema.Number.pipe(Schema.nonNaN())      // alias: Schema.NonNaN
Schema.Number.pipe(Schema.finite())      // alias: Schema.Finite

// Sign constraints
Schema.Number.pipe(Schema.positive())     // > 0, alias: Schema.Positive
Schema.Number.pipe(Schema.nonNegative())  // >= 0, alias: Schema.NonNegative
Schema.Number.pipe(Schema.negative())     // < 0, alias: Schema.Negative
Schema.Number.pipe(Schema.nonPositive())  // <= 0, alias: Schema.NonPositive

// Special constraints
Schema.Number.pipe(Schema.multipleOf(5))  // Evenly divisible
Schema.Uint8                              // 8-bit unsigned (0-255)
Schema.NonNegativeInt                     // Non-negative integer
```

### Array Filters

```typescript
import { Schema } from "effect"

Schema.Array(Schema.Number).pipe(Schema.maxItems(2))
Schema.Array(Schema.Number).pipe(Schema.minItems(2))
Schema.Array(Schema.Number).pipe(Schema.itemsCount(2))
```

### Date Filters

```typescript
import { Schema } from "effect"

declare const now: Date

Schema.DateFromSelf.pipe(Schema.validDate())  // alias: Schema.ValidDateFromSelf
Schema.Date.pipe(Schema.greaterThanDate(now))
Schema.Date.pipe(Schema.greaterThanOrEqualToDate(now))
Schema.Date.pipe(Schema.lessThanDate(now))
Schema.Date.pipe(Schema.lessThanOrEqualToDate(now))
Schema.Date.pipe(Schema.betweenDate(new Date(0), now))
```

### BigInt Filters

```typescript
import { Schema } from "effect"

Schema.BigInt.pipe(Schema.greaterThanBigInt(5n))
Schema.BigInt.pipe(Schema.greaterThanOrEqualToBigInt(5n))
Schema.BigInt.pipe(Schema.lessThanBigInt(5n))
Schema.BigInt.pipe(Schema.lessThanOrEqualToBigInt(5n))
Schema.BigInt.pipe(Schema.betweenBigInt(-2n, 2n))

Schema.BigInt.pipe(Schema.positiveBigInt())     // alias: Schema.PositiveBigIntFromSelf
Schema.BigInt.pipe(Schema.nonNegativeBigInt())  // alias: Schema.NonNegativeBigIntFromSelf
Schema.BigInt.pipe(Schema.negativeBigInt())     // alias: Schema.NegativeBigIntFromSelf
Schema.BigInt.pipe(Schema.nonPositiveBigInt())  // alias: Schema.NonPositiveBigIntFromSelf
```

### BigDecimal Filters

```typescript
import { BigDecimal, Schema } from "effect"

Schema.BigDecimal.pipe(Schema.greaterThanBigDecimal(BigDecimal.unsafeFromNumber(5)))
Schema.BigDecimal.pipe(Schema.lessThanBigDecimal(BigDecimal.unsafeFromNumber(5)))
Schema.BigDecimal.pipe(Schema.betweenBigDecimal(
  BigDecimal.unsafeFromNumber(-2),
  BigDecimal.unsafeFromNumber(2)
))

Schema.BigDecimal.pipe(Schema.positiveBigDecimal())
Schema.BigDecimal.pipe(Schema.nonNegativeBigDecimal())
Schema.BigDecimal.pipe(Schema.negativeBigDecimal())
Schema.BigDecimal.pipe(Schema.nonPositiveBigDecimal())
```

### Duration Filters

```typescript
import { Schema } from "effect"

Schema.Duration.pipe(Schema.greaterThanDuration("5 seconds"))
Schema.Duration.pipe(Schema.lessThanDuration("5 seconds"))
Schema.Duration.pipe(Schema.betweenDuration("5 seconds", "10 seconds"))
```

## Custom Filters

Define custom validation logic using `Schema.filter()`:

```typescript
import { Schema } from "effect"

const LongString = Schema.String.pipe(
  Schema.filter(
    (s) => s.length >= 10 || "a string at least 10 characters long"
  )
)
```

### Filter Return Types

The filter predicate can return:

| Return Type | Meaning |
|------------|---------|
| `true` or `undefined` | Validation passes |
| `false` | Validation fails (no error message) |
| `string` | Validation fails with error message |
| `ParseResult.ParseIssue` | Validation fails with detailed error |
| `FilterIssue` | Validation fails with path and message |
| `ReadonlyArray<FilterOutput>` | Multiple validation errors |

### Filter Annotations

Add metadata to filters for better error messages:

```typescript
import { Schema } from "effect"

const LongString = Schema.String.pipe(
  Schema.filter(
    (s) => s.length >= 10 ? undefined : "a string at least 10 characters long",
    {
      identifier: "LongString",
      jsonSchema: { minLength: 10 },
      description: "A string with at least 10 characters"
    }
  )
)
```

### Error Paths for Form Validation

Associate errors with specific fields using `path`:

```typescript
import { Schema } from "effect"

const Password = Schema.Trim.pipe(Schema.minLength(2))

const MyForm = Schema.Struct({
  password: Password,
  confirm_password: Password
}).pipe(
  Schema.filter((input) => {
    if (input.password !== input.confirm_password) {
      return {
        path: ["confirm_password"],
        message: "Passwords do not match"
      }
    }
  })
)
```

### Multiple Error Reporting

Return an array of issues to report multiple errors:

```typescript
import { Schema } from "effect"

const Password = Schema.Trim.pipe(Schema.minLength(2))

Schema.Struct({
  password: Password,
  confirm_password: Password,
  name: Schema.optional(Schema.String),
  surname: Schema.optional(Schema.String)
}).pipe(
  Schema.filter((input) => {
    const issues: Array<Schema.FilterIssue> = []

    if (input.password !== input.confirm_password) {
      issues.push({
        path: ["confirm_password"],
        message: "Passwords do not match"
      })
    }

    if (!input.name && !input.surname) {
      issues.push({
        path: ["surname"],
        message: "Surname must be present if name is not present"
      })
    }

    return issues
  })
)
```

### Effectful Filters

Use `Schema.filterEffect` for async validation:

```typescript
import { Effect, Schema } from "effect"

async function validateUsername(username: string) {
  return Promise.resolve(username === "gcanti")
}

const ValidUsername = Schema.String.pipe(
  Schema.filterEffect((username) =>
    Effect.promise(() =>
      validateUsername(username).then(
        (valid) => valid || "Invalid username"
      )
    )
  )
).annotations({ identifier: "ValidUsername" })
```

## Built-in Transformations

Transformations change data from one type to another, unlike filters which only validate.

### String Transformations

```typescript
import { Schema } from "effect"

// Whitespace and case transformations
Schema.Trim              // Remove leading/trailing whitespace
Schema.Lowercase         // Convert to lowercase
Schema.Uppercase         // Convert to uppercase
Schema.Capitalize        // Capitalize first character
Schema.Uncapitalize      // Uncapitalize first character

// Parsing transformations
Schema.split(",")        // Split string into array
Schema.parseJson()       // Parse JSON string to unknown
// Schema.parseJson(schema) requires a schema parameter - see Advanced Composition Patterns

// Encoding transformations
Schema.StringFromBase64        // Decode base64 to UTF-8
Schema.StringFromBase64Url     // Decode base64 URL to UTF-8
Schema.StringFromHex           // Decode hex to UTF-8
Schema.StringFromUriComponent  // Decode URI component to UTF-8
```

**Example:**
```typescript
import { Schema } from "effect"

const decode = Schema.decodeUnknownSync(Schema.Trim)
console.log(decode(" hello ")) // "hello"
```

### Number Transformations

```typescript
import { Schema } from "effect"

// Parse numbers from strings
Schema.NumberFromString  // "123" → 123 (supports "NaN", "Infinity", "-Infinity")
```

### Boolean Transformations

```typescript
import { Schema } from "effect"

// Transform various values to boolean
Schema.Not  // Negation: boolean → boolean
```

### Common Transformation Patterns

**URL Parsing:**
```typescript
import { Schema } from "effect"

// Parse strings into URL objects
const schema = Schema.URL
Schema.decodeUnknownSync(schema)("https://example.com")
// Output: URL { href: 'https://example.com/', ... }
```

**Date Parsing:**
```typescript
import { Schema } from "effect"

// Parse strings into Date objects
const schema = Schema.Date
Schema.decodeUnknownSync(schema)("2020-01-01")
// Output: Date object
```

## Custom Transformations

### Schema.transform - Simple Transformations

Use `Schema.transform` when the transformation always succeeds:

```typescript
import { Schema } from "effect"

const BooleanFromString = Schema.transform(
  Schema.Literal("on", "off"),  // Source schema
  Schema.Boolean,                // Target schema
  {
    strict: true,  // Optional: better TypeScript errors
    decode: (literal) => literal === "on",
    encode: (bool) => bool ? "on" : "off"
  }
)
```

**Key Points:**
- `decode` transforms from source output to target input
- `encode` transforms from target type back to source type
- Use `strict: true` for better TypeScript error messages

### Schema.transformOrFail - Transformations That Can Fail

Use `Schema.transformOrFail` when transformation might fail:

```typescript
import { ParseResult, Schema } from "effect"

const NumberFromString = Schema.transformOrFail(
  Schema.String,
  Schema.Number,
  {
    strict: true,
    decode: (input, options, ast) => {
      const parsed = parseFloat(input)
      if (isNaN(parsed)) {
        return ParseResult.fail(
          new ParseResult.Type(
            ast,
            input,
            "Failed to convert string to number"
          )
        )
      }
      return ParseResult.succeed(parsed)
    },
    encode: (input, options, ast) => ParseResult.succeed(input.toString())
  }
)
```

### Async Transformations

Return an `Effect` for async transformations:

```typescript
import { Effect, Schema, ParseResult } from "effect"

const get = (url: string): Effect.Effect<unknown, Error> =>
  Effect.tryPromise({
    try: () => fetch(url).then((res) => res.json()),
    catch: (e) => new Error(String(e))
  })

const PeopleId = Schema.String.pipe(Schema.brand("PeopleId"))

const PeopleIdFromString = Schema.transformOrFail(
  Schema.String,
  PeopleId,
  {
    strict: true,
    decode: (s, _, ast) =>
      Effect.mapBoth(get(`https://swapi.dev/api/people/${s}`), {
        onFailure: (e) => new ParseResult.Type(ast, s, e.message),
        onSuccess: () => s
      }),
    encode: ParseResult.succeed
  }
)
```

### One-Way Transformations

Use `ParseResult.Forbidden` to prevent encoding:

```typescript
import { Schema, ParseResult, Redacted } from "effect"
import { createHash } from "node:crypto"

const PlainPassword = Schema.String.pipe(
  Schema.minLength(6),
  Schema.brand("PlainPassword")
)

const HashedPassword = Schema.String.pipe(
  Schema.brand("HashedPassword")
)

const PasswordHashing = Schema.transformOrFail(
  PlainPassword,
  Schema.RedactedFromSelf(HashedPassword),
  {
    strict: true,
    decode: (plainPassword) => {
      const hash = createHash("sha256")
        .update(plainPassword)
        .digest("hex")
      return ParseResult.succeed(Redacted.make(hash))
    },
    encode: (hashedPassword, _, ast) =>
      ParseResult.fail(
        new ParseResult.Forbidden(
          ast,
          hashedPassword,
          "Encoding hashed passwords back to plain text is forbidden."
        )
      )
  }
)
```

## Streamlined Effect Patterns

### Direct flatMap with Schema.decodeUnknown

`Schema.decodeUnknown(schema)` returns a function that can be passed directly to `Effect.flatMap`:

```typescript
import { Effect, Schema } from "effect"

declare const self: Effect.Effect<unknown, unknown, unknown>
declare const schema: Schema.Schema<unknown, unknown, never>
declare const toError: (e: unknown) => unknown

// ❌ Verbose
self.pipe(
  Effect.flatMap((value) =>
    Schema.decodeUnknown(schema)(value).pipe(
      Effect.mapError(toError)
    )
  )
)

// ✅ Streamlined
self.pipe(
  Effect.flatMap(Schema.decodeUnknown(schema)),
  Effect.mapError(toError)
)
```

### Extract Schema Factories

Create reusable schema factories for common patterns:

```typescript
import { Effect, Schema } from "effect"

declare const toAssertionError: (e: unknown) => Error

const createGreaterThanSchema = (n: number) =>
  Schema.Number.pipe(Schema.greaterThan(n))

export const beGreaterThan = (n: number) =>
  <E, R>(self: Effect.Effect<number, E, R>) =>
    self.pipe(
      Effect.flatMap(Schema.decodeUnknown(createGreaterThanSchema(n))),
      Effect.mapError(toAssertionError)
    )
```

### Reuse Composed Schemas

Define schemas once and reuse them:

```typescript
import { Effect, Schema } from "effect"

declare const toAssertionError: (e: unknown) => Error

const TruthySchema = Schema.compose(Schema.BooleanFromUnknown, Schema.Literal(true))

export const beTruthy = () =>
  <E, R>(self: Effect.Effect<unknown, E, R>) =>
    self.pipe(
      Effect.flatMap(Schema.decodeUnknown(TruthySchema)),
      Effect.mapError(toAssertionError)
    )
```

## Decoding and Encoding

### Decoding APIs

| API | Return Type | Use Case |
|-----|-------------|----------|
| `decodeUnknownSync` | `Type` (throws on error) | Sync decoding, immediate error |
| `decodeUnknownOption` | `Option<Type>` | Sync decoding, no error details |
| `decodeUnknownEither` | `Either<ParseError, Type>` | Sync decoding, error handling |
| `decodeUnknownPromise` | `Promise<Type>` | Async decoding |
| `decodeUnknown` | `Effect<Type, ParseError, Context>` | Full Effect-based decoding |

**Example:**
```typescript
import { Schema, Either, Effect } from "effect"

const Person = Schema.Struct({
  name: Schema.String,
  age: Schema.Number
})

// Sync with error throwing
const person1 = Schema.decodeUnknownSync(Person)({ name: "Alice", age: 30 })

// Sync with Either
const result = Schema.decodeUnknownEither(Person)({ name: "Alice", age: 30 })
if (Either.isRight(result)) {
  console.log(result.right)
}

// Effect-based (required for async schemas)
declare const asyncSchema: Schema.Schema<unknown, unknown, unknown>
declare const data: unknown

const asyncResult = Schema.decodeUnknown(asyncSchema)(data)
Effect.runPromise(asyncResult).then(console.log)
```

### Encoding APIs

| API | Return Type | Use Case |
|-----|-------------|----------|
| `encodeSync` | `Encoded` (throws on error) | Sync encoding, immediate error |
| `encodeOption` | `Option<Encoded>` | Sync encoding, no error details |
| `encodeEither` | `Either<ParseError, Encoded>` | Sync encoding, error handling |
| `encodePromise` | `Promise<Encoded>` | Async encoding |
| `encode` | `Effect<Encoded, ParseError, Context>` | Full Effect-based encoding |

**Example:**
```typescript
import { Schema } from "effect"

const Person = Schema.Struct({
  name: Schema.NonEmptyString,
  age: Schema.NumberFromString
})

// Encode: number 30 → string "30"
console.log(Schema.encodeSync(Person)({ name: "Alice", age: 30 }))
// Output: { name: "Alice", age: "30" }
```

## Advanced Composition Patterns

### Combining Arrays and Transformations

```typescript
import { Schema } from "effect"

const ReadonlySetFromArray = <A, I, R>(
  itemSchema: Schema.Schema<A, I, R>
): Schema.Schema<ReadonlySet<A>, ReadonlyArray<I>, R> =>
  Schema.transform(
    Schema.Array(itemSchema),
    // Use Schema.typeSchema to avoid double decoding
    Schema.ReadonlySetFromSelf(Schema.typeSchema(itemSchema)),
    {
      strict: true,
      decode: (items) => new Set(items),
      encode: (set) => Array.from(set.values())
    }
  )

const schema = ReadonlySetFromArray(Schema.String)
// Schema<ReadonlySet<string>, readonly string[], never>
```

### Multi-Stage Transformations

```typescript
import { Schema } from "effect"

const BooleanFromString = Schema.transform(
  Schema.Literal("on", "off"),
  Schema.Boolean,
  {
    strict: true,
    decode: (s) => s === "on",
    encode: (bool) => bool ? "on" : "off"
  }
)

const BooleanFromNumericString = Schema.transform(
  Schema.NumberFromString,    // string → number
  BooleanFromString,          // "on"|"off" → boolean
  {
    strict: true,
    decode: (n) => n > 0 ? "on" : "off",
    encode: (bool) => bool === "on" ? 1 : -1
  }
)
// Result: Schema<boolean, string, never>
```

### Conditional Transformations (Non-strict)

When types don't align perfectly, use `strict: false`:

```typescript
import { Schema, Number } from "effect"

const clamp = (minimum: number, maximum: number) =>
  <A extends number, I, R>(self: Schema.Schema<A, I, R>) =>
    Schema.transform(
      self,
      self.pipe(
        Schema.typeSchema,
        Schema.filter((a) => a >= minimum && a <= maximum)
      ),
      {
        strict: false,  // Relax type constraints
        decode: (a) => Number.clamp(a, { minimum, maximum }),
        encode: (a) => a
      }
    )
```

## Struct and Object Schemas

### Basic Struct

```typescript
import { Schema } from "effect"

const Person = Schema.Struct({
  name: Schema.String,
  age: Schema.Number
})

// Type: { readonly name: string; readonly age: number }
```

### Optional Fields

```typescript
import { Schema } from "effect"

const User = Schema.Struct({
  username: Schema.String,
  email: Schema.optional(Schema.String)
})

// Type: { readonly username: string; readonly email?: string | undefined }
```

### Nullable Fields

```typescript
import { Schema } from "effect"

const Data = Schema.Struct({
  value: Schema.NullOr(Schema.String)
})

// Type: { readonly value: string | null }
```

### Partial and Required

```typescript
import { Schema } from "effect"

const User = Schema.Struct({
  username: Schema.String,
  email: Schema.optional(Schema.String)
})

// Make all fields optional
const PartialUser = Schema.partial(User)

// Make all fields required
const RequiredUser = Schema.required(PartialUser)
```

### Picking and Omitting

```typescript
import { Schema } from "effect"

const Recipe = Schema.Struct({
  id: Schema.String,
  name: Schema.String,
  ingredients: Schema.Array(Schema.String)
})

const JustTheName = Recipe.pick("name")
const NoIDRecipe = Recipe.omit("id")
```

### Extending Structs

```typescript
import { Schema } from "effect"

const Dog = Schema.Struct({
  name: Schema.String,
  age: Schema.Number
})

// Method 1: Using extend
const DogWithBreed = Dog.pipe(
  Schema.extend(Schema.Struct({ breed: Schema.String }))
)

// Method 2: Spreading fields (recommended)
const DogWithBreed2 = Schema.Struct({
  ...Dog.fields,
  breed: Schema.String
})
```

### Excess Property Handling

```typescript
import { Schema } from "effect"

const person = Schema.Struct({
  name: Schema.String
})

// Preserve extra properties
Schema.decodeUnknownSync(person)(
  { name: "bob dylan", extraKey: 61 },
  { onExcessProperty: "preserve" }
)
// Output: { name: "bob dylan", extraKey: 61 }

// Error on extra properties
Schema.decodeUnknownSync(person)(
  { name: "bob dylan", extraKey: 61 },
  { onExcessProperty: "error" }
)
// Throws ParseError
```

## Common Patterns

### Email Validation

```typescript
import { Schema } from "effect"

const Email = Schema.String.pipe(
  Schema.lowercased(),
  Schema.trimmed(),
  Schema.pattern(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)
)
```

### UUID Validation

```typescript
import { Schema } from "effect"

const UserId = Schema.UUID.pipe(
  Schema.brand("UserId")
)
```

### Clamping Numbers

```typescript
import { Schema } from "effect"

const Percentage = Schema.Number.pipe(
  Schema.between(0, 100),
  Schema.brand("Percentage")
)
```

### Template Literal Parsing

```typescript
import { Schema } from "effect"

// Parse Bearer tokens
const AuthToken = Schema.TemplateLiteralParser(
  "Bearer ",
  Schema.String.pipe(Schema.brand("Token"))
)

// Decodes: "Bearer abc123" → ["Bearer ", "abc123"]
```

### Branded Types

```typescript
import { Schema } from "effect"

const PositiveInt = Schema.Number.pipe(
  Schema.int(),
  Schema.positive(),
  Schema.brand("PositiveInt")
)

// Type: number & Brand<"PositiveInt">
```

### Form Validation

```typescript
import { Schema } from "effect"

const LoginForm = Schema.Struct({
  email: Schema.String.pipe(
    Schema.lowercased(),
    Schema.pattern(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)
  ),
  password: Schema.String.pipe(
    Schema.minLength(8),
    Schema.pattern(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/)
  )
})
```

### API Response Parsing

```typescript
import { Schema } from "effect"

const User = Schema.Struct({
  id: Schema.NumberFromString,
  name: Schema.String,
  email: Schema.String,
  createdAt: Schema.DateFromString
})

const UsersResponse = Schema.Struct({
  users: Schema.Array(User),
  total: Schema.Number
})
```

## Quality Checklist

When creating schemas, ensure:

- [ ] Use `Schema.compose` for type transformations, `Schema.pipe` for refinements
- [ ] Prefer built-in schemas (Positive, NonEmptyString, etc.) over custom filters
- [ ] Extract reusable schemas as constants or factory functions
- [ ] Use `Schema.decodeUnknown` directly in `Effect.flatMap` (no wrapper lambda)
- [ ] Place error mapping outside `flatMap` for cleaner composition
- [ ] Use `strict: true` for better TypeScript error messages in transformations
- [ ] Add annotations (identifier, description) to custom filters
- [ ] Use `Schema.typeSchema` when composing to avoid double decoding
- [ ] Handle async operations with `Schema.decodeUnknown`, not sync alternatives
- [ ] Return detailed error paths for form validation
- [ ] Use branded types for domain-specific values
- [ ] Validate both structure (type) and constraints (filters)

## Key Principles

1. **Composition over custom logic** - Leverage `Schema.compose` and `Schema.pipe` instead of manual validation
2. **Reusability** - Extract schemas as constants or factory functions
3. **Type safety** - Let Schema handle type inference and refinement
4. **Streamlined Effect chains** - Minimize lambda wrappers, use direct function passing
5. **Built-in schemas first** - Use Effect's built-in schemas before creating custom ones
6. **Parse, don't validate** - Transform data into the desired format, not just check it
7. **Fail fast, fail clearly** - Provide detailed error messages with paths and context

## References

- Effect Schema is imported from `effect/Schema` or `{ Schema } from "effect"`
- Schema API signature: `Schema<Type, Encoded, Context>`
- All schemas return `readonly` types by default
- Use `Schema.asSchema` to view any schema as `Schema<Type, Encoded, Context>`
- Access base schema before filter with `.from` property
- Access struct fields with `.fields` property
