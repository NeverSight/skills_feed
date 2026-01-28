---
name: aliyun-exec
description: 解析用户需求分析配置（JSON格式），生成并输出TODO任务清单。当用户提供阿里云资源查询需求分析配置、需要将JSON配置转换为可执行的任务清单时使用此技能。仅支持阿里云资源查询操作，拒绝任何变更类操作需求。使用Aliyun CLI命令行工具执行查询，通过aliyun help获取参数帮助。
---

# Aliyun Exec

Aliyun Exec 将用户需求分析配置（JSON格式）转换为可执行的 TODO 任务清单。它基于 Aliyun CLI 命令行工具执行阿里云资源查询，确保所有操作均为只读查询，拒绝任何变更操作。

## 核心约束

**只读查询原则**：此技能仅支持阿里云资源查询操作，严格拒绝任何变更类需求。当检测到以下操作时，必须拒绝执行并提示用户：

- Create/Delete/Modify/Update 等变更类 API
- 配置修改、资源释放、权限变更等操作
- 任何可能影响现有资源的非查询操作

## 工作流程

### Step 1: 解析输入配置

读取用户提供的 JSON 配置，提取以下关键信息：

- **intent_core**: 意图核心（主意图、子意图、复杂度、业务场景）
- **entities**: 实体信息（主资源、目标资源、标识符类型）
- **relationships**: 关系信息（关系类型、关系路径）
- **execution**: 执行计划（CLI 命令、参数、依赖关系、输出处理）

### Step 2: 安全性检查

对所有 CLI 命令进行安全性验证：

1. **检查操作类型**：确认所有命令均为 Describe/List/Get 等查询操作
2. **拒绝变更操作**：如果包含 Create/Delete/Modify/Update 等操作，拒绝执行
3. **验证参数安全性**：确保参数不包含破坏性或变更性内容

如检测到变更操作，输出拒绝信息并说明原因。

### Step 3: 生成任务清单

基于验证通过的执行计划，生成结构化的 TODO 任务清单。读取 [TODO任务清单模板.md](references/TODO任务清单模板.md) 了解标准格式。

任务清单包含以下阶段：

1. **环境准备阶段**
   - 验证 Aliyun CLI 安装
   - 验证凭证配置
   - 确认地域参数
   - 验证所需权限

2. **资源发现阶段**
   - 查询主资源列表
   - 提取资源标识符
   - 保存中间结果

3. **关联查询阶段**（如适用）
   - 根据依赖关系查询关联资源
   - 处理条件执行逻辑
   - 合并查询结果

4. **数据处理阶段**
   - 应用 jq 过滤和转换
   - 提取关键信息
   - 格式化输出

5. **报告生成阶段**
   - 汇总查询结果
   - 应用诊断规则（如有）
   - 生成最终报告

### Step 4: 处理命令参数不确定的情况

当 CLI 命令参数不确定时，按以下优先级处理：

1. **使用 Aliyun Help**：
   ```bash
   aliyun help                    # 查看所有产品帮助
   aliyun <product> help          # 查看特定产品帮助
   aliyun <product> <api> help    # 查看特定API帮助
   ```

2. **查阅 API 文档**：读取 [API操作映射库.md](references/API操作映射库.md) 获取标准参数

3. **参考示例**：查看历史执行记录或类似命令示例

### Step 5: 输出格式

输出格式化的 Markdown TODO 任务清单，包含：

- **任务分析**：概述任务类型、复杂度和目标
- **阶段划分**：按逻辑分组的任务列表
- **命令详情**：完整的 CLI 命令（包含参数）
- **依赖关系图**：可视化任务依赖
- **关键注意事项**：权限要求、参数说明、分页处理等

标准格式示例见 [示例.md](references/示例.md)。

## 命令构建规范

### CLI 命令格式

```bash
aliyun <service> <api> --param1 value1 --param2 value2
```

- **service**: 阿里云产品代码（如 ecs, rds, slb）
- **api**: API 操作名称（如 DescribeInstances）
- **参数格式**: `--ParameterName value`（注意 PascalCase）

### 参数替换规则

处理配置中的参数替换变量：

| 变量格式 | 说明 | 示例 |
|---------|------|------|
| `$REGION_ID` | 地域ID，需用户指定或使用默认值 | `cn-hangzhou` |
| `$.field` | JSONPath 引用上一步输出结果 | `$.LoadBalancers.LoadBalancer[*].LoadBalancerId` |
| `$var` | 自定义变量 | 具体值由用户或上下文提供 |

### 输出处理

使用 jq 进行 JSON 输出处理：

```bash
aliyun ecs DescribeInstances --RegionId cn-hangzhou \
  | jq '.Instances.Instance[] | {InstanceId, InstanceName, Status}'
```

## 常见查询场景

| 场景描述 | 主意图 | 典型命令 |
|---------|-------|---------|
| 查看所有ECS实例 | SIMPLE_QUERY | `aliyun ecs DescribeInstances` |
| 查询SLB监听器配置 | ASSOCIATION_QUERY | `aliyun slb DescribeLoadBalancerListeners` |
| 检查安全组规则 | DIAGNOSTIC_QUERY | `aliyun ecs DescribeSecurityGroupAttribute` |
| 查询VPC关联资源 | ASSOCIATION_QUERY | `aliyun vpc DescribeVpcAttribute` |

## 支持的阿里云服务

- **计算**: ECS, FC, ACK
- **数据库**: RDS, Redis, MongoDB, PolarDB
- **网络**: VPC, SLB, ALB, EIP
- **存储**: OSS, NAS
- **消息**: RocketMQ, Kafka
- **监控**: SLS, CMS
- **安全**: WAF, DDoS
- **其他**: DNS, CDN

完整服务 API 映射见 [API操作映射库.md](references/API操作映射库.md)。

## 错误处理

### 认证错误
```
Error: The account is not authorized.
解决：检查 Aliyun CLI 凭证配置 (aliyun configure)
```

### 参数错误
```
Error: InvalidParameter
解决：使用 aliyun <product> <api> help 查看正确参数
```

### 权限不足
```
Error: Forbidden.RAM
解决：确认账号具有对应查询权限
```

### Throttling
```
Error: Throttling
解决：请求频率超限，等待后重试
