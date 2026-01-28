---
name: wp-theme-development
description: WordPress theme development best practices and standards. Use when building new themes, creating custom templates, implementing theme features, working with template hierarchy, customizer options, or FSE block themes, or when user mentions "theme development", "child theme", "template hierarchy", "theme.json", "customizer", "template parts", "block theme", "classic theme", or "theme standards".
---

# WordPress Theme Development Skill

## Overview

Comprehensive guide for developing WordPress themes following best practices. Covers both classic PHP-based themes and modern FSE (Full Site Editing) block themes. **Core principle:** Build accessible, performant, and WordPress-standards-compliant themes.

## When to Use

**Use when:**
- Building new WordPress themes (classic or block)
- Creating child themes
- Implementing template hierarchy
- Adding customizer options
- Setting up FSE templates and template parts
- Troubleshooting theme issues

**Don't use for:**
- Plugin development (use wp-plugin-development)
- Block development specifically (use wp-gutenberg-blocks)
- Security auditing (use wp-security-review)

## Theme Types Overview

| Type | Description | Key Files |
|------|-------------|-----------|
| **Classic Theme** | PHP templates, customizer | style.css, functions.php, templates/*.php |
| **Block Theme** | FSE, theme.json based | style.css, theme.json, templates/*.html, parts/*.html |
| **Hybrid Theme** | Mix of both approaches | All of the above |
| **Child Theme** | Extends parent theme | style.css, functions.php |

## Classic Theme Structure

```
theme-name/
├── assets/
│   ├── css/
│   │   ├── style.css           # Compiled styles
│   │   └── editor-style.css    # Editor styles
│   ├── js/
│   │   ├── main.js             # Main scripts
│   │   └── navigation.js       # Nav scripts
│   ├── images/
│   └── fonts/
├── inc/
│   ├── customizer.php          # Customizer settings
│   ├── template-functions.php  # Template helpers
│   ├── template-tags.php       # Template tags
│   ├── theme-setup.php         # Theme setup
│   └── walker-nav.php          # Custom walkers
├── template-parts/
│   ├── header/
│   │   ├── site-branding.php
│   │   └── site-navigation.php
│   ├── footer/
│   │   ├── footer-widgets.php
│   │   └── site-info.php
│   ├── content/
│   │   ├── content.php
│   │   ├── content-page.php
│   │   ├── content-single.php
│   │   └── content-none.php
│   └── components/
│       ├── post-meta.php
│       └── pagination.php
├── languages/
│   └── theme-name.pot
├── 404.php
├── archive.php
├── comments.php
├── footer.php
├── front-page.php
├── functions.php
├── header.php
├── index.php
├── page.php
├── screenshot.png              # 1200x900px
├── search.php
├── sidebar.php
├── single.php
├── style.css
└── readme.txt
```

## Block Theme Structure

```
theme-name/
├── assets/
│   ├── css/
│   │   └── custom.css
│   ├── js/
│   └── fonts/
├── parts/
│   ├── header.html
│   ├── footer.html
│   └── sidebar.html
├── patterns/
│   ├── hero.php
│   ├── featured-posts.php
│   └── call-to-action.php
├── styles/
│   ├── blue.json              # Color variations
│   └── dark.json
├── templates/
│   ├── 404.html
│   ├── archive.html
│   ├── front-page.html
│   ├── home.html
│   ├── index.html
│   ├── page.html
│   ├── search.html
│   └── single.html
├── functions.php
├── screenshot.png
├── style.css
├── theme.json
└── readme.txt
```

## Required Files

### style.css Header

```css
/*
Theme Name:        Theme Name
Theme URI:         https://example.com/theme
Author:            Your Agency
Author URI:        https://youragency.com
Description:       A custom WordPress theme with modern features.
Version:           1.0.0
Requires at least: 6.0
Tested up to:      6.5
Requires PHP:      8.0
License:           GPL v2 or later
License URI:       https://www.gnu.org/licenses/gpl-2.0.html
Text Domain:       theme-name
Tags:              block-patterns, block-styles, custom-colors, custom-logo, editor-style, full-site-editing, wide-blocks

Theme Name is based on starter theme components.
*/
```

### functions.php Setup

```php
<?php
/**
 * Theme functions and definitions.
 *
 * @package Theme_Name
 */

if ( ! defined( 'THEME_NAME_VERSION' ) ) {
    define( 'THEME_NAME_VERSION', '1.0.0' );
}

/**
 * Theme setup.
 */
function theme_name_setup() {
    // Make theme available for translation.
    load_theme_textdomain( 'theme-name', get_template_directory() . '/languages' );

    // Add default posts and comments RSS feed links.
    add_theme_support( 'automatic-feed-links' );

    // Let WordPress manage the document title.
    add_theme_support( 'title-tag' );

    // Enable support for Post Thumbnails.
    add_theme_support( 'post-thumbnails' );
    set_post_thumbnail_size( 1200, 630, true );

    // Add custom image sizes.
    add_image_size( 'theme-name-featured', 1920, 1080, true );
    add_image_size( 'theme-name-card', 600, 400, true );

    // Register navigation menus.
    register_nav_menus(
        array(
            'primary'   => esc_html__( 'Primary Menu', 'theme-name' ),
            'footer'    => esc_html__( 'Footer Menu', 'theme-name' ),
            'social'    => esc_html__( 'Social Menu', 'theme-name' ),
        )
    );

    // HTML5 markup support.
    add_theme_support(
        'html5',
        array(
            'search-form',
            'comment-form',
            'comment-list',
            'gallery',
            'caption',
            'style',
            'script',
            'navigation-widgets',
        )
    );

    // Custom logo support.
    add_theme_support(
        'custom-logo',
        array(
            'height'      => 100,
            'width'       => 400,
            'flex-width'  => true,
            'flex-height' => true,
        )
    );

    // Custom background support.
    add_theme_support(
        'custom-background',
        array(
            'default-color' => 'ffffff',
            'default-image' => '',
        )
    );

    // Block editor support.
    add_theme_support( 'wp-block-styles' );
    add_theme_support( 'align-wide' );
    add_theme_support( 'responsive-embeds' );

    // Editor color palette.
    add_theme_support(
        'editor-color-palette',
        array(
            array(
                'name'  => esc_html__( 'Primary', 'theme-name' ),
                'slug'  => 'primary',
                'color' => '#0066cc',
            ),
            array(
                'name'  => esc_html__( 'Secondary', 'theme-name' ),
                'slug'  => 'secondary',
                'color' => '#6c757d',
            ),
            array(
                'name'  => esc_html__( 'Dark', 'theme-name' ),
                'slug'  => 'dark',
                'color' => '#212529',
            ),
            array(
                'name'  => esc_html__( 'Light', 'theme-name' ),
                'slug'  => 'light',
                'color' => '#f8f9fa',
            ),
        )
    );

    // Editor font sizes.
    add_theme_support(
        'editor-font-sizes',
        array(
            array(
                'name' => esc_html__( 'Small', 'theme-name' ),
                'slug' => 'small',
                'size' => 14,
            ),
            array(
                'name' => esc_html__( 'Normal', 'theme-name' ),
                'slug' => 'normal',
                'size' => 16,
            ),
            array(
                'name' => esc_html__( 'Large', 'theme-name' ),
                'slug' => 'large',
                'size' => 20,
            ),
            array(
                'name' => esc_html__( 'Huge', 'theme-name' ),
                'slug' => 'huge',
                'size' => 32,
            ),
        )
    );
}
add_action( 'after_setup_theme', 'theme_name_setup' );

/**
 * Set content width.
 */
function theme_name_content_width() {
    $GLOBALS['content_width'] = apply_filters( 'theme_name_content_width', 1200 );
}
add_action( 'after_setup_theme', 'theme_name_content_width', 0 );

/**
 * Register widget areas.
 */
function theme_name_widgets_init() {
    register_sidebar(
        array(
            'name'          => esc_html__( 'Sidebar', 'theme-name' ),
            'id'            => 'sidebar-1',
            'description'   => esc_html__( 'Add widgets here.', 'theme-name' ),
            'before_widget' => '<section id="%1$s" class="widget %2$s">',
            'after_widget'  => '</section>',
            'before_title'  => '<h2 class="widget-title">',
            'after_title'   => '</h2>',
        )
    );

    register_sidebar(
        array(
            'name'          => esc_html__( 'Footer', 'theme-name' ),
            'id'            => 'sidebar-footer',
            'description'   => esc_html__( 'Footer widget area.', 'theme-name' ),
            'before_widget' => '<div id="%1$s" class="widget %2$s">',
            'after_widget'  => '</div>',
            'before_title'  => '<h3 class="widget-title">',
            'after_title'   => '</h3>',
        )
    );
}
add_action( 'widgets_init', 'theme_name_widgets_init' );

/**
 * Enqueue scripts and styles.
 */
function theme_name_scripts() {
    // Main stylesheet.
    wp_enqueue_style(
        'theme-name-style',
        get_stylesheet_uri(),
        array(),
        THEME_NAME_VERSION
    );

    // Additional styles.
    wp_enqueue_style(
        'theme-name-main',
        get_template_directory_uri() . '/assets/css/main.css',
        array( 'theme-name-style' ),
        THEME_NAME_VERSION
    );

    // Main script.
    wp_enqueue_script(
        'theme-name-script',
        get_template_directory_uri() . '/assets/js/main.js',
        array(),
        THEME_NAME_VERSION,
        array(
            'in_footer' => true,
            'strategy'  => 'defer',
        )
    );

    // Navigation script.
    wp_enqueue_script(
        'theme-name-navigation',
        get_template_directory_uri() . '/assets/js/navigation.js',
        array(),
        THEME_NAME_VERSION,
        array(
            'in_footer' => true,
            'strategy'  => 'defer',
        )
    );

    // Localize script data.
    wp_localize_script(
        'theme-name-script',
        'themeNameData',
        array(
            'ajaxUrl' => admin_url( 'admin-ajax.php' ),
            'nonce'   => wp_create_nonce( 'theme_name_nonce' ),
        )
    );

    // Comment reply script.
    if ( is_singular() && comments_open() && get_option( 'thread_comments' ) ) {
        wp_enqueue_script( 'comment-reply' );
    }
}
add_action( 'wp_enqueue_scripts', 'theme_name_scripts' );

/**
 * Enqueue editor styles.
 */
function theme_name_editor_styles() {
    add_editor_style(
        array(
            'assets/css/editor-style.css',
        )
    );
}
add_action( 'after_setup_theme', 'theme_name_editor_styles' );

/**
 * Include required files.
 */
require get_template_directory() . '/inc/template-tags.php';
require get_template_directory() . '/inc/template-functions.php';
require get_template_directory() . '/inc/customizer.php';
```

## Template Hierarchy

### Template Selection Priority

```
# Single Post
single-{post-type}-{slug}.php
single-{post-type}.php
single.php
singular.php
index.php

# Page
page-{slug}.php
page-{id}.php
page.php
singular.php
index.php

# Category Archive
category-{slug}.php
category-{id}.php
category.php
archive.php
index.php

# Custom Post Type Archive
archive-{post-type}.php
archive.php
index.php

# Taxonomy Archive
taxonomy-{taxonomy}-{term}.php
taxonomy-{taxonomy}.php
taxonomy.php
archive.php
index.php

# Author Archive
author-{nicename}.php
author-{id}.php
author.php
archive.php
index.php

# Date Archive
date.php
archive.php
index.php

# Search Results
search.php
index.php

# 404 Error
404.php
index.php

# Front Page
front-page.php
home.php (if showing posts)
page.php (if showing page)
index.php

# Blog Home
home.php
index.php
```

### Template Parts Usage

```php
<?php
// In single.php.
get_header();

while ( have_posts() ) :
    the_post();

    // Load template part based on post format.
    get_template_part( 'template-parts/content/content', get_post_format() );

    // Previous/next navigation.
    get_template_part( 'template-parts/components/post-navigation' );

    // Comments.
    if ( comments_open() || get_comments_number() ) {
        comments_template();
    }

endwhile;

get_sidebar();
get_footer();
```

```php
<?php
// template-parts/content/content-single.php.
?>
<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
    <header class="entry-header">
        <?php the_title( '<h1 class="entry-title">', '</h1>' ); ?>

        <div class="entry-meta">
            <?php theme_name_posted_on(); ?>
            <?php theme_name_posted_by(); ?>
        </div>
    </header>

    <?php theme_name_post_thumbnail(); ?>

    <div class="entry-content">
        <?php
        the_content();

        wp_link_pages(
            array(
                'before' => '<div class="page-links">' . esc_html__( 'Pages:', 'theme-name' ),
                'after'  => '</div>',
            )
        );
        ?>
    </div>

    <footer class="entry-footer">
        <?php theme_name_entry_footer(); ?>
    </footer>
</article>
```

## Template Tags

### Custom Template Tags (inc/template-tags.php)

```php
<?php
/**
 * Custom template tags for this theme.
 *
 * @package Theme_Name
 */

if ( ! function_exists( 'theme_name_posted_on' ) ) :
    /**
     * Prints HTML with meta information for the current post-date/time.
     */
    function theme_name_posted_on() {
        $time_string = '<time class="entry-date published updated" datetime="%1$s">%2$s</time>';

        if ( get_the_time( 'U' ) !== get_the_modified_time( 'U' ) ) {
            $time_string = '<time class="entry-date published" datetime="%1$s">%2$s</time><time class="updated" datetime="%3$s">%4$s</time>';
        }

        $time_string = sprintf(
            $time_string,
            esc_attr( get_the_date( DATE_W3C ) ),
            esc_html( get_the_date() ),
            esc_attr( get_the_modified_date( DATE_W3C ) ),
            esc_html( get_the_modified_date() )
        );

        printf(
            '<span class="posted-on">%s</span>',
            '<a href="' . esc_url( get_permalink() ) . '" rel="bookmark">' . $time_string . '</a>'
        );
    }
endif;

if ( ! function_exists( 'theme_name_posted_by' ) ) :
    /**
     * Prints HTML with meta information for the current author.
     */
    function theme_name_posted_by() {
        printf(
            '<span class="byline">%s</span>',
            '<span class="author vcard"><a class="url fn n" href="' . esc_url( get_author_posts_url( get_the_author_meta( 'ID' ) ) ) . '">' . esc_html( get_the_author() ) . '</a></span>'
        );
    }
endif;

if ( ! function_exists( 'theme_name_post_thumbnail' ) ) :
    /**
     * Displays an optional post thumbnail.
     */
    function theme_name_post_thumbnail() {
        if ( post_password_required() || is_attachment() || ! has_post_thumbnail() ) {
            return;
        }

        if ( is_singular() ) :
            ?>
            <div class="post-thumbnail">
                <?php the_post_thumbnail( 'theme-name-featured' ); ?>
            </div>
            <?php
        else :
            ?>
            <a class="post-thumbnail" href="<?php the_permalink(); ?>" aria-hidden="true" tabindex="-1">
                <?php
                the_post_thumbnail(
                    'theme-name-card',
                    array(
                        'alt' => the_title_attribute( array( 'echo' => false ) ),
                    )
                );
                ?>
            </a>
            <?php
        endif;
    }
endif;

if ( ! function_exists( 'theme_name_entry_footer' ) ) :
    /**
     * Prints HTML with meta information for the categories, tags and comments.
     */
    function theme_name_entry_footer() {
        // Hide category and tag text for pages.
        if ( 'post' === get_post_type() ) {
            $categories_list = get_the_category_list( esc_html__( ', ', 'theme-name' ) );
            if ( $categories_list ) {
                printf(
                    '<span class="cat-links">%s%s</span>',
                    esc_html__( 'Posted in ', 'theme-name' ),
                    $categories_list
                );
            }

            $tags_list = get_the_tag_list( '', esc_html__( ', ', 'theme-name' ) );
            if ( $tags_list ) {
                printf(
                    '<span class="tags-links">%s%s</span>',
                    esc_html__( 'Tagged ', 'theme-name' ),
                    $tags_list
                );
            }
        }

        if ( ! is_single() && ! post_password_required() && ( comments_open() || get_comments_number() ) ) {
            echo '<span class="comments-link">';
            comments_popup_link(
                sprintf(
                    /* translators: %s: post title */
                    esc_html__( 'Leave a Comment on %s', 'theme-name' ),
                    '<span class="screen-reader-text">' . get_the_title() . '</span>'
                )
            );
            echo '</span>';
        }

        edit_post_link(
            sprintf(
                /* translators: %s: Name of current post */
                esc_html__( 'Edit %s', 'theme-name' ),
                '<span class="screen-reader-text">' . get_the_title() . '</span>'
            ),
            '<span class="edit-link">',
            '</span>'
        );
    }
endif;
```

## Customizer Implementation

### Customizer Settings (inc/customizer.php)

```php
<?php
/**
 * Theme Customizer settings.
 *
 * @package Theme_Name
 */

/**
 * Register customizer settings.
 *
 * @param WP_Customize_Manager $wp_customize Theme Customizer object.
 */
function theme_name_customize_register( $wp_customize ) {
    // Theme Options Panel.
    $wp_customize->add_panel(
        'theme_name_options',
        array(
            'title'       => esc_html__( 'Theme Options', 'theme-name' ),
            'description' => esc_html__( 'Configure theme settings.', 'theme-name' ),
            'priority'    => 130,
        )
    );

    // Header Section.
    $wp_customize->add_section(
        'theme_name_header',
        array(
            'title'    => esc_html__( 'Header', 'theme-name' ),
            'panel'    => 'theme_name_options',
            'priority' => 10,
        )
    );

    // Header Layout Setting.
    $wp_customize->add_setting(
        'header_layout',
        array(
            'default'           => 'default',
            'sanitize_callback' => 'theme_name_sanitize_select',
            'transport'         => 'refresh',
        )
    );

    $wp_customize->add_control(
        'header_layout',
        array(
            'label'   => esc_html__( 'Header Layout', 'theme-name' ),
            'section' => 'theme_name_header',
            'type'    => 'select',
            'choices' => array(
                'default'  => esc_html__( 'Default', 'theme-name' ),
                'centered' => esc_html__( 'Centered', 'theme-name' ),
                'minimal'  => esc_html__( 'Minimal', 'theme-name' ),
            ),
        )
    );

    // Sticky Header Toggle.
    $wp_customize->add_setting(
        'sticky_header',
        array(
            'default'           => false,
            'sanitize_callback' => 'theme_name_sanitize_checkbox',
            'transport'         => 'refresh',
        )
    );

    $wp_customize->add_control(
        'sticky_header',
        array(
            'label'   => esc_html__( 'Enable Sticky Header', 'theme-name' ),
            'section' => 'theme_name_header',
            'type'    => 'checkbox',
        )
    );

    // Footer Section.
    $wp_customize->add_section(
        'theme_name_footer',
        array(
            'title'    => esc_html__( 'Footer', 'theme-name' ),
            'panel'    => 'theme_name_options',
            'priority' => 20,
        )
    );

    // Footer Copyright Text.
    $wp_customize->add_setting(
        'footer_copyright',
        array(
            'default'           => '',
            'sanitize_callback' => 'wp_kses_post',
            'transport'         => 'postMessage',
        )
    );

    $wp_customize->add_control(
        'footer_copyright',
        array(
            'label'       => esc_html__( 'Copyright Text', 'theme-name' ),
            'description' => esc_html__( 'Enter custom copyright text for the footer.', 'theme-name' ),
            'section'     => 'theme_name_footer',
            'type'        => 'textarea',
        )
    );

    // Selective refresh for footer copyright.
    $wp_customize->selective_refresh->add_partial(
        'footer_copyright',
        array(
            'selector'        => '.site-info',
            'render_callback' => 'theme_name_customize_partial_copyright',
        )
    );

    // Typography Section.
    $wp_customize->add_section(
        'theme_name_typography',
        array(
            'title'    => esc_html__( 'Typography', 'theme-name' ),
            'panel'    => 'theme_name_options',
            'priority' => 30,
        )
    );

    // Body Font Size.
    $wp_customize->add_setting(
        'body_font_size',
        array(
            'default'           => 16,
            'sanitize_callback' => 'absint',
            'transport'         => 'postMessage',
        )
    );

    $wp_customize->add_control(
        'body_font_size',
        array(
            'label'       => esc_html__( 'Body Font Size (px)', 'theme-name' ),
            'section'     => 'theme_name_typography',
            'type'        => 'number',
            'input_attrs' => array(
                'min'  => 12,
                'max'  => 24,
                'step' => 1,
            ),
        )
    );
}
add_action( 'customize_register', 'theme_name_customize_register' );

/**
 * Sanitize select input.
 *
 * @param string $input   Input value.
 * @param object $setting Setting object.
 * @return string Sanitized value.
 */
function theme_name_sanitize_select( $input, $setting ) {
    $input   = sanitize_key( $input );
    $choices = $setting->manager->get_control( $setting->id )->choices;
    return ( array_key_exists( $input, $choices ) ? $input : $setting->default );
}

/**
 * Sanitize checkbox.
 *
 * @param bool $checked Whether checked.
 * @return bool
 */
function theme_name_sanitize_checkbox( $checked ) {
    return ( ( isset( $checked ) && true === $checked ) ? true : false );
}

/**
 * Render copyright partial.
 */
function theme_name_customize_partial_copyright() {
    $copyright = get_theme_mod( 'footer_copyright' );
    if ( $copyright ) {
        echo wp_kses_post( $copyright );
    } else {
        printf(
            /* translators: %s: Site name */
            esc_html__( '&copy; %1$s %2$s', 'theme-name' ),
            esc_html( gmdate( 'Y' ) ),
            esc_html( get_bloginfo( 'name' ) )
        );
    }
}

/**
 * Enqueue customizer preview script.
 */
function theme_name_customize_preview_js() {
    wp_enqueue_script(
        'theme-name-customizer',
        get_template_directory_uri() . '/assets/js/customizer.js',
        array( 'customize-preview' ),
        THEME_NAME_VERSION,
        true
    );
}
add_action( 'customize_preview_init', 'theme_name_customize_preview_js' );

/**
 * Output customizer CSS.
 */
function theme_name_customizer_css() {
    $body_font_size = get_theme_mod( 'body_font_size', 16 );

    $css = "
        body {
            font-size: {$body_font_size}px;
        }
    ";

    wp_add_inline_style( 'theme-name-style', $css );
}
add_action( 'wp_enqueue_scripts', 'theme_name_customizer_css' );
```

## Child Theme Setup

### style.css

```css
/*
Theme Name:   Theme Name Child
Theme URI:    https://example.com/theme-child
Description:  Child theme for Theme Name
Author:       Your Agency
Author URI:   https://youragency.com
Template:     theme-name
Version:      1.0.0
License:      GPL v2 or later
License URI:  https://www.gnu.org/licenses/gpl-2.0.html
Text Domain:  theme-name-child
*/

/* Custom styles below */
```

### functions.php

```php
<?php
/**
 * Child theme functions.
 *
 * @package Theme_Name_Child
 */

/**
 * Enqueue parent and child theme styles.
 */
function theme_name_child_enqueue_styles() {
    $parent_style = 'theme-name-style';

    // Parent theme stylesheet.
    wp_enqueue_style(
        $parent_style,
        get_template_directory_uri() . '/style.css',
        array(),
        wp_get_theme( 'theme-name' )->get( 'Version' )
    );

    // Child theme stylesheet.
    wp_enqueue_style(
        'theme-name-child-style',
        get_stylesheet_uri(),
        array( $parent_style ),
        wp_get_theme()->get( 'Version' )
    );
}
add_action( 'wp_enqueue_scripts', 'theme_name_child_enqueue_styles' );
```

## Accessibility Requirements

### Skip Link

```php
<!-- In header.php, right after <body> -->
<a class="skip-link screen-reader-text" href="#primary">
    <?php esc_html_e( 'Skip to content', 'theme-name' ); ?>
</a>
```

```css
/* Skip link styles */
.skip-link {
    position: absolute;
    left: -9999rem;
    top: 2.5rem;
    z-index: 999999999;
    padding: 0.5rem 1rem;
    background-color: #000;
    color: #fff;
}

.skip-link:focus {
    left: 1rem;
}
```

### Accessible Navigation

```php
<nav id="site-navigation" class="main-navigation" aria-label="<?php esc_attr_e( 'Primary Navigation', 'theme-name' ); ?>">
    <button class="menu-toggle" aria-controls="primary-menu" aria-expanded="false">
        <span class="screen-reader-text"><?php esc_html_e( 'Menu', 'theme-name' ); ?></span>
        <span class="hamburger"></span>
    </button>
    <?php
    wp_nav_menu(
        array(
            'theme_location' => 'primary',
            'menu_id'        => 'primary-menu',
            'container'      => false,
        )
    );
    ?>
</nav>
```

### Screen Reader Text

```css
.screen-reader-text {
    border: 0;
    clip: rect(1px, 1px, 1px, 1px);
    clip-path: inset(50%);
    height: 1px;
    margin: -1px;
    overflow: hidden;
    padding: 0;
    position: absolute;
    width: 1px;
    word-wrap: normal !important;
}

.screen-reader-text:focus {
    background-color: #f1f1f1;
    border-radius: 3px;
    box-shadow: 0 0 2px 2px rgba(0, 0, 0, 0.6);
    clip: auto !important;
    clip-path: none;
    color: #21759b;
    display: block;
    font-size: 0.875rem;
    font-weight: 700;
    height: auto;
    left: 5px;
    line-height: normal;
    padding: 15px 23px 14px;
    text-decoration: none;
    top: 5px;
    width: auto;
    z-index: 100000;
}
```

## Security Best Practices

```php
// ❌ BAD: Unescaped output.
echo $title;
echo get_the_title();

// ✅ GOOD: Always escape output.
echo esc_html( $title );
echo esc_html( get_the_title() );

// ❌ BAD: Unescaped URLs.
<a href="<?php echo $url; ?>">

// ✅ GOOD: Escape URLs.
<a href="<?php echo esc_url( $url ); ?>">

// ❌ BAD: Unescaped attributes.
<input value="<?php echo $value; ?>">

// ✅ GOOD: Escape attributes.
<input value="<?php echo esc_attr( $value ); ?>">

// ❌ BAD: Using include with user input.
include $_GET['template'];

// ✅ GOOD: Validate template names.
$allowed = array( 'header', 'footer', 'sidebar' );
$template = sanitize_file_name( $_GET['template'] );
if ( in_array( $template, $allowed, true ) ) {
    get_template_part( $template );
}
```

## Performance Optimization

### Lazy Load Images

```php
// WordPress 5.5+ handles lazy loading automatically.
// For older versions or custom implementation:
function theme_name_lazy_load_images( $content ) {
    return str_replace( '<img ', '<img loading="lazy" ', $content );
}
add_filter( 'the_content', 'theme_name_lazy_load_images' );
```

### Defer Non-Critical CSS

```php
function theme_name_defer_styles( $html, $handle ) {
    $defer_handles = array( 'theme-name-print', 'theme-name-animations' );

    if ( in_array( $handle, $defer_handles, true ) ) {
        $html = str_replace(
            "rel='stylesheet'",
            "rel='preload' as='style' onload=\"this.rel='stylesheet'\"",
            $html
        );
    }

    return $html;
}
add_filter( 'style_loader_tag', 'theme_name_defer_styles', 10, 2 );
```

### Preload Key Assets

```php
function theme_name_preload_assets() {
    // Preload main font.
    echo '<link rel="preload" href="' . esc_url( get_template_directory_uri() ) . '/assets/fonts/main.woff2" as="font" type="font/woff2" crossorigin>';
}
add_action( 'wp_head', 'theme_name_preload_assets', 1 );
```

## Theme Check Compliance

Before release, ensure:

- [ ] Passes Theme Check plugin (no errors)
- [ ] Passes Theme Sniffer (PHP coding standards)
- [ ] All strings are translation-ready
- [ ] Uses proper prefixing for functions, classes, options
- [ ] Includes screenshot.png (1200x900px)
- [ ] Includes readme.txt with proper format
- [ ] No bundled plugins (recommend instead)
- [ ] GPL-compatible license
- [ ] Escapes all output
- [ ] Sanitizes all input
- [ ] Uses proper enqueue functions
- [ ] Supports core WordPress features

## Severity Definitions

| Severity | Description |
|----------|-------------|
| **Critical** | Theme won't work, security vulnerability |
| **Warning** | Theme Check failure, accessibility issue |
| **Info** | Best practice suggestion, optimization |
