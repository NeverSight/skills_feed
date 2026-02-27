---
name: home-assistant-entities-services
description: Home Assistant entity discovery, states, helpers, labels, groups, and services. Use when the user asks about entities or services, needs to rename/move/hide/label entities, or requires service calls via ha-mcp tools.
---

# Home Assistant Entities & Services

## Workflow

- Discover entities and services before acting.
- Inspect current state/metadata before updates.
- When helper selection, templating, or entity renames/refactors are involved, follow `home-assistant-best-practices` references.
- Provide minimal tool calls or YAML examples.

## Tooling map (ha-mcp)

- Discover entities: `ha_get_overview`, `ha_search_entities`, `ha_get_state`
- Find usage/history: `ha_deep_search`, `ha_get_history`, `ha_get_statistics`
- Manage entities: `ha_get_entity`, `ha_set_entity`, `ha_rename_entity`, `ha_rename_entity_and_device`
- Devices: `ha_get_device`, `ha_update_device`
- Helpers: `ha_config_list_helpers`, `ha_config_set_helper`, `ha_create_config_entry_helper`
- Labels: `ha_config_get_label`, `ha_config_set_label`, `ha_manage_entity_labels`
- Groups: `ha_config_list_groups`, `ha_config_set_group`, `ha_config_remove_group`
- Services: `ha_list_services`, `ha_call_service`

## References

All reference files are relative to the location of this SKILL.md file.

- Best practices: `home-assistant-best-practices` (see its `references/helper-selection.md`, `references/template-guidelines.md`, `references/device-control.md`, `references/safe-refactoring.md`)
- State object quick ref: `references/STATE_OBJECT_QUICKREF.md`
- Limited templates: `references/LIMITED_TEMPLATES.md`
