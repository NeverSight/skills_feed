---
name: materal-enum-adapter
description: "Fetches Materal Framework enum data from API for TypeScript enum generation. Use when: (1) Working with Materal Framework OpenAPI specs, (2) Need real enum values from API (not schema-only), (3) Generating TypeScript enums with Chinese-to-English translations via AI."
---

# Materal Framework Enum Adapter

Detects Materal Framework's enum endpoints and fetches real enum data from the API for efficient enum generation.

## How It Works

Two-command workflow for fast, batch-style enum generation:

**fetch** - Get enum data from API
1. Parse OpenAPI spec for `Enums/GetAll*` endpoints (auto-detects namespace)
2. Extract enum names from endpoint paths
3. Fetch `{Key, Value}` pairs from Materal API (Chinese values)
4. Output JSON for AI batch translation

**generate** - Generate TypeScript files
1. Read AI-translated enum data (with English names)
2. Validate data structure
3. Generate TypeScript enum files (one per enum, overwrites existing)
4. **Note**: Does NOT generate `index.ts` - already exists from `generate-ts-models`

## Namespace Detection

Auto-detects namespace prefix from first enum endpoint:

| Endpoint Pattern | Detected Namespace | API URL Example |
|-----------------|-------------------|-----------------|
| `/MainAPI/Enums/GetAllRole` | `/MainAPI` | `{base-url}/MainAPI/Enums/GetAllRole` |
| `/GatewayAPI/Enums/GetAllStatus` | `/GatewayAPI` | `{base-url}/GatewayAPI/Enums/GetAllStatus` |
| `/Enums/GetAllType` | `(empty)` | `{base-url}/Enums/GetAllType` |

## Usage

### Fetch enum data from API

```bash
node skills/materal-enum-adapter/scripts/adapter.js <spec-file> --base-url <url> fetch
```

**Arguments:**
- `spec-file` - Path to OpenAPI JSON
- `--base-url` - Materal API base URL

**Example:**
```bash
node skills/materal-enum-adapter/scripts/adapter.js openapi.json --base-url http://localhost:5000 fetch
```

### Generate TypeScript files

```bash
node skills/materal-enum-adapter/scripts/adapter.js <translation-file> [--output-dir <dir>] generate
```

**Arguments:**
- `translation-file` - Path to AI-translated JSON file
- `--output-dir <dir>` - Output directory (default: `./src/enums`)

**Example:**
```bash
node skills/materal-enum-adapter/scripts/adapter.js translations.json --output-dir ./src/types generate
```

## Output Format

### fetch output (for AI translation)

```json
{
  "success": true,
  "detected": true,
  "enums": ["Role", "Status"],
  "enumsSkipped": 0,
  "enumData": [
    {
      "name": "Role",
      "description": "角色",
      "values": [
        {"key": 0, "value": "管理员"},
        {"key": 1, "value": "用户"}
      ]
    }
  ]
}
```

**Fields:**
- `success` - Operation completed successfully
- `detected` - Materal Framework enum controller found
- `enums` - Successfully fetched enum names
- `enumsSkipped` - Number of failed fetches
- `enumData[].name` - Enum name (PascalCase)
- `enumData[].description` - Enum description
- `enumData[].values[].key` - Enum key (number or string)
- `enumData[].values[].value` - Original Chinese value

### generate input (AI creates this)

Transform fetch output by replacing `value` with `englishName`:

```json
{
  "enumData": [
    {
      "name": "Role",
      "values": [
        {"key": 0, "englishName": "Administrator", "originalValue": "管理员"},
        {"key": 1, "englishName": "User", "originalValue": "用户"}
      ]
    }
  ]
}
```

**Required fields:**
- `enumData[].name` - Enum name (PascalCase)
- `enumData[].values[].key` - Enum key (number or string)
- `enumData[].values[].englishName` - English name (PascalCase)
- `enumData[].values[].originalValue` - Original Chinese value (optional)

### generate output (summary)

```json
{
  "success": true,
  "generated": 2,
  "enums": ["Role", "Status"],
  "outputDir": "./src/enums"
}
```

**Generated files:**
```
src/enums/
├── Role.ts
└── Status.ts
```

**Role.ts:**
```typescript
export enum Role {
  Administrator = 0,
  User = 1
}
```

**Note**: `index.ts` is NOT generated - it already exists from `generate-ts-models` workflow. This skill only overwrites individual enum files with translated values.

**Important**: Ensure `--output-dir` matches the directory used by `generate-ts-models` (default: `./types`).

## Workflow Example

```bash
# Step 1: Generate base models (includes enums + index.ts)
node skills/generate-ts-models/scripts/generate.js openapi.json ./src/types

# Step 2: Fetch real enum values from API
node skills/materal-enum-adapter/scripts/adapter.js openapi.json --base-url http://localhost:5000 fetch > raw.json

# Step 3: AI translates values (batch - single API call)
# Creates translations.json with englishName field

# Step 4: Generate translated enum files (overwrites only enum files)
node skills/materal-enum-adapter/scripts/adapter.js translations.json --output-dir ./src/types generate
```

**Final output:**
```
src/types/
├── User.ts              # from generate-ts-models
├── Role.ts              # from generate-ts-models, overwritten by materal-enum-adapter
├── index.ts             # from generate-ts-models (not regenerated)
```

**Performance**: 10-50x faster than AI generating files individually (single translation batch + instant file generation).

## Requirements

- OpenAPI spec with `Enums/GetAll*` endpoints (any namespace prefix)
- Materal API running at `--base-url`
- Network access to API

## Error Handling

### Common errors

| Command | Error | Cause | Action |
|---------|--------|--------|--------|
| fetch | `Cannot read spec file` | Invalid JSON or wrong path | Check file path and JSON validity |
| fetch | `No Materal Framework Enums controller detected` | No enum endpoints in spec | Verify spec format |
| fetch | `Failed to fetch Role enum after 3 retries` | API unreachable | Check API availability and network |
| generate | `Failed to read or parse translation file` | Invalid JSON | Check file path and JSON validity |
| generate | `Invalid translation data: missing or invalid enumData array` | Missing enumData | Verify JSON structure |
| generate | `Invalid value in Role: missing key or englishName` | Missing required fields | Check all values have key and englishName |

**Error codes**: All errors exit with code 1.
