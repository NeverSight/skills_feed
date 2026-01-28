---
name: accessory-setup-kit
description: AccessorySetupKit for privacy-preserving discovery and setup of Bluetooth, Wi-Fi, or Wi-Fi Aware accessories. Use for discovery sessions, picker-based authorization, migration, accessory renaming or removal, custom filtering, and required Info.plist declarations.
---

# AccessorySetupKit

## What to open

- Use `accessory-setup-kit/accessorysetupkit.md` for all API details and key names.
- Search within it for: "Discovering and configuring accessories", `ASAccessorySession`, `ASDiscoveryDescriptor`, `ASPickerDisplayItem`, `ASMigrationDisplayItem`, `ASPickerDisplaySettings`, and `ASAccessoryEventType`.

## Workflow

- Identify whether the accessory uses Bluetooth, Wi-Fi, or Wi-Fi Aware and set up matching discovery properties.
- Declare required Info.plist keys for AccessorySetupKit and any Bluetooth identifiers.
- Create and activate `ASAccessorySession`, then handle events on the provided queue.
- Present a picker with `ASPickerDisplayItem` items that match the accessories you support.
- Handle `.accessoryAdded` to connect to the selected device; handle `.accessoryRemoved` and `.accessoryChanged` as needed.

## Picker guidance

- A display item must include a descriptor with a Bluetooth identifier or Wi-Fi SSID/SSID prefix.
- For Bluetooth filters, provide at least a service UUID or company identifier, and optionally a name substring or manufacturer/service data mask pair.
- To do custom filtering, enable `filterDiscoveryResults` and handle `.accessoryDiscovered` by creating `ASDiscoveredDisplayItem` entries, then call `updatePicker(showing:completionHandler:)`.
- If custom filtering needs unlimited time, set `discoveryTimeout = .unbounded` and finish discovery with `finishPickerDiscovery(completionHandler:)`.

## Migration and post-setup

- Use `ASMigrationDisplayItem` to migrate previously-configured accessories into AccessorySetupKit.
- Use setup and rename options on picker items when the user should rename or finish setup in-app.

## Reminders

- Keep discovery descriptors specific to avoid broad Bluetooth access.
- For Wi-Fi Aware, set Wi-Fi Aware properties on `ASDiscoveryDescriptor` before discovery.
- Use the session event stream to keep app state in sync with user actions.
