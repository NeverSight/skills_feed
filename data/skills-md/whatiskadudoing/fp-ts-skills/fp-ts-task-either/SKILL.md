---
name: fp-ts-task-either
description: Functional async patterns using TaskEither for type-safe error handling in TypeScript
version: 1.0.0
author: kadu
tags:
  - fp-ts
  - functional-programming
  - typescript
  - async
  - error-handling
  - task-either
  - monads
---

# fp-ts TaskEither Async Patterns

TaskEither combines the laziness of Task with the error handling of Either, providing a powerful abstraction for async operations that can fail.

## Core Concepts

```typescript
import * as TE from 'fp-ts/TaskEither'
import * as T from 'fp-ts/Task'
import * as E from 'fp-ts/Either'
import { pipe, flow } from 'fp-ts/function'
```

**TaskEither<E, A>** is equivalent to `() => Promise<Either<E, A>>`
- `E` = Error type (left)
- `A` = Success type (right)
- Lazy: nothing executes until you call the function
- Composable: chain operations without try/catch

---

## 1. Converting Promises to TaskEither

### Using tryCatch

The primary way to lift Promises into TaskEither:

```typescript
import * as TE from 'fp-ts/TaskEither'

// Basic tryCatch pattern
const fetchUser = (id: string): TE.TaskEither<Error, User> =>
  TE.tryCatch(
    () => fetch(`/api/users/${id}`).then(res => res.json()),
    (reason) => new Error(String(reason))
  )

// With typed errors
interface ApiError {
  code: string
  message: string
  status: number
}

const fetchUserTyped = (id: string): TE.TaskEither<ApiError, User> =>
  TE.tryCatch(
    () => fetch(`/api/users/${id}`).then(res => res.json()),
    (reason): ApiError => ({
      code: 'FETCH_ERROR',
      message: reason instanceof Error ? reason.message : 'Unknown error',
      status: 500
    })
  )
```

### From existing Either

```typescript
// Lift an Either into TaskEither
const fromEither: TE.TaskEither<Error, number> = TE.fromEither(E.right(42))

// From a nullable value
const fromNullable = TE.fromNullable(new Error('Value was null'))
const result = fromNullable(maybeValue) // TaskEither<Error, NonNullable<T>>

// From an Option
import * as O from 'fp-ts/Option'
const fromOption = TE.fromOption(() => new Error('None value'))
const optionResult = fromOption(O.some(42)) // TaskEither<Error, number>
```

### Creating TaskEither values directly

```typescript
// Success value
const success = TE.right<Error, number>(42)

// Error value
const failure = TE.left<Error, number>(new Error('Something failed'))

// From a predicate
const validatePositive = TE.fromPredicate(
  (n: number) => n > 0,
  (n) => new Error(`Expected positive, got ${n}`)
)
```

---

## 2. Handling Async Errors Functionally

### Mapping over errors

```typescript
// Transform the error type
const withMappedError = pipe(
  fetchUser('123'),
  TE.mapLeft((error) => ({
    type: 'USER_FETCH_ERROR' as const,
    originalError: error,
    timestamp: Date.now()
  }))
)

// Bifunctor: map both sides
const mapped = pipe(
  fetchUser('123'),
  TE.bimap(
    (error) => new DetailedError(error),  // map error
    (user) => user.profile                 // map success
  )
)
```

### Error filtering

```typescript
// Filter with error on false
const validateAge = pipe(
  fetchUser('123'),
  TE.filterOrElse(
    (user) => user.age >= 18,
    (user) => new Error(`User ${user.name} is underage`)
  )
)
```

---

## 3. Chaining Async Operations

### Sequential chaining with chain/flatMap

```typescript
interface User { id: string; name: string; teamId: string }
interface Team { id: string; name: string; orgId: string }
interface Org { id: string; name: string }

const fetchUser = (id: string): TE.TaskEither<Error, User> =>
  TE.tryCatch(() => api.getUser(id), toError)

const fetchTeam = (teamId: string): TE.TaskEither<Error, Team> =>
  TE.tryCatch(() => api.getTeam(teamId), toError)

const fetchOrg = (orgId: string): TE.TaskEither<Error, Org> =>
  TE.tryCatch(() => api.getOrg(orgId), toError)

// Chain operations sequentially
const getUserOrg = (userId: string): TE.TaskEither<Error, Org> =>
  pipe(
    fetchUser(userId),
    TE.chain((user) => fetchTeam(user.teamId)),
    TE.chain((team) => fetchOrg(team.orgId))
  )

// flatMap is an alias for chain
const getUserOrgAlt = (userId: string): TE.TaskEither<Error, Org> =>
  pipe(
    fetchUser(userId),
    TE.flatMap((user) => fetchTeam(user.teamId)),
    TE.flatMap((team) => fetchOrg(team.orgId))
  )
```

### Chaining with intermediate values

```typescript
// Use bind to accumulate values
const getFullContext = (userId: string) =>
  pipe(
    TE.Do,
    TE.bind('user', () => fetchUser(userId)),
    TE.bind('team', ({ user }) => fetchTeam(user.teamId)),
    TE.bind('org', ({ team }) => fetchOrg(team.orgId)),
    TE.map(({ user, team, org }) => ({
      userName: user.name,
      teamName: team.name,
      orgName: org.name
    }))
  )
```

---

## 4. Parallel vs Sequential Execution

### Parallel execution with sequenceArray

```typescript
import * as A from 'fp-ts/Array'

const userIds = ['1', '2', '3', '4', '5']

// Parallel: all requests start immediately
// Fails fast: returns first error encountered
const fetchAllUsersParallel = pipe(
  userIds.map(fetchUser),
  TE.sequenceArray  // TaskEither<Error, readonly User[]>
)

// Sequential: one at a time (use when order matters or rate limiting)
const fetchAllUsersSequential = pipe(
  userIds,
  A.traverse(TE.ApplicativeSeq)(fetchUser)
)
```

### Parallel with traverseArray

```typescript
// More idiomatic: traverse combines map + sequence
const fetchAllUsers = (ids: string[]): TE.TaskEither<Error, readonly User[]> =>
  pipe(ids, TE.traverseArray(fetchUser))

// With index
const fetchWithIndex = pipe(
  userIds,
  TE.traverseArrayWithIndex((index, id) =>
    pipe(
      fetchUser(id),
      TE.map(user => ({ ...user, index }))
    )
  )
)
```

### Collecting all errors vs fail fast

```typescript
import * as These from 'fp-ts/These'
import * as TH from 'fp-ts/TaskThese'

// For collecting all errors, consider TaskThese
// Or use validation with sequenceT

import { sequenceT } from 'fp-ts/Apply'

// Parallel execution, collects results
const parallel = sequenceT(TE.ApplyPar)(
  fetchUser('1'),
  fetchTeam('team-1'),
  fetchOrg('org-1')
) // TaskEither<Error, [User, Team, Org]>

// Sequential execution
const sequential = sequenceT(TE.ApplySeq)(
  fetchUser('1'),
  fetchTeam('team-1'),
  fetchOrg('org-1')
)
```

### Concurrent with limit

```typescript
// For controlled concurrency, batch your operations
const batchSize = 3

const fetchInBatches = (ids: string[]): TE.TaskEither<Error, User[]> => {
  const batches = chunk(ids, batchSize)

  return pipe(
    batches,
    A.traverse(TE.ApplicativeSeq)((batch) =>
      pipe(batch, TE.traverseArray(fetchUser))
    ),
    TE.map(A.flatten)
  )
}
```

---

## 5. Error Recovery with orElse

### Basic error recovery

```typescript
// Try primary, fall back to secondary
const fetchWithFallback = pipe(
  fetchFromPrimaryApi(id),
  TE.orElse((primaryError) =>
    pipe(
      fetchFromBackupApi(id),
      TE.mapLeft((backupError) => ({
        primary: primaryError,
        backup: backupError
      }))
    )
  )
)

// Recover to a default value
const fetchWithDefault = pipe(
  fetchUser(id),
  TE.orElse(() => TE.right(defaultUser))
)

// orElseW when recovery has different error type
const fetchWithTypedFallback = pipe(
  fetchFromApi(id),           // TaskEither<ApiError, User>
  TE.orElseW((apiError) =>    // orElseW allows different error type
    fetchFromCache(id)         // TaskEither<CacheError, User>
  )
) // TaskEither<CacheError, User>
```

### Retry patterns

```typescript
const retry = <E, A>(
  te: TE.TaskEither<E, A>,
  retries: number,
  delay: number
): TE.TaskEither<E, A> =>
  pipe(
    te,
    TE.orElse((error) =>
      retries > 0
        ? pipe(
            T.delay(delay)(T.of(undefined)),
            T.chain(() => retry(te, retries - 1, delay * 2))
          )
        : TE.left(error)
    )
  )

// Usage
const fetchWithRetry = retry(fetchUser('123'), 3, 1000)
```

### Conditional recovery

```typescript
// Only recover from specific errors
const recoverFromNotFound = pipe(
  fetchUser(id),
  TE.orElse((error) =>
    error.code === 'NOT_FOUND'
      ? TE.right(createDefaultUser(id))
      : TE.left(error)  // re-throw other errors
  )
)

// Alt: try alternatives in order
import { alt } from 'fp-ts/TaskEither'

const fetchFromAnywhere = pipe(
  fetchFromCache(id),
  TE.alt(() => fetchFromApi(id)),
  TE.alt(() => fetchFromBackup(id))
)
```

---

## 6. Pattern Matching Async Results

### Using fold/match

```typescript
// fold executes the TaskEither and handles both cases
const handleResult = pipe(
  fetchUser('123'),
  TE.fold(
    (error) => T.of(`Error: ${error.message}`),
    (user) => T.of(`Welcome, ${user.name}`)
  )
) // Task<string> - no longer has error channel

// match is an alias for fold
const handleWithMatch = pipe(
  fetchUser('123'),
  TE.match(
    (error) => ({ success: false, error }),
    (user) => ({ success: true, data: user })
  )
)

// matchW when handlers return different types
const handleWithMatchW = pipe(
  fetchUser('123'),
  TE.matchW(
    (error) => ({ type: 'error' as const, error }),
    (user) => ({ type: 'success' as const, user })
  )
)
```

### Getting the underlying Either

```typescript
// Execute and get the Either
const getEither = async () => {
  const either = await fetchUser('123')()

  if (E.isLeft(either)) {
    console.error('Failed:', either.left)
  } else {
    console.log('User:', either.right)
  }
}

// Using getOrElse for default
const getWithDefault = pipe(
  fetchUser('123'),
  TE.getOrElse((error) => T.of(defaultUser))
) // Task<User>

// getOrElseW when default has different type
const getOrNull = pipe(
  fetchUser('123'),
  TE.getOrElseW(() => T.of(null))
) // Task<User | null>
```

---

## 7. Do Notation for Complex Workflows

### Building complex operations

```typescript
interface OrderContext {
  user: User
  cart: Cart
  payment: PaymentMethod
  shipping: ShippingAddress
}

const processOrder = (
  userId: string,
  cartId: string
): TE.TaskEither<OrderError, OrderConfirmation> =>
  pipe(
    TE.Do,
    // Bind values sequentially
    TE.bind('user', () => fetchUser(userId)),
    TE.bind('cart', () => fetchCart(cartId)),

    // Validate intermediate results
    TE.filterOrElse(
      ({ cart }) => cart.items.length > 0,
      () => ({ code: 'EMPTY_CART', message: 'Cart is empty' })
    ),

    // Continue building context
    TE.bind('payment', ({ user }) => getDefaultPayment(user.id)),
    TE.bind('shipping', ({ user }) => getDefaultShipping(user.id)),

    // Calculate derived values
    TE.bind('total', ({ cart }) => TE.right(calculateTotal(cart))),

    // Validate before final operation
    TE.filterOrElse(
      ({ payment, total }) => payment.limit >= total,
      ({ total }) => ({ code: 'LIMIT_EXCEEDED', message: `Order total ${total} exceeds limit` })
    ),

    // Final operation
    TE.chain(({ user, cart, payment, shipping, total }) =>
      createOrder({ user, cart, payment, shipping, total })
    )
  )
```

### Parallel fetching within Do

```typescript
const getOrderDetails = (orderId: string) =>
  pipe(
    TE.Do,
    TE.bind('order', () => fetchOrder(orderId)),

    // Parallel fetch based on order data
    TE.bind('details', ({ order }) =>
      sequenceT(TE.ApplyPar)(
        fetchUser(order.userId),
        fetchProducts(order.productIds),
        fetchShipping(order.shippingId)
      )
    ),

    TE.map(({ order, details: [user, products, shipping] }) => ({
      order,
      user,
      products,
      shipping
    }))
  )
```

### Using apS for simpler additions

```typescript
// apS is like bind but doesn't depend on previous values
const enrichUser = (userId: string) =>
  pipe(
    fetchUser(userId),
    TE.bindTo('user'),  // Wrap in { user: ... }
    TE.apS('config', fetchAppConfig()),  // Add independent value
    TE.apS('features', fetchFeatureFlags()),
    TE.bind('preferences', ({ user }) => fetchPreferences(user.id))  // Dependent
  )
```

---

## 8. Real-World API Call Patterns

### Typed API client

```typescript
interface ApiConfig {
  baseUrl: string
  timeout: number
}

interface ApiError {
  code: string
  message: string
  status: number
  details?: unknown
}

const createApiClient = (config: ApiConfig) => {
  const request = <T>(
    method: string,
    path: string,
    body?: unknown
  ): TE.TaskEither<ApiError, T> =>
    TE.tryCatch(
      async () => {
        const response = await fetch(`${config.baseUrl}${path}`, {
          method,
          headers: { 'Content-Type': 'application/json' },
          body: body ? JSON.stringify(body) : undefined,
          signal: AbortSignal.timeout(config.timeout)
        })

        if (!response.ok) {
          const error = await response.json().catch(() => ({}))
          throw { status: response.status, ...error }
        }

        return response.json()
      },
      (error): ApiError => ({
        code: 'API_ERROR',
        message: error instanceof Error ? error.message : 'Request failed',
        status: (error as any)?.status ?? 500,
        details: error
      })
    )

  return {
    get: <T>(path: string) => request<T>('GET', path),
    post: <T>(path: string, body: unknown) => request<T>('POST', path, body),
    put: <T>(path: string, body: unknown) => request<T>('PUT', path, body),
    delete: <T>(path: string) => request<T>('DELETE', path)
  }
}

// Usage
const api = createApiClient({ baseUrl: '/api', timeout: 5000 })

const getUser = (id: string) => api.get<User>(`/users/${id}`)
const createUser = (data: CreateUserDto) => api.post<User>('/users', data)
```

### Request with validation

```typescript
import * as t from 'io-ts'
import { PathReporter } from 'io-ts/PathReporter'

const UserCodec = t.type({
  id: t.string,
  name: t.string,
  email: t.string
})

type User = t.TypeOf<typeof UserCodec>

const fetchAndValidate = <A>(
  codec: t.Type<A>,
  url: string
): TE.TaskEither<Error, A> =>
  pipe(
    TE.tryCatch(
      () => fetch(url).then(r => r.json()),
      (e) => new Error(`Fetch failed: ${e}`)
    ),
    TE.chainEitherK((data) =>
      pipe(
        codec.decode(data),
        E.mapLeft((errors) =>
          new Error(`Validation failed: ${PathReporter.report(E.left(errors)).join(', ')}`)
        )
      )
    )
  )

const getValidatedUser = (id: string) =>
  fetchAndValidate(UserCodec, `/api/users/${id}`)
```

---

## 9. Database Operation Patterns

### Repository pattern

```typescript
interface Repository<E, T, ID> {
  findById: (id: ID) => TE.TaskEither<E, T>
  findAll: () => TE.TaskEither<E, readonly T[]>
  save: (entity: T) => TE.TaskEither<E, T>
  delete: (id: ID) => TE.TaskEither<E, void>
}

interface DbError {
  code: 'NOT_FOUND' | 'DUPLICATE' | 'CONSTRAINT' | 'CONNECTION'
  message: string
  cause?: unknown
}

const createUserRepository = (db: Database): Repository<DbError, User, string> => ({
  findById: (id) =>
    pipe(
      TE.tryCatch(
        () => db.query('SELECT * FROM users WHERE id = ?', [id]),
        (e): DbError => ({ code: 'CONNECTION', message: String(e), cause: e })
      ),
      TE.chain((rows) =>
        rows.length === 0
          ? TE.left({ code: 'NOT_FOUND', message: `User ${id} not found` })
          : TE.right(rows[0] as User)
      )
    ),

  findAll: () =>
    TE.tryCatch(
      () => db.query('SELECT * FROM users'),
      (e): DbError => ({ code: 'CONNECTION', message: String(e), cause: e })
    ),

  save: (user) =>
    TE.tryCatch(
      () => db.query(
        'INSERT INTO users (id, name, email) VALUES (?, ?, ?) ON CONFLICT (id) DO UPDATE SET name = ?, email = ?',
        [user.id, user.name, user.email, user.name, user.email]
      ).then(() => user),
      (e): DbError => {
        if (String(e).includes('UNIQUE constraint')) {
          return { code: 'DUPLICATE', message: 'Email already exists', cause: e }
        }
        return { code: 'CONNECTION', message: String(e), cause: e }
      }
    ),

  delete: (id) =>
    TE.tryCatch(
      () => db.query('DELETE FROM users WHERE id = ?', [id]).then(() => undefined),
      (e): DbError => ({ code: 'CONNECTION', message: String(e), cause: e })
    )
})
```

### Transaction handling

```typescript
interface Transaction {
  query: (sql: string, params?: unknown[]) => Promise<unknown>
  commit: () => Promise<void>
  rollback: () => Promise<void>
}

const withTransaction = <E, A>(
  db: Database,
  operation: (tx: Transaction) => TE.TaskEither<E, A>
): TE.TaskEither<E | DbError, A> =>
  pipe(
    TE.tryCatch(
      () => db.beginTransaction(),
      (e): DbError => ({ code: 'CONNECTION', message: 'Failed to start transaction', cause: e })
    ),
    TE.chain((tx) =>
      pipe(
        operation(tx),
        TE.chainFirst(() =>
          TE.tryCatch(
            () => tx.commit(),
            (e): DbError => ({ code: 'CONNECTION', message: 'Commit failed', cause: e })
          )
        ),
        TE.orElse((error) =>
          pipe(
            TE.tryCatch(() => tx.rollback(), () => error),
            TE.chain(() => TE.left(error))
          )
        )
      )
    )
  )

// Usage
const transferFunds = (fromId: string, toId: string, amount: number) =>
  withTransaction(db, (tx) =>
    pipe(
      TE.Do,
      TE.bind('from', () => getAccount(tx, fromId)),
      TE.bind('to', () => getAccount(tx, toId)),
      TE.filterOrElse(
        ({ from }) => from.balance >= amount,
        () => ({ code: 'INSUFFICIENT_FUNDS', message: 'Not enough balance' })
      ),
      TE.chain(({ from, to }) =>
        sequenceT(TE.ApplySeq)(
          updateBalance(tx, fromId, from.balance - amount),
          updateBalance(tx, toId, to.balance + amount)
        )
      ),
      TE.map(() => ({ success: true, amount }))
    )
  )
```

---

## 10. Task vs TaskEither: When to Use Which

### Use Task when:

```typescript
import * as T from 'fp-ts/Task'

// 1. Operation cannot fail
const delay = (ms: number): T.Task<void> =>
  () => new Promise(resolve => setTimeout(resolve, ms))

// 2. Errors are handled elsewhere
const logMessage = (msg: string): T.Task<void> =>
  () => console.log(msg) as unknown as Promise<void>

// 3. You want to ignore errors
const fetchOrDefault = (url: string, defaultValue: Data): T.Task<Data> =>
  pipe(
    TE.tryCatch(() => fetch(url).then(r => r.json()), E.toError),
    TE.getOrElse(() => T.of(defaultValue))
  )

// 4. Fire and forget
const trackAnalytics = (event: Event): T.Task<void> =>
  () => analytics.track(event).catch(() => {}) // Errors swallowed
```

### Use TaskEither when:

```typescript
// 1. Operation can fail and you need to handle the error
const fetchUser = (id: string): TE.TaskEither<Error, User> =>
  TE.tryCatch(() => api.getUser(id), E.toError)

// 2. You need typed errors for different failure modes
type AuthError =
  | { type: 'INVALID_CREDENTIALS' }
  | { type: 'EXPIRED_TOKEN' }
  | { type: 'NETWORK_ERROR'; cause: Error }

const authenticate = (token: string): TE.TaskEither<AuthError, User> => { /* ... */ }

// 3. Error recovery is part of business logic
const getConfig = (): TE.TaskEither<ConfigError, Config> =>
  pipe(
    fetchRemoteConfig(),
    TE.orElse(() => loadLocalConfig()),
    TE.orElse(() => TE.right(defaultConfig))
  )

// 4. Composing multiple fallible operations
const processOrder = (orderId: string): TE.TaskEither<OrderError, Receipt> =>
  pipe(
    validateOrder(orderId),
    TE.chain(chargePayment),
    TE.chain(fulfillOrder),
    TE.chain(sendConfirmation)
  )
```

### Converting between them

```typescript
// Task to TaskEither (infallible to fallible)
const taskToTE = <A>(task: T.Task<A>): TE.TaskEither<never, A> =>
  pipe(task, T.map(E.right))

// TaskEither to Task (handle/ignore error)
const teToTask = <E, A>(te: TE.TaskEither<E, A>, defaultValue: A): T.Task<A> =>
  TE.getOrElse(() => T.of(defaultValue))(te)

// TaskEither to Task (throw on error - escape hatch)
const teToTaskThrow = <E, A>(te: TE.TaskEither<E, A>): T.Task<A> =>
  pipe(
    te,
    TE.getOrElse((e) => () => Promise.reject(e))
  )
```

---

## Quick Reference

| Operation | Function | Description |
|-----------|----------|-------------|
| Create success | `TE.right(value)` | Wrap value in Right |
| Create failure | `TE.left(error)` | Wrap error in Left |
| From Promise | `TE.tryCatch(promise, onError)` | Convert Promise to TE |
| Transform value | `TE.map(f)` | Apply f to success value |
| Transform error | `TE.mapLeft(f)` | Apply f to error value |
| Chain operations | `TE.chain(f)` / `TE.flatMap(f)` | Sequence dependent operations |
| Recover from error | `TE.orElse(f)` | Try alternative on error |
| Handle both cases | `TE.fold(onError, onSuccess)` | Pattern match result |
| Parallel array | `TE.traverseArray(f)` | Map + sequence in parallel |
| Sequential array | `A.traverse(TE.ApplicativeSeq)(f)` | Map + sequence in order |
| Filter with error | `TE.filterOrElse(pred, onFalse)` | Validate with error |
| Get or default | `TE.getOrElse(onError)` | Extract value with fallback |

---

## Common Patterns Summary

```typescript
// 1. Fetch with error handling
const fetch = TE.tryCatch(() => api.get(url), toError)

// 2. Chain dependent calls
pipe(getA(), TE.chain(a => getB(a.id)), TE.chain(b => getC(b.id)))

// 3. Parallel independent calls
sequenceT(TE.ApplyPar)(getA(), getB(), getC())

// 4. Build context with Do
pipe(TE.Do, TE.bind('a', () => getA()), TE.bind('b', ({a}) => getB(a)))

// 5. Recover from errors
pipe(primary(), TE.orElse(() => fallback()))

// 6. Execute and handle result
pipe(operation(), TE.fold(handleError, handleSuccess))()
```
