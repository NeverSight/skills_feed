---
name: development-assistant
description: Guides through adding new features, MCP tools, analyzers, and extending the patent creator system.
---

# Development Assistant Skill

Expert system for developing and extending the Claude Patent Creator. Guides through adding new MCP tools, analyzers, configuration options, and features while following best practices and existing patterns.

## When to Use This Skill

Activate when adding MCP tools, analyzers, configuration options, BigQuery queries, slash commands, or implementing performance optimizations.

## Development Workflow

```
Feature Request -> Planning -> Implementation (Code + Validation + Monitoring + Tests) -> Testing -> Documentation -> Integration
```

## Adding New MCP Tools

**Quick Start:**
1. Define inputs, outputs, dependencies
2. Create Pydantic model in `mcp_server/validation.py`
3. Add tool function in `mcp_server/server.py` with decorators
4. Create test script in `scripts/`
5. Update CLAUDE.md

**Key Decorators:**
```python
@mcp.tool()                    # Register as MCP tool
@validate_input(YourInput)     # Pydantic validation
@track_performance             # Performance monitoring
```

**Template:**
```python
def your_tool(param: str, optional: int = 10) -> dict:
    """Comprehensive docstring (Claude sees this).

    Args:
        param: Description
        optional: Description with default

    Returns:
        Dictionary containing: key1, key2, key3
    """
    # Implementation
    return {"result": "data"}
```

## Adding New Analyzers

**Overview:** Analyzers inherit from `BaseAnalyzer` and check USPTO compliance.

**Minimal Example:**
```python
from mcp_server.analyzer_base import BaseAnalyzer

class YourAnalyzer(BaseAnalyzer):
    def __init__(self):
        super().__init__()
        self.mpep_sections = ["608", "2173"]

    def analyze(self, content: str) -> dict:
        issues = []
        if violation:
            issues.append({
                "type": "violation_name",
                "severity": "critical",
                "mpep_citation": "MPEP 608",
                "recommendation": "Fix description"
            })
        return {"compliant": len(issues) == 0, "issues": issues}
```

## Adding Configuration Options

Use Pydantic settings in `mcp_server/config.py`:

```python
# In config.py
class AppSettings(BaseSettings):
    enable_feature_x: bool = Field(default=False, description="Enable X")

# In your code
from mcp_server.config import get_settings
if get_settings().enable_feature_x:
    # Feature enabled
```

## Adding Performance Monitoring

```python
@track_performance
def your_function(data):
    with OperationTimer("step1"):
        result1 = step1(data)
    with OperationTimer("step2"):
        result2 = step2(result1)
    return result2
```

## Modifying RAG Search Pipeline

Pipeline: `Query -> HyDE -> Vector+BM25 -> RRF -> Reranking -> Results`

**Customization Points:** Query expansion, custom scoring, filtering, reranking strategies

## Adding New Slash Commands

1. Create `.claude/commands/your-command.md`
2. Add frontmatter: `description`, `model`
3. Write workflow instructions
4. Restart Claude Code

**Template:**
```markdown
---
description: Brief command description
model: claude-sonnet-4-5-20250929
---

# Command Name

## When to Use
- Use case 1

## How It Works
Step 1: ...
```

## Development Best Practices

1. Follow existing patterns
2. Use type hints
3. Write docstrings (Google style)
4. Handle errors gracefully
5. Validate inputs (Pydantic)
6. Log operations
7. Monitor performance

## Common Development Tasks

**Add BigQuery Query:** Add method in `mcp_server/bigquery_search.py`

**Add Validation Rule:**
```python
class YourInput(BaseModel):
    field: str

    @field_validator("field")
    @classmethod
    def validate_field(cls, v):
        if not meets_requirement(v):
            raise ValueError("Error message")
        return v
```

**Add Logging:**
```python
from mcp_server.logging_config import get_logger
logger = get_logger()
logger.info("event_name", extra={"context": "data"})
```

## Quick Reference: File Locations

| Task | Primary File | Related Files |
|------|-------------|---------------|
| Add MCP tool | `mcp_server/server.py` | `mcp_server/validation.py` |
| Add analyzer | `mcp_server/your_analyzer.py` | `mcp_server/analyzer_base.py` |
| Add config | `mcp_server/config.py` | `.env`, `CLAUDE.md` |
| Add BigQuery query | `mcp_server/bigquery_search.py` | - |
| Add test | `scripts/test_your_feature.py` | - |

## Key Patterns

**MCP Tool Pattern:**
```python
@mcp.tool()
@validate_input(InputModel)
@track_performance
def tool_name(param: type) -> dict:
    """Docstring visible to Claude."""
    from module import Component
    if invalid:
        return {"error": "message"}
    result = process(param)
    return {"key": "value"}
```

**Analyzer Pattern:**
```python
class YourAnalyzer(BaseAnalyzer):
    def analyze(self, content: str) -> dict:
        issues = []
        issues.extend(self._check_x(content))
        return {
            "compliant": len(issues) == 0,
            "issues": issues,
            "recommendations": self._generate_recommendations(issues)
        }
```
