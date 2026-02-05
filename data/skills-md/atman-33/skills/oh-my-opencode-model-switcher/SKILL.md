---
name: oh-my-opencode-model-switcher
description: Switch oh-my-opencode.json model configurations between different modes using YAML-based mapping definitions
metadata:
  short-description: Switch oh-my-opencode model configurations
---

# Model Switcher

This skill enables switching model configurations in oh-my-opencode.json between different modes:
- **default**: Original model settings
- **economy**: All models set to `opencode/glm-4.7-free`

Additional modes can be easily added by editing the mapping configuration.

## Usage

When the user requests to switch models or activate a specific mode, use this skill to update the configuration.

## Workflow

### Switch to a Mode

Execute the switch script with the desired mode:

```bash
python3 ~/.config/opencode/.claude/model-switcher/scripts/switch_models.py [mode_name]
```

Examples:
- `python3 ... switch_models.py economy` - Switch to economy mode
- `python3 ... switch_models.py default` - Switch to default mode

### List Available Modes

```bash
python3 ~/.config/opencode/.claude/model-switcher/scripts/switch_models.py --list
```

## How It Works

1. **Mapping-based approach**: Model assignments are defined in `config/model-mappings.yml`
2. **Partial updates**: Only specified models are updated, preserving other settings
3. **Wildcard support**: Use `"*"` to apply a model to all agents/categories
4. **Field preservation**: Other fields like `variant` are kept unchanged
5. **Structure-resilient**: New agents/categories in oh-my-opencode.json are preserved

## Configuration

Edit [config/model-mappings.yml](config/model-mappings.yml) to:
- Add new modes
- Modify existing mode mappings
- Define per-agent/category model assignments

Example mapping structure:
```yaml
modes:
  mode_name:
    agents:
      agent_name: model_name
      # or use "*" for all agents
    categories:
      category_name: model_name
```
