---
name: json-canvas
description: 优化的JSON Canvas可视化系统，专为学习笔记的知识图谱设计。提供思维导图、概念关系图、学习路径图等可视化功能，帮助构建直观的知识结构。
---

# 学习笔记可视化Canvas技能

## 🎨 设计理念

为学习笔记优化的可视化系统，实现：
- **知识结构化**: 将抽象概念转化为直观图形
- **关系可视化**: 清晰展示知识间的关联
- **路径规划**: 可视化学习进程和路径
- **思维整理**: 支持头脑风暴和概念梳理

## 📊 核心应用

JSON Canvas = 节点系统 + 连接关系 + 布局算法
- **节点类型**: 文本、文件、链接、分组
- **连接系统**: 有向边、无向边、标签边
- **布局模式**: 层次、网状、自由布局
- **交互功能**: 缩放、拖拽、折叠展开

## File Structure

A canvas file contains two top-level arrays:

```json
{
  "nodes": [],
  "edges": []
}
```

- `nodes` (optional): Array of node objects
- `edges` (optional): Array of edge objects connecting nodes

## Nodes

Nodes are objects placed on the canvas. There are four node types:
- `text` - Text content with Markdown
- `file` - Reference to files/attachments
- `link` - External URL
- `group` - Visual container for other nodes

### Z-Index Ordering

Nodes are ordered by z-index in the array:
- First node = bottom layer (displayed below others)
- Last node = top layer (displayed above others)

### Generic Node Attributes

All nodes share these attributes:

| Attribute | Required | Type | Description |
|-----------|----------|------|-------------|
| `id` | Yes | string | Unique identifier for the node |
| `type` | Yes | string | Node type: `text`, `file`, `link`, or `group` |
| `x` | Yes | integer | X position in pixels |
| `y` | Yes | integer | Y position in pixels |
| `width` | Yes | integer | Width in pixels |
| `height` | Yes | integer | Height in pixels |
| `color` | No | canvasColor | Node color (see Color section) |

### Text Nodes

Text nodes contain Markdown content.

```json
{
  "id": "6f0ad84f44ce9c17",
  "type": "text",
  "x": 0,
  "y": 0,
  "width": 400,
  "height": 200,
  "text": "# Hello World\n\nThis is **Markdown** content."
}
```

| Attribute | Required | Type | Description |
|-----------|----------|------|-------------|
| `text` | Yes | string | Plain text with Markdown syntax |

### File Nodes

File nodes reference files or attachments (images, videos, PDFs, notes, etc.).

```json
{
  "id": "a1b2c3d4e5f67890",
  "type": "file",
  "x": 500,
  "y": 0,
  "width": 400,
  "height": 300,
  "file": "Attachments/diagram.png"
}
```

```json
{
  "id": "b2c3d4e5f6789012",
  "type": "file",
  "x": 500,
  "y": 400,
  "width": 400,
  "height": 300,
  "file": "Notes/Project Overview.md",
  "subpath": "#Implementation"
}
```

| Attribute | Required | Type | Description |
|-----------|----------|------|-------------|
| `file` | Yes | string | Path to file within the system |
| `subpath` | No | string | Link to heading or block (starts with `#`) |

### Link Nodes

Link nodes display external URLs.

```json
{
  "id": "c3d4e5f678901234",
  "type": "link",
  "x": 1000,
  "y": 0,
  "width": 400,
  "height": 200,
  "url": "https://obsidian.md"
}
```

| Attribute | Required | Type | Description |
|-----------|----------|------|-------------|
| `url` | Yes | string | External URL |

### Group Nodes

Group nodes are visual containers for organizing other nodes.

```json
{
  "id": "d4e5f6789012345a",
  "type": "group",
  "x": -50,
  "y": -50,
  "width": 1000,
  "height": 600,
  "label": "Project Overview",
  "color": "4"
}
```

```json
{
  "id": "e5f67890123456ab",
  "type": "group",
  "x": 0,
  "y": 700,
  "width": 800,
  "height": 500,
  "label": "Resources",
  "background": "Attachments/background.png",
  "backgroundStyle": "cover"
}
```

| Attribute | Required | Type | Description |
|-----------|----------|------|-------------|
| `label` | No | string | Text label for the group |
| `background` | No | string | Path to background image |
| `backgroundStyle` | No | string | Background rendering style |

#### Background Styles

| Value | Description |
|-------|-------------|
| `cover` | Fills entire width and height of node |
| `ratio` | Maintains aspect ratio of background image |
| `repeat` | Repeats image as pattern in both directions |

## Edges

Edges are lines connecting nodes.

```json
{
  "id": "f67890123456789a",
  "fromNode": "6f0ad84f44ce9c17",
  "toNode": "a1b2c3d4e5f67890"
}
```

```json
{
  "id": "0123456789abcdef",
  "fromNode": "6f0ad84f44ce9c17",
  "fromSide": "right",
  "fromEnd": "none",
  "toNode": "b2c3d4e5f6789012",
  "toSide": "left",
  "toEnd": "arrow",
  "color": "1",
  "label": "leads to"
}
```

| Attribute | Required | Type | Default | Description |
|-----------|----------|------|---------|-------------|
| `id` | Yes | string | - | Unique identifier for the edge |
| `fromNode` | Yes | string | - | Node ID where connection starts |
| `fromSide` | No | string | - | Side where edge starts |
| `fromEnd` | No | string | `none` | Shape at edge start |
| `toNode` | Yes | string | - | Node ID where connection ends |
| `toSide` | No | string | - | Side where edge ends |
| `toEnd` | No | string | `arrow` | Shape at edge end |
| `color` | No | canvasColor | - | Line color |
| `label` | No | string | - | Text label for the edge |

### Side Values

| Value | Description |
|-------|-------------|
| `top` | Top edge of node |
| `right` | Right edge of node |
| `bottom` | Bottom edge of node |
| `left` | Left edge of node |

### End Shapes

| Value | Description |
|-------|-------------|
| `none` | No endpoint shape |
| `arrow` | Arrow endpoint |

## Colors

The `canvasColor` type can be specified in two ways:

### Hex Colors

```json
{
  "color": "#FF0000"
}
```

### Preset Colors

```json
{
  "color": "1"
}
```

| Preset | Color |
|--------|-------|
| `"1"` | Red |
| `"2"` | Orange |
| `"3"` | Yellow |
| `"4"` | Green |
| `"5"` | Cyan |
| `"6"` | Purple |

Note: Specific color values for presets are intentionally undefined, allowing applications to use their own brand colors.

## 🎓 学习笔记Canvas示例

### 🧠 概念思维导图
```json
{
  "nodes": [
    {
      "id": "neural-network-main",
      "type": "text",
      "x": 400,
      "y": 200,
      "width": 320,
      "height": 180,
      "text": "# 🧠 神经网络\n\n**核心概念**\n- 受生物神经系统启发\n- 多层神经元连接\n- 通过训练学习模式",
      "color": "6"
    },
    {
      "id": "basic-concepts",
      "type": "group",
      "x": 50,
      "y": 50,
      "width": 280,
      "height": 400,
      "label": "📖 基础概念",
      "color": "4"
    },
    {
      "id": "neuron",
      "type": "text",
      "x": 80,
      "y": 100,
      "width": 220,
      "height": 120,
      "text": "## 神经元\n\n- 基本计算单元\n- 接收输入信号\n- 产生输出响应\n- **权重**调节连接强度",
      "color": "4"
    },
    {
      "id": "activation",
      "type": "text",
      "x": 80,
      "y": 250,
      "width": 220,
      "height": 120,
      "text": "## 激活函数\n\n- **Sigmoid**: (0,1)\n- **ReLU**: max(0,x)\n- **Tanh**: (-1,1)\n- 引入非线性变换",
      "color": "4"
    },
    {
      "id": "algorithms",
      "type": "group",
      "x": 780,
      "y": 50,
      "width": 280,
      "height": 400,
      "label": "⚙️ 核心算法",
      "color": "3"
    },
    {
      "id": "forward",
      "type": "text",
      "x": 810,
      "y": 100,
      "width": 220,
      "height": 120,
      "text": "## 前向传播\n\n$$y = f(Wx + b)$$\n\n- 输入→隐藏→输出\n- 逐层计算激活值\n- 得到预测结果",
      "color": "3"
    },
    {
      "id": "backward",
      "type": "text",
      "x": 810,
      "y": 250,
      "width": 220,
      "height": 120,
      "text": "## 反向传播\n\n$$\\frac{\\partial L}{\\partial W} = \\delta \\cdot a^T$$\n\n- 计算损失梯度\n- 链式法则求导\n- 更新网络参数",
      "color": "3"
    },
    {
      "id": "applications",
      "type": "group",
      "x": 400,
      "y": 450,
      "width": 320,
      "height": 200,
      "label": "🎯 应用领域",
      "color": "1"
    },
    {
      "id": "cv",
      "type": "text",
      "x": 430,
      "y": 500,
      "width": 130,
      "height": 80,
      "text": "## 计算机视觉\n- 图像识别\n- 目标检测",
      "color": "1"
    },
    {
      "id": "nlp",
      "type": "text",
      "x": 580,
      "y": 500,
      "width": 130,
      "height": 80,
      "text": "## 自然语言\n- 文本分类\n- 机器翻译",
      "color": "1"
    }
  ],
  "edges": [
    {
      "id": "main-to-concepts",
      "fromNode": "neural-network-main",
      "fromSide": "left",
      "toNode": "basic-concepts",
      "toSide": "right",
      "label": "包含",
      "color": "4"
    },
    {
      "id": "main-to-algorithms",
      "fromNode": "neural-network-main",
      "fromSide": "right",
      "toNode": "algorithms",
      "toSide": "left",
      "label": "使用",
      "color": "3"
    },
    {
      "id": "main-to-applications",
      "fromNode": "neural-network-main",
      "fromSide": "bottom",
      "toNode": "applications",
      "toSide": "top",
      "label": "应用于",
      "color": "1"
    },
    {
      "id": "forward-to-backward",
      "fromNode": "forward",
      "fromSide": "bottom",
      "toNode": "backward",
      "toSide": "top",
      "label": "梯度",
      "toEnd": "arrow",
      "color": "2"
    }
  ]
}
```

### 📚 学习路径规划图
```json
{
  "nodes": [
    {
      "id": "learning-path",
      "type": "group",
      "x": 0,
      "y": 0,
      "width": 1200,
      "height": 600,
      "label": "🎯 机器学习学习路径",
      "backgroundStyle": "cover"
    },
    {
      "id": "foundation",
      "type": "group",
      "x": 50,
      "y": 100,
      "width": 300,
      "height": 400,
      "label": "📖 基础阶段",
      "color": "4"
    },
    {
      "id": "math-basics",
      "type": "text",
      "x": 80,
      "y": 150,
      "width": 240,
      "height": 100,
      "text": "## 数学基础\n\n- 线性代数\n- 微积分\n- 概率统计\n- 优化理论",
      "color": "4"
    },
    {
      "id": "programming",
      "type": "text",
      "x": 80,
      "y": 280,
      "width": 240,
      "height": 100,
      "text": "## 编程基础\n\n- Python语法\n- NumPy/Pandas\n- 数据可视化\n- 算法基础",
      "color": "4"
    },
    {
      "id": "ml-concepts",
      "type": "text",
      "x": 80,
      "y": 410,
      "width": 240,
      "height": 80,
      "text": "## ML概念\n\n- 监督/无监督学习\n- 特征工程\n- 模型评估",
      "color": "4"
    },
    {
      "id": "core-algorithms",
      "type": "group",
      "x": 400,
      "y": 100,
      "width": 300,
      "height": 400,
      "label": "⚙️ 核心算法",
      "color": "3"
    },
    {
      "id": "classical-ml",
      "type": "text",
      "x": 430,
      "y": 150,
      "width": 240,
      "height": 100,
      "text": "## 经典算法\n\n- 线性回归\n- 决策树\n- SVM\n- 集成学习",
      "color": "3"
    },
    {
      "id": "neural-networks",
      "type": "text",
      "x": 430,
      "y": 280,
      "width": 240,
      "height": 100,
      "text": "## 神经网络\n\n- 感知机\n- 多层网络\n- 反向传播\n- 激活函数",
      "color": "3"
    },
    {
      "id": "optimization",
      "type": "text",
      "x": 430,
      "y": 410,
      "width": 240,
      "height": 80,
      "text": "## 优化方法\n\n- 梯度下降\n- Adam优化\n- 正则化技术",
      "color": "3"
    },
    {
      "id": "advanced-topics",
      "type": "group",
      "x": 750,
      "y": 100,
      "width": 300,
      "height": 400,
      "label": "🚀 进阶主题",
      "color": "1"
    },
    {
      "id": "deep-learning",
      "type": "text",
      "x": 780,
      "y": 150,
      "width": 240,
      "height": 100,
      "text": "## 深度学习\n\n- CNN卷积网络\n- RNN循环网络\n- Transformer\n- 注意力机制",
      "color": "1"
    },
    {
      "id": "specialized",
      "type": "text",
      "x": 780,
      "y": 280,
      "width": 240,
      "height": 100,
      "text": "## 专业领域\n\n- 计算机视觉\n- 自然语言处理\n- 强化学习\n- 推荐系统",
      "color": "1"
    },
    {
      "id": "practical",
      "type": "text",
      "x": 780,
      "y": 410,
      "width": 240,
      "height": 80,
      "text": "## 实践应用\n\n- 项目实战\n- 模型部署\n- 性能优化",
      "color": "1"
    }
  ],
  "edges": [
    {
      "id": "foundation-to-core",
      "fromNode": "foundation",
      "fromSide": "right",
      "toNode": "core-algorithms",
      "toSide": "left",
      "label": "掌握基础后",
      "toEnd": "arrow",
      "color": "6"
    },
    {
      "id": "core-to-advanced",
      "fromNode": "core-algorithms",
      "fromSide": "right",
      "toNode": "advanced-topics",
      "toSide": "left",
      "label": "深入理解",
      "toEnd": "arrow",
      "color": "2"
    },
    {
      "id": "math-to-programming",
      "fromNode": "math-basics",
      "fromSide": "bottom",
      "toNode": "programming",
      "toSide": "top",
      "label": "同步学习",
      "color": "5"
    },
    {
      "id": "programming-to-ml",
      "fromNode": "programming",
      "fromSide": "bottom",
      "toNode": "ml-concepts",
      "toSide": "top",
      "label": "实践结合",
      "color": "5"
    }
  ]
}
```

### 🔍 知识关联图谱
```json
{
  "nodes": [
    {
      "id": "central-concept",
      "type": "text",
      "x": 500,
      "y": 300,
      "width": 350,
      "height": 200,
      "text": "# 🎯 深度学习\n\n**核心研究领域**\n- 基于神经网络的多层学习\n- 自动特征提取\n- 端到端训练\n\n**关键突破**: ImageNet 2012",
      "color": "6"
    },
    {
      "id": "related-notes",
      "type": "group",
      "x": 100,
      "y": 50,
      "width": 250,
      "height": 180,
      "label": "📝 相关笔记",
      "color": "5"
    },
    {
      "id": "nn-basics",
      "type": "file",
      "x": 120,
      "y": 80,
      "width": 210,
      "height": 60,
      "file": "神经网络基础.md",
      "subpath": "#核心概念"
    },
    {
      "id": "backprop",
      "type": "file",
      "x": 120,
      "y": 160,
      "width": 210,
      "height": 60,
      "file": "反向传播算法.md"
    },
    {
      "id": "resources",
      "type": "group",
      "x": 950,
      "y": 50,
      "width": 250,
      "height": 180,
      "label": "📚 学习资源",
      "color": "3"
    },
    {
      "id": "course-link",
      "type": "link",
      "x": 970,
      "y": 80,
      "width": 210,
      "height": 60,
      "url": "https://cs231n.github.io/",
      "text": "CS231n课程"
    },
    {
      "id": "book-link",
      "type": "link",
      "x": 970,
      "y": 160,
      "width": 210,
      "height": 60,
      "url": "https://www.deeplearningbook.org/",
      "text": "深度学习教材"
    },
    {
      "id": "applications",
      "type": "group",
      "x": 100,
      "y": 450,
      "width": 800,
      "height": 200,
      "label": "🎯 应用领域",
      "color": "1"
    },
    {
      "id": "cnn",
      "type": "text",
      "x": 150,
      "y": 490,
      "width": 180,
      "height": 100,
      "text": "## 🖼️ CNN\n\n- 图像分类\n- 目标检测\n- 语义分割",
      "color": "1"
    },
    {
      "id": "rnn",
      "type": "text",
      "x": 360,
      "y": 490",
      "width": 180,
      "height": 100,
      "text": "## 📝 RNN\n\n- 序列建模\n- 语言处理\n- 时间序列",
      "color": "1"
    },
    {
      "id": "gan",
      "type": "text",
      "x": 570,
      "y": 490,
      "width": 180,
      "height": 100,
      "text": "## 🎨 GAN\n\n- 图像生成\n- 风格迁移\n- 数据增强",
      "color": "1"
    },
    {
      "id": "transformer",
      "type": "text",
      "x": 780,
      "y": 490,
      "width": 180,
      "height": 100,
      "text": "## ⚡ Transformer\n\n- 注意力机制\n- BERT/GPT\n- 大语言模型",
      "color": "1"
    },
    {
      "id": "visual-diagram",
      "type": "file",
      "x": 950,
      "y": 300,
      "width": 250,
      "height": 200,
      "file": "assets/deep-learning-architecture.png",
      "subpath": ""
    }
  ],
  "edges": [
    {
      "id": "central-to-notes",
      "fromNode": "central-concept",
      "fromSide": "left",
      "toNode": "related-notes",
      "toSide": "right",
      "label": "理论基础",
      "color": "5"
    },
    {
      "id": "central-to-resources",
      "fromNode": "central-concept",
      "fromSide": "right",
      "toNode": "resources",
      "toSide": "left",
      "label": "学习材料",
      "color": "3"
    },
    {
      "id": "central-to-applications",
      "fromNode": "central-concept",
      "fromSide": "bottom",
      "toNode": "applications",
      "toSide": "top",
      "label": "实际应用",
      "color": "1"
    },
    {
      "id": "nn-to-central",
      "fromNode": "nn-basics",
      "fromSide": "right",
      "toNode": "central-concept",
      "toSide": "left",
      "label": "前置知识",
      "toEnd": "arrow",
      "color": "4"
    },
    {
      "id": "central-to-visual",
      "fromNode": "central-concept",
      "fromSide": "right",
      "toNode": "visual-diagram",
      "toSide": "left",
      "label": "架构图",
      "color": "2"
    },
    {
      "id": "app-connections",
      "fromNode": "cnn",
      "fromSide": "right",
      "toNode": "rnn",
      "toSide": "left",
      "label": "并行发展",
      "color": "6"
    },
    {
      "id": "rnn-to-transformer",
      "fromNode": "rnn",
      "fromSide": "right",
      "toNode": "transformer",
      "toSide": "left",
      "label": "演进关系",
      "toEnd": "arrow",
      "color": "2"
    }
  ]
}
```

### Flowchart

```json
{
  "nodes": [
    {
      "id": "a0b1c2d3e4f5a6b7",
      "type": "text",
      "x": 200,
      "y": 0,
      "width": 150,
      "height": 60,
      "text": "**Start**",
      "color": "4"
    },
    {
      "id": "b1c2d3e4f5a6b7c8",
      "type": "text",
      "x": 200,
      "y": 100,
      "width": 150,
      "height": 60,
      "text": "Step 1:\nGather data"
    },
    {
      "id": "c2d3e4f5a6b7c8d9",
      "type": "text",
      "x": 200,
      "y": 200,
      "width": 150,
      "height": 80,
      "text": "**Decision**\n\nIs data valid?",
      "color": "3"
    },
    {
      "id": "d3e4f5a6b7c8d9e0",
      "type": "text",
      "x": 400,
      "y": 200,
      "width": 150,
      "height": 60,
      "text": "Process data"
    },
    {
      "id": "e4f5a6b7c8d9e0f1",
      "type": "text",
      "x": 0,
      "y": 200,
      "width": 150,
      "height": 60,
      "text": "Request new data",
      "color": "1"
    },
    {
      "id": "f5a6b7c8d9e0f1a2",
      "type": "text",
      "x": 400,
      "y": 320,
      "width": 150,
      "height": 60,
      "text": "**End**",
      "color": "4"
    }
  ],
  "edges": [
    {
      "id": "a6b7c8d9e0f1a2b3",
      "fromNode": "a0b1c2d3e4f5a6b7",
      "fromSide": "bottom",
      "toNode": "b1c2d3e4f5a6b7c8",
      "toSide": "top"
    },
    {
      "id": "b7c8d9e0f1a2b3c4",
      "fromNode": "b1c2d3e4f5a6b7c8",
      "fromSide": "bottom",
      "toNode": "c2d3e4f5a6b7c8d9",
      "toSide": "top"
    },
    {
      "id": "c8d9e0f1a2b3c4d5",
      "fromNode": "c2d3e4f5a6b7c8d9",
      "fromSide": "right",
      "toNode": "d3e4f5a6b7c8d9e0",
      "toSide": "left",
      "label": "Yes",
      "color": "4"
    },
    {
      "id": "d9e0f1a2b3c4d5e6",
      "fromNode": "c2d3e4f5a6b7c8d9",
      "fromSide": "left",
      "toNode": "e4f5a6b7c8d9e0f1",
      "toSide": "right",
      "label": "No",
      "color": "1"
    },
    {
      "id": "e0f1a2b3c4d5e6f7",
      "fromNode": "e4f5a6b7c8d9e0f1",
      "fromSide": "top",
      "fromEnd": "none",
      "toNode": "b1c2d3e4f5a6b7c8",
      "toSide": "left",
      "toEnd": "arrow"
    },
    {
      "id": "f1a2b3c4d5e6f7a8",
      "fromNode": "d3e4f5a6b7c8d9e0",
      "fromSide": "bottom",
      "toNode": "f5a6b7c8d9e0f1a2",
      "toSide": "top"
    }
  ]
}
```

## ID Generation

Node and edge IDs must be unique strings. Obsidian generates 16-character hexadecimal IDs:

```json
"id": "6f0ad84f44ce9c17"
"id": "a3b2c1d0e9f8g7h6"
"id": "1234567890abcdef"
```

This format is a 16-character lowercase hex string (64-bit random value).

## 🎨 学习笔记Canvas最佳实践

### 📐 布局设计原则

#### 层次化布局
```json
// 推荐的知识层次布局
{
  "核心概念": { "x": 400, "y": 200, "层级": 0 },
  "基础理论": { "x": 100, "y": 100, "层级": 1 },
  "应用实践": { "x": 700, "y": 100, "层级": 1 },
  "相关资源": { "x": 100, "y": 400, "层级": 2 }
}
```

#### 节点尺寸规范
| 节点类型 | 建议宽度 | 建议高度 | 用途 |
|---------|----------|----------|------|
| 核心概念 | 350-450 | 180-220 | 中心主题，详细说明 |
| 主要分支 | 280-350 | 120-160 | 重要概念，中等内容 |
| 次要节点 | 200-280 | 80-120 | 补充信息，简洁内容 |
| 文件引用 | 250-350 | 100-150 | 笔记链接，预览 |
| 外部链接 | 220-300 | 80-120 | 网页资源，简短描述 |
| 分组容器 | 400-800 | 300-600 | 主题分组，包含多个节点 |

#### 间距和对齐
```json
// 标准间距配置
{
  "节点间距": "60-100px",
  "分组内边距": "30-50px", 
  "层次间距": "150-200px",
  "网格对齐": "20px倍数"
}
```

### 🎯 学习笔记类型模板

#### 🧠 概念关系图
```json
{
  "布局": "中心辐射式",
  "核心": "主要概念",
  "分支": "相关概念、属性、应用",
  "连接": "包含关系、影响关系、对比关系"
}
```

#### 🛤️ 学习路径图
```json
{
  "布局": "线性流程式", 
  "阶段": "基础→进阶→高级→实践",
  "连接": "前置关系、依赖关系",
  "标记": "完成状态、掌握程度"
}
```

#### 🌳 知识体系图
```json
{
  "布局": "树状层次式",
  "根节点": "学科领域",
  "分支": "子领域、具体方向",
  "叶子": "具体概念、技术点"
}
```

#### 🔄 思维导图
```json
{
  "布局": "自由发散式",
  "中心": "主题或问题",
  "分支": "想法、关键词、疑问",
  "连接": "关联思路、启发关系"
}
```

### 🎨 视觉设计指南

#### 颜色编码系统
```json
{
  "颜色方案": {
    "核心概念": "6 (紫色)",
    "理论基础": "4 (绿色)", 
    "实践应用": "1 (红色)",
    "资源链接": "3 (黄色)",
    "疑问问题": "2 (橙色)",
    "已完成": "4 (绿色)",
    "进行中": "3 (黄色)",
    "待开始": "1 (红色)"
  }
}
```

#### 连接线样式
```json
{
  "连接类型": {
    "包含关系": { "样式": "实线", "箭头": "无", "颜色": "4" },
    "依赖关系": { "样式": "实线", "箭头": "有", "颜色": "6" },
    "影响关系": { "样式": "虚线", "箭头": "有", "颜色": "2" },
    "对比关系": { "样式": "点线", "箭头": "无", "颜色": "3" },
    "时序关系": { "样式": "实线", "箭头": "双向", "颜色": "1" }
  }
}
```

### 📝 内容组织技巧

#### 文本内容结构
```markdown
# 节点标题
## 关键要点
- 要点1：简短描述
- 要点2：核心概念

## 重要公式
$$数学表达式$$

## 代码示例
`关键函数`

## 状态标记
✅ 已掌握  🔄 学习中  ❓ 有疑问
```

#### 分组命名规范
```json
{
  "分组类型": {
    "阶段分组": "📖 基础阶段 / ⚙️ 核心算法 / 🚀 进阶主题",
    "主题分组": "🧠 概念理论 / 💻 实践应用 / 📚 学习资源", 
    "状态分组": "✅ 已完成 / 🔄 进行中 / 📋 待开始",
    "类型分组": "🔧 工具方法 / 📊 数据分析 / 🎯 应用场景"
  }
}
```

### 🔄 维护和更新

#### 定期维护任务
```json
{
  "每周检查": [
    "更新学习进度状态",
    "添加新发现的概念关联", 
    "修正过时的信息链接"
  ],
  "每月整理": [
    "重新组织混乱的布局",
    "补充缺失的知识节点",
    "优化视觉设计效果"
  ]
}
```

#### 版本管理建议
```json
{
  "版本控制": {
    "重要节点": "创建备份前修改",
    "结构调整": "记录变更原因",
    "内容更新": "标注修改时间和内容"
  }
}
```

## Validation Rules

1. All `id` values must be unique across nodes and edges
2. `fromNode` and `toNode` must reference existing node IDs
3. Required fields must be present for each node type
4. `type` must be one of: `text`, `file`, `link`, `group`
5. `backgroundStyle` must be one of: `cover`, `ratio`, `repeat`
6. `fromSide`, `toSide` must be one of: `top`, `right`, `bottom`, `left`
7. `fromEnd`, `toEnd` must be one of: `none`, `arrow`
8. Color presets must be `"1"` through `"6"` or valid hex color

## References

- [JSON Canvas Spec 1.0](https://jsoncanvas.org/spec/1.0/)
- [JSON Canvas GitHub](https://github.com/obsidianmd/jsoncanvas)
