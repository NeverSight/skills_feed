---
name: coco-cli
description: ODB++ PCB design file analysis CLI. Query layers/nets/components, measure feature distances, analyze net clearances, render PNG images.
license: LicenseRef-Proprietary
compatibility: Requires coco CLI binary. Supports Windows, macOS, Linux.
metadata:
  author: Pentacube
  version: "0.1.0"
---

# coco CLI

Command-line tool for analyzing ODB++ PCB design files.

## When to Use

**Use coco CLI in these situations:**

1. **ODB++ folder detected** - Directory containing `matrix/`, `steps/`, `misc/` folders
2. **PCB-related queries** - Layer, net, component, feature, distance measurement requests
3. **DFM verification** - Clearance checks, short detection, design rule validation
4. **Keywords present** - ODB++, PCB, Gerber, layer, netlist, DRC

## Installation

```bash
# Check installation
coco --help

# If not installed
# Linux/macOS:
./scripts/install.sh
# Windows:
./scripts/install.ps1
```

## ODB++ Folder Identification

ODB++ folders are identified by internal structure (folder name is irrelevant):

```
<any_name>/       <- path for --input
├── matrix/
├── steps/
└── misc/
```

If `matrix/`, `steps/`, `misc/` folders are all present, it's an ODB++ root.

## Command Usage

**IMPORTANT: Always run `--help` first to discover available commands and options:**

```bash
# Discover all commands
coco --help

# Get specific command options (REQUIRED before using any command)
coco <command> --help
```

## Basic Workflow

```bash
# 1. Discover commands
coco --help

# 2. Check command options
coco list-layers --help

# 3. Run with appropriate options
coco list-layers --input <odb_path>
```

## Use Cases

- [DFM Clearance Verification](references/usecase-dfm.md)
- [Net Analysis](references/usecase-net.md)

## Troubleshooting

| Symptom | Solution |
|---------|----------|
| command not found | Run `scripts/install.sh` |
| step not found | Specify `--step <name>` option |
