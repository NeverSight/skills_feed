---
name: get-started
description: Get started with Novita Skills. Use when user wants to know what skills are available, needs help installing team skills, wants to contribute new skills, asks about team capabilities, or needs recommendations for which skills to install. Provides an overview of all team skills, contribution guidelines, and helps users discover and install the right skills.
---

# Get Started with Novita Skills

Your complete guide to discovering, installing, and contributing to team skills.

## Overview

This skill serves as the entry point to the Novita Skills repository, allowing you to:
- 📋 View all available team skills
- 🎯 Get skill recommendations based on your needs
- 📦 Quickly install required skills
- 🌟 Discover recommended public community skills
- 🔧 Detect and configure local development environment

## Available Team Skills

### 🤖 novita-docs
**Purpose**: Comprehensive Novita AI platform reference
**Use Cases**:
- Questions about any Novita AI product (Model APIs, GPU Instance, Serverless GPUs, Agent Sandbox)
- Need API usage guides and code examples
- Query pricing, features, and integration information
- Design system questions (colors, typography, buttons, navigation, icons, logo)
- Understanding Novita's capabilities and services

**Installation**:
```bash
npx skills add jaxzhang-svg/novita-skills --skill novita-docs
```

**Included Reference Documentation**:
- Product docs: brand.md, getting-started.md, model-apis.md, gpu-instance.md, serverless-gpus.md, agent-sandbox.md
- API reference: api-reference.md, integrations.md
- Design system: overview.md, typography.md, colors.md, buttons.md, navigation.md, icons.md, logo.md
- Other: resources.md, competitors-and-partners.md

### 🚨 x-crisis-monitor
**Purpose**: X (Twitter) crisis monitoring and management
**Use Cases**:
- Monitor brand sentiment and reputation on X
- Handle negative publicity and PR crises
- Manage social media crisis response
- Analyze public opinion trends
- Develop social media crisis response strategies

**Installation**:
```bash
npx skills add jaxzhang-svg/novita-skills --skill x-crisis-monitor
```

**Included Resources**:
- Keyword library: keyword-library.md (brand names, negative sentiment words, industry-specific terms)
- Decision tree: decision-tree.md (crisis level assessment framework)
- Response templates: response-templates.md (response templates for various crisis levels)
- Case studies: case-studies.md (historical crisis case analyses)
- Checklists: checklist.md (monitoring and response workflows)
- Post-mortem: post-mortem-template.md (crisis review template)

## Recommended Use Cases

### When you need to...

#### Develop Novita-related Projects
→ Install `novita-docs`
- Integrate Novita API
- Build applications using Novita services
- Follow Novita design system
- Understand product features and limitations

#### Social Media Monitoring and Crisis Management
→ Install `x-crisis-monitor`
- Monitor brand reputation
- Quickly respond to negative sentiment
- Execute crisis management processes
- Conduct post-crisis analysis and improvement

#### Comprehensive Team Capabilities
→ Install all skills
```bash
npx skills add jaxzhang-svg/novita-skills --skill '*'
```

## Environment Detection and Configuration

Many skills depend on Python or Node.js environments. Before installing skills, ensure your system is configured with these tools.

### Detect Current Environment

Run the following commands to check your environment:

```bash
# Check Python
python3 --version || python --version

# Check Node.js
node -v

# Check npm
npm -v
```

### Install Python Environment (via uv)

If you don't have Python or need a better Python package manager, we recommend using **uv** (a modern Python package manager):

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# After installation, restart your terminal or run
source $HOME/.cargo/env

# Verify installation
uv --version

# Use uv to install Python (if needed)
uv python install 3.12

# Use uv to create a virtual environment
uv venv

# Activate the virtual environment
source .venv/bin/activate  # macOS/Linux
```

**Why choose uv?**
- ⚡ Extremely fast package installation (10-100x faster than pip)
- 🔒 Better dependency resolution and locking
- 🎯 Unified Python version and package management
- 🚀 Written in Rust, excellent performance

### Install Node.js Environment (via nvm)

If you don't have Node.js, we recommend using **nvm** (Node Version Manager) for installation:

```bash
# 1. Download and install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash

# 2. Restart your terminal or run the following command to load nvm
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# 3. Install the latest LTS version of Node.js
nvm install 24

# 4. Set default version
nvm alias default 24

# 5. Verify installation
node -v   # Should show v24.x.x
npm -v    # Should show 11.x.x
```

**Why choose nvm?**
- 🔄 Easily switch between different Node.js versions
- 📦 Each project can use a different Node version
- 🎯 No sudo permission needed to install global packages
- 🛡️ Avoid system-level Node.js version conflicts

### Environment Configuration Checklist

Before installing skills, ensure the following conditions are met:

- [ ] **Python 3.10+** or **uv** installed
- [ ] **Node.js 18+** installed
- [ ] **npm or pnpm** package manager available
- [ ] **curl** command available (for downloading installation scripts)
- [ ] Terminal has network access

### Common Environment Issues

#### macOS Users
```bash
# If curl is not available, install via Homebrew
brew install curl

# If you encounter permission issues, ensure you're not using system-level Python/Node
which python3  # Should point to ~/.local/bin or virtual environment
which node     # Should point to ~/.nvm directory
```

#### Linux Users
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install curl

# Ensure bash or zsh configuration files are updated
# nvm and uv paths should be in ~/.bashrc or ~/.zshrc
```

#### Windows Users
We recommend using WSL2 (Windows Subsystem for Linux) or Git Bash, then follow the Linux installation method.

### Verify Environment Configuration

Run the following commands to ensure all tools are working properly:

```bash
# Complete environment check
echo "=== Python ==="
python3 --version 2>/dev/null || echo "Python not found"
uv --version 2>/dev/null || echo "uv not found"

echo -e "\n=== Node.js ==="
node -v 2>/dev/null || echo "Node.js not found"
npm -v 2>/dev/null || echo "npm not found"
nvm --version 2>/dev/null || echo "nvm not found"

echo -e "\n=== Tools ==="
curl --version 2>/dev/null | head -n 1 || echo "curl not found"
```

**If all checks pass, you're ready to start installing and using skills!** 🎉

## Recommended Community Skills

Looking for more skills to enhance your workflow? We've curated a comprehensive list of high-quality skills from Anthropic and other providers.

**See**: [Recommended Skills Guide](references/recommended-skills.md)

**Quick picks**:
- **Design & Frontend**: frontend-design, canvas-design, brand-guidelines
- **Development Tools**: skill-creator, mcp-builder, webapp-testing
- **Document Processing**: pdf, pptx, xlsx, docx
- **And many more...**

```bash
# Install any Anthropic skill
npx skills add anthropics/skills --skill <skill-name>
```

## Installation Guide

### Basic Installation

```bash
# Install a single skill
npx skills add jaxzhang-svg/novita-skills --skill <skill-name>

# Install multiple skills
npx skills add jaxzhang-svg/novita-skills --skill novita-docs x-crisis-monitor

# Install all skills
npx skills add jaxzhang-svg/novita-skills --skill '*'
```

## FAQ

### Q: Which skills should I install?
A: Choose based on your work:
- Novita product development → `novita-docs`
- Social media management → `x-crisis-monitor`
- Frontend design development → Anthropic's `frontend-design`
- Document processing → Anthropic's `pdf`, `docx`, `xlsx`, `pptx`
- Not sure? Install the get-started skill and ask the AI agent directly

### Q: Do skills affect performance?
A: No. Skills are only loaded when needed and don't continuously occupy resources. However, we recommend keeping installed skills under 50.

### Q: Can I customize or modify skills?
A: Yes! Fork the repository to modify, or submit improvement suggestions to the team.

### Q: What's the difference between skills and regular documentation?
A: Skills are structured knowledge optimized for AI agents, containing clear use cases and trigger conditions, allowing AI to apply knowledge more intelligently.

## Get Help

- 📖 Check the repository [README](../../README.md)
- 💬 Open an issue in the repository
- 🤝 Contact team members
- 🌐 Visit [skills.sh](https://skills.sh/) to learn more

## Command Quick Reference

| Command | Description |
|---------|-------------|
| `npx skills add jax/novita-skills -l` | List all available skills |
| `npx skills add jax/novita-skills --skill '*'` | Install all skills |
| `npx skills list` | View installed skills |
| `npx skills find` | Search for skills |
| `npx skills update` | Update skills |
| `npx skills remove` | Remove skills |

---

Start using team skills to boost your development efficiency! 🚀

---

## Contributing to Team Skills

Want to share your domain knowledge with the team? We welcome your contributions!

**See**: [Complete Contributing Guide](references/CONTRIBUTING.md)

### Quick Start

1. **Create a skill** using Anthropic's skill-creator:
   ```bash
   npx skills add https://github.com/anthropics/skills --skill skill-creator
   ```

2. **Add your skill** to the `skills/` directory

3. **Submit a PR** with your changes

For detailed requirements, submission process, and best practices, refer to the [Contributing Guide](references/CONTRIBUTING.md).

### Get Help

- 💬 Open an issue in the repository
- 📖 Refer to existing skills as examples
- 🤝 Contact team members
- 🎯 Ask the AI agent: "How do I contribute a new skill?"

---

**Thank you for contributing!** 🎉
