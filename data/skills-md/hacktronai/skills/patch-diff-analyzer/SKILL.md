---
name: patch-diff-analyzer
description: Specialized in reverse-engineering compiled binaries (JARs, DLLs). Use this when the user asks to compare versions, find security fixes, or analyze binary patches.
license: MIT
compatibility: Requires git, jadx (for JAR), ilspycmd (for DLL)
metadata:
  author: hacktron
  version: "1.0.0"
---

# Patch Diff Analyzer

**IMPORTANT**: Users may request analysis of security patches in compiled binaries (JARs, DLLs, etc.) to understand what vulnerabilities were fixed. This extension helps decompile binaries, generate diffs, and identify security-relevant changes.

## Available scripts

The extension have these scripts:

- setup-workspace.sh `<workspace-name>`

**What it does**:
1. Creates workspace directory
2. Initializes git repository for diff tracking
3. Configures git user for commits
4. Creates subdirectories: `decompiled/`, `output/`

- decompile-jar.sh <app.jar> <workspace>/decompiled/

**What it does**:
1. Creates decompiled directory in workspace dir
2. Decompiles the jar file in the dir.

- decompile-dll.sh <app.dll> <workspace>/decompiled/

**What it does**:
1. Creates decompiled directory in workspace dir
2. Decompiles the dll file in the dir.

- analyze-diff.sh <workspace>

**What it does**:
1. Verifies git repository has 2+ commits
2. Identifies `unpatched` and `patched` tags (or uses HEAD~1 and HEAD)
3. Generates diff statistics
4. Creates `patch-analysis.diff` file
5. Creates `changed-files.txt` list

---

## Workflow Decision Tree

When a user requests patch analysis:

1. **Identifying Binaries**: Do you need to determine which file is patched vs unpatched?
   - **YES** → Go to [Binary Identification](#binary-identification)
   - **NO** → User has specified versions, proceed to [Setup & Decompilation](#setup--decompilation)

2. **File Format**: What type of binary are you analyzing?
   - **Java JAR** → Use [JAR Decompilation Workflow](#jar-decompilation-workflow)
   - **.NET DLL/EXE** → Use [.NET Decompilation Workflow](#net-decompilation-workflow)
   - **Other** → Consult user for appropriate decompiler

3. **Analysis Context**: Does the user provide vulnerability information?
   - **YES (CVE/Description provided)** → Focus analysis on related changes
   - **NO (Blind analysis)** → Perform comprehensive security change analysis

---

## Binary Identification

**CRITICAL**: Before decompilation, correctly identify which binary is the patched version.

### Identification Methods

1. **Explicit Naming**:
   - Files named `patched.jar` / `unpatched.jar`
   - Files named `vulnerable.jar` / `fixed.jar`
   - → Use as specified

2. **Version Numbers**:
   - `app-1.2.3.jar` vs `app-1.2.4.jar`
   - → Higher version number is typically patched (1.2.4 > 1.2.3)
   - For semantic versioning: major.minor.patch format

3. **File Timestamps**:
   ```bash
   ls -lt *.jar
   ```
   - Newer timestamp typically indicates patched version
   - **Note**: Not reliable if files were copied/moved

4. **When Ambiguous**:
   - **ALWAYS** ask the user for clarification
   - Do not guess if there's any uncertainty

---

## Setup & Decompilation

### Workspace Setup Script

Use the provided setup script.

---

## Efficient Extraction (Skip Third-Party Libraries)

**CRITICAL**: For WAR files or large applications, extract ONLY proprietary code before decompiling. This saves significant time and storage.

### Identify Proprietary Code Location

**WAR file structure**:
```
application.war
├── WEB-INF/
│   ├── classes/          ← Application code (DECOMPILE THIS)
│   │   └── com/
│   │       └── vendor/   ← Proprietary packages
│   └── lib/              ← Third-party JARs (SKIP THESE)
│       ├── jackson-*.jar
│       ├── spring-*.jar
│       └── hibernate-*.jar
└── META-INF/
```

### Extract Proprietary Code Only

```bash
# 1. List WAR contents to identify proprietary packages
unzip -l unpatched.war | grep "WEB-INF/classes" | grep "\.class$" | head -30

# Look for company-specific packages:
# WEB-INF/classes/com/acme/
# WEB-INF/classes/com/vendor/
# WEB-INF/classes/org/internal/

# 2. Extract ONLY proprietary classes
mkdir -p temp-unpatched
unzip unpatched.war "WEB-INF/classes/com/vendor/*" -d temp-unpatched/
unzip unpatched.war "WEB-INF/classes/com/acme/*" -d temp-unpatched/

# 3. Create JAR from extracted classes
cd temp-unpatched/WEB-INF/classes
jar cf ../../../vendor-unpatched.jar .
cd ../../..

# 4. Repeat for patched version
mkdir -p temp-patched
unzip patched.war "WEB-INF/classes/com/vendor/*" -d temp-patched/
unzip patched.war "WEB-INF/classes/com/acme/*" -d temp-patched/
cd temp-patched/WEB-INF/classes
jar cf ../../../vendor-patched.jar .
cd ../../..

# Now decompile ONLY proprietary code (much faster!)
```

---

## JAR Decompilation Workflow

### Step 1: Decompile Unpatched Version (Proprietary Code)

- Use the JAR decompilation script provided with extension to decompile the JAR.

### Step 2: Commit Unpatched Version

```bash
cd <workspace>
git add -A
git commit -m "Unpatched version"
git tag unpatched
```

**CRITICAL**: The `unpatched` tag is used by the diff analysis script.

### Step 3: Decompile Patched Version

**IMPORTANT**: Clear the decompiled directory first to avoid mixing files.

```bash
rm -rf <workspace>/decompiled/*
```

### Step 4: Commit Patched Version

```bash
cd <workspace>
git add -A
git commit -m "Patched version"
git tag patched
```

**CRITICAL**: The `patched` tag is used by the diff analysis script.

---

## .NET Decompilation Workflow

### Step 1: Decompile Unpatched Version

- Use the DLL decompilation script provided with extension to decompile the DLL.

### Step 2-4: Same as JAR Workflow

Follow the same git commit process as the JAR workflow:
1. Commit unpatched with tag
2. Clear directory
3. Decompile patched
4. Commit patched with tag

---

## Diff Generation & Analysis

### Generate Diff

- Use analyze-diff.sh `<workspace>` to generate `patch-analysis.diff` and `changed-files.txt` list

### Read and Analyze Diff

**MANDATORY**: Read the generated diff file completely.

**DO NOT** use grep or pattern matching. The LLM must read and reason about the actual code changes.

---

## Security Analysis

**CRITICAL**: This is where you apply security expertise to understand the vulnerability fix.

### Step 1: Filter Third-Party Libraries

**MANDATORY FIRST STEP**: Before analyzing changes, separate proprietary code from third-party libraries.

**Why This Matters**:
- Third-party library updates are expected and well-documented (Jackson, Spring, Hibernate, etc.)
- Proprietary code changes indicate application-specific security fixes
- Custom vulnerabilities are more interesting than known library CVEs
- Focusing on proprietary code reveals unique attack vectors

### Step 2: Analysis Process

1. **Read Every Change**: Don't skip any modifications, even small ones
2. **Understand Context**: Look at surrounding code, not just the diff lines
3. **Identify Security Changes**: Distinguish security fixes from refactoring/features
4. **Reason About Vulnerability**: What attack was possible before? What does the fix prevent?
5. **Assess Completeness**: Is the fix comprehensive or could there be bypasses?

### What to Look For

**High-Priority Indicators**:
- Input validation added where none existed
- Sanitization/encoding of user-controlled data
- Authentication/authorization checks introduced
- Bounds checking before array/buffer access
- Type checking or casting changes
- Canonicalization of file paths
- Parameterized queries replacing string concatenation
- Deserialization filters or whitelists
- Resource limits (size, timeout, rate)

---

## Reporting Findings

### Report Structure

**MANDATORY**: Use this structure for your analysis report:

```markdown
# Patch Analysis Summary

## Overview
[Brief description of what was analyzed]

## Vulnerability Identified: [Type/CVE]

**Severity**: [Critical/High/Medium/Low]

## Detailed Analysis

### File: [path/to/file.java:line-range]

[Detailed analysis following the framework above]

## Completeness Assessment

[Is the fix complete? Any potential bypasses? Additional recommendations?]

## Confidence Level

Overall confidence: [HIGH/MEDIUM/LOW] ([percentage]%)
```

---

## Error Messages & Solutions

### "No decompiler found"
**Solution**: Install jadx (for JAR) or ilspycmd (for DLL)

### "Not a git repository"
**Solution**: Run `setup-workspace.sh` script first

### "Need at least 2 commits"
**Solution**: Ensure both unpatched and patched versions were committed

### "No differences found"
**Solution**:
- Verify you decompiled different versions
- Check `git log` to see commits
- May indicate files are identical

