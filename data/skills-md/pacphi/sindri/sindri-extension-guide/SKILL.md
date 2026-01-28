---
name: sindri-extension-guide
description: Guide users through creating Sindri extensions. Use when creating new extensions, understanding extension.yaml structure, validating extensions against schemas, or learning about extension installation methods (mise, apt, binary, npm, script, hybrid). Includes NEW capabilities system for project-init, authentication (multi-method API key + CLI auth), lifecycle hooks, and MCP integration. Helps with extension development, registry updates, and category assignment.
allowed-tools: Read, Glob, Grep, Bash, Write, Edit
---

# Sindri Extension Development Guide

## What's New: Extension Capabilities System

**Recent Addition (Jan 2026):** Sindri now supports an optional **capabilities system** for advanced extensions:

- **Project Initialization** - Commands to set up new projects (`project-init`)
- **Multi-Method Authentication** - Support both API key and CLI auth (`auth`)
- **Lifecycle Hooks** - Pre/post install and project-init hooks (`hooks`)
- **MCP Integration** - Register as Model Context Protocol servers (`mcp`)

**Most extensions don't need capabilities** - they're only for extensions that extend project management functionality (like Claude Flow, Agentic QE, Spec-Kit). Regular extensions (nodejs, python, docker) work exactly as before.

## Slash Commands (Recommended)

For reliable extension creation with all documentation updates, use these commands:

| Command                          | Purpose                                                   |
| -------------------------------- | --------------------------------------------------------- |
| `/extension/new <name> [source]` | Create new extension with complete documentation workflow |
| `/extension/update-docs <name>`  | Update documentation for existing extension               |

**Example:**

```
/extension/new mdflow https://github.com/johnlindquist/mdflow
/extension/update-docs nodejs
```

These commands enforce the complete workflow including all required documentation updates.

---

## Overview

This skill guides you through creating declarative YAML extensions for Sindri. Extensions are **YAML files, not bash scripts** - all configuration is driven by declarative YAML definitions.

## Documentation Locations

**IMPORTANT:** After creating any extension, you must update the relevant documentation.

### Key Documentation Files

| Type                | Path                                          | Purpose                            |
| ------------------- | --------------------------------------------- | ---------------------------------- |
| **Schema**          | `v2/docker/lib/schemas/extension.schema.json` | Extension validation schema        |
| **Registry**        | `v2/docker/lib/registry.yaml`                 | Master extension registry          |
| **Profiles**        | `v2/docker/lib/profiles.yaml`                 | Extension profile definitions      |
| **Categories**      | `v2/docker/lib/categories.yaml`               | Category definitions               |
| **Extension Docs**  | `docs/extensions/{NAME}.md`                   | Individual extension documentation |
| **Catalog**         | `docs/EXTENSIONS.md`                          | Overview of all extensions         |
| **Authoring Guide** | `docs/EXTENSION_AUTHORING.md`                 | Detailed authoring reference       |
| **Slides**          | `docs/slides/extensions.html`                 | Visual presentation                |

## Quick Start Checklist

1. [ ] Create directory: `v2/docker/lib/extensions/{name}/`
2. [ ] Create `extension.yaml` with required sections
3. [ ] Add to `v2/docker/lib/registry.yaml`
4. [ ] Validate: `./v2/cli/extension-manager validate {name}`
5. [ ] Test: `./v2/cli/extension-manager install {name}`
6. [ ] **Update documentation** (see Post-Extension Checklist below)

## Extension Directory Structure

```text
v2/docker/lib/extensions/{extension-name}/
├── extension.yaml       # Required: Main definition
├── scripts/             # Optional: Custom scripts
│   ├── install.sh       # Custom installation
│   ├── uninstall.sh     # Custom removal
│   └── validate.sh      # Custom validation
├── templates/           # Optional: Config templates
│   └── config.template
└── mise.toml            # Optional: mise configuration
```

## Minimal Extension Template

```yaml
metadata:
  name: my-extension
  version: 1.0.0
  description: Brief description (10-200 chars)
  category: dev-tools
  dependencies: []

install:
  method: mise
  mise:
    configFile: mise.toml

validate:
  commands:
    - name: mytool
      versionFlag: --version
      expectedPattern: "v\\d+\\.\\d+\\.\\d+"
```

## Extension YAML Sections

Extensions consist of required sections (metadata, install, validate) and optional sections (requirements, configure, remove, upgrade, bom, **capabilities**).

**IMPORTANT: Capabilities are OPTIONAL** - Most extensions (nodejs, python, docker, etc.) don't need capabilities. Only extensions requiring project initialization, authentication, lifecycle hooks, or MCP integration need the capabilities section.

### 1. Metadata (Required)

```yaml
metadata:
  name: extension-name # lowercase with hyphens
  version: 1.0.0 # semantic versioning
  description: What it does # 10-200 characters
  category: dev-tools # see categories below
  author: Your Name # optional
  homepage: https://... # optional
  dependencies: # other extensions needed
    - nodejs
    - python
```

**Valid Categories:**

- `base` - Core system components
- `language` - Programming runtimes (Node.js, Python, etc.)
- `dev-tools` - Development tools (linters, formatters)
- `infrastructure` - Cloud/container tools (Docker, K8s, Terraform)
- `ai` - AI/ML tools and frameworks
- `agile` - Project management tools (Jira, Linear)
- `database` - Database servers
- `monitoring` - Observability tools
- `mobile` - Mobile SDKs
- `desktop` - GUI environments
- `utilities` - General tools

### 2. Requirements (Optional)

```yaml
requirements:
  domains: # Network access needed
    - api.github.com
    - registry.npmjs.org
  diskSpace: 500 # MB required
  secrets: # Credentials needed
    - GITHUB_TOKEN
```

### 3. Install (Required)

Choose ONE installation method:

**mise** (recommended for language tools):

```yaml
install:
  method: mise
  mise:
    configFile: mise.toml # Reference to mise config
    reshim: true # Rebuild shims after install
```

**apt** (system packages):

```yaml
install:
  method: apt
  apt:
    repositories:
      - name: docker
        key: https://download.docker.com/linux/ubuntu/gpg
        url: https://download.docker.com/linux/ubuntu
        suite: jammy
        component: stable
    packages:
      - docker-ce
      - docker-ce-cli
```

**binary** (direct download):

```yaml
install:
  method: binary
  binary:
    url: https://github.com/org/repo/releases/download/v1.0.0/tool-linux-amd64.tar.gz
    extract: tar.gz # tar.gz, zip, or none
    destination: ~/.local/bin/tool
```

**npm** (Node.js packages):

```yaml
install:
  method: npm
  npm:
    packages:
      - typescript
      - eslint
    global: true
```

**script** (custom installation):

```yaml
install:
  method: script
  script:
    path: scripts/install.sh
    timeout: 300 # seconds (default: 300)
```

**hybrid** (multiple methods):

```yaml
install:
  method: hybrid
  hybrid:
    steps:
      - method: apt
        apt:
          packages: [build-essential]
      - method: script
        script:
          path: scripts/install.sh
```

### 4. Configure (Optional)

```yaml
configure:
  templates:
    - source: templates/config.template
      destination: ~/.config/tool/config.yaml
      mode: overwrite # overwrite|append|merge|skip-if-exists
  environment:
    - key: TOOL_HOME
      value: $HOME/.tool
      scope: bashrc # bashrc|profile|session
```

### 5. Validate (Required)

```yaml
validate:
  commands:
    - name: tool-name
      versionFlag: --version
      expectedPattern: "\\d+\\.\\d+\\.\\d+"
  mise:
    tools:
      - node
      - python
    minToolCount: 2
  script:
    path: scripts/validate.sh
    timeout: 60
```

### 6. Remove (Optional)

```yaml
remove:
  confirmation: true
  mise:
    removeConfig: true
    tools: [node, python]
  apt:
    packages: [package-name]
    purge: false
  script:
    path: scripts/uninstall.sh
  paths:
    - ~/.config/tool
    - ~/.local/share/tool
```

### 7. Upgrade (Optional)

```yaml
upgrade:
  strategy: automatic # automatic|manual|none
  mise:
    upgradeAll: true
  apt:
    packages: [package-name]
    updateFirst: true
  script:
    path: scripts/upgrade.sh
```

### 8. Bill of Materials (Optional but Recommended)

```yaml
bom:
  tools:
    - name: node
      version: dynamic # or specific version
      source: mise
      type: runtime
      license: MIT
      homepage: https://nodejs.org
```

### 9. Capabilities (Optional - Advanced Extensions Only)

**Use capabilities when your extension needs:**

- **Project initialization** - Commands to set up a new project (e.g., `claude-flow init`, `spec-kit init`)
- **Authentication** - Validate API keys or CLI authentication before running
- **Lifecycle hooks** - Pre/post install or project-init commands
- **MCP integration** - Register as a Model Context Protocol server for Claude Code

**Most extensions don't need capabilities.** Only use this for extensions that extend project management functionality.

```yaml
capabilities:
  # Project initialization (optional)
  project-init:
    enabled: true
    commands:
      - command: "mytool init --force"
        description: "Initialize mytool project"
        requiresAuth: anthropic # or: openai, github, none
        conditional: false # true = only run if condition met

    state-markers:
      - path: ".mytool"
        type: directory
        description: "Mytool configuration directory"
      - path: ".mytool/config.json"
        type: file
        description: "Mytool config file"

    validation:
      command: "mytool --version"
      expectedPattern: "^\\d+\\.\\d+\\.\\d+"
      expectedExitCode: 0

  # Authentication (optional)
  auth:
    provider: anthropic # or: openai, github, custom
    required: false # true = block installation without auth
    methods:
      - api-key # API key in environment variable
      - cli-auth # CLI authentication (e.g., Max/Pro plan)
    envVars:
      - ANTHROPIC_API_KEY
    validator:
      command: "claude --version"
      expectedExitCode: 0
    features:
      - name: agent-spawn
        requiresApiKey: false
        description: "CLI-based features"
      - name: api-integration
        requiresApiKey: true
        description: "Direct API features"

  # Lifecycle hooks (optional)
  hooks:
    pre-install:
      command: "echo 'Preparing installation...'"
      description: "Pre-installation checks"
    post-install:
      command: "mytool --version"
      description: "Verify installation"
    pre-project-init:
      command: "mytool doctor --check"
      description: "Pre-init health check"
    post-project-init:
      command: "echo 'Project initialized'"
      description: "Post-init notification"

  # MCP server registration (optional)
  mcp:
    enabled: true
    server:
      command: "npx"
      args:
        - "-y"
        - "@mytool/mcp-server"
        - "start"
      env:
        MYTOOL_MCP_MODE: "1"
    tools:
      - name: "mytool-action"
        description: "Perform mytool action"
      - name: "mytool-query"
        description: "Query mytool data"

  # Feature configuration (optional, V3+ extensions)
  features:
    core:
      daemon_autostart: true
      unified_config: true
    advanced:
      plugin_system: true
      security_scanning: false
```

**Capability Guidelines:**

1. **Keep it simple** - Only add capabilities you actually need
2. **State markers** - Define files/directories created by project-init for idempotency
3. **Conditional commands** - Use `conditional: true` for optional setup steps
4. **Multi-method auth** - Support both API key and CLI auth when possible
5. **Feature-level auth** - Some features may work without API key (use `features` array)

## Adding to Registry

After creating your extension, add it to `v2/docker/lib/registry.yaml`:

```yaml
extensions:
  my-extension:
    category: dev-tools
    description: Short description
    dependencies: [nodejs]
    protected: false
```

## Validation Commands

```bash
# Validate single extension
./v2/cli/extension-manager validate my-extension

# Validate all extensions
./v2/cli/extension-manager validate-all

# Check extension info
./v2/cli/extension-manager info my-extension

# Test installation
./v2/cli/extension-manager install my-extension

# Check status
./v2/cli/extension-manager status my-extension
```

## Common Patterns

### Language Runtime (mise-based)

Best for: Node.js, Python, Go, Rust, Ruby

- Use `method: mise` with a `mise.toml` config file
- Set appropriate environment variables in configure section
- Validate with version command
- **No capabilities needed** - just install tools

### Development Tool (npm-based)

Best for: TypeScript, ESLint, Prettier

- Depend on `nodejs` extension
- Use `method: npm` with global packages
- Add configuration templates

### CLI Tool (binary download)

Best for: GitHub releases, standalone binaries

- Use `method: binary` with GitHub release URL
- Handle extraction (tar.gz, zip)
- Validate binary exists and runs

### Complex Setup (hybrid)

Best for: Desktop environments, multi-step installs

- Use `method: hybrid` with ordered steps
- Combine apt + script for flexibility
- Include cleanup in remove section
- **No capabilities needed** unless it requires project initialization

### AI/Project Management Tool (with capabilities)

Best for: Claude Flow, Agentic QE, Spec-Kit

- Use appropriate install method (mise, script, npm)
- **Add capabilities section** for project initialization
- Define state markers for idempotency (`.claude/`, `.agentic-qe/`, `.github/spec.json`)
- Include authentication configuration (anthropic, openai, github, or none)
- Add lifecycle hooks for post-install/post-init actions
- Register MCP server if extension provides Claude Code tools
- Example extensions: `claude-flow-v3`, `spec-kit`, `agentic-qe`

**Current Extensions Using Capabilities:**

| Extension      | project-init | auth      | hooks | mcp | Notes                            |
| -------------- | ------------ | --------- | ----- | --- | -------------------------------- |
| claude-flow-v2 | ✓            | anthropic | ✓     | ✓   | Stable, 158+ aliases             |
| claude-flow-v3 | ✓            | anthropic | ✓     | ✓   | Alpha, 10x performance, 15 tools |
| agentic-qe     | ✓            | anthropic | ✓     | ✓   | AI-powered testing               |
| spec-kit       | ✓            | none      | ✓     | -   | GitHub spec documentation        |
| agentic-flow   | ✓            | anthropic | ✓     | ✓   | Multi-agent workflows            |

## Script Guidelines

All scripts must:

1. Start with `#!/usr/bin/env bash`
2. Include `set -euo pipefail`
3. Exit 0 on success, non-zero on failure
4. Use `$HOME`, `$WORKSPACE` environment variables
5. Log progress with echo statements

Example:

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "Installing my-tool..."
# Installation commands here
echo "my-tool installed successfully"
```

## Troubleshooting

| Issue                   | Solution                                  |
| ----------------------- | ----------------------------------------- |
| Schema validation fails | Check YAML syntax, verify required fields |
| Dependencies not found  | Add missing extensions to registry.yaml   |
| Install times out       | Increase timeout in script section        |
| Validation fails        | Check expectedPattern regex escaping      |
| Permission denied       | Scripts must be executable                |

---

## Post-Extension Documentation Checklist

**CRITICAL:** After creating or modifying an extension, you MUST complete these documentation updates:

### Required Updates (Always Do These)

- [ ] **Registry Entry** - Add to `v2/docker/lib/registry.yaml`

  ```yaml
  extensions:
    my-extension:
      category: dev-tools
      description: Short description
      dependencies: []
  ```

- [ ] **Extension Documentation** - Create `docs/extensions/{NAME}.md`
  - Use UPPERCASE for filename (e.g., `NODEJS.md`, `AI-TOOLKIT.md`)
  - Include: overview, installation, configuration, usage examples
  - For VisionFlow: `docs/extensions/vision-flow/VF-{NAME}.md`

- [ ] **Extension Catalog** - Update `docs/EXTENSIONS.md`
  - Add to appropriate category table
  - Include link to extension doc

### Conditional Updates (When Applicable)

- [ ] **Profiles** - If adding extension to profiles:
  - Update `v2/docker/lib/profiles.yaml`
  - Update relevant profile descriptions in `docs/EXTENSIONS.md`

- [ ] **Categories** - If adding new category:
  - Update `v2/docker/lib/categories.yaml`
  - Update `v2/docker/lib/schemas/extension.schema.json` (category enum)
  - Update category docs in `docs/EXTENSIONS.md`

- [ ] **Schema** - If adding new extension fields:
  - Update `v2/docker/lib/schemas/extension.schema.json`
  - Update `docs/SCHEMA.md`
  - Update `REFERENCE.md` in this skill

- [ ] **Slides** - If extension is notable/featured:
  - Update `docs/slides/extensions.html`

### VisionFlow-Specific Updates

- [ ] Update `docs/extensions/vision-flow/README.md`
- [ ] Update `docs/extensions/vision-flow/CAPABILITY-CATALOG.md`
- [ ] Update VisionFlow profile if applicable

### Validation After Updates

```bash
# Validate YAML files
pnpm validate:yaml

# Lint markdown
pnpm lint:md

# Validate extension
./v2/cli/extension-manager validate {name}
```

---

## Extension Documentation Template

When creating `docs/extensions/{NAME}.md`, use this template:

```markdown
# {Extension Name}

{Brief description of what the extension provides.}

## Overview

{More detailed explanation of the extension's purpose and capabilities.}

## Installation

\`\`\`bash
extension-manager install {name}
\`\`\`

## What Gets Installed

- {Tool 1} - {purpose}
- {Tool 2} - {purpose}

## Configuration

{Any configuration options or environment variables.}

## Usage

{Usage examples.}

## Dependencies

{List any extension dependencies.}

## Requirements

- **Disk Space:** {X} MB
- **Network:** {domains accessed}
- **Secrets:** {optional secrets}

## Related Extensions

- {Related extension 1}
- {Related extension 2}
```

---

## Reference Files

- **Schema**: `v2/docker/lib/schemas/extension.schema.json`
- **Registry**: `v2/docker/lib/registry.yaml`
- **Categories**: `v2/docker/lib/categories.yaml`
- **Profiles**: `v2/docker/lib/profiles.yaml`
- **Examples**: `v2/docker/lib/extensions/*/extension.yaml`

For detailed field reference, see REFERENCE.md.
For complete examples, see EXAMPLES.md.

**Tip:** Use `Glob` and `Grep` tools to discover current documentation files dynamically:

```bash
# Find all extension docs
ls docs/extensions/*.md

# Find VisionFlow docs
ls docs/extensions/vision-flow/*.md
```
