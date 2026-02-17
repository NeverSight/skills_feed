---
name: devtu-auto-discover-apis
description: Automatically discover life science APIs online, create ToolUniverse tools, validate them, and prepare integration PRs. Performs gap analysis to identify missing tool categories, web searches for APIs, automated tool creation using devtu-create-tool patterns, validation with devtu-fix-tool, and git workflow management. Use when expanding ToolUniverse coverage, adding new API integrations, or systematically discovering scientific resources.
---

# Automated Life Science API Discovery & Tool Creation

Discover, create, validate, and integrate life science APIs into ToolUniverse through fully automated workflows with human review checkpoints.

## When to Use This Skill

Use this skill when:
- Expanding ToolUniverse coverage in underrepresented domains
- Systematically discovering new life science APIs and databases
- Building a batch of tools from multiple APIs at once
- Identifying gaps in current ToolUniverse tool coverage
- Automating the tool creation pipeline from discovery to PR
- Adding emerging APIs from recent publications or releases

**Triggers**: "find new APIs", "expand tool coverage", "discover missing tools", "add APIs for [domain]"

---

## Table of Contents

1. [Overview](#overview)
2. [Four-Phase Workflow](#four-phase-workflow)
3. [Phase 1: Discovery & Gap Analysis](#phase-1-discovery--gap-analysis)
4. [Phase 2: Tool Creation](#phase-2-tool-creation)
5. [Phase 3: Validation](#phase-3-validation)
6. [Phase 4: Integration](#phase-4-integration)
7. [Configuration Options](#configuration-options)
8. [Output Artifacts](#output-artifacts)
9. [Quality Gates](#quality-gates)
10. [Common Patterns](#common-patterns)
11. [Troubleshooting](#troubleshooting)

---

## Overview

This skill orchestrates a complete pipeline:

```
Gap Analysis → API Discovery → Tool Creation → Validation → Integration
     ↓              ↓               ↓              ↓            ↓
  Coverage      Web Search      devtu-create   devtu-fix    Git PR
  Report        + Docs          patterns       validation   Ready
```

**Automation Level**: Fully automated with human approval gates at:
- After gap analysis (approve focus areas)
- After tool creation (review generated tools)
- Before PR submission (final review)

**Authentication Handling**: Supports public APIs, API keys, OAuth, and complex authentication schemes

**Output**: Working tool files (.py + .json), validation reports, discovery documentation, and integration-ready PRs

---

## Four-Phase Workflow

### Phase 1: Discovery & Gap Analysis (15-30 minutes)

**Objectives**:
1. Analyze current ToolUniverse tools by domain/category
2. Identify underrepresented areas (gap domains)
3. Search web for APIs in gap domains
4. Scrape API documentation for endpoints and schemas
5. Generate discovery report with prioritized candidates

**Key Activities**:
- Load ToolUniverse and categorize existing tools
- Calculate coverage metrics by domain
- Execute targeted web searches for gaps
- Extract API metadata from documentation
- Score APIs by quality, coverage, and integration feasibility

**Output**: `discovery_report.md` with prioritized API candidates

### Phase 2: Tool Creation (30-60 minutes per API)

**Objectives**:
1. Design tool architecture (multi-operation vs single-operation)
2. Generate Python tool classes following devtu-create-tool patterns
3. Create JSON configurations with proper schemas
4. Handle authentication (API keys, OAuth, tokens)
5. Generate realistic test examples

**Key Activities**:
- Map API endpoints to ToolUniverse operations
- Generate tool class with error handling
- Create return schemas with oneOf + data wrapper structure
- Find real test IDs from API documentation
- Register in default_config.py

**Output**: `.py` and `.json` files for each tool

### Phase 3: Validation (10-20 minutes per tool)

**Objectives**:
1. Run automated schema validation
2. Execute integration tests with real API calls
3. Verify devtu compliance (6-step checklist)
4. Check tool loading in ToolUniverse
5. Generate validation reports

**Key Activities**:
- Run `python scripts/test_new_tools.py <tool> -v`
- Verify return_schema has oneOf structure
- Test examples use real IDs (no placeholders)
- Confirm tools load into ToolUniverse registry
- Apply devtu-fix-tool patterns for any failures

**Output**: `validation_report.md` with pass/fail metrics

### Phase 4: Integration (5-10 minutes)

**Objectives**:
1. Create git branch for new tools
2. Commit tools with descriptive messages
3. Generate PR with full documentation
4. Include discovery notes and validation results

**Key Activities**:
- Create feature branch: `feature/add-<api-name>-tools`
- Commit tool files with Co-Authored-By Claude
- Write PR description with API info, tool list, validation results
- Push to remote and create PR

**Output**: Integration-ready PR for human review

---

## Phase 1: Discovery & Gap Analysis

### Step 1.1: Analyze Current Coverage

**Load and categorize existing tools**:

1. Initialize ToolUniverse and load all tools
2. Extract tool names and descriptions
3. Categorize by domain using keywords:
   - Genomics: sequence, genome, gene, variant, SNP
   - Proteomics: protein, structure, PDB, fold, domain
   - Drug Discovery: drug, compound, molecule, ligand, ADMET
   - Clinical: disease, patient, trial, phenotype, diagnosis
   - Omics: expression, transcriptome, metabolome, proteome
   - Imaging: microscopy, imaging, scan, radiology
   - Literature: pubmed, citation, publication, article
   - Pathways: pathway, network, interaction, signaling
   - Systems Biology: model, simulation, flux, dynamics

4. Count tools per category
5. Calculate coverage percentages

**Output**: Coverage matrix with tool counts

### Step 1.2: Identify Gap Domains

**Find underrepresented areas**:

**Gap Detection Criteria**:
- **Critical Gap**: <5 tools in category (or 0 tools)
- **Moderate Gap**: 5-15 tools but missing key subcategories
- **Emerging Gap**: New technologies not yet represented

**Common Gap Areas** (as of 2026):
- Single-cell genomics (spatial transcriptomics, ATAC-seq)
- Metabolomics databases (metabolite structures, pathways)
- Patient registries (rare disease, specific conditions)
- Clinical variant databases (somatic, germline beyond ClinVar)
- Microbial genomics (metagenomics, pathogen databases)
- Multi-omics integration platforms
- Synthetic biology tools (parts, circuits, chassis)
- Toxicology databases
- Agricultural genomics

**Prioritization Factors**:
1. **Impact**: How many researchers need this?
2. **Complementarity**: Fills existing workflow gaps?
3. **Quality**: Well-documented, maintained API?
4. **Accessibility**: Public or simple authentication?
5. **Freshness**: Recent updates, active development?

### Step 1.3: Web Search for Gap APIs

**Search Strategy**:

For each gap domain, execute multiple search queries:

1. **Direct API Search**:
   - "[domain] API REST JSON"
   - "[domain] database API documentation"
   - "[domain] web services programmatic access"

2. **Database Discovery**:
   - "[domain] public database"
   - "list of [domain] databases"
   - "[domain] resources bioinformatics"

3. **Recent Releases**:
   - "[domain] API 2025 OR 2026"
   - "new [domain] database"

4. **Academic Sources**:
   - "[domain] database" site:nar.oxfordjournals.org (NAR Database Issue)
   - "[domain] tool" site:bioinformatics.oxfordjournals.org

**Documentation Extraction**:

For each discovered API:
1. Find base URL and version
2. List available endpoints
3. Identify authentication method
4. Extract parameter schemas
5. Find example requests/responses
6. Check rate limits and terms of service

### Step 1.4: Score and Prioritize APIs

**Scoring Matrix** (0-100 points):

| Criterion | Max Points | Evaluation |
|-----------|------------|------------|
| Documentation Quality | 20 | OpenAPI/Swagger=20, detailed docs=15, basic=10, poor=5 |
| API Stability | 15 | Versioned+stable=15, versioned=10, unversioned=5 |
| Authentication | 15 | Public/API-key=15, OAuth=10, complex=5 |
| Coverage | 15 | Comprehensive=15, good=10, limited=5 |
| Maintenance | 10 | Active (updates <6mo)=10, moderate=6, stale=2 |
| Community | 10 | Popular (citations/stars)=10, moderate=6, unknown=2 |
| License | 10 | Open/Academic=10, free commercial=7, restricted=3 |
| Rate Limits | 5 | Generous=5, moderate=3, restrictive=1 |

**Prioritization**:
- **High Priority (≥70 points)**: Implement immediately
- **Medium Priority (50-69)**: Implement if time permits
- **Low Priority (<50)**: Document for future consideration

### Step 1.5: Generate Discovery Report

**Report Structure**:

```markdown
# API Discovery Report
Generated: [Timestamp]

## Executive Summary
- Total APIs discovered: X
- High priority: Y
- Gap domains addressed: Z

## Coverage Analysis
[Table showing tool counts by category, gaps highlighted]

## Prioritized API Candidates

### High Priority

#### 1. [API Name]
- **Domain**: [Category]
- **Score**: [Points]/100
- **Base URL**: [URL]
- **Auth**: [Method]
- **Endpoints**: [Count]
- **Rationale**: [Why this fills a gap]
- **Example Operations**:
  - Operation 1: Description
  - Operation 2: Description

[Repeat for each high-priority API]

## Medium Priority
[Similar structure]

## Implementation Roadmap
1. Batch 1 (Week 1): [APIs]
2. Batch 2 (Week 2): [APIs]

## Appendix: Search Methodology
[Search queries used, sources consulted]
```

---

## Phase 2: Tool Creation

### Step 2.1: Design Tool Architecture

**Decision Tree**:

```
API has multiple endpoints?
  ├─ YES → Multi-operation tool (single class, multiple JSON wrappers)
  └─ NO → Consider if more endpoints likely in future
       ├─ YES → Still use multi-operation (future-proof)
       └─ NO → Single-operation acceptable
```

**Multi-Operation Pattern** (Recommended):
- One Python class handles all operations
- Each endpoint gets a JSON wrapper
- Operations routed via `operation` parameter

**File Naming**:
- Python: `src/tooluniverse/[api_name]_tool.py`
- JSON: `src/tooluniverse/data/[api_name]_tools.json`
- Category key: `[api_category]` (lowercase, underscores)

### Step 2.2: Generate Python Tool Class

**Template Structure**:

```python
from typing import Dict, Any
from tooluniverse.tool import BaseTool
from tooluniverse.tool_utils import register_tool
import requests
import os

@register_tool("[APIName]Tool")
class [APIName]Tool(BaseTool):
    """Tool for [API Name] - [brief description]."""

    BASE_URL = "[API base URL]"

    def __init__(self, tool_config):
        super().__init__(tool_config)
        self.parameter = tool_config.get("parameter", {})
        self.required = self.parameter.get("required", [])
        # For optional API keys
        self.api_key = os.environ.get("[API_KEY_NAME]", "")

    def run(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Route to operation handler."""
        operation = arguments.get("operation")

        if not operation:
            return {"status": "error", "error": "Missing required parameter: operation"}

        # Route to handlers
        if operation == "operation1":
            return self._operation1(arguments)
        elif operation == "operation2":
            return self._operation2(arguments)
        else:
            return {"status": "error", "error": f"Unknown operation: {operation}"}

    def _operation1(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Description of operation1."""
        # Validate required parameters
        param1 = arguments.get("param1")
        if not param1:
            return {"status": "error", "error": "Missing required parameter: param1"}

        try:
            # Build request
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"

            # Make API call
            response = requests.get(
                f"{self.BASE_URL}/endpoint",
                params={"param1": param1},
                headers=headers,
                timeout=30
            )
            response.raise_for_status()

            # Parse response
            data = response.json()

            # Return with data wrapper
            return {
                "status": "success",
                "data": data.get("results", []),
                "metadata": {
                    "total": data.get("total", 0),
                    "source": "[API Name]"
                }
            }

        except requests.exceptions.Timeout:
            return {"status": "error", "error": "API timeout after 30 seconds"}
        except requests.exceptions.HTTPError as e:
            return {"status": "error", "error": f"HTTP {e.response.status_code}: {e.response.text[:200]}"}
        except Exception as e:
            return {"status": "error", "error": f"Unexpected error: {str(e)}"}
```

**Critical Requirements**:
- Always return `{"status": "success|error", "data": {...}}`
- NEVER raise exceptions in `run()` method
- Set timeout on all HTTP requests (30s recommended)
- Handle specific exceptions (Timeout, HTTPError, ConnectionError)
- Include helpful error messages with context

### Step 2.3: Generate JSON Configuration

**Template Structure**:

```json
[
  {
    "name": "[APIName]_operation1",
    "class": "[APIName]Tool",
    "description": "[What it does]. Returns [data format]. [Input details]. Example: [usage example]. [Special notes].",
    "parameter": {
      "type": "object",
      "required": ["operation", "param1"],
      "properties": {
        "operation": {
          "const": "operation1",
          "description": "Operation identifier (fixed)"
        },
        "param1": {
          "type": "string",
          "description": "Description of param1 with format/constraints"
        }
      }
    },
    "return_schema": {
      "oneOf": [
        {
          "type": "object",
          "properties": {
            "data": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "id": {"type": "string"},
                  "name": {"type": "string"}
                }
              }
            },
            "metadata": {
              "type": "object",
              "properties": {
                "total": {"type": "integer"},
                "source": {"type": "string"}
              }
            }
          }
        },
        {
          "type": "object",
          "properties": {
            "error": {"type": "string"}
          },
          "required": ["error"]
        }
      ]
    },
    "test_examples": [
      {
        "operation": "operation1",
        "param1": "real_value_from_api_docs"
      }
    ]
  }
]
```

**Critical Requirements**:
- **return_schema MUST have oneOf**: Success schema + error schema
- **Success schema MUST have data field**: Top-level `data` wrapper required
- **test_examples MUST use real IDs**: NO "TEST", "DUMMY", "PLACEHOLDER", "example_*"
- **Tool name ≤55 characters**: For MCP compatibility
- **Description 150-250 chars**: Include what, format, example, special notes

### Step 2.4: Handle Authentication

**Authentication Patterns**:

#### Pattern 1: Public API (No Auth)
```python
# No special handling needed
response = requests.get(url, params=params, timeout=30)
```

#### Pattern 2: API Key (Optional)
```python
# In __init__
self.api_key = os.environ.get("API_KEY_NAME", "")

# In JSON config
"optional_api_keys": ["API_KEY_NAME"],
"description": "... Rate limits: 3 req/sec without key, 10 req/sec with API_KEY_NAME."

# In request
headers = {}
if self.api_key:
    headers["Authorization"] = f"Bearer {self.api_key}"
response = requests.get(url, headers=headers, timeout=30)
```

#### Pattern 3: API Key (Required)
```python
# In __init__
self.api_key = os.environ.get("API_KEY_NAME")
if not self.api_key:
    raise ValueError("API_KEY_NAME environment variable required")

# In JSON config
"required_api_keys": ["API_KEY_NAME"]

# In request
headers = {"Authorization": f"Bearer {self.api_key}"}
response = requests.get(url, headers=headers, timeout=30)
```

#### Pattern 4: OAuth (Complex)
```python
# Document in skill: requires manual OAuth setup
# Store tokens in environment
# Implement token refresh logic
# Include example OAuth flow in documentation
```

### Step 2.5: Find Real Test Examples

**Strategy**: List → Get pattern

1. **Find List Endpoint**: Identify endpoint that lists resources
2. **Extract Real ID**: Call list endpoint, extract first valid ID
3. **Test Get Endpoint**: Verify ID works in detail endpoint
4. **Document in test_examples**: Use discovered real ID

**Example Process**:
```
1. API docs show: GET /items → returns [{id: "ABC123", ...}]
2. Make request: curl https://api.example.com/items
3. Extract: id = "ABC123"
4. Verify: curl https://api.example.com/items/ABC123 → 200 OK
5. Use in test_examples: {"operation": "get_item", "item_id": "ABC123"}
```

**Fallback**: Search API documentation examples, tutorial code, or forum posts for real IDs

### Step 2.6: Register in default_config.py

**Add to `src/tooluniverse/default_config.py`**:

```python
TOOLS_CONFIGS = {
    # ... existing entries ...
    "[api_category]": os.path.join(current_dir, "data", "[api_name]_tools.json"),
}
```

**Critical**: This step is commonly missed! Tools won't load without it.

---

## Phase 3: Validation

### Step 3.1: Schema Validation

**Check return_schema structure**:

```python
import json

with open("src/tooluniverse/data/[api_name]_tools.json") as f:
    tools = json.load(f)

for tool in tools:
    schema = tool.get("return_schema", {})

    # Must have oneOf
    assert "oneOf" in schema, f"{tool['name']}: Missing oneOf in return_schema"

    # oneOf must have 2 schemas (success + error)
    assert len(schema["oneOf"]) == 2, f"{tool['name']}: oneOf must have 2 schemas"

    # Success schema must have 'data' field
    success_schema = schema["oneOf"][0]
    assert "properties" in success_schema, f"{tool['name']}: Missing properties in success schema"
    assert "data" in success_schema["properties"], f"{tool['name']}: Missing 'data' field in success schema"

    print(f"✅ {tool['name']}: Schema valid")
```

### Step 3.2: Test Example Validation

**Check for placeholder values**:

```python
PLACEHOLDER_PATTERNS = [
    "test", "dummy", "placeholder", "example", "sample",
    "xxx", "temp", "fake", "mock", "your_"
]

for tool in tools:
    examples = tool.get("test_examples", [])

    for i, example in enumerate(examples):
        for key, value in example.items():
            if isinstance(value, str):
                value_lower = value.lower()
                if any(pattern in value_lower for pattern in PLACEHOLDER_PATTERNS):
                    print(f"❌ {tool['name']}: test_examples[{i}][{key}] contains placeholder: {value}")
                else:
                    print(f"✅ {tool['name']}: test_examples[{i}][{key}] appears real")
```

### Step 3.3: Tool Loading Verification

**Verify three-step registration**:

```python
import sys
sys.path.insert(0, 'src')

# Step 1: Check class registered
from tooluniverse.tool_registry import get_tool_registry
import tooluniverse.[api_name]_tool
registry = get_tool_registry()
assert "[APIName]Tool" in registry, "❌ Step 1 FAILED: Class not registered"
print("✅ Step 1: Class registered")

# Step 2: Check config registered
from tooluniverse.default_config import TOOLS_CONFIGS
assert "[api_category]" in TOOLS_CONFIGS, "❌ Step 2 FAILED: Config not in default_config.py"
print("✅ Step 2: Config registered")

# Step 3: Check wrappers generated
from tooluniverse import ToolUniverse
tu = ToolUniverse()
tu.load_tools()
assert hasattr(tu.tools, '[APIName]_operation1'), "❌ Step 3 FAILED: Wrapper not generated"
print("✅ Step 3: Wrappers generated")

print("✅ All registration steps complete!")
```

### Step 3.4: Integration Tests

**Run test_new_tools.py**:

```bash
# Test specific tools
python scripts/test_new_tools.py [api_name] -v

# Expected output:
# Testing [APIName]_operation1...
# ✅ PASS - Schema valid
#
# Results:
# Total: 3 tests
# Passed: 3 (100.0%)
# Failed: 0
# Schema invalid: 0
```

**Handle failures**:
- **404 ERROR**: Invalid test example ID → find real ID
- **Schema Mismatch**: return_schema doesn't match response → fix schema
- **Timeout**: API slow/down → increase timeout or add retry
- **Parameter Error**: Wrong parameter names → verify with API docs

### Step 3.5: Generate Validation Report

**Report Structure**:

```markdown
# Validation Report: [API Name]
Generated: [Timestamp]

## Summary
- Total tools: X
- Passed: Y (Z%)
- Failed: N
- Schema issues: M

## Tool Loading
- [x] Class registered in tool_registry
- [x] Config registered in default_config.py
- [x] Wrappers generated in tools/

## Schema Validation
- [x] All tools have oneOf structure
- [x] All success schemas have data wrapper
- [x] All error schemas have error field

## Test Examples
- [x] No placeholder values detected
- [x] All examples use real IDs

## Integration Tests

### [APIName]_operation1
- Status: ✅ PASS
- Response time: 1.2s
- Schema: Valid

### [APIName]_operation2
- Status: ✅ PASS
- Response time: 0.8s
- Schema: Valid

## Issues Found
None - all tests passing!

## devtu Compliance Checklist
1. [x] Tool Loading: Verified
2. [x] API Verification: Checked against docs
3. [x] Error Pattern Detection: None found
4. [x] Schema Validation: All valid
5. [x] Test Examples: All real IDs
6. [x] Parameter Verification: Matched API requirements

## Conclusion
All tools ready for integration.
```

---

## Phase 4: Integration

### Step 4.1: Create Git Branch

```bash
# Create feature branch
git checkout -b feature/add-[api-name]-tools

# Verify clean state
git status
```

### Step 4.2: Commit Tool Files

**Commit structure**:

```bash
# Stage tool files
git add src/tooluniverse/[api_name]_tool.py
git add src/tooluniverse/data/[api_name]_tools.json
git add src/tooluniverse/default_config.py

# Commit with descriptive message
git commit -m "$(cat <<'EOF'
Add [API Name] tools for [domain]

Implements X tools for [API Name] API:
- [APIName]_operation1: Description
- [APIName]_operation2: Description
- [APIName]_operation3: Description

API Details:
- Base URL: [URL]
- Authentication: [Method]
- Documentation: [URL]

Coverage:
- Addresses gap in [domain] tools
- Enables [use cases]

Validation:
- All tests passing (X/X passed)
- 100% schema validation
- Real test examples verified

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

### Step 4.3: Generate PR Description

**PR Template**:

```markdown
# Add [API Name] Tools

## Summary
Adds X new tools integrating the [API Name] API for [domain] research.

## Motivation
Current ToolUniverse has limited coverage in [domain]. These tools fill critical gaps:
- Gap 1: [Description]
- Gap 2: [Description]

## API Information
- **Name**: [API Name]
- **Base URL**: [URL]
- **Documentation**: [URL]
- **Authentication**: [Method]
- **Rate Limits**: [Details]
- **License**: [License type]

## Tools Added

| Tool Name | Operation | Description |
|-----------|-----------|-------------|
| [APIName]_operation1 | operation1 | [Description] |
| [APIName]_operation2 | operation2 | [Description] |

## Validation Results

✅ All tests passing (X/X passed)
✅ 100% schema validation
✅ Real test examples verified
✅ devtu compliance checklist complete

### Test Output
```
Testing [APIName] tools...
Total: X tests
Passed: X (100.0%)
Failed: 0
Schema invalid: 0
```

## Files Changed
- `src/tooluniverse/[api_name]_tool.py` - Tool implementation
- `src/tooluniverse/data/[api_name]_tools.json` - Tool configurations
- `src/tooluniverse/default_config.py` - Registration

## Discovery & Prioritization
- **Discovery Score**: [Score]/100
- **Priority**: High
- **Rationale**: [Why this API was prioritized]

## Usage Examples

```python
from tooluniverse import ToolUniverse

tu = ToolUniverse()
tu.load_tools()

# Example 1: [Operation 1]
result = tu.tools.[APIName]_operation1(
    operation="operation1",
    param1="value"
)

# Example 2: [Operation 2]
result = tu.tools.[APIName]_operation2(
    operation="operation2",
    param1="value"
)
```

## Related Issues
- Closes #[issue number if applicable]
- Addresses gap identified in [previous discussion/issue]

## Checklist
- [x] All tests passing
- [x] Schema validation complete
- [x] Real test examples
- [x] No placeholder values
- [x] Tool names ≤55 chars
- [x] default_config.py updated
- [x] Documentation clear
- [x] Error handling comprehensive

## Additional Notes
[Any special considerations, limitations, or future enhancements]

---

**Generated by devtu-auto-discover-apis skill**
Discovery Report: [link to discovery_report.md]
Validation Report: [link to validation_report.md]
```

### Step 4.4: Push and Create PR

```bash
# Push branch to remote
git push -u origin feature/add-[api-name]-tools

# Create PR using gh CLI
gh pr create \
  --title "Add [API Name] tools for [domain]" \
  --body-file pr_description.md \
  --label "enhancement,tools"

# Get PR URL
gh pr view --web
```

---

## Configuration Options

### Agent Configuration

```yaml
# config.yaml (optional)
discovery:
  focus_domains:
    - "metabolomics"
    - "single-cell"
  exclude_domains:
    - "deprecated_category"
  max_apis_per_batch: 5

search:
  max_results_per_query: 20
  include_academic_sources: true
  date_filter: "2024-2026"

creation:
  architecture: "multi-operation"  # or "auto-detect"
  include_async_support: true
  timeout_seconds: 30

validation:
  run_integration_tests: true
  require_100_percent_pass: true
  max_retries: 3

integration:
  auto_create_pr: false  # Require manual approval
  branch_prefix: "feature/add-"
  pr_labels: ["enhancement", "tools"]
```

### User Inputs

**Required**:
- None (fully automated with defaults)

**Optional**:
- `focus_domains`: List of specific domains to prioritize
- `api_names`: Specific APIs to integrate (skip discovery)
- `batch_size`: Number of APIs to process in one run
- `auto_approve`: Skip human approval gates (not recommended)

---

## Output Artifacts

### Generated During Execution

1. **discovery_report.md**
   - Coverage analysis
   - Gap identification
   - Prioritized API candidates
   - Implementation roadmap

2. **[api_name]_tool.py** (per API)
   - Python tool class implementation
   - Error handling
   - Authentication logic

3. **[api_name]_tools.json** (per API)
   - Tool configurations
   - Parameter schemas
   - Return schemas
   - Test examples

4. **validation_report.md** (per API)
   - Schema validation results
   - Integration test results
   - devtu compliance checklist
   - Issues found and resolved

5. **pr_description.md** (per batch)
   - Comprehensive PR description
   - Validation results
   - Usage examples

### Persistent Logs

- **discovery_log.json**: All APIs discovered with metadata
- **creation_log.json**: Tool creation decisions and rationale
- **validation_log.json**: Detailed test results
- **integration_log.json**: Git operations and PR links

---

## Quality Gates

### Gate 1: Post-Discovery (Human Approval)

**Review**: discovery_report.md

**Decision**:
- ✅ Approve: Prioritization looks good → proceed to creation
- 🔄 Modify: Change priorities, focus domains
- ❌ Abort: No suitable APIs found

### Gate 2: Post-Creation (Human Approval)

**Review**: Generated .py and .json files

**Decision**:
- ✅ Approve: Implementation looks good → proceed to validation
- 🔄 Modify: Adjust parameters, schemas, examples
- ❌ Abort: API integration not feasible

### Gate 3: Post-Validation (Human Approval)

**Review**: validation_report.md

**Decision**:
- ✅ Approve: All tests passing → proceed to integration
- 🔄 Fix: Apply devtu-fix-tool patterns, retry validation
- ❌ Abort: Fundamental issues with API

### Gate 4: Pre-PR (Human Approval)

**Review**: Full PR description

**Decision**:
- ✅ Approve: Create PR and push
- 🔄 Modify: Edit commit messages, PR description
- ❌ Abort: Not ready for integration

---

## Common Patterns

### Pattern 1: Batch Processing

Process multiple APIs in one execution:

```
Discovery → [API1, API2, API3] → Create All → Validate All → Single PR
```

**Benefits**: Efficient, cohesive PR
**Use When**: APIs from same domain, similar structure

### Pattern 2: Iterative Single-API

Process one API at a time with validation:

```
Discovery → API1 → Create → Validate → Integrate
         → API2 → Create → Validate → Integrate
```

**Benefits**: Catch issues early, smaller PRs
**Use When**: APIs have complex authentication, novel patterns

### Pattern 3: Discovery-Only Mode

Just discover and document APIs, create tools later:

```
Discovery → Generate Report → [Manual Review] → Schedule Implementation
```

**Benefits**: Rapid survey of landscape
**Use When**: Planning long-term roadmap, research phase

### Pattern 4: Validation-Only Mode

Validate previously created tools:

```
[Existing Tools] → Validation → Fix Issues → Re-validate → Report
```

**Benefits**: Quality assurance for existing tools
**Use When**: Reviewing PRs, auditing tool quality

---

## Troubleshooting

### Issue 1: API Documentation Not Found

**Symptom**: Web search finds API reference but no programmatic docs

**Solutions**:
1. Check for OpenAPI/Swagger spec (often at `/api/docs` or `/openapi.json`)
2. Look for SDKs in GitHub (reverse-engineer from SDK code)
3. Inspect browser network tab on web interface
4. Contact API provider for documentation
5. Document as "low priority" for future manual integration

### Issue 2: Authentication Too Complex

**Symptom**: OAuth flow requires interactive login, token management

**Solutions**:
1. Document OAuth setup in skill README
2. Implement token refresh logic
3. Use environment variables for tokens
4. Create setup guide for users
5. Consider if API worth the complexity

### Issue 3: No Real Test Examples Available

**Symptom**: Can't find valid IDs for test_examples

**Solutions**:
1. Use List endpoint to discover IDs
2. Search API documentation for examples
3. Check API GitHub issues/discussions for sample data
4. Use API playground/sandbox if available
5. Contact API provider for test IDs
6. Last resort: Create test data via API POST endpoints

### Issue 4: Tools Won't Load

**Symptom**: ToolUniverse doesn't see new tools

**Solutions**:
1. Check `default_config.py` registration (Step 2 of 3-step process)
2. Verify JSON syntax: `python -m json.tool file.json`
3. Check class decorator: `@register_tool("ClassName")`
4. Run verification script (see Phase 3, Step 3.3)
5. Clear Python cache: `find . -type d -name __pycache__ -exec rm -rf {} +`
6. Regenerate wrappers: `python -m tooluniverse.generate_tools --force`

### Issue 5: Schema Validation Fails

**Symptom**: return_schema doesn't match actual API response

**Solutions**:
1. Call API directly, inspect raw response
2. Update return_schema to match actual structure
3. Add nullable types for optional fields: `{"type": ["string", "null"]}`
4. Use oneOf for fields with multiple possible structures
5. Ensure data wrapper in success schema
6. Check for nested data structures

### Issue 6: Rate Limits Hit During Testing

**Symptom**: API returns 429 Too Many Requests

**Solutions**:
1. Add rate limiting to tool: `time.sleep(1)` between requests
2. Use optional API key if available (higher limits)
3. Reduce number of test examples
4. Implement exponential backoff on retry
5. Document rate limits in tool description

### Issue 7: API Changed Since Documentation

**Symptom**: Parameters/endpoints don't match docs

**Solutions**:
1. Check API version (may need to specify in base URL)
2. Look for API changelog or migration guide
3. Test with different API versions
4. Update documentation URL to correct version
5. Contact API maintainers about discrepancy

---

## Advanced Features

### Async Polling Support

For job-based APIs (submit → poll → retrieve):

```python
def _submit_job(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Submit job and poll for completion."""
    # Submit
    submit_resp = requests.post(
        f"{self.BASE_URL}/jobs",
        json={"data": arguments.get("data")},
        timeout=30
    )
    job_id = submit_resp.json().get("job_id")

    # Poll (with timeout)
    for attempt in range(60):  # 2 min max
        status_resp = requests.get(
            f"{self.BASE_URL}/jobs/{job_id}",
            timeout=30
        )
        result = status_resp.json()

        if result.get("status") == "completed":
            return {"status": "success", "data": result.get("results")}
        elif result.get("status") == "failed":
            return {"status": "error", "error": result.get("error")}

        time.sleep(2)

    return {"status": "error", "error": "Job timeout after 2 minutes"}
```

**JSON Config**:
```json
{
  "is_async": true,
  "poll_interval": 2,
  "max_wait_time": 120
}
```

### SOAP API Support

For SOAP-based APIs:

```python
# Add operation parameter
def run(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
    operation = arguments.get("operation")
    if not operation:
        return {"status": "error", "error": "SOAP APIs require 'operation' parameter"}
    # ... rest of implementation
```

**JSON Config**:
```json
{
  "parameter": {
    "properties": {
      "operation": {
        "const": "search_items",
        "description": "SOAP operation name (required)"
      }
    }
  }
}
```

### Pagination Handling

For paginated APIs:

```python
def _list_all(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Fetch all pages."""
    all_results = []
    page = 1

    while True:
        response = requests.get(
            f"{self.BASE_URL}/items",
            params={"page": page, "limit": 100},
            timeout=30
        )
        data = response.json()

        results = data.get("results", [])
        if not results:
            break

        all_results.extend(results)

        if len(results) < 100:  # Last page
            break

        page += 1

    return {
        "status": "success",
        "data": all_results,
        "metadata": {"total_pages": page, "total_items": len(all_results)}
    }
```

---

## Success Criteria

### Discovery Phase Success
- ✅ Coverage analysis complete with tool counts
- ✅ ≥3 high-priority APIs identified
- ✅ API documentation URLs verified accessible
- ✅ Authentication methods documented
- ✅ Discovery report generated

### Creation Phase Success
- ✅ All tool classes implement `@register_tool()`
- ✅ All JSON configs have proper structure
- ✅ return_schema has oneOf with data wrapper
- ✅ test_examples use real IDs (no placeholders)
- ✅ Tool names ≤55 characters
- ✅ default_config.py updated

### Validation Phase Success
- ✅ All tools load into ToolUniverse
- ✅ test_new_tools.py shows 100% pass rate
- ✅ No schema validation errors
- ✅ devtu compliance checklist complete
- ✅ Validation report generated

### Integration Phase Success
- ✅ Git branch created successfully
- ✅ Commits follow format with Co-Authored-By
- ✅ PR description comprehensive
- ✅ PR created and URL provided
- ✅ All files included in PR

---

## Maintenance

### Updating Discovered APIs

Re-run discovery periodically to find:
- New APIs in existing domains
- Emerging technologies (new domains)
- API version updates
- Deprecated APIs to remove

**Recommended**: Quarterly discovery runs

### Monitoring Tool Health

Track tool success rates:
```python
# Periodic health check
from tooluniverse import ToolUniverse

tu = ToolUniverse()
tu.load_tools()

for tool_name in tu.all_tool_dict.keys():
    # Run with test_examples
    # Log success/failure rates
    # Alert on degradation
```

### Gap Analysis Automation

Set up automated gap detection:
1. Weekly: Scan ToolUniverse for new tools
2. Update coverage metrics
3. Compare with target coverage goals
4. Generate gap report
5. Trigger discovery for critical gaps

---

## Summary

The `devtu-auto-discover-apis` skill provides a complete automation pipeline for:

1. **Discovery**: Systematic identification of API gaps and candidates
2. **Creation**: Automated tool generation following devtu-create-tool patterns
3. **Validation**: Comprehensive testing with devtu-fix-tool integration
4. **Integration**: Git workflow management with PR generation

**Key Benefits**:
- Reduces manual tool creation time by 80%
- Ensures consistent quality through automated validation
- Systematic gap filling improves ToolUniverse coverage
- Lowers barrier to adding new APIs

**Best Practices**:
- Always verify API documentation before creation
- Use real test examples (never placeholders)
- Follow devtu validation workflow strictly
- Include human approval at quality gates
- Document authentication requirements clearly

Apply this skill to systematically expand ToolUniverse with high-quality, validated tools for life science research.
