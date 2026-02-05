---
name: excalidraw-generator
description: Professional Excalidraw diagram generation expert that creates complete, valid .excalidraw files based on user descriptions. Use ONLY when users explicitly mention "Excalidraw" or request to create diagrams specifically with Excalidraw (e.g., "用 Excalidraw 画个流程图", "generate an Excalidraw diagram", "create Excalidraw file"). Do NOT trigger for generic diagram requests without Excalidraw mention. Generates ready-to-open files instead of requiring copy-paste.
---

# Excalidraw Diagram Generator

## Overview

This skill enables you to generate complete, valid `.excalidraw` files that users can directly open at excalidraw.com. You act as a professional diagram generation expert, creating beautiful, well-structured diagrams from user descriptions with automatic layout calculation and saving them as ready-to-use files.

**Supports two visual styles:**
- **专业模式 (Professional Mode)**: Clean, polished diagrams for technical documentation (default)
- **手绘模式 (Hand-drawn Mode)**: Sketch-style diagrams for brainstorming and informal use

## Core Capabilities

You can generate these diagram types:

1. **Flowcharts** - Process flows, decision trees, workflows
2. **Architecture Diagrams** - System architectures, network topologies, component diagrams
3. **UML Diagrams** - Class diagrams, sequence diagrams, use case diagrams
4. **Mind Maps** - Hierarchical concept maps, brainstorming diagrams

## Quick Start

When a user requests a diagram:

1. **Understand the request** - Identify the diagram type and key content
2. **Choose style** - Use **专业模式 (Professional Mode)** by default; switch to hand-drawn mode only if user requests it
3. **Choose a template** - Start from the relevant template in `assets/`
4. **Modify elements** - Adjust text, positions, colors based on requirements
5. **Calculate layout** - Use spacing guidelines from `references/excalidraw-format.md`
6. **Save to file** - Write the complete JSON to a `.excalidraw` file

## Workflow

### Step 1: Identify Diagram Type

Match the user's request to a diagram type:

- **Flowchart**: Process flows, algorithms, decision trees, workflows
- **Architecture**: System designs, microservices, cloud infrastructure, databases
- **UML Class**: Object-oriented design, class hierarchies, relationships
- **Mind Map**: Brainstorming, concept hierarchies, topic exploration

### Step 2: Use Templates as Foundation

Templates are located in `assets/` directory:

- `flowchart-template.json` - Start → Process → Decision flow
- `architecture-template.json` - Frontend → Backend → Database architecture
- `uml-class-template.json` - Class with attributes and methods
- `mindmap-template.json` - Central topic with three branches

**Template usage:**
1. Read the appropriate template file
2. Modify element IDs, text, positions, and colors
3. Add or remove elements as needed
4. Ensure all IDs are unique

### Step 3: Generate Elements

For detailed element specifications, consult `references/excalidraw-format.md`.

**Key element types:**
- `rectangle` - Boxes, containers, processes
- `ellipse` - Start/end nodes, databases, emphasis
- `diamond` - Decisions, conditional branches
- `arrow` / `line` - Connections, flows, relationships
- `text` - Labels, descriptions

**Essential properties all elements need:**
```json
{
  "id": "unique-id",
  "type": "rectangle|ellipse|diamond|arrow|text",
  "x": 100,
  "y": 100,
  "width": 150,
  "height": 80,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "#a5d8ff",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "angle": 0,
  "groupIds": [],
  "frameId": null,
  "roundness": { "type": 3 },
  "boundElements": [],
  "updated": 1705276800000,
  "link": null,
  "locked": false,
  "versionNonce": 123456789,
  "isDeleted": false,
  "seed": 987654321
}
```

### Step 4: Calculate Layout Automatically

**Spacing guidelines:**
- Minimum spacing between elements: 80-100px
- Vertical flow gap (parent → child): 120px
- Horizontal spacing (siblings): 150px
- Arrow padding from element edge: 10-20px

**Standard sizes:**
- Small boxes: 120×60
- Medium boxes: 150×80
- Large boxes: 200×100

**Text height calculation (CRITICAL):**
```
textHeight = fontSize × lineHeight × numberOfLines
           = fontSize × 1.25 × numberOfLines

Example:
- 1 line, fontSize 20: height = 20 × 1.25 × 1 = 25px
- 3 lines, fontSize 14: height = 14 × 1.25 × 3 = 52.5px ≈ 53px
- 12 lines, fontSize 15: height = 15 × 1.25 × 12 = 225px
```

**UML Class Diagram container height calculation:**
```
containerHeight = headerHeight + dividerHeight + attributesHeight + dividerHeight + methodsHeight + padding

Where:
- headerHeight = classNameTextHeight + topPadding (typically 15px + 15px = 30px)
- dividerHeight = 0 (line element, but reserve ~10px visual space after)
- attributesHeight = fontSize × 1.25 × numberOfAttributes + 10px (bottom padding)
- methodsHeight = fontSize × 1.25 × numberOfMethods + 10px (bottom padding)
- topPadding: 15px above class name
- bottomPadding: 10px below each section

Example for a class with 12 attributes and 10 methods (fontSize 15):
- headerHeight: 20 + 15 = 35px
- attributesHeight: 15 × 1.25 × 12 + 10 = 225 + 10 = 235px
- methodsHeight: 15 × 1.25 × 10 + 10 = 187.5 + 10 ≈ 198px
- Total: 35 + 10 + 235 + 10 + 198 = 488px (round to 500px for safety)
```

**Layout strategies:**
- **Flowcharts**: Top-to-bottom, centered alignment
- **Architecture**: Left-to-right for flow, grouped by layer
- **UML Class**: Use calculation formula above; ensure text doesn't overflow container
- **Mind Maps**: Radial from center, balanced branches

### Step 5: Style and Polish

**Choose a diagram style based on context:**

#### 专业模式 (Professional Mode) - 推荐用于技术文档
**适用场景：** 架构图、UML 图、技术文档、正式演示

**样式参数：**
- `roughness: 0` - 完全平滑，无手绘效果
- `fillStyle: "solid"` - 纯色填充，文字更易读
- `strokeWidth: 2` - 标准线宽
- `fontFamily: 2` - 正常字体（非手绘）
- **颜色使用淡色背景** 以提高可读性：
  - Primary: `#e7f5ff` (浅蓝)
  - Success: `#ebfbee` (浅绿)
  - Warning: `#fff9db` (浅黄)
  - Accent: `#f3f0ff` (浅紫)
  - Secondary: `#fff4e6` (浅橙)

**何时使用：** 默认模式，除非用户明确要求手绘风格

#### 手绘模式 (Hand-drawn Mode)
**适用场景：** 创意头脑风暴、快速草图、非正式分享

**样式参数：**
- `roughness: 1` - 手绘风格效果
- `fillStyle: "hachure"` - 斜线纹理填充
- `strokeWidth: 2` - 标准线宽
- `fontFamily: 1` - 手绘字体
- **颜色使用中等饱和度：**
  - Primary: `#a5d8ff` (蓝)
  - Success: `#b2f2bb` (绿)
  - Warning: `#ffec99` (黄)
  - Error: `#ffc9c9` (红)
  - Accent: `#d0bfff` (紫)
  - Secondary: `#ffd8a8` (橙)

**何时使用：** 用户明确要求"手绘风格"、"sketch"、"casual" 时

**通用样式建议：**
- Stroke color: `#1e1e1e` (深灰，比纯黑柔和)
- 箭头标签使用对比色，确保可读性
- 保持组件间距一致（80-100px）

### Step 6: Save to File

**Always save the diagram directly as a `.excalidraw` file** instead of showing JSON in a code block.

1. Use the Write tool to save the complete JSON to a file
2. Name the file descriptively (e.g., `user-login-flow.excalidraw`, `system-architecture.excalidraw`)
3. Save to the current working directory unless user specifies otherwise

**After saving the file, provide:**
1. Confirmation message with the file path
2. Brief description of the diagram structure
3. Instructions: "Open the file at excalidraw.com using 'Open' → 'Open from your computer', or drag and drop the file into the browser"
4. Any customization suggestions

## Common Patterns

### Pattern 1: Sequential Flow

For processes with steps A → B → C:
1. Place elements vertically with 120px gaps
2. Use rectangles for processes, ellipses for start/end
3. Connect with arrows (type: "arrow", endArrowhead: "arrow")
4. Center-align all elements

### Pattern 2: Decision Tree

For conditional branches:
1. Use diamond for decision nodes
2. Branch arrows left/right or up/down
3. Add text labels on arrows ("Yes", "No", "Success", "Fail")
4. Rejoin paths when appropriate

### Pattern 3: Hierarchical Structure

For layered architectures:
1. Group elements by layer (horizontal rows)
2. Use different colors per layer
3. Vertical arrows show dependencies
4. Maintain consistent element sizes within layers

### Pattern 4: Radial Mind Map

For concept exploration:
1. Central node (ellipse) in the middle
2. Branch lines (type: "line") radiate outward
3. Use different colors for each main branch
4. Rectangles for sub-topics

## Tips for Quality Diagrams

1. **Unique IDs**: Generate random 8-16 character IDs for each element
2. **Consistent spacing**: Follow the spacing guidelines strictly
3. **Color harmony**: Use the recommended color palette
4. **Text sizing**: Match text width to container width with padding
5. **Arrow connections**: Position arrow start/end points precisely
6. **Version numbers**: Use random integers for versionNonce and seed

## Handling Complex Requests

For large or complex diagrams:
1. **Start simple**: Create core structure first
2. **Iterate**: Add details progressively
3. **Group logically**: Use visual grouping (colors, spacing)
4. **Limit complexity**: Suggest breaking into multiple diagrams if needed
5. **Maintain readability**: Ensure text doesn't overlap, adequate spacing

## Reference Material

- **Complete format specification**: See `references/excalidraw-format.md`
  - Full element property reference
  - All element types and their specific properties
  - Color palette recommendations
  - Detailed layout guidelines

## Resources

### assets/
Contains starter templates for common diagram types:
- `flowchart-template.json` - Basic flowchart structure
- `architecture-template.json` - System architecture pattern
- `uml-class-template.json` - UML class diagram format
- `mindmap-template.json` - Mind map layout

### references/
- `excalidraw-format.md` - Complete Excalidraw JSON format specification, element types, properties, and examples
