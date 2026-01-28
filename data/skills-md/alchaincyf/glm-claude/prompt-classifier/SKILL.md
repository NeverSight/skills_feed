---
name: prompt-classifier
description: 自动识别prompt类型并保存到相应分类（技术/内容/教学/产品/通用），支持自动文件命名和索引管理。当用户提到"保存prompt"、"记录prompt"、"管理prompt"、"整理prompt"、"prompt库"时使用此技能。
---

# Prompt分类保存

## 何时使用此Skill
当用户出现以下任一需求时，使用此技能：
- 需要"保存prompt"、"记录prompt"
- 希望"管理prompt"、"整理prompt"
- 想要建立"prompt库"、"prompt合集"
- 需要给prompt"分类"、"打标签"
- 要求prompt"自动保存"、"批量管理"

## 核心目标
自动识别prompt类型，分类保存到标准化的目录结构中，并提供统一的索引管理，让用户能够快速找到和重用高质量的prompt。

## 执行流程

### 第一步：Prompt类型识别
**目标**：准确判断prompt的用途和分类

**识别标准**：
1. **技术类 (Technical)**
   - 代码编写、调试、优化
   - 系统设计、架构讨论
   - 技术问题解答、方案设计
   - 关键词：代码、开发、技术、系统、程序

2. **内容类 (Content)**
   - 文章写作、内容创作
   - 文案策划、营销内容
   - 博客文章、社交媒体内容
   - 关键词：写作、内容、文案、文章、创作

3. **教学类 (Educational)**
   - 知识讲解、概念说明
   - 教程编写、学习指导
   - 问题解答、知识梳理
   - 关键词：教学、讲解、教程、学习、知识

4. **产品类 (Product)**
   - 产品设计、功能规划
   - 用户体验、交互设计
   - 产品分析、竞品研究
   - 关键词：产品、设计、用户体验、功能

5. **通用类 (General)**
   - 通用任务、跨领域应用
   - 综合性、多用途prompt
   - 无法明确分类的prompt
   - 关键词：通用、综合、万能、多用途

### 第二步：自动文件命名
**目标**：生成标准化的文件名

**命名规则**：
```
格式：[分类前缀]_[功能描述]_[版本].md

分类前缀：
- tech_    技术类
- content_ 内容类
- edu_     教学类
- product_ 产品类
- general_ 通用类
```

**命名示例**：
```
tech_api_debugging_v1.md
content_blog_post_outline_v1.md
edu_concept_explanation_v1.md
product_user_flow_design_v1.md
general_task_planning_v1.md
```

### 第三步：内容结构化保存
**目标**：按标准格式保存prompt内容

**文件结构模板**：
```markdown
# [Prompt标题]

## 分类
[技术/内容/教学/产品/通用]

## 用途描述
[简要说明prompt的用途和适用场景]

## Prompt内容
```
[prompt的具体内容]
```

## 使用示例
[给出1-2个使用示例]

## 标签
[相关标签，用逗号分隔]

## 创建时间
[YYYY-MM-DD HH:MM:SS]

## 最后更新
[YYYY-MM-DD HH:MM:SS]

## 使用次数
[记录使用次数]

## 效果评价
[记录使用效果，1-5分]
```

### 第四步：目录结构创建
**目标**：建立标准的存储目录结构

**目录结构**：
```
prompts/
├── README.md                    # 总览文档
├── index.md                     # 索引文件
├── technical/                   # 技术类prompt
│   ├── api_debugging_v1.md
│   ├── code_review_v1.md
│   └── ...
├── content/                     # 内容类prompt
│   ├── blog_post_v1.md
│   ├── social_media_v1.md
│   └── ...
├── educational/                 # 教学类prompt
│   ├── concept_explain_v1.md
│   ├── tutorial_v1.md
│   └── ...
├── product/                     # 产品类prompt
│   ├── user_research_v1.md
│   ├── feature_design_v1.md
│   └── ...
└── general/                     # 通用类prompt
    ├── task_planning_v1.md
    ├── brainstorm_v1.md
    └── ...
```

### 第五步：索引文件更新
**目标**：自动更新全局索引文件

**索引格式**：
```markdown
# Prompt库索引

## 分类统计
- 技术类：X个
- 内容类：X个
- 教学类：X个
- 产品类：X个
- 通用类：X个
- 总计：X个

## 最新添加
1. [文件名] - [分类] - [创建时间] - [用途]
2. ...

## 按分类浏览

### 技术类
- [api_debugging_v1.md](technical/api_debugging_v1.md) - API调试助手
- [code_review_v1.md](technical/code_review_v1.md) - 代码审查助手

### 内容类
- [blog_post_v1.md](content/blog_post_v1.md) - 博客文章生成
- ...

## 按标签浏览
[生成热门标签云]

## 搜索提示
使用关键词搜索时，建议搜索：
- 功能关键词（如：调试、写作、设计）
- 应用场景（如：面试、营销、教学）
- 技术栈（如：Python、React、数据库）
```

## 特殊处理机制

### 1. 重复检测
**检测逻辑**：
- 计算prompt内容的相似度
- 相似度 > 80% 视为重复
- 提示用户是否覆盖或更新

**处理方式**：
```
检测到相似prompt：
- 已存在：tech_api_debugging_v1.md
- 相似度：85%
- 操作选择：
  1. 覆盖现有文件
  2. 创建新版本（v2）
  3. 保存为不同名称
```

### 2. 版本管理
**版本规则**：
- 相似功能但内容不同的：创建新版本
- 内容完全相同的：提示重复
- 功能相似的：关联推荐

### 3. 质量评估
**评估维度**：
- **完整性**：是否有明确的目标和指令
- **清晰度**：表达是否清楚无歧义
- **实用性**：是否解决实际问题
- **创新性**：是否有独特的思路

**评级标准**：
- ⭐⭐⭐⭐⭐ 优秀：值得收藏和分享
- ⭐⭐⭐⭐ 良好：有实用价值
- ⭐⭐⭐ 一般：可以使用但可优化
- ⭐⭐ 较差：需要大幅改进
- ⭐ 不推荐：不建议使用

## 批量操作功能

### 1. 批量导入
```bash
# 支持批量导入现有prompt
glm prompts import /path/to/prompts/
```

### 2. 批量分类
```bash
# 自动分类未分类的prompt
glm prompts classify --all
```

### 3. 批量导出
```bash
# 导出特定分类的prompt
glm prompts export --category technical
```

## 使用建议

### 1. 命名规范
- 使用描述性的文件名
- 避免特殊字符和空格
- 版本号清晰标识

### 2. 内容管理
- 定期整理和更新
- 删除不再需要的prompt
- 优化低质量的prompt

### 3. 共享机制
- 优质prompt可分享给团队
- 建立团队共享库
- 定期同步更新

## 质量标准
- 分类准确率 >= 95%
- 文件命名规范性 = 100%
- 索引更新及时性 = 100%
- 重复检测准确率 >= 90%

---
*最后更新：2024年*