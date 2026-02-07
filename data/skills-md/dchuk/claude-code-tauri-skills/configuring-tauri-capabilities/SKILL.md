---
name: configuring-tauri-capabilities
description: Guides users through configuring Tauri capabilities for security and access control, covering capability files, permissions, per-window security boundaries, and platform-specific configurations.
---

# Tauri Capabilities Configuration

Capabilities are Tauri's permission management system that granularly controls which APIs and commands the frontend can access. They define security boundaries by specifying which permissions apply to which windows or webviews.

## What Are Capabilities?

Capabilities serve as the bridge between permissions and windows/webviews. They:

- Define which permissions are granted or denied for specific windows
- Enable developers to minimize the impact of frontend compromises
- Create security boundaries based on window labels (not titles)
- Support platform-specific targeting (desktop vs mobile)

## Capability File Location

Capability files reside in `src-tauri/capabilities/` and use JSON or TOML format.

## Capability File Structure

A capability file contains:

| Field | Required | Description |
|-------|----------|-------------|
| `identifier` | Yes | Unique capability name |
| `description` | No | Purpose explanation |
| `windows` | Yes | Target window labels (supports wildcards) |
| `permissions` | Yes | Array of allowed/denied operations |
| `platforms` | No | Target platforms (linux, macOS, windows, iOS, android) |
| `remote` | No | Remote URL access configuration |
| `$schema` | No | Reference to generated schema for IDE support |

## Basic Capability Example

Create `src-tauri/capabilities/main.json`:

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "main-capability",
  "description": "Capability for the main window",
  "windows": ["main"],
  "permissions": [
    "core:path:default",
    "core:event:default",
    "core:window:default",
    "core:app:default",
    "core:resources:default",
    "core:menu:default",
    "core:tray:default"
  ]
}
```

## Default Capabilities

All capabilities in `src-tauri/capabilities/` are automatically enabled by default. No additional configuration is required.

To explicitly control which capabilities are active, configure them in `tauri.conf.json`:

```json
{
  "app": {
    "security": {
      "capabilities": ["main-capability", "editor-capability"]
    }
  }
}
```

When explicitly configured, only the listed capabilities apply.

## Configuration Methods

### Method 1: Separate Files (Recommended)

Store individual capability files in the capabilities directory:

```
src-tauri/
  capabilities/
    main.json
    editor.json
    settings.json
```

Reference by identifier in `tauri.conf.json`:

```json
{
  "app": {
    "security": {
      "capabilities": ["main-capability", "editor-capability", "settings-capability"]
    }
  }
}
```

### Method 2: Inline Definition

Embed capabilities directly in `tauri.conf.json`:

```json
{
  "app": {
    "security": {
      "capabilities": [
        {
          "identifier": "my-capability",
          "description": "Capability used for all windows",
          "windows": ["*"],
          "permissions": ["fs:default", "core:window:default"]
        }
      ]
    }
  }
}
```

### Method 3: Mixed Approach

Combine file-based and inline capabilities:

```json
{
  "app": {
    "security": {
      "capabilities": [
        {
          "identifier": "inline-capability",
          "windows": ["*"],
          "permissions": ["fs:default"]
        },
        "file-based-capability"
      ]
    }
  }
}
```

## Per-Window Capabilities

Assign different permissions to different windows using window labels:

### Single Window

```json
{
  "identifier": "main-capability",
  "windows": ["main"],
  "permissions": ["core:window:default", "fs:default"]
}
```

### Multiple Specific Windows

```json
{
  "identifier": "editor-capability",
  "windows": ["editor", "preview"],
  "permissions": ["fs:read-files", "core:event:default"]
}
```

### Wildcard (All Windows)

```json
{
  "identifier": "global-capability",
  "windows": ["*"],
  "permissions": ["core:event:default"]
}
```

### Pattern Matching

```json
{
  "identifier": "dialog-capability",
  "windows": ["dialog-*"],
  "permissions": ["core:window:allow-close"]
}
```

## Permission Syntax

Permissions follow a naming convention:

| Pattern | Description |
|---------|-------------|
| `<plugin>:default` | Default permission set for a plugin |
| `<plugin>:allow-<command>` | Allow a specific command |
| `<plugin>:deny-<command>` | Deny a specific command |

### Core Permissions

```json
{
  "permissions": [
    "core:path:default",
    "core:event:default",
    "core:window:default",
    "core:window:allow-set-title",
    "core:window:allow-close",
    "core:app:default",
    "core:resources:default",
    "core:menu:default",
    "core:tray:default"
  ]
}
```

### Plugin Permissions

```json
{
  "permissions": [
    "fs:default",
    "fs:allow-read-file",
    "fs:allow-write-file",
    "shell:allow-open",
    "dialog:allow-open",
    "dialog:allow-save",
    "http:default",
    "clipboard-manager:allow-read",
    "clipboard-manager:allow-write"
  ]
}
```

## Platform-Specific Capabilities

Target specific platforms using the `platforms` array.

### Desktop-Only Capability

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "desktop-capability",
  "windows": ["main"],
  "platforms": ["linux", "macOS", "windows"],
  "permissions": [
    "global-shortcut:allow-register",
    "global-shortcut:allow-unregister",
    "shell:allow-execute"
  ]
}
```

### Mobile-Only Capability

```json
{
  "$schema": "../gen/schemas/mobile-schema.json",
  "identifier": "mobile-capability",
  "windows": ["main"],
  "platforms": ["iOS", "android"],
  "permissions": [
    "nfc:allow-scan",
    "biometric:allow-authenticate",
    "barcode-scanner:allow-scan"
  ]
}
```

### Separate Files for Platform Variants

Create platform-specific capability files:

`src-tauri/capabilities/desktop.json`:
```json
{
  "identifier": "desktop-features",
  "windows": ["main"],
  "platforms": ["linux", "macOS", "windows"],
  "permissions": ["global-shortcut:default", "shell:default"]
}
```

`src-tauri/capabilities/mobile.json`:
```json
{
  "identifier": "mobile-features",
  "windows": ["main"],
  "platforms": ["iOS", "android"],
  "permissions": ["haptics:default", "biometric:default"]
}
```

## Remote API Access

Allow remote URLs to access Tauri commands (use with caution):

```json
{
  "$schema": "../gen/schemas/remote-schema.json",
  "identifier": "remote-capability",
  "windows": ["main"],
  "remote": {
    "urls": ["https://*.example.com"]
  },
  "permissions": ["http:default"]
}
```

## Custom Capabilities Example

A multi-window application with different permission levels:

`src-tauri/capabilities/main.json`:
```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "main-window",
  "description": "Full access for main application window",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "fs:default",
    "shell:allow-open",
    "dialog:default",
    "http:default",
    "clipboard-manager:default"
  ]
}
```

`src-tauri/capabilities/settings.json`:
```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "settings-window",
  "description": "Limited access for settings window",
  "windows": ["settings"],
  "permissions": [
    "core:window:allow-close",
    "core:event:default",
    "fs:allow-read-file",
    "fs:allow-write-file"
  ]
}
```

`src-tauri/capabilities/preview.json`:
```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "preview-window",
  "description": "Read-only access for preview window",
  "windows": ["preview"],
  "permissions": [
    "core:window:default",
    "core:event:default",
    "fs:allow-read-file"
  ]
}
```

## Security Boundaries

Capabilities protect against:

- Frontend compromise impact
- Unintended system interface exposure
- Frontend-to-backend privilege escalation

Capabilities do NOT protect against:

- Malicious Rust code
- Overly permissive scopes
- WebView vulnerabilities

## Best Practices

1. **Principle of Least Privilege**: Grant only the permissions each window needs
2. **Separate Capabilities by Window**: Create distinct capability files for different windows
3. **Use Descriptive Identifiers**: Name capabilities clearly (e.g., `main-window`, `editor-readonly`)
4. **Document Capabilities**: Include descriptions explaining the purpose
5. **Review Remote Access**: Carefully audit any remote URL access configurations
6. **Test Permission Boundaries**: Verify windows cannot access unpermitted APIs

## Schema Support

Generated schemas provide IDE autocompletion. Reference them in capability files:

```json
{
  "$schema": "../gen/schemas/desktop-schema.json"
}
```

Available schemas after build:
- `desktop-schema.json` - Desktop platforms
- `mobile-schema.json` - Mobile platforms
- `remote-schema.json` - Remote access capabilities

## Troubleshooting

### Permission Denied Errors

Check that the capability includes the required permission and targets the correct window label.

### Capability Not Applied

Verify the capability file is in `src-tauri/capabilities/` or explicitly listed in `tauri.conf.json`.

### Window Label Mismatch

Window labels in capabilities must match the labels defined when creating windows in Rust code. Labels are case-sensitive.
