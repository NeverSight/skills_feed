---
name: php-wordpress
version: "2.0.0"
description: WordPress development mastery - themes, plugins, Gutenberg blocks, and REST API
sasmp_version: "1.3.0"
bonded_agent: 04-php-wordpress
bond_type: PRIMARY_BOND
atomic: true
category: cms
---

# WordPress Development Skill

> Atomic skill for mastering WordPress theme and plugin development

## Overview

Comprehensive skill for building WordPress themes, plugins, and Gutenberg blocks. Covers WordPress 6.x with focus on modern development practices and security.

## Skill Parameters

### Input Validation
```typescript
interface SkillParams {
  topic:
    | "themes"           // Classic, block, FSE
    | "plugins"          // Architecture, hooks, settings
    | "gutenberg"        // Blocks, patterns, InnerBlocks
    | "rest-api"         // Custom endpoints, authentication
    | "security"         // Nonces, sanitization, escaping
    | "woocommerce";     // Store extensions

  level: "beginner" | "intermediate" | "advanced";
  wp_version?: "6.4" | "6.5" | "6.6" | "6.7";
  theme_type?: "classic" | "block" | "hybrid";
}
```

### Validation Rules
```yaml
validation:
  topic:
    required: true
    allowed: [themes, plugins, gutenberg, rest-api, security, woocommerce]
  level:
    required: true
  wp_version:
    default: "6.6"
```

## Learning Modules

### Module 1: Theme Development
```yaml
beginner:
  - Theme structure and files
  - Template hierarchy
  - Enqueuing styles/scripts

intermediate:
  - Custom post types
  - Theme customizer
  - Block theme basics

advanced:
  - Full Site Editing
  - theme.json deep dive
  - Performance optimization
```

### Module 2: Plugin Development
```yaml
beginner:
  - Plugin structure
  - Actions and filters
  - Shortcodes

intermediate:
  - Settings API
  - Custom database tables
  - AJAX handling

advanced:
  - Plugin architecture patterns
  - WP-CLI commands
  - Multisite support
```

### Module 3: Gutenberg Blocks
```yaml
beginner:
  - Block basics and block.json
  - Edit and save functions
  - Block attributes

intermediate:
  - InnerBlocks
  - Block variations
  - Server-side rendering

advanced:
  - Interactivity API
  - Block Bindings
  - Custom block categories
```

## Error Handling & Retry Logic

```yaml
errors:
  HOOK_ERROR:
    code: "WP_001"
    recovery: "Check hook name and timing"

  SECURITY_ERROR:
    code: "WP_002"
    recovery: "Add proper escaping/sanitization"

retry:
  max_attempts: 3
  backoff:
    type: exponential
    initial_delay_ms: 100
```

## Code Examples

### Plugin Header
```php
<?php
/**
 * Plugin Name: My Custom Plugin
 * Description: A custom WordPress plugin
 * Version: 1.0.0
 * Requires PHP: 8.0
 * Author: Developer
 */

declare(strict_types=1);

defined('ABSPATH') || exit;

final class MyCustomPlugin
{
    public function __construct()
    {
        add_action('init', [$this, 'registerPostType']);
        add_action('rest_api_init', [$this, 'registerRoutes']);
    }

    public function registerPostType(): void
    {
        register_post_type('portfolio', [
            'labels' => ['name' => __('Portfolio')],
            'public' => true,
            'show_in_rest' => true,
            'supports' => ['title', 'editor', 'thumbnail'],
        ]);
    }

    public function registerRoutes(): void
    {
        register_rest_route('myplugin/v1', '/items', [
            'methods' => 'GET',
            'callback' => [$this, 'getItems'],
            'permission_callback' => '__return_true',
        ]);
    }

    public function getItems(\WP_REST_Request $request): \WP_REST_Response
    {
        $items = get_posts(['post_type' => 'portfolio']);
        return new \WP_REST_Response($items, 200);
    }
}

new MyCustomPlugin();
```

### Gutenberg Block (block.json)
```json
{
  "$schema": "https://schemas.wp.org/trunk/block.json",
  "apiVersion": 3,
  "name": "myplugin/testimonial",
  "title": "Testimonial",
  "category": "widgets",
  "icon": "format-quote",
  "description": "Display a testimonial",
  "supports": {
    "html": false,
    "align": ["wide", "full"]
  },
  "attributes": {
    "content": { "type": "string" },
    "author": { "type": "string" }
  },
  "textdomain": "myplugin",
  "editorScript": "file:./index.js",
  "style": "file:./style-index.css"
}
```

### Security Best Practices
```php
<?php
// Input sanitization
$title = sanitize_text_field($_POST['title'] ?? '');
$content = wp_kses_post($_POST['content'] ?? '');
$id = absint($_POST['id'] ?? 0);

// Output escaping
echo esc_html($title);
echo esc_attr($attribute);
echo esc_url($url);
echo wp_kses_post($content);

// Nonce verification
if (!wp_verify_nonce($_POST['_wpnonce'], 'my_action')) {
    wp_die('Security check failed');
}

// Capability check
if (!current_user_can('edit_posts')) {
    wp_die('Unauthorized');
}

// Database queries
global $wpdb;
$results = $wpdb->get_results(
    $wpdb->prepare(
        "SELECT * FROM {$wpdb->prefix}custom_table WHERE id = %d",
        $id
    )
);
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Hook not firing | Check hook name spelling and timing |
| Block not appearing | Verify block.json, run npm build |
| REST API 403 | Check permission_callback |
| White screen | Enable WP_DEBUG, check error.log |

## Debug Constants
```php
// wp-config.php
define('WP_DEBUG', true);
define('WP_DEBUG_LOG', true);
define('WP_DEBUG_DISPLAY', false);
define('SCRIPT_DEBUG', true);
```

## Quality Metrics

| Metric | Target |
|--------|--------|
| Security compliance | 100% |
| Hook correctness | 100% |
| WPCS compliance | 100% |

## Usage

```
Skill("php-wordpress", {topic: "gutenberg", level: "intermediate"})
```
