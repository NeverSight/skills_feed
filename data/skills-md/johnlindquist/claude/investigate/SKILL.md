---
name: investigate
description: Debug and investigate code issues using search and AI analysis. Use when stuck on bugs, tracing execution flow, or understanding complex code.
---

# Investigation Toolkit

Debug issues through systematic search and AI-powered analysis.

## Prerequisites

```bash
# ripgrep for fast search
brew install ripgrep

# Gemini for analysis
pip install google-generativeai
export GEMINI_API_KEY=your_api_key
```

## Search Commands

### ripgrep Basics

```bash
# Search for pattern
rg "pattern" src/

# Case insensitive
rg -i "error" src/

# Whole word
rg -w "user" src/

# File types
rg -t ts "function" src/
rg -t py "def " src/

# Exclude patterns
rg "TODO" --glob "!node_modules"

# Show context
rg -C 3 "error" src/  # 3 lines before and after
rg -B 5 "crash" src/  # 5 lines before
rg -A 5 "crash" src/  # 5 lines after

# Just filenames
rg -l "pattern" src/

# Count matches
rg -c "pattern" src/
```

### Finding Definitions

```bash
# Function definitions (TypeScript)
rg "function\s+functionName" src/
rg "(const|let|var)\s+functionName\s*=" src/
rg "export\s+(async\s+)?function\s+\w+" src/

# Class definitions
rg "class\s+ClassName" src/

# Interface/Type definitions
rg "(interface|type)\s+TypeName" src/
```

### Tracing Usage

```bash
# Where is this function called?
rg "functionName\(" src/

# Where is this imported?
rg "import.*functionName" src/

# Where is this exported?
rg "export.*functionName" src/
```

## Investigation Patterns

### Bug Investigation

```bash
# 1. Search for error message
rg "exact error message" .

# 2. Find where error is thrown
rg "throw.*Error" src/ -C 3

# 3. Trace the function
rg "functionThatFails" src/ -C 5

# 4. Check recent changes
git log --oneline -20 --all -- src/problematic-file.ts
git diff HEAD~5 -- src/problematic-file.ts
```

### Trace Execution Flow

```bash
#!/bin/bash
ENTRY_POINT=$1

echo "=== Entry Point ==="
rg -A 10 "export.*$ENTRY_POINT" src/

echo "=== Called Functions ==="
rg -o "\w+\(" src/$ENTRY_POINT*.ts | sort -u

echo "=== Dependencies ==="
rg "^import" src/$ENTRY_POINT*.ts
```

### AI-Assisted Debugging

```bash
# Analyze error with context
ERROR="Your error message here"
CODE=$(cat problematic-file.ts)

gemini -m pro -o text -e "" "Debug this error:

ERROR: $ERROR

CODE:
$CODE

Provide:
1. Most likely cause
2. How to verify
3. How to fix
4. How to prevent in future"
```

### Hypothesis Testing

```bash
# Generate hypotheses
gemini -m pro -o text -e "" "Given this bug symptom:

SYMPTOM: [describe what's happening]
CONTEXT: [relevant code/system info]

Generate 5 hypotheses ranked by likelihood, with a test for each."

# Then test each hypothesis
rg "hypothesis-related-pattern" src/
```

## Common Investigations

### Find All Error Handling

```bash
rg "catch|\.catch|try\s*{" src/ -t ts
rg "throw\s+new" src/ -t ts
```

### Find API Endpoints

```bash
rg "(get|post|put|delete|patch)\s*\(" src/ -i
rg "router\.(get|post|put|delete)" src/
rg "@(Get|Post|Put|Delete)" src/
```

### Find Database Queries

```bash
rg "(SELECT|INSERT|UPDATE|DELETE)" src/ -i
rg "\.query\(|\.execute\(" src/
rg "prisma\.\w+\.(find|create|update|delete)" src/
```

### Find Configuration

```bash
rg "process\.env\." src/
rg "(config|settings)\[" src/
rg "getenv|os\.environ" src/ -t py
```

### Find Security Issues

```bash
# SQL injection potential
rg "query.*\+.*\"|'.*\+" src/

# Hardcoded secrets
rg "(password|secret|key|token)\s*=\s*['\"]" src/ -i

# Unsafe eval
rg "eval\(" src/
```

## Deep Investigation Script

```bash
#!/bin/bash
# investigate.sh - Comprehensive code investigation

TERM=$1
echo "=== Investigating: $TERM ==="

echo ""
echo "### Definitions ###"
rg "^(export\s+)?(function|const|class|interface|type)\s+$TERM" src/

echo ""
echo "### Usage ###"
rg "$TERM" src/ --stats | head -50

echo ""
echo "### Recent Changes ###"
git log --oneline -10 -S "$TERM"

echo ""
echo "### Blame ###"
for f in $(rg -l "$TERM" src/); do
  echo "--- $f ---"
  git blame -L "/$TERM/,+5" "$f" 2>/dev/null | head -10
done
```

## Best Practices

1. **Start with the error** - Search for exact message first
2. **Expand context** - Use `-C`, `-B`, `-A` for surrounding code
3. **Check history** - `git log -S` finds when code was introduced
4. **Use AI for complex** - When pattern matching isn't enough
5. **Document findings** - Note what you discover
6. **Test hypotheses** - Verify before assuming
