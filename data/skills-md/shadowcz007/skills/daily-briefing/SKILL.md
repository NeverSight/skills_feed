---
name: daily-briefing
description: 从 mixdao latest 获取数据 → 用 MiniMax-M2.5 做分类整理（agent loop：至多5组、每组至少3条）并生成分组摘要与每条推荐语 → 按 cachedStoryId 提交推荐语并上传简报到 mixdao。需配置 MIXDAO_API_KEY、ANTHROPIC_API_KEY。自然语言触发示例：「执行 daily briefing」「做今日 mixdao 简报」。
---

# Daily Briefing（拉取 + MiniMax 分类 + 简报上传 + 推荐语提交）

## 脚本

| 脚本 | 作用 |
|------|------|
| `scripts/01-fetch.js` | 拉取 mixdao `GET /api/latest`（环境变量 `MIXDAO_API_KEY`）→ 使用接口返回的 `date`，解析并扁平化为 `items` → 写入 `temp/briefing-{date}.json`（内容为 `{ date, items }`）→ 输出 `[FILE PATH] <path>`。 |
| `scripts/02-briefing.js` | 读取步骤 1 的 temp 文件 → 调用 **MiniMax-M2.5** 做分组（agent loop 直至满足约束）→ 生成分组摘要（100 字内）与每条推荐语（140 字内，创业者视角）→ 保存简报 MD，并 **PATCH /api/briefing** 上传简报到 mixdao → 按 **cachedStoryId** 批量 **PATCH /api/latest/recommendation** 提交推荐语。 |

## 工作流程

### 步骤 1：从 latest 获取数据

在 skill 根目录下执行：

```bash
node scripts/01-fetch.js
```

**输出**：`[FILE PATH] <temp 文件完整路径>`，供步骤 2 使用。

### 步骤 2：MiniMax 分类整理 + 提交推荐语

将步骤 1 输出的文件路径传入：

```bash
node scripts/02-briefing.js <filepath>
```

**示例**：

```bash
node scripts/02-briefing.js ./temp/briefing-2026-02-14.json
```

**02-briefing 内部流程**：
1. 读取 JSON（格式 `{ date, items }`，`date` 为 YYYY-MM-DD，`items` 为非空数组；每条 item 需含 `id`（即 cachedStoryId）及 `title`、`translatedTitle`、`text`、`url`，与 01-fetch 输出一致），校验 `date` 与 `items`。
2. **分组 Agent Loop**（MiniMax-M2.5）：对类似话题分组，**至多 5 组**，**每组至少 3 条**；不满足则反馈重试，最多 3 次。
3. **生成摘要与推荐语**：每组一段分组摘要（100 字内）；每条站在**创业者角度**生成推荐语（140 字内），格式：**xxx场景、xxx问题、xxx解决方案、xxx价值**。
4. 将简报写入与 temp 同目录的 `.md` 文件，并调用 mixdao **PATCH /api/briefing**（body: `{ date, title, content }`）上传简报。
5. 按 **cachedStoryId** 批量调用 mixdao `PATCH /api/latest/recommendation`（body: `{ items: [{ cachedStoryId, recommendationText }, ...] }`，Bearer `MIXDAO_API_KEY`）提交推荐语。根据返回的 `results` 统计成功/失败并打 log。

## 环境变量

| 变量 | 说明 |
|------|------|
| **MIXDAO_API_KEY** | 必填。mixdao API 的 Bearer token（拉取 latest 与提交推荐语）。 |
| **ANTHROPIC_BASE_URL** | 可选，默认 `https://api.minimaxi.com/anthropic`。MiniMax 兼容 Anthropic 的 base URL。 |
| **ANTHROPIC_API_KEY** | 必填。MiniMax API Key，用于调用 MiniMax-M2.5。 |

## 注意事项

- **环境变量**：运行前请设置 `MIXDAO_API_KEY` 与 `ANTHROPIC_API_KEY`（见上表）。
- **请求超时**：01-fetch 拉取 API 超时 15 秒；02-briefing 内推荐语为一次批量 PATCH，超时 15 秒。
- **临时文件**：步骤 1 将原始数据写入 `temp/`，步骤 2 仅读取，不删除；示例路径 `./temp/briefing-YYYY-MM-DD.json` 由 01-fetch 生成。
- **推荐语格式**：每条 140 字内，创业者视角：场景、问题、解决方案、价值。
