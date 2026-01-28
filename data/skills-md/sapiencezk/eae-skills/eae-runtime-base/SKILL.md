---
name: eae-runtime-base
description: >
  Reference guide for Runtime.Base library function blocks in EAE. Helps
  find, understand, and correctly use the ~100 built-in IEC 61499 blocks.
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
# EAE Runtime.Base Library Reference

Reference guide for the **Runtime.Base** standard library - ~100 built-in IEC 61499 function blocks for EcoStruxure Automation Expert.

**Use this skill to:**
- Find the right block for a task
- Understand block interfaces (events, inputs, outputs)
- Learn correct usage patterns
- Troubleshoot block behavior

## Quick Start

```
User: I need to delay an event by 5 seconds
Claude: Use E_DELAY - pass T#5s to DT input, trigger START

User: How do I create a cyclic task?
Claude: Use E_CYCLE with DT=T#100ms for 100ms cycle, or E_HRCYCLE for high-resolution

User: What blocks handle MQTT?
Claude: MQTT_CONNECTION (setup), MQTT_PUBLISH, MQTT_SUBSCRIBE
```

## Triggers

- `/eae-runtime-base`
- "which Runtime.Base block"
- "how to use E_DELAY"
- "find block for..."
- "Runtime.Base reference"
- "standard library block"

---

## Library Categories

| Category | Count | Purpose |
|----------|-------|---------|
| **Basics** | 14 | Event routing primitives (split, merge, select, permit) |
| **Composites** | 2 | Trigger detection (rising/falling edge) |
| **Services** | 80+ | Timers, math, logic, communication, data handling |
| **Resources** | 2 | Embedded resource types |

---

## Quick Reference by Task

### Event Flow Control

| Block | Purpose | Key Inputs |
|-------|---------|------------|
| `E_SPLIT` | 1 event → 2 outputs | EI → EO1, EO2 |
| `E_MERGE` | 2 events → 1 output | EI1, EI2 → EO |
| `E_SELECT` | Route by boolean | G (guard), EI0, EI1 → EO |
| `E_SWITCH` | Boolean switch | G, EI → EO0, EO1 |
| `E_PERMIT` | Gate events | PERMIT, EI → EO |
| `E_DEMUX` | 1 event → N outputs | K (index), EI → EO0..EOn |
| `E_REND` | Rendezvous (sync) | EI1, EI2, R → EO |

### Timing

| Block | Purpose | Key Inputs |
|-------|---------|------------|
| `E_CYCLE` | Periodic events | DT (period) → EO every DT |
| `E_HRCYCLE` | High-res periodic | DT, PHASE → EO |
| `E_DELAY` | Delay single event | DT, START → EO after DT |
| `E_DELAYR` | Retriggerable delay | DT, START → EO |
| `E_TRAIN` | Event train/burst | DT, N → N events at DT |
| `E_TABLE` | Scheduled sequence | DT[], START → EO at times |

### Edge Detection

| Block | Purpose | Interface |
|-------|---------|-----------|
| `E_R_TRIG` | Rising edge | EI, QI → EO when FALSE→TRUE |
| `E_F_TRIG` | Falling edge | EI, QI → EO when TRUE→FALSE |

### Latches & Flip-Flops

| Block | Purpose | Interface |
|-------|---------|-----------|
| `E_SR` | Set-Reset (S dominant) | S, R → Q |
| `E_RS` | Reset-Set (R dominant) | R, S → Q |
| `E_D_FF` | D Flip-Flop | CLK, D → Q |
| `E_CTU` | Up counter | CU, R, PV → Q, CV |

### Arithmetic

| Block | Purpose | Interface |
|-------|---------|-----------|
| `ADD` | Addition | IN1 + IN2 → OUT |
| `SUB` | Subtraction | IN1 - IN2 → OUT |
| `MUL` | Multiplication | IN1 * IN2 → OUT |
| `DIV` | Division | IN1 / IN2 → OUT |
| `ANAMATH` | Analog math | Multiple operations |
| `CALC_FORMULAR` | Formula evaluation | Expression string |

### Logic

| Block | Purpose | Interface |
|-------|---------|-----------|
| `AND` | Logical AND | IN1, IN2 → OUT |
| `OR` | Logical OR | IN1, IN2 → OUT |
| `NOT` | Logical NOT | IN → OUT |
| `XOR` | Exclusive OR | IN1, IN2 → OUT |
| `COMPARE` | Compare values | IN1, IN2 → LT, EQ, GT |
| `SELECT` | Conditional select | G, IN0, IN1 → OUT |

### Bit Manipulation

| Block | Purpose | Interface |
|-------|---------|-----------|
| `BITMAN` | Bit manipulation | Operations on bits |
| `SHL` | Shift left | IN, N → OUT |
| `SHR` | Shift right | IN, N → OUT |
| `ROL` | Rotate left | IN, N → OUT |
| `ROR` | Rotate right | IN, N → OUT |

### Communication - MQTT

| Block | Purpose | Key Inputs |
|-------|---------|------------|
| `MQTT_CONNECTION` | Broker connection | ServerURI, ClientID, User, Password |
| `MQTT_PUBLISH` | Publish messages | ConnectionID, Topic, Payload, QoS |
| `MQTT_SUBSCRIBE` | Subscribe to topics | ConnectionID, Topic |

### Communication - Other

| Block | Purpose | Key Inputs |
|-------|---------|------------|
| `WEBSOCKET_SERVER` | WebSocket server | Port, Path |
| `NETIO` | Network I/O | IP, Port |
| `SERIALIO` | Serial communication | Port, BaudRate |
| `QUERY_CONNECTION` | HTTP/REST queries | URL, Method |

### Data Handling

| Block | Purpose | Key Inputs |
|-------|---------|------------|
| `BUFFER` | Data buffer | IN → buffered → OUT |
| `BUFFERP` | Persistent buffer | With persistence |
| `ANY2ANY` | Type conversion | IN (any) → OUT (any) |
| `SPLIT` | Split data | IN → OUT1, OUT2 |
| `AGGREGATE` | Combine data | IN1, IN2 → OUT |

### JSON

| Block | Purpose | Interface |
|-------|---------|-----------|
| `JSON_BUILDER` | Build JSON | Key/Value pairs → JSON string |
| `JSON_PARSER` | Parse JSON | JSON string → Values |
| `JSON_FORMAT` | Format JSON | Structured → Formatted |

### Configuration & Parameters

| Block | Purpose | Interface |
|-------|---------|-----------|
| `CFG_ANY_GET` | Get config value | Path → Value |
| `CFG_ANY_SET` | Set config value | Path, Value → OK |
| `CFG_DIRECT_GET` | Direct param read | Address → Value |
| `CFG_DIRECT_SET` | Direct param write | Address, Value → OK |
| `PERSISTENCE` | Persist values | Save/Load from storage |

### Process Data (PD)

| Block | Purpose | Interface |
|-------|---------|-----------|
| `PD_ANY_IN` | Process data input | Address → Value |
| `PD_ANY_OUT` | Process data output | Value → Address |
| `PD_DIRECT_IN` | Direct PD read | Hardware address |
| `PD_DIRECT_OUT` | Direct PD write | Hardware address |
| `PD_COPY` | Copy process data | Source → Destination |

### System & Diagnostics

| Block | Purpose | Interface |
|-------|---------|-----------|
| `LOGGER` | Log messages | Message, Level → Log |
| `SYSLOGLOGGER` | Syslog logging | Remote syslog server |
| `CPUTICK` | CPU tick counter | → TICK (timing) |
| `REPORT_APP_STATE` | Application state | State → HMI/OPC-UA |
| `ALARM_BIT` | Alarm handling | Condition → Alarm |

### Value Encoding

| Block | Purpose | Interface |
|-------|---------|-----------|
| `VTQ_ENCODE` | Value+Time+Quality encode | V, T, Q → VTQ |
| `VTQ_DECODE` | VTQ decode | VTQ → V, T, Q |
| `VALFORMAT` | Format value to string | Value, Format → String |
| `VALSCAN` | Parse string to value | String → Value |

### Resources

| Block | Purpose | Use Case |
|-------|---------|----------|
| `EMB_RES_ECO` | Economy resource | Standard applications |
| `EMB_RES_ENH` | Enhanced resource | High-performance |

---

## Common Patterns

### Pattern 1: Cyclic Execution

```
E_CYCLE (DT=T#100ms)
    └── EO → Your_FB.REQ
```

### Pattern 2: Event Synchronization

```
Source1.CNF ──┐
              ├── E_REND.EI1, EI2 → EO → Next_Step
Source2.CNF ──┘
```

### Pattern 3: Conditional Routing

```
Condition ─── E_SWITCH.G
Event     ─── E_SWITCH.EI
              ├── EO0 (when G=FALSE)
              └── EO1 (when G=TRUE)
```

### Pattern 4: MQTT Publishing

```
MQTT_CONNECTION (ServerURI, ClientID)
    │
    ├── INITO → MQTT_PUBLISH.INIT (ConnectionID)
    │               │
    │               └── INITO → Ready to publish
    │
    └── CONNECTO → Connection established
```

### Pattern 5: Delayed One-Shot

```
Trigger ─── E_DELAY.START (DT=T#5s)
                │
                └── EO → Action (5s later)
```

---

## Block Interface Conventions

All Runtime.Base blocks follow IEC 61499 conventions:

| Element | Convention |
|---------|------------|
| `INIT` | Initialization event input |
| `INITO` | Initialization confirmation output |
| `REQ` | Request event input |
| `CNF` | Confirmation event output |
| `QI` | Input qualifier (BOOL) |
| `QO` | Output qualifier (BOOL) |
| `STATUS` | Status string output |

---

## Scripts

### Block Lookup

Search Runtime.Base blocks by keyword, category, or list all:

```bash
# Search for blocks matching keyword
python scripts/lookup_block.py "delay"
# Returns: E_DELAY, E_DELAYR

# Show categories with search results
python scripts/lookup_block.py "mqtt" --category
# Returns: MQTT_CONNECTION, MQTT_PUBLISH, MQTT_SUBSCRIBE [MQTT]

# List all block categories
python scripts/lookup_block.py --list-categories

# List all blocks
python scripts/lookup_block.py --list-all

# JSON output for automation
python scripts/lookup_block.py "timer" --json
```

**Features:**
- Searches block names, descriptions, and keywords
- Supports 17 categories covering ~100 blocks
- JSON output for CI/CD integration

**Exit codes:**
- `0` - Success (matches found or list completed)
- `1` - Error (invalid arguments)
- `2` - No matches found

---

## Troubleshooting

| Issue | Check |
|-------|-------|
| Block not firing | Verify input events are connected |
| E_CYCLE not running | START event must be triggered |
| MQTT not connecting | Check ServerURI format, credentials |
| Timer drift | Use E_HRCYCLE for precision |
| Data not updating | Check `With` associations in events |

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| `eae-se-process` | Higher-level process blocks (motors, valves, PID) built on Runtime.Base |
| `eae-basic-fb` | Create custom Basic FBs |
| `eae-composite-fb` | Create Composite FBs using these blocks |
| `eae-cat` | Create CAT blocks |
| `eae-skill-router` | Main EAE skill router |

---

## References

- [Block Catalog](references/block-catalog.md) - Complete block listing with details
- [Common Patterns](references/common-patterns.md) - Usage patterns and examples

---

## Extension Points

1. Add new blocks as Runtime.Base library expands
2. Create domain-specific pattern guides (MQTT, timers, etc.)
3. Add troubleshooting flowcharts for common issues
