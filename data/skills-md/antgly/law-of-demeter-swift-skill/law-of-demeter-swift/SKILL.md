---
name: law-of-demeter-swift
description: Use when reviewing, generating, or refactoring Swift code to aggressively detect Law of Demeter violations (deep reach-through chains, leaked structure, async traversal chains) and propose Swift-idiomatic owner-level APIs.
---

# Law of Demeter for Swift (Strict Review Mode)

## Purpose

Enforce **Law of Demeter (LoD)** in Swift code with a **strict-by-default** review posture:

- Flag deep structural access (`a.b.c`, `a?.b?.c`)
- Flag chained domain lookups across model/service boundaries
- Flag async/actor traversal chains after `await`
- Prefer **owner-level, intent-focused APIs**
- Preserve **Swift API naming style** (no Java-style `getX()` suggestions)

> **Core rule:** Ask for what you need. Do not traverse internal structure to reach strangers.

---

## Strict Review Mode (Default Behavior)

In this strict version, **assume a likely LoD violation** when all of the following are true:

1. The code is in **domain/app/business logic** (not a boundary adapter or fluent DSL)
2. A caller traverses **2+ domain hops** to obtain a value or trigger behavior
3. The traversal exposes another type’s internal structure or storage shape
4. The caller could reasonably ask an owning type/service for the same result

### Examples that should be flagged in strict mode

- `company.employee(for: id)?.address.city`
- `order.customer.paymentMethod.last4`
- `session.user.profile.preferences.theme`
- `try await accountService.currentAccount().owner.notificationSettings.marketingEmailsEnabled`

---

## What Counts as a “Stranger” (Swift Edition)

Inside a method or computed property body, **safe collaborators** are generally:

- `self`
- parameters
- locals created in the method
- direct stored properties / direct collaborators

A likely LoD violation occurs when code reaches **through** one of those collaborators to a nested collaborator that the caller does not own.

### Ask yourself

- Am I using a direct collaborator?
- Or am I using a collaborator **only as a path** to reach a stranger?

---

## Swift-Specific Requirements (Naming + Design)

### 1) Preserve Swift API style at the call site

When proposing a refactor:

- cheap read-only data → **property**
  - `employee.city`
  - `order.paymentLast4`
- action / async / throws / work → **method**
  - `company.city(for:)`
  - `accountService.marketingEmailsEnabled()`

**Do not** suggest Java-style names like:

- `getCity()`
- `getPostalCode()`
- `getMarketingEmailsEnabled()`

### 2) Dot count is a trigger, not proof

A long chain is a **signal**. In strict mode, review it, then classify it:

- **Structural reach-through** → flag
- **Intentional fluent API / stdlib pipeline** → usually allow

### 3) Concurrency does not exempt LoD

Swift async/await and actor code is still subject to LoD.
If `await` is followed by traversal through returned internals, treat it as a likely design smell.

---

## Aggressive Detection Heuristics (Use in Reviews)

Flag or strongly scrutinize code matching these patterns:

### Pattern A: Deep property traversal

- `a.b.c`
- `a.b.c.d`
- `a?.b?.c`
- `a?.b?.c?.d`

### Pattern B: Domain call + traversal

- `service.fetchX().y.z`
- `repo.load().nested.value`
- `store.state.user.profile`

### Pattern C: Async call + traversal (high-priority smell)

- `try await service.currentSession().user.profile.preferences`
- `await actor.snapshot().nested.value`

### Pattern D: Temporary drilling variables

```swift
let profile = user.profile
let address = profile.address
return address.postalCode
```

### Pattern E: Repeated chain access across files

If the same chain or a similar chain appears in multiple locations, escalate severity and suggest centralizing the API.

---

## Review Severity Levels (Strict)

Use these levels when reporting:

**Domain hop definition:** Count domain hops as the number of transitions (dots) between domain segments.  
For example, `order.customer.address.city` has 3 domain hops (`order → customer → address → city`).  
Treat 2+ domain hops as a likely LoD violation; the severity depends on context as described below.

### High severity
- Async/actor traversal chain after `await`
- 2+ domain hops in app/business logic
- Public API exposing nested structure
- Repeated chain smell in multiple call sites

### Medium severity
- 2-hop domain traversal in internal code
- UI/view model reaches into nested domain types
- Tests needing deep stubs because of traversal

### Low severity / review note
- Borderline chain in boundary mapping code
- One-off read in local adapter code (still worth watching)

---

## What Not to Flag (False-Positive Guardrails)

Even in strict mode, **do not auto-flag** these unless they also expose domain internals improperly:

### 1) Standard library pipelines

```swift
let ids = orders
    .filter(\.isOpen)
    .map(\.id)
    .sorted()
```

### 2) Common string/value transformations

```swift
let normalized = input
    .trimmingCharacters(in: .whitespacesAndNewlines)
    .lowercased()
```

### 3) Intentional fluent APIs / builders / DSLs

If chaining is the designed public abstraction, it may be fine.

### 4) DTO/adapter mapping code at boundaries

Some structural traversal is expected when decoding / mapping external data.
Keep it localized and do not leak it throughout the app.

> In strict mode, boundary code is **reviewed**, not automatically exempted.

---

## Refactoring Strategy (Strict, Minimal, Swift-Idiomatic)

When you flag a violation, propose the **smallest safe refactor** that improves design.

### Preferred order of fixes

1. **Add forwarding property** (cheap, stable data)
2. **Add owner-level method** (query/action/async/throws)
3. **Move behavior to owner**
4. **Add façade/protocol** (especially across module boundaries)
5. **Collapse async traversal behind actor/service API**

### Do this first (minimal change path)

- Add a property or method on the most appropriate owner
- Replace the call site chain
- Keep behavior unchanged
- Keep names Swift-idiomatic

---

## Canonical Examples (Strict Mode)

### ❌ Flag: caller traverses nested structure

```swift
import Foundation

struct Address {
    let city: String
    let postalCode: String
}

struct Employee {
    let id: UUID
    let address: Address
}

final class Company {
    private let employeesByID: [UUID: Employee]

    init(employeesByID: [UUID: Employee]) {
        self.employeesByID = employeesByID
    }

    func employee(for employeeID: UUID) -> Employee? {
        employeesByID[employeeID]
    }
}

let postalCode = company.employee(for: employeeID)?.address.postalCode
```

### ✅ Prefer: owner-level query

```swift
import Foundation

struct Address {
    let city: String
    let postalCode: String
}

struct Employee {
    let id: UUID
    private let address: Address

    var city: String { address.city }
    var postalCode: String { address.postalCode }
}

final class Company {
    private let employeesByID: [UUID: Employee]

    init(employeesByID: [UUID: Employee]) {
        self.employeesByID = employeesByID
    }

    func postalCode(for employeeID: UUID) -> String? {
        employeesByID[employeeID]?.postalCode
    }

    func city(for employeeID: UUID) -> String? {
        employeesByID[employeeID]?.city
    }
}

let postalCode = company.postalCode(for: employeeID)
```

---

## Swift Concurrency Example (Strict)

### ❌ High severity: async traversal chain

```swift
let marketingEmailsEnabled = try await accountService
    .currentAccount()
    .owner
    .notificationSettings
    .marketingEmailsEnabled
```

Why this is high severity:

- `await` boundary + structural traversal
- Caller learns internal account/owner/settings layout
- Refactors spread across many call sites

### ✅ Prefer: intent-focused actor/service API

```swift
let marketingEmailsEnabled = try await accountService.marketingEmailsEnabled()
```

### ✅ Possible implementation

```swift
actor AccountService {
    private var account: Account?

    func marketingEmailsEnabled() throws -> Bool {
        guard let account else { throw AccountError.notLoaded }
        return account.marketingEmailsEnabled
    }
}

enum AccountError: Error {
    case notLoaded
}

struct Account {
    private let owner: User

    var marketingEmailsEnabled: Bool {
        owner.marketingEmailsEnabled
    }
}

struct User {
    private let notificationSettings: NotificationSettings

    var marketingEmailsEnabled: Bool {
        notificationSettings.marketingEmailsEnabled
    }
}

struct NotificationSettings {
    let marketingEmailsEnabled: Bool
}
```

---

## Copilot/Codex Review Instructions (Strict Output Format)

When reviewing code, use this response pattern for each likely violation:

### 1) Identify the chain
- Quote the exact chain
- Name the owner and the stranger(s)

### 2) Explain the coupling
- What internal structure is leaked?
- Why will refactors be harder?
- Why is this especially risky if async/actor-based?

### 3) Propose a Swift-idiomatic replacement
- Prefer property for cheap data
- Prefer method for async/throws/work
- Avoid `getX()` naming

### 4) Show a minimal patch direction
- Add owner-level property/method
- Replace call site
- Preserve behavior

### 5) Classify severity
- High / Medium / Low (with a one-line reason)

---

## Review Comment Templates (Strict)

### Template: medium severity (sync chain)
- **LoD concern (medium):** `company.employee(for: id)?.address.city` reaches through `Employee` into `Address`, which leaks internal structure to the caller. Consider adding `company.city(for:)` (or `Employee.city` if that’s the right ownership boundary) and calling that instead.

### Template: high severity (async/actor chain)
- **LoD concern (high):** `try await accountService.currentAccount().owner.notificationSettings.marketingEmailsEnabled` crosses an async boundary and then traverses nested internals. This tightly couples callers to `Account`/`User`/`NotificationSettings` layout. Prefer an intent-level API such as `try await accountService.marketingEmailsEnabled()`.

### Template: naming reminder
- **Swift API naming:** If you add a replacement API, prefer Swift-style names (`city`, `city(for:)`, `marketingEmailsEnabled()`) rather than Java-style `getCity()` / `getMarketingEmailsEnabled()`.

---

## Quick Decision Rules (Strict)

### Flag immediately if
- 2+ domain hops (`a.b.c` in business logic)
- async/await + traversal (`await x().y.z`)
- public API returns structure only to force traversal by callers
- repeated chain smells in multiple files

### Usually allow if
- stdlib pipeline chain
- string/value fluent transformations
- builder/DSL chain
- localized DTO mapping code at a boundary

### If unsure
Treat as **review note** and ask:
- “Can this caller ask an owner for intent-level data instead?”

---

## Anti-Regression Guidance

After refactoring one LoD violation, look for siblings:

- Same chain in other files
- Similar chains on the same type
- Tests that still mock deep internals
- Public APIs that encourage traversal

If found, propose a small follow-up refactor to centralize the new owner-level API.

---

## Bottom Line

**Strict mode favors maintainability over convenience.**

In Swift code, especially with actors and async services, prefer APIs that:

- express **intent**
- hide **structure**
- preserve **Swift naming conventions**
- reduce refactor blast radius
- keep call sites simple and resilient
