---
name: openspec-context-loading-cn
description: 加载项目上下文，列出现有规范与变更，搜索能力与需求。用于用户询问项目状态、现有规范、进行中的变更、可用能力或需要发现上下文时。触发词包括"openspec上下文", "有哪些规范", "显示变更", "列出能力", "项目上下文", "查找规范", "规范包含什么", "展示规范"。
---

# 规范上下文加载

发现并加载项目规范、进行中的变更和需求，以提供上下文。

## 快速开始

上下文加载可帮助回答：
- 项目有哪些规范？
- 目前有哪些进行中的变更？
- 已定义了哪些需求？
- 系统具备哪些能力？
- 某项功能在何处有所规范？

**基本模式**：搜索 → 阅读 → 总结

## 发现命令

注意将控制台与管道输出编码统一为 UTF-8，确保中文字符正确显示。

### 列出所有规范

```bash
# 查找所有规范文件
find spec/specs -name "spec.md" -type f

# 查找所有能力目录
find spec/specs -mindepth 1 -maxdepth 1 -type d

# 显示规范树
tree spec/specs/  # 若已安装 tree
# 或
ls -R spec/specs/
```

**输出格式**：
```
spec/specs/
├── authentication/
│   └── spec.md
├── billing/
│   └── spec.md
└── notifications/
    └── spec.md
```

### 列出进行中的变更

```bash
# 显示所有进行中的变更
find spec/changes -maxdepth 1 -type d -not -path "spec/changes" -not -path "*/archive" | sort

# 显示修改时间
find spec/changes -maxdepth 1 -type d -not -path "spec/changes" -not -path "*/archive" -exec ls -ld {} \;

# 统计进行中的变更数量
find spec/changes -maxdepth 1 -type d -not -path "spec/changes" -not -path "*/archive" | wc -l
```

### 列出已归档的变更

```bash
# 显示所有已归档变更
ls -1 spec/archive/

# 显示日期
ls -la spec/archive/

# 查找最近 7 天归档的变更
find spec/archive/ -maxdepth 1 -type d -mtime -7
```

### 搜索需求

```bash
# 查找所有需求
grep -r "### Requirement:" spec/specs/

# 在特定能力中查找需求
grep "### Requirement:" spec/specs/authentication/spec.md

# 列出唯一需求名称
grep -h "### Requirement:" spec/specs/**/*.md | sed 's/### Requirement: //' | sort
```

### 搜索场景

```bash
# 查找所有场景
grep -r "#### Scenario:" spec/specs/

# 统计每个规范中的场景数量
for spec in spec/specs/**/spec.md; do
    count=$(grep -c "#### Scenario:" "$spec")
    echo "$spec: $count scenarios"
done
```

### 关键词搜索

```bash
# 查找提到 "authentication" 的规范
grep -r -i "authentication" spec/specs/

# 查找与 "password" 相关的需求
grep -B 1 -A 5 -i "password" spec/specs/**/*.md | grep -A 5 "### Requirement:"

# 查找提到 "error" 的场景
grep -B 1 -A 10 -i "error" spec/specs/**/*.md | grep -A 10 "#### Scenario:"
```

## 常见查询

### 查询 1："项目有哪些规范？"

```bash
# 列出所有能力
find spec/specs -mindepth 1 -maxdepth 1 -type d -exec basename {} \;

# 统计每个能力的需求数量
for cap in spec/specs/*/; do
    name=$(basename "$cap")
    count=$(grep -c "### Requirement:" "$cap/spec.md" 2>/dev/null || echo "0")
    echo "$name: $count requirements"
done
```

**响应格式**：
```markdown
## 现有规范

项目具备以下能力的规范：

- **authentication**：8 条需求
- **billing**：12 条需求
- **notifications**：5 条需求

合计：3 个能力，25 条需求
```

### 查询 2："当前有哪些变更在进行？"

```bash
# 附带提案摘要的列表
for change in spec/changes/*/; do
    if [ "$change" != "spec/changes/archive/" ]; then
        id=$(basename "$change")
        echo "=== $id ==="
        head -n 20 "$change/proposal.md" | grep -A 3 "## Why"
    fi
done
```

**响应格式**：
```markdown
## 进行中的变更

当前进行中的变更：

### add-user-auth
**Why**：用户需要安全的认证...

### update-billing-api
**Why**：支付处理需要 v2 API...

合计：2 个进行中变更
```

### 查询 3："查找 authentication 规范"

```bash
# 阅读完整规范
cat spec/specs/authentication/spec.md

# 或展示摘要
echo "需求："
grep "### Requirement:" spec/specs/authentication/spec.md

echo "场景："
grep "#### Scenario:" spec/specs/authentication/spec.md
```

**响应格式**：
```markdown
## Authentication 规范

（包含 spec.md 的完整内容）

摘要：
- 8 条需求
- 16 个场景
- 最近修改时间：[来自 git log 的日期]
```

### 查询 4："查找与 password 相关的规范"

```bash
# 关键词搜索
grep -r -i "password" spec/specs/ -A 5

# 显示提到该关键词的规范
grep -r -i "password" spec/specs/ -l
```

**响应格式**：
```markdown
## Specs Mentioning "Password"

发现于：
- spec/specs/authentication/spec.md（3 条需求）
- spec/specs/security/spec.md（1 条需求）

相关需求：
### Requirement: Password Validation
### Requirement: Password Reset
### Requirement: Password Strength
```

### 查询 5："变更 X 的具体内容是什么？"

```bash
# 展示完整的变更上下文
CHANGE_ID="add-user-auth"

echo "=== 提案 ==="
cat spec/changes/$CHANGE_ID/proposal.md

echo "\n=== 任务 ==="
cat spec/changes/$CHANGE_ID/tasks.json

echo "\n=== 规范变更 ==="
find spec/changes/$CHANGE_ID/specs -name "*.md" -exec echo "File: {}" \; -exec cat {} \;
```

## 仪表盘视图

创建全面的项目概览：

```bash
#!/bin/bash
# 项目规范仪表盘

echo "===  规范仪表盘 ==="
echo ""

# 能力
echo "## 能力"
CAPS=$(find spec/specs -mindepth 1 -maxdepth 1 -type d | wc -l)
echo "能力总数: $CAPS"
for cap in spec/specs/*/; do
    name=$(basename "$cap")
    reqs=$(grep -c "### Requirement:" "$cap/spec.md" 2>/dev/null || echo "0")
    echo "  - $name: $reqs 条需求"
done
echo ""

# 需求
echo "## 需求"
TOTAL_REQS=$(grep -r "### Requirement:" spec/specs/ | wc -l)
TOTAL_SCENARIOS=$(grep -r "#### Scenario:" spec/specs/ | wc -l)
echo "需求总数: $TOTAL_REQS"
echo "场景总数: $TOTAL_SCENARIOS"
echo "每个需求平均场景数: $(echo "scale=1; $TOTAL_SCENARIOS/$TOTAL_REQS" | bc)"
echo ""

# 变更
echo "## 变更"
ACTIVE=$(find spec/changes -maxdepth 1 -type d -not -path "spec/changes" -not -path "*/archive" | wc -l)
ARCHIVED=$(ls -1 spec/archive/ | wc -l)
echo "进行中的变更: $ACTIVE"
echo "已归档的变更: $ARCHIVED"
echo ""

# 最近活动
echo "## 最近活动"
echo "最近修改的规范:"
find spec/specs -name "spec.md" -type f -exec ls -lt {} \; | head -5
```

**响应格式**：
```markdown
# Specification Dashboard

## Capabilities
Total capabilities: 3
  - authentication: 8 requirements
  - billing: 12 requirements
  - notifications: 5 requirements

## Requirements
Total requirements: 25
Total scenarios: 52
Avg scenarios per requirement: 2.1

## Changes
Active changes: 2
Archived changes: 15

## Recent Activity
Recently modified specs:
- spec/specs/billing/spec.md（2 天前）
- spec/specs/authentication/spec.md（1 周前）
```

## 高级查询

### 查找相关需求

```bash
# 查找提到其他需求的内容
grep -r "User Login" spec/specs/ -A 10 | grep "### Requirement:"

# 查找交叉引用
grep -r "See Requirement:" spec/specs/
```

### 分析覆盖度

```bash
# 查找无场景的需求
for spec in spec/specs/**/spec.md; do
    awk '/### Requirement:/ {req=$0; getline; if ($0 !~ /#### Scenario:/) print req}' "$spec"
done

# 查找不包含完整 Given/When/Then 的场景
grep -A 5 "#### Scenario:" spec/specs/**/*.md | grep -v "GIVEN\|WHEN\|THEN"
```

### 对比进行中与已归档

```bash
# 展示时间演化
echo "归档历史:"
ls -1 spec/archive/ | head -10

echo "最近归档 (30天):"
find spec/archive/ -maxdepth 1 -type d -mtime -30 -exec basename {} \;
```

## 搜索模式

### 模式 1：能力发现

用户提问："系统能做什么？"

```bash
# 列出能力
find spec/specs -mindepth 1 -maxdepth 1 -type d -exec basename {} \;

# 展示高层需求
for cap in spec/specs/*/; do
    echo "=== $(basename $cap) ==="
    grep "### Requirement:" "$cap/spec.md" | head -3
done
```

### 模式 2：功能搜索

用户提问："有密码重置的规范吗？"

```bash
# 关键词搜索
grep -r -i "password reset" spec/specs/ -B 1 -A 10

# 若找到，展示完整需求
grep -B 1 -A 20 "Requirement:.*Password Reset" spec/specs/**/*.md
```

### 模式 3：变更跟踪

用户提问："现在做什么？"

```bash
# 附带状态展示进行中的变更
for change in spec/changes/*/; do
    if [ "$change" != "spec/changes/archive/" ]; then
        id=$(basename "$change")
        echo "$id:"
        test -f "$change/IMPLEMENTED" && echo "  状态: 已完成" || echo "  状态: 进行中"
        echo "  任务: $(grep -c '"task":' "$change/tasks.json")"
    fi
done
```

## 最佳实践

### 模式 1：先提供上下文再给细节

**良好流程**：
```markdown
1. 展示仪表盘（高层概览）
2. 用户询问具体能力
3. 展示该能力的需求
4. 用户询问具体需求
5. 展示包含场景的完整需求
```

### 模式 2：高效使用 grep

```bash
# 结合过滤器提高精度
grep -r "### Requirement:" spec/specs/ | grep -i "auth"

# 使用上下文标志提升可读性
grep -B 2 -A 10 "#### Scenario:" spec/specs/authentication/spec.md
```

### 模式 3：聚合信息

不要只是倾倒文件内容。应做总结：

```markdown
**坏**：（直接输出整个规范文件）

**好**：
"authentication 规范包含 8 条需求，覆盖：
- 用户登录
- 密码管理
- 会话处理
- 多因素认证

需要我展示某条具体需求吗？"
```

## 反模式避免

**不要**：
- 未经请求就读取整个规范文件
- 默认列出所有需求
- 输出未经格式化的原始 grep 结果
- 假定用户知道能力名称

**要**：
- 先给高层概览
- 询问用户希望深入了解的领域
- 清晰格式化输出
- 提供导航提示

## 参考资料

- [SEARCH_PATTERNS.md](reference/SEARCH_PATTERNS.md) - 高级 grep/find 模式

---

**Token 预算**：此 SKILL.md 约 460 行，低于建议的 500 行上限。