---
name: near-ai
description: NEAR AI agent development and integration. Use when building AI agents on NEAR, integrating AI models, creating agent workflows, or implementing AI-powered dApps on NEAR Protocol.
license: MIT
metadata:
  author: near
  version: "1.0.0"
---

# NEAR AI Development

Comprehensive guide for building AI agents and AI-powered applications on NEAR Protocol, including NEAR AI integration, agent workflows, and AI model deployment.

## When to Apply

Reference these guidelines when:
- Building AI agents on NEAR
- Integrating AI models with NEAR smart contracts
- Creating agent-based workflows
- Implementing AI-powered dApps
- Using NEAR AI infrastructure
- Building with NEAR AI Assistant

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Agent Architecture | CRITICAL | `arch-` |
| 2 | AI Integration | HIGH | `ai-` |
| 3 | Agent Communication | HIGH | `comm-` |
| 4 | Model Deployment | MEDIUM-HIGH | `model-` |
| 5 | Agent Workflows | MEDIUM | `workflow-` |
| 6 | Security & Privacy | MEDIUM | `security-` |
| 7 | Best Practices | MEDIUM | `best-` |

## Quick Reference

### 1. Agent Architecture (CRITICAL)

- `arch-agent-structure` - Design modular agent architecture
- `arch-state-management` - Manage agent state on-chain vs off-chain
- `arch-agent-registry` - Register agents in NEAR AI registry
- `arch-composability` - Build composable agents
- `arch-agent-capabilities` - Define clear agent capabilities

### 2. AI Integration (HIGH)

- `ai-model-selection` - Choose appropriate AI models
- `ai-inference-endpoints` - Use NEAR AI inference endpoints
- `ai-prompt-engineering` - Design effective prompts for agents
- `ai-context-management` - Manage conversation context
- `ai-response-validation` - Validate and sanitize AI responses

### 3. Agent Communication (HIGH)

- `comm-agent-protocol` - Implement standard agent communication protocols
- `comm-message-format` - Use structured message formats
- `comm-async-messaging` - Handle asynchronous agent communication
- `comm-multi-agent` - Coordinate multiple agents
- `comm-human-in-loop` - Implement human-in-the-loop patterns

### 4. Model Deployment (MEDIUM-HIGH)

- `model-hosting` - Deploy models on NEAR AI infrastructure
- `model-versioning` - Version and update AI models
- `model-optimization` - Optimize models for inference
- `model-monitoring` - Monitor model performance
- `model-fallbacks` - Implement fallback strategies

### 5. Agent Workflows (MEDIUM)

- `workflow-task-planning` - Implement agent task planning
- `workflow-execution` - Execute multi-step workflows
- `workflow-error-handling` - Handle workflow errors gracefully
- `workflow-state-persistence` - Persist workflow state
- `workflow-composability` - Compose workflows from smaller tasks

### 6. Security & Privacy (MEDIUM)

- `security-input-validation` - Validate user inputs to agents
- `security-output-sanitization` - Sanitize agent outputs
- `security-access-control` - Implement agent access control
- `security-data-privacy` - Protect user data privacy
- `security-prompt-injection` - Prevent prompt injection attacks

### 7. Best Practices (MEDIUM)

- `best-error-messages` - Provide clear error messages
- `best-logging` - Log agent interactions for debugging
- `best-testing` - Test agent behavior comprehensively
- `best-documentation` - Document agent capabilities and APIs
- `best-user-feedback` - Collect and incorporate user feedback

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/arch-agent-structure.md
rules/ai-inference-endpoints.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and NEAR AI-specific patterns

## NEAR AI Components

### NEAR AI Hub
Central registry for AI agents, models, and datasets on NEAR.

### NEAR AI Assistant
Infrastructure for building conversational AI agents.

### Agent Registry
On-chain registry for discovering and interacting with agents.

### Inference Endpoints
Decentralized inference infrastructure for AI models.

## Resources

- NEAR AI Documentation: https://docs.near.ai/
- NEAR AI Hub: https://app.near.ai/
- NEAR AI GitHub: https://github.com/near/nearai
- Agent Examples: https://github.com/near/nearai/tree/main/examples
- NEAR AI Research: https://near.ai/research

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
