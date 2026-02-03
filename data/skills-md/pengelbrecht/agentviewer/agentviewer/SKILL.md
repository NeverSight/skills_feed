---
name: agentviewer
description: Display rich content (markdown, code, diffs, mermaid diagrams) to users in a browser viewer. Use when you need to show complex content that benefits from rich rendering - reports, documentation, code with syntax highlighting, git diffs, or diagrams.
allowed-tools: "Read,Bash(curl:*,agentviewer:*)"
version: "0.1.0"
author: "Peter Engelbrecht <https://github.com/pengelbrecht>"
license: "MIT"
---

# Agentviewer

Display rich content in a browser-based tabbed viewer. Perfect for showing users:
- Markdown documents with rendered formatting
- Code with syntax highlighting (180+ languages)
- Git diffs with side-by-side comparison
- Mermaid diagrams and LaTeX math

## Prerequisites

The agentviewer CLI must be installed and available in your PATH.

### Installation Options

**macOS/Linux (Homebrew):**
```bash
brew install pengelbrecht/tap/agentviewer
```

**Windows (Scoop):**
```powershell
scoop bucket add agentviewer https://github.com/pengelbrecht/scoop-agentviewer
scoop install agentviewer
```

**Windows (Winget):**
```powershell
winget install pengelbrecht.agentviewer
```

**Linux (deb - Debian/Ubuntu):**
```bash
curl -LO https://github.com/pengelbrecht/agentviewer/releases/latest/download/agentviewer_amd64.deb
sudo dpkg -i agentviewer_amd64.deb
```

**Linux (rpm - Fedora/RHEL):**
```bash
curl -LO https://github.com/pengelbrecht/agentviewer/releases/latest/download/agentviewer_x86_64.rpm
sudo rpm -i agentviewer_x86_64.rpm
```

**Go:**
```bash
go install github.com/pengelbrecht/agentviewer@latest
```

**Binary:** Download from [GitHub Releases](https://github.com/pengelbrecht/agentviewer/releases)

### Verify Installation

```bash
agentviewer --version
```

## Quick Start

Start the server (runs in background, opens browser):
```bash
agentviewer serve --open &
```

Create a tab with content:
```bash
curl -X POST localhost:3333/api/tabs \
  -d '{"title": "Report", "type": "markdown", "content": "# Hello\n\nContent here..."}'
```

## API Reference

Base URL: `http://localhost:3333`

### Create/Update Tab
```bash
# Markdown (renders GFM with diagrams and math)
curl -X POST localhost:3333/api/tabs \
  -d '{"title": "Notes", "type": "markdown", "content": "# My Notes\n\n- Item 1\n- Item 2"}'

# Code with syntax highlighting
curl -X POST localhost:3333/api/tabs \
  -d '{"title": "main.go", "type": "code", "content": "package main\n\nfunc main() {}", "language": "go"}'

# From file path (auto-detects type, enables live reload)
curl -X POST localhost:3333/api/tabs \
  -d '{"title": "Config", "file": "/path/to/config.yaml"}'

# Git diff (side-by-side comparison)
curl -X POST localhost:3333/api/tabs \
  -d '{"type": "diff", "diff": {"left": "old.go", "right": "new.go"}}'

# With explicit ID (for updates)
curl -X POST localhost:3333/api/tabs \
  -d '{"id": "my-report", "title": "Report", "type": "markdown", "content": "..."}'
```

### Tab Management
```bash
# List all tabs
curl localhost:3333/api/tabs

# Get tab content
curl localhost:3333/api/tabs/{id}

# Delete specific tab
curl -X DELETE localhost:3333/api/tabs/{id}

# Delete all tabs
curl -X DELETE localhost:3333/api/tabs

# Activate (switch to) tab
curl -X POST localhost:3333/api/tabs/{id}/activate
```

### Server Status
```bash
# Check if server is running
curl localhost:3333/api/status
```

## Content Types

| Type | Description | Features |
|------|-------------|----------|
| markdown | Rendered markdown | GFM, Mermaid diagrams, LaTeX math, code blocks |
| code | Source code | Syntax highlighting for 180+ languages |
| diff | File comparison | Side-by-side view with line numbers |

### Markdown Features

Agentviewer renders GitHub-flavored markdown with extensions:

```markdown
# Mermaid Diagrams
\`\`\`mermaid
graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action]
    B -->|No| D[End]
\`\`\`

# LaTeX Math
Inline: $E = mc^2$

Block:
$$
\frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
$$

# Code Blocks (with syntax highlighting)
\`\`\`python
def hello():
    print("Hello, world!")
\`\`\`
```

## Common Workflows

### Show Analysis Results
```bash
# Start server
agentviewer serve --open &

# Show a markdown report
curl -X POST localhost:3333/api/tabs -d '{
  "title": "Analysis",
  "type": "markdown",
  "content": "# Code Analysis\n\n## Summary\n- 10 files analyzed\n- 2 issues found\n\n## Issues\n\n### Issue 1\n```go\n// problematic code\nfunc foo() {}\n```\n"
}'
```

### Show Code with Live Reload
```bash
# Show a code file (changes reload automatically)
curl -X POST localhost:3333/api/tabs -d '{
  "title": "main.go",
  "file": "./main.go"
}'
```

### Show Git Diff
```bash
# Get current changes
git diff HEAD > /tmp/changes.diff

# Display in viewer
curl -X POST localhost:3333/api/tabs -d '{
  "title": "Changes",
  "type": "diff",
  "file": "/tmp/changes.diff"
}'
```

### Create Architecture Diagram
```bash
curl -X POST localhost:3333/api/tabs -d '{
  "title": "Architecture",
  "type": "markdown",
  "content": "# System Architecture\n\n```mermaid\ngraph TB\n    subgraph Frontend\n        A[React App]\n    end\n    subgraph Backend\n        B[API Server]\n        C[Database]\n    end\n    A --> B\n    B --> C\n```"
}'
```

## Best Practices

1. **Start server once** at the beginning of a session
2. **Use file paths** when showing existing files (enables auto-reload)
3. **Use meaningful titles** - they appear in the tab bar
4. **Clean up** - delete tabs when no longer needed
5. **Use markdown** for complex documents - renders beautifully with diagrams
6. **Use explicit IDs** when updating content to avoid creating duplicate tabs

## Error Handling

```bash
# Check if server is running
if ! curl -s localhost:3333/api/status > /dev/null 2>&1; then
    agentviewer serve --open &
    sleep 1
fi
```

## CLI Reference

```bash
# Start server
agentviewer serve [--port 3333] [--open]

# Show version
agentviewer --version
agentviewer -v
```
