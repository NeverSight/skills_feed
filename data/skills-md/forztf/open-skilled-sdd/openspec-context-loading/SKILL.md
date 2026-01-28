---
name: openspec-context-loading
description: Loads project context, lists existing specs and changes, searches capabilities and requirements. Use when user asks about project state, existing specs, active changes, available capabilities, or needs context discovery. Triggers include "openspec context", "what specs exist", "show changes", "list capabilities", "project context", "find specs", "what's in the spec", "show me specs".
---

# Specification Context Loading

Discovers and loads project specifications, active changes, and requirements to provide context.

## Quick Start

Context loading helps answer:
- What specs exist in this project?
- What changes are currently active?
- What requirements are defined?
- What capabilities does the system have?
- Where is a specific feature specified?

**Basic pattern**: Search → Read → Summarize

## Discovery Commands

### List All Specifications

```bash
# Find all spec files
find spec/specs -name "spec.md" -type f

# Find all capability directories
find spec/specs -mindepth 1 -maxdepth 1 -type d

# Show spec tree
tree spec/specs/  # if tree is installed
# or
ls -R spec/specs/
```

**Output format**:
```
spec/specs/
├── authentication/
│   └── spec.md
├── billing/
│   └── spec.md
└── notifications/
    └── spec.md
```

### List Active Changes

```bash
# Show all active changes
find spec/changes -maxdepth 1 -type d -not -path "spec/changes" -not -path "*/archive" | sort

# Show with modification dates
find spec/changes -maxdepth 1 -type d -not -path "spec/changes" -not -path "*/archive" -exec ls -ld {} \;

# Count active changes
find spec/changes -maxdepth 1 -type d -not -path "spec/changes" -not -path "*/archive" | wc -l
```

### List Archived Changes

```bash
# Show all archived changes
ls -1 spec/archive/

# Show with dates
ls -la spec/archive/

# Find recently archived (last 7 days)
find spec/archive/ -maxdepth 1 -type d -mtime -7
```

### Search for Requirements

```bash
# Find all requirements
grep -r "### Requirement:" spec/specs/

# Find requirements in specific capability
grep "### Requirement:" spec/specs/authentication/spec.md

# List unique requirement names
grep -h "### Requirement:" spec/specs/**/*.md | sed 's/### Requirement: //' | sort
```

### Search for Scenarios

```bash
# Find all scenarios
grep -r "#### Scenario:" spec/specs/

# Count scenarios per spec
for spec in spec/specs/**/spec.md; do
    count=$(grep -c "#### Scenario:" "$spec")
    echo "$spec: $count scenarios"
done
```

### Search by Keyword

```bash
# Find specs mentioning "authentication"
grep -r -i "authentication" spec/specs/

# Find requirements about "password"
grep -B 1 -A 5 -i "password" spec/specs/**/*.md | grep -A 5 "### Requirement:"

# Find scenarios about "error"
grep -B 1 -A 10 -i "error" spec/specs/**/*.md | grep -A 10 "#### Scenario:"
```

## Common Queries

### Query 1: "What specs exist?"

```bash
# List all capabilities
find spec/specs -mindepth 1 -maxdepth 1 -type d -exec basename {} \;

# Count requirements per capability
for cap in spec/specs/*/; do
    name=$(basename "$cap")
    count=$(grep -c "### Requirement:" "$cap/spec.md" 2>/dev/null || echo "0")
    echo "$name: $count requirements"
done
```

**Response format**:
```markdown
## Existing Specifications

The project has specifications for the following capabilities:

- **authentication**: 8 requirements
- **billing**: 12 requirements
- **notifications**: 5 requirements

Total: 3 capabilities, 25 requirements
```

### Query 2: "What changes are active?"

```bash
# List with proposal summaries
for change in spec/changes/*/; do
    if [ "$change" != "spec/changes/archive/" ]; then
        id=$(basename "$change")
        echo "=== $id ==="
        head -n 20 "$change/proposal.md" | grep -A 3 "## Why"
    fi
done
```

**Response format**:
```markdown
## Active Changes

Currently active changes:

### add-user-auth
**Why**: Users need secure authentication...

### update-billing-api
**Why**: Payment processing requires v2 API...

Total: 2 active changes
```

### Query 3: "Show me the authentication spec"

```bash
# Read full spec
cat spec/specs/authentication/spec.md

# Or show summary
echo "Requirements:"
grep "### Requirement:" spec/specs/authentication/spec.md

echo "\nScenarios:"
grep "#### Scenario:" spec/specs/authentication/spec.md
```

**Response format**:
```markdown
## Authentication Specification

(Include full content of spec.md)

Summary:
- 8 requirements
- 16 scenarios
- Last modified: [date from git log]
```

### Query 4: "Find specs about password"

```bash
# Search for keyword
grep -r -i "password" spec/specs/ -A 5

# Show which specs mention it
grep -r -i "password" spec/specs/ -l
```

**Response format**:
```markdown
## Specs Mentioning "Password"

Found in:
- spec/specs/authentication/spec.md (3 requirements)
- spec/specs/security/spec.md (1 requirement)

Relevant requirements:
### Requirement: Password Validation
### Requirement: Password Reset
### Requirement: Password Strength
```

### Query 5: "What's in change X?"

```bash
# Show full change context
CHANGE_ID="add-user-auth"

echo "=== Proposal ==="
cat spec/changes/$CHANGE_ID/proposal.md

echo "\n=== Tasks ==="
cat spec/changes/$CHANGE_ID/tasks.md

echo "\n=== Spec Deltas ==="
find spec/changes/$CHANGE_ID/specs -name "*.md" -exec echo "File: {}" \; -exec cat {} \;
```

## Dashboard View

Create a comprehensive project overview:

```bash
#!/bin/bash
# Project specification dashboard

echo "===  Specification Dashboard ==="
echo ""

# Capabilities
echo "## Capabilities"
CAPS=$(find spec/specs -mindepth 1 -maxdepth 1 -type d | wc -l)
echo "Total capabilities: $CAPS"
for cap in spec/specs/*/; do
    name=$(basename "$cap")
    reqs=$(grep -c "### Requirement:" "$cap/spec.md" 2>/dev/null || echo "0")
    echo "  - $name: $reqs requirements"
done
echo ""

# Requirements
echo "## Requirements"
TOTAL_REQS=$(grep -r "### Requirement:" spec/specs/ | wc -l)
TOTAL_SCENARIOS=$(grep -r "#### Scenario:" spec/specs/ | wc -l)
echo "Total requirements: $TOTAL_REQS"
echo "Total scenarios: $TOTAL_SCENARIOS"
echo "Avg scenarios per requirement: $(echo "scale=1; $TOTAL_SCENARIOS/$TOTAL_REQS" | bc)"
echo ""

# Changes
echo "## Changes"
ACTIVE=$(find spec/changes -maxdepth 1 -type d -not -path "spec/changes" -not -path "*/archive" | wc -l)
ARCHIVED=$(ls -1 spec/archive/ | wc -l)
echo "Active changes: $ACTIVE"
echo "Archived changes: $ARCHIVED"
echo ""

# Recent activity
echo "## Recent Activity"
echo "Recently modified specs:"
find spec/specs -name "spec.md" -type f -exec ls -lt {} \; | head -5
```

**Response format**:
```markdown
# Specification Dashboard

## Capabilities
Total capabilities: 3
  - authentication: 8 requirements
  - billing: 12 requirements
  - notifications: 5 requirements

## Requirements
Total requirements: 25
Total scenarios: 52
Avg scenarios per requirement: 2.1

## Changes
Active changes: 2
Archived changes: 15

## Recent Activity
Recently modified specs:
- spec/specs/billing/spec.md (2 days ago)
- spec/specs/authentication/spec.md (1 week ago)
```

## Advanced Queries

### Find Related Requirements

```bash
# Find requirements that mention another requirement
grep -r "User Login" spec/specs/ -A 10 | grep "### Requirement:"

# Find cross-references
grep -r "See Requirement:" spec/specs/
```

### Analyze Coverage

```bash
# Find requirements without scenarios
for spec in spec/specs/**/spec.md; do
    awk '/### Requirement:/ {req=$0; getline; if ($0 !~ /#### Scenario:/) print req}' "$spec"
done

# Find scenarios without proper Given/When/Then
grep -A 5 "#### Scenario:" spec/specs/**/*.md | grep -v "GIVEN\|WHEN\|THEN"
```

### Compare Active vs Archive

```bash
# Show evolution over time
echo "Archive history:"
ls -1 spec/archive/ | head -10

echo "Recent archives (last 30 days):"
find spec/archive/ -maxdepth 1 -type d -mtime -30 -exec basename {} \;
```

## Search Patterns

### Pattern 1: Capability Discovery

User asks: "What can the system do?"

```bash
# List capabilities
find spec/specs -mindepth 1 -maxdepth 1 -type d -exec basename {} \;

# Show high-level requirements
for cap in spec/specs/*/; do
    echo "=== $(basename $cap) ==="
    grep "### Requirement:" "$cap/spec.md" | head -3
done
```

### Pattern 2: Feature Search

User asks: "Is there a spec for password reset?"

```bash
# Search for keyword
grep -r -i "password reset" spec/specs/ -B 1 -A 10

# If found, show full requirement
grep -B 1 -A 20 "Requirement:.*Password Reset" spec/specs/**/*.md
```

### Pattern 3: Change Tracking

User asks: "What's being worked on?"

```bash
# Show active changes with status
for change in spec/changes/*/; do
    if [ "$change" != "spec/changes/archive/" ]; then
        id=$(basename "$change")
        echo "$id:"
        test -f "$change/IMPLEMENTED" && echo "  Status: Implemented" || echo "  Status: In Progress"
        echo "  Tasks: $(grep -c "^[0-9]\+\." "$change/tasks.md")"
    fi
done
```

## Best Practices

### Pattern 1: Provide Context Before Details

**Good flow**:
```markdown
1. Show dashboard (high-level overview)
2. User asks about specific capability
3. Show that capability's requirements
4. User asks about specific requirement
5. Show full requirement with scenarios
```

### Pattern 2: Use Grep Efficiently

```bash
# Combine filters for precision
grep -r "### Requirement:" spec/specs/ | grep -i "auth"

# Use context flags for readability
grep -B 2 -A 10 "#### Scenario:" spec/specs/authentication/spec.md
```

### Pattern 3: Aggregate Information

Don't just dump file contents. Summarize:

```markdown
**Bad**: (dump entire spec file)

**Good**:
"The authentication spec has 8 requirements covering:
- User login
- Password management
- Session handling
- Multi-factor authentication

Would you like details on any specific requirement?"
```

## Anti-Patterns to Avoid

**Don't**:
- Read entire spec files without user request
- List every single requirement by default
- Show raw grep output without formatting
- Assume user knows capability names

**Do**:
- Start with high-level overview
- Ask which area user wants to explore
- Format output clearly
- Provide navigation hints

## Reference Materials

- [SEARCH_PATTERNS.md](reference/SEARCH_PATTERNS.md) - Advanced grep/find patterns

---

**Token budget**: This SKILL.md is approximately 460 lines, under the 500-line recommended limit.
