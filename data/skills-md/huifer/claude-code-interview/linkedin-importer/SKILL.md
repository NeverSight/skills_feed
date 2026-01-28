---
name: linkedin-importer
description: LinkedIn职位导入器。解析LinkedIn职位发布，提取JD和公司信息，批量导入求职系统。
allowed-tools: mcp__web_reader__webReader, Read, Write, Skill
---

# LinkedIn Importer Skill

智能导入LinkedIn职位发布到求职系统。

## 核心功能

### 1. LinkedIn URL解析
### 2. JD文本提取
### 3. 公司信息识别
### 4. 自动调用jd-analyzer
### 5. 批量导入支持

## 使用方法

### 从LinkedIn URL导入单个JD
```markdown
User: "帮我导入这个LinkedIn职位：https://www.linkedin.com/jobs/view/123456789/"

LinkedIn Importer:
✅ 开始导入LinkedIn职位...

Step 1/4: 读取LinkedIn页面...
  - URL: https://www.linkedin.com/jobs/view/123456789/
  - 状态: 成功
  - 提取: 2,456 字符

Step 2/4: 识别公司和职位...
  - 公司: Google ✅
  - 职位: Software Engineer III, Cloud Platform ✅
  - 级别: L4 (推断) ✅
  - 地点: Mountain View, CA / Remote ✅

Step 3/4: 提取JD详细信息...
  - 职位描述: 已提取 ✅
  - 技能要求: 7项必需 + 4项优先 ✅
  - 薪资信息: 未公开 ⚠️
  - 申请状态: Applied

Step 4/4: 分析并保存...
  - 调用: jd-analyzer skill
  - 技能匹配度: 75/100 ✅
  - 保存到: data/companies/google.json ✅

✅ 导入完成！

📊 导入摘要:
  公司: Google
  职位: Software Engineer III, Cloud Platform (L4)
  地点: Mountain View, CA / Remote
  匹配度: 75/100
  来源: LinkedIn

💡 下一步:
  1. /company/view google - 查看完整信息
  2. /resume/optimize google sse-l4 - 创建定制简历
  3. /interview/prep google - 准备面试
```

### 从文本粘贴导入
```markdown
User: "我复制了LinkedIn上的JD，能帮我导入吗？"

LinkedIn Importer:
当然可以！请粘贴JD文本，我会帮你解析和导入。

[用户粘贴JD文本]

✅ JD文本已接收！

正在分析...
  - 识别公司: Meta (Facebook)
  - 识别职位: Production Engineer II
  - 提取技能: 9项

调用jd-analyzer进行深度分析...

✅ 分析完成！

📊 分析结果:
  公司: Meta
  职位: Production Engineer II (E4)
  匹配度: 68/100
  必需技能: 7项
  优先技能: 4项

💡 建议:
  - 缺少技能: Kubernetes (需补充)
  - 优势技能: Distributed Systems (匹配)
  - 面试重点: 系统设计 + 生产环境问题

已保存到: data/companies/meta.json

下一步:
  - /resume/optimize meta pe-e4
  - /weakness/plan --focus kubernetes
```

### 批量导入LinkedIn职位
```markdown
User: "我有5个LinkedIn职位链接，能批量导入吗？"

LinkedIn Importer:
可以！请提供所有LinkedIn职位URL，我会逐个导入。

[用户提供5个URL]

✅ 开始批量导入...

Progress: [████████░░] 80% (4/5)

✅ 1. Google - Software Engineer L4
  - 状态: 导入成功
  - 匹配度: 75/100
  - 保存: data/companies/google.json

✅ 2. Amazon - Senior SDE L5
  - 状态: 导入成功
  - 匹配度: 82/100
  - 保存: data/companies/amazon.json

✅ 3. Meta - Production Engineer E4
  - 状态: 导入成功
  - 匹配度: 68/100
  - 保存: data/companies/meta.json

✅ 4. Stripe - Software Engineer
  - 状态: 导入成功
  - 匹配度: 70/100
  - 保存: data/companies/stripe.json

⚠️ 5. Netflix - Senior Backend Engineer
  - 状态: 部分成功
  - 问题: 公司识别失败
  - 解决: 手动确认为 "Netflix"
  - 匹配度: 72/100
  - 保存: data/companies/netflix.json

✅ 批量导入完成！

📊 导入摘要:
  总计: 5 个职位
  成功: 5 个 (100%)
  失败: 0 个

按匹配度排序:
  1. Amazon L5 - 82% ⭐⭐⭐
  2. Google L4 - 75% ⭐⭐⭐
  3. Netflix - 72% ⭐⭐
  4. Stripe - 70% ⭐⭐
  5. Meta E4 - 68% ⭐⭐

💡 批量操作建议:
  - 优先准备Amazon（最高匹配）
  - 本周申请: Amazon, Google
  - 下周申请: Stripe, Meta
  - 研究Netflix后再决定

是否需要我:
  1. 生成本周申请计划?
  2. 为每个公司优化简历?
  3. 创建面试准备时间表?
```

## LinkedIn URL格式处理

### 支持的URL格式
```markdown
## 🔗 LinkedIn URL Formats

### 标准职位查看URL
```
https://www.linkedin.com/jobs/view/[job-id]/
https://www.linkedin.com/jobs/view/123456789/
```

### 职位详情URL
```
https://www.linkedin.com/jobs/search/?currentJobId=[job-id]
https://www.linkedin.com/jobs/collections/recommended/123456789/
```

### 公司页面职位
```
https://www.linkedin.com/jobs/search/?f_C=[company-id]%2C[company-id]
```

### 移动端URL
```
https://www.linkedin.com/jobs/view/123456789/fromMobile
https://www.linkedin.com/jobs/view/123456789/refId=xxx
```

### 处理逻辑:
1. 提取job-id（URL中的数字ID）
2. 构造标准API URL
3. 读取职位详情页面
4. 解析职位信息
5. 提取JD内容
```

## JD内容提取

### LinkedIn页面结构
```markdown
## 📄 LinkedIn JD Extraction

### 页面结构
```html
<div class="description__text">
  <h2>About the job</h2>
  <p>[职位描述内容]</p>

  <h3>Qualifications</h3>
  <ul>
    <li>[技能要求1]</li>
    <li>[技能要求2]</li>
  </ul>

  <h3>Additional Information</h3>
  <p>[额外信息]</p>
</div>
```

### 提取字段
- **职位名称**: `<h1 class="top-card-layout__title">`
- **公司名称**: `<a class="topcard__org-name-link">`
- **地点**: `<span class="job-criteria__text">`
- **职位类型**: `<span class="job-criteria__text">`
- **工作经验**: `<span class="job-criteria__text">`
- **职位描述**: `<div class="description__text">`
- **发布时间**: `<span class="posted-time">`
- **申请人数**: `<span class="applicant-count">`
- **薪资信息**: `<span class="salary-cmp">` (如果提供)

### 清理步骤
1. 移除HTML标签
2. 清理多余空白
3. 移除LinkedIn特定的UI文本
4. 格式化为结构化JSON
5. 保留关键段落分隔
```

## 公司信息识别

### 智能公司识别
```markdown
## 🏢 Company Detection

### 方法 1: 从URL提取
```
LinkedIn公司URL: https://www.linkedin.com/company/google/

提取: "google"
```

### 方法 2: 从JD文本识别
```python
patterns = [
    r"at (Apple|Google|Microsoft|Amazon|Meta)",
    r"(Google|Amazon|Microsoft|Meta|Apple)'s",
    r"Join (Apple|Google|Microsoft|Amazon|Meta)",
    # ... 更多模式
]
```

### 方法 3: 职位标题推断
```
"Google Cloud Platform Engineer" → Google
"Amazon Web Services SDE" → Amazon
"Meta Production Engineer" → Meta
```

### 公司名称标准化
```markdown
常见变体 → 标准名称:
- "Google Inc." → "Google"
- "Google (Alphabet)" → "Google"
- "Amazon.com" → "Amazon"
- "Amazon Web Services" → "Amazon"
- "Meta (Facebook)" → "Meta"
- "Facebook" → "Meta"
- "M$" → "Microsoft"
- "Stripe, Inc." → "Stripe"
```

### 公司ID映射
```json
{
  "google": {
    "company_id": "google",
    "linkedin_id": "1441",
    "name": "Google",
    "careers_url": "careers.google.com"
  },
  "amazon": {
    "company_id": "amazon",
    "linkedin_id": "1061",
    "name": "Amazon",
    "careers_url": "jobs.amazon.com"
  },
  "meta": {
    "company_id": "meta",
    "linkedin_id": "1035",
    "name": "Meta",
    "careers_url": "careers.meta.com"
  }
}
```

## 级别推断

### 职位级别推断
```markdown
## 📊 Level Inference

### Google级别映射
```
Software Engineer II → L3
Software Engineer III → L4
Senior Software Engineer → L5
Staff Software Engineer → L6
Senior Staff SE → L7
Principal Engineer → L8
```

### Amazon级别映射
```
Software Dev Engineer I → SDE I (L4)
Software Dev Engineer II → SDE II (L5)
Senior SDE → Senior SDE (L6)
Principal SDE → Principal (L7)
Senior Principal → Sr Principal (L8)
```

### Meta级别映射
```
Software Engineer (E3) → Junior
Software Engineer (E4) → Mid-level
Senior Software Engineer (E5) → Senior
Staff Software Engineer (E6) → Staff
Senior Staff SE (E7) → Senior Staff
```

### 通用级别推断
```
关键词 → 级别:
- "Junior", "Associate", "Entry level" → Junior
- "Software Engineer", "Developer" → Mid-level
- "Senior", "Lead" → Senior
- "Staff", "Principal" → Staff/Principal
- "Director", "VP" → Executive
```

### 年限要求映射
```
"1-2 years experience" → Junior
"2-4 years experience" → Mid-level
"5+ years experience" → Senior
"8+ years experience" → Staff/Principal
```

## 批量导入功能

### 从CSV文件导入
```markdown
User: "我有一个CSV文件包含LinkedIn URL"

LinkedIn Importer:
可以！请提供CSV文件路径或内容。

CSV格式要求:
```csv
company,position,url,status,applied_date
Google,Software Engineer,https://linkedin.com/jobs/123,applied,2024-01-15
Amazon,SDE II,https://linkedin.com/jobs/456,applying,2024-01-16
```

或使用文件:
```bash
/linkedin-import --batch jobs.csv
```

处理流程:
1. 读取CSV文件
2. 逐个导入LinkedIn职位
3. 自动识别公司
4. 更新申请状态
5. 生成批量导入报告
```

### 从文本列表导入
```markdown
User: "我复制了多个LinkedIn URL"

LinkedIn Importer:
请粘贴所有URL，每行一个：

```
https://www.linkedin.com/jobs/view/123456789/
https://www.linkedin.com/jobs/view/987654321/
https://www.linkedin.com/jobs/view/456789123/
```

✅ 收到3个URL，开始导入...

[导入过程...]

✅ 导入完成！
```

## 与jd-analyzer集成

### 自动分析流程
```markdown
## 🔗 Integration with jd-analyzer

LinkedIn Importer工作流:

1. **提取LinkedIn JD**
   - 读取LinkedIn页面
   - 提取职位描述文本
   - 识别公司和职位信息

2. **调用jd-analyzer**
   - 自动传递JD文本
   - 返回结构化分析
   - 技能匹配评分

3. **保存到数据文件**
   - 创建/更新 company.json
   - 保存完整分析结果
   - 记录导入来源

### 数据流向
```
LinkedIn URL
    ↓
linkedin-importer (提取文本)
    ↓
jd-analyzer (分析技能)
    ↓
data/companies/{company}.json (保存)
    ↓
user (查看结果)
```

## 错误处理

### 常见问题和解决方案
```markdown
## ⚠️ Error Handling

### 错误 1: URL无法访问
```
原因: LinkedIn限制访问或URL失效
解决方案:
  1. 检查URL是否正确
  2. 尝试手动登录LinkedIn后访问
  3. 复制JD文本使用粘贴导入
  4. 使用Indeed或其他来源的相同职位
```

### 错误 2: 公司识别失败
```
原因: LinkedIn页面公司信息不明确
解决方案:
  1. 使用 --company 手动指定公司
  2. 从职位标题推断
  3. 交互式确认公司名称
```

### 错误 3: JD提取不完整
```
原因: LinkedIn动态加载或特殊格式
解决方案:
  1. 使用粘贴完整JD文本
  2. 增加timeout参数
  3. 手动复制粘贴关键部分
```

### 错误 4: 批量导入部分失败
```
原因: 部分URL无效或访问受限
解决方案:
  1. 继续处理其他URL
  2. 标记失败的URL
  3. 生成失败报告
  4. 逐个重试失败的项
```
```

## 高级功能

### 智能去重
```markdown
## 🔍 Duplicate Detection

### 检测重复
同一职位的判断标准:
1. 相同公司 + 相同职位名称
2. 相同LinkedIn Job ID
3. 相似度 > 90% (JD文本相似度)

### 处理重复
```
检测到重复:
  - 原有JD: Google SE III (导入于 2024-01-10)
  - 新JD: Google SE III (2024-01-15)

选择:
  1. 跳过（保留原有）
  2. 更新（替换为新的）
  3. 创建版本（保留两个版本）
```
```

### LinkedIn特定字段提取
```markdown
## 📊 LinkedIn-Specific Fields

### 申请人数
```
Applicants: 145
Your percentile: Top 30%
```
用途: 评估竞争激烈程度

### 发布时间
```
Posted 2 days ago
```
用途: 判断职位新鲜度

### 容易申请标志
```
"Easy Apply" ✅
```
用途: 一键申请

### 查看人数
```
85 people viewed this job in the past month
```
用途: 评估职位热度
```

## 数据输出

### 保存的数据结构
```json
{
  "company_id": "google",
  "job_applications": {
    "sse-l4-linkedin": {
      "source": "LinkedIn",
      "source_url": "https://www.linkedin.com/jobs/view/123456789/",
      "job_id": "123456789",
      "title": "Software Engineer III, Cloud Platform",
      "inferred_level": "L4",
      "location": "Mountain View, CA / Remote",
      "description_source": "LinkedIn",
      "imported_at": "2024-01-15T14:30:00Z",
      "last_updated": "2024-01-15T14:30:00Z",
      "application_status": "applied",
      "applied_date": "2024-01-15",
      "linkedin_specific": {
        "easy_apply": true,
        "applicants": 145,
        "applicant_percentile": "Top 30%",
        "posted_date": "2024-01-13",
        "views_past_month": 85
      }
    }
  }
}
```

## 性能优化

### 批量导入优化
```markdown
## ⚡ Performance Optimization

### 并发处理
- 单线程: 10个URL = ~60秒
- 并发(3): 10个URL = ~25秒
- 并发(5): 10个URL = ~18秒

推荐: 并发3-5（避免被LinkedIn限制）

### 缓存策略
```
已导入的JD → 缓存24小时
相同URL → 跳过或更新
```

### 增量更新
```
仅更新变化的部分:
- 如果JD未变化 → 跳过
- 如果有新申请 → 更新状态
- 如果职位关闭 → 标记状态
```
```

## 最佳实践

### 使用建议
```markdown
## 💡 Best Practices

### 1. 批量导入策略
- 一次导入5-10个职位（太多会混乱）
- 按优先级排序（匹配度高的优先）
- 分批处理（不同类型的职位分开）

### 2. 数据质量
- 总是检查识别的公司名称是否正确
- 确认职位级别推断是否准确
- 验证技能提取是否完整

### 3. 后续操作
- 导入后立即查看分析结果
- 根据匹配度优先排序
- 为高匹配度职位优化简历
- 制定申请时间表

### 4. 定期更新
- 每周重新导入（检查状态变化）
- 更新申请进度
- 标记已关闭的职位
```

## 相关命令和技能

- `/jd-import` - 通用JD导入（支持更多平台）
- `jd-analyzer` skill - JD分析
- `resume-optimizer` skill - 简历优化
- `/company/view` - 查看公司信息
- `/analytics/market` - 市场情报

---

**Pro Tip**: LinkedIn职位变化很快，建议每周重新检查申请状态，及时更新进度。Good luck with your applications! 🚀
