---
name: mise-task-managing
description: Use this skill when working with mise to manage your project. All projects should rely on mise for package management, encapsulating common tasks, and consolidating devops operations.
---

# Mise-Task-Managing Skill

Comprehensive assistance with mise-task-managing development, generated from official documentation.

## When to Use This Skill

This skill should be triggered when:

- Managing tool versions and installations across projects (Node.js, Python, Ruby, etc.)
- Setting up development environments with specific runtime versions
- Creating and managing automated tasks for build/deployment/DevOps workflows
- Working with mise configuration files (mise.toml, .tool-versions)
- Managing plugins for different programming languages and tools
- Implementing CI/CD pipelines using mise tasks
- Debugging mise configuration or environment issues
- Migrating from other version managers (asdf, rbenv, nvm, pyenv, etc.)
- Installing tools via various backends (core, aqua, ubi, cargo, pipx, gem)

## Key Concepts

**Tasks**: Reusable commands defined in mise.toml that can have dependencies, file-based triggers, and parallel execution for automating workflows.

**Backends**: Different methods mise uses to install tools - built-in backends like aqua (HTTP downloads), ubi (GitHub releases), cargo (Rust tools), pipx (Python), gem (Ruby), and external asdf plugins.

**Environments**: Environment-specific configurations using .mise.<env>.toml files for different deployment contexts (staging, production, etc.).

**Fuzzy Matching**: Mise accepts partial versions everywhere (e.g., "20" for Node.js 20.x versions) for user convenience.

**Activation**: mise activate modifies PATH to point to correct tool versions, much faster than asdf's shims.

## Quick Reference

### My Standards

ALWAYS FOLLOW MY STANDARDS WHEN USING THIS SKILL. THEY SHALL OVERRIDE ANY CONFLICTING INSTRUCTIONS.

1. Task Modularity and Dependencies

Always strive to build a logical dependency hierarchy for tasks to ensure efficient execution.

- You can use `depends`, `wait_for` and `depends_post` to control the order of execution.
- Avoid flat task structures where all tasks are independent. This leads to tasks looking like a random list.
  - build
  - build:legacy
  - build:hybrid
  - test
  - test:unit
  - package:linux

If 'test' is independent of build, I would have to update an unknown number of tasks whenever I change build logic. This is UNACCEPTABLE. Mise provides a robust dependency system to avoid this.

2. Optimize Task Execution

Be smart about task execution to minimize redundant work and speed up workflows.

- Use file-based triggers (sources/outputs) to minimize unnecessary task executions.
- Leverage parallel execution for independent tasks to optimize performance.

3. Utilize Default Task Registry when Possible

Mise will automatically register tasks for any scripts found in path like this `.mise/
tasks/:task_name`

- To add a description, simply add a comment at the top of the script file like `#MISE description="Build the CLI"`

4. Use mise to manage all tools!

Including but not limited to: `node`, `pnpm`, `bun`, `cargo`, `python`, `uv`

### Basic Tool Management

**Install and use Node.js 20.x:**

```bash
mise use node@latest
```

Installs the latest Node.js 20.x version and sets it as active in the current directory.

**Install tools globally:**

```bash
mise use -g node@latest python@3.11
```

Installs and configures tools globally in ~/.config/mise/config.toml.

**List current tool versions:**

```bash
mise ls --current
```

Shows active tool versions specified in config files.

### Mise as Task Runner

**Simple build task:**

```toml
[tasks.build]
run = "npm run build"
```

Defines a basic task that runs the npm build command.

**Task with dependencies and caching:**

```toml
[tasks.build]
run = "npm run build"
sources = ["src/**/*.ts"]
outputs = ["dist/**/*.js"]
depends = ["test"]
```

Builds only when sources change, depends on test task completing first.

**Run tasks:**

```bash
mise run build
```

Executes the build task with dependency checking and parallel execution.

### Backends & Plugins

**Install via aqua backend (no plugins needed):**

```bash
mise use aqua:BurntSushi/ripgrep
```

Uses aqua to download and install ripgrep directly from GitHub releases.

**Install Ruby gem tools:**

```bash
mise use gem:rubocop
```

Installs Rubocop via RubyGems backend without separate plugins.

**Sync existing Homebrew installations:**

```bash
mise sync node --brew
```

Imports Homebrew Node.js installations into mise management.

### Configuration

**Configure parallel jobs:**

```bash
mise settings set jobs 4
```

Sets number of parallel jobs for better performance on multi-core systems.

**Environment variable management:**

```bash
mise unset NODE_ENV
```

Removes NODE_ENV from the current directory's config file.

**Format config files:**

```bash
mise fmt
```

Sorts keys and cleans up whitespace in mise.toml files.

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **cli_reference.md** - Complete command-line reference for all 50+ mise commands with flags, arguments, and examples. Use for detailed syntax of any command.
- **configuration.md** - Environment variables, settings management, and config file handling. Essential for understanding mise.toml structure and global/local configs.
- **dev_tools.md** - Backend systems (aqua, ubi, cargo, pipx, gem), plugin management, and comparison with asdf. Critical for choosing the right installation method.
- **environments.md** - Environment-specific configurations (.mise.staging.toml, etc.) and activation patterns for different deployment contexts.
- **getting_started.md** - Installation guide, basic concepts, and initial setup. Start here if new to mise.
- **tasks.md** - Task definitions, dependencies, caching, and workflow automation. Core documentation for DevOps use cases.

Use `view` to read specific reference files when detailed information is needed.

## Working with This Skill

### For Beginners

Start with getting_started.md for installation and basic concepts. Focus on simple commands:

- Use `mise use node@latest` to install tools
- Check `mise ls` to see what's installed
- Define tasks in .mise.toml for common commands

### For Intermediate Users

- Explore tasks.md for workflow automation.
- Learn different backends in dev_tools.md (aqua for CLI tools, pipx for Python packages).
- Use environments.md for project-specific configurations.

### For Advanced Users

- Dive into configuration.md for performance tuning (jobs, caching).
- Create complex task dependencies.
- Use `mise settings` for global configurations.
- Implement CI/CD with task caching and parallel execution.

### Navigation Tips

- **Automation**: tasks.md for all workflow and dependency features
- **Troubleshooting**: cli_reference.md for detailed command options
- **Multi-environment**: environments.md for .mise.<env>.toml patterns

## Resources

Links to more documentation contained in this skill

### references/

Organized documentation extracted from official sources.

### scripts/

Add helper scripts here for common automation tasks.

### assets/

Add templates, boilerplate, or example project configurations here.

## Notes

- This skill was automatically generated from official documentation
- Reference files preserve the structure and examples from source docs
