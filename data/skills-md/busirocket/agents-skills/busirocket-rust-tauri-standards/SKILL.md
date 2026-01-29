---
name: busirocket-rust-tauri-standards
description:
  Rust and Tauri standards for maintainable desktop apps. Use when writing Rust
  code in Tauri projects, creating Tauri commands, separating SQL/prompts from
  Rust code, and enforcing one-thing-per-file discipline.
metadata:
  author: cristiandeluxe
  version: "1.0.0"
---

# Rust + Tauri Standards

Strict, reusable standards for Rust/Tauri desktop applications.

## When to Use

Use this skill when:

- Writing Rust code in Tauri projects
- Creating new Tauri commands
- Separating SQL queries and prompts from Rust code
- Enforcing one-thing-per-file discipline in Rust modules

## Non-Negotiables (MUST)

- **One public symbol per file** (function / type / trait).
- **No inline SQL strings** in `.rs` files; use dedicated SQL files with
  `include_str!()` (e.g. `src-tauri/sql/<area>/Xxx.sql`).
- **No inline LLM/AI prompts** in `.rs` files; use dedicated prompt files with
  `include_str!()` (e.g. `src-tauri/prompts/<area>/Xxx.prompt`).
- When creating a Tauri command: (1) create command file, (2) register in invoke
  handler, (3) add to permissions allowlist.

## Module Layout

- `src-tauri/src/services/`: external boundaries (IO, DB, network).
- `src-tauri/src/utils/`: pure logic (no IO).
- `src-tauri/src/models/`: domain types (one type per file).
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

### Tauri Commands

- `rust-tauri-commands-checklist` - Tauri commands checklist (MANDATORY)

### Validation

- `rust-validation` - Validation (run checks after changes)

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/rust-one-thing-per-file.md
rules/rust-sql-separation.md
rules/rust-tauri-commands-checklist.md
```

Each rule file contains:

- Brief explanation of why it matters
- Code examples (correct and incorrect patterns)
- Additional context and best practices
