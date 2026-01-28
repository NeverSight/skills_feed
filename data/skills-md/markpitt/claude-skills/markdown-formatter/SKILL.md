---
name: markdown-formatter
description: Formats markdown files according to best practices and common style guidelines. Use when cleaning up markdown documentation, ensuring consistent formatting, or standardizing README files.
allowed-tools: Read, Edit, Grep, Glob, Bash
version: 2.0
---

# Markdown Formatter

This skill provides modular, categorized formatting guidance for markdown documents. Load resources by formatting area as needed.

## Quick Reference: When to Load Which Resource

| Formatting Area | Load Resource | Common Issues |
|-----------------|---------------|---------------|
| Headers, document structure, hierarchy | `resources/headers-hierarchy.md` | Skipped levels, underline-style, spacing |
| Lists, nesting, indentation | `resources/lists-nesting.md` | Inconsistent markers, wrong indentation |
| Code blocks, inline code, emphasis | `resources/code-emphasis.md` | Missing language IDs, wrong markers |
| Links, images, references, alt text | `resources/links-images.md` | Bad link text, missing alt text |
| Spacing, tables, final polish | `resources/spacing-tables.md` | Inconsistent spacing, table alignment |

## Core Rules at a Glance

### Headers
- **ATX-style**: Use `#` notation, not underlines
- **One per document**: Single H1 at start
- **No skips**: Go H1 → H2 → H3, never skip levels
- **Spacing**: Blank line before (except first) and after each header

### Lists
- **Marker**: Use `-` consistently (not `*` or `+`)
- **Indentation**: 2 spaces per nesting level
- **Spacing**: Blank line before and after list blocks

### Code
- **Inline**: Single backticks for code references
- **Blocks**: Fenced (not indented) with language ID
- **Spacing**: Blank line before and after blocks

### Links & Images
- **Links**: Descriptive text (no "click here")
- **References**: Use reference-style for repeated URLs
- **Images**: Always include meaningful alt text

### Spacing
- **Between blocks**: One blank line
- **No trailing whitespace**: Remove all line-end spaces
- **End of file**: Single newline

### Spacing
- **Between blocks**: One blank line
- **No trailing whitespace**: Remove all line-end spaces
- **End of file**: Single newline

## Formatting Workflow

### Phase 1: Structural Scan
Check high-level structure first:
1. Read entire file to understand flow
2. Load `resources/headers-hierarchy.md` if issues found
3. Verify H1 count, levels, and spacing

### Phase 2: Block-Level Formatting
Process each formatting category in sequence:
1. **Headers** → `headers-hierarchy.md`
2. **Lists** → `lists-nesting.md`
3. **Code** → `code-emphasis.md`
4. **Links/Images** → `links-images.md`

### Phase 3: Final Polish
Complete document-level formatting:
1. Load `resources/spacing-tables.md`
2. Fix spacing around all blocks
3. Validate tables (if present)
4. Check line length and trailing whitespace
5. Verify single trailing newline

### Phase 4: Validation
Use validation tools to catch remaining issues:
```bash
./skills/markdown-formatter/scripts/validate-markdown.sh file.md
```

## How to Use Resources

Each resource file is **self-contained** and covers one formatting area:

- **Headers**: Read full file once for complete header guidance
- **Lists**: Reference indentation rules and spacing requirements
- **Code**: Check inline vs. block syntax and language identifiers
- **Links/Images**: Verify alt text guidelines and reference styles
- **Spacing**: Apply final polish and table formatting

### Resource Structure

Each resource includes:
- **Syntax examples** (correct and incorrect)
- **Rules and guidelines** (with explanations)
- **Common issues and fixes** (before/after)
- **Validation checklist** (quick verification)

### Resource Structure

Each resource includes:
- **Syntax examples** (correct and incorrect)
- **Rules and guidelines** (with explanations)
- **Common issues and fixes** (before/after)
- **Validation checklist** (quick verification)

## Common Formatting Issues

### Issue: Inconsistent List Markers
```markdown
<!-- Before: mixed markers -->
* Item 1
+ Item 2
- Item 3

<!-- After: consistent -->
- Item 1
- Item 2
- Item 3
```
→ Load `resources/lists-nesting.md` for full guidance

### Issue: Missing Code Block Language
```markdown
<!-- Before -->
```
npm install
```

<!-- After -->
```bash
npm install
```
```
→ Load `resources/code-emphasis.md`

### Issue: Skipped Header Levels
```markdown
<!-- Before -->
# Title
### Subsection (skipped H2!)

<!-- After -->
# Title
## Section
### Subsection
```
→ Load `resources/headers-hierarchy.md`

### Issue: Bad Link Text
```markdown
<!-- Before -->
Click [here](url) for details

<!-- After -->
See the [installation guide](url)
```
→ Load `resources/links-images.md`

### Issue: Missing Alt Text
```markdown
<!-- Before -->
![](screenshot.png)

<!-- After -->
![Dashboard showing user metrics](screenshot.png)
```
→ Load `resources/links-images.md`

## Output Format

When formatting files, provide:

**Summary**
- Original line count
- New line count
- Primary issues fixed

**Issues Fixed**
- List each category of corrections
- Count of fixes per category

**Recommendations**
- Content improvements (if any)
- Consistency notes
- Accessibility enhancements

## Formatting Decision Table

Use this table to decide what to fix and in what order:

| Priority | Category | When to Address | Load Resource |
|----------|----------|-----------------|----------------|
| 1 | Structure | First pass—headers, hierarchy | headers-hierarchy.md |
| 2 | Lists | Check consistency, indentation | lists-nesting.md |
| 3 | Code | Verify blocks have language IDs | code-emphasis.md |
| 4 | Links/Images | Descriptive text, alt text | links-images.md |
| 5 | Spacing | Final polish, cleanup | spacing-tables.md |

## Best Practices

### Preserve Content
Never change the meaning or information—only format structure.

### Be Consistent
Apply rules uniformly throughout the document.

### Respect Context
Some projects may have specific conventions. Ask if unclear.

### Document Changes
Clearly explain what was modified and why.

## Limitations

This skill does **not**:
- Check spelling or grammar
- Validate external links
- Optimize images
- Enforce strict line length

## Integration Points

**Works with:**
- Linters (markdownlint, etc.)
- CI/CD pipelines (pre-commit hooks)
- Documentation generators
- Static site builders

**Pairs well with:**
- GitHub issue templates
- README standards
- Style guides
- Documentation style checkers

## Resource Index

| Resource | Lines | Coverage |
|----------|-------|----------|
| headers-hierarchy.md | 250+ | Headers, hierarchy, structure |
| lists-nesting.md | 350+ | Lists, nesting, indentation |
| code-emphasis.md | 300+ | Code blocks, inline code, emphasis |
| links-images.md | 400+ | Links, images, alt text, references |
| spacing-tables.md | 350+ | Spacing, tables, document polish |

## Validation Tools

### Script: validate-markdown.sh
```bash
./skills/markdown-formatter/scripts/validate-markdown.sh file.md
```

Checks for:
- Missing newline at end
- Trailing whitespace
- Code blocks without language ID
- Inconsistent list markers
- Bad link text
- Missing alt text
- Multiple blank lines

## Guidelines for Complex Documents

### Large Documents (1000+ lines)
1. Process by section (headers first)
2. Validate each section before moving on
3. Run full validation at end

### Documents with Code
1. Ensure all code blocks have language IDs
2. Verify inline code uses backticks correctly
3. Check code examples for syntax errors

### Documents with Heavy Linking
1. Use reference-style for repeated URLs
2. Verify all links are descriptive
3. Validate internal anchors work

### Documents with Tables
1. Align columns for readability
2. Ensure header row present
3. Verify separator row has 3+ dashes

## When Uncertain

- **Multiple conventions present?** Ask the user for project preference
- **Non-standard markdown?** Check rendering before proceeding
- **Content ambiguous?** Clarify with user before formatting
- **Extensive changes needed?** Show before/after samples first

## Quick Checklist

After formatting, verify:
- [ ] Single H1 at document start
- [ ] ATX-style headers with proper spacing
- [ ] Consistent list markers (all `-`)
- [ ] Code blocks have language IDs
- [ ] All code formatted correctly
- [ ] Links have descriptive text
- [ ] Images have alt text
- [ ] Proper spacing around all blocks
- [ ] No trailing whitespace
- [ ] Single newline at end
- [ ] Document renders correctly

---

**Next Steps**: Load the appropriate resource file from the Quick Reference table above based on the formatting issues you've identified in the document.
