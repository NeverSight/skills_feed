---
name: svelte
description: Modern Svelte development for reactive web apps. Use when building Svelte components, managing state with stores, implementing real-time updates via WebSocket, or migrating from vanilla JS. Covers SvelteKit, TypeScript, and integration with Node.js backends.
---

# Svelte Skill

## Overview

This skill provides expertise for building reactive web applications with Svelte. It covers component architecture, the reactivity system, stores for state management, real-time updates with WebSockets, and SvelteKit for full-stack applications.

## Why Svelte

### Comparison with Vanilla JS

| Aspect | Vanilla JS | Svelte |
|--------|------------|--------|
| Reactivity | Manual DOM updates | Automatic - `count++` just works |
| Components | Template strings | Single-file components |
| State | Global variables | Stores with subscriptions |
| Bundle size | 0kb (but more code) | ~2kb runtime |
| Learning curve | None | Gentle (closest to vanilla) |

### Key Benefits

1. **Compile-time magic** - No virtual DOM, compiles to efficient vanilla JS
2. **Less boilerplate** - `let count = 0` is reactive by default
3. **Built-in transitions** - `transition:fade` for animations
4. **Scoped CSS** - Styles in components don't leak
5. **Stores** - Simple reactive state that works with WebSockets

## Core Concepts

### Reactivity

Svelte's reactivity is based on assignments:

```svelte
<script>
  let count = 0;

  // Reactive statements run when dependencies change
  $: doubled = count * 2;
  $: console.log('count changed to', count);

  function increment() {
    count++;  // This triggers UI update automatically
  }
</script>

<button on:click={increment}>
  Count: {count} (doubled: {doubled})
</button>
```

### Array/Object Reactivity

Svelte tracks assignments, not mutations:

```svelte
<script>
  let items = ['a', 'b', 'c'];

  // BAD: mutation doesn't trigger update
  function addBad() {
    items.push('d');  // UI won't update!
  }

  // GOOD: reassignment triggers update
  function addGood() {
    items = [...items, 'd'];  // UI updates
  }

  // Also works: assign back to self
  function addAlso() {
    items.push('d');
    items = items;  // Triggers update
  }
</script>
```

### Component Structure

Single-file components with script, markup, and style:

```svelte
<!-- PlayerCard.svelte -->
<script>
  // Props with defaults
  export let name;
  export let cash = 0;
  export let isActive = false;

  // Local state
  let expanded = false;

  // Event dispatcher
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();

  function handleClick() {
    dispatch('select', { name });
  }
</script>

<div class="player-card" class:active={isActive} on:click={handleClick}>
  <h3>{name}</h3>
  <p>Cash: £{cash}</p>

  {#if expanded}
    <slot />  <!-- Nested content goes here -->
  {/if}
</div>

<style>
  /* Scoped to this component only */
  .player-card {
    padding: 1rem;
    border: 2px solid #333;
    border-radius: 8px;
  }

  .player-card.active {
    border-color: #4a9eff;
    background: rgba(74, 158, 255, 0.1);
  }
</style>
```

### Using Components

```svelte
<!-- Game.svelte -->
<script>
  import PlayerCard from './PlayerCard.svelte';

  let players = [
    { id: 1, name: 'Germany', cash: 15 },
    { id: 2, name: 'Britain', cash: 12 }
  ];
  let activePlayerId = 1;

  function handleSelect(event) {
    console.log('Selected:', event.detail.name);
  }
</script>

{#each players as player (player.id)}
  <PlayerCard
    name={player.name}
    cash={player.cash}
    isActive={player.id === activePlayerId}
    on:select={handleSelect}
  >
    <p>Ships: {player.ships?.length ?? 0}</p>
  </PlayerCard>
{/each}
```

## Stores

### Writable Stores

For shared state across components:

```javascript
// stores/gameState.js
import { writable, derived } from 'svelte/store';

// Create a writable store
export const gameState = writable(null);

// Derived stores compute from other stores
export const currentPlayer = derived(
  gameState,
  $state => $state?.players?.[$state?.currentPlayerIndex]
);

export const isMyTurn = derived(
  [gameState, currentPlayer],
  ([$state, $player]) => $player?.id === myPlayerId
);

// Helper functions to update state
export function updateGameState(newState) {
  gameState.set(newState);
}

export function updatePlayer(playerId, changes) {
  gameState.update(state => ({
    ...state,
    players: {
      ...state.players,
      [playerId]: { ...state.players[playerId], ...changes }
    }
  }));
}
```

### Using Stores in Components

```svelte
<script>
  import { gameState, currentPlayer, isMyTurn } from './stores/gameState.js';

  // $ prefix auto-subscribes to store
  $: console.log('Game state updated:', $gameState);
</script>

<div>
  <h2>Turn: {$gameState?.turn}</h2>
  <p>Current player: {$currentPlayer?.name}</p>

  {#if $isMyTurn}
    <button>Take Action</button>
  {:else}
    <p>Waiting for {$currentPlayer?.name}...</p>
  {/if}
</div>
```

### Custom Stores

Create stores with custom methods:

```javascript
// stores/player.js
import { writable } from 'svelte/store';

function createPlayerStore() {
  const { subscribe, set, update } = writable({
    cash: 0,
    officers: 0,
    engineers: 0,
    gasCubes: { hydrogen: 0, helium: 0 }
  });

  return {
    subscribe,
    set,
    reset: () => set({ cash: 0, officers: 0, engineers: 0, gasCubes: { hydrogen: 0, helium: 0 } }),
    addCash: (amount) => update(p => ({ ...p, cash: p.cash + amount })),
    spendCash: (amount) => update(p => ({ ...p, cash: p.cash - amount })),
    buyGas: (type, amount) => update(p => ({
      ...p,
      gasCubes: { ...p.gasCubes, [type]: p.gasCubes[type] + amount }
    }))
  };
}

export const player = createPlayerStore();
```

## Real-Time Updates with WebSocket

### Socket Store Pattern

```javascript
// stores/socket.js
import { writable, get } from 'svelte/store';
import { io } from 'socket.io-client';
import { gameState } from './gameState.js';

export const connected = writable(false);
export const connectionError = writable(null);

let socket = null;

export function connect(serverUrl) {
  socket = io(serverUrl, {
    reconnection: true,
    reconnectionAttempts: 10,
    reconnectionDelay: 1000
  });

  socket.on('connect', () => {
    connected.set(true);
    connectionError.set(null);
    console.log('Connected to server');
  });

  socket.on('disconnect', () => {
    connected.set(false);
  });

  socket.on('connect_error', (error) => {
    connectionError.set(error.message);
  });

  // Game state updates from server
  socket.on('state-update', (newState) => {
    gameState.set(newState);
  });

  socket.on('state-sync', (fullState) => {
    gameState.set(fullState);
  });

  return socket;
}

export function joinGame(gameId, playerId) {
  if (socket) {
    socket.emit('join-game', { gameId, playerId });
  }
}

export function sendAction(action) {
  if (socket) {
    socket.emit('game-action', action);
  }
}

export function disconnect() {
  if (socket) {
    socket.disconnect();
    socket = null;
    connected.set(false);
  }
}
```

### Using Socket in Components

```svelte
<!-- Game.svelte -->
<script>
  import { onMount, onDestroy } from 'svelte';
  import { connect, joinGame, sendAction, disconnect, connected } from './stores/socket.js';
  import { gameState, currentPlayer } from './stores/gameState.js';

  export let gameId;
  export let playerId;

  onMount(() => {
    connect('http://localhost:3000');
    joinGame(gameId, playerId);
  });

  onDestroy(() => {
    disconnect();
  });

  function handleEndTurn() {
    sendAction({ type: 'END_TURN' });
  }
</script>

{#if !$connected}
  <div class="connecting">Connecting to server...</div>
{:else if !$gameState}
  <div class="loading">Loading game state...</div>
{:else}
  <div class="game">
    <h1>Turn {$gameState.turn}</h1>
    <p>Current player: {$currentPlayer?.name}</p>

    <button on:click={handleEndTurn}>End Turn</button>
  </div>
{/if}
```

## Conditional Rendering and Loops

### If/Else Blocks

```svelte
{#if loading}
  <Spinner />
{:else if error}
  <ErrorMessage {error} />
{:else if items.length === 0}
  <EmptyState />
{:else}
  <ItemList {items} />
{/if}
```

### Each Blocks with Keys

```svelte
<!-- Key is crucial for list updates -->
{#each ships as ship (ship.id)}
  <Ship {...ship} on:launch={handleLaunch} />
{:else}
  <p>No ships in hangar</p>
{/each}
```

### Await Blocks

```svelte
{#await fetchGameState()}
  <p>Loading...</p>
{:then state}
  <GameBoard {state} />
{:catch error}
  <p>Error: {error.message}</p>
{/await}
```

## Transitions and Animations

### Built-in Transitions

```svelte
<script>
  import { fade, fly, slide, scale } from 'svelte/transition';
  import { flip } from 'svelte/animate';

  let visible = true;
  let items = [];
</script>

{#if visible}
  <div transition:fade={{ duration: 300 }}>
    Fades in and out
  </div>
{/if}

<!-- One-way transitions -->
{#if showNotification}
  <div in:fly={{ y: -50, duration: 300 }} out:fade>
    Notification!
  </div>
{/if}

<!-- Animate list reordering -->
{#each items as item (item.id)}
  <div animate:flip={{ duration: 300 }}>
    {item.name}
  </div>
{/each}
```

### Custom Transitions

```svelte
<script>
  function whoosh(node, { duration = 400 }) {
    return {
      duration,
      css: (t) => {
        const eased = t;  // Could use easing function
        return `
          transform: scale(${eased}) rotate(${(1 - eased) * 360}deg);
          opacity: ${eased};
        `;
      }
    };
  }
</script>

{#if show}
  <div transition:whoosh>Whoooosh!</div>
{/if}
```

## Event Handling

### DOM Events

```svelte
<button on:click={handleClick}>Click</button>
<button on:click={() => count++}>Inline</button>

<!-- Event modifiers -->
<button on:click|preventDefault={submit}>Submit</button>
<button on:click|stopPropagation={handleClick}>Stop Bubble</button>
<button on:click|once={init}>Initialize Once</button>
<form on:submit|preventDefault={handleSubmit}>...</form>

<!-- Keyboard events -->
<input on:keydown|self={(e) => e.key === 'Enter' && submit()} />
```

### Component Events

```svelte
<!-- Child component -->
<script>
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();

  function handleSelect() {
    dispatch('select', { id: item.id, name: item.name });
  }
</script>

<!-- Parent component -->
<Card on:select={(e) => console.log(e.detail.name)} />

<!-- Forward DOM events -->
<button on:click>
  This click bubbles to parent
</button>
```

## Bindings

### Two-Way Binding

```svelte
<script>
  let name = '';
  let agreed = false;
  let selected = 'a';
  let quantity = 1;
</script>

<input bind:value={name} />
<input type="checkbox" bind:checked={agreed} />
<input type="number" bind:value={quantity} min="1" max="10" />

<select bind:value={selected}>
  <option value="a">Option A</option>
  <option value="b">Option B</option>
</select>

<!-- Group binding -->
<script>
  let selectedColors = [];
</script>
{#each ['red', 'green', 'blue'] as color}
  <label>
    <input type="checkbox" bind:group={selectedColors} value={color} />
    {color}
  </label>
{/each}
```

### Element Bindings

```svelte
<script>
  let inputElement;
  let divWidth;
  let divHeight;
</script>

<input bind:this={inputElement} />
<button on:click={() => inputElement.focus()}>Focus</button>

<div bind:clientWidth={divWidth} bind:clientHeight={divHeight}>
  Size: {divWidth}x{divHeight}
</div>
```

## SvelteKit

### Project Structure

```
my-app/
├── src/
│   ├── lib/           # Shared components and utilities
│   │   ├── components/
│   │   │   ├── PlayerCard.svelte
│   │   │   └── GameBoard.svelte
│   │   ├── stores/
│   │   │   ├── gameState.js
│   │   │   └── socket.js
│   │   └── utils/
│   ├── routes/        # File-based routing
│   │   ├── +page.svelte       # /
│   │   ├── +layout.svelte     # Shared layout
│   │   ├── game/
│   │   │   ├── +page.svelte   # /game
│   │   │   └── [id]/
│   │   │       └── +page.svelte  # /game/:id
│   │   └── api/       # API routes
│   │       └── games/
│   │           └── +server.js
│   ├── app.html
│   └── app.css
├── static/            # Static assets
├── svelte.config.js
└── package.json
```

### Page Load Functions

```javascript
// routes/game/[id]/+page.js
export async function load({ params, fetch }) {
  const response = await fetch(`/api/games/${params.id}`);

  if (!response.ok) {
    throw error(404, 'Game not found');
  }

  const game = await response.json();

  return {
    game,
    gameId: params.id
  };
}
```

```svelte
<!-- routes/game/[id]/+page.svelte -->
<script>
  export let data;  // From load function

  $: ({ game, gameId } = data);
</script>

<h1>Game: {game.name}</h1>
```

### API Routes

```javascript
// routes/api/games/+server.js
import { json } from '@sveltejs/kit';

export async function GET({ url }) {
  const games = await db.getGames();
  return json(games);
}

export async function POST({ request }) {
  const { name, playerId } = await request.json();
  const game = await db.createGame(name, playerId);
  return json(game, { status: 201 });
}
```

## TypeScript Support

```svelte
<script lang="ts">
  interface Player {
    id: string;
    name: string;
    cash: number;
    faction: 'germany' | 'britain' | 'usa' | 'italy';
  }

  interface Ship {
    id: string;
    name: string;
    status: 'hangar' | 'on_route' | 'destroyed';
  }

  export let player: Player;
  export let ships: Ship[] = [];

  let selectedShip: Ship | null = null;

  function selectShip(ship: Ship): void {
    selectedShip = ship;
  }
</script>
```

## Migration from Vanilla JS

### Before (Vanilla)

```javascript
// Vanilla JS pattern
let gameState = null;
const stateElement = document.getElementById('game-state');

function render() {
  stateElement.innerHTML = `
    <h2>Turn ${gameState.turn}</h2>
    <p>Cash: £${gameState.players[userId].cash}</p>
    ${gameState.players[userId].ships.map(ship => `
      <div class="ship">${ship.name}</div>
    `).join('')}
  `;
}

async function fetchState() {
  const res = await fetch(`/api/state/${gameId}`);
  gameState = await res.json();
  render();
}

// Poll every 2 seconds
setInterval(fetchState, 2000);
```

### After (Svelte)

```svelte
<script>
  import { onMount } from 'svelte';
  import { gameState } from './stores/gameState.js';
  import { connect, joinGame } from './stores/socket.js';

  export let gameId;
  export let userId;

  $: player = $gameState?.players?.[userId];

  onMount(() => {
    connect('http://localhost:3000');
    joinGame(gameId, userId);
  });
</script>

{#if $gameState}
  <h2>Turn {$gameState.turn}</h2>
  <p>Cash: £{player.cash}</p>

  {#each player.ships as ship (ship.id)}
    <div class="ship">{ship.name}</div>
  {/each}
{:else}
  <p>Loading...</p>
{/if}
```

## Best Practices

### Component Organization

```
lib/components/
├── ui/               # Generic reusable components
│   ├── Button.svelte
│   ├── Modal.svelte
│   └── Tooltip.svelte
├── game/             # Game-specific components
│   ├── GameBoard.svelte
│   ├── PlayerPanel.svelte
│   └── ShipCard.svelte
└── layout/           # Layout components
    ├── Header.svelte
    └── Sidebar.svelte
```

### Props and Events Naming

```svelte
<script>
  // Props: noun or adjective
  export let player;
  export let isActive = false;
  export let maxItems = 10;

  // Events: on:verbNoun pattern
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();

  // dispatch('select'), dispatch('launch'), dispatch('close')
</script>

<!-- Usage follows same pattern -->
<ShipCard
  ship={myShip}
  isSelected={selectedId === myShip.id}
  on:launch={handleLaunch}
  on:select={handleSelect}
/>
```

### Reactive Statement Order

```svelte
<script>
  export let items;
  export let filter;

  // Derived values first (these update when deps change)
  $: filteredItems = items.filter(i => i.type === filter);
  $: totalCount = filteredItems.length;

  // Side effects last (log, dispatch events, etc.)
  $: if (totalCount === 0) {
    console.log('No items match filter');
  }
</script>
```

### Avoiding Common Mistakes

```svelte
<script>
  // MISTAKE 1: Mutating without reassignment
  let items = [1, 2, 3];
  items.push(4);  // Won't trigger update!
  items = [...items, 4];  // Correct

  // MISTAKE 2: Destructuring props loses reactivity
  export let player;
  const { name } = player;  // name won't update!
  $: ({ name } = player);   // Reactive destructure

  // MISTAKE 3: Not using key in each
  {#each items as item}  // Bad for updates
  {#each items as item (item.id)}  // Good

  // MISTAKE 4: Store in template without $
  import { count } from './stores';
  // {count} shows store object, not value
  // {$count} shows the value
</script>
```

## Testing Svelte Components

```javascript
// PlayerCard.test.js
import { render, fireEvent } from '@testing-library/svelte';
import PlayerCard from './PlayerCard.svelte';

describe('PlayerCard', () => {
  it('displays player name and cash', () => {
    const { getByText } = render(PlayerCard, {
      props: { name: 'Germany', cash: 15 }
    });

    expect(getByText('Germany')).toBeInTheDocument();
    expect(getByText('Cash: £15')).toBeInTheDocument();
  });

  it('dispatches select event on click', async () => {
    const { getByRole, component } = render(PlayerCard, {
      props: { name: 'Germany', cash: 15 }
    });

    const selectHandler = vi.fn();
    component.$on('select', selectHandler);

    await fireEvent.click(getByRole('button'));

    expect(selectHandler).toHaveBeenCalledWith(
      expect.objectContaining({
        detail: { name: 'Germany' }
      })
    );
  });
});
```

## When This Skill Activates

Use this skill when:
- Building Svelte components
- Managing state with Svelte stores
- Implementing real-time updates via WebSocket
- Migrating vanilla JS to Svelte
- Setting up SvelteKit projects
- Adding TypeScript to Svelte
- Creating reactive UI patterns
- Optimizing Svelte performance
