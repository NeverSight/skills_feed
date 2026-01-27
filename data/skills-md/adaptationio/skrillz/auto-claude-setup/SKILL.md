---
name: auto-claude-setup
description: Complete Auto-Claude installation and setup guide for all platforms. Use when installing Auto-Claude on WSL, Windows, Linux, or macOS, setting up development environment, or troubleshooting installation issues.
version: 1.0.0
auto-claude-version: 2.7.2
---

# Auto-Claude Setup

Complete installation and environment setup for the Auto-Claude autonomous coding framework.

## Quick Start

### Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python | 3.12+ | Required for backend and Memory Layer |
| Node.js | 24+ | Required for frontend |
| npm | 10+ | Package manager |
| Git | Latest | Version control |
| Claude Pro/Max | Active | Subscription required |
| Claude Code CLI | Latest | `npm install -g @anthropic-ai/claude-code` |

### Installation Methods

#### Method 1: Pre-built Release (Recommended)

Download from [GitHub Releases](https://github.com/AndyMik90/Auto-Claude/releases/latest):

| Platform | Download |
|----------|----------|
| Windows | Auto-Claude-2.7.2.exe |
| macOS (Apple Silicon) | Auto-Claude-2.7.2-arm64.dmg |
| macOS (Intel) | Auto-Claude-2.7.2-x64.dmg |
| Linux (Universal) | Auto-Claude-2.7.2.AppImage |
| Linux (Debian) | Auto-Claude-2.7.2.deb |

#### Method 2: From Source (Development)

```bash
# Clone repository
git clone https://github.com/AndyMik90/Auto-Claude.git
cd Auto-Claude

# Install all dependencies
npm run install:all

# Run in development mode
npm run dev

# Or build and run
npm start
```

## Platform-Specific Setup

### WSL2 (Windows Subsystem for Linux)

```bash
# 1. Ensure WSL2 is updated
wsl --update

# 2. Install Python 3.12
sudo apt update && sudo apt install -y python3.12 python3.12-venv python3.12-dev

# 3. Install Node.js 24+ via nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash
source ~/.bashrc
nvm install 24
nvm use 24

# 4. Clone and setup
git clone https://github.com/AndyMik90/Auto-Claude.git
cd Auto-Claude
npm run install:all

# 5. Setup OAuth token
claude setup-token
```

### Windows (Native)

```powershell
# 1. Install Python 3.12
winget install Python.Python.3.12

# 2. Install Node.js 24
winget install OpenJS.NodeJS.LTS

# 3. Install Claude Code CLI
npm install -g @anthropic-ai/claude-code

# 4. Clone and setup
git clone https://github.com/AndyMik90/Auto-Claude.git
cd Auto-Claude
npm run install:all
```

### Linux (Ubuntu/Debian)

```bash
# 1. Install Python 3.12
sudo apt update
sudo apt install -y python3.12 python3.12-venv python3.12-dev

# 2. Install Node.js 24 via NodeSource
curl -fsSL https://deb.nodesource.com/setup_24.x | sudo -E bash -
sudo apt install -y nodejs

# 3. Install Claude Code CLI
sudo npm install -g @anthropic-ai/claude-code

# 4. Clone and setup
git clone https://github.com/AndyMik90/Auto-Claude.git
cd Auto-Claude
npm run install:all
```

### macOS

```bash
# 1. Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Install Python 3.12 and Node.js
brew install python@3.12 node@24

# 3. Install Claude Code CLI
npm install -g @anthropic-ai/claude-code

# 4. Clone and setup
git clone https://github.com/AndyMik90/Auto-Claude.git
cd Auto-Claude
npm run install:all
```

## Authentication Setup

### OAuth Token Configuration

```bash
# Generate OAuth token (opens browser for authentication)
claude setup-token

# Token is saved to:
# - macOS: Keychain
# - Windows: Credential Manager
# - Linux: ~/.config/claude/credentials
```

### Environment Configuration

Create `apps/backend/.env` from the example:

```bash
cd apps/backend
cp .env.example .env
```

**Required Configuration:**

```bash
# OAuth token (if not using keychain)
CLAUDE_CODE_OAUTH_TOKEN=your-oauth-token-here
```

**Optional Configuration:**

```bash
# Model override (default: claude-opus-4-5-20251101)
AUTO_BUILD_MODEL=claude-opus-4-5-20251101

# Default git branch
DEFAULT_BRANCH=main

# Debug mode
DEBUG=true
DEBUG_LEVEL=2

# Linear integration
LINEAR_API_KEY=lin_api_xxxxx

# Memory system (Graphiti)
GRAPHITI_ENABLED=true
GRAPHITI_LLM_PROVIDER=openai
OPENAI_API_KEY=sk-xxxxx
```

## Verification

### Test Installation

```bash
# Check Python version
python3 --version  # Should be 3.12+

# Check Node.js version
node --version  # Should be 24+

# Check Claude Code CLI
claude --version

# Test backend
cd apps/backend
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
python run.py --help

# Test frontend
cd apps/frontend
npm run dev
```

### Run First Task

```bash
cd apps/backend
source .venv/bin/activate

# Create a spec interactively
python spec_runner.py --interactive

# Or with a task description
python spec_runner.py --task "Add a hello world endpoint"
```

## Project Structure

```
Auto-Claude/
├── apps/
│   ├── backend/           # Python CLI and agents
│   │   ├── agents/        # Agent implementations
│   │   ├── core/          # Client, auth, security
│   │   ├── prompts/       # Agent system prompts
│   │   ├── spec/          # Spec creation pipeline
│   │   ├── .env           # Your configuration
│   │   └── run.py         # Main entry point
│   └── frontend/          # Electron desktop UI
├── guides/                # Documentation
├── tests/                 # Test suite
└── scripts/               # Build utilities
```

## Common Issues

### Windows: node-gyp Errors

Install Visual Studio Build Tools:
1. Download [Visual Studio Build Tools 2022](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. Select "Desktop development with C++" workload
3. Add "MSVC v143 - VS 2022 C++ x64/x86 Spectre-mitigated libs"
4. Restart terminal and run `npm install` again

### Python Version Mismatch

```bash
# Check which Python is being used
which python3
python3 --version

# Create venv with specific Python version
python3.12 -m venv .venv
```

### OAuth Token Issues

```bash
# Re-run token setup
claude setup-token

# Verify token is set
echo $CLAUDE_CODE_OAUTH_TOKEN

# Check Claude Code is working
claude --version
```

## Related Skills

- **auto-claude-cli**: Core CLI operations
- **auto-claude-spec**: Spec creation workflow
- **auto-claude-memory**: Memory system configuration
- **auto-claude-troubleshooting**: Debugging guide

## References

- [Official README](https://github.com/AndyMik90/Auto-Claude/blob/main/README.md)
- [Contributing Guide](https://github.com/AndyMik90/Auto-Claude/blob/main/CONTRIBUTING.md)
- [CLI Usage Guide](https://github.com/AndyMik90/Auto-Claude/blob/main/guides/CLI-USAGE.md)
