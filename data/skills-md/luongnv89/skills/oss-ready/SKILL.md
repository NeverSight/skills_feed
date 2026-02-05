---
name: oss-ready
description: Transform projects into professional open-source repositories with standard components. Use when users ask to "make this open source", "add open source files", "setup OSS standards", "create contributing guide", "add license", or want to prepare a project for public release with README, CONTRIBUTING, LICENSE, and GitHub templates.
---

## Workflow

### 1. Analyze Project

Identify:
- Primary language(s) and tech stack
- Project purpose and functionality
- Existing documentation to preserve
- Package manager (npm, pip, cargo, etc.)

### 2. Create/Update Core Files

**README.md** - Enhance with:
- Project overview and motivation
- Key features list
- Quick start (< 5 min setup)
- Prerequisites and installation
- Usage examples with code
- Project structure
- Technology stack
- Contributing link
- License badge

**CONTRIBUTING.md** - Include:
- How to contribute overview
- Development setup
- Branching strategy (feature branches from main)
- Commit conventions (Conventional Commits)
- PR process and review expectations
- Coding standards
- Testing requirements

**LICENSE** - Default to MIT unless specified. Copy from `assets/LICENSE-MIT`.

**CODE_OF_CONDUCT.md** - Use Contributor Covenant. Copy from `assets/CODE_OF_CONDUCT.md`.

**SECURITY.md** - Vulnerability reporting process. Copy from `assets/SECURITY.md`.

### 3. Create GitHub Templates

Copy from `assets/.github/`:
- `ISSUE_TEMPLATE/bug_report.md`
- `ISSUE_TEMPLATE/feature_request.md`
- `PULL_REQUEST_TEMPLATE.md`

### 4. Create Documentation Structure

```
docs/
├── ARCHITECTURE.md    # System design, components
├── DEVELOPMENT.md     # Dev setup, debugging
├── DEPLOYMENT.md      # Production deployment
└── CHANGELOG.md       # Version history
```

### 5. Update Project Metadata

Update package file based on tech stack:
- **Node.js**: `package.json` - name, description, keywords, repository, license
- **Python**: `pyproject.toml` or `setup.py`
- **Rust**: `Cargo.toml`
- **Go**: `go.mod` + README badges

### 6. Ensure .gitignore

Verify comprehensive patterns for the tech stack.

### 7. Present Checklist

After completion, show:
- [x] Files created/updated
- [ ] Items needing manual review
- Recommendations for next steps

## Guidelines

- Preserve existing content - enhance, don't replace
- Use professional, welcoming tone
- Adapt to project's actual tech stack
- Include working examples from the actual codebase

## Assets

Templates in `assets/`:
- `LICENSE-MIT` - MIT license template
- `CODE_OF_CONDUCT.md` - Contributor Covenant
- `SECURITY.md` - Security policy template
- `.github/ISSUE_TEMPLATE/bug_report.md`
- `.github/ISSUE_TEMPLATE/feature_request.md`
- `.github/PULL_REQUEST_TEMPLATE.md`
