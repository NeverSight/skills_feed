---
name: game-state
description: Game state management for turn-based board games. Use when designing state structure, implementing game logic, validating actions, managing phases/turns, or handling complex game rules. Covers reducers, state machines, and undo/redo.
---

# Game State Management Skill

## Overview

This skill provides expertise for managing complex game state in digital board games. It covers state structure design, action validation, phase management, and patterns for implementing intricate game rules reliably.

## Core Principles

### Immutable State

Always treat game state as immutable. Create new state objects rather than mutating existing ones:

```javascript
// BAD: Mutating state
function addMoney(state, playerId, amount) {
  state.players[playerId].money += amount;
  return state;
}

// GOOD: Creating new state
function addMoney(state, playerId, amount) {
  return {
    ...state,
    players: {
      ...state.players,
      [playerId]: {
        ...state.players[playerId],
        money: state.players[playerId].money + amount
      }
    }
  };
}
```

### Single Source of Truth

All game state should live in one canonical object:

```javascript
const gameState = {
  // Metadata
  id: 'game-123',
  version: 42,
  phase: 'worker-placement',
  currentPlayer: 'player-1',
  turnNumber: 5,
  age: 2,

  // Player states
  players: {
    'player-1': { /* player state */ },
    'player-2': { /* player state */ }
  },

  // Shared state
  board: { /* board state */ },
  market: { /* market state */ },
  decks: { /* deck state */ }
};
```

## State Structure Design

### Normalize Nested Data

Avoid deeply nested structures. Use ID references instead:

```javascript
// BAD: Deeply nested
const state = {
  players: [{
    ships: [{
      upgrades: [{ type: 'engine', stats: {...} }]
    }]
  }]
};

// GOOD: Normalized with references
const state = {
  players: {
    'p1': { id: 'p1', shipIds: ['ship-1', 'ship-2'] }
  },
  ships: {
    'ship-1': { id: 'ship-1', ownerId: 'p1', upgradeIds: ['upg-1'] }
  },
  upgrades: {
    'upg-1': { id: 'upg-1', type: 'engine', stats: {...} }
  }
};
```

### Separate Derived State

Don't store computed values in state:

```javascript
// BAD: Storing computed values
const playerState = {
  money: 100,
  income: 15,
  totalMoney: 115  // Don't store this!
};

// GOOD: Compute when needed
function getTotalMoney(player) {
  return player.money + player.income;
}

// Or use selectors
const selectors = {
  totalLift: (state, playerId) => {
    const player = state.players[playerId];
    return player.gasCubes * 5;
  },
  canLaunch: (state, playerId) => {
    const lift = selectors.totalLift(state, playerId);
    const weight = selectors.totalWeight(state, playerId);
    return lift >= weight;
  }
};
```

## Action/Reducer Pattern

### Action Structure

```javascript
// Actions describe what happened
const action = {
  type: 'PLACE_WORKER',
  playerId: 'player-1',
  payload: {
    workerId: 'agent-1',
    locationId: 'construction-hall'
  }
};

// Action creators for consistency
const actions = {
  placeWorker: (playerId, workerId, locationId) => ({
    type: 'PLACE_WORKER',
    playerId,
    payload: { workerId, locationId }
  }),

  acquireTechnology: (playerId, techId, cost) => ({
    type: 'ACQUIRE_TECHNOLOGY',
    playerId,
    payload: { techId, cost }
  })
};
```

### Reducer Implementation

```javascript
function gameReducer(state, action) {
  switch (action.type) {
    case 'PLACE_WORKER':
      return placeWorkerReducer(state, action);

    case 'ACQUIRE_TECHNOLOGY':
      return acquireTechnologyReducer(state, action);

    case 'LAUNCH_SHIP':
      return launchShipReducer(state, action);

    default:
      return state;
  }
}

function placeWorkerReducer(state, action) {
  const { playerId, payload: { workerId, locationId } } = action;

  return {
    ...state,
    workers: {
      ...state.workers,
      [workerId]: {
        ...state.workers[workerId],
        locationId,
        available: false
      }
    },
    locations: {
      ...state.locations,
      [locationId]: {
        ...state.locations[locationId],
        workerIds: [...state.locations[locationId].workerIds, workerId]
      }
    }
  };
}
```

## Action Validation

### Validation Layer

Always validate before applying actions:

```javascript
function validateAction(state, action) {
  const validator = validators[action.type];
  if (!validator) {
    return { valid: false, reason: 'Unknown action type' };
  }
  return validator(state, action);
}

const validators = {
  PLACE_WORKER: (state, action) => {
    const { playerId, payload: { workerId, locationId } } = action;

    // Check it's player's turn
    if (state.currentPlayer !== playerId) {
      return { valid: false, reason: 'Not your turn' };
    }

    // Check worker belongs to player and is available
    const worker = state.workers[workerId];
    if (!worker || worker.ownerId !== playerId) {
      return { valid: false, reason: 'Invalid worker' };
    }
    if (!worker.available) {
      return { valid: false, reason: 'Worker already placed' };
    }

    // Check location exists and has space
    const location = state.locations[locationId];
    if (!location) {
      return { valid: false, reason: 'Invalid location' };
    }
    if (location.workerIds.length >= location.capacity) {
      return { valid: false, reason: 'Location is full' };
    }

    return { valid: true };
  }
};
```

### Process Action Flow

```javascript
async function processAction(gameId, playerId, action) {
  // 1. Load current state
  const state = await loadGameState(gameId);

  // 2. Validate
  const validation = validateAction(state, action);
  if (!validation.valid) {
    return { success: false, error: validation.reason };
  }

  // 3. Apply action
  let newState = gameReducer(state, action);

  // 4. Check for triggered effects
  newState = processTriggers(newState, action);

  // 5. Check for phase transitions
  newState = checkPhaseTransition(newState);

  // 6. Increment version
  newState = { ...newState, version: newState.version + 1 };

  // 7. Persist
  await saveGameState(gameId, newState);

  return { success: true, newState };
}
```

## Phase & Turn Management

### State Machine for Phases

```javascript
const phases = {
  SETUP: 'setup',
  WORKER_PLACEMENT: 'worker-placement',
  REVEAL: 'reveal',
  LAUNCH: 'launch',
  INCOME: 'income',
  CLEANUP: 'cleanup',
  AGE_TRANSITION: 'age-transition',
  GAME_END: 'game-end'
};

const phaseTransitions = {
  [phases.SETUP]: {
    next: phases.WORKER_PLACEMENT,
    canTransition: (state) => allPlayersReady(state)
  },
  [phases.WORKER_PLACEMENT]: {
    next: phases.REVEAL,
    canTransition: (state) => allWorkersPlaced(state)
  },
  [phases.REVEAL]: {
    next: phases.LAUNCH,
    canTransition: (state) => allCardsRevealed(state)
  },
  // ... etc
};

function checkPhaseTransition(state) {
  const currentPhase = phaseTransitions[state.phase];
  if (currentPhase && currentPhase.canTransition(state)) {
    return transitionToPhase(state, currentPhase.next);
  }
  return state;
}
```

### Turn Order Management

```javascript
function getNextPlayer(state) {
  const playerOrder = state.playerOrder;
  const currentIndex = playerOrder.indexOf(state.currentPlayer);
  const nextIndex = (currentIndex + 1) % playerOrder.length;
  return playerOrder[nextIndex];
}

function advanceTurn(state) {
  const nextPlayer = getNextPlayer(state);
  const isNewRound = nextPlayer === state.playerOrder[0];

  return {
    ...state,
    currentPlayer: nextPlayer,
    turnNumber: isNewRound ? state.turnNumber + 1 : state.turnNumber
  };
}
```

## Complex Game Logic

### Calculating Ship Stats

```javascript
function calculateShipStats(state, playerId) {
  const player = state.players[playerId];
  const blueprint = state.blueprints[player.blueprintId];

  // Start with baseline stats
  let stats = { ...blueprint.baselineStats };

  // Add stats from installed upgrades
  for (const slotId of blueprint.slotIds) {
    const slot = state.slots[slotId];
    if (slot.upgradeId) {
      const upgrade = state.upgrades[slot.upgradeId];
      stats = mergeStats(stats, upgrade.stats);
    }
  }

  // Calculate lift from gas cubes
  const gasCubes = countGasCubes(state, playerId);
  stats.lift = gasCubes * 5;

  return stats;
}

function canLaunch(state, playerId) {
  const stats = calculateShipStats(state, playerId);

  // Physics check: Lift >= Weight
  if (stats.lift < stats.weight) {
    return { can: false, reason: 'Insufficient lift' };
  }

  // Must have pilot
  const player = state.players[playerId];
  if (player.pilots < 1) {
    return { can: false, reason: 'No pilot available' };
  }

  // Must have ship in hangar
  if (player.launchHangar.length === 0) {
    return { can: false, reason: 'No ships in hangar' };
  }

  return { can: true };
}
```

### Hazard Check Resolution

```javascript
function resolveHazardCheck(state, playerId, hazardCard) {
  const shipStats = calculateShipStats(state, playerId);
  const results = [];

  for (const check of hazardCard.checks) {
    const playerValue = shipStats[check.stat];
    const passed = playerValue >= check.difficulty;

    results.push({
      stat: check.stat,
      required: check.difficulty,
      actual: playerValue,
      passed
    });
  }

  const allPassed = results.every(r => r.passed);

  return {
    hazardCard,
    results,
    outcome: allPassed ? 'success' : hazardCard.failureEffect
  };
}
```

## Undo/Redo Support

### Action History

```javascript
const gameWithHistory = {
  ...gameState,
  history: {
    past: [],      // Previous states
    future: []     // States after undo (for redo)
  }
};

function applyActionWithHistory(state, action) {
  // Save current state to history
  const newPast = [...state.history.past, state];

  // Apply action
  const newState = gameReducer(state, action);

  return {
    ...newState,
    history: {
      past: newPast,
      future: [] // Clear redo stack on new action
    }
  };
}

function undo(state) {
  if (state.history.past.length === 0) return state;

  const previous = state.history.past[state.history.past.length - 1];
  const newPast = state.history.past.slice(0, -1);

  return {
    ...previous,
    history: {
      past: newPast,
      future: [state, ...state.history.future]
    }
  };
}
```

## Testing Game Logic

### Unit Testing Reducers

```javascript
describe('placeWorkerReducer', () => {
  it('should place worker at location', () => {
    const state = createTestState();
    const action = actions.placeWorker('p1', 'worker-1', 'location-a');

    const newState = gameReducer(state, action);

    expect(newState.workers['worker-1'].locationId).toBe('location-a');
    expect(newState.locations['location-a'].workerIds).toContain('worker-1');
  });

  it('should not mutate original state', () => {
    const state = createTestState();
    const original = JSON.stringify(state);
    const action = actions.placeWorker('p1', 'worker-1', 'location-a');

    gameReducer(state, action);

    expect(JSON.stringify(state)).toBe(original);
  });
});
```

### Integration Testing Game Flow

```javascript
describe('full game round', () => {
  it('should complete worker placement phase', () => {
    let state = createGameState({ playerCount: 2 });

    // Each player places 3 workers
    for (let i = 0; i < 6; i++) {
      const playerId = state.currentPlayer;
      const worker = getAvailableWorker(state, playerId);
      const location = getValidLocation(state);

      state = processAction(state, actions.placeWorker(
        playerId, worker.id, location.id
      ));
    }

    expect(state.phase).toBe('reveal');
  });
});
```

## When This Skill Activates

Use this skill when:
- Designing game state structure
- Implementing action/reducer logic
- Building validation for game rules
- Managing phase and turn transitions
- Calculating derived game values
- Implementing undo/redo
- Testing game logic
