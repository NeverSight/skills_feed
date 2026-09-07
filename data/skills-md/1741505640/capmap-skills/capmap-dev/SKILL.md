---
name: capmap-dev
description: >-
  开发落地后的文档收尾：更新能力底图 §1/§2（代码路径），并将对应方案主状态标为
  已开发。体量/大 须切片/<方案stem>/ 下全部切片已验收。底图不打状态 Tag。
  适用于「功能开发完了」「标记已开发」。
---

# capmap-dev — 开发完成标识

原则：[lifecycle](../capmap-system/reference/lifecycle.md) · Tag：[status-tags](../capmap-system/reference/status-tags.md)

## 做什么

1. 若方案为 **`体量/大`**：检查 `切片/<方案stem>/` 下所有切片（非规格）均为 `状态/已验收`；未齐则 **停止**，提示用 [capmap-gate](../capmap-gate/SKILL.md) 收尾  
2. 打开对应 `能力底图-*.md`：§1 状态列 → **已开发**；§2 补路径；§4 一行轨迹  
3. 底图 YAML：**仅** `能力底图`，去掉任何 `状态/*`  
4. 对应**方案**文主状态 → **`状态/已开发`**（保留体量 Tag）  
5. 提醒 `capmap-test`（方案可改 `验证中`）→ 通过后再 `capmap-norm` → `capmap-archive`  
6. **硬约束**：本阶段最多标到 `已开发`；**禁止**标 `落地中` / `已落地`（须先测试 `已验证`）

## Checklist

```
- [ ] 1. 体量/大 → 切片全已验收（或体量/小跳过）
- [ ] 2. 底图 §1/§2/§4 已更新
- [ ] 3. 底图无 状态/* Tag
- [ ] 4. 方案 Tag = 已开发（禁止已落地）
- [ ] 5. 提示测试 / 规范 / 归档
- [ ] 6. 未跳过验证门
```

## 不做

- 不写测试正文 → [capmap-test](../capmap-test/SKILL.md)  
- 不写规范 → [capmap-norm](../capmap-norm/SKILL.md)  
- 不归档 → [capmap-archive](../capmap-archive/SKILL.md)  
- 不代替 gate 验收切片  
