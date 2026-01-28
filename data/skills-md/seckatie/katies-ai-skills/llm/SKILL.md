---
name: llm
description: Access and interact with Large Language Models from the command line using Simon Willison's llm CLI tool. Supports OpenAI, Anthropic, Gemini, Llama, and dozens of other models via plugins. Features include chat sessions, embeddings, structured data extraction with schemas, prompt templates, conversation logging, and tool use. This skill is triggered when the user says things like "run a prompt with llm", "use the llm command", "call an LLM from the command line", "set up llm API keys", "install llm plugins", "create embeddings", or "extract structured data from text".
---

# LLM CLI Tool Skill

A CLI tool and Python library for interacting with Large Language Models including OpenAI, Anthropic's Claude, Google's Gemini, Meta's Llama, and dozens of others via remote APIs or locally installed models.

## When to Use This Skill

Use this skill when:
- Running prompts against LLMs from the command line
- Managing conversations and chat sessions
- Working with embeddings for semantic search
- Extracting structured data using schemas
- Installing and configuring LLM plugins
- Managing API keys for various providers
- Using templates for reusable prompts
- Logging and analyzing LLM interactions

## Quick Reference

### Basic Commands
```bash
# Run a prompt
llm "Your prompt here"

# Use a specific model
llm -m claude-4-opus "Your prompt"

# Chat mode
llm chat -m gpt-4.1

# With attachments (images, audio, video)
llm "describe this" -a image.jpg

# Pipe content
cat file.py | llm -s "Explain this code"
```

### Key Management
```bash
llm keys set openai
llm keys set anthropic
llm keys set gemini
```

### Plugin Management
```bash
llm install llm-anthropic
llm install llm-gemini
llm install llm-ollama
llm plugins
```

## Documentation Index

### Core Documentation

- **[README.md](README.md)** - Project overview and quick start guide
- **[docs/setup.md](docs/setup.md)** - Installation and initial configuration
- **[docs/usage.md](docs/usage.md)** - Comprehensive CLI usage guide (prompts, chat, attachments, conversations)
- **[docs/help.md](docs/help.md)** - Complete command reference and help text

### Model Configuration

- **[docs/openai-models.md](docs/openai-models.md)** - OpenAI model configuration and features
- **[docs/other-models.md](docs/other-models.md)** - Configuration for other model providers

### Advanced Features

- **[docs/tools.md](docs/tools.md)** - Tool use and function calling with LLMs
- **[docs/schemas.md](docs/schemas.md)** - Structured data extraction from text and images
- **[docs/templates.md](docs/templates.md)** - Creating and using prompt templates
- **[docs/fragments.md](docs/fragments.md)** - Long context support using fragments
- **[docs/aliases.md](docs/aliases.md)** - Creating model aliases

### Embeddings

- **[docs/embeddings/index.md](docs/embeddings/index.md)** - Embeddings overview
- **[docs/embeddings/cli.md](docs/embeddings/cli.md)** - Embeddings CLI commands
- **[docs/embeddings/python-api.md](docs/embeddings/python-api.md)** - Embeddings Python API
- **[docs/embeddings/storage.md](docs/embeddings/storage.md)** - Embeddings storage system
- **[docs/embeddings/writing-plugins.md](docs/embeddings/writing-plugins.md)** - Writing embedding plugins

### Plugins

- **[docs/plugins/index.md](docs/plugins/index.md)** - Plugin system overview
- **[docs/plugins/installing-plugins.md](docs/plugins/installing-plugins.md)** - Installing and managing plugins
- **[docs/plugins/directory.md](docs/plugins/directory.md)** - Plugin directory listing
- **[docs/plugins/tutorial-model-plugin.md](docs/plugins/tutorial-model-plugin.md)** - Tutorial: Creating a model plugin
- **[docs/plugins/advanced-model-plugins.md](docs/plugins/advanced-model-plugins.md)** - Advanced plugin development
- **[docs/plugins/plugin-hooks.md](docs/plugins/plugin-hooks.md)** - Plugin hooks reference
- **[docs/plugins/plugin-utilities.md](docs/plugins/plugin-utilities.md)** - Plugin utility functions

### Python API & Development

- **[docs/python-api.md](docs/python-api.md)** - Python library API reference
- **[docs/logging.md](docs/logging.md)** - Logging system and SQLite storage
- **[docs/contributing.md](docs/contributing.md)** - Contributing to LLM development

### Reference

- **[docs/related-tools.md](docs/related-tools.md)** - Related tools and ecosystem
- **[docs/changelog.md](docs/changelog.md)** - Version history and changes

## Common Workflows

### Starting a Conversation
```bash
# Start chat with context
llm chat -m gpt-4.1 -s "You are a helpful coding assistant"

# Continue a previous conversation
llm -c "Follow up question"
```

### Working with Files
```bash
# Analyze code
cat script.py | llm "Review this code for bugs"

# Process multiple files
cat *.md | llm "Summarize these documents"
```

### Structured Output
```bash
# Extract data with schema
llm -m gpt-4.1 "Extract person info" -a photo.jpg --schema name,age,occupation
```

### Template Usage
```bash
# List templates
llm templates

# Use a template
llm -t summarize < article.txt
```
