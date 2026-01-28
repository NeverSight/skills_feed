---
name: codex-cli
description: Orchestrate OpenAI Codex CLI for parallel task execution. As orchestrator, analyze tasks, inject context, manage sessions, and coordinate parallel instances. Use when delegating coding tasks to Codex or running multi-agent workflows. (user)
---

# Codex CLI Orchestrator

**角色定位**：Claude Code 是编排者，Codex 是执行者。

**核心价值**：通过智能编排，让 Codex 更快、更准、更省 token。

---

## 快速决策流程

```
收到任务
    │
    ├─ 1. 能否预注入上下文？ ──→ 是 → 收集代码/错误，注入 prompt
    │
    ├─ 2. 与已有会话相关？ ────→ 是 → 复用会话 (resume)
    │
    ├─ 3. 可拆分为独立子任务？ → 是 → 并行执行
    │
    └─ 4. 以上都否 ───────────→ 新建单会话串行执行
```

---

## 三大优化策略

### 策略 1: 上下文预注入 (最重要)

**原理**：Claude Code 先收集相关信息，注入 prompt，让 Codex 跳过探索。

| 注入内容 | 命令示例 |
|----------|----------|
| 文件路径 | `codex exec "Fix bug in: src/auth/login.ts, src/utils/token.ts"` |
| 错误信息 | `codex exec "Fix: $(npm run build 2>&1 \| grep error)"` |
| 代码片段 | `codex exec "Optimize: $(cat src/slow.ts)"` |
| 依赖关系 | `codex exec "Refactor A, deps: B→C→D"` |

**模板**：
```bash
codex exec "[任务]

## 文件: $FILES
## 错误: $ERRORS
## 代码:
\`\`\`
$CODE
\`\`\`

约束: 只修改上述文件，直接开始。"
```

### 策略 2: 会话复用

**原理**：关联任务复用已有会话，继承上下文，避免重复分析。

```bash
# 首次执行
codex exec "analyze src/auth for issues"

# 复用会话继续 (用 stdin 传递 prompt，避免 CLI bug)
echo "fix the issues you found" | codex exec resume --last

# 或使用 --full-auto 允许修改
echo "fix the issues" | codex exec resume --last --full-auto
```

> **注意**：`codex exec resume --last "prompt"` 有 CLI 解析 bug，必须用 stdin 传递 prompt。

**何时复用**：
- 分析后修复 → 复用 (知道发现了什么)
- 实现后测试 → 复用 (知道实现了什么)
- 测试后修复 → 复用 (知道哪里失败)

### 策略 3: 并行执行

**原理**：隔离良好的任务同时执行，节省总时间。

**可并行**：
- 不同目录/模块
- 不同分析维度 (安全/性能/质量)
- 只读操作

**需串行**：
- 写同一文件
- 依赖前序结果

```bash
# 并行执行
codex exec "analyze auth" > auth.txt 2>&1 &
codex exec "analyze api" > api.txt 2>&1 &
wait

# 并行 + 复用
codex exec resume $AUTH_SID --full-auto "fix" &
codex exec resume $API_SID --full-auto "fix" &
wait
```

---

## Prompt 设计要点

### 结构公式

```
[动词] + [范围] + [要求] + [输出格式] + [约束]
```

### 动词选择

| 只读 | 写入 |
|------|------|
| analyze, review, find, explain | fix, refactor, implement, add |

### 好 vs 差

| 差 | 好 |
|-----|-----|
| `review code` | `review src/auth for SQL injection, XSS. Output: markdown, severity levels.` |
| `find bugs` | `find bugs in src/utils. Output: file:line, description, fix suggestion.` |
| `improve code` | `refactor Button.tsx to hooks. Preserve props. Don't modify others.` |

### 并行时保持一致

```bash
# 结构一致，输出格式统一，便于聚合
codex exec "analyze src/auth for security. Output JSON." &
codex exec "analyze src/api for security. Output JSON." &
codex exec "analyze src/db for security. Output JSON." &
wait
```

---

## 综合示例

### 示例 1: 全流程优化 (预注入 + 并行 + 复用)

```bash
# Phase 1: Claude Code 收集信息
ERRORS=$(npm run lint 2>&1)
AUTH_ERR=$(echo "$ERRORS" | grep "src/auth")
API_ERR=$(echo "$ERRORS" | grep "src/api")

# Phase 2: 并行执行，预注入各自错误
codex exec --json --full-auto "Fix lint errors:
$AUTH_ERR
Only modify src/auth/" > auth.jsonl 2>&1 &

codex exec --json --full-auto "Fix lint errors:
$API_ERR
Only modify src/api/" > api.jsonl 2>&1 &
wait

# Phase 3: 如需继续，复用会话
AUTH_SID=$(grep -o '"thread_id":"[^"]*"' auth.jsonl | head -1 | cut -d'"' -f4)
codex exec resume $AUTH_SID "verify fixes and run tests"
```

### 示例 2: 迭代开发 (单会话多轮复用)

```bash
# Round 1: 分析
codex exec "analyze codebase, plan auth implementation"

# Round 2-4: 复用同一会话，继承全部上下文 (用 stdin)
echo "implement as planned" | codex exec resume --last --full-auto
echo "add tests" | codex exec resume --last --full-auto
echo "fix failures" | codex exec resume --last --full-auto
```

### 示例 3: 代码审查 (4 路并行 → 各自复用修复)

```bash
# 并行审查
codex exec --json "audit security" > sec.jsonl &
codex exec --json "audit performance" > perf.jsonl &
codex exec --json "audit quality" > qual.jsonl &
codex exec --json "audit practices" > prac.jsonl &
wait

# 提取会话 IDs
SEC=$(grep -o '"thread_id":"[^"]*"' sec.jsonl | head -1 | cut -d'"' -f4)
PERF=$(grep -o '"thread_id":"[^"]*"' perf.jsonl | head -1 | cut -d'"' -f4)
# ...

# 并行修复，各自复用
codex exec resume $SEC --full-auto "fix security issues" &
codex exec resume $PERF --full-auto "fix performance issues" &
# ...
wait
```

---

## 速查表

### 命令

```bash
codex exec "prompt"                              # 只读
codex exec --full-auto "prompt"                  # 可写
codex exec --cd /path "prompt"                   # 指定目录
codex exec --json "prompt"                       # JSON 输出
echo "prompt" | codex exec resume --last         # 复用最近会话
echo "prompt" | codex exec resume --last --full-auto  # 复用 + 可写
```

### 后台并行

```bash
codex exec "task1" > out1.txt 2>&1 &
codex exec "task2" > out2.txt 2>&1 &
wait
```

### 提取会话 ID

```bash
SID=$(grep -o '"thread_id":"[^"]*"' output.jsonl | head -1 | cut -d'"' -f4)
```

---

## 详细参考

见 [REFERENCE.md](./REFERENCE.md) 了解：
- 完整命令行参数
- Prompt 设计详解
- 并行执行详解
- 配置文件选项
