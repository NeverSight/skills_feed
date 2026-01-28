---
name: bundle
description: Bundle and share code as gists or markdown. Use to create shareable code bundles, extract imports, and create GitHub gists.
---

# Code Bundler

Bundle code for sharing via gists or markdown.

## Prerequisites

```bash
# GitHub CLI for gists
brew install gh
gh auth login
```

## CLI Reference

### GitHub Gists

#### Create Gist

```bash
# Single file gist (public)
gh gist create file.ts

# Private gist
gh gist create --private file.ts

# Multiple files
gh gist create file1.ts file2.ts file3.ts

# With description
gh gist create -d "My code snippet" file.ts

# From stdin
echo "console.log('hello')" | gh gist create -f hello.js

# Public with description
gh gist create -d "Utility functions" --public utils.ts helpers.ts
```

#### List Gists

```bash
# Your gists
gh gist list

# With limit
gh gist list --limit 20

# Public only
gh gist list --public

# Secret only
gh gist list --secret
```

#### View Gist

```bash
# View gist content
gh gist view <gist-id>

# View specific file
gh gist view <gist-id> --filename utils.ts

# Get raw content
gh gist view <gist-id> --raw
```

#### Edit Gist

```bash
# Edit in editor
gh gist edit <gist-id>

# Add file to gist
gh gist edit <gist-id> --add newfile.ts

# Remove file
gh gist edit <gist-id> --remove oldfile.ts
```

#### Clone Gist

```bash
# Clone as repo
gh gist clone <gist-id>

# Clone to specific directory
gh gist clone <gist-id> my-snippet
```

#### Delete Gist

```bash
gh gist delete <gist-id>
```

## Bundle Patterns

### Bundle File with Dependencies

```bash
#!/bin/bash
# bundle-file.sh - Bundle a file with its local imports

FILE=$1
OUTPUT=${2:-bundle.md}

echo "# Code Bundle" > $OUTPUT
echo "" >> $OUTPUT
echo "## Main File: $FILE" >> $OUTPUT
echo '```typescript' >> $OUTPUT
cat $FILE >> $OUTPUT
echo '```' >> $OUTPUT

# Extract and include imports
grep -E "^import.*from ['\"]\./" $FILE | while read import; do
  # Extract path
  path=$(echo $import | sed -E "s/.*from ['\"](.+)['\"].*/\1/")
  resolved="${path}.ts"
  if [ -f "$resolved" ]; then
    echo "" >> $OUTPUT
    echo "## $resolved" >> $OUTPUT
    echo '```typescript' >> $OUTPUT
    cat "$resolved" >> $OUTPUT
    echo '```' >> $OUTPUT
  fi
done

echo "Bundle created: $OUTPUT"
```

### Create CLAUDE.md for Project

```bash
#!/bin/bash
# Generate project context file

OUTPUT="CLAUDE.md"

echo "# Project Context" > $OUTPUT
echo "" >> $OUTPUT

# Package info
if [ -f "package.json" ]; then
  echo "## Dependencies" >> $OUTPUT
  echo '```json' >> $OUTPUT
  jq '.dependencies' package.json >> $OUTPUT
  echo '```' >> $OUTPUT
fi

# Key files
echo "" >> $OUTPUT
echo "## Key Files" >> $OUTPUT

for f in src/index.ts src/main.ts app.ts; do
  if [ -f "$f" ]; then
    echo "" >> $OUTPUT
    echo "### $f" >> $OUTPUT
    echo '```typescript' >> $OUTPUT
    head -100 "$f" >> $OUTPUT
    echo '```' >> $OUTPUT
  fi
done
```

### Share Code Snippet

```bash
# Quick share a file as gist
share-code() {
  local file=$1
  local desc=${2:-"Code snippet"}

  gh gist create -d "$desc" --public "$file" | tail -1
}

# Usage
share-code src/utils.ts "Utility functions"
```

## Import Extraction

### Find All Imports

```bash
# Extract import statements
grep -h "^import" src/**/*.ts | sort -u

# External imports only
grep -h "^import" src/**/*.ts | grep -v "from '\.\." | sort -u

# Local imports only
grep -h "^import" src/**/*.ts | grep "from '\.\." | sort -u
```

### Dependency Graph

```bash
# Show what imports what
for f in src/**/*.ts; do
  echo "=== $f ==="
  grep "^import" "$f" | sed 's/.*from /  <- /'
done
```

## Gist Workflow

### Code Review Share

```bash
# Share specific function for review
FILE=src/auth.ts
START=$(grep -n "export function login" $FILE | cut -d: -f1)
END=$(tail -n +$START $FILE | grep -n "^}" | head -1 | cut -d: -f1)

sed -n "${START},$((START+END-1))p" $FILE | \
  gh gist create -d "Login function for review" -f login.ts
```

### Quick Demo

```bash
# Create runnable demo
cat > /tmp/demo.ts << 'EOF'
// Demo: Array utilities
const nums = [1, 2, 3, 4, 5];
console.log(nums.filter(n => n % 2 === 0));
EOF

gh gist create -d "Quick demo" --public /tmp/demo.ts
```

### Documentation Gist

```bash
# Bundle docs with code
gh gist create \
  -d "My utility library" \
  README.md \
  src/utils.ts \
  examples/usage.ts
```

## Best Practices

1. **Add descriptions** - Use `-d` for context
2. **Use private by default** - Unless intentionally sharing
3. **Include README** - Explain what the code does
4. **Version important gists** - Clone and commit changes
5. **Clean before sharing** - Remove secrets, comments
6. **Bundle dependencies** - Include necessary context
