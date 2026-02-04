---
name: latex-build
description: LaTeX builds with latexmk and live preview. TRIGGERS - latexmk, LaTeX build, live preview, compilation.
allowed-tools: Read, Edit, Bash
---

# LaTeX Build Automation

## When to Use This Skill

Use this skill when:

- Compiling LaTeX documents
- Setting up live preview with auto-rebuild
- Managing multi-file projects
- Troubleshooting build failures
- Cleaning build artifacts
- Automating compilation workflows

## Quick Reference

## Why latexmk?

Industry standard build tool:

- Auto-detects dependencies (bibliography, index, etc.)
- Runs correct number of times (handles cross-references)
- Live preview mode watches for file changes
- Works with Skim for SyncTeX auto-reload
- Bundled with MacTeX (no separate install needed)

---

## Basic Usage

### One-Time Build

```bash
latexmk -pdf document.tex
# Result: document.pdf created
```

### Live Preview (Watch Mode)

```bash
latexmk -pvc -pdf document.tex

# What happens:
# - Compiles document initially
# - Watches for file changes
# - Auto-recompiles when files change
# - Auto-reloads PDF in Skim viewer
```

**Stop watching:** Press `Ctrl+C`

---

## Quick Reference Card

```bash
# Build once
latexmk -pdf document.tex

# Live preview (watch mode)
latexmk -pvc -pdf document.tex

# Build with SyncTeX
latexmk -pdf -synctex=1 document.tex

# Clean artifacts
latexmk -c              # Keep PDF
latexmk -C              # Remove PDF too

# Force rebuild
latexmk -gg -pdf document.tex

# Non-interactive (for CI)
latexmk -pdf -interaction=nonstopmode document.tex
```

---

## Build Checklist

- [ ] Verify latexmk installed: `which latexmk`
- [ ] Test basic build: `latexmk -pdf document.tex`
- [ ] Enable SyncTeX: Add `-synctex=1` flag
- [ ] Test live preview: `latexmk -pvc -pdf document.tex`
- [ ] Configure Skim for auto-reload
- [ ] Create Makefile for common tasks (optional)
- [ ] Create .latexmkrc for project-specific settings (optional)
- [ ] Test clean: `latexmk -c` removes artifacts

---

## Reference Documentation

For detailed information, see:

- [Common Commands](./references/common-commands.md) - Build options and output formats
- [Multi-File Projects](./references/multi-file-projects.md) - Automatic dependency tracking for complex documents
- [Configuration](./references/configuration.md) - .latexmkrc and Makefile integration
- [Troubleshooting](./references/troubleshooting.md) - Common build issues and solutions
- [Advanced Patterns](./references/advanced-patterns.md) - Parallel builds and CI/CD integration

**Official Docs**: Run `man latexmk` or `latexmk -help` for complete reference

**See Also**:

- Use `latex/setup` skill for installing LaTeX and configuring environment
- Use `latex/tables` skill for creating tables with tabularray

---

## Troubleshooting

| Issue                      | Cause                         | Solution                                             |
| -------------------------- | ----------------------------- | ---------------------------------------------------- |
| latexmk not found          | Not in PATH                   | Add `/Library/TeX/texbin` to PATH                    |
| Undefined control sequence | Missing package               | Check `\usepackage` statements for required packages |
| References show ??         | Need multiple runs            | latexmk handles this automatically; ensure no errors |
| Live preview not updating  | Skim auto-reload disabled     | Skim Preferences → Sync → Check for file changes     |
| Build hangs                | Input prompt in nonstop mode  | Use `-interaction=nonstopmode` flag                  |
| PDF not updating           | Build error preventing output | Check .log file for specific error                   |
| SyncTeX not working        | Missing -synctex=1 flag       | Add `-synctex=1` to build command                    |
| Too many aux files         | Normal build artifacts        | Run `latexmk -c` to clean (keeps PDF)                |
