---
name: agent-capability-discovery
description: Scans all skill directories in the repository to generate a comprehensive global map of agent capabilities, inputs, and outputs. Use when you need to understand the full potential of your agent library or when a master agent needs to decide which sub-agent skill to invoke for a complex task.
---
# Agent Capability Discovery

## Purpose and Intent
The `agent-capability-discovery` skill is the "brain" of a multi-agent system. It allows an agent to self-reflect and understand what tools and expertises are available within its environment by indexing all `skill.yaml` files.

## When to Use
- **System Initialization**: Run this when an agent starts up to populate its internal tool list.
- **Routing Decisions**: Use this when a master agent receives a complex user request and needs to identify which specialized skill (e.g., `hipaa-compliance-guard` vs. `pii-sanitizer`) is best suited for the job.
- **Documentation Generation**: Automatically keep a "Global Skills Map" up to date for human developers.

## When NOT to Use
- **Skill Execution**: This skill only *discovers* what is possible; it does not execute the other skills.
- **External Tooling**: It only indexes skills defined in the local repository structure.

## Input and Output Examples

### Input
```yaml
base_directory: "."
output_format: "markdown"
```

### Output
A markdown table or JSON object listing all discovered skills, their descriptions, and their primary capabilities.

## Error Conditions and Edge Cases
- **Broken YAML**: If a `skill.yaml` is malformed, the discovery tool will skip that directory and report a warning.
- **Circular Dependencies**: This tool does not handle execution dependencies, only discovery.

## Security and Data-Handling Considerations
- **Metadata Only**: The tool only reads the definition files; it never touches actual source code or data unless instructed by the indexed skills themselves.
- **Local Scope**: Discovery is confined to the provided root directory to prevent directory traversal attacks.
