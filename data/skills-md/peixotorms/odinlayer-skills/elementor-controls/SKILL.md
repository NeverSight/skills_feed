---
name: elementor-controls
description: Use when adding controls to Elementor widgets, creating custom controls, or referencing control type parameters. Covers add_control with types (TEXT, SELECT, SLIDER, COLOR, MEDIA, REPEATER, CHOOSE, NUMBER, SWITCHER, URL, ICONS), TYPOGRAPHY and BACKGROUND group controls, BORDER, BOX_SHADOW group controls, add_responsive_control, add_group_control, CSS selectors ({{WRAPPER}}, {{VALUE}}), condition and conditions for conditional display, dynamic content tags, POPOVER_TOGGLE, and global styles integration.
---

# Elementor Controls Reference

## 1. Controls Overview

Controls are the fields in the Elementor editor panel that allow users to configure widgets. Every control must live inside a **section**.

**Basic pattern:**
```php
$this->start_controls_section('section_id', [
    'label' => esc_html__('Section', 'textdomain'),
    'tab' => \Elementor\Controls_Manager::TAB_CONTENT, // or TAB_STYLE
]);

$this->add_control('control_id', [
    'label' => esc_html__('Label', 'textdomain'),
    'type' => \Elementor\Controls_Manager::TEXT,
    'default' => '',
]);

$this->end_controls_section();
```

**Control base classes:**

| Base Class | Purpose | Examples |
|---|---|---|
| `Base_Data_Control` | Controls that store a single value | TEXT, SELECT, COLOR, SWITCHER, NUMBER |
| `Control_Base_Multiple` | Controls returning arrays | URL, MEDIA, ICONS, IMAGE_DIMENSIONS |
| `Control_Base_Units` | Controls with size + unit | SLIDER, DIMENSIONS |
| `Base_UI_Control` | Display-only, no stored data | HEADING, DIVIDER, ALERT, RAW_HTML |
| `Group_Control_Base` | Grouped sets of controls | Typography, Background, Border |

**Available tabs:** `TAB_CONTENT`, `TAB_STYLE`, `TAB_ADVANCED`, `TAB_RESPONSIVE`, `TAB_LAYOUT`

**Common parameters (all controls):** `label`, `description`, `show_label` (bool), `label_block` (bool), `separator` (`default`|`before`|`after`), `condition`, `conditions`, `classes`, `dynamic`, `global`, `frontend_available`

## 2. Data Controls Quick Reference

> **Full PHP code examples for all data controls:** see `resources/data-controls-examples.md`

### Text Input Controls

| Control | Constant | Returns | Key Params |
|---|---|---|---|
| Text | `TEXT` | `string` | `input_type`, `placeholder`, `title` |
| Textarea | `TEXTAREA` | `string` | `rows`, `placeholder` |
| WYSIWYG | `WYSIWYG` | `string` | (rich text editor) |
| Code | `CODE` | `string` | `language` (`html`\|`css`\|`javascript`), `rows` |
| Number | `NUMBER` | `string` | `min`, `max`, `step`, `placeholder` |
| Hidden | `HIDDEN` | `string` | `default` (only param that matters) |

### Selection Controls

| Control | Constant | Returns | Key Params |
|---|---|---|---|
| Select | `SELECT` | `string` | `options` (key=>label array), `groups` |
| Select2 | `SELECT2` | `string\|array` | `options`, `multiple` (bool), `select2options` |
| Choose | `CHOOSE` | `string` | `options` (key=>[title,icon]), `toggle` (bool) |
| Visual Choice | `VISUAL_CHOICE` | `string` | `options` (key=>[title,image]) |
| Switcher | `SWITCHER` | `string` | `label_on`, `label_off`, `return_value` (default `'yes'`) |

### Unit / Dimension Controls

| Control | Constant | Returns | Key Params |
|---|---|---|---|
| Slider | `SLIDER` | `['size'=>int, 'unit'=>string]` | `size_units`, `range` (per unit: min/max/step) |
| Dimensions | `DIMENSIONS` | `['top','right','bottom','left','unit','isLinked']` | `size_units`, `range`, `allowed_dimensions` |
| Image Dimensions | `IMAGE_DIMENSIONS` | `['width'=>int, 'height'=>int]` | `default` |

### Media / Asset Controls

| Control | Constant | Returns | Key Params |
|---|---|---|---|
| Color | `COLOR` | `string` (hex/rgba) | `alpha` (bool, default true) |
| Media | `MEDIA` | `['id'=>int, 'url'=>string]` | `media_types` (default `['image']`) |
| Gallery | `GALLERY` | `array` of `['id','url']` | `default` |
| Icons | `ICONS` | `['value'=>string, 'library'=>string]` | `default`, `fa4compatibility`, `recommended`, `skin` |
| Icon | `ICON` | `string` | DEPRECATED - use ICONS instead |
| Font | `FONT` | `string` | `default` |
| URL | `URL` | `['url','is_external','nofollow','custom_attributes']` | `placeholder`, `autocomplete`, `options` |
| Date Time | `DATE_TIME` | `string` | `picker_options` (Flatpickr config) |

### REPEATER

Returns: `array` of rows, each row is an assoc array of field values. Use `title_field` for dynamic row labels.

**Render:** PHP: `$settings['list']` is array of rows. Each row has `_id` key. Use class `elementor-repeater-item-{$item['_id']}` for per-item styling with `{{CURRENT_ITEM}}`. JS template: `_.each(settings.list, function(item) { ... item._id ... })`

### POPOVER_TOGGLE

Used with `start_popover()` / `end_popover()` to group controls in a popup.

## 3. UI Controls

UI controls display information in the panel but store no data.

| Control | Constant | Key Params | Purpose |
|---|---|---|---|
| Heading | `HEADING` | `label` | Section heading text |
| Divider | `DIVIDER` | - | Horizontal separator line |
| Alert | `ALERT` | `alert_type` (`info`\|`success`\|`warning`\|`danger`), `content` | Colored alert box |
| Notice | `NOTICE` | `notice_type`, `content`, `dismissible` (bool), `heading` | Dismissible notice |
| Raw HTML | `RAW_HTML` | `raw`, `content_classes` | Arbitrary HTML in panel |
| Button | `BUTTON` | `text`, `button_type` (`default`\|`success`), `event` | Clickable button |
| Deprecated Notice | `DEPRECATED_NOTICE` | `widget`, `since`, `last`, `plugin`, `replacement` | Deprecation warning |

```php
// HEADING
$this->add_control('heading_style', [
    'label' => esc_html__('Title Style', 'textdomain'),
    'type' => \Elementor\Controls_Manager::HEADING,
    'separator' => 'before',
]);

// DIVIDER
$this->add_control('hr', [
    'type' => \Elementor\Controls_Manager::DIVIDER,
]);
```

## 4. Group Controls

Group controls bundle multiple related controls. Use `add_group_control()` with `selector` (singular, string) for CSS targeting.

> **Full PHP code examples for group controls, fields_options, custom controls, and global styles:** see `resources/group-custom-controls.md`

| Group Control | Class | Type Getter | Key Params |
|---|---|---|---|
| Typography | `Group_Control_Typography` | `::get_type()` | `selector`, `fields_options`, `global` |
| Background | `Group_Control_Background` | `::get_type()` | `selector`, `types` (`classic`\|`gradient`\|`video`\|`slideshow`) |
| Border | `Group_Control_Border` | `::get_type()` | `selector`, `fields_options` |
| Box Shadow | `Group_Control_Box_Shadow` | `::get_type()` | `selector`, `exclude` |
| Text Shadow | `Group_Control_Text_Shadow` | `::get_type()` | `selector`, `exclude` |
| Text Stroke | `Group_Control_Text_Stroke` | `::get_type()` | `selector`, `exclude` |
| CSS Filter | `Group_Control_Css_Filter` | `::get_type()` | `selector`, `exclude` |
| Image Size | `Group_Control_Image_Size` | `::get_type()` | `include`, `exclude`, `default` |

**Common group control params:** `name` (required, unique prefix), `selector`, `exclude` (array of inner control names), `fields_options` (override inner control settings).

## 5. Structural Controls

### Sections
Every control must be inside a section. Sections appear as collapsible panels.

```php
$this->start_controls_section('section_id', [
    'label' => esc_html__('Section Name', 'textdomain'),
    'tab' => \Elementor\Controls_Manager::TAB_CONTENT,  // default
    'condition' => [],  // optional
]);
// ... controls ...
$this->end_controls_section();
```

### Tabs (within a section)
Group controls into switchable tabs (e.g., Normal / Hover).

```php
$this->start_controls_tabs('style_tabs');

$this->start_controls_tab('normal_tab', [
    'label' => esc_html__('Normal', 'textdomain'),
]);
// ... normal state controls ...
$this->end_controls_tab();

$this->start_controls_tab('hover_tab', [
    'label' => esc_html__('Hover', 'textdomain'),
]);
// ... hover state controls ...
$this->end_controls_tab();

$this->end_controls_tabs();
```

### Popovers
Group controls in a popup that appears on toggle.

```php
$this->add_control('popover_toggle', [
    'type' => \Elementor\Controls_Manager::POPOVER_TOGGLE,
    'label' => esc_html__('Options', 'textdomain'),
    'label_off' => esc_html__('Default', 'textdomain'),
    'label_on' => esc_html__('Custom', 'textdomain'),
    'return_value' => 'yes',
]);
$this->start_popover();
// ... controls ...
$this->end_popover();
```

## 6. CSS Selectors

### The `{{WRAPPER}}` Pattern
All selectors should use `{{WRAPPER}}` for scoped styling. Resolves to `.elementor-{page_id} .elementor-element.elementor-element-{widget_id}`.

### Value Placeholders by Control Type

| Control Type | Selector Pattern |
|---|---|
| String controls (TEXT, SELECT, COLOR, etc.) | `'{{WRAPPER}} .el' => 'property: {{VALUE}};'` |
| SLIDER | `'{{WRAPPER}} .el' => 'width: {{SIZE}}{{UNIT}};'` |
| DIMENSIONS | `'{{WRAPPER}} .el' => 'margin: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};'` |
| URL / MEDIA | `'{{WRAPPER}} .el' => 'background-image: url({{URL}});'` |

### Multiple Properties in One Selector
```php
'selectors' => [
    '{{WRAPPER}} .el' => 'color: {{VALUE}}; border-color: {{VALUE}}; outline-color: {{VALUE}};',
],
```

### Multiple / Comma-Separated Selectors
```php
'selectors' => [
    '{{WRAPPER}} .heading, {{WRAPPER}} .content' => 'color: {{VALUE}};',
],
// OR as separate keys:
'selectors' => [
    '{{WRAPPER}} .heading' => 'color: {{VALUE}};',
    '{{WRAPPER}} .content' => 'color: {{VALUE}};',
],
```

### RTL/LTR Support
```php
'selectors' => [
    'body:not(.rtl) {{WRAPPER}} .el' => 'padding-left: {{VALUE}};',
    'body.rtl {{WRAPPER}} .el' => 'padding-right: {{VALUE}};',
],
```

### Hover States
```php
// Via group control:
'selector' => '{{WRAPPER}}:hover .el',
// Via tabs: put controls in a "Hover" tab
```

### Cross-Control Values
Reference another control's value by prefixing with the control name:
```php
$this->add_control('aspect_width', [
    'type' => \Elementor\Controls_Manager::NUMBER,
]);
$this->add_control('aspect_height', [
    'type' => \Elementor\Controls_Manager::NUMBER,
    'selectors' => [
        '{{WRAPPER}} img' => 'aspect-ratio: {{aspect_width.VALUE}} / {{aspect_height.VALUE}};',
    ],
]);
```

### Selectors Dictionary
Transform old stored values to new CSS values (backward compat). Only works with string-returning controls.
```php
$this->add_control('align', [
    'type' => \Elementor\Controls_Manager::CHOOSE,
    'selectors_dictionary' => [
        'left' => is_rtl() ? 'end' : 'start',
        'right' => is_rtl() ? 'start' : 'end',
    ],
    'selectors' => [
        '{{WRAPPER}} .el' => 'text-align: {{VALUE}};',
    ],
]);
```

### Element ID
`{{ID}}` resolves to the element's unique ID. Discouraged -- prefer `{{WRAPPER}}`.

## 7. Responsive Controls

Use `add_responsive_control()` instead of `add_control()`. Automatically creates per-device controls.

```php
$this->add_responsive_control('spacing', [
    'label' => esc_html__('Spacing', 'textdomain'),
    'type' => \Elementor\Controls_Manager::SLIDER,
    'range' => ['px' => ['min' => 0, 'max' => 100]],
    'devices' => ['desktop', 'tablet', 'mobile'],    // optional, default all 3
    'default' => ['size' => 30, 'unit' => 'px'],
    'tablet_default' => ['size' => 20, 'unit' => 'px'],
    'mobile_default' => ['size' => 10, 'unit' => 'px'],
    'selectors' => [
        '{{WRAPPER}} .el' => 'margin-bottom: {{SIZE}}{{UNIT}};',
    ],
]);
```

The `devices` parameter limits which breakpoints appear. Per-device defaults use `tablet_default` and `mobile_default` keys. Group controls automatically support responsive for their inner controls.

## 8. Conditional Display

### Basic `condition` Parameter
```php
// Show only when 'border' switcher is 'yes'
'condition' => ['border' => 'yes'],

// Show when value is one of multiple options (OR)
'condition' => ['type' => ['option1', 'option2']],

// Multiple conditions (AND)
'condition' => [
    'border' => 'yes',
    'border_style!' => '',   // ! suffix = not equal
],
```

### Advanced `conditions` Parameter
Supports operators: `==`, `!=`, `!==`, `===`, `in`, `!in`, `contains`, `!contains`, `<`, `<=`, `>`, `>=`
```php
'conditions' => [
    'relation' => 'or',  // 'and' (default) or 'or'
    'terms' => [
        ['name' => 'type', 'operator' => '===', 'value' => 'video'],
        ['name' => 'type', 'operator' => '===', 'value' => 'slideshow'],
    ],
],
```

Conditions can be nested. Repeater inner fields can only depend on other inner fields, NOT outer controls.

## 9. Dynamic Content

Enable dynamic tags (Elementor Pro) on any data control:

```php
$this->add_control('heading', [
    'label' => esc_html__('Heading', 'textdomain'),
    'type' => \Elementor\Controls_Manager::TEXT,
    'dynamic' => ['active' => true],
]);
```

Works with: TEXT, TEXTAREA, NUMBER, URL, MEDIA, WYSIWYG, and most data controls.

### Frontend Available
```php
$this->add_control('slides_count', [
    'type' => \Elementor\Controls_Manager::NUMBER,
    'default' => 3,
    'frontend_available' => true,  // default: false
]);
```
Access in JS handler: `this.getElementSettings('slides_count')`

## 10. Global Styles

Use the `global` parameter to inherit from the site's design system (set in Site Settings).

### Global Colors Constants
- `\Elementor\Core\Kits\Documents\Tabs\Global_Colors::COLOR_PRIMARY`
- `\Elementor\Core\Kits\Documents\Tabs\Global_Colors::COLOR_SECONDARY`
- `\Elementor\Core\Kits\Documents\Tabs\Global_Colors::COLOR_TEXT`
- `\Elementor\Core\Kits\Documents\Tabs\Global_Colors::COLOR_ACCENT`

### Global Typography Constants
- `\Elementor\Core\Kits\Documents\Tabs\Global_Typography::TYPOGRAPHY_PRIMARY`
- `\Elementor\Core\Kits\Documents\Tabs\Global_Typography::TYPOGRAPHY_SECONDARY`
- `\Elementor\Core\Kits\Documents\Tabs\Global_Typography::TYPOGRAPHY_TEXT`
- `\Elementor\Core\Kits\Documents\Tabs\Global_Typography::TYPOGRAPHY_ACCENT`

Controls with `global` show a globe icon for users to pick a global style or set custom.

## 12. Common Mistakes

| Mistake | Correct Approach |
|---|---|
| Using `add_control()` outside a section | Always wrap in `start_controls_section()` / `end_controls_section()` |
| Using `selector` (singular) on non-group controls | Non-group controls use `selectors` (plural, array). Group controls use `selector` (singular, string). |
| Forgetting `{{WRAPPER}}` in selectors | Always prefix selectors with `{{WRAPPER}}` for scoped styles |
| Using `{{VALUE}}` with SLIDER control | SLIDER returns array; use `{{SIZE}}{{UNIT}}` |
| Using `{{VALUE}}` with DIMENSIONS control | Use `{{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}}` |
| Using `{{VALUE}}` with URL/MEDIA control | Use `{{URL}}` for the URL component |
| Nesting `start_controls_section` inside another | Sections cannot be nested. End one before starting another. |
| Putting tabs outside a section | `start_controls_tabs()` must be inside a section |
| Repeater inner field depending on outer control | Conditional display across repeater levels is not supported |
| Using `selectors_dictionary` with array-returning controls | Only works with string-value controls (TEXT, SELECT, CHOOSE, etc.) |
| Not using `esc_html__()` for labels | Always internationalize user-facing strings |
| Setting SWITCHER default to `true` or `1` | SWITCHER returns a string; default should be `'yes'` or `''` |
| Using `innerHTML =` on frontend | Use Elementor's rendering patterns; may be blocked by CSP |
| Setting REPEATER `prevent_empty` wrong | Defaults to `true`; set `false` if all rows should be deletable |
