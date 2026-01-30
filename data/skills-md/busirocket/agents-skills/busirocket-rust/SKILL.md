---
name: busirocket-rust
description:
  Rust language and module standards for maintainable codebases. Use when
  writing Rust code, structuring modules, separating SQL/prompts from code, and
  enforcing one-thing-per-file discipline.
metadata:
  author: cristiandeluxe
  version: "1.0.0"
---

# Rust Standards

Strict, reusable standards for Rust codebases (libraries, CLIs, or backend
services).

## When to Use

Use this skill when:

- Writing or refactoring Rust code
- Structuring modules (services, utils, models)
- Separating SQL queries or LLM prompts from Rust code
- Enforcing one-thing-per-file discipline

## Non-Negotiables (MUST)

- **One public symbol per file** (function / type / trait).
- **No inline SQL strings** in `.rs` files; use dedicated SQL files with
  `include_str!()` (e.g. `sql/<area>/Xxx.sql`).
- **No inline LLM/AI prompts** in `.rs` files; use dedicated prompt files with
  `include_str!()` (e.g. `prompts/<area>/Xxx.prompt`).
- Handlers (HTTP, commands, etc.) must be thin: validate, call service, return.

## Module Layout

- `src/services/`: external boundaries (IO, DB, network).
- `src/utils/`: pure logic (no IO).
- `src/models/`: domain types (one type per file).
- No "misc" modules like `helpers.rs` or `common.rs`.

## Rules

### Language & Style

- `rust-language-style` - Language & style (English-only, struct/enum, error
  types)

### One Thing Per File

- `rust-one-thing-per-file` - One thing per file (STRICT)
- `rust-module-manifests` - Module manifests exception (mod.rs)

### Module Layout

- `rust-module-layout` - Module layout (STRICT) - services, utils, models

### SQL Separation

- `rust-sql-separation` - SQL separation (STRICT) - no inline SQL

### Prompt Separation

- `rust-prompt-separation` - Prompt separation (STRICT) - no inline prompts

### Boundaries

- `rust-boundaries` - Boundaries (thin handlers, validate, call service, return)

### Validation

- `rust-validation` - Validation (run checks after changes)

## Related Skills

- `busirocket-core-conventions` - General file structure principles
- `busirocket-tauri` - Tauri-specific layout and commands (when building desktop
  apps)

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/rust-one-thing-per-file.md
rules/rust-sql-separation.md
rules/rust-module-layout.md
```

Each rule file contains:

- Brief explanation of why it matters
- Code examples (correct and incorrect patterns)
- Additional context and best practices
