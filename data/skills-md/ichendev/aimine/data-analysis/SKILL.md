---
name: data-analysis
description: 数据分析流程，从数据探索到洞察报告的完整工作流
version: 1.1.0
author: AI Mine
tags:
  - data
  - analysis
  - visualization
  - statistics
enabled: true
tools:
  - bash
  - file_read
  - file_write
  - rag_search
---

# 数据分析技能

结构化的数据分析工作流程，从原始数据到可执行洞察。

## 适用场景

- CSV/Excel 数据集分析
- 业务指标分析
- 趋势和模式识别
- 数据质量评估

## 分析流程

### Phase 1: 数据加载与探索
```python
import pandas as pd

# 加载数据
df = pd.read_csv('data.csv')

# 基本信息
print(f"数据形状: {df.shape}")
print(f"列信息:\n{df.dtypes}")
print(f"缺失值:\n{df.isnull().sum()}")
print(f"基本统计:\n{df.describe()}")
```

### Phase 2: 数据清洗
1. 处理缺失值（删除/填充）
2. 处理异常值（识别/修正）
3. 数据类型转换
4. 重复值处理

### Phase 3: 描述性分析
1. 单变量分析（分布、集中趋势）
2. 双变量分析（相关性、对比）
3. 分组聚合统计
4. 时间序列趋势

### Phase 4: 可视化
```python
import matplotlib.pyplot as plt
import seaborn as sns

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 常用图表
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
# ... 绑定到 axes
plt.tight_layout()
plt.savefig('analysis.png', dpi=150)
```

### Phase 5: 洞察提取
1. 识别关键发现
2. 建立因果假设
3. 提出行动建议

## 输出模板

```markdown
# 📊 数据分析报告

## 1. 数据概览

### 数据集信息
| 属性 | 值 |
|------|------|
| 记录数 | X |
| 字段数 | Y |
| 时间范围 | YYYY-MM-DD ~ YYYY-MM-DD |
| 数据质量 | 缺失率 X% |

### 字段说明
| 字段 | 类型 | 描述 | 示例值 |
|------|------|------|--------|
| field1 | int | ... | ... |

## 2. 数据质量

### 缺失值
| 字段 | 缺失数 | 缺失率 | 处理方式 |
|------|--------|--------|----------|
| ... | ... | ...% | 删除/填充均值 |

### 异常值
- [字段]: 发现 X 个异常值，处理方式: [...]

## 3. 统计分析

### 数值字段统计
| 字段 | 均值 | 中位数 | 标准差 | 最小值 | 最大值 |
|------|------|--------|--------|--------|--------|
| ... | ... | ... | ... | ... | ... |

### 分类字段分布
| 字段 | 类别数 | Top 3 类别 |
|------|--------|-----------|
| ... | ... | A(X%), B(Y%), C(Z%) |

### 相关性分析
[热力图或相关系数表]

## 4. 关键发现

### 发现 1: [标题]
- **现象**: [描述观察到的现象]
- **数据支撑**: [具体数字]
- **可能原因**: [假设]

### 发现 2: [标题]
...

## 5. 可视化

[图表]

## 6. 建议与行动

### 短期行动
- [ ] [具体可执行的建议]

### 长期优化
- [ ] [需要进一步分析的方向]

## 附录: 代码
[关键分析代码]
```

## 分析原则

1. **数据先行**: 先看数据，再下结论
2. **质量第一**: 数据清洗是基础
3. **可视说话**: 用图表支撑发现
4. **行动导向**: 分析要指向决策
