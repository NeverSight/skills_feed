---
name: kwc-lwc-development
description: 本项目的前端开发专家。负责处理所有代码编写、组件修改、页面构建及咨询任务。在处理相关任务前，**请先检查本 Skill 是否已加载**；若尚未加载，则**必须**优先调用。本 Skill 内置了项目特定的环境检测逻辑，会自动识别 KWC LWC 架构（检查 .kd 目录等）并应用强制性的开发规范（即本 Skill 目录下的 rule.md）。无论用户问题是否包含特定关键词，只要涉及代码开发，都应确保此 Skill 处于激活状态以保证合规。
---

# KWC LWC 开发专家

本 Skill 是 KWC LWC 项目开发的**入口与总指挥**。

## 核心职责
你负责指导用户进行 KWC LWC 组件的开发、修改和维护。
**重要**：你必须严格遵守**本 Skill 目录下的** `rule.md` 文件中定义的硬性约束。在开始任何代码编写前，请务必阅读并理解这些规则。

## 1. 环境上下文确认
- **项目根目录**：包含 `.kd` 文件夹和 `app/kwc` 目录。
- **配置环境**：`.kd/config.json` 中 `framework` 配置为 `lwc`。
- **重要**：若当前环境**不满足**上述条件（如缺少 `.kd` 或 `framework` 不为 `lwc`），**必须立即停止**使用本 Skill 的所有约束，转而按**通用 Web 项目**标准协助用户。
- **执行原则**：仅在确认环境符合上述特征时，才强制执行本 Skill 及**本 Skill 目录下的** `rule.md` 定义的所有 KWC LWC 开发规范。

## 2. 平台差异说明 (Salesforce LWC vs @kdcloudjs/kwc)
`@kdcloudjs/kwc` 是 Salesforce LWC 的 100% 语法克隆，仅有以下差异需要注意：

| 项目 | Salesforce LWC | @kdcloudjs/kwc（本平台） |
|-----|---------------|------------------------|
| **基类** | `LightningElement` | `KingdeeElement` |
| **导入路径** | `from 'lwc'` | `from '@kdcloudjs/kwc'` |
| **配置文件** | `lwc.config.json` | `kwc.config.json` |
| **组件库** | `<lightning-button>` 等 | `<sl-button kwc:external>` 等（必须使用 `kwc:external` 属性，禁止直接使用 `lightning-*` 组件） |
| **平台限制** | 支持标准 LWC 语法 | HTML 中禁止表达式、禁止自闭合标签、Shoelace自定义事件在renderedCallback中绑定监听 |

## 3. 标准工作流 (Workflow)

1. **新建组件**：
   - **必须**使用 CLI 工具，严禁手工创建文件：
     ```bash
     kd project create [组件名] --type kwc
     ```
   - 组件命名遵循 `camelCase`。

2. **代码实现与修改**：
   - **必须先参考**：在实现前，**必须**先阅读并参考项目根目录下的 `app/kwc/exampleComponent` 或本 Skill 目录下的 `./assets/examples` 示例代码，确保掌握正确的开发模式。
   - **严格合规**：代码必须符合**本 Skill 目录下的** `rule.md` 中的所有约束（html无表达式、无自闭合、正确的事件绑定等）。
   - **Shoelace 集成**：涉及 Shoelace 组件时，确保导入路径正确且添加了 `kwc:external`。

3. **验证与交付**：
   - 按项目入口更新 `app/kwc/main*` 引用。
   - 运行 `npm run dev` 进行验证。
   - 检查代码是否符合所有硬性约束。

## 4. 关键约束摘要 (详细请见本 Skill 目录下的 rule.md)
以下仅列出最关键的几点，完整规则请查阅**本 Skill 目录下的** `rule.md`：
- **模板**：禁止 JS 表达式 (`{a+b}`)，禁止自闭合 (`<tag />`)，禁止 ID 选择器。
- **事件**：HTML 仅绑定原生事件 (`click`)，Shoelace 事件 (`sl-change`) 必须在 JS `renderedCallback` 中绑定。
- **Shoelace**：`sl-*` 标签必须加 `kwc:external`，属性全小写。
- **JS**：继承 `KingdeeElement`，DOM 查询用 `.class`。
- **CSS**：样式必须使用 Shoelace Design Token（`var(--sl-color-*)`、`var(--sl-spacing-*)`、`var(--sl-font-size-*)`、`var(--sl-border-radius-*)`），禁止硬编码 hex 色值和 px 数值。详见 `./reference/css-design-tokens.md`。

## 5. 常用资源
- 基类：`KingdeeElement` (`@kdcloudjs/kwc`)
- 组件库：`@kdcloudjs/shoelace`
  - **说明**：该库是 `@shoelace-style/shoelace` 的 **100% 克隆**，标准组件 API 完全一致，仅新增了 KWC 业务组件。
  - **标准组件文档**：[https://shoelace.style/](https://shoelace.style/)
- **所有扩展组件文档**（位于本 Skill 的 `reference/` 目录下）：
  - Table: `reference/table/index.md`
  - DatePicker: `reference/datepicker/index.md`
  - TimePicker: `reference/sl-timepicker.md`
  - Pagination: `reference/sl-pagination.md`
  - **使用前必须阅读相应文档**。

## 6. 输出检查清单
提交代码前，请自查：
- [ ] 新建组件使用了 `kd project create [组件名] --type kwc`
- [ ] 已阅读并遵守**本 Skill 目录下的** `rule.md` 中的所有约束
- [ ] HTML 无 JS 表达式、无自闭合标签、无 ID
- [ ] `sl-*` 标签包含 `kwc:external`
- [ ] Shoelace自定义事件在 JS 中绑定，HTML 仅绑定原生事件
- [ ] CSS 样式使用 Design Token，无硬编码色值/间距/字号/圆角
- [ ] **未运行**任何 ESLint/Prettier 修复命令，并**忽略**了所有 ESLint 格式报错
