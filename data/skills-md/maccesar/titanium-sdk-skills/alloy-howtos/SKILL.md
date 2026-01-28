---
name: alloy-howtos
description: "PRIMARY SOURCE for ALL official Alloy how-to guides covering best practices, CLI commands, configuration, debugging, and code samples. ALWAYS consult this skill FIRST for ANY Alloy implementation or troubleshooting question before searching online. Covers: (1) Creating/configuring Alloy projects, (2) Alloy CLI commands (new, generate, compile), (3) Configuring alloy.jmk/config.json/widget.json, (4) Debugging Alloy compilation/runtime errors, (5) Conditional views and data-binding, (6) Coding best practices and conventions, (7) Backbone.Events communication, (8) Custom XML tags."
---

# Titanium Alloy How-tos

Comprehensive guide for the Alloy MVC Framework in Titanium SDK.

## Table of Contents

- [Titanium Alloy How-tos](#titanium-alloy-how-tos)
  - [Table of Contents](#table-of-contents)
  - [Quick Reference](#quick-reference)
  - [Critical Best Practices](#critical-best-practices)
    - [Naming Conventions](#naming-conventions)
    - [Global Events - Use Backbone.Events](#global-events---use-backboneevents)
    - [Global Variables in Non-Controller Files](#global-variables-in-non-controller-files)
  - [Conditional Views](#conditional-views)
  - [Common Error Solutions](#common-error-solutions)
  - [CLI Quick Reference](#cli-quick-reference)
  - [Configuration Files Priority](#configuration-files-priority)
  - [Custom XML Tags](#custom-xml-tags)
  - [Resources](#resources)
    - [references/](#references)
  - [Related Skills](#related-skills)

---

## Quick Reference

| Topic                                        | Reference                                                               |
| -------------------------------------------- | ----------------------------------------------------------------------- |
| Best Practices & Naming Conventions          | [best_practices.md](references/best_practices.md)                       |
| CLI Commands (new, generate, compile)        | [cli_reference.md](references/cli_reference.md)                         |
| Configuration Files (alloy.jmk, config.json) | [config_files.md](references/config_files.md)                           |
| Custom XML Tags & Reusable Components        | [custom_tags.md](references/custom_tags.md)                             |
| Debugging & Common Errors                    | [debugging_troubleshooting.md](references/debugging_troubleshooting.md) |
| Code Samples & Conditionals                  | [samples.md](references/samples.md)                                     |

## Critical Best Practices

### Naming Conventions
- **Never use double underscore prefixes** (`__foo`) - reserved for Alloy
- **Never use JavaScript reserved words as IDs**

### Global Events - Use Backbone.Events
**AVOID** `Ti.App.fireEvent` / `Ti.App.addEventListener` - causes memory leaks and poor performance.

**USE** Backbone.Events pattern:
```javascript
// In alloy.js
Alloy.Events = _.clone(Backbone.Events);

// Listener
Alloy.Events.on('updateMainUI', refreshData);
// Clean up on close
$.controller.addEventListener('close', () => {
    Alloy.Events.off('updateMainUI');
});

// Trigger
Alloy.Events.trigger('updateMainUI');
```

### Global Variables in Non-Controller Files
Always require Alloy modules:
```javascript
const Alloy = require('alloy');
const Backbone = require('alloy/backbone');
const _ = require('alloy/underscore')._;
```

## Conditional Views

Use IF attributes in XML for conditional rendering (evaluated before render):

```xml
<Alloy>
    <Window>
        <View if="Alloy.Globals.isLoggedIn()" id="notLoggedIn">
             <Label text="Not logged in" />
        </View>
        <View if="!Alloy.Globals.isLoggedIn()" id="loggedIn">
            <Label text="Logged in" />
        </View>
    </Window>
</Alloy>
```

Conditional TSS styles:
```tss
"#info[if=Alloy.Globals.isIos7Plus]": {
    font: { textStyle: Ti.UI.TEXT_STYLE_FOOTNOTE }
}
```

Data-binding conditionals:
```xml
<TableViewRow if="$model.shouldShowCommentRow()">
```

## Common Error Solutions

| Error                                   | Solution                                                |
| --------------------------------------- | ------------------------------------------------------- |
| `No app.js found`                       | Run `alloy compile --config platform=<platform>`        |
| Android assets not showing              | Use absolute paths (prepend `/`)                        |
| `Alloy is not defined` (non-controller) | Add `const Alloy = require('alloy');`                   |
| iOS `invalid method passed to UIModule` | Creating Android-only object - use `platform` attribute |

## CLI Quick Reference

```bash
# New project
alloy new [path] [template]

# Generate components
alloy generate controller <name>
alloy generate model <name> <adapter> <schema>
alloy generate style --all

# Compile
alloy compile [--config platform=android,deploytype=test]

# Extract i18n strings
alloy extract-i18n en --apply

# Copy/move/remove controllers
alloy copy <old> <new>
alloy move <old> <new>
alloy remove <name>
```

## Configuration Files Priority

**config.json precedence:** `os:ios` > `env:production` > `global`

Access at runtime: `Alloy.CFG.yourKey`

## Custom XML Tags

Create reusable components without widgets - just drop a file in `app/lib/`:

**app/lib/checkbox.js**
```javascript
exports.createCheckBox = args => {
    const wrapper = Ti.UI.createView({ layout: "horizontal", checked: false });
    const box = Ti.UI.createView({ width: 15, height: 15, borderWidth: 1 });
    // ... build component, return Ti.UI.* object
    return wrapper;
};
```

**view.xml**
```xml
<CheckBox module="checkbox" id="terms" caption="I agree" onChange="onCheck" />
```

Key: `module` attribute points to file in `app/lib/` (without `.js`), function must be `create<TagName>`.

See [custom_tags.md](references/custom_tags.md) for complete examples.

## Resources

### references/

Complete documentation for each topic area:
- **best_practices.md** - Coding standards, naming conventions, global events patterns
- **cli_reference.md** - All CLI commands with options and model schema format
- **config_files.md** - alloy.jmk tasks, config.json structure, widget.json format
- **custom_tags.md** - Creating reusable custom XML tags without widgets
- **debugging_troubleshooting.md** - Common errors with solutions
- **samples.md** - Controller examples, conditional views, data-binding patterns

## Related Skills

For tasks beyond Alloy CLI and configuration, use these complementary skills:

| Task                                     | Use This Skill |
| ---------------------------------------- | -------------- |
| Modern architecture, services, patterns  | `alloy-expert` |
| Alloy MVC concepts, models, data binding | `alloy-guides` |
| SDK config, Hyperloop, app distribution  | `ti-guides`    |
| Utility-first styling with PurgeTSS      | `purgetss`     |
