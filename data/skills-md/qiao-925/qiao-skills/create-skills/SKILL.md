---
name: create-skills
description: 按 Agent Skills 官方规范指导编写技能。在用户要创建、设计或修改新 skill，或询问 skill 结构、SKILL.md 格式、agentskills.io 规范时使用。
---

## Instructions（分步说明）

### Step 1：确认目录结构

每个 skill 至少包含 `SKILL.md`，可选 `scripts/`、`references/`、`assets/`。完整格式规范见 [references/specification.md](references/specification.md)（来源：[agentskills.io/specification](https://agentskills.io/specification)）。

```
skill-name/
├── SKILL.md          # Required
├── scripts/          # Optional
├── references/       # Optional
└── assets/           # Optional
```

目录名必须与 frontmatter 中的 `name` 一致（小写、连字符、1–64 字符）。

**规则设计时的命名约定**（创建/修改 skill 时适用）：除必要外，所有文件名与目录名使用小写。

- **默认**：新建或重命名的文件、目录均使用小写。
- **「必要」**：仅当规范/框架**明确要求**某命名时不改为小写（如 `SKILL.md`、`README.md`、`Makefile`）。强制规范 > 本约定。
- **不确定时**：先查该规范文档；未写明则使用小写。

### Step 2：编写 frontmatter

必填两项：

- **name**：与目录名一致，仅 `a-z`、`0-9`、`-`，不以 `-` 开头或结尾，无 `--`
- **description**：做什么 + 何时用，含关键词，1–1024 字符，第三人称

### Step 3：编写正文

YAML 之后为 Markdown 正文。推荐包含：

- **Instructions**（分步说明）
- **Examples**（输入/输出示例，若适用）
- **Edge cases**（常见边界情况，若适用）


### Step 4：自检与验证

- [ ] 目录名 = `name`
- [ ] `description` 含「做什么」「何时用」和关键词
- [ ] 引用文件仅一层深度，用相对路径
- [ ] 若环境支持：`skills-ref validate ./skill-name`

---

## Example（最小可用 skill）

**输入**：用户要一个「处理 PDF」的 skill。

**输出**：创建目录 `pdf-processing/`，其中 `SKILL.md` 至少为：

```yaml
---
name: pdf-processing
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDFs or when the user mentions PDFs, forms, or document extraction.
---

# PDF Processing

## Instructions
1. ...
```

---

## 常见边界情况

- **name 与目录不一致**：必须一致，否则部分客户端无法发现
- **文件名与目录名**：规则设计时适用上述「除必要外小写」约定；目录名与 `name` 一致故自然小写
- **description 过泛**（如 "Helps with PDFs"）：代理难以匹配，应写清「做什么 + 何时用 + 关键词」
- **SKILL.md 超 500 行**：拆到 `references/`，正文只保留要点并链接
- **引用多层文件**：从 SKILL.md 只引用一层（如 `references/SPEC.md`），避免 `references/a/b.md`

---
