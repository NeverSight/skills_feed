---
name: tooluniverse-custom-tool
description: >
  Add custom local tools to ToolUniverse and use them alongside the 1000+ built-in tools.
  Use this skill when a user wants to: create their own tool for a private or custom API,
  add a local tool to their workspace, integrate an internal service with ToolUniverse,
  or use a custom tool via the MCP server or Python API. Covers both the JSON config
  approach (easiest, no Python needed) and the Python class approach (full control).
  Also covers how to verify tools loaded correctly and how to call them.
  Also covers the plugin package approach for reusable, shareable, pip-installable tool sets.
---

# Adding Custom Tools to ToolUniverse

Three ways to add tools — pick the one that fits your needs:

| Approach | When to use |
|---|---|
| **JSON config** | REST API with standard request/response — no coding needed |
| **Python class (workspace)** | Custom logic for local/private use only |
| **Plugin package** | Reusable tools you want to share or install via pip |

---

## Option A — Workspace tools (local use)

Tools in `.tooluniverse/tools/` are auto-discovered at startup. No installation needed.

```bash
mkdir -p .tooluniverse/tools
```

### JSON config

Create `.tooluniverse/tools/my_tools.json`:

```json
[
  {
    "name": "MyAPI_search",
    "description": "Search my internal database. Returns matching records with id, title, and score.",
    "type": "BaseRESTTool",
    "fields": {
      "endpoint": "https://my-api.example.com/search"
    },
    "parameter": {
      "type": "object",
      "properties": {
        "q": {
          "type": "string",
          "description": "Search query"
        },
        "limit": {
          "type": ["integer", "null"],
          "description": "Max results to return (default 10)"
        }
      },
      "required": ["q"]
    }
  }
]
```

One JSON file can define multiple tools — just add more objects to the array.

For the full JSON field reference, see [references/json-tool.md](references/json-tool.md).

### Python class

Create `.tooluniverse/tools/my_tool.py`:

```python
from tooluniverse.tool_registry import register_tool

@register_tool
class MyAPI_search:
    name = "MyAPI_search"
    description = "Search my internal database. Returns matching records with id, title, and score."
    input_schema = {
        "type": "object",
        "properties": {
            "q": {"type": "string", "description": "Search query"},
            "limit": {"type": "integer", "description": "Max results (default 10)"}
        },
        "required": ["q"]
    }

    def run(self, q: str, limit: int = 10) -> dict:
        import requests
        resp = requests.get(
            "https://my-api.example.com/search",
            params={"q": q, "limit": limit},
            timeout=30,
        )
        resp.raise_for_status()
        return {"status": "success", "data": resp.json()}
```

Note: workspace Python tools use `run(self, **named_params)` — arguments are unpacked as keyword
arguments matching the `input_schema` properties.

For the full Python class reference, see [references/python-tool.md](references/python-tool.md).

### Test workspace tools

```bash
# Uses test_examples from the tool's JSON config — zero config needed
tu test MyAPI_search

# Single ad-hoc call
tu test MyAPI_search '{"q": "test"}'

# Full config with assertions
tu test --config my_tool_tests.json
```

`tu test` automatically runs these checks on every call:
- Result is not None or empty
- `return_schema` validation — validates `result["data"]` against the JSON Schema defined in `return_schema` (if present)
- `expect_status` and `expect_keys` — only if set in the config file

**Gotcha:** `tu test` does NOT verify that results are non-empty. An empty array `[]` satisfies
`"type": "array"` and passes all checks. Make sure your `test_examples` use args that actually
return results — otherwise a completely broken tool can pass all tests silently.


**Verify test_examples manually before finalizing.** Run a quick Python snippet against
the real API with your chosen args BEFORE writing them into `test_examples`. Some APIs require
all query words to appear literally in a title field (`intitle`-style); overly specific queries
like "I2C pull-up resistor value" will return 0 results even though the tool works. Use 2-4 key
words that are reliably present in real content.

Use `urllib` rather than `curl` for API verification — `curl` requires shell quoting tricks and
may not follow redirects correctly, while `urllib` matches what the tool will actually do:

```python
import urllib.request, json
with urllib.request.urlopen("https://api.example.com/search?q=test") as r:
    print(json.dumps(json.loads(r.read()), indent=2))
```

**Also check that the URL is still a real JSON API** before writing any tool code. Some
candidate URLs (e.g. `certification.oshwa.org/api/projects`) may redirect to a GitHub Pages
static site that returns HTML, not JSON. A quick urllib fetch will reveal this immediately.

`my_tool_tests.json` (optional extra assertions):
```json
{
  "tool_name": "MyAPI_search",
  "tests": [
    {
      "name": "basic search",
      "args": {"q": "climate change"},
      "expect_status": "success",
      "expect_keys": ["data"]
    }
  ]
}
```

Add `test_examples` and `return_schema` to your JSON config for best coverage:
```json
{
  "name": "MyAPI_search",
  ...
  "test_examples": [
    {"q": "climate change"},
    {"q": "CRISPR", "limit": 3}
  ],
  "return_schema": {
    "type": "array",
    "items": {
      "type": "object",
      "properties": {
        "id":    { "type": "string" },
        "title": { "type": "string" },
        "score": { "type": "number" }
      }
    }
  }
}
```
`tu test` validates `result["data"]` against `return_schema`. Match the schema type to what
your `run()` returns under the `"data"` key:
- If `data` is a list: `"type": "array"`
- If `data` is a dict: `"type": "object"`

### Use with MCP server

Tools in `.tooluniverse/tools/` are automatically available when you run:

```bash
tu serve          # MCP stdio server (Claude Desktop, etc.)
tooluniverse      # same
```

The workspace directory is auto-detected in this priority order:
`--workspace` flag → `TOOLUNIVERSE_HOME` env var → `./.tooluniverse/` (current dir) → `~/.tooluniverse/` (global)

### Point to a different tools directory

Add a `sources` entry in `.tooluniverse/profile.yaml`:

```yaml
name: my-profile
sources:
  - ./my-custom-tools/    # relative to profile.yaml location
  - /absolute/path/tools/
```

Then start with:
```bash
tu serve --load .tooluniverse/profile.yaml
```

---

## Option B — Plugin package (shareable, pip-installable)

Use this when you want to distribute tools as a reusable Python package that other users can
install with `pip install`. The plugin package has the same directory layout as a workspace, plus a
`pyproject.toml` that declares the entry point.

### Package layout

```
my_project_root/           # directory containing pyproject.toml
    pyproject.toml
    my_tools_package/      # importable Python package (matches entry-point value)
        __init__.py        # minimal — one-line docstring, no registration code
        my_api_tool.py     # tool class(es) with @register_tool
        data/
            my_api_tools.json  # JSON tool configs (type must match registered class name)
        profile.yaml       # optional: name, description, required_env
```

JSON config files are discovered from both `data/` and the package root directory. The convention is `data/`.

### `pyproject.toml` entry point

```toml
[project.entry-points."tooluniverse.plugins"]
my-tools = "my_tools_package"
```

The value (`my_tools_package`) must be the importable Python package name.

### Python class in a plugin package

Plugin package tools use `BaseTool` and receive all arguments as a single `Dict`:

```python
import requests
from typing import Dict, Any
from tooluniverse.base_tool import BaseTool
from tooluniverse.tool_registry import register_tool

@register_tool("MyAPITool")
class MyAPITool(BaseTool):
    """Tool description here."""

    def __init__(self, tool_config: Dict[str, Any]):
        super().__init__(tool_config)
        self.timeout = tool_config.get("timeout", 30)
        fields = tool_config.get("fields", {})
        self.operation = fields.get("operation", "search")

    def run(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        query = arguments.get("query", "")
        if not query:
            return {"error": "query parameter is required"}
        try:
            resp = requests.get(
                "https://my-api.example.com/search",
                params={"q": query},
                timeout=self.timeout,
            )
            resp.raise_for_status()
            return {"status": "success", "data": resp.json()}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
```

Key differences from the workspace pattern:
- Inherit from `BaseTool` (from `tooluniverse.base_tool`)
- `@register_tool("ClassName")` takes the class name as a string argument
- `run(self, arguments: Dict)` receives all arguments in a single dict — extract them with `.get()`
- `__init__` receives `tool_config` dict; call `super().__init__(tool_config)` first

### JSON config in a plugin package

Place configs in `data/my_api_tools.json`. The `"type"` field must match the string passed to
`@register_tool(...)`:

```json
[
  {
    "name": "MyAPI_search",
    "description": "Search my API. Returns matching records.",
    "type": "MyAPITool",
    "fields": { "operation": "search" },
    "parameter": {
      "type": "object",
      "properties": {
        "query": { "type": "string", "description": "Search query" },
        "limit": { "type": ["integer", "null"], "description": "Max results" }
      },
      "required": ["query"]
    }
  }
]
```

### `__init__.py`

Keep it minimal — no registration code needed. The plugin system imports every `.py` file in the
package directory automatically (via `_discover_entry_point_plugins()`), so `@register_tool`
decorators fire on their own:

```python
"""My tools plugin for ToolUniverse."""
```

If you want IDE autocompletion or to make it easy to import specific classes directly, you can
add explicit imports — they are harmless because `@register_tool` is idempotent (registering
the same class twice is a no-op):

```python
"""My tools plugin for ToolUniverse."""

from . import my_api_tool       # optional — for IDE support
from . import my_other_tool     # optional
```

**Do not** add registration logic, JSON loading, or `register_tool_configs()` calls here.
Those run automatically at plugin discovery time.

### Install and verify

```bash
# Install in editable mode — path must point to the directory containing pyproject.toml
pip install -e /path/to/my_project_root

# Verify the entry point is registered
python -c "
from importlib.metadata import entry_points
eps = entry_points(group='tooluniverse.plugins')
print([ep.name for ep in eps])
"

# Test the tool — MUST run from the plugin repo directory
cd /path/to/my_project_root
tu test MyAPI_search '{"query": "test"}'
```

`tu test` finds plugin tools via the installed entry point — the package must be
`pip install -e`'d first. Always run `tu test` from the plugin repo directory (not
from an arbitrary location): ToolUniverse's workspace auto-detection looks for
`.tooluniverse/` in the current directory, which is where the plugin's `profile.yaml`
and any workspace-level config lives.

Add `test_examples` to your JSON config for zero-config testing:
```json
{ "name": "MyAPI_search", ..., "test_examples": [{"query": "test"}] }
```
Then: `tu test MyAPI_search`

**Note:** `tu list` shows tool counts grouped by category, not individual tool names. To confirm
your specific tool loaded, use `tu info MyAPI_search` or run `tu test MyAPI_search` directly.
If "Tool not found", see the gotcha above about the lazy registry refresh.

---

## Offline / pure-computation tools

Calculator tools that perform local math (no HTTP) follow the plugin-package pattern
but skip the HTTP layer entirely. Common designs:

### Preset lookup tables

Define named presets at **module level** as a `Dict[str, float]`, then resolve the
parameter with a priority chain: explicit user value → preset name → default.
Always include the preset table in `metadata` so callers can discover valid names
without reading source code:

```python
_PACKAGE_THETA_JA = {"sot-23": 200.0, "to-220": 50.0, "bga-256": 20.0}

def run(self, arguments):
    theta = arguments.get("theta_ja")
    if theta is None and arguments.get("package"):
        key = arguments["package"].lower()
        if key not in _PACKAGE_THETA_JA:
            return {"status": "error",
                    "message": f"Unknown package. Known: {list(_PACKAGE_THETA_JA)}"}
        theta = _PACKAGE_THETA_JA[key]
    return {
        "status": "success",
        "data": {"theta_ja": theta, ...},
        "metadata": {"package_presets": _PACKAGE_THETA_JA},
    }
```

### Solving the same equation in both directions

When the same formula can be rearranged to solve for different unknowns, expose them
as separate `operation` values with a single runtime-dispatch tool:

```python
# C_min = I × Δt / ΔV  →  also: ΔV = I × Δt / C
op = arguments.get("operation") or self.operation
if op == "solve_capacitance":
    dV = _req_float(arguments, "voltage_droop_V")
    C_min = I * dt / dV
    ...
elif op == "solve_droop":
    C = _req_float(arguments, "capacitance_F")
    dV = I * dt / C
    ...
```

The two directions share a single JSON config entry. Use `"fields": {"operation": "default_op"}`
in the JSON to set the default, and document both modes clearly in the description.

### Physical constants at module level

Define fundamental constants once, near the top of the file, so they appear in code
review and are easy to update:

```python
import math

_MU0   = 4.0 * math.pi * 1e-7   # H/m — permeability of free space
_KB_EV = 8.617333e-5             # eV/K — Boltzmann constant

# Material-specific values as a named dict
_MATERIAL_EA = {"al": 0.7, "cu": 0.9, "w": 1.0}   # activation energy in eV
```

### Multi-output operations

When a single computation naturally yields multiple related results (e.g., Tj AND
headroom AND pass/fail), return them all in `data` rather than forcing a second call:

```python
data = {
    "junction_temp_C":   tj,
    "headroom_C":        tj_max - tj,
    "passes_thermal":    (tj_max - tj) >= 0,
    ...
}
```

For the complete patterns (significant-figure rounding, `_req_float` helper, preset
resolution), see [references/python-tool.md](references/python-tool.md).
