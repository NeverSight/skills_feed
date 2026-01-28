---
name: builder-ux
description: Builder user experience systems for Three.js building games. Use when implementing prefab/blueprint save/load, undo/redo command patterns, ghost preview placement, multi-select, or copy/paste building mechanics. Covers the UX layer that makes building feel responsive and intuitive.
---

# Builder UX

Prefabs, blueprints, undo/redo, selection, and preview systems for building mechanics.

## Quick Start

```javascript
import { BlueprintManager } from './scripts/blueprint-manager.js';
import { CommandHistory, PlaceCommand, BatchCommand } from './scripts/command-history.js';
import { GhostPreview } from './scripts/ghost-preview.js';
import { SelectionManager } from './scripts/selection-manager.js';

// Initialize systems
const blueprints = new BlueprintManager();
const history = new CommandHistory({ maxSize: 50 });
const ghost = new GhostPreview(scene);
const selection = new SelectionManager({ maxSelection: 100 });

// Save selected pieces as blueprint
const { blueprint } = blueprints.save(selection.getSelection(), 'My Base');

// Load blueprint at new position
const { pieces } = blueprints.load(blueprint.id, newPosition, rotation);

// Place with undo support
history.execute(new PlaceCommand(pieceData, position, rotation, buildingSystem));
history.undo(); // Removes piece
history.redo(); // Restores piece

// Ghost preview with validity feedback
ghost.show('wall', cursorPosition, rotation);
ghost.setValid(canPlace); // Green/red color
ghost.updatePosition(newCursorPosition);

// Multi-select with box selection
selection.boxSelect(startNDC, endNDC, camera, allPieces);
selection.selectConnected(startPiece, getNeighbors); // Flood fill

// Batch operations
history.beginGroup('Delete selection');
for (const piece of selection.getSelection()) {
  history.execute(new RemoveCommand(piece, buildingSystem));
}
history.endGroup();
```

## Reference

See `references/builder-ux-advanced.md` for:
- Command pattern with PlaceCommand, RemoveCommand, UpgradeCommand, BatchCommand
- Blueprint serialization format and versioning
- Ghost preview rendering with pulse animation
- Selection systems: single, additive, box, radius, connected
- Copy/paste and blueprint sharing

## Scripts

| File | Lines | Purpose |
|------|-------|---------|
| `blueprint-manager.js` | ~450 | Save, load, export/import building designs |
| `command-history.js` | ~400 | Undo/redo stack with command pattern |
| `ghost-preview.js` | ~380 | Transparent placement preview with snapping |
| `selection-manager.js` | ~420 | Multi-select, box select, group operations |

## Key Patterns

### Command Pattern
Every building action becomes a command with `execute()` and `undo()`. This enables:
- Undo/redo for free
- Network replication (serialize command, send to server)
- Macro recording (save command sequences)
- Validation before execution

### Blueprint System
Blueprints store relative positions, making them position and rotation independent. Key features:
- Auto-centering on save
- Rotation support on load
- Export/import for sharing
- Thumbnail generation

### Ghost Preview
Shows placement intent before commitment:
- Green = valid placement
- Red = invalid (collision, no support)
- Orange = blocked (permissions)
- Pulse animation for visibility
- Grid/rotation snapping

### Selection Manager
Supports multiple selection modes:
- Single click (replace selection)
- Shift+click (additive)
- Ctrl+click (toggle)
- Box select (screen space)
- Radius select (world space)
- Connected select (flood fill)

## Integration

```javascript
// Full integration example
function setupBuildingUX(scene, buildingSystem) {
  const history = new CommandHistory({
    maxSize: 100,
    onChange: (status) => updateUndoRedoButtons(status)
  });
  
  const ghost = new GhostPreview(scene, {
    validColor: 0x00ff00,
    invalidColor: 0xff0000,
    snapGrid: 2,
    snapRotation: Math.PI / 4
  });
  
  const selection = new SelectionManager({
    maxSelection: 200,
    onSelectionChanged: (pieces) => updateSelectionUI(pieces)
  });
  
  const blueprints = new BlueprintManager({
    storage: localStorage,
    maxBlueprints: 50
  });
  
  // Keyboard shortcuts
  document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key === 'z') history.undo();
    if (e.ctrlKey && e.key === 'y') history.redo();
    if (e.ctrlKey && e.key === 'c') copySelection();
    if (e.ctrlKey && e.key === 'v') pasteBlueprint();
    if (e.key === 'r') ghost.rotate(Math.PI / 4);
  });
  
  return { history, ghost, selection, blueprints };
}
```

## Design Philosophy

Building UX separates intent from execution. The ghost preview shows what will happen, the command executes it, and the history allows reversal. This separation enables blueprint placement (preview entire structure), batch undo (reverse multiple operations), and networked building (commands serialize for transmission).
