---
name: local-llm-router
description: Route AI coding queries to local LLMs in air-gapped networks. Integrates Serena MCP for semantic code understanding. Use when working offline, with local models (Ollama, LM Studio, Jan, OpenWebUI), or in secure/closed environments. Triggers on local LLM, Ollama, LM Studio, Jan, air-gapped, offline AI, Serena, local inference, closed network, model routing, defense network, secure coding.
---

# Local LLM Router for Air-Gapped Networks

Intelligent routing of AI coding queries to local LLMs with Serena LSP integration for secure, offline-capable development environments.

## Prerequisites (CRITICAL)

Before using this skill, ensure:

1. **Serena MCP Server** installed and running (PRIMARY TOOL)
2. **At least one local LLM service** running (Ollama, LM Studio, Jan, etc.)

```bash
# Install Serena (required)
pip install serena
# Or via uvx
uvx --from git+https://github.com/oraios/serena serena start-mcp-server

# Verify local LLM service
curl http://localhost:11434/api/version  # Ollama
curl http://localhost:1234/v1/models     # LM Studio
curl http://localhost:1337/v1/models     # Jan
```

## Quick Start

```python
import httpx
import asyncio
from dataclasses import dataclass
from enum import Enum
from typing import Optional

class TaskCategory(Enum):
    CODING = "coding"
    REASONING = "reasoning"
    ANALYSIS = "analysis"
    DOCUMENTATION = "documentation"

@dataclass
class RouterConfig:
    """Local LLM Router configuration."""
    ollama_url: str = "http://localhost:11434"
    lmstudio_url: str = "http://localhost:1234"
    jan_url: str = "http://localhost:1337"
    serena_enabled: bool = True
    timeout: int = 30

async def quick_route(query: str, config: RouterConfig = RouterConfig()):
    """Quick routing example - detects services and routes query."""

    # 1. Detect available services
    services = await discover_services(config)
    if not services:
        raise RuntimeError("No local LLM services available")

    # 2. Classify task
    category = classify_task(query)

    # 3. Select best model for task
    model = select_model(category, services)

    # 4. Execute query
    return await execute_query(query, model, services[0])

# Example usage
async def main():
    response = await quick_route("Write a function to parse JSON safely")
    print(response)

asyncio.run(main())
```

## Serena Integration (PRIMARY TOOL)

**CRITICAL**: Serena MCP MUST be invoked FIRST for all code-related tasks. This provides semantic understanding of the codebase before routing to an LLM.

### Why Serena First?

1. **Token Efficiency**: Serena extracts only relevant code context
2. **Accuracy**: Symbol-level operations vs grep-style searches
3. **Codebase Awareness**: Understands types, references, call hierarchies
4. **Edit Precision**: Applies changes at symbol level, not string matching

### Serena MCP Setup

```python
import subprocess
import json
from typing import Any

class SerenaMCP:
    """Serena MCP client for code intelligence."""

    def __init__(self, workspace_root: str):
        self.workspace = workspace_root
        self.process = None

    async def start(self):
        """Start Serena MCP server."""
        self.process = subprocess.Popen(
            ["serena", "start-mcp-server", "--workspace", self.workspace],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

    async def call(self, method: str, params: dict) -> Any:
        """Call Serena MCP method."""
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params
        }
        self.process.stdin.write(json.dumps(request).encode() + b"\n")
        self.process.stdin.flush()
        response = self.process.stdout.readline()
        return json.loads(response)

    async def find_symbol(self, name: str) -> dict:
        """Find symbol definition by name."""
        return await self.call("find_symbol", {"name": name})

    async def get_references(self, file: str, line: int, char: int) -> list:
        """Get all references to symbol at position."""
        return await self.call("get_references", {
            "file": file,
            "line": line,
            "character": char
        })

    async def get_hover_info(self, file: str, line: int, char: int) -> dict:
        """Get type/documentation info at position."""
        return await self.call("get_hover_info", {
            "file": file,
            "line": line,
            "character": char
        })

    async def get_diagnostics(self, file: str) -> list:
        """Get errors/warnings for file."""
        return await self.call("get_diagnostics", {"file": file})

    async def apply_edit(self, file: str, edits: list) -> bool:
        """Apply code edits to file."""
        return await self.call("apply_edit", {"file": file, "edits": edits})

# Serena tools by priority (always use higher priority first)
SERENA_TOOLS = {
    # Priority 1: Symbol-level operations (highest)
    "find_symbol": {"priority": 1, "use_for": ["navigation", "definition"]},
    "get_references": {"priority": 1, "use_for": ["refactoring", "impact analysis"]},
    "get_hover_info": {"priority": 1, "use_for": ["type info", "documentation"]},

    # Priority 2: Code navigation
    "go_to_definition": {"priority": 2, "use_for": ["navigation"]},
    "go_to_type_definition": {"priority": 2, "use_for": ["type navigation"]},
    "go_to_implementation": {"priority": 2, "use_for": ["interface impl"]},

    # Priority 3: Code understanding
    "get_document_symbols": {"priority": 3, "use_for": ["file structure"]},
    "get_workspace_symbols": {"priority": 3, "use_for": ["codebase search"]},
    "get_call_hierarchy": {"priority": 3, "use_for": ["call analysis"]},

    # Priority 4: Code modification
    "apply_edit": {"priority": 4, "use_for": ["editing"]},
    "rename_symbol": {"priority": 4, "use_for": ["refactoring"]},

    # Priority 5: Diagnostics
    "get_diagnostics": {"priority": 5, "use_for": ["errors", "warnings"]},
    "get_code_actions": {"priority": 5, "use_for": ["quick fixes"]},
}
```

### Serena-First Request Handler

```python
async def handle_code_request(
    query: str,
    file_context: Optional[dict] = None,
    serena: SerenaMCP = None,
    router: "LLMRouter" = None
):
    """
    Handle code request with Serena-first pattern.

    CRITICAL: Serena is ALWAYS invoked first for code tasks.
    """

    # Step 1: Classify the task
    category = classify_task(query)

    # Step 2: ALWAYS use Serena for code context (if available)
    serena_context = {}
    if serena and file_context:
        # Gather semantic context from Serena
        if file_context.get("file") and file_context.get("position"):
            file = file_context["file"]
            line = file_context["position"]["line"]
            char = file_context["position"]["character"]

            # Get hover info (type, docs)
            serena_context["hover"] = await serena.get_hover_info(file, line, char)

            # For refactoring/analysis, get references
            if category in [TaskCategory.ANALYSIS, TaskCategory.CODING]:
                if "refactor" in query.lower() or "rename" in query.lower():
                    serena_context["references"] = await serena.get_references(
                        file, line, char
                    )

            # Always get diagnostics for the file
            serena_context["diagnostics"] = await serena.get_diagnostics(file)

    # Step 3: Build enriched prompt with Serena context
    enriched_query = build_enriched_query(query, serena_context)

    # Step 4: Select and route to appropriate LLM
    model = router.select_model(category)
    response = await router.execute(enriched_query, model)

    # Step 5: If response contains edits, apply via Serena
    if serena and contains_code_edit(response):
        edits = parse_code_edits(response)
        await serena.apply_edit(file_context["file"], edits)

    return response

def build_enriched_query(query: str, serena_context: dict) -> str:
    """Build query enriched with Serena context."""
    parts = [query]

    if serena_context.get("hover"):
        hover = serena_context["hover"]
        parts.append(f"\n## Type Information\n```\n{hover}\n```")

    if serena_context.get("references"):
        refs = serena_context["references"]
        parts.append(f"\n## References ({len(refs)} found)\n")
        for ref in refs[:10]:  # Limit to first 10
            parts.append(f"- {ref['file']}:{ref['line']}")

    if serena_context.get("diagnostics"):
        diags = serena_context["diagnostics"]
        if diags:
            parts.append(f"\n## Current Issues ({len(diags)})\n")
            for diag in diags[:5]:
                parts.append(f"- Line {diag['line']}: {diag['message']}")

    return "\n".join(parts)
```

## Service Discovery

### Supported Services

| Service | Default Endpoint | Health Check | Models Endpoint | Chat Endpoint | API Style |
|---------|-----------------|--------------|-----------------|---------------|-----------|
| Ollama | `localhost:11434` | `/api/version` | `/api/tags` | `/api/chat` | Native |
| LM Studio | `localhost:1234` | `/v1/models` | `/v1/models` | `/v1/chat/completions` | OpenAI |
| Jan | `localhost:1337` | `/v1/models` | `/v1/models` | `/v1/chat/completions` | OpenAI |
| OpenWebUI | `localhost:3000` | `/api/health` | `/api/models` | `/api/chat` | Custom |
| LocalAI | `localhost:8080` | `/readyz` | `/v1/models` | `/v1/chat/completions` | OpenAI |
| vLLM | `localhost:8000` | `/health` | `/v1/models` | `/v1/chat/completions` | OpenAI |
| llama.cpp | `localhost:8080` | `/health` | `/v1/models` | `/v1/chat/completions` | OpenAI |
| Kobold.cpp | `localhost:5001` | `/api/v1/info` | `/api/v1/models` | `/api/v1/generate` | Custom |
| GPT4All | `localhost:4891` | `/v1/models` | `/v1/models` | `/v1/chat/completions` | OpenAI |
| text-generation-webui | `localhost:5000` | `/api/v1/model` | `/api/v1/models` | `/api/v1/chat` | Custom |

### OS Detection

```python
import sys
import os
import platform
from dataclasses import dataclass

@dataclass
class OSInfo:
    platform: str      # 'windows', 'linux', 'darwin'
    release: str
    arch: str          # 'x64', 'arm64'
    is_wsl: bool
    is_container: bool

def detect_os() -> OSInfo:
    """Detect operating system and environment."""
    plat = sys.platform

    # Normalize platform name
    if plat == 'win32':
        plat = 'windows'
    elif plat == 'darwin':
        plat = 'darwin'
    else:
        plat = 'linux'

    # WSL detection
    is_wsl = False
    if plat == 'linux':
        try:
            with open('/proc/version', 'r') as f:
                is_wsl = 'microsoft' in f.read().lower()
        except FileNotFoundError:
            pass
        is_wsl = is_wsl or os.environ.get('WSL_DISTRO_NAME') is not None

    # Container detection
    is_container = (
        os.path.exists('/.dockerenv') or
        os.environ.get('KUBERNETES_SERVICE_HOST') is not None
    )
    if not is_container and plat == 'linux':
        try:
            with open('/proc/1/cgroup', 'r') as f:
                is_container = 'docker' in f.read() or 'kubepods' in f.read()
        except FileNotFoundError:
            pass

    return OSInfo(
        platform=plat,
        release=platform.release(),
        arch=platform.machine(),
        is_wsl=is_wsl,
        is_container=is_container
    )

def adjust_endpoint_for_os(endpoint: str, os_info: OSInfo) -> str:
    """Adjust endpoint based on OS environment."""
    if os_info.is_wsl or os_info.is_container:
        # In WSL/containers, localhost services are on the host
        return endpoint.replace('localhost', 'host.docker.internal')
    return endpoint
```

### Service Discovery Implementation

```python
import httpx
import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class DiscoveredModel:
    id: str
    name: str
    size: int = 0
    family: Optional[str] = None
    context_length: int = 4096
    quantization: Optional[str] = None

@dataclass
class LLMService:
    name: str
    type: str  # 'ollama', 'lmstudio', 'jan', 'openwebui', 'custom'
    endpoint: str
    status: str = 'unknown'  # 'online', 'offline', 'unknown'
    models: list = field(default_factory=list)
    last_checked: datetime = None
    api_style: str = 'openai'  # 'openai', 'native'

    # Endpoint paths
    health_path: str = '/v1/models'
    models_path: str = '/v1/models'
    chat_path: str = '/v1/chat/completions'

# Default service configurations
SERVICE_DEFAULTS = {
    'ollama': LLMService(
        name='Ollama',
        type='ollama',
        endpoint='http://localhost:11434',
        health_path='/api/version',
        models_path='/api/tags',
        chat_path='/api/chat',
        api_style='native'
    ),
    'lmstudio': LLMService(
        name='LM Studio',
        type='lmstudio',
        endpoint='http://localhost:1234',
        health_path='/v1/models',
        models_path='/v1/models',
        chat_path='/v1/chat/completions',
        api_style='openai'
    ),
    'jan': LLMService(
        name='Jan',
        type='jan',
        endpoint='http://localhost:1337',
        health_path='/v1/models',
        models_path='/v1/models',
        chat_path='/v1/chat/completions',
        api_style='openai'
    ),
    'openwebui': LLMService(
        name='Open WebUI',
        type='openwebui',
        endpoint='http://localhost:3000',
        health_path='/api/health',
        models_path='/api/models',
        chat_path='/api/chat',
        api_style='custom'
    ),
    'localai': LLMService(
        name='LocalAI',
        type='localai',
        endpoint='http://localhost:8080',
        health_path='/readyz',
        models_path='/v1/models',
        chat_path='/v1/chat/completions',
        api_style='openai'
    ),
    'vllm': LLMService(
        name='vLLM',
        type='vllm',
        endpoint='http://localhost:8000',
        health_path='/health',
        models_path='/v1/models',
        chat_path='/v1/chat/completions',
        api_style='openai'
    ),
    'llamacpp': LLMService(
        name='llama.cpp',
        type='llamacpp',
        endpoint='http://localhost:8080',
        health_path='/health',
        models_path='/v1/models',
        chat_path='/v1/chat/completions',
        api_style='openai'
    ),
    'koboldcpp': LLMService(
        name='Kobold.cpp',
        type='koboldcpp',
        endpoint='http://localhost:5001',
        health_path='/api/v1/info',
        models_path='/api/v1/model',
        chat_path='/api/v1/generate',
        api_style='custom'
    ),
    'gpt4all': LLMService(
        name='GPT4All',
        type='gpt4all',
        endpoint='http://localhost:4891',
        health_path='/v1/models',
        models_path='/v1/models',
        chat_path='/v1/chat/completions',
        api_style='openai'
    ),
}

class ServiceDiscovery:
    """Discover and monitor local LLM services."""

    def __init__(self, custom_endpoints: list = None):
        self.services: dict[str, LLMService] = {}
        self.os_info = detect_os()
        self.custom_endpoints = custom_endpoints or []
        self._client = httpx.AsyncClient(timeout=5.0)

    async def discover_all(self) -> list[LLMService]:
        """Discover all available LLM services."""
        discovered = []

        # Check default services
        tasks = []
        for key, default in SERVICE_DEFAULTS.items():
            service = LLMService(
                name=default.name,
                type=default.type,
                endpoint=adjust_endpoint_for_os(default.endpoint, self.os_info),
                health_path=default.health_path,
                models_path=default.models_path,
                chat_path=default.chat_path,
                api_style=default.api_style
            )
            tasks.append(self._check_service(service))

        # Check custom endpoints
        for custom in self.custom_endpoints:
            service = LLMService(
                name=custom.get('name', 'Custom'),
                type='custom',
                endpoint=custom['endpoint'],
                health_path=custom.get('health_path', '/v1/models'),
                models_path=custom.get('models_path', '/v1/models'),
                chat_path=custom.get('chat_path', '/v1/chat/completions'),
                api_style=custom.get('api_style', 'openai')
            )
            tasks.append(self._check_service(service))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            if isinstance(result, LLMService) and result.status == 'online':
                discovered.append(result)
                self.services[result.type] = result

        return discovered

    async def _check_service(self, service: LLMService) -> LLMService:
        """Check if service is online and discover models."""
        try:
            # Health check
            response = await self._client.get(
                f"{service.endpoint}{service.health_path}"
            )

            if response.status_code == 200:
                service.status = 'online'
                service.last_checked = datetime.now()

                # Discover models
                service.models = await self._discover_models(service)
            else:
                service.status = 'offline'

        except (httpx.ConnectError, httpx.TimeoutException):
            service.status = 'offline'

        return service

    async def _discover_models(self, service: LLMService) -> list[DiscoveredModel]:
        """Discover available models on service."""
        try:
            response = await self._client.get(
                f"{service.endpoint}{service.models_path}"
            )
            data = response.json()

            # Parse based on service type
            if service.type == 'ollama':
                return [
                    DiscoveredModel(
                        id=m['name'],
                        name=m['name'],
                        size=m.get('size', 0),
                        family=m.get('details', {}).get('family'),
                        context_length=self._infer_context_length(m['name'])
                    )
                    for m in data.get('models', [])
                ]
            else:  # OpenAI-style
                return [
                    DiscoveredModel(
                        id=m['id'],
                        name=m['id'],
                        context_length=m.get('context_length', 4096)
                    )
                    for m in data.get('data', [])
                ]
        except Exception:
            return []

    def _infer_context_length(self, model_name: str) -> int:
        """Infer context length from model name."""
        name_lower = model_name.lower()

        # Check for explicit context markers
        if '128k' in name_lower or '131k' in name_lower:
            return 131072
        if '64k' in name_lower:
            return 65536
        if '32k' in name_lower:
            return 32768
        if '16k' in name_lower:
            return 16384

        # Model family defaults
        if 'qwen' in name_lower:
            return 131072  # Qwen models typically have 128K+
        if 'deepseek' in name_lower:
            return 128000
        if 'llama-3' in name_lower or 'llama3' in name_lower:
            return 128000
        if 'codellama' in name_lower:
            return 100000
        if 'mixtral' in name_lower:
            return 65536

        return 8192  # Safe default
```

## Task Classification

### Classification System

```python
import re
from enum import Enum
from dataclasses import dataclass

class TaskCategory(Enum):
    CODING = "coding"
    REASONING = "reasoning"
    ANALYSIS = "analysis"
    DOCUMENTATION = "documentation"

@dataclass
class ClassificationResult:
    category: TaskCategory
    confidence: float  # 0.0 - 1.0
    requires_serena: bool
    keywords_matched: list[str]

# Task patterns (regex)
TASK_PATTERNS = {
    TaskCategory.CODING: [
        r"(?:write|create|implement|code|generate)\s+(?:a\s+)?(?:function|class|method|component)",
        r"(?:fix|debug|solve)\s+(?:this|the)\s+(?:bug|error|issue)",
        r"refactor\s+(?:this|the)",
        r"add\s+(?:error\s+handling|validation|logging|tests?)",
        r"complete\s+(?:this|the)\s+code",
        r"(?:convert|translate)\s+(?:this|the)\s+code",
        r"(?:optimize|improve)\s+(?:this|the)\s+(?:function|code|performance)",
    ],
    TaskCategory.REASONING: [
        r"(?:design|architect|plan)\s+(?:a|the)\s+(?:system|architecture|solution)",
        r"how\s+should\s+(?:I|we)\s+(?:approach|structure|implement)",
        r"what\s+(?:is|would\s+be)\s+the\s+best\s+(?:way|approach|pattern)",
        r"explain\s+the\s+(?:logic|reasoning|algorithm)",
        r"compare\s+(?:and\s+contrast|between)",
        r"(?:recommend|suggest)\s+(?:an?\s+)?(?:approach|solution|pattern)",
        r"trade-?offs?\s+(?:between|of)",
    ],
    TaskCategory.ANALYSIS: [
        r"(?:review|analyze|audit)\s+(?:this|the)\s+code",
        r"find\s+(?:potential\s+)?(?:issues|vulnerabilities|bugs|problems)",
        r"(?:security|performance)\s+(?:review|analysis|audit)",
        r"what\s+(?:could|might)\s+go\s+wrong",
        r"identify\s+(?:problems|improvements|issues)",
        r"(?:check|scan)\s+for\s+(?:vulnerabilities|issues)",
    ],
    TaskCategory.DOCUMENTATION: [
        r"(?:write|create|generate)\s+(?:documentation|docs|docstring)",
        r"(?:add|write)\s+(?:comments|jsdoc|docstring|type\s+hints)",
        r"(?:document|explain)\s+(?:this|the)\s+(?:code|function|api)",
        r"(?:create|write)\s+(?:a\s+)?readme",
        r"(?:generate|write)\s+(?:api\s+)?documentation",
        r"describe\s+(?:what|how)\s+(?:this|the)",
    ],
}

# Keyword weights for scoring
KEYWORD_WEIGHTS = {
    # Coding
    "function": (TaskCategory.CODING, 0.3),
    "implement": (TaskCategory.CODING, 0.4),
    "code": (TaskCategory.CODING, 0.2),
    "debug": (TaskCategory.CODING, 0.5),
    "refactor": (TaskCategory.CODING, 0.6),
    "fix": (TaskCategory.CODING, 0.4),
    "test": (TaskCategory.CODING, 0.3),
    "bug": (TaskCategory.CODING, 0.5),

    # Reasoning
    "architecture": (TaskCategory.REASONING, 0.6),
    "design": (TaskCategory.REASONING, 0.4),
    "approach": (TaskCategory.REASONING, 0.3),
    "strategy": (TaskCategory.REASONING, 0.5),
    "tradeoff": (TaskCategory.REASONING, 0.5),
    "compare": (TaskCategory.REASONING, 0.4),
    "recommend": (TaskCategory.REASONING, 0.4),

    # Analysis
    "review": (TaskCategory.ANALYSIS, 0.5),
    "analyze": (TaskCategory.ANALYSIS, 0.6),
    "security": (TaskCategory.ANALYSIS, 0.4),
    "vulnerability": (TaskCategory.ANALYSIS, 0.7),
    "performance": (TaskCategory.ANALYSIS, 0.3),
    "audit": (TaskCategory.ANALYSIS, 0.6),

    # Documentation
    "document": (TaskCategory.DOCUMENTATION, 0.6),
    "readme": (TaskCategory.DOCUMENTATION, 0.8),
    "docstring": (TaskCategory.DOCUMENTATION, 0.8),
    "comment": (TaskCategory.DOCUMENTATION, 0.4),
    "explain": (TaskCategory.DOCUMENTATION, 0.3),
}

def classify_task(query: str) -> ClassificationResult:
    """Classify a query into a task category."""
    query_lower = query.lower()
    scores = {cat: 0.0 for cat in TaskCategory}
    matched_keywords = []

    # Pattern matching (weight: 0.5)
    for category, patterns in TASK_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, query_lower):
                scores[category] += 0.5

    # Keyword scoring (weight: 0.5)
    words = re.findall(r'\w+', query_lower)
    for word in words:
        if word in KEYWORD_WEIGHTS:
            category, weight = KEYWORD_WEIGHTS[word]
            scores[category] += weight * 0.5
            matched_keywords.append(word)

    # Find highest scoring category
    best_category = max(scores, key=scores.get)
    confidence = min(scores[best_category], 1.0)

    # Default to CODING if no clear match
    if confidence < 0.2:
        best_category = TaskCategory.CODING
        confidence = 0.5

    # Determine if Serena is required
    requires_serena = (
        best_category == TaskCategory.ANALYSIS or
        any(kw in query_lower for kw in [
            'definition', 'reference', 'symbol', 'rename',
            'where is', 'find all', 'go to', 'jump to'
        ])
    )

    return ClassificationResult(
        category=best_category,
        confidence=confidence,
        requires_serena=requires_serena,
        keywords_matched=matched_keywords
    )
```

## Model Selection

### Model Capability Matrix

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class ModelCapability:
    id: str
    family: str
    context_window: int
    vram_gb: float
    categories: list[TaskCategory]
    performance_scores: dict[TaskCategory, int]  # 0-100
    tier: int  # 1=best, 2=good, 3=basic
    quantization: Optional[str] = None

# Comprehensive model database (40+ models) - Updated January 2025
MODEL_DATABASE: dict[str, ModelCapability] = {
    # === CODING SPECIALISTS (Tier 1) ===
    "deepseek-v3": ModelCapability(
        id="deepseek-v3",
        family="deepseek",
        context_window=128000,
        vram_gb=48,  # MoE: 685B total, 37B active
        categories=[TaskCategory.CODING, TaskCategory.REASONING, TaskCategory.ANALYSIS],
        performance_scores={
            TaskCategory.CODING: 99,
            TaskCategory.REASONING: 97,
            TaskCategory.ANALYSIS: 96,
            TaskCategory.DOCUMENTATION: 92
        },
        tier=1
    ),
    "qwen2.5-coder-32b": ModelCapability(
        id="qwen2.5-coder-32b",
        family="qwen",
        context_window=131072,
        vram_gb=22,
        categories=[TaskCategory.CODING, TaskCategory.ANALYSIS],
        performance_scores={
            TaskCategory.CODING: 96,
            TaskCategory.REASONING: 82,
            TaskCategory.ANALYSIS: 92,
            TaskCategory.DOCUMENTATION: 88
        },
        tier=1
    ),
    "deepseek-coder-v2": ModelCapability(
        id="deepseek-coder-v2",
        family="deepseek",
        context_window=128000,
        vram_gb=48,  # MoE: 236B total, 21B active
        categories=[TaskCategory.CODING, TaskCategory.ANALYSIS, TaskCategory.REASONING],
        performance_scores={
            TaskCategory.CODING: 95,
            TaskCategory.REASONING: 88,
            TaskCategory.ANALYSIS: 92,
            TaskCategory.DOCUMENTATION: 80
        },
        tier=1
    ),
    "codellama-70b": ModelCapability(
        id="codellama-70b",
        family="llama",
        context_window=100000,
        vram_gb=40,
        categories=[TaskCategory.CODING],
        performance_scores={
            TaskCategory.CODING: 90,
            TaskCategory.REASONING: 70,
            TaskCategory.ANALYSIS: 85,
            TaskCategory.DOCUMENTATION: 75
        },
        tier=1
    ),
    "codellama-34b": ModelCapability(
        id="codellama-34b",
        family="llama",
        context_window=100000,
        vram_gb=20,
        categories=[TaskCategory.CODING],
        performance_scores={
            TaskCategory.CODING: 85,
            TaskCategory.REASONING: 65,
            TaskCategory.ANALYSIS: 80,
            TaskCategory.DOCUMENTATION: 70
        },
        tier=2
    ),
    "qwen2.5-coder-14b": ModelCapability(
        id="qwen2.5-coder-14b",
        family="qwen",
        context_window=131072,
        vram_gb=10,
        categories=[TaskCategory.CODING],
        performance_scores={
            TaskCategory.CODING: 82,
            TaskCategory.REASONING: 60,
            TaskCategory.ANALYSIS: 75,
            TaskCategory.DOCUMENTATION: 70
        },
        tier=2
    ),
    "starcoder2-15b": ModelCapability(
        id="starcoder2-15b",
        family="starcoder",
        context_window=16384,
        vram_gb=10,
        categories=[TaskCategory.CODING],
        performance_scores={
            TaskCategory.CODING: 80,
            TaskCategory.REASONING: 50,
            TaskCategory.ANALYSIS: 70,
            TaskCategory.DOCUMENTATION: 60
        },
        tier=2
    ),
    "deepseek-coder-6.7b": ModelCapability(
        id="deepseek-coder-6.7b",
        family="deepseek",
        context_window=16384,
        vram_gb=5,
        categories=[TaskCategory.CODING],
        performance_scores={
            TaskCategory.CODING: 75,
            TaskCategory.REASONING: 50,
            TaskCategory.ANALYSIS: 65,
            TaskCategory.DOCUMENTATION: 55
        },
        tier=3
    ),
    "codellama-7b": ModelCapability(
        id="codellama-7b",
        family="llama",
        context_window=16384,
        vram_gb=5,
        categories=[TaskCategory.CODING],
        performance_scores={
            TaskCategory.CODING: 70,
            TaskCategory.REASONING: 45,
            TaskCategory.ANALYSIS: 60,
            TaskCategory.DOCUMENTATION: 50
        },
        tier=3
    ),

    # === REASONING SPECIALISTS ===
    "deepseek-r1": ModelCapability(
        id="deepseek-r1",
        family="deepseek",
        context_window=128000,
        vram_gb=160,  # 671B total
        categories=[TaskCategory.REASONING, TaskCategory.CODING],
        performance_scores={
            TaskCategory.CODING: 92,
            TaskCategory.REASONING: 99,
            TaskCategory.ANALYSIS: 95,
            TaskCategory.DOCUMENTATION: 90
        },
        tier=1
    ),
    "deepseek-r1-distill-70b": ModelCapability(
        id="deepseek-r1-distill-70b",
        family="deepseek",
        context_window=128000,
        vram_gb=42,
        categories=[TaskCategory.REASONING, TaskCategory.CODING],
        performance_scores={
            TaskCategory.CODING: 88,
            TaskCategory.REASONING: 94,
            TaskCategory.ANALYSIS: 90,
            TaskCategory.DOCUMENTATION: 86
        },
        tier=1
    ),
    "qwen2.5-72b-instruct": ModelCapability(
        id="qwen2.5-72b-instruct",
        family="qwen",
        context_window=131072,
        vram_gb=48,
        categories=[TaskCategory.REASONING, TaskCategory.CODING],
        performance_scores={
            TaskCategory.CODING: 88,
            TaskCategory.REASONING: 95,
            TaskCategory.ANALYSIS: 92,
            TaskCategory.DOCUMENTATION: 94
        },
        tier=1
    ),
    "llama-3.3-70b-instruct": ModelCapability(
        id="llama-3.3-70b-instruct",
        family="llama",
        context_window=128000,
        vram_gb=42,
        categories=[TaskCategory.REASONING, TaskCategory.CODING],
        performance_scores={
            TaskCategory.CODING: 85,
            TaskCategory.REASONING: 92,
            TaskCategory.ANALYSIS: 88,
            TaskCategory.DOCUMENTATION: 90
        },
        tier=1
    ),
    "deepseek-r1-distill-32b": ModelCapability(
        id="deepseek-r1-distill-32b",
        family="deepseek",
        context_window=128000,
        vram_gb=22,
        categories=[TaskCategory.REASONING, TaskCategory.CODING],
        performance_scores={
            TaskCategory.CODING: 82,
            TaskCategory.REASONING: 90,
            TaskCategory.ANALYSIS: 85,
            TaskCategory.DOCUMENTATION: 82
        },
        tier=2
    ),
    "mistral-small-24b": ModelCapability(
        id="mistral-small-24b",
        family="mistral",
        context_window=32768,
        vram_gb=16,
        categories=[TaskCategory.REASONING, TaskCategory.CODING],
        performance_scores={
            TaskCategory.CODING: 80,
            TaskCategory.REASONING: 85,
            TaskCategory.ANALYSIS: 82,
            TaskCategory.DOCUMENTATION: 84
        },
        tier=2
    ),
    "qwen2.5-32b-instruct": ModelCapability(
        id="qwen2.5-32b-instruct",
        family="qwen",
        context_window=131072,
        vram_gb=22,
        categories=[TaskCategory.REASONING, TaskCategory.DOCUMENTATION],
        performance_scores={
            TaskCategory.CODING: 78,
            TaskCategory.REASONING: 86,
            TaskCategory.ANALYSIS: 82,
            TaskCategory.DOCUMENTATION: 88
        },
        tier=2
    ),
    "phi-4": ModelCapability(
        id="phi-4",
        family="phi",
        context_window=16384,
        vram_gb=10,
        categories=[TaskCategory.REASONING, TaskCategory.CODING],
        performance_scores={
            TaskCategory.CODING: 82,
            TaskCategory.REASONING: 88,
            TaskCategory.ANALYSIS: 80,
            TaskCategory.DOCUMENTATION: 78
        },
        tier=2
    ),
    "deepseek-r1-distill-14b": ModelCapability(
        id="deepseek-r1-distill-14b",
        family="deepseek",
        context_window=128000,
        vram_gb=10,
        categories=[TaskCategory.REASONING],
        performance_scores={
            TaskCategory.CODING: 75,
            TaskCategory.REASONING: 85,
            TaskCategory.ANALYSIS: 78,
            TaskCategory.DOCUMENTATION: 76
        },
        tier=2
    ),
    "llama-3.2-11b-vision": ModelCapability(
        id="llama-3.2-11b-vision",
        family="llama",
        context_window=128000,
        vram_gb=8,
        categories=[TaskCategory.REASONING, TaskCategory.DOCUMENTATION],
        performance_scores={
            TaskCategory.CODING: 68,
            TaskCategory.REASONING: 78,
            TaskCategory.ANALYSIS: 75,
            TaskCategory.DOCUMENTATION: 80
        },
        tier=2
    ),
    "gemma-2-27b": ModelCapability(
        id="gemma-2-27b",
        family="gemma",
        context_window=8192,
        vram_gb=18,
        categories=[TaskCategory.REASONING, TaskCategory.CODING],
        performance_scores={
            TaskCategory.CODING: 78,
            TaskCategory.REASONING: 82,
            TaskCategory.ANALYSIS: 78,
            TaskCategory.DOCUMENTATION: 80
        },
        tier=2
    ),
    "deepseek-r1-distill-8b": ModelCapability(
        id="deepseek-r1-distill-8b",
        family="deepseek",
        context_window=128000,
        vram_gb=6,
        categories=[TaskCategory.REASONING],
        performance_scores={
            TaskCategory.CODING: 68,
            TaskCategory.REASONING: 78,
            TaskCategory.ANALYSIS: 70,
            TaskCategory.DOCUMENTATION: 68
        },
        tier=3
    ),
    "gemma-2-9b": ModelCapability(
        id="gemma-2-9b",
        family="gemma",
        context_window=8192,
        vram_gb=7,
        categories=[TaskCategory.REASONING, TaskCategory.CODING],
        performance_scores={
            TaskCategory.CODING: 72,
            TaskCategory.REASONING: 75,
            TaskCategory.ANALYSIS: 70,
            TaskCategory.DOCUMENTATION: 74
        },
        tier=3
    ),
    "llama-3.2-3b": ModelCapability(
        id="llama-3.2-3b",
        family="llama",
        context_window=128000,
        vram_gb=3,
        categories=[TaskCategory.REASONING],
        performance_scores={
            TaskCategory.CODING: 55,
            TaskCategory.REASONING: 65,
            TaskCategory.ANALYSIS: 58,
            TaskCategory.DOCUMENTATION: 65
        },
        tier=3
    ),

    # === ANALYSIS SPECIALISTS (Serena Required) ===
    "codellama-34b-instruct": ModelCapability(
        id="codellama-34b-instruct",
        family="llama",
        context_window=100000,
        vram_gb=20,
        categories=[TaskCategory.ANALYSIS],
        performance_scores={
            TaskCategory.CODING: 80,
            TaskCategory.REASONING: 70,
            TaskCategory.ANALYSIS: 88,
            TaskCategory.DOCUMENTATION: 75
        },
        tier=2
    ),

    # === DOCUMENTATION SPECIALISTS ===
    "mistral-nemo-12b": ModelCapability(
        id="mistral-nemo-12b",
        family="mistral",
        context_window=128000,
        vram_gb=8,
        categories=[TaskCategory.DOCUMENTATION],
        performance_scores={
            TaskCategory.CODING: 65,
            TaskCategory.REASONING: 70,
            TaskCategory.ANALYSIS: 65,
            TaskCategory.DOCUMENTATION: 82
        },
        tier=2
    ),
    "mistral-7b": ModelCapability(
        id="mistral-7b",
        family="mistral",
        context_window=32768,
        vram_gb=5,
        categories=[TaskCategory.DOCUMENTATION],
        performance_scores={
            TaskCategory.CODING: 55,
            TaskCategory.REASONING: 60,
            TaskCategory.ANALYSIS: 55,
            TaskCategory.DOCUMENTATION: 72
        },
        tier=3
    ),

    # === ADDITIONAL MODELS ===
    "phi-3-medium": ModelCapability(
        id="phi-3-medium",
        family="phi",
        context_window=128000,
        vram_gb=8,
        categories=[TaskCategory.CODING, TaskCategory.REASONING],
        performance_scores={
            TaskCategory.CODING: 72,
            TaskCategory.REASONING: 75,
            TaskCategory.ANALYSIS: 68,
            TaskCategory.DOCUMENTATION: 70
        },
        tier=2
    ),
    "gemma-2-27b": ModelCapability(
        id="gemma-2-27b",
        family="gemma",
        context_window=8192,
        vram_gb=18,
        categories=[TaskCategory.CODING, TaskCategory.REASONING],
        performance_scores={
            TaskCategory.CODING: 78,
            TaskCategory.REASONING: 80,
            TaskCategory.ANALYSIS: 75,
            TaskCategory.DOCUMENTATION: 78
        },
        tier=2
    ),
    "yi-34b": ModelCapability(
        id="yi-34b",
        family="yi",
        context_window=200000,
        vram_gb=20,
        categories=[TaskCategory.REASONING, TaskCategory.DOCUMENTATION],
        performance_scores={
            TaskCategory.CODING: 72,
            TaskCategory.REASONING: 82,
            TaskCategory.ANALYSIS: 75,
            TaskCategory.DOCUMENTATION: 80
        },
        tier=2
    ),
    "command-r-plus": ModelCapability(
        id="command-r-plus",
        family="cohere",
        context_window=128000,
        vram_gb=48,
        categories=[TaskCategory.REASONING, TaskCategory.DOCUMENTATION],
        performance_scores={
            TaskCategory.CODING: 70,
            TaskCategory.REASONING: 85,
            TaskCategory.ANALYSIS: 78,
            TaskCategory.DOCUMENTATION: 88
        },
        tier=1
    ),
    "wizardcoder-33b": ModelCapability(
        id="wizardcoder-33b",
        family="wizard",
        context_window=16384,
        vram_gb=20,
        categories=[TaskCategory.CODING],
        performance_scores={
            TaskCategory.CODING: 85,
            TaskCategory.REASONING: 60,
            TaskCategory.ANALYSIS: 75,
            TaskCategory.DOCUMENTATION: 65
        },
        tier=2
    ),
    "magicoder-7b": ModelCapability(
        id="magicoder-7b",
        family="magicoder",
        context_window=16384,
        vram_gb=5,
        categories=[TaskCategory.CODING],
        performance_scores={
            TaskCategory.CODING: 78,
            TaskCategory.REASONING: 50,
            TaskCategory.ANALYSIS: 65,
            TaskCategory.DOCUMENTATION: 55
        },
        tier=3
    ),
    "dolphin-mixtral-8x7b": ModelCapability(
        id="dolphin-mixtral-8x7b",
        family="dolphin",
        context_window=32768,
        vram_gb=28,
        categories=[TaskCategory.CODING, TaskCategory.REASONING],
        performance_scores={
            TaskCategory.CODING: 75,
            TaskCategory.REASONING: 78,
            TaskCategory.ANALYSIS: 72,
            TaskCategory.DOCUMENTATION: 75
        },
        tier=2
    ),
    "nous-hermes-2-mixtral": ModelCapability(
        id="nous-hermes-2-mixtral",
        family="nous",
        context_window=32768,
        vram_gb=28,
        categories=[TaskCategory.REASONING],
        performance_scores={
            TaskCategory.CODING: 72,
            TaskCategory.REASONING: 82,
            TaskCategory.ANALYSIS: 75,
            TaskCategory.DOCUMENTATION: 78
        },
        tier=2
    ),
    "solar-10.7b": ModelCapability(
        id="solar-10.7b",
        family="solar",
        context_window=4096,
        vram_gb=7,
        categories=[TaskCategory.REASONING, TaskCategory.DOCUMENTATION],
        performance_scores={
            TaskCategory.CODING: 60,
            TaskCategory.REASONING: 72,
            TaskCategory.ANALYSIS: 65,
            TaskCategory.DOCUMENTATION: 75
        },
        tier=3
    ),
}

# Task-to-model priority mapping (Updated January 2025)
TASK_MODEL_PRIORITY = {
    TaskCategory.CODING: [
        # Tier 1 - Best
        "deepseek-v3", "qwen2.5-coder-32b", "deepseek-coder-v2",
        # Tier 2 - Good
        "codellama-70b", "qwen2.5-coder-14b", "codellama-34b",
        "starcoder2-15b", "phi-4",
        # Tier 3 - Basic
        "qwen2.5-coder-7b", "codellama-7b", "deepseek-coder-6.7b"
    ],
    TaskCategory.REASONING: [
        # Tier 1 - Best
        "deepseek-r1", "deepseek-v3", "deepseek-r1-distill-70b",
        "qwen2.5-72b-instruct", "llama-3.3-70b-instruct",
        # Tier 2 - Good
        "deepseek-r1-distill-32b", "mistral-small-24b", "qwen2.5-32b-instruct",
        "phi-4", "gemma-2-27b",
        # Tier 3 - Basic
        "deepseek-r1-distill-14b", "deepseek-r1-distill-8b", "gemma-2-9b"
    ],
    TaskCategory.ANALYSIS: [
        # Requires Serena LSP
        "deepseek-v3", "qwen2.5-coder-32b", "deepseek-coder-v2",
        "codellama-34b-instruct", "qwen2.5-72b-instruct"
    ],
    TaskCategory.DOCUMENTATION: [
        "qwen2.5-72b-instruct", "llama-3.3-70b-instruct", "qwen2.5-32b-instruct",
        "mistral-small-24b", "mistral-nemo-12b", "gemma-2-27b"
    ],
}
```

### Model Selection Logic

```python
from typing import Optional

class ModelSelector:
    """Select optimal model for task based on availability and requirements."""

    def __init__(self, available_models: list[str]):
        self.available = set(m.lower() for m in available_models)

    def select(
        self,
        category: TaskCategory,
        required_context: int = 0,
        max_vram_gb: Optional[float] = None
    ) -> Optional[str]:
        """Select best available model for task category."""

        # Get priority list for category
        priority_list = TASK_MODEL_PRIORITY.get(category, [])

        for model_id in priority_list:
            # Check if model is available
            if not self._is_available(model_id):
                continue

            # Check model capability
            capability = MODEL_DATABASE.get(model_id)
            if not capability:
                continue

            # Check context window requirement
            if required_context > 0 and capability.context_window < required_context:
                continue

            # Check VRAM constraint
            if max_vram_gb and capability.vram_gb > max_vram_gb:
                continue

            return model_id

        # Fallback: return any available model
        for model_id, capability in MODEL_DATABASE.items():
            if self._is_available(model_id):
                return model_id

        return None

    def _is_available(self, model_id: str) -> bool:
        """Check if model is available (fuzzy matching)."""
        model_lower = model_id.lower()

        # Exact match
        if model_lower in self.available:
            return True

        # Partial match (model name contained in available)
        for avail in self.available:
            if model_lower in avail or avail in model_lower:
                return True

        return False

    def get_fallback_models(self, category: TaskCategory) -> list[str]:
        """Get list of fallback models for category."""
        priority_list = TASK_MODEL_PRIORITY.get(category, [])

        available_in_priority = [
            m for m in priority_list if self._is_available(m)
        ]

        # Return tier 2 and 3 models as fallbacks
        fallbacks = []
        for model_id in available_in_priority:
            capability = MODEL_DATABASE.get(model_id)
            if capability and capability.tier >= 2:
                fallbacks.append(model_id)

        return fallbacks
```

## Context Management

### Token Counting

```python
from abc import ABC, abstractmethod
import re

class TokenCounter(ABC):
    """Base class for token counting."""

    @abstractmethod
    def count(self, text: str) -> int:
        pass

class EstimationCounter(TokenCounter):
    """Estimation-based token counter (no external dependencies)."""

    def __init__(self, chars_per_token: float = 4.0):
        self.chars_per_token = chars_per_token

    def count(self, text: str) -> int:
        return int(len(text) / self.chars_per_token)

class QwenCounter(TokenCounter):
    """Token counter for Qwen models."""

    def count(self, text: str) -> int:
        # Qwen uses slightly different tokenization
        return int(len(text) / 3.5)

class LlamaCounter(TokenCounter):
    """Token counter for Llama models."""

    def count(self, text: str) -> int:
        # Llama uses SentencePiece
        return int(len(text) / 3.8)

# Model family to counter mapping
TOKEN_COUNTERS = {
    "qwen": QwenCounter(),
    "deepseek": EstimationCounter(4.0),
    "llama": LlamaCounter(),
    "mistral": EstimationCounter(4.0),
    "mixtral": EstimationCounter(4.0),
    "default": EstimationCounter(4.0),
}

def get_token_counter(model_id: str) -> TokenCounter:
    """Get appropriate token counter for model."""
    capability = MODEL_DATABASE.get(model_id)
    if capability:
        return TOKEN_COUNTERS.get(capability.family, TOKEN_COUNTERS["default"])
    return TOKEN_COUNTERS["default"]
```

### Context Manager

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Message:
    role: str  # 'system', 'user', 'assistant', 'tool'
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    token_count: int = 0
    metadata: dict = field(default_factory=dict)

@dataclass
class ConversationContext:
    session_id: str
    messages: list[Message] = field(default_factory=list)
    total_tokens: int = 0
    system_prompt: str = ""
    system_prompt_tokens: int = 0
    active_model: str = ""
    model_history: list[str] = field(default_factory=list)
    compaction_count: int = 0

class ContextManager:
    """Manage conversation context with compaction support."""

    def __init__(
        self,
        session_id: str,
        system_prompt: str = "",
        compaction_threshold: float = 0.8,  # 80% of context window
        compaction_target: float = 0.5,      # Compact to 50%
        preserve_recent: int = 10            # Keep last N messages
    ):
        self.context = ConversationContext(
            session_id=session_id,
            system_prompt=system_prompt
        )
        self.compaction_threshold = compaction_threshold
        self.compaction_target = compaction_target
        self.preserve_recent = preserve_recent
        self._counter: Optional[TokenCounter] = None

    def set_model(self, model_id: str):
        """Set active model and update token counter."""
        if self.context.active_model:
            self.context.model_history.append(self.context.active_model)
        self.context.active_model = model_id
        self._counter = get_token_counter(model_id)

        # Recount all tokens with new counter
        self._recount_tokens()

    def add_message(self, role: str, content: str, metadata: dict = None):
        """Add message to context."""
        token_count = self._counter.count(content) if self._counter else 0

        message = Message(
            role=role,
            content=content,
            token_count=token_count,
            metadata=metadata or {}
        )

        self.context.messages.append(message)
        self.context.total_tokens += token_count

    def check_and_compact(self, max_tokens: int) -> bool:
        """Check if compaction needed and perform if so."""
        threshold = int(max_tokens * self.compaction_threshold)

        if self.context.total_tokens > threshold:
            self._compact(max_tokens)
            return True
        return False

    def _compact(self, max_tokens: int):
        """Compact context to target size."""
        target = int(max_tokens * self.compaction_target)

        # Step 1: Truncate large tool outputs
        for msg in self.context.messages:
            if msg.role == 'tool' and msg.token_count > 500:
                original = msg.token_count
                msg.content = f"[Tool output truncated - {msg.metadata.get('tool_name', 'unknown')}]"
                msg.token_count = self._counter.count(msg.content)
                msg.metadata['truncated'] = True
                msg.metadata['original_tokens'] = original

        self._recalculate_total()

        if self.context.total_tokens <= target:
            return

        # Step 2: Summarize older messages
        if len(self.context.messages) > self.preserve_recent:
            older = self.context.messages[:-self.preserve_recent]
            recent = self.context.messages[-self.preserve_recent:]

            # Create summary of older messages
            summary = self._create_summary(older)
            summary_msg = Message(
                role='system',
                content=f"[Previous conversation summary]\n{summary}",
                token_count=self._counter.count(summary),
                metadata={'compacted': True}
            )

            self.context.messages = [summary_msg] + recent
            self.context.compaction_count += 1

        self._recalculate_total()

    def _create_summary(self, messages: list[Message]) -> str:
        """Create summary of messages (simple implementation)."""
        # In production, this would use a lightweight LLM
        key_points = []

        for msg in messages:
            if msg.role == 'user':
                # Extract first sentence of user queries
                first_sentence = msg.content.split('.')[0][:100]
                key_points.append(f"- User asked: {first_sentence}")
            elif msg.role == 'assistant' and len(key_points) < 10:
                # Extract key decisions/results
                if 'created' in msg.content.lower() or 'implemented' in msg.content.lower():
                    first_sentence = msg.content.split('.')[0][:100]
                    key_points.append(f"- Assistant: {first_sentence}")

        return "\n".join(key_points[:10])

    def _recount_tokens(self):
        """Recount all tokens with current counter."""
        if not self._counter:
            return

        self.context.system_prompt_tokens = self._counter.count(self.context.system_prompt)
        for msg in self.context.messages:
            msg.token_count = self._counter.count(msg.content)
        self._recalculate_total()

    def _recalculate_total(self):
        """Recalculate total token count."""
        self.context.total_tokens = (
            self.context.system_prompt_tokens +
            sum(m.token_count for m in self.context.messages)
        )

    def export_for_api(self) -> list[dict]:
        """Export messages in API format."""
        messages = []

        if self.context.system_prompt:
            messages.append({
                "role": "system",
                "content": self.context.system_prompt
            })

        for msg in self.context.messages:
            messages.append({
                "role": msg.role,
                "content": msg.content
            })

        return messages

    def prepare_handoff(self, new_model: str) -> "ContextManager":
        """Prepare context for model switch."""
        self.set_model(new_model)
        return self
```

## Configuration

### Inline Configuration Schema

```python
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class ServiceConfig:
    """Configuration for a single LLM service."""
    enabled: bool = True
    endpoint: str = ""
    priority: int = 1
    timeout: int = 30000
    max_retries: int = 3
    api_style: str = "openai"

@dataclass
class TaskRoutingConfig:
    """Configuration for task routing."""
    primary_models: list[str] = field(default_factory=list)
    fallback_models: list[str] = field(default_factory=list)
    min_context: int = 8192
    require_serena: bool = False

@dataclass
class SecurityConfig:
    """Security configuration for air-gapped networks."""
    allow_external: bool = False
    allowed_hosts: list[str] = field(default_factory=lambda: [
        "localhost", "127.0.0.1", "host.docker.internal"
    ])
    allowed_cidrs: list[str] = field(default_factory=lambda: [
        "192.168.0.0/16", "10.0.0.0/8", "172.16.0.0/12"
    ])
    audit_enabled: bool = True
    audit_log_path: str = "./audit.log"
    log_queries: bool = True
    log_responses: bool = False  # Don't log sensitive responses
    verify_checksums: bool = True

@dataclass
class ContextConfig:
    """Context management configuration."""
    compaction_threshold: float = 0.8
    compaction_target: float = 0.5
    preserve_recent_messages: int = 10
    preserve_recent_tool_calls: int = 5
    max_tool_output_tokens: int = 500

@dataclass
class RouterConfig:
    """Complete router configuration."""
    # Services
    ollama: ServiceConfig = field(default_factory=lambda: ServiceConfig(
        endpoint="http://localhost:11434",
        priority=1
    ))
    lmstudio: ServiceConfig = field(default_factory=lambda: ServiceConfig(
        endpoint="http://localhost:1234",
        priority=2
    ))
    jan: ServiceConfig = field(default_factory=lambda: ServiceConfig(
        endpoint="http://localhost:1337",
        priority=3
    ))
    custom_endpoints: list[dict] = field(default_factory=list)

    # Task routing (Updated January 2025)
    coding: TaskRoutingConfig = field(default_factory=lambda: TaskRoutingConfig(
        primary_models=["deepseek-v3", "qwen2.5-coder-32b", "deepseek-coder-v2"],
        fallback_models=["codellama-34b", "qwen2.5-coder-14b", "phi-4"],
        min_context=8192
    ))
    reasoning: TaskRoutingConfig = field(default_factory=lambda: TaskRoutingConfig(
        primary_models=["deepseek-r1", "deepseek-v3", "qwen2.5-72b-instruct"],
        fallback_models=["deepseek-r1-distill-32b", "mistral-small-24b"],
        min_context=16384
    ))
    analysis: TaskRoutingConfig = field(default_factory=lambda: TaskRoutingConfig(
        primary_models=["deepseek-v3", "qwen2.5-coder-32b"],
        fallback_models=["codellama-34b-instruct", "qwen2.5-72b-instruct"],
        min_context=16384,
        require_serena=True
    ))
    documentation: TaskRoutingConfig = field(default_factory=lambda: TaskRoutingConfig(
        primary_models=["qwen2.5-72b-instruct", "llama-3.3-70b-instruct"],
        fallback_models=["qwen2.5-32b-instruct", "mistral-nemo-12b"],
        min_context=8192
    ))

    # Serena
    serena_enabled: bool = True
    serena_priority: str = "always_first"

    # Context
    context: ContextConfig = field(default_factory=ContextConfig)

    # Security
    security: SecurityConfig = field(default_factory=SecurityConfig)

# Default configuration instance
DEFAULT_CONFIG = RouterConfig()

def load_config_from_dict(data: dict) -> RouterConfig:
    """Load configuration from dictionary (e.g., parsed YAML)."""
    config = RouterConfig()

    # Update services
    if 'services' in data:
        for service_name, service_data in data['services'].items():
            if hasattr(config, service_name):
                setattr(config, service_name, ServiceConfig(**service_data))

    # Update task routing
    for category in ['coding', 'reasoning', 'analysis', 'documentation']:
        if category in data.get('task_routing', {}):
            setattr(config, category, TaskRoutingConfig(**data['task_routing'][category]))

    # Update security
    if 'security' in data:
        config.security = SecurityConfig(**data['security'])

    return config
```

### Example YAML Configuration (for reference)

```yaml
# local-llm-router.yaml
# Copy this to your project and customize

version: "1.0"
environment: "air-gapped"

services:
  ollama:
    enabled: true
    endpoint: "http://localhost:11434"
    priority: 1
    timeout: 30000

  lmstudio:
    enabled: true
    endpoint: "http://localhost:1234"
    priority: 2

  jan:
    enabled: false
    endpoint: "http://localhost:1337"
    priority: 3

  custom_endpoints:
    - name: "internal-gpu-server"
      endpoint: "http://192.168.1.100:8000"
      priority: 0
      api_style: "openai"

task_routing:
  coding:
    primary_models:
      - "deepseek-v3"
      - "qwen2.5-coder-32b"
      - "deepseek-coder-v2"
    fallback_models:
      - "codellama-34b"
      - "qwen2.5-coder-14b"
      - "phi-4"
    min_context: 8192

  reasoning:
    primary_models:
      - "deepseek-r1"
      - "deepseek-v3"
      - "qwen2.5-72b-instruct"
    fallback_models:
      - "deepseek-r1-distill-32b"
      - "mistral-small-24b"
    min_context: 16384

  analysis:
    primary_models:
      - "deepseek-v3"
      - "qwen2.5-coder-32b"
    require_serena: true

  documentation:
    primary_models:
      - "qwen2.5-72b-instruct"
      - "llama-3.3-70b-instruct"
    fallback_models:
      - "mistral-nemo-12b"

serena:
  enabled: true
  priority: "always_first"
  workspace: "${WORKSPACE_ROOT}"

context:
  compaction_threshold: 0.8
  preserve_recent_messages: 10

security:
  allow_external: false
  allowed_hosts:
    - "localhost"
    - "127.0.0.1"
    - "192.168.0.0/16"
  audit_enabled: true
  audit_log_path: "./llm-router-audit.log"
```

## Fallback Strategy

### Graceful Degradation

```python
from enum import IntEnum
from dataclasses import dataclass
from typing import Optional, Any

class FallbackLevel(IntEnum):
    PRIMARY = 0
    FALLBACK_MODELS = 1
    REDUCED_CONTEXT = 2
    SMALLEST_MODEL = 3
    FAILED = 4

@dataclass
class ExecutionResult:
    success: bool
    model: Optional[str] = None
    service: Optional[str] = None
    response: Any = None
    fallback_level: FallbackLevel = FallbackLevel.PRIMARY
    error: Optional[str] = None

class FallbackExecutor:
    """Execute queries with multi-level fallback."""

    def __init__(
        self,
        discovery: ServiceDiscovery,
        context_manager: ContextManager,
        config: RouterConfig
    ):
        self.discovery = discovery
        self.context = context_manager
        self.config = config

    async def execute_with_fallback(
        self,
        query: str,
        category: TaskCategory
    ) -> ExecutionResult:
        """Execute query with fallback strategy."""

        # Get model lists
        task_config = getattr(self.config, category.value)
        primary_models = task_config.primary_models
        fallback_models = task_config.fallback_models

        # Level 0: Try primary models
        for model in primary_models:
            result = await self._try_model(model, query)
            if result.success:
                result.fallback_level = FallbackLevel.PRIMARY
                return result

        # Level 1: Try fallback models
        for model in fallback_models:
            result = await self._try_model(model, query)
            if result.success:
                result.fallback_level = FallbackLevel.FALLBACK_MODELS
                return result

        # Level 2: Reduce context and retry
        self.context._compact(task_config.min_context)
        for model in primary_models + fallback_models:
            result = await self._try_model(model, query)
            if result.success:
                result.fallback_level = FallbackLevel.REDUCED_CONTEXT
                return result

        # Level 3: Use smallest available model
        smallest = await self._find_smallest_model()
        if smallest:
            result = await self._try_model(smallest, query)
            if result.success:
                result.fallback_level = FallbackLevel.SMALLEST_MODEL
                return result

        # Level 4: All failed
        return ExecutionResult(
            success=False,
            fallback_level=FallbackLevel.FAILED,
            error="All fallback strategies exhausted"
        )

    async def _try_model(self, model_id: str, query: str) -> ExecutionResult:
        """Try executing query on specific model."""
        # Find service with this model
        service = await self._find_service_with_model(model_id)
        if not service:
            return ExecutionResult(
                success=False,
                error=f"Model {model_id} not available"
            )

        try:
            response = await self._execute_on_service(service, model_id, query)
            return ExecutionResult(
                success=True,
                model=model_id,
                service=service.name,
                response=response
            )
        except Exception as e:
            return ExecutionResult(
                success=False,
                error=str(e)
            )

    async def _find_service_with_model(self, model_id: str) -> Optional[LLMService]:
        """Find service that has the specified model."""
        services = list(self.discovery.services.values())

        # Sort by priority
        services.sort(key=lambda s: getattr(self.config, s.type, ServiceConfig()).priority)

        for service in services:
            for model in service.models:
                if model_id.lower() in model.id.lower() or model.id.lower() in model_id.lower():
                    return service

        return None

    async def _find_smallest_model(self) -> Optional[str]:
        """Find smallest available model by VRAM requirement."""
        smallest = None
        smallest_vram = float('inf')

        for service in self.discovery.services.values():
            for model in service.models:
                capability = MODEL_DATABASE.get(model.id)
                if capability and capability.vram_gb < smallest_vram:
                    smallest = model.id
                    smallest_vram = capability.vram_gb

        return smallest

    async def _execute_on_service(
        self,
        service: LLMService,
        model_id: str,
        query: str
    ) -> str:
        """Execute query on specific service."""
        import httpx

        messages = self.context.export_for_api()
        messages.append({"role": "user", "content": query})

        async with httpx.AsyncClient() as client:
            if service.api_style == 'native' and service.type == 'ollama':
                # Ollama native API
                response = await client.post(
                    f"{service.endpoint}{service.chat_path}",
                    json={
                        "model": model_id,
                        "messages": messages,
                        "stream": False
                    },
                    timeout=self.config.ollama.timeout / 1000
                )
                data = response.json()
                return data.get('message', {}).get('content', '')

            else:
                # OpenAI-compatible API
                response = await client.post(
                    f"{service.endpoint}{service.chat_path}",
                    json={
                        "model": model_id,
                        "messages": messages,
                        "stream": False
                    },
                    timeout=30
                )
                data = response.json()
                return data.get('choices', [{}])[0].get('message', {}).get('content', '')
```

## Security (Air-Gapped)

### Network Isolation

```python
import hashlib
import json
from datetime import datetime
from dataclasses import dataclass
from typing import Optional
import ipaddress
import logging

@dataclass
class AuditLogEntry:
    timestamp: str
    event_type: str
    session_id: Optional[str] = None
    model: Optional[str] = None
    service: Optional[str] = None
    query_hash: Optional[str] = None  # Hashed, not plaintext
    tokens_in: int = 0
    tokens_out: int = 0
    success: bool = True
    error: Optional[str] = None

class SecurityModule:
    """Security enforcement for air-gapped networks."""

    def __init__(self, config: SecurityConfig):
        self.config = config
        self._allowed_ips = self._parse_allowed_networks()
        self._logger = self._setup_audit_logger()

    def _parse_allowed_networks(self) -> list:
        """Parse allowed hosts and CIDRs."""
        networks = []

        for host in self.config.allowed_hosts:
            if '/' in host:
                # CIDR notation
                networks.append(ipaddress.ip_network(host, strict=False))
            else:
                # Single host
                try:
                    ip = ipaddress.ip_address(host)
                    networks.append(ipaddress.ip_network(f"{ip}/32"))
                except ValueError:
                    # Hostname like 'localhost'
                    if host == 'localhost':
                        networks.append(ipaddress.ip_network("127.0.0.0/8"))
                    elif host == 'host.docker.internal':
                        # Allow common Docker host IPs
                        networks.append(ipaddress.ip_network("172.17.0.0/16"))

        for cidr in self.config.allowed_cidrs:
            networks.append(ipaddress.ip_network(cidr, strict=False))

        return networks

    def _setup_audit_logger(self) -> logging.Logger:
        """Setup audit logger."""
        logger = logging.getLogger('llm-router-audit')
        logger.setLevel(logging.INFO)

        if self.config.audit_enabled:
            handler = logging.FileHandler(self.config.audit_log_path)
            handler.setFormatter(logging.Formatter('%(message)s'))
            logger.addHandler(handler)

        return logger

    def validate_endpoint(self, url: str) -> bool:
        """Validate that endpoint is in allowed network."""
        if self.config.allow_external:
            return True

        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            host = parsed.hostname

            # Check for localhost
            if host in ['localhost', '127.0.0.1', '::1']:
                return True

            # Check against allowed networks
            try:
                ip = ipaddress.ip_address(host)
                for network in self._allowed_ips:
                    if ip in network:
                        return True
            except ValueError:
                # Hostname - only allow specific ones
                return host in ['localhost', 'host.docker.internal']

            return False

        except Exception:
            return False

    def log_query(
        self,
        session_id: str,
        model: str,
        service: str,
        query: str,
        tokens_in: int,
        tokens_out: int,
        success: bool,
        error: Optional[str] = None
    ):
        """Log query for audit trail."""
        if not self.config.audit_enabled:
            return

        entry = AuditLogEntry(
            timestamp=datetime.now().isoformat(),
            event_type='query',
            session_id=session_id,
            model=model,
            service=service,
            query_hash=self._hash_content(query) if self.config.log_queries else None,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            success=success,
            error=error
        )

        self._logger.info(json.dumps(entry.__dict__))

    def log_security_event(self, event_type: str, details: dict):
        """Log security-related event."""
        if not self.config.audit_enabled:
            return

        entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': f'security:{event_type}',
            **details
        }

        self._logger.warning(json.dumps(entry))

    def _hash_content(self, content: str) -> str:
        """Hash content for audit logging (privacy)."""
        return hashlib.sha256(content.encode()).hexdigest()[:16]

# Security checklist for air-gapped deployment
AIR_GAPPED_CHECKLIST = """
## Air-Gapped Deployment Checklist

### Network
- [ ] Verify no external DNS resolution
- [ ] Block all egress traffic at firewall
- [ ] Whitelist only internal IP ranges
- [ ] Disable IPv6 if not needed

### Model Verification
- [ ] Pre-download all required models
- [ ] Generate SHA256 checksums for all models
- [ ] Store checksums in tamper-evident location
- [ ] Verify checksums before loading models

### Access Control
- [ ] Implement role-based access to LLM services
- [ ] Require authentication for all endpoints
- [ ] Use short-lived tokens for API access
- [ ] Log all access attempts

### Audit
- [ ] Enable comprehensive audit logging
- [ ] Log queries (hashed, not plaintext)
- [ ] Log model usage patterns
- [ ] Log all security events
- [ ] Implement log rotation and retention
"""
```

## Coding Agent Detection

### Detect Active Coding Agent

```python
import os
import sys
from dataclasses import dataclass
from typing import Optional

@dataclass
class CodingAgentInfo:
    name: str
    type: str
    version: Optional[str] = None
    config_path: Optional[str] = None

# Environment variable markers for different agents
AGENT_ENV_MARKERS = {
    # CLI-based agents
    'QWEN_CLI_VERSION': ('qwen-cli', 'cli'),
    'OPENCODE_SESSION': ('opencode', 'cli'),
    'AIDER_SESSION': ('aider', 'cli'),
    'CODEX_SESSION': ('codex', 'cli'),
    'GEMINI_CLI_SESSION': ('gemini-cli', 'cli'),

    # IDE extensions
    'CONTINUE_SESSION': ('continue', 'ide'),
    'CLINE_SESSION': ('cline', 'ide'),
    'ROO_CODE_SESSION': ('roo-code', 'ide'),
    'CURSOR_SESSION': ('cursor', 'ide'),

    # Local GUI apps
    'OPENWEBUI_SESSION': ('openwebui', 'gui'),
    'JAN_SESSION': ('jan', 'gui'),
    'AGNO_SESSION': ('agno', 'gui'),

    # Generic markers
    'LLM_AGENT': ('generic', 'unknown'),
}

def detect_coding_agent() -> CodingAgentInfo:
    """Detect which coding agent is invoking the router."""

    # Check environment variables
    for env_var, (name, agent_type) in AGENT_ENV_MARKERS.items():
        value = os.environ.get(env_var)
        if value:
            return CodingAgentInfo(
                name=name,
                type=agent_type,
                version=value if value != '1' else None
            )

    # Check process name / parent process
    try:
        import psutil
        parent = psutil.Process(os.getppid())
        parent_name = parent.name().lower()

        agent_process_names = {
            'qwen': 'qwen-cli',
            'aider': 'aider',
            'codex': 'codex',
            'continue': 'continue',
            'cursor': 'cursor',
        }

        for proc_name, agent_name in agent_process_names.items():
            if proc_name in parent_name:
                return CodingAgentInfo(name=agent_name, type='detected')

    except ImportError:
        pass  # psutil not available

    # Check for MCP client markers
    if os.environ.get('MCP_CLIENT'):
        return CodingAgentInfo(
            name=os.environ.get('MCP_CLIENT', 'mcp-client'),
            type='mcp'
        )

    # Default: unknown
    return CodingAgentInfo(name='unknown', type='unknown')

def get_agent_specific_config(agent: CodingAgentInfo) -> dict:
    """Get agent-specific configuration overrides."""

    configs = {
        'qwen-cli': {
            'default_model_preference': 'qwen',
            'context_format': 'qwen',
        },
        'aider': {
            'default_model_preference': 'gpt',
            'context_format': 'openai',
        },
        'cursor': {
            'default_model_preference': 'claude',
            'context_format': 'anthropic',
        },
        'continue': {
            'supports_streaming': True,
            'context_format': 'openai',
        },
    }

    return configs.get(agent.name, {})
```

## Complete Router Implementation

```python
class LocalLLMRouter:
    """
    Complete Local LLM Router with Serena integration.

    Usage:
        router = LocalLLMRouter(workspace="/path/to/project")
        await router.initialize()

        response = await router.route("Implement a binary search function")
        print(response)
    """

    def __init__(
        self,
        workspace: str,
        config: RouterConfig = None,
        session_id: str = None
    ):
        self.workspace = workspace
        self.config = config or DEFAULT_CONFIG
        self.session_id = session_id or self._generate_session_id()

        # Components
        self.serena: Optional[SerenaMCP] = None
        self.discovery: Optional[ServiceDiscovery] = None
        self.context: Optional[ContextManager] = None
        self.security: Optional[SecurityModule] = None
        self.selector: Optional[ModelSelector] = None
        self.fallback: Optional[FallbackExecutor] = None

        # State
        self.os_info = detect_os()
        self.coding_agent = detect_coding_agent()
        self._initialized = False

    async def initialize(self):
        """Initialize all router components."""

        # Security module
        self.security = SecurityModule(self.config.security)

        # Service discovery
        self.discovery = ServiceDiscovery(self.config.custom_endpoints)
        services = await self.discovery.discover_all()

        if not services:
            raise RuntimeError("No local LLM services available")

        # Model selector
        all_models = []
        for service in services:
            all_models.extend(m.id for m in service.models)
        self.selector = ModelSelector(all_models)

        # Context manager
        self.context = ContextManager(
            session_id=self.session_id,
            system_prompt=self._build_system_prompt(),
            compaction_threshold=self.config.context.compaction_threshold,
            compaction_target=self.config.context.compaction_target,
            preserve_recent=self.config.context.preserve_recent_messages
        )

        # Serena MCP (if enabled)
        if self.config.serena_enabled:
            self.serena = SerenaMCP(self.workspace)
            try:
                await self.serena.start()
            except Exception as e:
                logging.warning(f"Serena MCP failed to start: {e}")
                self.serena = None

        # Fallback executor
        self.fallback = FallbackExecutor(
            self.discovery,
            self.context,
            self.config
        )

        self._initialized = True

    async def route(
        self,
        query: str,
        file_context: dict = None
    ) -> str:
        """
        Route query to appropriate LLM.

        Args:
            query: The user's query
            file_context: Optional dict with 'file', 'position' for code context

        Returns:
            LLM response string
        """
        if not self._initialized:
            await self.initialize()

        # Step 1: Classify task
        classification = classify_task(query)

        # Step 2: Serena first (if code-related)
        serena_context = {}
        if self.serena and (classification.requires_serena or file_context):
            serena_context = await self._gather_serena_context(
                query, file_context, classification
            )

        # Step 3: Build enriched query
        enriched_query = self._build_enriched_query(query, serena_context)

        # Step 4: Select model
        model = self.selector.select(
            classification.category,
            required_context=self.context.context.total_tokens + len(query) // 4
        )

        if not model:
            raise RuntimeError("No suitable model available")

        # Step 5: Update context manager with selected model
        self.context.set_model(model)

        # Step 6: Check context and compact if needed
        model_capability = MODEL_DATABASE.get(model)
        if model_capability:
            self.context.check_and_compact(model_capability.context_window)

        # Step 7: Execute with fallback
        result = await self.fallback.execute_with_fallback(
            enriched_query,
            classification.category
        )

        # Step 8: Log for audit
        self.security.log_query(
            session_id=self.session_id,
            model=result.model or model,
            service=result.service or 'unknown',
            query=query,
            tokens_in=len(query) // 4,
            tokens_out=len(result.response or '') // 4,
            success=result.success,
            error=result.error
        )

        if not result.success:
            raise RuntimeError(f"Query failed: {result.error}")

        # Step 9: Update context with response
        self.context.add_message('user', query)
        self.context.add_message('assistant', result.response)

        # Step 10: Apply edits via Serena if needed
        if self.serena and file_context and contains_code_edit(result.response):
            await self._apply_serena_edits(result.response, file_context)

        return result.response

    async def _gather_serena_context(
        self,
        query: str,
        file_context: dict,
        classification: ClassificationResult
    ) -> dict:
        """Gather code context from Serena."""
        context = {}

        if not file_context:
            return context

        file = file_context.get('file')
        position = file_context.get('position', {})
        line = position.get('line', 0)
        char = position.get('character', 0)

        try:
            # Always get hover info
            context['hover'] = await self.serena.get_hover_info(file, line, char)

            # Get references for refactoring tasks
            if 'refactor' in query.lower() or 'rename' in query.lower():
                context['references'] = await self.serena.get_references(file, line, char)

            # Get diagnostics for analysis
            if classification.category == TaskCategory.ANALYSIS:
                context['diagnostics'] = await self.serena.get_diagnostics(file)

        except Exception as e:
            logging.warning(f"Serena context gathering failed: {e}")

        return context

    def _build_enriched_query(self, query: str, serena_context: dict) -> str:
        """Build query enriched with Serena context."""
        return build_enriched_query(query, serena_context)

    async def _apply_serena_edits(self, response: str, file_context: dict):
        """Apply code edits from response via Serena."""
        edits = parse_code_edits(response)
        if edits:
            await self.serena.apply_edit(file_context['file'], edits)

    def _build_system_prompt(self) -> str:
        """Build system prompt with router context."""
        return f"""You are a coding assistant running in a local, air-gapped environment.

Environment:
- OS: {self.os_info.platform} ({self.os_info.arch})
- Coding Agent: {self.coding_agent.name}
- Serena LSP: {'enabled' if self.config.serena_enabled else 'disabled'}

Guidelines:
- Provide concise, accurate code
- Use Serena's semantic information when provided
- Respect security constraints (no external calls)
- Focus on the specific task at hand
"""

    def _generate_session_id(self) -> str:
        """Generate unique session ID."""
        import uuid
        return str(uuid.uuid4())[:8]

# Utility functions
def contains_code_edit(response: str) -> bool:
    """Check if response contains code edits."""
    markers = ['```', 'def ', 'class ', 'function ', 'const ', 'let ', 'var ']
    return any(marker in response for marker in markers)

def parse_code_edits(response: str) -> list:
    """Parse code edits from response."""
    # Simple implementation - extract code blocks
    import re
    code_blocks = re.findall(r'```(?:\w+)?\n(.*?)```', response, re.DOTALL)
    return [{'content': block.strip()} for block in code_blocks]
```

## Resources

- **Serena MCP**: https://github.com/oraios/serena
- **Serena Documentation**: https://github.com/oraios/serena#user-guide
- **Ollama API**: https://github.com/ollama/ollama/blob/main/docs/api.md
- **LM Studio**: https://lmstudio.ai/docs/developer
- **Jan AI**: https://jan.ai/docs/desktop/api-server
- **OpenWebUI**: https://docs.openwebui.com/
- **LocalAI**: https://localai.io/basics/getting_started/
