---
name: quicktype
description: Generate TypeScript types from JSON files using quicktype CLI. Use when user wants to create types/interfaces from JSON data, API responses, or config files.
---

# Quicktype - JSON to Type Generator

Generate strongly-typed interfaces from JSON files or URLs.

## When to Use

- User asks to generate types from JSON
- User wants TypeScript interfaces for API responses
- User needs type definitions for config files
- User mentions "quicktype" or "json to types"

## Instructions

1. Parse the input to identify:
   - File path or URL
   - Target language (default: TypeScript)
   - Output file (optional)

2. Run the quicktype script:

```bash
python3 ~/.claude/skills/quicktype/scripts/quicktype.py <file> [--lang LANG] [--out FILE]
```

3. Display the generated types in a fenced code block

4. If `--out` specified, save to that file

## Supported Languages

| Flag     | Language          |
| -------- | ----------------- |
| `ts`     | TypeScript        |
| `go`     | Go structs        |
| `py`     | Python dataclass  |
| `rs`     | Rust structs      |
| `swift`  | Swift Codable     |
| `kotlin` | Kotlin data class |

## Examples

**Input:** `/quicktype api/users.json`
**Output:** TypeScript interfaces for the JSON structure

**Input:** `/quicktype config.json --lang go`
**Output:** Go struct definitions

**Input:** `/quicktype response.json --out src/types/api.ts`
**Output:** Types saved to specified file
