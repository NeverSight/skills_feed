---
name: eae-cat
description: >
  Create and register CAT (Composite Application Type) blocks in EAE with HMI
  visualization, OPC-UA server, and persistence features.
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
# EAE CAT Block Creation

Create and register CAT (Composite Application Type) blocks - the most common block type in EAE.

**CAT = Enhanced Composite FB with:**
- HMI visualization (symbols)
- OPC-UA server interface
- Persistence (offline parameters)

**This skill handles:**
- Creating new CAT blocks from scratch
- Registering CAT blocks in dfbproj (including forked blocks from eae-fork)
- Generating HMI symbol files
- Validating CAT registration

> **Tip:** Need standard blocks like E_CYCLE, E_DELAY, or MQTT inside your CAT? Use `/eae-runtime-base` to find the right Runtime.Base block.

## Quick Start

```
User: Create a CAT block called MotorController in MyLibrary namespace
Claude: [Creates IEC61499/MotorController/ folder with all files]
```

## Triggers

- `/eae-cat`
- `/eae-cat --register-only` - Register existing CAT block (used by eae-fork orchestration)
- "create CAT block"
- "create block with HMI"
- "create CAT with visualization"

---

## Register-Only Mode (for eae-fork Orchestration)

When called with `--register-only`, this skill skips file creation and only performs project registration. This mode is used by **eae-fork** to complete the fork workflow after file transformation.

```
/eae-cat --register-only {BlockName} {Namespace}
```

**What --register-only does:**

1. **Registers in dfbproj** - Adds ItemGroup entries for CAT block visibility
2. **Registers in csproj** - Adds HMI file entries to HMI project
3. **Updates Folders.xml** - Adds folder entries for library browser
4. **Validates** - Confirms block is properly registered

**What --register-only does NOT do:**

- Create IEC61499 files (.fbt, .cfg, etc.) - already done by eae-fork
- Create HMI files (.def.cs, .cnv.cs, etc.) - already done by eae-fork
- Update namespaces - already done by eae-fork

### Usage by eae-fork

```
eae-fork detects CAT type → calls /eae-cat --register-only
                                   │
                                   ├── python ../eae-skill-router/scripts/register_dfbproj.py {Block} {Lib} --type cat
                                   │
                                   └── Validates registration complete
```

### Manual Usage

If you need to manually register a CAT block (e.g., after manual file copy):

```bash
# Register a forked CAT block
python ../eae-skill-router/scripts/register_dfbproj.py AnalogInput SE.ScadapackWWW --type cat

# Verify registration
python ../eae-skill-router/scripts/register_dfbproj.py AnalogInput SE.ScadapackWWW --type cat --verify

# Dry run (see what would be added)
python ../eae-skill-router/scripts/register_dfbproj.py AnalogInput SE.ScadapackWWW --type cat --dry-run
```

---

## Files Generated

A CAT block creates **15+ files** in two locations:

### IEC61499/{CATName}/

| File | Purpose |
|------|---------|
| `{Name}.cfg` | CAT configuration (links all files) |
| `{Name}.fbt` | Main composite FB |
| `{Name}.doc.xml` | Documentation |
| `{Name}.meta.xml` | Metadata |
| `{Name}_CAT.offline.xml` | Offline parameter config |
| `{Name}_CAT.opcua.xml` | OPC-UA server config |
| `{Name}_HMI.fbt` | Service interface FB |
| `{Name}_HMI.doc.xml` | HMI documentation |
| `{Name}_HMI.meta.xml` | HMI metadata |
| `{Name}_HMI.offline.xml` | HMI offline config |
| `{Name}_HMI.opcua.xml` | HMI OPC-UA config |

### HMI/{CATName}/

| File | Purpose |
|------|---------|
| `{Name}.def.cs` | Symbol definitions |
| `{Name}.event.cs` | Event definitions |
| `{Name}.Design.resx` | Design resources |
| `{Name}_sDefault.cnv.cs` | Default symbol |
| `{Name}_sDefault.cnv.Designer.cs` | Symbol designer |
| `{Name}_sDefault.cnv.resx` | Symbol resources |
| `{Name}_sDefault.cnv.xml` | Symbol mapping |
| `{Name}_sDefault.doc.xml` | Symbol documentation |

---

## Workflow

1. **Create folder** `IEC61499/{CATName}/`
2. **Generate GUIDs** for CAT FB and HMI FB
3. **Create .cfg file** (links everything)
4. **Create .fbt file** (Composite FB with `Format="2.0"`)
5. **Create _HMI.fbt** (Service interface)
6. **Create supporting files** (.doc.xml, .meta.xml, .offline.xml, .opcua.xml)
7. **Create HMI folder** `HMI/{CATName}/`
8. **Create symbol files** (.def.cs, .event.cs, .cnv.* files)
9. **Register in .dfbproj**

---

## CAT Configuration File (.cfg)

The `.cfg` file links all CAT components:

```xml
<?xml version="1.0" encoding="utf-8"?>
<CAT xmlns:xsd="http://www.w3.org/2001/XMLSchema"
     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
     Name="{CATName}"
     CATFile="{CATName}\{CATName}.fbt"
     SymbolDefFile="..\HMI\{CATName}\{CATName}.def.cs"
     SymbolEventFile="..\HMI\{CATName}\{CATName}.event.cs"
     DesignFile="..\HMI\{CATName}\{CATName}.Design.resx"
     xmlns="http://www.nxtcontrol.com/IEC61499.xsd">

  <HMIInterface Name="IThis" FileName="{CATName}\{CATName}_HMI.fbt">
    <Symbol Name="sDefault" FileName="..\HMI\{CATName}\{CATName}_sDefault.cnv.cs">
      <DependentFiles>..\HMI\{CATName}\{CATName}_sDefault.cnv.Designer.cs</DependentFiles>
      <DependentFiles>..\HMI\{CATName}\{CATName}_sDefault.cnv.resx</DependentFiles>
      <DependentFiles>..\HMI\{CATName}\{CATName}_sDefault.cnv.xml</DependentFiles>
    </Symbol>
    <MetaFile>{CATName}\{CATName}_HMI.meta.xml</MetaFile>
  </HMIInterface>

  <Plugin Name="Plugin=OfflineParametrizationEditor;IEC61499Type=CAT_OFFLINE;$ItemType$=Content"
          Project="{Project}" Value="{CATName}\{CATName}_CAT.offline.xml" />
  <Plugin Name="Plugin=OPCUAConfigurator;IEC61499Type=CAT_OPCUA;$ItemType$=Content"
          Project="{Project}" Value="{CATName}\{CATName}_CAT.opcua.xml" />

  <HWConfiguration xsi:nil="true" />
</CAT>
```

**Note:** CAT .cfg files DO use `xmlns` - this is correct (unlike .fbt files).

---

## CAT FB Template (.fbt)

Same as Composite FB but with `HMI.Alias` attribute:

```xml
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE FBType SYSTEM "../LibraryElement.dtd">
<FBType Name="{CATName}" Namespace="{YourNamespace}" Format="2.0"
        GUID="{NEW-GUID}" Comment="CAT Function Block">
  <Attribute Name="HMI.Alias" Value="" />
  <Identification Standard="61499-2" />
  <VersionInfo Organization="{Org}" Version="0.0" Author="{Author}"
               Date="{MM/DD/YYYY}" Remarks="Initial version" />
  <CompilerInfo />
  <InterfaceList>
    <!-- Events and Variables -->
  </InterfaceList>
  <FBNetwork>
    <!-- FB instances and connections -->
  </FBNetwork>
</FBType>
```

---

## HMI Service FB Template (_HMI.fbt)

The HMI service interface defines what data is exposed to visualization:

```xml
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE FBType SYSTEM "../LibraryElement.dtd">
<FBType GUID="{NEW-GUID}" Name="{CATName}_HMI" Namespace="{YourNamespace}">
  <InterfaceList>
    <EventInputs>
      <Event ID="{HEX-ID}" Name="INIT">
        <With Var="QI" />
      </Event>
      <Event ID="{HEX-ID}" Name="UPD">
        <With Var="Value" />
        <With Var="Status" />
      </Event>
    </EventInputs>
    <EventOutputs>
      <Event ID="{HEX-ID}" Name="INITO">
        <With Var="QO" />
        <With Var="STATUS" />
      </Event>
    </EventOutputs>
    <InputVars>
      <VarDeclaration ID="{HEX-ID}" Name="QI" Type="BOOL" />
      <VarDeclaration ID="{HEX-ID}" Name="Value" Type="REAL" />
      <VarDeclaration ID="{HEX-ID}" Name="Status" Type="Status" Namespace="SE.App2Base" />
    </InputVars>
    <OutputVars>
      <VarDeclaration ID="{HEX-ID}" Name="QO" Type="BOOL" />
      <VarDeclaration ID="{HEX-ID}" Name="STATUS" Type="STRING" />
    </OutputVars>
  </InterfaceList>
  <Service RightInterface="" LeftInterface="">
    <ServiceSequence Name="" />
  </Service>
</FBType>
```

---

## SubCAT References

If your CAT contains other CAT blocks internally, add SubCAT references:

```xml
<SubCAT Name="{instanceName}" Type="{SubCATType}" Namespace="{Namespace}" UsedInCAT="true" />
```

---

## dfbproj Registration

CAT blocks have complex registration:

```xml
<!-- CAT configuration and supporting files -->
<ItemGroup>
  <None Include="{Name}\{Name}.cfg">
    <DependentUpon>{Name}.fbt</DependentUpon>
    <IEC61499Type>CAT</IEC61499Type>
  </None>
  <None Include="{Name}\{Name}_CAT.offline.xml">
    <DependentUpon>{Name}.fbt</DependentUpon>
    <Plugin>OfflineParametrizationEditor</Plugin>
    <IEC61499Type>CAT_OFFLINE</IEC61499Type>
  </None>
  <None Include="{Name}\{Name}_CAT.opcua.xml">
    <DependentUpon>{Name}.fbt</DependentUpon>
    <Plugin>OPCUAConfigurator</Plugin>
    <IEC61499Type>CAT_OPCUA</IEC61499Type>
  </None>
  <None Include="{Name}\{Name}_HMI.offline.xml">
    <DependentUpon>{Name}_HMI.fbt</DependentUpon>
    <Plugin>OfflineParametrizationEditor</Plugin>
    <IEC61499Type>CAT_OFFLINE</IEC61499Type>
  </None>
  <None Include="{Name}\{Name}_HMI.opcua.xml">
    <DependentUpon>{Name}_HMI.fbt</DependentUpon>
    <Plugin>OPCUAConfigurator</Plugin>
    <IEC61499Type>CAT_OPCUA</IEC61499Type>
  </None>
  <!-- .doc.xml and .meta.xml files... -->
</ItemGroup>

<!-- Main CAT FB -->
<ItemGroup>
  <Compile Include="{Name}\{Name}.fbt">
    <IEC61499Type>CAT</IEC61499Type>
  </Compile>
  <Compile Include="{Name}\{Name}_HMI.fbt">
    <IEC61499Type>CAT</IEC61499Type>
    <Usage>Private</Usage>
    <DependentUpon>{Name}.fbt</DependentUpon>
    <HMI>..\HMI\{Name}\{Name}_sDefault.cnv.cs</HMI>
  </Compile>
</ItemGroup>
```

---

## FBNetwork Layout

Follow the same layout guidelines as Composite FB. See [eae-composite-fb](../eae-composite-fb/SKILL.md#fbnetwork-layout-guidelines).

---

## Common Runtime.Base Blocks for CATs

CAT blocks often use standard Runtime.Base blocks internally. Use `/eae-runtime-base` for full documentation.

### Frequently Used in CATs

| Block | Purpose | Typical Use in CAT |
|-------|---------|-------------------|
| `E_CYCLE` | Periodic update | Update HMI values periodically |
| `E_DELAY` | Timed actions | Debounce, timeout handling |
| `E_REND` | Synchronize | Wait for multiple init completions |
| `E_SWITCH` | Conditional routing | Route based on mode/state |
| `PERSISTENCE` | Save values | Store parameters offline |
| `LOGGER` | Diagnostics | Log CAT events |

### Example: CAT with Periodic HMI Update

```xml
<FBNetwork>
  <!-- Timer for periodic HMI updates -->
  <FB ID="1" Name="updateTimer" Type="E_CYCLE" Namespace="Runtime.Base" x="500" y="350" />

  <!-- Your logic blocks -->
  <FB ID="2" Name="logic" Type="MyLogicFB" Namespace="MyLib" x="1100" y="350" />

  <EventConnections>
    <Connection Source="$INIT" Destination="$1.START" />
    <Connection Source="$1.EO" Destination="$2.REQ" />
  </EventConnections>
  <DataConnections>
    <Connection Source="T#500ms" Destination="$1.DT" />
  </DataConnections>
</FBNetwork>
```

> For the complete catalog of ~100 Runtime.Base blocks, see `/eae-runtime-base`.

---

## Common Rules

See [common-rules.md](../eae-skill-router/references/common-rules.md) for:
- ID generation
- DOCTYPE references
- dfbproj registration patterns

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| CAT won't load | Ensure all files in `{Name}/` subfolder |
| HMI not visible | Check .cfg HMIInterface paths |
| SubCAT missing | Add SubCAT reference in .cfg |
| Symbols not working | Verify HMI/ folder structure |

---

## Scripts

This skill includes Python scripts for autonomous validation and operation:

| Script | Purpose | Usage | Exit Codes |
|--------|---------|-------|------------|
| `validate_cat.py` | Verify all 15+ CAT files are consistent | `python scripts/validate_cat.py <IEC61499/CATName>` | 0=pass, 1=error, 10=validation failed, 11=pass with warnings |
| `validate_hmi.py` | Check HMI file structure | `python scripts/validate_hmi.py <HMI/CATName>` | 0=pass, 1=error, 10=validation failed, 11=pass with warnings |

### Validation Workflow

**Recommended:** Validate automatically after creating or modifying a CAT block:

```bash
# Validate CAT block (all 15+ files, namespaces, .cfg file)
python scripts/validate_cat.py path/to/IEC61499/MyCATBlock

# Validate HMI files (C# structure, conventions)
python scripts/validate_hmi.py path/to/HMI/MyCATBlock

# Generic validation (basic XML structure)
python ../eae-skill-router/scripts/validate_block.py --type cat path/to/IEC61499/MyCATBlock/
```

**Example: validate_cat.py**

```bash
# Basic validation
python scripts/validate_cat.py IEC61499/MyCATBlock

# Validate with expected namespace
python scripts/validate_cat.py IEC61499/MyCATBlock --namespace MyLibrary

# Verbose output with file details
python scripts/validate_cat.py IEC61499/MyCATBlock --verbose

# JSON output for automation/CI
python scripts/validate_cat.py IEC61499/MyCATBlock --json

# CI mode (JSON only, no human messages)
python scripts/validate_cat.py IEC61499/MyCATBlock --ci
```

**What validate_cat.py checks:**
- ✅ All required IEC61499 files exist (11 files: .cfg, .fbt, _HMI.fbt, .offline.xml, .opcua.xml, etc.)
- ✅ All required HMI files exist (8+ files: .def.cs, .event.cs, .cnv.*, etc.)
- ✅ .cfg file references correct paths (CATFile, HMIFile, SymbolDefFile)
- ✅ .cfg Name attribute matches directory name
- ✅ Namespaces are consistent across .fbt files
- ⚠️ Missing recommended HMI files (warnings)

**CAT Block File Checklist:**

IEC61499/{CATName}/ (11 files):
- ✅ `{Name}.cfg` - CAT configuration
- ✅ `{Name}.fbt` - Main composite FB
- ✅ `{Name}.doc.xml`, `{Name}.meta.xml`
- ✅ `{Name}_CAT.offline.xml`, `{Name}_CAT.opcua.xml`
- ✅ `{Name}_HMI.fbt` - Service interface FB
- ✅ `{Name}_HMI.doc.xml`, `{Name}_HMI.meta.xml`
- ✅ `{Name}_HMI.offline.xml`, `{Name}_HMI.opcua.xml`

HMI/{CATName}/ (8+ files):
- ✅ `{Name}.def.cs` - Symbol definitions
- ✅ `{Name}.event.cs` - Event definitions
- ✅ `{Name}.Design.resx` - Design resources
- ✅ `{Name}_sDefault.cnv.cs` - Default symbol
- ✅ `{Name}_sDefault.cnv.Designer.cs` - Symbol designer
- ✅ `{Name}_sDefault.cnv.resx` - Symbol resources
- ✅ `{Name}_sDefault.cnv.xml` - Symbol mapping
- ✅ `{Name}_sDefault.doc.xml` - Symbol documentation

**Example: validate_hmi.py**

```bash
# Validate HMI files
python scripts/validate_hmi.py HMI/MyCATBlock --verbose
```

**What validate_hmi.py checks:**
- ✅ .def.cs contains symbol definition class
- ✅ .def.cs inherits from SymbolDefinition
- ✅ .event.cs contains event definitions
- ✅ .event.cs uses partial class pattern
- ✅ Converter files (.cnv.*) are present
- ✅ Converter inherits from UserControl
- ⚠️ File structure warnings (missing namespaces, empty files)

**Note:** Full C# compilation is performed by the EAE IDE. These scripts catch common structural issues early to save compilation cycles.

### Generate IDs

CAT blocks need 2 GUIDs (CAT FB + HMI FB) plus hex IDs for events/vars:

```bash
python ../eae-skill-router/scripts/generate_ids.py --guid 2 --hex 10
```

---

## Templates

- [cat-config.xml](../eae-skill-router/assets/templates/cat-config.xml)
- [cat-fb.xml](../eae-skill-router/assets/templates/cat-fb.xml)
- [service-fb.xml](../eae-skill-router/assets/templates/service-fb.xml)

---

## Integration with Validation Skills

### Naming Validation

Use [eae-naming-validator](../eae-naming-validator/SKILL.md) to ensure compliance with SE Application Design Guidelines:

**Key Naming Rules for CAT:**
- CAT name: PascalCase (e.g., `AnalogInput`, `MotorController`)
- Interface variables (inputs/outputs): PascalCase (e.g., `PermitOn`, `FeedbackOn`)
- Internal variables: camelCase (e.g., `error`, `outMinActiveLast`)
- Events: SNAKE_CASE (e.g., `START_MOTOR`, `STOP_PROCESS`)
- Adapters (if used): IPascalCase (e.g., `IMotorControl`)

**Validate naming before creation:**
```bash
# Validate CAT and variable names
python ../eae-naming-validator/scripts/validate_names.py \
  --app-dir IEC61499/MyLibrary \
  --json
```

### Performance Analysis

Use [eae-performance-analyzer](../eae-performance-analyzer/SKILL.md) to prevent event storms in CAT FBNetworks:

```bash
# Analyze event flow in CAT block
python ../eae-performance-analyzer/scripts/analyze_event_flow.py \
  --app-dir IEC61499/MyLibrary

# Check for anti-patterns
python ../eae-performance-analyzer/scripts/detect_storm_patterns.py \
  --app-dir IEC61499/MyLibrary
```

**What to Check:**
- Event multiplication factor <10x
- No tight event loops (cycles ≤2 hops)
- HMI update frequency (E_CYCLE DT ≥100ms)
- I/O event connections <30 downstream

---

## Best Practices from EAE ADG

### 1. Naming Conventions (SE ADG Section 1.5)

**CAT Naming:**
- Use PascalCase: `MotorController`, `SpMon`, `OosMode`
- Single word preferred for folders: `Motors`, `Valves`
- Avoid abbreviations unless industry-standard (PID, HMI, OPC)

**Variable Naming:**
- Interface variables: PascalCase → `PermitOn`, `FeedbackOn`
- Internal variables: camelCase → `error`, `timerActive`
- Data types: Hungarian notation → `strMotorData`, `arrRecipeBuffer`

**Event Naming:**
- Use SNAKE_CASE: `START_MOTOR`, `STOP_PROCESS`
- Use INIT/INITO for initialization

**Reference:** EAE_ADG EIO0000004686.06, Section 1.5

### 2. FBNetwork Layout

**Grid Guidelines:**
- X-axis: 500, 1100, 1700, 2300, 2900 (600px spacing)
- Y-axis: 350, 800, 1250, 1700, 2150 (450px spacing)
- Top-to-bottom data flow
- Left-to-right event flow

### 3. HMI Interface Design

**Service FB (_HMI.fbt) Guidelines:**
- Keep interface minimal (expose only necessary data)
- Use periodic updates (E_CYCLE 500ms typical, 100ms minimum)
- Use SE.App2Base.Status for standardized status reporting
- Include QI/QO pattern for init handshake

**HMI Update Pattern:**
```xml
<FBNetwork>
  <FB ID="1" Name="hmiUpdate" Type="E_CYCLE" Namespace="Runtime.Base" x="500" y="350" />
  <EventConnections>
    <Connection Source="$INIT" Destination="$1.START" />
    <Connection Source="$1.EO" Destination="$HMI.UPD" />
  </EventConnections>
  <DataConnections>
    <Connection Source="T#500ms" Destination="$1.DT" />
  </DataConnections>
</FBNetwork>
```

---

## Anti-Patterns

### 1. Event Storm Anti-Patterns

❌ **TIGHT_EVENT_LOOP**
```xml
<!-- BAD: FB1 -> FB2 -> FB1 creates 2-hop loop -->
<EventConnections>
  <Connection Source="$1.CNF" Destination="$2.REQ" />
  <Connection Source="$2.CNF" Destination="$1.REQ" />
</EventConnections>
```

✅ **FIX: Add state guard with RS flip-flop**

❌ **HIGH_FREQUENCY_TIMER**
```xml
<!-- BAD: 10ms E_CYCLE causes 100 events/sec -->
<DataConnections>
  <Connection Source="T#10ms" Destination="$1.DT" />
</DataConnections>
```

✅ **FIX: Use appropriate interval (500ms for HMI, 100ms minimum)**

### 2. Naming Anti-Patterns

❌ **Inconsistent Casing**
```xml
<VarDeclaration Name="PermitOn" Type="BOOL" />
<VarDeclaration Name="Error" Type="BOOL" />  <!-- BAD: should be "error" if internal -->
```

❌ **Generic Event Names**
```xml
<Event Name="DO1" />  <!-- BAD: non-descriptive -->
```

✅ **Descriptive Event Names**
```xml
<Event Name="START_MOTOR" />
<Event Name="UPDATE_HMI" />
```

### 3. Structure Anti-Patterns

❌ **Missing .cfg File**
```
IEC61499/MyCATBlock/
  MyCATBlock.fbt           ✅
  MyCATBlock_HMI.fbt       ✅
  MyCATBlock.cfg           ❌ MISSING - CAT won't load!
```

❌ **Wrong .cfg Paths**
```xml
<!-- BAD: Absolute paths -->
<CAT CATFile="C:\Projects\IEC61499\MyCAT\MyCAT.fbt" ... />
```

✅ **Relative Paths**
```xml
<CAT CATFile="MyCAT\MyCAT.fbt"
     SymbolDefFile="..\HMI\MyCAT\MyCAT.def.cs" ... />
```

### 4. HMI Anti-Patterns

❌ **Too Many HMI Variables** (50+ variables exposed)

✅ **Minimal HMI Interface** (5-15 variables, use structured types)

❌ **Direct I/O in HMI Service** (_HMI.fbt should contain only `<Service>`, no `<FBNetwork>`)

---

## Verification Checklist

Before committing your CAT block:

**Structure:**
- [ ] All 11 IEC61499 files present in `{Name}/` subfolder
- [ ] All 8+ HMI files present in `HMI/{Name}/` subfolder
- [ ] .cfg file exists with correct relative paths
- [ ] Registered in .dfbproj with correct IEC61499Type tags

**Naming (run eae-naming-validator):**
- [ ] CAT name is PascalCase
- [ ] Interface variables are PascalCase
- [ ] Internal variables are camelCase
- [ ] Events are SNAKE_CASE

**Performance (run eae-performance-analyzer):**
- [ ] Event multiplication factor <10x
- [ ] No tight event loops (≤2 hops)
- [ ] E_CYCLE timers ≥100ms (unless justified)
- [ ] I/O event connections <30 downstream

**Scripts Validation:**
- [ ] `python scripts/validate_cat.py IEC61499/{Name}` exits with 0
- [ ] `python scripts/validate_hmi.py HMI/{Name}` exits with 0

**Manual Checks:**
- [ ] HMI interface has 5-15 variables (not 50+)
- [ ] _HMI.fbt contains `<Service>` only
- [ ] .cfg paths are relative
- [ ] SubCAT references added (if using nested CATs)

---

## Registering Forked Blocks

When eae-fork copies a block from a source library, it handles file transformation (copy, namespace update, reference update). **This skill (eae-cat) completes the process** by:

1. **Registering in dfbproj** - Makes block visible in EAE library browser
2. **Creating HMI files** - Symbol implementations (.cnv.cs, .cnv.Designer.cs, .cnv.resx, .cnv.xml)
3. **Validating registration** - Ensures block loads correctly

### Workflow: After eae-fork

```
eae-fork completes → eae-cat registers
     │                    │
     │ Steps 1-4:         │ Steps 5-7:
     │ • Copy files       │ • Generate HMI files
     │ • Update namespace │ • Register in dfbproj
     │ • Update refs      │ • Validate registration
     │ • Update .cfg      │
     ▼                    ▼
 Files in IEC61499/    Block visible in EAE
```

### Registration Command

```bash
# After forking AnalogInput to SE.ScadapackWWW:
python ../eae-skill-router/scripts/register_dfbproj.py AnalogInput SE.ScadapackWWW --type cat

# Output:
# [OK] Successfully registered CAT block 'AnalogInput' in dfbproj
# Entries:
#   + AnalogInput\AnalogInput.fbt (Compile/CAT)
#   + AnalogInput\AnalogInput_HMI.fbt (Compile/CAT)
#   + AnalogInput\AnalogInput.cfg (None/CAT)
#   + AnalogInput\AnalogInput_CAT.offline.xml (None/CAT_OFFLINE)
#   + AnalogInput\AnalogInput_CAT.opcua.xml (None/CAT_OPCUA)
#   + AnalogInput\AnalogInput_CAT.aspmap.xml (None/CAT_ASPMAP)
```

---

## Related Skills

| Skill | When to Use |
|-------|-------------|
| [eae-fork](../eae-fork/SKILL.md) | Fork blocks from SE libraries (calls eae-cat after for CAT blocks) |
| [eae-naming-validator](../eae-naming-validator/SKILL.md) | Validate naming compliance with SE ADG |
| [eae-performance-analyzer](../eae-performance-analyzer/SKILL.md) | Prevent event storms in FBNetwork |
| [eae-runtime-base](../eae-runtime-base/SKILL.md) | Find standard blocks (E_CYCLE, E_DELAY, MQTT, etc.) |
| [eae-se-process](../eae-se-process/SKILL.md) | Find SE process blocks (motors, valves, PID, signals) |
| [eae-composite-fb](../eae-composite-fb/SKILL.md) | Simple composite without HMI |
| [eae-basic-fb](../eae-basic-fb/SKILL.md) | Create custom logic blocks |
| [eae-datatype](../eae-datatype/SKILL.md) | Create custom data types |
