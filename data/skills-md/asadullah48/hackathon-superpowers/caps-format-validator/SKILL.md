---
name: caps-format-validator
description: Validate CAPS (Coding Agent Playbook Spec) playbooks for correctness, completeness, and compatibility with Claude Code and Goose
allowed-tools: bash_tool,view
---

# CAPS Format Validator

## Purpose
Validate CAPS playbooks to ensure correct formatting, completeness, and compatibility with both Claude Code Skills and Goose Recipes. Catch errors early before conversion or deployment.

## Prerequisites
- CAPS playbook file to validate (playbook.md)
- Python 3 (optional, for YAML validation)
- Basic understanding of CAPS format

## CAPS Format Requirements

Every valid CAPS playbook must have:
1. YAML frontmatter between `---` markers
2. `title` field in frontmatter
3. `description` field in frontmatter
4. `allowed_tools` array in frontmatter
5. Main content after frontmatter
6. `## Instructions` or `## Steps` section

## Instructions

### Step 1: Check File Structure
```bash
# Verify file exists
if [ ! -f "playbook.md" ]; then
    echo "❌ Error: playbook.md not found"
    exit 1
fi

# Check file not empty
if [ ! -s "playbook.md" ]; then
    echo "❌ Error: playbook.md is empty"
    exit 1
fi

echo "✅ File structure valid"
```

### Step 2: Validate YAML Frontmatter

Check that frontmatter exists and is valid YAML syntax between `---` markers.

### Step 3: Check Required Fields
```bash
# Check for title
if ! grep -q "^title:" playbook.md; then
    echo "❌ Missing required field: title"
    exit 1
fi

# Check for description
if ! grep -q "^description:" playbook.md; then
    echo "❌ Missing required field: description"
    exit 1
fi

# Check for allowed_tools
if ! grep -q "^allowed_tools:" playbook.md; then
    echo "❌ Missing required field: allowed_tools"
    exit 1
fi
```

### Step 4: Validate Content Structure

Check for Instructions section, code blocks, and step markers.

### Step 5: Test Conversion Compatibility

Verify the playbook can convert to both Claude Skills and Goose Recipes formats.

### Step 6: Check Best Practices

Check for Prerequisites, Validation, and Troubleshooting sections.

## Validation

Playbook is valid when:
- [ ] Has YAML frontmatter between `---` markers
- [ ] Includes title, description, allowed_tools
- [ ] allowed_tools is YAML array
- [ ] Has ## Instructions section
- [ ] Includes code examples
- [ ] Can convert to Claude Skills
- [ ] Can convert to Goose Recipes
- [ ] Passes validator with zero errors

## Common Errors

**Error**: Missing frontmatter
```markdown
❌ Wrong:
# My Playbook

✅ Correct:
---
title: My Playbook
---
```

**Error**: Incorrect tool format
```markdown
❌ Wrong:
allowed_tools: kubectl, helm

✅ Correct:
allowed_tools:
  - kubectl
  - helm
```

## Best Practices

1. **Test Before Committing**: Always validate locally
2. **Use Templates**: Start with valid template
3. **Include Examples**: Show commands and output
4. **Add Validation**: Define success criteria
5. **Version Playbooks**: Use semantic versioning
