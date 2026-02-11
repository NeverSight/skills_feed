---
name: js-gnome-extensions
description: "Build, debug, and maintain GNOME Shell extensions using GJS (GNOME JavaScript). Covers extension anatomy (metadata.json, extension.js, prefs.js, stylesheet.css), ESModule imports, GSettings preferences, popup menus, quick settings, panel indicators, dialogs, notifications, search providers, translations, and session modes. Use when the user wants to: (1) Create a new GNOME Shell extension, (2) Add UI elements like panel buttons, popup menus, quick settings toggles/sliders, or modal dialogs, (3) Implement extension preferences with GTK4/Adwaita, (4) Debug or test an extension, (5) Port an extension to a newer GNOME Shell version (45-49+), (6) Prepare an extension for submission to extensions.gnome.org, (7) Work with GNOME Shell internal APIs (Clutter, St, Meta, Shell, Main)."
---

# GNOME Shell Extensions

Build extensions for GNOME Shell 45+ using GJS with ESModules.

## Key Resources

- **Public APIs (GJS Docs)**: https://gjs-docs.gnome.org/
- **GNOME Shell UI Source**: https://gitlab.gnome.org/GNOME/gnome-shell/-/tree/main/js/ui
- **Extensions Guide**: https://gjs.guide/extensions/
- **Review Guidelines**: https://gjs.guide/extensions/review-guidelines/review-guidelines.html

## Architecture Overview

Extensions run inside the `gnome-shell` process using Clutter/St toolkits (not GTK).
Preferences run in a separate GTK4/Adwaita process.

**Library stack** (bottom-up):

- **Clutter** — Actor-based toolkit, layout managers, animations
- **St** — Shell Toolkit: buttons, icons, labels, entries, scroll views (CSS-styleable)
- **Meta** (Mutter) — displays, workspaces, windows, keybindings
- **Shell** — `global` object, app tracking, utilities
- **js/ui/** — GNOME Shell JS modules (Main, Panel, PopupMenu, QuickSettings, etc.)

Import conventions in `extension.js`:

```js
import Clutter from "gi://Clutter";
import GObject from "gi://GObject";
import Gio from "gi://Gio";
import GLib from "gi://GLib";
import Meta from "gi://Meta";
import Shell from "gi://Shell";
import St from "gi://St";

import {
  Extension,
  gettext as _,
} from "resource:///org/gnome/shell/extensions/extension.js";
import * as Main from "resource:///org/gnome/shell/ui/main.js";
import * as PanelMenu from "resource:///org/gnome/shell/ui/panelMenu.js";
import * as PopupMenu from "resource:///org/gnome/shell/ui/popupMenu.js";
import * as QuickSettings from "resource:///org/gnome/shell/ui/quickSettings.js";
```

Import conventions in `prefs.js`:

```js
import Gdk from "gi://Gdk?version=4.0";
import Gtk from "gi://Gtk?version=4.0";
import Adw from "gi://Adw";
import Gio from "gi://Gio";

import {
  ExtensionPreferences,
  gettext as _,
} from "resource:///org/gnome/Shell/Extensions/js/extensions/prefs.js";
```

**Critical rule**: Never import GTK/Gdk/Adw in `extension.js`. Never import Clutter/Meta/St/Shell in `prefs.js`.

## Extension Lifecycle

### Required Files

1. **`metadata.json`** — UUID, name, description, shell-version, url
2. **`extension.js`** — Default export: subclass of `Extension`

### Optional Files

- **`prefs.js`** — Subclass of `ExtensionPreferences` (GTK4/Adwaita)
- **`stylesheet.css`** — CSS for St widgets in gnome-shell (not prefs)
- **`schemas/`** — GSettings schema XML + compiled binary
- **`locale/`** — Gettext translation .mo files

### enable()/disable() Contract

```js
import { Extension } from "resource:///org/gnome/shell/extensions/extension.js";

export default class MyExtension extends Extension {
  enable() {
    // Create objects, connect signals, add UI
  }

  disable() {
    // MUST undo everything done in enable():
    // - Destroy all created widgets
    // - Disconnect all signals
    // - Remove all GLib.timeout/idle sources
    // - Null out all references
  }
}
```

**Rules** (enforced by extension review):

- Do NOT create GObject instances or connect signals in `constructor()`
- `constructor()` may only set up static data (RegExp, Map, etc.) and call `super(metadata)`
- Everything created in `enable()` MUST be cleaned up in `disable()`
- `disable()` is called on lock screen (unless `session-modes` includes `unlock-dialog`)

## Reference Files

Detailed documentation is split into reference files. Read the appropriate file based on the task:

- **[references/review-guidelines.md](references/review-guidelines.md)** — Complete review rules for extensions.gnome.org submission. Read before submitting or when reviewing extension code for compliance.
- **[references/ui-patterns.md](references/ui-patterns.md)** — Panel indicators, popup menus, quick settings (toggles, sliders, menus), dialogs, notifications, and search providers with complete code examples. Read when building any UI component.
- **[references/preferences.md](references/preferences.md)** — GSettings schemas, prefs.js with GTK4/Adwaita, settings binding. Read when implementing extension preferences.
- **[references/development.md](references/development.md)** — Getting started, testing, debugging, translations, InjectionManager, and packaging. Read when setting up a new extension or debugging.
- **[references/porting-guide.md](references/porting-guide.md)** — Breaking changes for GNOME Shell 45–49. Read when porting an extension to a newer version.

## Quick Start: Panel Indicator Extension

Minimal working extension with a panel icon:

### `metadata.json`

```json
{
  "uuid": "my-extension@example.com",
  "name": "My Extension",
  "description": "Does something useful",
  "shell-version": ["47", "48", "49"],
  "url": "https://github.com/user/my-extension"
}
```

### `extension.js`

```js
import St from "gi://St";

import { Extension } from "resource:///org/gnome/shell/extensions/extension.js";
import * as Main from "resource:///org/gnome/shell/ui/main.js";
import * as PanelMenu from "resource:///org/gnome/shell/ui/panelMenu.js";

export default class MyExtension extends Extension {
  enable() {
    this._indicator = new PanelMenu.Button(0.0, this.metadata.name, false);

    const icon = new St.Icon({
      icon_name: "face-laugh-symbolic",
      style_class: "system-status-icon",
    });
    this._indicator.add_child(icon);

    Main.panel.addToStatusArea(this.uuid, this._indicator);
  }

  disable() {
    this._indicator?.destroy();
    this._indicator = null;
  }
}
```

### Install & Test

```sh
# Create extension directory
mkdir -p ~/.local/share/gnome-shell/extensions/my-extension@example.com
# Copy files there, then:

# Wayland: run nested session
dbus-run-session gnome-shell --devkit --wayland   # GNOME 49+
dbus-run-session gnome-shell --nested --wayland    # GNOME 48 and earlier

# Enable extension in nested session
gnome-extensions enable my-extension@example.com

# Watch logs
journalctl -f -o cat /usr/bin/gnome-shell
```

## Common Patterns Cheatsheet

### Connect a signal (and clean up)

```js
enable() {
    this._handlerId = someObject.connect('some-signal', () => { /* ... */ });
}
disable() {
    if (this._handlerId) {
        someObject.disconnect(this._handlerId);
        this._handlerId = null;
    }
}
```

### Add a timeout (and clean up)

```js
enable() {
    this._timeoutId = GLib.timeout_add_seconds(GLib.PRIORITY_DEFAULT, 5, () => {
        // do work
        return GLib.SOURCE_CONTINUE; // or GLib.SOURCE_REMOVE
    });
}
disable() {
    if (this._timeoutId) {
        GLib.Source.remove(this._timeoutId);
        this._timeoutId = null;
    }
}
```

### Use GSettings

```js
enable() {
    this._settings = this.getSettings(); // uses metadata settings-schema
    this._settings.bind('show-indicator', this._indicator, 'visible',
        Gio.SettingsBindFlags.DEFAULT);
}
disable() {
    this._settings = null;
}
```

### Override a method (InjectionManager)

```js
import {
  Extension,
  InjectionManager,
} from "resource:///org/gnome/shell/extensions/extension.js";
import { Panel } from "resource:///org/gnome/shell/ui/panel.js";

export default class MyExtension extends Extension {
  enable() {
    this._injectionManager = new InjectionManager();
    this._injectionManager.overrideMethod(
      Panel.prototype,
      "toggleCalendar",
      (originalMethod) => {
        return function (...args) {
          console.debug("Calendar toggled!");
          originalMethod.call(this, ...args);
        };
      },
    );
  }
  disable() {
    this._injectionManager.clear();
    this._injectionManager = null;
  }
}
```

## Packaging for Submission

```sh
cd ~/.local/share/gnome-shell/extensions/my-extension@example.com
gnome-extensions pack --podir=po --extra-source=utils.js .

# GNOME 49+: upload directly
gnome-extensions upload --accept-tos
```
