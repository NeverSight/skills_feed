---
name: 4d-add-dependency
description: Add dependencies to a 4D project. Use when the user wants to add a component, library, or dependency to their 4D project. Supports GitHub repos (owner/repo format), GitHub URLs (with automatic tag extraction from release URLs), and local folder paths. Handles dependencies.json and environment4d.json configuration.
license: Apache 2.0
---

# 4D Add Dependency

Add dependencies to a 4D project by updating the appropriate configuration files.

## Usage

Run the script to add a dependency:

```bash
python3 scripts/add_dependency.py <repo> [options]
```

### Arguments

- `repo`: GitHub repo (`owner/repo`), GitHub URL, or local path

### Options

- `--name NAME`: Override dependency name (default: derived from repo)
- `--tag TAG`: Exact version tag (e.g., `1.0.0`)
- `--version VERSION`: Semantic version (e.g., `latest`, `1.1.0`)
- `--project PATH`: Path to 4D project root

## Examples

```bash
# GitHub dependency with tag
python3 scripts/add_dependency.py mesopelagique/JSONRPC --tag 1.0.0

# GitHub URL (no version)
python3 scripts/add_dependency.py https://github.com/mesopelagique/SemVer

# GitHub release URL (tag extracted automatically)
python3 scripts/add_dependency.py https://github.com/mesopelagique/SemVer/releases/tag/0.2.0

# Local sibling folder
python3 scripts/add_dependency.py ../MyComponent

# Local folder with custom name
python3 scripts/add_dependency.py /path/to/component --name MyComponent
```

## File Formats

### dependencies.json

Located at `Project/Sources/dependencies.json`:

```json
{
    "version": 2130,
    "dependencies": {
        "LocalComponent": {},
        "GitHubComponent": {
            "github": "owner/repo",
            "tag": "1.0.0"
        }
    }
}
```

### environment4d.json

Required for non-sibling local dependencies. Found by walking up from project root, or created in parent directory:

```json
{
    "dependencies": {
        "ComponentName": "file:///path/to/component.4dbase"
    }
}
```

## Behavior

1. **GitHub repos/URLs**: Add entry with `github` field and optional `tag`/`version`
   - Release URLs (`/releases/tag/x.x.x`) automatically extract the tag
2. **Local sibling folders**: Add empty entry `{}` to dependencies.json only
3. **Local non-sibling folders**: Also add `file://` path to environment4d.json
