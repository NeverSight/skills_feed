---
name: project-onboarding
description: Onboard new projects with standardized configuration and documentation
---


# Project Onboarding Skill

> Quickly onboard a new project into the agentic workspace with RAG collections, routing rules, and baseline knowledge.

## Overview

When starting work on a new project, this skill provides a systematic approach to:
- Create project-specific RAG collections
- Register semantic routing rules
- Ingest existing documentation as baseline knowledge
- Set up credentials and configuration
- Validate the setup

## Prerequisites

- Workspace with RAG server running
- Router server running
- Access to the project's source code or documentation

## Onboarding Steps

### Step 1: Gather Project Information

Before onboarding, collect:

```yaml
project:
  name: "project-slug"           # Lowercase, hyphenated
  display_name: "Project Name"   # Human-readable
  code_path: "/path/to/code"     # Absolute path to source
  description: "Brief description of the project"

  # Optional
  tech_stack:
    - python
    - fastapi
    - postgresql

  docs_paths:
    - README.md
    - docs/
    - ARCHITECTURE.md
```

### Step 2: Create RAG Collections

Create isolated collections for different content types:

```python
# Collection naming convention: {project}_{content_type}
collections = [
    f"{project_name}_docs",      # Documentation, READMEs
    f"{project_name}_code",      # Code snippets, patterns
    f"{project_name}_decisions", # ADRs, architectural decisions
    f"{project_name}_research",  # Research findings, notes
]

# Create via RAG server
for collection in collections:
    await rag.create_collection(collection)
```

**Recommended collection structure:**

| Collection | Content | Metadata |
|------------|---------|----------|
| `{project}_docs` | README, guides, API docs | `type: doc, source: file` |
| `{project}_code` | Reusable patterns, examples | `type: code, language: python` |
| `{project}_decisions` | ADRs, design docs | `type: decision, status: accepted` |
| `{project}_research` | Research notes, findings | `type: research, topic: x` |

### Step 3: Ingest Baseline Documentation

```bash
#!/bin/bash
# scripts/onboard-docs.sh

PROJECT=$1
CODE_PATH=$2

# Ingest README
if [ -f "$CODE_PATH/README.md" ]; then
    /ingest --collection "${PROJECT}_docs" \
            --source "readme" \
            --file "$CODE_PATH/README.md"
fi

# Ingest docs directory
if [ -d "$CODE_PATH/docs" ]; then
    find "$CODE_PATH/docs" -name "*.md" -exec \
        /ingest --collection "${PROJECT}_docs" \
                --source "docs" \
                --file {} \;
fi

# Ingest architecture docs
for doc in ARCHITECTURE.md DESIGN.md CONTRIBUTING.md; do
    if [ -f "$CODE_PATH/$doc" ]; then
        /ingest --collection "${PROJECT}_decisions" \
                --source "architecture" \
                --file "$CODE_PATH/$doc"
    fi
done
```

### Step 4: Register Routing Rules

Add project-specific routing so queries get directed appropriately:

```yaml
# routing/routes/project-{name}.yaml
routes:
  - name: "{project}_code_search"
    utterances:
      - "find code in {project}"
      - "search {project} for"
      - "how does {project} implement"
      - "{project} code pattern"
    action:
      type: rag_search
      collection: "{project}_code"

  - name: "{project}_docs_search"
    utterances:
      - "{project} documentation"
      - "how to use {project}"
      - "{project} setup"
      - "{project} guide"
    action:
      type: rag_search
      collection: "{project}_docs"

  - name: "{project}_decisions"
    utterances:
      - "why did {project}"
      - "{project} architecture"
      - "{project} design decision"
    action:
      type: rag_search
      collection: "{project}_decisions"
```

### Step 5: Create Project Configuration

```yaml
# config/projects/{project}.yaml
project:
  name: "{project}"
  display_name: "{Project Display Name}"
  code_path: "/path/to/code"

collections:
  docs: "{project}_docs"
  code: "{project}_code"
  decisions: "{project}_decisions"
  research: "{project}_research"

credentials:
  # Reference to .env variables
  api_key: "{PROJECT}_API_KEY"
  database_url: "{PROJECT}_DATABASE_URL"

defaults:
  search_collection: "{project}_docs"
  search_results: 5
```

### Step 6: Create Code Symlink

```bash
# Link project code into workspace
ln -sf /path/to/actual/code ./code/{project}
```

### Step 7: Validate Setup

```python
#!/usr/bin/env python3
"""Validate project onboarding."""

import asyncio
from pathlib import Path

async def validate_onboarding(project: str):
    errors = []

    # Check collections exist
    collections = await rag.list_collections()
    expected = [f"{project}_docs", f"{project}_code",
                f"{project}_decisions", f"{project}_research"]

    for coll in expected:
        if coll not in [c["name"] for c in collections]:
            errors.append(f"Missing collection: {coll}")

    # Check config exists
    config_path = Path(f"config/projects/{project}.yaml")
    if not config_path.exists():
        errors.append(f"Missing config: {config_path}")

    # Check code symlink
    code_path = Path(f"code/{project}")
    if not code_path.exists():
        errors.append(f"Missing code symlink: {code_path}")

    # Check routing rules
    route_path = Path(f"routing/routes/project-{project}.yaml")
    if not route_path.exists():
        errors.append(f"Missing routes: {route_path}")

    # Test search works
    try:
        results = await rag.search(
            query="project overview",
            collection=f"{project}_docs",
            n_results=1
        )
        if not results["results"]:
            errors.append("No documents in docs collection")
    except Exception as e:
        errors.append(f"Search failed: {e}")

    return errors

if __name__ == "__main__":
    import sys
    project = sys.argv[1]
    errors = asyncio.run(validate_onboarding(project))

    if errors:
        print("❌ Onboarding validation failed:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print(f"✅ Project '{project}' onboarded successfully!")
```

## Quick Onboarding Script

```bash
#!/bin/bash
# scripts/onboard-project.sh

set -e

PROJECT=$1
CODE_PATH=$2
DISPLAY_NAME=${3:-$PROJECT}

if [ -z "$PROJECT" ] || [ -z "$CODE_PATH" ]; then
    echo "Usage: onboard-project.sh <project-slug> <code-path> [display-name]"
    exit 1
fi

echo "🚀 Onboarding project: $PROJECT"

# Step 1: Create collections
echo "📦 Creating RAG collections..."
for type in docs code decisions research; do
    curl -X POST "http://localhost:8100/create_collection" \
        -d "{\"name\": \"${PROJECT}_${type}\"}"
done

# Step 2: Create config
echo "⚙️ Creating project config..."
cat > "config/projects/${PROJECT}.yaml" << EOF
project:
  name: "${PROJECT}"
  display_name: "${DISPLAY_NAME}"
  code_path: "${CODE_PATH}"

collections:
  docs: "${PROJECT}_docs"
  code: "${PROJECT}_code"
  decisions: "${PROJECT}_decisions"
  research: "${PROJECT}_research"
EOF

# Step 3: Create code symlink
echo "🔗 Creating code symlink..."
mkdir -p code
ln -sf "$CODE_PATH" "code/${PROJECT}"

# Step 4: Ingest docs
echo "📚 Ingesting documentation..."
./scripts/onboard-docs.sh "$PROJECT" "$CODE_PATH"

# Step 5: Create routing rules
echo "🔀 Creating routing rules..."
cat > "routing/routes/project-${PROJECT}.yaml" << EOF
routes:
  - name: "${PROJECT}_search"
    utterances:
      - "${PROJECT}"
      - "search ${PROJECT}"
      - "${PROJECT} code"
      - "${PROJECT} docs"
    action:
      type: rag_search
      collection: "${PROJECT}_docs"
EOF

# Step 6: Validate
echo "✅ Validating..."
python scripts/validate-onboarding.py "$PROJECT"

echo "🎉 Project '$PROJECT' onboarded successfully!"
```

## Usage Examples

```bash
# Onboard a Python project
./scripts/onboard-project.sh my-api ~/projects/my-api "My API Service"

# Onboard with just slug and path
./scripts/onboard-project.sh client-portal ~/work/client-portal

# Validate existing project
python scripts/validate-onboarding.py my-api
```

## Post-Onboarding

After onboarding:

1. **Ingest more content** as you work:
   ```
   /ingest --collection my-api_research --content "Found that..."
   ```

2. **Refine routing rules** based on actual usage patterns

3. **Add project-specific workflows** in `workflows/definitions/`

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Collections not created | Check RAG server is running |
| Search returns nothing | Verify documents were ingested |
| Routing not working | Reload router embeddings |
| Code symlink broken | Check absolute path is correct |

## Refinement Notes

> Add notes here as you onboard projects and discover improvements.

- [ ] Initial implementation
- [ ] Tested with real project
- [ ] Automated script working
- [ ] Routing integration verified
