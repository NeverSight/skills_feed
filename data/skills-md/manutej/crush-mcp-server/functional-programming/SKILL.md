---
name: functional-programming
description: Master functional programming principles and patterns including purity, immutability, composition, higher-order functions, algebraic data types, functors, monads, and effect management. Use when working with functional paradigms, pure functions, immutable data structures, function composition, type-safe error handling, or implementing functional patterns like map/filter/reduce, currying, partial application, recursion, lazy evaluation, or referential transparency.
---

# Functional Programming Mastery

## Core Principles

### The Zen of Functional Programming

**Purity is better than side effects**
Pure functions create predictable, testable code. Functions depend only on inputs and produce no side effects.

**Immutability is better than mutation**
Data that cannot change eliminates entire categories of bugs. State cannot be modified; concurrent operations become naturally safe.

**Composition is better than monoliths**
Small, focused functions combined thoughtfully solve complex problems elegantly.

**Declarative is better than imperative**
Express what you want, not how to get it.

**Referential transparency enables reasoning**
When expressions can be replaced by their values, code becomes mathematical.

**Functions are first-class citizens**
Treat functions as data. Pass them, return them, compose them.

**Explicit is better than hidden**
Make dependencies visible through function parameters. No global state, no hidden coupling.

**Recursion is iteration without mutation**
When loops require changing variables, let recursion express repetition through function calls.

**Type safety catches errors early**
Strong types are your allies. Let the compiler prove code correct before it runs.

**Separate effects from logic**
Isolate impure operations from pure computation. Draw clear boundaries between the ideal and the real.

**Statelessness enables concurrency**
Functions without shared state run safely in parallel.

**Errors should be values, not exceptions**
Make failure explicit in types. Return Maybe, Either, Result.

**Although practicality beats purity**
The real world requires side effects. Embrace them thoughtfully, manage them explicitly, isolate them carefully.

## Fundamental Concepts

### Pure Functions

Pure functions have two key properties:
1. **Deterministic**: Same input always produces same output
2. **No side effects**: No mutations, no I/O, no observable changes

```typescript
// Pure
const add = (a: number, b: number): number => a + b;

// Impure - depends on external state
let total = 0;
const addToTotal = (n: number): void => { total += n; };

// Impure - has side effect
const logAndAdd = (a: number, b: number): number => {
  console.log('adding'); // Side effect
  return a + b;
};
```

### Immutability

Never mutate data; always create new values.

```typescript
// Mutable (avoid)
const addItem = (arr: number[], item: number): void => {
  arr.push(item);
};

// Immutable (prefer)
const addItem = (arr: readonly number[], item: number): readonly number[] => 
  [...arr, item];

// Deep immutability
type DeepReadonly<T> = {
  readonly [P in keyof T]: T[P] extends object ? DeepReadonly<T[P]> : T[P];
};
```

### Function Composition

Build complex operations from simple functions.

```typescript
// Basic composition
const compose = <A, B, C>(f: (b: B) => C, g: (a: A) => B) => 
  (a: A): C => f(g(a));

// Pipe (left-to-right composition)
const pipe = <A, B, C>(f: (a: A) => B, g: (b: B) => C) => 
  (a: A): C => g(f(a));

// Example
const double = (n: number): number => n * 2;
const increment = (n: number): number => n + 1;

const doubleThenIncrement = pipe(double, increment);
doubleThenIncrement(5); // 11
```

### Higher-Order Functions

Functions that take or return functions.

```typescript
// Takes function as argument
const map = <A, B>(f: (a: A) => B) => 
  (arr: readonly A[]): readonly B[] => 
    arr.map(f);

// Returns function
const add = (a: number) => (b: number): number => a + b;
const add5 = add(5);

// Both
const compose = <A, B, C>(f: (b: B) => C) => 
  (g: (a: A) => B) => 
    (a: A): C => f(g(a));
```

### Currying and Partial Application

Transform multi-argument functions into chains of single-argument functions.

```typescript
// Uncurried
const add = (a: number, b: number, c: number): number => a + b + c;

// Curried
const addCurried = (a: number) => (b: number) => (c: number): number => 
  a + b + c;

const add5 = addCurried(5);
const add5and3 = add5(3);
add5and3(2); // 10

// Auto-curry utility
type Curry<T extends any[], R> = 
  T extends [infer First, ...infer Rest]
    ? (arg: First) => Rest extends [] ? R : Curry<Rest, R>
    : R;

const curry = <T extends any[], R>(
  fn: (...args: T) => R
): Curry<T, R> => {
  return ((...args: any[]) => 
    args.length >= fn.length 
      ? fn(...args as T)
      : curry((fn as any).bind(null, ...args))
  ) as any;
};
```

## Algebraic Data Types

### Sum Types (Union Types)

Represent "one of several" options.

```typescript
// Option/Maybe - represents presence or absence
type Option<A> = 
  | { tag: 'Some'; value: A }
  | { tag: 'None' };

// Either - represents success or failure
type Either<E, A> = 
  | { tag: 'Left'; value: E }
  | { tag: 'Right'; value: A };

// Result - common alias for Either
type Result<E, A> = Either<E, A>;

// Custom sum type
type PaymentMethod =
  | { type: 'CreditCard'; cardNumber: string }
  | { type: 'PayPal'; email: string }
  | { type: 'BankTransfer'; accountNumber: string };
```

### Product Types (Records/Tuples)

Combine multiple values.

```typescript
// Record (named fields)
type Person = {
  readonly name: string;
  readonly age: number;
};

// Tuple (positional fields)
type Coordinate = readonly [number, number];

// Nested product types
type Address = {
  readonly street: string;
  readonly city: string;
  readonly zipCode: string;
};

type Customer = {
  readonly person: Person;
  readonly address: Address;
};
```

## Functors

Containers that can be mapped over.

```typescript
interface Functor<F> {
  map<A, B>(fa: F, f: (a: A) => B): F;
}

// Array is a Functor
const arrayMap = <A, B>(arr: readonly A[], f: (a: A) => B): readonly B[] => 
  arr.map(f);

// Option is a Functor
const optionMap = <A, B>(opt: Option<A>, f: (a: A) => B): Option<B> => 
  opt.tag === 'None' ? opt : { tag: 'Some', value: f(opt.value) };

// Functor laws:
// 1. Identity: map(id) = id
// 2. Composition: map(f . g) = map(f) . map(g)
```

## Monads

Functors with additional structure for sequencing operations.

```typescript
interface Monad<M> extends Functor<M> {
  of<A>(a: A): M;
  flatMap<A, B>(ma: M, f: (a: A) => M): M;
}

// Option Monad
const optionOf = <A>(value: A): Option<A> => 
  ({ tag: 'Some', value });

const optionFlatMap = <A, B>(
  opt: Option<A>, 
  f: (a: A) => Option<B>
): Option<B> => 
  opt.tag === 'None' ? opt : f(opt.value);

// Either Monad
const eitherOf = <E, A>(value: A): Either<E, A> => 
  ({ tag: 'Right', value });

const eitherFlatMap = <E, A, B>(
  either: Either<E, A>,
  f: (a: A) => Either<E, B>
): Either<E, B> => 
  either.tag === 'Left' ? either : f(either.value);

// Monad laws:
// 1. Left identity: flatMap(of(a), f) = f(a)
// 2. Right identity: flatMap(m, of) = m
// 3. Associativity: flatMap(flatMap(m, f), g) = flatMap(m, x => flatMap(f(x), g))
```

## Common Patterns

### Pattern Matching

Safe exhaustive checking of sum types.

```typescript
const match = <T extends { tag: string }, R>(
  value: T,
  patterns: { [K in T['tag']]: (val: Extract<T, { tag: K }>) => R }
): R => {
  return patterns[value.tag](value as any);
};

// Usage
const describeOption = <A>(opt: Option<A>): string =>
  match(opt, {
    Some: ({ value }) => `Value: ${value}`,
    None: () => 'No value'
  });
```

### Recursion Patterns

Replace loops with recursive functions.

```typescript
// Tail-recursive sum
const sum = (arr: readonly number[]): number => {
  const go = (i: number, acc: number): number =>
    i >= arr.length ? acc : go(i + 1, acc + arr[i]);
  return go(0, 0);
};

// Recursive tree traversal
type Tree<A> = 
  | { tag: 'Leaf'; value: A }
  | { tag: 'Branch'; left: Tree<A>; right: Tree<A> };

const mapTree = <A, B>(tree: Tree<A>, f: (a: A) => B): Tree<B> =>
  tree.tag === 'Leaf' 
    ? { tag: 'Leaf', value: f(tree.value) }
    : {
        tag: 'Branch',
        left: mapTree(tree.left, f),
        right: mapTree(tree.right, f)
      };
```

### Trampolining

Optimize recursion to avoid stack overflow.

```typescript
type Trampoline<A> = 
  | { tag: 'Done'; value: A }
  | { tag: 'Continue'; next: () => Trampoline<A> };

const run = <A>(trampoline: Trampoline<A>): A => {
  let current = trampoline;
  while (current.tag === 'Continue') {
    current = current.next();
  }
  return current.value;
};

// Tail-recursive factorial using trampoline
const factorial = (n: number, acc = 1): Trampoline<number> =>
  n <= 1
    ? { tag: 'Done', value: acc }
    : { tag: 'Continue', next: () => factorial(n - 1, n * acc) };

run(factorial(10000)); // No stack overflow
```

### Lazy Evaluation

Defer computation until needed.

```typescript
type Lazy<A> = () => A;

const lazy = <A>(compute: () => A): Lazy<A> => {
  let cached: { computed: boolean; value?: A } = { computed: false };
  return () => {
    if (!cached.computed) {
      cached.value = compute();
      cached.computed = true;
    }
    return cached.value!;
  };
};

// Infinite sequences
type Stream<A> = {
  head: () => A;
  tail: () => Stream<A>;
};

const naturals = (n = 0): Stream<number> => ({
  head: () => n,
  tail: () => naturals(n + 1)
});

const take = <A>(n: number, stream: Stream<A>): A[] => {
  const result: A[] = [];
  let current = stream;
  for (let i = 0; i < n; i++) {
    result.push(current.head());
    current = current.tail();
  }
  return result;
};
```

## Effect Management

### IO Monad

Encapsulate side effects.

```typescript
type IO<A> = () => A;

const ioOf = <A>(value: A): IO<A> => () => value;

const ioMap = <A, B>(io: IO<A>, f: (a: A) => B): IO<B> => 
  () => f(io());

const ioFlatMap = <A, B>(io: IO<A>, f: (a: A) => IO<B>): IO<B> => 
  () => f(io())();

// Example
const log = (message: string): IO<void> => 
  () => console.log(message);

const prompt = (question: string): IO<string> => 
  () => window.prompt(question) || '';

const program = ioFlatMap(
  prompt('What is your name?'),
  name => log(`Hello, ${name}!`)
);

// Run at the edge
program();
```

### Reader Monad

Thread configuration through computations.

```typescript
type Reader<R, A> = (env: R) => A;

const readerOf = <R, A>(value: A): Reader<R, A> => 
  () => value;

const readerMap = <R, A, B>(
  reader: Reader<R, A>,
  f: (a: A) => B
): Reader<R, B> => 
  env => f(reader(env));

const readerFlatMap = <R, A, B>(
  reader: Reader<R, A>,
  f: (a: A) => Reader<R, B>
): Reader<R, B> => 
  env => f(reader(env))(env);

const ask = <R>(): Reader<R, R> => env => env;

// Example
type Config = { apiUrl: string; timeout: number };

const getApiUrl: Reader<Config, string> = 
  config => config.apiUrl;

const fetchUser = (id: number): Reader<Config, Promise<User>> =>
  env => fetch(`${env.apiUrl}/users/${id}`).then(r => r.json());
```

### Free Monad

Separate program description from interpretation.

```typescript
type Free<F, A> =
  | { tag: 'Pure'; value: A }
  | { tag: 'Impure'; command: F; next: (x: any) => Free<F, A> };

const pure = <F, A>(value: A): Free<F, A> => 
  ({ tag: 'Pure', value });

const liftF = <F, A>(command: F): Free<F, A> => 
  ({ tag: 'Impure', command, next: pure });

const freeMap = <F, A, B>(
  free: Free<F, A>,
  f: (a: A) => B
): Free<F, B> =>
  free.tag === 'Pure'
    ? pure(f(free.value))
    : { ...free, next: x => freeMap(free.next(x), f) };

const freeFlatMap = <F, A, B>(
  free: Free<F, A>,
  f: (a: A) => Free<F, B>
): Free<F, B> =>
  free.tag === 'Pure'
    ? f(free.value)
    : { ...free, next: x => freeFlatMap(free.next(x), f) };
```

## Performance Considerations

### Memoization

Cache pure function results.

```typescript
const memoize = <A extends any[], R>(
  fn: (...args: A) => R
): ((...args: A) => R) => {
  const cache = new Map<string, R>();
  return (...args: A): R => {
    const key = JSON.stringify(args);
    if (!cache.has(key)) {
      cache.set(key, fn(...args));
    }
    return cache.get(key)!;
  };
};

// Fibonacci with memoization
const fib = memoize((n: number): number =>
  n <= 1 ? n : fib(n - 1) + fib(n - 2)
);
```

### Transducers

Compose data transformations without intermediate collections.

```typescript
type Reducer<A, B> = (acc: B, value: A) => B;
type Transducer<A, B, C, D> = (reducer: Reducer<C, D>) => Reducer<A, B>;

const mapT = <A, B>(f: (a: A) => B): Transducer<A, any, B, any> =>
  reducer => (acc, value) => reducer(acc, f(value));

const filterT = <A>(pred: (a: A) => boolean): Transducer<A, any, A, any> =>
  reducer => (acc, value) => pred(value) ? reducer(acc, value) : acc;

const transduce = <A, B, C>(
  transducer: Transducer<A, B, A, C>,
  reducer: Reducer<A, C>,
  initial: C,
  collection: readonly A[]
): C => {
  const xf = transducer(reducer);
  return collection.reduce(xf, initial);
};
```

## Testing Pure Functions

```typescript
// Property-based testing pattern
type Gen<A> = () => A;

const genNumber: Gen<number> = () => Math.random() * 1000;
const genString: Gen<string> = () => Math.random().toString(36);

const property = <A>(
  name: string,
  gen: Gen<A>,
  pred: (a: A) => boolean,
  iterations = 100
): void => {
  for (let i = 0; i < iterations; i++) {
    const value = gen();
    if (!pred(value)) {
      throw new Error(`Property "${name}" failed for: ${value}`);
    }
  }
};

// Test pure function properties
property(
  'add is commutative',
  () => ({ a: genNumber(), b: genNumber() }),
  ({ a, b }) => add(a, b) === add(b, a)
);

property(
  'map identity',
  () => [1, 2, 3, 4, 5],
  arr => arrayMap(arr, x => x) === arr
);
```

## Best Practices

1. **Start pure, end impure**: Keep business logic pure; push effects to boundaries
2. **Use readonly liberally**: Make immutability explicit in types
3. **Compose small functions**: Build complex operations from simple, testable pieces
4. **Make illegal states unrepresentable**: Use types to prevent invalid data
5. **Prefer expressions over statements**: Every operation should return a value
6. **Avoid null/undefined**: Use Option/Maybe types instead
7. **Make errors explicit**: Use Either/Result instead of throwing exceptions
8. **Use const over let**: Prevent reassignment at language level
9. **Leverage type inference**: Let compiler deduce types where possible
10. **Document with types**: Types are better documentation than comments

## Common Pitfalls

1. **Forgetting to return in arrow functions**: `x => { x + 1 }` returns undefined
2. **Mutating in array methods**: `arr.sort()` mutates; use `[...arr].sort()`
3. **Shallow copying objects**: `{...obj}` only copies top level; nested objects shared
4. **Overusing composition**: Sometimes direct implementation is clearer
5. **Ignoring performance**: Immutability and composition have costs
6. **Fighting the language**: TypeScript isn't Haskell; pragmatism matters
