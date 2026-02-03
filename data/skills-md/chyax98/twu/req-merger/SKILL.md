---
name: req-merger
description: 合并需求问题答案，生成完备需求
allowed-tools: Read, Write, Bash
---

# 需求合并 Skill

## 目标

将 `cleaned-requirements/issues.md` 中的问题答案整合到需求文档中，生成完备需求。

## 输入输出

- **输入**：`cleaned-requirements/index.md`、`cleaned-requirements/issues.md`（已填写答案）
- **输出**：`clarified-requirements/index.md`

## 核心原则

1. **忠实整合**：准确反映问题答案，不自行发挥
2. **适当保持结构**：维持原需求文档的结构和格式，必要时可调整以提升清晰度
3. **清晰标注**：新增内容要清晰可辨识

---

## 执行流程

### 1. 整合方式

常见整合方式（可灵活选择）：

**方式1：直接更新原文**
- 适用场景：答案是对原文的补充或修正
- 示例：原文"用户可以上传图片" → 更新为"用户可以上传图片（支持 jpg/png/gif，最大 5MB）"

**方式2：添加补充说明章节**
- 适用场景：答案是新增的规则或说明
- 位置：文档末尾添加"## 补充说明（基于问题澄清）"

**方式3：融合到原文**
- 适用场景：答案需要与原文深度融合
- 要求：确保逻辑连贯，无突兀感

**核心要求**：无论采用哪种方式，必须确保答案完整整合，无遗漏。

### 2. 操作步骤

1. 复制 `cleaned-requirements/index.md` 到 `clarified-requirements/index.md`
2. 复制 `cleaned-requirements/assets/` 到 `clarified-requirements/assets/`（如果有图片）
3. 读取 `cleaned-requirements/issues.md` 中的所有问题和答案
4. 逐个问题处理：
   - 找到问题对应的原文位置
   - 判断用方式1还是方式2
   - 整合答案到文档
5. 生成 `clarified-requirements/index.md`

### 3. 答案检查

**答案完整性检查**：
- 确认所有 critical 优先级问题已回答
- 确认所有 warning 优先级问题已回答或标记为"待补充"
- 如果 critical 问题未回答或答案不完整，必须提示用户补充
- 如果 warning 问题未回答，建议用户补充（非强制）

**补充策略**：
- 核心流程相关的问题：必须补充
- 边界条件相关的问题：建议补充
- 异常处理相关的问题：建议补充
- 如果用户填写完毕后让你继续，但你觉得逻辑还不清晰，可以再次询问用户

---

## 示例

### 示例1：直接更新原文

**原文**：
```
用户可以上传图片
```

**问题答案**：
```
支持格式：jpg, png, gif
大小上限：5MB
```

**更新后**：
```
用户可以上传图片（支持 jpg/png/gif，最大 5MB）
```

### 示例2：添加补充说明

**原文**：
```
系统应快速响应
```

**问题答案**：
```
接口响应：<200ms
页面加载：<2s
```

**更新后（文档末尾添加）**：
```
## 补充说明（基于问题澄清）

### 性能指标
- 接口响应：<200ms
- 页面加载：<2s
```

---

## 检查清单

- [ ] 所有 critical 问题已回答
- [ ] 所有 warning 问题已回答或标记为"待补充"
- [ ] 答案已整合到文档中
- [ ] 新增内容清晰可辨识
- [ ] 保持了原文档结构
- [ ] 图片资源已复制到 clarified-requirements/assets/
- [ ] 生成了 clarified-requirements/index.md
