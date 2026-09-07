---
name: polyv-e-commerce-setup
description: 一键配置电商直播环境（频道、商品、优惠券）
---

# PolyV 电商场景快速配置

帮助用户一键配置完整的电商直播环境。

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

### 3. 执行场景初始化

```bash
npx polyv-live-cli@latest setup e-commerce
```

## 创建的资源

| 资源 | 说明 |
|-----|------|
| 频道 | 电商直播场景，竖屏 |
| 商品 | 示例商品 |
| 优惠券 | 新人满减券 |
