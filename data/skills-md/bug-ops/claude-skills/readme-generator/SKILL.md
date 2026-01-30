---
name: readme-generator
description: "Generate and improve README files for software projects. Triggers on: 'create readme', 'generate readme', 'write readme', 'improve readme', 'update readme', 'fix readme', 'readme for this project'. Supports Rust (libraries, CLI tools, services), TypeScript/JavaScript (npm packages), and Python (PyPI packages). Applies ecosystem-specific conventions: badges, installation sections, MSRV for Rust, feature flags documentation."
---

# README Generator

Generate professional README files or improve existing ones. Applies ecosystem-specific best practices from 90+ curated examples.

> [!IMPORTANT]
> Always detect project type FIRST before generating. Wrong template = wrong conventions.

## Quick Reference

| Project Type | Detection | Key Requirements |
|-------------|-----------|------------------|
| Rust library | `Cargo.toml` + `src/lib.rs` | crates.io badge, docs.rs, MSRV, feature flags |
| Rust CLI | `Cargo.toml` + `src/main.rs` | Multi-platform install (cargo, brew, apt, etc.) |
| TypeScript | `package.json` + `tsconfig.json` | npm/yarn/pnpm/bun tabs, bundle size badge |
| Python | `pyproject.toml` or `setup.py` | pip/poetry/conda, Python versions badge |

## GitHub Callouts

> [!IMPORTANT]
> Use GitHub callouts in generated READMEs to highlight critical information. They render beautifully on GitHub.

### Callout Types

Use these callout blocks in generated README files:

```markdown
> [!NOTE]
> Useful information that users should know, even when skimming content.

> [!TIP]
> Helpful advice for doing things better or more easily.

> [!IMPORTANT]
> Key information users need to know to achieve their goal.

> [!WARNING]
> Urgent info that needs immediate user attention to avoid problems.

> [!CAUTION]
> Advises about risks or negative outcomes of certain actions.
```

### When to Use Each Callout

| Callout | Use For | Example |
|---------|---------|---------|
| `[!NOTE]` | Additional context, FYI | "This crate re-exports types from X" |
| `[!TIP]` | Best practices, recommendations | "Use `--release` for production builds" |
| `[!IMPORTANT]` | Breaking changes, requirements | "Requires Rust 1.70+" |
| `[!WARNING]` | Potential issues, deprecations | "This API will change in v2.0" |
| `[!CAUTION]` | Dangerous operations, data loss | "This command deletes all data" |

### Callout Placement in README

Place callouts strategically:

1. **After Installation** — compatibility warnings, system requirements
2. **In Usage section** — tips for common patterns, important gotchas  
3. **Before Breaking Changes** — migration notes, deprecation warnings
4. **In Configuration** — dangerous options, security considerations

### Examples in Generated READMEs

**Rust library with MSRV:**

```markdown
## Installation

\`\`\`toml
[dependencies]
my-crate = "1.0"
\`\`\`

> [!IMPORTANT]
> Requires Rust 1.70 or later. See [MSRV policy](#msrv-policy).
```

**CLI tool with destructive command:**

```markdown
## Usage

\`\`\`bash
my-tool clean --all
\`\`\`

> [!CAUTION]
> The `--all` flag removes ALL cached data including user preferences. This cannot be undone.
```

**Library with async feature:**

```markdown
## Features

> [!TIP]
> Enable the `async` feature for non-blocking I/O. Recommended for high-throughput applications.

\`\`\`toml
my-crate = { version = "1.0", features = ["async"] }
\`\`\`
```

**Python package with version requirement:**

```markdown
## Installation

\`\`\`bash
pip install my-package
\`\`\`

> [!WARNING]
> Python 3.8 reaches end-of-life in October 2024. Consider upgrading to Python 3.10+.
```

## Workflow

### 1. Detect Project Type

```bash
# Check for project markers
ls -la Cargo.toml package.json pyproject.toml setup.py tsconfig.json 2>/dev/null
```

Decision tree:

- `Cargo.toml` exists → Rust project
  - Has `[[bin]]` or `src/main.rs` → CLI tool (use `references/rust-cli.md`)
  - Otherwise → Library (use `references/rust-library.md`)
- `package.json` exists → JavaScript/TypeScript
  - `tsconfig.json` exists → TypeScript (use `references/typescript.md`)
  - Otherwise → JavaScript (use `references/typescript.md`)
- `pyproject.toml` or `setup.py` → Python (use `references/python.md`)

### 2. Gather Project Context

> [!TIP]
> Extract metadata from project files — don't ask the user for info that's already in Cargo.toml/package.json.

Extract from project files:

**Rust:**

```bash
# Get package info
grep -E "^name|^version|^description|^license|^rust-version" Cargo.toml
# Get features
grep -A 50 "^\[features\]" Cargo.toml | head -50
# Check for binary
grep -E "^\[\[bin\]\]" Cargo.toml || ls src/main.rs 2>/dev/null
```

**TypeScript/JavaScript:**

```bash
# Get package info
cat package.json | jq '{name, version, description, license, keywords}'
# Check for types
ls src/*.ts tsconfig.json 2>/dev/null
```

**Python:**

```bash
# From pyproject.toml
grep -E "^name|^version|^description|^license" pyproject.toml
# Or from setup.py
grep -E "name=|version=|description=" setup.py
```

### 3. Load Template

After detecting project type, read the appropriate reference file:

- Rust library → Read `references/rust-library.md`
- Rust CLI → Read `references/rust-cli.md`
- TypeScript/JavaScript → Read `references/typescript.md`
- Python → Read `references/python.md`

### 4. Generate README

> [!WARNING]
> Never use placeholder text like `[TODO]` or `<description>` in final output. Extract real values or ask user.

Apply the template structure. Essential sections in order:

1. **Hero section** (required)
   - Project name as H1
   - One-line description (from package metadata)
   - Badge row (ecosystem-specific)

2. **Visual hook** (highly recommended)
   - GIF/screenshot demo if exists in `assets/`, `docs/`, or `images/`
   - Terminal recording for CLI tools

3. **Installation** (required)
   - Ecosystem-appropriate commands
   - Multiple package managers for CLI tools

4. **Usage/Examples** (required)
   - Runnable code snippets
   - Common use cases

5. **Features** (recommended)
   - Bullet list of key capabilities

6. **API/Configuration** (if applicable)
   - For libraries: key types and functions
   - For CLI: command-line arguments
   - For services: environment variables

7. **Contributing** (recommended)
   - Link to CONTRIBUTING.md if exists
   - Basic guidelines otherwise

8. **License** (required)
   - License name with link to LICENSE file

### 5. Improve Existing README

> [!NOTE]
> When improving, preserve existing custom sections and contribution acknowledgments. Don't overwrite user's content.

When improving an existing README:

1. **Audit current state:**

   ```bash
   cat README.md
   ```

2. **Check against requirements:**
   - Missing essential sections?
   - Outdated badges?
   - No code examples?
   - Wall of text without structure?

3. **Common improvements:**
   - Add missing badges
   - Add installation section if missing
   - Add usage examples if missing
   - Break up long paragraphs
   - Add table of contents if >500 words
   - Update outdated version numbers

4. **Preserve existing content:**
   - Keep custom sections
   - Maintain existing links
   - Preserve contribution history acknowledgments

## Badge Reference

See `references/badges.md` for complete badge syntax by ecosystem.

Quick reference:

```markdown
<!-- Rust -->
[![Crates.io](https://img.shields.io/crates/v/CRATE)](https://crates.io/crates/CRATE)
[![docs.rs](https://img.shields.io/docsrs/CRATE)](https://docs.rs/CRATE)

<!-- TypeScript/npm -->
[![npm](https://img.shields.io/npm/v/PACKAGE)](https://www.npmjs.com/package/PACKAGE)
[![Bundle Size](https://img.shields.io/bundlephobia/minzip/PACKAGE)](https://bundlephobia.com/package/PACKAGE)

<!-- Python -->
[![PyPI](https://img.shields.io/pypi/v/PACKAGE)](https://pypi.org/project/PACKAGE)
[![Python](https://img.shields.io/pypi/pyversions/PACKAGE)](https://pypi.org/project/PACKAGE)
```

## Quality Checklist

Before completing, verify:

- [ ] One-line description is clear and specific
- [ ] Badges are valid and ecosystem-appropriate
- [ ] Installation commands are copy-pasteable
- [ ] At least one runnable code example
- [ ] License is specified
- [ ] No broken links
- [ ] No placeholder text remaining
- [ ] **Callouts used for warnings, tips, and important notes**
- [ ] Callouts placed after relevant sections (not floating)

## Anti-patterns to Avoid

> [!CAUTION]
> These mistakes make READMEs significantly worse. Check against this list before completing.

- Wall of text without headers
- Generic descriptions ("A tool for doing things")
- Missing installation section
- No code examples
- Outdated badges/version numbers
- Excessive badges (>6 is usually too many)
- TOC for short READMEs (<300 words)
