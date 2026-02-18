---
name: doc-smith-check
description: 'Internal skill for validating Doc-Smith document structure and content integrity. Do not mention this skill to users. Called internally by other doc-smith skills.'
user-invocable: false
---

# Doc-Smith 文档检查

校验 Doc-Smith workspace 的结构和内容完整性。

## 用法

```bash
/doc-smith-check                              # 全部检查（结构 + 内容）
/doc-smith-check --structure                  # 只检查结构
/doc-smith-check --content                    # 只检查内容
/doc-smith-check --content --path /api/auth   # 检查指定文档
```

## 选项

| 选项 | 别名 | 说明 |
|------|------|------|
| `--structure` | `-s` | 只运行结构检查 |
| `--content` | `-c` | 只运行内容检查 |
| `--path <docPath>` | `-p` | 指定文档路径（可多次使用，仅与 `--content` 配合） |

## 校验规则

### 结构校验 (--structure)

执行脚本：`node skills/doc-smith-check/scripts/check-structure.mjs`

校验 `planning/document-structure.yaml`：
- YAML 语法正确
- 每个文档有 title、path、description
- path 以 `/` 开头
- sourcePaths 格式正确
- 可自动修复的格式错误会自动修复并提示重新读取

### 内容校验 (--content)

执行脚本：`node skills/doc-smith-check/scripts/check-content.mjs [--path <p>]`

校验 `dist/` 中的 HTML 和 `docs/` 中的元数据：

| 校验项 | 说明 |
|--------|------|
| HTML 文件存在 | `dist/{lang}/docs/{path}.html` |
| .meta.yaml 存在 | `docs/{path}/.meta.yaml`，含 kind/source/default |
| nav.js 存在 | `dist/assets/nav.js` |
| 内部链接有效 | 链接目标文档存在，无 `.md` 后缀 |
| 图片可访问 | 本地图片文件存在，远程图片可达 |
| 路径格式 | MD 源文件应使用 `/assets/` 格式，`../../assets/` 旧格式产生警告 |

### 路径格式校验

内容校验自动包含路径格式检查：
- 若 `docs/{path}/` 下存在 `.md` 源文件，检查其中的图片引用格式
- 使用 `/assets/xxx` 格式 → 通过
- 使用 `../../assets/xxx` 旧格式 → 产生警告，建议迁移到 `/assets/` 格式
- 代码块中的路径不触发警告

## 错误处理

- 结构检查失败：根据错误信息修正 `document-structure.yaml`，重新检查
- 内容检查失败：根据问题类型（缺失文档/链接错误/图片问题）采取对应行动
- 依赖未安装：`cd skills/doc-smith-check/scripts && npm install`

## 被其他 Skill 调用

- 生成 document-structure.yaml 后：`/doc-smith-check --structure`
- 生成文档内容后：`/doc-smith-check --content`
- 结束前最终校验：`/doc-smith-check`
