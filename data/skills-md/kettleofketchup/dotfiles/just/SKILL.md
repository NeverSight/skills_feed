---
name: just
description: Bootstrap repos with just command runner. Use when setting up new projects, creating justfiles, or adding task automation. Provides ./dev bootstrap script that installs just, modular justfile structure in just/ directory, and recipe conventions.
---

# Just Command Runner

Task automation using [just](https://github.com/casey/just) with a standardized project structure.

## Project Structure

```
project/
├── dev                 # Bootstrap script (installs just, runs `just dev`)
├── justfile            # Root: settings, imports, and modules
└── just/
    ├── dev.just        # Development recipes (imported, no namespace)
    ├── go.just         # Go module (go::build, go::test)
    ├── docker.just     # Docker module (docker::build, docker::push)
    └── lua.just        # Lua module (lua::install, lua::check)
```

## Bootstrapping a New Repo

1. Copy `assets/dev` to project root, make executable: `chmod +x dev`
2. Copy `assets/just/` directory to project root
3. Create root `justfile` with imports and modules
4. Edit `just/dev.just` with project-specific setup commands
5. Add additional `.just` modules as needed

## Quick Reference

### Root Justfile (Recommended Pattern)

**Put everything in root justfile** for tab completion to work:

```just
# justfile (root)
set quiet
set dotenv-load

# Imports: merged into root namespace
import 'just/dev.just'

# Modules: namespaced with :: syntax (specify path)
mod go 'just/go.just'           # go::build, go::test
mod docker 'just/docker.just'   # docker::build, docker::push
mod lua 'just/lua.just'         # lua::install, lua::check

default:
    just --list
```

### Module Example

```just
# just/go.just - called as go::build, go::test, etc.
VERSION := `git describe --tags --always 2>/dev/null || echo "dev"`
BIN_DIR := env_var("PWD") / "bin"

# Build the application
[group('go')]
build tool:
    @mkdir -p {{BIN_DIR}}
    go build -o {{BIN_DIR}}/{{tool}} .

# Run tests
[group('go')]
test tool:
    go test -race -cover ./...

# Run linter
[group('go')]
lint:
    golangci-lint run
```

### Import vs Module

| Feature | `import 'just/file.just'` | `mod name 'just/name.just'` |
|---------|---------------------------|----------------------------|
| Namespace | Merged into parent | Separate (`name::*`) |
| Calling | `just recipe` | `just name::recipe` |
| Working dir | Parent justfile's dir | Module's directory |
| Best for | dev.just only | All other modules |

**Rule of thumb:** Use `import` only for `dev.just`. Use `mod` for everything else.

### Module Working Directory

**Critical:** Module recipes run from the module's directory, not the invoking justfile's directory. This breaks commands like `git submodule status` when the module is in a subdirectory.

**Solution:** Add `[no-cd]` to recipes that need to run from the invocation directory:

```just
# just/git.just - Module for git operations
# Without [no-cd], git commands would run from just/ directory

[no-cd]
status:
    git submodule status

[no-cd]
update:
    git submodule update --remote --merge
```

**When to use `[no-cd]`:**
- Git operations (submodules, status, diff)
- Any command that operates on the project root
- Commands that expect to find files relative to where `just` was invoked

**Alternative:** Use `{{invocation_directory()}}` for specific paths:
```just
build:
    go build -o {{invocation_directory()}}/bin/app .
```

### Common Dev Module (Imported)

```just
# just/dev.just - Imported (no namespace) for common recipes

# Bootstrap the development environment
dev:
    echo "Installing dependencies..."
    # npm install / pip install -r requirements.txt / cargo build
    echo "Done!"

# Clean build artifacts
clean:
    rm -rf dist/ build/ target/
```

### Tool Module Example

```just
# just/lua.just - Called as lua::install, lua::check, etc.
lua_version := env("LUA_VERSION", "5.4.6")
prefix := env("PREFIX", "/usr/local")

# Install complete lua environment
[group('lua')]
default: check install
    echo "Lua environment setup complete"

# Check current installation status
[group('lua')]
check:
    command -v lua >/dev/null 2>&1 || echo "lua not found"

# Install all components
[group('lua')]
install: install-deps install-lua install-luarocks
    echo "Lua installation complete"

# Clean build artifacts
[group('lua')]
clean:
    rm -rf /tmp/lua-build/*
```

### Listing Recipes

```bash
just --list                    # Shows modules collapsed
just --list --list-submodules  # Shows all module recipes expanded
just lua::                     # Tab-complete shows lua recipes
```

## Shell Completions Setup

When setting up just for a user, check if shell completions are configured and set them up if missing.

### Detection

Check if `_just` completion function exists:

```bash
# For zsh
type _just &>/dev/null

# For bash
type _just &>/dev/null || complete -p just &>/dev/null
```

### Setup Steps

If completions don't exist:

1. **Create completions directory** (respects XDG):
   ```bash
   JUST_CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/just"
   mkdir -p "$JUST_CONFIG_DIR"
   ```

2. **Generate completions file**:
   ```bash
   # For zsh
   just --completions zsh > "$JUST_CONFIG_DIR/completions.zsh"

   # For bash
   just --completions bash > "$JUST_CONFIG_DIR/completions.bash"
   ```

3. **Add sourcing to shell rc** (if not already present):

   For **zsh** (`~/.zshrc`):
   ```bash
   # just completions
   if command -v just &>/dev/null; then
       [[ -f "${XDG_CONFIG_HOME:-$HOME/.config}/just/completions.zsh" ]] && source "${XDG_CONFIG_HOME:-$HOME/.config}/just/completions.zsh"
   fi
   ```

   For **bash** (`~/.bashrc`):
   ```bash
   # just completions
   if command -v just &>/dev/null; then
       [[ -f "${XDG_CONFIG_HOME:-$HOME/.config}/just/completions.bash" ]] && source "${XDG_CONFIG_HOME:-$HOME/.config}/just/completions.bash"
   fi
   ```

### Verification

After adding, verify with:
```bash
source ~/.zshrc  # or ~/.bashrc
type _just  # should show completion function
```

## References

Detailed syntax and patterns in `references/`:

| File | Contents |
|------|----------|
| `modules.md` | Module system (`mod`), namespacing with `::`, import vs mod |
| `settings.md` | All justfile settings (`set quiet`, `set dotenv-load`, etc.) |
| `recipes.md` | Recipe syntax, parameters, dependencies, shebang recipes |
| `attributes.md` | Recipe attributes (`[group]`, `[confirm]`, `[private]`, etc.) |
| `functions.md` | Built-in functions (`env()`, `os()`, `join()`, etc.) |
| `syntax.md` | Variables, strings, conditionals, imports |
