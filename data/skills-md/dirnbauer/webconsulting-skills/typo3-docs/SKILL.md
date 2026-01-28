---
name: typo3-docs
description: Create and maintain TYPO3 extension documentation following official docs.typo3.org standards. RST syntax, TYPO3 directives, rendering, and deployment.
version: 1.0.0
typo3_compatibility: "13.0 - 14.x"
triggers:
  - documentation
  - rst
  - docs
  - readme
  - typo3 documentation
---

# TYPO3 Documentation Skill

Create and maintain TYPO3 extension documentation following official docs.typo3.org standards.

## When to Use

- Creating documentation from scratch (no `Documentation/` exists)
- Editing `Documentation/**/*.rst` files
- Using TYPO3 directives: `confval`, `versionadded`, `card-grid`, `tabs`
- Creating/adding screenshots
- Rendering and testing documentation locally
- Deploying to docs.typo3.org

## Documentation Structure

```
Documentation/
├── Index.rst                 # Main entry point
├── guides.xml                # Configuration file
├── Introduction/
│   └── Index.rst
├── Installation/
│   └── Index.rst
├── Configuration/
│   └── Index.rst
├── Usage/
│   └── Index.rst
├── Developer/
│   └── Index.rst
└── Images/
    └── screenshot.png
```

## Creating Documentation from Scratch

When no `Documentation/` directory exists, use the init command:

```bash
docker run --rm --pull always -v $(pwd):/project -it \
  ghcr.io/typo3-documentation/render-guides:latest init
```

**Interactive prompts:**
1. **Format**: Choose `rst` (ReStructuredText) for full TYPO3 theme features
2. **Site Set**: Enter name/path if extension defines a Site set

## guides.xml Configuration

```xml
<?xml version="1.0" encoding="UTF-8"?>
<guides xmlns="https://www.phpdoc.org/guides" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="https://www.phpdoc.org/guides https://docs.typo3.org/render-guides/guides.xsd">
    <project title="My Extension"/>
    <extension name="my_extension"/>
</guides>
```

### With GitHub Integration

```xml
<?xml version="1.0" encoding="UTF-8"?>
<guides xmlns="https://www.phpdoc.org/guides" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="https://www.phpdoc.org/guides https://docs.typo3.org/render-guides/guides.xsd">
    <project title="My Extension" version="1.0.0"/>
    <extension name="my_extension"/>
    <inventory id="t3coreapi" url="https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/"/>
    <settings>
        <setting name="edit_on_github" value="https://github.com/vendor/my-extension/edit/main/Documentation/"/>
        <setting name="edit_on_github_branch" value="main"/>
    </settings>
</guides>
```

## RST Syntax Reference

### Headings

```rst
==========
Page Title
==========

Section
=======

Subsection
----------

Subsubsection
~~~~~~~~~~~~~
```

### Code Blocks

```rst
..  code-block:: php
    :caption: Classes/Service/MyService.php

    <?php
    declare(strict_types=1);

    namespace Vendor\MyExtension\Service;

    final class MyService
    {
        // ...
    }
```

### Inline Code and Text Roles

```rst
Use :php:`MyClass` for PHP references.
The file :file:`ext_localconf.php` is loaded automatically.
Click :guilabel:`Save` to apply changes.
Press :kbd:`Ctrl+S` to save.
```

### Links and References

```rst
See :ref:`my-reference-label` for more information.

External link: `TYPO3 Documentation <https://docs.typo3.org/>`__

..  _my-reference-label:

Section with Reference
======================

This section can be referenced from anywhere.
```

## TYPO3 Directives

### confval (Configuration Values)

```rst
..  confval:: encryptionMethod
    :name: ext-myext-encryptionMethod
    :type: string
    :default: 'aes-256-gcm'
    :required: false

    The encryption method to use for API keys.

    Available options:

    -   ``aes-256-gcm`` (recommended)
    -   ``aes-256-cbc``
```

### versionadded / versionchanged / deprecated

```rst
..  versionadded:: 2.0.0
    This feature was added in version 2.0.0.

..  versionchanged:: 2.1.0
    The default value was changed from ``false`` to ``true``.

..  deprecated:: 3.0.0
    Use :php:`newMethod()` instead.
```

### Admonitions

```rst
..  note::
    Background information users should know.

..  tip::
    Helpful suggestion for better results.

..  warning::
    Potential issue or data loss risk.

..  important::
    Critical information that must not be missed.
```

### Tabs

```rst
..  tabs::

    ..  group-tab:: Composer

        Install via Composer:

        ..  code-block:: bash

            composer require vendor/my-extension

    ..  group-tab:: TER

        Download from the TYPO3 Extension Repository.
```

### Card Grid

```rst
..  card-grid::
    :columns: 2
    :card-height: 100

    ..  card:: Installation

        Learn how to install the extension.

        :ref:`Read more <installation>`

    ..  card:: Configuration

        Configure the extension for your needs.

        :ref:`Read more <configuration>`
```

### Accordion

```rst
..  accordion::

    ..  accordion-item:: How do I install this extension?

        See the :ref:`installation` chapter.

    ..  accordion-item:: What PHP version is required?

        PHP 8.2 or higher is required.
```

## Editor Configuration

Create `Documentation/.editorconfig`:

```editorconfig
root = true

[*]
charset = utf-8
end_of_line = lf
indent_style = space
indent_size = 4
insert_final_newline = true
trim_trailing_whitespace = true
max_line_length = 80
```

## Rendering Documentation

### Local Rendering

```bash
# Render documentation
docker run --rm --pull always -v $(pwd):/project -it \
  ghcr.io/typo3-documentation/render-guides:latest

# Output is in Documentation-GENERATED-temp/
```

### With Live Preview

```bash
# Start watch mode for live preview
docker run --rm --pull always -v $(pwd):/project -p 8080:8080 -it \
  ghcr.io/typo3-documentation/render-guides:latest --watch

# Open http://localhost:8080 in browser
```

### Validation

```bash
# Validate RST syntax
docker run --rm --pull always -v $(pwd):/project -it \
  ghcr.io/typo3-documentation/render-guides:latest --no-progress --fail-on-log
```

## Screenshots

### Requirements
- PNG format
- 72 DPI
- Appropriate size (not too large)
- Always include `:alt:` text

### Adding Screenshots

```rst
..  figure:: /Images/BackendModule.png
    :alt: Backend module screenshot
    :class: with-shadow

    The backend module provides an overview of all items.
```

### Screenshot Directory

```
Documentation/
└── Images/
    ├── BackendModule.png
    ├── Configuration.png
    └── Frontend.png
```

## Writing Guidelines

### General Rules
- Use **American English** spelling (color, behavior, optimize)
- Use **sentence case** for headings (not Title Case)
- Maximum line length: **80 characters**
- Use **4 spaces** for indentation (no tabs)
- Add blank line before and after code blocks
- Use present tense

### CamelCase for Files
- `Index.rst` (not `index.rst`)
- `Configuration/` (not `configuration/`)
- `BackendModule.png` (not `backend-module.png`)

### Example: Good Documentation

```rst
============
Installation
============

This chapter explains how to install the extension.

Requirements
============

-   TYPO3 v13.4 or v14.x
-   PHP 8.2 or higher

Installation via Composer
=========================

Run the following command:

..  code-block:: bash

    composer require vendor/my-extension

After installation, activate the extension:

..  code-block:: bash

    vendor/bin/typo3 extension:activate my_extension
```

## Deployment to docs.typo3.org

### Prerequisites
1. Extension registered on extensions.typo3.org
2. Documentation in `Documentation/` directory
3. Valid `guides.xml` configuration

### Webhook Setup

1. Go to https://intercept.typo3.com/
2. Login with TYPO3.org account
3. Register your repository
4. Add webhook to GitHub/GitLab

### Trigger Rendering

Documentation is automatically rendered when:
- Webhook receives push event
- Manual trigger via Intercept

## Complete Index.rst Example

```rst
..  include:: /Includes.rst.txt

.. _start:

==============
My Extension
==============

:Extension key:
    my_extension

:Package name:
    vendor/my-extension

:Version:
    |release|

:Language:
    en

:Author:
    Your Name

:License:
    This document is published under the
    `Creative Commons BY 4.0 <https://creativecommons.org/licenses/by/4.0/>`__
    license.

:Rendered:
    |today|

----

This extension provides functionality for managing items.

----

**Table of Contents**

..  toctree::
    :maxdepth: 2
    :titlesonly:

    Introduction/Index
    Installation/Index
    Configuration/Index
    Usage/Index
    Developer/Index

..  toctree::
    :hidden:

    Sitemap
```

## Resources

- **TYPO3 Documentation Guide**: https://docs.typo3.org/m/typo3/docs-how-to-document/main/en-us/
- **RST Primer**: https://docs.typo3.org/m/typo3/docs-how-to-document/main/en-us/WritingReST/
- **Render Guides**: https://github.com/TYPO3-Documentation/render-guides
- **Intercept**: https://intercept.typo3.com/

---

## Credits & Attribution

This skill is based on the excellent work by
**[Netresearch DTT GmbH](https://www.netresearch.de/)**.

Original repository: https://github.com/netresearch/typo3-docs-skill

**Copyright (c) Netresearch DTT GmbH** - Methodology and best practices  
Adapted by webconsulting.at for this skill collection
