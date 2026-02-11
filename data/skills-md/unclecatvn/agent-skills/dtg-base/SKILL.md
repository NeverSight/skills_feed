---
name: dtg-base
description: Complete reference for DTG Base module utilities and helpers. DTGBase is an abstract model providing common utility methods for date/time handling, barcode generation, timezone conversion, file operations, and more.
globs: "**/addons_customs/erp/**/*.py"
license: MIT
author: UncleCat
version: 1.0.0
---

# DTG Base Skill

Complete reference for DTG Base module utilities and helpers in Odoo 18.

## What is DTG Base?

DTG Base is a custom abstract model (`dtg_base.DTGBase`) that provides common utility methods for Odoo development. It's designed to be inherited by other models to gain access to helpful utilities.

## Quick Reference

| Utility | Description |
|---------|-------------|
| [Date & Period](#date--period-utilities) | Find first/last date of period, period iteration |
| [Timezone](#timezone-conversion) | Convert local to UTC, UTC to local |
| [Barcode](#barcode-utilities) | Check barcode exists, generate EAN13 |
| [Batch Processing](#batch-processing) | Split large recordsets into batches |
| [after_commit](#after_commit-decorator) | Execute code after transaction commit |
| [Vietnamese Text](#string--text-utilities) | Strip accents, convert to non-accent |
| [File Utilities](#file-utilities) | Zip directories, get file size |
| [Number Utilities](#number-utilities) | Round to decimal places |

---

## Main Guide

**File**: `odoo-18-dtg-base-guide.md`

### When to use this skill

- Working with DTG Odoo codebase
- Need date/period calculations
- Timezone conversions
- Barcode validation
- Batch processing large recordsets
- Vietnamese text processing
- File zipping utilities

---

## DTGBase Abstract Model

### Inherit from DTGBase

**Location**: `addons_customs/erp/dtg_base/models/dtg_base.py`

```python
from odoo import models

class MyModel(models.Model):
    _name = 'my.model'
    _inherit = ['dtg_base.dtg_base']

    def my_method(self):
        # Now you have access to all DTGBase utilities
        first_date = self.find_first_date_of_period('2024-01-15', 'month')
        utc_date = self.convert_local_to_utc('2024-01-15 10:00:00')
```

---

## File Structure

```
agent-skills/skills/dtg-base/
├── SKILL.md                       # This file - master index
├── odoo-18-dtg-base-guide.md      # Complete DTG Base utilities reference
└── README.md                      # Skill overview
```

---

## Utilities Overview

### Date & Period Utilities
- `find_first_date_of_period(date, period_type)` - Get first date of period
- `find_last_date_of_period(date, period_type)` - Get last date of period
- `period_iter(start_date, end_date, period_type)` - Iterate over periods

### Timezone Conversion
- `convert_local_to_utc(local_dt, tz=None)` - Convert local datetime to UTC
- `convert_utc_to_local(utc_dt, tz=None)` - Convert UTC datetime to local

### Barcode Utilities
- `barcode_exists(barcode, exclude_id=0)` - Check if barcode already exists
- `get_ean13 barcode)` - Generate/check EAN13 barcode

### Batch Processing
- `splittor(limit=None)` - Split recordset into batches for processing

### String & Text Utilities
- `strip_accents(text)` - Remove Vietnamese accents
- `_no_accent_vietnamese(text)` - Convert Vietnamese text

### File Utilities
- `zip_dir(source_dir, output_file)` - Zip a directory
- `zip_dirs(dirs, output_file)` - Zip multiple directories
- `_get_file_size(file_path)` - Get human-readable file size

### Number Utilities
- `round_decimal(value, decimal_places)` - Round to specific decimal places

---

**For detailed documentation, see [odoo-18-dtg-base-guide.md](./odoo-18-dtg-base-guide.md)**
