---
name: pw-danger-gemini-web
description: |
  通过逆向工程的 Gemini Web API 进行文本和图像生成。

  核心能力:
  - 文本生成: 使用 Gemini 模型生成文本响应
  - 图像生成: 从文本提示生成图像并保存到本地
  - 视觉输入: 支持参考图像进行图生图或图生文
  - 多轮对话: 通过 sessionId 保持上下文连续性

  使用时机:
  - 需要生成高质量 AI 图像时 (封面图、配图、插画等)
  - 需要 Gemini 模型进行文本生成时
  - 需要基于参考图像生成变体或描述时
  - 作为其他技能 (pw-cover-image、pw-redbook-image) 的图像生成后端

  不适用场景:
  - 需要官方 API 支持和稳定性保证的生产环境
  - 对 API 变更敏感的关键业务流程
  - 需要批量高频调用的场景 (可能触发限流)

  重要提醒:
  - 首次使用需要用户同意免责声明
  - 需要 Google 账号认证 (自动打开浏览器登录)
  - 在中国大陆需要配置代理访问
  - 这是非官方 API, 可能随时失效
---

# Gemini Web 客户端

支持功能:
- 文本生成
- 图像生成（下载 + 保存）
- 参考图像用于视觉输入（附加本地图像）
- 通过持久化 `--sessionId` 进行多轮对话

## 脚本目录

**重要**: 所有脚本位于此技能的 `scripts/` 子目录中。

**Agent 执行说明**:
1. 确定此 SKILL.md 文件的目录路径为 `SKILL_DIR`
2. 脚本路径 = `${SKILL_DIR}/scripts/<script-name>.ts`
3. 将本文档中的所有 `${SKILL_DIR}` 替换为实际路径

**脚本参考**:
| 脚本 | 用途 |
|------|------|
| `scripts/main.ts` | 文本/图像生成的 CLI 入口点 |
| `scripts/gemini-webapi/*` | `gemini_webapi` 的 TypeScript 移植版（GeminiClient、类型、工具） |

## ⚠️ 免责声明（必需）

**使用此技能前**，必须执行同意检查。

### 同意检查流程

**步骤 1**: 检查同意文件

```bash
# macOS
cat ~/Library/Application\ Support/pw-skills/gemini-web/consent.json 2>/dev/null

# Linux
cat ~/.local/share/pw-skills/gemini-web/consent.json 2>/dev/null

# Windows (PowerShell)
Get-Content "$env:APPDATA\pw-skills\gemini-web\consent.json" 2>$null
```

**步骤 2**: 如果同意文件存在且 `accepted: true` 并匹配 `disclaimerVersion: "1.0"`:

打印警告并继续:
```
⚠️  警告: 使用逆向工程的 Gemini Web API（非官方）。接受时间: <acceptedAt 日期>
```

**步骤 3**: 如果同意文件不存在或 `disclaimerVersion` 不匹配:

显示免责声明并询问用户:

```
⚠️  免责声明

此工具使用逆向工程的 Gemini Web API，而非官方 Google API。

风险:
- 如果 Google 更改其 API，可能会在没有通知的情况下失效
- 没有官方支持或保证
- 使用风险自负

您是否接受这些条款并希望继续？
```

使用 `AskUserQuestion` 工具，选项为:
- **是，我接受** - 继续并保存同意
- **否，我拒绝** - 立即退出

**步骤 4**: 接受后，创建同意文件:

```bash
# macOS
mkdir -p ~/Library/Application\ Support/pw-skills/gemini-web
cat > ~/Library/Application\ Support/pw-skills/gemini-web/consent.json << 'EOF'
{
  "version": 1,
  "accepted": true,
  "acceptedAt": "<ISO 时间戳>",
  "disclaimerVersion": "1.0"
}
EOF

# Linux
mkdir -p ~/.local/share/pw-skills/gemini-web
cat > ~/.local/share/pw-skills/gemini-web/consent.json << 'EOF'
{
  "version": 1,
  "accepted": true,
  "acceptedAt": "<ISO 时间戳>",
  "disclaimerVersion": "1.0"
}
EOF
```

**步骤 5**: 拒绝后，输出消息并停止:
```
用户拒绝了免责声明。退出。
```

---

## 快速开始

```bash
npx -y bun ${SKILL_DIR}/scripts/main.ts "你好，Gemini"
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "解释量子计算"
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "一只可爱的猫" --image cat.png
npx -y bun ${SKILL_DIR}/scripts/main.ts --promptfiles system.md content.md --image out.png

# 多轮对话（agent 生成唯一的 sessionId）
npx -y bun ${SKILL_DIR}/scripts/main.ts "记住这个: 42" --sessionId my-unique-id-123
npx -y bun ${SKILL_DIR}/scripts/main.ts "什么数字?" --sessionId my-unique-id-123
```

## 命令

### 文本生成

```bash
# 简单提示（位置参数）
npx -y bun ${SKILL_DIR}/scripts/main.ts "你的提示内容"

# 显式提示标志
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "你的提示内容"
npx -y bun ${SKILL_DIR}/scripts/main.ts -p "你的提示内容"

# 选择模型
npx -y bun ${SKILL_DIR}/scripts/main.ts -p "你好" -m gemini-2.5-pro

# 从标准输入管道
echo "总结这个" | npx -y bun ${SKILL_DIR}/scripts/main.ts
```

### 图像生成

```bash
# 使用默认路径生成图像（./generated.png）
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "山上的日落" --image

# 使用自定义路径生成图像
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "一个可爱的机器人" --image robot.png

# 简写形式
npx -y bun ${SKILL_DIR}/scripts/main.ts "一条龙" --image=dragon.png
```

### 视觉输入（参考图像）

```bash
# 文本 + 图像 -> 文本
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "描述这张图片" --reference a.png

# 文本 + 图像 -> 图像
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "生成一个变体" --reference a.png --image out.png
```

### 输出格式

```bash
# 纯文本（默认）
npx -y bun ${SKILL_DIR}/scripts/main.ts "你好"

# JSON 输出
npx -y bun ${SKILL_DIR}/scripts/main.ts "你好" --json
```

## 参数说明

### 核心参数

**--prompt <text>** (别名: -p)
- 说明: 要发送给 Gemini 的提示文本
- 类型: 字符串
- 必需: 是 (除非使用 --promptfiles 或标准输入)
- 示例: `--prompt "生成一只可爱的猫咪"`
- 注意: 如果不使用标志，可以直接作为位置参数传递

**--promptfiles <files...>**
- 说明: 从一个或多个文件读取提示内容，按顺序连接
- 类型: 文件路径数组
- 必需: 否
- 示例: `--promptfiles system.md content.md`
- 使用场景: 提示内容较长或需要组合多个文件时
- 注意: 文件内容会按顺序拼接，中间用换行分隔

**--model <id>** (别名: -m)
- 说明: 选择使用的 Gemini 模型
- 类型: 枚举值
- 可选值:
  - `gemini-3-pro` (默认): 最新最强模型，推荐使用
  - `gemini-2.5-pro`: 上一代 pro 版本，稳定性好
  - `gemini-2.5-flash`: 快速轻量，适合简单任务
- 必需: 否
- 示例: `--model gemini-2.5-flash`
- 选择建议:
  - 图像生成: 使用 gemini-3-pro 获得最佳质量
  - 简单文本: 使用 gemini-2.5-flash 提高速度
  - 复杂推理: 使用 gemini-3-pro

### 图像相关参数

**--image [path]**
- 说明: 生成图像并保存到指定路径
- 类型: 可选字符串
- 必需: 否
- 默认值: `generated.png` (如果只写 --image 不带路径)
- 示例:
  - `--image` (保存为 generated.png)
  - `--image cat.png` (保存为 cat.png)
  - `--image=/path/to/output.png` (使用等号语法)
- 注意:
  - 路径可以是相对路径或绝对路径
  - 目录必须存在，否则会报错
  - 支持 PNG 格式

**--reference <files...>** (别名: --ref)
- 说明: 提供参考图像用于视觉输入
- 类型: 文件路径数组
- 必需: 否
- 示例:
  - `--reference photo.jpg` (单张图片)
  - `--reference img1.png img2.png` (多张图片)
- 使用场景:
  - 图生文: 描述图片内容
  - 图生图: 基于参考图生成变体
  - 图文结合: 结合图片和文字提示
- 注意: 支持常见图片格式 (PNG, JPG, JPEG, WebP)

### 会话管理参数

**--sessionId <id>**
- 说明: 多轮对话的会话标识符
- 类型: 字符串
- 必需: 否
- 示例: `--sessionId task-abc123`
- 使用场景:
  - 需要保持上下文的连续对话
  - 批量处理同一主题的多个任务
  - 需要 Gemini 记住之前的交互
- 最佳实践:
  - Agent 应生成唯一的 session ID (如 UUID 或基于任务的 hash)
  - 同一批次任务使用相同 session ID
  - 不同主题使用不同 session ID
- 注意: 会话数据存储在本地，不会过期

**--list-sessions**
- 说明: 列出所有已保存的会话
- 类型: 布尔标志
- 必需: 否
- 输出: 最多 100 个会话，按更新时间倒序排列
- 使用场景: 查看历史会话，决定是否复用

### 输出格式参数

**--json**
- 说明: 以 JSON 格式输出结果
- 类型: 布尔标志
- 必需: 否
- 输出格式:
  ```json
  {
    "text": "生成的文本内容",
    "imagePath": "/path/to/image.png",
    "sessionId": "task-abc123"
  }
  ```
- 使用场景: 需要程序化解析输出时
- 注意: 默认输出为纯文本

### 认证相关参数

**--login**
- 说明: 仅执行登录流程刷新 cookies，然后退出
- 类型: 布尔标志
- 必需: 否
- 使用场景:
  - Cookie 过期需要重新登录
  - 切换 Google 账号
  - 预先完成认证避免后续中断
- 注意: 会打开浏览器窗口，需要手动完成登录

**--cookie-path <path>**
- 说明: 自定义 cookie 文件存储路径
- 类型: 文件路径
- 必需: 否
- 默认值: 系统数据目录下的 cookies.json
- 使用场景: 多账号管理或自定义存储位置

**--profile-dir <path>**
- 说明: 指定 Chrome 配置文件目录
- 类型: 目录路径
- 必需: 否
- 使用场景: 使用特定 Chrome 配置文件

### 帮助参数

**--help** (别名: -h)
- 说明: 显示帮助信息
- 类型: 布尔标志

## 模型

- `gemini-3-pro` - 默认，最新模型
- `gemini-2.5-pro` - 上一代 pro 版本
- `gemini-2.5-flash` - 快速、轻量级

## 认证

首次运行会打开浏览器进行 Google 认证。Cookies 会被缓存以供后续运行使用。

**支持的浏览器**（按顺序自动检测）:
- Google Chrome
- Google Chrome Canary / Beta
- Chromium
- Microsoft Edge

如需要，可使用 `GEMINI_WEB_CHROME_PATH` 环境变量覆盖。

```bash
# 强制刷新 cookie
npx -y bun ${SKILL_DIR}/scripts/main.ts --login
```

**登录说明**:
- 浏览器打开后会一直等待，直到你完成登录
- 没有超时限制，你可以慢慢处理多因素认证等步骤
- 登录成功后，浏览器会在 3 秒后自动关闭

## 环境变量

| 变量 | 说明 |
|------|------|
| `GEMINI_WEB_DATA_DIR` | 数据目录 |
| `GEMINI_WEB_COOKIE_PATH` | Cookie 文件路径 |
| `GEMINI_WEB_CHROME_PROFILE_DIR` | Chrome 配置文件目录 |
| `GEMINI_WEB_CHROME_PATH` | Chrome 可执行文件路径 |

## 代理配置

如果需要代理访问 Google 服务（例如在中国），请在运行前设置 `HTTP_PROXY` 和 `HTTPS_PROXY` 环境变量:

```bash
# 使用本地代理的示例
HTTP_PROXY=http://127.0.0.1:7890 HTTPS_PROXY=http://127.0.0.1:7890 npx -y bun ${SKILL_DIR}/scripts/main.ts "你好"

# 使用代理生成图像
HTTP_PROXY=http://127.0.0.1:7890 HTTPS_PROXY=http://127.0.0.1:7890 npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "一只猫" --image cat.png

# 使用代理刷新 cookie
HTTP_PROXY=http://127.0.0.1:7890 HTTPS_PROXY=http://127.0.0.1:7890 npx -y bun ${SKILL_DIR}/scripts/main.ts --login
```

**注意**: 环境变量必须与命令内联设置。Shell 配置文件设置（如 `.bashrc`）可能不会被子进程继承。

## 示例

### 生成文本响应
```bash
npx -y bun ${SKILL_DIR}/scripts/main.ts "法国的首都是什么?"
```

### 生成图像
```bash
npx -y bun ${SKILL_DIR}/scripts/main.ts "一张金毛猎犬幼犬的逼真照片" --image puppy.png
```

### 获取 JSON 输出用于解析
```bash
npx -y bun ${SKILL_DIR}/scripts/main.ts "你好" --json | jq '.text'
```

### 从提示文件生成图像
```bash
# 将 system.md + content.md 连接作为提示
npx -y bun ${SKILL_DIR}/scripts/main.ts --promptfiles system.md content.md --image output.png
```

### 多轮对话
```bash
# 使用唯一 ID 开始会话（agent 生成此 ID）
npx -y bun ${SKILL_DIR}/scripts/main.ts "你是一个有帮助的数学导师。" --sessionId task-abc123

# 继续对话（记住上下文）
npx -y bun ${SKILL_DIR}/scripts/main.ts "2+2 等于多少?" --sessionId task-abc123
npx -y bun ${SKILL_DIR}/scripts/main.ts "现在乘以 10" --sessionId task-abc123

# 列出最近的会话（最多 100 个，按更新时间排序）
npx -y bun ${SKILL_DIR}/scripts/main.ts --list-sessions
```

**批量处理最佳实践**:
- 当处理一个目录下的多个文件时，建议使用同一个 session ID
- 这样可以保持对话连续性，Gemini 能记住之前的上下文
- 示例：为目录生成固定的 session ID

```bash
# 为目录生成固定的 session ID（使用目录路径的 hash）
DIR_PATH="/path/to/project"
SESSION_ID=$(echo -n "$DIR_PATH" | md5sum | cut -d' ' -f1)

# 批量处理该目录下的文件，使用同一个 session ID
npx -y bun ${SKILL_DIR}/scripts/main.ts "生成第一张图" --sessionId "$SESSION_ID" --image img1.png
npx -y bun ${SKILL_DIR}/scripts/main.ts "生成第二张图" --sessionId "$SESSION_ID" --image img2.png
npx -y bun ${SKILL_DIR}/scripts/main.ts "生成第三张图" --sessionId "$SESSION_ID" --image img3.png
```

会话文件存储在 `~/Library/Application Support/pw-skills/gemini-web/sessions/<id>.json` 中，包含:
- `id`: 会话 ID
- `metadata`: 用于继续的 Gemini 聊天元数据
- `messages`: `{role, content, timestamp, error?}` 数组
- `createdAt`, `updatedAt`: 时间戳

## 扩展支持

通过 EXTEND.md 进行自定义配置。

**检查路径** (优先级顺序):
1. `.pw-skills/pw-danger-gemini-web/EXTEND.md` (项目级)
2. `~/.pw-skills/pw-danger-gemini-web/EXTEND.md` (用户级)

如果找到，在工作流之前加载。扩展内容会覆盖默认值。

## 常见错误和解决方案

### 认证相关错误

**错误: "Cookie expired" 或 "Authentication failed"**
- 原因: Cookie 已过期或无效
- 解决方案:
  ```bash
  # 重新登录刷新 cookie
  npx -y bun ${SKILL_DIR}/scripts/main.ts --login
  ```

**错误: "Browser not found"**
- 原因: 系统中未找到支持的浏览器
- 解决方案:
  - 安装 Chrome、Chromium 或 Edge
  - 或使用环境变量指定浏览器路径:
    ```bash
    GEMINI_WEB_CHROME_PATH=/path/to/chrome npx -y bun ${SKILL_DIR}/scripts/main.ts --login
    ```

**错误: "Login timeout" 或登录窗口一直等待**
- 原因: 登录流程未完成
- 解决方案:
  - 确保在浏览器中完成完整的登录流程
  - 处理多因素认证 (如果启用)
  - 登录成功后浏览器会在 3 秒后自动关闭
  - 没有超时限制，可以慢慢完成登录

### 网络相关错误

**错误: "Connection refused" 或 "Network error"**
- 原因: 无法访问 Google 服务 (常见于中国大陆)
- 解决方案: 配置代理
  ```bash
  HTTP_PROXY=http://127.0.0.1:7890 HTTPS_PROXY=http://127.0.0.1:7890 \
  npx -y bun ${SKILL_DIR}/scripts/main.ts "你好"
  ```
- 注意: 环境变量必须与命令内联设置

**错误: "Rate limit exceeded"**
- 原因: 请求频率过高触发限流
- 解决方案:
  - 降低请求频率
  - 在请求之间添加延迟
  - 避免短时间内大量请求

### 图像相关错误

**错误: "Failed to save image" 或 "Directory not found"**
- 原因: 目标目录不存在
- 解决方案:
  ```bash
  # 确保目录存在
  mkdir -p /path/to/output
  npx -y bun ${SKILL_DIR}/scripts/main.ts "一只猫" --image /path/to/output/cat.png
  ```

**错误: "Image generation failed"**
- 原因: Gemini 无法根据提示生成图像
- 解决方案:
  - 检查提示是否清晰明确
  - 避免违反内容政策的提示
  - 尝试重新表述提示
  - 使用不同的模型 (如 gemini-3-pro)

**错误: "Reference image not found"**
- 原因: 参考图像路径不存在
- 解决方案:
  - 检查文件路径是否正确
  - 使用绝对路径避免相对路径问题
  - 确保文件格式受支持 (PNG, JPG, JPEG, WebP)

### 会话相关错误

**错误: "Session not found"**
- 原因: 指定的 session ID 不存在
- 解决方案:
  - 使用 `--list-sessions` 查看可用会话
  - 确保 session ID 拼写正确
  - 首次使用会自动创建新会话

**错误: "Session corrupted"**
- 原因: 会话文件损坏
- 解决方案:
  ```bash
  # 删除损坏的会话文件
  rm ~/Library/Application\ Support/pw-skills/gemini-web/sessions/<session-id>.json
  # 或在 Linux 上
  rm ~/.local/share/pw-skills/gemini-web/sessions/<session-id>.json
  ```

### 其他错误

**错误: "Bun not found"**
- 原因: 系统中未安装 Bun
- 解决方案: `npx -y bun` 会自动下载 Bun，无需手动安装

**错误: "Permission denied"**
- 原因: 没有写入权限
- 解决方案:
  - 检查输出目录权限
  - 检查数据目录权限
  - 使用有权限的路径

## 最佳实践

### Agent 使用建议

**1. Session ID 管理**
- 为每个独立任务生成唯一的 session ID
- 使用有意义的命名: `task-<uuid>` 或 `project-<hash>`
- 同一批次任务复用 session ID 保持上下文
- 示例:
  ```bash
  # 为目录生成固定 session ID
  SESSION_ID=$(echo -n "/path/to/project" | md5sum | cut -d' ' -f1)
  ```

**2. 错误处理**
- 始终检查命令退出码
- 使用 `--json` 输出便于解析结果
- 捕获并记录错误信息
- 示例:
  ```bash
  if ! output=$(npx -y bun ${SKILL_DIR}/scripts/main.ts "test" --json 2>&1); then
    echo "Error: $output"
    exit 1
  fi
  ```

**3. 代理配置**
- 在中国大陆环境自动添加代理环境变量
- 检测网络错误时提示用户配置代理
- 示例:
  ```bash
  # 检测是否需要代理
  if [[ $(curl -s -o /dev/null -w "%{http_code}" https://gemini.google.com) != "200" ]]; then
    echo "提示: 可能需要配置代理访问 Google 服务"
  fi
  ```

**4. 批量处理**
- 使用相同 session ID 处理相关任务
- 在请求之间添加适当延迟避免限流
- 使用 `--json` 输出便于批量解析
- 示例:
  ```bash
  for file in *.txt; do
    npx -y bun ${SKILL_DIR}/scripts/main.ts \
      --promptfiles "$file" \
      --sessionId "$SESSION_ID" \
      --image "${file%.txt}.png" \
      --json
    sleep 2  # 避免限流
  done
  ```

### 图像生成建议

**1. 提示词优化**
- 使用清晰、具体的描述
- 包含风格、色彩、构图等细节
- 避免模糊或抽象的表述
- 好的示例: "一张逼真的金毛猎犬幼犬照片，阳光明媚的草地背景，浅景深"
- 差的示例: "一只狗"

**2. 模型选择**
- 高质量图像: 使用 `gemini-3-pro`
- 快速预览: 使用 `gemini-2.5-flash`
- 复杂场景: 使用 `gemini-3-pro`

**3. 参考图像使用**
- 图生图: 提供清晰的参考图像和变化描述
- 图生文: 提供具体的描述要求
- 示例:
  ```bash
  # 基于参考图生成变体
  npx -y bun ${SKILL_DIR}/scripts/main.ts \
    --prompt "生成一个卡通风格的变体，保持主体不变" \
    --reference original.jpg \
    --image cartoon.png
  ```

### 多轮对话建议

**1. 上下文管理**
- 首次对话设置系统提示或角色
- 后续对话复用 session ID
- 示例:
  ```bash
  # 第一轮: 设置角色
  npx -y bun ${SKILL_DIR}/scripts/main.ts \
    "你是一个专业的图像描述专家" \
    --sessionId img-desc-001

  # 后续轮次: 描述图像
  npx -y bun ${SKILL_DIR}/scripts/main.ts \
    --prompt "描述这张图片" \
    --reference photo.jpg \
    --sessionId img-desc-001
  ```

**2. 会话清理**
- 定期清理不再需要的会话
- 使用 `--list-sessions` 查看会话列表
- 手动删除会话文件:
  ```bash
  # macOS
  rm ~/Library/Application\ Support/pw-skills/gemini-web/sessions/<id>.json

  # Linux
  rm ~/.local/share/pw-skills/gemini-web/sessions/<id>.json
  ```

### 性能优化

**1. 减少不必要的请求**
- 合并相关提示到一次请求
- 使用 `--promptfiles` 组合多个文件
- 避免重复生成相同内容

**2. 并行处理**
- 独立任务可以并行执行
- 使用不同 session ID 避免冲突
- 注意限流限制

**3. 缓存策略**
- Cookie 会自动缓存，无需每次登录
- 会话数据持久化，可复用上下文
- 生成的图像保存到本地，避免重复生成

### 安全建议

**1. 凭证管理**
- Cookie 文件包含敏感信息，注意保护
- 不要将 cookie 文件提交到版本控制
- 定期刷新 cookie 保持安全性

**2. 内容审查**
- 遵守 Google 内容政策
- 避免生成违规内容
- 注意版权和隐私问题

**3. 数据隐私**
- 会话数据存储在本地
- 提示内容会发送到 Google 服务器
- 不要在提示中包含敏感信息

## 故障排查清单

遇到问题时，按以下顺序检查:

1. **检查网络连接**
   ```bash
   curl -I https://gemini.google.com
   ```
   - 如果失败，配置代理

2. **检查认证状态**
   ```bash
   npx -y bun ${SKILL_DIR}/scripts/main.ts --login
   ```
   - 重新登录刷新 cookie

3. **检查浏览器**
   ```bash
   which chrome || which chromium || which microsoft-edge
   ```
   - 确保安装了支持的浏览器

4. **检查文件权限**
   ```bash
   ls -la ~/Library/Application\ Support/pw-skills/gemini-web/
   ```
   - 确保有读写权限

5. **检查输出目录**
   ```bash
   mkdir -p /path/to/output && ls -la /path/to/output
   ```
   - 确保目录存在且可写

6. **查看详细错误**
   ```bash
   npx -y bun ${SKILL_DIR}/scripts/main.ts "test" 2>&1 | tee error.log
   ```
   - 保存完整错误日志

7. **测试基本功能**
   ```bash
   # 测试文本生成
   npx -y bun ${SKILL_DIR}/scripts/main.ts "你好"

   # 测试图像生成
   npx -y bun ${SKILL_DIR}/scripts/main.ts "一只猫" --image test.png
   ```

## 技术限制

**已知限制:**
- 这是非官方 API，可能随时失效
- 没有官方支持或 SLA 保证
- 可能存在未知的限流限制
- API 变更可能导致功能中断
- 图像生成质量取决于 Gemini 模型能力

**不支持的功能:**
- 视频生成
- 音频生成
- 实时流式输出
- 批量 API 调用
- Webhook 回调

**性能特征:**
- 文本生成: 通常 2-5 秒
- 图像生成: 通常 10-30 秒
- 登录流程: 取决于用户操作速度
- 会话加载: 几乎即时

## 更新日志

查看项目 Git 历史了解最新变更:
```bash
cd ${SKILL_DIR}
git log --oneline --decorate
```
