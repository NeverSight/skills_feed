---
name: js-gnome-apps
description: Build native GNOME desktop applications using JavaScript (GJS) with GTK 4, Libadwaita, and the GNOME platform. Use when the user wants to create, modify, or debug a GNOME app written in JavaScript/GJS, including UI design with XML or Blueprint, GObject subclassing, Meson build setup, Flatpak packaging, or any task involving GJS bindings for GLib/GIO/GTK4/Adw libraries. Also use when working with `.ui` files, `meson.build`, GResource XML, GSettings schemas, `.desktop` files, or Flatpak manifests in a GJS project context.
---

# GNOME JavaScript (GJS) Application Development

## Technology Stack

| Component            | Purpose                                                               |
| -------------------- | --------------------------------------------------------------------- |
| GJS                  | JavaScript runtime (SpiderMonkey) with GObject Introspection bindings |
| GTK 4                | UI toolkit                                                            |
| Libadwaita (Adw) 1.x | GNOME-specific widgets, adaptive layouts, styling                     |
| GLib / GIO           | Core utilities, async I/O, settings, D-Bus, file operations           |
| Meson                | Build system                                                          |
| Flatpak              | App packaging and distribution                                        |
| Blueprint (optional) | Declarative UI markup that compiles to GTK XML                        |

## Imports (ES Modules — required for new code)

```js
// Built-in GJS modules
import Cairo from "cairo";
import Gettext from "gettext";
import System from "system";

// Platform libraries via gi:// URI
import GLib from "gi://GLib";
import GObject from "gi://GObject";
import Gio from "gi://Gio";

// Versioned imports (required when multiple API versions exist)
import Gtk from "gi://Gtk?version=4.0";
import Adw from "gi://Adw?version=1";

// Relative user modules (include .js extension)
import * as Utils from "./lib/utils.js";
```

Keep imports grouped: built-in → platform (`gi://`) → local, separated by blank lines. Use `PascalCase` for imported modules.

## GObject Subclassing

Register every GObject subclass with `GObject.registerClass()`. Use `constructor()` (not `_init()`, which is legacy pre-GNOME 42).

```js
const MyWidget = GObject.registerClass(
  {
    GTypeName: "MyWidget",
    Template: "resource:///com/example/MyApp/my-widget.ui",
    InternalChildren: ["title_label", "action_button"],
    Properties: {
      "example-prop": GObject.ParamSpec.string(
        "example-prop",
        "",
        "",
        GObject.ParamFlags.READWRITE,
        null,
      ),
    },
    Signals: {
      "item-selected": {
        param_types: [GObject.TYPE_STRING],
      },
    },
  },
  class MyWidget extends Gtk.Box {
    constructor(params = {}) {
      super(params);
      // Template children: this._title_label, this._action_button
    }

    get example_prop() {
      return this._example_prop ?? null;
    }

    set example_prop(value) {
      if (this.example_prop === value) return;
      this._example_prop = value;
      this.notify("example-prop");
    }
  },
);
```

**Key rules:**

- Property names: `kebab-case` in GObject declarations, `snake_case` in JS accessors
- Always call `this.notify('prop-name')` in setters to emit change notifications
- `GTypeName` is optional unless the type is referenced in UI XML `<template class="...">`
- `InternalChildren` maps `id` attrs in UI XML → `this._childId`; `Children` → `this.childId`

## Application Entry Point

```js
import GLib from "gi://GLib";
import GObject from "gi://GObject";
import Gio from "gi://Gio";
import Gtk from "gi://Gtk?version=4.0";
import Adw from "gi://Adw?version=1";

import { MyAppWindow } from "./window.js";

const MyApp = GObject.registerClass(
  class MyApp extends Adw.Application {
    constructor() {
      super({
        application_id: "com.example.MyApp",
        flags: Gio.ApplicationFlags.DEFAULT_FLAGS,
      });

      const quitAction = new Gio.SimpleAction({ name: "quit" });
      quitAction.connect("activate", () => this.quit());
      this.add_action(quitAction);
      this.set_accels_for_action("app.quit", ["<Primary>q"]);
    }

    vfunc_activate() {
      let win = this.active_window;
      if (!win) win = new MyAppWindow(this);
      win.present();
    }
  },
);

const app = new MyApp();
app.run([System.programInvocationName, ...ARGV]);
```

## Async with Gio.\_promisify

Wrap `*_async/*_finish` pairs once at module level for `async/await` usage:

```js
Gio._promisify(
  Gio.File.prototype,
  "load_contents_async",
  "load_contents_finish",
);

const file = Gio.File.new_for_path("/tmp/example.txt");
try {
  const [contents] = await file.load_contents_async(null);
  const text = new TextDecoder().decode(contents);
} catch (e) {
  logError(e, "Failed to load file");
}
```

## Code Style (GJS conventions)

- 4-space indentation, single quotes, semicolons
- `const` by default, `let` when mutation needed, never `var`
- File names: `lowerCamelCase.js`; directories: `lowercase`
- Arrow functions for inline callbacks; `.bind(this)` for method references
- `export` for public API, never `var`

## Reference Files

Consult these based on the task at hand:

- **Project setup & packaging**: [references/project-setup.md](references/project-setup.md) — Meson build, Flatpak manifests, GResource, application ID, desktop files, GSettings schemas, directory layout
- **UI design (GTK4 + Libadwaita)**: [references/ui-patterns.md](references/ui-patterns.md) — Widget templates (UI XML), adaptive layouts (breakpoints, split views, view switcher), boxed lists, style classes, header bars, GNOME HIG patterns
- **GIO & platform patterns**: [references/gio-patterns.md](references/gio-patterns.md) — File I/O, GSettings, actions & menus, D-Bus, subprocesses, list models, GVariant
