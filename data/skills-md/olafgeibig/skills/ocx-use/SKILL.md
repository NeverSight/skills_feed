---
name: ocx-use
description: Use this skill when managing OpenCode extensions with OCX (OpenCode eXtensions). This includes installing components from registries, using Ghost Mode for cross-repository development, auditing changes with SHA-256 verification, managing dependencies, configuring registries, or performing component updates and version management. Invoke for tasks involving ocx init, ocx add, ocx update, ocx diff, ocx ghost, or OCX registry operations.
compatibility: Requires OCX installed and internet access for registry operations
metadata:
  source: https://github.com/olafgeibig/skills
  version: "0.1.0"
---

# OCX Manager

OCX (OpenCode eXtensions) is the package manager for OpenCode components with auditability and dependency resolution.

## Quick Start

**Install and initialize:**
```bash
# Install OCX
curl -fsSL https://ocx.kdco.dev/install.sh | sh

# Initialize project
ocx init

# Add components
ocx add kdco/workspace kdco/agents
```

## Core Commands

**Component Management:**
```bash
# Add components (registry or npm)
ocx add kdco/workspace
ocx add npm:@franlol/opencode-md-table-formatter

# Update components
ocx update kdco/workspace              # Update specific
ocx update --all                       # Update all
ocx update kdco/workspace@1.2.0        # Pin version

# Audit changes
ocx diff                               # Show all changes
ocx diff kdco/workspace               # Specific component
```

**Registry Management:**
```bash
# Add registries
ocx registry add https://registry.kdco.dev --name kdco
ocx registry list

# Search components
ocx search agents                      # Find components
ocx search --installed                 # List installed
```

## Ghost Mode (Cross-Repository Development)

Work in any repository without modifying it:

```bash
# Setup Ghost Mode
ocx ghost init
ocx ghost profile add work

# Configure registries
ocx ghost registry add https://registry.kdco.dev --name kdco
ocx ghost add kdco/workspace kdco/agents

# Use in any project
cd ~/oss/project-name
ocx ghost opencode                     # Run with your config
```

**Profile Management:**
```bash
ocx ghost profile list                 # List profiles
ocx ghost profile use work             # Switch profile
ocx ghost profile add personal         # Create profile
ocx ghost config                       # Edit current profile
```

## Common Workflows

**Development Setup:**
```bash
ocx init
ocx registry add https://registry.kdco.dev --name kdco
ocx add kdco/workspace kdco/agents kdco/skills
ocx search --installed
```

**Audit Workflow:**
```bash
ocx diff                              # Check for changes
# Review changes shown
ocx update kdco/workspace             # Update if needed
ocx diff kdco/workspace              # Verify no changes
```

**Enterprise Setup:**
```bash
# Lock registries and pin versions
# Edit ocx.jsonc:
{
  "registries": {
    "internal": {
      "url": "https://registry.company.com",
      "version": "1.0.0"
    }
  },
  "lockRegistries": true
}
```

## Troubleshooting

**Common Issues:**
- `ocx init` first before adding components
- Check registry URLs with `ocx registry list`
- Use `--force` to overwrite conflicts
- Verify `$EDITOR` is set for `ocx ghost config`

For detailed documentation, see:
- `./reference/ghost-mode-workflows.md` - Advanced Ghost Mode usage
- `./reference/registry-management-guide.md` - Registry configuration
- `./reference/component-types-reference.md` - Component type details
- `./reference/configuration-files-guide.md` - Config file reference