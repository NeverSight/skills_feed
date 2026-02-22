---
name: just-init
description: >
  Navigate Python codebases by reading __init__.py files before opening other
  files in a package. Maintain every __init__.py as living documentation: a
  top-level docstring containing a one-line package description, a file tree
  of .py files and subdirectories, and a brief purpose for each entry.
  Use when: (1) exploring or navigating a Python codebase, (2) creating new
  Python packages or modules, (3) adding, removing, or renaming files within
  a Python package, (4) onboarding to an unfamiliar Python project.
---

# just-init

Use `__init__.py` files as the single source of truth for understanding and
documenting Python packages.

## Navigation Rule

Before opening any file in a Python package, read its `__init__.py` first.
Use the docstring to understand the package's purpose and decide which files
to explore next. Apply this recursively — when entering a sub-package, read
its `__init__.py` before going deeper.

When exploring an unfamiliar codebase, start from the top-level package
`__init__.py` and drill down based on what each docstring describes.

## Docstring Format

Every `__init__.py` must start with a triple-quoted docstring containing:

1. A one-line description of the package's purpose.
2. A file tree listing `.py` files and subdirectories (not non-Python files).
3. A `# comment` after each entry describing its purpose.

```python
"""
One-line description of what this package does.

package_name/
├── __init__.py        # Package init and public exports.
├── module_a.py        # Brief description of module_a.
├── module_b.py        # Brief description of module_b.
└── subpackage/        # Brief description of subpackage.
"""
```

Rules:
- Use `├──` for all entries except the last, which uses `└──`.
- List `.py` files first, then subdirectories, both in alphabetical order.
- Subdirectories end with `/` and are not expanded — their own `__init__.py`
  documents their contents.
- Descriptions are concise: aim for under 10 words per entry.
- The package name in the tree matches the directory name.

## Auto-Update Rule

After any of these changes, immediately update the affected `__init__.py`:

- **File added** — Add the new entry to the tree with a description.
- **File removed** — Remove the entry from the tree.
- **File renamed** — Update the entry name and description if needed.
- **Subdirectory added** — Add the directory entry (with trailing `/`) and
  create a new `__init__.py` inside it.
- **Subdirectory removed** — Remove the directory entry from the parent tree.

When a change affects a nested package, update both the sub-package's own
`__init__.py` and the parent's `__init__.py` if the sub-package entry changed.

Do not wait for the user to ask — update `__init__.py` as part of every file
operation within a Python package.

## New Package Rule

When creating a new Python package:

1. Create the directory.
2. Create `__init__.py` as the first file.
3. Write the docstring with the package description and initial file tree.
4. Then create the other files.
5. Update the tree in `__init__.py` after all files are in place.

## Edge Cases

- **Empty package** — The docstring contains only the description and a tree
  with just `__init__.py`.
- **Non-Python directories** (data, fixtures, configs) — List them in the tree
  with a trailing `/` and a description, but do not expand their contents and
  do not create an `__init__.py` inside them.
- **No existing docstring** — When encountering an `__init__.py` without a
  docstring, add one based on the current directory contents before proceeding.
- **Conflicting docstring** — If the docstring is outdated (doesn't match
  actual files), update it to reflect reality before continuing.

## Examples

See [references/examples.md](references/examples.md) for concrete patterns:
simple flat packages, nested packages, packages with non-Python directories,
and before/after update scenarios.
