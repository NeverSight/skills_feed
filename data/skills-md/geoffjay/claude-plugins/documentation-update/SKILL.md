---
name: documentation-update
description: Regenerates documentation files (agents.md, agent-skills.md, plugins.md, usage.md) from marketplace data using Jinja templates. Use when plugins are added, updated, or removed to keep documentation in sync.
---

# Documentation Update Skill

This skill automatically regenerates documentation files in the `docs/` directory by reading the marketplace catalog and applying Jinja2 templates.

## Purpose

Maintain synchronized documentation by:

- Generating agent reference documentation
- Creating skill catalog documentation
- Building plugin directory
- Updating usage guides
- Ensuring consistency across all docs

## When to Use

Use this skill when:

- A new plugin is added to the marketplace
- An existing plugin is updated (components added/removed)
- Agent or skill metadata changes
- Documentation needs to be regenerated
- Ensuring docs match marketplace state

## Documentation Files

This skill generates four main documentation files:

### 1. agents.md

Complete reference of all agents across all plugins:

- Organized by plugin
- Lists agent name, description, and model
- Includes links to agent files
- Shows agent capabilities and use cases

### 2. agent-skills.md

Catalog of all skills with progressive disclosure details:

- Organized by plugin
- Lists skill name and description
- Shows "Use when" triggers
- Includes skill structure information

### 3. plugins.md

Directory of all plugins in the marketplace:

- Organized by category
- Shows plugin name, description, and version
- Lists components (agents, commands, skills)
- Provides installation and usage information

### 4. usage.md

Usage guide and command reference:

- Getting started instructions
- Command usage examples
- Workflow patterns
- Integration guides

## Template Structure

Templates are stored in `assets/` using Jinja2 syntax:

```
assets/
├── agents.md.j2
├── agent-skills.md.j2
├── plugins.md.j2
└── usage.md.j2
```

### Template Variables

All templates receive the following context:

```python
{
  "marketplace": {
    "name": "marketplace-name",
    "owner": {...},
    "metadata": {...},
    "plugins": [...]
  },
  "plugins_by_category": {
    "category-name": [plugin1, plugin2, ...]
  },
  "all_agents": [
    {
      "plugin": "plugin-name",
      "name": "agent-name",
      "file": "agent-file.md",
      "description": "...",
      "model": "..."
    }
  ],
  "all_skills": [
    {
      "plugin": "plugin-name",
      "name": "skill-name",
      "path": "skill-path",
      "description": "..."
    }
  ],
  "all_commands": [
    {
      "plugin": "plugin-name",
      "name": "command-name",
      "file": "command-file.md",
      "description": "..."
    }
  ],
  "stats": {
    "total_plugins": 10,
    "total_agents": 25,
    "total_commands": 15,
    "total_skills": 30
  }
}
```

## Python Script

The skill includes a Python script `doc_generator.py` that:

1. **Loads marketplace.json**

   - Reads the marketplace catalog
   - Validates structure
   - Builds component index

2. **Scans Plugin Files**

   - Reads agent/command frontmatter
   - Extracts skill metadata
   - Builds comprehensive component list

3. **Prepares Template Context**

   - Organizes plugins by category
   - Creates component indexes
   - Calculates statistics

4. **Renders Templates**
   - Applies Jinja2 templates
   - Generates documentation files
   - Writes to docs/ directory

### Usage

```bash
# Generate all documentation files
python doc_generator.py

# Generate specific file only
python doc_generator.py --file agents

# Dry run (show output without writing)
python doc_generator.py --dry-run

# Specify custom paths
python doc_generator.py \
  --marketplace .claude-plugin/marketplace.json \
  --templates plugins/claude-plugin/skills/documentation-update/assets \
  --output docs
```

## Integration with Commands

The `/claude-plugin:create` and `/claude-plugin:update` commands should invoke this skill automatically after marketplace updates:

### Workflow

```
1. Plugin operation completes (add/update/remove)
2. Marketplace.json is updated
3. Invoke documentation-update skill
4. Documentation files regenerated
5. Changes ready to commit
```

### Example Integration

```python
# After creating/updating plugin
print("Updating documentation...")

# Run doc generator
import subprocess
result = subprocess.run(
    ["python", "plugins/claude-plugin/skills/documentation-update/doc_generator.py"],
    capture_output=True,
    text=True
)

if result.returncode == 0:
    print("✓ Documentation updated")
else:
    print(f"❌ Documentation update failed: {result.stderr}")
```

## Template Examples

### agents.md.j2

```jinja2
# Agent Reference

This document lists all agents available across plugins in the marketplace.

{% for category, plugins in plugins_by_category.items() %}
## {{ category|title }}

{% for plugin in plugins %}
### {{ plugin.name }}

{{ plugin.description }}

**Agents:**

{% for agent in all_agents %}
{% if agent.plugin == plugin.name %}
- **{{ agent.name }}** (`{{ agent.model }}`)
  - {{ agent.description }}
  - File: `plugins/{{ plugin.name }}/agents/{{ agent.file }}`
{% endif %}
{% endfor %}

{% endfor %}
{% endfor %}

---
*Last updated: {{ now }}*
*Total agents: {{ stats.total_agents }}*
```

### agent-skills.md.j2

```jinja2
# Agent Skills Reference

This document catalogs all skills with progressive disclosure patterns.

{% for plugin in marketplace.plugins %}
## {{ plugin.name }}

{{ plugin.description }}

**Skills:**

{% for skill in all_skills %}
{% if skill.plugin == plugin.name %}
### {{ skill.name }}

{{ skill.description }}

- **Location:** `plugins/{{ plugin.name }}/skills/{{ skill.path }}/`
- **Structure:** SKILL.md + assets/ + references/

{% endif %}
{% endfor %}

{% endfor %}

---
*Last updated: {{ now }}*
*Total skills: {{ stats.total_skills }}*
```

## Error Handling

### Marketplace Not Found

```
Error: Marketplace file not found: .claude-plugin/marketplace.json
Suggestion: Ensure marketplace.json exists
```

### Template Not Found

```
Error: Template file not found: assets/agents.md.j2
Suggestion: Ensure all template files exist in assets/
```

### Invalid Plugin Structure

```
Warning: Plugin 'plugin-name' missing components
Suggestion: Verify plugin has agents or commands
```

### Frontmatter Parse Error

```
Warning: Could not parse frontmatter in agents/agent-name.md
Suggestion: Check YAML frontmatter syntax
```

## Best Practices

1. **Always Regenerate After Changes**

   - Run after every plugin add/update/remove
   - Ensure docs stay synchronized
   - Commit documentation with plugin changes

2. **Validate Before Generation**

   - Run marketplace validation first
   - Fix any errors or warnings
   - Ensure all files exist

3. **Review Generated Output**

   - Check generated files for correctness
   - Verify formatting and links
   - Test any code examples

4. **Template Maintenance**

   - Keep templates simple and readable
   - Use consistent formatting
   - Document template variables

5. **Version Control**
   - Commit documentation changes
   - Include in pull requests
   - Document significant changes

## Template Customization

### Adding New Sections

To add a new section to a template:

1. **Modify Template**

   ```jinja2
   ## New Section

   {% for plugin in marketplace.plugins %}
   ### {{ plugin.name }}
   [Your content here]
   {% endfor %}
   ```

2. **Update Context (if needed)**

   - Add new data to template context in doc_generator.py
   - Process additional metadata

3. **Test Output**
   - Run generator with dry-run
   - Verify formatting
   - Check for errors

### Creating New Templates

To add a new documentation file:

1. **Create Template**

   - Add `assets/newdoc.md.j2`
   - Define structure and content

2. **Update Script**

   - Add to doc_generator.py template list
   - Define output path

3. **Test Generation**
   - Run generator
   - Verify output
   - Commit template and output

## File Structure

```
plugins/claude-plugin/skills/documentation-update/
├── SKILL.md                      # This file
├── doc_generator.py              # Python implementation
├── assets/                       # Jinja2 templates
│   ├── agents.md.j2
│   ├── agent-skills.md.j2
│   ├── plugins.md.j2
│   └── usage.md.j2
└── references/                   # Optional examples
    └── template-examples.md
```

## Requirements

- Python 3.8+
- No external dependencies (uses standard library only)
- Access to `.claude-plugin/marketplace.json`
- Read access to plugin directories
- Write access to `docs/` directory

## Success Criteria

After running this skill:

- ✓ All documentation files generated
- ✓ Content matches marketplace state
- ✓ All links are valid
- ✓ Formatting is consistent
- ✓ Statistics are accurate
- ✓ No template rendering errors

## Maintenance

### Updating Templates

When marketplace structure changes:

1. **Assess Impact**

   - Identify affected templates
   - Determine required changes

2. **Update Templates**

   - Modify Jinja2 templates
   - Test with current data

3. **Update Script**

   - Adjust context preparation if needed
   - Add new data processing

4. **Validate Output**
   - Regenerate all docs
   - Review changes
   - Test links and formatting

### Version Compatibility

- Templates should handle missing fields gracefully
- Use Jinja2 default filters for optional data
- Validate marketplace version compatibility

## Example Output

The skill generates comprehensive, well-formatted documentation:

- **agents.md**: ~500-1000 lines for 20-30 agents
- **agent-skills.md**: ~300-600 lines for 30-50 skills
- **plugins.md**: ~400-800 lines for 10-20 plugins
- **usage.md**: ~200-400 lines of usage information

All files include:

- Clear structure and headings
- Formatted tables where appropriate
- Links to source files
- Statistics and metadata
- Last updated timestamp
