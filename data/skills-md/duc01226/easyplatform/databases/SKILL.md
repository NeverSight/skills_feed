---
name: databases
version: 2.0.0
description: Database technology selection, schema design, query optimization, and migration guidance for MongoDB, SQL Server, PostgreSQL, and Redis. Triggers on database schema, mongodb query, sql server, postgresql, redis cache, database migration, index optimization.
infer: true
allowed-tools: Read, Bash, Grep, Glob
---

# Databases

## Purpose
Guide database technology selection, schema design, query optimization, and migration patterns -- with EasyPlatform-specific context for service-to-database mapping.

## When to Use
- Choosing which database technology for a new feature or service
- Designing a schema or data model for a new entity
- Optimizing slow queries or adding indexes
- Writing or reviewing database migrations
- Troubleshooting connection or performance issues
- Understanding EasyPlatform's database topology

## When NOT to Use
- Writing C# repository code -- use `easyplatform-backend` skill (repositories follow platform patterns)
- Cross-service data access design -- use `arch-cross-service-integration` skill (must use message bus, never direct DB access)
- General backend CQRS implementation -- use `easyplatform-backend` skill
- Frontend data fetching -- use `frontend-angular-api-service` skill

## Prerequisites
- Understand which EasyPlatform service you are working in
- Read `docs/claude/architecture.md` for service boundaries

## EasyPlatform Database Topology

| Service          | Database                     | Technology | Connection                            |
| ---------------- | ---------------------------- | ---------- | ------------------------------------- |
| TextSnippet      | Example service data         | MongoDB    | `localhost:27017` (root/rootPassXXX)  |
| TextSnippet (EF) | Example service data         | SQL Server | `localhost,14330` (sa/123456Abc)      |
| TextSnippet (PG) | Example service data         | PostgreSQL | `localhost:54320` (postgres/postgres) |
| Caching          | Session, rate limiting       | Redis      | `localhost:6379`                      |
| Messaging        | Event bus                    | RabbitMQ   | `localhost:15672` (guest/guest)       |

**CRITICAL**: Each service owns its database. Never access another service's database directly -- use the message bus.

## Workflow

### Step 1: Identify Service and Database

IF using MongoDB persistence module THEN MongoDB patterns apply.
IF using EF Core with SQL Server THEN SQL Server / EF Core patterns apply.
IF using EF Core with PostgreSQL THEN PostgreSQL / EF Core patterns apply.
IF caching or session data THEN Redis patterns apply.

### Step 2: Select Task

| Task                     | Go To   |
| ------------------------ | ------- |
| New entity/schema design | Step 3A |
| Query optimization       | Step 3B |
| Migration                | Step 3C |
| Index design             | Step 3D |

### Step 3A: Schema Design
1. Define entity class following platform patterns (see CLAUDE.md Entity section)
2. For MongoDB: design document structure, decide embed vs. reference
3. For SQL Server/PostgreSQL: design tables with proper normalization, foreign keys
4. For Redis: design key naming convention (`{service}:{entity}:{id}`)
5. Add navigation properties using `[PlatformNavigationProperty]` where needed

### Step 3B: Query Optimization
1. Identify the slow query (check logs or `EXPLAIN ANALYZE` / MongoDB `.explain()`)
2. Check if proper indexes exist for the query's filter and sort columns
3. For MongoDB: check if aggregation pipeline can replace multiple queries
4. For SQL Server/PostgreSQL: check if CTEs or window functions simplify logic
5. Verify N+1 queries are prevented -- use `loadRelatedEntities` parameter in repository calls

### Step 3C: Migration
1. For EF Core (SQL Server/PostgreSQL):
   ```bash
   dotnet ef migrations add MigrationName --project [Service].Persistence
   dotnet ef database update
   ```
2. For MongoDB (platform migration):
   - Create `PlatformMongoMigrationExecutor<ServiceDbContext>` class
   - Name format: `YYYYMMDD_Description`
   - Use paged processing for large datasets
3. For data seeding: use `PlatformDataMigrationExecutor<DbContext>`

### Step 3D: Index Design
1. **MongoDB**: Use compound indexes matching query patterns
   ```javascript
   db.collection.createIndex({ companyId: 1, status: 1, createdDate: -1 })
   ```
2. **SQL Server/PostgreSQL**: Index foreign keys and frequently filtered columns
   ```sql
   CREATE INDEX IX_Employee_CompanyId_Status ON Employees(CompanyId, Status) INCLUDE (Name);
   ```
3. **Redis**: No traditional indexes -- design keys for direct lookup patterns

### Step 4: Verification
- Run the query/migration in a test environment
- Verify performance improvement with explain plans
- Ensure migration is idempotent and backward-compatible
- Check that repository extensions use static expressions (see CLAUDE.md patterns)

## Output Format
```markdown
## Database: [Task Summary]

### Context
- Service: [Service name]
- Database: [MongoDB | SQL Server | PostgreSQL | Redis]
- Task: [schema | query | migration | index]

### Recommendation
[Specific technical recommendation]

### Implementation
[Code or SQL/MongoDB commands]

### Verification
[How to confirm correctness]
```

## Detailed References
Load for database-specific deep dives:

| Topic                  | File                                      |
| ---------------------- | ----------------------------------------- |
| MongoDB CRUD           | `references/mongodb-crud.md`              |
| MongoDB aggregation    | `references/mongodb-aggregation.md`       |
| MongoDB indexes        | `references/mongodb-indexing.md`          |
| MongoDB Atlas          | `references/mongodb-atlas.md`             |
| PostgreSQL queries     | `references/postgresql-queries.md`        |
| PostgreSQL CLI         | `references/postgresql-psql-cli.md`       |
| PostgreSQL performance | `references/postgresql-performance.md`    |
| PostgreSQL admin       | `references/postgresql-administration.md` |

## Related Skills
- `easyplatform-backend` -- for C# repository, entity, and migration execution patterns
- `database-optimization` -- for advanced performance tuning and N+1 prevention
- `arch-cross-service-integration` -- for cross-service data access via message bus

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**
- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
