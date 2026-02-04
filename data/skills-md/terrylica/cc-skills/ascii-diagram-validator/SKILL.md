---
name: ascii-diagram-validator
description: Validate ASCII diagram alignment in markdown. TRIGGERS - diagram alignment, ASCII art, box-drawing diagrams.
---

# ASCII Diagram Validator

Validate and fix alignment issues in ASCII box-drawing diagrams commonly used in architecture documentation, README files, and code comments.

## Overview

ASCII diagrams using box-drawing characters (─│┌┐└┘├┤┬┴┼ and double-line variants ═║╔╗╚╝╠╣╦╩╬) require precise column alignment. This skill provides:

1. **Validation script** - Detects misaligned characters with file:line:column locations
2. **Actionable fixes** - Specific suggestions for correcting each issue
3. **Multi-file support** - Validate individual files or entire directories

## When to Use This Skill

Invoke when:

- Creating or editing ASCII architecture diagrams in markdown
- Reviewing documentation with box-drawing diagrams
- Fixing "diagram looks wrong" complaints
- Before committing docs/ARCHITECTURE.md or similar files
- When user mentions "ASCII alignment", "diagram alignment", or "box drawing"

## Supported Characters

### Single-Line Box Drawing

```
Corners: ┌ ┐ └ ┘
Lines:   ─ │
T-joins: ├ ┤ ┬ ┴
Cross:   ┼
```

### Double-Line Box Drawing

```
Corners: ╔ ╗ ╚ ╝
Lines:   ═ ║
T-joins: ╠ ╣ ╦ ╩
Cross:   ╬
```

### Mixed (Double-Single)

```
╞ ╟ ╤ ╧ ╪ ╫
```

## Quick Start

### Validate a Single File

```bash
/usr/bin/env bash << 'PREFLIGHT_EOF'
uv run ${CLAUDE_PLUGIN_ROOT}/skills/ascii-diagram-validator/scripts/check_ascii_alignment.py docs/ARCHITECTURE.md
PREFLIGHT_EOF
```

### Validate Multiple Files

```bash
/usr/bin/env bash << 'PREFLIGHT_EOF_2'
uv run ${CLAUDE_PLUGIN_ROOT}/skills/ascii-diagram-validator/scripts/check_ascii_alignment.py docs/*.md
PREFLIGHT_EOF_2
```

### Validate Directory

```bash
/usr/bin/env bash << 'PREFLIGHT_EOF_3'
uv run ${CLAUDE_PLUGIN_ROOT}/skills/ascii-diagram-validator/scripts/check_ascii_alignment.py docs/
PREFLIGHT_EOF_3
```

## Output Format

The script outputs issues in a compiler-like format for easy navigation:

```
docs/ARCHITECTURE.md:45:12: error: vertical connector '│' at column 12 has no matching character above
  → Suggestion: Add '│', '├', '┤', '┬', or '┼' at line 44, column 12

docs/ARCHITECTURE.md:67:8: warning: horizontal line '─' at column 8 has no terminator
  → Suggestion: Add '┐', '┘', '┤', '┴', or '┼' to close the line
```

### Severity Levels

| Level   | Description                              |
| ------- | ---------------------------------------- |
| error   | Broken connections, misaligned verticals |
| warning | Unterminated lines, potential issues     |
| info    | Style suggestions (optional cleanup)     |

## Validation Rules

The script checks for:

1. **Vertical Alignment** - Vertical connectors (│║) must align with characters above/below
2. **Corner Connections** - Corners (┌┐└┘╔╗╚╝) must connect properly to adjacent lines
3. **Junction Validity** - T-joins and crosses must have correct incoming/outgoing connections
4. **Line Continuity** - Horizontal lines (─═) should terminate at valid endpoints
5. **Box Closure** - Boxes should be properly closed (no dangling edges)

## Exit Codes

| Code | Meaning                                         |
| ---- | ----------------------------------------------- |
| 0    | No issues found                                 |
| 1    | Errors detected                                 |
| 2    | Warnings only (errors ignored with --warn-only) |

## Integration with Claude Code

When Claude Code creates or edits ASCII diagrams:

1. Run the validator script on the file
2. Review any errors in the output
3. Apply suggested fixes
4. Re-run until clean

### Example Workflow

```bash
/usr/bin/env bash << 'PREFLIGHT_EOF_4'
# After editing docs/ARCHITECTURE.md
uv run ${CLAUDE_PLUGIN_ROOT}/skills/ascii-diagram-validator/scripts/check_ascii_alignment.py docs/ARCHITECTURE.md

# If errors found, Claude Code can read the output and fix:
# docs/ARCHITECTURE.md:45:12: error: vertical connector '│' at column 12 has no matching character above
# → Edit line 44, column 12 to add the missing connector
PREFLIGHT_EOF_4
```

## Limitations

- Detects structural alignment issues, not aesthetic spacing
- Requires consistent use of box-drawing characters (no mixed ASCII like +---+)
- Tab characters may cause false positives (convert to spaces first)
- Unicode normalization not performed (use pre-composed characters)

## Bundled Scripts

| Script                             | Purpose                |
| ---------------------------------- | ---------------------- |
| `scripts/check_ascii_alignment.py` | Main validation script |

## Related

- [ARCHITECTURE.md best practices](https://github.com/joelparkerhenderson/architecture-decision-record)
- [Unicode Box Drawing block](https://www.unicode.org/charts/PDF/U2500.pdf)

---

## Troubleshooting

| Issue                       | Cause                         | Solution                                            |
| --------------------------- | ----------------------------- | --------------------------------------------------- |
| Script not found            | Plugin not installed          | Verify plugin installed with `claude plugin list`   |
| False positives with tabs   | Tab characters misalign       | Convert tabs to spaces before validation            |
| Mixed ASCII not detected    | Using `+---+` style           | Script only validates Unicode box-drawing chars     |
| Column numbers off          | Unicode width calculation     | Use pre-composed characters, avoid combining marks  |
| No issues but looks wrong   | Aesthetic spacing not checked | Validator checks structure, not visual spacing      |
| Exit code 2 unexpected      | warnings only mode            | Use --warn-only flag to treat warnings as success   |
| Can't find validation error | Complex nested diagram        | Check line numbers in output, validate section only |
| Unicode chars not rendering | Terminal font missing glyphs  | Use font with full Unicode box-drawing support      |
