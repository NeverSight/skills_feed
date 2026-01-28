---
name: spice-views
description: Configure SQL views in Spice for virtual tables and query abstraction. Use when asked to "create a view", "add virtual table", "define SQL view", or "create derived table".
---

# Spice Views

Views are virtual tables defined by SQL queries, useful for simplifying complex queries and reusing logic.

## Basic Configuration

```yaml
views:
  - name: <view_name>
    sql: |
      SELECT ...
```

## Examples

### Simple View
```yaml
views:
  - name: active_users
    sql: |
      SELECT id, name, email
      FROM users
      WHERE status = 'active'
```

### Aggregation View
```yaml
views:
  - name: daily_sales
    sql: |
      SELECT 
        DATE(created_at) as date,
        SUM(amount) as total,
        COUNT(*) as orders
      FROM orders
      GROUP BY DATE(created_at)
```

### Join View
```yaml
views:
  - name: order_details
    sql: |
      SELECT 
        o.id,
        o.created_at,
        c.name as customer,
        p.name as product,
        o.quantity
      FROM orders o
      JOIN customers c ON o.customer_id = c.id
      JOIN products p ON o.product_id = p.id
```

### Accelerated View
Views can be accelerated like datasets:

```yaml
views:
  - name: rankings
    sql: |
      SELECT product_id, SUM(quantity) as total_sold
      FROM orders
      GROUP BY product_id
      ORDER BY total_sold DESC
      LIMIT 100
    acceleration:
      enabled: true
      refresh_check_interval: 1h
```

## Querying Views

Views are queried like regular tables:

```sql
SELECT * FROM active_users WHERE email LIKE '%@example.com';
SELECT * FROM daily_sales WHERE date >= '2024-01-01';
```

## Limitations

- Views are read-only (no INSERT/UPDATE/DELETE)
- Performance depends on underlying query complexity
- Complex views may benefit from acceleration

## Documentation

- [Views Overview](https://spiceai.org/docs/components/views)
- [Views Reference](https://spiceai.org/docs/reference/spicepod/views)
