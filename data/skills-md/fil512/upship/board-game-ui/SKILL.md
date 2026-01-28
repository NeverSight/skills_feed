---
name: board-game-ui
description: UI/UX design for digital board games. Use when building game interfaces, implementing drag-and-drop, rendering game boards, showing player information, handling animations, or designing responsive layouts. Covers Canvas, SVG, and DOM-based approaches.
---

# Board Game UI Skill

## Overview

This skill provides expertise for building user interfaces for digital board games. It covers rendering approaches (DOM, Canvas, SVG), interaction patterns (drag-and-drop, click-to-select), responsive design for different screen sizes, and UX principles specific to turn-based games.

## Rendering Approaches

### When to Use Each

| Approach | Best For | Avoid When |
|----------|----------|------------|
| **DOM/CSS** | Card games, simple boards, UI overlays | Many moving pieces, complex animations |
| **SVG** | Maps, vector graphics, zoomable boards | Thousands of elements, pixel effects |
| **Canvas** | Complex animations, particles, real-time | Accessibility needed, text-heavy |
| **Hybrid** | Most board games | Over-engineering simple games |

### Recommended: Hybrid Approach

Use DOM for UI chrome (menus, player info, cards) and Canvas/SVG for the game board:

```html
<div class="game-container">
  <!-- DOM: Player info, always visible -->
  <aside class="player-panel">
    <div class="player-info" data-player="1">...</div>
  </aside>

  <!-- SVG: The game board/map -->
  <main class="board-area">
    <svg id="game-board" viewBox="0 0 1000 800">
      <!-- Routes, cities, tokens -->
    </svg>
  </main>

  <!-- DOM: Action buttons, cards in hand -->
  <footer class="action-bar">
    <div class="hand-cards">...</div>
    <div class="action-buttons">...</div>
  </footer>
</div>
```

## Layout Patterns

### Responsive Game Layout

```css
.game-container {
  display: grid;
  height: 100vh;
  gap: 1rem;
  padding: 1rem;

  /* Desktop: sidebar layout */
  grid-template-columns: 250px 1fr;
  grid-template-rows: 1fr auto;
  grid-template-areas:
    "sidebar board"
    "sidebar actions";
}

/* Tablet: stack sidebar above */
@media (max-width: 1024px) {
  .game-container {
    grid-template-columns: 1fr;
    grid-template-rows: auto 1fr auto;
    grid-template-areas:
      "sidebar"
      "board"
      "actions";
  }

  .player-panel {
    display: flex;
    overflow-x: auto;
  }
}

/* Mobile: minimal chrome */
@media (max-width: 600px) {
  .game-container {
    padding: 0.5rem;
    gap: 0.5rem;
  }

  .player-panel {
    font-size: 0.875rem;
  }
}
```

### Aspect Ratio Preservation

```css
.board-area {
  grid-area: board;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

#game-board {
  max-width: 100%;
  max-height: 100%;
  aspect-ratio: 5 / 4;  /* Match your board dimensions */
}
```

## SVG Game Board

### Board Structure

```html
<svg id="game-board" viewBox="0 0 1000 800">
  <!-- Background layer -->
  <g id="background">
    <image href="/assets/map-age-1.jpg" width="1000" height="800" />
  </g>

  <!-- Routes layer -->
  <g id="routes">
    <path class="route" data-route-id="london-paris"
          d="M 200,150 Q 250,200 350,180"
          stroke="#666" stroke-width="8" fill="none" />
  </g>

  <!-- Cities layer -->
  <g id="cities">
    <g class="city" data-city-id="london" transform="translate(200, 150)">
      <circle r="20" fill="#333" />
      <text y="35" text-anchor="middle">London</text>
    </g>
  </g>

  <!-- Tokens layer (on top) -->
  <g id="tokens">
    <g class="ship-token" data-player="1" data-ship-id="ship-1"
       transform="translate(200, 150)">
      <use href="#airship-icon" fill="var(--player-1-color)" />
    </g>
  </g>

  <!-- Definitions -->
  <defs>
    <symbol id="airship-icon" viewBox="0 0 40 20">
      <ellipse cx="20" cy="10" rx="18" ry="8" />
      <rect x="8" y="14" width="24" height="4" rx="2" />
    </symbol>
  </defs>
</svg>
```

### Interactive Elements

```javascript
// Click handling on SVG elements
document.getElementById('game-board').addEventListener('click', (e) => {
  const route = e.target.closest('.route');
  const city = e.target.closest('.city');
  const token = e.target.closest('.ship-token');

  if (route) {
    handleRouteClick(route.dataset.routeId);
  } else if (city) {
    handleCityClick(city.dataset.cityId);
  } else if (token) {
    handleTokenClick(token.dataset.shipId);
  }
});

// Hover effects
function setupHoverEffects() {
  document.querySelectorAll('.route').forEach(route => {
    route.addEventListener('mouseenter', () => {
      route.classList.add('highlighted');
      showRouteTooltip(route.dataset.routeId);
    });
    route.addEventListener('mouseleave', () => {
      route.classList.remove('highlighted');
      hideTooltip();
    });
  });
}
```

```css
/* SVG hover/selection states */
.route {
  cursor: pointer;
  transition: stroke 0.2s, stroke-width 0.2s;
}

.route:hover,
.route.highlighted {
  stroke: #4a9eff;
  stroke-width: 12;
}

.route.claimed {
  stroke: var(--claiming-player-color);
}

.route.unavailable {
  opacity: 0.3;
  pointer-events: none;
}

.city:hover circle {
  fill: #555;
  transform: scale(1.1);
}
```

## Drag and Drop

### HTML5 Drag and Drop (for cards/tiles)

```javascript
// Make elements draggable
function setupDraggable(element, type, id) {
  element.draggable = true;

  element.addEventListener('dragstart', (e) => {
    e.dataTransfer.setData('application/json', JSON.stringify({ type, id }));
    e.dataTransfer.effectAllowed = 'move';
    element.classList.add('dragging');
  });

  element.addEventListener('dragend', () => {
    element.classList.remove('dragging');
    clearDropTargets();
  });
}

// Make slots accept drops
function setupDropTarget(element, acceptTypes, onDrop) {
  element.addEventListener('dragover', (e) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    element.classList.add('drop-target');
  });

  element.addEventListener('dragleave', () => {
    element.classList.remove('drop-target');
  });

  element.addEventListener('drop', (e) => {
    e.preventDefault();
    element.classList.remove('drop-target');

    const data = JSON.parse(e.dataTransfer.getData('application/json'));
    if (acceptTypes.includes(data.type)) {
      onDrop(data);
    }
  });
}
```

### Click-to-Select Alternative

For touch devices and accessibility:

```javascript
let selectedItem = null;

function handleItemClick(item) {
  if (selectedItem === item) {
    // Deselect
    deselectItem();
  } else if (selectedItem) {
    // Try to place selected item
    if (canPlaceAt(selectedItem, item)) {
      placeItem(selectedItem, item);
    }
    deselectItem();
  } else {
    // Select this item
    selectItem(item);
  }
}

function selectItem(item) {
  selectedItem = item;
  item.classList.add('selected');
  highlightValidTargets(item);
}

function deselectItem() {
  if (selectedItem) {
    selectedItem.classList.remove('selected');
    clearHighlights();
    selectedItem = null;
  }
}
```

## Player Board UI

### Blueprint Slot Grid

```html
<div class="blueprint">
  <div class="blueprint-grid">
    <!-- Frame slots -->
    <div class="slot frame-slot" data-slot-type="frame" data-slot-id="frame-1">
      <div class="slot-label">Frame</div>
      <div class="slot-content">
        <!-- Upgrade tile goes here when installed -->
      </div>
      <div class="gas-socket">
        <!-- Gas cube indicator -->
      </div>
    </div>

    <!-- Drive slots -->
    <div class="slot drive-slot" data-slot-type="drive" data-slot-id="drive-1">
      <div class="slot-label">Drive</div>
      <div class="slot-content empty"></div>
    </div>

    <!-- More slots... -->
  </div>

  <div class="blueprint-stats">
    <div class="stat">
      <span class="stat-icon">⚖️</span>
      <span class="stat-value" data-stat="weight">12</span>
    </div>
    <div class="stat">
      <span class="stat-icon">🎈</span>
      <span class="stat-value" data-stat="lift">15</span>
    </div>
    <!-- More stats -->
  </div>
</div>
```

```css
.blueprint-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.5rem;
  padding: 1rem;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  border-radius: 8px;
}

.slot {
  aspect-ratio: 1;
  border: 2px dashed #444;
  border-radius: 4px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: border-color 0.2s, background 0.2s;
}

.slot.empty:hover {
  border-color: #4a9eff;
  background: rgba(74, 158, 255, 0.1);
}

.slot.filled {
  border-style: solid;
  border-color: #666;
}

.slot.drop-target {
  border-color: #4aff4a;
  background: rgba(74, 255, 74, 0.1);
}
```

## Card Hand Display

```html
<div class="hand-container">
  <div class="hand" id="player-hand">
    <!-- Cards fan out -->
  </div>
</div>
```

```css
.hand-container {
  perspective: 1000px;
  padding: 1rem;
}

.hand {
  display: flex;
  justify-content: center;
}

.card {
  width: 120px;
  height: 180px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.3);
  margin-left: -40px;  /* Overlap */
  transition: transform 0.2s, margin 0.2s;
  cursor: pointer;
}

.card:first-child {
  margin-left: 0;
}

.card:hover {
  transform: translateY(-20px) scale(1.05);
  margin-left: 0;
  margin-right: 40px;
  z-index: 10;
}

.card.selected {
  transform: translateY(-30px);
  box-shadow: 0 0 20px rgba(74, 158, 255, 0.5);
}
```

## Animations

### Token Movement

```javascript
function animateTokenMove(tokenElement, fromPos, toPos, duration = 500) {
  return new Promise(resolve => {
    // Calculate path
    const dx = toPos.x - fromPos.x;
    const dy = toPos.y - fromPos.y;

    // Use CSS animation
    tokenElement.style.transition = `transform ${duration}ms ease-out`;
    tokenElement.style.transform = `translate(${dx}px, ${dy}px)`;

    setTimeout(() => {
      // After animation, update actual position
      tokenElement.style.transition = '';
      tokenElement.style.transform = '';
      tokenElement.setAttribute('transform', `translate(${toPos.x}, ${toPos.y})`);
      resolve();
    }, duration);
  });
}
```

### State Change Animations

```css
/* Highlight changes */
@keyframes pulse-highlight {
  0%, 100% { box-shadow: 0 0 0 0 rgba(74, 158, 255, 0.5); }
  50% { box-shadow: 0 0 0 10px rgba(74, 158, 255, 0); }
}

.stat-value.changed {
  animation: pulse-highlight 0.5s ease-out;
}

/* Income animation */
@keyframes float-up {
  0% { opacity: 1; transform: translateY(0); }
  100% { opacity: 0; transform: translateY(-30px); }
}

.income-popup {
  animation: float-up 1s ease-out forwards;
  color: #4aff4a;
  font-weight: bold;
}
```

## Turn Indicator

```html
<div class="turn-indicator">
  <div class="current-player">
    <div class="player-avatar" style="--player-color: var(--player-1-color)"></div>
    <span class="player-name">Germany</span>
  </div>
  <div class="turn-timer" id="turn-timer">
    <svg class="timer-ring" viewBox="0 0 36 36">
      <circle cx="18" cy="18" r="16" fill="none" stroke="#333" stroke-width="3" />
      <circle class="timer-progress" cx="18" cy="18" r="16"
              fill="none" stroke="#4a9eff" stroke-width="3"
              stroke-dasharray="100" stroke-dashoffset="0" />
    </svg>
    <span class="timer-text">60</span>
  </div>
</div>
```

```javascript
function startTurnTimer(duration) {
  const timerText = document.querySelector('.timer-text');
  const timerProgress = document.querySelector('.timer-progress');
  let remaining = duration;

  const interval = setInterval(() => {
    remaining--;
    timerText.textContent = remaining;

    const percent = (remaining / duration) * 100;
    timerProgress.style.strokeDashoffset = 100 - percent;

    if (remaining <= 0) {
      clearInterval(interval);
    }
  }, 1000);

  return () => clearInterval(interval);
}
```

## Tooltips and Info Panels

```javascript
// Tooltip system
const tooltip = document.getElementById('tooltip');

function showTooltip(content, x, y) {
  tooltip.innerHTML = content;
  tooltip.style.left = `${x + 10}px`;
  tooltip.style.top = `${y + 10}px`;
  tooltip.classList.add('visible');
}

function hideTooltip() {
  tooltip.classList.remove('visible');
}

// Rich tooltips for game elements
function getTechnologyTooltip(techId) {
  const tech = technologies[techId];
  return `
    <div class="tooltip-tech">
      <h4>${tech.name}</h4>
      <p class="tooltip-cost">Cost: ${tech.cost} Research</p>
      <p class="tooltip-desc">${tech.description}</p>
      <p class="tooltip-unlocks">Unlocks: ${tech.unlocks}</p>
    </div>
  `;
}
```

## Accessibility

### Keyboard Navigation

```javascript
// Make game elements keyboard accessible
document.querySelectorAll('.slot, .card, .route').forEach(el => {
  el.setAttribute('tabindex', '0');
  el.setAttribute('role', 'button');

  el.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      el.click();
    }
  });
});
```

### Screen Reader Support

```html
<!-- Announce game state changes -->
<div id="game-announcer" aria-live="polite" class="sr-only"></div>

<script>
function announce(message) {
  document.getElementById('game-announcer').textContent = message;
}

// Usage
announce("Germany's turn. They placed a worker at the Construction Hall.");
</script>
```

## Performance Tips

1. **Batch DOM updates** - Use DocumentFragment or requestAnimationFrame
2. **Virtual scrolling** - For long lists (action log, card library)
3. **Lazy load assets** - Load board images for other Ages on demand
4. **Debounce resize handlers** - Don't recalculate layout on every pixel
5. **Use CSS transforms** - For animations instead of top/left
6. **Layer with z-index** - Keep frequently-updated elements on separate layers

## When This Skill Activates

Use this skill when:
- Building game board rendering
- Implementing drag-and-drop interactions
- Designing player board layouts
- Creating card hand displays
- Adding animations and transitions
- Making responsive game layouts
- Improving game accessibility
