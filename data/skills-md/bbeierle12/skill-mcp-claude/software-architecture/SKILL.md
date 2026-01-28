---
name: software-architecture
description: Implements design patterns including Clean Architecture, SOLID principles, and comprehensive software design best practices. Use when designing systems, reviewing architecture, establishing patterns, or making structural decisions.
---

# Software Architecture

## SOLID Principles

### Single Responsibility Principle (SRP)
A class should have only one reason to change.

```typescript
// ❌ Bad: Multiple responsibilities
class User {
  saveToDatabase() { }
  sendEmail() { }
  generateReport() { }
}

// ✅ Good: Single responsibility
class User { }
class UserRepository { save(user: User) { } }
class EmailService { send(to: string) { } }
class ReportGenerator { generate(user: User) { } }
```

### Open/Closed Principle (OCP)
Open for extension, closed for modification.

```typescript
// ❌ Bad: Requires modification for new types
function calculateArea(shape: Shape) {
  if (shape.type === 'circle') {
    return Math.PI * shape.radius ** 2;
  } else if (shape.type === 'rectangle') {
    return shape.width * shape.height;
  }
  // Need to modify for new shapes
}

// ✅ Good: Extend without modification
interface Shape {
  area(): number;
}

class Circle implements Shape {
  constructor(private radius: number) {}
  area() { return Math.PI * this.radius ** 2; }
}

class Rectangle implements Shape {
  constructor(private width: number, private height: number) {}
  area() { return this.width * this.height; }
}
```

### Liskov Substitution Principle (LSP)
Subtypes must be substitutable for their base types.

```typescript
// ❌ Bad: Square violates Rectangle's contract
class Rectangle {
  setWidth(w: number) { this.width = w; }
  setHeight(h: number) { this.height = h; }
}

class Square extends Rectangle {
  setWidth(w: number) { this.width = w; this.height = w; } // Violates LSP
}

// ✅ Good: Separate hierarchies
interface Shape {
  area(): number;
}

class Rectangle implements Shape { }
class Square implements Shape { }
```

### Interface Segregation Principle (ISP)
Clients shouldn't depend on interfaces they don't use.

```typescript
// ❌ Bad: Fat interface
interface Worker {
  work(): void;
  eat(): void;
  sleep(): void;
}

// ✅ Good: Segregated interfaces
interface Workable { work(): void; }
interface Eatable { eat(): void; }
interface Sleepable { sleep(): void; }

class Human implements Workable, Eatable, Sleepable { }
class Robot implements Workable { }
```

### Dependency Inversion Principle (DIP)
Depend on abstractions, not concretions.

```typescript
// ❌ Bad: High-level depends on low-level
class UserService {
  private database = new MySQLDatabase();
}

// ✅ Good: Both depend on abstraction
interface Database {
  save(data: any): Promise<void>;
  find(id: string): Promise<any>;
}

class UserService {
  constructor(private database: Database) {}
}

// Now can inject any implementation
const service = new UserService(new MySQLDatabase());
const testService = new UserService(new MockDatabase());
```

## Clean Architecture

```
┌─────────────────────────────────────────────────┐
│                  Frameworks                      │
│  (Express, React, Database Drivers)              │
├─────────────────────────────────────────────────┤
│              Interface Adapters                  │
│  (Controllers, Presenters, Gateways)            │
├─────────────────────────────────────────────────┤
│              Application Layer                   │
│  (Use Cases, Application Services)              │
├─────────────────────────────────────────────────┤
│                Domain Layer                      │
│  (Entities, Value Objects, Domain Services)     │
└─────────────────────────────────────────────────┘

Dependencies point INWARD only.
Inner layers know nothing about outer layers.
```

### Domain Layer (Innermost)

```typescript
// entities/User.ts
export class User {
  constructor(
    public readonly id: string,
    public readonly email: Email,
    public name: string,
    private password: HashedPassword
  ) {}

  changeName(newName: string): void {
    if (newName.length < 2) {
      throw new DomainError('Name too short');
    }
    this.name = newName;
  }

  verifyPassword(plaintext: string): boolean {
    return this.password.verify(plaintext);
  }
}

// value-objects/Email.ts
export class Email {
  constructor(private readonly value: string) {
    if (!this.isValid(value)) {
      throw new DomainError('Invalid email');
    }
  }

  private isValid(email: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  toString(): string {
    return this.value;
  }
}
```

### Application Layer (Use Cases)

```typescript
// use-cases/CreateUser.ts
interface CreateUserInput {
  email: string;
  password: string;
  name: string;
}

interface CreateUserOutput {
  id: string;
  email: string;
  name: string;
}

export class CreateUserUseCase {
  constructor(
    private userRepository: UserRepository,
    private passwordHasher: PasswordHasher,
    private emailService: EmailService
  ) {}

  async execute(input: CreateUserInput): Promise<CreateUserOutput> {
    // Validate email uniqueness
    const existing = await this.userRepository.findByEmail(input.email);
    if (existing) {
      throw new ApplicationError('Email already exists');
    }

    // Create domain object
    const hashedPassword = await this.passwordHasher.hash(input.password);
    const user = new User(
      generateId(),
      new Email(input.email),
      input.name,
      hashedPassword
    );

    // Persist
    await this.userRepository.save(user);

    // Side effects
    await this.emailService.sendWelcome(user.email);

    return {
      id: user.id,
      email: user.email.toString(),
      name: user.name,
    };
  }
}
```

### Interface Adapters

```typescript
// controllers/UserController.ts
export class UserController {
  constructor(private createUserUseCase: CreateUserUseCase) {}

  async create(req: Request, res: Response): Promise<void> {
    const result = await this.createUserUseCase.execute({
      email: req.body.email,
      password: req.body.password,
      name: req.body.name,
    });

    res.status(201).json(result);
  }
}

// repositories/PrismaUserRepository.ts
export class PrismaUserRepository implements UserRepository {
  async save(user: User): Promise<void> {
    await prisma.user.create({
      data: {
        id: user.id,
        email: user.email.toString(),
        name: user.name,
      },
    });
  }

  async findByEmail(email: string): Promise<User | null> {
    const data = await prisma.user.findUnique({
      where: { email },
    });
    return data ? this.toDomain(data) : null;
  }

  private toDomain(data: PrismaUser): User {
    return new User(
      data.id,
      new Email(data.email),
      data.name,
      new HashedPassword(data.password)
    );
  }
}
```

## Design Patterns

### Repository Pattern
```typescript
interface Repository<T> {
  findById(id: string): Promise<T | null>;
  findAll(): Promise<T[]>;
  save(entity: T): Promise<void>;
  delete(id: string): Promise<void>;
}
```

### Factory Pattern
```typescript
interface PaymentProcessor {
  process(amount: number): Promise<void>;
}

class PaymentProcessorFactory {
  create(type: 'stripe' | 'paypal'): PaymentProcessor {
    switch (type) {
      case 'stripe': return new StripeProcessor();
      case 'paypal': return new PayPalProcessor();
    }
  }
}
```

### Strategy Pattern
```typescript
interface PricingStrategy {
  calculate(basePrice: number): number;
}

class RegularPricing implements PricingStrategy {
  calculate(basePrice: number) { return basePrice; }
}

class PremiumPricing implements PricingStrategy {
  calculate(basePrice: number) { return basePrice * 0.9; }
}

class Order {
  constructor(private pricingStrategy: PricingStrategy) {}
  
  getTotal(basePrice: number) {
    return this.pricingStrategy.calculate(basePrice);
  }
}
```

### Observer Pattern
```typescript
interface Observer<T> {
  update(data: T): void;
}

class EventEmitter<T> {
  private observers: Observer<T>[] = [];

  subscribe(observer: Observer<T>): void {
    this.observers.push(observer);
  }

  notify(data: T): void {
    this.observers.forEach(o => o.update(data));
  }
}
```

## Architecture Decision Records (ADR)

Document significant decisions:

```markdown
# ADR-001: Use PostgreSQL for Primary Database

## Status
Accepted

## Context
Need to choose a primary database for user data storage.

## Decision
Use PostgreSQL.

## Consequences
### Positive
- Strong consistency guarantees
- Rich query capabilities
- Well-supported ORMs

### Negative
- Requires more operational overhead than SQLite
- Horizontal scaling more complex than NoSQL
```

## Anti-Patterns to Avoid

### God Object
❌ One class that does everything

### Spaghetti Code
❌ No clear structure or flow

### Golden Hammer
❌ Using same solution for every problem

### Premature Optimization
❌ Optimizing before measuring

### Cargo Cult Programming
❌ Using patterns without understanding why
