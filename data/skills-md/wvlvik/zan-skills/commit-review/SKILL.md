---
name: commit-review
description: 微信小程序原生开发项目代码提交评审技能，检查架构约束、最佳实践和常见问题
---

# 微信小程序原生开发代码提交评审

这个技能用于在代码提交前进行全面的架构和代码质量评审，确保符合项目的关键约束和最佳实践。

## 何时使用

在以下场景使用此技能：
- 准备提交代码前（git commit 之前）
- 代码审查时
- 用户明确要求评审代码时
- 关键词：review, 评审, 检查, commit, 提交

## 评审检查清单

### 🔴 关键架构约束（必须遵守）

#### 1. Runtime 模块外部化
**最关键的架构约束** - runtime 模块必须保持外部引用，绝不能被打包。

**检查项：**
- [ ] 所有 `import ... from 'runtime'` 或 `import ... from 'runtime/...'` 的引用是否正确
- [ ] vite.config.ts 中是否正确配置了 runtime 外部化
- [ ] 没有尝试修改 runtime 的外部化配置
- [ ] 没有在 optimizeDeps.include 中包含 runtime

#### 2. 依赖安装规则
**所有新依赖必须安装为 devDependencies**

**检查项：**
- [ ] package.json 中是否有新增的 dependencies（应该为空或只有必要的运行时依赖）
- [ ] 所有新安装的包是否使用了 `pnpm i -D` 命令

**正确做法：**
```bash
# ✅ 正确
pnpm i -D package-name

# ❌ 错误
pnpm i package-name
```

#### 3. TypeScript 强制使用
**所有逻辑文件必须使用 TypeScript (.ts)，禁止使用 .js**

**检查项：**
- [ ] 新增或修改的页面/组件是否使用 .ts 文件
- [ ] 基本类型检查，确保类型正确，特别注意组件props和函数参数类型不能使用any
- [ ] 没有创建新的 .js 文件（除非是配置文件）
- [ ] 类型定义是否完整

**文件结构：**
```
pages/page-name/
├── page-name.ts      ✅ 使用 TypeScript
├── page-name.json
└── page-name.wxml

components/comp-name/
├── comp-name.ts      ✅ 使用 TypeScript
├── comp-name.json
└── comp-name.wxml
```

#### 4. Tailwind CSS 强制使用
**所有样式必须使用 Tailwind CSS，禁止创建 .wxss 文件**

**检查项：**
- [ ] 没有创建新的 .wxss 文件
- [ ] 所有样式都在 .wxml 中使用 Tailwind 类名
- [ ] 使用了正确的 rpx 单位（Tailwind 会自动转换 rem 为 rpx）

**正确做法：**
```html
<!-- ✅ 正确：使用 Tailwind CSS -->
<view class="flex items-center justify-between px-4 py-2 bg-white rounded-lg">
  <text class="text-base font-medium text-gray-900">标题</text>
</view>

<!-- ❌ 错误：创建 .wxss 文件 -->
```

### 🟡 组件开发规范

#### 5. Component 配置
**所有组件必须设置正确的 styleIsolation**

**检查项：**
- [ ] 组件的 .json 文件中是否包含 `"styleIsolation": "apply-shared"`
- [ ] 组件是否正确声明为 `"component": true`

**正确配置：**
```json
{
  "component": true,
  "styleIsolation": "apply-shared",
  "usingComponents": {}
}
```

### 🟢 性能最佳实践

#### 6. setData 优化
**使用数据路径和批量更新**

**检查项：**
- [ ] 是否使用了数据路径更新：`this.setData({ 'list[0].text': 'new' })`
- [ ] 是否合并了多个 setData 调用
- [ ] 没有在循环中调用 setData

**优化示例：**
```typescript
// ❌ 错误：多次调用
this.setData({ name: 'John' })
this.setData({ age: 25 })

// ✅ 正确：合并调用
this.setData({
  name: 'John',
  age: 25
})

// ✅ 正确：使用数据路径
this.setData({ 'list[0].text': 'new' })
```

#### 7. Component vs Page
**优先使用 Component() 而非 Page()**

**检查项：**
- [ ] 新页面是否使用 Component() 构造器
- [ ] 只在必要时使用 Page()

**推荐做法：**
```typescript
// ✅ 推荐：使用 Component
Component({
  data: {},
  methods: {}
})

// ⚠️ 仅在必要时使用 Page
Page({
  data: {},
  onLoad() {}
})
```

### 🔵 常见问题检查

#### 8. iOS 日期解析
**iOS 不支持 'YYYY-MM-DD' 格式**

**检查项：**
- [ ] 日期字符串是否使用 `.replace(/-/g, '/')` 处理

**正确做法：**
```typescript
// ❌ 错误：iOS 会解析失败
new Date('2024-01-01')

// ✅ 正确：兼容 iOS
new Date('2024-01-01'.replace(/-/g, '/'))
```

#### 10. 图标使用规范
**必须使用 iconfont，禁止使用图片文件**

**检查项：**
- [ ] 图标是否使用 `<text class="icon icon-xxx"></text>` 格式
- [ ] 没有为图标创建 .png/.jpg 等图片文件

**正确做法：**
```html
<!-- ✅ 正确：使用 iconfont -->
<text class="icon icon-arrow-right text-gray-400"></text>

<!-- ❌ 错误：使用图片 -->
<image src="/images/arrow.png"></image>
```

### 📦 构建和发布

#### 11. 构建产物检查
**确保三个输出目录的正确性**

**检查项：**
- [ ] dist/ - 主构建输出（包含 miniprogram_npm）
- [ ] dist_miniprogram/ - NPM 包分发（排除 pages、app.js、miniprogram_npm）
- [ ] dist_plugin/ - 插件包（包含 plugin.json）

#### 12. 插件发布准备
**发布前必须清理 dist 目录**

**检查项：**
- [ ] 是否更新了 project.config.json 中的 appid
- [ ] 是否更新了 miniprogram/app.json 中的 provider
- [ ] dist/app.json 是否替换为插件配置
- [ ] dist 目录是否只保留必要文件

### 🔒 安全检查

#### 13. 安全漏洞
**检查常见安全问题**

**检查项：**
- [ ] 没有命令注入风险
- [ ] 没有 XSS 漏洞（用户输入是否正确转义）
- [ ] 没有敏感信息泄露（API key、token 等）

### 📝 代码质量

#### 14. 代码简洁性
**避免过度工程**

**检查项：**
- [ ] 没有添加未被要求的功能
- [ ] 没有不必要的重构
- [ ] 没有为一次性操作创建工具函数
- [ ] 没有添加不必要的错误处理
- [ ] 没有添加未使用的类型定义或注释

#### 15. 向后兼容性
**避免兼容性黑客**

**检查项：**
- [ ] 没有重命名未使用的变量为 `_var`
- [ ] 没有为删除的代码添加 `// removed` 注释
- [ ] 没有重新导出未使用的类型
- [ ] 未使用的代码已完全删除

## 评审流程

1. **读取变更文件**
   ```bash
   git diff --cached --name-only
   git diff --cached
   ```

2. **逐项检查清单**
   - 按照上述检查清单逐项验证
   - 标记 🔴 关键问题（必须修复）
   - 标记 🟡 警告问题（建议修复）
   - 标记 🟢 优化建议（可选）

3. **生成评审报告**
   - 列出所有发现的问题
   - 提供具体的修复建议
   - 给出代码示例

4. **修复确认**
   - 如果有问题，要求修复后再次评审
   - 如果通过，允许提交

## 评审报告模板

```markdown
## 代码评审报告

### 📊 概览
- 变更文件数：X
- 新增行数：+X
- 删除行数：-X

### 🔴 关键问题（必须修复）
1. [问题描述]
   - 文件：path/to/file.ts:行号
   - 原因：[说明]
   - 修复建议：[具体方案]

### 🟡 警告问题（建议修复）
1. [问题描述]
   - 文件：path/to/file.ts:行号
   - 建议：[优化方案]

### 🟢 优化建议（可选）
1. [建议描述]

### ✅ 评审结论
- [ ] 通过，可以提交
- [ ] 需要修复后重新评审
```

## 使用示例

```bash
# 用户准备提交代码
git add .

# 触发评审
"请评审我的代码"
"review my changes"
"检查代码是否符合规范"
```

## 注意事项

1. **严格执行关键约束** - 🔴 标记的问题必须修复
2. **提供具体建议** - 不只指出问题，还要给出解决方案
3. **引用具体位置** - 使用 `file:line` 格式引用代码位置
4. **保持客观** - 基于规范评审，不做主观判断
5. **优先级排序** - 先解决关键问题，再处理优化建议
