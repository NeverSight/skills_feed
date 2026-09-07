---
name: gitignore
description: >-
  Manage and generate .gitignore files using the official GitHub gitignore template library via the `ign` CLI.
  Use when initializing new project repositories, automatically detecting project stack from files, adding
  language/framework/IDE ignore rules, inspecting applied templates, or safely modifying existing .gitignore files.
---

# Gitignore Management Skill (`ign`)

`ign` (GitHub Gitignore CLI) is a high-performance, explicitly managed, and Agent-friendly `.gitignore` manager built with Rust. Powered by the official [github/gitignore](https://github.com/github/gitignore) repository, it provides modular block-isolated merging, context-aware template detection, smart aliases, fuzzy search, and guaranteed preservation of custom user-defined rules. It operates completely offline by default with zero hidden network requests, synchronizing templates on-demand via explicit commands.

---

## 1. Prerequisites & Installation

Before performing any `.gitignore` operations, the Agent should verify installation and initialization in sequence:

### 1.1 Verify and Install the CLI Tool
```bash
command -v ign >/dev/null 2>&1 || cargo install ign
```

### 1.2 Verify and Initialize the Template Library
Check if `~/.config/ign/templates` is initialized. If not ready, clone the official template repository:
```bash
ign template status >/dev/null 2>&1 || ign template init
```

---

## 2. Context-Aware Template Selection

When configuring `.gitignore` for a project, the Agent should first **inspect the workspace context** (project markers, build files, OS, and IDE configuration) to automatically select and combine matching templates:

### 2.1 Language & Tech Stack Mapping

| Project Marker / Directory | Recommended Template | Description |
|---|---|---|
| `Cargo.toml`, `Cargo.lock` | `Rust` | Rust build artifacts (`target/`) and backups |
| `package.json`, `pnpm-lock.yaml`, `yarn.lock` | `Node` | Node.js / Web frontend dependencies and build outputs |
| `pyproject.toml`, `requirements.txt`, `Pipfile` | `Python` | Python virtual environments and `__pycache__/` |
| `go.mod`, `go.sum` | `Go` | Go binaries and vendor directories |
| `pom.xml` | `Java`, `Maven` | Java Maven projects |
| `build.gradle`, `build.gradle.kts`, `gradlew` | `Java`, `Gradle` | Gradle / Kotlin / Android projects |
| `composer.json` | `PHP` | PHP Composer dependencies |
| `Gemfile` | `Ruby` | Ruby / Rails dependencies and logs |
| `pubspec.yaml` | `Dart`, `Flutter` | Dart / Flutter cross-platform projects |
| `CMakeLists.txt`, `Makefile` | `C++` or `C` | C / C++ build outputs |
| `deno.json`, `deno.jsonc` | `Deno` | Deno cache and build artifacts |
| `mix.exs` | `Elixir` | Elixir / Phoenix projects |
| `*.sln`, `*.csproj` | `VisualStudio` | .NET / C# solutions |

### 2.2 Operating System & IDE Templates

- **Operating System (add based on current execution environment)**:
  - Linux: `Linux` (maps to `Global/Linux`)
  - macOS: `macOS` (maps to `Global/macOS`)
  - Windows: `Windows` (maps to `Global/Windows`)
- **Developer Tools / IDE (add based on workspace settings or user preference)**:
  - VS Code: `Visual_Studio_Code` (alias `vscode`, maps to `Global/VisualStudioCode`)
  - JetBrains (IDEA/CLion/RustRover/PyCharm/GoLand): `JetBrains` (alias `idea`, maps to `Global/JetBrains`)

### 2.3 Agent Automated Decision Examples

```bash
# Example: Rust project detected on Linux with VS Code and JetBrains IDEs
ign init Rust macOS Linux JetBrains Visual_Studio_Code

# Example: Frontend Node.js project detected
ign init Node macOS Linux Visual_Studio_Code
```

---

## 3. Usage & Commands

### 3.1 Initialize Project `.gitignore` (`init`)
- **Initialize with explicitly specified templates**:
  ```bash
  ign init Rust macOS JetBrains Visual_Studio_Code
  ```
- **Interactive multi-select selection**:
  ```bash
  ign init -i
  ```
- **Re-initialize existing file while preserving manual custom rules**:
  ```bash
  ign init Rust macOS
  ```

### 3.2 Append & Update Templates (`add`)
Safely append new language or tool templates into an existing `.gitignore` (auto-deduplicated, preserving custom rules):
```bash
ign add Linux Python
```

### 3.3 Inspect & Audit Applied Templates (`status`)
Inspect metadata of the current repository's `.gitignore` (applied templates, timestamps, custom rules):
```bash
# Human-readable terminal output
ign status

# Structured JSON output for Agent/CI consumption
ign status --json
```

**JSON Output Schema**:
```json
{
  "file_exists": true,
  "path": ".gitignore",
  "managed_by_ign": true,
  "templates_count": 4,
  "templates": [
    "Rust",
    "Global/macOS",
    "Global/JetBrains",
    "Global/VisualStudioCode"
  ],
  "created_at": "2026-08-29T04:33:10Z",
  "updated_at": "2026-08-29T04:33:21Z",
  "has_custom_rules": true,
  "custom_rules_lines": 2,
  "custom_rules": "# Custom user rule\nscratch/",
  "total_lines": 220
}
```

### 3.4 Remove Specified Templates (`remove`)
Remove templates from `.gitignore` while keeping remaining templates and custom rules intact:
```bash
ign remove Global/macOS
# Or using smart alias:
ign remove macos
```

### 3.5 Search & Explore Templates (`search` / `list` / `show`)
```bash
# Fuzzy search templates
ign search elixir
ign search jetbrains --json

# View raw template contents
ign show Rust

# List all templates in a category
ign list -c global
```

### 3.6 Local Template Repository Maintenance (`template`)
```bash
# Inspect local template library status and directory path
ign template status
ign template path

# Manually pull latest templates from GitHub
ign template update
# (Top-level shorthand: ign update)
```

---

## 4. Environment Variables

- **Default template storage path**: `~/.config/ign/templates`
- **Custom storage path override**: `export IGN_TEMPLATES_DIR="/path/to/custom/gitignore-repo"`

