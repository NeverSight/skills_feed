---
name: frontend-design
version: "1.0"
status: production
layer: skill
owner: wade
last_reviewed: 2026-01-02

description: >
  前端设计指导 Skill，用于 UI 组件设计、界面布局、设计系统一致性审查、
  CSS/Tailwind 优化、响应式设计和可访问性检查。当需要进行 UI 设计决策、
  组件结构规划、设计审查或样式优化时使用此 Skill。

sot_dependencies:
  required:
    - docs/3.dev-guides/UI_DESIGN_SYSTEM.md
    - docs/3.dev-guides/COMPONENT_REGISTRY.md
  optional:
    - docs/3.dev-guides/FRONTEND_DEVELOPMENT_RULES.md
    - docs/3.dev-guides/UI_FLOW_SPEC.md

output_boundaries:
  writable:
    - frontend/src/components/**
    - frontend/src/modules/**/components/**
    - frontend/src/styles/**
  forbidden:
    - frontend/node_modules/**
    - frontend/.next/**

allowed-tools: Read, Grep, Glob, Write, Edit
---

# Frontend Design Skill - 前端设计指导

## 1. Purpose

提供前端 UI/UX 设计指导，确保设计系统一致性、组件可复用性和用户体验质量。

**核心职责**:
- UI 组件设计和结构规划
- 设计系统一致性审查
- 响应式设计和布局优化
- 可访问性 (a11y) 检查
- CSS/Tailwind 最佳实践

## 2. Design Principles

### 2.1 设计系统核心原则

| 原则 | 描述 | 检查点 |
|------|------|--------|
| **一致性** | 统一的视觉语言和交互模式 | 颜色、间距、字体、圆角 |
| **层次感** | 清晰的信息层级和视觉重点 | 标题大小、颜色对比、空间分布 |
| **可预测** | 用户可预期的交互行为 | 按钮反馈、加载状态、错误提示 |
| **可访问** | 符合 WCAG 2.1 AA 标准 | 对比度、键盘导航、屏幕阅读器 |

### 2.2 颜色系统

```css
/* 主色调 - 品牌色 */
--primary: hsl(222, 47%, 11%);      /* 深蓝 */
--primary-foreground: hsl(0, 0%, 100%);

/* 语义色 */
--success: hsl(142, 71%, 45%);      /* 绿色 - 成功 */
--warning: hsl(38, 92%, 50%);       /* 橙色 - 警告 */
--destructive: hsl(0, 84%, 60%);    /* 红色 - 危险/错误 */

/* 中性色 */
--muted: hsl(210, 40%, 96%);
--muted-foreground: hsl(215, 16%, 47%);
```

### 2.3 间距系统

```css
/* Tailwind 间距规范 */
spacing-1: 0.25rem (4px)   /* 紧凑元素间距 */
spacing-2: 0.5rem  (8px)   /* 小间距 */
spacing-4: 1rem    (16px)  /* 标准间距 */
spacing-6: 1.5rem  (24px)  /* 卡片内边距 */
spacing-8: 2rem    (32px)  /* 区块间距 */
```

### 2.4 字体层级

| 级别 | Tailwind Class | 使用场景 |
|------|---------------|---------|
| H1 | `text-2xl font-bold` | 页面标题 |
| H2 | `text-xl font-semibold` | 区块标题 |
| H3 | `text-lg font-medium` | 卡片标题 |
| Body | `text-sm` | 正文 |
| Caption | `text-xs text-muted-foreground` | 辅助说明 |

## 3. Component Patterns

### 3.1 页面布局模式

```tsx
// 标准页面结构
<div className="space-y-6">
  {/* 页面头部 */}
  <div className="flex items-center justify-between">
    <h1 className="text-2xl font-bold">页面标题</h1>
    <Button>主操作</Button>
  </div>

  {/* 筛选区域 */}
  <Card>
    <CardHeader>
      <CardTitle className="text-lg">筛选条件</CardTitle>
    </CardHeader>
    <CardContent>
      {/* 筛选组件 */}
    </CardContent>
  </Card>

  {/* 内容区域 */}
  <Card>
    <CardContent className="pt-6">
      {/* 主体内容 */}
    </CardContent>
  </Card>
</div>
```

### 3.2 卡片组件模式

```tsx
// 数据卡片
<Card>
  <CardHeader className="pb-2">
    <CardTitle className="text-sm font-medium text-muted-foreground">
      标题
    </CardTitle>
  </CardHeader>
  <CardContent>
    <div className="text-2xl font-bold">数值</div>
    <p className="text-xs text-muted-foreground">
      辅助说明
    </p>
  </CardContent>
</Card>

// KPI 指标卡
<div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
  <MetricCard title="总收入" value="¥125,000" change="+12.5%" />
  <MetricCard title="总成本" value="¥98,000" change="-5.2%" />
  <MetricCard title="毛利" value="¥27,000" />
  <MetricCard title="CPL" value="¥45.5" />
</div>
```

### 3.3 表格组件模式

```tsx
// 使用 DataTable 组件
import { DataTable } from "@/components/ui/data-table/DataTable";

const columns = [
  { accessorKey: "id", header: "ID" },
  { accessorKey: "name", header: "名称" },
  {
    accessorKey: "status",
    header: "状态",
    cell: ({ row }) => (
      <StatusBadge status={row.original.status} />
    ),
  },
  {
    id: "actions",
    cell: ({ row }) => (
      <DropdownMenu>
        {/* 操作菜单 */}
      </DropdownMenu>
    ),
  },
];

<DataTable columns={columns} data={data} />
```

### 3.4 表单组件模式

```tsx
// 使用 react-hook-form + zod
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

const schema = z.object({
  name: z.string().min(1, "名称不能为空"),
  amount: z.number().positive("金额必须大于 0"),
});

function MyForm() {
  const form = useForm({
    resolver: zodResolver(schema),
    defaultValues: { name: "", amount: 0 },
  });

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>名称</FormLabel>
              <FormControl>
                <Input {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">提交</Button>
      </form>
    </Form>
  );
}
```

## 4. State Display Patterns

### 4.1 状态标签 (StatusBadge)

```tsx
// 状态颜色映射 - 对齐设计系统
const statusVariants = {
  // 日报状态
  raw_submitted: { label: "已提交", variant: "outline" },
  trend_ok: { label: "趋势正常", variant: "secondary" },
  final_confirmed: { label: "已确认", variant: "default" },

  // 充值状态
  pending: { label: "待处理", variant: "outline" },
  approved: { label: "已批准", variant: "default" },
  rejected: { label: "已拒绝", variant: "destructive" },

  // 账户状态
  active: { label: "活跃", variant: "default" },
  suspended: { label: "暂停", variant: "warning" },
  dead: { label: "死号", variant: "destructive" },
};
```

### 4.2 加载和错误状态

```tsx
// 使用 DataStateManager 组件
import { DataStateManager } from "@/components/ui/data-state-manager";

<DataStateManager
  isLoading={isLoading}
  error={error}
  isEmpty={!data?.length}
  loadingComponent={<TableSkeleton rows={5} />}
  errorComponent={<ErrorMessage message={error?.message} />}
  emptyComponent={<EmptyState message="暂无数据" />}
>
  <DataTable columns={columns} data={data} />
</DataStateManager>
```

## 5. Responsive Design

### 5.1 断点系统

| 断点 | 尺寸 | 适用设备 |
|------|------|---------|
| `sm` | 640px | 手机横屏 |
| `md` | 768px | 平板竖屏 |
| `lg` | 1024px | 平板横屏/小笔记本 |
| `xl` | 1280px | 桌面 |
| `2xl` | 1536px | 大屏桌面 |

### 5.2 响应式布局模式

```tsx
// 网格布局
<div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
  {/* 卡片组件 */}
</div>

// 侧边栏布局
<div className="flex flex-col lg:flex-row gap-6">
  <aside className="w-full lg:w-64 shrink-0">
    {/* 侧边栏 */}
  </aside>
  <main className="flex-1">
    {/* 主内容 */}
  </main>
</div>

// 隐藏/显示
<Button className="hidden md:inline-flex">桌面按钮</Button>
<Button className="md:hidden">移动按钮</Button>
```

## 6. Accessibility Checklist

### 6.1 基础要求

- [ ] 所有交互元素可通过键盘访问
- [ ] 焦点顺序合理且可见
- [ ] 颜色对比度 >= 4.5:1 (正文) / 3:1 (大文本)
- [ ] 表单元素有关联的 label
- [ ] 图片有 alt 属性

### 6.2 ARIA 使用

```tsx
// 加载状态
<div aria-busy={isLoading} aria-live="polite">
  {isLoading ? <Spinner /> : <Content />}
</div>

// 对话框
<Dialog>
  <DialogContent aria-labelledby="dialog-title" aria-describedby="dialog-desc">
    <DialogTitle id="dialog-title">标题</DialogTitle>
    <DialogDescription id="dialog-desc">描述</DialogDescription>
  </DialogContent>
</Dialog>

// 按钮
<Button aria-label="删除项目">
  <TrashIcon />
</Button>
```

## 7. Design Review Checklist

### 7.1 视觉一致性检查

| 检查项 | 验证方法 | 优先级 |
|--------|---------|--------|
| 颜色使用 | 对照颜色系统变量 | P0 |
| 间距一致 | 使用 Tailwind 标准间距 | P0 |
| 字体层级 | 对照字体规范 | P0 |
| 圆角一致 | 统一使用 `rounded-md` | P1 |
| 阴影一致 | Card 使用 `shadow-sm` | P1 |

### 7.2 交互设计检查

| 检查项 | 验证方法 | 优先级 |
|--------|---------|--------|
| 按钮反馈 | hover/active/disabled 状态 | P0 |
| 加载状态 | 有明确的加载指示 | P0 |
| 错误提示 | 用户友好的错误信息 | P0 |
| 成功反馈 | Toast 或状态更新 | P1 |

### 7.3 组件复用检查

| 检查项 | 验证方法 | 优先级 |
|--------|---------|--------|
| 使用注册组件 | 对照 COMPONENT_REGISTRY.md | P0 |
| 避免重复造轮子 | 检查现有组件库 | P0 |
| Props 接口一致 | 使用标准化 Props | P1 |

## 8. Anti-Patterns (禁止模式)

### 8.1 样式禁止

```tsx
// ❌ 内联样式
<div style={{ color: "red", marginTop: 20 }}>

// ✅ Tailwind 类
<div className="text-destructive mt-5">

// ❌ 硬编码颜色值
<div className="bg-[#ff0000]">

// ✅ 使用语义化变量
<div className="bg-destructive">

// ❌ 魔法数字
<div className="w-[347px] h-[89px]">

// ✅ 使用标准尺寸
<div className="w-80 h-24">
```

### 8.2 组件禁止

```tsx
// ❌ 手写表格
<table>
  <thead>...</thead>
  <tbody>...</tbody>
</table>

// ✅ 使用 DataTable
<DataTable columns={columns} data={data} />

// ❌ 自定义 Loading
<div className="spinner animate-spin">...</div>

// ✅ 使用 Skeleton 或 Loader
<Skeleton className="h-8 w-full" />

// ❌ 手写 Modal
<div className="fixed inset-0 z-50">...</div>

// ✅ 使用 Dialog
<Dialog>
  <DialogContent>...</DialogContent>
</Dialog>
```

## 9. Prompt Template

```xml
<SYSTEM>
你是"前端设计 Agent"，负责 UI/UX 设计决策和组件结构规划。

必须遵守的规则：
1. 遵循 UI_DESIGN_SYSTEM.md 设计规范
2. 使用 COMPONENT_REGISTRY.md 中的注册组件
3. 优先使用 shadcn/ui 和 Tailwind CSS
4. 确保响应式设计和可访问性
5. 保持设计系统一致性

技术栈：
- React 18+ / Next.js 14+
- Tailwind CSS
- shadcn/ui 组件库
- TypeScript
</SYSTEM>

<CONTEXT>
<DOC name="UI_DESIGN_SYSTEM">
{{UI_DESIGN_SYSTEM}}
</DOC>

<DOC name="COMPONENT_REGISTRY">
{{COMPONENT_REGISTRY}}
</DOC>
</CONTEXT>

<TASK>
{{TASK}}
</TASK>

<THINKING_CHAIN>
1. **需求分析**
   - 理解设计目标和用户场景
   - 识别需要的组件和布局

2. **设计系统检查**
   - 对照颜色、间距、字体规范
   - 确认可用的组件

3. **组件规划**
   - 选择合适的组件
   - 规划组件层次和数据流

4. **响应式考虑**
   - 确定断点策略
   - 规划不同屏幕布局

5. **可访问性检查**
   - 确保键盘可访问
   - 添加必要的 ARIA 属性

6. **输出设计方案**
   - 提供代码示例
   - 说明设计决策
</THINKING_CHAIN>
```

## 10. Version History

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-01-02 | 初始版本 |

---

**文档控制**: Owner: wade | Baseline: UI_DESIGN_SYSTEM.md, COMPONENT_REGISTRY.md
