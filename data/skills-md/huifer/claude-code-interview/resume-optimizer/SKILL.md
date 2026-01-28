---
name: resume-optimizer
description: 优化和定制简历以匹配特定公司和职位。分析JD，提取关键技能，重新排序经验，突出相关成就。用于创建简历变体、优化关键词、提升ATS通过率。当用户创建简历变体或优化简历时自动触发。
allowed-tools: Read, Write, Grep, Edit
---

# Resume Optimizer Skill

## 触发条件
当用户需要：
- 为特定公司定制简历
- 优化简历关键词
- 提升简历与JD的匹配度
- 生成简历变体
- 提高ATS（Applicant Tracking System）通过率

## 工作流程

### 步骤 1: JD分析
使用 jd-analyzer Skill 提取：
- 必需技能列表
- 优先技能列表
- 关键词和短语
- 公司文化和技术栈

### 步骤 2: 技能匹配
读取 `data/resume/base.json` 并：
- 识别匹配的技能
- 识别相关经验
- 识别相关项目
- 评估整体匹配度

### 步骤 3: 内容优化
针对目标公司调整简历：

#### 3.1 技能部分优化
```json
{
  "optimizations": {
    "highlighted_skills": [
      "Distributed Systems",
      "Machine Learning",
      "Python",
      "Go"
    ],
    "skills_reorder": {
      "programming_languages": ["Python", "Go", "Java"],
      "concepts": ["Microservices", "Cloud Computing", "System Design"]
    }
  }
}
```

#### 3.2 工作经验优化
- 重新排序（最相关的在前）
- 调整成就描述，使用JD关键词
- 突出相关项目和技术
- 量化成果

#### 3.3 项目经验优化
- 优先显示与JD最相关的项目
- 使用JD中的技术术语
- 突出影响力和成果
- 链接到相关技术

#### 3.4 Summary优化
- 针对公司文化定制
- 突出最相关的2-3个技能
- 体现与公司的匹配度
- 保持简洁（2-3行）

### 步骤 4: 关键词优化
#### 插入JD关键词的原则：
- 自然融入，不堆砌
- 放在成就描述中
- 使用同义词变体
- 保持专业性

#### 动作动词（Action Verbs）：
**技术类**：
- Designed, Implemented, Developed
- Architected, Engineered, Built
- Optimized, Refactored, Improved
- Deployed, Scaled, Launched

**管理类**：
- Led, Mentored, Guided
- Collaborated, Partnered
- Spearheaded, Championed
- Directed, Oversaw

**成就类**：
- Delivered, Shipped, Released
- Increased, Decreased, Reduced
- Achieved, Attained, Exceeded
- Won, Earned, Recognized

### 步骤 5: 输出简历变体
创建 `data/resume/variants/{company}.json`：

```json
{
  "variant_id": "google",
  "parent_resume": "base.json",
  "created_at": "2025-01-09T00:00:00Z",
  "updated_at": "2025-01-09T00:00:00Z",
  "target_company": "google",
  "target_position": "Software Engineer III",

  "optimizations": {
    "highlighted_skills": [...],
    "emphasized_projects": ["proj_001"],
    "tailored_summary": "...",
    "keywords_to_emphasize": [...],
    "de_emphasized_sections": ["certifications"],
    "reordered_sections": [
      "skills",
      "projects",
      "work_experience",
      "education"
    ]
  },

  "modifications": {
    "summary": {
      "original": "资深软件工程师...",
      "optimized": "资深软件工程师，专注于分布式系统和机器学习..."
    },
    "work_experience": {
      "exp_001": {
        "achievements_modified": [
          {
            "original": "优化系统性能",
            "optimized": "设计并实现高并发订单处理系统，处理能力提升300%，支持分布式部署"
          }
        ]
      }
    }
  }
}
```

## 优化策略

### 1. 技能突出策略
#### 完全匹配的技能（优先级最高）
- 放在技能列表最前面
- 在Summary中提及
- 在多个经验中体现

#### 部分匹配的技能
- 说明可迁移能力
- 强调学习经历
- 展示相关项目

#### 缺失的关键技能
- 在学习经历中提及
- 展示自学能力
- 相关技能类比

### 2. 经验排序策略
#### 相关性评分因素：
- 技术栈匹配度
- 项目规模相似度
- 行业相关性
- 成果可量化程度

### 3. 关键词密度
- Summary: 2-3个核心关键词
- 每段经验: 1-2个关键词
- 技能部分: 所有JD关键词
- 项目描述: 技术关键词

### 4. ATS优化
- 使用标准职位名称
- 避免特殊字符和图形
- 使用常见缩写（全称+缩写）
- 简洁的格式
- 避免表格和列

## 公司特定优化

### Google
**重点突出**：
- Scalability
- Reliability
- Distributed Systems
- "Googley"文化（好奇、学习、同理心）
- 技术卓越

**关键词**：
- Large-scale systems
- High-availability
- Cloud computing
- Data engineering
- Machine learning

### Meta
**重点突出**：
- 快速迭代
- 影响力（Impact）
- 基础设施
- 开源贡献

**关键词**：
- Move fast, ship code
- Impact at scale
- Infrastructure
- Performance
- Open source

### Amazon
**重点突出**：
- 客户导向
- 所有权精神
- 可扩展性
- 可用性

**关键词**：
- Customer Obsession
- Ownership
- Scalability
- Availability
- Distributed systems

### 初创公司
**重点突出**：
- 全栈能力
- 快速学习
- 多面手
- 创业精神

**关键词**：
- Full-stack
- End-to-end
- Fast-paced
- Wear multiple hats
- Self-starter

## 简历变体创建检查清单

- [ ] 读取并分析JD
- [ ] 提取关键技能和关键词
- [ ] 匹配用户技能
- [ ] 重新排序技能（最相关在前）
- [ ] 优化Summary（2-3行，突出核心匹配）
- [ ] 调整工作经验顺序
- [ ] 重写成就描述（使用JD关键词）
- [ ] 突出相关项目
- [ ] 检查关键词密度
- [ ] 验证ATS友好性
- [ ] 保存变体文件
- [ ] 生成匹配度报告

## 质量标准

### 优秀简历变体的特征：
1. **针对性**: 明确针对目标公司和职位
2. **真实性**: 所有内容真实可信
3. **量化性**: 成就可以量化
4. **简洁性**: 每个要点简洁明了
5. **一致性**: 风格和术语一致
6. **完整性**: 没有拼写或语法错误

### 避免的错误：
1. **过度堆砌关键词**: 不自然地重复关键词
2. **夸大或虚假**: 超出实际能力的描述
3. **忽略格式**: 不一致的格式和风格
4. **过于详细**: 每个要点超过2-3行
5. **忽略公司文化**: 没有考虑公司特色

## 与其他Skills的集成

### jd-analyzer
- 获取JD结构化分析
- 获取技能匹配报告
- 获取关键词列表

### interview-coach
- 提供优化后的简历信息
- 用于面试准备
- 识别需要深入准备的技能

### question-generator
- 基于优化后的技能
- 生成针对性面试题
- 优先级排序

## 输出示例

### 匹配度报告
```markdown
# Google - Software Engineer III 简历优化报告

## 匹配度评分: 85/100

### 完全匹配的技能 (7)
- Python (expert)
- Distributed Systems (advanced)
- Machine Learning (intermediate)
- Go (intermediate)
...

### 部分匹配的技能 (3)
- Java (intermediate, 需要advanced)
- Kubernetes (基础, 需要深入)
...

### 缺失的关键技能 (2)
- C++ (建议学习基础)
- gRPC (可以在项目中快速学习)

## 优化建议
1. 将Python和Distributed Systems放在技能列表最前面
2. 重新排序工作经历，突出分布式系统项目
3. 在成就描述中使用更多"scale", "reliable"等关键词
4. Summary中强调"大规模系统"和"机器学习"经验
```

## ATS优化增强（Phase 2新增）

### ATS系统识别与优化

不同的ATS系统有不同的解析特点，需要针对性优化：

#### 1. Workday (大公司广泛使用)
**特点**:
- 严格的结构化字段解析
- 善欢标准的日期格式
- 需要清晰的章节分隔

**优化策略**:
- 使用标准章节标题（Experience, Education, Skills）
- 避免创意性格式和布局
- 日期格式统一：YYYY-MM
- 联系信息放在顶部，使用标准标签
- 技能列表使用逗号分隔，而非复杂格式

**禁止**:
- ❌ 表格和列
- ❌ 图像和图标
- ❌ 复杂的嵌套列表
- ❌ 非标准字体

**推荐**:
- ✅ 简洁的单列布局
- ✅ 标准字体（Arial, Calibri, Times New Roman）
- ✅ 清晰的章节标题（全部大写或加粗）
- ✅ 电话使用格式：+86 138-1234-5678

#### 2. Greenhouse (科技公司常用)
**特点**:
- 更好的PDF解析能力
- 支持富文本格式
- 智能关键词提取

**优化策略**:
- 可以使用轻微的格式化（加粗、斜体）
- 重点关键词可以加粗强调
- 支持项目符号列表
- PDF导出时嵌入字体

**优势**:
- ✅ 支持超链接（LinkedIn, GitHub）
- ✅ 支持邮箱和电话的mailto/tel链接
- ✅ 更好的布局灵活性

#### 3. Lever (中型公司和初创公司)
**特点**:
- 现代化解析器
- 支持社交媒体链接
- 重视可读性

**优化策略**:
- 可以使用更现代的设计
- 突出个人品牌
- 强调文化契合度
- 添加项目作品集链接

**最佳实践**:
- ✅ 使用专业的简历模板
- ✅ 包含GitHub和项目链接
- ✅ 突出开源贡献
- ✅ 展示个人博客或技术文章

### 关键词密度分析与优化

#### 关键词分析流程：

**步骤1: 提取JD关键词**
```json
{
  "keyword_analysis": {
    "primary_keywords": [
      {"keyword": "Distributed Systems", "frequency": 8, "weight": 2.0},
      {"keyword": "Python", "frequency": 6, "weight": 2.0},
      {"keyword": "Kubernetes", "frequency": 5, "weight": 1.5}
    ],
    "secondary_keywords": [
      {"keyword": "Microservices", "frequency": 4, "weight": 1.0},
      {"keyword": "API Design", "frequency": 3, "weight": 1.0}
    ],
    "semantic_variations": [
      {"original": "Scalability", "variations": ["scale", "scalable", "scaling"]},
      {"original": "Reliability", "variations": ["reliable", "availability", "high-availability"]}
    ]
  }
}
```

**步骤2: 计算关键词密度**
- **Summary**: 目标 15-20% 关键词密度
- **Experience**: 目标 10-15% 关键词密度
- **Skills**: 目标 100% JD关键词覆盖
- **Projects**: 目标 20-25% 关键词密度

**步骤3: 关键词位置优化**
```markdown
# 高优先级位置：
1. Summary（前2行） - 最重要
2. 技能列表顶部 - ATS重点扫描
3. 最近工作的成就描述
4. 项目标题和描述

# 中优先级位置：
5. 工作经历标题
6. 教育背景相关课程
7. 认证和证书

# 低优先级位置：
8. 早期工作经验
9. 通用技能描述
```

**步骤4: 关键词自然度检查**
- ✅ 自然融入句子结构
- ✅ 使用上下文相关变体
- ✅ 避免重复同一短语
- ❌ 避免关键词堆砌
- ❌ 避免不相关的关键词插入

### 关键词优化示例

**原始描述**:
```
负责系统优化和性能提升
```

**优化后（针对Distributed Systems岗位）**:
```
设计并实现分布式系统架构，通过微服务拆分和负载均衡优化，
将系统处理能力提升300%，支持高并发场景下的数据一致性保证。
```

**包含的关键词**:
- 分布式系统 (Distributed Systems)
- 微服务 (Microservices)
- 负载均衡 (Load Balancing)
- 高并发 (High Concurrency)
- 数据一致性 (Data Consistency)

### PDF生成与导出

#### PDF导出最佳实践

**推荐工具**:
1. **Markdown to PDF**:
   - 使用 `wkhtmltopdf` 或 `pandoc`
   - 保持格式一致性
   - 嵌入标准字体

2. **LaTeX模板**:
   - 专业排版
   - 完全可定制
   - 适合技术岗位

3. **在线工具**:
   - Resume.io
   - Canva（专业模板）
   - Overleaf（LaTeX）

#### PDF导出检查清单

**格式检查**:
- [ ] 字体大小：正文10-12pt，标题14-16pt
- [ ] 页边距：0.5-1英寸
- [ ] 行间距：1.0-1.15
- [ ] 页面长度：1-2页（首选1页）
- [ ] 文件大小：< 1MB

**内容检查**:
- [ ] 所有链接可点击
- [ ] 联系信息准确
- [ ] 无拼写或语法错误
- [ ] 日期格式一致
- [ ] 专业邮箱地址

**ATS兼容性检查**:
- [ ] 使用标准字体
- [ ] 避免图像和图表
- [ ] 文本可选择（非扫描图片）
- [ ] 没有表格或列
- [ ] 文件名为: `FirstName_LastName_Resume.pdf`

**PDF元数据**:
```json
{
  "title": "Li Ming - Software Engineer Resume",
  "author": "Li Ming",
  "keywords": "Software Engineer, Python, Distributed Systems, Kubernetes",
  "creator": "Claude Code Interview System"
}
```

#### PDF导出命令示例

**使用pandoc**:
```bash
pandoc data/resume/base.md \
  -o exports/Li_Ming_Resume.pdf \
  --pdf-engine=xelatex \
  -V geometry:margin=1in \
  -V fontsize=11pt \
  --toc=false
```

**使用wkhtmltopdf**:
```bash
wkhtmltopdf \
  --margin-top 0.5in \
  --margin-bottom 0.5in \
  --margin-left 0.75in \
  --margin-right 0.75in \
  data/resume/base.html \
  exports/Li_Ming_Resume.pdf
```

### A/B测试与变体管理

#### 简历变体版本控制

**变体命名规范**:
```
{company}_{position}_{version}_{date}.json

示例:
google_sse_l4_v1_20240115.json
amazon_sde2_l5_v2_20240120.json
```

**变体对比功能**:
```json
{
  "comparison": {
    "variants": ["google_v1", "google_v2"],
    "metrics": {
      "keyword_density": {
        "v1": 12.5,
        "v2": 15.8,
        "improvement": "+26%"
      },
      "match_score": {
        "v1": 82,
        "v2": 89,
        "improvement": "+7"
      },
      "ats_compatibility": {
        "v1": "medium",
        "v2": "high"
      }
    },
    "recommendation": "使用v2版本，关键词密度更优"
  }
}
```

#### 变体效果追踪

**追踪指标**:
- 申请数量
- 面试邀请率
- 简历通过率
- ATS评分（如果可用）
- 获得offer数量

**数据结构**:
```json
{
  "variant_performance": {
    "variant_id": "google_v2",
    "applications_submitted": 5,
    "interviews_received": 3,
    "conversion_rate": 60.0,
    "offers": 1,
    "created_at": "2024-01-15",
    "last_used": "2024-01-20"
  }
}
```

### 高级优化技巧

#### 1. 语义关键词扩展
```json
{
  "skill_expansion": {
    "original": "Python",
    "expanded": [
      "Python",
      "Python 3",
      "PyPy",
      "Django",
      "Flask",
      "FastAPI",
      "Python编程"
    ]
  }
}
```

#### 2. 行业术语对齐
- 使用目标公司的术语体系
- 采用行业标准命名
- 包含流行技术栈的完整名称

#### 3. 量化成果增强
```markdown
弱: "优化了系统性能"
强: "通过分布式缓存和数据分片，将API响应时间从500ms降至50ms，
     提升90%，同时支持10x并发请求量"
```

#### 4. 动态摘要生成
基于JD动态调整Summary，突出最匹配的2-3个技能领域。

### 质量保证

**优化后验证**:
1. ✅ 所有JD关键词已包含
2. ✅ 关键词密度在目标范围内
3. ✅ ATS格式检查通过
4. ✅ 无虚假或夸大内容
5. ✅ 专业且易读
6. ✅ 文件大小合适
7. ✅ PDF导出测试通过

**评分系统**:
```
总分 100:
- 关键词匹配度 (30分)
- 内容质量 (25分)
- ATS兼容性 (20分)
- 专业性 (15分)
- 创新性 (10分)
```
