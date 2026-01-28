---
name: just
description: just is a handy command runner for saving and running project-specific commands. Features include recipe parameters, .env file loading, shell completion, cross-platform support, and recipes in arbitrary languages. This skill is triggered when the user says things like "create a justfile", "write a just recipe", "run just commands", "set up project automation with just", "understand justfile syntax", or "add a task to the justfile".
---

# just - Command Runner

`just` is a command runner that lets you save and run project-specific commands (called recipes) in a `justfile`. It's similar to `make` but focused purely on running commands, not building software.

## Documentation Files

This skill includes the complete official documentation from the just repository:

- **README.md** - Comprehensive documentation including installation, syntax reference, features, and examples (this is the primary reference)
- **GRAMMAR.md** - Formal grammar specification for justfile syntax
- **CHANGELOG.md** - Version history and release notes
- **CONTRIBUTING.md** - Contribution guidelines
- **LICENSE** - CC0 1.0 Universal license
- **examples/** - Example justfiles for various use cases

## Quick Reference

### Basic Justfile Structure

```just
# This is a comment
variable := "value"

# Recipe with no dependencies
recipe-name:
    echo "Running recipe"

# Recipe with dependencies
build: clean compile
    echo "Build complete"

# Recipe with parameters
greet name:
    echo "Hello, {{name}}!"

# Recipe with default parameter
serve port="8080":
    python -m http.server {{port}}
```

### Running Recipes

```bash
just                    # Run default recipe (first in file)
just recipe-name        # Run specific recipe
just recipe arg1 arg2   # Run recipe with arguments
just --list             # List available recipes
just --show recipe      # Show recipe source
just --dry-run recipe   # Show what would run without executing
just --choose           # Interactive recipe selection (requires fzf)
```

### Key Features

- **Recipe Parameters** - Pass arguments to recipes
- **Variables** - Define and use variables with `:=`
- **String Interpolation** - Use `{{variable}}` in recipes
- **Dotenv Support** - Automatically loads `.env` files
- **Shebang Recipes** - Write recipes in Python, Node, Ruby, etc.
- **Conditional Logic** - Use `if` expressions and functions
- **Dependencies** - Recipes can depend on other recipes
- **Private Recipes** - Prefix with `_` to hide from listing
- **Documentation** - Add doc comments with `# comment` above recipes
- **Cross-Platform** - Works on Linux, macOS, Windows, BSD

### Common Settings

```just
# Load .env file
set dotenv-load

# Use different shell
set shell := ["bash", "-c"]

# Export all variables as environment variables
set export

# Allow recipes with same name as built-in functions
set allow-duplicate-recipes

# Fail immediately on error
set shell := ["bash", "-uc"]
```

### Built-in Functions

```just
# Path functions
home_dir := home_directory()
current := justfile_directory()
parent := parent_directory(current)

# String functions
upper := uppercase("hello")
lower := lowercase("HELLO")
replaced := replace("hello", "l", "x")
trimmed := trim("  spaces  ")

# Environment
value := env_var("HOME")
value_or_default := env_var_or_default("VAR", "default")

# OS detection
os := os()
arch := arch()

# Conditionals
result := if os() == "linux" { "Linux" } else { "Other" }
```

### Shebang Recipes (Other Languages)

```just
# Python recipe
python-example:
    #!/usr/bin/env python3
    import sys
    print(f"Python version: {sys.version}")

# Node.js recipe
node-example:
    #!/usr/bin/env node
    console.log("Hello from Node!");

# Bash with strict mode
bash-example:
    #!/usr/bin/env bash
    set -euxo pipefail
    echo "Strict bash mode"
```

## Common Use Cases

When the user asks to:
- **Create a justfile** - Reference README.md for syntax and examples
- **Add a recipe** - Check README.md for recipe syntax patterns
- **Use variables/interpolation** - See README.md variable section
- **Set up for different OS** - Check cross-platform and shell settings
- **Write recipes in Python/Node/etc** - See shebang recipes section
- **Understand grammar** - Reference GRAMMAR.md for formal specification
- **Check version changes** - Reference CHANGELOG.md

## Tips

- Start recipe names with `_` to make them private (hidden from `just --list`)
- Use `@` at start of line to suppress command echoing
- Use `-` at start of line to continue on error
- Recipes are run from the justfile's directory by default
- Use `just --fmt` to format your justfile
- Shell completion scripts are available for bash, zsh, fish, powershell, and more

## Resources

- Homepage: https://just.systems/
- GitHub: https://github.com/casey/just
- Book (latest release docs): https://just.systems/man/en/
- Discord: https://discord.gg/ezYScXR
- Crates.io: https://crates.io/crates/just
