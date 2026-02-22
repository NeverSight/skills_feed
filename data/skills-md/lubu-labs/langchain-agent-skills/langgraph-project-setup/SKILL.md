---
name: langgraph-project-setup
description: Initialize and configure LangGraph projects with proper structure, langgraph.json configuration, environment variables, and dependency management. Use when users want to (1) create a new LangGraph project, (2) set up langgraph.json for deployment, (3) configure environment variables for LLM providers, (4) initialize project structure for agents, (5) set up local development with LangGraph Studio, (6) configure dependencies (pyproject.toml, requirements.txt, package.json), or (7) troubleshoot project configuration issues.
---

# LangGraph Project Setup

Initialize and configure LangGraph projects for local development and deployment.

## Quick Start

### Python Project

```bash
# Initialize new project
uv run scripts/init_langgraph_project.py my-agent

# Fallback if uv not available
python3 scripts/init_langgraph_project.py my-agent

# Or with options
uv run scripts/init_langgraph_project.py my-agent \
  --pattern multiagent \
  --python-version 3.12

# Fallback if uv not available
python3 scripts/init_langgraph_project.py my-agent \
  --pattern multiagent \
  --python-version 3.12
```

### JavaScript Project

```bash
# Initialize new project
node scripts/init_langgraph_project.js my-agent

# TypeScript project
node scripts/init_langgraph_project.js my-agent --typescript

# Multi-agent pattern
node scripts/init_langgraph_project.js my-agent \
  --pattern multiagent \
  --typescript
```

## Setup Workflow

### Step 1: Choose Project Pattern

**Simple Pattern:** Single agent with straightforward workflow
- Best for: Getting started, prototypes, single-purpose agents
- Structure: Minimal files, agent.py/agent.ts at package root

**Multi-Agent Pattern:** Modular architecture with separated concerns
- Best for: Complex workflows, multiple agents, production applications
- Structure: utils/ directory with state.py, nodes.py, tools.py

### Step 2: Initialize Project

Run the init script with your chosen pattern:

```bash
# Python - simple
uv run scripts/init_langgraph_project.py my-agent

# Fallback if uv not available
python3 scripts/init_langgraph_project.py my-agent

# Python - multi-agent
uv run scripts/init_langgraph_project.py my-agent --pattern multiagent

# Fallback if uv not available
python3 scripts/init_langgraph_project.py my-agent --pattern multiagent

# JavaScript/TypeScript - simple
node scripts/init_langgraph_project.js my-agent --typescript

# JavaScript/TypeScript - multi-agent
node scripts/init_langgraph_project.js my-agent --pattern multiagent --typescript
```

The script creates:
- Project directory structure
- `langgraph.json` configuration
- `.env` template
- Dependency files (pyproject.toml or package.json)
- `.gitignore`
- Boilerplate code with TODO comments

### Step 3: Install Dependencies

**Python:**
```bash
cd my-agent
uv venv --python 3.12
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e '.[dev]'

# Fallback if uv not available
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e '.[dev]'
```

**JavaScript:**
```bash
cd my-agent
npm install  # or: yarn install / pnpm install
```

### Step 4: Configure Environment Variables

**Option A: Interactive Setup (Recommended)**

```bash
uv run scripts/setup_providers.py
```

Follow the prompts to configure:
- OpenAI
- Anthropic (Claude)
- Google (Gemini)
- AWS Bedrock
- LangSmith (tracing)
- Tavily (search)

**Option B: Manual Configuration**

Edit `.env` file directly:

```bash
# Required: Choose at least one LLM provider
OPENAI_API_KEY=sk-...
# or
ANTHROPIC_API_KEY=sk-ant-...

# Optional: Enable tracing
LANGSMITH_API_KEY=lsv2_...
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=my-project
```

See `references/provider-configuration.md` for provider-specific setup.

### Step 5: Implement Agent Logic

Replace TODO comments in generated files:

**Python Simple:**
- Edit `my_agent/agent.py`
- Configure LLM in `call_model` function

**Python Multi-Agent:**
- Define state schema in `my_agent/utils/state.py`
- Implement node logic in `my_agent/utils/nodes.py`
- Add tools in `my_agent/utils/tools.py`
- Build graph in `my_agent/agent.py`

**JavaScript/TypeScript:**
- Similar structure in `src/` directory
- Import appropriate LangChain packages

### Step 6: Configure langgraph.json

The init script creates a basic configuration. Customize as needed:

```json
{
  "dependencies": ["."],
  "graphs": {
    "agent": "./my_agent/agent.py:graph"
  },
  "env": ".env",
  "python_version": "3.11"
}
```

**Key configuration options:**
- `dependencies`: Package dependencies location
- `graphs`: Mapping of graph IDs to code paths
- `env`: Path to environment file
- `python_version` or `node_version`: Runtime version

For complete schema reference, see `references/langgraph-json-schema.md`.

### Step 7: Start Development Server

**Option A: langgraph dev (Recommended for development)**

```bash
langgraph dev
```

- No Docker required
- In-memory state persistence
- Hot reloading enabled
- Default port: 2024

**Option B: langgraph up (Production-like testing)**

```bash
langgraph up
```

- Docker required
- PostgreSQL state persistence
- Production environment simulation
- Default port: 8123

### Step 8: Connect to LangGraph Studio

Access Studio in your browser:

```
https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
```

**Safari users:** Use `--tunnel` flag:
```bash
langgraph dev --tunnel
```

## Validation

### Validate Configuration

```bash
uv run scripts/validate_langgraph_config.py
```

Checks:
- Required fields (dependencies, graphs)
- File paths and references
- Optional field formats
- Common configuration errors

### Test Agent Locally

```bash
# Start server
langgraph dev

# In another terminal, test with curl
curl -X POST http://localhost:2024/invoke \
  -H "Content-Type: application/json" \
  -d '{"input": {"messages": [{"role": "user", "content": "Hello"}]}}'
```

## Common Configurations

### Python with OpenAI

```toml
# pyproject.toml
[project.optional-dependencies]
openai = ["langchain-openai>=1.1.0"]
```

```python
# agent.py
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o-mini")
```

### Python with Anthropic

```toml
# pyproject.toml
[project.optional-dependencies]
anthropic = ["langchain-anthropic>=1.1.0"]
```

```python
# agent.py
from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(model="claude-haiku-4-5-20251001")
```

### JavaScript with OpenAI

```json
// package.json
{
  "dependencies": {
    "@langchain/openai": "^1.1.0"
  }
}
```

```typescript
// agent.ts
import { ChatOpenAI } from "@langchain/openai";

const model = new ChatOpenAI({ model: "gpt-4o-mini" });
```

## Project Structure Reference

- Python structures: `references/python-project-structure.md`
- JavaScript structures: `references/javascript-project-structure.md`
- langgraph.json schema: `references/langgraph-json-schema.md`
- Provider setup: `references/provider-configuration.md`
- Deployment options: `references/deployment-targets.md`

## Troubleshooting

### "Module not found" errors

Ensure dependencies are installed:

```bash
# Python
uv pip install -e '.[dev]'

# Fallback if uv not available
pip install -e '.[dev]'

# JavaScript
npm install
```

### "Graph not found" in langgraph.json

Check graph path format:
- Python: `./package_name/agent.py:graph`
- JavaScript: `./src/agent.ts:graph`

Validate: `uv run scripts/validate_langgraph_config.py` (fallback: `python3 scripts/validate_langgraph_config.py`)

### Environment variables not loading

- Check `.env` file exists in project root
- Verify `"env": ".env"` in langgraph.json
- Ensure no quotes around values in .env
- Restart development server after changes

### Studio connection issues

- Verify server is running: `langgraph dev`
- Check correct port (default: 2024)
- Safari users: use `--tunnel` flag
- Check firewall/security software

### Hot reload not working

- Ensure using `langgraph dev` (not `langgraph up`)
- Check file is in correct directory
- Try manual restart if needed

## Next Steps

After setup:

1. Implement agent logic (replace TODOs)
2. Add tools and nodes as needed
3. Test with Studio
4. Write tests (see langgraph-testing-evaluation skill)
5. Deploy to LangSmith (see langsmith-deployment skill)

## Scripts Reference

### init_langgraph_project.py

Initialize Python project:

```bash
uv run scripts/init_langgraph_project.py <name> [--pattern simple|multiagent] [--python-version 3.11|3.12|3.13]

# Fallback if uv not available
python3 scripts/init_langgraph_project.py <name> [--pattern simple|multiagent] [--python-version 3.11|3.12|3.13]
```

### init_langgraph_project.js

Initialize JavaScript project:

```bash
node scripts/init_langgraph_project.js <name> [--pattern simple|multiagent] [--typescript]
```

### validate_langgraph_config.py

Validate langgraph.json:

```bash
uv run scripts/validate_langgraph_config.py [path/to/langgraph.json]

# Fallback if uv not available
python3 scripts/validate_langgraph_config.py [path/to/langgraph.json]
```

### setup_providers.py

Interactive provider setup:

```bash
uv run scripts/setup_providers.py [--output .env]

# Fallback if uv not available
python3 scripts/setup_providers.py [--output .env]
```

## Additional Resources

- [LangGraph Documentation](https://docs.langchain.com/langgraph)
- [LangSmith Documentation](https://docs.langchain.com/langsmith)
- [LangGraph CLI Reference](https://docs.langchain.com/langsmith/cli)
- [Application Structure Guide](https://docs.langchain.com/oss/python/langgraph/application-structure)
