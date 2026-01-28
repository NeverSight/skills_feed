---
name: godot-skills
description: Godot技能统一入口，根据用户需求智能选择并调用最适合的Godot子技能，提供15个专业技能的一站式开发体验
auto_trigger: true
trigger_priority: 1
---

# Godot技能统一入口

## 技能目标

作为所有Godot相关技能的统一入口，根据用户描述智能选择最适合的子技能，并确保在调用任何子技能前MCP连接正常。用户无需了解15个具体技能的功能，系统会自动处理MCP连接状态。

## 🔌 MCP连接管理

### 连接检测
- **自动检测**：每次调用技能前自动检测MCP连接状态
- **连接验证**：通过 `mcp__godot-mcp__get_project_info` 验证连接
- **状态报告**：清晰的连接状态显示

### 自动启动
- **集成auto-launcher**：内置 `godot-mcp-auto-launcher` 功能
- **自动启动**：连接失败时自动启动MCP服务器
- **重试机制**：智能重试和错误恢复

### 严格约束
- **仅使用MCP工具**：所有Godot操作必须通过 `mcp__godot-mcp__*` 工具
- **禁止直接操作**：不能直接读写Godot项目文件
- **安全优先**：确保项目数据安全

## 📚 集成的子技能 (15个)

### 🎯 核心开发技能 (7个)
1. **godot-project-creator** - 项目创建器
2. **godot-gameplay-developer** - 玩法开发
3. **godot-ui-designer** - UI设计器
4. **godot-animation-studio** - 动画工作室
5. **godot-performance-optimizer** - 性能优化器
6. **godot-test-debugger** - 测试调试器
7. **godot-product-polisher** - 产品打磨器

### 🔧 专业功能技能 (5个)
8. **godot-batch-operations** - 批量操作器
9. **godot-camera-system** - 相机系统
10. **godot-material-manager** - 材质管理器
11. **godot-resource-workflow** - 资源工作流
12. **godot-compatibility-checker** - 兼容性检查器

### 📚 支持辅助技能 (3个)
13. **context7-auto-research** - 自动研究员
14. **chinese-dev-guide** - 中文开发指南
15. **gdscript-syntax-guide** - GDScript语法指南

## 🎯 使用方式

用户只需用自然语言描述需求，系统会自动：

1. **检测MCP连接** → 确保Godot通信正常
2. **分析用户意图** → 识别具体需求类型
3. **选择最佳技能** → 智能匹配专业技能
4. **调用子技能** → 执行具体功能(仅通过MCP工具)
5. **返回结果** → 提供详细的处理结果

### MCP连接检测流程
```
用户请求 → 检测MCP连接 → [连接正常] → 继续处理
                ↓
            [连接失败] → 启动MCP服务器 → 重试检测 → 继续处理
                ↓
            [启动失败] → 报告错误 → 提供解决方案
```

### 示例对话

```
用户: 我想创建一个2D平台游戏项目
系统: [MCP检测: 连接正常] → [检测: 项目创建] → 调用godot-project-creator → 生成完整项目架构

用户: 实现角色跳跃和移动机制
系统: [MCP检测: 连接正常] → [检测: 玩法开发] → 调用godot-gameplay-developer → 创建物理系统

用户: 设计血条和主菜单界面
系统: [MCP检测: 连接正常] → [检测: UI设计] → 调用godot-ui-designer → 创建界面布局

用户: 优化游戏性能，提升帧率
系统: [MCP检测: 连接正常] → [检测: 性能优化] → 调用godot-performance-optimizer → 分析并优化

# 如果MCP未连接的情况
用户: 修复这个兼容性问题
系统: [MCP检测: 连接失败] → [启动MCP服务器] → [重试检测成功] → [检测: 兼容性] → 调用兼容性检查器
```

## 🧠 智能匹配规则

### 项目创建类
关键词：创建、新建、项目、初始化、开始、project、create、setup
→ 选择：godot-project-creator

### 玩法开发类
关键词：玩法、逻辑、机制、系统、功能、gameplay、logic、mechanic、feature
→ 选择：godot-gameplay-developer

### UI设计类
关键词：界面、UI、菜单、按钮、交互、interface、menu、hud、dialog
→ 选择：godot-ui-designer

### 动画特效类
关键词：动画、特效、粒子、资源、animation、effects、particles、visual
→ 选择：godot-animation-studio

### 性能优化类
关键词：性能、优化、帧率、内存、适配、performance、optimize、fps
→ 选择：godot-performance-optimizer

### 测试调试类
关键词：测试、调试、错误、bug、test、debug、unit、integration
→ 选择：godot-test-debugger

### 兼容性检查类
关键词：兼容性、版本、迁移、API、version、migration、upgrade
→ 选择：godot-compatibility-checker

### 文档研究类
关键词：文档、研究、API、查询、documentation、research、latest
→ 选择：context7-auto-research

### 中文支持类
关键词：中文、本地化、双语、环境、chinese、localization
→ 选择：chinese-dev-guide

### 语法指南类
关键词：语法、GDScript、规范、代码、syntax、gdscript、style
→ 选择：gdscript-syntax-guide

## 🔧 技能目录结构

```
godot-skills/
├── SKILL.md                    # 主技能定义
├── sub-skills/                 # 子技能目录 (15个专业技能)
│   ├── godot-project-creator/
│   ├── godot-gameplay-developer/
│   ├── godot-ui-designer/
│   ├── godot-animation-studio/
│   ├── godot-performance-optimizer/
│   ├── godot-test-debugger/
│   ├── godot-product-polisher/
│   ├── godot-batch-operations/
│   ├── godot-camera-system/
│   ├── godot-material-manager/
│   ├── godot-resource-workflow/
│   ├── godot-compatibility-checker/
│   ├── context7-auto-research/
│   ├── chinese-dev-guide/
│   ├── gdscript-syntax-guide/
│   └── skill-creator_技能创建器/
```

## 🔧 MCP错误处理

### 连接失败处理
- **自动重试**：MCP连接失败时自动重试3次
- **启动MCP**：重试失败时调用 `godot-mcp-auto-launcher` 启动服务器
- **端口检测**：支持9080和9081端口的自动检测
- **错误诊断**：提供详细的错误信息和解决方案

### 常见问题解决
```
问题1: "MCP连接失败"
解决: 自动启动MCP服务器，检测端口占用

问题2: "Godot编辑器未启动"
解决: 提醒用户启动Godot编辑器并启用MCP插件

问题3: "权限不足"
解决: 提供权限配置指导和解决方案
```

## ⚠️ 重要规则

### MCP工具使用约束
- **仅使用MCP工具**：所有Godot操作必须通过 `mcp__godot-mcp__*` 工具
- **禁止直接文件操作**：不能直接读写Godot项目文件(.tscn, .gd, .tres等)
- **安全优先**：确保项目数据安全，避免意外修改
- **工具验证**：每次操作前验证MCP工具可用性

### 技能设计原则
- **不依赖外部包**：仅使用技能系统提供的功能
- **纯技能调用**：通过Skill工具调用子技能
- **智能路由**：基于关键词和模式匹配选择技能
- **容错处理**：提供后备技能建议和错误恢复

### MCP强制检查
- **连接前置**：任何Godot操作前必须检测MCP连接
- **工具验证**：验证所有MCP工具的可用性
- **状态报告**：实时报告MCP连接状态
- **自动恢复**：连接失败时自动尝试恢复

## 🎯 技能触发模式

### 自动触发条件
- 检测到Godot相关关键词
- 提到游戏开发、UI设计、性能优化等
- 需要项目创建或功能实现
- **MCP连接检测**(最高优先级)

### 触发优先级
1. **MCP连接检测** - 每次调用前必须执行
2. **意图识别** - 分析用户具体需求
3. **技能匹配** - 选择最适合的子技能
4. **容错处理** - 提供后备方案

### MCP前置检查流程
```
用户请求 → [强制] MCP连接检测 → [成功] 意图分析 → 技能执行
                          ↓
                      [失败] 启动MCP → 重试检测 → 意图分析
                          ↓
                      [启动失败] 错误报告 → 解决方案
```

### 后备机制
- **MCP连接失败**：自动调用godot-mcp-auto-launcher
- **技能匹配失败**：提供相关技能列表
- **用户手动选择**：允许指定特定技能
- **错误恢复**：提供详细的使用建议

### MCP工具验证列表
- `mcp__godot-mcp__get_project_info` - 项目信息获取
- `mcp__godot-mcp__create_node` - 节点创建
- `mcp__godot-mcp__update_node_property` - 节点属性更新
- `mcp__godot-mcp__create_script` - 脚本创建
- `mcp__godot-mcp__open_scene` - 场景打开
- 其他相关MCP工具...

---

**目标**: 为Godot开发者提供最便捷的技能统一入口，让复杂的开发工作变得简单高效！