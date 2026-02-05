---
name: code-tidy
description: 整理 Java 代码。对 Git 未提交的 Java 类和方法添加/补充 Javadoc 注释，更新日期注释。当用户说"整理代码"、"添加注释"、"更新日期注释"时触发。
argument-hint: [project-dir]
metadata:
  author: lengleng
  version: "1.4.0"
---

# Code Tidy v1.4.0

整理 Git 未提交的 Java 代码，添加/补充 Javadoc 注释并更新日期。

## 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `$0` | 项目目录路径 | `/code-tidy pigx/` |
| 无参数 | 使用当前工作目录 | `/code-tidy` |

## 工作流程

### 1. 获取 Git 未提交的 Java 文件

**重要**：必须先 `cd` 到项目目录，再执行 git 命令（因为项目可能是独立的 git 仓库）。

```bash
cd ${PROJECT_DIR}
git status --porcelain | grep '\.java$' | awk '{print $2}'
```

**如果没有未提交的 Java 文件**：提示用户并退出。

### 2. 获取当前日期

```bash
CURRENT_DATE=$(date +"%Y-%m-%d")
CURRENT_YEAR=$(date +"%Y")
```

### 3. 逐个处理文件，添加/补充注释

对每个未提交的 Java 文件执行以下操作：

#### 3.1 类注释

**检查**：类声明前是否有 Javadoc 注释（`/** ... */`）

**如果缺失**，在类声明前添加：
```java
/**
 * 类功能描述
 *
 * @author lengleng
 * @date ${CURRENT_DATE}
 */
```

**如果已有注释但缺少 @author 或 @date**，补充缺失的标签。

#### 3.2 方法注释

**仅处理**：`public` 和 `protected` 方法

**跳过**：
- getter/setter 方法
- `@Override` 注解的方法
- private 方法
- 已有完整注释的方法

**如果缺失**，在方法声明前添加：
```java
/**
 * 方法功能描述
 *
 * @param paramName 参数说明
 * @return 返回值说明
 */
```

#### 3.3 更新日期注释

| 类型 | 查找模式 | 更新为 |
|------|----------|--------|
| @date | `@date YYYY/MM/DD` 或 `@date YYYY-MM-DD` | `${CURRENT_DATE}` |
| Copyright | `Copyright © YYYY` 或 `Copyright YYYY` | `${CURRENT_YEAR}` |

**注意**：`@since` 版本号保持不变。

### 4. 输出修改摘要

展示每个文件的修改情况：
- 添加了多少个类注释
- 添加了多少个方法注释
- 更新了多少个日期

## 注释规范

### 类注释必需元素

- 类功能描述（一句话概括）
- `@author` 作者名
- `@date` 创建/修改日期

### 方法注释必需元素

- 方法功能描述
- `@param` 每个参数说明（如有）
- `@return` 返回值说明（非 void 方法）
- `@throws` 异常说明（如有）
