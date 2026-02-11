---
name: elementor-themes
description: Use when building Elementor-compatible themes, registering theme locations, creating dynamic tags, or extending the Finder. Covers register_location, theme_builder locations, elementor_theme_do_location, Theme_Document and theme conditions, Tag_Base for dynamic tags (register_tag, get_value, render), Finder extension (Category_Base, register via elementor/finder/register), Context_Menu customization (elements/context-menu/groups filter), Hello Elementor theme (elementor-hello-theme, hello_elementor_* filters), and hosting page cache integration hooks.
---

## 1. Theme Builder Locations

### Registering Locations

Register all core locations at once:

```php
function theme_prefix_register_elementor_locations( $elementor_theme_manager ) {
    $elementor_theme_manager->register_all_core_location();
}
add_action( 'elementor/theme/register_locations', 'theme_prefix_register_elementor_locations' );
```

Register specific locations or custom locations:

```php
$elementor_theme_manager->register_location( 'header' );
$elementor_theme_manager->register_location( 'footer' );
$elementor_theme_manager->register_location( 'main-sidebar', [
    'label' => esc_html__( 'Main Sidebar', 'theme-name' ),
    'multiple' => true,        // allow multiple templates (default: false)
    'edit_in_content' => false, // edit in content area (default: true)
] );
```

### Location Types

| Location | Replaces |
|----------|----------|
| `header` | header.php |
| `footer` | footer.php |
| `single` | singular.php, single.php, page.php, attachment.php, 404.php |
| `archive` | archive.php, taxonomy.php, author.php, date.php, search.php |

### Displaying Locations with Fallback

```php
<?php
if ( ! function_exists( 'elementor_theme_do_location' ) || ! elementor_theme_do_location( 'archive' ) ) {
    get_template_part( 'template-parts/archive' );
}
?>
```

`elementor_theme_do_location()` returns `true` if a template was displayed, `false` otherwise.

### Migration: Functions Method

Use `elementor_theme_do_location()` with fallback in header.php, footer.php, single.php, archive.php:

```php
<!-- header.php -->
<!doctype html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo( 'charset' ); ?>">
    <?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php
if ( ! function_exists( 'elementor_theme_do_location' ) || ! elementor_theme_do_location( 'header' ) ) {
    get_template_part( 'template-parts/header' );
}
?>
```

### Migration: Hooks Method

Register locations with `hook` and `remove_hooks` parameters to auto-replace theme output:

```php
$elementor_theme_manager->register_location( 'header', [
    'hook' => 'theme_prefix_header',
    'remove_hooks' => [ 'theme_prefix_print_elementor_header' ],
] );
```

## 2. Theme Conditions

### Class Structure

Extend `\ElementorPro\Modules\ThemeBuilder\Conditions\Condition_Base`.

Required methods:

| Method | Returns | Purpose |
|--------|---------|---------|
| `get_type()` | string | Condition group: `general`, `singular`, `archive` |
| `get_name()` | string | Unique condition identifier |
| `get_label()` | string | Display label |
| `check( $args )` | bool | Evaluate if condition matches |
| `get_all_label()` | string | Label for "All" option (parent conditions only) |
| `register_sub_conditions()` | void | Register child conditions |

### Registration

```php
function register_new_theme_conditions( $conditions_manager ) {
    require_once( __DIR__ . '/theme-conditions/my-condition.php' );
    $conditions_manager->get_condition( 'general' )->register_sub_condition( new \My_Condition() );
}
add_action( 'elementor/theme/register_conditions', 'register_new_theme_conditions' );
```

### Condition Groups

| ID | Label | Description |
|----|-------|-------------|
| `general` | General | Entire site conditions |
| `archive` | Archives | Archive page conditions |
| `singular` | Singular | Single page/post conditions |

### Simple Example: 404 / Front Page

```php
class Front_Page_Condition extends \ElementorPro\Modules\ThemeBuilder\Conditions\Condition_Base {
    public static function get_type(): string { return 'general'; }
    public function get_name(): string { return 'front_page'; }
    public function get_label(): string { return esc_html__( 'Front Page', 'textdomain' ); }
    public function check( $args ): bool { return is_front_page(); }
}

class Not_Found_Condition extends \ElementorPro\Modules\ThemeBuilder\Conditions\Condition_Base {
    public static function get_type(): string { return 'general'; }
    public function get_name(): string { return 'not_found_404'; }
    public function get_label(): string { return esc_html__( '404 Page', 'textdomain' ); }
    public function check( $args ): bool { return is_404(); }
}
```

### Advanced Example: Parent with Sub-Conditions

```php
class Logged_In_User_Condition extends \ElementorPro\Modules\ThemeBuilder\Conditions\Condition_Base {
    public static function get_type(): string { return 'general'; }
    public function get_name(): string { return 'logged_in_user'; }
    public function get_label(): string { return esc_html__( 'Logged-in User', 'textdomain' ); }
    public function get_all_label(): string { return esc_html__( 'Any user role', 'textdomain' ); }

    public function register_sub_conditions(): void {
        global $wp_roles;
        if ( ! isset( $wp_roles ) ) { $wp_roles = new \WP_Roles(); }
        foreach ( $wp_roles->get_names() as $role ) {
            $this->register_sub_condition( new \User_Role_Condition( $role ) );
        }
    }

    public function check( $args ): bool { return is_user_logged_in(); }
}

class User_Role_Condition extends \ElementorPro\Modules\ThemeBuilder\Conditions\Condition_Base {
    private $user_role;
    public function __construct( $user_role ) { parent::__construct(); $this->user_role = $user_role; }
    public static function get_type(): string { return 'logged_in_user'; }
    public function get_name(): string { return strtolower( $this->user_role . '_role' ); }
    public function get_label(): string { return sprintf( esc_html__( '%s role', 'textdomain' ), $this->user_role ); }
    public function check( $args ): bool {
        $current_user = wp_get_current_user();
        return in_array( $this->user_role, (array) $current_user->roles );
    }
}
```

## 3. Dynamic Tags

### Class Structure

Extend `\Elementor\Core\DynamicTags\Tag`.

Required methods:

| Method | Returns | Purpose |
|--------|---------|---------|
| `get_name()` | string | Unique tag identifier |
| `get_title()` | string | Display title |
| `get_group()` | array | Groups this tag belongs to |
| `get_categories()` | array | Data type categories |
| `render()` | void | Output the dynamic value (echo) |
| `register_controls()` | void | Optional: add tag settings |

### Dynamic Tag Categories

| Constant | Value | Use For |
|----------|-------|---------|
| `Module::NUMBER_CATEGORY` | `number` | Numeric values |
| `Module::TEXT_CATEGORY` | `text` | Text strings |
| `Module::URL_CATEGORY` | `url` | URLs |
| `Module::COLOR_CATEGORY` | `color` | Color values |
| `Module::IMAGE_CATEGORY` | `image` | Image data |
| `Module::MEDIA_CATEGORY` | `media` | Media files |
| `Module::GALLERY_CATEGORY` | `gallery` | Image galleries |
| `Module::POST_META_CATEGORY` | `post_meta` | Post meta fields |

Full constant path: `\Elementor\Modules\DynamicTags\Module::CATEGORY_NAME`.

### Registration

```php
function register_dynamic_tags( $dynamic_tags_manager ) {
    require_once( __DIR__ . '/dynamic-tags/my-tag.php' );
    $dynamic_tags_manager->register( new \My_Dynamic_Tag() );
}
add_action( 'elementor/dynamic_tags/register', 'register_dynamic_tags' );
```

### Register Custom Group

```php
function register_custom_dynamic_tag_group( $dynamic_tags_manager ) {
    $dynamic_tags_manager->register_group( 'my-group', [
        'title' => esc_html__( 'My Group', 'textdomain' ),
    ] );
}
add_action( 'elementor/dynamic_tags/register', 'register_custom_dynamic_tag_group' );
```

### Controls in Dynamic Tags

Use `$this->add_control()` in `register_controls()` and `$this->get_settings( 'key' )` in `render()`.

### Code Examples

See [resources/dynamic-tags.md](resources/dynamic-tags.md) for complete examples: Simple tag (Random Number), Advanced tag with controls (ACF Average), Complex tag with SELECT control (Server Variables), and unregistering tags.

## 4. Finder

### Class Structure

Extend `\Elementor\Core\Common\Modules\Finder\Base_Category`.

| Method | Returns | Purpose |
|--------|---------|---------|
| `get_id()` | string | Unique category identifier |
| `get_title()` | string | Display title |
| `get_category_items( array $options = [] )` | array | Items in this category |
| `is_dynamic()` | bool | If true, items loaded via AJAX on search |

### Item Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `title` | string | Yes | Displayed to user |
| `icon` | string | No | Icon before title |
| `url` | string | Yes | Link URL |
| `keywords` | array | No | Search keywords |

### Registration

```php
function register_finder_category( $finder_categories_manager ) {
    require_once( __DIR__ . '/finder/my-category.php' );
    $finder_categories_manager->register( new \My_Finder_Category() );
}
add_action( 'elementor/finder/register', 'register_finder_category' );
```

### Default Categories

| ID | Description |
|----|-------------|
| `create` | Create posts, pages, templates |
| `edit` | Edit posts, pages, templates |
| `general` | General Elementor links |
| `settings` | Elementor settings pages |
| `tools` | Elementor tools |
| `site` | Site links |

### Add Items to Existing Category

```php
function add_finder_items( array $categories ) {
    $categories['create']['items']['theme-template'] = [
        'title' => esc_html__( 'Add New Theme Template', 'textdomain' ),
        'icon' => 'plus-circle-o',
        'url' => admin_url( 'edit.php?post_type=elementor_library#add_new' ),
        'keywords' => [ 'template', 'theme', 'new', 'create' ],
    ];
    return $categories;
}
add_filter( 'elementor/finder/categories', 'add_finder_items' );
```

### Remove Categories / Items

```php
// Remove entire category
function remove_finder_category( array $categories ) {
    unset( $categories['edit'] );
    return $categories;
}
add_filter( 'elementor/finder/categories', 'remove_finder_category' );

// Remove specific item
function remove_finder_item( array $categories ) {
    unset( $categories['create']['items']['post'] );
    return $categories;
}
add_filter( 'elementor/finder/categories', 'remove_finder_item' );
```

### Simple Example: Social Media Links

See [resources/context-menu-finder.md](resources/context-menu-finder.md) for a complete Finder category implementation.

## 5. Context Menu (JavaScript)

### Context Menu Types

1. **Element** - right-click on Section, Column, or Widget
2. **Empty Column** - right-click on empty column area
3. **Add New** - right-click on add new section/template area

### Available Groups by Element Type

| Group | Section | Column | Widget |
|-------|---------|--------|--------|
| `general` | Yes | Yes | Yes |
| `addNew` | No | Yes | No |
| `clipboard` | Yes | Yes | Yes |
| `save` | Yes | No | Yes |
| `tools` | Yes | Yes | Yes |
| `delete` | Yes | Yes | Yes |

### PHP: Enqueue Editor Script

```php
function my_context_menu_scripts() {
    wp_enqueue_script(
        'my-context-menus',
        plugins_url( 'assets/js/context-menus.js', __FILE__ ),
        [],
        '1.0.0',
        false
    );
}
add_action( 'elementor/editor/after_enqueue_scripts', 'my_context_menu_scripts' );
```

### JS: Add New Group with Actions

```js
window.addEventListener( 'elementor/init', () => {
    elementor.hooks.addFilter( 'elements/context-menu/groups', ( customGroups, elementType ) => {
        const newGroup = {
            name: 'my-custom-group',
            actions: [
                {
                    name: 'my-action-1',
                    icon: 'eicon-alert',
                    title: 'My Action',
                    isEnabled: () => true,
                    callback: () => console.log( 'Action triggered' ),
                },
            ],
        };
        if ( 'widget' === elementType ) {
            customGroups.push( newGroup );
        }
        return customGroups;
    } );
} );
```

### JS: Modify Groups and Actions

```js
// Add action to existing group
customGroups.forEach( ( group ) => {
    if ( 'general' === group.name ) { group.actions.push( newAction ); }
} );

// Remove group
const idx = customGroups.findIndex( ( g ) => 'my-group' === g.name );
if ( idx > -1 ) { customGroups.splice( idx, 1 ); }

// Remove action from group
group.actions.splice( group.actions.findIndex( ( a ) => 'my-action' === a.name ), 1 );

// Update action property
group.actions.forEach( ( a ) => { if ( 'my-action' === a.name ) { a.icon = 'eicon-code'; } } );
```

## 6. Hello Elementor Theme

### All Theme Hooks

| Hook (Filter) | Default | Purpose |
|----------------|---------|---------|
| `hello_elementor_post_type_support` | `true` | Register post type support |
| `hello_elementor_add_theme_support` | `true` | Register theme features (title-tag, thumbnails, etc.) |
| `hello_elementor_register_menus` | `true` | Register navigation menus |
| `hello_elementor_add_woocommerce_support` | `true` | Register WooCommerce support |
| `hello_elementor_register_elementor_locations` | `true` | Register Elementor theme locations |
| `hello_elementor_enqueue_style` | `true` | Load style.min.css |
| `hello_elementor_enqueue_theme_style` | `true` | Load theme.min.css |
| `hello_elementor_content_width` | `800` | Content width in pixels |
| `hello_elementor_page_title` | `true` | Show page title |
| `hello_elementor_viewport_content` | `width=device-width, initial-scale=1` | Viewport meta tag |
| `hello_elementor_enable_skip_link` | `true` | Enable accessibility skip link |
| `hello_elementor_skip_link_url` | `#content` | Skip link target URL |

### Disable a Feature

```php
add_filter( 'hello_elementor_register_menus', '__return_false' );
add_filter( 'hello_elementor_enqueue_theme_style', '__return_false' );
add_filter( 'hello_elementor_page_title', '__return_false' );
```

### Custom Content Width

```php
function custom_content_width() {
    return 1024;
}
add_filter( 'hello_elementor_content_width', 'custom_content_width' );
```

### Other Customizations

```php
// Custom viewport
add_filter( 'hello_elementor_viewport_content', fn() => 'width=100vw, height=100vh, user-scalable=no' );

// Custom skip link by page type
add_filter( 'hello_elementor_skip_link_url', function() {
    if ( is_404() ) { return '#404-content'; }
    return is_page() ? '#page-content' : '#main-content';
} );

// Override navigation menus
add_filter( 'hello_elementor_register_menus', '__return_false' );
register_nav_menus( [ 'my-header-menu' => esc_html__( 'Header Menu', 'textdomain' ) ] );

// Remove description meta tag
add_action( 'after_setup_theme', function() {
    remove_action( 'wp_head', 'hello_elementor_add_description_meta_tag' );
} );
```

## 7. Hosting Cache Integration

### Purge Everything

Action hook with no parameters. Clears all page cache.

```php
do_action( 'elementor/hosting/page_cache/purge_everything' );
```

### Allow Page Cache Filter

```php
function custom_page_cache( $allow ) {
    if ( ! $allow ) { return $allow; }
    return is_my_special_page();
}
add_filter( 'elementor/hosting/page_cache/allow_page_cache', 'custom_page_cache', 20 );
```

### Changed URLs Filter

Hook: `elementor/hosting/page_cache/{$content_type}_changed_urls`

`$content_type` values: `post`, `comment`, `woocommerce_product`, etc.

Parameters: `$urls` (array), `$content_id` (int).

```php
function clear_cache_on_product_update( $urls, $product_id ) {
    if ( ! is_array( $urls ) || empty( $urls ) ) { $urls = []; }
    $urls[] = site_url( '/my-path' );
    return $urls;
}
add_filter(
    'elementor/hosting/page_cache/woocommerce_product_changed_urls',
    'clear_cache_on_product_update', 10, 2
);
```

## 8. Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Not checking `function_exists( 'elementor_theme_do_location' )` | Fatal error if Elementor not active | Always wrap in function_exists check with fallback |
| Using `get_type()` value that does not match parent condition name | Sub-condition not displayed | `get_type()` must return the parent condition's `get_name()` value |
| Returning wrong category constant in dynamic tags | Tag not shown for matching controls | Use `\Elementor\Modules\DynamicTags\Module::*_CATEGORY` constants |
| Missing `echo` in dynamic tag `render()` | Empty output | `render()` must `echo`, not `return` |
| Not escaping dynamic tag output | XSS vulnerability | Use `wp_kses_post()`, `esc_html()`, or `esc_url()` |
| Forgetting `elementor/init` listener in context menu JS | Filter runs before Elementor ready | Wrap in `window.addEventListener( 'elementor/init', ... )` |
| Using `elementor/editor/after_enqueue_scripts` for frontend JS | Script only loads in editor | Use `wp_enqueue_scripts` for frontend, editor hook for editor-only |
| Not validating `$allow` parameter in cache filter | Overrides other filters | Check `if ( ! $allow ) { return $allow; }` first |
| Registering location without Elementor Pro active | Theme Builder requires Pro | Check if Elementor Pro is active before registering conditions |
| Calling `register_all_core_location()` and individual locations | Duplicate registrations | Use one or the other, not both |
