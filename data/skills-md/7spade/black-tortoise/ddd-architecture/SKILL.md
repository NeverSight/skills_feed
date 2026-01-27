---
name: ddd-architecture
description: Domain-Driven Design (DDD) patterns for Angular applications with clean architecture layers. Use when designing aggregates, entities, value objects, domain events, repositories, or implementing bounded contexts. Includes tactical patterns, strategic design, and layer dependency rules for scalable applications.
license: Complete terms in LICENSE.txt
---

# Domain-Driven Design (DDD) Architecture

## Rules

### Layered Architecture
- Use four-layer architecture: Presentation → Application → Domain ← Infrastructure
- Domain layer MUST be pure TypeScript with NO framework dependencies
- ALL dependencies point inward toward the Domain layer
- Do NOT allow Domain layer to depend on Application, Infrastructure, or Presentation

### Dependency Direction
- Presentation MAY depend on Application and Shared layers
- Application MAY depend on Domain and Shared layers
- Infrastructure MUST depend ONLY on Domain layer interfaces
- Domain MUST NOT depend on any other layer

### Domain Layer - Entities
- Use entities for objects with identity and lifecycle
- Encapsulate business logic in entity methods
- Use private fields with getters (NO public setters)
- Implement factory methods (e.g., `static create()`) for entity creation
- Raise domain events when state changes occur
- Do NOT expose internal state through public setters

### Domain Layer - Value Objects
- Use value objects for concepts without identity
- Make value objects IMMUTABLE (readonly fields, private constructor)
- Implement validation in static factory method (e.g., `static create()`)
- Implement `equals()` method for value-based equality comparison
- Do NOT create value objects without validation

### Domain Layer - Aggregates
- Use aggregates as consistency boundaries for related entities
- Enforce business invariants across all entities in the aggregate
- Access entities ONLY through the aggregate root
- Do NOT allow direct access to entities within an aggregate

### Domain Layer - Domain Events
- Raise domain events for business-significant occurrences
- Store events in entity's internal `_domainEvents` array
- Include `eventId`, `occurredOn`, and `eventType` in all events
- Clear events after publishing via `clearDomainEvents()`

### Domain Layer - Repository Interfaces
- Define repository interfaces in the Domain layer
- Use Observable return types for async operations
- Use domain entities and value objects in method signatures
- Do NOT implement repositories in the Domain layer

### Application Layer
- Orchestrate domain objects and infrastructure in application services
- Use command/query pattern for use case operations
- Publish domain events after persisting entities
- Do NOT put business logic in application services (belongs in Domain)

### Infrastructure Layer - Repository Implementation
- Implement domain repository interfaces in Infrastructure layer
- Convert between domain entities and persistence models
- Use `toDomain()` method to map persistence data to domain entities
- Use `toFirestore()` (or similar) method to map domain entities to persistence
- Do NOT expose persistence details to Domain or Application layers

### Testing
- Test domain entities and value objects independently (unit tests)
- Test invariants and business rules in domain layer
- Mock repository interfaces when testing application services
- Test domain event generation and clearing

---

## Context

### When to Use This Skill

Activate this skill when you need to:
- Design domain models with aggregates and entities
- Implement value objects and domain events
- Define repository interfaces and domain services
- Establish bounded contexts and ubiquitous language
- Enforce layer dependencies (Domain ← Application ← Infrastructure ← Presentation)
- Apply tactical DDD patterns (specifications, factories, domain events)
- Implement strategic DDD patterns (context mapping, anti-corruption layers)
- Migrate from anemic domain models to rich domain models

## Core DDD Concepts

### Layered Architecture

```
┌─────────────────────────────────────────┐
│      Presentation Layer (UI)            │  Angular Components
│      src/app/presentation/              │
└──────────────┬──────────────────────────┘
               │ depends on
┌──────────────▼──────────────────────────┐
│      Application Layer                  │  Use Cases, Stores
│      src/app/application/               │
└──────────────┬──────────────────────────┘
               │ depends on
┌──────────────▼──────────────────────────┐
│      Domain Layer (Business Logic)      │  Pure TypeScript
│      src/app/domain/                    │
└──────────────▲──────────────────────────┘
               │ implements
┌──────────────┴──────────────────────────┐
│      Infrastructure Layer               │  Firebase, External APIs
│      src/app/infrastructure/            │
└─────────────────────────────────────────┘
```

### Dependency Rules

**Golden Rule**: Dependencies point inward, never outward.

- ✅ Presentation → Application → Domain
- ✅ Infrastructure → Domain (implements interfaces)
- ❌ Domain → Application
- ❌ Domain → Infrastructure
- ❌ Domain → Presentation

## Domain Layer

### Entities

Entities have identity and lifecycle. Use for objects that need to be tracked over time.

```typescript
// src/app/domain/workspace/entities/workspace.entity.ts
import { WorkspaceId } from '../value-objects/workspace-id.value-object';
import { WorkspaceName } from '../value-objects/workspace-name.value-object';
import { WorkspaceCreatedEvent } from '../events/workspace-created.event';
import { DomainEvent } from '@domain/shared/domain-event';

export class Workspace {
  private readonly _id: WorkspaceId;
  private _name: WorkspaceName;
  private _ownerId: string;
  private _createdAt: Date;
  private _updatedAt: Date;
  private _domainEvents: DomainEvent[] = [];

  constructor(props: {
    id: WorkspaceId;
    name: WorkspaceName;
    ownerId: string;
    createdAt?: Date;
    updatedAt?: Date;
  }) {
    this._id = props.id;
    this._name = props.name;
    this._ownerId = props.ownerId;
    this._createdAt = props.createdAt ?? new Date();
    this._updatedAt = props.updatedAt ?? new Date();
  }

  // Factory method
  static create(props: { name: string; ownerId: string }): Workspace {
    const workspace = new Workspace({
      id: WorkspaceId.create(),
      name: WorkspaceName.create(props.name),
      ownerId: props.ownerId
    });
    
    // Raise domain event
    workspace.addDomainEvent(new WorkspaceCreatedEvent(workspace.id.value, workspace.name.value));
    
    return workspace;
  }

  // Getters (no setters - mutations via methods only)
  get id(): WorkspaceId { return this._id; }
  get name(): WorkspaceName { return this._name; }
  get ownerId(): string { return this._ownerId; }
  get createdAt(): Date { return this._createdAt; }
  get domainEvents(): DomainEvent[] { return this._domainEvents; }

  // Business methods encapsulate domain logic
  rename(newName: string): void {
    const oldName = this._name.value;
    this._name = WorkspaceName.create(newName);
    this._updatedAt = new Date();
    
    this.addDomainEvent(new WorkspaceRenamedEvent(this.id.value, oldName, newName));
  }

  // Invariant: Only owner can perform certain actions
  validateOwnership(userId: string): void {
    if (this._ownerId !== userId) {
      throw new Error('Only the owner can perform this action');
    }
  }

  private addDomainEvent(event: DomainEvent): void {
    this._domainEvents.push(event);
  }

  clearDomainEvents(): void {
    this._domainEvents = [];
  }
}
```

### Value Objects

Value objects have no identity, only value. They are immutable and equality is based on value.

```typescript
// src/app/domain/workspace/value-objects/workspace-name.value-object.ts
export class WorkspaceName {
  private readonly _value: string;

  private constructor(value: string) {
    this._value = value;
  }

  static create(value: string): WorkspaceName {
    // Validation rules
    if (!value || value.trim().length === 0) {
      throw new Error('Workspace name cannot be empty');
    }
    if (value.length > 100) {
      throw new Error('Workspace name cannot exceed 100 characters');
    }
    if (!/^[\w\s-]+$/.test(value)) {
      throw new Error('Workspace name contains invalid characters');
    }

    return new WorkspaceName(value.trim());
  }

  get value(): string {
    return this._value;
  }

  // Value objects are compared by value, not reference
  equals(other: WorkspaceName): boolean {
    return this._value === other._value;
  }

  toString(): string {
    return this._value;
  }
}
```

```typescript
// src/app/domain/workspace/value-objects/workspace-id.value-object.ts
import { v4 as uuidv4 } from 'uuid';

export class WorkspaceId {
  private readonly _value: string;

  private constructor(value: string) {
    this._value = value;
  }

  static create(): WorkspaceId {
    return new WorkspaceId(uuidv4());
  }

  static fromString(value: string): WorkspaceId {
    if (!this.isValid(value)) {
      throw new Error('Invalid workspace ID format');
    }
    return new WorkspaceId(value);
  }

  private static isValid(value: string): boolean {
    const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
    return uuidRegex.test(value);
  }

  get value(): string {
    return this._value;
  }

  equals(other: WorkspaceId): boolean {
    return this._value === other._value;
  }
}
```

### Aggregates

Aggregates are consistency boundaries. They group entities and value objects that must be consistent together.

```typescript
// src/app/domain/workspace/aggregates/workspace.aggregate.ts
import { Workspace } from '../entities/workspace.entity';
import { WorkspaceMember } from '../entities/workspace-member.entity';
import { MemberRole } from '../enums/member-role.enum';

export class WorkspaceAggregate {
  private readonly _workspace: Workspace;
  private readonly _members: WorkspaceMember[] = [];

  constructor(workspace: Workspace, members: WorkspaceMember[] = []) {
    this._workspace = workspace;
    this._members = members;
  }

  get workspace(): Workspace {
    return this._workspace;
  }

  get members(): ReadonlyArray<WorkspaceMember> {
    return this._members;
  }

  // Aggregate root enforces invariants across all entities
  addMember(userId: string, role: MemberRole, addedBy: string): void {
    // Invariant: Only admins or owner can add members
    const adder = this.findMember(addedBy);
    if (!adder || (!adder.isAdmin() && !this.isOwner(addedBy))) {
      throw new Error('Only admins or owner can add members');
    }

    // Invariant: Cannot add duplicate members
    if (this.findMember(userId)) {
      throw new Error('User is already a member');
    }

    // Invariant: Maximum members limit
    if (this._members.length >= 50) {
      throw new Error('Workspace has reached maximum member limit');
    }

    const member = WorkspaceMember.create({
      workspaceId: this._workspace.id.value,
      userId,
      role
    });

    this._members.push(member);
  }

  removeMember(userId: string, removedBy: string): void {
    // Invariant: Cannot remove the owner
    if (this.isOwner(userId)) {
      throw new Error('Cannot remove workspace owner');
    }

    // Invariant: Only admins or owner can remove members
    const remover = this.findMember(removedBy);
    if (!remover || (!remover.isAdmin() && !this.isOwner(removedBy))) {
      throw new Error('Only admins or owner can remove members');
    }

    const index = this._members.findIndex(m => m.userId === userId);
    if (index === -1) {
      throw new Error('Member not found');
    }

    this._members.splice(index, 1);
  }

  private findMember(userId: string): WorkspaceMember | undefined {
    return this._members.find(m => m.userId === userId);
  }

  private isOwner(userId: string): boolean {
    return this._workspace.ownerId === userId;
  }
}
```

### Domain Events

Domain events capture business-significant occurrences.

```typescript
// src/app/domain/shared/domain-event.ts
export interface DomainEvent {
  readonly eventId: string;
  readonly occurredOn: Date;
  readonly eventType: string;
}

export abstract class BaseDomainEvent implements DomainEvent {
  readonly eventId: string;
  readonly occurredOn: Date;
  readonly eventType: string;

  protected constructor(eventType: string) {
    this.eventId = uuidv4();
    this.occurredOn = new Date();
    this.eventType = eventType;
  }
}
```

```typescript
// src/app/domain/workspace/events/workspace-created.event.ts
import { BaseDomainEvent } from '@domain/shared/domain-event';

export class WorkspaceCreatedEvent extends BaseDomainEvent {
  constructor(
    public readonly workspaceId: string,
    public readonly name: string
  ) {
    super('WorkspaceCreated');
  }
}
```

### Repository Interfaces

Repositories are defined as interfaces in the domain layer and implemented in infrastructure.

```typescript
// src/app/domain/repositories/workspace.repository.ts
import { Observable } from 'rxjs';
import { Workspace } from '../workspace/entities/workspace.entity';
import { WorkspaceId } from '../workspace/value-objects/workspace-id.value-object';

export interface IWorkspaceRepository {
  findById(id: WorkspaceId): Observable<Workspace | null>;
  findByOwnerId(ownerId: string): Observable<Workspace[]>;
  save(workspace: Workspace): Observable<Workspace>;
  delete(id: WorkspaceId): Observable<void>;
}
```

### Domain Services

Domain services contain business logic that doesn't naturally fit in an entity or value object.

```typescript
// src/app/domain/services/workspace-guard.service.ts
export interface IWorkspaceGuardService {
  canUserAccessWorkspace(userId: string, workspaceId: string): Observable<boolean>;
  getUserPermissions(userId: string, workspaceId: string): Observable<string[]>;
}
```

## Application Layer

### Application Services

Application services orchestrate domain objects and infrastructure.

```typescript
// src/app/application/services/workspace.service.ts
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { map, tap } from 'rxjs/operators';
import { IWorkspaceRepository } from '@domain/repositories/workspace.repository';
import { Workspace } from '@domain/workspace/entities/workspace.entity';
import { WorkspaceId } from '@domain/workspace/value-objects/workspace-id.value-object';
import { DomainEventPublisher } from '@infrastructure/events/domain-event-publisher';

@Injectable({ providedIn: 'root' })
export class WorkspaceService {
  private readonly repository = inject(IWorkspaceRepository);
  private readonly eventPublisher = inject(DomainEventPublisher);

  createWorkspace(name: string, ownerId: string): Observable<Workspace> {
    // Create domain entity
    const workspace = Workspace.create({ name, ownerId });

    // Persist via repository
    return this.repository.save(workspace).pipe(
      tap(savedWorkspace => {
        // Publish domain events
        savedWorkspace.domainEvents.forEach(event => {
          this.eventPublisher.publish(event);
        });
        savedWorkspace.clearDomainEvents();
      })
    );
  }

  renameWorkspace(workspaceId: string, newName: string, userId: string): Observable<Workspace> {
    const id = WorkspaceId.fromString(workspaceId);
    
    return this.repository.findById(id).pipe(
      map(workspace => {
        if (!workspace) {
          throw new Error('Workspace not found');
        }
        
        // Domain logic enforces business rules
        workspace.validateOwnership(userId);
        workspace.rename(newName);
        
        return workspace;
      }),
      tap(workspace => this.repository.save(workspace)),
      tap(workspace => {
        workspace.domainEvents.forEach(event => {
          this.eventPublisher.publish(event);
        });
        workspace.clearDomainEvents();
      })
    );
  }
}
```

### Command Pattern

```typescript
// src/app/application/commands/create-workspace.command.ts
export class CreateWorkspaceCommand {
  constructor(
    public readonly name: string,
    public readonly ownerId: string
  ) {}
}

// src/app/application/commands/handlers/create-workspace.handler.ts
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { CreateWorkspaceCommand } from '../create-workspace.command';
import { WorkspaceService } from '@application/services/workspace.service';
import { Workspace } from '@domain/workspace/entities/workspace.entity';

@Injectable({ providedIn: 'root' })
export class CreateWorkspaceHandler {
  constructor(private workspaceService: WorkspaceService) {}

  execute(command: CreateWorkspaceCommand): Observable<Workspace> {
    return this.workspaceService.createWorkspace(command.name, command.ownerId);
  }
}
```

## Infrastructure Layer

### Repository Implementation

```typescript
// src/app/infrastructure/persistence/workspace-firestore.repository.ts
import { Injectable, inject } from '@angular/core';
import { Observable, from } from 'rxjs';
import { map } from 'rxjs/operators';
import { 
  Firestore, 
  collection, 
  doc, 
  getDoc, 
  setDoc, 
  query, 
  where, 
  getDocs 
} from '@angular/fire/firestore';
import { IWorkspaceRepository } from '@domain/repositories/workspace.repository';
import { Workspace } from '@domain/workspace/entities/workspace.entity';
import { WorkspaceId } from '@domain/workspace/value-objects/workspace-id.value-object';
import { WorkspaceName } from '@domain/workspace/value-objects/workspace-name.value-object';

@Injectable({ providedIn: 'root' })
export class WorkspaceFirestoreRepository implements IWorkspaceRepository {
  private firestore = inject(Firestore);
  private collectionRef = collection(this.firestore, 'workspaces');

  findById(id: WorkspaceId): Observable<Workspace | null> {
    const docRef = doc(this.collectionRef, id.value);
    return from(getDoc(docRef)).pipe(
      map(snapshot => {
        if (!snapshot.exists()) return null;
        return this.toDomain(snapshot.id, snapshot.data());
      })
    );
  }

  findByOwnerId(ownerId: string): Observable<Workspace[]> {
    const q = query(this.collectionRef, where('ownerId', '==', ownerId));
    return from(getDocs(q)).pipe(
      map(snapshot => snapshot.docs.map(doc => 
        this.toDomain(doc.id, doc.data())
      ))
    );
  }

  save(workspace: Workspace): Observable<Workspace> {
    const docRef = doc(this.collectionRef, workspace.id.value);
    const data = this.toFirestore(workspace);
    
    return from(setDoc(docRef, data)).pipe(
      map(() => workspace)
    );
  }

  delete(id: WorkspaceId): Observable<void> {
    const docRef = doc(this.collectionRef, id.value);
    return from(deleteDoc(docRef));
  }

  private toDomain(id: string, data: any): Workspace {
    return new Workspace({
      id: WorkspaceId.fromString(id),
      name: WorkspaceName.create(data.name),
      ownerId: data.ownerId,
      createdAt: data.createdAt?.toDate(),
      updatedAt: data.updatedAt?.toDate()
    });
  }

  private toFirestore(workspace: Workspace): any {
    return {
      name: workspace.name.value,
      ownerId: workspace.ownerId,
      createdAt: workspace.createdAt,
      updatedAt: new Date()
    };
  }
}
```

## Best Practices

### ✅ DO

- Keep domain layer pure (no framework dependencies)
- Use value objects for business concepts
- Encapsulate business rules in entities
- Raise domain events for state changes
- Define repository interfaces in domain
- Use aggregates for consistency boundaries
- Implement factories for complex object creation
- Use ubiquitous language consistently

### ❌ DON'T

- Put business logic in application or infrastructure
- Use anemic domain models (getters/setters only)
- Directly access database from domain
- Skip validation in value objects
- Expose entity internals via public setters
- Create circular dependencies between aggregates
- Mix infrastructure code with domain code

## Testing

### Domain Testing

```typescript
// workspace.entity.spec.ts
describe('Workspace Entity', () => {
  describe('create', () => {
    it('should create workspace with valid data', () => {
      const workspace = Workspace.create({
        name: 'Test Workspace',
        ownerId: 'user-123'
      });

      expect(workspace.name.value).toBe('Test Workspace');
      expect(workspace.ownerId).toBe('user-123');
      expect(workspace.domainEvents).toHaveLength(1);
      expect(workspace.domainEvents[0].eventType).toBe('WorkspaceCreated');
    });

    it('should throw error for invalid name', () => {
      expect(() => {
        Workspace.create({ name: '', ownerId: 'user-123' });
      }).toThrow('Workspace name cannot be empty');
    });
  });

  describe('rename', () => {
    it('should rename workspace and raise event', () => {
      const workspace = Workspace.create({
        name: 'Old Name',
        ownerId: 'user-123'
      });
      workspace.clearDomainEvents();

      workspace.rename('New Name');

      expect(workspace.name.value).toBe('New Name');
      expect(workspace.domainEvents).toHaveLength(1);
      expect(workspace.domainEvents[0].eventType).toBe('WorkspaceRenamed');
    });
  });
});
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Circular dependencies | Aggregates referencing each other | Use IDs instead of direct references |
| Domain depends on infrastructure | Import from wrong layer | Check imports, use interfaces |
| Anemic domain model | Business logic in services | Move logic to entities |
| Large aggregates | Too many entities in aggregate | Split into separate aggregates |
| Inconsistent state | Missing invariant validation | Add validation to entity methods |

## References

- [Domain-Driven Design by Eric Evans](https://www.domainlanguage.com/ddd/)
- [Implementing Domain-Driven Design by Vaughn Vernon](https://vaughnvernon.com/)
- [DDD Patterns](https://martinfowler.com/tags/domain%20driven%20design.html)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
