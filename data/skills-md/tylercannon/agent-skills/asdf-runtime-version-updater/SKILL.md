---
name: asdf-runtime-version-updater
description: "Update language runtime versions in .tool-versions files (asdf) and propagate changes to Dockerfiles, GitHub Actions workflows, and other version-referencing files. Use when: (1) updating a project's language runtime version(s), (2) synchronizing versions across .tool-versions, Dockerfiles, and CI/CD configs, or (3) migrating to a new runtime version."
---

# ASDF Runtime Version Updater

Update language runtime versions consistently across your project.

## Workflow

1. **Parse current versions** - Read `.tool-versions` to get current runtime versions
2. **Find latest version** - Run `asdf latest <runtime>` to get the latest available version
3. **Update `.tool-versions`** - Update the version in `.tool-versions`
4. **Install new version** - Run `asdf install` to install the runtime
5. **Find version references** - Search for files referencing the old version
6. **Update all references** - Update versions consistently across all files
7. **Verify project** - Install deps, build, format check, and run tests

## Version Lookup

```bash
# Get latest version for a runtime
asdf latest nodejs      # e.g., 22.13.1
asdf latest python      # e.g., 3.13.2
asdf latest ruby        # e.g., 3.4.2
asdf latest elixir      # e.g., 1.19.5-otp-28
asdf latest erlang      # e.g., 28.3.1
```

## File Patterns

### `.tool-versions` Format

```
nodejs 22.13.1
python 3.13.2
ruby 3.4.2
elixir 1.19.5-otp-28
erlang 28.3.1
```

### Dockerfile Patterns

```dockerfile
# Node.js
FROM node:22.13.1-alpine
FROM node:22-alpine

# Python
FROM python:3.13.2-slim
FROM python:3.13-slim

# Ruby
FROM ruby:3.4.2-alpine

# Elixir (often uses erlang base)
FROM elixir:1.19.5-otp-28
FROM hexpm/elixir:1.19.5-erlang-28.3.1-alpine-3.21.0
```

### Dockerfile ARG Patterns

Some Dockerfiles use `ARG` for version configuration:

```dockerfile
ARG ELIXIR_VERSION=1.19.5
ARG OTP_VERSION=28.3.1
ARG DEBIAN_VERSION=trixie-20260112-slim

ARG BUILDER_IMAGE="docker.io/hexpm/elixir:${ELIXIR_VERSION}-erlang-${OTP_VERSION}-debian-${DEBIAN_VERSION}"
```

Search for these patterns:
```bash
grep -E "^ARG\s+(ELIXIR|OTP|ERLANG|NODE|PYTHON|RUBY)_VERSION=" Dockerfile*
```

### GitHub Workflows (`.github/workflows/*.yml`)

```yaml
# Node.js
- uses: actions/setup-node@v4
  with:
    node-version: '22.13.1'
    node-version-file: '.tool-versions'

# Python
- uses: actions/setup-python@v5
  with:
    python-version: '3.13.2'

# Ruby
- uses: ruby/setup-ruby@v1
  with:
    ruby-version: '3.4.2'

# Elixir
- uses: erlef/setup-beam@v1
  with:
    elixir-version: '1.19.5'
    otp-version: '28.0'
```

### GitHub Workflow Job Containers

Jobs can also specify container images directly:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    container:
      image: hexpm/elixir:1.19.5-erlang-28.3.1-alpine-3.23.3
    
  build:
    runs-on: ubuntu-latest
    container: node:22.13.1-alpine
```

Search for these patterns:
```bash
grep -rE "^\s*(image:|container:)" .github/workflows/
```

### Other Version Files

| Runtime | Files |
|---------|-------|
| Node.js | `.nvmrc`, `.node-version`, `package.json` (engines, `@types/node`) |
| Python | `.python-version`, `pyproject.toml`, `setup.py` |
| Ruby | `.ruby-version`, `Gemfile` |

## Search Patterns

Use these patterns to find version references:

```bash
# Find version references in project
grep -r "22.13.1" .             # Specific version
grep -rE "node[:-]?22" .         # Node.js major version patterns
grep -rE "python[:-]?3\.13" .    # Python minor version patterns
```

## Example Update

**Before** (`.tool-versions`):
```
elixir 1.18.0-otp-27
erlang 27.2.4
```

**Steps**:
```bash
# Check latest versions
asdf latest elixir  # 1.19.5-otp-28
asdf latest erlang  # 28.3.1

# Update .tool-versions, then:
asdf install
```

**After** (`.tool-versions`):
```
elixir 1.19.5-otp-28
erlang 28.3.1
```

Then update all other files (Dockerfile, GitHub workflows, etc.) to match.

## Verification

After updating versions, verify the project still works:

### Elixir/Phoenix

```bash
mix deps.clean --all
mix deps.get
mix compile --warnings-as-errors
mix format --check-formatted
mix test
```

### Node.js

```bash
npm install
npm run build
npm run lint
npm test
```

### Python

```bash
pip install -e ".[dev]"
python -m build
ruff check .
pytest
```

### Ruby

```bash
bundle install
bundle exec rake build
bundle exec rubocop
bundle exec rspec
```

### Go

```bash
go mod download
go build ./...
go fmt ./...
go test ./...
```

## Resources

For detailed patterns per runtime, see [runtime-patterns.md](references/runtime-patterns.md).
