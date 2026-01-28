---
name: deps-minor
description: Safe minor dependency updates with validation (lint/test/build) and automatic rollback on failure.
---

# Purpose

Perform safe **minor** npm dependency updates for the current project.  
Run validation (lint → test → build) after each update, and revert if any step fails.  
No major updates are performed.

# Scope

- Operates on both `dependencies` and `devDependencies`.
- Updates only minor versions (`x.X.x`).
- No git operations.
- Excludes i18next* and storybook* packages.

# Process

1. **Discovery**
   - Run: `ncu --target minor --jsonAll`
   - Filter out:
     - Any package containing `i18next`, `18next`, or `storybook`
2. **Batch Update**
   - Update in batches of ≤8 packages:
     ```bash
     ncu -u <pkg-list> --target minor
     npm install --no-audit --no-fund
     ```
3. **Validation**
   - Run (if present):
     ```bash
     npm run lint
     npm run test
     npm run build
     ```
   - If any step fails:
     - Revert last batch changes using backup copy.
     - Log failure and skip problematic packages.
4. **Reporting**
   - Output summary with:
     - Updated packages
     - Skipped packages
     - Validation results
   - Remind user: “No git operations were performed.”

# Tool Permissions

- **Bash**: run shell commands
- **Read**: inspect `package.json`, test scripts
- **Write**: modify `package.json`, `package-lock.json`

# Safety

- Always back up `package.json` and `package-lock.json` before updates.
- Never touch excluded packages.
- Stop on first failed batch.
