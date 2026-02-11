---
name: linear-templates
description: Manage Linear issue templates. Use when creating or using templates.
allowed-tools: Bash
---

# Templates

```bash
# List templates
linear-cli tpl list
linear-cli tpl list --output json

# Show template
linear-cli tpl show bug
linear-cli tpl show TEMPLATE_ID --output json

# Create template
linear-cli tpl create bug

# Delete template
linear-cli tpl delete TEMPLATE_ID
```

## Flags

| Flag | Purpose |
|------|---------|
| `--output json` | JSON output |
