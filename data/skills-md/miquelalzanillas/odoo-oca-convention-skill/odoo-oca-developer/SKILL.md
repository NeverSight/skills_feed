---
name: odoo-oca-developer
description: "Expert guidance for developing, migrating, and maintaining Odoo modules (versions 14.0-19.0) following OCA conventions. Use when working with Odoo modules to create new modules from OCA template, migrate modules between versions using OpenUpgrade, extend core Odoo modules, ensure OCA compliance, and structure module files correctly. Includes OCA coding standards, module structure templates, OpenUpgrade migration patterns, and validation tools."
---

# Odoo OCA Developer

Expert assistant for Odoo module development following OCA conventions and best practices.

## Core Capabilities

### 1. Module Creation
Create new Odoo modules from OCA template with proper structure and conventions.

**Quick Start:**
```bash
python scripts/init_oca_module.py my_module_name --path /path/to/addons --version 17.0
```

**What this provides:**
- Complete OCA-compliant directory structure
- Pre-configured `__manifest__.py` with required keys
- README structure following OCA guidelines
- Proper `__init__.py` imports
- Example model, view, and security files

**Module naming conventions:**
- Use singular form: `sale_order_import` (not `sale_orders_import`)
- For base modules: prefix with `base_` (e.g., `base_location_nuts`)
- For localization: prefix with `l10n_CC_` (e.g., `l10n_es_pos`)
- For extensions: prefix with parent module (e.g., `mail_forward`)
- For combinations: Odoo module first (e.g., `crm_partner_firstname`)

### 2. Module Structure

Follow OCA conventions strictly. Reference [oca_conventions.md](references/oca_conventions.md) for detailed guidelines.

**Essential structure:**
```
module_name/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── <model_name>.py
├── views/
│   └── <model_name>_views.xml
├── security/
│   ├── ir.model.access.csv
│   └── <model_name>_security.xml
├── data/
│   └── <model_name>_data.xml
├── readme/
│   ├── DESCRIPTION.rst
│   ├── USAGE.rst
│   └── CONTRIBUTORS.rst
└── tests/
    ├── __init__.py
    └── test_<feature>.py
```

**Key principles:**
- One file per model: `models/sale_order.py`
- Views match model names: `views/sale_order_views.xml`
- Demo data has `_demo` suffix: `demo/sale_order_demo.xml`
- Migrations in versioned folders: `migrations/17.0.1.0.0/`

### 3. OCA Conventions Compliance

**__manifest__.py essentials:**
```python
{
    'name': 'Module Name',
    'version': '17.0.1.0.0',  # {odoo}.x.y.z format
    'category': 'Sales',
    'license': 'AGPL-3',  # or LGPL-3
    'author': 'Your Company, Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/<repository>',
    'depends': ['base', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/model_name_views.xml',
    ],
    'installable': True,
}
```

**Python code structure:**
```python
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    # Fields
    custom_field = fields.Char(string="Custom Field")
    
    # Compute methods
    @api.depends('order_line')
    def _compute_total(self):
        for order in self:
            order.total = sum(order.order_line.mapped('price_total'))
    
    # Business methods
    def action_custom(self):
        self.ensure_one()
        # Implementation
```

**XML naming conventions:**
- Views: `<model_name>_view_<type>` (e.g., `sale_order_view_form`)
- Actions: `<model_name>_action` (e.g., `sale_order_action`)
- Menus: `<model_name>_menu`
- Groups: `<model_name>_group_<name>`
- Demo: suffix with `_demo`

### 4. Module Migration with OpenUpgrade

Migrate modules between Odoo versions following OpenUpgrade patterns. See [openupgrade_migration.md](references/openupgrade_migration.md) for complete guide.

**Migration structure:**
```
module_name/
└── migrations/
    └── 17.0.1.0.0/
        ├── pre-migration.py
        ├── post-migration.py
        └── noupdate_changes.xml
```

**Pre-migration example:**
```python
from openupgradelib import openupgrade

@openupgrade.migrate()
def migrate(env, version):
    # Rename fields before module loads
    openupgrade.rename_fields(env, [
        ('sale.order', 'sale_order', 'old_field', 'new_field'),
    ])
    
    # Rename models
    openupgrade.rename_models(env.cr, [
        ('old.model', 'new.model'),
    ])
```

**Post-migration example:**
```python
from openupgradelib import openupgrade

@openupgrade.migrate()
def migrate(env, version):
    # Map old values to new
    openupgrade.map_values(
        env.cr,
        openupgrade.get_legacy_name('state'),
        'state',
        [('draft', 'pending'), ('confirm', 'confirmed')],
        table='sale_order',
    )
    
    # Recompute fields
    env['sale.order'].search([])._compute_total()
```

**Common migration tasks:**
- Rename fields: `openupgrade.rename_fields()`
- Rename models: `openupgrade.rename_models()`
- Rename tables: `openupgrade.rename_tables()`
- Map values: `openupgrade.map_values()`
- Delete obsolete data: `openupgrade.delete_records_safely_by_xml_id()`

### 5. Module Extension

Extend core Odoo modules following OCA patterns.

**Inherit existing model:**
```python
from odoo import fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    custom_field = fields.Char(string="Custom Info")
```

**Extend existing view:**
```xml
<record id="res_partner_view_form" model="ir.ui.view">
    <field name="model">res.partner</field>
    <field name="inherit_id" ref="base.view_partner_form"/>
    <field name="arch" type="xml">
        <xpath expr="//field[@name='email']" position="after">
            <field name="custom_field"/>
        </xpath>
    </field>
</record>
```

**Module dependencies:**
- Always declare dependencies in `__manifest__.py`
- Use `depends` key for Odoo core/OCA modules
- Use `external_dependencies` for Python packages
- Document installation requirements in README

### 6. Validation and Quality

**Validate module structure:**
```bash
python scripts/validate_module.py /path/to/module
```

**What is checked:**
- Required files presence (`__init__.py`, `__manifest__.py`)
- Manifest completeness (required keys)
- OCA author attribution
- License compliance (AGPL-3 or LGPL-3)
- Version format (x.y.z.w.v)
- File naming conventions
- Directory structure

**Code quality tools:**
```bash
# Install pre-commit for OCA checks
pip install pre-commit
pre-commit install

# Run checks
pre-commit run --all-files

# Run specific checks
flake8 module_name/
pylint --load-plugins=pylint_odoo module_name/
```

## Workflow Decision Tree

**"I need to create a new Odoo module"**
→ Use `scripts/init_oca_module.py` to generate OCA-compliant structure
→ Edit `__manifest__.py` with module details
→ Create models in `models/` directory
→ Create views in `views/` directory
→ Add security rules in `security/`
→ Update `readme/` documentation
→ Run validation: `scripts/validate_module.py`

**"I need to migrate a module to a new Odoo version"**
→ Check OpenUpgrade for breaking changes
→ Create migration folder: `migrations/<new_version>/`
→ Write pre-migration script for schema changes
→ Write post-migration script for data transformation
→ Test on copy of production database
→ Reference [openupgrade_migration.md](references/openupgrade_migration.md)

**"I need to extend a core Odoo module"**
→ Create new module with core module in `depends`
→ Use `_inherit` to extend models
→ Use `inherit_id` to extend views
→ Follow OCA naming: `<core_module>_<feature>`
→ Keep changes minimal and focused

**"I'm not sure if my module follows OCA conventions"**
→ Run `scripts/validate_module.py`
→ Check [oca_conventions.md](references/oca_conventions.md)
→ Review __manifest__.py for required keys
→ Verify file naming and structure
→ Ensure OCA author attribution

## Resources

### scripts/
- **init_oca_module.py**: Create new Odoo module with OCA-compliant structure
- **validate_module.py**: Validate module against OCA conventions

### references/
- **oca_conventions.md**: Complete OCA coding standards and module structure guidelines
- **openupgrade_migration.md**: OpenUpgrade migration patterns and best practices

### assets/
- **module_template/**: Official OCA module template with complete directory structure

## Best Practices

### Module Development
- Start with OCA template: `scripts/init_oca_module.py`
- Follow naming conventions strictly
- One file per model
- Keep models, views, and data separate
- Use meaningful xmlids following OCA patterns
- Include comprehensive tests
- Document in readme/ folder

### Code Quality
- Follow PEP8 for Python code
- Use 4-space indentation in XML
- No SQL injection vulnerabilities
- Never bypass ORM without justification
- Never commit transactions manually
- Use `_logger.debug()` for import errors
- Handle external dependencies properly

### Git Commits
Format: `[TAG] module_name: short summary`

Common tags:
- `[ADD]` - New feature/module
- `[FIX]` - Bug fix
- `[REF]` - Refactoring
- `[IMP]` - Improvement
- `[MIG]` - Migration
- `[REM]` - Removal

### Migration Strategy
1. Study OpenUpgrade analysis for target version
2. Check for breaking changes in core modules
3. Test on database copy first
4. Write pre-migration for schema changes
5. Write post-migration for data transformation
6. Document breaking changes in README
7. Update version following semantic versioning

## Common Patterns

### Pattern: Add computed field with dependencies
```python
total = fields.Float(compute='_compute_total', store=True)

@api.depends('line_ids.amount')
def _compute_total(self):
    for record in self:
        record.total = sum(record.line_ids.mapped('amount'))
```

### Pattern: Extend view safely
```xml
<xpath expr="//field[@name='partner_id']" position="after">
    <field name="custom_field"/>
</xpath>
```

### Pattern: Add security group
```xml
<record id="group_custom" model="res.groups">
    <field name="name">Custom Access</field>
    <field name="category_id" ref="base.module_category_sales"/>
</record>
```

### Pattern: Migration with value mapping
```python
openupgrade.map_values(
    env.cr,
    openupgrade.get_legacy_name('old_field'),
    'new_field',
    [('old_value', 'new_value')],
    table='model_table',
)
```

## Troubleshooting

**Module not appearing in Apps**
- Check `'installable': True` in __manifest__.py
- Verify __init__.py imports
- Run: `odoo-bin -u module_name -d database`

**Import errors**
- Add try-except for external dependencies
- Document installation in readme/INSTALL.rst
- Add to requirements.txt for Python packages

**Migration fails**
- Check pre-migration runs before module load
- Verify table/column names with `\d table` in psql
- Use `openupgrade.logged_query()` for debugging
- Test on copy database first

**Tests failing**
- Use `tagged('post_install', '-at_install')`
- Test with minimal user permissions using `@users()`
- Avoid dynamic dates, use `freezegun`
- Mock external services

## Quick Reference

**Create module:**
```bash
python scripts/init_oca_module.py my_module --version 17.0
```

**Validate module:**
```bash
python scripts/validate_module.py path/to/module
```

**Check conventions:**
See [oca_conventions.md](references/oca_conventions.md)

**Migration guide:**
See [openupgrade_migration.md](references/openupgrade_migration.md)

**Module template:**
Copy from [assets/module_template/](assets/module_template/)

