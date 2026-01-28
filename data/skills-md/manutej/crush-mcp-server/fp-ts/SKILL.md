---
name: fp-ts
description: Master the fp-ts library for typed functional programming in TypeScript, including Option, Either, Task, TaskEither, Reader, State, IO, Array, Record, pipe/flow composition, Do notation, optics (lenses/prisms), and integration with the Effect-TS ecosystem. Use when working with fp-ts data types, composing functional pipelines, handling effects functionally, implementing monadic patterns, or using fp-ts utilities for type-safe functional code.
---

# fp-ts Mastery

fp-ts is the most widely used library for typed functional programming in TypeScript, bringing abstractions from Haskell and Scala with strict type safety.

## Installation and Setup

```bash
npm install fp-ts
```

```typescript
// Import from specific modules
import * as O from 'fp-ts/Option';
import * as E from 'fp-ts/Either';
import * as A from 'fp-ts/Array';
import * as TE from 'fp-ts/TaskEither';
import { pipe, flow } from 'fp-ts/function';
```

## Core Concepts

### pipe and flow

The foundation of fp-ts composition.

```typescript
import { pipe, flow } from 'fp-ts/function';

// pipe - apply functions left-to-right on a value
const result = pipe(
  5,
  n => n * 2,    // 10
  n => n + 1,    // 11
  n => n.toString() // "11"
);

// flow - compose functions without initial value
const processNumber = flow(
  (n: number) => n * 2,
  n => n + 1,
  n => n.toString()
);

processNumber(5); // "11"
```

### The HKT (Higher-Kinded Types) System

fp-ts uses a sophisticated type system for generic abstractions.

```typescript
// Module augmentation for HKT
import { HKT, Kind, Kind2, URIS, URIS2 } from 'fp-ts/HKT';

// URIS identifies type constructors
const optionURI = 'Option';
type OptionURI = typeof optionURI;

// Use Kind to apply type constructor
type OptionKind<A> = Kind<OptionURI, A>;
```

## Option Type

Represents optional values without null/undefined.

### Construction

```typescript
import * as O from 'fp-ts/Option';

// Create Option values
const some = O.some(42);           // Some(42)
const none = O.none;                // None
const fromNullable = O.fromNullable(maybeValue); // Some or None
const fromPredicate = O.fromPredicate((n: number) => n > 0)(5); // Some(5)

// Type: Option<number>
```

### Core Operations

```typescript
import { pipe } from 'fp-ts/function';
import * as O from 'fp-ts/Option';

// map - transform the value
pipe(
  O.some(5),
  O.map(n => n * 2)
); // Some(10)

// flatMap (chain) - sequencing operations that return Option
pipe(
  O.some(5),
  O.flatMap(n => n > 0 ? O.some(n * 2) : O.none)
); // Some(10)

// getOrElse - extract value with default
pipe(
  O.none,
  O.getOrElse(() => 0)
); // 0

// fold (match) - handle both cases
pipe(
  O.some(5),
  O.fold(
    () => 'No value',
    n => `Value: ${n}`
  )
); // "Value: 5"

// filter
pipe(
  O.some(5),
  O.filter(n => n > 3)
); // Some(5)

// alt - provide alternative Option
pipe(
  O.none,
  O.alt(() => O.some(42))
); // Some(42)
```

### Advanced Patterns

```typescript
// Traverse array of Options
import * as A from 'fp-ts/Array';

const options = [O.some(1), O.some(2), O.some(3)];

pipe(
  options,
  A.sequence(O.Applicative)
); // Some([1, 2, 3])

pipe(
  [O.some(1), O.none, O.some(3)],
  A.sequence(O.Applicative)
); // None

// Do notation for imperative-style sequencing
pipe(
  O.Do,
  O.bind('x', () => O.some(5)),
  O.bind('y', () => O.some(3)),
  O.map(({ x, y }) => x + y)
); // Some(8)

// exists and every
pipe(
  O.some(5),
  O.exists(n => n > 3)
); // true

// toNullable and toUndefined
pipe(
  O.some(5),
  O.toNullable
); // 5

pipe(
  O.none,
  O.toNullable
); // null
```

### Common Use Cases

```typescript
// Safe array access
const head = <A>(arr: readonly A[]): O.Option<A> =>
  pipe(arr, A.head);

// Safe property access
const getProp = <K extends string>(key: K) =>
  <T extends Record<K, unknown>>(obj: T): O.Option<T[K]> =>
    O.fromNullable(obj[key]);

// Safe parsing
const parseNumber = (s: string): O.Option<number> =>
  pipe(
    O.tryCatch(() => {
      const n = parseFloat(s);
      return isNaN(n) ? null : n;
    })
  );

// Chaining optional operations
type User = { name: string; address?: { city?: string } };

const getCity = (user: User): O.Option<string> =>
  pipe(
    user.address,
    O.fromNullable,
    O.flatMap(addr => O.fromNullable(addr.city))
  );
```

## Either Type

Represents computations that can fail.

### Construction

```typescript
import * as E from 'fp-ts/Either';

// Create Either values
const right = E.right(42);               // Right(42)
const left = E.left('error');            // Left('error')
const fromPredicate = E.fromPredicate(
  (n: number) => n > 0,
  n => `${n} is not positive`
)(5); // Right(5)

// Type: Either<string, number>
```

### Core Operations

```typescript
import { pipe } from 'fp-ts/function';
import * as E from 'fp-ts/Either';

// map - transform right value
pipe(
  E.right(5),
  E.map(n => n * 2)
); // Right(10)

// mapLeft - transform left value
pipe(
  E.left('error'),
  E.mapLeft(e => e.toUpperCase())
); // Left('ERROR')

// flatMap (chain) - sequence Either-returning operations
pipe(
  E.right(5),
  E.flatMap(n => n > 0 ? E.right(n * 2) : E.left('negative'))
); // Right(10)

// fold (match) - handle both cases
pipe(
  E.right(5),
  E.fold(
    error => `Error: ${error}`,
    value => `Success: ${value}`
  )
); // "Success: 5"

// getOrElse - extract value with default
pipe(
  E.left('error'),
  E.getOrElse(() => 0)
); // 0

// orElse - provide alternative Either
pipe(
  E.left('error'),
  E.orElse(() => E.right(42))
); // Right(42)

// swap - exchange left and right
pipe(
  E.right(5),
  E.swap
); // Left(5)

// bimap - map both sides
pipe(
  E.right<string, number>(5),
  E.bimap(
    e => e.toUpperCase(),
    n => n * 2
  )
); // Right(10)
```

### Error Handling Patterns

```typescript
// tryCatch - wrap throwing code
const safeParse = (json: string): E.Either<Error, unknown> =>
  E.tryCatch(
    () => JSON.parse(json),
    reason => new Error(`Parse error: ${reason}`)
  );

// Validation with Either
const validateEmail = (email: string): E.Either<string, string> =>
  email.includes('@') 
    ? E.right(email)
    : E.left('Invalid email');

const validateAge = (age: number): E.Either<string, number> =>
  age >= 18
    ? E.right(age)
    : E.left('Must be 18 or older');

// Chain validations
const validateUser = (email: string, age: number): E.Either<string, User> =>
  pipe(
    validateEmail(email),
    E.flatMap(validEmail =>
      pipe(
        validateAge(age),
        E.map(validAge => ({ email: validEmail, age: validAge }))
      )
    )
  );

// Do notation for cleaner syntax
const validateUserDo = (email: string, age: number): E.Either<string, User> =>
  pipe(
    E.Do,
    E.bind('email', () => validateEmail(email)),
    E.bind('age', () => validateAge(age))
  );
```

### Combining Multiple Eithers

```typescript
import * as A from 'fp-ts/Array';
import { sequenceT } from 'fp-ts/Apply';

// Sequence array of Eithers (fails on first error)
const eithers: E.Either<string, number>[] = [
  E.right(1),
  E.right(2),
  E.right(3)
];

pipe(
  eithers,
  A.sequence(E.Applicative)
); // Right([1, 2, 3])

// Parallel validation with sequenceT
pipe(
  sequenceT(E.Applicative)(
    validateEmail('test@example.com'),
    validateAge(25)
  )
); // Right(['test@example.com', 25])

// Convert to Option
pipe(
  E.right(5),
  E.toOption
); // Some(5)

pipe(
  E.left('error'),
  E.toOption
); // None
```

## Task and TaskEither

Handle asynchronous operations.

### Task

Lazy Promise (only executes when called).

```typescript
import * as T from 'fp-ts/Task';
import { pipe } from 'fp-ts/function';

// Create Task
const delay = (ms: number): T.Task<void> =>
  () => new Promise(resolve => setTimeout(resolve, ms));

const fetchData = (): T.Task<Data> =>
  () => fetch('/api/data').then(r => r.json());

// map
pipe(
  fetchData(),
  T.map(data => data.items.length)
); // Task<number>

// flatMap (chain)
pipe(
  fetchData(),
  T.flatMap(data => 
    pipe(
      delay(1000),
      T.map(() => data)
    )
  )
); // Task<Data>

// Execute
const task = fetchData();
task().then(data => console.log(data));
```

### TaskEither

Asynchronous operations that can fail.

```typescript
import * as TE from 'fp-ts/TaskEither';
import { pipe } from 'fp-ts/function';

// Create TaskEither
const fetchUser = (id: number): TE.TaskEither<Error, User> =>
  TE.tryCatch(
    () => fetch(`/api/users/${id}`).then(r => {
      if (!r.ok) throw new Error('Not found');
      return r.json();
    }),
    reason => new Error(`Fetch failed: ${reason}`)
  );

// map - transform success value
pipe(
  fetchUser(1),
  TE.map(user => user.name)
); // TaskEither<Error, string>

// mapLeft - transform error
pipe(
  fetchUser(1),
  TE.mapLeft(error => ({ message: error.message, code: 500 }))
); // TaskEither<{message: string, code: number}, User>

// flatMap (chain) - sequence async operations
pipe(
  fetchUser(1),
  TE.flatMap(user => fetchPosts(user.id))
); // TaskEither<Error, Post[]>

// fold (match)
pipe(
  fetchUser(1),
  TE.fold(
    error => T.of(`Error: ${error.message}`),
    user => T.of(`User: ${user.name}`)
  )
)(); // Promise<string>

// getOrElse
pipe(
  fetchUser(1),
  TE.getOrElse(error => T.of(defaultUser))
)(); // Promise<User>

// orElse - provide alternative
pipe(
  fetchUser(1),
  TE.orElse(error => fetchUserFromCache(1))
); // TaskEither<Error, User>
```

### Do Notation with TaskEither

```typescript
const processUser = (id: number): TE.TaskEither<Error, Result> =>
  pipe(
    TE.Do,
    TE.bind('user', () => fetchUser(id)),
    TE.bind('posts', ({ user }) => fetchPosts(user.id)),
    TE.bind('comments', ({ posts }) => fetchComments(posts[0].id)),
    TE.map(({ user, posts, comments }) => ({
      user,
      postCount: posts.length,
      commentCount: comments.length
    }))
  );
```

### Parallel Execution

```typescript
import { sequenceT } from 'fp-ts/Apply';
import { sequenceArray } from 'fp-ts/Array';

// Execute in parallel with sequenceT
const fetchUserData = (id: number): TE.TaskEither<Error, UserData> =>
  pipe(
    sequenceT(TE.ApplicativePar)(
      fetchUser(id),
      fetchPosts(id),
      fetchComments(id)
    ),
    TE.map(([user, posts, comments]) => ({
      user,
      posts,
      comments
    }))
  );

// Execute array in parallel
const fetchUsers = (ids: number[]): TE.TaskEither<Error, User[]> =>
  pipe(
    ids.map(fetchUser),
    TE.sequenceArray  // or A.sequence(TE.ApplicativePar)
  );

// Execute array sequentially
const fetchUsersSeq = (ids: number[]): TE.TaskEither<Error, User[]> =>
  pipe(
    ids.map(fetchUser),
    A.sequence(TE.ApplicativeSeq)
  );
```

## Array Operations

fp-ts provides powerful array utilities.

```typescript
import * as A from 'fp-ts/Array';
import * as O from 'fp-ts/Option';
import { pipe } from 'fp-ts/function';

// Safe head and tail
pipe([1, 2, 3], A.head); // Some(1)
pipe([], A.head);        // None
pipe([1, 2, 3], A.tail); // Some([2, 3])

// filter and partition
pipe(
  [1, 2, 3, 4, 5],
  A.filter(n => n % 2 === 0)
); // [2, 4]

pipe(
  [1, 2, 3, 4, 5],
  A.partition(n => n % 2 === 0)
); // { left: [1, 3, 5], right: [2, 4] }

// filterMap - filter and transform in one pass
pipe(
  ['1', 'foo', '2', 'bar', '3'],
  A.filterMap(s => {
    const n = parseInt(s);
    return isNaN(n) ? O.none : O.some(n);
  })
); // [1, 2, 3]

// flatMap (chain)
pipe(
  [1, 2, 3],
  A.flatMap(n => [n, n * 2])
); // [1, 2, 2, 4, 3, 6]

// reduce
pipe(
  [1, 2, 3, 4, 5],
  A.reduce(0, (acc, n) => acc + n)
); // 15

// findFirst and findLast
pipe(
  [1, 2, 3, 4, 5],
  A.findFirst(n => n > 3)
); // Some(4)

// lookup - safe array access
pipe(
  [1, 2, 3],
  A.lookup(1)
); // Some(2)

// uniq - remove duplicates
pipe(
  [1, 2, 2, 3, 3, 3, 4],
  A.uniq(Eq.eqNumber)
); // [1, 2, 3, 4]

// sort
import * as Ord from 'fp-ts/Ord';

pipe(
  [3, 1, 4, 1, 5],
  A.sort(Ord.ordNumber)
); // [1, 1, 3, 4, 5]

// groupBy
pipe(
  ['foo', 'bar', 'baz', 'qux'],
  A.groupBy(s => s[0])
); // { f: ['foo'], b: ['bar', 'baz'], q: ['qux'] }

// zip
pipe(
  A.zip([1, 2, 3], ['a', 'b', 'c'])
); // [[1, 'a'], [2, 'b'], [3, 'c']]

// chunksOf
pipe(
  [1, 2, 3, 4, 5, 6, 7],
  A.chunksOf(3)
); // [[1, 2, 3], [4, 5, 6], [7]]
```

### Traversing with Effects

```typescript
// Traverse with Option
const parseNumbers = (strs: string[]): O.Option<number[]> =>
  pipe(
    strs,
    A.traverse(O.Applicative)(s => {
      const n = parseInt(s);
      return isNaN(n) ? O.none : O.some(n);
    })
  );

parseNumbers(['1', '2', '3']); // Some([1, 2, 3])
parseNumbers(['1', 'foo', '3']); // None

// Traverse with Either
const validateAll = (
  users: UnvalidatedUser[]
): E.Either<string, User[]> =>
  pipe(
    users,
    A.traverse(E.Applicative)(validateUser)
  );

// Traverse with TaskEither
const fetchAllUsers = (ids: number[]): TE.TaskEither<Error, User[]> =>
  pipe(
    ids,
    A.traverse(TE.ApplicativePar)(fetchUser)
  );
```

## Record Operations

Work with objects functionally.

```typescript
import * as R from 'fp-ts/Record';
import { pipe } from 'fp-ts/function';

// map - transform all values
pipe(
  { a: 1, b: 2, c: 3 },
  R.map(n => n * 2)
); // { a: 2, b: 4, c: 6 }

// filter
pipe(
  { a: 1, b: 2, c: 3 },
  R.filter(n => n > 1)
); // { b: 2, c: 3 }

// filterMap
pipe(
  { a: '1', b: 'foo', c: '2' },
  R.filterMap(s => {
    const n = parseInt(s);
    return isNaN(n) ? O.none : O.some(n);
  })
); // { a: 1, c: 2 }

// lookup - safe property access
pipe(
  { a: 1, b: 2 },
  R.lookup('a')
); // Some(1)

// has - check key existence
pipe(
  { a: 1, b: 2 },
  R.has('c')
); // false

// keys and values
R.keys({ a: 1, b: 2, c: 3 }); // ['a', 'b', 'c']
R.collect((k, v) => [k, v])({ a: 1, b: 2 }); // [['a', 1], ['b', 2]]

// fromFoldable - create from iterable
import * as A from 'fp-ts/Array';

pipe(
  [['a', 1], ['b', 2], ['c', 3]],
  R.fromFoldable(
    { concat: (x, y) => y }, // last value wins
    A.Foldable
  )
); // { a: 1, b: 2, c: 3 }

// traverse with effects
const validateRecord = (
  record: Record<string, string>
): E.Either<string, Record<string, number>> =>
  pipe(
    record,
    R.traverse(E.Applicative)(s => {
      const n = parseInt(s);
      return isNaN(n) 
        ? E.left(`Invalid number: ${s}`)
        : E.right(n);
    })
  );
```

## Reader Monad

Thread configuration/dependencies through computations.

```typescript
import * as R from 'fp-ts/Reader';
import { pipe } from 'fp-ts/function';

type Config = {
  apiUrl: string;
  timeout: number;
};

// Create Reader
const getApiUrl: R.Reader<Config, string> = 
  config => config.apiUrl;

const getTimeout: R.Reader<Config, number> =
  config => config.timeout;

// map
const getFullUrl = (path: string): R.Reader<Config, string> =>
  pipe(
    getApiUrl,
    R.map(url => `${url}${path}`)
  );

// flatMap (chain)
const fetchWithTimeout = (path: string): R.Reader<Config, Promise<Response>> =>
  pipe(
    R.Do,
    R.bind('url', () => getFullUrl(path)),
    R.bind('timeout', () => getTimeout),
    R.map(({ url, timeout }) =>
      fetch(url, { signal: AbortSignal.timeout(timeout) })
    )
  );

// ask - get the environment
const logConfig: R.Reader<Config, void> =
  pipe(
    R.ask<Config>(),
    R.map(config => console.log(config))
  );

// local - modify environment locally
const withDifferentUrl = <A>(
  reader: R.Reader<Config, A>
): R.Reader<Config, A> =>
  pipe(
    reader,
    R.local((config: Config) => ({
      ...config,
      apiUrl: 'https://api-v2.example.com'
    }))
  );

// Execute Reader
const config: Config = {
  apiUrl: 'https://api.example.com',
  timeout: 5000
};

const result = fetchWithTimeout('/users')(config);
```

## ReaderTaskEither

Combine Reader, Task, and Either for dependency injection with async error handling.

```typescript
import * as RTE from 'fp-ts/ReaderTaskEither';
import { pipe } from 'fp-ts/function';

type Deps = {
  db: Database;
  logger: Logger;
  config: Config;
};

// Create RTE
const getUser = (id: number): RTE.ReaderTaskEither<Deps, Error, User> =>
  pipe(
    RTE.ask<Deps>(),
    RTE.flatMap(({ db, logger }) =>
      RTE.tryCatch(
        async () => {
          logger.info(`Fetching user ${id}`);
          return db.users.findById(id);
        },
        reason => new Error(`Failed to fetch user: ${reason}`)
      )
    )
  );

// Compose operations
const getUserWithPosts = (
  id: number
): RTE.ReaderTaskEither<Deps, Error, UserWithPosts> =>
  pipe(
    RTE.Do,
    RTE.bind('user', () => getUser(id)),
    RTE.bind('posts', ({ user }) => getPosts(user.id)),
    RTE.map(({ user, posts }) => ({ ...user, posts }))
  );

// Execute
const deps: Deps = {
  db: createDatabase(),
  logger: createLogger(),
  config: loadConfig()
};

getUserWithPosts(1)(deps)()
  .then(E.fold(
    error => console.error(error),
    user => console.log(user)
  ));

// local - modify dependencies
const withTestDb = <A>(
  rte: RTE.ReaderTaskEither<Deps, Error, A>
): RTE.ReaderTaskEither<Deps, Error, A> =>
  pipe(
    rte,
    RTE.local((deps: Deps) => ({
      ...deps,
      db: createTestDatabase()
    }))
  );
```

## State Monad

Thread state through computations.

```typescript
import * as S from 'fp-ts/State';
import { pipe } from 'fp-ts/function';

type Counter = { count: number };

// Create State
const increment: S.State<Counter, number> =
  state => [state.count + 1, { count: state.count + 1 }];

const decrement: S.State<Counter, number> =
  state => [state.count - 1, { count: state.count - 1 }];

// get and put
const getCount: S.State<Counter, number> =
  state => [state.count, state];

const setCount = (count: number): S.State<Counter, void> =>
  _state => [undefined, { count }];

// modify
const multiplyCount = (factor: number): S.State<Counter, void> =>
  S.modify((state: Counter) => ({ count: state.count * factor }));

// Compose operations
const complexOperation: S.State<Counter, string> =
  pipe(
    S.Do,
    S.bind('initial', () => getCount),
    S.bind('after1', () => increment),
    S.bind('after2', () => increment),
    S.bind('multiplied', () => {
      multiplyCount(2);
      return getCount;
    }),
    S.map(({ initial, after1, after2, multiplied }) =>
      `${initial} -> ${after1} -> ${after2} -> ${multiplied}`
    )
  );

// Execute State
const initialState: Counter = { count: 0 };
const [result, finalState] = complexOperation(initialState);
```

## IO Monad

Encapsulate side effects.

```typescript
import * as IO from 'fp-ts/IO';
import { pipe } from 'fp-ts/function';

// Create IO
const log = (message: string): IO.IO<void> =>
  () => console.log(message);

const random: IO.IO<number> =
  () => Math.random();

const now: IO.IO<Date> =
  () => new Date();

// map
pipe(
  random,
  IO.map(n => n * 100)
); // IO<number>

// flatMap (chain)
pipe(
  random,
  IO.flatMap(n => log(`Random: ${n}`))
); // IO<void>

// Do notation
const program: IO.IO<string> =
  pipe(
    IO.Do,
    IO.bind('time', () => now),
    IO.bind('rand', () => random),
    IO.chainFirst(({ time }) => log(`Time: ${time}`)),
    IO.map(({ time, rand }) => `${time}: ${rand}`)
  );

// Execute at program boundary
program();
```

## Optics (Lenses, Prisms, Traversals)

Access and modify nested data structures immutably.

```typescript
import { pipe } from 'fp-ts/function';
import * as O from 'fp-ts/Option';
import { Lens, Optional, Prism } from 'monocle-ts';

type Address = {
  street: string;
  city: string;
  zipCode: string;
};

type Person = {
  name: string;
  age: number;
  address: Address;
};

// Lens - focus on a field
const addressLens = Lens.fromProp<Person>()('address');
const cityLens = Lens.fromProp<Address>()('city');

// Compose lenses
const personCityLens = pipe(addressLens, Lens.compose(cityLens));

const person: Person = {
  name: 'John',
  age: 30,
  address: { street: '123 Main', city: 'NYC', zipCode: '10001' }
};

// Get
personCityLens.get(person); // 'NYC'

// Set
const updated = personCityLens.set('LA')(person);
// { ..., address: { ..., city: 'LA' } }

// Modify
const capitalized = personCityLens.modify(city => city.toUpperCase())(person);

// Optional - for nullable fields
type User = {
  name: string;
  email?: string;
};

const emailOptional = Optional.fromNullableProp<User>()('email');

const user: User = { name: 'John', email: 'john@example.com' };

emailOptional.getOption(user); // Some('john@example.com')
emailOptional.set('new@example.com')(user);

// Prism - for sum types
type Shape =
  | { type: 'circle'; radius: number }
  | { type: 'rectangle'; width: number; height: number };

const circlePrism = Prism.fromPredicate((s: Shape): s is Extract<Shape, { type: 'circle' }> =>
  s.type === 'circle'
);

const shape: Shape = { type: 'circle', radius: 5 };

circlePrism.getOption(shape); // Some({ type: 'circle', radius: 5 })
circlePrism.modify(c => ({ ...c, radius: c.radius * 2 }))(shape);

// Traversal - for collections
import { Traversal } from 'monocle-ts';
import * as A from 'fp-ts/Array';

const arrayTraversal = <A>() => Traversal.fromTraversable(A.Traversable)<A>();

const numbers = [1, 2, 3, 4, 5];

pipe(
  numbers,
  arrayTraversal<number>().modify(n => n * 2)
); // [2, 4, 6, 8, 10]
```

## Eq, Ord, and Semigroup

Type classes for comparison and combination.

```typescript
import * as Eq from 'fp-ts/Eq';
import * as Ord from 'fp-ts/Ord';
import * as S from 'fp-ts/Semigroup';
import { pipe } from 'fp-ts/function';

// Eq - equality checking
const eqPerson = Eq.struct<Person>({
  name: Eq.eqString,
  age: Eq.eqNumber,
  address: Eq.struct({
    street: Eq.eqString,
    city: Eq.eqString,
    zipCode: Eq.eqString
  })
});

eqPerson.equals(person1, person2); // boolean

// Ord - ordering
const ordPerson = pipe(
  Ord.ordNumber,
  Ord.contramap((p: Person) => p.age)
);

const people = [person1, person2, person3];
pipe(people, A.sort(ordPerson));

// Semigroup - combining values
const semigroupSum = S.semigroupSum;
S.concatAll(semigroupSum)(0)([1, 2, 3, 4]); // 10

const semigroupProduct = S.semigroupProduct;
S.concatAll(semigroupProduct)(1)([2, 3, 4]); // 24

// Custom semigroup
type User = { name: string; age: number };

const userSemigroup: S.Semigroup<User> = {
  concat: (x, y) => ({
    name: `${x.name} & ${y.name}`,
    age: Math.max(x.age, y.age)
  })
};

// Monoid - Semigroup with identity
import * as M from 'fp-ts/Monoid';

const monoidString = M.monoidString;
M.concatAll(monoidString)(['hello', ' ', 'world']); // 'hello world'
```

## Practical Patterns

### API Request Pipeline

```typescript
import * as TE from 'fp-ts/TaskEither';
import * as E from 'fp-ts/Either';
import { pipe } from 'fp-ts/function';

type ApiError = 
  | { type: 'NetworkError'; message: string }
  | { type: 'ParseError'; message: string }
  | { type: 'ValidationError'; errors: string[] };

const request = <A>(
  url: string,
  options?: RequestInit
): TE.TaskEither<ApiError, A> =>
  pipe(
    TE.tryCatch(
      () => fetch(url, options),
      reason => ({ 
        type: 'NetworkError' as const, 
        message: String(reason) 
      })
    ),
    TE.flatMap(response =>
      TE.tryCatch(
        () => response.json(),
        reason => ({ 
          type: 'ParseError' as const, 
          message: String(reason) 
        })
      )
    )
  );

const validateUser = (data: unknown): E.Either<ApiError, User> => {
  // Validation logic
  if (isValidUser(data)) {
    return E.right(data as User);
  }
  return E.left({ 
    type: 'ValidationError', 
    errors: ['Invalid user data'] 
  });
};

const fetchUser = (id: number): TE.TaskEither<ApiError, User> =>
  pipe(
    request<unknown>(`/api/users/${id}`),
    TE.flatMapEither(validateUser)
  );
```

### Form Validation

```typescript
import * as E from 'fp-ts/Either';
import * as A from 'fp-ts/Array';
import { pipe } from 'fp-ts/function';
import { sequenceT } from 'fp-ts/Apply';

type ValidationError = {
  field: string;
  message: string;
};

type Validation<A> = E.Either<ValidationError[], A>;

const validateRequired = (field: string) => (value: string): Validation<string> =>
  value.length > 0
    ? E.right(value)
    : E.left([{ field, message: 'Required' }]);

const validateEmail = (value: string): Validation<string> =>
  value.includes('@')
    ? E.right(value)
    : E.left([{ field: 'email', message: 'Invalid email' }]);

const validateAge = (value: number): Validation<number> =>
  value >= 18
    ? E.right(value)
    : E.left([{ field: 'age', message: 'Must be 18+' }]);

// Applicative validation (accumulates all errors)
import * as Ap from 'fp-ts/Apply';

const getValidationApplicative = <E>(): Ap.Applicative2C<'Either', E[]> => ({
  ...E.Applicative,
  ap: (fab, fa) =>
    pipe(
      fab,
      E.flatMap(f =>
        pipe(
          fa,
          E.map(f),
          E.mapLeft(e1 =>
            pipe(
              fab,
              E.mapLeft(e2 => [...e2, ...e1]),
              E.getLeft,
              O.getOrElse((): E[] => e1)
            )
          )
        )
      )
    )
});

const validateForm = (
  email: string,
  age: number
): Validation<{ email: string; age: number }> =>
  pipe(
    sequenceT(getValidationApplicative<ValidationError>())(
      pipe(email, validateRequired('email'), E.flatMap(validateEmail)),
      validateAge(age)
    ),
    E.map(([email, age]) => ({ email, age }))
  );
```

### Dependency Injection

```typescript
import * as RTE from 'fp-ts/ReaderTaskEither';
import { pipe } from 'fp-ts/function';

type Services = {
  userRepo: UserRepository;
  emailService: EmailService;
  logger: Logger;
};

class UserService {
  getUser(id: number): RTE.ReaderTaskEither<Services, Error, User> {
    return pipe(
      RTE.ask<Services>(),
      RTE.flatMap(({ userRepo, logger }) =>
        RTE.tryCatch(
          async () => {
            logger.info(`Fetching user ${id}`);
            return userRepo.findById(id);
          },
          e => new Error(`Failed: ${e}`)
        )
      )
    );
  }

  createUser(data: UserData): RTE.ReaderTaskEither<Services, Error, User> {
    return pipe(
      RTE.Do,
      RTE.bind('services', () => RTE.ask<Services>()),
      RTE.bind('user', ({ services }) =>
        RTE.tryCatch(
          () => services.userRepo.create(data),
          e => new Error(`Failed: ${e}`)
        )
      ),
      RTE.chainFirst(({ services, user }) =>
        RTE.fromTask(() => 
          services.emailService.sendWelcome(user.email)
        )
      ),
      RTE.map(({ user }) => user)
    );
  }
}

// Usage
const services: Services = {
  userRepo: new UserRepository(),
  emailService: new EmailService(),
  logger: new Logger()
};

const userService = new UserService();

userService.createUser(userData)(services)()
  .then(E.fold(
    error => console.error(error),
    user => console.log('Created:', user)
  ));
```

## Best Practices

1. **Use pipe for data flow**: Always use `pipe` for left-to-right data transformation
2. **Leverage Do notation**: Use Do notation for imperative-style sequencing when clearer
3. **Choose appropriate effects**: Use TaskEither for async+errors, Reader for DI, IO for side effects
4. **Prefer traverse over manual loops**: Use `traverse` and `sequence` for effectful operations
5. **Type your errors explicitly**: Use discriminated unions for error types
6. **Use Applicative for parallel**: Use `ApplicativePar` for parallel execution
7. **Compose with flow**: Use `flow` to create reusable function compositions
8. **Avoid nesting**: Flatten nested structures with `flatMap`
9. **Use type classes**: Leverage Eq, Ord, Semigroup, Monoid for generic operations
10. **Test with property-based testing**: fp-ts types work great with fast-check

## Common Patterns

### Error Recovery

```typescript
const fetchWithRetry = <A>(
  fetch: TE.TaskEither<Error, A>,
  maxRetries: number
): TE.TaskEither<Error, A> => {
  const retry = (n: number): TE.TaskEither<Error, A> =>
    pipe(
      fetch,
      TE.orElse(error =>
        n > 0
          ? pipe(
              T.delay(1000)(T.of(undefined)),
              TE.fromTask,
              TE.flatMap(() => retry(n - 1))
            )
          : TE.left(error)
      )
    );
  
  return retry(maxRetries);
};
```

### Caching

```typescript
const cached = <A>(
  fetch: TE.TaskEither<Error, A>
): TE.TaskEither<Error, A> => {
  let cache: O.Option<A> = O.none;
  
  return pipe(
    cache,
    O.fold(
      () =>
        pipe(
          fetch,
          TE.map(value => {
            cache = O.some(value);
            return value;
          })
        ),
      value => TE.right(value)
    )
  );
};
```

### Resource Management

```typescript
const bracket = <R, E, A>(
  acquire: TE.TaskEither<E, R>,
  use: (r: R) => TE.TaskEither<E, A>,
  release: (r: R) => TE.TaskEither<E, void>
): TE.TaskEither<E, A> =>
  pipe(
    acquire,
    TE.flatMap(resource =>
      pipe(
        use(resource),
        TE.chainFirst(() => release(resource))
      )
    )
  );
```

## Integration with Effect-TS

fp-ts is evolving as part of the Effect-TS ecosystem, which provides even richer effect and functional abstractions. Consider Effect for new projects requiring advanced features like fiber-based concurrency, structured concurrency, resource management, and more sophisticated effect systems.

```typescript
import { Effect } from 'effect';

// Effect provides more powerful abstractions
const program = Effect.gen(function* (_) {
  const user = yield* _(fetchUser(1));
  const posts = yield* _(fetchPosts(user.id));
  return { user, posts };
});
```
