---
name: dreamina-api-config
description: Dreamina API 基础配置，包含内网和公网 endpoint、headers 和通用参数
---

# Dreamina API 配置

## Base URL

### 公网 API (推荐)
```
https://jimeng.jianying.com/mweb/v1
```
- 无需内网环境
- 支持图片上传、生成、查询


## 公网 API Headers
```bash
Content-Type: application/json
Accept: application/json, text/plain, */*
Appid: 513695
Appvr: 5.8.0
Pf: 7
Origin: https://jimeng.jianying.com
Referer: https://jimeng.jianying.com
Cookie: sessionid=<your_sessionid>
Device-Time: <unix_timestamp>
Sign: <md5_signature>
Sign-Ver: 1
```

### Sign 签名生成
```python
import hashlib
import time

def generate_sign(uri_path):
    device_time = int(time.time())
    # uri_path 取最后7个字符
    sign_str = f"9e2c|{uri_path[-7:]}|7|5.8.0|{device_time}||11ac"
    sign = hashlib.md5(sign_str.encode()).hexdigest()
    return sign, device_time
```


## 通用参数
- `aid`: `513695`
- `device_platform`: `web`
- `region`: `CN`
- `submit_id`: UUID 格式，用于幂等

## model_key 枚举
| 模型 | model_key |
|---|---|
| 图片 4.5 | `high_aes_general_v40l` |
| 图片 4.1 | `high_aes_general_v41` |
| 图片 4.0 | `high_aes_general_v40` |
| 图片 3.1 | `high_aes_general_v30l_art_fangzhou:general_v3.0_18b` |
| 图片 3.0 | `high_aes_general_v30l:general_v3.0_18b` |

## image_ratio 枚举
| 比例 | image_ratio 值 |
|---|---|
| 21:9 | 0 |
| 16:9 | 1 |
| 3:2 | 2 |
| 4:3 | 3 |
| 1:1 | 8 |
| 3:4 | 4 |
| 2:3 | 5 |
| 9:16 | 6 |

## 分辨率尺寸

### 2K 分辨率 (4.x 模型)
| 比例 | 尺寸 |
|---|---|
| 21:9 | 3024x1296 |
| 16:9 | 2560x1440 |
| 3:2 | 2496x1664 |
| 4:3 | 2304x1728 |
| 1:1 | 2048x2048 |
| 3:4 | 1728x2304 |
| 2:3 | 1664x2496 |
| 9:16 | 1440x2560 |

### 1K 分辨率 (3.x 模型)
| 比例 | 尺寸 |
|---|---|
| 16:9 | 1664x936 |
| 1:1 | 1328x1328 |
| 9:16 | 936x1664 |

## 任务状态码
| status | 说明 |
|---|---|
| 20 | 队列中 |
| 42 | 处理中 |
| 45 | 处理中(中间状态) |
| 50 | 已完成 |
| 30 | 失败 |

## ImageX 上传服务
- 上传令牌: `https://jimeng.jianying.com/mweb/v1/get_upload_token`
- ImageX API: `https://imagex.bytedanceapi.com/`
- ServiceId: `tb4s082cfz`
