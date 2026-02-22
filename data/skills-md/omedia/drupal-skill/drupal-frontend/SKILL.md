---
name: drupal-frontend
description: Drupal Front End Specialist skill for theme development, Twig templates, and rendering system (Drupal 8-11+). Use when working with Drupal themes, Twig syntax, preprocessing, CSS/JS libraries, or template suggestions.
---

# Drupal Front End Development

## Overview

Enable expert-level Drupal front end development capabilities. Provide comprehensive guidance for theme development, Twig templating, preprocessing, responsive design, and asset management for Drupal 8, 9, 10, and 11+.

## When to Use This Skill

Invoke this skill when working with:
- **Theme development**: Creating or customizing Drupal themes
- **Twig templates**: Writing or modifying .twig template files
- **Preprocessing**: Implementing preprocess functions for templates
- **Template suggestions**: Adding custom template naming patterns
- **CSS/JS libraries**: Managing theme assets and dependencies
- **Responsive design**: Implementing breakpoints and mobile-first design
- **Rendering system**: Understanding Drupal's rendering pipeline
- **Theme hooks**: Implementing theme-related hooks and alterations

## Core Capabilities

### 1. Theme Development

Build complete, standards-compliant Drupal themes with proper structure:

**Quick start workflow:**
1. Use theme template from `assets/theme-template/` as starting point
2. Replace `THEMENAME` with your theme's machine name
3. Replace `THEMELABEL` with human-readable name
4. Customize templates, CSS, JS, and libraries
5. Enable theme and configure via Appearance UI

**Theme components:**
- `.info.yml` - Theme metadata and configuration
- `.libraries.yml` - CSS/JS library definitions
- `.theme` - Preprocess functions and theme logic
- `.breakpoints.yml` - Responsive breakpoints
- `templates/` - Twig template files
- `css/` - Stylesheets
- `js/` - JavaScript files

**Reference documentation:**
- `references/theming.md` - Complete theming guide with examples

### 2. Twig Template System

Master Twig syntax and Drupal-specific extensions:

**Twig fundamentals:**
- `{{ variable }}` - Print variables
- `{% if/for/set %}` - Control structures and logic
- `{# comment #}` - Comments and documentation
- `{{ var|filter }}` - Apply filters to variables
- `{% extends %}` - Template inheritance
- `{% block %}` - Define overridable sections

**Drupal-specific Twig:**
- `{{ 'Text'|t }}` - Translate strings
- `{{ attach_library('theme/library') }}` - Load CSS/JS
- `{{ url('route.name') }}` - Generate URLs
- `{{ path('route.name') }}` - Generate paths
- `{{ file_url('public://image.jpg') }}` - File URLs
- `{{ content|without('field') }}` - Exclude fields

**Common templates:**
- `page.html.twig` - Page layout structure
- `node.html.twig` - Node display
- `block.html.twig` - Block rendering
- `field.html.twig` - Field output
- `views-view.html.twig` - Views output

### 3. Preprocessing Functions

Modify template variables before rendering:

**Preprocess pattern:**
```php
function THEMENAME_preprocess_HOOK(&$variables) {
  // Add or modify variables
  // Access entities, services, configuration
  // Prepare data for templates
}
```

**Common preprocess hooks:**
- `hook_preprocess_page()` - Page-level variables
- `hook_preprocess_node()` - Node-specific data
- `hook_preprocess_block()` - Block modifications
- `hook_preprocess_field()` - Field alterations
- `hook_preprocess_html()` - HTML document

**Best practices:**
- Keep logic in preprocess, markup in templates
- Use dependency injection when possible
- Cache properly with cache contexts/tags
- Document complex preprocessing

### 4. Template Suggestions

Provide specific templates for different contexts:

**Suggestion patterns:**
```
page--front.html.twig                  # Homepage
page--node--{nid}.html.twig            # Specific node
page--node--{type}.html.twig           # Content type
node--{type}--{viewmode}.html.twig     # Type + view mode
block--{plugin-id}.html.twig           # Specific block
field--{entity}--{field}.html.twig     # Specific field
```

**Adding suggestions:**
```php
function THEMENAME_theme_suggestions_HOOK_alter(array &$suggestions, array $variables) {
  // Add custom suggestions
  $suggestions[] = 'custom__suggestion';
}
```

### 5. CSS & JavaScript Management

Organize and load theme assets efficiently:

**Library definition:**
```yaml
# THEMENAME.libraries.yml
global-styling:
  version: 1.0
  css:
    base:
      css/base/reset.css: {}
    theme:
      css/theme/styles.css: {}
  js:
    js/custom.js: {}
  dependencies:
    - core/drupal
```

**Loading libraries:**
- Global: Define in `.info.yml`
- Conditional: Use `attach_library()` in templates
- Preprocessed: Attach in preprocess functions

**Best practices:**
- Separate CSS into layers (base, layout, component, theme)
- Use CSS aggregation in production
- Minimize JavaScript dependencies
- Leverage Drupal's asset library system

### 6. Responsive Design

Implement mobile-first, accessible designs:

**Breakpoints definition:**
```yaml
# THEMENAME.breakpoints.yml
THEMENAME.mobile:
  label: Mobile
  mediaQuery: 'screen and (min-width: 0px)'
  weight: 0

THEMENAME.tablet:
  label: Tablet
  mediaQuery: 'screen and (min-width: 768px)'
  weight: 1

THEMENAME.desktop:
  label: Desktop
  mediaQuery: 'screen and (min-width: 1024px)'
  weight: 2
```

**Mobile-first approach:**
1. Design for smallest screens first
2. Enhance for larger viewports
3. Use responsive images
4. Test across devices
5. Follow accessibility standards (WCAG)

## Development Workflow

### Creating a New Theme

1. **Scaffold the theme:**
   ```bash
   cp -r assets/theme-template/ /path/to/drupal/themes/custom/mytheme/
   cd /path/to/drupal/themes/custom/mytheme/

   # Rename files
   mv THEMENAME.info.yml mytheme.info.yml
   mv THEMENAME.libraries.yml mytheme.libraries.yml
   mv THEMENAME.theme mytheme.theme
   ```

2. **Update theme configuration:**
   - Edit `mytheme.info.yml` - Set name, regions, base theme
   - Edit `mytheme.libraries.yml` - Define CSS/JS libraries
   - Replace `THEMENAME` with your machine name
   - Replace `THEMELABEL` with your label

3. **Enable the theme:**
   ```bash
   ddev drush cr
   # Enable via UI at /admin/appearance or:
   ddev drush config:set system.theme default mytheme -y
   ```

4. **Enable Twig debugging:**
   - Copy `sites/default/default.services.yml` to `sites/default/services.yml`
   - Set `twig.config.debug: true`
   - Set `twig.config.auto_reload: true`
   - Set `twig.config.cache: false`
   - Run `ddev drush cr`

5. **Develop and iterate:**
   - Modify templates in `templates/`
   - Update CSS in `css/`
   - Clear cache frequently: `ddev drush cr`
   - Check browser console for errors

### Standard Development Workflow

1. **Enable development settings** (Twig debug, disable CSS/JS aggregation)
2. **Create/modify templates** based on suggestions from Twig debug
3. **Implement preprocessing** in `.theme` file for complex data manipulation
4. **Add CSS/JS** via libraries system
5. **Test** across browsers and devices
6. **Clear cache** after changes: `ddev drush cr`

### Finding Template Names

With Twig debugging enabled, inspect HTML source:

```html
<!-- FILE NAME SUGGESTIONS:
   * page--node--123.html.twig
   * page--node--article.html.twig
   * page--node.html.twig
   x page.html.twig
-->
```

The `x` indicates the active template. Others are suggestions you can create.

## Common Patterns

### Adding Custom Variables in Preprocess

```php
function mytheme_preprocess_page(&$variables) {
  // Add site slogan
  $variables['site_slogan'] = \Drupal::config('system.site')->get('slogan');

  // Add current user
  $variables['is_logged_in'] = \Drupal::currentUser()->isAuthenticated();

  // Add custom class
  $variables['attributes']['class'][] = 'custom-page-class';
}
```

### Template Inheritance

```twig
{# templates/page--article.html.twig #}
{% extends "page.html.twig" %}

{% block content %}
  <div class="article-wrapper">
    {{ parent() }}
  </div>
{% endblock %}
```

### Conditional Library Loading

```php
function mytheme_preprocess_node(&$variables) {
  if ($variables['node']->bundle() == 'article') {
    $variables['#attached']['library'][] = 'mytheme/article-styles';
  }
}
```

### Accessing Field Values in Twig

```twig
{# Get field value #}
{{ node.field_custom.value }}

{# Check if field has value #}
{% if node.field_image|render %}
  {{ content.field_image }}
{% endif %}

{# Loop through multi-value field #}
{% for item in node.field_tags %}
  {{ item.entity.label }}
{% endfor %}
```

## Best Practices

### Theme Development
1. **Base theme**: Choose appropriate base (Olivero, Claro, or none)
2. **Structure**: Organize CSS logically (base, layout, components, theme)
3. **Naming**: Use BEM or similar CSS methodology
4. **Comments**: Document complex Twig logic and preprocessing
5. **Performance**: Optimize images, minimize CSS/JS, lazy load when possible

### Twig Templates
1. **Logic**: Keep complex logic in preprocess, not templates
2. **Filters**: Use appropriate filters (|t, |clean_class, |safe_join)
3. **Whitespace**: Use {% spaceless %} to control output
4. **Debugging**: Enable Twig debugging during development only
5. **Suggestions**: Use specific templates only when needed

### Preprocessing
1. **Services**: Use dependency injection in theme service subscribers
2. **Caching**: Add proper cache contexts and tags
3. **Performance**: Avoid heavy operations in frequently-called preprocessors
4. **Organization**: Group related preprocessing logically

### CSS & JavaScript
1. **Libraries**: Group related assets into logical libraries
2. **Dependencies**: Declare all library dependencies
3. **Loading**: Load globally only when necessary
4. **Aggregation**: Enable in production for performance

### Accessibility
1. **Semantic HTML**: Use proper elements (header, nav, main, etc.)
2. **ARIA**: Add labels and roles when needed
3. **Keyboard**: Ensure keyboard navigation works
4. **Contrast**: Meet WCAG color contrast requirements
5. **Alt text**: Provide for all images

### Responsive Design
1. **Mobile-first**: Design for small screens, enhance for large
2. **Breakpoints**: Define logical breakpoints
3. **Images**: Use responsive image styles
4. **Testing**: Test across devices and screen sizes
5. **Performance**: Optimize for mobile networks

## Troubleshooting

### Template Changes Not Showing
- Clear cache: `ddev drush cr`
- Verify file location and naming
- Check Twig debug for active template
- Ensure library is properly defined

### CSS/JS Not Loading
- Check library definition in `.libraries.yml`
- Verify file paths are correct
- Ensure library is attached (globally or conditionally)
- Clear cache and check browser console

### Variables Not Available in Template
- Check preprocess function naming
- Verify variables are being set correctly
- Use Twig debugging: `{{ dump() }}`
- Clear cache after preprocessing changes

### Twig Debugging Not Working
- Verify `sites/default/services.yml` exists
- Check `twig.config.debug: true` is set
- Clear cache: `ddev drush cr`
- Check file permissions

## Resources

### Reference Documentation

- **`references/theming.md`** - Comprehensive theming guide
  - Twig syntax and filters
  - Template suggestions
  - Preprocessing patterns
  - Library management
  - Responsive design
  - Best practices

### Asset Templates

- **`assets/theme-template/`** - Complete theme scaffold
  - `.info.yml` with regions and configuration
  - `.libraries.yml` with CSS/JS examples
  - `.theme` with preprocess examples
  - Page template
  - CSS and JS starter files

### Searching References

```bash
# Find specific Twig filter
grep -r "clean_class" references/

# Find preprocessing examples
grep -r "preprocess_node" references/

# Find library patterns
grep -r "libraries.yml" references/
```

## Version Compatibility

### Drupal 8 vs 9 vs 10 vs 11
- **Twig syntax**: Consistent across all versions
- **Base themes**: Some legacy themes removed in 10+
- **Libraries**: Same structure across versions
- **jQuery**: Drupal 9+ doesn't load jQuery by default
- **Claro**: Admin theme standard in 9+
- **Olivero**: Frontend theme standard in 10+

### Migration Notes
- When upgrading, check for deprecated base themes
- Review jQuery dependencies
- Test with current Twig version
- Check for removed core templates

## See Also

- **drupal-backend** - Module development, hooks, APIs
- **drupal-tooling** - DDEV and Drush development tools
- [Drupal Theming Guide](https://www.drupal.org/docs/theming-drupal) - Official documentation
- [Twig Documentation](https://twig.symfony.com/doc/) - Twig syntax reference
