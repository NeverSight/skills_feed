---
name: figlet-text-converter
description: This skill processes files containing figlet tags and replaces them with ASCII art representations. It detects and preserves comment styles (forward slash forward slash, hash, double-dash, forward slash asterisk), automatically manages Node.js dependencies, and supports 400+ fonts (defaulting to the standard font). The skill should be used when a user requests converting marked text in a file to ASCII art using figlet tag syntax, or when they want to list available fonts.
---

# Figlet Text Converter

## Overview

This skill converts marked text in files to ASCII art using the figlet library. It uses a simple, universal tag syntax that works across all file types and intelligently preserves comment formatting when tags are placed in commented sections. The skill handles dependency management automatically and supports 400+ fonts with sensible defaults.

## When to Use This Skill

Use this skill when:
- User asks to convert text in a file to ASCII art
- User provides a file containing `<figlet>` tags
- User requests to list available figlet fonts
- User wants to add visual ASCII art headers or banners to code, documentation, or configuration files

## Tag Syntax

### Universal Markup

Insert `<figlet>` tags anywhere in a file to mark text for ASCII art conversion:

**With font specification:**
```
<figlet font="3-D">Text to Convert</figlet>
```

**Using default font (standard):**
```
<figlet>Text to Convert</figlet>
```

### Usage in Different Contexts

#### Markdown Documents
```markdown
# Section Title

<figlet font="Standard">Important Notice</figlet>

Content goes here...
```

#### Shell Scripts
```bash
#!/bin/bash

echo '<figlet>Deployment Started</figlet>'

# Script logic...
```

#### Python Code
```python
# <figlet>Configuration</figlet>

config = {
    'setting': 'value'
}
```

#### PHP/JavaScript
```php
// <figlet font="Block">Database Connection</figlet>

function connectDB() {
    // ...
}
```

#### Plain Text/Config Files
```
<figlet>System Status Report</figlet>

This report contains...
```

## Workflow

### Processing a File

When a user requests ASCII art conversion:

1. Read the file containing `<figlet>` tags
2. Validate all font names (error immediately if invalid)
3. For each tag:
   - Extract the font name (or use 'standard' if omitted)
   - Generate ASCII art for the text
   - Detect comment style from the surrounding line (// # -- /*)
   - Format output with appropriate comment prefixes
4. Replace tags with formatted ASCII art
5. Write changes back to the file

### Handling Comments

The skill automatically detects comment context:

**Single-line comments:**
```bash
// <figlet>Section Break</figlet>
```
Outputs each line with `// ` prefix:
```bash
// ___         _   _                  ____          _
// / __| ___  | | | | ___  _ _      | __ ) _ _  __| | |
// \__ \/ -_) | |_| |/ _ \| '  \    | _ \| '_|/ _` | |
// |___/\___|  \___/ \___/|_|_|_|   |_| \_\_|  \__,_|_|
```

**Hash comments (Python, Shell):**
```python
# <figlet>Configuration</figlet>
```
Outputs with `# ` prefix.

**SQL/SQL comments:**
```sql
-- <figlet>Query Section</figlet>
```
Outputs with `-- ` prefix.

**Block comments:**
```java
/* <figlet>Module Start</figlet>
```
Outputs with ` * ` prefix:
```java
 * ___  _           _     _        ___   _             _
 * |  \/  | ___   __| | _ | | ___  / __| | |_  __ _  _ | |_
 * | |\/| |/ _ \ / _` ||_|| |/ -_) \__ \ |  _|/ _` || ||  _|
 * |_|  |_|\___/ \__,_| \__/ \___|  |___/ |_|  \__,_|\__|\__|
```

**Plain text (no comment prefix):**
```
<figlet>Plain ASCII Art</figlet>
```
Outputs raw ASCII art without formatting.

## Font Selection

### Default Font

If no font is specified, 'standard' is used:
```
<figlet>Default Font Example</figlet>
```

### Custom Fonts

Specify any of 400+ available fonts:
```
<figlet font="Block">Bold Text</figlet>
<figlet font="3-D">3D Effect</figlet>
<figlet font="Shadow">Shadowed</figlet>
```

### Finding Fonts

When user requests to list available fonts, run the font discovery script to show:
- Previews of the first 10 fonts with examples
- Complete alphabetical listing of all 400+ fonts
- Font names for use in tags

Popular fonts:
- standard (default)
- 3-D
- Block
- Big
- Shadow
- Slant
- Graffiti
- Doom

## Error Handling

The skill validates fonts before processing:
- **Invalid font specified**: Error immediately with font name and suggestion to list available fonts
- **File not found**: Error with file path
- **Node.js/npm issues**: Error with installation instructions

## Bundled Resources

### scripts/

**process-file.js**
- Main processing script that reads files, finds all `<figlet>` tags, validates fonts, generates ASCII art, detects comment styles, and writes results
- Handles automatic Node.js verification and npm dependency installation on first run
- Usage: `node process-file.js <file-path>`

**list-fonts.js**
- Displays all available figlet fonts with previews and complete listing
- Helps users find the exact font names to use in tags
- Usage: `node list-fonts.js`

**package.json**
- Node.js project file with figlet v1.7.0+ dependency

**.gitignore**
- Excludes node_modules from version control

### references/

**usage-guide.md** - Comprehensive reference documentation for all features and edge cases

## Technical Details

- **Node.js Requirement**: v14 or higher
- **Figlet Package**: v1.7.0 or higher (auto-installed on first use)
- **Tag Format**: `<figlet font="font-name">text</figlet>` or `<figlet>text</figlet>`
- **Comment Styles Supported**: //, #, --, /*, or none
- **Default Font**: standard
- **File Processing**: In-place modification
