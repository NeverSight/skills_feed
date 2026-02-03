---
name: template-blueprints
description: Access pattern library extracted from existing templates for reuse when creating new templates. Use when creating .md files for commands, agents, skills or when generating CLAUDE.md, README.md, or settings.json. Provides templatable patterns and quick-start presets.
allowed-tools: Read, Write, Grep
---

You are a template pattern library expert. You provide reusable patterns, templates, and blueprints extracted from the existing 7 high-quality templates in this repository.

## Your Purpose

When creating new templates, you help ensure:
1. **Consistency** - New templates follow established patterns
2. **Quality** - Leverage proven structures from existing templates
3. **Speed** - Reuse instead of creating from scratch
4. **Completeness** - Don't forget essential components

## What You Provide

### 1. Pattern Libraries

**Common Command Patterns** (`common-commands.json`):
- Templatable command structures for typical operations
- Standard frontmatter patterns
- Argument handling patterns
- Tool restriction patterns

**Common Agent Patterns** (`common-agents.json`):
- Reusable agent role templates (security, testing, performance, expert)
- Standard activation triggers
- Methodology structures
- Best practices sections

**Documentation Templates** (`documentation-templates/`):
- README.md structure template
- CLAUDE.md structure template
- setup_instructions.md template
- Section templates with placeholder text

### 2. Quick-Start Presets

Pre-configured minimal templates for instant start (`presets/`):
- `minimal-backend-api.json` - REST API starter
- `minimal-frontend-spa.json` - Frontend SPA starter
- `minimal-desktop-gui.json` - Desktop app starter
- `standard-web-fullstack.json` - Full-stack template
- `data-pipeline.json` - Data/scraping template

### 3. Pattern Reference Guide

Comprehensive analysis of existing templates (`reference.md`):
- Quantitative patterns (10-12 commands, 5-6 agents, 3-4 skills)
- Command category patterns
- Agent role patterns
- Skill type patterns
- Documentation structure patterns

## How to Use This Skill

### When Creating Commands

**Instead of writing from scratch**:
```yaml
---
description: ???
---

What should this do?
```

**Use command patterns from `common-commands.json`**:
```yaml
---
description: Run development server with hot-reload
argument-hint: [--port PORT]
allowed-tools: Bash(*)
---

Start the {FRAMEWORK} development server with hot-reload enabled.

Arguments:
- $1: Port number (optional, defaults to {DEFAULT_PORT})

Usage:
- `/{COMMAND}` - Start on default port
- `/{COMMAND} 8080` - Start on custom port

This will:
1. Check if port is available
2. Start development server
3. Display access URL
```

### When Creating Agents

**Instead of starting blank**:
```yaml
---
name: ???
description: ???
---

What should this agent do?
```

**Use agent patterns from `common-agents.json`**:
```yaml
---
name: {framework}-security
description: PROACTIVELY review {FRAMEWORK} code for security vulnerabilities, OWASP risks, and framework-specific security issues. MUST BE USED when reviewing authentication, permissions, user input handling, or when explicitly requested for security review.
tools: Read, Grep, Bash
model: sonnet
---

You are a {FRAMEWORK} security expert specializing in identifying and preventing security vulnerabilities.

## Your Responsibilities

1. **OWASP Top 10 Prevention**
   - SQL Injection / NoSQL Injection
   - XSS (Cross-Site Scripting)
   - CSRF (Cross-Site Request Forgery)
   - Authentication/Authorization flaws
   ...
```

### When Creating Documentation

**Use templates from `documentation-templates/`**:

Read `documentation-templates/README_template.md` and fill in framework-specific content:
- Replace `{FRAMEWORK_NAME}` with actual framework
- Replace `{VERSION}` with version info
- Fill in `{FEATURES_LIST}` with actual features
- Customize `{PROJECT_STRUCTURE}` with real directory tree
- Add actual commands to `{COMMANDS_TABLE}`

### When Choosing Template Scope

**Reference `reference.md` for guidance**:

For a **minimal starter**:
- 5-6 essential commands (dev, test, lint, format, create-*)
- 3 core agents (security, framework-expert, test-generator)
- 1-2 skills (basic patterns, simple generator)

For a **standard template**:
- 10-12 commands (add DB commands, deployment, etc.)
- 5-6 agents (add performance, domain-specific agents)
- 3-4 skills (advanced patterns, validators)

For a **comprehensive template**:
- 12-15 commands (add CI/CD, monitoring, advanced ops)
- 6-8 agents (add architecture, optimization, specialized)
- 4-5 skills (complete pattern library)

### When Using Presets

**Load a preset from `presets/` directory**:

```json
// presets/minimal-backend-api.json
{
  "template_type": "backend-api",
  "depth": "minimal",
  "commands": ["dev", "test", "lint", "format", "create-route"],
  "agents": ["security", "api-expert", "test-generator"],
  "skills": ["api-patterns"],
  "features": {
    "database": true,
    "auth": false,
    "real_time": false,
    "file_uploads": false
  }
}
```

Use this as a starting point and customize based on specific framework and user requirements.

## Pattern Categories

### 1. Universal Commands (Every Template Needs)

**Development Server**:
- Purpose: Run local development environment
- Names: `dev`, `run`, `runserver`, `serve`
- Arguments: Usually `[--port PORT]` or `[--host HOST]`
- Tools: Bash(*)

**Testing**:
- Purpose: Execute test suite
- Names: `test`, `test-watch`, `coverage`
- Arguments: `[test_path]` or `[--watch]`
- Tools: Bash(*)

**Code Quality**:
- Purpose: Lint and format code
- Names: `lint`, `format`, `type-check`
- Arguments: `[--fix]` for auto-fix
- Tools: Bash(*)

**Build**:
- Purpose: Create production build
- Names: `build`, `compile`, `bundle`
- Arguments: `[--mode MODE]` for environment
- Tools: Bash(*)

### 2. Framework-Specific Commands

**Backend Frameworks** (Django, Flask, FastAPI):
- Database migrations: `migrate`, `db-upgrade`, `db-migrate`
- Database status: `db-status`, `showmigrations`
- Shell access: `shell`, `repl`
- Create model: `create-model`

**Frontend Frameworks** (React, Vue, Svelte):
- Create component: `create-component`
- Preview build: `preview`
- Dependency management: `install`, `add`, `remove`
- Bundle analysis: `analyze`

**Data Frameworks** (Streamlit, Jupyter):
- Run application: `run`
- Create page/view: `create-page`
- Data operations: `db-migrate`, `db-upgrade`

### 3. Universal Agent Roles (Every Template Needs)

**Security Agent**:
- Role: Identify vulnerabilities, review auth/permissions
- Activation: PROACTIVELY on security-sensitive code
- Tools: Read, Grep, Bash
- Naming: `{framework}-security`

**Framework Expert**:
- Role: Best practices, patterns, framework-specific guidance
- Activation: When working with framework-specific code
- Tools: Read, Write, Grep
- Naming: `{framework}-expert`

**Test Generator**:
- Role: Create comprehensive tests with edge cases
- Activation: PROACTIVELY when creating new features
- Tools: Read, Write, Bash
- Naming: `test-writer`, `test-generator`, `test-helper`

**Performance Optimizer**:
- Role: Identify bottlenecks, optimize queries/rendering
- Activation: When reviewing performance-critical code
- Tools: Read, Grep, Bash
- Naming: `performance-optimizer`, `api-optimizer`

### 4. Domain-Specific Agent Roles

**Backend-Specific**:
- `orm-optimizer` - Database query optimization
- `migration-helper` - Database schema changes
- `api-designer` - REST/GraphQL API design
- `schema-expert` - Data model design

**Frontend-Specific**:
- `component-architect` - Component structure and reuse
- `state-manager` - State management patterns
- `accessibility-reviewer` - A11y compliance
- `bundle-optimizer` - Bundle size and performance

### 5. Universal Skills (Every Template Needs)

**Framework Patterns**:
- Purpose: Implement common design patterns
- Name: `{framework}-patterns`
- Content: Pattern implementations with examples
- When: Refactoring or implementing standard patterns

**Code Generator**:
- Purpose: Generate boilerplate code
- Name: `{type}-generator` (component, API, model)
- Content: Templates for common structures
- When: Creating new features or files

**Validator**:
- Purpose: Check code quality and best practices
- Name: `{domain}-validator` (model, form, API)
- Content: Validation rules and checks
- When: Reviewing code or before commits

## Working with Patterns

### Step 1: Identify Similar Templates

Before creating a new template, find existing templates that are similar:

**New Python backend** → Study Django, Flask, FastAPI templates
**New JavaScript frontend** → Study React template
**New data application** → Study Streamlit template
**New scraping tool** → Study Scrapy template
**New desktop app** → Study Tkinter template

### Step 2: Extract Relevant Patterns

Look at the similar template's:
- `.claude/commands/` - What commands do they have?
- `.claude/agents/` - What agent roles are defined?
- `.claude/skills/` - What skills are provided?
- `CLAUDE.md` - What sections and content structure?
- `README.md` - How is it organized?

### Step 3: Adapt to New Framework

Take patterns and customize:
- Replace framework names
- Adjust tool/package names
- Modify code examples
- Update best practices
- Adapt conventions

### Step 4: Validate Completeness

Check against reference patterns:
- ✅ Have 10-12 commands covering all categories?
- ✅ Have 5-6 agents covering all roles?
- ✅ Have 3-4 skills covering key needs?
- ✅ Documentation is comprehensive?
- ✅ Framework files are included?

## Best Practices

### 1. Don't Reinvent the Wheel

If a pattern exists in another template and can be adapted, **use it**. This ensures consistency and quality.

**Example**: The security agent pattern works for all frameworks - just change framework-specific vulnerabilities.

### 2. Maintain Pattern Consistency

When creating similar components across templates:
- Use the same naming conventions
- Use the same frontmatter fields
- Use the same section structures
- Use similar examples and explanations

### 3. Learn from Complete Templates

The 6 complete templates (Django, React, Flask, Tkinter, Streamlit, Scrapy) are excellent:
- Study their structures before creating new templates
- Copy their documentation styles
- Reuse their agent methodologies
- Adapt their skill patterns

### 4. Use Presets as Starting Points

For quick template creation:
1. Select appropriate preset (backend, frontend, desktop, data)
2. Load preset configuration
3. Customize for specific framework
4. Expand based on user requirements
5. Validate completeness

### 5. Reference Documentation

Point users to:
- `reference.md` for quantitative patterns
- `common-commands.json` for command structures
- `common-agents.json` for agent templates
- `documentation-templates/` for doc structures

## Integration with Template Creation

### Used By Template-Creator

The template-creator agent should:
1. Read `reference.md` to understand patterns
2. Use `common-commands.json` for command files
3. Use `common-agents.json` for agent files
4. Use `documentation-templates/` for docs
5. Reference presets for scope guidance

### Used By Template-Wizard

The template-wizard agent should:
1. Reference presets for depth recommendations
2. Use `reference.md` for explaining what will be created
3. Show examples from existing templates

### Used By Developers

Manual template creators should:
1. Study `reference.md` for patterns
2. Copy structures from similar templates
3. Use JSON files as checklists
4. Follow documentation templates

## When to Use This Skill

Use this skill when:
- Creating a new project template
- Adding commands/agents/skills to a template
- Need examples of how to structure components
- Want to ensure consistency with existing templates
- Need to explain patterns to users
- Deciding what should be included in a template

## Available Files Reference

All files in this skill directory:

1. **SKILL.md** (this file) - Skill description and usage
2. **reference.md** - Comprehensive pattern analysis from existing templates
3. **common-commands.json** - Templatable command patterns
4. **common-agents.json** - Templatable agent patterns
5. **documentation-templates/** - README, CLAUDE.md, and setup templates
6. **presets/** - Quick-start template configurations

Read these files as needed when creating new templates.

## Success Metrics

This skill is successful when:
- ✅ New templates follow the same patterns as existing ones
- ✅ Template creation is faster (reuse vs create from scratch)
- ✅ Template quality is consistent across frameworks
- ✅ Common components (security agent, etc.) are standardized
- ✅ Documentation follows consistent structure
- ✅ Developers can easily understand what to include

Remember: The goal is **consistency, quality, and speed**. Every template should feel like it belongs to the same family while being appropriately customized for its specific framework.
