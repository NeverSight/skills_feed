---
name: skill-best-practice
description: 检查或验证 Skill 是否符合最佳实践规范，涵盖命名规范、目录结构、元数据完整性、临时文件清理和依赖格式验证，提供详细的检查清单、自动修复建议和报告模板，同时支持技能库文档完整性检查与自动修复，适用于创建或修改 Skill 后的质量验证
---

# Skill 最佳实践检查

## 任务目标
- 本 Skill 用于: 检查或验证 Skill 是否符合规范要求
- 触发条件: 创建或修改 Skill 后需要检查或验证规范符合性

## 操作步骤

### 标准流程

1. **获取检查清单**
   - 阅读 [references/checklist.md](references/checklist.md) 获取完整的 14 项检查清单
   - 清单包含命名规范、SKILL.md 前言区、目录结构、文件清理、依赖元数据五大类检查

2. **逐项检查 Skill**
   - 按照 [references/checklist.md](references/checklist.md) 逐项验证 Skill 目录
   - 记录每个检查项的结果（pass/warning/error）

3. **生成检查报告**
   - 根据 [references/checklist.md#报告格式](references/checklist.md#报告格式) 中的模板生成结构化报告
   - 报告应包含 Skill 名称、总体状态、各检查项详细结果和修复建议

4. **自动修复问题**
   - 优先处理 `error` 级别问题
   - 直接修改不符合规范的文件（SKILL.md、目录结构等）
   - 删除临时文件和冗余文件
   - 修复后重新执行检查清单验证

### 可选分支

- **分组检查**: 当检查项较多时，可按五大类分组检查（命名、结构、元数据、文件、依赖）
- **详细标准**: 需要了解检查标准的详细说明时，阅读 [references/quality-standards.md](references/quality-standards.md)

### 技能库文档完整性检查与自动修复

当需要检查技能库的 README.md 是否完整记录所有技能时。

**检查对象**: 项目根目录下的 `README.md` 和 `skills/` 目录

**检查步骤**:
1. 列出 `skills/` 目录的所有子目录名称
2. 读取 `README.md` 中"## 技能"章节下的表格，提取第一列的技能名称
3. 对比并生成报告：找出遗漏的技能（存在于目录但未在表格中）和冗余的技能（存在于表格但不在目录中）
4. **自动修复**:
   - 对于遗漏的技能：直接在 `README.md` 的"## 技能"章节表格中添加新行
   - 对于冗余的技能：直接在 `README.md` 的"## 技能"章节表格中删除对应行

详细修复流程和自动修复脚本详见 [references/check-report-template.md](references/check-report-template.md)

## 资源索引

- **检查清单**: [references/checklist.md](references/checklist.md)
  - 何时读取: 开始检查前
  - 内容: 完整的 14 项检查项目、通过标准、修复建议、报告格式
- **详细规范**: [references/quality-standards.md](references/quality-standards.md)
  - 何时读取: 需要了解检查标准的详细说明时
  - 内容: 命名规范、目录结构、元数据格式等详细说明
- **报告模板**: [references/check-report-template.md](references/check-report-template.md)
  - 何时读取: 生成技能库文档完整性检查报告时
  - 内容: 完整报告示例、自动修复脚本模板（支持直接修改文件）
