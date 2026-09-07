---
name: polyv-live-cli
description: 保利威官方 skill。通过 npm 发布版 polyv-live-cli 管理保利威云直播服务。用于查询或管理直播频道、推流地址和状态、商品、优惠券、回放、文档、场次、聊天、签到、问答、问卷、抽奖、打赏、观众、观看条件、白名单、平台设置、播放器、卡片推送、推广渠道、转播频道、AI 数字人、监控面板、场景初始化和直播统计。
allowed-tools: Bash(npx --yes polyv-live-cli@latest:*)
---

# 保利威云直播 CLI

以 npm 发布版 CLI 为准。不要根据旧示例、缓存文档、历史记忆或其他非发布版资料推断命令语法；只要能访问 npm，就先用发布版 `--help` 校验。

## CLI 前缀

本文档和 `references/` 中的 `<CLI>` 表示：

```bash
npx --yes polyv-live-cli@latest
```

执行命令前必须把 `<CLI>` 展开为上面的真实命令；不要直接执行字面量 `<CLI>`。如果 npm latest help 与 reference 冲突，必须以 npm latest 的 `<CLI> ... --help` 为准。

## 入口校验

先确认 npm 发布版命令面：

```bash
<CLI> --version
<CLI> --help
```

`<CLI> --version` 应返回当前 npm latest 版本。

每次处理某个命令族前，先运行最相关 help：

```bash
<CLI> <command> --help
<CLI> <command> <subcommand> --help
```

不要根据本地源码、旧示例、缓存文档或记忆推断 npm latest 语法。

## 认证预检

除 `--help`、`--version`、`account` 和 `use` 外，直播 API 命令通常需要账号配置。

执行业务命令前先检查：

```bash
<CLI> account current
<CLI> account list
```

缺少账号或默认账号时，停止并请用户提供凭据。不要回显 AppSecret。用户明确请求推流地址/推流密钥时，可以返回 `stream get-key -o json` 的推流凭证，但提醒只提供给可信推流端。

## 任务路由

自然语言任务先读 `references/task-routing.md`。如果仍不确定命令路径，再读 `references/command-index.md`，然后用对应 help 校验真实参数。

高频路由：

- 频道基础、状态、角色、装修、分发、MR、频道 token：`channel`
- 推流地址、直播状态、断流恢复、推流开关：`stream`
- 本地图片上传为公网图片 URL：`web image-upload`
- 观看页菜单、分享、退出跳转、页面信息、观看页打赏：`web`
- 播放器 Logo、水印、暖场、片头、暂停页：`player`
- 观看条件、鉴权、白名单观看：`watch-condition`、`whitelist`
- 回放、录制文件、合并、转码、断点续录：`playback`、`record`
- 文档、课件、多媒体资源关联：`document`
- 场次、外部 ID、场次统计：`session`、`statistics`
- 聊天消息、聊天开关、在线人数、禁言、踢人：`chat`
- 抽奖、签到、问答、问卷、打赏：`lottery`、`checkin`、`qa`、`questionnaire`、`donate`
- 互动脚本、互动监听、任务奖励、点赞/奖励：`interaction`
- 商品、优惠券、商品标签、商品统计/设置：`product`、`coupon`
- 卡片推送、推广渠道、转播频道：`card-push`、`promotion`、`transmit`
- 观众、用户自定义字段、邀请榜单：`viewer`、`custom-field`、`invite-sales`
- 平台/账号/全局设置、分组账号、伙伴账号：`platform`、`global`、`user`、`group`、`partner`
- 素材库、WebApp、机器人、财务/审核、AI 数字人：`material`、`webapp`、`robot`、`finance`、`ai`

## 风险规则

只读命令如 `list`、`get`、`detail`、`status`、`export` 通常可以直接执行。写入或影响生产状态的命令必须先确认，或者在用户已经明确授权时使用命令支持的 `--force`。

下列动词默认视为高风险：`create`、`add`、`update`、`delete`、`remove`、`clear`、`batch-delete`、`enable`、`disable`、`start`、`stop`、`end`、`push`、`send`、`import`、`apply`、`register`、`allocate`、`merge`、`transcode`、`resume`、`cancel`。

测试写入类真实命令时，优先临时创建频道或测试对象，结束后清理；不要默认修改用户长期使用的频道，除非用户明确指定并授权。

## 输出规则

做数据提取、对比、报告或后续脚本处理时，优先使用 JSON：

```bash
<CLI> channel list -o json
```

示例里的 `<频道ID>`、`<商品ID>`、`<回放ID>`、`<账号名>` 都是占位符。不要直接执行 reference 中的示例 ID。

## 本地图片与公网 URL

很多图片参数只接受可公网访问的 HTTP(S) URL，不接受本地文件路径。用户提供本地图片、截图或附件，并要求设置频道封面、直播引导图、播放器 logo、暖场图、广告图、打赏图标、邀请卡、菜单图片、管理员/助教头像等图片类配置时，先用通用上传命令得到图片 URL，再把返回的 URL 用到目标命令。

通用上传命令：

```bash
<CLI> web image-upload --type <图片类型> --files <本地图片路径> --force -o json
```

返回值是图片 URL 数组；单图场景通常取第一个 URL。`--type` 必须按用途选择并用 `web image-upload --help` 校验，常见值包括 `coverImage`、`splashImage`、`logoImage`、`warmImage`、`adImage`、`startAdImage`、`stopAdImage`、`goodImage`、`invitationImage`、`menuImage`、`adminAvatar`、`assistantAvatar`、`authCodeImage`。

示例流程：用户给本地 logo 并要求设置播放器 logo 时，先上传：

```bash
<CLI> web image-upload --type logoImage --files ./logo.png --force -o json
```

然后把返回的 URL 填入播放器或频道配置命令。不要把本地路径直接传给只接受图片 URL 的参数。

## 参考资料路由

按最小范围读取：

- `task-routing.md`：自然语言任务到命令族的映射。
- `command-index.md`：npm latest help 生成的一级命令和直接子命令索引。
- `authentication.md`：账号配置和认证来源。
- `channel-management.md`、`streaming.md`、`monitor.md`、`scene-setup.md`：频道和推流流程。
- `products.md`、`coupons.md`、`card-push.md`、`transmit.md`：商品、优惠券、卡片推送、转播等营销能力。
- `playback.md`、`record-settings.md`、`documents.md`、`session-management.md`：回放、录制、文档、场次。
- `chat-management.md`、`checkin.md`、`qa-questionnaire.md`、`lottery.md`、`donate.md`：直播互动工具。
- `viewer.md`、`viewer-management.md`、`watch-condition.md`、`whitelist.md`：观众、标签、观看条件、白名单。
- `platform.md`、`player.md`、`statistics.md`：平台设置、播放器配置、统计报表。
- `ai.md`、`finance.md`、`material.md`、`robot.md`、`webapp.md`：AI、财务审核、素材库、机器人、WebApp。
- `custom-field.md`、`invite-sales.md`、`user.md`、`group.md`、`global.md`、`partner.md`：用户、字段、邀请销售、分组、全局、伙伴账号。
- `interaction.md`、`promotion.md`、`web.md`：跨互动能力、推广渠道、观看页配置。

新增 npm latest 命令若没有专门 reference，先查 `command-index.md` 和对应 help，不要编造参数。

## 失败处理

参数解析失败时：

1. 对最深层命令重新运行 `--help`。
2. 检查 camelCase、kebab-case 和短参数是否真实存在。
3. 删除 help 没列出的参数。
4. 修正文档或回复时优先使用完整参数名。

API 阶段失败时：

1. 运行 `account current` 和 `account list`。
2. 用只读 `list`、`get`、`status` 命令核对账号、频道 ID 和对象 ID。
3. 报告实际错误和命令形态，不暴露 AppSecret。

## 官方资源与支持

以下入口用于了解产品、查阅业务 API 或联系人工支持；命令语法仍以当前 npm 发布版 `--help` 为准。

- 官网：https://www.polyv.net/
- 保利威直播 API 文档：https://help.polyv.net/#/live/api/
- 邮箱：support@polyv.net
- 技术支持：400-993-9533
