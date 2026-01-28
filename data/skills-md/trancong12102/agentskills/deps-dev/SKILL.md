---
name: deps-dev
description: Look up the latest version of any package using deps.dev API. Use this skill when checking package versions, updating dependencies, adding new packages to a project, or when the user asks about the current version of a library.
---

# Latest Package Version Lookup

Query the deps.dev API to get the latest stable version of open source packages.

## Supported Ecosystems

| Ecosystem | System ID | Example Package                    |
| --------- | --------- | ---------------------------------- |
| npm       | `npm`     | `express`, `@types/node`           |
| PyPI      | `pypi`    | `requests`, `django`               |
| Go        | `go`      | `github.com/gin-gonic/gin`         |
| Cargo     | `cargo`   | `serde`, `tokio`                   |
| Maven     | `maven`   | `org.springframework:spring-core`  |
| NuGet     | `nuget`   | `Newtonsoft.Json`                  |

## Workflow

Think step-by-step:

1. **Identify the ecosystem** from context:
   - `package.json` or `node_modules` → npm
   - `requirements.txt`, `pyproject.toml`, `setup.py` → pypi
   - `go.mod`, `go.sum` → go
   - `Cargo.toml` → cargo
   - `pom.xml`, `build.gradle` → maven
   - `*.csproj`, `packages.config` → nuget
   - If unclear, ask the user

2. **Run the get-versions script**:

```bash
SCRIPT=scripts/get-versions.py
python3 $SCRIPT <system> <pkg1> [pkg2] ...
```

1. **Report the results** from the JSON output

## Script Usage

**Single package:**

```bash
python3 scripts/get-versions.py npm express
```

**Multiple packages:**

```bash
python3 scripts/get-versions.py npm express lodash @types/node
```

**Different ecosystems:**

```bash
python3 scripts/get-versions.py pypi requests django flask
python3 scripts/get-versions.py go github.com/gin-gonic/gin
python3 scripts/get-versions.py maven org.springframework:spring-core
```

## Output Format

The script outputs JSON with the following structure:

```json
{
  "system": "npm",
  "packages": [
    {
      "package": "express",
      "version": "5.0.0",
      "publishedAt": "2024-09-10T04:40:34Z",
      "isDeprecated": false
    },
    {
      "package": "lodash",
      "version": "4.17.21",
      "publishedAt": "2021-02-20T15:42:16Z",
      "isDeprecated": false
    }
  ]
}
```

**Error response:**

```json
{
  "system": "npm",
  "packages": [
    {
      "package": "nonexistent-pkg",
      "error": "HTTP 404: Not Found"
    }
  ]
}
```

## Error Handling

- **HTTP 404**: Package not found - check spelling and ecosystem
- **Network error**: deps.dev API may be temporarily unavailable
- **No default version**: Script returns the latest available version with a note

## Rules

- Always use the script instead of manual curl commands
- The script handles URL encoding automatically
- Multiple packages are fetched in parallel for efficiency
- Use `isDeprecated` field to warn users about deprecated packages
