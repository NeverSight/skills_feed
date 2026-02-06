---
name: e2e-ci-debug
description: Debug CI E2E failures from pull requests by inspecting GitHub checks, downloading Playwright reports, and mapping failures to local Nx commands. Use when debugging failed E2E tests in PR workflows.
---

# E2E CI Debug

Debug Playwright E2E test failures from CI with automated artifact downloading, intelligent failure parsing, and local reproduction guidance.

## Quick Start

**Full debugging workflow:**

```bash
# 1. Download artifacts from failing CI run
.cursor/skills/e2e-ci-debug/scripts/download-artifacts.sh

# 2. Parse JUnit results to identify failures
.cursor/skills/e2e-ci-debug/scripts/parse-junit.py

# 3. Run local reproduction command (shown by parse-junit.py)
cd dap-workspace && nx affected -t e2e --base=origin/main

# 4. Clean up downloaded artifacts (Important!)
.cursor/skills/e2e-ci-debug/scripts/cleanup-artifacts.sh
```

**Output:** Failing spec name, error message, file location, stack trace, and local reproduction command.

## Workflow E2E Test Structure

### Main Workflow E2E Tests
- **Path**: `dap-workspace/tests/workflow/typescript/`
- **Config**: `playwright.config.ts`
- **Test Directory**: `tests/e2e/`
  - `builder/` - Workflow builder tests (9 spec files)
  - `catalog/` - Catalog navigation tests (2 spec files)
  - `visual-diff/` - Visual regression tests (1 spec file)
- **Projects**: `sanity` → `setup` → `e2e` (dependency chain)
- **Reports**: `reports/typescript-playwright/workflow/`
  - HTML: `playwright-report/`
  - JUnit: `junit.xml`
- **Base URL**: `WORKFLOW_BASE_URL` env var or `http://localhost:4200`

### Component-Level E2E Tests
- **Path**: `dap-workspace/libs/workflow/workflow-fe/workflow-fe-e2e/`
- **Config**: `playwright.config.ts`
- **Test Directory**: `src/`
- **WebServer**: Auto-starts `workflow-root-fe` on `http://localhost:4200`
- Used for component-level testing within workflow libraries

## CI Workflow Context

### PR E2E Tests

**When they run:**
- Automatically on pull requests via `dispatcher.yml` → `pr-core.yaml` → `pr-processor.yml`
- Only **affected** E2E tests execute (via `nx affected -t e2e`)

**How to find them:**
```bash
# List PR checks
gh pr checks

# View specific run
gh run view <run_id> --log

# Download PR E2E artifacts
gh run download <run_id> -n <artifact-name>
```

**Workflow chain:**
1. `.github/workflows/dispatcher.yml` - PR entry point
2. `.github/workflows/pr-core.yaml` - Runs test, lint, docker, deploy jobs
3. `pr-processor.yml` (external) - Handles deployment and E2E execution

## Local Debugging

Run workflow E2E tests locally before pushing to CI:

### Run Workflow E2E Project

```bash
cd dap-workspace

# Run full workflow E2E suite (with project dependencies)
nx e2e tests-workflow-typescript --project=e2e

# Run only sanity tests
nx e2e tests-workflow-typescript --project=sanity
```

### Run Affected E2E Tests

```bash
cd dap-workspace

# Compare against main branch
nx affected -t e2e --base=origin/main

# Compare against specific branch
nx affected -t e2e --base=origin/v4.0
```

### Run Specific Test File

```bash
cd dap-workspace/tests/workflow/typescript

# Run single spec
npx playwright test tests/e2e/builder/workflow-builder.e2e.spec.ts

# Run specific suite
npx playwright test tests/e2e/builder

# Run with UI mode for debugging
npx playwright test --ui

# Run with headed browser
npx playwright test --headed
```

### View Local Test Reports

```bash
cd dap-workspace

# Open HTML report for workflow tests
npx playwright show-report reports/typescript-playwright/workflow/playwright-report
```

## PR Checks Debugging

### E2E Test Failures

1. **Find failing E2E job:**
   ```bash
   gh pr checks
   # Look for "Run E2E Tests" or similar job names
   ```

2. **Download artifacts:**
   ```bash
   # Use the download-artifacts.sh script (auto-detects current PR)
   .cursor/skills/e2e-ci-debug/scripts/download-artifacts.sh
   
   # Or manually with run ID
   .cursor/skills/e2e-ci-debug/scripts/download-artifacts.sh <run_id>
   ```

3. **Parse failures:**
   ```bash
   .cursor/skills/e2e-ci-debug/scripts/parse-junit.py
   ```

4. **Reproduce locally:**
   ```bash
   cd dap-workspace
   nx affected -t e2e --base=origin/<base-branch>
   ```

### Unit Test Failures

```bash
# View test job logs
gh run view <run_id> --log --job <job_id>

# Find the specific test command in logs
# Usually: nx affected -t test --base=origin/<base-branch>

# Run locally
cd dap-workspace
nx affected -t test --base=origin/main
```

### Lint Failures

```bash
# View lint job logs
gh run view <run_id> --log --job <job_id>

# Run locally
cd dap-workspace
nx affected -t lint --base=origin/main

# Auto-fix many issues
nx affected -t lint --base=origin/main --fix
```

### Docker Build Failures

```bash
# View docker job logs
gh run view <run_id> --log --job <job_id>

# Look for:
# - Docker build errors
# - Missing dependencies
# - Build context issues
# - Registry authentication problems
```

## Utility Scripts

All scripts are located in the skill's `scripts/` directory. After installation via `npx add-skill`, they'll be at `.cursor/skills/e2e-ci-debug/scripts/`

### download-artifacts.sh

Downloads Playwright test artifacts from GitHub Actions for the current PR.

**Usage:**
```bash
# Auto-detect from current PR
./download-artifacts.sh

# Specify run ID
./download-artifacts.sh <run_id>

# Specify run ID and artifact name
./download-artifacts.sh <run_id> <artifact_name>
```

**What it does:**
- Fetches Playwright report archives from GitHub Actions
- Extracts to `playwright-results/` directory
- Cleans up ZIP files after extraction

### parse-junit.py

Parses JUnit XML from Playwright results and extracts structured failure information, including paths to failure screenshots for AI model analysis.

**Usage:**
```bash
# Parse default location
./parse-junit.py

# Parse specific file
./parse-junit.py path/to/junit.xml

# Output as JSON (includes screenshot/trace/video paths)
./parse-junit.py --json

# Show screenshot paths for AI model analysis
./parse-junit.py --screenshots

# Open HTML report after parsing
./parse-junit.py --open-report

# Show help
./parse-junit.py --help
```

**Output includes:**
- Test name and status
- Error message
- File location (spec file:line number)
- Stack trace
- **Screenshot paths** (absolute paths for AI model to read with Read tool)
- **Trace file paths** (for Playwright trace viewer)
- **Video paths** (if video recording was enabled)
- Local reproduction command for workflow tests

**Output Formats:**
- **Text (default):** Human-readable with colors and emojis, shows artifact paths inline
- **JSON (`--json`):** Structured output with `screenshots`, `traces`, and `videos` arrays per failure

**AI Model Integration:**
The screenshot paths are absolute, allowing AI models to directly read the images using the Read tool to visually analyze where Playwright failed.

### find-failing-job.sh

Finds failing E2E jobs from recent PR workflow runs.

**Usage:**
```bash
# List recent PR workflow runs
./find-failing-job.sh

# Find specific workflow
./find-failing-job.sh "PR Deploy Core"
```

**Output:**
- Recent workflow runs with status
- Run ID and job IDs for failed E2E tests
- Command to download artifacts

### cleanup-artifacts.sh

Removes all downloaded Playwright artifacts after debugging.

**Usage:**
```bash
./cleanup-artifacts.sh
```

**What it removes:**
- `playwright-results/` directory
- `*-playwright-results.zip` files
- Any other temporary E2E debug files

**Safety:**
- Idempotent (safe to run multiple times)
- Confirms cleanup with file count and freed disk space

## Common Failure Patterns

### Test Timeout

**Symptom:** Test exceeds timeout (default: 30s for sanity, 120s for setup, 30s for e2e)

**Solutions:**
- Check for network delays or slow API responses
- Increase timeout in `playwright.config.ts` if legitimate
- Look for missing `await` on async operations

### Element Not Found

**Symptom:** `Selector not found` or `Element is not visible`

**Solutions:**
- Verify element exists in the DOM
- Check for timing issues (add proper waits)
- Inspect for dynamic class names or IDs
- Use data-testid attributes instead of classes

### Setup/Seed Failures

**Symptom:** `setup` project fails before `e2e` tests can run

**Solutions:**
- Check database seeding in `tests/*/typescript/seed/*.setup.ts`
- Verify API endpoints are accessible
- Ensure authentication/tokens are valid

### Flaky Tests

**Symptom:** Test passes locally but fails in CI (or vice versa)

**Solutions:**
- Check for race conditions
- Avoid hard-coded waits (`page.waitForTimeout()`)
- Use proper Playwright assertions with auto-retry
- Verify test isolation (no shared state)

## Additional Resources

For detailed workflow documentation, artifact paths, and Playwright configuration details, see [reference.md](reference.md).

## When to Use This Skill

Use this skill when:
- A PR has failing E2E checks and you need to debug
- You want to reproduce CI E2E failures locally
- You need to understand E2E test structure and locations
- You're debugging flaky or timing-related test failures in PRs
