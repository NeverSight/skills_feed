---
name: design-patterns
description: Classic and modern software design patterns
domain: software-design
version: 1.0.0
tags: [patterns, gang-of-four, creational, structural, behavioral, functional]
triggers:
  keywords:
    primary: [design pattern, pattern, singleton, factory, observer, strategy]
    secondary: [creational, structural, behavioral, gof, gang of four, adapter, decorator]
  context_boost: [oop, refactor, architecture, clean code]
  context_penalty: [database, devops, testing]
  priority: high
---

# Design Patterns

## Overview

Reusable solutions to common software design problems. Understanding patterns helps you communicate design ideas effectively and avoid reinventing the wheel.

---

## Creational Patterns

### Factory Method
**Purpose**: Create objects without specifying exact class

```typescript
// Abstract factory
interface PaymentProcessor {
  process(amount: number): Promise<Result>;
}

class StripeProcessor implements PaymentProcessor { /* ... */ }
class PayPalProcessor implements PaymentProcessor { /* ... */ }

function createProcessor(type: string): PaymentProcessor {
  switch (type) {
    case 'stripe': return new StripeProcessor();
    case 'paypal': return new PayPalProcessor();
    default: throw new Error(`Unknown processor: ${type}`);
  }
}
```

### Builder
**Purpose**: Construct complex objects step by step

```typescript
class QueryBuilder {
  private query: Query = {};

  select(...fields: string[]) {
    this.query.fields = fields;
    return this;
  }

  from(table: string) {
    this.query.table = table;
    return this;
  }

  where(condition: Condition) {
    this.query.conditions ??= [];
    this.query.conditions.push(condition);
    return this;
  }

  build(): string {
    return this.compile(this.query);
  }
}

// Usage
const sql = new QueryBuilder()
  .select('id', 'name')
  .from('users')
  .where({ age: { gte: 18 } })
  .build();
```

### Singleton
**Purpose**: Ensure single instance (use sparingly)

```typescript
// Modern approach: module-level instance
// database.ts
class Database {
  private constructor() {}

  private static instance: Database;

  static getInstance(): Database {
    if (!Database.instance) {
      Database.instance = new Database();
    }
    return Database.instance;
  }
}

// Better: Dependency injection
class UserService {
  constructor(private db: Database) {}
}
```

---

## Structural Patterns

### Adapter
**Purpose**: Make incompatible interfaces work together

```typescript
// Legacy API returns XML
interface LegacyAPI {
  getDataXML(): string;
}

// New code expects JSON
interface ModernAPI {
  getData(): object;
}

class APIAdapter implements ModernAPI {
  constructor(private legacy: LegacyAPI) {}

  getData(): object {
    const xml = this.legacy.getDataXML();
    return this.parseXML(xml);
  }

  private parseXML(xml: string): object {
    // Convert XML to object
  }
}
```

### Decorator
**Purpose**: Add behavior without modifying original

```typescript
// Base interface
interface DataSource {
  read(): string;
  write(data: string): void;
}

// Decorator adds encryption
class EncryptedDataSource implements DataSource {
  constructor(private wrapped: DataSource) {}

  read(): string {
    return this.decrypt(this.wrapped.read());
  }

  write(data: string): void {
    this.wrapped.write(this.encrypt(data));
  }
}

// Decorator adds compression
class CompressedDataSource implements DataSource {
  constructor(private wrapped: DataSource) {}
  // Similar pattern...
}

// Compose decorators
const source = new EncryptedDataSource(
  new CompressedDataSource(
    new FileDataSource('data.txt')
  )
);
```

### Facade
**Purpose**: Simplify complex subsystem

```typescript
// Complex subsystems
class VideoConverter { /* ... */ }
class AudioExtractor { /* ... */ }
class BitrateCalculator { /* ... */ }
class CodecFactory { /* ... */ }

// Simple facade
class VideoExporter {
  export(video: Video, format: Format): File {
    const codec = CodecFactory.getCodec(format);
    const bitrate = BitrateCalculator.optimal(video);
    const converter = new VideoConverter(codec, bitrate);
    const audio = AudioExtractor.extract(video);
    return converter.convert(video, audio);
  }
}

// Client only needs facade
const exporter = new VideoExporter();
const mp4 = exporter.export(video, 'mp4');
```

### Proxy
**Purpose**: Control access to object

```typescript
// Virtual proxy for lazy loading
class ImageProxy implements Image {
  private realImage: RealImage | null = null;

  constructor(private filename: string) {}

  display(): void {
    if (!this.realImage) {
      this.realImage = new RealImage(this.filename); // Expensive
    }
    this.realImage.display();
  }
}

// Protection proxy
class SecureDocumentProxy implements Document {
  constructor(
    private doc: Document,
    private user: User
  ) {}

  read(): string {
    if (!this.user.hasPermission('read')) {
      throw new Error('Access denied');
    }
    return this.doc.read();
  }
}
```

---

## Behavioral Patterns

### Observer
**Purpose**: Notify dependents of state changes

```typescript
class EventEmitter<T extends Record<string, unknown>> {
  private listeners = new Map<keyof T, Set<Function>>();

  on<K extends keyof T>(event: K, callback: (data: T[K]) => void) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event)!.add(callback);

    // Return unsubscribe function
    return () => this.listeners.get(event)?.delete(callback);
  }

  emit<K extends keyof T>(event: K, data: T[K]) {
    this.listeners.get(event)?.forEach(cb => cb(data));
  }
}

// Usage
interface Events {
  userCreated: User;
  orderPlaced: Order;
}

const emitter = new EventEmitter<Events>();
emitter.on('userCreated', user => sendWelcomeEmail(user));
```

### Strategy
**Purpose**: Interchange algorithms at runtime

```typescript
interface CompressionStrategy {
  compress(data: Buffer): Buffer;
}

class ZipCompression implements CompressionStrategy {
  compress(data: Buffer): Buffer { /* ... */ }
}

class GzipCompression implements CompressionStrategy {
  compress(data: Buffer): Buffer { /* ... */ }
}

class FileCompressor {
  constructor(private strategy: CompressionStrategy) {}

  setStrategy(strategy: CompressionStrategy) {
    this.strategy = strategy;
  }

  compress(file: File): Buffer {
    return this.strategy.compress(file.data);
  }
}
```

### Command
**Purpose**: Encapsulate actions as objects

```typescript
interface Command {
  execute(): void;
  undo(): void;
}

class MoveCommand implements Command {
  private previousPosition: Position;

  constructor(
    private object: GameObject,
    private newPosition: Position
  ) {}

  execute() {
    this.previousPosition = this.object.position;
    this.object.position = this.newPosition;
  }

  undo() {
    this.object.position = this.previousPosition;
  }
}

class CommandHistory {
  private history: Command[] = [];
  private current = -1;

  execute(command: Command) {
    command.execute();
    this.history = this.history.slice(0, this.current + 1);
    this.history.push(command);
    this.current++;
  }

  undo() {
    if (this.current >= 0) {
      this.history[this.current].undo();
      this.current--;
    }
  }

  redo() {
    if (this.current < this.history.length - 1) {
      this.current++;
      this.history[this.current].execute();
    }
  }
}
```

### State
**Purpose**: Change behavior based on state

```typescript
interface State {
  handle(context: Context): void;
}

class DraftState implements State {
  handle(context: Context) {
    console.log('Document is draft');
    // Can edit, save, submit for review
  }
}

class ReviewState implements State {
  handle(context: Context) {
    console.log('Document under review');
    // Can approve or reject
  }
}

class PublishedState implements State {
  handle(context: Context) {
    console.log('Document is published');
    // Read-only, can unpublish
  }
}

class Document {
  private state: State = new DraftState();

  setState(state: State) {
    this.state = state;
  }

  handle() {
    this.state.handle(this);
  }
}
```

---

## Functional Patterns

### Monad (Result/Option)
```typescript
type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };

function map<T, U, E>(
  result: Result<T, E>,
  fn: (value: T) => U
): Result<U, E> {
  return result.ok
    ? { ok: true, value: fn(result.value) }
    : result;
}

function flatMap<T, U, E>(
  result: Result<T, E>,
  fn: (value: T) => Result<U, E>
): Result<U, E> {
  return result.ok ? fn(result.value) : result;
}

// Usage - compose operations safely
const result = pipe(
  parseJSON(input),
  flatMap(validate),
  flatMap(save),
  map(formatResponse)
);
```

### Pipeline / Middleware
```typescript
type Middleware<T> = (context: T, next: () => Promise<void>) => Promise<void>;

class Pipeline<T> {
  private middlewares: Middleware<T>[] = [];

  use(middleware: Middleware<T>) {
    this.middlewares.push(middleware);
    return this;
  }

  async execute(context: T) {
    let index = 0;

    const next = async (): Promise<void> => {
      if (index < this.middlewares.length) {
        const middleware = this.middlewares[index++];
        await middleware(context, next);
      }
    };

    await next();
  }
}
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| God Object | One class does everything | Split into focused classes |
| Spaghetti Code | Tangled dependencies | Apply SRP, use modules |
| Golden Hammer | Using one pattern everywhere | Choose right pattern per problem |
| Premature Optimization | Optimizing before measuring | Profile first, then optimize |

---

## Decision Guide

```
Need to create objects?
├── Complex construction → Builder
├── Family of related objects → Abstract Factory
├── Subclass decides type → Factory Method
└── Single instance → Singleton (rarely)

Need to structure objects?
├── Make incompatible interfaces work → Adapter
├── Add behavior dynamically → Decorator
├── Simplify complex system → Facade
└── Control access → Proxy

Need to manage behavior?
├── Notify on state change → Observer
├── Swap algorithms → Strategy
├── Encapsulate actions → Command
└── State-dependent behavior → State
```

## Related Skills

- [[architecture-patterns]] - Higher-level patterns
- [[code-quality]] - When to apply patterns
- [[refactoring]] - Introducing patterns to existing code
