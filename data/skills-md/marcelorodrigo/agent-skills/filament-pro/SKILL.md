---
name: filament-pro
description: Build Laravel admin panels with Filament v5. Use for creating resources, forms, tables, widgets, and testing admin interfaces with Livewire v4.
license: MIT
compatibility: Requires Laravel 11.28+, PHP 8.2+, Livewire v4, TailwindCSS v4.1+
metadata:
  version: "1.0.0"
---

# Filament v5

Build powerful Laravel admin panels using Filament v5's server-driven UI with Schemas and Livewire v4 reactivity.

## Overview

Filament v5 is a Laravel admin panel framework that provides complete CRUD interfaces, forms, tables, and dashboard components through a declarative PHP API. Built on Livewire v4, it offers real-time reactivity without writing JavaScript.

### Key Concepts

- **PanelProvider**: Central configuration class defining your admin panel
- **Resources**: Automatic CRUD interfaces for Eloquent models
- **Schemas**: Declarative UI components (forms, tables, infolists)
- **Actions**: Interactive buttons with modals and backend logic
- **Widgets**: Dashboard components for data visualization

### System Requirements

- Laravel 11.28+
- PHP 8.2+
- Livewire v4
- Node.js 18+
- Tailwind CSS v4.1+

## Installation

Install Filament via Composer and scaffold a panel:

```bash
composer require filament/filament:"^5.0" -W
php artisan filament:install --scaffold
npm install && npm run dev
php artisan make:filament-user
```

This creates the panel provider, directory structure, and assets needed to start building.

### Directory Structure

```
app/
  Filament/
    Resources/          # CRUD resources with forms and tables
    Pages/              # Custom pages
    Widgets/            # Dashboard widgets
  Providers/
    Filament/
      AdminPanelProvider.php
```

## Core Concepts

### Panel Configuration

The PanelProvider is the entry point for your admin panel. It configures:

- **Identity**: ID, path, branding (name, logo, colors)
- **Discovery**: Auto-discovery of resources, pages, and widgets
- **Middleware**: Session, authentication, and custom middleware
- **Tenancy**: Multi-tenant configuration for SaaS applications

### Resources

Resources provide complete CRUD interfaces through:

- **Forms**: Schema-based forms with 20+ field types (TextInput, Select, DatePicker, FileUpload, RichEditor, etc.)
- **Tables**: Data tables with columns, filters, sorting, and actions
- **Pages**: Automatic generation of List, Create, Edit, and View pages
- **Relations**: Relation managers for handling model relationships

### Forms

Forms use a schema-based approach where you declare fields as PHP objects:

- **Input Fields**: Text, select, checkbox, toggle, date/time pickers
- **Media**: File and image uploads with validation
- **Complex Fields**: Rich text editors, repeaters, builders
- **Layout**: Grids, sections, tabs, and wizards
- **Validation**: Built-in Laravel validation rules

### Tables

Tables display data with extensive customization:

- **Columns**: Text, badges, icons, images, colors
- **Filters**: Select, ternary, and custom filter logic
- **Actions**: Per-row actions, bulk actions, header actions
- **Features**: Search, sorting, pagination, grouping

### Actions

Actions are interactive buttons that trigger:

- **Modals**: Form dialogs for data collection
- **Confirmation**: Destructive action confirmation
- **Wizards**: Multi-step processes
- **Notifications**: User feedback after completion

### Widgets

Dashboard widgets include:

- **Stats Overview**: Metric cards with trends and sparklines
- **Charts**: Line, bar, pie charts using Chart.js
- **Tables**: Data tables for recent records

### Testing

Filament uses Pest PHP with Livewire testing helpers:

- **Page Testing**: List, create, edit, view page functionality
- **Form Testing**: Validation, state management, submission
- **Table Testing**: Search, filters, sorting, actions
- **Authorization Testing**: Access control and permissions

### Authorization

Access control through:

- **Panel Access**: FilamentUser contract for panel-level access
- **Policies**: Laravel policies for resource-level permissions
- **Field Visibility**: Show/hide fields based on user roles
- **Multi-Tenancy**: Tenant isolation for SaaS applications

## Architecture Patterns

### Server-Driven UI

Filament uses a server-driven approach where the backend defines the UI structure through schemas. The PHP code describes forms, tables, and layouts which Filament renders as Livewire components.

### Schema System

Schemas are PHP configuration objects that define:
- Form fields and their validation rules
- Table columns and their formatting
- Layout containers (grids, sections, tabs)
- Action definitions and their behavior

### Livewire Integration

All components mount as Livewire components, providing:
- Real-time reactivity without page reloads
- Automatic state management
- Event handling and AJAX updates
- Form validation with instant feedback

### Resource-First Design

The framework encourages a resource-first approach:
1. Define your Eloquent models
2. Create resources that map to those models
3. Configure forms and tables for each resource
4. Add actions and widgets as needed

## Command Reference

| Command | Purpose |
|---------|---------|
| `filament:install --scaffold` | Install Filament with panel scaffolding |
| `make:filament-resource` | Create CRUD resource |
| `make:filament-page` | Create custom page |
| `make:filament-widget` | Create dashboard widget |
| `make:filament-panel` | Create additional panel |
| `make:filament-user` | Create admin user |
| `make:filament-relation-manager` | Create relation manager |
| `filament:cache-components` | Cache for production |

## Detailed Documentation

### Reference Guides

Comprehensive documentation for each component:

- **[Forms](references/forms.md)** - All form components, validation rules, layouts, and conditional logic
- **[Tables](references/tables.md)** - Column types, filters, actions, and table configuration
- **[Resources](references/resources.md)** - CRUD resources, relation managers, infolists, and global search
- **[Infolists](references/infolists.md)** - Read-only data display components (TextEntry, ImageEntry, IconEntry)
- **[Widgets](references/widgets.md)** - Stats overview, charts, and table widgets
- **[Actions](references/actions.md)** - Modal actions, notifications, action groups, and wizards
- **[Notifications](references/notifications.md)** - Flash messages, database, and broadcast notifications
- **[Schemas](references/schemas.md)** - Schema system, layouts, and component organization
- **[Testing](references/testing.md)** - Pest testing patterns for resources, forms, tables, and authorization
- **[Authorization](references/authorization.md)** - Access control, policies, roles, and multi-tenancy

### Code Examples

See [examples.md](references/examples.md) for complete working code examples including:
- Complete resource implementations
- Form configurations
- Table setups
- Widget configurations
- Test suites
- Authorization patterns

## Best Practices

### Performance

- Use `getEloquentQuery()` to eager load relationships and prevent N+1 queries
- Enable component caching in production with `filament:cache-components`
- Limit pagination options and use deferred loading for large datasets
- Cache expensive calculations in widgets

### Security

- Always implement the FilamentUser contract for panel access control
- Use Laravel policies for resource-level authorization
- Validate all input with appropriate form rules
- Never skip authorization in production environments
- Implement proper tenant isolation for multi-tenant applications

### Code Organization

- Organize by feature: `app/Filament/Admin/Resources/`
- Extract complex forms and tables to separate classes
- Create reusable form components for common patterns
- Keep resources focused on single responsibility
- Use dedicated pages for non-CRUD functionality

### Testing

- Test all CRUD operations for each resource
- Validate form validation rules with multiple scenarios
- Test table features: search, filters, sorting, actions
- Verify authorization with different user roles
- Use factories to create realistic test data

## When to Use Filament

Filament is ideal for:

- **Admin Panels**: Back-office interfaces for managing application data
- **CMS**: Content management systems with rich editing capabilities
- **CRM**: Customer relationship management tools
- **E-commerce**: Product, order, and inventory management
- **SaaS Applications**: Multi-tenant admin interfaces
- **Internal Tools**: Business process management and data entry

## Additional Resources

- [Official Documentation](https://filamentphp.com/docs/5.x)
- [GitHub Repository](https://github.com/filamentphp/filament)
- [Live Demo](https://demo.filamentphp.com)
- [Discord Community](https://filamentphp.com/discord)

---

**Version**: 1.0.0  
**License**: MIT  
**Compatibility**: Laravel 11+, PHP 8.2+, Livewire v4
