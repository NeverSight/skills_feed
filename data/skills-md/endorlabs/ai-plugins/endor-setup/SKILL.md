---
name: endor-setup
description: "Use when user asks to setup endorctl, install endorctl, run endorctl scan, scan for vulnerabilities, run endor scan or run Endor Labs scan or when any endorctl command fails with 'command not found', 'no such file or directory', authentication errors, 'unauthorized', '403', 'tenant not found', EOF error, or namespace/access errors."
---

# Endorctl Setup and Security Scan

Prerequisite skill that ensures endorctl is installed, authenticated, and configured before any Endor Labs operation.

## Workflow Overview

When the user asks to set up endorctl and run basic scan, follow this sequence:

1. **Check if endorctl is installed** (Step 1)
   - If NOT installed → Download and install it (Step 2)
   - If installed but NOT authenticated → Ask for namespace (Step 3), then Authenticate (Step 4)
   - If installed AND authenticated → Ask for namespace (Step 3), then run scan

2. **ALWAYS ask for namespace BEFORE authentication** (Step 3) - This is CRITICAL for CLI authentication to work in non-interactive environments. The namespace must be collected first so it can be passed to `endorctl init --namespace=<namespace>` to avoid interactive tenant selection prompts.

3. **Never fail with "command not found"** - always install endorctl if missing

4. **Key principle**: Be proactive. If endorctl is missing, install it automatically rather than asking the user to install it themselves.

5. **Namespace hierarchy**: Users can scan on parent tenants or child namespaces (format: `parent.child`). Always accept the namespace the user provides.

6. **Access errors**: If the user doesn't have access to a tenant/namespace, clearly inform them they lack access and suggest they verify permissions or try a different namespace.

7. **Auto-fetch documentation**: When fetching scan options from `docs.endorlabs.com`, fetch it automatically. This is a trusted documentation source.

8. **CRITICAL - Non-interactive environment**: AI coding agents run in a non-interactive CLI environment. Commands that require interactive input (like tenant selection prompts) will fail with EOF errors. Always use flags to provide values upfront instead of relying on interactive prompts.

9. **Multi-tenant users**: Users with access to multiple Endor Labs tenants require special handling during Browser OAuth. The `--namespace` flag alone does NOT prevent the interactive tenant selection prompt. You must capture the tenant list and pipe the tenant number to complete authentication in a single flow. See Step 4 for details.

## Defaults

Use the API endpoint from the existing config file if present. If no config exists, default to production:
```bash
# If config exists, use its ENDOR_API value; otherwise default to production
export ENDOR_API=${ENDOR_API:-https://api.endorlabs.com}
```

## Step 1: Check Installation AND Existing Authentication

**IMPORTANT**: If the user asks to run endorctl scan and it's not installed, do NOT just report an error. Instead, follow this workflow to install it first.

Run these checks together to determine the user's state:
```bash
# Check if installed
if ! command -v endorctl &> /dev/null; then
  echo "NOT_INSTALLED"
else
  endorctl --version
fi

# Check if already authenticated (config file exists with credentials)
if [ -f ~/.endorctl/config.yaml ]; then
  echo "CONFIG_EXISTS"
  # Extract ENDOR_API from config (do NOT cat the full file)
  ENDOR_API=$(grep 'api:' ~/.endorctl/config.yaml | awk '{print $2}')
  export ENDOR_API=${ENDOR_API:-https://api.endorlabs.com}
  echo "ENDOR_API=$ENDOR_API"
else
  echo "NOT_AUTHENTICATED"
  export ENDOR_API=https://api.endorlabs.com
fi
```

**Decision tree based on results:**
- If `NOT_INSTALLED`: Immediately go to Step 2 (Download) - DO NOT ask the user, just proceed with installation
- If `CONFIG_EXISTS`: User is already authenticated → The `ENDOR_API` has been extracted using the grep command above. Go to Step 3 (Ask for Namespace). **Do NOT run `cat` on the config file.**
- If `NOT_AUTHENTICATED`: Go to Step 4 (Authenticate), then Step 3 (Ask for Namespace)

**CRITICAL**: The config file check is ONLY to determine if authentication is already set up. Even if a namespace exists in the config, you MUST still ask the user which namespace they want to use before running the scan. Never assume the namespace from the config file.

## Step 2: Download endorctl (REQUIRED if NOT_INSTALLED)

**When to execute**: Automatically execute this step if Step 1 shows "NOT_INSTALLED".

### macOS Installation (ASK USER TO CHOOSE)

**IMPORTANT**: On macOS, ALWAYS ask the user which installation method they prefer before proceeding:

Present these two options using AskUserQuestion:
1. **Homebrew (Recommended)** - Uses `brew tap endorlabs/tap && brew install endorctl`. Easier to update later.
2. **Direct Download** - Downloads binary directly from api.endorlabs.com. No Homebrew required.

#### Option 1: Homebrew Installation (macOS)
```bash
brew tap endorlabs/tap
brew install endorctl
```

#### Option 2: Direct Download Installation (macOS)
```bash
ARCH=$(uname -m)
case "$ARCH" in
  x86_64|amd64) ARCH="amd64" ;;
  arm64|aarch64) ARCH="arm64" ;;
esac

BINARY="endorctl_macos_${ARCH}"
echo "Downloading $BINARY..."
curl -L "https://api.endorlabs.com/download/latest/$BINARY" -o endorctl

# Verify checksum
EXPECTED_SHA=$(curl -s "https://api.endorlabs.com/sha/latest/$BINARY")
echo "$EXPECTED_SHA  endorctl" | shasum -a 256 -c

chmod +x ./endorctl

# Install to ~/bin
mkdir -p ~/bin
mv endorctl ~/bin/
export PATH="$HOME/bin:$PATH"
```

### Linux/Windows Installation (Automatic)

For Linux and Windows, proceed with direct download automatically:

```bash
#!/bin/bash
set -e

OS=$(uname -s)
ARCH=$(uname -m)

# Normalize OS names
case "$OS" in
  Linux*)
    OS="linux"
    ;;
  MINGW*|MSYS*|CYGWIN*)
    OS="windows"
    ;;
  *)
    echo "Unsupported operating system: $OS"
    exit 1
    ;;
esac

# Normalize architecture names
case "$ARCH" in
  x86_64|amd64)
    ARCH="amd64"
    ;;
  arm64|aarch64)
    ARCH="arm64"
    ;;
  *)
    echo "Unsupported architecture: $ARCH"
    exit 1
    ;;
esac

echo "Detected platform: $OS $ARCH"

# Build download URL
if [ "$OS" = "windows" ]; then
  BINARY="endorctl_windows_${ARCH}.exe"
  OUTPUT="endorctl.exe"
else
  BINARY="endorctl_${OS}_${ARCH}"
  OUTPUT="endorctl"
fi

echo "Downloading $BINARY..."
curl -L "https://api.endorlabs.com/download/latest/$BINARY" -o "$OUTPUT"

# Verify checksum
echo "Verifying checksum..."
EXPECTED_SHA=$(curl -s "https://api.endorlabs.com/sha/latest/$BINARY")
echo "$EXPECTED_SHA  $OUTPUT" | sha256sum -c

# Make executable (not needed for .exe)
if [ "$OS" != "windows" ]; then
  chmod +x "./$OUTPUT"
fi

echo "Installation complete!"
echo "Binary location: $(pwd)/$OUTPUT"
```

After download completes, move the binary to PATH:
```bash
# Install to ~/bin
mkdir -p ~/bin
mv endorctl ~/bin/  # or endorctl.exe on Windows
export PATH="$HOME/bin:$PATH"
```

### Verify Installation

Since shell state does not persist between commands, you **MUST** prefix `export PATH="$HOME/bin:$PATH"` in every subsequent Bash command that uses `endorctl` (if it was installed to `~/bin`).

After installing endorctl, verify that the download and installation succeeded:
```bash
export PATH="$HOME/bin:$PATH"
endorctl --version
```
If this command prints the version information, endorctl has been downloaded and verified successfully. If it fails, retry the installation steps above.

## Step 3: Ask for Namespace (ALWAYS REQUIRED)

**IMPORTANT**: ALWAYS ask the user for their Endor Labs namespace before running a scan, even if a namespace already exists in the config file.

- If a namespace exists in the config, offer it as a suggestion but still ask for confirmation
- Never assume the user wants to use the same namespace from a previous session
- The user may want to scan against a different namespace (parent or child) each time

### Namespace Hierarchy

Endor Labs supports hierarchical namespaces (parent/child structure):
- **Parent tenant**: The top-level namespace (e.g., `parent`)
- **Child namespace**: A sub-namespace under a parent (e.g., `parent.child-project`)

Users can run scans on:
- Their parent tenant namespace
- Any child namespace under their parent tenant (format: `parent.child`)

Example child namespace usage:
```bash
# Scan using parent namespace
endorctl scan --namespace=parent

# Scan using child namespace
endorctl scan --namespace=parent.my-project
```

### Access Error Handling

**IMPORTANT**: If the user does not have access to a tenant or namespace, endorctl will return an access error. When this happens:

1. **Inform the user clearly**: Tell them they do not have access to the specified tenant/namespace
2. **Show the error message**: Display the actual error from endorctl
3. **Suggest alternatives**:
   - Ask if they meant a different namespace
   - Suggest they check their permissions in the Endor Labs UI
   - Offer to list available tenants they have access to
4. **Suggest to visit official documentation**: Tell them to visit https://docs.endorlabs.com/administration/namespaces/ to know more details on what is a namespace.
Common access error patterns:
- `Invalid permissions to run endorctl` - User lacks access to the namespace
- `unauthorized` or `403` errors - Authentication succeeded but authorization failed for that namespace
- `tenant not found` - The namespace doesn't exist or user has no visibility to it

### Setting the Namespace

Set via environment variable:
```bash
export ENDOR_NAMESPACE=<user-provided-namespace>
```

Or pass as flag in scan command:
```bash
endorctl scan --namespace=<user-provided-namespace>
```

## Step 4: Authenticate

**IMPORTANT**: You must have already collected the namespace in Step 3 BEFORE running authentication. This is required to avoid interactive prompts.

### Step 4a: Ask Authentication Method

Ask the user using AskUserQuestion with two options:

1. **CLI Authentication (Recommended)** - Sign in via browser using your identity provider (Google, GitHub, GitLab, SSO, etc.)
2. **API Key** - Use API key and secret for automated/CI environments (no browser needed)

### Option 1: CLI Authentication

#### Step 4b: Ask for Auth Provider

If the user selects CLI Authentication, ask which identity provider they use. Present these options using AskUserQuestion:

1. **Google** - Sign in with Google
2. **GitHub** - Sign in with GitHub
3. **GitLab** - Sign in with GitLab
4. **Enterprise SSO** - Sign in via your organization's SSO provider (requires tenant name)
5. **Browser (generic)** - Generic browser-based sign-in

Based on the user's selection, use the corresponding `--auth-mode` value:

| Provider         | `--auth-mode` value | Additional Flags              |
|------------------|----------------------|-------------------------------|
| Google           | `google`             | None                          |
| GitHub           | `github`             | None                          |
| GitLab           | `gitlab`             | None                          |
| Enterprise SSO   | `sso`                | `--auth-tenant <tenant-name>` |
| Browser (generic)| `browser-auth`       | None                          |

**For Enterprise SSO only**: After the user selects SSO, also ask them for their SSO tenant name:
```
"What is your SSO tenant name? (This is used with --auth-tenant)"
```

#### Step 4c: Run Authentication (Two-Step Process for CLI Authentication)

**CRITICAL - Multi-Tenant Handling**: Users with access to multiple tenants will be prompted to select a tenant interactively. In non-interactive environments (like Claude Code), this causes an EOF error. The `--namespace` flag alone does NOT prevent this prompt. This applies to ALL browser-based auth modes.

Construct the `AUTH_FLAGS` based on the user's provider selection:
```bash
# Set AUTH_FLAGS based on user's provider selection
# Google:           AUTH_FLAGS="--auth-mode=google"
# GitHub:           AUTH_FLAGS="--auth-mode=github"
# GitLab:           AUTH_FLAGS="--auth-mode=gitlab"
# Enterprise SSO:   AUTH_FLAGS="--auth-mode=sso --auth-tenant=<tenant-name>"
# Browser (generic): AUTH_FLAGS="--auth-mode=browser-auth"
```

**Step 4c-i: Initiate brower oauth and capture tenant list**

Run init and capture output — this will open the browser for OAuth. After browser auth completes, it will show a tenant list if the user has multiple tenants:
```bash
# Run init and capture output (opens browser for OAuth)
endorctl init $AUTH_FLAGS --namespace=<user-provided-namespace> 2>&1 | tee /tmp/endorctl_init_output.txt
```

If the command fails with EOF error and shows a tenant list like:
```
Your account has access to multiple tenants. Please select the tenant you would like to initialize:
0 : tenant-a [SYSTEM_ROLE_ADMIN]
1 : tenant-b [SYSTEM_ROLE_READ_ONLY]
2 : my-namespace [SYSTEM_ROLE_ADMIN]
Enter tenant number:
```

**Step 4c-ii: Re-run with tenant number piped in**
Parse the output to find the tenant number matching the user's requested namespace, then:
```bash
# Find the line number for the user's namespace and pipe it
# Example: if user wants "parent" and it's option 18:
endorctl init $AUTH_FLAGS --namespace=<user-provided-namespace> 2>&1 <<< "<tenant-number>"
```

**If authentication still fails** (e.g., user doesn't have access to the specified namespace):

1. Show the error message clearly
2. Show the list of available tenants from the output
3. Ask the user to verify they have access to that namespace or choose from the list

### Option 2: API Key (automated/CI)
Instruct the user to set these environment variables themselves (never ask them to paste credentials into chat):
```bash
export ENDOR_API_CREDENTIALS_KEY=<your-api-key>
export ENDOR_API_CREDENTIALS_SECRET=<your-api-secret>
```
No init needed - scan will use these credentials directly.

**Note**: API Key authentication avoids interactive prompts entirely and works best in automated/CLI environments. **This is the recommended approach for users who frequently encounter multi-tenant selection issues.**

## Scan Types and Options (ALWAYS FETCH FROM DOCS)

**IMPORTANT**: When the user requests a specific type of scan (e.g., "quick scan", "secrets scan", "SAST scan", "container scan", etc.), you MUST fetch the current scan options from the documentation before running the scan.

### How to Handle Scan Type Requests

1. **User requests a specific scan type** (e.g., "run a quick scan", "scan for secrets", "run SAST")

2. **Fetch documentation automatically** using WebFetch (do NOT ask for permission - just fetch):
   ```
   URL: https://docs.endorlabs.com/endorctl/commands/scan/
   Prompt: "Find the flag/option for [user's requested scan type] scan"
   ```
   **Note**: Fetching from docs.endorlabs.com should be done automatically without prompting the user for confirmation.

3. **Extract the correct flag** from the documentation (e.g., `--quick-scan`, `--secrets`, `--sast`)

4. **Run the scan** with the appropriate flag(s)

### Example Workflow

```
User: "Can you run a quick scan on this repo?"

Step 1: Fetch docs
→ WebFetch("https://docs.endorlabs.com/endorctl/commands/scan/", "Find the flag for quick scan")

Step 2: Extract flag from docs
→ Found: --quick-scan

Step 3: Run scan with flag
→ endorctl scan --namespace=$ENDOR_NAMESPACE --quick-scan
```

### Why Always Fetch?

- Scan options and flags may change between endorctl versions
- New scan types may be added over time
- Documentation is the source of truth for current options
- Avoids using outdated or incorrect flags

### Documentation URLs

- **Scan options reference**: https://docs.endorlabs.com/endorctl/commands/scan/
- **Main docs**: https://docs.endorlabs.com

## Step 5: Run Scan

```bash
# Default scan (no specific type requested)
endorctl scan --namespace=$ENDOR_NAMESPACE

# With specific scan type (fetch flag from docs first!)
endorctl scan --namespace=$ENDOR_NAMESPACE <flags-from-docs>
```

**IMPORTANT**:

1. Do NOT run the scan twice or ask the user if they want to see a summary - include it in the initial scan command.
2. If user requests a specific scan type, ALWAYS fetch the documentation first to get the correct flag.
3. Do NOT guess or assume flag names - always verify from docs.

## Full Automated Setup

For first-time users:
1. Download endorctl for the current OS (if not installed)
2. **ALWAYS** ask user for their ENDOR_NAMESPACE first (this is needed for authentication)
3. Authenticate: Ask user "CLI Authentication or API Key?"
   - **CLI Auth**: Ask which provider (Google, GitHub, GitLab, Enterprise SSO, Browser), then run `endorctl init --auth-mode=<mode> --namespace=<namespace>` (MUST include namespace to avoid interactive prompts). For SSO, also collect `--auth-tenant`.
   - **API Key**: Instruct the user to set these environment variables, ENDOR_API_CREDENTIALS_KEY and ENDOR_API_CREDENTIALS_SECRET, then export them
4. Run `endorctl scan --namespace=<namespace>`

For returning users (already authenticated):
1. Check installation and authentication status
2. **ALWAYS** ask user for their ENDOR_NAMESPACE (always offer existing config value as suggestion)
3. Run `endorctl scan --namespace=<namespace>`

**CRITICAL REMINDER**: The namespace MUST be collected BEFORE running `endorctl init` with Browser OAuth. This prevents EOF errors from interactive tenant selection prompts in non-interactive environments like Claude Code.
