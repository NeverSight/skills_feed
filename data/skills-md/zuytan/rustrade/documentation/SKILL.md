---
name: Documentation
description: Keep project documentation up to date
---

# Skill: Documentation

## When to use this skill

- After adding a new feature
- Modifying the architecture
- User-facing behavior changes
- Before a release

## Available templates

| Template | Usage |
|----------|-------|
| `templates/version_entry.md` | Format for GLOBAL_APP_DESCRIPTION_VERSIONS.md |
| `templates/rustdoc.md` | Rustdoc documentation for functions |

## Files to update

### GLOBAL_APP_DESCRIPTION.md

**When**: New feature, architecture change, new strategy

**Content**: Complete system overview, organized by sections:
1. System Overview
2. Core Architecture
3. Trading Intelligence
4. Risk Management
5. User Interface
6. Infrastructure
7. Performance
8. Server Mode
9. Contributor Documentation

### GLOBAL_APP_DESCRIPTION_VERSIONS.md

**When**: On every significant commit

**Format**:
```markdown
## Version X.Y.Z - YYYY-MM-DD

### Added
- New feature A
- New feature B

### Changed
- Behavior modification X

### Fixed
- Bug fix Y

### Removed
- Removed obsolete feature Z
```

### Cargo.toml

**When**: On every release

**SemVer rules**:
| Change type | Version |
|-------------|---------|
| Bug fix, patch | 0.0.X → 0.0.X+1 |
| New backward-compatible feature | 0.X.0 → 0.X+1.0 |
| Breaking change | X.0.0 → X+1.0.0 |

### docs/STRATEGIES.md

**When**: Adding or modifying trading strategies

**Content per strategy**:
- Name and description
- Indicators used
- Entry/exit conditions
- Configurable parameters
- Recommended use cases

## Documentation checklist

For a new feature:
- [ ] Description added in GLOBAL_APP_DESCRIPTION.md
- [ ] Entry in GLOBAL_APP_DESCRIPTION_VERSIONS.md
- [ ] Version incremented in Cargo.toml
- [ ] README.md updated if needed
- [ ] Rustdoc comments on new public functions
- [ ] Skills updated if applicable (see below)

## Skills update (.agent/skills/)

**IMPORTANT**: Skills must reflect the current state of the code.

| If you add... | Update... |
|---------------|-----------|
| New trading strategy | `rust-trading/SKILL.md` |
| New technical indicator | `rust-trading/SKILL.md` |
| New benchmark command | `benchmarking/SKILL.md` |
| New benchmark script | `benchmarking/scripts/` |
| New test pattern | `implementation/templates/test_module.md` |
| New module structure | `implementation/templates/module_structure.md` |
| New doc convention | `documentation/SKILL.md` or `templates/` |
| New quality rule | `critical-review/SKILL.md` |
| New validation step | `testing/SKILL.md` |
| New UI component | `ui-design/SKILL.md` |
| New system feature | `spec-management/SKILL.md` (Update `specs/`) |

## Documentation conventions

### Rustdoc

```rust
/// Brief description of the function.
///
/// More detailed explanation if needed.
///
/// # Arguments
///
/// * `param1` - Description of param1
/// * `param2` - Description of param2
///
/// # Returns
///
/// Description of return value
///
/// # Errors
///
/// Description of possible errors
///
/// # Examples
///
/// ```
/// let result = my_function(arg1, arg2);
/// ```
pub fn my_function(param1: Type1, param2: Type2) -> Result<ReturnType, Error> {
    // ...
}
```

### Markdown

- Use hierarchical headers (##, ###)
- Include code examples
- Use tables for structured data
- Link to source files when relevant
