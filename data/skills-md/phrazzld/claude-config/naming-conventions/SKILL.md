---
name: naming-conventions
user-invocable: false
description: "Apply universal naming principles: avoid Manager/Helper/Util, use intention-revealing names, domain language, verb+noun functions. Use when naming variables, functions, classes, reviewing names, or refactoring for clarity. Language-agnostic principles."
allowed-tools:
  - Read
  - Grep
---

# Naming Conventions

Universal principles for clear, intention-revealing names. Language-agnostic—applies to TypeScript, Go, Rust, Python, etc.

## Core Principle

**Names should reveal intent and domain, not implementation.**

- `users` not `userArray` (domain, not data structure)
- `calculateTax` not `doTaxCalculation` (clear verb)
- `PaymentProcessor` not `PaymentManager` (specific action, not vague)

---

## Prohibited Patterns

### NEVER Use These Names

❌ **Manager, Helper, Util**

These are Ousterhout red flags — they're vague and don't reveal what the code does.

**Bad:**
```
UserManager
PaymentHelper
StringUtil
```

**Good:**
```
UserAuthenticator
PaymentProcessor
StringFormatter
```

**Why:** Naming forces design thinking. If you can't name it specifically, you don't understand what it does.

### RARELY Use (Context-Dependent)

⚠️ **Service, Handler, Processor, Controller**

These can work when they're domain-specific or framework patterns, but prefer more specific names.

**Bad (vague):**
```
DataService         // What kind of data?
RequestHandler      // What kind of request?
```

**Better (specific):**
```
OrderService        // Domain context: orders
HttpRequestHandler  // Framework pattern: HTTP requests
PaymentProcessor    // Domain action: processing payments
```

### SOMETIMES Acceptable

⚠️ **Base, Abstract (prefixes)**

Valid for framework/library code, but often hide intent in application code.

**Framework (acceptable):**
```typescript
abstract class BaseComponent { ... }
abstract class AbstractRepository { ... }
```

**Application (avoid):**
```typescript
// Better to name by domain
class Component { ... }              // If it's the base, no prefix needed
class Repository<T> { ... }         // Generic is clear without prefix
```

### Always Avoid

❌ **Generic containers:** Manager, Helper, Util, Misc, Common
❌ **Temporal names:** step1, phase1, doFirst, doSecond
❌ **Single letters:** x, y, temp (except loop counters i, j, k)
❌ **Vague abbreviations:** usr, msg, ctx (except well-known: id, url, api, http)

---

## Positive Patterns

### Variables

**Pattern:** Descriptive nouns

**Use domain language, not implementation:**
```
✅ activeUsers       // Domain concept
✅ totalRevenue      // Clear business term
✅ selectedItems     // What they are

❌ userArray         // Implementation detail (array)
❌ rev               // Abbreviation (unclear)
❌ items             // Too vague (items of what?)
❌ data              // Maximally vague
```

**Guidelines:**
- Descriptive, not abbreviated
- Domain terms, not data structures (users, not userArray)
- Context matters: `count` alone is vague, `activeUserCount` is clear
- Avoid single-letter names except loop counters (i, j, k)

### Functions

**Pattern:** Verb + noun

**Describe the action:**
```
✅ calculateTotal       // Clear action + target
✅ fetchUserData        // Action: fetch, target: user data
✅ isValidEmail         // Question: is valid?
✅ formatCurrency       // Transform: format

❌ total                // Missing verb (noun alone)
❌ getUserData          // Vague verb "get"
❌ validateEmail        // Returns boolean, use "is"
❌ currency             // Missing verb
❌ process              // Vague verb, no target
```

**Guidelines:**
- Start with clear verb (calculate, fetch, format, validate, parse, send, save)
- Pure functions: describe transformation (format, parse, convert)
- Side effects: verb implies action (save, send, fetch, update, delete)
- Boolean returns: use question prefix (is, has, can, should)
- Avoid vague verbs: get, do, handle, manage, process (without context)

### Classes & Types

**Pattern:** Singular nouns

**Use domain concepts:**
```
✅ User                // Domain entity
✅ PaymentProcessor    // Action-specific
✅ OrderRepository     // Pattern adds meaning
✅ EmailNotifier       // Clear purpose

❌ Users               // Plural (unless collection type)
❌ PaymentManager      // Manager anti-pattern
❌ OrderDB             // Implementation leak
❌ EmailHelper         // Helper anti-pattern
```

**Guidelines:**
- Singular nouns (User, Order, Payment, not Users, Orders)
- Domain terms, not technical terms (Invoice, not BillingDocument)
- Pattern suffixes acceptable when they add meaning (Repository, Factory, Builder, Strategy)
- Avoid generic suffixes (Manager, Helper, Util, Handler without context)

### Booleans

**Pattern:** Question prefix (is/has/can/should/will)

**Prefix reveals boolean nature:**
```
✅ isActive            // State question
✅ hasPermission       // Possession question
✅ canEdit             // Capability question
✅ shouldRefetch       // Conditional question
✅ willExpire          // Future state question

❌ active              // Ambiguous (could be status string)
❌ permission          // Looks like object
❌ editable            // Unclear (adjective, not question)
❌ enabled             // Past participle (prefer isEnabled)
```

**Prefix meanings:**
- **is**: State (isActive, isLoading, isValid, isEmpty)
- **has**: Possession (hasPermission, hasChildren, hasErrors)
- **can**: Capability (canEdit, canDelete, canSubmit)
- **should**: Conditional (shouldRefetch, shouldValidate)
- **will**: Future (willExpire, willRetry)

**Why questions work:** Boolean names should read like yes/no questions.

### Collections

**Pattern:** Plural indicates multiple items

**Use plural, avoid type suffixes:**
```
✅ users               // Plural indicates collection
✅ selectedItems       // What they are, plural
✅ errorMessages       // Clear and plural
✅ userById            // Keyed collection (by what)

❌ userList            // Redundant type suffix
❌ userArray           // Implementation leak
❌ userCollection      // Redundant suffix
❌ item                // Singular for plural collection
```

**Keyed collections (maps/dictionaries):**
```
✅ userById            // By key type
✅ configByEnv         // By environment
✅ productsByCategory  // Grouped by category

❌ userMap             // Type suffix redundant
❌ users               // Unclear it's keyed (ambiguous)
```

---

## Context-Aware Exceptions

Some generic names have valid domain justification:

### Framework Patterns

✅ **When acceptable:**
- `EventManager` in event-driven system (but `EventBus` is better)
- `ApiService` wrapping external API (but `ApiClient` is clearer)
- `RequestHandler` in HTTP framework (framework convention)
- `BaseComponent` in UI framework (inheritance pattern)

**Still prefer specific names when possible.**

### Repository Pattern

✅ **Acceptable:**
```
UserRepository
OrderRepository
```

This is a well-known pattern. The suffix adds meaning.

### Factory Pattern

✅ **Acceptable:**
```
UserFactory
ComponentFactory
```

Pattern name clarifies purpose.

---

## Quick Reference

### Pattern Templates

**Variables:** Descriptive nouns
```
activeUsers, totalCount, selectedItem, currentPage
```

**Functions:** Verb + noun
```
calculateTotal, fetchUser, formatDate, parseJson
```

**Booleans:** Question prefix
```
isActive, hasPermission, canEdit, shouldRefetch
```

**Classes:** Singular noun (+ pattern if meaningful)
```
User, Order, PaymentProcessor, OrderRepository
```

**Collections:** Plural nouns
```
users, items, errors, messages
```

---

## Examples: Before & After

### Example 1: Vague to Clear

❌ **Before:**
```
class DataManager
  processData(data)
  getData()
```

✅ **After:**
```
class OrderProcessor
  calculateOrderTotal(order)
  fetchActiveOrders()
```

### Example 2: Implementation to Domain

❌ **Before:**
```
userArray = fetchFromDB()
dataList = parseJsonString(response)
```

✅ **After:**
```
users = fetchUsers()
orders = parseOrderResponse(response)
```

### Example 3: Temporal to Functional

❌ **Before:**
```
function step1(data)
function step2(data)
function step3(data)
```

✅ **After:**
```
function validateData(data)
function enrichData(data)
function persistData(data)
```

---

## Philosophy

**"If you can't name it, you don't understand it."**

Naming is thinking. Bad names indicate unclear thinking. Good names indicate clear understanding.

**Naming forces design decisions:**
- Can't name a class? Maybe it's doing too much.
- Name is vague (Manager/Helper)? Unclear responsibility.
- Name is long (UserAccountPaymentProcessorManager)? Poor abstraction.

**Use domain language:**
- Domain experts should understand your names
- Names should match business concepts
- Avoid technical jargon when domain terms exist

**Names are for humans, not compilers.**

Write names for the person who reads your code in 6 months. That person is future you.
