---
name: pytincture-dhxpyt
description: Build or modify apps that use the pytincture framework and the dhxpyt widgetset. Use when asked to create pytincture services, add backend-for-frontend (BFF) classes/policies, generate UI layouts with dhxpyt widgets (grid, form, toolbar, sidebar, tabbar, etc.), or embed pytincture.js for browser-only Python UI scripts.
---

# Pytincture + DhxPyt

## Overview
Build Python-driven UIs with dhxpyt and run them either as full pytincture services or as browser-only apps using the pytincture runtime.

## Quick start decisions
- Choose **service mode** when you need backend routes, BFF calls, auth, or full app delivery.
- Choose **standalone mode** when you want a single HTML page that runs Python in the browser with no server.
- Use bundled examples to bootstrap: see `references/examples.md`.

## Task 1: Build a pytincture app (backend + app delivery)
1. Create a module with a `MainWindow` subclass and build UI via dhxpyt.
2. Add any BFF data classes with `@backend_for_frontend` and optional `@bff_policy`.
3. Call `launch_service(modules_folder=".")` so the server can discover your classes.
4. Run the module and open the generated route (typically `/ClassName`).

Start from:
- `assets/examples/pytincture_app/py_ui.py`
- `assets/examples/pytincture_app/py_ui_data.py`

Reference details:
- Read `references/pytincture.md` for BFF policies and service setup.

## Task 2: Build a dhxpyt UI (widgetset-focused)
1. Subclass `MainWindow`.
2. Create a layout with `add_layout` and attach widgets to layout cells.
3. Prefer widget helpers on the layout or window (for example, `add_cardpanel`, `add_grid`, `add_form`) instead of instantiating widgets directly; this guarantees a valid container is created.
4. Configure widgets using `*Config` classes or dicts.
5. Wire event handlers via `.on_*` methods on components (for example, `toolbar.on_click(...)`).

Avoid: `CardPanel(..., root="#id")` unless you have already created that DOM node with `attach_html`.

Start from:
- `assets/examples/dhxpyt_ui/testui.py`

Reference details:
- Read `references/dhxpyt.md` for usage patterns.
- Load `references/dhxpyt.html` when you need full widget API specifics.

## Task 3: Use pytincture.js in a standalone HTML page
1. Use `assets/standalone/index.html` as the base template.
2. Embed Python in `<script type="text/python">`.
3. Add optional wheels to `#micropip-libs`.
4. Set `window.pytinctureAutoStartConfig` if you need custom widgetlib or Pyodide URLs.

Troubleshooting:
- If the runtime tries to fetch a wheel like `dhxpyt-99.99.99-py3-none-any.whl`, it means a placeholder filename was used. Replace it with `"dhxpyt"` in `#micropip-libs` or supply a real wheel file in your appcode.
- If you see `ComboConfig.__init__() got an unexpected keyword argument 'options'`, use `data` instead of `options` for combo items (see `references/dhxpyt/form.html`).
- If you see `CardPanel: target container not found`, make sure the target DOM element exists first, or pass a layout cell as `container` instead of `root` (see `references/dhxpyt/cardpanel.html`).
- If you see `Tabbar.add_cardpanel() got an unexpected keyword argument 'panel_config'`, use `cardpanel_config=` (not `panel_config`).

Reference details:
- Read `references/pytincture-runtime.md` for runtime configuration and manual start.

## Resources
### references/
- `references/pytincture.md`: service mode + BFF policy patterns
- `references/pytincture-runtime.md`: standalone runtime setup
- `references/dhxpyt.md`: dhxpyt usage overview
- `references/dhxpyt.html`: full dhxpyt API docs
- `references/examples.md`: index of bundled example assets

### assets/
- `assets/examples/pytincture_app/`: full app example
- `assets/examples/dhxpyt_ui/`: minimal dhxpyt UI example
- `assets/standalone/`: browser-only runtime template and JS
