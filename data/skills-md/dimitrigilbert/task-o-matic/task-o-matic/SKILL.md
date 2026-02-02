---
name: task-o-matic
description: AI-powered task management CLI for project initialization, PRD parsing, task breakdown, and execution with multi-provider AI support
---

# Task-O-Matic

AI-powered task management CLI for single projects. Helps initialize projects, parse PRDs into tasks, break down work with AI, and execute tasks with automatic retry and verification.

## When to Use

Use when the user wants to:
- Initialize a new project with task-o-matic
- Attach task-o-matic to an existing project (detect stack automatically)
- Parse a PRD (Product Requirements Document) into structured tasks
- Break down tasks into smaller subtasks using AI
- Enhance tasks with AI-powered documentation research
- Execute tasks with AI coding assistants
- Configure AI providers and models

## CLI Location

The CLI binary is at: `packages/cli/dist/cli/bin.js` (after building)

Run with: `node packages/cli/dist/cli/bin.js <command> [options]`

Or if installed globally: `task-o-matic <command> [options]`

## Core Workflow

```
# New project workflow
1. Initialize project (task-o-matic init init)
2. Configure AI provider (task-o-matic config set-ai-provider)
3. Parse PRD into tasks (task-o-matic prd parse)
4. Split tasks into subtasks (task-o-matic tasks split --all)
5. Execute tasks (task-o-matic tasks execute-loop)

# Existing project workflow
1. Attach to existing project (task-o-matic init attach)
2. Configure AI provider (task-o-matic config set-ai-provider)
3. Generate PRD from codebase (task-o-matic prd generate --from-codebase)
4. Create tasks from PRD (task-o-matic prd parse)
5. Execute tasks (task-o-matic tasks execute-loop)
```

## Common Commands

### Initialize Project

```bash
# Basic initialization
task-o-matic init init --project-name my-app --package-manager bun

# With specific AI provider
task-o-matic init init --project-name my-app --ai-provider openrouter --ai-model xiaomi/mimo-v2-flash:free

# With Better-T-Stack bootstrap
task-o-matic init init --project-name my-app --frontend next --backend convex --auth better-auth
```

**Options:**
- `--ai-provider <provider>`: AI provider (openrouter/anthropic/openai/custom)
- `--ai-model <model>`: AI model
- `--project-name <name>`: Project name
- `--package-manager <pm>`: bun/npm/pnpm (default: npm)
- `--frontend <frontends...>`: Frontend framework(s) (default: next)
- `--backend <backend>`: Backend framework (default: convex)
- `--auth <auth>`: Authentication (default: better-auth)
- `--directory <dir>`: Working directory

### Attach to Existing Project

```bash
# Attach to existing project (auto-detect stack)
task-o-matic init attach

# With full project analysis
task-o-matic init attach --analyze

# Dry run (just show detection, don't create files)
task-o-matic init attach --dry-run

# Force re-detection (update cached stack.json)
task-o-matic init attach --redetect
```

**Options:**
- `--analyze`: Run full project analysis (TODOs, features, structure)
- `--dry-run`: Just detect stack, don't create files
- `--redetect`: Force re-detection (overwrites cached stack.json)
- `--ai-provider <provider>`: AI provider (openrouter/anthropic/openai/custom)
- `--ai-model <model>`: AI model
- `--context7-api-key <key>`: Context7 API key

**What it detects:**
- Language (TypeScript/JavaScript)
- Framework(s) (Next.js, Express, Hono, etc.)
- Database (Postgres, MongoDB, SQLite, etc.)
- ORM (Prisma, Drizzle, etc.)
- Auth (Better-Auth, Clerk, NextAuth, etc.)
- Package Manager (npm, pnpm, bun, yarn)
- Runtime (Node, Bun)
- API style (tRPC, GraphQL, REST)
- Testing frameworks
- Build tools

**What it creates:**
- `.task-o-matic/config.json` - AI settings
- `.task-o-matic/stack.json` - Cached stack detection (used by AI context)
- `.task-o-matic/mcp.json` - Context7 config
- `.task-o-matic/tasks/` - Task storage
- `.task-o-matic/prd/` - PRD storage
- Updates `.gitignore` if git exists

### Configure AI Provider

```bash
# Set provider and model
task-o-matic config set-ai-provider openrouter xiaomi/mimo-v2-flash:free

# Set with custom URL
task-o-matic config set-ai-provider custom https://api.example.com

# Check current config
task-o-matic config get-ai-config
```

### Generate PRD from Codebase

```bash
# Analyze current project and generate PRD
task-o-matic prd generate

# With streaming output
task-o-matic prd generate --stream

# With custom output filename
task-o-matic prd generate --output my-project-prd.md
```

### Parse PRD

```bash
# Basic parse
task-o-matic prd parse --file prd.md

# With streaming output
task-o-matic prd parse --file prd.md --stream

# With reasoning tokens (for models that support it)
task-o-matic prd parse --file prd.md --ai-reasoning 4000 --stream

# Multiple models with combination
task-o-matic prd parse --file prd.md --ai openrouter:model1 openrouter:model2 --combine-ai openrouter:combine-model
```

**Options:**
- `--file <path>`: Path to PRD file (required)
- `--stream`: Show streaming AI output
- `--ai-reasoning <tokens>`: Max reasoning tokens for supported models
- `--ai <models...>`: Multiple AI models
- `--combine-ai <provider:model>`: Model to combine results
- `--tools`: Enable filesystem tools for project analysis

### Work with Tasks

#### List Tasks

```bash
task-o-matic tasks list

# With filters
task-o-matic tasks list --status todo
task-o-matic tasks list --tag frontend
```

#### Create Task

```bash
# Manual creation
task-o-matic tasks create --title "Add authentication" --content "Implement OAuth2 login"

# With AI enhancement
task-o-matic tasks create --title "Add authentication" --ai-enhance --stream
```

#### Split Tasks

```bash
# Split specific task
task-o-matic tasks split --task-id 1 --stream

# Split all tasks
task-o-matic tasks split --all --stream

# With filters
task-o-matic tasks split --all --status todo --stream
```

**Options:**
- `--task-id <id>`: Specific task to split
- `--all`: Split all tasks without subtasks
- `--status <status>`: Filter by status (todo/in-progress/completed)
- `--stream`: Show streaming output
- `--ai-reasoning <tokens>`: Enable reasoning
- `--dry`: Preview without changes

#### Enhance Tasks

```bash
# Enhance specific task
task-o-matic tasks enhance --task-id 1 --stream

# Enhance all tasks
task-o-matic tasks enhance --all --stream

# With filter
task-o-matic tasks enhance --all --status todo --stream
```

**Options:**
- `--task-id <id>`: Specific task to enhance
- `--all`: Enhance all tasks
- `--status <status>`: Filter by status
- `--tag <tag>`: Filter by tag
- `--dry`: Preview without changes
- `--force`: Skip confirmation

#### Task Status

```bash
# Set task status
task-o-matic tasks status --task-id 1 --status in-progress

# Available statuses: todo, in-progress, completed
```

#### Task Tree

```bash
# Show hierarchical task tree
task-o-matic tasks tree
```

#### Get Next Task

```bash
# Get next task to work on
task-o-matic tasks get-next
```

### Execute Tasks

```bash
# Execute all todo tasks
task-o-matic tasks execute-loop --status todo

# Execute specific tasks
task-o-matic tasks execute-loop --ids 1,2,3

# With specific tool
task-o-matic tasks execute-loop --tool claude

# With planning phase
task-o-matic tasks execute-loop --plan --review-plan

# With verification
task-o-matic tasks execute-loop --verify "bun run test" --verify "bun run type-check"

# Progressive model escalation
task-o-matic tasks execute-loop --try-models "gpt-4o-mini,gpt-4o,claude:sonnet-4"
```

**Options:**
- `--status <status>`: Filter by status
- `--tag <tag>`: Filter by tag
- `--ids <ids>`: Comma-separated task IDs
- `--tool <tool>`: opencode/claude/gemini/codex (default: opencode)
- `--max-retries <number>`: Max retries per task (default: 3)
- `--model <model>`: Force specific model
- `--verify <command>`: Verification command (can be used multiple times)
- `--plan`: Generate implementation plan before execution
- `--plan-model <model>`: Model for planning
- `--review-plan`: Pause for human review of plan
- `--review`: Run AI review after execution
- `--auto-commit`: Auto-commit after each task
- `--try-models <models>`: Progressive models for retries
- `--dry`: Show what would execute

### PRD Management

#### Create PRD from Description

```bash
task-o-matic prd create "Build a task management app with real-time updates"
```

#### Refine PRD with Questions

```bash
# Generate questions, answer interactively, refine PRD
task-o-matic prd refine --file prd.md --output prd_refined.md --stream

# Questions mode: AI generates clarifying questions
task-o-matic prd question --file prd.md
```

#### Combine PRDs

```bash
task-o-matic prd combine --files prd1.md,prd2.md --output master.md
```

#### Get Tech Stack Suggestion

```bash
task-o-matic prd get-stack --file prd.md
```

### Interactive Workflow

The `workflow` command provides an all-in-one interactive experience:

```bash
# Full interactive workflow
task-o-matic workflow

# Skip specific steps
task-o-matic workflow --skip-bootstrap --skip-prd-question-refine

# Auto-accept all suggestions
task-o-matic workflow --auto-accept

# Use config file
task-o-matic workflow --config-file workflow-config.json
```

**Workflow covers:**
- Project initialization
- PRD creation/upload
- PRD question & refinement
- Task generation
- Task splitting
- Task execution

## AI Providers

### OpenRouter

```bash
task-o-matic config set-ai-provider openrouter xiaomi/mimo-v2-flash:free
```

Popular free models:
- `xiaomi/mimo-v2-flash:free`
- `google/gemma-3-27b-it:free`
- `meta-llama/llama-3.3-8b-instruct:free`

### Anthropic

```bash
task-o-matic config set-ai-provider anthropic claude-3-5-sonnet-20241022
```

### OpenAI

```bash
task-o-matic config set-ai-provider openai gpt-4o
```

### Custom

```bash
task-o-matic config set-ai-provider custom https://api.example.com
```

## Environment Variables

Set in `.env` file or environment:

```bash
AI_PROVIDER=openrouter
AI_MODEL=xiaomi/mimo-v2-flash:free
OPENROUTER_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
```

## Project Structure

After initialization:

```
.task-o-matic/
├── config.json       # Project configuration
├── tasks.json        # Tasks database
├── prd.md            # PRD file
└── plans/            # Implementation plans
```

## Best Practices

1. **Always use `--stream`** for long-running AI operations to see progress
2. **Use `--ai-reasoning`** with models that support it for better task breakdown
3. **Filter by status** when splitting/enhancing to avoid reprocessing completed tasks
4. **Use `--dry`** first for bulk operations to preview changes
5. **Start with free models** (OpenRouter free tier) before using paid models
6. **Use `--verify`** during execution to run tests after each task
7. **Enable `--plan`** for complex tasks to get implementation plans first

## Example Session

```bash
# 1. Initialize
task-o-matic init init --project-name my-app --package-manager bun

# 2. Configure AI (optional if set in .env)
task-o-matic config set-ai-provider openrouter xiaomi/mimo-v2-flash:free

# 3. Parse PRD
task-o-matic prd parse --file prd.md --stream --ai-reasoning 4000

# 4. Review tasks
task-o-matic tasks tree

# 5. Split all tasks
task-o-matic tasks split --all --stream --ai-reasoning 4000

# 6. Enhance tasks with documentation
task-o-matic tasks enhance --all --stream

# 7. Execute
task-o-matic tasks execute-loop --status todo --verify "bun run test" --plan
```

## Advanced Topics

### Progressive Model Escalation

Use cheaper models first, escalate to better ones on failure:

```bash
task-o-matic tasks execute-loop \
  --try-models "xiaomi/mimo-v2-flash:free,gpt-4o-mini,claude:sonnet-4" \
  --max-retries 3
```

### Planning Phase

Generate implementation plans before execution:

```bash
task-o-matic tasks execute-loop \
  --plan \
  --plan-model gpt-4o \
  --review-plan
```

### Custom Verification

Run multiple verification commands:

```bash
task-o-matic tasks execute-loop \
  --verify "bun run type-check" \
  --verify "bun run test" \
  --verify "bun run lint"
```

## See Also

- [Complete Command Reference](REFERENCES.md) - Detailed command options
- [Project README](../../README.md) - Full project documentation
- [Tutorial](../../TUTORIAL.md) - Step-by-step guide
