---
name: storyboard-master-gemini3
description: 使用 Gemini 3 Pro 的深度思考能力专业分析和优化影视分镜，提供结构化评估和改进建议
---

# 分镜大师 - Gemini 3 驱动的专业影视分镜分析工具

## 功能概述

利用 Gemini 3 Pro 的深度思考能力（thinking 功能），为影视创作者提供专业的分镜分析、评估和优化建议。支持电影、广告、MV、短视频等多种影视类型。

## API 配置

### 端点选择
```bash
# 生产环境
POST https://gpt-i18n.byteintl.net/gpt/openapi/online/v2/crawl?ak=${GEMINI3_API_KEY}

# 办公网络（需要时切换）
POST https://genai-sg-og.tiktok-row.org/gpt/openapi/online/v2/crawl?ak=${GEMINI3_API_KEY}
```

**注意**: 需要设置环境变量 `GEMINI3_API_KEY`

### 模型配置
- **模型**: `gemini-3-pro-preview-new`
- **thinking budget**: 8192（深度分析）
- **max_tokens**: 4096
- **include_thoughts**: true（显示思考过程）

## 核心分析提示词

```json
{
    "stream": false,
    "model": "gemini-3-pro-preview-new",
    "max_tokens": 4096,
    "messages": [
        {
            "role": "system",
            "content": "你是一位获奖的导演+摄影指导+分镜艺术家，拥有20年的行业经验。你精通视觉叙事、镜头语言、剪辑节奏和导演思维。你需要像专业电影人一样分析分镜，提供深度洞察和可执行的改进方案。"
        },
        {
            "role": "user",
            "content": "请专业分析以下分镜脚本：\n\n[分镜内容]\n\n分析框架：\n\n1. 【空间构成分析】\n   - 识别所有关键主体（人物/道具/环境元素）\n   - 分析空间关系（前景/中景/背景、左右分布、朝向）\n   - 评估场面调度（Staging）的效果\n\n2. 【镜头语言评估】\n   - 景别选择的合理性（ECU/CU/MS/FS/LS/ELS）\n   - 镜头运动设计（推拉摇移跟/手持/稳定器）\n   - 焦距建议（18/24/35/50/85/135mm）\n   - 景深运用和焦点转换\n\n3. 【叙事连贯性检查】\n   - 时空逻辑的清晰度\n   - 180度轴线规则遵守情况\n   - 视线匹配和动作连续性\n   - 情绪曲线和节奏变化\n\n4. 【剪辑预判分析】\n   - 镜头之间的衔接流畅度\n   - 剪辑点的选择合理性\n   - 转场方式的恰当性\n   - 整体节奏感评估\n\n5. 【制作可行性评估】\n   - 拍摄难度分级（1-5级）\n   - 设备需求清单\n   - 场地和道具要求\n   - 预算影响因素\n\n请提供：\n- 优势亮点（保持并强化）\n- 问题诊断（具体定位）\n- 优化方案（可执行步骤）\n- 参考案例（经典镜头借鉴）"
        }
    ],
    "thinking": {
        "include_thoughts": true,
        "budget_tokens": 8192
    }
}
```

## 分析维度详解

### 1. 镜头结构与逻辑
```
检查要点：
- 镜头序列的连贯性
- 场景转换的合理性
- 时空关系的清晰度
- 叙事线索的完整性
```

### 2. 视觉叙事效果
```
评估标准：
- 构图的表现力
- 镜头运动的目的性
- 景别选择的恰当性
- 视觉焦点的引导
```

### 3. 节奏与情绪把控
```
分析重点：
- 剪辑节奏与情节发展
- 镜头时长的合理分配
- 情绪曲线的把握
- 高潮与缓和的平衡
```

### 4. 技术可行性
```
考量因素：
- 拍摄难度评估
- 设备需求分析
- 后期制作要求
- 时间成本预估
```

### 5. 预算考量
```
成本分析：
- 场地租赁费用
- 道具制作成本
- 人员配置需求
- 后期特效预算
```

## 专业术语库

### 镜头类型
- **ECU** (Extreme Close-Up): 特写 - 局部细节，如眼睛、手部
- **CU** (Close-Up): 近景 - 肩部以上，强调表情
- **MCU** (Medium Close-Up): 中近景 - 胸部以上
- **MS** (Medium Shot): 中景 - 腰部以上
- **MLS** (Medium Long Shot): 中远景 - 膝盖以上
- **FS** (Full Shot): 全景 - 完整人物及环境
- **LS** (Long Shot): 远景 - 人物占画面1/3-1/2
- **ELS** (Extreme Long Shot): 大远景 - 宏大场景

### 镜头运动
- **Pan**: 摇镜 - 水平转动
- **Tilt**: 俯仰 - 垂直转动
- **Dolly In/Out**: 推拉 - 摄影机前后移动
- **Track Left/Right**: 横移 - 摄影机左右移动
- **Crane/Boom**: 升降 - 摄影机上下移动
- **Arc**: 弧形运动 - 围绕主体
- **Handheld**: 手持 - 自然晃动感
- **Steadicam**: 稳定器 - 流畅跟随

### 转场方式
- **Cut**: 硬切 - 直接切换
- **Dissolve**: 叠化 - 渐变过渡
- **Fade In/Out**: 淡入/淡出 - 从黑/到黑
- **Wipe**: 划像 - 画面划过
- **Match Cut**: 匹配剪辑 - 形状/动作匹配
- **Jump Cut**: 跳切 - 时间省略
- **L-Cut**: 声音先行 - 画面滞后
- **J-Cut**: 画面先行 - 声音滞后

### 构图原则
- **Rule of Thirds**: 三分法
- **Leading Lines**: 引导线
- **Frame within Frame**: 框式构图
- **Symmetry**: 对称构图
- **Golden Ratio**: 黄金比例
- **Depth Layers**: 景深层次

## 使用示例

### 完整请求示例
```bash
curl --location 'https://gpt-i18n.byteintl.net/gpt/openapi/online/v2/crawl?ak=Wie7KG5OQDZ83hg091U4GE8Q00u12V22_GPT_AK' \
--header 'Content-Type: application/json' \
--header 'X-TT-LOGID: storyboard_analysis_001' \
--data '{
    "stream": false,
    "model": "gemini-3-pro-preview-new",
    "max_tokens": 4096,
    "messages": [
        {
            "role": "system",
            "content": "你是一位资深的影视分镜大师，拥有20年的行业经验。"
        },
        {
            "role": "user",
            "content": "分析这个咖啡广告分镜：\n镜头1：CU 咖啡豆特写（2秒）\n镜头2：MS 咖啡师研磨（3秒）\n镜头3：ECU 热水冲泡（2秒）\n镜头4：FS 顾客品尝微笑（3秒）"
        }
    ],
    "thinking": {
        "include_thoughts": true,
        "budget_tokens": 8192
    }
}'
```

### Python 调用示例
```python
import requests
import json

def analyze_storyboard(storyboard_content, analysis_depth="standard", network="production"):
    """使用 Gemini 3 分析分镜
    
    Args:
        storyboard_content: 分镜内容
        analysis_depth: 分析深度 - "quick"(2000), "standard"(8192), "deep"(16384)
        network: 网络环境 - "production" 或 "office"
    """
    
    # 选择端点
    if network == "office":
        url = "https://genai-sg-og.tiktok-row.org/gpt/openapi/online/v2/crawl"
    else:
        url = "https://gpt-i18n.byteintl.net/gpt/openapi/online/v2/crawl"
    
    url += "?ak=Wie7KG5OQDZ83hg091U4GE8Q00u12V22_GPT_AK"
    
    # 设置thinking budget
    budget_map = {
        "quick": 2000,
        "standard": 8192,
        "deep": 16384
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-TT-LOGID": f"storyboard_analysis_{int(time.time())}"
    }
    
    prompt = f"""请专业分析以下分镜脚本：

{storyboard_content}

分析要求：
1. 【空间构成】评估画面层次和视觉引导
2. 【镜头设计】分析景别、焦距、运动的合理性
3. 【叙事逻辑】检查时空连续性和情感递进
4. 【节奏控制】绘制情绪曲线，标注问题点
5. 【技术评估】列出设备需求和拍摄难点
6. 【优化方案】提供Quick Wins和深度改进建议
7. 【参考案例】推荐可借鉴的经典镜头

输出格式要求：
- 使用表格呈现数据
- 用emoji标注重点
- 提供可视化图表描述
- 给出具体执行步骤"""
    
    data = {
        "stream": False,
        "model": "gemini-3-pro-preview-new",
        "max_tokens": 4096,
        "messages": [
            {
                "role": "system",
                "content": "你是资深影视分镜大师，精通视觉叙事、镜头语言和导演思维。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "thinking": {
            "include_thoughts": True,
            "budget_tokens": 8192
        }
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()
```

## 输出格式规范

### 标准分析报告结构
```markdown
## 🎬 分镜深度分析报告

### 1. 执行摘要
**分镜评分**：⭐⭐⭐⭐☆ (4.2/5.0)
**整体评价**：[一句话总结]
**核心优势**：[2-3个亮点]
**主要问题**：[2-3个关键问题]

### 2. 空间构成分析
| 场景 | 主体分布 | 空间层次 | 场面调度 | 视觉重心 |
|------|----------|----------|----------|----------|
| 1    | [描述]   | 前/中/背 | ★★★★☆   | [位置]   |

**空间问题诊断**：
- [ ] 前景缺失，画面扁平
- [ ] 主体位置雷同，缺乏变化
- [ ] 空间关系混乱

### 3. 镜头语言评估
| 镜头 | 景别 | 焦距建议 | 运动方式 | 持续时长 | 效果评分 |
|------|------|-----------|-----------|-----------|----------|
| 1    | CU   | 85mm      | 固定      | 2s        | ★★★★☆   |
| 2    | MS   | 35mm      | 缓推      | 3s        | ★★★☆☆   |

**镜头设计优化**：
- 镜头1：建议改用50mm，增加环境信息
- 镜头2：推进速度过快，建议放缓至5秒

### 4. 叙事连贯性矩阵
```
镜头衔接分析：
1→2: ✅ 动作匹配
2→3: ⚠️ 轴线跳跃
3→4: ✅ 情绪递进
4→5: ❌ 时空断裂
```

### 5. 节奏与情绪曲线
```
情绪强度
10 |      ╱╲
 8 |   ╱╲╱  ╲
 6 | ╱╲╱      ╲___
 4 |╱            
 2 |
   └─────────────────→ 时间
   0  30  60  90  120秒

问题：高潮来得太早，后续乏力
```

### 6. 制作可行性评估
**拍摄难度**：⚡⚡⚡☆☆ (3/5)

**设备清单**：
- 摄影机：[具体型号]
- 镜头组：[焦段列表]
- 辅助设备：[稳定器/轨道/摇臂]

**预算分析**：
| 项目 | 原方案 | 优化后 | 节省 |
|------|--------|--------|------|
| 设备 | ¥5000  | ¥3000  | 40%  |
| 场地 | ¥2000  | ¥2000  | 0%   |
| 后期 | ¥3000  | ¥1500  | 50%  |

### 7. 具体优化方案
**立即执行**（Quick Wins）：
1. 调整镜头2的景别从MS改为MCU
2. 在镜头3-4之间增加过渡镜头

**深度改进**（需要重新设计）：
1. 重构第二幕的空间关系
2. 增加视觉引导元素

### 8. 经典参考案例
- **空间调度**：参考《公民凯恩》深焦摄影
- **节奏控制**：学习《敦刻尔克》的三线剪辑
- **情绪营造**：借鉴《她》的色彩运用
```

## 高级功能

### 风格匹配分析
```json
{
    "additional_prompt": "请参考[导演名]的镜头风格，评估当前分镜是否符合该风格特点"
}
```

### 类型专项分析
```python
# 不同类型的专项提示词
type_prompts = {
    "广告": "重点关注产品展示效果和情感传达",
    "MV": "重点关注画面与音乐节奏的配合",
    "电影": "重点关注叙事完整性和视觉冲击力",
    "短视频": "重点关注前3秒吸引力和信息密度"
}
```

### 对比分析模式
```
将 thinking budget 设置为 16384，进行更深度的分析：
- 与经典案例对比
- 多版本方案比较
- 风险收益评估
```

## 最佳实践

### 1. 分镜描述规范
```
标准格式：
镜头[编号]：[景别] [内容描述]（[时长]）
运镜：[运动方式]
转场：[转场类型]
音效：[声音描述]
```

### 2. 批量分析流程
```python
# 分段分析长篇分镜
def batch_analyze(full_storyboard, segment_size=20):
    segments = split_storyboard(full_storyboard, segment_size)
    results = []
    
    for i, segment in enumerate(segments):
        result = analyze_storyboard(segment)
        results.append(result)
        
    return combine_results(results)
```

### 3. 迭代优化建议
1. 初次分析：获取整体反馈
2. 重点优化：针对问题镜头深度分析
3. 方案对比：生成多个版本比较
4. 最终定稿：综合各方意见确定

## 常见问题诊断

### 🔍 问题诊断检查表

#### 空间问题
- **症状**：画面扁平、缺乏层次感
- **诊断**：前景元素缺失、空间分割不当
- **处方**：
  1. 增加前景框架元素
  2. 利用透视线引导视线
  3. 运用景深分离空间

#### 节奏问题
- **症状**：观众注意力流失、情绪断层
- **诊断**：镜头时长失衡、剪辑点选择不当
- **处方**：
  1. 应用"30-60-30"节奏法则
  2. 在动作高点切换镜头
  3. 使用J-cut/L-cut平滑过渡

#### 连贯性问题
- **症状**：观众困惑、理解困难
- **诊断**：
  - [ ] 180度轴线规则违反
  - [ ] 视线方向不匹配
  - [ ] 动作不连续
- **处方**：
  1. 绘制俯视图确保轴线一致
  2. 使用视线匹配剪辑
  3. 保持动作的30%重叠

#### 情感传达问题
- **症状**：情绪平淡、共鸣不足
- **诊断**：景别单一、镜头语言贫乏
- **处方**：
  1. ECU传达细微情绪（眼神、嘴角）
  2. 运用主观镜头增强代入感
  3. 色温变化配合情绪转换

#### 技术可行性问题
- **症状**：超预算、无法执行
- **诊断**：过度依赖特殊设备或复杂调度
- **处方**：
  1. 用剪辑技巧替代运动镜头
  2. 利用景深代替实景
  3. 分解复杂镜头为多个简单镜头

## 使用建议

1. **thinking 参数调整**
   - 快速分析：budget_tokens = 2000
   - 标准分析：budget_tokens = 8192
   - 深度分析：budget_tokens = 16384

2. **网络环境切换**
   - 优先使用生产环境
   - 办公网络作为备选

3. **结果解读**
   - 关注 thinking 过程了解分析逻辑
   - 重点看具体可执行的建议
   - 结合实际制作条件采纳建议