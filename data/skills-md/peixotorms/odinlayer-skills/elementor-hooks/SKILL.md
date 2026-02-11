---
name: elementor-hooks
description: Use when hooking into Elementor lifecycle events, injecting controls, filtering widget output, or using the JS APIs. Covers elementor/init, elementor/element/before_section_end, elementor/element/after_section_end, elementor/widget/render_content filter, elementor/frontend/after_enqueue_styles, frontend JS hooks (elementorFrontend.hooks, frontend/element_ready), editor JS hooks (elementor.hooks), $e.commands API ($e.run, $e.commands.register), $e.routes, $e.hooks (registerUIBefore, registerUIAfter), control injection patterns, CSS file hooks, forms hooks (Pro), and query filters.
---

# Elementor Hooks Reference

## 1. PHP Action Hooks

### Lifecycle

| Hook Name | Parameters | Description |
|-----------|-----------|-------------|
| `elementor/loaded` | none | Fires when Elementor plugin is loaded, before components initialize. Use for checking Elementor availability. |
| `elementor/init` | none | Fires when Elementor is fully loaded. Use for registering custom functionality. |

### Registration

| Hook Name | Parameters | Description |
|-----------|-----------|-------------|
| `elementor/widgets/register` | `Widgets_Manager $widgets_manager` | Register custom widgets |
| `elementor/controls/register` | `Controls_Manager $controls_manager` | Register custom controls |
| `elementor/dynamic_tags/register` | `Dynamic_Tags_Manager $dynamic_tags_manager` | Register dynamic tags |
| `elementor/finder/register` | `Categories_Manager $categories_manager` | Register Finder categories |
| `elementor/elements/categories_registered` | `Elements_Manager $elements_manager` | Register widget categories |
| `elementor/documents/register` | `Documents_Manager $documents_manager` | Register document types |

### Frontend Scripts and Styles

| Hook Name | Parameters | Description |
|-----------|-----------|-------------|
| `elementor/frontend/after_register_scripts` | none | After frontend scripts registered |
| `elementor/frontend/before_register_scripts` | none | Before frontend scripts registered |
| `elementor/frontend/after_register_styles` | none | After frontend styles registered |
| `elementor/frontend/before_register_styles` | none | Before frontend styles registered |
| `elementor/frontend/after_enqueue_scripts` | none | After frontend scripts enqueued |
| `elementor/frontend/before_enqueue_scripts` | none | Before frontend scripts enqueued |
| `elementor/frontend/after_enqueue_styles` | none | After frontend styles enqueued |
| `elementor/frontend/before_enqueue_styles` | none | Before frontend styles enqueued |

### Editor Scripts and Styles

| Hook Name | Parameters | Description |
|-----------|-----------|-------------|
| `elementor/editor/before_enqueue_scripts` | none | Before editor scripts enqueued |
| `elementor/editor/after_enqueue_scripts` | none | After editor scripts enqueued |
| `elementor/editor/after_enqueue_styles` | none | After editor styles enqueued |
| `elementor/editor/before_enqueue_styles` | none | Before editor styles enqueued |

### Preview Scripts and Styles

| Hook Name | Parameters | Description |
|-----------|-----------|-------------|
| `elementor/preview/enqueue_scripts` | none | Enqueue scripts in the preview iframe |
| `elementor/preview/enqueue_styles` | none | Enqueue styles in the preview iframe |

### Widget Rendering

| Hook Name | Parameters | Description |
|-----------|-----------|-------------|
| `elementor/widget/{$widget_name}/skins_init` | `Widget_Base $widget` | Register custom skins for a widget |
| `elementor/widget/before_render_content` | `Widget_Base $widget` | Before widget content renders |
| `elementor/frontend/before_render` | `Element_Base $element` | Before any element renders (all types) |
| `elementor/frontend/after_render` | `Element_Base $element` | After any element renders (all types) |
| `elementor/frontend/{$element_type}/before_render` | `Element_Base $element` | Before specific element type renders |
| `elementor/frontend/{$element_type}/after_render` | `Element_Base $element` | After specific element type renders |

Element types for `{$element_type}`: `section`, `column`, `container`, `widget`

### Document and Editor Save

| Hook Name | Parameters | Description |
|-----------|-----------|-------------|
| `elementor/documents/register_controls` | `Document $document` | Register controls for documents/page settings |
| `elementor/editor/after_save` | `int $post_id, array $editor_data` | After user saves editor data |
| `elementor/document/before_save` | `Document $document, array $data` | Before document saves |
| `elementor/document/after_save` | `Document $document, array $data` | After document saves |

### CSS File Hooks

| Hook Name | Parameters | Description |
|-----------|-----------|-------------|
| `elementor/element/parse_css` | `Post $post_css, Element_Base $element` | Add custom CSS rules to element CSS |
| `elementor/element/before_parse_css` | `Post $post_css, Element_Base $element` | Before CSS is parsed |
| `elementor/css-file/{$name}/enqueue` | `CSS_File $css_file` | When a CSS file is enqueued |
| `elementor/core/files/clear_cache` | none | When CSS cache is cleared |

### Forms (Pro)

| Hook Name | Parameters | Description |
|-----------|-----------|-------------|
| `elementor_pro/forms/validation` | `Form_Record $record, Ajax_Handler $ajax_handler` | Validate all form fields |
| `elementor_pro/forms/validation/{$field_type}` | `array $field, Form_Record $record, Ajax_Handler $ajax_handler` | Validate specific field type |
| `elementor_pro/forms/process` | `Form_Record $record, Ajax_Handler $ajax_handler` | After fields validated, process form |
| `elementor_pro/forms/process/{$field_type}` | `array $field, Form_Record $record, Ajax_Handler $ajax_handler` | Process specific field type |
| `elementor_pro/forms/new_record` | `Form_Record $record, Ajax_Handler $ajax_handler` | After form actions run |
| `elementor_pro/forms/form_submitted` | `Forms\Module $module` | When form POST received |
| `elementor_pro/forms/mail_sent` | `array $settings, Form_Record $record` | After form email sent |
| `elementor_pro/forms/webhooks/response` | `array\|WP_Error $response, Form_Record $record` | Handle webhook response |

### Query (Pro)

| Hook Name | Parameters | Description |
|-----------|-----------|-------------|
| `elementor/query/{$query_id}` | `WP_Query $query, Widget_Base $widget` | Filter Posts/Portfolio widget query. Set Query ID in widget settings. |

### Other Important Actions

| Hook Name | Parameters | Description |
|-----------|-----------|-------------|
| `elementor/ajax/register_actions` | `Ajax_Manager $ajax_manager` | Register AJAX handlers |
| `elementor/editor/init` | none | Editor initialization |
| `elementor/editor/footer` | none | Editor footer output |
| `elementor/preview/init` | none | Preview initialization |
| `elementor/kit/register_tabs` | `Kit $kit` | Register kit (site settings) tabs |
| `elementor/page_templates/canvas/before_content` | none | Before canvas template content |
| `elementor/page_templates/canvas/after_content` | none | After canvas template content |
| `elementor/template-library/after_save_template` | `int $template_id, array $data` | After template saved |
| `elementor/element/after_add_attributes` | `Element_Base $element` | After render attributes added |
| `elementor/experiments/default-features-registered` | `Experiments_Manager $manager` | Register experiments |

---

## 2. PHP Filter Hooks

### Widget Output Filters

| Filter Name | Parameters | Description |
|-------------|-----------|-------------|
| `elementor/widget/render_content` | `string $content, Widget_Base $widget` | Filter widget HTML on frontend |
| `elementor/{$element_type}/print_template` | `string $template, Widget_Base $widget` | Filter widget JS template in preview |
| `elementor/frontend/the_content` | `string $content` | Filter entire Elementor page output |
| `elementor/frontend/{$element_type}/should_render` | `bool $should_render, Element_Base $element` | Control whether element renders |

### Document and Config Filters

| Filter Name | Parameters | Description |
|-------------|-----------|-------------|
| `elementor/document/config` | `array $config, Document $document` | Filter document config |
| `elementor/document/save/data` | `array $data, Document $document` | Filter data before save |
| `elementor/document/urls/edit` | `string $url, Document $document` | Filter edit URL |
| `elementor/document/urls/preview` | `string $url, Document $document` | Filter preview URL |
| `elementor/editor/localize_settings` | `array $settings` | Filter editor localized settings |

### Visual Element Filters

| Filter Name | Parameters | Description |
|-------------|-----------|-------------|
| `elementor/frontend/print_google_fonts` | `bool $print` | Return false to disable Google Fonts loading |
| `elementor/shapes/additional_shapes` | `array $shapes` | Add custom shape dividers |
| `elementor/mask_shapes/additional_shapes` | `array $shapes` | Add custom mask shapes |
| `elementor/utils/get_placeholder_image_src` | `string $src` | Change default placeholder image |
| `elementor/icons_manager/additional_tabs` | `array $tabs` | Add custom icon libraries |
| `elementor/fonts/additional_fonts` | `array $fonts` | Add custom fonts |
| `elementor/controls/animations/additional_animations` | `array $animations` | Add custom animations |
| `elementor/divider/styles/additional_styles` | `array $styles` | Add custom divider styles |

### Finder and Template Filters

| Filter Name | Parameters | Description |
|-------------|-----------|-------------|
| `elementor/finder/categories` | `array $categories` | Add/modify Finder categories |
| `elementor/template-library/get_template` | `array $template_data` | Filter template data |
| `elementor/template_library/is_template_supports_export` | `bool $supports, array $template` | Control template export |
| `elementor/files/allow_unfiltered_upload` | `bool $allow` | Allow unfiltered file uploads |
| `elementor/files/svg/enabled` | `bool $enabled` | Enable/disable SVG support |

### Forms Filters (Pro)

| Filter Name | Parameters | Description |
|-------------|-----------|-------------|
| `elementor_pro/forms/wp_mail_headers` | `string $headers` | Filter form email headers |
| `elementor_pro/forms/wp_mail_message` | `string $message` | Filter form email body HTML |
| `elementor_pro/custom_fonts/font_display` | `string $display` | Override custom fonts `font-display` value |

### Other Important Filters

| Filter Name | Parameters | Description |
|-------------|-----------|-------------|
| `elementor/frontend/builder_content_data` | `array $data, int $post_id` | Filter builder content data |
| `elementor/frontend/assets_url` | `string $url` | Filter frontend assets URL |
| `elementor/widgets/black_list` | `array $black_list` | Widget class blacklist |
| `elementor/element/get_child_type` | `string $child_type, array $data` | Filter allowed child types |
| `elementor/utils/is_post_type_support` | `bool $support, int $post_id, string $post_type` | Filter post type support |

---

## 3. Injecting Controls

### Targeting All Elements

Inject controls into every element using these hooks:

| Hook Name | Params | Use |
|-----------|--------|-----|
| `elementor/element/before_section_start` | `$element, $section_id, $args` | Add new section before an existing section |
| `elementor/element/after_section_start` | `$element, $section_id, $args` | Add control inside start of existing section |
| `elementor/element/before_section_end` | `$element, $section_id, $args` | Add control inside end of existing section |
| `elementor/element/after_section_end` | `$element, $section_id, $args` | Add new section after an existing section |

### Targeting Specific Elements

Use `{$stack_name}` and `{$section_id}` to target a specific widget and section:

| Hook Pattern | Params | Use |
|-------------|--------|-----|
| `elementor/element/{$stack_name}/{$section_id}/before_section_start` | `$element, $args` | Add section before |
| `elementor/element/{$stack_name}/{$section_id}/after_section_start` | `$element, $args` | Add control at section start |
| `elementor/element/{$stack_name}/{$section_id}/before_section_end` | `$element, $args` | Add control at section end |
| `elementor/element/{$stack_name}/{$section_id}/after_section_end` | `$element, $args` | Add section after |

See `resources/injecting-controls-examples.md` for code examples.

---

## 4. JS Frontend Hooks

Frontend hooks use `elementorFrontend.hooks` (available on the frontend page).

### Actions

| Hook Name | Parameters | Description |
|-----------|-----------|-------------|
| `elementor/frontend/init` | none | Frontend initialized |
| `frontend/element_ready/global` | `$scope (jQuery), $ (jQuery)` | Any element is ready (sections, columns, widgets) |
| `frontend/element_ready/widget` | `$scope (jQuery), $ (jQuery)` | Any widget is ready |
| `frontend/element_ready/{widgetType.skinName}` | `$scope (jQuery), $ (jQuery)` | Specific widget+skin is ready (e.g. `image.default`) |

### Filters

| Hook Name | Parameters | Description |
|-----------|-----------|-------------|
| `frontend/handlers/menu_anchor/scroll_top_distance` | `int scrollTop` | Adjust scroll distance for menu anchors |

See `resources/js-hooks-commands.md` for code examples.

---

## 5. JS Editor Hooks

Editor hooks use `elementor.hooks` (available inside the Elementor editor).

### Actions

| Hook Name | Parameters | Description |
|-----------|-----------|-------------|
| `panel/open_editor/{elementType}` | `panel, model, view` | Settings panel opened for element type (`widget`, `section`, `column`) |
| `panel/open_editor/{elementType}/{elementName}` | `panel, model, view` | Settings panel opened for a specific widget name |

### Filters

| Hook Name | Parameters | Description |
|-----------|-----------|-------------|
| `elements/context-menu/groups` | `array groups` | Modify right-click context menu groups |

See `resources/js-hooks-commands.md` for code examples.

---

## 6. JS Commands API (`$e.commands`)

The Commands API (since 2.7.0) manages all editor commands. Run commands with `$e.run()`.

### Key Methods

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `$e.commands.register()` | `component, command, callback` | `Commands` | Register a new command |
| `$e.run()` | `string command, object args` | `*` | Execute a command |
| `$e.commands.getAll()` | none | `Object` | Get all registered commands |
| `$e.commands.getCurrent()` | none | `Object` | Get currently running commands |
| `$e.commands.is()` | `string command` | `Boolean` | Check if command is currently running |
| `$e.commands.getCurrentArgs()` | none | `Object` | Get args of currently running command |
| `$e.commands.getCurrentFirst()` | none | `String` | Get first currently running command |

### Command Types

| Base Class | Type | Purpose |
|-----------|------|---------|
| `$e.modules.CommandBase` | User commands | Represent user actions |
| `$e.modules.CommandInternalBase` | Internal commands | For internal editor use |
| `$e.modules.CommandData` | Data commands | Communicate with data/cache/backend |

See `resources/js-hooks-commands.md` for full code examples.

---

## 7. JS Components API (`$e.components`)

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `$e.components.register()` | `ComponentBase component` | `ComponentBase` | Register a component |
| `$e.components.get()` | `string id` | `ComponentBase` | Get component by namespace |
| `$e.components.getAll()` | none | `array` | Get all components |
| `$e.components.activate()` | `string namespace` | | Activate a component |
| `$e.components.inactivate()` | `string namespace` | | Deactivate a component |
| `$e.components.isActive()` | `string namespace` | `Boolean` | Check if component is active |
| `$e.components.getActive()` | none | `Object` | Get all active components |

A component serves as a namespace that holds commands, hooks, routes, tabs, shortcuts, and utils. Component class files should be named `component.js`.

See `resources/js-hooks-commands.md` for code examples.

---

## 8. JS Hooks API (`$e.hooks`)

The `$e.hooks` API manages hooks that fire before/after commands run via `$e.run()`.

### UI Hooks

| Method | Parameter | Description |
|--------|-----------|-------------|
| `$e.hooks.registerUIBefore()` | `HookBase instance` | Before command runs (UI) |
| `$e.hooks.registerUIAfter()` | `HookBase instance` | After command runs (UI) |
| `$e.hooks.registerUICatch()` | `HookBase instance` | When command fails (UI) |

### Data Hooks

| Method | Parameter | Description |
|--------|-----------|-------------|
| `$e.hooks.registerDataDependency()` | `HookBase instance` | Before command (dependency check) |
| `$e.hooks.registerDataAfter()` | `HookBase instance` | After command runs (data) |
| `$e.hooks.registerDataCatch()` | `HookBase instance` | When command fails (data) |

See `resources/js-hooks-commands.md` for hook convention code examples and import patterns.

---

## 9. Common Patterns

| I want to... | Use this hook |
|---------------|--------------|
| Register a custom widget | `elementor/widgets/register` (action) |
| Register a custom control | `elementor/controls/register` (action) |
| Add a widget category | `elementor/elements/categories_registered` (action) |
| Register a dynamic tag | `elementor/dynamic_tags/register` (action) |
| Enqueue frontend script | `elementor/frontend/after_register_scripts` (action) |
| Enqueue editor script | `elementor/editor/after_enqueue_scripts` (action) |
| Enqueue preview script | `elementor/preview/enqueue_scripts` (action) |
| Add control to existing widget | `elementor/element/{widget}/{section}/before_section_end` (action) |
| Add control to page settings | `elementor/documents/register_controls` (action) |
| Add control to user preferences | `elementor/element/editor-preferences/preferences/before_section_end` (action) |
| Modify widget HTML output | `elementor/widget/render_content` (filter) |
| Modify widget JS template | `elementor/widget/print_template` (filter) |
| Filter entire page output | `elementor/frontend/the_content` (filter) |
| Disable Google Fonts | `elementor/frontend/print_google_fonts` return false (filter) |
| Change placeholder image | `elementor/utils/get_placeholder_image_src` (filter) |
| Add custom shape dividers | `elementor/shapes/additional_shapes` (filter) |
| Add custom mask shapes | `elementor/mask_shapes/additional_shapes` (filter) |
| Validate form data **(Pro)** | `elementor_pro/forms/validation` (action) |
| Process form after submit **(Pro)** | `elementor_pro/forms/new_record` (action) |
| Filter posts widget query **(Pro)** | `elementor/query/{$query_id}` (action) |
| Add CSS rules to elements | `elementor/element/parse_css` (action) |
| Run code when widget ready (JS) | `frontend/element_ready/{widget.skin}` via `elementorFrontend.hooks` |
| Hook into editor panel open (JS) | `panel/open_editor/{type}/{name}` via `elementor.hooks` |
| Register editor command (JS) | `$e.commands.register()` or component `defaultCommands()` |
| Hook before/after command (JS) | `$e.hooks.registerUIBefore()` / `$e.hooks.registerUIAfter()` |
