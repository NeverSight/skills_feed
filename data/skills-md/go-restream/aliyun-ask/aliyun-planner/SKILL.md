---
name: aliyun-planner
description: 自然语言理解阿里云资源查询意图，规划并生成标准化的Aliyun CLI执行计划（JSON格式）。当用户查询阿里云资源（ECS、RDS、VPC、SLB、OSS等）、需要获取资源状态、查看资源详情、或分析资源关联关系时使用此技能。支持简单查询、关联查询、复合查询、诊断查询等多种场景。
---

# Aliyun Planner

Aliyun Planner 将用户的自然语言查询转换为标准化的 Aliyun CLI 执行计划。它通过意图分类、实体抽取、关系识别和API映射四个步骤，输出可执行的 JSON 格式 CLI 命令序列。

## 工作流程

### Step 1: 意图分类
读取 [意图分类词典库.md](references/意图分类词典库.md)，分析用户查询确定：

- **primary_intent**: 主意图（SIMPLE_QUERY, ASSOCIATION_QUERY, COMPOUND_QUERY, DIAGNOSTIC_QUERY, COMPARISON_QUERY, OPERATIONAL_QUERY）
- **sub_intent**: 子意图（如 SIMPLE_INSTANCE, ASSOC_HIERARCHY 等）
- **complexity**: 复杂度等级（L1-L5）
- **business_scenario**: 业务场景
- **confidence**: 置信度

如用户信息模糊，可进一步询问澄清。

### Step 2: 实体抽取
读取 [实体知识库.md](references/实体知识库.md)，识别云资源实体：

- **primary_entity**: 主查询目标资源
- **target_entities**: 其他相关资源
- **ambiguous_entities**: 模糊实体候选（需澄清）
- **filters**: 过滤条件（状态、标签等）

### Step 3: 关系识别
读取 [关系知识库.md](references/关系知识库.md)，建立资源关联：

- **relations**: 显式关系列表
- **relationship_path**: 关系链条
- **join_conditions**: API关联键
- **inferred_relations**: 隐含关系

### Step 4: 执行计划生成
读取 [API操作映射库.md](references/API操作映射库.md)，生成 CLI 命令：

- **execution_strategy**: 执行策略（SEQUENTIAL, PARALLEL, CACHE_FIRST）
- **cli_commands**: CLI命令列表（含command、parameters、depends_on、output_processing）
  - **command**: 命令数组格式，如 `["ecs", "DescribeInstances"]`（不包含 "aliyun" 前缀）
  - **tid**: 任务ID，从 0 开始顺序分配
- **data_flow**: 数据流转关系
- **estimated_time**: 预估时间
- **prerequisites**: 前提条件

### Step 5: 输出校验
使用 [scripts/validate_json.py](scripts/validate_json.py) 对输出 JSON 进行 Pydantic 验证：

- **验证内容**: JSON 结构完整性、字段类型、必填字段、数值范围
- **验证失败处理**: 如果验证失败，返回 Step 4 重新生成执行计划
- **循环机制**: 持续验证直到输出符合规范，确保最终输出为正确格式的 JSON

运行验证：
```bash
python3 scripts/validate_json.py your_output.json
```

或作为库使用：
```python
from validate_json import validate_json_output
is_valid, message = validate_json_output(your_json_dict)
```

## 输出格式

**仅输出 JSON 格式**，包含以下结构：

```json
{
  "intent_core": {
    "primary_intent": "ASSOCIATION_QUERY",
    "sub_intent": "ASSOC_HIERARCHICAL",
    "complexity": "L3",
    "business_scenario": "生产部署",
    "confidence": 0.88
  },
  "entities": {
    "primary_entity": {
      "service": "rds",
      "resource_type": "instance",
      "identifier_type": "tag",
      "identifier_value": "role:master",
      "original_expression": "生产数据库集群"
    }
  },
  "relationships": {
    "relations": [
      {
        "type": "PART_OF_CLUSTER",
        "source": "master_instance",
        "target": "readonly_instances"
      }
    ],
    "relationship_path": ["RDS主实例", "RDS只读实例"]
  },
  "execution": {
    "execution_strategy": "SEQUENTIAL",
    "cli_commands": [
      {
        "command": ["rds", "DescribeDBInstances"],
        "parameters": {
          "RegionId": "cn-hangzhou",
          "Tags": "[{\"key\":\"env\", \"value\":\"prod\"}]"
        },
        "tid": 0
      },
      {
        "command": ["rds", "DescribeDBInstanceAttribute"],
        "parameters": {
          "DBInstanceId": "$.DBInstances.DBInstance[0].DBInstanceId"
        },
        "tid": 1,
        "depends_on": [0],
        "output_processing": "jq '.Items.DBInstanceAttribute[] | select(.Role == \"ReadOnly\")'"
      }
    ]
  }
}
```

## 常见查询示例

| 用户查询 | 主意图 | 子意图 |
|---------|-------|--------|
| "我的ECS实例有哪些" | SIMPLE_QUERY | SIMPLE_INSTANCE |
| "ECS i-123挂载了哪些磁盘" | ASSOCIATION_QUERY | ASSOC_DIRECT |
| "VPC vpc-xxx下的所有资源" | ASSOCIATION_QUERY | ASSOC_HIERARCHY |
| "生产环境所有数据库" | COMPOUND_QUERY | COMPOUND_CONDITIONAL |
| "检查安全组是否安全" | DIAGNOSTIC_QUERY | DIAG_SECURITY |
| "对比生产和测试环境" | COMPARISON_QUERY | COMPARE_CONFIG |

## 支持的阿里云服务

- **计算**: ECS, FC, ACK
- **数据库**: RDS, Redis, MongoDB, PolarDB
- **网络**: VPC, VSwitch, EIP, SLB, ALB
- **存储**: OSS, NAS
- **消息**: RocketMQ, Kafka
- **监控**: SLS, CMS
- **安全**: WAF, DDoS
- **其他**: DNS, CDN

完整服务列表详见 [实体知识库.md](references/实体知识库.md)。

## 执行策略选择

- **SEQUENTIAL**: 存在依赖关系，需顺序执行
- **PARALLEL**: 无依赖的独立查询，可并行
- **CACHE_FIRST**: 重复查询相同资源，优先使用缓存
- **BATCH**: 大量资源查询，分页处理
