---
name: querying-yaml
description: Extracts specific fields from YAML files efficiently using yq instead of reading entire files, saving 80-95% context. Use this skill when querying YAML files, filtering/transforming configuration data, or getting specific field(s) from large YAML files like docker-compose.yml or GitHub Actions workflows
---

# yq: YAML Query and Extraction Tool

**Always invoke yq skill to extract YAML fields - do not execute bash commands directly.**

Use yq to extract specific fields from YAML files without reading entire file contents, saving 80-95% context usage.

## When to Use yq

**Use yq when:**
- Need specific field(s) from structured YAML file
- File is large (>50 lines) and only need subset of data
- Querying nested structures in YAML
- Filtering/transforming YAML data
- Working with docker-compose.yml, GitHub Actions workflows, K8s configs

**Just use Read when:**
- File is small (<50 lines)
- Need to understand overall structure
- Making edits (need full context anyway)

## Tool Selection

**JSON files** → Use `jq`
- Common: package.json, tsconfig.json, lock files, API responses

**YAML files** → Use `yq`
- Common: docker-compose.yml, GitHub Actions, CI/CD configs

Both tools extract exactly what you need in one command - massive context savings.

## Default Strategy

**Invoke yq skill** for extracting specific fields from YAML files efficiently. Use instead of reading entire files to save 80-95% context.

Common workflow: fd skill → yq skill → other skills (fzf, sd, bat) for extraction and transformation.

## Pipeline Combinations
- **yq | fzf**: Interactive selection from YAML data
- **yq | sd**: Transform YAML to other formats
- **yq | bat**: View extracted YAML with syntax highlighting

## Skill Combinations

### For Discovery Phase
- **fd → yq**: Find YAML config files and extract specific fields
- **ripgrep → yq**: Find YAML usage patterns and extract values
- **extracting-code-structure → yq**: Understand API structures before extraction

### For Analysis Phase
- **yq → fzf**: Interactive selection from structured data
- **yq → bat**: View extracted data with syntax highlighting
- **yq → tokei**: Extract statistics from YAML output

### For Refactoring Phase
- **yq → sd**: Transform YAML data to other formats
- **yq → jq**: Convert YAML to JSON for different tools
- **yq → xargs**: Use extracted values as command arguments

### Multi-Skill Workflows
- **yq → jq → sd → bat**: YAML to JSON transformation with preview
- **yq → fzf → xargs**: Interactive selection and execution based on YAML data
- **fd → yq → ripgrep**: Find config files, extract values, search usage
- **docker-compose workflow**: yq → fzf → nc (extract ports, test connectivity)

### Common Integration Examples
```bash
# Get service ports and test connectivity
yq '.services.*.ports' docker-compose.yml | sd - '[^0-9]' '' | fzf | xargs -I {} nc -zv localhost {}

# Extract and filter environment variables
yq '.services.*.environment' docker-compose.yml | sd '\s*-\s*' '' | fzf
```

### Note: Choosing Between jq and yq
- **JSON files** (package.json, tsconfig.json): Use `jq`
- **YAML files** (docker-compose.yml, GitHub Actions): Use `yq`

## Quick Examples

```bash
# Get service ports from docker-compose
yq '.services.*.ports' docker-compose.yml

# Get specific service configuration
yq '.services.web.image' docker-compose.yml

# List all service names
yq '.services | keys[]' docker-compose.yml
```

## Detailed Reference

For comprehensive yq patterns, syntax, and examples, load [yq guide](./reference/yq-guide.md) when needing:
- Complex YAML structure navigation
- Array manipulation and filtering
- Data transformation patterns
- Docker Compose and Kubernetes examples
- Integration with other tools
- Core patterns (80% of use cases)
- Real-world workflows (Docker Compose, GitHub Actions, Kubernetes)
- Advanced patterns and edge case handling
- Output formats and pipe composition
- Best practices and integration with other tools
