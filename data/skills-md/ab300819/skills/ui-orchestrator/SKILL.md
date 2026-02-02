---
name: ui-orchestrator
description: UI/UX skill dispatcher that routes to specialized external skills based on project needs. Use when working on UI development, design systems, or frontend tasks. Triggers on keywords like "UI", "界面", "前端", "组件", "animation", "动画", "layout", "布局", "SwiftUI".
allowed-tools: Read, Glob, Bash, AskUserQuestion
---

# UI Orchestrator

UI/UX 技能调度器，根据项目需求路由到专业的外部 Skill。

## Language

- Accept questions in both Chinese and English
- Always respond in Chinese

## 外部 Skill 清单

| Skill | 定位 | 适用场景 | 安装命令 |
|-------|------|----------|----------|
| `baseline-ui` | 代码审查 & 质量守护 | 企业内部系统、代码审查、性能优化 | `npx skills add ibelick/ui-skills` |
| `ui-ux-pro-max` | 设计系统生成 & 决策引擎 | 行业垂直产品、Dashboard、新项目设计 | `npm install -g uipro-cli && uipro init --ai claude` |
| `frontend-design` | 创意美学 & 视觉冲击 | 营销着陆页、品牌官网、创意作品集 | `npx skills add anthropics/skills --skill frontend-design` |
| `swiftui-expert-skill` | SwiftUI 专家指导 | iOS/macOS SwiftUI 开发 | `npx skills add https://github.com/avdlee/swiftui-agent-skill --skill swiftui-expert-skill` |

## 设计哲学光谱

```
保守/安全                    中性/平衡                    大胆/创意
    │                          │                          │
    ▼                          ▼                          ▼
baseline-ui              ui-ux-pro-max              frontend-design

"不出错"                   "符合行业"                  "令人难忘"
```

## 工作流程

```
1. 检测项目需求
   │
   ├── 平台类型（Web / iOS / Android）
   ├── 项目性质（企业 / 创意 / 行业垂直）
   └── 任务类型（新建 / 审查 / 修复）
   │
   ▼
2. 检查 Skill 是否存在
   │
   ├── 存在 → 路由到对应 Skill
   └── 不存在 → 提示安装命令
   │
   ▼
3. 执行对应 Skill
```

## 场景路由表

### 按平台路由

| 平台 | 首选 Skill | 备选 |
|------|-----------|------|
| **SwiftUI** (iOS/macOS) | `swiftui-expert-skill` | - |
| **Web** (React/Vue/HTML) | 见下方按任务路由 | - |
| **Flutter/Compose** | `ui-ux-pro-max` | - |

### 按任务路由（Web）

| 任务类型 | 首选 Skill | 理由 |
|----------|-----------|------|
| **新项目设计系统** | `ui-ux-pro-max` | 生成完整设计系统 |
| **代码审查** | `baseline-ui` | 专为审查设计 |
| **修复无障碍** | `baseline-ui` (`fixing-accessibility`) | 最专业 |
| **修复动画性能** | `baseline-ui` (`fixing-motion-performance`) | 最深入 |
| **营销着陆页** | `frontend-design` | 需要视觉冲击力 |
| **品牌官网** | `frontend-design` | 需要独特识别度 |
| **企业内部系统** | `baseline-ui` | 稳定、可维护 |
| **Dashboard** | `ui-ux-pro-max` → `baseline-ui` | 功能性 + 质量保障 |

### 按项目性质路由

| 项目性质 | 推荐组合 | 使用顺序 |
|----------|---------|----------|
| **创意/营销** | `frontend-design` → `baseline-ui` | 先创意，后审查 |
| **企业/行业** | `ui-ux-pro-max` → `baseline-ui` | 先设计系统，后质量 |
| **内部工具** | `baseline-ui` | 全程约束 |

## Skill 检测

在调用外部 Skill 前，**必须**检测其是否已安装。

### 检测方法

```bash
# 检查 skills 目录（Claude Code）
ls -la ~/.claude/skills/ 2>/dev/null | grep -E "(baseline-ui|ui-ux-pro-max|frontend-design|swiftui-expert)"

# 检查项目本地 skills
ls -la .skills/ 2>/dev/null | grep -E "(baseline-ui|ui-ux-pro-max|frontend-design|swiftui-expert)"
```

### 未安装提示模板

```markdown
**⚠️ 所需 Skill 未安装**

您需要的 `{skill-name}` 尚未安装。请运行以下命令安装：

{install-command}

安装完成后，请重新运行 UI 任务。
```

## 约束

### 调度约束

- [ ] **必须先检测目标 Skill 是否存在**
- [ ] **不存在时必须提示安装命令**
- [ ] **必须根据场景选择合适的 Skill**
- [ ] **禁止复制外部 Skill 的具体规则**

### 路由约束

- [ ] SwiftUI 项目 → 必须路由到 `swiftui-expert-skill`
- [ ] 创意/营销项目 → 优先 `frontend-design`
- [ ] 企业/内部项目 → 优先 `baseline-ui`
- [ ] 新项目设计系统 → 优先 `ui-ux-pro-max`

### 组合使用约束

- [ ] 创意项目完成后，**建议**使用 `baseline-ui` 审查
- [ ] 设计系统生成后，**建议**使用 `baseline-ui` 确保质量

## Skill 协作

| 场景 | 协作 Skill | 说明 |
|------|-----------|------|
| 开发阶段 | `/devdocs-dev-workflow` | 被调用：UI 任务开发时 |
| 代码审查 | `/code-quality` | 协作：UI 代码质量检查 |
| 测试阶段 | `/testing-guide` | 协作：UI 组件测试 |

## 使用示例

### 示例一：SwiftUI 开发

```
用户：帮我优化这个 SwiftUI 视图的性能

Claude：
1. 检测 Skill...
   ✅ swiftui-expert-skill 已安装

2. 路由到 swiftui-expert-skill 处理 SwiftUI 性能优化...
```

### 示例二：新项目设计系统

```
用户：我要做一个医疗行业的 SaaS 产品，帮我设计 UI

Claude：
1. 检测 Skill...
   ❌ ui-ux-pro-max 未安装

⚠️ 所需 Skill 未安装

您需要的 `ui-ux-pro-max` 尚未安装。请运行以下命令安装：

npm install -g uipro-cli && uipro init --ai claude

安装完成后，请重新运行 UI 任务。
```

### 示例三：营销着陆页

```
用户：帮我设计一个有视觉冲击力的产品着陆页

Claude：
1. 检测 Skill...
   ✅ frontend-design 已安装

2. 路由到 frontend-design 处理创意设计...

（设计完成后）

3. 建议：设计完成后，可使用 baseline-ui 进行无障碍和性能审查
```

## 参考资料

- [ibelick/ui-skills](https://github.com/ibelick/ui-skills) - 代码审查 & 质量守护
- [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) - 设计系统生成
- [AvdLee/SwiftUI-Agent-Skill](https://github.com/AvdLee/SwiftUI-Agent-Skill) - SwiftUI 专家指导
- [anthropics/skills/frontend-design](https://github.com/anthropics/skills) - 创意美学 & 视觉冲击
