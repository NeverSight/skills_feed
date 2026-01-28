---
name: eae-composite-fb
description: >
  Create Composite Function Blocks in EAE with FBNetwork containing
  interconnected FB instances.
license: MIT
compatibility: Designed for EcoStruxure Automation Expert 25.0+, Python 3.8+, PowerShell (Windows)
metadata:
  version: "2.0.0"
  author: Claude
  domain: industrial-automation
  parent-skill: eae-skill-router
  user-invocable: true
  platform: EcoStruxure Automation Expert
  standard: IEC-61499
---
# EAE Composite Function Block Creation

Create or modify Composite FBs that wire together existing function blocks.

> **CRITICAL RULE:** ALWAYS use this skill for ANY operation on Composite FB files.
> - Creating new Composite FBs
> - Modifying existing Composite FBs (adding events, variables, FB instances, connections)
> - NEVER directly edit `.fbt` files outside of this skill

**Composite FB = Network of FBs**
- Contains FB instances wired together
- No algorithms (logic is in child FBs)
- Has `Format="2.0"` attribute

> **Note:** For blocks that need HMI visualization, use `/eae-cat` instead.

> **Tip:** Need standard blocks like E_CYCLE, E_DELAY, or MQTT? Use `/eae-runtime-base` to find the right Runtime.Base block.

## Quick Start

```
User: Create a Composite FB called Calculator that chains two Multiplier blocks
Claude: [Creates .fbt with FBNetwork containing FB1 → FB2]
```

## Triggers

- `/eae-composite-fb`
- `/eae-composite-fb --register-only` - Register existing Composite FB (used by eae-fork orchestration)
- "create composite FB"
- "modify composite FB"
- "add event to composite"
- "add FB instance"
- "add connection"
- "create block with FBNetwork"
- "compose existing blocks"

---

## Register-Only Mode (for eae-fork Orchestration)

When called with `--register-only`, this skill skips file creation and only performs dfbproj registration. This mode is used by **eae-fork** to complete the fork workflow after file transformation.

```
/eae-composite-fb --register-only {BlockName} {Namespace}
```

**What --register-only does:**

1. **Registers in dfbproj** - Adds ItemGroup entries for Composite FB visibility

**What --register-only does NOT do:**

- Create IEC61499 files (.fbt, etc.) - already done by eae-fork
- Update namespaces - already done by eae-fork

### Usage

```bash
# Register a forked Composite FB
python ../eae-skill-router/scripts/register_dfbproj.py MyComposite SE.ScadapackWWW --type composite

# Verify registration
python ../eae-skill-router/scripts/register_dfbproj.py MyComposite SE.ScadapackWWW --type composite --verify
```

---

## Modification Workflow

When modifying an existing Composite FB:

1. Read the existing `.fbt` file to understand current structure
2. Identify what needs to be added/changed
3. Generate new hex IDs for any new Events or VarDeclarations
4. Update the InterfaceList (events, variables) if needed
5. Update the FBNetwork:
   - Add new Input/Output pins for new interface elements
   - Add new FB instances if needed
   - Add new EventConnections
   - Add new DataConnections
6. Position new elements following layout guidelines

---

## Files Generated

| File | Purpose |
|------|---------|
| `{Name}.fbt` | Main block with FBNetwork |
| `{Name}.doc.xml` | Documentation |
| `{Name}.meta.xml` | Metadata |
| `{Name}.composite.offline.xml` | Offline parameter config |

Location: `IEC61499/`

---

## Workflow

1. Generate GUID for FBType
2. Generate hex IDs for each Event and VarDeclaration
3. Create `.fbt` with:
   - `<!DOCTYPE FBType SYSTEM "../LibraryElement.dtd">`
   - **`Format="2.0"`** attribute
   - `<Identification Standard="61499-2" />`
   - `<FBNetwork>` with FB instances and connections
4. Create `.doc.xml`, `.meta.xml`, `.composite.offline.xml`
5. Register in `.dfbproj`

---

## Composite FB Template

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE FBType SYSTEM "../LibraryElement.dtd">
<FBType Name="{BlockName}" Namespace="{YourNamespace}" Format="2.0"
        GUID="{NEW-GUID}" Comment="{Description}">
  <Attribute Name="Configuration.FB.IDCounter" Value="10" />
  <Identification Standard="61499-2" />
  <VersionInfo Organization="{Org}" Version="0.0" Author="{Author}"
               Date="{MM/DD/YYYY}" Remarks="Initial version" />
  <InterfaceList>
    <EventInputs>
      <Event Name="INIT" Comment="Initialization Request">
        <With Var="QI" />
      </Event>
      <Event Name="REQ" Comment="Normal Execution Request">
        <With Var="QI" />
      </Event>
    </EventInputs>
    <EventOutputs>
      <Event Name="INITO" Comment="Initialization Confirm">
        <With Var="QO" />
      </Event>
      <Event Name="CNF" Comment="Execution Confirmation">
        <With Var="QO" />
      </Event>
    </EventOutputs>
    <InputVars>
      <VarDeclaration ID="{HEX-ID}" Name="QI" Type="BOOL"
                      Comment="Input event qualifier" />
    </InputVars>
    <OutputVars>
      <VarDeclaration ID="{HEX-ID}" Name="QO" Type="BOOL"
                      Comment="Output event qualifier" />
    </OutputVars>
  </InterfaceList>
  <FBNetwork>
    <!-- FB instances, inputs, outputs, connections -->
  </FBNetwork>
</FBType>
```

**Important:** Composite FB MUST have `Format="2.0"` attribute.

---

## FBNetwork Layout Guidelines

Follow these guidelines for clean, readable layouts in EAE.

### Core Principles

1. **Position inputs close to their target FB** - Don't stack all inputs on the left. Place inputs near the FB they connect to.

2. **Give FBs enough horizontal space** - FBs need room for connection routing. Use ~1000+ units between FBs, not 400.

3. **Align vertically with FB ports** - Events and data should align with the FB's event and data port sections.

4. **Minimize connection crossings** - Position elements to create clean, parallel connection lines.

5. **Group related elements** - Keep events together, keep data together, with visual separation between groups.

### Input Positioning

| Input Type | Guideline |
|------------|-----------|
| Connects to **first FB** | Place on left edge (x ≈ 100) |
| Connects to **middle/later FB** | Place between FBs, near target |
| Connects to **multiple FBs** | Place on left, use cross-reference connections |

### Vertical Organization

```
┌─────────────────────────────────────────────────────────┐
│  EVENTS (top)     - INIT, REQ aligned with FB events    │
├─────────────────────────────────────────────────────────┤
│  FB INSTANCES     - Centered vertically                 │
├─────────────────────────────────────────────────────────┤
│  DATA (bottom)    - QI, Values aligned with FB data     │
└─────────────────────────────────────────────────────────┘
```

### Spacing Guidelines

| Element | Guideline |
|---------|-----------|
| Between FBs (horizontal) | ~1000-1200 units for routing space |
| Between events (vertical) | ~60 units |
| Between data vars (vertical) | ~60-80 units |
| Gap between events and data | ~150-200 units |
| Output margin from last FB | ~400-500 units |

### Reference Example

See [TestComposite.fbt](../../../src/TestProject/Test.MyBlocks/IEC61499/TestComposite.fbt) for a well-laid-out example with:
- 2 chained FBs with proper spacing
- Inputs positioned near their target FBs
- Clean connection routing

---

## FBNetwork Elements

### FB Instances

```xml
<FB ID="1" Name="Calc1" Type="Calculator" x="720" y="360" Namespace="MyLib" />
<FB ID="2" Name="Calc2" Type="Calculator" x="1820" y="360" Namespace="MyLib" />
```

### Input/Output Pins

```xml
<Input Name="INIT" x="100" y="372" Type="Event" />
<Input Name="REQ" x="100" y="432" Type="Event" />
<Input Name="QI" x="100" y="498" Type="Data" />
<Input Name="Value1" x="100" y="672" Type="Data" />

<Output Name="INITO" x="2300" y="372" Type="Event" />
<Output Name="CNF" x="2300" y="432" Type="Event" />
<Output Name="QO" x="2300" y="632" Type="Data" />
<Output Name="Result" x="2300" y="692" Type="Data" />
```

### Event Connections

Connect events using `$` prefix for composite interface, `$N.` for FB instances:

```xml
<EventConnections>
  <!-- External to FB1 -->
  <Connection Source="$INIT" Destination="$1.INIT" />
  <Connection Source="$REQ" Destination="$1.REQ" />

  <!-- FB1 to FB2 (chaining) -->
  <Connection Source="$1.CNF" Destination="$2.REQ" />

  <!-- FB2 to External -->
  <Connection Source="$2.CNF" Destination="$CNF" />
</EventConnections>
```

### Data Connections

```xml
<DataConnections>
  <!-- External to FB1 -->
  <Connection Source="$QI" Destination="$1.QI" dx1="120" />
  <Connection Source="$Value1" Destination="$1.Value1" />

  <!-- FB1 output to FB2 input -->
  <Connection Source="$1.Result" Destination="$2.Value1" />

  <!-- FB2 to External -->
  <Connection Source="$2.Result" Destination="$Result" />
</DataConnections>
```

### Cross-Reference Connections

When a single input connects to multiple FBs:

```xml
<Connection Source="$QI" Destination="$2.QI" dx1="555.2084">
  <Attribute Name="Configuration.Connections.CrossReference" Value="True" />
</Connection>
```

---

## Connection Syntax

| Pattern | Meaning |
|---------|---------|
| `$INIT` | Composite's INIT input event |
| `$QI` | Composite's QI input variable |
| `$1.INIT` | FB instance 1's INIT event (by ID) |
| `$1.QI` | FB instance 1's QI variable |
| `$Calc1.INIT` | FB instance by name (also works) |

**Recommendation:** Use IDs (`$1.`, `$2.`) for consistency.

---

## Common Runtime.Base Blocks

When building Composite FBs, these standard blocks are frequently used. Use `/eae-runtime-base` for full documentation.

### Timing

| Block | Purpose | Usage |
|-------|---------|-------|
| `E_CYCLE` | Periodic events | `DT=T#100ms` → EO every 100ms |
| `E_DELAY` | Delayed event | `DT=T#5s`, START → EO after 5s |
| `E_HRCYCLE` | High-res timing | For precision timing with phase |

### Event Routing

| Block | Purpose | Usage |
|-------|---------|-------|
| `E_SPLIT` | 1 event → 2 | Fan out events |
| `E_MERGE` | 2 events → 1 | Combine event sources |
| `E_REND` | Synchronize | Wait for both EI1 and EI2 |
| `E_SWITCH` | Conditional | Route by boolean G |
| `E_PERMIT` | Gate events | Only pass when PERMIT=TRUE |

### Edge Detection

| Block | Purpose | Usage |
|-------|---------|-------|
| `E_R_TRIG` | Rising edge | Detect FALSE→TRUE |
| `E_F_TRIG` | Falling edge | Detect TRUE→FALSE |

### Example: Cyclic Composite

```xml
<!-- Add E_CYCLE from Runtime.Base to make composite run periodically -->
<FB ID="1" Name="timer" Type="E_CYCLE" Namespace="Runtime.Base" x="500" y="350" />
<FB ID="2" Name="logic" Type="MyLogicFB" Namespace="MyLib" x="1100" y="350" />

<EventConnections>
  <Connection Source="$INIT" Destination="$1.START" />
  <Connection Source="$1.EO" Destination="$2.REQ" />
</EventConnections>
<DataConnections>
  <Connection Source="T#100ms" Destination="$1.DT" />
</DataConnections>
```

> For the complete catalog of ~100 Runtime.Base blocks, see `/eae-runtime-base`.

---

## dfbproj Registration

```xml
<ItemGroup>
  <None Include="{Name}.doc.xml">
    <DependentUpon>{Name}.fbt</DependentUpon>
  </None>
  <None Include="{Name}.meta.xml">
    <DependentUpon>{Name}.fbt</DependentUpon>
  </None>
  <None Include="{Name}.composite.offline.xml">
    <DependentUpon>{Name}.fbt</DependentUpon>
  </None>
</ItemGroup>
<ItemGroup>
  <Compile Include="{Name}.fbt">
    <IEC61499Type>Composite</IEC61499Type>
  </Compile>
</ItemGroup>
```

---

## Common Rules

See [common-rules.md](../eae-skill-router/references/common-rules.md) for:
- ID generation
- DOCTYPE references
- dfbproj registration patterns

---

## Example: Chained Calculators

```xml
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE FBType SYSTEM "../LibraryElement.dtd">
<FBType GUID="ce04221d-d92f-44d7-aa4f-e2de60c36165" Name="ChainedCalc"
        Format="2.0" Comment="Two calculators chained" Namespace="MyLib">
  <Attribute Name="Configuration.FB.IDCounter" Value="10" />
  <Identification Standard="61499-2" />
  <VersionInfo Organization="MyOrg" Version="1.0" Author="Claude"
               Date="01/16/2026" Remarks="Initial" />
  <InterfaceList>
    <EventInputs>
      <Event Name="INIT"><With Var="QI" /></Event>
      <Event Name="REQ">
        <With Var="QI" /><With Var="A" /><With Var="B" /><With Var="C" />
      </Event>
    </EventInputs>
    <EventOutputs>
      <Event Name="INITO"><With Var="QO" /></Event>
      <Event Name="CNF"><With Var="QO" /><With Var="Result" /></Event>
    </EventOutputs>
    <InputVars>
      <VarDeclaration ID="64257C7C336B4CD7" Name="QI" Type="BOOL" />
      <VarDeclaration ID="85CCBD5763374CD5" Name="A" Type="REAL" />
      <VarDeclaration ID="D6B7E7BEB50D434B" Name="B" Type="REAL" />
      <VarDeclaration ID="573F800297694CAB" Name="C" Type="REAL" />
    </InputVars>
    <OutputVars>
      <VarDeclaration ID="C159DF3BBE7745AC" Name="QO" Type="BOOL" />
      <VarDeclaration ID="2AAED22B103B4FE6" Name="Result" Type="REAL" />
    </OutputVars>
  </InterfaceList>
  <FBNetwork>
    <FB ID="1" Name="Calc1" Type="Multiplier" x="720" y="360" Namespace="MyLib" />
    <FB ID="2" Name="Calc2" Type="Multiplier" x="1820" y="360" Namespace="MyLib" />

    <Input Name="INIT" x="100" y="372" Type="Event" />
    <Input Name="REQ" x="100" y="432" Type="Event" />
    <Input Name="QI" x="100" y="498" Type="Data" />
    <Input Name="A" x="100" y="672" Type="Data" />
    <Input Name="B" x="100" y="752" Type="Data" />
    <Input Name="C" x="1180" y="752" Type="Data" />

    <Output Name="INITO" x="2300" y="372" Type="Event" />
    <Output Name="CNF" x="2300" y="432" Type="Event" />
    <Output Name="QO" x="2300" y="632" Type="Data" />
    <Output Name="Result" x="2300" y="692" Type="Data" />

    <EventConnections>
      <Connection Source="$INIT" Destination="$1.INIT" />
      <Connection Source="$1.INITO" Destination="$2.INIT" />
      <Connection Source="$2.INITO" Destination="$INITO" />
      <Connection Source="$REQ" Destination="$1.REQ" />
      <Connection Source="$1.CNF" Destination="$2.REQ" />
      <Connection Source="$2.CNF" Destination="$CNF" />
    </EventConnections>
    <DataConnections>
      <Connection Source="$QI" Destination="$1.QI" />
      <Connection Source="$QI" Destination="$2.QI">
        <Attribute Name="Configuration.Connections.CrossReference" Value="True" />
      </Connection>
      <Connection Source="$A" Destination="$1.Value1" />
      <Connection Source="$B" Destination="$1.Value2" />
      <Connection Source="$1.Result" Destination="$2.Value1" />
      <Connection Source="$C" Destination="$2.Value2" />
      <Connection Source="$2.QO" Destination="$QO" />
      <Connection Source="$2.Result" Destination="$Result" />
    </DataConnections>
  </FBNetwork>
</FBType>
```

---

## Scripts

This skill includes Python scripts for autonomous validation and operation:

| Script | Purpose | Usage | Exit Codes |
|--------|---------|-------|------------|
| `validate_fbnetwork.py` | Verify FBNetwork connection correctness | `python scripts/validate_fbnetwork.py <file.fbt>` | 0=pass, 1=error, 10=validation failed, 11=pass with warnings |
| `validate_layout.py` | Check FBNetwork layout guidelines | `python scripts/validate_layout.py <file.fbt>` | 0=pass, 1=error, 11=pass with warnings |

### Validation Workflow

**Recommended:** Validate automatically after creating or modifying a Composite FB:

```bash
# Validate FBNetwork connections (checks type compatibility, dangling pins)
python scripts/validate_fbnetwork.py path/to/MyBlock.fbt

# Validate layout guidelines (checks positioning, overlaps)
python scripts/validate_layout.py path/to/MyBlock.fbt

# Generic validation (basic XML structure)
python ../eae-skill-router/scripts/validate_block.py --type composite path/to/MyBlock.fbt
```

**Example: validate_fbnetwork.py**

```bash
# Basic validation
python scripts/validate_fbnetwork.py MyBlock.fbt

# Verbose output with connection details
python scripts/validate_fbnetwork.py MyBlock.fbt --verbose

# JSON output for automation/CI
python scripts/validate_fbnetwork.py MyBlock.fbt --json

# CI mode (JSON only, no human messages)
python scripts/validate_fbnetwork.py MyBlock.fbt --ci
```

**What validate_fbnetwork.py checks:**
- ✅ Event connections are event-to-event
- ✅ Data connections have compatible types (BOOL→BOOL, REAL→REAL, etc.)
- ✅ No dangling connections (all Source/Destination valid)
- ✅ FB instances referenced in connections exist
- ✅ Cross-reference connections (../../) are properly formed
- ✅ Interface inputs/outputs are correctly referenced
- ⚠️ FB instances with no connections (warnings)

**Type Compatibility Matrix:**

| Source Type | Compatible Destination Types |
|-------------|------------------------------|
| BOOL | BOOL |
| INT | INT, DINT, REAL, LREAL (widening) |
| DINT | DINT, REAL, LREAL (widening) |
| REAL | REAL, LREAL (widening) |
| STRING | STRING |
| BYTE | BYTE, WORD, DWORD (widening) |

**Note:** Narrowing conversions (REAL→INT) are flagged as errors and require explicit conversion.

**Example: validate_layout.py**

```bash
# Validate layout guidelines
python scripts/validate_layout.py MyBlock.fbt --verbose
```

**What validate_layout.py checks:**
- ⚠️ FBs positioned within recommended bounds (x: 0-5000, y: 0-3000)
- ⚠️ No overlapping FBs (minimum spacing: 100 pixels)
- ⚠️ Layout follows left-to-right flow guidelines

**Note:** Layout validation produces **warnings only** (non-critical). Layout issues don't prevent compilation but affect visual clarity in the EAE IDE.

### Generate IDs

```bash
python ../eae-skill-router/scripts/generate_ids.py --hex 4 --guid 1
```

---

## Templates

- [composite-fb.xml](../eae-skill-router/assets/templates/composite-fb.xml)
- [doc.xml](../eae-skill-router/assets/templates/doc.xml)
- [meta.xml](../eae-skill-router/assets/templates/meta.xml)
- [offline.xml](../eae-skill-router/assets/templates/offline.xml)

---

## Integration with Validation Skills

### Naming Validation

Use [eae-naming-validator](../eae-naming-validator/SKILL.md) to ensure compliance with SE Application Design Guidelines:

**Key Naming Rules for Composite FB:**
- FB name: camelCase (e.g., `sequenceManager`, `dataProcessor`, `valueScaler`)
- Interface variables: PascalCase (e.g., `PermitOn`, `FeedbackOn`, `Value`)
- Events: SNAKE_CASE (e.g., `INIT`, `REQ`, `START_SEQUENCE`)
- FB instances (in FBNetwork): camelCase (e.g., `timer`, `controller`, `scaler`)

**Validate naming before creation:**
```bash
# Validate FB and variable names
python ../eae-naming-validator/scripts/validate_names.py \
  --app-dir IEC61499 \
  --artifact-type CompositeFB \
  --name sequenceManager
```

**Reference:** EAE_ADG EIO0000004686.06, Section 1.5

### Performance Analysis

Use [eae-performance-analyzer](../eae-performance-analyzer/SKILL.md) to prevent event storms in FBNetwork:

```bash
# Analyze event flow in composite FB
python ../eae-performance-analyzer/scripts/analyze_event_flow.py \
  --app-dir IEC61499

# Detect anti-patterns
python ../eae-performance-analyzer/scripts/detect_storm_patterns.py \
  --app-dir IEC61499
```

**What to Check:**
- Event multiplication factor <10x
- No tight event loops (cycles ≤2 hops)
- Total event connections from single source <30

---

## Best Practices from EAE ADG

### 1. Naming Conventions (SE ADG Section 1.5)

**Composite FB Naming:**
- Use camelCase: `sequenceManager`, `dataProcessor`, `valueScaler`
- Use descriptive names that indicate purpose
- Avoid generic names: `composite1`, `network`, `wrapper`

**Variable Naming:**
- Interface variables: PascalCase → `PermitOn`, `SetPoint`, `Result`
- Use descriptive names (avoid `Data1`, `Value`)

**Event Naming:**
- Use SNAKE_CASE: `INIT`, `REQ`, `START_SEQUENCE`, `COMPLETE_OPERATION`
- Standard events: INIT/INITO, REQ/CNF

**FB Instance Naming:**
- Use camelCase for instances: `timer`, `controller`, `scaler1`
- Use semantic names: `cycleTimer` not `fb1`

**Reference:** EAE_ADG EIO0000004686.06, Section 1.5

### 2. FBNetwork Layout Principles

**Positioning Guidelines:**
- X-axis spacing: 1000-1200 units between FBs (for clean routing)
- Y-axis spacing: 60 units between events, 60-80 units between data
- Events at top (y ≈ 350-450), data at bottom (y ≈ 500-800)

**Connection Flow:**
- Left-to-right data flow preferred
- Minimize crossing connections
- Place inputs near their target FBs (not all on left edge)

### 3. Event Connection Best Practices

**Connection Patterns:**
- Chain events for sequential operations: FB1 → FB2 → FB3
- Use E_SPLIT for parallel operations
- Use E_REND for synchronization
- Avoid circular event paths

**Example: Sequential Chain**
```xml
<EventConnections>
  <Connection Source="$REQ" Destination="$1.REQ" />
  <Connection Source="$1.CNF" Destination="$2.REQ" />
  <Connection Source="$2.CNF" Destination="$CNF" />
</EventConnections>
```

---

## Anti-Patterns

### 1. Naming Anti-Patterns

❌ **Wrong Casing for Composite FB**
```xml
<!-- BAD: Using PascalCase for Composite FB -->
<FBType Name="SequenceManager" Format="2.0" ...>
```

✅ **Correct camelCase**
```xml
<FBType Name="sequenceManager" Format="2.0" ...>
```

❌ **Generic FB Instance Names**
```xml
<!-- BAD: Non-descriptive instance names -->
<FB ID="1" Name="fb1" Type="E_CYCLE" ... />
<FB ID="2" Name="logic" Type="MyBlock" ... />
```

✅ **Descriptive Instance Names**
```xml
<FB ID="1" Name="cycleTimer" Type="E_CYCLE" Namespace="Runtime.Base" ... />
<FB ID="2" Name="valueCalculator" Type="MyBlock" ... />
```

### 2. Structure Anti-Patterns

❌ **Missing Format="2.0"**
```xml
<!-- BAD: Composite FB without Format attribute -->
<FBType Name="myComposite" ...>
  <FBNetwork>...</FBNetwork>
</FBType>
```

✅ **Format="2.0" Required**
```xml
<FBType Name="myComposite" Format="2.0" ...>
  <FBNetwork>...</FBNetwork>
</FBType>
```

❌ **Using BasicFB Instead of FBNetwork**
```xml
<!-- BAD: Composite should not have BasicFB -->
<FBType Name="myComposite" Format="2.0" ...>
  <BasicFB>
    <ECC>...</ECC>
  </BasicFB>
</FBType>
```

✅ **Use FBNetwork**
```xml
<FBType Name="myComposite" Format="2.0" ...>
  <FBNetwork>
    <FB ID="1" ... />
  </FBNetwork>
</FBType>
```

### 3. Event Connection Anti-Patterns

❌ **Tight Event Loop**
```xml
<!-- BAD: FB1 → FB2 → FB1 creates 2-hop loop -->
<EventConnections>
  <Connection Source="$1.OUT1" Destination="$2.IN" />
  <Connection Source="$2.OUT" Destination="$1.IN" />
</EventConnections>
```

✅ **Break Loops with State Guards**
```xml
<!-- Use RS flip-flop or conditional logic to break loop -->
<FB ID="3" Name="loopGuard" Type="RS" Namespace="Runtime.Base" ... />
```

❌ **Event Multiplication >30x**
```xml
<!-- BAD: Single event triggers 50+ downstream events -->
<EventConnections>
  <Connection Source="$1.OUT" Destination="$2.IN" />
  <Connection Source="$1.OUT" Destination="$3.IN" />
  <!-- ... 50+ more connections from $1.OUT -->
</EventConnections>
```

✅ **Use Event Consolidation**
```xml
<!-- Use E_SPLIT sparingly, prefer sequential chains -->
<FB ID="splitter" Type="E_SPLIT" Namespace="Runtime.Base" ... />
```

### 4. Layout Anti-Patterns

❌ **All Inputs on Left Edge**
```xml
<!-- BAD: Input C connects to FB3 but is placed on left edge -->
<Input Name="A" x="100" y="672" Type="Data" />  <!-- Connects to FB1 (OK) -->
<Input Name="B" x="100" y="752" Type="Data" />  <!-- Connects to FB1 (OK) -->
<Input Name="C" x="100" y="832" Type="Data" />  <!-- Connects to FB3 (BAD: should be near FB3!) -->
```

✅ **Position Inputs Near Their Targets**
```xml
<Input Name="A" x="100" y="672" Type="Data" />   <!-- Near FB1 -->
<Input Name="B" x="100" y="752" Type="Data" />   <!-- Near FB1 -->
<Input Name="C" x="1180" y="752" Type="Data" />  <!-- Near FB3 -->
```

❌ **Insufficient FB Spacing**
```xml
<!-- BAD: FBs too close together (400 units) -->
<FB ID="1" Name="fb1" x="500" y="360" ... />
<FB ID="2" Name="fb2" x="900" y="360" ... />  <!-- Only 400 units apart! -->
```

✅ **Adequate FB Spacing**
```xml
<!-- Use 1000-1200 units for clean connection routing -->
<FB ID="1" Name="fb1" x="720" y="360" ... />
<FB ID="2" Name="fb2" x="1820" y="360" ... />  <!-- 1100 units apart -->
```

❌ **Overlapping Elements**
```xml
<!-- BAD: Events and data at same y position -->
<Input Name="REQ" x="100" y="500" Type="Event" />
<Input Name="QI" x="100" y="500" Type="Data" />  <!-- Same y! -->
```

✅ **Separated Events and Data**
```xml
<!-- Events at top, data at bottom with gap -->
<Input Name="REQ" x="100" y="432" Type="Event" />
<Input Name="QI" x="100" y="650" Type="Data" />  <!-- 200+ unit gap -->
```

### 5. Connection Anti-Patterns

❌ **Type Mismatch**
```xml
<!-- BAD: Connecting REAL to BOOL -->
<DataConnections>
  <Connection Source="$RealValue" Destination="$1.BoolInput" />
</DataConnections>
```

❌ **Dangling Connections**
```xml
<!-- BAD: References non-existent FB -->
<EventConnections>
  <Connection Source="$1.OUT" Destination="$99.IN" />  <!-- FB ID 99 doesn't exist! -->
</EventConnections>
```

❌ **Event-to-Data Connection**
```xml
<!-- BAD: Cannot connect event to data -->
<Connection Source="$INIT" Destination="$1.QI" />  <!-- INIT is Event, QI is Data! -->
```

---

## Verification Checklist

Before committing your Composite FB:

**Naming (run eae-naming-validator):**
- [ ] FB name is camelCase
- [ ] Interface variables are PascalCase
- [ ] Events are SNAKE_CASE
- [ ] FB instances use camelCase semantic names

**Structure:**
- [ ] Root element is `<FBType>` with `Format="2.0"`
- [ ] Uses `Standard="61499-2"`
- [ ] Has `<FBNetwork>` (NOT `<BasicFB>`)
- [ ] All FB instances have unique IDs

**FBNetwork Validation (run validate_fbnetwork.py):**
- [ ] All event connections are event-to-event
- [ ] All data connections have compatible types
- [ ] No dangling connections (all Source/Destination valid)
- [ ] No event-to-data or data-to-event connections

**Layout Validation (run validate_layout.py):**
- [ ] FBs spaced 1000-1200 units apart horizontally
- [ ] No overlapping elements
- [ ] Inputs positioned near their target FBs
- [ ] Events and data vertically separated

**Performance (run eae-performance-analyzer):**
- [ ] Event multiplication factor <10x
- [ ] No tight event loops (≤2 hops)
- [ ] Total event connections from single source <30

**Scripts Validation:**
- [ ] `python scripts/validate_fbnetwork.py {Name}.fbt` exits with 0
- [ ] `python scripts/validate_layout.py {Name}.fbt` exits with 0 or 11 (warnings OK)

**Registration:**
- [ ] Registered in .dfbproj with `IEC61499Type="Composite"`
- [ ] .doc.xml, .meta.xml, .composite.offline.xml files created

---

## Related Skills

| Skill | When to Use |
|-------|-------------|
| [eae-naming-validator](../eae-naming-validator/SKILL.md) | Validate naming compliance (camelCase for Composite FB) |
| [eae-performance-analyzer](../eae-performance-analyzer/SKILL.md) | Prevent event storms in FBNetwork |
| [eae-runtime-base](../eae-runtime-base/SKILL.md) | Find standard blocks (E_CYCLE, E_DELAY, MQTT, etc.) |
| [eae-se-process](../eae-se-process/SKILL.md) | Find SE process blocks (motors, valves, PID, signals) |
| [eae-cat](../eae-cat/SKILL.md) | Need HMI visualization |
| [eae-basic-fb](../eae-basic-fb/SKILL.md) | Need custom algorithms |
| [eae-datatype](../eae-datatype/SKILL.md) | Create custom data types |
