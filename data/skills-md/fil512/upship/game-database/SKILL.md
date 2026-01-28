---
name: game-database
description: Database design for multiplayer games with PostgreSQL. Use when designing schemas, handling game persistence, managing user accounts, implementing lobbies, or optimizing queries. Covers JSONB for game state and relational patterns.
---

# Game Database Skill

## Overview

This skill provides expertise for designing and implementing database schemas for multiplayer turn-based games. It covers PostgreSQL patterns, game state persistence, user management, and the hybrid approach of relational tables with JSONB for complex game state.

## Database Selection

### Why PostgreSQL for Games

- **JSONB support**: Store complex game state as JSON while keeping it queryable
- **ACID transactions**: Critical for game state consistency
- **Row-level locking**: Handle concurrent updates safely
- **Railway integration**: Easy deployment and management
- **Mature ecosystem**: Excellent Node.js support via pg or Prisma

## Schema Design Patterns

### Core Tables

```sql
-- Users table
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  username VARCHAR(50) UNIQUE NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  display_name VARCHAR(100),
  avatar_url VARCHAR(500),
  created_at TIMESTAMP DEFAULT NOW(),
  last_login TIMESTAMP,
  is_active BOOLEAN DEFAULT true
);

-- Games table (lobby + active games)
CREATE TABLE games (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(100) NOT NULL,
  status VARCHAR(20) DEFAULT 'waiting',  -- waiting, in_progress, completed, abandoned
  host_id UUID REFERENCES users(id),
  min_players INTEGER DEFAULT 2,
  max_players INTEGER DEFAULT 4,
  settings JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT NOW(),
  started_at TIMESTAMP,
  completed_at TIMESTAMP,

  CONSTRAINT valid_status CHECK (status IN ('waiting', 'in_progress', 'completed', 'abandoned'))
);

-- Game players (join table)
CREATE TABLE game_players (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  game_id UUID REFERENCES games(id) ON DELETE CASCADE,
  user_id UUID REFERENCES users(id),
  faction VARCHAR(50),
  seat_position INTEGER,
  joined_at TIMESTAMP DEFAULT NOW(),
  is_ready BOOLEAN DEFAULT false,

  UNIQUE(game_id, user_id),
  UNIQUE(game_id, seat_position)
);

-- Game state (the actual game data)
CREATE TABLE game_states (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  game_id UUID REFERENCES games(id) ON DELETE CASCADE UNIQUE,
  version INTEGER DEFAULT 1,
  current_player_id UUID REFERENCES users(id),
  phase VARCHAR(50),
  turn_number INTEGER DEFAULT 1,
  age INTEGER DEFAULT 1,
  state JSONB NOT NULL,  -- The full game state
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Action history (for replay/undo)
CREATE TABLE game_actions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  game_id UUID REFERENCES games(id) ON DELETE CASCADE,
  player_id UUID REFERENCES users(id),
  action_type VARCHAR(50) NOT NULL,
  action_data JSONB NOT NULL,
  state_version INTEGER NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for common queries
CREATE INDEX idx_games_status ON games(status);
CREATE INDEX idx_games_host ON games(host_id);
CREATE INDEX idx_game_players_user ON game_players(user_id);
CREATE INDEX idx_game_players_game ON game_players(game_id);
CREATE INDEX idx_game_actions_game ON game_actions(game_id);
CREATE INDEX idx_game_states_game ON game_states(game_id);
```

### JSONB for Game State

Store complex, nested game state as JSONB:

```javascript
// Example game state stored in game_states.state
{
  "players": {
    "uuid-1": {
      "money": 15,
      "income": 5,
      "pilots": 2,
      "engineers": 3,
      "technologies": ["tech-1", "tech-2"],
      "blueprint": {
        "slots": {
          "frame-1": { "upgradeId": "upg-1" },
          "drive-1": { "upgradeId": null }
        }
      },
      "hangar": {
        "launch": ["ship-1"],
        "repair": []
      }
    }
  },
  "board": {
    "locations": {
      "construction-hall": { "workers": ["w1", "w2"] }
    },
    "rdBoard": {
      "available": ["tech-3", "tech-4", "tech-5"]
    }
  },
  "progress": 8,
  "market": {
    "heliumPrice": 5,
    "visibleCards": ["card-1", "card-2", "card-3"]
  }
}
```

### Querying JSONB

```sql
-- Find games where a specific player has more than 20 money
SELECT g.id, g.name
FROM games g
JOIN game_states gs ON g.id = gs.game_id
WHERE gs.state->'players'->>'uuid-1'->>'money' > '20';

-- Find all technologies owned by a player
SELECT gs.state->'players'->'uuid-1'->'technologies' as techs
FROM game_states gs
WHERE gs.game_id = 'game-uuid';

-- Update a specific field in JSONB
UPDATE game_states
SET state = jsonb_set(
  state,
  '{players,uuid-1,money}',
  to_jsonb((state->'players'->'uuid-1'->>'money')::int + 10)
)
WHERE game_id = 'game-uuid';
```

## Data Access Patterns

### Repository Pattern

```javascript
// gameRepository.js
const { pool } = require('./db');

const gameRepository = {
  async create(hostId, name, settings = {}) {
    const result = await pool.query(`
      INSERT INTO games (host_id, name, settings)
      VALUES ($1, $2, $3)
      RETURNING *
    `, [hostId, name, settings]);
    return result.rows[0];
  },

  async findById(gameId) {
    const result = await pool.query(`
      SELECT g.*, gs.state, gs.version
      FROM games g
      LEFT JOIN game_states gs ON g.id = gs.game_id
      WHERE g.id = $1
    `, [gameId]);
    return result.rows[0];
  },

  async findWaitingGames() {
    const result = await pool.query(`
      SELECT g.*, COUNT(gp.id) as player_count
      FROM games g
      LEFT JOIN game_players gp ON g.id = gp.game_id
      WHERE g.status = 'waiting'
      GROUP BY g.id
      ORDER BY g.created_at DESC
    `);
    return result.rows;
  },

  async updateState(gameId, newState, newVersion) {
    const result = await pool.query(`
      UPDATE game_states
      SET state = $2, version = $3, updated_at = NOW()
      WHERE game_id = $1 AND version = $3 - 1
      RETURNING *
    `, [gameId, newState, newVersion]);

    if (result.rows.length === 0) {
      throw new Error('Optimistic lock failed - state was modified');
    }
    return result.rows[0];
  }
};
```

### Transaction Handling

```javascript
async function processGameAction(gameId, playerId, action) {
  const client = await pool.connect();

  try {
    await client.query('BEGIN');

    // Lock the game state row
    const stateResult = await client.query(`
      SELECT * FROM game_states
      WHERE game_id = $1
      FOR UPDATE
    `, [gameId]);

    const currentState = stateResult.rows[0];

    // Validate and apply action
    const validation = validateAction(currentState.state, action);
    if (!validation.valid) {
      await client.query('ROLLBACK');
      return { success: false, error: validation.reason };
    }

    const newState = applyAction(currentState.state, action);
    const newVersion = currentState.version + 1;

    // Save new state
    await client.query(`
      UPDATE game_states
      SET state = $1, version = $2, updated_at = NOW()
      WHERE game_id = $3
    `, [newState, newVersion, gameId]);

    // Record action in history
    await client.query(`
      INSERT INTO game_actions (game_id, player_id, action_type, action_data, state_version)
      VALUES ($1, $2, $3, $4, $5)
    `, [gameId, playerId, action.type, action, newVersion]);

    await client.query('COMMIT');

    return { success: true, newState, version: newVersion };

  } catch (error) {
    await client.query('ROLLBACK');
    throw error;
  } finally {
    client.release();
  }
}
```

## Optimistic Locking

Prevent concurrent modification conflicts:

```javascript
async function updateGameState(gameId, newState, expectedVersion) {
  const result = await pool.query(`
    UPDATE game_states
    SET
      state = $2,
      version = version + 1,
      updated_at = NOW()
    WHERE game_id = $1 AND version = $3
    RETURNING version
  `, [gameId, newState, expectedVersion]);

  if (result.rows.length === 0) {
    // Version mismatch - someone else updated first
    throw new OptimisticLockError('State was modified by another request');
  }

  return result.rows[0].version;
}
```

## User Session Management

```sql
-- Sessions table
CREATE TABLE sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  token VARCHAR(255) UNIQUE NOT NULL,
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  ip_address INET,
  user_agent TEXT
);

CREATE INDEX idx_sessions_token ON sessions(token);
CREATE INDEX idx_sessions_user ON sessions(user_id);
CREATE INDEX idx_sessions_expires ON sessions(expires_at);
```

```javascript
// Session repository
const sessionRepository = {
  async create(userId, token, expiresAt) {
    await pool.query(`
      INSERT INTO sessions (user_id, token, expires_at)
      VALUES ($1, $2, $3)
    `, [userId, token, expiresAt]);
  },

  async findByToken(token) {
    const result = await pool.query(`
      SELECT s.*, u.username, u.display_name
      FROM sessions s
      JOIN users u ON s.user_id = u.id
      WHERE s.token = $1 AND s.expires_at > NOW()
    `, [token]);
    return result.rows[0];
  },

  async deleteExpired() {
    await pool.query(`DELETE FROM sessions WHERE expires_at < NOW()`);
  }
};
```

## Game Lobby Queries

```javascript
const lobbyRepository = {
  // Get games available to join
  async getAvailableGames() {
    return pool.query(`
      SELECT
        g.id,
        g.name,
        g.settings,
        g.max_players,
        g.created_at,
        u.display_name as host_name,
        COUNT(gp.id) as current_players,
        array_agg(json_build_object(
          'id', pu.id,
          'name', pu.display_name,
          'faction', gp.faction
        )) as players
      FROM games g
      JOIN users u ON g.host_id = u.id
      LEFT JOIN game_players gp ON g.id = gp.game_id
      LEFT JOIN users pu ON gp.user_id = pu.id
      WHERE g.status = 'waiting'
      GROUP BY g.id, u.display_name
      HAVING COUNT(gp.id) < g.max_players
      ORDER BY g.created_at DESC
    `);
  },

  // Get player's active games
  async getPlayerGames(userId) {
    return pool.query(`
      SELECT g.*, gs.phase, gs.current_player_id
      FROM games g
      JOIN game_players gp ON g.id = gp.game_id
      LEFT JOIN game_states gs ON g.id = gs.game_id
      WHERE gp.user_id = $1
        AND g.status IN ('waiting', 'in_progress')
      ORDER BY g.created_at DESC
    `, [userId]);
  }
};
```

## Database Migrations

Use a migration system for schema changes:

```javascript
// migrations/001_initial_schema.js
exports.up = async (client) => {
  await client.query(`
    CREATE TABLE users (
      id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
      username VARCHAR(50) UNIQUE NOT NULL,
      -- ... rest of schema
    );
  `);
};

exports.down = async (client) => {
  await client.query(`DROP TABLE IF EXISTS users CASCADE`);
};
```

```javascript
// Simple migration runner
async function runMigrations() {
  const client = await pool.connect();

  await client.query(`
    CREATE TABLE IF NOT EXISTS migrations (
      id SERIAL PRIMARY KEY,
      name VARCHAR(255) NOT NULL,
      run_at TIMESTAMP DEFAULT NOW()
    )
  `);

  const migrations = require('./migrations');

  for (const [name, migration] of Object.entries(migrations)) {
    const existing = await client.query(
      'SELECT id FROM migrations WHERE name = $1',
      [name]
    );

    if (existing.rows.length === 0) {
      console.log(`Running migration: ${name}`);
      await migration.up(client);
      await client.query(
        'INSERT INTO migrations (name) VALUES ($1)',
        [name]
      );
    }
  }

  client.release();
}
```

## Connection Pooling

```javascript
// db.js
const { Pool } = require('pg');

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,                    // Max connections in pool
  idleTimeoutMillis: 30000,   // Close idle connections after 30s
  connectionTimeoutMillis: 2000
});

// Health check
pool.on('error', (err) => {
  console.error('Unexpected error on idle client', err);
});

async function healthCheck() {
  const client = await pool.connect();
  try {
    await client.query('SELECT 1');
    return true;
  } finally {
    client.release();
  }
}

module.exports = { pool, healthCheck };
```

## Railway PostgreSQL Setup

```javascript
// Railway provides DATABASE_URL automatically
const connectionString = process.env.DATABASE_URL;

// For SSL in production
const pool = new Pool({
  connectionString,
  ssl: process.env.NODE_ENV === 'production'
    ? { rejectUnauthorized: false }
    : false
});
```

## When This Skill Activates

Use this skill when:
- Designing database schemas for games
- Implementing game state persistence
- Building user authentication storage
- Creating lobby/matchmaking queries
- Handling concurrent state updates
- Setting up migrations
- Optimizing database queries
