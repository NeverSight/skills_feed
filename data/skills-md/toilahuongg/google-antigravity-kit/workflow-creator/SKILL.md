---
name: workflow-creator
description: Create and manage workflows that guide the Agent through repetitive tasks. Use this skill when users want to create new workflows, update existing workflows, or need guidance on writing effective step-by-step workflows for common operations like deployments, code reviews, testing, or any repeatable process.
---

# Workflow Creator

Create effective workflows that guide the AI Agent through structured, repeatable tasks.

## What Are Workflows?

Workflows are markdown files that define a series of steps for the Agent to follow when performing repetitive tasks. They enable:

- **Consistency** - Same process every time
- **Efficiency** - No need to re-explain steps
- **Automation** - Slash command invocation (e.g., `/deploy`)
- **Documentation** - Steps are version-controlled and shareable

## Workflow Structure

Workflows are saved to `.agent/workflows/{workflow-name}.md` with this format:

```markdown
---
description: [short description of what this workflow does]
---

# [Workflow Title]

[Brief overview of the workflow purpose]

## Prerequisites

[Optional: List any requirements before starting]

## Steps

1. [First step with clear instruction]
2. [Second step]
3. [Third step]
...

## Notes

[Optional: Additional context, warnings, or tips]
```

## Workflow Creation Process

### Step 1: Identify the Workflow

Ask the user:
1. What repetitive task do you want to automate?
2. What are the exact steps you follow each time?
3. Are there any variations or conditional paths?
4. What command name do you want? (e.g., `/deploy`, `/test`)

### Step 2: Define Steps

Write clear, actionable steps:
- Use imperative verbs ("Run", "Create", "Check")
- Include exact commands when applicable
- Specify file paths and parameters
- Note any user inputs needed

### Step 3: Add Turbo Annotations

Use annotations to auto-run safe commands:

- `// turbo` - Auto-run the next step only
- `// turbo-all` - Auto-run ALL steps in the workflow

```markdown
## Steps

1. Backup existing files

// turbo
2. Run `npm install`

3. Update configuration (requires user review)

// turbo
4. Run `npm run build`
```

### Step 4: Validate the Workflow

Check against this list:
- [ ] Clear, descriptive name and description?
- [ ] Steps are sequential and logical?
- [ ] Commands are exact and copy-pasteable?
- [ ] Turbo annotations only on safe commands?
- [ ] Prerequisites listed if any?
- [ ] Total file under 12,000 characters?

## Quick Templates

For ready-to-use templates, see [references/workflow-templates.md](references/workflow-templates.md).

### Deployment Workflow

```markdown
---
description: Deploy application to production
---

# Deploy to Production

## Prerequisites

- All tests passing
- On `main` branch

## Steps

// turbo
1. Run tests to confirm everything passes:
   ```bash
   npm run test
   ```

2. Build production bundle:
   ```bash
   npm run build
   ```

// turbo
3. Deploy to production:
   ```bash
   npm run deploy
   ```

4. Verify deployment by checking the live URL.
```

### Code Review Workflow

```markdown
---
description: Review a pull request systematically
---

# PR Review

## Steps

1. Fetch and checkout the PR branch:
   ```bash
   git fetch origin pull/<PR_NUMBER>/head:pr-<PR_NUMBER>
   git checkout pr-<PR_NUMBER>
   ```

2. Review the diff for:
   - Code quality and style
   - Security concerns
   - Test coverage
   - Performance implications

3. Run tests locally:
   ```bash
   npm run test
   ```

4. Provide feedback or approve the PR.
```

### Database Migration Workflow

```markdown
---
description: Run database migrations safely
---

# Database Migration

## Prerequisites

- Database backup completed
- Migration files ready in `migrations/`

## Steps

1. Create a backup before migration:
   ```bash
   npm run db:backup
   ```

// turbo
2. Run pending migrations:
   ```bash
   npm run db:migrate
   ```

3. Verify data integrity:
   ```bash
   npm run db:verify
   ```

4. If issues found, rollback:
   ```bash
   npm run db:rollback
   ```
```

## Output Location

Workflows must be saved in `.agent/workflows/` directory:

```
.agent/workflows/
├── deploy.md           # /deploy command
├── test.md             # /test command
├── pr-review.md        # /pr-review command
├── db-migrate.md       # /db-migrate command
└── security-scan.md    # /security-scan command
```

### File Naming

- Use kebab-case: `{workflow-name}.md`
- Name becomes the slash command: `deploy.md` → `/deploy`
- Keep names short and memorable

### Frontmatter

Required YAML frontmatter:

```yaml
---
description: [Short description shown when listing workflows]
---
```

## Managing Workflows

### Listing Workflows

Scan `.agent/workflows/` to show available commands.

### Invoking Workflows

User types `/workflow-name` to trigger:
- `/deploy` → `.agent/workflows/deploy.md`
- `/test` → `.agent/workflows/test.md`

### Updating Workflows

When updating:
1. Preserve turbo annotations unless asked to change
2. Maintain step numbering
3. Test commands before committing

## Common Workflow Categories

| Category | Examples | Description |
|----------|----------|-------------|
| **Build/Deploy** | `/deploy`, `/build`, `/release` | Compilation and deployment |
| **Testing** | `/test`, `/e2e`, `/lint` | Running test suites |
| **Database** | `/db-migrate`, `/db-seed`, `/db-backup` | Database operations |
| **Git** | `/pr-review`, `/release-notes` | Version control tasks |
| **Security** | `/security-scan`, `/audit` | Security checks |
| **Maintenance** | `/cleanup`, `/update-deps` | Maintenance tasks |
| **Development** | `/dev-setup`, `/new-feature` | Development workflows |

## Best Practices

1. **Keep steps atomic** - One action per step
2. **Be explicit** - Include exact commands, not vague instructions
3. **Use turbo wisely** - Only on safe, non-destructive commands
4. **Document prerequisites** - What must be true before starting
5. **Include rollback** - How to undo if something fails
6. **Stay under 12K chars** - Split large workflows if needed
7. **Version control** - Workflows should be committed to git
