---
name: coding-standards
description: >
  Enforces consistent coding standards across the codebase including naming conventions,
  code organization, and documentation requirements. Use when writing new code, reviewing
  pull requests, or refactoring existing code.
compatibility: Works with any codebase
metadata:
  version: "2.1.0"
---

# Coding Standards

Enforces consistent naming conventions, code organization, and documentation across the codebase.

## When to use this skill

- Writing new code
- Reviewing pull requests
- Refactoring existing code
- Onboarding to a new codebase

## Skill Contents

### Sections

- [When to use this skill](#when-to-use-this-skill) (L16-L22)
- [Quick Start](#quick-start) (L51-L63)
- [Naming Conventions](#naming-conventions) (L64-L74)
- [Available Scripts](#available-scripts) (L75-L86)
- [References](#references) (L87-L94)
- [Assets](#assets) (L95-L100)
- [Related Skills](#related-skills) (L101-L104)

### Available Resources

**📚 references/** - Detailed documentation
- [code organization](references/code-organization.md)
- [documentation standards](references/documentation-standards.md)
- [general principles](references/general-principles.md)
- [naming conventions](references/naming-conventions.md)

**🔧 scripts/** - Automation scripts
- [check naming conventions](scripts/check-naming-conventions.ts)

**📦 assets/** - Templates and resources
- [templates](assets/templates)

---

## Quick Start

Run naming convention checks:

```bash
# Via skills CLI
node .scripts/skills-cli.ts coding-standards validate

# Programmatically
import { codingStandards } from './.scripts/lib/skills/index.ts';
const result = await codingStandards.validate('./src');
```

## Naming Conventions

| Language | Convention | Example |
|----------|------------|---------|
| Java | PascalCase for classes | `UserService.java` |
| Python | snake_case for modules | `user_service.py` |
| TypeScript/JS | kebab-case or camelCase | `user-service.ts` |
| Shell | kebab-case | `run-tests.sh` |

For complete rules, see [references/naming-conventions.md](references/naming-conventions.md).

## Available Scripts

Scripts are implemented in `.scripts/lib/skills/coding-standards.ts`:

| Function | Description |
|----------|-------------|
| `validate(dir)` | Run all naming convention checks |
| `checkNamingConventions(dir)` | Check file naming |
| `checkJavaClass(path)` | Validate Java class name |
| `checkPythonModule(path)` | Validate Python module name |
| `checkTypeScriptFile(path)` | Validate TS/JS file name |

## References

| Reference | Description |
|-----------|-------------|
| [references/naming-conventions.md](references/naming-conventions.md) | Naming rules by language |
| [references/code-organization.md](references/code-organization.md) | Project structure patterns |
| [references/documentation-standards.md](references/documentation-standards.md) | Documentation requirements |

## Assets

| Asset | Description |
|-------|-------------|
| [assets/templates/file-header-template.txt](assets/templates/file-header-template.txt) | Standard file header |

## Related Skills

- `quality-gateway` - Orchestrates coding standards with other quality checks
- `doc-sync` - Documentation synchronization
<!-- AUTO-GENERATED FILE - DO NOT EDIT DIRECTLY -->
<!-- Source: bitsoex/ai-code-instructions → global/skills/coding-standards/SKILL.md -->
<!-- To modify, edit the source file and run the distribution workflow -->

