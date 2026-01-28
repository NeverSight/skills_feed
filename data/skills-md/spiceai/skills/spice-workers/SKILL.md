---
name: spice-workers
description: Configure workers for model load balancing and fallback in Spice. Use when asked to "add load balancing", "configure model fallback", "set up worker", or "route between models".
---

# Spice Workers

Workers coordinate model interactions, enabling load balancing and fallback strategies across multiple models.

## Basic Configuration

```yaml
workers:
  - name: <worker_name>
    type: load_balance
    description: |
      Worker description
    load_balance:
      routing:
        - from: <model_name>
```

## Load Balancing Strategies

### Round Robin
Distribute requests evenly across models:

```yaml
workers:
  - name: round_robin
    type: load_balance
    load_balance:
      routing:
        - from: model_a
        - from: model_b
        - from: model_c
```

### Fallback (Priority Order)
Try models in order, falling back on failure:

```yaml
workers:
  - name: fallback
    type: load_balance
    load_balance:
      routing:
        - from: primary_model
          order: 1
        - from: backup_model
          order: 2
        - from: emergency_model
          order: 3
```

### Weighted Distribution
Route by percentage weight:

```yaml
workers:
  - name: weighted
    type: load_balance
    load_balance:
      routing:
        - from: fast_model
          weight: 8     # 80% of traffic
        - from: slow_model
          weight: 2     # 20% of traffic
```

## Using Workers

Workers are invoked using the same API as models:

```bash
curl http://localhost:8090/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "fallback",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

## Full Example

```yaml
models:
  - from: openai:gpt-4o
    name: gpt4
    params:
      openai_api_key: ${ secrets:OPENAI_API_KEY }
  - from: anthropic:claude-sonnet-4-5
    name: claude
    params:
      anthropic_api_key: ${ secrets:ANTHROPIC_API_KEY }

workers:
  - name: smart_router
    type: load_balance
    description: Try GPT-4 first, fall back to Claude
    load_balance:
      routing:
        - from: gpt4
          order: 1
        - from: claude
          order: 2
```

## Documentation

- [Workers Overview](https://spiceai.org/docs/components/workers)
- [Workers Reference](https://spiceai.org/docs/reference/spicepod/workers)
