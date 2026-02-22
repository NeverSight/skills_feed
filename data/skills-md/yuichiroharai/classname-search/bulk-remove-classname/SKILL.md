---
name: bulk-remove-classname
description: Removes a specified class name from HTML/JSX files using the classname-search CLI tool. Use when you need to safely remove all occurrences of a specified class name from target files.
---

# Guide to Bulk Removing a Class Name

## Prerequisites

Refer to the `classname-search` agent skill to understand how to use the `classname-search` CLI tool.

> [!WARNING]
> If the `classname-search` agent skill is not found, do not proceed with the work. Do not attempt to obtain information from the internet or other sources.

## Required Inputs

- A glob pattern to specify target files
- The class name to remove

## Before Proceeding

Before executing the removal, you must:

1. Ask the user to create a backup of the target files using their preferred method (e.g., Git commit, file copy, etc.)
2. Explain the work to the user
3. Warn that this will remove **all occurrences** of the specified class name from all matching files (bulk removal)
4. Proceed only after receiving explicit user approval

## Procedure

Execute the following steps for each target class name.

### 1. Record the State Before Removal

#### 1.1 Get and Record the Match Count

```bash
npx classname-search stats '<glob>' '^<class-name>$'
```

> [!IMPORTANT]
> Record the output match count (e.g., `Total: 7 matches in 2 files`). This will be referred to as the `pre-removal count`.

#### 1.2 Save Search Results to a File (for Verification)

```bash
npx classname-search search '<glob>' '^<class-name>$' --output 'verification-<class-name>.jsonl'
```

This file is used for verification and troubleshooting if an error occurs during the removal process.

### 2. Remove the Class Name

```bash
npx classname-search remove '<glob>' '^<class-name>$'
```

> [!IMPORTANT]
> Record the removal count shown in the command output (e.g., `Removed 7 matches`). This will be referred to as the `removal count`.

### 3. Post-Removal Verification

#### 3.1 Verify the Post-Removal Match Count

```bash
npx classname-search stats '<glob>' '^<class-name>$'
```

Record the output match count. This will be referred to as the `post-removal count`.

#### 3.2 Determine Verification Result

Verification is considered successful only if **both** of the following conditions are met:

1. The `post-removal count` is **0**
2. The `pre-removal count` and `removal count` **match**

**If verification succeeds**:

1. Delete the verification file:
   ```bash
   rm 'verification-<class-name>.jsonl'
   ```
2. Proceed to the next class name

**If verification fails**:

- **Always report to the user and stop subsequent work**

**Report contents**:

- Target class name
- Pre-removal count
- Removal count (output of replace command)
- Post-removal match count
- Path to verification file (`verification-<class-name>.jsonl`)
