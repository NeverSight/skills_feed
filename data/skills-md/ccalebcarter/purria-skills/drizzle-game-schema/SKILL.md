---
name: drizzle-game-schema
description: Drizzle ORM database schema patterns for games including player profiles, inventories, leaderboards, game sessions, and achievements. Use when designing database schemas, creating migrations, optimizing queries, or implementing save systems. Triggers on requests for game database design, Drizzle schemas, player data storage, or leaderboard systems.
---

# Drizzle Game Schema

Production-ready database patterns for game persistence using Drizzle ORM with SQLite/Turso.

## Schema Organization

```
packages/db/src/schema/
├── index.ts          # Export all schemas
├── auth.ts           # Better-Auth tables
├── player.ts         # Player profiles, stats
├── inventory.ts      # Items, currencies
├── game-session.ts   # Active game state
├── progression.ts    # Achievements, unlocks
└── social.ts         # Leaderboards, friends
```

## Core Schemas

### Player Profile

```typescript
// schema/player.ts
import { sqliteTable, text, integer, real } from 'drizzle-orm/sqlite-core';
import { user } from './auth';

export const playerProfile = sqliteTable('player_profile', {
  id: text('id').primaryKey(),
  userId: text('user_id').notNull().references(() => user.id, { onDelete: 'cascade' }),
  
  // Display
  displayName: text('display_name').notNull(),
  avatarUrl: text('avatar_url'),
  
  // Stats
  totalScore: integer('total_score').notNull().default(0),
  highScore: integer('high_score').notNull().default(0),
  gamesPlayed: integer('games_played').notNull().default(0),
  totalPlayTime: integer('total_play_time').notNull().default(0), // seconds
  
  // Progression
  level: integer('level').notNull().default(1),
  experience: integer('experience').notNull().default(0),
  
  // Timestamps
  createdAt: integer('created_at', { mode: 'timestamp' }).notNull().$defaultFn(() => new Date()),
  updatedAt: integer('updated_at', { mode: 'timestamp' }).notNull().$defaultFn(() => new Date()),
  lastActiveAt: integer('last_active_at', { mode: 'timestamp' }),
});

// Indexes for common queries
export const playerProfileIndexes = {
  byUserId: sqliteIndex('player_by_user').on(playerProfile.userId),
  byScore: sqliteIndex('player_by_score').on(playerProfile.totalScore),
  byLevel: sqliteIndex('player_by_level').on(playerProfile.level),
};
```

### Inventory & Currencies

```typescript
// schema/inventory.ts
import { sqliteTable, text, integer, real, primaryKey } from 'drizzle-orm/sqlite-core';

export const playerCurrency = sqliteTable('player_currency', {
  playerId: text('player_id').notNull().references(() => playerProfile.id),
  currencyType: text('currency_type').notNull(), // 'coins', 'tulipBulbs', 'seeds'
  amount: integer('amount').notNull().default(0),
  lifetimeEarned: integer('lifetime_earned').notNull().default(0),
  updatedAt: integer('updated_at', { mode: 'timestamp' }).notNull(),
}, (table) => ({
  pk: primaryKey({ columns: [table.playerId, table.currencyType] }),
}));

export const inventoryItem = sqliteTable('inventory_item', {
  id: text('id').primaryKey(),
  playerId: text('player_id').notNull().references(() => playerProfile.id),
  
  itemType: text('item_type').notNull(),    // 'simulin', 'seed', 'decoration'
  itemId: text('item_id').notNull(),         // Reference to item definition
  quantity: integer('quantity').notNull().default(1),
  
  // Item state (for unique items like Simulins)
  metadata: text('metadata', { mode: 'json' }).$type<Record<string, unknown>>(),
  
  acquiredAt: integer('acquired_at', { mode: 'timestamp' }).notNull(),
  equippedSlot: text('equipped_slot'), // null if not equipped
});

export const inventoryIndexes = {
  byPlayer: sqliteIndex('inv_by_player').on(inventoryItem.playerId),
  byType: sqliteIndex('inv_by_type').on(inventoryItem.playerId, inventoryItem.itemType),
};
```

### Game Session (Save State)

```typescript
// schema/game-session.ts
import { sqliteTable, text, integer, blob } from 'drizzle-orm/sqlite-core';

export const gameSession = sqliteTable('game_session', {
  id: text('id').primaryKey(),
  playerId: text('player_id').notNull().references(() => playerProfile.id),
  
  // Session metadata
  sessionType: text('session_type').notNull(), // 'campaign', 'daily', 'event'
  status: text('status').notNull().default('active'), // 'active', 'completed', 'abandoned'
  
  // Game state (serialized)
  gameState: text('game_state', { mode: 'json' }).$type<{
    time: { season: number; day: number; phase: string };
    resources: { tulipBulbs: number; coins: number; stamina: number };
    hexes: Record<string, unknown>;
    troubles: Record<string, unknown>;
    score: number;
  }>(),
  
  // Metrics
  startedAt: integer('started_at', { mode: 'timestamp' }).notNull(),
  lastSavedAt: integer('last_saved_at', { mode: 'timestamp' }).notNull(),
  completedAt: integer('completed_at', { mode: 'timestamp' }),
  playDuration: integer('play_duration').notNull().default(0), // seconds
  
  // Results (when completed)
  finalScore: integer('final_score'),
  rewards: text('rewards', { mode: 'json' }).$type<{
    coins: number;
    experience: number;
    items: string[];
  }>(),
});
```

### Achievements & Unlocks

```typescript
// schema/progression.ts
import { sqliteTable, text, integer, primaryKey } from 'drizzle-orm/sqlite-core';

export const achievement = sqliteTable('achievement', {
  id: text('id').primaryKey(),
  name: text('name').notNull(),
  description: text('description').notNull(),
  category: text('category').notNull(), // 'farming', 'gambling', 'social'
  
  // Requirements
  requirement: text('requirement', { mode: 'json' }).$type<{
    type: string;
    target: number;
    conditions?: Record<string, unknown>;
  }>(),
  
  // Rewards
  rewardCoins: integer('reward_coins').default(0),
  rewardExp: integer('reward_exp').default(0),
  rewardItem: text('reward_item'),
  
  // Display
  iconUrl: text('icon_url'),
  rarity: text('rarity').default('common'), // common, rare, epic, legendary
  hidden: integer('hidden', { mode: 'boolean' }).default(false),
});

export const playerAchievement = sqliteTable('player_achievement', {
  playerId: text('player_id').notNull().references(() => playerProfile.id),
  achievementId: text('achievement_id').notNull().references(() => achievement.id),
  
  progress: integer('progress').notNull().default(0),
  completed: integer('completed', { mode: 'boolean' }).notNull().default(false),
  completedAt: integer('completed_at', { mode: 'timestamp' }),
  claimed: integer('claimed', { mode: 'boolean' }).notNull().default(false),
}, (table) => ({
  pk: primaryKey({ columns: [table.playerId, table.achievementId] }),
}));

export const unlock = sqliteTable('player_unlock', {
  playerId: text('player_id').notNull().references(() => playerProfile.id),
  unlockType: text('unlock_type').notNull(), // 'simulin', 'table', 'cosmetic'
  unlockId: text('unlock_id').notNull(),
  unlockedAt: integer('unlocked_at', { mode: 'timestamp' }).notNull(),
}, (table) => ({
  pk: primaryKey({ columns: [table.playerId, table.unlockType, table.unlockId] }),
}));
```

### Leaderboards

```typescript
// schema/social.ts
import { sqliteTable, text, integer, index } from 'drizzle-orm/sqlite-core';

export const leaderboardEntry = sqliteTable('leaderboard_entry', {
  id: text('id').primaryKey(),
  playerId: text('player_id').notNull().references(() => playerProfile.id),
  
  boardType: text('board_type').notNull(),  // 'daily', 'weekly', 'alltime', 'season_1'
  period: text('period').notNull(),          // '2026-01-10', '2026-W02', 'alltime'
  
  score: integer('score').notNull(),
  rank: integer('rank'),                     // Computed/cached
  
  metadata: text('metadata', { mode: 'json' }).$type<{
    gamesPlayed?: number;
    bestCombo?: number;
    favoriteTable?: string;
  }>(),
  
  updatedAt: integer('updated_at', { mode: 'timestamp' }).notNull(),
}, (table) => ({
  scoreIdx: index('lb_score').on(table.boardType, table.period, table.score),
  playerIdx: index('lb_player').on(table.playerId, table.boardType),
}));
```

## Common Queries

### Get Player with Stats

```typescript
import { eq } from 'drizzle-orm';

async function getPlayerWithStats(userId: string) {
  return db.query.playerProfile.findFirst({
    where: eq(playerProfile.userId, userId),
    with: {
      currencies: true,
      achievements: {
        where: eq(playerAchievement.completed, true),
      },
    },
  });
}
```

### Update Currency (Transaction)

```typescript
async function addCurrency(
  playerId: string, 
  type: string, 
  amount: number
) {
  return db.transaction(async (tx) => {
    const current = await tx.query.playerCurrency.findFirst({
      where: and(
        eq(playerCurrency.playerId, playerId),
        eq(playerCurrency.currencyType, type)
      ),
    });
    
    if (current) {
      await tx.update(playerCurrency)
        .set({ 
          amount: current.amount + amount,
          lifetimeEarned: amount > 0 
            ? current.lifetimeEarned + amount 
            : current.lifetimeEarned,
          updatedAt: new Date(),
        })
        .where(and(
          eq(playerCurrency.playerId, playerId),
          eq(playerCurrency.currencyType, type)
        ));
    } else {
      await tx.insert(playerCurrency).values({
        playerId,
        currencyType: type,
        amount: Math.max(0, amount),
        lifetimeEarned: Math.max(0, amount),
        updatedAt: new Date(),
      });
    }
  });
}
```

### Leaderboard Query

```typescript
async function getLeaderboard(
  boardType: string, 
  period: string, 
  limit = 100
) {
  return db.select({
    rank: leaderboardEntry.rank,
    score: leaderboardEntry.score,
    player: {
      id: playerProfile.id,
      displayName: playerProfile.displayName,
      avatarUrl: playerProfile.avatarUrl,
      level: playerProfile.level,
    },
  })
  .from(leaderboardEntry)
  .innerJoin(playerProfile, eq(leaderboardEntry.playerId, playerProfile.id))
  .where(and(
    eq(leaderboardEntry.boardType, boardType),
    eq(leaderboardEntry.period, period)
  ))
  .orderBy(desc(leaderboardEntry.score))
  .limit(limit);
}
```

### Save Game State

```typescript
async function saveGameState(
  sessionId: string, 
  gameState: GameState
) {
  await db.update(gameSession)
    .set({
      gameState: {
        time: gameState.time,
        resources: gameState.resources,
        hexes: Object.fromEntries(gameState.hexes),
        troubles: gameState.troubles,
        score: gameState.score,
      },
      lastSavedAt: new Date(),
      playDuration: sql`play_duration + ${AUTOSAVE_INTERVAL}`,
    })
    .where(eq(gameSession.id, sessionId));
}
```

## Migration Workflow

```bash
# Generate migration from schema changes
bun run db:generate

# Apply migrations to database
bun run db:migrate

# Push schema directly (dev only)
bun run db:push

# Open Drizzle Studio
bun run db:studio
```

## Performance Tips

1. **Index frequently filtered columns**: playerId, timestamps, scores
2. **Use JSON columns sparingly**: Good for flexible data, bad for querying
3. **Batch inserts**: Use `insert().values([...])` for bulk operations
4. **Denormalize carefully**: Store computed ranks, not just scores
5. **Archive old data**: Move completed sessions to archive tables
