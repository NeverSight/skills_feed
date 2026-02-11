---
name: lint-markdown
description: >
  Lint and fix Markdown files using markdownlint-cli2. Use when asked to:
  lint, fix, format, or clean up Markdown (.md) files; enforce Markdown
  best practices or style standards; resolve markdownlint errors or warnings.
  Triggers on requests mentioning markdownlint, markdown linting, or
  formatting Markdown to best standards.
---

# Markdown Linting with `markdownlint-cli2`

## Workflow

### 1. Run auto-fix first

```bash
markdownlint-cli2 --fix "<filepath>"
```

This resolves ~30 fixable rules automatically (white space, list style, blank lines, emphasis style, etc.).

### 2. Re-lint to find remaining issues

```bash
markdownlint-cli2 "<filepath>" 2>&1
```

- Exit code `0` = clean. Stop here.
- Exit code `1` = errors remain. Continue to step 3.

Parse each error line: `<file>:<line>[:<col>] <MDXXX>/<alias> <description>`

### 3. Manually fix remaining errors

Read the file, then apply fixes with the Edit tool. For rule-specific fix strategies, consult [references/rules.md](references/rules.md).

Common non-fixable issues and quick fixes:

- **MD040 (fenced-code-language)**: Add a language identifier after opening ` ``` ` (e.g., ` ```bash `, ` ```json `). Use `text` if no language applies.
- **MD033 (no-inline-html)**: Replace HTML tags with Markdown equivalents. Remove tags with no Markdown equivalent if they are non-essential.
- **MD001 (heading-increment)**: Ensure headings increase by one level only (`#` then `##`, never `#` then `###`).
- **MD045 (no-alt-text)**: Add descriptive alt text to images: `![description](url)`.

### 4. Verify clean

```bash
markdownlint-cli2 "<filepath>" 2>&1
```

Repeat steps 3-4 until exit code is `0`.

## Notes

- Always quote file paths in commands to handle spaces.
- If a `.markdownlint-cli2.jsonc`, `.markdownlint.yaml`, or similar config exists in the project, respect its rule overrides.
- When linting multiple files, use globs: `markdownlint-cli2 --fix "**/*.md"`.
- The `--fix` flag modifies files in place. It is safe to run repeatedly.
