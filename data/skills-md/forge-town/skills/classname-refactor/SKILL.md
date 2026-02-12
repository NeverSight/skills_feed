---
name: classname-refactor
description: 自动检查并转换 React/Vue 文件中 className 的模板字符串为 cn 函数调用；支持递归扫描文件夹、详细报告所有 className 位置
---

# ClassName Refactor

## 任务目标
- 本 Skill 用于：检查并转换代码中 `className` 属性的模板字符串为 `cn` 函数调用
- 能力包含：递归文件夹扫描、详细位置报告、批量转换、结果汇总
- 触发条件：用户上传文件/文件夹并要求检查/转换 className

## 核心原则

**所有模板字符串形式的 className 必须转换为调用 cn 函数**

- ❌ 错误：`className={`flex ${condition}`}`
- ✅ 正确：`className={cn("flex", condition)}`

**必须导入 cn 函数**

在转换后的文件顶部添加标准导入语句：

```tsx
import { cn } from "@/lib/utils";
```

## 标准流程

### 第一步：识别输入类型并递归扫描
判断是单个文件还是文件夹：
- **单个文件**：直接读取该文件内容
- **文件夹**：递归扫描所有子文件夹，列出所有 .tsx/.jsx/.vue 文件

### 第二步：逐个文件详细检查
对每个文件执行以下检查：
1. 读取完整文件内容
2. 检查是否已导入 cn 函数
3. 扫描所有 className 属性
4. 记录每个 className 的位置（文件名、行号）和格式
5. 分类统计：
   - 使用模板字符串的 className（**必须转换为 cn 函数调用**）
   - 使用普通字符串的 className（符合要求）
   - 已使用 cn 函数的 className（符合要求）

### 第三步：生成详细报告
**无论是否符合要求，都要显示所有 className 的位置**

#### 报告结构
```
📁 扫描完成！共发现 X 个目标文件

✅/🔍 检查结果：[总结]

详细检查报告：
[每个文件的详细列表，包含文件名、行号、className 内容、类型标注]

📊 统计摘要：
- 扫描文件：X 个
- className 总数：Y 个
- 使用模板字符串：Z 个（必须转换为 cn 函数调用）
- 符合要求：W 个
- 需要导入 cn 函数：N 个

[如果需要转换]
需要转换为 cn 函数调用的文件：
- 文件列表和转换数量

[如果需要导入]
需要添加 cn 函数导入的文件：
- 文件列表
```

#### 报告标注说明
- ⚠️ 必须转换为 cn 函数调用：使用模板字符串的 className
- 符合要求：普通字符串或已调用 cn 函数

### 第四步：执行转换（仅在需要时）
将模板字符串转换为调用 cn 函数，输出完整代码。

**注意**：如果文件中未导入 cn 函数，在输出代码时提醒用户添加：

```tsx
import { cn } from "@/lib/utils";
```

### 第五步：验证与提醒
1. 检查导入语句，列出需要添加 cn 函数导入的文件
2. 提供转换摘要
3. 建议测试验证

## 转换规则（必须调用 cn 函数）

```tsx
// 规则 1：静态类名
className={`flex gap-4`}
→ className={cn("flex gap-4")}

// 规则 2：动态变量
className={`${myClass}`}
→ className={cn(myClass)}

// 规则 3：混合
className={`base ${dynamic}`}
→ className={cn("base", dynamic)}

// 规则 4：条件表达式
className={`base ${isActive ? 'active' : ''}`}
→ className={cn("base", isActive ? "active" : "")}

// 规则 5：多个参数
className={`base ${a} ${b}`}
→ className={cn("base", a, b)}
```

## cn 函数导入

### 标准导入方式

**cn 函数的标准导入路径为 `@/lib/utils`**

在文件顶部添加：

```tsx
import { cn } from "@/lib/utils";
```

### 检查导入

转换后，检查文件是否已导入 cn 函数：
- 如果已导入：无需额外操作
- 如果未导入：提醒用户添加导入语句

### 导入位置

cn 函数的导入语句应放在文件顶部的导入区域，与其他导入语句一起。

```tsx
import { useState } from "react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
```

## 资源索引
- [references/conversion-rules.md](references/conversion-rules.md)（详细规则）
- [references/examples.md](references/examples.md)（示例文档）

## 注意事项
- **必须调用 cn 函数**：所有模板字符串形式的 className 必须转换为调用 cn 函数
- **必须导入 cn 函数**：转换后的文件必须导入 cn 函数，标准路径为 `@/lib/utils`
- **递归扫描**：必须递归扫描所有子文件夹，不能遗漏任何文件
- **详细报告**：无论是否符合要求，都要显示所有 className 的文件和行号
- **完整统计**：提供完整的统计摘要，包括所有 className 的数量
- **分类明确**：清楚标注每个 className 的类型（模板字符串/普通字符串/cn 函数调用）
- **测试验证**：转换后必须测试组件的显示效果

## 常见问题
**Q: 文件夹嵌套很深怎么办？**
A: 递归扫描所有子文件夹，无论嵌套多深都要扫描。

**Q: 如何确保不遗漏文件？**
A: 使用递归扫描，列出所有 .tsx/.jsx/.vue 文件，逐个检查。

**Q: 文件太多报告会很长吗？**
A: 提供详细的分类报告和统计摘要，便于快速了解整体情况。

**Q: 为什么要使用 cn 函数？**
A: cn 函数提供了更好的可读性、类型安全和条件类名处理能力。

**Q: cn 函数从哪里导入？**
A: cn 函数的标准导入路径为 `@/lib/utils`。
