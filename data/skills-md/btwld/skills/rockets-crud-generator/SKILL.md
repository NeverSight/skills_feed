---
name: rockets-crud-generator
description: Generate complete Rockets SDK CRUD modules with TypeORM entities, NestJS modules, controllers, services, DTOs, and interfaces. Use when creating new entities, domain objects, or junction tables for many-to-many relationships.
---

# Rockets SDK CRUD Generator

Generate complete CRUD modules following Rockets SDK patterns with TypeORM, NestJS, and proper DTOs/interfaces.

## Quick Start

```bash
node crud-generator/scripts/generate.js '{
  "entityName": "Category",
  "fields": [
    { "name": "name", "type": "string", "required": true, "maxLength": 100 }
  ]
}'
```

## Configuration

```typescript
interface Config {
  // Required
  entityName: string;           // PascalCase entity name

  // Optional naming
  pluralName?: string;          // API path plural (auto-pluralized)
  tableName?: string;           // Database table (snake_case)

  // Output paths (configurable per project)
  paths?: {
    entity?: string;            // Default: "src/entities"
    module?: string;            // Default: "src/modules"
    shared?: string;            // Default: "src/shared" (set to null to skip)
  };

  // Shared package import path for generated code
  sharedPackage?: string;       // e.g., "@my-org/shared" (default: relative import)

  // Fields & Relations
  fields: FieldConfig[];
  relations?: RelationConfig[];

  // Operations (default: all)
  operations?: ('readMany' | 'readOne' | 'createOne' | 'updateOne' | 'deleteOne' | 'recoverOne')[];

  // Options
  generateModelService?: boolean;
  isJunction?: boolean;
}
```

### Field Configuration

```typescript
interface FieldConfig {
  name: string;
  type: 'string' | 'text' | 'number' | 'float' | 'boolean' | 'date' | 'uuid' | 'json' | 'enum';
  required?: boolean;           // Default: true
  unique?: boolean;
  maxLength?: number;
  minLength?: number;
  min?: number;
  max?: number;
  precision?: number;           // For float
  scale?: number;               // For float
  default?: any;
  enumValues?: string[];        // Required for enum type
  apiDescription?: string;
  apiExample?: any;
  creatable?: boolean;          // Include in CreateDto (default: true)
  updatable?: boolean;          // Include in UpdateDto (default: true)
}
```

### Relation Configuration

```typescript
interface RelationConfig {
  name: string;
  type: 'manyToOne' | 'oneToMany' | 'oneToOne';
  targetEntity: string;
  foreignKey?: string;          // Default: targetCamelId
  joinType?: 'LEFT' | 'INNER';
  onDelete?: 'CASCADE' | 'SET NULL' | 'RESTRICT';
  nullable?: boolean;
}
```

## Examples

### Basic Entity

```json
{
  "entityName": "Tag",
  "fields": [
    { "name": "name", "type": "string", "required": true, "maxLength": 50, "unique": true },
    { "name": "color", "type": "string", "maxLength": 7, "apiExample": "#FF5733" }
  ]
}
```

### With Custom Paths (monorepo)

```json
{
  "entityName": "Product",
  "paths": {
    "entity": "apps/api/src/entities",
    "module": "apps/api/src/modules",
    "shared": "packages/shared/src"
  },
  "fields": [
    { "name": "name", "type": "string", "required": true },
    { "name": "price", "type": "float", "precision": 10, "scale": 2 }
  ]
}
```

### Junction Table

```json
{
  "entityName": "ProductTag",
  "tableName": "product_tag",
  "isJunction": true,
  "fields": [],
  "relations": [
    { "name": "product", "type": "manyToOne", "targetEntity": "Product", "onDelete": "CASCADE" },
    { "name": "tag", "type": "manyToOne", "targetEntity": "Tag", "onDelete": "CASCADE" }
  ],
  "operations": ["readMany", "readOne", "createOne", "deleteOne"]
}
```

### Skip Shared Package

```json
{
  "entityName": "InternalLog",
  "paths": {
    "shared": null
  },
  "fields": [
    { "name": "message", "type": "text" }
  ]
}
```

## Generated Files

For entity `Category` with default paths:

```
src/
├── entities/
│   └── category.entity.ts
├── modules/category/
│   ├── constants/category.constants.ts
│   ├── category.module.ts
│   ├── category.crud.controller.ts
│   ├── category.crud.service.ts
│   ├── category-typeorm-crud.adapter.ts
│   └── category-access-query.service.ts
└── shared/category/          (if paths.shared is set)
    ├── dtos/
    │   ├── category.dto.ts
    │   ├── category-create.dto.ts
    │   ├── category-update.dto.ts
    │   └── category-paginated.dto.ts
    ├── interfaces/
    │   ├── category.interface.ts
    │   ├── category-creatable.interface.ts
    │   └── category-updatable.interface.ts
    └── index.ts
```

## Post-Generation

1. Export entity from entities index
2. Import module in app.module.ts
3. Add ACL resource (if using access control)
4. Export from shared index (if using shared package)
