---
name: home-assistant-integrations-addons
description: Home Assistant integrations, add-ons, updates, and system operations. Use when the user asks about config entries, add-ons, updates, reloads/restarts, or system health, and when mapping those needs to ha-mcp tools.
---

# Home Assistant Integrations & Add-ons

## Workflow

- Discover current integrations/add-ons and update availability.
- Summarize current state before changes.
- Avoid destructive operations unless explicitly requested.
- Prefer reloads over restarts when supported; validate config before restart.

## Tooling map (ha-mcp)

- Integrations: `ha_get_integration`, `ha_set_integration_enabled`, `ha_delete_config_entry`
- Add-ons: `ha_get_addon`
- Updates: `ha_get_updates`
- System health: `ha_get_system_health`
- Reload/restart: `ha_reload_core`, `ha_check_config`, `ha_restart`

## References

All reference and script files are relative to the location of this SKILL.md file.

- Safe operations: `references/SAFE_OPERATIONS.md`
- Update flow: `references/UPDATE_FLOW.md`
- Add-on notes: `references/ADDON_NOTES.md`
