---
name: webapp-testing
description: "使用 Playwright 与本地 Web 应用交互与测试。支持验证前端功能、调试 UI、截图、查看浏览器日志。当需要测试本地 Web 应用时使用。"
license: MIT
---

# Web 应用测试

使用 Python + Playwright 编写本地 Web 应用测试脚本。

**辅助脚本**：`scripts/with_server.py` 管理服务生命周期（支持多服务）。  
**先执行 `--help`** 查看用法，勿优先读源码；脚本可能很大，作为黑盒调用即可。

## 流程选择

```
任务 → 是否纯静态 HTML？
    ├─ 是 → 直接读 HTML 找选择器 → 写 Playwright 脚本
    └─ 否（动态应用）→ 服务是否已启动？
        ├─ 否 → 运行 python scripts/with_server.py --help，再用该辅助脚本 + 简化 Playwright
        └─ 是 → 侦察再操作：
            1. 打开页面并 wait_for_load_state('networkidle')
            2. 截图或检查 DOM
            3. 从渲染结果确定选择器
            4. 用选择器执行操作
```

## 使用 with_server.py

**单服务**：
```bash
python scripts/with_server.py --server "npm run dev" --port 5173 -- python your_automation.py
```

**多服务（如前后端）**：
```bash
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- python your_automation.py
```

自动化脚本只写 Playwright 逻辑，服务由 with_server 管理：
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://localhost:5173')
    page.wait_for_load_state('networkidle')  # 关键：等 JS 执行完
    # ... 你的自动化逻辑
    browser.close()
```

## 侦察再操作

1. **查看 DOM**：`page.screenshot()`、`page.content()`、`page.locator(...).all()`  
2. 根据结果确定选择器  
3. 用选择器执行操作  

## 常见坑

❌ 动态应用在未 `networkidle` 前就检查 DOM  
✅ 先 `page.wait_for_load_state('networkidle')` 再检查  

## 实践建议

- 将 `scripts/` 当黑盒使用，`--help` 后直接调用  
- 使用 `sync_playwright()`，用毕关闭 browser  
- 选择器优先：`text=`、`role=`、CSS、ID  
- 适当 `wait_for_selector` 或 `wait_for_timeout`  

**参考**：原技能 `examples/` 下的 `element_discovery.py`、`static_html_automation.py`、`console_logging.py` 等。
