---
name: eae-sln-overview
description: >
  Explores EAE projects and generates comprehensive summary reports including
  network architecture, protocols, libraries, I/O counts, ISA88 hierarchy,
  project description, and quality rating. Supports multiple output formats.
license: MIT
compatibility: Designed for EcoStruxure Automation Expert 24.0+, Python 3.8+
metadata:
  version: "1.1.0"
  author: Claude
  domain: industrial-automation
  platform: EcoStruxure Automation Expert
  parent-skill: eae-skill-router
  user-invocable: true
  standard: IEC-61499
---

# EAE Solution Overview

Analyzes EcoStruxure Automation Expert (EAE) projects and generates comprehensive reports.

## Quick Start

```bash
# Basic analysis - generates markdown report
python scripts/analyze_project.py --project-dir /path/to/project

# JSON output for automation
python scripts/analyze_project.py --project-dir /path/to/project --json

# Quick summary
python scripts/analyze_project.py --project-dir /path/to/project --format summary

# Save report to file
python scripts/analyze_project.py --project-dir /path/to/project --output report.md
```

## Triggers

Use this skill when:
- "analyze EAE project"
- "generate project report"
- "project overview"
- "solution summary"
- "show project quality"
- "what's in this EAE project"
- `/eae-sln-overview`

## Quick Reference

| Analysis | Description | Script |
|----------|-------------|--------|
| Solution | Projects, blocks, library refs, EAE version | `parse_solution.py` |
| Topology | Devices, resources, CAT instances | `parse_system_topology.py` |
| Protocols | OPC-UA, Modbus, EtherNet/IP, IO-Link | `parse_protocols.py` |
| Libraries | SE vs custom, dependencies | `parse_libraries.py` |
| I/O | Event/data inputs/outputs | `count_io.py` |
| ISA88 | System/subsystem hierarchy | `parse_isa88.py` |
| Description | Project description (docs or inferred) | `parse_description.py` |
| Quality | 8-dimension scoring | `calculate_quality.py` |

## Report Sections

### 1. Executive Summary

Quick metrics table with quality score, project count, device count, blocks, and I/O points.

### 2. Network Architecture

ASCII diagram showing device topology with:
- Device names and types
- Resource counts
- CAT instance counts

### 3. Protocol Inventory

| Protocol | What's Detected |
|----------|-----------------|
| OPC-UA Server | Exposed node count, over-exposure warnings |
| OPC-UA Client | Cross-device connections |
| Modbus TCP/RTU | Masters and slaves |
| EtherNet/IP | Scanner instances |
| Other | DNP3, PROFINET, IO-Link, etc. |

### 4. Library Matrix

- **SE Standard Libraries**: Runtime.Base, SE.App2CommonProcess, etc.
- **Custom Libraries**: Project-specific namespaces with dependencies

### 5. I/O Summary

| Category | Description |
|----------|-------------|
| Event Inputs | INIT, REQ, etc. |
| Event Outputs | INITO, CNF, etc. |
| Data Inputs | Interface variables (inputs) |
| Data Outputs | Interface variables (outputs) |
| Internal Vars | Private variables |
| Adapters | Socket/Plug connections |

### 6. ISA88 Hierarchy

System/Subsystem hierarchy from System.sys:
```
System: System
  +-- Subsystem: JetMix (JetMix)
      +-- Equipment modules...
  +-- Subsystem: JetSpray (JetSpray)
      +-- Equipment modules...
```

Parsed from `Device.FolderPath` attribute and CAT instances in System.sys.

### 7. Quality Score

8-dimension scoring system (100 points total):

| Dimension | Max | Description |
|-----------|-----|-------------|
| Naming Compliance | 20 | SE naming convention adherence |
| Library Organization | 15 | SE/custom separation, dependencies |
| Documentation | 15 | .doc.xml coverage, comments |
| ISA88 Hierarchy | 15 | Asset structure and CAT linking |
| Protocol Config | 10 | OPC-UA exposure, clean configs |
| Code Organization | 10 | Folder structure, consistency |
| Block Complexity | 10 | Variable counts, event fanout |
| Reusability | 5 | Adapter usage, composition |

**Grades**: A (90+), B (80-89), C (70-79), D (60-69), F (<60)

## Commands

### Main Orchestrator

```bash
python scripts/analyze_project.py --project-dir PATH [OPTIONS]

Options:
  --project-dir PATH    EAE project root directory (required)
  --format FORMAT       Output: markdown, json, summary (default: markdown)
  --output PATH         Write to file instead of stdout
  --json                Shortcut for --format json
```

### Individual Scripts

Run individual analysis modules for targeted inspection:

```bash
# Solution structure
python scripts/parse_solution.py --project-dir PATH [--json]

# System topology
python scripts/parse_system_topology.py --project-dir PATH [--json]

# Protocol detection
python scripts/parse_protocols.py --project-dir PATH [--json]

# Library analysis
python scripts/parse_libraries.py --project-dir PATH [--json]

# I/O counting
python scripts/count_io.py --project-dir PATH [--json] [--details]

# ISA88 hierarchy
python scripts/parse_isa88.py --project-dir PATH [--json]

# Project description
python scripts/parse_description.py --project-dir PATH [--json]

# Quality scoring
python scripts/calculate_quality.py --project-dir PATH [--json]
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Analysis complete, quality >= 70% |
| 1 | Error (project not found, critical failure) |
| 10 | Analysis complete with warnings, or quality 50-69% |
| 11 | Analysis complete, quality < 50% |

## Output Formats

### Markdown (default)

Full report with tables, ASCII diagrams, and formatted sections. Best for documentation.

### JSON

Structured data for automation and integration:

```json
{
  "project_dir": "/path/to/project",
  "analyzed_at": "2024-01-15T10:30:00",
  "solution": { ... },
  "topology": { ... },
  "protocols": { ... },
  "libraries": { ... },
  "io": { ... },
  "isa88": { ... },
  "quality": { ... }
}
```

### Summary

One-line-per-metric quick overview:

```
Project: MyProject
Description: MyProject is an IEC 61499 automation project for food and beverage processing.
EAE Version: 24.0.0.0
Quality: 75/100 (Grade C)
Projects: 3
Blocks: 250
I/O Points: 8,287
SE Libraries (16): Runtime.Base, SE.AppBase, ...
Custom Libraries (3): MyLib.IoLink, ...
Protocols: OPC-UA (0 refs), Modbus (334 refs), EtherNet/IP (1475 refs)
System: System
Subsystems (4): JetMix, JetSpray, JetFlam, Ligne
Equipment Modules: 114
```

## Project Locations

Default EAE project locations:

- `C:\Users\{user}\Documents\Schneider Electric\EcoStruxureAutomationExpertProjects`
- `C:\Users\{user}\Documents\GitHub`

## Files Analyzed

| Pattern | Purpose |
|---------|---------|
| `*.sln`, `*.nxtsln` | Solution structure |
| `*.dfbproj` | Project metadata, library refs, EAE version |
| `*.fbt` | Function blocks (interfaces) |
| `*.adp` | Adapters |
| `*.dt` | Data types |
| `System.cfg`, `System.sys` | Topology, CAT instances, ISA88 hierarchy |
| `*.opcua.xml` | OPC-UA server configuration |
| `*.hcf` | Hardware configuration (protocol detection) |
| `*.doc.xml` | Documentation (description extraction) |
| `Folders.xml` | Code organization |
| `README.md` | Project documentation |

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| `eae-naming-validator` | Quality scoring uses naming patterns |
| `eae-performance-analyzer` | Can be run after overview for deep analysis |
| `eae-skill-router` | Parent skill for routing |

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Analyzing without reading | May miss context | Review report sections |
| Ignoring quality warnings | Technical debt | Address recommendations |
| Over-exposed OPC-UA | Security risk | Review exposed nodes |
| Empty ISA88 | Missing asset management | Configure hierarchy |

## Verification

After running analysis:

- [ ] Quality score calculated (not error)
- [ ] All 8 analysis sections present (solution, topology, protocols, libraries, io, isa88, description, quality)
- [ ] No critical warnings
- [ ] Library list includes SE and custom libraries
- [ ] Protocol detection shows expected communication types
- [ ] ISA88 subsystems match expected configuration

## Troubleshooting

### "Project directory not found"

Ensure the path points to the root containing `.sln` or `IEC61499/` folder.

### "No .dfbproj files found"

The project may not be an IEC61499 project or may have a non-standard structure.

### "System directory not found"

The project doesn't have a configured system topology yet. This is normal for library-only projects.

### "No subsystems found"

ISA88 hierarchy is not configured in System.sys. Ensure Device.FolderPath is defined with subsystem names.

---

## Changelog

### v1.1.0
- Added `parse_description.py` - hybrid description generation (docs + metadata inference)
- Enhanced protocol detection from .hcf files and library references
- Added EAE version detection from .dfbproj files
- Fixed ISA88 parsing to use System.sys instead of Assets.json
- Improved custom library detection via ProjectReference elements
- Added compatibility field to frontmatter

### v1.0.0
- Initial release
- 7 analysis modules
- 8-dimension quality scoring
- Markdown, JSON, summary output formats
- ASCII network diagrams
