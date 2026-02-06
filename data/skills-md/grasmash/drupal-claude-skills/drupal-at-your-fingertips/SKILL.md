---
name: drupal-at-your-fingertips
description: Comprehensive Drupal patterns from "Drupal at Your Fingertips" by Selwyn Polit. Covers 50+ topics including services, hooks, forms, entities, caching, testing, and more.
---

# Drupal at Your Fingertips

**Source**: [drupalatyourfingertips.com](https://drupalatyourfingertips.com)
**Author**: Selwyn Polit
**License**: Open access documentation

## When This Skill Activates

Activates when working with Drupal development topics covered in the d9book including:
- Core APIs (services, hooks, events, plugins)
- Content (nodes, fields, entities, paragraphs, taxonomy)
- Forms and validation
- Routing and controllers
- Theming (Twig, render arrays, preprocess)
- Caching and performance
- Testing (PHPUnit, DTT)
- Common patterns and best practices

---

## Available Topics

All topics are available as references in the `/references/` directory.

Each reference links to the full chapter on drupalatyourfingertips.com with:
- Detailed explanations and code examples
- Best practices and common patterns
- Step-by-step guides
- Troubleshooting tips

### Core Concepts
- @references/services.md - Dependency injection and service container
- @references/hooks.md - Hook system and implementations
- @references/events.md - Event subscribers and dispatchers
- @references/plugins.md - Plugin API and annotations
- @references/entities.md - Entity API and custom entities

### Content Management
- @references/nodes-and-fields.md - Node and field API
- @references/forms.md - Form API and validation
- @references/paragraphs.md - Paragraphs module patterns
- @references/taxonomy.md - Taxonomy and vocabularies
- @references/menus.md - Menu system

### Development Tools
- @references/composer.md - Dependency management
- @references/drush.md - Drush commands
- @references/debugging.md - Debugging techniques
- @references/logging.md - Logging and monitoring
- @references/dtt.md - Drupal Test Traits

### Advanced Topics
- @references/batch.md - Batch API for long operations
- @references/queue.md - Queue API for background tasks
- @references/cron.md - Cron jobs and scheduling
- @references/ajax.md - AJAX framework
- @references/javascript.md - JavaScript in Drupal

See `/references/` directory for complete list of 50+ topics.

---

---

**To update**: Run `.claude/scripts/sync-d9book.sh`
