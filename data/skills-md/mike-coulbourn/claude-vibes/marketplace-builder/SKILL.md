---
name: marketplace-builder
description: "Create and configure Claude Code marketplaces and plugins. Use when the user wants to create a marketplace, publish plugins, set up team plugin distribution, or configure marketplace.json or plugin.json files. Triggers: create marketplace, publish plugin, plugin distribution, marketplace.json, plugin.json, team plugins, share plugins"
---

# Marketplace Builder

A comprehensive guide to creating Claude Code marketplaces and plugins for distributing commands, agents, skills, hooks, and MCP servers.

---

## Quick Reference

### Marketplace vs Plugin Distinction

**Critical concept**: These are NOT the same thing.

| Concept | What It Is | Analogy |
|---------|------------|---------|
| **Marketplace** | JSON catalog listing where plugins live | Library catalog |
| **Plugin** | Packaged collection of components | Book |
| **Components** | Commands, agents, skills, hooks, MCP servers | Chapters |

**Relationship**: One marketplace → many plugins → many components per plugin

**Key insight**: Marketplaces don't HOST plugins. They INDEX them. Plugins can live anywhere (GitHub, GitLab, private git, local paths).

---

### JSON Schema Quick Reference

**Minimal marketplace.json**:
```json
{
  "name": "marketplace-name",
  "owner": {"name": "Owner Name"},
  "plugins": [
    {
      "name": "plugin-name",
      "source": "./path-to-plugin",
      "description": "What this plugin does",
      "version": "1.0.0"
    }
  ]
}
```

**Minimal plugin.json** (inside `.claude-plugin/`):
```json
{
  "name": "plugin-name",
  "description": "What this plugin does",
  "version": "1.0.0"
}
```

**Team settings.json** (inside `.claude/`):
```json
{
  "extraKnownMarketplaces": {
    "marketplace-name": {
      "source": {"source": "github", "repo": "owner/repo"}
    }
  },
  "enabledPlugins": {
    "plugin-name@marketplace-name": true
  }
}
```

---

### Source Types

| Type | Syntax | Best For |
|------|--------|----------|
| **GitHub** | `{"source": "github", "repo": "owner/repo"}` | Public plugins |
| **Git URL** | `{"source": "git", "url": "https://..."}` | Private/GitLab |
| **Directory** | `{"source": "directory", "path": "./path"}` | Monorepo |
| **Relative** | `"./path"` | Shorthand for directory |

---

### Command Reference

```bash
# Add a marketplace
/plugin marketplace add owner/repo
/plugin marketplace add https://gitlab.com/org/repo.git
/plugin marketplace add ./local-marketplace

# List marketplaces
/plugin marketplace list

# Update marketplace catalog
/plugin marketplace update marketplace-name

# Browse and install plugins
/plugin                                    # Interactive browser
/plugin install plugin-name@marketplace    # Direct install

# Manage plugins
/plugin enable plugin@marketplace
/plugin disable plugin@marketplace
/plugin uninstall plugin@marketplace

# Validate structure
claude plugin validate .
```

---

## 6-Phase Workflow

### Phase 1: Requirements Gathering

**Use AskUserQuestion to understand the user's needs:**

1. **What are you distributing?**
   - Commands (slash commands)
   - Agents (subagents)
   - Skills (model-invoked capabilities)
   - Hooks (event handlers)
   - MCP servers (external tools)
   - Mix of the above

2. **How many plugins?**
   - Single plugin
   - Multiple related plugins
   - Large plugin collection

3. **Who is the audience?**
   - Personal use (just me)
   - Team (colleagues via git)
   - Organization (company-wide)
   - Public community

4. **What hosting?**
   - GitHub (public or private)
   - GitLab or other git service
   - Self-hosted git
   - Local development only

**Document the answers before proceeding.**

---

### Phase 2: Architecture Decision

Based on requirements, recommend one of these patterns:

#### Pattern A: Basic Marketplace (Single Plugin)
**Use when**: One plugin, simple distribution
```
my-marketplace/
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── commands/
└── agents/
```

#### Pattern B: Monorepo (Multiple Plugins, One Repo)
**Use when**: Related plugins, unified versioning, team ownership
```
company-plugins/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   ├── formatter/
│   │   ├── .claude-plugin/plugin.json
│   │   └── commands/
│   ├── linter/
│   │   ├── .claude-plugin/plugin.json
│   │   └── commands/
│   └── tester/
│       ├── .claude-plugin/plugin.json
│       └── agents/
```

#### Pattern C: Multi-Repo (Plugins in Separate Repos)
**Use when**: Independent plugins, different owners, community collection
```
# Marketplace repo
my-marketplace/
└── .claude-plugin/
    └── marketplace.json  # Points to other repos

# Plugin repos (separate)
tool-a/
├── .claude-plugin/plugin.json
└── commands/

tool-b/
├── .claude-plugin/plugin.json
└── agents/
```

#### Pattern D: Enterprise (Hybrid Private + Public)
**Use when**: Mix of internal and external tools, strict access control
```json
{
  "plugins": [
    {"name": "internal-tool", "source": {"source": "git", "url": "https://git.corp/..."}},
    {"name": "community-tool", "source": {"source": "github", "repo": "public/tool"}}
  ]
}
```

**Decision tree**:
- Single plugin? → Pattern A
- Multiple plugins, same team? → Pattern B
- Plugins from different sources? → Pattern C
- Enterprise with private + public? → Pattern D

---

### Phase 3: Plugin Creation

For each plugin, create this structure:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json         # Required: plugin manifest
├── commands/               # Optional: slash commands
│   └── my-command.md
├── agents/                 # Optional: subagents
│   └── my-agent.md
├── skills/                 # Optional: skills
│   └── my-skill/
│       └── SKILL.md
├── hooks/                  # Optional: event handlers
│   └── hooks.json
└── .mcp.json              # Optional: MCP servers
```

**Write plugin.json**:
```json
{
  "name": "plugin-name",
  "description": "Clear description of what this plugin provides",
  "version": "1.0.0",
  "author": {
    "name": "Author Name",
    "email": "author@example.com"
  },
  "homepage": "https://docs.example.com",
  "repository": "https://github.com/owner/repo",
  "license": "MIT"
}
```

**Naming conventions**:
- Plugin name: `kebab-case` (e.g., `code-formatter`)
- Version: Semantic versioning `MAJOR.MINOR.PATCH`
- Commands: `verb-noun.md` (e.g., `format-code.md`)
- Agents: `role-name.md` (e.g., `code-reviewer.md`)

---

### Phase 4: Marketplace Creation

Create `.claude-plugin/marketplace.json`:

**For monorepo (plugins in same repo)**:
```json
{
  "name": "company-tools",
  "owner": {
    "name": "Company Name",
    "email": "team@company.com"
  },
  "metadata": {
    "description": "Company development tools",
    "version": "1.0.0",
    "pluginRoot": "./plugins"
  },
  "plugins": [
    {
      "name": "formatter",
      "source": "./plugins/formatter",
      "description": "Code formatting tools",
      "version": "1.0.0"
    },
    {
      "name": "linter",
      "source": "./plugins/linter",
      "description": "Code linting tools",
      "version": "1.0.0"
    }
  ]
}
```

**For multi-repo (plugins in separate repos)**:
```json
{
  "name": "community-collection",
  "owner": {
    "name": "Community",
    "email": "maintainers@example.com"
  },
  "plugins": [
    {
      "name": "tool-a",
      "source": {
        "source": "github",
        "repo": "community/tool-a"
      },
      "description": "Tool A description",
      "version": "2.1.0"
    },
    {
      "name": "tool-b",
      "source": {
        "source": "github",
        "repo": "community/tool-b"
      },
      "description": "Tool B description",
      "version": "1.3.0"
    }
  ]
}
```

---

### Phase 5: Distribution Setup

#### For Personal Use
No additional setup. Add marketplace locally:
```bash
/plugin marketplace add ./path-to-marketplace
```

#### For Team Distribution
Add to project's `.claude/settings.json`:
```json
{
  "extraKnownMarketplaces": {
    "team-tools": {
      "source": {
        "source": "github",
        "repo": "company/claude-plugins"
      }
    }
  },
  "enabledPlugins": {
    "formatter@team-tools": true,
    "linter@team-tools": true
  }
}
```

**How it works**:
1. Team member clones project
2. Claude Code reads `.claude/settings.json`
3. Prompts to trust configured marketplaces
4. Prompts to install enabled plugins
5. New team members get correct setup automatically

#### For Public Distribution
1. Push marketplace repo to GitHub
2. Document installation in README:
   ```markdown
   ## Installation

   Add the marketplace:
   ```bash
   /plugin marketplace add owner/repo
   ```

   Install plugins:
   ```bash
   /plugin install formatter@owner-tools
   ```
   ```

#### For Enterprise
1. Set up private git access (SSH keys or tokens)
2. Create internal marketplace with git URL sources
3. Configure `.claude/settings.json` in project templates
4. Document for IT/security review

---

### Phase 6: Validation and Testing

#### Step 1: Validate JSON Syntax
```bash
# Validate marketplace structure
claude plugin validate .

# Manual JSON validation
python3 -c "import json; json.load(open('.claude-plugin/marketplace.json'))"
python3 -c "import json; json.load(open('.claude-plugin/plugin.json'))"
```

#### Step 2: Test Marketplace Addition
```bash
# Add marketplace locally
/plugin marketplace add ./path-to-marketplace

# Verify it appears
/plugin marketplace list
```

#### Step 3: Test Plugin Installation
```bash
# Browse available plugins
/plugin

# Install a plugin
/plugin install plugin-name@marketplace-name

# Verify components work
/help  # Check commands appear
```

#### Step 4: Test Team Flow (if applicable)
1. Clone project with settings.json to new location
2. Trust folder when prompted
3. Verify marketplaces and plugins install correctly

#### Step 5: Verify All Components
- Commands: Run `/command-name` to test
- Agents: Check `/agents` or try invoking via Task
- Skills: Use trigger terms to activate
- Hooks: Trigger events to test
- MCP servers: Check MCP tool availability

---

## Architecture Patterns

### Monorepo Pattern

**Structure**:
```
company-plugins/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   ├── plugin-a/
│   ├── plugin-b/
│   └── plugin-c/
└── README.md
```

**Pros**:
- Single repo to manage
- Unified versioning
- Easy cross-plugin changes
- Simpler CI/CD

**Cons**:
- All plugins share access control
- Larger repo size
- All-or-nothing updates

**Best for**: Team tools, related plugins, unified ownership

---

### Multi-Repo Pattern

**Structure**:
```
# Marketplace repo
tools-marketplace/
└── .claude-plugin/marketplace.json

# Separate plugin repos
plugin-a/   # github.com/org/plugin-a
plugin-b/   # github.com/org/plugin-b
plugin-c/   # github.com/org/plugin-c
```

**Pros**:
- Independent versioning
- Separate access control
- Distributed ownership
- Smaller repos

**Cons**:
- More repos to manage
- Version coordination needed
- More complex CI/CD

**Best for**: Community collections, mixed ownership, independent plugins

---

### Hybrid Pattern

**Structure**:
```json
{
  "plugins": [
    {"name": "core", "source": "./plugins/core"},
    {"name": "community", "source": {"source": "github", "repo": "community/tool"}},
    {"name": "internal", "source": {"source": "git", "url": "https://git.corp/..."}}
  ]
}
```

**Pros**:
- Flexibility to mix sources
- Can include community plugins
- Supports private + public

**Cons**:
- More complex to maintain
- Mixed trust levels
- Varied update cycles

**Best for**: Enterprise, mature ecosystems, gradual migration

---

## Common Pitfalls

### 1. Confusing Marketplace with Plugin

**Wrong**: Thinking marketplace.json IS the plugin
**Right**: marketplace.json POINTS TO plugins

marketplace.json is a catalog. The actual plugin code lives in separate directories or repos.

### 2. Wrong Source Type

**Wrong**: Using GitHub shorthand for private repos
```json
{"source": "github", "repo": "private-org/private-repo"}  // May fail
```

**Right**: Use git URL for private repos
```json
{"source": "git", "url": "git@github.com:private-org/private-repo.git"}
```

### 3. Missing Required Fields

**marketplace.json required**:
- `name`
- `owner.name`
- `plugins` array

**plugin.json required**:
- `name`
- `description`
- `version`

### 4. Path Errors

**Wrong**: Relative paths from wrong directory
```json
{"source": "../plugins/tool"}  // Relative to what?
```

**Right**: Paths relative to marketplace.json location
```json
{"source": "./plugins/tool"}  // Relative to .claude-plugin/
```

### 5. Version Mismatch

Keep versions in sync:
- `plugin.json` version
- `marketplace.json` plugin entry version

When you update a plugin, update both files.

### 6. Forgetting Validation

Always run before publishing:
```bash
claude plugin validate .
```

### 7. Trust Model Misunderstanding

Users MUST explicitly trust marketplaces. You cannot force-install plugins on team members. The settings.json only PRE-CONFIGURES - users still approve.

---

## When to Use This Skill

**Use marketplace-builder when**:
- Creating a new marketplace
- Publishing plugins for distribution
- Setting up team-wide plugin configuration
- Converting local plugins to distributable packages
- Troubleshooting marketplace or plugin issues

**Don't use when**:
- Creating individual commands (use slash-command-builder)
- Creating individual agents (use agent-builder)
- Creating individual skills (use skill-builder)
- Just using existing plugins (use /plugin commands directly)

---

## File Reference

### Templates
- `templates/basic-marketplace.md` - Single plugin, simple setup
- `templates/plugin-structure.md` - Complete plugin creation guide
- `templates/multi-plugin.md` - Monorepo pattern
- `templates/multi-repo.md` - Distributed plugins pattern
- `templates/enterprise-marketplace.md` - Enterprise with team config

### Examples
- `examples/development-tools.md` - 6 dev tool plugins
- `examples/team-workflows.md` - 6 team workflow plugins
- `examples/specialized-domains.md` - 6 domain-specific plugins

### Reference
- `reference/syntax-guide.md` - Complete JSON schemas
- `reference/best-practices.md` - Design principles
- `reference/troubleshooting.md` - Common issues and debugging
