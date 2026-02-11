---
name: dreamina-query-result
description: 查询 Dreamina 生成任务结果，获取图片/视频下载链接
---

# 结果查询工具

## API 端点
```
POST https://jimeng.jianying.com/mweb/v1/get_history_by_ids
```

## Python 示例

```python
import requests
import hashlib
import time

def generate_sign(uri_path):
    device_time = int(time.time())
    sign_str = f"9e2c|{uri_path[-7:]}|7|5.8.0|{device_time}||11ac"
    sign = hashlib.md5(sign_str.encode()).hexdigest()
    return sign, device_time

def query_result(sessionid, history_ids):
    uri = "/mweb/v1/get_history_by_ids"
    sign, device_time = generate_sign(uri)
    
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
    
    resp = requests.post(
        f"https://jimeng.jianying.com{uri}",
        params={"aid": 513695, "device_platform": "web", "region": "CN"},
        headers=headers,
        json={"history_ids": history_ids, "http_common_info": {"aid": 513695}}
    )
    return resp.json()
```

## 响应结构 - 图片
```json
{
  "ret": "0",
  "data": {
    "<history_id>": {
      "status": 50,
      "item_list": [{
        "image": {
          "large_images": [{
            "image_uri": "tos-cn-i-tb4s082cfz/<hash>",
            "image_url": "https://p26-dreamina-sign.byteimg.com/...",
            "width": 2048,
            "height": 2048,
            "format": "png"
          }]
        }
      }]
    }
  }
}
```

## 响应结构 - 视频
```json
{
  "ret": "0",
  "data": {
    "<history_id>": {
      "status": 50,
      "item_list": [{
        "video": {
          "video_resource": {
            "video_url": "https://...",
            "video_uri": "tos-cn-v-xxx/...",
            "duration": 5000,
            "width": 1280,
            "height": 720
          }
        }
      }]
    }
  }
}
```

## 任务状态
| status | 说明 |
|--------|------|
| 20 | 队列中 |
| 42 | 处理中 |
| 45 | 处理中(中间状态) |
| 50 | 已完成 |
| 30 | 失败 |

## 轮询示例

```python
import time

def wait_for_result(sessionid, history_id, max_attempts=30, interval=3):
    for i in range(max_attempts):
        result = query_result(sessionid, [history_id])
        data = result.get('data', {}).get(history_id, {})
        status = data.get('status')
        
        if status == 50:
            item = data['item_list'][0]
            if 'image' in item:
                return item['image']['large_images'][0]['image_url']
            elif 'video' in item:
                return item['video']['video_resource']['video_url']
        elif status == 30:
            raise Exception(f"Generation failed: {data.get('fail_msg')}")
        
        time.sleep(interval)
    
    raise Exception("Timeout waiting for result")
```

## 下载资源

```python
def download_file(url, output_path):
    resp = requests.get(url, timeout=60)
    with open(output_path, 'wb') as f:
        f.write(resp.content)
    return len(resp.content)
```

## 注意事项
- 图片/视频 URL 带签名，约 1-2 小时过期
- 建议生成后立即下载
- 支持批量查询多个 history_id
- 图片轮询间隔 3 秒，视频 5-10 秒
