---
name: skills-collection-manager
description: Comprehensive toolkit for managing large Claude Code skill collections including bulk downloading from GitHub, organizing into categories, detecting and removing duplicates, consolidating skills, and maintaining clean skill repositories with 100+ skills.
license: MIT
tags: [skills, collection-management, automation, organization, deduplication]
---

# Skills Collection Manager

Efficiently manage, organize, and maintain large collections of Claude Code skills at scale.

## Overview

As skill collections grow to hundreds of entries, manual management becomes impractical. This skill provides automated tools and workflows for:
- Bulk downloading skills from GitHub repositories
- Organizing skills into logical categories
- Detecting and removing duplicates
- Consolidating similar skills
- Maintaining repository health
- Generating documentation and indexes

## When to Use

Use this skill when:
- Managing 50+ skills in a collection
- Importing skills from multiple GitHub repositories
- Organizing an unstructured skill directory
- Identifying duplicate or redundant skills
- Creating team-wide skill libraries
- Maintaining organizational skill repositories
- Building curated skill collections
- Auditing skill quality and coverage

## Directory Structure Patterns

### Pattern 1: Flat Structure

```
skills/
├── docker-helper/
│   └── SKILL.md
├── kubernetes-deploy/
│   └── SKILL.md
├── postgres-optimization/
│   └── SKILL.md
└── ...
```

**Pros**: Simple, easy to navigate
**Cons**: Hard to manage at scale (100+ skills)

### Pattern 2: Categorized Structure

```
skills/
├── automation/
│   ├── skill-harvester/
│   │   └── SKILL.md
│   └── workflow-automation/
│       └── SKILL.md
├── backend/
│   ├── api-design/
│   │   └── SKILL.md
│   └── database-optimization/
│       └── SKILL.md
├── devops/
│   ├── docker-optimization/
│   │   └── SKILL.md
│   └── kubernetes-deploy/
│       └── SKILL.md
└── ...
```

**Pros**: Organized, scalable
**Cons**: Requires categorization logic

### Pattern 3: Hybrid Structure

```
skills/              # Flat for easy access
skills-by-category/  # Organized for browsing
duplicates/          # Quarantine area
archived/            # Old/deprecated skills
```

**Pros**: Best of both worlds
**Cons**: More complex to maintain

## Bulk Skill Download

### Download from GitHub Repository

```bash
#!/bin/bash
# bulk-download-skills.sh - Download skills from GitHub repos

REPOS_FILE="${1:-repos.txt}"
OUTPUT_DIR="downloaded-skills"
CHECKPOINT="download-checkpoint.txt"

# Create repos list if it doesn't exist
if [ ! -f "$REPOS_FILE" ]; then
    cat > "$REPOS_FILE" << EOF
https://github.com/anthropics/claude-code-skills
https://github.com/user/custom-skills
https://github.com/team/shared-skills
EOF
    echo "Created example $REPOS_FILE - edit and run again"
    exit 0
fi

mkdir -p "$OUTPUT_DIR"

# Process repos in batches
while read -r repo_url; do
    # Skip comments and empty lines
    [[ "$repo_url" =~ ^# ]] && continue
    [[ -z "$repo_url" ]] && continue

    # Check if already downloaded
    if grep -q "$repo_url" "$CHECKPOINT" 2>/dev/null; then
        echo "✓ Skipping $repo_url (already downloaded)"
        continue
    fi

    echo "=== Downloading: $repo_url ==="

    # Extract repo name
    REPO_NAME=$(basename "$repo_url" .git)
    TEMP_DIR=$(mktemp -d)

    # Clone with timeout
    if timeout 60s git clone --depth 1 "$repo_url" "$TEMP_DIR" 2>/dev/null; then
        # Find and copy skill files
        SKILLS_FOUND=0

        # Look for skills in common locations
        for PATTERN in "skills/*/SKILL.md" "skills/**/skill.md" ".claude/skills/*/SKILL.md"; do
            find "$TEMP_DIR" -path "*/$PATTERN" 2>/dev/null | while read skill_file; do
                # Extract skill name (parent directory)
                SKILL_NAME=$(basename $(dirname "$skill_file"))
                DEST_DIR="$OUTPUT_DIR/${REPO_NAME}/${SKILL_NAME}"

                mkdir -p "$DEST_DIR"
                cp "$skill_file" "$DEST_DIR/"

                # Copy additional files if present
                SKILL_DIR=$(dirname "$skill_file")
                cp "$SKILL_DIR"/*.md "$DEST_DIR/" 2>/dev/null || true
                cp "$SKILL_DIR"/*.yaml "$DEST_DIR/" 2>/dev/null || true
                cp "$SKILL_DIR"/*.json "$DEST_DIR/" 2>/dev/null || true

                SKILLS_FOUND=$((SKILLS_FOUND + 1))
                echo "  ✓ Copied: $SKILL_NAME"
            done
        done

        if [ $SKILLS_FOUND -gt 0 ]; then
            echo "$repo_url" >> "$CHECKPOINT"
            echo "✓ Downloaded $SKILLS_FOUND skills from $REPO_NAME"
        else
            echo "⚠️  No skills found in $REPO_NAME"
        fi

        rm -rf "$TEMP_DIR"
    else
        echo "✗ Failed to clone $repo_url"
    fi

    echo ""
done < "$REPOS_FILE"

# Summary
TOTAL_SKILLS=$(find "$OUTPUT_DIR" -name "SKILL.md" -o -name "skill.md" | wc -l)
echo "=== Download Complete ==="
echo "Total skills downloaded: $TOTAL_SKILLS"
echo "Output directory: $OUTPUT_DIR"
```

### Batch Download Script

```bash
#!/bin/bash
# download-top-repos.sh - Download skills from popular repositories

# Top Claude Code skill repositories
REPOS=(
    "https://github.com/anthropics/claude-code-skills"
    "https://github.com/works/claude-code-skills"
    "https://github.com/jonbaker99/my-claude-code-skills"
    "https://github.com/diet103/my_claude_skills"
    "https://github.com/mrgoonie/my-claude-code-skills"
)

BATCH_SIZE=5
PROCESSED=0

for repo in "${REPOS[@]}"; do
    echo "$repo" >> repos-batch.txt
    PROCESSED=$((PROCESSED + 1))

    # Process in batches to avoid timeouts
    if [ $((PROCESSED % BATCH_SIZE)) -eq 0 ]; then
        ./bulk-download-skills.sh repos-batch.txt
        rm repos-batch.txt
        echo "Batch complete. Continuing..."
        sleep 2
    fi
done

# Process remaining
if [ -f repos-batch.txt ]; then
    ./bulk-download-skills.sh repos-batch.txt
    rm repos-batch.txt
fi
```

## Skill Organization

### Auto-Categorization

```bash
#!/bin/bash
# categorize-skills.sh - Auto-categorize skills based on content

SKILLS_DIR="${1:-skills}"
OUTPUT_DIR="skills-by-category"

# Category mapping based on keywords
declare -A CATEGORIES=(
    ["docker|container|kubernetes|k8s"]="infrastructure"
    ["api|endpoint|rest|graphql|backend"]="backend"
    ["react|vue|angular|frontend|ui|component"]="frontend"
    ["test|testing|jest|pytest|mocha"]="testing"
    ["ci|cd|deploy|github.action|jenkins"]="devops"
    ["database|postgres|mysql|mongodb|sql"]="databases"
    ["auth|authentication|jwt|oauth|security"]="security"
    ["aws|azure|gcp|cloud|serverless"]="cloud"
    ["python|javascript|typescript|golang|rust"]="development"
    ["doc|documentation|readme|markdown"]="documentation"
)

mkdir -p "$OUTPUT_DIR"

# Process each skill
find "$SKILLS_DIR" -name "SKILL.md" -o -name "skill.md" | while read skill_file; do
    SKILL_NAME=$(basename $(dirname "$skill_file"))
    SKILL_CONTENT=$(cat "$skill_file" | tr '[:upper:]' '[:lower:]')

    echo "Processing: $SKILL_NAME"

    # Try to match category
    MATCHED_CATEGORY=""
    for pattern in "${!CATEGORIES[@]}"; do
        if echo "$SKILL_CONTENT" | grep -qE "$pattern"; then
            MATCHED_CATEGORY="${CATEGORIES[$pattern]}"
            break
        fi
    done

    # Default category if no match
    if [ -z "$MATCHED_CATEGORY" ]; then
        MATCHED_CATEGORY="uncategorized"
    fi

    # Copy to categorized directory
    DEST_DIR="$OUTPUT_DIR/$MATCHED_CATEGORY/$SKILL_NAME"
    mkdir -p "$DEST_DIR"
    cp -r "$(dirname $skill_file)"/* "$DEST_DIR/"

    echo "  → $MATCHED_CATEGORY"
done

# Generate summary
echo ""
echo "=== Categorization Summary ==="
for category_dir in "$OUTPUT_DIR"/*; do
    CATEGORY=$(basename "$category_dir")
    COUNT=$(find "$category_dir" -name "SKILL.md" -o -name "skill.md" | wc -l)
    printf "%-20s : %3d skills\n" "$CATEGORY" "$COUNT"
done
```

### Manual Reorganization

```bash
#!/bin/bash
# reorganize-skills.sh - Interactive skill reorganization

SKILLS_DIR="skills"
CATEGORIES=("automation" "backend" "cloud" "data-engineering" "devops" "documentation" "frontend" "infrastructure" "security" "testing")

# Show uncategorized skills
echo "=== Uncategorized Skills ==="
find "$SKILLS_DIR" -maxdepth 1 -type d | tail -n +2 | while read skill_dir; do
    SKILL_NAME=$(basename "$skill_dir")
    echo "- $SKILL_NAME"
done

echo ""
echo "Available categories:"
for i in "${!CATEGORIES[@]}"; do
    echo "$((i+1))) ${CATEGORIES[$i]}"
done

echo ""
read -p "Reorganize skills? (y/n) " -n 1 -r
echo
[[ ! $REPLY =~ ^[Yy]$ ]] && exit 0

find "$SKILLS_DIR" -maxdepth 1 -type d | tail -n +2 | while read skill_dir; do
    SKILL_NAME=$(basename "$skill_dir")

    echo ""
    echo "Skill: $SKILL_NAME"
    echo "Description: $(grep -m 1 "description:" "$skill_dir/SKILL.md" 2>/dev/null | cut -d: -f2-)"
    echo ""

    read -p "Category (1-${#CATEGORIES[@]}, s=skip): " choice

    if [[ "$choice" =~ ^[0-9]+$ ]] && [ "$choice" -ge 1 ] && [ "$choice" -le "${#CATEGORIES[@]}" ]; then
        CATEGORY="${CATEGORIES[$((choice-1))]}"
        DEST_DIR="skills-by-category/$CATEGORY/$SKILL_NAME"

        mkdir -p "$DEST_DIR"
        mv "$skill_dir"/* "$DEST_DIR/"
        rmdir "$skill_dir"

        echo "✓ Moved to $CATEGORY"
    fi
done
```

## Duplicate Detection

### Simple Duplicate Finder

```bash
#!/bin/bash
# find-duplicates.sh - Find duplicate skills

SKILLS_DIR="${1:-skills}"
DUPLICATES_DIR="duplicates"

mkdir -p "$DUPLICATES_DIR"

# Create temporary index
TEMP_INDEX=$(mktemp)

# Index all skills by normalized name
find "$SKILLS_DIR" -name "SKILL.md" -o -name "skill.md" | while read skill_file; do
    SKILL_DIR=$(dirname "$skill_file")
    SKILL_NAME=$(basename "$SKILL_DIR")

    # Normalize name (remove variations)
    NORMALIZED=$(echo "$SKILL_NAME" | tr '[:upper:]' '[:lower:]' | sed 's/[-_]//g')

    echo "$NORMALIZED|$SKILL_DIR" >> "$TEMP_INDEX"
done

# Find duplicates
cat "$TEMP_INDEX" | cut -d'|' -f1 | sort | uniq -d | while read dup_name; do
    echo "=== Duplicate: $dup_name ==="

    grep "^$dup_name|" "$TEMP_INDEX" | cut -d'|' -f2 | while read skill_dir; do
        ORIGINAL_NAME=$(basename "$skill_dir")
        echo "  - $ORIGINAL_NAME"

        # Move to duplicates folder
        DUP_DEST="$DUPLICATES_DIR/$ORIGINAL_NAME"
        if [ ! -d "$DUP_DEST" ]; then
            mv "$skill_dir" "$DUP_DEST"
            echo "    → Moved to $DUPLICATES_DIR"
        fi
    done
    echo ""
done

rm "$TEMP_INDEX"

# Summary
DUP_COUNT=$(find "$DUPLICATES_DIR" -name "SKILL.md" -o -name "skill.md" | wc -l)
echo "Found $DUP_COUNT potential duplicates in $DUPLICATES_DIR"
echo "Review and manually merge or delete"
```

### Advanced Duplicate Detection (Content-based)

```python
#!/usr/bin/env python3
# detect-duplicates.py - Content-based duplicate detection

import os
import re
from pathlib import Path
from difflib import SequenceMatcher
from collections import defaultdict

def normalize_content(content):
    """Normalize content for comparison"""
    # Remove frontmatter
    content = re.sub(r'^---.*?---', '', content, flags=re.DOTALL)
    # Remove whitespace and lowercase
    content = re.sub(r'\s+', ' ', content.lower())
    return content.strip()

def similarity_ratio(content1, content2):
    """Calculate similarity ratio between two contents"""
    return SequenceMatcher(None, content1, content2).ratio()

def find_duplicates(skills_dir, threshold=0.8):
    """Find skills with similar content"""
    skills = {}

    # Read all skills
    for skill_file in Path(skills_dir).rglob('SKILL.md'):
        skill_name = skill_file.parent.name
        with open(skill_file, 'r', encoding='utf-8') as f:
            content = normalize_content(f.read())
            skills[skill_name] = {
                'content': content,
                'path': str(skill_file.parent)
            }

    # Find duplicates
    duplicates = defaultdict(list)
    checked = set()

    for name1, data1 in skills.items():
        for name2, data2 in skills.items():
            if name1 == name2 or (name1, name2) in checked:
                continue

            ratio = similarity_ratio(data1['content'], data2['content'])

            if ratio >= threshold:
                duplicates[name1].append({
                    'name': name2,
                    'similarity': ratio,
                    'path': data2['path']
                })

            checked.add((name1, name2))
            checked.add((name2, name1))

    # Report findings
    if duplicates:
        print("=== Duplicate Skills Found ===\n")
        for skill, dups in duplicates.items():
            print(f"{skill}:")
            for dup in dups:
                print(f"  - {dup['name']} ({dup['similarity']:.1%} similar)")
                print(f"    Path: {dup['path']}")
            print()

        print(f"\nTotal duplicate groups: {len(duplicates)}")
    else:
        print("No duplicates found")

if __name__ == '__main__':
    import sys
    skills_dir = sys.argv[1] if len(sys.argv) > 1 else 'skills'
    threshold = float(sys.argv[2]) if len(sys.argv) > 2 else 0.8

    find_duplicates(skills_dir, threshold)
```

## Skill Consolidation

### Merge Similar Skills

```bash
#!/bin/bash
# consolidate-skills.sh - Merge similar skills

SKILL1_DIR="$1"
SKILL2_DIR="$2"
OUTPUT_NAME="$3"

if [ -z "$SKILL1_DIR" ] || [ -z "$SKILL2_DIR" ] || [ -z "$OUTPUT_NAME" ]; then
    echo "Usage: $0 <skill1-dir> <skill2-dir> <output-name>"
    exit 1
fi

OUTPUT_DIR="skills/$OUTPUT_NAME"
mkdir -p "$OUTPUT_DIR"

# Extract metadata from both skills
SKILL1_NAME=$(grep "^name:" "$SKILL1_DIR/SKILL.md" | cut -d: -f2 | xargs)
SKILL2_NAME=$(grep "^name:" "$SKILL2_DIR/SKILL.md" | cut -d: -f2 | xargs)

DESC1=$(grep "^description:" "$SKILL1_DIR/SKILL.md" | cut -d: -f2 | xargs)
DESC2=$(grep "^description:" "$SKILL2_DIR/SKILL.md" | cut -d: -f2 | xargs)

# Create consolidated skill
cat > "$OUTPUT_DIR/SKILL.md" << EOF
---
name: $OUTPUT_NAME
description: Consolidated skill combining $SKILL1_NAME and $SKILL2_NAME
consolidated-from:
  - $SKILL1_NAME
  - $SKILL2_NAME
license: MIT
---

# ${OUTPUT_NAME^}

This skill consolidates functionality from:
- **$SKILL1_NAME**: $DESC1
- **$SKILL2_NAME**: $DESC2

## From $SKILL1_NAME

$(sed -n '/^# /,$ p' "$SKILL1_DIR/SKILL.md" | tail -n +2)

---

## From $SKILL2_NAME

$(sed -n '/^# /,$ p' "$SKILL2_DIR/SKILL.md" | tail -n +2)

---

## Combined Usage

TODO: Add guidance on using consolidated functionality

EOF

echo "✓ Created consolidated skill: $OUTPUT_DIR"
echo "Review and edit: $OUTPUT_DIR/SKILL.md"
```

## Repository Maintenance

### Health Check

```bash
#!/bin/bash
# health-check.sh - Check repository health

SKILLS_DIR="${1:-skills}"

echo "=== Skills Repository Health Check ==="
echo ""

# Count total skills
TOTAL=$(find "$SKILLS_DIR" -name "SKILL.md" -o -name "skill.md" | wc -l)
echo "Total skills: $TOTAL"
echo ""

# Check for required files
echo "=== Missing Files ==="
MISSING=0
find "$SKILLS_DIR" -type d -mindepth 1 | while read skill_dir; do
    if [ ! -f "$skill_dir/SKILL.md" ] && [ ! -f "$skill_dir/skill.md" ]; then
        echo "✗ $(basename $skill_dir): No SKILL.md file"
        MISSING=$((MISSING + 1))
    fi
done
[ $MISSING -eq 0 ] && echo "✓ All skills have SKILL.md files"
echo ""

# Check for metadata
echo "=== Missing Metadata ==="
find "$SKILLS_DIR" -name "SKILL.md" -o -name "skill.md" | while read skill_file; do
    SKILL_NAME=$(basename $(dirname "$skill_file"))

    # Check for required frontmatter
    if ! grep -q "^name:" "$skill_file"; then
        echo "✗ $SKILL_NAME: Missing 'name' in frontmatter"
    fi

    if ! grep -q "^description:" "$skill_file"; then
        echo "✗ $SKILL_NAME: Missing 'description' in frontmatter"
    fi
done
echo ""

# Check for empty files
echo "=== Empty Skills ==="
find "$SKILLS_DIR" -name "SKILL.md" -o -name "skill.md" | while read skill_file; do
    if [ ! -s "$skill_file" ]; then
        echo "✗ $(basename $(dirname $skill_file)): Empty file"
    fi
done
echo ""

# Check naming conventions
echo "=== Naming Convention Issues ==="
find "$SKILLS_DIR" -type d -mindepth 1 | while read skill_dir; do
    SKILL_NAME=$(basename "$skill_dir")

    # Check for kebab-case
    if ! echo "$SKILL_NAME" | grep -qE '^[a-z0-9]+(-[a-z0-9]+)*$'; then
        echo "⚠️  $SKILL_NAME: Not in kebab-case format"
    fi
done
echo ""

echo "=== Health Check Complete ==="
```

### Generate Documentation

```bash
#!/bin/bash
# generate-docs.sh - Generate skill collection documentation

SKILLS_DIR="${1:-skills}"
OUTPUT_FILE="SKILLS_COLLECTION_README.md"

cat > "$OUTPUT_FILE" << EOF
# Skills Collection

Auto-generated documentation for skill collection.

**Last Updated**: $(date +"%Y-%m-%d")
**Total Skills**: $(find "$SKILLS_DIR" -name "SKILL.md" -o -name "skill.md" | wc -l)

## Skills by Category

EOF

# Group by category (if using categorized structure)
if [ -d "skills-by-category" ]; then
    for category_dir in skills-by-category/*; do
        CATEGORY=$(basename "$category_dir")
        COUNT=$(find "$category_dir" -name "SKILL.md" -o -name "skill.md" | wc -l)

        echo "### ${CATEGORY^} ($COUNT)" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"

        find "$category_dir" -name "SKILL.md" -o -name "skill.md" | sort | while read skill_file; do
            SKILL_NAME=$(basename $(dirname "$skill_file"))
            DESC=$(grep "^description:" "$skill_file" | cut -d: -f2- | xargs)

            echo "- **$SKILL_NAME**: $DESC" >> "$OUTPUT_FILE"
        done

        echo "" >> "$OUTPUT_FILE"
    done
else
    # Flat structure
    find "$SKILLS_DIR" -name "SKILL.md" -o -name "skill.md" | sort | while read skill_file; do
        SKILL_NAME=$(basename $(dirname "$skill_file"))
        DESC=$(grep "^description:" "$skill_file" | cut -d: -f2- | xargs)

        echo "- **$SKILL_NAME**: $DESC" >> "$OUTPUT_FILE"
    done
fi

echo "✓ Generated: $OUTPUT_FILE"
```

## Best Practices

### ✅ DO

1. **Categorize consistently** - Use standard categories across team
2. **Check for duplicates** regularly before adding new skills
3. **Maintain metadata** - Ensure all skills have proper frontmatter
4. **Document changes** - Keep CHANGELOG or version history
5. **Use naming conventions** - kebab-case for all skill names
6. **Version control** - Commit frequently with clear messages
7. **Test skills** - Verify skills work before adding to collection
8. **Review regularly** - Audit collection health monthly

### ❌ DON'T

1. **Don't mix formats** - Keep consistent SKILL.md naming
2. **Don't duplicate** - Search before creating new skills
3. **Don't leave orphans** - Remove skills properly (don't just delete files)
4. **Don't skip descriptions** - Every skill needs clear description
5. **Don't over-categorize** - Keep category tree shallow (1-2 levels)
6. **Don't hoard** - Archive or delete truly obsolete skills
7. **Don't ignore errors** - Fix health check issues promptly

## Workflows

### Weekly Maintenance

```bash
#!/bin/bash
# weekly-maintenance.sh

echo "=== Weekly Skills Collection Maintenance ==="

# 1. Health check
./health-check.sh skills

# 2. Find duplicates
./find-duplicates.sh skills

# 3. Update documentation
./generate-docs.sh skills

# 4. Commit changes
git add .
git commit -m "chore: Weekly skills collection maintenance"

echo "✓ Maintenance complete"
```

### New Skills Integration

```bash
#!/bin/bash
# integrate-new-skills.sh

NEW_SKILLS_DIR="$1"

# 1. Check for duplicates against existing
echo "Checking for duplicates..."
# ... duplicate check logic ...

# 2. Auto-categorize
echo "Categorizing new skills..."
./categorize-skills.sh "$NEW_SKILLS_DIR"

# 3. Move to main collection
echo "Integrating into collection..."
cp -r "$NEW_SKILLS_DIR"/* skills/

# 4. Update docs
./generate-docs.sh

echo "✓ Integration complete"
```

---

**Version**: 1.0.0
**Author**: Harvested from your_claude_skills repository (270+ skills managed)
**Last Updated**: 2025-11-18
**License**: MIT

## Quick Reference

```bash
# Download skills from GitHub repos
./bulk-download-skills.sh repos.txt

# Auto-categorize skills
./categorize-skills.sh skills/

# Find duplicates
./find-duplicates.sh skills/

# Run health check
./health-check.sh skills/

# Generate documentation
./generate-docs.sh skills/

# Weekly maintenance
./weekly-maintenance.sh
```

Scale your skill collection management with confidence! 📚
