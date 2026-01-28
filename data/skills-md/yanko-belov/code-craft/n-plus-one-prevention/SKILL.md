---
name: n-plus-one-prevention
description: Use when fetching related data in loops. Use when seeing multiple queries for one request. Use when database is slow on list endpoints.
---

# N+1 Query Prevention

## Overview

**Never query in a loop. Fetch related data in a single query.**

N+1 is when you fetch N items, then make N more queries to get related data. It's the most common database performance killer.

## When to Use

- Fetching a list with related data
- Loop that contains a database query
- Slow list/index endpoints
- Multiple queries for one API response

## The Iron Rule

```
NEVER put a database query inside a loop.
```

**No exceptions:**
- Not for "it's only a few items"
- Not for "the query is fast"
- Not for "we'll cache it"
- Not for "it's simpler"

## Detection: N+1 Pattern

If you query inside a loop, STOP:

```typescript
// ❌ VIOLATION: N+1 queries
const orders = await Order.findAll();  // 1 query

const ordersWithCustomers = await Promise.all(
  orders.map(async (order) => {
    // N queries (one per order)
    const customer = await Customer.findByPk(order.customerId);
    return { ...order, customerName: customer.name };
  })
);
// Total: 1 + N queries
```

For 100 orders = 101 database queries!

## The Correct Pattern: Eager Loading

```typescript
// ✅ CORRECT: Single query with JOIN

// Sequelize
const orders = await Order.findAll({
  include: [{ model: Customer, attributes: ['name'] }]
});
// 1 query with JOIN

// Prisma
const orders = await prisma.order.findMany({
  include: { customer: { select: { name: true } } }
});

// TypeORM
const orders = await orderRepository.find({
  relations: ['customer']
});

// Raw SQL
const orders = await db.query(`
  SELECT o.*, c.name as customer_name 
  FROM orders o
  JOIN customers c ON o.customer_id = c.id
`);
```

## Common N+1 Scenarios

### 1. Related Entity
```typescript
// ❌ N+1
posts.map(post => await User.findById(post.authorId));

// ✅ Eager load
Post.findAll({ include: [User] });
```

### 2. Aggregates
```typescript
// ❌ N+1
users.map(user => await Order.count({ where: { userId: user.id } }));

// ✅ Subquery or GROUP BY
User.findAll({
  attributes: {
    include: [[sequelize.fn('COUNT', sequelize.col('orders.id')), 'orderCount']]
  },
  include: [{ model: Order, attributes: [] }],
  group: ['User.id']
});
```

### 3. Multiple Relations
```typescript
// ❌ N+1 (multiple)
orders.map(order => {
  await Customer.findByPk(order.customerId);
  await Product.findAll({ where: { orderId: order.id } });
});

// ✅ Eager load all
Order.findAll({
  include: [Customer, Product]
});
```

## Detection Tools

```typescript
// Log query count per request
let queryCount = 0;
db.on('query', () => queryCount++);

app.use((req, res, next) => {
  queryCount = 0;
  res.on('finish', () => {
    if (queryCount > 10) {
      console.warn(`N+1 alert: ${req.path} made ${queryCount} queries`);
    }
  });
  next();
});
```

## Pressure Resistance Protocol

### 1. "It's Only a Few Items"
**Pressure:** "We only have 10 orders"

**Response:** 10 becomes 100 becomes 10,000. Fix it now.

**Action:** Always use eager loading regardless of current data size.

### 2. "The Query Is Fast"
**Pressure:** "Each query takes 1ms"

**Response:** 1ms × 1000 = 1 second. Network overhead adds more.

**Action:** One 5ms query beats 1000 × 1ms queries.

### 3. "We'll Cache It"
**Pressure:** "Redis will cache the results"

**Response:** Cache misses still hit the DB. First requests are slow. Cache adds complexity.

**Action:** Fix the query. Cache if still needed.

### 4. "It's Simpler"
**Pressure:** "Looping is easier to understand"

**Response:** Simple code that's 100x slower isn't simple.

**Action:** Learn your ORM's eager loading syntax.

## Red Flags - STOP and Reconsider

- `await` inside `.map()` or `.forEach()`
- Query count grows with result size
- List endpoints slower than detail endpoints
- "Loading..." takes forever on lists
- ORM lazy loading by default

**All of these mean: Refactor to eager loading.**

## Quick Reference

| N+1 (Bad) | Eager Loading (Good) |
|-----------|---------------------|
| Loop + query | JOIN / include |
| 1 + N queries | 1 query |
| O(N) round trips | O(1) round trips |
| Slower with more data | Constant query count |

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "Few items" | Data grows. Fix now. |
| "Fast query" | N slow > 1 medium. |
| "We'll cache" | Cache doesn't fix bad queries. |
| "It's simpler" | Slow isn't simple. |
| "ORM handles it" | ORMs default to lazy loading. |

## The Bottom Line

**One query for the list. One query for related data. Never query in a loop.**

Use eager loading (include/join) to fetch related data. Watch query counts. Any query inside a loop is a bug waiting to scale.
