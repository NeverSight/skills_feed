---
name: eae-se-process
description: >
  Reference guide for SE.App2Base and SE.App2CommonProcess libraries in EAE.
  Find and use standard industrial process blocks for motors, valves, PID
  control, signals, and equipment modules.
license: MIT
compatibility: Designed for EcoStruxure Automation Expert 25.0+, Python 3.8+, PowerShell (Windows)
metadata:
  version: "1.0.0"
  author: Claude
  domain: industrial-automation
  parent-skill: eae-skill-router
  user-invocable: true
  platform: EcoStruxure Automation Expert
  standard: IEC-61499
---
# EAE SE Process Libraries Reference

Reference skill for the **SE.App2Base** and **SE.App2CommonProcess** libraries - the standard industrial process control libraries in EcoStruxure Automation Expert.

**These libraries provide:**
- Signal processing (analog/digital I/O)
- Motor and valve control
- PID and process control
- Equipment modules (pumps, flow control)
- Interlocks, failures, permissives
- HMI-ready CATs with faceplates

> **Note:** SE.App2CommonProcess depends on SE.App2Base and Runtime.Base.

## Quick Start

```
User: I need a PID controller block
Claude: Use `PID` from SE.App2CommonProcess - a standard PID with auto/manual modes

User: What block handles analog input scaling?
Claude: Use `AnalogInput` CAT or `AISignalScaling` from SE.App2Base
```

## Triggers

- `/eae-se-process`
- "find process block"
- "motor control block"
- "valve control block"
- "PID block"
- "analog input block"
- "SE.App2Base"
- "SE.App2CommonProcess"

---

## Quick Reference by Task

### Signal Processing

| Task | Block | Library | Type |
|------|-------|---------|------|
| Read analog input | `AnalogInput` | SE.App2CommonProcess | CAT |
| Write analog output | `AnalogOutput` | SE.App2CommonProcess | CAT |
| Read digital input | `DigitalInput` | SE.App2CommonProcess | CAT |
| Write digital output | `DigitalOutput` | SE.App2CommonProcess | CAT |
| Scale analog signal | `AISignalScaling` | SE.App2Base | CAT |
| Totalize flow | `Total` | SE.App2CommonProcess | CAT |
| Multi-input analog | `MultiAnalogInput` | SE.App2CommonProcess | CAT |

### Motor Control

| Task | Block | Library | Type |
|------|-------|---------|------|
| Single-speed motor | `Motor` | SE.App2CommonProcess | CAT |
| Two-direction motor | `Motor2D` | SE.App2CommonProcess | CAT |
| Two-speed motor | `Motor2S` | SE.App2CommonProcess | CAT |
| Cyclic motor | `MotorCyc` | SE.App2CommonProcess | CAT |
| Variable speed motor | `MotorVs` | SE.App2CommonProcess | CAT |

### Valve Control

| Task | Block | Library | Type |
|------|-------|---------|------|
| On/Off valve | `Valve` | SE.App2CommonProcess | CAT |
| Two-output valve | `Valve2Op` | SE.App2CommonProcess | CAT |
| Control valve (analog) | `ValveControl` | SE.App2CommonProcess | CAT |
| Hand valve (monitor) | `ValveHand` | SE.App2CommonProcess | CAT |
| Motorized valve | `ValveM` | SE.App2CommonProcess | CAT |
| Motorized with position | `ValveMPos` | SE.App2CommonProcess | CAT |

### Process Control

| Task | Block | Library | Type |
|------|-------|---------|------|
| PID control | `PID` | SE.App2CommonProcess | CAT |
| PID with multiplexer | `PIDMultiplexer` | SE.App2CommonProcess | CAT |
| Lead/Lag compensation | `LeadLag` | SE.App2CommonProcess | CAT |
| Ramp generation | `Ramp` | SE.App2CommonProcess | CAT |
| Ratio control | `Ratio` | SE.App2CommonProcess | CAT |
| Split range | `Split2Range` | SE.App2CommonProcess | CAT |
| Step control (3-point) | `Step3` | SE.App2CommonProcess | CAT |
| PWM output | `PWM` | SE.App2CommonProcess | CAT |

### Equipment Modules

| Task | Block | Library | Type |
|------|-------|---------|------|
| Pump management | `PumpSet` | SE.App2CommonProcess | CAT |
| Pump asset | `PumpAssets` | SE.App2CommonProcess | CAT |
| Flow control | `FlowCtl` | SE.App2CommonProcess | CAT |
| Scheduler | `Scheduler` | SE.App2CommonProcess | CAT |

### Common Services

| Task | Block | Library | Type |
|------|-------|---------|------|
| Interlock item | `ilckCondItem` | SE.App2CommonProcess | Composite |
| Interlock summary | `IlckCondSum` | SE.App2CommonProcess | CAT |
| Failure item | `failCondItem` | SE.App2CommonProcess | Composite |
| Failure summary | `FailCondSum` | SE.App2CommonProcess | CAT |
| Permissive item | `permCondItem` | SE.App2CommonProcess | Composite |
| Permissive summary | `PermCondSum` | SE.App2CommonProcess | CAT |
| Preventive maintenance | `DevMnt` | SE.App2CommonProcess | CAT |

### Display/HMI (SE.App2Base)

| Task | Block | Library | Type |
|------|-------|---------|------|
| Display boolean | `DisplayBool` | SE.App2Base | CAT |
| Display integer | `DisplayInt` / `DisplayDint` | SE.App2Base | CAT |
| Display real | `DisplayReal` | SE.App2Base | CAT |
| Display string | `DisplayString` | SE.App2Base | CAT |
| Display time | `DisplayTime` | SE.App2Base | CAT |
| Set boolean | `SetBool` | SE.App2Base | CAT |
| Set integer | `SetInt` / `SetDint` | SE.App2Base | CAT |
| Set real | `SetReal` | SE.App2Base | CAT |
| Set string | `SetString` | SE.App2Base | CAT |
| Set time | `SetTime` | SE.App2Base | CAT |

### Alarms (SE.App2Base)

| Task | Block | Library | Type |
|------|-------|---------|------|
| Limit alarm | `LimitAlarm` | SE.App2Base | CAT |
| Deviation alarm | `DeviationAlarm` | SE.App2Base | CAT |
| Rate of change alarm | `ROCAlarm` | SE.App2Base | CAT |
| State alarm | `StateAlarm` | SE.App2Base | CAT |
| Digital signal alarm | `DiSignalAlarm` | SE.App2Base | CAT |
| Alarm summary | `AlarmSummary` | SE.App2CommonProcess | CAT |

---

## Library Architecture

```
Runtime.Base (IEC 61499 primitives)
    │
    ▼
SE.App2Base (Foundation process library)
    ├── Basic FBs: alarmCalc, counterBasic, modeBase, etc.
    ├── Composites: aISignal, aOSignal, dISignal, dOSignal
    ├── Adapters: IAnalog, IDigital, IDInt, IString, ITime
    ├── DataTypes: Status, OwnerState, ActiveState, etc.
    └── CATs: Display*, Set*, *Alarm, Mode, Owner
    │
    ▼
SE.App2CommonProcess (Application CATs)
    ├── Signal Processing: AnalogInput, DigitalInput, etc.
    ├── Motors: Motor, Motor2D, Motor2S, MotorVs
    ├── Valves: Valve, Valve2Op, ValveControl, ValveM
    ├── Process Control: PID, Ramp, Ratio, LeadLag
    ├── Equipment: PumpSet, FlowCtl, Scheduler
    └── Services: Interlocks, Failures, Permissives
```

---

## Scripts

### Block Lookup

Search SE.App2Base and SE.App2CommonProcess blocks by keyword, category, or list all:

```bash
# Find motor-related blocks
python scripts/lookup_block.py "motor"
# Returns: Motor, Motor2D, Motor2S, MotorCyc, MotorVs, motorLogic, etc.

# Find all PID blocks
python scripts/lookup_block.py "pid"

# Show category with results
python scripts/lookup_block.py "valve" --category

# Show library (App2Base vs App2CommonProcess) with results
python scripts/lookup_block.py "alarm" --library

# List all categories
python scripts/lookup_block.py --list-categories

# List all blocks
python scripts/lookup_block.py --list-all

# JSON output for automation
python scripts/lookup_block.py "analog" --json
```

**Features:**
- Searches block names, descriptions, and keywords
- Covers SE.App2Base (basics, composites, adapters, datatypes, CATs)
- Covers SE.App2CommonProcess (motors, valves, process control, equipment)
- Supports 20+ categories covering 100+ blocks
- JSON output for CI/CD integration

**Exit codes:**
- `0` - Success (matches found or list completed)
- `1` - Error (invalid arguments)
- `2` - No matches found

---

## Common Usage Patterns

See [common-patterns.md](references/common-patterns.md) for detailed patterns:

1. **Basic Analog Input** - AnalogInput with scaling and alarms
2. **Motor with Interlocks** - Motor CAT with ilckCondItem chain
3. **PID Control Loop** - PID with cascade mode
4. **Valve with Permissives** - Valve2Op with permCondItem chain
5. **Equipment Module** - PumpSet with FlowCtl coordination

---

## Key Adapters

### SE.App2Base Adapters

| Adapter | Purpose | Data Flow |
|---------|---------|-----------|
| `IAnalog` | Analog signal interface | Value, Status, Quality |
| `IDigital` | Digital signal interface | State, Status |
| `IDInt` | Integer signal interface | Value, Status |
| `IString` | String signal interface | Value, Status |
| `ITime` | Time signal interface | Value, Status |

### SE.App2CommonProcess Adapters

| Adapter | Purpose | Usage |
|---------|---------|-------|
| `IDevice` | Device command/status | Motor, Valve control |
| `IFailCondSum` | Failure condition chain | Connect failCondItem |
| `IIlckCondSum` | Interlock condition chain | Connect ilckCondItem |
| `IPermCondSum` | Permissive condition chain | Connect permCondItem |
| `ISeqData` | Sequence data interface | Recipe/batch control |
| `ICascadeLoop` | Cascade PID interface | PID cascade mode |

---

## Key DataTypes (SE.App2Base)

| Type | Purpose | Values |
|------|---------|--------|
| `Status` | Signal quality status | Good, Bad, Uncertain |
| `OwnerState` | Owner control state | Manual, Auto, Program |
| `ActiveState` | Active/inactive state | Enum |
| `StateSel` | State selection | Enum |
| `TimeFormat` | Time format selection | Enum |

---

## Namespaces

| Library | Namespace |
|---------|-----------|
| SE.App2Base | `SE.App2Base` |
| SE.App2CommonProcess | `SE.App2CommonProcess` |

**Usage in FBNetwork:**

```xml
<!-- SE.App2Base block -->
<FB ID="1" Name="display" Type="DisplayReal" Namespace="SE.App2Base" x="500" y="350" />

<!-- SE.App2CommonProcess block -->
<FB ID="2" Name="motor" Type="Motor" Namespace="SE.App2CommonProcess" x="1100" y="350" />
```

---

## Related Skills

| Skill | When to Use |
|-------|-------------|
| [eae-runtime-base](../eae-runtime-base/SKILL.md) | Low-level IEC 61499 blocks (E_CYCLE, E_DELAY, MQTT) |
| [eae-cat](../eae-cat/SKILL.md) | Create new CAT blocks |
| [eae-composite-fb](../eae-composite-fb/SKILL.md) | Create composite blocks using SE process blocks |
| [eae-basic-fb](../eae-basic-fb/SKILL.md) | Create custom logic blocks |
| [eae-datatype](../eae-datatype/SKILL.md) | Create custom data types |

---

## References

- [Block Catalog](references/block-catalog.md) - Complete categorized block list
- [Common Patterns](references/common-patterns.md) - Usage patterns and examples
- [DataTypes Reference](references/datatypes.md) - SE.App2Base data types
