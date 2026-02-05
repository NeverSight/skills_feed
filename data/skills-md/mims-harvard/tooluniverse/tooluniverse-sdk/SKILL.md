---
name: tooluniverse-sdk
description: Build AI scientist systems using ToolUniverse Python SDK for scientific research. Use when users need to access 1000++ scientific tools through Python code, create scientific workflows, perform drug discovery, protein analysis, genomics analysis, literature research, or any computational biology task. Triggers include requests to use scientific tools programmatically, build research pipelines, analyze biological data, search literature, predict drug properties, or create AI-powered scientific workflows.
---

# ToolUniverse Python SDK

ToolUniverse provides programmatic access to 1000++ scientific tools through a unified interface. It implements the AI-Tool Interaction Protocol for building AI scientist systems that integrate ML models, databases, APIs, and scientific packages.

## Installation

```bash
# Standard installation
pip install tooluniverse

# With optional features
pip install tooluniverse[embedding]  # Embedding search (GPU)
pip install tooluniverse[ml]         # ML model tools
pip install tooluniverse[all]        # All features
```

### Environment Setup

```bash
# Required for LLM-based tool search and hooks
export OPENAI_API_KEY="sk-..."

# Optional for higher rate limits
export NCBI_API_KEY="..."
```

Or use `.env` file:

```python
from dotenv import load_dotenv
load_dotenv()
```

## Quick Start

```python
from tooluniverse import ToolUniverse

# 1. Initialize and load tools
tu = ToolUniverse()
tu.load_tools()  # Loads 1000++ tools (~5-10 seconds first time)

# 2. Find tools (three methods)
# Method A: Keyword (fast, no API key)
tools = tu.run({
    "name": "Tool_Finder_Keyword",
    "arguments": {"description": "protein structure", "limit": 10}
})

# Method B: LLM (intelligent, requires OPENAI_API_KEY)
tools = tu.run({
    "name": "Tool_Finder_LLM",
    "arguments": {"description": "predict drug toxicity", "limit": 5}
})

# Method C: Embedding (semantic, requires GPU)
tools = tu.run({
    "name": "Tool_Finder",
    "arguments": {"description": "protein interactions", "limit": 10}
})

# 3. Execute tools (two ways)
# Dictionary API
result = tu.run({
    "name": "UniProt_get_entry_by_accession",
    "arguments": {"accession": "P05067"}
})

# Function API (recommended)
result = tu.tools.UniProt_get_entry_by_accession(accession="P05067")
```

## Core Patterns

### Pattern 1: Discovery → Execute

```python
# Find tools
tools = tu.run({
    "name": "Tool_Finder_Keyword",
    "arguments": {"description": "ADMET prediction", "limit": 3}
})

# Check results structure
if isinstance(tools, dict) and 'tools' in tools:
    for tool in tools['tools']:
        print(f"{tool['name']}: {tool['description']}")

# Execute tool
result = tu.tools.ADMETAI_predict_admet(
    smiles="CC(C)Cc1ccc(cc1)C(C)C(O)=O"
)
```

### Pattern 2: Batch Execution

```python
# Define calls
calls = [
    {"name": "UniProt_get_entry_by_accession", "arguments": {"accession": "P05067"}},
    {"name": "UniProt_get_entry_by_accession", "arguments": {"accession": "P12345"}},
    {"name": "RCSB_PDB_get_structure_by_id", "arguments": {"pdb_id": "1ABC"}}
]

# Execute in parallel
results = tu.run_batch(calls)
```

### Pattern 3: Scientific Workflow

```python
def drug_discovery_pipeline(disease_id):
    tu = ToolUniverse(use_cache=True)
    tu.load_tools()
    
    try:
        # Get targets
        targets = tu.tools.OpenTargets_get_associated_targets_by_disease_efoId(
            efoId=disease_id
        )
        
        # Get compounds (batch)
        compound_calls = [
            {"name": "ChEMBL_search_molecule_by_target", 
             "arguments": {"target_id": t['id'], "limit": 10}}
            for t in targets['data'][:5]
        ]
        compounds = tu.run_batch(compound_calls)
        
        # Predict ADMET
        admet_results = []
        for comp_list in compounds:
            if comp_list and 'molecules' in comp_list:
                for mol in comp_list['molecules'][:3]:
                    admet = tu.tools.ADMETAI_predict_admet(
                        smiles=mol['smiles'],
                        use_cache=True
                    )
                    admet_results.append(admet)
        
        return {"targets": targets, "compounds": compounds, "admet": admet_results}
    finally:
        tu.close()
```

## Configuration

### Caching

```python
# Enable globally
tu = ToolUniverse(use_cache=True)
tu.load_tools()

# Or per-call
result = tu.tools.ADMETAI_predict_admet(
    smiles="...",
    use_cache=True  # Cache expensive predictions
)

# Manage cache
stats = tu.get_cache_stats()
tu.clear_cache()
```

### Hooks (Auto-summarization)

```python
# Enable hooks for large outputs
tu = ToolUniverse(hooks_enabled=True)
tu.load_tools()

result = tu.tools.OpenTargets_get_target_gene_ontology_by_ensemblID(
    ensemblId="ENSG00000012048"
)

# Check if summarized
if isinstance(result, dict) and "summary" in result:
    print(f"Summarized: {result['summary']}")
```

### Load Specific Categories

```python
# Faster loading
tu = ToolUniverse()
tu.load_tools(categories=["proteins", "drugs"])
```

## Critical Things to Know

### ⚠️ Always Call load_tools()

```python
# ❌ Wrong - will fail
tu = ToolUniverse()
result = tu.tools.some_tool()  # Error!

# ✅ Correct
tu = ToolUniverse()
tu.load_tools()
result = tu.tools.some_tool()
```

### ⚠️ Tool Finder Returns Nested Structure

```python
# ❌ Wrong
tools = tu.run({"name": "Tool_Finder_Keyword", "arguments": {"description": "protein"}})
for tool in tools:  # Error: tools is dict
    print(tool['name'])

# ✅ Correct
if isinstance(tools, dict) and 'tools' in tools:
    for tool in tools['tools']:
        print(tool['name'])
```

### ⚠️ Check Required Parameters

```python
# Check tool schema first
tool_info = tu.all_tool_dict["UniProt_get_entry_by_accession"]
required = tool_info['parameter'].get('required', [])
print(f"Required: {required}")

# Then call
result = tu.tools.UniProt_get_entry_by_accession(accession="P05067")
```

### ⚠️ Cache Strategy

```python
# ✅ Cache: ML predictions, database queries (deterministic)
result = tu.tools.ADMETAI_predict_admet(smiles="...", use_cache=True)

# ❌ Don't cache: real-time data, time-sensitive results
result = tu.tools.get_latest_publications()  # No cache
```

### ⚠️ Error Handling

```python
from tooluniverse.exceptions import ToolError, ToolUnavailableError

try:
    result = tu.tools.UniProt_get_entry_by_accession(accession="P05067")
except ToolUnavailableError as e:
    print(f"Tool unavailable: {e}")
except ToolError as e:
    print(f"Execution failed: {e}")
```

### ⚠️ Tool Names Are Case-Sensitive

```python
# ❌ Wrong
result = tu.tools.uniprot_get_entry_by_accession(accession="P05067")

# ✅ Correct
result = tu.tools.UniProt_get_entry_by_accession(accession="P05067")
```

## Execution Options

```python
result = tu.tools.tool_name(
    param="value",
    use_cache=True,      # Cache this call
    validate=True,       # Validate parameters (default)
    stream_callback=None # Streaming output
)
```

## Performance Tips

```python
# 1. Load specific categories
tu.load_tools(categories=["proteins"])

# 2. Use batch execution
results = tu.run_batch(calls)

# 3. Enable caching
tu = ToolUniverse(use_cache=True)

# 4. Disable validation (after testing)
result = tu.tools.tool_name(param="value", validate=False)
```

## Troubleshooting

### Tool Not Found

```python
# Search for tool
tools = tu.run({
    "name": "Tool_Finder_Keyword",
    "arguments": {"description": "partial_name", "limit": 10}
})

# Check if exists
if "Tool_Name" in tu.all_tool_dict:
    print("Found!")
```

### API Key Issues

```python
import os
if not os.environ.get("OPENAI_API_KEY"):
    print("⚠️ OPENAI_API_KEY not set")
    print("Set: export OPENAI_API_KEY='sk-...'")
```

### Validation Errors

```python
from tooluniverse.exceptions import ToolValidationError

try:
    result = tu.tools.some_tool(param="value")
except ToolValidationError as e:
    # Check schema
    tool_info = tu.all_tool_dict["some_tool"]
    print(f"Required: {tool_info['parameter'].get('required', [])}")
    print(f"Properties: {tool_info['parameter']['properties'].keys()}")
```

### Enable Debug Logging

```python
from tooluniverse.logging_config import set_log_level
set_log_level("DEBUG")
```

## Tool Categories

| Category | Tools | Use Cases |
|----------|-------|-----------|
| Proteins | UniProt, RCSB PDB, AlphaFold | Protein analysis, structure |
| Drugs | DrugBank, ChEMBL, PubChem | Drug discovery, compounds |
| Genomics | Ensembl, NCBI Gene, gnomAD | Gene analysis, variants |
| Diseases | OpenTargets, ClinVar | Disease-target associations |
| Literature | PubMed, Europe PMC | Literature search |
| ML Models | ADMET-AI, AlphaFold | Predictions, modeling |
| Pathways | KEGG, Reactome | Pathway analysis |

## Resources

- **Documentation**: https://zitniklab.hms.harvard.edu/ToolUniverse/
- **Tool List**: https://zitniklab.hms.harvard.edu/ToolUniverse/tools/tools_config_index.html
- **GitHub**: https://github.com/mims-harvard/ToolUniverse
- **Examples**: See `examples/` directory in repository
- **Slack**: https://join.slack.com/t/tooluniversehq/shared_invite/zt-3dic3eoio-5xxoJch7TLNibNQn5_AREQ

For detailed guides, see [REFERENCE.md](REFERENCE.md).
