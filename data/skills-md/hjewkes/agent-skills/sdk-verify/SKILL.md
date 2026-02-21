---
name: sdk-verify
description: Verify Claude Agent SDK applications. Use after creating or modifying TypeScript or Python Agent SDK apps to check configuration and best practices.
---

# Agent SDK Verifiers

Available agents (spawn via Task tool with `general-purpose` type):

- **agent-sdk-verifier-ts** — TypeScript SDK verification
- **agent-sdk-verifier-py** — Python SDK verification

## Usage

1. Read the corresponding reference file for the agent's full system prompt
2. Spawn a `general-purpose` Task agent with that prompt
3. Point it at the SDK application directory

## Reference Files

| Agent | Reference |
|-------|-----------|
| agent-sdk-verifier-ts | [references/verifier-ts.md](references/verifier-ts.md) |
| agent-sdk-verifier-py | [references/verifier-py.md](references/verifier-py.md) |
