---
name: go-function-analysis
description: Analyze Go function lengths within a workspace and generate statistics (p50, p90, p99). Use when you need to audit function complexity, identify long functions, or generate code metrics for Go projects. Only analyzes files matching **/*.go within the current workspace, excluding dependencies.
---

# Go Function Analysis

## Overview

This skill analyzes all Go functions in a workspace and generates:

1. A complete list of functions with their line counts and maximum call depths
2. Statistical analysis (p50, p90, p99 percentiles)

## When to Use

Use this skill when:

- Auditing code complexity in a Go project
- Identifying long functions that may need refactoring
- Generating code metrics for documentation
- Reviewing function size distribution

## How to Execute

### Step 1: Find All Go Files

Find all `.go` files in the workspace, excluding common dependency directories:

```bash
find . -name "*.go" -type f ! -path "./vendor/*" ! -path "./.git/*" ! -path "*_test.go"
```

### Step 2: Extract Functions and Calculate Lengths

For each `.go` file, use the helper script to extract function information:

```bash
./scripts/analyze_functions.sh <workspace_path>
```

Or manually parse using this approach for each file:

1. Find all function declarations with line numbers
2. For each function, count lines from `func` declaration to matching closing brace
3. Record: file path, function name, start line, end line, total lines

### Step 3: Calculate Percentiles

Given all function lengths sorted ascending:

- **p50** (median): Value at position `count * 0.50`
- **p90**: Value at position `count * 0.90`
- **p99**: Value at position `count * 0.99`

### Step 4: Generate README.function.md

Create `README.function.md` in the workspace root with this format:

```markdown
# Go Function Analysis

Generated: YYYY-MM-DD

## Summary Statistics

| File Path | Function Name | Function Lines | Depth Level | Percentile |
| --------- | ------------- | -------------- | ----------- | ---------- |
| path/to/f | funcName      | X              | Y           | p50        |
| ...       | ...           | ...            | ...         | ...        |

**Total functions:** N
**Average length:** X lines

## All Functions (sorted by length, descending)

| File Path | Function Name | Function Lines | Depth Level |
| --------- | ------------- | -------------- | ----------- |
| path/to/f | funcName      | X              | Y           |
| ...       | ...           | ...            | ...         |
```

---

## Manual Analysis Approach

If the script is not available, follow these steps:

### Finding Functions in Go

Go functions are declared with:

```go
func FunctionName(params) returnType {
    // body
}

func (receiver Type) MethodName(params) returnType {
    // body
}
```

### Counting Lines

For each function:

1. Start from the `func` keyword line
2. Count until the matching closing `}`
3. Include the `func` and `}` lines in the count

### Example

```go
func example() {     // Line 1
    fmt.Println()    // Line 2
    if true {        // Line 3
        doSomething()// Line 4
    }                // Line 5
}                    // Line 6
```

This function has **6 lines**.

---

## Important Notes

> [!NOTE]
> Only analyze `.go` files within the workspace.
> Exclude `/vendor/`, `/.git/`, and external dependencies.

> [!TIP]
> Functions over 50 lines may be candidates for refactoring.
> p90+ functions often warrant closer review.
