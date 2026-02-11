---
name: openharmony-cpp
description: Expert coding guide for OpenHarmony C++ development. Use this skill when writing, refactoring, or reviewing C++ code for OpenHarmony projects. It enforces strict project-specific conventions (naming, formatting, headers) and critical security requirements (input validation, memory safety).
---

# OpenHarmony C++ Coding Skills

## Core Mandates (Common Pitfalls)

These rules are strictly enforced in OpenHarmony and often differ from general C++ projects.

### 1. Strict Naming & Formatting
- **Extensions:** Always use `.cpp` and `.h`.
- **Files:** Filenames **must** match class names (Unix-like, e.g., `my_class.cpp`).
- **Variables:** Global vars must start with `g_` (e.g., `g_config`). Class members must end with `_` (e.g., `value_`).
- **Braces:** **K&R Style** is mandatory (opening brace on the same line).
- **Details:** See [naming_formatting.md](references/naming_formatting.md).

### 2. Header Management
- **Guards:** Use `#ifndef` guards. **#pragma once is FORBIDDEN.**
- **Includes:** Prefer `#include` over forward declarations to prevent hidden dependencies.
- **Details:** See [headers_scopes.md](references/headers_scopes.md).

### 3. Critical Security Requirements
- **Input Validation:** All external data must be validated before use (indices, sizes, loops).
- **Memory Safety:** Pointers must be set to `nullptr` **immediately** after deletion.
- **Bitwise:** Only on **unsigned** types.
- **Details:** See [secure_coding.md](references/secure_coding.md).

## Usage Guide

### When to use
- **New Code:** Generating new classes or modules.
- **Refactoring:** Cleaning up legacy code.
- **Review:** Checking code against OpenHarmony standards.

### Reference Map
- **[naming_formatting.md](references/naming_formatting.md)**: Naming conventions (g_, _), braces (K&R), line length.
- **[secure_coding.md](references/secure_coding.md)**: Input validation, integer safety, memory management, prohibited functions.
- **[class_function_design.md](references/class_function_design.md)**: Constructors, inheritance, modern C++ (nullptr, const), function size.
- **[headers_scopes.md](references/headers_scopes.md)**: Header guards, namespaces, include rules.
