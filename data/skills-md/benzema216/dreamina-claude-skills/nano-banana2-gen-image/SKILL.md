---
name: nano-banana2-gen-image
description: 使用 nano-banana2 模型生成图片，支持多种比例和高质量输出
---

# nano-banana2 图片生成工具

## API 端点

### 生产环境
```
POST https://gpt-i18n.byteintl.net/gpt/openapi/online/multimodal/crawl?ak=gGoT3706okXuOVHBBhA1SBG8erOvgihU_GPT_AK
```

### 办公网络环境
```
POST https://genai-sg-og.tiktok-row.org/gpt/openapi/online/multimodal/crawl?ak=gGoT3706okXuOVHBBhA1SBG8erOvgihU_GPT_AK
```

## 完整请求示例

```python
import requests
import json
import base64
import uuid
from datetime import datetime

def generate_image_nano_banana(prompt, aspect_ratio="1:1", image_size="1K", network="production"):
    """
    使用 nano-banana2 生成图片
    
    Args:
        prompt: 图片描述提示词
        aspect_ratio: 图片比例，支持 21:9, 16:9, 4:3, 3:2, 1:1, 9:16, 3:4, 2:3, 5:4, 4:5
        image_size: 图片大小，支持 "1K" 或 "2K"
        network: 网络环境，"production" 或 "office"
    
    Returns:
        dict: 包含图片base64数据和元信息
    """
    
    # 选择正确的端点
    if network == "office":
        url = "https://genai-sg-og.tiktok-row.org/gpt/openapi/online/multimodal/crawl"
    else:
        url = "https://gpt-i18n.byteintl.net/gpt/openapi/online/multimodal/crawl"
    
    # 添加 API key
    url += "?ak=gGoT3706okXuOVHBBhA1SBG8erOvgihU_GPT_AK"
    
    # 生成 logid
    logid = f"nanobanana_{uuid.uuid4().hex}_{int(datetime.now().timestamp())}"
    
    headers = {
        "Content-Type": "application/json",
        "X-TT-LOGID": logid
    }
    
    data = {
        "stream": False,
        "model": "nano-banana2",
        "max_tokens": 20000,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ],
        "response_modalities": ["TEXT", "IMAGE"],
        "image_config": {
            "aspectRatio": aspect_ratio,
            "imageSize": image_size,
            "imageOutputOptions": {
                "mimeType": "image/png"
            }
        }
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        if result.get("code") == 0:
            # 提取图片数据
            messages = result.get("data", {}).get("choices", [])[0].get("message", {})
            multimodal_contents = messages.get("multimodal_contents", [])
            
            images = []
            for content in multimodal_contents:
                if content.get("type") == "inline_data":
                    image_data = content.get("inline_data", {})
                    images.append({
                        "base64": image_data.get("data"),
                        "mime_type": image_data.get("mime_type"),
                        "prompt": prompt,
                        "aspect_ratio": aspect_ratio
                    })
            
            return {
                "status": "success",
                "images": images,
                "logid": logid
            }
    
    return {
        "status": "error",
        "error": f"Request failed: {response.status_code}",
        "response": response.text
    }

def save_base64_image(base64_data, filename):
    """保存 base64 图片到文件"""
    image_data = base64.b64decode(base64_data)
    with open(filename, 'wb') as f:
        f.write(image_data)
    print(f"Image saved: {filename}")

# 使用示例
# result = generate_image_nano_banana("一只可爱的柴犬在公园里玩耍", aspect_ratio="16:9", image_size="2K")
# if result["status"] == "success" and result["images"]:
#     save_base64_image(result["images"][0]["base64"], "shiba_inu.png")
```

## Bash 命令示例

```bash
# 生成图片的 curl 命令
curl --location 'https://gpt-i18n.byteintl.net/gpt/openapi/online/multimodal/crawl?ak=gGoT3706okXuOVHBBhA1SBG8erOvgihU_GPT_AK' \
--header 'Content-Type: application/json' \
--header 'X-TT-LOGID: nanobanana_test_'$(date +%s) \
--data '{
    "stream": false,
    "model": "nano-banana2",
    "max_tokens": 20000,
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "生成一张南方小城老旧居民区的照片，写实风格"
                }
            ]
        }
    ],
    "response_modalities": ["TEXT","IMAGE"],
    "image_config": {
        "aspectRatio": "16:9",
        "imageSize": "2K",
        "imageOutputOptions": {
            "mimeType": "image/png"
        }
    }
}' | jq '.data.choices[0].message.multimodal_contents[] | select(.type=="inline_data") | .inline_data.data' -r | base64 -d > output.png
```

## 参数说明

### 必填参数
| 参数 | 类型 | 说明 |
|-----|-----|-----|
| messages | array | 用户消息数组，包含文本提示词 |
| model | string | 固定值 "nano-banana2" |

### 可选参数
| 参数 | 类型 | 默认值 | 说明 |
|-----|-----|-------|-----|
| aspect_ratio | string | "1:1" | 图片比例 |
| image_size | string | "1K" | 图片尺寸 |
| max_tokens | number | 20000 | 最大token数 |

### 支持的比例
- **横向**: 21:9, 16:9, 4:3, 3:2
- **方形**: 1:1
- **纵向**: 9:16, 3:4, 2:3
- **灵活**: 5:4, 4:5

### 图片尺寸
- **1K**: 标准质量（默认）
- **2K**: 高质量

## 响应处理

### 成功响应结构
```json
{
    "code": 0,
    "msg": "success",
    "data": {
        "choices": [{
            "finish_reason": "stop",
            "message": {
                "multimodal_contents": [
                    {
                        "type": "text",
                        "text": "好的，为你生成..."
                    },
                    {
                        "type": "inline_data",
                        "inline_data": {
                            "mime_type": "image/png",
                            "data": "base64_encoded_image_data"
                        }
                    }
                ]
            }
        }]
    }
}
```

### 提取图片数据
```python
# 从响应中提取所有图片
def extract_images(response_json):
    images = []
    choices = response_json.get("data", {}).get("choices", [])
    
    for choice in choices:
        contents = choice.get("message", {}).get("multimodal_contents", [])
        for content in contents:
            if content.get("type") == "inline_data":
                images.append(content.get("inline_data"))
    
    return images
```

## 使用建议

1. **提示词优化**
   - 使用详细的描述获得更好的结果
   - 指明风格、光线、氛围等细节
   - 可以使用中文或英文提示词

2. **比例选择**
   - 角色肖像：使用 2:3 或 3:4
   - 场景横幅：使用 16:9 或 21:9
   - 社交媒体：使用 1:1 或 9:16

3. **批量生成**
   - 可以通过多次调用实现批量生成
   - 建议每批控制在 5-10 张

4. **网络环境**
   - 办公网络使用 tiktok-row.org 域名
   - 其他环境使用 byteintl.net 域名

## 错误处理

```python
def handle_error(response):
    if response.status_code == 400:
        return "请求参数错误，请检查参数格式"
    elif response.status_code == 401:
        return "API Key 无效或过期"
    elif response.status_code == 429:
        return "请求频率过高，请稍后重试"
    else:
        return f"未知错误: {response.status_code}"
```

## 注意事项

1. **API Key 安全**：请勿在生产环境中硬编码 API Key
2. **图片存储**：生成的图片为 base64 格式，需要及时保存
3. **请求频率**：避免过于频繁的请求，建议间隔 1-2 秒
4. **内容审核**：生成内容需符合相关法律法规