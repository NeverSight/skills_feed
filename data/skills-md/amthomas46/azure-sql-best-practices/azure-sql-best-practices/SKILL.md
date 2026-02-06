---
name: azure-sql-best-practices
description: Azure SQL Database best practices skill for optimizing T-SQL code, database configuration, indexing strategies, and application patterns. Based on Microsoft SQL Assessment API, SSDT Code Analysis rules, Azure SQL Database performance guidance, and official Microsoft best practices. Use this skill when writing, reviewing, or refactoring code that interacts with Azure SQL Database.
license: MIT
metadata:
  author: microsoft-community
  version: "1.1.0"
  sources:
    - SQL Assessment API
    - SSDT Code Analysis (SR0001-SR0016)
    - Azure SQL Database Performance Guidance
    - Microsoft Learn Documentation
---

# Azure SQL Database Best Practices

Comprehensive best practices guide for Azure SQL Database development and optimization. This skill helps AI agents analyze and improve T-SQL scripts, application database code, indexing strategies, security configurations, and connection patterns.

Based on:
- [SQL Assessment API](https://learn.microsoft.com/en-us/sql/tools/sql-assessment-api/sql-assessment-api-overview)
- [SSDT Code Analysis Rules](https://learn.microsoft.com/en-us/previous-versions/visualstudio/visual-studio-2010/dd172133(v=vs.100))
- [Azure SQL Database Performance Guidance](https://learn.microsoft.com/en-us/azure/azure-sql/database/performance-guidance)
- [Azure SQL Database Security Best Practices](https://learn.microsoft.com/en-us/azure/azure-sql/database/security-best-practice)

## When to Apply

Reference these guidelines when:
- Writing new T-SQL queries, stored procedures, or scripts
- Reviewing database code for performance issues
- Configuring Azure SQL Database settings
- Implementing data access patterns in applications
- Optimizing indexing strategies
- Auditing security configurations
- Refactoring existing database code
- Migrating from SQL Server to Azure SQL Database

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Query Performance | CRITICAL | `query-` |
| 2 | Indexing Strategy | CRITICAL | `index-` |
| 3 | Security & Compliance | HIGH | `security-` |
| 4 | Connection Management | HIGH | `connection-` |
| 5 | T-SQL Patterns | MEDIUM-HIGH | `tsql-` |
| 6 | SSDT Code Analysis | MEDIUM-HIGH | `SR****` |
| 7 | Database Configuration | MEDIUM | `config-` |
| 8 | Data Modeling | MEDIUM | `model-` |
| 9 | Monitoring & Diagnostics | LOW-MEDIUM | `monitor-` |

## SSDT Code Analysis Rules (Microsoft Static Analysis)

These rules are from Microsoft's SQL Server Data Tools (SSDT) static code analysis. They are enforced in Visual Studio Database Projects.

### Design Issues (SR0001, SR0008-SR0014)

| Rule ID | Description | Severity |
|---------|-------------|----------|
| **SR0001** | Avoid SELECT * in queries | HIGH |
| **SR0008** | Use SCOPE_IDENTITY() instead of @@IDENTITY | MEDIUM |
| **SR0009** | Avoid VARCHAR/NVARCHAR with size 1 or 2 | LOW |
| **SR0010** | Avoid deprecated *= and =* join syntax | MEDIUM |
| **SR0013** | Output parameter not populated in all code paths | MEDIUM |
| **SR0014** | Potential data loss from implicit type casting | HIGH |

### Performance Issues (SR0004-SR0007, SR0015)

| Rule ID | Description | Severity |
|---------|-------------|----------|
| **SR0004** | Avoid non-indexed columns in IN predicates | HIGH |
| **SR0005** | Avoid LIKE patterns starting with '%' | HIGH |
| **SR0006** | Move column reference to one side of comparison | MEDIUM |
| **SR0007** | Use ISNULL(column, default) on nullable columns | MEDIUM |
| **SR0015** | Extract deterministic function calls from WHERE | MEDIUM |

### Naming Issues (SR0011, SR0012, SR0016)

| Rule ID | Description | Severity |
|---------|-------------|----------|
| **SR0011** | Avoid special characters in object names | LOW |
| **SR0012** | Avoid reserved words for type names | MEDIUM |
| **SR0016** | Avoid sp_ prefix for stored procedures | MEDIUM |

## Quick Reference

### 1. Query Performance (CRITICAL)

- `query-avoid-select-star` (SR0001) - Never use SELECT * in production code
- `query-parameterize` - Always use parameterized queries to prevent SQL injection and enable plan caching
- `query-avoid-functions-on-columns` - Don't apply functions to columns in WHERE clauses
- `query-sargable` - Write SARGable (Search ARGument ABLE) predicates for index usage
- `query-batch-operations` - Batch INSERT/UPDATE/DELETE operations to reduce round trips
- `query-avoid-cursors` - Replace cursors with set-based operations
- `query-limit-results` - Use TOP or OFFSET-FETCH for pagination
- `query-avoid-implicit-conversion` (SR0014) - Match data types to prevent implicit conversions
- `query-join-optimization` - Order joins for optimal execution plans
- `query-exists-vs-count` - Use EXISTS instead of COUNT(*) > 0
- `query-avoid-leading-wildcard` (SR0005) - Avoid LIKE '%value' patterns

### 2. Indexing Strategy (CRITICAL)

- `index-cover-queries` - Create covering indexes for frequent queries
- `index-avoid-over-indexing` - Balance read vs write performance
- `index-missing-index-dmv` - Use DMVs to identify missing indexes
- `index-unused-indexes` - Remove unused indexes consuming resources
- `index-fragmentation` - Monitor and address index fragmentation
- `index-columnstore` - Use columnstore indexes for analytics workloads
- `index-filtered` - Use filtered indexes for subset queries
- `index-include-columns` - Use INCLUDE for non-key columns
- `index-key-order` - Order index keys by selectivity
- `index-avoid-wide-keys` - Keep index keys narrow
- `index-in-predicate` (SR0004) - Ensure columns in IN predicates are indexed

### 3. Security & Compliance (HIGH)

- `security-parameterize-queries` - Prevent SQL injection with parameters
- `security-least-privilege` - Grant minimum required permissions
- `security-avoid-sa` - Never use sa or dbo for application access
- `security-encrypt-connections` - Always use encrypted connections
- `security-row-level-security` - Implement RLS for multi-tenant apps
- `security-dynamic-data-masking` - Mask sensitive data
- `security-always-encrypted` - Use Always Encrypted for sensitive columns
- `security-tde` - Enable Transparent Data Encryption
- `security-audit-logging` - Enable SQL Audit for compliance
- `security-vulnerability-assessment` - Regular vulnerability scans

### 4. Connection Management (HIGH)

- `connection-pooling` - Always use connection pooling
- `connection-retry-logic` - Implement retry logic for transient failures
- `connection-timeout` - Set appropriate connection timeouts
- `connection-close-dispose` - Always close/dispose connections
- `connection-async` - Use async/await for database calls
- `connection-read-replicas` - Use read replicas for read workloads
- `connection-application-intent` - Set ApplicationIntent for read replicas
- `connection-multisubnetfailover` - Enable for geo-replicated databases

### 5. T-SQL Patterns (MEDIUM-HIGH)

- `tsql-set-nocount` - Use SET NOCOUNT ON in stored procedures
- `tsql-schema-qualify` - Always schema-qualify object names
- `tsql-avoid-hints` - Avoid query hints unless necessary
- `tsql-temp-tables-vs-variables` - Choose appropriately between temp tables and table variables
- `tsql-transaction-scope` - Keep transactions short
- `tsql-error-handling` - Use TRY-CATCH with proper error handling
- `tsql-avoid-triggers` - Minimize trigger usage
- `tsql-cte-vs-subquery` - Use CTEs for readability and recursion
- `tsql-merge-carefully` - Use MERGE with caution
- `tsql-avoid-dynamic-sql` - Minimize dynamic SQL, parameterize when used
- `tsql-scope-identity` (SR0008) - Use SCOPE_IDENTITY() instead of @@IDENTITY
- `tsql-avoid-deprecated-joins` (SR0010) - Use ANSI JOIN syntax, not *= or =*
- `tsql-output-params` (SR0013) - Populate output parameters in all code paths
- `tsql-avoid-sp-prefix` (SR0016) - Don't prefix stored procedures with sp_

### 6. Data Type Best Practices (MEDIUM)

- `type-appropriate-size` (SR0009) - Avoid VARCHAR(1) or VARCHAR(2), use CHAR instead
- `type-avoid-deprecated` - Don't use TEXT, NTEXT, IMAGE types
- `type-match-column-types` - Match parameter types to column types
- `type-avoid-max-unnecessarily` - Use specific sizes instead of MAX when possible
- `type-nullable-handling` (SR0007) - Use ISNULL on nullable columns in expressions
- `type-reserved-words` (SR0012) - Don't use reserved words for type names

### 7. Naming Conventions (MEDIUM)

- `naming-avoid-special-chars` (SR0011) - Avoid special characters in object names
- `naming-avoid-reserved-words` (SR0012) - Don't use reserved words as identifiers
- `naming-consistent-case` - Use consistent casing (PascalCase or snake_case)
- `naming-descriptive` - Use descriptive, meaningful names
- `naming-avoid-prefixes` - Avoid Hungarian notation prefixes

### 8. Database Configuration (MEDIUM)

- `config-query-store` - Enable Query Store for performance insights
- `config-auto-tuning` - Enable automatic tuning
- `config-max-dop` - Configure appropriate MAXDOP
- `config-memory-grant` - Monitor memory grants
- `config-compatibility-level` - Use appropriate compatibility level
- `config-auto-stats` - Enable auto create/update statistics
- `config-page-verify` - Use CHECKSUM for page verification
- `config-recovery-model` - Choose appropriate recovery model
- `config-tempdb` - Optimize tempdb configuration
- `config-accelerated-recovery` - Enable Accelerated Database Recovery

### 9. Data Modeling (MEDIUM)

- `model-normalization` - Normalize appropriately (3NF minimum)
- `model-appropriate-types` - Use appropriate data types
- `model-avoid-nullable` - Minimize NULL columns where possible
- `model-partition-strategy` - Implement partitioning for large tables
- `model-computed-columns` - Use computed columns for derived values
- `model-constraint-enforcement` - Use constraints for data integrity
- `model-hierarchical-pk` - Use hierarchical partition keys for scale
- `model-temporal-tables` - Use temporal tables for audit trails
- `model-json-columns` - Use JSON columns judiciously

### 10. Monitoring & Diagnostics (LOW-MEDIUM)

- `monitor-query-performance-insight` - Use Query Performance Insight
- `monitor-dmvs` - Leverage DMVs for diagnostics
- `monitor-extended-events` - Use Extended Events for tracing
- `monitor-intelligent-insights` - Enable Intelligent Insights
- `monitor-resource-utilization` - Track DTU/vCore usage
- `monitor-deadlock-analysis` - Analyze and prevent deadlocks
- `monitor-wait-statistics` - Monitor wait statistics
- `monitor-log-io` - Monitor transaction log I/O

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/query-avoid-select-star.md
rules/index-cover-queries.md
rules/security-parameterize-queries.md
rules/tsql-code-analysis.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- How to detect violations
- References and additional context

## Full Compiled Document

For the complete guide with all rules expanded:
`AGENTS.md`

## Scripts

Helper scripts for automated analysis:
- `scripts/analyze-tsql.py` - Analyze T-SQL files for violations (includes SSDT rules)
- `scripts/check-indexes.sql` - Check for missing/unused indexes
- `scripts/security-audit.sql` - Security configuration audit
- `scripts/run-assessment.ps1` - Run SQL Assessment API checks

## References

- `references/sql-assessment-api.md` - SQL Assessment API overview
- `references/dmv-queries.md` - Useful DMV queries for diagnostics
- `references/connection-strings.md` - Connection string best practices
- `references/ssdt-code-analysis.md` - SSDT Code Analysis rules reference
