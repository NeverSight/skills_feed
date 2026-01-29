---
name: odoo-upgrade
description: Comprehensive Odoo ERP upgrade assistant for migrating modules between Odoo versions (14-19). Handles XML views, Python API changes, JavaScript/OWL components, theme SCSS variables, and manifest updates. Use when user asks to upgrade Odoo modules, fix version compatibility issues, migrate themes between versions, or resolve Odoo 17/18/19 migration errors. Specializes in frontend RPC service migrations, view XML transformations, and theme variable restructuring.
---

# Odoo Upgrade Assistant

A comprehensive skill for upgrading Odoo modules between versions, with extensive pattern recognition and automated fixes for common migration issues.

## When to Use This Skill

Activate this skill when:
- User requests upgrading Odoo modules between versions (14→19)
- Fixing Odoo version compatibility errors
- Migrating themes or custom modules
- Resolving RPC service errors in frontend components
- Converting XML views for newer Odoo versions
- Updating SCSS variables for Odoo 19 themes

## Upgrade Workflow

### 1. Initial Analysis
```bash
# Analyze source module structure
- Check __manifest__.py version
- Identify module dependencies
- List all file types (XML, Python, JS, SCSS)
- Create backup before changes
```

### 2. Manifest Updates
- Update version number to target format (e.g., "19.0.1.0.0")
- Add missing 'license' key (default: 'LGPL-3')
- Declare external dependencies
- Update category if needed

### 3. XML/View Transformations

#### Search Views (Odoo 19)
```xml
<!-- BEFORE (Invalid in Odoo 19) -->
<search>
    <group expand="0" string="Group By">
        <filter name="type" string="Type"/>
    </group>
</search>

<!-- AFTER (Valid in Odoo 19) -->
<search>
    <filter name="type" string="Type"/>
</search>
```

#### Tree to List Views
```xml
<!-- BEFORE -->
<tree string="Title" edit="1" editable="top">

<!-- AFTER -->
<list string="Title" editable="top">
```

#### Kanban Templates (Odoo 19)
```xml
<!-- BEFORE -->
<t t-name="kanban-box">

<!-- AFTER -->
<t t-name="card">
```

#### Form View Context (Odoo 19)
```xml
<!-- BEFORE -->
context="{'search_default_type_id': active_id}"

<!-- AFTER -->
context="{'search_default_type_id': id}"
```

#### Cron Jobs (Odoo 19)
Remove `numbercall` field - no longer supported:
```xml
<!-- Remove this line -->
<field name="numbercall">-1</field>
```

### 4. Python API Migrations

#### Slug Function (Odoo 18+)
```python
# Add compatibility wrapper
from odoo.http import request

def slug(value):
    """Compatibility wrapper for slug function"""
    return request.env['ir.http']._slug(value)

def unslug(value):
    """Compatibility wrapper for unslug function"""
    return request.env['ir.http']._unslug(value)
```

#### URL For Function (Odoo 19)
```python
# BEFORE
from odoo.addons.http_routing.models.ir_http import url_for
url = url_for('/path')

# AFTER
url = self.env['ir.http']._url_for('/path')
```

### 5. JavaScript/OWL Frontend Migrations

#### RPC Service Replacement (Odoo 19)
The RPC service is NOT available in Odoo 19 frontend/public components.

```javascript
/** @odoo-module **/

// BEFORE (Odoo 17)
import {useService} from "@web/core/utils/hooks";

export class MyComponent extends Component {
    setup() {
        this.rpc = useService("rpc");
    }

    async fetchData() {
        const data = await this.rpc("/api/endpoint", params);
    }
}

// AFTER (Odoo 19)
export class MyComponent extends Component {
    setup() {
        // RPC service removed - using fetch instead
    }

    async _jsonRpc(endpoint, params = {}) {
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Csrf-Token': document.querySelector('meta[name="csrf-token"]')?.content || '',
                },
                body: JSON.stringify({
                    jsonrpc: "2.0",
                    method: "call",
                    params: params,
                    id: Math.floor(Math.random() * 1000000)
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            if (data.error) {
                throw new Error(data.error.message || 'RPC call failed');
            }
            return data.result;
        } catch (error) {
            console.error('JSON-RPC call failed:', error);
            throw error;
        }
    }

    async fetchData() {
        const data = await this._jsonRpc("/api/endpoint", params);
    }
}
```

### 6. Theme SCSS Variables (Odoo 19)

#### Proper Structure
```scss
// ===================================================================
// Theme Name - Primary Variables
// ===================================================================

// Typography Hierarchy
$o-theme-h1-font-size-multiplier: (64 / 16);
$o-theme-headings-font-weight: 700;  // NOT $headings-font-weight

// Website Values Palette
$o-website-values-palettes: (
    (
        'color-palettes-name': 'my_theme',
        'font': 'Inter',
        'headings-font': 'Inter',
        'btn-padding-y': 1rem,  // Use rem not px
        'btn-padding-x': 2rem,
    ),
);

// Color Palette with menu/footer assignments
$o-color-palettes: map-merge($o-color-palettes, (
    'my_theme': (
        'o-color-1': #124F81,
        'o-color-2': #B1025D,
        'o-color-3': #f8fafc,
        'o-color-4': #ffffff,
        'o-color-5': #1e293b,
        'menu': 1,        // IMPORTANT: Specify which color for menu
        'footer': 4,      // IMPORTANT: Specify which color for footer
        'copyright': 5,   // IMPORTANT: Specify which color for copyright
    ),
));

// Font Configuration (use map-merge!)
$o-theme-font-configs: map-merge($o-theme-font-configs, (
    'Inter': (
        'family': ('Inter', sans-serif),
        'url': 'Inter:300,400,500,600,700&display=swap',
        'properties': (  // IMPORTANT: Add properties section
            'base': (
                'font-size-base': 1rem,
                'line-height-base': 1.6,
            ),
        )
    ),
));
```

### 7. Theme Snippet System (Odoo 19)

Remove incompatible `website.snippet_options` inheritance:
```xml
<!-- REMOVE this template - not compatible with Odoo 19 -->
<template id="custom_footer_op" inherit_id="website.snippet_options">
    <!-- Snippet options content -->
</template>
```

## Common Errors and Solutions

### Error: "Service rpc is not available"
- **Cause**: Using `useService("rpc")` in frontend components
- **Solution**: Replace with `_jsonRpc` helper method using fetch API

### Error: "Invalid field 'numbercall' in 'ir.cron'"
- **Cause**: Field removed in Odoo 19
- **Solution**: Remove `<field name="numbercall">` from cron definitions

### Error: "Invalid view definition" (search views)
- **Cause**: `<group>` tags not allowed in search views (Odoo 19)
- **Solution**: Remove `<group>` tags, keep filters at root level

### Error: "Missing 'card' template"
- **Cause**: Kanban template name changed in Odoo 19
- **Solution**: Change `t-name="kanban-box"` to `t-name="card"`

### Error: "cannot import name 'slug'"
- **Cause**: Import location changed in Odoo 18+
- **Solution**: Add compatibility wrapper function

### Error: "External ID not found: website.snippet_options"
- **Cause**: Snippet system changed in Odoo 19
- **Solution**: Remove the incompatible template

### Error: "field 'active_id' does not exist"
- **Cause**: `active_id` not available in form view contexts (Odoo 19)
- **Solution**: Replace `active_id` with `id`

## Testing Checklist

After upgrade, test:
- [ ] Module installation without errors
- [ ] All views load correctly
- [ ] JavaScript components function
- [ ] Theme displays properly
- [ ] API endpoints respond
- [ ] Cron jobs execute
- [ ] Search/filter functionality
- [ ] Form submissions work
- [ ] Reports generate correctly

## Helper Commands

```bash
# Install upgraded module
python -m odoo -d [DB] -i [MODULE] --addons-path=odoo/addons,projects/[PROJECT] --stop-after-init

# Update module after changes
python -m odoo -d [DB] -u [MODULE] --stop-after-init

# Run with development mode for debugging
python -m odoo -d [DB] --dev=xml,css,js

# Install Python dependencies
pip install geopy spacy hachoir
```

## Migration Report Template

Generate comprehensive reports documenting:
- Files modified count
- Lines changed
- Patterns applied
- Manual fixes needed
- External dependencies added
- Testing status
- Known issues
- Rollback instructions

## Advanced Patterns

### Multi-Module Projects
When upgrading projects with multiple interdependent modules:
1. Analyze dependency tree
2. Upgrade in dependency order
3. Test each module individually
4. Test integrated functionality

### Theme Migrations
Special considerations for themes:
1. SCSS variable structure changes
2. Bootstrap version compatibility
3. Snippet system updates
4. Asset bundling changes

### Performance Optimization
After upgrade:
1. Regenerate assets
2. Clear caches
3. Recompile Python files
4. Optimize database indexes

## Version-Specific Notes

### Odoo 17 → 18
- Minor XML changes
- Python API mostly compatible
- JavaScript minor updates

### Odoo 18 → 19
- Major frontend architecture changes
- RPC service removed from public
- Snippet system overhaul
- Kanban template naming changes
- Search view structure changes

### Odoo 16 → 17
- OWL framework adoption
- Widget system changes
- Asset pipeline updates

## References

- [Patterns Documentation](./patterns/common_patterns.md)
- [Fix Templates](./fixes/)
- [Error Catalog](./reference/error_catalog.md)
- [API Changes](./reference/api_changes.md)