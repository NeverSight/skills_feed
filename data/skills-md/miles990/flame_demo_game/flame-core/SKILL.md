---
name: flame-core
description: Flame Engine core fundamentals - components, input, collision, camera, animation, scenes
domain: game-development
version: 2.0.0
tags: [flame, flutter, dart, 2d-games, game-engine]
---

# Flame Core Fundamentals

Flame Engine 核心基礎，涵蓋組件系統、輸入處理、碰撞檢測、相機、動畫與場景管理。

## Quick Start

```bash
flutter create my_game && cd my_game
flutter pub add flame
flutter pub add flame_audio       # Optional
flutter pub add flame_tiled       # Optional
```

```dart
import 'package:flame/game.dart';
import 'package:flutter/material.dart';

void main() => runApp(GameWidget(game: MyGame()));

class MyGame extends FlameGame with HasCollisionDetection {
  @override
  Future<void> onLoad() async {
    camera.viewfinder.anchor = Anchor.topLeft;
  }
}
```

## Reference Index

| Topic | File | Description |
|-------|------|-------------|
| **Components** | `references/components.md` | 組件生命週期、類型、最佳實踐 |
| **Input** | `references/input.md` | 觸控、鍵盤、搖桿輸入處理 |
| **Collision** | `references/collision.md` | 碰撞檢測、Hitbox 類型 |
| **Camera** | `references/camera.md` | 相機設置、跟隨、HUD |
| **Animation** | `references/animation.md` | 精靈動畫、Effects 系統 |
| **Scenes** | `references/scenes.md` | RouterComponent、Overlays、UI |
| **Audio** | `references/audio.md` | 音效、背景音樂、AudioPool |
| **Particles** | `references/particles.md` | 粒子系統、特效、爆炸效果 |
| **Performance** | `references/performance.md` | 效能優化、最佳實踐、常見問題 |
| **Debug** | `references/debug.md` | 除錯模式、日誌、效能監控 |

## AI Usage Guide

```
需要了解組件系統？ → Read references/components.md
需要處理輸入？     → Read references/input.md
需要碰撞檢測？     → Read references/collision.md
需要相機設置？     → Read references/camera.md
需要動畫效果？     → Read references/animation.md
需要場景管理/UI？  → Read references/scenes.md
需要音效/音樂？    → Read references/audio.md
需要粒子特效？     → Read references/particles.md
需要效能優化？     → Read references/performance.md
需要除錯/日誌？    → Read references/debug.md
```

## Component Types Quick Reference

| Type | Use Case |
|------|----------|
| `Component` | Logic only |
| `PositionComponent` | Has position/size |
| `SpriteComponent` | Static image |
| `SpriteAnimationComponent` | Animated sprite |
| `SpriteAnimationGroupComponent` | Multiple states |

## Related Skills

- `flame-systems` - 14 個遊戲系統（任務、對話、背包等）
- `flame-templates` - 遊戲類型模板（RPG、平台、Roguelike）
