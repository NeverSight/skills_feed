---
name: error-handling
description: Implement typed error handling in Effect using Data.TaggedError, catchTag/catchTags, and recovery patterns. Use this skill when working with Effect error channels, handling expected failures, or designing error recovery strategies.
---

You are an Effect TypeScript expert specializing in typed error handling, recovery patterns, and error channel management.

## Effect Documentation Access

For comprehensive Effect documentation, view the Effect repository git subtree in `.context/effect/`

Reference this for:
- Data.TaggedError and error class creation
- Error handling combinators (catchTag, catchTags, catchAll)
- Error transformation and recovery patterns
- Defects vs error channel distinction

## Core Error Handling Philosophy

Effect distinguishes between two types of failures:

1. **Expected Errors (Error Channel)** - Business logic failures that should be handled
   - Type-safe and tracked in the effect signature: `Effect<A, E, R>`
   - Represented by the `E` type parameter
   - Handle with catchTag, catchTags, catchAll

2. **Unexpected Errors (Defects)** - Programming errors that indicate bugs
   - Not tracked in the type system
   - Result from programming mistakes (null refs, unhandled cases, assertions)
   - Usually should NOT be caught; use catchAllDefect only at boundaries

### When to Use Error Channel vs Defects

```typescript
import { Effect, Data } from "effect"

declare const findUser: (userId: string) => Effect.Effect<User, UserNotFound>
declare const validatePassword: (user: User, password: string) => Effect.Effect<boolean, InvalidCredentials>
declare const database: { query: (sql: string, ...params: ReadonlyArray<unknown>) => Effect.Effect<unknown> }

interface User {
  readonly id: string
  readonly name: string
}

// CORRECT - Expected business failures in error channel
class UserNotFound extends Data.TaggedError("UserNotFound")<{
  readonly userId: string
}> {}

class InvalidCredentials extends Data.TaggedError("InvalidCredentials")<{
  readonly reason: string
}> {}

const authenticateUser = (userId: string, password: string): Effect.Effect<User, UserNotFound | InvalidCredentials> =>
  Effect.gen(function* () {
    const user = yield* findUser(userId) // Can fail with UserNotFound
    const valid = yield* validatePassword(user, password) // Can fail with InvalidCredentials
    return user
  })

// CORRECT - Programmer errors as defects (use Effect.die)
const assertPositive = (n: number): Effect.Effect<number> =>
  n > 0
    ? Effect.succeed(n)
    : Effect.die(new Error(`Expected positive number, got ${n}`))

// WRONG - Business failure as defect
const findUserWrong = (userId: string): Effect.Effect<User> =>
  Effect.gen(function* () {
    const user = yield* database.query("SELECT * FROM users WHERE id = ?", userId)
    if (!user) {
      yield* Effect.die(new Error("User not found")) // Should be in error channel!
    }
    return user as User
  })
```

## Creating Tagged Errors

### Basic Tagged Error

```typescript
import { Data } from "effect"

// Simple error with no additional data
export class NetworkError extends Data.TaggedError("NetworkError")<{}> {}

// Error with context data
export class ValidationError extends Data.TaggedError("ValidationError")<{
  readonly field: string
  readonly message: string
  readonly value?: unknown
}> {}

// Error with optional cause
export class DatabaseError extends Data.TaggedError("DatabaseError")<{
  readonly operation: string
  readonly cause?: unknown
}> {}

// Usage
const error = new ValidationError({
  field: "email",
  message: "Invalid email format",
  value: "not-an-email"
})
```

### Schema-Based Tagged Errors

For errors that need serialization (RPC, persistence, etc.):

```typescript
import { Schema } from "effect"

export class ApiError extends Schema.TaggedError<ApiError>(
  "@myapp/ApiError" // Globally unique identifier for serialization
)("ApiError", {
  statusCode: Schema.Number,
  message: Schema.String,
  details: Schema.optional(Schema.Unknown)
}) {}

export class RateLimitError extends Schema.TaggedError<RateLimitError>(
  "@myapp/RateLimitError"
)("RateLimitError", {
  retryAfter: Schema.Number,
  limit: Schema.Number
}) {}
```

### Error with Custom Properties

```typescript
import { Data } from "effect"

export class HttpError extends Data.TaggedError("HttpError")<{
  readonly status: number
  readonly body: string
}> {
  // Add computed properties
  get isClientError() {
    return this.status >= 400 && this.status < 500
  }

  get isServerError() {
    return this.status >= 500
  }
}

// Usage
const error = new HttpError({ status: 404, body: "Not Found" })
console.log(error.isClientError) // true
```

## Handling Errors by Tag

### catchTag - Single Error Type

```typescript
import { Effect, Data } from "effect"

declare const createGuestUser: (id: string) => User

interface User {
  readonly id: string
  readonly name: string
}

class NotFound extends Data.TaggedError("NotFound")<{
  readonly id: string
}> {}

class Unauthorized extends Data.TaggedError("Unauthorized")<{}> {}

//          Effect<User, NotFound | Unauthorized, Dependencies>
//      ↓
const getUser = (id: string): Effect.Effect<User, NotFound | Unauthorized> => Effect.fail(new NotFound({ id }))

// Handle single error type
//          Effect<User, Unauthorized, Dependencies>
//      ↓
const program = getUser("123").pipe(
  Effect.catchTag("NotFound", (error) =>
    // Return default user when not found
    Effect.succeed(createGuestUser(error.id))
  )
)
```

### catchTags - Multiple Error Types

```typescript
import { Effect, Data } from "effect"

interface Data {
  readonly data: ReadonlyArray<unknown>
  readonly cached?: boolean
  readonly timeout?: boolean
  readonly parseError?: boolean
}

class NetworkError extends Data.TaggedError("NetworkError")<{}> {}
class TimeoutError extends Data.TaggedError("TimeoutError")<{}> {}
class ParseError extends Data.TaggedError("ParseError")<{
  readonly input: string
}> {}

//          Effect<Data, NetworkError | TimeoutError | ParseError, Dependencies>
//      ↓
const fetchData = (): Effect.Effect<Data, NetworkError | TimeoutError | ParseError> => Effect.fail(new NetworkError())

// Handle multiple error types at once
//          Effect<Data, never, Dependencies>
//      ↓
const program = fetchData().pipe(
  Effect.catchTags({
    NetworkError: (_error) =>
      Effect.succeed({ data: [], cached: true }),

    TimeoutError: (_error) =>
      Effect.succeed({ data: [], timeout: true }),

    ParseError: (error) =>
      // Access error-specific fields
      Effect.logError(`Failed to parse: ${error.input}`).pipe(
        Effect.as({ data: [], parseError: true })
      )
  })
)
```

### catchAll - Handle All Errors

```typescript
import { Effect, Data } from "effect"

declare const getDefaultResult: () => Result

interface Result {
  readonly value: string
}

class InvalidInput extends Data.TaggedError("InvalidInput")<{}> {}
class ProcessingError extends Data.TaggedError("ProcessingError")<{}> {}

//          Effect<Result, InvalidInput | ProcessingError, Dependencies>
//      ↓
const process = (): Effect.Effect<Result, InvalidInput | ProcessingError> => Effect.fail(new InvalidInput())

// Handle all errors with single handler
//          Effect<Result, never, Dependencies>
//      ↓
const program = process().pipe(
  Effect.catchAll((error) =>
    // error is typed as: InvalidInput | ProcessingError
    Effect.logError(`Operation failed: ${error._tag}`).pipe(
      Effect.as(getDefaultResult())
    )
  )
)
```

## Exhaustive Error Handling with Match

Use Match for exhaustive error handling with compile-time guarantees:

```typescript
import { Effect, Match, Data } from "effect"

declare const dangerousOperation: () => Effect.Effect<string, AppError>

class ConnectionError extends Data.TaggedError("ConnectionError")<{}> {}
class AuthError extends Data.TaggedError("AuthError")<{}> {}
class DataError extends Data.TaggedError("DataError")<{
  readonly message: string
}> {}

type AppError = ConnectionError | AuthError | DataError

const handleError = (error: AppError): Effect.Effect<string> =>
  Match.value(error).pipe(
    Match.tag("ConnectionError", () =>
      Effect.succeed("Please check your network connection")
    ),
    Match.tag("AuthError", () =>
      Effect.succeed("Authentication required")
    ),
    Match.tag("DataError", (err) =>
      Effect.succeed(`Data error: ${err.message}`)
    ),
    Match.exhaustive // Compiler ensures all cases handled
  )

const program = dangerousOperation().pipe(
  Effect.catchAll(handleError)
)
```

## Error Transformation

### mapError - Transform Error Type

```typescript
import { Effect, Data } from "effect"

declare const fetchFromDatabase: () => Effect.Effect<Data, InfrastructureError>

interface Data {
  readonly value: string
}

class DomainError extends Data.TaggedError("DomainError")<{
  readonly message: string
}> {}

class InfrastructureError extends Data.TaggedError("InfrastructureError")<{
  readonly cause: unknown
}> {}

// Transform infrastructure errors to domain errors
//          Effect<Data, DomainError, Dependencies>
//      ↓
const program = fetchFromDatabase().pipe(
  Effect.mapError((infraError: InfrastructureError) =>
    new DomainError({
      message: `Database operation failed: ${infraError.cause}`
    })
  )
)
```

### Error Context Enrichment

```typescript
import { Effect, Data } from "effect"

declare const getCurrentUserId: () => Effect.Effect<string>
declare const riskyOperation: () => Effect.Effect<string, BaseError>

class BaseError extends Data.TaggedError("BaseError")<{
  readonly message: string
}> {}

class EnrichedError extends Data.TaggedError("EnrichedError")<{
  readonly originalError: BaseError
  readonly context: {
    readonly userId: string
    readonly timestamp: number
  }
}> {}

const enrichError = (error: BaseError, userId: string) =>
  new EnrichedError({
    originalError: error,
    context: {
      userId,
      timestamp: Date.now()
    }
  })

const program = Effect.gen(function* () {
  const userId = yield* getCurrentUserId()
  const result = yield* riskyOperation().pipe(
    Effect.mapError((error) => enrichError(error, userId))
  )
  return result
})
```

## Error Recovery Patterns

### Fallback with orElse

```typescript
import { Effect, Data } from "effect"

interface Data {
  readonly value: string
}

class PrimaryServiceError extends Data.TaggedError("PrimaryServiceError")<{}> {}
class SecondaryServiceError extends Data.TaggedError("SecondaryServiceError")<{}> {}

const primaryService: Effect.Effect<Data, PrimaryServiceError> = Effect.fail(new PrimaryServiceError())
const secondaryService: Effect.Effect<Data, SecondaryServiceError> = Effect.fail(new SecondaryServiceError())

// Try primary, fallback to secondary
//          Effect<Data, SecondaryServiceError, Dependencies>
//      ↓
const program = primaryService.pipe(
  Effect.orElse(() => secondaryService)
)
```

### Retry with Schedule

```typescript
import { Effect, Schedule, Data } from "effect"

interface Data {
  readonly value: string
}

class TransientError extends Data.TaggedError("TransientError")<{}> {}

const unreliableOperation: Effect.Effect<Data, TransientError> = Effect.fail(new TransientError())

// Retry with exponential backoff
const program = unreliableOperation.pipe(
  Effect.retry(
    Schedule.exponential("100 millis").pipe(
      Schedule.compose(Schedule.recurs(5)) // Max 5 retries
    )
  )
)
```

### Provide Default Value

```typescript
import { Effect, Data } from "effect"

declare const getDefaultConfig: () => Config

interface Config {
  readonly port: number
  readonly host: string
}

class FetchError extends Data.TaggedError("FetchError")<{}> {}

const fetchConfig: Effect.Effect<Config, FetchError> = Effect.fail(new FetchError())

// Provide default on failure
//          Effect<Config, never, Dependencies>
//      ↓
const program = fetchConfig.pipe(
  Effect.orElseSucceed(() => getDefaultConfig())
)
```

### Convert Error to Option

```typescript
import { Effect, Data, Option } from "effect"

interface Item {
  readonly id: string
  readonly name: string
}

class NotFoundError extends Data.TaggedError("NotFoundError")<{}> {}

const findItem: Effect.Effect<Item, NotFoundError> = Effect.fail(new NotFoundError())

// Convert to Option (None if error)
//          Effect<Option<Item>, never, Dependencies>
//      ↓
const program = findItem.pipe(
  Effect.option
)
```

### Convert Error to Exit

```typescript
import { Effect, Exit, Data } from "effect"

interface Data {
  readonly value: string
}

class AppError extends Data.TaggedError("AppError")<{
  readonly message: string
}> {}

const riskyOperation: Effect.Effect<Data, AppError> = Effect.fail(new AppError({ message: "error" }))

// Get Exit with full cause information
//          Effect<Exit<Data, AppError>, never, Dependencies>
//      ↓
const program = Effect.exit(riskyOperation)

// Handle Exit
Effect.gen(function* () {
  const exit = yield* program

  if (Exit.isSuccess(exit)) {
    console.log("Success:", exit.value)
  } else {
    console.log("Failure:", exit.cause)
  }
})
```

## Error Channel vs Defect Operators

### Converting Errors to Defects

```typescript
import { Effect, Data } from "effect"

interface Config {
  readonly port: number
  readonly host: string
}

class ConfigError extends Data.TaggedError("ConfigError")<{}> {}

const loadConfig: Effect.Effect<Config, ConfigError> = Effect.fail(new ConfigError())

// Convert error to defect (terminates fiber)
//          Effect<Config, never, Dependencies>
//      ↓
const program = loadConfig.pipe(
  Effect.orDie // Error becomes a defect
)

// With custom defect message
const program2 = loadConfig.pipe(
  Effect.orDieWith((error) =>
    new Error(`Fatal: Configuration failed to load: ${error._tag}`)
  )
)
```

### Handling Defects (Boundary Only)

```typescript
import { Effect } from "effect"

declare const dangerousPlugin: () => Effect.Effect<unknown>
declare const getDefaultPluginBehavior: () => unknown

// NOTE: ONLY use at application boundaries
const safeProgram = dangerousPlugin().pipe(
  Effect.catchAllDefect((defect) =>
    Effect.logError(`Plugin crashed: ${defect}`).pipe(
      Effect.as(getDefaultPluginBehavior())
    )
  )
)
```

### Handling All Causes

```typescript
import { Effect, Cause } from "effect"

declare const riskyOperation: () => Effect.Effect<unknown>

const program = riskyOperation().pipe(
  Effect.catchAllCause((cause) =>
    Cause.match(cause, {
      onEmpty: () => Effect.succeed("No failure"),
      onFail: (error) => Effect.succeed(`Handled error: ${error._tag}`),
      onDie: (defect) => Effect.succeed(`Caught defect: ${defect}`),
      onInterrupt: () => Effect.succeed("Interrupted"),
      onSequential: (left, right) => Effect.succeed("Sequential failures"),
      onParallel: (left, right) => Effect.succeed("Parallel failures")
    })
  )
)
```

## Layered Error Handling

Structure error handling in layers from specific to general:

```typescript
import { Effect, Data } from "effect"

declare const validateUserData: (data: UserData) => Effect.Effect<ValidatedUserData, ValidationError>
declare const saveToDatabase: (data: ValidatedUserData) => Effect.Effect<string, DatabaseError>
declare const notifyUserCreated: (userId: string) => Effect.Effect<void, NetworkError>

interface UserData {
  readonly name: string
  readonly email: string
}

interface ValidatedUserData {
  readonly name: string
  readonly email: string
}

class ValidationError extends Data.TaggedError("ValidationError")<{}> {}
class DatabaseError extends Data.TaggedError("DatabaseError")<{}> {}
class NetworkError extends Data.TaggedError("NetworkError")<{}> {}
class UnknownError extends Data.TaggedError("UnknownError")<{
  readonly cause: unknown
}> {}

const createUser = (data: UserData) =>
  Effect.gen(function* () {
    // Layer 1: Validate input
    const validated = yield* validateUserData(data).pipe(
      Effect.catchTag("ValidationError", (error) =>
        Effect.fail(new UnknownError({ cause: error }))
      )
    )

    // Layer 2: Database operation
    const userId = yield* saveToDatabase(validated).pipe(
      Effect.catchTag("DatabaseError", (error) =>
        Effect.fail(new UnknownError({ cause: error }))
      )
    )

    // Layer 3: Network notification
    yield* notifyUserCreated(userId).pipe(
      Effect.catchTag("NetworkError", (error) =>
        // Non-critical: log but don't fail
        Effect.logWarning(`Failed to notify: ${error._tag}`)
      )
    )

    return userId
  })
```

## Domain-Specific Error Patterns

### Repository Errors

```typescript
import { Data } from "effect"

export class EntityNotFound extends Data.TaggedError("EntityNotFound")<{
  readonly entityType: string
  readonly id: string
}> {}

export class DuplicateEntity extends Data.TaggedError("DuplicateEntity")<{
  readonly entityType: string
  readonly id: string
}> {}

export class QueryError extends Data.TaggedError("QueryError")<{
  readonly query: string
  readonly cause: unknown
}> {}

export type RepositoryError = EntityNotFound | DuplicateEntity | QueryError
```

### Service Errors

```typescript
import { Data } from "effect"

export class ServiceUnavailable extends Data.TaggedError("ServiceUnavailable")<{
  readonly service: string
  readonly retryAfter?: number
}> {}

export class ServiceTimeout extends Data.TaggedError("ServiceTimeout")<{
  readonly service: string
  readonly timeoutMs: number
}> {}

export class InvalidResponse extends Data.TaggedError("InvalidResponse")<{
  readonly service: string
  readonly response: unknown
}> {}

export type ServiceError = ServiceUnavailable | ServiceTimeout | InvalidResponse
```

### Validation Errors

```typescript
import { Effect, Data } from "effect"

declare const isValidEmail: (email: string) => boolean

interface User {
  readonly email: string
  readonly age: number
}

export class InvalidField extends Data.TaggedError("InvalidField")<{
  readonly field: string
  readonly value: unknown
  readonly constraint: string
}> {}

export class MissingField extends Data.TaggedError("MissingField")<{
  readonly field: string
}> {}

export class InvalidFormat extends Data.TaggedError("InvalidFormat")<{
  readonly format: string
  readonly input: string
}> {}

export type ValidationError = InvalidField | MissingField | InvalidFormat

// Collect multiple validation errors
const validateUser = (input: any): Effect.Effect<User, Array<ValidationError>> =>
  Effect.gen(function* () {
    const errors: Array<ValidationError> = []

    if (!input.email) {
      errors.push(new MissingField({ field: "email" }))
    } else if (!isValidEmail(input.email)) {
      errors.push(new InvalidFormat({ format: "email", input: input.email }))
    }

    if (!input.age) {
      errors.push(new MissingField({ field: "age" }))
    } else if (input.age < 0) {
      errors.push(new InvalidField({ field: "age", value: input.age, constraint: "positive" }))
    }

    if (errors.length > 0) {
      yield* Effect.fail(errors)
    }

    return { email: input.email, age: input.age }
  })
```

## Testing Error Scenarios

```typescript
import { Effect, Exit, Data } from "effect"
import { describe, it, expect } from "vitest"

class MyError extends Data.TaggedError("MyError")<{
  readonly code: number
}> {}

describe("Error Handling", () => {
  it("should catch specific error", async () => {
    const program = Effect.fail(new MyError({ code: 404 })).pipe(
      Effect.catchTag("MyError", (error) =>
        Effect.succeed(`Handled: ${error.code}`)
      )
    )

    const result = await Effect.runPromise(program)
    expect(result).toBe("Handled: 404")
  })

  it("should propagate unhandled error", async () => {
    class UnhandledError extends Data.TaggedError("UnhandledError")<{}> {}

    const program = Effect.fail(new UnhandledError()).pipe(
      Effect.catchTag("MyError", () => Effect.succeed("Should not reach"))
    )

    const exit = await Effect.runPromiseExit(program)
    expect(Exit.isFailure(exit)).toBe(true)
  })

  it("should handle all errors with catchAll", async () => {
    const program = Effect.fail(new MyError({ code: 500 })).pipe(
      Effect.catchAll((error) =>
        Effect.succeed(`Caught ${error._tag}`)
      )
    )

    const result = await Effect.runPromise(program)
    expect(result).toBe("Caught MyError")
  })
})
```

## Error Documentation Best Practices

```typescript
import { Effect, Data } from "effect"

declare const NotFound: typeof Data.TaggedError

interface User {
  readonly id: string
  readonly name: string
}

interface Database {}

class InvalidCredentials extends Data.TaggedError("InvalidCredentials")<{}> {}
class UserNotFound extends Data.TaggedError("UserNotFound")<{}> {}
class UserLocked extends Data.TaggedError("UserLocked")<{
  readonly unlockAt: Date
}> {}
class DatabaseError extends Data.TaggedError("DatabaseError")<{}> {}

/**
 * Authenticates a user with the provided credentials.
 *
 * @param email - User email address
 * @param password - User password
 * @returns Effect that succeeds with User or fails with auth errors
 *
 * @category Authentication
 * @since 1.0.0
 *
 * @errors
 * - `InvalidCredentials` - Email or password is incorrect
 * - `UserNotFound` - No user exists with the given email
 * - `UserLocked` - Account is temporarily locked due to failed attempts
 * - `DatabaseError` - Database query failed
 */
export const authenticateUser = (
  email: string,
  password: string
): Effect.Effect<
  User,
  InvalidCredentials | UserNotFound | UserLocked | DatabaseError,
  Database
> => Effect.fail(new UserNotFound())
```

## Quality Checklist

Before completing error handling implementation:

- [ ] All domain errors use Data.TaggedError or Schema.TaggedError
- [ ] Error types have meaningful, specific names
- [ ] Errors include relevant context (ids, values, reasons)
- [ ] Business failures in error channel, programmer errors as defects
- [ ] catchTag/catchTags used for specific error handling
- [ ] catchAll only when handling truly all error types
- [ ] Error transformations preserve important context
- [ ] Recovery strategies match business requirements
- [ ] Defect handling only at application boundaries
- [ ] Error types exported from domain modules
- [ ] JSDoc includes @errors section listing possible failures
- [ ] Tests cover error scenarios
- [ ] Type signatures accurately reflect error channel

## Common Patterns

### Conditional Error Handling

```typescript
import { Effect, Schedule, Data } from "effect"

declare const riskyOperation: () => Effect.Effect<unknown, RetryableError>

class RetryableError extends Data.TaggedError("RetryableError")<{
  readonly retryable: boolean
}> {}

const program = riskyOperation().pipe(
  Effect.catchTag("RetryableError", (error) =>
    error.retryable
      ? Effect.retry(riskyOperation(), Schedule.recurs(3))
      : Effect.fail(error)
  )
)
```

### Error Accumulation

```typescript
import { Effect } from "effect"

declare const validateEmail: (email: string) => Effect.Effect<string, ValidationError>
declare const validateAge: (age: number) => Effect.Effect<number, ValidationError>
declare const validateName: (name: string) => Effect.Effect<string, ValidationError>

interface FormInput {
  readonly email: string
  readonly age: number
  readonly name: string
}

interface ValidData {
  readonly email: string
  readonly age: number
  readonly name: string
}

interface ValidationError {
  readonly _tag: string
}

const validateFields = (input: FormInput): Effect.Effect<ValidData, Array<ValidationError>> =>
  Effect.all([
    validateEmail(input.email),
    validateAge(input.age),
    validateName(input.name)
  ], { mode: "validate" }).pipe(
    Effect.map(([email, age, name]) => ({ email, age, name }))
  ) as Effect.Effect<ValidData, Array<ValidationError>>
```

### Error Boundaries

```typescript
import { Effect, Data } from "effect"

declare const processRequest: (request: Request) => Effect.Effect<Response, ValidationError | NotFoundError | DatabaseError>
declare const HttpResponse: {
  badRequest: (message: string) => Response
  notFound: () => Response
  internalServerError: () => Response
}

interface Request {
  readonly url: string
}

interface Response {
  readonly status: number
}

class ValidationError extends Data.TaggedError("ValidationError")<{
  readonly message: string
}> {}

class NotFoundError extends Data.TaggedError("NotFoundError")<{}> {}

class DatabaseError extends Data.TaggedError("DatabaseError")<{}> {}

// Define clear boundaries where errors are handled
const apiEndpoint = (request: Request) =>
  Effect.gen(function* () {
    // Business logic
    const result = yield* processRequest(request)
    return result
  }).pipe(
    // Error boundary: convert all errors to HTTP responses
    Effect.catchTags({
      ValidationError: (error) =>
        Effect.succeed(HttpResponse.badRequest(error.message)),
      NotFoundError: () =>
        Effect.succeed(HttpResponse.notFound()),
      DatabaseError: (error) =>
        Effect.logError(error).pipe(
          Effect.as(HttpResponse.internalServerError())
        )
    }),
    // Catch any unhandled errors
    Effect.catchAll((error) =>
      Effect.logError(`Unhandled error: ${error._tag}`).pipe(
        Effect.as(HttpResponse.internalServerError())
      )
    )
  )
```

Your error handling implementations should be type-safe, exhaustive, and maintain clear separation between expected failures and programmer errors.
