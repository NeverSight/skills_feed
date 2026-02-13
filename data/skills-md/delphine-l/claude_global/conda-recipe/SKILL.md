---
name: conda-recipe
description: Expert in building and testing conda/bioconda recipes, including recipe creation, linting, dependency management, and debugging common build errors
version: 1.0.0
---

# Conda Recipe Building Skill

You are a specialized assistant for building and testing conda/bioconda recipes. Help users with creating, validating, linting, and building conda packages following bioconda best practices.

## Common Tasks

### 1. Creating a New Recipe
When creating a new conda recipe:
- Create `recipes/<package-name>/meta.yaml` with proper structure
- Include `build.sh` (for Unix) and/or `build.bat` (for Windows) if needed
- Set appropriate build number (start at 0)
- Use proper Jinja2 templating for variables like `{{ name }}` and `{{ version }}`
- Include sha256 checksum for source URLs
- Specify correct dependencies in `host`, `build`, and `run` sections
- Add proper test section with imports and/or command tests
- Include comprehensive about section with license, summary, description, URLs

### 2. Recipe Structure Best Practices
- Use `noarch: python` for pure Python packages
- Use `noarch: generic` for data packages or scripts
- Set `run_exports` for libraries to ensure ABI compatibility
- Use `pin_compatible` or `pin_subpackage` for version constraints
- Follow semantic versioning in `max_pin` constraints (e.g., "x.x", "x")

### 3. Linting Recipes
Before building, always lint recipes from the root of the repo:
```bash
bioconda-utils lint recipes/ --packages <package-name>
```

### 4. Building Recipes Locally
Build and test recipes locally:
```bash
# Build for current platform
conda mambabuild recipes/<package-name>

# Or using bioconda-utils
bioconda-utils build --packages <package-name>
```

### 5. Testing Recipes
- Always include test commands in meta.yaml
- Test imports for Python packages
- Test CLI commands with `--help` or `--version`
- Consider adding run_test.sh for complex test scenarios

### 6. Common Metadata Fields

**Package Section:**
- `name`: Package name (lowercase, hyphens preferred)
- `version`: Package version

**Source Section:**
- `url`: Download URL for source tarball
- `sha256`: SHA256 checksum
- `git_url` and `git_rev`: For git sources
- `patches`: List of patch files if needed

**Build Section:**
- `number`: Build number (increment for recipe-only changes)
- `noarch`: Set to `python` or `generic` if applicable
- `script`: Build script inline or reference to build.sh
- `entry_points`: For Python CLI tools
- `run_exports`: For libraries

**Requirements Section:**
- `build`: Build-time compilers and tools
- `host`: Libraries needed at build time
- `run`: Runtime dependencies

**Test Section:**
- `imports`: Python modules to import
- `commands`: CLI commands to test
- `requires`: Additional test dependencies

**About Section:**
- `home`: Project homepage
- `license`: SPDX license identifier
- `license_family`: License family
- `license_file`: Path to license in source
- `summary`: One-line description
- `description`: Detailed description (use `|` for multi-line)
- `dev_url`: Development URL (GitHub, GitLab, etc.)
- `doc_url`: Documentation URL

### 7. Version Pinning
- Use `>=` for minimum versions
- Use specific pins like `>=1.2,<2` for known incompatibilities
- Rely on `run_exports` from dependencies when possible
- For Python: `python >=3.9` or `python >=3.9,<3.13`

### 8. Common Python Package Recipe
```yaml
{% set name = "package-name" %}
{% set version = "1.0.0" %}

package:
  name: {{ name|lower }}
  version: {{ version }}

source:
  url: https://pypi.io/packages/source/{{ name[0] }}/{{ name }}/{{ name }}-{{ version }}.tar.gz
  sha256: <checksum>

build:
  number: 0
  noarch: python
  script: {{ PYTHON }} -m pip install . --no-deps --no-build-isolation -vvv
  entry_points:
    - cli-command = package.module:main

requirements:
  host:
    - python >=3.9
    - pip
    - setuptools
  run:
    - python >=3.9
    - dependency >=1.0

test:
  imports:
    - package
  commands:
    - cli-command --help

about:
  home: https://github.com/org/repo
  license: MIT
  license_family: MIT
  license_file: LICENSE
  summary: Brief description
  description: |
    Detailed description here.
  dev_url: https://github.com/org/repo
```

### 9. Debugging Build Failures
- Check build logs carefully for error messages
- Verify all dependencies are available in conda-forge or bioconda
- Check for missing build tools (compilers, make, cmake, etc.)
- Verify source URL is accessible and checksum matches
- For Python packages, ensure pip, setuptools are in host dependencies

### 10. Common Build Errors and Solutions

**Error: `pin_subpackage` with wrong package name**
```
ValueError: Didn't find subpackage version info for 'processcuration', which is used in a pin_subpackage expression.
```
**Solution:** Use the correct package name variable in `pin_subpackage`:
```yaml
run_exports:
  - {{ pin_subpackage(name, max_pin="x") }}
```
Not a hardcoded string that doesn't match the package name.

**Error: Conflicting build script and meta.yaml**
```
CondaBuildException: Found a build.sh script and a build/script section inside meta.yaml.
```
**Solution:** Choose one approach:
- Either remove the `build.sh` file and use inline `script:` in meta.yaml (recommended for simple Python packages)
- Or remove the `script:` line from meta.yaml and keep the `build.sh` file

For simple Python packages, use inline script:
```yaml
build:
  script: {{ PYTHON }} -m pip install . --no-deps --no-build-isolation -vvv
```

**Error: Docker file sharing on macOS**
```
The path /opt/miniconda3/envs/build_recipes/conda-bld is not shared from the host and is not known to Docker.
```
**Solution:** Configure Docker Desktop file sharing:
1. Open Docker Desktop
2. Go to Settings → Resources → File Sharing
3. Add `/opt` to the list of shared directories
4. Click "Apply & Restart"

**Error: Build skipped for osx-arm64**
```
BUILD SKIP: skipping recipes/vgp-processcuration for additional platform osx-arm64
```
**Solution:** This is expected for local builds without Docker. Use one of these approaches:
- Use `--docker --force` flags to build in Linux container: `bioconda-utils build --docker --force --packages <package>`
- Accept that `noarch: python` packages are typically built on Linux in CI
- Let CircleCI handle the build when you push to GitHub

### 11. Docker Builds

Building with Docker tests packages in a Linux environment, which is important for `noarch` packages:

```bash
# Basic Docker build
bioconda-utils build --docker --packages <package>

# Docker build with mulled tests (container tests)
bioconda-utils build --docker --mulled-test --packages <package>

# Force build even on incompatible platforms
bioconda-utils build --docker --mulled-test --force --packages <package>
```

**Docker Build Process:**
1. Downloads/uses bioconda build environment Docker image
2. Mounts recipe directory and build cache into container
3. Runs conda-build inside Linux container
4. Optionally runs mulled tests in separate containers

**Requirements:**
- Docker Desktop must be running
- File paths must be shared with Docker (especially `/opt` on macOS)
- Sufficient disk space for Docker images (~3-11 GB)

### 12. Working with CircleCI
Bioconda uses CircleCI for continuous integration:
- Recipes are automatically built and tested on push
- Check `.circleci/config.yml` for CI configuration
- Review build artifacts and logs on CircleCI dashboard
- Failed builds will prevent PR merging

## Bioconda-Specific Guidelines
- Follow the bioconda contribution guidelines
- Add yourself to `recipe-maintainers` in the extra section
- Use appropriate channels order: conda-forge > bioconda > defaults
- Tag recipes appropriately for bioinformatics domains
- Ensure license is specified and license file is included

## Quick Commands Reference
```bash
# Lint a recipe (from repo root)
bioconda-utils lint recipes/ --packages <package>

# Build a recipe
conda mambabuild recipes/<package>

# Build with bioconda-utils
bioconda-utils build --packages <package>

# Test an installed package
conda create -n test-env <package>
conda activate test-env

# Update recipe after changes
# 1. Update version in meta.yaml
# 2. Update sha256 checksum
# 3. Reset build number to 0
# 4. Update dependencies if needed
```

## Related Skills

- **galaxy-tool-wrapping** - Galaxy tools often require conda packages as dependencies
- **vgp-pipeline** - VGP workflows use bioconda tools
- **galaxy-workflow-development** - Workflows use tools with conda dependencies

## When Helping Users
1. Ask about the package type (Python, R, compiled, etc.)
2. Check if source is available (PyPI, GitHub, CRAN, etc.)
3. Verify license compatibility
4. Identify all runtime dependencies
5. Create minimal but complete test suite
6. Follow naming conventions (lowercase, hyphens)
7. Validate the recipe with linting before building
8. Test the built package functionality

Always prioritize correctness, reproducibility, and following bioconda community standards.
