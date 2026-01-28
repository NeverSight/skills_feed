---
name: architect-pro
description: Advanced Software Architecture Masterclass. Implements Clean Architecture, Hexagonal (Ports & Adapters), and DDD for 2026 ecosystems (Next.js 16.2, React 19.3, Node.js 24). Optimized for AI-driven development.
---

# Architect Pro: Advanced Software Architecture (2026 Edition)

Master the art of building maintainable, scalable, and testable systems using proven architectural patterns. This skill is optimized for the **Next.js 16.2 / React 19.3 / Node.js 24** ecosystem, focusing on decoupling business logic from infrastructure and enabling **Autonomous AI Agents** to work effectively within your codebase.

## 🎓 Prerequisites & Skill Level
- **Level**: Senior / Lead Engineer / Software Architect
- **Prerequisites**: 
  - Deep understanding of TypeScript 5.5+ (Generics, Discriminated Unions, Template Literal Types).
  - Familiarity with Next.js App Router and Server Components.
  - Basic knowledge of SQL (PostgreSQL) and NoSQL (Redis/MongoDB) databases.
  - Experience with automated testing (Jest, Vitest, Playwright).
  - Interest in Domain-Driven Design (DDD).

---

## 📌 Table of Contents
1. [Core Philosophy](#core-philosophy)
2. [Why Clean Architecture in 2026?](#why-clean-architecture-in-2026)
3. [Architecture for AI Agents](#architecture-for-ai-agents)
4. [Quick Start: The 2026 Stack](#quick-start-the-2026-stack)
5. [Modern Data Flow: React 19 + Next.js 16](#modern-data-flow-react-19--next-js-16)
6. [Standard Pattern: Clean Architecture + Server Actions](#standard-pattern-clean-architecture--server-actions)
7. [Tactical DDD: Entities, Value Objects, and Aggregates](#tactical-ddd-entities-value-objects-and-aggregates)
8. [Domain Services vs Application Services](#domain-services-vs-application-services)
9. [Advanced Pattern: Event-Driven DDD](#advanced-pattern-event-driven-ddd)
10. [Event Storming & Domain Modeling](#event-storming--domain-modeling)
11. [Architecture Decision Records (ADR)](#architecture-decision-records-adr)
12. [Context Mapping & Strategic DDD](#context-mapping--strategic-ddd)
13. [Testing Strategy for Architects](#testing-strategy-for-architects)
14. [Architectural Enforcement & Guardrails](#architectural-enforcement--guardrails)
15. [Performance & Scalability at the Architectural Level](#performance--scalability-at-the-architectural-level)
16. [Glossary of Architectural Terms](#glossary-of-architectural-terms)
17. [The Do Not List (Anti-Patterns)](#the-do-not-list-anti-patterns)
18. [Deep-Dive References](#deep-dive-references)
19. [Repository Analysis with Repomix](#repository-analysis-with-repomix)

---

## 🏛️ Core Philosophy
In 2026, software is increasingly built and refactored by **AI Coding Agents**. For an agent to be effective, the codebase must have **predictable boundaries** and **explicit contracts**.

- **Decoupling**: Business logic (Domain) must not depend on the database, UI, or frameworks.
- **Testability**: You should be able to test your core logic without spinning up a database or mocking complex framework internals.
- **Independence**: The system should be agnostic of its delivery mechanisms (Web, CLI, Mobile, AI Agents).
- **Predictability**: Files and folders should follow a strict convention so that both humans and AI can locate logic instantly.

---

## 🧠 Why Clean Architecture in 2026?
The "Move Fast and Break Things" era has evolved into the "Move Fast with AI and Maintain Sanity" era. Without a solid architecture:
1. **AI Agents Hallucinate**: When business logic is mixed with Prisma queries and React hooks, AI often loses context and introduces subtle bugs.
2. **Framework Churn**: Next.js and React versions move fast. A clean domain layer protects you from the next breaking change in the `app` router or server actions.
3. **Complexity Debt**: What starts as a simple "CRUD" app often grows into a complex domain. Clean Architecture allows for "Gradual Complexity" where you can add layers only when needed.

---

## 🤖 Architecture for AI Agents
In 2026, we design for two audiences: Humans and Agents.
- **Deterministic File Paths**: Using a strict Clean Architecture folder structure helps AI find the "Source of Truth" (Domain) instantly.
- **Strong Typing (TS 5.5+)**: Explicit return types in Use Cases act as "API Documentation" for AI agents.
- **Small Context Windows**: Decoupled layers allow AI to work on a single file (like a Use Case) without needing to understand the entire database schema.
- **Repomix Context Packing**: We use tools to pack high-density context for AI agents, and a clean architecture makes this packing 10x more efficient.

---

## ⚡ Quick Start: The 2026 Stack
The most common production stack in 2026 uses **Next.js 16.2** with **Server Functions**, **TypeScript 5.x**, and **Bun/pnpm** monorepos.

### Recommended Folder Structure
```bash
src/
├── domain/           # Core Logic (The "Truth")
│   ├── entities/     # Identifiable objects with identity and lifecycle
│   ├── value-objects/# Data wrappers with validation (Email, Money)
│   ├── services/     # Pure logic involving multiple entities
│   ├── events/       # Domain Events (OrderPlaced, UserDeactivated)
│   └── exceptions/   # Custom domain exceptions
├── application/      # Orchestration (The "User's Intent")
│   ├── use-cases/    # Specific business actions (Commands)
│   ├── ports/        # Interfaces (contracts for Infrastructure)
│   ├── dtos/         # Data Transfer Objects
│   └── queries/      # Read-only operations (if using CQRS)
├── infrastructure/   # Tools (The "Implementation")
│   ├── adapters/     # Implementations of Ports (Prisma, Stripe, AWS)
│   ├── persistence/  # DB Schemas, Migrations, Seeders
│   └── external/     # Third-party API clients
├── presentation/     # UI (The "View")
│   ├── components/   # React 19 Server/Client components
│   ├── actions/      # Next.js Server Actions (Primary Adapters)
│   └── pages/        # Route Handlers and Page definitions
└── shared/           # Cross-cutting concerns (Constants, Utils)
```

---

## 🌊 Modern Data Flow: React 19 + Next.js 16
The interaction model has changed. We no longer just "fetch from API". We "Invoke a Service".

### 1. View (React 19)
Uses the new `useActionState` and `useOptimistic` for a seamless UX.
```typescript
// presentation/components/ProjectForm.tsx
'use client'

import { useActionState } from 'react';
import { createProjectAction } from '../actions/project-actions';

export function ProjectForm() {
  const [state, formAction, isPending] = useActionState(createProjectAction, null);

  return (
    <form action={formAction}>
      <div className="flex flex-col gap-4">
        <label htmlFor="projectName">Project Name</label>
        <input 
          id="projectName" 
          name="projectName" 
          className="border p-2 rounded" 
          required 
        />
        <button 
          className="bg-blue-600 text-white p-2 rounded"
          disabled={isPending}
        >
          {isPending ? 'Creating...' : 'Create Project'}
        </button>
        {state?.error && <p className="text-red-500">{state.error}</p>}
      </div>
    </form>
  );
}
```

### 2. Action (Next.js 16.2)
Acts as the **Primary Adapter**. It handles the transition from HTTP (FormData) to Application logic.
```typescript
// presentation/actions/project-actions.ts
'use server'

import { CreateProjectUseCase } from '@/application/use-cases/CreateProject';
import { PrismaProjectRepository } from '@/infrastructure/adapters/PrismaProjectRepository';

export async function createProjectAction(prevState: any, formData: FormData) {
  const name = formData.get('projectName') as string;
  
  // Dependency Injection: In 2026, we prefer explicit composition over complex DI containers
  const repo = new PrismaProjectRepository();
  const useCase = new CreateProjectUseCase(repo);

  try {
    const project = await useCase.execute({ name });
    return { success: true, data: project };
  } catch (e) {
    // Audit log or Error tracking integration
    console.error("[Action Error]", e);
    return { success: false, error: e.message };
  }
}
```

---

## 🛠️ Standard Pattern: Clean Architecture + Server Actions

### 1. The Domain Entity
Entities represent business concepts with identity.
```typescript
// src/domain/entities/User.ts
import { Email } from '../value-objects/Email';

export class User {
  constructor(
    public readonly id: string,
    public readonly email: Email,
    private _isActive: boolean = true
  ) {}

  public deactivate() {
    this._isActive = false;
  }

  get isActive() { return this._isActive; }
}
```

### 2. The Use Case (Application Layer)
Use Cases orchestrate the domain objects to perform a specific task.
```typescript
// src/application/use-cases/DeactivateUser.ts
import { IUserRepository } from '../ports/IUserRepository';

export class DeactivateUserUseCase {
  constructor(private userRepo: IUserRepository) {}

  async execute(userId: string): Promise<void> {
    // 1. Fetch from repository (Port)
    const user = await this.userRepo.findById(userId);
    if (!user) throw new Error("User not found");
    
    // 2. Perform domain logic (Entity)
    user.deactivate();
    
    // 3. Persist changes (Port)
    await this.userRepo.save(user);
  }
}
```

### 3. The Repository Implementation (Infrastructure)
The "Adapter" that talks to the database.
```typescript
// src/infrastructure/adapters/PrismaUserRepository.ts
import { IUserRepository } from '@/application/ports/IUserRepository';
import { User } from '@/domain/entities/User';
import { Email } from '@/domain/value-objects/Email';
import { prisma } from '../prisma';

export class PrismaUserRepository implements IUserRepository {
  async findById(id: string): Promise<User | null> {
    const data = await prisma.user.findUnique({ where: { id } });
    if (!data) return null;
    
    return new User(
      data.id,
      Email.create(data.email),
      data.isActive
    );
  }

  async save(user: User): Promise<void> {
    await prisma.user.upsert({
      where: { id: user.id },
      update: { isActive: user.isActive },
      create: { 
        id: user.id, 
        email: user.email.value, 
        isActive: user.isActive 
      }
    });
  }
}
```

---

## 🧩 Tactical DDD: Entities, Value Objects, and Aggregates

### Value Objects (The Power of Types)
Don't use `string` for everything. Use Value Objects for validation and business logic.
```typescript
// domain/value-objects/Money.ts
export class Money {
  private constructor(public readonly amount: number, public readonly currency: string) {}

  static create(amount: number, currency: string = 'USD'): Money {
    if (amount < 0) throw new Error("Amount cannot be negative");
    return new Money(amount, currency);
  }

  add(other: Money): Money {
    if (this.currency !== other.currency) throw new Error("Currency mismatch");
    return new Money(this.amount + other.amount, this.currency);
  }
}
```

### Aggregates (The Consistency Boundary)
An Aggregate ensures that business rules are always met across multiple related objects.
```typescript
// domain/entities/Order.ts
export class Order {
  private items: OrderItem[] = [];
  
  addItem(product: Product, quantity: number) {
    const totalItems = this.items.reduce((sum, item) => sum + item.quantity, 0);
    if (totalItems + quantity > 50) {
      throw new Error("An order cannot have more than 50 items");
    }
    this.items.push(new OrderItem(product.id, quantity));
  }
}
```

---

## ⚙️ Domain Services vs Application Services
One of the most common points of confusion in DDD.

- **Domain Service**: Contains business logic that belongs to the domain but doesn't fit in a single entity (e.g., `TransferService` between two bank accounts). It works with entities and value objects.
- **Application Service (Use Case)**: Contains NO business logic. It only orchestrates. It calls repositories, triggers domain services, and sends emails.

---

## 🚀 Advanced Pattern: Event-Driven DDD
Capture intent and decouple side-effects.

### Domain Service Example
```typescript
// domain/services/TransferService.ts
export class TransferService {
  async execute(from: Account, to: Account, amount: Money) {
    from.withdraw(amount);
    to.deposit(amount);
    
    // Domain Events are captured here
    return new FundsTransferredEvent(from.id, to.id, amount);
  }
}
```

---

## 🌪️ Event Storming & Domain Modeling
In 2026, we don't start with "Tables". We start with "Events".
1. **Domain Events**: What happens in the business? (e.g., `OrderPlaced`, `InventoryReduced`).
2. **Commands**: What triggers these events? (e.g., `PlaceOrder`).
3. **Aggregates**: What objects are involved in making sure the rules are followed?
4. **Read Models**: How do we want to display this information to the user?

---

## 📝 Architecture Decision Records (ADR)
In 2026, we record *why* we made a choice, not just *what* we chose.
```markdown
# ADR 005: Use Clean Architecture for AI Core

## Status
Accepted

## Context
We need a way for AI agents to refactor code safely without breaking business rules. The previous "Spaghetti Monolith" resulted in AI hallucinating database queries in React components.

## Decision
We will use Clean Architecture with strict separation between Domain and Infrastructure.

## Consequences
- Pros: Predictable file structure, high testability, zero framework leakage in domain.
- Cons: More boilerplate for simple CRUD operations, higher learning curve for junior devs.
```

---

## 🗺️ Context Mapping & Strategic DDD
How different parts of the system talk to each other.
- **Customer/Supplier**: One team depends on another.
- **Shared Kernel**: Two teams share a common model (rarely recommended).
- **Anticorruption Layer (ACL)**: A layer that translates between a legacy system and your clean new system.
- **Separate Ways**: No relationship between contexts.

---

## 🧪 Testing Strategy for Architects
In a Clean Architecture, you have different "Testing Grooves":

1. **Domain Unit Tests**: Test entities and value objects. ZERO mocks needed. 100% code coverage expected here.
2. **Use Case Tests**: Test orchestration. Use **In-Memory Adapters** (Mocks/Fakes) for the database.
3. **Integration Tests**: Test the real adapters (e.g., Prisma repository against a real Test Container).
4. **E2E Tests**: Test the full Next.js flow using Playwright.

### Example: Use Case Test (No DB)
```typescript
// tests/use-cases/DeactivateUser.test.ts
import { DeactivateUserUseCase } from '@/application/use-cases/DeactivateUser';
import { InMemoryUserRepository } from '../mocks/InMemoryUserRepository';

test('should deactivate user', async () => {
  const repo = new InMemoryUserRepository();
  await repo.save({ id: '1', email: 'test@test.com', isActive: true });
  
  const useCase = new DeactivateUserUseCase(repo);
  await useCase.execute('1');
  
  const user = await repo.findById('1');
  expect(user.isActive).toBe(false);
});
```

---

## 🛡️ Architectural Enforcement & Guardrails
Use tools to ensure the "Dependency Rule" is never broken.

### `dependency-cruiser` config (2026 best practice)
```json
{
  "forbidden": [
    {
      "name": "domain-not-import-infra",
      "from": { "path": "src/domain" },
      "to": { "path": "src/infrastructure" }
    },
    {
      "name": "usecase-not-import-infra",
      "from": { "path": "src/application" },
      "to": { "path": "src/infrastructure" }
    },
    {
      "name": "presentation-not-import-infra",
      "from": { "path": "src/presentation" },
      "to": { "path": "src/infrastructure" }
    }
  ]
}
```

---

## 📈 Performance & Scalability at the Architectural Level
- **Read-Write Segregation (CQRS)**: Use a fast NoSQL database for reads and a robust SQL database for writes.
- **Caching as a First-Class Citizen**: Don't put cache logic in your Use Case. Use a **Caching Adapter** or the Next.js `use cache` directive in the presentation layer.
- **Job Queues**: Offload heavy work (Email, AI Processing) to background jobs via Domain Events.

---

## 📖 Glossary of Architectural Terms
- **Bounded Context**: A specific boundary (usually a module or service) where a domain model is consistent.
- **Port**: An interface defined by the application layer that infrastructure must implement.
- **Adapter**: An implementation of a port (e.g., a SQL database implementation of an `IUserRepository`).
- **Inversion of Control (IoC)**: The principle where the domain defines its needs (Ports), and the high-level layers provide the implementations (Adapters).
- **Aggregate Root**: The main entity in an aggregate that controls all access and enforces business rules.
- **Ubiquitous Language**: A common language used by all team members to describe the domain.

---

## 🚫 The Do Not List (Anti-Patterns)

### 1. **Framework Leakage**
**BAD**: Using `@prisma/client` types as return types in your Domain or Application layers.
**GOOD**: Map database rows to Domain Entities in the Infrastructure layer.

### 2. **Anemic Domain Model**
**BAD**: Putting all your logic in `UserService` and having `User` as just a `type`.
**GOOD**: Move business rules (e.g., `user.canJoinProject()`) into the `User` class.

### 3. **The "Shared" Dumpster**
**BAD**: Putting everything in `shared/` because you are too lazy to decide where it belongs.
**GOOD**: Keep `shared/` minimal. If it's business-related, it's `domain/`. If it's tool-related, it's `infrastructure/`.

### 4. **Premature Microservices**
**BAD**: Splitting into 10 repos before you understand the domain boundaries.
**GOOD**: Build a **Modular Monolith** using Clean Architecture first. Boundaries are easy to cut later if they are clean.

### 5. **Lazy Naming**
**BAD**: `data`, `info`, `manager`, `process`.
**GOOD**: `PaymentRecord`, `UserAuthenticationDetails`, `OrderOrchestrator`.

---

## 📚 Deep-Dive References
Explore our specialized documentation for deeper technical insights:
- [Clean Architecture Guide](./references/clean-architecture.md)
- [Hexagonal Architecture (Ports & Adapters)](./references/hexagonal-architecture.md)
- [DDD Patterns & Tactical Design](./references/ddd-patterns.md)
- [Performance & Scalability 2026](./references/performance-scalability.md)
- [Migration & Refactoring Strategies](./references/migration-refactoring.md)
- [Repository Analysis Guide](./references/repository-analysis.md)

---

## 🔍 Repository Analysis with Repomix
Before refactoring, always analyze the existing codebase structure.
```bash
# Optimized command for architecture discovery
npx repomix@latest --include "src/**/*.ts" --compress --output /tmp/arch-discovery.xml
```
Using Repomix allows you to "pack" your architecture into a single file that can be fed into an AI for a full audit.

---

## 💎 Best Practices Checklist
- [ ] Is my Domain Layer free of external dependencies?
- [ ] Are my Use Cases doing only orchestration?
- [ ] Do I have interfaces (Ports) for all external services (DB, Auth, Mail, Stripe)?
- [ ] Am I using Value Objects for things like Email, Money, and Address?
- [ ] Is my code testable without a real database?
- [ ] Have I mapped my infrastructure errors to domain exceptions?
- [ ] Have I used ADRs to document major architectural decisions?
- [ ] Is my ubiquitous language reflected in the code?

---

*Updated: January 22, 2026 - 15:18*
