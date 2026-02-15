---
name: toon
description: Converts JSON to compact TOON format for reduced token usage. Use when inspecting JSON APIs, processing large JSON payloads, or reducing token costs when sending data to LLMs.
---

# TOON CLI

Token-Optimized Object Notation reduces JSON token counts by 30-50%.

## Quick Reference

### Convert JSON to TOON

```bash
# From file
toon data.json -o output.toon

# From stdin (pipe from curl, jq, etc.)
curl -s https://api.example.com/data | npx @toon-format/cli

# With token statistics
toon data.json --stats

# Pipe from jq
jq '.results' data.json | npx @toon-format/cli --stats
```

### Convert TOON to JSON

```bash
# From file
toon data.toon -o output.json

# From stdin
cat data.toon | toon --decode
```

### Common Options

| Option                | Description                             |
| --------------------- | --------------------------------------- | --- |
| `-o, --output <file>` | Output file (stdout if omitted)         |
| `-e, --encode`        | Force encode mode (JSON → TOON)         |
| `-d, --decode`        | Force decode mode (TOON → JSON)         |
| `--stats`             | Show token savings (encode only)        |
| `--delimiter <char>`  | Array delimiter: `,` (default), `\t`, ` | `   |
| `--keyFolding safe`   | Collapse nested objects to dotted paths |
| `--expandPaths safe`  | Expand dotted paths when decoding       |

## Use Cases

### Inspect API Response

```bash
# Quick preview of API data in compact form
curl -s https://api.github.com/users/torvalds | npx @toon-format/cli

# With token count comparison
curl -s https://api.github.com/repos/torvalds/linux | npx @toon-format/cli --stats
```

### Process Large JSON Files

```bash
# Convert large file with streaming (memory efficient)
toon huge-dataset.json -o output.toon

# Check token savings before processing
toon large-api-response.json --stats
```

### Optimize for LLM Context

```bash
# Maximum compression: key folding + tab delimiter
toon data.json --keyFolding safe --delimiter "\t" --stats -o compressed.toon

# Round-trip: encode with folding, decode with expansion
toon input.json --keyFolding safe -o compressed.toon
toon compressed.toon --expandPaths safe -o restored.json
```

### Pipeline Integration

```bash
# Filter with jq, compress with toon
jq '.data.items[:10]' response.json | npx @toon-format/cli > subset.toon

# Fetch, transform, compress
curl -s https://api.example.com/data | jq '.results' | npx @toon-format/cli --stats
```

## Format Overview

TOON uses indentation instead of braces and brackets, with inline arrays and tabular object arrays:

**JSON:**

```json
{
  "user": {
    "id": 123,
    "name": "Ada",
    "tags": ["admin", "ops"]
  },
  "items": [
    { "sku": "A1", "qty": 2, "price": 9.99 },
    { "sku": "B2", "qty": 1, "price": 14.5 }
  ]
}
```

**TOON:**

```yaml
user:
  id: 123
  name: Ada
  tags[2]: admin,ops
items[2]{sku,qty,price}: A1,2,9.99
  B2,1,14.5
```

### Key Features

- **No braces/brackets**: Indentation defines structure
- **Inline primitive arrays**: `tags[2]: admin,ops` instead of `["admin","ops"]`
- **Tabular objects**: Arrays of uniform objects become CSV-like tables
- **Optional key folding**: `data.metadata.items[2]: a,b` instead of nested objects
- **Unquoted strings**: Only quote when necessary (special chars, delimiters)

## Token Savings Example

```bash
$ curl -s https://api.github.com/users/torvalds | npx @toon-format/cli --stats

✔ Encoded stdin → stdout

ℹ Token estimates: ~245 (JSON) → ~156 (TOON)
✔ Saved ~89 tokens (-36.3%)
```

## Related

- [TOON Specification](https://toonformat.dev/reference/spec.html)
- [Interactive Playground](https://toonformat.dev/playground.html)
