---
name: repo
description: Create repository context bundles and code maps. Use to share codebase context, generate documentation, and understand project structure.
---

# Repository Context

Generate context bundles and maps for codebases.

## Structure Analysis

### Quick Structure

```bash
# Tree view (basic)
tree -L 2 -I 'node_modules|.git|dist|build'

# With file counts
tree -L 2 -I 'node_modules|.git' --dirsfirst -C

# Just directories
tree -d -L 3 -I 'node_modules|.git'
```

### Detailed Structure

```bash
#!/bin/bash
# repo-structure.sh

echo "# Repository Structure"
echo ""
echo "## Root Files"
ls -la | grep "^-" | awk '{print "- " $NF}'

echo ""
echo "## Directories"
for dir in */; do
  if [[ "$dir" != "node_modules/" && "$dir" != ".git/" ]]; then
    echo "### $dir"
    ls -la "$dir" | head -10
    echo ""
  fi
done
```

## Code Maps

### Generate Code Map

```bash
#!/bin/bash
# codemap.sh - Generate code map

echo "# Code Map"
echo ""

# Find all source files
find src -name "*.ts" -o -name "*.tsx" | while read file; do
  echo "## $file"
  echo '```typescript'

  # Extract exports
  grep -E "^export (function|const|class|interface|type)" "$file" | head -20

  echo '```'
  echo ""
done
```

### Function Index

```bash
# List all exported functions
grep -rh "^export function" src/ | sort

# With file locations
grep -rn "^export function" src/ | sort
```

### Class Index

```bash
# List all classes
grep -rn "^export class" src/ | sort

# With methods
grep -rh "^export class\|^\s*\(async \)\?[a-z]\+(" src/ | head -50
```

## Context Bundles

### Create Bundle for AI

```bash
#!/bin/bash
# bundle-context.sh - Create context for AI

OUTPUT="CONTEXT.md"

cat > $OUTPUT << 'EOF'
# Repository Context

## Project Overview
EOF

# Add package.json summary
if [ -f package.json ]; then
  echo '```json' >> $OUTPUT
  jq '{name, description, main, scripts: .scripts | keys}' package.json >> $OUTPUT
  echo '```' >> $OUTPUT
fi

# Add key files
echo "" >> $OUTPUT
echo "## Key Files" >> $OUTPUT

for file in src/index.ts src/main.ts app.ts; do
  if [ -f "$file" ]; then
    echo "" >> $OUTPUT
    echo "### $file" >> $OUTPUT
    echo '```typescript' >> $OUTPUT
    head -100 "$file" >> $OUTPUT
    echo '```' >> $OUTPUT
  fi
done

echo "Context bundle created: $OUTPUT"
```

### Smart Pack (Key Files Only)

```bash
#!/bin/bash
# smart-pack.sh - Pack only important files

# Identify key files
KEY_PATTERNS=(
  "package.json"
  "tsconfig.json"
  "src/index.ts"
  "src/main.ts"
  "README.md"
)

for pattern in "${KEY_PATTERNS[@]}"; do
  if [ -f "$pattern" ]; then
    echo "=== $pattern ==="
    cat "$pattern"
    echo ""
  fi
done
```

## Import Analysis

### Dependency Graph

```bash
# Find what imports what
grep -rh "^import.*from" src/ | \
  sed "s/.*from ['\"]//; s/['\"].*//" | \
  sort | uniq -c | sort -rn | head -20
```

### External Dependencies

```bash
# Most used external packages
grep -rh "^import.*from ['\"]" src/ | \
  grep -v "from ['\"]\./" | \
  sed "s/.*from ['\"]//; s/['\"].*//" | \
  sort | uniq -c | sort -rn
```

### Internal Module Graph

```bash
# Internal imports
grep -rh "^import.*from ['\"]\./" src/ | \
  sed "s/.*from ['\"]//; s/['\"].*//" | \
  sort | uniq -c | sort -rn
```

## AI-Powered Analysis

### Architecture Summary

```bash
STRUCTURE=$(tree -L 2 -I 'node_modules|.git' --dirsfirst)
PACKAGE=$(cat package.json 2>/dev/null)

gemini -m pro -o text -e "" "Analyze this repository structure:

Structure:
$STRUCTURE

package.json:
$PACKAGE

Provide:
1. Architecture pattern used
2. Main entry points
3. Key modules and their purpose
4. Dependencies overview
5. Suggested improvements"
```

### Code Quality Overview

```bash
# Get sample of files
SAMPLES=$(find src -name "*.ts" | head -5 | xargs cat)

gemini -m pro -o text -e "" "Review code quality:

$SAMPLES

Assess:
1. Code organization
2. Naming conventions
3. Error handling
4. Type safety
5. Suggestions"
```

## Documentation Generation

### Auto README

```bash
gemini -m pro -o text -e "" "Generate a README for this project:

package.json:
$(cat package.json)

Main file:
$(cat src/index.ts | head -100)

Include:
- Description
- Installation
- Usage
- API overview
- Contributing"
```

### API Documentation

```bash
# Extract all exports
EXPORTS=$(grep -rh "^export" src/ | head -50)

gemini -m pro -o text -e "" "Generate API documentation for:

$EXPORTS

Format as markdown with:
- Function signatures
- Parameter descriptions
- Return types
- Example usage"
```

## Best Practices

1. **Ignore noise** - Exclude node_modules, .git, build
2. **Focus on entry points** - Start with main files
3. **Track dependencies** - Understand what's imported
4. **Use AI for summaries** - Large codebases need synthesis
5. **Keep bundles updated** - Regenerate after major changes
6. **Share context** - Help others understand quickly
