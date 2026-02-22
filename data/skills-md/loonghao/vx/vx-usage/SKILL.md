---
name: vx-usage
description: |
  This skill teaches AI coding agents how to use vx - the universal development tool manager.
  Use this skill whenever the user's project uses vx (has vx.toml or .vx/ directory),
  or when the user mentions vx, tool version management, or cross-platform development setup.
  vx transparently manages Node.js, Python, Go, Rust, and 50+ other tools with zero-config.
---

# VX - Universal Development Tool Manager

vx is a universal development tool manager that automatically installs and manages
development tools (Node.js, Python/uv, Go, Rust, etc.) with zero configuration.

## Core Concept

Instead of requiring users to manually install tools, prefix any command with `vx`:

```bash
vx node --version      # Auto-installs Node.js if needed
vx uv pip install x    # Auto-installs uv if needed
vx go build .          # Auto-installs Go if needed
vx cargo build         # Auto-installs Rust if needed
vx just test           # Auto-installs just if needed
```

vx is fully transparent - same commands, same arguments, just add `vx` prefix.

## Essential Commands

### Tool Execution (most common)
```bash
vx <tool> [args...]           # Run any tool (auto-installs if missing)
vx node app.js                # Run Node.js
vx python script.py           # Run Python (via uv)
vx npm install                # Run npm
vx npx create-react-app app   # Run npx
vx cargo test                 # Run cargo
vx just build                 # Run just (task runner)
vx git status                 # Run git
```

### Tool Management
```bash
vx install node@22            # Install specific version
vx install uv go rust         # Install multiple tools at once
vx list                       # List all available tools
vx list --installed           # List installed tools only
vx versions node              # Show available versions
vx switch node@20             # Switch active version
vx uninstall go@1.21          # Remove a version
```

### Project Management
```bash
vx init                       # Initialize vx.toml for project
vx sync                       # Install all tools from vx.toml
vx setup                      # Full project setup (sync + hooks)
vx dev                        # Enter dev environment with all tools
vx run test                   # Run project scripts from vx.toml
vx check                      # Verify tool constraints
vx lock                       # Generate vx.lock for reproducibility
```

### Environment & Config
```bash
vx env list                   # List environments
vx config show                # Show configuration
vx cache info                 # Show cache usage
vx search <query>             # Search available tools
vx info                       # System info and capabilities
```

## Project Configuration (vx.toml)

Projects use `vx.toml` in the root directory:

```toml
[tools]
node = "22"         # Major version
go = "1.22"         # Minor version
uv = "latest"       # Always latest
rust = "1.80"       # Specific version
just = "*"          # Any version

[scripts]
dev = "npm run dev"
test = "cargo test"
lint = "npm run lint && cargo clippy"
build = "just build"

[hooks]
pre_commit = ["vx run lint"]
post_setup = ["npm install"]
```

## Using `--with` for Multi-Runtime

When a command needs additional runtimes available:

```bash
vx --with bun node app.js     # Node.js + Bun in PATH
vx --with deno npm test        # npm + Deno available
```

## Supported Tools (50+)

| Category | Tools |
|----------|-------|
| JavaScript | node, npm, npx, bun, deno, pnpm, yarn, vite |
| Python | uv, uvx, python, pip |
| Rust | cargo, rustc, rustup |
| Go | go, gofmt |
| System | git, just, jq, cmake, make, ninja, meson |
| Cloud | docker, kubectl, helm, awscli, azcli, gcloud, terraform |
| .NET | dotnet, msbuild, nuget |
| Other | zig, java, protoc, ffmpeg, gh, ollama, dagu, skills |

## Important Rules for AI Agents

1. **Always use `vx` prefix** when running tools in vx-managed projects
2. **Use `vx just`** instead of `just` for task runner commands
3. **Use `vx npm`** instead of `npm` directly
4. **Use `vx cargo`** instead of `cargo` directly
5. **Check `vx.toml`** first to understand project tool requirements
6. **Use `vx run <script>`** for project-defined scripts
7. **Never suggest manual tool installation** - vx handles it automatically
8. Commands like `vx install` are for explicit pre-installation; normal usage auto-installs
