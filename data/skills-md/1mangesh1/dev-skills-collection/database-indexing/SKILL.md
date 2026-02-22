---
name: database-indexing
description: Database indexing strategies and query optimization. Use when user asks to "optimize queries", "create indexes", "database performance", "query analysis", "explain plans", "index selection", "slow queries", "database tuning", "schema optimization", or mentions database performance and query optimization.
---

# Database Indexing & Query Optimization

Strategies for optimizing database queries through proper indexing and schema design.

## Index Types

### B-Tree Index
- Default for most databases (MySQL, PostgreSQL)
- Balanced tree structure
- Good for range queries and sorting

### Hash Index
- O(1) lookup for equality
- Not suitable for range queries
- Fast point lookups

### Full-Text Index
- Optimized for text search
- Language-specific analysis
- Used with text search queries

### Spatial Index
- R-tree, Quadtree for geographic data
- Optimized for spatial queries

### Composite Index
- Multiple columns in one index
- Column order matters (leftmost prefix)

## Query Optimization Techniques

### EXPLAIN Plans
```sql
EXPLAIN ANALYZE SELECT * FROM users WHERE id = 1;
```

### Index Selection
1. Look for WHERE clause columns
2. Consider JOIN conditions
3. Evaluate sorting/grouping columns
4. Check cardinality (selectivity)

### Avoid Common Mistakes
- Creating indexes on low-cardinality columns
- Creating unused indexes
- Over-indexing (write performance impact)
- Not analyzing index usage

## Performance Tuning

1. **Analyze queries** - Use EXPLAIN
2. **Identify bottlenecks** - Query profiling
3. **Test thoroughly** - Before/after metrics
4. **Monitor regularly** - Track performance changes
5. **Denormalize carefully** - Balance read vs write
6. **Archive old data** - Keep active data small
7. **Partition tables** - Handle large datasets

## Schema Design

- **Normalization** - Reduce redundancy
- **Appropriate data types** - Use INT not VARCHAR for IDs
- **Foreign keys** - Maintain referential integrity
- **Constraints** - Enforce data quality

## Tools & Commands

PostgreSQL:
```sql
CREATE INDEX idx_users_email ON users(email);
DROP INDEX idx_users_email;
ANALYZE;
```

MySQL:
```sql
EXPLAIN analyzer SELECT * FROM users WHERE email = 'test@example.com';
CREATE INDEX idx_email ON users(email);
```

## References

- PostgreSQL Index Documentation
- MySQL Performance Tuning
- Database Query Optimization Principles
- Use the Index, Luke! (Free online book)
