---
name: question-generator
description: 智能面试问题生成器。基于JD分析、用户简历和公司特点，生成定制化面试问题。支持技术面试、系统设计、行为面试（STAR）、HR面试。提供不同难度级别（简单/中等/困难）。自动维护问题库，追踪练习历史。与jd-analyzer和interview-coach集成。
allowed-tools: Read, Write, Grep
---

# Question Generator Skill

## 触发条件
当用户需要：
- 生成目标公司的面试问题
- 练习特定类型的面试问题
- 获取不同难度的问题
- 更新问题库
- 查看问题练习历史

## 核心能力

### 1. 问题生成引擎
基于以下维度生成问题：
- **JD分析结果**: 从jd-analyzer提取的技能要求
- **公司特点**: 公司类型、技术栈、业务领域
- **职位级别**: Junior/Mid/Senior/Staff/Principal
- **面试类型**: 技术/系统设计/行为/HR
- **难度级别**: 简单/中等/困难

### 2. 问题类型

#### 技术面试问题
**编程题**:
- 算法和数据结构
- LeetCode风格题目
- 代码优化
- 边界条件处理

**技术深度问题**:
- 语言特性
- 框架原理
- 系统架构
- 性能优化
- 最佳实践

**设计问题**:
- API设计
- 数据库设计
- 类设计
- 设计模式应用

#### 系统设计问题
**经典系统设计**:
- URL Shortener
- Twitter Timeline
- Chat System
- File Storage
- Rate Limiter
- Key-Value Store

**大规模系统**:
- 分布式系统
- 微服务架构
- 数据一致性
- 负载均衡
- 缓存策略
- 消息队列

#### 行为面试问题
**STAR方法问题**:
- 团队合作
- 冲突解决
- 领导力
- 挑战项目
- 失败经历
- 成就展示

**情景问题**:
- 如何处理紧急情况
- 如何与难相处的同事合作
- 如何在压力下工作
- 如何学习新技术

#### HR面试问题
- 自我介绍
- 职业规划
- 薪资期望
- 离职原因
- 为什么选择这家公司
- 优势和劣势

### 3. 难度级别算法

**简单 (Easy)**:
- 基础概念和定义
- 直接应用
- 单一步骤问题
- 适合：Junior职位、Warm-up

**中等 (Medium)**:
- 需要多步思考
- 组合多个概念
- 有一定复杂度
- 适合：Mid-level职位、核心面试

**困难 (Hard)**:
- 需要深入分析
- 系统级思考
- 优化和Trade-offs
- 适合：Senior+职位、筛选面试

### 4. 问题库管理

#### 问题存储结构
```json
{
  "question_id": "unique_id",
  "type": "technical|system_design|behavioral|hr",
  "category": "algorithm|database|distributed_system|teamwork",
  "difficulty": "easy|medium|hard",
  "question_text": "...",
  "tags": ["array", "dynamic_programming", "google"],
  "created_at": "2024-01-01",
  "times_asked": 0,
  "success_rate": 0.0,
  "related_skills": ["Python", "Algorithms"]
}
```

#### 练习历史追踪
```json
{
  "practice_session": {
    "session_id": "unique_id",
    "date": "2024-01-01",
    "company_id": "...",
    "questions_practiced": [...],
    "performance": {...},
    "improvement_areas": [...]
  }
}
```

## 工作流程

### 步骤 1: 读取上下文
使用Read工具读取：
- `data/companies/{company}.json` - 目标公司和JD分析
- `data/resume/base.json` - 用户基础简历
- `data/questions/technical.json` - 现有技术问题库
- `data/questions/behavioral.json` - 现有行为问题库

### 步骤 2: 分析需求
从JD分析中提取：
- 必需技能（required_skills）
- 优先技能（preferred_skills）
- 职位级别
- 公司类型（Big Tech/Startup/等）
- 技术栈

### 步骤 3: 生成问题
根据分析结果生成问题：

```json
{
  "generated_questions": {
    "company": "Google",
    "position": "Software Engineer L3",
    "technical": {
      "easy": [
        {
          "question_id": "tech_001",
          "question": "实现一个LRU Cache",
          "category": "data_structure",
          "related_skills": ["Hash Table", "Doubly Linked List"],
          "estimated_time": "20-30 minutes",
          "follow_up_questions": ["如何O(1)时间复杂度实现？", "如何处理并发？"]
        }
      ],
      "medium": [...],
      "hard": [...]
    },
    "system_design": [...],
    "behavioral": [...],
    "hr": [...]
  }
}
```

### 步骤 4: 更新问题库
将新生成的问题添加到对应的问题库文件：
- 技术问题 → `data/questions/technical.json`
- 行为问题 → `data/questions/behavioral.json`
- 系统设计 → `data/questions/system_design.json`
- HR问题 → `data/questions/hr.json`

### 步骤 5: 记录生成历史
更新 `data/analytics/question_generation.json`:
```json
{
  "generation_history": [
    {
      "timestamp": "2024-01-01T10:00:00Z",
      "company_id": "google",
      "position": "Software Engineer L3",
      "questions_generated": 15,
      "question_types": ["technical", "behavioral", "system_design"],
      "difficulty_distribution": {
        "easy": 5,
        "medium": 7,
        "hard": 3
      }
    }
  ]
}
```

## 集成点

### 与 jd-analyzer 集成
- 读取JD分析结果中的技能要求
- 基于技能匹配度生成相关技术问题
- 针对技能差距生成准备性问题

### 与 interview-coach 集成
- 将生成的问题传递给interview-coach用于模拟面试
- 接收面试反馈，调整问题难度
- 基于表现推荐额外练习问题

### 与 interview-simulator 集成
- 为模拟器提供问题库
- 根据模拟结果更新问题难度评级
- 追踪问题成功率

## 问题生成策略

### 公司特定策略

**Google**:
- 强调算法和数据结构
- 系统设计的可扩展性
- 开放式问题（"设计一个..."）
- Leadership Principle相关行为问题

**Meta (Facebook)**:
- 实用编程问题
- 分布式系统
- "Move Fast"文化相关行为问题
- 影响力和成就感

**Amazon**:
- 系统设计和架构
- 实际问题解决
- Leadership Principles行为问题
- 客户 obsession

**Microsoft**:
- 产品设计思维
- 跨平台开发
- 成长型思维（Growth Mindset）
- 团队协作

**Startup**:
- 全栈能力
- 快速学习能力
- 适应变化
- 多任务处理

### 职位级别策略

**Junior (L2-L3)**:
- 基础概念和编码能力
- 学习潜力
- 简单到中等难度
- 基础系统设计

**Mid-level (L4)**:
- 项目经验
- 问题解决能力
- 中等到困难
- 完整系统设计

**Senior (L5)**:
- 架构设计
- 技术领导力
- 困难级别
- 复杂系统设计

**Staff+ (L6+)**:
- 跨团队协作
- 技术战略
- 极具挑战性问题
- 多系统设计

## 输出格式

### 标准问题输出
```markdown
## 技术面试问题 - 中等难度

### 问题: 实现一个分布式缓存系统

**背景**:
- 需要支持高并发读写
- 数据需要持久化
- 节点可能故障

**要求**:
1. 设计系统架构
2. 讨论数据一致性策略
3. 处理节点故障
4. 优化性能

**评估要点**:
- CAP理论理解
- 分片策略
- 复制机制
- 一致性协议
- 性能优化

**预计时间**: 45分钟
**相关技能**: Distributed Systems, Cache, Consistency
```

### 批量问题输出
```json
{
  "batch_questions": {
    "company": "Google",
    "position": "Software Engineer L3",
    "total_questions": 20,
    "questions_by_type": {
      "technical": 8,
      "system_design": 4,
      "behavioral": 5,
      "hr": 3
    },
    "estimated_preparation_time": "2-3 weeks",
    "priority_order": [...]
  }
}
```

## 最佳实践

1. **问题多样性**: 避免重复，每次生成略有不同
2. **难度递进**: 从简单到困难，帮助用户建立信心
3. **相关性**: 确保问题与目标职位高度相关
4. **时效性**: 基于当前技术趋势更新问题
5. **反馈驱动**: 根据用户表现调整问题难度
6. **全面覆盖**: 平衡各类问题，不偏重某一类型

## 命令集成

此skill可被以下命令调用：
- `/interview/prep` - 生成面试准备问题集
- `/interview/simulate` - 为模拟面试提供问题
- `/company/questions` - 生成公司特定问题
- `/weakness/practice` - 针对弱点生成练习题

## 数据文件依赖

- `data/companies/*.json` - 公司和JD数据
- `data/resume/base.json` - 用户简历
- `data/questions/*.json` - 问题库
- `data/analytics/question_generation.json` - 生成历史
