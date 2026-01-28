---
name: eae-datatype
description: >
  Create custom DataTypes in EAE including structures, enumerations, arrays,
  and subranges.
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
# EAE DataType Creation

Create or modify custom data types: structures, enumerations, arrays, and subranges.

> **CRITICAL RULE:** ALWAYS use this skill for ANY operation on DataType files.
> - Creating new DataTypes
> - Modifying existing DataTypes (adding fields, enum values, etc.)
> - NEVER directly edit `.dt` files outside of this skill

**DataType Key Differences:**
- Uses `DataType.dtd` (NOT LibraryElement.dtd)
- Uses `Standard="1131-3"` (IEC 61131-3)
- Has **NO GUID** attribute
- Located in `IEC61499/DataType/` subfolder
- Uses `.dt` extension (NOT `.dtp`)

## Quick Start

```
User: Create an enumeration for machine states: Idle, Running, Error
Claude: [Creates IEC61499/DataType/MachineState.dt]
```

## Triggers

- `/eae-datatype`
- `/eae-datatype --register-only` - Register existing DataType (used by eae-fork orchestration)
- "create enum"
- "modify enum"
- "create structure"
- "modify structure"
- "add field to structure"
- "create data type"
- "create array type"

---

## Register-Only Mode (for eae-fork Orchestration)

When called with `--register-only`, this skill skips file creation and only performs dfbproj registration. This mode is used by **eae-fork** to complete the fork workflow after file transformation.

```
/eae-datatype --register-only {TypeName} {Namespace}
```

**What --register-only does:**

1. **Registers in dfbproj** - Adds ItemGroup entries for DataType visibility

**What --register-only does NOT do:**

- Create IEC61499 files (.dt, etc.) - already done by eae-fork
- Update namespaces - already done by eae-fork

### Usage

```bash
# Register a forked DataType
python ../eae-skill-router/scripts/register_dfbproj.py MyStatus SE.ScadapackWWW --type datatype

# Verify registration
python ../eae-skill-router/scripts/register_dfbproj.py MyStatus SE.ScadapackWWW --type datatype --verify
```

---

## Modification Workflow

When modifying an existing DataType:

1. Read the existing `.dt` file to understand current structure
2. Identify what needs to be added/changed
3. For structures: add/modify VarDeclaration elements
4. For enums: add/modify EnumeratedValue elements
5. For arrays: modify BaseType or Subrange
6. For subranges: modify limits or InitialValue

---

## DataType Subtypes

| Subtype | Element | Use Case |
|---------|---------|----------|
| **Structure** | `<StructuredType>` | Group related fields |
| **Enumeration** | `<EnumeratedType>` | Named value sets |
| **Array** | `<ArrayType>` | Fixed-size collections |
| **Subrange** | `<SubrangeType>` | Constrained numeric range |

---

## Files Generated

| File | Purpose |
|------|---------|
| `{Name}.dt` | Main type definition |
| `{Name}.doc.xml` | Documentation |

**Location:** `IEC61499/DataType/` (NOT `IEC61499/`)

---

## Critical Rules

| Rule | Value |
|------|-------|
| DOCTYPE | `<!DOCTYPE DataType SYSTEM "../DataType.dtd">` |
| Standard | `<Identification Standard="1131-3" />` |
| GUID | **None** (DataTypes don't have GUIDs) |
| Extension | `.dt` (NOT `.dtp`) |
| Location | `IEC61499/DataType/` subfolder |

---

## Structure Type

Groups related fields together:

```xml
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE DataType SYSTEM "../DataType.dtd">
<DataType Name="MotorData" Namespace="MyLibrary" Comment="Motor parameters">
  <Identification Standard="1131-3" />
  <VersionInfo Organization="MyOrg" Version="1.0" Author="Claude"
               Date="01/16/2026" Remarks="Initial" />
  <CompilerInfo />
  <StructuredType>
    <VarDeclaration Name="Speed" Type="REAL" Comment="Motor speed in RPM" />
    <VarDeclaration Name="Current" Type="REAL" Comment="Current in Amps" />
    <VarDeclaration Name="Running" Type="BOOL" Comment="Motor running state" />
    <VarDeclaration Name="ErrorCode" Type="INT" Comment="Error code" />
  </StructuredType>
</DataType>
```

### Nested Types

```xml
<VarDeclaration Name="Status" Type="MachineStatus" Namespace="MyLibrary" />
```

---

## Enumeration Type

Named value sets:

```xml
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE DataType SYSTEM "../DataType.dtd">
<DataType Name="MachineState" Namespace="MyLibrary" Comment="Machine states">
  <Identification Standard="1131-3" />
  <VersionInfo Organization="MyOrg" Version="1.0" Author="Claude"
               Date="01/16/2026" Remarks="Initial" />
  <CompilerInfo />
  <EnumeratedType>
    <EnumeratedValue Name="Idle" />
    <EnumeratedValue Name="Starting" />
    <EnumeratedValue Name="Running" />
    <EnumeratedValue Name="Stopping" />
    <EnumeratedValue Name="Error" />
    <EnumeratedValue Name="Maintenance" />
  </EnumeratedType>
</DataType>
```

---

## Array Type

Fixed-size collections:

```xml
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE DataType SYSTEM "../DataType.dtd">
<DataType Name="SensorArray" Namespace="MyLibrary" Comment="Array of 10 sensor values">
  <Identification Standard="1131-3" />
  <VersionInfo Organization="MyOrg" Version="1.0" Author="Claude"
               Date="01/16/2026" Remarks="Initial" />
  <CompilerInfo />
  <ArrayType BaseType="REAL" Namespace="">
    <Subrange LowerLimit="0" UpperLimit="9" />
  </ArrayType>
</DataType>
```

### Array of Custom Types

```xml
<ArrayType BaseType="MotorData" Namespace="MyLibrary">
  <Subrange LowerLimit="0" UpperLimit="3" />
</ArrayType>
```

---

## Subrange Type

Constrained numeric values:

```xml
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE DataType SYSTEM "../DataType.dtd">
<DataType Name="Percentage" Namespace="MyLibrary" Comment="0-100 range">
  <Identification Standard="1131-3" />
  <VersionInfo Organization="MyOrg" Version="1.0" Author="Claude"
               Date="01/16/2026" Remarks="Initial" />
  <CompilerInfo />
  <SubrangeType BaseType="INT" InitialValue="0">
    <Subrange LowerLimit="0" UpperLimit="100" />
  </SubrangeType>
</DataType>
```

---

## dfbproj Registration

```xml
<ItemGroup>
  <None Include="DataType\{Name}.doc.xml">
    <DependentUpon>{Name}.dt</DependentUpon>
  </None>
</ItemGroup>
<ItemGroup>
  <Compile Include="DataType\{Name}.dt">
    <IEC61499Type>DataType</IEC61499Type>
  </Compile>
</ItemGroup>
```

**Note:** Path includes `DataType\` prefix.

---

## Built-in Types Reference

| Type | Description | Example |
|------|-------------|---------|
| BOOL | Boolean | TRUE, FALSE |
| INT | 16-bit signed | -32768 to 32767 |
| DINT | 32-bit signed | Larger integers |
| REAL | 32-bit float | 3.14159 |
| LREAL | 64-bit float | High precision |
| STRING | Text | 'Hello' |
| STRING[n] | Fixed-length | STRING[15] |
| TIME | Duration | T#5s |
| DATE | Date | D#2026-01-16 |

---

## Common Rules

See [common-rules.md](../eae-skill-router/references/common-rules.md) for:
- dfbproj registration patterns
- Documentation file template

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| DataType not found | Ensure file is in `DataType/` subfolder |
| Wrong extension | Use `.dt`, not `.dtp` |
| Load error | Use `DataType.dtd`, not `LibraryElement.dtd` |
| Standard error | Use `Standard="1131-3"`, not `61499-2` |
| GUID error | DataTypes should NOT have GUID |

---

## Validation

After creating a DataType, validate it:

```bash
python ../eae-skill-router/scripts/validate_block.py --type datatype MyType.dt
```

**Note:** DataTypes do not require ID generation (no GUIDs or hex IDs).

---

## Templates

- [datatype-structure.xml](../eae-skill-router/assets/templates/datatype-structure.xml)
- [datatype-enum.xml](../eae-skill-router/assets/templates/datatype-enum.xml)
- [datatype-array.xml](../eae-skill-router/assets/templates/datatype-array.xml)
- [datatype-subrange.xml](../eae-skill-router/assets/templates/datatype-subrange.xml)
- [doc.xml](../eae-skill-router/assets/templates/doc.xml)

---

## Integration with Validation Skills

### Naming Validation

Use [eae-naming-validator](../eae-naming-validator/SKILL.md) to ensure compliance with SE Application Design Guidelines:

**Key Naming Rules for DataTypes (SE ADG EIO0000004686.06 Section 1.5):**

| DataType | Convention | Pattern | Example |
|----------|------------|---------|---------|
| Structure | strPascalCase | `str[A-Z][a-zA-Z0-9]*` | `strMotorData`, `strAlarmConfig` |
| Enumeration | ePascalCase | `e[A-Z][a-zA-Z0-9]*` | `eMachineState`, `eProductType` |
| Array | arrPascalCase | `arr[A-Z][a-zA-Z0-9]*` | `arrSensorValues`, `arrMotorData` |
| Subrange | (context-dependent) | PascalCase | `Percentage`, `ValidRange` |

**Validate naming before creation:**
```bash
python ../eae-naming-validator/scripts/validate_names.py \
  --app-dir IEC61499/MyLibrary \
  --artifact-type DataType
```

### Validation After Creation

```bash
# Validate DataType structure
python scripts/validate_datatype.py IEC61499/DataType/strMotorData.dt

# Validate with JSON output for CI/CD
python scripts/validate_datatype.py IEC61499/DataType/*.dt --json
```

---

## Best Practices from EAE ADG

### 1. Naming Conventions (Hungarian Notation)

**Always use Hungarian prefixes for DataTypes:**

| Prefix | Type | Example |
|--------|------|---------|
| `str` | Structure | `strMotorConfig` |
| `e` | Enumeration | `eProductState` |
| `arr` | Array | `arrSensorBuffer` |
| `a` | Array (alternative) | `aValues` |

```xml
<!-- CORRECT: Hungarian notation -->
<DataType Name="strMotorData" Namespace="MyLibrary">

<!-- INCORRECT: No prefix -->
<DataType Name="MotorData" Namespace="MyLibrary">
```

### 2. Field Naming in Structures

**Interface fields:** PascalCase
```xml
<VarDeclaration Name="Speed" Type="REAL" />
<VarDeclaration Name="MaxTemperature" Type="REAL" />
```

**Internal/private fields:** camelCase
```xml
<VarDeclaration Name="lastValue" Type="REAL" />
<VarDeclaration Name="errorCount" Type="INT" />
```

### 3. Enumeration Values

**Use meaningful, action-oriented names:**
```xml
<EnumeratedType>
  <EnumeratedValue Name="Idle" />
  <EnumeratedValue Name="Starting" />
  <EnumeratedValue Name="Running" />
  <EnumeratedValue Name="Stopping" />
  <EnumeratedValue Name="Faulted" />
</EnumeratedType>
```

**Avoid generic names:**
```xml
<!-- BAD -->
<EnumeratedValue Name="State1" />
<EnumeratedValue Name="State2" />
```

### 4. Documentation

**Always include meaningful Comment attributes:**
```xml
<DataType Name="strMotorData" Namespace="MyLibrary"
          Comment="Motor operating parameters and status">
  <VarDeclaration Name="Speed" Type="REAL" Comment="Motor speed in RPM" />
  <VarDeclaration Name="Current" Type="REAL" Comment="Motor current in Amps" />
</DataType>
```

### 5. Type Selection

| Need | Use Type | Rationale |
|------|----------|-----------|
| Related fields | Structure | Groups logically connected data |
| Fixed set of states | Enumeration | Type-safe, self-documenting |
| Multiple values of same type | Array | Efficient memory, iteration |
| Bounded numeric values | Subrange | Compiler-enforced constraints |

---

## Anti-Patterns

### 1. Naming Anti-Patterns

**Missing Hungarian Prefix**
```xml
<!-- BAD: No 'str' prefix for structure -->
<DataType Name="MotorData" ...>
  <StructuredType>

<!-- CORRECT: Hungarian prefix -->
<DataType Name="strMotorData" ...>
  <StructuredType>
```

**Missing 'e' Prefix for Enum**
```xml
<!-- BAD: No 'e' prefix for enumeration -->
<DataType Name="MachineState" ...>
  <EnumeratedType>

<!-- CORRECT: Hungarian prefix -->
<DataType Name="eMachineState" ...>
  <EnumeratedType>
```

**Inconsistent Field Naming**
```xml
<!-- BAD: Mixed conventions -->
<StructuredType>
  <VarDeclaration Name="speed" Type="REAL" />        <!-- lowercase -->
  <VarDeclaration Name="MAX_TEMP" Type="REAL" />     <!-- SCREAMING_CASE -->
  <VarDeclaration Name="errorCode" Type="INT" />     <!-- camelCase -->
</StructuredType>

<!-- CORRECT: Consistent PascalCase for interface fields -->
<StructuredType>
  <VarDeclaration Name="Speed" Type="REAL" />
  <VarDeclaration Name="MaxTemp" Type="REAL" />
  <VarDeclaration Name="ErrorCode" Type="INT" />
</StructuredType>
```

### 2. Structure Anti-Patterns

**Wrong DOCTYPE**
```xml
<!-- BAD: Using LibraryElement.dtd -->
<!DOCTYPE DataType SYSTEM "../LibraryElement.dtd">

<!-- CORRECT: DataType.dtd -->
<!DOCTYPE DataType SYSTEM "../DataType.dtd">
```

**Wrong Standard**
```xml
<!-- BAD: Using 61499-2 -->
<Identification Standard="61499-2" />

<!-- CORRECT: IEC 61131-3 -->
<Identification Standard="1131-3" />
```

**Including GUID**
```xml
<!-- BAD: DataTypes should NOT have GUIDs -->
<DataType Name="strConfig" GUID="12345678-1234-...">

<!-- CORRECT: No GUID attribute -->
<DataType Name="strConfig" Namespace="MyLibrary">
```

**Wrong Extension**
```
BAD:  strMotorData.dtp
CORRECT: strMotorData.dt
```

**Wrong Location**
```
BAD:  IEC61499/strMotorData.dt
CORRECT: IEC61499/DataType/strMotorData.dt
```

### 3. Enumeration Anti-Patterns

**Generic State Names**
```xml
<!-- BAD: Non-descriptive -->
<EnumeratedType>
  <EnumeratedValue Name="State0" />
  <EnumeratedValue Name="State1" />
  <EnumeratedValue Name="State2" />
</EnumeratedType>

<!-- CORRECT: Meaningful names -->
<EnumeratedType>
  <EnumeratedValue Name="Idle" />
  <EnumeratedValue Name="Active" />
  <EnumeratedValue Name="Complete" />
</EnumeratedType>
```

**Too Many Values Without Grouping**
```xml
<!-- BAD: 20+ values without structure -->
<EnumeratedType>
  <!-- Consider using multiple enums or a different approach -->
</EnumeratedType>

<!-- CORRECT: Group related states or use bit flags -->
```

### 4. Array Anti-Patterns

**Zero-Length Arrays**
```xml
<!-- BAD: Empty array -->
<ArrayType BaseType="REAL">
  <Subrange LowerLimit="0" UpperLimit="0" />
</ArrayType>

<!-- CORRECT: At least 1 element -->
<ArrayType BaseType="REAL">
  <Subrange LowerLimit="0" UpperLimit="9" />
</ArrayType>
```

**Excessive Array Size**
```xml
<!-- BAD: Very large array (memory concerns) -->
<ArrayType BaseType="REAL">
  <Subrange LowerLimit="0" UpperLimit="9999" />
</ArrayType>

<!-- CORRECT: Reasonable size, consider chunking if needed -->
<ArrayType BaseType="REAL">
  <Subrange LowerLimit="0" UpperLimit="99" />
</ArrayType>
```

---

## Verification Checklist

Before deployment, verify:

### Structure
- [ ] DOCTYPE references `DataType.dtd`
- [ ] Standard is `1131-3` (NOT 61499-2)
- [ ] **NO GUID** attribute present
- [ ] File extension is `.dt`
- [ ] Located in `IEC61499/DataType/` folder
- [ ] Name uses `str` prefix (strPascalCase)
- [ ] All fields have meaningful names
- [ ] All fields have Comment attributes
- [ ] Registered in `.dfbproj` with path `DataType\{Name}.dt`

### Enumeration
- [ ] Name uses `e` prefix (ePascalCase)
- [ ] All values have meaningful names
- [ ] No duplicate values
- [ ] Reasonable number of values (<20 typical)

### Array
- [ ] Name uses `arr` or `a` prefix
- [ ] LowerLimit < UpperLimit
- [ ] BaseType exists and is valid
- [ ] Namespace specified if custom BaseType

### Subrange
- [ ] LowerLimit < UpperLimit
- [ ] InitialValue within range
- [ ] BaseType is numeric (INT, DINT, REAL, etc.)

### Naming Validation
```bash
# Run naming validator
python ../eae-naming-validator/scripts/validate_names.py \
  --app-dir IEC61499/MyLibrary \
  --artifact-type DataType \
  --json
```

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [eae-skill-router](../eae-skill-router/SKILL.md) | Parent skill, routing logic |
| [eae-naming-validator](../eae-naming-validator/SKILL.md) | Validate naming conventions |
| [eae-basic-fb](../eae-basic-fb/SKILL.md) | Uses DataTypes in VarDeclarations |
| [eae-composite-fb](../eae-composite-fb/SKILL.md) | Uses DataTypes in FBNetwork |
| [eae-cat](../eae-cat/SKILL.md) | Uses DataTypes for HMI binding |
| [eae-fork](../eae-fork/SKILL.md) | Fork DataTypes from SE libraries |
