---
name: eae-basic-fb
description: >
  Create Basic Function Blocks in EAE with ECC (Execution Control Chart)
  state machine and ST algorithms.
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
# EAE Basic Function Block Creation

Create or modify Basic FBs with state machine logic (ECC) and Structured Text algorithms.

> **CRITICAL RULE:** ALWAYS use this skill for ANY operation on Basic FB files.
> - Creating new Basic FBs
> - Modifying existing Basic FBs (adding events, variables, states, algorithms)
> - NEVER directly edit `.fbt` files outside of this skill

**Basic FB = State Machine + Algorithms**
- ECC (Execution Control Chart) for state transitions
- Algorithms in ST (Structured Text) for computation
- No internal FBNetwork (unlike Composite)

## Quick Start

```
User: Create a Basic FB called Calculator in MyLibrary that multiplies two REALs
Claude: [Creates .fbt with ECC + REQ algorithm: Result := Value1 * Value2]
```

## Triggers

- `/eae-basic-fb`
- `/eae-basic-fb --register-only` - Register existing Basic FB (used by eae-fork orchestration)
- "create basic FB"
- "modify basic FB"
- "add event to basic FB"
- "add variable to basic FB"
- "create block with algorithm"
- "create state machine FB"

---

## Register-Only Mode (for eae-fork Orchestration)

When called with `--register-only`, this skill skips file creation and only performs dfbproj registration. This mode is used by **eae-fork** to complete the fork workflow after file transformation.

```
/eae-basic-fb --register-only {BlockName} {Namespace}
```

**What --register-only does:**

1. **Registers in dfbproj** - Adds ItemGroup entries for Basic FB visibility

**What --register-only does NOT do:**

- Create IEC61499 files (.fbt, etc.) - already done by eae-fork
- Update namespaces - already done by eae-fork

### Usage

```bash
# Register a forked Basic FB
python ../eae-skill-router/scripts/register_dfbproj.py MyBasicFB SE.ScadapackWWW --type basic

# Verify registration
python ../eae-skill-router/scripts/register_dfbproj.py MyBasicFB SE.ScadapackWWW --type basic --verify
```

---

## Modification Workflow

When modifying an existing Basic FB:

1. Read the existing `.fbt` file to understand current structure
2. Identify what needs to be added/changed
3. Generate new hex IDs for any new Events or VarDeclarations
4. Update the `.fbt` file with the changes
5. Update event-variable associations (`<With Var="...">`) if needed
6. Add new ECC states/transitions if adding new events
7. Add/update algorithms if needed

---

## Files Generated

| File | Purpose |
|------|---------|
| `{Name}.fbt` | Main block with ECC + algorithms |
| `{Name}.doc.xml` | Documentation |
| `{Name}.meta.xml` | Metadata |

Location: `IEC61499/`

---

## Workflow

1. Generate GUID for FBType
2. Generate hex IDs for each Event and VarDeclaration
3. Create `.fbt` with:
   - `<!DOCTYPE FBType SYSTEM "../LibraryElement.dtd">`
   - `<Identification Standard="61499-2" />`
   - Standard events (INIT/REQ/INITO/CNF)
   - ECC with START, INIT, REQ states
   - Algorithms in ST
4. Create `.doc.xml` and `.meta.xml`
5. Register in `.dfbproj`

---

## Basic FB Template

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE FBType SYSTEM "../LibraryElement.dtd">
<FBType Name="{BlockName}" Namespace="{YourNamespace}"
        GUID="{NEW-GUID}" Comment="{Description}">
  <Identification Standard="61499-2" />
  <VersionInfo Organization="{Org}" Version="0.0" Author="{Author}"
               Date="{MM/DD/YYYY}" Remarks="Initial version" />
  <CompilerInfo />
  <InterfaceList>
    <EventInputs>
      <Event ID="{HEX-ID}" Name="INIT" Comment="Initialization Request">
        <With Var="QI" />
      </Event>
      <Event ID="{HEX-ID}" Name="REQ" Comment="Normal Execution Request">
        <With Var="QI" />
        <!-- Add With Var for each input used in REQ -->
      </Event>
    </EventInputs>
    <EventOutputs>
      <Event ID="{HEX-ID}" Name="INITO" Comment="Initialization Confirm">
        <With Var="QO" />
      </Event>
      <Event ID="{HEX-ID}" Name="CNF" Comment="Execution Confirmation">
        <With Var="QO" />
        <!-- Add With Var for each output produced -->
      </Event>
    </EventOutputs>
    <InputVars>
      <VarDeclaration ID="{HEX-ID}" Name="QI" Type="BOOL"
                      Comment="Input event qualifier" />
      <!-- Add custom inputs here -->
    </InputVars>
    <OutputVars>
      <VarDeclaration ID="{HEX-ID}" Name="QO" Type="BOOL"
                      Comment="Output event qualifier" />
      <!-- Add custom outputs here -->
    </OutputVars>
  </InterfaceList>
  <BasicFB>
    <ECC>
      <ECState Name="START" Comment="Initial State" x="552.9412" y="429.4117" />
      <ECState Name="INIT" Comment="Initialization" x="923.5294" y="141.1765">
        <ECAction Algorithm="INIT" Output="INITO" />
      </ECState>
      <ECState Name="REQ" Comment="Normal execution" x="217.647" y="752.9412">
        <ECAction Algorithm="REQ" Output="CNF" />
      </ECState>
      <ECTransition Source="START" Destination="INIT" Condition="INIT"
                    x="923.5294" y="429.4117" />
      <ECTransition Source="INIT" Destination="START" Condition="1"
                    x="552.9412" y="141.1765" />
      <ECTransition Source="START" Destination="REQ" Condition="REQ"
                    x="552.9412" y="600.0" />
      <ECTransition Source="REQ" Destination="START" Condition="1"
                    x="217.647" y="429.4117" />
    </ECC>
    <Algorithm Name="INIT" Comment="Initialization algorithm">
      <ST><![CDATA[QO := QI;]]></ST>
    </Algorithm>
    <Algorithm Name="REQ" Comment="Normally executed algorithm">
      <ST><![CDATA[QO := QI;
(* Add your logic here *)]]></ST>
    </Algorithm>
  </BasicFB>
</FBType>
```

**Note:** Basic FB does NOT have `Format="2.0"` attribute.

---

## ECC (Execution Control Chart)

The ECC defines the state machine:

### Standard States

| State | Purpose | Actions |
|-------|---------|---------|
| START | Initial state | None |
| INIT | Initialization | Run INIT algorithm, fire INITO |
| REQ | Normal execution | Run REQ algorithm, fire CNF |

### Standard Transitions

| From | To | Condition |
|------|-----|-----------|
| START | INIT | `INIT` event received |
| INIT | START | `1` (unconditional) |
| START | REQ | `REQ` event received |
| REQ | START | `1` (unconditional) |

### Adding Custom States

```xml
<ECState Name="CUSTOM_STATE" Comment="Custom state" x="800" y="500">
  <ECAction Algorithm="CUSTOM_ALG" Output="CUSTOM_EVENT" />
</ECState>
<ECTransition Source="START" Destination="CUSTOM_STATE"
              Condition="CUSTOM_INPUT_EVENT" x="700" y="450" />
```

---

## Algorithms (Structured Text)

Algorithms are written in ST (Structured Text):

```xml
<Algorithm Name="REQ" Comment="Calculation algorithm">
  <ST><![CDATA[
QO := QI;
Result := Value1 * Value2;
]]></ST>
</Algorithm>
```

### ST Syntax Basics

```st
(* Assignment *)
Result := Value1 + Value2;

(* Conditional *)
IF Condition THEN
  Output := TRUE;
ELSE
  Output := FALSE;
END_IF;

(* Loop *)
FOR i := 0 TO 10 DO
  Array[i] := 0;
END_FOR;
```

---

## Event-Variable Associations

Use `<With Var="...">` to associate variables with events:

```xml
<Event Name="REQ" Comment="Request">
  <With Var="QI" />      <!-- Always include QI -->
  <With Var="Value1" />  <!-- Input used in REQ -->
  <With Var="Value2" />  <!-- Input used in REQ -->
</Event>

<Event Name="CNF" Comment="Confirm">
  <With Var="QO" />      <!-- Always include QO -->
  <With Var="Result" />  <!-- Output produced by REQ -->
</Event>
```

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
</ItemGroup>
<ItemGroup>
  <Compile Include="{Name}.fbt">
    <IEC61499Type>Basic</IEC61499Type>
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

## Example: Multiplier Block

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE FBType SYSTEM "../LibraryElement.dtd">
<FBType Name="Multiplier" Namespace="MyLibrary"
        GUID="a1b2c3d4-e5f6-7890-abcd-ef1234567890" Comment="Multiplies two values">
  <Identification Standard="61499-2" />
  <VersionInfo Organization="MyOrg" Version="1.0" Author="Claude"
               Date="01/16/2026" Remarks="Initial" />
  <CompilerInfo />
  <InterfaceList>
    <EventInputs>
      <Event ID="1234567890ABCDEF" Name="INIT" Comment="Initialize">
        <With Var="QI" />
      </Event>
      <Event ID="ABCDEF1234567890" Name="REQ" Comment="Calculate">
        <With Var="QI" />
        <With Var="Value1" />
        <With Var="Value2" />
      </Event>
    </EventInputs>
    <EventOutputs>
      <Event ID="FEDCBA0987654321" Name="INITO" Comment="Init done">
        <With Var="QO" />
      </Event>
      <Event ID="0987654321FEDCBA" Name="CNF" Comment="Result ready">
        <With Var="QO" />
        <With Var="Result" />
      </Event>
    </EventOutputs>
    <InputVars>
      <VarDeclaration ID="1111111111111111" Name="QI" Type="BOOL" />
      <VarDeclaration ID="2222222222222222" Name="Value1" Type="REAL" />
      <VarDeclaration ID="3333333333333333" Name="Value2" Type="REAL" />
    </InputVars>
    <OutputVars>
      <VarDeclaration ID="4444444444444444" Name="QO" Type="BOOL" />
      <VarDeclaration ID="5555555555555555" Name="Result" Type="REAL" />
    </OutputVars>
  </InterfaceList>
  <BasicFB>
    <ECC>
      <ECState Name="START" x="550" y="430" />
      <ECState Name="INIT" x="920" y="140">
        <ECAction Algorithm="INIT" Output="INITO" />
      </ECState>
      <ECState Name="REQ" x="220" y="750">
        <ECAction Algorithm="REQ" Output="CNF" />
      </ECState>
      <ECTransition Source="START" Destination="INIT" Condition="INIT" x="920" y="430" />
      <ECTransition Source="INIT" Destination="START" Condition="1" x="550" y="140" />
      <ECTransition Source="START" Destination="REQ" Condition="REQ" x="550" y="600" />
      <ECTransition Source="REQ" Destination="START" Condition="1" x="220" y="430" />
    </ECC>
    <Algorithm Name="INIT">
      <ST><![CDATA[QO := QI;]]></ST>
    </Algorithm>
    <Algorithm Name="REQ">
      <ST><![CDATA[QO := QI;
Result := Value1 * Value2;]]></ST>
    </Algorithm>
  </BasicFB>
</FBType>
```

---

## Scripts

This skill includes Python scripts for autonomous validation and operation:

| Script | Purpose | Usage | Exit Codes |
|--------|---------|-------|------------|
| `validate_ecc.py` | Verify ECC state machine correctness | `python scripts/validate_ecc.py <file.fbt>` | 0=pass, 1=error, 10=validation failed, 11=pass with warnings |
| `validate_st_algorithm.py` | Check ST algorithm consistency (basic checks) | `python scripts/validate_st_algorithm.py <file.fbt>` | 0=pass, 1=error, 10=validation failed, 11=pass with warnings |

### Validation Workflow

**Recommended:** Validate automatically after creating or modifying a Basic FB:

```bash
# Validate ECC state machine (checks reachability, transitions, algorithms)
python scripts/validate_ecc.py path/to/MyBlock.fbt

# Validate ST algorithms (checks variable references, algorithm consistency)
python scripts/validate_st_algorithm.py path/to/MyBlock.fbt

# Generic validation (basic XML structure)
python ../eae-skill-router/scripts/validate_block.py --type basic path/to/MyBlock.fbt
```

**Example: validate_ecc.py**

```bash
# Basic validation
python scripts/validate_ecc.py MyBlock.fbt

# Verbose output with detailed information
python scripts/validate_ecc.py MyBlock.fbt --verbose

# JSON output for automation/CI
python scripts/validate_ecc.py MyBlock.fbt --json

# CI mode (JSON only, no human messages)
python scripts/validate_ecc.py MyBlock.fbt --ci
```

**What validate_ecc.py checks:**
- ✅ All states are reachable from START
- ✅ All event inputs have at least one transition
- ✅ All transitions reference valid algorithms
- ✅ No circular dependencies in state machine
- ✅ Standard states present (START, INIT, REQ if applicable)
- ⚠️ States without outgoing transitions (warnings)
- ⚠️ Event inputs not used in transitions (warnings)

**Example: validate_st_algorithm.py**

```bash
# Validate algorithms
python scripts/validate_st_algorithm.py MyBlock.fbt --verbose
```

**What validate_st_algorithm.py checks:**
- ✅ Algorithm names match ECC references
- ✅ Variables referenced in algorithms are declared
- ⚠️ Empty algorithms (warnings)
- ⚠️ Potentially undefined variables (warnings, may be false positives)
- ⚠️ Unused algorithms (warnings)

**Note:** Full ST syntax validation is performed by the EAE compiler. These scripts catch common mistakes early to save compilation cycles.

### Generate IDs

```bash
python ../eae-skill-router/scripts/generate_ids.py --hex 6 --guid 1
```

---

## Integration with Validation Skills

### Naming Validation

Use [eae-naming-validator](../eae-naming-validator/SKILL.md) to ensure compliance with SE Application Design Guidelines:

**Key Naming Rules for Basic FB:**
- FB name: camelCase (e.g., `scaleLogic`, `stateDevice`, `motorControl`)
- Interface variables: PascalCase (e.g., `PermitOn`, `FeedbackOn`, `Value`)
- Internal variables: camelCase (e.g., `error`, `outMinActiveLast`, `timerActive`)
- Events: SNAKE_CASE (e.g., `INIT`, `REQ`, `CUSTOM_EVENT`)
- Algorithms: Match corresponding events (e.g., INIT algorithm, REQ algorithm)

**Validate naming before creation:**
```bash
# Validate FB and variable names
python ../eae-naming-validator/scripts/validate_names.py \
  --app-dir IEC61499 \
  --artifact-type BasicFB \
  --name scaleLogic
```

**Reference:** EAE_ADG EIO0000004686.06, Section 1.5

### Performance Analysis

Use [eae-performance-analyzer](../eae-performance-analyzer/SKILL.md) to estimate CPU load:

```bash
# Analyze ST algorithm complexity
python ../eae-performance-analyzer/scripts/estimate_cpu_load.py \
  --app-dir IEC61499 \
  --platform soft-dpac-windows
```

**What to Check:**
- ST algorithm complexity (cyclomatic complexity)
- Execution time estimates
- CPU load percentage

---

## Best Practices from EAE ADG

### 1. Naming Conventions (SE ADG Section 1.5)

**Basic FB Naming:**
- Use camelCase: `scaleLogic`, `stateDevice`, `motorControl`
- Use descriptive names that indicate purpose
- Avoid generic names: `block1`, `fb`, `logic`

**Variable Naming:**
- Interface variables (inputs/outputs): PascalCase → `PermitOn`, `FeedbackOn`, `SetPoint`
- Internal variables (local to FB): camelCase → `error`, `outMinActiveLast`, `timerActive`
- Hungarian notation for complex types: `strConfig`, `arrBuffer`, `eState`

**Event Naming:**
- Use SNAKE_CASE: `INIT`, `REQ`, `CUSTOM_EVENT`, `START_OPERATION`
- Standard events: INIT/INITO for initialization, REQ/CNF for requests
- Avoid generic names: `E1`, `DO`, `OUT`

**Algorithm Naming:**
- Match corresponding event names: INIT algorithm, REQ algorithm
- For custom states: Use descriptive names like `calculateAverage`, `checkLimits`

**Reference:** EAE_ADG EIO0000004686.06, Section 1.5

### 2. ECC Design Principles

**State Machine Guidelines:**
- Keep states focused (single responsibility)
- Use START state as the central hub
- Always include INIT/INITO pattern for initialization
- Use conditional transitions sparingly (prefer simple event-driven logic)
- Document complex transitions in comments

**Standard Pattern:**
```
START ← → INIT (on INIT event, run INIT algorithm, fire INITO)
START ← → REQ (on REQ event, run REQ algorithm, fire CNF)
```

### 3. ST Algorithm Best Practices

**Algorithm Structure:**
- Always set QO := QI at the beginning
- Keep algorithms simple (cyclomatic complexity <10 typical)
- Use clear variable names
- Add comments for complex logic
- Avoid deeply nested IF statements (max 3 levels)

**Example:**
```st
(* INIT Algorithm *)
QO := QI;
error := FALSE;
result := 0.0;

(* REQ Algorithm *)
QO := QI;
IF QI THEN
  result := inputValue * scaleFactor;
  IF result > maxLimit THEN
    result := maxLimit;
    error := TRUE;
  END_IF;
ELSE
  error := TRUE;
END_IF;
```

### 4. Event-Variable Associations

**With Var Guidelines:**
- Always include QI with input events
- Always include QO with output events
- Associate all inputs used in the algorithm with the triggering event
- Associate all outputs produced by the algorithm with the output event

---

## Anti-Patterns

### 1. Naming Anti-Patterns

❌ **Wrong Casing for Basic FB**
```xml
<!-- BAD: Using PascalCase for Basic FB -->
<FBType Name="MotorControl" ...>
```

✅ **Correct camelCase**
```xml
<FBType Name="motorControl" ...>
```

❌ **Inconsistent Variable Casing**
```xml
<!-- Interface variables should be PascalCase -->
<VarDeclaration Name="permitOn" Type="BOOL" />  <!-- BAD: should be "PermitOn" -->

<!-- Internal variables should be camelCase -->
<VarDeclaration Name="Error" Type="BOOL" />  <!-- BAD: should be "error" if internal -->
```

❌ **Generic Event Names**
```xml
<Event Name="E1" />  <!-- BAD: non-descriptive -->
<Event Name="DO" />  <!-- BAD: generic -->
```

✅ **Descriptive Event Names**
```xml
<Event Name="START_OPERATION" />
<Event Name="CALCULATE_RESULT" />
```

### 2. ECC Anti-Patterns

❌ **Missing START State**
```xml
<ECC>
  <!-- BAD: No START state -->
  <ECState Name="INIT" x="500" y="350" />
</ECC>
```

✅ **START State Required**
```xml
<ECC>
  <ECState Name="START" x="550" y="430" />
  <ECState Name="INIT" x="920" y="140">
    <ECAction Algorithm="INIT" Output="INITO" />
  </ECState>
</ECC>
```

❌ **Unreachable States**
```xml
<ECC>
  <ECState Name="START" x="550" y="430" />
  <ECState Name="ORPHAN" x="800" y="500">
    <ECAction Algorithm="ORPHAN_ALG" Output="OUT" />
  </ECState>
  <!-- NO transitions to ORPHAN state - unreachable! -->
</ECC>
```

❌ **Algorithm/Event Mismatch**
```xml
<ECState Name="REQ" x="220" y="750">
  <ECAction Algorithm="INIT" Output="CNF" />  <!-- BAD: INIT algorithm in REQ state -->
</ECState>
```

✅ **Matching Algorithm Names**
```xml
<ECState Name="REQ" x="220" y="750">
  <ECAction Algorithm="REQ" Output="CNF" />
</ECState>
```

### 3. ST Algorithm Anti-Patterns

❌ **Missing QO Assignment**
```xml
<Algorithm Name="REQ">
  <ST><![CDATA[
(* BAD: Forgot to set QO := QI *)
Result := Value1 * Value2;
]]></ST>
</Algorithm>
```

✅ **Always Set QO**
```xml
<Algorithm Name="REQ">
  <ST><![CDATA[
QO := QI;
Result := Value1 * Value2;
]]></ST>
</Algorithm>
```

❌ **Overly Complex Algorithms**
```st
(* BAD: Cyclomatic complexity > 15, deeply nested *)
IF condition1 THEN
  IF condition2 THEN
    IF condition3 THEN
      IF condition4 THEN
        (* 4+ levels of nesting - hard to read *)
      END_IF;
    END_IF;
  END_IF;
END_IF;
```

✅ **Refactor Complex Logic**
```st
(* Use early returns or break into multiple algorithms *)
IF NOT condition1 THEN
  error := TRUE;
  RETURN;
END_IF;

IF NOT condition2 THEN
  error := TRUE;
  RETURN;
END_IF;

(* Main logic here *)
```

❌ **Undefined Variables**
```xml
<Algorithm Name="REQ">
  <ST><![CDATA[
QO := QI;
Result := UnknownVar * 2;  (* UnknownVar not declared! *)
]]></ST>
</Algorithm>
```

### 4. Event-Variable Association Anti-Patterns

❌ **Missing With Var**
```xml
<Event Name="REQ">
  <With Var="QI" />
  <!-- BAD: Algorithm uses Value1 and Value2 but they're not associated -->
</Event>
<Algorithm Name="REQ">
  <ST><![CDATA[
Result := Value1 * Value2;  (* Value1, Value2 should be in With Var *)
]]></ST>
</Algorithm>
```

✅ **Complete With Var Associations**
```xml
<Event Name="REQ">
  <With Var="QI" />
  <With Var="Value1" />
  <With Var="Value2" />
</Event>
```

---

## Verification Checklist

Before committing your Basic FB:

**Naming (run eae-naming-validator):**
- [ ] FB name is camelCase
- [ ] Interface variables are PascalCase
- [ ] Internal variables are camelCase
- [ ] Events are SNAKE_CASE

**Structure:**
- [ ] Root element is `<FBType>` (NOT `<AdapterType>`)
- [ ] Uses `Standard="61499-2"` (NOT `61499-1`)
- [ ] Has `<BasicFB>` element (NOT `<FBNetwork>`)
- [ ] Has `<ECC>` with START state

**ECC Validation (run validate_ecc.py):**
- [ ] All states reachable from START
- [ ] All event inputs have transitions
- [ ] All algorithms referenced in ECActions exist
- [ ] No orphaned states

**ST Algorithm Validation (run validate_st_algorithm.py):**
- [ ] All algorithms set QO := QI
- [ ] All referenced variables are declared
- [ ] Cyclomatic complexity <10 (typical)
- [ ] No undefined variables

**Event-Variable Associations:**
- [ ] INIT event has `<With Var="QI" />`
- [ ] INITO event has `<With Var="QO" />`
- [ ] All inputs used in algorithms are associated with triggering event
- [ ] All outputs produced are associated with output event

**Performance (run eae-performance-analyzer):**
- [ ] ST algorithm complexity is reasonable
- [ ] Estimated CPU load <70% (soft dPAC)

**Scripts Validation:**
- [ ] `python scripts/validate_ecc.py {Name}.fbt` exits with 0
- [ ] `python scripts/validate_st_algorithm.py {Name}.fbt` exits with 0

**Registration:**
- [ ] Registered in .dfbproj with `IEC61499Type="Basic"`
- [ ] .doc.xml and .meta.xml files created and registered

---

## Related Skills

| Skill | When to Use |
|-------|-------------|
| [eae-naming-validator](../eae-naming-validator/SKILL.md) | Validate naming compliance (camelCase for Basic FB) |
| [eae-performance-analyzer](../eae-performance-analyzer/SKILL.md) | Estimate CPU load from ST algorithms |
| [eae-composite-fb](../eae-composite-fb/SKILL.md) | Create composite FBs with FBNetwork |
| [eae-cat](../eae-cat/SKILL.md) | Create CAT blocks with HMI |
| [eae-datatype](../eae-datatype/SKILL.md) | Create custom data types for variables |

---

## Templates

- [basic-fb.xml](../eae-skill-router/assets/templates/basic-fb.xml)
- [doc.xml](../eae-skill-router/assets/templates/doc.xml)
- [meta.xml](../eae-skill-router/assets/templates/meta.xml)
