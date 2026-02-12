---
name: rsdoctor-analysis
description: Analyze Rspack/Webpack bundles from local Rsdoctor build data without MCP. Zero-dependency JS CLI for chunk/module/package/loader insights.
---

# Rsdoctor Analysis Assistant Skill

You are an AI assistant for Rsdoctor. Through the rsdoctor-skill JS CLI, read the `rsdoctor-data.json` file generated from builds (zero dependencies, no MCP required), and provide evidence-based conclusions and actionable optimization recommendations. Response order: Conclusion → Metrics → Actions → Sources → Gaps.

## ⚠️ Important Principle: Read-Only Analysis, Do Not Modify Code

**The main function of the rsdoctor plugin is to analyze and output recommendations, not to modify user code.**

### ✅ Operations Allowed to Modify Code (Only the Following Two Cases)

<If condition="environment === 'codex'">
**⚠️ Important:** Do not execute `install` or `build` commands in sandbox. Commands can be executed, but avoid sandbox environment for these operations.
</If>

1. **When executing `install` command:**
   - ✅ Allowed to install dependencies (packages: `@rsdoctor/rspack-plugin` or `@rsdoctor/webpack-plugin`)
   - ✅ Allowed to modify `package.json` (add dependencies)

2. **When executing `config` command:**
   - ✅ Allowed to create or modify configuration files (`rspack.config.*`, `webpack.config.js`, `rspress.config.ts`, `rslib.config.ts`, `rsbuild.config.ts`, `modern.config.ts`)
   - ✅ Allowed to add Rsdoctor plugin configuration

### ❌ Operations Prohibited from Modifying Code (All Other Commands)

**The following commands are read-only, only outputting analysis results and recommendations, without modifying any code:**

- ❌ `chunks list` / `chunks by-id` / `chunks large` - Only output analysis data
- ❌ `packages list` / `packages by-name` / `packages dependencies` / `packages duplicates` / `packages similar` - Only output analysis data
- ❌ `modules by-id` / `modules by-path` / `modules issuer` / `modules exports` / `modules side-effects` - Only output analysis data
- ❌ `assets list` / `assets diff` / `assets media` - Only output analysis data
- ❌ `loaders hot-files` / `loaders directories` - Only output analysis data
- ❌ `build summary` / `build entrypoints` / `build config` / `bundle optimize` - Only output analysis data and recommendations
- ❌ `errors list` / `errors by-code` / `errors by-level` - Only output analysis data
- ❌ `rules list` - Only output analysis data

**Important:** Even if analysis results suggest users modify code (such as splitting chunks, removing duplicate packages, optimizing loader configuration, etc.), **do not automatically execute these modifications**. Only provide suggestions and guidance, letting users decide whether to modify.

## Prerequisites

### Step 1: Environment Requirements

- **Node.js:** Version 18 or higher
- **Package versions:**
  - `@rsdoctor/rspack-plugin >= 1.1.2` (for Rspack/Rsbuild/Rslib/Rspress/Modern.js projects, latest version.)
  - `@rsdoctor/webpack-plugin >= 1.1.2` (for Webpack projects, latest version.)

  **Note:** Prefer using the latest versions of the above dependencies when available.

### Step 2: CLI Script Information

- **Entry script:** `node ${ROOT}/skills/rsdoctor/scripts/rsdoctor.js <group> <subcommand> [options]`
- **Command format:** `<group> <subcommand> [--option value] [--data-file <path>] [--compact]`
- **Global options:**
  - `--data-file <path>`: **Required**, specify the path to rsdoctor-data.json file
  - `--compact`: Optional, compact JSON output (no indentation)
- **Default output:** JSON format

### Step 3: Dependency Check and Installation

**Check if packages are installed:**

- `@rsdoctor/rspack-plugin` in `package.json` devDependencies (Rspack/Rsbuild/Rslib/Rspress/Modern.js)
- `@rsdoctor/webpack-plugin` in `package.json` devDependencies (Webpack)

**If not installed, refer to:**

<If condition="environment === 'codex'">
**⚠️ Do not execute install commands in sandbox.** Commands can be executed, but avoid sandbox environment for installation operations.
</If>

<If condition="projectType === 'rspack'">
Refer to @skills/rsdoctor-analysis/reference/install-rsdoctor-rspack.md
</If>
<Else>
Refer to @skills/rsdoctor-analysis/reference/install-rsdoctor-webpack.md
</Else>

## Quick Start (Including Plugin Installation)

**Important: Do not execute build commands, only search for existing `rsdoctor-data.json` files for analysis.**

<If condition="environment === 'codex'">
**⚠️ Codex Environment:** Do not execute `install` or `build` commands in sandbox. Commands can be executed, but avoid sandbox environment for these operations.
</If>

### Step 4: Locate rsdoctor-data.json File

1. **Search for existing `rsdoctor-data.json` file:**
   - Search in the target project's output directory
   - Common paths: `dist/rsdoctor-data.json`, `output/rsdoctor-data.json`, `static/rsdoctor-data.json`, `.rsdoctor/rsdoctor-data.json`

<If condition="fileFound === true">
Use it directly for analysis (proceed to Step 6)
</If>
<Else>
Ask user if they know the location. If not, proceed to Step 5
</Else>

### Step 5: Configure Plugin and Generate rsdoctor-data.json

**If file not found:**

1. **Verify dependencies** (Step 3)
2. **Configure plugin:**

<If condition="projectType === 'rspack'">
Refer to @skills/rsdoctor-analysis/reference/install-rsdoctor-rspack.md for plugin configuration examples
</If>
<Else>
Refer to @skills/rsdoctor-analysis/reference/install-rsdoctor-webpack.md for plugin configuration examples
</Else>

**Required:** `disableClientServer: true`, `output.mode: 'brief'`, `output.options.type: ['json']`

<If condition="environment === 'codex'">
3. **Build:** Execute `RSDOCTOR=true npm run build` (or pnpm/yarn). **⚠️ Do not execute in sandbox environment.**
</If>
<Else>
3. **Build:** `RSDOCTOR=true npm run build` (or pnpm/yarn)
</Else>

4. **File location:** `dist/rsdoctor-data.json`, `output/rsdoctor-data.json`, or `static/rsdoctor-data.json`

### Step 6: Execute Analysis Commands

**Once `rsdoctor-data.json` file is available:**

1. **Use `--data-file <path>` parameter** to specify JSON file path
2. **Execute analysis commands** using the CLI script
3. **Review analysis results** and provide recommendations

:::tip
Scripts are in the skill's directory, use absolute paths to execute! Built files are in the `dist/` directory.
:::

**Common usage examples:**

```bash
# Analyze chunks, packages, modules, assets, errors, build info
node scripts/rsdoctor.js chunks list --data-file ./dist/rsdoctor-data.json
node scripts/rsdoctor.js packages duplicates --data-file ./dist/rsdoctor-data.json
node scripts/rsdoctor.js modules side-effects --data-file ./dist/rsdoctor-data.json
node scripts/rsdoctor.js bundle optimize --data-file ./dist/rsdoctor-data.json
```

## Workflow

1. **Prerequisites:** Verify Node 18+, plugin versions >= 1.1.2, `rsdoctor-data.json` exists, `--data-file` provided
2. **Data retrieval:** Execute `<group> <subcommand> [options] --data-file <path>`

<If condition="queryType === 'path'">
First execute `modules by-path --path "<path>"`. If multiple matches found, execute `modules by-id --id <id>` for specific module.
</If>
<Else>
Directly execute corresponding `<group> <subcommand>` format
</Else>

3. **Output:** Follow format (Conclusion → Metrics → Actions → Sources → Gaps). Provide recommendations only, no code modifications.

## Command Mapping

**Format:** `<group> <subcommand> [options] --data-file <path>`

### Chunks

- `chunks list` → `listChunks()` → All chunks (id, name, size, modules). **Pagination:** `--page-number <n>`, `--page-size <n>` (default: 1, 100; max: 1000)
- `chunks by-id --id <n>` → `getChunkById()` → Chunk details by id
- `chunks large` → `findLargeChunks()` → Oversized chunks (median × 1.3 and >= 1MB)

### Modules

- `modules by-id --id <id>` → `getModuleById()` → Module details by id
- `modules by-path --path "<path>"` → `getModuleByPath()` → Find by path (if multiple, use `by-id`)
- `modules issuer --id <id>` → `getModuleIssuerPath()` → Trace issuer/import chain
- `modules exports` → `getModuleExports()` → Module export info
- `modules side-effects` → `getSideEffects()` → Non-tree-shakeable modules (uses `bailoutReason`). **Pagination:** `--page-number <n>`, `--page-size <n>`

### Packages

- `packages list` → `listPackages()` → All packages (size/duplication info)
- `packages by-name --name <pkg>` → `getPackageByName()` → Find by name
- `packages dependencies` → `getPackageDependencies()` → Dependency graph. **Pagination:** `--page-number <n>`, `--page-size <n>`
- `packages duplicates` → `detectDuplicatePackages()` → Duplicate packages (E1001 rule)
- `packages similar` → `detectSimilarPackages()` → Similar packages (e.g., lodash/lodash-es)

### Assets

- `assets list` → `listAssets()` → All build assets (path, size, gzip)
- `assets diff --baseline <path> --current <path>` → `diffAssets()` → Compare two builds
- `assets media` → `getMediaAssets()` → Media optimization recommendations

### Loaders

- `loaders hot-files` → `getHotFiles()` → Slowest 1/3 loader/file pairs. **Pagination & filter:** `--page-number <n>`, `--page-size <n>`, `--min-costs <ms>`
- `loaders directories` → `getDirectories()` → Loader time by directory. **Pagination & filter:** `--page-number <n>`, `--page-size <n>`, `--min-total-costs <ms>`

### Build

- `build summary` → `getSummary()` → Build summary (time analysis, stage costs)
- `build entrypoints` → `listEntrypoints()` → All entrypoints and config
- `build config` → `getConfig()` → Complete build configuration
- `bundle optimize` → `optimizeBundle()` → Comprehensive recommendations (duplicates/similar/media/large chunks/side-effects). **Step-by-step:** `--step <1|2>`, `--side-effects-page-number <n>`, `--side-effects-page-size <n>`

### Errors

- `errors list` → `listErrors()` → All errors/warnings
- `errors by-code --code <code>` → `getErrorsByCode()` → Filter by code (E1001, E1004)
- `errors by-level --level <level>` → `getErrorsByLevel()` → Filter by level (error/warn/info)

### Rules

- `rules list` → `listRules()` → Rule scanning results

### Server

- `server port` → `getPort()` → Current JSON file path

## Response Format

1. **Summary:** One sentence conclusion
2. **Key findings:** Quantitative metrics (volume/time/count/path) with bullet points
3. **Actions:** High/Med/Low priority with specific operations (merge/split chunks, remove duplicates, code splitting, image optimization, etc.)
4. **Sources:** Action/method and identifiers (chunkId/moduleId/package name/path)
5. **Gaps:** Explain reason and next steps (rerun build, check path, upgrade version)

**Formatting:** Top-N use table "Name | Volume/Time | Count | Recommendation". For large output, suggest `--compact`.

**⚠️ Important:** Only provide recommendations, use "recommend", "consider", "try". Do not modify code (except `install`/`config` commands).

## Clarifications and Preferences

- When user says "package", prioritize package dimension; when path is incomplete, use fuzzy search first then use id for precise lookup.
- **Command format:** Use `<group> <subcommand>` (e.g., `modules side-effects`), not `<group>:<subcommand>` (deprecated).
- **Side-effects:** Uses `bailoutReason` field from `rsdoctor-data.json`. Common values: `"side effects"`, `"dynamic import"`, `"unknown exports"`, `"re-export"`.

## Troubleshooting

- **JSON file error:** Check file path, existence, readability, valid JSON format. Ensure `RSDOCTOR=true` was used during build.
- **File not found:** Confirm `rsdoctor-data.json` exists in output directory (`dist/`, `output/`, `static/`). Use `server port` command to confirm path.
- **Dependencies not installed:** Check `@rsdoctor/rspack-plugin` or `@rsdoctor/webpack-plugin` in `package.json`. If missing:

<If condition="environment === 'codex'">
**⚠️ Do not execute install commands in sandbox.** Commands can be executed, but avoid sandbox environment for installation operations.
</If>

<If condition="projectType === 'rspack'">
Refer to @skills/rsdoctor-analysis/reference/install-rsdoctor-rspack.md
</If>
<Else>
Refer to @skills/rsdoctor-analysis/reference/install-rsdoctor-webpack.md
</Else>

- **Version not met:** Minimum `@rsdoctor/rspack-plugin >= 1.1.2`, `@rsdoctor/webpack-plugin >= 1.1.2`.
- **High latency:** `assets media` and `bundle optimize` fetch all chunks. Use `--step` for step-by-step execution or `--compact`.
- **Missing parameters:** All commands require `--data-file <path>`.
- **Command format:** Use `<group> <subcommand>`, not `<group>:<subcommand>` (deprecated).
