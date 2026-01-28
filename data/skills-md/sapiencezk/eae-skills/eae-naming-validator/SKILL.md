---
name: eae-naming-validator
description: >
  Enforces Schneider Electric naming conventions across EcoStruxure
  Automation Expert applications. Validates 14+ artifact types (CAT, Function
  Blocks, Adapters, DataTypes, Variables, Events, Folders) against official
  SE Application Design Guidelines, providing actionable error messages for
  compliance.
license: MIT
compatibility: Designed for EcoStruxure Automation Expert 25.0+, Python 3.8+, PowerShell (Windows)
metadata:
  version: "1.0.0"
  model: claude-opus-4-5-20251101
  domain: industrial-automation
  standard: IEC-61499
  eae_version: "25.0+"
  adg_reference: EIO0000004686.06
  timelessness_score: 8/10
  user-invocable: true
  platform: EcoStruxure Automation Expert
---
# EAE Naming Validator - SE Convention Enforcement

Enforces Schneider Electric naming conventions across EcoStruxure Automation Expert applications with automated validation and actionable fix suggestions.

**Critical Problem**: Non-compliant naming reduces code readability, increases maintenance burden, and violates SE Application Design Guidelines. Manual review of naming across hundreds of artifacts is error-prone and time-consuming.

**Solution**: Automated validation engine that parses EAE XML files (.fbt, .cat, .dtp, .adp), applies 14+ SE naming rules, and reports violations with specific fix recommendations. Integrates with CI/CD pipelines via JSON output.

---

## Quick Start

### Validate Entire Application

```python
python scripts/validate_names.py --app-dir /path/to/eae/app

# With JSON output for CI/CD
python scripts/validate_names.py --app-dir /path/to/eae/app --output violations.json
```

### Validate Specific Artifact Type

```python
# Only CATs
python scripts/validate_names.py --app-dir /path/to/eae/app --artifact-type CAT

# Only Basic Function Blocks
python scripts/validate_names.py --app-dir /path/to/eae/app --artifact-type BasicFB
```

### Example Output

```
Validating naming conventions in: /path/to/eae/app
Found 45 artifacts across 12 files

VIOLATIONS FOUND: 8

[ERROR] BasicFB "ScaleLogic" (scaleLogic.fbt:1)
  Rule: Basic Function Blocks must use camelCase
  Expected pattern: ^[a-z][a-zA-Z0-9]*$
  Suggestion: Rename to "scaleLogic"

[WARNING] Variable "permit_on" (motorControl.fbt:23)
  Rule: Interface variables must use PascalCase
  Expected pattern: ^[A-Z][a-zA-Z0-9]*$
  Suggestion: Rename to "PermitOn"

Summary: 3 ERRORS, 5 WARNINGS, 0 INFO
Compliance: 82% (37/45 artifacts compliant)
Exit code: 11 (errors found)
```

---

## Triggers

Use any of these phrases to invoke the skill:

- "Validate naming conventions in this EAE application"
- "Check if names follow SE Application Design Guidelines"
- "Enforce EAE naming standards"
- "Find naming violations in my EcoStruxure application"
- "Verify artifact names comply with SE conventions"

---

## Quick Reference: SE Naming Conventions

| Artifact Type | Convention | Pattern | Example | Severity if Violated |
|---------------|-----------|---------|---------|---------------------|
| **CAT** | PascalCase | `^[A-Z][a-zA-Z0-9]*$` | AnalogInput | ERROR |
| **SubApp** | PascalCase | `^[A-Z][a-zA-Z0-9]*$` | SeqManager | ERROR |
| **Basic FB** | camelCase | `^[a-z][a-zA-Z0-9]*$` | scaleLogic | ERROR |
| **Composite FB** | camelCase | `^[a-z][a-zA-Z0-9]*$` | stateDevice | ERROR |
| **Function** | camelCase | `^[a-z][a-zA-Z0-9]*$` | calculateAverage | ERROR |
| **Adapter** | IPascalCase | `^I[A-Z][a-zA-Z0-9]*$` | IAnalogValue | ERROR |
| **Event** | SNAKE_CASE | `^[A-Z_]+$` | START_MOTOR | ERROR |
| **Structure** | strPascalCase | `^str[A-Z][a-zA-Z0-9]*$` | strMotorData | ERROR |
| **Alias** | aPascalCase | `^a[A-Z][a-zA-Z0-9]*$` | aFrame | WARNING |
| **Enum** | ePascalCase | `^e[A-Z][a-zA-Z0-9]*$` | eProductType | ERROR |
| **Array** | arrPascalCase | `^arr[A-Z][a-zA-Z0-9]*$` | arrRecipeBuffer | WARNING |
| **Variable (I/O)** | PascalCase | `^[A-Z][a-zA-Z0-9]*$` | PermitOn | ERROR |
| **Variable (Internal)** | camelCase | `^[a-z][a-zA-Z0-9]*$` | outMinActiveLast | WARNING |
| **Folder** | PascalCase | `^[A-Z][a-zA-Z0-9]*$` | Motors | WARNING |

**Special Cases**:
- Reserved event names `INIT` and `INITO` are always valid
- Folders should preferably be single words but multi-word PascalCase is acceptable
- Numbers in names are allowed but should not start the name (enforced by patterns)

---

## How It Works

### 1. File Discovery

The validator scans the application directory for:
- `.fbt` files (Function Block Types - Basic, Composite, Function)
- `.cat` files (Composite Application Types)
- `.dtp` files (Data Type definitions - Structure, Enum, Alias, Array)
- `.adp` files (Adapter declarations)
- Application metadata for folder names

### 2. XML Parsing

Each file is parsed to extract:
- **Artifact type** (determined from XML root element and attributes)
- **Name** (from `Name` attribute)
- **Variables** (from InterfaceList/VarDeclaration, InternalVars)
- **Events** (from EventInputs, EventOutputs)
- **Context** (interface vs internal scope, data type category)

### 3. Rule Application

For each extracted name:
1. **Detect context**: Is this a variable? If so, is it interface or internal?
2. **Select rule**: Match artifact type + context to naming rule
3. **Apply regex pattern**: Test name against expected pattern
4. **Classify severity**: ERROR (blocks deployment), WARNING (should fix), INFO (suggestion)

### 4. Violation Reporting

Violations include:
- **Location**: File path and line number (approximate based on XML structure)
- **Rule description**: Human-readable explanation of the convention
- **Expected pattern**: Regex for developers, plain English for users
- **Suggested fix**: Auto-generated compliant name where possible
- **Severity**: ERROR / WARNING / INFO

### 5. Output Formats

**Human-Readable** (default):
- Color-coded console output with grouped violations
- Summary statistics (compliance percentage, violation counts)
- Sorted by severity and file

**JSON** (for CI/CD):
```json
{
  "success": false,
  "errors": [
    {
      "artifact_type": "BasicFB",
      "name": "ScaleLogic",
      "file": "scaleLogic.fbt",
      "line": 1,
      "rule": "Basic Function Blocks must use camelCase",
      "pattern": "^[a-z][a-zA-Z0-9]*$",
      "suggestion": "scaleLogic",
      "severity": "ERROR"
    }
  ],
  "warnings": [ ... ],
  "details": {
    "total_artifacts": 45,
    "compliant": 37,
    "compliance_percentage": 82.2
  }
}
```

---

## Commands

### Basic Usage

```bash
# Validate entire application
python scripts/validate_names.py --app-dir /path/to/eae/app

# Save violations to JSON file
python scripts/validate_names.py --app-dir /path/to/eae/app --output violations.json
```

### Filtering

```bash
# Only specific artifact types
python scripts/validate_names.py --app-dir /path/to/eae/app --artifact-type CAT
python scripts/validate_names.py --app-dir /path/to/eae/app --artifact-type BasicFB

# Only specific severity levels
python scripts/validate_names.py --app-dir /path/to/eae/app --min-severity ERROR

# Exclude specific files or folders
python scripts/validate_names.py --app-dir /path/to/eae/app --exclude "Legacy/*"
```

### CI/CD Integration

```bash
# Exit codes for automation
# 0 = all compliant
# 10 = warnings found (may proceed)
# 11 = errors found (should block)
# 1 = parsing failure

# Jenkins/GitHub Actions example
python scripts/validate_names.py --app-dir $APP_DIR --output report.json
EXIT_CODE=$?

if [ $EXIT_CODE -eq 11 ]; then
  echo "Naming violations found - deployment blocked"
  exit 1
elif [ $EXIT_CODE -eq 10 ]; then
  echo "Naming warnings found - review recommended"
fi
```

---

## Scripts

### validate_names.py

**Purpose**: Main validation engine for SE naming conventions

**Usage**:
```bash
python scripts/validate_names.py --app-dir <path> [options]

Options:
  --app-dir PATH             Path to EAE application (required)
  --output PATH              JSON output file path (default: stdout)
  --artifact-type TYPE       Filter to specific type (CAT, BasicFB, CompositeFB, etc.)
  --min-severity LEVEL       Minimum severity to report (ERROR, WARNING, INFO)
  --exclude PATTERN          Exclude files matching glob pattern
  --strict                   Treat all violations as ERRORS
  --help                     Show full help
```

**Exit Codes**:
- `0`: All artifacts compliant (or no violations of requested severity level)
- `10`: Warnings found (non-blocking violations)
- `11`: Errors found (blocking violations requiring fixes)
- `1`: Parsing failure or invalid arguments

**Output**: JSON structure with ValidationResult pattern (success, errors, warnings, details)

**Example**:
```bash
# Validate with strict mode (all warnings become errors)
python scripts/validate_names.py --app-dir ./MyApp --strict

# Filter to only CATs and Basic FBs
python scripts/validate_names.py --app-dir ./MyApp --artifact-type CAT,BasicFB

# CI/CD integration with JSON output
python scripts/validate_names.py --app-dir $CI_WORKSPACE --output violations.json --min-severity ERROR
```

---

## Integration with Other EAE Skills

| Skill | Integration Point | Use Case |
|-------|-------------------|----------|
| **eae-cat** | Validate names when creating CATs | Ensure new CATs follow PascalCase before generation |
| **eae-basic-fb** | Validate names when creating Basic FBs | Ensure FB and variables use correct case |
| **eae-composite-fb** | Validate FB instances | Check instance names match conventions |
| **eae-adapter** | Validate adapter interfaces | Ensure adapters use IPascalCase prefix |
| **eae-datatype** | Validate type declarations | Check struct/enum/array/alias prefixes |
| **eae-performance-analyzer** | Pre-validation step | Fix naming before performance analysis |

**Workflow Example**:
```
1. User: "Create a new CAT called analog_input"
2. eae-cat creates CAT scaffolding
3. eae-naming-validator checks name: VIOLATION (should be AnalogInput)
4. User: "Fix the naming violation"
5. eae-naming-validator suggests: "Rename to AnalogInput"
6. eae-cat renames CAT to AnalogInput
7. Validation passes
```

---

## Anti-Patterns

| Anti-Pattern | Why It Fails | Instead |
|--------------|--------------|---------|
| **Manual name reviews** | Error-prone, inconsistent, time-consuming | Automated validation on every commit |
| **Vague error messages** | "Name is invalid" doesn't help users fix it | Include expected pattern + suggestion |
| **Blocking legacy code** | Old but functional apps shouldn't break builds | Use `--min-severity ERROR` for gradual adoption |
| **Slow validation** | Users won't run if it takes >30s | Optimize XML parsing, cache file reads |
| **Ignoring context** | Same name has different rules in different scopes | Detect variable scope (interface vs internal) |
| **No CI/CD integration** | Violations discovered too late | JSON output + exit codes for automation |

---

## Verification Checklist

After running validation:

- [ ] No ERROR-level violations remain (required for deployment)
- [ ] WARNING-level violations reviewed and accepted or fixed
- [ ] Compliance percentage ≥95% for new code
- [ ] JSON output parseable by CI/CD tools (if using automation)
- [ ] All suggested fixes tested (rename operations don't break connections)
- [ ] Validation completes in <10 seconds for typical application (50-200 artifacts)

---

<details>
<summary><strong>Deep Dive: Naming Rule Catalog</strong></summary>

See [references/naming-rules.md](references/naming-rules.md) for the complete catalog of 14+ naming rules with:
- Detailed pattern explanations
- Rationale for each convention
- Edge cases and special considerations
- Examples of compliant and non-compliant names
- SE Application Design Guidelines references

</details>

<details>
<summary><strong>Deep Dive: XML Parsing Strategy</strong></summary>

### File Type Detection

The validator identifies artifact types from XML structure:

**CAT (.cat files)**:
```xml
<CompositeFBType Name="AnalogInput">
  <!-- Has attribute CompositeFBType or contains HMI elements -->
</CompositeFBType>
```

**Basic FB (.fbt files)**:
```xml
<FBType Name="scaleLogic">
  <ECC> <!-- Execution Control Chart indicates Basic FB -->
    ...
  </ECC>
</FBType>
```

**Composite FB (.fbt files)**:
```xml
<FBType Name="stateDevice">
  <FBNetwork> <!-- FBNetwork indicates Composite FB -->
    ...
  </FBNetwork>
</FBType>
```

**Adapter (.adp files)**:
```xml
<AdapterType Name="IAnalogValue">
  ...
</AdapterType>
```

**DataType (.dtp files)**:
```xml
<!-- Structure -->
<StructuredType Name="strMotorData">
  ...
</StructuredType>

<!-- Enum -->
<EnumeratedType Name="eProductType">
  ...
</EnumeratedType>

<!-- Array -->
<ArrayType Name="arrRecipeBuffer">
  ...
</ArrayType>

<!-- Alias -->
<DataType Name="aFrame" Comment="ALIAS">
  ...
</DataType>
```

### Variable Scope Detection

**Interface Variables** (PascalCase):
```xml
<InterfaceList>
  <EventInputs>
    <Event Name="START" />
  </EventInputs>
  <InputVars>
    <VarDeclaration Name="PermitOn" Type="BOOL" />
  </InputVars>
</InterfaceList>
```

**Internal Variables** (camelCase):
```xml
<BasicFB>
  <InternalVars>
    <VarDeclaration Name="outMinActiveLast" Type="BOOL" />
  </InternalVars>
</BasicFB>
```

### Performance Optimizations

1. **Lazy parsing**: Only parse Name attributes unless detailed validation requested
2. **Batch processing**: Group files by type for optimized rule application
3. **Incremental validation**: Cache results for unchanged files
4. **Parallel processing**: Validate multiple files concurrently (optional)

</details>

<details>
<summary><strong>Deep Dive: Suggested Fix Generation</strong></summary>

### Auto-Fix Strategies

| Violation | Detection | Suggested Fix |
|-----------|-----------|---------------|
| **Wrong case** | Matches pattern after case conversion | Convert to correct case |
| **Missing prefix** | Name would match with prefix added | Add required prefix |
| **Extra characters** | Name has underscores/hyphens where not allowed | Remove/convert to camelCase |
| **Reserved conflict** | Uses reserved keyword incorrectly | Append suffix or suggest synonym |

**Example Transformations**:
```python
# PascalCase → camelCase
"ScaleLogic" → "scaleLogic"

# camelCase → PascalCase
"permitOn" → "PermitOn"

# snake_case → PascalCase
"permit_on" → "PermitOn"

# Missing prefix (Adapter)
"AnalogValue" → "IAnalogValue"

# Missing prefix (Structure)
"MotorData" → "strMotorData"

# Wrong case for Event
"start_motor" → "START_MOTOR"
```

**Limitations**:
- Cannot auto-fix ambiguous cases (e.g., acronym capitalization: "HTTPServer" vs "HttpServer")
- Semantic meaning may be lost (e.g., "permit_on" → "PermitOn" removes word boundary clarity)
- Users should review suggested fixes before applying

### Future Enhancement: Auto-Apply Mode

```bash
# Dry-run (show what would be fixed)
python scripts/validate_names.py --app-dir ./MyApp --auto-fix --dry-run

# Apply fixes automatically
python scripts/validate_names.py --app-dir ./MyApp --auto-fix

# Apply only specific fixes
python scripts/validate_names.py --app-dir ./MyApp --auto-fix --only "BasicFB,Variable"
```

**Safety Checks**:
- Backup original files before modification
- Verify XML remains well-formed after rename
- Update all references to renamed artifact (cross-references, connections)
- Report any manual fixesneed needed (e.g., HMI symbol names)

</details>

---

## Extension Points

1. **Custom Rule Sets**: Support project-specific naming conventions via JSON configuration
2. **Auto-Fix Mode**: Automatically apply suggested renames (with backup and verification)
3. **IDE Integration**: Real-time validation in EAE editor via plugin
4. **Historical Tracking**: Track compliance trends over time, generate compliance reports
5. **Internationalization**: Support localized error messages for non-English teams
6. **Cross-Reference Validation**: Ensure adapter socket/plug names match, instance names unique per scope

---

## Changelog

### v1.0.0 (Current)
- Initial release with 14 naming rule validators
- Support for CAT, Basic/Composite FB, Adapter, DataType, Variable, Event, Folder
- JSON output for CI/CD integration
- Human-readable console reports with color coding
- Exit codes for automation (0/10/11/1)
- Context-aware validation (interface vs internal variables)
- Suggested fix generation for common violations
