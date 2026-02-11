---
name: dreamina-super-resolution
description: 使用智能超清工具对图片进行高清放大 (pro_hd)
---

# 图片智能超清工具

## API 端点
```
POST https://jimeng.jianying.com/mweb/v1/aigc_draft/generate
```

## Python 示例

```python
import requests
import hashlib
import time
import uuid
import json

def generate_sign(uri_path):
    device_time = int(time.time())
    sign_str = f"9e2c|{uri_path[-7:]}|7|5.8.0|{device_time}||11ac"
    sign = hashlib.md5(sign_str.encode()).hexdigest()
    return sign, device_time

def super_resolution(sessionid, image_uri, resolution_type="4k", detail_strength=0.5):
    """
    智能超清 - 将图片放大到 4K 分辨率
    
    Args:
        sessionid: 登录 sessionid
        image_uri: 输入图片 URI (通过 upload_image 获取)
        resolution_type: "2k" 或 "4k"，默认 "4k"
        detail_strength: 细节生成程度 0-1，默认 0.5
    """
    uri = "/mweb/v1/aigc_draft/generate"
    sign, device_time = generate_sign(uri)
    
    component_id = str(uuid.uuid4())
    submit_id = str(uuid.uuid4())
    
    draft_content = {
        "type": "draft",
        "id": str(uuid.uuid4()),
        "min_version": "3.2.8",
        "min_features": ["AIGC_GenerateType_ProHD"],
        "is_from_tsn": True,
        "version": "3.3.8",
        "main_component_id": component_id,
        "component_list": [{
            "type": "image_base_component",
            "id": component_id,
            "min_version": "3.0.2",
            "aigc_mode": "workbench",
            "metadata": {
                "type": "",
                "id": str(uuid.uuid4()),
                "created_platform": 3,
                "created_time_in_ms": str(int(time.time() * 1000))
            },
            "generate_type": "pro_hd",
            "abilities": {
                "type": "",
                "id": str(uuid.uuid4()),
                "pro_hd": {
                    "type": "",
                    "id": str(uuid.uuid4()),
                    "resolution_type": resolution_type,
                    "hd_scene_type": "auto",
                    "original_image_strength": 0.65,
                    "detail_strength": detail_strength,
                    "postedit_param": {
                        "type": "",
                        "id": str(uuid.uuid4()),
                        "generate_type": 35,
                        "origin_image": {
                            "type": "image",
                            "id": str(uuid.uuid4()),
                            "source_from": "upload",
                            "platform_type": 1,
                            "image_uri": image_uri,
                            "uri": image_uri
                        }
                    }
                }
            }
        }]
    }
    
    headers = {
        "Content-Type": "application/json",
        "Appid": "513695",
        "Appvr": "5.8.0",
        "Pf": "7",
        "Origin": "https://jimeng.jianying.com",
        "Referer": "https://jimeng.jianying.com",
        "Cookie": f"sessionid={sessionid}",
        "Device-Time": str(device_time),
        "Sign": sign,
        "Sign-Ver": "1"
    }
    
    data = {
        "extend": {},
        "submit_id": submit_id,
        "draft_content": json.dumps(draft_content),
        "http_common_info": {"aid": 513695}
    }
    
    resp = requests.post(
        f"https://jimeng.jianying.com{uri}",
        params={
            "aid": 513695, 
            "device_platform": "web", 
            "region": "cn",
            "da_version": "3.3.8",
            "web_version": "7.5.0"
        },
        headers=headers,
        json=data
    )
    return resp.json()
```

## 参数说明
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| image_uri | string | 是 | 输入图片 URI (通过 upload_image 获取) |
| resolution_type | string | 否 | `2k` 或 `4k`，默认 `4k` |
| detail_strength | float | 否 | 细节生成程度 0-1，默认 0.5 |

## 关键参数
- **generate_type**: `pro_hd`
- **gen_type**: `35`
- **hd_scene_type**: `auto` (自动选择场景)

## 使用流程
1. 上传图片获取 `image_uri` (见 dreamina-upload-image)
2. 调用智能超清 API
3. 轮询查询结果 (见 dreamina-query-result)
4. 下载高清图片
