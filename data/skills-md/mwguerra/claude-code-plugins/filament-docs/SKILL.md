---
name: filament-docs
description: Reference FilamentPHP v4 documentation for patterns, methods, and implementation examples
---

# FilamentPHP Documentation Reference Skill

## Overview

This skill provides access to the complete FilamentPHP v4 official documentation. Use this skill to look up exact implementations, method signatures, and patterns before generating any Filament code.

## Documentation Location

All documentation is stored in:
`/home/mwguerra/projects/mwguerra/claude-code-plugins/filament-specialist/skills/filament-docs/references/`

## Directory Structure

```
references/
├── actions/                    # Action buttons and modals
│   └── *.md                    # Action types and configurations
├── forms/                      # Form components
│   └── *.md                    # All form field types
├── general/
│   ├── 01-introduction/        # Getting started, installation
│   ├── 03-resources/           # CRUD resources
│   ├── 06-navigation/          # Menu and navigation
│   ├── 07-users/               # Auth and permissions
│   ├── 08-styling/             # Themes and CSS
│   ├── 09-advanced/            # Advanced patterns
│   ├── 10-testing/             # Testing guide
│   ├── 11-plugins/             # Plugin development
│   └── 12-components/          # UI components
├── infolists/                  # Infolist entries
│   └── *.md                    # Display components
├── notifications/              # Notification system
│   └── *.md                    # Toast and DB notifications
├── schemas/                    # Schema validation
│   └── *.md                    # Schema patterns
├── tables/                     # Table components
│   ├── 02-columns/             # Column types
│   └── 03-filters/             # Filter types
└── widgets/                    # Dashboard widgets
    └── *.md                    # Widget types
```

## Usage

### When to Use This Skill

1. Before generating any Filament component code
2. When troubleshooting Filament errors
3. To verify method signatures and parameters
4. To find correct import statements
5. To understand Filament v4 patterns

### Search Workflow

1. **Identify Topic**: Determine what documentation is needed
2. **Navigate to Folder**: Go to relevant directory
3. **Read Documentation**: Extract exact patterns
4. **Apply Knowledge**: Use in code generation

### Common Lookups

| Topic | Directory |
|-------|-----------|
| Resource creation | `general/03-resources/` |
| Form fields | `forms/` |
| Table columns | `tables/02-columns/` |
| Table filters | `tables/03-filters/` |
| Actions | `actions/` |
| Widgets | `widgets/` |
| Infolists | `infolists/` |
| Testing | `general/10-testing/` |
| Styling | `general/08-styling/` |
| Navigation | `general/06-navigation/` |
| Auth/Permissions | `general/07-users/` |
| Plugin Development | `general/11-plugins/` |

## Documentation Reading Pattern

When reading documentation:

1. **Find the right file**: Match component to documentation file
2. **Read the overview**: Understand the component's purpose
3. **Extract code examples**: Copy exact patterns
4. **Note imports**: Get correct use statements
5. **Check configuration**: Review options and parameters

## Example Usage

### Looking up TextInput field

1. Navigate to `forms/` directory
2. Find text-input documentation
3. Extract:
   - Basic usage pattern
   - Available methods (required, email, tel, etc.)
   - Validation integration
   - Correct import statement

### Looking up Table columns

1. Navigate to `tables/02-columns/`
2. Find specific column type
3. Extract:
   - Column configuration
   - Formatting options
   - Relationship handling
   - Sorting and searching

## Output

After reading documentation, provide:

1. **Exact code pattern** from docs
2. **Required imports**
3. **Configuration options**
4. **Best practices noted**
5. **Version-specific considerations**
