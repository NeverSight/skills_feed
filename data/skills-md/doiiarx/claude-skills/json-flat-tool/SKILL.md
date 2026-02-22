---
name: json-flat-tool
description: "JSON flat view, schema inference, and edit tool. Use when the user provides a JSON file or data and wants to explore its structure, infer its schema, or modify fields. Triggers on: view json, edit json, json schema, json structure, set json field, jstool, analyze json, flat view, orderbook, json flat."
---

# JSON Flat Tool

A single-script tool (`jstool.py`) for viewing, inspecting, and editing JSON data.

Script path: `~/.claude/skills/json-flat-tool/jstool.py`

## Invocation

```bash
python3 ~/.claude/skills/json-flat-tool/jstool.py <command> [args]
```

## Commands

| Command | Description |
|---------|-------------|
| `view [file] [opts]` | Flat path/type/value display |
| `schema [file] [--title T]` | Infer JSON Schema Draft 7 |
| `set <path> <value> [file] [-f]` | Set a field value |
| `<path> = <value> [file] [-f]` | Same, B-style syntax |
| `before <path> <value> [file] [-f]` | Insert before array element |
| `after <path> <value> [file] [-f]` | Insert after array element |
| `del <path> [file] [-f]` | Delete a key or element |
| `set-null <path> [file] [-f]` | Set a field to null |
| `copy <src> <dst> [file] [-f]` | Deep-clone a subtree to a new path |
| `merge <path> <patch.json> [file] [-f]` | Deep-merge a JSON file into a path |
| `find <pattern> [file] [opts]` | Search paths and values by regex or glob |

Omit `[file]` to read from stdin.

## view Options

| Flag | Unit | Description |
|------|------|-------------|
| `-s` | — | Schema mode: collapse `[N]→[*]`, deduplicate, hide values |
| `-F <path>` | — | Filter: show only this path and its children |
| `-n <N>` | rows | Show at most N rows |
| `-O <N>` | rows | Skip first N rows |
| `-E <N>` | elements | Skip first N array elements (use with `-F`) |
| `-L <N>` | elements | Show at most N array elements (use with `-F`) |
| `-d <N>` | depth | Collapse containers deeper than N levels (object key depth; array indices don't count) |

`-E` and `-L` are element-aware and never cut an element in the middle.

## Edit flags

- `-f` — Force: apply change to file. Default is **preview-only**.
- Without `-f`: shows a color-annotated diff of the original JSON with `~~~~~` underline markers at the exact change position.

## Path syntax

```
root              root node
count             root-level key
users[0]          array element
users[0].name     nested key
root[0].key       root-array element key
```

## Value parsing

Values are parsed as JSON first, then fall back to plain string:

```
Alice          → string
42             → integer
3.14           → number
true / false   → boolean
null           → null
'{"k":"v"}'    → object
'[1,2,3]'      → array
@path/to.json  → read value from file
```

## Output format (view)

```
root object
users array
users[0] object
users[0].name string Alice
users[0].age integer 30
users[1].age integer (null)    ← magenta: null with inferred type
orphan unknown (null)          ← red: null, type unknown
meta object (empty)            ← dim: empty container
config object {3 keys}         ← dim: collapsed by -d
tags array [12 items]          ← dim: collapsed by -d
```

Colors: cyan = path, yellow = type, green = value,
        magenta = inferred null, red = unknown/delete, dim = empty/collapsed.

## Workflow

### Explore a JSON file

```bash
# Quick structure overview
python3 ~/.claude/skills/json-flat-tool/jstool.py view data.json -s

# Filter to a nested array, element-aware pagination
python3 ~/.claude/skills/json-flat-tool/jstool.py view data.json -F "data[0].bids" -E 5 -L 3

# Infer JSON Schema Draft 7
python3 ~/.claude/skills/json-flat-tool/jstool.py schema data.json --title "My API"

# Depth-limited view: collapse containers beyond 2 key levels
python3 ~/.claude/skills/json-flat-tool/jstool.py view data.json -d 2

# Combine with filter: expand just one branch while keeping others collapsed
python3 ~/.claude/skills/json-flat-tool/jstool.py view data.json -d 1 -F users
```

### Edit a JSON file

```bash
# Preview change (default)
python3 ~/.claude/skills/json-flat-tool/jstool.py set users[0].name Bob data.json

# Apply change
python3 ~/.claude/skills/json-flat-tool/jstool.py set users[0].name Bob data.json -f

# B-style
python3 ~/.claude/skills/json-flat-tool/jstool.py "users[0].name" = Bob data.json -f

# Insert / delete
python3 ~/.claude/skills/json-flat-tool/jstool.py before users[1] '{"name":"Eve"}' data.json -f
python3 ~/.claude/skills/json-flat-tool/jstool.py del users[2] data.json -f
python3 ~/.claude/skills/json-flat-tool/jstool.py set-null users[0].age data.json -f
```

### Set value from file (`@file`)

```bash
# Write a complex object to a file, then set it at a path
python3 ~/.claude/skills/json-flat-tool/jstool.py set provider.openai @/tmp/openai.json config.json -f
```

### Clone a subtree (`copy`)

```bash
# Clone an existing model as the base for a new one (preview)
python3 ~/.claude/skills/json-flat-tool/jstool.py copy \
  provider.google.models.antigravity-gemini-3-pro \
  provider.google.models.my-new-model \
  config.json

# Apply
python3 ~/.claude/skills/json-flat-tool/jstool.py copy \
  provider.google.models.antigravity-gemini-3-pro \
  provider.google.models.my-new-model \
  config.json -f
```

### Deep-merge a patch file (`merge`)

```bash
# patch.json only needs to contain the fields to add/update
# preview: shows which keys are added (+) and updated (~)
python3 ~/.claude/skills/json-flat-tool/jstool.py merge provider.google.models /tmp/new-models.json config.json

# Apply
python3 ~/.claude/skills/json-flat-tool/jstool.py merge provider.google.models /tmp/new-models.json config.json -f
```

### Find nodes by pattern (`find`)

```bash
# Regex search in both paths and values (default)
python3 ~/.claude/skills/json-flat-tool/jstool.py find apiKey config.json

# Search path only (-k), value only (-v)
python3 ~/.claude/skills/json-flat-tool/jstool.py find apiKey config.json -k
python3 ~/.claude/skills/json-flat-tool/jstool.py find "sk-.*" config.json -v

# Case-insensitive
python3 ~/.claude/skills/json-flat-tool/jstool.py find "APIKEY" config.json -k -i

# Glob mode (full-string wildcard, use * to match anywhere)
python3 ~/.claude/skills/json-flat-tool/jstool.py find "*api*" config.json -k -g -i
```

**find options**:

| Flag | Description |
|------|-------------|
| `-k` | Match path only |
| `-v` | Match value only |
| `-i` | Case-insensitive |
| `-g` | Glob mode (fnmatch full-string wildcard instead of regex) |

`-k` and `-v` are mutually exclusive. Without either flag, both path and value are searched.

### Inline / piped JSON

```bash
echo '{"name":"Alice"}' | python3 ~/.claude/skills/json-flat-tool/jstool.py view
curl https://api.example.com/data | python3 ~/.claude/skills/json-flat-tool/jstool.py schema
```

## Notes

- `before` / `after` only apply to **array elements**, not object keys.
- To add a new key to an object, use `set`.
- `-f` without a file path prints modified JSON to stdout.
- `-E` / `-L` require `-F` pointing to an array path.
- Array sampling for schema inference: up to 20 elements.
- `required` in schema = fields present and non-empty in all sampled elements.
- `@file` syntax works with `set` and B-style (`=`); `merge` always takes a file path directly.
- `copy` performs a deep clone — mutations to the copy do not affect the source.
- `merge` for non-dict targets replaces the value entirely (patch wins).
- `find -g` uses `fnmatch` (full-string wildcard): use `*api*` not `api*` for substring matching.
- `find` without `-g` uses Python `re.search` (substring regex by default).
- `-d N` only affects the flat view display; schema inference and edit commands are unaffected.
- `-d N` depth counts object key traversals only — array indices (`[0]`, `[1]`, …) do not increment depth.
