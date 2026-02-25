---
name: unity-compile-fixer
description: Detect and resolve Unity C# compilation errors using VSCode diagnostics. Use this skill when Unity projects have compilation errors that need diagnosis and automated fixes. Analyzes errors from VSCode Language Server, proposes solutions based on error patterns, and handles version control conflicts for Unity projects.
---

# Unity Compile Fixer

## Overview

This skill enables automatic detection and resolution of Unity C# compilation errors by leveraging VSCode's diagnostic system. It collects real-time errors from the OmniSharp C# language server, analyzes error patterns against a curated database of common Unity issues, and proposes context-aware solutions for user approval before applying fixes.

## When to Use This Skill

Use this skill when:
- Unity projects report C# compilation errors in VSCode
- Need to diagnose the root cause of Unity compiler errors (CS* error codes)
- Want automated fix suggestions for common Unity scripting issues
- Working with Unity projects that have version control integration (Git, Unity Collaborate, Plastic SCM)
- Need to handle Unity .meta file conflicts

**Example user requests:**
- "Check Unity compilation errors and help me fix them"
- "My Unity project has compiler errors, can you diagnose and fix?"
- "Unity scripts are not compiling, what's wrong?"
- "Fix the C# errors in my Unity project"

## Workflow

Follow this workflow when the skill is invoked:

### 1. Detect Compilation Errors

Use the `mcp__ide__getDiagnostics` tool to collect errors from VSCode:

```typescript
// Collect all project diagnostics
mcp__ide__getDiagnostics()

// Or target specific Unity script files
mcp__ide__getDiagnostics({ uri: "file:///path/to/PlayerController.cs" })
```

Filter the diagnostics to focus on Unity-relevant errors:
- **Severity**: Only process errors with `severity: "Error"` (ignore warnings)
- **Source**: Only process `source: "csharp"` (OmniSharp C# diagnostics)
- **Error Codes**: Focus on CS* compiler error codes (e.g., CS0246, CS0029, CS1061)

### 2. Analyze Error Patterns

For each detected error:

1. **Extract error information:**
   - File path and line number from `uri` and `range`
   - Error code from `message` (e.g., "CS0246")
   - Full error message text

2. **Match against error pattern database:**
   - Load `references/error-patterns.json`
   - Find the error code entry (e.g., CS0246)
   - Retrieve common causes and solutions

3. **Read affected file context:**
   - Use Read tool to load the file with errors
   - Examine surrounding code for context
   - Identify missing imports, incorrect types, or API misuse

### 3. Generate Solution Proposals

For each error, create a structured fix proposal:

```markdown
**Error**: CS0246 at PlayerController.cs:45
**Message**: The type or namespace name 'Rigidbody' could not be found

**Analysis**:
- Missing using directive for UnityEngine namespace
- Common Unity API usage pattern

**Proposed Solution**:
Add `using UnityEngine;` at the top of PlayerController.cs

**Changes Required**:
- File: Assets/Scripts/PlayerController.cs
- Action: Insert using directive at line 1
```

### 4. User Confirmation

Before applying any fixes:

1. **Present all proposed solutions** in a clear, structured format
2. **Use AskUserQuestion tool** to get user approval:
   - List each error and proposed fix
   - Allow user to approve all, select specific fixes, or cancel

3. **Wait for explicit confirmation** - do not apply fixes automatically

### 5. Apply Approved Fixes

For each approved fix:

1. **Use Edit tool** to modify the affected file
2. **Preserve code formatting** and existing structure
3. **Apply minimal changes** - only fix the specific error

Example:
```typescript
Edit({
  file_path: "Assets/Scripts/PlayerController.cs",
  old_string: "public class PlayerController : MonoBehaviour",
  new_string: "using UnityEngine;\n\npublic class PlayerController : MonoBehaviour"
})
```

### 6. Verify Version Control Status

After applying fixes:

1. **Check for .meta file conflicts:**
   - Use Grep to search for Unity .meta files
   - Verify that script GUID hasn't changed
   - Check for merge conflict markers (<<<<<<, ======, >>>>>>)

2. **Report VCS status:**
   - List modified files
   - Warn about any .meta file issues
   - Suggest git operations if needed

### 7. Re-validate Compilation

After fixes are applied:

1. **Re-run diagnostics** using `mcp__ide__getDiagnostics()`
2. **Compare error count** before and after
3. **Report results** to the user:
   - Number of errors fixed
   - Remaining errors (if any)
   - Success rate

## Error Pattern Database

The skill relies on `references/error-patterns.json` for error analysis. This database contains:

- **Error Code**: CS* compiler error code
- **Description**: Human-readable explanation
- **Common Causes**: Typical reasons this error occurs in Unity
- **Solutions**: Step-by-step fix instructions
- **Unity-Specific Notes**: Unity API considerations

To analyze an error, load the database and match the error code:

```typescript
Read({ file_path: "references/error-patterns.json" })
// Parse JSON and find errorCode entry
```

## Analysis Scripts

The skill includes Node.js scripts in `scripts/` for complex error analysis:

### scripts/analyze-diagnostics.js

Processes VSCode diagnostics JSON output and extracts Unity-relevant errors.

**Usage:**
```bash
node scripts/analyze-diagnostics.js <diagnostics-json-file>
```

**Output:**
- Filtered list of Unity C# compilation errors
- Error classification by type (missing imports, type errors, API issues)
- Severity and file location information

This script can be run independently or invoked from the SKILL.md workflow when detailed analysis is needed.

## Best Practices

When using this skill:

1. **Start with full project diagnostics** - use `mcp__ide__getDiagnostics()` without parameters to get complete error picture
2. **Prioritize errors by severity and dependency** - fix foundational errors (missing imports) before downstream errors
3. **Batch related fixes** - group errors from the same file for efficient editing
4. **Always verify VCS status** - Unity .meta files are critical for version control
5. **Re-validate after fixes** - ensure errors are actually resolved

## Resources

### scripts/analyze-diagnostics.js
Node.js script for processing VSCode diagnostics and filtering Unity-specific C# errors.

### references/error-patterns.json
Curated database of common Unity C# compilation errors with solutions and Unity-specific guidance.
