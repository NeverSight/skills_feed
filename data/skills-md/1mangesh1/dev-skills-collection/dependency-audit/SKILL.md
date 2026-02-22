---
name: dependency-audit
description: Dependency auditing, updating, and vulnerability management for npm, pip, and other package managers. Use when user asks to "audit dependencies", "update packages", "fix vulnerabilities", "check outdated", "npm audit", "pip audit", "upgrade dependencies safely", or any dependency management tasks.
---

# Dependency Audit

Audit, update, and manage dependencies safely.

## npm / Node.js

### Audit

```bash
# Run security audit
npm audit
npm audit --json              # Machine-readable
npm audit --production        # Production deps only

# Fix automatically
npm audit fix
npm audit fix --force         # Allow major version bumps

# Check specific advisory
npm audit --advisory=1234
```

### Check Outdated

```bash
# List outdated packages
npm outdated

# Output:
# Package    Current  Wanted  Latest  Location
# express    4.17.1   4.17.3  5.0.0   my-app
# lodash     4.17.20  4.17.21 4.17.21 my-app

# Wanted = highest version matching semver range in package.json
# Latest = latest version published
```

### Update Strategies

```bash
# Update within semver range (safe)
npm update

# Update specific package
npm update express

# Update to latest (may break)
npm install express@latest

# Interactive update tool
npx npm-check-updates         # List all updates
npx npm-check-updates -u      # Update package.json
npm install                    # Install updated

# Update with target
npx npm-check-updates --target minor  # Only minor+patch
npx npm-check-updates --target patch  # Only patch
```

### Lock File

```bash
# Regenerate lock file
rm package-lock.json && npm install

# Check lock file integrity
npm ci    # Clean install from lock file (CI)

# Deduplicate
npm dedupe
```

## Python / pip

### Audit

```bash
# pip-audit (recommended)
pip install pip-audit
pip-audit
pip-audit -r requirements.txt
pip-audit --fix               # Auto-fix vulnerabilities
pip-audit --json              # Machine-readable

# Safety (alternative)
pip install safety
safety check
safety check -r requirements.txt
```

### Check Outdated

```bash
# List outdated packages
pip list --outdated
pip list --outdated --format=json

# Check specific package
pip show package-name
```

### Update Strategies

```bash
# Update single package
pip install --upgrade requests

# Update all packages (careful!)
pip list --outdated --format=json | python -c "
import json, sys
for pkg in json.load(sys.stdin):
    print(pkg['name'])" | xargs -n1 pip install --upgrade

# Pin versions after updating
pip freeze > requirements.txt
```

### pip-tools (Recommended)

```bash
pip install pip-tools

# Define requirements.in (unpinned)
# requirements.in:
# flask
# sqlalchemy>=2.0

# Compile to pinned requirements.txt
pip-compile requirements.in

# Update all
pip-compile --upgrade requirements.in

# Update specific package
pip-compile --upgrade-package flask requirements.in

# Sync environment to match
pip-sync requirements.txt
```

## Yarn

```bash
# Audit
yarn audit
yarn audit --level moderate    # Only moderate+

# Outdated
yarn outdated

# Update
yarn upgrade                   # Within ranges
yarn upgrade --latest          # To latest versions
yarn upgrade-interactive       # Interactive picker

# Dedupe
yarn dedupe
```

## pnpm

```bash
# Audit
pnpm audit
pnpm audit --fix

# Outdated
pnpm outdated

# Update
pnpm update
pnpm update --latest
pnpm update --interactive
```

## Renovate / Dependabot

### Dependabot (GitHub)

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    reviewers:
      - "team-name"
    labels:
      - "dependencies"
    groups:
      dev-deps:
        patterns:
          - "*"
        dependency-type: "development"
      prod-deps:
        patterns:
          - "*"
        dependency-type: "production"

  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

### Renovate

```json
// renovate.json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["config:recommended"],
  "schedule": ["before 6am on Monday"],
  "automerge": true,
  "automergeType": "pr",
  "packageRules": [
    {
      "matchUpdateTypes": ["patch"],
      "automerge": true
    },
    {
      "matchUpdateTypes": ["major"],
      "automerge": false,
      "labels": ["breaking"]
    }
  ]
}
```

## Update Workflow

```
1. Check what's outdated
   npm outdated / pip list --outdated

2. Run audit for vulnerabilities
   npm audit / pip-audit

3. Update patch versions first (safest)
   npx ncu --target patch -u && npm install

4. Run tests
   npm test / pytest

5. Update minor versions
   npx ncu --target minor -u && npm install && npm test

6. Update major versions one at a time
   npm install package@latest && npm test
   Read migration guides for major bumps

7. Commit and push
   git add package.json package-lock.json
   git commit -m "chore: update dependencies"
```

## License Checking

```bash
# npm
npx license-checker --summary
npx license-checker --onlyAllow "MIT;ISC;BSD-3-Clause;Apache-2.0"

# Python
pip install pip-licenses
pip-licenses --summary
pip-licenses --allow-only "MIT;BSD;Apache-2.0"
```

## Reference

For CI integration and automation: `references/automation.md`
