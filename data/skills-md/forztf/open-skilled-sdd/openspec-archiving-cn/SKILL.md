---
name: openspec-archiving-cn
description: 归档已完成的变更并将规范差异合并到常驻文档。用于变更已部署、准备归档或实施后需要更新规范时。触发词包括 "openspec归档", "归档", "归档提案", "合并规范", "完成提案", "更新文档", "定稿规范", "标记完成"。
---

# 规范归档

归档已完成的变更提案，并将其规范差异合并到常驻规范文档中。

## 快速开始

归档包含两项主要操作：
1. **移动变更目录**至带时间戳的归档位置
2. **合并规范差异**到常驻规范（ADDED/MODIFIED/REMOVED）

**关键规则**：在归档前验证所有任务已完成。归档意味着已部署且完成。

## 工作流

复制此清单并跟踪进度：

```
归档进度:
- [ ] 第 1 步：验证实施完成
- [ ] 第 2 步：审阅待合并的规范差异
- [ ] 第 3 步：创建带时间戳的归档目录
- [ ] 第 4 步：合并 ADDED 需求到常驻规范
- [ ] 第 5 步：合并 MODIFIED 需求到常驻规范
- [ ] 第 6 步：合并 REMOVED 需求到常驻规范
- [ ] 第 7 步：移动变更目录到归档
- [ ] 第 8 步：验证常驻规范结构
```

### 第 1 步：验证实施完成

在归档前确认所有工作已完成：

```bash
# 检查 IMPLEMENTED 标记
test -f spec/changes/{change-id}/IMPLEMENTED && echo "✓ 已实施" || echo "✗ 未实施"

# 查看任务
cat spec/changes/{change-id}/tasks.json

# 使用 git 检查未提交工作
git status
```

**询问用户**：
```markdown
所有任务是否已完成并通过测试？
该变更是否已部署到生产？
是否继续归档？
```

### 第 2 步：审阅待合并的规范差异

了解需要合并的内容：

```bash
# 列出所有规范差异文件
find spec/changes/{change-id}/specs -name "*.md" -type f

# 读取每个差异文件
for file in spec/changes/{change-id}/specs/**/*.md; do
    echo "=== $file ==="
    cat "$file"
done
```

**识别**：
- 哪些能力受到影响
- ADDED/MODIFIED/REMOVED 各有多少需求
- 这些变更在常驻规范中的归属位置

### 第 3 步：创建带时间戳的归档目录

```bash
# 以当天日期创建归档目录
TIMESTAMP=$(date +%Y-%m-%d)
mkdir -p spec/archive/${TIMESTAMP}-{change-id}
```

**示例**：
```bash
# 对 2025-10-26 归档的 "add-user-auth" 变更
mkdir -p spec/archive/2025-10-26-add-user-auth
```

### 第 4 步：合并 ADDED 需求到常驻规范

对每个 `## ADDED Requirements` 部分：

**流程**：
1. 定位目标常驻规范文件
2. 将新增需求追加到文件末尾
3. 保持正确的 Markdown 格式

**示例**：

**来源**（`spec/changes/add-user-auth/specs/authentication/spec-delta.md`）：
```markdown
## ADDED Requirements

### Requirement: 用户登录
WHEN 用户提交有效凭据,
系统 SHALL 认证用户并创建会话。

#### Scenario: 登录成功
GIVEN 有效的凭据
WHEN 用户提交登录表单
THEN 系统创建会话
```

**目标**（`spec/specs/authentication/spec.md`）：
```bash
# 追加到常驻规范
cat >> spec/specs/authentication/spec.md << 'EOF'

### Requirement: 用户登录
WHEN 用户提交有效凭据,
系统 SHALL 认证用户并创建会话。

#### Scenario: 登录成功
GIVEN 有效的凭据
WHEN 用户提交登录表单
THEN 系统创建会话
EOF
```

### 第 5 步：合并 MODIFIED 需求到常驻规范

对每个 `## MODIFIED Requirements` 部分：

**流程**：
1. 在常驻规范中定位现有需求
2. 替换**整个**需求块（包括全部场景）
3. 使用差异文件中的完整更新文本

**示例（使用 sed）**：

```bash
# 查找并替换需求块
# 这是概念示例——实际实现取决于结构

# 首先，确定旧需求的起始行
START_LINE=$(grep -n "### Requirement: 用户登录" spec/specs/authentication/spec.md | cut -d: -f1)

# 查找结束位置（下一个需求或文件末尾）
END_LINE=$(tail -n +$((START_LINE + 1)) spec/specs/authentication/spec.md | \
           grep -n "^### Requirement:" | head -1 | cut -d: -f1)

# 删除旧需求
sed -i "${START_LINE},${END_LINE}d" spec/specs/authentication/spec.md

# 在相同位置插入新需求
#（从差异文件提取并插入）
```

**手动方式**（出于安全建议）：
```markdown
1. 在编辑器中打开常驻规范
2. 通过名称查找目标需求
3. 删除整个块（需求 + 所有场景）
4. 将差异文件中的更新需求粘贴到该处
5. 保存
```

### 第 6 步：合并 REMOVED 需求到常驻规范

对每个 `## REMOVED Requirements` 部分：

**流程**：
1. 在常驻规范中定位该需求
2. 删除整个需求块
3. 添加一条注释记录移除

**示例**：

```bash
# 方案 1：带注释删除
# 手动编辑 spec/specs/authentication/spec.md

# 添加弃用注释
echo "<!-- Requirement 'Legacy Password Reset' removed $(date +%Y-%m-%d) -->" >> spec/specs/authentication/spec.md

# 通过手动或 sed 删除该需求块
```

**模式**：
```markdown
<!-- Removed 2025-10-26: 用户需使用基于邮件的密码重置 -->
~~### Requirement: SMS Password Reset~~
```

### 第 7 步：将变更目录移动到归档

在所有差异合并后：

```bash
# 将完整的变更目录移动到归档
mv spec/changes/{change-id} spec/archive/${TIMESTAMP}-{change-id}
```

**验证移动成功**：
```bash
# 检查归档是否存在
ls -la spec/archive/${TIMESTAMP}-{change-id}

# 检查 changes 目录是否干净
ls spec/changes/ | grep "{change-id}"  # 应无结果
```

### 第 8 步：验证常驻规范结构

在合并后，验证常驻规范的完整性：

```bash
# 检查需求格式
grep -n "### Requirement:" spec/specs/**/*.md

# 检查场景格式
grep -n "#### Scenario:" spec/specs/**/*.md

# 统计每个规范中的需求数量
for spec in spec/specs/**/spec.md; do
    count=$(grep -c "### Requirement:" "$spec")
    echo "$spec: $count 条需求"
done
```

**手动审阅**：
- 打开每个被修改的规范文件
- 验证 Markdown 格式正确
- 检查需求逻辑是否连贯
- 确保不存在重复需求

## 合并逻辑参考

### ADDED 操作

```
动作：追加到常驻规范
位置：文件末尾（任何页脚/附录之前）
格式：按原文复制需求与全部场景
```

### MODIFIED 操作

```
动作：替换现有需求
位置：通过需求名称定位，替换整个块
格式：使用差异文件的完整更新文本（不拼接，直接替换）
说明：旧版本保留在归档中
```

### REMOVED 操作

```
动作：删除需求，并添加弃用注释
位置：通过需求名称定位
格式：删除整个块，可选添加 <!-- Removed YYYY-MM-DD: reason -->
```

### RENAMED 操作（不常见）

```
动作：更新需求名称，保留内容
位置：通过旧名称定位，更新为新名称
格式：仅修改标题：### Requirement: 新名称
说明：通常使用 MODIFIED 更为常见
```

## 最佳实践

### 模式 1：移动前先验证

**务必**在移动到归档前验证差异合并：

```bash
# 合并后查看差异
git diff spec/specs/

# 审阅变更
git diff spec/specs/authentication/spec.md

# 若正确则提交
git add spec/specs/
git commit -m "Merge spec deltas from add-user-auth"

# 然后再归档
mv spec/changes/add-user-auth spec/archive/2025-10-26-add-user-auth
```

### 模式 2：原子化归档

归档整个变更，而非单个文件：

**好**：
```bash
# 移动完整变更目录
mv spec/changes/add-user-auth spec/archive/2025-10-26-add-user-auth
```

**坏**：
```bash
# 不要挑拣文件
mv spec/changes/add-user-auth/proposal.md spec/archive/
#（会留下孤儿文件）
```

### 模式 3：归档保全

归档是历史记录。切勿修改归档文件：

```markdown
❌ 不要：编辑 spec/archive/
✓ 要：将归档视为只读历史
```

### 模式 4：Git 提交策略

推荐提交流程：

```bash
# 提交 1：合并差异
git add spec/specs/
git commit -m "Merge spec deltas from add-user-auth

- Added User Login requirement
- Modified Password Policy requirement
- Removed Legacy Auth requirement"

# 提交 2：归档变更
git add spec/archive/ spec/changes/
git commit -m "Archive add-user-auth change"
```

## 进阶主题

**复杂差异**：见 [reference/MERGE_LOGIC.md](reference/MERGE_LOGIC.md)

**冲突解决**：若多个变更修改同一需求，需手动合并。

**回滚策略**：若需回滚归档，反向执行流程（从归档移回 changes，并从常驻规范移除已合并内容）。

## 常见模式

### 模式 1：简单新增

```markdown
变更新增 1 条需求 → 追加到规范 → 归档
```

### 模式 2：行为变更

```markdown
变更修改 1 条需求 → 在规范中替换 → 归档
```

### 模式 3：弃用

```markdown
变更移除 1 条需求 → 删除并添加注释 → 归档
```

### 模式 4：多需求的功能

```markdown
变更在 2 个规范中新增 5 条需求
→ 分别追加到相应规范
→ 验证全部已合并
→ 归档
```

## 反模式避免

**不要**：
- 归档未完成的实施
- 在部署前合并差异
- 修改归档文件
- 跳过合并后的验证
- 忘记在合并规范后进行 git 提交

**要**：
- 在归档前验证所有任务完成
- 小心且完整地合并差异
- 将归档视为不可变历史
- 验证合并后规范结构
- 在归档移动前提交合并后的规范

## 故障排查

### 问题：合并冲突（常驻规范已有该需求）

**解决方案**：
```markdown
1. 若名称相同但内容不同 → 使用 MODIFIED 模式
2. 若确实是不同需求 → 重命名其中之一
3. 若属重复错误 → 选择正确版本
```

### 问题：找不到需要修改/移除的需求

**解决方案**：
```markdown
1. 按部分名称搜索：grep -i "login" spec/specs/**/*.md
2. 检查是否已被移除
3. 检查是否位于其他能力文件
```

### 问题：合并后常驻规范格式错误

**解决方案**：
```markdown
1. 手动修复格式
2. 重新运行验证：grep -n "###" spec/specs/**/*.md
3. 确保标题层级一致
```

## 参考资料

- [MERGE_LOGIC.md](reference/MERGE_LOGIC.md) - 详细的合并操作规则

---

**Token 预算**：此 SKILL.md 约 430 行，低于建议的 500 行上限。