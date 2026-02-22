---
name: smartthings-edge-driver
description: Build and troubleshoot SmartThings Edge device drivers in Lua, including Zigbee, Z-Wave, Matter, LAN, capabilities, device profiles, driver channels, and Edge driver API reference usage.
---

# SmartThings Edge Driver

Use this skill when working on SmartThings Edge drivers (Lua). Always open the exact official doc pages from `references/` before answering so guidance stays current.

## Workflow
1. Identify the device protocol (Zigbee, Z-Wave, Matter, LAN) and the device capabilities.
2. Confirm required capabilities, profiles, and preferences in the device docs.
3. Use Edge driver structure docs to set up driver layout and lifecycle handlers.
4. Consult the Edge driver API reference for exact class/module usage and defaults.
5. For protocol-specific behavior, use the corresponding library reference.
6. Link the exact pages used in the response.

## References
- Core Edge docs and device fundamentals: `references/edge-links.md`
- Full Edge driver API reference (Lua): `references/edge-reference.md`

Load only the reference file(s) needed for the user request.
