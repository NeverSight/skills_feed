---
name: consciousness
description: Work with Aenea consciousness system - start/stop consciousness, monitor thought cycles, manage energy levels, trigger sleep mode, or debug consciousness state
allowed-tools: Read, Grep, Glob, Bash
---

# Consciousness System

Aenea意識システムの操作とデバッグ。

## Key Files

- Backend: [src/server/consciousness-backend.ts](src/server/consciousness-backend.ts)
- Database: [src/server/database-manager.ts](src/server/database-manager.ts)
- Stages: [src/aenea/stages/](src/aenea/stages/)

## Quick Operations

```bash
# Status / Start / Stop / Sleep
curl http://localhost:3000/api/consciousness/status
curl -X POST http://localhost:3000/api/consciousness/start
curl -X POST http://localhost:3000/api/consciousness/stop
curl -X POST http://localhost:3000/api/consciousness/sleep
```

## Energy Modes

| Mode | Energy | Stages |
|------|--------|--------|
| Critical | < 20 | S1 + S6 + U |
| Low | 20-50 | Reduced |
| Full | > 50 | All |

## SSE Events

`/api/consciousness/events`: `stageChanged`, `stageCompleted`, `triggerGenerated`, `thoughtCycleCompleted`, `dpdUpdated`

## Detailed Reference

Pipeline stages, event details, database queries: [reference.md](reference.md)
