---
name: postgresql-rails-analyzer
description: Comprehensive PostgreSQL configuration and usage analysis for Rails applications. Use when Claude Code needs to analyze a Rails codebase for database performance issues, optimization opportunities, or best practice violations. Detects N+1 queries, missing indexes, suboptimal database configurations, anti-patterns, and provides actionable recommendations. Ideal for performance audits, optimization tasks, or when users ask to "analyze the database", "check for N+1 queries", "optimize PostgreSQL", "review database performance", or "suggest database improvements".
---

# PostgreSQL Rails Analyzer

Analyze Rails applications for PostgreSQL performance issues and provide actionable optimization recommendations based on "High Performance PostgreSQL for Rails" best practices.

## Overview

This skill performs comprehensive analysis of Rails applications to identify:

- N+1 query problems and missing eager loading
- Missing or suboptimal indexes
- Database configuration issues
- Common anti-patterns
- Performance optimization opportunities

## Analysis Scripts

Run these scripts from the Rails application root directory to analyze different aspects of the codebase:

### 1. N+1 Query Analysis

```bash
python3 scripts/analyze_n_plus_one.py
```

Detects potential N+1 query issues by analyzing:

- Controller actions for queries without eager loading
- View files for association access patterns
- Missing `includes`, `preload`, or `eager_load` calls

### 2. Index Analysis

```bash
python3 scripts/analyze_indexes.py
```

Identifies indexing opportunities:

- Foreign keys without indexes (critical)
- Boolean columns that could benefit from partial indexes
- Columns frequently used in WHERE clauses
- Missing composite indexes

### 3. Configuration Analysis

```bash
python3 scripts/analyze_config.py
```

Reviews database.yml for:

- Connection pool sizing
- Timeout configurations (statement_timeout, lock_timeout)
- Prepared statements settings
- SSL/TLS configuration
- Connection reaping configuration
- Recommended PostgreSQL extensions

## Workflow

When a user requests PostgreSQL analysis, follow this workflow:

### Step 1: Understand the Request

Clarify what the user wants to analyze:

- Full performance audit?
- Specific issue (slow queries, N+1 problems)?
- Configuration review?
- Schema optimization?

### Step 2: Run Appropriate Analysis Scripts

Based on the request, run one or more analysis scripts:

```bash
# For comprehensive analysis, run all three
python3 scripts/analyze_n_plus_one.py
python3 scripts/analyze_indexes.py
python3 scripts/analyze_config.py
```

### Step 3: Review Results

Examine the output from each script, which categorizes issues by severity:

- **WARNING**: High-priority issues that likely impact performance
- **INFO**: Optimization opportunities and best practice recommendations

### Step 4: Provide Recommendations

Create a prioritized list of actionable recommendations:

1. **Critical Issues** (fix immediately)
   - Foreign keys without indexes
   - N+1 queries in hot paths
   - Missing statement timeouts

2. **Performance Optimizations** (high impact)
   - Add partial indexes for boolean columns
   - Implement counter caches
   - Enable eager loading in specific queries

3. **Best Practices** (lower priority, preventative)
   - Configuration tuning
   - Connection pool optimization
   - Enable monitoring extensions

### Step 5: Generate Migration Code

For index and schema recommendations, provide ready-to-use migration code:

```ruby
class AddPerformanceIndexes < ActiveRecord::Migration[7.0]
  def change
    # Add foreign key index
    add_index :posts, :user_id, algorithm: :concurrently

    # Add partial index for boolean column
    add_index :users, :active, where: "active = false", algorithm: :concurrently

    # Add composite index
    add_index :orders, [:status, :created_at], algorithm: :concurrently
  end
end
```

Note: Use `algorithm: :concurrently` for production migrations to avoid locking tables.

### Step 6: Reference Additional Documentation

When users need deeper understanding, refer them to:

- `references/performance_guide.md` - Comprehensive best practices guide
- `references/anti_patterns.md` - Common mistakes and solutions

Load these references when:

- User asks "how do I fix this?"
- User wants to understand why something is a problem
- User needs examples of solutions
- User asks about specific patterns (e.g., "what's a partial index?")

## Common User Requests

### "Analyze my Rails app for performance issues"

Run all three analysis scripts and provide a comprehensive report organized by priority.

### "Check for N+1 queries"

Run `analyze_n_plus_one.py` and explain each detected issue with suggested fixes using `includes`, `preload`, or `eager_load`.

### "Why are my queries slow?"

1. Run index analysis
2. Review database configuration
3. Check for N+1 patterns
4. Suggest EXPLAIN ANALYZE for specific slow queries

### "Review my database.yml"

Run `analyze_config.py` and explain each configuration recommendation with context about why it matters.

### "Should I add an index?"

Run index analysis and evaluate:

- Is there a foreign key without an index?
- Is the column used in WHERE clauses frequently?
- Would a partial or composite index be more appropriate?

## Key Principles

### Always Explain Why

Don't just list issues - explain:

- Why it's a problem
- What impact it has on performance
- How to fix it
- Trade-offs of the solution

### Provide Context

Reference specific chapters from "High Performance PostgreSQL for Rails" when relevant:

- Chapter 2: Administration Basics
- Chapter 5: Optimizing Active Record
- Chapter 7: Improving Query Performance
- Chapter 8: Optimized Indexes for Fast Retrieval

### Be Pragmatic

Not every detected issue requires immediate action. Help users prioritize:

- What will have the biggest impact?
- What's easiest to fix?
- What can wait?

### Show, Don't Tell

Always provide concrete examples and migration code, not just abstract recommendations.

## Advanced Analysis

For deeper analysis beyond the scripts, manually review:

### Schema Design

- Check for appropriate data types (bigint for high-volume PKs, jsonb vs json)
- Verify constraints are in place (NOT NULL, CHECK, FOREIGN KEY)
- Identify missing validation constraints

### Query Patterns

- Use `rails c` to run EXPLAIN ANALYZE on slow queries
- Check for sequential scans on large tables
- Identify expensive joins

### Model Code

- Look for missing counter caches
- Check for potential batch operation opportunities
- Identify queries that could use `find_each` instead of `each`

## Limitations

These analysis scripts use static analysis and may produce:

- **False positives**: Flagging issues that aren't actually problems in practice
- **False negatives**: Missing issues that require runtime analysis

Always recommend:

- Testing fixes in a staging environment
- Using EXPLAIN ANALYZE to verify query performance
- Monitoring production impact after changes

## Tools Integration

Suggest complementary tools for ongoing monitoring:

- **PgHero**: PostgreSQL performance dashboard
- **pg_stat_statements**: Query performance tracking
- **Bullet gem**: Runtime N+1 query detection
- **Rails query logging**: Enable in development

## Example Output Format

When providing analysis results, use this format:

```text
PostgreSQL Performance Analysis Report
=====================================

🔍 Analysis Summary:
- Scanned X files
- Found Y issues
- Z high-priority recommendations

⚠️  CRITICAL ISSUES (fix immediately):
1. Missing foreign key index on posts.user_id
   Impact: Slow joins, cascading delete performance
   Fix: add_index :posts, :user_id, algorithm: :concurrently

2. N+1 query in PostsController#index
   Impact: 1 + N queries instead of 2 queries
   Fix: Use .includes(:user) on line 12

💡 OPTIMIZATION OPPORTUNITIES:
1. Partial index for users.active column
   Impact: Faster queries for inactive users
   Fix: add_index :users, :active, where: "active = false"

📊 CONFIGURATION RECOMMENDATIONS:
1. Set statement_timeout to prevent runaway queries
   Add to database.yml: statement_timeout: 30000

✅ BEST PRACTICES:
- Enable pg_stat_statements for query monitoring
- Consider adding counter caches for frequently counted associations
```

## Tips for Claude Code

When using this skill in Claude Code:

1. Always navigate to the Rails root directory first
2. Run scripts with Python 3 (`python3`, not `python`)
3. Parse script output carefully - it's formatted for human readability
4. Provide migration code in addition to recommendations
5. Ask clarifying questions if the codebase structure is unusual
6. Offer to create migration files directly if the user requests it
