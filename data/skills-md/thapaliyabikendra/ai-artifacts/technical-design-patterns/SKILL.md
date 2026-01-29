---
name: technical-design-patterns
description: "Create technical design documents for ABP Framework features including API contracts, database schemas, and architecture decisions. Use when: (1) designing REST APIs, (2) planning database schemas, (3) creating technical specifications, (4) documenting architecture decisions (ADRs)."
layer: 2
tech_stack: [agnostic, markdown, mermaid]
topics: [technical-specification, api-contract, database-schema, adr, architecture-decisions]
depends_on: [mermaid-diagram-patterns]
complements: [api-design-principles]
keywords: [TSD, ADR, API Contract, Schema, ERD, Specification, Architecture]
---

# Technical Design Patterns

Create comprehensive technical design documents that guide implementation of ABP Framework features.

## When to Use

- Designing REST API endpoints and contracts
- Planning database schemas and indexes
- Creating Technical Specification Documents (TSD)
- Documenting Architecture Decision Records (ADRs)
- Defining DTO structures and validation rules

## Technical Design Document Structure

A complete TSD for an ABP feature includes:

1. **Overview** - Feature summary and scope
2. **API Contract** - Endpoints, methods, DTOs
3. **Database Schema** - Tables, columns, indexes, relationships
4. **Permissions** - Required permissions and role mappings
5. **Validation Rules** - Input constraints
6. **Caching Strategy** - What to cache, TTL
7. **Open Questions** - Items needing clarification

## API Contract Template

```markdown
## API: {Resource}

### Overview
| Attribute | Value |
|-----------|-------|
| Base Path | `/api/app/{resources}` |
| Authentication | Required |
| Rate Limit | 100/min |

### Endpoints

| Method | Path | Description | Permission | Request | Response |
|--------|------|-------------|------------|---------|----------|
| GET | `/{resources}` | List with pagination | `{Project}.{Resources}` | `Get{Resource}ListInput` | `PagedResultDto<{Resource}Dto>` |
| GET | `/{resources}/{id}` | Get by ID | `{Project}.{Resources}` | - | `{Resource}Dto` |
| POST | `/{resources}` | Create new | `{Project}.{Resources}.Create` | `CreateUpdate{Resource}Dto` | `{Resource}Dto` |
| PUT | `/{resources}/{id}` | Update existing | `{Project}.{Resources}.Edit` | `CreateUpdate{Resource}Dto` | `{Resource}Dto` |
| DELETE | `/{resources}/{id}` | Soft delete | `{Project}.{Resources}.Delete` | - | - |

### DTOs

#### {Resource}Dto (Output)
```json
{
  "id": "guid",
  "property1": "string",
  "property2": 0,
  "creationTime": "datetime",
  "lastModificationTime": "datetime"
}
```

#### CreateUpdate{Resource}Dto (Input)
```json
{
  "property1": "string (required, max 100)",
  "property2": "number (optional, min 0)"
}
```

#### Get{Resource}ListInput (Query)
```json
{
  "filter": "string (optional)",
  "sorting": "string (optional, e.g., 'name asc')",
  "skipCount": "number (default 0)",
  "maxResultCount": "number (default 10, max 100)"
}
```
```

## Database Schema Template

```markdown
## Entity: {Name}

### Table: {TableName}

| Column | Type | Nullable | Default | Constraints | Description |
|--------|------|----------|---------|-------------|-------------|
| `Id` | `uuid` | NO | `gen_random_uuid()` | PK | Unique identifier |
| `Name` | `varchar(100)` | NO | - | - | Display name |
| `Email` | `varchar(255)` | NO | - | UNIQUE | Contact email |
| `Status` | `smallint` | NO | `0` | - | Enum: 0=Active, 1=Inactive |
| `ParentId` | `uuid` | YES | - | FK | Reference to parent |
| `CreationTime` | `timestamp` | NO | `now()` | - | ABP audit field |
| `CreatorId` | `uuid` | YES | - | - | ABP audit field |
| `LastModificationTime` | `timestamp` | YES | - | - | ABP audit field |
| `LastModifierId` | `uuid` | YES | - | - | ABP audit field |
| `IsDeleted` | `boolean` | NO | `false` | - | ABP soft delete |
| `DeleterId` | `uuid` | YES | - | - | ABP audit field |
| `DeletionTime` | `timestamp` | YES | - | - | ABP audit field |

### Indexes

| Name | Columns | Type | Purpose |
|------|---------|------|---------|
| `PK_{Table}` | `Id` | Primary | Primary key |
| `IX_{Table}_Email` | `Email` | Unique | Email lookup |
| `IX_{Table}_Name` | `Name` | B-tree | Name search |
| `IX_{Table}_ParentId` | `ParentId` | B-tree | Parent lookup |
| `IX_{Table}_IsDeleted` | `IsDeleted` | Partial (false) | Active records filter |

### Relationships

| Relationship | Type | Target | FK Column | On Delete |
|--------------|------|--------|-----------|-----------|
| Parent | N:1 | `{Parent}` | `ParentId` | SET NULL |
| Children | 1:N | `{Child}` | - | CASCADE |
```

## Permission Design Template

```markdown
## Permissions: {Resource}

### Permission Definitions

| Permission | Display Name | Parent |
|------------|--------------|--------|
| `{Project}.{Resources}` | {Resource} Management | - |
| `{Project}.{Resources}.Create` | Create {Resource} | `{Project}.{Resources}` |
| `{Project}.{Resources}.Edit` | Edit {Resource} | `{Project}.{Resources}` |
| `{Project}.{Resources}.Delete` | Delete {Resource} | `{Project}.{Resources}` |

### Role Mapping

| Role | View | Create | Edit | Delete |
|------|------|--------|------|--------|
| Admin | ✓ | ✓ | ✓ | ✓ |
| Manager | ✓ | ✓ | ✓ | - |
| User | ✓ | - | - | - |
```

## Architecture Decision Record (ADR) Template

```markdown
# ADR-{NNN}: {Decision Title}

**Status**: Proposed | Accepted | Deprecated | Superseded
**Date**: YYYY-MM-DD
**Deciders**: [List of people involved]

## Context

[Describe the issue motivating this decision. What is the problem we're trying to solve?]

## Decision Drivers

- [Driver 1: e.g., performance requirement]
- [Driver 2: e.g., maintainability concern]
- [Driver 3: e.g., team expertise]

## Considered Options

1. **[Option 1]** - [Brief description]
2. **[Option 2]** - [Brief description]
3. **[Option 3]** - [Brief description]

## Decision

We will use **[Option X]** because [rationale].

## Consequences

### Positive
- [Benefit 1]
- [Benefit 2]

### Negative
- [Drawback 1]
- [Drawback 2]

### Risks
- [Risk 1 and mitigation]

## Related Decisions

- [ADR-XXX: Related decision]
```

## Validation Rules Template

```markdown
## Validation: CreateUpdate{Resource}Dto

| Property | Rules | Error Message |
|----------|-------|---------------|
| `Name` | Required, MaxLength(100) | "Name is required" / "Name cannot exceed 100 characters" |
| `Email` | Required, EmailFormat, MaxLength(255) | "Valid email is required" |
| `Phone` | Optional, PhoneFormat | "Invalid phone format" |
| `Amount` | Required, Range(0, 999999.99) | "Amount must be between 0 and 999999.99" |
```

## Caching Strategy Template

```markdown
## Caching: {Resource}

| Operation | Cache Key | TTL | Invalidation |
|-----------|-----------|-----|--------------|
| GetById | `{resource}:{id}` | 5 min | On Update, Delete |
| GetList | `{resource}:list:{hash}` | 1 min | On Create, Update, Delete |
| GetCount | `{resource}:count` | 1 min | On Create, Delete |

### Cache Implementation
- **Provider**: Redis (distributed)
- **Serialization**: JSON
- **Compression**: None (small payloads)
```

## Quality Checklist

Before finalizing technical design:

- [ ] All CRUD endpoints defined with permissions
- [ ] DTOs match entity properties (no entity exposure)
- [ ] Database schema includes all ABP audit columns
- [ ] Indexes defined for query patterns
- [ ] Validation rules specified for all inputs
- [ ] Relationships and cascade behavior defined
- [ ] Caching strategy considered for read-heavy operations
- [ ] Open questions documented

## References

- [references/api-examples.md](references/api-examples.md) - Real API contract examples
- [references/schema-examples.md](references/schema-examples.md) - Database schema examples
