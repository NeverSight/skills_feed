---
name: myvibe-publish
description: Publish static HTML, ZIP archive, or directory to MyVibe. Use this skill when user wants to publish/deploy web content to MyVibe.
references:
  - references/metadata-analysis.md
---

# MyVibe Publish

Publish web content (HTML file, ZIP archive, or directory) to MyVibe.

## Usage

```bash
# Publish a ZIP file
/myvibe:myvibe-publish --file ./dist.zip

# Publish a single HTML file
/myvibe:myvibe-publish --file ./index.html

# Publish a directory (auto-zip)
/myvibe:myvibe-publish --dir ./dist

# Import and publish from URL
/myvibe:myvibe-publish --url https://example.com/my-app

# Publish to specific myvibe instance
/myvibe:myvibe-publish --file ./dist.zip --hub https://custom-hub.com
```

## Options

| Option | Alias | Description |
|--------|-------|-------------|
| `--file <path>` | `-f` | Path to HTML file or ZIP archive |
| `--dir <path>` | `-d` | Directory to compress and publish |
| `--url <url>` | `-u` | URL to import and publish |
| `--hub <url>` | `-h` | MyVibe URL (default: https://staging.myvibe.so/) |
| `--title <title>` | `-t` | Project title |
| `--desc <desc>` | | Project description |
| `--visibility <vis>` | `-v` | Visibility: public or private (default: public) |

## Workflow

**CRITICAL: You MUST read reference files before starting analysis**

Before starting any analysis, you MUST use the Read tool to read:
- `references/metadata-analysis.md` - Detailed metadata extraction and tags matching workflow

### Workflow Overview

1. **Detect Project Type** → determine if build is needed
2. **Build** (if needed) → compile the project
3. **Metadata Analysis** → extract title, description, tags, screenshot
4. **Confirm Publish** → show metadata, get user confirmation
5. **Execute Publish** → upload to MyVibe

**IMPORTANT**: Step 3 (Metadata Analysis) is ALWAYS required, including after build.

### 1. Detect Project Type

Determine what type of project this is and what the publish target will be.

**Target directory**: `--dir` if specified, otherwise current working directory.

#### Project Type Detection

| Check | Project Type | Next Step |
|-------|-------------|-----------|
| `--file` with HTML file | **Single HTML** | → Step 3 (analyze the HTML file) |
| `--file` with ZIP file | **ZIP Archive** | → Step 3 (extract and analyze) |
| Has `dist/index.html`, `build/index.html`, or `out/index.html` | **Pre-built** | → Step 2 (confirm rebuild or use existing) |
| Has `package.json` with `build` script, no output folder | **Buildable** | → Step 2 (build first) |
| Has multiple `package.json` files or workspace config | **Monorepo** | → Step 2 (select app, then build) |
| Has `index.html` at root, no `package.json` | **Static** | → Step 3 (analyze root directory) |
| Cannot determine | **Unknown** | → Step 3 (analyze as-is) |

Output format:
```
Project Type Detection:
- Type: [type]
- Reason: [why this type was detected]
- Publish target: [directory or file path]
- Next step: [Step 2: Build / Step 3: Metadata Analysis]
```

### 2. Build Decision (for Pre-built/Buildable/Monorepo projects)

#### Detect Build Configuration

**Package Manager** (from lock files):

| Lock File | Package Manager |
|-----------|-----------------|
| `pnpm-lock.yaml` | pnpm |
| `yarn.lock` | yarn |
| `bun.lockb` or `bun.lock` | bun |
| `package-lock.json` | npm |
| None | npm (default) |

**Build Command** (from `package.json` scripts):
- Priority: `build:prod` > `build:production` > `build`

**Output Directory** (from config files):

| Config File | Expected Output |
|-------------|-----------------|
| `vite.config.*` | `dist` |
| `next.config.*` | `.next` or `out` |
| `webpack.config.*` | `dist` |
| `astro.config.*` | `dist` |
| `nuxt.config.*` | `.output` |
| None recognized | Check `dist`, `build`, `out` in order |

#### Show Analysis & Confirm Build

Present the analysis to user:

```
Project Analysis:
- Type: [framework] project
- Package Manager: [pm]
- Build Command: [pm] run build
- Output Directory: [dir]

Warnings (if any):
- Missing .env file (.env.example exists)
- Large files detected (> 10MB)
```

**For Pre-built projects** (existing build output found), use `AskUserQuestion`:

```
Question: "Found existing build output in [dir]/. Rebuild to ensure latest?"
Header: "Build"
Options:
  - Label: "Rebuild & Publish"
    Description: "Run build again, then publish [dir]/"
  - Label: "Use Existing"
    Description: "Publish existing [dir]/ without rebuilding"
  - Label: "Publish Source"
    Description: "Skip output folder, publish source as-is"
```

**For Buildable projects** (no build output), use `AskUserQuestion`:

```
Question: "Proceed with build before publishing?"
Header: "Build"
Options:
  - Label: "Build & Publish"
    Description: "Run build, then publish [output_dir]/"
  - Label: "Publish Source"
    Description: "Skip build, publish source as-is"
```

#### Execute Build (if confirmed)

```bash
cd [project_dir] && [pm] install && [pm] run build
```

**On build failure:**
- Analyze error output
- Offer to help fix common issues (missing dependencies, config errors)
- User can choose to fix and retry, or publish source as-is

**After build completes:** Proceed to **Step 3: Metadata Analysis** with the build output directory as the publish target.

#### Monorepo Handling

When multiple `package.json` files detected, use `AskUserQuestion`:

```
Question: "Monorepo detected. Which app would you like to publish?"
Header: "App"
Options:
  - Label: "[apps/web]"
    Description: "[framework] detected in apps/web"
  - Label: "[apps/admin]"
    Description: "[framework] detected in apps/admin"
  - Label: "Other"
    Description: "Specify a different path"
```

After selecting and building the app, proceed to **Step 3: Metadata Analysis**.

### 3. Metadata Analysis

**CRITICAL: This step is MANDATORY for ALL project types, including after build.**

Follow `references/metadata-analysis.md` completely. Each step MUST output results:

1. Extract metadata (title, description, githubRepo)
2. Fetch and match tags
3. Generate screenshot

If screenshot fails, skip coverImage and let server auto-generate.

### 4. Confirm Publish

Present all extracted metadata to the user:

```
Publishing to MyVibe:
──────────────────────
Title: [extracted title]

Description:
[generated story, 50-150 words]

Visibility: public
Source: [directory path]

GitHub: [repo URL or "Not detected"]
Cover Image: [screenshot URL or "Will be auto-generated"]

Tags (auto-detected):
- Tech Stack: [matched tag names, e.g., "React, TypeScript, Vite"]
- Platform: [matched tag names or "None"]
- Category: [suggested category or "None"]
- Model: [detected AI models or "None"]
```

Use `AskUserQuestion` to confirm:

```
Question: "Confirm publish with these details?"
Header: "Publish"
Options:
  - Label: "Publish"
    Description: "Publish with the metadata shown above"
  - Label: "Edit details"
    Description: "Modify title, description, tags, or other fields"
```

If user selects "Edit details", collect corrections via follow-up questions.

### 5. Execute Publish

Only after user confirmation in Step 4, execute the publish script.

**Dependency Check Strategy:**
1. Check if `skills/myvibe-publish/scripts/node_modules` directory exists
2. If not exists: run `npm install` first
3. If publish fails with module errors: run `npm install` and retry

**Method 1: Using Config File (Recommended for full metadata)**

Write a YAML config file with all metadata, then publish:

```bash
# Write config file in current directory
# File: ./publish-config.yaml
```

```yaml
source:
  type: dir
  path: ./dist
hub: https://staging.myvibe.so
metadata:
  title: My App
  description: A cool web application
  visibility: public
  coverImage: https://...
  githubRepo: https://github.com/user/repo
  platformTags: [1, 2]
  techStackTags: [3, 4, 5]
  categoryTags: [6]
  modelTags: [7]
```

```bash
# Publish using config file
node skills/myvibe-publish/scripts/publish.mjs --config ./publish-config.yaml
```

The config file is automatically deleted after successful publish.

**Method 2: Command Line Arguments (Simple cases)**

```bash
# Publish a directory
node skills/myvibe-publish/scripts/publish.mjs \
  --dir ./dist \
  --hub https://staging.myvibe.so \
  --title "My App" \
  --desc "A cool app" \
  --visibility public

# Publish a file
node skills/myvibe-publish/scripts/publish.mjs \
  --file ./dist.zip \
  --hub https://staging.myvibe.so \
  --title "My App"

# Import from URL
node skills/myvibe-publish/scripts/publish.mjs \
  --url https://example.com/my-app \
  --hub https://staging.myvibe.so
```

**Script Output:**

On success:
```
Published successfully!
URL: https://staging.myvibe.so/{userDid}/{vibeDid}
```

### 6. Return Result

- On success: Show the published URL to the user
- On failure: Show the error message and suggest solutions

## Error Handling

| Error | Handling |
|-------|----------|
| Dependencies not installed | Run `npm install` in scripts directory |
| 401/403 Authorization error | Token will be cleared automatically, re-run to authorize again |
| Upload failed | Show error message, suggest checking file format |
| Conversion failed | Show conversion error from API |
| Network error | Suggest retry |
| Build failed | Analyze error, offer to help fix, or publish source as-is |
| Missing dependencies | Run `[pm] install` first |
| Config error | Check framework config files |
| Screenshot failed | Skip coverImage, proceed without it |
| agent-browser not installed | Run `npm install -g agent-browser && agent-browser install` |
| agent-browser Chromium missing | Run `agent-browser install` (or `--with-deps` on Linux) |
| Tags fetch failed | Use expired cache if available, or skip tag matching |
| Image upload failed | Skip coverImage, proceed without it |

## Authorization

The script handles authorization automatically:
- First run opens browser for user to authorize
- Token is saved for future use
- On 401/403 errors, token is cleared and user needs to re-authorize on next run

## Notes

- Always analyze content before publishing to generate meaningful title/description
- Never use directory names as title - they are often meaningless
- Confirm with user before executing publish
- Default hub is https://staging.myvibe.so/
- Local build detection is preprocessing only; server has its own build pipeline
- Be conservative: if project type is uncertain, publish as-is and let server handle
- `--dir` specifies target directory and requires full metadata analysis
- `--file` specifies single file and also requires metadata analysis and screenshot generation
- Build detection should not block publishing
- Tags are cached locally for 7 days to avoid repeated API calls
- All auto-detected metadata should be shown as "suggestions" - user can modify
- If screenshot fails, skip coverImage and let server auto-generate
- Use config file method when publishing with extended metadata (tags, coverImage, etc.)
