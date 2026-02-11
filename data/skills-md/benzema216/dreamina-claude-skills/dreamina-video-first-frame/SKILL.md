---
name: dreamina-video-first-frame
description: 将图片作为首帧生成视频 (gen_video)
---

# 首帧生视频工具

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
import random

def generate_sign(uri_path):
    device_time = int(time.time())
    sign_str = f"9e2c|{uri_path[-7:]}|7|5.8.0|{device_time}||11ac"
    sign = hashlib.md5(sign_str.encode()).hexdigest()
    return sign, device_time

def image_to_video(sessionid, image_uri, prompt, width=1536, height=1536, 
                   duration_ms=5000, resolution="720p", 
                   model="dreamina_ic_generate_video_model_vgfm_3.0_fast"):
    """
    首帧生视频 - 基于图片生成视频
    
    Args:
        sessionid: 登录 sessionid
        image_uri: 首帧图片 URI
        prompt: 视频运动描述
        width: 图片宽度
        height: 图片高度
        duration_ms: 视频时长毫秒 (3000-10000)
        resolution: 分辨率 "720p" 或 "1080p"
        model: 模型名称
    """
    uri = "/mweb/v1/aigc_draft/generate"
    sign, device_time = generate_sign(uri)
    
    component_id = str(uuid.uuid4())
    submit_id = str(uuid.uuid4())
    seed = random.randint(1000000000, 9999999999)
    
    aspect_ratio = f"{width}:{height}"
    if width == height:
        aspect_ratio = "1:1"
    elif width > height:
        aspect_ratio = "16:9"
    else:
        aspect_ratio = "9:16"
    
    draft_content = {
        "type": "draft",
        "id": str(uuid.uuid4()),
        "min_version": "3.2.5",
        "min_features": [],
        "is_from_tsn": True,
        "version": "3.3.8",
        "main_component_id": component_id,
        "component_list": [{
            "type": "video_base_component",
            "id": component_id,
            "min_version": "1.0.0",
            "aigc_mode": "workbench",
            "metadata": {
                "type": "",
                "id": str(uuid.uuid4()),
                "created_platform": 3,
                "created_time_in_ms": str(int(time.time() * 1000))
            },
            "generate_type": "gen_video",
            "abilities": {
                "type": "",
                "id": str(uuid.uuid4()),
                "gen_video": {
                    "type": "",
                    "id": str(uuid.uuid4()),
                    "text_to_video_params": {
                        "type": "",
                        "id": str(uuid.uuid4()),
                        "video_gen_inputs": [{
                            "type": "",
                            "id": str(uuid.uuid4()),
                            "min_version": "3.0.5",
                            "prompt": prompt,
                            "first_frame_image": {
                                "type": "image",
                                "id": str(uuid.uuid4()),
                                "source_from": "upload",
                                "platform_type": 1,
                                "image_uri": image_uri,
                                "width": width,
                                "height": height,
                                "uri": image_uri
                            },
                            "video_mode": 2,
                            "fps": 24,
                            "duration_ms": duration_ms,
                            "resolution": resolution,
                            "idip_meta_list": []
                        }],
                        "video_aspect_ratio": aspect_ratio,
                        "seed": seed,
                        "model_req_key": model,
                        "priority": 0
                    }
                }
            },
            "process_type": 1
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
        "extend": {
            "root_model": model,
            "m_video_commerce_info": {
                "benefit_type": "basic_video_operation_vgfm_v_three",
                "resource_id": "generate_video",
                "resource_id_type": "str",
                "resource_sub_type": "aigc"
            }
        },
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
| image_uri | string | 是 | 首帧图片 URI |
| prompt | string | 是 | 视频运动描述 |
| duration_ms | int | 否 | 时长毫秒 3000-10000，默认 5000 |
| resolution | string | 否 | 分辨率 720p/1080p，默认 720p |
| model | string | 否 | 模型名称，默认 vgfm_3.0_fast |

## 模型选项
| 模型 | 说明 |
|------|------|
| `dreamina_ic_generate_video_model_vgfm_3.0_fast` | 视频 3.0 Fast (推荐) |
| `dreamina_ic_generate_video_model_vgfm_3.0` | 视频 3.0 标准版 |

## 关键参数
- **generate_type**: `gen_video`
- **gen_type**: `10`
- **video_mode**: `2` (首帧模式)
- **fps**: `24`

## 描述要点
- **镜头运动**：推拉、摇移、跟随、升降、变焦
- **主体动作**：自然连续，幅度适中
- **背景动态**：风吹、光影变化、人群流动
- 镜头需遵循首帧角度

## 使用流程
1. 上传首帧图片获取 `image_uri`
2. 调用图生视频 API
3. 轮询查询结果 (视频生成较慢，建议 10 秒间隔)
4. 下载视频文件
