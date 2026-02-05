---
name: generate-ts-models
description: Generate TypeScript type declarations from OpenAPI/Swagger specification. Use phrases like "Generate TS models", "Create TypeScript interfaces from swagger", "Generate API types", etc.
---

# Generate TypeScript Models

Converts OpenAPI/Swagger schema definitions into TypeScript type declarations (interfaces, types, enums). Supports customizable naming conventions, type mappings, and output formats.

## How It Works

1. Parses the OpenAPI/Swagger specification file (JSON/YAML)
2. Extracts schema definitions from components/definitions
3. Applies type mapping and naming transformations
4. Generates TypeScript declarations (interfaces and enums)
5. Writes the output to the specified file

## Usage

```bash
bash /mnt/skills/user/generate-ts-models/scripts/generate.sh <spec-file> [output-path] [options]
```

**Arguments:**
- `spec-file` - Path to the OpenAPI/Swagger specification file (required)
- `output-path` - Path for the generated TypeScript file or directory (optional, defaults to `api-models.ts`)
- `--output-mode <mode>` - Explicit output mode: `single` (one file), `folder` (one file per model), or `auto` (auto-detect based on path)

**Examples:**

Generate with default settings (single file): 
```bash
bash /mnt/skills/user/generate-ts-models/scripts/generate.sh ./swagger.json
```

Generate to custom single file:
```bash
bash /mnt/skills/user/generate-ts-models/scripts/generate.sh ./swagger.json ./src/types/api.ts
```

Generate to folder (one file per model):
```bash
bash /mnt/skills/user/generate-ts-models/scripts/generate.sh ./swagger.json ./src/types/
```

Generate with explicit folder mode:
```bash
bash /mnt/skills/user/generate-ts-models/scripts/generate.sh ./swagger.json ./src/types/ --output-mode folder
```

Generate single file to directory path (must use explicit mode):
```bash
bash /mnt/skills/user/generate-ts-models/scripts/generate.sh ./swagger.json ./src/types/api.ts --output-mode single
```

## Output

### Single File Mode (default)

```typescript
/**
 * Auto-generated from OpenAPI specification
 * Do not edit manually
 */

/**
 * User information
 */
export interface User {
  /** User unique identifier */
  id: number;
  /** User's email address */
  email: string;
  /** User's full name */
  name?: string;
  /** User account status */
  status: UserStatus;
}

/**
 * User account status
 */
export enum UserStatus {
  Active = "Active",
  Inactive = "Inactive",
  Suspended = "Suspended"
}
```

### Folder Mode

Generates separate files:

**`User.ts`:**
```typescript
/**
 * Auto-generated from OpenAPI specification
 * Do not edit manually
 */

/**
 * User information
 */
export interface User {
  /** User unique identifier */
  id: number;
  /** User's email address */
  email: string;
  /** User's full name */
  name?: string;
  /** User account status */
  status: UserStatus;
}
```

**`UserStatus.ts`:**
```typescript
/**
 * Auto-generated from OpenAPI specification
 * Do not edit manually
 */

/**
 * User account status
 */
export enum UserStatus {
  Active = "Active",
  Inactive = "Inactive",
  Suspended = "Suspended"
}
```

**`index.ts`:** (if `generateIndex` is enabled)
```typescript
export * from './User';
export * from './UserStatus';
```

## Configuration

The behavior can be customized via `config.json`:

```json
{
  "typeMapping": {
    "string": "string",
    "integer": "number",
    "float": "number",
    "boolean": "boolean",
    "array": "Array<{{type}}>",
    "object": "Record<string, any>"
  },
  "formatMapping": {
    "date": "Date",
    "date-time": "Date",
    "uuid": "string",
    "uri": "string",
    "url": "string",
    "email": "string",
    "password": "string",
    "byte": "string",
    "binary": "Blob"
  },
  "naming": {
    "interface": "PascalCase",
    "property": "camelCase",
    "enum": "PascalCase"
  },
  "output": {
    "addWarningHeader": true,
    "mode": "auto",
    "generateIndex": true,
    "fileExtension": ".ts",
    "indexFileName": "index.ts"
  }
}
```

### Type Mapping Options

| OpenAPI Type | Default TS Type |
|--------------|-----------------|
| `string` | `string` |
| `integer` | `number` |
| `float` | `number` |
| `boolean` | `boolean` |
| `array` | `Array<T>` |
| `object` | `Record<string, any>` |

### Format Mapping Options

| OpenAPI Format | Default TS Type |
|----------------|-----------------|
| `date` | `Date` |
| `date-time` | `Date` |
| `uuid` | `string` |
| `uri` | `string` |
| `url` | `string` |
| `email` | `string` |
| `password` | `string` |
| `byte` | `string` |
| `binary` | `Blob` |

### Naming Convention Options

| Option | Values | Description |
|--------|--------|-------------|
| `interface` | `PascalCase` | Interface naming style |
| `property` | `camelCase` | Property naming style |
| `enum` | `PascalCase` | Enum naming style |

### Output Mode Options

| Option | Values | Description |
|--------|--------|-------------|
| `mode` | `"auto"` \| `"single"` \| `"folder"` | Output mode - auto-detect, single file, or one file per model |
| `generateIndex` | `true` \| `false` | Generate index.ts file in folder mode |
| `fileExtension` | `".ts"` | File extension for generated files |
| `indexFileName` | `"index.ts"` | Name of index file in folder mode |

**Output Mode Behavior:**
- `auto`: Automatically detects based on output path - `.ts` extension → single file, directory → folder
- `single`: All models in one TypeScript file (backward compatible)
- `folder`: One TypeScript file per model (interface/enum) with optional index.ts

## Present Results to User

Successfully generated TypeScript models:

**Single File Mode:**
- **Output file**: `./api-models.ts`
- **Interfaces**: 15
- **Enums**: 4
- **Source specification**: swagger.json

**Folder Mode:**
- **Output directory**: `./src/types/`
- **Files generated**: 20 (15 interfaces, 4 enums, 1 index.ts)
- **Interfaces**: 15
- **Enums**: 4
- **Source specification**: swagger.json

The generated types are ready to use in your TypeScript project.

## Troubleshooting

**Error: Failed to parse specification file**
- Ensure the specification file is valid JSON or YAML format
- Check that the file path is correct and accessible
- Verify OpenAPI/Swagger version is supported (2.0 or 3.x)

**Error: No schemas found in specification**
- Check that your spec contains `components/schemas` (OpenAPI 3.x) or `definitions` (Swagger 2.0)
- Some specs use inline schemas instead of named definitions

**Type names conflict or are invalid**
- Adjust the `naming` settings in `config.json` to change naming conventions
- Modify the `typeMapping` and `formatMapping` in `config.json` to customize type conversions
