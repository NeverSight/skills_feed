---
name: skill-system-postgres
description: "Postgres-backed observability and policy store for the skill system. Provides tables for policy profiles (effect allowlists), skill execution runs, and step-level events. Use when setting up the skill system database or querying execution history."
license: MIT
compatibility: opencode
metadata:
  storage: postgresql
  os: windows, linux, macos
---

# Skill System (Postgres State)

Database schema for skill system observability and policy.

## Install

```bash
psql -U postgres -d agent_memory -v ON_ERROR_STOP=1 -f init.sql
```

```powershell
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -d agent_memory -v "ON_ERROR_STOP=1" -f init.sql
```

For existing v1 installations, also run `migrate-v2.sql`.

## Tables

- `skill_system.policy_profiles` — effect allowlists (what skills are allowed to do)
- `skill_system.runs` — execution records (goal, agent, status, duration, metrics)
- `skill_system.run_events` — step-level event log (which skill, which op, result)

## Usage

The Agent writes to these tables as instructed by the Router skill. This skill does not execute anything — it's a state store.

```skill-manifest
{
  "schema_version": "2.0",
  "id": "skill-system-postgres",
  "version": "1.0.0",
  "capabilities": ["skill-policy-check", "skill-run-log"],
  "effects": ["db.read", "db.write"],
  "operations": {
    "check-policy": {
      "description": "Check if a skill's effects are allowed by the active policy profile.",
      "input": {
        "policy_name": { "type": "string", "required": true, "description": "Policy profile name (e.g. dev)" },
        "effects": { "type": "json", "required": true, "description": "Array of effect strings to check" }
      },
      "output": {
        "description": "Whether all effects are allowed",
        "fields": { "allowed": "boolean", "blocked_effects": "array" }
      },
      "entrypoints": {
        "agent": "Query skill_system.policy_profiles WHERE name = policy_name"
      }
    },
    "log-run": {
      "description": "Log a skill execution run for observability.",
      "input": {
        "skill_id": { "type": "string", "required": true },
        "operation": { "type": "string", "required": true },
        "status": { "type": "string", "required": true },
        "duration_ms": { "type": "integer", "required": false }
      },
      "output": {
        "description": "Run ID",
        "fields": { "run_id": "integer" }
      },
      "entrypoints": {
        "agent": "INSERT INTO skill_system.runs and skill_system.run_events"
      }
    }
  },
  "stdout_contract": {
    "last_line_json": false,
    "note": "Agent-executed SQL; no executable scripts."
  }
}
```
