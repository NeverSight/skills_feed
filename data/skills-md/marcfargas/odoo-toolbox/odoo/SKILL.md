---
name: odoo
description: Odoo ERP integration - connect, introspect, and automate your Odoo instance
---

# /odoo

Odoo ERP integration via `@marcfargas/odoo-client`. Connect, query, and automate.

## Quick Start

```typescript
import { createClient } from '@marcfargas/odoo-client';

const client = await createClient();  // reads ODOO_URL, ODOO_DB, ODOO_USER, ODOO_PASSWORD

// Core CRUD — directly on client
const partners = await client.searchRead('res.partner', [['is_company', '=', true]], {
  fields: ['name', 'email'],
  limit: 10,
});

// Chatter — via client.mail service accessor
await client.mail.postInternalNote('crm.lead', 42, '<p>Called customer.</p>');
await client.mail.postOpenMessage('res.partner', 7, 'Order shipped.');

// Module management — via client.modules accessor
if (await client.modules.isModuleInstalled('sale')) { /* ... */ }
```

### Service Accessors

Domain-specific helpers are accessed via lazy getters on the client:

| Accessor | Description | Skill doc |
|----------|-------------|-----------|
| `client.mail.*` | Post notes & messages on chatter | `mail/chatter.md` |
| `client.modules.*` | Install, uninstall, check modules | `base/modules.md` |
| `client.accounting.*` | Cash discovery, reconciliation, partner resolution | `modules/accounting.md` |
| `client.attendance.*` | Clock in/out, presence tracking | `modules/attendance.md` |
| `client.timesheets.*` | Timer start/stop, time logging | `modules/timesheets.md` |

Core CRUD (`searchRead`, `create`, `write`, `unlink`, etc.) stays directly on `client`.

## Prerequisites (Must Read First)

Before any Odoo operation, load these foundational modules:

1. `base/connection.md` — `createClient()`, authentication, environment variables
2. `base/field-types.md` — Odoo type system (read/write asymmetry)
3. `base/domains.md` — Query filter syntax

## Additional Modules

Load as needed by reading `base/{name}.md`:

| Module | Description |
|--------|-------------|
| introspection | Discover models & fields |
| crud | Create, read, update, delete patterns |
| search | Search & filtering patterns |
| properties | Dynamic user-defined fields |
| modules | Module lifecycle management |
| skill-generation | How to create new skills |

## Mail & Messaging

Skills for Odoo's mail system. Load by reading `mail/{name}.md`:

| Module | Description |
|--------|-------------|
| chatter | Post messages and notes on records (`client.mail.*`) |
| activities | Schedule and manage activities/tasks |
| discuss | Chat channels and direct messages |

**Note:** The `mail` module is part of base Odoo and is typically always installed.

## Version-Specific Notes

Breaking changes between Odoo versions are documented in `CHANGES_V{XX}.md`:

| Document | Version | Key Changes |
|----------|---------|-------------|
| `CHANGES_V17.md` | Odoo 17 | mail.channel → discuss.channel, read tracking |

## Module-Specific Skills

Skills that require specific Odoo modules to be installed. Before loading, verify the required modules are present using `client.modules.isModuleInstalled()`.

Load by reading the path shown below:

| Skill | Path | Required Modules | Description |
|-------|------|------------------|-------------|
| accounting | `modules/accounting.md` | `account` | Accounting patterns, cashflow, reconciliation, PnL, validation |
| contracts | `modules/contracts.md` | `contract` (OCA) | Recurring contracts, billing schedules, revenue projection |
| attendance | `modules/attendance.md` | `hr_attendance` | Clock in/out, presence tracking (`client.attendance.*`) |
| timesheets | `modules/timesheets.md` | `hr_timesheet` | Timer start/stop, time logging on projects (`client.timesheets.*`) |
| mis-builder | `oca/mis-builder.md` | `mis_builder`, `date_range`, `report_xlsx` | MIS Builder — reading, computing, exporting reports |
| mis-builder-dev | `oca/mis-builder-dev.md` | `mis_builder`, `date_range`, `report_xlsx` | MIS Builder — creating & editing report templates, expression language, styling |

## Skill Generation Workflow

1. Read `base/introspection.md`
2. Introspect target model schema
3. Create `skills/{model-action}.md` following the format in `base/skill-generation.md`
4. Update this SKILL.md to reference the new skill
