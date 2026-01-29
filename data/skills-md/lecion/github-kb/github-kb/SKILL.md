---
name: github-kb
description: Explore, research, and learn GitHub open source projects. Use when users want to understand implementation details, technical solutions, or track trending repositories. Clone repos and analyze source code based on user questions. Manage a local knowledge base with CLAUDE.md index.
---

# GitHub Knowledge Base Explorer

## Installation

Add via Claude Code plugin marketplace:

```bash
/plugin marketplace add lecion/github-kb
```

## Configuration

Set the `GITHUB_KB_ROOT` environment variable to customize the working directory.

## Working Directory

Dynamic path based on `GITHUB_KB_ROOT` environment variable (default: `~/github-kb/`).

## Knowledge Base Management

### CLAUDE.md Location

The knowledge base index is located at `{GITHUB_KB_ROOT}/CLAUDE.md`. This file indexes all explored repositories.

### CLAUDE.md Format

```markdown
# Claude Code 知识库

本目录包含 X 个 GitHub 项目，涵盖...领域描述

---

## Category Name

### [project-name](/project-name)
Brief description of the project
```

### Updating CLAUDE.md

When cloning or exploring a new repository, update CLAUDE.md to maintain consistency:

- Add the project under an appropriate category
- Include project name (linked to its directory) and brief description
- Update the project count in the header

## Workflow

### 1. Knowledge Base Lookup (First Step)

When user asks about a repository:

1. Read `{GITHUB_KB_ROOT}/CLAUDE.md` to check if the project exists
2. If found, explore the existing directory using Read, Glob, and Grep tools
3. If not found, proceed to clone

### 2. Cloning New Repositories

When user wants to explore a new repo or the repo doesn't exist:

```bash
cd {GITHUB_KB_ROOT}
git clone <repo-url>
```

- Use HTTPS or SSH based on repo accessibility
- Default clone directory is always `{GITHUB_KB_ROOT}`

### 3. Exploring and Analyzing

After cloning or when working with existing repos:

- Use the Task tool with Explore agent for comprehensive code analysis
- Use Glob/Read/Grep for targeted on: architecture, exploration
- Focus implementation details, technical decisions, key files

### 4. Maintaining the Knowledge Base

After successful exploration:

- Update CLAUDE.md with new project entry
- Include accurate category and description
- Ensure links and formatting are correct

## Categories for CLAUDE.md

Common categories for organizing projects:

- **Web Frameworks** - Frontend/backend frameworks
- **DevOps Tools** - CI/CD, deployment, infrastructure
- **Machine Learning** - ML libraries, models, tools
- **Mobile Development** - iOS, Android, cross-platform
- **Utilities** - CLI tools, productivity
- **Databases** - Database clients, ORMs
- **APIs & Services** - API clients, SDKs
- **Other** - Projects that don't fit other categories

## Environment Variables

| Variable        | Description                | Default        |
|-----------------|----------------------------|----------------|
| `GITHUB_KB_ROOT` | Root directory for clones  | `~/github-kb/` |

## Examples

```markdown
# Clone a new repository
cd $GITHUB_KB_ROOT
git clone https://github.com/example/repo.git

# Explore an existing repository
Task tool -> Explore agent -> analyze repo structure

# Update knowledge base
Edit CLAUDE.md -> add new project entry
```

## Backward Compatibility

Existing users don't need any configuration changes. The default path maintains backward compatibility.
