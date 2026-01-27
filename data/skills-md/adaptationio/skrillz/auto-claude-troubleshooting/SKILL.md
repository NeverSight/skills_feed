---
name: auto-claude-troubleshooting
description: Auto-Claude debugging and troubleshooting guide. Use when fixing installation issues, debugging build failures, resolving agent errors, or diagnosing performance problems.
version: 1.0.0
auto-claude-version: 2.7.2
---

# Auto-Claude Troubleshooting

Comprehensive debugging guide for all Auto-Claude issues.

## Quick Diagnostics

### Check System Requirements

```bash
# Python version (need 3.12+)
python3 --version

# Node.js version (need 24+)
node --version

# Claude Code CLI
claude --version

# Git
git --version
```

### Verify Installation

```bash
cd apps/backend

# Check virtual environment
source .venv/bin/activate  # or .venv\Scripts\activate
python --version

# Test import
python -c "from core.client import create_client; print('OK')"

# Check dependencies
pip list | grep claude-agent-sdk
```

### Check Configuration

```bash
# Environment variables
cat .env | grep -v "^#" | grep -v "^$"

# OAuth token
echo $CLAUDE_CODE_OAUTH_TOKEN | head -c 20

# Test Claude Code
claude --version
```

## Common Issues

### Installation Problems

#### Python Version Mismatch

```bash
# Wrong Python version
$ python3 --version
Python 3.9.7  # Too old!

# Fix: Install Python 3.12+
# macOS
brew install python@3.12

# Ubuntu
sudo apt install python3.12 python3.12-venv

# Windows
winget install Python.Python.3.12

# Create venv with correct version
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### node-gyp Errors (Windows)

```bash
# Error: node-gyp rebuild failed

# Fix: Install Visual Studio Build Tools
# 1. Download from https://visualstudio.microsoft.com/visual-cpp-build-tools/
# 2. Select "Desktop development with C++"
# 3. Restart terminal
npm install
```

#### Permission Denied

```bash
# Error: Permission denied

# Fix: Use sudo or change ownership
sudo npm install -g @anthropic-ai/claude-code

# Or fix npm permissions
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

### Authentication Issues

#### OAuth Token Invalid

```bash
# Error: Invalid OAuth token

# Fix: Re-generate token
claude setup-token

# Add to .env
echo "CLAUDE_CODE_OAUTH_TOKEN=$(claude setup-token --output)" >> apps/backend/.env
```

#### Token Not Found

```bash
# Error: CLAUDE_CODE_OAUTH_TOKEN not set

# Check if set
echo $CLAUDE_CODE_OAUTH_TOKEN

# Set manually
export CLAUDE_CODE_OAUTH_TOKEN="your-token-here"

# Or add to .env
echo "CLAUDE_CODE_OAUTH_TOKEN=your-token-here" >> apps/backend/.env
```

#### Subscription Issues

```bash
# Error: Claude Pro/Max subscription required

# Fix: Verify subscription at https://claude.ai/upgrade
# Must have active Pro or Max subscription
```

### Build Failures

#### Spec Not Found

```bash
# Error: Spec 001 not found

# List available specs
python run.py --list

# Check spec directory
ls -la .auto-claude/specs/

# Create spec first
python spec_runner.py --interactive
```

#### Agent Timeout

```bash
# Error: Agent timed out

# Increase timeout
API_TIMEOUT_MS=600000 python run.py --spec 001

# Or add to .env
echo "API_TIMEOUT_MS=600000" >> .env
```

#### Build Stuck

```bash
# Build appears stuck

# Check progress
tail -f .auto-claude/specs/001-feature/build-progress.txt

# Check for PAUSE file
ls -la .auto-claude/specs/001-feature/PAUSE

# Remove pause
rm .auto-claude/specs/001-feature/PAUSE

# Add human input to unstick
echo "Please proceed with the next subtask" > .auto-claude/specs/001-feature/HUMAN_INPUT.md
```

#### Security Hook Rejection

```bash
# Error: Command not allowed

# Check security log
cat .auto-claude-security.json

# Add command to allowlist in security.py
# Or run without sandbox (not recommended)
```

### Workspace Issues

#### Worktree Already Exists

```bash
# Error: Worktree already exists

# Remove existing worktree
git worktree remove .worktrees/auto-claude/001-feature

# Or force remove
git worktree remove --force .worktrees/auto-claude/001-feature
git worktree prune
```

#### Branch Already Exists

```bash
# Error: Branch auto-claude/001-feature already exists

# Delete existing branch
git branch -D auto-claude/001-feature

# Then retry
python run.py --spec 001
```

#### Merge Conflicts

```bash
# Error: Merge conflicts detected

# Manual resolution
cd .worktrees/auto-claude/001-feature/
git merge main --no-commit
git status

# Resolve conflicts in editor
code path/to/conflicted/file

# Complete merge
git add .
git commit -m "Resolved conflicts"
cd ../../apps/backend
```

### Memory System Issues

#### Graphiti Not Working

```bash
# Error: Graphiti initialization failed

# Check if enabled
grep GRAPHITI apps/backend/.env

# Verify provider credentials
# For OpenAI
curl -H "Authorization: Bearer $OPENAI_API_KEY" https://api.openai.com/v1/models

# For Ollama
curl http://localhost:11434/api/tags
```

#### Embedding Dimension Mismatch

```bash
# Error: Embedding dimension mismatch

# Clear embeddings and re-index
rm -rf ~/.auto-claude/memories/embeddings
python run.py --spec 001
```

#### Database Corruption

```bash
# Error: Database corrupted

# Backup and reset
mv ~/.auto-claude/memories ~/.auto-claude/memories.backup
python query_memory.py --search "test"  # Creates fresh DB
```

### QA Issues

#### QA Loop Never Completes

```bash
# QA keeps rejecting

# Check QA report
cat .auto-claude/specs/001-feature/qa_report.md

# Skip QA temporarily
python run.py --spec 001 --skip-qa

# Or limit iterations
MAX_QA_ITERATIONS=5 python run.py --spec 001 --qa
```

#### QA Fixer Not Fixing

```bash
# QA Fixer fails to fix issues

# Check fix request
cat .auto-claude/specs/001-feature/QA_FIX_REQUEST.md

# Add human guidance
echo "Focus on fixing the session storage issue first" > .auto-claude/specs/001-feature/HUMAN_INPUT.md
```

## Debug Mode

### Enable Verbose Logging

```bash
# Level 1: Basic
DEBUG=true DEBUG_LEVEL=1 python run.py --spec 001

# Level 2: Detailed
DEBUG=true DEBUG_LEVEL=2 python run.py --spec 001

# Level 3: Verbose (everything)
DEBUG=true DEBUG_LEVEL=3 python run.py --spec 001
```

### Log to File

```bash
# Log to file
DEBUG=true DEBUG_LOG_FILE=debug.log python run.py --spec 001

# View in real-time
tail -f debug.log
```

### Agent Communication

```bash
# See agent messages
DEBUG=true python run.py --spec 001 2>&1 | tee agent.log

# Search for errors
grep -i error agent.log
grep -i failed agent.log
```

## Recovery Procedures

### Restart Clean

```bash
# Full reset for a spec
rm -rf .auto-claude/specs/001-feature
rm -rf .worktrees/auto-claude/001-feature
git branch -D auto-claude/001-feature 2>/dev/null
git worktree prune

# Recreate spec
python spec_runner.py --task "Your task description"
```

### Resume from Checkpoint

```bash
# Continue interrupted spec
python spec_runner.py --continue 001-feature

# Continue interrupted build
python run.py --spec 001
```

### Manual Intervention

```bash
# 1. Pause the build
touch .auto-claude/specs/001-feature/PAUSE

# 2. Make manual changes in worktree
cd .worktrees/auto-claude/001-feature/
# ... edit files ...
git add .
git commit -m "Manual fix"

# 3. Resume
cd ../../apps/backend
rm .auto-claude/specs/001-feature/PAUSE
python run.py --spec 001
```

## Performance Issues

### Slow Builds

```bash
# Use faster model
AUTO_BUILD_MODEL=claude-sonnet-4-5-20250929 python run.py --spec 001

# Reduce thinking tokens
# Edit agent creation to use max_thinking_tokens=3000

# Skip research phase
SKIP_RESEARCH_PHASE=true python spec_runner.py --task "..."
```

### High Memory Usage

```bash
# Monitor memory
watch -n 1 'ps aux | grep python'

# Reduce context
MAX_CONTEXT_FILES=30 python run.py --spec 001

# Use smaller embedding model
OLLAMA_EMBEDDING_MODEL=all-minilm
OLLAMA_EMBEDDING_DIM=384
```

### API Rate Limits

```bash
# Error: Rate limit exceeded

# Wait and retry
sleep 60
python run.py --spec 001

# Or use different endpoint
ANTHROPIC_BASE_URL=http://localhost:3456 python run.py --spec 001
```

## Getting Help

### Gather Diagnostics

```bash
# System info
echo "Python: $(python3 --version)"
echo "Node: $(node --version)"
echo "Git: $(git --version)"
echo "Claude: $(claude --version)"

# Auto-Claude version
cat package.json | grep '"version"'

# Last 50 lines of logs
tail -50 .auto-claude/specs/*/build-progress.txt
```

### Community Resources

- **Discord**: https://discord.gg/KCXaPBr4Dj
- **GitHub Issues**: https://github.com/AndyMik90/Auto-Claude/issues
- **Discussions**: https://github.com/AndyMik90/Auto-Claude/discussions

### Report a Bug

Include:
1. Operating system and version
2. Python and Node.js versions
3. Auto-Claude version
4. Steps to reproduce
5. Error messages
6. Relevant logs

## Related Skills

- **auto-claude-setup**: Installation guide
- **auto-claude-cli**: CLI reference
- **auto-claude-optimization**: Performance tuning
