---
name: "proxyman-app-settings"
description: "Inspect, explain, audit, and safely change Proxyman macOS App Settings. Use when a user asks where a preference lives, what it does, why it is locked or ineffective, or requests a settings change or review. Do not use for individual debugging-tool rules."
---

# Proxyman App Settings

Guide the current Proxyman macOS Settings window without treating every preference as an MCP or CLI operation.

## Select The Relevant Reference

- Read [General, Appearance, and Privacy](references/general-appearance-privacy.md) for certificates, proxy port/startup behavior, layout, theme/editor display, analytics, or crash reporting.
- Read [Workspace, Tools, and Integrations](references/workspace-tools-integrations.md) for Team Workspace, Map Local/Scripting defaults, copy/export preferences, GitHub Gist, Products, or MCP.
- Read [Advanced](references/advanced.md) for the Proxy Helper Tool, time format, window/resource behavior, update notifications, proxy restoration, or app language.

Read more than one reference only when the request spans those tabs.

## Establish The Actual UI

This skill's bundled catalog is a reviewed macOS snapshot. Before giving exact current instructions:

1. Identify the installed Proxyman version, distribution, and platform when available.
2. Open the Settings window and use its visible tab/control names as the authority for that build.
3. When product behavior or documentation may have changed, fetch `https://docs.proxyman.com/llms.txt`, follow the selected `.md` link, and cite the corresponding public page. Do not invent a documentation URL.
4. Account for build differences. The reviewed Setapp build omits Workspace and changes some Products destinations.

Do not claim the Windows or Linux Settings UI matches this macOS catalog unless the installed build confirms it.

## Handle A Settings Request

1. Restate the desired outcome and identify the owning tab and control.
2. Read the current value before changing it. For audits, report current, recommended target, consequence, and any restart requirement separately.
3. Check whether the control is unavailable because of license, build, organization/CLI policy, current certificate state, or a genuinely disabled/coming-soon implementation.
4. Explain material side effects before the change. Obtain confirmation immediately before certificate/private-key export or deletion, trust-store changes, helper-tool install/removal, GitHub authorization/removal, public sharing, disabling AI redaction, or exposing script environment variables.
5. Apply only the requested setting through the interface actually exposed by the installed build.
6. Verify by reopening the tab or observing the independent effect described in the relevant reference. A click or saved checkbox alone is not sufficient when runtime behavior is testable.
7. State how to restore the previous value. Record the prior value first when a change affects routing, trust, external sharing, or privacy.

Ordinary reversible display preferences do not need extra confirmation when the user already asked for the change.

## Interface Boundary

The reviewed MCP server has no generic read/write API for App Settings. Use the GUI as the canonical interface unless a specialized overlap exists:

- MCP can inspect/install/uninstall the generated root certificate, but it does not expose every General certificate action.
- MCP can read system/proxy status and change current system-proxy or External Proxy state, but those are not substitutes for startup preferences or arbitrary proxy-port editing.
- `proxyman-cli mcp on|off` controls the MCP organization/CLI lock and persisted server state; discover installed help before use.
- `proxyman-cli export` and `import` operate only on the configuration scope documented by the installed command. Do not assume they serialize every tab.
- Most Appearance, Privacy, Workspace, Tools, GitHub, Products, and Advanced preferences are GUI-only in the reviewed interfaces.

Route generated/custom certificate lifecycle, Debug Mode, Reset Network Proxy, and Factory Reset to `proxyman-certificates-recovery`; live traffic/rule operations to `proxyman-traffic-debugging`; exact shell automation to `proxyman-cli`; MCP client connection work to `proxyman-mcp-setup`; and per-rule feature guidance to `proxyman-debugging-tools`.

## Response Shape

For guidance or an audit, report:

```text
Tab > control
Current state (if observed)
What it changes
How to change it
How to verify
Restart / license / build limitation
Risk and rollback (when material)
Official docs (when available)
```

Say when no dedicated public documentation exists; use the installed UI and reviewed source behavior instead of stretching an unrelated page into evidence.
