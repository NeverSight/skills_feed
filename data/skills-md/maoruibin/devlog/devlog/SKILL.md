---
name: devlog
description: 开发日志存档工具。将日常工作中的关键节点（调试、方案设计、故障排查）结构化记录到 Markdown 文件。支持全局/项目本地双模式存储，具备智能防重功能，便于后续生成周报。
license: MIT
---

# DevLog

开发者的"第二大脑"，将碎片化工作上下文结构化存储。

## 使用方式

```
/devlog <category> <title> [-d detail] [--here|--path DIR]
```

**分类 (category)**:
- `incident` - 线上故障（必填根因与修复）
- `feat` - 业务需求
- `design` - 技术方案
- `ops` - 运维部署
- `bug` - 常规 Bug
- `learn` - 技术调研

**存储选项**:
- 无参数 → 全局默认（首次运行时配置）
- `--here` → 项目本地 (`./.devlog/`)
- `--path DIR` → 自定义目录

## 示例

```bash
# 记录线上故障（全局）
devlog incident "首页Crash" -d "NPE in FeedAdapter.notifyDataSetChanged()，已添加空值检查"

# 记录技术方案（项目本地，可提交 git）
devlog design "Feed缓存策略" -d "Cache-Aside + TTL随机化" --here

# 记录常规 Bug
devlog bug "修复点赞数不刷新"

# 查看今日日志
devlog list --here
```

## 触发规则

**显式触发**（必须满足）：
- 用户说："记一下"、"存档"、"log this"、"archive"、"记录日志"
- 用户说中文："存一下"、"记录到日志"

**仅在这些场景下触发**：
- 完成一项明确的开发任务后（Debug成功、设计方案确认、代码实现完成）
- 用户明确要求记录时

**禁止隐式触发**：不要自动记录，始终让用户明确意图。

## 执行流程

1. **识别分类和内容**：根据用户输入判断分类和标题
2. **确定存储位置**：
   - 默认使用全局存储
   - 用户说"存到项目"、"here"、"本地"时使用 `--here`
   - 用户指定路径时使用 `--path`
3. **调用脚本**：
   ```bash
   python3 ~/.claude/skills/devlog/devlog.py <category> "<title>" -d "<detail>" [options]
   ```
4. **解析反馈**：将脚本的彩色输出转换为简洁的确认消息

## 反馈格式

执行成功后向用户展示：

```
✅ **已归档**
📂 `/path/to/file.md`
🏷️ [类别] 标题
```

## 输出格式

日志文件格式（Markdown）：

```markdown
# 📅 2026-01-21 Work Log

### [14:30] `@Weibo_Project` INCIDENT: 修复首页 Crash
> Root Cause: NPE in FeedAdapter.notifyDataSetChanged()
> Fix: 添加空值检查，已提交 PR #123

### [11:15] `@Weibo_Project` DESIGN: Feed 缓存策略方案
> 采用 Cache-Aside + TTL 随机化防止雪崩

---
```

## 配置

**首次运行**：首次使用时会提示选择全局日志目录
```
devlog feat "测试"     # 首次运行会触发配置向导
```

**配置管理命令**：
```bash
devlog config show     # 查看当前配置
devlog config reset    # 重置配置（重新触发向导）
```

**配置文件**：`~/.claude/skills/devlog/.config`（JSON 格式）

**环境变量**：支持 `DEVLOG_GLOBAL_DIR` 临时覆盖配置路径
