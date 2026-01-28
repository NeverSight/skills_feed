---
name: eae-adapter
description: >
  Create Adapter types in EAE for reusable bidirectional interfaces
  (socket/plug pattern).
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
# EAE Adapter Creation

Create or modify Adapter types for reusable bidirectional interfaces.

> **CRITICAL RULE:** ALWAYS use this skill for ANY operation on Adapter files.
> - Creating new Adapters
> - Modifying existing Adapters (adding events, variables, service sequences)
> - NEVER directly edit `.adp` files outside of this skill

**Adapter = Bidirectional Interface Pattern**
- Socket side: sees interface as defined
- Plug side: sees interface reversed
- Used for standard communication patterns

**Adapter Key Differences:**
- Uses `<AdapterType>` root element (NOT FBType)
- Uses `.adp` extension (NOT `.fbt`)
- Uses `Standard="61499-1"` (NOT 61499-2)
- Has `<Service>` element defining communication sequences

## Quick Start

```
User: Create an adapter for request/response communication
Claude: [Creates IEC61499/MyAdapter.adp with service sequences]
```

## Triggers

- `/eae-adapter`
- `/eae-adapter --register-only` - Register existing Adapter (used by eae-fork orchestration)
- "create adapter"
- "modify adapter"
- "add event to adapter"
- "create interface adapter"
- "socket plug interface"

---

## Register-Only Mode (for eae-fork Orchestration)

When called with `--register-only`, this skill skips file creation and only performs dfbproj registration. This mode is used by **eae-fork** to complete the fork workflow after file transformation.

```
/eae-adapter --register-only {AdapterName} {Namespace}
```

**What --register-only does:**

1. **Registers in dfbproj** - Adds ItemGroup entries for Adapter visibility

**What --register-only does NOT do:**

- Create IEC61499 files (.adp, etc.) - already done by eae-fork
- Update namespaces - already done by eae-fork

### Usage

```bash
# Register a forked Adapter
python ../eae-skill-router/scripts/register_dfbproj.py IMyAdapter SE.ScadapackWWW --type adapter

# Verify registration
python ../eae-skill-router/scripts/register_dfbproj.py IMyAdapter SE.ScadapackWWW --type adapter --verify
```

---

## Modification Workflow

When modifying an existing Adapter:

1. Read the existing `.adp` file to understand current structure
2. Identify what needs to be added/changed
3. Generate new hex IDs for any new Events or VarDeclarations
4. Update the InterfaceList (events, variables) if needed
5. Update the Service element with new ServiceSequences if needed
6. Ensure service transactions match the new events/data

---

## Files Generated

| File | Purpose |
|------|---------|
| `{Name}.adp` | Main adapter (NOT .fbt!) |
| `{Name}.doc.xml` | Documentation |

**Note:** No `.meta.xml` for adapters.

Location: `IEC61499/`

---

## Critical Rules

| Rule | Value |
|------|-------|
| Root Element | `<AdapterType>` (NOT FBType) |
| DOCTYPE | `<!DOCTYPE AdapterType SYSTEM "../LibraryElement.dtd">` |
| Standard | `<Identification Standard="61499-1" />` |
| Extension | `.adp` (NOT `.fbt`) |
| Service Element | Required |

---

## Adapter Template

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE AdapterType SYSTEM "../LibraryElement.dtd">
<AdapterType Name="{AdapterName}" Namespace="{YourNamespace}"
             GUID="{NEW-GUID}" Comment="Adapter Interface">
  <Identification Standard="61499-1" />
  <VersionInfo Organization="{Org}" Version="0.0" Author="{Author}"
               Date="{MM/DD/YYYY}" Remarks="Initial" />
  <CompilerInfo />
  <InterfaceList>
    <EventInputs>
      <Event ID="{HEX-ID}" Name="REQ" Comment="Request from Socket">
        <With Var="REQD" />
      </Event>
      <Event ID="{HEX-ID}" Name="RSP" Comment="Response from Socket">
        <With Var="RSPD" />
      </Event>
    </EventInputs>
    <EventOutputs>
      <Event ID="{HEX-ID}" Name="CNF" Comment="Confirmation from Plug">
        <With Var="CNFD" />
      </Event>
      <Event ID="{HEX-ID}" Name="IND" Comment="Indication from Plug">
        <With Var="INDD" />
      </Event>
    </EventOutputs>
    <InputVars>
      <VarDeclaration ID="{HEX-ID}" Name="REQD" Type="STRING[15]"
                      Comment="Request Data from Socket" />
      <VarDeclaration ID="{HEX-ID}" Name="RSPD" Type="STRING[15]"
                      Comment="Response Data from Socket" />
    </InputVars>
    <OutputVars>
      <VarDeclaration ID="{HEX-ID}" Name="CNFD" Type="STRING[15]"
                      Comment="Confirmation Data from Plug" />
      <VarDeclaration ID="{HEX-ID}" Name="INDD" Type="STRING[15]"
                      Comment="Indication Data from Plug" />
    </OutputVars>
  </InterfaceList>
  <Service RightInterface="PLUG" LeftInterface="SOCKET">
    <ServiceSequence Name="request_confirm">
      <ServiceTransaction>
        <InputPrimitive Interface="SOCKET" Event="REQ" Parameters="REQD" />
        <OutputPrimitive Interface="PLUG" Event="REQ" Parameters="REQD" />
      </ServiceTransaction>
      <ServiceTransaction>
        <InputPrimitive Interface="PLUG" Event="CNF" Parameters="CNFD" />
        <OutputPrimitive Interface="SOCKET" Event="CNF" Parameters="CNFD" />
      </ServiceTransaction>
    </ServiceSequence>
    <ServiceSequence Name="indication_response">
      <ServiceTransaction>
        <InputPrimitive Interface="PLUG" Event="IND" Parameters="INDD" />
        <OutputPrimitive Interface="SOCKET" Event="IND" Parameters="INDD" />
      </ServiceTransaction>
      <ServiceTransaction>
        <InputPrimitive Interface="SOCKET" Event="RSP" Parameters="RSPD" />
        <OutputPrimitive Interface="PLUG" Event="RSP" Parameters="RSPD" />
      </ServiceTransaction>
    </ServiceSequence>
  </Service>
</AdapterType>
```

---

## Socket vs Plug

| Side | Sees Interface As | Usage |
|------|------------------|-------|
| **Socket** | As defined | Provider/Server side |
| **Plug** | Reversed | Consumer/Client side |

### Example in FBNetwork

```xml
<!-- Socket adapter (provider) -->
<AdapterDeclaration Name="ServerPort" Type="MyAdapter" Namespace="MyLib" IsPlug="false" />

<!-- Plug adapter (consumer) -->
<AdapterDeclaration Name="ClientPort" Type="MyAdapter" Namespace="MyLib" IsPlug="true" />
```

---

## Service Sequences

The `<Service>` element defines communication patterns:

### Request-Confirm Pattern

Client sends request, server confirms:

```xml
<ServiceSequence Name="request_confirm">
  <ServiceTransaction>
    <InputPrimitive Interface="SOCKET" Event="REQ" Parameters="REQD" />
    <OutputPrimitive Interface="PLUG" Event="REQ" Parameters="REQD" />
  </ServiceTransaction>
  <ServiceTransaction>
    <InputPrimitive Interface="PLUG" Event="CNF" Parameters="CNFD" />
    <OutputPrimitive Interface="SOCKET" Event="CNF" Parameters="CNFD" />
  </ServiceTransaction>
</ServiceSequence>
```

### Indication-Response Pattern

Server sends indication, client responds:

```xml
<ServiceSequence Name="indication_response">
  <ServiceTransaction>
    <InputPrimitive Interface="PLUG" Event="IND" Parameters="INDD" />
    <OutputPrimitive Interface="SOCKET" Event="IND" Parameters="INDD" />
  </ServiceTransaction>
  <ServiceTransaction>
    <InputPrimitive Interface="SOCKET" Event="RSP" Parameters="RSPD" />
    <OutputPrimitive Interface="PLUG" Event="RSP" Parameters="RSPD" />
  </ServiceTransaction>
</ServiceSequence>
```

---

## Standard Event Names

| Event | Direction | Purpose |
|-------|-----------|---------|
| REQ | Socket → Plug | Request |
| CNF | Plug → Socket | Confirmation |
| IND | Plug → Socket | Indication |
| RSP | Socket → Plug | Response |

---

## dfbproj Registration

```xml
<ItemGroup>
  <None Include="{Name}.doc.xml">
    <DependentUpon>{Name}.adp</DependentUpon>
  </None>
</ItemGroup>
<ItemGroup>
  <Compile Include="{Name}.adp">
    <IEC61499Type>Adapter</IEC61499Type>
  </Compile>
</ItemGroup>
```

---

## Using Adapters in FBs

### In InterfaceList

```xml
<InterfaceList>
  <!-- ... events and vars ... -->
  <AdapterDeclarations>
    <AdapterDeclaration ID="{HEX-ID}" Name="DataPort" Type="MyAdapter"
                        Namespace="MyLib" IsPlug="false" Comment="Data interface" />
  </AdapterDeclarations>
</InterfaceList>
```

### Connecting Adapters

In FBNetwork, adapter connections use special syntax:

```xml
<AdapterConnections>
  <Connection Source="$FB1.DataPort" Destination="$FB2.DataPort" />
</AdapterConnections>
```

---

## Common Rules

See [common-rules.md](../eae-skill-router/references/common-rules.md) for:
- ID generation
- dfbproj registration patterns

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Adapter won't load | Use `.adp` extension, not `.fbt` |
| Standard error | Use `Standard="61499-1"`, not `61499-2` |
| Missing Service | Adapters require `<Service>` element |
| Wrong root element | Use `<AdapterType>`, not `<FBType>` |

---

## Example: Command Adapter

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE AdapterType SYSTEM "../LibraryElement.dtd">
<AdapterType Name="CommandAdapter" Namespace="MyLibrary"
             GUID="a1b2c3d4-e5f6-7890-abcd-ef1234567890" Comment="Command interface">
  <Identification Standard="61499-1" />
  <VersionInfo Organization="MyOrg" Version="1.0" Author="Claude"
               Date="01/16/2026" Remarks="Initial" />
  <CompilerInfo />
  <InterfaceList>
    <EventInputs>
      <Event ID="1111111111111111" Name="CMD" Comment="Command from controller">
        <With Var="CommandCode" />
        <With Var="Parameter" />
      </Event>
    </EventInputs>
    <EventOutputs>
      <Event ID="2222222222222222" Name="DONE" Comment="Command completed">
        <With Var="Result" />
        <With Var="ErrorCode" />
      </Event>
    </EventOutputs>
    <InputVars>
      <VarDeclaration ID="3333333333333333" Name="CommandCode" Type="INT" />
      <VarDeclaration ID="4444444444444444" Name="Parameter" Type="REAL" />
    </InputVars>
    <OutputVars>
      <VarDeclaration ID="5555555555555555" Name="Result" Type="REAL" />
      <VarDeclaration ID="6666666666666666" Name="ErrorCode" Type="INT" />
    </OutputVars>
  </InterfaceList>
  <Service RightInterface="PLUG" LeftInterface="SOCKET">
    <ServiceSequence Name="execute_command">
      <ServiceTransaction>
        <InputPrimitive Interface="SOCKET" Event="CMD" Parameters="CommandCode,Parameter" />
        <OutputPrimitive Interface="PLUG" Event="CMD" Parameters="CommandCode,Parameter" />
      </ServiceTransaction>
      <ServiceTransaction>
        <InputPrimitive Interface="PLUG" Event="DONE" Parameters="Result,ErrorCode" />
        <OutputPrimitive Interface="SOCKET" Event="DONE" Parameters="Result,ErrorCode" />
      </ServiceTransaction>
    </ServiceSequence>
  </Service>
</AdapterType>
```

---

## Validation

After creating an Adapter, validate it:

```bash
python ../eae-skill-router/scripts/validate_block.py --type adapter MyAdapter.adp
```

Generate IDs:

```bash
python ../eae-skill-router/scripts/generate_ids.py --hex 8 --guid 1
```

---

## Integration with Validation Skills

### Naming Validation

Use [eae-naming-validator](../eae-naming-validator/SKILL.md) to ensure compliance with SE Application Design Guidelines:

**Key Naming Rules for Adapter:**
- Adapter name: **IPascalCase** with uppercase 'I' prefix (e.g., `IPv`, `IAnalogValue`, `IMotorControl`)
- Events: SNAKE_CASE (e.g., `REQ`, `CNF`, `IND`, `RSP`)
- Variables: PascalCase (e.g., `CommandCode`, `Parameter`, `Result`)

**Validate naming before creation:**
```bash
# Validate adapter name (must have 'I' prefix)
python ../eae-naming-validator/scripts/validate_names.py \
  --app-dir IEC61499 \
  --artifact-type Adapter \
  --name IMyAdapter
```

**Reference:** EAE_ADG EIO0000004686.06, Section 1.5 (Adapter Naming Convention)

---

## Best Practices from EAE ADG

### 1. Naming Conventions (SE ADG Section 1.5)

**Adapter Naming:**
- **ALWAYS use IPascalCase** with uppercase 'I' prefix
- The 'I' denotes "Interface" (socket/plug pattern)
- Examples: `IPv`, `IAnalogValue`, `IMotorControl`, `ICommandInterface`

**Variable Naming:**
- Use PascalCase for all adapter variables: `CommandCode`, `Parameter`, `Result`
- Use descriptive names (avoid `Data1`, `Var1`)
- Include data types in complex names: `PositionValue`, `ErrorCode`, `StatusText`

**Event Naming:**
- Use standard IEC 61499 event names: `REQ`, `CNF`, `IND`, `RSP`
- For custom events, use SNAKE_CASE: `START_COMMAND`, `ABORT_REQUEST`
- Avoid generic names: `E1`, `DO1`, `OUTPUT`

**Reference:** EAE_ADG EIO0000004686.06, Section 1.5

### 2. Service Sequence Design

**Communication Patterns:**
- Use Request-Confirm for client-initiated operations
- Use Indication-Response for server-initiated notifications
- Keep service sequences simple (2-4 transactions typical)
- Document the protocol flow in comments

**Service Transaction Guidelines:**
- Always pair InputPrimitive with OutputPrimitive
- Match Parameters in both Socket and Plug sides
- Use semantic names for ServiceSequence (e.g., `execute_command`, not `seq1`)

### 3. Adapter Reusability

**Design for Reuse:**
- Keep adapters generic (avoid application-specific logic)
- Use standard data types (BOOL, INT, REAL, STRING)
- Define clear interface contracts in comments
- Provide example usage in .doc.xml

**When to Create New Adapter:**
- Standardize repeated communication patterns
- Define reusable interfaces across FB types
- Separate concerns between provider and consumer
- Enable plug-and-play component replacement

---

## Anti-Patterns

### 1. Naming Anti-Patterns

❌ **Missing 'I' Prefix**
```xml
<!-- BAD: Adapter without 'I' prefix -->
<AdapterType Name="MotorControl" ...>
```

✅ **Correct IPascalCase**
```xml
<!-- Correct: Adapter with uppercase 'I' prefix -->
<AdapterType Name="IMotorControl" ...>
```

❌ **Lowercase 'i' Prefix**
```xml
<!-- BAD: Lowercase 'i' -->
<AdapterType Name="iMotorControl" ...>
```

❌ **Generic Variable Names**
```xml
<!-- BAD: Non-descriptive variable names -->
<VarDeclaration Name="Data1" Type="INT" />
<VarDeclaration Name="Value" Type="REAL" />
```

✅ **Descriptive Variable Names**
```xml
<VarDeclaration Name="CommandCode" Type="INT" />
<VarDeclaration Name="PositionValue" Type="REAL" />
```

### 2. Structure Anti-Patterns

❌ **Wrong Root Element**
```xml
<!-- BAD: Using FBType instead of AdapterType -->
<FBType Name="IMyAdapter" ...>
```

✅ **Correct Root Element**
```xml
<AdapterType Name="IMyAdapter" ...>
```

❌ **Wrong Standard**
```xml
<!-- BAD: Using 61499-2 -->
<Identification Standard="61499-2" />
```

✅ **Correct Standard**
```xml
<!-- Adapters use 61499-1 -->
<Identification Standard="61499-1" />
```

❌ **Wrong File Extension**
```
IMyAdapter.fbt    ❌ Wrong extension
```

✅ **Correct File Extension**
```
IMyAdapter.adp    ✅ Correct extension
```

❌ **Missing Service Element**
```xml
<AdapterType Name="IMyAdapter" ...>
  <InterfaceList>...</InterfaceList>
  <!-- Missing <Service> element! -->
</AdapterType>
```

✅ **Service Element Required**
```xml
<AdapterType Name="IMyAdapter" ...>
  <InterfaceList>...</InterfaceList>
  <Service RightInterface="PLUG" LeftInterface="SOCKET">
    <ServiceSequence Name="request_confirm">...</ServiceSequence>
  </Service>
</AdapterType>
```

### 3. Service Sequence Anti-Patterns

❌ **Unmatched Parameters**
```xml
<!-- BAD: Parameters don't match -->
<ServiceTransaction>
  <InputPrimitive Interface="SOCKET" Event="REQ" Parameters="Data1,Data2" />
  <OutputPrimitive Interface="PLUG" Event="REQ" Parameters="Data1" />  <!-- Missing Data2! -->
</ServiceTransaction>
```

✅ **Matched Parameters**
```xml
<ServiceTransaction>
  <InputPrimitive Interface="SOCKET" Event="REQ" Parameters="Data1,Data2" />
  <OutputPrimitive Interface="PLUG" Event="REQ" Parameters="Data1,Data2" />
</ServiceTransaction>
```

❌ **Overly Complex Service Sequences**
```xml
<!-- BAD: 10+ ServiceTransaction elements in one sequence -->
<ServiceSequence Name="complex_protocol">
  <!-- Too many steps - hard to understand and maintain -->
</ServiceSequence>
```

✅ **Simple, Clear Service Sequences**
```xml
<!-- Keep sequences simple (2-4 transactions) -->
<ServiceSequence Name="request_confirm">
  <ServiceTransaction>...</ServiceTransaction>
  <ServiceTransaction>...</ServiceTransaction>
</ServiceSequence>
```

### 4. Reusability Anti-Patterns

❌ **Application-Specific Adapter**
```xml
<!-- BAD: Too specific to one application -->
<AdapterType Name="ILine3Tank5Valve2Control" ...>
```

✅ **Generic, Reusable Adapter**
```xml
<!-- Generic valve control interface -->
<AdapterType Name="IValveControl" ...>
```

❌ **Using Custom Data Types in Adapters**
```xml
<!-- BAD: Reduces reusability -->
<VarDeclaration Name="Config" Type="MyCustomConfig" Namespace="MyApp" />
```

✅ **Using Standard Data Types**
```xml
<!-- Better: Use standard types or SE.App2Base types -->
<VarDeclaration Name="ConfigCode" Type="INT" />
```

---

## Verification Checklist

Before committing your Adapter:

**Naming (run eae-naming-validator):**
- [ ] Adapter name uses IPascalCase with uppercase 'I' prefix
- [ ] All variables use PascalCase
- [ ] Events use SNAKE_CASE or standard names (REQ, CNF, IND, RSP)

**Structure:**
- [ ] Root element is `<AdapterType>` (NOT `<FBType>`)
- [ ] File extension is `.adp` (NOT `.fbt`)
- [ ] Uses `Standard="61499-1"` (NOT `61499-2`)
- [ ] `<Service>` element is present with at least one ServiceSequence

**Service Sequences:**
- [ ] All InputPrimitive/OutputPrimitive pairs have matching Parameters
- [ ] ServiceSequence names are descriptive (not `seq1`, `seq2`)
- [ ] Sequences are simple (2-4 transactions typical)

**Reusability:**
- [ ] Adapter name is generic (not application-specific)
- [ ] Uses standard data types (BOOL, INT, REAL, STRING)
- [ ] Interface contract documented in comments

**Registration:**
- [ ] Registered in .dfbproj with `IEC61499Type="Adapter"`
- [ ] .doc.xml file created and registered as DependentUpon

**Validation:**
- [ ] `python scripts/validate_adapter.py {Name}.adp` passes
- [ ] `python ../eae-skill-router/scripts/validate_block.py --type adapter {Name}.adp` passes

---

## Scripts

### Validate Adapter

Validate adapter files against EAE rules and SE ADG naming conventions:

```bash
# Validate a single adapter
python scripts/validate_adapter.py IEC61499/IMotorControl.adp

# Validate all adapters in directory
python scripts/validate_adapter.py IEC61499/

# JSON output for CI/CD
python scripts/validate_adapter.py IEC61499/ --json

# Strict mode (treat warnings as errors)
python scripts/validate_adapter.py IEC61499/ --strict
```

**Validates:**
- Root element is AdapterType (NOT FBType)
- Standard is "61499-1" (NOT 61499-2)
- File extension is .adp
- IPascalCase naming with uppercase 'I' prefix
- GUID is present
- Service element and ServiceSequence consistency
- Event and variable naming conventions

**Exit codes:**
- `0` - All validations passed
- `1` - Error running validation
- `10` - Validation warnings (non-blocking)
- `11` - Validation errors (blocking)

---

## Related Skills

| Skill | When to Use |
|-------|-------------|
| [eae-naming-validator](../eae-naming-validator/SKILL.md) | Validate adapter naming compliance (IPascalCase) |
| [eae-basic-fb](../eae-basic-fb/SKILL.md) | Create FBs that use adapters |
| [eae-composite-fb](../eae-composite-fb/SKILL.md) | Create composite FBs with adapter connections |
| [eae-cat](../eae-cat/SKILL.md) | Create CAT blocks with adapters |

---

## Templates

- [adapter.xml](../eae-skill-router/assets/templates/adapter.xml)
- [doc.xml](../eae-skill-router/assets/templates/doc.xml)
