---
name: huml
description: Write, read, and validate HUML (Human-oriented Markup Language) documents. Use when working with .huml files, converting YAML/JSON/TOML to HUML, creating configuration files in HUML format, or when the user mentions "huml" or asks about human-readable markup alternatives to YAML.
license: MIT
metadata:
  author: arya
  version: "1.0.0"
---

# HUML (Human-oriented Markup Language)

HUML is a strict, unambiguous serialization language similar to YAML but without YAML's quirks and gotchas. It's designed for configuration files and data serialization where human readability matters.

## Core Syntax Rules

### Indentation
- **Strictly 2 spaces** per nesting level (tabs not allowed)
- No trailing spaces (except in multiline strings)

### Keys and Values
- **Single colon `:`** for scalar values (strings, numbers, booleans, null)
- **Double colon `::`** for vectors (lists and dicts)
- Single space required after `:` and `::`

```huml
name: "MyApp"           # scalar - single colon
settings::              # vector - double colon
  debug: true
```

### Strings
- **Must be double-quoted** (no barewords like YAML)
- Escape `\` and `"` with backslash
- Multi-line strings use triple quotes `"""`

```huml
simple: "hello world"
escaped: "path\\to\\file"
multiline: """
  Line one
  Line two
"""
```

### Numbers
```huml
integer: 42
float: 3.14
scientific: 1.5e-3
hex: 0x1A
binary: 0b1010
special: inf, -inf, nan
```

### Booleans and Null
```huml
enabled: true
disabled: false
empty: null
```

### Lists
```huml
# Inline
tags:: "web", "api", "v2"

# Multiline
items::
  - "first"
  - "second"

# Empty
empty:: []
```

### Dicts
```huml
# Inline (scalars only)
point:: x: 1, y: 2

# Multiline (supports nesting)
database::
  host: "localhost"
  port: 5432

# Empty
empty:: {}
```

### Comments
```huml
# Comment (space after # required)
key: "value"  # inline comment
```

### Version Directive (Optional)
```huml
%HUML v0.2.0
```

## Quick Reference

| Feature | HUML Syntax |
|---------|-------------|
| String | `"quoted"` |
| Number | `42`, `3.14`, `0xFF` |
| Boolean | `true`, `false` |
| Null | `null` |
| Scalar key | `key: value` |
| Vector key | `key:: items` |
| List item | `- item` |
| Comment | `# text` |

## Common Patterns

### Configuration File
```huml
%HUML v0.2.0

app::
  name: "MyService"
  port: 8080
  debug: false

database::
  host: "localhost"
  credentials::
    user: "admin"
    pass: "secret"
```

### List of Objects
```huml
servers::
  - name: "web1"
    host: "10.0.0.1"
    port: 80
  - name: "web2"
    host: "10.0.0.2"
    port: 80
```

## Validation

Use the bundled validation script to check HUML syntax and convert to JSON:

```bash
node scripts/validate.mjs path/to/file.huml
```

On success, outputs the parsed JSON. On failure, shows detailed error message.

**Requirements:** Node.js with `@huml-lang/huml` package installed.

## Full Specification

See `references/spec.md` for the complete v0.2.0 specification including:
- All number formats and escape sequences
- Multiline string indentation rules
- Key naming rules
- Edge cases and formatting details

## Resources

- Official site: https://huml.io
- Playground: https://huml.io/playground
- npm package: `@huml-lang/huml`
