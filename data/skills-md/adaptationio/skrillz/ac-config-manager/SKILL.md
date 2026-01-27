---
name: ac-config-manager
description: Configuration management for autonomous coding. Use when loading settings, managing environment variables, configuring providers, or setting up autonomous mode options.
version: 1.0.0
layer: foundation
category: auto-claude-replication
triggers:
  - "configure autonomous"
  - "setup config"
  - "load settings"
  - "environment config"
---

# AC Config Manager

Centralized configuration management for the Auto-Claude replication skill set.

## Overview

Manages all configuration for autonomous coding:
- Environment variables
- Provider settings (LLM, embeddings, memory)
- Build configuration
- Safety limits
- Path management

## Quick Start

### Load Configuration
```python
from scripts.config_manager import ConfigManager

config = ConfigManager(project_dir)
settings = config.load()

# Access settings
model = settings.model  # claude-opus-4-5-20251101
max_iterations = settings.max_iterations  # 50
```

### Create Configuration
```python
config.create_default_config()
# Creates .claude/autonomous-config.json with defaults
```

### Update Configuration
```python
config.update({
    "max_iterations": 30,
    "max_cost_usd": 15.00,
    "verbose": True
})
```

## Configuration Schema

### .claude/autonomous-config.json
```json
{
  "enabled": true,
  "objective": "Build feature X",
  "success_criteria": [
    "All tests pass",
    "Code coverage > 80%"
  ],
  "max_iterations": 50,
  "max_cost_usd": 20.00,
  "max_consecutive_failures": 3,
  "max_runtime_minutes": 480,
  "analyzer_model": "claude-sonnet-4-20250514",
  "verbose": false,
  "notify_on_complete": true
}
```

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | Yes | - | API key for Claude |
| `AUTO_BUILD_MODEL` | No | claude-opus-4-5-20251101 | Model for builds |
| `DEFAULT_BRANCH` | No | auto-detect | Base branch |
| `GRAPHITI_ENABLED` | No | true | Enable memory |
| `GRAPHITI_LLM_PROVIDER` | No | openai | LLM for memory |
| `GRAPHITI_EMBEDDER_PROVIDER` | No | openai | Embeddings |
| `DEBUG` | No | false | Debug logging |
| `DEBUG_LEVEL` | No | 1 | Verbosity (1-3) |

### Build Configuration

```python
@dataclass
class BuildConfig:
    model: str = "claude-opus-4-5-20251101"
    max_thinking_tokens: dict = field(default_factory=lambda: {
        'planner': 5000,
        'coder': None,
        'qa_reviewer': 10000,
        'qa_fixer': None
    })
    max_iterations: int = 50
    max_parallel_agents: int = 4
    skip_qa: bool = False
    timeout_ms: int = 600000
```

## Operations

### 1. Load Configuration

```python
settings = config.load()
# Merges: defaults → env vars → config file → overrides
```

### 2. Validate Configuration

```python
errors = config.validate()
if errors:
    for error in errors:
        print(f"Config error: {error}")
```

### 3. Get Provider Settings

```python
memory_config = config.get_memory_config()
# Returns Graphiti configuration

build_config = config.get_build_config()
# Returns build settings
```

### 4. Path Management

```python
paths = config.get_paths()
# Returns:
#   specs_dir: .auto-claude/specs/
#   worktrees_dir: .worktrees/auto-claude/
#   memory_dir: .claude/memory/
#   checkpoints_dir: .claude/checkpoints/
```

## Default Values

| Setting | Default | Description |
|---------|---------|-------------|
| `enabled` | false | Autonomous mode |
| `max_iterations` | 50 | Max loop iterations |
| `max_cost_usd` | 20.00 | Budget limit |
| `max_consecutive_failures` | 3 | Before escalation |
| `max_runtime_minutes` | 480 | 8 hour limit |
| `context_threshold` | 0.85 | Trigger handoff |
| `auto_checkpoint` | true | Create checkpoints |

## Integration Points

- **ac-state-tracker**: Loads state config
- **ac-session-manager**: Gets session settings
- **ac-memory-manager**: Gets memory provider config
- **ac-cost-optimizer**: Gets budget limits
- **ac-opus-analyzer**: Gets analyzer model

## References

- `references/CONFIG-SCHEMA.md` - Full schema documentation
- `references/ENVIRONMENT.md` - Environment variable guide

## Scripts

- `scripts/config_manager.py` - Core ConfigManager class
- `scripts/config_schema.py` - Configuration schemas
- `scripts/path_manager.py` - Path utilities
