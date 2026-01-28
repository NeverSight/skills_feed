---
name: generate-swagger-docs
description: Generate OpenAPI documentation from source code. Analyzes repository to automatically discover API endpoints and create swagger.json and interactive HTML documentation. Use when generating API docs, creating OpenAPI specs, documenting REST APIs, or analyzing API endpoints.
allowed-tools: Bash
---

# Generate Swagger Documentation

Generate OpenAPI docs from your codebase in seconds with automatic API key setup.

## How It Works

This skill automates the Swagger/OpenAPI documentation generation:

1. **API Key Setup** - Accepts your OpenAI API key and sets it as an environment variable
2. **Initialization** - Downloads and sets up the apimesh tool
3. **Automatic Processing** - The tool analyzes your codebase and generates documentation
4. **Output** - Outputs are saved to the apimesh/ directory

## Setup Requirements

You need an OpenAI API key to use this skill. Get one from [OpenAI's platform](https://platform.openai.com/account/api-keys) if you don't have one already.

## Recommended: Quick Setup with API Key

The easiest way to use this skill is to pass your API key directly:

```bash
/Users/ankits/.claude/skills/generate-swagger-docs/generate-with-key.sh "sk-proj-your-api-key-here"
```

This will:
1. Accept your OpenAI API key as an argument
2. Create the `apimesh/` directory and download the apimesh tool
3. Set up the environment variables correctly
4. Generate your Swagger documentation automatically
5. Display the output file locations

## Automatic Flow

When you run this skill:

1. **First Time:** You'll be prompted for your OpenAI API key (starts with `sk-proj-`)
   - The key is saved locally and used for subsequent runs
   - The key is NOT committed to version control

2. **Subsequent Runs:** The skill uses the saved API key automatically
   - No additional prompts for the key unless you clear the config

3. **Framework Detection:** Automatically detects your API framework
   - Supports: Express, NestJS, FastAPI, Django, Rails, Go, and more

## What It Does

- Scans your repository for API endpoints
- Detects the web framework (Django, Flask, FastAPI, Express, NestJS, Rails, Go)
- Generates OpenAPI 3.0 specification (`swagger.json`)
- Creates interactive HTML documentation (`apimesh-docs.html`)

## Output

- `apimesh/swagger.json` - OpenAPI 3.0 spec
- `apimesh/apimesh-docs.html` - Interactive Swagger UI (self-contained, shareable)
- `apimesh/config.json` - Saved configuration (includes your settings, gitignore this file)

## Important Notes

- Your OpenAI API key is needed for the LLM analysis
- The generated `config.json` should be added to `.gitignore` as it contains secrets
- Framework detection is automatic but can be manually specified if needed
- The tool supports both public and private repositories

## API Key Setup Methods

### Method 1: Wrapper Script (Recommended) ✓

Use the provided wrapper script that properly handles environment variable propagation:

```bash
/Users/ankits/.claude/skills/generate-swagger-docs/generate-with-key.sh "sk-proj-your-api-key-here"
```

**Why this works best:**
- Properly passes the API key to the Python subprocess
- No interactive prompts in non-TTY environments
- Handles environment variable propagation correctly
- Provides clear success/error messages

### Method 2: Using Saved Configuration

After the first run with Method 1, your key is saved in `apimesh/config.json`. On subsequent runs, you can omit the key (if you trust your local setup):

```bash
/Users/ankits/.claude/skills/generate-swagger-docs/generate-with-key.sh
```

**Important:** Never commit the `config.json` file to version control. Add it to `.gitignore`.

### Method 3: Manual apimesh Setup

If you need more control, download and run apimesh directly:

```bash
export OPENAI_API_KEY="sk-proj-your-api-key-here"
mkdir -p apimesh && \
  curl -sSL https://raw.githubusercontent.com/qodex-ai/apimesh/refs/heads/main/run.sh -o apimesh/run.sh && \
  chmod +x apimesh/run.sh && \
  cd apimesh && \
  OPENAI_API_KEY="$OPENAI_API_KEY" ./run.sh
```

**Note:** The `OPENAI_API_KEY` must be explicitly passed to the subprocess as shown above.
