---
name: clean-code
description: |
  Write clean, readable, and maintainable code following principles from Robert C.
  Martin's "Clean Code" and Object Calisthenics. Use when writing, reviewing, or
  refactoring code to improve naming, function design, formatting, error handling,
  and class structure. Includes code smell detection and refactoring guidance.
---

# Clean Code

Principles for transforming "code that works" into "code that is clean" — code
that can be read, understood, and enhanced by any developer.

> "Code is clean if it can be understood easily — by everyone on the team." — Dave Thomas

## When to Apply

Reference these guidelines when:

- Writing new code and choosing names, function signatures, structure
- Reviewing pull requests for readability and maintainability
- Refactoring legacy code or reducing complexity
- Identifying and fixing code smells
- Improving team code standards

## Rule Categories

| Priority | Category | Impact |
| -------- | -------- | ------ |
| 1 | Naming | HIGH — affects every line of code |
| 2 | Functions | HIGH — core unit of abstraction |
| 3 | Code Smells | HIGH — early detection prevents rot |
| 4 | Formatting | MEDIUM — readability at a glance |
| 5 | Error Handling | MEDIUM — robustness and clarity |
| 6 | Comments | MEDIUM — most are avoidable |
| 7 | Object Calisthenics | ASPIRATIONAL — exercises for better OO design |

## 1. Naming

Good names are the single most impactful thing you can do for readability.

**Priority order:**

1. **Consistency** — same concept = same name everywhere
2. **Intent-revealing** — name says what it does, not how
3. **Specific** — avoid vague names like `data`, `info`, `manager`, `handler`, `utils`
4. **Searchable** — unique enough to grep
5. **Brief** — short but not cryptic

```typescript
// Bad
const d = new Date();
const arr = users.filter((u) => u.a);
function process(data: any) {}

// Good
const createdAt = new Date();
const activeUsers = users.filter((user) => user.isActive);
function validatePayment(payment: Payment) {}
```

**Conventions:**

- **Classes/types**: nouns (`Customer`, `OrderRepository`). Avoid `Manager`, `Data`, `Info`.
- **Methods/functions**: verbs (`createOrder`, `validateEmail`, `isEligible`)
- **Booleans**: question form (`isActive`, `hasPermission`, `canWithdraw`)
- **Collections**: plural nouns (`users`, `orderItems`)

See `references/NAMING.md` for full guidelines.

## 2. Functions

```typescript
// Bad — does too many things, unclear name
function handle(order: Order, sendEmail: boolean, log: boolean) {
  // validate, calculate, save, email, log — all in one
}

// Good — small, single-purpose, descriptive
function validateOrder(order: Order): ValidationResult { ... }
function calculateTotal(items: OrderItem[]): Money { ... }
function saveOrder(order: Order): Promise<void> { ... }
```

**Rules:**

- **Small** — strive for under 20 lines
- **Do one thing** — if you use "and" to describe it, split it
- **One level of abstraction** — don't mix business logic with low-level details
- **Few arguments** — 0-2 ideal, 3+ warrants a parameter object
- **No side effects** — or name them explicitly (`saveAndNotify`, not `save`)
- **Command/Query separation** — a function either does something or returns something, not both

## 3. Code Smells

Indicators that code may need refactoring. Not bugs, but design friction.

| Smell | Symptom | Quick Fix |
| ----- | ------- | --------- |
| **Long Method** | > 20 lines, multiple concerns | Extract methods |
| **Large Class** | Many responsibilities | Extract class (SRP) |
| **Long Parameter List** | > 3 parameters | Introduce parameter object |
| **Primitive Obsession** | Strings/numbers for domain concepts | Wrap in value objects |
| **Feature Envy** | Method uses another class's data more than its own | Move method |
| **Data Clumps** | Same group of fields appear together | Extract class |
| **Switch Statements** | Type-checking switch/if-else across codebase | Replace with polymorphism |
| **Divergent Change** | One class changed for many reasons | Split by responsibility |
| **Shotgun Surgery** | One change touches many files | Move related code together |
| **Speculative Generality** | "Just in case" abstractions | Delete (YAGNI) |
| **Dead Code** | Unreachable or unused code | Delete |
| **Message Chains** | `a.getB().getC().doSomething()` | Hide delegate (Law of Demeter) |

See `references/CODE_SMELLS.md` for detailed examples and refactoring strategies.

## 4. Formatting

**The Newspaper Metaphor** — code should read top-to-bottom like a newspaper
article. High-level summary at the top, details below.

```typescript
class OrderProcessor {
  // Public API first — the "headline"
  process(order: Order): ProcessResult {
    this.validate(order);
    const total = this.calculateTotal(order);
    return this.save(order, total);
  }

  // Supporting methods below, in order of appearance
  private validate(order: Order) { ... }
  private calculateTotal(order: Order): Money { ... }
  private save(order: Order, total: Money): ProcessResult { ... }
}
```

**Rules:**

- Related code stays close together (vertical density)
- Blank lines between concepts (vertical openness)
- Variables declared near their usage
- Caller above callee (stepdown rule)
- Consistent indentation — non-negotiable

## 5. Error Handling

- **Exceptions over error codes** — keeps happy path clean
- **Don't return `null`** — use `undefined`, `Result` types, or throw
- **Don't pass `null`** — leads to defensive checks everywhere
- **Fail fast** — validate at boundaries, trust internals
- **Specific exceptions** — `InsufficientFundsError` over generic `Error`

```typescript
// Bad — null checks cascade through codebase
function getUser(id: string): User | null {
  return db.find(id);
}
const user = getUser(id);
if (user === null) { ... } // Every caller must check

// Good — throw at boundary, trust within domain
function getUser(id: string): User {
  const user = db.find(id);
  if (!user) throw new UserNotFoundError(id);
  return user;
}
```

## 6. Comments

> "Don't comment bad code — rewrite it."

Most comments compensate for failure to express intent in code. Prefer
self-documenting code over comments.

**Good comments:**

- **Why** something is done (business reason, non-obvious decision)
- **Warnings** ("this is slow because X", "order matters here")
- **TODOs** with context (link to issue)
- **Legal/license** headers
- **Public API docs** (JSDoc for libraries)

**Bad comments:**

- Restating what the code does (`// increment counter`)
- Commented-out code (that's what git is for)
- Journal/changelog comments
- Noise (`// constructor`, `// getters`)
- Mandated boilerplate

```typescript
// Bad — restates the obvious
// Check if user is active
if (user.isActive) { ... }

// Good — explains a non-obvious business rule
// Users who haven't verified email within 30 days are auto-deactivated
// per compliance requirement GDPR-2024-42
if (user.isAutoDeactivated) { ... }
```

## 7. Object Calisthenics

Nine exercises from Jeff Bay to improve OO design. Treat these as aspirational
targets — strict during practice, pragmatic in production.

| # | Rule | Goal |
| - | ---- | ---- |
| 1 | One level of indentation per method | Extract methods aggressively |
| 2 | Don't use `else` | Early returns, guard clauses, polymorphism |
| 3 | Wrap all primitives with domain meaning | Value objects (`Email`, `Money`, `UserId`) |
| 4 | First-class collections | Wrap arrays in domain-specific classes |
| 5 | One dot per line | Law of Demeter — talk to friends only |
| 6 | Don't abbreviate | If the name is too long, the class does too much |
| 7 | Keep entities small | Classes < 50 lines, methods < 10 lines |
| 8 | Limit instance variables | Strive for 2-3; forces focused classes |
| 9 | No getters/setters | Objects have behavior, not just data |

See `references/OBJECT_CALISTHENICS.md` for examples of each rule.

## Implementation Checklist

Before submitting code:

- [ ] Can a new team member understand this without asking questions?
- [ ] Are names intention-revealing and consistent?
- [ ] Does each function do exactly one thing?
- [ ] Are there any code smells I can fix while I'm here?
- [ ] Are comments explaining *why*, not *what*?
- [ ] Is error handling clean and specific?
- [ ] Did I leave the code better than I found it? (Boy Scout Rule)
