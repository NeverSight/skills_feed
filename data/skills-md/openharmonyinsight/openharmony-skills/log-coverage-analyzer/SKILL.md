---
name: log-coverage-analyzer
description: Analyze code repository logging coverage to ensure all function branches have LOGE/LOGI logs and identify high-frequency log risks. Supports multiple programming languages (C++, Java, Python, JavaScript, etc.)
license: MIT
---

This skill performs comprehensive log coverage analysis for code repositories. It identifies logging deficiencies in call chains and detects high-frequency log risks that may impact performance.

## Analysis Principles

### Log Level Definitions

| Log Level | Behavior | Use Case |
|-----------|----------|----------|
| LOGE | Always prints, never lost | **Critical** - Must exist on all error return paths |
| LOGI | Always prints, may be lost if high-frequency triggered at same location | **Important** - Success paths, key operations |
| LOGD | Only prints when debug switch enabled | **Optional** - Debug information only |
| LOGW | Only prints when debug switch enabled | **Optional** - Warning information only |

### Core Analysis Rules

1. **Log Coverage Rule**: Each branch in a function call chain must have LOGE or LOGI level logging
2. **High-Frequency Risk Rule**: Functions that may be called frequently (loops, timers, callbacks, event handlers) with LOGE/LOGI logs pose performance risks
3. **Error Path Rule**: All error return paths MUST have LOGE logging
4. **Context Rule**: All logs must include sufficient context information (IDs, states, parameters)

## Execution Workflow

### Step 00: Create Analysis Plan

Description: Create detailed analysis plan before starting

Actions:
- Use `TodoWrite` tool to create task list
- Plan analysis scope:
  - Source file discovery and filtering
  - Function call chain extraction
  - Log coverage analysis per branch
  - High-frequency risk detection
  - Report generation

Output: Analysis plan created via `TodoWrite` tool

### Step 01: Discover Source Files

Description: Find all relevant source files in the repository

Actions:
- Use `Glob` tool to find source files based on language patterns:
  - C/C++: `**/*.cpp`, `**/*.cc`, `**/*.cxx`, `**/*.h`, `**/*.hpp`
  - Java: `**/*.java`
  - Python: `**/*.py`
  - JavaScript/TypeScript: `**/*.js`, `**/*.ts`
  - Go: `**/*.go`
  - Rust: `**/*.rs`
- Exclude test files if specified (patterns: `**/test/**`, `**/tests/**`, `**/*_test.*`)
- Exclude build directories (patterns: `**/build/**`, `**/out/**`, `**/target/**`)

Output: List of source files to analyze

### Step 02: Scan Logging Patterns

Description: Scan all source files for logging macros/functions

Actions:
- Use `Grep` tool to find log statements with pattern:
  - Case-insensitive search for: `LOG[DEIW]`, `HILOG[DEIW]`, `ALOG[DEIW]`
  - Also search for: `\.log[deiw]\(`, `Log\.[deiw]`, `LOG\.`
- Count occurrences per file
- Identify log level distribution

Output: Log statistics per file

### Step 03: Extract Functions and Call Chains

Description: Parse source files to extract function definitions and call relationships

Actions:
- For each source file:
  - Identify function definitions (various patterns per language)
  - Extract function bodies including all branches
  - Identify function calls within each function
  - Build call chain graph
- Map branch conditions (if/else, switch/case, try/catch, early returns)

Output: Function list with call relationships

### Step 04: Analyze Log Coverage per Branch

Description: Check each branch in call chains for required logging

Actions:
- For each function in call chain:
  - Identify all branches:
    - Early returns
    - if/else branches
    - switch/case branches
    - try/catch blocks
    - loop exits with error conditions
  - Check each branch for LOGE or LOGI presence
  - Flag branches without required logging as **Log Deficiency**
  - Check error return paths specifically for LOGE

Deficiency Classification:
- **High Priority**: Error return path without LOGE
- **Medium Priority**: Success path without LOGI for multi-step operations
- **Low Priority**: Branch without any logging (non-critical)

Output: List of log deficiencies with locations

### Step 05: Detect High-Frequency Log Risks

Description: Identify functions with LOGE/LOGI that may be called frequently

Actions:
- Identify high-frequency function patterns:
  - Network data callbacks (`OnDataReceived`, `OnPacketReceived`, `OnMessage`)
  - Timer callbacks (`OnTimer`, `Tick`, `Update`)
  - Event handlers (`HandleEvent`, `ProcessEvent`, `OnEvent`)
  - Loop operations (`ProcessItem`, `HandlePacket`, `SendData`)
  - Stream processing (`ProcessStream`, `HandleFrame`, `EncodeFrame`)
  - Message queue handlers (`OnMessage`, `Dispatch`)
- For functions with LOGE/LOGI in these patterns:
  - Analyze call frequency potential
  - Classify risk level: High/Medium/Low
  - Flag as **High-Frequency Risk**

Risk Classification:
- **High Risk**: Per-packet/per-frame LOGE/LOGI in data path
- **Medium Risk**: Per-message LOGI in messaging path
- **Low Risk**: Low-frequency callbacks with logs

Output: List of high-frequency risks with locations

### Step 06: Generate Analysis Report

Description: Create comprehensive analysis report with all findings

Actions:
- Generate Markdown report with:
  1. Summary statistics
  2. Log deficiencies with fix suggestions
  3. High-frequency risks with fix suggestions
  4. Call chain analysis
  5. Detailed code examples
- Use `Write` tool to save report to `log-coverage-report-YYYYMMDD-HHmmss.md`

Output: Complete analysis report

## Language-Specific Patterns

### C/C++

Function Definition Patterns:
```cpp
[return_type] [class::]function_name([parameters]) {
[\w\s:*,]*\{
```

Log Patterns:
- `LOG[DEIW]\(`, `HILOG[DEIW]\(`, `ALOG[DEIW]\(`
- `__android_log_print`
- `OHOS::HiviewDFX::HiLog::[Error|Warn|Info|Debug]`

### Java

Function Definition Patterns:
```java
(public|private|protected)?(\s+static)?\s+\w+\s+\w+\s*\(.*\)\s*(throws\s+[\w\s,]+)?\s*\{
```

Log Patterns:
- `Log\.[deiw]\(`
- `Logger\.(error|warn|info|debug)\(`
- `Timber\.[deiw]\(`

### Python

Function Definition Patterns:
```python
def\s+\w+\s*\(.*\)\s*->?\s*.*:
```

Log Patterns:
- `logger\.(error|warning|info|debug)\(`
- `logging\.(error|warning|info|debug)\(`
- `print\(`

### JavaScript/TypeScript

Function Definition Patterns:
```javascript
function\s+\w+\s*\(.*\)\s*\{
|\w+\s*\([^)]*\)\s*(=>|\{)
```

Log Patterns:
- `console\.(error|warn|info|log)\(`
- `logger\.(error|warn|info|debug)\(`

## Fix Recommendations

### For Log Deficiencies

**Error Return Path (Must Fix)**:
```cpp
// BEFORE:
if (remote == nullptr) {
    return ERR_NULL_OBJECT;  // ❌ No LOGE
}

// AFTER:
if (remote == nullptr) {
    HILOGE("FunctionName: remote is null, context=%{public}d", context);
    return ERR_NULL_OBJECT;
}
```

**Success Path (Should Fix)**:
```cpp
// BEFORE:
int32_t CreateSession(...) {
    // ... initialization code
    return ERR_OK;  // ❌ No LOGI on success
}

// AFTER:
int32_t CreateSession(...) {
    // ... initialization code
    HILOGI("CreateSession: success, sessionId=%{public}d, name=%{public}s", id, name);
    return ERR_OK;
}
```

### For High-Frequency Risks

**Remove High-Frequency LOGI**:
```cpp
// BEFORE:
void OnPacketReceived(int socketId, const void* data, uint32_t len) {
    HILOGI("packet received: socket=%{public}d, len=%{public}u", socketId, len);  // ⚠️ Per-packet
    // ... process packet
}

// AFTER:
void OnPacketReceived(int socketId, const void* data, uint32_t len) {
    // Removed per-packet LOGI
    static std::atomic<uint64_t> packetCount{0};
    if (++packetCount % 1000 == 1) {
        HILOGI("Packet stats: count=%{public}llu, socket=%{public}d",
            packetCount.load(), socketId);
    }
    // ... process packet
}
```

**Use Throttled LOGE for Errors**:
```cpp
// BEFORE:
void ProcessPacket(const Packet* pkt) {
    if (pkt == nullptr) {
        HILOGE("packet is null");  // ⚠️ Per-packet error
        return;
    }
}

// AFTER:
void ProcessPacket(const Packet* pkt) {
    if (pkt == nullptr) {
        static std::atomic<uint32_t> errorCount{0};
        if (++errorCount % 100 == 1) {
            HILOGE("ProcessPacket: null packet, count=%{public}u", errorCount.load());
        }
        return;
    }
}
```

## Output Format

```
================================================================================
Log Coverage Analysis Report
================================================================================

Repository: <repository_path>
Analysis Date: <timestamp>
Files Analyzed: <count>

## Summary Statistics

| Metric | Count |
|--------|-------|
| Total Source Files | <number> |
| Total Functions | <number> |
| Functions Analyzed | <number> |
| Log Deficiencies | <number> |
| High-Frequency Risks | <number> |

## Log Deficiencies

### [High/Medium/Low] Priority

**File**: `<file_path>`
**Function**: `<function_name>`
**Lines**: `<line_range>`
**Issue**: `<description>`

**Evidence**:
```cpp
<code snippet>
```

**Impact**:
<explain impact on debugging/troubleshooting>

**Fix**:
```cpp
<fixed code>
```

---

## High-Frequency Risks

### [High/Medium/Low] Risk

**File**: `<file_path>`
**Function**: `<function_name>`
**Lines**: `<line_range>`
**Risk**: <description>

**Evidence**:
```cpp
<code snippet>
```

**Analysis**:
<explain why this is high-frequency>

**Fix**:
```cpp
<fixed code with throttling/statistics>
```

---

## Call Chain Analysis

### Call Chain: <chain_name>

```
<function_1>()
    ↓ [✓/✗/⚠️] <log_status>
<function_2>()
    ↓ [✓/✗/⚠️] <log_status>
<function_3>()
    ├─ [✓/✗/⚠️] branch_1
    ├─ [✓/✗/⚠️] branch_2
    └─ [✓/✗/⚠️] branch_3
```

Legend:
- ✓ : Has required LOGE/LOGI
- ✗ : Missing required logging
- ⚠️ : Has high-frequency log risk

---

## Recommendations

### Immediate Actions (P0)
<list of critical items>

### Follow-up Actions (P1)
<list of important items>

### Long-term Improvements (P2)
<list of improvement suggestions>

================================================================================
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--path` | No | Repository path (default: current directory) |
| `--exclude-tests` | No | Exclude test files (default: true) |
| `--lang` | No | Language filter (cpp, java, python, js, all) |
| `--output` | No | Output report path |

## Usage Examples

```
# Analyze current directory
/log-coverage-analyzer

# Analyze specific repository
/log-coverage-analyzer --path /path/to/repo

# Analyze C++ code only
/log-coverage-analyzer --lang cpp --path /path/to/repo

# Include test files in analysis
/log-coverage-analyzer --exclude-tests false

# Custom output location
/log-coverage-analyzer --output /path/to/report.md
```

## Tips

- Use `Grep` with `output_mode: content` and `-B/-C` flags for context
- Use `Read` tool with `offset` and `limit` for large files
- For large repositories, focus on critical directories first
- High-frequency risks should be prioritized over minor log deficiencies
- Always include context (IDs, states, parameters) in LOGE messages
