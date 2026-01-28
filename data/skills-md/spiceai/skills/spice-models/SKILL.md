---
name: spice-models
description: Configure AI/LLM model providers in Spice (OpenAI, Anthropic, Azure, Bedrock, local models). Use when asked to "add a model", "configure LLM", "set up OpenAI", "add language model", or "enable chat completions".
---

# Spice Model Providers

Model providers enable LLM chat completions and ML inference through a unified OpenAI-compatible API.

## Basic Configuration

```yaml
models:
  - from: <provider>:<model_id>
    name: <model_name>
    params:
      <provider>_api_key: ${ secrets:API_KEY }
      tools: auto                    # optional: enable runtime tools
      system_prompt: 'You are...'    # optional: default system prompt
```

## Provider Prefixes

| Provider     | From Format                    | Example                          |
|--------------|--------------------------------|----------------------------------|
| `openai`     | `openai:<model_id>`            | `openai:gpt-4o`                  |
| `anthropic`  | `anthropic:<model_id>`         | `anthropic:claude-sonnet-4-5`    |
| `azure`      | `azure:<deployment>`           | `azure:my-gpt4-deployment`       |
| `bedrock`    | `bedrock:<model_id>`           | `bedrock:anthropic.claude-3`     |
| `google`     | `google:<model_id>`            | `google:gemini-pro`              |
| `xai`        | `xai:<model_id>`               | `xai:grok-beta`                  |
| `databricks` | `databricks:<endpoint>`        | `databricks:llama-3-70b`         |
| `spiceai`    | `spiceai:<model>`              | `spiceai:llama3`                 |
| `hf`         | `hf:<repo_id>`                 | `hf:meta-llama/Llama-3-8B`       |
| `file`       | `file:<path>`                  | `file:./models/llama.gguf`       |

## Common Parameters

| Parameter       | Description                                      |
|-----------------|--------------------------------------------------|
| `tools`         | Runtime tools: `auto`, `sql`, `search`, `memory` |
| `system_prompt` | Default system prompt for all requests           |
| `endpoint`      | Override API endpoint (for compatible providers) |

## Examples

### OpenAI Model
```yaml
models:
  - from: openai:gpt-4o
    name: gpt4
    params:
      openai_api_key: ${ secrets:OPENAI_API_KEY }
      tools: auto
```

### Model with Memory
```yaml
datasets:
  - from: memory:store
    name: llm_memory
    access: read_write

models:
  - from: openai:gpt-4o
    name: assistant
    params:
      openai_api_key: ${ secrets:OPENAI_API_KEY }
      tools: memory, sql
```

### Local Model (GGUF)
```yaml
models:
  - from: file:./models/llama-3.gguf
    name: local_llama
```

## Using Models

Query via OpenAI-compatible API:
```bash
curl http://localhost:8090/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt4", "messages": [{"role": "user", "content": "Hello"}]}'
```

## Documentation

- [Model Providers Overview](https://spiceai.org/docs/components/models)
- [Models Reference](https://spiceai.org/docs/reference/spicepod/models)
- [LLM Tools](https://spiceai.org/docs/features/large-language-models/tools)
- [Memory](https://spiceai.org/docs/features/large-language-models/memory)
