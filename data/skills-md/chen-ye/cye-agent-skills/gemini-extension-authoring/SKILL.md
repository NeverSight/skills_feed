---
name: Gemini Extension Authoring
description: This skill should be used when the user asks to "create a gemini extension", "author a gemini extension", "package a gemini hook", "publish a gemini extension", or asks about "extension structure", "gemini-extension.json", or "hooks.json".
version: 1.0.0
---

# Gemini Extension Authoring

Provide expert guidance on creating, packaging, and publishing extensions for the Gemini CLI.

## Extension Structure

Organize Gemini CLI extensions as self-contained directories including commands, hooks, MCP servers, and other resources.

Maintain the following extension directory structure:

```
my-extension/
├── gemini-extension.json  (Required: Manifest)
├── README.md              (Required: Documentation)
├── LICENSE                (Required: License)
├── hooks/
│   ├── hooks.json         (Optional: Hook definitions)
│   └── my_hook.py         (Optional: Hook script)
├── commands/              (Optional: Custom commands)
├── mcp-servers/           (Optional: MCP server code)
├── skills/                (Optional: Agent skills)
└── agents/                (Optional: Sub-agent definitions)
```

## Core Components

### The Manifest (`gemini-extension.json`)

Use the `gemini-extension.json` manifest to define metadata, configuration settings, dependencies, and entry points for hooks or MCP servers.

**Key Fields:**

- `name`: Unique identifier (kebab-case).
- `version`: Semantic version (e.g., "1.0.0").
- `mcpServers`: Definitions for bundled MCP servers.
- `settings`: Configuration options exposed to the user.
- `dependencies`: Required system tools (e.g., `{"python": ">=3.7"}`).

Consult **`references/extension-schema.md`** for the full schema specification.

### Hooks Configuration (`hooks.json`)

Define hooks in a JSON file to intercept and modify CLI behavior. Reference this file in the manifest.

**Structure:**

- Group by event name (e.g., `AfterAgent`, `BeforeTool`).
- Use `matcher` to filter events (e.g., `*` for all, or specific tool names).
- Define the `command` to execute.

**Best Practice:** Use `${extensionPath}` in command strings to reference files within the extension directory reliably.

```json
"command": "${extensionPath}/hooks/my_script.py"
```

Consult **`references/hooks-schema.md`** for detailed event types and configuration options.

### MCP Servers

Bundle MCP servers to expose tools and resources to the model.

**Configuration:**

Define servers in `gemini-extension.json` under the `mcpServers` object.

```json
"mcpServers": {
  "my-server": {
    "command": "node",
    "args": ["${extensionPath}/mcp-server/index.js"],
    "env": {
      "API_KEY": "${env:MY_API_KEY}"
    }
  }
}
```

- **Note**: Ensure all standard MCP configuration options are supported except `trust`.
- **Conflict Resolution**: Ensure servers compliant with `gemini-extension.json` override those in `settings.json` if names collide.

### Agent Skills

Provide specialized workflows by placing skills in a `skills/` directory.

```
skills/
└── security-audit/
    └── SKILL.md
```

The model automatically discovers skills within this directory.

**Recommendation:** To learn how to write effective skills, activate the **Skill Development** skill.
```
activate_skill("Skill Development")
```

### Sub-agents (Experimental)

Bundle sub-agents by placing markdown definitions in an `agents/` directory.

```
agents/
├── security-auditor.md
└── database-expert.md
```

Consult **`references/agents-schema.md`** for configuration details.

### Custom Commands

Add slash commands by placing TOML configuration files in a `commands/` directory.

```
commands/
├── deploy.toml  -> /deploy
└── gcs/
    └── sync.toml -> /gcs:sync
```

Consult **`references/commands-schema.md`** for the TOML specification.

**Conflict Resolution:** Handle name collisions between user commands and extension commands:

- User command: `/deploy`
- Extension command: `/extension-name.deploy`

## Development Workflow
...
## Additional Resources

### Reference Files

- **`references/extension-schema.md`** - Detailed `gemini-extension.json` schema.
- **`references/hooks-schema.md`** - Detailed `hooks.json` schema and event types.
- **`references/agents-schema.md`** - Configuration for sub-agents (`agents/`).
- **`references/commands-schema.md`** - Configuration for custom commands (`commands/`).

### Examples

- **`examples/gemini-extension.json`** - Complete manifest example.
- **`examples/hooks.json`** - Complete hooks configuration example.
