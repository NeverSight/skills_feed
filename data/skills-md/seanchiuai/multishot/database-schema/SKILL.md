---
name: database-schema
description: SQLite database schema and operations using better-sqlite3. Use when working with StateManager, persisting runs/rounds/agents, or querying run history.
---

# Database Schema

> **STATUS: NOT IMPLEMENTED IN MVP**
> This skill documents the planned schema for post-MVP persistence.
> MVP currently has no database - all state is in-memory.

Location: `~/.multishot/database.sqlite`

## Tables

```sql
CREATE TABLE runs (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  created_at INTEGER NOT NULL,
  status TEXT NOT NULL,  -- 'active' | 'completed'
  current_round_id TEXT,
  FOREIGN KEY (current_round_id) REFERENCES rounds(id)
);

CREATE TABLE rounds (
  id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL,
  round_number INTEGER NOT NULL,
  base_prompt TEXT NOT NULL,
  created_at INTEGER NOT NULL,
  winner_agent_id TEXT,
  winner_files_path TEXT,
  status TEXT NOT NULL,  -- 'running' | 'selecting' | 'completed'
  FOREIGN KEY (run_id) REFERENCES runs(id),
  FOREIGN KEY (winner_agent_id) REFERENCES agents(id)
);

CREATE TABLE agents (
  id TEXT PRIMARY KEY,
  round_id TEXT NOT NULL,
  agent_number INTEGER NOT NULL,  -- 1-4
  sandbox_id TEXT,
  variation_prompt TEXT NOT NULL,
  status TEXT NOT NULL,  -- 'initializing' | 'running' | 'completed' | 'failed' | 'selected'
  created_at INTEGER NOT NULL,
  completed_at INTEGER,
  error_message TEXT,
  FOREIGN KEY (round_id) REFERENCES rounds(id)
);

CREATE TABLE output_logs (
  id TEXT PRIMARY KEY,
  agent_id TEXT NOT NULL,
  timestamp INTEGER NOT NULL,
  content TEXT NOT NULL,
  FOREIGN KEY (agent_id) REFERENCES agents(id)
);

CREATE TABLE credentials (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL,  -- Reference to safeStorage, not plaintext
  updated_at INTEGER NOT NULL
);
```

## Indexes

```sql
CREATE INDEX idx_runs_created_at ON runs(created_at DESC);
CREATE INDEX idx_agents_round_id ON agents(round_id);
CREATE INDEX idx_logs_agent_id ON output_logs(agent_id);
```

## better-sqlite3 Usage

```typescript
import Database from 'better-sqlite3'

const db = new Database(path.join(os.homedir(), '.multishot', 'database.sqlite'))

// Synchronous API (no async/await needed)
const run = db.prepare('SELECT * FROM runs WHERE id = ?').get(runId)
const agents = db.prepare('SELECT * FROM agents WHERE round_id = ?').all(roundId)

db.prepare('INSERT INTO runs (id, name, created_at, status) VALUES (?, ?, ?, ?)')
  .run(id, name, Date.now(), 'active')
```

## File Storage

Winner files extracted to: `~/.multishot/runs/[run-uuid]/round-N-winner/`

Logs archived to: `~/.multishot/runs/[run-uuid]/logs/agent-N.log`
