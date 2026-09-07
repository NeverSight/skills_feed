---
name: polyv-scenario-setup
description: 快速配置直播场景（电商/教育/研讨会等）
parameters:
  scenario:
    type: string
    required: false
    description: 场景名称 (e-commerce, education, webinar, marketing)
    default: interactive
---

# PolyV 场景快速配置

帮助用户一键配置完整的直播场景环境。

## 使用方式

- `/polyv-scenario-setup` - 交互式选择场景
- `/polyv-scenario-setup e-commerce` - 电商直播场景
- `/polyv-scenario-setup education` - 在线教育场景
- `/polyv-scenario-setup webinar` - 企业研讨会场景
- `/polyv-scenario-setup marketing` - 营销活动场景

## 可用场景

| 场景 | 说明 | 创建资源 |
|-----|------|---------|
| e-commerce | 电商直播 | 频道(竖屏)、商品、优惠券 |
| education | 在线教育 | 频道(横屏)、课程商品 |
| webinar | 企业研讨会 | 频道、签到、问答 |
| marketing | 营销活动 | 频道、抽奖、优惠券 |

## 执行步骤

### 1. 检测认证状态

```bash
npx polyv-live-cli@latest account list
```

### 2. 配置认证（如需要）

如果用户未配置认证，引导用户提供 AppID 和 AppSecret：

```
请提供你的 PolyV AppID 和 AppSecret：
- 访问 https://console.polyv.net/ 后台获取
- 路径：云直播 -> 设置 -> 开发者信息
```

然后用用户提供的凭据配置：

```bash
npx polyv-live-cli@latest account add --name <name> --app-id <appId> --app-secret <appSecret>
npx polyv-live-cli@latest account set-default <name>
```

### 3. 交互式场景选择（无参数时）

如果用户未指定场景，展示可用场景列表并引导选择：

```
你想配置什么类型的直播场景？

[1] 电商带货 (e-commerce)
    - 适合：商品展示、直播带货
    - 包含：频道、商品、优惠券

[2] 在线教育 (education)
    - 适合：课程直播、培训教学
    - 包含：频道、课程商品

[3] 企业研讨会 (webinar)
    - 适合：企业会议、行业研讨
    - 包含：频道、签到、问答

[4] 营销活动 (marketing)
    - 适合：品牌推广、活动直播
    - 包含：频道、抽奖、优惠券

请输入场景编号或名称：
```

### 4. 查看场景详情（可选）

```bash
npx polyv-live-cli@latest setup --list --detailed
```

### 5. 预览资源（推荐）

执行前先预览将创建的资源：

```bash
npx polyv-live-cli@latest setup <scenario> --dry-run
```

### 6. 执行场景初始化

```bash
npx polyv-live-cli@latest setup <scenario>
```

## 示例对话

### 交互式使用

```
用户: /polyv-scenario-setup

AI: 你想配置什么类型的直播场景？

    [1] 电商带货 (e-commerce)
    [2] 在线教育 (education)
    [3] 企业研讨会 (webinar)
    [4] 营销活动 (marketing)

用户: 1

AI: 好的，我来帮你配置电商直播场景。
    先预览一下将创建的资源...

    [执行 dry-run]

    确认创建以上资源吗？(y/n)

用户: y

AI: [执行 setup e-commerce]
    电商直播环境配置完成！

    频道ID: 123456
    商品数: 3
    优惠券: 1
```

### 直接指定场景

```
用户: /polyv-scenario-setup e-commerce

AI: 配置电商直播场景...

    [执行 setup e-commerce]

    完成！已创建：
    - 频道: 电商直播间 (竖屏)
    - 商品: 3个示例商品
    - 优惠券: 新人满减券
```

## 扩展新场景

要添加新场景，需要：

1. 在 CLI 的 setup handler 中注册场景定义
2. 在此 skill 的可用场景表中添加说明
3. 定义场景创建的资源模板

## 注意事项

- 确保用户有足够的 API 配额
- 某些场景可能需要额外权限
- 建议先用 `--dry-run` 预览
