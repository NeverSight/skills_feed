---
name: dependency-analyzer
description: Analyze project dependencies, build dependency trees, detect conflicts,
  and check compatibility
allowed-tools: Read, Bash, Grep
---

# Dependency Analyzer Skill

## Purpose

The Dependency Analyzer skill provides comprehensive dependency analysis capabilities for Python projects. It parses dependency configuration files (requirements.txt, pyproject.toml), builds dependency trees, detects version conflicts, and checks compatibility constraints.

**Key Functions:**
- Parse and analyze current project dependencies
- Identify new dependencies required for features
- Build visual dependency trees
- Detect version conflicts and incompatibilities
- Check compatibility across Python versions
- Generate structured dependency reports

## When to Use

Use this skill when you need to:
- Analyze current project dependencies before adding new features
- Identify all dependencies required for a new feature implementation
- Detect version conflicts between dependencies
- Build dependency trees to understand package relationships
- Verify compatibility of new dependencies with existing ones
- Generate dependency reports for documentation

**Typical Scenarios:**
- Phase 2 design (dependency analysis for PRP)
- Pre-implementation dependency planning
- Dependency upgrade planning
- Conflict resolution
- Security vulnerability assessment (dependency version analysis)

## Workflow

### 1. Parse Current Dependencies

**Action**: Read and parse all dependency configuration files in the project

```bash
# Check for requirements.txt
if [ -f requirements.txt ]; then
  echo "Found requirements.txt"
  cat requirements.txt
fi

# Check for pyproject.toml
if [ -f pyproject.toml ]; then
  echo "Found pyproject.toml"
  grep -A 30 "dependencies\|requires" pyproject.toml
fi

# Check for setup.py
if [ -f setup.py ]; then
  echo "Found setup.py"
  grep -A 20 "install_requires\|extras_require" setup.py
fi
```

**Output**: Inventory of current dependencies with versions

### 2. Build Dependency Tree

**Action**: Use dependency-checker script to build complete dependency tree

```bash
python .claude/skills/dependency-analyzer/dependency-checker-script.py \
  --analyze \
  --project-root . \
  --output-format tree
```

**Output**: Visual dependency tree showing relationships

### 3. Identify New Dependencies

**Action**: Extract required libraries from feature analysis

**Process**:
- Read feature analysis document
- Extract library names from requirements section
- Determine package sources (PyPI, npm, etc.)
- Classify as core vs. development dependencies
- Research latest stable versions

**Output**: List of new dependencies with recommended versions

### 4. Check Compatibility

**Action**: Verify version compatibility and constraints

```bash
python .claude/skills/dependency-analyzer/dependency-checker-script.py \
  --check-compatibility \
  --new-deps "package1>=1.0,package2~=2.0" \
  --python-version "3.11"
```

**Checks**:
- Python version compatibility (3.11+)
- Dependency version constraints (>=, ~=, ^, ==)
- Breaking changes between versions
- Platform-specific requirements

**Output**: Compatibility report with warnings and recommendations

### 5. Detect Conflicts

**Action**: Identify version conflicts in dependency tree

```bash
python .claude/skills/dependency-analyzer/dependency-checker-script.py \
  --check-conflicts \
  --new-deps "package1,package2,package3"
```

**Detects**:
- Version conflicts (Package A requires B>=2.0, Package C requires B<2.0)
- Circular dependencies
- Incompatible package combinations
- Transitive dependency conflicts

**Output**: Conflict report with resolution strategies

## Output Format

### Dependency Analysis Report

```markdown
## Dependency Analysis

### Current Dependencies (12 total)
**Core Dependencies:**
- requests==2.31.0 - HTTP library
- pydantic==2.5.0 - Data validation
- click==8.1.7 - CLI framework

**Development Dependencies:**
- pytest==7.4.3 - Testing framework
- black==23.12.0 - Code formatter
- mypy==1.7.1 - Type checker

### New Dependencies Required (3 total)
| Package | Version | Purpose | Type | Source |
|---------|---------|---------|------|--------|
| httpx | >=0.27.0 | Async HTTP client | core | PyPI |
| pydantic-settings | >=2.0.0 | Settings management | core | PyPI |
| pytest-asyncio | >=0.21.0 | Async test support | dev | PyPI |

### Dependency Tree
```
project-root/
├── requests==2.31.0
│   ├── urllib3>=1.21.1,<3
│   ├── certifi>=2017.4.17
│   └── charset-normalizer>=2,<4
├── pydantic==2.5.0
│   ├── typing-extensions>=4.6.1
│   └── annotated-types>=0.4.0
└── [new] httpx>=0.27.0
    ├── httpcore>=1.0.0
    ├── certifi
    └── sniffio
```

### Compatibility Check
✅ Python 3.11+ compatible
✅ No breaking changes detected
✅ All version constraints satisfied
⚠️  httpx and requests overlap (both HTTP clients)

### Conflicts Detected
**None** - All dependencies compatible

### Recommendations
1. Consider migrating from requests to httpx for async support
2. Pin versions in production: httpx==0.27.2
3. Update requirements.txt with new dependencies
4. Run `pip install -r requirements.txt` to verify installation
```

## Best Practices

### Version Specification
- **Use version ranges** for flexibility: `package>=1.0,<2.0`
- **Pin exact versions** in production: `package==1.2.3`
- **Understand specifiers**:
  - `>=1.0` - Minimum version 1.0
  - `~=1.2` - Compatible release (>=1.2, <2.0)
  - `^1.2.3` - Caret (npm-style, rare in Python)
  - `==1.2.3` - Exact version

### Dependency Management
- **Separate core and dev** dependencies clearly
- **Use pyproject.toml** for modern Python projects
- **Document dependency rationale** in comments
- **Regular updates** to patch security vulnerabilities
- **Test after updates** to catch breaking changes

### Conflict Resolution
1. **Identify conflict source** (which packages require incompatible versions)
2. **Check if upgradeable** (can Package A use newer B?)
3. **Find compatible versions** (use compatibility matrix)
4. **Test resolution** with dry-run installation
5. **Document resolution** in dependency report

## Supporting Resources

### dependency-checker-script.py

**Location**: `.claude/skills/dependency-analyzer/dependency-checker-script.py`

**Usage**:
```bash
# Analyze current dependencies
python dependency-checker-script.py --analyze --project-root .

# Check compatibility
python dependency-checker-script.py --check-compatibility \
  --new-deps "httpx>=0.27.0,pydantic-settings>=2.0"

# Detect conflicts
python dependency-checker-script.py --check-conflicts \
  --new-deps "package1,package2"

# Generate full report
python dependency-checker-script.py --full-report \
  --output dependency-report.md
```

**Features**:
- Parse requirements.txt, pyproject.toml, setup.py
- Build dependency trees
- Check version compatibility
- Detect conflicts
- Query PyPI for latest versions
- Generate markdown reports

### compatibility-matrix.md

**Location**: `.claude/skills/dependency-analyzer/compatibility-matrix.md`

**Contents**:
- Common Python library compatibility rules
- Known incompatible package combinations
- Platform-specific dependency notes
- Python version compatibility matrix
- Resolution strategies for common conflicts

## Example Usage

### Scenario 1: Pre-Feature Dependency Analysis

**Input**: Feature requires webhook notifications with async HTTP

**Process**:
1. Parse current dependencies → Find `requests==2.31.0`
2. Identify new dependencies → Need `httpx` for async support
3. Check compatibility → `httpx>=0.27.0` compatible with Python 3.11+
4. Detect conflicts → No conflicts (httpx and requests can coexist)
5. Generate report → Structured dependency analysis

**Output**:
```markdown
### New Dependencies Required
- httpx>=0.27.0 - Async HTTP client for webhook delivery

### Compatibility: ✅ Compatible
- Python 3.11+ supported
- No conflicts with existing dependencies

### Installation:
```bash
pip install httpx>=0.27.0
```

### Scenario 2: Conflict Detection

**Input**: Feature requires `package-a>=2.0` but existing `package-b` requires `package-a<2.0`

**Process**:
1. Analyze current dependencies → Find `package-b==1.5` requires `package-a<2.0`
2. Check new requirements → Feature needs `package-a>=2.0`
3. Detect conflict → Version conflict detected
4. Research solutions → Check if `package-b>=2.0` supports `package-a>=2.0`
5. Generate report → Conflict report with resolution strategy

**Output**:
```markdown
### Conflicts Detected
**Conflict**: package-a version conflict
- Feature requires: package-a>=2.0
- package-b==1.5 requires: package-a<2.0

**Resolution Strategy**:
1. Upgrade package-b to 2.0.0 (supports package-a>=2.0)
2. Update requirements.txt:
   - package-a>=2.0
   - package-b>=2.0

**Validation**:
```bash
pip install --dry-run package-a>=2.0 package-b>=2.0
```
```

## Integration with Feature Implementation Flow

**Input**: Analysis document with dependencies section

**Process**:
1. Dependency Manager agent activates this skill
2. Skill parses current dependencies from project files
3. Skill extracts new dependencies from analysis document
4. Skill checks compatibility and detects conflicts
5. Skill generates structured dependency report

**Output**: Dependency analysis section for PRP

**Next Step**: Design Orchestrator synthesizes dependency analysis into complete PRP

## Error Handling

### Common Errors

**Missing dependency file**:
```
Error: No dependency configuration file found
Resolution: Create requirements.txt or pyproject.toml
```

**Invalid version specifier**:
```
Error: Invalid version specifier "package>=abc"
Resolution: Use valid version format (e.g., "package>=1.0.0")
```

**Conflict detected**:
```
Warning: Version conflict detected
Action: Review conflict report and apply resolution strategy
```

**PyPI query failure**:
```
Error: Failed to query PyPI for package "xyz"
Resolution: Check network connectivity or package name spelling
```

## Advanced Features

### Custom Compatibility Rules

Define project-specific compatibility rules in `compatibility-matrix.md`:

```yaml
# Example rule
package-a:
  python: ">=3.11"
  conflicts:
    - package-b<2.0
  recommends:
    - package-c>=1.0
```

### Dependency Tree Visualization

Generate visual dependency trees for documentation:

```bash
python dependency-checker-script.py --analyze --format tree --output tree.txt
```

Output:
```
myproject==1.0.0
├── requests==2.31.0
│   ├── urllib3>=1.21.1,<3
│   ├── certifi>=2017.4.17
│   └── charset-normalizer>=2,<4
├── pydantic==2.5.0
│   ├── typing-extensions>=4.6.1
│   └── annotated-types>=0.4.0
└── httpx==0.27.2
    ├── httpcore==1.0.2
    ├── certifi
    └── sniffio
```

---

**Version**: 2.0.0
**Agent**: @dependency-manager
**Phase**: 2 (Design & Planning)
**Created**: 2025-10-29