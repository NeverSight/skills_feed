---
name: easy-query-expert
description: Guidance for Easy-Query ORM (Java), covering type-safe proxy queries, implicit joins, and tracking updates.
version: 1.0.0
author: cc123hh
tags: [java, orm, database, easy-query, sql, backend, proxy, type-safe, lambda]
repository: https://github.com/dromara/easy-query
---

# Easy-Query ORM

Easy-Query is a Java ORM framework based on APT proxy pattern, providing type-safe Lambda query syntax. This skill covers core concepts, common operations, relationship mapping, and advanced features.

## Core Concepts

### Proxy Pattern

Easy-Query uses APT (Annotation Processing Tool) to generate proxy classes at compile time, enabling type-safe query syntax.

**Entity Proxy** (`@EntityProxy`):
```java
@Table("t_blog")
@EntityProxy
public class BlogEntity implements ProxyEntityAvailable<BlogEntity, BlogEntityProxy> {
    private String title;
    private BigDecimal score;
}
```

**VO Proxy** (`@EntityFileProxy`):
```java
@EntityFileProxy
public class BlogVO {
    private String title;
    private BigDecimal avgScore;
}
```

### Proxy Class Generation Requirements

After using `@EntityProxy` or `@EntityFileProxy` annotations, **you must compile the project first** to generate proxy classes:
```bash
mvn clean compile
```

Generated proxy classes are located at: `target/generated-sources/annotations/`

### Lambda Field References

When querying, you must use Lambda expressions with proxy objects to access fields:
```java
// ✅ Correct: Using Lambda expression
easyEntityQuery.queryable(BlogEntity.class)
    .where(b -> b.title().like("Spring%"))
    .toList();

// ❌ Incorrect: Directly using getter method
easyEntityQuery.queryable(BlogEntity.class)
    .where(b -> b.getTitle().like("Spring%")) // Compilation error
```

## Quick Reference

### CRUD Operations Cheat Sheet

| Operation | Method | Example |
|-----------|--------|---------|
| Query Single | `firstOrNull()` | `.where(b -> b.id().eq("123")).firstOrNull()` |
| Query List | `toList()` | `.where(b -> b.score().gt(3.0)).toList()` |
| Insert | `insertable()` | `easyEntityQuery.insertable(entity).executeRows()` |
| Expression Update | `updatable().setColumns()` | `.setColumns(b -> b.title().set("New Title"))` |
| Entity Update | `updatable(entity)` | `easyEntityQuery.updatable(entity).executeRows()` |
| Delete | `deletable()` | `.where(b -> b.score().lt(1.0)).executeRows()` |

### Join Operations Cheat Sheet

| Type | Method | Use Case |
|------|--------|----------|
| Left Join | `.leftJoin(Class, (a,b) -> condition)` | Keep all left table data |
| Inner Join | `.innerJoin(Class, (a,b) -> condition)` | Return only matched data |
| Right Join | `.rightJoin(Class, (a,b) -> condition)` | Keep all right table data |

### Relationship Types Cheat Sheet

| Annotation Value | Relationship Type | Example |
|------------------|-------------------|---------|
| `OneToOne` | One-to-One | User ↔ Profile |
| `OneToMany` | One-to-Many | Topic → Multiple Blogs |
| `ManyToOne` | Many-to-One | Blog →所属 Topic |
| `ManyToMany` | Many-to-Many | Student ↔ Course |

## Common Operation Patterns

### Basic Queries

```java
// Single record query
BlogEntity blog = easyEntityQuery.queryable(BlogEntity.class)
    .where(b -> b.id().eq("123"))
    .firstOrNull();

// Multi-condition query
List<BlogEntity> blogs = easyEntityQuery.queryable(BlogEntity.class)
    .where(b -> {
        b.title().like("Easy%");
        b.score().gt(new BigDecimal("3.0"));
    })
    .orderBy(b -> b.publishTime().desc())
    .toList();
```

### Multi-Table Join

```java
// Left Join
easyEntityQuery.queryable(Topic.class)
    .leftJoin(BlogEntity.class, (t, b) -> t.id().eq(b.id()))
    .where((t, b) -> {
        t.id().eq("123");
        b.title().isNotNull();
    })
    .toList();
```

### Differential Update

```java
TrackManager trackManager = easyEntityQuery.getRuntimeContext().getTrackManager();
try {
    trackManager.begin();
    BlogEntity blog = easyEntityQuery.queryable(BlogEntity.class)
        .asTracking()
        .whereById("123").firstNotNull();
    blog.setViewCount(blog.getViewCount() + 1);
    easyEntityQuery.updatable(blog).executeRows();
} finally {
    trackManager.release();
}
```

### Pagination Query

```java
EasyPageResult<BlogEntity> pageResult = easyEntityQuery.queryable(BlogEntity.class)
    .where(b -> b.status().eq(1))
    .orderBy(b -> b.publishTime().desc())
    .toPageResult(1, 20);

long total = pageResult.getTotalCount();
List<BlogEntity> list = pageResult.getList();
```

### VO Query Mapping

```java
// Define VO
@EntityFileProxy
public class BlogVO {
    private String title;
    private BigDecimal avgScore;
}

// Use VO to receive results
List<BlogVO> vos = easyEntityQuery.queryable(BlogEntity.class)
    .groupBy(b -> b.category())
    .select(g -> new BlogVOProxy()
        .title().set(g.key())
        .avgScore().set(g.groupTable().score().avg())
    )
    .toList();
```

## Relationship Mapping Configuration

Use `@Navigate` annotation to define relationships between entities:

```java
// One-to-Many
@Navigate(value = RelationTypeEnum.OneToMany,
          selfProperty = "id",
          targetProperty = "topicId")
private List<BlogEntity> blogs;

// Many-to-One
@Navigate(value = RelationTypeEnum.ManyToOne,
          selfProperty = "topicId",
          targetProperty = "id")
private Topic topic;

// One-to-One
@Navigate(value = RelationTypeEnum.OneToOne,
          selfProperty = "id",
          targetProperty = "userId")
private UserProfile profile;
```

## Advanced Features Overview

### Implicit Join

Automatically handles OneToOne/ManyToOne relationships without explicit join:
```java
// Automatically generates LEFT JOIN
easyEntityQuery.queryable(SysUser.class)
    .where(u -> u.company().name().like("Alibaba"))
    .toList();
```

### Implicit Subquery

Automatically handles OneToMany/ManyToMany relationships:
```java
// Automatically generates EXISTS subquery
easyEntityQuery.queryable(Company.class)
    .where(c -> c.users().any(u -> u.name().like("Xiaoming")))
    .toList();
```

### Aggregation Query

```java
easyEntityQuery.queryable(BlogEntity.class)
    .where(b -> b.score().gt(new BigDecimal("3.0")))
    .groupBy(b -> GroupKeys.of(b.category()))
    .select(g -> Select.DRAFT.of(
        g.key1(),
        g.groupTable().score().avg(),
        g.groupTable().id().count()
    ))
    .toList();
```

## Common Issues Cheat Sheet

| Issue | Solution |
|-------|----------|
| Cannot find XXXProxy class | Run `mvn clean compile` to generate proxy classes |
| @Column mapping not working | VO needs to use the same column name mapping |
| Circular reference serialization issues | Use select to specify fields when querying or add JSON ignore annotations |
| Slow Join query performance | Optimize with `subQueryToGroupJoin = true` |

## Complete Resources

### Detailed Documentation

- **`references/advanced-features.md`** - Five implicit features explained in detail (Implicit Join/Subquery/Grouping/Partition/CASE WHEN)
- **`references/relationship-mapping.md`** - Complete @Navigate annotation configuration and best practices
- **`references/performance-optimization.md`** - Performance optimization tips and common pitfalls

### Working Examples

- **`examples/BlogEntity.java`** - Complete entity class example
- **`examples/QueryExamples.java`** - Various query operation examples
- **`examples/JoinExamples.java`** - Multi-table Join examples
- **`examples/TrackingUpdateExample.java`** - Complete differential update example

## Core Annotation Locations

- `@EntityProxy` / `@EntityFileProxy`: `sql-core/src/main/java/com/easy/query/core/annotation/`
- `@Table` / `@Column`: `sql-core/src/main/java/com/easy/query/core/annotation/`
- `@Navigate`: `sql-core/src/main/java/com/easy/query/core/annotation/`
- `ProxyEntityAvailable`: `sql-platform/sql-api-proxy/src/main/java/com/easy/query/core/proxy/`
