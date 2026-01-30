---
name: busirocket-tauri
description:
  Tauri-specific standards for desktop apps. Use when creating Tauri commands,
  configuring invoke handler and permissions, and applying Rust layout under
  src-tauri.
metadata:
  author: cristiandeluxe
  version: "1.0.0"
---

# Tauri Standards

Tauri-specific conventions for desktop applications. Builds on `busirocket-rust`
for language and module rules.

## When to Use

Use this skill when:

- Creating or refactoring Tauri commands
- Registering commands in the invoke handler and permissions
- Structuring a Tauri project (src-tauri layout, sql, prompts)

## Non-Negotiables (MUST)

- When creating a Tauri command: (1) create command file, (2) register in invoke
  handler, (3) add to permissions allowlist.
- Rust code lives under `src-tauri/src/`; apply `busirocket-rust` module layout
  there (services, utils, models).
- SQL under `src-tauri/sql/<area>/`, prompts under `src-tauri/prompts/<area>/`.

## Rules

### Project Structure

- `tauri-project-structure` - Where Rust, SQL, and prompts live in a Tauri app

### Tauri Commands

- `tauri-commands-checklist` - Tauri commands checklist (MANDATORY)

## Related Skills

- `busirocket-rust` - Rust language, one-thing-per-file, boundaries, SQL/prompt
  separation
- `busirocket-core-conventions` - General file structure principles

## How to Use

Read the rule files for Tauri-specific steps and paths:

```
rules/tauri-commands-checklist.md
rules/tauri-project-structure.md
```

Apply `busirocket-rust` for all Rust code inside `src-tauri/src/`.
