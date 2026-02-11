---
name: elementor-development
description: Use when building Elementor addons, creating custom widgets, or managing Elementor components. Covers Widget_Base class (get_name, get_title, get_icon, register_controls, render, content_template), widget registration via elementor/widgets/register hook, addon structure and plugin header, wp_enqueue_script for widget assets, get_script_depends, get_style_depends, inline editing toolbars, custom widget categories, manager registration (register/unregister), selector tokens ({{WRAPPER}}), deprecation handling, and Elementor CLI commands.
---

# Elementor Addon & Widget Development

Consolidated reference for addon architecture, widget creation, manager registration,
scripts/styles, data structure, deprecations, and CLI commands.

See also:
- [Widget Rendering Details](resources/widget-rendering.md) -- full control registration, render(), content_template(), render attributes
- [Data Structure, Deprecations & CLI](resources/data-deprecations-cli.md) -- JSON format, element structure, deprecation timeline, CLI commands

---

## 1. Addon Structure

### Plugin Header

Every Elementor addon requires standard WordPress headers plus optional Elementor headers.

```php
<?php
/**
 * Plugin Name:      Elementor Test Addon
 * Description:      Custom Elementor addon.
 * Plugin URI:       https://elementor.com/
 * Version:          1.0.0
 * Author:           Elementor Developer
 * Author URI:       https://developers.elementor.com/
 * Text Domain:      elementor-test-addon
 * Requires Plugins: elementor
 *
 * Elementor tested up to: 3.25.0
 * Elementor Pro tested up to: 3.25.0
 */

defined( 'ABSPATH' ) || exit;

function elementor_test_addon() {
    require_once __DIR__ . '/includes/plugin.php';
    \Elementor_Test_Addon\Plugin::instance();
}
add_action( 'plugins_loaded', 'elementor_test_addon' );
```

### Main Class (Singleton + Compatibility Checks)

```php
namespace Elementor_Test_Addon;

final class Plugin {

    const VERSION                  = '1.0.0';
    const MINIMUM_ELEMENTOR_VERSION = '3.20.0';
    const MINIMUM_PHP_VERSION      = '7.4';

    private static $_instance = null;

    public static function instance() {
        if ( is_null( self::$_instance ) ) {
            self::$_instance = new self();
        }
        return self::$_instance;
    }

    public function __construct() {
        if ( $this->is_compatible() ) {
            add_action( 'elementor/init', [ $this, 'init' ] );
        }
    }

    public function is_compatible(): bool {
        if ( ! did_action( 'elementor/loaded' ) ) {
            add_action( 'admin_notices', [ $this, 'admin_notice_missing_main_plugin' ] );
            return false;
        }
        if ( ! version_compare( ELEMENTOR_VERSION, self::MINIMUM_ELEMENTOR_VERSION, '>=' ) ) {
            add_action( 'admin_notices', [ $this, 'admin_notice_minimum_elementor_version' ] );
            return false;
        }
        if ( version_compare( PHP_VERSION, self::MINIMUM_PHP_VERSION, '<' ) ) {
            add_action( 'admin_notices', [ $this, 'admin_notice_minimum_php_version' ] );
            return false;
        }
        return true;
    }

    public function init(): void {
        add_action( 'elementor/widgets/register', [ $this, 'register_widgets' ] );
        add_action( 'elementor/controls/register', [ $this, 'register_controls' ] );
    }

    public function register_widgets( $widgets_manager ): void {
        require_once __DIR__ . '/widgets/widget-1.php';
        $widgets_manager->register( new \Elementor_Widget_1() );
    }

    public function register_controls( $controls_manager ): void {
        require_once __DIR__ . '/controls/control-1.php';
        $controls_manager->register( new \Elementor_Control_1() );
    }
}
```

### Folder Structure

```
elementor-test-addon/
  elementor-test-addon.php      # Main file with headers
  includes/
    plugin.php                  # Main class (singleton)
    widgets/                    # Widget classes
    controls/                   # Custom controls
    dynamic-tags/               # Dynamic tag classes
    finder/                     # Finder category classes
  assets/
    js/                         # Frontend/editor JS
    css/                        # Frontend/editor CSS
    images/
```

---

## 2. Widget Development

### Widget Class Skeleton

```php
class Elementor_Test_Widget extends \Elementor\Widget_Base {

    // --- Required ---
    public function get_name(): string {
        return 'test_widget';
    }

    public function get_title(): string {
        return esc_html__( 'Test Widget', 'textdomain' );
    }

    public function get_icon(): string {
        return 'eicon-code';
    }

    public function get_categories(): array {
        return [ 'general' ];
    }

    // --- Optional ---
    public function get_keywords(): array {
        return [ 'test', 'example' ];
    }

    public function get_custom_help_url(): string {
        return 'https://example.com/widget-help';
    }

    public function get_script_depends(): array {
        return [ 'widget-custom-script' ];
    }

    public function get_style_depends(): array {
        return [ 'widget-custom-style' ];
    }

    public function has_widget_inner_wrapper(): bool {
        return false; // DOM optimization: single wrapper
    }

    protected function is_dynamic_content(): bool {
        return false; // Enable output caching for static content
    }

    protected function get_upsale_data(): array {
        return [
            'condition'   => ! \Elementor\Utils::has_pro(),
            'image'       => esc_url( ELEMENTOR_ASSETS_URL . 'images/go-pro.svg' ),
            'image_alt'   => esc_attr__( 'Upgrade', 'textdomain' ),
            'title'       => esc_html__( 'Promotion heading', 'textdomain' ),
            'description' => esc_html__( 'Get the premium version.', 'textdomain' ),
            'upgrade_url' => esc_url( 'https://example.com/upgrade-to-pro/' ),
            'upgrade_text' => esc_html__( 'Upgrade Now', 'textdomain' ),
        ];
    }

    protected function register_controls(): void { /* see resources/widget-rendering.md */ }
    protected function render(): void { /* see resources/widget-rendering.md */ }
    protected function content_template(): void { /* see resources/widget-rendering.md */ }
}
```

### Register Custom Widget Category

```php
function add_elementor_widget_categories( $elements_manager ) {
    $elements_manager->add_category( 'my-category', [
        'title' => esc_html__( 'My Category', 'textdomain' ),
        'icon'  => 'fa fa-plug',
    ] );
}
add_action( 'elementor/elements/categories_registered', 'add_elementor_widget_categories' );
```

### Selector Tokens

| Token | Description |
|-------|-------------|
| `{{WRAPPER}}` | Widget wrapper element |
| `{{VALUE}}` | Control value |
| `{{UNIT}}` | Unit control value |
| `{{URL}}` | URL from media control |
| `{{SELECTOR}}` | Group control CSS selector |

### Inline Editing Toolbars

| Mode | Toolbar | Use Case |
|------|---------|----------|
| `'none'` | No toolbar | Plain text headings |
| `'basic'` | Bold, italic, underline | Short descriptions |
| `'advanced'` | Full (links, headings, lists) | Rich text content |

---

## 3. Manager Registration

### Registration Hooks Reference

| Component | Hook | Manager Type | Method |
|-----------|------|-------------|--------|
| Widgets | `elementor/widgets/register` | `\Elementor\Widgets_Manager` | `register()` / `unregister()` |
| Controls | `elementor/controls/register` | `\Elementor\Controls_Manager` | `register()` / `unregister()` |
| Dynamic Tags | `elementor/dynamic_tags/register` | `\Elementor\Core\DynamicTags\Manager` | `register()` / `unregister()` |
| Finder | `elementor/finder/register` | `Categories_Manager` | `register()` / `unregister()` |
| Categories | `elementor/elements/categories_registered` | `Elements_Manager` | `add_category()` |

### Register Widgets

```php
function register_new_widgets( $widgets_manager ) {
    require_once __DIR__ . '/widgets/widget-1.php';
    $widgets_manager->register( new \Elementor_Widget_1() );
}
add_action( 'elementor/widgets/register', 'register_new_widgets' );
```

### Unregister Widgets

```php
function unregister_widgets( $widgets_manager ) {
    $widgets_manager->unregister( 'heading' );
    $widgets_manager->unregister( 'image' );
}
add_action( 'elementor/widgets/register', 'unregister_widgets' );
```

### Register/Unregister Controls

```php
function register_new_controls( $controls_manager ) {
    require_once __DIR__ . '/controls/control-1.php';
    $controls_manager->register( new \Elementor_Control_1() );
}
add_action( 'elementor/controls/register', 'register_new_controls' );

function unregister_controls( $controls_manager ) {
    $controls_manager->unregister( 'control-1' );
}
add_action( 'elementor/controls/register', 'unregister_controls' );
```

### Register/Unregister Dynamic Tags

```php
function register_dynamic_tags( $dynamic_tags_manager ) {
    require_once __DIR__ . '/dynamic-tags/tag-1.php';
    $dynamic_tags_manager->register( new \Elementor_Dynamic_Tag_1() );
}
add_action( 'elementor/dynamic_tags/register', 'register_dynamic_tags' );

function unregister_dynamic_tags( $dynamic_tags_manager ) {
    $dynamic_tags_manager->unregister( 'dynamic-tag-1' );
}
add_action( 'elementor/dynamic_tags/register', 'unregister_dynamic_tags' );
```

### Register/Unregister Finder Categories

```php
function register_finder_categories( $finder_manager ) {
    require_once __DIR__ . '/finder/finder-1.php';
    $finder_manager->register( new \Elementor_Finder_Category_1() );
}
add_action( 'elementor/finder/register', 'register_finder_categories' );

function unregister_finder_categories( $finder_manager ) {
    $finder_manager->unregister( 'finder-category-1' );
}
add_action( 'elementor/finder/register', 'unregister_finder_categories' );
```

---

## 4. Scripts & Styles

### Frontend Hooks

| Hook | Purpose |
|------|---------|
| `elementor/frontend/before_register_scripts` | Register scripts before Elementor |
| `elementor/frontend/after_register_scripts` | Register scripts after Elementor |
| `elementor/frontend/before_enqueue_scripts` | Enqueue scripts before Elementor |
| `elementor/frontend/after_enqueue_scripts` | Enqueue scripts after Elementor |
| `elementor/frontend/before_register_styles` | Register styles before Elementor |
| `elementor/frontend/after_register_styles` | Register styles after Elementor |
| `elementor/frontend/before_enqueue_styles` | Enqueue styles before Elementor |
| `elementor/frontend/after_enqueue_styles` | Enqueue styles after Elementor |

### Editor Hooks

| Hook | Purpose |
|------|---------|
| `elementor/editor/before_enqueue_scripts` | Enqueue editor scripts (before) |
| `elementor/editor/after_enqueue_scripts` | Enqueue editor scripts (after) |
| `elementor/editor/before_enqueue_styles` | Enqueue editor styles (before) |
| `elementor/editor/after_enqueue_styles` | Enqueue editor styles (after) |

### Preview Hooks

| Hook | Purpose |
|------|---------|
| `elementor/preview/enqueue_scripts` | Enqueue preview scripts |
| `elementor/preview/enqueue_styles` | Enqueue preview styles |

### Frontend Registration Pattern

```php
function my_plugin_frontend_scripts() {
    wp_register_script( 'my-widget-script', plugins_url( 'assets/js/widget.js', __FILE__ ) );
    wp_register_style( 'my-widget-style', plugins_url( 'assets/css/widget.css', __FILE__ ) );
}
add_action( 'wp_enqueue_scripts', 'my_plugin_frontend_scripts' );
```

### Widget-Level Dependencies

Declare in the widget class; Elementor loads them only when the widget is used.

```php
public function get_script_depends(): array {
    return [ 'my-widget-script', 'external-library' ];
}

public function get_style_depends(): array {
    return [ 'my-widget-style', 'external-framework' ];
}
```

### Control-Level Enqueue

```php
class My_Control extends \Elementor\Base_Control {

    protected function enqueue(): void {
        wp_enqueue_script( 'control-script' );
        wp_enqueue_style( 'control-style' );
    }
}
```

---

## 8. Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using `elementor/widgets/widgets_registered` hook | Use `elementor/widgets/register` (old hook deprecated) |
| Calling `register_widget_type()` | Use `register()` on the widgets manager |
| Using `scheme` for colors/typography | Use `global` with `Global_Colors`/`Global_Typography` constants |
| Using `_register_controls()` with underscore prefix | Use `register_controls()` (no underscore) |
| Skipping `did_action('elementor/loaded')` check | Always verify Elementor is loaded before using its classes |
| Missing `Requires Plugins: elementor` header | Add it so WordPress enforces Elementor dependency |
| Using `{{ }}` for HTML output in JS templates | Use `{{{ }}}` (triple) for unescaped HTML; `{{ }}` escapes output |
| Not declaring widget script/style dependencies | Implement `get_script_depends()` / `get_style_depends()` |
| Enqueueing scripts globally instead of per-widget | Register with `wp_register_script`, declare via `get_script_depends()` |
| Using `innerHTML =` in editor JS | Use Elementor template syntax or DOM methods |
| Not using `esc_html__()` for translatable strings | Always wrap user-visible strings in localization functions |
| Missing `defined('ABSPATH') \|\| exit;` guard | Add to every PHP file to prevent direct access |
| Using `has_widget_inner_wrapper` returning `true` without need | Return `false` to reduce DOM nodes (optimization) |
| Not implementing `content_template()` | Without it, editor preview requires server round-trip on every change |
| Using `add_render_attribute` inside `content_template()` | Use `view.addRenderAttribute()` in JS templates |
