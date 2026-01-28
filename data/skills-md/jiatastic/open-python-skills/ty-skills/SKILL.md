---
name: ty-skills
description: >
  Python type checking expertise using ty - the extremely fast type checker by Astral.
  Use when: (1) Adding type annotations to Python code, (2) Fixing type errors reported by ty,
  (3) Migrating from mypy/pyright to ty, (4) Configuring ty for projects,
  (5) Understanding advanced type patterns (generics, protocols, intersection types),
  (6) Setting up ty in editors (VS Code, Cursor, Neovim, PyCharm).
---

# ty-skills

Master Python type checking with [ty](https://docs.astral.sh/ty/) - the extremely fast type checker written in Rust by Astral (creators of uv and Ruff).

## When to Use This Skill

- Adding type annotations to Python code
- Fixing type errors and diagnostics from ty
- Configuring ty rules and severity levels
- Migrating from mypy or pyright to ty
- Understanding advanced type patterns (intersection types, protocols, generics)
- Setting up ty language server in your editor

## Quick Start

```bash
# Install
uv tool install ty
# or: pip install ty

# Check current directory
ty check

# Check specific files
ty check src/

# Full diagnostics
ty check --output-format full
```

## Configuration

Configure via `pyproject.toml`:

```toml
[tool.ty.environment]
python-version = "3.12"
python = "./.venv"
python-platform = "linux"
root = ["./src"]
extra-paths = ["./typings"]

[tool.ty.rules]
# error: fail CI, warn: report, ignore: disable
possibly-unresolved-reference = "error"
invalid-argument-type = "error"
division-by-zero = "warn"
unused-ignore-comment = "warn"

[tool.ty.src]
include = ["src", "tests"]
exclude = ["src/migrations/"]

# Per-file overrides
[[tool.ty.overrides]]
include = ["tests/**"]

[tool.ty.overrides.rules]
possibly-unresolved-reference = "warn"
```

## Rules Quick Reference

| Rule | Default | Description |
|------|---------|-------------|
| `possibly-unresolved-reference` | error | Variable might not be defined |
| `invalid-argument-type` | error | Argument type mismatch |
| `incompatible-assignment` | error | Assigned value incompatible |
| `missing-argument` | error | Required argument missing |
| `unsupported-operator` | error | Operator not supported for types |
| `invalid-return-type` | error | Return type mismatch |
| `division-by-zero` | warn | Potential division by zero |
| `unused-ignore-comment` | warn | Suppression not needed |
| `redundant-cast` | warn | Cast has no effect |
| `possibly-unbound-attribute` | warn | Attribute might not exist |
| `index-out-of-bounds` | warn | Index might be out of range |

## Intersection Types (ty Exclusive)

ty has first-class intersection type support:

```python
def output_as_json(obj: Serializable) -> str:
    if isinstance(obj, Versioned):
        reveal_type(obj)  # reveals: Serializable & Versioned
        return str({
            "data": obj.serialize_json(),  # From Serializable
            "version": obj.version          # From Versioned
        })
    return obj.serialize_json()
```

## Suppression Comments

```python
# Suppress single rule
x: int = "hello"  # type: ignore[incompatible-assignment]

# Suppress multiple
y = risky()  # type: ignore[possibly-unresolved-reference, invalid-argument-type]
```

## Reference Documents

For detailed information, see:

| Document | Content |
|----------|---------|
| `references/ty_rules_reference.md` | All rules with examples and fixes |
| `references/typing_cheatsheet.md` | Python typing module quick reference |
| `references/advanced_patterns.md` | Protocols, generics, type guards, variance |
| `references/migration_guide.md` | mypy/pyright → ty migration |
| `references/common_errors.md` | Error solutions with examples |
| `references/editor_setup/` | VS Code, Cursor, Neovim setup |

## Resources

- [ty Documentation](https://docs.astral.sh/ty/)
- [ty Playground](https://play.astral.sh/ty)
- [ty GitHub](https://github.com/astral-sh/ty)
