---
name: developing-opencode-meta
description: "Build OpenCode plugins, agents, hooks, and tools. Use when creating, reviewing, or debugging OpenCode extensions. Covers plugin architecture, agent configuration, lifecycle hooks, custom tools, and distribution. Invoke PROACTIVELY when user mentions OpenCode plugins, agents, hooks, or wants to extend OpenCode functionality."
---

<essential_principles>
This skill covers building extensions for **OpenCode**, an open-source AI coding assistant. OpenCode's plugin system allows customizing agents, tools, hooks, and more.

**1. Plugins are the extension mechanism**
Everything in OpenCode is extended through plugins. A plugin is a TypeScript function that returns configuration for agents, tools, hooks, and other features. Plugins can be distributed via npm.

**2. Agents define AI behaviour**
Agents are configured AI assistants with specific prompts, models, and tool access. OpenCode has two modes: `primary` (main agent) and `subagent` (delegated tasks). Agent prompts are full TypeScript strings, giving complete control.

**3. Hooks intercept lifecycle events**
Hooks let plugins react to events like tool execution, session creation, context limits, and more. They enable features like auto-compaction, TDD enforcement, and context monitoring.

**4. Tools extend agent capabilities**
Custom tools give agents new abilities. Tools are defined with Zod schemas for parameters and can access the plugin context for session management, file operations, etc.

**5. Skills work differently in OpenCode**
OpenCode can load Claude Code skills, but also has its own skill system. Skills in OpenCode are simpler — markdown files that agents can invoke for domain knowledge.
</essential_principles>

<never_do>
- NEVER export non-plugin functions from main index.ts (OpenCode calls ALL exports as plugins)
- NEVER use blocking `task()` calls for explore/librarian agents (always use `background_task`)
- NEVER allow subagents to spawn subagents without explicit design (can cause runaway delegation)
- NEVER skip the `tool.execute.before` hook when modifying tool arguments
- NEVER hardcode models — always accept model as parameter with sensible defaults
</never_do>

<escalation>
Stop and ask the user when:
- Unclear whether feature needs plugin vs fork of OpenCode
- Hook interaction could cause infinite loops
- Agent delegation depth exceeds 2 levels
- Custom tool needs access to APIs not exposed by plugin context
- Distribution approach unclear (npm vs local)
</escalation>

<intake>
What would you like to build for OpenCode?

1. **Plugin** — Create a new plugin with agents, tools, or hooks
2. **Agent** — Define a custom agent with specific behaviour
3. **Hook** — Intercept lifecycle events for custom behaviour
4. **Tool** — Add a new capability for agents to use
5. **Review** — Audit an existing OpenCode plugin

**Wait for response before proceeding.**
</intake>

<routing>
| Response | Next Action | Reference |
|----------|-------------|-----------|
| 1, "plugin", "extension", "create plugin" | Scaffold plugin structure | references/plugin-architecture.md |
| 2, "agent", "custom agent", "subagent" | Define agent config | references/agent-configuration.md |
| 3, "hook", "lifecycle", "intercept" | Implement hook | references/lifecycle-hooks.md |
| 4, "tool", "custom tool", "capability" | Create tool definition | references/custom-tools.md |
| 5, "review", "audit", "check" | Analyze plugin structure | Use all references |

**After identifying the intent, read the relevant reference file and follow its guidance.**
</routing>

<quick_reference>
**Plugin Entry Point:**
```typescript
import type { Plugin } from "@opencode-ai/plugin"

const MyPlugin: Plugin = async (ctx) => {
  return {
    tool: { /* custom tools */ },
    config: { agents: { /* agent definitions */ } },
    event: async (input) => { /* lifecycle events */ },
    "tool.execute.before": async (input, output) => { /* pre-tool hook */ },
    "tool.execute.after": async (input, output) => { /* post-tool hook */ },
  }
}

export default MyPlugin
```

**Agent Definition:**
```typescript
import type { AgentConfig } from "@opencode-ai/sdk"

const myAgent: AgentConfig = {
  description: "What this agent does (shown in delegation UI)",
  mode: "subagent",  // or "primary"
  model: "anthropic/claude-sonnet-4",
  temperature: 0.1,
  tools: { write: true, edit: true, bash: true },
  prompt: `Full agent prompt here...`,
}
```

**Custom Tool:**
```typescript
import { z } from "zod"

const myTool = {
  description: "What this tool does",
  parameters: z.object({
    input: z.string().describe("Parameter description"),
  }),
  async execute(params, ctx) {
    // Tool logic
    return { result: "output" }
  },
}
```

**Key Hooks:**
- `event` — Session lifecycle (created, deleted, error)
- `tool.execute.before` — Modify tool args before execution
- `tool.execute.after` — Process tool results
- `experimental.session.compacting` — Inject context into summaries
- `chat.message` — Intercept user messages
</quick_reference>

<key_concepts>
## Plugin Context (`ctx`)

The plugin receives a context object with:
- `ctx.client` — OpenCode client for session operations
- `ctx.directory` — Current working directory
- `ctx.client.session.summarize()` — Trigger context compaction

## Agent Modes

| Mode | Purpose | Use Case |
|------|---------|----------|
| `primary` | Main conversation agent | Custom main agent replacing default |
| `subagent` | Delegated task executor | Specialized agents for specific work |

## Tool Access Control

Agents can restrict tool access:
```typescript
tools: {
  write: true,      // File writing
  edit: true,       // File editing
  bash: true,       // Shell commands
  background_task: false,  // Prevent sub-subagent spawning
}
```

## Hook Execution Order

1. `chat.message` — User input received
2. `tool.execute.before` — Before each tool call
3. Tool executes
4. `tool.execute.after` — After each tool call
5. `event` — Session events (async, not blocking)

## Distribution

Plugins are distributed via npm:
```bash
# Install
bunx my-opencode-plugin install

# This registers in ~/.config/opencode/opencode.json
```
</key_concepts>

<reference_index>
- `references/plugin-architecture.md` — Plugin structure, entry points, exports
- `references/agent-configuration.md` — Agent config, modes, prompt design
- `references/lifecycle-hooks.md` — All available hooks and patterns
- `references/custom-tools.md` — Tool definition, Zod schemas, execution
</reference_index>

<success_criteria>
A well-built OpenCode plugin:

- Single default export (plugin function)
- No non-plugin exports from main index.ts
- Agents use appropriate mode (primary vs subagent)
- Hooks don't cause infinite loops
- Tools have clear Zod schemas with descriptions
- Distribution via npm with CLI installer
</success_criteria>
