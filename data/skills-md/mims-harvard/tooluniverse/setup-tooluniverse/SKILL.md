---
name: setup-tooluniverse
description: Install and configure ToolUniverse with MCP integration for any AI coding client (Cursor, Claude Desktop, Windsurf, VS Code, Codex, Gemini CLI, Trae, Cline, Antigravity, OpenCode, etc.). Covers uv/uvx setup, MCP configuration, API key walkthrough, skill installation, and upgrading. Use when setting up ToolUniverse, configuring MCP servers, troubleshooting installation issues, upgrading versions, or when user mentions installing ToolUniverse or setting up scientific tools.
---

# Setup ToolUniverse

Guide the user step-by-step through setting up ToolUniverse with MCP (Model Context Protocol) integration.

## Agent Behavior

**Be friendly, conversational, and interactive.** This is a setup wizard, not a reference manual.

- **Detect the user's language** from their first message. If they write in Chinese, Japanese, Spanish, etc., respond in that language throughout the entire setup. All explanations, questions, and celebrations should be in their language. Only keep commands, code blocks, URLs, and env variable names in English (those are technical and must stay as-is).
- Go **one step at a time**. Don't dump all steps at once.
- **Ask before proceeding** to the next step. Confirm the previous step worked.
- Use the **AskQuestion tool** for structured choices when available (client selection, research areas, etc.).
- **Explain briefly** what each step does and why, in plain language.
- When something goes wrong, be reassuring and help troubleshoot before moving on.
- **Celebrate small wins** -- when uv installs successfully, when the MCP server appears, when the first tool call works.

## Internal Notes (do not show to user)

⚠️ **ToolUniverse has 1200+ tools** which will cause context window overflow if all exposed directly. The default `tooluniverse` command already enables compact mode automatically.

**Compact mode** exposes only 5 core tools (list_tools, grep_tools, get_tool_info, execute_tool, find_tools) while keeping all 1200+ tools accessible via execute_tool.

## Step 0: Welcome & Discovery

Start by welcoming the user and asking two questions to tailor the setup:

**Question 1: Which app are you using?**

Use AskQuestion if available:
- Cursor
- Claude Desktop
- VS Code / Copilot
- Windsurf
- Claude Code
- Gemini CLI
- Codex (OpenAI)
- Cline
- Trae
- Antigravity
- OpenCode
- Other

**Question 2: How will you use ToolUniverse?**
- **MCP server** (use scientific tools through chat) -- this is the default for most users
- **Python coding** (write scripts that `import tooluniverse`) -- also needs pip install

For MCP-only users, only `uv` is needed. `uvx` automatically installs and runs ToolUniverse.

For coding use, also ask about Python version (`python3 --version`, needs >=3.10, <3.14).

## Installation Workflow

### Step 1: Make sure uv is installed

First, check if the user already has `uv` (a fast Python package manager). Run this for them:

```bash
which uv || echo "uv not installed"
```

If it's already installed, let them know and move on. If not, explain that `uv` is a fast package manager that makes MCP setup simple, then install it:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Confirm it worked** before moving to the next step.

### Step 2: Add ToolUniverse to your MCP config

Now we'll add ToolUniverse to your app's MCP configuration. Based on the client the user chose in Step 0, help them find and edit the right config file. All clients use the same server config -- only the file location differs.

#### MCP Server Configuration (same for all clients)

**Default method: Using uvx (Recommended)**
```json
{
  "mcpServers": {
    "tooluniverse": {
      "command": "uvx",
      "args": ["tooluniverse"],
      "env": {
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

`uvx tooluniverse` automatically installs and runs ToolUniverse with compact mode enabled by default (the `tooluniverse` entry point enables `--compact-mode` automatically). No separate `pip install` step required.

**Alternative: Using a pre-installed command** (if user already has ToolUniverse installed via pip)
```json
{
  "mcpServers": {
    "tooluniverse": {
      "command": "tooluniverse",
      "args": [],
      "env": {
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

#### Config File Locations by Client

| Client | Config File (macOS) | How to Access |
|--------|-------------------|---------------|
| **Cursor** | `~/.cursor/mcp.json` | Settings → MCP → Add new global MCP server |
| **Claude Desktop** | `~/Library/Application Support/Claude/claude_desktop_config.json` | Settings → Developer → Edit Config |
| **Claude Code** | `~/.claude.json` (user) or `.mcp.json` (project) | `claude mcp add` CLI or edit directly |
| **Windsurf** | `~/.codeium/windsurf/mcp_config.json` | Click MCP hammer icon → Configure |
| **VS Code (Copilot)** | `.vscode/mcp.json` (workspace) or user profile `mcp.json` | Cmd Palette → "MCP: Add Server" (see different format below) |
| **Cline** | `cline_mcp_settings.json` (in VS Code extension globalStorage) | Cline panel → MCP Servers → Configure |
| **Codex (OpenAI)** | `~/.codex/config.toml` | Create/edit manually (TOML format, see below) |
| **Gemini CLI** | `~/.gemini/settings.json` (user) or `.gemini/settings.json` (project) | `gemini mcp add` CLI or edit directly |
| **Antigravity** | `mcp_config.json` | "..." dropdown → Manage MCP Servers → View raw config |
| **Trae** | `.trae/mcp.json` (project) or global via Trae UI | Ctrl+U → AI Management → MCP → Configure Manually |
| **OpenCode** | `~/.config/opencode/opencode.json` or `opencode.json` (project) | Edit directly |

**Windows/Linux paths differ** -- check your client's documentation for the exact location.

Most clients use the same JSON `mcpServers` format shown above. **Exceptions**: VS Code uses `"servers"` key, Codex uses TOML, and OpenCode uses a `"mcp"` key -- see below for their specific formats.

#### Clients with Different Config Formats

**VS Code (Copilot)** -- uses `"servers"` key (not `"mcpServers"`) and requires `"type"` field. Add to `.vscode/mcp.json`:
```json
{
  "servers": {
    "tooluniverse": {
      "type": "stdio",
      "command": "uvx",
      "args": ["tooluniverse"],
      "env": { "PYTHONIOENCODING": "utf-8" }
    }
  }
}
```

**Codex (TOML format)** -- add to `~/.codex/config.toml`:
```toml
[mcp_servers.tooluniverse]
command = "uvx"
args = ["tooluniverse"]
env = { "PYTHONIOENCODING" = "utf-8" }
```

**OpenCode** -- uses `mcp` key with `type` and `command` as array in `opencode.json`:
```json
{
  "mcp": {
    "tooluniverse": {
      "type": "local",
      "command": ["uvx", "tooluniverse"],
      "enabled": true,
      "environment": { "PYTHONIOENCODING": "utf-8" }
    }
  }
}
```

### Step 3 (Only if user chose coding use): Install Python package

Skip this if the user only needs MCP. For coding use, install into their Python environment:

```bash
pip install tooluniverse
```

Then verify together:
```python
from tooluniverse import ToolUniverse
tu = ToolUniverse()
print(f"ToolUniverse version: {tu.__version__}")
```

Let them know this is separate from the MCP server -- `uvx` installs into uv's cache, while `pip install` puts it in their Python environment for importing.

### Step 4: Set up API Keys

Many tools work without API keys, but some unlock powerful features. Before diving into keys, **ask the user about their research interests** to recommend only what's relevant.

Read [API_KEYS_REFERENCE.md](API_KEYS_REFERENCE.md) for detailed per-key info (what it does, step-by-step registration, which tools need it).

#### How to guide API key setup

1. **Ask the user** what research areas they're interested in. Use AskQuestion if available with options like:
   - Literature search & publications
   - Drug discovery & pharmacology
   - Protein structure & interactions
   - Genomics & disease associations
   - Rare diseases & clinical
   - Enzymology & biochemistry
   - Patent search
   - AI-powered analysis (needs LLM key)
   - All of the above
   - Not sure yet / skip for now

2. **Map their answer to recommended keys** using the tiers below. Don't overwhelm -- suggest 2-4 keys to start.

3. **Walk through each key one at a time**:
   - Explain in plain language what it unlocks (e.g., "This lets you search PubMed faster")
   - Give them the registration link
   - Wait for them to sign up and get the key
   - Help them add it to their config file
   - Move to the next key

4. **After all keys are added**, restart the app and test one key with a real tool call.

5. Let them know they can always come back to add more keys later.

#### Tier 1: Core Scientific Keys (Recommended for most users)

| Key | Service | What It Unlocks | Free? | Registration |
|-----|---------|----------------|-------|-------------|
| `NCBI_API_KEY` | NCBI/PubMed | PubMed literature search (raises rate limit 3->10 req/s) | Yes | https://account.ncbi.nlm.nih.gov/settings/ |
| `NVIDIA_API_KEY` | NVIDIA NIM | 16 tools: AlphaFold2 structure prediction, molecular docking, genomics | Yes | https://build.nvidia.com |
| `BIOGRID_API_KEY` | BioGRID | Protein-protein interaction queries | Yes | https://webservice.thebiogrid.org/ |
| `DISGENET_API_KEY` | DisGeNET | 5 gene-disease association tools | Yes (academic) | https://disgenet.com/academic-apply |

#### Tier 2: Specialized Scientific Keys (Based on research needs)

| Key | Service | What It Unlocks | Free? | Registration |
|-----|---------|----------------|-------|-------------|
| `OMIM_API_KEY` | OMIM | 4 Mendelian/rare disease tools | Yes | https://omim.org/api |
| `ONCOKB_API_TOKEN` | OncoKB | Precision oncology annotations | Yes (academic) | https://www.oncokb.org/apiAccess |
| `UMLS_API_KEY` | UMLS/NLM | 5 medical terminology & concept mapping tools | Yes | https://uts.nlm.nih.gov/uts/ |
| `USPTO_API_KEY` | USPTO | 6 patent search & analysis tools | Yes | https://account.uspto.gov/api-manager/ |
| `SEMANTIC_SCHOLAR_API_KEY` | Semantic Scholar | Literature search (raises rate limit 1->100 req/s) | Yes | https://www.semanticscholar.org/product/api |
| `FDA_API_KEY` | openFDA | Drug/food/device adverse event queries (raises limit 240->1000 req/min) | Yes | https://open.fda.gov/apis/authentication/ |
| `BRENDA_EMAIL` + `BRENDA_PASSWORD` | BRENDA | 3 enzyme database tools (both email and password required) | Yes | https://brenda-enzymes.org/register.php |

#### Tier 3: LLM Provider Keys (For agentic tool features)

At least **one** LLM key is needed for agentic features. The system tries providers in order: Azure OpenAI -> OpenRouter -> Gemini.

| Key | Service | What It Unlocks | Free Tier? | Registration |
|-----|---------|----------------|-----------|-------------|
| `GEMINI_API_KEY` | Google Gemini | Agentic tools via Gemini (good free tier) | Yes | https://aistudio.google.com/apikey |
| `OPENROUTER_API_KEY` | OpenRouter | Agentic tools via 100+ LLM models | Pay-per-use | https://openrouter.ai/ |
| `OPENAI_API_KEY` | OpenAI | Embedding features, LLM-based tool finding | Pay-per-use | https://platform.openai.com/ |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI | Agentic tools via Azure (enterprise) | Pay-per-use | Azure Portal |
| `ANTHROPIC_API_KEY` | Anthropic Claude | Claude-based features | Pay-per-use | https://console.anthropic.com/ |
| `HF_TOKEN` | HuggingFace | Model/dataset access, HF Inference API | Yes | https://huggingface.co/settings/tokens |

#### Adding Keys to Configuration

**Best approach: Add to the `env` block in your MCP config file** (the same file from Step 2). This way keys are passed directly to the MCP server:

```json
"env": {
  "PYTHONIOENCODING": "utf-8",
  "NCBI_API_KEY": "your_key_here",
  "NVIDIA_API_KEY": "your_key_here"
}
```

**Alternative**: Create a `.env` file in your project directory with `KEY=value` pairs.

**After adding keys**: Restart the app for changes to take effect.

#### Verify keys work

Test each configured key with a real tool call:
- `NCBI_API_KEY` -> `execute_tool("PubMed_search_articles", {"query": "CRISPR", "max_results": 1})`
- `NVIDIA_API_KEY` -> `execute_tool("NvidiaNIM_alphafold2_predict", {"sequence": "MKTVRQERLKS"})`
- `BIOGRID_API_KEY` -> `execute_tool("BioGRID_get_interactions", {"geneList": "TP53", "taxId": 9606})`

### Step 5: Test it together

Time to see it in action! Ask the user to restart their app, then try a real tool call together:

1. **Restart the app** (Cursor/Claude Desktop/etc.) so the new MCP config is picked up
2. **Check the MCP server appears** in the server list
3. **Run a test call** -- suggest something relevant to their research interests:
   - General: `grep_tools` with keyword "protein" or `list_tools`
   - Literature: `execute_tool("PubMed_search_articles", {"query": "CRISPR", "max_results": 1})`
   - Drug discovery: `execute_tool("ChEMBL_search_compound", {"query": "aspirin"})`

If it works, celebrate and move to Step 6. If something goes wrong, check the Common Issues section below.

### Step 6: Install ToolUniverse Skills (Highly Recommended)

**Strongly recommend this step.** Skills are pre-built research workflows that teach the AI how to conduct comprehensive scientific research -- they turn basic tool calls into expert-level investigations.

Explain to the user: "ToolUniverse comes with 19 research skills that act like expert guides. For example, the drug-research skill knows exactly which tools to call, in what order, to build a complete drug profile. Without skills, you'd need to figure out which of the 1200+ tools to use yourself."

#### Available Skills

| Skill | What It Does |
|-------|-------------|
| `tooluniverse` | General strategies for using 1200+ tools effectively |
| `tooluniverse-drug-research` | Comprehensive drug profiling (identity, pharmacology, safety, ADMET) |
| `tooluniverse-target-research` | Drug target intelligence (structure, interactions, druggability) |
| `tooluniverse-disease-research` | Systematic disease analysis across 10 research dimensions |
| `tooluniverse-literature-deep-research` | Thorough literature reviews with evidence grading |
| `tooluniverse-drug-repurposing` | Find new therapeutic uses for existing drugs |
| `tooluniverse-precision-oncology` | Mutation-based treatment recommendations for cancer |
| `tooluniverse-rare-disease-diagnosis` | Phenotype-to-diagnosis for suspected rare diseases |
| `tooluniverse-pharmacovigilance` | Drug safety signal analysis from FDA adverse event data |
| `tooluniverse-infectious-disease` | Rapid pathogen characterization & drug repurposing |
| `tooluniverse-protein-structure-retrieval` | Protein 3D structure retrieval & quality assessment |
| `tooluniverse-sequence-retrieval` | DNA/RNA/protein sequence retrieval from NCBI/ENA |
| `tooluniverse-chemical-compound-retrieval` | Chemical compound data from PubChem/ChEMBL |
| `tooluniverse-expression-data-retrieval` | Gene expression & omics datasets |
| `tooluniverse-variant-interpretation` | Genetic variant clinical interpretation |
| `tooluniverse-protein-therapeutic-design` | AI-guided protein therapeutic design |
| `tooluniverse-binder-discovery` | Small molecule binder discovery via virtual screening |
| `tooluniverse-sdk` | Build research pipelines with the Python SDK |
| `setup-tooluniverse` | This setup guide |

#### How to Install Skills

Skills are in the `skills/` folder of the ToolUniverse GitHub repo: https://github.com/mims-harvard/ToolUniverse/tree/main/skills

First, help the user download the skills:

```bash
# Clone just the skills folder from GitHub
git clone --depth 1 --filter=blob:none --sparse https://github.com/mims-harvard/ToolUniverse.git /tmp/tu-skills
cd /tmp/tu-skills && git sparse-checkout set skills
```

Then install based on their client:

**Cursor** -- copy to `.cursor/skills/` (auto-discovered):
```bash
mkdir -p .cursor/skills && cp -r /tmp/tu-skills/skills/* .cursor/skills/
```

**Windsurf** -- Cascade supports SKILL.md files the same way:
```bash
mkdir -p .windsurf/skills && cp -r /tmp/tu-skills/skills/* .windsurf/skills/
```

**Codex (OpenAI)** -- uses `.agents/skills/` directory (auto-discovered):
```bash
mkdir -p .agents/skills && cp -r /tmp/tu-skills/skills/* .agents/skills/
```

**Gemini CLI** -- uses `.gemini/skills/` directory (auto-discovered):
```bash
mkdir -p .gemini/skills && cp -r /tmp/tu-skills/skills/* .gemini/skills/
```

**Claude Code** -- uses `.claude/skills/` directory (auto-discovered):
```bash
mkdir -p .claude/skills && cp -r /tmp/tu-skills/skills/* .claude/skills/
```

**OpenCode** -- uses `.opencode/skills/` directory (auto-discovered):
```bash
mkdir -p .opencode/skills && cp -r /tmp/tu-skills/skills/* .opencode/skills/
```

**Trae** -- supports skills via `.trae/skills/`:
```bash
mkdir -p .trae/skills && cp -r /tmp/tu-skills/skills/* .trae/skills/
```

**Cline / VS Code / Qwen** -- copy skills into the project and reference as needed:
```bash
mkdir -p .skills && cp -r /tmp/tu-skills/skills/* .skills/
```

**Clean up** after copying:
```bash
rm -rf /tmp/tu-skills
```

#### How to Use Skills

Explain to the user:
- Skills activate automatically when the AI detects a relevant request
- The user can also trigger them explicitly, e.g., "Research the drug aspirin" will activate the drug-research skill
- Skills guide the AI through multi-step research workflows, calling the right tools in the right order
- The output is typically a comprehensive research report with evidence grading and source citations

**Suggest a skill to try** based on their research interests from Step 4. For example:
- "Try asking: 'Research the drug metformin' -- the drug-research skill will generate a full drug profile"
- "Try asking: 'What does the literature say about CRISPR in cancer?' -- the literature-deep-research skill will do a thorough review"

## Common Issues & Solutions

### Issue 1: Python Version Incompatibility

**Symptom**: `requires-python = ">=3.10"` error. **Fix**: `brew install python@3.12` then `python3.12 -m pip install tooluniverse`

### Issue 2: uvx or uv Not Found

**Symptom**: `uvx: command not found`. **Fix**: `curl -LsSf https://astral.sh/uv/install.sh | sh` then restart shell (`source ~/.zshrc`)

### Issue 3: Context Window Overflow

**Symptom**: MCP server loads but Cursor/Claude becomes slow or errors

**Solution**: **Enable compact mode** (should already be set):
- Verify `--compact-mode` is in args
- Restart application
- Check you're using stdio command, not HTTP server

### Issue 4: Import Errors for Specific Tools

**Symptom**: Some tools fail with `ModuleNotFoundError`

**Solution**: Install optional dependencies: `pip install tooluniverse[all]` (or specific extras like `[singlecell]`, `[ml,embedding]`, `[visualization]`)

### Issue 5: MCP Server Won't Start

**Symptom**: No tooluniverse server appears in Cursor/Claude

**Diagnostic steps**:
1. Test command directly:
   ```bash
   uvx tooluniverse
   # Should start without errors (Ctrl+C to exit)
   ```
2. Check JSON syntax in mcp.json (no trailing commas, proper quotes)
3. View Cursor logs: `~/Library/Application Support/Cursor/logs/` (macOS)
4. Verify file permissions on mcp.json

### Issue 6: API Key Errors (401/403)

**Symptom**: Tool returns "unauthorized", "forbidden", or "invalid API key"

**Common causes and fixes**:
- **Key not set**: Check it's in the `env` block of mcp.json (or `.env` file) and app was restarted
- **Wrong key name**: Double-check the exact env variable name (e.g., `ONCOKB_API_TOKEN` not `ONCOKB_API_KEY`)
- **Key expired or revoked**: Log into the service and regenerate the key
- **Copy-paste error**: Make sure there are no extra spaces or newlines in the key value
- **Free tier limits**: Some services (DisGeNET, OMIM) require account approval before the key works

### Issue 7: Upgrading ToolUniverse

**Symptom**: User wants a newer version, or tools are missing/outdated

`uvx` caches packages and may serve an older version. To upgrade:

```bash
# Clear the cached version and get the latest
uv cache clean tooluniverse
```

Then restart the MCP client. `uvx` will download the latest version on next start.

To pin a specific version:
```json
"args": ["tooluniverse==1.0.18"]
```

For pip users:
```bash
pip install --upgrade tooluniverse
```

### Still stuck?

If you run into an issue that can't be resolved with the steps above, encourage the user to open a GitHub issue at https://github.com/mims-harvard/ToolUniverse/issues or reach out to [Shanghua Gao](mailto:shanghuagao@gmail.com), the creator of ToolUniverse.

## What's Next?

After setup is complete, suggest the user try one of these to get started:

- **"Research the drug metformin"** -- triggers the drug-research skill for a full drug profile
- **"What are the known targets of imatinib?"** -- triggers target-research
- **"What does the literature say about CRISPR in sickle cell disease?"** -- triggers literature-deep-research
- **"Find protein structures for human EGFR"** -- triggers protein-structure-retrieval

Point them to the **`tooluniverse` general skill** for tips on getting the most out of 1200+ tools, and remind them they can always come back to add more API keys or skills later.

## Quick Reference

- **Default setup**: `uvx tooluniverse` -- auto-installs, auto-enables compact mode
- **Upgrade**: `uv cache clean tooluniverse` then restart the app
- **First load**: May take 30-60 seconds (downloads + installs); subsequent loads are fast
- **All scientific API keys are free** to obtain
- **Agentic features** need at least one LLM key (Gemini has a good free tier)
- **Detailed API key docs**: [API_KEYS_REFERENCE.md](API_KEYS_REFERENCE.md)
- **Skills repo**: https://github.com/mims-harvard/ToolUniverse/tree/main/skills
- **Need help?** Open a [GitHub issue](https://github.com/mims-harvard/ToolUniverse/issues) or email [Shanghua Gao](mailto:shanghuagao@gmail.com)
