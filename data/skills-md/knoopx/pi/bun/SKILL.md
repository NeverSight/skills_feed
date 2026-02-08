---
name: bun
description: Initializes projects, manages dependencies, runs scripts, executes tests, and bundles code using Bun. Use when working with package.json, installing packages, running dev servers, or building for production.
---

# Bun

Fast all-in-one JavaScript runtime, bundler, test runner, and package manager.

## Quick Start

```bash
bun init              # Create new project
bun install           # Install dependencies
bun run ./file.ts     # Run a script
bun test              # Run tests
```

## Package Management

```bash
# Installation
bun add <pkg>              # Production dep
bun add -d <pkg>           # Dev dependency
bun add --optional <pkg>   # Optional dep
bun add -g <pkg>           # Global install
bun add <pkg>@^1.0.0       # Specific version
bun add <owner>/<repo>     # From git

# Management
bun remove <pkg>           # Remove package
bun update                 # Update all
bun update <pkg>           # Update specific
bun outdated               # Show outdated
bun audit                  # Security audit
bun why <pkg>              # Why installed
bun info <pkg>             # Package metadata
bun publish                # Publish to npm
bun patch <pkg>            # Patch a package
bun link                   # Link local package
bun unlink                 # Unlink local package
```

## Running Code

```bash
bun run ./file.ts          # Execute file
bun run dev                # Run script from package.json
bun -e "code"              # Eval code
bun exec ./script.sh       # Run shell script
bun run ./cli.ts arg1 arg2 # With arguments

# Long-running/watch mode (use tmux)
tmux new -d -s dev 'bun run --watch ./file.ts'
tmux new -d -s hot 'bun run --hot ./file.ts'
tmux new -d -s repl 'bun repl'
```

## Testing

```bash
bun test                   # Run all tests
bun test tests/test.ts     # Specific file
bun test --coverage        # With coverage
bun test -t "pattern"      # Filter by name
bun test --bail 3          # Stop after N failures
bun test -u                # Update snapshots
bun test --timeout 5000    # With timeout
bun test --verbose         # Verbose output

# Watch mode (use tmux)
tmux new -d -s test 'bun test --watch'
```

## Building

```bash
bun build ./src/index.ts              # Bundle
bun build --production ./src/index.ts # Minified
bun build --target=node ./src/index.ts # Node target
bun build --compile ./cli.ts          # Standalone executable
bun build --splitting ./src/index.ts  # Code splitting
bun build --outdir ./dist ./src/index.ts # Output directory
```

## Configuration

### bunfig.toml

```toml
[install]
linker = "hoisted"
minimumReleaseAge = 259200

[test]
timeout = 5000
coverage = { reporter = ["text"] }

[build]
minify = true
sourcemap = "external"
outdir = "dist"
```

### package.json

```json
{
  "name": "my-project",
  "type": "module",
  "module": "src/index.ts",
  "scripts": {
    "dev": "bun run --watch src/index.ts",
    "test": "bun test"
  }
}
```

## Workspaces

```json
{
  "workspaces": ["packages/*"],
  "catalog": {
    "react": "^18.0.0",
    "typescript": "^5.0.0"
  }
}
```

```bash
bun run --workspaces test    # Run in all workspaces
bun add <pkg> --filter <ws>  # Add to specific workspace
```

## Environment Variables

```bash
bun run --env-file=.env dev  # Load .env
VAR=value bun run ./file.ts  # Set inline
process.env.VAR              # Access in code
```

## Tips

- Use `bunx` for one-off CLIs (auto-installs)
- Commit `bun.lock` for reproducible installs
- Use `--frozen-lockfile` in CI
- Use `bun run -i` to auto-install missing deps
- Standalone executables: `bun build --compile`
- Use tmux for watch/hot modes
