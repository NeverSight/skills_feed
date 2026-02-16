---
name: development-environment
description: IDE setup, dev containers, and local development tools
domain: tools-integrations
version: 1.0.0
tags: [vscode, devcontainers, docker, dotfiles, terminal]
triggers:
  keywords:
    primary: [vscode, ide, devcontainer, docker, dotfiles, terminal, setup]
    secondary: [extension, config, workspace, neovim, vim, tmux, zsh]
  context_boost: [development, local, environment, tooling]
  context_penalty: [production, deploy, cloud]
  priority: medium
---

# Development Environment

## Overview

Setting up efficient development environments with modern tools, containers, and automation.

---

## VS Code Setup

### Settings

```jsonc
// .vscode/settings.json
{
  // Editor
  "editor.fontSize": 14,
  "editor.fontFamily": "'JetBrains Mono', 'Fira Code', monospace",
  "editor.fontLigatures": true,
  "editor.tabSize": 2,
  "editor.insertSpaces": true,
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit",
    "source.organizeImports": "explicit"
  },
  "editor.rulers": [80, 120],
  "editor.minimap.enabled": false,
  "editor.bracketPairColorization.enabled": true,
  "editor.guides.bracketPairs": true,
  "editor.inlineSuggest.enabled": true,

  // Files
  "files.autoSave": "onFocusChange",
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true,
  "files.exclude": {
    "**/.git": true,
    "**/node_modules": true,
    "**/.DS_Store": true,
    "**/coverage": true,
    "**/dist": true
  },

  // Terminal
  "terminal.integrated.fontSize": 13,
  "terminal.integrated.fontFamily": "'JetBrains Mono', monospace",
  "terminal.integrated.defaultProfile.osx": "zsh",

  // TypeScript
  "typescript.preferences.importModuleSpecifier": "relative",
  "typescript.updateImportsOnFileMove.enabled": "always",
  "typescript.suggest.autoImports": true,

  // Prettier
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[json]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },

  // Git
  "git.autofetch": true,
  "git.confirmSync": false,
  "git.enableSmartCommit": true
}
```

### Extensions

```jsonc
// .vscode/extensions.json
{
  "recommendations": [
    // Essential
    "esbenp.prettier-vscode",
    "dbaeumer.vscode-eslint",
    "ms-vscode.vscode-typescript-next",

    // Git
    "eamodio.gitlens",
    "mhutchie.git-graph",

    // Development
    "ms-vscode-remote.remote-containers",
    "ms-vscode.live-server",
    "bradlc.vscode-tailwindcss",

    // Testing
    "vitest.explorer",
    "ms-playwright.playwright",

    // Productivity
    "usernamehw.errorlens",
    "streetsidesoftware.code-spell-checker",
    "christian-kohler.path-intellisense",
    "formulahendry.auto-rename-tag",

    // Themes
    "GitHub.github-vscode-theme",
    "PKief.material-icon-theme"
  ]
}
```

### Tasks & Launch

```jsonc
// .vscode/tasks.json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "dev",
      "type": "npm",
      "script": "dev",
      "problemMatcher": [],
      "isBackground": true,
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    },
    {
      "label": "build",
      "type": "npm",
      "script": "build",
      "group": {
        "kind": "build",
        "isDefault": true
      },
      "problemMatcher": ["$tsc"]
    },
    {
      "label": "test",
      "type": "npm",
      "script": "test",
      "group": {
        "kind": "test",
        "isDefault": true
      }
    }
  ]
}
```

```jsonc
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug Current File",
      "type": "node",
      "request": "launch",
      "program": "${file}",
      "runtimeArgs": ["--loader", "tsx"],
      "console": "integratedTerminal",
      "internalConsoleOptions": "neverOpen"
    },
    {
      "name": "Debug Jest Tests",
      "type": "node",
      "request": "launch",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["test", "--", "--runInBand"],
      "console": "integratedTerminal"
    },
    {
      "name": "Attach to Process",
      "type": "node",
      "request": "attach",
      "port": 9229
    },
    {
      "name": "Debug Next.js",
      "type": "node",
      "request": "launch",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "dev"],
      "console": "integratedTerminal",
      "serverReadyAction": {
        "pattern": "started server on .+, url: (https?://.+)",
        "uriFormat": "%s",
        "action": "debugWithChrome"
      }
    }
  ]
}
```

---

## Dev Containers

### Basic Configuration

```jsonc
// .devcontainer/devcontainer.json
{
  "name": "Node.js Development",
  "image": "mcr.microsoft.com/devcontainers/typescript-node:20",

  // Features to add
  "features": {
    "ghcr.io/devcontainers/features/github-cli:1": {},
    "ghcr.io/devcontainers/features/docker-in-docker:2": {},
    "ghcr.io/devcontainers/features/aws-cli:1": {}
  },

  // Ports to forward
  "forwardPorts": [3000, 5432, 6379],

  // Post-create commands
  "postCreateCommand": "npm install",

  // VS Code customizations
  "customizations": {
    "vscode": {
      "settings": {
        "terminal.integrated.defaultProfile.linux": "zsh"
      },
      "extensions": [
        "esbenp.prettier-vscode",
        "dbaeumer.vscode-eslint"
      ]
    }
  },

  // Mount points
  "mounts": [
    "source=${localEnv:HOME}/.ssh,target=/home/node/.ssh,type=bind,consistency=cached"
  ],

  // Environment variables
  "containerEnv": {
    "NODE_ENV": "development"
  },

  // Run as non-root user
  "remoteUser": "node"
}
```

### Docker Compose Dev Container

```jsonc
// .devcontainer/devcontainer.json
{
  "name": "Full Stack Development",
  "dockerComposeFile": "docker-compose.yml",
  "service": "app",
  "workspaceFolder": "/workspace",

  "features": {
    "ghcr.io/devcontainers/features/github-cli:1": {}
  },

  "forwardPorts": [3000, 5432, 6379],

  "postCreateCommand": "npm install",

  "customizations": {
    "vscode": {
      "extensions": [
        "esbenp.prettier-vscode",
        "dbaeumer.vscode-eslint",
        "prisma.prisma"
      ]
    }
  }
}
```

```yaml
# .devcontainer/docker-compose.yml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    volumes:
      - ..:/workspace:cached
      - node_modules:/workspace/node_modules
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/dev
      - REDIS_URL=redis://cache:6379
    depends_on:
      - db
      - cache

  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=dev

  cache:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  node_modules:
  postgres_data:
  redis_data:
```

```dockerfile
# .devcontainer/Dockerfile
FROM mcr.microsoft.com/devcontainers/typescript-node:20

# Install additional tools
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install global npm packages
RUN npm install -g prisma tsx

# Set up zsh
RUN sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

USER node
```

---

## Terminal Setup

### Zsh Configuration

```bash
# ~/.zshrc

# Oh My Zsh
export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="robbyrussell"

plugins=(
  git
  docker
  docker-compose
  npm
  node
  z
  zsh-autosuggestions
  zsh-syntax-highlighting
)

source $ZSH/oh-my-zsh.sh

# Aliases
alias ll='ls -la'
alias g='git'
alias gst='git status'
alias gco='git checkout'
alias gp='git push'
alias gl='git pull'
alias gc='git commit'
alias gd='git diff'
alias glog='git log --oneline --graph --all'

alias d='docker'
alias dc='docker-compose'
alias dps='docker ps'
alias dcu='docker-compose up -d'
alias dcd='docker-compose down'

alias nr='npm run'
alias nrd='npm run dev'
alias nrb='npm run build'
alias nrt='npm run test'

# Functions
mkcd() { mkdir -p "$1" && cd "$1"; }

# Node version manager
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Auto-switch node version
autoload -U add-zsh-hook
load-nvmrc() {
  local nvmrc_path="$(nvm_find_nvmrc)"
  if [ -n "$nvmrc_path" ]; then
    local nvmrc_node_version=$(nvm version "$(cat "${nvmrc_path}")")
    if [ "$nvmrc_node_version" = "N/A" ]; then
      nvm install
    elif [ "$nvmrc_node_version" != "$(nvm version)" ]; then
      nvm use
    fi
  fi
}
add-zsh-hook chpwd load-nvmrc
load-nvmrc
```

### Starship Prompt

```toml
# ~/.config/starship.toml

format = """
$directory\
$git_branch\
$git_status\
$nodejs\
$python\
$rust\
$docker_context\
$line_break\
$character"""

[directory]
truncation_length = 3
truncate_to_repo = true

[git_branch]
symbol = "🌱 "
format = "[$symbol$branch]($style) "

[git_status]
format = '([$all_status$ahead_behind]($style) )'
conflicted = "⚔️"
ahead = "⬆️${count}"
behind = "⬇️${count}"
diverged = "⬆️${ahead_count}⬇️${behind_count}"
untracked = "📁"
stashed = "📦"
modified = "📝"
staged = "✅"
deleted = "🗑️"

[nodejs]
format = "[$symbol($version )]($style)"
symbol = "⬢ "

[python]
format = "[$symbol($version )]($style)"
symbol = "🐍 "

[rust]
format = "[$symbol($version )]($style)"
symbol = "🦀 "

[docker_context]
format = "[$symbol$context]($style) "
symbol = "🐳 "

[character]
success_symbol = "[❯](bold green)"
error_symbol = "[❯](bold red)"
```

---

## Dotfiles Management

```bash
# Initialize dotfiles repo
mkdir ~/.dotfiles
cd ~/.dotfiles
git init

# Structure
~/.dotfiles/
├── .gitconfig
├── .zshrc
├── .vimrc
├── install.sh
├── macos/
│   └── defaults.sh
├── vscode/
│   ├── settings.json
│   └── keybindings.json
└── config/
    └── starship.toml
```

```bash
#!/bin/bash
# install.sh

# Create symlinks
ln -sf ~/.dotfiles/.zshrc ~/.zshrc
ln -sf ~/.dotfiles/.gitconfig ~/.gitconfig
ln -sf ~/.dotfiles/config/starship.toml ~/.config/starship.toml

# VS Code settings
ln -sf ~/.dotfiles/vscode/settings.json \
  ~/Library/Application\ Support/Code/User/settings.json

# Install Homebrew packages
if [[ "$OSTYPE" == "darwin"* ]]; then
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

  brew bundle --file=~/.dotfiles/Brewfile
fi

# Install Oh My Zsh
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# Install Starship
curl -sS https://starship.rs/install.sh | sh

echo "Dotfiles installed!"
```

```ruby
# Brewfile
# CLI tools
brew "git"
brew "gh"
brew "node"
brew "python"
brew "rust"
brew "go"
brew "jq"
brew "ripgrep"
brew "fd"
brew "bat"
brew "exa"
brew "fzf"
brew "starship"
brew "zoxide"

# Development
brew "docker"
brew "docker-compose"
brew "postgresql@15"
brew "redis"

# Applications
cask "visual-studio-code"
cask "iterm2"
cask "docker"
cask "postman"
cask "figma"
cask "slack"
cask "notion"
```

---

## Local Development

### Environment Variables

```bash
# .env.example
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/myapp

# Redis
REDIS_URL=redis://localhost:6379

# Auth
JWT_SECRET=your-secret-key
SESSION_SECRET=another-secret

# External APIs
STRIPE_SECRET_KEY=sk_test_...
SENDGRID_API_KEY=SG....

# Feature Flags
ENABLE_NEW_CHECKOUT=false
```

```typescript
// env.ts - Type-safe environment variables
import { z } from 'zod';

const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  REDIS_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  NODE_ENV: z.enum(['development', 'test', 'production']).default('development'),
  PORT: z.coerce.number().default(3000),
});

export const env = envSchema.parse(process.env);
```

---

## Related Skills

- [[devops-cicd]] - CI/CD integration
- [[docker]] - Containerization
- [[git-workflows]] - Version control

