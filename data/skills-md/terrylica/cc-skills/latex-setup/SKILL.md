---
name: latex-setup
description: LaTeX environment setup on macOS. TRIGGERS - install LaTeX, MacTeX, Skim viewer, SyncTeX setup.
allowed-tools: Read, Edit, Bash
---

# LaTeX Environment Setup

## When to Use This Skill

Use this skill when:

- Installing LaTeX on a new machine
- Setting up MacTeX distribution
- Configuring Skim PDF viewer with SyncTeX
- Verifying LaTeX installation
- Troubleshooting missing packages

## Quick Reference

## Recommended Stack

| Component        | Purpose                                 | Status          |
| ---------------- | --------------------------------------- | --------------- |
| **MacTeX 2025**  | Full LaTeX distribution (TeX Live 2025) | ✅ Recommended  |
| **Skim 1.7.11**  | PDF viewer with SyncTeX support         | ✅ macOS only   |
| **TeXShop 5.57** | Integrated LaTeX IDE (optional)         | ✅ Native macOS |

---

## Quick Start

### Install MacTeX

```bash
brew install --cask mactex
# Size: ~4.5 GB (includes everything)
```

### Verify Installation

```bash
tex --version
# Expected: TeX 3.141592653 (TeX Live 2025)

pdflatex --version
latexmk --version
```

### Test Compilation

```bash
echo '\documentclass{article}\begin{document}Hello World!\end{document}' > test.tex
pdflatex test.tex
ls test.pdf  # Verify PDF created
```

---

## Post-Installation Checklist

- [ ] Verify `tex --version` shows TeX Live 2025
- [ ] Verify `latexmk --version` shows 4.86a+
- [ ] Verify `pdflatex test.tex` creates PDF
- [ ] Install Skim if using mactex-no-gui
- [ ] Test SyncTeX: compile with `-synctex=1` flag
- [ ] Configure Skim preferences for editor integration
- [ ] Add `/Library/TeX/texbin` to PATH if needed
- [ ] Test package installation: `sudo tlmgr install <package>`

---

## Reference Documentation

For detailed information, see:

- [Installation](./references/installation.md) - Full MacTeX vs lightweight options, Skim installation
- [Verification](./references/verification.md) - Check installation, verify PATH, test compilation
- [Package Management](./references/package-management.md) - Check, install, search for packages with tlmgr
- [Skim Configuration](./references/skim-configuration.md) - Enable SyncTeX, configure preferences for editor integration
- [Troubleshooting](./references/troubleshooting.md) - PATH issues, tlmgr problems, permissions

**See Also**:

- Build Workflows: Use `latex/build` skill for latexmk automation
- Table Creation: Use `latex/tables` skill for tabularray usage

---

## Troubleshooting

| Issue                     | Cause                         | Solution                                           |
| ------------------------- | ----------------------------- | -------------------------------------------------- |
| tex command not found     | PATH not configured           | Add `/Library/TeX/texbin` to PATH in shell profile |
| Permission denied (tlmgr) | Need sudo for system packages | Use `sudo tlmgr install <package>`                 |
| Package not found         | Missing from TeX Live         | Run `tlmgr search <package>` to find correct name  |
| Skim not showing PDF      | SyncTeX not enabled           | Compile with `-synctex=1` flag                     |
| Outdated TeX Live         | Old MacTeX version            | Run `sudo tlmgr update --self --all`               |
| Compilation hangs         | Infinite loop in document     | Check for circular includes or missing \end{}      |
| Missing font error        | Font not in TeX distribution  | Install with `tlmgr install <font-package>`        |
| Disk space error          | Full TeX Live too large       | Consider BasicTeX (smaller) if space limited       |
