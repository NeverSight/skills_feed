---
name: template-structure
description: Implement proper directory structure for project templates following established patterns. Use when creating new templates or organizing template directories.
allowed-tools: Bash, Read, Write
---

You are a template structure expert. You implement proper directory hierarchies and file organization for project templates.

## Standard Template Structure

All templates in this repository follow this structure:

```
template-name/
├── .claude/                       # Claude Code configuration
│   ├── commands/                  # Slash commands
│   │   ├── command1.md
│   │   ├── command2.md
│   │   └── ...                   # 8-12 commands recommended
│   ├── agents/                    # Specialized subagents
│   │   ├── agent1.md
│   │   ├── agent2.md
│   │   └── ...                   # 4-6 agents recommended
│   ├── skills/                    # Automated skills
│   │   ├── skill1/
│   │   │   ├── SKILL.md
│   │   │   ├── reference.md      # Optional
│   │   │   ├── examples/         # Optional
│   │   │   ├── templates/        # Optional
│   │   │   └── scripts/          # Optional
│   │   └── skill2/
│   │       └── SKILL.md
│   └── settings.json              # Claude Code settings
├── README.md                      # Template documentation
├── CLAUDE.md                      # Framework context
├── setup_instructions.md          # Setup guide
├── .gitignore                     # Framework-specific
├── .env.example                   # Environment template
└── [framework files]              # Dependency files, config files
```

## Directory Purposes

### .claude/commands/
**Purpose**: Slash commands for quick operations

**Contents**: Markdown files with YAML frontmatter
- One command per file
- Filename: lowercase-with-hyphens.md
- Must have `description` field
- 8-12 commands recommended

**Command categories**:
- Essential: build, test, run, lint
- Development: create-component, install, clean
- Deployment: deploy, validate, build-prod

### .claude/agents/
**Purpose**: Specialized AI assistants

**Contents**: Markdown files with YAML frontmatter
- One agent per file
- Filename: lowercase-with-hyphens.md
- Must have `name` and `description`
- Description should include PROACTIVELY or MUST BE USED
- 4-6 agents recommended

**Agent categories**:
- Security: framework-specific vulnerability detection
- Performance: optimization and profiling
- Testing: test generation
- Expert: deep framework knowledge
- Optional: accessibility, API design, state management

### .claude/skills/
**Purpose**: Automated capabilities triggered by context

**Contents**: Directories with SKILL.md
- One skill per directory
- Directory name: lowercase-letters-numbers-hyphens
- Must have SKILL.md with frontmatter
- Optional: reference.md, examples/, templates/, scripts/
- 2-4 skills recommended

**Skill categories**:
- Patterns: design pattern implementation
- Generation: code/config generation
- Validation: best practices checking

### Root Files

**README.md**:
- Template overview
- What's included
- Quick start
- Commands/agents/skills documentation
- Development workflow
- Troubleshooting
- Resources

**CLAUDE.md**:
- Framework overview and version
- Project structure
- Common commands
- Code conventions
- Best practices
- Security considerations
- Performance patterns
- Testing strategy
- Official docs links

**setup_instructions.md**:
- Prerequisites
- Step-by-step setup
- Environment configuration
- Database setup (if applicable)
- First component creation
- Running tests
- Deployment guide
- Common issues

**.gitignore**:
- Framework-specific patterns
- .env exclusion
- Build/dist exclusion
- .claude/*.local.* exclusion

**.env.example**:
- All environment variables
- Helpful comments
- No actual secrets
- Grouped logically

**.claude/settings.json**:
- Model configuration
- Environment variables
- Permissions
- Hooks (auto-formatting)

## Creating Template Structure

### Step 1: Create Base Directories

```bash
mkdir -p template-name/.claude/commands
mkdir -p template-name/.claude/agents
mkdir -p template-name/.claude/skills
```

### Step 2: Create Root Files

```bash
touch template-name/README.md
touch template-name/CLAUDE.md
touch template-name/setup_instructions.md
touch template-name/.gitignore
touch template-name/.env.example
touch template-name/.claude/settings.json
```

### Step 3: Framework-Specific Structure

Add framework-specific directories and files:

**Python/Django**:
```bash
mkdir -p template-name/static
mkdir -p template-name/templates
mkdir -p template-name/media
touch template-name/requirements.txt
```

**JavaScript/React**:
```bash
mkdir -p template-name/src
mkdir -p template-name/public
touch template-name/package.json
touch template-name/tsconfig.json
```

**Rust**:
```bash
mkdir -p template-name/src
touch template-name/Cargo.toml
```

## File Organization Best Practices

### Commands Organization
- Group related commands in subdirectories if >15 commands
- Example: `.claude/commands/frontend/`, `.claude/commands/backend/`
- Use clear, descriptive filenames

### Agents Organization
- Keep flat structure in `.claude/agents/`
- Use descriptive names: `framework-security.md`, not `security.md`
- One clear specialty per agent

### Skills Organization
- Each skill in its own directory
- Add supporting files as needed:
  - `reference.md` for detailed API docs
  - `examples/` for code samples
  - `templates/` for reusable code templates
  - `scripts/` for helper scripts

### Documentation Organization
- Keep root docs focused and clear
- Use consistent formatting
- Include tables of contents for long docs
- Link between related docs

## Validation Checklist

When implementing template structure:

**Directories**:
- [ ] `.claude/commands/` exists
- [ ] `.claude/agents/` exists
- [ ] `.claude/skills/` exists
- [ ] Framework-specific directories created

**Root Files**:
- [ ] README.md present
- [ ] CLAUDE.md present
- [ ] setup_instructions.md present
- [ ] .gitignore present
- [ ] .env.example present
- [ ] .claude/settings.json present
- [ ] Dependency file present (requirements.txt, package.json, etc.)

**Commands**:
- [ ] 8+ command files
- [ ] All have .md extension
- [ ] All use lowercase-with-hyphens naming
- [ ] All have YAML frontmatter with description

**Agents**:
- [ ] 4+ agent files
- [ ] All have .md extension
- [ ] All use lowercase-with-hyphens naming
- [ ] All have YAML frontmatter with name and description

**Skills**:
- [ ] 2+ skill directories
- [ ] Each has SKILL.md
- [ ] All use proper naming convention
- [ ] All have YAML frontmatter

**Consistency**:
- [ ] Follows django-template pattern
- [ ] Naming conventions consistent
- [ ] File structure logical
- [ ] Documentation complete

## Common Mistakes to Avoid

❌ **Inconsistent naming**: Using CamelCase or underscores instead of lowercase-with-hyphens

❌ **Missing required files**: Forgetting README.md, CLAUDE.md, or setup_instructions.md

❌ **Insufficient commands**: Having fewer than 8 commands (template feels incomplete)

❌ **Vague agent names**: Using "helper.md" instead of specific names like "security-auditor.md"

❌ **Flat skill structure**: Putting SKILL.md in `.claude/skills/` instead of a subdirectory

❌ **Missing .env.example**: Users won't know what environment variables are needed

❌ **Generic .gitignore**: Not including framework-specific exclusions

## Framework-Specific Considerations

### Python Projects
- Include pytest.ini or setup.cfg if using pytest
- Add requirements-dev.txt for development dependencies
- Consider pipfile if using pipenv

### JavaScript/TypeScript Projects
- Include package-lock.json or yarn.lock (or note in .gitignore)
- Add tsconfig.json for TypeScript
- Include .eslintrc and .prettierrc for code quality
- Add jest.config.js if using Jest

### Rust Projects
- Include Cargo.lock (or note when to commit/ignore)
- Add .cargo/config.toml for custom build configuration
- Include rust-toolchain.toml for version pinning

### Go Projects
- Include go.mod and go.sum
- Add .golangci.yml for linting
- Include Makefile for common operations

## Implementation Process

1. **Create base structure**: Directories and placeholder files
2. **Add framework files**: Dependencies, configurations
3. **Generate commands**: Based on framework workflows
4. **Create agents**: Based on framework needs
5. **Develop skills**: Based on common patterns
6. **Write documentation**: Complete all root files
7. **Validate structure**: Check against standards

This skill ensures all templates follow consistent, comprehensive structure patterns.
