---
name: understanding-saleor-domain
description: "Explains Saleor e-commerce domain and Configurator business rules. Covers entity identification (slug vs name), deployment pipeline stages, and configuration schema. Triggers on: entity types, deployment pipeline, config schema, slug identification, categories, products, channels, YAML configuration."
allowed-tools: "Read, Grep, Glob, Bash(pnpm:*), Bash(git:*), Bash(ls:*)"
---

# Saleor Domain Expert

## Purpose

Provide deep domain knowledge about the Saleor e-commerce platform and the Configurator's business logic for entity management, configuration, deployment, and synchronization.

## When to Use

- Implementing new entity types or features
- Understanding entity identification patterns
- Working with deployment pipeline stages
- Debugging configuration synchronization issues
- Understanding business rules and constraints

## Table of Contents

- [Core Concepts](#core-concepts)
- [Entity Identification System](#entity-identification-system)
  - [Slug-Based Entities](#slug-based-entities)
  - [Name-Based Entities](#name-based-entities)
  - [Singleton Entities](#singleton-entities)
- [Deployment Pipeline](#deployment-pipeline)
- [Configuration Schema](#configuration-schema)
- [Bulk Operations](#bulk-operations)
- [Diff & Comparison Logic](#diff--comparison-logic)
- [Common Patterns](#common-patterns)
- [References](#references)

## Core Concepts

### What is Saleor Configurator?

A "commerce as code" CLI tool that enables declarative configuration management for Saleor e-commerce platforms. It allows developers to:

1. **Introspect**: Download remote Saleor configuration to local YAML files
2. **Deploy**: Apply local YAML configuration to remote Saleor instance
3. **Diff**: Compare local and remote configurations
4. **Start**: Interactive wizard for first-time setup

### Configuration as Code Philosophy

- Single source of truth for store state
- Version-controlled configuration (YAML in git)
- Reproducible deployments across environments
- Declarative over imperative management

## Entity Identification System

**Critical Rule**: Every entity has exactly ONE identification strategy.

### Slug-Based Entities

Identified by `slug` field. Used for entities that need URL-friendly identifiers.

| Entity | Identifier Field | Example |
|--------|------------------|---------|
| Categories | `slug` | `electronics` |
| Channels | `slug` | `default-channel` |
| Collections | `slug` | `summer-sale` |
| Menus | `slug` | `main-navigation` |
| Products | `slug` | `iphone-15-pro` |
| Warehouses | `slug` | `us-east-warehouse` |

**Implementation Pattern**:
```typescript
// Comparison uses slug
const isSameEntity = (local: Category, remote: Category) =>
  local.slug === remote.slug;

// Lookups use slug
const existing = await repository.findBySlug(entity.slug);
```

### Name-Based Entities

Identified by `name` field. Used for internal configuration entities.

| Entity | Identifier Field | Example |
|--------|------------------|---------|
| ProductTypes | `name` | `Physical Product` |
| PageTypes | `name` | `Blog Post` |
| TaxClasses | `name` | `Standard Rate` |
| ShippingZones | `name` | `North America` |
| Attributes | `name` | `Color` |

**Implementation Pattern**:
```typescript
// Comparison uses name
const isSameEntity = (local: ProductType, remote: ProductType) =>
  local.name === remote.name;
```

### Singleton Entities

Only one instance exists. No identifier needed.

| Entity | Notes |
|--------|-------|
| Shop | Global store settings |

## Deployment Pipeline

### Stage Order (Dependencies)

Stages execute in specific order due to dependencies:

```
1. Validation       → Pre-flight checks
2. Shop Settings    → Global configuration
3. Product Types    → Must exist before products
4. Page Types       → Must exist before pages
5. Attributes       → Used by product/page types
6. Categories       → Product organization
7. Collections      → Product groupings
8. Warehouses       → Required for inventory
9. Shipping Zones   → Geographic shipping rules
10. Products        → Depends on types, categories
11. Tax Config      → Tax rules and classes
12. Channels        → Sales channels
13. Menus           → Navigation (may reference products)
14. Models          → Custom data models
```

### Why Order Matters

**Example**: Cannot create a Product without its ProductType existing first.

```yaml
# This product depends on "Physical Product" type
products:
  - name: "iPhone 15"
    slug: "iphone-15"
    productType: "Physical Product"  # Must exist!
```

### Stage Execution Pattern

Each stage follows:
1. **Fetch**: Get current remote state
2. **Compare**: Diff local vs remote
3. **Plan**: Determine creates/updates/deletes
4. **Execute**: Apply changes with chunking
5. **Report**: Log results and failures

## Configuration Schema

### Top-Level Structure

```yaml
shop:
  # Global store settings

channels:
  # Sales channel definitions

taxClasses:
  # Tax rate classifications

productTypes:
  # Product type templates

pageTypes:
  # CMS page templates

attributes:
  # Shared attribute definitions

categories:
  # Product category hierarchy

collections:
  # Dynamic product collections

warehouses:
  # Fulfillment center definitions

shippingZones:
  # Geographic shipping configurations

products:
  # Product catalog

menus:
  # Navigation menu structures

models:
  # Custom data models
```

### Attribute Types

Attributes can be of various types:

| Type | Description | Example Values |
|------|-------------|----------------|
| `DROPDOWN` | Single select | `["Red", "Blue", "Green"]` |
| `MULTISELECT` | Multiple select | `["Feature A", "Feature B"]` |
| `RICH_TEXT` | HTML content | Rich text editor |
| `PLAIN_TEXT` | Simple text | Text input |
| `BOOLEAN` | True/false | Checkbox |
| `DATE` | Date picker | `2024-01-15` |
| `DATE_TIME` | Date and time | `2024-01-15T10:30:00` |
| `NUMERIC` | Numbers | `42.5` |
| `SWATCH` | Color/image swatch | Color picker |
| `FILE` | File upload | Document/image |
| `REFERENCE` | Entity reference | Links to other entities |

**Reference Attributes** (Special):
```yaml
attributes:
  - name: "Related Products"
    type: REFERENCE
    entityType: PRODUCT  # Must specify what it references
```

## Bulk Operations

### Chunking Strategy

Large operations are chunked to avoid timeouts and rate limits:

```typescript
const CHUNK_SIZE = 50; // Default chunk size
const chunks = splitIntoChunks(items, CHUNK_SIZE);

for (const chunk of chunks) {
  await processChunk(chunk);
  // Rate limiting handled by urql retry exchange
}
```

### Rate Limit Handling

The GraphQL client handles HTTP 429 automatically:
- Exponential backoff with jitter
- Max 5 retries
- Network error recovery

## Diff & Comparison Logic

### Comparison Dimensions

For each entity type, comparison checks:
1. **Existence**: Does entity exist remotely?
2. **Equality**: Are all relevant fields equal?
3. **Children**: Are nested structures equal?

### Diff Result Types

```typescript
type DiffAction = 'create' | 'update' | 'delete' | 'unchanged';

interface DiffResult<T> {
  action: DiffAction;
  local?: T;
  remote?: T;
  changes?: FieldChange[];
}
```

### Comparator Pattern

Each entity has a dedicated comparator:

```typescript
// src/core/diff/comparators/category-comparator.ts
export const compareCategorys = (
  local: Category[],
  remote: Category[]
): DiffResult<Category>[] => {
  // Match by slug
  // Compare relevant fields
  // Return diff results
};
```

## Common Patterns

### Adding a New Entity Type

1. Define Zod schema in `src/modules/config/schema/`
2. Create service in `src/modules/<entity>/`
3. Create repository with GraphQL operations
4. Add comparator in `src/core/diff/comparators/`
5. Add deployment stage in pipeline
6. Update schema documentation

### Handling Entity Dependencies

```typescript
// Check dependency exists before creating
const productType = await productTypeRepository.findByName(product.productType);
if (!productType) {
  throw new EntityDependencyError(
    `ProductType "${product.productType}" not found`
  );
}
```

## References

For detailed information, see:
- `{baseDir}/.claude/skills/saleor-domain-expert/references/entity-identification.md` - Complete entity identification rules
- `{baseDir}/.claude/skills/saleor-domain-expert/references/deployment-stages.md` - Pipeline stage details
- `{baseDir}/.claude/skills/saleor-domain-expert/references/schema-patterns.md` - YAML configuration patterns
- `{baseDir}/docs/ENTITY_REFERENCE.md` - Full entity documentation
- `{baseDir}/docs/ARCHITECTURE.md` - System architecture
- `{baseDir}/src/modules/config/schema/schema.ts` - Zod schema definitions

## Related Skills

- **Implementing entities**: See `adding-entity-types` for complete implementation workflow
- **Config schemas**: See `designing-zod-schemas` for schema patterns
- **GraphQL operations**: See `writing-graphql-operations` for Saleor API integration

## Quick Reference Rules

For condensed quick references, see:
- `.claude/rules/entity-development.md` (automatically loaded when editing `src/modules/**/*.ts`)
- `.claude/rules/diff-engine.md` (automatically loaded when editing `src/core/diff/**/*.ts`)
