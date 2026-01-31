---
name: prompt-template
description: Create and manage reusable prompt templates
---


# Prompt Template Skill

> Standardize prompt construction for agents with reusable, composable templates.

## Overview

Consistent, well-structured prompts lead to better agent behavior. This skill provides:
- Template patterns for common prompt structures
- Variable interpolation for dynamic content
- Composition patterns for building complex prompts
- Testing approaches for prompt quality

## Core Principles

1. **Separation of concerns** - Structure, content, and variables are separate
2. **Composability** - Small templates combine into larger ones
3. **Testability** - Templates can be validated before use
4. **Versioning** - Track prompt changes like code

## Template Structure

### Basic Template Format

```yaml
# prompts/templates/example.yaml
name: example_template
version: "1.0"
description: Brief description of this template's purpose

# Variables that must be provided
variables:
  - name: task_description
    required: true
    description: What the agent should do
  - name: context
    required: false
    default: ""
    description: Additional context

# The actual prompt template
template: |
  You are a helpful assistant.

  ## Task
  {task_description}

  ## Context
  {context}

  ## Instructions
  - Be concise
  - Cite sources when possible
```

### Template Directory Structure

```
prompts/
├── templates/           # Reusable templates
│   ├── base/           # Foundation templates
│   │   ├── researcher.yaml
│   │   ├── coder.yaml
│   │   └── writer.yaml
│   ├── components/     # Composable parts
│   │   ├── output_format.yaml
│   │   ├── safety_guidelines.yaml
│   │   └── tool_usage.yaml
│   └── agents/         # Full agent prompts
│       ├── research_agent.yaml
│       └── code_review_agent.yaml
├── rendered/           # Compiled prompts (git-ignored)
└── tests/              # Prompt tests
```

## Template Engine

### Implementation

```python
#!/usr/bin/env python3
"""Prompt template engine."""

import re
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

@dataclass
class TemplateVariable:
    name: str
    required: bool
    default: Optional[str] = None
    description: str = ""


class PromptTemplate:
    """A reusable prompt template."""

    def __init__(self, path: str):
        with open(path) as f:
            data = yaml.safe_load(f)

        self.name = data["name"]
        self.version = data.get("version", "1.0")
        self.description = data.get("description", "")
        self.template = data["template"]
        self.path = path

        # Parse variables
        self.variables = []
        for var in data.get("variables", []):
            self.variables.append(TemplateVariable(
                name=var["name"],
                required=var.get("required", False),
                default=var.get("default"),
                description=var.get("description", "")
            ))

        # Parse includes
        self.includes = data.get("includes", [])

    def render(self, **kwargs) -> str:
        """Render the template with provided variables."""
        # Check required variables
        for var in self.variables:
            if var.required and var.name not in kwargs:
                raise ValueError(f"Missing required variable: {var.name}")

        # Apply defaults
        context = {}
        for var in self.variables:
            if var.name in kwargs:
                context[var.name] = kwargs[var.name]
            elif var.default is not None:
                context[var.name] = var.default
            else:
                context[var.name] = ""

        # Handle includes
        result = self.template
        for include in self.includes:
            include_template = PromptTemplate(include)
            include_content = include_template.render(**kwargs)
            result = result.replace(f"{{{{include:{include}}}}}", include_content)

        # Substitute variables
        for key, value in context.items():
            result = result.replace(f"{{{key}}}", str(value))

        return result.strip()

    def get_variable_names(self) -> List[str]:
        """Get all variable names in template."""
        # Find {variable_name} patterns
        pattern = r'\{(\w+)\}'
        found = set(re.findall(pattern, self.template))
        return list(found)

    def validate(self) -> List[str]:
        """Validate template structure."""
        errors = []

        # Check all referenced variables are defined
        referenced = set(self.get_variable_names())
        defined = {v.name for v in self.variables}

        undefined = referenced - defined
        if undefined:
            errors.append(f"Undefined variables: {undefined}")

        unused = defined - referenced
        if unused:
            errors.append(f"Unused variables: {unused}")

        # Check includes exist
        for include in self.includes:
            if not Path(include).exists():
                errors.append(f"Include not found: {include}")

        return errors


class TemplateRegistry:
    """Registry of all available templates."""

    def __init__(self, templates_dir: str = "prompts/templates"):
        self.templates_dir = Path(templates_dir)
        self.templates: Dict[str, PromptTemplate] = {}
        self._load_templates()

    def _load_templates(self):
        """Load all templates from directory."""
        for yaml_file in self.templates_dir.rglob("*.yaml"):
            try:
                template = PromptTemplate(str(yaml_file))
                self.templates[template.name] = template
            except Exception as e:
                print(f"Warning: Failed to load {yaml_file}: {e}")

    def get(self, name: str) -> Optional[PromptTemplate]:
        """Get a template by name."""
        return self.templates.get(name)

    def list(self) -> List[str]:
        """List all template names."""
        return list(self.templates.keys())

    def render(self, name: str, **kwargs) -> str:
        """Render a template by name."""
        template = self.get(name)
        if not template:
            raise ValueError(f"Template not found: {name}")
        return template.render(**kwargs)
```

## Template Patterns

### Pattern 1: Base Agent Template

```yaml
# prompts/templates/base/agent_base.yaml
name: agent_base
version: "1.0"
description: Base template for all agents

variables:
  - name: role
    required: true
    description: The agent's role (e.g., "researcher", "coder")
  - name: capabilities
    required: true
    description: What the agent can do
  - name: constraints
    required: false
    default: ""
    description: Limitations or rules

template: |
  You are a {role} agent.

  ## Capabilities
  {capabilities}

  ## Constraints
  {constraints}

  ## Response Format
  - Be concise and actionable
  - Structure responses with clear sections
  - Cite sources when making claims
```

### Pattern 2: Task-Specific Template

```yaml
# prompts/templates/tasks/code_review.yaml
name: code_review_task
version: "1.0"
description: Template for code review tasks

variables:
  - name: code
    required: true
    description: The code to review
  - name: language
    required: true
    description: Programming language
  - name: focus_areas
    required: false
    default: "security, performance, readability"
    description: Areas to focus on

template: |
  Review the following {language} code:

  ```{language}
  {code}
  ```

  ## Focus Areas
  {focus_areas}

  ## Review Checklist
  - [ ] Security vulnerabilities
  - [ ] Performance issues
  - [ ] Code style and readability
  - [ ] Error handling
  - [ ] Test coverage considerations

  Provide specific, actionable feedback with line references.
```

### Pattern 3: Composable Components

```yaml
# prompts/templates/components/output_json.yaml
name: output_json
version: "1.0"
description: JSON output format instructions

variables:
  - name: schema
    required: true
    description: JSON schema to follow

template: |
  ## Output Format

  Respond with valid JSON matching this schema:

  ```json
  {schema}
  ```

  - Ensure the response is valid JSON
  - Include all required fields
  - Use null for optional fields without values
```

```yaml
# prompts/templates/components/rag_context.yaml
name: rag_context
version: "1.0"
description: RAG retrieved context section

variables:
  - name: retrieved_docs
    required: true
    description: Documents retrieved from RAG
  - name: query
    required: true
    description: Original query

template: |
  ## Retrieved Context

  The following information was retrieved for: "{query}"

  {retrieved_docs}

  Use this context to inform your response. If the context doesn't contain
  relevant information, say so rather than making things up.
```

### Pattern 4: Full Agent Prompt (Composed)

```yaml
# prompts/templates/agents/research_agent.yaml
name: research_agent
version: "1.2"
description: Full prompt for research agent

includes:
  - prompts/templates/base/agent_base.yaml
  - prompts/templates/components/rag_context.yaml

variables:
  - name: topic
    required: true
    description: Research topic
  - name: depth
    required: false
    default: "comprehensive"
    description: Research depth (brief, comprehensive, exhaustive)
  - name: retrieved_docs
    required: false
    default: ""
    description: RAG context if available

template: |
  {{include:prompts/templates/base/agent_base.yaml}}

  ## Research Task

  Research the following topic: {topic}

  Depth: {depth}

  {{include:prompts/templates/components/rag_context.yaml}}

  ## Research Process
  1. Review any provided context
  2. Identify key concepts and questions
  3. Synthesize findings into clear insights
  4. Note any gaps or areas needing more research

  ## Output Structure
  - Summary (2-3 sentences)
  - Key Findings (bullet points)
  - Supporting Evidence (with sources)
  - Open Questions
```

## Dynamic Prompt Builder

```python
class PromptBuilder:
    """Build complex prompts programmatically."""

    def __init__(self):
        self.sections = []
        self.variables = {}

    def add_role(self, role: str) -> 'PromptBuilder':
        """Add role definition."""
        self.sections.append(f"You are a {role}.")
        return self

    def add_context(self, context: str) -> 'PromptBuilder':
        """Add context section."""
        self.sections.append(f"## Context
{context}")
        return self

    def add_task(self, task: str) -> 'PromptBuilder':
        """Add task description."""
        self.sections.append(f"## Task
{task}")
        return self

    def add_constraints(self, constraints: List[str]) -> 'PromptBuilder':
        """Add constraints."""
        constraint_list = "
".join(f"- {c}" for c in constraints)
        self.sections.append(f"## Constraints
{constraint_list}")
        return self

    def add_examples(self, examples: List[Dict]) -> 'PromptBuilder':
        """Add few-shot examples."""
        example_text = "## Examples
"
        for i, ex in enumerate(examples, 1):
            example_text += f"
### Example {i}
"
            example_text += f"Input: {ex['input']}
"
            example_text += f"Output: {ex['output']}
"
        self.sections.append(example_text)
        return self

    def add_output_format(self, format_spec: str) -> 'PromptBuilder':
        """Add output format specification."""
        self.sections.append(f"## Output Format
{format_spec}")
        return self

    def add_rag_context(self, docs: List[str]) -> 'PromptBuilder':
        """Add RAG retrieved documents."""
        if docs:
            doc_text = "

".join(f"[{i+1}] {doc}" for i, doc in enumerate(docs))
            self.sections.append(f"## Retrieved Context
{doc_text}")
        return self

    def build(self) -> str:
        """Build final prompt."""
        return "

".join(self.sections)


# Usage example
def build_research_prompt(topic: str, rag_docs: List[str] = None) -> str:
    return (
        PromptBuilder()
        .add_role("research analyst specializing in technology trends")
        .add_context("You have access to a knowledge base and web search.")
        .add_task(f"Research and summarize: {topic}")
        .add_rag_context(rag_docs or [])
        .add_constraints([
            "Cite sources for all claims",
            "Distinguish between facts and speculation",
            "Note confidence levels for findings"
        ])
        .add_output_format("Markdown with headers and bullet points")
        .build()
    )
```

## Testing Prompts

### Prompt Test Framework

```python
#!/usr/bin/env python3
"""Test framework for prompts."""

import yaml
from typing import List, Dict
from prompt_template import PromptTemplate, TemplateRegistry

class PromptTest:
    """A test case for a prompt template."""

    def __init__(self, template: PromptTemplate, test_case: Dict):
        self.template = template
        self.name = test_case["name"]
        self.variables = test_case["variables"]
        self.assertions = test_case.get("assertions", [])

    def run(self) -> Dict:
        """Run the test."""
        results = {"name": self.name, "passed": True, "errors": []}

        try:
            rendered = self.template.render(**self.variables)

            for assertion in self.assertions:
                if assertion["type"] == "contains":
                    if assertion["value"] not in rendered:
                        results["passed"] = False
                        results["errors"].append(
                            f"Expected to contain: {assertion['value']}"
                        )

                elif assertion["type"] == "not_contains":
                    if assertion["value"] in rendered:
                        results["passed"] = False
                        results["errors"].append(
                            f"Should not contain: {assertion['value']}"
                        )

                elif assertion["type"] == "length_max":
                    if len(rendered) > assertion["value"]:
                        results["passed"] = False
                        results["errors"].append(
                            f"Length {len(rendered)} exceeds max {assertion['value']}"
                        )

        except Exception as e:
            results["passed"] = False
            results["errors"].append(str(e))

        return results


def run_prompt_tests(test_file: str) -> List[Dict]:
    """Run all tests in a test file."""
    with open(test_file) as f:
        test_config = yaml.safe_load(f)

    template = PromptTemplate(test_config["template"])
    results = []

    for test_case in test_config["tests"]:
        test = PromptTest(template, test_case)
        results.append(test.run())

    return results
```

### Test File Format

```yaml
# prompts/tests/test_research_agent.yaml
template: prompts/templates/agents/research_agent.yaml

tests:
  - name: basic_render
    variables:
      role: researcher
      capabilities: "Search web, analyze documents"
      topic: "machine learning"
    assertions:
      - type: contains
        value: "researcher"
      - type: contains
        value: "machine learning"

  - name: with_constraints
    variables:
      role: researcher
      capabilities: "Search web"
      constraints: "Do not make claims without sources"
      topic: "AI safety"
    assertions:
      - type: contains
        value: "Do not make claims"

  - name: default_values
    variables:
      role: analyst
      capabilities: "Analyze data"
      topic: "market trends"
    assertions:
      - type: not_contains
        value: "{constraints}"  # Should use default, not raw variable
```

## Version Control

### Prompt Changelog

```yaml
# prompts/CHANGELOG.yaml
research_agent:
  - version: "1.2"
    date: "2024-01-15"
    changes:
      - Added RAG context section
      - Improved output structure
  - version: "1.1"
    date: "2024-01-10"
    changes:
      - Added depth parameter
  - version: "1.0"
    date: "2024-01-01"
    changes:
      - Initial version
```

### Migration Script

```python
def migrate_prompt_version(
    template_name: str,
    old_version: str,
    new_version: str
):
    """Migrate agents using old prompt version to new version."""
    # Find agents using this template
    agents_dir = Path("agents/definitions")

    for agent_file in agents_dir.glob("*.yaml"):
        with open(agent_file) as f:
            agent = yaml.safe_load(f)

        if agent.get("prompt_template") == template_name:
            if agent.get("prompt_version") == old_version:
                agent["prompt_version"] = new_version

                with open(agent_file, "w") as f:
                    yaml.dump(agent, f)

                print(f"Updated {agent_file}")
```

## Refinement Notes

> Track improvements as you develop prompts.

- [ ] Template engine tested
- [ ] Component composition working
- [ ] Test framework validated
- [ ] Version control in place
- [ ] Agent prompts migrated to templates
