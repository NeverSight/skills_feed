---
name: commit-pr-contract
description: |
  用中文生成 commit message（title + body）与 PR 描述，明确区分"长期证据/可追溯性"的 commit 视角和"帮助 reviewer 理解与评审"的 PR 视角。适用于用户请求"写 commit message/写 PR 描述/根据改动生成 commit+PR"，并需遵守 `M-xxx(type): title` 格式与合同式 PR 四块结构；可基于改动描述/代码差异自行推断风险与评审关注点，不足时再询问。
---

# Commit/PR Contract

## 目标
- 生成中文的 commit title/body 与 PR 描述
- 强调 commit 是长期证据，PR 是 reviewer 视角的说明
- 尽量从改动描述/代码差异自行推断风险与 review focus
- 保持简洁、可复用、可追溯

## 工作流
1. 判断输出范围：只 commit、只 PR、或两者都要
2. 收集/补齐最小信息（见下方清单）
3. 优先根据改动描述/代码差异推断风险、验证方式、review focus
4. 识别是否为多主题改动；如是，提示建议拆分 commit（不强制）
5. 生成 commit message（按规则与模板）
6. 生成 PR 描述（按合同式四块结构）
7. 仅在无法推断或影响关键结论时再提问

## 输入最小清单（缺失时询问）
- 改动是什么/为什么
- 影响范围/用户体验变化
- 验证方式（测试/日志/指标/截图）
- 风险与缓解/回滚方式
- Reviewer 重点关注点（1-2 个）
- AI 是否参与
- ticket 编号（M-xxx）与 commit type

## 推断优先级
1. 用户明确提供的信息
2. 变更摘要/代码差异中的事实
3. 明确标注的推断（不要伪造证据）

## 风险与 Review focus 推断提示
- 影响面：是否改动接口/数据结构/配置/权限/支付/计费/安全
- 兼容性：向后兼容、迁移、版本依赖、灰度策略
- 可靠性：异常处理、边界条件、超时/重试、并发/竞态
- 性能：热点路径、N+1、缓存失效、批量规模
- 可观测性：日志/指标/告警是否覆盖关键路径
- 回滚：是否可回退、是否需要数据修复
- 如果能判断风险等级，写出高/中/低并说明原因
- Review focus 只挑 1-2 个最重要的可验证点

## Commit message 规则（长期证据）
- 使用格式：`M-xxx(type): {title}`
- 不臆造 ticket 编号；未知时保留 `M-xxx`
- 从 `feat|fix|inf|chore|test|docs` 选 type；不确定时请求澄清或基于改动推断
- Title 说明"做了什么 + 影响对象"，避免复述 PR 关注点
- Body 仅保留长期有价值的信息，避免评审指令/临时协作细节
- Body 小节按需选用，不强行全写：
  - Why/Context: 变更动机、业务影响
  - What: 关键实现或行为变化
  - Proof: 测试/验证证据（如未验证明确写未验证）
  - Risk: 潜在风险与缓解（仅长期有效信息）
  - Notes: 兼容性/数据迁移/行为差异等
- 多主题改动时，提示"建议拆分 commit"，简述原因

## PR 描述规则（Reviewer 视角）
- 使用四块结构（中文标题）：
  1) 做了什么/为什么（What/Why）
  2) 证明它可行（Proof it works）
  3) 风险与 AI 参与（Risk + AI role）
  4) 评审关注点（Review focus）
- 默认认为 AI 参与；如用户明确未使用 AI，则写"AI 参与：无"
- 风险描述面向评审：影响范围、失败方式、缓解/回滚
- Review focus 要具体、可行动（如"关注 X 边界条件""确认 Y 配置覆盖面"）
- 避免复制 commit body；强调评审理解与验证

## 输出格式
- 先输出 commit title + body（纯文本，无额外标签）
- 空一行
- 再输出 PR 描述四块（用清晰标题/小节）
