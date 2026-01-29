---
name: code-quality-report
description: 生成代码质量报告。当用户请求为项目源代码生成质量报告时，使用此功能。输出名为 code-quality-report.html 的单页 HTML 文件作为质量报告，该报告集成了 Node.js 脚本和 HTML 模板。
license: Complete terms in LICENSE.txt
---

# 生成代码质量报告

## 质量判断和优化标准

- 依赖`\reference\code-quality-standard.md`作为质量判断和优化标准

## 生成步骤

1. **确定路径和输出目录**
   - 确定源码文件夹路径（通常为`src/`）
   - 确定报告输出文件夹：默认为项目根目录下的`.cqm/code-quality-report/``
   - 如果输出文件夹不存在，则创建该目录

2. **初始化文件结构数据**
   - 执行脚本 node 脚本`generate-file-structure.js`，第一个参数是`源码文件夹路径`，第二个参数是`${报告输出文件夹}/code-quality-report.json`
   - 脚本会在输出文件夹下生成 `code-quality-report.json` 文件
   - 该 JSON 文件包含源码目录结构，每个代码文件的`code_quality`字段初始值为`0`

3. **评估代码质量**
   - 读取`${报告输出文件夹}/code-quality-report.json`获取所有代码文件列表
   - 对于 JSON 中的每个代码文件：
     - 读取文件内容
     - 根据判断标准，运用 AI 能力评估其质量
     - 每个代码文件的质量指标都是独立的，可使用多个子 Agent 并行处理
     - 将评估结果（0-100 的分数）更新到该文件对应的 `code_quality` 字段
     - 将更新后的数据写回 `code-quality-report.json`

4. **生成 HTML 报告**
   - 读取模板文件：`code-quality-report-template.html`
   - 读取最终的`code-quality-report.json`数据
   - 在模板文件中找到`rawData`变量（通常在 JavaScript 代码中）
   - 将`code-quality-report.json`的内容直接赋值给`rawData`变量
   - 将更新后的模板内容保存为`${报告输出文件夹}/code-quality-report.html`

5. **收尾**
   - 最终报告文件位于`${报告输出文件夹}/code-quality-report.html`
   - 如果模板文件`code-quality-report-template.html`中有更改则还原

6. **优化**
   - 最后如果存在得分低于 90 分的文件，则询问是否进行优化
