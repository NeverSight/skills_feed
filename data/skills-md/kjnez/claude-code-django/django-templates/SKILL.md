---
name: django-templates
description: Django template patterns including inheritance, partials, tags, and filters. Use when working with templates, creating reusable components, or organizing template structure.
---

# Django Template Patterns

## Template Organization

```
templates/
├── base.html              # Root template with common structure
├── partials/              # Reusable fragments (navbar, footer, pagination)
├── components/            # UI components (button, card, modal)
└── <app>/                 # App-specific templates
    ├── list.html          # Full pages extend base.html
    ├── detail.html
    ├── _list.html         # HTMX partials (underscore prefix)
    └── _form.html
```

**Naming conventions:**
- Full pages: `list.html`, `detail.html`, `form.html`
- HTMX partials: `_list.html`, `_card.html` (underscore prefix)
- Shared partials: `partials/_navbar.html`, `partials/_pagination.html`
- Components: `components/_button.html`, `components/_modal.html`

## Template Inheritance

Use three-level inheritance for consistent layouts:

1. **base.html** - Site-wide structure (HTML skeleton, navbar, footer)
2. **Section templates** - Optional intermediate templates for sections with shared elements
3. **Page templates** - Individual pages that extend base or section templates

**Standard blocks to define in base.html:**
- `title` - Page title (use `{{ block.super }}` to append to site name)
- `content` - Main page content
- `extra_css` - Page-specific stylesheets
- `extra_js` - Page-specific scripts

## Partials and Components

**Partials** are template fragments included in other templates. Use for:
- Repeated content (pagination, empty states)
- HTMX responses that replace portions of the page
- Keeping templates DRY

**Components** are self-contained UI elements with configurable behavior. Pass context with:
- `{% include "components/_button.html" with text="Submit" variant="primary" %}`
- Add `only` to isolate context: `{% include "_card.html" with title=post.title only %}`

## Custom Tags and Filters

**When to create custom template tags:**
- `simple_tag` - Return a string value (e.g., active link class, formatted output)
- `inclusion_tag` - Render a template fragment (e.g., pagination component, user avatar)

**When to create custom filters:**
- Transform a single value (e.g., initials from name, percentage calculation)
- Chain with other filters for composable transformations

**Location:** `apps/<app>/templatetags/<app>_tags.py` (create `__init__.py` in templatetags directory)

## Anti-Patterns

**Move logic out of templates:**
- Complex conditionals belong in views or model methods
- Use `user.can_moderate` not `user.role == "admin" or user.role == "moderator"`

**Use URL names, not hardcoded paths:**
- Use `{% url 'posts:detail' pk=post.pk %}` not `/posts/{{ post.id }}/`

**Use CSS classes, not inline styles:**
- Use `class="error-message"` not `style="color: red;"`

**Handle empty states:**
- Always include `{% empty %}` clause in loops that might have no items

## Integration with Other Skills

- **htmx-patterns** - HTMX partial templates and dynamic UI
- **django-forms** - Form rendering and validation patterns
- **pytest-django-patterns** - Testing template rendering
