---
name: encapsulation
description: Use when exposing internal state. Use when making fields public for convenience. Use when external code modifies object internals.
---

# Encapsulation

## Overview

**Hide internal state. Expose behavior, not data. Control access through methods.**

Public fields let anyone modify your object's internals, bypassing validation and breaking invariants. Encapsulation protects data integrity.

## When to Use

- Designing classes with state
- Tempted to make fields public
- External code directly modifies object state
- Invariants can be violated by direct access

## The Iron Rule

```
NEVER expose internal state directly. Always use methods to control access.
```

**No exceptions:**
- Not for "it's simpler"
- Not for "we trust callers"
- Not for "it's just data"
- Not for "getters/setters are verbose"

## Detection: Exposed State Smell

If internal state is directly accessible, STOP:

```typescript
// ❌ VIOLATION: Public state
class BankAccount {
  public balance: number = 0;  // Anyone can modify!
  public transactions: Transaction[] = [];
}

// Callers can break invariants
const account = new BankAccount();
account.balance = -1000000;  // Negative balance!
account.transactions = [];   // Audit trail destroyed!
```

Problems:
- No validation on changes
- Invariants easily violated
- No audit trail
- Can't change internal representation

## The Correct Pattern: Private State, Public Methods

```typescript
// ✅ CORRECT: Encapsulated state
class BankAccount {
  private _balance: number = 0;
  private _transactions: Transaction[] = [];
  
  get balance(): number {
    return this._balance;
  }
  
  deposit(amount: number): void {
    if (amount <= 0) {
      throw new Error('Deposit must be positive');
    }
    
    this._balance += amount;
    this._transactions.push({
      type: 'deposit',
      amount,
      timestamp: new Date()
    });
  }
  
  withdraw(amount: number): void {
    if (amount <= 0) {
      throw new Error('Withdrawal must be positive');
    }
    if (amount > this._balance) {
      throw new Error('Insufficient funds');
    }
    
    this._balance -= amount;
    this._transactions.push({
      type: 'withdrawal',
      amount,
      timestamp: new Date()
    });
  }
  
  getTransactionHistory(): ReadonlyArray<Transaction> {
    return [...this._transactions];  // Return copy
  }
}

// Now invariants are protected
const account = new BankAccount();
account.deposit(100);     // ✅ Validated, logged
account.withdraw(50);     // ✅ Validated, logged
account.balance = -1000;  // ❌ Error: Cannot set
```

## Encapsulation Techniques

### 1. Private Fields
```typescript
class User {
  private _password: string;
  
  setPassword(newPassword: string): void {
    if (newPassword.length < 8) throw new Error('Too short');
    this._password = hash(newPassword);
  }
  
  checkPassword(attempt: string): boolean {
    return verify(attempt, this._password);
  }
}
```

### 2. Readonly for Read-Only Access
```typescript
class Config {
  readonly apiUrl: string;
  readonly timeout: number;
  
  constructor(apiUrl: string, timeout: number) {
    this.apiUrl = apiUrl;
    this.timeout = timeout;
  }
}
```

### 3. Return Copies, Not References
```typescript
class Order {
  private _items: OrderItem[] = [];
  
  // ❌ BAD: Returns reference
  getItems(): OrderItem[] {
    return this._items;  // Caller can modify!
  }
  
  // ✅ GOOD: Returns copy
  getItems(): OrderItem[] {
    return [...this._items];
  }
  
  // ✅ ALSO GOOD: Return readonly
  getItems(): ReadonlyArray<OrderItem> {
    return this._items;
  }
}
```

### 4. Validate in Setters
```typescript
class Product {
  private _price: number = 0;
  
  get price(): number {
    return this._price;
  }
  
  set price(value: number) {
    if (value < 0) throw new Error('Price cannot be negative');
    if (value > 1000000) throw new Error('Price too high');
    this._price = value;
  }
}
```

## Pressure Resistance Protocol

### 1. "It's Simpler"
**Pressure:** "Public fields are less code"

**Response:** Less code now, more bugs later. Encapsulation prevents invalid states.

**Action:** Private fields + methods. The extra code is validation.

### 2. "We Trust Callers"
**Pressure:** "Our team won't misuse public fields"

**Response:** Teams grow. Code evolves. Mistakes happen. Protect invariants in code.

**Action:** Don't rely on caller discipline. Enforce in class.

### 3. "It's Just Data"
**Pressure:** "This class is just a data container"

**Response:** Even data has rules. Emails have formats. Ages have ranges.

**Action:** Use DTOs/interfaces for pure data. Classes = behavior + encapsulation.

### 4. "Getters/Setters Are Verbose"
**Pressure:** "Java-style getters/setters are boilerplate"

**Response:** TypeScript has concise `get`/`set` syntax. Use it.

**Action:** `get balance()` is not verbose.

## Red Flags - STOP and Reconsider

- `public` keyword on mutable fields
- Direct property assignment from outside
- Arrays/objects returned by reference
- No validation on state changes
- Invariants only documented, not enforced

**All of these mean: Encapsulate the state.**

## Quick Reference

| Exposed (Bad) | Encapsulated (Good) |
|---------------|---------------------|
| `public balance` | `private _balance` + `deposit()`/`withdraw()` |
| `return this.items` | `return [...this.items]` |
| Direct mutation | Method with validation |
| Trust callers | Enforce in class |

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "Simpler" | Simpler to write, harder to maintain. |
| "We trust callers" | Code should enforce, not trust. |
| "Just data" | Data has constraints. Enforce them. |
| "Verbose" | TypeScript getters are concise. |
| "Over-engineering" | It's just engineering. |

## The Bottom Line

**Private state. Public methods. Validate on every change.**

Never expose internal state directly. Return copies of collections. Validate in setters. Encapsulation protects invariants and enables safe evolution.
