---
name: shared
description: Shared reference documents for distributed mode skills (not directly invocable)
internal: true
---

# Shared References

This directory contains shared reference documents used by multiple skills:

- `agent-mail-protocol.md` - Message protocol for distributed mode coordination
- `validation-contract.md` - Verification requirements for accepting spawned work

These are **not directly invocable skills**. They are loaded by other skills (crank, swarm, inbox, implement) when needed for distributed mode operation.
