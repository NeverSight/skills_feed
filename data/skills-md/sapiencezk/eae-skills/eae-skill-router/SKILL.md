---
name: eae-skill-router
description: >
  Router for EAE IEC 61499 skills. Routes to specialized subskills for CAT,
  Basic, Composite, DataType, and Adapter blocks.
license: MIT
compatibility: Designed for EcoStruxure Automation Expert, Python 3.8+, PowerShell (Windows)
metadata:
  version: "5.0.0"
  author: Claude
  domain: industrial-automation
  platform: EcoStruxure Automation Expert
  user-invocable: true
  standard: IEC-61499
---
# EAE Skills Router

Router skill for EAE (EcoStruxure Automation Expert) development.

> **CRITICAL RULE - NEVER BYPASS SKILLS:**
> - **ALWAYS** use an EAE skill for ANY operation on EAE files (`.fbt`, `.adp`, `.dt`, `.cfg`, `.dfbproj`, etc.)
> - This applies to **BOTH creating AND modifying** existing blocks
> - **NEVER** directly read, edit, or write EAE files outside of a skill context
> - When modifying an existing block, invoke the appropriate skill with the modification request
> - The skill will handle reading, validating, and updating all related files correctly

## What Are You Doing?

| Action | Use This Skill |
|--------|----------------|
| Create OR modify a CAT block | `/eae-cat` |
| Create OR modify a Basic FB | `/eae-basic-fb` |
| Create OR modify a Composite FB | `/eae-composite-fb` |
| Create OR modify a DataType | `/eae-datatype` |
| Create OR modify an Adapter | `/eae-adapter` |
| **Fork block from SE library to custom library** | `/eae-fork` |
| Find/use Runtime.Base standard blocks | `/eae-runtime-base` |
| Find/use SE process blocks (motors, valves, PID) | `/eae-se-process` |
| **Analyze project overview, quality, protocols** | `/eae-sln-overview` |
| Validate naming conventions | `/eae-naming-validator` |
| Analyze performance/event storms | `/eae-performance-analyzer` |

## What Are You Creating?

| Need | Block Type | Use This Skill |
|------|------------|----------------|
| Full-featured block with HMI + OPC-UA + persistence | **CAT Block** | `/eae-cat` |
| State machine with algorithms (ST code) | Basic FB | `/eae-basic-fb` |
| Network of existing FBs wired together | Composite FB | `/eae-composite-fb` |
| Custom data structure (struct/enum/array) | DataType | `/eae-datatype` |
| Reusable bidirectional interface | Adapter | `/eae-adapter` |

## Quick Decision Tree

```
What are you doing?
│
├── Forking/copying block from SE library to custom library?
│   └── YES → /eae-fork (handles namespace migration)
│
├── Creating a NEW block from scratch?
│   │
│   ├── Full block with HMI visualization, OPC-UA, or persistence?
│   │   └── YES → /eae-cat (most common)
│   │
│   ├── Need algorithms or state logic?
│   │   └── YES → /eae-basic-fb
│   │
│   ├── Composing existing FBs together (no HMI)?
│   │   └── YES → /eae-composite-fb
│   │
│   ├── Custom data type (enum, struct, array)?
│   │   └── YES → /eae-datatype
│   │
│   └── Reusable interface pattern (socket/plug)?
│       └── YES → /eae-adapter
│
└── Looking up existing blocks?
    ├── Runtime.Base library → /eae-runtime-base
    └── SE process blocks → /eae-se-process
```

## Triggers

### Block Creation/Modification
- `/eae-cat` - Create CAT block with HMI (most common)
- `/eae-basic-fb` - Create Basic FB
- `/eae-composite-fb` - Create Composite FB
- `/eae-datatype` - Create DataType
- `/eae-adapter` - Create Adapter
- `/eae-fork` - Fork block from SE library to custom library with namespace migration

### Library Reference
- `/eae-runtime-base` - Find/reference Runtime.Base standard library blocks
- `/eae-se-process` - Find/reference SE.App2Base and SE.App2CommonProcess blocks

### Analysis & Validation
- `/eae-sln-overview` - Project overview, quality score, protocols, libraries
- `/eae-naming-validator` - Validate SE naming conventions
- `/eae-performance-analyzer` - Detect event storms, analyze performance

### Router
- `/eae-skill-router` - This router (shows decision tree)

---

## Quick Reference

| Type | Extension | Location | IEC61499Type | Features |
|------|-----------|----------|--------------|----------|
| **CAT** | `.cfg` | `IEC61499/{Name}/` | `CAT` | HMI + OPC-UA + Persistence |
| Basic FB | `.fbt` | `IEC61499/` | `Basic` | ECC + Algorithms |
| Composite FB | `.fbt` | `IEC61499/` | `Composite` | FBNetwork |
| DataType | `.dt` | `IEC61499/DataType/` | `DataType` | Struct/Enum/Array |
| Adapter | `.adp` | `IEC61499/` | `Adapter` | Socket/Plug Interface |

---

## Common Rules

These rules apply to ALL block types. See [common-rules.md](references/common-rules.md) for full details.

### ID Generation

All Events and VarDeclarations need 16-character hex IDs:

```powershell
# Generate GUID for FBType
[guid]::NewGuid()

# Generate hex ID for elements (16 chars)
[guid]::NewGuid().ToString("N").Substring(0,16).ToUpper()
```

### dfbproj Registration

Every block must be registered in the library's `.dfbproj` file:

```xml
<ItemGroup>
  <Compile Include="BlockName.fbt">
    <IEC61499Type>Basic</IEC61499Type>
  </Compile>
</ItemGroup>
```

### Critical XML Rules

| Rule | Applies To |
|------|------------|
| NO `xmlns` on root element | FBType, AdapterType, DataType |
| DOCTYPE must reference correct DTD | All blocks |
| `Format="2.0"` required | Composite FB, CAT FB only |
| GUID required | All except DataType |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `<FBType xmlns=...> was not expected` | Remove `xmlns` attribute from FBType |
| Block not in Solution Explorer | Register in `.dfbproj` file |
| DataType not found | Must be in `DataType/` subfolder with `.dt` extension |
| Adapter won't load | Use `.adp` extension, not `.fbt` |
| CAT block broken | Ensure all files in `{Name}/` subfolder |

---

## Scripts

Helper scripts for agentic operation are in `scripts/`. **These are shared infrastructure used by all child skills.**

### Register Block in dfbproj (Universal)

Register any block type in the library's dfbproj file. **All child skills should use this script.**

```bash
# Register with explicit type
python scripts/register_dfbproj.py MyBlock MyLib --type cat
python scripts/register_dfbproj.py MyBlock MyLib --type composite
python scripts/register_dfbproj.py MyBlock MyLib --type basic
python scripts/register_dfbproj.py MyBlock MyLib --type adapter
python scripts/register_dfbproj.py MyBlock MyLib --type datatype

# Auto-detect type from existing files
python scripts/register_dfbproj.py MyBlock MyLib

# Verify registration
python scripts/register_dfbproj.py MyBlock MyLib --verify

# Dry run (show what would happen)
python scripts/register_dfbproj.py MyBlock MyLib --dry-run

# Output as JSON
python scripts/register_dfbproj.py MyBlock MyLib --json
```

**Supported types:**

| Type | IEC61499Type | Extension | Subfolder |
|------|--------------|-----------|-----------|
| `cat` | CAT | `.fbt` + `.cfg` | `{Name}/` |
| `composite` | Composite | `.fbt` | `{Name}/` |
| `basic` | Basic | `.fbt` | `{Name}/` |
| `adapter` | Adapter | `.adp` | `{Name}/` |
| `datatype` | DataType | `.dt` | `DataType/` |

**Exit codes:**
- `0` - Registration successful
- `1` - General error
- `11` - Registration issue

### Generate IDs

Generate GUIDs and hex IDs for blocks:

```bash
# Generate 1 GUID + 1 hex ID (default)
python scripts/generate_ids.py

# Generate 5 hex IDs for Events/VarDeclarations
python scripts/generate_ids.py --hex 5

# Generate 2 GUIDs for multiple blocks
python scripts/generate_ids.py --guid 2

# Output as JSON for automation
python scripts/generate_ids.py --hex 4 --guid 1 --json
```

### Validate Block

Validate .fbt, .adp, .dt files against EAE rules:

```bash
# Auto-detect block type and validate
python scripts/validate_block.py MyBlock.fbt

# Validate a CAT folder
python scripts/validate_block.py IEC61499/MyCAT/

# Specify block type explicitly
python scripts/validate_block.py --type basic MyBasicFB.fbt

# Output as JSON
python scripts/validate_block.py --json MyBlock.fbt
```

**Exit codes:**
- `0` - Validation passed
- `1` - Error running validation
- `10` - Validation failed (errors found)

### Cross-Validate Consistency

Verify consistency between files on disk and dfbproj registration:

```bash
# Validate a single block
python scripts/validate_consistency.py MyBlock SE.ScadapackWWW

# Validate all blocks in a library
python scripts/validate_consistency.py --all SE.ScadapackWWW

# Show fix commands for issues
python scripts/validate_consistency.py --fix --all SE.ScadapackWWW

# Output as JSON
python scripts/validate_consistency.py --json --all SE.ScadapackWWW

# Specify expected block type
python scripts/validate_consistency.py --type cat MyCAT SE.ScadapackWWW
```

**What it checks:**

| Check | Description |
|-------|-------------|
| Files exist | Required files present for block type |
| Registration | Block registered in dfbproj |
| Type match | File type matches registration type |
| Orphans | Blocks in one location but not other |

**Exit codes:**
- `0` - Validation passed (all consistent)
- `1` - Error running validation
- `10` - Validation failed (inconsistencies found)
- `11` - Registration issues (missing or wrong entries)

### Track Blocks (State Management)

Track blocks created/forked during a session for rollback and audit:

```bash
# Add a block to tracking
python scripts/track_block.py add MyBlock SE.ScadapackWWW --type cat --operation fork --source SE.App2CommonProcess

# Add a created block
python scripts/track_block.py add MyBlock SE.ScadapackWWW --type basic --operation create

# Check block status
python scripts/track_block.py status MyBlock SE.ScadapackWWW

# Update status (e.g., mark as failed)
python scripts/track_block.py update MyBlock SE.ScadapackWWW --status failed --error "Build failed"

# Remove from tracking
python scripts/track_block.py remove MyBlock SE.ScadapackWWW
```

### List Tracked Blocks

View all tracked blocks with filtering:

```bash
# List all tracked blocks
python scripts/list_tracked_blocks.py SE.ScadapackWWW

# Filter by status
python scripts/list_tracked_blocks.py SE.ScadapackWWW --status failed

# Filter by type
python scripts/list_tracked_blocks.py SE.ScadapackWWW --type cat

# Filter by operation
python scripts/list_tracked_blocks.py SE.ScadapackWWW --operation fork

# Show summary only
python scripts/list_tracked_blocks.py SE.ScadapackWWW --summary

# Clear tracking (start fresh)
python scripts/list_tracked_blocks.py SE.ScadapackWWW --clear

# JSON output
python scripts/list_tracked_blocks.py SE.ScadapackWWW --json
```

**Tracking manifest location:** `{Library}/IEC61499/.eae-tracking/manifest.json`

### Rollback Operations

Undo failed or unwanted fork/create operations:

```bash
# Rollback a single block
python scripts/rollback_operation.py MyBlock SE.ScadapackWWW

# Rollback all failed blocks
python scripts/rollback_operation.py --all-failed SE.ScadapackWWW

# Preview without making changes
python scripts/rollback_operation.py --dry-run MyBlock SE.ScadapackWWW

# Skip confirmation prompt
python scripts/rollback_operation.py --force MyBlock SE.ScadapackWWW

# Specify block type if not tracked
python scripts/rollback_operation.py --type cat MyBlock SE.ScadapackWWW

# JSON output
python scripts/rollback_operation.py --json MyBlock SE.ScadapackWWW
```

**What rollback does:**

| Action | Description |
|--------|-------------|
| Delete folders | IEC61499/{Block}/ and HMI/{Block}/ |
| Delete files | For DataTypes: .dt and .doc.xml files |
| Remove dfbproj | Removes ItemGroup entries |
| Remove csproj | For CAT blocks: removes HMI entries |
| Update tracking | Marks block as "rolled_back" |

**Exit codes:**
- `0` - Rollback successful
- `1` - Error
- `10` - Block not found in tracking
- `11` - Rollback partially failed

---

## Related Skills

| Skill | Description |
|-------|-------------|
| [eae-cat](../eae-cat/SKILL.md) | CAT blocks with HMI, OPC-UA, persistence |
| [eae-basic-fb](../eae-basic-fb/SKILL.md) | Basic FB with ECC and algorithms |
| [eae-composite-fb](../eae-composite-fb/SKILL.md) | Composite FB with FBNetwork |
| [eae-datatype](../eae-datatype/SKILL.md) | DataTypes (struct, enum, array, subrange) |
| [eae-adapter](../eae-adapter/SKILL.md) | Adapter interfaces |
| [eae-fork](../eae-fork/SKILL.md) | Fork blocks from SE libraries with namespace migration |
| [eae-runtime-base](../eae-runtime-base/SKILL.md) | Runtime.Base standard library reference |
| [eae-se-process](../eae-se-process/SKILL.md) | SE.App2Base and SE.App2CommonProcess reference |
