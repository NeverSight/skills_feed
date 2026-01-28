---
name: flame-systems
description: Flame Engine 14 game systems - quest, dialogue, inventory, combat, save/load, shop, crafting, and more
domain: game-development
version: 2.0.0
tags: [flame, flutter, dart, game-systems, rpg]
---

# Flame Game Systems

14 個常見遊戲系統的實作模式與參考代碼。

## Reference Index

| System | File | Description |
|--------|------|-------------|
| **Quest** | `references/quest.md` | 任務系統、目標追蹤、獎勵 |
| **Dialogue** | `references/dialogue.md` | 對話系統、分支選項、NPC |
| **Localization** | `references/localization.md` | 多語言、文本管理 |
| **Inventory** | `references/inventory.md` | 背包、物品堆疊、分類 |
| **Paper Doll** | `references/paperdoll.md` | 角色外觀、裝備視覺 |
| **Combat** | `references/combat.md` | 戰鬥系統、傷害計算 |
| **Skills** | `references/skills.md` | 技能樹、冷卻、效果 |
| **Save/Load** | `references/saveload.md` | 存檔、序列化、雲端 |
| **Achievement** | `references/achievement.md` | 成就、解鎖、進度 |
| **Shop** | `references/shop.md` | 商店、交易、貨幣 |
| **Crafting** | `references/crafting.md` | 製作、配方、材料 |
| **Procedural** | `references/procedural.md` | 隨機生成、Roguelike |
| **Multiplayer** | `references/multiplayer.md` | 多人連線、同步 |
| **Level Editor** | `references/leveleditor.md` | 關卡編輯器、地圖工具 |

## AI Usage Guide

```
需要任務系統？     → Read references/quest.md
需要對話系統？     → Read references/dialogue.md
需要多語言？       → Read references/localization.md
需要背包系統？     → Read references/inventory.md
需要裝備外觀？     → Read references/paperdoll.md
需要戰鬥系統？     → Read references/combat.md
需要技能系統？     → Read references/skills.md
需要存檔功能？     → Read references/saveload.md
需要成就系統？     → Read references/achievement.md
需要商店系統？     → Read references/shop.md
需要製作系統？     → Read references/crafting.md
需要隨機生成？     → Read references/procedural.md
需要多人連線？     → Read references/multiplayer.md
需要關卡編輯？     → Read references/leveleditor.md
```

## System Dependencies

```
Combat ──→ Skills (技能影響戰鬥)
       ──→ Inventory (裝備影響屬性)
       ──→ Paper Doll (裝備外觀)

Quest ──→ Dialogue (NPC 給予任務)
      ──→ Achievement (完成任務獲得成就)
      ──→ Inventory (任務獎勵物品)

Shop ──→ Inventory (購買物品存入背包)
     ──→ Crafting (購買材料用於製作)

Procedural ──→ Combat (生成敵人)
           ──→ Inventory (隨機掉落)
```

## Related Skills

- `flame-core` - 引擎核心基礎
- `flame-templates` - 遊戲類型模板
