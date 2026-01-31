---
name: router-builder
description: Build intent routers for agent task distribution
---


# Router Builder Skill

> Build the Semantic Router for intelligent resource selection.

## Overview

The router provides fast, embedding-based routing to:
- Slash commands
- Sub-agents  
- Skills
- Workflows

Uses the same embedding model as RAG for consistency.

## Prerequisites

```bash
pip install semantic-router sentence-transformers pyyaml
```

## Build Steps

### Step 1: Create Router Core

**File: `routing/router.py`**

```python
#!/usr/bin/env python3
"""
Hierarchical Semantic Router

Two-tier routing:
- Tier 1: Category (command | agent | skill | workflow)
- Tier 2: Specific resource within category
"""

import os
import yaml
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum

from semantic_router import Route
from semantic_router.layer import RouteLayer
from semantic_router.encoders import HuggingFaceEncoder

# Configuration
ROUTES_PATH = Path(os.getenv("ROUTES_PATH", "./routing/routes"))
CONFIDENCE_THRESHOLD = float(os.getenv("ROUTING_CONFIDENCE", "0.5"))


class Category(Enum):
    COMMAND = "command"
    AGENT = "agent"
    SKILL = "skill"
    WORKFLOW = "workflow"
    GENERAL = "general"


@dataclass
class RoutingResult:
    """Result of a routing decision."""
    category: Category
    resource: Optional[str]
    confidence: float
    metadata: Dict
    fallback: bool = False


class Router:
    """Hierarchical semantic router."""
    
    def __init__(self):
        # Use same model as RAG
        self.encoder = HuggingFaceEncoder(name="all-MiniLM-L6-v2")
        self.category_layer = self._build_category_layer()
        self.domain_layers: Dict[Category, RouteLayer] = {}
        self._build_domain_layers()
    
    def _load_routes(self, path: Path) -> List[Route]:
        """Load routes from YAML."""
        if not path.exists():
            return []
        
        with open(path) as f:
            data = yaml.safe_load(f) or {}
        
        return [
            Route(
                name=r["name"],
                utterances=r["utterances"],
                metadata=r.get("metadata", {})
            )
            for r in data.get("routes", [])
        ]
    
    def _build_category_layer(self) -> RouteLayer:
        """Build tier-1 category router."""
        routes = self._load_routes(ROUTES_PATH / "categories.yaml")
        
        if not routes:
            # Default routes
            routes = [
                Route(name="command", utterances=[
                    "/research", "/code-review", "/daily-standup",
                    "run the command", "execute command", "use slash command"
                ]),
                Route(name="agent", utterances=[
                    "ask the researcher", "have the coder", "use the analyst",
                    "delegate to agent", "agent should handle"
                ]),
                Route(name="skill", utterances=[
                    "use the skill", "apply skill", "leverage skill for"
                ]),
                Route(name="workflow", utterances=[
                    "run workflow", "start pipeline", "execute automation"
                ]),
            ]
        
        return RouteLayer(encoder=self.encoder, routes=routes)
    
    def _build_domain_layers(self):
        """Build tier-2 domain routers."""
        mappings = {
            Category.COMMAND: "commands.yaml",
            Category.AGENT: "agents.yaml",
            Category.SKILL: "skills.yaml",
            Category.WORKFLOW: "workflows.yaml",
        }
        
        for category, filename in mappings.items():
            routes = self._load_routes(ROUTES_PATH / filename)
            if routes:
                self.domain_layers[category] = RouteLayer(
                    encoder=self.encoder,
                    routes=routes
                )
    
    def route(self, query: str) -> RoutingResult:
        """Route a query through both tiers."""
        
        # Tier 1: Category
        cat_result = self.category_layer(query)
        
        if cat_result.name is None:
            return RoutingResult(
                category=Category.GENERAL,
                resource=None,
                confidence=0.0,
                metadata={"reason": "no_category_match"},
                fallback=True
            )
        
        category = Category(cat_result.name)
        
        # Tier 2: Specific resource
        if category in self.domain_layers:
            domain_result = self.domain_layers[category](query)
            
            if domain_result.name is not None:
                return RoutingResult(
                    category=category,
                    resource=domain_result.name,
                    confidence=0.8,  # TODO: extract actual score
                    metadata=getattr(domain_result, 'metadata', {}) or {}
                )
        
        # Category matched but no specific resource
        return RoutingResult(
            category=category,
            resource=None,
            confidence=0.5,
            metadata={"reason": "no_resource_match"},
            fallback=True
        )
    
    def add_route(self, category: Category, name: str, utterances: List[str], metadata: Dict = None):
        """Dynamically add a route."""
        route = Route(name=name, utterances=utterances, metadata=metadata or {})
        
        if category not in self.domain_layers:
            self.domain_layers[category] = RouteLayer(
                encoder=self.encoder,
                routes=[route]
            )
        else:
            # Rebuild with new route
            existing = list(self.domain_layers[category].routes)
            existing.append(route)
            self.domain_layers[category] = RouteLayer(
                encoder=self.encoder,
                routes=existing
            )


# Singleton
_router: Optional[Router] = None

def get_router() -> Router:
    global _router
    if _router is None:
        _router = Router()
    return _router

def route(query: str) -> RoutingResult:
    return get_router().route(query)
```

### Step 2: Create Route Definitions

**File: `routing/routes/categories.yaml`**

```yaml
routes:
  - name: command
    utterances:
      - "/research"
      - "/code-review"
      - "/daily-standup"
      - "/summarize"
      - "run the research command"
      - "execute code review"
      - "use slash command"
      - "run command for"
      
  - name: agent
    utterances:
      - "ask the researcher"
      - "have the coder implement"
      - "let the writer draft"
      - "use the analyst"
      - "delegate to agent"
      - "which agent should"
      - "agent help with"
      
  - name: skill
    utterances:
      - "use web research skill"
      - "apply document generation"
      - "use the skill for"
      - "leverage skill"
      
  - name: workflow
    utterances:
      - "run the workflow"
      - "start the pipeline"
      - "execute automation"
      - "trigger workflow"
```

**File: `routing/routes/commands.yaml`**

```yaml
routes:
  - name: research
    utterances:
      - "research this"
      - "find information about"
      - "look up"
      - "investigate"
      - "deep dive into"
      - "gather info on"
    metadata:
      file: ".claude/commands/research.md"
      
  - name: code-review
    utterances:
      - "review code"
      - "check for bugs"
      - "analyze code"
      - "security review"
      - "code quality"
    metadata:
      file: ".claude/commands/code-review.md"
      
  - name: daily-standup
    utterances:
      - "daily standup"
      - "standup report"
      - "what did I work on"
      - "yesterday today blockers"
    metadata:
      file: ".claude/commands/daily-standup.md"
```

**File: `routing/routes/agents.yaml`**

```yaml
routes:
  - name: researcher
    utterances:
      - "research topic"
      - "find information"
      - "look up facts"
      - "gather data"
      - "fact check"
    metadata:
      path: "agents/sub-agents/researcher"
      
  - name: coder
    utterances:
      - "write code"
      - "implement function"
      - "debug"
      - "fix bug"
      - "refactor"
    metadata:
      path: "agents/sub-agents/coder"
      
  - name: writer
    utterances:
      - "write document"
      - "draft email"
      - "compose"
      - "edit text"
    metadata:
      path: "agents/sub-agents/writer"
      
  - name: analyst
    utterances:
      - "analyze data"
      - "create chart"
      - "visualize"
      - "statistics"
    metadata:
      path: "agents/sub-agents/analyst"
```

### Step 3: Create MCP Server

**File: `mcp/servers/router-server/server.py`**

```python
#!/usr/bin/env python3
"""Router MCP Server."""

import asyncio
import json
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from mcp.server import Server
from mcp.server.stdio import stdio_server
from routing.router import Router, Category


class RouterServer:
    def __init__(self):
        self.server = Server("router-server")
        self.router = Router()
        self._setup_tools()
    
    def _setup_tools(self):
        
        @self.server.tool()
        async def route_query(query: str) -> str:
            """Route a query to the appropriate resource."""
            result = self.router.route(query)
            return json.dumps({
                "category": result.category.value,
                "resource": result.resource,
                "confidence": result.confidence,
                "metadata": result.metadata,
                "fallback": result.fallback
            })
        
        @self.server.tool()
        async def list_routes(category: str = None) -> str:
            """List available routes."""
            routes = {}
            
            # Category layer
            routes["categories"] = [r.name for r in self.router.category_layer.routes]
            
            # Domain layers
            for cat, layer in self.router.domain_layers.items():
                if category is None or cat.value == category:
                    routes[cat.value] = [
                        {"name": r.name, "samples": r.utterances[:3]}
                        for r in layer.routes
                    ]
            
            return json.dumps(routes)
    
    async def run(self):
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(read_stream, write_stream)


def main():
    server = RouterServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
```

### Step 4: Create Test Script

**File: `routing/test_router.py`**

```python
#!/usr/bin/env python3
"""Test the semantic router."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from routing.router import route, Category

def test_routing():
    """Test various queries."""
    
    test_cases = [
        # (query, expected_category, expected_resource)
        ("research quantum computing", Category.COMMAND, "research"),
        ("/code-review", Category.COMMAND, "code-review"),
        ("ask the researcher to find", Category.AGENT, "researcher"),
        ("write code for sorting", Category.AGENT, "coder"),
        ("run the workflow", Category.WORKFLOW, None),
    ]
    
    print("Testing router...
")
    
    for query, expected_cat, expected_res in test_cases:
        result = route(query)
        status = "✅" if result.category == expected_cat else "❌"
        print(f"{status} '{query}'")
        print(f"   → {result.category.value}/{result.resource}")
        print(f"   confidence: {result.confidence}")
        print()
    
    print("Router test complete!")

if __name__ == "__main__":
    test_routing()
```

## Verification

```bash
# Install dependencies
pip install semantic-router sentence-transformers pyyaml

# Run tests
cd routing
python test_router.py
```

## Adding New Routes

1. Edit the appropriate YAML file in `routing/routes/`
2. Add 5-10 example utterances per route
3. Include metadata for resource location

```yaml
# Example: Adding a new command
routes:
  - name: my-new-command
    utterances:
      - "run my new command"
      - "execute my-new-command"
      - "new command please"
      # ... more variations
    metadata:
      file: ".claude/commands/my-new-command.md"
```

## After Building

1. ✅ Run tests to verify
2. Update `CLAUDE.md` status
3. Proceed to slash commands or `skills/agent-builder/SKILL.md`

## Refinement Notes

> Add notes here as we discover what works.

- [ ] Initial implementation
- [ ] Tuned confidence thresholds
- [ ] Added more utterance examples
- [ ] Tested with real queries
