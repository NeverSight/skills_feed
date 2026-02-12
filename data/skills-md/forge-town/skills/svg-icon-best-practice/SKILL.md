---
name: svg-icon-best-practice
description: 统一管理 React TypeScript 项目中的 SVG 图标；支持图标组件封装、命名规范、迁移指导；适用于项目图标重构、新项目图标规范制定、图标维护优化场景
---

# SVG 图标管理规范

## 任务目标
- 本 Skill 用于：统一 React TypeScript 项目中 SVG 图标的存储、封装和使用方式
- 能力包含：SVG 转换为 React 组件、图标迁移流程、使用规范说明
- 触发条件：用户需要"统一管理 SVG 图标"、"重构图标代码"、"创建图标规范"、"迁移内联 SVG"

## 前置准备
- 依赖说明：无外部依赖，使用 React + TypeScript 内置能力
- 目录结构准备：确保项目中存在 `components/` 目录，创建 `components/icons/` 子目录
  ```bash
  mkdir -p src/components/icons
  ```

**最佳实践示例**：参考 [best-practice-examples/](best-practice-examples/) 目录下的实际项目示例
- `best-practice-examples/assets/` - 业务组件示例
- `best-practice-examples/components/icons/` - 图标组件示例

## 快速开始（给智能体的执行指令）

当用户要求"将内联 SVG 抽离"或"统一管理图标"时，智能体应按以下步骤执行：

### 步骤 1：扫描并识别图标
```
1. 使用 glob_file 或 grep_file 搜索项目中所有的 .tsx/.jsx 文件
2. 在这些文件中搜索包含 <svg> 标签的代码
3. 记录所有找到的内联 SVG 位置（文件路径、行号）
4. 读取这些文件，提取完整的 SVG 代码
```

### 步骤 2：创建图标组件
```
1. 对于每个提取的 SVG：
   - 确定图标功能，生成合适的组件名（PascalCase）
   - 在 src/components/icons/ 目录创建对应的 .tsx 文件
   - 按照 icon-component-template.md 的模板编写组件代码
   - 确保包含 TypeScript 类型定义
```

### 步骤 3：更新业务组件
```
1. 对于每个包含内联 SVG 的文件：
   - 添加 import 语句导入新创建的图标组件
   - 删除原有的 <svg> 标签
   - 替换为 <IconName /> 组件调用
   - 迁移原始的属性（width、height、fill 等）
```

### 步骤 4：验证完成
```
1. 确认所有内联 SVG 都已替换为组件
2. 确认所有图标组件都保存在 src/components/icons/ 目录
3. 确认所有组件文件名和命名符合规范
4. 确认 TypeScript 编译无错误
```

---

## 操作步骤

### 1. 创建图标目录结构
在项目根目录执行以下操作：
- 创建 `components/icons/` 目录（如果不存在）
- 该目录将存放所有图标组件

### 2. 提取并封装 SVG 为 React 组件

#### 2.1 识别并读取需要迁移的图标
**执行步骤：**
1. 使用文件搜索工具查找项目中所有 `.tsx` 和 `.jsx` 文件
2. 在这些文件中搜索内联的 `<svg>` 标签
3. 记录所有包含内联 SVG 的文件路径和行号
4. 读取这些文件，提取完整的 SVG 代码
5. 识别每个 SVG 的用途（按钮图标、导航图标等）

**关键检查点：**
- [ ] 已定位所有内联 SVG 的位置
- [ ] 已记录每个 SVG 的上下文用途
- [ ] 已提取完整的 SVG 代码（包括 viewBox、path 等）

#### 2.2 转换 SVG 为 React 组件
**执行步骤：**
对于每个提取的 SVG，执行以下操作：

1. **读取并解析 SVG 代码**：获取完整的 `<svg>` 标签及其内容
2. **转换文件名**：将原始文件名或功能描述转换为 PascalCase 格式
3. **创建组件文件**：在 `src/components/icons/` 目录下创建 `.tsx` 文件
4. **编写组件代码**：参考 [references/icon-component-template.md](references/icon-component-template.md)，按照模板编写组件
5. **保存文件**：将创建的组件保存到 `src/components/icons/` 目录

**示例操作：**
```
输入：从 Button.tsx 提取的箭头 SVG
  ↓
步骤 1：读取 SVG 代码 <svg viewBox="0 0 24 24"><path d="..." /></svg>
  ↓
步骤 2：转换文件名 ArrowRight
  ↓
步骤 3：创建 src/components/icons/ArrowRight.tsx
  ↓
步骤 4：参考模板编写组件代码
  ↓
步骤 5：保存文件
```

**完整模板和示例：** 详见 [references/icon-component-template.md](references/icon-component-template.md)

### 3. 更新业务组件

#### 3.1 替换内联 SVG
**执行步骤：**
对于每个包含内联 SVG 的业务组件：

1. **定位内联 SVG 代码**：找到组件中的 `<svg>` 标签
2. **记录原始属性**：记下原有的 width、height、fill、className 等属性值
3. **添加导入语句**：在文件顶部添加 `import IconName from '@/components/icons/IconName'`
4. **替换 SVG 标签**：删除 `<svg>` 标签及其内容，替换为 `<IconName />`
5. **迁移属性**：将原始属性作为 props 传递给新组件（如 `<IconName width={24} height={24} />`）
6. **验证功能**：确认替换后组件功能和样式保持一致

#### 3.2 使用封装的 Icon 组件
- 从 `components/icons` 导入图标组件
- 按需传递 props（size、color 等）
- 支持通过 className 自定义样式

详细使用示例见 [references/best-practice-examples.md](references/best-practice-examples.md)

### 4. 图标迁移检查清单
完整的迁移检查清单详见 [references/migration-checklist.md](references/migration-checklist.md)，包含：
- 迁移前环境检查
- 逐步迁移操作指南
- 迁移后功能验证
- 常见问题解决方案

### 5. 代码审查与规范检查
在完成迁移后，检查以下规范：

**禁止场景：**
- ❌ 禁止在业务组件内直接写 SVG 代码
- ❌ 禁止在 icons 目录外存放独立的 SVG 组件文件
- ❌ 禁止在非 components/icons 目录下创建图标组件

**规范要求：**
- ✅ 所有 SVG 图标必须封装为 React 组件
- ✅ 组件必须保存在 `components/icons/` 目录下
- ✅ 必须从 `components/icons` 导入使用
- ✅ 组件必须包含 TypeScript 类型定义
- ✅ 支持通过 props 配置常用属性

详细的规范要求详见各参考文档。

## 资源索引
- 最佳实践示例：见 [best-practice-examples/](best-practice-examples/)（实际项目示例，包含 components 和 assets）
  - [best-practice-examples/components/icons/](best-practice-examples/components/icons/) - 图标组件示例
  - [best-practice-examples/assets/](best-practice-examples/assets/) - 业务组件示例
- 组件模板：见 [references/icon-component-template.md](references/icon-component-template.md)（标准 React 图标组件模板、属性配置、常见变体）
- 迁移清单：见 [references/migration-checklist.md](references/migration-checklist.md)（完整迁移检查项、问题解决方案）
- 最佳实践文档：见 [references/best-practice-examples.md](references/best-practice-examples.md)（基于实际项目的最佳实践和使用说明）

## 注意事项
- 仅在需要创建新的图标组件或迁移现有图标时读取参考文档
- 智能体已具备理解和转换 SVG 代码的能力，无需自动化脚本
- 转换时保留 SVG 的 viewBox 和 path 数据，确保图标形状不变
- 默认 fill="currentColor" 以支持通过 CSS 控制颜色
- 使用 TypeScript 确保类型安全，避免运行时错误
- [best-practice-examples/](best-practice-examples/) 目录包含实际项目示例，可供参考

## 使用示例

### 场景 1：迁移现有内联 SVG
**需求：** 将 Button 组件中的内联箭头图标提取为独立组件

**执行方式：** 智能体手动执行
1. 读取 Button 组件中的 SVG 代码
2. 参考 [references/icon-component-template.md](references/icon-component-template.md) 创建 ArrowRight.tsx
3. 参考 [best-practice-examples/components/icons/](best-practice-examples/components/icons/) 中的示例
4. 替换 Button 组件中的内联 SVG
5. 测试验证显示效果

### 场景 2：创建新图标规范
**需求：** 新项目需要建立图标管理规范

**执行方式：** 智能体自然语言指导
1. 创建 components/icons/ 目录
2. 参考 [references/icon-component-template.md](references/icon-component-template.md) 创建图标组件
3. 参考 [best-practice-examples/components/icons/](best-practice-examples/components/icons/) 中的桶导出方式
4. 在项目中推行统一的图标使用方式

### 场景 3：批量迁移图标
**需求：** 项目中有多个内联 SVG 需要统一迁移

**执行方式：** 智能体逐个处理
1. 扫描识别所有内联 SVG 位置
2. 按照 [references/migration-checklist.md](references/migration-checklist.md) 逐个迁移
3. 替换所有业务组件中的内联 SVG
4. 执行完整回归测试
