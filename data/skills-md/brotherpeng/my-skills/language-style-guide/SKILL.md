---
name: language-style-guide
description: 强制在所有交互、代码注释和文档生成中严格使用中文，并遵循高级技术写作规范。Enforces strict adherence to Chinese language in all interactions, code comments, and documentation with high-quality technical writing standards.
---

# language-style-guide Skill

此 Skill 为 **语言无关 (Language Agnostic)** 的通用规范，适用于所有编程语言（如 JavaScript, Python, Go, Java, Rust, C++ 等）及各类配置文件。无论使用何种技术栈，均需遵循本规范以确保中文技术社区的最佳实践。

## 1. 核心原则 (Core Principles)

*   **强制中文回复**：除非用户明确要求使用其他语言，否则所有对话回复、解释说明必须使用**简体中文**。
*   **专业性与准确性**：保持技术专业度。不要使用机器翻译腔。
*   **混合排版规范**：在中英文混排时，单词前后建议保留空格（例如：使用 `Redis` 缓存），以提升阅读体验。

## 2. 代码注释规范 (Code Commenting Standards)

在编写或修改代码时，注释必须遵循以下规则：

*   **语言**：所有注释文本必须为**简体中文**。
*   **风格**：
    *   **行内注释**：解释代码的“意图”而非“字面意思”。
    *   **函数/类文档**：严格遵循当前语言的标准文档规范（如 JS/TS 的 JSDoc, Python 的 Docstrings, Go 的 GoDoc, Rust 的 Rustdoc 等）。
    *   **TODO/FIXME**：标记必须清晰，描述具体待办事项。

**示例 (通用代码风格)**:

```javascript
/**
 * 处理核心业务数据
 * 验证输入有效性，并在执行失败时进行错误回溯
 * 
 * @param {string} inputId - 唯一标识符
 * @param {object} config - 配置参数对象
 * @returns {boolean} 操作是否成功完成
 */
function processCoreData(inputId, config) {
  // 校验步骤：确保 ID 不为空且格式正确
  if (!isValid(inputId)) {
    return false;
  }

  try {
    // 执行主要逻辑：连接远程服务同步状态
    // 注意：此处需要设置超时时间防止阻塞
    const result = remoteService.sync(inputId, {
      timeout: 5000, 
      mode: config.mode 
    });

    return result.isSuccess;
  } catch (error) {
    // 异常处理：记录堆栈信息以便后续排查
    logError("Data sync failed", error);
    throw error;
  }
}
```

**示例 (Python)**:

```python
def process_user_data(user_id, options=None):
    """
    清洗并转换用户传入的原始数据
    
    Args:
        user_id (str): 用户的唯一标识 ID
        options (dict, optional): 处理选项配置. Defaults to None.
    
    Returns:
        dict: 处理后的标准化用户数据字典
        
    Raises:
        ValueError: 当 user_id 格式不符合预期时抛出
    """
    # 预检：验证 ID 格式
    if not validate_id(user_id):
        raise ValueError("无效的用户 ID 格式")
        
    # TODO: 待优化 - 大数据量时建议改用批量处理
    raw_data = db.fetch(user_id)
    
    return transform(raw_data)
```

## 3. 文档编写规范 (Documentation Standards)

创建或更新 Markdown 文档（如 README.md, API 文档）时：

*   **标题层级**：结构清晰，合理使用 H1, H2, H3。
*   **描述性语言**：使用简洁、有力的中文动词。
*   **术语处理**：
    *   保留行业标准英文术语（如 `Kubernetes`, `React Hook`, `Middleware`），**不要**强行意译（如：不要翻译为“舵手”、“反应钩子”）。
    *   首次出现的生僻缩写，建议在括号内简要说明。

## 4. 交互与回复风格 (Interaction Style)

*   **结构化回答**：对于复杂问题，使用“分析”、“方案”、“实施步骤”等小标题分段。
*   **代码解释**：在提供代码块后，用中文简要解释关键变更点。
*   **拒绝生硬翻译**：
    *   Bad: "现在的上下文是..." (The current context is...) -> Good: "当前的执行环境..." 或 "目前的情况..."
    *   Bad: "跑这个命令" (Run this command) -> Good: "执行以下命令"

## 5. 例外情况 (Exceptions)

*   **日志/错误信息**：引用原始系统日志或报错信息时，保持原文（通常是英文），但在分析时用中文解释。
*   **特定字符串**：代码中作为数据值的英文（如 `'en-US'`, `'Content-Type'`）不可修改。
*   **用户强制要求**：如果用户明确并在 Prompt 中要求 "Answer in English"，则单次回复遵循用户指令，但生成的工件（代码注释）仍建议保持项目一致性（除非项目本身是全英文环境）。
