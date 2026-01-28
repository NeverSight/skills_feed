---
name: backend-model-creation
description: Create a new Mongoose model with proper typing, utilities, and patterns. Use when asked to "create a model", "add a data model", "create a schema", or "add a new entity".
---

# Backend Model Creation

This skill creates Mongoose models following established patterns with proper typing from `@{project}/types`.

## Overview

Models follow a types-first approach:
1. Define TypeScript types in `@{project}/types`
2. Create Mongoose model in backend importing those types
3. Use shared enum options for validation

## File Structure

```
libs/types/src/
├── lib/
│   ├── Workflow.ts         # Type definitions
│   └── {Resource}.ts       # New resource types
└── index.ts                # Re-exports

apps/backend/src/models/
├── _utils.ts               # generateId, stripId helpers
├── Workflow.ts             # Mongoose model
└── {Resource}.ts           # New resource model
```

## Step 1: Create Types in @{project}/types

Create `libs/types/src/lib/{Resource}.ts`:

```typescript
// Define enum options as const arrays (used for both TS types and Mongoose validation)
export const ResourceStatusOptions = ['active', 'inactive', 'archived'] as const;
export type ResourceStatus = typeof ResourceStatusOptions[number];

// Optional: Additional enum options
export const ResourcePriorityOptions = ['low', 'medium', 'high'] as const;
export type ResourcePriority = typeof ResourcePriorityOptions[number];

// Subdocument types (if needed)
export type ResourceMetadata = {
  source?: string;
  tags?: string[];
  priority?: ResourcePriority;
};

// Main entity type
export type Resource = {
  id: string;
  name: string;
  description?: string;
  status: ResourceStatus;
  metadata?: ResourceMetadata;
  createdAt: Date;
  updatedAt: Date;
};
```

Export from `libs/types/src/index.ts`:

```typescript
export * from './lib/Resource';
```

## Step 2: Create the Mongoose Model

Create `apps/backend/src/models/{Resource}.ts`:

```typescript
import { Schema, model, Document, Types } from 'mongoose';
import {
  Resource as IResource,
  ResourceStatusOptions,
  ResourcePriorityOptions,
} from '@{project}/types';
import { generateId, stripId } from './_utils';

// Subdocument schema (if needed)
const MetadataSchema = new Schema(
  {
    source: { type: String },
    tags: { type: [String], default: undefined },
    priority: { type: String, enum: ResourcePriorityOptions },
  },
  { _id: false }
);

// Main schema
const resourceSchema = new Schema<IResource>(
  {
    id: { type: String, required: true, unique: true, index: true, default: generateId },
    name: { type: String, required: true },
    description: { type: String },
    status: { type: String, enum: ResourceStatusOptions, required: true, default: 'active' },
    metadata: { type: MetadataSchema },
    createdAt: { type: Date, default: Date.now },
    updatedAt: { type: Date, default: Date.now },
  },
  {
    id: false,           // Disable Mongoose's virtual id (we use our own)
    versionKey: false,   // Disable __v field
    toJSON: { transform: stripId },
    toObject: { transform: stripId },
  }
);

// Compound indexes for common queries
resourceSchema.index({ status: 1, createdAt: -1 });

// Pre-save hook to update timestamp (Mongoose 8+ - no next() callback)
resourceSchema.pre('save', function () {
  this.updatedAt = new Date();
});

// Export document type for services
export type ResourceDocument = Document<unknown, object, IResource> &
  IResource & { _id: Types.ObjectId };

const Resource = model<IResource>('Resource', resourceSchema);
export default Resource;
```

## Key Patterns

### Utilities from `_utils.ts`

Always import from `_utils`:

```typescript
import { generateId, stripId } from './_utils';
```

- `generateId`: UUID v4 wrapper for generating unique IDs
- `stripId`: Transform helper to remove `_id` from JSON/object output

### ID Field Pattern

Always use this pattern for the `id` field:

```typescript
id: { type: String, required: true, unique: true, index: true, default: generateId },
```

### Enum Options Pattern

Define options as `const` arrays in types:

```typescript
// In @{project}/types
export const StatusOptions = ['active', 'inactive'] as const;
export type Status = typeof StatusOptions[number];

// In Mongoose model
import { StatusOptions } from '@{project}/types';
status: { type: String, enum: StatusOptions, required: true, default: 'active' },
```

### Schema Options

Always include these options to ensure clean API responses:

```typescript
{
  id: false,           // Disable Mongoose's virtual id
  versionKey: false,   // Disable __v field
  toJSON: { transform: stripId },
  toObject: { transform: stripId },
}
```

### Subdocument Schemas

For embedded documents, always disable `_id`:

```typescript
const AddressSchema = new Schema(
  {
    street: { type: String, required: true },
    city: { type: String, required: true },
    zipCode: { type: String },
  },
  { _id: false }
);

// Use in main schema
address: { type: AddressSchema }
```

### Array Fields

For optional arrays, use `default: undefined` to avoid empty arrays:

```typescript
tags: { type: [String], default: undefined },
```

For required arrays with default empty:

```typescript
items: { type: [ItemSchema], required: true, default: [] },
```

### Indexes

Single field indexes:

```typescript
id: { type: String, index: true },
```

Compound indexes (add after schema definition):

```typescript
// Put equality filters first, then sort fields
resourceSchema.index({ status: 1, createdAt: -1 });
resourceSchema.index({ userId: 1, status: 1 });
```

### Pre-save Hook

Mongoose 8+ uses synchronous hooks (no `next()` callback):

```typescript
resourceSchema.pre('save', function () {
  this.updatedAt = new Date();
});
```

### Document Type Export

Export the document type for use in services:

```typescript
export type ResourceDocument = Document<unknown, object, IResource> &
  IResource & { _id: Types.ObjectId };
```

## Complete Example

### Types (`libs/types/src/lib/Project.ts`)

```typescript
export const ProjectStatusOptions = ['planning', 'active', 'completed', 'archived'] as const;
export type ProjectStatus = typeof ProjectStatusOptions[number];

export const ProjectPriorityOptions = ['low', 'medium', 'high', 'critical'] as const;
export type ProjectPriority = typeof ProjectPriorityOptions[number];

export type ProjectMember = {
  userId: string;
  role: 'owner' | 'editor' | 'viewer';
  joinedAt: Date;
};

export type Project = {
  id: string;
  name: string;
  description?: string;
  status: ProjectStatus;
  priority: ProjectPriority;
  members: ProjectMember[];
  ownerId: string;
  startDate?: Date;
  dueDate?: Date;
  completedAt?: Date;
  createdAt: Date;
  updatedAt: Date;
};
```

### Model (`apps/backend/src/models/Project.ts`)

```typescript
import { Schema, model, Document, Types } from 'mongoose';
import {
  Project as IProject,
  ProjectStatusOptions,
  ProjectPriorityOptions,
} from '@{project}/types';
import { generateId, stripId } from './_utils';

// Member subdocument schema
const MemberSchema = new Schema(
  {
    userId: { type: String, required: true },
    role: { type: String, enum: ['owner', 'editor', 'viewer'], required: true },
    joinedAt: { type: Date, default: Date.now },
  },
  { _id: false }
);

// Main Project schema
const projectSchema = new Schema<IProject>(
  {
    id: { type: String, required: true, unique: true, index: true, default: generateId },
    name: { type: String, required: true },
    description: { type: String },
    status: { type: String, enum: ProjectStatusOptions, required: true, default: 'planning' },
    priority: { type: String, enum: ProjectPriorityOptions, required: true, default: 'medium' },
    members: { type: [MemberSchema], required: true, default: [] },
    ownerId: { type: String, required: true, index: true },
    startDate: { type: Date },
    dueDate: { type: Date },
    completedAt: { type: Date },
    createdAt: { type: Date, default: Date.now },
    updatedAt: { type: Date, default: Date.now },
  },
  {
    id: false,
    versionKey: false,
    toJSON: { transform: stripId },
    toObject: { transform: stripId },
  }
);

// Indexes
projectSchema.index({ ownerId: 1, status: 1 });
projectSchema.index({ status: 1, dueDate: 1 });

// Pre-save hook
projectSchema.pre('save', function () {
  this.updatedAt = new Date();
});

// Document type
export type ProjectDocument = Document<unknown, object, IProject> &
  IProject & { _id: Types.ObjectId };

const Project = model<IProject>('Project', projectSchema);
export default Project;
```

## Checklist

After creating a new model:

1. **Create types** in `libs/types/src/lib/{Resource}.ts`
   - Define enum options as `const` arrays
   - Define subdocument types if needed
   - Define main entity type

2. **Export types** from `libs/types/src/index.ts`

3. **Build types library**: `npx tsc -b libs/types/tsconfig.lib.json`

4. **Create model** in `apps/backend/src/models/{Resource}.ts`
   - Import types and enum options from `@{project}/types`
   - Import `generateId` and `stripId` from `./_utils`
   - Create subdocument schemas with `{ _id: false }`
   - Add schema options: `id: false`, `versionKey: false`, transforms
   - Add indexes for common queries
   - Add pre-save hook for `updatedAt`
   - Export document type

5. **Create API schemas** (if needed) in `libs/types/src/api/{resource}.ts` (see backend-route-creation skill)

6. **Create routes** (if needed) in `apps/backend/src/routes/{resource}.ts` (see backend-route-creation skill)
