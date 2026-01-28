---
name: spec-driven-development
description: Implement the complete spec-driven development workflow from instructions through requirements, design, and implementation planning. Use this skill when starting new features or major refactorings that benefit from structured planning before coding.
---

# Spec-Driven Development

A rigorous six-phase workflow that captures requirements, designs solutions, defines behavioral contracts through tests, and plans implementations before writing code. This approach ensures alignment, reduces rework, and creates living documentation.

## Critical Rule

**NEVER IMPLEMENT WITHOUT AUTHORIZATION**

After completing each phase, you MUST:
1. Present the completed work
2. Explicitly ask for user approval
3. Wait for clear confirmation
4. NEVER proceed automatically to the next phase

This is not optional. Each phase requires explicit user authorization.

## When to Use This Skill

Use spec-driven development for:
- **New features**: Any non-trivial feature requiring design decisions
- **Major refactorings**: Architectural changes affecting multiple components
- **API design**: Public interfaces that need careful consideration
- **Complex bugs**: Issues requiring investigation and design changes
- **Team coordination**: Work requiring clear communication and approval

Skip this process for:
- Trivial bug fixes (typos, simple logic errors)
- Documentation updates
- Configuration tweaks
- Minor refactorings with clear solutions

## Directory Structure

```
specs/
 README.md                      # Feature directory listing
 [feature-name]/
     instructions.md            # Phase 1: Raw requirements
     requirements.md            # Phase 2: Structured requirements
     design.md                  # Phase 3: Technical design
     behaviors.test.ts          # Phase 4: Behavioral tests (executable specs)
     plan.md                    # Phase 5: Implementation plan
```

The `specs/README.md` maintains a simple checkbox list of all features:

```markdown
# Feature Specifications

- [x] **[payment-intents](./payment-intents/)** - Payment intent workflow
- [ ] **[user-authentication](./user-authentication/)** - User auth system
- [ ] **[data-sync](./data-sync/)** - Real-time data synchronization
```

## Six-Phase Workflow

### Phase 1: Capture Instructions

**Goal**: Document raw user requirements without interpretation.

**Create**: `specs/[feature-name]/instructions.md`

**Contents**:
- Raw user requirements (exactly as provided)
- User stories ("As a [role], I want [feature] so that [benefit]")
- Acceptance criteria (what defines success)
- Constraints and dependencies
- Out of scope items (what this does NOT include)

**Template**:

```markdown
# [Feature Name] - Instructions

## Overview

[Brief description of what the user wants]

## User Stories

- As a [role], I want [feature] so that [benefit]
- As a [role], I want [feature] so that [benefit]

## Acceptance Criteria

- [ ] [Concrete, testable criterion]
- [ ] [Concrete, testable criterion]

## Constraints

- [Technical constraint]
- [Business constraint]
- [Timeline constraint]

## Dependencies

- [Existing feature or system]
- [External service]

## Out of Scope

- [What this feature does NOT include]
```

**After completion**:
1. Add entry to `specs/README.md`
2. Present instructions to user
3. Ask: "Does this accurately capture your requirements? Should I proceed to Phase 2 (Requirements)?"
4. **STOP and wait for approval**

---

### Phase 2: Derive Requirements

**REQUIRES APPROVAL FROM PHASE 1**

**Goal**: Transform raw instructions into structured, technical requirements.

**Create**: `specs/[feature-name]/requirements.md`

**Contents**:
- Functional requirements (what the system must do)
- Non-functional requirements (performance, security, scalability)
- Technical constraints (libraries, patterns, compatibility)
- Dependencies on other features or systems
- Data requirements (schemas, storage, validation)
- Error handling requirements

**Template**:

```markdown
# [Feature Name] - Requirements

## Functional Requirements

### FR-1: [Requirement Name]
**Priority**: High | Medium | Low
**Description**: [What must happen]
**Acceptance**: [How to verify]

### FR-2: [Requirement Name]
**Priority**: High | Medium | Low
**Description**: [What must happen]
**Acceptance**: [How to verify]

## Non-Functional Requirements

### NFR-1: Performance
- [Specific metric, e.g., "Response time < 100ms"]
- [Throughput requirement]

### NFR-2: Security
- [Authentication requirement]
- [Authorization requirement]

### NFR-3: Scalability
- [Concurrent users]
- [Data volume]

## Technical Constraints

- Must use [specific library or pattern]
- Must integrate with [existing system]
- Must support [platform or environment]

## Dependencies

### Internal
- [Feature or service name]: [Why needed]

### External
- [Library or API]: [Why needed]

## Data Requirements

### Schema
```typescript
export interface DataModel {
  readonly id: string
  readonly name: string
  readonly value: number
  readonly createdAt: Date
}
```

### Validation
- [Field-level validation rules]
- [Cross-field validation rules]

### Storage
- [Where data is stored]
- [Persistence strategy]

## Error Handling

- [Error scenario 1]: [Required handling]
- [Error scenario 2]: [Required handling]

## Traceability

- Addresses instructions: [Section references]
```

**Ask Questions**: Use `AskUserQuestion` tool if:
- Requirements are ambiguous or unclear
- Multiple valid approaches exist
- Trade-offs need user input
- Domain knowledge is missing
- Priority conflicts arise

**After completion**:
1. Present requirements to user
2. Ask: "Do these requirements accurately reflect the system needs? Should I proceed to Phase 3 (Design)?"
3. **STOP and wait for approval**

---

### Phase 3: Create Design

**REQUIRES APPROVAL FROM PHASE 2**

**Goal**: Make architectural decisions and design the solution.

**Create**: `specs/[feature-name]/design.md`

**Contents**:
- Architecture decisions (patterns, structure)
- API design (functions, types, interfaces)
- Data models (schemas with Effect Schema)
- Effect patterns to use (services, layers, streams)
- Error handling strategy (error types, recovery)
- Testing strategy (unit, integration, property tests)

**Template**:

```markdown
# [Feature Name] - Design

## Architecture Overview

[High-level description of the solution]

Data flow: `ComponentA → ComponentB → ComponentC` (use `→` for dependencies, `||` for parallel)

## Architecture Decisions

### AD-1: [Decision Name]
**Context**: [Why this decision is needed]
**Decision**: [What was decided]
**Rationale**: [Why this approach]
**Alternatives**: [What was considered but rejected]
**Consequences**: [Implications of this decision]

### AD-2: [Decision Name]
[Same structure]

## API Design

### Public Interface

```typescript
import { Effect, Context } from "effect"

// Declare types used in examples
declare const Input1: unique symbol
declare const Output1: unique symbol
declare const Error1: unique symbol
declare const Deps1: unique symbol
declare const Input2: unique symbol
declare const Output2: unique symbol
declare const Error2: unique symbol
declare const Deps2: unique symbol

export interface FeatureService {
  readonly operation1: (input: typeof Input1) => Effect.Effect<typeof Output1, typeof Error1, typeof Deps1>
  readonly operation2: (input: typeof Input2) => Effect.Effect<typeof Output2, typeof Error2, typeof Deps2>
}
```

### Type Definitions

```typescript
import { Data } from "effect"

// Domain types
export interface DomainType {
  readonly field1: string
  readonly field2: number
}

// Error types
export class FeatureError extends Data.TaggedError("FeatureError")<{
  readonly reason: string
}> {}
```

## Data Models

### Schemas

```typescript
import { Schema } from "effect"

export const InputSchema = Schema.Struct({
  field1: Schema.String,
  field2: Schema.Number
})

export interface Input extends Schema.Schema.Type<typeof InputSchema> {}
```

### Validation Rules

- **field1**: Must be non-empty, max 100 characters
- **field2**: Must be positive integer

## Effect Patterns

### Services

- **FeatureService**: Main service providing feature operations
- **RepositoryService**: Data access layer
- **ValidationService**: Input validation

### Layers

```typescript
// Layer dependencies: FeatureServiceLive → {RepositoryServiceLive → DatabaseLive, ValidationServiceLive → ConfigLive}
```

### Error Handling

```typescript
import { Effect, Data } from "effect"

// Declare error types
declare class ValidationError extends Data.TaggedError("ValidationError")<{
  readonly message: string
}> {}

declare class DatabaseError extends Data.TaggedError("DatabaseError")<{
  readonly message: string
}> {}

declare class BusinessRuleError extends Data.TaggedError("BusinessRuleError")<{
  readonly message: string
}> {}

// Error hierarchy
export type FeatureError =
  | ValidationError
  | DatabaseError
  | BusinessRuleError

// Recovery strategy example
declare const operation: Effect.Effect<string, FeatureError, never>

const recovered = operation.pipe(
  Effect.catchTags({
    ValidationError: (_e: ValidationError) => Effect.succeed("retry with corrected input"),
    DatabaseError: (_e: DatabaseError) => Effect.succeed("fallback to cache"),
    BusinessRuleError: (_e: BusinessRuleError) => Effect.succeed("notify user")
  })
)
```

### Streams (if applicable)

```typescript
import { Stream } from "effect"

// Declare types
declare const Update: unique symbol
declare type Update = typeof Update
declare const CustomError: unique symbol
declare type CustomError = typeof CustomError
declare const Deps: unique symbol
declare type Deps = typeof Deps

declare const source: EventSource
declare function parse(event: MessageEvent): Update
declare function validate(update: Update): boolean

// Real-time updates
const updates: Stream.Stream<Update, CustomError, Deps> =
  Stream.fromEventSource(source).pipe(
    Stream.map(parse),
    Stream.filter(validate)
  )
```

## Component Structure

Structure files for parallel implementation: one file = one task, interface separate from implementation.

**File mapping by phase**:
- P1 (interfaces): `{Schema.ts, Error.ts, Service.ts, Repository.ts}`
- P2 (implementations): `{ServiceLive.ts, RepositoryLive.ts, Validation.ts}`
- P3 (tests): `{Service.test.ts, Repository.test.ts, Validation.test.ts}`

Execution: `P1 ; P2 ; P3` — interfaces first enables parallel implementation against stable types.

### Dependencies

```typescript
// Internal
import type { DatabaseService } from "../database"
import type { LoggerService } from "../logger"

// External
import { Schema, Effect, Layer, Stream } from "effect"
```

## Testing Strategy

### Unit Tests
- Test each service method in isolation
- Use test layers for dependencies
- Property-based testing for validation

### Integration Tests
- Test service with real database (test instance)
- Test error scenarios
- Test stream behavior

### Test Structure

```typescript
import { Effect, Layer, Context } from "effect"
import { describe, it, expect } from "vitest"

// Declare service interface
interface FeatureService {
  readonly operation: (input: string) => Effect.Effect<string, never, never>
}

const FeatureService = Context.GenericTag<FeatureService>("FeatureService")

// Declare layers
declare const FeatureServiceLive: Layer.Layer<FeatureService, never, DatabaseService | ConfigService>
declare const DatabaseTest: Layer.Layer<DatabaseService, never, never>
declare const ConfigTest: Layer.Layer<ConfigService, never, never>

// Declare types
declare const DatabaseService: Context.Tag<DatabaseService, {}>
declare const ConfigService: Context.Tag<ConfigService, {}>
declare const validInput: string
declare const expectedOutput: string

describe("FeatureService", () => {
  const TestLive = FeatureServiceLive.pipe(
    Layer.provide(DatabaseTest),
    Layer.provide(ConfigTest)
  )

  it("should handle valid input", () =>
    Effect.gen(function* () {
      const service = yield* FeatureService
      const result = yield* service.operation(validInput)
      expect(result).toEqual(expectedOutput)
    }).pipe(Effect.provide(TestLive), Effect.runPromise)
  )
})
```

## Performance Considerations

- [Caching strategy]
- [Batch operations]
- [Resource pooling]

## Security Considerations

- [Authentication checks]
- [Authorization rules]
- [Data sanitization]

## Traceability

- Addresses requirements: [FR-1, FR-2, NFR-1, etc.]
- Implements instructions: [Section references]
```

**Ask Questions**: Use `AskUserQuestion` for:
- Architecture choices (monolithic vs modular)
- Technology selections (which libraries)
- Error handling approaches
- Performance trade-offs
- Security requirements

**After completion**:
1. Present design to user
2. Ask: "Does this design meet your expectations? Should I proceed to Phase 4 (Behavioral Tests)?"
3. **STOP and wait for approval**

---

### Phase 4: Define Behavioral Tests

**REQUIRES APPROVAL FROM PHASE 3**

**Goal**: Write tests that serve as executable specifications of expected behavior.

**Create**: `specs/[feature-name]/behaviors.test.ts`

**Philosophy**:
Tests are behavioral interfaces. They define the API surface and expected behaviors more precisely than prose. Unlike text descriptions, tests:
- Are executable specifications that can be incrementally implemented
- Define the exact API surface users will interact with
- Force concrete thinking about inputs, outputs, and edge cases
- Become passing tests as implementation progresses
- Serve as permanent, verifiable documentation

**Important**: These tests are NOT expected to run or type-check initially. They are written to define behavior, not to pass. Use `declare` statements for types/services that don't exist yet, and `Layer.mock` for partial layer implementations. The focus is clarity of intent, not correctness of implementation.

**Contents**:
- Happy path tests for each major operation
- Error scenario tests (what errors should occur when)
- Edge case tests (boundaries, empty inputs, limits)
- Integration behavior tests (how components interact)

**Guidelines**:

1. **Use `declare`** for all types, services, and layers that don't exist yet
2. **Use `Layer.mock`** for incremental test layer implementation:
   - `Layer.mock(Tag, { method: impl })` creates a type-safe partial implementation
   - Only implement the methods needed for current tests
   - Unimplemented methods throw "not implemented" errors at runtime
   - Add method implementations incrementally as you write more tests
   - This enables layer creation using partials without type errors
3. **Focus on behavior, not implementation** - describe what should happen, not how
4. **Cover the essential paths**:
   - Happy path (normal successful operation)
   - Validation failures (bad input)
   - Business rule violations (constraints, conflicts)
   - Not found scenarios
   - Edge cases specific to the domain
5. **Keep tests readable** - they serve as documentation for future implementers
6. **Don't over-specify** - test observable behavior, not internal details

**Ask Questions**: Use `AskUserQuestion` if:
- Expected behavior for edge cases is unclear
- Error handling semantics need clarification
- There are multiple valid ways to handle a scenario
- Business rules need user input

**After completion**:
1. Present behavioral tests to user
2. Ask: "Do these tests accurately capture the expected behaviors? Should I proceed to Phase 5 (Plan)?"
3. **STOP and wait for approval**

---

### Phase 5: Generate Plan

**REQUIRES APPROVAL FROM PHASE 4**

**Goal**: Break down implementation into concrete, ordered tasks optimized for parallel agent execution.

**Create**: `specs/[feature-name]/plan.md`

**Critical: Parallel Decomposition**

Tasks must be structured for concurrent agent execution. Use standard notation:
- `A || B` — A and B execute in parallel (no file overlap)
- `A ; B` — A completes before B starts (dependency)
- `{T1, T2, T3}` — task set (all parallel within set)

**Execution model**: `Phase1 ; Phase2 ; Phase3` where each phase is `{T1 || T2 || ... || Tn}`

**Constraints**:
- File isolation: `∀ Ti, Tj ∈ Phase: files(Ti) ∩ files(Tj) = ∅`
- Interface-first: Phase 1 defines interfaces, Phase 2+ implements against them
- One file = one task (split further if task spans multiple files)
- Target |Phase| ≥ 5 tasks for maximum parallelism

**Contents**: Task sets per phase, file ownership per task, phase dependencies, validation commands

**Template**:

```markdown
# [Feature Name] - Implementation Plan

## Execution Structure

P1 ; P2 ; P3 (sequential phases, parallel tasks within each)

## Phase 1: Interfaces {T1.1 || T1.2 || T1.3 || T1.4}

- T1.1: `FeatureSchema.ts` — domain types
- T1.2: `FeatureError.ts` — error types
- T1.3: `FeatureService.ts` — service interface + Tag
- T1.4: `FeatureRepository.ts` — repository interface + Tag

Gate: typechecks pass (DELEGATE to agent)

## Phase 2: Implementations {T2.1 || T2.2 || T2.3}

- T2.1: `FeatureRepositoryLive.ts` — implements FeatureRepository
- T2.2: `FeatureServiceLive.ts` — implements FeatureService
- T2.3: `FeatureValidation.ts` — validation functions

Gate: typechecks pass (DELEGATE to agent)

## Phase 3: Tests {T3.1 || T3.2 || T3.3}

- T3.1: `FeatureRepository.test.ts`
- T3.2: `FeatureService.test.ts`
- T3.3: `FeatureValidation.test.ts`

Gate: tests pass (DELEGATE to agent)
```

**After completion**:
1. Present plan to user
2. Ask: "Does this implementation plan look correct? Should I proceed to Phase 6 (Implementation)?"
3. **STOP and wait for approval**

---

### Phase 6: Execute Implementation

**REQUIRES APPROVAL FROM PHASE 5**

**Goal**: Implement the solution exactly as planned.

**No new files**: Implementation follows the plan exactly.

**Process**:
1. Execute tasks per phase following the plan
2. After each file: format, typecheck, fix errors
3. After each phase: run tests
4. Update plan.md progress markers

**Quality gates**: Gates (typecheck, test) SHALL be delegated to agents — do not run directly from orchestrating agent.

**Legal review**: For significant changes (multiple files, architectural impact), perform `/legal-review` before finalizing implementation.

**After completion**:
1. Present implementation summary
2. Show test results
3. Highlight any deviations from plan (with justification)
4. Ask: "Implementation complete. Would you like me to create a PR or make any changes?"

---

## Approval Checkpoints

Each phase requires explicit user approval before proceeding:

- 1→2: "Does this capture your requirements? Proceed to Requirements?"
- 2→3: "Do these requirements reflect system needs? Proceed to Design?"
- 3→4: "Does this design meet expectations? Proceed to Behavioral Tests?"
- 4→5: "Do these tests capture expected behaviors? Proceed to Plan?"
- 5→6: "Is this plan correct? Proceed to Implementation?"
- 6→✓: "Implementation complete. Create PR or make changes?"

Never skip checkpoints—changes cascade through dependent phases.

## When to Ask Questions

Use the `AskUserQuestion` tool liberally throughout:

### Phase 1 (Instructions)
- Clarify ambiguous requirements
- Resolve conflicting user stories
- Understand domain terminology
- Identify edge cases

### Phase 2 (Requirements)
- Prioritize requirements
- Resolve technical constraints
- Choose between valid approaches
- Define success metrics

### Phase 3 (Design)
- Select architecture patterns
- Choose libraries or frameworks
- Decide error handling strategies
- Resolve performance trade-offs

### Phase 4 (Behavioral Tests)
- Clarify expected behavior for edge cases
- Determine error handling semantics
- Resolve ambiguous business rules
- Define success/failure criteria

### Phase 5 (Plan)
- Identify parallelization opportunities
- Resolve file ownership conflicts between tasks
- Sequence only truly dependent phases
- Identify risks
- Plan contingencies

### Phase 6 (Implementation)
- Handle unexpected issues
- Adjust for missing dependencies
- Resolve test failures
- Document deviations

**Question Quality**:
- Provide context for why you're asking
- Offer 2-4 concrete options
- Explain trade-offs of each option
- Recommend a default choice

Example:
```typescript
// Example of tool call structure (not executable TypeScript)
declare function AskUserQuestion(params: {
  questions: Array<{
    question: string
    header: string
    multiSelect: boolean
    options: Array<{
      label: string
      description: string
    }>
  }>
}): void

// Usage:
AskUserQuestion({
  questions: [{
    question: "How should we handle concurrent updates to the counter?",
    header: "Concurrency",
    multiSelect: false,
    options: [
      {
        label: "Last-write-wins",
        description: "Simple but may lose updates under high concurrency"
      },
      {
        label: "Optimistic locking",
        description: "Retry on conflict, guarantees no lost updates"
      },
      {
        label: "CRDT merge",
        description: "Automatic conflict resolution, complex but robust"
      }
    ]
  }]
})
```

## Quality Standards

Each specification document must:

### Clarity
- Use precise, unambiguous language
- Define all domain terms
- Include concrete examples
- Avoid vague words ("should", "might", "probably")

### Completeness
- Address all user requirements
- Cover error scenarios
- Document edge cases
- Include success criteria

### Traceability
- Link back to previous phases
- Reference source requirements
- Map to implementation tasks
- Enable impact analysis

### Effect Alignment
- Use Effect patterns (services, layers, streams)
- Leverage Effect error handling
- Design for composition
- Follow Effect best practices

### Testability
- Define measurable acceptance criteria
- Specify test scenarios
- Include performance benchmarks
- Enable automated validation

### Documentation
- Add inline code examples
- Include usage scenarios
- Document design rationale
- Explain trade-offs

## Common Pitfalls

### Skipping Phases
**Don't**: Jump straight to implementation
**Do**: Follow all six phases in order

### Assuming Requirements
**Don't**: Fill in gaps with assumptions
**Do**: Ask questions using `AskUserQuestion`

### Over-designing
**Don't**: Design for hypothetical future requirements
**Do**: Design for stated requirements with room to extend

### Under-planning
**Don't**: Create vague tasks like "implement feature"
**Do**: Break into concrete, testable subtasks

### Poor Parallelization
**Don't**: Create tasks that touch overlapping files
**Do**: Structure tasks so each owns distinct files, enabling 5+ parallel agents

### Sequential When Parallel Is Possible
**Don't**: Chain tasks that could run concurrently (Task 2 depends on Task 1 when they touch different files)
**Do**: Group truly independent tasks into phases that execute in parallel

### Ignoring Feedback
**Don't**: Proceed when user requests changes
**Do**: Update specs and get re-approval

### Poor Traceability
**Don't**: Lose connection between phases
**Do**: Explicitly reference previous phase decisions

## Integration with Other Skills

Spec-driven development works with:

- **domain-modeling**: Use when designing domain types in Phase 3
- **service-implementation**: Apply during Phase 6 implementation
- **layer-design**: Reference when creating layers in Phase 3
- **typeclass-design**: Use for generic abstractions in Phase 3
- **effect-testing**: Apply test patterns in Phase 4 (behavioral tests) and Phase 6 (implementation)

## Examples

### Small Feature: Add Logging
- Phase 1: "Add debug logging to payment flow"
- Phase 2: Log levels, what to log, PII handling
- Phase 3: Logger service design, Effect integration
- Phase 4: Tests for log output, error scenarios
- Phase 5: Update files, add logger calls
- Phase 6: Implement, verify logs appear and tests pass

### Medium Feature: User Authentication
- Phase 1: Login, registration, password reset stories
- Phase 2: Security requirements, session management
- Phase 3: Service design, token strategy, error types
- Phase 4: Tests for login flows, token validation, error cases
- Phase 5: Multi-phase plan (auth service, session, middleware)
- Phase 6: Implement all components, make tests pass

### Large Feature: Real-time Sync
- Phase 1: Sync requirements across devices
- Phase 2: Conflict resolution, consistency guarantees
- Phase 3: CRDT design, stream architecture, error recovery
- Phase 4: Tests for conflict scenarios, sync behaviors, edge cases
- Phase 5: Phased rollout (local, network, UI integration)
- Phase 6: Iterative implementation with progress updates

## Success Criteria

A successful spec-driven development cycle:

1. **Alignment**: Final implementation matches original user intent
2. **Quality**: All behavioral tests pass, code follows patterns
3. **Documentation**: Specs accurately describe implementation
4. **Traceability**: Clear path from instructions to code
5. **Maintainability**: Future developers understand design rationale
6. **Confidence**: User approved at each phase checkpoint
7. **Executable Specs**: Behavioral tests serve as living documentation that verifies behavior

Remember: The goal is not perfect specs, but **shared understanding** and **documented decisions** that guide implementation and enable future maintenance. Behavioral tests bridge the gap between prose documentation and running code—they start as specifications and end as verified behavior.
