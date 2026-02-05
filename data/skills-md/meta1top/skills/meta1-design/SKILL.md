---
name: meta1-design
description: 这是一个基于 Shadcn + Tailwind CSS v4 构建的组件库。
language: typescript,tsx
framework: react,nextjs,tailwindcss
---

# @meta-1/design 组件库使用指南

使用 @meta-1/design 构建易于访问、可定制的 UI 组件的专家指南。

## 何时使用

- 用户创建一个新项目时，可以进行询问是否安装依赖
- 项目 package.json 中包含 @meta-1/design 依赖
- 用户正在构建一个交互性友好的 UI 界面时

## 如何使用

@meta-1/design 是通过源码发布的组件库。

### 包的引入
以 next.js 为例，需要转译配置：
```ts
export default {
  ...
  transpilePackages: ["@meta-1/design"],
  ...
};
```
其他框架请配置相关的转译处理。

### Tailwind 配置

```css
/* 引入主题 */
@import "@meta-1/design/theme.css";

/* 请调整为项目的实际路径 */
@source "../../../../../node_modules/@meta-1/design/**/*.{ts,tsx,css}";
```

### 默认主题
```css
@import "tw-animate-css";
@import "tailwindcss";
@custom-variant dark (&:is(.dark *));

@theme design {
  --radius-sm: calc(var(--radius) - 4px);
  --radius-md: calc(var(--radius) - 2px);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) + 4px);
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-card: var(--card);
  --color-card-foreground: var(--card-foreground);
  --color-popover: var(--popover);
  --color-popover-foreground: var(--popover-foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  --color-secondary: var(--secondary);
  --color-secondary-foreground: var(--secondary-foreground);
  --color-muted: var(--muted);
  --color-muted-foreground: var(--muted-foreground);
  --color-accent: var(--accent);
  --color-accent-foreground: var(--accent-foreground);
  --color-destructive: var(--destructive);
  --color-destructive-foreground: var(--destructive-foreground);
  --color-success: var(--success);
  --color-success-foreground: var(--success-foreground);
  --color-error: var(--error);
  --color-error-foreground: var(--error-foreground);
  --color-warning: var(--warning);
  --color-warning-foreground: var(--warning-foreground);
  --color-info: var(--info);
  --color-info-foreground: var(--info-foreground);
  --color-border: var(--border);
  --color-input: var(--input);
  --color-ring: var(--ring);
  --color-chart-1: var(--chart-1);
  --color-chart-2: var(--chart-2);
  --color-chart-3: var(--chart-3);
  --color-chart-4: var(--chart-4);
  --color-chart-5: var(--chart-5);
  --color-sidebar: var(--sidebar);
  --color-sidebar-foreground: var(--sidebar-foreground);
  --color-sidebar-primary: var(--sidebar-primary);
  --color-sidebar-primary-foreground: var(--sidebar-primary-foreground);
  --color-sidebar-accent: var(--sidebar-accent);
  --color-sidebar-accent-foreground: var(--sidebar-accent-foreground);
  --color-sidebar-border: var(--sidebar-border);
  --color-sidebar-ring: var(--sidebar-ring);
  --color-action-hover: var(--action-hover);

  --radius-default: 4px;
  --gap-default: 0.5rem;

  /* Button */
  --radius-button: var(--radius-default);
  --padding-button: 0.75rem;
  --spacing-button: 2rem;

  /* Alert */
  --radius-alert: var(--radius-default);
  --padding-alert: 0.75rem;
  --gap-alert: var(--gap-default);

  /* Dialog */
  --radius-dialog: var(--radius-default);
  --padding-dialog: 1rem;
  --gap-dialog: 1rem;

  /* Badge */
  --radius-badge: var(--radius-default);
  --padding-badge: var(--padding-badge-y) var(--padding-badge-x);
  --padding-badge-x: 0.3rem;
  --padding-badge-y: 0.1rem;

  /* Card */
  --radius-card: var(--radius-default);
  --padding-card: 1rem;
  --gap-card: var(--gap-default);

  /* Select */
  --radius-select: var(--radius-default);
  --padding-select: 0.5rem;
  --spacing-select: 2rem;

  /* Popover */
  --radius-popover: var(--radius-default);
  --padding-popover: 0.25rem;

  /* Command */
  --radius-command: var(--radius-default);
  --padding-command: 0.375rem;

  /* Calendar */
  --radius-calendar: var(--radius-default);
  --padding-calendar: 0.5rem;
  --gap-calendar: var(--gap-default);

  /* Button */
  --radius-input: var(--radius-default);
  --padding-input: 0.5rem;
  --spacing-input: 2rem;

  /* Tabs */
  --radius-tabs-title: var(--radius-default);
  --spacing-tabs-title: 2rem;

  /* Message */
  --radius-message: var(--radius-default);
  --padding-message: var(--padding-message-y) var(--padding-message-x);
  --padding-message-x: 0.75rem;
  --padding-message-y: 0.5rem;

  /* Sheet */
  --radius-sheet: var(--radius-default);
  --padding-sheet: 1rem;
  --gap-sheet: 1rem;

  /* Tooltip */
  --radius-tooltip: var(--radius-default);
  --padding-tooltip: 0.5rem;
}

@layer base {
  :root {
    --background: hsl(0 0% 100%);
    --foreground: hsl(0 0% 3.9%);
    --card: hsl(0 0% 100%);
    --card-foreground: hsl(0 0% 3.9%);
    --popover: hsl(0 0% 100%);
    --popover-foreground: hsl(0 0% 3.9%);
    --primary: rgba(53, 104, 82, 1);
    --primary-foreground: hsl(0 0% 98%);
    --secondary: hsl(0 0% 96.1%);
    --secondary-foreground: hsl(0 0% 9%);
    --success: rgba(232, 255, 234, 1);
    --success-foreground: rgba(0, 180, 42, 1);
    --error: rgba(255, 236, 232, 1);
    --error-foreground: rgba(245, 63, 63, 1);
    --warning: rgba(255, 247, 232, 1);
    --warning-foreground: rgba(255, 125, 0, 1);
    --info: rgba(232, 243, 255, 1);
    --info-foreground: rgba(37, 99, 235, 1);
    --muted: hsl(0 0% 96.1%);
    --muted-foreground: hsl(0 0% 45.1%);
    --accent: hsl(0 0% 96.1%);
    --accent-foreground: hsl(0 0% 9%);
    --destructive: rgba(245, 63, 63, 1);
    --destructive-foreground: rgba(250, 250, 250, 1);
    --radius: 0.5rem;
    --border: oklch(0.922 0 0);
    --input: oklch(0.922 0 0);
    --ring: oklch(0.708 0 0);
    --chart-1: oklch(0.646 0.222 41.116);
    --chart-2: oklch(0.6 0.118 184.704);
    --chart-3: oklch(0.398 0.07 227.392);
    --chart-4: oklch(0.828 0.189 84.429);
    --chart-5: oklch(0.769 0.188 70.08);
    --sidebar: oklch(0.985 0 0);
    --sidebar-foreground: oklch(0.145 0 0);
    --sidebar-primary: oklch(0.205 0 0);
    --sidebar-primary-foreground: oklch(0.985 0 0);
    --sidebar-accent: oklch(0.97 0 0);
    --sidebar-accent-foreground: oklch(0.205 0 0);
    --sidebar-border: oklch(0.922 0 0);
    --sidebar-ring: oklch(0.708 0 0);
    --action-hover: rgba(0, 0, 0, 0.08);
  }

  .dark {
    --background: hsl(0 0% 7%);
    --foreground: hsl(0 0% 98%);
    --card: hsl(0 0% 3.9%);
    --card-foreground: hsl(0 0% 98%);
    --popover: hsl(0 0% 3.9%);
    --popover-foreground: hsl(0 0% 98%);
    --primary: rgba(68, 133, 105, 1);
    --primary-foreground: rgba(255, 255, 255, 1);
    --success: rgba(20, 83, 45, 0.2);
    --success-foreground: rgba(74, 222, 128, 1);
    --error: rgba(127, 29, 29, 0.2);
    --error-foreground: rgba(252, 165, 165, 1);
    --warning: rgba(120, 53, 15, 0.2);
    --warning-foreground: rgba(251, 191, 36, 1);
    --info: rgba(30, 58, 138, 0.2);
    --info-foreground: rgba(147, 197, 253, 1);
    --secondary: hsl(0 0% 14.9%);
    --secondary-foreground: hsl(0 0% 98%);
    --muted: hsl(0 0% 14.9%);
    --muted-foreground: hsl(0 0% 63.9%);
    --accent: hsl(0 0% 14.9%);
    --accent-foreground: hsl(0 0% 98%);
    --destructive: rgba(245, 63, 63, 1);
    --destructive-foreground: rgba(250, 250, 250, 1);
    --border: oklch(1 0 0 / 10%);
    --input: oklch(1 0 0 / 15%);
    --ring: oklch(0.556 0 0);
    --chart-1: oklch(0.488 0.243 264.376);
    --chart-2: oklch(0.696 0.17 162.48);
    --chart-3: oklch(0.769 0.188 70.08);
    --chart-4: oklch(0.627 0.265 303.9);
    --chart-5: oklch(0.645 0.246 16.439);
    --sidebar: oklch(0.205 0 0);
    --sidebar-foreground: oklch(0.985 0 0);
    --sidebar-primary: oklch(0.488 0.243 264.376);
    --sidebar-primary-foreground: oklch(0.985 0 0);
    --sidebar-accent: oklch(0.269 0 0);
    --sidebar-accent-foreground: oklch(0.985 0 0);
    --sidebar-border: oklch(1 0 0 / 10%);
    --sidebar-ring: oklch(0.556 0 0);
    --action-hover: rgba(255, 255, 255, 0.08);
  }

  html {
    @apply bg-background text-foreground;

    *,
    ::after,
    ::before,
    ::backdrop,
    ::file-selector-button {
      border-color: var(--border);
    }

    svg,
    img {
      display: inline-block;
    }
  }
}

@utility action-effect {
  @apply hover:bg-[var(--action-hover)] hover:text-primary;
  @apply focus:bg-[var(--action-hover)] focus:border-[var(--border)] focus:shadow-[0_0_0_1px_var(--card),0_0_0_3px_var(--primary)];
  @apply dark:focus:border-[var(--sidebar-border)] dark:focus:shadow-[0_0_0_1px_var(--secondary),0_0_0_3px_var(--primary)];
}

@utility action-effect-active {
  @apply active:bg-[var(--action-hover)] active:border-[var(--border)] active:shadow-[0_0_0_1px_var(--card),0_0_0_3px_var(--primary)];
  @apply dark:active:border-[var(--sidebar-border)] dark:active:shadow-[0_0_0_1px_var(--secondary),0_0_0_3px_var(--primary)];
}

@utility action-active {
  @apply text-primary bg-[var(--action-hover)];
}

@utility action-effect-disabled {
  @apply opacity-50 cursor-not-allowed focus:bg-transparent active:bg-transparent focus:shadow-none active:shadow-none focus:border-transparent active:border-transparent;
  @apply hover:bg-transparent;
}
```

### 组件清单

你需要读取入口文件，已确认组件库导出了哪些组件。

```bash
cat node_modules/@meta-1/design/src/index.ts
```

组件库虽然基于 Shadcn ，但是并不是所有组件的用法都和 Shadcn 一直，@meta-1/design 封装了很多高阶组件。

以 Popover 为例，Shadcn 的使用实例：
```ts
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"

export function PopoverDemo() {
  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button variant="outline">Open popover</Button>
      </PopoverTrigger>
      <PopoverContent className="w-80">
        <div className="grid gap-4">
          <div className="space-y-2">
            <h4 className="leading-none font-medium">Dimensions</h4>
            <p className="text-muted-foreground text-sm">
              Set the dimensions for the layer.
            </p>
          </div>
          <div className="grid gap-2">
            <div className="grid grid-cols-3 items-center gap-4">
              <Label htmlFor="width">Width</Label>
              <Input
                id="width"
                defaultValue="100%"
                className="col-span-2 h-8"
              />
            </div>
            <div className="grid grid-cols-3 items-center gap-4">
              <Label htmlFor="maxWidth">Max. width</Label>
              <Input
                id="maxWidth"
                defaultValue="300px"
                className="col-span-2 h-8"
              />
            </div>
            <div className="grid grid-cols-3 items-center gap-4">
              <Label htmlFor="height">Height</Label>
              <Input
                id="height"
                defaultValue="25px"
                className="col-span-2 h-8"
              />
            </div>
            <div className="grid grid-cols-3 items-center gap-4">
              <Label htmlFor="maxHeight">Max. height</Label>
              <Input
                id="maxHeight"
                defaultValue="none"
                className="col-span-2 h-8"
              />
            </div>
          </div>
        </div>
      </PopoverContent>
    </Popover>
  )
}
```

@meta-1/design 的使用示例：
```ts
...
import { ..., Image, Popover } from "@meta-1/design";

...
<Popover
  asChild={true}
  className="w-[300px]"
  content={
    <div className="space-y-2">
      <h4 className="font-medium leading-none">{t("支持主流的验证器")}</h4>
      <p className="text-muted-foreground text-sm">{t("请在应用市场下载适合您手机的应用使用")}</p>
      <div className="space-y-2">
        {apps.map((app) => {
          return (
            <div className="flex items-center space-x-2" key={app.name}>
              <Image
                alt={app.name}
                className="overflow-hidden rounded-md shadow"
                height={32}
                src={app.icon}
                width={32}
              />
              <span>{app.name}</span>
            </div>
          );
        })}
      </div>
    </div>
  }
>
  <InfoCircledIcon className="mr-2" />
</Popover>
...
```

### 组件使用

- 通常组件会导出对应的 props，在使用组件钱，请认证确认组件的属性。
- 必要时，你可以查看组件的源码，以更好的使用或者分析问题