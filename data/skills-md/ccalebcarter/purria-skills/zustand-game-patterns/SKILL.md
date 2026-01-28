---
name: zustand-game-patterns
description: Zustand state management patterns optimized for games including persistence, undo/redo, time-travel debugging, subscriptions, and performance optimization. Use when designing game state architecture, implementing save/load, optimizing re-renders, or debugging state issues. Triggers on requests involving Zustand stores, game state management, state persistence, or React performance in games.
---

# Zustand Game Patterns

Production-ready patterns for managing complex game state with Zustand.

## Store Architecture

### Modular Store Pattern

Split large game state into focused slices:

```typescript
// stores/slices/timeSlice.ts
import { StateCreator } from 'zustand';
import { GameState } from '../types';

export interface TimeSlice {
  time: GameTime;
  advancePhase: () => void;
  setDay: (day: number) => void;
}

export const createTimeSlice: StateCreator<
  GameState,
  [['zustand/immer', never]],
  [],
  TimeSlice
> = (set) => ({
  time: { season: 1, day: 1, phase: 'morning' },
  
  advancePhase: () => set((state) => {
    const phases = ['morning', 'action', 'resolution', 'night'];
    const idx = phases.indexOf(state.time.phase);
    state.time.phase = phases[(idx + 1) % 4];
    if (idx === 3) state.time.day = Math.min(state.time.day + 1, 42);
  }),
  
  setDay: (day) => set((state) => {
    state.time.day = Math.max(1, Math.min(day, 42));
  }),
});
```

### Combining Slices

```typescript
// stores/gameStore.ts
import { create } from 'zustand';
import { immer } from 'zustand/middleware/immer';
import { subscribeWithSelector } from 'zustand/middleware';
import { createTimeSlice, TimeSlice } from './slices/timeSlice';
import { createResourceSlice, ResourceSlice } from './slices/resourceSlice';
import { createHexSlice, HexSlice } from './slices/hexSlice';

type GameState = TimeSlice & ResourceSlice & HexSlice;

export const useGameStore = create<GameState>()(
  subscribeWithSelector(
    immer((...args) => ({
      ...createTimeSlice(...args),
      ...createResourceSlice(...args),
      ...createHexSlice(...args),
    }))
  )
);
```

## Persistence

### Local Storage Save/Load

```typescript
import { persist, createJSONStorage } from 'zustand/middleware';

export const useGameStore = create<GameState>()(
  persist(
    subscribeWithSelector(
      immer((set, get) => ({
        // ... state and actions
      }))
    ),
    {
      name: 'game-save',
      storage: createJSONStorage(() => localStorage),
      
      // Only persist specific fields
      partialize: (state) => ({
        time: state.time,
        resources: state.resources,
        score: state.score,
        // Exclude transient state like selectedHex
      }),
      
      // Handle version migrations
      version: 1,
      migrate: (persisted, version) => {
        if (version === 0) {
          // Migration from v0 to v1
          return { ...persisted, newField: 'default' };
        }
        return persisted;
      },
    }
  )
);
```

### Multiple Save Slots

```typescript
interface SaveSlot {
  id: string;
  name: string;
  timestamp: number;
  data: Partial<GameState>;
}

const SAVE_SLOTS_KEY = 'game-saves';

export const saveToSlot = (slotId: string, name: string) => {
  const state = useGameStore.getState();
  const saves = JSON.parse(localStorage.getItem(SAVE_SLOTS_KEY) || '[]');
  
  const saveData: SaveSlot = {
    id: slotId,
    name,
    timestamp: Date.now(),
    data: {
      time: state.time,
      resources: state.resources,
      score: state.score,
      hexes: Object.fromEntries(state.hexes),
    },
  };
  
  const idx = saves.findIndex((s: SaveSlot) => s.id === slotId);
  if (idx >= 0) saves[idx] = saveData;
  else saves.push(saveData);
  
  localStorage.setItem(SAVE_SLOTS_KEY, JSON.stringify(saves));
};

export const loadFromSlot = (slotId: string) => {
  const saves = JSON.parse(localStorage.getItem(SAVE_SLOTS_KEY) || '[]');
  const slot = saves.find((s: SaveSlot) => s.id === slotId);
  
  if (slot) {
    useGameStore.setState({
      ...slot.data,
      hexes: new Map(Object.entries(slot.data.hexes || {})),
    });
  }
};
```

## Undo/Redo (Time Travel)

```typescript
import { temporal } from 'zundo';

export const useGameStore = create<GameState>()(
  temporal(
    immer((set) => ({
      // ... state and actions
    })),
    {
      // Limit history size
      limit: 50,
      
      // Only track specific changes
      partialize: (state) => ({
        hexes: state.hexes,
        resources: state.resources,
      }),
      
      // Equality check to prevent duplicate history
      equality: (a, b) => JSON.stringify(a) === JSON.stringify(b),
    }
  )
);

// Usage
const { undo, redo, pastStates, futureStates } = useGameStore.temporal.getState();
```

## Subscriptions & Side Effects

### Subscribe to State Changes

```typescript
// Subscribe outside React
const unsubscribe = useGameStore.subscribe(
  (state) => state.time.phase,
  (phase, prevPhase) => {
    console.log(`Phase changed: ${prevPhase} → ${phase}`);
    
    // Trigger side effects
    if (phase === 'morning') {
      useGameStore.getState().spawnTrouble();
    }
  }
);

// Subscribe to multiple selectors
useGameStore.subscribe(
  (state) => ({ day: state.time.day, phase: state.time.phase }),
  ({ day, phase }) => {
    // Analytics tracking
    analytics.track('game_progress', { day, phase });
  },
  { equalityFn: shallow }
);
```

### React Subscription Hook

```typescript
import { useEffect } from 'react';
import { useShallow } from 'zustand/react/shallow';

// Optimized selector with shallow comparison
export const useGameTime = () => useGameStore(
  useShallow((state) => ({
    day: state.time.day,
    phase: state.time.phase,
    season: state.time.season,
  }))
);

// Effect on state change
export const usePhaseEffects = () => {
  const phase = useGameStore((s) => s.time.phase);
  
  useEffect(() => {
    if (phase === 'resolution') {
      // Play resolution animation
      playSound('phase_change');
    }
  }, [phase]);
};
```

## Performance Optimization

### Selector Memoization

```typescript
// ❌ Bad: Creates new object every render
const { time, resources } = useGameStore((state) => ({
  time: state.time,
  resources: state.resources,
}));

// ✅ Good: Use shallow comparison
import { useShallow } from 'zustand/react/shallow';

const { time, resources } = useGameStore(
  useShallow((state) => ({
    time: state.time,
    resources: state.resources,
  }))
);

// ✅ Best: Separate selectors for independent updates
const time = useGameStore((s) => s.time);
const resources = useGameStore((s) => s.resources);
```

### Computed Selectors

```typescript
// Create memoized selectors for derived state
import { createSelector } from 'reselect';

const selectTroubles = (state: GameState) => state.troubles;
const selectGridSize = (state: GameState) => state.gridSize;

export const selectTroubleCount = createSelector(
  [selectTroubles],
  (troubles) => Object.keys(troubles).length
);

export const selectTotalTroubleHexes = createSelector(
  [selectTroubles],
  (troubles) => Object.values(troubles)
    .reduce((sum, t) => sum + t.hexCoords.length, 0)
);

// Usage
const troubleCount = useGameStore(selectTroubleCount);
```

### Batched Updates

```typescript
// Batch multiple state changes
const endDay = () => {
  useGameStore.setState((state) => {
    // All updates in single render
    state.metaPots.activeBets = [];
    state.time.phase = 'morning';
    state.time.day += 1;
    state.resources.stamina = 100;
  });
};
```

## Devtools Integration

```typescript
import { devtools } from 'zustand/middleware';

export const useGameStore = create<GameState>()(
  devtools(
    subscribeWithSelector(
      immer((set) => ({
        // ... state and actions
        
        // Named actions for devtools
        advancePhase: () => set(
          (state) => { /* ... */ },
          false,
          'time/advancePhase' // Action name in devtools
        ),
      }))
    ),
    {
      name: 'GameStore',
      enabled: process.env.NODE_ENV === 'development',
    }
  )
);
```

## Testing Patterns

```typescript
// Reset store between tests
beforeEach(() => {
  useGameStore.setState({
    time: { season: 1, day: 1, phase: 'morning' },
    resources: { tulipBulbs: 10, coins: 3000, stamina: 100 },
    // ... initial state
  });
});

// Test actions
test('advancePhase cycles through phases', () => {
  const { advancePhase } = useGameStore.getState();
  
  expect(useGameStore.getState().time.phase).toBe('morning');
  advancePhase();
  expect(useGameStore.getState().time.phase).toBe('action');
  advancePhase();
  expect(useGameStore.getState().time.phase).toBe('resolution');
});

// Test subscriptions
test('spawns trouble on morning phase', () => {
  const spawnTrouble = vi.spyOn(useGameStore.getState(), 'spawnTrouble');
  
  // Advance to morning
  useGameStore.setState({ time: { ...initialTime, phase: 'night' } });
  useGameStore.getState().advancePhase();
  
  expect(spawnTrouble).toHaveBeenCalled();
});
```
