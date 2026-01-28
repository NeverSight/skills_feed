---
name: jd-analyzer
description: 分析职位描述（JD）以提取关键信息、技能要求、资格条件。识别核心技能、软技能、经验要求。用于简历匹配、面试准备、技能差距分析。当用户提供JD文本或添加公司信息时自动触发。
allowed-tools: Read, Write, Grep
---

# JD Analyzer Skill

## 触发条件
当用户需要：
- 分析职位描述（JD）
- 提取关键技能和要求
- 评估简历与JD的匹配度
- 识别技能差距
- 为特定公司准备面试

## 分析维度

### 1. 基本信息
- 职位名称和级别
- 团队和部门
- 工作地点
- 职位类型（全职/兼职/实习）

### 2. 技能分析
#### 编程语言
- 必需语言（Required）
- 优先语言（Preferred）
- 框架和库
- 工具和平台

#### 系统设计
- 分布式系统
- 微服务架构
- 数据库设计
- 可扩展性要求
- 性能优化

#### 领域知识
- 行业特定知识
- 业务领域理解
- 专业术语

### 3. 软技能
- 沟通能力
- 领导力
- 团队协作
- 问题解决
- 适应能力

### 4. 资格要求
- 教育背景（学位、专业）
- 工作经验年限
- 特定领域经验
- 认证或证书

### 5. 职责范围
- 主要工作内容
- 项目类型
- 影响范围
- 决策权限

### 6. 加分项
- 优先考虑的技能
- 额外的认证或经验
- 特殊贡献或成就

## 工作流程

### 步骤 1: 提取原始信息
从JD文本中提取：
- 所有技能关键词
- 经验要求
- 教育要求
- 职责描述

### 步骤 2: 结构化分析
将提取的信息分类到：
```json
{
  "structured_analysis": {
    "required_skills": [...],
    "preferred_skills": [...],
    "responsibilities": [...],
    "minimum_qualifications": [...],
    "preferred_qualifications": [...]
  }
}
```

### 步骤 3: 技能匹配
对比用户基础简历（data/resume/base.json）：
```json
{
  "skill_match_analysis": {
    "matched_skills": [
      {"skill": "Python", "proficiency": "expert"}
    ],
    "partial_match_skills": [
      {"skill": "Java", "proficiency": "intermediate", "required": "advanced"}
    ],
    "missing_skills": [
      {"skill": "C++", "action": "需要学习基础"}
    ]
  }
}
```

### 步骤 4: 生成建议
基于匹配分析提供：
- 需要补充的技能
- 应该突出的经验
- 面试准备重点
- 简历优化建议

## 技能提取模式

### 编程语言识别
识别以下模式：
- "Proficiency in/with X"
- "Experience with/using X"
- "Strong knowledge of X"
- "X developer"
- "X, Y, or Z"

### 经验级别判断
- Entry: 0-2 years
- Mid: 2-5 years
- Senior: 5+ years
- Staff/Principal: 8+ years

### 系统设计关键词
- "Distributed systems"
- "Microservices architecture"
- "Scalable systems"
- "High-availability"
- "Large-scale systems"
- "Cloud-native"

### 软技能识别
- "Excellent communication"
- "Leadership experience"
- "Team player"
- "Problem-solving skills"
- "Self-motivated"

## 输出格式

### 公司信息文件更新
更新 `data/companies/{company}.json` 的 `job_descriptions` 部分：

```json
{
  "job_descriptions": {
    "pos_001": {
      "title": "Software Engineer III",
      "description_source": "...",
      "scraped_at": "2025-01-09T00:00:00Z",
      "raw_text": "完整JD文本...",

      "structured_analysis": {
        "required_skills": ["Python", "Distributed Systems"],
        "preferred_skills": ["Kubernetes", "ML"],
        "responsibilities": ["设计并开发软件"],
        "minimum_qualifications": ["计算机学位", "3年经验"],
        "preferred_qualifications": ["硕士", "5年经验"]
      },

      "skill_match_analysis": {
        "matched_skills": [...],
        "partial_match_skills": [...],
        "missing_skills": [...]
      }
    }
  }
}
```

## 使用示例

### 场景 1: 添加新公司时
用户提供JD文本，自动：
1. 提取所有技能和要求
2. 分析与用户简历的匹配度
3. 生成结构化分析报告
4. 保存到公司信息文件

### 场景 2: 简历优化前
为简历优化器提供：
- 关键技能列表
- 优先级排序
- 匹配度评分
- 优化建议

### 场景 3: 面试准备时
生成面试准备重点：
- 技术主题清单
- 可能的问题类型
- 需要深入研究的领域

## 匹配规则

### 完全匹配
- 用户有直接使用经验
- 项目中实际应用
- 可以深度讨论

### 部分匹配
- 了解相关技术
- 有相似技术经验
- 可以快速学习

### 缺失
- 完全没有经验
- 需要从头学习
- 建议学习路径

## 权重计算
用于匹配度评分：
- 必需技能：权重 2.0
- 优先技能：权重 1.0
- 加分项：权重 0.5

```
匹配度 = Σ(匹配等级 × 权重) / Σ(最大权重)
```

## 注意事项

1. **上下文理解**: 考虑JD的整体语境，而不是孤立的关键词
2. **技能归类**: 将不同名称但本质相同的技能归类
3. **公司特色**: 识别公司的技术文化（如Google重视可扩展性）
4. **隐含要求**: 识别JD中未明确表达的期望
5. **动态更新**: 随着用户技能提升，重新评估匹配度

## 高级分析功能（Phase 2新增）

### 公司文化分析

#### 文化指标识别

**工作文化关键词**:
```json
{
  "culture_indicators": {
    "pace": {
      "fast": ["fast-paced", "move fast", "rapid iteration", "agile", "startup environment"],
      "balanced": ["work-life balance", "sustainable pace", "flexible hours"],
      "intense": ["high-pressure", "demanding", "deadline-driven"]
    },
    "collaboration": {
      "collaborative": ["team player", "cross-functional", "collaborate", "pair programming"],
      "independent": ["self-starter", "independent", "autonomous", "own initiatives"],
      "leadership": ["lead", "mentor", "guide", "influence", "drive decisions"]
    },
    "innovation": {
      "innovative": ["innovative", "cutting-edge", "pioneer", "breakthrough", "novel"],
      "stable": ["stable", "proven", "established", "reliable", "mature"],
      "scalable": ["scale", "growth", "expand", "multiply", "massive impact"]
    },
    "values": {
      "customer_obsessed": ["customer obsessed", "customer first", "user-centric"],
      "data_driven": ["data-driven", "analytics", "metrics", "experimentation"],
      "ownership": ["ownership", "end-to-end", "responsibility", "accountability"],
      "excellence": ["high standards", "excellence", "quality", "best practices"]
    }
  }
}
```

#### 文化匹配分析
```json
{
  "culture_analysis": {
    "company_culture_type": "Innovative & Fast-paced",
    "key_culture_traits": [
      "Data-driven decision making",
      "Fast iteration and experimentation",
      "Collaborative cross-functional work",
      "High ownership and accountability"
    ],
    "culture_indicators_found": [
      {"trait": "fast-paced", "evidence": "fast-paced environment", "frequency": 3},
      {"trait": "data-driven", "evidence": "data-driven approach", "frequency": 5},
      {"trait": "collaborative", "evidence": "cross-functional teams", "frequency": 2}
    ],
    "fit_assessment": {
      "score": 85,
      "strengths": ["匹配快速迭代环境", "有跨团队协作经验"],
      "considerations": ["需要适应高压环境", "强调数据驱动决策"]
    }
  }
}
```

### 薪资范围检测

#### 薪资信息提取

**识别模式**:
```regex
# 基础薪资
"(\$?\d{2,3}k?[-–to]\$?\d{2,3}k?)\s*(per year|annually|/year|annual)"

# 股票/股权
"(stock|equity|RSU|option|grant).*?(\$?\d{2,3}k?)"

# 奖金
"(bonus|signing|target).*?(\$?\d{1,2}k?|\d{1,2}%)"

# 总薪酬
"(total compensation|TC|OTE).*?(\$?\d{2,3}k?)"
```

**薪资结构分析**:
```json
{
  "salary_analysis": {
    "base_salary": {
      "range": "$150,000 - $200,000",
      "currency": "USD",
      "period": "yearly",
      "confidence": "high"
    },
    "equity": {
      "mentioned": true,
      "estimated_range": "$50,000 - $100,000/year",
      "type": "RSU",
      "vesting": "4 years"
    },
    "bonus": {
      "mentioned": true,
      "percentage": "20%",
      "estimated_value": "$30,000 - $40,000"
    },
    "total_compensation": {
      "estimated_range": "$230,000 - $340,000",
      "breakdown": ["Base: $150k-$200k", "Bonus: $30k-$40k", "Equity: $50k-$100k"]
    },
    "market_comparison": {
      "percentile": "75th",
      "comparison": "Above market average"
    }
  }
}
```

#### 地区薪资调整
```json
{
  "location_adjustments": {
    "SF Bay Area": 1.0,
    "New York": 0.95,
    "Seattle": 0.90,
    "Austin": 0.80,
    "Remote (US)": 0.85,
    "Beijing": 0.60,
    "Shanghai": 0.62
  }
}
```

### 增强的技能提取模式

#### AI/ML技能识别
```json
{
  "ai_ml_skills": {
    "machine_learning": ["Machine Learning", "ML", "Deep Learning", "Neural Networks"],
    "frameworks": ["TensorFlow", "PyTorch", "Keras", "Scikit-learn", "MXNet"],
    "nlp": ["NLP", "Natural Language Processing", "Transformers", "BERT", "GPT"],
    "computer_vision": ["Computer Vision", "CV", "Image Processing", "CNN"],
    "mlops": ["MLOps", "ML Engineering", "Model Deployment", "Feature Engineering"]
  }
}
```

#### 云平台技能
```json
{
  "cloud_skills": {
    "aws": ["AWS", "Amazon Web Services", "EC2", "S3", "Lambda", "RDS", "DynamoDB"],
    "gcp": ["GCP", "Google Cloud", "GKE", "BigQuery", "Cloud Functions"],
    "azure": ["Azure", "Microsoft Azure", "AKS", "Azure Functions"],
    "cloud_native": ["Kubernetes", "K8s", "Docker", "Helm", "Istio", "Service Mesh"]
  }
}
```

#### 数据技能
```json
{
  "data_skills": {
    "databases": ["SQL", "NoSQL", "PostgreSQL", "MySQL", "MongoDB", "Redis", "Cassandra"],
    "data_engineering": ["ETL", "Data Pipeline", "Spark", "Kafka", "Airflow", "Hadoop"],
    "analytics": ["Data Analysis", "Analytics", "Visualization", "Tableau", "Power BI"],
    "big_data": ["Big Data", "Distributed Computing", "Data Lakes", "Data Warehousing"]
  }
}
```

### 多语言JD支持

#### 语言检测
```json
{
  "language_detection": {
    "detected_language": "zh-CN",
    "confidence": 0.95,
    "supported_languages": ["en", "zh-CN", "zh-TW", "ja", "ko"],
    "translation_needed": false
  }
}
```

#### 双语JD处理
```json
{
  "bilingual_jd": {
    "primary_language": "en",
    "secondary_language": "zh-CN",
    "merge_strategy": "primary_first",
    "skill_extraction": {
      "from_primary": true,
      "from_secondary": true,
      "merge_duplicates": true
    }
  }
}
```

#### 跨语言技能映射
```json
{
  "skill_translation": {
    "machine_learning": {
      "en": "Machine Learning",
      "zh": "机器学习",
      "ja": "機械学習",
      "ko": "기계 학습"
    },
    "distributed_systems": {
      "en": "Distributed Systems",
      "zh": "分布式系统",
      "ja": "分散システム",
      "ko": "분산 시스템"
    }
  }
}
```

### 智能技能分组

#### 相关技能聚类
```json
{
  "skill_clusters": {
    "backend_development": {
      "skills": ["Python", "Java", "Go", "APIs", "Microservices"],
      "weight": 2.0,
      "priority": "high"
    },
    "data_processing": {
      "skills": ["SQL", "ETL", "Kafka", "Spark"],
      "weight": 1.5,
      "priority": "medium"
    },
    "frontend": {
      "skills": ["React", "JavaScript", "TypeScript", "HTML/CSS"],
      "weight": 1.0,
      "priority": "low"
    }
  }
}
```

#### 技能依赖关系分析
```json
{
  "skill_dependencies": {
    "Kubernetes": {
      "prerequisites": ["Docker", "Linux", "Networking"],
      "related": ["Helm", "Istio", "Prometheus"],
      "advanced": ["Cloud Native", "Service Mesh"]
    },
    "Machine Learning": {
      "prerequisites": ["Python", "Statistics", "Linear Algebra"],
      "related": ["Deep Learning", "MLOps", "Data Engineering"],
      "advanced": ["Neural Networks", "Computer Vision", "NLP"]
    }
  }
}
```

### 隐含技能要求识别

#### 基于职责推断技能
```json
{
  "inferred_skills": {
    "from_responsibility": "Design and build scalable web applications",
    "inferred_skills": [
      {"skill": "Web Development", "confidence": 0.95},
      {"skill": "API Design", "confidence": 0.90},
      {"skill": "Scalability", "confidence": 0.85},
      {"skill": "Performance Optimization", "confidence": 0.80}
    ],
    "reasoning": "Building scalable web apps requires these core skills"
  }
}
```

#### 基于项目规模推断经验
```json
{
  "scale_inference": {
    "indicators": ["millions of users", "petabytes of data", "high QPS"],
    "inferred_requirements": [
      {"skill": "Distributed Systems", "importance": "critical"},
      {"skill": "Scalability", "importance": "critical"},
      {"skill": "Performance Tuning", "importance": "high"},
      {"skill": "System Design", "importance": "high"}
    ]
  }
}
```

### 市场需求分析

#### 技能趋势分析
```json
{
  "market_analysis": {
    "skill_demand": {
      "Distributed Systems": {
        "demand_level": "high",
        "trend": "increasing",
        "market_saturation": "low"
      },
      "Kubernetes": {
        "demand_level": "very_high",
        "trend": "stable",
        "market_saturation": "medium"
      }
    },
    "competitiveness": {
      "score": 75,
      "interpretation": "Moderately competitive position",
      "recommendations": [
        "Strengthen distributed systems fundamentals",
        "Gain hands-on Kubernetes experience",
        "Build system design portfolio"
      ]
    }
  }
}
```

### 增强的输出格式

#### 完整的JD分析报告
```json
{
  "jd_analysis_report": {
    "metadata": {
      "company": "Example Tech",
      "position": "Senior Software Engineer",
      "analysis_date": "2024-01-15T10:00:00Z",
      "jd_language": "en",
      "confidence_score": 0.92
    },

    "basic_info": {
      "title": "Senior Software Engineer",
      "level": "L4-L5",
      "department": "Cloud Infrastructure",
      "location": "Remote / SF",
      "employment_type": "Full-time"
    },

    "culture_analysis": {
      "culture_type": "Innovative & Data-driven",
      "key_traits": ["Fast-paced", "Collaborative", "Customer-obsessed"],
      "work_style": "Hybrid remote",
      "team_size": "5-10 engineers"
    },

    "compensation": {
      "base_salary": "$180k-$220k",
      "equity": "$80k-$120k/year",
      "bonus": "20% target",
      "total_range": "$280k-$360k",
      "market_position": "75th percentile"
    },

    "skills": {
      "required": [
        {"skill": "Python", "weight": 2.0, "proficiency": "advanced"},
        {"skill": "Distributed Systems", "weight": 2.0, "proficiency": "advanced"},
        {"skill": "Kubernetes", "weight": 2.0, "proficiency": "intermediate"}
      ],
      "preferred": [
        {"skill": "Go", "weight": 1.0, "proficiency": "intermediate"},
        {"skill": "ML Engineering", "weight": 1.0, "proficiency": "intermediate"}
      ]
    },

    "skill_match_analysis": {
      "overall_match": 85.5,
      "matched_skills": 7,
      "partial_match": 3,
      "missing_skills": 2,
      "gap_analysis": {
        "critical_gaps": ["Kubernetes depth"],
        "nice_to_have": ["Go proficiency"],
        "recommendations": ["Take Kubernetes course", "Build Go side project"]
      }
    },

    "readiness_assessment": {
      "technical_readiness": 80,
      "experience_match": 85,
      "culture_fit": 90,
      "overall_score": 85,
      "ready_to_apply": true,
      "prep_time_estimate": "2-3 weeks"
    }
  }
}
```

### 分析质量保证

**验证检查项**:
- [ ] 所有关键技能已识别
- [ ] 薪资信息已提取（如存在）
- [ ] 文化指标已分析
- [ ] 隐含技能已推断
- [ ] 匹配度计算准确
- [ ] 建议具有可操作性
- [ ] 多语言支持正确
- [ ] 输出格式符合Schema

**置信度评分**:
```
高置信度 (90%+): 清晰的技能描述，明确的要求
中置信度 (70-89%): 有一些歧义，需要推断
低置信度 (<70%): JD描述模糊，信息不完整
```
