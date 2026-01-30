---
name: workleap-chromatic-best-practices
description: |
  Audit and update repositories to follow Workleap's Chromatic best practices for snapshot cost control and CI optimization.

  Use this skill when:
  (1) Auditing a repository for Chromatic best practices compliance
  (2) Implementing Chromatic cost optimizations in a project
  (3) Fixing TurboSnap-disabling patterns in code
  (4) Setting up chromatic.config.json with the untraced option
  (5) Updating CI workflows for conditional Chromatic execution
  (6) Refactoring barrel file imports in Storybook preview files
  (7) Reviewing PRs for Chromatic cost impact
  (8) Setting up Chromatic in a new Turborepo project
  (9) Checking for local Chromatic usage that should be removed
---

# Workleap Chromatic Best Practices

Guide for auditing and updating repositories to follow Workleap's Chromatic best practices.

## Audit Workflow

When asked to audit or update a repository for Chromatic best practices, follow these steps in order:

### Step 1: Locate Chromatic Configuration

Search for existing Chromatic setup:

```
chromatic.config.json
.storybook/preview.ts
.storybook/preview.tsx
.github/workflows/*chromatic*.yml
.github/workflows/*storybook*.yml
package.json (scripts section)
```

If no Chromatic configuration exists, ask the user if they want to set it up.

### Step 2: Audit and Fix Each Practice

#### 2.1 Check `untraced` Configuration (Optional)

**Find:** `chromatic.config.json`

**Optional configuration:**

```json
{
    "$schema": "https://www.chromatic.com/config-file.schema.json",
    "untraced": ["**/package.json"]
}
```

**Trade-off:** Adding `package.json` to `untraced` reduces snapshot costs but may cause missed visual regressions when updating NPM packages that include breaking visual changes (e.g., UI library updates like Hopper).

**When to use `untraced`:**
- Projects where dependency updates rarely affect visuals
- Teams that manually verify visual changes after dependency updates

**When to avoid `untraced`:**
- Projects heavily dependent on UI libraries (Hopper, design systems)
- When visual regression detection for dependency updates is critical

**Action:** Ask the user about their preference. If they want to reduce costs and accept the trade-off, add the `untraced` option. Otherwise, skip this optimization.

#### 2.2 Audit Storybook Preview Imports

**Find:** `.storybook/preview.ts` or `.storybook/preview.tsx`

**Look for barrel file imports:**

```ts
// BAD - barrel file import triggers full build when ANY export changes
import { ThemeProvider, I18nProvider } from "@app/providers";
import { something } from "../src";
import { util } from "@app/utils";
```

**Replace with direct imports:**

```ts
// GOOD - direct imports only trigger rebuilds for specific file changes
import { ThemeProvider } from "@app/providers/ThemeProvider";
import { I18nProvider } from "@app/providers/I18nProvider";
```

**Detection patterns:**
- Imports from paths ending in `/index` (explicit or implicit)
- Imports from package-level paths like `@app/utils` or `../src`
- Multiple named imports from a single module (often indicates barrel)

**Action:** Refactor to direct imports. If the direct path doesn't exist, note it as a recommendation.

#### 2.3 Check for Local Chromatic Usage

**Find:** `package.json` scripts section

**Bad patterns:**

```json
{
  "scripts": {
    "chromatic": "chromatic",
    "test:visual": "chromatic --project-token=...",
    "storybook:test": "chromatic"
  }
}
```

**Action:** Remove or comment out local Chromatic scripts. Chromatic should only run from CI via pull requests, never locally.

**Why:** Running Chromatic locally triggers the entire visual test suite, wasting snapshots.

#### 2.4 Check CI Workflow for Label-Based Triggering

**Find:** GitHub Actions workflow files that run Chromatic

**Required pattern:**

```yaml
on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main
    types:
      - opened
      - labeled
  workflow_dispatch:

jobs:
  chromatic:
    steps:
      - name: Early exit if "run chromatic" label is not present
        if: github.event_name == 'pull_request' && !contains(github.event.pull_request.labels.*.name, 'run chromatic')
        run: |
          echo "No \"run chromatic\" label present. Skipping Chromatic workflow."
          exit 78
```

**Bad patterns:**

```yaml
# BAD - runs on every PR without label check
on:
  pull_request:

jobs:
  chromatic:
    # No label check
```

**Action:** Add label-based conditional execution. The label name should be `run chromatic`.

#### 2.5 Check CI Workflow for Required Flags

**Find:** Chromatic action step in CI workflow

**Required flags:**

```yaml
- name: Chromatic
  uses: chromaui/action@latest
  with:
    projectToken: ${{ secrets.CHROMATIC_PROJECT_TOKEN }}
    onlyChanged: true        # Enables TurboSnap
    exitOnceUploaded: true   # Faster CI, doesn't wait for build
    autoAcceptChanges: main  # Auto-accept on main branch
```

**Check for:**
- `onlyChanged: true` - Required for TurboSnap
- `exitOnceUploaded: true` - Recommended for faster CI
- `autoAcceptChanges: main` - Recommended to auto-accept baseline on main

**Action:** Add missing flags to the Chromatic action.

#### 2.6 Check CI Workflow for Proper Git Checkout

**Find:** Checkout step in CI workflow

**Required configuration:**

```yaml
- name: Checkout
  uses: actions/checkout@v6
  with:
    fetch-depth: 0  # Required for TurboSnap
    ref: ${{ github.event.pull_request.head.ref }}
  env:
    CHROMATIC_BRANCH: ${{ github.event.pull_request.head.ref || github.ref_name }}
    CHROMATIC_SHA: ${{ github.event.pull_request.head.sha || github.ref }}
    CHROMATIC_SLUG: ${{ github.repository }}
```

**Critical check:** `fetch-depth: 0` is required for TurboSnap to work properly.

**Action:** Add `fetch-depth: 0` and Chromatic environment variables if missing.

#### 2.7 Check Browser Configuration

**Find:** Chromatic CLI flags in CI workflow or `chromatic.config.json`

**Look for multi-browser flags:**

```yaml
# BAD - doubles/triples snapshot count
npx chromatic --browsers chrome,firefox
```

**Required:** Chrome only (default, no flag needed)

**Action:** Remove multi-browser flags unless explicitly required.

#### 2.8 Check for Renovate/Changesets Exclusion

**Find:** CI workflow and branch ruleset configuration

**Recommendation:** Exclude Renovate bot and Changesets branches from the required status check ruleset, not from the workflow itself.

**Action:** Document recommendation to configure branch ruleset to exclude:
- `renovate/*` branches
- `changeset-release/*` branches

#### 2.9 Identify Large Files in Preview Dependencies

**Scan files imported by `.storybook/preview.ts[x]`** for problematic patterns:

**Problematic file types:**
- Localization files (`**/resources.json`, `**/translations/*.json`)
- Route definitions (large route config objects)
- Environment configs
- Utility files with many exports

**Detection:** Files with >20 exports or >500 lines that are imported by preview.

**Action:** Document findings and recommend splitting into smaller, focused modules.

#### 2.10 Check for Workflow Optimizations

**Find:** CI workflow file

**Recommended patterns:**

```yaml
# Concurrency to cancel in-progress runs
concurrency:
  group: chromatic-${{ github.ref }}
  cancel-in-progress: true

# Label removal after completion
- name: Remove "run chromatic" label after Chromatic completion
  if: github.event_name == 'pull_request'
  uses: actions/github-script@v8
  with:
    script: |
      github.rest.issues.removeLabel({
          owner: context.repo.owner,
          repo: context.repo.repo,
          issue_number: context.issue.number,
          name: 'run chromatic'
      });
```

**Action:** Add concurrency settings and label removal step if missing.

### Step 3: Generate Audit Report

After completing the audit, provide a summary:

```markdown
## Chromatic Best Practices Audit

### Findings

| Practice | Status | Action Required |
|----------|--------|-----------------|
| `untraced` config (optional) | ✅/❌/N/A | [action or user declined] |
| Preview barrel imports | ✅/❌ | [action] |
| No local Chromatic scripts | ✅/❌ | [action] |
| CI label-based triggering | ✅/❌ | [action] |
| CI `onlyChanged: true` flag | ✅/❌ | [action] |
| CI `fetch-depth: 0` | ✅/❌ | [action] |
| CI Chromatic env vars | ✅/❌ | [action] |
| Chrome-only snapshots | ✅/❌ | [action] |
| CI concurrency settings | ✅/❌ | [action] |
| CI label auto-removal | ✅/❌ | [action] |
| Large file dependencies | ✅/❌ | [action] |

### Changes Made
- [list of files modified]

### Recommendations
- [list of suggested improvements that require user decision]
- Consider adding `untraced` for package.json (trade-off: may miss UI library regressions)
- Configure branch ruleset to exclude Renovate/Changesets branches
- Add `run chromatic` as a required status check
```

## Reference: Why These Practices Matter

### TurboSnap Preservation

TurboSnap analyzes Git changes to snapshot only affected stories. These patterns disable TurboSnap and trigger full builds (all stories):

| Change Type | Files |
|-------------|-------|
| Storybook preview | `.storybook/preview.ts[x]` |
| Barrel file dependencies | Any `index.ts[x]` imported by preview |
| Package dependencies | `**/package.json` (optionally use `untraced`) |
| Large shared files | Routes, constants, localization |
| Shallow git clone | Missing `fetch-depth: 0` |

### Snapshot Cost Multipliers

| Configuration | Snapshots per Story |
|---------------|---------------------|
| Chrome only | 1x |
| Chrome + Safari | 2x |
| Chrome + Safari + Firefox | 3x |

### CI Trigger Strategy

Running Chromatic on every PR commit wastes snapshots on work-in-progress:
- Use `run chromatic` label to trigger workflow
- Auto-remove label after completion
- Make workflow a required status check to remind reviewers

## Monorepo-Specific Audit

For Turborepo/monorepo projects, additional checks:

1. **Per-package Chromatic configs:** Each package with Storybook should have its own `chromatic.config.json`

2. **Turborepo cache in CI:** Workflow should restore/save Turborepo cache:
   ```yaml
   - name: Restore Turborepo cache
     uses: actions/cache/restore@v5
     with:
       key: ${{ runner.os }}-turbo-chromatic-${{ github.sha }}
       restore-keys: |
         ${{ runner.os }}-turbo-chromatic-
         ${{ runner.os }}-turbo-
       path: .turbo
   ```

3. **Module-level triggering:** For modular architecture, configure CI to run Chromatic only for affected modules

## Critical Rules

1. **Never invent Chromatic options** - Only use documented configuration
2. **CI-only execution** - Never recommend running Chromatic locally
3. **Preserve TurboSnap** - Every recommendation should maintain TurboSnap effectiveness
4. **Cost awareness** - Every snapshot counts toward monthly budget
