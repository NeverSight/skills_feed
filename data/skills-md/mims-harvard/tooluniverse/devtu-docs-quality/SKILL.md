---
name: devtu-docs-quality
description: Comprehensive documentation quality system combining automated validation with ToolUniverse-specific auditing. Detects outdated commands, circular navigation, inconsistent terminology, auto-generated file conflicts, broken links, and structural problems. Use when reviewing documentation, before releases, after refactoring, or when user asks to audit, optimize, or improve documentation quality.
---

# Documentation Quality Assurance

Systematic documentation quality system combining automated validation scripts with ToolUniverse-specific structural audits.

## When to Use

- Pre-release documentation review
- After major refactoring (commands, APIs, tool counts changed)
- User reports confusing or outdated documentation
- Circular navigation or structural problems suspected
- Want to establish automated validation pipeline

## Approach: Two-Phase Strategy

**Phase A: Automated Validation** (15-20 min)
- Create validation scripts for systematic detection
- Test commands, links, terminology consistency
- Priority-based fixes (blockers → polish)

**Phase B: ToolUniverse-Specific Audit** (20-25 min)
- Circular navigation checks
- MCP configuration duplication
- Tool count consistency
- Auto-generated file conflicts

## Phase A: Automated Validation

### A1. Build Validation Script

Create `scripts/validate_documentation.py`:

```python
#!/usr/bin/env python3
"""Documentation validator for ToolUniverse"""

import re
import glob
from pathlib import Path

DOCS_ROOT = Path("docs")

# ToolUniverse-specific patterns
DEPRECATED_PATTERNS = [
    (r"python -m tooluniverse\.server", "tooluniverse-server"),
    (r"600\+?\s+tools", "1000+ tools"),
    (r"750\+?\s+tools", "1000+ tools"),
]

def is_false_positive(match, content):
    """Smart context checking to avoid false positives"""
    start = max(0, match.start() - 100)
    end = min(len(content), match.end() + 100)
    context = content[start:end].lower()
    
    # Skip if discussing deprecation itself
    if any(kw in context for kw in ['deprecated', 'old version', 'migration']):
        return True
    
    # Skip technical values (ports, dimensions, etc.)
    if any(kw in context for kw in ['width', 'height', 'port', '":"']):
        return True
    
    return False

def validate_file(filepath):
    """Check one file for issues"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    
    # Check deprecated patterns
    for old_pattern, new_text in DEPRECATED_PATTERNS:
        matches = re.finditer(old_pattern, content)
        for match in matches:
            if is_false_positive(match, content):
                continue
            
            line_num = content[:match.start()].count('\n') + 1
            issues.append({
                'file': filepath,
                'line': line_num,
                'severity': 'HIGH',
                'found': match.group(),
                'suggestion': new_text
            })
    
    return issues

# Scan all docs
all_issues = []
for doc_file in glob.glob(str(DOCS_ROOT / "**/*.md"), recursive=True):
    all_issues.extend(validate_file(doc_file))

for doc_file in glob.glob(str(DOCS_ROOT / "**/*.rst"), recursive=True):
    all_issues.extend(validate_file(doc_file))

# Report
if all_issues:
    print(f"❌ Found {len(all_issues)} issues\n")
    for issue in all_issues:
        print(f"{issue['file']}:{issue['line']} [{issue['severity']}]")
        print(f"  Found: {issue['found']}")
        print(f"  Should be: {issue['suggestion']}\n")
    exit(1)
else:
    print("✅ Documentation validation passed")
    exit(0)
```

### A2. Command Accuracy Check

Test that commands in docs actually work:

```bash
# Extract and test commands
grep -r "^\s*\$\s*" docs/ | while read line; do
    cmd=$(echo "$line" | sed 's/.*\$ //' | cut -d' ' -f1)
    if ! command -v "$cmd" &> /dev/null; then
        echo "❌ Command not found: $cmd in $line"
    fi
done
```

### A3. Link Integrity Check

For RST docs:

```python
def check_rst_links(docs_root):
    """Validate :doc: references"""
    pattern = r':doc:`([^`]+)`'
    
    for rst_file in glob.glob(f"{docs_root}/**/*.rst", recursive=True):
        with open(rst_file) as f:
            content = f.read()
        
        matches = re.finditer(pattern, content)
        for match in matches:
            ref = match.group(1)
            
            # Check if target exists
            possible = [f"{ref}.rst", f"{ref}.md", f"{ref}/index.rst"]
            if not any(Path(docs_root, p).exists() for p in possible):
                print(f"❌ Broken link in {rst_file}: {ref}")
```

### A4. Terminology Consistency

Track variations and standardize:

```python
# Define standard terms
TERMINOLOGY = {
    'api_endpoint': ['endpoint', 'url', 'route', 'path'],
    'tool_count': ['tools', 'resources', 'integrations'],
}

def check_terminology(content):
    """Find inconsistent terminology"""
    for standard, variations in TERMINOLOGY.items():
        counts = {v: content.lower().count(v) for v in variations}
        if len([c for c in counts.values() if c > 0]) > 2:
            return f"Inconsistent terminology: {counts}"
    return None
```

## Phase B: ToolUniverse-Specific Audit

### B1. Circular Navigation Check

**Issue**: Documentation pages that reference each other in loops.

**Check manually**:
```bash
# Find cross-references
grep -r ":doc:\`" docs/*.rst | grep -E "(quickstart|getting_started|installation)"
```

**Checklist**:
- [ ] Is there a clear "Start Here" on `docs/index.rst`?
- [ ] Does navigation follow linear path: index → quickstart → getting_started → guides?
- [ ] No "you should have completed X first" statements that create dependency loops?

**Common patterns to fix**:
- `quickstart.rst` → "See getting_started"
- `getting_started.rst` → "Complete quickstart first"

### B2. Duplicate Content Check

**Common duplicates in ToolUniverse**:
1. Multiple FAQs: `docs/faq.rst` and `docs/help/faq.rst`
2. Getting started: `docs/installation.rst`, `docs/quickstart.rst`, `docs/getting_started.rst`
3. MCP configuration: All files in `docs/guide/building_ai_scientists/`

**Detection**:
```bash
# Find MCP config duplication
rg "MCP.*configuration" docs/ -l | wc -l
rg "pip install tooluniverse" docs/ -l | wc -l
```

**Action**: Consolidate or clearly differentiate

### B3. Tool Count Consistency

**Standard**: Use "1000+ tools" consistently.

**Detection**:
```bash
# Find all tool count mentions
rg "[0-9]+\+?\s+(tools|resources|integrations)" docs/ --no-filename | sort -u
```

**Check**:
- [ ] Are different numbers used (600, 750, 1195)?
- [ ] Is "1000+ tools" used consistently?
- [ ] Exact counts avoided in favor of "1000+"?

### B4. Auto-Generated File Headers

**Auto-generated directories**:
- `docs/tools/*_tools.rst` (from `generate_config_index.py`)
- `docs/api/*.rst` (from `sphinx-apidoc`)

**Required header**:
```rst
.. AUTO-GENERATED - DO NOT EDIT MANUALLY
.. Generated by: docs/generate_config_index.py
.. Last updated: 2024-02-05
.. 
.. To modify, edit source files and regenerate.
```

**Check**:
```bash
head -5 docs/tools/*_tools.rst | grep "AUTO-GENERATED"
```

### B5. CLI Tools Documentation

**Check pyproject.toml for all CLIs**:
```bash
grep -A 20 "\[project.scripts\]" pyproject.toml
```

**Common undocumented**:
- `tooluniverse-expert-feedback`
- `tooluniverse-expert-feedback-web`
- `generate-mcp-tools`

**Action**: Ensure all in `docs/reference/cli_tools.rst`

### B6. Environment Variables

**Discovery**:
```bash
# Find all env vars in code
rg "os\.getenv|os\.environ" src/tooluniverse/ -o | sort -u
rg "TOOLUNIVERSE_[A-Z_]+" src/tooluniverse/ -o | sort -u
```

**Categories to document**:
- Cache: `TOOLUNIVERSE_CACHE_*`
- Logging: `TOOLUNIVERSE_LOG_*`
- LLM: `TOOLUNIVERSE_LLM_*`
- API keys: `*_API_KEY`

**Check**:
- [ ] Does `docs/reference/environment_variables.rst` exist?
- [ ] Are variables categorized?
- [ ] Each has: default, description, example?
- [ ] Is there `.env.template` at project root?

### B7. ToolUniverse-Specific Jargon

**Terms to define on first use**:
- Tool Specification
- EFO ID
- MCP, SMCP
- Compact Mode
- Tool Finder
- AI Scientist

**Check**:
- [ ] Is there `docs/glossary.rst`?
- [ ] Terms defined inline with `:term:` references?
- [ ] Glossary linked from main index?

### B8. CI/CD Documentation Regeneration

**Required in `.github/workflows/deploy-docs.yml`**:
```yaml
- name: Regenerate tool documentation
  run: |
    cd docs
    python generate_config_index.py
    python generate_remote_tools_docs.py
    python generate_tool_reference.py
```

**Check**:
- [ ] CI/CD regenerates docs before build?
- [ ] Regeneration happens BEFORE Sphinx build?
- [ ] `docs/api/` excluded from cache?

## Priority Framework

### Issue Severity

| Severity | Definition | Examples | Timeline |
|----------|------------|----------|----------|
| **CRITICAL** | Blocks release | Broken builds, dangerous instructions | Immediate |
| **HIGH** | Blocks users | Wrong commands, broken setup | Same day |
| **MEDIUM** | Causes confusion | Inconsistent terminology, unclear examples | Same week |
| **LOW** | Reduces quality | Long files, minor formatting | Future task |

### Fix Order

1. Run automated validation → Fix HIGH issues
2. Check circular navigation → Fix CRITICAL loops
3. Verify tool counts → Standardize to "1000+"
4. Check auto-generated headers → Add missing
5. Validate CLI docs → Document all from pyproject.toml
6. Check env vars → Create reference page
7. Review jargon → Create/update glossary
8. Verify CI/CD → Add regeneration steps

## Validation Checklist

Before considering docs "done":

### Accuracy
- [ ] Automated validation passes
- [ ] All commands tested
- [ ] Version numbers current
- [ ] Counts match reality

### Structure (ToolUniverse-specific)
- [ ] No circular navigation
- [ ] Clear "Start Here" entry point
- [ ] Linear learning path
- [ ] Max 2-3 level hierarchy

### Consistency
- [ ] "1000+ tools" everywhere
- [ ] Same terminology throughout
- [ ] Auto-generated files have headers
- [ ] All CLIs documented

### Completeness
- [ ] All features documented
- [ ] All CLIs in pyproject.toml covered
- [ ] All env vars documented
- [ ] Glossary includes all jargon

## Output: Audit Report

```markdown
# Documentation Quality Report

**Date**: [date]
**Scope**: Automated validation + ToolUniverse audit

## Executive Summary
- Files scanned: X
- Issues found: Y (Critical: A, High: B, Medium: C, Low: D)

## Critical Issues
1. **[Issue]** - Location: file:line
   - Problem: [description]
   - Fix: [action]
   - Effort: [time]

## Automated Validation Results
- Deprecated commands: X instances
- Inconsistent counts: Y instances
- Broken links: Z instances

## ToolUniverse-Specific Findings
- Circular navigation: [yes/no]
- Tool count variations: [list]
- Missing CLI docs: [list]
- Auto-generated headers: X missing

## Recommendations
1. Immediate (today): [list]
2. This week: [list]
3. Next sprint: [list]

## Validation Command
Run `python scripts/validate_documentation.py` to verify fixes
```

## CI/CD Integration

Add to `.github/workflows/validate-docs.yml`:

```yaml
name: Validate Documentation
on: [pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run validation
        run: python scripts/validate_documentation.py
      - name: Check auto-generated headers
        run: |
          for f in docs/tools/*_tools.rst; do
            if ! head -1 "$f" | grep -q "AUTO-GENERATED"; then
              echo "Missing header: $f"
              exit 1
            fi
          done
```

## Common Issues Quick Reference

| Issue | Detection | Fix |
|-------|-----------|-----|
| Deprecated command | `rg "old-cmd" docs/` | Replace with `new-cmd` |
| Wrong tool count | `rg "[0-9]+ tools" docs/` | Change to "1000+ tools" |
| Circular nav | Manual trace | Remove back-references |
| Missing header | `head -1 file.rst` | Add AUTO-GENERATED header |
| Undocumented CLI | Check pyproject.toml | Add to cli_tools.rst |
| Missing env var | `rg "os.getenv" src/` | Add to env vars reference |

## Best Practices

1. **Automate first** - Build validation before manual audit
2. **Context matters** - Smart pattern matching avoids false positives
3. **Fix systematically** - Batch similar issues together
4. **Validate continuously** - Add to CI/CD pipeline
5. **ToolUniverse-specific last** - Automated checks catch most issues

## Success Criteria

Documentation quality achieved when:
- ✅ Automated validation reports 0 HIGH issues
- ✅ No circular navigation
- ✅ "1000+ tools" used consistently
- ✅ All auto-generated files have headers
- ✅ All CLIs from pyproject.toml documented
- ✅ All env vars have reference page
- ✅ Glossary covers all technical terms
- ✅ CI/CD validates on every PR
