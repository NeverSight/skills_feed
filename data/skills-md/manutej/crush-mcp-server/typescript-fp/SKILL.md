---
name: typescript-fp
description: Master functional programming in TypeScript with type-safe patterns, strict typing, advanced type system features, discriminated unions, mapped types, conditional types, and functional patterns. Use when writing TypeScript code with functional paradigms, type-safe error handling with Option/Either types, implementing type-safe composition, leveraging TypeScript's type system for functional patterns, or ensuring compile-time safety in functional code.
---

# Functional Programming in TypeScript

## The Zen of Functional Programming in TypeScript

**Types are truth**
The type system is your first and best test; trust it, extend it, let it guide refactoring.

**Functions, not methods**
Favor pure, standalone functions over mutating methods. Logic and data are better apart.

**Compose, don't construct**
Build complex behavior by wiring small functions, not by inheritance or sprawling classes.

**Immutability is clarity**
Changing data increases entropy; prefer readonly and new values.

**Explicit is safety**
Encode nullable, optional, and error-prone states as explicit types: Option, Either, custom unions.

**Pipelines flow clearly**
Use composition (pipe, flow) to make data transformations readable and reasoned about at a glance.

**Effects are contained**
Push side effects to the edge. Pure in the middle, async/io only when necessary and clearly isolated.

**Type errors are friends**
If code doesn't type-check, it's not safe—fix it at compile time, not at runtime.

**Libraries are bridges**
Leverage fp-ts, purify, and effect libraries—they bring the best of ML/Haskell/Scala worlds without leaving TypeScript.

**The simplest solution wins**
If achievable by composing two pure functions, resist the urge for classes, frameworks, or lifecycles.

**There is no 'any' in zen**
Avoid any: prefer unknown, never, or expressive unions. Demand and supply information with care.

**Pattern match with safety**
Discriminated unions and pattern matching are clearer than chains of if/else or error-prone casts.

**Refactor fearlessly**
Small, pure, and well-typed functions invite confident change—use types as a foundation for safety.

**Embrace strictness**
strict: true and linting are not obstacles—they are the clearest guides on the path to quality.

## TypeScript Configuration for FP

### tsconfig.json

```json
{
  "compilerOptions": {
    "strict": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitAny": true,
    "noImplicitThis": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noPropertyAccessFromIndexSignature": true,
    "allowUnusedLabels": false,
    "allowUnreachableCode": false,
    "target": "ES2022",
    "lib": ["ES2022"],
    "module": "ES2022",
    "moduleResolution": "bundler"
  }
}
```

### ESLint Configuration

```javascript
module.exports = {
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:functional/recommended'
  ],
  plugins: ['@typescript-eslint', 'functional'],
  rules: {
    'functional/no-let': 'error',
    'functional/no-loop-statement': 'error',
    'functional/no-mutation': 'error',
    'functional/prefer-readonly-type': 'error',
    'functional/immutable-data': 'error',
    'functional/no-throw-statement': 'error',
    'functional/no-class': 'warn',
    'functional/no-this': 'warn',
    '@typescript-eslint/no-explicit-any': 'error',
    'prefer-const': 'error'
  }
};
```

## Type System Features for FP

### Advanced Type Utilities

```typescript
// Readonly deeply nested structures
type DeepReadonly<T> = T extends Primitive
  ? T
  : T extends Array<infer U>
  ? ReadonlyArray<DeepReadonly<U>>
  : T extends Map<infer K, infer V>
  ? ReadonlyMap<DeepReadonly<K>, DeepReadonly<V>>
  : T extends Set<infer U>
  ? ReadonlySet<DeepReadonly<U>>
  : { readonly [K in keyof T]: DeepReadonly<T[K]> };

type Primitive = string | number | boolean | bigint | symbol | null | undefined;

// Extract function return type
type ReturnTypeOf<F> = F extends (...args: any[]) => infer R ? R : never;

// Extract function argument types
type ArgumentsOf<F> = F extends (...args: infer A) => any ? A : never;

// Make specific properties optional
type PartialBy<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>;

// Make specific properties required
type RequiredBy<T, K extends keyof T> = Omit<T, K> & Required<Pick<T, K>>;

// Union to intersection
type UnionToIntersection<U> = 
  (U extends any ? (k: U) => void : never) extends 
  (k: infer I) => void ? I : never;

// Get keys where value type matches
type KeysOfType<T, V> = {
  [K in keyof T]: T[K] extends V ? K : never;
}[keyof T];

// NonEmptyArray type
type NonEmptyArray<T> = [T, ...T[]];

// Brand types for type safety
declare const brand: unique symbol;
type Brand<T, B> = T & { readonly [brand]: B };

type UserId = Brand<string, 'UserId'>;
type Email = Brand<string, 'Email'>;

const makeUserId = (id: string): UserId => id as UserId;
const makeEmail = (email: string): Email => email as Email;
```

### Discriminated Unions

```typescript
// Basic discriminated union
type Shape =
  | { kind: 'circle'; radius: number }
  | { kind: 'rectangle'; width: number; height: number }
  | { kind: 'square'; size: number };

const area = (shape: Shape): number => {
  switch (shape.kind) {
    case 'circle':
      return Math.PI * shape.radius ** 2;
    case 'rectangle':
      return shape.width * shape.height;
    case 'square':
      return shape.size ** 2;
  }
};

// Result type with discriminated union
type Result<E, A> =
  | { readonly _tag: 'Left'; readonly left: E }
  | { readonly _tag: 'Right'; readonly right: A };

const Left = <E, A = never>(left: E): Result<E, A> => 
  ({ _tag: 'Left', left });

const Right = <A, E = never>(right: A): Result<E, A> => 
  ({ _tag: 'Right', right });

// Type-safe pattern matching
const matchResult = <E, A, B>(
  result: Result<E, A>,
  patterns: {
    Left: (error: E) => B;
    Right: (value: A) => B;
  }
): B =>
  result._tag === 'Left' 
    ? patterns.Left(result.left) 
    : patterns.Right(result.right);
```

### Mapped Types

```typescript
// Make all properties optional recursively
type DeepPartial<T> = T extends Primitive
  ? T
  : T extends Array<infer U>
  ? Array<DeepPartial<U>>
  : T extends ReadonlyArray<infer U>
  ? ReadonlyArray<DeepPartial<U>>
  : { [K in keyof T]?: DeepPartial<T[K]> };

// Make all properties readonly recursively
type DeepReadonlyMap<T> = {
  readonly [K in keyof T]: DeepReadonly<T[K]>;
};

// Pick properties that are functions
type FunctionProperties<T> = Pick<T, KeysOfType<T, Function>>;

// Pick properties that are not functions
type NonFunctionProperties<T> = Pick<T, Exclude<keyof T, KeysOfType<T, Function>>>;

// Convert all methods to readonly functions
type ReadonlyMethods<T> = {
  readonly [K in keyof T]: T[K] extends (...args: infer A) => infer R
    ? (...args: A) => R
    : T[K];
};
```

### Conditional Types

```typescript
// Unwrap Promise type
type Awaited<T> = T extends Promise<infer U> ? Awaited<U> : T;

// Check if type is exactly a certain type
type IsExact<T, U> = 
  (<G>() => G extends T ? 1 : 2) extends 
  (<G>() => G extends U ? 1 : 2) ? true : false;

// Filter nullable values from union
type NonNullableFields<T> = {
  [K in keyof T]: NonNullable<T[K]>;
};

// Conditional required fields
type RequiredFields<T> = {
  [K in keyof T as T[K] extends Required<T>[K] ? K : never]: T[K];
};

// Conditional optional fields
type OptionalFields<T> = {
  [K in keyof T as T[K] extends Required<T>[K] ? never : K]: T[K];
};
```

## Option Type Implementation

```typescript
// Option type definition
type Option<A> =
  | { readonly _tag: 'None' }
  | { readonly _tag: 'Some'; readonly value: A };

// Constructors
const None = <A = never>(): Option<A> => ({ _tag: 'None' });

const Some = <A>(value: A): Option<A> => ({ _tag: 'Some', value });

// Type guards
const isNone = <A>(opt: Option<A>): opt is { _tag: 'None' } => 
  opt._tag === 'None';

const isSome = <A>(opt: Option<A>): opt is { _tag: 'Some'; value: A } => 
  opt._tag === 'Some';

// Core operations
const map = <A, B>(opt: Option<A>, f: (a: A) => B): Option<B> =>
  isSome(opt) ? Some(f(opt.value)) : None();

const flatMap = <A, B>(opt: Option<A>, f: (a: A) => Option<B>): Option<B> =>
  isSome(opt) ? f(opt.value) : None();

const getOrElse = <A>(opt: Option<A>, defaultValue: A): A =>
  isSome(opt) ? opt.value : defaultValue;

const fold = <A, B>(
  opt: Option<A>,
  onNone: () => B,
  onSome: (a: A) => B
): B =>
  isSome(opt) ? onSome(opt.value) : onNone();

// Convert from nullable
const fromNullable = <A>(value: A | null | undefined): Option<A> =>
  value == null ? None() : Some(value);

// Convert to nullable
const toNullable = <A>(opt: Option<A>): A | null =>
  isSome(opt) ? opt.value : null;

// Filter
const filter = <A>(opt: Option<A>, pred: (a: A) => boolean): Option<A> =>
  isSome(opt) && pred(opt.value) ? opt : None();

// Chaining operations
const pipe = <A>(opt: Option<A>) => ({
  map: <B>(f: (a: A) => B) => pipe(map(opt, f)),
  flatMap: <B>(f: (a: A) => Option<B>) => pipe(flatMap(opt, f)),
  filter: (pred: (a: A) => boolean) => pipe(filter(opt, pred)),
  getOrElse: (defaultValue: A): A => getOrElse(opt, defaultValue),
  fold: <B>(onNone: () => B, onSome: (a: A) => B): B => 
    fold(opt, onNone, onSome)
});

// Usage example
const safeDivide = (a: number, b: number): Option<number> =>
  b === 0 ? None() : Some(a / b);

const result = pipe(safeDivide(10, 2))
  .map(x => x * 2)
  .filter(x => x > 5)
  .getOrElse(0);
```

## Either Type Implementation

```typescript
// Either type definition
type Either<E, A> =
  | { readonly _tag: 'Left'; readonly left: E }
  | { readonly _tag: 'Right'; readonly right: A };

// Constructors
const Left = <E, A = never>(left: E): Either<E, A> => 
  ({ _tag: 'Left', left });

const Right = <A, E = never>(right: A): Either<E, A> => 
  ({ _tag: 'Right', right });

// Type guards
const isLeft = <E, A>(either: Either<E, A>): either is { _tag: 'Left'; left: E } =>
  either._tag === 'Left';

const isRight = <E, A>(either: Either<E, A>): either is { _tag: 'Right'; right: A } =>
  either._tag === 'Right';

// Core operations
const mapEither = <E, A, B>(
  either: Either<E, A>,
  f: (a: A) => B
): Either<E, B> =>
  isRight(either) ? Right(f(either.right)) : either;

const mapLeft = <E, A, F>(
  either: Either<E, A>,
  f: (e: E) => F
): Either<F, A> =>
  isLeft(either) ? Left(f(either.left)) : either;

const flatMapEither = <E, A, B>(
  either: Either<E, A>,
  f: (a: A) => Either<E, B>
): Either<E, B> =>
  isRight(either) ? f(either.right) : either;

const foldEither = <E, A, B>(
  either: Either<E, A>,
  onLeft: (e: E) => B,
  onRight: (a: A) => B
): B =>
  isLeft(either) ? onLeft(either.left) : onRight(either.right);

const getOrElseEither = <E, A>(
  either: Either<E, A>,
  onLeft: (e: E) => A
): A =>
  isLeft(either) ? onLeft(either.left) : either.right;

const swap = <E, A>(either: Either<E, A>): Either<A, E> =>
  isLeft(either) ? Right(either.left) : Left(either.right);

// Try-catch wrapper
const tryCatch = <A>(
  f: () => A,
  onError: (error: unknown) => Error = e => 
    e instanceof Error ? e : new Error(String(e))
): Either<Error, A> => {
  try {
    return Right(f());
  } catch (error) {
    return Left(onError(error));
  }
};

// Async variant
const tryCatchAsync = async <A>(
  f: () => Promise<A>,
  onError: (error: unknown) => Error = e => 
    e instanceof Error ? e : new Error(String(e))
): Promise<Either<Error, A>> => {
  try {
    return Right(await f());
  } catch (error) {
    return Left(onError(error));
  }
};

// Chaining operations
const pipeEither = <E, A>(either: Either<E, A>) => ({
  map: <B>(f: (a: A) => B) => pipeEither(mapEither(either, f)),
  mapLeft: <F>(f: (e: E) => F) => pipeEither(mapLeft(either, f)),
  flatMap: <B>(f: (a: A) => Either<E, B>) => pipeEither(flatMapEither(either, f)),
  fold: <B>(onLeft: (e: E) => B, onRight: (a: A) => B): B => 
    foldEither(either, onLeft, onRight),
  getOrElse: (onLeft: (e: E) => A): A => 
    getOrElseEither(either, onLeft),
  swap: () => pipeEither(swap(either))
});

// Usage example
const parseJSON = <A>(json: string): Either<Error, A> =>
  tryCatch(() => JSON.parse(json));

const validateUser = (data: unknown): Either<Error, User> => {
  if (typeof data !== 'object' || data === null) {
    return Left(new Error('Invalid data'));
  }
  // Validation logic...
  return Right(data as User);
};

const result = pipeEither(parseJSON<unknown>(jsonString))
  .flatMap(validateUser)
  .map(user => ({ ...user, name: user.name.toUpperCase() }))
  .fold(
    error => `Error: ${error.message}`,
    user => `Success: ${user.name}`
  );
```

## Function Composition Utilities

```typescript
// Compose (right-to-left)
function compose<A, B>(f: (a: A) => B): (a: A) => B;
function compose<A, B, C>(
  f: (b: B) => C,
  g: (a: A) => B
): (a: A) => C;
function compose<A, B, C, D>(
  f: (c: C) => D,
  g: (b: B) => C,
  h: (a: A) => B
): (a: A) => D;
function compose(...fns: Function[]): Function {
  return (x: any) => fns.reduceRight((acc, fn) => fn(acc), x);
}

// Pipe (left-to-right)
function pipe<A>(a: A): A;
function pipe<A, B>(a: A, f: (a: A) => B): B;
function pipe<A, B, C>(
  a: A,
  f: (a: A) => B,
  g: (b: B) => C
): C;
function pipe<A, B, C, D>(
  a: A,
  f: (a: A) => B,
  g: (b: B) => C,
  h: (c: C) => D
): D;
function pipe(a: any, ...fns: Function[]): any {
  return fns.reduce((acc, fn) => fn(acc), a);
}

// Flow (function composition)
function flow<A, B>(f: (a: A) => B): (a: A) => B;
function flow<A, B, C>(
  f: (a: A) => B,
  g: (b: B) => C
): (a: A) => C;
function flow<A, B, C, D>(
  f: (a: A) => B,
  g: (b: B) => C,
  h: (c: C) => D
): (a: A) => D;
function flow(...fns: Function[]): Function {
  return (x: any) => fns.reduce((acc, fn) => fn(acc), x);
}

// Usage examples
const double = (n: number): number => n * 2;
const increment = (n: number): number => n + 1;
const toString = (n: number): string => n.toString();

const processNumber = flow(double, increment, toString);
processNumber(5); // "11"

const result = pipe(
  5,
  double,
  increment,
  toString
); // "11"
```

## Async/Promise Utilities

```typescript
// TaskEither for async operations with error handling
type TaskEither<E, A> = () => Promise<Either<E, A>>;

const taskEitherOf = <E, A>(value: A): TaskEither<E, A> =>
  async () => Right(value);

const taskEitherFromPromise = <A>(
  promise: () => Promise<A>,
  onError: (error: unknown) => Error
): TaskEither<Error, A> =>
  async () => tryCatchAsync(promise, onError);

const mapTaskEither = <E, A, B>(
  task: TaskEither<E, A>,
  f: (a: A) => B
): TaskEither<E, B> =>
  async () => {
    const either = await task();
    return mapEither(either, f);
  };

const flatMapTaskEither = <E, A, B>(
  task: TaskEither<E, A>,
  f: (a: A) => TaskEither<E, B>
): TaskEither<E, B> =>
  async () => {
    const either = await task();
    if (isLeft(either)) return either;
    return f(either.right)();
  };

// Parallel execution
const sequenceTaskEither = <E, A>(
  tasks: readonly TaskEither<E, A>[]
): TaskEither<E, readonly A[]> =>
  async () => {
    const results = await Promise.all(tasks.map(t => t()));
    const lefts = results.filter(isLeft);
    if (lefts.length > 0) return lefts[0];
    return Right(results.map(r => (r as any).right));
  };

// Usage example
const fetchUser = (id: number): TaskEither<Error, User> =>
  taskEitherFromPromise(
    () => fetch(`/api/users/${id}`).then(r => r.json()),
    e => new Error(`Failed to fetch user: ${e}`)
  );

const processUser = flow(
  fetchUser,
  te => mapTaskEither(te, user => ({ ...user, processed: true }))
);
```

## Lens Pattern for Immutable Updates

```typescript
// Lens type
type Lens<S, A> = {
  get: (s: S) => A;
  set: (a: A) => (s: S) => S;
};

// Create lens
const lens = <S, A>(
  get: (s: S) => A,
  set: (a: A) => (s: S) => S
): Lens<S, A> => ({ get, set });

// Modify through lens
const modify = <S, A>(
  lens: Lens<S, A>,
  f: (a: A) => A
): ((s: S) => S) =>
  s => lens.set(f(lens.get(s)))(s);

// Compose lenses
const composeLens = <S, A, B>(
  outer: Lens<S, A>,
  inner: Lens<A, B>
): Lens<S, B> =>
  lens(
    s => inner.get(outer.get(s)),
    b => s => outer.set(inner.set(b)(outer.get(s)))(s)
  );

// Property lens helper
const prop = <S, K extends keyof S>(key: K): Lens<S, S[K]> =>
  lens(
    s => s[key],
    value => s => ({ ...s, [key]: value })
  );

// Usage example
type Address = { street: string; city: string };
type Person = { name: string; address: Address };

const addressLens = prop<Person, 'address'>('address');
const cityLens = prop<Address, 'city'>('city');
const personCityLens = composeLens(addressLens, cityLens);

const person: Person = {
  name: 'John',
  address: { street: '123 Main St', city: 'NYC' }
};

const updatedPerson = modify(personCityLens, () => 'LA')(person);
```

## Validation Pattern

```typescript
// Validation type
type Validation<E, A> = Either<readonly E[], A>;

const success = <E, A>(value: A): Validation<E, A> => Right(value);
const failure = <E, A>(errors: readonly E[]): Validation<E, A> => Left(errors);

// Applicative validation (accumulates errors)
const validateApply = <E, A, B>(
  vf: Validation<E, (a: A) => B>,
  va: Validation<E, A>
): Validation<E, B> => {
  if (isLeft(vf) && isLeft(va)) {
    return Left([...vf.left, ...va.left]);
  }
  if (isLeft(vf)) return vf as any;
  if (isLeft(va)) return va as any;
  return Right(vf.right(va.right));
};

// Validation builder
const validate = <A>(value: A) => ({
  check: <E>(
    pred: (a: A) => boolean,
    error: E
  ): Validation<E, A> =>
    pred(value) ? success(value) : failure([error]),
  
  checkAsync: async <E>(
    pred: (a: A) => Promise<boolean>,
    error: E
  ): Promise<Validation<E, A>> =>
    (await pred(value)) ? success(value) : failure([error])
});

// Combine validations
const combineValidations = <E, A extends readonly any[]>(
  ...validations: { [K in keyof A]: Validation<E, A[K]> }
): Validation<E, A> => {
  const errors: E[] = [];
  const values: any[] = [];
  
  for (const v of validations) {
    if (isLeft(v)) {
      errors.push(...v.left);
    } else {
      values.push(v.right);
    }
  }
  
  return errors.length > 0 ? Left(errors) : Right(values as any);
};

// Usage example
type ValidationError = { field: string; message: string };

const validateEmail = (email: string): Validation<ValidationError, string> =>
  validate(email)
    .check(
      e => e.includes('@'),
      { field: 'email', message: 'Must contain @' }
    );

const validateAge = (age: number): Validation<ValidationError, number> =>
  validate(age)
    .check(
      a => a >= 18,
      { field: 'age', message: 'Must be 18 or older' }
    );

const validateUser = (email: string, age: number) =>
  combineValidations(
    validateEmail(email),
    validateAge(age)
  );
```

## Best Practices

### 1. Always use readonly for immutability

```typescript
// Good
type User = {
  readonly id: string;
  readonly name: string;
  readonly tags: readonly string[];
};

// Better - utility type
type Immutable<T> = {
  readonly [K in keyof T]: T[K] extends object 
    ? Immutable<T[K]> 
    : T[K];
};
```

### 2. Avoid any - use unknown or never

```typescript
// Bad
const parse = (json: string): any => JSON.parse(json);

// Good
const parse = (json: string): unknown => JSON.parse(json);

// Better - with type guard
const parseUser = (json: string): Either<Error, User> => {
  const result = tryCatch(() => JSON.parse(json));
  return flatMapEither(result, data => {
    if (isUser(data)) return Right(data);
    return Left(new Error('Invalid user data'));
  });
};
```

### 3. Use discriminated unions for state

```typescript
// Good
type AsyncData<E, A> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'error'; error: E }
  | { status: 'success'; data: A };

// Can't access data in wrong state
const renderData = (state: AsyncData<Error, string>): string => {
  switch (state.status) {
    case 'idle': return 'Not started';
    case 'loading': return 'Loading...';
    case 'error': return state.error.message; // Type-safe
    case 'success': return state.data; // Type-safe
  }
};
```

### 4. Leverage type inference

```typescript
// Let TypeScript infer types
const numbers = [1, 2, 3, 4, 5]; // inferred as number[]
const doubled = numbers.map(n => n * 2); // inferred as number[]

// Explicit when necessary
const parseNumbers = (strs: string[]): number[] =>
  strs.map(s => parseInt(s, 10));
```

### 5. Use const assertions for literals

```typescript
// Mutable array of string literals
const colors = ['red', 'green', 'blue'];
// Type: string[]

// Immutable tuple of literal types
const colors = ['red', 'green', 'blue'] as const;
// Type: readonly ["red", "green", "blue"]

// Object with literal types
const config = {
  apiUrl: 'https://api.example.com',
  timeout: 5000
} as const;
// Type: { readonly apiUrl: "https://api.example.com"; readonly timeout: 5000 }
```

### 6. Prefer type over interface for data

```typescript
// Type - better for FP
type Point = {
  readonly x: number;
  readonly y: number;
};

// Type allows unions
type Shape = Circle | Rectangle | Square;

// Type allows mapped types
type Readonly<T> = { readonly [K in keyof T]: T[K] };
```

## Common Patterns

### Railway-Oriented Programming

```typescript
// Chain operations that can fail
const processUser = flow(
  parseJSON<unknown>,
  flatMapEither(validateUser),
  mapEither(normalizeUser),
  flatMapEither(saveUser),
  mapEither(formatResponse)
);

const result = processUser(jsonString);
```

### Builder Pattern with Types

```typescript
type Builder<T> = {
  readonly build: () => T;
};

const userBuilder = () => {
  let name: string | undefined;
  let age: number | undefined;
  
  return {
    withName: (n: string) => (name = n, builder),
    withAge: (a: number) => (age = a, builder),
    build: (): Either<string, User> => {
      if (!name) return Left('Name required');
      if (!age) return Left('Age required');
      return Right({ name, age });
    }
  };
};
```

## Testing

```typescript
import { describe, it, expect } from 'vitest';

describe('Option', () => {
  it('maps over Some', () => {
    const opt = Some(5);
    const result = map(opt, n => n * 2);
    expect(result).toEqual(Some(10));
  });
  
  it('maps over None', () => {
    const opt = None<number>();
    const result = map(opt, n => n * 2);
    expect(result).toEqual(None());
  });
  
  it('flatMaps Some to Some', () => {
    const opt = Some(5);
    const result = flatMap(opt, n => Some(n * 2));
    expect(result).toEqual(Some(10));
  });
  
  it('flatMaps Some to None', () => {
    const opt = Some(5);
    const result = flatMap(opt, () => None());
    expect(result).toEqual(None());
  });
});

// Property-based testing
import fc from 'fast-check';

describe('Option laws', () => {
  it('satisfies functor identity', () => {
    fc.assert(
      fc.property(fc.integer(), n => {
        const opt = Some(n);
        const mapped = map(opt, x => x);
        expect(mapped).toEqual(opt);
      })
    );
  });
  
  it('satisfies functor composition', () => {
    const f = (n: number) => n * 2;
    const g = (n: number) => n + 1;
    
    fc.assert(
      fc.property(fc.integer(), n => {
        const opt = Some(n);
        const composed = map(map(opt, g), f);
        const direct = map(opt, x => f(g(x)));
        expect(composed).toEqual(direct);
      })
    );
  });
});
```

## Performance Optimization

```typescript
// Memoization with WeakMap for object keys
const memoizeObject = <K extends object, V>(
  fn: (key: K) => V
): ((key: K) => V) => {
  const cache = new WeakMap<K, V>();
  return (key: K): V => {
    if (!cache.has(key)) {
      cache.set(key, fn(key));
    }
    return cache.get(key)!;
  };
};

// Lazy evaluation for expensive operations
const lazyMap = <A, B>(
  arr: readonly A[],
  f: (a: A) => B
): (() => readonly B[]) => {
  let cached: readonly B[] | null = null;
  return () => {
    if (cached === null) {
      cached = arr.map(f);
    }
    return cached;
  };
};

// Batching async operations
const batchPromises = <A, B>(
  items: readonly A[],
  fn: (item: A) => Promise<B>,
  batchSize: number
): Promise<readonly B[]> => {
  const batches: A[][] = [];
  for (let i = 0; i < items.length; i += batchSize) {
    batches.push(items.slice(i, i + batchSize) as A[]);
  }
  
  return batches.reduce(
    async (acc, batch) => {
      const results = await acc;
      const batchResults = await Promise.all(batch.map(fn));
      return [...results, ...batchResults];
    },
    Promise.resolve([] as readonly B[])
  );
};
```
