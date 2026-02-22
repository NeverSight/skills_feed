---
name: Self-Evolving Skill
description: Meta-cognitive self-learning system - Automated skill evolution based on predictive coding and value-driven mechanisms.
homepage: https://github.com/whtoo/self-evolving-bot

---


# Self-Evolving Skill

元认知自学习系统 - 基于预测编码和价值驱动的Skill自动演化。

## 功能

- **ResidualPyramid金字塔分解，量化认知缺口
-**: 残差 **自适应反思触发**: 基于残差能量自动判断何时需要学习
- **经验回放**: 缓存已学模式，降低重复触发
- **价值门控**: 只有提升长期价值才接受变异
- **持久化**: 经验自动保存/加载

## 安装

```bash
# 技能已安装到 ~/.openclaw/skills/self-evolving-skill
# 或使用ClawHub
clawhub install self-evolving-skill
```

## 架构

```
self-evolving-skill/
├── core/                      # Python核心
│   ├── residual_pyramid.py     # 残差金字塔（SVD分解）
│   ├── reflection_trigger.py  # 自适应触发器
│   ├── experience_replay.py   # 经验回放缓存
│   ├── skill_engine.py        # 核心引擎+ValueGate
│   ├── storage.py             # 持久化
│   └── mcp_server.py          # MCP服务器
├── src/                       # TypeScript SDK
│   ├── index.ts               # 主入口
│   ├── cli.ts                 # CLI
│   └── mcp-tools.ts           # 工具定义
├── skills/                    # OpenClaw Skill
│   └── self-evolving-skill/    # 技能封装
├── MCP_CONFIG.md              # MCP配置
└── README.md                   # 文档
```

## MCP工具

| 工具 | 描述 | 参数 |
|------|------|------|
| `skill_create` | 创建Skill | `name`, `description` |
| `skill_execute` | 执行并学习 | `skill_id`, `context`, `success`, `value` |
| `skill_analyze` | 分析嵌入 | `embedding` |
| `skill_list` | 列出Skills | - |
| `skill_stats` | 系统统计 | - |
| `skill_save` | 持久化保存 | `skill_id` |
| `skill_load` | 加载 | `skill_id` |

## 使用方式

### CLI

```bash
# 列出所有Skill
openclaw skill self-evolving-skill list

# 创建Skill
openclaw skill self-evolving-skill create --name "MySkill"

# 执行
openclaw skill self-evolving-skill execute <id> --success

# 分析
openclaw skill self-evolving-skill analyze --embedding '[0.1,0.2,...]'

# 统计
openclaw skill self-evolving-skill stats
```

### MCP服务器

```bash
# 启动MCP服务器
cd ~/.openclaw/skills/self-evolving-skill
./run_mcp.sh

# 或使用适配器
python3 mcporter_adapter.py skill_list '{}'
```

### 编程

```typescript
import { SelfEvolvingSkillEngine } from 'self-evolving-skill';

const engine = new SelfEvolvingSkillEngine();
await engine.init();

const { skillId } = await engine.createSkill({ name: 'Analyzer' });
const stats = await engine.stats();
```

## 核心算法

### 1. 残差金字塔分解

```python
pyramid = ResidualPyramid(max_layers=5, use_pca=True)
decomposition = pyramid.decompose(embedding)

# 输出:
# - residual_ratio: 残差能量比率
# - suggested_abstraction: POLICY / SUB_SKILL / PREDICATE
# - novelty_score: 综合新颖性
```

### 2. 三层跃迁规则

| 覆盖率 | 抽象层级 | 操作 |
|--------|---------|------|
| >80% | POLICY | 调整策略权重 |
| 40-80% | SUB_SKILL | 生成子Skill |
| <40% | PREDICATE | 归纳新谓词 |

### 3. 自适应阈值

```python
trigger = ReflectionTrigger(
  min_energy_ratio=0.10,     # 初始阈值
  value_gain_threshold=0.20, # 触发阈值
  target_trigger_rate=0.15   # 目标15%触发率
)
```

## 文件位置

| 路径 | 说明 |
|------|------|
| `~/.openclaw/skills/self-evolving-skill` | 技能根目录 |
| `~/.openclaw/mcp_servers/self-evolving-skill.json` | MCP服务器配置 |
| `~/.openclaw/workspace/self-evolving-skill/storage` | 数据存储 |

## 相关文档

- [README.md](./README.md) - 完整文档
- [MCP_CONFIG.md](./MCP_CONFIG.md) - MCP配置说明
- [MEMORY.md](../MEMORY.md) - 研究笔记
