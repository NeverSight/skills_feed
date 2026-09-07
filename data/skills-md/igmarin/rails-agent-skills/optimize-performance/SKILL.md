---
name: optimize-performance
type: atomic
license: MIT
description: >
  Use when investigating N+1s, slow queries, caching, or query plans in Rails.
  Profile before changing code. Trigger words: N+1, slow, performance,
  caching, EXPLAIN.
metadata:
  version: 1.0.0
  user-invocable: "true"
---

# Optimize Performance

Identify and fix performance bottlenecks in Rails applications.

## Quick Reference

| Tool | Use |
|------|-----|
| `bullet` | N+1 detection in development |
| `rack-mini-profiler` | Endpoint timing breakdown |
| `EXPLAIN ANALYZE` | Query plan analysis |

## HARD-GATE

```text
NEVER optimize without a baseline measurement
ALWAYS write a regression spec before optimizing (query count assertion)
ALWAYS verify with EXPLAIN ANALYZE for database changes

NEVER write the report as "I applied includes(:author), then wrote a spec
to lock it in." The spec MUST be written and shown failing BEFORE the fix
appears in your output. Reordering for narrative flow fails the audit even
when the underlying work was correct.
```

## Output Style

When completing a performance optimization, output MUST follow this seven-step report order. Each step must appear in output:

```markdown
# Performance Optimization — [Description]

## 1. Baseline
<N> queries for <endpoint/action> — source: <log line / profiler output>

## 2. Bottleneck
<N+1 on association X / missing index on column Y> — tool: <bullet / rack-mini-profiler / EXPLAIN ANALYZE>

## 3. Regression Spec — RED
`make_database_queries(count: <N>)` at <path>:<line> — failure: expected <M>, got <N>

## 4. Fix
<path>:<line> — <includes(:association) / add_index / cache block>

## 5. Regression Spec — GREEN
Spec passes ✓ (<M> queries)

## 6. EXPLAIN ANALYZE
Before: Seq Scan, actual time=<X>ms → After: Index Scan, actual time=<Y>ms

## 7. Quantified Improvement
Queries: <N> → <M> | p95: <X>ms → <Y>ms
```

Language: English unless explicitly requested otherwise.

## Extended Resources

**Less-Obvious Optimization**
```ruby
# Use counter_cache to avoid COUNT queries in loops
# In migration: add_column :users, :posts_count, :integer, default: 0
# In Post model: belongs_to :user, counter_cache: true
user.posts_count  # no extra query
```

**Regression Spec (Query Count Assertion)**
```ruby
RSpec.describe "Post index performance" do
  it "loads posts with authors in a fixed number of queries" do
    create_list(:post, 10, :with_author)

    expect do
      get posts_path
    end.to make_database_queries(count: 2) # 1 posts query + 1 authors query
  end
end
```
Use the `db-query-matchers` gem or a custom `make_database_queries` matcher.

Run directly in `rails dbconsole` (PostgreSQL) after applying an index or query change:
```sql
EXPLAIN ANALYZE
  SELECT posts.*, users.name
  FROM posts
  INNER JOIN users ON users.id = posts.author_id
  WHERE posts.published = true;
```

**Reference Files and External Links**

Load these files only when their specific content is needed:

- **[references/tools.md](references/tools.md)** — Use when you need detailed Bullet, rack-mini-profiler, or EXPLAIN ANALYZE configuration and installation steps

External references:
- [Active Record Querying](https://guides.rubyonrails.org/active_record_querying.html)
- [rack-mini-profiler](https://github.com/MiniProfiler/rack-mini-profiler)
- [Bullet gem](https://github.com/flyerhzm/bullet)

## Integration

| Skill | When to chain |
|-------|---------------|
| **write-tests** | For regression specs |
| **review-migration** | When adding an index |
