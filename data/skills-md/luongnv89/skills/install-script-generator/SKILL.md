---
name: install-script-generator
version: 2.0.0
description: |
  Generate cross-platform installation scripts for any software, library, or module. Use when users ask to "create an installer", "generate installation script", "automate installation", "setup script for X", "install X on any OS", or need automated deployment across Windows, Linux, and macOS. The skill generates a standalone `install.sh` (and optionally `install.ps1`) script that can be run via a single curl/wget one-liner from GitHub raw user content. It follows a four-phase approach: (1) Environment exploration - detect OS, gather system info, check dependencies; (2) Installation planning - propose steps with verification; (3) Script generation - produce a self-contained install script with one-liner command; (4) Documentation generation.
---

# Install Script Generator

Generate robust, cross-platform installation scripts that users can run with a **single bash command** via GitHub raw URLs.

## Primary Goal

Generate a **self-contained `install.sh`** script that:
1. Detects the user's OS, architecture, and package manager automatically
2. Installs all dependencies and the target software
3. Verifies the installation
4. Can be executed via a **one-liner** using GitHub raw user content:

```bash
curl -sSL https://raw.githubusercontent.com/<owner>/<repo>/<branch>/install.sh | bash
```

or with wget:

```bash
wget -qO- https://raw.githubusercontent.com/<owner>/<repo>/<branch>/install.sh | bash
```

## Workflow

### Phase 1: Environment Exploration

Before generating the script, understand the project context:

1. **Identify the target** — What software/module/tool is being installed?
2. **Check the repository** — Look for existing build files, `Makefile`, `package.json`, `setup.py`, `Cargo.toml`, `go.mod`, etc.
3. **Identify dependencies** — What does the software need to build/run?
4. **Determine the GitHub repo** — The `<owner>/<repo>` for the raw URL (check git remote or ask user)

Run the environment explorer for local testing:

```bash
python3 scripts/env_explorer.py
```

The script detects:
- Operating system (Windows/Linux/macOS) and version
- CPU architecture (x86_64, ARM64, etc.)
- Package managers available (apt, yum, brew, choco, winget)
- Shell environment (bash, zsh, powershell, cmd)
- Existing dependencies and versions
- User permissions (admin/sudo availability)

### Phase 2: Installation Planning

Based on the environment analysis and target software:

1. **Identify dependencies** — List all required packages/libraries
2. **Check existing installations** — Avoid reinstalling what exists
3. **Order operations** — Resolve dependency graph
4. **Add verification steps** — Each step must be verifiable
5. **Plan rollback** — Define cleanup on failure

Use the plan generator for structured planning:

```bash
python3 scripts/plan_generator.py --target "<software_name>" --env-file env_info.json
```

### Phase 3: Script Generation (Primary Output)

Generate a **self-contained `install.sh`** script at the project root. The script MUST follow this structure:

```bash
#!/usr/bin/env bash
set -euo pipefail

# ============================================================================
# <Software Name> Installer
# Usage: curl -sSL https://raw.githubusercontent.com/<owner>/<repo>/<branch>/install.sh | bash
# ============================================================================

# --- Configuration ---
TOOL_NAME="<software_name>"
REPO_OWNER="<owner>"
REPO_NAME="<repo>"
DEFAULT_BRANCH="<branch>"
INSTALL_PREFIX="${INSTALL_PREFIX:-/usr/local}"

# --- Color Output ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

info()  { printf "${BLUE}[INFO]${NC}  %s\n" "$*"; }
ok()    { printf "${GREEN}[ OK ]${NC}  %s\n" "$*"; }
warn()  { printf "${YELLOW}[WARN]${NC}  %s\n" "$*"; }
err()   { printf "${RED}[ERR ]${NC}  %s\n" "$*" >&2; }
die()   { err "$@"; exit 1; }

# --- OS / Arch Detection ---
detect_os() {
    local os
    os="$(uname -s | tr '[:upper:]' '[:lower:]')"
    case "$os" in
        linux*)  echo "linux" ;;
        darwin*) echo "macos" ;;
        mingw*|msys*|cygwin*) echo "windows" ;;
        *)       die "Unsupported operating system: $os" ;;
    esac
}

detect_arch() {
    local arch
    arch="$(uname -m)"
    case "$arch" in
        x86_64|amd64)  echo "x86_64" ;;
        aarch64|arm64) echo "arm64" ;;
        armv7l)        echo "armv7" ;;
        *)             die "Unsupported architecture: $arch" ;;
    esac
}

detect_package_manager() {
    if command -v apt-get &>/dev/null; then echo "apt"
    elif command -v dnf &>/dev/null; then echo "dnf"
    elif command -v yum &>/dev/null; then echo "yum"
    elif command -v pacman &>/dev/null; then echo "pacman"
    elif command -v brew &>/dev/null; then echo "brew"
    elif command -v zypper &>/dev/null; then echo "zypper"
    else echo "unknown"
    fi
}

need_sudo() {
    if [ "$(id -u)" -ne 0 ]; then
        if command -v sudo &>/dev/null; then
            echo "sudo"
        else
            die "This script requires root privileges. Please run as root or install sudo."
        fi
    else
        echo ""
    fi
}

# --- Dependency Installation ---
install_deps() {
    local pm="$1"
    local sudo_cmd="$2"
    shift 2
    local deps=("$@")

    [ ${#deps[@]} -eq 0 ] && return 0

    info "Installing dependencies: ${deps[*]}"
    case "$pm" in
        apt)    $sudo_cmd apt-get update -qq && $sudo_cmd apt-get install -y -qq "${deps[@]}" ;;
        dnf)    $sudo_cmd dnf install -y -q "${deps[@]}" ;;
        yum)    $sudo_cmd yum install -y -q "${deps[@]}" ;;
        pacman) $sudo_cmd pacman -Sy --noconfirm "${deps[@]}" ;;
        brew)   brew install "${deps[@]}" ;;
        zypper) $sudo_cmd zypper install -y "${deps[@]}" ;;
        *)      die "Cannot install dependencies: unsupported package manager '$pm'" ;;
    esac
    ok "Dependencies installed"
}

# --- Main Installation Logic ---
install_<tool>() {
    # ... tool-specific installation steps ...
    # This section is customized per target software
    :
}

# --- Verification ---
verify_installation() {
    info "Verifying installation..."
    if command -v "$TOOL_NAME" &>/dev/null; then
        ok "$TOOL_NAME $(${TOOL_NAME} --version 2>/dev/null || echo '') installed successfully"
    else
        die "$TOOL_NAME installation could not be verified"
    fi
}

# --- Entry Point ---
main() {
    info "Installing $TOOL_NAME"
    info "============================================"

    local os arch pm sudo_cmd
    os="$(detect_os)"
    arch="$(detect_arch)"
    pm="$(detect_package_manager)"
    sudo_cmd="$(need_sudo)"

    info "OS: $os | Arch: $arch | Package Manager: $pm"

    # Install dependencies (customize per target)
    # install_deps "$pm" "$sudo_cmd" dep1 dep2 dep3

    # Install the tool
    install_<tool>

    # Verify
    verify_installation

    info "============================================"
    ok "Installation complete!"
    info "Run '$TOOL_NAME --help' to get started."
}

main "$@"
```

#### Script Requirements

The generated `install.sh` MUST:
- Start with `#!/usr/bin/env bash` and `set -euo pipefail`
- Be fully self-contained (no external script dependencies)
- Auto-detect OS (Linux, macOS, Windows/MSYS), architecture, and package manager
- Handle `sudo` gracefully (detect if needed, fail with clear message if unavailable)
- Use colored output for readability
- Verify the installation at the end
- Exit with non-zero code on any failure
- Include the one-liner command in the header comment
- Support `INSTALL_PREFIX` environment variable override where applicable

#### Optional: Windows Support

If Windows support is needed, also generate `install.ps1`:

```powershell
# Usage: irm https://raw.githubusercontent.com/<owner>/<repo>/<branch>/install.ps1 | iex
```

### Phase 4: Documentation Generation

After generating the install script, update the project's README (or generate a section) with the one-liner:

**Example output for README:**

````markdown
## Installation

### Quick Install (one command)

```bash
curl -sSL https://raw.githubusercontent.com/<owner>/<repo>/main/install.sh | bash
```

Or with wget:

```bash
wget -qO- https://raw.githubusercontent.com/<owner>/<repo>/main/install.sh | bash
```

### Advanced Options

```bash
# Install to a custom prefix
INSTALL_PREFIX=~/.local curl -sSL https://raw.githubusercontent.com/<owner>/<repo>/main/install.sh | bash

# Download and inspect before running
curl -sSL https://raw.githubusercontent.com/<owner>/<repo>/main/install.sh -o install.sh
less install.sh  # review the script
bash install.sh
```
````

Also generate the full usage documentation:

```bash
python3 scripts/doc_generator.py --target "<software_name>" --plan installation_plan.yaml
```

## Output Files

The skill generates these files:

| File | Description |
|------|-------------|
| `install.sh` | **Primary output** — standalone install script for `curl \| bash` |
| `install.ps1` | *(Optional)* Windows PowerShell installer |
| `env_info.json` | System environment analysis (local testing) |
| `installation_plan.yaml` | Detailed installation steps |
| `USAGE_GUIDE.md` | User documentation |

## Determining the GitHub Raw URL

To construct the one-liner URL, the skill needs:

1. **Repository owner and name** — Check `git remote -v` for origin URL, or ask the user
2. **Branch** — Default to `main`, check with `git branch --show-current`
3. **File path** — `install.sh` at the repo root

The raw URL format is:
```
https://raw.githubusercontent.com/<owner>/<repo>/<branch>/install.sh
```

If the repo uses a non-standard structure (e.g., the script is in a subdirectory), adjust the path:
```
https://raw.githubusercontent.com/<owner>/<repo>/<branch>/path/to/install.sh
```

## Platform-Specific Notes

### Windows
- Prefer `winget` over `choco` when available
- Use PowerShell for script execution (`install.ps1`)
- Handle UAC elevation requirements
- One-liner: `irm https://raw.githubusercontent.com/<owner>/<repo>/main/install.ps1 | iex`

### Linux
- Detect distro family (Debian/RedHat/Arch)
- Use appropriate package manager
- Handle sudo requirements gracefully
- Support both `curl` and `wget` for the one-liner

### macOS
- Use Homebrew as primary package manager
- Handle Apple Silicon vs Intel differences
- Respect Gatekeeper and notarization

## Example Usage

### Example 1: "Create an install script for this project"

1. Detect the project type (e.g., Python package, Go binary, Node module)
2. Check `git remote -v` to get `<owner>/<repo>`
3. Generate `install.sh` with proper dependency installation and build steps
4. Output the one-liner command for the README

### Example 2: "Generate a curl install command for my CLI tool"

1. Analyze the project's build system
2. Generate `install.sh` that downloads the latest release binary or builds from source
3. Include architecture detection for pre-built binaries
4. Output: `curl -sSL https://raw.githubusercontent.com/user/tool/main/install.sh | bash`

### Example 3: "Make my module installable with a single command"

1. Check for existing `Makefile`, `setup.py`, `package.json`, etc.
2. Generate `install.sh` that wraps the build/install process
3. Add dependency installation (compilers, libraries, runtimes)
4. Verify the module is available after install

## Error Handling

- All scripts exit with non-zero codes on failure (`set -e`)
- Each step logs what it's doing before execution
- Failed dependency installs show the exact missing package and package manager
- Verification failure at the end gives clear remediation steps
- Colored output makes errors easy to spot in terminal
