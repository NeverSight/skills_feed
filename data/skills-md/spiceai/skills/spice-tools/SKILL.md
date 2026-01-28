---
name: spice-tools
description: Configure LLM tools (function calling) in Spice including SQL, search, memory, and MCP. Use when asked to "add tools to model", "enable function calling", "configure MCP", or "set up web search".
---

# Spice LLM Tools

Tools extend LLM capabilities with runtime functions like SQL queries, search, and external integrations.

## Enabling Tools on Models

```yaml
models:
  - from: openai:gpt-4o
    name: assistant
    params:
      openai_api_key: ${ secrets:OPENAI_API_KEY }
      tools: auto    # enable all default tools
```

## Built-in Tools

| Tool                   | Description                              | Group    |
|------------------------|------------------------------------------|----------|
| `list_datasets`        | List available datasets                  | `auto`   |
| `sql`                  | Execute SQL queries                      | `auto`   |
| `table_schema`         | Get table schema                         | `auto`   |
| `search`               | Vector similarity search                 | `auto`   |
| `sample_distinct_columns` | Sample distinct column values         | `auto`   |
| `random_sample`        | Random row sampling                      | `auto`   |
| `top_n_sample`         | Top N rows by ordering                   | `auto`   |
| `memory:load`          | Load stored memories                     | `memory` |
| `memory:store`         | Store new memories                       | `memory` |
| `websearch`            | Search the web                           | -        |

## Tool Groups

| Group    | Description                         |
|----------|-------------------------------------|
| `auto`   | All default runtime tools           |
| `memory` | Memory persistence tools            |

## Examples

### SQL and Search Tools
```yaml
models:
  - from: openai:gpt-4o
    name: analyst
    params:
      tools: sql, search, table_schema
```

### With Memory
```yaml
datasets:
  - from: memory:store
    name: llm_memory
    access: read_write

models:
  - from: openai:gpt-4o
    name: assistant
    params:
      tools: auto, memory
```

### Web Search Tool
```yaml
tools:
  - name: web
    from: websearch
    params:
      engine: perplexity
      perplexity_auth_token: ${ secrets:PERPLEXITY_TOKEN }

models:
  - from: openai:gpt-4o
    name: researcher
    params:
      tools: auto, web
```

### MCP Server Integration
```yaml
tools:
  - name: external_tools
    from: mcp
    params:
      mcp_endpoint: http://localhost:3000/mcp
```

## Custom Tool Configuration

Define custom tools in the `tools` section:

```yaml
tools:
  - name: my_search
    from: websearch
    description: 'Search the web for information'
    params:
      engine: perplexity
      perplexity_auth_token: ${ secrets:PERPLEXITY_TOKEN }
```

## Documentation

- [LLM Tools Overview](https://spiceai.org/docs/components/tools)
- [Tools Reference](https://spiceai.org/docs/reference/spicepod/tools)
- [Web Search](https://spiceai.org/docs/components/tools/websearch)
- [MCP Integration](https://spiceai.org/docs/components/tools/mcp)
- [Memory](https://spiceai.org/docs/features/large-language-models/memory)
