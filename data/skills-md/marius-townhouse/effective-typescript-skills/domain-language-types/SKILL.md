---
name: domain-language-types
description: Use when naming types. Use when types describe structure not meaning. Use when domain experts won't understand type names.
---

# Name Types Using the Language of Your Problem Domain

## Overview

**Type names should communicate meaning, not structure.**

A type named `INodeNameValueData` tells you nothing. A type named `APIResponse` or `CustomerOrder` tells you everything. Use the language of your business domain, not the language of data structures.

## When to Use This Skill

- Naming new types
- Refactoring unclear type names
- Reviewing code with domain experts
- Designing public APIs

## The Iron Rule

```
Type names should be meaningful to domain experts.
If a non-programmer can't understand it, rename it.
```

**Remember:**
- Business terms > technical terms
- Meaning > structure
- Names are documentation
- Domain experts should recognize types

## Detection: Structural Names

```typescript
// Bad: describes structure, not meaning
interface IEntityWithIdAndName {
  id: string;
  name: string;
}

interface IStringPairList {
  items: [string, string][];
}

interface IDataRecord {
  data: Record<string, unknown>;
}
```

What IS an `IEntityWithIdAndName`? A user? A product? A category?

## Better: Domain Names

```typescript
// Good: describes what it IS
interface User {
  id: string;
  name: string;
}

interface TranslationPairs {
  items: [sourcePhrase: string, targetPhrase: string][];
}

interface CustomerProfile {
  data: Record<string, unknown>;
}
```

## Real Example: E-commerce

```typescript
// Bad: generic/structural names
interface IData {
  id: string;
  props: Record<string, unknown>;
}

interface IEntity extends IData {
  type: string;
}

interface ICollection {
  items: IEntity[];
  total: number;
}
```

vs.

```typescript
// Good: domain language
interface Product {
  sku: string;
  name: string;
  price: Money;
  inventory: number;
}

interface Order {
  orderNumber: string;
  customer: Customer;
  items: OrderItem[];
  total: Money;
}

interface ProductCatalog {
  products: Product[];
  totalCount: number;
}
```

## Avoid These Patterns

### Hungarian Notation Prefixes

```typescript
// Bad: I prefix for interfaces
interface IUser { }
interface IProduct { }

// Good: just the name
interface User { }
interface Product { }
```

### Type Suffixes

```typescript
// Bad: redundant suffixes
interface UserType { }
interface ProductInterface { }
interface OrderObject { }

// Good: clean names
interface User { }
interface Product { }
interface Order { }
```

### Generic Technical Terms

```typescript
// Bad: generic
interface DataModel { }
interface EntityRecord { }
interface ItemContainer { }

// Good: specific
interface Invoice { }
interface ShippingAddress { }
interface ShoppingCart { }
```

## Property Names Too

```typescript
// Bad: technical property names
interface User {
  dataString: string;
  valueNumber: number;
  itemsArray: Product[];
}

// Good: domain property names
interface User {
  email: string;
  age: number;
  purchases: Product[];
}
```

## Context Matters

Same structure, different domains:

```typescript
// Healthcare domain
interface Patient {
  mrn: string;          // Medical Record Number
  admissionDate: Date;
  diagnosis: string[];
}

// Education domain  
interface Student {
  studentId: string;
  enrollmentDate: Date;
  courses: string[];
}
```

The structure is similar, but the names communicate different meanings.

## When Technical Names Are OK

### Standard Technical Concepts

```typescript
// OK: widely understood technical terms
interface HttpRequest { }
interface DatabaseConnection { }
interface CacheEntry { }
```

### Generic Utilities

```typescript
// OK: truly generic utilities
type Nullable<T> = T | null;
type AsyncResult<T> = Promise<T>;
```

### Internal Implementation

```typescript
// OK for internal implementation details
interface InternalCacheNode<T> { }
interface TreeNodeImpl<T> { }
```

## Ubiquitous Language

From Domain-Driven Design: use "ubiquitous language" that both developers and domain experts share.

```typescript
// If domain experts say "fulfillment", use that:
interface OrderFulfillment { }

// Not:
interface OrderProcessingData { }
interface IOrderExecutionEntity { }
```

## Pressure Resistance Protocol

### 1. "It's a Technical Detail"

**Pressure:** "Users won't see this type name"

**Response:** Developers will. Future you will. Make it meaningful.

**Action:** Name it for what it represents, not how it's structured.

### 2. "We Have Naming Conventions"

**Pressure:** "Our style guide says use I prefix"

**Response:** Conventions should serve clarity, not hinder it.

**Action:** Challenge conventions that reduce clarity. IUser adds nothing.

## Red Flags - STOP and Reconsider

- Type names starting with I, T, or ending in Type/Interface/Object
- Names that describe structure (StringArray, NumberMap)
- Names that a domain expert wouldn't recognize
- Multiple types that could all be called "Data"

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "It matches our backend" | Backend might have bad names too |
| "It's just internal" | Internal code needs clarity too |
| "That's our convention" | Bad conventions should change |

## Quick Reference

```typescript
// DON'T: Structural/technical names
interface IDataEntity { }
interface StringValuePair { }
interface ItemsCollection<T> { }

// DO: Domain language names
interface Customer { }
interface PriceRange { }  // [min: Money, max: Money]
interface ProductCatalog { }

// DON'T: Redundant suffixes
interface UserType { }
interface ProductInterface { }

// DO: Clean names
interface User { }
interface Product { }
```

## The Bottom Line

**Name types for what they mean, not how they're structured.**

Domain experts should be able to read your type names and understand what they represent. `Invoice` tells you more than `IFinancialDataRecord`. Use the language of your problem domain.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 41: Name Types Using the Language of Your Problem Domain.
