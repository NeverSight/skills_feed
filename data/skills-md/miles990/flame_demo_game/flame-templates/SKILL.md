---
name: flame-templates
description: Game type templates for Flame Engine - RPG, Platformer, Roguelike starter code
domain: game-development
version: 2.0.0
tags: [flame, flutter, dart, game-templates, starter]
---

# Flame Game Templates

三種主要遊戲類型的完整起始模板和架構。

## Reference Index

| Template | File | Description |
|----------|------|-------------|
| **RPG** | `references/rpg.md` | 回合制/動作 RPG 完整架構 |
| **Platformer** | `references/platformer.md` | 橫向卷軸平台遊戲 |
| **Roguelike** | `references/roguelike.md` | 程序生成地下城 |

## AI Usage Guide

```
需要 RPG 遊戲？      → Read references/rpg.md
需要平台遊戲？       → Read references/platformer.md
需要 Roguelike？    → Read references/roguelike.md
```

## Template Comparison

| Feature | RPG | Platformer | Roguelike |
|---------|-----|------------|-----------|
| View | Top-down / Isometric | Side-view | Top-down |
| Combat | Turn-based / Action | Real-time | Turn / Real-time |
| Progression | Level + Equipment | Checkpoints | Permadeath + Meta |
| Map | Static + Towns | Linear Levels | Procedural |

## Quick Start

每個模板包含：
- 完整 main.dart
- Player 類別
- 核心遊戲循環
- 基礎 UI

## Related Skills

- `flame-core` - 引擎核心基礎
- `flame-systems` - 14 個遊戲系統
